import * as THREE from "../vendor/three.module.min.js";
import { createCharacter } from "./character.js";
import { createWorld, LANE_X, CIELO_Y } from "./world.js";
import { initControls, setSwipeThreshold } from "./controls.js";
import {
  sndTaco, sndJump, sndSlide, sndLaneSwitch, sndHit, sndPoint, unlockAudio, vibrate, startMusic, stopMusic,
  sndFanfarria, sndChapa, pausarMusica, hablar, sndCaida, sirena,
  setSfxVolume, setSfxMuted, setMusicVolume, setMusicMuted,
} from "./audio.js";
import { getSave, addTacos, spendTacos, reportRunScore, getSettings, updateSettings, resetProgress, getNiveles, guardarNivel, estrellasDe } from "./save.js";
import { NIVELES, piezasDeNivel, nivelAbierto, sinFinAbierto, usaKit, hitosDeNivel, salidaControl } from "./levels.js";
import { icono, pintarIconos } from "./iconos.js";
import { lienzo as lienzoPegatina, urlPegatina } from "./pegatinas.js";
import { abrirTienda, aplicarTienda } from "./tienda.js";
import { PIEZAS_KIT } from "./edificios.js";
import { applyI18n, toggleLang, setLang, t, randomCatchphrase, getLang } from "./i18n.js";
import { initErrorReporting, reportError } from "./errors.js";
import { makePool } from "./pool.js";
import { loadZoneModels, modelo, cargarCarpeta, cargarPersonaje } from "./models.js";
import * as misiones from "./missions.js";
import { FRASES } from "./frases.js";

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
// 27/10: en los niveles la velocidad va con lo recorrido, no con el tiempo:
// de 13 al empezar a `velMax` del nivel (20-23) al llegar, y un poco mas en
// el sprint final. Un nivel dura asi unos 3 minutos (antes 2 y medio).
const SPRINT_EXTRA = 1.08;
// Seguir tras chocar: cuesta tacos, cada vez el doble.
const PRECIO_SEGUIR = 300;
const INVULNERABLE = 2.2;    // segundos de parpadeo al seguir: lo de delante no cuenta

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
// 27/10: la camara del menu, al otro lado: el presidente se da la vuelta hacia
// ella y detras se ve la calle con sus edificios (antes, una carretera gris vacia).
const MENU_CAM = { pos: new THREE.Vector3(2.3, 1.9, 6.2), look: new THREE.Vector3(0, 0.05, 0) };
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
// La pegatina del taco, para la interfaz (en vez del emoji).
const TACO_IMG = () => `<img class="peg" src="${urlPegatina("taco")}" alt="">`;
function pintarPegatinas() {
  document.querySelectorAll("img[data-peg]").forEach((im) => { im.src = urlPegatina(im.dataset.peg); });
  const hudIcono = document.getElementById("hudTacoIcono");
  if (hudIcono) hudIcono.src = urlPegatina("taco");
  const logo = document.querySelector(".logoTacoIcono");
  if (logo) logo.innerHTML = `<img class="pegLogo" src="${urlPegatina("taco")}" alt="">`;
}

// Misiones posibles con lo que hay abierto (27/10): antes de pasar Nueva York
// solo las basicas; despues ya se puede todo (en Findlay o en el Sin fin hay
// autobuses, jefe y gorra gigante, y el cohete y el hielo en el Sin fin).
function misionPosible(tipo) {
  if (["tacos", "distancia", "saltos", "deslizar"].includes(tipo)) return true;
  return sinFinAbierto(getNiveles());
}
misiones.fijarDisponibles(misionPosible);

function pintarMisiones(id) {
  const el = document.getElementById(id);
  if (!el) return;
  el.innerHTML = `<div class="zoneLabel">${t("misiones")}</div>` + misiones.activas().map((m) => {
    const meta = Math.round(misiones.metaDe(m));
    const hecho = Math.min(meta, Math.floor(m.hecho));
    return `<div class="mision"><div class="misionFila"><span>${t("mis_" + m.tipo).replace("{n}", meta)}</span>`
      + `<span class="misionPremio">+${misiones.premioDe(m)} ${TACO_IMG()}</span></div>`
      + `<div class="misionBarra"><div style="width:${(100 * hecho / meta).toFixed(0)}%"></div></div></div>`;
  }).join("");
}
const colaAvisos = [];
let avisoVisible = false;
function avisarMisiones(cumplidas) {
  for (const c of cumplidas) colaAvisos.push(`${t("misionCumplida")} +${c.premio} ${TACO_IMG()}`);
  if (!avisoVisible) siguienteAviso();
}
// Otros avisos en la misma cola (chapas, punto de control...).
function avisoVerde(html) {
  colaAvisos.push(html);
  if (!avisoVisible) siguienteAviso();
}
function siguienteAviso() {
  const el = document.getElementById("misionToast");
  const texto = colaAvisos.shift();
  if (!texto) { avisoVisible = false; el.classList.add("hidden"); return; }
  avisoVisible = true;
  el.innerHTML = texto;
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
  } else if (luz === "mediodia") {
    // Mediodia (Findlay): sol alto y blanco, sombras cortas, cielo azul fuerte.
    sun.color.set(0xfffaf0); sun.intensity = 1.3; sun.position.set(2.5, 12, -2);
    hemi.color.set(0xe8f3ff); hemi.groundColor.set(0x8c8270);
  } else if (luz === "tarde") {
    // Tarde dorada (Phoenix): sol bajo, naranja, desde el oeste (a la izquierda).
    sun.color.set(0xffc98a); sun.intensity = 1.3; sun.position.set(-8, 6, -1);
    hemi.color.set(0xffe4c4); hemi.groundColor.set(0x8a6a4e);
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
// 27/10: las etiquetas van cada una en su sitio (antes «Findlay, Ohio» tapaba
// a «Nueva York») y el ultimo viaje, de Las Vegas a Washington, va en avion
// con un arco por encima (antes una linea cruzaba el pais de lado a lado).
function abrirMapa() {
  const svg = document.getElementById("mapaSvg");
  const hechos = getNiveles();
  const porTierra = NIVELES.slice(0, -1).map((n) => n.mapa.join(",")).join(" ");
  const [vx, vy] = NIVELES[NIVELES.length - 2].mapa, [wx, wy] = NIVELES[NIVELES.length - 1].mapa;
  const arco = `M${vx},${vy} Q${(vx + wx) / 2},${Math.min(vy, wy) - 26} ${wx},${wy}`;
  svg.innerHTML = `<polygon class="tierra" points="${SILUETA_EEUU}"/><polyline class="ruta" points="${porTierra}"/>`
    + `<path class="rutaAvion" d="${arco}"/>`
    + `<g transform="translate(${(vx + wx) / 2 - 3},${Math.min(vy, wy) - 17}) scale(0.26)">${icono("avion").replace(/<\/?svg[^>]*>/g, "")}</g>`
    + NIVELES.map((n) => {
      const [x, y] = n.mapa;
      const [ex, ey] = n.etiqueta || [0, 6.2];
      const abierto = nivelAbierto(n, hechos);
      const color = hechos[n.id] ? "#2fa84f" : abierto ? "#e8463c" : "#a7b0c0";
      return `<g class="parada" data-id="${n.id}"><circle cx="${x}" cy="${y}" r="3.2" fill="${color}"/>`
        + `<text x="${x}" y="${y + 1.1}">${abierto || hechos[n.id] ? n.numero : "?"}</text>`
        + `<text class="etiqueta" x="${x + ex}" y="${y + ey}">${n.lugar}</text></g>`;
    }).join("");
  // Donde vas: un anillo que late en el nivel abierto mas avanzado.
  const actual = [...NIVELES].reverse().find((n) => nivelAbierto(n, hechos)) || NIVELES[0];
  svg.querySelector(".ruta").insertAdjacentHTML("afterend", `<circle class="actual" cx="${actual.mapa[0]}" cy="${actual.mapa[1]}" r="4.8"/>`);
  svg.querySelectorAll(".parada").forEach((g) => g.addEventListener("click", () => elegirNivel(g.dataset.id)));
  pintarReceta(hechos);
  elegirNivel(nivelElegido || actual.id);
  document.getElementById("startScreen").classList.add("hidden");
  document.getElementById("mapaGira").classList.remove("hidden");
}
// La receta (27/10/2026): los ingredientes que robo el Burrito-Bot, uno por
// nivel. Los recuperados salen en color; los que faltan, en gris.
const RECETA = [["nueva_york", "tortilla"], ["pueblo", "maiz"], ["phoenix", "chile"], ["vegas", "salsa"], ["washington", "taco_perfecto"]];
function pintarReceta(hechos) {
  const fila = RECETA.map(([id, peg], i) => {
    const signo = i === RECETA.length - 1 ? '<span class="recetaIgual">=</span>' : i ? '<span class="recetaMas">+</span>' : "";
    return signo + `<img class="recetaPeg ${hechos[id] ? "tengo" : "falta"}" src="${urlPegatina(peg)}" alt="">`;
  }).join("");
  document.getElementById("receta").innerHTML = `<div class="recetaTitulo">${t("receta")}</div><div class="recetaFila">${fila}</div>`;
}
// Las tres estrellas de un nivel, cada una con su objetivo.
function filaObjetivos(n, r) {
  const chapas = r && r.chapas ? r.chapas.filter(Boolean).length : 0;
  const obj = [
    [r && (r.meta || r.superado), t("objMeta")],
    [r && r.sinChocar, t("objSinChocar")],
    [chapas === 3, `${t("objChapas")} (${chapas}/3)`],
  ];
  return obj.map(([ok, txt]) => `<li>${icono(ok ? "estrella" : "estrellaVacia")}<span>${txt}</span></li>`).join("");
}
function elegirNivel(id) {
  const n = NIVELES.find((x) => x.id === id);
  nivelElegido = id;
  const r = getNiveles()[id];
  const abierto = nivelAbierto(n, getNiveles());
  const i = NIVELES.indexOf(n);
  const cierre = !n.listo ? t("proximamente")
    : t("superaAntes").replace("{n}", NIVELES[i - 1] ? NIVELES[i - 1].nombre : "");
  const ingrediente = INGREDIENTE[n.id];
  const atajo = n.id === "washington" && !NIVELES.slice(0, i).every((x) => x.listo) ? `<div class="miAtajo">${t("atajoDc")}</div>` : "";
  document.getElementById("mapaInfo").innerHTML =
    `<div class="miNombre">${ingrediente ? `<img class="peg" src="${urlPegatina(ingrediente)}" alt="">` : ""} ${t("nivel")} ${n.numero} · ${n.nombre}</div><div class="miLugar">${n.lugar}</div>`
    + (n.historia ? `<div class="miHistoria">${n.historia[getLang()] || n.historia.es}</div>` : "")
    + atajo
    + (abierto ? `<ul class="objetivos">${filaObjetivos(n, r)}</ul><button id="mapaJugar" class="bigBtn">${t("jugarNivel")}</button>`
      : `<div class="proximamente">${icono("candado")} ${cierre}</div>`);
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
  startMusic(n.id);
  intento = nuevoIntento();
  resetRun();
  arrancar();
}
// Lo que dura todo un intento de un nivel (aunque se siga desde el punto de
// control): si se ha chocado alguna vez, las chapas y cuantas veces se ha
// pagado por seguir.
let intento = null;
function nuevoIntento() {
  return { chocado: false, chapas: [false, false, false], control: null, pagos: 0 };
}
function arrancar() {
  gameState = "playing";
  pausado = false;
  for (const id of ["mapaGira", "startScreen", "choqueNivel", "gameOverScreen", "nivelFin", "pausaOverlay"]) document.getElementById(id).classList.add("hidden");
  document.getElementById("hud").classList.remove("hidden");
  prepararBarra();
}

// ---- Barra de progreso del nivel (27/10/2026) ----
// Isidro: «los niveles no se cuando acaban». Arriba, la calle entera: los
// edificios famosos, el punto de control, la meta y por donde vas.
const barras = [...document.querySelectorAll(".pgPista")];
function prepararBarra() {
  const n = nivelActual;
  document.getElementById("hudProgreso").classList.toggle("hidden", !n);
  document.getElementById("hudScore").classList.toggle("hidden", !!n);
  document.getElementById("hudChapas").classList.toggle("hidden", !n || !n.chapas);
  if (!n) return;
  const marcas = hitosDeNivel(n).map((h) => `<i class="pgHito" style="left:${(100 * h.d / n.largo).toFixed(1)}%"></i>`).join("")
    + (n.control ? `<i class="pgControl" style="left:${(100 * n.control / n.largo).toFixed(1)}%">${icono("control")}</i>` : "")
    + `<i class="pgMeta">${icono("meta")}</i>`;
  for (const b of barras) {
    b.querySelector(".pgMarcas").innerHTML = marcas;
    b.querySelector(".pgYo").innerHTML = `<img src="${urlPegatina("taco")}" alt="">`;
  }
  pintarChapas();
}
function pintarBarra(el, d) {
  const n = nivelActual;
  const k = Math.max(0, Math.min(1, d / n.largo));
  el.querySelector(".pgLleno").style.transform = `scaleX(${k})`;
  el.querySelector(".pgYo").style.left = `${(k * 100).toFixed(2)}%`;
}
function pintarChapas() {
  const el = document.getElementById("hudChapas");
  if (!nivelActual || !nivelActual.chapas) return;
  const antes = (getNiveles()[nivelActual.id] || {}).chapas || [];
  el.innerHTML = [0, 1, 2].map((i) => {
    const clase = intento && intento.chapas[i] ? "cogida" : antes[i] ? "antes" : "falta";
    return `<span class="chapaHud ${clase}"><img src="${urlPegatina("chapa")}" alt=""></span>`;
  }).join("");
}
// ---- Llegada a la Casa Blanca: unos 10 segundos ----
// 0 frena y anda hasta la escalinata · 1 sube al portico y llega a la puerta
// · 2 se da la vuelta y saluda · 3 se gira y entra · 4 se cierran las puertas.
function iniciarFinal() {
  gameState = "final";
  apagarSirenas();
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
  animarPremio(dt);
  const cb = world.getCasaBlanca();
  if (!cb) { completarNivel(); return; }
  if (nivelActual.final === "camion") { finalCamion(dt, cb); return; }
  if (nivelActual.final === "mitin") { finalMitin(dt, cb); return; }
  if (nivelActual.final === "parada") { finalCamion(dt, cb, cb.position.z + (nivelActual.parada || 3)); return; }
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
    if (zPuerta + dz >= -1.4) { fin.fase = 2; fin.t = 0; showBubble(t("finCasaBlanca")); vibrate([30, 40, 30]); mostrarPremio("taco_perfecto"); spawnConfetti(30); }
  } else if (fin.fase === 2) {
    character.object3D.rotation.y += (Math.PI - character.object3D.rotation.y) * Math.min(1, dt * 5);
    character.setIdlePose(fin.t + 1);
    if (fin.t > 2.6) { fin.fase = 3; fin.t = 0; }
  } else if (fin.fase === 3) {
    character.object3D.rotation.y += (0 - character.object3D.rotation.y) * Math.min(1, dt * 6);
    if (fin.t > 0.45) { dz = 2.2 * dt; character.updateRun(dt, 0.4); if (mazorca) mazorca.visible = false; }
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
// (27/10: tambien el del diner de Phoenix, con `zParada` propia.)
function finalCamion(dt, flat, zParadaDada) {
  const zParada = zParadaDada !== undefined ? zParadaDada : flat.position.z + 21.6 + 1.6;   // delante del morro del camion
  playerX += (0 - playerX) * Math.min(1, dt * 4);
  let dz = 0;
  if (fin.fase === 0) {
    fin.v = Math.max(5, Math.min(fin.v - dt * 6, -zParada * 1.5 + 4));
    dz = fin.v * dt;
    character.updateRun(dt, Math.max(0.45, fin.v / BASE_SPEED));
    if (zParada + dz >= 0) { dz = Math.max(0, -zParada); fin.fase = 2; fin.t = 0; showBubble(nivelActual.fin[getLang()] || nivelActual.fin.es); vibrate([30, 40, 30]); mostrarPremio(INGREDIENTE[nivelActual.id] || "tortilla"); spawnConfetti(30); }
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
  // En el diner, mas lejos y mas alto: que se vea el chile gigante del tejado.
  const lejos = zParadaDada !== undefined;
  const objetivo = cerca ? (lejos ? new THREE.Vector3(2.6, 4.6, 16) : new THREE.Vector3(2.0, 3.2, 9.5)) : new THREE.Vector3(0, 4.6, 11);
  const mira = cerca ? (lejos ? new THREE.Vector3(0, 4.4, -6) : new THREE.Vector3(0, 2.2, -3)) : new THREE.Vector3(0, 2.4, -8);
  camera.position.lerp(objetivo, Math.min(1, dt * 1.6));
  fin.look.lerp(mira, Math.min(1, dt * 1.6));
  camera.lookAt(fin.look);
}

// Mitin en el juzgado (Findlay): frena, sube los escalones del escenario, se
// planta en medio, se da la vuelta y saluda; el maiz aparece por encima.
// 27/10: el ingrediente recuperado es una pegatina como el taco (antes el
// emoji, que en cada movil sale distinto), y sale en los tres finales.
let mazorca = null;
const texPremio = {};
const INGREDIENTE = { nueva_york: "tortilla", pueblo: "maiz", phoenix: "chile", vegas: "salsa", washington: "taco_perfecto" };
function mostrarPremio(nombre) {
  if (!texPremio[nombre]) {
    texPremio[nombre] = new THREE.CanvasTexture(lienzoPegatina(nombre));
    texPremio[nombre].colorSpace = THREE.SRGBColorSpace;
  }
  if (!mazorca) {
    mazorca = new THREE.Sprite(new THREE.SpriteMaterial({ transparent: true, depthTest: false }));
    mazorca.renderOrder = 10;
    scene.add(mazorca);
  }
  mazorca.material.map = texPremio[nombre];
  mazorca.material.needsUpdate = true;
  mazorca.scale.setScalar(0.01);
  mazorca.visible = true;
  mazorca.userData.t = 0;
}
// Encima de la cabeza: crece con un saltito y flota.
function animarPremio(dt) {
  if (!mazorca || !mazorca.visible) return;
  mazorca.userData.t += dt;
  const k = Math.min(1, mazorca.userData.t / 0.6);
  mazorca.scale.setScalar(1.6 * k * (2 - k));
  mazorca.position.set(character.object3D.position.x, py + 3.0 + 0.5 * k + Math.sin(mazorca.userData.t * 3) * 0.08, character.object3D.position.z);
}
function finalMitin(dt, cb) {
  const zPie = cb.position.z + 18.4;      // pie de los escalones del escenario
  const zParada = cb.position.z + 12.8;   // en medio del escenario
  playerX += (0 - playerX) * Math.min(1, dt * 4);
  let dz = 0;
  if (fin.fase === 0) {
    fin.v = Math.max(6, Math.min(fin.v - dt * 5, -zPie * 1.5 + 5));
    dz = fin.v * dt;
    character.updateRun(dt, Math.max(0.45, fin.v / BASE_SPEED));
    if (zPie + dz >= 0) fin.fase = 1;
  } else if (fin.fase === 1) {
    dz = Math.min(2.8 * dt, Math.max(0, -zParada));
    character.updateRun(dt, 0.45);
    if (zParada + dz >= -0.02) {
      fin.fase = 2; fin.t = 0;
      showBubble(nivelActual.fin[getLang()] || nivelActual.fin.es);
      vibrate([30, 40, 30]);
      mostrarPremio("maiz");
      spawnConfetti(30);
    }
  } else if (fin.fase === 2) {
    character.object3D.rotation.y += (Math.PI - character.object3D.rotation.y) * Math.min(1, dt * 5);
    character.setIdlePose(fin.t + 1);
    if (fin.t > 3.2) { fin.fase = 5; completarNivel(); }
  }
  if (dz) world.update(dz);
  // Los escalones: suben 1 en los 2,4 que hay entre el pie y el escenario.
  const subido = zPie + dz > 0 ? Math.min(1, (zPie + dz) / 2.4) : 0;
  if (fin.fase <= 1) py = subido;
  character.object3D.position.set(playerX, py, 0);
  shadowBlob.position.set(playerX, py + 0.015, 0);
  const cerca = fin.fase >= 2;
  const objetivo = cerca ? new THREE.Vector3(1.6, 3.6 + py, 10.5) : new THREE.Vector3(0, 4.6 + py, 11);
  const mira = cerca ? new THREE.Vector3(0, 2.6 + py, -3) : new THREE.Vector3(0, 2.4 + py, -8);
  camera.position.lerp(objetivo, Math.min(1, dt * 1.6));
  fin.look.lerp(mira, Math.min(1, dt * 1.6));
  camera.lookAt(fin.look);
}

function completarNivel() {
  gameState = "completado";
  const n = nivelActual;
  const tacos = Math.floor(tacosThisRun);
  const antes = getNiveles();
  const abiertosAntes = NIVELES.filter((x) => nivelAbierto(x, antes)).map((x) => x.id);
  const sinFinAntes = sinFinAbierto(antes);
  addTacos(tacos);
  const r = guardarNivel(n.id, { sinChocar: !intento.chocado, chapas: intento.chapas });
  misiones.fijarDisponibles(misionPosible);
  avisarMisiones([...misiones.evento("tacos", tacosThisRun), ...misiones.evento("distancia", distance)]);
  document.getElementById("nivelFinTitulo").textContent = n.id === "washington" ? t("llegadaCasaBlanca")
    : n.fin ? (n.fin[getLang()] || n.fin.es).replace(/\p{Extended_Pictographic}/gu, "").trim() : t("nivelSuperado");
  const ingrediente = INGREDIENTE[n.id] || "taco";
  document.getElementById("nivelFinPremio").src = urlPegatina(ingrediente);
  pintarSinFin();
  const est = estrellasDe(r);
  document.getElementById("nivelFinEstrellas").innerHTML = [0, 1, 2].map((i) => icono(i < est ? "estrella" : "estrellaVacia")).join("");
  // Los tres objetivos: lo de este intento, y las chapas que ya tenias.
  const chapasYa = r.chapas.filter(Boolean).length;
  const objetivos = [
    [true, t("objMeta")],
    [!intento.chocado || r.sinChocar, t("objSinChocar")],
    [chapasYa === 3, `${t("objChapas")} (${chapasYa}/3)`],
  ];
  document.getElementById("nivelFinObjetivos").innerHTML = objetivos.map(([ok, txt]) => `<li>${icono(ok ? "check" : "cruz")}<span>${txt}</span></li>`).join("");
  document.getElementById("nivelFinTacos").textContent = tacos;
  // ¿Se ha abierto algo nuevo?
  const ahora = getNiveles();
  const nuevos = NIVELES.filter((x) => nivelAbierto(x, ahora) && !abiertosAntes.includes(x.id));
  const avisos = nuevos.map((x) => t("nivelDesbloqueado").replace("{n}", x.nombre));
  if (!sinFinAntes && sinFinAbierto(ahora)) avisos.push(t("sinFinDesbloqueado"));
  const des = document.getElementById("nivelFinDesbloqueo");
  des.innerHTML = avisos.map((a) => `<div>${icono("candado").replace("#9aa4b8", "#2fa84f").replace("#9aa4b8", "#2fa84f")} ${a}</div>`).join("");
  des.classList.toggle("hidden", !avisos.length);
  pintarMisiones("misionesNivel");
  document.getElementById("nivelFin").classList.remove("hidden");
  spawnConfetti(45);
  sndFanfarria();
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
    showBubble(t("jefeVencido"));
    avisoVerde(`+150 ${TACO_IMG()}`);
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
// (Las frases estan en frases.js.)
let frasesPintadas = "";
function pintarFrases() {
  // Solo toca la pagina si algo ha cambiado (se llama en cada fotograma).
  const clave = gameState + frasesCargas + microVisto;
  if (clave === frasesPintadas) return;
  frasesPintadas = clave;
  const el = document.getElementById("hudFrases");
  el.innerHTML = Array.from({ length: MAX_FRASES }, (_, i) => `<span class="${i < frasesCargas ? "lleno" : "vacio"}">${icono(i < frasesCargas ? "micro" : "microVacio")}</span>`).join("");
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
  hablar(texto);
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
// 27/10: pausa, caida al chocar, parpadeo al seguir, el tramo que se ha
// anunciado y el jefe de los niveles.
let pausado = false, cuenta = 0, cayendo = 0, invulnerable = 0;
let tramoMostrado = null, jefeLanzado = false;
let mostrarTutorial = false;

// `desde`: metros desde los que se empieza (el punto de control); 0 = desde el principio.
function resetRun(desde = 0) {
  if (mazorca) mazorca.visible = false;
  currentLane = 1;
  playerX = 0;
  elapsed = 0; speed = BASE_SPEED; distance = desde;
  tacosThisRun = desde && intento && intento.control ? intento.control.tacos : 0;
  isJumping = false; jumpElapsed = 0;
  py = 0; vy = 0; enSuelo = true; camY = 0;
  megaTimeLeft = 0; character.setMega(1);
  freezeTimeLeft = 0; rocketTimeLeft = 0; nextJefeAt = JEFE_PRIMERO; misionesReloj = 0;
  frasesCargas = 1;   // empieza con una para que se pruebe enseguida
  if (monturaCohete) monturaCohete.visible = false;
  world.setCielo(false);
  document.getElementById("bossBar").classList.add("hidden");
  if (!desde) misiones.empezarPartida();
  isSliding = false; slideElapsed = 0;
  streak = 0; multiplier = 1; lastTacoTime = 0;
  shieldActive = false; magnetTimeLeft = 0; boostTimeLeft = 0;
  lastTacoShown = Math.floor(tacosThisRun);
  shakeTimeLeft = 0;
  pausado = false; cuenta = 0; cayendo = 0; invulnerable = 0;
  tramoMostrado = null; jefeLanzado = false;
  if (typeof apagarSirenas === "function") apagarSirenas();
  mostrarTutorial = !!nivelActual && nivelActual.numero === 1 && !getNiveles()[nivelActual.id];
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
  world.reset(desde);
  character.object3D.visible = true;
  fin = null;
  if (nivelActual && !desde) mostrarBanner(nivelActual);
  if (nivelActual && nivelActual.cameoJefe && !desde) {
    world.cameoJefe();
    setTimeout(() => { if (gameState === "playing") showBubble(t("robaTortilla"), 2600); }, 700);
  }
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
let hudFaltaPintada = -1;
function updateHud() {
  const tacoFloor = Math.floor(tacosThisRun);
  if (tacoFloor !== lastTacoShown) {
    const delta = tacoFloor - lastTacoShown;
    if (delta > 0) popupScore(delta);
    lastTacoShown = tacoFloor;
    pulse(document.getElementById("hudTacos"));
  }
  document.getElementById("hudTacoCount").textContent = tacoFloor;
  if (nivelActual) {
    // La barra: por donde vas y cuanto falta para la meta.
    pintarBarra(barras[0], distance);
    const falta = Math.max(0, Math.ceil((nivelActual.largo - distance) / 10) * 10);
    if (falta !== hudFaltaPintada) {
      hudFaltaPintada = falta;
      document.querySelector("#hudProgreso .pgTexto").textContent = t("faltanM").replace("{n}", falta.toLocaleString(getLang() === "en" ? "en" : "es"));
    }
  } else document.getElementById("hudScoreValue").textContent = Math.floor(distance);
  const streakEl = document.getElementById("hudStreak");
  if (multiplier > 1) { streakEl.textContent = "x" + multiplier; streakEl.classList.remove("hidden"); }
  else { streakEl.classList.add("hidden"); }
}

// 27/10: cada potenciador con su icono y una barrita que se vacia (antes un
// emoji y los segundos con decimales, que no se leian corriendo).
let badgePintado = "";
function updatePowerupBadge() {
  const badge = document.getElementById("powerupBadge");
  let p = null;
  if (rocketTimeLeft > 0) p = ["cohete", rocketTimeLeft / ROCKET_DURATION, t("powerupRocket")];
  else if (megaTimeLeft > 0) p = ["gorra", megaTimeLeft / MEGA_DURATION, t("powerupMega")];
  else if (freezeTimeLeft > 0) p = ["hielo", freezeTimeLeft / FREEZE_DURATION, t("powerupFreeze")];
  else if (shieldActive) p = ["escudo", 1, t("powerupShield")];
  else if (magnetTimeLeft > 0) p = ["iman", magnetTimeLeft / MAGNET_DURATION, t("powerupMagnet")];
  else if (boostTimeLeft > 0) p = ["boost", boostTimeLeft / BOOST_DURATION, t("powerupBoost")];
  if (!p) { badge.classList.add("hidden"); badgePintado = ""; return; }
  const [tipo, quedan, nombre] = p;
  if (badgePintado !== tipo + getLang()) {
    badge.innerHTML = `${icono(tipo)}<span>${nombre}</span><i class="pbBarra"><b></b></i>`;
    badgePintado = tipo + getLang();
  }
  badge.querySelector(".pbBarra b").style.transform = `scaleX(${quedan.toFixed(3)})`;
  badge.classList.remove("hidden");
}

// ---------- Globo de frases ----------
let bubbleTimeout = null;
function showBubble(text, ms = 1300) {
  const el = document.getElementById("speechBubble");
  el.textContent = text;
  el.classList.add("show");
  if (bubbleTimeout) clearTimeout(bubbleTimeout);
  bubbleTimeout = setTimeout(() => el.classList.remove("show"), ms);
  hablar(text);
}

// ---- Cartel de cada tramo y avisos del tutorial (27/10/2026) ----
function mostrarTramo(texto, claro = false) {
  const el = document.getElementById("tramoBanner");
  el.textContent = texto;
  el.classList.toggle("sprint", claro);
  el.classList.remove("hidden");
  el.style.animation = "none"; void el.offsetWidth; el.style.animation = "";
  clearTimeout(mostrarTramo.t);
  mostrarTramo.t = setTimeout(() => el.classList.add("hidden"), 2400);
}
const GESTOS = { carril: "lados", saltar: "arriba", agachar: "abajo", frase: "toque" };
function mostrarGesto(tipo) {
  const el = document.getElementById("avisoGesto");
  el.dataset.gesto = GESTOS[tipo] || "toque";
  el.querySelector(".gestoTexto").textContent = t("av_" + tipo);
  el.classList.remove("hidden");
  clearTimeout(mostrarGesto.t);
  mostrarGesto.t = setTimeout(() => el.classList.add("hidden"), 2300);
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
function accionJugador(action) {
  if (action === "pausa") { if (pausado) reanudar(); else pausar(); return; }
  if (gameState !== "playing" || pausado) return;
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
}
initControls(document.getElementById("touchControls"), accionJugador);

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
    if (invulnerable > 0) {
      // Recien seguido tras chocar: lo que hay delante se aparta.
      world.smash(o);
      continue;
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

// Chapas de campaña: hay que pasar justo por su sitio (no las atrae el iman).
function checkChapas() {
  for (const c of world.chapas) {
    if (c.collected || c.lane !== currentLane) continue;
    if (c.z < -0.9 || c.z > 0.9) continue;
    if (Math.abs(c.baseY - (py + 1.0)) > 0.8) continue;
    c.collected = true;
    if (!intento) continue;
    intento.chapas[c.idx] = true;
    pintarChapas();
    sndChapa();
    vibrate([20, 30, 20]);
    const n = intento.chapas.filter(Boolean).length;
    avisoVerde(`<img class="peg" src="${urlPegatina("chapa")}" alt=""> ${t("chapaCogida").replace("{n}", n)}`);
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
    world, character, renderer, scene, inmortal: false, choques: 0,
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
    intento: () => intento, tramo: () => tramoMostrado, velocidad: () => speed,
    // Pulsa como el jugador (carril, saltar, agacharse): para el piloto automatico de las pruebas.
    accion: (a) => accionJugador(a),
    paso: (n = 1, dt = 1 / 60) => { for (let i = 0; i < n; i++) frame(dt); },
  };
}

// ---- Chocar (27/10/2026) ----
// Antes: se quedaba congelado y salia la pantalla del sin fin («¡Te
// atraparon!», el record de metros y confeti aunque se hubiera perdido) y el
// nivel volvia a empezar de cero. Ahora se cae de espaldas y, en un nivel,
// sale cuanto faltaba para la meta y se puede seguir pagando tacos, desde el
// punto de control o desde el principio.
function triggerGameOver() {
  if (PRUEBA && window.__juego.inmortal) { window.__juego.choques++; return; }
  if (invulnerable > 0 || gameState !== "playing") return;
  gameState = "cayendo";
  cayendo = 0;
  if (intento) intento.chocado = true;
  speedLinesEl.style.opacity = "0";
  isSliding = false;
  sndHit();
  vibrate([80, 40, 80]);
  for (let d = 0; d < 8; d++) spawnDust(character.object3D.position.x, 0.4, 0);
}
function apagarSirenas() {
  document.getElementById("sirenas").classList.add("hidden");
  sirena(false);
}
function terminarCaida() {
  apagarSirenas();
  document.getElementById("hud").classList.add("hidden");
  document.getElementById("powerupBadge").classList.add("hidden");
  document.getElementById("bossBar").classList.add("hidden");
  gameState = "gameover";
  if (nivelActual) mostrarChoqueNivel();
  else mostrarFinSinFin();
}
// Seguir cuesta tacos (los guardados mas los de esta partida), cada vez el doble.
function precioSeguir() {
  return PRECIO_SEGUIR * Math.pow(2, intento ? intento.pagos : 0);
}
function puedePagar(precio) {
  return getSave().totalTacos + Math.floor(tacosThisRun) >= precio;
}
function pagar(precio) {
  if (!puedePagar(precio)) return false;
  const deGuardados = Math.min(getSave().totalTacos, precio);
  spendTacos(deGuardados);
  tacosThisRun -= precio - deGuardados;
  lastTacoShown = Math.floor(tacosThisRun);
  return true;
}
function botonSeguir(id) {
  const b = document.getElementById(id);
  const precio = precioSeguir();
  b.innerHTML = `${t("seguirAqui").replace("{n}", precio)} ${TACO_IMG()}`;
  b.disabled = !puedePagar(precio);
  b.classList.toggle("apagado", b.disabled);
}
function mostrarChoqueNivel() {
  const n = nivelActual;
  document.getElementById("choqueTitulo").textContent = t("chocaste");
  const falta = Math.max(0, Math.round(n.largo - distance));
  document.getElementById("choqueFalta").textContent = t("faltaban")
    .replace("{n}", falta.toLocaleString(getLang() === "en" ? "en" : "es"))
    .replace("{m}", n.metaNombre ? (n.metaNombre[getLang()] || n.metaNombre.es) : "");
  pintarBarra(barras[1], distance);
  document.getElementById("choqueTacos").textContent = Math.floor(tacosThisRun);
  botonSeguir("choqueSeguirAqui");
  document.getElementById("choqueControl").classList.toggle("hidden", !intento.control);
  document.getElementById("choqueNivel").classList.remove("hidden");
}
function mostrarFinSinFin() {
  avisarMisiones([...misiones.evento("tacos", tacosThisRun), ...misiones.evento("distancia", distance)]);
  pintarMisiones("misionesFin");
  const record = Math.floor(distance) > getSave().bestScore;
  document.getElementById("finalScore").textContent = Math.floor(distance);
  document.getElementById("finalTacos").textContent = Math.floor(tacosThisRun);
  document.getElementById("bestLine").innerHTML = record ? `${icono("estrella")} ${t("newRecord")}` : "";
  botonSeguir("seguirSinFin");
  document.getElementById("gameOverScreen").classList.remove("hidden");
  if (record) spawnConfetti(40);
}
// Cerrar la carrera: se guardan los tacos de esta partida (y el record del sin fin).
function cerrarCarrera() {
  if (gameState === "cerrada" || gameState === "completado") return;
  addTacos(Math.floor(tacosThisRun));
  if (!nivelActual) reportRunScore(Math.floor(distance));
  avisarMisiones([...misiones.evento("tacos", tacosThisRun), ...misiones.evento("distancia", distance)]);
  gameState = "cerrada";
}
// Seguir justo donde se choco: lo de delante se aparta y se parpadea un rato.
function seguirAqui() {
  if (!pagar(precioSeguir())) return;
  if (!intento) intento = nuevoIntento();
  intento.pagos++;
  for (const o of world.obstacles) if (!o.smashed && o.z > -6 && o.z < 4) world.smash(o);
  character.setSlidePose(false);
  invulnerable = INVULNERABLE;
  gameState = "playing";
  for (const id of ["choqueNivel", "gameOverScreen"]) document.getElementById(id).classList.add("hidden");
  document.getElementById("hud").classList.remove("hidden");
  if (world.jefeActivo()) document.getElementById("bossBar").classList.remove("hidden");
  sndPoint();
  empezarCuenta();
}

// ---- Pausa (27/10/2026): boton arriba a la derecha, y sola al salir de la app ----
function pausar() {
  if (gameState !== "playing" || pausado) return;
  pausado = true;
  sirena(false);
  cuenta = 0;
  document.getElementById("cuentaAtras").classList.add("hidden");
  const info = nivelActual
    ? `${t("nivel")} ${nivelActual.numero} · ${nivelActual.nombre}<br>${t("faltanM").replace("{n}", Math.max(0, Math.round(nivelActual.largo - distance)))}`
    : `${Math.floor(distance)} m`;
  document.getElementById("pausaInfo").innerHTML = info;
  pintarBotonesSonido();
  document.getElementById("pausaOverlay").classList.remove("hidden");
  pausarMusica(true);
}
function reanudar() {
  if (!pausado) return;
  if (tramoMostrado && tramoMostrado.tipo === "persecucion") sirena(true);
  document.getElementById("pausaOverlay").classList.add("hidden");
  pausarMusica(false);
  empezarCuenta();
}
// 3, 2, 1 antes de volver a correr (para no chocar nada mas quitar la pausa).
function empezarCuenta() {
  pausado = true;
  cuenta = 1.5;
}
document.addEventListener("visibilitychange", () => { if (document.hidden && !PRUEBA) pausar(); });
window.addEventListener("blur", () => { if (!PRUEBA) pausar(); });
document.getElementById("pausaBtn").addEventListener("click", () => pausar());
document.getElementById("pausaSeguir").addEventListener("click", reanudar);
document.getElementById("pausaRepetir").addEventListener("click", () => {
  document.getElementById("pausaOverlay").classList.add("hidden");
  pausarMusica(false);
  cerrarCarrera();
  if (nivelActual) intento = nuevoIntento();
  resetRun();
  arrancar();
});
document.getElementById("pausaSalir").addEventListener("click", () => {
  document.getElementById("pausaOverlay").classList.add("hidden");
  pausarMusica(false);
  pausado = false;
  cerrarCarrera();
  const habiaNivel = !!nivelActual;
  volverAlMenu();
  if (habiaNivel) abrirMapa();
});
function pintarBotonesSonido() {
  const s = getSettings();
  document.getElementById("pausaMusica").innerHTML = icono(s.musicMuted ? "musicaNo" : "musica");
  document.getElementById("pausaSonido").innerHTML = icono(s.sfxMuted ? "sonidoNo" : "sonido");
  document.getElementById("musicMuteBtn").innerHTML = icono(s.musicMuted ? "musicaNo" : "musica");
  document.getElementById("sfxMuteBtn").innerHTML = icono(s.sfxMuted ? "sonidoNo" : "sonido");
}
document.getElementById("pausaMusica").addEventListener("click", () => {
  const m = !getSettings().musicMuted; setMusicMuted(m); updateSettings({ musicMuted: m }); pintarBotonesSonido();
});
document.getElementById("pausaSonido").addEventListener("click", () => {
  const m = !getSettings().sfxMuted; setSfxMuted(m); updateSettings({ sfxMuted: m }); pintarBotonesSonido();
});

// Botones de la pantalla de choque del nivel y del fin del sin fin.
document.getElementById("choqueSeguirAqui").addEventListener("click", seguirAqui);
document.getElementById("seguirSinFin").addEventListener("click", seguirAqui);
document.getElementById("choqueControl").addEventListener("click", () => {
  if (!intento.control) return;
  resetRun(salidaControl(nivelActual));
  arrancar();
  avisoVerde(`${icono("control")} ${t("controlGuardado")}`);
});
document.getElementById("choqueRepetir").addEventListener("click", () => {
  cerrarCarrera();
  intento = nuevoIntento();
  resetRun();
  arrancar();
});
document.getElementById("choqueMapa").addEventListener("click", () => {
  cerrarCarrera();
  volverAlMenu();
  abrirMapa();
});

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

  // En pausa se sigue dibujando (quieto); al quitarla, 3-2-1 y a correr.
  if (pausado) {
    if (cuenta > 0) {
      cuenta -= dt;
      const el = document.getElementById("cuentaAtras");
      const n = String(Math.max(1, Math.ceil(cuenta / 0.5)));
      if (el.textContent !== n || el.classList.contains("hidden")) {
        el.textContent = n;
        el.classList.remove("hidden");
        el.style.animation = "none"; void el.offsetWidth; el.style.animation = "";
      }
      if (cuenta <= 0) { pausado = false; el.classList.add("hidden"); }
    }
    renderer.render(scene, camera);
    return;
  }

  if (gameState === "playing") {
    elapsed += dt;
    if (nivelActual) {
      // Nivel: la velocidad va con lo recorrido (y un poco mas en el sprint).
      const k = Math.min(1, distance / nivelActual.largo);
      speed = BASE_SPEED + ((nivelActual.velMax || MAX_SPEED) - BASE_SPEED) * k;
      if (tramoMostrado && tramoMostrado.tipo === "sprint") speed *= SPRINT_EXTRA;
    } else speed = Math.min(MAX_SPEED, BASE_SPEED + elapsed * ACCEL);
    if (invulnerable > 0) {
      invulnerable = Math.max(0, invulnerable - dt);
      character.object3D.visible = invulnerable === 0 || Math.floor(invulnerable * 12) % 2 === 0;
    }
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

    // ---- Tramos: el cartel al entrar, el jefe de los niveles y el punto de control ----
    const tramo = world.tramoEn(distance);
    if (tramo !== tramoMostrado) {
      tramoMostrado = tramo;
      // (El del primer tramo no: saldria encima del cartel del nivel.)
      const titulo = tramo.titulo && tramo.desde > 0 ? t("tr_" + tramo.titulo) : "";
      if (titulo) mostrarTramo(titulo, tramo.tipo === "sprint");
      if (tramo.tipo === "sprint") { sndFanfarria(true); vibrate([20, 30, 20]); }
      // La policia te persigue: luces rojas y azules por los bordes y la sirena.
      const persigue = tramo.tipo === "persecucion";
      document.getElementById("sirenas").classList.toggle("hidden", !persigue);
      sirena(persigue);
      if (persigue) setTimeout(() => { if (gameState === "playing") showBubble(FRASES[getLang()].patrulla, 1800); }, 900);
    }
    if (nivelActual && tramo.tipo === "jefe" && !jefeLanzado && distance > tramo.desde + 25 && rocketTimeLeft === 0 && !world.jefeActivo()) {
      if (world.iniciarJefe()) {
        jefeLanzado = true;
        document.getElementById("bossFill").style.width = "100%";
        document.getElementById("bossBar").classList.remove("hidden");
        showBubble(t("jefeLlega"), 2200);
        triggerCameraShake(0.04);
      }
    }
    // En un nivel el Burrito-Bot se va cuando se acaba su tramo.
    if (nivelActual && tramo.tipo !== "jefe" && world.jefeActivo()) world.despedirJefe();
    if (nivelActual && nivelActual.control && intento && !intento.control && distance >= nivelActual.control) {
      intento.control = { tacos: Math.floor(tacosThisRun) };
      avisoVerde(`${icono("control")} ${t("controlGuardado")}`);
      vibrate(20);
    }
    const av = world.tomarAviso(distance);
    if (av && mostrarTutorial) mostrarGesto(av.tipo);
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
    checkChapas();
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
  } else if (gameState === "cayendo") {
    // Se cae de espaldas; la calle se para en seco y sale la pantalla de choque.
    cayendo += dt;
    character.setCaida(cayendo);
    world.update(Math.max(0, 0.2 - cayendo) * speed * dt);
    updateDust(dt);
    if (cayendo > 1.15) terminarCaida();
  } else if (gameState === "final") {
    frameFinal(dt);
  } else if (gameState === "menu") {
    idlePhase += dt;
    character.object3D.rotation.y = Math.PI + Math.sin(idlePhase * 0.5) * 0.4;
    character.setIdlePose(idlePhase);
    shadowBlob.position.set(0, 0.015, 0);
    shadowBlob.scale.setScalar(1);
    updateDust(dt);
  }

  if (!(PRUEBA && window.__juego && window.__juego.sinDibujar)) renderer.render(scene, camera);
  if (firstFrame) {
    firstFrame = false;
    const loadingScreen = document.getElementById("loadingScreen");
    if (loadingScreen) loadingScreen.classList.add("fadeOut");
    if (loadingScreen) setTimeout(() => loadingScreen.remove(), 350);
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
  b.innerHTML = `${icono(abierto ? "infinito" : "candado")}<span>${t("sinFin")}</span>`;
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
  startMusic("sinfin");
  nivelActual = null;
  intento = nuevoIntento();
  resetRun();
  document.getElementById("sinFinOverlay").classList.add("hidden");
  arrancar();
});
// Idioma en ajustes: marcar el elegido como los demas selectores.
function marcarIdioma() {
  const en = getLang() === "en";
  document.getElementById("settingsLangEs").classList.toggle("equippedBtn", !en);
  document.getElementById("settingsLangEn").classList.toggle("equippedBtn", en);
}
function volverAlMenu() {
  gameState = "menu";
  apagarSirenas();
  pausado = false;
  idlePhase = 0;
  if (mazorca) mazorca.visible = false;
  character.object3D.visible = true;
  character.object3D.position.set(0, 0, 0);
  character.object3D.rotation.set(0, 0, 0);
  character.setSlidePose(false);
  setCameraMode("menu");
  for (const id of ["gameOverScreen", "nivelFin", "mapaGira", "hud", "bossBar", "bannerNivel", "choqueNivel", "pausaOverlay", "cuentaAtras", "tramoBanner", "avisoGesto", "powerupBadge"]) document.getElementById(id).classList.add("hidden");
  document.getElementById("startScreen").classList.remove("hidden");
  pintarMisiones("misionesMenu");
  pintarSinFin();
  stopMusic();
}
document.getElementById("mapaCerrar").addEventListener("click", volverAlMenu);
document.getElementById("nivelFinMapa").addEventListener("click", () => { volverAlMenu(); abrirMapa(); });
document.getElementById("nivelFinRepetir").addEventListener("click", () => {
  intento = nuevoIntento();
  resetRun();
  arrancar();
});

document.getElementById("retryBtn").addEventListener("click", () => {
  cerrarCarrera();
  intento = nuevoIntento();
  resetRun();
  arrancar();
});

document.getElementById("menuBtn").addEventListener("click", () => { cerrarCarrera(); volverAlMenu(); });

function cambiarIdioma(lang) {
  if (lang) setLang(lang); else toggleLang();
  pintarIconos();
  marcarIdioma();
  pintarMisiones("misionesMenu");
  pintarSinFin();
}
document.getElementById("startLangBtn").addEventListener("click", () => cambiarIdioma());

// La tienda (27/10/2026): los tacos ya sirven para algo.
document.getElementById("startShopBtn").addEventListener("click", () => { unlockAudio(); abrirTienda(character); });
// El ranking mundial necesita un servidor: sigue oculto.
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
pintarBotonesSonido();

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
  pintarBotonesSonido();
});
sfxMuteBtn.addEventListener("click", () => {
  const s = getSettings();
  const muted = !s.sfxMuted;
  setSfxMuted(muted);
  updateSettings({ sfxMuted: muted });
  pintarBotonesSonido();
});
document.getElementById("settingsLangEs").addEventListener("click", () => cambiarIdioma("es"));
document.getElementById("settingsLangEn").addEventListener("click", () => cambiarIdioma("en"));
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
pintarIconos();
pintarPegatinas();
pintarBotonesSonido();
aplicarTienda(character);
requestAnimationFrame(tick);

// Para poder instalar el juego en el movil (26/10/2026): ver sw.js.
if ("serviceWorker" in navigator) {
  navigator.serviceWorker.register("sw.js").catch(() => {});
}
