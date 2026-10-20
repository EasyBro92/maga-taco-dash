// Pool generico compartido: reutiliza objetos (meshes) en vez de crear/tirar
// geometria y materiales constantemente. Usado por world.js (obstaculos,
// tacos, power-ups, chispas) y main.js (polvo bajo los pies).
export function makePool(factory) {
  const free = [];
  return {
    acquire() {
      return free.length ? free.pop() : factory();
    },
    release(mesh) {
      mesh.visible = false;
      free.push(mesh);
    },
  };
}
