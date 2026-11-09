// Huellas de los archivos del juego (09/11/2026).
// Isidro: «el juego tarda mucho en cargar al inicio». La app del movil
// preguntaba a GitHub por cada archivo (unos 240) si habia cambiado, uno a uno.
// Ahora baja solo esta lista ({ "/ruta": "huella" }) y pide unicamente los
// archivos cuya huella no coincide con la que ya tiene guardada.
//
// Uso: node herramientas/huellas.mjs [carpeta=www] [salida=<carpeta>/huellas.json]
// La lista se hace sola al publicar (.github/workflows/pages.yml) y al
// construir el APK (apk/construir.sh); no se sube a git.
import { createHash } from "node:crypto";
import { readdirSync, readFileSync, writeFileSync, statSync } from "node:fs";
import { join, relative, sep } from "node:path";

const carpeta = process.argv[2] || "www";
const salida = process.argv[3] || join(carpeta, "huellas.json");
const huellas = {};
(function recorrer(dir) {
  for (const nombre of readdirSync(dir)) {
    if (nombre.startsWith("_") || nombre === "huellas.json" || nombre === "sw.js") continue;
    const ruta = join(dir, nombre);
    if (statSync(ruta).isDirectory()) { recorrer(ruta); continue; }
    const clave = "/" + relative(carpeta, ruta).split(sep).join("/");
    huellas[clave] = createHash("sha1").update(readFileSync(ruta)).digest("hex").slice(0, 12);
  }
})(carpeta);
writeFileSync(salida, JSON.stringify(huellas));
console.log(`${Object.keys(huellas).length} huellas en ${salida}`);
