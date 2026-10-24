// La gira de campaña hasta la Casa Blanca (24/10/2026). Ver DECISIONS.md.
//
// Cinco niveles con calles de verdad. Cada lado de la calle es una lista de
// edificios EN SU ORDEN REAL, uno detras de otro: [pieza, veces] repite un
// tramo de fachada (los edificios federales son muy largos), y un numero
// suelto es un cruce de calle (hueco sin edificios). Asi cada partida del
// mismo nivel tiene exactamente la misma calle, como en la vida real.
//
// Las piezas son modelos de www/models/<carpeta>/<pieza>.glb.

export const NIVELES = [
  { id: "nueva_york", numero: 1, nombre: "Quinta Avenida", lugar: "Nueva York", listo: false, mapa: [88, 25] },
  { id: "pueblo", numero: 2, nombre: "Calle Mayor", lugar: "Ohio", listo: false, mapa: [73, 29] },
  { id: "ruta66", numero: 3, nombre: "Ruta 66", lugar: "Arizona", listo: false, mapa: [27, 45] },
  { id: "vegas", numero: 4, nombre: "El Strip", lugar: "Las Vegas", listo: false, mapa: [17, 38] },
  {
    id: "washington", numero: 5, nombre: "Pennsylvania Avenue", lugar: "Washington D.C.", listo: true, mapa: [85, 33],
    zona: "dc",
    carpeta: "washington",
    luz: "atardecer",
    semilla: 1600,                 // el mismo reparto de obstaculos cada vez
    largo: 3300,                   // donde esta la verja de la Casa Blanca
    estrellas: [350, 700, 1100],   // tacos para 1, 2 y 3 estrellas
    linea: 11.5,                   // x de las fachadas
    // Hacia el oeste: el sur queda a la izquierda y el norte a la derecha.
    izquierda: [
      60,
      ["galeria_este", 1], 18,
      ["archivos_ala", 12], ["archivos_portico", 1], ["archivos_ala", 12], 18,   // 7th - 9th
      ["justicia", 30], 18,                                                    // 9th - 10th
      ["irs", 24], 12,                                                         // 10th - 12th
      ["correos", 10], ["correos_torre", 1], ["correos", 10], 18,                 // 12th
      ["reagan", 36], 18,                                                      // 12th - 14th
      ["wilson", 1], 18,                                                       // 14th
      ["pershing", 1],
    ],
    derecha: [
      60,
      ["canada", 1], 18, ["cristal", 1], 18,                                    // 4th - 6th
      ["navy", 1], 18,                                                         // 7th - 9th
      ["fbi", 40], 18,                                                         // 9th - 10th
      ["irs", 30], 18, ["cristal", 1], 18, ["justicia", 34], 18,
      ["correos", 10], 18, ["reagan", 14], 18,                // 10th - 14th
      ["willard", 1], 18,                                                      // 14th
      ["canada", 1],
    ],
    // Al final de la avenida: el Tesoro a la izquierda y la Casa Blanca al fondo.
    fondo: [
      { pieza: "tesoro", d: 3110, lado: -1 },
      { pieza: "casa_blanca_final", d: 3340, centro: true },
    ],
    // Mobiliario de la acera (este si se repite: farolas y arboles, como en la calle de verdad).
    acera: ["dc/farola", "pueblo/roble"],
  },
];

// Ancho de cada pieza a lo largo de la calle (el de su fachada, sin contar lo
// que sobresale la cornisa: asi los tramos encajan sin pisarse).
export const ANCHO = {
  archivos_ala: 20, archivos_portico: 34, justicia: 20, irs: 20, correos: 20, correos_torre: 30,
  reagan: 20, wilson: 40, pershing: 40, canada: 30, cristal: 30, navy: 40, fbi: 20, willard: 35,
  galeria_este: 40, tesoro: 60, casa_blanca_final: 76,
};

export function nivelPorId(id) {
  return NIVELES.find((n) => n.id === id) || null;
}

// Pasa las listas de cada lado a posiciones: { pieza, d (donde empieza a lo
// largo de la calle), lado }. Necesita el ancho de cada pieza (medidas).
export function colocarNivel(nivel, anchoDe) {
  const salida = [];
  for (const [lista, lado] of [[nivel.izquierda, -1], [nivel.derecha, 1]]) {
    let d = 0;
    for (const item of lista) {
      if (typeof item === "number") { d += item; continue; }
      const [pieza, veces] = item;
      const ancho = anchoDe(pieza);
      for (let k = 0; k < veces; k++) {
        salida.push({ pieza, d, lado, ancho });
        d += ancho;
      }
    }
  }
  for (const f of nivel.fondo || []) salida.push({ pieza: f.pieza, d: f.d, lado: f.lado || 0, centro: !!f.centro, ancho: anchoDe(f.pieza) });
  return salida.sort((a, b) => a.d - b.d);
}

// Azar repetible (mulberry32): con la misma semilla, la misma secuencia.
export function azarConSemilla(semilla) {
  let a = semilla >>> 0;
  return () => {
    a = (a + 0x6d2b79f5) >>> 0;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

// Piezas que hay que cargar para jugar un nivel (las de su calle, el fondo y la puerta).
export function piezasDeNivel(nivel) {
  const set = new Set();
  for (const lado of [nivel.izquierda, nivel.derecha]) for (const it of lado) if (Array.isArray(it)) set.add(it[0]);
  for (const f of nivel.fondo || []) set.add(f.pieza);
  if (nivel.carpeta === "washington") set.add("puerta_cb");
  return [...set];
}
