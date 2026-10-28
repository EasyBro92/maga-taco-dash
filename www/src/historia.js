// La historia de la gira (28/10/2026). Ver HISTORIA.md.
//
// Wall Street le llama «TACO» (Trump siempre se raja) y él contesta que va a
// ganar los 50 estados. Cada nivel es un estado: cada taco es un votante, y al
// llegar a la meta el estado se pinta de rojo y suma sus votos electorales de
// verdad (270 para ser presidente; él los quiere los 538). Los enemigos son la
// Liga del Pantano: todos son líos que ha montado él mismo.

// Mapa de casillas: [columna, fila, nombre, name, votos electorales].
// Cada estado es un cuadrado colocado más o menos donde está; así en el móvil
// se ven igual de bien Texas que Rhode Island.
export const ESTADOS = {
  AK: [0, 0, "Alaska", "Alaska", 3],                 ME: [10, 0, "Maine", "Maine", 4],
  WI: [5, 1, "Wisconsin", "Wisconsin", 10],          VT: [8, 1, "Vermont", "Vermont", 3],
  NH: [9, 1, "Nuevo Hampshire", "New Hampshire", 4],
  WA: [0, 2, "Washington", "Washington", 12],        ID: [1, 2, "Idaho", "Idaho", 4],
  MT: [2, 2, "Montana", "Montana", 4],               ND: [3, 2, "Dakota del Norte", "North Dakota", 3],
  MN: [4, 2, "Minnesota", "Minnesota", 10],          IL: [5, 2, "Illinois", "Illinois", 19],
  MI: [6, 2, "Míchigan", "Michigan", 15],            NY: [8, 2, "Nueva York", "New York", 28],
  MA: [9, 2, "Massachusetts", "Massachusetts", 11],
  OR: [0, 3, "Oregón", "Oregon", 8],                 NV: [1, 3, "Nevada", "Nevada", 6],
  WY: [2, 3, "Wyoming", "Wyoming", 3],               SD: [3, 3, "Dakota del Sur", "South Dakota", 3],
  IA: [4, 3, "Iowa", "Iowa", 6],                     IN: [5, 3, "Indiana", "Indiana", 11],
  OH: [6, 3, "Ohio", "Ohio", 17],                    PA: [7, 3, "Pensilvania", "Pennsylvania", 19],
  NJ: [8, 3, "Nueva Jersey", "New Jersey", 14],      CT: [9, 3, "Connecticut", "Connecticut", 7],
  RI: [10, 3, "Rhode Island", "Rhode Island", 4],
  CA: [0, 4, "California", "California", 54],       UT: [1, 4, "Utah", "Utah", 6],
  CO: [2, 4, "Colorado", "Colorado", 10],            NE: [3, 4, "Nebraska", "Nebraska", 5],
  MO: [4, 4, "Misuri", "Missouri", 10],              KY: [5, 4, "Kentucky", "Kentucky", 8],
  WV: [6, 4, "Virginia Occidental", "West Virginia", 4], VA: [7, 4, "Virginia", "Virginia", 13],
  MD: [8, 4, "Maryland", "Maryland", 10],            DE: [9, 4, "Delaware", "Delaware", 3],
  AZ: [1, 5, "Arizona", "Arizona", 11],              NM: [2, 5, "Nuevo México", "New Mexico", 5],
  KS: [3, 5, "Kansas", "Kansas", 6],                 AR: [4, 5, "Arkansas", "Arkansas", 6],
  TN: [5, 5, "Tennessee", "Tennessee", 11],          NC: [6, 5, "Carolina del Norte", "North Carolina", 16],
  SC: [7, 5, "Carolina del Sur", "South Carolina", 9], DC: [8, 5, "Washington D.C.", "Washington D.C.", 3],
  OK: [3, 6, "Oklahoma", "Oklahoma", 7],             LA: [4, 6, "Luisiana", "Louisiana", 8],
  MS: [5, 6, "Misisipi", "Mississippi", 6],          AL: [6, 6, "Alabama", "Alabama", 9],
  GA: [7, 6, "Georgia", "Georgia", 16],
  HI: [0, 7, "Hawái", "Hawaii", 4],                  TX: [3, 7, "Texas", "Texas", 40],
  FL: [8, 7, "Florida", "Florida", 30],
};
export const TOTAL_VOTOS = 538, PARA_GANAR = 270;

// Los actos: cada uno acaba con un jefe de la Liga del Pantano.
export const ACTOS = [
  null,
  { es: "La escalera dorada", en: "The Golden Escalator", jefe: { es: "el Burrito-Bot", en: "Burrito-Bot" } },
  { es: "La guerra de los aranceles", en: "The Tariff War", jefe: { es: "el Rey Pingüino", en: "the Penguin King" } },
  { es: "La tormenta de papeles", en: "The Paper Storm", jefe: { es: "los Papeles de Epstein", en: "the Epstein Files" } },
  { es: "La Armada Española", en: "The Spanish Armada", jefe: { es: "el Toro", en: "the Bull" } },
  { es: "El sentido común", en: "Common Sense", jefe: { es: "el Sentido Común", en: "Common Sense" } },
  { es: "La investidura", en: "Inauguration Day", jefe: { es: "la Liga del Pantano", en: "the Swamp League" } },
];

// Las 51 paradas en orden. [id, estado, nombre, lugar, acto, jefe, historia es, historia en]
// Los niveles ya hechos (en levels.js) ponen su calle; los demás salen en el
// mapa con candado («Próximamente»).
const P = [
  ["nueva_york", "NY", "Quinta Avenida", "Nueva York", 1, false,
    "Wall Street te llama «TACO»: dicen que siempre te rajas. Sal de tu torre y demuéstrales lo contrario. ¡Ojo con las furgonetas de las Fake News!",
    "Wall Street calls you «TACO»: they say you always chicken out. Leave your tower and prove them wrong. Watch out for the Fake News vans!"],
  ["pueblo", "OH", "Main Street", "Findlay, Ohio", 1, false,
    "Mitin en Findlay, la ciudad de las banderas. El Burrito-Bot, el candidato robot hecho en China, ha venido a reventarlo. ¡Súbete a los autobuses y llega al juzgado!",
    "Rally in Findlay, Flag City USA. Burrito-Bot, the made-in-China robot candidate, came to wreck it. Ride the buses and reach the courthouse!"],
  ["phoenix", "AZ", "Central Avenue", "Phoenix, Arizona", 1, false,
    "Phoenix, en pleno desierto. La policía te persigue: ¡es una caza de brujas! Llega al diner antes de que te pillen.",
    "Phoenix, in the middle of the desert. The police are after you: it's a witch hunt! Reach the diner before they catch you."],
  ["vegas", "NV", "El Strip", "Las Vegas, Nevada", 1, true,
    "Debate en el Strip contra el Burrito-Bot. Si le ganas, echará chispas: hecho en China, roto en América.",
    "Debate on the Strip against Burrito-Bot. Beat him and he'll short-circuit: made in China, broken in America."],
  ["des_moines", "IA", "Des Moines", "Iowa", 2, false,
    "La primera votación de verdad. Los granjeros tienen montañas de soja que China ya no compra… por tus aranceles.",
    "The first real vote. Farmers have mountains of soybeans China won't buy anymore… because of your tariffs."],
  ["omaha", "NE", "Omaha", "Nebraska", 2, false,
    "Tierra de vacas. Por la calle, cajas de tus «Filetes Trump», los que nadie compró.",
    "Cattle country. Boxes of your «Trump Steaks», the ones nobody bought, all over the street."],
  ["wichita", "KS", "Wichita", "Kansas", 2, false,
    "Un tornado como el de «El mago de Oz» se lleva las vallas. ¡No hay sitio como la Casa Blanca!",
    "A Wizard of Oz tornado is blowing the fences away. There's no place like the White House!"],
  ["san_luis", "MO", "San Luis", "Misuri", 2, false,
    "Bajo el arco Gateway, las etiquetas de precio no paran de crecer. Los aranceles los paga… ¿quién?",
    "Under the Gateway Arch, price tags keep growing. Who pays the tariffs again?"],
  ["indianapolis", "IN", "Indianápolis", "Indiana", 2, false,
    "El circuito de las 500 millas. Los coches de carreras no esperan a nadie.",
    "The Indy 500 track. Race cars wait for no one."],
  ["detroit", "MI", "Detroit", "Míchigan", 2, false,
    "La ciudad del motor, con coches llenos de aranceles. En el puente, canadienses enfadados: no quieren ser el estado 51.",
    "Motor City, full of tariffed cars. On the bridge, angry Canadians: they don't want to be the 51st state."],
  ["chicago", "IL", "Chicago", "Illinois", 2, false,
    "La ciudad del viento. Agárrate el tupé.",
    "The Windy City. Hold on to your hair."],
  ["milwaukee", "WI", "Milwaukee", "Wisconsin", 2, false,
    "Te subes a un camión de la basura con chaleco reflectante, como aquella vez. Huele a queso.",
    "You hop on a garbage truck in a safety vest, just like that time. It smells like cheese."],
  ["minneapolis", "MN", "Minneapolis", "Minnesota", 2, false,
    "Lagos helados y pistas de hockey. Los canadienses siguen enfadados.",
    "Frozen lakes and hockey rinks. The Canadians are still mad."],
  ["rushmore", "SD", "Monte Rushmore", "Dakota del Sur", 2, false,
    "Quieres tu cara en la montaña, junto a los cuatro presidentes. El escultor dice que no… de momento.",
    "You want your face on the mountain next to the four presidents. The sculptor says no… for now."],
  ["fargo", "ND", "Fargo", "Dakota del Norte", 2, true,
    "Pusiste aranceles a unas islas donde solo viven pingüinos. Ahora el Rey Pingüino viene a cobrártelo en plena nevada.",
    "You put tariffs on islands where only penguins live. Now the Penguin King is coming to collect, in the snow."],
  ["houston", "TX", "Houston", "Texas", 3, false,
    "La NASA. Tu examigo Elon, enfadado tras la pelea, te persigue en cohete.",
    "NASA. Your ex-buddy Elon, still mad after the fight, chases you in a rocket."],
  ["oklahoma", "OK", "Oklahoma City", "Oklahoma", 3, false,
    "Molinos de viento girando en mitad de la calle. Tú dices que dan cáncer.",
    "Windmills spinning in the middle of the street. You say they cause cancer."],
  ["little_rock", "AR", "Little Rock", "Arkansas", 3, false,
    "La mina de diamantes de Arkansas: tacos de oro para tu torre.",
    "Arkansas's diamond mine: golden tacos for your tower."],
  ["jackson", "MS", "Jackson", "Misisipi", 3, false,
    "Barcos de vapor en el Misisipi y pajitas de papel que se deshacen. Tú prefieres las de plástico.",
    "Steamboats on the Mississippi and soggy paper straws. You prefer plastic."],
  ["nueva_orleans", "LA", "Nueva Orleans", "Luisiana", 3, false,
    "Carnaval. Has rebautizado el golfo de México como «golfo de América» y los mapas se han vuelto locos.",
    "Mardi Gras. You renamed the Gulf of Mexico «Gulf of America» and the maps went crazy."],
  ["birmingham", "AL", "Birmingham", "Alabama", 3, false,
    "Llega un huracán que solo existe porque lo pintaste tú con un rotulador en el mapa.",
    "Here comes a hurricane that only exists because you drew it on the map with a marker."],
  ["nashville", "TN", "Nashville", "Tennessee", 3, false,
    "Música country. Llega a la meta bailando el YMCA.",
    "Country music. Dance the YMCA all the way to the finish."],
  ["louisville", "KY", "Louisville", "Kentucky", 3, false,
    "La carrera de caballos del Derby. Los caballos corren más que tú.",
    "The Kentucky Derby. The horses are faster than you."],
  ["atlanta", "GA", "Atlanta", "Georgia", 3, false,
    "Tu foto de la ficha policial está en todas las paredes. Misión: «encuéntrame 11.780 votos». Aquí puedes pasar de 270.",
    "Your mugshot is on every wall. Mission: «find me 11,780 votes». Here you can pass 270."],
  ["charlotte", "NC", "Charlotte", "Carolina del Norte", 3, false,
    "El circuito de NASCAR, a toda velocidad.",
    "The NASCAR track, full throttle."],
  ["charleston_sc", "SC", "Charleston", "Carolina del Sur", 3, false,
    "Te escapas a jugar al golf. Pelotas volando y carritos por todas partes.",
    "You sneak off to play golf. Flying balls and golf carts everywhere."],
  ["miami", "FL", "Miami", "Florida", 3, true,
    "Un huracán de papeles con tachones negros llega a Mar-a-Lago: los papeles de Epstein. Tú dices que es un bulo.",
    "A hurricane of blacked-out papers hits Mar-a-Lago: the Epstein files. You say it's a hoax."],
  ["albuquerque", "NM", "Albuquerque", "Nuevo México", 4, false,
    "Globos… y carteles en español: España dice que estos nombres los puso ella. Y un platillo volante de Roswell.",
    "Balloons… and signs in Spanish: Spain says it named these places. And a flying saucer from Roswell."],
  ["denver", "CO", "Denver", "Colorado", 4, false,
    "«Colorado» significa rojo en español. Tú dices que es una señal.",
    "«Colorado» means red in Spanish. You say it's a sign."],
  ["cheyenne", "WY", "Cheyenne", "Wyoming", 4, false,
    "Rodeo y estampida de bisontes.",
    "Rodeo and a bison stampede."],
  ["billings", "MT", "Billings", "Montana", 4, false,
    "«Montana» viene de «montaña». Osos pardos en la carretera.",
    "«Montana» comes from the Spanish for mountain. Grizzly bears on the road."],
  ["boise", "ID", "Boise", "Idaho", 4, false,
    "Patatas rodando cuesta abajo.",
    "Potatoes rolling downhill."],
  ["salt_lake", "UT", "Salt Lake City", "Utah", 4, false,
    "El desierto de sal: el tramo más rápido de la gira.",
    "The salt flats: the fastest stretch of the tour."],
  ["seattle", "WA", "Seattle", "Washington", 4, false,
    "Llueve sin parar. Tu pelo corre peligro.",
    "Nonstop rain. Your hair is in danger."],
  ["portland_or", "OR", "Portland", "Oregón", 4, false,
    "Manifestantes disfrazados de rana hinchable. Sí, pasó de verdad.",
    "Protesters in inflatable frog costumes. Yes, that really happened."],
  ["anchorage", "AK", "Anchorage", "Alaska", 4, false,
    "Intentas comprar Alaska. Te recuerdan que ya es tuya. «Pues compro Groenlandia».",
    "You try to buy Alaska. They remind you it's already yours. «Then I'll buy Greenland»."],
  ["honolulu", "HI", "Honolulu", "Hawái", 4, false,
    "Surf, cocos que caen y otra partida de golf.",
    "Surf, falling coconuts and another round of golf."],
  ["los_angeles", "CA", "Los Ángeles", "California", 4, true,
    "Dijiste que España era del BRICS y la quisiste echar de la OTAN. Ahora España suelta al Toro: ¡encierro de San Fermín por Hollywood!",
    "You said Spain was in BRICS and tried to kick it out of NATO. Now Spain unleashes the Bull: a Pamplona bull run down Hollywood!"],
  ["charleston_wv", "WV", "Charleston", "Virginia Occidental", 5, false,
    "Vagonetas de tu «precioso carbón limpio».",
    "Carts of your «beautiful clean coal»."],
  ["richmond", "VA", "Richmond", "Virginia", 5, false,
    "Tanques del desfile de tu cumpleaños. Defensa ahora se llama «Departamento de Guerra».",
    "Tanks from your birthday parade. Defense is now the «Department of War»."],
  ["baltimore", "MD", "Baltimore", "Maryland", 5, false,
    "Cangrejos que pellizcan los tobillos.",
    "Crabs that pinch your ankles."],
  ["wilmington", "DE", "Wilmington", "Delaware", 5, false,
    "El pueblo de tu rival dormilón: mecedoras y helados por la calle.",
    "Your sleepy rival's hometown: rocking chairs and ice cream all over the street."],
  ["filadelfia", "PA", "Filadelfia", "Pensilvania", 5, false,
    "La Campana de la Libertad. Te pones en la freidora de un McDonald's, como aquella vez.",
    "The Liberty Bell. You work the fryer at a McDonald's, just like that time."],
  ["atlantic_city", "NJ", "Atlantic City", "Nueva Jersey", 5, false,
    "Tus casinos arruinados. Contigo, hasta la banca pierde.",
    "Your bankrupt casinos. With you, even the house loses."],
  ["hartford", "CT", "Hartford", "Connecticut", 5, false,
    "La capital de los seguros. Ninguno te cubre los tropezones.",
    "The insurance capital. None of them cover your stumbles."],
  ["burlington", "VT", "Burlington", "Vermont", 5, false,
    "Helados y un senador con guantes de lana que lo critica todo.",
    "Ice cream and a senator in wool mittens who criticizes everything."],
  ["portland_me", "ME", "Portland", "Maine", 5, false,
    "Langostas por todas partes. Pellizcan más que los cangrejos.",
    "Lobsters everywhere. They pinch harder than crabs."],
  ["manchester", "NH", "Manchester", "Nuevo Hampshire", 5, false,
    "La primera nevada. El lema del estado: «Vive libre o muere».",
    "The first snowfall. State motto: «Live free or die»."],
  ["providence", "RI", "Providence", "Rhode Island", 5, false,
    "El estado más pequeño y el nivel más corto. Tú dices que es enorme, tremendo.",
    "The smallest state and the shortest level. You say it's huge, tremendous."],
  ["boston", "MA", "Boston", "Massachusetts", 5, true,
    "Lo último que te queda por vencer es el sentido común, escondido en Harvard. Lanza libros y datos. Tú tienes el «¡COVFEFE!».",
    "The last thing in your way is common sense, hiding at Harvard. It throws books and facts. You have «COVFEFE!»."],
  ["washington", "DC", "Pennsylvania Avenue", "Washington D.C.", 6, true,
    "La investidura. Toda la Liga del Pantano se junta para pararte. Corre por Pennsylvania Avenue, drena el pantano y entra en la Casa Blanca.",
    "Inauguration day. The whole Swamp League teams up to stop you. Run down Pennsylvania Avenue, drain the swamp and enter the White House."],
];
export const PARADAS = P.map(([id, estado, nombre, lugar, acto, jefe, es, en], i) => ({
  id, estado, nombre, lugar, acto, jefe, numero: i + 1, votos: ESTADOS[estado][4], historia: { es, en },
}));

export function nombreEstado(codigo, lang = "es") {
  const e = ESTADOS[codigo];
  return e ? (lang === "en" ? e[3] : e[2]) : codigo;
}

// Votos de los estados ya ganados.
export function votosGanados(niveles, superados) {
  return niveles.reduce((s, n) => s + (superados[n.id] ? n.votos : 0), 0);
}

// El prólogo: se enseña la primera vez que se abre el mapa (y con el botón «Historia»).
export const PROLOGO = [
  { peg: "taco",
    es: ["«TACO»", "En la tele, los de Wall Street se ríen de él. Le han puesto un mote: TACO, «Trump siempre se raja», porque anuncia aranceles y luego se echa atrás."],
    en: ["«TACO»", "On TV, Wall Street is laughing at him. They gave him a nickname: TACO, «Trump Always Chickens Out», because he announces tariffs and then backs down."] },
  { peg: "taco_perfecto",
    es: ["«¿Que me rajo?»", "Se pide un taco bowl en el grill de su torre y lo suelta: «Voy a ganar los 50 estados. Todos. La mayor victoria de la historia, nunca vista»."],
    en: ["«Me? Chicken out?»", "He orders a taco bowl at his tower's grill and says: «I'm going to win all 50 states. Every one. The greatest victory in history, never seen before»."] },
  { icono: "jefe",
    es: ["La Liga del Pantano", "Mientras, en un pantano de Washington, se juntan sus enemigos: el Burrito-Bot de China, los aranceles, los papeles de Epstein, España y el sentido común. Todos son líos que ha montado él… pero él jura que es una conspiración."],
    en: ["The Swamp League", "Meanwhile, in a Washington swamp, his enemies team up: China's Burrito-Bot, the tariffs, the Epstein files, Spain and common sense. He made every one of those messes himself… but he swears it's a conspiracy."] },
  { peg: "voto",
    es: ["Cada taco es un votante", "Gana un estado y se pintará de rojo en el mapa. Con 270 votos ya eres presidente, pero él los quiere todos: 538. ¡A correr!"],
    en: ["Every taco is a voter", "Win a state and it turns red on the map. 270 votes make you president, but he wants them all: 538. Run!"] },
];

// Lo que pone en su red social al ganar un estado.
const POSTS = {
  nueva_york: { es: "¡Nueva York ha votado ROJO! Las Fake News no se lo creen. ¿TACO? Nadie se raja menos que yo. ¡TREMENDO!",
    en: "New York voted RED! The Fake News can't believe it. TACO? Nobody chickens out less than me. TREMENDOUS!" },
  pueblo: { es: "Findlay me AMA. El Burrito-Bot vino a reventar mi mitin y salió huyendo. ¡TRISTE!",
    en: "Findlay LOVES me. Burrito-Bot came to wreck my rally and ran away. SAD!" },
  phoenix: { es: "La mayor caza de brujas de la historia y aun así gano Arizona. ¡Nadie corre como yo!",
    en: "The greatest witch hunt in history and I still win Arizona. Nobody runs like me!" },
  vegas: { es: "He ganado el debate. Todo el mundo lo dice. El Burrito-Bot sigue echando chispas. ¡Hecho en China, roto en América!",
    en: "I won the debate. Everybody says so. Burrito-Bot is still sparking. Made in China, broken in America!" },
};
export function postDe(n, lang, votosAntes, votosAhora, todoRojo) {
  const L = lang === "en" ? "en" : "es";
  if (n.id === "washington") {
    return todoRojo
      ? (L === "en" ? "538 TO 0. The greatest victory in history, never seen before. Now, a taco bowl. Who's calling? GREENLAND?"
        : "538 A 0. La mayor victoria de la historia, nunca vista. Ahora, un taco bowl. ¿Quién llama? ¿GROENLANDIA?")
      : (L === "en" ? "I've seen the White House from the inside! I still need more states, but I'll be back. The greatest inauguration in history."
        : "¡He visto la Casa Blanca por dentro! Aún me faltan estados, pero volveré. Será la mayor investidura de la historia.");
  }
  const e = nombreEstado(n.estado, L);
  let txt = POSTS[n.id] ? POSTS[n.id][L]
    : L === "en" ? `${e} voted RED! Nobody ever won ${e} like me. TREMENDOUS!` : `¡${e} ha votado ROJO! Nadie ha ganado ${e} como yo. ¡TREMENDO!`;
  if (votosAntes < PARA_GANAR && votosAhora >= PARA_GANAR) {
    txt += L === "en" ? " 270! I'm the PRESIDENT-ELECT! But I want all 538." : " ¡270! ¡Soy el PRESIDENTE ELECTO! Pero quiero los 538.";
  }
  return txt;
}
