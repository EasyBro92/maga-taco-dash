// Audio 100% sintetizado con Web Audio API, sin archivos externos.
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

function beep(freq, dur, type, vol, glide) {
  try {
    const ac = audio();
    const osc = ac.createOscillator();
    const gain = ac.createGain();
    osc.type = type || "sine";
    osc.frequency.setValueAtTime(freq, ac.currentTime);
    if (glide) osc.frequency.exponentialRampToValueAtTime(Math.max(freq + glide, 20), ac.currentTime + dur);
    gain.gain.setValueAtTime(vol || 0.2, ac.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, ac.currentTime + dur);
    osc.connect(gain).connect(ensureSfxGain());
    osc.start();
    osc.stop(ac.currentTime + dur);
  } catch (e) {}
}

export function sndTaco() {
  beep(880, 0.1, "triangle", 0.2, 400);
  setTimeout(() => beep(1200, 0.08, "triangle", 0.15, 200), 55);
}
export function sndJump() { beep(500, 0.1, "square", 0.15, 300); }
export function sndSlide() { beep(300, 0.08, "sawtooth", 0.12, -120); }
export function sndLaneSwitch() { beep(700, 0.05, "sine", 0.1, 100); }
export function sndHit() { beep(120, 0.35, "sawtooth", 0.25, -60); }
export function sndPoint() { beep(1000, 0.1, "sine", 0.15, 300); }

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
let musicVol = 0.8, musicMuted = false;

export function setSfxVolume(v) {
  sfxVol = v;
  ensureSfxGain().gain.value = sfxMuted ? 0 : sfxVol;
}
export function setSfxMuted(m) {
  sfxMuted = m;
  ensureSfxGain().gain.value = sfxMuted ? 0 : sfxVol;
}
export function setMusicVolume(v) {
  musicVol = v;
  ensureMusicGain().gain.value = musicMuted ? 0 : musicVol * 0.16;
}
export function setMusicMuted(m) {
  musicMuted = m;
  ensureMusicGain().gain.value = musicMuted ? 0 : musicVol * 0.16;
}

// ---------- Musica chiptune sintetizada (loop, sin archivos) ----------
const STEP_DUR = 60 / 140 / 2;
const LOOKAHEAD = 0.12;
// 32 pasos: primeros 16 = seccion A, siguientes 16 = seccion B (variacion)
const BASS_PATTERN = [
  110, null, 110, null, 146.83, null, 130.81, null, 110, null, 110, null, 164.81, null, 146.83, null,
  110, null, 130.81, null, 146.83, null, 110, null, 164.81, null, 174.61, null, 146.83, null, 130.81, null,
];
const LEAD_PATTERN = [
  440, null, 523.25, null, 440, null, 392, null, 493.88, null, 440, null, 392, null, 349.23, null,
  523.25, 587.33, 523.25, null, 493.88, null, 440, null, 587.33, null, 523.25, 493.88, 440, null, 392, null,
];
const KICK_STEPS = new Set([0, 8, 16, 24]);
const SNARE_STEPS = new Set([4, 12, 20, 28]);

let musicGainNode = null;
let musicTimer = null;
let nextStepTime = 0;
let stepIndex = 0;
let noiseBuffer = null;

function ensureMusicGain() {
  const ac = audio();
  if (!musicGainNode) {
    musicGainNode = ac.createGain();
    musicGainNode.gain.value = musicMuted ? 0 : musicVol * 0.16;
    musicGainNode.connect(ac.destination);
  }
  return musicGainNode;
}

function getNoiseBuffer(ac) {
  if (!noiseBuffer) {
    const len = Math.floor(ac.sampleRate * 0.2);
    noiseBuffer = ac.createBuffer(1, len, ac.sampleRate);
    const data = noiseBuffer.getChannelData(0);
    for (let i = 0; i < len; i++) data[i] = Math.random() * 2 - 1;
  }
  return noiseBuffer;
}

function kickHit(time) {
  const ac = audio();
  const o = ac.createOscillator();
  o.type = "sine";
  o.frequency.setValueAtTime(150, time);
  o.frequency.exponentialRampToValueAtTime(42, time + 0.12);
  const g = ac.createGain();
  g.gain.setValueAtTime(0.5, time);
  g.gain.exponentialRampToValueAtTime(0.001, time + 0.18);
  o.connect(g).connect(ensureMusicGain());
  o.start(time); o.stop(time + 0.2);
}

function snareHit(time) {
  const ac = audio();
  const src = ac.createBufferSource();
  src.buffer = getNoiseBuffer(ac);
  const filter = ac.createBiquadFilter();
  filter.type = "highpass";
  filter.frequency.value = 1400;
  const g = ac.createGain();
  g.gain.setValueAtTime(0.35, time);
  g.gain.exponentialRampToValueAtTime(0.001, time + 0.12);
  src.connect(filter).connect(g).connect(ensureMusicGain());
  src.start(time); src.stop(time + 0.15);
}

function scheduleStep(time) {
  const ac = audio();
  const idx = stepIndex % 32;
  if (KICK_STEPS.has(idx)) kickHit(time);
  if (SNARE_STEPS.has(idx)) snareHit(time);

  const bassFreq = BASS_PATTERN[idx];
  if (bassFreq) {
    const o = ac.createOscillator();
    o.type = "triangle";
    o.frequency.value = bassFreq;
    const g = ac.createGain();
    g.gain.setValueAtTime(0.24, time);
    g.gain.exponentialRampToValueAtTime(0.001, time + STEP_DUR * 1.6);
    o.connect(g).connect(ensureMusicGain());
    o.start(time); o.stop(time + STEP_DUR * 1.6);
  }
  const leadFreq = LEAD_PATTERN[idx];
  if (leadFreq) {
    const o = ac.createOscillator();
    o.type = "square";
    o.frequency.value = leadFreq;
    const g = ac.createGain();
    g.gain.setValueAtTime(0.11, time);
    g.gain.exponentialRampToValueAtTime(0.001, time + STEP_DUR * 0.9);
    o.connect(g).connect(ensureMusicGain());
    o.start(time); o.stop(time + STEP_DUR * 0.9);
  }
  stepIndex++;
}

export function startMusic() {
  if (musicTimer) return;
  const ac = audio();
  nextStepTime = ac.currentTime + 0.05;
  musicTimer = setInterval(() => {
    while (nextStepTime < ac.currentTime + LOOKAHEAD) {
      scheduleStep(nextStepTime);
      nextStepTime += STEP_DUR;
    }
  }, 30);
}

export function stopMusic() {
  if (musicTimer) { clearInterval(musicTimer); musicTimer = null; }
}
