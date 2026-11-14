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
export const OBJETOS = { nueva_orleans: "collar", birmingham: "rotulador", little_rock: "diamante", jackson: "pajita", houston: "casco", oklahoma: "gota", rushmore: "cincel", fargo: "orejeras", nueva_york: "manzana", pueblo: "bandera", phoenix: "placa", vegas: "ficha", des_moines: "maiz", omaha: "filete", wichita: "zapato", san_luis: "etiqueta", indianapolis: "cuadros", detroit: "sirope", chicago: "laca", milwaukee: "queso", minneapolis: "patin", washington: "voto" };
export const OBJETOS_POR_NIVEL = 10, PREMIO_OBJETOS = 300;
// Los metros de cada uno: repartidos a partes iguales por los tramos que
// valen (fuera del tutorial, del jefe, del festin y del sprint final).
export function sitiosObjetos(nivel) {
  if (!OBJETOS[nivel.id] || !nivel.tramos) return [];
  // 06/11 (3): tampoco en los momentos que cambian la calle (rampa, convoy...).
  const trozos = nivel.tramos.filter(([, , tipo]) => !["tutorial", "jefe", "festin", "sprint", "rampa", "convoy", "premios", "alfombra", "lluvia", "jefe_paso", "metro_vias", "metro_techo", "banderas", "baldosas", "circuito", "puente_canada", "giro", "viento", "basura", "hockey"].includes(tipo))
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
  const { quitar } = crucesDeNivel(nivel);
  recorrerLado(nivel, nivel.izquierda, -1, anchoDe, (e) => salida.push(e));
  recorrerLado(nivel, nivel.derecha, 1, anchoDe, (e) => { if (!(e.pieza === "kit" && quitar.has(e.d))) salida.push(e); });
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
    salida.push({ tipo: "cruce", d: c.d, lados: c.lados, cuatro: c.cuatro, n: c.n, giro: (nivel.giros || []).find((g) => g.d === c.d) || null });
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
    if (n++ % 2 === 0) {
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
  detroit: ["Michigan Ave", "Jefferson Ave"], chicago: ["Rush St", "Wabash Ave"], milwaukee: ["Water St", "Jefferson St"], minneapolis: ["7th St", "Hennepin Ave"], rushmore: ["Mt Rushmore Rd", "Needles Hwy"], fargo: ["NP Ave", "Main Ave"], houston: ["Texas Ave", "NASA Pkwy"], oklahoma: ["Sheridan Ave", "Lincoln Blvd"], little_rock: ["Cumberland St", "Main St"], jackson: ["Farish St", "State St"], nueva_orleans: ["Royal St", "Canal St"], birmingham: ["Morris Ave", "1st Ave N"], washington: ["15th St NW", "Constitution Ave"],
};
function aplicarGiros(nivel) {
  const { cruces } = crucesDeNivel(nivel);
  const lejos = [nivel.control, nivel.caja, ...(nivel.chapas || []).map(([d]) => d)].filter((x) => x != null);
  const giros = [];
  for (const [f, pref] of [[0.35, 1], [0.7, -1]]) {
    const objetivo = nivel.largo * f;
    const vale = cruces.filter((c) => {
      // (11/11: 65 m: con 45 la chapa del carril quedaba justo en la curva)
      if (Math.abs(c.d - objetivo) > nivel.largo * 0.2 || lejos.some((x) => Math.abs(x - c.d) < 65)) return false;
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
    nivel.tramos.splice(i, 1, [a, g.d - 60, tipo, op],
      [g.d - 60, g.d + 25, "giro", { lado: g.lado, cruce: g.d, titulo: g.lado > 0 ? "giro_der" : "giro_izq" }],
      [g.d + 25, b, tipo, resto]);
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

// 08/11 (2): los desvios de cada nivel (aqui, cuando ya existe ANCHO).
for (const n of NIVELES) if (n.tramos && n.izquierda) aplicarGiros(n);
