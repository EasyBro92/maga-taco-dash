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
const C7 = [60, 64, 67, 70], F7 = [65, 69, 72, 75], G7 = [67, 71, 74, 77], Bb = [70, 74, 77];
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
  } else if (c.timbre === "metal") {
    if (enCompas === 0 || enCompas === 3 || enCompas === 6) acorde.forEach((n) => nota(N(n - 12), t, corchea * 1.4, { tipo: "sawtooth", vol: 0.025, filtro: 1400, ataque: 0.03 }));
  } else if (enCompas % 2 === 1) acorde.forEach((n) => nota(N(n - 12), t, corchea * 0.9, { tipo: "square", vol: 0.018, filtro: 2200 }));

  // Melodia
  const m = c.melodia[paso];
  if (m) {
    const largo = c.melodia[(paso + 1) % 32] === null ? corchea * 1.8 : corchea * 0.95;
    if (c.timbre === "metal") nota(N(m), t, largo, { tipo: "sawtooth", vol: 0.06, filtro: 2400, ataque: 0.025, vibrato: 0.006 });
    else if (c.timbre === "banjo") { nota(N(m), t, 0.25, { tipo: "triangle", vol: 0.1 }); nota(N(m + 12), t, 0.1, { tipo: "square", vol: 0.02, filtro: 3000 }); }
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
let indiceVoces = null;
const archivosVoz = {}, bufferVoz = {};
let vozSonando = null;
fetch("voces/indice.json").then((r) => (r.ok ? r.json() : null)).then((j) => { indiceVoces = j; }).catch(() => {});
function limpiar(texto) {
  return texto.normalize("NFC").replace(/\p{Extended_Pictographic}|️/gu, "").replace(/\s+/g, " ").trim();
}
export async function hablar(texto) {
  if (!indiceVoces || sfxMuted) return;
  const e = indiceVoces[limpiar(texto)];
  if (!e) return;
  const [archivo, desde, largo] = e;
  try {
    const ac = audio();
    const clave = archivo + desde;
    if (!bufferVoz[clave]) {
      if (!archivosVoz[archivo]) archivosVoz[archivo] = fetch("voces/" + archivo).then((r) => r.arrayBuffer());
      const todo = await archivosVoz[archivo];
      bufferVoz[clave] = await ac.decodeAudioData(todo.slice(desde, desde + largo));
    }
    if (vozSonando) { try { vozSonando.stop(); } catch (er) {} }
    const src = ac.createBufferSource();
    src.buffer = bufferVoz[clave];
    const g = ac.createGain(); g.gain.value = 1.3;
    src.connect(g).connect(ensureSfxGain());
    src.start();
    vozSonando = src;
    // La musica baja un poco mientras habla.
    if (musicGainNode) {
      musicGainNode.gain.setTargetAtTime(volumenMusica() * 0.45, ac.currentTime, 0.05);
      musicGainNode.gain.setTargetAtTime(volumenMusica(), ac.currentTime + src.buffer.duration, 0.2);
    }
  } catch (er) {}
}
