const KEY = "tacoDashSave_v1";

function load() {
  try {
    const raw = localStorage.getItem(KEY);
    if (!raw) return defaults();
    return { ...defaults(), ...JSON.parse(raw) };
  } catch (e) {
    return defaults();
  }
}

function defaults() {
  return {
    bestScore: 0,
    totalTacos: 0,
    playerName: "",
    ownedItems: ["suit_navy", "tie_red"],
    equipped: { suit: "suit_navy", tie: "tie_red" },
    settings: {
      musicVol: 0.8,
      sfxVol: 0.8,
      musicMuted: false,
      sfxMuted: false,
      swipeSensitivity: 28,
      graphicsQuality: "high", // low | medium | high
      selectedZone: "auto", // auto | city | desert | town | dc
    },
  };
}

let state = load();

function persist() {
  localStorage.setItem(KEY, JSON.stringify(state));
}

// Para modulos que cambian la partida guardada por dentro (misiones).
export function persistSave() {
  persist();
}

export function getSave() {
  return state;
}

export function addTacos(n) {
  state.totalTacos += n;
  persist();
  return state.totalTacos;
}

export function spendTacos(n) {
  if (state.totalTacos < n) return false;
  state.totalTacos -= n;
  persist();
  return true;
}

export function reportRunScore(score) {
  const isRecord = score > state.bestScore;
  if (isRecord) state.bestScore = score;
  persist();
  return isRecord;
}

export function setPlayerName(name) {
  state.playerName = name;
  persist();
}

export function ownItem(id) {
  if (!state.ownedItems.includes(id)) state.ownedItems.push(id);
  persist();
}

export function equipItem(slot, id) {
  state.equipped[slot] = id;
  persist();
}

export function isOwned(id) {
  return state.ownedItems.includes(id);
}

export function getSettings() {
  return state.settings;
}

export function updateSettings(partial) {
  state.settings = { ...state.settings, ...partial };
  persist();
  return state.settings;
}

export function resetProgress() {
  const settings = state.settings;
  state = defaults();
  state.settings = settings;
  persist();
  return state;
}

// ---- Niveles de la gira (24/10/2026) ----
// 27/10: cada estrella es un objetivo: llegar a la meta, llegar sin chocar ni
// una vez y encontrar las tres chapas de campaña. Lo conseguido se suma entre
// intentos (las chapas se pueden ir encontrando en partidas distintas).
// Las partidas guardadas de antes (estrellas por tacos) cuentan como «llegar».
export function getNiveles() {
  return state.niveles || {};
}
export function estrellasDe(r) {
  if (!r) return 0;
  if (r.meta === undefined) return r.superado ? 1 : 0;
  return (r.meta ? 1 : 0) + (r.sinChocar ? 1 : 0) + ((r.chapas || []).filter(Boolean).length === 3 ? 1 : 0);
}
export function guardarNivel(id, logros) {
  state.niveles = state.niveles || {};
  const a = state.niveles[id] || {};
  const chapas = [0, 1, 2].map((i) => !!(a.chapas && a.chapas[i]) || !!(logros.chapas && logros.chapas[i]));
  const n = { superado: true, meta: true, sinChocar: !!a.sinChocar || !!logros.sinChocar, chapas };
  n.estrellas = estrellasDe(n);
  state.niveles[id] = n;
  persist();
  return n;
}

// ---- Tienda (27/10/2026): lo comprado y lo puesto ----
export function getTienda() {
  if (!state.tienda) state.tienda = { tengo: ["gorra_ninguna", "traje_azul"], puesto: { gorra: "gorra_ninguna", traje: "traje_azul" } };
  return state.tienda;
}
export function comprar(id, precio) {
  const t = getTienda();
  if (t.tengo.includes(id)) return true;
  if (state.totalTacos < precio) return false;
  state.totalTacos -= precio;
  t.tengo.push(id);
  persist();
  return true;
}
export function ponerse(hueco, id) {
  getTienda().puesto[hueco] = id;
  persist();
}
