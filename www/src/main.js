import * as THREE from "../vendor/three.module.min.js";
import { createCharacter } from "./character.js";
import { createWorld, LANE_X } from "./world.js";
import { initControls, setSwipeThreshold } from "./controls.js";
import {
  sndTaco, sndJump, sndSlide, sndLaneSwitch, sndHit, sndPoint, unlockAudio, vibrate, startMusic,
  setSfxVolume, setSfxMuted, setMusicVolume, setMusicMuted,
} from "./audio.js";
import { getSave, addTacos, reportRunScore, getSettings, updateSettings, resetProgress } from "./save.js";
import { applyI18n, toggleLang, setLang, t, randomCatchphrase } from "./i18n.js";
import { initErrorReporting, reportError } from "./errors.js";
import { makePool } from "./pool.js";

initErrorReporting();

const BASE_SPEED = 17;
const MAX_SPEED = 29;
const ACCEL = 0.24;
const JUMP_DURATION = 0.4;
const JUMP_HEIGHT = 1.35;
const SLIDE_DURATION = 0.5;
const STREAK_RESET_GAP = 2.2;
const MAGNET_DURATION = 6;
const BOOST_DURATION = 4;
const BOOST_MULT = 1.5;

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
const camera = new THREE.PerspectiveCamera(55, 1, 0.1, 150);

// Camara elevada y alejada tipo Minion Rush: el personaje se ve pequeno,
// se ve mucho tramo de pista por delante para reaccionar con tiempo.
const RACE_CAM = { pos: new THREE.Vector3(0, 5.2, 7.2), look: new THREE.Vector3(0, 0.6, -14) };
// Camara de menu por delante y a un lado: el personaje corre alejandose, asi
// que con la posicion antigua (z positivo) el menu solo enseñaba su espalda y
// la mochila. Ahora se le ve la cara y el traje, que es lo que da personalidad
// a la pantalla de inicio.
// Apunta por debajo del pecho (y=0.45) para que el personaje quede en la
// mitad ALTA del encuadre y se le vea la cara y el traje por encima de la
// tarjeta del menu, que ocupa el centro de la pantalla.
const MENU_CAM = { pos: new THREE.Vector3(-1.25, 1.25, -2.75), look: new THREE.Vector3(0, 0.45, 0) };
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

const world = createWorld(scene);

const character = createCharacter(getSave().equipped);
character.object3D.position.set(0, 0, 0);
scene.add(character.object3D);

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
function spawnDust(x, z) {
  const m = dustPool.acquire();
  m.visible = true;
  m.position.set(x + (Math.random() - 0.5) * 0.2, 0.03, z + 0.3 + Math.random() * 0.15);
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
let isJumping = false, jumpElapsed = 0;
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
  world.setForcedZone(zoneChoice === "auto" ? null : zoneChoice);
  world.reset();
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
  if (shieldActive) { badge.textContent = "🛡 " + t("powerupShield"); badge.classList.remove("hidden"); }
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
  else if (action === "jump" && !isJumping && !isSliding) { isJumping = true; jumpElapsed = 0; sndJump(); vibrate(15); }
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
  for (const o of world.obstacles) {
    // Usa la posicion X real del personaje, no el carril logico (que cambia
    // instantaneo al pulsar) -- asi solo choca si de verdad esta centrado
    // en ese carril, no si solo lo esta rozando de lado al cambiar.
    if (Math.abs(playerX - LANE_X[o.lane]) > HIT_LANE_TOLERANCE) continue;
    if (o.z < -0.7 || o.z > 0.7) continue;
    if (o.type === "low") {
      const jumpProgress = isJumping ? jumpElapsed / JUMP_DURATION : 0;
      const h = isJumping ? Math.sin(jumpProgress * Math.PI) * JUMP_HEIGHT : 0;
      if (h > 0.55) continue;
    } else if (o.type === "high") {
      if (isSliding) continue;
    }
    if (shieldActive) {
      shieldActive = false;
      character.setShieldActive(false);
      updatePowerupBadge();
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
    updatePowerupBadge();
  }
}

function triggerGameOver() {
  gameState = "gameover";
  speedLinesEl.style.opacity = "0";
  sndHit();
  vibrate([80, 40, 80]);
  addTacos(Math.floor(tacosThisRun));
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
  if (contextLost) return;
  const dt = Math.min(clock.getDelta(), 0.05);

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

    if (isJumping) {
      jumpElapsed += dt;
      const p = Math.min(1, jumpElapsed / JUMP_DURATION);
      const h = Math.sin(p * Math.PI) * JUMP_HEIGHT;
      character.object3D.position.y = h;
      character.setJumpPose(p);
      shadowBlob.scale.setScalar(Math.max(0.4, 1 - h / JUMP_HEIGHT));
      if (p >= 1) {
        isJumping = false;
        character.object3D.position.y = 0;
        shadowBlob.scale.setScalar(1);
        // Aterrizaje con peso: nube de polvo a los pies + vibracion corta.
        // Antes el salto terminaba en seco, sin ningun impacto. Se usa la X
        // real del personaje (ya incluye el desplazamiento de la curva) --
        // `curveX` de este frame todavia no existe aqui, se calcula despues.
        for (let d = 0; d < 5; d++) spawnDust(character.object3D.position.x, character.object3D.position.z);
        vibrate(10);
      }
    } else if (isSliding) {
      slideElapsed += dt;
      character.setSlidePose(true);
      if (slideElapsed >= SLIDE_DURATION) { isSliding = false; character.setSlidePose(false); }
    } else {
      character.updateRun(dt, speed / BASE_SPEED);
    }

    const curveX = world.update(frameSpeed * dt);
    // La pista curva: personaje/sombra se mueven con el mismo offset que el
    // grupo del mundo, asi que el carril relativo y las colisiones no cambian.
    character.object3D.position.x = playerX + curveX;
    checkCollisions();
    checkCollectibles(dt);
    checkPowerups();
    updateExpression(dt);
    updateHud();

    shadowBlob.position.x = playerX + curveX;
    shadowBlob.position.z = character.object3D.position.z;

    // ---- Camara dinamica: sigue en X, FOV punch en boost, temblor, inclinacion en giros ----
    // (magnitudes deliberadamente sutiles: la primera pasada se sintio muy exagerada)
    camBaseX += (playerX + curveX - camBaseX) * dt * 6;
    const targetFov = boostTimeLeft > 0 ? BASE_FOV + 1.2 : BASE_FOV;
    camera.fov += (targetFov - camera.fov) * Math.min(1, dt * 2.5);
    const tiltTarget = Math.max(-0.03, Math.min(0.03, -(playerX - prevX) * 0.6));
    camera.rotation.z += (tiltTarget - camera.rotation.z) * Math.min(1, dt * 4);
    let shakeX = 0, shakeY = 0;
    if (shakeTimeLeft > 0) {
      shakeTimeLeft = Math.max(0, shakeTimeLeft - dt);
      const k = shakeTimeLeft / SHAKE_DURATION;
      shakeX = (Math.random() - 0.5) * shakeMag * k;
      shakeY = (Math.random() - 0.5) * shakeMag * k * 0.6;
    }
    camera.position.x = camBaseX + shakeX;
    camera.position.y = RACE_CAM.pos.y + shakeY;
    camera.updateProjectionMatrix();

    // ---- Lineas de velocidad ----
    const speedFrac = Math.max(0, Math.min(1, (speed - BASE_SPEED * 1.15) / (MAX_SPEED - BASE_SPEED * 1.15)));
    speedLinesEl.style.opacity = String(Math.min(1, speedFrac * 0.8 + (boostTimeLeft > 0 ? 0.5 : 0)));

    // ---- Polvo bajo los pies (solo corriendo en el suelo, mas seguido cuanto mas rapido) ----
    if (!isJumping && !isSliding) {
      dustSpawnTimer -= dt;
      if (dustSpawnTimer <= 0) {
        if (speedFrac > 0.1) spawnDust(playerX + curveX, character.object3D.position.z);
        dustSpawnTimer = 0.12 - speedFrac * 0.06;
      }
    }
    updateDust(dt);
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
document.getElementById("startBtn").addEventListener("click", () => {
  unlockAudio();
  startMusic();
  resetRun();
  gameState = "playing";
  document.getElementById("startScreen").classList.add("hidden");
  document.getElementById("hud").classList.remove("hidden");
});

document.getElementById("retryBtn").addEventListener("click", () => {
  resetRun();
  gameState = "playing";
  document.getElementById("gameOverScreen").classList.add("hidden");
  document.getElementById("hud").classList.remove("hidden");
});

document.getElementById("menuBtn").addEventListener("click", () => {
  gameState = "menu";
  idlePhase = 0;
  character.object3D.position.set(0, 0, 0);
  character.object3D.rotation.set(0, 0, 0);
  setCameraMode("menu");
  document.getElementById("gameOverScreen").classList.add("hidden");
  document.getElementById("startScreen").classList.remove("hidden");
});

document.getElementById("langToggle").addEventListener("click", () => { toggleLang(); updatePowerupBadge(); });
document.getElementById("startLangBtn").addEventListener("click", () => { toggleLang(); });

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
document.getElementById("settingsLangEs").addEventListener("click", () => setLang("es"));
document.getElementById("settingsLangEn").addEventListener("click", () => setLang("en"));

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
