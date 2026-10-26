// La gira de campaña hasta la Casa Blanca (24/10/2026). Ver DECISIONS.md.
//
// Cinco niveles con calles de verdad. Cada lado de la calle es una lista de
// edificios EN SU ORDEN REAL, uno detras de otro: [pieza, veces] repite un
// tramo de fachada (los edificios federales son muy largos), y un numero
// suelto es un cruce de calle (hueco sin edificios). Asi cada partida del
// mismo nivel tiene exactamente la misma calle, como en la vida real.
//
// Las piezas son modelos de www/models/<carpeta>/<pieza>.glb.

// Una cuadra: cuatro edificios unicos del kit y el cruce de la calle siguiente.
function cuadras(n) {
  const out = [];
  for (let i = 0; i < n; i++) out.push(["kit", 4], 14);
  return out;
}

// Edificio del kit con aire oficial (Washington).
const FED = { federal: true, minPlantas: 5, maxPlantas: 7 };

export const NIVELES = [
  {
    id: "nueva_york", numero: 1, nombre: "Quinta Avenida", lugar: "Nueva York", listo: true, mapa: [88, 25],
    ingrediente: "🫓", historia: { es: "¡Empieza la carrera a la Casa Blanca! Sal de tu torre y recupera la tortilla.", en: "The race to the White House begins! Leave your tower and get the tortilla back." },
    fin: { es: "¡Tortilla recuperada! 🫓", en: "Tortilla recovered! 🫓" },
    zona: "city", carpeta: "nueva_york", luz: "manana", semilla: 725,
    largo: 3200, estrellas: [300, 600, 950], linea: 11.5,
    // Primer nivel: lo basico. Sin autobuses ni coches patrulla; iman y microfonos.
    sinBus: true, sinPatrulla: true, potenciadores: ["magnet", "magnet", "shield", "boost"],
    kit: { minPlantas: 5, maxPlantas: 11 },
    // Bajando por la Quinta Avenida desde la calle 56: el este queda a la izquierda.
    // Cada cuadra entre dos calles son edificios unicos del kit; los monumentos en su esquina.
    izquierda: [
      ["torre_trump", 1], 14, ["kit", 2], ["st_regis", 1], 14,                    // 56th - 55th
      ...cuadras(3), ["catedral", 1], 14, ["saks", 1], ["kit", 1], 14,           // 54th - 49th
      ...cuadras(22), ["madison", 1], ["kit", 3],                               // 48th - 23rd
    ],
    derecha: [
      ["kit", 2], 14, ["peninsula", 1], ["kit", 1], 14,                           // 56th - 55th
      ["kit", 1], ["santo_tomas", 1], 14, ...cuadras(1), ["kit", 1], ["rockefeller", 1], 14,   // 53rd - 49th
      ...cuadras(6), ["biblioteca", 1], 14,                                     // 48th - 40th
      ...cuadras(6), ["empire", 1], 14,                                         // 39th - 33rd
      ...cuadras(12), ["kit", 2],                                              // 32nd - 23rd
    ],
    // Al fondo, el Flatiron con el camion de tacos delante (ahi se para).
    fondo: [{ pieza: "flatiron", d: 3245, centro: true }],
    final: "camion",
    acera: ["ciudad/farola_ciudad", "ciudad/arbol_ciudad"],
  },
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
    // Edificios del kit: 6-10 plantas (en Washington no se puede subir mas que el Capitolio).
    kit: { minPlantas: 6, maxPlantas: 10 },
    // Hacia el oeste: el sur queda a la izquierda y el norte a la derecha.
    // 26/10: los monumentos de verdad en su sitio, sus fachadas en tramos
    // cortos con patios entre medias, y el resto edificios unicos del kit
    // (FED: piedra clara y frontones, como los ministerios del Triangulo Federal).
    izquierda: [
      60,
      ["galeria_este", 1], 18,
      ["kit", 8, FED], 18, ["kit", 6, FED], 18,                                 // Galeria Nacional
      ["archivos_ala", 5], ["archivos_portico", 1], ["archivos_ala", 5], 18,     // 7th - 9th
      ["justicia", 8], 10, ["justicia", 8], 18, ["kit", 5, FED], 18,                                // 9th - 10th
      ["irs", 8], ["kit", 4, FED], ["irs", 8], 12,                              // 10th - 12th
      ["kit", 3, FED], ["correos", 5], ["correos_torre", 1], ["correos", 5], 18,  // 12th
      ["reagan", 8], ["kit", 5, FED], ["reagan", 8], 10, ["kit", 4, FED], 18,     // 12th - 14th
      ["kit", 6, FED], 18, ["kit", 3, FED], ["wilson", 1], 18,                                      // 14th
      ["kit", 2, FED], ["pershing", 1],
    ],
    derecha: [
      60,
      ["canada", 1], 18, ["cristal", 1], 18,                                    // 4th - 6th
      ["kit", 6], 18, ["kit", 5], 18, ["navy", 1], ["kit", 5], 18,             // 7th - 9th
      ["fbi", 8], 10, ["fbi", 8], 18,                                          // 9th - 10th
      ["kit", 6], 18, ["kit", 6], 18, ["kit", 5], 18, ["cristal", 1], ["kit", 5], 18, ["kit", 6], 18,  // 10th - 13th
      ["kit", 6], 18, ["kit", 6], 18, ["kit", 6], 18, ["kit", 5], 18,          // 13th - 14th
      ["kit", 6], 18, ["kit", 6], 18,
      ["willard", 1], 18,                                                      // 14th
      ["kit", 3],
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
  // Nueva York
  torre_trump: 30, st_regis: 30, peninsula: 30, santo_tomas: 28, catedral: 60, rockefeller: 60,
  saks: 40, biblioteca: 60, empire: 40, madison: 40, flatiron: 32,
};

// ¿Se puede jugar este nivel? Como en AlienZ: en orden. El primero siempre;
// cada uno, si se supero el anterior; los ya superados, siempre.
export function nivelAbierto(n, superados) {
  if (!n.listo) return false;
  if (superados[n.id]) return true;
  // Hay que haber pasado todos los anteriores QUE YA EXISTEN: mientras falten
  // niveles por hacer, al pasar Nueva York se abre directamente Washington.
  const i = NIVELES.indexOf(n);
  return NIVELES.slice(0, i).filter((x) => x.listo).every((x) => superados[x.id]);
}
// El Sin fin se abre al superar el primer nivel.
export function sinFinAbierto(superados) {
  return !!superados[NIVELES[0].id];
}

export function nivelPorId(id) {
  return NIVELES.find((n) => n.id === id) || null;
}

// Recorre un lado de la calle y da cada edificio con su sitio: { pieza, d,
// ancho, semilla (kit), opciones (kit) }. Los numeros sueltos son cruces.
function recorrerLado(nivel, lista, lado, anchoDe, alEdificio, alCruce) {
  let d = 0;
  for (const item of lista) {
    if (typeof item === "number") { if (alCruce) alCruce(d, item); d += item; continue; }
    const [pieza, veces, opciones] = item;
    for (let k = 0; k < veces; k++) {
      if (pieza === "kit") {
        // Edificio unico: su ancho y su semilla salen del sitio que ocupa.
        const semilla = nivel.semilla * 7919 + (lado > 0 ? 500000 : 0) + Math.round(d);
        const a = azarConSemilla(semilla);
        const ancho = [18, 20, 22, 24, 26, 40][Math.floor(a() * 6)];
        alEdificio({ pieza, d, lado, ancho, semilla, opciones });
        d += ancho;
        continue;
      }
      const ancho = anchoDe(pieza);
      alEdificio({ pieza, d, lado, ancho });
      d += ancho;
    }
  }
  return d;
}

// Pasa las listas de cada lado a posiciones: { pieza, d (donde empieza a lo
// largo de la calle), lado }. Necesita el ancho de cada pieza (medidas).
export function colocarNivel(nivel, anchoDe) {
  const salida = [];
  recorrerLado(nivel, nivel.izquierda, -1, anchoDe, (e) => salida.push(e));
  recorrerLado(nivel, nivel.derecha, 1, anchoDe, (e) => salida.push(e));
  for (const f of nivel.fondo || []) salida.push({ pieza: f.pieza, d: f.d, lado: f.lado || 0, centro: !!f.centro, ancho: anchoDe(f.pieza) });
  return salida.sort((a, b) => a.d - b.d);
}

// Lo largo que es cada lado (para comprobar que llegan a donde toca).
export function largoDeLados(nivel) {
  const a = (k) => ANCHO[k] || 20;
  return [recorrerLado(nivel, nivel.izquierda, -1, a, () => {}), recorrerLado(nivel, nivel.derecha, 1, a, () => {})];
}

// Lo que va pintado o puesto en el suelo de la calle (25/10): un paso de
// cebra en cada cruce (los huecos de 12 o mas de la acera izquierda) y tapas
// de alcantarilla junto al bordillo cada 45-70. Siempre en el mismo sitio.
// (26/10: los cruces se miden con el ancho real de cada edificio del kit.)
export function sueloDeNivel(nivel) {
  const salida = [];
  recorrerLado(nivel, nivel.izquierda, -1, (k) => ANCHO[k] || 20, () => {}, (d, hueco) => {
    if (hueco >= 12) salida.push({ tipo: "cebra", d: d + hueco / 2 });
  });
  const azar = azarConSemilla(nivel.semilla + 7);
  for (let x = 30; x < nivel.largo - 40; x += 45 + azar() * 25) {
    salida.push({ tipo: "tapa", d: x, x: (azar() < 0.5 ? -1 : 1) * 3.1 });
  }
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
  set.delete("kit");   // los del kit van en su carpeta (ver usaKit)
  return [...set];
}
export function usaKit(nivel) {
  return [nivel.izquierda, nivel.derecha].some((lado) => lado.some((it) => Array.isArray(it) && it[0] === "kit"));
}
