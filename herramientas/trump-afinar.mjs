// Afina dónde empieza y acaba cada frase de herramientas/trump.mjs (31/10/2026).
//
//   node herramientas/trump-afinar.mjs
//
// En las grabaciones largas los tiempos de whisper se van retrasando (hasta
// 2 s en el discurso de investidura) y el corte pillaba media frase. Aquí se
// vuelve a pasar whisper solo por un trozo de 8 s alrededor de cada frase, que
// da tiempos mucho más justos, y se guardan en _trump/tiempos.json. Después
// trump.mjs corta con ellos y vuelve a comprobar con whisper que se entiende.
import fs from "node:fs";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath, pathToFileURL } from "node:url";

const aqui = path.dirname(fileURLToPath(import.meta.url));
const T = path.join(aqui, "_trump");
const WHISPER = path.join(T, "programa/bin/Release/whisper-cli.exe");
const MODELO = path.join(T, "modelo/ggml-base.en.bin");
const { CORTES, guardarWav } = await import(pathToFileURL(path.join(aqui, "trump-cortes.mjs")));
const { leerWav } = await import(pathToFileURL(path.resolve(aqui, "../../z-resistance/herramientas/voces/sonido.mjs")));

const norm = (s) => s.toLowerCase().replace(/[^a-z0-9']/g, "");
function palabrasDe(json) {
  return JSON.parse(fs.readFileSync(json, "utf8")).transcription
    .map((t) => ({ w: norm(t.text), a: t.offsets.from / 1000, b: t.offsets.to / 1000 })).filter((p) => p.w);
}
function buscar(p, frase, vez = 0) {
  const f = frase.split(" "), sitios = [];
  for (let i = 0; i + f.length <= p.length; i++) if (f.every((w, k) => p[i + k].w === w)) sitios.push([p[i].a, p[i + f.length - 1].b, i]);
  return sitios.length ? sitios[vez < 0 ? sitios.length + vez : Math.min(vez, sitios.length - 1)] : null;
}
const largos = {}, audios = {};
const tmp = path.join(T, "ventana");
const tiempos = {};
for (const [texto, [fuente, frase, vez]] of Object.entries(CORTES)) {
  largos[fuente] = largos[fuente] || palabrasDe(path.join(T, "texto", fuente + ".json"));
  audios[fuente] = audios[fuente] || leerWav(path.join(T, "wav16", fuente + ".wav")).datos;
  const aprox = buscar(largos[fuente], frase, vez);
  if (!aprox) { console.log("NO ESTA", texto); continue; }
  // ventana de 8 s que empieza 3 s antes de donde dice whisper
  const v0 = Math.max(0, aprox[0] - 3), v1 = Math.min(audios[fuente].length / 16000, aprox[1] + 3);
  guardarWav(tmp + ".wav", audios[fuente].slice(Math.floor(v0 * 16000), Math.floor(v1 * 16000)), 16000);
  spawnSync(WHISPER, ["-m", MODELO, "-f", tmp + ".wav", "-ml", "1", "-sow", "-oj", "-of", tmp, "-t", "8", "-np"], { stdio: "ignore" });
  const cerca = buscar(palabrasDe(tmp + ".json"), frase, 0);
  if (!cerca) { tiempos[texto] = [aprox[0], aprox[1]]; console.log(`${texto.padEnd(40)} (sin afinar)`); continue; }
  tiempos[texto] = [+(v0 + cerca[0]).toFixed(2), +(v0 + cerca[1]).toFixed(2)];
  console.log(`${texto.padEnd(40)} ${aprox[0].toFixed(2)} -> ${tiempos[texto][0].toFixed(2)}   ${aprox[1].toFixed(2)} -> ${tiempos[texto][1].toFixed(2)}`);
}
// Aparte, para no pisar los tiempos repasados a mano (trump-tiempos.json).
fs.writeFileSync(path.join(T, "tiempos.json"), JSON.stringify(tiempos, null, 1));
