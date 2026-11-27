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

// 12/11: un trozo de bosque de las Black Hills (Monte Rushmore): pinares y
// agujas de granito, sin huecos grandes (no son calles).
function bosque(n) {
  const out = [];
  for (let i = 0; i < n; i++) out.push(["pinar", 1], 4, ["agujas_granito", 1], 4);
  return out;
}

// Edificio del kit con aire oficial (Washington).
const FED = { federal: true, minPlantas: 5, maxPlantas: 7 };
// East Village de Des Moines: ladrillo bajo, de una a tres plantas (y nevado).
const EV = { pueblo: true, minPlantas: 1, maxPlantas: 3 };
function cuadrasCon(n, op) {
  const out = [];
  for (let i = 0; i < n; i++) out.push(["kit", 4, op], 14);
  return out;
}

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
//   jefe      llega el Burrito-Bot (tacos y chiles para darle); con { jefe: "dragon" },
//             el dragon de China (Des Moines)
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
    largo: 1400, linea: 11.5, velMax: 20,
    // Primer nivel: lo basico. Sin autobuses ni coches patrulla; iman y microfonos.
    sinBus: true, sinPatrulla: true, potenciadores: ["magnet", "magnet", "shield", "boost"],
    kit: { minPlantas: 5, maxPlantas: 11 },
    horizonte: "manhattan", cameoJefe: true,
    // 31/10: cada mapa con sus obstaculos (Isidro: «que los mapas se sientan diferentes»).
    // 06/11: Isidro: «se hacen repetitivos los obstaculos, faltan mas tipos y mas
    // dinamismo». Nuevos: la boca de riego abierta, el balon que viene botando, el semaforo colgado,
    // el coche de caballos (cambia de carril) y el paseador de perros (cruza).
    obstaculos: { low: ["alcantarilla", "basura", "hidrante", "balon"], high: ["andamio", "viga", "semaforo"],
      full: ["taxi", "contenedor", "perritos", "furgoneta", "carruaje", "paseador"] },
    publico: { personas: ["ejecutivo", "turista", "chico", "senora", "turista"], valla: "policia", cada: 2 },
    // 05/11: Isidro: «los primeros niveles deben ser mas cortos y luego ir
    // alargandose» y «los niveles se siguen sintiendo muy iguales». Antes los
    // seis median 3,2 km y seguian el mismo orden casi en los mismos metros.
    // Nueva York: 1.400 m. Tutorial, el atasco y las obras; el festin, al final.
    // 06/11 (3): Isidro: «más cosas, muchas más, que no sea tan repetitivo».
    // Un momento cada 20 s más o menos (ver «Los momentos» en world.js); el
    // largo del nivel no cambia.
    tramos: [
      [0, 280, "tutorial"],
      [280, 420, "lluvia", { titulo: "lluvia" }],
      [420, 560, "slalom", { full: ["taxi", "taxi", "carruaje"], titulo: "atasco" }],
      [560, 700, "jefe_paso", { titulo: "jefe_paso" }],
      [700, 780, "calma"],
      // 07/11: el momento estrella, el metro (en lugar de las obras y el festin).
      // Primero las vias y luego el techo del tren; la estacion, en `fondo`.
      [780, 930, "metro_vias", { titulo: "metro" }],
      [930, 1078, "metro_techo", { titulo: "metro_techo" }],
      [1078, 1240, "repartidores", { momento: "persigue", perseguidor: "furgoneta_fake", titulo: "persigue_prensa" }],
      [1240, 1370, "sprint", { titulo: "sprint" }],
    ],
    control: 712, caja: 640,
    // (La segunda, en el techo del tren del metro.)
    chapas: [[430, "arco"], [995, "techo"], [1180, "arco"]],
    // 07/11: el metro: la boca a ras de calle justo despues de la biblioteca,
    // dos trozos de tunel, la estacion 5 Av (150 m), cuatro de tunel y la salida.
    // (08/11 (2): la boca es un edificio de estacion de lado a lado: sin los
    // edificios de los lados, que se metian en ella.)
    interior: { rango: [772, 1082], tipo: "metro", sinEdificios: [760, 1090] },
    // (El helicoptero, fuera del metro.)
    // (11/11: una sola vez: a los 1150 coincidia con la furgoneta de la prensa)
    helicoptero: [420],
    hitos: ["rockefeller", "catedral", "biblioteca", "empire", "madison"],
    meta: "flatiron", metaNombre: { es: "el Flatiron", en: "the Flatiron" },
    // Bajando por la Quinta Avenida desde la calle 56: el este queda a la izquierda.
    // Cada cuadra entre dos calles son edificios unicos del kit; los monumentos en su esquina.
    izquierda: [
      ["torre_trump", 1], 14, ["kit", 2], ["st_regis", 1], 14,                    // 56th - 55th
      ...cuadras(3), ["catedral", 1], 14, ["saks", 1], ["kit", 1], 14,           // 54th - 49th
      ...cuadras(6), ["madison", 1], ["kit", 3],                               // 48th - 23rd
    ],
    derecha: [
      ["kit", 2], 14, ["peninsula", 1], ["kit", 1], 14,                           // 56th - 55th
      ["kit", 1], ["santo_tomas", 1], 14, ...cuadras(1), ["kit", 1], ["rockefeller", 1], 14,   // 53rd - 49th
      ...cuadras(3), ["biblioteca", 1], 14,                                     // 48th - 40th
      ...cuadras(3), ["empire", 1], 14,                                         // 39th - 33rd
      ...cuadras(2), ["kit", 2],                                              // 32nd - 23rd
    ],
    // Al fondo, el Flatiron con el camion de tacos delante (ahi se para).
    fondo: [{ pieza: "flatiron", d: 1445, centro: true },
      { pieza: "metro_boca", d: 772, cruza: true },
      ...[780, 804].map((d) => ({ pieza: "metro_tunel", d, cruza: true })),
      ...[828, 858, 888, 918, 948].map((d) => ({ pieza: "metro_estacion", d, cruza: true })),
      ...[978, 1002, 1026, 1050].map((d) => ({ pieza: "metro_tunel", d, cruza: true })),
      { pieza: "metro_salida", d: 1074, cruza: true }],
    final: "camion",
    // 08/11 (2): mas cosas en la acera y distintas en cada ciudad.
    acera: ["ciudad/farola_ciudad", "ciudad/arbol_ciudad", "ciudad/hidrante", "ciudad/farola_ciudad", "ciudad/arbol_ciudad", "ciudad/buzon"],
  },
  {
    id: "pueblo", nombre: "Main Street", lugar: "Findlay, Ohio", listo: true,
    zona: "city", carpeta: "findlay", luz: "mediodia", semilla: 1888,
    largo: 1700, linea: 11.5, velMax: 21.5,
    // Segundo nivel: entran los autobuses de campaña (por el techo hay tacos).
    sinPatrulla: true, potenciadores: ["magnet", "shield", "boost", "magnet", "botas"],
    // Main Street de pueblo: ladrillo, de una a tres plantas sobre las tiendas.
    kit: { pueblo: true, minPlantas: 1, maxPlantas: 3 },
    horizonte: "ohio",
    // 06/11: Isidro: «se hacen repetitivos los obstaculos, faltan mas tipos y mas
    // dinamismo». Nuevos: el paso a nivel del tren (sube y baja), los pavos (cruzan), la bandera
    // gigante, el cortacesped (cambia de carril) y el puesto de limonada.
    obstaculos: { low: ["paca", "calabazas", "paso_nivel", "pavos"], high: ["guirnalda", "globos", "bandera_grande"],
      full: ["tractor", "carroza", "vaca", "furgoneta", "cortacesped", "limonada"] },
    publico: { personas: ["abuelo", "senora", "fan", "chico", "abuelo"], valla: "banderas", cada: 2 },
    // 05/11: Isidro: «los primeros niveles deben ser mas cortos y luego ir
    // alargandose» y «los niveles se siguen sintiendo muy iguales». Antes los
    // seis median 3,2 km y seguian el mismo orden casi en los mismos metros.
    // Findlay: 1.700 m. Empieza con el desfile, el jefe a mitad y las vacas al final.
    tramos: [
      // 06/11 (2): Isidro: «algunos mapas largos al principio se hacen aburridos»:
      // la calma de la salida pasa de 150 a 70-90 m en los niveles largos.
      [0, 80, "calma", { titulo: "main_street" }],
      // 07/11: el momento estrella: el tunel de banderas del 4 de julio, por
      // encima de las carrozas del desfile (en lugar del desfile y de subirse a
      // la carroza). Las banderas, en `fondo`.
      [80, 380, "banderas", { titulo: "banderas" }],
      [380, 640, "autobuses", { titulo: "autobuses" }],
      [640, 740, "premios", { titulo: "premios" }],
      [740, 1340, "jefe", { titulo: "jefe" }],
      [1340, 1430, "festin", { potenciador: "mega", titulo: "gigante" }],
      [1430, 1580, "vacas", { momento: "persigue", perseguidor: "vaca", titulo: "persigue_vaca" }],
      [1580, 1670, "sprint", { titulo: "sprint" }],
    ],
    // (El control, detras de los arcos de premio: delante se tapaban.)
    control: 720, caja: 600,
    chapas: [[540, "bus"], [1490, "arco"], [1620, "carril"]],
    hitos: ["courier", "heladeria", "deposito_agua", "davis"],
    meta: "juzgado_final", metaNombre: { es: "el juzgado", en: "the courthouse" },
    // Subiendo por South Main Street hacia el norte: el oeste queda a la izquierda.
    izquierda: [
      40, ["kit", 3], 14, ["courier", 1], ["kit", 2], 14,
      ...cuadras(4), ["heladeria", 1], ["kit", 3], 14,
      ...cuadras(4), ["deposito_agua", 1], ["kit", 3], 14,
      ...cuadras(2), ["kit", 2], ["davis", 1], ["kit", 3],
    ],
    derecha: [
      40, ["marathon", 1], ["kit", 2], 14,
      ...cuadras(14), ["kit", 2],
    ],
    // Al fondo, el juzgado del condado con la plaza y el escenario del mitin.
    fondo: [{ pieza: "juzgado_final", d: 1740, centro: true },
      ...Array.from({ length: 17 }, (_, i) => ({ pieza: "banderas_arco", d: 86 + i * 18, cruza: true }))],
    final: "mitin",
    acera: ["findlay/farola_bandera", "ciudad/arbol_ciudad"],
  },
  {
    // 27/10/2026: Isidro quiere la capital o la ciudad mas famosa de cada
    // estado (ver GIRA.md); en Arizona, Phoenix. Final en un diner, luz de tarde dorada.
    id: "phoenix", nombre: "Central Avenue", lugar: "Phoenix, Arizona", listo: true,
    zona: "city", carpeta: "phoenix", luz: "tarde", semilla: 1912,
    largo: 2000, linea: 11.5, velMax: 22,
    potenciadores: ["magnet", "shield", "boost", "mega", "botas"],
    // Centro de Phoenix: estuco de colores calidos, de dos a nueve plantas.
    kit: { desierto: true, minPlantas: 2, maxPlantas: 9 },
    horizonte: "phoenix",
    // 06/11: Isidro: «se hacen repetitivos los obstaculos, faltan mas tipos y mas
    // dinamismo». Nuevos: la serpiente de cascabel, la rueda suelta que viene botando, la piñata,
    // la autocaravana (cambia de carril) y el vaquero a caballo (cruza).
    obstaculos: { low: ["nopal", "calavera", "serpiente", "rueda_loca"], high: ["arco_neon", "cartel_ruta", "pinata"],
      full: ["saguaro", "pickup", "furgoneta", "autocaravana", "vaquero"] },
    publico: { personas: ["turista", "fan", "abuelo", "chico", "senora"], valla: "banderas", cada: 3 },
    // 05/11: Isidro: «los primeros niveles deben ser mas cortos y luego ir
    // alargandose» y «los niveles se siguen sintiendo muy iguales». Antes los
    // seis median 3,2 km y seguian el mismo orden casi en los mismos metros.
    // Phoenix: 2.000 m. Las rodadoras nada mas salir y la gran persecucion al final.
    // 06/11 (3): Isidro: «más cosas, muchas más, que no sea tan repetitivo».
    // Un momento cada 20 s más o menos (ver «Los momentos» en world.js); el
    // largo del nivel no cambia.
    tramos: [
      [0, 70, "calma", { titulo: "central" }],
      [70, 300, "rodadoras", { titulo: "rodadoras" }],
      [300, 440, "rampa", { titulo: "rampa" }],
      [440, 520, "festin", { potenciador: "boost", titulo: "festin" }],
      [520, 720, "autobuses", { titulo: "autobuses" }],
      [720, 860, "jefe_paso", { titulo: "jefe_paso" }],
      // 08/11: el momento estrella: el puente sobre el cañon (en lugar de los
      // neones). El cañon, en `fondo`; la calle se corta (`interior`).
      [860, 1130, "canon", { puente: [920, 1070], titulo: "canon" }],
      [1130, 1220, "suave", { densidad: 0.55, momento: "vehiculo", vehiculo: "carrito_golf", titulo: "sube_golf" }],
      [1220, 1400, "desfile_cruza", { cruzan: ["vaquero"], titulo: "cruzan_vaqueros" }],
      [1400, 1830, "persecucion", { titulo: "caza_brujas" }],
      [1830, 1970, "sprint", { titulo: "sprint_diner" }],
    ],
    control: 812, caja: 1250,
    chapas: [[600, "bus"], [1050, "arco"], [1300, "carril"]],
    hitos: ["san_carlos", "westward_ho", "biblioteca_barr", "museo_arte", "museo_heard"],
    meta: "diner_final", metaNombre: { es: "el diner", en: "the diner" }, coche: "patrulla",
    // Subiendo por Central Avenue hacia el norte: el oeste queda a la izquierda.
    izquierda: [
      40, ["kit", 2], ["san_carlos", 1], ["kit", 1], 14,
      ...cuadras(5), ["biblioteca_barr", 1], ["kit", 2], 14,
      ...cuadras(10), ["kit", 4],
    ],
    derecha: [
      40, ["kit", 3], 14, ...cuadras(2), ["westward_ho", 1], ["kit", 2], 14,
      // (11/11: el museo, antes del cañón: dentro no hay edificios y no salía)
      ...cuadras(2), ["museo_arte", 1], ["kit", 2], 14,
      ...cuadras(7), ["museo_heard", 1], ["kit", 2], 14,
      ...cuadras(2), ["kit", 2],
    ],
    fondo: [{ pieza: "diner_final", d: 2045, centro: true },
      ...[860, 890].map((d) => ({ pieza: "canon_corte", d, cruza: true })),
      ...[920, 950, 980, 1010, 1040].map((d) => ({ pieza: "canon_puente", d, cruza: true })),
      ...[1070, 1100].map((d) => ({ pieza: "canon_corte", d, cruza: true }))],
    // 08/11: el cañon: sin calle, sin edificios y sin lo de las aceras (como los
    // interiores, pero sin cambiar la luz).
    interior: { rango: [860, 1130], tipo: "canon", sinEdificios: true },
    final: "parada", parada: 3.2,
    acera: ["phoenix/palmera", "phoenix/saguaro_maceta"],
  },
  {
    // 29/10/2026: nivel 4, el debate contra el Burrito-Bot (jefe del acto 1).
    // Isidro eligio final en la torre dorada del hotel Trump, luz de anochecer
    // con los neones encendidos (fijos: nada parpadea) y ganar el debate con
    // microfonos: cada uno que coges le lanza una frase al robot.
    id: "vegas", nombre: "El Strip", lugar: "Las Vegas, Nevada", listo: true,
    zona: "city", carpeta: "vegas", luz: "anochecer", semilla: 1905,
    largo: 2300, linea: 11.5, velMax: 22.5,
    potenciadores: ["magnet", "shield", "boost", "mega", "botas"],
    // Hoteles y casinos: altos, claros y con letreros de neon.
    kit: { vegas: true, minPlantas: 4, maxPlantas: 12 },
    horizonte: "vegas", debate: true,
    // 06/11: Isidro: «se hacen repetitivos los obstaculos, faltan mas tipos y mas
    // dinamismo». Nuevos: la ruleta, la barrera del aparcamiento (sube y baja), el cartel de la
    // capilla de bodas, el descapotable rosa (cambia de carril) y las bailarinas (cruzan).
    obstaculos: { low: ["fichas", "ruleta", "barrera_valet"], high: ["marquesina", "cartel_boda"],
      full: ["tragaperras", "limusina", "elvis", "furgoneta", "descapotable", "bailarinas"] },
    publico: { personas: ["turista", "fan", "ejecutivo", "senora", "chico"], valla: "verja", cada: 2 },
    // 05/11: Isidro: «los primeros niveles deben ser mas cortos y luego ir
    // alargandose» y «los niveles se siguen sintiendo muy iguales». Antes los
    // seis median 3,2 km y seguian el mismo orden casi en los mismos metros.
    // Las Vegas: 2.300 m. Las limusinas de entrada, los dados y el debate a mitad.
    // 06/11 (3): Isidro: «más cosas, muchas más, que no sea tan repetitivo».
    // Un momento cada 20 s más o menos (ver «Los momentos» en world.js); el
    // largo del nivel no cambia.
    tramos: [
      [0, 70, "calma", { titulo: "strip" }],
      [70, 260, "slalom", { full: ["limusina", "limusina", "descapotable"], titulo: "limusinas" }],
      [260, 380, "alfombra", { titulo: "alfombra" }],
      // 07/11: el momento estrella: dentro del casino Trump (la sala, en
      // `fondo`) y, al salir, una lluvia de fichas delante de la torre Eiffel.
      // Justo antes de la torre: dentro del casino no se veria.
      [380, 550, "casino", { titulo: "casino" }],
      [550, 650, "lluvia", { fichas: true, titulo: "lluvia_fichas" }],
      [650, 780, "dados", { titulo: "dados" }],
      [780, 1400, "jefe", { titulo: "debate" }],
      [1400, 1500, "festin", { potenciador: "mega", titulo: "gigante" }],
      [1500, 1680, "vallas", { high: ["marquesina", "cartel_boda"], momento: "gorras", titulo: "gorras" }],
      [1680, 1840, "mixto", { densidad: 0.6, momento: "vehiculo", vehiculo: "descapotable", titulo: "sube_descapotable" }],
      [1840, 1980, "convoy", { titulo: "convoy" }],
      // (El reto, unos 10 s a la velocidad de aqui: 200 m.)
      [1980, 2180, "mixto", { densidad: 0.5, momento: "reto", titulo: "reto" }],
      [2180, 2270, "sprint", { titulo: "sprint_trump" }],
    ],
    control: 712, caja: 1450,
    // (La del autobus, despues del convoy: dentro chocaba con los camiones.)
    chapas: [[560, "arco"], [1700, "carril"], [2030, "bus"]],
    hitos: ["piramide", "castillo", "torre_eiffel", "fuentes", "cesar", "noria", "campanile"],
    meta: "hotel_trump", metaNombre: { es: "el hotel Trump", en: "Trump Hotel" }, coche: "patrulla",
    // Subiendo por el Strip hacia el norte desde el cartel de bienvenida: el
    // oeste queda a la izquierda. Los casinos en su orden de verdad.
    izquierda: [
      40, ["cartel_vegas", 1], 30, ["piramide", 1], ["kit", 1], 14, ...cuadras(1), ["kit", 2], ["castillo", 1], 14,
      ...cuadras(3), ["fuentes", 1], ["kit", 1], 14,
      ...cuadras(5), ["cesar", 1], ["kit", 2], 14,
      ...cuadras(7), ["kit", 2],
    ],
    derecha: [
      40, ["kit", 3], 14, ...cuadras(4), ["torre_eiffel", 1], ["kit", 2], 14,
      ...cuadras(6), ["noria", 1], ["kit", 2], 14,
      ...cuadras(3), ["campanile", 1], ["kit", 2], 14,
      ...cuadras(4), ["kit", 2],
    ],
    // Al fondo, la torre dorada con la alfombra roja hasta la acera.
    fondo: [{ pieza: "hotel_trump", d: 2352, centro: true },
      { pieza: "casino_entrada", d: 380, cruza: true },
      ...[388, 418, 448, 478, 508].map((d) => ({ pieza: "casino_sala", d, cruza: true })),
      { pieza: "casino_salida", d: 538, cruza: true }],
    interior: { rango: [380, 546], tipo: "casino" },
    final: "parada", parada: 11,
    // Para el final: mas abajo y mirando hacia arriba, que se vea la torre.
    camaraFinal: { pos: [3.0, 2.3, 19], mira: [0, 9, -12] },
    acera: ["phoenix/palmera", "ciudad/farola_ciudad"],
    extras: ["noria_rueda"],
  },
  {
    // 01/11/2026: nivel 5, el caucus de Iowa. Isidro eligio final en el
    // Capitolio dorado, mañana de invierno (el caucus es en enero) y cuatro
    // tramos: montañas de soja, cerdos sueltos, cosechadoras y la cola del caucus.
    id: "des_moines", nombre: "Locust Street", lugar: "Des Moines, Iowa", listo: true,
    zona: "city", carpeta: "des_moines", luz: "invierno", semilla: 1846,
    largo: 2600, linea: 11.5, velMax: 23,
    potenciadores: ["magnet", "shield", "boost", "mega", "botas"],
    // Centro de oficinas hasta el rio y, despues, el East Village de ladrillo.
    kit: { minPlantas: 4, maxPlantas: 13, nieve: true },
    horizonte: "iowa",
    // 06/11: Isidro: «se hacen repetitivos los obstaculos, faltan mas tipos y mas
    // dinamismo». Nuevos: la bola de nieve que viene rodando, el niño en trineo (cruza), la rama
    // nevada con el jilguero, el autobus escolar (cambia de carril) y el ciervo (cruza).
    obstaculos: { low: ["sacos_soja", "monton_nieve", "urna", "bola_nieve", "trineo"], high: ["sinfin", "pancarta_caucus", "rama_nevada"],
      full: ["quitanieves", "monton_soja", "munieco_nieve", "votantes", "furgoneta", "bus_escolar", "ciervo"] },
    publico: { personas: ["granjero", "abuelo", "senora", "granjero", "fan", "chico"], valla: "banderas", cada: 2 },
    // 05/11: Isidro: «los primeros niveles deben ser mas cortos y luego ir
    // alargandose» y «los niveles se siguen sintiendo muy iguales». Antes los
    // seis median 3,2 km y seguian el mismo orden casi en los mismos metros.
    // Des Moines: 2.600 m. La soja y los cerdos primero, el caucus y luego el dragon.
    tramos: [
      [0, 70, "calma", { titulo: "locust" }],
      [70, 280, "soja", { titulo: "soja" }],
      // 06/11 (3): Isidro: «más cosas, muchas más, que no sea tan repetitivo».
      // Un momento cada 20 s más o menos (ver «Los momentos» en world.js); el
      // largo del nivel no cambia.
      [280, 440, "convoy", { titulo: "convoy" }],
      // 08/11: el momento estrella: la Feria del Estado de Iowa (en lugar de los
      // cerdos y del tractor). La feria, en `fondo`.
      [440, 760, "feria", { titulo: "feria" }],
      [760, 830, "calma"],
      [830, 1000, "cosechadoras", { momento: "persigue", perseguidor: "cosechadora", titulo: "persigue_cosechadora" }],
      [1000, 1150, "lluvia", { titulo: "lluvia" }],
      [1150, 1250, "festin", { potenciador: "boost", titulo: "festin" }],
      [1250, 1500, "caucus", { momento: "reto", titulo: "reto" }],
      [1500, 1580, "calma"],
      // 03/11: el dragon de China viene a por la soja.
      [1580, 2150, "jefe", { jefe: "dragon", titulo: "dragon" }],
      [2150, 2300, "desfile_cruza", { cruzan: ["ciervo"], titulo: "cruzan_ciervos" }],
      [2300, 2440, "mixto", { densidad: 0.55, momento: "gorras", titulo: "gorras" }],
      [2440, 2570, "sprint", { titulo: "sprint_capitolio" }],
    ],
    control: 1512, caja: 1200,
    // 08/11: en la feria no hay edificios: los puestos, las carpas y la noria.
    sinEdificios: [440, 776],
    // (La primera, despues del convoy: dentro chocaba con los camiones.)
    chapas: [[460, "arco"], [1050, "carril"], [2300, "arco"]],
    hitos: ["parque_esculturas", "hotel_fort", "biblioteca_dm", "ruan", "torre_801", "world_food", "rio"],
    meta: "capitolio_iowa", metaNombre: { es: "el Capitolio", en: "the Capitol" },
    // El helicoptero de la tele, despues del rio: por el centro pasan las
    // pasarelas por encima de la calle y lo atravesarian.
    helicoptero: [1602, 2092],
    // Bajando por Locust Street hacia el este, hasta el Capitolio: el norte
    // queda a la izquierda. Despues del puente, el East Village.
    izquierda: [
      40, ["kit", 2], 14, ["parque_esculturas", 1], 14,
      ...cuadras(2), ["biblioteca_dm", 1], ["kit", 2], 14,
      ...cuadras(3), ["torre_801", 1], ["kit", 2], 14,
      ...cuadras(5), ["arena", 1], 48,
      ...cuadrasCon(9, EV),
    ],
    derecha: [
      // (11/11: el Ruan, antes del tramo sin edificios: no salía)
      40, ["kit", 3], 14, ...cuadras(1), ["hotel_fort", 1], ["kit", 2], 14,
      ["ruan", 1], ["kit", 2], 14,
      ...cuadras(9), ["kit", 1], ["world_food", 1], 68,
      ...cuadrasCon(8, EV), ["kit", 1, EV],
    ],
    // Las pasarelas acristaladas, el puente sobre el rio y el Capitolio al fondo.
    fondo: [
      { pieza: "skywalk", d: 365, cruza: true }, { pieza: "skywalk", d: 640, cruza: true },
      { pieza: "feria_entrada", d: 440, cruza: true },
      ...Array.from({ length: 10 }, (_, i) => ({ pieza: i % 2 ? "feria_puestos_b" : "feria_puestos", d: 444 + i * 30, cruza: true })),
      { pieza: "feria_noria", d: 600, cruza: true },
      { pieza: "skywalk", d: 1180, cruza: true }, { pieza: "skywalk", d: 1420, cruza: true },
      { pieza: "rio", d: 1557, cruza: true },
      { pieza: "capitolio_iowa", d: 2650, centro: true },
    ],
    final: "parada", parada: 4,
    // Para el final: abajo, al pie de la escalinata, mirando la cupula de oro.
    camaraFinal: { pos: [3, 3.2, 30], mira: [0, 17, -24] },
    acera: ["des_moines/arbol_nieve", "ciudad/farola_ciudad"],
  },
  {
    // 08/11/2026: Isidro: «haz más mapas, todos los que puedas, con sus
    // escenarios, obstáculos y su dinamismo». Nivel 6: Omaha (blender/omaha.py).
    // Eligió final en Union Station (art déco) y atardecer en la pradera. Tierra
    // de vacas: cajas de Filetes Trump por la calle y la estampida en los
    // corrales (el momento estrella).
    id: "omaha", nombre: "Farnam Street", lugar: "Omaha, Nebraska", listo: true,
    zona: "city", carpeta: "omaha", luz: "pradera", semilla: 1854,
    largo: 2700, linea: 11.5, velMax: 23,
    potenciadores: ["magnet", "shield", "boost", "mega", "botas"],
    kit: { minPlantas: 3, maxPlantas: 8, estilo: "omaha" },
    horizonte: "iowa",
    obstaculos: { low: ["caja_filetes", "rodillo_heno", "paca", "calabazas"], high: ["cartel_steak", "guirnalda", "bandera_grande"],
      full: ["camion_ganado", "fan_huskers", "vaca", "carruaje", "furgoneta", "tractor"] },
    publico: { personas: ["granjero", "fan", "abuelo", "senora", "chico", "granjero"], valla: "banderas", cada: 2 },
    tramos: [
      [0, 70, "calma", { titulo: "omaha" }],
      [70, 300, "vallas", { low: ["caja_filetes", "caja_filetes", "paca"], high: ["cartel_steak"], titulo: "filetes" }],
      [300, 440, "rampa", { titulo: "rampa" }],
      // El momento estrella: la estampida en los corrales de ganado.
      [440, 790, "corrales", { momento: "persigue", perseguidor: "vaca", titulo: "corrales" }],
      [790, 860, "calma"],
      [860, 1010, "premios", { titulo: "premios" }],
      [1010, 1180, "slalom", { full: ["camion_ganado", "camion_ganado", "carruaje"], titulo: "camiones_ganado" }],
      [1180, 1330, "lluvia", { titulo: "lluvia" }],
      [1330, 1530, "vallas", { low: ["caja_filetes", "rodillo_heno"], high: ["cartel_steak"], momento: "gorras", titulo: "gorras" }],
      [1530, 1690, "mixto", { densidad: 0.55, momento: "vehiculo", vehiculo: "carruaje", titulo: "sube_carruaje" }],
      [1690, 1830, "jefe_paso", { titulo: "jefe_paso" }],
      [1830, 1990, "convoy", { titulo: "convoy" }],
      [1990, 2140, "desfile_cruza", { cruzan: ["fan_huskers"], titulo: "cruzan_huskers" }],
      [2140, 2350, "mixto", { densidad: 0.5, momento: "reto", titulo: "reto" }],
      [2350, 2500, "alfombra", { titulo: "alfombra" }],
      [2500, 2650, "sprint", { titulo: "sprint_omaha" }],
    ],
    control: 1312, caja: 1100,
    // En los corrales no hay edificios: las vallas, las vacas y el granero.
    // (11/11: y el final despejado, como en los demas niveles con parada)
    sinEdificios: [[440, 806], [2690, 3800]],
    chapas: [[620, "arco"], [1250, "carril"], [2180, "bus"]],
    hitos: ["first_national", "woodmen", "old_market", "orpheum"],
    meta: "union_station", metaNombre: { es: "Union Station", en: "Union Station" },
    // Bajando por Farnam Street hacia la estación.
    izquierda: [
      40, ["kit", 3], 14, ["first_national", 1], ["kit", 2], 14, ...cuadras(4),
      ...cuadras(5), ["old_market", 1], ["kit", 2], 14, ...cuadras(14),
    ],
    derecha: [
      40, ["kit", 2], 14, ...cuadras(1), ["woodmen", 1], ["kit", 2], 14, ...cuadras(9),
      ["orpheum", 1], ["kit", 2], 14, ...cuadras(14),
    ],
    fondo: [{ pieza: "union_station", d: 2760, centro: true },
      { pieza: "corrales_entrada", d: 440, cruza: true },
      ...Array.from({ length: 12 }, (_, i) => ({ pieza: "corrales", d: 444 + i * 30, cruza: true }))],
    final: "parada", parada: 6,
    camaraFinal: { pos: [3, 3.2, 30], mira: [0, 10, -20] },
    // 08/11 (2): mas cosas en la acera y distintas en cada ciudad.
    acera: ["ciudad/arbol_ciudad", "ciudad/farola_ciudad", "ciudad/banco", "ciudad/arbol_ciudad", "ciudad/farola_ciudad", "ciudad/buzon"],
  },
  {
    // 08/11/2026: nivel 7: Wichita (blender/wichita.py). Eligió final en el
    // Guardián de las Llanuras y cielo de tornado. Historia: un tornado como el
    // de El Mago de Oz se lleva las vallas. Momento estrella: el tornado pasa
    // junto a la calle; y el camino de baldosas amarillas.
    id: "wichita", nombre: "Douglas Avenue", lugar: "Wichita, Kansas", listo: true,
    zona: "city", carpeta: "wichita", luz: "tornado", semilla: 1870,
    largo: 2800, linea: 11.5, velMax: 23.5,
    potenciadores: ["magnet", "shield", "boost", "mega", "botas"],
    kit: { minPlantas: 2, maxPlantas: 7, estilo: "wichita" },
    horizonte: "kansas",
    obstaculos: { low: ["tejado_volando", "paca", "calabazas"], high: ["valla_volando", "vaca_volando", "guirnalda"],
      full: ["espantapajaros", "bruja_bici", "tractor", "furgoneta", "vaca"] },
    publico: { personas: ["granjero", "abuelo", "senora", "fan", "chico", "granjero"], valla: "banderas", cada: 2 },
    tramos: [
      [0, 70, "calma", { titulo: "wichita" }],
      [70, 300, "mixto", { densidad: 0.5, titulo: "viento_ks" }],
      [300, 450, "rampa", { titulo: "rampa" }],
      [450, 620, "baldosas", { titulo: "baldosas" }],
      [620, 700, "calma"],
      // El momento estrella: el tornado pasa junto a la calle.
      [700, 1000, "tornado", { titulo: "tornado" }],
      [1000, 1150, "premios", { titulo: "premios" }],
      [1150, 1330, "slalom", { full: ["bruja_bici", "bruja_bici", "tractor"], titulo: "gulch" }],
      [1330, 1480, "lluvia", { titulo: "lluvia" }],
      [1480, 1680, "vallas", { low: ["tejado_volando", "paca"], high: ["valla_volando"], momento: "gorras", titulo: "gorras" }],
      [1680, 1840, "mixto", { densidad: 0.55, momento: "vehiculo", vehiculo: "tractor", titulo: "sube_tractor" }],
      [1840, 1990, "jefe_paso", { titulo: "jefe_paso" }],
      [1990, 2150, "convoy", { titulo: "convoy" }],
      [2150, 2300, "desfile_cruza", { cruzan: ["valla_volando", "vaca_volando"], titulo: "vuelan" }],
      [2300, 2510, "mixto", { densidad: 0.5, momento: "reto", titulo: "reto" }],
      [2510, 2640, "alfombra", { titulo: "alfombra" }],
      [2640, 2760, "sprint", { titulo: "sprint_wichita" }],
    ],
    control: 1412, caja: 1100,
    // En el tornado se sale a la pradera: sin edificios, para que se vea el embudo.
    sinEdificios: [[700, 1010], [2790, 3800]],
    chapas: [[560, "arco"], [1260, "carril"], [2400, "bus"]],
    hitos: ["epic_center", "museo_aviacion", "century_ii"],
    meta: "guardian_llanuras", metaNombre: { es: "el Guardián de las Llanuras", en: "the Keeper of the Plains" },
    izquierda: [
      40, ["kit", 3], 14, ["epic_center", 1], ["kit", 2], 14, ...cuadras(10),
      ["museo_aviacion", 1], ["kit", 2], 14, ...cuadras(14),
    ],
    derecha: [
      40, ["kit", 2], 14, ...cuadras(4), ["century_ii", 1], ["kit", 2], 14, ...cuadras(20),
    ],
    fondo: [{ pieza: "guardian_llanuras", d: 2860, centro: true },
      // El tornado, a la derecha y lejos (gira despacio).
      { pieza: "tornado_embudo", d: 860, cruza: true, x: 30 }],
    final: "parada", parada: 4,
    camaraFinal: { pos: [3, 3.0, 28], mira: [0, 12, -24] },
    // 08/11 (2): mas cosas en la acera y distintas en cada ciudad.
    acera: ["ciudad/arbol_ciudad", "findlay/farola_bandera", "ciudad/banco", "ciudad/arbol_ciudad", "findlay/farola_bandera", "ciudad/hidrante"],
  },
  {
    // 08/11/2026: nivel 8: San Luis (blender/sanluis.py). Isidro: «Aplica todas
    // las preguntas que digas recomendados»: final bajo el arco Gateway y mañana
    // soleada. Historia: las etiquetas de precio no paran de crecer (los
    // aranceles). Momento estrella: el súper de los aranceles, por dentro.
    id: "san_luis", nombre: "Market Street", lugar: "San Luis, Misuri", listo: true,
    zona: "city", carpeta: "san_luis", luz: "manana", semilla: 1764,
    largo: 2900, linea: 11.5, velMax: 23.5,
    potenciadores: ["magnet", "shield", "boost", "mega", "botas"],
    kit: { minPlantas: 4, maxPlantas: 12, estilo: "san_luis" },
    horizonte: "ohio",
    obstaculos: { low: ["caja_precio", "carrito_compra", "basura", "conos"], high: ["etiqueta_precio", "andamio", "semaforo"],
      full: ["carro_clydesdale", "fan_cardinals", "taxi", "furgoneta", "contenedor"] },
    publico: { personas: ["ejecutivo", "fan", "turista", "senora", "chico", "abuelo"], valla: "banderas", cada: 2 },
    tramos: [
      [0, 70, "calma", { titulo: "san_luis" }],
      [70, 300, "vallas", { low: ["caja_precio", "carrito_compra"], high: ["etiqueta_precio"], titulo: "precios" }],
      [300, 450, "rampa", { titulo: "rampa" }],
      // El momento estrella: el súper de los aranceles (el súper, en `fondo`).
      [450, 800, "super", { titulo: "super" }],
      [800, 870, "calma"],
      [870, 1020, "premios", { titulo: "premios" }],
      [1020, 1200, "slalom", { full: ["carro_clydesdale", "carro_clydesdale", "taxi"], titulo: "clydesdales" }],
      [1200, 1350, "lluvia", { titulo: "lluvia" }],
      [1350, 1550, "vallas", { low: ["caja_precio", "carrito_compra"], high: ["etiqueta_precio"], momento: "gorras", titulo: "gorras" }],
      [1550, 1710, "mixto", { densidad: 0.55, momento: "vehiculo", vehiculo: "carro_clydesdale", titulo: "sube_clydesdale" }],
      [1710, 1850, "jefe_paso", { titulo: "jefe_paso" }],
      [1850, 2010, "convoy", { titulo: "convoy" }],
      [2010, 2160, "desfile_cruza", { cruzan: ["fan_cardinals"], titulo: "cruzan_cardinals" }],
      [2160, 2370, "mixto", { densidad: 0.5, momento: "reto", titulo: "reto" }],
      [2370, 2520, "alfombra", { titulo: "alfombra" }],
      [2520, 2700, "mixto", { densidad: 0.55, titulo: "" }],
      [2700, 2860, "sprint", { titulo: "sprint_arco" }],
    ],
    control: 1312, caja: 1100,
    // (08/11 (2): el super ocupa la manzana entera: sin edificios a los lados.
    // Acaba en 796, donde acaba su salida: antes quedaban 4 m sin suelo.)
    interior: { rango: [450, 796], tipo: "super", sinEdificios: [440, 806] },
    extras: ["super_puerta"],
    chapas: [[620, "arco"], [1250, "carril"], [2250, "bus"]],
    hitos: ["old_courthouse", "busch_stadium", "union_station_stl"],
    meta: "arco_gateway", metaNombre: { es: "el arco Gateway", en: "the Gateway Arch" },
    izquierda: [
      40, ["kit", 3], 14, ["old_courthouse", 1], ["kit", 2], 14, ...cuadras(8),
      ["union_station_stl", 1], ["kit", 2], 14, ...cuadras(17),
    ],
    derecha: [
      40, ["kit", 2], 14, ...cuadras(1), ["busch_stadium", 1], ["kit", 2], 14, ...cuadras(28),
    ],
    fondo: [{ pieza: "arco_gateway", d: 2950, centro: true },
      { pieza: "super_entrada", d: 450, cruza: true },
      ...Array.from({ length: 11 }, (_, i) => ({ pieza: "super_pasillo", d: 458 + i * 30, cruza: true })),
      { pieza: "super_salida", d: 788, cruza: true }],
    // Se para en el paseo, a 30 m del arco, y la camara mira hacia arriba (el
    // arco entero no cabe en el movil en vertical: se ve la curva de arriba).
    final: "parada", parada: 18,
    camaraFinal: { pos: [0, 3.0, 18], mira: [0, 22, -40] },
    // Al final, el parque junto al rio: sin edificios.
    sinEdificios: [2880, 3800],
    // 08/11 (2): mas cosas en la acera y distintas en cada ciudad.
    acera: ["ciudad/arbol_ciudad", "ciudad/farola_ciudad", "ciudad/hidrante", "ciudad/arbol_ciudad", "ciudad/farola_ciudad", "ciudad/banco"],
  },
  {
    // 08/11/2026: nivel 9: Indianápolis (blender/indy.py). Isidro: «Aplica todas
    // las preguntas que digas recomendados»: final en la meta del circuito y luz
    // de dia de carrera. Historia: «Los coches de carreras no esperan a nadie».
    // Momento estrella: la recta de las 500 millas, entre gradas, adelantando a
    // los coches de carreras, hasta la franja de ladrillos de la meta.
    id: "indianapolis", nombre: "Meridian Street", lugar: "Indianápolis, Indiana", listo: true,
    zona: "city", carpeta: "indianapolis", luz: "mediodia", semilla: 1911,
    largo: 2900, linea: 11.5, velMax: 24,
    potenciadores: ["magnet", "shield", "boost", "mega", "botas"],
    kit: { minPlantas: 4, maxPlantas: 14, estilo: "indy" },
    horizonte: "ohio",
    obstaculos: { low: ["pila_neumaticos", "conos", "basura"], high: ["bandera_cuadros", "andamio", "semaforo"],
      full: ["coche_seguridad", "taxi", "furgoneta", "contenedor"] },
    publico: { personas: ["fan", "turista", "ejecutivo", "senora", "chico", "abuelo"], valla: "banderas", cada: 2 },
    tramos: [
      [0, 70, "calma", { titulo: "indianapolis" }],
      [70, 300, "vallas", { low: ["pila_neumaticos", "conos"], high: ["bandera_cuadros"], titulo: "boxes" }],
      [300, 450, "rampa", { titulo: "rampa" }],
      [450, 610, "desfile_cruza", { cruzan: ["pit_crew"], titulo: "cruzan_mecanicos" }],
      [610, 680, "calma"],
      [680, 830, "premios", { titulo: "premios" }],
      [830, 1010, "slalom", { full: ["coche_seguridad", "coche_seguridad", "taxi"], titulo: "pace_car" }],
      [1010, 1160, "lluvia", { titulo: "lluvia" }],
      [1160, 1360, "vallas", { low: ["pila_neumaticos", "conos"], high: ["bandera_cuadros"], momento: "gorras", titulo: "gorras" }],
      [1360, 1520, "mixto", { densidad: 0.55, momento: "vehiculo", vehiculo: "descapotable", titulo: "sube_descapotable" }],
      [1520, 1660, "jefe_paso", { titulo: "jefe_paso" }],
      [1660, 1820, "convoy", { titulo: "convoy" }],
      [1820, 2020, "mixto", { densidad: 0.5, momento: "reto", titulo: "reto" }],
      [2020, 2170, "alfombra", { titulo: "alfombra" }],
      [2170, 2330, "mixto", { densidad: 0.55, titulo: "" }],
      // El momento estrella: la recta del circuito (las gradas, en `fondo`).
      [2330, 2730, "circuito", { titulo: "circuito" }],
      [2730, 2880, "sprint", { titulo: "sprint_meta" }],
    ],
    control: 1290, caja: 1100,
    // Al aire libre: se ve el horizonte y la luz es la de fuera (solo se quita
    // la calle, la acera y los edificios).
    interior: { rango: [2340, 2990], tipo: "circuito", aire: true, sinEdificios: [2320, 3800] },
    chapas: [[640, "arco"], [1250, "carril"], [2250, "bus"]],
    hitos: ["soldiers_monument", "statehouse_in", "lucas_oil", "jw_marriott"],
    meta: "meta_indy", metaNombre: { es: "la meta de las 500 millas", en: "the Indy 500 finish line" },
    izquierda: [
      40, ["kit", 3], 14, ["soldiers_monument", 1], ["kit", 2], 14, ...cuadras(9),
      ["lucas_oil", 1], ["kit", 2], 14, ...cuadras(16),
    ],
    derecha: [
      40, ["kit", 2], 14, ...cuadras(1), ["statehouse_in", 1], ["kit", 2], 14, ...cuadras(6),
      ["jw_marriott", 1], ["kit", 2], 14, ...cuadras(19),
    ],
    // (Las piezas que cruzan empiezan en `d`. 08/11 (2): el muro del circuito
    // en 2336 y el tunel por debajo de las gradas hasta 2370 (su suelo empieza
    // en 2340, donde se quita la calle); despues las gradas hasta la meta, sin
    // huecos ni suelos encima de otros.)
    fondo: [{ pieza: "meta_indy", d: 2910, centro: true },
      { pieza: "circuito_entrada", d: 2336, cruza: true },
      ...Array.from({ length: 18 }, (_, i) => ({ pieza: "grada", d: 2370 + i * 30, cruza: true }))],
    // Se para encima de la franja de ladrillos, y la camara mira la Pagoda.
    final: "parada", parada: -0.5,
    camaraFinal: { pos: [2.4, 2.8, 10], mira: [-9, 9, -16] },
    // 08/11 (2): mas cosas en la acera y distintas en cada ciudad.
    acera: ["ciudad/farola_ciudad", "ciudad/arbol_ciudad", "findlay/farola_bandera", "ciudad/banco", "ciudad/arbol_ciudad", "ciudad/buzon"],
  },
  {
    // 08/11/2026: nivel 10: Detroit (blender/detroit.py). Se aplico lo
    // recomendado: final delante del Renaissance Center y luz de tarde.
    // Historia: «La ciudad del motor, con coches llenos de aranceles. En el
    // puente, canadienses enfadados: no quieren ser el estado 51». Momento
    // estrella: el puente Ambassador a Canada, con el rio muy abajo.
    id: "detroit", nombre: "Woodward Avenue", lugar: "Detroit, Míchigan", listo: true,
    zona: "city", carpeta: "detroit", luz: "tarde", semilla: 1701,
    largo: 2950, linea: 11.5, velMax: 24,
    potenciadores: ["magnet", "shield", "boost", "mega", "botas"],
    kit: { minPlantas: 4, maxPlantas: 14, estilo: "detroit" },
    horizonte: "ohio",
    obstaculos: { low: ["pila_neumaticos", "conos", "basura"], high: ["pancarta_canada", "andamio", "semaforo"],
      full: ["coche_arancel", "taxi", "furgoneta", "contenedor"] },
    publico: { personas: ["ejecutivo", "fan", "turista", "senora", "chico", "abuelo"], valla: "banderas", cada: 2 },
    tramos: [
      [0, 70, "calma", { titulo: "detroit" }],
      [70, 300, "vallas", { low: ["pila_neumaticos", "conos"], high: ["andamio"], titulo: "motor" }],
      [300, 450, "rampa", { titulo: "rampa" }],
      [450, 620, "slalom", { full: ["coche_arancel", "coche_arancel", "taxi"], titulo: "coches_arancel" }],
      [620, 700, "calma"],
      // El momento estrella: el puente Ambassador (tramos y torres, en `fondo`).
      [700, 1070, "puente_canada", { titulo: "puente_canada" }],
      [1070, 1140, "calma"],
      [1140, 1290, "premios", { titulo: "premios" }],
      [1290, 1440, "lluvia", { titulo: "lluvia" }],
      [1440, 1640, "vallas", { low: ["pila_neumaticos", "conos"], high: ["pancarta_canada"], momento: "gorras", titulo: "gorras" }],
      [1640, 1800, "mixto", { densidad: 0.55, momento: "vehiculo", vehiculo: "limusina", titulo: "sube_limusina" }],
      [1800, 1940, "jefe_paso", { titulo: "jefe_paso" }],
      [1940, 2100, "convoy", { titulo: "convoy" }],
      [2100, 2260, "desfile_cruza", { cruzan: ["canadiense", "alce"], titulo: "cruzan_canadienses" }],
      [2260, 2460, "mixto", { densidad: 0.5, momento: "reto", titulo: "reto" }],
      [2460, 2610, "alfombra", { titulo: "alfombra" }],
      [2610, 2790, "mixto", { densidad: 0.55, titulo: "" }],
      [2790, 2940, "sprint", { titulo: "sprint_rencen" }],
    ],
    control: 1300, caja: 1160,
    // El puente va al aire libre: se quita la calle (y el suelo: abajo, el rio).
    interior: { rango: [705, 1065], tipo: "puente", aire: true, sinEdificios: true },
    sinEdificios: [2860, 3800],
    chapas: [[1200, "arco"], [1700, "carril"], [2300, "bus"]],
    hitos: ["spirit_detroit", "fox_theatre", "puno_joe_louis", "guardian_building"],
    meta: "ren_cen", metaNombre: { es: "el Renaissance Center", en: "the Renaissance Center" },
    izquierda: [
      40, ["kit", 3], 14, ["spirit_detroit", 1], ["kit", 2], 14, ...cuadras(10),
      ["guardian_building", 1], ["kit", 2], 14, ...cuadras(17),
    ],
    derecha: [
      // (11/11: el puño, antes del puente: no salía)
      40, ["kit", 2], 14, ["fox_theatre", 1], ["kit", 2], 14, ...cuadras(2),
      ["puno_joe_louis", 1], ["kit", 2], 14, ...cuadras(27),
    ],
    // Las piezas que cruzan empiezan en `d`: 12 tramos de 705 a 1065 (la
    // segunda mitad, los de la primera dados la vuelta) y una torre en cada punta.
    fondo: [{ pieza: "ren_cen", d: 3000, centro: true },
      ...Array.from({ length: 12 }, (_, i) => ({ pieza: "puente_amb_" + (i < 6 ? i : 11 - i), d: 705 + i * 30, cruza: true, giro: i >= 6 })),
      { pieza: "torre_ambassador", d: 703, cruza: true },
      { pieza: "torre_ambassador", d: 1063, cruza: true }],
    // Se para al pie de la escalinata, y la camara mira hacia arriba.
    final: "parada", parada: 14,
    camaraFinal: { pos: [5, 3.2, 21], mira: [0, 24, -40] },
    // 08/11 (2): mas cosas en la acera y distintas en cada ciudad.
    acera: ["ciudad/farola_ciudad", "ciudad/arbol_ciudad", "ciudad/buzon", "ciudad/farola_ciudad", "ciudad/arbol_ciudad", "ciudad/hidrante"],
  },
  {
    // 08/11/2026: nivel 11: Chicago (blender/chicago.py). Se aplico lo
    // recomendado: final delante de la Alubia (Cloud Gate, en Millennium
    // Park) y mañana de otoño con viento. Historia: «La ciudad del viento: el
    // viento le levanta el tupe». Momento estrella: la ciudad del viento
    // (paraguas que cruzan volando, periodicos, papeleras rodando, el tupe
    // levantado y un paraguas que te lleva por el aire).
    id: "chicago", nombre: "Michigan Avenue", lugar: "Chicago, Illinois", listo: true,
    zona: "city", carpeta: "chicago", luz: "otono", semilla: 1801,
    largo: 3000, linea: 11.5, velMax: 24,
    potenciadores: ["magnet", "shield", "boost", "mega", "botas"],
    kit: { minPlantas: 5, maxPlantas: 16, estilo: "chicago" },
    horizonte: "chicago",
    obstaculos: { low: ["cajas_pizza", "conos", "basura"], high: ["periodicos", "andamio", "semaforo"],
      full: ["carrito_perritos", "taxi", "furgoneta", "contenedor"] },
    publico: { personas: ["ejecutivo", "fan", "turista", "senora", "chico", "abuelo"], valla: "banderas", cada: 2 },
    tramos: [
      [0, 70, "calma", { titulo: "chicago" }],
      [70, 280, "vallas", { low: ["cajas_pizza", "conos"], high: ["periodicos"], titulo: "milla" }],
      [280, 430, "rampa", { titulo: "rampa" }],
      [430, 600, "slalom", { full: ["carrito_perritos", "taxi", "carrito_perritos"], titulo: "perritos" }],
      [600, 690, "calma"],
      // El puente DuSable sobre el rio verde (pieza de `fondo` e `interior`).
      [690, 800, "mixto", { densidad: 0.35, titulo: "rio_verde" }],
      [800, 870, "calma"],
      [870, 1030, "premios", { titulo: "premios" }],
      [1030, 1190, "desfile_cruza", { cruzan: ["segway"], titulo: "cruzan_segways" }],
      [1190, 1380, "vallas", { low: ["cajas_pizza", "conos"], high: ["periodicos"], momento: "gorras", titulo: "gorras" }],
      [1380, 1450, "calma"],
      // El momento estrella: la ciudad del viento.
      [1450, 1880, "viento", { titulo: "viento" }],
      [1880, 1950, "calma"],
      [1950, 2110, "jefe_paso", { titulo: "jefe_paso" }],
      [2110, 2270, "convoy", { titulo: "convoy" }],
      [2270, 2430, "mixto", { densidad: 0.55, momento: "vehiculo", vehiculo: "limusina", titulo: "sube_limusina" }],
      [2430, 2610, "mixto", { densidad: 0.5, momento: "reto", titulo: "reto" }],
      [2610, 2760, "alfombra", { titulo: "alfombra" }],
      [2760, 2850, "mixto", { densidad: 0.55, titulo: "" }],
      [2850, 2990, "sprint", { titulo: "sprint_alubia" }],
    ],
    control: 1400, caja: 900,
    // El puente DuSable: se quita la calle y el suelo (abajo, el rio).
    interior: { rango: [700, 760], tipo: "puente", aire: true, sinEdificios: [696, 764] },
    sinEdificios: [2900, 3800],
    chapas: [[950, "arco"], [1250, "carril"], [2500, "bus"]],
    hitos: ["hancock", "water_tower", "trump_chicago", "tribune_tower", "wrigley_building"],
    meta: "cloud_gate", metaNombre: { es: "la Alubia", en: "the Bean" },
    extras: ["barco", "alubia"],
    // Bajando por Michigan Avenue hacia el sur: el este (el lago) a la izquierda.
    // La Tribune Tower y el Wrigley Building, uno enfrente del otro, justo
    // antes del rio; y la torre Trump, junto al Wrigley (con su nombre).
    izquierda: [
      40, ["kit", 2], 14, ["hancock", 1], ["kit", 2], 14, ...cuadras(4), ["kit", 1], ["tribune_tower", 1], 88,
      ...cuadras(19),
    ],
    derecha: [
      40, ["kit", 3], 14, ["water_tower", 1], ["kit", 2], 14, ...cuadras(3), ["kit", 1], ["trump_chicago", 1], ["wrigley_building", 1], 78,
      ...cuadras(19),
    ],
    // El puente (de 700 a 760) y la meta al fondo.
    fondo: [{ pieza: "cloud_gate", d: 3050, centro: true },
      { pieza: "puente_dusable", d: 700, cruza: true }],
    final: "parada", parada: 14,
    // Se para al pie de la plaza: el delante saludando y la Alubia detras.
    camaraFinal: { pos: [3.5, 2.6, 10], mira: [0, 4.5, -30] },
    acera: ["ciudad/farola_ciudad", "ciudad/arbol_ciudad", "ciudad/buzon", "ciudad/farola_ciudad", "ciudad/arbol_ciudad", "ciudad/banco"],
  },
  {
    // 09/11/2026: nivel 12: Milwaukee (blender/milwaukee.py). Isidro: «sigue
    // creando mas estados, aplica tus propias recomendaciones». Se aplico lo
    // recomendado: final delante del museo de arte de Calatrava (las alas
    // blancas junto al lago, que se abren al llegar) y tarde dorada de otoño.
    // Historia: «Se sube a un camion de la basura con chaleco, como hizo de
    // verdad. Quesos». Momento estrella: el camion de la basura (se pone el
    // chaleco y va de pie encima, arrollando cubos y bolsas).
    id: "milwaukee", nombre: "Wisconsin Avenue", lugar: "Milwaukee, Wisconsin", listo: true,
    zona: "city", carpeta: "milwaukee", luz: "dorada", semilla: 1846,
    largo: 3050, linea: 11.5, velMax: 24.5,
    potenciadores: ["magnet", "shield", "boost", "mega", "botas"],
    kit: { minPlantas: 3, maxPlantas: 12, estilo: "milwaukee" },
    horizonte: "milwaukee",
    obstaculos: { low: ["cuna_queso", "bolsas_basura", "conos", "cubo_basura"], high: ["cartel_queso", "andamio", "semaforo"],
      full: ["moto_harley", "taxi", "furgoneta", "camion_basura"] },
    publico: { personas: ["fan", "turista", "ejecutivo", "senora", "granjero", "abuelo"], valla: "banderas", cada: 2 },
    tramos: [
      [0, 70, "calma", { titulo: "milwaukee" }],
      [70, 280, "vallas", { low: ["cuna_queso", "bolsas_basura"], high: ["cartel_queso"], titulo: "quesos" }],
      [280, 430, "rampa", { titulo: "rampa" }],
      [430, 600, "slalom", { full: ["moto_harley", "moto_harley", "taxi"], titulo: "motos" }],
      [600, 740, "calma"],
      // El puente sobre el rio Milwaukee (pieza de `fondo` e `interior`).
      [740, 830, "mixto", { densidad: 0.35, titulo: "rio_mke" }],
      [830, 900, "calma"],
      [900, 1060, "premios", { titulo: "premios" }],
      [1060, 1220, "desfile_cruza", { cruzan: ["fan_queso"], titulo: "cheeseheads" }],
      [1220, 1420, "vallas", { low: ["rueda_queso", "cuna_queso"], high: ["cartel_queso"], momento: "gorras", titulo: "gorras" }],
      [1420, 1490, "calma"],
      // El momento estrella: el camion de la basura.
      [1490, 1920, "basura", { momento: "vehiculo", vehiculo: "camion_basura", titulo: "basura" }],
      [1920, 1990, "calma"],
      [1990, 2150, "jefe_paso", { titulo: "jefe_paso" }],
      [2150, 2310, "convoy", { titulo: "convoy" }],
      [2310, 2470, "vallas", { low: ["rueda_queso", "cubo_basura"], high: ["cartel_queso"], titulo: "quesos_ruedan" }],
      [2470, 2650, "mixto", { densidad: 0.5, momento: "reto", titulo: "reto" }],
      [2650, 2800, "alfombra", { titulo: "alfombra" }],
      [2800, 2890, "mixto", { densidad: 0.55, titulo: "" }],
      [2890, 3040, "sprint", { titulo: "sprint_museo" }],
    ],
    control: 1450, caja: 950,
    // El puente sobre el rio: se quita la calle y el suelo (abajo, el rio).
    interior: { rango: [760, 810], tipo: "puente", aire: true, sinEdificios: [756, 814] },
    sinEdificios: [3065, 3900],
    chapas: [[1000, "arco"], [1300, "carril"], [2550, "bus"]],
    hitos: ["gesu_church", "germania", "pfister_hotel", "city_hall_mke", "us_bank_center"],
    meta: "museo_calatrava", metaNombre: { es: "el museo de las alas", en: "the winged museum" },
    extras: ["ala_museo"],
    // Por Wisconsin Avenue hacia el este (el lago al fondo): el norte a la
    // izquierda. El Gesu junto a Marquette, el Germania antes del rio; pasado
    // el rio, el Ayuntamiento, el Pfister y, ya cerca del lago, el U.S. Bank.
    izquierda: [
      40, ["kit", 2], 14, ["gesu_church", 1], ["kit", 2], 14, ...cuadras(3), ["kit", 1], ["germania", 1], 14,
      ["kit", 3], 14, ...cuadras(2), ["city_hall_mke", 1], 14, ...cuadras(20),
    ],
    derecha: [
      40, ["kit", 3], 14, ...cuadras(4), ["kit", 2], 14, ["kit", 3], 14, ...cuadras(1), ["kit", 2], ["pfister_hotel", 1], 14,
      ...cuadras(13), ["us_bank_center", 1], 14, ...cuadras(5),
    ],
    // El puente (de 760 a 810) y la meta al fondo.
    fondo: [{ pieza: "museo_calatrava", d: 3100, centro: true },
      { pieza: "puente_mke", d: 760, cruza: true }],
    final: "parada", parada: 14,
    // Se para al pie de la plaza: el delante saludando y las alas detras.
    camaraFinal: { pos: [4, 3.2, 10], mira: [0, 12, -90] },
    acera: ["ciudad/farola_ciudad", "ciudad/arbol_ciudad", "ciudad/banco", "ciudad/farola_ciudad", "ciudad/arbol_ciudad", "ciudad/hidrante"],
  },
  {
    // 09/11/2026: nivel 13: Minneapolis (blender/minneapolis.py). Isidro: «sigue
    // creando mas estados, aplica tus propias recomendaciones». Se aplico lo
    // recomendado: final en el jardin de esculturas (la cuchara gigante con la
    // cereza, nevado) y un dia de invierno de sol y mucho frio (luz `helada`).
    // Historia: «Lagos helados y pistas de hockey de los canadienses».
    // Momento estrella: el lago helado de Loring Park con tres pistas de hockey
    // (discos gigantes, canadienses patinando, casetas de pesca y el gol final).
    id: "minneapolis", nombre: "Nicollet Mall", lugar: "Minneapolis, Minnesota", listo: true,
    zona: "city", carpeta: "minneapolis", luz: "helada", semilla: 1867,
    largo: 3150, linea: 11.5, velMax: 25,
    potenciadores: ["magnet", "shield", "boost", "mega", "botas"],
    kit: { minPlantas: 4, maxPlantas: 14, estilo: "minneapolis", nieve: true },
    horizonte: "minneapolis",
    obstaculos: { low: ["monton_nieve", "porteria_hockey", "trineo"], high: ["pancarta_eh", "andamio", "semaforo"],
      full: ["quitanieves", "munieco_nieve", "taxi", "furgoneta", "pulidora_hielo"] },
    publico: { personas: ["fan", "turista", "ejecutivo", "senora", "abuelo", "chico"], valla: "banderas", cada: 2 },
    tramos: [
      [0, 70, "calma", { titulo: "minneapolis" }],
      [70, 280, "vallas", { low: ["monton_nieve", "porteria_hockey"], high: ["pancarta_eh"], titulo: "nieve_mpls" }],
      [280, 430, "rampa", { titulo: "rampa" }],
      [430, 600, "slalom", { full: ["quitanieves", "quitanieves", "taxi"], titulo: "quitanieves" }],
      [600, 740, "calma"],
      [740, 900, "desfile_cruza", { cruzan: ["jugador_hockey"], titulo: "canadienses" }],
      [900, 1060, "premios", { titulo: "premios" }],
      [1060, 1220, "vallas", { low: ["monton_nieve", "porteria_hockey"], high: ["pancarta_eh"], momento: "gorras", titulo: "gorras" }],
      [1220, 1290, "calma"],
      [1290, 1450, "jefe_paso", { titulo: "jefe_paso" }],
      [1450, 1610, "convoy", { titulo: "convoy" }],
      [1610, 1770, "mixto", { densidad: 0.5, momento: "reto", titulo: "reto" }],
      [1770, 1880, "calma"],
      // El momento estrella: el lago helado (pieza de `fondo` e `interior`).
      [1880, 2320, "hockey", { titulo: "lago_helado" }],
      [2320, 2400, "calma"],
      // (Los discos que se deslizan, solo en el lago: en las vallas llegaban a la
      // vez que una pancarta de agacharse y no habia forma de pasar.)
      [2400, 2560, "vallas", { low: ["porteria_hockey", "monton_nieve"], high: ["pancarta_eh"], titulo: "porterias" }],
      [2560, 2710, "alfombra", { titulo: "alfombra" }],
      [2710, 2990, "mixto", { densidad: 0.55, titulo: "" }],
      [2990, 3140, "sprint", { titulo: "sprint_cuchara" }],
    ],
    control: 1800, caja: 950,
    // El lago helado: se quita la calle y el suelo (el hielo lo pone la pieza).
    interior: { rango: [1882, 2318], tipo: "lago", aire: true, sinEdificios: [1868, 2332] },
    sinEdificios: [3165, 4000],
    chapas: [[1000, "arco"], [1150, "carril"], [2760, "bus"]],
    hitos: ["city_hall_mpls", "ids_center", "foshay_tower", "wells_fargo_mpls", "basilica_mary"],
    meta: "cuchara_cereza", metaNombre: { es: "la cuchara gigante", en: "the giant spoon" },
    // Por Nicollet Mall hacia el suroeste: el Ayuntamiento y la Foshay a la
    // izquierda; el IDS, el Wells Fargo y la basilica a la derecha; luego el
    // lago helado de Loring Park y, al fondo, el jardin de esculturas.
    izquierda: [
      40, ["kit", 2], 14, ["city_hall_mpls", 1], 14, ...cuadras(5), ["kit", 2], ["foshay_tower", 1], 14, ...cuadras(30),
    ],
    derecha: [
      40, ["kit", 3], 14, ...cuadras(3), ["kit", 2], ["ids_center", 1], 14, ...cuadras(5), ["wells_fargo_mpls", 1], 14,
      ...cuadras(3), ["kit", 3], ["basilica_mary", 1], 14, ...cuadras(20),
    ],
    fondo: [{ pieza: "cuchara_cereza", d: 3200, centro: true },
      { pieza: "lago_helado", d: 1880, cruza: true }],
    final: "parada", parada: 14,
    // Se para al pie del jardin: el delante saludando y la cuchara detras.
    camaraFinal: { pos: [4, 3.0, 10], mira: [0, 6, -60] },
    acera: ["des_moines/arbol_nieve", "ciudad/farola_ciudad", "ciudad/banco", "ciudad/farola_ciudad", "des_moines/arbol_nieve", "ciudad/hidrante"],
  },
  {
    // 12/11/2026: nivel 14: Monte Rushmore (blender/rushmore.py). Isidro:
    // «sigue creando mapas y que se sientan muy diferentes, con dinámicas
    // diferentes». Se aplicó lo recomendado: luz de mañana (las caras miran al
    // este) y final en la terraza bajo la montaña. Primero Rapid City, «la
    // ciudad de los presidentes»; luego las Black Hills por la Iron Mountain
    // Road (bosque, agujas de granito, túneles) y la Avenida de las Banderas.
    // Dinámicas propias: los bisontes que embisten si te pones en su carril,
    // los perritos de la pradera que asoman y se esconden, y el momento
    // estrella: las rocas que caen de la montaña con su sombra avisando.
    id: "rushmore", nombre: "Iron Mountain Road", lugar: "Monte Rushmore, Dakota del Sur", listo: true,
    zona: "town", carpeta: "rushmore", luz: "manana", semilla: 1927,
    largo: 3200, linea: 11.5, velMax: 25,
    potenciadores: ["magnet", "shield", "boost", "mega", "botas"],
    kit: { minPlantas: 2, maxPlantas: 5, estilo: "rapid" },
    horizonte: "rushmore",
    obstaculos: { low: ["roca_caida", "calavera", "paca"], high: ["cartel_no_caras", "cartel_ruta"],
      full: ["autocaravana", "moto_harley", "pickup", "vaquero"] },
    publico: { personas: ["turista", "fan", "abuelo", "chico", "senora"], valla: "banderas", cada: 3 },
    // En el bosque, ni publico ni farolas.
    sinPublico: [[700, 2880]], sinAcera: [[700, 3400]],
    tramos: [
      [0, 80, "calma", { titulo: "rushmore" }],
      [80, 300, "mixto", { densidad: 0.45, titulo: "ciudad_presidentes" }],
      [300, 450, "rampa", { titulo: "rampa" }],
      [450, 620, "slalom", { full: ["autocaravana", "moto_harley", "pickup"], titulo: "sturgis" }],
      [620, 700, "calma"],
      [700, 880, "premios", { titulo: "premios" }],
      [880, 960, "calma", { titulo: "black_hills" }],
      [960, 1300, "bisontes", { titulo: "bisontes" }],
      [1300, 1370, "calma"],
      [1370, 1530, "jefe_paso", { titulo: "jefe_paso" }],
      [1530, 1850, "perritos", { titulo: "perritos" }],
      [1850, 1920, "calma"],
      [1920, 2080, "mixto", { densidad: 0.5, momento: "reto", titulo: "reto" }],
      [2080, 2160, "calma"],
      // El momento estrella: la montaña tira rocas (su sombra avisa de donde caen).
      [2160, 2620, "rocas", { titulo: "rocas" }],
      [2620, 2700, "calma"],
      [2700, 2880, "bisontes", { titulo: "bisontes2" }],
      [2880, 3040, "alfombra", { titulo: "avenida_banderas" }],
      [3040, 3190, "sprint", { titulo: "sprint_rushmore" }],
    ],
    control: 1700, caja: 800,
    sinEdificios: [3150, 4000],
    chapas: [[760, "arco"], [1980, "carril"], [2950, "arco"]],
    hitos: ["hotel_alex_johnson", "dino_park", "wall_drug", "avenida_banderas"],
    meta: "monte_rushmore", metaNombre: { es: "el monte Rushmore", en: "Mount Rushmore" },
    // Por Main Street de Rapid City (el hotel y el cartel a la izquierda, el
    // dinosaurio en su colina a la derecha), luego el bosque y, al final, las
    // columnas con las banderas de los estados.
    izquierda: [
      40, ["kit", 2], 14, ["hotel_alex_johnson", 1], 14, ...cuadras(3), ["wall_drug", 1], 14, ...cuadras(2),
      ...bosque(33), ["avenida_banderas", 4],
    ],
    derecha: [
      40, ["kit", 3], 14, ...cuadras(1), ["dino_park", 1], 14, ...cuadras(4),
      ...bosque(34), ["avenida_banderas", 4],
    ],
    fondo: [{ pieza: "monte_rushmore", d: 3255, centro: true },
      ...[1100, 1880, 2740].map((d) => ({ pieza: "tunel_roca", d, cruza: true }))],
    final: "parada", parada: 22,
    // Se para en la terraza y la camara mira arriba, a las caras.
    camaraFinal: { pos: [-4, 3, 34], mira: [-10, 30, -33] },
    acera: ["rushmore/estatua_bronce", "ciudad/farola_ciudad", "ciudad/arbol_ciudad", "ciudad/farola_ciudad"],
  },
  {
    // 12/11/2026: nivel 15: Fargo (blender/fargo.py). Jefe: el Rey Pingüino
    // viene a cobrar el arancel de las islas de los pingüinos en plena
    // nevada. Recomendado: ventisca (luz `invierno`, nieve que cae) y final
    // ante el teatro de Fargo. Dinámicas propias: las placas de hielo (el
    // cambio de carril resbala), las rafagas de ventisca que te empujan de
    // carril (con aviso) y los pingüinos que cruzan deslizandose.
    id: "fargo", nombre: "Broadway", lugar: "Fargo, Dakota del Norte", listo: true,
    zona: "city", carpeta: "fargo", luz: "invierno", semilla: 1871,
    largo: 3250, linea: 11.5, velMax: 24,
    potenciadores: ["magnet", "shield", "boost", "mega", "botas"],
    kit: { minPlantas: 3, maxPlantas: 8, estilo: "fargo", nieve: true },
    horizonte: "fargo",
    obstaculos: { low: ["monton_nieve", "bloque_hielo", "trineo"], high: ["cartel_pinguino", "andamio"],
      full: ["quitanieves", "munieco_nieve", "caseta_pesca", "taxi"] },
    publico: { personas: ["granjero", "abuelo", "fan", "chico", "senora"], valla: "banderas", cada: 2 },
    tramos: [
      [0, 70, "calma", { titulo: "fargo" }],
      [70, 260, "vallas", { low: ["monton_nieve", "bloque_hielo"], high: ["cartel_pinguino"], titulo: "nieve_fargo" }],
      [260, 420, "hielo", { titulo: "placas_hielo" }],
      [420, 500, "calma"],
      [500, 680, "pinguinos", { titulo: "pinguinos" }],
      [680, 760, "calma"],
      [760, 1050, "ventisca", { titulo: "ventisca" }],
      [1050, 1130, "calma"],
      [1130, 1290, "premios", { titulo: "premios" }],
      [1290, 1450, "slalom", { full: ["quitanieves", "quitanieves", "caseta_pesca"], titulo: "quitanieves" }],
      [1450, 1530, "calma"],
      [1530, 2150, "jefe", { jefe: "pinguino", titulo: "rey_pinguino" }],
      [2150, 2230, "calma"],
      [2230, 2450, "hielo", { titulo: "hielo2" }],
      [2450, 2700, "ventisca", { titulo: "ventisca2" }],
      [2700, 2780, "calma"],
      [2780, 2950, "pinguinos", { titulo: "pinguinos2" }],
      [2950, 3100, "mixto", { densidad: 0.5, titulo: "" }],
      [3100, 3240, "sprint", { titulo: "sprint_fargo" }],
    ],
    control: 1500, caja: 1250,
    sinEdificios: [3220, 4000],
    chapas: [[1200, "arco"], [2960, "carril"], [3060, "arco"]],
    hitos: ["hotel_donaldson", "np_depot", "black_building", "radisson_fargo"],
    meta: "fargo_theatre", metaNombre: { es: "el teatro de Fargo", en: "the Fargo Theatre" },
    izquierda: [
      40, ["kit", 2], 14, ["hotel_donaldson", 1], 14, ...cuadras(4), ["kit", 2], ["black_building", 1], 14, ...cuadras(23),
    ],
    derecha: [
      40, ["kit", 3], 14, ...cuadras(2), ["np_depot", 1], 14, ...cuadras(6), ["radisson_fargo", 1], 14, ...cuadras(19),
    ],
    fondo: [{ pieza: "fargo_theatre", d: 3290, centro: true }],
    final: "parada", parada: 10,
    camaraFinal: { pos: [4, 2.8, 10], mira: [0, 8, -60] },
    acera: ["des_moines/arbol_nieve", "ciudad/farola_ciudad", "ciudad/banco", "ciudad/farola_ciudad"],
  },
  {
    // 12/11/2026: nivel 16: Houston (blender/houston.py). «La NASA. Tu examigo
    // Elon, enfadado tras la pelea, te persigue en cohete». Recomendado: tarde
    // de calor de Texas y final en Independence Plaza (el 747 con el
    // transbordador). Dinamicas propias: la diana de Elon (te sigue de carril y,
    // al fijarse, cae un Cybertruck) y el momento estrella, el hangar de la Luna
    // con gravedad lunar (se salta por encima de los vehiculos lunares).
    id: "houston", nombre: "Main Street", lugar: "Houston, Texas", listo: true,
    zona: "city", carpeta: "houston", luz: "tarde", semilla: 1961,
    largo: 3300, linea: 11.5, velMax: 25,
    potenciadores: ["magnet", "shield", "boost", "mega", "rocket", "botas"],
    kit: { minPlantas: 4, maxPlantas: 16, estilo: "houston" },
    horizonte: "houston",
    obstaculos: { low: ["roca_lunar", "paca", "valla_metal"], high: ["cartel_elon", "andamio"],
      full: ["pickup", "furgoneta", "autocaravana", "taxi"] },
    publico: { personas: ["fan", "turista", "ejecutivo", "chico", "senora"], valla: "banderas", cada: 2 },
    tramos: [
      [0, 70, "calma", { titulo: "houston" }],
      [70, 280, "mixto", { densidad: 0.45, titulo: "main_street_hou" }],
      [280, 430, "rampa", { titulo: "rampa" }],
      [430, 600, "slalom", { full: ["pickup", "furgoneta", "autocaravana"], titulo: "texas" }],
      [600, 680, "calma"],
      [680, 1120, "elon", { titulo: "elon" }],
      [1120, 1190, "calma"],
      [1190, 1350, "premios", { titulo: "premios" }],
      [1350, 1510, "jefe_paso", { titulo: "jefe_paso" }],
      [1510, 1680, "vallas", { low: ["roca_lunar", "paca"], high: ["cartel_elon"], titulo: "fans_elon" }],
      [1680, 1760, "calma"],
      [1760, 1920, "mixto", { densidad: 0.5, momento: "reto", titulo: "reto" }],
      [1920, 2000, "calma", { titulo: "space_center" }],
      // El momento estrella: el hangar de la Luna (pieza de `fondo` e `interior`).
      [2000, 2420, "luna", { titulo: "luna" }],
      [2420, 2500, "calma"],
      [2500, 2900, "elon", { titulo: "elon2" }],
      [2900, 3150, "alfombra", { titulo: "rocket_park" }],
      [3150, 3290, "sprint", { titulo: "sprint_houston" }],
    ],
    control: 1800, caja: 1200,
    interior: { rango: [2002, 2418], tipo: "luna", sinEdificios: [1990, 2430] },
    sinEdificios: [3200, 4000],
    chapas: [[1560, "arco"], [1840, "carril"], [3000, "arco"]],
    hitos: ["bank_of_america_hou", "jpmorgan_hou", "city_hall_hou", "saturno_v"],
    meta: "independence_plaza", metaNombre: { es: "el transbordador de la NASA", en: "the NASA shuttle" },
    izquierda: [
      40, ["kit", 2], 14, ["bank_of_america_hou", 1], 14, ...cuadras(5), ["city_hall_hou", 1], 14, ...cuadras(26),
    ],
    derecha: [
      40, ["kit", 3], 14, ...cuadras(2), ["jpmorgan_hou", 1], 14, ...cuadras(22), ["saturno_v", 1], 14, ...cuadras(3),
    ],
    fondo: [{ pieza: "independence_plaza", d: 3366, centro: true },
      { pieza: "hangar_luna", d: 2000, cruza: true }],
    final: "parada", parada: 44,
    camaraFinal: { pos: [6, 3, 12], mira: [0, 18, -60] },
    acera: ["phoenix/palmera", "ciudad/farola_ciudad", "ciudad/hidrante", "ciudad/farola_ciudad"],
  },
  {
    // 12/11/2026: nivel 17: Oklahoma City (blender/oklahoma.py). «Molinos de
    // viento girando en la pista (él dice que dan cáncer)». Recomendado: luz
    // dorada de la llanura y final ante el Capitolio (con su pozo de
    // petroleo). Dinamicas propias: los molinos en medio de la calle (la torre
    // en el centro y las aspas barriendo los lados: hay que pasar cuando no
    // baja ninguna) y los geiseres de petroleo (burbujean, escupen y su charco
    // resbala). Por en medio cruza el puente Skydance.
    id: "oklahoma", nombre: "Bricktown", lugar: "Oklahoma City, Oklahoma", listo: true,
    zona: "city", carpeta: "oklahoma", luz: "dorada", semilla: 1889,
    largo: 3300, linea: 11.5, velMax: 25,
    potenciadores: ["magnet", "shield", "boost", "mega", "botas"],
    kit: { minPlantas: 3, maxPlantas: 10, estilo: "oklahoma" },
    horizonte: "oklahoma",
    obstaculos: { low: ["paca", "calavera", "valla_metal"], high: ["cartel_molinos", "cartel_ruta"],
      full: ["pickup", "tractor", "vaquero", "furgoneta"] },
    publico: { personas: ["granjero", "fan", "turista", "abuelo", "chico"], valla: "banderas", cada: 2 },
    tramos: [
      [0, 70, "calma", { titulo: "oklahoma" }],
      [70, 260, "vallas", { low: ["paca", "calavera"], high: ["cartel_molinos"], titulo: "bricktown" }],
      [260, 420, "geiseres", { titulo: "geiseres" }],
      [420, 500, "calma"],
      [500, 660, "slalom", { full: ["pickup", "tractor", "vaquero"], titulo: "rodeo" }],
      [660, 740, "calma"],
      // El momento estrella: los molinos en la calle.
      [740, 1100, "molinos", { titulo: "molinos" }],
      [1100, 1180, "calma"],
      [1180, 1340, "premios", { titulo: "premios" }],
      [1340, 1500, "jefe_paso", { titulo: "jefe_paso" }],
      [1500, 1820, "geiseres", { titulo: "geiseres2" }],
      [1820, 1900, "calma"],
      [1900, 2060, "mixto", { densidad: 0.5, momento: "reto", titulo: "reto" }],
      [2060, 2140, "calma"],
      [2140, 2600, "molinos", { titulo: "parque_eolico" }],
      [2600, 2680, "calma"],
      [2680, 2860, "rampa", { titulo: "rampa" }],
      [2860, 3140, "mixto", { densidad: 0.55, titulo: "" }],
      [3140, 3290, "sprint", { titulo: "sprint_capitolio_ok" }],
    ],
    control: 1900, caja: 1200,
    sinEdificios: [3260, 4000],
    chapas: [[600, "carril"], [1930, "carril"], [2950, "arco"]],
    hitos: ["bricktown", "devon_tower", "cristal_bridge"],
    meta: "capitolio_ok", metaNombre: { es: "el Capitolio de Oklahoma", en: "the Oklahoma Capitol" },
    izquierda: [
      40, ["bricktown", 1], 14, ...cuadras(4), ["devon_tower", 1], 14, ...cuadras(23),
    ],
    derecha: [
      40, ["kit", 3], 14, ["bricktown", 1], 14, ...cuadras(6), ["cristal_bridge", 1], 14, ...cuadras(20),
    ],
    fondo: [{ pieza: "capitolio_ok", d: 3330, centro: true },
      { pieza: "skydance", d: 1640, cruza: true }],
    final: "parada", parada: 14,
    camaraFinal: { pos: [5, 3, 12], mira: [0, 14, -60] },
    acera: ["ciudad/farola_ciudad", "ciudad/arbol_ciudad", "ciudad/banco", "ciudad/farola_ciudad"],
  },
  {
    // 13/11/2026: nivel 18: Little Rock (blender/littlerock.py). «La mina de
    // diamantes: tacos de oro para su torre». Recomendado: otoño en las
    // Ozark (luz `otono`) y final ante el Capitolio de Arkansas. Dinamicas
    // propias: los jabalies Razorback que vienen zigzagueando entre dos
    // carriles y el momento estrella, la mina a oscuras (se ve poco) con
    // brillos que se desentierran deslizandose (+25 tacos).
    id: "little_rock", nombre: "President Clinton Avenue", lugar: "Little Rock, Arkansas", listo: true,
    zona: "city", carpeta: "littlerock", luz: "otono", semilla: 1821,
    largo: 3300, linea: 11.5, velMax: 25,
    potenciadores: ["magnet", "shield", "boost", "mega", "botas"],
    kit: { minPlantas: 3, maxPlantas: 10, estilo: "littlerock" },
    horizonte: "littlerock",
    obstaculos: { low: ["tnt", "paca", "valla_metal"], high: ["cartel_pig", "andamio"],
      full: ["pickup", "tractor", "furgoneta", "taxi"] },
    publico: { personas: ["fan", "granjero", "abuelo", "chico", "senora"], valla: "banderas", cada: 2 },
    tramos: [
      [0, 70, "calma", { titulo: "littlerock" }],
      [70, 280, "mixto", { densidad: 0.45, titulo: "river_market" }],
      [280, 430, "rampa", { titulo: "rampa" }],
      [430, 780, "jabalies", { titulo: "razorbacks" }],
      [780, 860, "calma"],
      [860, 1020, "premios", { titulo: "premios" }],
      [1020, 1180, "jefe_paso", { titulo: "jefe_paso" }],
      [1180, 1260, "calma", { titulo: "bajada_mina" }],
      // El momento estrella: la mina (pieza de `fondo` e `interior`).
      [1260, 1680, "mina", { titulo: "mina" }],
      [1680, 1760, "calma"],
      [1760, 1920, "mixto", { densidad: 0.5, momento: "reto", titulo: "reto" }],
      [1920, 2000, "calma"],
      [2000, 2400, "jabalies", { titulo: "razorbacks2" }],
      [2400, 2480, "calma"],
      [2480, 2640, "vallas", { low: ["tnt", "paca"], high: ["cartel_pig"], titulo: "woo_pig" }],
      [2640, 2800, "alfombra", { titulo: "alfombra" }],
      [2800, 3140, "mixto", { densidad: 0.55, titulo: "" }],
      [3140, 3290, "sprint", { titulo: "sprint_capitolio_ar" }],
    ],
    control: 1720, caja: 900,
    interior: { rango: [1262, 1678], tipo: "mina", sinEdificios: [1250, 1690] },
    sinEdificios: [3260, 4000],
    chapas: [[700, "carril"], [1800, "carril"], [2900, "arco"]],
    hitos: ["river_market", "clinton_library", "old_state_house"],
    meta: "capitolio_ar", metaNombre: { es: "el Capitolio de Arkansas", en: "the Arkansas Capitol" },
    izquierda: [
      40, ["kit", 2], 14, ["river_market", 1], 14, ...cuadras(4), ["old_state_house", 1], 14, ...cuadras(24),
    ],
    derecha: [
      40, ["kit", 3], 14, ...cuadras(1), ["clinton_library", 1], 14, ...cuadras(26),
    ],
    fondo: [{ pieza: "capitolio_ar", d: 3330, centro: true },
      { pieza: "mina", d: 1260, cruza: true }],
    final: "parada", parada: 14,
    camaraFinal: { pos: [5, 3, 12], mira: [0, 14, -60] },
    acera: ["ciudad/farola_ciudad", "ciudad/arbol_ciudad", "ciudad/banco", "ciudad/farola_ciudad"],
  },
  {
    // 13/11/2026: nivel 19: Jackson (blender/jackson.py). «Barcos de vapor.
    // Pajitas de papel que se deshacen (él volvió a las de plástico)».
    // Recomendado: atardecer del sur y final ante el Capitolio de Misisipi
    // (el aguila dorada). Dinamicas propias: las pajitas de papel (de lejos
    // cierran el carril; a 16 m se doblan y se saltan) y el momento estrella,
    // el barco de vapor: el chorro de vapor cruza la cubierta a ratos a la
    // altura de la cabeza (hay que deslizarse a tiempo).
    id: "jackson", nombre: "Capitol Street", lugar: "Jackson, Misisipi", listo: true,
    zona: "city", carpeta: "jackson", luz: "atardecer", semilla: 1822,
    largo: 3300, linea: 11.5, velMax: 25,
    potenciadores: ["magnet", "shield", "boost", "mega", "botas"],
    kit: { minPlantas: 2, maxPlantas: 8, estilo: "jackson" },
    horizonte: "jackson",
    obstaculos: { low: ["bala_algodon", "paca", "valla_metal"], high: ["cartel_pajitas", "guirnalda"],
      full: ["carruaje", "pickup", "tractor", "furgoneta"] },
    publico: { personas: ["abuelo", "senora", "fan", "chico", "turista"], valla: "banderas", cada: 2 },
    tramos: [
      [0, 70, "calma", { titulo: "jackson" }],
      [70, 280, "mixto", { densidad: 0.45, titulo: "farish_street" }],
      [280, 560, "pajitas", { titulo: "pajitas" }],
      [560, 640, "calma"],
      [640, 800, "premios", { titulo: "premios" }],
      [800, 960, "slalom", { full: ["carruaje", "pickup", "tractor"], titulo: "algodonales" }],
      [960, 1040, "calma", { titulo: "embarque" }],
      // El momento estrella: el barco de vapor (pieza de `fondo` e `interior`).
      [1040, 1460, "vapor", { titulo: "barco_vapor" }],
      [1460, 1540, "calma"],
      [1540, 1700, "jefe_paso", { titulo: "jefe_paso" }],
      [1700, 2000, "pajitas", { titulo: "pajitas2" }],
      [2000, 2080, "calma"],
      [2080, 2240, "mixto", { densidad: 0.5, momento: "reto", titulo: "reto" }],
      [2240, 2400, "vallas", { low: ["bala_algodon", "paca"], high: ["cartel_pajitas"], titulo: "algodon" }],
      [2400, 2480, "calma"],
      [2480, 2640, "rampa", { titulo: "rampa" }],
      [2640, 2800, "alfombra", { titulo: "alfombra" }],
      [2800, 3140, "mixto", { densidad: 0.55, titulo: "" }],
      [3140, 3290, "sprint", { titulo: "sprint_capitolio_ms" }],
    ],
    control: 1650, caja: 700,
    interior: { rango: [1042, 1458], tipo: "barco", aire: true, sinEdificios: [1030, 1470] },
    sinEdificios: [3260, 4000],
    chapas: [[720, "arco"], [2150, "carril"], [2900, "arco"]],
    hitos: ["old_capitol_ms", "casa_blues"],
    meta: "capitolio_ms", metaNombre: { es: "el Capitolio de Misisipi", en: "the Mississippi Capitol" },
    izquierda: [
      40, ["kit", 2], 14, ["old_capitol_ms", 1], 14, ...cuadras(26),
    ],
    derecha: [
      40, ["kit", 3], 14, ...cuadras(2), ["casa_blues", 1], ["kit", 2], 14, ...cuadras(25),
    ],
    fondo: [{ pieza: "capitolio_ms", d: 3330, centro: true },
      { pieza: "barco_vapor", d: 1040, cruza: true }],
    final: "parada", parada: 14,
    camaraFinal: { pos: [5, 3, 12], mira: [0, 14, -60] },
    acera: ["jackson/magnolia", "ciudad/farola_ciudad", "jackson/magnolia", "ciudad/banco"],
  },
  {
    // 13/11/2026: nivel 20: Nueva Orleans (blender/nuevaorleans.py).
    // «Carnaval. Ha rebautizado el golfo de Mexico como "golfo de America" y
    // los mapas se vuelven locos». Recomendado: anochecer de Mardi Gras (con
    // los faroles y neones) y final ante la catedral de San Luis. Dinamicas
    // propias: el desfile (las carrozas frenan cerca y se adelantan, y tiran
    // tacos de oro que vuelan a los carriles de al lado) y el momento
    // estrella, el golfo de America: izquierda y derecha van al reves.
    id: "nueva_orleans", nombre: "Bourbon Street", lugar: "Nueva Orleans, Luisiana", listo: true,
    zona: "city", carpeta: "nuevaorleans", luz: "anochecer", semilla: 1823,
    largo: 3300, linea: 11.5, velMax: 25,
    potenciadores: ["magnet", "shield", "boost", "mega", "botas"],
    kit: { minPlantas: 2, maxPlantas: 4, estilo: "nuevaorleans" },
    horizonte: "nuevaorleans",
    obstaculos: { low: ["rosca_reyes", "valla_desfile", "paca"], high: ["cartel_golfo", "guirnalda"],
      full: ["carruaje", "furgoneta", "taxi", "pickup"] },
    coche: "tranvia_nola",
    publico: { personas: ["fan", "turista", "chico", "senora", "abuelo"], valla: "banderas", cada: 2 },
    tramos: [
      [0, 70, "calma", { titulo: "nueva_orleans" }],
      [70, 300, "mixto", { densidad: 0.45, titulo: "bourbon_street" }],
      [300, 450, "rampa", { titulo: "rampa" }],
      [450, 520, "calma", { titulo: "mardi_gras" }],
      [520, 900, "desfile", { titulo: "desfile" }],
      [900, 980, "calma"],
      [980, 1140, "premios", { titulo: "premios" }],
      [1140, 1300, "jefe_paso", { titulo: "jefe_paso" }],
      [1300, 1380, "calma", { titulo: "golfo_cartel" }],
      // El momento estrella: el golfo de America (izquierda y derecha al reves).
      [1380, 1700, "golfo", { titulo: "golfo" }],
      [1700, 1780, "calma", { titulo: "golfo_fin" }],
      [1780, 1940, "mixto", { densidad: 0.5, momento: "reto", titulo: "reto" }],
      [1940, 2020, "calma"],
      [2020, 2400, "desfile", { titulo: "desfile2" }],
      [2400, 2480, "calma"],
      [2480, 2640, "vallas", { low: ["rosca_reyes", "valla_desfile"], high: ["cartel_golfo"], titulo: "beignets" }],
      [2640, 2800, "alfombra", { titulo: "alfombra" }],
      [2800, 3140, "mixto", { densidad: 0.55, titulo: "" }],
      [3140, 3290, "sprint", { titulo: "sprint_catedral" }],
    ],
    control: 1750, caja: 1050,
    sinEdificios: [3260, 4000],
    chapas: [[700, "carril"], [1850, "carril"], [2900, "arco"]],
    hitos: ["casa_criolla", "cafe_du_monde", "superdome"],
    meta: "catedral_sl", metaNombre: { es: "la catedral de San Luis", en: "St. Louis Cathedral" },
    izquierda: [
      40, ["kit", 2], 14, ["casa_criolla", 1], ["kit", 2], 14, ...cuadras(3), ["cafe_du_monde", 1], 14, ...cuadras(22),
    ],
    derecha: [
      40, ["kit", 3], 14, ...cuadras(3), ["superdome", 1], 14, ...cuadras(3), ["casa_criolla", 1], 14, ...cuadras(20),
    ],
    fondo: [{ pieza: "catedral_sl", d: 3330, centro: true },
      { pieza: "arco_carnaval", d: 470, cruza: true }, { pieza: "arco_carnaval", d: 1990, cruza: true },
      { pieza: "golfo_america", d: 1376, cruza: true }],
    final: "parada", parada: 14,
    camaraFinal: { pos: [5, 3, 12], mira: [0, 20, -45] },
    acera: ["ciudad/farola_ciudad", "ciudad/arbol_ciudad", "ciudad/banco", "ciudad/farola_ciudad"],
  },
  {
    // 13/11/2026: nivel 21: Birmingham (blender/birmingham.py). «Un huracan
    // que solo existe porque lo pinto el con un rotulador en el mapa».
    // Recomendado: mediodia de sol (el huracan solo esta pintado: en el cielo
    // del horizonte) y final ante la estatua de Vulcano. Dinamicas propias:
    // el rotulador gigante pinta muros de tinta carril a carril (hay que ir
    // por el que no pinta) y el momento estrella, la fundicion Sloss: el
    // martinete manda ondas al rojo por el suelo que hay que saltar a tiempo.
    id: "birmingham", nombre: "20th Street", lugar: "Birmingham, Alabama", listo: true,
    zona: "city", carpeta: "birmingham", luz: "mediodia", semilla: 1824,
    largo: 3300, linea: 11.5, velMax: 25,
    potenciadores: ["magnet", "shield", "boost", "mega", "botas"],
    kit: { minPlantas: 3, maxPlantas: 12, estilo: "birmingham" },
    horizonte: "birmingham",
    obstaculos: { low: ["lingotes", "paca", "valla_metal"], high: ["cartel_huracan", "andamio"],
      full: ["pickup", "furgoneta", "taxi", "tractor"] },
    publico: { personas: ["fan", "abuelo", "chico", "senora", "granjero"], valla: "banderas", cada: 2 },
    tramos: [
      [0, 70, "calma", { titulo: "birmingham" }],
      [70, 280, "mixto", { densidad: 0.45, titulo: "magic_city" }],
      [280, 640, "rotulador", { titulo: "rotulador" }],
      [640, 720, "calma"],
      [720, 880, "premios", { titulo: "premios" }],
      [880, 1040, "slalom", { full: ["pickup", "furgoneta", "taxi"], titulo: "alabama_theatre" }],
      [1040, 1120, "calma", { titulo: "entrada_sloss" }],
      // El momento estrella: la fundicion Sloss (pieza de `fondo` e `interior`).
      [1120, 1540, "fundicion", { titulo: "fundicion" }],
      [1540, 1620, "calma"],
      [1620, 1780, "jefe_paso", { titulo: "jefe_paso" }],
      [1780, 1860, "calma"],
      [1860, 2020, "mixto", { densidad: 0.5, momento: "reto", titulo: "reto" }],
      [2020, 2400, "rotulador", { titulo: "rotulador2" }],
      [2400, 2480, "calma"],
      [2480, 2640, "vallas", { low: ["lingotes", "paca"], high: ["cartel_huracan"], titulo: "cono" }],
      [2640, 2800, "rampa", { titulo: "rampa" }],
      [2800, 3140, "mixto", { densidad: 0.55, titulo: "" }],
      [3140, 3290, "sprint", { titulo: "sprint_vulcano" }],
    ],
    control: 1700, caja: 800,
    interior: { rango: [1122, 1538], tipo: "fundicion", sinEdificios: [1110, 1550] },
    sinEdificios: [3260, 4000],
    chapas: [[760, "carril"], [1900, "carril"], [2900, "arco"]],
    hitos: ["alabama_theatre", "sloss_hornos"],
    meta: "vulcano", metaNombre: { es: "la estatua de Vulcano", en: "the Vulcan statue" },
    izquierda: [
      40, ["kit", 2], 14, ...cuadras(3), ["alabama_theatre", 1], 14, ...cuadras(24),
    ],
    derecha: [
      40, ["kit", 3], 14, ...cuadras(5), ["sloss_hornos", 1], 14, ...cuadras(22),
    ],
    fondo: [{ pieza: "vulcano", d: 3330, centro: true },
      { pieza: "magic_city", d: 120, cruza: true },
      { pieza: "fundicion", d: 1120, cruza: true }],
    final: "parada", parada: 14,
    camaraFinal: { pos: [5, 3, 12], mira: [0, 30, -40] },
    acera: ["ciudad/farola_ciudad", "ciudad/arbol_ciudad", "ciudad/banco", "ciudad/farola_ciudad"],
  },
  {
    // 14/11/2026: nivel 22: Nashville (blender/nashville.py). «Musica
    // country. Llega a la meta bailando el YMCA». Recomendado: Broadway al
    // atardecer (con los neones de los honky-tonks) y final ante el Partenon
    // de Nashville, donde baila el YMCA (`baileFinal`, main.js). Dinamicas
    // propias: el baile en linea (una pareja de vaqueros tapa dos carriles y
    // da pasos de lado a lado: el carril libre va cambiando) y el momento
    // estrella, el Grand Ole Opry: el escenario es el mastil de una guitarra
    // gigante y las notas que brillan se pisan (suenan y dan tacos).
    id: "nashville", nombre: "Broadway", lugar: "Nashville, Tennessee", listo: true,
    zona: "city", carpeta: "nashville", luz: "atardecer", semilla: 1825,
    largo: 3300, linea: 11.5, velMax: 25,
    potenciadores: ["magnet", "shield", "boost", "mega", "botas"],
    kit: { minPlantas: 2, maxPlantas: 5, estilo: "nashville" },
    horizonte: "nashville",
    obstaculos: { low: ["amplificador", "bota_vaquera", "paca"], high: ["cartel_country", "guirnalda"],
      full: ["pickup", "furgoneta", "taxi", "bateria"] },
    publico: { personas: ["fan", "turista", "chico", "senora", "granjero"], valla: "banderas", cada: 2 },
    tramos: [
      [0, 70, "calma", { titulo: "nashville" }],
      [70, 280, "mixto", { densidad: 0.45, titulo: "broadway" }],
      [280, 640, "baile", { titulo: "baile" }],
      [640, 720, "calma"],
      [720, 880, "premios", { titulo: "premios" }],
      [880, 1040, "slalom", { full: ["pickup", "furgoneta", "taxi"], titulo: "ryman" }],
      [1040, 1120, "calma", { titulo: "entrada_opry" }],
      // El momento estrella: el Grand Ole Opry (pieza de `fondo` e `interior`).
      [1120, 1540, "opry", { titulo: "opry" }],
      [1540, 1620, "calma"],
      [1620, 1780, "jefe_paso", { titulo: "jefe_paso" }],
      [1780, 1860, "calma"],
      [1860, 2020, "mixto", { densidad: 0.5, momento: "reto", titulo: "reto" }],
      [2020, 2400, "baile", { titulo: "baile2" }],
      [2400, 2480, "calma"],
      [2480, 2640, "vallas", { low: ["amplificador", "bota_vaquera"], high: ["cartel_country"], titulo: "honky" }],
      [2640, 2800, "rampa", { titulo: "rampa" }],
      [2800, 3140, "mixto", { densidad: 0.55, titulo: "" }],
      [3140, 3290, "sprint", { titulo: "sprint_partenon" }],
    ],
    control: 1600, caja: 680,
    interior: { rango: [1122, 1538], tipo: "opry", sinEdificios: [1110, 1550] },
    sinEdificios: [3260, 4000],
    chapas: [[200, "carril"], [1930, "carril"], [2900, "arco"]],
    hitos: ["honky_tonk", "ryman", "batman_building"],
    meta: "partenon", metaNombre: { es: "el Partenón de Nashville", en: "the Nashville Parthenon" },
    izquierda: [
      40, ["kit", 2], 14, ["honky_tonk", 1], ["kit", 2], 14, ...cuadras(3), ["ryman", 1], 14, ...cuadras(22),
    ],
    derecha: [
      40, ["kit", 3], 14, ...cuadras(4), ["batman_building", 1], 14, ...cuadras(3), ["honky_tonk", 1], 14, ...cuadras(20),
    ],
    fondo: [{ pieza: "partenon", d: 3330, centro: true },
      { pieza: "arco_broadway", d: 120, cruza: true }, { pieza: "arco_broadway", d: 2000, cruza: true },
      { pieza: "opry", d: 1120, cruza: true }],
    // Se para en medio del escenario redondo y baila el YMCA (cuatro posturas, dos veces).
    final: "parada", parada: 7, baileFinal: "ymca",
    camaraFinal: { pos: [2.2, 1.7, 6.5], mira: [0, 4.2, -30] },
    acera: ["ciudad/farola_ciudad", "ciudad/arbol_ciudad", "ciudad/banco", "ciudad/farola_ciudad"],
  },
  {
    // 14/11/2026: nivel 23: Louisville (blender/louisville.py). «La carrera
    // de caballos del Derby: los caballos le adelantan». Recomendado: tarde
    // de primavera (el Derby se corre por la tarde) y final en el circulo del
    // ganador de Churchill Downs, bajo las dos agujas. Dinamicas propias:
    // los bates gigantes de Louisville Slugger (de pie en el bordillo, caen
    // atravesados en la calle) y el momento estrella, la pista de Churchill
    // Downs: los caballos vienen por DETRAS y le adelantan (una flecha en el
    // suelo marca el carril del que hay que quitarse).
    id: "louisville", nombre: "Main Street", lugar: "Louisville, Kentucky", listo: true,
    zona: "city", carpeta: "louisville", luz: "tarde", semilla: 1826,
    largo: 3300, linea: 11.5, velMax: 25,
    potenciadores: ["magnet", "shield", "boost", "mega", "botas"],
    kit: { minPlantas: 2, maxPlantas: 6, estilo: "louisville" },
    horizonte: "louisville",
    obstaculos: { low: ["barricas_bourbon", "seto_derby", "paca"], high: ["cartel_rosas", "andamio"],
      full: ["pickup", "furgoneta", "cubo_pollo", "tractor"] },
    publico: { personas: ["fan", "senora", "abuelo", "chico", "granjero"], valla: "banderas", cada: 2 },
    tramos: [
      [0, 70, "calma", { titulo: "louisville" }],
      [70, 300, "mixto", { densidad: 0.45, titulo: "main_street" }],
      [300, 450, "rampa", { titulo: "rampa" }],
      [450, 520, "calma", { titulo: "slugger" }],
      [520, 900, "bates", { titulo: "bates" }],
      [900, 980, "calma"],
      [980, 1140, "premios", { titulo: "premios" }],
      [1140, 1300, "jefe_paso", { titulo: "jefe_paso" }],
      [1300, 1380, "calma"],
      [1380, 1540, "mixto", { densidad: 0.5, momento: "reto", titulo: "reto" }],
      [1540, 1700, "alfombra", { titulo: "alfombra" }],
      [1700, 1780, "calma", { titulo: "bourbon" }],
      [1780, 2140, "bates", { titulo: "bates2" }],
      [2140, 2220, "calma", { titulo: "entrada_pista" }],
      // El momento estrella: la pista de Churchill Downs (pieza de `fondo` e `interior`, al aire libre).
      [2220, 2640, "derby", { titulo: "derby" }],
      [2640, 2720, "calma", { titulo: "derby_fin" }],
      [2720, 2880, "vallas", { low: ["seto_derby", "barricas_bourbon"], high: ["cartel_rosas"], titulo: "rosas" }],
      [2880, 3140, "mixto", { densidad: 0.55, titulo: "" }],
      [3140, 3290, "sprint", { titulo: "sprint_churchill" }],
    ],
    control: 1740, caja: 940,
    interior: { rango: [2222, 2638], tipo: "hipodromo", aire: true, sinEdificios: [2210, 2650] },
    sinEdificios: [3260, 4000],
    chapas: [[180, "carril"], [1460, "carril"], [3000, "arco"]],
    hitos: ["slugger_museum", "destileria", "pollo_frito"],
    meta: "churchill_downs", metaNombre: { es: "la tribuna de Churchill Downs", en: "the Churchill Downs grandstand" },
    izquierda: [
      40, ["kit", 2], 14, ...cuadras(2), ["slugger_museum", 1], 14, ...cuadras(8), ["destileria", 1], 14, ...cuadras(16),
    ],
    derecha: [
      40, ["kit", 3], 14, ...cuadras(4), ["pollo_frito", 1], 14, ...cuadras(5), ["destileria", 1], 14, ...cuadras(4), ["pollo_frito", 1], 14, ...cuadras(12),
    ],
    fondo: [{ pieza: "churchill_downs", d: 3330, centro: true },
      { pieza: "arco_derby", d: 120, cruza: true }, { pieza: "arco_derby", d: 2190, cruza: true },
      { pieza: "hipodromo", d: 2220, cruza: true }],
    final: "parada", parada: 5,
    camaraFinal: { pos: [5, 3, 12], mira: [0, 14, -40] },
    acera: ["ciudad/farola_ciudad", "ciudad/arbol_ciudad", "ciudad/banco", "ciudad/farola_ciudad"],
  },
  {
    // 14/11/2026: nivel 24: Atlanta (blender/atlanta.py). «Su foto de la ficha
    // policial en cada pared. Mision: "encuentrame 11.780 votos". Aqui pasa de
    // 270». Recomendado: manana de sol por Peachtree Street y final ante el
    // teatro de las cupulas, con la marquesina «PRESIDENT ELECT · 270».
    // Dinamicas propias: la mision de los votos (contador arriba), las
    // papeletas que se escapan (vuelan haciendo eses de carril a carril: 300
    // votos cada una) y el momento estrella, el pabellon del recuento: el
    // trile de las urnas (la papeleta de oro entra en una, se barajan y hay
    // que pasar por la buena: 2.500 votos).
    id: "atlanta", nombre: "Peachtree Street", lugar: "Atlanta, Georgia", listo: true,
    zona: "city", carpeta: "atlanta", luz: "manana", semilla: 1827,
    largo: 3300, linea: 11.5, velMax: 25,
    potenciadores: ["magnet", "shield", "boost", "mega", "botas"],
    kit: { minPlantas: 3, maxPlantas: 12, estilo: "atlanta" },
    horizonte: "atlanta",
    obstaculos: { low: ["urna_voto", "cajas_melocoton", "paca"], high: ["cartel_fraude", "andamio"],
      full: ["pickup", "furgoneta", "taxi", "camion_melocotones"] },
    publico: { personas: ["fan", "ejecutivo", "chico", "senora", "turista"], valla: "banderas", cada: 2 },
    mision: { votos: 11780 },
    tramos: [
      [0, 70, "calma", { titulo: "atlanta" }],
      [70, 250, "mixto", { densidad: 0.45, titulo: "peachtree" }],
      [250, 610, "papeletas", { titulo: "papeletas" }],
      [610, 690, "calma", { titulo: "mural" }],
      [690, 850, "slalom", { full: ["pickup", "furgoneta", "taxi", "camion_melocotones"], titulo: "melocotones" }],
      [850, 1010, "premios", { titulo: "premios" }],
      [1010, 1090, "calma"],
      [1090, 1250, "jefe_paso", { titulo: "jefe_paso" }],
      [1250, 1330, "calma"],
      [1330, 1490, "mixto", { densidad: 0.5, momento: "reto", titulo: "reto" }],
      [1490, 1650, "rampa", { titulo: "rampa" }],
      [1650, 1730, "calma", { titulo: "entrada_recuento" }],
      // El momento estrella: el pabellon del recuento (pieza de `fondo` e `interior`).
      [1730, 2150, "recuento", { titulo: "recuento" }],
      [2150, 2230, "calma", { titulo: "recuento_fin" }],
      [2230, 2590, "papeletas", { titulo: "papeletas2" }],
      [2590, 2670, "calma"],
      [2670, 2830, "vallas", { low: ["urna_voto", "cajas_melocoton"], high: ["cartel_fraude"], titulo: "fraude" }],
      [2830, 3140, "mixto", { densidad: 0.55, titulo: "" }],
      [3140, 3290, "sprint", { titulo: "sprint_fox" }],
    ],
    control: 1300, caja: 930,
    interior: { rango: [1732, 2148], tipo: "recuento", sinEdificios: [1720, 2160] },
    sinEdificios: [3260, 4000],
    chapas: [[180, "carril"], [1400, "carril"], [2950, "arco"]],
    hitos: ["mural_ficha", "capitolio_georgia", "torre_piramide", "westin_cilindro"],
    meta: "fox_theatre", metaNombre: { es: "el teatro de las cúpulas", en: "the domed theatre" },
    izquierda: [
      40, ["kit", 2], 14, ...cuadras(2), ["mural_ficha", 1], 14, ...cuadras(3), ["capitolio_georgia", 1], 14, ...cuadras(22),
    ],
    derecha: [
      40, ["kit", 3], 14, ["torre_piramide", 1], 14, ...cuadras(4), ["westin_cilindro", 1], 14, ...cuadras(4), ["mural_ficha", 1], 14, ...cuadras(17),
    ],
    fondo: [{ pieza: "fox_theatre", d: 3330, centro: true },
      { pieza: "arco_melocoton", d: 120, cruza: true }, { pieza: "arco_melocoton", d: 2240, cruza: true },
      { pieza: "recuento", d: 1730, cruza: true }],
    final: "parada", parada: 6,
    camaraFinal: { pos: [5, 3, 12], mira: [0, 12, -40] },
    acera: ["ciudad/farola_ciudad", "atlanta/ficha_poster", "ciudad/arbol_ciudad", "ciudad/banco"],
  },
  {
    // 14/11/2026: nivel 25: Charlotte (blender/charlotte.py). «El circuito de
    // NASCAR». Recomendado: de noche y con focos (las carreras de Charlotte
    // son de noche) y final en el salon de la fama, con la cinta de acero y
    // los tres coches campeones. Dinamicas propias: el rebufo (los coches de
    // carreras van delante a tu velocidad: pegado detras se carga y, al
    // salirte de su carril, te lanza; cuando se les encienden las luces de
    // freno, fuera) y el momento estrella, el ovalo: el accidente en cadena
    // (tres coches en paralelo hacen trompos y se quedan cruzados: hay que
    // ver por donde queda el hueco).
    id: "charlotte", nombre: "Tryon Street", lugar: "Charlotte, Carolina del Norte", listo: true,
    zona: "city", carpeta: "charlotte", luz: "anochecer", semilla: 1828,
    largo: 3300, linea: 11.5, velMax: 26,
    potenciadores: ["magnet", "shield", "boost", "mega", "botas"],
    kit: { minPlantas: 4, maxPlantas: 14, estilo: "charlotte" },
    horizonte: "charlotte",
    obstaculos: { low: ["pila_ruedas", "carro_boxes", "paca"], high: ["cartel_carrera", "andamio"],
      full: ["pickup", "furgoneta", "taxi", "camion_equipo"] },
    publico: { personas: ["fan", "granjero", "chico", "senora", "abuelo"], valla: "banderas", cada: 2 },
    tramos: [
      [0, 70, "calma", { titulo: "charlotte" }],
      [70, 230, "mixto", { densidad: 0.45, titulo: "tryon" }],
      [230, 390, "premios", { titulo: "premios" }],
      [390, 470, "calma", { titulo: "olor_gasolina" }],
      [470, 830, "rebufo", { titulo: "rebufo" }],
      [830, 910, "calma"],
      [910, 1070, "vallas", { low: ["pila_ruedas", "carro_boxes"], high: ["cartel_carrera"], titulo: "boxes_clt" }],
      [1070, 1230, "rampa", { titulo: "rampa" }],
      [1230, 1310, "calma", { titulo: "entrada_ovalo" }],
      // El momento estrella: el ovalo (pieza de `fondo` e `interior`, al aire libre).
      [1310, 1730, "ovalo", { titulo: "ovalo" }],
      [1730, 1810, "calma", { titulo: "bandera_cuadros" }],
      [1810, 1970, "jefe_paso", { titulo: "jefe_paso" }],
      [1970, 2050, "calma"],
      [2050, 2210, "mixto", { densidad: 0.5, momento: "reto", titulo: "reto" }],
      [2210, 2570, "rebufo", { titulo: "rebufo2" }],
      [2570, 2650, "calma"],
      [2650, 2810, "slalom", { full: ["pickup", "furgoneta", "taxi", "camion_equipo"], titulo: "camiones" }],
      [2810, 3140, "mixto", { densidad: 0.55, titulo: "" }],
      [3140, 3290, "sprint", { titulo: "sprint_salon" }],
    ],
    control: 1770, caja: 320,
    interior: { rango: [1312, 1728], tipo: "ovalo", aire: true, sinEdificios: [1300, 1740] },
    sinEdificios: [3260, 4000],
    chapas: [[150, "carril"], [2100, "carril"], [2950, "arco"]],
    hitos: ["torre_corona", "garaje_carreras", "iglesia_presbiteriana", "torre_led"],
    meta: "salon_fama", metaNombre: { es: "el salón de la fama", en: "the Hall of Fame" },
    izquierda: [
      40, ["kit", 2], 14, ["torre_corona", 1], 14, ...cuadras(4), ["iglesia_presbiteriana", 1], 14, ...cuadras(22),
    ],
    derecha: [
      40, ["kit", 3], 14, ...cuadras(2), ["garaje_carreras", 1], 14, ...cuadras(3), ["torre_led", 1], 14, ...cuadras(4), ["garaje_carreras", 1], 14, ...cuadras(16),
    ],
    fondo: [{ pieza: "salon_fama", d: 3330, centro: true },
      { pieza: "arco_carrera", d: 120, cruza: true }, { pieza: "arco_carrera", d: 2620, cruza: true },
      { pieza: "speedway", d: 1310, cruza: true }],
    final: "parada", parada: 8,
    camaraFinal: { pos: [5, 3, 12], mira: [0, 10, -40] },
    acera: ["ciudad/farola_ciudad", "ciudad/arbol_ciudad", "ciudad/banco", "ciudad/farola_ciudad"],
  },
  {
    // 14/11/2026: nivel 26: Charleston (blender/charleston.py). «Se escapa a
    // jugar al golf: pelotas volando y carritos». Recomendado: tarde dorada
    // por East Bay Street y final en la fuente de la pina del parque del
    // puerto, con el puente de los diamantes al fondo. Dinamicas propias: las
    // calesas de turistas (van delante y el caballo deja «regalitos» que se
    // saltan) y el momento estrella, el campo de golf: Trump da golpes y hay
    // que correr al carril donde cae su bola (el aro amarillo).
    id: "charleston_sc", nombre: "East Bay Street", lugar: "Charleston, Carolina del Sur", listo: true,
    zona: "city", carpeta: "charleston", luz: "dorada", semilla: 1829,
    largo: 3300, linea: 11.5, velMax: 25,
    potenciadores: ["magnet", "shield", "boost", "mega", "botas"],
    kit: { minPlantas: 2, maxPlantas: 4, estilo: "charleston" },
    horizonte: "charleston",
    obstaculos: { low: ["bolsa_golf", "paca", "valla_metal"], high: ["cartel_fore", "andamio"],
      full: ["pickup", "furgoneta", "taxi", "carrito_parado"] },
    publico: { personas: ["turista", "senora", "abuelo", "fan", "chico"], valla: "banderas", cada: 2 },
    tramos: [
      [0, 70, "calma", { titulo: "charleston" }],
      [70, 250, "mixto", { densidad: 0.45, titulo: "east_bay" }],
      [250, 610, "calesas", { titulo: "calesas" }],
      [610, 690, "calma", { titulo: "rainbow_row" }],
      [690, 850, "premios", { titulo: "premios" }],
      [850, 1010, "slalom", { full: ["carrito_parado", "pickup", "furgoneta", "taxi"], titulo: "carritos" }],
      [1010, 1090, "calma"],
      [1090, 1250, "jefe_paso", { titulo: "jefe_paso" }],
      [1250, 1330, "calma"],
      [1330, 1490, "mixto", { densidad: 0.5, momento: "reto", titulo: "reto" }],
      [1490, 1570, "calma", { titulo: "entrada_golf" }],
      // El momento estrella: el campo de golf (pieza de `fondo` e `interior`, al aire libre).
      [1570, 1990, "golf", { titulo: "golf" }],
      [1990, 2070, "calma", { titulo: "hoyo18" }],
      [2070, 2430, "calesas", { titulo: "calesas2" }],
      [2430, 2510, "calma"],
      [2510, 2670, "vallas", { low: ["bolsa_golf", "valla_metal"], high: ["cartel_fore"], titulo: "fore" }],
      [2670, 2830, "rampa", { titulo: "rampa" }],
      [2830, 3140, "mixto", { densidad: 0.55, titulo: "" }],
      [3140, 3290, "sprint", { titulo: "sprint_pina" }],
    ],
    control: 1290, caja: 770,
    interior: { rango: [1572, 1988], tipo: "golf", aire: true, sinEdificios: [1560, 2000] },
    sinEdificios: [3260, 4000],
    chapas: [[150, "carril"], [1400, "carril"], [2950, "arco"]],
    hitos: ["rainbow_row", "san_miguel", "mercado_charleston", "casa_battery"],
    meta: "fuente_pina", metaNombre: { es: "la fuente de la piña", en: "the Pineapple Fountain" },
    izquierda: [
      40, ["kit", 2], 14, ["rainbow_row", 1], 14, ...cuadras(3), ["mercado_charleston", 1], 14, ...cuadras(5), ["casa_battery", 1], 14, ...cuadras(16),
    ],
    derecha: [
      40, ["kit", 3], 14, ...cuadras(2), ["san_miguel", 1], 14, ...cuadras(2), ["rainbow_row", 1], 14, ...cuadras(6), ["casa_battery", 1], 14, ...cuadras(13),
    ],
    fondo: [{ pieza: "fuente_pina", d: 3330, centro: true },
      { pieza: "arco_charleston", d: 120, cruza: true }, { pieza: "arco_charleston", d: 2030, cruza: true },
      { pieza: "campo_golf", d: 1570, cruza: true }],
    final: "parada", parada: 2,
    camaraFinal: { pos: [5, 3, 12], mira: [0, 8, -40] },
    acera: ["ciudad/farola_ciudad", "ciudad/arbol_ciudad", "ciudad/banco", "ciudad/farola_ciudad"],
  },
  {
    // 14/11/2026: nivel 27: Miami (blender/miami.py). Jefe. «El huracan de
    // papeles llega a Mar-a-Lago: carpetas con tachones y cajas de documentos
    // secretos en el bano. Intenta desviarlo con su rotulador». Recomendado:
    // Ocean Drive con cielo de huracan (verde gris, sin relampagos) y final
    // en Mar-a-Lago. Dinamicas propias: las olas que cruzan la calle desde la
    // playa (solo pillan el carril por el que pasan justo cuando llegas: ahi
    // se saltan), el momento estrella, el bano dorado de Mar-a-Lago, con
    // lamparas de arana que se balancean entre vateres de oro y torres de
    // cajas de documentos, y el jefe: el remolino de papeles (con el rotulador).
    id: "miami", nombre: "Ocean Drive", lugar: "Miami, Florida", listo: true,
    zona: "city", carpeta: "miami", luz: "tornado", semilla: 1830,
    largo: 3300, linea: 11.5, velMax: 25,
    potenciadores: ["magnet", "shield", "boost", "mega", "botas"],
    kit: { minPlantas: 3, maxPlantas: 6, estilo: "miami" },
    horizonte: "miami",
    obstaculos: { low: ["tumbona", "paca", "valla_metal"], high: ["sombrilla", "cartel_tachado"],
      full: ["descapotable", "taxi", "furgoneta", "flamencos"] },
    publico: { personas: ["turista", "fan", "chico", "senora", "ejecutivo"], valla: "banderas", cada: 2 },
    tramos: [
      [0, 70, "calma", { titulo: "miami" }],
      [70, 250, "mixto", { densidad: 0.45, titulo: "ocean_drive" }],
      [250, 610, "marejada", { titulo: "marejada" }],
      [610, 690, "calma"],
      [690, 850, "slalom", { full: ["descapotable", "taxi", "flamencos"], titulo: "flamencos" }],
      [850, 930, "calma", { titulo: "entrada_bano" }],
      // El momento estrella: el bano dorado de Mar-a-Lago (pieza de `fondo` e `interior`).
      [930, 1350, "bano", { titulo: "bano_dorado" }],
      [1350, 1430, "calma", { titulo: "bano_fin" }],
      [1430, 1590, "premios", { titulo: "premios" }],
      [1590, 1670, "calma"],
      [1670, 2290, "jefe", { jefe: "papeles", titulo: "huracan_papeles" }],
      [2290, 2370, "calma"],
      [2370, 2730, "marejada", { titulo: "marejada2" }],
      [2730, 2810, "calma"],
      [2810, 2970, "vallas", { low: ["tumbona", "valla_metal"], high: ["sombrilla", "cartel_tachado"], titulo: "tachones" }],
      [2970, 3140, "mixto", { densidad: 0.55, titulo: "" }],
      [3140, 3290, "sprint", { titulo: "sprint_maralago" }],
    ],
    control: 1630, caja: 1510,
    interior: { rango: [932, 1348], tipo: "bano", sinEdificios: [920, 1360] },
    sinEdificios: [3260, 4000],
    chapas: [[160, "carril"], [3000, "carril"], [3100, "arco"]],
    hitos: ["hotel_deco_rosa", "playa_socorrista", "hotel_deco_azul"],
    meta: "mar_a_lago", metaNombre: { es: "Mar-a-Lago", en: "Mar-a-Lago" },
    izquierda: [
      40, ["kit", 2], 14, ["hotel_deco_rosa", 1], 14, ...cuadras(2), ["hotel_deco_azul", 1], 14, ...cuadras(3), ["hotel_deco_rosa", 1], 14, ...cuadras(19),
    ],
    derecha: [
      40, ["playa_socorrista", 1], 14, ["kit", 2], 14, ["playa_socorrista", 1], 14, ...cuadras(3), ["playa_socorrista", 1], 14, ...cuadras(19),
    ],
    fondo: [{ pieza: "mar_a_lago", d: 3330, centro: true },
      { pieza: "arco_miami", d: 120, cruza: true }, { pieza: "arco_miami", d: 2330, cruza: true },
      { pieza: "bano_dorado", d: 930, cruza: true }],
    final: "parada", parada: 4,
    camaraFinal: { pos: [5, 3, 12], mira: [0, 14, -40] },
    acera: ["phoenix/palmera", "ciudad/farola_ciudad", "phoenix/palmera", "ciudad/banco"],
  },
  {
    // 14/11/2026: nivel 28: Albuquerque (blender/albuquerque.py). Empieza el
    // acto de la Armada Espanola. «El festival de globos. Primeros carteles
    // espanoles. Un platillo volante de Roswell». Recomendado: Central Avenue
    // (la Ruta 66) por la manana, con la sierra de Sandia al fondo, y final en
    // la plaza vieja ante San Felipe Neri. Dinamicas propias: el platillo que
    // se lleva un coche por el aire y lo suelta en el carril libre, y el
    // momento estrella, la fiesta de los globos: solo despega el globo del
    // quemador encendido. Pasa el Toro (el jefe del acto) y hay pancartas de
    // Espana: ALBURQUERQUE, con la R que perdio la ciudad.
    id: "albuquerque", nombre: "Central Avenue", lugar: "Albuquerque, Nuevo México", listo: true,
    zona: "city", carpeta: "albuquerque", luz: "manana", semilla: 1831,
    largo: 3300, linea: 11.5, velMax: 25,
    potenciadores: ["magnet", "shield", "boost", "mega", "botas"],
    kit: { minPlantas: 1, maxPlantas: 3, estilo: "albuquerque" },
    horizonte: "albuquerque",
    obstaculos: { low: ["horno_adobe", "cesta_globo", "valla_metal"], high: ["ristra_chiles", "cartel_alburquerque"],
      full: ["lowrider", "pickup", "autocaravana", "furgoneta"] },
    publico: { personas: ["turista", "fan", "chico", "senora", "abuelo"], valla: "banderas", cada: 2 },
    tramos: [
      [0, 70, "calma", { titulo: "albuquerque" }],
      [70, 250, "mixto", { densidad: 0.45, titulo: "ruta66" }],
      [250, 610, "platillo", { titulo: "platillo" }],
      [610, 690, "calma", { titulo: "kimo" }],
      [690, 850, "slalom", { full: ["lowrider", "pickup", "autocaravana"], titulo: "lowriders" }],
      [850, 930, "calma"],
      [930, 1070, "jefe_paso", { jefe: "toro", titulo: "toro_paso" }],
      [1070, 1150, "calma"],
      [1150, 1310, "mixto", { densidad: 0.5, momento: "reto", titulo: "reto" }],
      [1310, 1390, "calma", { titulo: "entrada_globos" }],
      // El momento estrella: la fiesta de los globos (pieza de `fondo` e `interior`, al aire libre).
      [1390, 1810, "globos", { titulo: "globos" }],
      [1810, 1890, "calma", { titulo: "globos_fin" }],
      [1890, 2050, "premios", { titulo: "premios" }],
      [2050, 2410, "platillo", { titulo: "platillo2" }],
      [2410, 2490, "calma"],
      [2490, 2650, "vallas", { low: ["horno_adobe", "valla_metal"], high: ["ristra_chiles", "cartel_alburquerque"], titulo: "con_r" }],
      [2650, 2810, "rampa", { titulo: "rampa" }],
      [2810, 3140, "mixto", { densidad: 0.55, titulo: "" }],
      [3140, 3290, "sprint", { titulo: "sprint_old_town" }],
    ],
    control: 1850, caja: 1970,
    interior: { rango: [1392, 1808], tipo: "globos", aire: true, sinEdificios: [1380, 1820] },
    sinEdificios: [3260, 4000],
    chapas: [[150, "carril"], [1200, "carril"], [2950, "arco"]],
    hitos: ["kimo_theatre", "casa_adobe", "motel_66"],
    meta: "san_felipe_neri", metaNombre: { es: "la plaza vieja", en: "the old plaza" },
    izquierda: [
      40, ["kit", 2], 14, ["kimo_theatre", 1], 14, ...cuadras(3), ["casa_adobe", 1], 14, ...cuadras(5), ["motel_66", 1], 14, ...cuadras(16),
    ],
    derecha: [
      40, ["kit", 3], 14, ...cuadras(2), ["motel_66", 1], 14, ...cuadras(3), ["casa_adobe", 1], 14, ...cuadras(6), ["casa_adobe", 1], 14, ...cuadras(13),
    ],
    fondo: [{ pieza: "san_felipe_neri", d: 3330, centro: true },
      { pieza: "arco_66", d: 120, cruza: true }, { pieza: "arco_66", d: 2450, cruza: true },
      { pieza: "campo_globos", d: 1390, cruza: true }],
    final: "parada", parada: 4,
    camaraFinal: { pos: [5, 3, 12], mira: [0, 10, -40] },
    acera: ["ciudad/farola_ciudad", "phoenix/saguaro_maceta", "ciudad/banco", "ciudad/farola_ciudad"],
  },
  {
    // 14/11/2026: nivel 29: Denver (blender/denver.py). «"Colorado" quiere
    // decir rojo en espanol: el dice que es una senal». Recomendado: el 16th
    // Street Mall en invierno, con las Rocosas nevadas al fondo, y final en el
    // Capitolio de Colorado (la cupula de oro y el escalon de la milla).
    // Dinamicas propias: las bolas de nieve que bajan rodando y crecen (las
    // pequenas se saltan, las grandes se esquivan) y el momento estrella, la
    // pista de esqui de las Rocosas con las puertas del eslalon (tacos por
    // puerta, oro cada cinco seguidas). Pasa el Toro y hay pancartas de
    // Espana: COLORADO = ROJO.
    // 24/11/2026: se paso a jugar esquiando (v77); el 25/11 Isidro: «Denver
    // esta bien; el esqui, prefiero que quede en el contenido desbloqueable».
    // Vuelve la calle, y la bajada al Capitolio es el modo «Esqui» del menu,
    // que se abre al superar este nivel (ESQUI, mas abajo).
    id: "denver", nombre: "16th Street Mall", lugar: "Denver, Colorado", listo: true,
    zona: "city", carpeta: "denver", luz: "invierno", semilla: 1832,
    largo: 3300, linea: 11.5, velMax: 25,
    potenciadores: ["magnet", "shield", "boost", "mega", "botas"],
    kit: { minPlantas: 3, maxPlantas: 7, estilo: "denver" },
    horizonte: "denver",
    obstaculos: { low: ["monton_nieve", "trineo", "valla_metal"], high: ["cartel_colorado", "pancarta"],
      full: ["mallride", "quitanieves", "pickup", "furgoneta"] },
    publico: { personas: ["turista", "fan", "chico", "senora", "ejecutivo"], valla: "banderas", cada: 2 },
    tramos: [
      [0, 70, "calma", { titulo: "denver" }],
      [70, 250, "mixto", { densidad: 0.45, titulo: "mall16" }],
      [250, 610, "bolas", { titulo: "bolas" }],
      [610, 690, "calma", { titulo: "union_station" }],
      [690, 850, "slalom", { full: ["mallride", "quitanieves", "pickup"], titulo: "mallride" }],
      [850, 930, "calma"],
      [930, 1090, "vallas", { low: ["monton_nieve", "valla_metal"], high: ["cartel_colorado"], titulo: "colorado_rojo" }],
      [1090, 1170, "calma"],
      [1170, 1330, "mixto", { densidad: 0.5, momento: "reto", titulo: "reto" }],
      [1330, 1410, "calma", { titulo: "entrada_esqui" }],
      // El momento estrella: la pista de esqui (pieza de `fondo` e `interior`, al aire libre).
      [1410, 1830, "esqui", { titulo: "esqui" }],
      [1830, 1910, "calma", { titulo: "esqui_fin" }],
      [1910, 2070, "premios", { titulo: "premios" }],
      [2070, 2210, "jefe_paso", { jefe: "toro", titulo: "toro_paso" }],
      [2210, 2290, "calma"],
      [2290, 2650, "bolas", { titulo: "bolas2" }],
      [2650, 2810, "rampa", { titulo: "rampa" }],
      [2810, 3140, "mixto", { densidad: 0.55, titulo: "" }],
      [3140, 3290, "sprint", { titulo: "sprint_capitolio_co" }],
    ],
    control: 1870, caja: 1990,
    interior: { rango: [1412, 1828], tipo: "esqui", aire: true, sinEdificios: [1400, 1840] },
    sinEdificios: [3260, 4000],
    chapas: [[150, "carril"], [1250, "carril"], [2950, "arco"]],
    hitos: ["torre_daniels", "union_station_den", "oso_azul"],
    meta: "capitolio_colorado", metaNombre: { es: "el Capitolio de Colorado", en: "the Colorado Capitol" },
    izquierda: [
      40, ["kit", 2], 14, ["torre_daniels", 1], 14, ...cuadras(3), ["union_station_den", 1], 14, ...cuadras(5), ["oso_azul", 1], 14, ...cuadras(14),
    ],
    derecha: [
      40, ["kit", 3], 14, ...cuadras(2), ["oso_azul", 1], 14, ...cuadras(4), ["torre_daniels", 1], 14, ...cuadras(5), ["union_station_den", 1], 14, ...cuadras(12),
    ],
    fondo: [{ pieza: "capitolio_colorado", d: 3330, centro: true },
      { pieza: "arco_denver", d: 120, cruza: true }, { pieza: "arco_denver", d: 2250, cruza: true },
      { pieza: "pista_esqui", d: 1410, cruza: true }],
    final: "parada", parada: 6,
    camaraFinal: { pos: [5, 3, 12], mira: [0, 14, -40] },
    acera: ["des_moines/arbol_nieve", "ciudad/farola_ciudad", "ciudad/banco", "ciudad/farola_ciudad"],
  },
  {
    // 14/11/2026: nivel 30: Cheyenne (blender/cheyenne.py). «Rodeo y estampida
    // de bisontes». Recomendado: Capitol Avenue en pleno Cheyenne Frontier
    // Days, a mediodia de verano, y final en el Capitolio de Wyoming (la
    // cupula de oro y el jinete de bronce del caballo que corcovea). Dinamicas
    // propias: la estampida, que se para echando el lazo (tocar la pantalla:
    // cuando vienen tres en fila es la unica salida), y el momento estrella,
    // el ruedo de Frontier Park: aguantar 8 segundos encima del toro con la
    // barra de equilibrio. Pancartas de Espana: ¡RODEO ES ESPAÑOL!
    id: "cheyenne", nombre: "Capitol Avenue", lugar: "Cheyenne, Wyoming", listo: true,
    zona: "city", carpeta: "cheyenne", luz: "mediodia", semilla: 1833,
    largo: 3300, linea: 11.5, velMax: 25,
    potenciadores: ["magnet", "shield", "boost", "mega", "botas"],
    kit: { minPlantas: 1, maxPlantas: 4, estilo: "cheyenne" },
    horizonte: "cheyenne",
    obstaculos: { low: ["barril_rodeo", "paca", "valla_rodeo"], high: ["cartel_rodeo", "pancarta"],
      full: ["diligencia", "pickup", "autocaravana", "payaso_barril"] },
    publico: { personas: ["turista", "fan", "chico", "senora", "abuelo"], valla: "banderas", cada: 2 },
    tramos: [
      [0, 70, "calma", { titulo: "cheyenne" }],
      [70, 250, "mixto", { densidad: 0.45, titulo: "frontier" }],
      [250, 610, "estampida", { titulo: "estampida" }],
      [610, 690, "calma", { titulo: "depot" }],
      [690, 850, "slalom", { full: ["diligencia", "pickup", "autocaravana"], titulo: "diligencias" }],
      [850, 930, "calma"],
      [930, 1090, "vallas", { low: ["barril_rodeo", "valla_rodeo"], high: ["cartel_rodeo"], titulo: "rodeo_es" }],
      [1090, 1170, "calma"],
      [1170, 1330, "mixto", { densidad: 0.5, momento: "reto", titulo: "reto" }],
      [1330, 1410, "calma", { titulo: "entrada_ruedo" }],
      // El momento estrella: el ruedo de Frontier Park (pieza de `fondo` e `interior`, al aire libre).
      [1410, 1830, "rodeo", { momento: "vehiculo", vehiculo: "toro_rodeo", titulo: "ruedo" }],
      [1830, 1910, "calma", { titulo: "ruedo_fin" }],
      [1910, 2070, "premios", { titulo: "premios" }],
      [2070, 2430, "estampida", { titulo: "estampida2" }],
      [2430, 2510, "calma"],
      [2510, 2650, "slalom", { full: ["payaso_barril", "diligencia", "pickup"], titulo: "payasos" }],
      [2650, 2810, "rampa", { titulo: "rampa" }],
      [2810, 3140, "mixto", { densidad: 0.55, titulo: "" }],
      [3140, 3290, "sprint", { titulo: "sprint_capitolio_wy" }],
    ],
    control: 1870, caja: 1990,
    interior: { rango: [1412, 1828], tipo: "rodeo", aire: true, sinEdificios: [1400, 1840] },
    sinEdificios: [3260, 4000],
    chapas: [[150, "carril"], [1250, "carril"], [2950, "arco"]],
    hitos: ["cheyenne_depot", "plains_hotel", "big_boy"],
    meta: "capitolio_wyoming", metaNombre: { es: "el Capitolio de Wyoming", en: "the Wyoming Capitol" },
    izquierda: [
      40, ["kit", 2], 14, ["cheyenne_depot", 1], 14, ...cuadras(3), ["plains_hotel", 1], 14, ...cuadras(5), ["big_boy", 1], 14, ...cuadras(14),
    ],
    derecha: [
      40, ["kit", 3], 14, ...cuadras(2), ["big_boy", 1], 14, ...cuadras(4), ["plains_hotel", 1], 14, ...cuadras(5), ["cheyenne_depot", 1], 14, ...cuadras(12),
    ],
    fondo: [{ pieza: "capitolio_wyoming", d: 3330, centro: true },
      { pieza: "arco_cheyenne", d: 120, cruza: true }, { pieza: "arco_cheyenne", d: 2250, cruza: true },
      { pieza: "arena_rodeo", d: 1410, cruza: true }],
    final: "parada", parada: 6,
    camaraFinal: { pos: [5, 3, 12], mira: [0, 14, -40] },
    acera: ["cheyenne/bota_gigante", "ciudad/farola_ciudad", "ciudad/banco", "ciudad/farola_ciudad"],
  },
  {
    // 14/11/2026: nivel 31: Billings (blender/billings.py). «"Montana" viene
    // de "montaña". Osos pardos». Recomendado: Montana Avenue en otono, con
    // las Rimrocks al fondo, y final al pie de las Rimrocks, en la puerta de
    // rancho de THE MAGIC CITY. Dinamicas propias: los osos que se van a tu
    // carril (apartarse no sirve: al pardo, que se pone de pie, hazte el
    // muerto; al negro, hazte grande), y el momento estrella, el Gran Arreo
    // de Montana: la vaca huye de ti y hay que llevarla al corral poniendose
    // al otro lado. Pancartas de Espana: MONTANA = MONTAÑA.
    id: "billings", nombre: "Montana Avenue", lugar: "Billings, Montana", listo: true,
    zona: "city", carpeta: "billings", luz: "otono", semilla: 1834,
    largo: 3300, linea: 11.5, velMax: 25,
    potenciadores: ["magnet", "shield", "boost", "mega", "botas"],
    kit: { minPlantas: 2, maxPlantas: 5, estilo: "billings" },
    horizonte: "billings",
    obstaculos: { low: ["tronco_caido", "paca", "valla_metal"], high: ["cartel_montana", "pancarta"],
      full: ["remolque_ganado", "pickup", "autocaravana", "furgoneta"] },
    publico: { personas: ["turista", "fan", "chico", "senora", "abuelo"], valla: "banderas", cada: 2 },
    tramos: [
      [0, 70, "calma", { titulo: "billings" }],
      [70, 250, "mixto", { densidad: 0.45, titulo: "montana_ave" }],
      [250, 610, "osos", { titulo: "osos" }],
      [610, 690, "calma", { titulo: "moss" }],
      [690, 850, "slalom", { full: ["remolque_ganado", "pickup", "autocaravana"], titulo: "remolques" }],
      [850, 930, "calma"],
      [930, 1090, "vallas", { low: ["tronco_caido", "valla_metal"], high: ["cartel_montana"], titulo: "montana_es" }],
      [1090, 1170, "calma"],
      [1170, 1330, "mixto", { densidad: 0.5, momento: "reto", titulo: "reto" }],
      [1330, 1410, "calma", { titulo: "entrada_arreo" }],
      // El momento estrella: el Gran Arreo de Montana (pieza de `fondo` e `interior`, al aire libre).
      [1410, 1830, "arreo", { titulo: "arreo" }],
      [1830, 1910, "calma", { titulo: "arreo_fin" }],
      [1910, 2070, "premios", { titulo: "premios" }],
      [2070, 2430, "osos", { titulo: "osos2" }],
      [2430, 2510, "calma", { titulo: "skypoint" }],
      [2510, 2650, "mixto", { densidad: 0.5 }],
      [2650, 2810, "rampa", { titulo: "rampa" }],
      [2810, 3140, "mixto", { densidad: 0.55, titulo: "" }],
      [3140, 3290, "sprint", { titulo: "sprint_rims" }],
    ],
    control: 1870, caja: 1990,
    interior: { rango: [1412, 1828], tipo: "arreo", aire: true, sinEdificios: [1400, 1840] },
    sinEdificios: [3260, 4000],
    chapas: [[150, "carril"], [1250, "carril"], [2950, "arco"]],
    hitos: ["billings_depot", "first_interstate", "moss_mansion"],
    meta: "rims_billings", metaNombre: { es: "las Rimrocks", en: "the Rimrocks" },
    izquierda: [
      40, ["kit", 2], 14, ["billings_depot", 1], 14, ...cuadras(3), ["first_interstate", 1], 14, ...cuadras(5), ["moss_mansion", 1], 14, ...cuadras(14),
    ],
    derecha: [
      40, ["kit", 3], 14, ...cuadras(2), ["moss_mansion", 1], 14, ...cuadras(4), ["first_interstate", 1], 14, ...cuadras(5), ["billings_depot", 1], 14, ...cuadras(12),
    ],
    fondo: [{ pieza: "rims_billings", d: 3330, centro: true },
      { pieza: "skypoint", d: 120, cruza: true }, { pieza: "skypoint", d: 2470, cruza: true },
      { pieza: "pradera_arreo", d: 1410, cruza: true }],
    final: "parada", parada: -2,
    camaraFinal: { pos: [5, 3, 12], mira: [0, 14, -40] },
    acera: ["ciudad/farola_ciudad", "ciudad/arbol_ciudad", "ciudad/banco", "ciudad/farola_ciudad"],
  },
  {
    // 14/11/2026: nivel 32: Boise (blender/boise.py). «Patatas rodando cuesta
    // abajo». Recomendado: Capitol Boulevard, de la estacion de estilo mision
    // espanola al Capitolio de Idaho, una manana de verano, pasando por el
    // Basque Block (la comunidad vasca mas grande de America). Dinamicas
    // propias: la patata caliente (hay que pasarsela a un periodista chocando
    // con el antes de que queme) y el momento estrella, los aizkolaris del
    // Jaialdi (filas de troncos que tapan la calle: tocar muy deprisa llena el
    // hacha y parte el tuyo). Las patatas gigantes bajan rodando por la calle.
    // Pancartas: ¡AUPA BOISE!
    id: "boise", nombre: "Capitol Boulevard", lugar: "Boise, Idaho", listo: true,
    zona: "city", carpeta: "boise", luz: "manana", semilla: 1835,
    largo: 3300, linea: 11.5, velMax: 25,
    potenciadores: ["magnet", "shield", "boost", "mega", "botas"],
    kit: { minPlantas: 1, maxPlantas: 4, estilo: "boise" },
    horizonte: "boise",
    obstaculos: { low: ["saco_patatas", "caja_patatas", "patata_rodante"], high: ["cartel_boise", "pancarta"],
      full: ["camion_patata", "pickup", "autocaravana", "furgoneta"] },
    publico: { personas: ["turista", "fan", "chico", "senora", "abuelo"], valla: "banderas", cada: 2 },
    tramos: [
      [0, 70, "calma", { titulo: "boise" }],
      [70, 250, "mixto", { densidad: 0.45, titulo: "capitol_blvd" }],
      [250, 610, "patata", { titulo: "patata" }],
      [610, 690, "calma", { titulo: "egipcio" }],
      [690, 850, "slalom", { full: ["camion_patata", "pickup", "autocaravana"], titulo: "camion_patata" }],
      [850, 930, "calma"],
      [930, 1090, "vallas", { low: ["saco_patatas", "caja_patatas"], high: ["cartel_boise"], titulo: "aupa" }],
      [1090, 1170, "calma"],
      [1170, 1330, "mixto", { densidad: 0.5, momento: "reto", titulo: "reto" }],
      [1330, 1410, "calma", { titulo: "entrada_jaialdi" }],
      // El momento estrella: los aizkolaris del Jaialdi (pieza de `fondo` e `interior`, al aire libre).
      [1410, 1830, "aizkolari", { titulo: "aizkolari" }],
      [1830, 1910, "calma", { titulo: "aizkolari_fin" }],
      [1910, 2070, "premios", { titulo: "premios" }],
      [2070, 2430, "patata", { titulo: "patata2" }],
      [2430, 2510, "calma", { titulo: "depot_boise" }],
      [2510, 2650, "mixto", { densidad: 0.5 }],
      [2650, 2810, "rampa", { titulo: "rampa" }],
      [2810, 3140, "mixto", { densidad: 0.55, titulo: "" }],
      [3140, 3290, "sprint", { titulo: "sprint_capitolio_id" }],
    ],
    control: 1870, caja: 1990,
    interior: { rango: [1412, 1828], tipo: "aizkolari", aire: true, sinEdificios: [1400, 1840] },
    sinEdificios: [3260, 4000],
    chapas: [[150, "carril"], [1250, "carril"], [2950, "arco"]],
    hitos: ["boise_depot", "egyptian_theatre", "casa_vasca"],
    meta: "capitolio_idaho", metaNombre: { es: "el Capitolio de Idaho", en: "the Idaho Capitol" },
    izquierda: [
      40, ["kit", 2], 14, ["boise_depot", 1], 14, ...cuadras(3), ["egyptian_theatre", 1], 14, ...cuadras(5), ["casa_vasca", 1], 14, ...cuadras(14),
    ],
    derecha: [
      40, ["kit", 3], 14, ...cuadras(2), ["casa_vasca", 1], 14, ...cuadras(4), ["egyptian_theatre", 1], 14, ...cuadras(5), ["boise_depot", 1], 14, ...cuadras(12),
    ],
    fondo: [{ pieza: "capitolio_idaho", d: 3330, centro: true },
      { pieza: "arco_vasco", d: 120, cruza: true }, { pieza: "arco_vasco", d: 2470, cruza: true },
      { pieza: "plaza_aizkolari", d: 1410, cruza: true }],
    final: "parada", parada: 6,
    camaraFinal: { pos: [5, 3, 12], mira: [0, 14, -40] },
    acera: ["boise/patata_acera", "ciudad/farola_ciudad", "ciudad/banco", "ciudad/farola_ciudad"],
  },
  {
    // 14/11/2026: nivel 33: Salt Lake City (blender/saltlake.py). «El desierto
    // de sal: el tramo mas rapido de la gira». Recomendado: State Street en
    // pleno julio, bajo el arco del aguila, y final en el Capitolio de Utah.
    // Dinamicas propias: los espejismos (una fila de coches parece tapar la
    // calle, pero los que no tienen sombra no existen: se pasa por dentro) y
    // el momento estrella, el record de Bonneville en el bolido (tocar cuando
    // la aguja esta en lo verde para meter la marcha siguiente: cada una, mas
    // velocidad). Pancartas de Espana: ¡ESCALANTE LLEGO PRIMERO! (1776).
    id: "salt_lake", nombre: "State Street", lugar: "Salt Lake City, Utah", listo: true,
    zona: "city", carpeta: "saltlake", luz: "mediodia", semilla: 1836,
    largo: 3300, linea: 11.5, velMax: 25,
    potenciadores: ["magnet", "shield", "boost", "mega", "botas"],
    kit: { minPlantas: 2, maxPlantas: 6, estilo: "saltlake" },
    horizonte: "saltlake",
    obstaculos: { low: ["bloque_sal", "barricada", "valla_metal"], high: ["cartel_utah", "pancarta"],
      full: ["trax", "hot_rod", "pickup", "autocaravana"] },
    publico: { personas: ["turista", "fan", "chico", "senora", "abuelo"], valla: "banderas", cada: 2 },
    tramos: [
      [0, 70, "calma", { titulo: "salt_lake" }],
      [70, 250, "mixto", { densidad: 0.45, titulo: "state_street" }],
      [250, 610, "espejismo", { titulo: "espejismo" }],
      [610, 690, "calma", { titulo: "eagle_gate" }],
      [690, 850, "slalom", { full: ["trax", "pickup", "autocaravana"], titulo: "trax" }],
      [850, 930, "calma"],
      [930, 1090, "vallas", { low: ["bloque_sal", "valla_metal"], high: ["cartel_utah"], titulo: "escalante" }],
      [1090, 1170, "calma"],
      [1170, 1330, "mixto", { densidad: 0.5, momento: "reto", titulo: "reto" }],
      [1330, 1410, "calma", { titulo: "entrada_salar" }],
      // El momento estrella: el record de Bonneville (pieza de `fondo` e `interior`, al aire libre).
      [1410, 1830, "record", { momento: "vehiculo", vehiculo: "bolido_sal", titulo: "record" }],
      [1830, 1910, "calma", { titulo: "record_fin" }],
      [1910, 2070, "premios", { titulo: "premios" }],
      [2070, 2430, "espejismo", { titulo: "espejismo2" }],
      [2430, 2510, "calma", { titulo: "colmenas" }],
      [2510, 2650, "slalom", { full: ["hot_rod", "trax", "pickup"], titulo: "hot_rods" }],
      [2650, 2810, "rampa", { titulo: "rampa" }],
      [2810, 3140, "mixto", { densidad: 0.55, titulo: "" }],
      [3140, 3290, "sprint", { titulo: "sprint_capitolio_ut" }],
    ],
    control: 1870, caja: 1990,
    interior: { rango: [1412, 1828], tipo: "record", aire: true, sinEdificios: [1400, 1840] },
    sinEdificios: [3260, 4000],
    chapas: [[150, "carril"], [1250, "carril"], [2950, "arco"]],
    hitos: ["city_county_slc", "depot_slc", "beehive_house"],
    meta: "capitolio_utah", metaNombre: { es: "el Capitolio de Utah", en: "the Utah Capitol" },
    izquierda: [
      40, ["kit", 2], 14, ["city_county_slc", 1], 14, ...cuadras(3), ["depot_slc", 1], 14, ...cuadras(5), ["beehive_house", 1], 14, ...cuadras(14),
    ],
    derecha: [
      40, ["kit", 3], 14, ...cuadras(2), ["beehive_house", 1], 14, ...cuadras(4), ["depot_slc", 1], 14, ...cuadras(5), ["city_county_slc", 1], 14, ...cuadras(12),
    ],
    fondo: [{ pieza: "capitolio_utah", d: 3330, centro: true },
      { pieza: "eagle_gate", d: 660, cruza: true }, { pieza: "eagle_gate", d: 2470, cruza: true },
      { pieza: "salar_bonneville", d: 1410, cruza: true }],
    final: "parada", parada: 6,
    camaraFinal: { pos: [5, 3, 12], mira: [0, 14, -40] },
    acera: ["saltlake/colmena", "ciudad/farola_ciudad", "ciudad/arbol_ciudad", "ciudad/farola_ciudad"],
  },
  {
    // 15/11/2026: nivel 34: Seattle (blender/seattle.py). «Llueve sin parar:
    // su pelo corre peligro». Recomendado: 5th Avenue bajo la lluvia (luz
    // «lluvia», con su lluvia que cae), con el monorrail por encima de la
    // acera, y final en la Space Needle. Dinamicas propias: el chaparron (el
    // tupe se moja: hay que ir de marquesina en marquesina) y el momento
    // estrella, los pescaderos de Pike Place que te lanzan salmones (tocar
    // justo cuando el aro se junta). Pancartas de Espana: JUAN DE FUCA LLEGO
    // EN 1592.
    id: "seattle", nombre: "5th Avenue", lugar: "Seattle, Washington", listo: true,
    zona: "city", carpeta: "seattle", luz: "lluvia", semilla: 1837,
    largo: 3300, linea: 11.5, velMax: 25,
    potenciadores: ["magnet", "shield", "boost", "mega", "botas"],
    kit: { minPlantas: 3, maxPlantas: 8, estilo: "seattle" },
    horizonte: "seattle",
    obstaculos: { low: ["cajon_hielo", "barricada", "valla_metal"], high: ["cartel_seattle", "pancarta"],
      full: ["tranvia_seattle", "carrito_cafe", "pickup", "furgoneta"] },
    publico: { personas: ["turista", "fan", "chico", "senora", "abuelo"], valla: "banderas", cada: 2 },
    tramos: [
      [0, 70, "calma", { titulo: "seattle" }],
      [70, 250, "mixto", { densidad: 0.45, titulo: "quinta_sea" }],
      [250, 610, "chaparron", { titulo: "chaparron" }],
      [610, 690, "calma", { titulo: "smith_tower" }],
      [690, 850, "slalom", { full: ["tranvia_seattle", "carrito_cafe", "pickup"], titulo: "tranvia_slu" }],
      [850, 930, "calma"],
      [930, 1090, "vallas", { low: ["cajon_hielo", "valla_metal"], high: ["cartel_seattle"], titulo: "juan_de_fuca" }],
      [1090, 1170, "calma"],
      [1170, 1330, "mixto", { densidad: 0.5, momento: "reto", titulo: "reto" }],
      [1330, 1410, "calma", { titulo: "entrada_pike" }],
      // El momento estrella: los pescaderos de Pike Place (pieza de `fondo` e `interior`).
      [1410, 1830, "pescado", { titulo: "pescado" }],
      [1830, 1910, "calma", { titulo: "pescado_fin" }],
      [1910, 2070, "premios", { titulo: "premios" }],
      [2070, 2430, "chaparron", { titulo: "chaparron2" }],
      [2430, 2510, "calma", { titulo: "monorail_t" }],
      [2510, 2650, "mixto", { densidad: 0.5 }],
      [2650, 2810, "rampa", { titulo: "rampa" }],
      [2810, 3140, "mixto", { densidad: 0.55, titulo: "" }],
      [3140, 3290, "sprint", { titulo: "sprint_needle" }],
    ],
    control: 1870, caja: 1990,
    interior: { rango: [1412, 1828], tipo: "pescado", aire: true, sinEdificios: [1400, 1840] },
    sinEdificios: [3260, 4000],
    chapas: [[150, "carril"], [1250, "carril"], [2950, "arco"]],
    hitos: ["mercado_pike", "smith_tower", "biblioteca_seattle"],
    meta: "space_needle", metaNombre: { es: "la Space Needle", en: "the Space Needle" },
    izquierda: [
      40, ["kit", 2], 14, ["mercado_pike", 1], 14, ...cuadras(3), ["smith_tower", 1], 14, ...cuadras(5), ["biblioteca_seattle", 1], 14, ...cuadras(14),
    ],
    derecha: [
      40, ["kit", 3], 14, ...cuadras(2), ["biblioteca_seattle", 1], 14, ...cuadras(4), ["smith_tower", 1], 14, ...cuadras(5), ["mercado_pike", 1], 14, ...cuadras(12),
    ],
    fondo: [{ pieza: "space_needle", d: 3330, centro: true },
      { pieza: "monorail", d: 200, cruza: true }, { pieza: "monorail", d: 2560, cruza: true },
      { pieza: "mercado_pescado", d: 1410, cruza: true }],
    final: "parada", parada: 6,
    camaraFinal: { pos: [5, 3, 12], mira: [0, 22, -40] },
    acera: ["seattle/cerdita_rachel", "ciudad/farola_ciudad", "ciudad/arbol_ciudad", "ciudad/farola_ciudad"],
  },
  {
    // 15/11/2026: nivel 35: Portland, Oregon (blender/portland.py).
    // «Manifestantes disfrazados de rana hinchable». Recomendado: Burnside
    // Street una tarde de verano, y final en el letrero PORTLAND OREGON con
    // el ciervo. Dinamicas propias: las ranas hinchables (cuando tapan la
    // calle, se toca una en la pantalla para deshincharla) y el momento
    // estrella, la regata de barcos dragon del Festival de las Rosas en el
    // Willamette (remar deslizando a izquierda y derecha, alternando).
    // Pancartas de Espana: ¿OREGON? ¡VIENE DE OREJON!
    id: "portland_or", nombre: "Burnside Street", lugar: "Portland, Oregón", listo: true,
    zona: "city", carpeta: "portland", luz: "tarde", semilla: 1838,
    largo: 3300, linea: 11.5, velMax: 25,
    potenciadores: ["magnet", "shield", "boost", "mega", "botas"],
    kit: { minPlantas: 2, maxPlantas: 5, estilo: "portland" },
    horizonte: "portland",
    obstaculos: { low: ["bicis_aparcadas", "barricada", "valla_metal"], high: ["cartel_oregon", "pancarta"],
      full: ["food_truck", "pickup", "furgoneta", "autocaravana"] },
    publico: { personas: ["turista", "fan", "chico", "senora", "abuelo"], valla: "banderas", cada: 2 },
    tramos: [
      [0, 70, "calma", { titulo: "portland_or" }],
      [70, 250, "mixto", { densidad: 0.45, titulo: "burnside" }],
      [250, 610, "ranas", { titulo: "ranas" }],
      [610, 690, "calma", { titulo: "powells_t" }],
      [690, 850, "slalom", { full: ["food_truck", "pickup", "furgoneta"], titulo: "food_trucks" }],
      [850, 930, "calma"],
      [930, 1090, "vallas", { low: ["bicis_aparcadas", "valla_metal"], high: ["cartel_oregon"], titulo: "orejon" }],
      [1090, 1170, "calma"],
      [1170, 1330, "mixto", { densidad: 0.5, momento: "reto", titulo: "reto" }],
      [1330, 1410, "calma", { titulo: "entrada_rio" }],
      // El momento estrella: la regata en el Willamette (pieza de `fondo` e `interior`, al aire libre).
      [1410, 1830, "regata", { momento: "vehiculo", vehiculo: "barco_dragon", titulo: "regata" }],
      [1830, 1910, "calma", { titulo: "regata_fin" }],
      [1910, 2070, "premios", { titulo: "premios" }],
      [2070, 2430, "ranas", { titulo: "ranas2" }],
      [2430, 2510, "calma", { titulo: "rosas" }],
      [2510, 2650, "mixto", { densidad: 0.5 }],
      [2650, 2810, "rampa", { titulo: "rampa" }],
      [2810, 3140, "mixto", { densidad: 0.55, titulo: "" }],
      [3140, 3290, "sprint", { titulo: "sprint_stag" }],
    ],
    control: 1870, caja: 1990,
    interior: { rango: [1412, 1828], tipo: "regata", aire: true, sinEdificios: [1400, 1840] },
    sinEdificios: [3260, 4000],
    chapas: [[150, "carril"], [1250, "carril"], [2950, "arco"]],
    hitos: ["powells", "portland_building", "union_station_pdx"],
    meta: "white_stag", metaNombre: { es: "el letrero de Portland", en: "the Portland sign" },
    izquierda: [
      40, ["kit", 2], 14, ["powells", 1], 14, ...cuadras(3), ["portland_building", 1], 14, ...cuadras(5), ["union_station_pdx", 1], 14, ...cuadras(14),
    ],
    derecha: [
      40, ["kit", 3], 14, ...cuadras(2), ["union_station_pdx", 1], 14, ...cuadras(4), ["portland_building", 1], 14, ...cuadras(5), ["powells", 1], 14, ...cuadras(12),
    ],
    fondo: [{ pieza: "white_stag", d: 3330, centro: true },
      { pieza: "arco_rosas", d: 120, cruza: true }, { pieza: "arco_rosas", d: 2470, cruza: true },
      { pieza: "rio_willamette", d: 1410, cruza: true }],
    final: "parada", parada: 6,
    camaraFinal: { pos: [5, 3, 12], mira: [0, 18, -40] },
    acera: ["portland/carrito_comida", "ciudad/farola_ciudad", "ciudad/arbol_ciudad", "ciudad/farola_ciudad"],
  },
  {
    // 15/11/2026: nivel 36: Anchorage (blender/anchorage.py). «Intenta comprar
    // Alaska. Le recuerdan que ya es suya. "Pues compro Groenlandia"».
    // Recomendado: 4th Avenue en verano (la luz dorada del sol de medianoche),
    // y final en la estacion del ferrocarril de Alaska con el cartel SE VENDE
    // GROENLANDIA. Dinamicas propias: el cheque gigante de 7,2 millones (va
    // por el carril de al lado: se cambia de lado tocando) y el momento
    // estrella, el hidroavion por las montañas Chugach (tocar para subir,
    // entre crestas y nubes; la camara no se mueve). Pancartas de España:
    // VALDEZ Y CORDOVA SON NOMBRES ESPAÑOLES.
    id: "anchorage", nombre: "4th Avenue", lugar: "Anchorage, Alaska", listo: true,
    zona: "city", carpeta: "anchorage", luz: "dorada", semilla: 1839,
    largo: 3300, linea: 11.5, velMax: 25,
    potenciadores: ["magnet", "shield", "boost", "mega", "botas"],
    kit: { minPlantas: 1, maxPlantas: 4, estilo: "anchorage" },
    horizonte: "anchorage",
    obstaculos: { low: ["nasa_cangrejo", "barricada", "valla_metal"], high: ["cartel_alaska", "pancarta"],
      full: ["autocaravana", "pickup", "alce", "furgoneta"] },
    publico: { personas: ["turista", "fan", "chico", "senora", "abuelo"], valla: "banderas", cada: 2 },
    tramos: [
      [0, 70, "calma", { titulo: "anchorage" }],
      [70, 250, "mixto", { densidad: 0.45, titulo: "cuarta" }],
      [250, 610, "cheque", { titulo: "cheque" }],
      [610, 690, "calma", { titulo: "teatro_4th" }],
      [690, 850, "slalom", { full: ["autocaravana", "pickup", "furgoneta"], titulo: "rv" }],
      [850, 930, "calma"],
      [930, 1090, "vallas", { low: ["nasa_cangrejo", "valla_metal"], high: ["cartel_alaska"], titulo: "valdez" }],
      [1090, 1170, "calma"],
      [1170, 1330, "mixto", { densidad: 0.5, momento: "reto", titulo: "reto" }],
      [1330, 1410, "calma", { titulo: "entrada_lago" }],
      // El momento estrella: el hidroavion (pieza de `fondo` e `interior`, al aire libre).
      [1410, 1830, "vuelo", { momento: "vehiculo", vehiculo: "hidroavion", titulo: "vuelo" }],
      [1830, 1910, "calma", { titulo: "vuelo_fin" }],
      [1910, 2070, "premios", { titulo: "premios" }],
      [2070, 2430, "cheque", { titulo: "cheque2" }],
      [2430, 2510, "calma", { titulo: "iditarod" }],
      [2510, 2650, "mixto", { densidad: 0.5 }],
      [2650, 2810, "rampa", { titulo: "rampa" }],
      [2810, 3140, "mixto", { densidad: 0.55, titulo: "" }],
      [3140, 3290, "sprint", { titulo: "sprint_estacion" }],
    ],
    control: 1870, caja: 1990,
    interior: { rango: [1412, 1828], tipo: "vuelo", aire: true, sinEdificios: [1400, 1840] },
    sinEdificios: [3260, 4000],
    chapas: [[150, "carril"], [1250, "carril"], [2950, "arco"]],
    hitos: ["teatro_4th", "cabana_troncos", "hotel_captain_cook"],
    meta: "estacion_alaska", metaNombre: { es: "la estación de Alaska", en: "the Alaska Railroad depot" },
    izquierda: [
      40, ["kit", 2], 14, ["teatro_4th", 1], 14, ...cuadras(3), ["cabana_troncos", 1], 14, ...cuadras(5), ["hotel_captain_cook", 1], 14, ...cuadras(14),
    ],
    derecha: [
      40, ["kit", 3], 14, ...cuadras(2), ["hotel_captain_cook", 1], 14, ...cuadras(4), ["cabana_troncos", 1], 14, ...cuadras(5), ["teatro_4th", 1], 14, ...cuadras(12),
    ],
    fondo: [{ pieza: "estacion_alaska", d: 3330, centro: true },
      { pieza: "arco_iditarod", d: 120, cruza: true }, { pieza: "arco_iditarod", d: 2470, cruza: true },
      { pieza: "vuelo_chugach", d: 1410, cruza: true }],
    final: "parada", parada: 6,
    camaraFinal: { pos: [5, 3, 12], mira: [0, 10, -40] },
    acera: ["anchorage/alce_pintado", "ciudad/farola_ciudad", "ciudad/arbol_ciudad", "ciudad/farola_ciudad"],
  },
  {
    // 15/11/2026: nivel 37: Honolulu (blender/honolulu.py). «Surf, cocos que
    // caen y golf otra vez». Recomendado: Kalakaua Avenue (Waikiki) una
    // mañana de sol, y final en el palacio Iolani. Dinamicas propias: el
    // collar de flores (coger las flores en el orden de colores de arriba; los
    // cocos caen de las palmeras y se quedan en la calle) y el momento
    // estrella, el surf (la ola te levanta: piruetas deslizando en el aire, y
    // aterrizar sin girar). El golf ya estaba en Charleston: no se repite.
    // Pancartas de España: PANIOLO = ESPAÑOL.
    id: "honolulu", nombre: "Kalakaua Avenue", lugar: "Honolulu, Hawái", listo: true,
    zona: "city", carpeta: "honolulu", luz: "manana", semilla: 1840,
    largo: 3300, linea: 11.5, velMax: 25,
    potenciadores: ["magnet", "shield", "boost", "mega", "botas"],
    kit: { minPlantas: 2, maxPlantas: 7, estilo: "honolulu" },
    horizonte: "honolulu",
    obstaculos: { low: ["tablas_surf", "barricada", "valla_metal"], high: ["cartel_hawaii", "pancarta"],
      full: ["trolley_waikiki", "carrito_raspado", "pickup", "furgoneta"] },
    publico: { personas: ["turista", "fan", "chico", "senora", "abuelo"], valla: "banderas", cada: 2 },
    tramos: [
      [0, 70, "calma", { titulo: "honolulu" }],
      [70, 250, "mixto", { densidad: 0.45, titulo: "kalakaua" }],
      [250, 610, "leis", { titulo: "leis" }],
      [610, 690, "calma", { titulo: "aloha_t" }],
      [690, 850, "slalom", { full: ["trolley_waikiki", "carrito_raspado", "pickup"], titulo: "trolley" }],
      [850, 930, "calma"],
      [930, 1090, "vallas", { low: ["tablas_surf", "valla_metal"], high: ["cartel_hawaii"], titulo: "paniolo" }],
      [1090, 1170, "calma"],
      [1170, 1330, "mixto", { densidad: 0.5, momento: "reto", titulo: "reto" }],
      [1330, 1410, "calma", { titulo: "entrada_playa" }],
      // El momento estrella: el surf en Waikiki (pieza de `fondo` e `interior`, al aire libre).
      [1410, 1830, "surf", { momento: "vehiculo", vehiculo: "tabla_surf", titulo: "surf" }],
      [1830, 1910, "calma", { titulo: "surf_fin" }],
      [1910, 2070, "premios", { titulo: "premios" }],
      [2070, 2430, "leis", { titulo: "leis2" }],
      [2430, 2510, "calma", { titulo: "rosa_hotel" }],
      [2510, 2650, "mixto", { densidad: 0.5 }],
      [2650, 2810, "rampa", { titulo: "rampa" }],
      [2810, 3140, "mixto", { densidad: 0.55, titulo: "" }],
      [3140, 3290, "sprint", { titulo: "sprint_iolani" }],
    ],
    control: 1870, caja: 1990,
    interior: { rango: [1412, 1828], tipo: "surf", aire: true, sinEdificios: [1400, 1840] },
    sinEdificios: [3260, 4000],
    chapas: [[150, "carril"], [1250, "carril"], [2950, "arco"]],
    hitos: ["aloha_tower", "royal_hawaiian", "capitolio_hawaii"],
    meta: "palacio_iolani", metaNombre: { es: "el palacio Iolani", en: "Iolani Palace" },
    izquierda: [
      40, ["kit", 2], 14, ["aloha_tower", 1], 14, ...cuadras(3), ["royal_hawaiian", 1], 14, ...cuadras(5), ["capitolio_hawaii", 1], 14, ...cuadras(14),
    ],
    derecha: [
      40, ["kit", 3], 14, ...cuadras(2), ["capitolio_hawaii", 1], 14, ...cuadras(4), ["royal_hawaiian", 1], 14, ...cuadras(5), ["aloha_tower", 1], 14, ...cuadras(12),
    ],
    fondo: [{ pieza: "palacio_iolani", d: 3330, centro: true },
      { pieza: "arco_aloha", d: 120, cruza: true }, { pieza: "arco_aloha", d: 2470, cruza: true },
      { pieza: "playa_waikiki", d: 1410, cruza: true }],
    final: "parada", parada: 6,
    camaraFinal: { pos: [5, 3, 12], mira: [0, 12, -40] },
    acera: ["honolulu/palmera_cocos", "ciudad/farola_ciudad", "ciudad/banco", "ciudad/farola_ciudad"],
  },
  {
    // 15/11/2026: nivel 38: Los Angeles (blender/losangeles.py). Nivel con
    // jefe: el Toro. «Encierro de San Fermin por Hollywood Boulevard: el Toro,
    // paelleras y la siesta española, que lo deja todo congelado». Recomendado:
    // Hollywood Boulevard al atardecer, las colinas con las letras LOS ANGELES
    // (las ha cambiado España) y final en el teatro chino. Dinamicas propias:
    // la siesta (la calle llena de gente durmiendo: la barra del ruido sube al
    // saltar; si se llena, chanclazo), el momento estrella, el rodaje en el
    // plato (hacer lo que grita el director a tiempo; cinco tomas seguidas, un
    // Oscar) y el jefe, el Toro del encierro (con paelleras y capotes).
    // Pancartas de España: LOS ANGELES ES ESPAÑOL (fin del acto).
    id: "los_angeles", nombre: "Hollywood Boulevard", lugar: "Los Ángeles, California", listo: true,
    zona: "city", carpeta: "losangeles", luz: "atardecer", semilla: 1841,
    largo: 3300, linea: 11.5, velMax: 25,
    potenciadores: ["magnet", "shield", "boost", "mega", "botas"],
    kit: { minPlantas: 2, maxPlantas: 5, estilo: "losangeles" },
    horizonte: "losangeles",
    obstaculos: { low: ["dormilon", "barricada", "valla_metal"], high: ["cartel_la", "pancarta", "hamaca"],
      full: ["autobus_estrellas", "camara_cine", "mozo", "pickup"] },
    publico: { personas: ["turista", "fan", "chico", "senora", "ejecutivo"], valla: "banderas", cada: 2 },
    tramos: [
      [0, 70, "calma", { titulo: "los_angeles" }],
      [70, 250, "mixto", { densidad: 0.45, titulo: "hollywood_blvd" }],
      [250, 610, "siesta", { titulo: "siesta" }],
      [610, 690, "calma", { titulo: "capitol_records_t" }],
      [690, 850, "slalom", { full: ["autobus_estrellas", "camara_cine", "mozo"], titulo: "mozos" }],
      [850, 930, "calma", { titulo: "entrada_plato" }],
      // El momento estrella: el rodaje en el plato (pieza de `fondo` e `interior`, al aire libre).
      [930, 1350, "rodaje", { titulo: "rodaje" }],
      [1350, 1430, "calma", { titulo: "rodaje_fin" }],
      [1430, 1590, "premios", { titulo: "premios" }],
      [1590, 1670, "calma"],
      [1670, 2290, "jefe", { jefe: "toro", titulo: "encierro" }],
      [2290, 2370, "calma"],
      [2370, 2730, "siesta", { titulo: "siesta2" }],
      [2730, 2810, "calma"],
      [2810, 2970, "vallas", { low: ["dormilon", "valla_metal"], high: ["cartel_la", "hamaca"], titulo: "los_angeles_es" }],
      [2970, 3140, "mixto", { densidad: 0.55, titulo: "" }],
      [3140, 3290, "sprint", { titulo: "sprint_chino" }],
    ],
    control: 1630, caja: 1510,
    interior: { rango: [932, 1348], tipo: "rodaje", aire: true, sinEdificios: [920, 1360] },
    sinEdificios: [3260, 4000],
    chapas: [[160, "carril"], [3000, "carril"], [3100, "arco"]],
    hitos: ["capitol_records", "el_capitan", "hotel_roosevelt"],
    meta: "teatro_chino", metaNombre: { es: "el teatro chino", en: "the Chinese Theatre" },
    izquierda: [
      40, ["kit", 2], 14, ["capitol_records", 1], 14, ...cuadras(2), ["el_capitan", 1], 14, ...cuadras(3), ["hotel_roosevelt", 1], 14, ...cuadras(19),
    ],
    derecha: [
      40, ["kit", 3], 14, ["hotel_roosevelt", 1], 14, ...cuadras(3), ["el_capitan", 1], 14, ...cuadras(3), ["capitol_records", 1], 14, ...cuadras(17),
    ],
    fondo: [{ pieza: "teatro_chino", d: 3330, centro: true },
      { pieza: "arco_san_fermin", d: 120, cruza: true }, { pieza: "arco_san_fermin", d: 2330, cruza: true },
      { pieza: "plato_cine", d: 930, cruza: true }],
    final: "parada", parada: 4,
    camaraFinal: { pos: [5, 3, 12], mira: [0, 12, -40] },
    acera: ["losangeles/estrella_fama", "ciudad/farola_ciudad", "ciudad/arbol_ciudad", "ciudad/farola_ciudad"],
  },
  {
    // 15/11/2026: nivel 39: Charleston, Virginia Occidental
    // (blender/charlestonwv.py). Empieza el acto del Sentido Comun. «Vagonetas
    // de su "precioso carbon limpio"». Recomendado: Capitol Street una tarde de
    // otoño, y final en el Capitolio con la cupula de oro. Dinamicas propias:
    // el saco de carbon (cada trozo pesa: vas mas lento de un carril a otro;
    // se vacia en las vagonetas) y el momento estrella, la vagoneta por las
    // vias del patio de carbon (solo se cambia de via en las agujas; las vias
    // cortadas cuestan tacos). Pancarta del Sentido Comun: EL CARBON MANCHA.
    id: "charleston_wv", nombre: "Capitol Street", lugar: "Charleston, Virginia Occidental", listo: true,
    zona: "city", carpeta: "charlestonwv", luz: "otono", semilla: 1842,
    largo: 3300, linea: 11.5, velMax: 25,
    potenciadores: ["magnet", "shield", "boost", "mega", "botas"],
    kit: { minPlantas: 1, maxPlantas: 4, estilo: "charlestonwv" },
    horizonte: "charlestonwv",
    obstaculos: { low: ["carbon_monton", "barricada", "valla_metal"], high: ["cartel_wv", "pancarta"],
      full: ["pickup", "furgoneta", "autocaravana"] },
    publico: { personas: ["turista", "fan", "chico", "senora", "abuelo"], valla: "banderas", cada: 2 },
    tramos: [
      [0, 70, "calma", { titulo: "charleston_wv" }],
      [70, 250, "mixto", { densidad: 0.45, titulo: "capitol_st" }],
      [250, 610, "carbon", { titulo: "carbon" }],
      [610, 690, "calma", { titulo: "daniel_boone" }],
      [690, 850, "slalom", { full: ["pickup", "furgoneta", "autocaravana"], titulo: "camiones_wv" }],
      [850, 930, "calma"],
      [930, 1090, "vallas", { low: ["carbon_monton", "valla_metal"], high: ["cartel_wv"], titulo: "sentido_carbon" }],
      [1090, 1170, "calma"],
      [1170, 1330, "mixto", { densidad: 0.5, momento: "reto", titulo: "reto" }],
      [1330, 1410, "calma", { titulo: "entrada_patio" }],
      // El momento estrella: la vagoneta por el patio de carbon (pieza de `fondo` e `interior`, al aire libre).
      [1410, 1830, "vias", { momento: "vehiculo", vehiculo: "vagoneta_carbon", titulo: "vias" }],
      [1830, 1910, "calma", { titulo: "vias_fin" }],
      [1910, 2070, "premios", { titulo: "premios" }],
      [2070, 2430, "carbon", { titulo: "carbon2" }],
      [2430, 2510, "calma", { titulo: "tipple" }],
      [2510, 2650, "mixto", { densidad: 0.5 }],
      [2650, 2810, "rampa", { titulo: "rampa" }],
      [2810, 3140, "mixto", { densidad: 0.55, titulo: "" }],
      [3140, 3290, "sprint", { titulo: "sprint_capitolio_wv" }],
    ],
    control: 1870, caja: 1990,
    interior: { rango: [1412, 1828], tipo: "vias", aire: true, sinEdificios: [1400, 1840] },
    sinEdificios: [3260, 4000],
    chapas: [[150, "carril"], [1250, "carril"], [2950, "arco"]],
    hitos: ["daniel_boone_hotel", "panaderia_pepperoni", "tipple_carbon"],
    meta: "capitolio_wv", metaNombre: { es: "el Capitolio de Virginia Occidental", en: "the West Virginia Capitol" },
    izquierda: [
      40, ["kit", 2], 14, ["daniel_boone_hotel", 1], 14, ...cuadras(3), ["panaderia_pepperoni", 1], 14, ...cuadras(5), ["tipple_carbon", 1], 14, ...cuadras(14),
    ],
    derecha: [
      40, ["kit", 3], 14, ...cuadras(2), ["tipple_carbon", 1], 14, ...cuadras(4), ["panaderia_pepperoni", 1], 14, ...cuadras(5), ["daniel_boone_hotel", 1], 14, ...cuadras(12),
    ],
    fondo: [{ pieza: "capitolio_wv", d: 3330, centro: true },
      { pieza: "arco_wv", d: 120, cruza: true }, { pieza: "arco_wv", d: 2470, cruza: true },
      { pieza: "patio_carbon", d: 1410, cruza: true }],
    final: "parada", parada: 6,
    camaraFinal: { pos: [5, 3, 12], mira: [0, 14, -40] },
    acera: ["charlestonwv/carretilla_carbon", "ciudad/farola_ciudad", "ciudad/arbol_ciudad", "ciudad/farola_ciudad"],
  },
  {
    // 15/11/2026: nivel 40: Richmond (blender/richmond.py). Acto del Sentido
    // Comun. «Tanques del desfile de su cumpleaños. Ha rebautizado Defensa
    // como "Departamento de Guerra"». Recomendado: Broad Street un dia de
    // desfile, y final en el Capitolio de Virginia (el templo de Jefferson).
    // Dinamicas propias: las minas de confeti escondidas (el detector avisa;
    // saltando no se pisan) y el momento estrella, el desfile por Monument
    // Avenue al paso del tambor (tocar al ritmo; ocho seguidos, premio).
    // Pancarta del Sentido Comun: LOS TANQUES ROMPEN LA CALLE.
    id: "richmond", nombre: "Broad Street", lugar: "Richmond, Virginia", listo: true,
    zona: "city", carpeta: "richmond", luz: "manana", semilla: 1843,
    largo: 3300, linea: 11.5, velMax: 25,
    potenciadores: ["magnet", "shield", "boost", "mega", "botas"],
    kit: { minPlantas: 1, maxPlantas: 4, estilo: "richmond" },
    horizonte: "richmond",
    obstaculos: { low: ["tarta_cumple", "barricada", "valla_metal"], high: ["cartel_va", "pancarta"],
      full: ["tanque", "pickup", "furgoneta", "autocaravana"] },
    publico: { personas: ["turista", "fan", "chico", "senora", "abuelo"], valla: "banderas", cada: 2 },
    tramos: [
      [0, 70, "calma", { titulo: "richmond" }],
      [70, 250, "mixto", { densidad: 0.45, titulo: "broad_st" }],
      [250, 610, "minas", { titulo: "minas" }],
      [610, 690, "calma", { titulo: "main_st" }],
      [690, 850, "slalom", { full: ["tanque", "pickup", "furgoneta"], titulo: "tanques" }],
      [850, 930, "calma"],
      [930, 1090, "vallas", { low: ["tarta_cumple", "valla_metal"], high: ["cartel_va"], titulo: "tanques_calle" }],
      [1090, 1170, "calma"],
      [1170, 1330, "mixto", { densidad: 0.5, momento: "reto", titulo: "reto" }],
      [1330, 1410, "calma", { titulo: "entrada_desfile" }],
      [1410, 1830, "desfile", { titulo: "desfile" }],
      [1830, 1910, "calma", { titulo: "desfile_fin" }],
      [1910, 2070, "premios", { titulo: "premios" }],
      [2070, 2430, "minas", { titulo: "minas2" }],
      [2430, 2510, "calma", { titulo: "guerra" }],
      [2510, 2650, "mixto", { densidad: 0.5 }],
      [2650, 2810, "rampa", { titulo: "rampa" }],
      [2810, 3140, "mixto", { densidad: 0.55, titulo: "" }],
      [3140, 3290, "sprint", { titulo: "sprint_capitolio_va" }],
    ],
    control: 1870, caja: 1990,
    interior: { rango: [1412, 1828], tipo: "desfile", aire: true, sinEdificios: [1400, 1840] },
    sinEdificios: [3260, 4000],
    chapas: [[150, "carril"], [1250, "carril"], [2950, "arco"]],
    hitos: ["estacion_main_st", "departamento_guerra", "teatro_byrd"],
    meta: "capitolio_va", metaNombre: { es: "el Capitolio de Virginia", en: "the Virginia Capitol" },
    izquierda: [
      40, ["kit", 2], 14, ["estacion_main_st", 1], 14, ...cuadras(3), ["departamento_guerra", 1], 14, ...cuadras(5), ["teatro_byrd", 1], 14, ...cuadras(14),
    ],
    derecha: [
      40, ["kit", 3], 14, ...cuadras(2), ["teatro_byrd", 1], 14, ...cuadras(4), ["departamento_guerra", 1], 14, ...cuadras(5), ["estacion_main_st", 1], 14, ...cuadras(12),
    ],
    fondo: [{ pieza: "capitolio_va", d: 3330, centro: true },
      { pieza: "arco_desfile", d: 120, cruza: true }, { pieza: "arco_desfile", d: 2470, cruza: true },
      { pieza: "desfile_monument", d: 1410, cruza: true }],
    final: "parada", parada: 6,
    camaraFinal: { pos: [5, 3, 12], mira: [0, 14, -40] },
    acera: ["richmond/globo_cumple", "ciudad/farola_ciudad", "ciudad/arbol_ciudad", "ciudad/farola_ciudad"],
  },
  {
    // 15/11/2026: nivel 41: Baltimore (blender/baltimore.py). Acto del Sentido
    // Comun. «Cangrejos que pellizcan los tobillos». Recomendado: Pratt Street
    // junto al Inner Harbor por la tarde, y final en el fuerte McHenry con la
    // bandera gigante. Dinamicas propias: los cangrejos que van de lado y, si
    // te pillan, se agarran al tobillo (no puedes saltar; tres cambios de
    // carril para soltarlo) y el momento estrella, las banderas de señales
    // del muelle (memorizar cuatro colores y pasar por ellos en orden).
    // Pancarta del Sentido Comun: LOS CANGREJOS PELLIZCAN.
    id: "baltimore", nombre: "Pratt Street", lugar: "Baltimore, Maryland", listo: true,
    zona: "city", carpeta: "baltimore", luz: "tarde", semilla: 1844,
    largo: 3300, linea: 11.5, velMax: 25,
    potenciadores: ["magnet", "shield", "boost", "mega", "botas"],
    kit: { minPlantas: 2, maxPlantas: 4, estilo: "baltimore" },
    horizonte: "baltimore",
    obstaculos: { low: ["olla_cangrejos", "barricada", "valla_metal"], high: ["cartel_md", "pancarta"],
      full: ["camion_especias", "pickup", "furgoneta", "autocaravana"] },
    publico: { personas: ["turista", "fan", "chico", "senora", "abuelo"], valla: "banderas", cada: 2 },
    tramos: [
      [0, 70, "calma", { titulo: "baltimore" }],
      [70, 250, "mixto", { densidad: 0.45, titulo: "pratt" }],
      [250, 610, "cangrejos", { titulo: "cangrejos" }],
      [610, 690, "calma", { titulo: "torre_bal" }],
      [690, 850, "slalom", { full: ["camion_especias", "pickup", "furgoneta"], titulo: "especias" }],
      [850, 930, "calma"],
      [930, 1090, "vallas", { low: ["olla_cangrejos", "valla_metal"], high: ["cartel_md"], titulo: "pellizcan" }],
      [1090, 1170, "calma"],
      [1170, 1330, "mixto", { densidad: 0.5, momento: "reto", titulo: "reto" }],
      [1330, 1410, "calma", { titulo: "entrada_muelle" }],
      [1410, 1830, "banderas", { titulo: "banderas" }],
      [1830, 1910, "calma", { titulo: "banderas_fin" }],
      [1910, 2070, "premios", { titulo: "premios" }],
      [2070, 2430, "cangrejos", { titulo: "cangrejos2" }],
      [2430, 2510, "calma", { titulo: "acuario_t" }],
      [2510, 2650, "mixto", { densidad: 0.5 }],
      [2650, 2810, "rampa", { titulo: "rampa" }],
      [2810, 3140, "mixto", { densidad: 0.55, titulo: "" }],
      [3140, 3290, "sprint", { titulo: "sprint_mchenry" }],
    ],
    control: 1870, caja: 1990,
    interior: { rango: [1412, 1828], tipo: "banderas", aire: true, sinEdificios: [1400, 1840] },
    sinEdificios: [3260, 4000],
    chapas: [[150, "carril"], [1250, "carril"], [2950, "arco"]],
    hitos: ["torre_reloj_bal", "casas_formstone", "acuario"],
    meta: "fuerte_mchenry", metaNombre: { es: "el fuerte McHenry", en: "Fort McHenry" },
    izquierda: [
      40, ["kit", 2], 14, ["torre_reloj_bal", 1], 14, ...cuadras(3), ["casas_formstone", 1], 14, ...cuadras(5), ["acuario", 1], 14, ...cuadras(14),
    ],
    derecha: [
      40, ["kit", 3], 14, ...cuadras(2), ["acuario", 1], 14, ...cuadras(4), ["casas_formstone", 1], 14, ...cuadras(5), ["torre_reloj_bal", 1], 14, ...cuadras(12),
    ],
    fondo: [{ pieza: "fuerte_mchenry", d: 3330, centro: true },
      { pieza: "arco_harbor", d: 120, cruza: true }, { pieza: "arco_harbor", d: 2470, cruza: true },
      { pieza: "muelle_harbor", d: 1410, cruza: true }],
    final: "parada", parada: 6,
    camaraFinal: { pos: [5, 3, 12], mira: [0, 14, -40] },
    acera: ["baltimore/banco_baltimore", "ciudad/farola_ciudad", "ciudad/arbol_ciudad", "ciudad/farola_ciudad"],
  },
  {
    // 15/11/2026: nivel 42: Wilmington (blender/wilmington.py). Acto del
    // Sentido Comun. «El pueblo de su rival dormilon: mecedoras y helados por
    // la calle». Recomendado: Market Street por la mañana, mecedoras en las
    // aceras, y final en la estacion de Wilmington. Dinamicas propias: las
    // gallinas azules de Delaware (se apartan si las ves venir por su carril:
    // hay que meterse en el ultimo momento) y el momento estrella, la torre
    // de helado en el paseo de Rehoboth (cada bola se apila y la torre se
    // tambalea al cambiar de carril y al saltar). Pancarta: EL HELADO SE DERRITE.
    id: "wilmington", nombre: "Market Street", lugar: "Wilmington, Delaware", listo: true,
    zona: "city", carpeta: "wilmington", luz: "manana", semilla: 1845,
    largo: 3300, linea: 11.5, velMax: 25,
    potenciadores: ["magnet", "shield", "boost", "mega", "botas"],
    kit: { minPlantas: 1, maxPlantas: 4, estilo: "wilmington" },
    horizonte: "wilmington",
    obstaculos: { low: ["cucurucho_caido", "mecedora_obst", "valla_metal"], high: ["cartel_de", "pancarta"],
      full: ["camion_helados", "pickup", "furgoneta", "autocaravana"] },
    publico: { personas: ["turista", "fan", "chico", "senora", "abuelo"], valla: "banderas", cada: 2 },
    tramos: [
      [0, 70, "calma", { titulo: "wilmington" }],
      [70, 250, "mixto", { densidad: 0.45, titulo: "market_wil" }],
      [250, 610, "gallinas", { titulo: "gallinas" }],
      [610, 690, "calma", { titulo: "opera" }],
      [690, 850, "slalom", { full: ["camion_helados", "pickup", "furgoneta"], titulo: "helados_camion" }],
      [850, 930, "calma"],
      [930, 1090, "vallas", { low: ["cucurucho_caido", "mecedora_obst"], high: ["cartel_de"], titulo: "derrite" }],
      [1090, 1170, "calma"],
      [1170, 1330, "mixto", { densidad: 0.5, momento: "reto", titulo: "reto" }],
      [1330, 1410, "calma", { titulo: "entrada_paseo" }],
      [1410, 1830, "helados", { titulo: "helados" }],
      [1830, 1910, "calma", { titulo: "helados_fin" }],
      [1910, 2070, "premios", { titulo: "premios" }],
      [2070, 2430, "gallinas", { titulo: "gallinas2" }],
      [2430, 2510, "calma", { titulo: "mecedoras" }],
      [2510, 2650, "mixto", { densidad: 0.5 }],
      [2650, 2810, "rampa", { titulo: "rampa" }],
      [2810, 3140, "mixto", { densidad: 0.55, titulo: "" }],
      [3140, 3290, "sprint", { titulo: "sprint_estacion_wil" }],
    ],
    control: 1870, caja: 1990,
    interior: { rango: [1412, 1828], tipo: "helados", aire: true, sinEdificios: [1400, 1840] },
    sinEdificios: [3260, 4000],
    chapas: [[150, "carril"], [1250, "carril"], [2950, "arco"]],
    hitos: ["opera_wilmington", "heladeria", "casa_mecedoras"],
    meta: "estacion_wilmington", metaNombre: { es: "la estación de Wilmington", en: "Wilmington Station" },
    izquierda: [
      40, ["kit", 2], 14, ["opera_wilmington", 1], 14, ...cuadras(3), ["heladeria", 1], 14, ...cuadras(5), ["casa_mecedoras", 1], 14, ...cuadras(14),
    ],
    derecha: [
      40, ["kit", 3], 14, ...cuadras(2), ["casa_mecedoras", 1], 14, ...cuadras(4), ["heladeria", 1], 14, ...cuadras(5), ["opera_wilmington", 1], 14, ...cuadras(12),
    ],
    fondo: [{ pieza: "estacion_wilmington", d: 3330, centro: true },
      { pieza: "arco_first_state", d: 120, cruza: true }, { pieza: "arco_first_state", d: 2470, cruza: true },
      { pieza: "paseo_rehoboth", d: 1410, cruza: true }],
    final: "parada", parada: 6,
    camaraFinal: { pos: [5, 3, 12], mira: [0, 14, -40] },
    acera: ["wilmington/mecedora", "ciudad/farola_ciudad", "ciudad/arbol_ciudad", "wilmington/mecedora"],
  },
  {
    // 15/11/2026: nivel 43: Filadelfia (blender/filadelfia.py). Acto del
    // Sentido Comun. «La Campana de la Libertad. Se pone en la freidora de un
    // McDonald's, como hizo de verdad». Recomendado: Market Street por la
    // tarde, y final en el Salon de la Independencia con la Campana. Dinamicas
    // propias: la freidora (las cestas se doran al acercarse, cada una a su
    // ritmo: coger la que llegue dorada) y el momento estrella, la Casa de la
    // Moneda por dentro (las prensas golpean en cadena: pasar por el carril
    // que este arriba). Pancarta: LA CAMPANA YA ESTA ROTA.
    id: "filadelfia", nombre: "Market Street", lugar: "Filadelfia, Pensilvania", listo: true,
    zona: "city", carpeta: "filadelfia", luz: "tarde", semilla: 1846,
    largo: 3300, linea: 11.5, velMax: 25,
    potenciadores: ["magnet", "shield", "boost", "mega", "botas"],
    kit: { minPlantas: 2, maxPlantas: 6, estilo: "filadelfia" },
    horizonte: "filadelfia",
    obstaculos: { low: ["pretzel_gigante", "barricada", "valla_metal"], high: ["cartel_pa", "pancarta"],
      full: ["autobus_septa", "pickup", "furgoneta", "autocaravana"] },
    publico: { personas: ["turista", "fan", "chico", "senora", "abuelo"], valla: "banderas", cada: 2 },
    tramos: [
      [0, 70, "calma", { titulo: "filadelfia" }],
      [70, 250, "mixto", { densidad: 0.45, titulo: "market_phl" }],
      [250, 610, "freidora", { titulo: "freidora" }],
      [610, 690, "calma", { titulo: "ayuntamiento_phl" }],
      [690, 850, "slalom", { full: ["autobus_septa", "pickup", "furgoneta"], titulo: "autobuses_phl" }],
      [850, 930, "calma"],
      [930, 1090, "vallas", { low: ["pretzel_gigante", "valla_metal"], high: ["cartel_pa"], titulo: "campana_rota" }],
      [1090, 1170, "calma"],
      [1170, 1330, "mixto", { densidad: 0.5, momento: "reto", titulo: "reto" }],
      [1330, 1410, "calma", { titulo: "entrada_moneda" }],
      [1410, 1830, "prensas", { titulo: "prensas" }],
      [1830, 1910, "calma", { titulo: "prensas_fin" }],
      [1910, 2070, "premios", { titulo: "premios" }],
      [2070, 2430, "freidora", { titulo: "freidora2" }],
      [2430, 2510, "calma", { titulo: "rocky" }],
      [2510, 2650, "mixto", { densidad: 0.5 }],
      [2650, 2810, "rampa", { titulo: "rampa" }],
      [2810, 3140, "mixto", { densidad: 0.55, titulo: "" }],
      [3140, 3290, "sprint", { titulo: "sprint_independencia" }],
    ],
    control: 1870, caja: 1990,
    interior: { rango: [1412, 1828], tipo: "prensas", aire: true, sinEdificios: [1400, 1840] },
    sinEdificios: [3260, 4000],
    chapas: [[150, "carril"], [1250, "carril"], [2950, "arco"]],
    hitos: ["ayuntamiento_philly", "museo_arte", "freiduria"],
    meta: "salon_independencia", metaNombre: { es: "el Salón de la Independencia", en: "Independence Hall" },
    izquierda: [
      40, ["kit", 2], 14, ["ayuntamiento_philly", 1], 14, ...cuadras(3), ["museo_arte", 1], 14, ...cuadras(5), ["freiduria", 1], 14, ...cuadras(14),
    ],
    derecha: [
      40, ["kit", 3], 14, ...cuadras(2), ["freiduria", 1], 14, ...cuadras(4), ["museo_arte", 1], 14, ...cuadras(5), ["ayuntamiento_philly", 1], 14, ...cuadras(12),
    ],
    fondo: [{ pieza: "salon_independencia", d: 3330, centro: true },
      { pieza: "arco_philly", d: 120, cruza: true }, { pieza: "arco_philly", d: 2470, cruza: true },
      { pieza: "casa_moneda_int", d: 1410, cruza: true }],
    final: "parada", parada: 6,
    camaraFinal: { pos: [5, 3, 12], mira: [0, 14, -40] },
    acera: ["filadelfia/carrito_pretzel", "ciudad/farola_ciudad", "ciudad/arbol_ciudad", "ciudad/farola_ciudad"],
  },
  {
    // 15/11/2026: nivel 44: Atlantic City (blender/atlanticcity.py). Acto del
    // Sentido Comun. «Sus casinos arruinados: con el hasta la banca pierde.
    // Fichas rodando». Recomendado: el Boardwalk al atardecer, y final en el
    // casino arruinado de las cupulas (CERRADO). Dinamicas propias: las
    // tragaperras sobre la calle (tocar para parar los tres rodillos: BOOM
    // pone fichas en ese carril, TACO pone tacos, tres iguales premio) y el
    // momento estrella, el blackjack en el casino (coger cartas por carril y
    // plantarse antes de pasarse de 21). Pancarta: LA BANCA SIEMPRE GANA.
    id: "atlantic_city", nombre: "El Boardwalk", lugar: "Atlantic City, Nueva Jersey", listo: true,
    zona: "city", carpeta: "atlanticcity", luz: "atardecer", semilla: 1847,
    largo: 3300, linea: 11.5, velMax: 25,
    potenciadores: ["magnet", "shield", "boost", "mega", "botas"],
    kit: { minPlantas: 3, maxPlantas: 7, estilo: "atlanticcity" },
    horizonte: "atlanticcity",
    obstaculos: { low: ["ficha_gigante", "barricada", "valla_metal"], high: ["cartel_nj", "pancarta"],
      full: ["jitney", "pila_fichas", "pickup", "furgoneta"] },
    publico: { personas: ["turista", "fan", "chico", "senora", "abuelo"], valla: "banderas", cada: 2 },
    tramos: [
      [0, 70, "calma", { titulo: "atlantic_city" }],
      [70, 250, "mixto", { densidad: 0.45, titulo: "boardwalk" }],
      [250, 610, "tragaperras", { titulo: "tragaperras" }],
      [610, 690, "calma", { titulo: "boardwalk_hall" }],
      [690, 850, "slalom", { full: ["jitney", "pila_fichas", "pickup"], titulo: "jitneys" }],
      [850, 930, "calma"],
      [930, 1090, "vallas", { low: ["ficha_gigante", "valla_metal"], high: ["cartel_nj"], titulo: "banca" }],
      [1090, 1170, "calma"],
      [1170, 1330, "mixto", { densidad: 0.5, momento: "reto", titulo: "reto" }],
      [1330, 1410, "calma", { titulo: "entrada_casino" }],
      [1410, 1830, "blackjack", { titulo: "blackjack" }],
      [1830, 1910, "calma", { titulo: "blackjack_fin" }],
      [1910, 2070, "premios", { titulo: "premios" }],
      [2070, 2430, "tragaperras", { titulo: "tragaperras2" }],
      [2430, 2510, "calma", { titulo: "lucy" }],
      [2510, 2650, "mixto", { densidad: 0.5 }],
      [2650, 2810, "rampa", { titulo: "rampa" }],
      [2810, 3140, "mixto", { densidad: 0.55, titulo: "" }],
      [3140, 3290, "sprint", { titulo: "sprint_casino" }],
    ],
    control: 1870, caja: 1990,
    interior: { rango: [1412, 1828], tipo: "blackjack", aire: true, sinEdificios: [1400, 1840] },
    sinEdificios: [3260, 4000],
    chapas: [[150, "carril"], [1250, "carril"], [2950, "arco"]],
    hitos: ["boardwalk_hall", "steel_pier", "lucy_elefanta"],
    meta: "casino_arruinado", metaNombre: { es: "el casino arruinado", en: "the bankrupt casino" },
    izquierda: [
      40, ["kit", 2], 14, ["boardwalk_hall", 1], 14, ...cuadras(3), ["steel_pier", 1], 14, ...cuadras(5), ["lucy_elefanta", 1], 14, ...cuadras(14),
    ],
    derecha: [
      40, ["kit", 3], 14, ...cuadras(2), ["lucy_elefanta", 1], 14, ...cuadras(4), ["steel_pier", 1], 14, ...cuadras(5), ["boardwalk_hall", 1], 14, ...cuadras(12),
    ],
    fondo: [{ pieza: "casino_arruinado", d: 3330, centro: true },
      { pieza: "arco_boardwalk", d: 120, cruza: true }, { pieza: "arco_boardwalk", d: 2470, cruza: true },
      { pieza: "casino_floor", d: 1410, cruza: true }],
    final: "parada", parada: 6,
    camaraFinal: { pos: [5, 3, 12], mira: [0, 14, -40] },
    acera: ["atlanticcity/tragaperras_acera", "ciudad/farola_ciudad", "ciudad/banco", "ciudad/farola_ciudad"],
  },
  {
    // 15/11/2026: nivel 45: Hartford (blender/hartford.py). Acto del Sentido
    // Comun. «La capital de los seguros: ninguno le cubre los tropezones».
    // Recomendado: Main Street en otoño, y final en el Capitolio de
    // Connecticut con la cupula de oro. Dinamicas propias: la valla de Tom
    // Sawyer (por el carril de la orilla se pinta la valla; al final, tacos
    // segun lo pintado) y el momento estrella, el tiovivo del parque Bushnell
    // (en el caballito, que sube y baja, tocar cuando pasa la anilla dorada a
    // la altura de la mano). Pancarta: LEE LA LETRA PEQUEÑA.
    id: "hartford", nombre: "Farmington Ave · Main St", lugar: "Hartford, Connecticut", listo: true,
    zona: "city", carpeta: "hartford", luz: "otono", semilla: 1848,
    // 27/11/2026: Isidro: «más riguroso con el realismo de las calles, dónde
    // está cada cosa». El recorrido de verdad, medido en OpenStreetMap, metro a
    // metro (3,5 km): de la casa de Mark Twain por Farmington Avenue (la
    // catedral de San José a la izquierda y, enfrente, la sede de Aetna) y
    // Asylum Street hasta Main Street; giro a la derecha en el antiguo
    // Capitolio (la T de Asylum St) y por Main Street, en su acera este el
    // antiguo Capitolio, la torre Travelers, el Atheneum, el ayuntamiento y la
    // biblioteca; en la oeste, el cementerio de 1640 y Center Church frente a
    // la torre. Giro a la derecha a Elm Street (Main Street sigue recta), con
    // el parque Bushnell a la derecha (alli, el tiovivo), hasta el Capitolio.
    // Cada calle que cruza esta en su sitio y con su nombre.
    largo: 3630, linea: 11.5, velMax: 25,
    potenciadores: ["magnet", "shield", "boost", "mega", "botas"],
    kit: { minPlantas: 2, maxPlantas: 6, estilo: "hartford" },
    horizonte: "hartford",
    obstaculos: { low: ["cubo_volcado", "barricada", "valla_metal"], high: ["cartel_ct", "pancarta"],
      full: ["furgon_seguros", "pickup", "furgoneta", "autocaravana"] },
    publico: { personas: ["turista", "fan", "chico", "senora", "abuelo"], valla: "banderas", cada: 2 },
    tramos: [
      [0, 70, "calma", { titulo: "twain" }],
      [70, 250, "mixto", { densidad: 0.45, titulo: "hartford" }],
      [250, 610, "mixto", { densidad: 0.5 }],
      [610, 790, "mixto", { densidad: 0.55 }],
      [790, 880, "calma", { titulo: "catedral_sj" }],
      [880, 1210, "slalom", { full: ["furgon_seguros", "pickup", "furgoneta"], titulo: "seguros" }],
      [1210, 1290, "calma", { titulo: "main_hfd" }],
      [1290, 1450, "vallas", { low: ["cubo_volcado", "valla_metal"], high: ["cartel_ct"], titulo: "letra_pequena" }],
      [1450, 1530, "calma"],
      [1530, 1690, "mixto", { densidad: 0.5, momento: "reto", titulo: "reto" }],
      [1690, 1770, "calma"],
      [1770, 1930, "premios", { titulo: "premios" }],
      [1930, 2290, "mixto", { densidad: 0.55 }],
      [2290, 2500, "mixto", { densidad: 0.5 }],
      // 27/11: los momentos de verdad. La Carta del Roble (1687) por Main
      // Street desde el antiguo Capitolio (alli estaba la casa de reuniones).
      [2500, 2860, "carta_roble", { titulo: "carta_roble" }],
      [2860, 3070, "calma", { titulo: "entrada_carrusel" }],
      [3070, 3320, "carrusel", { momento: "vehiculo", vehiculo: "caballito", titulo: "carrusel" }],
      [3320, 3360, "calma", { titulo: "carrusel_fin" }],
      // El maraton de Hartford llega al parque Bushnell por Trinity St (3.545).
      [3360, 3625, "maraton", { titulo: "maraton" }],
    ],
    control: 1730, caja: 1850,
    interior: { rango: [3072, 3318], tipo: "carrusel", aire: true, sinEdificios: [3060, 3330] },
    sinEdificios: [3590, 4000],
    chapas: [[150, "carril"], [1600, "carril"], [2870, "arco"]],
    hitos: ["catedral_san_jose", "old_state_house", "torre_seguros"],
    meta: "capitolio_ct", metaNombre: { es: "el Capitolio de Connecticut", en: "the Connecticut Capitol" },
    girosReales: [{ d: 2459, lado: 1, calle: "Main St" }, { d: 2989, lado: 1, calle: "Elm St", sigue: true }],
    nombresCruces: {"176":"Gillett St","217":"Forest St","326":"Marshall St","436":"Laurel St","580":"Imlay St","722":"Sigourney St","1198":"Flower St","1363":"Broad St","1490":"Asylum Ave","1530":"Garden St","1679":"Spruce St","1750":"Union Pl","1846":["High St","Ford St"],"2046":"Ann Uccello St","2133":"Haynes St","2244":"Trumbull St","2459":"Main St","2540":["Central Row","Pearl St"],"2733":"Gold St","2907":["Arch St","Wells St"],"2989":["Sheldon St","Elm St"],"3545":"Trinity St"},
    izquierda: [
      ["kit", 1], ["kit", 1], ["kit", 1], ["kit", 1], ["kit", 1], ["kit", 1], ["kit", 1,{ ancho: 11 }], 14, ["kit", 1], ["kit", 1], ["kit", 1],
      ["kit", 1], ["kit", 1], ["kit", 1,{ ancho: 28 }], 14, ["kit", 1], ["kit", 1], ["kit", 1], ["kit", 1,{ ancho: 14 }], 14, ["kit", 1], ["kit", 1],
      ["kit", 1], ["kit", 1], ["kit", 1], ["kit", 1], ["kit", 1], ["kit", 1], ["kit", 1], ["kit", 1,{ ancho: 32 }], 14, ["kit", 1], ["kit", 1],
      ["kit", 1], ["kit", 1,{ ancho: 34 }], ["catedral_san_jose", 1], ["kit", 1], ["kit", 1], ["kit", 1], ["kit", 1], ["kit", 1], ["kit", 1],
      ["kit", 1], ["kit", 1], ["kit", 1], ["kit", 1], ["kit", 1], ["kit", 1], ["kit", 1], ["kit", 1], ["kit", 1], ["kit", 1], ["kit", 1,{ ancho: 41 }],
      14, ["kit", 1], ["kit", 1], ["kit", 1], ["kit", 1,{ ancho: 29 }], 14, ["kit", 1], ["kit", 1,{ ancho: 8 }], 14, ["kit", 1], ["kit", 1],
      ["kit", 1], ["kit", 1], ["kit", 1], ["kit", 1,{ ancho: 27 }], 14, ["kit", 1], ["kit", 1,{ ancho: 17 }], 14, ["kit", 1], ["kit", 1],
      ["kit", 1,{ ancho: 18 }], 14, ["kit", 1], ["kit", 1], ["kit", 1], ["kit", 1], ["kit", 1], ["kit", 1], ["kit", 1], ["kit", 1,{ ancho: 26 }], 14,
      ["kit", 1], ["kit", 1], ["kit", 1], ["kit", 1], ["kit", 1], ["kit", 1], ["kit", 1], ["kit", 1,{ ancho: 28 }], 14, ["kit", 1], ["kit", 1],
      ["kit", 1], ["kit", 1], ["kit", 1], ["kit", 1], ["kit", 1], ["kit", 1], ["kit", 1,{ ancho: 15 }], 14, ["kit", 1,{ ancho: 19 }],
      ["old_state_house", 1], ["kit", 1,{ ancho: 22 }], 14, ["kit", 1], ["kit", 1], ["kit", 1], ["kit", 1], ["kit", 1,{ ancho: 9 }],
      ["torre_seguros", 1], ["kit", 1], ["kit", 1], ["kit", 1], ["kit", 1,{ ancho: 20 }], ["atheneum", 1], ["kit", 1], ["kit", 1],
      ["kit", 1,{ ancho: 11 }], ["ayuntamiento_hfd", 1], 1, 14, ["kit", 1], ["kit", 1,{ ancho: 9 }], ["biblioteca_hfd", 1], 7, 19, ["kit", 1],
      ["kit", 1], ["kit", 1], ["kit", 1], ["kit", 1], ["kit", 1], ["kit", 1], ["kit", 1], ["kit", 1], ["kit", 1], ["kit", 1], ["kit", 1], ["kit", 1],
      ["kit", 1], ["kit", 1], ["kit", 1], ["kit", 1], ["kit", 1], ["kit", 1], ["kit", 1,{ ancho: 15 }], 14,
    ],
    derecha: [
      ["kit", 1], ["kit", 1], ["kit", 1,{ ancho: 17 }], ["casa_mark_twain", 1], ["kit", 1], ["kit", 1], ["kit", 1], ["kit", 1], ["kit", 1],
      ["kit", 1,{ ancho: 9 }], 14, ["kit", 1], ["kit", 1], ["kit", 1], ["kit", 1], ["kit", 1], ["kit", 1], ["kit", 1], ["kit", 1,{ ancho: 13 }], 14,
      ["kit", 1], ["kit", 1], ["kit", 1], ["kit", 1], ["kit", 1], ["kit", 1,{ ancho: 22 }], 14, ["kit", 1], ["kit", 1], ["kit", 1], ["kit", 1],
      ["kit", 1], ["kit", 1,{ ancho: 10 }], 14, ["kit", 1], ["kit", 1], ["kit", 1], ["kit", 1], ["kit", 1], ["kit", 1], ["kit", 1], ["kit", 1],
      ["kit", 1], ["kit", 1,{ ancho: 22 }], ["aetna", 1], ["kit", 1], ["kit", 1,{ ancho: 12 }], 14, ["kit", 1], ["kit", 1], ["kit", 1], ["kit", 1],
      ["kit", 1], ["kit", 1], ["kit", 1,{ ancho: 17 }], 14, ["kit", 1], ["kit", 1], ["kit", 1], ["kit", 1], ["kit", 1], ["kit", 1], ["kit", 1],
      ["kit", 1], ["kit", 1], ["kit", 1], ["kit", 1], ["kit", 1], ["kit", 1], ["kit", 1], ["kit", 1], ["kit", 1], ["kit", 1], ["kit", 1],
      ["kit", 1,{ ancho: 25 }], 14, ["kit", 1], ["kit", 1], ["kit", 1], ["kit", 1], ["kit", 1], ["kit", 1], ["kit", 1], ["kit", 1], ["kit", 1],
      ["kit", 1,{ ancho: 29 }], 14, ["kit", 1], ["kit", 1], ["kit", 1], ["kit", 1,{ ancho: 13 }], 14, ["kit", 1], ["kit", 1], ["kit", 1], ["kit", 1],
      ["kit", 1], ["kit", 1], ["kit", 1,{ ancho: 39 }], 14, ["kit", 1], ["kit", 1], ["kit", 1,{ ancho: 29 }], 14, ["kit", 1], ["kit", 1], ["kit", 1],
      ["kit", 1], ["kit", 1,{ ancho: 14 }], ["cementerio_antiguo", 1], ["center_church", 1], ["kit", 1], ["kit", 1,{ ancho: 9 }], 14, ["kit", 1],
      ["kit", 1], ["kit", 1], ["kit", 1], ["kit", 1,{ ancho: 22 }], 14, ["kit", 1], ["kit", 1], ["kit", 1,{ ancho: 10 }], 14, 5,
      ["parque_bushnell", 25],
    ],
    fondo: [{ pieza: "capitolio_ct", d: 3660, centro: true },
      { pieza: "carrusel_bushnell", d: 3070, cruza: true }],
    final: "parada", parada: 6,
    camaraFinal: { pos: [5, 3, 12], mira: [0, 14, -40] },
    acera: ["hartford/cubo_pintura", "ciudad/farola_ciudad", "ciudad/arbol_ciudad", "ciudad/farola_ciudad"],
  },
  {
    // 16/11/2026: nivel 46: Burlington (blender/burlington.py). Acto del
    // Sentido Comun. «Helados y un senador con guantes de lana que lo critica
    // todo». Recomendado: Church Street en otoño, y final en la iglesia de
    // ladrillo de lo alto de la calle. En la acera, el senador gruñón con sus
    // manoplas y su cartel ¡TODO MAL!. Dinamicas propias: los montones de
    // hojas (cayendo encima se rebota al siguiente, en cadena) y el momento
    // estrella, el paseo sobre el lago Champlain, donde asoma Champ, el
    // monstruo del lago (hacerle fotos desde el carril de su lado).
    // Pancarta: NADA ES GRATIS.
    id: "burlington", nombre: "Church Street", lugar: "Burlington, Vermont", listo: true,
    zona: "city", carpeta: "burlington", luz: "otono", semilla: 1865,
    largo: 3300, linea: 11.5, velMax: 25,
    potenciadores: ["magnet", "shield", "boost", "mega", "botas"],
    kit: { minPlantas: 2, maxPlantas: 4, estilo: "burlington" },
    horizonte: "burlington",
    obstaculos: { low: ["garrafa_arce", "calabazas", "valla_metal"], high: ["cartel_vt", "pancarta"],
      full: ["camion_leche", "tractor", "pickup", "furgoneta"] },
    publico: { personas: ["turista", "fan", "chico", "senora", "abuelo"], valla: "banderas", cada: 2 },
    tramos: [
      [0, 70, "calma", { titulo: "burlington" }],
      [70, 250, "mixto", { densidad: 0.45, titulo: "church_st" }],
      [250, 610, "hojas", { titulo: "hojas" }],
      [610, 690, "calma", { titulo: "ayto_btv" }],
      [690, 850, "slalom", { full: ["camion_leche", "tractor", "pickup"], titulo: "lecheros" }],
      [850, 930, "calma"],
      [930, 1090, "vallas", { low: ["garrafa_arce", "calabazas"], high: ["cartel_vt"], titulo: "gratis" }],
      [1090, 1170, "calma"],
      [1170, 1330, "mixto", { densidad: 0.5, momento: "reto", titulo: "reto" }],
      [1330, 1410, "calma", { titulo: "entrada_champlain" }],
      [1410, 1830, "champ", { titulo: "champ" }],
      [1830, 1910, "calma", { titulo: "champ_fin" }],
      [1910, 2070, "premios", { titulo: "premios" }],
      [2070, 2430, "hojas", { titulo: "hojas2" }],
      [2430, 2510, "calma", { titulo: "heladeria" }],
      [2510, 2650, "mixto", { densidad: 0.5 }],
      [2650, 2810, "rampa", { titulo: "rampa" }],
      [2810, 3140, "mixto", { densidad: 0.55, titulo: "" }],
      [3140, 3290, "sprint", { titulo: "sprint_iglesia" }],
    ],
    control: 1870, caja: 1990,
    interior: { rango: [1412, 1828], tipo: "champlain", aire: true, sinEdificios: [1400, 1840] },
    sinEdificios: [3260, 4000],
    chapas: [[150, "carril"], [1250, "carril"], [2950, "arco"]],
    hitos: ["ayuntamiento_btv", "heladeria_vaca", "granero_rojo"],
    meta: "iglesia_unitaria", metaNombre: { es: "la iglesia de Church Street", en: "the Church Street church" },
    izquierda: [
      40, ["kit", 2], 14, ["ayuntamiento_btv", 1], 14, ...cuadras(3), ["heladeria_vaca", 1], 14, ...cuadras(5), ["granero_rojo", 1], 14, ...cuadras(14),
    ],
    derecha: [
      40, ["kit", 3], 14, ...cuadras(2), ["granero_rojo", 1], 14, ...cuadras(4), ["heladeria_vaca", 1], 14, ...cuadras(5), ["ayuntamiento_btv", 1], 14, ...cuadras(12),
    ],
    fondo: [{ pieza: "iglesia_unitaria", d: 3330, centro: true },
      { pieza: "puente_cubierto", d: 120, cruza: true }, { pieza: "puente_cubierto", d: 2470, cruza: true },
      { pieza: "senador_manoplas", d: 760, cruza: true, x: -6.4 },
      { pieza: "causeway_champlain", d: 1410, cruza: true }],
    final: "parada", parada: 6,
    camaraFinal: { pos: [5, 3, 12], mira: [0, 14, -40] },
    acera: ["burlington/arce_cubo", "ciudad/farola_ciudad", "ciudad/banco", "ciudad/farola_ciudad"],
  },
  {
    // 16/11/2026: nivel 47: Portland, Maine (blender/portlandme.py). Acto del
    // Sentido Comun. «Langostas». Recomendado: el Old Port por la mañana, y
    // final en el faro de Portland Head. Dinamicas propias: la medida de la
    // langosta (solo valen las medianas; las pequeñas y las gigantes, multa;
    // la azul, premio) y el momento estrella, la costa en la niebla (no se ve
    // casi nada: el haz del faro marca lo que viene con luces de colores).
    // Pancarta: SI HAY NIEBLA, VE DESPACIO.
    id: "portland_me", nombre: "Old Port", lugar: "Portland, Maine", listo: true,
    zona: "city", carpeta: "portlandme", luz: "manana", semilla: 1786,
    largo: 3300, linea: 11.5, velMax: 25,
    potenciadores: ["magnet", "shield", "boost", "mega", "botas"],
    kit: { minPlantas: 2, maxPlantas: 5, estilo: "portlandme" },
    horizonte: "portlandme",
    obstaculos: { low: ["boya_suelta", "barricada", "valla_metal"], high: ["cartel_me", "pancarta"],
      full: ["camion_langostas", "pickup", "furgoneta"] },
    publico: { personas: ["turista", "fan", "chico", "senora", "abuelo"], valla: "banderas", cada: 2 },
    tramos: [
      [0, 70, "calma", { titulo: "portland_me" }],
      [70, 250, "mixto", { densidad: 0.45, titulo: "old_port" }],
      [250, 610, "medida", { titulo: "medida" }],
      [610, 690, "calma", { titulo: "observatorio" }],
      [690, 850, "slalom", { full: ["camion_langostas", "pickup", "furgoneta"], titulo: "langosteros" }],
      [850, 930, "calma"],
      [930, 1090, "vallas", { low: ["boya_suelta", "valla_metal"], high: ["cartel_me"], titulo: "niebla_sc" }],
      [1090, 1170, "calma"],
      [1170, 1330, "mixto", { densidad: 0.5, momento: "reto", titulo: "reto" }],
      [1330, 1410, "calma", { titulo: "entrada_faro" }],
      [1410, 1830, "faro", { titulo: "faro" }],
      [1830, 1910, "calma", { titulo: "faro_fin" }],
      [1910, 2070, "premios", { titulo: "premios" }],
      [2070, 2430, "medida", { titulo: "medida2" }],
      [2430, 2510, "calma", { titulo: "shack" }],
      [2510, 2650, "mixto", { densidad: 0.5 }],
      [2650, 2810, "rampa", { titulo: "rampa" }],
      [2810, 3140, "mixto", { densidad: 0.55, titulo: "" }],
      [3140, 3290, "sprint", { titulo: "sprint_faro" }],
    ],
    control: 1870, caja: 1990,
    interior: { rango: [1412, 1828], tipo: "faro", sinEdificios: [1400, 1840] },
    sinEdificios: [3260, 4000],
    chapas: [[150, "carril"], [1250, "carril"], [2950, "arco"]],
    hitos: ["observatorio_portland", "almacen_old_port", "casa_langostas"],
    meta: "faro_portland", metaNombre: { es: "el faro de Portland Head", en: "Portland Head Light" },
    izquierda: [
      40, ["kit", 2], 14, ["observatorio_portland", 1], 14, ...cuadras(3), ["almacen_old_port", 1], 14, ...cuadras(5), ["casa_langostas", 1], 14, ...cuadras(14),
    ],
    derecha: [
      40, ["kit", 3], 14, ...cuadras(2), ["casa_langostas", 1], 14, ...cuadras(4), ["almacen_old_port", 1], 14, ...cuadras(5), ["observatorio_portland", 1], 14, ...cuadras(12),
    ],
    fondo: [{ pieza: "faro_portland", d: 3330, centro: true },
      { pieza: "arco_old_port", d: 120, cruza: true }, { pieza: "arco_old_port", d: 2470, cruza: true },
      { pieza: "costa_niebla", d: 1410, cruza: true }],
    final: "parada", parada: 6,
    camaraFinal: { pos: [5, 3, 12], mira: [0, 14, -40] },
    acera: ["portlandme/nasas_apiladas", "ciudad/farola_ciudad", "ciudad/banco", "ciudad/farola_ciudad"],
  },
  {
    // 16/11/2026: nivel 48: Manchester (blender/manchester.py). Acto del
    // Sentido Comun. «La primera nevada. El lema del estado: Vive libre o
    // muere». Recomendado: Elm Street con la primera nevada (luz de
    // invierno), y final en los molinos de Amoskeag. Dinamicas propias: la
    // guerra de bolas de nieve (los niños asoman de sus fuertes y tiran: la
    // sombra dice donde cae; tocando a tiempo les das tu primero) y el
    // momento estrella, las promesas imposibles de las primarias (el otro
    // candidato las lanza desde su atril; tocar justo al llegar la devuelve).
    // Pancarta: ABRÍGATE, QUE NIEVA.
    id: "manchester", nombre: "Elm Street", lugar: "Manchester, Nuevo Hampshire", listo: true,
    zona: "city", carpeta: "manchester", luz: "invierno", semilla: 1846,
    largo: 3300, linea: 11.5, velMax: 25,
    potenciadores: ["magnet", "shield", "boost", "mega", "botas"],
    kit: { minPlantas: 2, maxPlantas: 5, estilo: "manchester" },
    horizonte: "manchester",
    obstaculos: { low: ["monton_nieve", "barricada", "valla_metal"], high: ["cartel_nh", "pancarta"],
      full: ["quitanieves", "munieco_nieve", "pickup", "furgoneta"] },
    publico: { personas: ["turista", "fan", "chico", "senora", "abuelo"], valla: "banderas", cada: 2 },
    tramos: [
      [0, 70, "calma", { titulo: "manchester" }],
      [70, 250, "mixto", { densidad: 0.45, titulo: "elm_st" }],
      [250, 610, "guerra", { titulo: "bolas_nieve" }],
      [610, 690, "calma", { titulo: "palace" }],
      [690, 850, "slalom", { full: ["quitanieves", "pickup", "furgoneta"], titulo: "quitanieves_mht" }],
      [850, 930, "calma"],
      [930, 1090, "vallas", { low: ["monton_nieve", "valla_metal"], high: ["cartel_nh"], titulo: "abrigate" }],
      [1090, 1170, "calma"],
      [1170, 1330, "mixto", { densidad: 0.5, momento: "reto", titulo: "reto" }],
      [1330, 1410, "calma", { titulo: "entrada_promesas" }],
      [1410, 1830, "promesas", { titulo: "promesas" }],
      [1830, 1910, "calma", { titulo: "promesas_fin" }],
      [1910, 2070, "premios", { titulo: "premios" }],
      [2070, 2430, "guerra", { titulo: "bolas_nieve2" }],
      [2430, 2510, "calma", { titulo: "diner" }],
      [2510, 2650, "mixto", { densidad: 0.5 }],
      [2650, 2810, "rampa", { titulo: "rampa" }],
      [2810, 3140, "mixto", { densidad: 0.55, titulo: "" }],
      [3140, 3290, "sprint", { titulo: "sprint_molinos" }],
    ],
    control: 1870, caja: 1990,
    interior: { rango: [1412, 1828], tipo: "plato", sinEdificios: [1400, 1840] },
    sinEdificios: [3260, 4000],
    chapas: [[150, "carril"], [1250, "carril"], [2950, "arco"]],
    hitos: ["teatro_palace", "city_hall_mht", "diner_flecha"],
    meta: "molinos_amoskeag", metaNombre: { es: "los molinos de Amoskeag", en: "the Amoskeag Mills" },
    izquierda: [
      40, ["kit", 2], 14, ["teatro_palace", 1], 14, ...cuadras(3), ["city_hall_mht", 1], 14, ...cuadras(5), ["diner_flecha", 1], 14, ...cuadras(14),
    ],
    derecha: [
      40, ["kit", 3], 14, ...cuadras(2), ["diner_flecha", 1], 14, ...cuadras(4), ["city_hall_mht", 1], 14, ...cuadras(5), ["teatro_palace", 1], 14, ...cuadras(12),
    ],
    fondo: [{ pieza: "molinos_amoskeag", d: 3330, centro: true },
      { pieza: "arco_libre", d: 120, cruza: true }, { pieza: "arco_libre", d: 2470, cruza: true },
      { pieza: "estudio_debate", d: 1410, cruza: true }],
    final: "parada", parada: 6,
    camaraFinal: { pos: [5, 3, 12], mira: [0, 14, -40] },
    acera: ["manchester/muneco_acera", "ciudad/farola_ciudad", "ciudad/banco", "ciudad/farola_ciudad"],
  },
  {
    // 16/11/2026: nivel 49: Providence (blender/providence.py). Acto del
    // Sentido Comun. «El estado mas pequeño y el nivel mas corto. El dice que
    // es enorme, tremendo». Recomendado: Westminster Street al atardecer (los
    // braseros de WaterFire en la acera) y final en el Capitolio de marmol con
    // el Hombre Independiente. El nivel mas corto: 2300 m. Dinamicas propias:
    // encogido (por debajo de las pancartas se pasa solo y, deslizandote, por
    // debajo de los coches; el bicho azul no) y el momento estrella, el examen
    // de la Universidad de Brown (preguntas sobre Rhode Island: se contesta
    // pasando bajo la pizarra buena). Pancarta: LO PEQUEÑO TAMBIÉN VALE.
    id: "providence", nombre: "Westminster Street", lugar: "Providence, Rhode Island", listo: true,
    zona: "city", carpeta: "providence", luz: "atardecer", semilla: 1636,
    largo: 2300, linea: 11.5, velMax: 25,
    potenciadores: ["magnet", "shield", "boost", "mega", "botas"],
    kit: { minPlantas: 2, maxPlantas: 5, estilo: "providence" },
    horizonte: "providence",
    obstaculos: { low: ["barricada", "valla_metal"], high: ["cartel_ri", "pancarta"],
      full: ["bicho_azul", "pickup", "taxi"] },
    publico: { personas: ["turista", "fan", "chico", "senora", "abuelo"], valla: "banderas", cada: 2 },
    tramos: [
      [0, 70, "calma", { titulo: "providence" }],
      [70, 220, "mixto", { densidad: 0.45, titulo: "westminster" }],
      [220, 520, "mini", { titulo: "mini" }],
      [520, 600, "calma", { titulo: "arcade" }],
      [600, 740, "vallas", { low: ["barricada", "valla_metal"], high: ["cartel_ri"], titulo: "pequeno" }],
      [740, 820, "calma", { titulo: "entrada_brown" }],
      [820, 1180, "examen", { titulo: "examen" }],
      [1180, 1260, "calma", { titulo: "examen_fin" }],
      [1260, 1400, "premios", { titulo: "premios" }],
      [1400, 1700, "mini", { titulo: "mini2" }],
      [1700, 1780, "calma", { titulo: "superman" }],
      [1780, 1940, "rampa", { titulo: "rampa" }],
      [1940, 2140, "mixto", { densidad: 0.55, titulo: "" }],
      [2140, 2290, "sprint", { titulo: "sprint_capitolio_ri" }],
    ],
    control: 1240, caja: 1300,
    interior: { rango: [822, 1178], tipo: "brown", aire: true, sinEdificios: [810, 1190] },
    sinEdificios: [2260, 3100],
    chapas: [[150, "carril"], [1300, "carril"], [2000, "arco"]],
    hitos: ["bicho_azul_edificio", "arcade_ri", "torre_superman"],
    meta: "capitolio_ri", metaNombre: { es: "el Capitolio de Rhode Island", en: "the Rhode Island State House" },
    izquierda: [
      40, ["kit", 2], 14, ["bicho_azul_edificio", 1], 14, ...cuadras(3), ["arcade_ri", 1], 14, ...cuadras(5), ["torre_superman", 1], 14, ...cuadras(14),
    ],
    derecha: [
      40, ["kit", 3], 14, ...cuadras(2), ["torre_superman", 1], 14, ...cuadras(4), ["arcade_ri", 1], 14, ...cuadras(5), ["bicho_azul_edificio", 1], 14, ...cuadras(12),
    ],
    fondo: [{ pieza: "capitolio_ri", d: 2330, centro: true },
      { pieza: "arco_federal_hill", d: 120, cruza: true }, { pieza: "arco_federal_hill", d: 1480, cruza: true },
      { pieza: "patio_brown", d: 820, cruza: true }],
    final: "parada", parada: 6,
    camaraFinal: { pos: [5, 3, 12], mira: [0, 14, -40] },
    acera: ["providence/brasero_acera", "ciudad/farola_ciudad", "ciudad/banco", "ciudad/farola_ciudad"],
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
    // 06/11: Isidro: «se hacen repetitivos los obstaculos, faltan mas tipos y mas
    // dinamismo». Nuevos: microfonos de la prensa, la barrera del control (sube
    // y baja), el dron de la tele, la furgoneta de las Fake News (cambia de
    // carril) y el turista en Segway (cruza la calle).
    obstaculos: { low: ["valla_metal", "cajas", "microfonos", "barrera_control"], high: ["protesta", "dron_tele"],
      full: ["agentes", "furgoneta", "guardaespaldas", "furgoneta_fake", "segway"] },
    publico: { personas: ["ejecutivo", "fan", "turista", "senora", "ejecutivo"], valla: "verja", cada: 2 },
    // 05/11: Isidro: «los primeros niveles deben ser mas cortos y luego ir
    // alargandose» y «los niveles se siguen sintiendo muy iguales». Antes los
    // seis median 3,2 km y seguian el mismo orden casi en los mismos metros.
    // Washington sigue en 3.300 m (es el final de la gira), con otro orden.
    // 06/11 (3): Isidro: «más cosas, muchas más, que no sea tan repetitivo».
    // Un momento cada 20 s más o menos (ver «Los momentos» en world.js); el
    // largo del nivel no cambia.
    tramos: [
      [0, 40, "calma", { titulo: "pennsylvania" }],
      // 07/11: el momento estrella: dentro del Capitolio (donde se jura el
      // cargo) y de ahi, por Pennsylvania Avenue, la comitiva. Las piezas, en `fondo`.
      [40, 208, "capitolio", { titulo: "capitolio" }],
      [208, 330, "comitiva", { titulo: "comitiva" }],
      [330, 480, "mixto", { densidad: 0.5, momento: "gorras", titulo: "gorras" }],
      [480, 640, "rampa", { titulo: "rampa" }],
      [640, 800, "alfombra", { titulo: "alfombra" }],
      [800, 900, "festin", { potenciador: "rocket", titulo: "cohete" }],
      [900, 1100, "autobuses", { titulo: "autobuses" }],
      [1100, 1250, "lluvia", { titulo: "lluvia" }],
      [1250, 1450, "vallas", { high: ["protesta", "dron_tele"], titulo: "protesta" }],
      [1450, 1600, "premios", { titulo: "premios" }],
      [1600, 1680, "calma"],
      // 09/11: el jefe final es el Monstruo del Pantano (todos los jefes juntos).
      [1680, 2400, "jefe", { jefe: "pantano", titulo: "jefe_final" }],
      [2400, 2550, "festin", { potenciador: "freeze", titulo: "hielo" }],
      [2550, 2750, "slalom", { full: ["agentes", "furgoneta", "furgoneta_fake", "segway"], momento: "vehiculo", vehiculo: "limusina", titulo: "sube_limusina" }],
      [2750, 2860, "desfile_cruza", { cruzan: ["segway"], titulo: "cruzan_segways" }],
      // (El reto, unos 10 s a la velocidad de aqui: 210 m.)
      [2860, 3070, "mixto", { densidad: 0.5, momento: "reto", titulo: "reto" }],
      [3070, 3270, "sprint", { titulo: "sprint_dc" }],
    ],
    control: 1612, caja: 1150,
    // 07/11: el Capitolio por dentro (la rotonda es mas ancha que la calle: sin edificios).
    interior: { rango: [40, 208], tipo: "capitolio", sinEdificios: true },
    // (La primera, despues de la rampa: en la alfombra la cortaba.)
    chapas: [[610, "arco"], [1100, "bus"], [2751, "carril"]],
    hitos: ["archivos_portico", "fbi", "irs", "correos_torre", "willard", "tesoro"],
    meta: "casa_blanca_final", metaNombre: { es: "la Casa Blanca", en: "the White House" }, coche: "suv",
    // Hacia el oeste: el sur queda a la izquierda y el norte a la derecha.
    // 26/10: los monumentos de verdad en su sitio, sus fachadas en tramos
    // cortos con patios entre medias, y el resto edificios unicos del kit
    // (FED: piedra clara y frontones, como los ministerios del Triangulo Federal).
    // (11/11: empiezan al salir del Capitolio; antes las primeras quedaban
    // dentro de la rotonda, donde no hay edificios, y no se veian.)
    izquierda: [
      212,
      ["galeria_este", 1], 18,
      ["kit", 8, FED], 18,                                                      // Galeria Nacional
      ["archivos_ala", 5], ["archivos_portico", 1], ["archivos_ala", 5], 18,     // 7th - 9th
      ["justicia", 8], 10, ["justicia", 8], 18, ["kit", 5, FED], 18,                                // 9th - 10th
      ["irs", 8], ["kit", 4, FED], ["irs", 8], 12,                              // 10th - 12th
      ["kit", 3, FED], ["correos", 5], ["correos_torre", 1], ["correos", 5], 18,  // 12th
      ["reagan", 8], ["kit", 5, FED], ["reagan", 8], 10, ["kit", 4, FED], 18,     // 12th - 14th
      ["kit", 6, FED], 18, ["kit", 3, FED], ["wilson", 1], 18,                                      // 14th
      ["kit", 2, FED], ["pershing", 1],
    ],
    derecha: [
      212,
      ["canada", 1], 18, ["cristal", 1], 18,                                    // 4th - 6th
      ["kit", 5], 18, ["navy", 1], ["kit", 5], 18,                             // 7th - 9th
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
      { pieza: "capitolio_fachada", d: 40, cruza: true },
      ...[50, 80].map((d) => ({ pieza: "capitolio_pasillo", d, cruza: true })),
      { pieza: "capitolio_rotonda", d: 110, cruza: true },
      ...[140, 170].map((d) => ({ pieza: "capitolio_pasillo", d, cruza: true })),
      { pieza: "capitolio_salida", d: 200, cruza: true },
      { pieza: "casa_blanca_final", d: 3340, centro: true },
    ],
    // Mobiliario de la acera (este si se repite: farolas y arboles, como en la calle de verdad).
    acera: ["dc/farola", "pueblo/roble"],
  },
];

// 05/11: el objeto de cada ciudad (Isidro: «que no todo sean tacos»). Diez
// por nivel, repartidos por la calle; cogerlos todos da un premio en tacos.
export const OBJETOS = { providence: "bicho", manchester: "gorro", portland_me: "langosta", burlington: "manopla", hartford: "brocha", atlantic_city: "dado", filadelfia: "campana", wilmington: "helado", baltimore: "cangrejo", richmond: "tarta", charleston_wv: "pico", los_angeles: "estrella", honolulu: "coco", anchorage: "pepita", portland_or: "rosa", seattle: "cafe", salt_lake: "gelatina", boise: "patata", billings: "huella", cheyenne: "sombrero", denver: "esquis", albuquerque: "globo", charleston_sc: "pina", miami: "flamenco", atlanta: "melocoton", charlotte: "rueda", nashville: "guitarra", louisville: "herradura", nueva_orleans: "collar", birmingham: "rotulador", little_rock: "diamante", jackson: "pajita", houston: "casco", oklahoma: "gota", rushmore: "cincel", fargo: "orejeras", nueva_york: "manzana", pueblo: "bandera", phoenix: "placa", vegas: "ficha", des_moines: "maiz", omaha: "filete", wichita: "zapato", san_luis: "etiqueta", indianapolis: "cuadros", detroit: "sirope", chicago: "laca", milwaukee: "queso", minneapolis: "patin", washington: "voto" };
export const OBJETOS_POR_NIVEL = 10, PREMIO_OBJETOS = 300;
// Los metros de cada uno: repartidos a partes iguales por los tramos que
// valen (fuera del tutorial, del jefe, del festin y del sprint final).
export function sitiosObjetos(nivel) {
  if (!OBJETOS[nivel.id] || !nivel.tramos) return [];
  // 06/11 (3): tampoco en los momentos que cambian la calle (rampa, convoy...).
  const trozos = nivel.tramos.filter(([, , tipo]) => !["tutorial", "jefe", "festin", "sprint", "rampa", "convoy", "premios", "alfombra", "lluvia", "jefe_paso", "metro_vias", "metro_techo", "banderas", "baldosas", "circuito", "puente_canada", "giro", "viento", "basura", "hockey", "recuento", "rebufo", "ovalo", "calesas", "golf", "globos", "platillo", "bolas", "esqui", "estampida", "rodeo", "osos", "arreo", "patata", "aizkolari", "espejismo", "record", "chaparron", "pescado", "ranas", "regata", "cheque", "vuelo", "leis", "surf", "siesta", "rodaje", "carbon", "vias", "minas", "desfile", "cangrejos", "banderas", "gallinas", "helados", "freidora", "prensas", "tragaperras", "blackjack", "valla", "carrusel", "carta_roble", "maraton", "hojas", "champ", "medida", "faro", "guerra", "promesas", "mini", "examen"].includes(tipo))
    .map(([a, b]) => [a + 15, b - 15]).filter(([a, b]) => b > a);
  const total = trozos.reduce((s, [a, b]) => s + b - a, 0);
  const salida = [];
  for (let i = 0; i < OBJETOS_POR_NIVEL; i++) {
    let resto = ((i + 0.5) / OBJETOS_POR_NIVEL) * total;
    for (const [a, b] of trozos) {
      if (resto <= b - a) { salida.push(a + resto); break; }
      resto -= b - a;
    }
  }
  return salida;
}

// Las 51 paradas de la historia, con la calle de las que ya existen.
// (`jefe` de la historia pasa a `esJefe`: el jefe de verdad es el tramo «jefe».)
export const NIVELES = PARADAS.map(({ jefe, ...p }) => {
  const calle = CALLES.find((c) => c.id === p.id);
  return calle ? { ...calle, ...p, esJefe: jefe, objeto: OBJETOS[p.id] } : { ...p, esJefe: jefe, listo: false };
});

// 26/11/2026: Isidro: «hay muchos niveles muy repetitivos, falta dinamismo».
// Casi todos los niveles seguian la misma plantilla y el tramo «mixto» sin
// nada propio (el de despues de la alfombra) era igual en todas partes. Ahora,
// en cada ciudad, ese tramo es uno con movimiento, distinto del de la ciudad
// anterior (sale de su semilla: en cada partida es el mismo): el camion que
// pierde la carga (nuevo), las obras con los carriles cortados, la policia que
// viene de frente, los repartidores en bici o la comitiva de coches oficiales.
const DINAMICOS = ["mudanza", "obras", "persecucion", "repartidores", "comitiva"];
{
  let previo = null;
  for (const nv of NIVELES) {
    if (!nv.tramos || nv.id === "nueva_york" || nv.id === "washington") continue;
    const az = azarConSemilla(nv.semilla * 31 + 5);
    const libres = nv.tramos.filter(([a, b, tipo, o]) => tipo === "mixto" && !(o && (o.momento || o.titulo)) && b - a >= 120);
    for (const tr of libres.slice(0, 2)) {
      const opciones = DINAMICOS.filter((x) => x !== previo);
      const tipo = opciones[Math.floor(az() * opciones.length)];
      tr[2] = tipo;
      tr[3] = { ...(tr[3] || {}), titulo: tipo };
      previo = tipo;
    }
  }
}

// Ancho de cada pieza a lo largo de la calle (el de su fachada, sin contar lo
// que sobresale la cornisa: asi los tramos encajan sin pisarse).
export const ANCHO = {
  archivos_ala: 20, archivos_portico: 34, justicia: 20, irs: 20, correos: 20, correos_torre: 30,
  reagan: 20, wilson: 40, pershing: 40, canada: 30, cristal: 30, navy: 40, fbi: 20, willard: 35,
  galeria_este: 40, tesoro: 60, casa_blanca_final: 76,
  // 07/11: el metro de Nueva York
  metro_boca: 8, metro_tunel: 24, metro_estacion: 30, metro_salida: 8,
  banderas_arco: 2, casino_entrada: 8, casino_sala: 30, casino_salida: 8,
  capitolio_fachada: 10, capitolio_pasillo: 30, capitolio_rotonda: 30, capitolio_salida: 8,
  feria_entrada: 4, feria_puestos: 30, feria_puestos_b: 30, feria_noria: 2,
  canon_corte: 30, canon_puente: 30,
  // 08/11: Omaha
  first_national: 30, woodmen: 30, old_market: 40, orpheum: 30, union_station: 90, corrales_entrada: 2, corrales: 30,
  // 08/11: Wichita
  epic_center: 30, century_ii: 40, museo_aviacion: 30, guardian_llanuras: 90, tornado_embudo: 2,
  // 08/11: San Luis
  old_courthouse: 30, busch_stadium: 40, union_station_stl: 30, arco_gateway: 100, super_entrada: 8, super_pasillo: 30, super_salida: 8,
  // 08/11: Indianápolis
  soldiers_monument: 30, statehouse_in: 40, lucas_oil: 40, jw_marriott: 30, grada: 30, circuito_entrada: 34, meta_indy: 80,
  // 08/11: Detroit
  spirit_detroit: 30, guardian_building: 30, fox_theatre: 30, puno_joe_louis: 20, ren_cen: 100, torre_ambassador: 4,
  puente_amb_0: 30, puente_amb_1: 30, puente_amb_2: 30, puente_amb_3: 30, puente_amb_4: 30, puente_amb_5: 30,
  // 08/11: Chicago
  hancock: 40, water_tower: 30, tribune_tower: 30, wrigley_building: 30, trump_chicago: 40, puente_dusable: 60, cloud_gate: 100,
  // 09/11: Milwaukee
  gesu_church: 30, germania: 42, city_hall_mke: 42, pfister_hotel: 32, us_bank_center: 40, puente_mke: 50, museo_calatrava: 100,
  // 09/11: Minneapolis
  // 12/11: Monte Rushmore y Fargo
  hotel_alex_johnson: 32, dino_park: 48, wall_drug: 28, pinar: 30, agujas_granito: 26, tunel_roca: 16, avenida_banderas: 34, monte_rushmore: 120,
  bank_of_america_hou: 35, jpmorgan_hou: 36, city_hall_hou: 40, saturno_v: 70, independence_plaza: 80, hangar_luna: 420,
  capitolio_ar: 78, clinton_library: 54, old_state_house: 40, river_market: 37, mina: 420,
  capitolio_ms: 82, old_capitol_ms: 35, casa_blues: 21, barco_vapor: 420,
  catedral_sl: 70, casa_criolla: 19, cafe_du_monde: 22, superdome: 64, arco_carnaval: 4, golfo_america: 2,
  vulcano: 52, sloss_hornos: 42, alabama_theatre: 23, magic_city: 2, fundicion: 420,
  partenon: 40, ryman: 32, batman_building: 27, honky_tonk: 21, arco_broadway: 2, opry: 420,
  churchill_downs: 60, slugger_museum: 28, destileria: 26, pollo_frito: 18, arco_derby: 2, hipodromo: 420,
  fox_theatre: 48, capitolio_georgia: 46, torre_piramide: 26, westin_cilindro: 28, mural_ficha: 22, arco_melocoton: 2, recuento: 420,
  fuente_pina: 24, rainbow_row: 40, san_miguel: 22, mercado_charleston: 26, casa_battery: 30, arco_charleston: 2, campo_golf: 420,
  molinos_amoskeag: 90, teatro_palace: 20, city_hall_mht: 22, diner_flecha: 20, arco_libre: 2, estudio_debate: 420,
  capitolio_ri: 90, bicho_azul_edificio: 18, arcade_ri: 22, torre_superman: 22, arco_federal_hill: 2, patio_brown: 360,
  iglesia_unitaria: 90, ayuntamiento_btv: 28, heladeria_vaca: 14, granero_rojo: 26, puente_cubierto: 12, senador_manoplas: 2, causeway_champlain: 420,
  faro_portland: 90, observatorio_portland: 12, almacen_old_port: 26, casa_langostas: 14, arco_old_port: 2, costa_niebla: 420,
  casino_arruinado: 80, boardwalk_hall: 46, steel_pier: 18, lucy_elefanta: 30, arco_boardwalk: 2, casino_floor: 420,
  capitolio_ct: 90, torre_seguros: 24, casa_mark_twain: 24, catedral_san_jose: 60, aetna: 148, old_state_house: 26, arco_soldados: 2, carrusel_bushnell: 250,
  g_fox: 28, cheney_building: 28, center_church: 20, cementerio_antiguo: 26, atheneum: 34, ayuntamiento_hfd: 38,
  biblioteca_hfd: 32, butler_mccook: 26, bushnell_teatro: 38, parque_bushnell: 24,
  estacion_wilmington: 80, opera_wilmington: 24, heladeria: 16, casa_mecedoras: 18, arco_first_state: 2, paseo_rehoboth: 420,
  salon_independencia: 80, ayuntamiento_philly: 42, museo_arte: 40, freiduria: 16, arco_philly: 2, casa_moneda_int: 420,
  capitolio_va: 90, estacion_main_st: 38, departamento_guerra: 36, teatro_byrd: 20, arco_desfile: 2, desfile_monument: 420,
  fuerte_mchenry: 90, torre_reloj_bal: 16, casas_formstone: 26, acuario: 34, arco_harbor: 2, muelle_harbor: 420,
  teatro_chino: 80, capitol_records: 22, el_capitan: 22, hotel_roosevelt: 32, arco_san_fermin: 2, plato_cine: 420,
  capitolio_wv: 90, daniel_boone_hotel: 26, panaderia_pepperoni: 16, tipple_carbon: 24, arco_wv: 2, patio_carbon: 420,
  estacion_alaska: 80, teatro_4th: 22, cabana_troncos: 18, hotel_captain_cook: 30, arco_iditarod: 2, vuelo_chugach: 420,
  palacio_iolani: 80, aloha_tower: 18, royal_hawaiian: 44, capitolio_hawaii: 38, arco_aloha: 2, playa_waikiki: 420,
  space_needle: 80, mercado_pike: 32, smith_tower: 24, biblioteca_seattle: 36, monorail: 160, mercado_pescado: 420,
  white_stag: 70, powells: 36, portland_building: 32, union_station_pdx: 40, arco_rosas: 2, rio_willamette: 420,
  capitolio_idaho: 90, boise_depot: 40, egyptian_theatre: 22, casa_vasca: 36, arco_vasco: 2, plaza_aizkolari: 420,
  capitolio_utah: 96, city_county_slc: 44, depot_slc: 46, beehive_house: 24, eagle_gate: 2, salar_bonneville: 420,
  capitolio_wyoming: 80, cheyenne_depot: 44, plains_hotel: 26, big_boy: 46, arco_cheyenne: 2, arena_rodeo: 420,
  rims_billings: 120, billings_depot: 40, first_interstate: 32, moss_mansion: 28, skypoint: 12, pradera_arreo: 420,
  capitolio_colorado: 76, torre_daniels: 14, union_station_den: 50, oso_azul: 40, arco_denver: 2, pista_esqui: 420,
  san_felipe_neri: 60, kimo_theatre: 22, casa_adobe: 20, motel_66: 30, arco_66: 2, campo_globos: 420,
  mar_a_lago: 60, hotel_deco_rosa: 22, hotel_deco_azul: 22, playa_socorrista: 40, arco_miami: 2, bano_dorado: 420,
  salon_fama: 54, torre_corona: 26, torre_led: 24, iglesia_presbiteriana: 18, garaje_carreras: 24, arco_carrera: 2, speedway: 420,
  devon_tower: 34, cristal_bridge: 46, bricktown: 40, skydance: 8, capitolio_ok: 72,
  fargo_theatre: 26, hotel_donaldson: 25, black_building: 26, radisson_fargo: 30, np_depot: 42,
  ids_center: 36, foshay_tower: 30, wells_fargo_mpls: 34, city_hall_mpls: 46, basilica_mary: 44, lago_helado: 440, cuchara_cereza: 100,
  // Nueva York
  torre_trump: 30, st_regis: 30, peninsula: 30, santo_tomas: 28, catedral: 60, rockefeller: 60,
  saks: 40, biblioteca: 60, empire: 40, madison: 40, flatiron: 32,
  // Findlay
  courier: 24, heladeria: 20, deposito_agua: 20, davis: 20, marathon: 40, juzgado_final: 62,
  // Phoenix
  san_carlos: 30, westward_ho: 30, biblioteca_barr: 40, museo_arte: 40, museo_heard: 40, diner_final: 30,
  // Las Vegas
  cartel_vegas: 10, piramide: 60, castillo: 48, fuentes: 58, cesar: 44, torre_eiffel: 40, noria: 44,
  campanile: 50, hotel_trump: 44,
  // Des Moines (el rio y las pasarelas cruzan la calle: su ancho es a lo largo)
  parque_esculturas: 60, biblioteca_dm: 40, torre_801: 36, ruan: 30, hotel_fort: 30, world_food: 44,
  arena: 60, rio: 40, skywalk: 4, capitolio_iowa: 80,
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

// 25/11/2026: el modo Esqui (esqui2d.js): la bajada de las Rocosas al
// Capitolio de Colorado, de lado, como contenido que se desbloquea al
// superar Denver. Siempre la misma ladera (la semilla de Denver), sin punto
// de control; los tacos que se cogen van a la hucha.
export const ESQUI = { nivel: "denver", largo: 2400, semilla: 1832, objeto: "esquis",
  metaNombre: { es: "el Capitolio de Colorado", en: "the Colorado Capitol" } };
export function esquiAbierto(superados) {
  return !!superados[ESQUI.nivel];
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
        // (27/11: `ancho` en las opciones: para que los de verdad caigan en su metro)
        const ancho = (opciones && opciones.ancho) || [18, 20, 22, 24, 26, 40][Math.floor(a() * 6)];
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
// 27/11/2026: Isidro: «quiero mejorar de una vez los giros en las calles; solo
// quiero que el personaje gire por ellas sin hacer una transicion». En el
// desvio se gira de verdad (world.js, doblarMundo) a una calle como la de
// siempre: de fachada a fachada, 2 x (linea + 0,5). En el lado del giro se abre
// ese hueco: los del kit se recortan y los modelados se apartan (empujando a
// los de al lado). En el otro lado, los que llegan a la esquina de enfrente se
// quedan con la calle vieja (`preGiro`: no giran con la calle nueva).
function abrirGiros(nivel, salida) {
  const W = (nivel.linea || 11.5) + 0.5;
  for (const g of nivel.giros || []) {
    const a = g.d - W, b = g.d + W;
    for (const lado of [-1, 1]) {
      const fila = salida.filter((e) => e.lado === lado && !e.cruza && !e.centro && !e.arco).sort((x, y) => x.d - y.d);
      if (lado !== g.lado) {
        for (const e of fila) if (e.d < b - 0.5 && e.d + e.ancho > g.d) { e.preGiro = g.d; g.finPre = Math.max(g.finPre || 0, e.d + e.ancho); }
        continue;
      }
      let tope = a;
      for (const e of fila.filter((x) => x.d < g.d).reverse()) {
        if (e.d + e.ancho <= tope) break;
        if (e.pieza !== "kit") { e.d = tope - e.ancho; tope = e.d; continue; }
        if (e.d <= tope - 8) { e.ancho = tope - e.d; break; }
        e.quitar = true;
      }
      tope = b;
      for (const e of fila.filter((x) => x.d >= g.d)) {
        if (e.d >= tope) break;
        if (e.pieza !== "kit") { e.d = tope; tope = e.d + e.ancho; continue; }
        const fin = e.d + e.ancho;
        if (fin >= tope + 8) { e.d = tope; e.ancho = fin - tope; break; }
        e.quitar = true;
      }
    }
  }
  for (let i = salida.length - 1; i >= 0; i--) if (salida[i].quitar) salida.splice(i, 1);
}
export function colocarNivel(nivel, anchoDe) {
  const salida = [];
  const { quitar } = crucesDeNivel(nivel);
  recorrerLado(nivel, nivel.izquierda, -1, anchoDe, (e) => salida.push(e));
  recorrerLado(nivel, nivel.derecha, 1, anchoDe, (e) => { if (!(e.pieza === "kit" && quitar.has(e.d))) salida.push(e); });
  abrirGiros(nivel, salida);
  // (`cruza`: de lado a lado de la calle, como el puente o las pasarelas de Des Moines)
  for (const f of nivel.fondo || []) salida.push({ pieza: f.pieza, d: f.d, lado: f.lado || 0, centro: !!f.centro, cruza: !!f.cruza, x: f.x || 0, giro: !!f.giro, ancho: anchoDe(f.pieza) });
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
  // 08/11 (2): cada calle lateral es un cruce de verdad (ver crucesDeNivel).
  for (const c of crucesDeNivel(nivel).cruces) {
    // (27/11: `nombresCruces`: el nombre de verdad de cada calle, { metro: "Laurel St" },
    // o [la de la izquierda, la de la derecha] si cambia de nombre al cruzar)
    const nombre = Object.entries(nivel.nombresCruces || {}).find(([d]) => Math.abs(d - c.d) < 4);
    salida.push({ tipo: "cruce", d: c.d, lados: c.lados, cuatro: c.cuatro, n: c.n, nombre: nombre && nombre[1], giro: (nivel.giros || []).find((g) => g.d === c.d) || null });
  }
  const azar = azarConSemilla(nivel.semilla + 7);
  for (let x = 30; x < nivel.largo - 40; x += 45 + azar() * 25) {
    salida.push({ tipo: "tapa", d: x, x: (azar() < 0.5 ? -1 : 1) * 3.1 });
  }
  // 31/10: la calle con mas detalle. Parches de asfalto, manchas de aceite y
  // charcos (en Phoenix no: es el desierto). Pocos y de poco contraste, para
  // que al pasar por debajo no hagan rayas que parpadeen.
  const az = azarConSemilla(nivel.semilla + 13);
  const seco = !!(nivel.kit && nivel.kit.desierto);
  for (let x = 60; x < nivel.largo - 60; x += 55 + az() * 60) {
    salida.push({ tipo: "parche", d: x, x: (az() - 0.5) * 3.6, ancho: 1.6 + az() * 2.2, largo: 2.5 + az() * 4, giro: (az() - 0.5) * 0.3, v: Math.floor(az() * 3) });
  }
  for (let x = 45; x < nivel.largo - 60; x += 35 + az() * 50) {
    salida.push({ tipo: "mancha", d: x, x: [-2.2, 0, 2.2][Math.floor(az() * 3)] + (az() - 0.5) * 0.6, r: 0.5 + az() * 0.6 });
  }
  if (!seco) {
    for (let x = 120; x < nivel.largo - 80; x += 110 + az() * 120) {
      const borde = az() < 0.7;
      salida.push({ tipo: "charco", d: x, x: borde ? (az() < 0.5 ? -1 : 1) * 2.75 : (az() - 0.5) * 3, r: 0.9 + az() * 0.9 });
    }
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

// ---- Cruces y desvios (08/11/2026) ----
// Isidro: «falta que tenga sentido la carretera, hay coches que se cruzan donde
// no hay carreteras, añade algun cruce, y haz que el personaje tenga que
// cambiar a otra carretera de vez en cuando».
// Antes habia un paso de cebra en cada hueco de la acera izquierda y por alli
// cruzaban coches aunque enfrente hubiera un edificio. Ahora cada hueco de 12 m
// o mas es una calle lateral con su asfalto (world.js, hacerCruce). Cuando los
// huecos de los dos lados coinciden es un cruce de cuatro; y, de cada dos
// huecos de la izquierda, se abre tambien la calle a la derecha quitando los
// edificios del kit que la tapaban. Solo en los cruces de cuatro cruzan coches.
// Nada de cruces en los interiores, donde no hay edificios, en los arcos y
// puentes del fondo, ni al salir o al llegar.
// Los tramos sin edificios de un nivel: uno ([a, b]) o varios ([[a, b], [c, d]]).
export const rangosSin = (x) => (!x ? [] : Array.isArray(x[0]) ? x : [x]);

export function crucesDeNivel(nivel, anchoDe = (k) => ANCHO[k] || 20) {
  if (nivel._cruces) return nivel._cruces;
  const huecos = { [-1]: [], [1]: [] }, edif = { [-1]: [], [1]: [] };
  for (const lado of [-1, 1]) {
    recorrerLado(nivel, lado < 0 ? nivel.izquierda : nivel.derecha, lado, anchoDe,
      (e) => edif[lado].push(e), (d, h) => { if (h >= 12) huecos[lado].push([d, d + h]); });
  }
  const prohibido = [[-1e9, 50], [nivel.largo - 50, 1e9]];
  const ri = nivel.interior && nivel.interior.rango;
  if (ri) prohibido.push([ri[0] - 25, ri[1] + 25]);
  const si = nivel.interior && nivel.interior.sinEdificios;
  if (Array.isArray(si)) prohibido.push(si);
  for (const r of rangosSin(nivel.sinEdificios)) prohibido.push(r);
  for (const f of nivel.fondo || []) if (f.cruza || f.centro) prohibido.push([f.d - 20, f.d + (anchoDe(f.pieza) || 20) + 20]);
  if (nivel.control) prohibido.push([nivel.control - 12, nivel.control + 12]);
  const libre = (c) => !prohibido.some((r) => c - 7 < r[1] && c + 7 > r[0]);
  const cruces = [], quitar = new Set();
  let n = 0;
  for (const [a, b] of huecos[-1]) {
    const c = (a + b) / 2;
    if (!libre(c)) continue;
    const otro = huecos[1].find(([x, y]) => Math.min(b, y) - Math.max(a, x) >= 11);
    if (otro) { cruces.push({ d: (Math.max(a, otro[0]) + Math.min(b, otro[1])) / 2, lados: [-1, 1], cuatro: true }); continue; }
    // (27/11: no en los niveles hechos con el mapa: cada calle sale por donde sale)
    if (!nivel.nombresCruces && n++ % 2 === 0) {
      const tapan = edif[1].filter((e) => e.d < c + 6.5 && e.d + e.ancho > c - 6.5);
      if (tapan.length && tapan.every((e) => e.pieza === "kit")) {
        tapan.forEach((e) => quitar.add(e.d));
        cruces.push({ d: c, lados: [-1, 1], cuatro: true });
        continue;
      }
    }
    cruces.push({ d: c, lados: [-1], cuatro: false });
  }
  for (const [a, b] of huecos[1]) {
    const c = (a + b) / 2;
    if (!libre(c) || cruces.some((x) => Math.abs(x.d - c) < 16)) continue;
    cruces.push({ d: c, lados: [1], cuatro: false });
  }
  cruces.sort((x, y) => x.d - y.d);
  cruces.forEach((c, i) => { c.n = i + 1; });   // el numero de la calle (1st St, 2nd St...)
  nivel._cruces = { cruces, quitar };
  return nivel._cruces;
}

// Los desvios: dos por nivel (hacia el 35 % y el 70 %), en un cruce con calle
// hacia el lado del giro y dentro de un tramo tranquilo (sin momento). La
// calle de enfrente esta cortada por obras y hay que ponerse en el carril de
// ese lado; al llegar se gira a la otra calle (main.js pone el cartel verde
// con su nombre). El tramo «giro» va de 60 m antes del cruce a 25 m despues.
const TRAMOS_GIRO = ["mixto", "calma", "vallas", "slalom", "suave", "lluvia", "premios"];
export const CALLES_GIRO = {
  nueva_york: ["W 42nd St", "Madison Ave"], pueblo: ["Sandusky St", "Main Cross St"], phoenix: ["Van Buren St", "Washington St"],
  vegas: ["Flamingo Rd", "Tropicana Ave"], des_moines: ["Grand Ave", "Court Ave"], omaha: ["Dodge St", "Harney St"],
  wichita: ["Broadway", "William St"], san_luis: ["Olive St", "Washington Ave"], indianapolis: ["Washington St", "Capitol Ave"],
  detroit: ["Michigan Ave", "Jefferson Ave"], chicago: ["Rush St", "Wabash Ave"], milwaukee: ["Water St", "Jefferson St"], minneapolis: ["7th St", "Hennepin Ave"], rushmore: ["Mt Rushmore Rd", "Needles Hwy"], fargo: ["NP Ave", "Main Ave"], houston: ["Texas Ave", "NASA Pkwy"], oklahoma: ["Sheridan Ave", "Lincoln Blvd"], little_rock: ["Cumberland St", "Main St"], jackson: ["Farish St", "State St"], nueva_orleans: ["Royal St", "Canal St"], birmingham: ["Morris Ave", "1st Ave N"], nashville: ["2nd Ave", "Printers Alley"], louisville: ["4th St", "Bardstown Rd"], atlanta: ["Auburn Ave", "Edgewood Ave"], charleston_sc: ["King St", "Broad St"], miami: ["Collins Ave", "Washington Ave"], albuquerque: ["4th St", "Rio Grande Blvd"], denver: ["Larimer St", "Colfax Ave"], cheyenne: ["Pioneer Ave", "Lincolnway"], billings: ["N 27th St", "Broadway"], boise: ["Main St", "Grove St"], seattle: ["Pike St", "Pine St"], anchorage: ["E St", "5th Ave"], los_angeles: ["Vine St", "Highland Ave"], richmond: ["Main St", "Cary St"], wilmington: ["King St", "French St"], atlantic_city: ["Pacific Ave", "Atlantic Ave"], burlington: ["Main St", "Pearl St"], manchester: ["Hanover St", "Merrimack St"], providence: ["Dorrance St", "Mathewson St"], portland_me: ["Fore St", "Exchange St"], hartford: ["Asylum St", "Pearl St"], filadelfia: ["Broad St", "Chestnut St"], baltimore: ["Light St", "Charles St"], charleston_wv: ["Quarrier St", "Lee St"], honolulu: ["Lewers St", "Seaside Ave"], portland_or: ["Broadway", "SW 10th Ave"], salt_lake: ["South Temple", "200 S"], charlotte: ["Trade St", "4th St"], washington: ["15th St NW", "Constitution Ave"],
};
function aplicarGiros(nivel) {
  const { cruces } = crucesDeNivel(nivel);
  const lejos = [nivel.control, nivel.caja, ...(nivel.chapas || []).map(([d]) => d)].filter((x) => x != null);
  const giros = [];
  // 27/11/2026: los niveles hechos con el mapa de verdad (Hartford) traen sus
  // giros en sus esquinas: `girosReales: [{ d, lado, calle, muro, sigue }]`
  // (`muro`: el edificio que cierra la T, si es uno de verdad; `sigue`: no es
  // una T, la calle vieja sigue recta). Tienen que caer en un cruce (un hueco
  // de 12 m o mas en el lado del giro).
  for (const r of nivel.girosReales || []) {
    const c = cruces.find((x) => Math.abs(x.d - r.d) < 1 && x.lados.includes(r.lado));
    if (!c) { console.warn("giro sin cruce", nivel.id, r.d); continue; }
    giros.push({ d: c.d, lado: r.lado, n: giros.length, calle: r.calle, muro: r.muro, sigue: r.sigue });
  }
  for (const [f, pref] of nivel.girosReales ? [] : [[0.35, 1], [0.7, -1]]) {
    const objetivo = nivel.largo * f;
    const vale = cruces.filter((c) => {
      // (11/11: 65 m: con 45 la chapa del carril quedaba justo en la curva)
      if (Math.abs(c.d - objetivo) > nivel.largo * 0.2 || lejos.some((x) => Math.abs(x - c.d) < 65)) return false;
      if (nivel.__crucesAntes && !nivel.__crucesAntes.includes(c.d)) return false;
      if (giros.some((g) => Math.abs(g.d - c.d) < 300)) return false;
      const t = nivel.tramos.find(([a, b]) => c.d >= a && c.d < b);
      // (los momentos pequeños, el reto y las gorras, se acaban en el desvio)
      const op = t && t[3] || {};
      return t && TRAMOS_GIRO.includes(t[2]) && !op.vehiculo && (!op.momento || ["reto", "gorras"].includes(op.momento)) && c.d - 65 >= t[0] && c.d + 30 <= t[1];
    }).sort((a, b) => Math.abs(a.d - objetivo) - Math.abs(b.d - objetivo));
    const c = vale.find((x) => x.lados.includes(pref)) || vale[0];
    if (!c) continue;
    const lado = c.lados.includes(pref) ? pref : c.lados[0];
    giros.push({ d: c.d, lado, n: giros.length, calle: (CALLES_GIRO[nivel.id] || [])[giros.length] || `${c.n + 1}th St` });
  }
  for (const g of giros) {
    const i = nivel.tramos.findIndex(([a, b]) => g.d >= a && g.d < b);
    const [a, b, tipo, op] = nivel.tramos[i];
    const { titulo, momento, ...resto } = op || {};
    // (27/11: lo que quedaria de menos de 20 m a un lado, para el giro)
    const g0 = g.d - 60 - a < 20 ? a : g.d - 60, g1 = b - (g.d + 25) < 20 ? b : g.d + 25;
    nivel.tramos.splice(i, 1, ...[g0 > a ? [a, g0, tipo, op] : null,
      [g0, g1, "giro", { lado: g.lado, cruce: g.d }],   // (27/11: sin cartel: se gira solo)
      g1 < b ? [g1, b, tipo, resto] : null].filter(Boolean));
  }
  nivel.giros = giros;
}

// Piezas que hay que cargar para jugar un nivel (las de su calle, el fondo y la puerta).
export function piezasDeNivel(nivel) {
  const set = new Set();
  for (const lado of [nivel.izquierda, nivel.derecha]) for (const it of lado) if (Array.isArray(it)) set.add(it[0]);
  for (const f of nivel.fondo || []) set.add(f.pieza);
  for (const e of nivel.extras || []) set.add(e);      // piezas que van pegadas a otras (la rueda de la noria)
  if (nivel.carpeta === "washington") set.add("puerta_cb");
  set.delete("kit");   // los del kit van en su carpeta (ver usaKit)
  return [...set];
}
export function usaKit(nivel) {
  return [nivel.izquierda, nivel.derecha].some((lado) => lado.some((it) => Array.isArray(it) && it[0] === "kit"));
}

// 26/11/2026 (2): Isidro: «en casi todos los mapas, cuando llega justo al
// final, el mapa se ve como el suelo cargando, queda cutre». Al alargar los
// niveles a 3,3 km (05/11) las listas de edificios no se alargaron: en 36
// niveles los edificios se acababan 300-600 m antes de la meta y el final era
// una explanada gris y vacia. Ahora cada lado se completa hasta la plaza del
// edificio final con lo mismo que llevaba al final (manzanas del kit con su
// calle cada cuatro, o la avenida de banderas en Rushmore).
for (const nv of NIVELES) {
  if (!nv.izquierda || !nv.derecha) continue;
  const fin = (nv.fondo || []).find((f) => f.centro);
  let objetivo = Math.min(nv.largo + 15, fin ? fin.d - 15 : 1e9);
  for (const [a, b] of rangosSin(nv.sinEdificios)) if (a < objetivo && b >= objetivo) objetivo = a;
  const anchoDe = (k) => ANCHO[k] || 20;
  // (Los cruces del relleno no se usan para los desvios: el nivel se juega igual.)
  nv.__crucesAntes = crucesDeNivel(nv).cruces.map((c) => c.d);
  delete nv._cruces;
  for (const [lista, lado] of [[nv.izquierda, -1], [nv.derecha, 1]]) {
    const relleno = [...lista].reverse().find((x) => Array.isArray(x) && (x[0] === "kit" || x[1] >= 2));
    if (!relleno) continue;
    let seguidos = 0;
    for (let i = lista.length - 1; i >= 0 && Array.isArray(lista[i]); i--) seguidos += lista[i][1];
    for (let vueltas = 0; vueltas < 60; vueltas++) {
      if (recorrerLado(nv, lista, lado, anchoDe, () => {}) >= objetivo - 12) break;
      if (relleno[0] === "kit" && seguidos >= 4) { lista.push(14); seguidos = 0; continue; }
      lista.push(relleno[2] ? [relleno[0], 1, relleno[2]] : [relleno[0], 1]);
      seguidos++;
      // El ultimo no se mete en la plaza del final.
      if (recorrerLado(nv, lista, lado, anchoDe, () => {}) > objetivo + 4) { lista.pop(); break; }
    }
  }
}

// 08/11 (2): los desvios de cada nivel (aqui, cuando ya existe ANCHO).
for (const n of NIVELES) if (n.tramos && n.izquierda) aplicarGiros(n);
