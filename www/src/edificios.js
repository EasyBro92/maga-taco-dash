import * as THREE from "../vendor/three.module.min.js";
import { medidas } from "./models.js";

// Edificios de relleno únicos (25/10/2026), montados con el kit de blender/kit.py.
//
// Isidro: «que las calles no sean genéricas sino que cada edificio sea único y
// esté siempre en el mismo punto». Cada solar trae su semilla (levels.js): con
// ella se elige el bajo, cuántas plantas y de qué estilo, la cornisa, el remate,
// el color, los toldos y el rótulo. La misma semilla da siempre el mismo
// edificio, así que la calle es siempre la misma, pero no hay dos iguales.
//
// Las piezas del kit vienen casi blancas: aquí se tiñen. Miden 20 de ancho;
// un edificio de 18 a 26 se estira un poco, y uno de 40 son dos columnas.

export const PIEZAS_KIT = [
  "bajo_tiendas", "bajo_grande", "bajo_banco",
  "planta_lisa", "planta_frontones", "planta_miradores", "planta_cristal", "planta_ladrillo", "planta_balcones",
  "cornisa_clasica", "cornisa_deco", "cornisa_simple",
  "remate_deposito", "remate_mansarda", "remate_atico", "remate_antena", "toldo_kit",
];

const BAJOS = ["bajo_tiendas", "bajo_tiendas", "bajo_grande", "bajo_banco"];
const PLANTAS = ["planta_lisa", "planta_frontones", "planta_miradores", "planta_cristal", "planta_ladrillo", "planta_balcones"];
const REMATES = ["remate_deposito", "remate_mansarda", "remate_atico", "remate_antena", null, null];
// Colores de fachada naturales (piedra, arenisca, ladrillo, revocos suaves).
const PIEDRAS = [0xf1e3c8, 0xe9d6c0, 0xd9dbe0, 0xe2d2b0, 0xcfd8de, 0xeadcb0, 0xd8c3b4, 0xc9d1c0, 0xf3ece0, 0xdcc9a8];
const LADRILLOS = [0xc8735a, 0xb8604a, 0xa85a48, 0xc98b6a, 0x9a5a50];
const TOLDOS = [0x2d5a3a, 0x7a2a32, 0x22314f, 0xb8862b, 0x8a3a6a, 0x3a6a8a, 0x2a2a2e, 0xc0532f];
const ROTULOS = ["DELI", "BAGELS", "PIZZA", "JEWELRY", "BOUTIQUE", "BOOKS", "SHOES", "PHARMACY", "CAFÉ", "FLOWERS",
  "TOYS", "BANK", "GIFTS", "HATS", "DONUTS", "CHOCOLATE", "WATCHES", "PERFUME", "TAILOR", "CANDY", "BAKERY", "MUSIC"];

const elegir = (azar, lista) => lista[Math.floor(azar() * lista.length)];

// Rotulo pintado: letras de color sobre fondo oscuro o claro.
const rotulos = {};
function texturaRotulo(texto, fondo, letra) {
  const clave = texto + fondo + letra;
  if (rotulos[clave]) return rotulos[clave];
  const c = document.createElement("canvas");
  c.width = 512; c.height = 96;
  const ctx = c.getContext("2d");
  ctx.fillStyle = fondo;
  ctx.beginPath(); ctx.roundRect(4, 4, 504, 88, 16); ctx.fill();
  ctx.font = '700 60px Fredoka, "Arial Rounded MT Bold", Arial, sans-serif';
  ctx.textAlign = "center"; ctx.textBaseline = "middle";
  ctx.fillStyle = letra;
  ctx.fillText(texto, 256, 52);
  const tex = new THREE.CanvasTexture(c);
  tex.colorSpace = THREE.SRGBColorSpace;
  tex.anisotropy = 4;
  rotulos[clave] = tex;
  return tex;
}
const rotuloGeo = new THREE.PlaneGeometry(1, 1);

function pieza(nombre, tintes, color) {
  const p = medidas("kit/" + nombre);
  if (!p) return null;
  let m = tintes.get(nombre + color);
  if (!m) {
    m = p.material.clone();
    m.color.set(color);
    tintes.set(nombre + color, m);
  }
  return new THREE.Mesh(p.geometry, m);
}

// Un edificio de `ancho` (a lo largo de la calle) a partir de un azar con semilla.
export function construirEdificio(azar, ancho, opciones = {}) {
  const g = new THREE.Group();
  const tintes = new Map();
  const columnas = ancho >= 36 ? 2 : 1;
  const anchoCol = ancho / columnas;
  const sx = anchoCol / 20;
  const planta = elegir(azar, PLANTAS);
  const esLadrillo = planta === "planta_ladrillo";
  const color = esLadrillo ? elegir(azar, LADRILLOS) : elegir(azar, PIEDRAS);
  const colorBajo = azar() < 0.5 ? color : elegir(azar, PIEDRAS);
  const bajo = elegir(azar, BAJOS);
  const minP = opciones.minPlantas ?? 3, maxP = opciones.maxPlantas ?? 10;
  const plantas = minP + Math.floor(azar() * (maxP - minP + 1));
  // A veces la primera planta (la «noble») va con frontones aunque el resto no.
  const noble = azar() < 0.35 ? "planta_frontones" : planta;
  const cornisa = planta === "planta_cristal" ? "cornisa_simple" : elegir(azar, ["cornisa_clasica", "cornisa_clasica", "cornisa_deco"]);
  const remate = elegir(azar, REMATES);
  const toldo = elegir(azar, TOLDOS);
  const rotulo = elegir(azar, ROTULOS);
  const fondoRotulo = azar() < 0.5 ? "#22304f" : "#2b2b2e";
  const letraRotulo = elegir(azar, ["#ffd23f", "#ffffff", "#f6c27a", "#e8f4ff"]);

  for (let c = 0; c < columnas; c++) {
    const col = new THREE.Group();
    col.position.x = -ancho / 2 + anchoCol * (c + 0.5);
    col.scale.x = sx;
    g.add(col);
    const b = pieza(bajo, tintes, colorBajo);
    if (b) col.add(b);
    if (bajo === "bajo_tiendas") {
      for (const x of [-6.4, 0, 6.4]) {
        const t = pieza("toldo_kit", tintes, toldo);
        if (t) { t.position.set(x, 3.25, 0); col.add(t); }
      }
      // El rotulo, en la banda de encima de los escaparates (sin estirar).
      const r = new THREE.Mesh(rotuloGeo, new THREE.MeshBasicMaterial({ map: texturaRotulo(rotulo, fondoRotulo, letraRotulo) }));
      r.scale.set(9 / sx, 0.75, 1);
      r.position.set(0, 4.17, 0.24);
      col.add(r);
    }
    let z = 4.6;
    for (let k = 0; k < plantas; k++) {
      const p = pieza(k === 0 ? noble : planta, tintes, color);
      if (p) { p.position.y = z; col.add(p); }
      z += 3.0;
    }
    const co = pieza(cornisa, tintes, color);
    if (co) { co.position.y = z; col.add(co); }
    const alto = z + 1.2;
    if (remate && c === columnas - 1) {
      const re = pieza(remate, tintes, remate === "remate_mansarda" ? 0xb8c2cc : color);
      if (re) { re.position.y = alto - (cornisa === "cornisa_simple" ? 0.7 : 0); col.add(re); }
    }
  }
  g.userData.ancho = ancho;
  g.userData.frente = 1.3;
  return g;
}
