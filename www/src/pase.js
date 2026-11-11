// El pase de campaña (11/11/2026). Isidro eligió «las recomendadas» de las
// ideas para que el juego enganche más. Es un pase de temporada:
//   - Cada mes, 30 escalones. Se suben con puntos de campaña: cada carrera
//     da puntos (metros, tacos, jefes vencidos, niveles ganados) y los retos
//     de la semana dan muchos más.
//   - Cada escalón tiene su premio (tacos, cajas, cajas de líder) y el último,
//     un líder que solo sale aquí: Boris Johnson.
//   - Tres retos cada semana (lunes a domingo), los mismos para todos.
// Al cambiar de mes empieza de cero (lo cobrado se queda).

import { getSave, persistSave } from "./save.js";
import { getLang } from "./i18n.js";

export const ESCALONES = 30;
export const PUNTOS_ESCALON = 250;
export const PUNTOS_RETO = 300;
export const LIDER_PASE = "boris";

const dosDigitos = (n) => String(n).padStart(2, "0");
function temporadaHoy(d = new Date()) { return `${d.getFullYear()}-${dosDigitos(d.getMonth() + 1)}`; }
// La semana: numero de semanas (empezando en lunes) desde el 5/1/2026.
function semanaHoy(d = new Date()) {
  const lunes0 = Date.UTC(2026, 0, 5);
  const hoy = Date.UTC(d.getFullYear(), d.getMonth(), d.getDate());
  return Math.floor((hoy - lunes0) / (7 * 86400000));
}
export function diasQuedan(d = new Date()) {
  const fin = new Date(d.getFullYear(), d.getMonth() + 1, 1);
  return Math.max(1, Math.ceil((fin - d) / 86400000));
}

function estado() {
  const s = getSave();
  const tem = temporadaHoy();
  if (!s.pase || s.pase.temporada !== tem) s.pase = { temporada: tem, puntos: 0, cobrados: [] };
  const sem = semanaHoy();
  if (!s.semana || s.semana.clave !== sem) s.semana = { clave: sem, cont: {}, hechos: [] };
  return s;
}

// ---- Premios de cada escalón ----
// tipo: "tacos" | "caja" | "cajaLider" | "lider"
export function premioEscalon(n) {
  if (n === ESCALONES) return { tipo: "lider", id: LIDER_PASE };
  if (n % 10 === 0) return { tipo: "cajaLider" };
  if (n % 5 === 0) return { tipo: "caja" };
  return { tipo: "tacos", n: 150 + 25 * n };
}

export function estadoPase() {
  const s = estado();
  const p = s.pase;
  const escalon = Math.min(ESCALONES, Math.floor(p.puntos / PUNTOS_ESCALON));
  const resto = escalon >= ESCALONES ? PUNTOS_ESCALON : p.puntos - escalon * PUNTOS_ESCALON;
  const porCobrar = [];
  for (let i = 1; i <= escalon; i++) if (!p.cobrados.includes(i)) porCobrar.push(i);
  return { puntos: p.puntos, escalon, resto, porCobrar, cobrados: p.cobrados, dias: diasQuedan(), mes: mesNombre() };
}
function mesNombre() {
  return new Date().toLocaleDateString(getLang() === "en" ? "en" : "es", { month: "long" });
}

// Suma puntos; devuelve los escalones nuevos alcanzados.
export function sumarPuntos(n) {
  const s = estado();
  const antes = Math.min(ESCALONES, Math.floor(s.pase.puntos / PUNTOS_ESCALON));
  s.pase.puntos += Math.max(0, Math.round(n));
  persistSave();
  const ahora = Math.min(ESCALONES, Math.floor(s.pase.puntos / PUNTOS_ESCALON));
  return ahora - antes;
}
// Los puntos de una carrera.
export function puntosCarrera({ metros = 0, tacos = 0, jefes = 0, ganado = false }) {
  return Math.round(metros / 20 + tacos / 4 + jefes * 60 + (ganado ? 80 : 0));
}

// Marca un escalón como cobrado (el premio lo da quien llama). Devuelve el premio o null.
export function cobrar(n) {
  const s = estado();
  const { escalon } = estadoPase();
  if (n > escalon || s.pase.cobrados.includes(n)) return null;
  s.pase.cobrados.push(n);
  persistSave();
  return premioEscalon(n);
}

// ---- Retos de la semana ----
const RETOS = [
  { tipo: "jefes", metas: [2, 3, 4], es: "Derrota {n} jefes", en: "Defeat {n} bosses" },
  { tipo: "tacos", metas: [1200, 1800, 2500], es: "Recoge {n} tacos", en: "Collect {n} tacos" },
  { tipo: "metros", metas: [8000, 12000, 16000], es: "Corre {n} metros", en: "Run {n} meters" },
  { tipo: "lanzar", metas: [25, 40, 60], es: "Lanza {n} cosas a los jefes", en: "Throw {n} things at bosses" },
  { tipo: "pelos", metas: [10, 15, 25], es: "{n} veces «¡Por los pelos!»", en: "{n} close calls" },
  { tipo: "niveles", metas: [3, 4, 6], es: "Gana {n} niveles", en: "Win {n} levels" },
  { tipo: "lider", metas: [4, 6, 8], es: "Juega {n} carreras con un líder", en: "Play {n} runs as a leader" },
  { tipo: "cajas", metas: [2, 3, 4], es: "Abre {n} cajas sorpresa", en: "Open {n} surprise boxes" },
];
export function retosSemana() {
  const s = estado();
  const k = s.semana.clave;
  // Tres distintos cada semana, siempre los mismos para esa semana.
  const orden = RETOS.map((r, i) => ({ r, i, peso: Math.sin(k * 12.9898 + i * 78.233) * 43758.5453 % 1 }))
    .sort((a, b) => a.peso - b.peso).slice(0, 3);
  return orden.map(({ r, i }) => {
    const meta = r.metas[(k + i) % r.metas.length];
    const id = r.tipo;
    return { id, meta, hecho: Math.min(meta, s.semana.cont[id] || 0), cumplido: s.semana.hechos.includes(id),
      texto: (r[getLang()] || r.es).replace("{n}", meta.toLocaleString(getLang() === "en" ? "en" : "es")) };
  });
}
// Cuenta algo para los retos; devuelve los retos que se acaban de cumplir
// (sus puntos ya van sumados al pase).
export function contar(tipo, n = 1) {
  const s = estado();
  const activos = retosSemana().filter((r) => r.id === tipo && !r.cumplido);
  if (!activos.length) return [];
  s.semana.cont[tipo] = (s.semana.cont[tipo] || 0) + n;
  const hechos = [];
  for (const r of activos) {
    if (s.semana.cont[tipo] >= r.meta) { s.semana.hechos.push(r.id); hechos.push(r); }
  }
  persistSave();
  if (hechos.length) sumarPuntos(PUNTOS_RETO * hechos.length);
  return hechos;
}
