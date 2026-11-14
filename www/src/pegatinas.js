// Pegatinas 2D del juego (27/10/2026): el taco, la chapa de campaña, el maíz,
// la tortilla y el taco perfecto. Todas con el mismo estilo que el taco que
// eligió Isidro: dibujo plano, borde blanco gordo y contorno marrón. Se usan
// en la pista (como sprites) y en la interfaz (como imagen), así que el
// juego ya no depende de los emojis de cada móvil, que cambian de uno a otro.

const CONTORNO = "#5b3412";
const cache = {};

export function lienzo(nombre) {
  if (cache[nombre]) return cache[nombre];
  const c = document.createElement("canvas");
  c.width = c.height = 256;
  const x = c.getContext("2d");
  x.lineJoin = x.lineCap = "round";
  (DIBUJOS[nombre] || DIBUJOS.taco)(x);
  cache[nombre] = c;
  return c;
}

// Para <img> en la interfaz.
const urls = {};
export function urlPegatina(nombre) {
  if (!urls[nombre]) urls[nombre] = lienzo(nombre).toDataURL("image/png");
  return urls[nombre];
}
export function imgPegatina(nombre, clase = "peg") {
  return `<img class="${clase}" src="${urlPegatina(nombre)}" alt="" draggable="false">`;
}

function estrella(x, cx, cy, r, ri, puntas = 5, giro = -Math.PI / 2) {
  x.beginPath();
  for (let i = 0; i < puntas * 2; i++) {
    const rr = i % 2 ? ri : r;
    const a = giro + (i * Math.PI) / puntas;
    x.lineTo(cx + Math.cos(a) * rr, cy + Math.sin(a) * rr);
  }
  x.closePath();
}

const DIBUJOS = {
  taco(x) {
    const cx = 128, cy = 112, r = 96;
    const relleno = () => {
      x.beginPath();
      x.moveTo(cx - r, cy);
      for (let i = 0; i <= 8; i++) {
        const px = cx - r + (2 * r * i) / 8;
        x.quadraticCurveTo(px - r / 8, cy - 46 - (i % 2) * 12, px, cy - 26);
      }
      x.lineTo(cx + r, cy);
      x.closePath();
    };
    x.save();
    x.strokeStyle = "#ffffff"; x.lineWidth = 26;
    relleno(); x.stroke();
    x.beginPath(); x.arc(cx, cy, r, 0, Math.PI); x.closePath(); x.stroke();
    x.restore();
    relleno();
    x.fillStyle = "#5cc93c"; x.fill();
    x.lineWidth = 7; x.strokeStyle = CONTORNO; x.stroke();
    x.fillStyle = "#8b4a22";
    for (const [px, py, pr] of [[-60, -14, 20], [-22, -20, 22], [18, -16, 21], [56, -18, 19]]) {
      x.beginPath(); x.arc(cx + px, cy + py, pr, 0, Math.PI * 2); x.fill();
    }
    for (const [px, py] of [[-44, -34], [6, -40], [46, -36]]) {
      x.beginPath(); x.arc(cx + px, cy + py, 13, 0, Math.PI * 2);
      x.fillStyle = "#ee3b2f"; x.fill();
      x.lineWidth = 4; x.strokeStyle = CONTORNO; x.stroke();
      x.beginPath(); x.arc(cx + px - 4, cy + py - 4, 4, 0, Math.PI * 2);
      x.fillStyle = "#ffb3a8"; x.fill();
    }
    x.strokeStyle = "#ffd84a"; x.lineWidth = 6;
    for (const [px, py, ang] of [[-70, -24, 0.4], [-30, -40, -0.5], [28, -28, 0.6], [70, -26, -0.3], [-6, -24, 0.2]]) {
      x.beginPath();
      x.moveTo(cx + px - Math.cos(ang) * 10, cy + py - Math.sin(ang) * 10);
      x.lineTo(cx + px + Math.cos(ang) * 10, cy + py + Math.sin(ang) * 10);
      x.stroke();
    }
    x.beginPath(); x.arc(cx, cy, r, 0, Math.PI); x.closePath();
    const grad = x.createLinearGradient(0, cy, 0, cy + r);
    grad.addColorStop(0, "#ffd35c"); grad.addColorStop(1, "#f0a42a");
    x.fillStyle = grad; x.fill();
    x.save(); x.clip();
    x.fillStyle = "rgba(196,110,30,0.55)";
    for (const [px, py, pr] of [[-56, 26, 7], [-20, 52, 6], [24, 34, 8], [60, 18, 6], [8, 74, 5], [-48, 60, 5], [52, 56, 6]]) {
      x.beginPath(); x.arc(cx + px, cy + py, pr, 0, Math.PI * 2); x.fill();
    }
    x.strokeStyle = "rgba(255,255,255,0.55)"; x.lineWidth = 9;
    x.beginPath(); x.arc(cx, cy, r - 18, Math.PI * 0.62, Math.PI * 0.86); x.stroke();
    x.restore();
    x.lineWidth = 8; x.strokeStyle = CONTORNO;
    x.beginPath(); x.arc(cx, cy, r, 0, Math.PI); x.closePath(); x.stroke();
  },

  // Urna con la papeleta (28/10/2026): cada estado ganado. Sustituye a los
  // ingredientes del taco de la historia de antes.
  voto(x) {
    const caja = () => { x.beginPath(); x.roundRect(46, 112, 164, 112, 14); };
    const papel = () => { x.beginPath(); x.roundRect(-46, -66, 92, 112, 8); };
    x.save();                                                           // borde blanco
    x.strokeStyle = "#ffffff"; x.lineWidth = 26;
    caja(); x.stroke();
    x.translate(128, 86); x.rotate(-0.12); papel(); x.stroke();
    x.restore();
    x.save();                                                           // la papeleta con la cruz roja
    x.translate(128, 86); x.rotate(-0.12);
    papel(); x.fillStyle = "#ffffff"; x.fill(); x.lineWidth = 7; x.strokeStyle = CONTORNO; x.stroke();
    x.lineWidth = 6; x.strokeStyle = "#c9d2e0";
    for (const yy of [16, 30]) { x.beginPath(); x.moveTo(-28, yy); x.lineTo(28, yy); x.stroke(); }
    x.lineWidth = 16; x.strokeStyle = "#e8463c";
    x.beginPath(); x.moveTo(-24, -24); x.lineTo(-6, -4); x.lineTo(26, -44); x.stroke();
    x.restore();
    caja();                                                             // la urna, por delante
    const g = x.createLinearGradient(0, 112, 0, 224);
    g.addColorStop(0, "#3f7ef0"); g.addColorStop(1, "#1f4fb0");
    x.fillStyle = g; x.fill(); x.lineWidth = 8; x.strokeStyle = CONTORNO; x.stroke();
    x.fillStyle = "#16306e"; x.beginPath(); x.roundRect(82, 121, 92, 10, 5); x.fill();   // ranura
    x.fillStyle = "#ffffff"; x.fillRect(50, 160, 156, 30);             // franja con estrella
    estrella(x, 128, 176, 20, 8); x.fillStyle = "#e8463c"; x.fill();
  },

  // Chapa de campaña: roja, blanca y azul con la estrella en medio.
  chapa(x) {
    const cx = 128, cy = 128;
    x.beginPath(); x.arc(cx, cy, 116, 0, Math.PI * 2);
    x.fillStyle = "#ffffff"; x.fill();
    x.beginPath(); x.arc(cx, cy, 104, 0, Math.PI * 2);
    x.fillStyle = "#e8463c"; x.fill();
    x.lineWidth = 8; x.strokeStyle = CONTORNO; x.stroke();
    x.beginPath(); x.arc(cx, cy, 84, 0, Math.PI * 2);
    x.fillStyle = "#ffffff"; x.fill();
    x.beginPath(); x.arc(cx, cy, 70, 0, Math.PI * 2);
    const g = x.createLinearGradient(0, cy - 70, 0, cy + 70);
    g.addColorStop(0, "#3f7ef0"); g.addColorStop(1, "#1f4fb0");
    x.fillStyle = g; x.fill();
    estrella(x, cx, cy + 4, 50, 21);
    x.fillStyle = "#ffd23f"; x.fill();
    x.lineWidth = 5; x.strokeStyle = "#b07a00"; x.stroke();
    for (let i = 0; i < 12; i++) {                                     // puntitos del aro
      const a = (i / 12) * Math.PI * 2;
      x.beginPath(); x.arc(cx + Math.cos(a) * 94, cy + Math.sin(a) * 94, 4, 0, Math.PI * 2);
      x.fillStyle = "#ffffff"; x.fill();
    }
    x.strokeStyle = "rgba(255,255,255,0.7)"; x.lineWidth = 10;      // brillo de chapa
    x.beginPath(); x.arc(cx, cy, 92, Math.PI * 1.08, Math.PI * 1.42); x.stroke();
  },

  // 05/11: los objetos de cada ciudad (diez por nivel, con su premio).
  // La Gran Manzana (Nueva York).
  manzana(x) {
    const cuerpo = () => {
      x.beginPath();
      x.moveTo(128, 86);
      x.bezierCurveTo(162, 60, 224, 74, 220, 142);
      x.bezierCurveTo(216, 198, 174, 230, 142, 216);
      x.bezierCurveTo(134, 212, 122, 212, 114, 216);
      x.bezierCurveTo(82, 230, 40, 198, 36, 142);
      x.bezierCurveTo(32, 74, 94, 60, 128, 86);
      x.closePath();
    };
    const hoja = () => { x.beginPath(); x.ellipse(164, 50, 30, 14, -0.5, 0, Math.PI * 2); };
    x.lineWidth = 26; x.strokeStyle = "#fff"; cuerpo(); x.stroke(); hoja(); x.stroke();
    x.beginPath(); x.moveTo(128, 88); x.lineTo(138, 40); x.stroke();
    x.lineWidth = 12; x.strokeStyle = CONTORNO;                       // el rabito
    x.beginPath(); x.moveTo(128, 90); x.quadraticCurveTo(130, 62, 140, 42); x.stroke();
    hoja(); x.fillStyle = "#3fae3a"; x.fill(); x.lineWidth = 6; x.stroke();
    cuerpo();
    const g = x.createLinearGradient(40, 70, 210, 220);
    g.addColorStop(0, "#ff5a48"); g.addColorStop(1, "#b81c22");
    x.fillStyle = g; x.fill(); x.lineWidth = 8; x.strokeStyle = CONTORNO; x.stroke();
    x.fillStyle = "rgba(255,255,255,0.65)";                            // brillo
    x.beginPath(); x.ellipse(84, 124, 14, 30, 0.35, 0, Math.PI * 2); x.fill();
  },

  // La bandera (Findlay es «Flag City, USA»).
  bandera(x) {
    const tela = () => {
      x.beginPath();
      x.moveTo(66, 52);
      x.bezierCurveTo(110, 30, 160, 76, 218, 50);
      x.lineTo(218, 152);
      x.bezierCurveTo(160, 178, 110, 132, 66, 154);
      x.closePath();
    };
    x.lineWidth = 26; x.strokeStyle = "#fff"; tela(); x.stroke();
    x.beginPath(); x.moveTo(58, 34); x.lineTo(58, 232); x.stroke();
    x.lineWidth = 14; x.strokeStyle = "#8a5a2b";                      // el mastil
    x.beginPath(); x.moveTo(58, 38); x.lineTo(58, 228); x.stroke();
    x.fillStyle = "#ffd23f"; x.beginPath(); x.arc(58, 32, 11, 0, Math.PI * 2); x.fill();
    x.save();
    tela(); x.clip();
    x.fillStyle = "#ffffff"; x.fillRect(60, 20, 170, 170);
    x.fillStyle = "#e8463c";                                          // las rayas, ondeando
    for (let i = 0; i < 7; i += 2) {
      const y0 = 52 + i * 14.6;
      x.beginPath();
      x.moveTo(60, y0 + 4); x.bezierCurveTo(110, y0 - 18, 160, y0 + 28, 222, y0);
      x.lineTo(222, y0 + 14.6); x.bezierCurveTo(160, y0 + 42, 110, y0 - 4, 60, y0 + 18);
      x.closePath(); x.fill();
    }
    x.fillStyle = "#1f4fb0"; x.fillRect(60, 30, 70, 70);             // el cuadro azul
    x.fillStyle = "#ffffff";
    for (const [sx, sy] of [[80, 56], [108, 52], [94, 78], [120, 76]]) { estrella(x, sx, sy, 9, 4); x.fill(); }
    x.restore();
    tela(); x.lineWidth = 7; x.strokeStyle = CONTORNO; x.stroke();
  },

  // La placa de sheriff (el Viejo Oeste de Arizona).
  placa(x) {
    const cx = 128, cy = 132;
    x.lineWidth = 26; x.strokeStyle = "#fff";
    estrella(x, cx, cy, 100, 54, 6); x.stroke();
    const puntas = [];
    for (let i = 0; i < 6; i++) { const a = -Math.PI / 2 + (i * Math.PI) / 3; puntas.push([cx + Math.cos(a) * 100, cy + Math.sin(a) * 100]); }
    for (const [px, py] of puntas) { x.beginPath(); x.arc(px, py, 14, 0, Math.PI * 2); x.stroke(); }
    const g = x.createLinearGradient(0, cy - 100, 0, cy + 100);
    g.addColorStop(0, "#ffe27a"); g.addColorStop(1, "#d39a14");
    estrella(x, cx, cy, 100, 54, 6); x.fillStyle = g; x.fill(); x.lineWidth = 7; x.strokeStyle = CONTORNO; x.stroke();
    for (const [px, py] of puntas) { x.beginPath(); x.arc(px, py, 14, 0, Math.PI * 2); x.fillStyle = "#ffd23f"; x.fill(); x.lineWidth = 6; x.stroke(); }
    x.beginPath(); x.arc(cx, cy, 40, 0, Math.PI * 2); x.fillStyle = "#f3c13a"; x.fill();
    x.lineWidth = 6; x.strokeStyle = "#a8740a"; x.stroke();
    estrella(x, cx, cy + 2, 24, 10); x.fillStyle = "#a8740a"; x.fill();
    x.strokeStyle = "rgba(255,255,255,0.7)"; x.lineWidth = 9;        // brillo
    x.beginPath(); x.moveTo(cx - 60, cy - 20); x.lineTo(cx - 34, cy - 58); x.stroke();
  },

  // 08/11: el bote de laca de Chicago (para que el viento no le levante el tupe).
  laca(x) {
    x.save();
    x.translate(124, 140); x.scale(0.9, 0.9); x.rotate(-0.12);
    x.lineJoin = "round";
    const bote = () => {
      x.beginPath();
      x.moveTo(-44, -60); x.quadraticCurveTo(-44, -76, -28, -76); x.lineTo(28, -76); x.quadraticCurveTo(44, -76, 44, -60);
      x.lineTo(44, 84); x.quadraticCurveTo(44, 100, 28, 100); x.lineTo(-28, 100); x.quadraticCurveTo(-44, 100, -44, 84);
      x.closePath();
    };
    const tapa = () => { x.beginPath(); x.moveTo(-30, -76); x.quadraticCurveTo(-30, -112, 0, -112); x.quadraticCurveTo(30, -112, 30, -76); x.closePath(); };
    x.lineWidth = 24; x.strokeStyle = "#fff"; bote(); x.stroke(); tapa(); x.stroke();
    x.beginPath(); x.arc(58, -118, 26, 0, Math.PI * 2); x.stroke();
    bote(); x.fillStyle = "#e8b33a"; x.fill();
    x.fillStyle = "#f6d36a"; x.fillRect(-30, -66, 12, 156);
    x.fillStyle = "#d8202a"; x.fillRect(-44, -10, 88, 52);
    // La estrella blanca en la etiqueta.
    x.fillStyle = "#fbf8f2";
    x.beginPath();
    for (let i = 0; i < 10; i++) { const a = -Math.PI / 2 + i * Math.PI / 5, rr = i % 2 ? 9 : 21; x.lineTo(Math.cos(a) * rr, 16 + Math.sin(a) * rr); }
    x.closePath(); x.fill();
    tapa(); x.fillStyle = "#2f6bd8"; x.fill();
    x.fillStyle = "#fbf8f2"; x.fillRect(-6, -122, 12, 12);
    // La nube de laca.
    x.fillStyle = "rgba(190,225,255,0.95)";
    for (const [px, py, rr] of [[40, -118, 12], [58, -130, 10], [66, -108, 11], [78, -124, 8]]) { x.beginPath(); x.arc(px, py, rr, 0, Math.PI * 2); x.fill(); }
    x.lineWidth = 7; x.strokeStyle = CONTORNO; bote(); x.stroke(); tapa(); x.stroke();
    x.restore();
  },

  // 09/11: la cuña de queso de Milwaukee (Wisconsin, el estado del queso).
  queso(x) {
    x.save();
    x.translate(128, 150); x.rotate(-0.08);
    x.lineJoin = "round";
    const cuna = () => {
      x.beginPath();
      x.moveTo(-96, 50); x.lineTo(96, 50); x.lineTo(96, -20); x.lineTo(-96, -60); x.closePath();
    };
    const tapa = () => { x.beginPath(); x.moveTo(-96, -60); x.lineTo(96, -20); x.lineTo(60, -62); x.closePath(); };
    x.lineWidth = 24; x.strokeStyle = "#fff"; cuna(); x.stroke(); tapa(); x.stroke();
    cuna(); x.fillStyle = "#f2b632"; x.fill();
    tapa(); x.fillStyle = "#f8d468"; x.fill();
    // Los agujeros.
    x.fillStyle = "#c8901e";
    for (const [px, py, rr] of [[-50, 0, 14], [10, 20, 18], [55, -2, 10], [-10, -22, 9], [70, 30, 8], [-70, 30, 9]]) { x.beginPath(); x.arc(px, py, rr, 0, Math.PI * 2); x.fill(); }
    x.fillStyle = "#e09a22";
    for (const [px, py, rr] of [[20, -42, 7], [50, -40, 5]]) { x.beginPath(); x.ellipse(px, py, rr * 1.4, rr * 0.6, 0, 0, Math.PI * 2); x.fill(); }
    x.lineWidth = 7; x.strokeStyle = CONTORNO; cuna(); x.stroke(); tapa(); x.stroke();
    x.restore();
  },

  // 13/11: el diamante de la mina de Little Rock.
  diamante(x) {
    x.save();
    x.translate(128, 132);
    x.lineJoin = "round";
    const gema = () => { x.beginPath(); x.moveTo(-90, -30); x.lineTo(-50, -80); x.lineTo(50, -80); x.lineTo(90, -30); x.lineTo(0, 92); x.closePath(); };
    x.lineWidth = 26; x.strokeStyle = "#fff"; gema(); x.stroke();
    gema(); x.fillStyle = "#9fe6f6"; x.fill();
    x.fillStyle = "#d8f8ff";
    x.beginPath(); x.moveTo(-50, -80); x.lineTo(-20, -30); x.lineTo(20, -30); x.lineTo(50, -80); x.closePath(); x.fill();
    x.fillStyle = "#6fc8e0";
    x.beginPath(); x.moveTo(-90, -30); x.lineTo(90, -30); x.lineTo(0, 92); x.closePath(); x.globalAlpha = 0.35; x.fill(); x.globalAlpha = 1;
    x.strokeStyle = "#5aaecc"; x.lineWidth = 4;
    for (const [a, b] of [[[-20, -30], [0, 92]], [[20, -30], [0, 92]], [[-90, -30], [90, -30]]]) { x.beginPath(); x.moveTo(...a); x.lineTo(...b); x.stroke(); }
    x.lineWidth = 7; x.strokeStyle = CONTORNO; gema(); x.stroke();
    x.restore();
  },
  // 13/11: la pajita de plástico de Jackson (doblada, roja y blanca).
  // 14/11: la guitarra de Nashville.
  guitarra(x) {
    x.save();
    x.translate(128, 128); x.rotate(0.6);
    const forma = () => {
      x.beginPath();
      x.ellipse(0, 52, 56, 50, 0, 0, Math.PI * 2);
      x.ellipse(0, -8, 40, 36, 0, 0, Math.PI * 2);
      x.rect(-11, -108, 22, 80);
      x.rect(-17, -124, 34, 24);
    };
    x.lineJoin = "round";
    x.lineWidth = 30; x.strokeStyle = "#fff"; forma(); x.stroke();
    x.lineWidth = 8; x.strokeStyle = CONTORNO; forma(); x.stroke();
    x.fillStyle = "#d88a2a"; x.beginPath(); x.ellipse(0, 52, 56, 50, 0, 0, Math.PI * 2); x.fill();
    x.beginPath(); x.ellipse(0, -8, 40, 36, 0, 0, Math.PI * 2); x.fill();
    x.fillStyle = "#6a3a1e"; x.fillRect(-11, -108, 22, 96); x.fillRect(-17, -124, 34, 24);
    x.fillStyle = "#2a1a12"; x.beginPath(); x.arc(0, 22, 18, 0, Math.PI * 2); x.fill();
    x.fillStyle = "#3a2416"; x.fillRect(-24, 70, 48, 9);
    x.strokeStyle = "#f4f0e8"; x.lineWidth = 1.6;
    for (const dx of [-6, -2, 2, 6]) { x.beginPath(); x.moveTo(dx, -104); x.lineTo(dx * 2.4, 74); x.stroke(); }
    x.fillStyle = "rgba(255,255,255,0.45)"; x.beginPath(); x.ellipse(-26, 34, 9, 18, 0.5, 0, Math.PI * 2); x.fill();
    x.restore();
  },
  // 14/11: la piña de la hospitalidad (Charleston).
  pina(x) {
    x.save();
    x.translate(128, 150);
    x.lineJoin = "round";
    const cuerpo = () => { x.beginPath(); x.ellipse(0, 10, 58, 76, 0, 0, Math.PI * 2); };
    const hojas = () => {
      x.beginPath();
      for (const [a, l] of [[-0.9, 70], [-0.45, 92], [0, 104], [0.45, 92], [0.9, 70]]) {
        x.moveTo(-14, -58); x.quadraticCurveTo(Math.sin(a) * l * 0.5, -66 - Math.cos(a) * l * 0.5, Math.sin(a) * l, -60 - Math.cos(a) * l);
        x.quadraticCurveTo(Math.sin(a) * l * 0.5 + 10, -60 - Math.cos(a) * l * 0.4, 14, -58);
      }
    };
    x.lineWidth = 28; x.strokeStyle = "#fff"; cuerpo(); x.stroke(); hojas(); x.stroke();
    x.lineWidth = 8; x.strokeStyle = CONTORNO; cuerpo(); x.stroke(); hojas(); x.stroke();
    x.fillStyle = "#4a9a3a"; hojas(); x.fill();
    x.fillStyle = "#f0b830"; cuerpo(); x.fill();
    x.save(); cuerpo(); x.clip();
    x.strokeStyle = "#b07818"; x.lineWidth = 4;
    for (let k = -6; k <= 6; k++) { x.beginPath(); x.moveTo(k * 22 - 80, -80); x.lineTo(k * 22 + 80, 100); x.stroke(); x.beginPath(); x.moveTo(k * 22 + 80, -80); x.lineTo(k * 22 - 80, 100); x.stroke(); }
    x.restore();
    x.fillStyle = "rgba(255,255,255,0.45)"; x.beginPath(); x.ellipse(-26, -10, 10, 22, 0.4, 0, Math.PI * 2); x.fill();
    x.restore();
  },
  // 14/11: el flamenco rosa de Miami.
  flamenco(x) {
    x.save();
    x.translate(128, 128);
    x.lineJoin = "round"; x.lineCap = "round";
    const cuerpo = () => { x.beginPath(); x.ellipse(-6, 22, 50, 32, -0.25, 0, Math.PI * 2); };
    const cuello = () => { x.beginPath(); x.moveTo(30, 6); x.quadraticCurveTo(70, -20, 40, -50); x.quadraticCurveTo(20, -80, 46, -92); };
    const patas = () => { x.beginPath(); x.moveTo(-6, 50); x.lineTo(-6, 112); x.moveTo(8, 50); x.lineTo(24, 80); x.lineTo(2, 84); };
    x.lineWidth = 30; x.strokeStyle = "#fff"; cuerpo(); x.stroke(); cuello(); x.stroke(); patas(); x.stroke();
    x.lineWidth = 20; x.strokeStyle = CONTORNO; cuello(); x.stroke();
    x.lineWidth = 12; patas(); x.stroke();
    x.lineWidth = 8; cuerpo(); x.stroke();
    x.fillStyle = "#f07aa0"; cuerpo(); x.fill();
    x.lineWidth = 12; x.strokeStyle = "#f07aa0"; cuello(); x.stroke();
    x.lineWidth = 5; x.strokeStyle = "#e86a90"; patas(); x.stroke();
    x.fillStyle = "#f07aa0"; x.beginPath(); x.arc(48, -94, 14, 0, Math.PI * 2); x.fill();
    x.fillStyle = "#2a1a1a"; x.beginPath(); x.moveTo(58, -98); x.lineTo(76, -84); x.lineTo(60, -86); x.closePath(); x.fill();
    x.fillStyle = "#fff"; x.beginPath(); x.arc(50, -98, 3.5, 0, Math.PI * 2); x.fill();
    x.fillStyle = "#e05a88"; x.beginPath(); x.ellipse(-20, 18, 26, 14, -0.4, 0, Math.PI * 2); x.fill();
    x.restore();
  },
  // 14/11: los esquís cruzados con los bastones (Denver).
  esquis(x) {
    x.save();
    x.translate(128, 132);
    x.lineJoin = "round"; x.lineCap = "round";
    const esqui = (a) => { x.save(); x.rotate(a); x.beginPath(); x.moveTo(-14, 96); x.lineTo(-14, -80); x.quadraticCurveTo(-14, -112, 0, -116); x.quadraticCurveTo(14, -112, 14, -80); x.lineTo(14, 96); x.closePath(); x.restore(); };
    const baston = (a) => { x.save(); x.rotate(a); x.beginPath(); x.moveTo(0, -104); x.lineTo(0, 100); x.restore(); };
    for (const a of [-0.42, 0.42]) { x.lineWidth = 30; x.strokeStyle = "#fff"; esqui(a); x.stroke(); }
    for (const a of [-0.42, 0.42]) {
      x.lineWidth = 8; x.strokeStyle = CONTORNO; esqui(a); x.stroke();
      x.fillStyle = a < 0 ? "#c8202a" : "#2a5ab8"; esqui(a); x.fill();
      x.save(); x.rotate(a); x.fillStyle = "#f6f4ee"; x.fillRect(-14, -20, 28, 10); x.restore();
    }
    for (const a of [-0.12, 0.12]) { x.lineWidth = 8; x.strokeStyle = CONTORNO; baston(a); x.stroke(); x.lineWidth = 4; x.strokeStyle = "#d8dce0"; baston(a); x.stroke(); }
    x.fillStyle = "rgba(255,255,255,0.45)"; x.beginPath(); x.ellipse(-30, -40, 6, 26, -0.42, 0, Math.PI * 2); x.fill();
    x.restore();
  },
  // 14/11: el globo de la fiesta de Albuquerque (gajos rojos y amarillos).
  globo(x) {
    x.save();
    x.translate(128, 112);
    x.lineJoin = "round"; x.lineCap = "round";
    const tela = () => { x.beginPath(); x.moveTo(-30, 62); x.bezierCurveTo(-118, -10, -70, -104, 0, -104); x.bezierCurveTo(70, -104, 118, -10, 30, 62); x.closePath(); };
    const cesta = () => { x.beginPath(); x.rect(-20, 92, 40, 30); };
    const cuerdas = () => { x.beginPath(); x.moveTo(-28, 62); x.lineTo(-18, 94); x.moveTo(28, 62); x.lineTo(18, 94); };
    x.lineWidth = 28; x.strokeStyle = "#fff"; tela(); x.stroke(); cesta(); x.stroke(); cuerdas(); x.stroke();
    x.lineWidth = 8; x.strokeStyle = CONTORNO; tela(); x.stroke(); cesta(); x.stroke();
    x.lineWidth = 5; cuerdas(); x.stroke();
    x.fillStyle = "#e8402a"; tela(); x.fill();
    x.save(); tela(); x.clip();
    x.fillStyle = "#f6c81e";
    for (const k of [-2, 0, 2]) { x.beginPath(); x.ellipse(k * 26, -20, 12, 110, 0, 0, Math.PI * 2); x.fill(); }
    x.restore();
    x.fillStyle = "#a8783e"; cesta(); x.fill();
    x.strokeStyle = "#7a5228"; x.lineWidth = 3;
    for (const dy of [100, 110]) { x.beginPath(); x.moveTo(-20, dy); x.lineTo(20, dy); x.stroke(); }
    x.fillStyle = "rgba(255,255,255,0.45)"; x.beginPath(); x.ellipse(-40, -50, 12, 26, 0.4, 0, Math.PI * 2); x.fill();
    x.restore();
  },
  // 14/11: el melocotón de Georgia (Atlanta).
  melocoton(x) {
    x.save();
    x.translate(128, 140);
    x.lineJoin = "round";
    const bola = () => { x.beginPath(); x.arc(0, 0, 80, 0, Math.PI * 2); };
    x.lineWidth = 30; x.strokeStyle = "#fff"; bola(); x.stroke();
    x.lineWidth = 8; x.strokeStyle = CONTORNO; bola(); x.stroke();
    const g = x.createRadialGradient(-28, -26, 10, 0, 0, 84);
    g.addColorStop(0, "#ffd08a"); g.addColorStop(0.55, "#f8a060"); g.addColorStop(1, "#e0583e");
    x.fillStyle = g; bola(); x.fill();
    x.strokeStyle = "rgba(190,70,40,0.75)"; x.lineWidth = 5;
    x.beginPath(); x.moveTo(4, -76); x.quadraticCurveTo(-22, 0, 6, 74); x.stroke();
    x.fillStyle = "#5a3a1e"; x.fillRect(-4, -100, 8, 26);
    x.save(); x.translate(26, -92); x.rotate(-0.5);
    const hoja = () => { x.beginPath(); x.ellipse(0, 0, 30, 14, 0, 0, Math.PI * 2); };
    x.lineWidth = 14; x.strokeStyle = "#fff"; hoja(); x.stroke();
    x.lineWidth = 6; x.strokeStyle = CONTORNO; hoja(); x.stroke();
    x.fillStyle = "#5aa040"; hoja(); x.fill();
    x.restore();
    x.fillStyle = "rgba(255,255,255,0.5)"; x.beginPath(); x.ellipse(-36, -30, 14, 22, 0.6, 0, Math.PI * 2); x.fill();
    x.restore();
  },
  // 14/11: la rueda de carreras (Charlotte): goma negra con la raya amarilla y llanta de oro.
  rueda(x) {
    x.save();
    x.translate(128, 128);
    const disco = (r) => { x.beginPath(); x.arc(0, 0, r, 0, Math.PI * 2); };
    x.lineWidth = 30; x.strokeStyle = "#fff"; disco(92); x.stroke();
    x.lineWidth = 8; x.strokeStyle = CONTORNO; disco(92); x.stroke();
    x.fillStyle = "#202024"; disco(92); x.fill();
    x.strokeStyle = "#f0c020"; x.lineWidth = 7; disco(73); x.stroke();
    x.fillStyle = "#e8b840"; disco(50); x.fill();
    x.strokeStyle = "#8a6420"; x.lineWidth = 4; disco(50); x.stroke();
    x.fillStyle = "#b8862a"; disco(18); x.fill();
    x.fillStyle = "#4a3a1a";
    for (let k = 0; k < 5; k++) { const a = k * Math.PI * 2 / 5 - Math.PI / 2; x.beginPath(); x.arc(Math.cos(a) * 32, Math.sin(a) * 32, 6, 0, Math.PI * 2); x.fill(); }
    x.fillStyle = "rgba(255,255,255,0.35)"; x.beginPath(); x.ellipse(-44, -46, 12, 26, 0.75, 0, Math.PI * 2); x.fill();
    x.restore();
  },
  // 14/11: la herradura de la suerte del Derby de Louisville.
  herradura(x) {
    x.save();
    x.translate(128, 122);
    const arco = (ancho, color) => {
      x.lineWidth = ancho; x.strokeStyle = color; x.lineCap = "butt"; x.lineJoin = "round";
      x.beginPath(); x.moveTo(-50, 94); x.lineTo(-58, 30); x.arc(0, 0, 66, Math.PI * 0.85, Math.PI * 0.15); x.lineTo(50, 94); x.stroke();
    };
    arco(62, "#fff"); arco(42, CONTORNO); arco(28, "#c8c8c0");
    x.lineWidth = 6; x.strokeStyle = "rgba(255,255,255,0.6)";
    x.beginPath(); x.arc(0, 0, 74, Math.PI * 1.15, Math.PI * 1.6); x.stroke();
    x.fillStyle = "#4a4e54";
    for (const a of [0.95, 1.2, 1.5, 1.8, 2.05]) { x.beginPath(); x.arc(Math.cos(a * Math.PI) * 66, Math.sin(a * Math.PI) * 66, 5, 0, Math.PI * 2); x.fill(); }
    for (const sx of [-1, 1]) { x.beginPath(); x.arc(sx * 54, 60, 5, 0, Math.PI * 2); x.fill(); }
    x.restore();
  },
  // 13/11: el collar del carnaval de Nueva Orleans (morado, verde y oro).
  collar(x) {
    x.save();
    x.translate(128, 132);
    const cols = ["#7a3aaa", "#2aa85a", "#f0c030"];
    for (let capa = 0; capa < 3; capa++) {
      for (let k = 0; k < 22; k++) {
        const a = (k / 22) * Math.PI * 2;
        x.beginPath(); x.arc(Math.cos(a) * 74, Math.sin(a) * 86, capa === 0 ? 25 : capa === 1 ? 18 : 14, 0, Math.PI * 2);
        x.fillStyle = capa === 0 ? "#fff" : capa === 1 ? CONTORNO : cols[k % 3];
        x.fill();
      }
    }
    x.fillStyle = "rgba(255,255,255,0.7)";
    for (let k = 0; k < 22; k++) {
      const a = (k / 22) * Math.PI * 2;
      x.beginPath(); x.arc(Math.cos(a) * 74 - 4, Math.sin(a) * 86 - 5, 4, 0, Math.PI * 2); x.fill();
    }
    x.restore();
  },
  // 13/11: el rotulador del huracan de Birmingham.
  rotulador(x) {
    x.save();
    x.translate(128, 128); x.rotate(-0.75);
    const cuerpo = () => { x.beginPath(); x.rect(-96, -28, 150, 56); };
    const punta = () => { x.beginPath(); x.moveTo(54, -22); x.lineTo(96, -8); x.lineTo(104, 0); x.lineTo(96, 8); x.lineTo(54, 22); x.closePath(); };
    x.lineJoin = "round";
    x.lineWidth = 30; x.strokeStyle = "#fff"; cuerpo(); x.stroke(); punta(); x.stroke();
    x.lineWidth = 8; x.strokeStyle = CONTORNO; cuerpo(); x.stroke(); punta(); x.stroke();
    cuerpo(); x.fillStyle = "#1b1c20"; x.fill();
    punta(); x.fillStyle = "#6a6e72"; x.fill();
    x.fillStyle = "#f4f0e8"; x.fillRect(-40, -28, 34, 56);
    x.fillStyle = "#1b1c20"; x.beginPath(); x.moveTo(96, -8); x.lineTo(104, 0); x.lineTo(96, 8); x.closePath(); x.fill();
    x.restore();
  },
  pajita(x) {
    x.save();
    x.translate(128, 140); x.rotate(0.2);
    x.lineCap = "round"; x.lineJoin = "round";
    const tubo = () => { x.beginPath(); x.moveTo(-20, 100); x.lineTo(-20, -40); x.quadraticCurveTo(-20, -80, 30, -90); x.lineTo(80, -100); };
    x.lineWidth = 64; x.strokeStyle = "#fff"; tubo(); x.stroke();
    x.lineWidth = 38; x.strokeStyle = CONTORNO; tubo(); x.stroke();
    x.lineWidth = 30; x.strokeStyle = "#f6f2e6"; tubo(); x.stroke();
    x.strokeStyle = "#d8323a"; x.lineWidth = 30; x.setLineDash([16, 16]); tubo(); x.stroke(); x.setLineDash([]);
    x.restore();
  },
  // 12/11: el casco de astronauta de Houston (blanco, con el visor dorado).
  casco(x) {
    x.save();
    x.translate(128, 132);
    x.lineJoin = "round"; x.lineCap = "round";
    const casco = () => { x.beginPath(); x.arc(0, -10, 92, Math.PI * 0.92, Math.PI * 2.08); x.lineTo(80, 70); x.lineTo(-80, 70); x.closePath(); };
    const visor = () => { x.beginPath(); x.ellipse(0, -6, 62, 50, 0, 0, Math.PI * 2); };
    x.lineWidth = 26; x.strokeStyle = "#fff"; casco(); x.stroke();
    casco(); x.fillStyle = "#f2f2ee"; x.fill();
    visor(); x.fillStyle = "#e0b040"; x.fill();
    x.fillStyle = "rgba(255,255,255,0.55)"; x.beginPath(); x.ellipse(-24, -26, 18, 10, -0.5, 0, Math.PI * 2); x.fill();
    x.fillStyle = "#1f4fa8"; x.fillRect(-36, 72, 72, 12);
    x.lineWidth = 7; x.strokeStyle = CONTORNO; casco(); x.stroke(); visor(); x.stroke();
    x.restore();
  },
  // 12/11: la gota de petroleo de Oklahoma (negra y brillante).
  gota(x) {
    x.save();
    x.translate(128, 140);
    x.lineJoin = "round";
    const gota = () => { x.beginPath(); x.moveTo(0, -110); x.bezierCurveTo(40, -50, 82, -10, 82, 30); x.arc(0, 30, 82, 0, Math.PI); x.bezierCurveTo(-82, -10, -40, -50, 0, -110); x.closePath(); };
    x.lineWidth = 26; x.strokeStyle = "#fff"; gota(); x.stroke();
    gota(); x.fillStyle = "#1a1620"; x.fill();
    x.fillStyle = "rgba(255,255,255,0.5)"; x.beginPath(); x.ellipse(-32, 10, 14, 32, -0.3, 0, Math.PI * 2); x.fill();
    x.lineWidth = 7; x.strokeStyle = CONTORNO; gota(); x.stroke();
    x.restore();
  },
  // 12/11: el cincel del escultor del monte Rushmore (mango de madera y punta de acero).
  cincel(x) {
    x.save();
    x.translate(128, 128); x.rotate(-0.75);
    x.lineJoin = "round"; x.lineCap = "round";
    const mango = () => { x.beginPath(); x.roundRect(-30, -100, 60, 110, 18); };
    const hoja = () => { x.beginPath(); x.moveTo(-22, 10); x.lineTo(22, 10); x.lineTo(16, 92); x.lineTo(-16, 92); x.closePath(); };
    x.lineWidth = 26; x.strokeStyle = "#fff"; mango(); x.stroke(); hoja(); x.stroke();
    hoja(); x.fillStyle = "#b8c0c8"; x.fill();
    x.fillStyle = "#e6ecf0"; x.fillRect(-10, 16, 8, 70);
    mango(); x.fillStyle = "#b8743a"; x.fill();
    x.fillStyle = "#8a5226"; for (let k = 0; k < 3; k++) x.fillRect(-30, -80 + k * 28, 60, 6);
    x.fillStyle = "#7a7268"; x.fillRect(-26, 0, 52, 14);
    x.lineWidth = 7; x.strokeStyle = CONTORNO; mango(); x.stroke(); hoja(); x.stroke();
    x.restore();
  },
  // 12/11: el gorro de orejeras de Fargo (el de la pelicula), rojo y con borrego.
  orejeras(x) {
    x.save();
    x.translate(128, 140);
    x.lineJoin = "round"; x.lineCap = "round";
    const copa = () => { x.beginPath(); x.moveTo(-80, 0); x.quadraticCurveTo(-82, -96, 0, -100); x.quadraticCurveTo(82, -96, 80, 0); x.closePath(); };
    const oreja = (s) => { x.beginPath(); x.moveTo(s * 50, -6); x.quadraticCurveTo(s * 98, 0, s * 86, 70); x.quadraticCurveTo(s * 62, 82, s * 50, 40); x.closePath(); };
    x.lineWidth = 26; x.strokeStyle = "#fff"; copa(); x.stroke(); oreja(-1); x.stroke(); oreja(1); x.stroke();
    for (const s of [-1, 1]) { oreja(s); x.fillStyle = "#f2e8d4"; x.fill(); }
    copa(); x.fillStyle = "#c8282c"; x.fill();
    x.fillStyle = "#a81e22"; for (let k = 0; k < 4; k++) x.fillRect(-70 + k * 40, -80, 10, 80);
    x.fillStyle = "#f2e8d4"; x.beginPath(); x.roundRect(-86, -14, 172, 28, 14); x.fill();
    x.lineWidth = 7; x.strokeStyle = CONTORNO; copa(); x.stroke(); oreja(-1); x.stroke(); oreja(1); x.stroke();
    x.beginPath(); x.roundRect(-86, -14, 172, 28, 14); x.stroke();
    x.restore();
  },
  // 09/11: el patin de hielo de Minneapolis (lagos helados y hockey).
  patin(x) {
    x.save();
    x.translate(128, 132); x.rotate(-0.12);
    x.lineJoin = "round"; x.lineCap = "round";
    const bota = () => {
      x.beginPath();
      x.moveTo(-60, -80); x.lineTo(10, -80); x.lineTo(14, -10);
      x.quadraticCurveTo(80, 0, 92, 30); x.lineTo(92, 46); x.lineTo(-64, 46); x.closePath();
    };
    const cuchilla = () => { x.beginPath(); x.moveTo(-74, 66); x.lineTo(96, 66); x.quadraticCurveTo(116, 66, 108, 50); };
    x.lineWidth = 26; x.strokeStyle = "#fff"; bota(); x.stroke(); cuchilla(); x.stroke();
    x.lineWidth = 9; x.strokeStyle = "#c8ced6"; cuchilla(); x.stroke();
    x.fillStyle = "#9aa2aa";
    for (const px of [-46, 70]) x.fillRect(px - 5, 46, 10, 20);
    bota(); x.fillStyle = "#f4f4f2"; x.fill();
    x.fillStyle = "#d52b1e"; x.fillRect(-60, -80, 70, 16);
    x.strokeStyle = "#3a3a40"; x.lineWidth = 4;
    for (let k = 0; k < 4; k++) { x.beginPath(); x.moveTo(-6, -54 + k * 14); x.lineTo(18, -48 + k * 14); x.stroke(); }
    x.lineWidth = 7; x.strokeStyle = CONTORNO; bota(); x.stroke();
    x.restore();
  },

  // 08/11: la botella de sirope de arce de Detroit (los canadienses del puente).
  sirope(x) {
    x.save();
    x.translate(128, 132); x.rotate(0.15);
    x.lineJoin = "round";
    const botella = () => {
      x.beginPath();
      x.moveTo(-22, -100); x.lineTo(22, -100); x.lineTo(22, -62);
      x.quadraticCurveTo(70, -40, 70, 10); x.lineTo(70, 80);
      x.quadraticCurveTo(70, 100, 50, 100); x.lineTo(-50, 100);
      x.quadraticCurveTo(-70, 100, -70, 80); x.lineTo(-70, 10);
      x.quadraticCurveTo(-70, -40, -22, -62); x.closePath();
    };
    x.lineWidth = 24; x.strokeStyle = "#fff"; botella(); x.stroke();
    botella(); x.fillStyle = "#c8781e"; x.fill();
    x.fillStyle = "#e8a040"; x.beginPath(); x.ellipse(-30, 20, 14, 40, 0, 0, Math.PI * 2); x.fill();
    x.fillStyle = "#d8202a"; x.fillRect(-22, -112, 44, 22);
    x.fillStyle = "#fbf8f2"; x.fillRect(-52, 18, 104, 56);
    // La hoja de arce, sencilla: un rombo con dos puntas a los lados.
    x.fillStyle = "#d8202a";
    x.beginPath();
    x.moveTo(0, 24); x.lineTo(12, 40); x.lineTo(28, 36); x.lineTo(16, 52); x.lineTo(6, 52); x.lineTo(4, 68);
    x.lineTo(-4, 68); x.lineTo(-6, 52); x.lineTo(-16, 52); x.lineTo(-28, 36); x.lineTo(-12, 40); x.closePath(); x.fill();
    x.lineWidth = 7; x.strokeStyle = CONTORNO; botella(); x.stroke();
    x.strokeRect(-22, -112, 44, 22);
    x.restore();
  },

  // 08/11: la bandera de cuadros de Indianápolis (la meta de las 500 millas).
  cuadros(x) {
    x.save();
    x.translate(128, 128); x.rotate(-0.18);
    x.lineCap = "round"; x.lineJoin = "round";
    const mastil = () => { x.beginPath(); x.moveTo(-82, -92); x.lineTo(-82, 104); };
    x.lineWidth = 30; x.strokeStyle = "#fff"; mastil(); x.stroke();
    x.lineWidth = 15; x.strokeStyle = CONTORNO; mastil(); x.stroke();
    x.lineWidth = 7; x.strokeStyle = "#d9d2c4"; mastil(); x.stroke();
    const tela = () => {
      x.beginPath();
      x.moveTo(-82, -92);
      x.bezierCurveTo(-25, -122, 30, -58, 98, -86);
      x.lineTo(98, 14);
      x.bezierCurveTo(30, 42, -25, -22, -82, 8);
      x.closePath();
    };
    x.lineWidth = 24; x.strokeStyle = "#fff"; tela(); x.stroke();
    tela(); x.fillStyle = "#fbf8f2"; x.fill();
    x.save(); tela(); x.clip();
    x.fillStyle = "#1d1f25";
    for (let i = 0; i < 6; i++) {
      const off = -14 * Math.sin(((i + 0.5) / 6) * Math.PI * 1.7);
      for (let j = 0; j < 7; j++) if ((i + j) % 2 === 0) x.fillRect(-82 + i * 30, -118 + off + j * 22, 30.5, 22.5);
    }
    x.restore();
    x.lineWidth = 7; x.strokeStyle = CONTORNO; tela(); x.stroke();
    x.restore();
  },

  // 08/11: la etiqueta de precio de San Luis (los aranceles: «$$$»).
  etiqueta(x) {
    x.save();
    x.translate(128, 128); x.rotate(-0.35);
    const forma = () => {
      x.beginPath();
      x.moveTo(-60, -70); x.lineTo(70, -70); x.lineTo(70, 70); x.lineTo(-60, 70); x.lineTo(-100, 0); x.closePath();
    };
    x.lineWidth = 24; x.strokeStyle = "#fff"; forma(); x.stroke();
    forma(); x.fillStyle = "#fff6d8"; x.fill();
    x.lineWidth = 7; x.strokeStyle = CONTORNO; forma(); x.stroke();
    x.beginPath(); x.arc(-66, 0, 11, 0, Math.PI * 2); x.fillStyle = "#fff"; x.fill(); x.stroke();
    x.fillStyle = "#d8202a"; x.font = "900 70px sans-serif"; x.textAlign = "center"; x.textBaseline = "middle";
    x.fillText("$$", 14, 4);
    x.restore();
  },

  // 08/11: los zapatos de rubi de Dorothy (Wichita, El Mago de Oz).
  zapato(x) {
    const zapato = (cx, cy, giro) => {
      x.save(); x.translate(cx, cy); x.rotate(giro);
      const forma = () => {
        x.beginPath();
        x.moveTo(-70, 10); x.quadraticCurveTo(-72, -30, -40, -34); x.lineTo(10, -20);
        x.quadraticCurveTo(60, -16, 70, 12); x.quadraticCurveTo(66, 30, 30, 30); x.lineTo(-50, 30);
        x.quadraticCurveTo(-70, 30, -70, 10); x.closePath();
      };
      x.lineWidth = 22; x.strokeStyle = "#fff"; forma(); x.stroke();
      const g = x.createLinearGradient(0, -34, 0, 30);
      g.addColorStop(0, "#ff4a5a"); g.addColorStop(1, "#a8101e");
      forma(); x.fillStyle = g; x.fill();
      x.fillStyle = "rgba(255,255,255,0.75)";
      for (let k = 0; k < 14; k++) { x.beginPath(); x.arc(-55 + (k * 37) % 115, -18 + (k * 23) % 40, 3, 0, Math.PI * 2); x.fill(); }
      x.fillStyle = "#7a0a14"; x.fillRect(-62, 22, 14, 26);           // el tacon
      x.beginPath(); x.ellipse(18, -18, 16, 10, 0, 0, Math.PI * 2); x.fillStyle = "#ff8a9a"; x.fill();   // el lazo
      x.lineWidth = 6; x.strokeStyle = CONTORNO; forma(); x.stroke();
      x.restore();
    };
    zapato(118, 104, -0.15);
    zapato(138, 168, 0.1);
  },

  // 08/11: el filete de Omaha (un chuleton con su hueso en T).
  filete(x) {
    x.save();
    x.translate(128, 132); x.rotate(-0.25);
    const carne = () => { x.beginPath(); x.ellipse(0, 0, 100, 74, 0, 0, Math.PI * 2); };
    x.lineWidth = 26; x.strokeStyle = "#fff"; carne(); x.stroke();
    carne(); x.fillStyle = "#f4e6c8"; x.fill();                      // la grasa del borde
    x.beginPath(); x.ellipse(0, 0, 86, 60, 0, 0, Math.PI * 2);
    const g = x.createRadialGradient(-20, -20, 10, 0, 0, 90);
    g.addColorStop(0, "#c8503c"); g.addColorStop(1, "#8a2a22");
    x.fillStyle = g; x.fill();
    x.strokeStyle = "rgba(60,20,10,0.55)"; x.lineWidth = 7;            // las marcas de la parrilla
    for (let k = -2; k <= 2; k++) { x.beginPath(); x.moveTo(-60 + k * 22, -44); x.lineTo(-20 + k * 22, 44); x.stroke(); }
    x.fillStyle = "#fbf6ea"; x.strokeStyle = CONTORNO; x.lineWidth = 6;   // el hueso en T
    x.beginPath(); x.rect(-8, -50, 16, 100); x.fill(); x.stroke();
    x.beginPath(); x.rect(-36, -10, 72, 16); x.fill(); x.stroke();
    x.lineWidth = 7; x.strokeStyle = CONTORNO; carne(); x.stroke();
    x.restore();
  },

  // La ficha de casino (Las Vegas).
  ficha(x) {
    const cx = 128, cy = 128;
    x.beginPath(); x.arc(cx, cy, 112, 0, Math.PI * 2); x.fillStyle = "#ffffff"; x.fill();
    x.beginPath(); x.arc(cx, cy, 100, 0, Math.PI * 2);
    x.fillStyle = "#d8232a"; x.fill(); x.lineWidth = 8; x.strokeStyle = CONTORNO; x.stroke();
    x.fillStyle = "#ffffff";                                          // las marcas del canto
    for (let i = 0; i < 8; i++) {
      x.save(); x.translate(cx, cy); x.rotate((i * Math.PI) / 4);
      x.beginPath(); x.roundRect(-12, -98, 24, 30, 5); x.fill();
      x.restore();
    }
    x.beginPath(); x.arc(cx, cy, 62, 0, Math.PI * 2); x.fillStyle = "#ffffff"; x.fill();
    x.lineWidth = 5; x.strokeStyle = "#d8232a"; x.stroke();
    x.setLineDash([10, 9]); x.beginPath(); x.arc(cx, cy, 54, 0, Math.PI * 2); x.stroke(); x.setLineDash([]);
    estrella(x, cx, cy + 3, 36, 15); x.fillStyle = "#ffd23f"; x.fill();
    x.lineWidth = 5; x.strokeStyle = "#b07a00"; x.stroke();
  },

  // Mazorca de maíz (el ingrediente de Ohio).
  maiz(x) {
    x.save();
    x.translate(128, 132); x.rotate(-0.5);
    const mazorca = () => { x.beginPath(); x.ellipse(0, -18, 46, 92, 0, 0, Math.PI * 2); };
    x.lineWidth = 26; x.strokeStyle = "#fff"; mazorca(); x.stroke();
    mazorca();
    const g = x.createLinearGradient(-46, 0, 46, 0);
    g.addColorStop(0, "#ffcf33"); g.addColorStop(1, "#f2a516");
    x.fillStyle = g; x.fill();
    x.save(); mazorca(); x.clip();
    for (let fila = -6; fila <= 6; fila++) {                           // los granos
      for (let col = -3; col <= 3; col++) {
        const gx = col * 14 + (fila % 2 ? 7 : 0), gy = -18 + fila * 15;
        x.beginPath(); x.ellipse(gx, gy, 6, 6.5, 0, 0, Math.PI * 2);
        x.fillStyle = "#ffe066"; x.fill();
        x.fillStyle = "rgba(255,255,255,0.6)";
        x.beginPath(); x.arc(gx - 2, gy - 2, 2, 0, Math.PI * 2); x.fill();
      }
    }
    x.restore();
    x.lineWidth = 7; x.strokeStyle = CONTORNO; mazorca(); x.stroke();
    for (const s of [-1, 1]) {                                         // las hojas
      x.beginPath();
      x.moveTo(0, 96);
      x.quadraticCurveTo(s * 70, 70, s * 52, -40);
      x.quadraticCurveTo(s * 30, 30, 0, 96);
      x.fillStyle = s < 0 ? "#4fbf3a" : "#3fa82e"; x.fill();
      x.lineWidth = 6; x.strokeStyle = CONTORNO; x.stroke();
    }
    x.restore();
  },

  // La tortilla (el ingrediente de Nueva York).
  tortilla(x) {
    const cx = 128, cy = 132;
    x.beginPath(); x.ellipse(cx, cy, 108, 90, 0, 0, Math.PI * 2);
    x.lineWidth = 24; x.strokeStyle = "#fff"; x.stroke();
    const g = x.createRadialGradient(cx - 20, cy - 20, 10, cx, cy, 110);
    g.addColorStop(0, "#fbe7b0"); g.addColorStop(1, "#e9c278");
    x.fillStyle = g; x.fill();
    x.fillStyle = "rgba(176,108,40,0.5)";
    for (const [px, py, r] of [[-50, -30, 9], [30, -44, 7], [60, 10, 10], [-20, 30, 8], [10, 56, 6], [-66, 24, 6], [44, 46, 7], [-4, -6, 5]]) {
      x.beginPath(); x.ellipse(cx + px, cy + py, r, r * 0.7, 0.4, 0, Math.PI * 2); x.fill();
    }
    x.strokeStyle = "rgba(255,255,255,0.6)"; x.lineWidth = 9;
    x.beginPath(); x.ellipse(cx, cy, 86, 70, 0, Math.PI * 1.1, Math.PI * 1.45); x.stroke();
    x.lineWidth = 8; x.strokeStyle = CONTORNO;
    x.beginPath(); x.ellipse(cx, cy, 108, 90, 0, 0, Math.PI * 2); x.stroke();
  },

  // El chile (el ingrediente de Arizona).
  chile(x) {
    x.save();
    x.translate(128, 128); x.rotate(0.6);
    const cuerpo = () => {
      x.beginPath();
      x.moveTo(-20, -70);
      x.bezierCurveTo(40, -80, 52, -10, 30, 40);
      x.bezierCurveTo(14, 78, -18, 96, -34, 100);
      x.bezierCurveTo(-20, 70, -36, 10, -40, -30);
      x.bezierCurveTo(-42, -56, -34, -66, -20, -70);
      x.closePath();
    };
    x.lineWidth = 26; x.strokeStyle = "#fff"; cuerpo(); x.stroke();
    cuerpo();
    const g = x.createLinearGradient(-40, 0, 50, 0);
    g.addColorStop(0, "#ff4a3a"); g.addColorStop(1, "#c81e1e");
    x.fillStyle = g; x.fill();
    x.lineWidth = 7; x.strokeStyle = CONTORNO; x.stroke();
    x.strokeStyle = "rgba(255,255,255,0.6)"; x.lineWidth = 9;
    x.beginPath(); x.moveTo(-26, -48); x.quadraticCurveTo(-30, 0, -22, 40); x.stroke();
    x.fillStyle = "#3fae3a";                                         // el rabito
    x.beginPath(); x.ellipse(-4, -74, 30, 14, 0.1, 0, Math.PI * 2); x.fill();
    x.lineWidth = 6; x.strokeStyle = CONTORNO; x.stroke();
    x.lineWidth = 10; x.strokeStyle = "#3fae3a";
    x.beginPath(); x.moveTo(-4, -82); x.quadraticCurveTo(4, -104, 26, -108); x.stroke();
    x.restore();
  },

  // La lata de salsa (el ingrediente de Las Vegas).
  salsa(x) {
    const lata = () => { x.beginPath(); x.roundRect(64, 52, 128, 160, 18); };
    x.lineWidth = 26; x.strokeStyle = "#fff"; lata(); x.stroke();
    lata();
    const g = x.createLinearGradient(64, 0, 192, 0);
    g.addColorStop(0, "#d63a2e"); g.addColorStop(0.5, "#f05a40"); g.addColorStop(1, "#b52a22");
    x.fillStyle = g; x.fill();
    x.fillStyle = "#ffe066"; x.fillRect(64, 104, 128, 58);           // la etiqueta
    x.fillStyle = "#c81e1e";
    x.font = '700 34px Fredoka, "Arial Rounded MT Bold", Arial, sans-serif';
    x.textAlign = "center"; x.textBaseline = "middle";
    x.fillText("SALSA", 128, 134);
    x.fillStyle = "#cfd5dc"; x.fillRect(64, 52, 128, 14); x.fillRect(64, 198, 128, 14);   // tapa y culo
    x.strokeStyle = "rgba(255,255,255,0.55)"; x.lineWidth = 9;
    x.beginPath(); x.moveTo(84, 74); x.lineTo(84, 96); x.moveTo(84, 172); x.lineTo(84, 190); x.stroke();
    x.lineWidth = 7; x.strokeStyle = CONTORNO; lata(); x.stroke();
  },

  // El taco perfecto de la Casa Blanca: el taco con estrellas doradas.
  taco_perfecto(x) {
    x.drawImage(lienzo("taco"), 0, 18);
    for (const [px, py, r] of [[34, 40, 18], [222, 52, 14], [200, 222, 12], [48, 210, 10]]) {
      estrella(x, px, py, r, r * 0.42);
      x.fillStyle = "#ffd23f"; x.fill();
      x.lineWidth = 3; x.strokeStyle = "#b07a00"; x.stroke();
    }
  },
};
