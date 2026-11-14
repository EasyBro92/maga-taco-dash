import * as THREE from "../vendor/three.module.min.js";
import { medidas } from "./models.js";
import { mergeGeometries } from "../vendor/BufferGeometryUtils.js";

// Edificios de relleno únicos (25/10/2026), montados con el kit de blender/kit.py.
//
// Isidro: «que las calles no sean genéricas sino que cada edificio sea único y
// esté siempre en el mismo punto». Cada solar trae su semilla (levels.js): con
// ella se elige el bajo, cuántas plantas y de qué estilo, la cornisa, el remate,
// el color, los toldos y el rótulo. La misma semilla da siempre el mismo
// edificio, así que la calle es siempre la misma, pero no hay dos iguales.
//
// Las piezas del kit vienen casi blancas: aquí se tiñen. Miden 20 de ancho;
// un edificio de 18 a 26 se estira un poco, y uno de 40 son dos columnas.

export const PIEZAS_KIT = [
  "bajo_tiendas", "bajo_grande", "bajo_banco",
  "planta_lisa", "planta_frontones", "planta_miradores", "planta_cristal", "planta_ladrillo", "planta_balcones",
  "cornisa_clasica", "cornisa_deco", "cornisa_simple",
  "remate_deposito", "remate_mansarda", "remate_atico", "remate_antena", "toldo_kit",
];

const BAJOS = ["bajo_tiendas", "bajo_tiendas", "bajo_grande", "bajo_banco"];
const PLANTAS = ["planta_lisa", "planta_frontones", "planta_miradores", "planta_cristal", "planta_ladrillo", "planta_balcones"];
const REMATES = ["remate_deposito", "remate_mansarda", "remate_atico", "remate_antena", null, null];
// Colores de fachada naturales (piedra, arenisca, ladrillo, revocos suaves).
const PIEDRAS = [0xf1e3c8, 0xe9d6c0, 0xd9dbe0, 0xe2d2b0, 0xcfd8de, 0xeadcb0, 0xd8c3b4, 0xc9d1c0, 0xf3ece0, 0xdcc9a8];
const LADRILLOS = [0xc8735a, 0xb8604a, 0xa85a48, 0xc98b6a, 0x9a5a50];
const TOLDOS = [0x2d5a3a, 0x7a2a32, 0x22314f, 0xb8862b, 0x8a3a6a, 0x3a6a8a, 0x2a2a2e, 0xc0532f];
const ROTULOS = ["DELI", "BAGELS", "PIZZA", "JEWELRY", "BOUTIQUE", "BOOKS", "SHOES", "PHARMACY", "CAFÉ", "FLOWERS",
  "TOYS", "BANK", "GIFTS", "HATS", "DONUTS", "CHOCOLATE", "WATCHES", "PERFUME", "TAILOR", "CANDY", "BAKERY", "MUSIC"];

// Las Vegas (29/10): letreros de neon (fijos, sin parpadeo) y colores de hotel.
const ROTULOS_VEGAS = ["CASINO", "SLOTS", "BUFFET", "POKER", "JACKPOT", "BINGO", "SHOWS", "WEDDING CHAPEL", "MOTEL",
  "LIVE MUSIC", "OPEN 24H", "BLACKJACK", "LUCKY 7", "KENO", "STEAKHOUSE", "MAGIC SHOW", "ELVIS"];
const GRANDES_VEGAS = ["CASINO", "HOTEL", "SLOTS", "RESORT", "JACKPOT", "LUCKY 7", "GOLD", "STARS", "DIAMOND", "ROYAL"];
const NEONES = ["#ff4fd8", "#46e0d0", "#ffe066", "#7cff6b", "#ff6a3a", "#6ab8ff"];
const COLORES_VEGAS = [0xf6f1e6, 0xf3e6c8, 0xe9d6b8, 0xf2c7c0, 0xbfe3e0, 0xe8d08a, 0xd9dbe0, 0xd8c8f0, 0xf6dcc0];

const elegir = (azar, lista) => lista[Math.floor(azar() * lista.length)];

// 08/11/2026 (2): Isidro: «faltan detalles en los mapas, me gustan pero se
// sienten muy parecidos». Las ciudades nuevas tenian todas los mismos
// edificios: ahora cada una lleva su estilo (`kit.estilo` en levels.js), con
// sus plantas, sus colores, sus cornisas, sus remates, sus toldos y los
// rotulos de sus tiendas.
const ESTILOS = {
  // Omaha: el Old Market, almacenes de ladrillo rojo oscuro con depositos de agua.
  omaha: { plantas: ["planta_ladrillo", "planta_ladrillo", "planta_ladrillo", "planta_lisa", "planta_miradores"],
    ladrillos: [0x8a3f2e, 0x7a3428, 0x9a4a36, 0x6e3a2c, 0xa85a3e], piedras: [0xd8c3a8, 0xc9b08a, 0xe2d2b0],
    cornisas: ["cornisa_clasica", "cornisa_simple"], remate: ["remate_deposito", 0.35], bajos: ["bajo_tiendas", "bajo_tiendas", "bajo_grande"],
    toldos: [0x2d5a3a, 0x7a2a32, 0x1f2a3a, 0xb8862b],
    rotulos: ["STEAKHOUSE", "OLD MARKET", "ANTIQUES", "BREWERY", "CANDY", "BOOKS", "BBQ", "SADDLERY", "GALLERY", "ICE CREAM"] },
  // Wichita: arenisca y ladrillo claro, pocas plantas y aire del oeste.
  wichita: { plantas: ["planta_lisa", "planta_balcones", "planta_ladrillo", "planta_frontones"],
    ladrillos: [0xc98b6a, 0xb8704f, 0xd09a72], piedras: [0xe8cfa6, 0xe2d2b0, 0xd8c2a0, 0xf0dcc0, 0xcdb48e],
    cornisas: ["cornisa_clasica", "cornisa_deco"], remate: ["remate_atico", 0.15], toldos: [0x8a3a2a, 0x2a4a6a, 0xb8862b, 0x3a5a3a],
    rotulos: ["WESTERN WEAR", "BOOTS", "BBQ", "AVIATION", "SADDLES", "DINER", "RODEO", "HARDWARE", "PIZZA", "COFFEE"] },
  // San Luis: el ladrillo rojo de toda la vida con cornisas de piedra.
  san_luis: { plantas: ["planta_ladrillo", "planta_ladrillo", "planta_frontones", "planta_miradores", "planta_lisa"],
    ladrillos: [0xa8402e, 0x9a3a2a, 0xb8503a, 0x8a3428], piedras: [0xe4dcc8, 0xd8ccb4, 0xcfc3aa],
    cornisas: ["cornisa_clasica", "cornisa_clasica", "cornisa_deco"], remate: ["remate_mansarda", 0.15], toldos: [0xc8202e, 0x1f3a6a, 0x2d5a3a, 0xf2c230],
    rotulos: ["TOASTED RAVIOLI", "BLUES CLUB", "BBQ", "BREWERY", "CUSTARD", "BASEBALL", "GOOEY BUTTER", "PRETZELS", "JAZZ", "BAKERY"] },
  // Indianapolis: la piedra caliza de Indiana, clara, y torres de cristal.
  indy: { plantas: ["planta_frontones", "planta_lisa", "planta_cristal", "planta_lisa", "planta_balcones"],
    ladrillos: [0xb8704f], piedras: [0xe6dcc6, 0xefe6d2, 0xdcd0b8, 0xe9e0cc, 0xd8ccb0], cristal: [0xcfd8de, 0xbcd0e0, 0xd9dbe0],
    cornisas: ["cornisa_clasica", "cornisa_simple"], remate: ["remate_antena", 0.15], toldos: [0x1d1f25, 0xc8202e, 0x1f3a8a, 0xf2c230],
    rotulos: ["RACING GEAR", "PIT STOP", "TIRES", "CHECKERED", "DINER", "PIZZA", "SPEED SHOP", "TROPHIES", "COFFEE", "BURGERS"] },
  // Detroit: art deco, ladrillo oscuro y terracota, y alguna torre de cristal.
  detroit: { plantas: ["planta_lisa", "planta_ladrillo", "planta_cristal", "planta_miradores", "planta_ladrillo"],
    ladrillos: [0x7a3a2e, 0x6a3428, 0x8a4a34, 0x5e3026], piedras: [0xc98a5a, 0xb8a080, 0x9a8a78, 0xd8b890, 0x8a7a6e], cristal: [0x9aaabb, 0xb0bcc8],
    cornisas: ["cornisa_deco", "cornisa_deco", "cornisa_clasica"], remate: ["remate_antena", 0.25], toldos: [0x1d1f25, 0x7a2a32, 0x2a4a6a, 0xc0532f],
    rotulos: ["CONEY ISLAND", "MOTOWN", "RECORDS", "AUTO PARTS", "COFFEE", "PIZZA", "SOUL FOOD", "HOT DOGS", "GARAGE", "TIRES"] },
  // Chicago: la escuela de Chicago (miradores y ventanas anchas), terracota
  // blanca, caliza y torres de cristal.
  chicago: { plantas: ["planta_miradores", "planta_miradores", "planta_lisa", "planta_frontones", "planta_cristal", "planta_ladrillo"],
    ladrillos: [0x9a4a36, 0x7a3a2e, 0xb8704f], piedras: [0xe6dcc6, 0xd8ccb0, 0xefe6d2, 0xf4f0e6, 0xc9b896], cristal: [0x9fb4c4, 0xb8c8d4, 0x8aa0b4],
    cornisas: ["cornisa_clasica", "cornisa_deco", "cornisa_simple"], remate: ["remate_antena", 0.15], toldos: [0x1f3a6a, 0xc8202e, 0x2d5a3a, 0x1d1f25],
    rotulos: ["DEEP DISH", "HOT DOGS", "BLUES", "JAZZ CLUB", "POPCORN", "STEAKHOUSE", "THEATRE", "RECORDS", "PIZZA", "BOOKS"] },
  // Milwaukee, «la ciudad crema»: el ladrillo color crema de su arcilla, algo
  // de ladrillo rojo, piedra y las tabernas y queserias de toda la vida.
  milwaukee: { plantas: ["planta_ladrillo", "planta_ladrillo", "planta_frontones", "planta_miradores", "planta_lisa", "planta_cristal"],
    ladrillos: [0xe2cfa4, 0xd8c294, 0xcdb688, 0xa8523a], piedras: [0xe6dcc6, 0xd8ccb0, 0xcfc3aa], cristal: [0x9fb4c4, 0xb8c8d4],
    cornisas: ["cornisa_clasica", "cornisa_clasica", "cornisa_simple"], remate: ["remate_antena", 0.1], toldos: [0x203a30, 0xffb612, 0xc8202e, 0x1f3a6a],
    rotulos: ["CHEESE", "BRATWURST", "CUSTARD", "TAVERN", "POLKA HALL", "FISH FRY", "BREWERY", "SAUSAGE", "SUPPER CLUB", "BOWLING"] },
  // 12/11: Rapid City: pueblo del Oeste de ladrillo y madera, con las tiendas
  // de los turistas que van al monte Rushmore.
  rapid: { plantas: ["planta_ladrillo", "planta_frontones", "planta_lisa", "planta_balcones", "planta_ladrillo"],
    ladrillos: [0xa8603e, 0x9a5236, 0xc0884e, 0x8a4a30], piedras: [0xd8c8a6, 0xcbb894, 0xe2d4b6], cristal: [0x8aa0b0, 0x9fb4c4],
    cornisas: ["cornisa_clasica", "cornisa_simple", "cornisa_clasica"], remate: ["remate_antena", 0.05], toldos: [0x8a2a1e, 0x2d5a3a, 0x1f3a6a, 0xc89a3a],
    rotulos: ["SALOON", "GOLD", "JERKY", "BLACK HILLS GOLD", "TRADING POST", "MOTEL", "ROCK SHOP", "BBQ", "BOOTS", "ROCK'N ROLL"] },
  // 13/11: Little Rock: ladrillo del River Market y tiendas de Arkansas.
  littlerock: { plantas: ["planta_ladrillo", "planta_frontones", "planta_lisa", "planta_ladrillo", "planta_balcones"],
    ladrillos: [0x9a4a32, 0xa85a3a, 0x8a3e2a, 0xb06a48], piedras: [0xe2d4b6, 0xd8c8a6], cristal: [0x8aa0b0, 0x9fb4c4],
    cornisas: ["cornisa_clasica", "cornisa_simple"], remate: ["remate_antena", 0.08], toldos: [0x9d2235, 0x2d5a3a, 0x1f3a6a, 0xc89a3a],
    rotulos: ["DIAMONDS", "BBQ", "RAZORBACKS", "CATFISH", "PIG SOOIE", "OZARK", "BOOTS", "PIES", "MINING CO", "BLUES"] },
  // 13/11: Nueva Orleans: casas del Barrio Francés, bajas, de colores y con balcones.
  nuevaorleans: { plantas: ["planta_balcones", "planta_balcones", "planta_miradores", "planta_balcones", "planta_lisa"],
    ladrillos: [0xe8a8a0, 0xf2d48a, 0xa8c8b0, 0xb8a8d8, 0xf0b890], piedras: [0xf4efe4, 0xe8dcc8], cristal: [0x8aa0b0, 0x9fb4c4],
    cornisas: ["cornisa_clasica", "cornisa_simple"], remate: ["remate_antena", 0.02], toldos: [0x5a2a8a, 0x1f8a4a, 0xe8b830, 0x8a2a1e],
    rotulos: ["JAZZ", "GUMBO", "BEIGNETS", "VOODOO", "PRALINES", "OYSTERS", "PO-BOYS", "CREOLE", "BOURBON ST", "MARDI GRAS"] },
  // 13/11: Birmingham: ladrillo de la ciudad del hierro y el acero.
  birmingham: { plantas: ["planta_ladrillo", "planta_frontones", "planta_lisa", "planta_ladrillo", "planta_miradores"],
    ladrillos: [0x8a4a3a, 0x9a5a42, 0x7a3e2e, 0xa86a4a], piedras: [0xe2d4b6, 0xd0c0a0], cristal: [0x8aa0b0, 0x9fb4c4],
    cornisas: ["cornisa_clasica", "cornisa_deco"], remate: ["remate_antena", 0.1], toldos: [0x8a2a1e, 0x2d5a3a, 0x1f3a6a, 0xc89a3a],
    rotulos: ["STEEL", "IRON WORKS", "MAGIC CITY", "BBQ", "SWEET TEA", "FOUNDRY", "HOT DOGS", "RAILROAD", "VULCAN", "BISCUITS"] },
  // 13/11: Jackson: casas del sur con balcones y porches, y bares de blues.
  jackson: { plantas: ["planta_balcones", "planta_ladrillo", "planta_miradores", "planta_lisa", "planta_balcones"],
    ladrillos: [0xc8a070, 0xb88a5a, 0x9a4a32, 0xe0c8a0], piedras: [0xf0e6d0, 0xe2d4b6], cristal: [0x8aa0b0, 0x9fb4c4],
    cornisas: ["cornisa_clasica", "cornisa_deco"], remate: ["remate_antena", 0.05], toldos: [0x2f6a8a, 0x8a2a1e, 0x2d5a3a, 0xc89a3a],
    rotulos: ["BLUES", "CATFISH", "JUKE JOINT", "SOUL FOOD", "COTTON", "GUMBO", "TAMALES", "RECORDS", "MAGNOLIA", "STEAMBOAT"] },
  // 12/11: Houston: torres de cristal y oficinas del petroleo, y tiendas tejanas.
  houston: { plantas: ["planta_cristal", "planta_cristal", "planta_lisa", "planta_ladrillo", "planta_frontones"],
    ladrillos: [0xb8784a, 0xa8603e, 0xc8a070], piedras: [0xe6dcc6, 0xd8ccb0, 0xcfc3aa], cristal: [0x6f9fc0, 0x8fb4cc, 0x5a7f9a],
    cornisas: ["cornisa_simple", "cornisa_deco"], remate: ["remate_antena", 0.2], toldos: [0xc8202e, 0x1f3a6a, 0xf2a830, 0x2d5a3a],
    rotulos: ["BBQ", "TEX-MEX", "OIL & GAS", "RODEO", "BOOTS", "SPACE", "TACOS", "HONKY TONK", "HOUSTON", "STEAKHOUSE"] },
  // 12/11: Oklahoma City: almacenes de ladrillo de Bricktown y tiendas del Oeste.
  oklahoma: { plantas: ["planta_ladrillo", "planta_ladrillo", "planta_frontones", "planta_lisa", "planta_balcones"],
    ladrillos: [0x9a4a32, 0xa85a3a, 0x8a3e2a, 0xb87048], piedras: [0xe2d4b6, 0xd8c8a6], cristal: [0x8aa0b0, 0x9fb4c4],
    cornisas: ["cornisa_clasica", "cornisa_simple"], remate: ["remate_antena", 0.08], toldos: [0x841617, 0x2d5a3a, 0x1f3a6a, 0xc89a3a],
    rotulos: ["OIL", "STEAKS", "SOONER", "RODEO", "BOOTS", "SADDLES", "BBQ", "CATTLE CO", "DRILL", "SALOON"] },
  // 12/11: Fargo: almacenes de ladrillo rojo del ferrocarril y tiendas para el frio.
  fargo: { plantas: ["planta_ladrillo", "planta_ladrillo", "planta_frontones", "planta_lisa", "planta_cristal"],
    ladrillos: [0x9a4a36, 0x8a3e2e, 0xb06a4a, 0x7a3a2e], piedras: [0xe6dcc6, 0xd8ccb0], cristal: [0x7f9fb8, 0x9fb4c4],
    cornisas: ["cornisa_simple", "cornisa_clasica", "cornisa_deco"], remate: ["remate_antena", 0.1], toldos: [0x1f3a6a, 0xc8202e, 0x2d5a3a, 0x4a2a6a],
    rotulos: ["HOTDISH", "SNOW GEAR", "WOODCHIPPER", "YAH SURE", "BISON", "COFFEE", "BOOTS", "LUTEFISK", "PARKAS", "BAR"] },
  // Minneapolis: ladrillo rojo de los almacenes, cristal de las torres y las
  // tiendas del frio (patines, cebos, saunas) y la comida de alli.
  minneapolis: { plantas: ["planta_ladrillo", "planta_cristal", "planta_lisa", "planta_frontones", "planta_cristal", "planta_ladrillo"],
    ladrillos: [0x9a4a36, 0xa8604a, 0x7a3a2e], piedras: [0xe6dcc6, 0xd8ccb0, 0xcfc3aa], cristal: [0x7f9fb8, 0x9fb4c4, 0x6a8aa8],
    cornisas: ["cornisa_simple", "cornisa_deco", "cornisa_clasica"], remate: ["remate_antena", 0.15], toldos: [0x4a2a6a, 0x1f3a6a, 0xc8202e, 0x2d5a3a],
    rotulos: ["HOT DISH", "JUICY LUCY", "SKATES", "HOCKEY", "UFF DA", "BAIT SHOP", "SAUNA", "LEFSE", "BOOKS", "DINER"] },
};

// Rotulo pintado: letras de color sobre fondo oscuro o claro.
const rotulos = {};
function texturaRotulo(texto, fondo, letra, neon = false) {
  const clave = texto + fondo + letra + neon;
  if (rotulos[clave]) return rotulos[clave];
  const c = document.createElement("canvas");
  c.width = 512; c.height = 96;
  const ctx = c.getContext("2d");
  ctx.fillStyle = fondo;
  ctx.beginPath(); ctx.roundRect(4, 4, 504, 88, 16); ctx.fill();
  ctx.font = '700 60px Fredoka, "Arial Rounded MT Bold", Arial, sans-serif';
  ctx.textAlign = "center"; ctx.textBaseline = "middle";
  ctx.fillStyle = letra;
  if (texto.length > 11) ctx.font = '700 46px Fredoka, "Arial Rounded MT Bold", Arial, sans-serif';
  if (neon) {
    // Neon: un halo del mismo color alrededor de las letras y un borde.
    ctx.shadowColor = letra; ctx.shadowBlur = 14;
    ctx.strokeStyle = letra; ctx.lineWidth = 4;
    ctx.beginPath(); ctx.roundRect(10, 10, 492, 76, 12); ctx.stroke();
  }
  ctx.fillText(texto, 256, 52);
  const tex = new THREE.CanvasTexture(c);
  tex.colorSpace = THREE.SRGBColorSpace;
  tex.anisotropy = 4;
  rotulos[clave] = tex;
  return tex;
}
const rotuloGeo = new THREE.PlaneGeometry(1, 1);
const nieveGeo = new THREE.BoxGeometry(1, 1, 1).translate(0, 0.5, 0);

function pieza(nombre, tintes, color) {
  const p = medidas("kit/" + nombre);
  if (!p) return null;
  let m = tintes.get(nombre + color);
  if (!m) {
    m = p.material.clone();
    m.color.set(color);
    tintes.set(nombre + color, m);
  }
  return new THREE.Mesh(p.geometry, m);
}

// Un edificio de `ancho` (a lo largo de la calle) a partir de un azar con semilla.
export function construirEdificio(azar, ancho, opciones = {}) {
  const g = new THREE.Group();
  const tintes = new Map();
  const columnas = ancho >= 36 ? 2 : 1;
  const anchoCol = ancho / columnas;
  const sx = anchoCol / 20;
  const planta = elegir(azar, PLANTAS);
  const esLadrillo = planta === "planta_ladrillo";
  const color = esLadrillo ? elegir(azar, LADRILLOS) : elegir(azar, PIEDRAS);
  const colorBajo = azar() < 0.5 ? color : elegir(azar, PIEDRAS);
  const bajo = elegir(azar, BAJOS);
  const minP = opciones.minPlantas ?? 3, maxP = opciones.maxPlantas ?? 10;
  const plantas = minP + Math.floor(azar() * (maxP - minP + 1));
  // A veces la primera planta (la «noble») va con frontones aunque el resto no.
  const noble = azar() < 0.35 ? "planta_frontones" : planta;
  const cornisa = planta === "planta_cristal" ? "cornisa_simple" : elegir(azar, ["cornisa_clasica", "cornisa_clasica", "cornisa_deco"]);
  const remate = elegir(azar, REMATES);
  let toldo = elegir(azar, TOLDOS);
  let rotulo = elegir(azar, ROTULOS);
  const fondoRotulo = azar() < 0.5 ? "#22304f" : "#2b2b2e";
  const letraRotulo = elegir(azar, ["#ffd23f", "#ffffff", "#f6c27a", "#e8f4ff"]);
  let rotuloV = null;
  let estilo = { planta, noble, color, colorBajo, bajo, cornisa, remate };
  if (opciones.federal) {
    // Ministerio de Washington (26/10): piedra clara, sin tiendas, frontones
    // o lisa, cornisa clasica y tejado plano. Se eligen despues de lo normal
    // para no cambiar los edificios de los niveles que ya existian.
    const p = azar() < 0.55 ? "planta_frontones" : "planta_lisa";
    const piedra = elegir(azar, [0xf1e3c8, 0xe9e2d4, 0xe2d2b0, 0xeadcb0, 0xf3ece0, 0xdcd3c2]);
    estilo = { planta: p, noble: "planta_frontones", color: piedra, colorBajo: piedra,
      bajo: azar() < 0.6 ? "bajo_banco" : "bajo_grande", cornisa: "cornisa_clasica",
      remate: azar() < 0.2 ? "remate_mansarda" : null };
  }
  if (opciones.pueblo) {
    // Main Street de un pueblo del Medio Oeste (26/10): casi todo ladrillo,
    // tiendas con toldo abajo, cornisa de ménsulas y tejado plano. Tambien se
    // elige despues de lo normal para no cambiar los otros niveles.
    const lad = azar() < 0.7;
    const p = lad ? "planta_ladrillo" : elegir(azar, ["planta_lisa", "planta_balcones", "planta_miradores"]);
    const c = lad ? elegir(azar, [...LADRILLOS, 0xb8704f, 0xc58a62]) : elegir(azar, [0xf1e3c8, 0xe9d6c0, 0xe2d2b0, 0xd8c3b4, 0xc9d1c0, 0xf3ece0]);
    estilo = { planta: p, noble: p, color: c, colorBajo: azar() < 0.6 ? c : elegir(azar, PIEDRAS),
      bajo: azar() < 0.85 ? "bajo_tiendas" : "bajo_grande", cornisa: azar() < 0.6 ? "cornisa_clasica" : "cornisa_deco",
      remate: azar() < 0.12 ? "remate_deposito" : null };
  }

  if (opciones.desierto) {
    // Centro de Phoenix (27/10): estuco de colores calidos del desierto
    // (arena, terracota, melocoton, adobe), tiendas con toldo y alguna
    // torre de cristal. Tambien se elige despues de lo normal.
    const p = elegir(azar, ["planta_lisa", "planta_lisa", "planta_balcones", "planta_cristal", "planta_miradores"]);
    const c = p === "planta_cristal" ? elegir(azar, [0xd9dbe0, 0xcfd8de]) : elegir(azar, [0xe8cfa6, 0xd9a877, 0xf0c9a0, 0xc98e66, 0xf3ece0, 0xe6b88a, 0xd8c2a0, 0xe9d6b8]);
    estilo = { planta: p, noble: p, color: c, colorBajo: azar() < 0.5 ? c : elegir(azar, [0xf3ece0, 0xe8cfa6, 0xc98e66]),
      bajo: azar() < 0.75 ? "bajo_tiendas" : "bajo_grande", cornisa: p === "planta_cristal" ? "cornisa_simple" : (azar() < 0.6 ? "cornisa_simple" : "cornisa_deco"),
      remate: azar() < 0.15 ? "remate_antena" : azar() < 0.15 ? "remate_atico" : null };
  }

  const est = ESTILOS[opciones.estilo];
  if (est) {
    // (Se elige despues de lo normal, como los otros: no cambia los niveles de antes.)
    const p = elegir(azar, est.plantas);
    const c = p === "planta_ladrillo" ? elegir(azar, est.ladrillos) : p === "planta_cristal" ? elegir(azar, est.cristal || [0xd9dbe0, 0xcfd8de]) : elegir(azar, est.piedras);
    estilo = { planta: p, noble: azar() < 0.3 && p !== "planta_cristal" ? "planta_frontones" : p, color: c,
      colorBajo: azar() < 0.6 ? c : elegir(azar, est.piedras), bajo: elegir(azar, est.bajos || BAJOS),
      cornisa: p === "planta_cristal" ? "cornisa_simple" : elegir(azar, est.cornisas),
      remate: azar() < est.remate[1] ? est.remate[0] : null };
    toldo = elegir(azar, est.toldos);
    rotulo = elegir(azar, est.rotulos);
  }

  let grande = null;
  if (opciones.vegas) {
    // Strip de Las Vegas (29/10): hoteles y casinos claros, de cristal o con
    // balcones, entrada grande o tiendas, rotulos de neon y un letrero
    // grande en el tejado. Se elige despues de lo normal, como los otros.
    const p = elegir(azar, ["planta_cristal", "planta_balcones", "planta_lisa", "planta_miradores", "planta_cristal"]);
    const c = p === "planta_cristal" ? elegir(azar, [0xe8d08a, 0xbfe3e0, 0xd9dbe0, 0xd8c8f0]) : elegir(azar, COLORES_VEGAS);
    estilo = { planta: p, noble: p, color: c, colorBajo: azar() < 0.5 ? c : elegir(azar, COLORES_VEGAS),
      bajo: azar() < 0.55 ? "bajo_tiendas" : "bajo_grande", cornisa: p === "planta_cristal" ? "cornisa_simple" : "cornisa_deco",
      remate: azar() < 0.15 ? "remate_antena" : null };
    rotuloV = { texto: elegir(azar, ROTULOS_VEGAS), fondo: elegir(azar, ["#1d1030", "#141826", "#2a0f22"]), letra: elegir(azar, NEONES) };
    if (azar() < 0.7) grande = { texto: elegir(azar, GRANDES_VEGAS), letra: elegir(azar, NEONES) };
  }

  for (let c = 0; c < columnas; c++) {
    const col = new THREE.Group();
    col.position.x = -ancho / 2 + anchoCol * (c + 0.5);
    col.scale.x = sx;
    g.add(col);
    const b = pieza(estilo.bajo, tintes, estilo.colorBajo);
    if (b) col.add(b);
    if (estilo.bajo === "bajo_tiendas") {
      for (const x of [-6.4, 0, 6.4]) {
        const t = pieza("toldo_kit", tintes, toldo);
        if (t) { t.position.set(x, 3.25, 0); col.add(t); }
      }
      // El rotulo, en la banda de encima de los escaparates (sin estirar).
      const tx = rotuloV ? texturaRotulo(rotuloV.texto, rotuloV.fondo, rotuloV.letra, true) : texturaRotulo(rotulo, fondoRotulo, letraRotulo);
      const r = new THREE.Mesh(rotuloGeo, new THREE.MeshBasicMaterial({ map: tx }));
      r.scale.set(9 / sx, 0.75, 1);
      r.position.set(0, 4.17, 0.24);
      col.add(r);
    }
    let z = 4.6;
    for (let k = 0; k < plantas; k++) {
      const p = pieza(k === 0 ? estilo.noble : estilo.planta, tintes, estilo.color);
      if (p) { p.position.y = z; col.add(p); }
      z += 3.0;
    }
    const co = pieza(estilo.cornisa, tintes, estilo.color);
    if (co) { co.position.y = z; col.add(co); }
    const alto = z + 1.2;
    if (grande && c === 0) {
      // El letrero grande del tejado, de pie sobre la cornisa.
      const r = new THREE.Mesh(rotuloGeo, new THREE.MeshBasicMaterial({ map: texturaRotulo(grande.texto, "#140c22", grande.letra, true) }));
      r.scale.set(15 / sx, 2.8, 1);
      r.position.set(0, alto + 1.5, 0.4);
      col.add(r);
    }
    if (estilo.remate && c === columnas - 1) {
      const re = pieza(estilo.remate, tintes, estilo.remate === "remate_mansarda" ? 0xb8c2cc : estilo.color);
      if (re) { re.position.y = alto - (estilo.cornisa === "cornisa_simple" ? 0.7 : 0); col.add(re); }
    }
    if (opciones.nieve) {
      // Des Moines (01/11): una capa de nieve sobre el tejado plano.
      const pl = medidas("kit/" + estilo.planta);
      if (pl) {
        let m = tintes.get("nieve");
        if (!m) { m = pl.material.clone(); m.map = null; m.color.set(0xf2f6fa); tintes.set("nieve", m); }
        const s = new THREE.Mesh(nieveGeo, m);
        s.scale.set(19.2, 0.4, Math.max(1, pl.fondo - 0.8));
        s.position.set(0, alto - (estilo.cornisa === "cornisa_simple" ? 0.7 : 0), pl.frente - pl.fondo / 2);
        col.add(s);
      }
    }
  }
  return juntarPorMaterial(g, ancho);
}

// 27/10/2026: las piezas que comparten material (todas las plantas iguales,
// los tres toldos...) se juntan en una sola malla. Un edificio pasaba de ~15
// llamadas de dibujo a ~6, y en la calle hay unos treinta a la vez. El rotulo
// (textura propia) va aparte. Lo juntado es de este edificio solo: al quitarlo
// de la calle hay que soltarlo (soltarEdificio).
function juntarPorMaterial(g, ancho) {
  g.updateMatrixWorld(true);
  const porMat = new Map();
  const aparte = [];
  g.traverse((o) => {
    if (!o.isMesh) return;
    if (o.material.isMeshBasicMaterial) { aparte.push(o); return; }
    if (!porMat.has(o.material)) porMat.set(o.material, []);
    porMat.get(o.material).push(o);
  });
  const nuevo = new THREE.Group();
  for (const [mat, mallas] of porMat) {
    const geos = mallas.map((m) => m.geometry.clone().applyMatrix4(m.matrixWorld));
    const junta = mallas.length > 1 ? mergeGeometries(geos, false) : geos[0];
    if (mallas.length > 1) geos.forEach((x) => x.dispose());
    const malla = new THREE.Mesh(junta || mallas[0].geometry, mat);
    malla.userData.propia = !!junta;
    nuevo.add(malla);
  }
  for (const o of aparte) {
    const c = new THREE.Mesh(o.geometry, o.material);
    c.applyMatrix4(o.matrixWorld);
    nuevo.add(c);
  }
  nuevo.userData.ancho = ancho;
  nuevo.userData.frente = 1.3;
  nuevo.userData.kit = true;
  return nuevo;
}

// Suelta de la memoria lo que era solo de un edificio del kit.
export function soltarEdificio(g) {
  if (!g.userData.kit) return;
  g.traverse((o) => {
    if (!o.isMesh) return;
    if (o.userData.propia) o.geometry.dispose();
    o.material.dispose();
  });
}
