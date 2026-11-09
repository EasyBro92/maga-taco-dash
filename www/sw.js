// Service worker de MAGA Taco Dash (26/10/2026). Hace que el juego se pueda
// instalar en el movil y que funcione sin conexion.
//
// 09/11/2026: Isidro: «el juego tarda mucho en cargar al inicio». Antes se
// pedia a internet todo (unos 240 archivos, 23 MB) cada vez que se abria.
// Ahora, al abrir, se baja solo la lista de huellas (huellas.json, la hace
// GitHub al publicar) y cada archivo sale de lo guardado si su huella no ha
// cambiado; solo se baja lo nuevo. Sin lista (en el PC de pruebas), como antes:
// primero internet y, sin conexion, lo guardado.
const CACHE = "taco-dash-v45";
const ARCHIVOS = "taco-dash-archivos";   // lo que va por huella (no cambia de nombre)

self.addEventListener("install", () => self.skipWaiting());
self.addEventListener("activate", (e) => e.waitUntil((async () => {
  // Las cajas de versiones antiguas ocupaban 23 MB cada una: fuera.
  for (const k of await caches.keys()) if (k !== CACHE && k !== ARCHIVOS) await caches.delete(k);
  await self.clients.claim();
})()));

const BASE = new URL(self.registration.scope).pathname;   // "/maga-taco-dash/"
const EN_PC = /^(localhost|127\.0\.0\.1)$/.test(self.location.hostname) && !/huellas/.test(self.location.search);
let huellas = null, pidiendo = null;
function pedirHuellas() {
  pidiendo = fetch(BASE + "huellas.json?t=" + Date.now(), { cache: "no-store" })
    .then((r) => (r.ok ? r.json() : null)).catch(() => null)
    .then((h) => { if (h) huellas = h; return huellas; });
  return pidiendo;
}

async function porHuella(req, ruta, h) {
  const caja = await caches.open(ARCHIVOS);
  const clave = BASE + ruta.slice(1) + "?h=" + h;
  const guardada = await caja.match(clave);
  if (guardada) return guardada;
  try {
    const res = await fetch(clave, { cache: "no-store" });
    if (res.ok) {
      await caja.put(clave, res.clone());
      // Las versiones viejas del mismo archivo sobran.
      const sin = BASE + ruta.slice(1) + "?h=";
      for (const k of await caja.keys()) {
        const u = new URL(k.url);
        if (u.pathname + "?h=" === sin && u.search !== "?h=" + h) caja.delete(k);
      }
    }
    return res;
  } catch (e) {
    // Sin conexion: la ultima version guardada de ese archivo, sea cual sea.
    for (const k of await caja.keys()) if (new URL(k.url).pathname === BASE + ruta.slice(1)) return caja.match(k);
    const vieja = await caches.match(req);
    return vieja || Response.error();
  }
}

function primeroInternet(req) {
  return fetch(req)
    .then((res) => {
      if (res.ok) {
        const copia = res.clone();
        caches.open(CACHE).then((c) => c.put(req, copia));
      }
      return res;
    })
    .catch(() => caches.match(req).then((r) => r || Response.error()));
}

self.addEventListener("fetch", (e) => {
  const req = e.request;
  if (req.method !== "GET" || !req.url.startsWith(self.location.origin)) return;
  const url = new URL(req.url);
  // (En el PC de pruebas siempre lo ultimo: alli los archivos cambian a cada rato.)
  if (!url.pathname.startsWith(BASE) || url.search || EN_PC) return e.respondWith(primeroInternet(req));
  let ruta = "/" + url.pathname.slice(BASE.length);
  if (ruta === "/") ruta = "/index.html";
  if (ruta === "/huellas.json" || ruta === "/sw.js") return;
  e.respondWith((async () => {
    // Al abrir el juego (la pagina) se mira la lista nueva; el resto usa esa.
    const lista = req.mode === "navigate" ? await pedirHuellas() : huellas || await (pidiendo || pedirHuellas());
    const h = lista && lista[ruta];
    return h ? porHuella(req, ruta, h) : primeroInternet(req);
  })());
});
