// El botón de instalar (10/11/2026). Isidro: «pon el botón de instalar si no
// lo tienes instalado, tanto para Android como Google».
//
// Qué hace según dónde se abra el juego:
//   · dentro de la app de Android (https://taco.dash/) o ya instalado como
//     app (pantalla completa): no sale.
//   · en un móvil Android: baja la app (el APK, que se actualiza sola). En su
//     Xiaomi la web no se instalaba bien (ver la memoria del APK), por eso
//     en Android va la app de verdad y no la web.
//   · en Chrome / Edge del ordenador: la ventana de instalar del navegador.
//   · en iPhone / iPad: Safari no deja instalar desde un botón; se explica
//     cómo (Compartir → Añadir a pantalla de inicio).

const APK = "https://easybro92.github.io/maga-taco-dash/descargas/TacoDash.apk";

let peticion = null;
const avisos = new Set();
if (typeof window !== "undefined") {
  window.addEventListener("beforeinstallprompt", (e) => { e.preventDefault(); peticion = e; for (const f of avisos) f(); });
  window.addEventListener("appinstalled", () => { peticion = null; for (const f of avisos) f(); });
}

const ua = () => (typeof navigator === "undefined" ? "" : navigator.userAgent);
export const enApp = () => location.host === "taco.dash"
  || (window.matchMedia && window.matchMedia("(display-mode: standalone)").matches)
  || navigator.standalone === true;
export const esAndroid = () => /Android/i.test(ua());
export const esIos = () => /iPhone|iPad|iPod/i.test(ua()) || (/Macintosh/.test(ua()) && navigator.maxTouchPoints > 1);

// Qué botón toca ahora: "android" | "web" | "ios" | null (ninguno).
export function modoInstalar() {
  if (enApp()) return null;
  if (esAndroid()) return "android";
  if (esIos()) return "ios";
  return peticion ? "web" : null;
}
export function alCambiarInstalar(fn) { avisos.add(fn); fn(); }

// Devuelve "ios" si hay que enseñar las instrucciones.
export async function instalar() {
  const m = modoInstalar();
  if (m === "android") { location.href = APK; return null; }
  if (m === "web" && peticion) {
    peticion.prompt();
    try { await peticion.userChoice; } catch (e) { /* cerrada */ }
    peticion = null;
    for (const f of avisos) f();
    return null;
  }
  return m === "ios" ? "ios" : null;
}
