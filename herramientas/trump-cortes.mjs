// Las frases con su voz de verdad: de qué grabación sale cada una (31/10/2026).
// Lo usan trump-afinar.mjs y trump.mjs. Ver trump.mjs.
import fs from "node:fs";

// texto del juego → [grabación, palabras que dice (como las escribe whisper), cuál de las veces (0 = la primera, -1 = la última)]
export const CORTES = {
  "THIS IS FAKE NEWS!": ["fake_news_rusia", "this is fake news", 0],
  "RUSSIA IS FAKE NEWS!": ["fake_news_rusia", "russia is fake news", 0],
  "FAKE. PHONY. FAKE!": ["fake_news_cpac", "it's fake fony fake", 0],
  "IT'S A WITCH HUNT AND IT'S A DISGRACE!": ["very_sad_manafort", "it's a witch hunt and it's a disgrace", 0],
  "IT'S A VERY SAD THING.": ["very_sad_manafort", "it's a very sad thing", 0],
  "TREMENDOUS!": ["tremendous_trade", "tremendous", 0],
  "IT'S INCREDIBLE!": ["tremendous_trade", "it's incredible", 0],
  "THEY'RE VERY DISHONEST PEOPLE.": ["fake_news_cpac", "they're very dishonest people", 0],
  "THE ENEMY OF THE PEOPLE!": ["fake_news_cpac", "the enemy of the people", 0],
  "AMERICA FIRST!": ["investidura_2017", "america first", 0],
  "WE WILL MAKE AMERICA GREAT AGAIN!": ["investidura_2017", "we will make america great again", 0],
  "WINNING LIKE NEVER BEFORE!": ["investidura_2017", "winning like never before", 0],
  "WE WILL BRING BACK OUR JOBS!": ["investidura_2017", "we will bring back our jobs", 0],
  "WE WILL BRING BACK OUR BORDERS!": ["investidura_2017", "we will bring back our borders", 0],
  "BUY AMERICAN AND HIRE AMERICAN!": ["investidura_2017", "buy american and hire american", 0],
  "GOD BLESS AMERICA!": ["investidura_2017", "god bless america", 0],
  "WE WILL WIN!": ["cien_dias", "we will win", -1],
  "YOU WILL NEVER BE IGNORED AGAIN!": ["investidura_2017", "you will never be ignored again", 0],
};

// WAV de 16 bits y una pista.
export function guardarWav(ruta, d, hz) {
  const b = Buffer.alloc(44 + d.length * 2);
  b.write("RIFF", 0); b.writeUInt32LE(36 + d.length * 2, 4); b.write("WAVEfmt ", 8);
  b.writeUInt32LE(16, 16); b.writeUInt16LE(1, 20); b.writeUInt16LE(1, 22); b.writeUInt32LE(hz, 24);
  b.writeUInt32LE(hz * 2, 28); b.writeUInt16LE(2, 32); b.writeUInt16LE(16, 34); b.write("data", 36); b.writeUInt32LE(d.length * 2, 40);
  for (let i = 0; i < d.length; i++) b.writeInt16LE(Math.max(-32768, Math.min(32767, Math.round(d[i] * 32767))), 44 + i * 2);
  fs.writeFileSync(ruta, b);
}
