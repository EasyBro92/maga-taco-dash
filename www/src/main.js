import * as THREE from "../vendor/three.module.min.js";
import { createCharacter } from "./character.js";
import { createWorld, LANE_X, CIELO_Y } from "./world.js";
import { initControls, setSwipeThreshold } from "./controls.js";
import {
  sndTaco, sndJump, sndSlide, sndLaneSwitch, sndHit, sndPoint, unlockAudio, vibrate, startMusic,
  setSfxVolume, setSfxMuted, setMusicVolume, setMusicMuted,
} from "./audio.js";
import { getSave, addTacos, reportRunScore, getSettings, updateSettings, resetProgress, getNiveles, guardarNivel } from "./save.js";
import { NIVELES, piezasDeNivel, nivelAbierto, sinFinAbierto, usaKit } from "./levels.js";
import { PIEZAS_KIT } from "./edificios.js";
import { applyI18n, toggleLang, setLang, t, randomCatchphrase, getLang } from "./i18n.js";
import { initErrorReporting, reportError } from "./errors.js";
import { makePool } from "./pool.js";
import { loadZoneModels, modelo, cargarCarpeta, cargarPersonaje } from "./models.js";
import * as misiones from "./missions.js";

initErrorReporting();

// 24/10: arranque mas lento y subida mas suave (le mareaba ir tan rapido):
// de 13 a 25 en unos 100 s, en vez de 17 a 29 en 50 s.
const BASE_SPEED = 13;
const MAX_SPEED = 25;
const ACCEL = 0.12;
const JUMP_DURATION = 0.62;   // 26/10: mas rato en el aire (habia que estar muy encima para saltar)
const JUMP_HEIGHT = 1.7;
const SLIDE_DURATION = 0.5;
const STREAK_RESET_GAP = 2.2;
const MAGNET_DURATION = 6;
const BOOST_DURATION = 4;
const BOOST_MULT = 1.5;
// Fisica vertical de verdad (22/10/2026): hace falta para subir por la rampa
// del autobus, correr por el techo y caer al acabarse. Gravedad y velocidad
// de salto salen de la altura y la duracion de siempre, asi que el salto en
// el suelo se siente exactamente igual que antes.
const GRAVEDAD = 8 * JUMP_HEIGHT / (JUMP_DURATION * JUMP_DURATION);
const V_SALTO = 4 * JUMP_HEIGHT / JUMP_DURATION;
// Modo gigante (gorra roja): el personaje crece y aplasta lo que toca.
const MEGA_DURATION = 7;
const MEGA_SCALE = 1.7;
// Rayo congelador, cohete y jefe (22/10/2026, mas Minion Rush).
const FREEZE_DURATION = 6;
const ROCKET_DURATION = 6.5;
const JEFE_PRIMERO = 1200;   // metros hasta el primer Burrito-Bot
const JEFE_CADA = 2000;      // y luego cada tantos

// ---------- Soporte WebGL ----------
function hasWebGL() {
  try {
    const test = document.createElement("canvas");
    return !!(window.WebGLRenderingContext && (test.getContext("webgl") || test.getContext("experimental-webgl")));
  } catch (e) {
    return false;
  }
}

function showWebglError() {
  document.getElementById("loadingScreen").classList.add("hidden");
  document.getElementById("webglError").classList.remove("hidden");
}

if (!hasWebGL()) {
  showWebglError();
  throw new Error("WebGL no soportado en este dispositivo.");
}

// ---------- Calidad grafica ----------
// antialias solo puede fijarse al crear el WebGLRenderer, por eso la
// calidad se lee de guardado ANTES de crearlo; cambiarla desde Ajustes
// recarga la pagina para aplicarse limpiamente.
const QUALITY_PRESETS = {
  low: { antialias: false, pixelRatioCap: 1 },
  medium: { antialias: false, pixelRatioCap: 1.5 },
  high: { antialias: true, pixelRatioCap: 2 },
};
const quality = QUALITY_PRESETS[getSettings().graphicsQuality] || QUALITY_PRESETS.high;
const shadowsEnabled = getSettings().graphicsQuality !== "low";

// ---------- Render setup ----------
const canvas = document.getElementById("game");
let renderer;
try {
  renderer = new THREE.WebGLRenderer({ canvas, antialias: quality.antialias });
} catch (e) {
  reportError("No se pudo crear el WebGLRenderer", { stack: e.stack });
  showWebglError();
  throw e;
}
renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, quality.pixelRatioCap));
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.12;
renderer.outputColorSpace = THREE.SRGBColorSpace;
if (shadowsEnabled) {
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
}

let contextLost = false;
canvas.addEventListener("webglcontextlost", (e) => {
  e.preventDefault();
  contextLost = true;
  reportError("Contexto WebGL perdido");
  document.getElementById("webglError").classList.remove("hidden");
}, false);
canvas.addEventListener("webglcontextrestored", () => {
  // Three.js no puede re-subir texturas/geometrias de forma fiable sin
  // volver a construir toda la escena: recargar es la recuperacion mas
  // simple y robusta tras perder el contexto (comun en moviles con poca RAM).
  window.location.reload();
});

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(55, 1, 0.1, 320);   // 25/10: de 150 a 320 (ver SPAWN_Z en world.js)

// Camara elevada y alejada tipo Minion Rush: el personaje se ve pequeno,
// se ve mucho tramo de pista por delante para reaccionar con tiempo.
// 24/10: mas alta y mas lejos (lo pidio contra el mareo): el suelo pasa mas
// despacio por la pantalla y se ve mas pista por delante.
const RACE_CAM = { pos: new THREE.Vector3(0, 7.2, 9.8), look: new THREE.Vector3(0, 0.4, -18) };
// Camara de menu por delante y a un lado: el personaje corre alejandose, asi
// que con la posicion antigua (z positivo) el menu solo enseñaba su espalda y
// la mochila. Ahora se le ve la cara y el traje, que es lo que da personalidad
// a la pantalla de inicio.
// Apunta por debajo del pecho (y=0.45) para que el personaje quede en la
// mitad ALTA del encuadre y se le vea la cara y el traje por encima de la
// tarjeta del menu, que ocupa el centro de la pantalla.
// 24/10: algo mas lejos para el presidente de Meshy, que es mas alto que el muñeco.
const MENU_CAM = { pos: new THREE.Vector3(-2.3, 1.9, -6.2), look: new THREE.Vector3(0, 0.05, 0) };
function setCameraMode(mode) {
  const c = mode === "menu" ? MENU_CAM : RACE_CAM;
  camera.position.copy(c.pos);
  camera.lookAt(c.look);
}
setCameraMode("menu");

// Iluminacion brillante y pareja tipo "juguete" (referencia: Subway
// Surfers) -- ambiente alto + relleno frontal suave para que no haya
// lados oscuros marcados, y el sol solo aporta el brillo especular del
// MeshPhongMaterial y la sombra proyectada.
const hemi = new THREE.HemisphereLight(0xcfeeff, 0x8a7a5a, 0.95);
const sun = new THREE.DirectionalLight(0xfff6e0, 1.05);
sun.position.set(4, 8, 4);
if (shadowsEnabled) {
  sun.castShadow = true;
  sun.shadow.mapSize.set(1024, 1024);
  const cam = sun.shadow.camera;
  cam.left = -6; cam.right = 6; cam.top = 4; cam.bottom = -6;
  cam.near = 1; cam.far = 20;
  sun.shadow.bias = -0.004;
  sun.target.position.set(0, 0, 0);
  scene.add(sun.target);
}
const fill = new THREE.DirectionalLight(0xffffff, 0.35);
fill.position.set(-3, 4, -6);
scene.add(hemi, sun, fill);

// Destello de sol: sprite radial (textura generada en canvas) anclado a la
// escena, no al grupo que hace scroll, para que nunca se quede atras.
function makeGlowTexture() {
  const size = 128;
  const c = document.createElement("canvas");
  c.width = c.height = size;
  const ctx = c.getContext("2d");
  const grad = ctx.createRadialGradient(size / 2, size / 2, 0, size / 2, size / 2, size / 2);
  grad.addColorStop(0, "rgba(255,250,220,0.9)");
  grad.addColorStop(0.4, "rgba(255,240,190,0.45)");
  grad.addColorStop(1, "rgba(255,240,190,0)");
  ctx.fillStyle = grad;
  ctx.fillRect(0, 0, size, size);
  return new THREE.CanvasTexture(c);
}
const sunGlare = new THREE.Sprite(new THREE.SpriteMaterial({
  map: makeGlowTexture(), transparent: true, depthWrite: false, depthTest: false, blending: THREE.AdditiveBlending,
}));
sunGlare.scale.set(16, 16, 1);
sunGlare.position.set(9, 16, -35);
sunGlare.renderOrder = -1;
scene.add(sunGlare);

// Las piezas de Blender tienen que estar antes de crear el mundo (los pools
// de decorado se llenan al crearlo). Si alguna falla, world.js usa la antigua.
{
  const barra = document.querySelector(".loadingBarFill");
  try {
    await Promise.all([cargarPersonaje(), loadZoneModels((n, total) => {
      if (barra) barra.style.width = `${Math.round(20 + 80 * n / total)}%`;
    })]);
  } catch (e) {
    console.warn("Modelos de Blender no cargados", e);
  }
}
const world = createWorld(scene);

const character = createCharacter(getSave().equipped);
character.object3D.position.set(0, 0, 0);
scene.add(character.object3D);

// El cohete en el que se monta (oculto hasta coger el potenciador). Viene con
// la punta hacia +z y el personaje corre hacia -z: se gira media vuelta, y se
// baja para que el personaje quede sentado encima.
const monturaCohete = modelo("obstaculos/cohete");
if (monturaCohete) {
  monturaCohete.rotation.y = Math.PI;
  monturaCohete.position.set(0, -0.92, 0.2);
  monturaCohete.visible = false;
  character.object3D.add(monturaCohete);
}

// ---- Misiones: lista en el menu y al acabar, y aviso al cumplir una ----
function pintarMisiones(id) {
  const el = document.getElementById(id);
  if (!el) return;
  el.innerHTML = `<div class="zoneLabel">🎯 ${t("misiones")}</div>` + misiones.activas().map((m) => {
    const meta = Math.round(misiones.metaDe(m));
    const hecho = Math.min(meta, Math.floor(m.hecho));
    return `<div class="mision"><div class="misionFila"><span>${t("mis_" + m.tipo).replace("{n}", meta)}</span>`
      + `<span class="misionPremio">+${misiones.premioDe(m)} 🌮</span></div>`
      + `<div class="misionBarra"><div style="width:${(100 * hecho / meta).toFixed(0)}%"></div></div></div>`;
  }).join("");
}
const colaAvisos = [];
let avisoVisible = false;
function avisarMisiones(cumplidas) {
  for (const c of cumplidas) colaAvisos.push(`${t("misionCumplida")} +${c.premio} 🌮`);
  if (!avisoVisible) siguienteAviso();
}
function siguienteAviso() {
  const el = document.getElementById("misionToast");
  const texto = colaAvisos.shift();
  if (!texto) { avisoVisible = false; el.classList.add("hidden"); return; }
  avisoVisible = true;
  el.textContent = texto;
  el.classList.remove("hidden");
  el.style.animation = "none"; void el.offsetWidth; el.style.animation = "";
  sndPoint();
  setTimeout(siguienteAviso, 2400);
}
pintarMisiones("misionesMenu");

// ================================================================
// ---- La gira hasta la Casa Blanca (24/10/2026) ----
// Niveles con calle real y final. `nivelActual` = null es el modo sin fin.
// ================================================================
let nivelActual = null;
let fin = null;

// Luz del nivel. El atardecer: sol bajo, dorado y de lado; cielo calido.
const LUZ_NORMAL = { sun: sun.color.getHex(), sunI: sun.intensity, sunPos: sun.position.clone(), hemi: hemi.color.getHex(), suelo: hemi.groundColor.getHex() };
function aplicarLuz(luz) {
  if (luz === "manana") {
    // Mañana: sol claro y algo bajo, de frente a la derecha; cielo limpio.
    sun.color.set(0xfff1d8); sun.intensity = 1.15; sun.position.set(6, 9, -5);
    hemi.color.set(0xe6f1ff); hemi.groundColor.set(0x8a8070);
  } else if (luz === "atardecer") {
    sun.color.set(0xffc690); sun.intensity = 1.25; sun.position.set(-7, 5, 2);
    hemi.color.set(0xffe2c4); hemi.groundColor.set(0x7a6656);
  } else {
    sun.color.set(LUZ_NORMAL.sun); sun.intensity = LUZ_NORMAL.sunI; sun.position.copy(LUZ_NORMAL.sunPos);
    hemi.color.set(LUZ_NORMAL.hemi); hemi.groundColor.set(LUZ_NORMAL.suelo);
  }
}

function mostrarBanner(n) {
  const el = document.getElementById("bannerNivel");
  el.querySelector(".bnNumero").textContent = `${t("nivel")} ${n.numero}`;
  el.querySelector(".bnNombre").textContent = n.nombre;
  el.querySelector(".bnLugar").textContent = n.lugar;
  el.classList.remove("hidden");
  el.style.animation = "none"; void el.offsetWidth; el.style.animation = "";
  clearTimeout(mostrarBanner.t);
  mostrarBanner.t = setTimeout(() => el.classList.add("hidden"), 2800);
}

// ---- El mapa de la gira ----
const SILUETA_EEUU = "8,8 6,14 5,22 7,30 10,38 14,45 20,47 26,50 33,52 38,51 44,54 47,60 52,57 55,52 60,50 66,51 72,52 76,58 79,57 77,50 80,44 84,40 86,34 90,28 94,22 96,16 95,12 88,16 82,20 76,18 70,14 60,12 40,10 20,8";
let nivelElegido = null;
function abrirMapa() {
  const svg = document.getElementById("mapaSvg");
  const hechos = getNiveles();
  const ruta = NIVELES.map((n) => n.mapa.join(",")).join(" ");
  svg.innerHTML = `<polygon class="tierra" points="${SILUETA_EEUU}"/><polyline class="ruta" points="${ruta}"/>`
    + NIVELES.map((n) => {
      const [x, y] = n.mapa;
      const abierto = nivelAbierto(n, hechos);
      const color = hechos[n.id] ? "#2fa84f" : abierto ? "#e8463c" : "#a7b0c0";
      return `<g class="parada" data-id="${n.id}"><circle cx="${x}" cy="${y}" r="3.2" fill="${color}"/>`
        + `<text x="${x}" y="${y + 1.1}">${abierto || hechos[n.id] ? n.numero : "🔒"}</text><text class="etiqueta" x="${x}" y="${y + 6.2}">${n.lugar}</text></g>`;
    }).join("");
  // El autobus de campaña, en el nivel abierto mas avanzado.
  const actual = [...NIVELES].reverse().find((n) => nivelAbierto(n, hechos)) || NIVELES[0];
  svg.innerHTML += `<text x="${actual.mapa[0] - 6}" y="${actual.mapa[1] - 4}" font-size="5">🚌</text>`;
  svg.querySelectorAll(".parada").forEach((g) => g.addEventListener("click", () => elegirNivel(g.dataset.id)));
  elegirNivel(nivelElegido || actual.id);
  document.getElementById("startScreen").classList.add("hidden");
  document.getElementById("mapaGira").classList.remove("hidden");
}
function elegirNivel(id) {
  const n = NIVELES.find((x) => x.id === id);
  nivelElegido = id;
  const hecho = getNiveles()[id];
  const est = hecho ? "★".repeat(hecho.estrellas) + "☆".repeat(3 - hecho.estrellas) : "☆☆☆";
  const abierto = nivelAbierto(n, getNiveles());
  const i = NIVELES.indexOf(n);
  // Cerrado: si existe y falta pasar el anterior, se dice cual; si no existe, proximamente.
  const cierre = !n.listo ? t("proximamente")
    : `🔒 ${t("superaAntes").replace("{n}", NIVELES[i - 1] ? NIVELES[i - 1].nombre : "")}`;
  document.getElementById("mapaInfo").innerHTML =
    `<div class="miNombre">${n.ingrediente || ""} ${t("nivel")} ${n.numero} · ${n.nombre}</div><div class="miLugar">${n.lugar}</div>`
    + (n.historia ? `<div class="miHistoria">${n.historia[getLang()] || n.historia.es}</div>` : "")
    + (abierto ? `<div class="miEstrellas">${est}</div><button id="mapaJugar" class="bigBtn">${t("jugarNivel")}</button>`
      : `<div class="proximamente">${cierre}</div>`);
  const b = document.getElementById("mapaJugar");
  if (b) b.addEventListener("click", () => empezarNivel(n));
}
async function empezarNivel(n) {
  if (!nivelAbierto(n, getNiveles()) && !PRUEBA) return;
  const boton = document.getElementById("mapaJugar");
  // Bajar los edificios del nivel la primera vez (se quedan para la siguiente).
  const piezas = piezasDeNivel(n);
  await cargarCarpeta(n.carpeta, piezas, (h, total) => { if (boton) boton.textContent = `${Math.round((100 * h) / total)}%`; });
  if (usaKit(n)) await cargarCarpeta("kit", PIEZAS_KIT);
  for (const k of n.acera || []) { const [c, p] = k.split("/"); await cargarCarpeta(c, [p]); }
  nivelActual = n;
  unlockAudio();
  startMusic();
  resetRun();
  gameState = "playing";
  document.getElementById("mapaGira").classList.add("hidden");
  document.getElementById("startScreen").classList.add("hidden");
  document.getElementById("hud").classList.remove("hidden");
}

// ---- Llegada a la Casa Blanca: unos 10 segundos ----
// 0 frena y anda hasta la escalinata · 1 sube al portico y llega a la puerta
// · 2 se da la vuelta y saluda · 3 se gira y entra · 4 se cierran las puertas.
function iniciarFinal() {
  gameState = "final";
  fin = { fase: 0, t: 0, v: speed, look: new THREE.Vector3(0, 0.4, -18) };
  currentLane = 1;
  isSliding = false; character.setSlidePose(false);
  rocketTimeLeft = 0; freezeTimeLeft = 0; megaTimeLeft = 0; character.setMega(1);
  if (monturaCohete) monturaCohete.visible = false;
  world.setCielo(false);
  document.getElementById("hud").classList.add("hidden");
  document.getElementById("powerupBadge").classList.add("hidden");
  speedLinesEl.style.opacity = "0";
}
function frameFinal(dt) {
  fin.t += dt;
  const cb = world.getCasaBlanca();
  if (!cb) { completarNivel(); return; }
  if (nivelActual.final === "camion") { finalCamion(dt, cb); return; }
  const zPasos = cb.position.z + 8.8;     // pie de la escalinata del portico norte
  const zPuerta = cb.position.z + 0.06;
  // Por el camino de coches: en el jardin la fuente queda en medio, asi que
  // entre 31 y 9 de la fachada se rodea por la curva de la derecha (radio 11).
  const u = -cb.position.z;
  const xCamino = u > 9 && u < 31 ? 11 * Math.sin(((u - 9) / 22) * Math.PI) : 0;
  playerX += (xCamino - playerX) * Math.min(1, dt * 6);
  let dz = 0;
  if (fin.fase === 0) {
    fin.v = Math.max(7, Math.min(fin.v - dt * 5, -zPasos * 1.6 + 6));
    dz = fin.v * dt;
    character.updateRun(dt, Math.max(0.45, fin.v / BASE_SPEED));
    if (zPasos + dz >= 0) fin.fase = 1;
  } else if (fin.fase === 1) {
    dz = 2.6 * dt;
    py = Math.min(1, Math.max(0, zPasos / 1.8));
    character.updateRun(dt, 0.45);
    if (zPuerta + dz >= -1.4) { fin.fase = 2; fin.t = 0; showBubble(t("finCasaBlanca")); vibrate([30, 40, 30]); }
  } else if (fin.fase === 2) {
    character.object3D.rotation.y += (Math.PI - character.object3D.rotation.y) * Math.min(1, dt * 5);
    character.setIdlePose(fin.t + 1);
    if (fin.t > 2.6) { fin.fase = 3; fin.t = 0; }
  } else if (fin.fase === 3) {
    character.object3D.rotation.y += (0 - character.object3D.rotation.y) * Math.min(1, dt * 6);
    if (fin.t > 0.45) { dz = 2.2 * dt; character.updateRun(dt, 0.4); }
    if (zPuerta + dz > 0.9) { fin.fase = 4; fin.t = 0; character.object3D.visible = false; }
  } else if (fin.fase === 4) {
    const k = Math.min(1, fin.t / 0.9);
    const suave = k * k * (3 - 2 * k);
    for (const h of cb.userData.puertas || []) h.rotation.y = Math.PI / 2 + (h.userData.cerrada - Math.PI / 2) * suave;
    if (fin.t > 1.7) { fin.fase = 5; completarNivel(); }
  }
  if (dz) world.update(dz);
  character.object3D.position.set(playerX, py, 0);
  shadowBlob.position.set(playerX, py + 0.015, 0);
  // Camara de cine: baja y se acerca a medida que llega al portico.
  const cerca = fin.fase >= 2;
  const objetivo = cerca ? new THREE.Vector3(1.2, 3.4 + py, 12.5) : new THREE.Vector3(playerX * 0.6, 4.4 + py, 11);
  const mira = cerca ? new THREE.Vector3(0, 3.6 + py, -3) : new THREE.Vector3(playerX * 0.8, 2.6 + py, -6);
  camera.position.lerp(objetivo, Math.min(1, dt * 1.6));
  fin.look.lerp(mira, Math.min(1, dt * 1.6));
  camera.lookAt(fin.look);
}
// Llegada al camion de tacos (Nueva York): frena, se planta delante, se da la
// vuelta y saluda con la tortilla recuperada.
function finalCamion(dt, flat) {
  const zParada = flat.position.z + 21.6 + 1.6;   // delante del morro del camion
  playerX += (0 - playerX) * Math.min(1, dt * 4);
  let dz = 0;
  if (fin.fase === 0) {
    fin.v = Math.max(5, Math.min(fin.v - dt * 6, -zParada * 1.5 + 4));
    dz = fin.v * dt;
    character.updateRun(dt, Math.max(0.45, fin.v / BASE_SPEED));
    if (zParada + dz >= 0) { dz = Math.max(0, -zParada); fin.fase = 2; fin.t = 0; showBubble(nivelActual.fin[getLang()] || nivelActual.fin.es); vibrate([30, 40, 30]); }
  } else if (fin.fase === 2) {
    character.object3D.rotation.y += (Math.PI - character.object3D.rotation.y) * Math.min(1, dt * 5);
    character.setIdlePose(fin.t + 1);
    if (fin.t > 2.8) { fin.fase = 5; completarNivel(); }
  }
  if (dz) world.update(dz);
  py = 0;
  character.object3D.position.set(playerX, 0, 0);
  shadowBlob.position.set(playerX, 0.015, 0);
  const cerca = fin.fase >= 2;
  const objetivo = cerca ? new THREE.Vector3(2.0, 3.2, 9.5) : new THREE.Vector3(0, 4.6, 11);
  const mira = cerca ? new THREE.Vector3(0, 2.2, -3) : new THREE.Vector3(0, 2.4, -8);
  camera.position.lerp(objetivo, Math.min(1, dt * 1.6));
  fin.look.lerp(mira, Math.min(1, dt * 1.6));
  camera.lookAt(fin.look);
}

function completarNivel() {
  gameState = "completado";
  const n = nivelActual;
  const tacos = Math.floor(tacosThisRun);
  const estrellas = n.estrellas.filter((e) => tacos >= e).length;
  addTacos(tacos);
  guardarNivel(n.id, estrellas);
  avisarMisiones([...misiones.evento("tacos", tacosThisRun), ...misiones.evento("distancia", distance)]);
  document.getElementById("nivelFinTitulo").textContent = n.id === "washington" ? t("llegadaCasaBlanca")
    : n.fin ? (n.fin[getLang()] || n.fin.es) : t("nivelSuperado");
  pintarSinFin();
  document.getElementById("nivelFinEstrellas").textContent = "★".repeat(estrellas) + "☆".repeat(3 - estrellas);
  document.getElementById("nivelFinTacos").textContent = tacos;
  pintarMisiones("misionesNivel");
  document.getElementById("nivelFin").classList.remove("hidden");
  spawnConfetti(45);
}

// ---- Jefe: barra de vida y premio ----
world.onJefe((evento, vida) => {
  const barra = document.getElementById("bossBar");
  if (evento === "golpe") {
    document.getElementById("bossFill").style.width = `${(vida / 5) * 100}%`;
    triggerCameraShake(0.03);
    flashExpression("happy", 0.5);
  } else if (evento === "derrotado") {
    document.getElementById("bossFill").style.width = "0%";
    tacosThisRun += 150;
    showBubble(t("jefeVencido") + " +150 🌮");
    spawnConfetti(30);
    triggerCameraShake(0.06);
    vibrate([40, 30, 80]);
    avisarMisiones(misiones.evento("jefe"));
    setTimeout(() => barra.classList.add("hidden"), 1500);
  } else if (evento === "escapa") {
    showBubble(t("jefeEscapa"));
    setTimeout(() => barra.classList.add("hidden"), 1000);
  }
});

const shadowBlob = new THREE.Mesh(
  new THREE.CircleGeometry(0.4, 16),
  new THREE.MeshBasicMaterial({ color: 0x000000, transparent: true, opacity: 0.32 })
);
shadowBlob.rotation.x = -Math.PI / 2;
shadowBlob.position.y = 0.015;
shadowBlob.visible = !shadowsEnabled; // con sombras reales activas, el blob 2D sobra
scene.add(shadowBlob);

// ---------- Camara dinamica (FOV punch en boost, temblor al chocar, inclinacion en giros) ----------
const BASE_FOV = 55;
const SHAKE_DURATION = 0.3;
let camBaseX = camera.position.x;
let shakeTimeLeft = 0, shakeMag = 0;
function triggerCameraShake(magnitude) {
  shakeTimeLeft = SHAKE_DURATION;
  shakeMag = magnitude;
}

// ---------- Lineas de velocidad (overlay CSS reactivo a la velocidad) ----------
const speedLinesEl = document.getElementById("speedLines");

// ---------- Polvo bajo los pies al correr rapido ----------
const dustGeo = new THREE.CircleGeometry(0.13, 8);
const dustMatBase = new THREE.MeshBasicMaterial({ color: 0xfff6e0, transparent: true, opacity: 0.5, depthWrite: false });
const dustPool = makePool(() => {
  const m = new THREE.Mesh(dustGeo, dustMatBase.clone());
  m.rotation.x = -Math.PI / 2;
  return m;
});
const activeDust = [];
let dustSpawnTimer = 0;
function spawnDust(x, z, y = 0) {
  const m = dustPool.acquire();
  m.visible = true;
  m.position.set(x + (Math.random() - 0.5) * 0.2, y + 0.03, z + 0.3 + Math.random() * 0.15);
  m.scale.setScalar(0.6 + Math.random() * 0.3);
  m.material.opacity = 0.5;
  if (!m.parent) scene.add(m);
  activeDust.push({ mesh: m, life: 0.4, maxLife: 0.4, vx: (Math.random() - 0.5) * 0.6 });
}
function updateDust(dt) {
  for (let i = activeDust.length - 1; i >= 0; i--) {
    const d = activeDust[i];
    d.life -= dt;
    if (d.life <= 0) { dustPool.release(d.mesh); activeDust.splice(i, 1); continue; }
    d.mesh.position.x += d.vx * dt;
    const k = d.life / d.maxLife;
    d.mesh.material.opacity = 0.5 * k;
    d.mesh.scale.setScalar((0.6 + (1 - k) * 0.5));
  }
}

function resize() {
  const w = window.innerWidth, h = window.innerHeight;
  renderer.setSize(w, h);
  camera.aspect = w / h;
  camera.updateProjectionMatrix();
}
let resizeTimer = null;
window.addEventListener("resize", () => {
  clearTimeout(resizeTimer);
  resizeTimer = setTimeout(resize, 150);
});
resize();

// ---------- Estado de juego ----------
let gameState = "menu"; // menu | playing | gameover
let currentLane = 1;
let playerX = 0;
let elapsed = 0, speed = BASE_SPEED, distance = 0, tacosThisRun = 0;
let isJumping = false, jumpElapsed = 0;   // isJumping = en el aire (salto o caida)
let py = 0, vy = 0, enSuelo = true, camY = 0;
let megaTimeLeft = 0, freezeTimeLeft = 0, rocketTimeLeft = 0;
let nextJefeAt = JEFE_PRIMERO, misionesReloj = 0;
// Frases (25/10): cargas de microfono, hasta 3.
let frasesCargas = 0, microVisto = false;
const MAX_FRASES = 3;
// Lo que suelta segun lo que tenga delante (la pieza del obstaculo).
const FRASES = {
  es: { furgoneta: "¡FAKE NEWS!", patrulla: "¡CAZA DE BRUJAS!", guardaespaldas: "¡ESTÁS DESPEDIDO!",
    barricada: "¡TOTAL DESASTRE!", conos: "¡TOTAL DESASTRE!", pancarta: "¡TRISTE!", globos: "¡TRISTE!",
    barril: "¡HECHO EN CHINA!", jefe: "¡CHINA! ¡CHINA!",
    nada: ["¡CRÉEME!", "¡ENORME!", "¡COVFEFE!", "¡NADIE LO HACE MEJOR!"] },
  en: { furgoneta: "FAKE NEWS!", patrulla: "WITCH HUNT!", guardaespaldas: "YOU'RE FIRED!",
    barricada: "TOTAL DISASTER!", conos: "TOTAL DISASTER!", pancarta: "SAD!", globos: "SAD!",
    barril: "MADE IN CHINA!", jefe: "CHINA! CHINA!",
    nada: ["BELIEVE ME!", "HUGE!", "COVFEFE!", "NOBODY DOES IT BETTER!"] },
};
let frasesPintadas = "";
function pintarFrases() {
  // Solo toca la pagina si algo ha cambiado (se llama en cada fotograma).
  const clave = gameState + frasesCargas + microVisto;
  if (clave === frasesPintadas) return;
  frasesPintadas = clave;
  const el = document.getElementById("hudFrases");
  el.innerHTML = Array.from({ length: MAX_FRASES }, (_, i) => `<span class="${i < frasesCargas ? "lleno" : "vacio"}">🎤</span>`).join("");
  el.classList.toggle("hidden", gameState !== "playing" || (frasesCargas === 0 && !microVisto));
}
function lanzarFrase() {
  if (frasesCargas <= 0) return;
  const f = FRASES[getLang()] || FRASES.es;
  const o = world.primerObstaculo(currentLane, 60);
  let texto, objetivo;
  if (o) { texto = f[o.pool] || f.nada[Math.floor(Math.random() * f.nada.length)]; objetivo = o; }
  else if (world.jefeActivo()) { texto = f.jefe; objetivo = "jefe"; }
  else { texto = f.nada[Math.floor(Math.random() * f.nada.length)]; objetivo = null; }
  frasesCargas--;
  world.lanzarFrase(currentLane, texto, objetivo);
  if (objetivo && objetivo !== "jefe") tacosThisRun += 3 * multiplier;
  flashExpression("determined", 0.6);
  triggerCameraShake(0.02);
  vibrate(25);
  sndPoint();
  pintarFrases();
}
let isSliding = false, slideElapsed = 0;
let idlePhase = 0;

let streak = 0, multiplier = 1, lastTacoTime = 0;
let shieldActive = false;
let magnetTimeLeft = 0;
let boostTimeLeft = 0;

function resetRun() {
  currentLane = 1;
  playerX = 0;
  elapsed = 0; speed = BASE_SPEED; distance = 0; tacosThisRun = 0;
  isJumping = false; jumpElapsed = 0;
  py = 0; vy = 0; enSuelo = true; camY = 0;
  megaTimeLeft = 0; character.setMega(1);
  freezeTimeLeft = 0; rocketTimeLeft = 0; nextJefeAt = JEFE_PRIMERO; misionesReloj = 0;
  frasesCargas = 1;   // empieza con una para que se pruebe enseguida
  if (monturaCohete) monturaCohete.visible = false;
  world.setCielo(false);
  document.getElementById("bossBar").classList.add("hidden");
  misiones.empezarPartida();
  isSliding = false; slideElapsed = 0;
  streak = 0; multiplier = 1; lastTacoTime = 0;
  shieldActive = false; magnetTimeLeft = 0; boostTimeLeft = 0;
  lastTacoShown = 0;
  shakeTimeLeft = 0;
  character.object3D.position.set(0, 0, 0);
  character.object3D.rotation.set(0, 0, 0);
  character.object3D.scale.set(1, 1, 1);
  character.setSlidePose(false);
  character.setShieldActive(false);
  character.setExpression("normal");
  appliedExpression = "normal";
  expressionFlashLeft = 0;
  const zoneChoice = getSettings().selectedZone || "auto";
  // En un nivel manda el nivel (su zona, su luz y su calle); en el sin fin, la zona elegida.
  world.setNivel(nivelActual);
  world.setLuz(nivelActual ? nivelActual.luz : null);
  aplicarLuz(nivelActual ? nivelActual.luz : null);
  // 25/10: cada mapa por separado. En «Auto» se sortea UNA zona al empezar y
  // no cambia en toda la partida (antes rotaba cada pocos cientos de metros y
  // el fondo cambiaba de golpe de un sitio a otro).
  const zonas = ["city", "desert", "town", "dc"];
  const zonaSinFin = zoneChoice === "auto" ? zonas[Math.floor(Math.random() * zonas.length)] : zoneChoice;
  world.setForcedZone(nivelActual ? nivelActual.zona : zonaSinFin);
  world.reset();
  character.object3D.visible = true;
  fin = null;
  if (nivelActual) mostrarBanner(nivelActual);
  setCameraMode("race");
  camBaseX = camera.position.x;
  camera.fov = BASE_FOV;
  camera.rotation.z = 0;
  camera.updateProjectionMatrix();
  updateHud();
  updatePowerupBadge();
}

// Expresion = una capa de fondo continua (segun como va la carrera) mas
// destellos puntuales que la pisan durante unos instantes. Antes solo habia
// destellos con setTimeout que reseteaban a "normal" a ciegas, asi que la
// cara no reflejaba nada del estado del juego: corriendo a tope o recien
// arrancando ponia exactamente la misma expresion.
let expressionFlashLeft = 0;
let appliedExpression = "normal";
function flashExpression(name, durationSec) {
  character.setExpression(name);
  appliedExpression = name;
  expressionFlashLeft = durationSec;
}

// Distancia a la que un obstaculo del carril actual empieza a preocupar.
const WORRY_DIST = 11;
function updateExpression(dt) {
  if (expressionFlashLeft > 0) {
    expressionFlashLeft -= dt;
    return; // un destello (golpe, taco) manda sobre la expresion de fondo
  }
  // Obstaculo cerca en mi carril y sin escudo -> apuro.
  let worry = false;
  for (const o of world.obstacles) {
    if (o.lane !== currentLane) continue;
    if (o.z < -WORRY_DIST || o.z > 0) continue;
    worry = true;
    break;
  }
  const speedFrac = (speed - BASE_SPEED) / (MAX_SPEED - BASE_SPEED);
  let base = "normal";
  if (worry && !shieldActive) base = "worried";
  // Umbral bajo (0.18) a proposito: con ACCEL=0.24 la velocidad sube despacio,
  // y con el 0.45 inicial hacian falta ~22 s de carrera para verlo -- mas de lo
  // que dura la mayoria de partidas, asi que la cara de concentracion no
  // aparecia practicamente nunca. Comprobado espiando la expresion en partida
  // real: con 0.45 solo salian "normal" y "worried".
  else if (speedFrac > 0.18 || boostTimeLeft > 0) base = "determined";
  if (base !== appliedExpression) {
    character.setExpression(base);
    appliedExpression = base;
  }
}

function pulse(el) {
  el.classList.remove("pulse");
  void el.offsetWidth; // fuerza reflow para poder reiniciar la animacion
  el.classList.add("pulse");
}

function popupScore(delta) {
  const host = document.getElementById("hudTacos");
  const span = document.createElement("div");
  span.className = "scorePopup";
  span.textContent = "+" + delta;
  host.appendChild(span);
  setTimeout(() => span.remove(), 700);
}

let lastTacoShown = 0;
function updateHud() {
  const tacoFloor = Math.floor(tacosThisRun);
  if (tacoFloor !== lastTacoShown) {
    const delta = tacoFloor - lastTacoShown;
    if (delta > 0) popupScore(delta);
    lastTacoShown = tacoFloor;
    pulse(document.getElementById("hudTacos"));
  }
  document.getElementById("hudTacoCount").textContent = tacoFloor;
  document.getElementById("hudScoreValue").textContent = Math.floor(distance);
  const streakEl = document.getElementById("hudStreak");
  if (multiplier > 1) { streakEl.textContent = "x" + multiplier; streakEl.classList.remove("hidden"); }
  else { streakEl.classList.add("hidden"); }
}

function updatePowerupBadge() {
  const badge = document.getElementById("powerupBadge");
  if (rocketTimeLeft > 0) { badge.textContent = "🚀 " + t("powerupRocket") + " " + rocketTimeLeft.toFixed(1) + "s"; badge.classList.remove("hidden"); }
  else if (megaTimeLeft > 0) { badge.textContent = "🧢 " + t("powerupMega") + " " + megaTimeLeft.toFixed(1) + "s"; badge.classList.remove("hidden"); }
  else if (freezeTimeLeft > 0) { badge.textContent = "🧊 " + t("powerupFreeze") + " " + freezeTimeLeft.toFixed(1) + "s"; badge.classList.remove("hidden"); }
  else if (shieldActive) { badge.textContent = "🛡 " + t("powerupShield"); badge.classList.remove("hidden"); }
  else if (magnetTimeLeft > 0) { badge.textContent = "🧲 " + t("powerupMagnet") + " " + magnetTimeLeft.toFixed(1) + "s"; badge.classList.remove("hidden"); }
  else if (boostTimeLeft > 0) { badge.textContent = "🚀 " + t("powerupBoost") + " " + boostTimeLeft.toFixed(1) + "s"; badge.classList.remove("hidden"); }
  else { badge.classList.add("hidden"); }
}

// ---------- Globo de frases ----------
let bubbleTimeout = null;
function showBubble(text) {
  const el = document.getElementById("speechBubble");
  el.textContent = text;
  el.classList.add("show");
  if (bubbleTimeout) clearTimeout(bubbleTimeout);
  bubbleTimeout = setTimeout(() => el.classList.remove("show"), 1300);
}

// ---------- Confeti ----------
const CONFETTI_COLORS = ["#d4af37", "#c81e1e", "#1f4fb0", "#ffffff"];
function spawnConfetti(count) {
  const layer = document.getElementById("confettiLayer");
  for (let i = 0; i < count; i++) {
    const piece = document.createElement("div");
    piece.className = "confetti-piece";
    piece.style.left = Math.random() * 100 + "%";
    piece.style.background = CONFETTI_COLORS[Math.floor(Math.random() * CONFETTI_COLORS.length)];
    const dur = 1.4 + Math.random() * 1.2;
    piece.style.animationDuration = dur + "s";
    piece.style.animationDelay = (Math.random() * 0.3) + "s";
    layer.appendChild(piece);
    setTimeout(() => piece.remove(), (dur + 0.4) * 1000);
  }
}

// ---------- Controles ----------
initControls(document.getElementById("touchControls"), (action) => {
  if (gameState !== "playing") return;
  if (action === "left" && currentLane > 0) { currentLane--; sndLaneSwitch(); }
  else if (action === "right" && currentLane < 2) { currentLane++; sndLaneSwitch(); }
  else if (action === "frase") lanzarFrase();
  else if (action === "jump" && enSuelo && !isSliding) {
    vy = V_SALTO; enSuelo = false; isJumping = true; jumpElapsed = 0; sndJump(); vibrate(15);
  }
  // Deslizarse otra vez mientras ya te deslizas REINICIA el cronometro en vez
  // de ignorarse: con dos vallas seguidas el jugador da al boton por segunda
  // vez y antes se levantaba igual en medio de la segunda valla.
  else if (action === "slide" && !isJumping) {
    if (isSliding) { slideElapsed = 0; }
    else { isSliding = true; slideElapsed = 0; sndSlide(); }
  }
});

// ---------- Colisiones ----------
const HIT_LANE_TOLERANCE = 0.85; // menos que medio ancho de carril (1.1): rozar el borde durante un cambio de carril no cuenta como choque
function checkCollisions() {
  if (rocketTimeLeft > 0) return;          // en el cohete se vuela por encima de todo
  for (const o of world.obstacles) {
    // Usa la posicion X real del personaje, no el carril logico (que cambia
    // instantaneo al pulsar) -- asi solo choca si de verdad esta centrado
    // en ese carril, no si solo lo esta rozando de lado al cambiar.
    if (o.smashed) continue;
    if (Math.abs(playerX - LANE_X[o.lane]) > HIT_LANE_TOLERANCE) continue;
    if (o.type === "bus") {
      // Autobus: solo choca si te lo encuentras de lado o de frente a ras de
      // suelo (por la rampa se sube sin mas). `o.z` es lo que llevas metido
      // desde el pie de la rampa; la rampa mide 2.2 y el autobus entero 10.2.
      if (o.z < 0.3 || o.z > 10.2) continue;
      const suelo = o.z < 2.2 ? 1.55 * o.z / 2.2 : 1.55;
      if (py > suelo - 0.45) {
        if (o.z > 2.2 && !o.contado) { o.contado = true; avisarMisiones(misiones.evento("autobus")); }
        continue;
      }
    } else {
      const zc = o.z + (o.centro || 0);
      const medio = o.medio || 0.7;
      if (zc < -medio || zc > medio) continue;
      if (o.type === "low" && py > 0.55) {
        if (!o.contado) { o.contado = true; avisarMisiones(misiones.evento("saltos")); }
        continue;
      }
      if (o.type === "high" && isSliding) {
        if (!o.contado) { o.contado = true; avisarMisiones(misiones.evento("deslizar")); }
        continue;
      }
      if (o.alto !== undefined && py > o.alto - 0.1) continue;   // le pasas por encima
    }
    if (o.congelado) {
      // Congelado por el rayo: se rompe al tocarlo.
      world.smash(o);
      sndHit();
      vibrate(15);
      tacosThisRun += 2 * multiplier;
      avisarMisiones(misiones.evento("hielo"));
      continue;
    }
    if (megaTimeLeft > 0) {
      // Gigante: lo que toca sale volando.
      world.smash(o);
      sndHit();
      vibrate(25);
      triggerCameraShake(0.04);
      tacosThisRun += 5 * multiplier;
      avisarMisiones(misiones.evento("gigante"));
      continue;
    }
    if (shieldActive) {
      shieldActive = false;
      character.setShieldActive(false);
      updatePowerupBadge();
      world.smash(o);
      sndHit();
      vibrate(20);
      flashExpression("surprised", 0.5);
      triggerCameraShake(0.035);
      continue;
    }
    flashExpression("surprised", 1);
    triggerCameraShake(0.055);
    triggerGameOver();
    return;
  }
}

function registerTaco(amount) {
  streak++;
  lastTacoTime = elapsed;
  const newMultiplier = Math.min(5, 1 + Math.floor(streak / 5));
  if (newMultiplier > multiplier) {
    multiplier = newMultiplier;
    showBubble(randomCatchphrase());
    sndPoint();
    flashExpression("happy", 0.6);
  }
  tacosThisRun += amount * multiplier;
}

const MAGNET_RANGE = 14; // alcance del iman hacia delante: solo absorbe lo cercano segun se va pasando, no toda la pista de golpe
function checkCollectibles(dt) {
  const magnetActive = magnetTimeLeft > 0;
  for (const tItem of world.tacos) {
    if (tItem.collected) continue;
    const inMagnetRange = magnetActive && tItem.z > -MAGNET_RANGE;
    if (inMagnetRange) {
      // Absorcion de verdad: la tortilla se acerca al personaje en X **y en
      // Z**. Antes solo se alineaba con el carril y seguia avanzando a la
      // velocidad normal de la pista, asi que parecia que el iman solo
      // "ordenaba" las tortillas en fila en vez de atraerlas.
      // La fuerza crece al acercarse (1 en el borde del rango, ~3 encima del
      // jugador), que es lo que da la sensacion de succion acelerada.
      const dist = Math.max(0.35, -tItem.z);
      const pull = Math.min(1, dt * (2.5 + 9 * (1 - dist / MAGNET_RANGE)));
      const targetX = LANE_X[currentLane];
      tItem.mesh.position.x = THREE.MathUtils.lerp(tItem.mesh.position.x, targetX, pull);
      // Acercarla en Z de forma explicita: se resta distancia ADEMAS del
      // avance normal del mundo, por eso vuela hacia el jugador.
      tItem.z = THREE.MathUtils.lerp(tItem.z, 0, pull);
      tItem.mesh.position.z = tItem.z;
      // (No se toca la Y: world.update() la reescribe cada frame con su
      // rebote propio, asi que cualquier arco que pusieramos aqui se
      // perderia al frame siguiente.)
      // Radio de recogida mas generoso con el iman: al llegar volando no
      // tiene por que caer justo en la ventana estrecha de +-0.8.
      if (Math.abs(tItem.z) < 1.3 && Math.abs(tItem.mesh.position.x - targetX) < 0.9) {
        tItem.collected = true;
        registerTaco(1);
        sndTaco();
      }
      continue;
    }
    if (tItem.lane !== currentLane) continue;
    // A la altura del personaje (volando en cohete no se cogen los del suelo,
    // ni desde el suelo los del cielo). Holgado: los arcos se cogen saltando.
    if (Math.abs(tItem.baseY - (py + 0.9)) > 1.7) continue;
    if (tItem.z < -0.8 || tItem.z > 0.8) continue;
    tItem.collected = true;
    registerTaco(1);
    sndTaco();
  }
  if (streak > 0 && elapsed - lastTacoTime > STREAK_RESET_GAP) {
    streak = 0; multiplier = 1;
  }
}

function checkPowerups() {
  for (const p of world.powerups) {
    if (p.collected || p.lane !== currentLane) continue;
    if (p.z < -0.8 || p.z > 0.8) continue;
    p.collected = true;
    sndPoint();
    if (p.kind === "shield") { shieldActive = true; character.setShieldActive(true); showBubble(t("powerupShield") + "!"); }
    else if (p.kind === "magnet") { magnetTimeLeft = MAGNET_DURATION; showBubble(t("powerupMagnet") + "!"); }
    else if (p.kind === "boost") { boostTimeLeft = BOOST_DURATION; showBubble(t("powerupBoost") + "!"); }
    else if (p.kind === "mega") {
      megaTimeLeft = MEGA_DURATION;
      character.setMega(MEGA_SCALE);
      showBubble(t("powerupMega") + "!");
      flashExpression("happy", 1);
      triggerCameraShake(0.05);
      vibrate([30, 30, 60]);
    } else if (p.kind === "freeze") {
      freezeTimeLeft = FREEZE_DURATION;
      showBubble(t("powerupFreeze") + "!");
      vibrate(30);
    } else if (p.kind === "rocket") {
      rocketTimeLeft = ROCKET_DURATION;
      if (monturaCohete) monturaCohete.visible = true;
      world.setCielo(true);
      isSliding = false; character.setSlidePose(false);
      showBubble(t("powerupRocket") + "!");
      flashExpression("happy", 1.5);
      triggerCameraShake(0.05);
      vibrate([30, 30, 60]);
      avisarMisiones(misiones.evento("cohete"));
    } else if (p.kind === "micro") {
      frasesCargas = Math.min(MAX_FRASES, frasesCargas + 1);
      if (!microVisto) { microVisto = true; showBubble(t("microfono")); }
      pintarFrases();
    } else if (p.kind === "chile") {
      // Chile picante: sale disparado hacia el Burrito-Bot.
      world.dispararJefe(playerX, py + 1.2);
      vibrate(15);
    }
    updatePowerupBadge();
  }
}

// ?prueba en la direccion: deja mirar y tocar el estado desde la consola
// (para comprobar mecanicas sin jugar a mano). `__juego.inmortal = true`
// hace que los choques no acaben la partida.
const PRUEBA = /prueba/.test(location.search);
if (PRUEBA) {
  window.__juego = {
    world, character, inmortal: false, choques: 0,
    estado: () => ({ fase: fin ? fin.fase : null, nivel: nivelActual ? nivelActual.id : null, gameState, py, vy, enSuelo, megaTimeLeft, freezeTimeLeft, rocketTimeLeft, currentLane, tacos: tacosThisRun, distancia: distance }),
    carril: (l) => { currentLane = l; },
    saltar: () => { if (enSuelo && !isSliding) { vy = V_SALTO; enSuelo = false; isJumping = true; jumpElapsed = 0; } },
    gigante: () => { megaTimeLeft = MEGA_DURATION; character.setMega(MEGA_SCALE); },
    rayo: () => { freezeTimeLeft = FREEZE_DURATION; },
    cohete: () => { rocketTimeLeft = ROCKET_DURATION; if (monturaCohete) monturaCohete.visible = true; world.setCielo(true); },
    jefe: () => { nextJefeAt = 0; },
    // Empieza el nivel de Washington (o el que se diga) sin pasar por el mapa.
    nivel: async (id = "washington") => { await empezarNivel(NIVELES.find((n) => n.id === id)); },
    final: () => { distance = nivelActual ? nivelActual.largo - 40 : distance; },
    // Adelanta la partida hasta la distancia `d` a saltos cortos (los reciclajes de la pista van de 129 en 129).
    saltarA: (d) => { while (distance < d) { const dz = Math.min(30, d - distance); distance += dz; world.update(dz, 1 / 60); } },
    misiones,
    paso: (n = 1, dt = 1 / 60) => { for (let i = 0; i < n; i++) frame(dt); },
  };
}

function triggerGameOver() {
  if (PRUEBA && window.__juego.inmortal) { window.__juego.choques++; return; }
  gameState = "gameover";
  speedLinesEl.style.opacity = "0";
  sndHit();
  vibrate([80, 40, 80]);
  addTacos(Math.floor(tacosThisRun));
  avisarMisiones([...misiones.evento("tacos", tacosThisRun), ...misiones.evento("distancia", distance)]);
  pintarMisiones("misionesFin");
  document.getElementById("bossBar").classList.add("hidden");
  const isRecord = reportRunScore(Math.floor(distance));
  document.getElementById("finalScore").textContent = Math.floor(distance);
  document.getElementById("finalTacos").textContent = Math.floor(tacosThisRun);
  const bestLine = document.getElementById("bestLine");
  bestLine.textContent = isRecord ? "🏆 " + getSave().bestScore + " m" : "";
  document.getElementById("hud").classList.add("hidden");
  document.getElementById("powerupBadge").classList.add("hidden");
  document.getElementById("gameOverScreen").classList.remove("hidden");
  spawnConfetti(isRecord ? 40 : 18);
}

// ---------- Loop ----------
const clock = new THREE.Clock();
let firstFrame = true;

function tick() {
  requestAnimationFrame(tick);
  frame();
}

// Un fotograma del juego. `dtFijo` solo lo usa el modo ?prueba para avanzar
// paso a paso aunque la ventana este oculta (ahi el navegador no da fotogramas).
function frame(dtFijo) {
  if (contextLost) return;
  pintarFrases();
  // ?prueba: `__juego.pausa = true` congela el juego (sigue dibujando) para mirar una escena.
  if (PRUEBA && window.__juego && window.__juego.pausa && dtFijo === undefined) { renderer.render(scene, camera); return; }
  const dt = dtFijo !== undefined ? dtFijo : Math.min(clock.getDelta(), 0.05);

  if (gameState === "playing") {
    elapsed += dt;
    speed = Math.min(MAX_SPEED, BASE_SPEED + elapsed * ACCEL);
    if (magnetTimeLeft > 0) { magnetTimeLeft = Math.max(0, magnetTimeLeft - dt); updatePowerupBadge(); }
    if (boostTimeLeft > 0) { boostTimeLeft = Math.max(0, boostTimeLeft - dt); updatePowerupBadge(); }
    const frameSpeed = speed * (boostTimeLeft > 0 ? BOOST_MULT : 1);
    distance += frameSpeed * dt;

    const targetX = LANE_X[currentLane];
    const prevX = playerX;
    playerX += (targetX - playerX) * Math.min(1, dt * 10);
    character.object3D.position.x = playerX;
    character.setLean((playerX - prevX) * 12);

    if (megaTimeLeft > 0) {
      megaTimeLeft = Math.max(0, megaTimeLeft - dt);
      if (megaTimeLeft === 0) character.setMega(1);
      updatePowerupBadge();
    }

    if (freezeTimeLeft > 0) {
      freezeTimeLeft = Math.max(0, freezeTimeLeft - dt);
      world.congelar(45);
      updatePowerupBadge();
    }

    // ---- Cohete: sube al cielo y vuela recogiendo tacos ----
    if (rocketTimeLeft > 0) {
      rocketTimeLeft = Math.max(0, rocketTimeLeft - dt);
      py += (CIELO_Y - py) * Math.min(1, dt * 2.5);
      vy = 0; enSuelo = false; isJumping = true; jumpElapsed = JUMP_DURATION * 0.5;
      // Las ultimas filas antes de aterrizar salen vacias: se aterriza limpio.
      if (rocketTimeLeft < 1.6) world.setCielo(false);
      if (monturaCohete) monturaCohete.rotation.z = Math.sin(elapsed * 9) * 0.05;
      if (rocketTimeLeft === 0 && monturaCohete) monturaCohete.visible = false;
      updatePowerupBadge();
    }

    // ---- El Burrito-Bot llega cada tantos metros ----
    world.setJugador(currentLane);
    if (nivelActual && distance >= nivelActual.largo - 1) { iniciarFinal(); return; }
    if (!nivelActual && distance >= nextJefeAt && rocketTimeLeft === 0 && !world.jefeActivo() && world.iniciarJefe()) {
      nextJefeAt = distance + JEFE_CADA;
      document.getElementById("bossFill").style.width = "100%";
      document.getElementById("bossBar").classList.remove("hidden");
      showBubble(t("jefeLlega"));
      triggerCameraShake(0.04);
    }

    // Misiones "de una partida": se miran una vez por segundo (no a cada
    // fotograma, que cada aviso guarda la partida).
    misionesReloj -= dt;
    if (misionesReloj <= 0) {
      misionesReloj = 1;
      avisarMisiones([...misiones.evento("tacos", tacosThisRun), ...misiones.evento("distancia", distance)]);
    }

    // ---- Altura: suelo, rampa y techo del autobus ----
    const suelo = world.surfaceAt(playerX);
    if (enSuelo) {
      if (suelo < py - 0.05) { enSuelo = false; vy = 0; isJumping = true; jumpElapsed = JUMP_DURATION / 2; } // se acabo el techo: a caer
      else py = suelo;                                                    // por la rampa se sube andando
    }
    if (!enSuelo && rocketTimeLeft === 0) {
      vy -= GRAVEDAD * dt;
      py += vy * dt;
      if (py <= suelo && vy <= 0) {
        py = suelo; vy = 0; enSuelo = true; isJumping = false;
        character.setJumpPose(1);
        // Aterrizaje con peso: nube de polvo a los pies + vibracion corta.
        for (let d = 0; d < 5; d++) spawnDust(character.object3D.position.x, character.object3D.position.z, py);
        vibrate(10);
      }
    }
    character.object3D.position.y = py;
    shadowBlob.position.y = suelo + 0.015;
    shadowBlob.scale.setScalar(Math.max(0.4, 1 - (py - suelo) / JUMP_HEIGHT));

    if (isJumping) {
      jumpElapsed += dt;
      // Pose de salto mientras se esta en el aire; en una caida larga se
      // queda en la mitad recogida hasta tocar suelo.
      character.setJumpPose(Math.min(0.95, jumpElapsed / JUMP_DURATION));
    } else if (isSliding) {
      slideElapsed += dt;
      character.setSlidePose(true);
      if (slideElapsed >= SLIDE_DURATION) { isSliding = false; character.setSlidePose(false); }
    } else {
      character.updateRun(dt, speed / BASE_SPEED);
    }

    const curveX = world.update(frameSpeed * dt, dtFijo !== undefined ? dt : undefined);
    // La pista curva: personaje/sombra se mueven con el mismo offset que el
    // grupo del mundo, asi que el carril relativo y las colisiones no cambian.
    character.object3D.position.x = playerX + curveX;
    // La pista ya ha avanzado este fotograma: si va por la rampa, se recoloca
    // a la altura nueva antes de mirar choques (si no, va un pelin por debajo
    // de la rampa y cuenta como chocar con el autobus).
    if (enSuelo) {
      py = Math.max(py, world.surfaceAt(playerX));
      character.object3D.position.y = py;
    }
    checkCollisions();
    checkCollectibles(dt);
    checkPowerups();
    updateExpression(dt);
    updateHud();

    shadowBlob.position.x = playerX + curveX;
    shadowBlob.position.z = character.object3D.position.z;

    // ---- Camara dinamica: sigue en X, FOV punch en boost, temblor, inclinacion en giros ----
    // (magnitudes deliberadamente sutiles: la primera pasada se sintio muy exagerada)
    // 23/10, contra el mareo: la camara solo acompaña la mitad del cambio de
    // carril (antes se deslizaba entera con cada cambio) y ya no se inclina.
    camBaseX += ((playerX + curveX) * 0.5 - camBaseX) * Math.min(1, dt * 3);
    const targetFov = boostTimeLeft > 0 ? BASE_FOV + 1.2 : BASE_FOV;
    camera.fov += (targetFov - camera.fov) * Math.min(1, dt * 2.5);
    camera.rotation.z = 0;
    let shakeX = 0, shakeY = 0;
    if (shakeTimeLeft > 0) {
      shakeTimeLeft = Math.max(0, shakeTimeLeft - dt);
      const k = shakeTimeLeft / SHAKE_DURATION;
      shakeX = (Math.random() - 0.5) * shakeMag * k;
      shakeY = (Math.random() - 0.5) * shakeMag * k * 0.6;
    }
    camera.position.x = camBaseX + shakeX;
    // La camara sube con el jugador cuando va por el techo del autobus, y un
    // poco mas en modo gigante para que se vea la pista por encima de el.
    // Sigue al suelo que pisa (techo del autobus) o al cohete, no a cada salto:
    // subir y bajar la camara en cada salto era otro vaiven que mareaba.
    const alturaCam = rocketTimeLeft > 0 ? py : world.surfaceAt(playerX);
    camY += ((alturaCam * 0.75 + (megaTimeLeft > 0 ? 1.2 : 0)) - camY) * Math.min(1, dt * 2.5);
    camera.position.y = RACE_CAM.pos.y + camY + shakeY;
    camera.updateProjectionMatrix();

    // ---- Lineas de velocidad ----
    const speedFrac = Math.max(0, Math.min(1, (speed - BASE_SPEED * 1.15) / (MAX_SPEED - BASE_SPEED * 1.15)));
    speedLinesEl.style.opacity = String(Math.min(0.35, speedFrac * 0.25 + (boostTimeLeft > 0 ? 0.2 : 0)));

    // ---- Polvo bajo los pies (solo corriendo en el suelo, mas seguido cuanto mas rapido) ----
    if (!isJumping && !isSliding) {
      dustSpawnTimer -= dt;
      if (dustSpawnTimer <= 0) {
        if (speedFrac > 0.1) spawnDust(playerX + curveX, character.object3D.position.z, py);
        dustSpawnTimer = 0.12 - speedFrac * 0.06;
      }
    }
    updateDust(dt);
  } else if (gameState === "final") {
    frameFinal(dt);
  } else if (gameState === "menu") {
    idlePhase += dt;
    character.object3D.rotation.y = Math.sin(idlePhase * 0.5) * 0.5;
    character.setIdlePose(idlePhase);
    shadowBlob.position.set(0, 0.015, 0);
    shadowBlob.scale.setScalar(1);
    updateDust(dt);
  }

  renderer.render(scene, camera);
  if (firstFrame) {
    firstFrame = false;
    const loadingScreen = document.getElementById("loadingScreen");
    loadingScreen.classList.add("fadeOut");
    setTimeout(() => loadingScreen.remove(), 350);
  }
}

// ---------- UI wiring ----------
// JUGAR abre el mapa de la gira; «Sin fin» es el modo de siempre.
document.getElementById("startBtn").addEventListener("click", () => { unlockAudio(); abrirMapa(); });
// «Sin fin» abre primero la eleccion de zona (25/10: antes estaba en el inicio).
// Candado (25/10): el Sin fin se abre al superar el nivel 1. Cerrado, avisa de que hace falta.
function avisoMenu(texto) {
  const el = document.getElementById("avisoMenu");
  el.textContent = texto;
  el.classList.remove("hidden");
  el.style.animation = "none"; void el.offsetWidth; el.style.animation = "";
  clearTimeout(avisoMenu.t);
  avisoMenu.t = setTimeout(() => el.classList.add("hidden"), 2600);
}
function pintarSinFin() {
  const abierto = sinFinAbierto(getNiveles());
  const b = document.getElementById("sinFinBtn");
  b.textContent = abierto ? t("sinFin") : "🔒 " + t("sinFin").replace("♾️ ", "");
  b.classList.toggle("cerrado", !abierto);
}
document.getElementById("sinFinBtn").addEventListener("click", () => {
  unlockAudio();
  if (!sinFinAbierto(getNiveles()) && !PRUEBA) { avisoMenu(t("sinFinCerrado")); return; }
  document.getElementById("sinFinOverlay").classList.remove("hidden");
});
pintarSinFin();
document.getElementById("sinFinCerrar").addEventListener("click", () => {
  document.getElementById("sinFinOverlay").classList.add("hidden");
});
document.getElementById("sinFinCorrer").addEventListener("click", () => {
  startMusic();
  nivelActual = null;
  resetRun();
  gameState = "playing";
  document.getElementById("sinFinOverlay").classList.add("hidden");
  document.getElementById("startScreen").classList.add("hidden");
  document.getElementById("hud").classList.remove("hidden");
});
// Idioma en ajustes: marcar el elegido como los demas selectores.
function marcarIdioma() {
  const en = getLang() === "en";
  document.getElementById("settingsLangEs").classList.toggle("equippedBtn", !en);
  document.getElementById("settingsLangEn").classList.toggle("equippedBtn", en);
}
function volverAlMenu() {
  gameState = "menu";
  idlePhase = 0;
  character.object3D.visible = true;
  character.object3D.position.set(0, 0, 0);
  character.object3D.rotation.set(0, 0, 0);
  setCameraMode("menu");
  for (const id of ["gameOverScreen", "nivelFin", "mapaGira", "hud", "bossBar", "bannerNivel"]) document.getElementById(id).classList.add("hidden");
  document.getElementById("startScreen").classList.remove("hidden");
  pintarMisiones("misionesMenu");
  pintarSinFin();
}
document.getElementById("mapaCerrar").addEventListener("click", volverAlMenu);
document.getElementById("nivelFinMapa").addEventListener("click", () => { volverAlMenu(); abrirMapa(); });
document.getElementById("nivelFinRepetir").addEventListener("click", () => {
  document.getElementById("nivelFin").classList.add("hidden");
  resetRun();
  gameState = "playing";
  document.getElementById("hud").classList.remove("hidden");
});

document.getElementById("retryBtn").addEventListener("click", () => {
  resetRun();
  gameState = "playing";
  document.getElementById("gameOverScreen").classList.add("hidden");
  document.getElementById("hud").classList.remove("hidden");
});

document.getElementById("menuBtn").addEventListener("click", volverAlMenu);

document.getElementById("langToggle").addEventListener("click", () => { toggleLang(); updatePowerupBadge(); });
document.getElementById("startLangBtn").addEventListener("click", () => { toggleLang(); marcarIdioma(); pintarMisiones("misionesMenu"); pintarSinFin(); });

// Fase 2/4 todavia no implementadas: ocultar accesos por ahora.
document.getElementById("startShopBtn").style.display = "none";
document.getElementById("startRankBtn").style.display = "none";

// ---------- Ajustes ----------
const settings = getSettings();
setSwipeThreshold(settings.swipeSensitivity);
setSfxVolume(settings.sfxVol);
setSfxMuted(settings.sfxMuted);
setMusicVolume(settings.musicVol);
setMusicMuted(settings.musicMuted);

const musicVolRange = document.getElementById("musicVolRange");
const sfxVolRange = document.getElementById("sfxVolRange");
const sensitivityRange = document.getElementById("sensitivityRange");
const musicMuteBtn = document.getElementById("musicMuteBtn");
const sfxMuteBtn = document.getElementById("sfxMuteBtn");

musicVolRange.value = Math.round(settings.musicVol * 100);
sfxVolRange.value = Math.round(settings.sfxVol * 100);
sensitivityRange.value = settings.swipeSensitivity;
musicMuteBtn.textContent = settings.musicMuted ? "🔇" : "🔊";
sfxMuteBtn.textContent = settings.sfxMuted ? "🔇" : "🔊";

document.getElementById("startSettingsBtn").addEventListener("click", () => {
  document.getElementById("settingsOverlay").classList.remove("hidden");
});
document.getElementById("settingsClose").addEventListener("click", () => {
  document.getElementById("settingsOverlay").classList.add("hidden");
});

musicVolRange.addEventListener("input", () => {
  const v = musicVolRange.value / 100;
  setMusicVolume(v);
  updateSettings({ musicVol: v });
});
sfxVolRange.addEventListener("input", () => {
  const v = sfxVolRange.value / 100;
  setSfxVolume(v);
  updateSettings({ sfxVol: v });
});
sensitivityRange.addEventListener("input", () => {
  const px = Number(sensitivityRange.value);
  setSwipeThreshold(px);
  updateSettings({ swipeSensitivity: px });
});
musicMuteBtn.addEventListener("click", () => {
  const s = getSettings();
  const muted = !s.musicMuted;
  setMusicMuted(muted);
  updateSettings({ musicMuted: muted });
  musicMuteBtn.textContent = muted ? "🔇" : "🔊";
});
sfxMuteBtn.addEventListener("click", () => {
  const s = getSettings();
  const muted = !s.sfxMuted;
  setSfxMuted(muted);
  updateSettings({ sfxMuted: muted });
  sfxMuteBtn.textContent = muted ? "🔇" : "🔊";
});
document.getElementById("settingsLangEs").addEventListener("click", () => { setLang("es"); marcarIdioma(); pintarMisiones("misionesMenu"); pintarSinFin(); });
document.getElementById("settingsLangEn").addEventListener("click", () => { setLang("en"); marcarIdioma(); pintarMisiones("misionesMenu"); pintarSinFin(); });
marcarIdioma();

const qualityBtns = {
  low: document.getElementById("qualityLow"),
  medium: document.getElementById("qualityMedium"),
  high: document.getElementById("qualityHigh"),
};
function highlightQuality(level) {
  for (const key in qualityBtns) qualityBtns[key].classList.toggle("equippedBtn", key === level);
}
highlightQuality(settings.graphicsQuality);
for (const level in qualityBtns) {
  qualityBtns[level].addEventListener("click", () => {
    if (getSettings().graphicsQuality === level) return;
    updateSettings({ graphicsQuality: level });
    window.location.reload();
  });
}
document.getElementById("resetProgressBtn").addEventListener("click", () => {
  if (window.confirm(t("resetConfirm"))) {
    resetProgress();
  }
});

// ---------- Selector de zona (pantalla de inicio) ----------
const zoneBtns = Array.from(document.querySelectorAll(".zoneBtn"));
function highlightZone(zone) {
  for (const btn of zoneBtns) btn.classList.toggle("equippedBtn", btn.dataset.zone === zone);
}
highlightZone(settings.selectedZone || "auto");
for (const btn of zoneBtns) {
  btn.addEventListener("click", () => {
    const zone = btn.dataset.zone;
    updateSettings({ selectedZone: zone });
    highlightZone(zone);
  });
}

applyI18n();
requestAnimationFrame(tick);
