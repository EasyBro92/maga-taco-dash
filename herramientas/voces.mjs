// Las frases del presidente con voz (27/10/2026).
//
//   node herramientas/voces.mjs
//
// Dice con Piper (el programa de voces que se bajó para AlienZ, con permiso de
// Isidro del 11/10/2026) cada frase que sale en un bocadillo, en castellano y
// en inglés (la voz inglesa la bajó con su permiso el 27/10/2026), y las deja
// juntas en www/voces/<idioma>.<huella>.mp3 con su índice en
// www/voces/indice.json ({ texto: [archivo, desde, bytes] }). El juego
// (audio.js) busca el texto del bocadillo en el índice: si está, lo dice.
//
// Usa las herramientas de z-resistance (Piper, sus voces y el paso a MP3),
// que están en este mismo PC: ver z-resistance/herramientas/voces/bajar-piper.mjs.
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

// Los textos, sacados del propio juego (asi no se desincronizan). Node lee los
// .js del juego como CommonJS: se copian como .mjs para importarlos.
globalThis.localStorage = { getItem: () => null, setItem: () => {} };
Object.defineProperty(globalThis, "navigator", { value: { language: "es" }, configurable: true });
globalThis.document = { querySelectorAll: () => [], getElementById: () => null };
const crudo = path.join(aqui, "_voces");
fs.mkdirSync(crudo, { recursive: true });
const src = (f) => { const d = path.join(crudo, f.replace(/\.js$/, ".mjs")); fs.copyFileSync(path.join(raiz, "www/src", f), d); return pathToFileURL(d); };
const { FRASES } = await import(src("frases.js"));
const { CATCHPHRASES, t, setLang } = await import(src("i18n.js"));

const limpiar = (s) => s.normalize("NFC").replace(/\p{Extended_Pictographic}|️/gu, "").replace(/\s+/g, " ").trim();
function textosDe(lang) {
  setLang(lang);
  const textos = new Set();
  for (const v of Object.values(FRASES[lang])) for (const s of [].concat(v)) textos.add(limpiar(s));
  for (const s of CATCHPHRASES[lang]) textos.add(limpiar(s));
  // 29/10: los del jefe en Washington y en el debate de Las Vegas. (Los textos
  // de cada nivel ya no salen de levels.js: desde la historia nueva el final
  // de cada estado es «¡X vota rojo!», que cambia con el estado.)
  for (const k of ["robaTortilla", "finCasaBlanca", "jefeLlega", "jefeVencido", "jefeEscapa", "jefeLlegaDc", "jefeVencidoDc",
    "jefeEscapaDc", "jefeLlegaVegas", "jefeVencidoVegas", "jefeEscapaVegas"]) if (t(k) !== k) textos.add(limpiar(t(k)));
  for (const k of ["powerupShield", "powerupMagnet", "powerupBoost", "powerupMega", "powerupFreeze", "powerupRocket"]) textos.add(limpiar(t(k) + "!"));
  return [...textos];
}

// Como se dice (Piper en castellano lee las palabras inglesas a su manera).
const DECIR = {
  es: [[/FAKE NEWS/gi, "feik nius"], [/COVFEFE/gi, "cofefe"], [/believe me/gi, "bilív mi"], [/Huge/g, "Jiuch"], [/huge/g, "jiuch"],
    [/Burrito-Bot/g, "Burrito Bot"], [/Covfefe Boost/gi, "Cofefe bust"]],
  en: [[/Burrito-Bot/g, "Burrito Bot"], [/COVFEFE/gi, "covfefe"]],
};
function comoSeDice(s, lang) {
  let d = s;
  for (const [a, b] of DECIR[lang]) d = d.replace(a, b);
  // Las de mayusculas, en minusculas (si no, alguna la deletrea).
  if (d === d.toUpperCase()) d = d.toLowerCase();
  if (lang === "es" && !/^[¡¿]/.test(d) && /!$/.test(d)) d = "¡" + d;
  return d;
}

// La voz de cada idioma: hombre, un poco mas grave y despacio (el tono se baja
// diciendola mas deprisa y estirandola despues, como en AlienZ).
const VOCES = {
  es: { modelo: "es_ES-davefx-medium", tono: -9, ritmo: -4 },
  en: { modelo: "en_US-ryan-medium", tono: -8, ritmo: -6 },
};
const HZ = 22050;
const huella = (...c) => crypto.createHash("sha1").update(c.join("|")).digest("hex");
const destino = path.join(raiz, "www/voces");
fs.mkdirSync(destino, { recursive: true });
const indice = {}, archivos = [];

for (const [lang, v] of Object.entries(VOCES)) {
  if (!fs.existsSync(modeloDe(v.modelo))) { console.log(`Sin la voz ${v.modelo}: las frases en ${lang} no tendran voz`); continue; }
  const lineas = textosDe(lang).map((texto) => {
    const dice = comoSeDice(texto, lang);
    return { texto, dice, id: huella(v.modelo, v.tono, v.ritmo, dice).slice(0, 14) };
  });
  const wav = (l) => path.join(crudo, l.id + ".wav");
  const faltan = lineas.filter((l) => !fs.existsSync(wav(l)));
  if (faltan.length) {
    if (!fs.existsSync(EJECUTABLE)) throw new Error("Falta Piper: node ../z-resistance/herramientas/voces/bajar-piper.mjs");
    const largo = (1 + v.tono / 100) / (1 + v.ritmo / 100);
    const entrada = faltan.map((l) => JSON.stringify({ text: l.dice, output_file: wav(l) })).join("\n") + "\n";
    const r = spawnSync(EJECUTABLE, ["--model", modeloDe(v.modelo), "--json-input", "--length_scale", largo.toFixed(3), "--sentence_silence", "0.1", "--quiet"],
      { env: entornoPiper(), input: Buffer.from(entrada, "utf8") });
    if (r.status !== 0) throw new Error(`Piper falla (${r.status}): ${r.stderr?.toString().slice(0, 300)}`);
    console.log(`${lang}: ${faltan.length} frases dichas con Piper`);
  }
  const trozos = [], sitio = {};
  let p = 0, segundos = 0;
  for (const l of lineas) {
    const { hz, datos } = leerWav(wav(l));
    const d = igualar(apretar(recortar(afinar(datos, hz, HZ, 1 + v.tono / 100), HZ), HZ));
    const mp3 = aMp3(d, HZ, 40);
    trozos.push(mp3);
    sitio[l.texto] = [p, mp3.length];
    p += mp3.length;
    segundos += d.length / HZ;
  }
  const todo = Buffer.concat(trozos);
  const archivo = `${lang}.${huella(todo.toString("base64")).slice(0, 8)}.mp3`;
  fs.writeFileSync(path.join(destino, archivo), todo);
  archivos.push(archivo);
  for (const [texto, [desde, n]] of Object.entries(sitio)) indice[texto] = [archivo, desde, n];
  console.log(`${lang}: ${lineas.length} frases, ${segundos.toFixed(0)} s, ${(todo.length / 1024).toFixed(0)} KB en www/voces/${archivo}`);
}
// Lo que ya no usa nadie (versiones viejas).
for (const f of fs.readdirSync(destino)) if (f.endsWith(".mp3") && !archivos.includes(f)) fs.rmSync(path.join(destino, f));
fs.writeFileSync(path.join(destino, "indice.json"), JSON.stringify(indice) + "\n");
