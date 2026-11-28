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

// 10/11/2026: la cuenta (cuenta.js) se entera de cada guardado para subirlo.
let alGuardar = null;
export function onGuardar(fn) { alGuardar = fn; }

function persist() {
  state.guardado = Date.now();
  localStorage.setItem(KEY, JSON.stringify(state));
  if (alGuardar) alGuardar();
}

// La partida para la nube (sin los ajustes: esos son de cada movil; ni
// `tacosNube`, que es lo que este movil sabe que hay en la nube).
export function partidaParaNube() {
  const { settings, tacosNube, ...resto } = state;
  return resto;
}
// 28/11: cuenta.js avisa de que la nube ya tiene `total` tacos de este movil
// (se apunta sin avisar de un guardado nuevo: si no, se subiria otra vez).
export function marcarSubido(total) {
  state.tacosNube = total;
  try { localStorage.setItem(KEY, JSON.stringify(state)); } catch (e) { /* sin almacenamiento */ }
}
// Junta la partida de la nube con la de este movil sin perder nada: lo mejor
// de cada nivel, todo lo comprado y los tacos y el record mas altos. De lo
// demas (misiones, cajas...) se queda la partida que tenga mas estrellas.
export function fundirPartida(n, primeraVez = false) {
  if (!n || typeof n !== "object") return false;
  const a = state;
  const estrellas = (s) => Object.values(s.niveles || {}).reduce((x, r) => x + (r.estrellas || 0), 0);
  // 28/11 (prueba con jugadores): un jugador nuevo aun no tiene niveles,
  // lideres ni mejoras; al juntar salian vacios y parecia un cambio, asi que
  // la primera vez que se abria el juego con cuenta se recargaba sin motivo.
  // Se ponen antes de comparar, y se compara sin mirar el orden de las claves.
  if (!a.niveles) a.niveles = {};
  if (!a.lideres) a.lideres = [];
  if (!a.mejoras) a.mejoras = {};
  const igualar = (x) => JSON.stringify(x, (k, v) => (v && typeof v === "object" && !Array.isArray(v)
    ? Object.fromEntries(Object.entries(v).sort(([p], [q]) => (p < q ? -1 : p > q ? 1 : 0))) : v));
  const antes = igualar(partidaParaNube());
  // 13/11 (auditoria): si las dos saben cuando se guardaron, manda la mas
  // reciente (asi lo gastado no vuelve y lo cobrado no se cobra otra vez).
  const conHora = !!(a.guardado && n.guardado);
  const nubeMejor = conHora ? n.guardado > a.guardado
    : estrellas(n) > estrellas(a) || (estrellas(n) === estrellas(a) && (n.totalTacos || 0) > (a.totalTacos || 0));
  const b = nubeMejor ? { ...defaults(), ...n } : { ...a };
  b.settings = a.settings;
  // 28/11 (prueba con jugadores): los tacos eran los de la partida mas
  // reciente entera. Quien jugaba un poco en un movil nuevo y luego entraba
  // en su cuenta perdia todos los de la nube (Marta: tenia 4.844, jugo un
  // nivel sin cuenta en el otro movil y se quedo con 2.202). Ahora: lo que
  // hay en la nube mas lo ganado (o gastado) en este movil desde la ultima vez
  // que se junto. Un movil que entra por primera vez aporta todo lo suyo. Los
  // que ya tenian cuenta antes de esto, la primera vez, como antes.
  const base = typeof a.tacosNube === "number" ? a.tacosNube : primeraVez ? 0 : null;
  b.totalTacos = base !== null ? Math.max(0, (n.totalTacos || 0) + (a.totalTacos || 0) - base)
    : conHora ? ((nubeMejor ? n : a).totalTacos || 0) : Math.max(a.totalTacos || 0, n.totalTacos || 0);
  b.tacosNube = n.totalTacos || 0;   // (lo que hay en la nube hasta que se suba lo nuevo)
  // El pase del mismo mes: los puntos mas altos y todo lo cobrado en los dos.
  if (a.pase && n.pase && a.pase.temporada === n.pase.temporada) {
    b.pase = { temporada: a.pase.temporada, puntos: Math.max(a.pase.puntos || 0, n.pase.puntos || 0),
      cobrados: [...new Set([...(a.pase.cobrados || []), ...(n.pase.cobrados || [])])] };
  }
  // Los retos de la misma semana: lo mas avanzado de cada uno.
  if (a.semana && n.semana && a.semana.clave === n.semana.clave) {
    const cont = { ...(a.semana.cont || {}) };
    for (const [k, v] of Object.entries(n.semana.cont || {})) cont[k] = Math.max(cont[k] || 0, v);
    b.semana = { clave: a.semana.clave, cont, hechos: [...new Set([...(a.semana.hechos || []), ...(n.semana.hechos || [])])] };
  }
  // El premio del dia: el del dia mas reciente (AAAA-MM-DD se compara tal cual).
  if (a.diario || n.diario) b.diario = ((a.diario || {}).dia || "") >= ((n.diario || {}).dia || "") ? a.diario : n.diario;
  b.bestScore = Math.max(a.bestScore || 0, n.bestScore || 0);
  b.ownedItems = [...new Set([...(a.ownedItems || []), ...(n.ownedItems || [])])];
  b.lideres = [...new Set([...(a.lideres || []), ...(n.lideres || [])])];
  b.mejoras = { ...(a.mejoras || {}) };
  for (const [k, v] of Object.entries(n.mejoras || {})) b.mejoras[k] = Math.max(b.mejoras[k] || 0, v);
  const niveles = {};
  for (const id of new Set([...Object.keys(a.niveles || {}), ...Object.keys(n.niveles || {})])) {
    const x = (a.niveles || {})[id], y = (n.niveles || {})[id];
    if (!x || !y) { niveles[id] = x || y; continue; }
    const r = { superado: !!(x.superado || y.superado), meta: !!(x.meta || y.meta), sinChocar: !!(x.sinChocar || y.sinChocar),
      chapas: [0, 1, 2].map((i) => !!((x.chapas || [])[i] || (y.chapas || [])[i])) };
    r.estrellas = estrellasDe(r);
    niveles[id] = r;
  }
  b.niveles = niveles;
  if (a.tienda || n.tienda) {
    const ta = a.tienda || { tengo: [], puesto: {} }, tn = n.tienda || { tengo: [], puesto: {} };
    b.tienda = { tengo: [...new Set([...(ta.tengo || []), ...(tn.tengo || [])])], puesto: (nubeMejor ? tn : ta).puesto || {} };
  }
  // (13/11: se rellena el mismo objeto: los modulos que guardaron
  // getSave() siguen viendo la partida buena.)
  for (const k of Object.keys(state)) delete state[k];
  Object.assign(state, b);
  localStorage.setItem(KEY, JSON.stringify(state));
  return igualar(partidaParaNube()) !== antes;
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
