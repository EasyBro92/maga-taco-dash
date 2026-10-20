import * as THREE from "../vendor/three.module.min.js";

// Shading suave y brillante estilo "juguete de vinilo" (referencia: Subway
// Surfers) -- MeshPhongMaterial con un especular suave da ese aspecto
// pulido/redondeado, sin bandas duras ni contorno negro tipo comic.
//
// El nombre `toon`/`withOutline` se mantiene por compatibilidad (lo usan
// character.js y world.js en decenas de sitios) aunque ya no hacen shading
// tipo comic; cambiar la implementacion aqui actualiza TODOS los
// materiales del juego a la vez sin tocar cada punto de uso.

export function toon(color, opts) {
  return new THREE.MeshPhongMaterial(Object.assign(
    { color, shininess: 45, specular: 0x666666 },
    opts || {}
  ));
}

// Subway-Surfers-style: sin contorno, todo shading suave. Se deja como
// funcion (en vez de borrar las decenas de llamadas) para no tocar cada
// punto de uso; simplemente ya no anade nada.
export function withOutline(mesh) {
  return mesh;
}
