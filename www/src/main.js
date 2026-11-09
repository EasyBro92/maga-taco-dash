import * as THREE from "../vendor/three.module.min.js";
import { createCharacter } from "./character.js";
import { createWorld, LANE_X, CIELO_Y, RAMPA_LARGO, RAMPA_ALTO, SALTO_VY, SALTO_G } from "./world.js";
import { initControls, setSwipeThreshold } from "./controls.js";
import {
  sndTaco, sndJump, sndSlide, sndLaneSwitch, sndHit, sndPoint, unlockAudio, vibrate, startMusic, stopMusic,
  sndFanfarria, sndChapa, pausarMusica, hablar, decir, precargarVoces, callarVoces, sndCaida, sirena, sndTropiezo,
  setSfxVolume, setSfxMuted, setMusicVolume, setMusicMuted,
} from "./audio.js";
import { getSave, addTacos, spendTacos, reportRunScore, getSettings, updateSettings, resetProgress, getNiveles, guardarNivel, estrellasDe, persistSave } from "./save.js";
import { FORMAS, CENTROS } from "./mapa-eeuu.js";
import { ACTOS, PROLOGO, TOTAL_VOTOS, PARA_GANAR, nombreEstado, votosGanados, postDe } from "./historia.js";
import { NIVELES, piezasDeNivel, nivelAbierto, sinFinAbierto, usaKit, hitosDeNivel, salidaControl, OBJETOS_POR_NIVEL, PREMIO_OBJETOS } from "./levels.js";
import { icono, pintarIconos } from "./iconos.js";
import { lienzo as lienzoPegatina, urlPegatina } from "./pegatinas.js";
import { abrirTienda, aplicarTienda } from "./tienda.js";
import { PIEZAS_KIT } from "./edificios.js";
import { applyI18n, toggleLang, setLang, t, getLang } from "./i18n.js";
import { initErrorReporting, reportError } from "./errors.js";
import { makePool } from "./pool.js";
import { loadZoneModels, modelo, cargarCarpeta, cargarPersonaje } from "./models.js";
import * as misiones from "./missions.js";
import { FRASES, TRUMP, traduccion } from "./frases.js";
import { abrirCaja, cajasPendientes, guardarCaja, premioDiario } from "./cajas.js";

initErrorReporting();

// 24/10: arranque mas lento y subida mas suave (le mareaba ir tan rapido):
// de 13 a 25 en unos 100 s, en vez de 17 a 29 en 50 s.
const BASE_SPEED = 13;
const MAX_SPEED = 25;
const ACCEL = 0.12;
const JUMP_DURATION = 0.62;   // 26/10: mas rato en el aire (habia que estar muy encima para saltar)
const JUMP_HEIGHT = 1.7;
const SLIDE_DURATION = 0.5;
const STREAK_RESET_GAP = 4;   // 05/11: antes 2,2 (con menos tacos, entre tira y tira hay mas hueco)
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
const PREMIO_BASE = 500, PREMIO_ESTRELLA = 250;   // 05/11: el premio de cada victoria (750 a 1250 tacos)
const INVULNERABLE = 2.2;    // segundos de parpadeo al seguir: lo de delante no cuenta
// ---- 28/10/2026: ideas de Subway Surfers ----
const BOTAS_DURATION = 10;    // botas de vaquero: saltos altos (las «súper zapatillas»)
const BOTAS_ALTURA = 2.9;     // con ellas se salta por encima de los coches
const V_SALTO_BOTAS = Math.sqrt(2 * GRAVEDAD * BOTAS_ALTURA);
const RECUERDA_GESTO = 0.22;  // un salto pulsado justo antes de tocar suelo no se pierde
const COYOTE = 0.12;          // al caer del techo del autobus aun se puede saltar un instante
const CAIDA_RAPIDA = -16;     // deslizar en el aire: baja de golpe y rueda al tocar suelo
const PERSIGUE = 7;           // segundos que te sigue la policia tras un tropezon

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
  renderer.localClippingEnabled = true;   // 08/11: el corte de la calle en los interiores (world.js)
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
// 25/10: far de 150 a 320 (ver SPAWN_Z en world.js). 02/11: near de 0.1 a 0.5:
// la cámara nunca tiene nada a menos de medio metro, y así el buffer de
// profundidad es 5 veces más preciso de lejos (el suelo, el asfalto y lo que
// va pintado encima ya no se pisan entre sí a distancia).
const camera = new THREE.PerspectiveCamera(55, 1, 0.5, 320);

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
  // (Giro y luego cabeceo: asi el giro al cambiar de carril no tuerce el horizonte.)
  camera.rotation.order = "YXZ";
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
// 08/11: Chicago: el paraguas que te lleva volando (vuela como el cohete,
// colgado del paraguas, con el tupe al viento).
const monturaParaguas = modelo("obstaculos/paraguas_vuelo");
let enParaguas = false;
const _mano = new THREE.Vector3();
if (monturaParaguas) {
  monturaParaguas.scale.setScalar(1.25);
  monturaParaguas.position.set(0.35, 2.0, 0);
  monturaParaguas.visible = false;
  character.object3D.add(monturaParaguas);
}
function quitarParaguas() {
  enParaguas = false;
  if (monturaParaguas) monturaParaguas.visible = false;
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
// 07/11: la luz de la estacion del metro (calida y fija). Se mezcla poco a
// poco con la del nivel al entrar y al salir (world.factorMetro).
let luzBase = null, metroAntes = 0;
// La luz de cada interior: el metro, calida y algo oscura; el casino, dorada y
// roja; el Capitolio, blanca y calida, la mas clara.
const LUZ_INTERIOR = {
  metro: { hemi: new THREE.Color(0xffd6a0), suelo: new THREE.Color(0x7a5a3c), hemiI: 1.05, fill: new THREE.Color(0xffc890), fillI: 0.7, sunI: 0.2 },
  casino: { hemi: new THREE.Color(0xffd8b8), suelo: new THREE.Color(0xa04060), hemiI: 1.45, fill: new THREE.Color(0xfff0d0), fillI: 1.3, sunI: 0.3 },
  capitolio: { hemi: new THREE.Color(0xfff2dc), suelo: new THREE.Color(0xb39c7a), hemiI: 1.2, fill: new THREE.Color(0xfff4e4), fillI: 0.85, sunI: 0.35 },
  super: { hemi: new THREE.Color(0xf4f8ff), suelo: new THREE.Color(0xb0b8c2), hemiI: 1.3, fill: new THREE.Color(0xffffff), fillI: 1.0, sunI: 0.3 },
};
function guardarLuzBase() {
  luzBase = { sunI: sun.intensity, hemiC: hemi.color.clone(), hemiG: hemi.groundColor.clone(), hemiI: hemi.intensity,
    fillI: fill.intensity, fillC: fill.color.clone(), fillP: fill.position.clone() };
}
function luzMetro() {
  const f = world.factorMetro(), li = LUZ_INTERIOR[world.tipoInterior()];
  if (!luzBase || !li || (f === 0 && metroAntes === 0)) return;
  metroAntes = f;
  sun.intensity = luzBase.sunI + (li.sunI - luzBase.sunI) * f;
  hemi.color.copy(luzBase.hemiC).lerp(li.hemi, f);
  hemi.groundColor.copy(luzBase.hemiG).lerp(li.suelo, f);
  hemi.intensity = luzBase.hemiI + (li.hemiI - luzBase.hemiI) * f;
  fill.color.copy(luzBase.fillC).lerp(li.fill, f);
  fill.intensity = luzBase.fillI + (li.fillI - luzBase.fillI) * f;
  fill.position.copy(luzBase.fillP).lerp(_fillMetro, f);
  sunGlare.visible = f < 0.3;
}
const _fillMetro = new THREE.Vector3(0, 6, 10);
function aplicarLuz(luz) {
  metroAntes = 0;
  aplicarLuzNivel(luz);
  guardarLuzBase();
}
function aplicarLuzNivel(luz) {
  sunGlare.visible = true;
  fill.color.set(0xffffff); fill.intensity = 0.35; fill.position.set(-3, 4, -6);
  if (camera.far !== 320) { camera.far = 320; camera.updateProjectionMatrix(); }
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
  } else if (luz === "anochecer") {
    // Anochecer (Las Vegas): el sol ya casi no esta, luz rosada y baja desde
    // el oeste; el cielo morado da la luz de relleno. Lo demas lo ponen los neones.
    // 06/11 (4): Isidro: «el mapa de Las Vegas es algo oscuro, cuesta ver los
    // obstaculos». El sol venia de delante y lo que se ve de cada obstaculo (la
    // cara que mira al jugador) quedaba a oscuras. Ahora una luz suave por
    // detras de la camara, como la de las farolas y los neones, ilumina esa
    // cara, y el relleno del cielo es mas claro. El cielo sigue de noche.
    sun.color.set(0xffaaa0); sun.intensity = 1.0; sun.position.set(-8, 4, -1);
    hemi.color.set(0xd0c4f6); hemi.groundColor.set(0x6a5878);
    fill.color.set(0xfff0e8); fill.intensity = 1.15; fill.position.set(1.5, 6, 10);
  } else if (luz === "tornado") {
    // 08/11: Wichita, cielo de tornado: luz verdosa y apagada, con la de
    // relleno por detras para que los obstaculos se vean bien (lo de Las Vegas).
    sun.color.set(0xe0e8c0); sun.intensity = 0.85; sun.position.set(-4, 9, -6);
    hemi.color.set(0xc4d0b0); hemi.groundColor.set(0x5e5e48);
    fill.color.set(0xf0f4e0); fill.intensity = 0.85; fill.position.set(1.5, 6, 10);
  } else if (luz === "pradera") {
    // 08/11: Omaha, atardecer en la pradera: sol bajo y naranja por el oeste.
    sun.color.set(0xffa868); sun.intensity = 1.25; sun.position.set(-8, 4.5, -3);
    hemi.color.set(0xffd8bc); hemi.groundColor.set(0x8a6248);
    fill.intensity = 0.55; fill.position.set(1, 5, 9);
  } else if (luz === "invierno") {
    // Mañana de invierno (Des Moines): sol bajo y blanco por delante a la
    // derecha; la nieve rebota la luz, asi que el relleno de abajo es claro.
    sun.color.set(0xfff4e8); sun.intensity = 1.15; sun.position.set(6, 6, -7);
    hemi.color.set(0xe2ecff); hemi.groundColor.set(0xb4bfcc);
  } else if (luz === "dorada") {
    // 09/11: Milwaukee, tarde dorada: el sol bajo por detras y a la derecha
    // (el oeste), que pinta de oro las fachadas y el museo del fondo.
    sun.color.set(0xffd9a0); sun.intensity = 1.25; sun.position.set(5, 6, 7);
    hemi.color.set(0xffe8cc); hemi.groundColor.set(0x86705a);
  } else if (luz === "otono") {
    // 08/11: Chicago, mañana de otoño: sol claro y bajo por el este (a la izquierda).
    sun.color.set(0xfff0d8); sun.intensity = 1.2; sun.position.set(-6, 8, -5);
    hemi.color.set(0xe0ecff); hemi.groundColor.set(0x857c6c);
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

// ---- El mapa de la gira (02/11/2026: el mapa electoral de verdad) ----
// Los estados con su forma real y sus votos electorales, como en los mapas de
// las elecciones: los que faltan, azules; al ganarlo se pinta de rojo (más
// intenso con más estrellas). Los estados pequeños del noreste llevan una
// etiqueta aparte para poder tocarlos. Debajo, la barra de los 270 votos.
let nivelElegido = null;
// Etiquetas aparte de los estados pequeños: [x, y] de la caja (72x32).
const CAJA_W = 72, CAJA_H = 32;
const ETIQUETA_APARTE = {
  VT: [742, 58], NH: [818, 58],
  MA: [906, 200], RI: [906, 236], CT: [906, 272], NJ: [906, 308], DE: [906, 344], MD: [906, 380], DC: [906, 416],
};
// Dónde va el número cuando el centro calculado no queda bien. El de Hawái va
// fuera, al lado de las islas (en blanco), porque dentro no cabe.
const NUMERO_FUERA = { HI: [346, 566] };
const CENTRO_AJUSTE = { FL: [797, 552], ID: [200, 162], LA: [562, 470], MI: [690, 192], CA: [80, 282], KY: [692, 324] };
function centroEstado(e) {
  const a = ETIQUETA_APARTE[e];
  return a ? [a[0] + CAJA_W / 2, a[1] + CAJA_H / 2] : CENTRO_AJUSTE[e] || CENTROS[e];
}
// El que toca jugar: el primero abierto sin pasar (o el último ganado).
function nivelEnCurso(hechos) {
  return NIVELES.find((n) => nivelAbierto(n, hechos) && !hechos[n.id])
    || [...NIVELES].reverse().find((n) => hechos[n.id]) || NIVELES[0];
}
// 08/11/2026: al ganar, el siguiente que toca (el primero abierto sin pasar
// despues de este; si ya estan todos pasados, el siguiente abierto).
function siguienteAbierto(n, hechos) {
  const resto = NIVELES.slice(NIVELES.indexOf(n) + 1);
  return resto.find((x) => nivelAbierto(x, hechos) && !hechos[x.id])
    || NIVELES.find((x) => x !== n && nivelAbierto(x, hechos) && !hechos[x.id])
    || resto.find((x) => nivelAbierto(x, hechos)) || null;
}
function abrirMapa() {
  const svg = document.getElementById("mapaSvg");
  const hechos = getNiveles();
  const actual = nivelEnCurso(hechos);
  svg.setAttribute("viewBox", "0 14 980 594");
  let estados = "", textos = "";
  for (const n of NIVELES) {
    const e = n.estado;
    if (!FORMAS[e]) continue;
    const r = hechos[n.id];
    const clase = r ? `ganado e${Math.max(1, estrellasDe(r))}` : nivelAbierto(n, hechos) ? "abierto" : n.listo ? "cerrado" : "futuro";
    const a = ETIQUETA_APARTE[e];
    let extra = "";
    if (a) {
      // Raya desde la caja hasta el estado, y la caja con el nombre y los votos.
      const [cx, cy] = CENTROS[e];
      const arriba = a[1] < 120;
      const [lx, ly] = arriba ? [a[0] + CAJA_W / 2, a[1] + CAJA_H] : [a[0], a[1] + CAJA_H / 2];
      extra = `<line class="raya" x1="${lx}" y1="${ly}" x2="${cx}" y2="${cy}"/>`
        + `<rect class="caja" x="${a[0]}" y="${a[1]}" width="${CAJA_W}" height="${CAJA_H}" rx="6"/>`;
      textos += `<text class="enCaja" x="${a[0] + CAJA_W / 2}" y="${a[1] + 23.5}">${e} ${n.votos}</text>`;
    } else if (NUMERO_FUERA[e]) {
      const [x, y] = NUMERO_FUERA[e];
      textos += `<text class="fuera" x="${x}" y="${y + 10.5}">${n.votos}</text>`;
    } else {
      const [x, y] = centroEstado(e);
      textos += `<text x="${x}" y="${y + 10.5}">${n.votos}</text>`;
    }
    if (n.esJefe) {
      // La misma carita de jefe que sale en la ficha del nivel: a la derecha
      // del número, o en la esquina de la caja de los estados pequeños.
      const [x, y] = NUMERO_FUERA[e] || centroEstado(e);
      const [jx, jy, jl] = a ? [a[0] - 14, a[1] - 12, 24] : [x + String(n.votos).length * 9 + 3, y - 15, 28];
      textos += icono("jefe").replace("<svg class=\"ico\"", `<svg class="marcaJefe" x="${jx}" y="${jy}" width="${jl}" height="${jl}"`);
    }
    estados += `<g class="estado ${clase}" data-id="${n.id}"><path d="${FORMAS[e]}"/>${extra}</g>`;
  }
  const [ax, ay] = centroEstado(actual.estado);
  const leyenda = `<g class="leyenda"><rect class="lRojo" x="836" y="478" width="20" height="20" rx="4"/><text x="864" y="495">${t("mapaGanados")}</text>`
    + `<rect class="lAzul" x="836" y="508" width="20" height="20" rx="4"/><text x="864" y="525">${t("mapaPorGanar")}</text></g>`;
  svg.innerHTML = `<g class="capaEstados">${estados}</g><g class="capaTextos">${textos}</g>`
    + `<circle class="actual" cx="${ax}" cy="${ay}" r="24"/>${leyenda}`;
  // Los que se pueden jugar, encima, para que su borde dorado se vea entero.
  const capa = svg.querySelector(".capaEstados");
  capa.querySelectorAll(".estado.abierto").forEach((g) => capa.appendChild(g));
  svg.querySelectorAll(".estado").forEach((g) => g.addEventListener("click", () => elegirNivel(g.dataset.id)));
  pintarVotos(hechos);
  elegirNivel(nivelElegido || actual.id);
  document.getElementById("startScreen").classList.add("hidden");
  document.getElementById("mapaGira").classList.remove("hidden");
  if (!getSave().prologo && !PRUEBA) mostrarPrologo();
}
function pintarVotos(hechos) {
  const v = votosGanados(NIVELES, hechos);
  document.getElementById("votos").innerHTML =
    `<div class="votosFila"><span>${t("votosElectorales")}</span><b>${v} / ${TOTAL_VOTOS}</b></div>`
    + `<div class="votosBarra"><div class="votosLleno" style="width:${(100 * v) / TOTAL_VOTOS}%"></div>`
    + `<div class="votosMarca" style="left:${(100 * PARA_GANAR) / TOTAL_VOTOS}%"></div></div>`
    + `<div class="votosNota">${v >= PARA_GANAR ? t("yaPresidente") : t("paraGanar")}</div>`;
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
  const hechos = getNiveles();
  const r = hechos[id];
  const abierto = nivelAbierto(n, hechos);
  const i = NIVELES.indexOf(n);
  const L = getLang();
  document.querySelectorAll("#mapaSvg .estado").forEach((g) => {
    const si = g.dataset.id === id;
    g.classList.toggle("elegido", si);
    if (si) g.parentNode.appendChild(g); // encima de los vecinos, para que se vea el borde
  });
  // Para abrirlo: el nivel hecho anterior que falta por pasar.
  const falta = [...NIVELES.slice(0, i)].reverse().find((x) => x.listo && !hechos[x.id]);
  const cierre = !n.listo ? t("proximamente") : t("superaAntes").replace("{n}", falta ? falta.nombre : "");
  const acto = ACTOS[n.acto];
  const cabecera = n.acto < 6 ? `${t("actoN")} ${n.acto} · ${acto[L] || acto.es}` : `${t("finalActo")} · ${acto[L] || acto.es}`;
  const jefe = n.esJefe ? `<div class="miJefe">${icono("jefe")} ${t("jefeNivel").replace("{j}", acto.jefe[L] || acto.jefe.es)}</div>` : "";
  const atajo = n.id === "washington" && !NIVELES.slice(0, i).every((x) => x.listo) ? `<div class="miAtajo">${t("atajoDc")}</div>` : "";
  document.getElementById("mapaInfo").innerHTML =
    `<div class="miActo">${cabecera}</div>`
    + `<div class="miNombre">${r ? `<img class="peg" src="${urlPegatina("voto")}" alt="">` : ""} ${t("nivel")} ${n.numero} · ${n.nombre}</div>`
    + `<div class="miLugar">${n.lugar} · ${t("votosN").replace("{n}", n.votos)}</div>`
    + `<div class="miHistoria">${n.historia[L] || n.historia.es}</div>`
    + jefe + atajo
    + (abierto ? `<ul class="objetivos">${filaObjetivos(n, r)}</ul><button id="mapaJugar" class="bigBtn">${t("jugarNivel")}</button>`
      : `<div class="proximamente">${icono("candado")} ${cierre}</div>`);
  const b = document.getElementById("mapaJugar");
  if (b) b.addEventListener("click", () => empezarNivel(n));
}
// ---- El prólogo (28/10/2026): la primera vez que se abre el mapa ----
function mostrarPrologo() {
  const ov = document.getElementById("prologo");
  let i = 0;
  const pintar = () => {
    const p = PROLOGO[i];
    const [titulo, texto] = p[getLang()] || p.es;
    document.getElementById("prologoImg").innerHTML = p.peg ? `<img src="${urlPegatina(p.peg)}" alt="">` : icono(p.icono);
    document.getElementById("prologoTitulo").textContent = titulo;
    document.getElementById("prologoTexto").textContent = texto;
    document.getElementById("prologoPuntos").innerHTML = PROLOGO.map((_, k) => `<span class="${k === i ? "on" : ""}"></span>`).join("");
    document.getElementById("prologoSigue").textContent = i < PROLOGO.length - 1 ? t("prologoSigue") : t("prologoFin");
  };
  const cerrar = () => { ov.classList.add("hidden"); getSave().prologo = true; persistSave(); };
  document.getElementById("prologoSigue").onclick = () => { if (i < PROLOGO.length - 1) { i++; pintar(); } else cerrar(); };
  document.getElementById("prologoSalta").onclick = cerrar;
  pintar();
  ov.classList.remove("hidden");
}
document.getElementById("mapaHistoria").addEventListener("click", mostrarPrologo);
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
  return { chocado: false, chapas: [false, false, false], control: null, pagos: 0, objetos: [] };
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
// 27/10 (2): no la veia («pon una barra arriba»): iba fina y apretada entre
// los tacos y la pausa. Ahora va en su propia fila, a todo lo ancho, con
// «Faltan X m para el Flatiron», el porcentaje y la bandera de cuadros; y al
// pasar cada edificio famoso sale su nombre debajo.
const NOMBRE_HITO = {
  es: { rockefeller: "Rockefeller Center", catedral: "Catedral de San Patricio", biblioteca: "Biblioteca Pública", empire: "Empire State",
    madison: "Madison Square", courier: "The Courier", heladeria: "Heladería Dietsch", deposito_agua: "El depósito de agua",
    davis: "Edificio Davis", archivos_portico: "Archivos Nacionales", fbi: "Edificio del FBI", irs: "Edificio de Hacienda",
    correos_torre: "La antigua Oficina de Correos", willard: "Hotel Willard", tesoro: "Departamento del Tesoro",
    san_carlos: "Hotel San Carlos", westward_ho: "Westward Ho", biblioteca_barr: "Biblioteca Burton Barr", museo_arte: "Museo de Arte de Phoenix",
    museo_heard: "Museo Heard",
    piramide: "La pirámide", castillo: "El castillo", torre_eiffel: "La torre Eiffel", fuentes: "Las fuentes",
    cesar: "El palacio romano", noria: "La noria gigante", campanile: "El campanario de Venecia",
    parque_esculturas: "Parque de esculturas", hotel_fort: "Hotel Fort Des Moines", biblioteca_dm: "Biblioteca central",
    ruan: "La torre de acero", torre_801: "801 Grand, la torre más alta de Iowa", world_food: "Salón del Premio Mundial de la Alimentación",
    rio: "El río Des Moines",
    first_national: "First National, la torre más alta de Nebraska", woodmen: "La torre Woodmen", old_market: "El Old Market",
    orpheum: "El teatro Orpheum",
    epic_center: "Epic Center, la torre más alta de Kansas", museo_aviacion: "Museo de la aviación", century_ii: "Century II",
    old_courthouse: "El antiguo juzgado", busch_stadium: "El estadio de los Cardinals", union_station_stl: "Union Station",
    soldiers_monument: "El Monumento a los Soldados y Marineros", statehouse_in: "El Capitolio de Indiana",
    lucas_oil: "El estadio de los Colts", jw_marriott: "El hotel de cristal azul",
    spirit_detroit: "El Espíritu de Detroit", fox_theatre: "El teatro Fox",
    puno_joe_louis: "El puño de Joe Louis", guardian_building: "El Guardian Building",
    hancock: "El John Hancock", water_tower: "La Water Tower, la que aguantó el gran incendio",
    tribune_tower: "La Tribune Tower", wrigley_building: "El Wrigley Building", trump_chicago: "La torre Trump",
    gesu_church: "La iglesia del Gesu", germania: "El Germania, el de los cascos de cobre",
    pfister_hotel: "El hotel Pfister", city_hall_mke: "El Ayuntamiento de Milwaukee", us_bank_center: "El U.S. Bank Center, el más alto de Wisconsin" },
  en: { catedral: "St. Patrick's Cathedral", biblioteca: "Public Library", deposito_agua: "The water tower", davis: "Davis Building",
    archivos_portico: "National Archives", fbi: "FBI Building", irs: "IRS Building", correos_torre: "Old Post Office",
    tesoro: "Treasury Department", biblioteca_barr: "Burton Barr Library", museo_arte: "Phoenix Art Museum", museo_heard: "Heard Museum",
    heladeria: "Dietsch Brothers",
    piramide: "The pyramid", castillo: "The castle", torre_eiffel: "The Eiffel Tower", fuentes: "The fountains",
    cesar: "The Roman palace", noria: "The giant wheel", campanile: "The Venice bell tower",
    parque_esculturas: "Sculpture Park", biblioteca_dm: "Central Library", ruan: "The steel tower",
    torre_801: "801 Grand, Iowa's tallest tower", world_food: "World Food Prize Hall", rio: "The Des Moines River",
    first_national: "First National, Nebraska's tallest tower", woodmen: "Woodmen Tower", old_market: "The Old Market",
    orpheum: "The Orpheum Theater",
    epic_center: "Epic Center, Kansas's tallest tower", museo_aviacion: "Aviation museum", century_ii: "Century II",
    old_courthouse: "The Old Courthouse", busch_stadium: "The Cardinals ballpark", union_station_stl: "Union Station",
    soldiers_monument: "The Soldiers' and Sailors' Monument", statehouse_in: "The Indiana Statehouse",
    lucas_oil: "The Colts' stadium", jw_marriott: "The blue glass hotel",
    spirit_detroit: "The Spirit of Detroit", fox_theatre: "The Fox Theatre",
    puno_joe_louis: "The Joe Louis Fist", guardian_building: "The Guardian Building",
    hancock: "The John Hancock Center", water_tower: "The Water Tower, which survived the Great Fire",
    tribune_tower: "The Tribune Tower", wrigley_building: "The Wrigley Building", trump_chicago: "Trump Tower",
    gesu_church: "Gesu Church", germania: "The Germania Building, with its copper helmets",
    pfister_hotel: "The Pfister Hotel", city_hall_mke: "Milwaukee City Hall", us_bank_center: "The U.S. Bank Center, the tallest in Wisconsin" },
};
let hitosBarra = [], hitoAvisado = 0, mitadAvisada = false;
const barras = [...document.querySelectorAll(".pgPista")];
function prepararBarra() {
  const n = nivelActual;
  document.getElementById("hudProgreso").classList.toggle("hidden", !n);
  document.getElementById("hudScore").classList.toggle("hidden", !!n);
  document.getElementById("hudChapas").classList.toggle("hidden", !n || !n.chapas);
  if (!n) return;
  hitosBarra = hitosDeNivel(n);
  hitoAvisado = hitosBarra.filter((h) => h.d < distance).length;
  mitadAvisada = distance > n.largo / 2;
  hudFaltaPintada = -1;
  document.querySelector("#hudProgreso .pgHitoNombre").classList.add("hidden");
  const marcas = hitosBarra.map((h) => `<i class="pgHito" style="left:${(100 * h.d / n.largo).toFixed(1)}%"></i>`).join("")
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
  }).join("")
    + (nivelActual.objeto ? `<span class="objHud"><img src="${urlPegatina(nivelActual.objeto)}" alt="">${intento ? intento.objetos.filter(Boolean).length : 0}/${OBJETOS_POR_NIVEL}</span>` : "");
}
// ---- Llegada a la Casa Blanca: unos 10 segundos ----
// 0 frena y anda hasta la escalinata · 1 sube al portico y llega a la puerta
// · 2 se da la vuelta y saluda · 3 se gira y entra · 4 se cierran las puertas.
function iniciarFinal() {
  quitarReto();
  gameState = "final";
  apagarSirenas();
  fin = { fase: 0, t: 0, v: speed, look: new THREE.Vector3(0, 0.4, -18) };
  currentLane = 1;
  isSliding = false; character.setSlidePose(false);
  rocketTimeLeft = 0; freezeTimeLeft = 0; megaTimeLeft = 0; character.setMega(1);
  if (monturaCohete) monturaCohete.visible = false;
  quitarParaguas(); if (character.setViento) character.setViento(0);
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
  // 08/11: Isidro: «al llegar a la Casa Blanca el personaje gira de forma poco
  // natural». Rodeaba la fuente de lado, mirando siempre al frente. Ahora mira
  // hacia donde va por la curva (la pendiente del camino).
  if (fin.fase <= 1) {
    const pendiente = u > 9 && u < 31 ? -11 * Math.cos(((u - 9) / 22) * Math.PI) * (Math.PI / 22) : 0;
    const rumbo = -Math.atan(pendiente);
    character.object3D.rotation.y += (rumbo - character.object3D.rotation.y) * Math.min(1, dt * 6);
  }
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
    if (zPuerta + dz >= -1.4) { fin.fase = 2; fin.t = 0; showBubble(t("finCasaBlanca"), 1300, 3); vibrate([30, 40, 30]); mostrarPremio("taco_perfecto"); spawnConfetti(30); }
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
  shadowBlob.position.set(playerX, py + 0.06, 0);
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
    if (zParada + dz >= 0) { dz = Math.max(0, -zParada); fin.fase = 2; fin.t = 0; showBubble(finTexto(nivelActual), 1300, 3); vibrate([30, 40, 30]); mostrarPremio(premioDe(nivelActual)); spawnConfetti(30); }
  } else if (fin.fase === 2) {
    character.object3D.rotation.y += (Math.PI - character.object3D.rotation.y) * Math.min(1, dt * 5);
    character.setIdlePose(fin.t + 1);
    if (fin.t > 2.8) { fin.fase = 5; completarNivel(); }
  }
  if (dz) world.update(dz);
  py = 0;
  character.object3D.position.set(playerX, 0, 0);
  shadowBlob.position.set(playerX, 0.06, 0);
  const cerca = fin.fase >= 2;
  // En el diner, mas lejos y mas alto: que se vea el chile gigante del tejado.
  // 29/10: el nivel puede traer su propia camara (Las Vegas, mirando la torre).
  const lejos = zParadaDada !== undefined;
  const cf = nivelActual && nivelActual.camaraFinal;
  // 01/11: mirando hacia arriba, el destello del sol (se pinta encima de todo)
  // caia sobre el edificio del final: fuera mientras dura.
  // Y la camara, mas atras que en la carrera, dejaba fuera el fondo del cielo
  // (se veia un gris en pico): que vea mas lejos mientras dura.
  if (cerca && cf) {
    sunGlare.visible = false;
    if (camera.far !== 420) { camera.far = 420; camera.updateProjectionMatrix(); }
  }
  const objetivo = cerca ? (cf ? new THREE.Vector3(...cf.pos) : lejos ? new THREE.Vector3(2.6, 4.6, 16) : new THREE.Vector3(2.0, 3.2, 9.5)) : new THREE.Vector3(0, 4.6, 11);
  const mira = cerca ? (cf ? new THREE.Vector3(...cf.mira) : lejos ? new THREE.Vector3(0, 4.4, -6) : new THREE.Vector3(0, 2.2, -3)) : new THREE.Vector3(0, 2.4, -8);
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
// 28/10: ya no hay ingredientes: al ganar un estado sale la urna (en la Casa
// Blanca, el taco bowl que se pide al llegar).
function premioDe(n) { return n && n.id === "washington" ? "taco_perfecto" : "voto"; }
function finTexto(n) { return t("votaRojo").replace("{e}", nombreEstado(n.estado, getLang())); }
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
      showBubble(finTexto(nivelActual), 1300, 3);
      vibrate([30, 40, 30]);
      mostrarPremio(premioDe(nivelActual));
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
  shadowBlob.position.set(playerX, py + 0.06, 0);
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
  const votosAntes = votosGanados(NIVELES, antes);
  const estadoNuevo = !antes[n.id];   // (antes es el mismo objeto que se guarda: mirarlo ya)
  addTacos(tacos);
  const r = guardarNivel(n.id, { sinChocar: !intento.chocado, chapas: intento.chapas });
  misiones.fijarDisponibles(misionPosible);
  avisarMisiones([...misiones.evento("tacos", tacosThisRun), ...misiones.evento("distancia", distance)]);
  document.getElementById("nivelFinTitulo").textContent = n.id === "washington" ? t("llegadaCasaBlanca") : finTexto(n);
  document.getElementById("nivelFinPremio").src = urlPegatina(premioDe(n));
  pintarSinFin();
  const est = estrellasDe(r);
  // 05/11: con muchos menos tacos por la calle, cada victoria trae un premio
  // en tacos segun las estrellas, para que la tienda siga a mano.
  const premio = PREMIO_BASE + PREMIO_ESTRELLA * Math.max(1, est);
  addTacos(premio);
  const yaHechos = getNiveles();
  const votosAhora = votosGanados(NIVELES, yaHechos);
  const todoRojo = NIVELES.every((x) => x.id === "washington" || yaHechos[x.id]);
  document.getElementById("nivelFinVictoria").innerHTML = `<b>${t("victoria" + Math.max(1, est))}</b>`
    + (estadoNuevo ? ` · ${t("masVotos").replace("{n}", n.votos)}` : "")
    + `<div>${t("llevasVotos").replace("{n}", votosAhora)}</div>`;
  document.getElementById("nivelFinPost").innerHTML = `<div class="postCabeza"><img src="${urlPegatina("chapa")}" alt=""><div><b>${t("candidato")}</b><small>@ElCandidato</small></div></div>`
    + `<p>${postDe(n, getLang(), votosAntes, votosAhora, todoRojo)}</p>`;
  document.getElementById("nivelFinEstrellas").innerHTML = [0, 1, 2].map((i) => icono(i < est ? "estrella" : "estrellaVacia")).join("");
  // Los tres objetivos: lo de este intento, y las chapas que ya tenias.
  const chapasYa = r.chapas.filter(Boolean).length;
  const objetivos = [
    [true, t("objMeta")],
    [!intento.chocado || r.sinChocar, t("objSinChocar")],
    [chapasYa === 3, `${t("objChapas")} (${chapasYa}/3)`],
  ];
  // 05/11: el objeto de la ciudad (no cuenta para las estrellas: da tacos).
  if (n.objeto) {
    const cogidos = intento.objetos.filter(Boolean).length;
    objetivos.push([cogidos === OBJETOS_POR_NIVEL, `${t("objObjetos").replace("{o}", nombreObjetos(n))} (${cogidos}/${OBJETOS_POR_NIVEL})`]);
  }
  document.getElementById("nivelFinObjetivos").innerHTML = objetivos.map(([ok, txt]) => `<li>${icono(ok ? "check" : "cruz")}<span>${txt}</span></li>`).join("");
  document.getElementById("nivelFinTacos").textContent = tacos + premio;
  document.getElementById("nivelFinBonus").textContent = t("premioVictoria").replace("{n}", premio);
  // ¿Se ha abierto algo nuevo?
  const ahora = getNiveles();
  const nuevos = NIVELES.filter((x) => nivelAbierto(x, ahora) && !abiertosAntes.includes(x.id));
  const avisos = nuevos.map((x) => t("nivelDesbloqueado").replace("{n}", x.nombre));
  if (!sinFinAntes && sinFinAbierto(ahora)) avisos.push(t("sinFinDesbloqueado"));
  const des = document.getElementById("nivelFinDesbloqueo");
  des.innerHTML = avisos.map((a) => `<div>${icono("candado").replace("#9aa4b8", "#2fa84f").replace("#9aa4b8", "#2fa84f")} ${a}</div>`).join("");
  des.classList.toggle("hidden", !avisos.length);
  pintarMisiones("misionesNivel");
  // 08/11/2026: el boton grande lleva al siguiente nivel, y el mapa ya lo
  // trae elegido (antes volvia a salir el mismo).
  const sig = siguienteAbierto(n, ahora);
  const bSig = document.getElementById("nivelFinSiguiente");
  bSig.classList.toggle("hidden", !sig);
  document.getElementById("nivelFinMapa").className = sig ? "smallBtn" : "bigBtn";
  if (sig) bSig.textContent = `${t("siguienteNivel")}: ${sig.nombre}`;
  nivelElegido = sig ? sig.id : null;
  document.getElementById("nivelFin").classList.remove("hidden");
  spawnConfetti(45);
  sndFanfarria();
  abrirCajasLuego(1800);
}
// ---- Jefe: barra de vida y premio ----
// 28/10: en Washington el Burrito-Bot viene mandado por la Liga del Pantano.
// 29/10: en Las Vegas es un debate.
// 03/11: y el dragon de China (Des Moines y el sin fin).
function textoJefe(clave) {
  const id = nivelActual && nivelActual.id;
  if (world.tipoJefe() === "dragon") return t(clave + "Dragon");
  return t(id === "washington" ? clave + "Dc" : id === "vegas" ? clave + "Vegas" : clave);
}
// La barra del jefe. En el debate es la encuesta: tú en rojo contra el robot
// en amarillo; empieza 50-50 y cada frase que le da te sube un 10 %.
function pintarBarraJefe(vida) {
  const debate = !!(nivelActual && nivelActual.debate);
  const barra = document.getElementById("bossBar");
  barra.classList.toggle("debate", debate);
  if (!debate) {
    barra.querySelector(".bossName").textContent = world.tipoJefe() === "dragon" ? t("dragonNombre") : "BURRITO-BOT";
    document.getElementById("bossFill").style.width = `${(vida / world.vidaJefe()) * 100}%`;
    return;
  }
  const yo = Math.round(50 + ((world.vidaJefe() - vida) / world.vidaJefe()) * 50);
  barra.querySelector(".bossName").innerHTML = `<span class="yo">${t("encuestaYo")} ${yo} %</span> ${t("encuesta")} <span class="el">${100 - yo} % BOT</span>`;
  document.getElementById("bossFill").style.width = `${yo}%`;
}
// 31/10: llega el helicoptero de la tele de las Fake News.
world.onHelicoptero(() => {
  setTimeout(() => { if (gameState === "playing") showBubble((FRASES[getLang()] || FRASES.es).furgoneta, 1600); }, 1200);
});
// 08/11/2026 (2): el desvio (levels.js, aplicarGiros). Al llegar al cruce, el
// cartel verde con la calle nueva pasa tapando la pantalla y, tapada, se quita
// la manzana que cerraba la calle de enfrente: ya vas por la otra calle.
world.onGiro((lado, calle, quitarMuro) => {
  const el = document.getElementById("giroCalle");
  el.querySelector("small").textContent = t("ahoraPor");
  el.querySelector(".placa").textContent = lado > 0 ? `${calle.toUpperCase()} →` : `← ${calle.toUpperCase()}`;
  el.getAnimations().forEach((a) => a.cancel());
  el.classList.remove("hidden");
  el.animate([{ transform: `translateX(${lado * 105}%)` }, { transform: "translateX(0)" }], { duration: 260, easing: "ease-out", fill: "forwards" });
  // (Con temporizadores y no al acabar la animacion: si la pagina no se ve,
  // las animaciones no avanzan y la manzana se quedaba puesta.)
  setTimeout(() => { quitarMuro(); vibrate(20); }, 270);
  setTimeout(() => {
    el.animate([{ transform: "translateX(0)" }, { transform: `translateX(${-lado * 105}%)` }], { duration: 260, easing: "ease-in", fill: "forwards" });
    setTimeout(() => el.classList.add("hidden"), 280);
  }, 620);
});
world.onJefe((evento, vida) => {
  const barra = document.getElementById("bossBar");
  if (evento === "golpe") {
    pintarBarraJefe(vida);
    triggerCameraShake(0.03);
    flashExpression("happy", 0.5);
  } else if (evento === "derrotado") {
    if (nivelActual && nivelActual.debate) pintarBarraJefe(0);
    else document.getElementById("bossFill").style.width = "0%";
    tacosThisRun += 150;
    showBubble(textoJefe("jefeVencido"), 1300, 3);
    avisoVerde(`+150 ${TACO_IMG()}`);
    spawnConfetti(30);
    triggerCameraShake(0.06);
    vibrate([40, 30, 80]);
    avisarMisiones(misiones.evento("jefe"));
    setTimeout(() => barra.classList.add("hidden"), 1500);
  } else if (evento === "pasa") {
    showBubble(t("jefePasaVa"), 1300, 2);
  } else if (evento === "escapa") {
    showBubble(textoJefe("jefeEscapa"), 1300, 3);
    setTimeout(() => barra.classList.add("hidden"), 1000);
  }
});

const shadowBlob = new THREE.Mesh(
  new THREE.CircleGeometry(0.4, 16),
  new THREE.MeshBasicMaterial({ color: 0x000000, transparent: true, opacity: 0.32, depthWrite: false, polygonOffset: true, polygonOffsetFactor: -4, polygonOffsetUnits: -8 })
);
shadowBlob.rotation.x = -Math.PI / 2;
shadowBlob.position.y = 0.06;
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
let frasesCargas = 0, microVisto = false, fraseDebate = 0;
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
  if (o) { texto = f[o.pool] && f[o.pool] !== dichasHace[dichasHace.length - 1] ? f[o.pool] : sinRepetir(f.nada); objetivo = o; }
  else if (world.jefeActivo()) { texto = world.tipoJefe() === "dragon" ? f.dragon : f.jefe; objetivo = "jefe"; }
  else { texto = sinRepetir(f.nada); objetivo = null; }
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
// 28/10: botas, gesto recordado, tropezon y el coche que te persigue.
let botasTimeLeft = 0;
let gestoGuardado = null, gestoReloj = 0, coyote = 0;
let carrilAntes = 1, tropiezo = 0, persigueLeft = 0;
// 27/10: pausa, caida al chocar, parpadeo al seguir, el tramo que se ha
// anunciado y el jefe de los niveles.
let pausado = false, cuenta = 0, cayendo = 0, invulnerable = 0;
let tramoMostrado = null, jefeLanzado = false;
// 03/11: con el dragon delante, el presidente grita «¡China!» de vez en cuando.
// En el sin fin los jefes se turnan: primero el dragon y luego el robot.
let gritoChina = 0, jefeSinFin = "dragon";
let mostrarTutorial = false;

// `desde`: metros desde los que se empieza (el punto de control); 0 = desde el principio.
function resetRun(desde = 0) {
  callarVoces(); precargarVoces();
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
  quitarParaguas(); if (character.setViento) character.setViento(0);
  if (character.setChaleco) character.setChaleco(false);
  world.setCielo(false);
  document.getElementById("bossBar").classList.add("hidden");
  if (!desde) misiones.empezarPartida();
  isSliding = false; slideElapsed = 0;
  streak = 0; multiplier = 1; lastTacoTime = 0;
  shieldActive = false; magnetTimeLeft = 0; boostTimeLeft = 0;
  botasTimeLeft = 0; gestoGuardado = null; gestoReloj = 0; coyote = 0;
  carrilAntes = 1; tropiezo = 0; persigueLeft = 0; world.perseguir(false, true);
  montado = false; superSalto = false; persigueMomento = false; dobleLeft = 0; reto = null;
  document.getElementById("retoBar").classList.add("hidden");
  lastTacoShown = Math.floor(tacosThisRun);
  shakeTimeLeft = 0;
  pausado = false; cuenta = 0; cayendo = 0; invulnerable = 0;
  tramoMostrado = null; jefeLanzado = false; gritoChina = 0; jefeSinFin = "dragon";
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
  world.reset(desde, { cajaHecha: !!(desde && intento && intento.caja),
    objetosHechos: desde && intento ? intento.objetos.map((v, i) => (v ? i : -1)).filter((i) => i >= 0) : [] });
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
      const meta = nivelActual.metaNombre ? (nivelActual.metaNombre[getLang()] || nivelActual.metaNombre.es) : "";
      document.querySelector("#hudProgreso .pgTexto").textContent = (meta ? t("faltanPara").replace("{m}", meta) : t("faltanM"))
        .replace("{n}", falta.toLocaleString(getLang() === "en" ? "en" : "es"));
      document.querySelector("#hudProgreso .pgPorcentaje").textContent = `${Math.min(100, Math.floor((100 * distance) / nivelActual.largo))} %`;
    }
    // El nombre de cada edificio famoso al pasarlo, y el aviso de la mitad.
    if (hitoAvisado < hitosBarra.length && distance >= hitosBarra[hitoAvisado].d - 25) {
      const hito = hitosBarra[hitoAvisado++];
      const el = document.querySelector("#hudProgreso .pgHitoNombre");
      el.textContent = (NOMBRE_HITO[getLang()] || {})[hito.pieza] || NOMBRE_HITO.es[hito.pieza] || "";
      el.classList.toggle("hidden", !el.textContent);
      el.style.animation = "none"; void el.offsetWidth; el.style.animation = "";
      clearTimeout(updateHud.tHito);
      updateHud.tHito = setTimeout(() => el.classList.add("hidden"), 2600);
      document.querySelectorAll("#hudProgreso .pgHito")[hitoAvisado - 1]?.classList.add("pasado");
    }
    // La mitad del camino: la barra late (el aviso es el del punto de control, que esta ahi mismo).
    if (!mitadAvisada && distance >= nivelActual.largo / 2) {
      mitadAvisada = true;
      if (!nivelActual.control) avisoVerde(t("mitadCamino"));
      const p = document.getElementById("hudProgreso");
      p.classList.remove("late"); void p.offsetWidth; p.classList.add("late");
    }
  } else document.getElementById("hudScoreValue").textContent = Math.floor(distance);
  const streakEl = document.getElementById("hudStreak");
  const mult = multiplier * (dobleLeft > 0 ? 2 : 1);
  if (mult > 1) { streakEl.textContent = "x" + mult; streakEl.classList.remove("hidden"); }
  else { streakEl.classList.add("hidden"); }
}

// 27/10: cada potenciador con su icono y una barrita que se vacia (antes un
// emoji y los segundos con decimales, que no se leian corriendo).
let badgePintado = "";
function updatePowerupBadge() {
  const badge = document.getElementById("powerupBadge");
  let p = null;
  if (rocketTimeLeft > 0) p = enParaguas ? ["paraguas", rocketTimeLeft / ROCKET_DURATION, t("powerupParaguas")] : ["cohete", rocketTimeLeft / ROCKET_DURATION, t("powerupRocket")];
  else if (megaTimeLeft > 0) p = ["gorra", megaTimeLeft / MEGA_DURATION, t("powerupMega")];
  else if (dobleLeft > 0) p = ["gorra", dobleLeft / DOBLE_DURATION, t("dobleTacos")];
  else if (freezeTimeLeft > 0) p = ["hielo", freezeTimeLeft / FREEZE_DURATION, t("powerupFreeze")];
  else if (botasTimeLeft > 0) p = ["botas", botasTimeLeft / BOTAS_DURATION, t("powerupBotas")];
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
// 31/10: sus frases de verdad (en ingles) llevan la traduccion debajo en
// castellano, y se quedan mas rato: son mas largas.
// 05/11: el globo sale cuando empieza a sonar la voz (audio.js: decir) y
// dura lo que ella; si hay otra frase sonando, espera su turno o no sale.
function showBubble(text, ms = 1300, prioridad = 1) {
  return decir(text, prioridad, (dura) => pintarGlobo(text, Math.max(ms, dura * 1000)), ms);
}
// 05/11: las frases al azar no se repiten: ninguna de las tres ultimas.
const dichasHace = [];
function sinRepetir(lista) {
  const vale = lista.filter((x) => !dichasHace.includes(x));
  const de = vale.length ? vale : lista;
  const f = de[Math.floor(Math.random() * de.length)];
  dichasHace.push(f);
  if (dichasHace.length > 3) dichasHace.shift();
  return f;
}
function pintarGlobo(text, ms) {
  const el = document.getElementById("speechBubble");
  const trad = traduccion(text, getLang());
  if (trad) {
    el.textContent = text;
    const s = document.createElement("small");
    s.textContent = trad;
    el.appendChild(s);
  } else el.textContent = text;
  if (TRUMP[text]) ms = Math.max(ms, 2600);
  el.classList.add("show");
  if (bubbleTimeout) clearTimeout(bubbleTimeout);
  bubbleTimeout = setTimeout(() => el.classList.remove("show"), ms);
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
  if (action === "left" && currentLane > 0) { carrilAntes = currentLane; currentLane--; sndLaneSwitch(); }
  else if (action === "right" && currentLane < 2) { carrilAntes = currentLane; currentLane++; sndLaneSwitch(); }
  else if (action === "frase") lanzarFrase();
  else if (action === "jump") {
    // 28/10: se puede saltar agachado (se levanta saltando), un instante
    // despues de caer de un techo, y si se pulsa en el aire justo antes de
    // tocar suelo, salta al aterrizar (antes ese toque se perdia).
    if (rocketTimeLeft > 0 || montado || superSalto) return;
    if (enSuelo || coyote > 0) saltar();
    else { gestoGuardado = "jump"; gestoReloj = RECUERDA_GESTO; }
  }
  // Deslizarse otra vez mientras ya te deslizas REINICIA el cronometro en vez
  // de ignorarse: con dos vallas seguidas el jugador da al boton por segunda
  // vez y antes se levantaba igual en medio de la segunda valla.
  else if (action === "slide") {
    if (rocketTimeLeft > 0 || montado || superSalto) return;
    if (!enSuelo) {
      // 28/10, como en Subway Surfers: en el aire baja de golpe y rueda al tocar suelo.
      vy = Math.min(vy, CAIDA_RAPIDA);
      gestoGuardado = "slide"; gestoReloj = 1;
    } else if (isSliding) { slideElapsed = 0; }
    else { isSliding = true; slideElapsed = 0; sndSlide(); }
  }
}
function saltar() {
  vy = botasTimeLeft > 0 ? V_SALTO_BOTAS : V_SALTO;
  enSuelo = false; isJumping = true; jumpElapsed = 0; coyote = 0;
  gestoGuardado = null; gestoReloj = 0;
  if (isSliding) { isSliding = false; character.setSlidePose(false); }
  sndJump(); vibrate(15);
}
initControls(document.getElementById("touchControls"), accionJugador);

// ---------- Colisiones ----------
const HIT_LANE_TOLERANCE = 0.85; // menos que medio ancho de carril (1.1): rozar el borde durante un cambio de carril no cuenta como choque
// Tropezon (28/10/2026, como en Subway Surfers): darse DE LADO contra algo al
// cambiar de carril ya no acaba la carrera. Rebota al carril de antes, pierde
// la racha y le sigue un coche de policia unos segundos; si vuelve a tropezar
// mientras, le pillan. Chocar de frente sigue siendo chocar.
function esDeLado(o, paso) {
  if (carrilAntes === currentLane || Math.abs(playerX - LANE_X[currentLane]) < 0.15) return false;
  if (o.type === "bus") return true;
  const zc = o.z + (o.centro || 0), medio = o.medio || 0.7;
  // Ya lo tenia al lado (no le ha llegado de frente este fotograma).
  return zc > -medio + 0.35 + paso * 2;
}
function tropezar(o) {
  o.rozado = true;
  const vuelta = carrilAntes;
  carrilAntes = currentLane;
  currentLane = vuelta;
  streak = 0; multiplier = 1;
  tropiezo = 0.5;
  sndTropiezo();
  vibrate([25, 40, 25]);
  triggerCameraShake(0.03);
  flashExpression("surprised", 0.9);
  if (PRUEBA && window.__juego) window.__juego.tropiezos++;
  if (persigueLeft > 0) {
    // Segundo tropezon con la policia detras: te pillan.
    showBubble(t("tePillaron"), 1600);
    triggerGameOver();
    return;
  }
  persigueLeft = PERSIGUE;
  world.perseguir(true);
  ponerSirenas();
  showBubble(t("tePersiguen"), 1600);
}
// Luces y sirena: en el tramo de persecucion y mientras te sigue el coche.
function ponerSirenas() {
  const policia = !persigueMomento || /patrulla|suv/.test((tramoMostrado && tramoMostrado.perseguidor) || "");
  const on = gameState === "playing" && !pausado && ((tramoMostrado && tramoMostrado.tipo === "persecucion") || (persigueLeft > 0 && policia));
  document.getElementById("sirenas").classList.toggle("hidden", !on);
  sirena(on);
}

function checkCollisions(paso = 0) {
  if (rocketTimeLeft > 0 || superSalto) return;          // en el cohete (y en el salto de la rampa) se vuela por encima de todo
  if (montado) {
    // 06/11 (3): en el vehiculo, todo lo que pilla sale volando.
    for (const o of world.obstacles) {
      if (o.smashed || o.type === "nada" || o.type === "rampa" || o.fuera || Math.abs(playerX - LANE_X[o.lane]) > 1.2) continue;
      const zc = o.type === "bus" ? o.z - 1 : o.z + (o.centro || 0), medio = o.type === "bus" ? 1.2 : (o.medio || 0.7);
      if (zc < -medio - 1.6 || zc > medio) continue;
      world.smash(o);
      sndHit(); vibrate(20); triggerCameraShake(0.02);
      tacosThisRun += 3 * multiplier;
    }
    return;
  }
  for (const o of world.obstacles) {
    // Usa la posicion X real del personaje, no el carril logico (que cambia
    // instantaneo al pulsar) -- asi solo choca si de verdad esta centrado
    // en ese carril, no si solo lo esta rozando de lado al cambiar.
    if (o.smashed || o.rozado || o.abierta || o.fuera) continue;   // (abierta: la barrera, con el brazo arriba; fuera: se quedo en la acera)
    if (o.type === "nada" || o.type === "rampa") continue;       // la alfombra, los arcos y la rampa se pisan
    if (Math.abs(playerX - LANE_X[o.lane]) > HIT_LANE_TOLERANCE) continue;
    if (o.type === "bus") {
      // Autobus: solo choca si te lo encuentras de lado o de frente a ras de
      // suelo (por la rampa se sube sin mas). `o.z` es lo que llevas metido
      // desde el pie de la rampa; la rampa mide 2.2 y el autobus entero 10.2.
      // (07/11: cada uno con su largo, su rampa y su techo; el coche del metro no tiene rampa.)
      const largo = o.largo || 10.2, rampa = o.rampa ?? 2.2, techo = o.techo || 1.55;
      if (o.z < (rampa ? 0.3 : -0.2) || o.z > largo) continue;
      const suelo = o.z < rampa ? techo * o.z / rampa : techo;
      if (py > suelo - 0.45) {
        if (o.z > 2.2 && !o.contado) { o.contado = true; avisarMisiones(misiones.evento("autobus")); }
        continue;
      }
    } else {
      const zc = o.z + (o.centro || 0);
      const medio = o.medio || 0.7;
      if (zc < -medio || zc > medio) continue;
      // 07/11: lo que va encima del techo del tren (`base`): desde abajo no se toca.
      const base = o.base || 0;
      if (base && py + 1.6 < base) continue;
      if (o.type === "low" && py > base + 0.55) {
        if (!o.contado) { o.contado = true; avisarMisiones(misiones.evento("saltos")); }
        continue;
      }
      if (o.type === "high" && isSliding) {
        if (!o.contado) { o.contado = true; avisarMisiones(misiones.evento("deslizar")); }
        continue;
      }
      if (o.alto !== undefined && py > base + o.alto - 0.1) continue;   // le pasas por encima
      // Con las botas se salta por encima de los coches y de todo lo que se esquiva.
      if (botasTimeLeft > 0 && o.type === "full" && py > (o.alto !== undefined ? o.alto : 1.8) - 0.1) continue;
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
    if (esDeLado(o, paso)) { tropezar(o); return; }
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
    // 05/11: antes salia una frase cada vez que subia (cada 5 tacos seguidos):
    // tres o cuatro en dos segundos. Ahora solo al llegar a x3 y a x5, y si no habla ya.
    if (multiplier === 3 || multiplier === 5) showBubble(sinRepetir((FRASES[getLang()] || FRASES.es).animo), 1300, 0);
    sndPoint();
    flashExpression("happy", 0.6);
  }
  tacosThisRun += amount * multiplier * (dobleLeft > 0 ? 2 : 1);
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
        cobrarTaco(tItem);
      }
      continue;
    }
    if (tItem.lane !== currentLane) continue;
    // A la altura del personaje (volando en cohete no se cogen los del suelo,
    // ni desde el suelo los del cielo). Holgado: los arcos se cogen saltando.
    if (Math.abs(tItem.baseY - (py + 0.9)) > 1.7) continue;
    if (tItem.z < -0.8 || tItem.z > 0.8) continue;
    tItem.collected = true;
    cobrarTaco(tItem);
  }
  if (streak > 0 && elapsed - lastTacoTime > STREAK_RESET_GAP) {
    streak = 0; multiplier = 1;
  }
}

// 05/11: un taco normal vale 1, el dorado 10; el objeto de la ciudad va aparte.
function cobrarTaco(tItem) {
  if (tItem.obj !== undefined) { cogerObjeto(tItem.obj); return; }
  if (reto) reto.n++;
  registerTaco(tItem.vale || (tItem.oro ? 10 : 1));
  sndTaco();
  if (tItem.oro) sndPoint();
}
function nombreObjetos(n) { return t("obj_" + n.objeto); }
function cogerObjeto(i) {
  sndChapa();
  vibrate(15);
  if (!intento || intento.objetos[i]) return;
  intento.objetos[i] = true;
  pintarChapas();
  const n = intento.objetos.filter(Boolean).length;
  if (n === OBJETOS_POR_NIVEL) {
    tacosThisRun += PREMIO_OBJETOS;
    avisoVerde(`<img class="peg" src="${urlPegatina(nivelActual.objeto)}" alt=""> ${t("objetosTodos").replace("{o}", nombreObjetos(nivelActual)).replace("{n}", PREMIO_OBJETOS)}`);
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
    else if (p.kind === "botas") { botasTimeLeft = BOTAS_DURATION; showBubble(t("powerupBotas") + "!"); vibrate([20, 20, 40]); }
    else if (p.kind === "caja") {
      // Caja sorpresa: se guarda y se abre al acabar (con ruleta).
      guardarCaja();
      if (intento) intento.caja = true;   // al seguir desde el control no vuelve a salir
      sndChapa();
      vibrate([20, 30, 20]);
      avisoVerde(`${icono("regalo")} ${t("cajaCogida")}`);
    }
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
      world.setCielo(true, speed * (boostTimeLeft > 0 ? BOOST_MULT : 1), ROCKET_DURATION);
      isSliding = false; character.setSlidePose(false);
      showBubble(t("powerupRocket") + "!");
      flashExpression("happy", 1.5);
      triggerCameraShake(0.05);
      vibrate([30, 30, 60]);
      avisarMisiones(misiones.evento("cohete"));
    } else if (p.kind === "paraguas") {
      // 08/11: Chicago: el viento te levanta colgado del paraguas.
      rocketTimeLeft = ROCKET_DURATION; enParaguas = true;
      if (monturaParaguas) monturaParaguas.visible = true;
      world.setCielo(true, speed * (boostTimeLeft > 0 ? BOOST_MULT : 1), ROCKET_DURATION);
      isSliding = false; character.setSlidePose(false);
      showBubble(t("paraguasVuela"), 1800);
      flashExpression("happy", 1.5);
      vibrate([30, 30, 60]);
    } else if (p.kind === "micro" && nivelActual && nivelActual.debate && world.jefeActivo()) {
      // El debate (Las Vegas): el microfono no se guarda, la frase sale ya.
      const lista = (FRASES[getLang()] || FRASES.es).debate;
      const texto = lista[fraseDebate++ % lista.length];
      world.lanzarFrase(currentLane, texto, "jefe");
      hablar(texto);
      flashExpression("determined", 0.6);
      vibrate(20);
    } else if (p.kind === "micro") {
      frasesCargas = Math.min(MAX_FRASES, frasesCargas + 1);
      if (!microVisto) { microVisto = true; showBubble(t("microfono")); }
      pintarFrases();
    } else if (p.kind === "gorra_fan") {
      // 06/11 (3): la gorra que lanzan los fans: tacos x2 unos segundos.
      dobleLeft = DOBLE_DURATION;
      showBubble(t("dobleTacos"), 1100, 0);
      vibrate(20);
    } else if (p.kind === "chile" || p.kind === "arancel") {
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
    world, character, renderer, scene, camera, inmortal: false, choques: 0, tropiezos: 0,
    botas: () => { botasTimeLeft = BOTAS_DURATION; },
    perseguido: () => persigueLeft,
    cajas: { abrir: () => abrirCaja(pintarCajaBtn), guardar: guardarCaja, diario: () => premioDiario(pintarCajaBtn), pintar: () => pintarCajaBtn() },
    estado: () => ({ fase: fin ? fin.fase : null, nivel: nivelActual ? nivelActual.id : null, gameState, py, vy, enSuelo, megaTimeLeft, freezeTimeLeft, rocketTimeLeft, botasTimeLeft, isSliding, currentLane, playerX, tacos: tacosThisRun, distancia: distance, montado, superSalto, reto: reto && { t: reto.t, n: reto.n }, dobleLeft, persigueLeft, py }),
    carril: (l) => { currentLane = l; },
    saltar: () => { if (enSuelo && !isSliding) { vy = V_SALTO; enSuelo = false; isJumping = true; jumpElapsed = 0; } },
    gigante: () => { megaTimeLeft = MEGA_DURATION; character.setMega(MEGA_SCALE); },
    rayo: () => { freezeTimeLeft = FREEZE_DURATION; },
    cohete: () => { rocketTimeLeft = ROCKET_DURATION; if (monturaCohete) monturaCohete.visible = true; world.setCielo(true, speed, ROCKET_DURATION); },
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
// ---- 06/11 (3): los momentos (ver world.js) ----
// Los que van encima de un tramo de la ciudad se arrancan al entrar en el
// tramo y se acaban al salir: te persiguen, el vehiculo y el reto relampago.
let montado = false, superSalto = false, persigueMomento = false, dobleLeft = 0, reto = null, confetiReloj = 0;
const VEHICULO_MULT = 1.2, DOBLE_DURATION = 6, RETO_TIEMPO = 10, RETO_META = 25, RETO_PREMIO = 100;
function velNivel(d) {
  // 06/11 (2): en los primeros 350 m hace casi la mitad de la subida, y el resto poco a poco hasta la meta.
  const ARRANQUE = 350, L = nivelActual.largo;
  const k = d < ARRANQUE ? 0.45 * (d / ARRANQUE) : 0.45 + 0.55 * Math.min(1, (d - ARRANQUE) / Math.max(1, L - ARRANQUE));
  return BASE_SPEED + ((nivelActual.velMax || MAX_SPEED) - BASE_SPEED) * k;
}
world.setVelEn((d) => (nivelActual ? velNivel(d) : null));
function empezarMomento(tr) {
  if (!tr || !nivelActual || gameState !== "playing") return;
  if (tr.tipo === "lluvia" && !tr.fichas) world.lanzarAvion();
  if (tr.momento === "persigue") {
    persigueMomento = true; persigueLeft = 1e6;
    world.perseguir(true, false, tr.perseguidor || null);
    setTimeout(() => { if (gameState === "playing" && persigueMomento) showBubble(t("persigueAviso"), 1800, 2); }, 900);
  } else if (tr.momento === "reto") {
    reto = { t: RETO_TIEMPO, n: 0, pintado: "" };
    document.getElementById("retoBar").classList.remove("hidden");
    pintarReto();
  }
}
// Salta encima del vehiculo aparcado: lo bastante alto para pasar por encima
// de la parte de atras (el camion de la basura es alto) y cae donde pisa.
function subirAlVehiculo() {
  const tope = world.subirVehiculo();
  montado = true;
  if (isSliding) { isSliding = false; character.setSlidePose(false); }
  vy = Math.sqrt(2 * GRAVEDAD * Math.max(JUMP_HEIGHT, tope - py + 1.0));
  enSuelo = false; isJumping = true; jumpElapsed = 0; coyote = 0; gestoGuardado = null; gestoReloj = 0;
  sndJump(); vibrate([20, 30, 40]); flashExpression("happy", 2);
  showBubble(t("subeAviso"), 1600, 2);
  // (09/11: en el camion de la basura se pone el chaleco al subir, y ya no se
  // lo quita hasta la meta.)
  if (tramoMostrado && tramoMostrado.tipo === "basura" && character.setChaleco) {
    character.setChaleco(true);
    setTimeout(() => { if (gameState === "playing") showBubble(t("chalecoAviso"), 1800); }, 1700);
  }
}
function terminarMomento(tr) {
  if (!tr) return;
  if (tr.momento === "persigue" && persigueMomento) { persigueMomento = false; persigueLeft = 0; world.perseguir(false); }
  if (tr.momento === "vehiculo" && montado) {
    montado = false;
    world.bajarVehiculo();
    if (gameState === "playing") saltar();
  }
}
function pintarReto() {
  const el = document.getElementById("retoBar");
  const texto = t("retoHud").replace("{n}", Math.min(reto.n, RETO_META)).replace("{m}", RETO_META).replace("{s}", Math.max(0, Math.ceil(reto.t)));
  if (texto !== reto.pintado) { el.querySelector(".bossName").textContent = texto; reto.pintado = texto; }
  el.querySelector(".retoFill").style.width = `${Math.max(0, reto.t / RETO_TIEMPO) * 100}%`;
}
function acabarReto(bien) {
  document.getElementById("retoBar").classList.add("hidden");
  if (bien) {
    tacosThisRun += RETO_PREMIO;
    showBubble(t("retoBien"), 1500, 2);
    avisoVerde(`+${RETO_PREMIO} ${TACO_IMG()}`);
    spawnConfetti(24);
    sndPoint(); vibrate([30, 30, 60]);
  } else showBubble(t("retoMal").replace("{n}", reto.n).replace("{m}", RETO_META), 1300, 1);
  reto = null;
}

function quitarReto() { if (reto) { reto = null; document.getElementById("retoBar").classList.add("hidden"); } }
function triggerGameOver() {
  if (PRUEBA && window.__juego.inmortal) { window.__juego.choques++; return; }
  if (invulnerable > 0 || gameState !== "playing") return;
  quitarReto();
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
  abrirCajasLuego(900);
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
  // 28/10: la policia se va (si no, el siguiente roce volvia a pillarle) y,
  // si sigue en el tramo de persecucion, vuelven sus luces.
  persigueLeft = 0; tropiezo = 0; gestoGuardado = null;
  world.perseguir(false);
  gameState = "playing";
  ponerSirenas();
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
  if ((tramoMostrado && tramoMostrado.tipo === "persecucion") || persigueLeft > 0) sirena(true);
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
      // 06/11 (2): Isidro: «algunos mapas largos al principio se hacen aburridos».
      // La velocidad subia igual por todo el nivel y en Washington (3,3 km)
      // apenas se notaba en el primer kilometro. Ahora en los primeros 350 m
      // hace casi la mitad de la subida, y el resto poco a poco hasta la meta.
      speed = velNivel(distance);
      if (tramoMostrado && tramoMostrado.tipo === "sprint") speed *= SPRINT_EXTRA;
    } else speed = Math.min(MAX_SPEED, BASE_SPEED + elapsed * ACCEL);
    if (invulnerable > 0) {
      invulnerable = Math.max(0, invulnerable - dt);
      character.object3D.visible = invulnerable === 0 || Math.floor(invulnerable * 12) % 2 === 0;
    }
    if (magnetTimeLeft > 0) { magnetTimeLeft = Math.max(0, magnetTimeLeft - dt); updatePowerupBadge(); }
    if (boostTimeLeft > 0) { boostTimeLeft = Math.max(0, boostTimeLeft - dt); updatePowerupBadge(); }
    if (botasTimeLeft > 0) { botasTimeLeft = Math.max(0, botasTimeLeft - dt); updatePowerupBadge(); }
    if (persigueLeft > 0) {
      persigueLeft = Math.max(0, persigueLeft - dt);
      if (persigueLeft === 0) { world.perseguir(false); ponerSirenas(); }
    }
    const frameSpeed = speed * (boostTimeLeft > 0 ? BOOST_MULT : 1) * (montado ? VEHICULO_MULT : 1);
    if (dobleLeft > 0) { dobleLeft = Math.max(0, dobleLeft - dt); updatePowerupBadge(); }
    // 07/11: confeti en el tunel de banderas de Findlay.
    if (tramoMostrado && tramoMostrado.tipo === "banderas") {
      confetiReloj -= dt;
      if (confetiReloj <= 0) { spawnConfetti(12); confetiReloj = 2.2; }
    }
    if (reto) {
      reto.t -= dt;
      if (reto.n >= RETO_META) acabarReto(true);
      else if (reto.t <= 0) acabarReto(false);
      else pintarReto();
    }
    distance += frameSpeed * dt;

    const targetX = LANE_X[currentLane];
    const prevX = playerX;
    playerX += (targetX - playerX) * Math.min(1, dt * 10);
    character.object3D.position.x = playerX;
    // Tropezon: un tambaleo corto.
    let tambaleo = 0;
    if (tropiezo > 0) { tropiezo = Math.max(0, tropiezo - dt); tambaleo = Math.sin(tropiezo * 30) * 0.6 * (tropiezo / 0.5); }
    character.setLean((playerX - prevX) * 12 + tambaleo);
    if (Math.abs(playerX - targetX) < 0.15) carrilAntes = currentLane;
    world.moverPerseguidor(dt, playerX);
    // 09/11: el vehiculo espera aparcado: se sube solo quien llega a su carril.
    const ve = !montado && rocketTimeLeft === 0 && world.vehiculoEsperando();
    if (ve && ve.z > -5 && ve.z - ve.largo < -0.5 && Math.abs(playerX - LANE_X[ve.lane]) < 0.9) subirAlVehiculo();
    world.moverVehiculo(dt, playerX);

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
      // (El paraguas se mece despacio con el viento.)
      if (enParaguas && monturaParaguas) monturaParaguas.rotation.z = Math.sin(elapsed * 1.8) * 0.08;
      if (rocketTimeLeft === 0) { if (monturaCohete) monturaCohete.visible = false; quitarParaguas(); world.quitarCielo(); }
      updatePowerupBadge();
    }

    // ---- El Burrito-Bot llega cada tantos metros ----
    world.setJugador(currentLane);
    if (nivelActual && distance >= nivelActual.largo - 1) { iniciarFinal(); return; }

    // ---- Tramos: el cartel al entrar, el jefe de los niveles y el punto de control ----
    const tramo = world.tramoEn(distance);
    if (tramo !== tramoMostrado) {
      const antes = tramoMostrado;
      tramoMostrado = tramo;
      terminarMomento(antes);
      empezarMomento(tramo);
      // 08/11: Chicago: en la ciudad del viento se le levanta el tupe.
      if (character.setViento) character.setViento(tramo.tipo === "viento" ? 1 : 0);
      if (tramo.tipo === "viento") setTimeout(() => { if (gameState === "playing") showBubble(t("tupeViento"), 1600); }, 1300);
      // 09/11: Milwaukee: al subir al camion de la basura se pone el chaleco
      // reflectante (y ya no se lo quita hasta la meta).
      // (El del primer tramo no: saldria encima del cartel del nivel.)
      const titulo = tramo.titulo && tramo.desde > 0 ? t("tr_" + tramo.titulo) : "";
      if (titulo) mostrarTramo(titulo, tramo.tipo === "sprint");
      if (tramo.tipo === "sprint") { sndFanfarria(true); vibrate([20, 30, 20]); }
      // La policia te persigue: luces rojas y azules por los bordes y la sirena.
      const persigue = tramo.tipo === "persecucion";
      ponerSirenas();
      if (persigue) setTimeout(() => { if (gameState === "playing") showBubble(FRASES[getLang()].patrulla, 1800); }, 900);
    }
    if (nivelActual && tramo.tipo === "jefe" && !jefeLanzado && distance > tramo.desde + 25 && rocketTimeLeft === 0 && !world.jefeActivo()) {
      if (world.iniciarJefe(tramo.jefe)) {
        jefeLanzado = true;
        gritoChina = 2.6;
        pintarBarraJefe(5);
        document.getElementById("bossBar").classList.remove("hidden");
        showBubble(textoJefe("jefeLlega"), 2200, 3);
        triggerCameraShake(0.04);
      }
    }
    // En un nivel el Burrito-Bot se va cuando se acaba su tramo.
    if (nivelActual && tramo.tipo !== "jefe" && tramo.tipo !== "jefe_paso" && world.jefeActivo()) world.despedirJefe();
    // 06/11 (3): el jefe de paso de los niveles sin jefe (tres barriles y se va).
    if (nivelActual && tramo.tipo === "jefe_paso" && !tramo.lanzado && distance > tramo.desde + 8 && rocketTimeLeft === 0 && !world.jefeActivo()) {
      tramo.lanzado = true;
      if (world.iniciarJefe("robot", true)) { showBubble(t("jefePasa"), 1800, 3); triggerCameraShake(0.03); }
    }
    if (nivelActual && nivelActual.control && intento && !intento.control && distance >= nivelActual.control) {
      intento.control = { tacos: Math.floor(tacosThisRun) };
      avisoVerde(`${icono("control")} ${t("controlGuardado")}`);
      vibrate(20);
    }
    const av = world.tomarAviso(distance);
    if (av && mostrarTutorial) mostrarGesto(av.tipo);
    if (!nivelActual && distance >= nextJefeAt && rocketTimeLeft === 0 && !world.jefeActivo() && world.iniciarJefe(jefeSinFin)) {
      nextJefeAt = distance + JEFE_CADA;
      jefeSinFin = jefeSinFin === "dragon" ? "robot" : "dragon";
      gritoChina = 2.6;
      pintarBarraJefe(5);
      document.getElementById("bossBar").classList.remove("hidden");
      showBubble(textoJefe("jefeLlega"), 1300, 3);
      triggerCameraShake(0.04);
    }

    // El grito: el primero en cuanto se va el aviso de que llega, y luego cada 6 a 9 s.
    if (world.jefeActivo() && world.tipoJefe() === "dragon") {
      gritoChina -= dt;
      if (gritoChina <= 0) {
        // Si esta hablando de otra cosa, lo vuelve a intentar enseguida.
        gritoChina = showBubble("CHINA!", 1500, 2) ? 6 + Math.random() * 3 : 1;
        flashExpression("determined", 0.6);
      }
    }

    // Misiones "de una partida": se miran una vez por segundo (no a cada
    // fotograma, que cada aviso guarda la partida).
    misionesReloj -= dt;
    if (misionesReloj <= 0) {
      misionesReloj = 1;
      avisarMisiones([...misiones.evento("tacos", tacosThisRun), ...misiones.evento("distancia", distance)]);
    }

    // ---- Altura: suelo, rampa y techo del autobus ----
    if (!superSalto && rocketTimeLeft === 0) {
      for (const o of world.obstacles) {
        if (o.type !== "rampa" || o.lanzado || o.z < RAMPA_LARGO - 0.25 || o.z > RAMPA_LARGO + 4 || Math.abs(playerX - LANE_X[o.lane]) > 1.1) continue;
        for (const r of world.obstacles) if (r.type === "rampa" && Math.abs(r.z - o.z) < 0.5) r.lanzado = true;
        superSalto = true; enSuelo = false; isJumping = true; jumpElapsed = 0; coyote = 0;
        if (isSliding) { isSliding = false; character.setSlidePose(false); }
        vy = Math.max(vy, SALTO_VY); py = Math.max(py, RAMPA_ALTO);
        sndJump(); vibrate([20, 30, 40]); flashExpression("happy", 2);
        break;
      }
    }
    const suelo = world.surfaceAt(playerX);
    if (enSuelo) {
      if (suelo < py - 0.05) { enSuelo = false; vy = 0; isJumping = true; jumpElapsed = JUMP_DURATION / 2; coyote = COYOTE; } // se acabo el techo: a caer
      else py = suelo;                                                    // por la rampa se sube andando
    }
    if (coyote > 0) coyote = Math.max(0, coyote - dt);
    if (gestoReloj > 0) { gestoReloj -= dt; if (gestoReloj <= 0) gestoGuardado = null; }
    if (!enSuelo && rocketTimeLeft === 0) {
      vy -= (superSalto ? SALTO_G : GRAVEDAD) * dt;
      py += vy * dt;
      if (py <= suelo && vy <= 0) {
        py = suelo; vy = 0; enSuelo = true; isJumping = false; superSalto = false;
        character.setJumpPose(1);
        // Aterrizaje con peso: nube de polvo a los pies + vibracion corta.
        for (let d = 0; d < 5; d++) spawnDust(character.object3D.position.x, character.object3D.position.z, py);
        vibrate(10);
        // Lo que se pulso en el aire: saltar otra vez o rodar al caer.
        const g = gestoGuardado;
        gestoGuardado = null; gestoReloj = 0;
        if (g === "jump") saltar();
        else if (g === "slide") { isSliding = true; slideElapsed = 0; sndSlide(); }
      }
    }
    character.object3D.position.y = py;
    shadowBlob.position.y = suelo + 0.06;
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
    } else if (montado) {
      character.setIdlePose(elapsed);   // de pie en el vehiculo
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
    checkCollisions(frameSpeed * dt);
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
    // 09/11: Isidro: «al cambiar de carril la camara deberia girar
    // directamente, deberia seguir para hacerlo mas frenetico». Ahora sigue
    // el cambio de carril entero y rapido (como Subway Surfers), y mientras
    // alcanza al jugador gira un poco hacia el (sin inclinar el horizonte).
    const xJugador = playerX + curveX;
    camBaseX += (xJugador - camBaseX) * Math.min(1, dt * 12);
    const targetFov = boostTimeLeft > 0 ? BASE_FOV + 1.2 : BASE_FOV;
    camera.fov += (targetFov - camera.fov) * Math.min(1, dt * 2.5);
    camera.rotation.y = THREE.MathUtils.clamp(-(xJugador - camBaseX) * 0.07, -0.06, 0.06);
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
    // 06/11 (3): tambien en el salto de la rampa; en el convoy se queda a la
    // altura de los techos (bajar y subir en cada hueco era otro vaiven).
    let alturaCam = rocketTimeLeft > 0 ? py : superSalto ? py * 0.85 : world.surfaceAt(playerX);
    if (tramoMostrado && tramoMostrado.tipo === "convoy") alturaCam = Math.max(alturaCam, 1.55);
    if (tramoMostrado && tramoMostrado.tipo === "metro_techo") alturaCam = Math.max(alturaCam, 2.2);
    luzMetro();
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
    world.moverPerseguidor(dt, playerX);
    world.update(Math.max(0, 0.2 - cayendo) * speed * dt);
    updateDust(dt);
    if (cayendo > 1.15) terminarCaida();
  } else if (gameState === "final") {
    frameFinal(dt);
  } else if (gameState === "menu") {
    idlePhase += dt;
    character.object3D.rotation.y = Math.PI + Math.sin(idlePhase * 0.5) * 0.4;
    character.setIdlePose(idlePhase);
    shadowBlob.position.set(0, 0.06, 0);
    shadowBlob.scale.setScalar(1);
    updateDust(dt);
  }

  // 08/11: Chicago: colgado del paraguas, el mango en la mano levantada.
  if (enParaguas && monturaParaguas && character.brazoArriba && character.brazoArriba(_mano)) monturaParaguas.position.set(_mano.x - 0.08, _mano.y - 0.05, _mano.z);
  if (!(PRUEBA && window.__juego && window.__juego.sinDibujar)) renderer.render(scene, camera);
  if (firstFrame) {
    firstFrame = false;
    const loadingScreen = document.getElementById("loadingScreen");
    if (loadingScreen) loadingScreen.classList.add("fadeOut");
    if (loadingScreen) setTimeout(() => loadingScreen.remove(), 350);
    pintarCajaBtn();
    setTimeout(mostrarDiario, 700);
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
  pintarCajaBtn();
  stopMusic();
}
// 28/10: cajas sorpresa sin abrir (se cogen en la calle) y premio del dia.
function pintarCajaBtn() {
  const n = cajasPendientes();
  const b = document.getElementById("cajaBtn");
  b.classList.toggle("hidden", !n);
  b.innerHTML = `${icono("regalo")} ${t("cajaAbrir")}${n > 1 ? " (" + n + ")" : ""}`;
}
document.getElementById("cajaBtn").addEventListener("click", () => abrirCaja(pintarCajaBtn));
function abrirCajasLuego(ms) {
  if (!cajasPendientes()) return;
  setTimeout(() => { if (cajasPendientes() && (gameState === "completado" || gameState === "gameover")) abrirCaja(pintarCajaBtn); }, ms);
}
function mostrarDiario() {
  if (PRUEBA) return;
  premioDiario(() => pintarCajaBtn());
}
document.getElementById("mapaCerrar").addEventListener("click", volverAlMenu);
document.getElementById("nivelFinMapa").addEventListener("click", () => { volverAlMenu(); abrirMapa(); });
document.getElementById("nivelFinSiguiente").addEventListener("click", () => {
  volverAlMenu(); abrirMapa();
  const b = document.getElementById("mapaJugar");
  if (b) b.click();
});
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
