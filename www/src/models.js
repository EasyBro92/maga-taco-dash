import * as THREE from "../vendor/three.module.min.js";
import { GLTFLoader } from "../vendor/GLTFLoader.js";
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
