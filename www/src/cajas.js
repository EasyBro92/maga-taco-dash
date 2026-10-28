// Caja sorpresa y premio del día (28/10/2026), ideas de Subway Surfers.
//
// - La caja sorpresa sale de vez en cuando en la calle (pocas: como mucho dos
//   por carrera). Se guarda al cogerla y se abre al acabar, con una ruleta de
//   premios como la de las cajas de AlienZ, que a Isidro le gustó.
// - El premio del día crece si se entra días seguidos (siete días y vuelta a
//   empezar); el séptimo trae una caja. Si se salta un día, vuelve al primero.

import { getSave, addTacos, persistSave, getTienda } from "./save.js";
import { urlPegatina } from "./pegatinas.js";
import { icono } from "./iconos.js";
import { t, getLang } from "./i18n.js";
import { sndTic, sndChapa, sndFanfarria, vibrate } from "./audio.js";

// Premios: [tacos, color de rareza, probabilidad]. El último es una prenda de
// la tienda que aún no se tenga (si ya se tiene todo, son 1500 tacos).
const PREMIOS = [
  { tacos: 50,   color: "#b0c3d9", p: 30 },
  { tacos: 100,  color: "#5e98d9", p: 25 },
  { tacos: 200,  color: "#4b69ff", p: 18 },
  { tacos: 400,  color: "#8847ff", p: 12 },
  { tacos: 800,  color: "#d32ce6", p: 7 },
  { tacos: 1500, color: "#eb4b4b", p: 3 },
  { prenda: true, color: "#e4ae39", p: 5 },
];
const PRENDAS = [
  { id: "gorra_roja", es: "Gorra roja", en: "Red cap" },
  { id: "traje_negro", es: "Traje negro", en: "Black suit" },
  { id: "vaquero", es: "Sombrero vaquero", en: "Cowboy hat" },
  { id: "traje_rojo", es: "Traje rojo", en: "Red suit" },
];

export function cajasPendientes() {
  return getSave().cajas || 0;
}
export function guardarCaja() {
  const s = getSave();
  s.cajas = (s.cajas || 0) + 1;
  persistSave();
}

function sortear() {
  const total = PREMIOS.reduce((n, p) => n + p.p, 0);
  let r = Math.random() * total;
  for (const p of PREMIOS) { if ((r -= p.p) < 0) return p; }
  return PREMIOS[0];
}
function prendaLibre() {
  const tengo = getTienda().tengo;
  return PRENDAS.find((p) => !tengo.includes(p.id)) || null;
}
function carta(p) {
  const prenda = p.prenda ? prendaLibre() : null;
  const dentro = prenda
    ? `${icono("gorra")}<span>${prenda[getLang()] || prenda.es}</span>`
    : `<img src="${urlPegatina("taco")}" alt=""><span>${(p.prenda ? 1500 : p.tacos).toLocaleString("es")}</span>`;
  return `<div class="ruletaCarta" style="--c:${p.color}">${dentro}</div>`;
}

// Abre UNA caja: la ruleta gira, se para en el premio y se cobra.
// `alCerrar` se llama al darle a «¡Genial!» (si quedan más, se puede abrir otra).
export function abrirCaja(alCerrar) {
  const s = getSave();
  if (!s.cajas) { if (alCerrar) alCerrar(); return; }
  s.cajas--;
  const premio = sortear();
  const prenda = premio.prenda ? prendaLibre() : null;
  // Se cobra ya (si se cierra la app a mitad de la ruleta, no se pierde).
  if (prenda) getTienda().tengo.push(prenda.id);
  else addTacos(premio.prenda ? 1500 : premio.tacos);
  persistSave();

  const ov = document.getElementById("cajaOverlay");
  const cinta = document.getElementById("ruletaCinta");
  const texto = document.getElementById("cajaPremio");
  const vale = document.getElementById("cajaVale");
  const otra = document.getElementById("cajaOtra");
  // 34 cartas al azar y el premio en la 30.
  const GANA = 30;
  const cartas = [];
  for (let i = 0; i < 34; i++) cartas.push(i === GANA ? premio : sortear());
  cinta.innerHTML = cartas.map(carta).join("");
  cinta.style.transition = "none";
  cinta.style.transform = "translateX(0)";
  texto.textContent = "";
  vale.classList.add("hidden");
  otra.classList.add("hidden");
  ov.classList.remove("hidden");

  const ANCHO = 92;   // carta (84) + hueco (8)
  const caja = document.querySelector("#cajaOverlay .ruleta");
  const centro = caja.clientWidth / 2;
  const desfase = (Math.random() - 0.5) * 60;   // que no pare siempre en el centro exacto
  const fin = -(GANA * ANCHO + 42 - centro + desfase);
  void cinta.offsetWidth;   // que el navegador vea la posicion de salida antes de animar
  cinta.style.transition = "transform 4.2s cubic-bezier(0.1, 0.7, 0.16, 1)";
  cinta.style.transform = `translateX(${fin}px)`;
  // Un «tic» cada vez que pasa una carta por la marca (con reloj, no con
  // fotogramas: asi acaba aunque la pantalla se apague a mitad).
  let ultima = -1;
  const t0 = performance.now();
  const reloj = setInterval(() => {
    const tr = getComputedStyle(cinta).transform;
    const x = tr && tr !== "none" ? new DOMMatrixReadOnly(tr).m41 : 0;
    const i = Math.floor((centro - x) / ANCHO);
    if (i !== ultima) { ultima = i; sndTic(); }
    if (performance.now() - t0 >= 4300) { clearInterval(reloj); terminar(); }
  }, 25);

  function terminar() {
    const nombre = prenda ? (prenda[getLang()] || prenda.es) : `${(premio.prenda ? 1500 : premio.tacos).toLocaleString("es")} tacos`;
    texto.innerHTML = `${t("cajaGanas")} <b>${nombre}</b>!`;
    cinta.children[GANA].classList.add("gana");
    if (prenda || premio.tacos >= 800) sndFanfarria(true); else sndChapa();
    vibrate([20, 30, 40]);
    vale.classList.remove("hidden");
    if (getSave().cajas > 0) {
      otra.textContent = `${t("cajaOtra")} (${getSave().cajas})`;
      otra.classList.remove("hidden");
    }
  }
  vale.onclick = () => { ov.classList.add("hidden"); if (alCerrar) alCerrar(); };
  otra.onclick = () => abrirCaja(alCerrar);
}

// ---- Premio del día ----
const DIARIO = [50, 100, 150, 200, 300, 400, "caja"];
function hoy(d = new Date()) {
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
}
// Enseña el premio si hoy aún no se ha recogido. Devuelve true si lo enseña.
export function premioDiario(alCerrar) {
  const s = getSave();
  const d = s.diario || { dia: "", racha: 0 };
  const hoyStr = hoy();
  if (d.dia === hoyStr) return false;
  const ayer = new Date(); ayer.setDate(ayer.getDate() - 1);
  const racha = d.dia === hoy(ayer) ? d.racha % 7 + 1 : 1;   // del 1 al 7
  const cont = document.getElementById("diarioDias");
  cont.innerHTML = DIARIO.map((p, i) => {
    const dia = i + 1;
    const clase = dia < racha ? "hecho" : dia === racha ? "hoy" : "";
    const dentro = p === "caja" ? `${icono("regalo")}<span>+500</span>` : `<img src="${urlPegatina("taco")}" alt=""><span>${p}</span>`;
    return `<div class="diarioDia ${clase}"><small>${t("dia")} ${dia}</small>${dentro}${dia < racha ? icono("check") : ""}</div>`;
  }).join("");
  const ov = document.getElementById("diarioOverlay");
  ov.classList.remove("hidden");
  document.getElementById("diarioRecoger").onclick = () => {
    const premio = DIARIO[racha - 1];
    if (premio === "caja") { addTacos(500); guardarCaja(); } else addTacos(premio);
    s.diario = { dia: hoyStr, racha };
    persistSave();
    sndChapa();
    vibrate(20);
    ov.classList.add("hidden");
    if (alCerrar) alCerrar(premio === "caja");
  };
  return true;
}
