// Las mejoras de la tienda (11/11/2026). Isidro: «la tienda sigue siendo
// floja». Como en Subway Surfers: cada potenciador se puede mejorar en cinco
// niveles (dura más), más munición para el jefe y más tacos al acabar. Así
// los tacos siempre tienen en qué gastarse y cada mejora se nota al jugar.
// Cada día una mejora sale con descuento (la oferta de hoy).

import { getSave, persistSave, spendTacos } from "./save.js";

// base: lo que vale sin mejorar; paso: lo que suma cada nivel.
export const MEJORAS = [
  { id: "iman", icono: "iman", base: 6, paso: 2, unidad: "s",
    nombre: { es: "Imán", en: "Magnet" }, texto: { es: "Atrae los tacos más rato", en: "Pulls tacos for longer" } },
  { id: "bolsillo", icono: "chile", base: 3, paso: 1, unidad: "",
    nombre: { es: "Bolsillo", en: "Pocket" }, texto: { es: "Más cosas para lanzar al jefe", en: "More things to throw at the boss" } },
  { id: "botas", icono: "botas", base: 10, paso: 2.5, unidad: "s",
    nombre: { es: "Botas de salto", en: "Jump boots" }, texto: { es: "Saltos altos más rato", en: "High jumps for longer" } },
  { id: "turbo", icono: "boost", base: 4, paso: 1, unidad: "s",
    nombre: { es: "Turbo", en: "Turbo" }, texto: { es: "Corre más rápido más rato", en: "Faster for longer" } },
  { id: "gigante", icono: "gorra", base: 7, paso: 1.5, unidad: "s",
    nombre: { es: "Presidente gigante", en: "Giant president" }, texto: { es: "Aplasta todo más rato", en: "Smash everything for longer" } },
  { id: "cohete", icono: "cohete", base: 6.5, paso: 1.2, unidad: "s",
    nombre: { es: "Cohete", en: "Rocket" }, texto: { es: "Vuela más rato", en: "Fly for longer" } },
  { id: "doble", icono: "estrella", base: 6, paso: 2, unidad: "s",
    nombre: { es: "Tacos dobles", en: "Double tacos" }, texto: { es: "La gorra de los fans dura más", en: "The fans' cap lasts longer" } },
  { id: "recaudacion", icono: "regalo", base: 0, paso: 6, unidad: "%",
    nombre: { es: "Recaudación", en: "Fundraising" }, texto: { es: "Más tacos al acabar cada carrera", en: "More tacos after every run" } },
];
export const MAX_NIVEL = 5;
const PRECIOS = [500, 1200, 2500, 5000, 9000];
export const PRECIO_CAJA = 2500;

const mejora = (id) => MEJORAS.find((m) => m.id === id);
export function nivelMejora(id) {
  return (getSave().mejoras || {})[id] || 0;
}
export function valorMejora(id, nivel = nivelMejora(id)) {
  const m = mejora(id);
  return m ? m.base + m.paso * nivel : 0;
}
// La oferta de hoy: una mejora a mitad de camino, con el 40 % de descuento.
export function ofertaHoy() {
  const libres = MEJORAS.filter((m) => nivelMejora(m.id) < MAX_NIVEL);
  if (!libres.length) return null;
  const d = new Date();
  const k = d.getFullYear() * 372 + d.getMonth() * 31 + d.getDate();
  return libres[(k * 7 + 3) % libres.length].id;
}
export function precioMejora(id) {
  const n = nivelMejora(id);
  if (n >= MAX_NIVEL) return null;
  return ofertaHoy() === id ? Math.round((PRECIOS[n] * 0.6) / 10) * 10 : PRECIOS[n];
}
export function subirMejora(id) {
  const p = precioMejora(id);
  if (p === null || !spendTacos(p)) return false;
  const s = getSave();
  s.mejoras = { ...(s.mejoras || {}), [id]: nivelMejora(id) + 1 };
  persistSave();
  return true;
}
