// Las frases del presidente con voz (27/10/2026).
//
//   node herramientas/voces.mjs
//
// Dice con Piper (el programa de voces que se bajó para AlienZ, con permiso de
// Isidro del 11/10/2026) cada frase en castellano que sale en un bocadillo, y
// las deja juntas en www/voces/presidente.<huella>.mp3 con su índice en
// www/voces/indice.json ({ texto: [archivo, desde, bytes] }). El juego (audio.js)
// busca el texto del bocadillo en el índice: si está, lo dice.
//
// Usa las herramientas de z-resistance (Piper, y el paso a MP3), que están en
// este mismo PC: ver z-resistance/herramientas/voces/bajar-piper.mjs.
//
// Las frases en inglés no tienen voz: Piper solo tiene voces en castellano aquí.
import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import { spawnSync } from "node:child_process";
import { fileURLToPath, pathToFileURL } from "node:url";

const aqui = path.dirname(fileURLToPath(import.meta.url));
const raiz = path.resolve(aqui, "..");
const zr = path.resolve(raiz, "../z-resistance/herramientas/voces");
const { EJECUTABLE, modeloDe, entornoPiper } = await import(pathToFileURL(path.join(zr, "bajar-piper.mjs")));
const { leerWav, recortar, apretar, igualar, afinar, aMp3 } = await import(pathToFileURL(path.join(zr, "sonido.mjs")));

// Los textos, sacados del propio juego (asi no se desincronizan).
globalThis.localStorage = { getItem: () => null, setItem: () => {} };
Object.defineProperty(globalThis, "navigator", { value: { language: "es" }, configurable: true });
// (Node lee los .js del juego como CommonJS: se copian como .mjs para importarlos.)
fs.mkdirSync(path.join(aqui, "_voces"), { recursive: true });
const src = (f) => { const d = path.join(aqui, "_voces", f.replace(/.js$/, ".mjs")); fs.copyFileSync(path.join(raiz, "www/src", f), d); return pathToFileURL(d); };
const { FRASES } = await import(src("frases.js"));
const { CATCHPHRASES, t, setLang } = await import(src("i18n.js"));
const { NIVELES } = await import(src("levels.js"));

const limpiar = (s) => s.normalize("NFC").replace(/\p{Extended_Pictographic}|️/gu, "").replace(/\s+/g, " ").trim();
const textos = new Set();
for (const v of Object.values(FRASES.es)) for (const s of [].concat(v)) textos.add(limpiar(s));
for (const s of CATCHPHRASES.es) textos.add(limpiar(s));
for (const k of ["robaTortilla", "finCasaBlanca", "jefeLlega", "jefeVencido", "jefeEscapa"]) textos.add(limpiar(t(k)));
for (const k of ["powerupShield", "powerupMagnet", "powerupBoost", "powerupMega", "powerupFreeze", "powerupRocket"]) textos.add(limpiar(t(k) + "!"));
for (const n of NIVELES) if (n.fin) textos.add(limpiar(n.fin.es));

// Como se dice (Piper lee en castellano: las palabras inglesas, a su manera).
const DECIR = [
  [/FAKE NEWS/gi, "feik nius"], [/COVFEFE/gi, "cofefe"], [/believe me/gi, "bilív mi"], [/Huge/g, "Jiuch"], [/huge/g, "jiuch"],
  [/Burrito-Bot/g, "Burrito Bot"], [/Covfefe Boost/gi, "Cofefe bust"],
];
function comoSeDice(s) {
  let d = s;
  for (const [a, b] of DECIR) d = d.replace(a, b);
  // Las de mayusculas, en minusculas (si no, alguna la deletrea).
  if (d === d.toUpperCase()) d = d.toLowerCase();
  if (!/^[¡¿]/.test(d) && /!$/.test(d)) d = "¡" + d;
  return d;
}

// La voz: hombre de España, un poco mas grave y despacio (el tono se baja
// diciendola mas deprisa y estirandola despues, como en AlienZ).
const MODELO = "es_ES-davefx-medium", TONO = -9, RITMO = -4, HZ = 22050;
const crudo = path.join(aqui, "_voces");
fs.mkdirSync(crudo, { recursive: true });
const huella = (...c) => crypto.createHash("sha1").update(c.join("|")).digest("hex");
const lineas = [...textos].map((texto) => ({ texto, dice: comoSeDice(texto), id: huella(MODELO, TONO, RITMO, comoSeDice(texto)).slice(0, 14) }));
const wav = (l) => path.join(crudo, l.id + ".wav");
const faltan = lineas.filter((l) => !fs.existsSync(wav(l)));
if (faltan.length) {
  if (!fs.existsSync(EJECUTABLE)) throw new Error("Falta Piper: node ../z-resistance/herramientas/voces/bajar-piper.mjs");
  const largo = (1 + TONO / 100) / (1 + RITMO / 100);
  const entrada = faltan.map((l) => JSON.stringify({ text: l.dice, output_file: wav(l) })).join("\n") + "\n";
  const r = spawnSync(EJECUTABLE, ["--model", modeloDe(MODELO), "--json-input", "--length_scale", largo.toFixed(3), "--sentence_silence", "0.1", "--quiet"],
    { env: entornoPiper(), input: Buffer.from(entrada, "utf8") });
  if (r.status !== 0) throw new Error(`Piper falla (${r.status}): ${r.stderr?.toString().slice(0, 300)}`);
  console.log(`${faltan.length} frases dichas con Piper`);
}

const destino = path.join(raiz, "www/voces");
fs.mkdirSync(destino, { recursive: true });
const trozos = [], sitio = {};
let p = 0, segundos = 0;
for (const l of lineas) {
  const { hz, datos } = leerWav(wav(l));
  const d = igualar(apretar(recortar(afinar(datos, hz, HZ, 1 + TONO / 100), HZ), HZ));
  const mp3 = aMp3(d, HZ, 40);
  trozos.push(mp3);
  sitio[l.texto] = [p, mp3.length];
  p += mp3.length;
  segundos += d.length / HZ;
}
const todo = Buffer.concat(trozos);
const archivo = `presidente.${huella(todo.toString("base64")).slice(0, 8)}.mp3`;
for (const viejo of fs.readdirSync(destino)) if (viejo.endsWith(".mp3") && viejo !== archivo) fs.rmSync(path.join(destino, viejo));
fs.writeFileSync(path.join(destino, archivo), todo);
const indice = {};
for (const [texto, [desde, n]] of Object.entries(sitio)) indice[texto] = [archivo, desde, n];
fs.writeFileSync(path.join(destino, "indice.json"), JSON.stringify(indice, null, 0) + "\n");
console.log(`${lineas.length} frases, ${segundos.toFixed(0)} s, ${(todo.length / 1024).toFixed(0)} KB en www/voces/${archivo}`);
