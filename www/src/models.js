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
  publico: ["ejecutivo", "senora", "chico", "abuelo", "turista", "fan"],
  obstaculos: ["barricada", "conos", "pancarta", "globos", "guardaespaldas", "furgoneta", "patrulla", "autobus", "gorra",
    "rayo", "cohete", "barril", "chile", "jefe"],
  pueblo: ["vict_blanca", "vict_azul", "rancho", "colonial", "cabana_rosa", "iglesia", "roble", "arbusto",
    "buzon_pueblo", "farola_pueblo"],
};

const plantillas = {};

export async function loadZoneModels(onProgress) {
  // ?sinblender: arrancar con las piezas antiguas, para comparar.
  if (/sinblender/.test(location.search)) return 0;
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
            const mapa = malla.material.map;
            if (mapa) {
              mapa.colorSpace = THREE.SRGBColorSpace;
              mapa.anisotropy = 4;
            }
            malla.material.dispose();
            malla.material = toon(0xffffff, mapa ? { map: mapa, shininess: 18, specular: 0x222222 } : null);
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
  const loader = new GLTFLoader();
  const faltan = nombres.filter((n) => !plantillas[`${carpeta}/${n}`]);
  let hechas = 0;
  await Promise.all(faltan.map((nombre) =>
    loader.loadAsync(`models/${carpeta}/${nombre}.glb`).then((gltf) => {
      let malla = null;
      gltf.scene.traverse((o) => { if (o.isMesh && !malla) malla = o; });
      if (!malla) return;
      const mapa = malla.material.map;
      if (mapa) { mapa.colorSpace = THREE.SRGBColorSpace; mapa.anisotropy = 4; }
      malla.material.dispose();
      malla.material = toon(0xffffff, mapa ? { map: mapa, shininess: 14, specular: 0x1a1a1a } : null);
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

// ---- Contorno de dibujo animado (22/10/2026) ----
// Para que los obstaculos se distingan de un vistazo, como en Minion Rush: una
// copia de la malla un poco hinchada hacia fuera, negra y vista solo por
// dentro (la tecnica clasica de "casco invertido"). Se hincha con normales
// suavizadas propias -- con las de la malla, partidas en cada arista, el
// contorno se abria en las esquinas.
const contornos = {};
const contornoMat = new THREE.ShaderMaterial({
  uniforms: { grosor: { value: 0.035 }, color: { value: new THREE.Color(0x1b1424) } },
  vertexShader: `uniform float grosor;
    void main() {
      vec3 p = position + normalize(normal) * grosor;
      gl_Position = projectionMatrix * modelViewMatrix * vec4(p, 1.0);
    }`,
  fragmentShader: `uniform vec3 color; void main() { gl_FragColor = vec4(color, 1.0); }`,
  side: THREE.BackSide,
});

export function modeloConContorno(clave) {
  const g = modelo(clave);
  if (!g) return null;
  let geo = contornos[clave];
  if (!geo) {
    const base = plantillas[clave].geometry.clone();
    for (const nombre of Object.keys(base.attributes)) if (nombre !== "position") base.deleteAttribute(nombre);
    geo = mergeVertices(base, 1e-3);
    geo.computeVertexNormals();
    contornos[clave] = geo;
  }
  g.add(new THREE.Mesh(geo, contornoMat));
  return g;
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
  if (!contornos[clave]) { const g = modeloConContorno(clave); g.clear(); }
  return new THREE.Mesh(contornos[clave], hieloMat);
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
