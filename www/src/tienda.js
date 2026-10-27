import * as THREE from "../vendor/three.module.min.js";
import { getTienda, comprar, ponerse, getSave } from "./save.js";
import { t, getLang } from "./i18n.js";
import { icono } from "./iconos.js";
import { urlPegatina } from "./pegatinas.js";
import { modelo } from "./models.js";
import { toon } from "./toon.js";

// La tienda (27/10/2026). En la revisión: «los tacos no sirven para nada».
// Ahora se gastan en gorras y sombreros que se le ponen en la cabeza al
// presidente, en trajes de otros colores y en seguir corriendo tras chocar
// (eso va en la pantalla de choque). El panel va abajo, como el del inicio,
// para que se vea al presidente probándose lo que se toca.

const ARTICULOS = [
  { id: "gorra_ninguna", hueco: "gorra", precio: 0, nombre: { es: "Sin nada", en: "Nothing" } },
  { id: "gorra_roja", hueco: "gorra", precio: 1500, nombre: { es: "Gorra roja", en: "Red cap" } },
  { id: "vaquero", hueco: "gorra", precio: 3000, nombre: { es: "Sombrero vaquero", en: "Cowboy hat" } },
  { id: "chistera", hueco: "gorra", precio: 5000, nombre: { es: "Chistera", en: "Top hat" } },
  { id: "corona", hueco: "gorra", precio: 10000, nombre: { es: "Corona", en: "Crown" } },
  { id: "traje_azul", hueco: "traje", precio: 0, color: null, nombre: { es: "Traje azul", en: "Navy suit" } },
  { id: "traje_negro", hueco: "traje", precio: 2000, color: 0x2a2c33, nombre: { es: "Traje negro", en: "Black suit" } },
  { id: "traje_rojo", hueco: "traje", precio: 3500, color: 0xb3262c, nombre: { es: "Traje rojo", en: "Red suit" } },
  { id: "traje_blanco", hueco: "traje", precio: 6000, color: 0xe8e6e0, nombre: { es: "Traje blanco", en: "White suit" } },
  { id: "traje_dorado", hueco: "traje", precio: 12000, color: 0xd9a520, nombre: { es: "Traje dorado", en: "Gold suit" } },
];

// ---- Los sombreros (hechos aquí: pocas piezas, colores lisos) ----
// Mirando a +z y con la base en y = 0; el presidente los gira a su cabeza.
function sombrero(id) {
  if (id === "gorra_roja") {
    const g = modelo("obstaculos/gorra");
    if (g) { g.scale.setScalar(0.62); g.position.y = -0.03; }
    return g;
  }
  const g = new THREE.Group();
  const pieza = (geo, mat, y = 0, sy = 1) => { const m = new THREE.Mesh(geo, mat); m.position.y = y; m.scale.y = sy; g.add(m); return m; };
  if (id === "vaquero") {
    const piel = toon(0x8a5a2b, { shininess: 10 }), cinta = toon(0x3a2414);
    pieza(new THREE.CylinderGeometry(0.33, 0.33, 0.025, 28), piel, 0.02).scale.set(1, 1, 0.82);
    pieza(new THREE.CylinderGeometry(0.15, 0.17, 0.17, 22), piel, 0.11);
    pieza(new THREE.SphereGeometry(0.15, 22, 10, 0, Math.PI * 2, 0, Math.PI / 2), piel, 0.19, 0.35);
    pieza(new THREE.CylinderGeometry(0.172, 0.172, 0.035, 22), cinta, 0.05);
  } else if (id === "chistera") {
    const negro = toon(0x1c1d22, { shininess: 60 });
    pieza(new THREE.CylinderGeometry(0.24, 0.24, 0.02, 28), negro, 0.01).scale.set(1, 1, 0.85);
    pieza(new THREE.CylinderGeometry(0.135, 0.125, 0.3, 24), negro, 0.16);
    [0xe8463c, 0xffffff, 0x2f6bd8].forEach((c, i) => pieza(new THREE.CylinderGeometry(0.128, 0.128, 0.022, 24), toon(c), 0.045 + i * 0.022));
  } else if (id === "corona") {
    const oro = toon(0xffc23c, { shininess: 90, specular: 0x886622 });
    pieza(new THREE.CylinderGeometry(0.15, 0.14, 0.09, 24, 1, true), oro, 0.045);
    for (let i = 0; i < 6; i++) {
      const a = (i / 6) * Math.PI * 2;
      const p = new THREE.Mesh(new THREE.ConeGeometry(0.035, 0.1, 8), oro);
      p.position.set(Math.cos(a) * 0.145, 0.13, Math.sin(a) * 0.145);
      g.add(p);
      const gema = new THREE.Mesh(new THREE.SphereGeometry(0.022, 10, 8), toon([0xe8463c, 0x2f6bd8, 0x2fa84f][i % 3], { shininess: 120 }));
      gema.position.set(Math.cos(a) * 0.152, 0.05, Math.sin(a) * 0.152);
      g.add(gema);
    }
  } else return null;
  g.traverse((o) => { if (o.isMesh) o.castShadow = true; });
  return g;
}

export function aplicarTienda(character) {
  const { puesto } = getTienda();
  if (character.ponerSombrero) character.ponerSombrero(sombrero(puesto.gorra));
  const traje = ARTICULOS.find((a) => a.id === puesto.traje);
  if (character.teñirTraje) character.teñirTraje(traje ? traje.color : null);
}

// ---- El panel ----
let hueco = "gorra";
let personaje = null;
function iconoArticulo(a) {
  if (a.hueco === "traje") {
    const c = a.color === null ? "#2b3f7a" : "#" + a.color.toString(16).padStart(6, "0");
    return `<span class="muestraTraje" style="background:${c}"></span>`;
  }
  return icono({ gorra_ninguna: "cruz", gorra_roja: "gorra", vaquero: "gorra", chistera: "gorra", corona: "estrella" }[a.id]);
}
function pintar() {
  const tienda = getTienda();
  document.getElementById("shopTacoCount").textContent = getSave().totalTacos;
  const pestanas = `<div class="segmentos tiendaPestanas">
      <button class="segmento ${hueco === "gorra" ? "equippedBtn" : ""}" data-hueco="gorra">${t("tiendaGorras")}</button>
      <button class="segmento ${hueco === "traje" ? "equippedBtn" : ""}" data-hueco="traje">${t("tiendaTrajes")}</button></div>`;
  const lista = ARTICULOS.filter((a) => a.hueco === hueco).map((a) => {
    const tengo = tienda.tengo.includes(a.id);
    const puesto = tienda.puesto[a.hueco] === a.id;
    const llega = getSave().totalTacos >= a.precio;
    const boton = puesto ? `<button class="puesto">${t("tiendaPuesto")}</button>`
      : tengo ? `<button class="ponerse" data-id="${a.id}">${t("tiendaPonerse")}</button>`
      : `<button class="${llega ? "comprar" : "caro"}" data-id="${a.id}" ${llega ? "" : "disabled"}>${a.precio} <img class="peg" src="${urlPegatina("taco")}" alt=""></button>`;
    return `<div class="shopItem ${puesto ? "llevo" : ""}" data-probar="${a.id}">${iconoArticulo(a)}<div class="name">${a.nombre[getLang()] || a.nombre.es}</div>${boton}</div>`;
  }).join("");
  document.getElementById("shopGrid").innerHTML = pestanas + `<div class="tiendaLista">${lista}</div>`;
}
function probar(id) {
  const a = ARTICULOS.find((x) => x.id === id);
  if (!a || !personaje) return;
  if (a.hueco === "gorra" && personaje.ponerSombrero) personaje.ponerSombrero(sombrero(a.id));
  if (a.hueco === "traje" && personaje.teñirTraje) personaje.teñirTraje(a.color);
}
export function abrirTienda(character) {
  personaje = character;
  pintar();
  document.getElementById("startScreen").classList.add("hidden");
  document.getElementById("shopOverlay").classList.remove("hidden");
}
function cerrar() {
  aplicarTienda(personaje);   // lo que se estaba probando sin comprar, fuera
  document.getElementById("shopOverlay").classList.add("hidden");
  document.getElementById("startScreen").classList.remove("hidden");
}
document.getElementById("shopClose").addEventListener("click", cerrar);
document.getElementById("shopGrid").addEventListener("click", (e) => {
  const pest = e.target.closest("[data-hueco]");
  if (pest) { hueco = pest.dataset.hueco; aplicarTienda(personaje); pintar(); return; }
  const b = e.target.closest("button[data-id]");
  if (b) {
    const a = ARTICULOS.find((x) => x.id === b.dataset.id);
    if (b.classList.contains("comprar") && !comprar(a.id, a.precio)) return;
    ponerse(a.hueco, a.id);
    aplicarTienda(personaje);
    pintar();
    return;
  }
  const item = e.target.closest("[data-probar]");
  if (item) probar(item.dataset.probar);
});
