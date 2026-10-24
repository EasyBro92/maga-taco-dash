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

// ---- Niveles de la gira (24/10/2026): estrellas conseguidas en cada uno ----
export function getNiveles() {
  return state.niveles || {};
}
export function guardarNivel(id, estrellas) {
  state.niveles = state.niveles || {};
  const antes = state.niveles[id] || { estrellas: 0, superado: false };
  state.niveles[id] = { estrellas: Math.max(antes.estrellas, estrellas), superado: true };
  persist();
  return state.niveles[id];
}
