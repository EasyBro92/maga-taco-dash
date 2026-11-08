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
    interior: { rango: [772, 1082], tipo: "metro" },
    // (El helicoptero, fuera del metro.)
    helicoptero: [420, 1150],
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
    acera: ["ciudad/farola_ciudad", "ciudad/arbol_ciudad"],
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
      [860, 1060, "vallas", { high: ["arco_neon", "pinata"], titulo: "neones" }],
      [1060, 1220, "suave", { densidad: 0.55, momento: "vehiculo", vehiculo: "carrito_golf", titulo: "sube_golf" }],
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
      ...cuadras(5), ["museo_arte", 1], ["kit", 2], 14,
      ...cuadras(4), ["museo_heard", 1], ["kit", 2], 14,
      ...cuadras(2), ["kit", 2],
    ],
    fondo: [{ pieza: "diner_final", d: 2045, centro: true }],
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
      40, ["kit", 3], 14, ...cuadras(1), ["hotel_fort", 1], ["kit", 2], 14,
      ...cuadras(3), ["ruan", 1], ["kit", 2], 14,
      ...cuadras(6), ["kit", 1], ["world_food", 1], 68,
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
      [1680, 2400, "jefe", { titulo: "jefe_final" }],
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
export const OBJETOS = { nueva_york: "manzana", pueblo: "bandera", phoenix: "placa", vegas: "ficha", des_moines: "maiz", washington: "voto" };
export const OBJETOS_POR_NIVEL = 10, PREMIO_OBJETOS = 300;
// Los metros de cada uno: repartidos a partes iguales por los tramos que
// valen (fuera del tutorial, del jefe, del festin y del sprint final).
export function sitiosObjetos(nivel) {
  if (!OBJETOS[nivel.id] || !nivel.tramos) return [];
  // 06/11 (3): tampoco en los momentos que cambian la calle (rampa, convoy...).
  const trozos = nivel.tramos.filter(([, , tipo]) => !["tutorial", "jefe", "festin", "sprint", "rampa", "convoy", "premios", "alfombra", "lluvia", "jefe_paso", "metro_vias", "metro_techo", "banderas"].includes(tipo))
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
  recorrerLado(nivel, nivel.izquierda, -1, anchoDe, (e) => salida.push(e));
  recorrerLado(nivel, nivel.derecha, 1, anchoDe, (e) => salida.push(e));
  // (`cruza`: de lado a lado de la calle, como el puente o las pasarelas de Des Moines)
  for (const f of nivel.fondo || []) salida.push({ pieza: f.pieza, d: f.d, lado: f.lado || 0, centro: !!f.centro, cruza: !!f.cruza, ancho: anchoDe(f.pieza) });
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
