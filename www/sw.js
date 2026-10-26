// Service worker de MAGA Taco Dash (26/10/2026). Hace que el juego se pueda
// instalar en el movil. Siempre pide primero a internet (asi cada cambio
// publicado llega al momento) y, si no hay conexion, usa lo ya guardado.
const CACHE = "taco-dash-v1";

self.addEventListener("install", () => self.skipWaiting());
self.addEventListener("activate", (e) => e.waitUntil(self.clients.claim()));

self.addEventListener("fetch", (e) => {
  const req = e.request;
  if (req.method !== "GET" || !req.url.startsWith(self.location.origin)) return;
  e.respondWith(
    fetch(req)
      .then((res) => {
        if (res.ok) {
          const copia = res.clone();
          caches.open(CACHE).then((c) => c.put(req, copia));
        }
        return res;
      })
      .catch(() => caches.match(req).then((r) => r || Response.error()))
  );
});
