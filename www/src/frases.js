// Lo que suelta el presidente con el micrófono, según lo que tenga delante
// (la pieza del obstáculo).
//
// 31/10/2026: Isidro pidió su voz de verdad («las voces a veces no se
// entienden»). Ahora son frases que dijo él, tal cual y en inglés, cortadas de
// grabaciones de dominio público (la Casa Blanca y Voice of America, en
// Wikimedia Commons; ver herramientas/trump.mjs). En castellano sale debajo la
// traducción. Cada texto de aquí tiene su corte de audio: si se añade uno
// nuevo, hay que darle su corte en trump.mjs.

// Las frases, con su traducción para el bocadillo.
export const TRUMP = {
  "THIS IS FAKE NEWS!": "¡Esto son noticias falsas!",
  "RUSSIA IS FAKE NEWS!": "¡Lo de Rusia son noticias falsas!",
  "FAKE. PHONY. FAKE!": "¡Falso. Farsante. Falso!",
  "IT'S A WITCH HUNT AND IT'S A DISGRACE!": "¡Es una caza de brujas y una vergüenza!",
  "IT'S A VERY SAD THING.": "Es algo muy triste.",
  "TREMENDOUS!": "¡Tremendo!",
  "IT'S INCREDIBLE!": "¡Es increíble!",
  "THEY'RE VERY DISHONEST PEOPLE.": "Es gente muy deshonesta.",
  "THE ENEMY OF THE PEOPLE!": "¡El enemigo del pueblo!",
  "AMERICA FIRST!": "¡América primero!",
  "WE WILL MAKE AMERICA GREAT AGAIN!": "¡Haremos América grande otra vez!",
  "WINNING LIKE NEVER BEFORE!": "¡Ganando como nunca!",
  "WE WILL BRING BACK OUR JOBS!": "¡Recuperaremos nuestros empleos!",
  "BUY AMERICAN AND HIRE AMERICAN!": "¡Compra americano y contrata americano!",
  "WE WILL BRING BACK OUR BORDERS!": "¡Recuperaremos nuestras fronteras!",
  "GOD BLESS AMERICA!": "¡Dios bendiga a América!",
  "WE WILL WIN!": "¡Ganaremos!",
  "YOU WILL NEVER BE IGNORED AGAIN!": "¡Nunca más os ignorarán!",
  "CHINA!": "¡China!",
};

// La traducción que sale debajo, solo si el juego está en castellano.
export function traduccion(texto, lang) {
  return lang === "es" ? TRUMP[texto] || "" : "";
}

// Lo que dice según el obstáculo que tenga delante (los mismos textos en los
// dos idiomas: son sus palabras).
const DICHOS = {
  // Los enemigos de siempre: la prensa, la policía de la «caza de brujas», los manifestantes.
  furgoneta: "THIS IS FAKE NEWS!", patrulla: "IT'S A WITCH HUNT AND IT'S A DISGRACE!", suv: "IT'S A WITCH HUNT AND IT'S A DISGRACE!",
  guardaespaldas: "THEY'RE VERY DISHONEST PEOPLE.", agentes: "THEY'RE VERY DISHONEST PEOPLE.",
  barricada: "WE WILL BRING BACK OUR BORDERS!", conos: "WE WILL BRING BACK OUR BORDERS!",
  valla_metal: "WE WILL BRING BACK OUR BORDERS!",
  pancarta: "IT'S A VERY SAD THING.", globos: "IT'S A VERY SAD THING.", protesta: "IT'S A VERY SAD THING.",
  barril: "FAKE. PHONY. FAKE!", jefe: "AMERICA FIRST!",
  // 03/11: el dragon de China y sus bolas de fuego
  dragon: "CHINA!", bola_fuego: "CHINA!",
  // 09/11: los jefes nuevos y lo que tiran
  pinguino: "BUY AMERICAN AND HIRE AMERICAN!", bloque_hielo: "TREMENDOUS!", pez_helado: "IT'S INCREDIBLE!",
  papeles: "FAKE. PHONY. FAKE!", caja_documentos: "IT'S A WITCH HUNT AND IT'S A DISGRACE!", carpeta_vuela: "THIS IS FAKE NEWS!",
  toro: "AMERICA FIRST!", paellera: "WE WILL WIN!", capote: "WINNING LIKE NEVER BEFORE!",
  cerebro: "THEY'RE VERY DISHONEST PEOPLE.", libro_gordo: "FAKE. PHONY. FAKE!", grafico_datos: "THIS IS FAKE NEWS!",
  pantano: "THE ENEMY OF THE PEOPLE!", bola_barro: "IT'S A VERY SAD THING.",
  // Nueva York
  taxi: "BUY AMERICAN AND HIRE AMERICAN!", contenedor: "THE ENEMY OF THE PEOPLE!", alcantarilla: "THE ENEMY OF THE PEOPLE!",
  andamio: "WE WILL BRING BACK OUR JOBS!", viga: "WE WILL BRING BACK OUR JOBS!", basura: "THE ENEMY OF THE PEOPLE!",
  perritos: "BUY AMERICAN AND HIRE AMERICAN!", bici: "THIS IS FAKE NEWS!",
  // Findlay
  tractor: "YOU WILL NEVER BE IGNORED AGAIN!", paca: "YOU WILL NEVER BE IGNORED AGAIN!", vaca: "YOU WILL NEVER BE IGNORED AGAIN!",
  calabazas: "YOU WILL NEVER BE IGNORED AGAIN!", carroza: "GOD BLESS AMERICA!", guirnalda: "GOD BLESS AMERICA!",
  // Phoenix
  saguaro: "TREMENDOUS!", nopal: "TREMENDOUS!", rodadora: "IT'S INCREDIBLE!", calavera: "IT'S INCREDIBLE!",
  pickup: "BUY AMERICAN AND HIRE AMERICAN!", arco_neon: "IT'S INCREDIBLE!", cartel_ruta: "AMERICA FIRST!",
  // Las Vegas
  dado: "WINNING LIKE NEVER BEFORE!", fichas: "WINNING LIKE NEVER BEFORE!", tragaperras: "WE WILL WIN!",
  limusina: "TREMENDOUS!", marquesina: "WE WILL WIN!", elvis: "IT'S INCREDIBLE!",
  // Washington
  cajas: "IT'S A WITCH HUNT AND IT'S A DISGRACE!",
  // Des Moines (01/11): la soja que China no compra, el campo y el caucus
  sacos_soja: "BUY AMERICAN AND HIRE AMERICAN!", monton_soja: "BUY AMERICAN AND HIRE AMERICAN!",
  sinfin: "WE WILL BRING BACK OUR JOBS!", cosechadora: "WE WILL BRING BACK OUR JOBS!", fantasma: "WE WILL BRING BACK OUR JOBS!",
  cerdo: "YOU WILL NEVER BE IGNORED AGAIN!", votantes: "YOU WILL NEVER BE IGNORED AGAIN!",
  urna: "WE WILL WIN!", pancarta_caucus: "WE WILL WIN!",
  quitanieves: "TREMENDOUS!", monton_nieve: "TREMENDOUS!", munieco_nieve: "IT'S INCREDIBLE!",
  // 09/11: los que no tenian frase (salia una cualquiera)
  etiqueta_precio: "CHINA!", caja_precio: "CHINA!", carrito_compra: "BUY AMERICAN AND HIRE AMERICAN!",
  rueda_queso: "TREMENDOUS!", cartel_queso: "TREMENDOUS!", cubo_basura: "THE ENEMY OF THE PEOPLE!",
  jugador_hockey: "THEY'RE VERY DISHONEST PEOPLE.", porteria_hockey: "WE WILL WIN!", periodicos: "THIS IS FAKE NEWS!",
  moto_harley: "BUY AMERICAN AND HIRE AMERICAN!", coche_seguridad: "BUY AMERICAN AND HIRE AMERICAN!", pit_crew: "WE WILL BRING BACK OUR JOBS!",
  caja_filetes: "TREMENDOUS!", cartel_steak: "TREMENDOUS!", cajas_pizza: "IT'S INCREDIBLE!", carrito_perritos: "BUY AMERICAN AND HIRE AMERICAN!",
  carro_clydesdale: "AMERICA FIRST!", bruja_bici: "IT'S A WITCH HUNT AND IT'S A DISGRACE!", segway: "THEY'RE VERY DISHONEST PEOPLE.",
  // El debate de Las Vegas: lo que le suelta al Burrito-Bot con cada micrófono.
  debate: ["RUSSIA IS FAKE NEWS!", "FAKE. PHONY. FAKE!", "THEY'RE VERY DISHONEST PEOPLE.", "THE ENEMY OF THE PEOPLE!", "THIS IS FAKE NEWS!"],
  // Sin nada delante, y cuando sube el multiplicador de tacos.
  nada: ["WE WILL MAKE AMERICA GREAT AGAIN!", "TREMENDOUS!", "WINNING LIKE NEVER BEFORE!", "AMERICA FIRST!"],
  animo: ["TREMENDOUS!", "WINNING LIKE NEVER BEFORE!", "IT'S INCREDIBLE!", "WE WILL WIN!", "WE WILL MAKE AMERICA GREAT AGAIN!"],
};
export const FRASES = { es: DICHOS, en: DICHOS };
