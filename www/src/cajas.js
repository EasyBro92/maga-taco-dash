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
import { LIDERES, RAREZAS, liderLibre, darLider, ponerLider, nombreLider, tituloLider, fotoLider } from "./lideres.js";

// 10/11/2026: Isidro: «los premios se sienten muy sosos y sin ningún
// significado». Ahora la caja reparte sobre todo LÍDERES (lideres.js): cada
// uno corre con su cara y empieza las carreras con su ventaja. Los tacos
// quedan de relleno. Un líder repetido se cambia por tacos (más cuanto más
// raro). La primera caja de todas trae un líder seguro.
const PREMIOS = [
  { tacos: 100, color: "#b0c3d9", p: 28 },
  { tacos: 250, color: "#5e98d9", p: 20 },
  { tacos: 600, color: "#8847ff", p: 8 },
  { lider: "raro", color: RAREZAS.raro.color, p: 26 },
  { lider: "epico", color: RAREZAS.epico.color, p: 13 },
  { lider: "legendario", color: RAREZAS.legendario.color, p: 5 },
];
const REPETIDO = { raro: 800, epico: 1500, legendario: 3000 };
const unoDe = (rareza) => { const de = LIDERES.filter((x) => x.rareza === rareza); return de[Math.floor(Math.random() * de.length)]; };

// 11/11: la caja de lider (dia 7 de la racha y algunos escalones del pase):
// trae seguro un lider que no se tenga (si ya estan todos, 3000 tacos).
export function cajasPendientes() {
  const s = getSave();
  return (s.cajas || 0) + (s.cajasLider || 0);
}
export function guardarCaja(tipo) {
  const s = getSave();
  if (tipo === "lider") s.cajasLider = (s.cajasLider || 0) + 1;
  else s.cajas = (s.cajas || 0) + 1;
  persistSave();
}
function liderSeguro() {
  const r = Math.random();
  const orden = r < 0.12 ? ["legendario", "epico", "raro"] : r < 0.42 ? ["epico", "raro", "legendario"] : ["raro", "epico", "legendario"];
  for (const rz of orden) { const l = liderLibre(rz); if (l) return { premio: PREMIOS.find((p) => p.lider === rz), lider: l }; }
  return null;
}

function sortear() {
  const total = PREMIOS.reduce((n, p) => n + p.p, 0);
  let r = Math.random() * total;
  for (const p of PREMIOS) { if ((r -= p.p) < 0) return p; }
  return PREMIOS[0];
}
// Carta de la cinta: con un líder de esa rareza (el ganado, en la del premio).
function carta(p, l = null) {
  if (p.lider) {
    l = l || unoDe(p.lider);
    return `<div class="ruletaCarta lider" style="--c:${p.color}"><img src="${fotoLider(l.id)}" alt=""><span>${l.corto}</span></div>`;
  }
  return `<div class="ruletaCarta" style="--c:${p.color}"><img src="${urlPegatina("taco")}" alt=""><span>${p.tacos.toLocaleString("es")}</span></div>`;
}

// Abre UNA caja: la ruleta gira, se para en el premio y se cobra.
// `alCerrar` se llama al darle a «¡Genial!» (si quedan más, se puede abrir otra).
export function abrirCaja(alCerrar) {
  const s = getSave();
  if (!s.cajas && !s.cajasLider) { if (alCerrar) alCerrar(); return; }
  const deLider = !!s.cajasLider;
  if (deLider) s.cajasLider--; else s.cajas--;
  let premio = sortear();
  let seguro = deLider ? liderSeguro() : null;
  if (deLider && !seguro) premio = { tacos: 3000, color: "#e4ae39", p: 0 };
  if (seguro) premio = seguro.premio;
  if (!s.primeraCaja) { s.primeraCaja = true; if (!seguro && liderLibre("raro")) premio = PREMIOS.find((p) => p.lider === "raro"); }
  const lider = seguro ? seguro.lider : premio.lider ? liderLibre(premio.lider) : null;
  window.dispatchEvent(new Event("cajaAbierta"));
  document.querySelector("#cajaOverlay .title").textContent = t(deLider ? "cajaLiderTitulo" : "cajaTitulo");
  // Si ya se tienen todos los de esa rareza: uno repetido, y se cambia por tacos.
  const repe = premio.lider && !lider ? unoDe(premio.lider) : null;
  const tacos = premio.lider ? (lider ? 0 : REPETIDO[premio.lider]) : premio.tacos;
  // Se cobra ya (si se cierra la app a mitad de la ruleta, no se pierde).
  if (lider) darLider(lider.id);
  if (tacos) addTacos(tacos);
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
  cinta.innerHTML = cartas.map((p, i) => carta(p, i === GANA ? lider || repe : null)).join("");
  cinta.style.transition = "none";
  cinta.style.transform = "translateX(0)";
  texto.textContent = "";
  const jugar = document.getElementById("cajaJugar");
  vale.classList.add("hidden");
  otra.classList.add("hidden");
  jugar.classList.add("hidden");
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
    if (lider) {
      const r = RAREZAS[lider.rareza];
      texto.innerHTML = `<span class="rareza" style="background:${r.color}">${r[getLang()] || r.es}</span> ${t("cajaLider")} <b>${nombreLider(lider)}</b>!<small>${tituloLider(lider)}</small>`;
      jugar.classList.remove("hidden");
      jugar.onclick = () => { ponerLider(lider.id); location.reload(); };
    } else if (repe) {
      texto.innerHTML = `${t("cajaRepetido").replace("{n}", nombreLider(repe))} <b>+${tacos.toLocaleString("es")} tacos</b>`;
    } else {
      texto.innerHTML = `${t("cajaGanas")} <b>${tacos.toLocaleString("es")} tacos</b>!`;
    }
    cinta.children[GANA].classList.add("gana");
    if (lider || tacos >= 800) sndFanfarria(true); else sndChapa();
    vibrate([20, 30, 40]);
    vale.classList.remove("hidden");
    if (cajasPendientes() > 0) {
      otra.textContent = `${t("cajaOtra")} (${cajasPendientes()})`;
      otra.classList.remove("hidden");
    }
  }
  vale.onclick = () => { ov.classList.add("hidden"); if (alCerrar) alCerrar(); };
  otra.onclick = () => abrirCaja(alCerrar);
}

// ---- Premio del día ----
// 11/11: el dia 7, una caja de lider (un lider seguro). Si se salta un dia,
// la racha vuelve al primero: por eso engancha.
const DIARIO = [100, 150, 200, 300, 400, "caja", "lider"];
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
    const dentro = p === "lider" ? `${icono("estrella")}<span>${t("liderSeguro")}</span>`
      : p === "caja" ? `${icono("regalo")}<span>+500</span>` : `<img src="${urlPegatina("taco")}" alt=""><span>${p}</span>`;
    return `<div class="diarioDia ${clase} ${p === "lider" ? "diaLider" : ""}"><small>${t("dia")} ${dia}</small>${dentro}${dia < racha ? icono("check") : ""}</div>`;
  }).join("");
  const ov = document.getElementById("diarioOverlay");
  ov.classList.remove("hidden");
  document.getElementById("diarioRecoger").onclick = () => {
    const premio = DIARIO[racha - 1];
    if (premio === "lider") guardarCaja("lider");
    else if (premio === "caja") { addTacos(500); guardarCaja(); } else addTacos(premio);
    s.diario = { dia: hoyStr, racha };
    persistSave();
    sndChapa();
    vibrate(20);
    ov.classList.add("hidden");
    if (alCerrar) alCerrar(premio === "caja" || premio === "lider");
  };
  return true;
}
