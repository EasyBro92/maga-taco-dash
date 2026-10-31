// Las frases del presidente con su voz de verdad (31/10/2026).
//
//   node herramientas/trump.mjs
//
// Isidro pidió su voz de verdad. Se cortan de grabaciones de dominio público
// de Wikimedia Commons (vídeos de Voice of America y de la Casa Blanca, obras
// del gobierno de EE. UU.), bajadas con su permiso a herramientas/_trump/
// (fuera de git):
//   fake_news_rusia     «Trump Calls Russia 'Fake News'» (VOA, 16/02/2017)
//   fake_news_cpac      «Trump on 'fake news' and information leaks» (VOA, CPAC 2017)
//   very_sad_manafort   «Trump 'very sad' about Manafort conviction» (VOA, 21/08/2018)
//   tremendous_trade    «We signed a tremendous trade deal» (la Casa Blanca, 2025)
//   investidura_2017    discurso de investidura, 20/01/2017 (copia MP3 de Commons)
//   cien_dias           «President Trump's First 100 Days» (VOA, 2017)
// Los pasos:
//   1. Blender las pasa a WAV (herramientas/a_wav.py): a _trump/wav16 para
//      whisper y a _trump/wav22 para cortar.
//   2. whisper.cpp dice en qué momento va cada palabra (_trump/texto/*.json).
//   3. trump-afinar.mjs afina el principio y el final de cada frase
//      (herramientas/trump-tiempos.json, repasado luego a mano).
//   4. Este: corta, iguala el volumen, junta todo en www/voces/trump.<huella>.mp3
//      con su índice www/voces/trump.json (audio.js lo junta con indice.json) y
//      vuelve a pasar whisper por cada corte para comprobar que se entiende.
import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import { spawnSync } from "node:child_process";
import { fileURLToPath, pathToFileURL } from "node:url";

const aqui = path.dirname(fileURLToPath(import.meta.url));
const raiz = path.resolve(aqui, "..");
const T = path.join(aqui, "_trump");
const zr = path.resolve(raiz, "../z-resistance/herramientas/voces");
const { leerWav, igualar, aMp3, silencio, juntar, afinar } = await import(pathToFileURL(path.join(zr, "sonido.mjs")));
const { CORTES, guardarWav } = await import(pathToFileURL(path.join(aqui, "trump-cortes.mjs")));

// Que no falte ninguna de las que usa el juego. (Node lee los .js del juego
// como CommonJS: se copia como .mjs para importarlo.)
const copia = path.join(T, "frases.mjs");
fs.copyFileSync(path.join(raiz, "www/src/frases.js"), copia);
const { TRUMP } = await import(pathToFileURL(copia));
for (const t of Object.keys(TRUMP)) if (!CORTES[t]) throw new Error("Sin corte: " + t);
// Los tiempos de cada frase: los saca trump-afinar.mjs y luego se repasaron a
// mano oyendo cada corte con whisper (ver la salida «oye:»). Están en git.
const tiempos = JSON.parse(fs.readFileSync(path.join(aqui, "trump-tiempos.json"), "utf8"));
// Ajustes a mano (en segundos) donde whisper no afina solo: [principio, final].
const AJUSTES = fs.existsSync(path.join(T, "ajustes.json")) ? JSON.parse(fs.readFileSync(path.join(T, "ajustes.json"), "utf8")) : {};

const HZ = 22050;
const audios = {};
// El trozo, con un poco de margen; luego se le quita lo que no llega al
// umbral por los bordes y se le ponen una entrada y una salida suaves.
function cortar(fuente, a, b) {
  if (!audios[fuente]) audios[fuente] = leerWav(path.join(T, "wav22", fuente + ".wav")).datos;
  const d = audios[fuente];
  let i0 = Math.max(0, Math.floor((a - 0.1) * HZ)), i1 = Math.min(d.length, Math.ceil((b + 0.15) * HZ));
  const ventana = Math.round(0.02 * HZ);
  const fuerte = (i) => { let s = 0; for (let k = i; k < i + ventana && k < d.length; k++) s += d[k] * d[k]; return Math.sqrt(s / ventana); };
  let pico = 0;
  for (let i = i0; i < i1; i += ventana) pico = Math.max(pico, fuerte(i));
  const umbral = pico * 0.06;
  while (i0 < i1 - ventana && fuerte(i0) < umbral) i0 += ventana / 2;
  while (i1 > i0 + ventana && fuerte(i1 - ventana) < umbral) i1 -= ventana / 2;
  i0 = Math.max(0, i0 - Math.round(0.03 * HZ)); i1 = Math.min(d.length, i1 + Math.round(0.05 * HZ));
  const t = d.slice(i0, i1);
  const fundido = Math.round(0.015 * HZ);
  for (let k = 0; k < fundido; k++) { t[k] *= k / fundido; t[t.length - 1 - k] *= k / fundido; }
  return igualar(t, 0.16);
}

const cortes = path.join(T, "cortes");
fs.mkdirSync(cortes, { recursive: true });
for (const v of fs.readdirSync(cortes)) fs.rmSync(path.join(cortes, v));
const WHISPER = path.join(T, "programa/bin/Release/whisper-cli.exe"), MODELO = path.join(T, "modelo/ggml-base.en.bin");
const trozos = [], sitio = {};
let p = 0;
for (const [texto, [fuente]] of Object.entries(CORTES)) {
  if (!tiempos[texto]) throw new Error("Sin tiempos (falta trump-afinar.mjs): " + texto);
  const [da, db] = AJUSTES[texto] || [0, 0];
  const a = tiempos[texto][0] + da, b = tiempos[texto][1] + db;
  const d = juntar([silencio(HZ, 0.04), cortar(fuente, a, b), silencio(HZ, 0.06)]);
  const mp3 = aMp3(d, HZ, 48);
  trozos.push(mp3);
  sitio[texto] = [p, mp3.length];
  p += mp3.length;
  // Comprobar: lo que entiende whisper de este corte.
  const wav = path.join(cortes, texto.replace(/[^A-Z]+/g, "_").replace(/^_|_$/g, "") + ".wav");
  guardarWav(wav, afinar(d, HZ, 16000), 16000);
  const oye = spawnSync(WHISPER, ["-m", MODELO, "-f", wav, "-nt", "-np", "-t", "8"], { encoding: "utf8" }).stdout.replace(/\s+/g, " ").trim();
  console.log(`${texto.padEnd(40)} ${a.toFixed(2)}-${b.toFixed(2)} ${(d.length / HZ).toFixed(2)} s  oye: ${oye}`);
}
const todo = Buffer.concat(trozos);
const destino = path.join(raiz, "www/voces");
const archivo = `trump.${crypto.createHash("sha1").update(todo).digest("hex").slice(0, 8)}.mp3`;
for (const f of fs.readdirSync(destino)) if (/^trump\..*\.mp3$/.test(f)) fs.rmSync(path.join(destino, f));
fs.writeFileSync(path.join(destino, archivo), todo);
const indice = {};
for (const [texto, [desde, n]] of Object.entries(sitio)) indice[texto] = [archivo, desde, n];
fs.writeFileSync(path.join(destino, "trump.json"), JSON.stringify(indice) + "\n");
console.log(`${Object.keys(indice).length} frases, ${(todo.length / 1024).toFixed(0)} KB en www/voces/${archivo}`);
