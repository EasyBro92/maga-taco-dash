// Los líderes (10/11/2026). Isidro: «los premios se sienten muy sosos y sin
// ningún significado, cámbialos a nuevos personajes como Netanyahu, Vladimir
// Putin, Kim Jong-un y presidentes polémicos del mundo».
//
// Salen de la caja sorpresa (ruleta). Cada uno corre con el cuerpo del muñeco
// de piezas y su cabeza de Blender (blender/lideres.py), tiene su ventaja al
// empezar cada carrera y sus frases. El presidente de siempre es "trump".
// Los colores (piel, cejas, traje) van a juego con los de lideres.py.

import { getSave, persistSave } from "./save.js";
import { getLang } from "./i18n.js";

export const RAREZAS = {
  raro: { color: "#4b69ff", es: "Raro", en: "Rare" },
  epico: { color: "#d32ce6", es: "Épico", en: "Epic" },
  legendario: { color: "#e4ae39", es: "Legendario", en: "Legendary" },
};

// ventaja: el potenciador con el que empieza cada carrera (main.js, regaloLider).
export const LIDERES = [
  {
    id: "putin", corto: "Putin", rareza: "legendario", ventaja: "magnet", gesto: "pistolero",
    nombre: { es: "Vladimir Putin", en: "Vladimir Putin" },
    titulo: { es: "Se queda con todo: empieza con imán", en: "Takes it all: starts with a magnet" },
    piel: 0xf3c9ad, ceja: 0xa8916f, traje: 0x2f333b, corbata: 0x55627a, ancho: 0.96,
    frases: {
      es: ["¡Es una operación especial!", "¿Elecciones? Ya las gané.", "Lo tuyo es mío, camarada.", "Yo no he estado aquí.", "¡Todo el gas para mí!"],
      en: ["It's a special operation!", "Elections? I already won.", "What's yours is mine, comrade.", "I was never here.", "All the gas is mine!"],
    },
  },
  {
    id: "kim", corto: "Kim", rareza: "legendario", ventaja: "mega",
    nombre: { es: "Kim Jong-un", en: "Kim Jong-un" },
    titulo: { es: "Líder Supremo: empieza gigante", en: "Supreme Leader: starts giant" },
    piel: 0xf6d2ac, ceja: 0x1a1a1c, traje: 0x26282d, corbata: null, ancho: 1.16, gordo: 1.12,
    frases: {
      es: ["¡Aplaudid o nada!", "¡Misil de prueba!", "¡Este peinado es obligatorio!", "¡El Querido Líder nunca tropieza!", "¡Tengo un botón más grande!"],
      en: ["Clap or else!", "Test missile!", "This haircut is mandatory!", "The Dear Leader never trips!", "My button is bigger!"],
    },
  },
  {
    id: "netanyahu", corto: "Bibi", rareza: "epico", ventaja: "shield",
    nombre: { es: "Bibi Netanyahu", en: "Bibi Netanyahu" },
    titulo: { es: "Cúpula de Hierro: empieza con escudo", en: "Iron Dome: starts with a shield" },
    piel: 0xefc2a1, ceja: 0xc8c5be, traje: 0x1f2a44, corbata: 0x5a8fd8, ancho: 1.0,
    frases: {
      es: ["¡Cúpula de Hierro activada!", "¿El juicio? Luego, que tengo prisa.", "¡Esto es un complot!", "¡Bibi no se rinde!", "¡Otra vez yo de primero!"],
      en: ["Iron Dome activated!", "The trial? Later, I'm busy.", "It's a conspiracy!", "Bibi never quits!", "Me first, again!"],
    },
  },
  {
    id: "xi", corto: "Xi", rareza: "epico", ventaja: "doble",
    nombre: { es: "Xi Jinping", en: "Xi Jinping" },
    titulo: { es: "Made in China: empieza con tacos dobles", en: "Made in China: starts with double tacos" },
    piel: 0xf4d0a6, ceja: 0x1c1c1e, traje: 0x24272e, corbata: 0xc0272d, ancho: 1.05,
    frases: {
      es: ["¡Esto lo fabriqué yo!", "¡Aranceles para ti también!", "No me compares con Winnie Pooh.", "¡Todo es Made in China!", "¡Presidente para siempre!"],
      en: ["I made this!", "Tariffs for you too!", "Don't compare me to Winnie the Pooh.", "Everything is Made in China!", "President forever!"],
    },
  },
  {
    id: "milei", corto: "Milei", rareza: "raro", ventaja: "botas",
    nombre: { es: "Javier Milei", en: "Javier Milei" },
    titulo: { es: "¡Afuera!: empieza con botas de salto", en: "Afuera!: starts with jump boots" },
    piel: 0xf1c4a0, ceja: 0x4a2e19, traje: 0x1d1e22, corbata: 0x18181b, ancho: 1.0,
    frases: {
      es: ["¡AFUERA!", "¡Viva la libertad, carajo!", "¡Motosierra al gasto!", "¡No hay plata!", "¡La casta tiene miedo!"],
      en: ["AFUERA!", "Long live freedom, dammit!", "Chainsaw the spending!", "There's no money!", "The elite is scared!"],
    },
  },
  {
    id: "maduro", corto: "Maduro", rareza: "raro", ventaja: "boost",
    nombre: { es: "Nicolás Maduro", en: "Nicolás Maduro" },
    titulo: { es: "Turbo bolivariano: empieza acelerando", en: "Bolivarian turbo: starts with a boost" },
    piel: 0xd8a27c, ceja: 0x221c19, traje: 0x2140a0, corbata: null, ancho: 1.08,
    frases: {
      es: ["¡Me lo dijo un pajarito!", "¡Es culpa del imperio!", "¡Los votos los cuento yo!", "¡A bailar salsa!", "¡Chándal presidencial!"],
      en: ["A little bird told me!", "It's the empire's fault!", "I count the votes!", "Let's dance salsa!", "Presidential tracksuit!"],
    },
  },
  {
    id: "bolsonaro", corto: "Bolsonaro", rareza: "raro", ventaja: "magnet",
    nombre: { es: "Jair Bolsonaro", en: "Jair Bolsonaro" },
    titulo: { es: "Talkey: empieza con imán", en: "Talkey: starts with a magnet" },
    piel: 0xf0c4a3, ceja: 0x595350, traje: 0x2b3346, corbata: 0x2fa84f, ancho: 1.0,
    frases: {
      es: ["¡Es solo una gripecita!", "¡Talkey!", "¡Brasil por encima de todo!", "¡Yo no pierdo, me roban!", "¡A la playa en moto!"],
      en: ["It's just a little flu!", "Talkey!", "Brazil above everything!", "I don't lose, I get robbed!", "Beach ride on my motorbike!"],
    },
  },
  {
    id: "erdogan", corto: "Erdoğan", rareza: "raro", ventaja: "shield",
    nombre: { es: "Recep Erdoğan", en: "Recep Erdoğan" },
    titulo: { es: "Sultán blindado: empieza con escudo", en: "Armoured sultan: starts with a shield" },
    piel: 0xeab995, ceja: 0xbab4ab, traje: 0x2a2d35, corbata: 0x7a1f2a, ancho: 1.02,
    frases: {
      es: ["¡One minute!", "¡Mi palacio tiene mil habitaciones!", "¡El sultán no espera!", "¡Bloqueo esta calle!", "¡Té para todos!"],
      en: ["One minute!", "My palace has a thousand rooms!", "The sultan doesn't wait!", "I'm blocking this street!", "Tea for everyone!"],
    },
  },
];

export const liderDe = (id) => LIDERES.find((l) => l.id === id) || null;
export const nombreLider = (l) => (l ? l.nombre[getLang()] || l.nombre.es : "Donald Trump");
export const tituloLider = (l) => l.titulo[getLang()] || l.titulo.es;
export const fotoLider = (id) => `models/lideres/${id}.png`;

export function lideresTengo() {
  return getSave().lideres || [];
}
export function tengoLider(id) {
  return lideresTengo().includes(id);
}
export function darLider(id) {
  const s = getSave();
  s.lideres = s.lideres || [];
  if (!s.lideres.includes(id)) s.lideres.push(id);
  persistSave();
}
// El que corre ahora (null: el presidente de siempre).
export function liderPuesto() {
  const id = getSave().lider;
  return id && tengoLider(id) ? id : null;
}
export function ponerLider(id) {
  getSave().lider = id && id !== "trump" ? id : null;
  persistSave();
}
// Para la ruleta: uno de esa rareza que aún no se tenga (o null).
export function liderLibre(rareza) {
  const libres = LIDERES.filter((l) => l.rareza === rareza && !tengoLider(l.id));
  return libres.length ? libres[Math.floor(Math.random() * libres.length)] : null;
}
