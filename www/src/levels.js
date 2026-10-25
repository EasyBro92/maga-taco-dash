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
  { id: "nueva_york", numero: 1, nombre: "Quinta Avenida", lugar: "Nueva York", listo: false, mapa: [88, 25],
    ingrediente: "🫓", historia: { es: "¡Empieza la carrera a la Casa Blanca! Sal de tu torre y recupera la tortilla.", en: "The race to the White House begins! Leave your tower and get the tortilla back." } },
  { id: "pueblo", numero: 2, nombre: "Calle Mayor", lugar: "Ohio", listo: false, mapa: [73, 29],
    ingrediente: "🌽", historia: { es: "Mitin en un pueblo de Ohio. El Burrito-Bot ha escondido el maíz: ¡súbete a los autobuses!", en: "Rally in an Ohio town. Burrito-Bot hid the corn: ride the buses!" } },
  { id: "ruta66", numero: 3, nombre: "Ruta 66", lugar: "Arizona", listo: false, mapa: [27, 45],
    ingrediente: "🌶️", historia: { es: "Ruta 66 por el desierto. ¡La policía te persigue! Es una caza de brujas.", en: "Route 66 through the desert. The police are after you! It is a witch hunt." } },
  { id: "vegas", numero: 4, nombre: "El Strip", lugar: "Las Vegas", listo: false, mapa: [17, 38],
    ingrediente: "🥫", historia: { es: "Debate en Las Vegas contra el Burrito-Bot, el candidato hecho en China. ¡Gánale!", en: "Debate in Las Vegas against Burrito-Bot, the made-in-China candidate. Beat him!" } },
  {
    id: "washington", numero: 5, nombre: "Pennsylvania Avenue", lugar: "Washington D.C.", listo: true, mapa: [85, 33],
    ingrediente: "🏛️", historia: { es: "La recta final. Corre por Pennsylvania Avenue y entra en la Casa Blanca: ¡el taco perfecto te espera!", en: "The home stretch. Run down Pennsylvania Avenue into the White House: the perfect taco awaits!" },
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

// ¿Se puede jugar este nivel? Como en AlienZ: en orden. El primero siempre;
// cada uno, si se supero el anterior; los ya superados, siempre.
// Mientras no exista el nivel 1, Washington queda abierto (lo decidio Isidro el
// 25/10 para poder seguir jugandolo mientras se hacen los otros).
export function nivelAbierto(n, superados) {
  if (!n.listo) return false;
  if (superados[n.id]) return true;
  if (n.id === "washington" && !NIVELES[0].listo) return true;
  const i = NIVELES.indexOf(n);
  return i === 0 || !!superados[NIVELES[i - 1].id];
}
// El Sin fin se abre al superar el primer nivel.
export function sinFinAbierto(superados) {
  return !!superados[NIVELES[0].id];
}

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
