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
