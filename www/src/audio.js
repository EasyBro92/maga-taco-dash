// Sonido del juego, hecho con Web Audio (sin archivos), salvo las voces.
//
// 27/10/2026: Isidro, en la revisión: «el sonido son pitidos». Los efectos
// ahora se montan con varias capas (un campanilleo para el taco, un soplido
// para saltar y agacharse, un golpe sordo al chocar, una fanfarria de metales
// al llegar) y cada nivel tiene su canción: Nueva York con swing, Ohio
// country, Washington marcha y el sin fin pop. Las frases del presidente
// tienen voz (herramientas/voces.mjs las dice con Piper y las deja en
// www/voces/); si no están, el juego sigue igual, con el bocadillo.

let actx = null;
function audio() {
  if (!actx) actx = new (window.AudioContext || window.webkitAudioContext)();
  return actx;
}

let sfxGainNode = null;
function ensureSfxGain() {
  const ac = audio();
  if (!sfxGainNode) {
    sfxGainNode = ac.createGain();
    sfxGainNode.gain.value = 0.8;
    sfxGainNode.connect(ac.destination);
  }
  return sfxGainNode;
}

// ---- Piezas para montar sonidos ----
function tono(freq, dur, { tipo = "sine", vol = 0.2, glide = 0, ataque = 0.005, cuando = 0, destino = null, filtro = 0 } = {}) {
  try {
    const ac = audio();
    const t0 = ac.currentTime + cuando;
    const osc = ac.createOscillator();
    const g = ac.createGain();
    osc.type = tipo;
    osc.frequency.setValueAtTime(freq, t0);
    if (glide) osc.frequency.exponentialRampToValueAtTime(Math.max(freq + glide, 20), t0 + dur);
    g.gain.setValueAtTime(0.0001, t0);
    g.gain.exponentialRampToValueAtTime(vol, t0 + ataque);
    g.gain.exponentialRampToValueAtTime(0.0001, t0 + dur);
    let nodo = osc;
    if (filtro) {
      const f = ac.createBiquadFilter();
      f.type = "lowpass"; f.frequency.value = filtro;
      osc.connect(f); nodo = f;
    }
    nodo.connect(g).connect(destino || ensureSfxGain());
    osc.start(t0);
    osc.stop(t0 + dur + 0.02);
  } catch (e) {}
}
let ruidoBuf = null;
function ruidoBuffer(ac) {
  if (!ruidoBuf) {
    const len = Math.floor(ac.sampleRate * 1.0);
    ruidoBuf = ac.createBuffer(1, len, ac.sampleRate);
    const d = ruidoBuf.getChannelData(0);
    for (let i = 0; i < len; i++) d[i] = Math.random() * 2 - 1;
  }
  return ruidoBuf;
}
// Ruido filtrado que barre de una frecuencia a otra: soplidos, golpes, platillos.
function soplo(dur, { desde = 800, hasta = 3000, tipo = "bandpass", vol = 0.2, q = 1.2, cuando = 0, destino = null } = {}) {
  try {
    const ac = audio();
    const t0 = ac.currentTime + cuando;
    const src = ac.createBufferSource();
    src.buffer = ruidoBuffer(ac);
    const f = ac.createBiquadFilter();
    f.type = tipo; f.Q.value = q;
    f.frequency.setValueAtTime(desde, t0);
    f.frequency.exponentialRampToValueAtTime(hasta, t0 + dur);
    const g = ac.createGain();
    g.gain.setValueAtTime(0.0001, t0);
    g.gain.exponentialRampToValueAtTime(vol, t0 + Math.min(0.03, dur * 0.3));
    g.gain.exponentialRampToValueAtTime(0.0001, t0 + dur);
    src.connect(f).connect(g).connect(destino || ensureSfxGain());
    src.start(t0, Math.random() * 0.5);
    src.stop(t0 + dur + 0.02);
  } catch (e) {}
}

// ---- Efectos ----
let tacoTono = 0, tacoUltimo = 0;
export function sndTaco() {
  // Campanilla que sube un poco en las rachas seguidas.
  const ahora = performance.now();
  tacoTono = ahora - tacoUltimo < 400 ? Math.min(7, tacoTono + 1) : 0;
  tacoUltimo = ahora;
  const f = 1046 * Math.pow(2, [0, 2, 4, 5, 7, 9, 11, 12][tacoTono] / 12);
  tono(f, 0.16, { tipo: "sine", vol: 0.14 });
  tono(f * 2, 0.1, { tipo: "sine", vol: 0.05 });
  tono(f * 1.5, 0.12, { tipo: "triangle", vol: 0.05, cuando: 0.04 });
}
export function sndJump() {
  soplo(0.22, { desde: 500, hasta: 2600, vol: 0.12 });
  tono(330, 0.18, { tipo: "triangle", vol: 0.1, glide: 260 });
}
export function sndSlide() {
  soplo(0.3, { desde: 2400, hasta: 400, vol: 0.14, q: 0.8 });
}
export function sndLaneSwitch() {
  soplo(0.12, { desde: 900, hasta: 1800, vol: 0.06, q: 2 });
}
export function sndHit() {
  tono(140, 0.4, { tipo: "sine", vol: 0.4, glide: -90 });
  soplo(0.35, { desde: 1800, hasta: 200, tipo: "lowpass", vol: 0.3, q: 0.7 });
  tono(90, 0.25, { tipo: "square", vol: 0.06, glide: -40, filtro: 600 });
}
export const sndCaida = sndHit;
// 28/10: tropezon (golpe flojo, no el de chocar) y el tic de la ruleta de la caja.
export function sndTropiezo() {
  tono(260, 0.16, { tipo: "triangle", vol: 0.22, glide: -110 });
  soplo(0.16, { desde: 1400, hasta: 300, tipo: "lowpass", vol: 0.16, q: 0.7 });
}
export function sndTic() {
  tono(2100, 0.025, { tipo: "square", vol: 0.035, filtro: 3200 });
}
export function sndPoint() {
  tono(880, 0.14, { tipo: "triangle", vol: 0.12 });
  tono(1318, 0.2, { tipo: "triangle", vol: 0.1, cuando: 0.07 });
}
export function sndChapa() {
  // Arpegio brillante: do-mi-sol-do, como una moneda especial.
  [1046, 1318, 1568, 2093].forEach((f, i) => {
    tono(f, 0.28, { tipo: "triangle", vol: 0.12, cuando: i * 0.06 });
    tono(f * 2, 0.12, { tipo: "sine", vol: 0.04, cuando: i * 0.06 });
  });
}
// Fanfarria de metales (sierra con filtro y un poco de vibrato). Corta en el sprint.
export function sndFanfarria(corta = false) {
  const notas = corta ? [[523, 0, 0.18], [659, 0.15, 0.18], [784, 0.3, 0.4]]
    : [[523, 0, 0.16], [523, 0.16, 0.16], [523, 0.32, 0.16], [659, 0.5, 0.5], [784, 1.0, 0.25], [659, 1.25, 0.2], [784, 1.45, 0.8]];
  for (const [f, t, d] of notas) {
    tono(f, d, { tipo: "sawtooth", vol: 0.09, cuando: t, ataque: 0.03, filtro: 1800 });
    tono(f / 2, d, { tipo: "sawtooth", vol: 0.05, cuando: t, ataque: 0.03, filtro: 900 });
  }
  if (!corta) soplo(1.2, { desde: 6000, hasta: 9000, tipo: "highpass", vol: 0.06, cuando: 1.45 });
}

export function vibrate(pattern) {
  try { if (navigator.vibrate) navigator.vibrate(pattern); } catch (e) {}
}

export function unlockAudio() {
  try {
    const ac = audio();
    if (ac.state === "suspended") ac.resume();
  } catch (e) {}
}

// ---------- Control de volumen (usado por el menu de ajustes) ----------
let sfxVol = 0.8, sfxMuted = false;
let musicVol = 0.8, musicMuted = false, musicaPausada = false;

export function setSfxVolume(v) {
  sfxVol = v;
  ensureSfxGain().gain.value = sfxMuted ? 0 : sfxVol;
}
export function setSfxMuted(m) {
  sfxMuted = m;
  ensureSfxGain().gain.value = sfxMuted ? 0 : sfxVol;
}
function volumenMusica() { return musicMuted || musicaPausada ? 0 : musicVol * 0.2; }
export function setMusicVolume(v) {
  musicVol = v;
  ensureMusicGain().gain.value = volumenMusica();
}
export function setMusicMuted(m) {
  musicMuted = m;
  ensureMusicGain().gain.value = volumenMusica();
}
export function pausarMusica(p) {
  musicaPausada = p;
  ensureMusicGain().gain.setTargetAtTime(volumenMusica(), audio().currentTime, 0.05);
}

// ================================================================
// ---------- Musica (27/10/2026): una cancion por nivel ----------
// Cada cancion: tempo, una progresion de acordes (4 compases), un bajo, la
// melodia y el estilo de bateria. Se toca en bucle con un programador que va
// un poco por delante del reloj de audio.
// ================================================================
const N = (nota) => 440 * Math.pow(2, (nota - 69) / 12);   // numero MIDI -> Hz
// Acordes como lista de notas MIDI.
const C = [60, 64, 67], F = [65, 69, 72], G = [67, 71, 74], Am = [69, 72, 76], Dm = [62, 65, 69], E7 = [64, 68, 71, 74];
const C7 = [60, 64, 67, 70], F7 = [65, 69, 72, 75], G7 = [67, 71, 74, 77], Bb = [70, 74, 77], D = [62, 66, 69];
const CANCIONES = {
  // Nueva York: swing de big band, bajo caminando y platillo.
  nueva_york: { bpm: 132, swing: 0.62, acordes: [C7, F7, C7, G7], bateria: "swing", bajo: "camina",
    melodia: [72, null, 75, 76, null, 79, 76, null, 77, null, 75, 72, null, 70, 72, null,
      72, null, 75, 76, null, 79, 81, null, 79, 77, 74, null, 71, null, 72, null],
    timbre: "metal" },
  // Ohio: country alegre, «boom-chic» y banjo.
  pueblo: { bpm: 150, swing: 0.5, acordes: [C, F, G, C], bateria: "country", bajo: "alterna",
    melodia: [67, 69, 72, null, 72, 74, 76, null, 74, 72, 69, null, 67, null, null, null,
      65, 67, 69, null, 72, null, 74, 76, 74, null, 71, 72, null, null, null, null],
    timbre: "banjo" },
  // Washington: marcha patriotica, caja redoblando y metales.
  washington: { bpm: 116, swing: 0.5, acordes: [C, G, C, F, C, G, F, C].slice(0, 4).concat([Bb, F, G, C]), bateria: "marcha", bajo: "marcha",
    melodia: [67, null, 72, null, 72, 74, 76, null, 76, null, 74, 72, 74, null, 67, null,
      69, null, 74, null, 74, 76, 77, null, 76, 74, 72, 71, 72, null, null, null],
    timbre: "metal" },
  // Phoenix: del Oeste, en menor, con trompeta de mariachi y guitarra.
  phoenix: { bpm: 124, swing: 0.5, acordes: [Am, G, F, E7], bateria: "country", bajo: "alterna",
    melodia: [69, null, 72, 76, null, 74, 72, null, 71, null, 67, 71, 74, null, null, null,
      69, null, 72, 76, null, 77, 76, 74, 72, null, 71, 68, 69, null, null, null],
    timbre: "metal" },
  // Las Vegas (29/10): orquesta de casino, swing rapido y metales de espectaculo.
  vegas: { bpm: 152, swing: 0.6, acordes: [C, F, C, G7], bateria: "swing", bajo: "camina",
    melodia: [72, 76, 79, null, 81, 79, 76, null, 77, null, 74, 77, 81, null, 79, null,
      72, 76, 79, null, 84, null, 83, 81, 79, null, 76, 74, 72, null, null, null],
    timbre: "metal" },
  // Des Moines (01/11): folk del Medio Oeste en invierno, alegre y con banjo.
  des_moines: { bpm: 138, swing: 0.5, acordes: [G, C, G, D], bateria: "country", bajo: "alterna",
    melodia: [67, 71, 74, null, 74, 76, 74, 71, 72, null, 69, 72, 71, null, 67, null,
      67, 71, 74, null, 79, null, 78, 76, 74, null, 72, 69, 67, null, null, null],
    timbre: "banjo" },
  // Omaha (08/11): country de la pradera al atardecer, con banjo.
  omaha: { bpm: 128, swing: 0.55, acordes: [G, C, D, G], bateria: "country", bajo: "alterna",
    melodia: [67, null, 71, 74, null, 71, 69, null, 67, null, 64, 67, 69, null, null, null,
      67, null, 71, 74, null, 76, 74, 71, 72, null, 71, 69, 67, null, null, null],
    timbre: "banjo" },
  // Wichita (08/11): llanura antes de la tormenta, mas tensa (menor).
  wichita: { bpm: 126, swing: 0.5, acordes: [Am, F, C, G], bateria: "country", bajo: "alterna",
    melodia: [69, null, 72, 76, null, 74, 72, null, 69, null, 67, 69, 72, null, null, null,
      69, null, 72, 76, null, 77, 76, 74, 72, null, 71, 67, 69, null, null, null],
    timbre: "pluck" },
  // San Luis (08/11): el blues de San Luis, con swing y metales.
  san_luis: { bpm: 116, swing: 0.62, acordes: [C7, F7, C7, G7], bateria: "swing", bajo: "camina",
    melodia: [72, null, 75, 76, null, 72, 70, null, 67, null, 70, 72, null, null, null, null,
      72, null, 75, 76, null, 79, 77, 75, 72, null, 70, 67, 72, null, null, null],
    timbre: "metal" },
  // Indianápolis (08/11): rock de carreras, rapido, con metales.
  indianapolis: { bpm: 146, swing: 0.5, acordes: [D, C, G, D], bateria: "pop", bajo: "octavas",
    melodia: [74, null, 74, 76, 78, null, 76, 74, 72, null, 72, 74, 76, null, null, null,
      74, null, 74, 76, 78, 81, 79, 78, 76, null, 74, 72, 74, null, null, null],
    timbre: "metal" },
  // Detroit (08/11): soul de la Motown, con swing y bajo que camina.
  detroit: { bpm: 112, swing: 0.6, acordes: [Am, Dm, G, C], bateria: "swing", bajo: "camina",
    melodia: [76, null, 74, 72, null, 69, null, 72, 74, null, 72, 69, null, null, null, null,
      76, null, 79, 77, 76, null, 74, 72, 74, null, 76, 72, 69, null, null, null],
    timbre: "metal" },
  // Chicago (08/11): blues de Chicago, con guitarra y bajo que camina.
  chicago: { bpm: 104, swing: 0.66, acordes: [C7, F7, G7, C7], bateria: "swing", bajo: "camina",
    melodia: [67, null, 70, 72, null, 75, 72, 70, 67, null, null, 70, 72, null, null, null,
      72, null, 75, 77, null, 79, 77, 75, 72, null, 70, 67, 70, null, 67, null],
    timbre: "pluck" },
  // Milwaukee (09/11): polka de Wisconsin, con acordeon y el bajo de umpa.
  milwaukee: { bpm: 132, swing: 0.5, acordes: [C, G7, F, C], bateria: "country", bajo: "alterna",
    melodia: [72, 71, 72, 76, 79, null, 76, null, 77, 76, 74, 71, 74, null, null, null,
      72, 74, 76, 77, 79, null, 81, 79, 77, null, 76, 74, 72, null, null, null],
    timbre: "acordeon" },
  // Minneapolis (09/11): el organo de los partidos de hockey.
  minneapolis: { bpm: 138, swing: 0.5, acordes: [C, F, G, C], bateria: "pop", bajo: "octavas",
    melodia: [67, null, 72, null, 76, null, 79, null, 76, 79, null, null, null, null, null, null,
      74, null, 77, null, 81, null, 79, 77, 76, null, 74, null, 72, null, null, null],
    timbre: "organo" },
  // Sin fin y menu: pop electronico con ganas.
  sinfin: { bpm: 140, swing: 0.5, acordes: [Am, F, C, G], bateria: "pop", bajo: "octavas",
    melodia: [76, null, 76, 79, null, 76, 74, null, 72, null, 72, 74, 76, null, 72, null,
      76, null, 76, 79, null, 81, 79, null, 77, 76, 74, null, 72, null, null, null],
    timbre: "pluck" },
};

let musicGainNode = null;
let musicTimer = null;
let nextStepTime = 0;
let stepIndex = 0;
let cancion = CANCIONES.sinfin;

function ensureMusicGain() {
  const ac = audio();
  if (!musicGainNode) {
    musicGainNode = ac.createGain();
    musicGainNode.gain.value = volumenMusica();
    // Un poco de «sala»: un eco corto y suave para que no suene seco.
    const eco = ac.createDelay(); eco.delayTime.value = 0.18;
    const ecoG = ac.createGain(); ecoG.gain.value = 0.18;
    const ecoF = ac.createBiquadFilter(); ecoF.type = "lowpass"; ecoF.frequency.value = 2500;
    musicGainNode.connect(ac.destination);
    musicGainNode.connect(eco); eco.connect(ecoF).connect(ecoG).connect(ac.destination); ecoG.connect(eco);
  }
  return musicGainNode;
}

function nota(freq, t, dur, { tipo = "triangle", vol = 0.12, filtro = 0, ataque = 0.01, vibrato = 0 } = {}) {
  const ac = audio();
  const o = ac.createOscillator();
  o.type = tipo;
  o.frequency.setValueAtTime(freq, t);
  if (vibrato) {
    const lfo = ac.createOscillator(); lfo.frequency.value = 5.5;
    const lg = ac.createGain(); lg.gain.value = freq * vibrato;
    lfo.connect(lg).connect(o.frequency); lfo.start(t + 0.08); lfo.stop(t + dur + 0.05);
  }
  const g = ac.createGain();
  g.gain.setValueAtTime(0.0001, t);
  g.gain.exponentialRampToValueAtTime(vol, t + ataque);
  g.gain.exponentialRampToValueAtTime(0.0001, t + dur);
  let n = o;
  if (filtro) { const f = ac.createBiquadFilter(); f.type = "lowpass"; f.frequency.value = filtro; o.connect(f); n = f; }
  n.connect(g).connect(ensureMusicGain());
  o.start(t); o.stop(t + dur + 0.05);
}
function golpe(t, { desde = 150, hasta = 45, vol = 0.45, dur = 0.18 } = {}) {
  const ac = audio();
  const o = ac.createOscillator();
  o.frequency.setValueAtTime(desde, t);
  o.frequency.exponentialRampToValueAtTime(hasta, t + dur * 0.7);
  const g = ac.createGain();
  g.gain.setValueAtTime(vol, t);
  g.gain.exponentialRampToValueAtTime(0.001, t + dur);
  o.connect(g).connect(ensureMusicGain());
  o.start(t); o.stop(t + dur + 0.02);
}
function ruidoMusica(t, { dur = 0.1, f = 3000, tipo = "highpass", vol = 0.2 } = {}) {
  const ac = audio();
  const src = ac.createBufferSource();
  src.buffer = ruidoBuffer(ac);
  const fl = ac.createBiquadFilter(); fl.type = tipo; fl.frequency.value = f;
  const g = ac.createGain();
  g.gain.setValueAtTime(vol, t);
  g.gain.exponentialRampToValueAtTime(0.001, t + dur);
  src.connect(fl).connect(g).connect(ensureMusicGain());
  src.start(t, Math.random() * 0.5); src.stop(t + dur + 0.02);
}

// Un paso = una corchea. 8 pasos por compas; los acordes cambian cada compas.
function scheduleStep(t) {
  const c = cancion;
  const paso = stepIndex % 32;
  const compas = Math.floor(stepIndex / 8) % c.acordes.length;
  const acorde = c.acordes[compas];
  const enCompas = stepIndex % 8;
  const raiz = acorde[0] - 24;
  const corchea = 60 / c.bpm / 2;

  // Bateria
  if (c.bateria === "swing") {
    if (enCompas % 4 === 0) golpe(t, { vol: 0.3 });
    if (enCompas % 2 === 0) ruidoMusica(t, { dur: 0.22, f: 7000, vol: 0.06 });
    if (enCompas % 4 === 3) ruidoMusica(t, { dur: 0.08, f: 7000, vol: 0.05 });
    if (enCompas === 2 || enCompas === 6) ruidoMusica(t, { dur: 0.12, f: 1800, tipo: "bandpass", vol: 0.12 });
  } else if (c.bateria === "country") {
    if (enCompas % 4 === 0) golpe(t, { vol: 0.35 });
    if (enCompas % 4 === 2) ruidoMusica(t, { dur: 0.1, f: 2000, tipo: "bandpass", vol: 0.18 });
    ruidoMusica(t, { dur: 0.04, f: 8000, vol: 0.04 });
  } else if (c.bateria === "marcha") {
    if (enCompas % 4 === 0) golpe(t, { vol: 0.4, desde: 110 });
    ruidoMusica(t, { dur: 0.07, f: 1600, tipo: "bandpass", vol: enCompas % 2 ? 0.07 : 0.14 });
    if (paso === 30 || paso === 31) { ruidoMusica(t + corchea / 2, { dur: 0.06, f: 1600, tipo: "bandpass", vol: 0.12 }); }
  } else {
    if (enCompas % 2 === 0) golpe(t, { vol: 0.42 });
    if (enCompas === 2 || enCompas === 6) ruidoMusica(t, { dur: 0.14, f: 1500, tipo: "bandpass", vol: 0.2 });
    ruidoMusica(t, { dur: 0.03, f: 9000, vol: 0.05 });
  }

  // Bajo
  let nb = null;
  if (c.bajo === "camina") nb = [raiz, raiz + 4, raiz + 7, raiz + 9][Math.floor(enCompas / 2)] ;
  else if (c.bajo === "alterna") nb = enCompas % 4 === 0 ? raiz : enCompas % 4 === 2 ? raiz + 7 : null;
  else if (c.bajo === "marcha") nb = enCompas % 2 === 0 ? (enCompas % 4 === 0 ? raiz : raiz + 7) : null;
  else nb = enCompas % 2 === 0 ? raiz : raiz + 12;
  if (nb !== null && (c.bajo !== "camina" || enCompas % 2 === 0)) nota(N(nb), t, corchea * (c.bajo === "camina" ? 1.9 : 1.2), { tipo: "triangle", vol: 0.22, filtro: 900 });

  // Acordes de acompañamiento
  if (c.timbre === "banjo") {
    if (enCompas % 2 === 1) acorde.forEach((n, i) => nota(N(n), t + i * 0.012, 0.18, { tipo: "triangle", vol: 0.05 }));
  } else if (c.timbre === "organo") {
    // 09/11: el organo del pabellon: el acorde largo al empezar cada compas.
    if (enCompas === 0) acorde.forEach((n) => nota(N(n), t, corchea * 7, { tipo: "square", vol: 0.014, filtro: 2400, ataque: 0.02, vibrato: 0.006 }));
  } else if (c.timbre === "acordeon") {
    // 09/11: el umpa de la polka: el acorde en cada contratiempo.
    if (enCompas % 2 === 1) acorde.forEach((n) => nota(N(n), t, corchea * 0.7, { tipo: "sawtooth", vol: 0.02, filtro: 1600, ataque: 0.01 }));
  } else if (c.timbre === "metal") {
    if (enCompas === 0 || enCompas === 3 || enCompas === 6) acorde.forEach((n) => nota(N(n - 12), t, corchea * 1.4, { tipo: "sawtooth", vol: 0.025, filtro: 1400, ataque: 0.03 }));
  } else if (enCompas % 2 === 1) acorde.forEach((n) => nota(N(n - 12), t, corchea * 0.9, { tipo: "square", vol: 0.018, filtro: 2200 }));

  // Melodia
  const m = c.melodia[paso];
  if (m) {
    const largo = c.melodia[(paso + 1) % 32] === null ? corchea * 1.8 : corchea * 0.95;
    if (c.timbre === "metal") nota(N(m), t, largo, { tipo: "sawtooth", vol: 0.06, filtro: 2400, ataque: 0.025, vibrato: 0.006 });
    else if (c.timbre === "banjo") { nota(N(m), t, 0.25, { tipo: "triangle", vol: 0.1 }); nota(N(m + 12), t, 0.1, { tipo: "square", vol: 0.02, filtro: 3000 }); }
    else if (c.timbre === "organo") { nota(N(m), t, largo, { tipo: "square", vol: 0.035, filtro: 2800, vibrato: 0.01 }); nota(N(m + 12), t, largo, { tipo: "sine", vol: 0.02 }); }
    else if (c.timbre === "acordeon") { nota(N(m), t, largo, { tipo: "sawtooth", vol: 0.04, filtro: 2200, vibrato: 0.008 }); nota(N(m - 12), t, largo, { tipo: "square", vol: 0.015, filtro: 1800 }); }
    else nota(N(m), t, largo, { tipo: "square", vol: 0.04, filtro: 3200 });
  }
  stepIndex++;
}

export function startMusic(nombre) {
  cancion = CANCIONES[nombre] || cancion;
  if (musicTimer) return;
  const ac = audio();
  nextStepTime = ac.currentTime + 0.08;
  stepIndex = 0;
  musicTimer = setInterval(() => {
    const corchea = 60 / cancion.bpm / 2;
    while (nextStepTime < ac.currentTime + 0.15) {
      // Swing: la corchea de la parte debil se retrasa un poco.
      const swing = stepIndex % 2 === 1 ? (cancion.swing - 0.5) * corchea * 2 : 0;
      scheduleStep(nextStepTime + swing);
      nextStepTime += corchea;
    }
  }, 30);
}

export function stopMusic() {
  if (musicTimer) { clearInterval(musicTimer); musicTimer = null; }
}

// ================================================================
// ---------- Voces (27/10/2026) ----------
// voces/indice.json: { texto: [archivo, desde, cuantos bytes] }. Cada frase es
// un trozo de MP3 dentro de un archivo; se decodifica la primera vez que hace
// falta. Si no hay voces (o es otra frase), no pasa nada.
// ================================================================
//
// 05/11/2026, el director de voces. Isidro: «las voces no acaban de sonar
// cuando toca, dicen cosas repetidas o no acaban la locución». Antes cada
// frase nueva cortaba la de antes, y cada una se bajaba y preparaba la
// primera vez que hacia falta (en el movil llegaba tarde). Ahora:
//   - se preparan todas al empezar la partida (precargarVoces);
//   - nada corta a nada: si ya esta hablando, la frase nueva espera su turno
//     un poco o se queda sin decir si es de las menos importantes;
//   - entre frase y frase hay un respiro, mas largo para las de animo;
//   - el globo sale cuando empieza a sonar y dura lo que dura la voz.
// Prioridades: 3 el jefe y la meta · 2 el microfono y «CHINA!» ·
//              1 potenciadores y avisos · 0 las de animo.
let indiceVoces = null;
const archivosVoz = {}, bufferVoz = {};
let vozSonando = null, ocupadaHasta = 0, pendiente = null, temporizador = null;
const RESPIRO = [5, 0.5, 0.3, 0.2];     // silencio que pide antes de sonar, segun la prioridad
const ESPERA = [0, 1.2, 2.5, 3];        // lo que puede esperar su turno sin perder sentido
// 31/10: y las de su voz de verdad (herramientas/trump.mjs), en su propio indice.
const vocesListas = Promise.all(["voces/indice.json", "voces/trump.json"].map((u) => fetch(u).then((r) => (r.ok ? r.json() : {})).catch(() => ({}))))
  .then(([a, b]) => { indiceVoces = { ...a, ...b }; });
function limpiar(texto) {
  return texto.normalize("NFC").replace(/\p{Extended_Pictographic}|️/gu, "").replace(/\s+/g, " ").trim();
}
const ahora = () => performance.now() / 1000;
function preparar(e) {
  const [archivo, desde, largo] = e, clave = archivo + desde;
  if (!bufferVoz[clave]) {
    if (!archivosVoz[archivo]) archivosVoz[archivo] = fetch("voces/" + archivo).then((r) => r.arrayBuffer());
    bufferVoz[clave] = archivosVoz[archivo]
      .then((todo) => audio().decodeAudioData(todo.slice(desde, desde + largo)))
      .then((b) => (bufferVoz[clave] = b))
      .catch(() => { delete bufferVoz[clave]; });
  }
  return bufferVoz[clave];
}
// Todas listas antes de que hagan falta (al empezar cada partida; la segunda vez no hace nada).
export async function precargarVoces() {
  await vocesListas;
  for (const e of Object.values(indiceVoces || {})) { try { await preparar(e); } catch (er) {} }
}
// La voz ya preparada de un texto (o null si no tiene, o aun no esta).
function vozDe(texto) {
  const e = indiceVoces && indiceVoces[limpiar(texto)];
  if (!e) return null;
  const b = preparar(e);
  return b instanceof AudioBuffer ? b : null;
}
function sonar(item) {
  const b = sfxMuted ? null : vozDe(item.texto);
  let dura = item.ms / 1000;
  if (b) {
    try {
      const ac = audio();
      const src = ac.createBufferSource();
      src.buffer = b;
      const g = ac.createGain(); g.gain.value = 1.3;
      src.connect(g).connect(ensureSfxGain());
      src.start();
      vozSonando = src;
      src.onended = () => { if (vozSonando === src) vozSonando = null; };
      // La musica baja un poco mientras habla.
      if (musicGainNode) {
        musicGainNode.gain.setTargetAtTime(volumenMusica() * 0.45, ac.currentTime, 0.05);
        musicGainNode.gain.setTargetAtTime(volumenMusica(), ac.currentTime + b.duration, 0.2);
      }
      dura = Math.max(dura, b.duration + 0.4);
      ocupadaHasta = ahora() + b.duration;
    } catch (er) { ocupadaHasta = ahora() + dura * 0.7; }
  } else ocupadaHasta = ahora() + dura * 0.7;   // un globo sin voz tambien pide su rato
  if (item.alEmpezar) item.alEmpezar(dura);
}
function libre(p) { return ahora() >= ocupadaHasta + RESPIRO[p]; }
function siguiente() {
  temporizador = null;
  const item = pendiente;
  if (!item) return;
  if (ahora() > item.caduca) { pendiente = null; return; }
  if (libre(item.prioridad)) { pendiente = null; sonar(item); return; }
  temporizador = setTimeout(siguiente, Math.max(30, (ocupadaHasta + RESPIRO[item.prioridad] - ahora()) * 1000));
}
// Dice un texto (si tiene voz) y avisa con alEmpezar(segundos) cuando empieza,
// para sacar el globo a la vez. Devuelve false si se queda sin decir.
export function decir(texto, prioridad = 1, alEmpezar = null, ms = 1300) {
  const item = { texto, prioridad, alEmpezar, ms, caduca: ahora() + ESPERA[prioridad] };
  if (!pendiente && libre(prioridad)) { sonar(item); return true; }
  if (prioridad === 0 || (pendiente && pendiente.prioridad > prioridad)) return false;
  pendiente = item;
  if (!temporizador) siguiente();
  return true;
}
// Lo de antes, para las frases del microfono (sin globo: salen volando por la pista).
export function hablar(texto, prioridad = 2) { return decir(texto, prioridad); }
// Al empezar otra partida, nada de la anterior se queda sonando ni esperando.
export function callarVoces() {
  if (vozSonando) { try { vozSonando.stop(); } catch (er) {} vozSonando = null; }
  pendiente = null; ocupadaHasta = 0;
  if (temporizador) { clearTimeout(temporizador); temporizador = null; }
}

// ---------- La sirena de la policia (Phoenix, 27/10/2026) ----------
// Un aullido que sube y baja mientras te persiguen; suave, para no tapar la musica.
let sirenaNodos = null;
export function sirena(on) {
  try {
    const ac = audio();
    if (on && !sirenaNodos) {
      const o = ac.createOscillator(); o.type = "sawtooth"; o.frequency.value = 760;
      const lfo = ac.createOscillator(); lfo.frequency.value = 0.55;
      const lg = ac.createGain(); lg.gain.value = 170;
      lfo.connect(lg).connect(o.frequency);
      const f = ac.createBiquadFilter(); f.type = "lowpass"; f.frequency.value = 1500;
      const g = ac.createGain(); g.gain.value = 0.0001;
      g.gain.exponentialRampToValueAtTime(0.035, ac.currentTime + 0.4);
      o.connect(f).connect(g).connect(ensureSfxGain());
      o.start(); lfo.start();
      sirenaNodos = { o, lfo, g };
    } else if (!on && sirenaNodos) {
      const { o, lfo, g } = sirenaNodos;
      sirenaNodos = null;
      g.gain.setTargetAtTime(0.0001, ac.currentTime, 0.15);
      o.stop(ac.currentTime + 0.8); lfo.stop(ac.currentTime + 0.8);
    }
  } catch (e) {}
}
