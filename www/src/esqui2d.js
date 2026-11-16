// 16/11/2026: el esquí de Denver visto de lado (prueba de la fase 1).
//
// Isidro: «quiero cambiar la forma en la que se corre … que se vea en 2D
// esquiando con saltos». Bajada por la ladera vista de lado: tocar es
// saltar, mantener el dedo en el aire da volteretas y hay que aterrizar con
// los esquís rectos sobre la nieve. Detrás baja rodando la bola de nieve
// gigante de Denver: si te pilla, se acaba.
//
// Fase 1: la ladera, los saltos, las volteretas, los aterrizajes, los tacos,
// los montones de nieve y la bola. Lo de Denver (sus edificios, sus objetos y
// el final en el Capitolio) va en la fase 2, cuando Isidro dé el visto bueno.
//
// Nada que maree (ver la memoria «juegos sin mareo»): la cámara nunca gira,
// solo se desliza suave detrás del esquiador; nada parpadea.

import * as THREE from "../vendor/three.module.min.js";
import { cargarPersonaje, cargarCarpeta, modeloConContorno, hayModelo } from "./models.js";
import { createCharacter } from "./character.js";
import { lienzo, urlPegatina } from "./pegatinas.js";
import { sndJump, sndHit, sndPoint, sndFanfarria, unlockAudio } from "./audio.js";

// ---------------------------------------------------------------- ajustes
const G = 22;              // gravedad (algo más fuerte que la real: saltos con chispa)
const V_MIN = 9, V_MAX = 34;
const IMPULSO = 9.5;       // el salto, hacia fuera de la ladera
const GIRO = 7.6;          // volteretas: radianes por segundo con el dedo puesto
const TOLERANCIA = 0.75;   // aterrizaje bueno si los esquís no se desvían más (rad)
const PERFECTO = 0.22;
const BOLA_R = 3.2;

// ---------------------------------------------------------------- la ladera
// La altura del suelo en cada x: una bajada con lomas suaves y, cada 90-170
// m, un trampolín que acaba en un cortado (ahí se vuela).
let semilla = 7;
const azar = () => { semilla = (semilla * 16807) % 2147483647; return (semilla - 1) / 2147483646; };
let rasgos = [], rasgosHasta = 70;
function prepararRasgos(hasta) {
  while (rasgosHasta < hasta) {
    const x0 = rasgosHasta + 90 + azar() * 80;
    rasgos.push({ x0, alto: 2.2 + azar() * 1.4, largo: 8 + azar() * 3, caida: 3 + azar() * 7 });
    rasgosHasta = x0;
  }
}
function base(x) { return -0.3 * x + 4 * Math.sin(x / 31) + 1.6 * Math.sin(x / 11.3 + 1.3) + 0.6 * Math.sin(x / 4.7); }
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
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
renderer.outputColorSpace = THREE.SRGBColorSpace;
cont.prepend(renderer.domElement);
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x8ec8ec);
scene.fog = new THREE.Fog(0xc8e2f4, 90, 300);
const camera = new THREE.PerspectiveCamera(50, 2, 0.5, 600);
scene.add(new THREE.HemisphereLight(0xeaf4ff, 0x8a9ab0, 1.6));
const sol = new THREE.DirectionalLight(0xfff4e0, 1.6);
sol.position.set(-20, 40, 30);
scene.add(sol);

function medir() {
  const w = window.innerWidth, h = window.innerHeight;
  const girado = h > w;
  const W = girado ? h : w, H = girado ? w : h;
  cont.classList.toggle("girado", girado);
  cont.style.width = W + "px"; cont.style.height = H + "px";
  renderer.setSize(W, H);
  camera.aspect = W / H;
  camera.updateProjectionMatrix();
}
window.addEventListener("resize", medir);
medir();

// Los montes del fondo (las Rocosas): una tira que se repite cada P metros y
// se mueve despacio (parallax), siempre a la altura del horizonte.
function crearMontes(P, z, alto, colorBajo, colorAlto, nieve, armonicos) {
  const pos = [], col = [], c1 = new THREE.Color(colorBajo), c2 = new THREE.Color(colorAlto), cn = new THREE.Color(0xf6f8fc);
  const N = 240;
  const y = (x) => alto + armonicos.reduce((s, [k, a, f]) => s + a * Math.sin(2 * Math.PI * k * x / P + f), 0);
  for (let i = 0; i < N; i++) {
    const xa = -P + (2 * P * i) / N, xb = -P + (2 * P * (i + 1)) / N;
    const ya = y(xa), yb = y(xb), fondo = -120;
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
const montesLejos = crearMontes(900, -220, 30, 0x9ab4cc, 0xb8cce0, 44, [[3, 16, 0], [7, 9, 1], [13, 5, 2], [23, 2.5, 0.5]]);
const montesCerca = crearMontes(500, -110, 8, 0x3a6a5a, 0x5a8a7a, 99, [[4, 6, 0.3], [9, 3, 1.7], [19, 1.5, 0.9]]);

// La nieve: trozos de 50 m con la cara de delante (azulada, más oscura
// abajo), la parte de arriba (blanca) y un filo para que se lea bien.
const TROZO = 50, PASO = 0.5;
const matNieve = new THREE.MeshLambertMaterial({ vertexColors: true });
const matFilo = new THREE.MeshBasicMaterial({ color: 0x7a9cc8 });
const trozos = new Map();
const deco = [];          // pinos y muñecos de detrás (para quitarlos con su trozo)
function crearTrozo(i) {
  const x0 = i * TROZO, pos = [], col = [], filo = [];
  const arriba = new THREE.Color(0xf4f8fc), cara = new THREE.Color(0xd8e6f4), fondoC = new THREE.Color(0x9ab0cc);
  const n = TROZO / PASO;
  for (let k = 0; k < n; k++) {
    const xa = x0 + k * PASO, xb = xa + PASO, ya = suelo(xa), yb = suelo(xb);
    // cara de delante (z = 2)
    pos.push(xa, ya, 2, xa, ya - 40, 2, xb, yb - 40, 2, xa, ya, 2, xb, yb - 40, 2, xb, yb, 2);
    for (const c of [cara, fondoC, fondoC, cara, fondoC, cara]) col.push(c.r, c.g, c.b);
    // la parte de arriba (de z = 2 a z = -10)
    pos.push(xa, ya, 2, xb, yb, 2, xb, yb, -10, xa, ya, 2, xb, yb, -10, xa, ya, -10);
    for (let j = 0; j < 6; j++) col.push(arriba.r, arriba.g, arriba.b);
    filo.push(xa, ya, 2.02, xa, ya - 0.18, 2.02, xb, yb - 0.18, 2.02, xa, ya, 2.02, xb, yb - 0.18, 2.02, xb, yb, 2.02);
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
  // Pinos y algún muñeco de nieve detrás de la pista.
  let x = x0 + 3 + azar() * 6;
  while (x < x0 + TROZO) {
    const nombre = azar() < 0.85 ? "obstaculos/pino_nevado" : "obstaculos/munieco_nieve";
    if (hayModelo(nombre)) {
      const p = modeloConContorno(nombre);
      const s = nombre.includes("pino") ? 0.8 + azar() * 0.6 : 0.9;
      p.scale.setScalar(s);
      p.position.set(x, suelo(x) - 0.2, -5 - azar() * 4);
      grupo.add(p);
    }
    x += 5 + azar() * 10;
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

// ---------------------------------------------------------------- tacos y montones
const texTaco = new THREE.CanvasTexture(lienzo("taco"));
texTaco.colorSpace = THREE.SRGBColorSpace;
const matTaco = new THREE.SpriteMaterial({ map: texTaco });
let tacos = [], montones = [];
function ponerTaco(x, y) {
  const s = new THREE.Sprite(matTaco);
  s.scale.setScalar(1.1);
  s.position.set(x, y, 0.4);
  scene.add(s);
  tacos.push({ x, y, s, cogido: false });
}
function cercaDeTrampolin(x) { return rasgos.some((f) => x > f.x0 - f.largo - 14 && x < f.x0 + 26); }
function ponerCosas(x0) {
  if (x0 < 40) return;
  // Un arco de tacos por encima de cada trampolín de este trozo (el vuelo de
  // un salto normal) y filas por la nieve.
  for (const f of rasgos) {
    if (f.x0 < x0 || f.x0 >= x0 + TROZO) continue;
    const ang = Math.atan(pendiente(f.x0 - 0.3)), v = 21;
    for (let t = 0.2; t < 1.5; t += 0.18) {
      const x = f.x0 + v * Math.cos(ang) * t, y = suelo(f.x0) + v * Math.sin(ang) * t - G * t * t / 2 + 1.0;
      if (y > suelo(x) + 1.2) ponerTaco(x, y);
    }
  }
  let x = x0 + 8 + azar() * 10;
  while (x < x0 + TROZO) {
    if (!cercaDeTrampolin(x)) {
      if (azar() < 0.45 && hayModelo("obstaculos/monton_nieve")) {
        const m = modeloConContorno("obstaculos/monton_nieve");
        m.position.set(x, suelo(x) - 0.05, 0);
        m.rotation.z = Math.atan(pendiente(x));
        scene.add(m);
        montones.push({ x, alto: 0.85, m, tocado: false });
        // tacos encima: el premio por saltarlo
        for (let k = -1; k <= 1; k++) ponerTaco(x + k * 1.6, suelo(x + k * 1.6) + 2.6 - Math.abs(k) * 0.5);
      } else {
        for (let k = 0; k < 4; k++) ponerTaco(x + k * 2.2, suelo(x + k * 2.2) + 1.0);
      }
    }
    x += 16 + azar() * 22;
  }
}

// ---------------------------------------------------------------- el esquiador
const esquiador = new THREE.Group();    // gira con la ladera y con las volteretas
scene.add(esquiador);
let personaje = null;
function vestir() {
  personaje = createCharacter(null);
  personaje.object3D.rotation.y = -Math.PI / 2;    // mira hacia donde baja (+x)
  esquiador.add(personaje.object3D);
  const matEsqui = new THREE.MeshLambertMaterial({ color: 0xc8302a });
  for (const z of [-0.17, 0.17]) {
    const e = new THREE.Mesh(new THREE.BoxGeometry(1.9, 0.06, 0.12), matEsqui);
    e.position.set(0.1, 0.03, z);
    esquiador.add(e);
    const punta = new THREE.Mesh(new THREE.BoxGeometry(0.3, 0.06, 0.12), matEsqui);
    punta.position.set(1.1, 0.1, z); punta.rotation.z = 0.5;
    esquiador.add(punta);
  }
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
  for (const m of montones) scene.remove(m.m);
  tacos = []; montones = [];
  for (const i of [...trozos.keys()]) quitarTrozo(i);
  semilla = 7 + Math.floor(Math.random() * 100000);
  rasgos = []; rasgosHasta = 70;
  Object.assign(E, {
    fase: "inicio", x: 0, y: suelo(0), s: 12, vx: 12, vy: 0, ang: Math.atan(pendiente(0)), suelo: true,
    dedo: false, giroAcum: 0, tumbo: 0, intocable: 0, salto: 0, buffer: 0,
    tacos: 0, vueltasTot: 0, choques: 0, perfectos: 0, t: 0,
    bx: -45, bv: 14, camY: suelo(0), camZ: 17,
  });
}

// ---------------------------------------------------------------- avisos en pantalla
const elMsg = document.getElementById("msg");
let msgHasta = 0;
function aviso(texto, sub = "") { elMsg.innerHTML = texto + (sub ? `<small>${sub}</small>` : ""); elMsg.style.opacity = 1; msgHasta = performance.now() + 1100; }

// ---------------------------------------------------------------- física
function saltar() {
  if (!E.suelo || E.tumbo > 0) return false;
  const a = Math.atan(pendiente(E.x));
  E.vx = E.s * Math.cos(a) - IMPULSO * Math.sin(a);
  E.vy = E.s * Math.sin(a) + IMPULSO * Math.cos(a);
  E.suelo = false; E.giroAcum = 0; E.salto = 0;
  sndJump();
  return true;
}
function chocar(texto) {
  E.tumbo = 0.7; E.intocable = 1.5; E.choques++;
  E.s = Math.max(V_MIN, E.s * 0.5);
  sndHit();
  aviso(texto);
}
function aterrizar() {
  const a = Math.atan(pendiente(E.x));
  const desvio = Math.abs(envolver(E.ang - a));
  const vueltas = Math.round(E.giroAcum / (Math.PI * 2));
  const rapidez = Math.hypot(E.vx, E.vy), aLo = E.vx * Math.cos(a) + E.vy * Math.sin(a);
  E.s = Math.min(V_MAX, Math.max(V_MIN, 0.6 * rapidez + 0.4 * aLo));
  E.suelo = true; E.y = suelo(E.x); E.ang = a;
  if (desvio > TOLERANCIA) { chocar(vueltas > 0 ? "¡TORTAZO!<small>¡Aterriza con los esquís rectos!</small>" : "¡TORTAZO!"); return; }
  if (vueltas > 0) {
    const n = 5 * vueltas;
    E.tacos += n; E.vueltasTot += vueltas;
    E.s = Math.min(V_MAX, E.s + 4 * vueltas);
    aviso(vueltas === 1 ? "¡VOLTERETA!" : `¡${vueltas} VOLTERETAS!`, `+${n} tacos`);
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
    const p = pendiente(E.x), n = Math.hypot(1, p);
    const tx = 1 / n, ty = p / n;
    if (E.tumbo > 0) { E.tumbo -= dt; E.s = Math.max(V_MIN * 0.6, E.s - 6 * dt); }
    else E.s += (G * 0.55 * (-ty) - 0.4 - 0.004 * E.s * E.s) * dt;
    E.s = Math.min(V_MAX, Math.max(E.tumbo > 0 ? 4 : V_MIN, E.s));
    const nx = E.x + E.s * tx * dt, yBal = E.y + E.s * ty * dt, yS = suelo(nx);
    E.x = nx;
    if (yBal - yS > 0.09 && E.tumbo <= 0) {
      // El suelo se va (un trampolín o un cortado): a volar.
      E.suelo = false; E.vx = E.s * tx; E.vy = E.s * ty; E.y = yBal; E.giroAcum = 0; E.salto = 0;
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
  // Los montones de nieve: por el suelo, tortazo (saltándolos, nada).
  if (E.intocable <= 0) for (const m of montones) {
    if (m.tocado || Math.abs(m.x - E.x) > 0.8) continue;
    if (E.y - suelo(m.x) < m.alto * 0.8) { m.tocado = true; chocar("¡TORTAZO!<small>Salta los montones</small>"); }
  }
  // Los tacos.
  for (const t of tacos) {
    if (t.cogido || Math.abs(t.x - E.x) > 1.3) continue;
    if (Math.abs(t.y - (E.y + 1.0)) < 1.3) { t.cogido = true; t.s.visible = false; E.tacos++; sndPoint(); }
  }
  // La bola: va cogiendo velocidad; si te alcanza, se acabó.
  E.bv = 13 + E.t * 0.04;
  E.bx += E.bv * dt;
  if (E.bx < E.x - 70) E.bx = E.x - 70;   // (no se queda demasiado atrás: siempre aprieta)
  if (E.bx + BOLA_R * 0.7 >= E.x) acabar();
}

// ---------------------------------------------------------------- dibujo
const elDist = document.getElementById("dist"), elTacos = document.getElementById("nTacos"), elBola = document.getElementById("bola");
function dibujar(dt) {
  // Trozos de nieve alrededor de la cámara.
  const i0 = Math.floor((E.x - 70) / TROZO), i1 = Math.floor((E.x + 160) / TROZO);
  for (let i = i0; i <= i1; i++) if (!trozos.has(i)) crearTrozo(i);
  for (const i of [...trozos.keys()]) if (i < i0 - 1) quitarTrozo(i);
  tacos = tacos.filter((t) => { if (t.x < E.x - 80) { scene.remove(t.s); return false; } return true; });
  montones = montones.filter((m) => { if (m.x < E.x - 80) { scene.remove(m.m); return false; } return true; });
  // El esquiador.
  esquiador.position.set(E.x, E.y, 0);
  esquiador.rotation.z = E.tumbo > 0 ? E.ang + (0.7 - E.tumbo) * 9 : E.ang;
  if (personaje) {
    if (E.suelo && E.tumbo <= 0) personaje.setJumpPose(0.5);
    else personaje.setJumpPose(E.dedo ? 0.5 : 0.35);
  }
  // La bola.
  bola.position.set(E.bx, suelo(E.bx) + BOLA_R * 0.92, 0.5);
  bola.userData.giro.rotation.z -= (E.bv * dt) / BOLA_R;
  // La cámara: solo se desliza (nunca gira) y se aleja un poco con la velocidad.
  // (en el aire mira a medio camino del suelo de delante: se ve donde caes)
  const objetivoY = E.suelo ? E.y : (E.y + suelo(E.x + 12)) / 2;
  E.camY += (objetivoY - E.camY) * Math.min(1, dt * 3.2);
  E.camZ += (17 + Math.min(9, Math.max(0, E.s - 14) * 0.4) - E.camZ) * Math.min(1, dt * 0.8);
  // (mirando un poco ladera abajo: el esquiador queda arriba a la izquierda
  // y se ve lo que viene)
  const cx = E.x + 8.5;
  camera.position.set(cx, E.camY - 0.6, E.camZ);
  camera.lookAt(cx, E.camY - 2.6, 0);
  for (const m of [montesLejos, montesCerca]) {
    const P = m.userData.P, f = m === montesLejos ? 0.1 : 0.3;
    m.position.x = cx - (((cx * f) % P) + P) % P;
    m.position.y = E.camY - (m === montesLejos ? 26 : 30);
  }
  // Marcadores.
  const d = Math.max(0, Math.floor(E.x));
  elDist.innerHTML = `${d} m<small>récord ${Math.max(record, d)} m</small>`;
  elTacos.textContent = E.tacos;
  const hueco = E.x - E.bx;
  if (hueco > 18 && E.fase === "juego") { elBola.style.display = "block"; elBola.textContent = `⚪ ¡La bola! ${Math.floor(hueco)} m`; }
  else elBola.style.display = "none";
  if (msgHasta && performance.now() > msgHasta) { elMsg.style.opacity = 0; msgHasta = 0; }
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
    `Has bajado <b>${d} m</b> · ${E.tacos} tacos · ${E.vueltasTot} volteretas<br>Récord: ${record} m`;
  capaFin.classList.remove("oculto");
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
    ang: Math.round(E.ang * 100) / 100, tacos: E.tacos, vueltas: E.vueltasTot, choques: E.choques, perfectos: E.perfectos, hueco: Math.round(E.x - E.bx) }),
  empezar, dedo: (on) => (on ? dedoAbajo() : dedoArriba()),
  avanzar: (seg, cada) => { for (let k = 0; k < seg * 120; k++) { if (cada) cada(); if (E.fase !== "juego") break; paso(1 / 120); } return window.__esqui.estado(); },
  sinDibujar: (v) => { sinDibujar = v; }, dibujar: () => dibujar(1 / 60), suelo, pendiente, rasgos: () => rasgos, montones: () => montones,
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
