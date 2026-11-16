// 16/11/2026: el esquí de Denver visto de lado (prueba de la fase 1).
//
// Isidro: «quiero cambiar la forma en la que se corre … que se vea en 2D
// esquiando con saltos». Bajada por la ladera vista de lado: tocar es
// saltar, mantener el dedo en el aire da volteretas y hay que aterrizar con
// los esquís rectos sobre la nieve. Detrás baja rodando la bola de nieve
// gigante de Denver: si te pilla, se acaba.
//
// 16/11 (2): «el juego se tiene que ver vertical … mejora la animación y la
// jugabilidad». En vertical la ladera es mucho más empinada y baja en
// diagonal (de arriba a la izquierda hacia abajo a la derecha): así cabe lo
// que viene y los saltos caen pantalla abajo. Nieve que salta de los esquís,
// polvo al aterrizar, tacos que flotan y estallan, la sombra de donde vas a
// caer, los esquís en VERDE cuando es buen momento de soltar, combos y
// avisos para aprender en la primera bajada.
//
// Fase 1: la ladera, los saltos, las volteretas, los aterrizajes, los tacos,
// los montones, las rocas y la bola. Lo de Denver (sus edificios, sus
// objetos y el final en el Capitolio) va en la fase 2.
//
// Nada que maree (ver la memoria «juegos sin mareo»): la cámara nunca gira,
// solo se desliza suave detrás del esquiador; nada parpadea.

import * as THREE from "../vendor/three.module.min.js";
import { cargarPersonaje, cargarCarpeta, modeloConContorno, hayModelo } from "./models.js";
import { createCharacter } from "./character.js";
import { lienzo, urlPegatina } from "./pegatinas.js";
import { sndJump, sndHit, sndPoint, sndFanfarria, unlockAudio } from "./audio.js";
import { crearHorizonte } from "./horizonte.js";

// ---------------------------------------------------------------- ajustes
// (16/11: «se siente pesado»: gravedad baja, volteretas rápidas y
// aterrizajes algo perdonados.)
const G = 16;              // gravedad
const V_MIN = 10, V_MAX = 30;
const IMPULSO = 9.2;       // el salto, hacia fuera de la ladera
const GIRO = 8.6;          // volteretas: radianes por segundo con el dedo puesto
const TOLERANCIA = 0.85;   // aterrizaje bueno si los esquís no se desvían más (rad)
const PERFECTO = 0.22;
const BOLA_R = 3.6;
const ESCALA = 1.8;        // el esquiador, más grande para que se vea bien en vertical
const ANCHO_VISTO = 23;    // metros que se ven de lado a lado
// 16/11 (4): Isidro: «parece que no hay forma de perder» (sin tocar nada se
// aguantaban más de 2 minutos). La bola, en 50 s, llega a tu paso (18 m/s);
// luego sigue acelerando despacio hasta 21, y nunca se queda más de 35 m
// atrás: cada tortazo se nota.
const BOLA_V0 = 12, BOLA_HUECO = 35;
const velBola = (t) => Math.min(21, BOLA_V0 + 6 * Math.min(1, t / 50) + 0.02 * Math.max(0, t - 50));
const V_TACOS = 25;        // la velocidad de un salto bueno (lo normal al llegar al trampolín): con ella se dibujan los arcos de tacos

// ---------------------------------------------------------------- la ladera
// La altura del suelo en cada x: una bajada empinada (tramos más y menos
// pendientes, lomas) y, cada 70-130 m, un trampolín que acaba en un
// cortado: ahí se vuela.
let semilla = 7;
const azar = () => { semilla = (semilla * 16807) % 2147483647; return (semilla - 1) / 2147483646; };
let rasgos = [], rasgosHasta = 60;
function prepararRasgos(hasta) {
  while (rasgosHasta < hasta) {
    const x0 = rasgosHasta + 110 + azar() * 60;
    const mas = Math.min(1.2, x0 / 2500);    // (cada vez más grandes)
    rasgos.push({ x0, alto: 2.6 + azar() * 1.0 + mas, largo: 5.5 + azar() * 1.5, caida: 4 + azar() * 6 + mas * 3 });
    rasgosHasta = x0;
  }
}
function base(x) { return -0.85 * x - 16 * (1 - Math.cos(x / 80)) + 3 * Math.sin(x / 23) + 1.1 * Math.sin(x / 8.7 + 1.3); }
function rasgo(f, x) {
  const a = f.x0 - f.largo;
  if (x <= a) return 0;
  if (x <= f.x0) { const u = (x - a) / f.largo; return f.alto * u * u; }
  const u = Math.min(1, (x - f.x0) / 0.8);
  return f.alto * (1 - u) - f.caida * u;
}
function suelo(x) {
  prepararRasgos(x + 400);
  let h = base(x);
  for (const f of rasgos) { if (f.x0 - f.largo > x) break; h += rasgo(f, x); }
  return h;
}
function pendiente(x) { return (suelo(x + 0.05) - suelo(x - 0.05)) / 0.1; }
const envolver = (a) => Math.atan2(Math.sin(a), Math.cos(a));

// ---------------------------------------------------------------- escena
const cont = document.getElementById("juego");
const renderer = new THREE.WebGLRenderer({ antialias: (window.devicePixelRatio || 1) < 2, powerPreference: "high-performance" });
renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 1.5));   // (más ligero en el móvil)
renderer.outputColorSpace = THREE.SRGBColorSpace;
cont.prepend(renderer.domElement);
const scene = new THREE.Scene();
scene.fog = new THREE.Fog(0xd4e6f4, 110, 340);
const camera = new THREE.PerspectiveCamera(55, 0.5, 0.5, 700);
scene.add(camera);
renderer.autoClear = false;
// 16/11 (3): Isidro: «le falta calidad visual, el fondo». El fondo es el
// mismo horizonte de Denver que pinta el juego (las Rocosas con nieve, los
// edificios y las nubes), en su propia escena con su camara quieta, sobre un
// cielo degradado. Al bajar, gira muy despacio: de las montañas a la ciudad.
const fondo = new THREE.Scene();
fondo.background = (() => {
  const c = document.createElement("canvas"); c.width = 4; c.height = 256;
  const x = c.getContext("2d");
  const g = x.createLinearGradient(0, 0, 0, 256);
  g.addColorStop(0, "#3a80d2"); g.addColorStop(0.5, "#8ec8ec"); g.addColorStop(1, "#e6f1fa");
  x.fillStyle = g; x.fillRect(0, 0, 4, 256);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace;
  return t;
})();
const camFondo = new THREE.PerspectiveCamera(55, 0.5, 1, 1200);
camFondo.position.set(0, 7, 10);
camFondo.rotation.order = "YXZ";
const horizonte = crearHorizonte(fondo);
horizonte.pintar("denver", 0x8ec8ec, 0xd4e6f4);
// (en vertical las nubes del juego salian enormes y tapaban las montañas)
fondo.traverse((o) => { if (o.isSprite) { o.scale.multiplyScalar(0.5); o.position.y += 14; } });
scene.add(new THREE.HemisphereLight(0xeaf4ff, 0x8a9ab0, 1.6));
const sol = new THREE.DirectionalLight(0xfff4e0, 1.6);
sol.position.set(-20, 40, 30);
scene.add(sol);

// En vertical, como el juego. En el PC (pantalla apaisada) se ve una
// columna en el centro, con la forma de un móvil.
function medir() {
  const w = window.innerWidth, h = window.innerHeight;
  const W = Math.min(w, Math.round(h * 0.56)), H = h;
  cont.style.width = W + "px"; cont.style.height = H + "px";
  cont.style.left = Math.round((w - W) / 2) + "px";
  renderer.setSize(W, H);
  camera.aspect = camFondo.aspect = W / H;
  camera.updateProjectionMatrix(); camFondo.updateProjectionMatrix();
}
window.addEventListener("resize", medir);
medir();

// Los montes del fondo (las Rocosas): una tira que se repite cada P metros y
// se mueve despacio (parallax).
function crearMontes(P, z, alto, colorBajo, colorAlto, nieve, armonicos) {
  const pos = [], col = [], c1 = new THREE.Color(colorBajo), c2 = new THREE.Color(colorAlto), cn = new THREE.Color(0xf6f8fc);
  const N = 240;
  const y = (x) => alto + armonicos.reduce((s, [k, a, f]) => s + a * Math.sin(2 * Math.PI * k * x / P + f), 0);
  for (let i = 0; i < N; i++) {
    const xa = -P + (2 * P * i) / N, xb = -P + (2 * P * (i + 1)) / N;
    const ya = y(xa), yb = y(xb), fondo = -160;
    const ca = ya > nieve ? cn : c2, cb = yb > nieve ? cn : c2;
    pos.push(xa, fondo, 0, xb, fondo, 0, xb, yb, 0, xa, fondo, 0, xb, yb, 0, xa, ya, 0);
    for (const c of [c1, c1, cb, c1, cb, ca]) col.push(c.r, c.g, c.b);
  }
  const g = new THREE.BufferGeometry();
  g.setAttribute("position", new THREE.Float32BufferAttribute(pos, 3));
  g.setAttribute("color", new THREE.Float32BufferAttribute(col, 3));
  const m = new THREE.Mesh(g, new THREE.MeshBasicMaterial({ vertexColors: true, fog: false }));
  m.position.z = z;
  m.userData.P = P;
  scene.add(m);
  return m;
}
// Dos filas de bosque delante de las montañas (mas azuladas cuanto mas
// lejos): la loma y sus pinos con la punta nevada.
function crearBosque(P, z, colLoma, colPino, nPinos, armonicos, f, dy, relleno = 0, hondo = 0) {
  const pos = [], col = [];
  const cL = new THREE.Color(colLoma), cP = new THREE.Color(colPino), cN = new THREE.Color(0xf2f6fb).lerp(new THREE.Color(colLoma), 0.25);
  const y = (x) => armonicos.reduce((s, [k, a, fa]) => s + a * Math.sin(2 * Math.PI * k * x / P + fa), 0);
  const tri = (a, b, c, color) => { pos.push(...a, ...b, ...c); for (let i = 0; i < 3; i++) col.push(color.r, color.g, color.b); };
  const N = 200;
  for (let i = 0; i < N; i++) {
    const xa = -P + (2 * P * i) / N, xb = -P + (2 * P * (i + 1)) / N;
    tri([xa, -200, 0], [xb, -200, 0], [xb, y(xb), 0], cL);
    tri([xa, -200, 0], [xb, y(xb), 0], [xa, y(xa), 0], cL);
  }
  let q = 99;
  const r = () => { q = (q * 16807) % 2147483647; return q / 2147483647; };
  // (los de la loma y, si hay relleno, más pinos ladera abajo: un bosque)
  const sitios = [];
  for (let i = 0; i < nPinos; i++) sitios.push([r() * P, 1.5 + r() * 3]);
  for (let i = 0; i < relleno; i++) sitios.push([r() * P, 4 + r() * hondo]);
  for (const [x0, baja] of sitios) for (const off of [-P, 0]) {
    const x = x0 + off, h = 5 + r() * 6, w = h * 0.32, base = y(x) - baja;
    tri([x - w, base, 0.1], [x + w, base, 0.1], [x, base + h, 0.1], cP);
    tri([x - w * 0.3, base + h * 0.7, 0.12], [x + w * 0.3, base + h * 0.7, 0.12], [x, base + h, 0.12], cN);
  }
  const g = new THREE.BufferGeometry();
  g.setAttribute("position", new THREE.Float32BufferAttribute(pos, 3));
  g.setAttribute("color", new THREE.Float32BufferAttribute(col, 3));
  const m = new THREE.Mesh(g, new THREE.MeshBasicMaterial({ vertexColors: true, fog: false }));
  m.position.z = z;
  Object.assign(m.userData, { P, f, dy });
  scene.add(m);
  return m;
}
const bosques = [
  crearBosque(700, -210, 0x9cb4cc, 0x7f98b4, 160, [[3, 5, 0], [8, 2.5, 1], [17, 1.2, 2]], 0.16, 22, 120, 22),
  crearBosque(400, -125, 0x6d9488, 0x3f6e5c, 110, [[4, 4, 0.3], [9, 2, 1.7], [19, 1, 0.9]], 0.3, 6, 260, 45),
];

// La nieve: trozos de 50 m con la cara de delante (azulada, más oscura
// abajo), la parte de arriba (blanca) y un filo para que se lea bien.
const TROZO = 50, PASO = 0.5;
const matNieve = new THREE.MeshBasicMaterial({ vertexColors: true });
const geoRocaCara = new THREE.DodecahedronGeometry(1, 0);
const matRocaCara = new THREE.MeshLambertMaterial({ color: 0x7c8898, flatShading: true });
const matNieveCap = new THREE.MeshBasicMaterial({ color: 0xf6f9fd });
const matFilo = new THREE.MeshBasicMaterial({ color: 0x7a9cc8 });
const trozos = new Map();
function crearTrozo(i) {
  const x0 = i * TROZO, pos = [], col = [], filo = [];
  const arriba = new THREE.Color(0xfbfdff), detras = new THREE.Color(0xd9e5f3);
  const cara = new THREE.Color(0xf0f6fc), medio = new THREE.Color(0xd0e0f0), fondoC = new THREE.Color(0xa4bcda);
  const n = TROZO / PASO;
  let ya = suelo(x0);
  const quad = (a, b, c, d, ca, cb, cc, cd) => { pos.push(...a, ...b, ...c, ...a, ...c, ...d); for (const q of [ca, cb, cc, ca, cc, cd]) col.push(q.r, q.g, q.b); };
  for (let k = 0; k < n; k++) {
    const xa = x0 + k * PASO, xb = xa + PASO, yb = suelo(xb);
    // la cara de delante: blanca arriba y azulandose hacia abajo
    quad([xa, ya, 2], [xa, ya - 5, 2], [xb, yb - 5, 2], [xb, yb, 2], cara, medio, medio, cara);
    quad([xa, ya - 5, 2], [xa, ya - 60, 2], [xb, yb - 60, 2], [xb, yb - 5, 2], medio, fondoC, fondoC, medio);
    // la parte de arriba: blanca delante y algo azulada al fondo
    quad([xa, ya, 2], [xb, yb, 2], [xb, yb, -10], [xa, ya, -10], arriba, arriba, detras, detras);
    filo.push(xa, ya, 2.02, xa, ya - 0.22, 2.02, xb, yb - 0.22, 2.02, xa, ya, 2.02, xb, yb - 0.22, 2.02, xb, yb, 2.02);
    ya = yb;
  }
  const g = new THREE.BufferGeometry();
  g.setAttribute("position", new THREE.Float32BufferAttribute(pos, 3));
  g.setAttribute("color", new THREE.Float32BufferAttribute(col, 3));
  g.computeVertexNormals();
  const gf = new THREE.BufferGeometry();
  gf.setAttribute("position", new THREE.Float32BufferAttribute(filo, 3));
  const grupo = new THREE.Group();
  grupo.add(new THREE.Mesh(g, matNieve));
  grupo.add(new THREE.Mesh(gf, matFilo));
  // Rocas asomando en la cara de la nieve y en los cortados de los trampolines.
  const roca = (x, y, r) => {
    const m = new THREE.Mesh(geoRocaCara, matRocaCara);
    m.position.set(x, y, 2.15); m.scale.set(r * (1 + azar() * 0.6), r, 0.35); m.rotation.z = azar() * 3;
    grupo.add(m);
    const cap = new THREE.Mesh(geoRocaCara, matNieveCap);
    cap.position.set(x, y + r * 0.62, 2.3); cap.scale.set(r * 1.1, r * 0.25, 0.3);
    grupo.add(cap);
  };
  for (let k = 0; k < 4; k++) { const x = x0 + azar() * TROZO; roca(x, suelo(x) - 3 - azar() * 14, 0.7 + azar() * 1.1); }
  for (const f of rasgos) if (f.x0 >= x0 && f.x0 < x0 + TROZO) {
    const alto = f.alto + f.caida;
    for (let k = 0; k < 4; k++) roca(f.x0 + 0.4 + azar() * 0.6, suelo(f.x0 + 1) + alto * (0.15 + 0.22 * k), 0.8 + azar() * 0.6);
  }
  // Pinos y algún muñeco de nieve detrás de la pista.
  let x = x0 + 3 + azar() * 6;
  while (x < x0 + TROZO) {
    const nombre = azar() < 0.85 ? "obstaculos/pino_nevado" : "obstaculos/munieco_nieve";
    if (hayModelo(nombre)) {
      const p = modeloConContorno(nombre);
      p.scale.setScalar(nombre.includes("pino") ? 1.0 + azar() * 0.7 : 1.2);
      p.position.set(x, suelo(x) - 0.2, -4 - azar() * 5);
      grupo.add(p);
    }
    x += 4 + azar() * 8;
  }
  scene.add(grupo);
  trozos.set(i, grupo);
  ponerCosas(x0);
}
function quitarTrozo(i) {
  const g = trozos.get(i);
  g.traverse((o) => { if (o.isMesh && o.geometry && (o.material === matNieve || o.material === matFilo)) o.geometry.dispose(); });
  scene.remove(g);
  trozos.delete(i);
}

// ---------------------------------------------------------------- tacos, montones y rocas
const texTaco = new THREE.CanvasTexture(lienzo("taco"));
texTaco.colorSpace = THREE.SRGBColorSpace;
const matTaco = new THREE.SpriteMaterial({ map: texTaco });
let tacos = [], obstaculos = [];
function ponerTaco(x, y, de = "") {
  const s = new THREE.Sprite(matTaco);
  s.scale.setScalar(1.3);
  s.position.set(x, y, 0.4);
  scene.add(s);
  tacos.push({ x, y, s, cogido: false, pop: 0, de });
}
// 16/11 (4): Isidro: «los tacos se alinean y se mueven según el salto que he
// hecho; tienen que estar fijos, pero acordes con el salto». Ya no se mueven
// nunca: cada arco se dibuja de antemano con el vuelo de un salto bueno (a
// V_TACOS). Si vas lento o muy rápido, o saltas a destiempo, se te escapan.
function arco(x, y, vx, vy, hastaX) {
  const pts = [];
  for (let k = 1; k < 600; k++) {
    vy -= G / 120; x += vx / 120; y += vy / 120;
    if (y <= suelo(x) || x > hastaX) break;
    pts.push({ x, y });
  }
  return pts;
}
function alturaEn(pts, x) {
  let m = null;
  for (const p of pts) if (!m || Math.abs(p.x - x) < Math.abs(m.x - x)) m = p;
  return m && Math.abs(m.x - x) < 0.5 ? m.y : null;
}
const matRoca = new THREE.MeshLambertMaterial({ color: 0x7a7a84, flatShading: true });
const matRocaNieve = new THREE.MeshLambertMaterial({ color: 0xf4f8fc, flatShading: true });
function hacerRoca() {
  const g = new THREE.Group();
  const r = new THREE.Mesh(new THREE.DodecahedronGeometry(0.75, 0), matRoca);
  r.scale.set(1.3, 0.95, 1); r.position.y = 0.55; r.rotation.set(azar(), azar(), azar());
  g.add(r);
  const n = new THREE.Mesh(new THREE.DodecahedronGeometry(0.45, 0), matRocaNieve);
  n.scale.set(1.6, 0.4, 1.2); n.position.y = 1.15;
  g.add(n);
  return g;
}
// (nada de montones en los 40 m antes de un trampolín, que saltarlos te haría
// pasar el trampolín por encima, ni debajo de su vuelo, donde no se tocan)
function finVuelo(f) {
  if (f.fin === undefined) {
    const a = Math.atan(pendiente(f.x0 - 0.12));
    const pts = arco(f.x0, suelo(f.x0), V_TACOS * Math.cos(a), V_TACOS * Math.sin(a), f.x0 + 200);
    f.fin = pts.length ? pts[pts.length - 1].x : f.x0 + 30;
  }
  return f.fin;
}
function cercaDeTrampolin(x) { return rasgos.some((f) => x > f.x0 - f.largo - 30 && x < finVuelo(f) - 6); }
function ponerCosas(x0) {
  if (x0 < 40) return;
  // Un arco de tacos por el vuelo de cada trampolín y, por la nieve, filas
  // de tacos, montones y rocas (con tacos encima: el premio por saltarlos).
  for (const f of rasgos) {
    if (f.x0 < x0 || f.x0 >= x0 + TROZO) continue;
    // (el vuelo del trampolín sin tocar nada: te lanza él)
    // (el primer segundo y medio del vuelo: más allá, cada velocidad cae en un sitio)
    const a = Math.atan(pendiente(f.x0 - 0.12));
    const pts = arco(f.x0, suelo(f.x0), V_TACOS * Math.cos(a), V_TACOS * Math.sin(a), f.x0 + 60);
    for (let i = 12; i < Math.min(pts.length, 190); i += 20) if (pts[i].y > suelo(pts[i].x) + 1.6) ponerTaco(pts[i].x, pts[i].y + 1.4, "trampolin");
  }
  let x = x0 + 6 + azar() * 8;
  while (x < x0 + TROZO) {
    if (!cercaDeTrampolin(x)) {
      const r = azar();
      if (r < 0.7) {
        const roca = r < 0.25;
        let m = null;
        if (roca) m = hacerRoca();
        else if (hayModelo("obstaculos/monton_nieve")) { m = modeloConContorno("obstaculos/monton_nieve"); m.scale.setScalar(1.3); }
        if (m) {
          m.position.set(x, suelo(x) - 0.05, 0);
          m.rotation.z = Math.atan(pendiente(x));
          scene.add(m);
          const ob = { x, alto: roca ? 1.2 : 1.05, m, tocado: false };
          obstaculos.push(ob);
          // (el vuelo de un salto dado 0,3 s antes del montón)
          const xj = x - 0.3 * V_TACOS * Math.cos(Math.atan(pendiente(x))), aj = Math.atan(pendiente(xj));
          const pts = arco(xj, suelo(xj), V_TACOS * Math.cos(aj) - IMPULSO * Math.sin(aj), V_TACOS * Math.sin(aj) + IMPULSO * Math.cos(aj), x + 6);
          for (let k = -1; k <= 3; k += 2) { const y = alturaEn(pts, x + k); if (y !== null) ponerTaco(x + k, y + 1.4, "monton"); }
        }
      } else {
        for (let k = 0; k < 4; k++) ponerTaco(x + k * 2.2, suelo(x + k * 2.2) + 1.3);
      }
    }
    x += 11 + azar() * 13;
  }
}

// ---------------------------------------------------------------- la nieve que salta (partículas)
// Bolitas de nieve que salen, suben un poco y se deshacen poco a poco (nada
// parpadea: solo se van aclarando).
const texCopo = (() => {
  const c = document.createElement("canvas"); c.width = c.height = 64;
  const x = c.getContext("2d");
  const gr = x.createRadialGradient(32, 32, 2, 32, 32, 30);
  gr.addColorStop(0, "rgba(255,255,255,1)"); gr.addColorStop(0.6, "rgba(240,246,252,0.8)"); gr.addColorStop(1, "rgba(230,240,250,0)");
  x.fillStyle = gr; x.fillRect(0, 0, 64, 64);
  return new THREE.CanvasTexture(c);
})();
const particulas = [];
for (let i = 0; i < 90; i++) {
  const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: texCopo, transparent: true, depthWrite: false }));
  s.visible = false;
  scene.add(s);
  particulas.push({ s, vida: 0, t: 1, vx: 0, vy: 0, tam: 1 });
}
let siguiente = 0;
function soltarNieve(x, y, vx, vy, vida, tam) {
  const p = particulas[siguiente];
  siguiente = (siguiente + 1) % particulas.length;
  p.s.visible = true; p.s.position.set(x, y, 0.8);
  Object.assign(p, { vida, t: 0, vx, vy, tam });
}
function nubeNieve(x, y, n, fuerza, tam) {
  for (let i = 0; i < n; i++) soltarNieve(x, y, (Math.random() - 0.5) * fuerza * 2, 1.5 + Math.random() * fuerza, 0.5 + Math.random() * 0.35, tam * (0.7 + Math.random() * 0.6));
}
function moverNieve(dt) {
  for (const p of particulas) {
    if (!p.s.visible) continue;
    p.t += dt;
    if (p.t >= p.vida) { p.s.visible = false; continue; }
    p.vy -= 6 * dt;
    p.s.position.x += p.vx * dt; p.s.position.y += p.vy * dt;
    const u = p.t / p.vida;
    p.s.material.opacity = 0.85 * (1 - u);
    p.s.scale.setScalar(p.tam * (0.6 + 0.8 * u));
  }
}

// ---------------------------------------------------------------- el esquiador
const esquiador = new THREE.Group();    // gira con la ladera y con las volteretas
esquiador.scale.setScalar(ESCALA);
scene.add(esquiador);
let personaje = null;
const matEsqui = new THREE.MeshLambertMaterial({ color: 0xc8302a });
const ROJO = new THREE.Color(0xc8302a), VERDE = new THREE.Color(0x2ac84a), NARANJA = new THREE.Color(0xe88a2a);
function vestir() {
  personaje = createCharacter(null);
  // Postura fija de esquiar (Isidro: sin animar). Se pone con el muñeco sin
  // girar y ya no se toca.
  if (personaje.setEsquiPose) personaje.setEsquiPose(); else if (personaje.setJumpPose) personaje.setJumpPose(0.5);
  personaje.object3D.rotation.y = -Math.PI / 2;    // mira hacia donde baja (+x)
  esquiador.add(personaje.object3D);
  for (const z of [-0.17, 0.17]) {
    const e = new THREE.Mesh(new THREE.BoxGeometry(1.9, 0.07, 0.13), matEsqui);
    e.position.set(0.1, 0.035, z);
    esquiador.add(e);
    const punta = new THREE.Mesh(new THREE.BoxGeometry(0.3, 0.07, 0.13), matEsqui);
    punta.position.set(1.1, 0.1, z); punta.rotation.z = 0.5;
    esquiador.add(punta);
  }
}
// La sombra de donde vas a caer (en el aire).
const sombra = new THREE.Group();
const sombraM = new THREE.Mesh(new THREE.CircleGeometry(1, 24), new THREE.MeshBasicMaterial({ color: 0x2a4a8a, transparent: true, opacity: 0.32, depthWrite: false }));
sombraM.rotation.x = -Math.PI / 2; sombraM.scale.set(1.6, 0.6, 1); sombraM.position.y = 0.06;
sombra.add(sombraM);
sombra.visible = false;
scene.add(sombra);

// Las huellas de los esquis (dos rayitas que se quedan en la nieve).
const MAXH = 260;
const huellaPos = new Float32Array(MAXH * 4 * 3);
const huellaGeo = new THREE.BufferGeometry();
huellaGeo.setAttribute("position", new THREE.BufferAttribute(huellaPos, 3));
huellaGeo.setDrawRange(0, 0);
scene.add(new THREE.LineSegments(huellaGeo, new THREE.LineBasicMaterial({ color: 0xa6bad6 })));
let huellaPts = [], huellaCorte = true;
// Copos que caen (pegados a la camara, por delante de todo).
const copos = [];
for (let i = 0; i < 55; i++) {
  const c = new THREE.Sprite(new THREE.SpriteMaterial({ map: texCopo, transparent: true, depthWrite: false, opacity: 0.75, fog: false }));
  const t = 0.12 + Math.random() * 0.22;
  c.scale.set(t, t, 1);
  c.position.set((Math.random() - 0.5) * 22, (Math.random() - 0.5) * 52, -20);
  c.userData.v = 1.2 + Math.random() * 1.8; c.userData.f = Math.random() * 6;
  camera.add(c);
  copos.push(c);
}

// La bola de nieve gigante que baja detrás.
const bola = new THREE.Group();
scene.add(bola);
function hacerBola() {
  let m;
  if (hayModelo("obstaculos/bola_nieve")) {
    m = modeloConContorno("obstaculos/bola_nieve");
    const caja = new THREE.Box3().setFromObject(m), tam = new THREE.Vector3();
    caja.getSize(tam);
    const k = (2 * BOLA_R) / Math.max(tam.x, tam.y, tam.z);
    m.scale.setScalar(k);
    const centro = new THREE.Vector3(); caja.getCenter(centro);
    m.position.set(-centro.x * k, -centro.y * k, -centro.z * k);
  } else {
    m = new THREE.Mesh(new THREE.IcosahedronGeometry(BOLA_R, 2), new THREE.MeshLambertMaterial({ color: 0xf4f8fc, flatShading: true }));
  }
  const giro = new THREE.Group();
  giro.add(m);
  bola.add(giro);
  bola.userData.giro = giro;
}

// ---------------------------------------------------------------- estado
const E = {};
let record = 0;
try { record = +localStorage.getItem("esqui_record") || 0; } catch (e) { /* sin guardar */ }
function reiniciar() {
  for (const t of tacos) scene.remove(t.s);
  for (const m of obstaculos) scene.remove(m.m);
  tacos = []; obstaculos = [];
  for (const i of [...trozos.keys()]) quitarTrozo(i);
  for (const p of particulas) p.s.visible = false;
  huellaPts = []; huellaCorte = true;
  semilla = 7 + Math.floor(Math.random() * 100000);
  rasgos = []; rasgosHasta = 60;
  Object.assign(E, {
    fase: "inicio", x: 0, y: suelo(0), s: 14, vx: 14, vy: 0, ang: Math.atan(pendiente(0)), suelo: true,
    dedo: false, giroAcum: 0, tumbo: 0, intocable: 0, salto: 0, buffer: 0, desdeTrampolin: false,
    tacos: 0, vueltasTot: 0, choques: 0, perfectos: 0, combo: 0, comboMax: 0, t: 0,
    bx: -BOLA_HUECO, bv: BOLA_V0, camX: 0, camY: suelo(0), camD: 0, rastro: 0, rastroBola: 0, aterriza: null,
    ayudaSalto: false, ayudaVuelta: false,
  });
}

// ---------------------------------------------------------------- avisos en pantalla
const elMsg = document.getElementById("msg");
let msgHasta = 0;
function aviso(texto, sub = "", ms = 1100) { elMsg.innerHTML = texto + (sub ? `<small>${sub}</small>` : ""); elMsg.style.opacity = 1; msgHasta = performance.now() + ms; }

// ---------------------------------------------------------------- física
function saltar() {
  if (!E.suelo || E.tumbo > 0) return false;
  // En el trampolín no se salta: te lanza él (y el vuelo sigue la línea de
  // tacos). El dedo puesto sirve para empezar la voltereta al despegar.
  if (rasgos.some((f) => E.x > f.x0 - f.largo - 1 && E.x < f.x0 + 0.5)) return false;
  const a = Math.atan(pendiente(E.x));
  E.vx = E.s * Math.cos(a) - IMPULSO * Math.sin(a);
  E.vy = E.s * Math.sin(a) + IMPULSO * Math.cos(a);
  E.suelo = false; E.giroAcum = 0; E.salto = 0; E.desdeTrampolin = false;
  sndJump();
  return true;
}
function chocar(texto) {
  E.tumbo = 0.7; E.intocable = 1.0; E.choques++; E.combo = 0;
  E.s = Math.max(V_MIN + 1, E.s * 0.55);
  nubeNieve(E.x, E.y + 0.6, 18, 4, 1.4);
  sndHit();
  aviso(texto);
}
// Dónde vas a caer, siguiendo el vuelo desde ahora (para la sombra y para
// saber si los esquís van bien).
function caida() {
  let x = E.x, y = E.y, vx = E.vx, vy = E.vy;
  for (let k = 0; k < 480; k++) {
    vy -= G / 120; x += vx / 120; y += vy / 120;
    if (y <= suelo(x)) return { x, t: k / 120 };
  }
  return null;
}
function aterrizar() {
  const a = Math.atan(pendiente(E.x));
  const desvio = Math.abs(envolver(E.ang - a));
  const vueltas = Math.round(E.giroAcum / (Math.PI * 2));
  const rapidez = Math.hypot(E.vx, E.vy), aLo = E.vx * Math.cos(a) + E.vy * Math.sin(a);
  E.s = Math.min(V_MAX, Math.max(V_MIN, 0.6 * rapidez + 0.4 * aLo));
  E.suelo = true; E.y = suelo(E.x); E.ang = a;
  nubeNieve(E.x, E.y + 0.2, E.salto > 0.6 ? 12 : 5, 3, 1.0);
  if (desvio > TOLERANCIA) { chocar(vueltas > 0 ? "¡TORTAZO!<small>Suelta cuando los esquís estén VERDES</small>" : "¡TORTAZO!"); return; }
  if (vueltas > 0) {
    E.combo++; E.comboMax = Math.max(E.comboMax, E.combo);
    const n = 5 * vueltas * E.combo;
    E.tacos += n; E.vueltasTot += vueltas;
    E.s = Math.min(V_MAX, E.s + 4 * vueltas);
    // (y la bola se queda atrás: las volteretas son la forma de escaparse)
    const atras = Math.min(8 * vueltas, BOLA_HUECO - (E.x - E.bx));
    if (atras > 0) E.bx -= atras;
    const titulo = vueltas === 1 ? "¡VOLTERETA!" : `¡${vueltas} VOLTERETAS!`;
    aviso(E.combo > 1 ? `${titulo}<br>COMBO x${E.combo}` : titulo, `+${n} tacos` + (atras >= 1 ? ` · la bola, ${Math.round(atras)} m atrás` : ""));
    sndFanfarria(true);
  } else if (desvio < PERFECTO && E.salto > 0.5) {
    E.tacos += 2; E.perfectos++; E.s = Math.min(V_MAX, E.s + 1.5);
    aviso("¡ATERRIZAJE PERFECTO!", "+2 tacos");
    sndPoint();
  }
  if (E.buffer > 0) { E.buffer = 0; saltar(); }
}
function paso(dt) {
  E.t += dt;
  E.intocable = Math.max(0, E.intocable - dt);
  E.buffer = Math.max(0, E.buffer - dt);
  if (E.suelo) {
    // (en el borde de un cortado manda la cuesta de detrás: así se sale
    // volando y no se «esquía» por el cortado abajo)
    const pA = (suelo(E.x) - suelo(E.x - 0.1)) / 0.1, pD = (suelo(E.x + 0.1) - suelo(E.x)) / 0.1;
    const p = pD < pA - 1.5 ? pA : (pA + pD) / 2, n = Math.hypot(1, p);
    const tx = 1 / n, ty = p / n;
    if (E.tumbo > 0) { E.tumbo -= dt; E.s = Math.max(V_MIN * 0.7, E.s - 4 * dt); }
    else E.s += (G * 0.75 * (-ty) - 0.4 - 0.014 * E.s * E.s) * dt;
    E.s = Math.min(V_MAX, Math.max(E.tumbo > 0 ? 4 : V_MIN, E.s));
    const nx = E.x + E.s * tx * dt, yBal = E.y + E.s * ty * dt, yS = suelo(nx);
    E.x = nx;
    if (yBal - yS > 0.09 && E.tumbo <= 0) {
      // El suelo se va (un trampolín o un cortado): a volar.
      E.suelo = false; E.vx = E.s * tx; E.vy = E.s * ty; E.y = yBal; E.giroAcum = 0; E.salto = 0;
      E.desdeTrampolin = rasgos.some((f) => Math.abs(f.x0 - E.x) < 3);
    } else {
      E.y = yS;
      E.ang += (Math.atan(p) - E.ang) * Math.min(1, dt * 14);
    }
  } else {
    E.salto += dt;
    E.vy -= G * dt;
    E.x += E.vx * dt; E.y += E.vy * dt;
    const aS = Math.atan(pendiente(E.x));
    if (E.dedo) { E.ang += GIRO * dt; E.giroAcum += GIRO * dt; }
    else if (Math.abs(envolver(E.ang - aS)) < 1.0) E.ang += envolver(aS - E.ang) * Math.min(1, dt * 3);
    if (E.y <= suelo(E.x)) aterrizar();
  }
  // Montones y rocas: por el suelo, tortazo (saltándolos, nada).
  if (E.intocable <= 0) for (const m of obstaculos) {
    if (m.tocado || Math.abs(m.x - E.x) > 0.9) continue;
    if (E.y - suelo(m.x) < m.alto * 0.8) { m.tocado = true; chocar("¡TORTAZO!<small>TOCA para saltar</small>"); }
  }
  // Los tacos (quietos: hay que pasar por ellos).
  for (const t of tacos) {
    // (un círculo alrededor del cuerpo: con la cuesta, una caja dejaba coger
    // tacos altos sin saltar)
    if (t.cogido || Math.abs(t.x - E.x) > 1.6) continue;
    if (Math.hypot(t.x - E.x, t.y - (E.y + 1.4)) < 1.3) { t.cogido = true; t.pop = 0.001; E.tacos++; sndPoint(); }
  }
  // La bola: va cogiendo velocidad; si te alcanza, se acabó.
  E.bv = velBola(E.t);
  E.bx += E.bv * dt;
  if (E.bx < E.x - BOLA_HUECO) E.bx = E.x - BOLA_HUECO;   // (no se queda atrás: siempre aprieta)
  if (E.bx + BOLA_R * 0.7 >= E.x) acabar();
}

// ---------------------------------------------------------------- dibujo
const elDist = document.getElementById("dist"), elTacos = document.getElementById("nTacos"), elBola = document.getElementById("bola");
let reloj = 0;
function dibujar(dt) {
  reloj += dt;
  // Trozos de nieve alrededor de la cámara.
  const i0 = Math.floor((E.x - 60) / TROZO), i1 = Math.floor((E.x + 120) / TROZO);
  for (let i = i0; i <= i1; i++) if (!trozos.has(i)) crearTrozo(i);
  for (const i of [...trozos.keys()]) if (i < i0 - 1) quitarTrozo(i);
  tacos = tacos.filter((t) => { if (t.x < E.x - 60) { scene.remove(t.s); return false; } return true; });
  obstaculos = obstaculos.filter((m) => { if (m.x < E.x - 60) { scene.remove(m.m); return false; } return true; });
  // Los tacos están quietos (16/11: nada de moverse sin motivo); los cogidos
  // crecen y se deshacen.
  for (const t of tacos) {
    if (!t.pop) continue;
    t.pop += dt;
    if (!t.clonado) { t.clonado = true; t.s.material = matTaco.clone(); }
    const u = Math.min(1, t.pop / 0.28);
    t.s.scale.setScalar(1.3 * (1 + u * 0.9));
    t.s.material.opacity = 1 - u;
    if (u >= 1) { t.s.visible = false; t.pop = 0; }
  }
  // El esquiador.
  esquiador.position.set(E.x, E.y, 0);
  esquiador.rotation.z = E.tumbo > 0 ? E.ang + (0.7 - E.tumbo) * 9 : E.ang;
  // Nieve que salta de los esquís al bajar (más cuanto más rápido).
  E.rastro -= dt;
  if (E.fase === "juego" && E.suelo && E.tumbo <= 0 && E.rastro <= 0) {
    E.rastro = 0.045 - Math.min(0.025, E.s * 0.001);
    const a = E.ang;
    soltarNieve(E.x - 0.9 * Math.cos(a), E.y + 0.15, -E.s * 0.12 + (Math.random() - 0.5), 1.5 + Math.random() * 2, 0.45, 0.7);
  }
  // En el aire: la sombra de donde caes y los esquís en VERDE si ahora
  // aterrizarías bien.
  const c = E.suelo || E.fase !== "juego" ? null : caida();
  E.aterriza = c;
  if (c) {
    const aL = Math.atan(pendiente(c.x));
    sombra.visible = true;
    sombra.position.set(c.x, suelo(c.x), 0);
    sombra.rotation.z = aL;
    const bien = Math.abs(envolver(E.ang - aL)) < TOLERANCIA - 0.1;
    matEsqui.color.copy(bien ? VERDE : E.giroAcum > 0.5 ? NARANJA : ROJO);
    sombraM.scale.set(1.6, 0.6, 1);
  } else {
    // en el suelo, una sombrita bajo los esquis
    sombra.visible = true;
    sombra.position.set(E.x, E.y, 0); sombra.rotation.z = E.ang;
    sombraM.scale.set(1.3, 0.42, 1);
    matEsqui.color.copy(ROJO);
  }
  // Las huellas de los esquis en la nieve.
  if (E.fase === "juego") {
    const ult = huellaPts[huellaPts.length - 1];
    if (E.suelo && E.tumbo <= 0) {
      if (!ult || E.x - ult.x > 0.6) { huellaPts.push({ x: E.x, y: E.y, corte: !ult || huellaCorte }); huellaCorte = false; }
    } else huellaCorte = true;
    if (huellaPts.length > MAXH) huellaPts.splice(0, huellaPts.length - MAXH);
    let v = 0;
    for (let i = 1; i < huellaPts.length; i++) {
      const a = huellaPts[i - 1], b = huellaPts[i];
      if (b.corte) continue;
      for (const z of [-0.3, 0.3]) { huellaPos.set([a.x, a.y + 0.04, z, b.x, b.y + 0.04, z], v * 3); v += 2; }
    }
    huellaGeo.setDrawRange(0, v);
    huellaGeo.attributes.position.needsUpdate = true;
  }
  moverNieve(dt);
  // La bola (y la nieve que levanta).
  const yb = suelo(E.bx) + BOLA_R * 0.92;
  bola.position.set(E.bx, yb, 0.5);
  bola.userData.giro.rotation.z -= (E.bv * dt) / BOLA_R;
  E.rastroBola -= dt;
  if (E.fase === "juego" && E.rastroBola <= 0 && E.x - E.bx < 40) { E.rastroBola = 0.07; soltarNieve(E.bx - BOLA_R * 0.6, yb - BOLA_R * 0.8, -2 - Math.random() * 2, 2 + Math.random() * 2, 0.6, 1.6); }
  // Avisos para aprender (la primera vez en cada bajada).
  if (E.fase === "juego") {
    if (!E.ayudaSalto) { const m = obstaculos.find((o) => !o.tocado && o.x > E.x && o.x - E.x < E.s * 1.6); if (m) { E.ayudaSalto = true; aviso("¡TOCA para saltar!", "salta los montones y las rocas", 1600); } }
    if (!E.ayudaVuelta && !E.suelo && E.desdeTrampolin) { E.ayudaVuelta = true; aviso("¡MANTÉN el dedo!", "das la vuelta: suelta cuando los esquís estén VERDES", 2000); }
  }
  // La cámara: solo se desliza (nunca gira). En vertical, el esquiador
  // arriba a la izquierda y la ladera bajando hacia abajo a la derecha; en
  // el aire mira hacia donde vas a caer y se aleja un poco.
  // (en el aire, que se vean a la vez el esquiador y la sombra de donde cae;
  // si la caída es muy larga, la cámara se aleja)
  const objX = E.x + 7.5;
  let objY = E.y - 11, dObj = 0;
  if (c) {
    const yL = suelo(c.x), caidaM = E.y - yL;
    objY = Math.min(E.y - 9, Math.max(E.y - 15, (E.y + yL) / 2 - 2));
    dObj = Math.min(30, Math.max(0, caidaM - 18) * 1.1);
  }
  E.camX += (objX - E.camX) * Math.min(1, dt * 6);
  E.camY += (objY - E.camY) * Math.min(1, dt * 3);
  E.camD += (dObj - E.camD) * Math.min(1, dt * 1.2);
  const d = ANCHO_VISTO / (2 * Math.tan(THREE.MathUtils.degToRad(camera.fov / 2)) * camera.aspect) + E.camD;
  camera.position.set(E.camX, E.camY + 2, d);
  camera.lookAt(E.camX, E.camY, 0);
  for (const m of bosques) {
    const { P, f, dy } = m.userData;
    m.position.x = E.camX - (((E.camX * f) % P) + P) % P;
    m.position.y = E.camY + dy;
  }
  // (mirando un poco hacia abajo: el horizonte queda en el tercio de arriba,
  // con las montañas por encima de los bosques)
  camFondo.rotation.set(-0.12, 0.32 - Math.min(1, Math.max(0, E.x) / 2500) * 0.64, 0);
  horizonte.animar(dt);
  // Copos que caen despacio por delante (van con la camara: no marean).
  for (const c of copos) {
    c.position.y -= c.userData.v * dt;
    c.position.x += Math.sin(reloj * 0.8 + c.userData.f) * 0.3 * dt;
    if (c.position.y < -26) { c.position.y += 52; c.position.x = (Math.random() - 0.5) * 22; }
  }
  // Marcadores.
  const dm = Math.max(0, Math.floor(E.x));
  elDist.innerHTML = `${dm} m<small>récord ${Math.max(record, dm)} m</small>`;
  elTacos.textContent = E.tacos;
  const hueco = E.x - E.bx;
  if (hueco > 14 && E.fase === "juego") { elBola.style.display = "block"; elBola.textContent = `⚪ ¡La bola! ${Math.floor(hueco)} m`; }
  else elBola.style.display = "none";
  if (msgHasta && performance.now() > msgHasta) { elMsg.style.opacity = 0; msgHasta = 0; }
  renderer.clear();
  renderer.render(fondo, camFondo);
  renderer.clearDepth();
  renderer.render(scene, camera);
}

// ---------------------------------------------------------------- partida
const capaInicio = document.getElementById("inicio"), capaFin = document.getElementById("fin");
let finDesde = 0;
function acabar() {
  if (E.fase !== "juego") return;
  E.fase = "fin"; finDesde = performance.now();
  const d = Math.floor(E.x);
  if (d > record) { record = d; try { localStorage.setItem("esqui_record", String(d)); } catch (e) { /* sin guardar */ } }
  document.getElementById("finTexto").innerHTML =
    `Has bajado <b>${d} m</b><br>${E.tacos} tacos · ${E.vueltasTot} volteretas · combo x${E.comboMax}<br>Récord: ${record} m`;
  capaFin.classList.remove("oculto");
  nubeNieve(E.x, E.y + 1, 24, 5, 2);
  sndHit();
}
function empezar() {
  reiniciar();
  E.fase = "juego";
  capaInicio.classList.add("oculto"); capaFin.classList.add("oculto");
}
function dedoAbajo(e) {
  if (e) e.preventDefault();
  unlockAudio();
  if (E.fase === "inicio") { empezar(); return; }
  if (E.fase === "fin") { if (performance.now() - finDesde > 700) empezar(); return; }
  E.dedo = true;
  if (!saltar() && !E.suelo && E.y - suelo(E.x) < 1.2 && E.vy < 0) E.buffer = 0.18;
}
function dedoArriba() { E.dedo = false; }
window.addEventListener("pointerdown", dedoAbajo, { passive: false });
window.addEventListener("pointerup", dedoArriba);
window.addEventListener("pointercancel", dedoArriba);
window.addEventListener("keydown", (e) => { if (e.code === "Space" && !e.repeat) dedoAbajo(e); });
window.addEventListener("keyup", (e) => { if (e.code === "Space") dedoArriba(); });

let antes = performance.now(), sinDibujar = false;
function bucle(ahora) {
  const dt = Math.min(0.05, (ahora - antes) / 1000);
  antes = ahora;
  if (E.fase === "juego") {
    let resto = dt;
    while (resto > 1e-6) { const h = Math.min(1 / 120, resto); paso(h); resto -= h; if (E.fase !== "juego") break; }
  }
  if (!sinDibujar) dibujar(dt);
  requestAnimationFrame(bucle);
}

// Para las pruebas automáticas (desde la consola del navegador).
window.__esqui = {
  estado: () => ({ fase: E.fase, x: Math.round(E.x * 10) / 10, y: Math.round(E.y * 10) / 10, s: Math.round(E.s * 10) / 10, suelo: E.suelo,
    ang: Math.round(E.ang * 100) / 100, tacos: E.tacos, vueltas: E.vueltasTot, choques: E.choques, perfectos: E.perfectos, comboMax: E.comboMax, hueco: Math.round(E.x - E.bx) }),
  empezar, dedo: (on) => (on ? dedoAbajo() : dedoArriba()),
  avanzar: (seg, cada) => { for (let k = 0; k < seg * 120; k++) { if (cada) cada(); if (E.fase !== "juego") break; paso(1 / 120); } return window.__esqui.estado(); },
  sinDibujar: (v) => { sinDibujar = v; }, dibujar: (dt = 1 / 60) => dibujar(dt), suelo, pendiente, rasgos: () => rasgos, montones: () => obstaculos,
  verde: () => matEsqui.color.getHex() === VERDE.getHex(),
  tacos: () => tacos,
};

// ---------------------------------------------------------------- arranque
(async () => {
  document.getElementById("tacoImg").src = urlPegatina("taco");
  await Promise.all([cargarPersonaje(), cargarCarpeta("obstaculos", ["pino_nevado", "munieco_nieve", "monton_nieve", "bola_nieve"])]);
  vestir();
  hacerBola();
  reiniciar();
  document.getElementById("carga").remove();
  capaInicio.classList.remove("oculto");
  requestAnimationFrame(bucle);
})();
