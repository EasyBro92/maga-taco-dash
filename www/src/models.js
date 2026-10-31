import * as THREE from "../vendor/three.module.min.js";
import { GLTFLoader } from "../vendor/GLTFLoader.js";
import { mergeVertices } from "../vendor/BufferGeometryUtils.js";
import { toon } from "./toon.js";

// Piezas hechas en Blender (blender/*.py). Cada .glb es UNA malla con UNA
// textura donde ya van horneados los colores y la sombra de los rincones; aqui
// se cambia su material por el del juego (toon) para que la luz del juego la
// ilumine igual que a todo lo demas.
//
// Si un modelo no carga (sin conexion la primera vez, archivo que falta...),
// `modelo()` devuelve null y world.js usa la pieza antigua hecha con primitivas.

const LISTA = {
  dc: ["casa_blanca", "capitolio", "lincoln", "federal", "georgetown", "cerezo", "farola", "monumento"],
  ciudad: ["tienda_roja", "tienda_crema", "oficina_azul", "oficina_verde", "artdeco", "diner", "apart_morado",
    "apart_naranja", "arbol_ciudad", "farola_ciudad", "semaforo", "hidrante", "banco", "buzon", "taxi",
    "coche_rojo", "coche_azul"],
  personaje: ["personaje"],
  publico: ["ejecutivo", "senora", "chico", "abuelo", "turista", "fan", "valla_policia", "verja"],
  obstaculos: ["barricada", "conos", "pancarta", "globos", "guardaespaldas", "furgoneta", "patrulla", "autobus", "gorra",
    "rayo", "cohete", "barril", "chile", "jefe",
    // 27/10: los de cada ciudad (blender/obstaculos2.py)
    "taxi", "alcantarilla", "andamio", "contenedor", "paca", "tractor", "carroza", "guirnalda",
    "valla_metal", "protesta", "agentes", "suv",
    // y los de Phoenix
    "nopal", "rodadora", "saguaro", "pickup", "arco_neon",
    // 28/10: botas de salto y caja sorpresa (ideas de Subway Surfers)
    "botas", "caja_sorpresa",
    // 29/10: los de Las Vegas y el atril del debate
    "dado", "fichas", "tragaperras", "limusina", "marquesina", "atril",
    // 31/10: el helicoptero de la tele de las Fake News (decorado, en todos)
    "helicoptero",
    // 31/10 (2): los propios de cada mapa
    "basura", "viga", "perritos", "bici", "calabazas", "vaca", "calavera", "cartel_ruta", "elvis", "cajas"],
  pueblo: ["vict_blanca", "vict_azul", "rancho", "colonial", "cabana_rosa", "iglesia", "roble", "arbusto",
    "buzon_pueblo", "farola_pueblo"],
};

const plantillas = {};

// El material del juego para una pieza de Blender: su textura con la luz del
// juego. 29/10: si trae textura de luz (neones, bombillas, ventanas encendidas
// de Las Vegas), va de emisiva: brilla igual aunque la escena este oscura.
function materialDe(original, shininess, specular) {
  const mapa = original.map, luz = original.emissiveMap;
  for (const t of [mapa, luz]) if (t) { t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 4; }
  original.dispose();
  if (!mapa) return toon(0xffffff, null);
  return toon(0xffffff, luz ? { map: mapa, shininess, specular, emissiveMap: luz, emissive: 0xffffff }
    : { map: mapa, shininess, specular });
}

// ---- Halos (31/10/2026) ----
// Donde brilla cada pieza (neones y bombillas): lo apunta Blender en
// models/<carpeta>/luces.json ({ pieza: [[x, y, z, radio, color], ...] }).
// Solo las carpetas que lo tienen (las demas darian un error 404).
const CON_LUCES = new Set(["vegas", "obstaculos"]);
const luces = {};
async function cargarLuces(carpeta) {
  if (!CON_LUCES.has(carpeta) || luces[carpeta]) return;
  luces[carpeta] = {};
  try { luces[carpeta] = await (await fetch(`models/${carpeta}/luces.json`)).json(); } catch (e) { /* sin halos */ }
}
export function lucesDe(clave) {
  const [carpeta, pieza] = clave.split("/");
  return (luces[carpeta] && luces[carpeta][pieza]) || null;
}

export async function loadZoneModels(onProgress) {
  // ?sinblender: arrancar con las piezas antiguas, para comparar.
  if (/sinblender/.test(location.search)) return 0;
  await cargarLuces("obstaculos");
  const loader = new GLTFLoader();
  const tareas = [];
  const total = Object.values(LISTA).reduce((n, l) => n + l.length, 0);
  let hechas = 0;
  for (const zona in LISTA) {
    for (const nombre of LISTA[zona]) {
      tareas.push(
        loader.loadAsync(`models/${zona}/${nombre}.glb`).then((gltf) => {
          // Un archivo puede traer varias piezas (el personaje): cada malla se
          // guarda tambien con su propio nombre, `zona/<nombre de la malla>`.
          const mallas = [];
          gltf.scene.traverse((o) => { if (o.isMesh) mallas.push(o); });
          mallas.forEach((malla, i) => {
            malla.material = materialDe(malla.material, 18, 0x222222);
            malla.geometry.computeBoundingBox();
            const caja = malla.geometry.boundingBox;
            const p = {
              geometry: malla.geometry,
              material: malla.material,
              ancho: caja.max.x - caja.min.x,
              fondo: caja.max.z - caja.min.z,
              frente: caja.max.z, // lo que sobresale por delante de la fachada (cesped, escalinata)
            };
            if (i === 0) plantillas[`${zona}/${nombre}`] = p;
            if (mallas.length > 1) plantillas[`${zona}/${malla.name}`] = p;
          });
        }).catch((e) => {
          console.warn(`No se pudo cargar ${zona}/${nombre}.glb`, e);
        }).finally(() => onProgress && onProgress(++hechas, total))
      );
    }
  }
  await Promise.all(tareas);
  return Object.keys(plantillas).length;
}

// Carga bajo demanda (24/10/2026): los modelos de un nivel (Pennsylvania
// Avenue pesa 6 MB) solo se bajan al entrar en el, no al abrir el juego.
// Lo ya cargado no se vuelve a pedir.
export async function cargarCarpeta(carpeta, nombres, onProgress) {
  await cargarLuces(carpeta);
  const loader = new GLTFLoader();
  const faltan = nombres.filter((n) => !plantillas[`${carpeta}/${n}`]);
  let hechas = 0;
  await Promise.all(faltan.map((nombre) =>
    loader.loadAsync(`models/${carpeta}/${nombre}.glb`).then((gltf) => {
      let malla = null;
      gltf.scene.traverse((o) => { if (o.isMesh && !malla) malla = o; });
      if (!malla) return;
      malla.material = materialDe(malla.material, 14, 0x1a1a1a);
      malla.geometry.computeBoundingBox();
      const caja = malla.geometry.boundingBox;
      plantillas[`${carpeta}/${nombre}`] = {
        geometry: malla.geometry, material: malla.material,
        ancho: caja.max.x - caja.min.x, fondo: caja.max.z - caja.min.z, frente: caja.max.z,
      };
    }).catch((e) => console.warn(`No se pudo cargar ${carpeta}/${nombre}.glb`, e))
      .finally(() => onProgress && onProgress(++hechas, faltan.length))));
}

export function hayModelo(clave) {
  return !!plantillas[clave];
}

export function medidas(clave) {
  return plantillas[clave] || null;
}

// Grupo nuevo que comparte geometria y material con la plantilla (no copia
// nada: cien Casas Blancas cuestan lo mismo en memoria que una).
export function modelo(clave) {
  const p = plantillas[clave];
  if (!p) return null;
  const g = new THREE.Group();
  g.add(new THREE.Mesh(p.geometry, p.material));
  g.userData.ancho = p.ancho;
  g.userData.fondo = p.fondo;
  g.userData.frente = p.frente;
  return g;
}

// ---- Sin contorno (27/10/2026) ----
// Los obstaculos llevaban un contorno negro de dibujo animado (una copia de la
// malla hinchada y vista por dentro). Isidro eligio «sin contorno» para todo el
// juego y era lo unico que lo tenia: ya no se pone. La forma hinchada se sigue
// calculando, pero solo para la capa de hielo del rayo congelador.
const contornos = {};
function formaHinchada(clave) {
  let geo = contornos[clave];
  if (!geo) {
    const base = plantillas[clave].geometry.clone();
    for (const nombre of Object.keys(base.attributes)) if (nombre !== "position") base.deleteAttribute(nombre);
    geo = mergeVertices(base, 1e-3);
    geo.computeVertexNormals();
    contornos[clave] = geo;
  }
  return geo;
}

export function modeloConContorno(clave) {
  return modelo(clave);
}

// ---- Capa de hielo del rayo congelador (22/10/2026) ----
// La misma forma hinchada del contorno, pero mas gorda, azul hielo y
// translucida por fuera: el obstaculo se ve metido en un bloque de hielo.
const hieloMat = new THREE.ShaderMaterial({
  uniforms: { grosor: { value: 0.09 } },
  vertexShader: `uniform float grosor; varying vec3 vN; varying vec3 vV;
    void main() {
      vec3 p = position + normalize(normal) * grosor;
      vec4 mv = modelViewMatrix * vec4(p, 1.0);
      vN = normalize(normalMatrix * normal); vV = normalize(-mv.xyz);
      gl_Position = projectionMatrix * mv;
    }`,
  fragmentShader: `varying vec3 vN; varying vec3 vV;
    void main() {
      float borde = 1.0 - abs(dot(vN, vV));
      gl_FragColor = vec4(mix(vec3(0.55, 0.9, 1.0), vec3(1.0), borde * 0.7), 0.45 + borde * 0.4);
    }`,
  transparent: true,
  depthWrite: false,
});

export function capaHielo(clave) {
  if (!plantillas[clave]) return null;
  return new THREE.Mesh(formaHinchada(clave), hieloMat);
}

// ---- El presidente de Meshy (24/10/2026): con esqueleto y animaciones ----
// Este no es una malla quieta como el resto: es un personaje con huesos
// (andar y correr de Meshy), asi que se guarda la escena entera del .glb.
let personaje = null;
export async function cargarPersonaje() {
  if (/sinmeshy/.test(location.search)) return null;
  try {
    const gltf = await new GLTFLoader().loadAsync("models/personaje/presidente.glb");
    personaje = gltf;
  } catch (e) {
    console.warn("No se pudo cargar el presidente de Meshy", e);
  }
  return personaje;
}
export function getPersonaje() {
  return personaje;
}
