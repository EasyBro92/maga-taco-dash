// Misiones con premio, como las de Minion Rush (22/10/2026).
//
// Siempre hay tres activas, cada una de un tipo distinto. Al cumplir una se
// cobra el premio en tacos y entra el siguiente nivel de ese mismo tipo (mas
// dificil y mejor pagado). Dos clases:
//   - "partida": hay que hacerlo en UNA partida (se empieza de cero cada vez)
//   - "total":   se va sumando entre partidas
// El progreso se guarda con el resto de la partida guardada (save.js).

import { getSave, addTacos, persistSave } from "./save.js";

const TIPOS = {
  tacos:     { clase: "partida", metas: [150, 300, 600, 1000, 1600] },
  distancia: { clase: "partida", metas: [1000, 2000, 3500, 5000, 8000] },
  saltos:    { clase: "total",   metas: [15, 40, 100, 200] },
  deslizar:  { clase: "total",   metas: [10, 30, 80, 160] },
  autobus:   { clase: "total",   metas: [2, 5, 12, 25] },
  gigante:   { clase: "total",   metas: [5, 15, 40, 80] },
  hielo:     { clase: "total",   metas: [5, 15, 40, 80] },
  cohete:    { clase: "total",   metas: [1, 3, 8, 15] },
  jefe:      { clase: "total",   metas: [1, 3, 6, 10] },
};
const PREMIOS = [60, 150, 300, 500, 800];

function estado() {
  const s = getSave();
  if (!s.misiones) {
    s.misiones = {
      activas: [{ tipo: "tacos", nivel: 0, hecho: 0 }, { tipo: "saltos", nivel: 0, hecho: 0 }, { tipo: "deslizar", nivel: 0, hecho: 0 }],
      niveles: {},
      cumplidas: 0,
    };
  }
  return s.misiones;
}

export function metaDe(m) {
  const t = TIPOS[m.tipo];
  return t.metas[Math.min(m.nivel, t.metas.length - 1)] * (m.nivel >= t.metas.length ? 1 + (m.nivel - t.metas.length + 1) * 0.5 : 1);
}
export function premioDe(m) {
  return PREMIOS[Math.min(m.nivel, PREMIOS.length - 1)];
}
export function activas() {
  return estado().activas;
}

// Se llama al empezar cada partida: las misiones "de partida" vuelven a cero.
export function empezarPartida() {
  for (const m of estado().activas) if (TIPOS[m.tipo].clase === "partida") m.hecho = 0;
}

// Avisa de que ha pasado algo. Para las de partida, `valor` es el total de
// esta partida (se queda el mayor); para las totales, lo que se suma.
// Devuelve las misiones cumplidas en este momento (para enseñar el aviso).
export function evento(tipo, valor = 1) {
  const e = estado();
  const cumplidas = [];
  for (let i = 0; i < e.activas.length; i++) {
    const m = e.activas[i];
    if (m.tipo !== tipo) continue;
    if (TIPOS[tipo].clase === "partida") m.hecho = Math.max(m.hecho, valor);
    else m.hecho += valor;
    if (m.hecho >= metaDe(m)) {
      const premio = premioDe(m);
      addTacos(premio);
      cumplidas.push({ tipo, meta: metaDe(m), premio });
      e.cumplidas++;
      e.niveles[tipo] = m.nivel + 1;
      e.activas[i] = siguiente(m.tipo);
    }
  }
  persistSave();
  return cumplidas;
}

// ---- Solo misiones que se puedan hacer (27/10/2026) ----
// Antes salian misiones imposibles: subirse a autobuses en Nueva York (alli no
// hay) o vencer al jefe sin haberlo visto nunca. main.js dice que se puede
// hacer con lo que hay abierto; las que no, se cambian por otras.
let sePuede = () => true;
export function fijarDisponibles(fn) {
  sePuede = fn;
  const e = estado();
  let cambio = false;
  for (let i = 0; i < e.activas.length; i++) {
    if (!sePuede(e.activas[i].tipo)) { e.activas[i] = siguiente(null); cambio = true; }
  }
  if (cambio) persistSave();
}

// La siguiente mision tras cumplir una: el mismo tipo un nivel mas arriba la
// mitad de las veces; si no, un tipo que no este ya entre las activas.
function siguiente(tipoCumplido) {
  const e = estado();
  const usados = new Set(e.activas.map((m) => m.tipo));
  const libres = Object.keys(TIPOS).filter((t) => !usados.has(t) && sePuede(t));
  const repetir = tipoCumplido && sePuede(tipoCumplido) && (Math.random() < 0.5 || !libres.length);
  const tipo = repetir ? tipoCumplido : libres.length ? libres[Math.floor(Math.random() * libres.length)] : "tacos";
  return { tipo, nivel: e.niveles[tipo] || 0, hecho: 0 };
}
