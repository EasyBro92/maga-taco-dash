import * as THREE from "../vendor/three.module.min.js";
import { toon, withOutline } from "./toon.js";
import { makePool } from "./pool.js";
import { modelo, hayModelo, medidas, modeloConContorno, capaHielo } from "./models.js";
import { colocarNivel, ANCHO, azarConSemilla, sueloDeNivel } from "./levels.js";
import { construirEdificio, soltarEdificio } from "./edificios.js";
import { lienzo as lienzoPegatina } from "./pegatinas.js";
import { crearHorizonte } from "./horizonte.js";
import { t as tr } from "./i18n.js";

export const LANE_WIDTH = 2.2;
export const LANE_X = [-LANE_WIDTH, 0, LANE_WIDTH];
// Altura a la que vuela el cohete (los tacos del cielo van un poco mas arriba).
export const CIELO_Y = 7;
// Debe coincidir con BIOME_NAMES + "dc" dentro de createWorld(). Se duplica
// aqui a nivel de modulo (en vez de exportar la lista interna) para que
// main.js pueda construir el selector de zona sin acoplarse al cierre de
// createWorld().
export const ZONE_NAMES = ["city", "desert", "town", "dc"];

// Los objetos nacen MUY lejos (antes -90) para que cuando entren en el rango
// visible ya lleven mucho rato existiendo. Junto con camera.far=150 y la
// niebla en 118-150 (ver createWorld y main.js), el punto de nacimiento queda
// completamente fuera de lo que se ve.
// 25/10: de -128 a -280. Las cosas aparecian de golpe: nacian donde la niebla
// aun no las tapaba del todo, y los edificios altos asomaban como una silueta
// clara contra el cielo. Ahora nacen muy lejos, dentro de la bruma, y el cielo
// bajo es del mismo color que la niebla: van saliendo poco a poco.
const SPAWN_Z = -280;
const DESPAWN_Z = 8;
const ROW_SPACING = 7;

// Fundido de salida: los props laterales se encogen a 0 justo antes de
// reciclarse cerca del jugador, para no desaparecer de golpe. Sin fundido de
// ENTRADA a proposito -- crecer desde 0 al nacer, por lento que sea, se lee
// como "esto acaba de aparecer", que es justo lo que no queremos. En vez de
// eso los props nacen ya a escala completa, muy lejos (ver SPAWN_Z) y muy
// tapados por la niebla (ver fog en createWorld) -- se revelan poco a poco
// porque la niebla se va aclarando al acercarse, como si siempre hubieran
// estado ahi y la neblina simplemente dejara de taparlos.
function edgeFade(z, wrapZ, fadeOutDist) {
  return THREE.MathUtils.clamp((wrapZ - z) / fadeOutDist, 0, 1);
}

const GOLD = 0xffce3d;

// Brillo/glow compartido (usado por el taco)
const glowMat = new THREE.MeshBasicMaterial({ color: 0xffe27a, transparent: true, opacity: 0.3, depthWrite: false });
const glowGeo = new THREE.CircleGeometry(0.34, 16);

// Texturas procedurales (canvas) -> solo en navegador; en Node (tests) se omiten.
// Base clara y ruido suave: la textura se multiplica por el color de bioma
// (ver BIOME_COLORS/groundMat mas abajo), asi que tiene que partir de un
// gris claro/casi blanco para no oscurecer siempre el resultado.
// ---- Suelo estilo Minion Rush (22/10/2026) ----
// Texturas de dibujo animado: bases casi blancas (las tiñe el color de cada
// zona), manchas suaves grandes en vez de ruido fino, y baldosas con relieve
// pintado (luz arriba-izquierda, sombra abajo-derecha). Todo se dibuja tambien
// desplazado un lado entero para que la textura empalme sin costuras.
function lienzo(size, fondo) {
  const c = document.createElement("canvas");
  c.width = c.height = size;
  const ctx = c.getContext("2d");
  ctx.fillStyle = fondo;
  ctx.fillRect(0, 0, size, size);
  return { c, ctx };
}
function sinCostura(size, x, y, dibujar) {
  for (const dx of [-size, 0, size]) for (const dy of [-size, 0, size]) dibujar(x + dx, y + dy);
}
function mancha(ctx, x, y, r, claro, alfa) {
  const g = ctx.createRadialGradient(x, y, 0, x, y, r);
  const c = claro ? "255,255,255" : "0,0,40";
  g.addColorStop(0, `rgba(${c},${alfa})`);
  g.addColorStop(1, `rgba(${c},0)`);
  ctx.fillStyle = g;
  ctx.fillRect(x - r, y - r, r * 2, r * 2);
}
function texturaRepetida(c, rx, ry) {
  const tex = new THREE.CanvasTexture(c);
  tex.wrapS = tex.wrapT = THREE.RepeatWrapping;
  tex.colorSpace = THREE.SRGBColorSpace;
  tex.anisotropy = 8;
  tex.repeat.set(rx, ry);
  return tex;
}
// ---- 23/10: suelo que no marea ----
// Isidro se mareaba a los pocos segundos. Lo que pasa por debajo a 25-30 u/s
// tiene que ser casi liso: cualquier dibujo pequeño y con contraste (juntas
// oscuras, grietas, manchas, rayitas de cesped) se repite muchas veces por
// segundo y "tiembla" en pantalla. Ahora: juntas apenas marcadas, baldosas
// grandes, sin relieve pintado, y el asfalto sin grietas ni manchas.
function dibujarBaldosas(ctx, size, cols, filas, junta, variacion) {
  const w = size / cols, h = size / filas;
  ctx.fillStyle = "#dcd8d2";
  ctx.fillRect(0, 0, size, size);
  for (let i = 0; i < cols; i++) {
    for (let j = 0; j < filas; j++) {
      const x = i * w + junta / 2, y = j * h + junta / 2, bw = w - junta, bh = h - junta;
      const v = 240 + Math.round((Math.random() - 0.5) * variacion);
      ctx.fillStyle = `rgb(${v},${v},${v})`;
      ctx.beginPath();
      ctx.roundRect(x, y, bw, bh, junta);
      ctx.fill();
    }
  }
}

// Asfalto: liso con un granulado finisimo y de muy poco contraste (de lejos
// se funde en un tono uniforme; de cerca no parece plastico). Sin manchas ni
// grietas, que eran lo que se veia pasar y repetirse.
function makeAsphaltTexture() {
  if (typeof document === "undefined") return null;
  const size = 256;
  const { c, ctx } = lienzo(size, "#ececee");
  for (let i = 0; i < 1400; i++) {
    ctx.fillStyle = Math.random() < 0.5 ? "rgba(255,255,255,0.08)" : "rgba(0,0,20,0.05)";
    ctx.fillRect(Math.random() * size, Math.random() * size, 1.2, 1.2);
  }
  return texturaRepetida(c, 6, 45);
}

// Acera: losas grandes (1 x 2 por textura: unos 2 x 2.2) con la junta apenas marcada.
function makeSidewalkTexture() {
  if (typeof document === "undefined") return null;
  const size = 256;
  const { c, ctx } = lienzo(size, "#ffffff");
  dibujarBaldosas(ctx, size, 1, 2, 4, 6);
  return texturaRepetida(c, 2, 90);
}

// Suelo de plaza para ciudad y D.C.: losetas medianas, muy suaves.
function makePavingTexture() {
  if (typeof document === "undefined") return null;
  const size = 256;
  const { c, ctx } = lienzo(size, "#ffffff");
  dibujarBaldosas(ctx, size, 3, 3, 3, 8);
  return texturaRepetida(c, 10, 70);
}

// Cesped del pueblo: solo manchas grandes y suaves de tono, sin rayitas.
function makeGrassTexture() {
  if (typeof document === "undefined") return null;
  const size = 256;
  const { c, ctx } = lienzo(size, "#e9efe4");
  for (let i = 0; i < 18; i++) {
    const x = Math.random() * size, y = Math.random() * size, r = 30 + Math.random() * 40;
    sinCostura(size, x, y, (px, py) => mancha(ctx, px, py, r, Math.random() < 0.5, 0.05 + Math.random() * 0.04));
  }
  return texturaRepetida(c, 10, 70);
}

// Tierra/arena compacta para el bioma desierto: parches grandes e
// irregulares (no ruido fino uniforme como el asfalto) + un par de rodadas
// de neumatico, para que se lea como pista de tierra y no como autopista
// pintada. Misma base clara que el asfalto (se multiplica por el tinte de
// bioma igual que el resto del suelo).
function makeDirtTexture() {
  if (typeof document === "undefined") return null;
  const size = 128;
  const c = document.createElement("canvas");
  c.width = c.height = size;
  const ctx = c.getContext("2d");
  ctx.fillStyle = "#d9d3c4";
  ctx.fillRect(0, 0, size, size);
  for (let i = 0; i < 90; i++) {
    const v = Math.random() * 34 - 17;
    ctx.fillStyle = `rgba(${v > 0 ? 255 : 0},${v > 0 ? 255 : 0},${v > 0 ? 255 : 0},${Math.abs(v) / 60})`;
    const r = 3 + Math.random() * 7;
    ctx.beginPath();
    ctx.ellipse(Math.random() * size, Math.random() * size, r, r * (0.5 + Math.random() * 0.5), Math.random() * Math.PI, 0, Math.PI * 2);
    ctx.fill();
  }
  ctx.fillStyle = "rgba(0,0,0,0.1)";
  for (const x of [size * 0.38, size * 0.62]) {
    ctx.fillRect(x - 2, 0, 4, size);
  }
  const tex = new THREE.CanvasTexture(c);
  tex.wrapS = tex.wrapT = THREE.RepeatWrapping;
  tex.repeat.set(10, 70);
  return tex;
}

// Hormigon de acera con juntas de dilatacion (antes la acera era un plano de
// color liso sin ninguna textura -- se notaba muy plano al lado del asfalto
// con ruido y ahora la tierra con parches).
function makeConcreteTexture() {
  if (typeof document === "undefined") return null;
  const size = 128;
  const c = document.createElement("canvas");
  c.width = c.height = size;
  const ctx = c.getContext("2d");
  ctx.fillStyle = "#e4ddd0";
  ctx.fillRect(0, 0, size, size);
  for (let i = 0; i < 260; i++) {
    const v = Math.random() * 22 - 11;
    ctx.fillStyle = `rgba(${v > 0 ? 255 : 0},${v > 0 ? 255 : 0},${v > 0 ? 255 : 0},${Math.abs(v) / 70})`;
    ctx.fillRect(Math.random() * size, Math.random() * size, 1.4, 1.4);
  }
  ctx.strokeStyle = "rgba(0,0,0,0.18)";
  ctx.lineWidth = 2;
  for (let y = 0; y < size; y += size / 3) {
    ctx.beginPath();
    ctx.moveTo(0, y);
    ctx.lineTo(size, y);
    ctx.stroke();
  }
  const tex = new THREE.CanvasTexture(c);
  tex.wrapS = tex.wrapT = THREE.RepeatWrapping;
  tex.repeat.set(2, 90);
  return tex;
}

function makeCityTexture(name) {
  if (typeof document === "undefined") return null;
  const w = 512, h = 176;
  const c = document.createElement("canvas");
  c.width = w; c.height = h;
  const ctx = c.getContext("2d");
  ctx.fillStyle = "#0a3d1f";
  ctx.fillRect(0, 0, w, h);
  ctx.strokeStyle = "#ffffff";
  ctx.lineWidth = 10;
  ctx.strokeRect(12, 12, w - 24, h - 24);
  ctx.fillStyle = "#ffffff";
  ctx.textAlign = "center";
  ctx.font = "bold 36px sans-serif";
  ctx.fillText("WELCOME TO", w / 2, 68);
  ctx.font = "bold 58px sans-serif";
  ctx.fillText(name.toUpperCase(), w / 2, 140);
  return new THREE.CanvasTexture(c);
}

const US_CITIES = ["New York", "Chicago", "Miami", "Austin", "Phoenix", "Nashville", "Detroit", "Denver", "Atlanta", "Seattle", "Boston", "Las Vegas"];

// Base blanca + lineas oscuras finas: al multiplicarse con el color real
// del material (blanco x color = color), da un patron de tablillas/tejas
// sin perder el tinte deseado.
function makeClapboardTexture() {
  if (typeof document === "undefined") return null;
  const size = 64;
  const c = document.createElement("canvas");
  c.width = c.height = size;
  const ctx = c.getContext("2d");
  ctx.fillStyle = "#ffffff";
  ctx.fillRect(0, 0, size, size);
  ctx.strokeStyle = "rgba(0,0,0,0.2)";
  ctx.lineWidth = 2;
  for (let y = 5; y < size; y += 9) {
    ctx.beginPath();
    ctx.moveTo(0, y);
    ctx.lineTo(size, y);
    ctx.stroke();
  }
  const tex = new THREE.CanvasTexture(c);
  tex.wrapS = tex.wrapT = THREE.RepeatWrapping;
  tex.repeat.set(2, 3);
  return tex;
}

function makeShingleTexture() {
  if (typeof document === "undefined") return null;
  const size = 64;
  const c = document.createElement("canvas");
  c.width = c.height = size;
  const ctx = c.getContext("2d");
  ctx.fillStyle = "#ffffff";
  ctx.fillRect(0, 0, size, size);
  ctx.strokeStyle = "rgba(0,0,0,0.25)";
  ctx.lineWidth = 1.5;
  for (let row = 0; row < 8; row++) {
    const y = row * 8;
    const offset = row % 2 === 0 ? 0 : 4;
    for (let x = -8; x < size + 8; x += 8) {
      ctx.strokeRect(x + offset, y, 8, 8);
    }
  }
  const tex = new THREE.CanvasTexture(c);
  tex.wrapS = tex.wrapT = THREE.RepeatWrapping;
  tex.repeat.set(3, 2);
  return tex;
}

// La bandera de EE. UU. de las astas de la acera (27/10/2026).
function texturaBandera() {
  if (typeof document === 'undefined') return null;
  const c = document.createElement('canvas');
  c.width = 190; c.height = 100;
  const x = c.getContext('2d');
  for (let i = 0; i < 13; i++) { x.fillStyle = i % 2 ? '#ffffff' : '#c8303a'; x.fillRect(0, (i * 100) / 13, 190, 100 / 13 + 1); }
  x.fillStyle = '#2a3f8f'; x.fillRect(0, 0, 80, 54);
  x.fillStyle = '#ffffff';
  for (let f = 0; f < 5; f++) for (let k = 0; k < 6; k++) { x.beginPath(); x.arc(8 + k * 13 + (f % 2) * 6, 7 + f * 10, 2.2, 0, Math.PI * 2); x.fill(); }
  const t = new THREE.CanvasTexture(c);
  t.colorSpace = THREE.SRGBColorSpace;
  return t;
}

export function createWorld(scene) {
  const group = new THREE.Group();
  scene.add(group);

  scene.background = new THREE.Color(0x9fe6ff);
  // Vuelta 15: el pop-in seguia notandose con niebla (68-79) porque esa
  // distancia ya estaba pegada al limite de la camara (80) -- los props
  // laterales (offset en X, hasta ~17 unidades) tienen una distancia real a
  // camara mayor que los del centro por Pitagoras, asi que nacian FUERA del
  // rango de niebla (sin fundido) y ademas hacian todo su crecimiento de
  // escala en solo 8 unidades. En vez de rellenar todo de niebla otra vez
  // (el usuario pidio explicitamente lo contrario: "no quiero blur, quiero
  // vision mas larga"), se alarga el mundo entero: nace mas lejos (SPAWN_Z),
  // la camara ve mas lejos (camera.far en main.js) y el domo de cielo crece
  // a juego (si no, el cielo -esfera opaca- tapa la pista antes de llegar al
  // nuevo limite). La niebla queda como una franja corta y lejana, pegada al
  // limite real, para que la desaparicion en el horizonte no tenga un corte
  // duro -- no como fondo difuminado permanente.
  scene.fog = new THREE.Fog(0x9fe6ff, 130, 285);

  // ---- Cielo degradado (domo con vertex colors), anclado a la escena y no
  // al grupo que hace scroll, para que nunca se quede atras. Se recolorea
  // (instantaneo, no cada frame) al cruzar a un bioma distinto. Radio > que
  // camera.far (100) con margen para cubrir tambien los rayos diagonales
  // hacia las esquinas del frustum, si no el domo (esfera opaca) tapa la
  // pista lejana antes de llegar al limite real de dibujado. ----
  const skyGeo = new THREE.SphereGeometry(310, 24, 16);
  const skyPos = skyGeo.attributes.position;
  const skyColorAttr = new Float32Array(skyPos.count * 3);
  const tmpColor = new THREE.Color();
  function updateSkyColors(topHex, bottomHex) {
    const top = tmpColor.set(topHex).clone();
    const bottom = new THREE.Color(bottomHex);
    for (let i = 0; i < skyPos.count; i++) {
      // El tercio de abajo, del color de la niebla (asi lo lejano se funde
      // con el cielo en vez de recortarse); arriba, el azul del cielo.
      const t = THREE.MathUtils.smoothstep(skyPos.getY(i) / 310, 0.28, 0.8);
      tmpColor.copy(bottom).lerp(top, t);
      skyColorAttr[i * 3] = tmpColor.r; skyColorAttr[i * 3 + 1] = tmpColor.g; skyColorAttr[i * 3 + 2] = tmpColor.b;
    }
    skyGeo.attributes.color.needsUpdate = true;
  }
  skyGeo.setAttribute("color", new THREE.BufferAttribute(skyColorAttr, 3));
  updateSkyColors(0x3d8fff, 0xe0f5ff);
  const skyMat = new THREE.MeshBasicMaterial({ vertexColors: true, side: THREE.BackSide, fog: false });
  const sky = new THREE.Mesh(skyGeo, skyMat);
  scene.add(sky);

  let lastZoneName = "city";

  // Reloj propio para animaciones (bounce/pulso/oleo de banderas), independiente
  // de dz (que es distancia recorrida, no tiempo real).
  let animClock = 0;
  let lastTime = typeof performance !== "undefined" ? performance.now() : Date.now();

  // ---- Curvas organicas: dos ondas de distinta frecuencia combinadas (no
  // un solo seno perfectamente periodico) para que la pista serpentee de
  // forma menos mecanica/repetitiva. Todo el grupo se desplaza en X segun
  // la distancia recorrida; el personaje/camara en main.js reciben el mismo
  // offset (ver valor de retorno de update()), asi que el carril relativo
  // del jugador y las colisiones no cambian en nada. ----
  const CURVE_FREQ = (Math.PI * 2) / 130;
  // 23/10: a cero. La pista se balanceaba de lado sin parar (casi un carril
  // cada ~5 s y otro poco cada ~2): ese vaiven lento es lo que mas marea.
  const CURVE_AMPLITUDE = 0;
  const CURVE_FREQ2 = (Math.PI * 2) / 47;
  const CURVE_AMPLITUDE2 = 0;
  let totalScrolled = 0;
  let curveX = 0;

  // ---- Biomas: el anillo exterior de decoracion (mas alla de la
  // decoracion del mitin) cambia segun distancia recorrida, simulando pasar
  // por distintas zonas de una gira de campana por EEUU. ----
  const BIOME_LENGTH = 260;
  const BIOME_NAMES = ["city", "desert", "town"]; // rotacion automatica de una partida normal
  // "dc" no entra en la rotacion automatica -- solo se juega si se elige a
  // proposito desde el menu (ver setForcedZone).
  // Colores vivos tipo "caramelo": el suelo se multiplica con la textura de
  // asfalto (clara, ver makeAsphaltTexture), asi que estos tonos si que se
  // ven en pantalla en vez de quedar apagados.
  const BIOME_COLORS = {
    // `horizon` bastante mas oscuro/saturado que `sky`: antes eran casi el
    // mismo tono (0xaebfd6 contra 0x9fe6ff) y la cordillera del fondo, que
    // ademas va sin niebla, se fundia con el cielo -- se dibujaba pero no se
    // veia, y el fondo seguia leyendose como un vacio blanco.
    // 22/10 estilo Minion Rush; 23/10 rebajados porque mareaban: calzada gris
    // pizarra (no azul vivo), aceras beis suave y cesped menos chillon.
    city: { sky: 0x9fe6ff, skyTop: 0x3d8fff, ground: 0xd9cbb4, fog: 0x9fe6ff, road: 0x5c6170, horizon: 0x6d86ad, sidewalk: 0xe6dccb },
    // Pista de tierra bastante mas oscura que la arena de alrededor: antes
    // ambas compartian textura Y tono parecido, asi que el borde de la pista
    // desaparecia, no habia referencia de donde estabas y el conjunto se leia
    // como una superficie plana y transparente que marea.
    desert: { sky: 0xffe0ae, skyTop: 0xff9d4d, ground: 0xe9c47e, fog: 0xffe0ae, road: 0xb88456, horizon: 0xb0724a, sidewalk: 0xdcc09a },
    town: { sky: 0xbdeaff, skyTop: 0x5cabff, ground: 0x86c766, fog: 0xbdeaff, road: 0x5d6272, horizon: 0x7d9e86, sidewalk: 0xeee5d2 },
    dc: { sky: 0xbfe0ff, skyTop: 0x4a8fd6, ground: 0xe6dcc6, fog: 0xbfe0ff, road: 0x5a5f6d, horizon: 0x74879f, sidewalk: 0xf0e9dc },
  };

  // ---- Horizonte pintado y nubes altas (27/10/2026, ver horizonte.js) ----
  // Sustituye a la cordillera de conos grises y a los bloques sueltos del fondo.
  const horizonte = typeof document !== 'undefined' ? crearHorizonte(scene) : null;
  const SITIO_DE_ZONA = { city: 'manhattan', desert: 'desierto', town: 'pueblo', dc: 'dc' };
  function showMidLayer(zone) {
    if (!horizonte) return;
    const sitio = (nivel && nivel.horizonte) || SITIO_DE_ZONA[zone] || 'manhattan';
    horizonte.pintar(sitio, BIOME_COLORS[zone].sky, BIOME_COLORS[zone].fog);
  }

  // Zona forzada: si esta activa, toda la partida se queda en esa zona (sin
  // rotar) -- se usa para el selector de zona del menu. null = rotacion
  // automatica normal por ciudad/desierto/pueblo.
  let forcedZone = null;
  function setForcedZone(name) {
    forcedZone = name || null;
  }
  function currentZoneName(distance) {
    if (forcedZone) return forcedZone;
    return BIOME_NAMES[Math.floor(Math.max(0, distance) / BIOME_LENGTH) % BIOME_NAMES.length];
  }
  function biomeBlendAt(distance) {
    if (forcedZone) return { from: forcedZone, to: forcedZone, t: 0 };
    const raw = Math.max(0, distance) / BIOME_LENGTH;
    const idx = Math.floor(raw) % BIOME_NAMES.length;
    const nextIdx = (idx + 1) % BIOME_NAMES.length;
    const frac = raw - Math.floor(raw);
    const TRANSITION = 0.3;
    const t = frac > 1 - TRANSITION ? (frac - (1 - TRANSITION)) / TRANSITION : 0;
    return { from: BIOME_NAMES[idx], to: BIOME_NAMES[nextIdx], t };
  }
  const blendA = new THREE.Color(), blendB = new THREE.Color();

  // Suelo ancho tipo carretera/asfalto (cubre tambien la zona donde esta el
  // skyline mas alejado, para que no quede un hueco vacio entre la
  // decoracion y los edificios).
  const asphaltTex = makeAsphaltTexture();
  const dirtTex = makeDirtTexture();
  const pavingTex = makePavingTexture();
  const grassTex = makeGrassTexture();
  // Que textura lleva cada parte del suelo segun la zona.
  const texSuelo = (zona) => (zona === "desert" ? dirtTex : zona === "town" ? grassTex : pavingTex);
  const texCalzada = (zona) => (zona === "desert" ? dirtTex : asphaltTex);
  const groundMat = toon(BIOME_COLORS.city.ground, pavingTex ? { map: pavingTex, shininess: 8 } : null);
  const ground = new THREE.Mesh(new THREE.PlaneGeometry(60, 400), groundMat);
  ground.rotation.x = -Math.PI / 2;
  ground.position.z = -150;
  ground.receiveShadow = true;
  group.add(ground);

  // Lineas amarillas discontinuas de carretera, a ambos lados de la
  // alfombra roja, sobre el asfalto (pool reciclado igual que las franjas).
  const roadLines = [];
  const roadLineMat = toon(GOLD);
  // 23/10: tramos de 3 seguidos (la misma separacion con que se ponen):
  // linea continua. Discontinua, a 25 u/s, parpadeaba unas 8 veces por
  // segundo y era una de las cosas que mareaban.
  const roadLineGeo = new THREE.BoxGeometry(0.15, 0.02, 3.02);
  const TRAMOS_RAYA = Math.ceil(Math.abs(SPAWN_Z) / 3) * 3;
  function spawnRoadLine(z) {
    for (const x of [-9, 9]) {
      const m = new THREE.Mesh(roadLineGeo, roadLineMat);
      m.position.set(x, 0.06, z);
      group.add(m);
      roadLines.push(m);
    }
  }
  // (27/10: sin estas lineas amarillas: quedaban pintadas sobre el suelo, mas alla de la acera.)

  // Acera de hormigon a ambos lados, entre la calzada y donde estan los
  // props (antes el suelo era una sola superficie sin ninguna referencia).
  const concreteTex = makeSidewalkTexture() || makeConcreteTexture();
  const sidewalkMat = toon(BIOME_COLORS.city.sidewalk, concreteTex ? { map: concreteTex, shininess: 12 } : null);
  const texturasSuelo = [asphaltTex, dirtTex, pavingTex, grassTex, concreteTex];
  sidewalkMat.polygonOffset = true;
  sidewalkMat.polygonOffsetFactor = -1;
  sidewalkMat.polygonOffsetUnits = -2;
  const curbMat = toon(0xfff6e0);
  for (const side of [-1, 1]) {
    const sidewalk = new THREE.Mesh(new THREE.PlaneGeometry(4.2, 400), sidewalkMat);
    sidewalk.rotation.x = -Math.PI / 2;
    sidewalk.position.set(side * 6, 0.025, -150);
    sidewalk.receiveShadow = true;
    group.add(sidewalk);
    // Bordillo mas gordo y alto: en los dibujos los bordes se marcan mucho.
    const curb = new THREE.Mesh(new THREE.BoxGeometry(0.22, 0.12, 400), curbMat);
    curb.position.set(side * 3.95, 0.06, -150);
    group.add(curb);
  }

  // Antes siempre roja (alfombra de mitin) en las 4 zonas. Ahora asfalto/
  // tierra realista a juego con la zona, igual que el suelo lateral -- las
  // rayas blancas/amarillas ya existentes quedan como marcas de carril de
  // verdad en vez de sobre un fondo rojo sin sentido real.
  // polygonOffset: las capas de suelo (suelo base / calzada / acera / rayas)
  // son casi coplanares y con camera.far=100 (ronda 15) la precision del
  // buffer de profundidad a distancia ya no basta para separarlas por Y sola
  // -- parpadeaban entre si (z-fighting), que en pantalla se ve como si el
  // suelo fuera medio transparente y marea. El offset las ordena en el
  // rasterizador sin depender de la distancia.
  const carpetMat = toon(BIOME_COLORS.city.road, asphaltTex ? { map: asphaltTex, shininess: 20 } : null);
  carpetMat.polygonOffset = true;
  carpetMat.polygonOffsetFactor = -2;
  carpetMat.polygonOffsetUnits = -4;
  const carpet = new THREE.Mesh(new THREE.PlaneGeometry(LANE_WIDTH * 3, 400), carpetMat);
  carpet.rotation.x = -Math.PI / 2;
  carpet.position.y = 0.04;
  carpet.position.z = -150;
  carpet.receiveShadow = true;
  group.add(carpet);

  // ---- Ribetes dorados a los bordes de la alfombra ----
  // Se guardan para poder ocultarlos en el desierto: son decoracion de mitin
  // (alfombra roja), no tienen sentido sobre una pista de tierra, y eran la
  // "linea" que seguia viendose ahi aunque ya se ocultaran las rayas de
  // carril y las lineas de autopista.
  const goldMat = toon(GOLD);
  const goldTrims = [];
  for (const side of [-1, 1]) {
    const trim = new THREE.Mesh(new THREE.BoxGeometry(0.12, 0.03, 400), goldMat);
    trim.position.set(side * (LANE_WIDTH * 1.5 + 0.06), 0.07, -150);
    group.add(trim);
    goldTrims.push(trim);
  }

  // Arcenes de tierra removida: sustituyen a los ribetes dorados en el
  // desierto para que la pista siga teniendo un borde legible. Sin ningun
  // borde, la pista y la arena se funden y se pierde la nocion de carril.
  const dirtBerms = [];
  for (const side of [-1, 1]) {
    const berm = new THREE.Mesh(new THREE.BoxGeometry(0.5, 0.05, 400), toon(0x7d5433));
    berm.position.set(side * (LANE_WIDTH * 1.5 + 0.22), 0.05, -150);
    berm.visible = false;
    group.add(berm);
    dirtBerms.push(berm);
  }

  // ---- Banderines (bunting) colgando sobre los bordes (pool reciclado) ----
  const bunting = [];
  const buntingColors = [0xff2d2d, 0xffffff, 0x2f6bff, GOLD];
  const buntingMats = buntingColors.map((c) => toon(c));
  const buntingGeo = new THREE.ConeGeometry(0.09, 0.2, 3);
  function spawnBunting(z) {
    for (const side of [-1, 1]) {
      for (let i = 0; i < 3; i++) {
        const mat = buntingMats[Math.floor(Math.random() * buntingMats.length)];
        const pennant = new THREE.Mesh(buntingGeo, mat);
        pennant.rotation.x = Math.PI;
        pennant.position.set(side * (LANE_WIDTH * 1.5 + 0.1), 2.05 - Math.abs(i - 1) * 0.06, z + i * 0.4);
        pennant.userData.phase = Math.random() * Math.PI * 2;
        group.add(pennant);
        bunting.push(pennant);
      }
    }
  }
  // (27/10: sin banderines: flotaban sueltos, sin cuerda.)

  // ---- Franjas divisorias de carril (pool reciclado) ----
  const stripes = [];
  // Rayas de carril continuas y de un blanco suave (23/10): las amarillas
  // discontinuas pasaban a 10 por segundo como una luz estroboscopica.
  const stripeGeo = new THREE.BoxGeometry(0.1, 0.02, 3.02);
  const stripeMat = toon(0xeae6dc);
  // 27/10: dos rayas largas en vez de ~190 trocitos de 3 (eran casi 200
  // llamadas de dibujo). Como son continuas, no hace falta moverlas: solo se
  // recortan donde acaba la calle del nivel.
  const rayaGeo = new THREE.BoxGeometry(0.1, 0.02, 1);
  rayaGeo.translate(0, 0, -0.5);            // de z = 0 hacia -z
  for (const laneEdge of [-LANE_WIDTH / 2, LANE_WIDTH / 2]) {
    const m = new THREE.Mesh(rayaGeo, stripeMat);
    m.position.set(laneEdge, 0.07, 8);
    m.scale.z = 8 - SPAWN_Z;
    group.add(m);
    stripes.push(m);
  }

  // ---- Banderas + publico decorativo (pool reciclado) ----
  const decor = [];
  const banderaMat = toon(0xffffff, { side: THREE.DoubleSide, shininess: 10, map: texturaBandera() });
  const banderaGeo = new THREE.PlaneGeometry(0.95, 0.58);
  function makeFlagPole() {
    const g = new THREE.Group();
    const pole = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.04, 3, 6), toon(0xd8dde3));
    pole.position.y = 1.5;
    g.add(pole);
    // 27/10: la bandera de EE. UU. (antes un rectangulo azul liso que parecia un cartel en blanco).
    const flag = new THREE.Mesh(banderaGeo, banderaMat);
    flag.position.set(0.47, 2.62, 0);
    g.add(flag);
    g.userData.kind = "flag";
    g.userData.flagMesh = flag;
    g.userData.phase = Math.random() * Math.PI * 2;
    return g;
  }

  const SHIRT_COLORS = [0xff2d2d, 0xffffff, 0x2f6bff, GOLD];
  const shirtMats = SHIRT_COLORS.map((c) => toon(c));
  const PANTS_COLORS = [0x2b2b33, 0x35415c, 0x4a4038, 0x24303a];
  const pantsMats = PANTS_COLORS.map((c) => toon(c));
  const HAIR_COLORS = [0x2b1e14, 0x4a3222, 0x161616, 0xd9b063, 0x6b4a2f];
  const hairMats = HAIR_COLORS.map((c) => toon(c));
  const personSkinMat = toon(0xffc999);
  const shoeMat = toon(0x2a2018);
  // Antes era 4 cajas planas (cuerpo/piernas en bloque, sin brazos). Torso
  // en capsula (menos "ladrillo"), brazos y zapatos propios, y pelo -- sigue
  // siendo barato en poligonos (son figuras de fondo vistas de lejos) pero
  // ya no se lee como un maniqui de caja.
  // ---- Publico estilo Pixar (25/10/2026, blender/publico.py) ----
  // Seis personas con cara y el brazo derecho aparte: saludan, botan y se
  // animan mas cuando pasa el jugador. Si no han cargado, el muñeco viejo.
  const PERSONAS = ["ejecutivo", "senora", "chico", "abuelo", "turista", "fan"];
  const HOMBROS = { ejecutivo: [0.272, 1.368], senora: [0.23, 1.277], chico: [0.158, 0.874],
    abuelo: [0.262, 1.262], turista: [0.239, 1.322], fan: [0.233, 1.292] };
  const PUBLICO_PIXAR = PERSONAS.every((n) => hayModelo(`publico/${n}_cuerpo`) && hayModelo(`publico/${n}_brazo`));
  function personaPixar(lista) {
    const vale = (lista || PERSONAS).filter((x) => PERSONAS.includes(x));
    const n = vale.length ? vale[Math.floor(Math.random() * vale.length)] : PERSONAS[Math.floor(Math.random() * PERSONAS.length)];
    const g = new THREE.Group();
    const c = medidas(`publico/${n}_cuerpo`), b = medidas(`publico/${n}_brazo`);
    g.add(new THREE.Mesh(c.geometry, c.material));
    const hombro = new THREE.Group();
    hombro.position.set(HOMBROS[n][0], HOMBROS[n][1], 0);
    hombro.add(new THREE.Mesh(b.geometry, b.material));
    g.add(hombro);
    g.userData.kind = "person";
    g.userData.brazo = hombro;
    g.userData.phase = Math.random() * Math.PI * 2;
    g.userData.ritmo = 0.8 + Math.random() * 0.5;
    return g;
  }
  function makePerson(lista) {
    if (PUBLICO_PIXAR) return personaPixar(lista);
    const g = new THREE.Group();
    const shirtMat = shirtMats[Math.floor(Math.random() * shirtMats.length)];
    const pantsMat = pantsMats[Math.floor(Math.random() * pantsMats.length)];
    // Complexion y estatura variables: antes todos eran clones exactos del
    // mismo muñeco, y una multitud de copias identicas se lee como una caja
    // de piezas de juguete por mucho que cambie el color de la camiseta.
    const build = 0.86 + Math.random() * 0.32;   // ancho de torso
    const tall = 0.9 + Math.random() * 0.22;     // estatura

    const body = new THREE.Mesh(new THREE.CapsuleGeometry(0.15 * build, 0.22 * tall, 4, 8), shirtMat);
    body.position.y = 0.56 * tall;
    g.add(body);
    // Hombros redondeados que unen brazos y torso (antes los brazos salian
    // de la nada por los costados, la union tipica de figura de juguete).
    for (const side of [-1, 1]) {
      const shoulder = new THREE.Mesh(new THREE.SphereGeometry(0.07 * build, 8, 6), shirtMat);
      shoulder.position.set(side * 0.15 * build, 0.68 * tall, 0);
      g.add(shoulder);
      const arm = new THREE.Mesh(new THREE.CapsuleGeometry(0.045, 0.3 * tall, 4, 6), personSkinMat);
      arm.position.set(side * (0.17 * build + 0.04), 0.52 * tall, 0);
      arm.rotation.z = side * (0.1 + Math.random() * 0.25);
      g.add(arm);
    }
    // Piernas separadas en vez de un bloque unico.
    for (const side of [-1, 1]) {
      const leg = new THREE.Mesh(new THREE.CapsuleGeometry(0.058, 0.26 * tall, 4, 6), pantsMat);
      leg.position.set(side * 0.075, 0.22 * tall, 0);
      g.add(leg);
      const shoe = new THREE.Mesh(new THREE.BoxGeometry(0.11, 0.065, 0.22), shoeMat);
      shoe.position.set(side * 0.075, 0.033, 0.03);
      g.add(shoe);
    }
    const head = new THREE.Mesh(new THREE.SphereGeometry(0.15, 8, 6), personSkinMat);
    head.scale.set(1, 1.08, 0.95);
    head.position.y = 0.92 * tall;
    g.add(head);
    const hairMat2 = hairMats[Math.floor(Math.random() * hairMats.length)];
    const hair = new THREE.Mesh(new THREE.SphereGeometry(0.16, 8, 6, 0, Math.PI * 2, 0, Math.PI * 0.55), hairMat2);
    hair.position.y = 0.97 * tall;
    g.add(hair);
    // Una parte del publico lleva gorra: rompe la fila de cabezas iguales.
    if (Math.random() < 0.35) {
      const capMat = shirtMats[Math.floor(Math.random() * shirtMats.length)];
      const cap = new THREE.Mesh(new THREE.SphereGeometry(0.163, 10, 6, 0, Math.PI * 2, 0, Math.PI * 0.5), capMat);
      cap.position.y = 0.985 * tall;
      g.add(cap);
      const visor = new THREE.Mesh(new THREE.BoxGeometry(0.2, 0.022, 0.13), capMat);
      visor.position.set(0, 0.985 * tall, 0.14);
      g.add(visor);
    }
    const signUp = Math.random() < 0.5;
    const sign = new THREE.Mesh(new THREE.PlaneGeometry(0.36, 0.24), toon(0xffffff, { side: THREE.DoubleSide }));
    sign.position.set(0.25, signUp ? 1.25 : 0.6, 0);
    sign.rotation.z = 0.3;
    g.add(sign);
    g.userData.kind = "person";
    g.userData.phase = Math.random() * Math.PI * 2;
    return g;
  }

  function makeCloud() {
    const g = new THREE.Group();
    const cloudMat = toon(0xffffff);
    for (let i = 0; i < 3; i++) {
      const puff = new THREE.Mesh(new THREE.SphereGeometry(0.7 + Math.random() * 0.4, 7, 6), cloudMat);
      puff.position.set(i * 0.8 - 0.8, Math.random() * 0.3, Math.random() * 0.4);
      g.add(puff);
    }
    g.userData.kind = "cloud";
    return g;
  }

  // ---- Graderio con publico sentado (prop extra para variedad lateral) ----
  function makeBleacher() {
    const g = new THREE.Group();
    const stepMat = toon(0xd6dce6);
    for (let i = 0; i < 3; i++) {
      const step = new THREE.Mesh(new THREE.BoxGeometry(1.7 - i * 0.1, 0.35, 1.0 - i * 0.28), stepMat);
      step.position.set(0, 0.2 + i * 0.35, -i * 0.32);
      withOutline(step, 1.04);
      g.add(step);
    }
    for (let i = 0; i < 4; i++) {
      const p = makePerson();
      p.scale.setScalar(0.75);
      p.position.set(-0.6 + i * 0.4, 0.42 + Math.floor(i / 2) * 0.35, -Math.floor(i / 2) * 0.32);
      g.add(p);
    }
    g.userData.kind = "bleacher";
    return g;
  }

  function spawnDecorCluster(z, i, conf) {
    // Grupos alternos: unos con publico (detras de su valla) y otros con un
    // par de banderas; asi la acera no es la misma fila repetida.
    const conPublico = conf.personas && i % (conf.cada || 2) === 0;
    for (const side of [-1, 1]) {
      if (!conPublico) {
        if (conf.banderas === false) continue;
        const f = makeFlagPole();
        f.position.set(side * 4.45, 0, z - Math.random() * 3);
        f.rotation.y = side > 0 ? Math.PI : 0;
        group.add(f); decor.push(f);
        continue;
      }
      if (conf.valla && hayModelo("publico/" + conf.valla)) {
        const v = modelo("publico/" + conf.valla);
        v.position.set(side * 4.35, 0, z - 1);
        v.rotation.y = side < 0 ? Math.PI / 2 : -Math.PI / 2;
        v.userData.kind = "valla";
        group.add(v); decor.push(v);
      }
      const n = 2 + Math.floor(Math.random() * 2);
      for (let k = 0; k < n; k++) {
        const p = makePerson(conf.personas);
        p.position.set(side * (4.95 + Math.random() * 0.5 + (k % 2) * 0.55), 0, z - k * 0.95 + (Math.random() - 0.5) * 0.3);
        p.rotation.y = side < 0 ? 0.35 + Math.random() * 0.3 : -0.35 - Math.random() * 0.3;
        group.add(p); decor.push(p);
      }
    }
  }
  // Publico y banderas segun el sitio: el de cada nivel, o el de su zona en el sin fin.
  const PUBLICO_ZONA = {
    city: { personas: PERSONAS, valla: "valla_policia", cada: 2 },
    town: { personas: ["abuelo", "senora", "chico", "fan"], cada: 3 },
    dc: { personas: ["ejecutivo", "fan", "turista", "senora"], valla: "verja", cada: 2 },
    desert: { personas: null, banderas: false },
  };
  const VALLAS = { policia: "valla_policia", verja: "verja", banderas: null };
  let decorDe = null;
  function montarDecor() {
    const conf = nivel && nivel.publico
      ? { ...nivel.publico, valla: VALLAS[nivel.publico.valla] }
      : PUBLICO_ZONA[currentZoneName(0)] || PUBLICO_ZONA.city;
    const clave = JSON.stringify(conf);
    if (clave === decorDe) return;
    decorDe = clave;
    for (const d of decor) group.remove(d);
    decor.length = 0;
    let i = 0;
    for (let z = -5; z > SPAWN_Z; z -= 11) spawnDecorCluster(z, i++, conf);
  }

  // ---- Props del anillo exterior, por bioma ----

  // -- Ciudad: edificios + mobiliario urbano real (no solo cajas) --
  const buildingMats = [toon(0xb47fe0), toon(0xff9d5c), toon(0x5cc9d6), toon(0xffd966)];
  const windowMat = toon(0xfff3c4);
  const windowGeo = new THREE.PlaneGeometry(1, 0.5);
  function makeBuilding() {
    const h = 4 + Math.random() * 8;
    // Fondo (X) menor que el ancho (Z): el edificio es mas ancho A LO LARGO
    // de la calle que hacia dentro de la manzana, como en una calle real.
    // Antes ambos eran ~iguales (casi un cubo), asi que la cara que veias de
    // frente era la lisa sin ventanas y la fachada con ventanas quedaba de
    // canto -- de ahi la sensacion de que miraban a la camara y no a la calle.
    const w = 1.8 + Math.random() * 1.0;
    const d = 3.4 + Math.random() * 2.2;
    const mat = buildingMats[Math.floor(Math.random() * buildingMats.length)];
    const g = new THREE.Group();
    const body = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), mat);
    body.position.y = h / 2;
    g.add(body);
    // Ventanas solo en la cara que mira hacia la pista (cara -X local; la
    // rotacion al spawnear la orienta hacia el jugador segun el lado).
    // Rejilla de ventanas (varias columnas por planta) en vez de una sola
    // ventana ancha: con la fachada ya orientada a la calle, una retícula se
    // lee como un edificio de verdad. Algunas apagadas al azar para que no
    // sean todas idénticas.
    const rows = Math.max(2, Math.floor(h / 1.4));
    const cols = Math.max(2, Math.round(d / 1.5));
    for (let r = 0; r < rows; r++) {
      for (let c = 0; c < cols; c++) {
        if (Math.random() < 0.22) continue; // ventana apagada
        const win = new THREE.Mesh(windowGeo, windowMat);
        win.scale.set((d / cols) * 0.52, 0.34, 1);
        win.position.set(-w / 2 - 0.01, 0.9 + r * 1.4, -d / 2 + (c + 0.5) * (d / cols));
        win.rotation.y = -Math.PI / 2;
        g.add(win);
      }
    }
    // Cornisa en el borde del techo + puerta a pie de calle (antes el
    // edificio era una caja lisa con ventanas y nada mas: sin remate arriba
    // ni entrada marcada abajo).
    const trim = new THREE.Mesh(new THREE.BoxGeometry(w + 0.12, 0.1, d + 0.12), toon(0x2a2a2e));
    trim.position.y = h - 0.05;
    g.add(trim);

    // Variantes de silueta: antes TODOS los edificios eran la misma caja con
    // ventanas y solo cambiaba el color, asi que la calle se volvia repetitiva
    // en cuanto veias tres. Ahora hay cuatro remates distintos.
    const style = Math.random();
    if (style < 0.28) {
      // Cuerpo retranqueado (escalonado) tipo art deco
      const setback = new THREE.Mesh(new THREE.BoxGeometry(w * 0.7, h * 0.28, d * 0.7), mat);
      setback.position.y = h + h * 0.14;
      g.add(setback);
      const crown = new THREE.Mesh(new THREE.BoxGeometry(w * 0.72 + 0.1, 0.09, d * 0.72 + 0.1), toon(0x2a2a2e));
      crown.position.y = h + h * 0.28;
      g.add(crown);
    } else if (style < 0.46) {
      // Antena/aguja de comunicaciones
      const mast = new THREE.Mesh(new THREE.CylinderGeometry(0.035, 0.06, 1.5, 6), toon(0x8a8f96));
      mast.position.y = h + 0.75;
      g.add(mast);
      const beacon = new THREE.Mesh(new THREE.SphereGeometry(0.075, 8, 6), new THREE.MeshBasicMaterial({ color: 0xff3b3b }));
      beacon.position.y = h + 1.5;
      g.add(beacon);
    } else if (style < 0.62) {
      // Cubierta a dos aguas (edificio bajo tipo almacen/nave)
      const roofMat = toon(0x7a4a3a);
      const rise = 0.5;
      for (const side of [-1, 1]) {
        const half = Math.hypot(w / 2, rise);
        const panel = new THREE.Mesh(new THREE.BoxGeometry(half, 0.07, d + 0.1), roofMat);
        panel.position.set(side * w / 4, h + rise / 2, 0);
        panel.rotation.z = -side * Math.atan2(rise, w / 2);
        g.add(panel);
      }
    }
    // Toldo sobre la puerta en algunos: detalle de planta baja comercial.
    if (Math.random() < 0.4) {
      const awning = new THREE.Mesh(new THREE.BoxGeometry(0.06, 0.28, 0.95), toon(0xd8322f));
      awning.position.set(-w / 2 - 0.12, 1.05, 0);
      awning.rotation.z = 0.5;
      g.add(awning);
    }
    const door = new THREE.Mesh(new THREE.PlaneGeometry(0.5, 0.9), toon(0x1a1a1a));
    door.position.set(-w / 2 - 0.01, 0.45, 0);
    door.rotation.y = -Math.PI / 2;
    g.add(door);
    if (Math.random() < 0.5) {
      // Unidades de aire acondicionado sueltas en el techo, al azar.
      const acCount = 1 + Math.floor(Math.random() * 2);
      for (let i = 0; i < acCount; i++) {
        const ac = new THREE.Mesh(new THREE.BoxGeometry(0.3, 0.18, 0.3), toon(0x8a8f96));
        ac.position.set((Math.random() - 0.5) * (w - 0.5), h + 0.09, (Math.random() - 0.5) * (d - 0.5));
        g.add(ac);
      }
    }
    if (Math.random() < 0.25) {
      // torre de agua, toque clasico de ciudad estadounidense
      const tankBody = new THREE.Mesh(new THREE.CylinderGeometry(0.32, 0.32, 0.4, 8), toon(0x9aa2ad));
      tankBody.position.y = h + 0.5;
      g.add(tankBody);
      for (const lx of [-0.2, 0.2]) for (const lz of [-0.2, 0.2]) {
        const leg = new THREE.Mesh(new THREE.CylinderGeometry(0.02, 0.02, 0.5, 4), toon(0x6b6b6b));
        leg.position.set(lx, h + 0.25, lz);
        g.add(leg);
      }
    }
    return g;
  }
  function makeStreetLamp() {
    const g = new THREE.Group();
    const poleMat = toon(0x2a2a2e);
    const base = new THREE.Mesh(new THREE.CylinderGeometry(0.09, 0.11, 0.1, 8), poleMat);
    base.position.y = 0.05;
    g.add(base);
    const pole = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.05, 2.55, 8), poleMat);
    pole.position.y = 1.3;
    g.add(pole);
    // Brazo redondo en diagonal (antes una caja recta horizontal).
    const arm = new THREE.Mesh(new THREE.CylinderGeometry(0.025, 0.03, 0.42, 8), poleMat);
    arm.rotation.z = Math.PI / 2.3;
    arm.position.set(0.19, 2.58, 0);
    g.add(arm);
    const lamp = new THREE.Mesh(new THREE.SphereGeometry(0.09, 8, 8), new THREE.MeshBasicMaterial({ color: 0xfff3c4 }));
    lamp.position.set(0.38, 2.5, 0);
    g.add(lamp);
    const cap = new THREE.Mesh(new THREE.ConeGeometry(0.1, 0.09, 8), poleMat);
    cap.position.set(0.38, 2.58, 0);
    g.add(cap);
    return g;
  }
  const CAR_COLORS = [0xd8322f, 0x2a5cc9, 0xf4f4f4, 0x2a2a2e, 0xf4c430];
  function makeParkedCar() {
    const g = new THREE.Group();
    const bodyMat = toon(CAR_COLORS[Math.floor(Math.random() * CAR_COLORS.length)]);
    const body = new THREE.Mesh(new THREE.BoxGeometry(1.7, 0.4, 0.75), bodyMat);
    body.position.y = 0.35;
    withOutline(body, 1.05);
    g.add(body);
    const cabin = new THREE.Mesh(new THREE.BoxGeometry(0.9, 0.32, 0.68), bodyMat);
    cabin.position.set(-0.1, 0.68, 0);
    withOutline(cabin, 1.05);
    g.add(cabin);
    const wheelMat = toon(0x1a1a1a);
    for (const wx of [-0.55, 0.55]) for (const wz of [-0.34, 0.34]) {
      const wheel = new THREE.Mesh(new THREE.CylinderGeometry(0.16, 0.16, 0.12, 10), wheelMat);
      wheel.rotation.z = Math.PI / 2;
      wheel.position.set(wx, 0.17, wz);
      g.add(wheel);
    }
    // Espejos + luces (antes solo carroceria + cabina + ruedas, sin ningun detalle pequeno).
    const mirrorMat = toon(0x1a1a1a);
    for (const wz of [-0.4, 0.4]) {
      const mirror = new THREE.Mesh(new THREE.BoxGeometry(0.06, 0.06, 0.1), mirrorMat);
      mirror.position.set(0.32, 0.62, wz);
      g.add(mirror);
    }
    const headlightMat = new THREE.MeshBasicMaterial({ color: 0xfff6d8 });
    const taillightMat = new THREE.MeshBasicMaterial({ color: 0xb5241f });
    for (const wz of [-0.28, 0.28]) {
      const headlight = new THREE.Mesh(new THREE.BoxGeometry(0.04, 0.1, 0.16), headlightMat);
      headlight.position.set(0.85, 0.36, wz);
      g.add(headlight);
      const taillight = new THREE.Mesh(new THREE.BoxGeometry(0.04, 0.1, 0.14), taillightMat);
      taillight.position.set(-0.85, 0.36, wz);
      g.add(taillight);
    }
    return g;
  }
  function makeStreetTree() {
    const g = new THREE.Group();
    const trunk = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.1, 1.1, 8), toon(0x6b4a2f));
    trunk.position.y = 0.55;
    g.add(trunk);
    const foliageMat = toon(0x4caf50);
    for (let i = 0; i < 3; i++) {
      const puff = new THREE.Mesh(new THREE.SphereGeometry(0.45 - i * 0.06, 10, 8), foliageMat);
      puff.position.set((Math.random() - 0.5) * 0.2, 1.3 + i * 0.3, (Math.random() - 0.5) * 0.2);
      g.add(puff);
    }
    return g;
  }
  // Antes el asiento era un solo bloque plano. Listones separados + patas y
  // reposabrazos redondeados (cilindros, no cajas) para que se lea como un
  // banco de parque real y no como un ladrillo con un respaldo pegado.
  function makeBench() {
    const g = new THREE.Group();
    const seatMat = toon(0x8a6a3f);
    const legMat = toon(0x2a2a2e);
    for (let i = 0; i < 3; i++) {
      const slat = new THREE.Mesh(new THREE.BoxGeometry(0.9, 0.04, 0.085), seatMat);
      slat.position.set(0, 0.4, -0.1 + i * 0.1);
      g.add(slat);
    }
    const back = new THREE.Mesh(new THREE.BoxGeometry(0.9, 0.35, 0.05), seatMat);
    back.position.set(0, 0.6, -0.13);
    g.add(back);
    for (const lx of [-0.38, 0.38]) {
      const leg = new THREE.Mesh(new THREE.CylinderGeometry(0.035, 0.035, 0.4, 6), legMat);
      leg.position.set(lx, 0.2, 0);
      g.add(leg);
      const arm = new THREE.Mesh(new THREE.CylinderGeometry(0.03, 0.03, 0.28, 6), legMat);
      arm.rotation.x = Math.PI / 2;
      arm.position.set(lx, 0.5, -0.02);
      g.add(arm);
    }
    return g;
  }
  function makeFireHydrant() {
    const g = new THREE.Group();
    const mat = toon(0xd8322f);
    const body = new THREE.Mesh(new THREE.CylinderGeometry(0.09, 0.1, 0.32, 8), mat);
    body.position.y = 0.2;
    g.add(body);
    const cap = new THREE.Mesh(new THREE.SphereGeometry(0.1, 8, 6), mat);
    cap.position.y = 0.38;
    g.add(cap);
    // Bocas laterales, el detalle real de un hidrante (antes solo cuerpo + tapa, sin salientes).
    const nozzleMat = toon(0xb5241f);
    for (const side of [-1, 1]) {
      const nozzle = new THREE.Mesh(new THREE.CylinderGeometry(0.03, 0.03, 0.08, 6), nozzleMat);
      nozzle.rotation.z = Math.PI / 2;
      nozzle.position.set(side * 0.1, 0.24, 0);
      g.add(nozzle);
    }
    return g;
  }
  function makeTrafficLight() {
    const g = new THREE.Group();
    const poleMat = toon(0x2a2a2e);
    const pole = new THREE.Mesh(new THREE.CylinderGeometry(0.035, 0.035, 2.4, 8), poleMat);
    pole.position.y = 1.2;
    g.add(pole);
    // Union visible entre el poste y la caja (antes la caja flotaba pegada sin soporte).
    const bracket = new THREE.Mesh(new THREE.BoxGeometry(0.06, 0.06, 0.1), poleMat);
    bracket.position.set(0, 2.12, 0.04);
    g.add(bracket);
    const box = new THREE.Mesh(new THREE.BoxGeometry(0.16, 0.4, 0.16), toon(0x1a1a1a));
    box.position.y = 2.3;
    g.add(box);
    const hoodMat = toon(0x161616);
    [0xff3b3b, 0xffce3d, 0x4caf50].forEach((c, i) => {
      const y = 2.45 - i * 0.12;
      const dot = new THREE.Mesh(new THREE.SphereGeometry(0.045, 8, 8), new THREE.MeshBasicMaterial({ color: c }));
      dot.position.set(0, y, 0.09);
      g.add(dot);
      // Visera sobre cada luz, como en los semaforos reales (antes las 3 bolas
      // quedaban peladas sobre la caja negra).
      const hood = new THREE.Mesh(new THREE.BoxGeometry(0.1, 0.02, 0.06), hoodMat);
      hood.position.set(0, y + 0.05, 0.12);
      hood.rotation.x = -0.3;
      g.add(hood);
    });
    return g;
  }

  // -- Desierto --
  function makeCactus() {
    const g = new THREE.Group();
    const mat = toon(0x3f7a4a);
    const h = 1.4 + Math.random() * 1.2;
    const trunk = new THREE.Mesh(new THREE.CylinderGeometry(0.18, 0.22, h, 10), mat);
    trunk.position.y = h / 2;
    withOutline(trunk, 1.05);
    g.add(trunk);
    for (const side of [-1, 1]) {
      if (Math.random() < 0.75) {
        const arm = new THREE.Mesh(new THREE.CylinderGeometry(0.09, 0.11, 0.55, 8), mat);
        arm.position.set(side * 0.22, h * 0.55, 0);
        arm.rotation.z = side * 0.9;
        g.add(arm);
        const armUp = new THREE.Mesh(new THREE.CylinderGeometry(0.09, 0.09, 0.4, 8), mat);
        armUp.position.set(side * 0.4, h * 0.55 + 0.35, 0);
        g.add(armUp);
      }
    }
    return g;
  }
  function makeTumbleweed() {
    const g = new THREE.Group();
    const mat = toon(0x8a6a3f);
    for (let i = 0; i < 5; i++) {
      const ring = new THREE.Mesh(new THREE.TorusGeometry(0.22, 0.02, 4, 8), mat);
      ring.rotation.set(Math.random() * Math.PI, Math.random() * Math.PI, Math.random() * Math.PI);
      g.add(ring);
    }
    g.userData.kind = "tumbleweed";
    g.userData.spinSpeed = 2 + Math.random() * 3;
    return g;
  }
  // Antes 3 cajas apiladas perfectamente alineadas (se notaba mucho el
  // "bloque"). Ahora cada capa tiene su propio tono de estrato, ancho/fondo
  // irregular y una leve rotacion (erosion), mas rocas sueltas en la base.
  const MESA_STRATA = [0xa8582f, 0x9a4f2a, 0xb56a3a, 0x8f4826];
  function makeMesa() {
    const g = new THREE.Group();
    for (let i = 0; i < 3; i++) {
      const w = 4 - i * 1.1 + (Math.random() - 0.5) * 0.4;
      const h = 1.2;
      const depth = w * (0.7 + Math.random() * 0.2);
      const layer = new THREE.Mesh(new THREE.BoxGeometry(w, h, depth), toon(MESA_STRATA[i % MESA_STRATA.length]));
      layer.position.y = i * h + h / 2;
      layer.rotation.y = (Math.random() - 0.5) * 0.3;
      g.add(layer);
    }
    const rockMat = toon(0x8f4826);
    for (let i = 0; i < 4; i++) {
      const r = 0.12 + Math.random() * 0.14;
      const rock = new THREE.Mesh(new THREE.DodecahedronGeometry(r, 0), rockMat);
      const ang = Math.random() * Math.PI * 2;
      const dist = 1.6 + Math.random() * 0.8;
      rock.position.set(Math.cos(ang) * dist, r * 0.6, Math.sin(ang) * dist);
      rock.rotation.set(Math.random() * Math.PI, Math.random() * Math.PI, Math.random() * Math.PI);
      g.add(rock);
    }
    return g;
  }
  function makeDeadTree() {
    const g = new THREE.Group();
    const mat = toon(0x4a3826);
    const trunk = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.09, 1.3, 6), mat);
    trunk.position.y = 0.65;
    g.add(trunk);
    for (let i = 0; i < 3; i++) {
      const branch = new THREE.Mesh(new THREE.CylinderGeometry(0.02, 0.03, 0.5, 5), mat);
      branch.position.set((Math.random() - 0.5) * 0.3, 1.1 + i * 0.15, 0);
      branch.rotation.z = (Math.random() - 0.5) * 1.4;
      g.add(branch);
    }
    return g;
  }

  // -- Pueblo: casas con cesped y valla propios. Mezcla de estilo victoriano
  // claro y estilo "suburbio moderno" (tablilla oscura + remates blancos,
  // como en fotos reales de barrios residenciales de EEUU) para variedad.
  const HOUSE_COLORS = [0xf5efe0, 0xe8ddc8, 0xf0e6e6, 0xe6ece8, 0x2a3648, 0x2e2e38, 0x3a4550, 0x33404a];
  const ROOF_COLORS = [0x9a3f33, 0x6b4a2f, 0x3a4a5c, 0x6b3f52];
  const TRIM_COLORS = [0x7a2020, 0x2e5a3a, 0x1f3a5c, 0x5a3a6b];
  const clapboardTex = makeClapboardTexture();
  const shingleTex = makeShingleTexture();
  const lawnMat = toon(0x6fc24a);
  const lawnGeo = new THREE.PlaneGeometry(3.6, 3.2);

  function makeHouse() {
    // Casa estilo victoriano detallada: tablillas en las paredes, tejado
    // con tejas, buhardilla, ventana circular decorativa, chimenea, porche
    // con techo y postes, ventanas con marco+contraventanas -- y su propio
    // cesped con valla blanca de estacas delante, como un jardin real.
    const g = new THREE.Group();
    const wallMat = toon(HOUSE_COLORS[Math.floor(Math.random() * HOUSE_COLORS.length)], clapboardTex ? { map: clapboardTex } : null);
    const trimColor = TRIM_COLORS[Math.floor(Math.random() * TRIM_COLORS.length)];
    const trimMat = toon(trimColor);
    const whiteMat = toon(0xfffdf5);
    const roofColor = ROOF_COLORS[Math.floor(Math.random() * ROOF_COLORS.length)];
    const roofMat = toon(roofColor, shingleTex ? { map: shingleTex } : null);
    const w = 2.3, h = 1.6, d = 2.1;
    const baseY = 0.18;

    // Cesped delante de la casa (hacia la pista) + valla blanca de estacas
    // bordeandolo -- como hijos de la casa para que aparezcan siempre juntos.
    const lawn = new THREE.Mesh(lawnGeo, lawnMat);
    lawn.rotation.x = -Math.PI / 2;
    lawn.position.set(0, 0.006, d / 2 + 0.7);
    lawn.receiveShadow = true;
    g.add(lawn);
    const fenceZ = d / 2 + 2.15;
    for (let i = -6; i <= 6; i++) {
      const picket = new THREE.Mesh(new THREE.BoxGeometry(0.045, 0.3, 0.045), whiteMat);
      picket.position.set(i * 0.27, 0.15, fenceZ);
      g.add(picket);
    }
    const fenceRail = new THREE.Mesh(new THREE.BoxGeometry(3.35, 0.035, 0.03), whiteMat);
    fenceRail.position.set(0, 0.22, fenceZ);
    g.add(fenceRail);

    // Setos recortados a lo largo de la fachada, pegados al zocalo
    const hedgeMat = toon(0x4a8f3f);
    for (let i = -1; i <= 1; i += 2) {
      const hedge = new THREE.Mesh(new THREE.SphereGeometry(0.22, 10, 8), hedgeMat);
      hedge.scale.set(1.4, 0.75, 0.9);
      hedge.position.set(i * (w * 0.32), 0.16, d / 2 + 0.22);
      g.add(hedge);
    }

    const foundation = new THREE.Mesh(new THREE.BoxGeometry(w + 0.06, baseY, d + 0.06), toon(0xb8b0a0));
    foundation.position.y = baseY / 2;
    g.add(foundation);

    const body = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), wallMat);
    body.position.y = baseY + h / 2;
    withOutline(body);
    g.add(body);

    const trimBand = new THREE.Mesh(new THREE.BoxGeometry(w + 0.02, 0.07, d + 0.02), whiteMat);
    trimBand.position.y = baseY + h;
    g.add(trimBand);

    // Tejado a dos aguas: dos paneles inclinados que suben hacia el centro
    // (la cumbrera) y bajan hacia los aleros -- no una piramide de 4 caras.
    const roofBaseY = baseY + h + 0.06;
    const roofAngle = 0.62;
    const roofOverhang = 0.22;
    const halfSpan = w / 2 + roofOverhang;
    const panelLen = halfSpan / Math.cos(roofAngle);
    const roofRise = halfSpan * Math.tan(roofAngle);
    for (const side of [-1, 1]) {
      const panel = new THREE.Mesh(new THREE.BoxGeometry(panelLen, 0.06, d + roofOverhang * 2), roofMat);
      panel.position.set(side * halfSpan * 0.5, roofBaseY + roofRise * 0.5, 0);
      panel.rotation.z = -side * roofAngle;
      withOutline(panel);
      g.add(panel);
    }

    // Buhardilla con su propio tejadillo a dos aguas, asomando del tejado
    if (Math.random() < 0.55) {
      const dw = 0.55, dh = 0.4, dd = 0.5;
      const dx = -w * 0.18, dz = d * 0.05;
      const dy = roofBaseY + roofRise * 0.4;
      const dormerBody = new THREE.Mesh(new THREE.BoxGeometry(dw, dh, dd), wallMat);
      dormerBody.position.set(dx, dy, dz);
      g.add(dormerBody);
      const dHalf = dw / 2 + 0.07;
      const dLen = dHalf / Math.cos(roofAngle);
      const dRise = dHalf * Math.tan(roofAngle);
      for (const side of [-1, 1]) {
        const dp = new THREE.Mesh(new THREE.BoxGeometry(dLen, 0.04, dd + 0.14), roofMat);
        dp.position.set(dx + side * dHalf * 0.5, dy + dh / 2 + dRise * 0.5, dz);
        dp.rotation.z = -side * roofAngle;
        g.add(dp);
      }
      const dormerWin = new THREE.Mesh(new THREE.PlaneGeometry(0.26, 0.26), windowMat);
      dormerWin.position.set(dx, dy, dz + dd / 2 + 0.01);
      g.add(dormerWin);
    }

    // Ventana circular decorativa cerca de la cumbrera
    if (Math.random() < 0.5) {
      const roundFrame = new THREE.Mesh(new THREE.TorusGeometry(0.14, 0.025, 8, 16), trimMat);
      roundFrame.position.set(w * 0.16, roofBaseY + roofRise * 0.5, d / 2 + 0.01);
      g.add(roundFrame);
      const roundWin = new THREE.Mesh(new THREE.CircleGeometry(0.12, 16), windowMat);
      roundWin.position.set(w * 0.16, roofBaseY + roofRise * 0.5, d / 2 + 0.006);
      g.add(roundWin);
    }

    if (Math.random() < 0.6) {
      const chimney = new THREE.Mesh(new THREE.BoxGeometry(0.22, 0.5, 0.22), toon(0x8a5a4a));
      chimney.position.set(w * 0.32, roofBaseY + roofRise * 0.75 + 0.22, d * 0.12);
      g.add(chimney);
      const chimneyCap = new THREE.Mesh(new THREE.BoxGeometry(0.28, 0.05, 0.28), toon(0x5a3a2a));
      chimneyCap.position.set(w * 0.32, roofBaseY + roofRise * 0.75 + 0.47, d * 0.12);
      g.add(chimneyCap);
    }

    // Puerta, marco y porche con techo propio
    const door = new THREE.Mesh(new THREE.BoxGeometry(0.4, 0.72, 0.05), toon(0x5c3a24));
    door.position.set(0, baseY + 0.36, d / 2 + 0.01);
    g.add(door);
    const doorFrame = new THREE.Mesh(new THREE.BoxGeometry(0.5, 0.84, 0.03), whiteMat);
    doorFrame.position.set(0, baseY + 0.42, d / 2 - 0.006);
    g.add(doorFrame);
    const stoop = new THREE.Mesh(new THREE.BoxGeometry(0.95, 0.08, 0.45), toon(0xc9c2b0));
    stoop.position.set(0, baseY - 0.04, d / 2 + 0.24);
    g.add(stoop);
    // Porche cubierto con columnas mas gruesas (base+capitel) y un pequeno
    // fronton triangular encima, tipo entrada "colonial" de barrio real.
    const porchRoof = new THREE.Mesh(new THREE.BoxGeometry(1.05, 0.05, 0.5), roofMat);
    porchRoof.position.set(0, baseY + 0.95, d / 2 + 0.3);
    g.add(porchRoof);
    const pedimentAngle = 0.5;
    const pedimentHalf = 0.55;
    const pedimentLen = pedimentHalf / Math.cos(pedimentAngle);
    const pedimentRise = pedimentHalf * Math.tan(pedimentAngle);
    for (const side of [-1, 1]) {
      const pp = new THREE.Mesh(new THREE.BoxGeometry(pedimentLen, 0.04, 0.42), whiteMat);
      pp.position.set(side * pedimentHalf * 0.5, baseY + 0.98 + pedimentRise * 0.5, d / 2 + 0.3);
      pp.rotation.z = -side * pedimentAngle;
      g.add(pp);
    }
    for (const px of [-0.42, 0.42]) {
      const colBase = new THREE.Mesh(new THREE.BoxGeometry(0.13, 0.05, 0.13), whiteMat);
      colBase.position.set(px, baseY + 0.1, d / 2 + 0.4);
      g.add(colBase);
      const column = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.055, 0.82, 10), whiteMat);
      column.position.set(px, baseY + 0.42, d / 2 + 0.4);
      g.add(column);
      const colCap = new THREE.Mesh(new THREE.BoxGeometry(0.14, 0.05, 0.14), whiteMat);
      colCap.position.set(px, baseY + 0.85, d / 2 + 0.4);
      g.add(colCap);
    }

    // Garaje adosado a un lado, con su entrada de coches desde la calle
    if (Math.random() < 0.65) {
      const garageW = 1.1, garageH = 1.1, garageD = 1.3;
      const gx = w / 2 + garageW / 2 - 0.05;
      const garageBody = new THREE.Mesh(new THREE.BoxGeometry(garageW, garageH, garageD), wallMat);
      garageBody.position.set(gx, baseY + garageH / 2, 0.1);
      withOutline(garageBody);
      g.add(garageBody);
      const garageDoor = new THREE.Mesh(new THREE.BoxGeometry(garageW - 0.15, garageH - 0.35, 0.04), whiteMat);
      garageDoor.position.set(gx, baseY + (garageH - 0.35) / 2 + 0.1, garageD / 2 + 0.01);
      g.add(garageDoor);
      for (let gy = 1; gy < 4; gy++) {
        const line = new THREE.Mesh(new THREE.BoxGeometry(garageW - 0.15, 0.015, 0.045), toon(0xc9c2b0));
        line.position.set(gx, baseY + 0.1 + gy * (garageH - 0.35) / 4, garageD / 2 + 0.03);
        g.add(line);
      }
      const driveway = new THREE.Mesh(new THREE.PlaneGeometry(1.3, 2.6), toon(0x9a9488));
      driveway.rotation.x = -Math.PI / 2;
      driveway.position.set(gx, 0.007, garageD / 2 + 1.3);
      driveway.receiveShadow = true;
      g.add(driveway);
    }

    // Ventanas altas con marco blanco y contraventanas de color a ambos lados
    for (const side of [-0.68, 0.68]) {
      const frame = new THREE.Mesh(new THREE.BoxGeometry(0.4, 0.6, 0.025), whiteMat);
      frame.position.set(side, baseY + h * 0.58, d / 2 + 0.006);
      g.add(frame);
      const win = new THREE.Mesh(new THREE.PlaneGeometry(0.3, 0.5), windowMat);
      win.position.set(side, baseY + h * 0.58, d / 2 + 0.022);
      g.add(win);
      for (const sSide of [-1, 1]) {
        const shutter = new THREE.Mesh(new THREE.BoxGeometry(0.09, 0.54, 0.025), trimMat);
        shutter.position.set(side + sSide * 0.24, baseY + h * 0.58, d / 2 + 0.012);
        g.add(shutter);
      }
    }

    return g;
  }
  function makeFenceSegment() {
    const g = new THREE.Group();
    const mat = toon(0xf2ede0);
    for (let i = 0; i < 4; i++) {
      const post = new THREE.Mesh(new THREE.BoxGeometry(0.05, 0.5, 0.05), mat);
      post.position.set(-0.6 + i * 0.4, 0.25, 0);
      g.add(post);
      // Remate en punta sobre cada poste (antes terminaban en un corte plano).
      const cap = new THREE.Mesh(new THREE.ConeGeometry(0.045, 0.09, 4), mat);
      cap.rotation.y = Math.PI / 4;
      cap.position.set(-0.6 + i * 0.4, 0.545, 0);
      g.add(cap);
    }
    for (const ry of [0.15, 0.35]) {
      const rail = new THREE.Mesh(new THREE.BoxGeometry(1.3, 0.05, 0.03), mat);
      rail.position.y = ry;
      g.add(rail);
    }
    return g;
  }
  function makeMailbox() {
    const g = new THREE.Group();
    const post = new THREE.Mesh(new THREE.BoxGeometry(0.05, 0.8, 0.05), toon(0x6b4a2f));
    post.position.y = 0.4;
    g.add(post);
    const box = new THREE.Mesh(new THREE.CapsuleGeometry(0.09, 0.2, 4, 8), toon(0x3a5a8a));
    box.rotation.z = Math.PI / 2;
    box.position.y = 0.82;
    g.add(box);
    // Bandera roja lateral, el detalle clasico de un buzon de EEUU (antes
    // era solo el cilindro pelado sin nada que lo distinguiera).
    const flagMat = toon(0xd8322f);
    const flagPole = new THREE.Mesh(new THREE.CylinderGeometry(0.008, 0.008, 0.1, 4), toon(0x8a8a8a));
    flagPole.position.set(0.1, 0.9, 0.02);
    flagPole.rotation.z = -0.5;
    g.add(flagPole);
    const flag = new THREE.Mesh(new THREE.BoxGeometry(0.03, 0.08, 0.01), flagMat);
    flag.position.set(0.14, 0.95, 0.02);
    flag.rotation.z = -0.5;
    g.add(flag);
    return g;
  }

  // Postes de tendido electrico con cables colgando (catenaria aproximada
  // con varios segmentos rectos) -- toque clasico de calle urbana.
  function makePowerLinePoles() {
    const g = new THREE.Group();
    const poleMat = toon(0x4a4a4a);
    const postXs = [-1.6, 1.6];
    const crossbarY = 3.05;
    for (const px of postXs) {
      const pole = new THREE.Mesh(new THREE.CylinderGeometry(0.035, 0.045, 3.2, 8), poleMat);
      pole.position.set(px, 1.6, 0);
      g.add(pole);
      const crossbar = new THREE.Mesh(new THREE.BoxGeometry(0.5, 0.04, 0.04), poleMat);
      crossbar.position.set(px, crossbarY, 0);
      g.add(crossbar);
    }
    const wireMat = toon(0x2a2a2a);
    const segments = 8;
    for (let i = 0; i < segments; i++) {
      const t0 = i / segments, t1 = (i + 1) / segments;
      const x0 = postXs[0] + (postXs[1] - postXs[0]) * t0;
      const x1 = postXs[0] + (postXs[1] - postXs[0]) * t1;
      const y0 = crossbarY - Math.sin(Math.PI * t0) * 0.35;
      const y1 = crossbarY - Math.sin(Math.PI * t1) * 0.35;
      const segLen = Math.hypot(x1 - x0, y1 - y0);
      const seg = new THREE.Mesh(new THREE.CylinderGeometry(0.012, 0.012, segLen, 4), wireMat);
      seg.position.set((x0 + x1) / 2, (y0 + y1) / 2, 0);
      seg.rotation.z = Math.atan2(y1 - y0, x1 - x0) + Math.PI / 2;
      g.add(seg);
    }
    return g;
  }

  // -- Washington D.C.: monumentos reconocibles pero estilizados, en el
  // mismo lenguaje low-poly/juguete que el resto del juego. Zona solo
  // jugable si se elige a proposito en el menu (ver setForcedZone). --
  function makeWhiteHouse() {
    const wMat = toon(0xfdfdf5);
    const g = new THREE.Group();
    const w = 3.2, h = 1.3, d = 2.2;
    const body = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), wMat);
    body.position.y = h / 2;
    withOutline(body);
    g.add(body);
    // Portico central con columnas
    const porticoW = 1.6, porticoH = 1.0;
    for (let i = 0; i < 5; i++) {
      const col = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.06, porticoH, 10), wMat);
      col.position.set(-porticoW / 2 + i * (porticoW / 4), porticoH / 2, d / 2 + 0.35);
      g.add(col);
    }
    const porticoRoof = new THREE.Mesh(new THREE.BoxGeometry(porticoW + 0.2, 0.08, 0.75), wMat);
    porticoRoof.position.set(0, porticoH + 0.04, d / 2 + 0.35);
    g.add(porticoRoof);
    const pedAngle = 0.45, pedHalf = (porticoW + 0.2) / 2;
    const pedLen = pedHalf / Math.cos(pedAngle), pedRise = pedHalf * Math.tan(pedAngle);
    for (const side of [-1, 1]) {
      const pp = new THREE.Mesh(new THREE.BoxGeometry(pedLen, 0.05, 0.7), wMat);
      pp.position.set(side * pedHalf * 0.5, porticoH + 0.08 + pedRise * 0.5, d / 2 + 0.35);
      pp.rotation.z = -side * pedAngle;
      g.add(pp);
    }
    // Cupula central (insinuada, no literal)
    const dome = new THREE.Mesh(new THREE.SphereGeometry(0.32, 12, 10, 0, Math.PI * 2, 0, Math.PI * 0.55), wMat);
    dome.position.set(0, h + 0.02, 0);
    g.add(dome);
    for (let i = 0; i < 5; i++) {
      const win = new THREE.Mesh(new THREE.PlaneGeometry(0.26, 0.38), windowMat);
      win.position.set(-w / 2 + 0.35 + i * (w - 0.7) / 4, h * 0.55, d / 2 + 0.01);
      g.add(win);
    }
    // Alas laterales mas bajas (antes solo el cuerpo central -- la
    // referencia real tiene el Ala Oeste y el Ala Este a los costados) y
    // un par de chimeneas en el techo.
    for (const side of [-1, 1]) {
      const wing = new THREE.Mesh(new THREE.BoxGeometry(0.9, h * 0.6, d * 0.75), wMat);
      wing.position.set(side * (w / 2 + 0.5), h * 0.3, -d * 0.05);
      g.add(wing);
    }
    const chimneyMat = toon(0xd8d2c0);
    for (const cx of [-0.9, 0.9]) {
      const chimney = new THREE.Mesh(new THREE.BoxGeometry(0.12, 0.3, 0.12), chimneyMat);
      chimney.position.set(cx, h + 0.15, -d * 0.25);
      g.add(chimney);
    }
    g.userData.frontZ = true; // portico y ventanas miran a +Z
    // Escala de monumento: sin esto medía 1.3 de alto, mas bajo que el propio
    // jugador (2.2) y perdido al lado de los edificios de ciudad (4-12).
    g.scale.setScalar(2.4);
    return g;
  }
  function makeWashingtonMonument() {
    const g = new THREE.Group();
    const stoneMat = toon(0xe8e4d8);
    const h = 5.2;
    const shaft = new THREE.Mesh(new THREE.CylinderGeometry(0.18, 0.26, h, 4), stoneMat);
    shaft.position.y = h / 2;
    shaft.rotation.y = Math.PI / 4;
    withOutline(shaft);
    g.add(shaft);
    const tip = new THREE.Mesh(new THREE.ConeGeometry(0.19, 0.4, 4), stoneMat);
    tip.position.y = h + 0.2;
    tip.rotation.y = Math.PI / 4;
    g.add(tip);
    return g;
  }
  function makePentagon() {
    const g = new THREE.Group();
    const mat = toon(0xc9bfa0);
    // Altura subida de 0.55 a 1.9: era un disco plano tumbado en el suelo,
    // invisible desde la camara de carrera por muy ancho que fuera.
    const outer = new THREE.Mesh(new THREE.CylinderGeometry(1.5, 1.5, 1.9, 5), mat);
    outer.position.y = 0.95;
    g.add(outer);
    // El patio sube con el edificio (antes se quedaba en y=0.29 y con el
    // cuerpo ya alto habria quedado enterrado dentro).
    const courtyard = new THREE.Mesh(new THREE.CylinderGeometry(0.78, 0.78, 2.0, 5), toon(0x6fc24a));
    courtyard.position.y = 0.97;
    g.add(courtyard);
    // Franjas horizontales que marcan las plantas, para que se lea como un
    // edificio y no como un prisma liso.
    for (let i = 1; i <= 3; i++) {
      const band = new THREE.Mesh(new THREE.CylinderGeometry(1.53, 1.53, 0.06, 5), toon(0xa89e80));
      band.position.y = i * 0.47;
      g.add(band);
    }
    g.scale.setScalar(1.6);
    return g;
  }
  // Antes era una caja lisa con columnas pegadas -- sin remate arriba, sin
  // entrada, sin ventanas. Ahora tiene fronton triangular, escalinata,
  // ventanas laterales y un asta con bandera en el techo.
  function makeGovBuilding() {
    const g = new THREE.Group();
    const mat = toon(0xf0ede0);
    const w = 1.8, h = 1.8, d = 1.6;
    const body = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), mat);
    body.position.y = h / 2;
    g.add(body);
    for (let i = 0; i < 4; i++) {
      const col = new THREE.Mesh(new THREE.CylinderGeometry(0.045, 0.045, h * 0.85, 8), mat);
      col.position.set(-w / 2 + 0.25 + i * (w - 0.5) / 3, h * 0.425, d / 2 + 0.02);
      g.add(col);
    }
    const pedAngle = 0.4, pedHalf = w / 2 + 0.1;
    const pedLen = pedHalf / Math.cos(pedAngle), pedRise = pedHalf * Math.tan(pedAngle);
    for (const side of [-1, 1]) {
      const pp = new THREE.Mesh(new THREE.BoxGeometry(pedLen, 0.06, 0.5), mat);
      pp.position.set(side * pedHalf * 0.5, h + pedRise * 0.5, d / 2 + 0.02);
      pp.rotation.z = -side * pedAngle;
      g.add(pp);
    }
    const stepMat = toon(0xd8d2c0);
    for (let i = 0; i < 3; i++) {
      const sw = w * 0.6 + i * 0.15;
      const step = new THREE.Mesh(new THREE.BoxGeometry(sw, 0.08, 0.18), stepMat);
      step.position.set(0, 0.04 + i * 0.08, d / 2 + 0.35 - i * 0.18);
      g.add(step);
    }
    for (let i = 0; i < 3; i++) {
      const win = new THREE.Mesh(windowGeo, windowMat);
      win.scale.set(d * 0.16, 0.3, 1);
      win.position.set(-w / 2 - 0.01, 0.35 + i * 0.55, (i - 1) * 0.4);
      win.rotation.y = -Math.PI / 2;
      g.add(win);
    }
    const flagPole = new THREE.Mesh(new THREE.CylinderGeometry(0.02, 0.02, 0.5, 6), stepMat);
    flagPole.position.set(0, h + pedRise + 0.25, 0);
    g.add(flagPole);
    const flag = new THREE.Mesh(new THREE.PlaneGeometry(0.22, 0.14), toon(0x2f6bff, { side: THREE.DoubleSide }));
    flag.position.set(0.11, h + pedRise + 0.42, 0);
    g.add(flag);
    g.userData.frontZ = true; // fronton, columnas y escalinata miran a +Z
    g.scale.setScalar(2.0);
    return g;
  }
  // Capitolio: faltaba por completo, y es junto a la Casa Blanca el edificio
  // que hace reconocible la zona. Cuerpo alargado con alas a los lados,
  // escalinata, portico de columnas y sobre todo la cupula sobre tambor
  // cilindrico rematada en linterna -- la silueta que lo identifica.
  function makeCapitol() {
    const g = new THREE.Group();
    const stoneMat = toon(0xf2efe2);
    const w = 4.4, h = 1.5, d = 2.0;
    const body = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), stoneMat);
    body.position.y = h / 2;
    g.add(body);
    // Alas laterales mas bajas
    for (const side of [-1, 1]) {
      const wing = new THREE.Mesh(new THREE.BoxGeometry(1.3, h * 0.72, d * 0.85), stoneMat);
      wing.position.set(side * (w / 2 + 0.6), h * 0.36, 0);
      g.add(wing);
    }
    // Tambor + cupula + linterna (la silueta caracteristica)
    const drum = new THREE.Mesh(new THREE.CylinderGeometry(0.62, 0.7, 0.75, 16), stoneMat);
    drum.position.y = h + 0.375;
    g.add(drum);
    for (let i = 0; i < 12; i++) {
      const a = (i / 12) * Math.PI * 2;
      const col = new THREE.Mesh(new THREE.CylinderGeometry(0.045, 0.045, 0.68, 6), stoneMat);
      col.position.set(Math.cos(a) * 0.66, h + 0.375, Math.sin(a) * 0.66);
      g.add(col);
    }
    const dome = new THREE.Mesh(new THREE.SphereGeometry(0.66, 18, 12, 0, Math.PI * 2, 0, Math.PI * 0.5), stoneMat);
    dome.position.y = h + 0.75;
    dome.scale.y = 1.15;
    g.add(dome);
    const lantern = new THREE.Mesh(new THREE.CylinderGeometry(0.13, 0.16, 0.3, 10), stoneMat);
    lantern.position.y = h + 1.5;
    g.add(lantern);
    const statue = new THREE.Mesh(new THREE.ConeGeometry(0.09, 0.22, 8), toon(0xbfae6a));
    statue.position.y = h + 1.76;
    g.add(statue);
    // Portico de columnas y escalinata al frente (cara +Z local)
    for (let i = 0; i < 6; i++) {
      const col = new THREE.Mesh(new THREE.CylinderGeometry(0.07, 0.07, h * 0.8, 10), stoneMat);
      col.position.set(-0.75 + i * 0.3, h * 0.4, d / 2 + 0.16);
      g.add(col);
    }
    const pedAngle = 0.4, pedHalf = 1.05;
    const pedLen = pedHalf / Math.cos(pedAngle), pedRise = pedHalf * Math.tan(pedAngle);
    for (const side of [-1, 1]) {
      const pp = new THREE.Mesh(new THREE.BoxGeometry(pedLen, 0.07, 0.42), stoneMat);
      pp.position.set(side * pedHalf * 0.5, h * 0.8 + pedRise * 0.5, d / 2 + 0.16);
      pp.rotation.z = -side * pedAngle;
      g.add(pp);
    }
    const steps = toon(0xdcd6c4);
    for (let i = 0; i < 4; i++) {
      const st = new THREE.Mesh(new THREE.BoxGeometry(2.2 + i * 0.25, 0.09, 0.22), steps);
      st.position.set(0, 0.045 + i * 0.09, d / 2 + 0.55 - i * 0.22);
      g.add(st);
    }
    g.userData.frontZ = true; // su fachada mira a +Z, no a -X
    g.scale.setScalar(2.2);
    return g;
  }

  function makeCherryBlossomTree() {
    const g = new THREE.Group();
    const trunk = new THREE.Mesh(new THREE.CylinderGeometry(0.07, 0.09, 1.0, 8), toon(0x6b4a2f));
    trunk.position.y = 0.5;
    g.add(trunk);
    const foliageMat = toon(0xffb7c5);
    for (let i = 0; i < 3; i++) {
      const puff = new THREE.Mesh(new THREE.SphereGeometry(0.42 - i * 0.05, 10, 8), foliageMat);
      puff.position.set((Math.random() - 0.5) * 0.2, 1.15 + i * 0.28, (Math.random() - 0.5) * 0.2);
      g.add(puff);
    }
    return g;
  }

  const BIOME_PROP_FACTORIES = {
    city: [makeBuilding, makeStreetLamp, makeParkedCar, makeStreetTree, makeBench, makeFireHydrant, makeTrafficLight, makePowerLinePoles],
    desert: [makeCactus, makeTumbleweed, makeMesa, makeDeadTree],
    town: [makeHouse, makeFenceSegment, makeMailbox, makeStreetTree],
    dc: [makeWhiteHouse, makeWashingtonMonument, makeCapitol, makeGovBuilding, makeCherryBlossomTree, makePentagon],
  };
  // Zonas hechas en Blender (blender/<zona>.py). Si alguno de sus modelos no
  // ha cargado, esa zona se queda con la version de primitivas de arriba.
  //   fachadas/pesos: los edificios y cuanto sale cada uno (los monumentos
  //     menos que el relleno, para que no haya tres Casas Blancas seguidas)
  //   linea: x donde acaba lo que sobresale por delante (cesped, escalones)
  //   acera: mobiliario sobre la acera; `alterna` = uno y uno, en orden
  //   coches: aparcados en batería delante de las fachadas, a lo largo de la calle
  const ZONAS_BLENDER = {
    dc: {
      carpeta: "dc", linea: 9.2, alterna: true,
      fachadas: ["casa_blanca", "capitolio", "lincoln", "federal", "georgetown"], pesos: [1, 1, 1, 3, 3],
      acera: ["cerezo", "farola"], aceraPesos: [1, 1], coches: [],
    },
    city: {
      carpeta: "ciudad", linea: 10.2,
      fachadas: ["tienda_roja", "tienda_crema", "oficina_azul", "oficina_verde", "artdeco", "diner", "apart_morado", "apart_naranja"],
      pesos: [2, 2, 2, 2, 1, 1, 2, 2],
      acera: ["arbol_ciudad", "farola_ciudad", "semaforo", "hidrante", "banco", "buzon"], aceraPesos: [4, 4, 1, 1, 2, 1],
      coches: ["taxi", "coche_rojo", "coche_azul"],
      orienta: { farola_ciudad: "brazo", banco: "calle", buzon: "calle", semaforo: "jugador" },
    },
    town: {
      carpeta: "pueblo", linea: 9.6,
      fachadas: ["vict_blanca", "vict_azul", "rancho", "colonial", "cabana_rosa", "iglesia"], pesos: [3, 3, 3, 3, 3, 1],
      acera: ["roble", "arbusto", "buzon_pueblo", "farola_pueblo"], aceraPesos: [4, 2, 2, 2],
      // los coches son los de la ciudad (un nombre con "/" es carpeta/pieza)
      coches: ["ciudad/coche_rojo", "ciudad/coche_azul"],
      orienta: { buzon_pueblo: "calle" },
    },
  };
  const zonaBlender = {};
  const clave = (z, n) => (n.includes("/") ? n : `${z.carpeta}/${n}`);
  for (const zona in ZONAS_BLENDER) {
    const z = ZONAS_BLENDER[zona];
    const nombres = [...z.fachadas, ...z.acera, ...z.coches];
    if (!nombres.every((n) => hayModelo(clave(z, n)))) continue;
    BIOME_PROP_FACTORIES[zona] = nombres.map((n, i) => () => {
      const g = modelo(clave(z, n));
      g.userData.fachada = i < z.fachadas.length;
      return g;
    });
    const repartir = (pesos, desde) => pesos.flatMap((p, i) => Array(p).fill(desde + i));
    zonaBlender[zona] = {
      ...z,
      sorteoFachada: repartir(z.pesos, 0),
      sorteoAcera: repartir(z.aceraPesos, z.fachadas.length),
      primerCoche: z.fachadas.length + z.acera.length,
      medidas: nombres.map((n) => medidas(clave(z, n))),
    };
  }
  const outerPools = {};
  for (const biome in BIOME_PROP_FACTORIES) {
    outerPools[biome] = BIOME_PROP_FACTORIES[biome].map((factory) => makePool(factory));
  }

  const outerProps = [];
  let lastOuterZ = -4;
  // Indices (dentro de BIOME_PROP_FACTORIES) de los props "grandes" que
  // forman la linea de fachada de la calle. El resto es mobiliario urbano y
  // va en la banda cercana, entre la acera y las fachadas. El desierto no
  // tiene fachada a proposito: ahi lo natural ES que este todo disperso.
  // D.C.: Casa Blanca(0) y Capitolio(2) son los que hacen reconocible la
  // zona, asi que van repetidos en la lista para que salgan mas a menudo que
  // el edificio generico(3). Monumento(1), cerezos(4) y Pentagono(5) quedan
  // como relleno cercano.
  const BIOME_FRONTAGE_IDX = { city: [0], town: [0], dc: [0, 0, 2, 2, 3], desert: [] };
  // D.C. usa un retranqueo mayor: sus monumentos son mucho mas anchos que un
  // edificio corriente (la Casa Blanca escalada mide ~8 de ancho), asi que
  // con la linea comun se meterian encima de la acera.
  const FRONTAGE_X_BY_ZONE = { city: 10.5, town: 10.5, dc: 14.5, desert: 10.5 };
  // Separacion subida de 8 a 11: al triplicar la distancia de dibujado el
  // numero de props vivos se disparo (5712 mallas medidas). Los edificios
  // miden 3.4-5.6 de ancho y van 2 por grupo, o sea uno cada 5.5, asi que la
  // fachada sigue siendo continua con bastante menos coste.
  const OUTER_SPACING = 11;

  const frontCursor = { "-1": null, "1": null };
  const frontLast = { "-1": -1, "1": -1 };

  // ---- Modo nivel (24/10/2026): la calle de verdad de levels.js ----
  // Cada edificio sale en su sitio fijo de la avenida (no al azar) y la
  // calle se acaba en la Casa Blanca. `nivel` = null es el modo sin fin.
  let nivel = null;
  let azar = Math.random;
  let calle = [], siguientePieza = 0;
  const calleViva = [];
  let casaBlanca = null;
  const COLORES_ORIGINALES = JSON.parse(JSON.stringify(BIOME_COLORS));
  function setNivel(n) { nivel = n || null; }
  function getNivel() { return nivel; }
  // Luz del nivel: el atardecer tiñe cielo, niebla y horizonte de Washington.
  function setLuz(luz) {
    for (const z in COLORES_ORIGINALES) BIOME_COLORS[z] = { ...COLORES_ORIGINALES[z] };
    if (luz === "manana") {
      Object.assign(BIOME_COLORS.city, { sky: 0xd8ebff, skyTop: 0x5f9fea, fog: 0xd8ebff, horizon: 0x8aa2c4 });
    }
    if (luz === "mediodia") {
      Object.assign(BIOME_COLORS.city, { sky: 0xb4dcff, skyTop: 0x2f7fe6, fog: 0xc4e2ff, horizon: 0x7f9fc8 });
    }
    if (luz === "atardecer") {
      Object.assign(BIOME_COLORS.dc, { sky: 0xffd2a8, skyTop: 0x6d7fc4, fog: 0xf6d2b0, horizon: 0x8d7f9c });
    }
  }
  function prepararCalle() {
    for (const p of calleViva) { group.remove(p.mesh); soltarEdificio(p.mesh); }
    calleViva.length = 0;
    casaBlanca = null;
    calle = nivel ? [...colocarNivel(nivel, (k) => ANCHO[k] || 20), ...sueloDeNivel(nivel)].sort((a, b) => a.d - b.d) : [];
    siguientePieza = 0;
    // Siguiendo desde el punto de control: lo que ya quedo atras no se pone.
    while (siguientePieza < calle.length && calle[siguientePieza].d + (calle[siguientePieza].ancho || 10) < totalScrolled - 15) siguientePieza++;
    azar = nivel ? azarConSemilla(nivel.semilla) : Math.random;
  }
  // Retranqueo: lo que sobresale mucho (porticos, plazas) se mete hacia
  // dentro para no invadir la acera; la fachada queda un poco mas atras.
  function actualizarCalle(dz) {
    if (!nivel) return;
    // Primero se mueve lo que ya estaba y despues se pone lo nuevo (si no, lo
    // recien puesto avanzaba dz de mas y salia mas cerca de lo que toca).
    for (let i = calleViva.length - 1; i >= 0; i--) {
      const p = calleViva[i];
      p.mesh.position.z += dz;
      if (p.mesh.position.z > DESPAWN_Z + p.fin && p.mesh !== casaBlanca) {
        group.remove(p.mesh);
        soltarEdificio(p.mesh);
        calleViva.splice(i, 1);
      }
    }
    const alcance = Math.abs(SPAWN_Z) + 25;
    while (siguientePieza < calle.length && calle[siguientePieza].d - totalScrolled < alcance) {
      const p = calle[siguientePieza++];
      if (p.tipo) {
        // Del suelo: paso de cebra o tapa de alcantarilla (no son modelos).
        const m = p.tipo === "cebra" ? hacerCebra() : hacerTapa();
        m.position.set(p.x || 0, 0, -(p.d - totalScrolled));
        group.add(m);
        calleViva.push({ mesh: m, fin: 10 });
        continue;
      }
      if (p.arco) {
        // El arco del punto de control, de lado a lado de la calle.
        const a = construirArco();
        a.position.set(0, 0, -(p.d - totalScrolled));
        group.add(a);
        calleViva.push({ mesh: a, fin: 20 });
        continue;
      }
      const clave = `${nivel.carpeta}/${p.pieza}`;
      // Edificio unico del kit (su semilla sale del sitio que ocupa) o pieza modelada.
      const mesh = p.pieza === "kit" ? construirEdificio(azarConSemilla(p.semilla), p.ancho, { ...nivel.kit, ...p.opciones }) : modelo(clave);
      if (!mesh) continue;
      const m = p.pieza === "kit" ? { frente: mesh.userData.frente } : medidas(clave);
      if (p.centro) {
        mesh.position.set(0, 0.05, -(p.d - totalScrolled));
        if (p.pieza === "casa_blanca_final") {
          // Las dos hojas de la puerta, abiertas; la escena final las cierra.
          const puertas = [];
          for (const lado of [-1, 1]) {
            const hoja = modelo(`${nivel.carpeta}/puerta_cb`);
            if (!hoja) continue;
            hoja.position.set(lado * 1.3, 1.0, 0.06);
            hoja.rotation.y = Math.PI / 2;
            hoja.userData.cerrada = lado < 0 ? 0 : Math.PI;
            mesh.add(hoja);
            puertas.push(hoja);
          }
          mesh.userData.puertas = puertas;
        }
        casaBlanca = mesh;   // lo del fondo: donde acaba el nivel (Casa Blanca, Flatiron...)
      } else {
        const retranqueo = Math.max(0, m.frente - 3);
        mesh.position.set(p.lado * (nivel.linea + retranqueo), 0, -(p.d + p.ancho / 2 - totalScrolled));
        mesh.rotation.y = p.lado < 0 ? Math.PI / 2 : -Math.PI / 2;
      }
      group.add(mesh);
      calleViva.push({ mesh, fin: p.ancho + 40 });
    }
  }
  // Farolas y arboles de la acera, alternos (estos si se repiten: es mobiliario).
  const acerasNivel = {};
  function aceraNivel(z) {
    if (totalScrolled - z > nivel.largo - 15) return;
    if (!acerasNivel[nivel.id]) {
      acerasNivel[nivel.id] = nivel.acera.map((k) => makePool(() => modelo(k)));
      outerPools["nivel_" + nivel.id] = acerasNivel[nivel.id];
    }
    const pools = acerasNivel[nivel.id];
    aceraNivel.n = (aceraNivel.n || 0) + 1;
    for (const side of [-1, 1]) {
      for (let k = 0; k < 1; k++) {
        const idx = (aceraNivel.n + (side > 0 ? 1 : 0)) % pools.length;
        const mesh = pools[idx].acquire();
        if (!mesh) continue;
        mesh.visible = true;
        mesh.rotation.set(0, side < 0 ? 0 : Math.PI, 0);
        mesh.position.set(side * 7.6, 0, z - k * (OUTER_SPACING / 2));
        if (!mesh.parent) group.add(mesh);
        outerProps.push({ mesh, biome: "nivel_" + nivel.id, poolIndex: idx });
      }
    }
  }
  function getCasaBlanca() { return casaBlanca; }

  // ---- Arco del punto de control (27/10/2026) ----
  // Dos columnas hinchables con rayas rojas y blancas y un cartel azul con
  // estrellas: se ve venir de lejos y al pasar por debajo se guarda el sitio.
  const arcoRojo = toon(0xe8463c), arcoBlanco = toon(0xffffff), arcoAzul = toon(0x2350c8), arcoOro = toon(GOLD);
  const arcoSegGeo = new THREE.CylinderGeometry(0.42, 0.42, 0.78, 16);
  let arcoTex = null, arcoTexLang = null;
  function texturaArco() {
    const lang = tr("puntoControl");
    if (arcoTex && arcoTexLang === lang) return arcoTex;
    const c = document.createElement("canvas");
    c.width = 1024; c.height = 160;
    const x = c.getContext("2d");
    x.fillStyle = "#2350c8"; x.fillRect(0, 0, 1024, 160);
    x.strokeStyle = "#ffffff"; x.lineWidth = 10; x.strokeRect(10, 10, 1004, 140);
    x.fillStyle = "#ffffff";
    x.font = '700 84px Fredoka, "Arial Rounded MT Bold", Arial, sans-serif';
    x.textAlign = "center"; x.textBaseline = "middle";
    x.fillText(lang.toUpperCase(), 512, 86);
    x.fillStyle = "#ffd23f";
    for (const px of [60, 964]) {
      x.beginPath();
      for (let i = 0; i < 10; i++) {
        const r = i % 2 ? 16 : 38, a = -Math.PI / 2 + (i * Math.PI) / 5;
        x.lineTo(px + Math.cos(a) * r, 80 + Math.sin(a) * r);
      }
      x.closePath(); x.fill();
    }
    arcoTex = new THREE.CanvasTexture(c);
    arcoTex.colorSpace = THREE.SRGBColorSpace;
    arcoTex.anisotropy = 4;
    arcoTexLang = lang;
    return arcoTex;
  }
  function construirArco() {
    const g = new THREE.Group();
    for (const s of [-1, 1]) {
      for (let i = 0; i < 7; i++) {
        const seg = new THREE.Mesh(arcoSegGeo, i % 2 ? arcoBlanco : arcoRojo);
        seg.position.set(s * 4.55, 0.39 + i * 0.78, 0);
        g.add(seg);
      }
      const bola = new THREE.Mesh(new THREE.SphereGeometry(0.5, 16, 12), arcoOro);
      bola.position.set(s * 4.55, 5.75, 0);
      g.add(bola);
    }
    const cartel = new THREE.Mesh(new THREE.BoxGeometry(9.4, 1.5, 0.35), arcoAzul);
    cartel.position.y = 4.85;
    g.add(cartel);
    const letrero = new THREE.Mesh(new THREE.PlaneGeometry(9.0, 1.4), new THREE.MeshBasicMaterial({ map: texturaArco() }));
    letrero.position.set(0, 4.85, 0.18);
    g.add(letrero);
    return g;
  }
  const cebraGeo = new THREE.BoxGeometry(0.55, 0.02, 4.2);
  const cebraMat = toon(0xf2efe6);
  const lineaGeo = new THREE.BoxGeometry(7.6, 0.02, 0.35);
  function hacerCebra() {
    const g = new THREE.Group();
    for (let k = 0; k < 8; k++) {
      const b = new THREE.Mesh(cebraGeo, cebraMat);
      b.position.set(-3.3 + k * 0.95, 0.072, 0);
      g.add(b);
    }
    const l = new THREE.Mesh(lineaGeo, cebraMat);
    l.position.set(0, 0.072, 3.2);
    g.add(l);
    return g;
  }
  const tapaGeo = new THREE.CylinderGeometry(0.42, 0.42, 0.03, 18);
  const tapaMat = toon(0x4a4c52);
  const tapaAroGeo = new THREE.TorusGeometry(0.42, 0.04, 6, 18);
  function hacerTapa() {
    const g = new THREE.Group();
    const t = new THREE.Mesh(tapaGeo, tapaMat);
    t.position.y = 0.065;
    const a = new THREE.Mesh(tapaAroGeo, toon(0x6a6c72));
    a.rotation.x = Math.PI / 2; a.position.y = 0.075;
    g.add(t, a);
    return g;
  }

  function spawnOuterCluster(z) {
    if (nivel) { aceraNivel(z); return; }
    // Un prop spawneado ahora en z (negativo) sera alcanzado tras recorrer
    // |z| unidades mas -> el bioma se decide para la distancia en que
    // realmente llegara el jugador, no la actual (o la zona forzada, si hay una).
    const biome = currentZoneName(totalScrolled - z);
    const factories = BIOME_PROP_FACTORIES[biome];
    const pools = outerPools[biome];
    const frontIdx = BIOME_FRONTAGE_IDX[biome] || [];

    // Los edificios corrientes tienen la fachada en su cara -X, asi que con
    // rotacion 0/PI ya miran a la calzada. Pero los monumentos de D.C. se
    // construyeron con el portico, las columnas y la escalinata en la cara
    // +Z: con la misma rotacion quedaban de canto o de espaldas, y por eso
    // no se reconocian aunque estuvieran ahi. Los marcados con `frontZ` se
    // giran 90 grados extra para que su fachada mire de verdad a la calle.
    function place(idx, x, pz, ry) {
      const mesh = pools[idx].acquire();
      mesh.visible = true;
      // Piezas de Blender: la fachada mira a +Z local; girada +90 grados mira a
      // +X (calle a la izquierda) y -90 a -X (calle a la derecha).
      const faceZ = mesh.userData.fachada ? (x < 0 ? Math.PI / 2 : -Math.PI / 2)
        : mesh.userData.frontZ ? (x < 0 ? -Math.PI / 2 : Math.PI / 2) : ry;
      mesh.rotation.set(0, faceZ, 0);
      mesh.position.set(x, 0, pz);
      if (!mesh.parent) group.add(mesh);
      outerProps.push({ mesh, biome, poolIndex: idx });
    }

    // Zonas de Blender: manzana continua. Cada lado lleva un cursor que avanza
    // lo que mide de ancho cada edificio, asi el Capitolio (16 de ancho) no se
    // monta encima del vecino. Todos alinean su parte delantera (cesped o
    // escalinata) en la misma linea, detras de la acera.
    const zb = zonaBlender[biome];
    if (zb) {
      const sortear = (lista) => lista[Math.floor(Math.random() * lista.length)];
      for (const side of [-1, 1]) {
        if (frontCursor[side] === null || Math.abs(frontCursor[side] - z) > 40) frontCursor[side] = z + OUTER_SPACING / 2;
        while (frontCursor[side] > z - OUTER_SPACING / 2) {
          let idx = sortear(zb.sorteoFachada);
          for (let t = 0; t < 4 && idx === frontLast[side]; t++) idx = sortear(zb.sorteoFachada);
          frontLast[side] = idx;
          const m = zb.medidas[idx];
          place(idx, side * (zb.linea + m.frente), frontCursor[side] - m.ancho / 2, 0);
          frontCursor[side] -= m.ancho + 0.5 + Math.random() * 1.5;
        }
        for (let k = 0; k < 2; k++) {
          const idx = zb.alterna ? zb.fachadas.length + k : sortear(zb.sorteoAcera);
          // Blender: el brazo de la farola apunta a +X y el frente de banco,
          // buzon y semaforo a +Z local.
          const giro = {
            brazo: side < 0 ? 0 : Math.PI,                 // hacia la calzada
            calle: side < 0 ? Math.PI / 2 : -Math.PI / 2,  // de cara a la calzada
            jugador: 0,                                    // de cara a quien llega
          }[(zb.orienta || {})[zb.acera[idx - zb.fachadas.length]]];
          place(idx, side * (7.4 + Math.random() * 0.4), z - k * (OUTER_SPACING / 2) + (Math.random() - 0.5),
            giro === undefined ? Math.random() * Math.PI * 2 : giro);
        }
        if (zb.coches.length && Math.random() < 0.6) {
          const idx = zb.primerCoche + Math.floor(Math.random() * zb.coches.length);
          place(idx, side * 8.95, z - 2 - Math.random() * 6, Math.random() < 0.5 ? Math.PI / 2 : -Math.PI / 2);
        }
      }
      return;
    }

    // Desierto: disperso y con orientacion libre, como antes.
    if (!frontIdx.length) {
      for (const side of [-1, 1]) {
        const count = 2 + Math.floor(Math.random() * 2);
        for (let i = 0; i < count; i++) {
          place(Math.floor(Math.random() * factories.length),
            side * (9.5 + Math.random() * 7), z - i * 2 + (Math.random() - 0.5), Math.random() * Math.PI * 2);
        }
      }
      return;
    }

    // Resto de zonas: calle de verdad. Los edificios se alinean sobre una
    // linea de retranqueo casi constante y se colocan pegados entre si a lo
    // largo de la calle, en vez de caer a una X aleatoria entre 9.5 y 16.5
    // como antes -- que era justo lo que los dejaba sueltos, desalineados y
    // sin ninguna continuidad de manzana.
    const furnitureIdx = factories.map((_, i) => i).filter((i) => frontIdx.indexOf(i) === -1);
    for (const side of [-1, 1]) {
      const rot = side < 0 ? Math.PI : 0; // fachada (cara -X local) siempre hacia la calzada
      const perCluster = 2;
      for (let i = 0; i < perCluster; i++) {
        place(frontIdx[Math.floor(Math.random() * frontIdx.length)],
          side * ((FRONTAGE_X_BY_ZONE[biome] || 10.5) + Math.random() * 0.6), z - i * (OUTER_SPACING / perCluster), rot);
      }
      if (furnitureIdx.length) {
        const count = 1 + Math.floor(Math.random() * 2);
        for (let i = 0; i < count; i++) {
          place(furnitureIdx[Math.floor(Math.random() * furnitureIdx.length)],
            side * (7.1 + Math.random() * 1.5), z - i * 3.5 + (Math.random() - 0.5), rot);
        }
      }
    }
  }
  function ensureOuterProps() {
    while (lastOuterZ > SPAWN_Z) {
      spawnOuterCluster(lastOuterZ);
      lastOuterZ -= OUTER_SPACING;
    }
  }
  ensureOuterProps();

  // ---- Carteles "Welcome to [Ciudad]" cada cierta distancia recorrida,
  // como si fuera una gira de campana por EEUU. No usan pool (evento raro,
  // una vez cada 300-500 unidades) asi que se construyen y se destruyen
  // (dispose) al pasar, en vez de reciclarse. ----
  const citySigns = [];
  let cityIndex = 0;
  let nextSignAt = 260;
  function buildCitySign(name) {
    const g = new THREE.Group();
    const postMat = toon(0xd8dde3);
    for (const side of [-0.9, 0.9]) {
      const post = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.05, 2.2, 8), postMat);
      post.position.set(side, 1.1, 0);
      g.add(post);
    }
    const tex = makeCityTexture(name);
    const boardMat = tex ? new THREE.MeshBasicMaterial({ map: tex }) : toon(0x0a3d1f);
    const board = new THREE.Mesh(new THREE.PlaneGeometry(2.2, 0.75), boardMat);
    board.position.set(0, 1.95, 0);
    g.add(board);
    const boardBack = new THREE.Mesh(new THREE.PlaneGeometry(2.2, 0.75), toon(0x0a3d1f));
    boardBack.position.set(0, 1.95, -0.02);
    boardBack.rotation.y = Math.PI;
    g.add(boardBack);
    return g;
  }
  function disposeCitySign(sign) {
    group.remove(sign);
    sign.traverse((o) => {
      if (o.isMesh) {
        if (o.material.map) o.material.map.dispose();
        o.material.dispose();
      }
    });
  }
  function maybeSpawnSign() {
    // Con una zona fija elegida a proposito (ej. Washington D.C.), no tiene
    // sentido seguir mostrando carteles de "Welcome to" de otras ciudades
    // al azar -- esos carteles son parte de la gira de campana en modo
    // automatico, no de una zona fija.
    if (forcedZone) return;
    if (totalScrolled < nextSignAt) return;
    nextSignAt += 320 + Math.random() * 160;
    const name = US_CITIES[cityIndex % US_CITIES.length];
    cityIndex++;
    const side = Math.random() < 0.5 ? -1 : 1;
    const sign = buildCitySign(name);
    sign.position.set(side * 5.6, 0, SPAWN_Z - 3);
    sign.rotation.y = side > 0 ? Math.PI * 0.18 : -Math.PI * 0.18;
    group.add(sign);
    citySigns.push(sign);
  }

  // ---- Obstaculos tematicos ----
  const obstacles = [];
  const tacos = [];

  const metalMat = toon(0xd6dce6);
  const darkMat = toon(0x20222c);
  const guardSuitMat = toon(0x1a1c22);
  const guardHeadMat = toon(0x2a2a2e);
  const bannerRedMat = toon(0xe0272c);
  const bannerBlueMat = toon(0x2f6bff);
  const podiumMat = toon(0x2251c9);

  function buildBarrier() {
    // LOW: valla de seguridad, se salta
    const g = new THREE.Group();
    for (const side of [-0.55, 0.55]) {
      const post = new THREE.Mesh(new THREE.CylinderGeometry(0.045, 0.045, 0.55, 12), metalMat);
      post.position.set(side, 0.28, 0);
      g.add(post);
      const cap = new THREE.Mesh(new THREE.SphereGeometry(0.06, 10, 8), goldMat);
      cap.position.set(side, 0.56, 0);
      g.add(cap);
    }
    const bar = new THREE.Mesh(new THREE.BoxGeometry(1.3, 0.07, 0.07), metalMat);
    bar.position.y = 0.48;
    withOutline(bar, 1.15);
    g.add(bar);
    const bar2 = new THREE.Mesh(new THREE.BoxGeometry(1.3, 0.06, 0.06), metalMat);
    bar2.position.y = 0.2;
    g.add(bar2);
    const stripeGeo2 = new THREE.BoxGeometry(0.14, 0.09, 0.09);
    for (let i = 0; i < 7; i++) {
      const c = i % 2 === 0 ? darkMat : goldMat;
      const seg = new THREE.Mesh(stripeGeo2, c);
      seg.position.set(-0.56 + i * 0.19, 0.34, 0);
      g.add(seg);
    }
    return g;
  }

  function buildBanner() {
    // HIGH: pancarta colgante, se desliza por debajo
    const g = new THREE.Group();
    for (const side of [-0.68, 0.68]) {
      const pole = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.04, 1.75, 12), metalMat);
      pole.position.set(side, 0.875, 0);
      g.add(pole);
    }
    const bannerL = new THREE.Mesh(new THREE.BoxGeometry(0.65, 0.32, 0.06), bannerRedMat);
    bannerL.position.set(-0.34, 1.55, 0);
    withOutline(bannerL, 1.1);
    g.add(bannerL);
    const bannerR = new THREE.Mesh(new THREE.BoxGeometry(0.65, 0.32, 0.06), bannerBlueMat);
    bannerR.position.set(0.34, 1.55, 0);
    withOutline(bannerR, 1.1);
    g.add(bannerR);
    const trim = new THREE.Mesh(new THREE.BoxGeometry(1.36, 0.05, 0.08), goldMat);
    trim.position.y = 1.72;
    g.add(trim);
    for (let i = 0; i < 3; i++) {
      const star = new THREE.Mesh(new THREE.SphereGeometry(0.045, 10, 8), goldMat);
      star.position.set(0.34 + (i - 1) * 0.16, 1.55, 0.035);
      g.add(star);
    }
    return g;
  }

  function buildPodiumGuard() {
    // FULL: atril + guardaespaldas generico, obliga a cambiar de carril
    const g = new THREE.Group();
    const podium = new THREE.Mesh(new THREE.BoxGeometry(0.62, 0.85, 0.42), podiumMat);
    podium.position.set(0, 0.425, 0.35);
    withOutline(podium, 1.08);
    g.add(podium);
    const emblem = new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.12, 0.02, 16), goldMat);
    emblem.rotation.x = Math.PI / 2;
    emblem.position.set(0, 0.55, 0.57);
    g.add(emblem);

    const micStand = new THREE.Mesh(new THREE.CylinderGeometry(0.02, 0.02, 0.3, 10), metalMat);
    micStand.position.set(0.18, 0.98, 0.5);
    micStand.rotation.z = -0.3;
    g.add(micStand);
    const micHead = new THREE.Mesh(new THREE.SphereGeometry(0.06, 12, 10), darkMat);
    micHead.position.set(0.29, 1.1, 0.5);
    g.add(micHead);

    const guardBody = new THREE.Mesh(new THREE.BoxGeometry(0.5, 0.95, 0.34), guardSuitMat);
    guardBody.position.set(0, 0.55, -0.25);
    withOutline(guardBody, 1.08);
    g.add(guardBody);
    const guardHead = new THREE.Mesh(new THREE.SphereGeometry(0.17, 12, 10), guardHeadMat);
    guardHead.position.set(0, 1.14, -0.25);
    withOutline(guardHead, 1.08);
    g.add(guardHead);
    return g;
  }

  const obstaclePools = {
    low: makePool(buildBarrier),
    high: makePool(buildBanner),
    full: makePool(buildPodiumGuard),
  };

  // ---- Obstaculos de Blender, estilo Minion Rush (blender/obstaculos.py, 22/10/2026) ----
  //   choque: como se esquiva (low = saltar, high = deslizarse, full = cambiar
  //     de carril, bus = subirse por la rampa o cambiar de carril)
  //   medio: medio largo a lo largo de la pista; centro: donde cae su centro
  //     respecto al origen (los vehiculos se modelaron hacia atras desde el morro)
  //   alto: por encima de esto se le pasa por encima saltando
  //   mueve: velocidad propia hacia el jugador (el coche patrulla)
  const TIPOS = {
    barricada: { choque: "low", medio: 0.45, alto: 0.95 },
    conos: { choque: "low", medio: 0.45, alto: 0.75 },
    pancarta: { choque: "high", medio: 0.45, alto: 2.5 },
    globos: { choque: "high", medio: 0.45, alto: 2.4 },
    guardaespaldas: { choque: "full", medio: 0.75, alto: 2.4, centro: 0 },
    furgoneta: { choque: "full", medio: 1.3, alto: 2.8, centro: -1.3 },
    patrulla: { choque: "full", medio: 1.3, alto: 1.2, centro: -1.3, mueve: 7 },
    autobus: { choque: "bus", alto: 1.55 },
    // Lo lanza el jefe: cae del cielo y rueda hacia el jugador. Se salta.
    barril: { choque: "low", medio: 0.5, alto: 0.9, mueve: 4 },
  };
  // 27/10: los de cada ciudad (blender/obstaculos2.py). Si alguno no carga,
  // se usan los de siempre.
  const TIPOS_LOCALES = {
    taxi: { choque: "full", medio: 1.4, alto: 1.5, centro: -1.4 },
    alcantarilla: { choque: "low", medio: 0.55, alto: 0.8 },
    andamio: { choque: "high", medio: 0.45, alto: 2.5 },
    contenedor: { choque: "full", medio: 1.15, alto: 1.35, centro: -1.15 },
    paca: { choque: "low", medio: 0.45, alto: 0.9 },
    tractor: { choque: "full", medio: 1.35, alto: 2.2, centro: -1.35 },
    carroza: { choque: "full", medio: 1.75, alto: 2.5, centro: -1.75 },
    guirnalda: { choque: "high", medio: 0.3, alto: 2.5 },
    valla_metal: { choque: "low", medio: 0.4, alto: 0.95 },
    protesta: { choque: "high", medio: 0.35, alto: 2.2 },
    agentes: { choque: "full", medio: 0.5, alto: 2.1, centro: 0 },
    suv: { choque: "full", medio: 1.5, alto: 1.6, centro: -1.5, mueve: 7 },
  };
  const DE_TIPO = { low: ["barricada", "conos"], high: ["pancarta", "globos"], full: ["guardaespaldas", "furgoneta"] };
  const BUS_RAMPA = 2.2, BUS_LARGO = 10.2, BUS_TECHO = 1.55;
  const USAR_BLENDER = Object.keys(TIPOS).every((n) => hayModelo("obstaculos/" + n)) && hayModelo("obstaculos/gorra");
  for (const n in TIPOS_LOCALES) if (USAR_BLENDER && hayModelo("obstaculos/" + n)) TIPOS[n] = TIPOS_LOCALES[n];
  const EXTRAS = ["rayo", "cohete", "chile", "jefe"].every((n) => hayModelo("obstaculos/" + n));

  // Sombra suave bajo cada obstaculo: lo "asienta" en el suelo y ayuda a
  // calcular la distancia, que era lo que mas costaba al verlos venir.
  const sombraTex = (() => {
    if (typeof document === "undefined") return null;
    const c = document.createElement("canvas");
    c.width = c.height = 64;
    const ctx = c.getContext("2d");
    const g = ctx.createRadialGradient(32, 32, 4, 32, 32, 32);
    g.addColorStop(0, "rgba(0,0,0,0.55)");
    g.addColorStop(1, "rgba(0,0,0,0)");
    ctx.fillStyle = g;
    ctx.fillRect(0, 0, 64, 64);
    return new THREE.CanvasTexture(c);
  })();
  const sombraMat = new THREE.MeshBasicMaterial({ map: sombraTex, transparent: true, depthWrite: false, opacity: 0.85 });
  const sombraGeo = new THREE.PlaneGeometry(1, 1);
  sombraGeo.rotateX(-Math.PI / 2);

  // Luces de la sirena del coche patrulla, que parpadean (van aparte del modelo).
  const sirenaRoja = new THREE.MeshBasicMaterial({ color: 0xff2a2a });
  const sirenaAzul = new THREE.MeshBasicMaterial({ color: 0x2a6bff });
  const sirenaGeo = new THREE.BoxGeometry(0.28, 0.12, 0.2);

  function construirObstaculo(nombre) {
    const g = modeloConContorno("obstaculos/" + nombre);
    const m = medidas("obstaculos/" + nombre);
    const sombra = new THREE.Mesh(sombraGeo, sombraMat);
    sombra.scale.set(m.ancho * 1.15, 1, m.fondo * 1.1 + 0.4);
    sombra.position.set(0, 0.075, m.frente - m.fondo / 2);
    g.add(sombra);
    if (nombre === "patrulla") {
      const roja = new THREE.Mesh(sirenaGeo, sirenaRoja);
      const azul = new THREE.Mesh(sirenaGeo, sirenaAzul);
      roja.position.set(-0.2, 1.22, -1.4);
      azul.position.set(0.2, 1.22, -1.4);
      g.add(roja, azul);
      g.userData.sirena = [roja, azul];
    }
    if (nombre === "suv") {
      // Las luces de la comitiva, en la calandra (rojas y azules, alternas).
      const roja = new THREE.Mesh(sirenaGeo, sirenaRoja);
      const azul = new THREE.Mesh(sirenaGeo, sirenaAzul);
      roja.scale.set(0.8, 0.8, 0.4); azul.scale.set(0.8, 0.8, 0.4);
      roja.position.set(-0.28, 0.58, 0.06);
      azul.position.set(0.28, 0.58, 0.06);
      g.add(roja, azul);
      g.userData.sirena = [roja, azul];
    }
    if (nombre === "alcantarilla") {
      // El vapor que sale de la alcantarilla: tres bocanadas que suben y se deshacen.
      const vapor = [];
      for (let i = 0; i < 3; i++) {
        const s = new THREE.Sprite(vaporMat.clone());
        s.position.set(0, 0.4, 0);
        g.add(s);
        vapor.push(s);
      }
      g.userData.vapor = vapor;
    }
    return g;
  }
  // Textura de una bocanada de vapor (redonda, blanca y difuminada).
  const vaporMat = new THREE.SpriteMaterial({
    map: (() => {
      if (typeof document === "undefined") return null;
      const c = document.createElement("canvas");
      c.width = c.height = 64;
      const x = c.getContext("2d");
      const gr = x.createRadialGradient(32, 32, 2, 32, 32, 32);
      gr.addColorStop(0, "rgba(255,255,255,0.9)");
      gr.addColorStop(0.5, "rgba(245,248,252,0.5)");
      gr.addColorStop(1, "rgba(240,244,250,0)");
      x.fillStyle = gr; x.fillRect(0, 0, 64, 64);
      return new THREE.CanvasTexture(c);
    })(),
    transparent: true, depthWrite: false,
  });
  if (USAR_BLENDER) {
    for (const nombre in TIPOS) obstaclePools[nombre] = makePool(() => construirObstaculo(nombre));
  }

  function spawnObstacle(lane, type, z, nombre) {
    const pool = USAR_BLENDER ? (nombre || DE_TIPO[type][Math.floor(Math.random() * DE_TIPO[type].length)]) : type;
    const t = USAR_BLENDER ? TIPOS[pool] : { medio: 0.7, alto: type === "low" ? 0.6 : 3 };
    const obj = obstaclePools[pool].acquire();
    obj.visible = true;
    obj.position.set(LANE_X[lane], 0, z);
    obj.rotation.set(0, 0, 0);
    if (!obj.parent) group.add(obj);
    const o = { mesh: obj, lane, type: t.choque || type, pool, z, phase: Math.random() * Math.PI * 2,
      medio: t.medio || 0.7, centro: t.centro || 0, alto: t.alto, mueve: t.mueve || 0, smashed: null };
    obstacles.push(o);
    return o;
  }

  // Altura del suelo bajo el jugador en un carril: la rampa y el techo del
  // autobus. `d` es cuanto se ha metido el jugador desde el pie de la rampa.
  function surfaceAt(x) {
    let h = 0;
    for (const o of obstacles) {
      if (o.type !== "bus" || o.smashed) continue;
      if (Math.abs(x - LANE_X[o.lane]) > 0.85) continue;
      const d = o.z;
      if (d < 0 || d > BUS_LARGO) continue;
      h = Math.max(h, d < BUS_RAMPA ? BUS_TECHO * d / BUS_RAMPA : BUS_TECHO);
    }
    return h;
  }

  // Un obstaculo aplastado (modo gigante o escudo) sale volando dando vueltas.
  // ---- Frases (25/10/2026): un bocadillo enorme que sale volando por el
  // carril y tumba lo primero que pilla (o le da al Burrito-Bot). ----
  const texturasFrase = {};
  function texturaFrase(texto) {
    if (texturasFrase[texto]) return texturasFrase[texto];
    const c = document.createElement("canvas");
    c.width = 512; c.height = 192;
    const ctx = c.getContext("2d");
    ctx.fillStyle = "#ffffff"; ctx.strokeStyle = "#22304f"; ctx.lineWidth = 10;
    ctx.beginPath(); ctx.roundRect(12, 12, 488, 140, 60); ctx.fill(); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(200, 148); ctx.lineTo(170, 186); ctx.lineTo(250, 148); ctx.closePath(); ctx.fill(); ctx.stroke();
    ctx.fillStyle = "#ffffff"; ctx.fillRect(196, 140, 58, 14);
    let tam = 74;
    ctx.font = `900 ${tam}px Fredoka, "Arial Rounded MT Bold", Arial, sans-serif`;
    while (ctx.measureText(texto).width > 440 && tam > 30) { tam -= 4; ctx.font = `900 ${tam}px Fredoka, Arial, sans-serif`; }
    ctx.textAlign = "center"; ctx.textBaseline = "middle";
    ctx.lineWidth = 8; ctx.strokeStyle = "#ffd23f"; ctx.strokeText(texto, 256, 84);
    ctx.fillStyle = "#e8463c"; ctx.fillText(texto, 256, 84);
    const tex = new THREE.CanvasTexture(c);
    tex.colorSpace = THREE.SRGBColorSpace;
    texturasFrase[texto] = tex;
    return tex;
  }
  const frases = [];
  function primerObstaculo(lane, alcance) {
    let mejor = null;
    for (const o of obstacles) {
      if (o.smashed || o.lane !== lane || o.type === "bus") continue;
      const zc = o.z + (o.centro || 0);
      if (zc > 1 || zc < -alcance) continue;
      if (!mejor || zc > mejor.z + (mejor.centro || 0)) mejor = o;
    }
    return mejor;
  }
  function lanzarFrase(lane, texto, objetivo) {
    const sprite = new THREE.Sprite(new THREE.SpriteMaterial({ map: texturaFrase(texto), transparent: true, depthTest: false }));
    sprite.scale.set(4.2, 1.6, 1);
    sprite.position.set(LANE_X[lane], 2.6, -0.5);
    sprite.renderOrder = 5;
    group.add(sprite);
    frases.push({ sprite, lane, objetivo, t: 0 });
  }
  function actualizarFrases(dt) {
    for (let i = frases.length - 1; i >= 0; i--) {
      const f = frases[i];
      f.t += dt;
      const s = f.sprite;
      // Sale con un «pop» y vuela recto por el carril.
      const pop = Math.min(1, f.t * 6);
      s.scale.set(4.2 * pop, 1.6 * pop, 1);
      s.position.z -= 48 * dt;
      s.position.y = 2.6 + Math.sin(f.t * 10) * 0.08;
      let llego = false;
      if (f.objetivo === "jefe") {
        if (!jefeActivo()) llego = true;
        else {
          s.position.x += (jefe.x - s.position.x) * Math.min(1, dt * 6);
          if (s.position.z <= jefe.z + 1) { golpearJefe(); llego = true; }
        }
      } else if (f.objetivo && !f.objetivo.smashed) {
        if (s.position.z <= f.objetivo.z + (f.objetivo.centro || 0) + 0.5) { smash(f.objetivo); llego = true; }
      } else if (f.objetivo && f.objetivo.smashed) llego = true;
      if (llego || f.t > 1.4) {
        burstSparkles(s.position.x, s.position.y, s.position.z);
        group.remove(s);
        s.material.dispose();
        frases.splice(i, 1);
      }
    }
  }

  function smash(o) {
    if (o.smashed) return;
    const lado = LANE_X[o.lane] === 0 ? (Math.random() < 0.5 ? -1 : 1) : Math.sign(LANE_X[o.lane]);
    o.smashed = { vx: lado * (4 + Math.random() * 3), vy: 9 + Math.random() * 4, vz: -14 - Math.random() * 6,
      rx: (Math.random() - 0.5) * 9, ry: (Math.random() - 0.5) * 9, rz: (Math.random() - 0.5) * 9 };
    burstSparkles(o.mesh.position.x, 1, o.mesh.position.z);
  }

  // Rayo congelador: lo que hay delante a menos de `alcance` se mete en un
  // bloque de hielo, se para (el coche patrulla tambien) y al tocarlo se
  // rompe en vez de chocar. El autobus no se congela: es para subirse.
  function congelar(alcance) {
    let nuevos = 0;
    for (const o of obstacles) {
      if (o.congelado || o.smashed || o.type === "bus" || o.z < -alcance || o.z > 1) continue;
      o.congelado = true;
      o.mueve = 0;
      if (USAR_BLENDER && !o.hielo) {
        o.hielo = capaHielo("obstaculos/" + o.pool);
        if (o.hielo) o.mesh.add(o.hielo);
      }
      burstSparkles(o.mesh.position.x, 1, o.mesh.position.z);
      nuevos++;
    }
    return nuevos;
  }

  // Ritmo actual de la pista (unidades por segundo), para calcular por donde
  // se va a cruzar un coche que viene de frente con lo que ya hay en la pista.
  let ritmo = 17;

  // ---- Taco en 2D, como el del menu (26/10/2026) ----
  // Isidro: el de piezas 3D «parece de Playmobil». Ahora es un dibujo plano
  // tipo pegatina que siempre mira a la camara (el dibujo esta en pegatinas.js,
  // que tambien pinta la chapa de campaña y lo que sale en la interfaz).
  function texturaPegatina(nombre) {
    const tex = new THREE.CanvasTexture(lienzoPegatina(nombre));
    tex.colorSpace = THREE.SRGBColorSpace;
    tex.anisotropy = 4;
    return tex;
  }
  function texturaTaco() { return texturaPegatina("taco"); }
  function texturaChapa() { return texturaPegatina("chapa"); }
  const tacoMat = typeof document !== "undefined"
    ? new THREE.SpriteMaterial({ map: texturaTaco(), transparent: true, alphaTest: 0.05, fog: true })
    : new THREE.SpriteMaterial({ color: 0xffc94d });
  function texturaBrillo() {
    const c = document.createElement("canvas");
    c.width = c.height = 64;
    const x = c.getContext("2d");
    const g = x.createRadialGradient(32, 32, 0, 32, 32, 32);
    g.addColorStop(0, "rgba(255,240,170,1)"); g.addColorStop(0.5, "rgba(255,226,122,0.6)"); g.addColorStop(1, "rgba(255,226,122,0)");
    x.fillStyle = g; x.fillRect(0, 0, 64, 64);
    return new THREE.CanvasTexture(c);
  }
  const tacoGlowMat = new THREE.SpriteMaterial({ map: typeof document !== "undefined" ? texturaBrillo() : null, color: 0xffffff, transparent: true, opacity: 0.55, depthWrite: false, fog: true });

  function buildTaco() {
    const g = new THREE.Group();
    // 27/10: sin el brillo de detras (quedaba tapado por el propio taco y
    // costaba otra llamada de dibujo por cada taco de la pista).
    g.userData.glow = null;
    const taco = new THREE.Sprite(tacoMat);
    taco.scale.setScalar(0.95);
    g.add(taco);
    return g;
  }

  function randomizeTacoLumps() {}

  const tacoPool = makePool(buildTaco);

  function spawnTaco(lane, z, y) {
    const mesh = tacoPool.acquire();
    randomizeTacoLumps(mesh);
    mesh.visible = true;
    mesh.rotation.y = 0;
    mesh.position.set(LANE_X[lane], y || 0.9, z);
    if (!mesh.parent) group.add(mesh);
    tacos.push({ mesh, lane, z, baseY: y || 0.9, phase: Math.random() * Math.PI * 2, collected: false });
  }

  // ---- Chispas al recoger un taco (pool reciclado) ----
  const sparkleMat = new THREE.MeshBasicMaterial({ color: 0xffe27a, transparent: true });
  const sparkleGeo = new THREE.OctahedronGeometry(0.045, 0);
  const sparklePool = makePool(() => new THREE.Mesh(sparkleGeo, sparkleMat.clone()));
  const activeSparkles = [];
  function burstSparkles(x, y, z) {
    const count = 6;
    for (let i = 0; i < count; i++) {
      const m = sparklePool.acquire();
      m.visible = true;
      m.position.set(x, y, z);
      m.scale.setScalar(1);
      m.material.opacity = 1;
      if (!m.parent) group.add(m);
      const angle = (i / count) * Math.PI * 2;
      activeSparkles.push({
        mesh: m,
        vx: Math.cos(angle) * 0.9,
        vy: 1.1 + Math.random() * 0.6,
        vz: Math.sin(angle) * 0.9,
        life: 0.45,
        maxLife: 0.45,
      });
    }
  }

  // ---- Power-ups: Orden Ejecutiva (escudo), Iman Dorado, Covfefe Boost ----
  const powerups = [];
  const magnetMat = toon(0xff2d2d);
  // Flechas de boost pegadas al suelo (antes un cono flotante que giraba en
  // el aire, poco reconocible como "acelera"). Forma de chevron real via
  // Shape/ShapeGeometry -- no cajas rotadas a ojo -- tumbada sobre la pista y
  // apuntando hacia delante, como un boost pad de un arcade de carreras.
  const boostArrowMat = toon(0xffa53d, { emissive: 0x5c2600 });
  const chevronShape = new THREE.Shape();
  chevronShape.moveTo(0, 0.34);
  chevronShape.lineTo(0.3, -0.14);
  chevronShape.lineTo(0.16, -0.14);
  chevronShape.lineTo(0, 0.06);
  chevronShape.lineTo(-0.16, -0.14);
  chevronShape.lineTo(-0.3, -0.14);
  chevronShape.closePath();
  const chevronGeo = new THREE.ShapeGeometry(chevronShape);

  function buildPowerupIcon(kind) {
    const g = new THREE.Group();
    if (kind === "shield") {
      const ico = new THREE.Mesh(new THREE.OctahedronGeometry(0.24, 0), goldMat);
      withOutline(ico, 1.12);
      g.add(ico);
    } else if (kind === "magnet") {
      const horseshoe = new THREE.Mesh(new THREE.TorusGeometry(0.2, 0.08, 8, 12, Math.PI * 1.3), magnetMat);
      horseshoe.rotation.z = Math.PI * 0.35;
      withOutline(horseshoe, 1.12);
      g.add(horseshoe);
      for (const side of [-1, 1]) {
        const tip = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.08, 0.08), goldMat);
        tip.position.set(side * 0.17, -0.15, 0);
        g.add(tip);
      }
    } else {
      const chevrons = [];
      for (let i = 0; i < 3; i++) {
        const chevron = new THREE.Mesh(chevronGeo, boostArrowMat);
        chevron.rotation.x = -Math.PI / 2;
        chevron.position.z = i * 0.4;
        chevron.userData.baseZ = i * 0.4;
        g.add(chevron);
        chevrons.push(chevron);
      }
      g.userData.chevrons = chevrons;
    }
    return g;
  }

  const powerupPools = {
    shield: makePool(() => buildPowerupIcon("shield")),
    magnet: makePool(() => buildPowerupIcon("magnet")),
    boost: makePool(() => buildPowerupIcon("boost")),
    // Gorra roja de campaña: el modo gigante (el "Mega Minion" de Minion Rush).
    mega: makePool(() => {
      const g = modeloConContorno("obstaculos/gorra") || buildPowerupIcon("shield");
      g.scale.setScalar(1.5);
      return g;
    }),
    // 22/10 (2): rayo congelador, cohete y el chile para darle al jefe.
    freeze: makePool(() => { const g = modeloConContorno("obstaculos/rayo") || buildPowerupIcon("shield"); g.scale.setScalar(1.3); return g; }),
    rocket: makePool(() => { const g = modeloConContorno("obstaculos/cohete") || buildPowerupIcon("boost"); g.scale.setScalar(0.42); return g; }),
    // 25/10: microfono dorado, la carga para lanzar una frase.
    micro: makePool(() => {
      const g = new THREE.Group();
      const oro = toon(0xf2c23a, { emissive: 0x3a2a00 });
      const rejilla = new THREE.Mesh(new THREE.SphereGeometry(0.2, 16, 12), toon(0xd9dde3, { emissive: 0x222222 }));
      rejilla.position.y = 0.32;
      const aro = new THREE.Mesh(new THREE.TorusGeometry(0.2, 0.035, 8, 20), oro);
      aro.position.y = 0.32; aro.rotation.x = Math.PI / 2;
      const mango = new THREE.Mesh(new THREE.CylinderGeometry(0.07, 0.05, 0.5, 12), oro);
      mango.position.y = -0.05;
      g.add(rejilla, aro, mango);
      g.rotation.z = 0.35;
      g.scale.setScalar(1.4);
      return g;
    }),
    chile: makePool(() => { const g = modeloConContorno("obstaculos/chile") || buildPowerupIcon("shield"); g.scale.setScalar(1.4); g.position.y = -0.4; return g; }),
  };

  function spawnPowerup(lane, z, kind) {
    const mesh = powerupPools[kind].acquire();
    mesh.visible = true;
    mesh.rotation.y = 0;
    mesh.position.set(LANE_X[lane], kind === "boost" ? 0.02 : 1.0, z);
    if (!mesh.parent) group.add(mesh);
    powerups.push({ mesh, lane, z, kind, collected: false });
  }

  let lastRowZ = -14;

  // Arranque limpio: los primeros 3 segundos de CADA partida no traen ningun
  // obstaculo (antes traian la mitad de lo normal, que aun asi podia poner uno
  // encima nada mas empezar). 3 s a la velocidad inicial de 17 u/s son 51
  // unidades, de ahi el -52: un obstaculo situado en z=-51 tardaria justo esos
  // 3 s en llegar al jugador, que esta en z=0.
  // Solo afecta al relleno inicial: una vez rodando, las filas nuevas nacen en
  // SPAWN_Z (-128), muy por debajo de este umbral, y usan la probabilidad
  // normal. Los tacos si siguen apareciendo en este tramo (ver rama `else`),
  // asi que la salida no queda vacia.
  const EASY_ZONE_Z = -52;
  // Carril del autobus y cuantas filas mas ocupa (mide 10.2: la suya y las
  // dos siguientes). En esas filas no se pone nada mas en su carril.
  let busCarril = -1, busFilas = 0;

  // ¿Puede salir un coche patrulla en `lane` desde `z`? Viene de frente mas
  // rapido que la pista, asi que adelanta a las filas que ya hay delante: su
  // carril tiene que estar libre en todas ellas, y no puede cruzarse cerca del
  // jugador con una fila que ya tape los otros dos carriles.
  function cocheCabe(lane, z, mueve) {
    for (const o of obstacles) {
      if (o.smashed || o.z <= z) continue;
      if (o.lane === lane) return false;
    }
    const filas = {};
    for (const o of obstacles) {
      if (o.smashed || o.z <= z || o.type !== "full") continue;
      (filas[o.z] = filas[o.z] || new Set()).add(o.lane);
    }
    for (const fz in filas) {
      if (filas[fz].size < 2) continue;
      const t = (Number(fz) - z) / mueve;
      const cruce = Number(fz) + ritmo * t;
      if (cruce > -30 && cruce < 3) return false;
    }
    return true;
  }

  function arcoDeTacos(lane, z) {
    // Tacos en arco por encima de lo que se salta, como los platanos de Minion Rush.
    for (let i = -2; i <= 2; i++) spawnTaco(lane, z - i * 1.1, 0.9 + 1.25 * (1 - (i * i) / 5));
  }

  // ---- Cohete: mientras se vuela, las filas nuevas son tacos en el cielo ----
  let cielo = false, carrilCielo = 1;
  function setCielo(v) {
    // Al despegar se llena de tacos el cielo de delante: si no, los primeros
    // tardarian 5 s en llegar desde el horizonte y el vuelo dura 6.5.
    if (v && !cielo) {
      for (let z = -10; z > lastRowZ; z -= 1.4) {
        if (Math.random() < 0.12) carrilCielo = Math.max(0, Math.min(2, carrilCielo + (Math.random() < 0.5 ? -1 : 1)));
        spawnTaco(carrilCielo, z, CIELO_Y + 0.9);
      }
    }
    cielo = v;
  }

  // ---- Jefe: el Burrito-Bot (22/10/2026) ----
  // Como los jefes de Minion Rush: flota delante, lanza barriles de salsa al
  // carril donde estas y se le vence recogiendo chiles, que salen disparados
  // hacia el. Cinco golpes. Si tarda demasiado, se va sin premio.
  const JEFE_VIDA = 5, JEFE_Z = -34, JEFE_Y = 2.6, JEFE_TIEMPO = 40;
  const jefe = { activo: false, mesh: null, vida: 0, carril: 1, x: 0, z: -90, tiro: 0, tiempo: 0,
    golpe: 0, saliendo: false, derrotado: false };
  const disparos = [];
  let jugadorCarril = 1;
  let alEventoJefe = null;
  function setJugador(l) { jugadorCarril = l; }
  function onJefe(fn) { alEventoJefe = fn; }
  function jefeActivo() { return jefe.activo && !jefe.saliendo; }
  // En un nivel, al acabarse su tramo se va (sin premio).
  function despedirJefe() {
    if (!jefeActivo()) return;
    jefe.saliendo = true;
    if (alEventoJefe) alEventoJefe("escapa", 0);
  }
  function iniciarJefe() {
    if (jefe.activo || !EXTRAS) return false;
    if (!jefe.mesh) jefe.mesh = modeloConContorno("obstaculos/jefe");
    jefe.mesh.visible = true;
    jefe.mesh.rotation.set(0, 0, 0);
    if (!jefe.mesh.parent) group.add(jefe.mesh);
    Object.assign(jefe, { activo: true, vida: JEFE_VIDA, carril: 1, x: 0, z: -95, tiempo: 0, golpe: 0,
      saliendo: false, derrotado: false,
      // El primer barril espera a que pase lo que ya estaba en la pista
      // (hasta 128 por delante): asi nunca coincide con un obstaculo normal.
      tiro: 5.5 });
    return true;
  }
  const chileGeo = () => modelo("obstaculos/chile");
  function dispararJefe(x, y) {
    if (!jefeActivo()) return;
    const m = chileGeo();
    m.scale.setScalar(1.6);
    m.position.set(x, y, 0);
    group.add(m);
    disparos.push({ mesh: m, t: 0, x0: x, y0: y });
  }
  function acabarJefe() {
    if (jefe.mesh) jefe.mesh.visible = false;
    jefe.activo = false;
    for (const d of disparos) group.remove(d.mesh);
    disparos.length = 0;
  }
  function actualizarJefe(dt) {
    if (!jefe.activo) return;
    const m = jefe.mesh;
    jefe.tiempo += dt;
    if (jefe.saliendo) {
      // Vencido: sale despedido girando. Si se va por tiempo, se aleja volando.
      m.position.y += (jefe.derrotado ? 9 : 5) * dt;
      jefe.z -= (jefe.derrotado ? 10 : 25) * dt;
      if (jefe.derrotado) { m.rotation.z += dt * 6; m.rotation.x += dt * 3; }
      m.position.z = jefe.z;
      if (m.position.y > 30) acabarJefe();
      return;
    }
    jefe.z += (JEFE_Z - jefe.z) * Math.min(1, dt * 1.2);
    jefe.x += (LANE_X[jefe.carril] - jefe.x) * Math.min(1, dt * 4);
    const temblor = jefe.golpe > 0 ? Math.sin(jefe.tiempo * 70) * 0.25 * jefe.golpe : 0;
    m.position.set(jefe.x + temblor, JEFE_Y + Math.sin(jefe.tiempo * 2.2) * 0.25, jefe.z);
    m.rotation.z = Math.sin(jefe.tiempo * 1.7) * 0.06;
    if (jefe.golpe > 0) {
      jefe.golpe = Math.max(0, jefe.golpe - dt * 2.5);
      m.scale.setScalar(1 + jefe.golpe * 0.25);
    }
    // Lanza un barril al carril donde esta (casi siempre el tuyo) y cambia de carril.
    jefe.tiro -= dt;
    if (jefe.tiro <= 0 && jefe.z > JEFE_Z - 6) {
      const o = spawnObstacle(jefe.carril, "low", jefe.z + 1.5, "barril");
      o.cae = { vy: 2 };
      o.mesh.position.y = JEFE_Y;
      jefe.carril = Math.random() < 0.6 ? jugadorCarril : Math.floor(Math.random() * 3);
      jefe.tiro = 1.6;
    }
    if (jefe.tiempo > JEFE_TIEMPO) {
      jefe.saliendo = true;
      if (alEventoJefe) alEventoJefe("escapa", 0);
    }
  }
  function actualizarDisparos(dt) {
    for (let i = disparos.length - 1; i >= 0; i--) {
      const d = disparos[i];
      d.t += dt / 0.45;
      const t = Math.min(1, d.t);
      d.mesh.position.set(d.x0 + (jefe.x - d.x0) * t, d.y0 + (JEFE_Y + 1.5 - d.y0) * t + Math.sin(t * Math.PI) * 2,
        jefe.z * t);
      d.mesh.rotation.x += dt * 12;
      if (t >= 1) {
        group.remove(d.mesh);
        disparos.splice(i, 1);
        golpearJefe();
      }
    }
  }
  function golpearJefe() {
    if (!jefeActivo()) return;
    jefe.vida--;
    jefe.golpe = 1;
    for (let k = 0; k < 3; k++) burstSparkles(jefe.x, JEFE_Y + 1.5, jefe.z);
    if (jefe.vida <= 0) {
      jefe.saliendo = true; jefe.derrotado = true;
      if (alEventoJefe) alEventoJefe("derrotado", 0);
    } else if (alEventoJefe) alEventoJefe("golpe", jefe.vida);
  }

  // ================================================================
  // ---- La pista por tramos (27/10/2026) ----
  // Antes cada fila salia al azar de principio a fin y todo el nivel era
  // igual. Ahora el nivel va por partes (levels.js: tramos), cada una con su
  // forma: un respiro de tacos, vallas, slalom, autobuses, lo propio de cada
  // ciudad, el jefe y el sprint final. El sin fin encadena tramos al azar.
  // Cada fila de un nivel sale de su propia semilla (la de su metro), asi que
  // al seguir desde el punto de control la calle es la misma.
  // ================================================================
  const LANES = [0, 1, 2];
  const elegirDe = (l) => l[Math.floor(Math.random() * l.length)];
  // Obstaculos de cada sitio: los del nivel, o los de la zona en el sin fin.
  const LOCALES_ZONA = {
    city: { low: ["conos", "barricada", "alcantarilla"], high: ["pancarta", "andamio", "globos"], full: ["taxi", "taxi", "furgoneta", "contenedor", "guardaespaldas"] },
    town: { low: ["paca", "paca", "conos", "barricada"], high: ["guirnalda", "pancarta", "globos"], full: ["tractor", "carroza", "furgoneta"] },
    dc: { low: ["valla_metal", "barricada", "conos"], high: ["protesta", "pancarta", "globos"], full: ["agentes", "furgoneta", "guardaespaldas"] },
    desert: DE_TIPO,
  };
  // El carril que ocupa un autobus de la fila anterior: ahi no se pone nada.
  let carrilOcupado = -1;
  function nombreObstaculo(type, d, lista) {
    const deNivel = nivel && nivel.obstaculos ? nivel.obstaculos[type] : null;
    const set = lista || deNivel || (LOCALES_ZONA[currentZoneName(d)] || DE_TIPO)[type] || DE_TIPO[type];
    const vale = set.filter((n) => obstaclePools[n]);
    return elegirDe(vale.length ? vale : DE_TIPO[type]);
  }
  // Carril que se deja libre un trecho (detras de una chapa escondida).
  let reserva = null;
  function obst(lane, type, z, d, lista) {
    if (lane === carrilOcupado) return null;
    if (reserva && lane === reserva.lane && d > reserva.desde && d <= reserva.hasta) return null;
    return spawnObstacle(lane, type, z, USAR_BLENDER ? nombreObstaculo(type, d, lista) : undefined);
  }
  function tacosEn(lane, z, n = 4, y = 0.9, paso = 1.1) {
    if (lane === carrilOcupado) return;
    for (let i = 0; i < n; i++) spawnTaco(lane, z - i * paso, y);
  }

  // Autobus de campaña con rampa: subirse y correr por el techo lleno de tacos.
  // `chapa`: en vez del ultimo taco del techo, una chapa escondida.
  function filaBus(z, d, lane, chapa) {
    spawnObstacle(lane, "bus", z, "autobus");
    busCarril = lane; busFilas = 2;
    const n = chapa !== undefined ? 6 : 7;
    for (let i = 0; i < n; i++) spawnTaco(lane, z - BUS_RAMPA - 0.6 - i * 1.15, BUS_TECHO + 0.9);
    if (chapa !== undefined) spawnChapa(lane, z - BUS_RAMPA - 0.6 - 6 * 1.15 - 0.4, BUS_TECHO + 1.0, chapa);
    const otros = LANES.filter((l) => l !== lane);
    const lado = elegirDe(otros);
    obst(lado, Math.random() < 0.5 ? "full" : "low", z, d);
    otros.filter((l) => l !== lado).forEach((l) => tacosEn(l, z, 1));
  }

  // La fila de siempre (al azar), con la densidad que diga el tramo.
  function filaMixta(z, d, densidad) {
    const roll = Math.random();
    const ocupado = carrilOcupado;
    const coche = (nivel && nivel.coche) || "patrulla";
    if (USAR_BLENDER && !(nivel && nivel.sinBus) && roll < densidad && ocupado < 0 && d > 220 && Math.random() < 0.12) {
      filaBus(z, d, Math.floor(Math.random() * 3));
      return;
    }
    if (USAR_BLENDER && !(nivel && nivel.sinPatrulla) && roll < densidad && d > 300 && Math.random() < 0.1) {
      const opciones = LANES.filter((l) => l !== ocupado && cocheCabe(l, z, TIPOS[coche].mueve));
      if (opciones.length) {
        const lane = elegirDe(opciones);
        spawnObstacle(lane, "full", z, coche);
        LANES.filter((l) => l !== lane).forEach((l) => { if (Math.random() < 0.6) tacosEn(l, z, 1); });
        return;
      }
    }
    if (roll < densidad) {
      const libres = LANES.filter((l) => l !== ocupado);
      const blockCount = ocupado >= 0 ? 1 : (Math.random() < 0.5 ? 1 : 2);
      const blocked = libres.slice().sort(() => Math.random() - 0.5).slice(0, blockCount);
      blocked.forEach((lane) => {
        const typeRoll = Math.random();
        const type = typeRoll < 0.4 ? "low" : typeRoll < 0.75 ? "high" : "full";
        obst(lane, type, z, d);
        if (type === "low" && Math.random() < 0.45) arcoDeTacos(lane, z);
      });
      const free = libres.filter((l) => !blocked.includes(l));
      let powerupLane = null;
      if (Math.random() < 0.08 && free.length > 0) {
        powerupLane = elegirDe(free);
        const kinds = !USAR_BLENDER ? ["shield", "magnet", "boost"]
          : EXTRAS ? ["shield", "magnet", "boost", "mega", "freeze", "rocket"] : ["shield", "magnet", "boost", "mega"];
        spawnPowerup(powerupLane, z, elegirDe(nivel && nivel.potenciadores ? nivel.potenciadores : kinds));
      }
      if (powerupLane === null && free.length && USAR_BLENDER && Math.random() < 0.12) {
        powerupLane = elegirDe(free);
        spawnPowerup(powerupLane, z, "micro");
      }
      free.forEach((lane) => { if (lane !== powerupLane && Math.random() < 0.7) tacosEn(lane, z, 1); });
    } else {
      tacosEn(elegirDe(LANES.filter((l) => l !== ocupado)), z, 4);
    }
  }

  // Cada forma de tramo: (z de la fila, d = metro de la partida, el tramo, k = fila dentro del tramo).
  const SERPIENTE = [1, 1, 0, 0, 1, 1, 2, 2];
  const PATRONES = {
    // Un respiro: una hilera de tacos que va culebreando de carril.
    calma(z, d, t, k) {
      const lane = SERPIENTE[k % SERPIENTE.length];
      for (let i = 0; i < 5; i++) if (lane !== carrilOcupado) spawnTaco(lane, z - i * 1.4, 0.9 + Math.sin((k * 5 + i) * 0.45) * 0.25);
      if (k % 9 === 4 && USAR_BLENDER) spawnPowerup((lane + 1) % 3, z, "micro");
    },
    // El primer nivel enseña los gestos uno a uno (main.js pone el aviso).
    tutorial(z, d, t, k) {
      if (k === 8) { obst(1, "full", z, d); tacosEn(0, z); tacosEn(2, z); aviso(d, "carril"); }
      else if (k === 17) { for (const l of LANES) obst(l, "low", z, d); arcoDeTacos(1, z); aviso(d, "saltar"); }
      else if (k === 26) { for (const l of LANES) obst(l, "high", z, d); aviso(d, "agachar"); }
      else if (k === 34 && USAR_BLENDER) { spawnPowerup(1, z, "micro"); tacosEn(0, z, 3); tacosEn(2, z, 3); aviso(d, "frase"); }
      else if (k > 2 && ![7, 9, 16, 18, 25, 27, 33, 35].includes(k)) tacosEn(1, z, 4);
    },
    suave(z, d, t) { filaMixta(z, d, t.densidad || 0.4); },
    mixto(z, d, t) { filaMixta(z, d, t.densidad || 0.55); },
    // Filas enteras: o se salta, o se pasa agachado (o se elige carril).
    vallas(z, d, t, k) {
      if (k % 3 === 1) { tacosEn(Math.floor(Math.random() * 3), z, 3); return; }
      if (k % 3 === 2) return;
      const r = Math.random();
      if (r < 0.4) { for (const l of LANES) obst(l, "low", z, d, t.low); arcoDeTacos(Math.floor(Math.random() * 3), z); }
      else if (r < 0.75) { for (const l of LANES) obst(l, "high", z, d, t.high); tacosEn(Math.floor(Math.random() * 3), z - 1.5, 3, 0.6); }
      else {
        const tipos = ["low", "high", Math.random() < 0.5 ? "low" : "high"].sort(() => Math.random() - 0.5);
        LANES.forEach((l, i) => obst(l, tipos[i], z, d, tipos[i] === "high" ? t.high : t.low));
      }
    },
    // Dos carriles cerrados; el libre va cambiando de uno en uno.
    slalom(z, d, t, k) {
      if (k % 2 === 1) return;
      const seq = [1, 1, 0, 0, 1, 2, 2, 1, 0, 1, 2, 2];
      const libre = seq[(k / 2) % seq.length];
      for (const l of LANES) if (l !== libre) obst(l, "full", z, d, t.full);
      tacosEn(libre, z + 1.5, 4);
    },
    // Un autobus tras otro, cambiando de carril: se va de techo en techo.
    autobuses(z, d, t, k) {
      if (k % 4 === 0 && busFilas === 0 && USAR_BLENDER) filaBus(z, d, [1, 0, 2, 1, 2, 0][(k / 4) % 6]);
      else if (k % 4 === 2) {
        const l = elegirDe(LANES.filter((x) => x !== carrilOcupado));
        obst(l, Math.random() < 0.5 ? "low" : "high", z, d);
      }
    },
    // Un potenciador seguro y lluvia de tacos por los tres carriles.
    festin(z, d, t, k) {
      if (k === 1) {
        if (USAR_BLENDER || ["shield", "magnet", "boost"].includes(t.potenciador)) spawnPowerup(1, z, t.potenciador);
        tacosEn(0, z); tacosEn(2, z);
        return;
      }
      const valla = k > 4 && k % 4 === 0 ? Math.floor(Math.random() * 3) : -1;
      for (const l of LANES) {
        if (l === valla) { obst(l, "low", z, d); arcoDeTacos(l, z); } else tacosEn(l, z, 4);
      }
    },
    // El ultimo tramo: tacos en los tres carriles y obstaculos sueltos.
    sprint(z, d, t, k) {
      if (nivel && d > nivel.largo - 80) { tacosEn(1, z, 5, 0.9, 1.4); return; }
      const ob = k % 2 === 0 ? Math.floor(Math.random() * 3) : -1;
      for (const l of LANES) {
        if (l === ob) obst(l, Math.random() < 0.5 ? "low" : "high", z, d);
        else tacosEn(l, z, 4);
      }
    },
    // Nueva York: un carril cortado por obras que va cambiando, y alcantarillas.
    obras(z, d, t, k) {
      const bloque = Math.floor(k / 7), paso = k % 7;
      const cerrado = [0, 2, 1, 0, 2, 1][bloque % 6];
      if (paso <= 4) obst(cerrado, paso % 2 === 0 ? "full" : "low", z, d, paso % 2 === 0 ? ["contenedor"] : ["conos"]);
      const otros = LANES.filter((l) => l !== cerrado || paso > 4);
      if (paso === 2 || (t.low && paso === 4)) {
        const l = elegirDe(otros);
        obst(l, "low", z, d, t.low || ["alcantarilla"]);
        otros.filter((x) => x !== l).forEach((x) => tacosEn(x, z, 3));
      } else otros.forEach((l) => { if (Math.random() < 0.5) tacosEn(l, z, 3); });
    },
    // Findlay: el desfile de Flag City, carrozas y pacas de paja.
    desfile(z, d, t, k) {
      if (k % 3 === 0) {
        const p = [1, 0, 2, 1, 2, 0][(k / 3) % 6];
        obst(p, "full", z, d, ["carroza"]);
        const otros = LANES.filter((l) => l !== p);
        obst(otros[k % 2], "low", z, d, ["paca"]);
        tacosEn(otros[1 - (k % 2)], z, 4);
      } else if (k % 3 === 2 && Math.random() < 0.6) obst(Math.floor(Math.random() * 3), "high", z, d, ["guirnalda"]);
    },
    // Washington: la comitiva viene de frente y los agentes cortan el paso.
    comitiva(z, d, t, k) {
      if (k % 3 === 1) { tacosEn(Math.floor(Math.random() * 3), z, 3); return; }
      if (k % 3 === 2) return;
      const coche = obstaclePools.suv ? "suv" : "patrulla";
      const opciones = USAR_BLENDER ? LANES.filter((l) => l !== carrilOcupado && cocheCabe(l, z, TIPOS[coche].mueve)) : [];
      if (opciones.length) {
        const l = elegirDe(opciones);
        spawnObstacle(l, "full", z, coche);
        const otros = LANES.filter((x) => x !== l);
        if (Math.random() < 0.6) obst(elegirDe(otros), "full", z, d, ["agentes"]);
      } else obst(Math.floor(Math.random() * 3), "full", z, d, ["agentes"]);
    },
    // El Burrito-Bot: sin obstaculos normales (solo sus barriles), tacos y chiles.
    jefe(z, d, t, k) {
      const lane = Math.floor(Math.random() * 3);
      tacosEn(lane, z, 4);
      if (EXTRAS && Math.random() < 0.55) spawnPowerup((lane + 1 + Math.floor(Math.random() * 2)) % 3, z, "chile");
    },
  };

  // ---- Los tramos del nivel, o los del sin fin (al azar, se van añadiendo) ----
  let tramos = [];
  // Fuera de los tramos del nivel (el final de la calle): siempre el mismo objeto.
  const TRAMO_FINAL = { desde: 0, hasta: 1e9, tipo: "calma" }, TRAMO_MIXTO = { desde: 0, hasta: 1e9, tipo: "mixto" };
  const SIN_FIN = [["suave", 2], ["mixto", 4], ["slalom", 2], ["vallas", 2], ["autobuses", 2], ["festin", 1], ["calma", 1], ["local", 2]];
  const LOCAL_DE_ZONA = { city: "obras", town: "desfile", dc: "comitiva", desert: "mixto" };
  function prepararTramos() {
    tramos = nivel && nivel.tramos ? nivel.tramos.map(([desde, hasta, tipo, op]) => ({ desde, hasta, tipo, ...(op || {}) })) : [];
  }
  function tramoEn(d) {
    if (nivel) {
      for (const t of tramos) if (d >= t.desde && d < t.hasta) return t;
      return nivel.tramos ? TRAMO_FINAL : TRAMO_MIXTO;
    }
    while (!tramos.length || tramos[tramos.length - 1].hasta <= d) {
      const ant = tramos[tramos.length - 1];
      const desde = ant ? ant.hasta : 0;
      if (!ant) { tramos.push({ desde: 0, hasta: 150, tipo: "calma" }); continue; }
      let tipo;
      do {
        let r = Math.random() * SIN_FIN.reduce((n, [, p]) => n + p, 0);
        tipo = SIN_FIN.find(([, p]) => (r -= p) < 0)[0];
      } while (tipo === ant.tipo || (tipo === "calma" && ant.tipo === "festin") || (tipo === "festin" && ant.tipo === "calma"));
      if (tipo === "local") tipo = LOCAL_DE_ZONA[currentZoneName(desde + 150)] || "mixto";
      const corto = tipo === "calma" || tipo === "festin";
      const kinds = EXTRAS ? ["shield", "magnet", "boost", "mega", "freeze", "rocket"] : ["shield", "magnet", "boost"];
      tramos.push({ desde, hasta: desde + (corto ? 120 + Math.random() * 50 : 240 + Math.random() * 170), tipo,
        densidad: 0.45 + Math.min(0.2, desde / 12000), potenciador: elegirDe(kinds), titulo: tipo === "festin" ? "festin" : null });
      if (tramos.length > 40) tramos.splice(0, 10);
    }
    for (let i = tramos.length - 1; i >= 0; i--) if (d >= tramos[i].desde) return tramos[i];
    return tramos[0];
  }

  // ---- Avisos del tutorial: main.js los enseña un poco antes de llegar ----
  const avisos = [];
  function aviso(d, tipo) { avisos.push({ d, tipo }); }
  function tomarAviso(distancia) {
    const i = avisos.findIndex((a) => distancia >= a.d - 30);
    return i < 0 ? null : avisos.splice(i, 1)[0];
  }

  // ---- Chapas de campaña: tres escondidas en cada nivel ----
  const chapas = [];
  let chapasHechas = new Set();     // ya puestas (o cogidas antes del punto de control)
  const chapaPool = makePool(() => {
    const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: texturaChapa(), transparent: true, depthWrite: false }));
    s.scale.set(1.15, 1.15, 1);
    const brillo = new THREE.Sprite(new THREE.SpriteMaterial({ map: texturaBrillo(), color: 0xffe9a0, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending }));
    brillo.scale.set(2.2, 2.2, 1);
    brillo.renderOrder = -1;
    const g = new THREE.Group();
    g.add(brillo, s);
    g.userData.brillo = brillo;
    return g;
  });
  function spawnChapa(lane, z, y, idx) {
    if (lane === carrilOcupado && y < 1.5) return;
    const mesh = chapaPool.acquire();
    mesh.visible = true;
    mesh.position.set(LANE_X[lane], y, z);
    if (!mesh.parent) group.add(mesh);
    chapas.push({ mesh, lane, z, baseY: y, idx, collected: false, phase: Math.random() * 6 });
  }
  function filaChapa(z, d, tipo, idx) {
    if (tipo === "bus" && USAR_BLENDER && busFilas === 0) { filaBus(z, d, 1, idx); return; }
    if (tipo === "carril") {
      const l = Math.random() < 0.5 ? 0 : 2;
      const o = obst(l, "full", z, d);
      const atras = o ? o.centro - o.medio : -1.4;
      spawnChapa(l, z + atras - 3.6, 0.95, idx);
      reserva = { lane: l, desde: d, hasta: d + 15 };
      tacosEn(1, z + 1, 4);
      tacosEn(2 - l, z + 1, 2);
      return;
    }
    // arco: vallas en los tres carriles y la chapa alta sobre la del medio.
    for (const l of LANES) obst(l, "low", z, d);
    arcoDeTacos(0, z); arcoDeTacos(2, z);
    spawnChapa(1, z, 2.45, idx);
  }

  // Una fila de la pista a la distancia `d` de la partida.
  const SALIDA_LIMPIA_Z = -52;      // las primeras filas de cada salida, sin obstaculos
  function generarFila(z) {
    const d = totalScrolled - z;
    if (nivel && d > nivel.largo - 30) return;
    if (cielo) {
      // Volando en cohete: una hilera de tacos en el cielo que va cambiando de carril.
      if (Math.random() < 0.5) carrilCielo = Math.max(0, Math.min(2, carrilCielo + (Math.random() < 0.5 ? -1 : 1)));
      for (let i = 0; i < 5; i++) spawnTaco(carrilCielo, z - i * 1.4, CIELO_Y + 0.9);
      return;
    }
    carrilOcupado = busFilas > 0 ? busCarril : -1;
    if (busFilas > 0) busFilas--;
    try {
      if (!nivel && jefeActivo()) { PATRONES.jefe(z, d, null, 0); return; }
      if (z > SALIDA_LIMPIA_Z) { if (z < -20) PATRONES.calma(z, d, null, 0); return; }
      if (nivel && nivel.chapas) {
        const i = nivel.chapas.findIndex(([cd]) => Math.abs(cd - d) <= ROW_SPACING / 2);
        if (i >= 0 && !chapasHechas.has(i)) { chapasHechas.add(i); filaChapa(z, d, nivel.chapas[i][1], i); return; }
      }
      const t = tramoEn(d);
      const k = Math.round((d - t.desde) / ROW_SPACING);
      (PATRONES[t.tipo] || PATRONES.mixto)(z, d, t, k);
    } finally { carrilOcupado = -1; }
  }

  function ensureRows() {
    while (lastRowZ > SPAWN_Z) {
      if (!nivel) generarFila(lastRowZ);
      else {
        // Nivel: cada fila con la semilla de su metro (la misma en cada intento).
        const r = Math.random;
        Math.random = azarConSemilla(nivel.semilla * 100003 + Math.round(totalScrolled - lastRowZ));
        try { generarFila(lastRowZ); } finally { Math.random = r; }
      }
      lastRowZ -= ROW_SPACING;
    }
  }
  ensureRows();

  // ---- El Burrito-Bot se escapa al empezar Nueva York (se lleva la tortilla) ----
  const cameo = { t: -1 };
  function cameoJefe() {
    if (!EXTRAS) return;
    if (!jefe.mesh) jefe.mesh = modeloConContorno("obstaculos/jefe");
    jefe.mesh.visible = true;
    if (!jefe.mesh.parent) group.add(jefe.mesh);
    cameo.t = 0;
  }
  function actualizarCameo(dt) {
    if (cameo.t < 0 || jefe.activo) return;
    cameo.t += dt;
    const k = cameo.t, m = jefe.mesh;
    // Se planta delante, se ríe y sale volando calle abajo.
    const huye = Math.max(0, k - 1.4);
    m.position.set(Math.sin(k * 2.2) * 0.6, 2.4 + Math.sin(k * 3) * 0.2 + huye * 1.6, -16 - huye * huye * 9);
    m.rotation.set(0, Math.min(Math.PI, huye * 4), Math.sin(k * 4) * 0.08);
    if (k > 5) { m.visible = false; m.rotation.set(0, 0, 0); cameo.t = -1; }
  }

  function update(dz, dtFijo) {
    const now = typeof performance !== "undefined" ? performance.now() : Date.now();
    const dt = dtFijo !== undefined ? dtFijo : Math.min(0.05, Math.max(0, (now - lastTime) / 1000));
    lastTime = now;
    animClock += dt;

    totalScrolled += dz;
    // El suelo avanza de verdad: calzada, aceras y suelo eran laminas quietas
    // y solo pasaban las rayas. Cada textura se desplaza lo mismo que la pista
    // (el plano mide 400 y la textura se repite repeat.y veces en el).
    for (const tex of texturasSuelo) {
      if (!tex) continue;
      tex.offset.y = (tex.offset.y + (dz * tex.repeat.y) / 400) % 1;
    }
    curveX = Math.sin(totalScrolled * CURVE_FREQ) * CURVE_AMPLITUDE
      + Math.sin(totalScrolled * CURVE_FREQ2 + 1.3) * CURVE_AMPLITUDE2;
    group.position.x = curveX;

    // ---- Bioma: transicion suave de color de suelo/cielo/niebla ----
    const blend = biomeBlendAt(totalScrolled);
    const cFrom = BIOME_COLORS[blend.from], cTo = BIOME_COLORS[blend.to];
    blendA.set(cFrom.ground); blendB.set(cTo.ground); blendA.lerp(blendB, blend.t);
    groundMat.color.copy(blendA);
    blendA.set(cFrom.road); blendB.set(cTo.road); blendA.lerp(blendB, blend.t);
    carpetMat.color.copy(blendA);
    blendA.set(cFrom.sidewalk); blendB.set(cTo.sidewalk); blendA.lerp(blendB, blend.t);
    sidewalkMat.color.copy(blendA);
    blendA.set(cFrom.fog); blendB.set(cTo.fog); blendA.lerp(blendB, blend.t);
    scene.fog.color.copy(blendA);
    scene.background.copy(blendA);
    const zoneNow = currentZoneName(totalScrolled);
    if (zoneNow !== lastZoneName) {
      lastZoneName = zoneNow;
      const c = BIOME_COLORS[zoneNow];
      updateSkyColors(c.skyTop, c.sky);
      // El patron del suelo cambia con la zona (no solo el tinte): tierra
      // compacta en el desierto, asfalto en el resto. Es un cambio brusco de
      // patron en vez de crossfade como el color, pero al ser una textura de
      // ruido fino y de baja escala no se nota como un "pop" -- coincide
      // ademas con el momento en que ya esta cambiando el color del suelo.
      groundMat.map = texSuelo(zoneNow);
      groundMat.needsUpdate = true;
      carpetMat.map = texCalzada(zoneNow);
      carpetMat.needsUpdate = true;
      for (const t of goldTrims) t.visible = zoneNow !== "desert";
      for (const b of dirtBerms) b.visible = zoneNow === "desert";
      showMidLayer(zoneNow);
    }

    lastOuterZ += dz;
    if (frontCursor[-1] !== null) frontCursor[-1] += dz;
    if (frontCursor[1] !== null) frontCursor[1] += dz;
    ensureOuterProps();
    for (let i = outerProps.length - 1; i >= 0; i--) {
      const p = outerProps[i];
      p.mesh.position.z += dz;
      p.mesh.scale.setScalar(Math.max(0.001, edgeFade(p.mesh.position.z, DESPAWN_Z, 6)));
      if (p.mesh.userData.kind === "tumbleweed") {
        p.mesh.rotation.x += dt * p.mesh.userData.spinSpeed;
        p.mesh.rotation.z += dt * p.mesh.userData.spinSpeed * 0.6;
      }
      if (p.mesh.position.z > DESPAWN_Z) {
        outerPools[p.biome][p.poolIndex].release(p.mesh);
        outerProps.splice(i, 1);
      }
    }

    maybeSpawnSign();
    for (let i = citySigns.length - 1; i >= 0; i--) {
      const sign = citySigns[i];
      sign.position.z += dz;
      if (sign.position.z > DESPAWN_Z) { disposeCitySign(sign); citySigns.splice(i, 1); }
    }

    // Ninguna marca pintada sobre tierra/arena. En la ronda 17 solo se
    // ocultaron las lineas amarillas exteriores (roadLines) y se olvidaron
    // estas rayas blancas de carril, que son justo las del centro del camino
    // -- por eso el camino de tierra seguia teniendo lineas de autopista.
    // Cada marca consulta la zona en SU propia posicion (no la del jugador)
    // porque conviven varias franjas de bioma a lo largo del recorrido.
    for (const s of stripes) {
      // Hasta donde llega la calle del nivel (o hasta el horizonte).
      const hasta = nivel ? Math.min(8 - SPAWN_Z, Math.max(0.01, 8 + nivel.largo - totalScrolled)) : 8 - SPAWN_Z;
      s.scale.z = hasta;
      s.visible = currentZoneName(totalScrolled) !== "desert";
    }
    for (const rl of roadLines) {
      rl.position.z += dz; if (rl.position.z > 4) rl.position.z -= TRAMOS_RAYA;
      rl.visible = currentZoneName(totalScrolled - rl.position.z) !== "desert" && !(nivel && totalScrolled - rl.position.z > nivel.largo);
    }
    for (const d of decor) {
      d.position.z += dz; if (d.position.z > 6) d.position.z -= Math.abs(SPAWN_Z);
      d.scale.setScalar(Math.max(0.001, edgeFade(d.position.z, 6, 5)));
      d.visible = !(nivel && totalScrolled - d.position.z > nivel.largo - 10);
      if (d.userData.kind === "flag") {
        d.userData.flagMesh.rotation.y = Math.sin(animClock * 3 + d.userData.phase) * 0.3;
      } else if (d.userData.kind === "person") {
        // Se animan al ver pasar al jugador: botan mas y agitan el brazo.
        const cerca = THREE.MathUtils.clamp(1 - Math.abs(d.position.z) / 18, 0, 1);
        const r = d.userData.ritmo || 1;
        d.position.y = Math.max(0, Math.sin(animClock * 2.4 * r + d.userData.phase)) * (0.08 + 0.16 * cerca);
        if (d.userData.brazo) d.userData.brazo.rotation.z = 1.2 + 1.1 * cerca + Math.sin(animClock * (5 + 4 * cerca) * r + d.userData.phase) * (0.25 + 0.35 * cerca);
      }
    }
    for (const b of bunting) {
      b.position.z += dz; if (b.position.z > 4) b.position.z -= Math.abs(SPAWN_Z);
      b.scale.setScalar(Math.max(0.001, edgeFade(b.position.z, 4, 4)));
      b.visible = !(nivel && totalScrolled - b.position.z > nivel.largo - 10);
      b.rotation.z = Math.sin(animClock * 2.2 + b.userData.phase) * 0.22;
    }

    if (dt > 0) ritmo += (dz / dt - ritmo) * Math.min(1, dt * 2);
    actualizarCalle(dz);
    actualizarJefe(dt);
    actualizarDisparos(dt);
    actualizarFrases(dt);
    for (let i = obstacles.length - 1; i >= 0; i--) {
      const o = obstacles[i];
      o.z += dz + o.mueve * dt;
      if (o.cae && !o.smashed) {
        // Barril del jefe: cae desde su mano hasta la pista.
        o.cae.vy -= 30 * dt;
        o.mesh.position.y = Math.max(0, o.mesh.position.y + o.cae.vy * dt);
        if (o.mesh.position.y === 0) o.cae = null;
      }
      if (o.pool === "barril" && o.mueve) o.mesh.rotation.x -= dt * 9;   // rueda
      if (o.smashed) {
        // Sale volando dando vueltas y cae fuera de la pista.
        const s = o.smashed;
        s.vy -= 26 * dt;
        o.z += s.vz * dt;
        o.mesh.position.x += s.vx * dt;
        o.mesh.position.y += s.vy * dt;
        o.mesh.rotation.x += s.rx * dt; o.mesh.rotation.y += s.ry * dt; o.mesh.rotation.z += s.rz * dt;
      }
      o.mesh.position.z = o.z;
      if (o.mesh.userData.sirena) {
        const on = Math.floor(animClock * 6) % 2 === 0;
        o.mesh.userData.sirena[0].visible = on;
        o.mesh.userData.sirena[1].visible = !on;
      }
      if (o.mesh.userData.vapor) {
        // El vapor de la alcantarilla sube, crece y se deshace.
        o.mesh.userData.vapor.forEach((s, k) => {
          const f = (animClock * 0.7 + k / 3 + o.phase) % 1;
          s.position.y = 0.2 + f * 2.6;
          s.position.x = Math.sin((f + k) * 5) * 0.15;
          s.scale.setScalar(0.7 + f * 1.6);
          s.material.opacity = Math.sin(f * Math.PI) * 0.8;
        });
      }
      if (o.mueve) {
        // El coche se lleva por delante los tacos de su carril.
        for (const t of tacos) {
          if (!t.collected && t.lane === o.lane && Math.abs(t.z - (o.z + o.centro)) < o.medio) { t.collected = true; t.atropellado = true; }
        }
      }
      if (o.z > DESPAWN_Z + (o.type === "bus" ? BUS_LARGO : 0) || o.mesh.position.y < -6) {
        o.mesh.position.y = 0;
        if (o.hielo) { o.mesh.remove(o.hielo); o.hielo = null; }
        obstaclePools[o.pool].release(o.mesh);
        obstacles.splice(i, 1);
      }
    }
    for (let i = tacos.length - 1; i >= 0; i--) {
      const it = tacos[i];
      it.z += dz; it.mesh.position.z = it.z;
      it.mesh.rotation.y += 0.08;
      it.mesh.position.y = it.baseY + Math.sin(animClock * 3 + it.phase) * 0.08;
      const glowPulse = 1 + Math.sin(animClock * 4 + it.phase) * 0.18;
      if (it.mesh.userData.glow) it.mesh.userData.glow.scale.setScalar(glowPulse * 0.85);
      if (it.z > DESPAWN_Z || it.collected) {
        if (it.collected) burstSparkles(it.mesh.position.x, it.mesh.position.y, it.mesh.position.z);
        tacoPool.release(it.mesh);
        tacos.splice(i, 1);
      }
    }
    // Chapas de campaña: flotan y brillan mas que un taco.
    for (let i = chapas.length - 1; i >= 0; i--) {
      const c = chapas[i];
      c.z += dz; c.mesh.position.z = c.z;
      c.mesh.position.y = c.baseY + Math.sin(animClock * 2.6 + c.phase) * 0.1;
      c.mesh.userData.brillo.material.opacity = 0.55 + Math.sin(animClock * 5 + c.phase) * 0.25;
      if (c.z > DESPAWN_Z || c.collected) {
        if (c.collected) for (let k = 0; k < 3; k++) burstSparkles(c.mesh.position.x, c.mesh.position.y, c.mesh.position.z);
        chapaPool.release(c.mesh);
        chapas.splice(i, 1);
      }
    }
    actualizarCameo(dt);
    if (horizonte) horizonte.animar(dt);
    for (let i = powerups.length - 1; i >= 0; i--) {
      const p = powerups[i];
      p.z += dz; p.mesh.position.z = p.z;
      if (p.kind === "boost") {
        // Pegadas al suelo, con una ola de brillo/escala que recorre las 3
        // flechas hacia el jugador -- se lee como energia fluyendo hacia
        // delante, en vez de girar flotando en el aire como antes.
        p.mesh.position.y = 0.02;
        for (const chevron of p.mesh.userData.chevrons) {
          const t = ((animClock * 2.4 - chevron.userData.baseZ * 1.6) % 1 + 1) % 1;
          chevron.scale.setScalar(0.85 + Math.max(0, Math.sin(t * Math.PI)) * 0.3);
        }
      } else {
        p.mesh.rotation.y += 0.05;
        p.mesh.position.y = 1.0 + Math.sin(p.z * 0.5) * 0.08;
      }
      if (p.z > DESPAWN_Z || p.collected) { powerupPools[p.kind].release(p.mesh); powerups.splice(i, 1); }
    }

    for (let i = activeSparkles.length - 1; i >= 0; i--) {
      const s = activeSparkles[i];
      s.life -= dt;
      if (s.life <= 0) { sparklePool.release(s.mesh); activeSparkles.splice(i, 1); continue; }
      s.mesh.position.x += s.vx * dt;
      s.mesh.position.y += s.vy * dt;
      s.mesh.position.z += s.vz * dt;
      s.vy -= dt * 2.2; // gravedad leve
      const k = s.life / s.maxLife;
      s.mesh.material.opacity = k;
      s.mesh.scale.setScalar(0.5 + k * 0.7);
    }

    lastRowZ += dz;
    ensureRows();
    return curveX;
  }

  // `desde`: seguir desde el punto de control (los metros de la partida en
  // los que se empieza). `chapasHechas`: las chapas que ya no hay que poner.
  function reset(desde = 0, opciones = {}) {
    totalScrolled = desde;
    curveX = 0;
    group.position.x = 0;
    chapas.forEach((c) => chapaPool.release(c.mesh));
    chapas.length = 0;
    chapasHechas = new Set(opciones.chapasHechas || []);
    avisos.length = 0;
    reserva = null;
    cameo.t = -1;
    prepararTramos();
    obstacles.forEach((o) => { o.mesh.position.y = 0; if (o.hielo) { o.mesh.remove(o.hielo); o.hielo = null; } obstaclePools[o.pool].release(o.mesh); });
    acabarJefe(); cielo = false;
    for (const f of frases) group.remove(f.sprite);
    frases.length = 0;
    busCarril = -1; busFilas = 0;
    tacos.forEach((t) => tacoPool.release(t.mesh));
    powerups.forEach((p) => powerupPools[p.kind].release(p.mesh));
    activeSparkles.forEach((s) => sparklePool.release(s.mesh));
    citySigns.forEach((s) => disposeCitySign(s));
    outerProps.forEach((p) => outerPools[p.biome][p.poolIndex].release(p.mesh));
    frontCursor[-1] = frontCursor[1] = null;
    obstacles.length = 0; tacos.length = 0; powerups.length = 0; activeSparkles.length = 0; citySigns.length = 0; outerProps.length = 0;
    cityIndex = 0;
    nextSignAt = 260;
    lastRowZ = -14;
    lastOuterZ = -4;
    prepararCalle();
    montarDecor();
    lastZoneName = forcedZone || "city";
    const startColors = BIOME_COLORS[lastZoneName];
    updateSkyColors(startColors.skyTop, startColors.sky);
    groundMat.color.set(startColors.ground);
    groundMat.map = texSuelo(lastZoneName);
    groundMat.needsUpdate = true;
    carpetMat.color.set(startColors.road);
    sidewalkMat.color.set(startColors.sidewalk);
    carpetMat.map = texCalzada(lastZoneName);
    carpetMat.needsUpdate = true;
    for (const t of goldTrims) t.visible = lastZoneName !== "desert";
    for (const b of dirtBerms) b.visible = lastZoneName === "desert";
    showMidLayer(lastZoneName);
    scene.fog.color.set(startColors.fog);
    scene.background.set(startColors.sky);
    ensureRows();
    ensureOuterProps();
  }

  // Lo de la acera y el horizonte, ya para el menu (luego se rehacen en cada partida).
  montarDecor();
  showMidLayer("city");

  return { group, obstacles, tacos, powerups, chapas, update, reset, setForcedZone, surfaceAt, smash, spawnObstacle, spawnPowerup,
    congelar, setCielo, iniciarJefe, jefeActivo, dispararJefe, onJefe, setJugador, primerObstaculo, lanzarFrase,
    setNivel, getNivel, setLuz, getCasaBlanca, tramoEn, tomarAviso, cameoJefe, currentZoneName, despedirJefe };
}
