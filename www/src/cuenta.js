// La cuenta del jugador (10/11/2026). Isidro: «la posibilidad de iniciar
// sesión o crear un usuario de forma simple para seguir tu progreso».
//
// Sin cuenta se juega igual: todo se guarda en el móvil. Con cuenta (un nombre
// de usuario y una contraseña, sin correo), la partida se sube sola a la nube
// cada vez que se guarda y, al entrar en otro móvil, se juntan las dos sin
// perder nada (save.js, fundirPartida).
//
// Usa el Firebase de AlienZ (el mismo proyecto, con usuario y contraseña ya
// activados): cada jugador tiene su ficha en `tacodash/{uid}` y las reglas
// (z-resistance/firestore.rules) solo le dejan tocar la suya. El usuario va
// como un correo inventado (<nombre>@magatacodash.app): no se manda nada a
// ningún sitio. Firebase se baja solo si hay sesión o se pulsa Entrar.

import { onGuardar, partidaParaNube, fundirPartida, getSave } from "./save.js";

const CONFIG = {
  apiKey: "AIzaSyAwzbv3vb6Ju-ie3mgYPBp9C-V0QMw_ZKY",
  authDomain: "alienz-resistance.firebaseapp.com",
  projectId: "alienz-resistance",
  storageBucket: "alienz-resistance.firebasestorage.app",
  messagingSenderId: "134292140642",
  appId: "1:134292140642:web:a204f937309a7c933a573b",
};
const V = "10.12.2";
const CLAVE_SESION = "tacoDashCuenta_v1";   // el nombre, si hubo sesión en este móvil
const DOMINIO = "@magatacodash.app";

let fb = null;
function cargar() {
  fb ??= Promise.all([
    import(`https://www.gstatic.com/firebasejs/${V}/firebase-app.js`),
    import(`https://www.gstatic.com/firebasejs/${V}/firebase-auth.js`),
    import(`https://www.gstatic.com/firebasejs/${V}/firebase-firestore.js`),
  ]).then(([app, auth, fs]) => {
    const a = app.getApps().find((x) => x.name === "taco") || app.initializeApp(CONFIG, "taco");
    return { auth, fs, sesion: auth.getAuth(a), db: fs.getFirestore(a) };
  });
  fb.catch(() => { fb = null; });
  return fb;
}

let usuario = null;          // { uid, nombre }
const avisos = new Set();
function avisar() { for (const f of avisos) f(usuario); }
export function alCambiarCuenta(fn) { avisos.add(fn); fn(usuario); }
export function cuentaActual() { return usuario; }
export function nombreGuardado() { try { return localStorage.getItem(CLAVE_SESION) || ""; } catch (e) { return ""; } }

// Nombre: de 3 a 20 letras, números, punto, guion o guion bajo.
export function nombreValido(n) { return /^[a-z0-9._-]{3,20}$/i.test(n || ""); }
const correo = (n) => n.trim().toLowerCase() + DOMINIO;

// ---- Subir: cada guardado, agrupado (3 s después del último) ----
let reloj = null, nubeRota = false;
async function subir() {
  if (!usuario) return;
  try {
    const { fs, db } = await cargar();
    await fs.setDoc(fs.doc(db, "tacodash", usuario.uid), {
      nombre: usuario.nombre, partida: JSON.stringify(partidaParaNube()), fecha: fs.serverTimestamp(),
    });
    nubeRota = false;
  } catch (e) { nubeRota = true; console.warn("[cuenta] no se pudo subir", e && e.code); }
}
onGuardar(() => {
  if (!usuario) return;
  clearTimeout(reloj);
  reloj = setTimeout(subir, 3000);
});
export function nubeFalla() { return nubeRota; }

// ---- 11/11: el ranking del sin fin (tacodash_top/{uid}: nombre y metros) ----
export async function subirRecord(metros) {
  if (!usuario || !(metros > 0)) return;
  try {
    const { fs, db } = await cargar();
    await fs.setDoc(fs.doc(db, "tacodash_top", usuario.uid), { nombre: usuario.nombre, metros: Math.floor(metros), fecha: fs.serverTimestamp() });
  } catch (e) { console.warn("[ranking] no se pudo subir", e && e.code); }
}
export async function leerRanking(n = 30) {
  const { fs, db } = await cargar();
  const q = fs.query(fs.collection(db, "tacodash_top"), fs.orderBy("metros", "desc"), fs.limit(n));
  const r = await fs.getDocs(q);
  return r.docs.map((d) => ({ uid: d.id, ...d.data() }));
}

// Baja la ficha de la nube y la junta con la de este móvil. Si cambia algo,
// devuelve true (main.js recarga para que todo lo pinte de nuevo).
async function bajarYJuntar() {
  const { fs, db } = await cargar();
  const d = await fs.getDoc(fs.doc(db, "tacodash", usuario.uid));
  let cambio = false;
  if (d.exists()) {
    try { cambio = fundirPartida(JSON.parse(d.data().partida || "{}")); } catch (e) { /* ficha rota: se queda la del móvil */ }
  }
  await subir();
  return cambio;
}

function traducirError(e) {
  const c = (e && e.code) || "";
  if (/user-not-found|invalid-credential|wrong-password|invalid-login/.test(c)) return "malUsuario";
  if (/email-already-in-use/.test(c)) return "yaExiste";
  if (/weak-password/.test(c)) return "claveCorta";
  if (/too-many-requests/.test(c)) return "muchosIntentos";
  if (/network|unavailable|failed-to-fetch/.test(c) || !c) return "sinRed";
  if (/permission/.test(c)) return "nubeNoLista";
  return "errorCuenta";
}

async function trasEntrar(u, nombre) {
  usuario = { uid: u.uid, nombre };
  try { localStorage.setItem(CLAVE_SESION, nombre); } catch (e) { /* sin almacenamiento */ }
  avisar();
  try { const cambio = await bajarYJuntar(); subirRecord(getSave().bestScore); return { ok: true, cambio }; }
  catch (e) { nubeRota = true; return { ok: true, cambio: false, aviso: traducirError(e) }; }
}

export async function entrar(nombre, clave) {
  if (!nombreValido(nombre)) return { error: "nombreMal" };
  try {
    const { auth, sesion } = await cargar();
    const r = await auth.signInWithEmailAndPassword(sesion, correo(nombre), clave);
    return trasEntrar(r.user, nombre.trim());
  } catch (e) { return { error: traducirError(e) }; }
}

export async function crear(nombre, clave) {
  if (!nombreValido(nombre)) return { error: "nombreMal" };
  if (!clave || clave.length < 6) return { error: "claveCorta" };
  try {
    const { auth, sesion } = await cargar();
    const r = await auth.createUserWithEmailAndPassword(sesion, correo(nombre), clave);
    return trasEntrar(r.user, nombre.trim());
  } catch (e) { return { error: traducirError(e) }; }
}

export async function salir() {
  try { const { auth, sesion } = await cargar(); await auth.signOut(sesion); } catch (e) { /* da igual */ }
  usuario = null;
  try { localStorage.removeItem(CLAVE_SESION); } catch (e) { /* sin almacenamiento */ }
  avisar();
}

// Al arrancar: si en este móvil hubo sesión, se recupera sola (Firebase la
// guarda) y se juntan las partidas por si se jugó en otro sitio.
export async function arrancarCuenta(alCambiarPartida) {
  const nombre = nombreGuardado();
  if (!nombre) return;
  try {
    const { auth, sesion } = await cargar();
    const u = await new Promise((ok) => { const fin = auth.onAuthStateChanged(sesion, (x) => { fin(); ok(x); }); });
    if (!u) { try { localStorage.removeItem(CLAVE_SESION); } catch (e) { /* nada */ } return; }
    usuario = { uid: u.uid, nombre };
    avisar();
    const cambio = await bajarYJuntar();
    subirRecord(getSave().bestScore);
    if (cambio && alCambiarPartida) alCambiarPartida();
  } catch (e) { nubeRota = true; }
}
