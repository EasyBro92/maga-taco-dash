// La gira de campaña hasta la Casa Blanca (24/10/2026). Ver DECISIONS.md.
//
// 28/10/2026: la historia nueva (HISTORIA.md, src/historia.js) pone el orden:
// 51 paradas, una por estado, y Washington la última. Aquí solo están las
// calles de los niveles ya hechos; los demás salen en el mapa con candado.
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

// ---- Tramos (27/10/2026) ----
// Isidro: «los niveles no sé cuándo acaban, son muy repetitivos». Antes cada
// fila salía al azar de principio a fin. Ahora cada nivel va por partes, cada
// una con su forma y su nombre (lo que sale en el cartel al entrar):
//   [desde, hasta, tipo, opciones]
//   tutorial  enseña los gestos (solo el nivel 1)
//   calma     solo tacos: un respiro
//   suave / mixto   lo de siempre, con más o menos obstáculos (densidad)
//   vallas    filas enteras que hay que saltar o pasar agachado
//   slalom    dos carriles cerrados y el libre va cambiando de sitio
//   autobuses autobuses con tacos en el techo, uno tras otro
//   festin    un potenciador seguro y lluvia de tacos
//   obras · desfile · comitiva   lo propio de cada ciudad
//   jefe      llega el Burrito-Bot (tacos y chiles para darle)
//   sprint    el último tramo, con aviso: ya se ve la meta
// `control` es el punto de control (se puede seguir desde ahí si se choca) y
// `chapas` las tres chapas de campaña escondidas, cada una con su truco:
//   arco (se coge saltando sobre una valla), carril (justo detrás de un
//   obstáculo) o bus (en el techo de un autobús).
// Las estrellas: llegar · llegar sin chocar · las tres chapas.

import { PARADAS } from "./historia.js";

const CALLES = [
  {
    id: "nueva_york", nombre: "Quinta Avenida", lugar: "Nueva York", listo: true,
    zona: "city", carpeta: "nueva_york", luz: "manana", semilla: 725,
    largo: 3200, linea: 11.5, velMax: 20,
    // Primer nivel: lo basico. Sin autobuses ni coches patrulla; iman y microfonos.
    sinBus: true, sinPatrulla: true, potenciadores: ["magnet", "magnet", "shield", "boost"],
    kit: { minPlantas: 5, maxPlantas: 11 },
    horizonte: "manhattan", cameoJefe: true,
    obstaculos: { low: ["conos", "barricada", "alcantarilla"], high: ["pancarta", "andamio", "globos"],
      full: ["taxi", "taxi", "furgoneta", "contenedor", "guardaespaldas"] },
    publico: { personas: ["ejecutivo", "turista", "chico", "senora", "turista"], valla: "policia", cada: 2 },
    tramos: [
      [0, 280, "tutorial"],
      [280, 620, "suave", { densidad: 0.4, titulo: "quinta" }],
      [620, 760, "festin", { potenciador: "magnet", titulo: "festin" }],
      [760, 1150, "slalom", { full: ["taxi"], titulo: "atasco" }],
      [1150, 1290, "calma"],
      [1290, 1580, "obras", { titulo: "obras" }],
      [1580, 1680, "calma"],
      [1680, 2100, "vallas", { titulo: "vallas" }],
      [2100, 2240, "festin", { potenciador: "shield", titulo: "festin" }],
      [2240, 2650, "mixto", { densidad: 0.55, titulo: "hora_punta" }],
      [2650, 2900, "obras", { low: ["alcantarilla"], titulo: "vapor" }],
      [2900, 3170, "sprint", { titulo: "sprint" }],
    ],
    control: 1610, caja: 1100,
    chapas: [[700, "arco"], [1430, "carril"], [2520, "arco"]],
    hitos: ["rockefeller", "catedral", "biblioteca", "empire", "madison"],
    meta: "flatiron", metaNombre: { es: "el Flatiron", en: "the Flatiron" },
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
  {
    id: "pueblo", nombre: "Main Street", lugar: "Findlay, Ohio", listo: true,
    zona: "city", carpeta: "findlay", luz: "mediodia", semilla: 1888,
    largo: 3200, linea: 11.5, velMax: 21.5,
    // Segundo nivel: entran los autobuses de campaña (por el techo hay tacos).
    sinPatrulla: true, potenciadores: ["magnet", "shield", "boost", "magnet", "botas"],
    // Main Street de pueblo: ladrillo, de una a tres plantas sobre las tiendas.
    kit: { pueblo: true, minPlantas: 1, maxPlantas: 3 },
    horizonte: "ohio",
    obstaculos: { low: ["paca", "paca", "conos", "barricada"], high: ["guirnalda", "pancarta", "globos"],
      full: ["tractor", "carroza", "furgoneta"] },
    publico: { personas: ["abuelo", "senora", "fan", "chico", "abuelo"], valla: "banderas", cada: 2 },
    tramos: [
      [0, 200, "calma", { titulo: "main_street" }],
      [200, 560, "suave", { densidad: 0.42 }],
      [560, 860, "autobuses", { titulo: "autobuses" }],
      [860, 1000, "festin", { potenciador: "mega", titulo: "gigante" }],
      [1000, 1400, "desfile", { titulo: "desfile" }],
      [1400, 1540, "calma"],
      [1540, 2300, "jefe", { titulo: "jefe" }],
      [2300, 2650, "slalom", { full: ["tractor"], titulo: "tractores" }],
      [2650, 2900, "autobuses", { titulo: "autobuses" }],
      [2900, 3170, "sprint", { titulo: "sprint" }],
    ],
    control: 1547, caja: 1000,
    chapas: [[700, "bus"], [1253, "arco"], [2786, "bus"]],
    hitos: ["courier", "heladeria", "deposito_agua", "davis"],
    meta: "juzgado_final", metaNombre: { es: "el juzgado", en: "the courthouse" },
    // Subiendo por South Main Street hacia el norte: el oeste queda a la izquierda.
    izquierda: [
      40, ["kit", 3], 14, ["courier", 1], ["kit", 2], 14,
      ...cuadras(7), ["heladeria", 1], ["kit", 3], 14,
      ...cuadras(8), ["deposito_agua", 1], ["kit", 3], 14,
      ...cuadras(9), ["kit", 2], ["davis", 1], ["kit", 1],
    ],
    derecha: [
      40, ["marathon", 1], ["kit", 2], 14,
      ...cuadras(27), ["kit", 2],
    ],
    // Al fondo, el juzgado del condado con la plaza y el escenario del mitin.
    fondo: [{ pieza: "juzgado_final", d: 3240, centro: true }],
    final: "mitin",
    acera: ["findlay/farola_bandera", "ciudad/arbol_ciudad"],
  },
  {
    // 27/10/2026: Isidro quiere la capital o la ciudad mas famosa de cada
    // estado (ver GIRA.md); en Arizona, Phoenix. Final en un diner, luz de tarde dorada.
    id: "phoenix", nombre: "Central Avenue", lugar: "Phoenix, Arizona", listo: true,
    zona: "city", carpeta: "phoenix", luz: "tarde", semilla: 1912,
    largo: 3200, linea: 11.5, velMax: 22,
    potenciadores: ["magnet", "shield", "boost", "mega", "botas"],
    // Centro de Phoenix: estuco de colores calidos, de dos a nueve plantas.
    kit: { desierto: true, minPlantas: 2, maxPlantas: 9 },
    horizonte: "phoenix",
    obstaculos: { low: ["nopal", "nopal", "conos", "barricada"], high: ["arco_neon", "pancarta", "globos"],
      full: ["saguaro", "pickup", "pickup", "furgoneta"] },
    publico: { personas: ["turista", "fan", "abuelo", "chico", "senora"], valla: "banderas", cada: 3 },
    tramos: [
      [0, 200, "calma", { titulo: "central" }],
      [200, 560, "suave", { densidad: 0.42 }],
      [560, 860, "rodadoras", { titulo: "rodadoras" }],
      [860, 1000, "festin", { potenciador: "boost", titulo: "festin" }],
      [1000, 1400, "persecucion", { titulo: "persecucion" }],
      [1400, 1540, "calma"],
      [1540, 1950, "vallas", { high: ["arco_neon"], titulo: "neones" }],
      [1950, 2300, "autobuses", { titulo: "autobuses" }],
      [2300, 2450, "festin", { potenciador: "mega", titulo: "gigante" }],
      [2450, 2900, "persecucion", { titulo: "caza_brujas" }],
      [2900, 3170, "sprint", { titulo: "sprint_diner" }],
    ],
    control: 1547, caja: 1150,
    chapas: [[707, "arco"], [2100, "bus"], [2604, "carril"]],
    hitos: ["san_carlos", "westward_ho", "biblioteca_barr", "museo_arte", "museo_heard"],
    meta: "diner_final", metaNombre: { es: "el diner", en: "the diner" }, coche: "patrulla",
    // Subiendo por Central Avenue hacia el norte: el oeste queda a la izquierda.
    izquierda: [
      40, ["kit", 2], ["san_carlos", 1], ["kit", 1], 14,
      ...cuadras(8), ["biblioteca_barr", 1], ["kit", 2], 14,
      ...cuadras(17), ["kit", 4],
    ],
    derecha: [
      40, ["kit", 3], 14, ...cuadras(3), ["westward_ho", 1], ["kit", 2], 14,
      ...cuadras(8), ["museo_arte", 1], ["kit", 2], 14,
      ...cuadras(7), ["museo_heard", 1], ["kit", 2], 14,
      ...cuadras(6), ["kit", 2],
    ],
    fondo: [{ pieza: "diner_final", d: 3245, centro: true }],
    final: "parada", parada: 3.2,
    acera: ["phoenix/palmera", "phoenix/saguaro_maceta"],
  },
  {
    id: "washington", nombre: "Pennsylvania Avenue", lugar: "Washington D.C.", listo: true,
    zona: "dc",
    carpeta: "washington",
    luz: "atardecer",
    semilla: 1600,                 // el mismo reparto de obstaculos cada vez
    largo: 3300,                   // donde esta la verja de la Casa Blanca
    linea: 11.5,                   // x de las fachadas
    velMax: 23,
    // Edificios del kit: 6-10 plantas (en Washington no se puede subir mas que el Capitolio).
    kit: { minPlantas: 6, maxPlantas: 10 },
    horizonte: "dc",
    potenciadores: ["magnet", "shield", "boost", "mega", "freeze", "rocket", "botas"],
    obstaculos: { low: ["valla_metal", "valla_metal", "barricada", "conos"], high: ["protesta", "pancarta", "globos"],
      full: ["agentes", "agentes", "furgoneta", "guardaespaldas"] },
    publico: { personas: ["ejecutivo", "fan", "turista", "senora", "ejecutivo"], valla: "verja", cada: 2 },
    tramos: [
      [0, 200, "calma", { titulo: "pennsylvania" }],
      [200, 560, "mixto", { densidad: 0.5 }],
      [560, 900, "comitiva", { titulo: "comitiva" }],
      [900, 1060, "festin", { potenciador: "rocket", titulo: "cohete" }],
      [1060, 1450, "vallas", { high: ["protesta"], titulo: "protesta" }],
      [1450, 1680, "autobuses", { titulo: "autobuses" }],
      [1680, 1750, "calma"],
      [1750, 2450, "jefe", { titulo: "jefe_final" }],
      [2450, 2600, "festin", { potenciador: "freeze", titulo: "hielo" }],
      [2600, 3000, "slalom", { full: ["agentes", "furgoneta"], titulo: "recta" }],
      [3000, 3270, "sprint", { titulo: "sprint_dc" }],
    ],
    control: 1694, caja: 950,
    chapas: [[1204, "arco"], [1561, "bus"], [2751, "carril"]],
    hitos: ["archivos_portico", "fbi", "irs", "correos_torre", "willard", "tesoro"],
    meta: "casa_blanca_final", metaNombre: { es: "la Casa Blanca", en: "the White House" }, coche: "suv",
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

// Las 51 paradas de la historia, con la calle de las que ya existen.
// (`jefe` de la historia pasa a `esJefe`: el jefe de verdad es el tramo «jefe».)
export const NIVELES = PARADAS.map(({ jefe, ...p }) => {
  const calle = CALLES.find((c) => c.id === p.id);
  return calle ? { ...calle, ...p, esJefe: jefe } : { ...p, esJefe: jefe, listo: false };
});

// Ancho de cada pieza a lo largo de la calle (el de su fachada, sin contar lo
// que sobresale la cornisa: asi los tramos encajan sin pisarse).
export const ANCHO = {
  archivos_ala: 20, archivos_portico: 34, justicia: 20, irs: 20, correos: 20, correos_torre: 30,
  reagan: 20, wilson: 40, pershing: 40, canada: 30, cristal: 30, navy: 40, fbi: 20, willard: 35,
  galeria_este: 40, tesoro: 60, casa_blanca_final: 76,
  // Nueva York
  torre_trump: 30, st_regis: 30, peninsula: 30, santo_tomas: 28, catedral: 60, rockefeller: 60,
  saks: 40, biblioteca: 60, empire: 40, madison: 40, flatiron: 32,
  // Findlay
  courier: 24, heladeria: 20, deposito_agua: 20, davis: 20, marathon: 40, juzgado_final: 62,
  // Phoenix
  san_carlos: 30, westward_ho: 30, biblioteca_barr: 40, museo_arte: 40, museo_heard: 40, diner_final: 30,
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
  // El arco del punto de control, de lado a lado de la calle.
  if (nivel.control) salida.push({ pieza: "arco_control", d: nivel.control, lado: 0, arco: true, ancho: 2 });
  return salida.sort((a, b) => a.d - b.d);
}

// Los edificios famosos que salen en la barra de progreso: { pieza, d } con
// la d en el centro de su fachada (la primera vez que aparece cada uno).
export function hitosDeNivel(nivel) {
  const lista = colocarNivel(nivel, (k) => ANCHO[k] || 20);
  return (nivel.hitos || []).map((h) => {
    const e = lista.find((x) => x.pieza === h);
    return e ? { pieza: h, d: e.d + e.ancho / 2 } : null;
  }).filter(Boolean);
}

// El punto de control en metros redondos de fila (7): si se sigue desde ahi,
// las filas caen en el mismo sitio que la primera vez.
export function salidaControl(nivel) {
  return Math.floor((nivel.control - 25) / 7) * 7;
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
