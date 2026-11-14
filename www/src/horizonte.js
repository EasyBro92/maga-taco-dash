import * as THREE from "../vendor/three.module.min.js";

// Horizontes pintados (27/10/2026).
//
// En la revisión: detrás de Nueva York, de Ohio y de Washington salían unas
// montañas grises de conos (parecían nevadas) y unos bloques sueltos que no se
// movían. Ahora cada sitio tiene su horizonte pintado en un lienzo, como los
// fondos de las películas de animación, en dos capas (la de atrás más lavada,
// con el aire): el perfil de Manhattan, los campos y silos de Ohio, Washington
// con el obelisco, las mesetas del desierto y las colinas del pueblo. Va en una
// banda curva muy lejos y quieta (como el horizonte de verdad), sin niebla.
// Arriba, nubes blancas y altas (antes, bolas grises a la altura de los edificios).

const ANCHO = 4096, ALTO = 512;
const R = 292, ALTO_BANDA = 120, ARCO = Math.PI * 0.95, BAJO = -12;
// La linea del suelo en el lienzo (y = 0 del mundo).
const SUELO = ALTO * (1 - (0 - BAJO) / ALTO_BANDA);
const px = (alto) => (alto / ALTO_BANDA) * ALTO;   // unidades del mundo -> pixeles

function azar(semilla) {
  let a = semilla >>> 0;
  return () => {
    a = (a + 0x6d2b79f5) >>> 0;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
const mezcla = (a, b, k) => new THREE.Color(a).lerp(new THREE.Color(b), k).getStyle();

// ---- Cada sitio ----
// c: { cielo, suelo, cerca, lejos } colores; cada funcion pinta sobre el lienzo.
function torre(x, base, w, h, color, r, remate) {
  x.fillStyle = color;
  x.fillRect(base[0], SUELO - h, w, h + 2);
  if (remate === "escalones") {
    x.fillRect(base[0] + w * 0.15, SUELO - h - h * 0.12, w * 0.7, h * 0.12 + 2);
    x.fillRect(base[0] + w * 0.32, SUELO - h - h * 0.22, w * 0.36, h * 0.12 + 2);
    x.fillRect(base[0] + w * 0.47, SUELO - h - h * 0.42, w * 0.06, h * 0.22);
  } else if (remate === "antena") {
    x.fillRect(base[0] + w * 0.46, SUELO - h - h * 0.18, Math.max(2, w * 0.08), h * 0.18);
  } else if (remate === "pico") {
    x.beginPath(); x.moveTo(base[0], SUELO - h); x.lineTo(base[0] + w / 2, SUELO - h - w * 0.9); x.lineTo(base[0] + w, SUELO - h); x.fill();
  }
  // Filas de ventanas, muy suaves (de dia casi no se ven).
  x.fillStyle = "rgba(255,255,255,0.07)";
  for (let yy = SUELO - h + 6; yy < SUELO - 4; yy += 7) x.fillRect(base[0] + 3, yy, w - 6, 2);
}
const SITIOS = {
  manhattan(x, c, r) {
    for (const [capa, color, hMin, hMax] of [[0, c.lejos, 40, 150], [1, c.cerca, 25, 110]]) {
      let cx = -20;
      while (cx < ANCHO + 20) {
        const w = 22 + r() * 60;
        const h = hMin + r() * (hMax - hMin) * (r() < 0.15 ? 1.6 : 1);
        torre(x, [cx, 0], w, h, color, r, r() < 0.18 ? "antena" : r() < 0.1 ? "pico" : null);
        cx += w * (capa ? 0.95 : 0.8);
      }
      if (capa === 0) {
        // Los famosos, en la capa de atras: el Empire, el Chrysler y la torre nueva.
        torre(x, [1180, 0], 70, 250, color, r, "escalones");
        x.fillStyle = color;
        x.beginPath(); x.moveTo(2600, SUELO); x.lineTo(2604, SUELO - 210); x.quadraticCurveTo(2632, SUELO - 270, 2660, SUELO - 210); x.lineTo(2664, SUELO); x.fill();
        x.fillRect(2630, SUELO - 300, 4, 40);
        x.beginPath(); x.moveTo(3300, SUELO); x.lineTo(3312, SUELO - 300); x.lineTo(3352, SUELO - 300); x.lineTo(3364, SUELO); x.fill();
        x.fillRect(3330, SUELO - 350, 3, 50);
        torre(x, [470, 0], 28, 290, color, r, "antena");
      }
    }
  },
  ohio(x, c, r) {
    // Colinas suaves, campos y arboledas; granjas con silos y un deposito de agua.
    x.fillStyle = c.lejos;
    x.beginPath(); x.moveTo(0, SUELO);
    for (let i = 0; i <= 40; i++) x.lineTo((i / 40) * ANCHO, SUELO - 18 - Math.sin(i * 0.7) * 10 - r() * 8);
    x.lineTo(ANCHO, SUELO); x.fill();
    for (let i = 0; i < 70; i++) {                                   // arboledas
      const cx = r() * ANCHO, rr = 10 + r() * 14;
      x.fillStyle = r() < 0.5 ? c.lejos : c.cerca;
      x.beginPath(); x.arc(cx, SUELO - rr * 0.6, rr, 0, Math.PI * 2); x.arc(cx + rr * 0.9, SUELO - rr * 0.4, rr * 0.8, 0, Math.PI * 2); x.fill();
    }
    for (let k = 0; k < 9; k++) {                                     // granjas
      const cx = 200 + k * 440 + r() * 120;
      x.fillStyle = c.granero;
      x.fillRect(cx, SUELO - 34, 46, 34);
      x.beginPath(); x.moveTo(cx - 4, SUELO - 34); x.lineTo(cx + 23, SUELO - 52); x.lineTo(cx + 50, SUELO - 34); x.fill();
      x.fillStyle = c.silo;
      for (let s = 0; s < 1 + Math.floor(r() * 2); s++) {
        const sx = cx + 54 + s * 20;
        x.fillRect(sx, SUELO - 70, 16, 70);
        x.beginPath(); x.arc(sx + 8, SUELO - 70, 8, Math.PI, 0); x.fill();
      }
    }
    x.fillStyle = c.cerca;                                            // deposito de agua
    for (const cx of [900, 2900]) {
      x.fillRect(cx - 2, SUELO - 80, 4, 80); x.fillRect(cx + 26, SUELO - 80, 4, 80);
      x.beginPath(); x.ellipse(cx + 14, SUELO - 92, 28, 16, 0, 0, Math.PI * 2); x.fill();
    }
    x.fillRect(1850, SUELO - 120, 34, 120);                           // elevador de grano
    x.fillRect(1884, SUELO - 90, 26, 90);
  },
  dc(x, c, r) {
    // Ciudad baja (en Washington no se puede subir mas que el Capitolio), arboles y el obelisco.
    x.fillStyle = c.lejos;
    x.beginPath(); x.moveTo(0, SUELO);
    for (let i = 0; i <= 30; i++) x.lineTo((i / 30) * ANCHO, SUELO - 30 - Math.sin(i * 0.5 + 1) * 14);
    x.lineTo(ANCHO, SUELO); x.fill();
    let cx = 0;
    while (cx < ANCHO) { const w = 40 + r() * 90, h = 30 + r() * 40; x.fillStyle = r() < 0.5 ? c.lejos : c.cerca; x.fillRect(cx, SUELO - h, w, h + 2); cx += w; }
    for (let i = 0; i < 60; i++) { const tx = r() * ANCHO, rr = 9 + r() * 10; x.fillStyle = c.arbol; x.beginPath(); x.arc(tx, SUELO - rr * 0.5, rr, 0, Math.PI * 2); x.fill(); }
    // El monumento a Washington, delante a la izquierda (corriendo hacia el oeste).
    x.fillStyle = c.monumento;
    x.beginPath(); x.moveTo(1540, SUELO); x.lineTo(1548, SUELO - 300); x.lineTo(1560, SUELO - 318); x.lineTo(1572, SUELO - 300); x.lineTo(1580, SUELO); x.fill();
    x.fillStyle = "rgba(0,0,0,0.08)"; x.fillRect(1560, SUELO - 300, 20, 300);
    // Una cupula al fondo a la derecha y las colinas de Virginia.
    x.fillStyle = c.lejos;
    x.beginPath(); x.arc(2700, SUELO - 70, 34, Math.PI, 0); x.fill(); x.fillRect(2660, SUELO - 70, 80, 70);
  },
  phoenix(x, c, r) {
    // Las montanas que rodean Phoenix: South Mountain, larga y con antenas, a
    // la izquierda; Camelback (la joroba y la cabeza del camello) a la derecha.
    x.fillStyle = c.lejos;
    x.beginPath(); x.moveTo(0, SUELO);
    for (let i = 0; i <= 60; i++) {
      const u = i / 60;
      const h = 70 + Math.sin(u * 9) * 14 + Math.sin(u * 23) * 6 + (u < 0.4 ? 30 * Math.sin((u / 0.4) * Math.PI) : 0);
      x.lineTo(u * ANCHO, SUELO - h - r() * 5);
    }
    x.lineTo(ANCHO, SUELO); x.fill();
    for (const ax of [520, 610, 700]) { x.fillRect(ax, SUELO - 170, 3, 50); x.fillRect(ax - 6, SUELO - 160, 15, 2); }
    x.fillStyle = c.cerca;
    x.beginPath(); x.moveTo(2500, SUELO);                              // Camelback
    x.bezierCurveTo(2650, SUELO - 40, 2700, SUELO - 175, 2880, SUELO - 170);
    x.bezierCurveTo(3000, SUELO - 165, 3020, SUELO - 95, 3080, SUELO - 100);
    x.bezierCurveTo(3150, SUELO - 120, 3190, SUELO - 125, 3230, SUELO - 95);
    x.bezierCurveTo(3300, SUELO - 50, 3400, SUELO - 20, 3500, SUELO);
    x.fill();
    // Ciudad baja, palmeras y saguaros por delante.
    let cx = 0;
    while (cx < ANCHO) { const w = 40 + r() * 80, h = 14 + r() * 26; x.fillStyle = c.lejos; x.fillRect(cx, SUELO - h, w, h + 2); cx += w + r() * 40; }
    x.fillStyle = c.arbol;
    for (let i = 0; i < 40; i++) {
      const px = r() * ANCHO, h = 40 + r() * 40;
      x.fillRect(px, SUELO - h, 3, h);
      for (let k = 0; k < 6; k++) { const a = (k / 6) * Math.PI * 2; x.beginPath(); x.ellipse(px + 1.5 + Math.cos(a) * 9, SUELO - h + Math.sin(a) * 3, 10, 2.5, a, 0, Math.PI * 2); x.fill(); }
    }
    for (let i = 0; i < 30; i++) {
      const px = r() * ANCHO, h = 22 + r() * 22;
      x.fillRect(px, SUELO - h, 6, h);
      x.fillRect(px - 8, SUELO - h * 0.7, 4, h * 0.35); x.fillRect(px - 8, SUELO - h * 0.45, 10, 3);
      x.fillRect(px + 10, SUELO - h * 0.8, 4, h * 0.4); x.fillRect(px + 4, SUELO - h * 0.5, 10, 3);
    }
  },
  vegas(x, c, r) {
    // Las Vegas al anochecer (29/10): las montañas moradas de alrededor, la
    // ciudad con las ventanitas encendidas y la torre STRAT al norte. Las
    // luces son fijas (nada parpadea).
    x.fillStyle = c.lejos;
    x.beginPath(); x.moveTo(0, SUELO);
    for (let i = 0; i <= 80; i++) {
      const u = i / 80;
      const h = 85 + Math.sin(u * 7) * 22 + Math.sin(u * 19 + 1) * 9 + (u > 0.6 && u < 0.85 ? 45 * Math.sin(((u - 0.6) / 0.25) * Math.PI) : 0);
      x.lineTo(u * ANCHO, SUELO - h - r() * 6);
    }
    x.lineTo(ANCHO, SUELO); x.fill();
    let cx = 0;
    while (cx < ANCHO) {
      const w = 30 + r() * 70, h = 18 + r() * 75;
      x.fillStyle = c.cerca; x.fillRect(cx, SUELO - h, w, h + 2);
      x.fillStyle = r() < 0.5 ? "rgba(255,214,120,0.85)" : "rgba(255,240,205,0.7)";
      for (let wy = SUELO - h + 5; wy < SUELO - 4; wy += 7) for (let wx = cx + 4; wx < cx + w - 4; wx += 7) if (r() < 0.5) x.fillRect(wx, wy, 3, 3);
      cx += w + r() * 30;
    }
    const tx = 2050, th = 290;
    x.fillStyle = c.cerca;
    x.beginPath(); x.moveTo(tx - 16, SUELO); x.lineTo(tx - 8, SUELO - th); x.lineTo(tx + 8, SUELO - th); x.lineTo(tx + 16, SUELO); x.fill();
    x.beginPath(); x.ellipse(tx, SUELO - th - 12, 40, 22, 0, 0, Math.PI * 2); x.fill();
    x.fillRect(tx - 3, SUELO - th - 100, 6, 80);
    x.fillStyle = "rgba(255,90,210,0.95)"; x.fillRect(tx - 38, SUELO - th - 14, 76, 4);
    x.fillStyle = "rgba(255,230,140,0.95)"; x.fillRect(tx - 30, SUELO - th - 4, 60, 3);
    x.fillStyle = "rgba(255,60,60,1)"; x.beginPath(); x.arc(tx, SUELO - th - 102, 4, 0, Math.PI * 2); x.fill();
  },
  // 08/11: Chicago: a la izquierda (el este) el lago Michigan, liso hasta el
  // horizonte, con veleros; delante y a la derecha, el Loop: la Willis Tower
  // (negra, en escalones, con sus dos antenas), el Aon (la losa blanca) y el
  // Two Prudential (con la aguja).
  chicago(x, c, r) {
    x.fillStyle = c.lago;
    x.fillRect(0, SUELO - 5, 1500, 7);
    for (let i = 0; i < 9; i++) {
      const bx = 120 + i * 150 + r() * 60;
      x.fillStyle = c.vela;
      x.beginPath(); x.moveTo(bx, SUELO - 5); x.lineTo(bx, SUELO - 22); x.lineTo(bx + 10, SUELO - 5); x.fill();
    }
    for (const [capa, color, hMin, hMax] of [[0, c.lejos, 50, 170], [1, c.cerca, 30, 120]]) {
      let cx = 1380 + capa * 90;
      while (cx < ANCHO + 20) {
        const w = 24 + r() * 55;
        const h = hMin + r() * (hMax - hMin) * (r() < 0.15 ? 1.4 : 1);
        torre(x, [cx, 0], w, h, color, r, r() < 0.2 ? "antena" : r() < 0.1 ? "escalones" : null);
        cx += w * (capa ? 0.95 : 0.8);
      }
      if (capa === 0) {
        torre(x, [1880, 0], 52, 270, color, r, null);                         // el Aon
        x.fillStyle = color;
        x.fillRect(1780, SUELO - 230, 40, 232);                                // el Two Prudential
        x.beginPath(); x.moveTo(1780, SUELO - 230); x.lineTo(1800, SUELO - 300); x.lineTo(1820, SUELO - 230); x.fill();
      }
    }
    // La Willis Tower, delante de todo.
    const wx = 2520;
    x.fillStyle = c.willis;
    x.fillRect(wx, SUELO - 250, 72, 252);
    x.fillRect(wx + 24, SUELO - 310, 48, 62);
    x.fillRect(wx + 24, SUELO - 345, 24, 40);
    x.fillRect(wx + 30, SUELO - 400, 4, 58); x.fillRect(wx + 40, SUELO - 390, 4, 48);
  },
  // 09/11: Milwaukee: al fondo de Wisconsin Avenue, el lago Michigan (liso
  // hasta el horizonte, con veleros); a la derecha el puente Hoan (el arco
  // sobre la bocana del puerto) y, a la izquierda, el faro de North Point.
  milwaukee(x, c, r) {
    x.fillStyle = c.lago;
    x.fillRect(0, SUELO - 5, ANCHO, 7);
    for (let i = 0; i < 14; i++) {
      const bx = 60 + i * 290 + r() * 120;
      x.fillStyle = c.vela;
      x.beginPath(); x.moveTo(bx, SUELO - 5); x.lineTo(bx, SUELO - 20); x.lineTo(bx + 9, SUELO - 5); x.fill();
    }
    // El puente Hoan: el tablero largo y el arco atirantado de en medio.
    x.fillStyle = c.puente;
    x.fillRect(2200, SUELO - 40, 520, 5);
    for (let k = 0; k <= 10; k++) x.fillRect(2200 + k * 52, SUELO - 40, 4, 40);
    x.lineWidth = 5; x.strokeStyle = c.puente;
    x.beginPath(); x.moveTo(2380, SUELO - 38); x.quadraticCurveTo(2460, SUELO - 120, 2540, SUELO - 38); x.stroke();
    x.lineWidth = 1.5;
    for (let k = 1; k < 8; k++) { const px = 2380 + k * 20; x.beginPath(); x.moveTo(px, SUELO - 40); x.lineTo(px, SUELO - 38 - 82 * Math.sin(Math.PI * k / 8)); x.stroke(); }
    // El faro de North Point, blanco con la linterna.
    x.fillStyle = c.vela;
    x.fillRect(1500, SUELO - 70, 10, 66);
    x.fillStyle = c.puente;
    x.fillRect(1497, SUELO - 80, 16, 10);
    // Algunas torres de la ciudad, a los lados.
    for (const [x0, x1] of [[3000, 3500], [600, 900]]) {
      let cx = x0;
      while (cx < x1) {
        const w = 22 + r() * 40, h = 30 + r() * 90;
        torre(x, [cx, 0], w, h, c.lejos, r, r() < 0.2 ? "antena" : null);
        cx += w * 0.9;
      }
    }
  },
  // 09/11: Minneapolis en invierno: el suelo nevado hasta lejos, abetos, el
  // puente de piedra de los arcos sobre el Misisipi (Stone Arch) y el silo
  // con el letrero de la harina (Gold Medal Flour), y torres a los lados.
  minneapolis(x, c, r) {
    x.fillStyle = c.nieve;
    x.fillRect(0, SUELO - 6, ANCHO, 8);
    // El puente de los arcos.
    x.fillStyle = c.puente;
    x.fillRect(2250, SUELO - 34, 560, 8);
    for (let k = 0; k < 10; k++) {
      const ax = 2250 + k * 56;
      x.fillRect(ax, SUELO - 30, 10, 30);
      x.beginPath(); x.moveTo(ax + 10, SUELO - 30); x.quadraticCurveTo(ax + 33, SUELO - 4, ax + 56, SUELO - 30); x.lineTo(ax + 56, SUELO - 34); x.lineTo(ax + 10, SUELO - 34); x.fill();
    }
    // El silo de la harina con su letrero.
    x.fillStyle = c.lejos;
    for (let k = 0; k < 4; k++) x.fillRect(1180 + k * 26, SUELO - 90, 22, 90);
    x.fillRect(1176, SUELO - 96, 110, 8);
    x.fillStyle = c.letrero;
    x.fillRect(1170, SUELO - 120, 122, 18);
    // Abetos.
    for (let i = 0; i < 40; i++) {
      const px = r() * ANCHO, h = 18 + r() * 26;
      x.fillStyle = c.pino;
      x.beginPath(); x.moveTo(px, SUELO - 4 - h); x.lineTo(px - h * 0.32, SUELO - 4); x.lineTo(px + h * 0.32, SUELO - 4); x.fill();
    }
    // Torres de la ciudad a los lados.
    for (const [x0, x1] of [[3000, 3550], [500, 950]]) {
      let cx = x0;
      while (cx < x1) {
        const w = 22 + r() * 40, h = 40 + r() * 110;
        torre(x, [cx, 0], w, h, c.lejos, r, r() < 0.2 ? "antena" : null);
        cx += w * 0.9;
      }
    }
  },
  // 12/11: Monte Rushmore: las Black Hills, colinas oscuras de pinos ("negras"
  // de lejos), agujas de granito y el pico del monumento.
  rushmore(x, c, r) {
    for (let capa = 0; capa < 3; capa++) {
      x.fillStyle = capa === 0 ? c.lejos : capa === 1 ? c.pino : c.cerca;
      const base = SUELO - 4, alto = [120, 85, 50][capa];
      x.beginPath(); x.moveTo(0, base);
      for (let px = 0; px <= ANCHO; px += 40) {
        const h = alto * (0.55 + 0.45 * Math.sin(px * 0.004 + capa * 1.7) * Math.sin(px * 0.0013 + capa)) + r() * 10;
        x.lineTo(px, base - h);
      }
      x.lineTo(ANCHO, base); x.closePath(); x.fill();
    }
    // Agujas de granito.
    x.fillStyle = c.monumento;
    for (let i = 0; i < 14; i++) {
      const px = r() * ANCHO, h = 40 + r() * 70, w = 8 + r() * 10;
      x.beginPath(); x.moveTo(px - w, SUELO - 4); x.lineTo(px - w * 0.3, SUELO - 4 - h); x.lineTo(px + w * 0.3, SUELO - 4 - h * 0.92); x.lineTo(px + w, SUELO - 4); x.fill();
    }
    // Pinos sueltos delante.
    for (let i = 0; i < 50; i++) {
      const px = r() * ANCHO, h = 16 + r() * 22;
      x.fillStyle = c.pino;
      x.beginPath(); x.moveTo(px, SUELO - 4 - h); x.lineTo(px - h * 0.28, SUELO - 4); x.lineTo(px + h * 0.28, SUELO - 4); x.fill();
    }
  },
  // 13/11: Little Rock: las colinas de las Ozark en otoño, el río Arkansas
  // con el puente de hierro y las torres del centro.
  littlerock(x, c, r) {
    for (let capa = 0; capa < 2; capa++) {
      x.fillStyle = capa === 0 ? c.lejos : c.arbol;
      x.beginPath(); x.moveTo(0, SUELO - 4);
      for (let px = 0; px <= ANCHO; px += 40) x.lineTo(px, SUELO - 4 - (40 + capa * -14) * (0.6 + 0.4 * Math.sin(px * 0.003 + capa * 2)) - r() * 8);
      x.lineTo(ANCHO, SUELO - 4); x.closePath(); x.fill();
    }
    x.fillStyle = c.lago;
    x.fillRect(0, SUELO - 8, ANCHO, 6);
    x.fillStyle = c.puente;
    x.fillRect(2600, SUELO - 22, 420, 5);
    for (let k = 0; k < 6; k++) x.fillRect(2600 + k * 84, SUELO - 22, 5, 22);
    for (const [x0, x1] of [[900, 1300]]) {
      let cx = x0;
      while (cx < x1) { const w = 24 + r() * 30, h = 40 + r() * 80; torre(x, [cx, 0], w, h, c.lejos, r, null); cx += w * 0.9; }
    }
  },
  // 13/11: Jackson: el río, un barco de vapor a lo lejos, algodonales y robles.
  // 13/11: Nueva Orleans: el Misisipi con el puente Crescent City Connection,
  // las torres del centro y el Superdome a lo lejos.
  nuevaorleans(x, c, r) {
    x.fillStyle = c.lago;
    x.fillRect(0, SUELO - 7, ANCHO, 6);
    x.fillStyle = c.puente;
    x.fillRect(380, SUELO - 30, 760, 4);
    for (const cx of [600, 920]) {
      x.beginPath(); x.moveTo(cx - 130, SUELO - 30); x.lineTo(cx, SUELO - 74); x.lineTo(cx + 130, SUELO - 30);
      x.lineTo(cx + 116, SUELO - 30); x.lineTo(cx, SUELO - 64); x.lineTo(cx - 116, SUELO - 30); x.closePath(); x.fill();
      x.fillRect(cx - 4, SUELO - 74, 8, 68);
    }
    for (const [x0, x1] of [[1500, 1980]]) {
      let cx = x0;
      while (cx < x1) { const w = 24 + r() * 30, h = 50 + r() * 90; torre(x, [cx, 0], w, h, c.lejos, r, null); cx += w * 0.9; }
    }
    x.fillStyle = c.vela;
    x.beginPath(); x.ellipse(2400, SUELO - 20, 80, 24, 0, Math.PI, 0); x.fill();
    x.fillRect(2320, SUELO - 20, 160, 16);
  },
  // 14/11: Nashville: las colinas de Tennessee, el rio Cumberland con su
  // puente de arcos y el centro con el «edificio Batman» (las dos orejas).
  nashville(x, c, r) {
    x.fillStyle = c.arbol;
    x.beginPath(); x.moveTo(0, SUELO - 4);
    for (let px = 0; px <= ANCHO; px += 40) x.lineTo(px, SUELO - 4 - 34 * (0.6 + 0.4 * Math.sin(px * 0.0021 + 2)) - r() * 5);
    x.lineTo(ANCHO, SUELO - 4); x.closePath(); x.fill();
    x.fillStyle = c.lago;
    x.fillRect(0, SUELO - 6, ANCHO, 5);
    x.strokeStyle = c.puente; x.fillStyle = c.puente; x.lineWidth = 4;
    x.fillRect(2500, SUELO - 24, 620, 4);
    for (let k = 0; k < 4; k++) { x.beginPath(); x.arc(2577 + k * 155, SUELO - 24, 74, Math.PI, 0); x.stroke(); }
    for (const [x0, x1] of [[900, 1250], [1420, 1800]]) {
      let cx = x0;
      while (cx < x1) { const w = 24 + r() * 28, h = 44 + r() * 80; torre(x, [cx, 0], w, h, c.lejos, r, null); cx += w * 0.9; }
    }
    x.fillStyle = c.willis;
    x.fillRect(1290, SUELO - 150, 86, 150);
    x.fillRect(1318, SUELO - 162, 30, 14);
    for (const px of [1296, 1366]) { x.beginPath(); x.moveTo(px - 5, SUELO - 150); x.lineTo(px, SUELO - 212); x.lineTo(px + 5, SUELO - 150); x.closePath(); x.fill(); }
  },
  // 14/11: Louisville: el rio Ohio con el puente de hierro (el Big Four) y el
  // de la autopista, el centro y, a un lado, las dos agujas de Churchill Downs.
  louisville(x, c, r) {
    x.fillStyle = c.arbol;
    x.beginPath(); x.moveTo(0, SUELO - 4);
    for (let px = 0; px <= ANCHO; px += 40) x.lineTo(px, SUELO - 4 - 18 * (0.6 + 0.4 * Math.sin(px * 0.0018)) - r() * 5);
    x.lineTo(ANCHO, SUELO - 4); x.closePath(); x.fill();
    x.fillStyle = c.lago;
    x.fillRect(0, SUELO - 7, ANCHO, 6);
    x.strokeStyle = c.puente; x.fillStyle = c.puente; x.lineWidth = 3;
    x.fillRect(500, SUELO - 30, 760, 4);
    for (let k = 0; k < 5; k++) {
      const a = 500 + k * 152;
      x.fillRect(a - 3, SUELO - 30, 6, 26);
      x.beginPath(); x.moveTo(a, SUELO - 30); x.lineTo(a + 30, SUELO - 62); x.lineTo(a + 122, SUELO - 62); x.lineTo(a + 152, SUELO - 30); x.stroke();
      for (let j = 1; j < 5; j++) { x.beginPath(); x.moveTo(a + j * 30.4, SUELO - 30); x.lineTo(a + j * 30.4, SUELO - 62); x.stroke(); }
    }
    for (const [x0, x1] of [[1500, 1980]]) {
      let cx = x0;
      while (cx < x1) { const w = 24 + r() * 30, h = 46 + r() * 84; torre(x, [cx, 0], w, h, c.lejos, r, null); cx += w * 0.9; }
    }
    x.fillStyle = c.vela;
    x.fillRect(2760, SUELO - 34, 300, 30);
    for (const px of [2880, 2940]) {
      x.fillRect(px - 7, SUELO - 50, 14, 18);
      x.beginPath(); x.moveTo(px - 9, SUELO - 50); x.lineTo(px, SUELO - 86); x.lineTo(px + 9, SUELO - 50); x.closePath(); x.fill();
    }
  },
  // 13/11: Birmingham: Red Mountain con Vulcano en lo alto, las chimeneas de
  // Sloss y, en el cielo, el huracan pintado con rotulador (con su cono).
  birmingham(x, c, r) {
    x.fillStyle = c.arbol;
    x.beginPath(); x.moveTo(0, SUELO - 4);
    for (let px = 0; px <= ANCHO; px += 40) x.lineTo(px, SUELO - 4 - 46 * (0.55 + 0.45 * Math.sin(px * 0.0016 + 1)) - r() * 6);
    x.lineTo(ANCHO, SUELO - 4); x.closePath(); x.fill();
    x.fillStyle = c.willis;
    x.fillRect(1300, SUELO - 112, 8, 26); x.fillRect(1297, SUELO - 126, 14, 16); x.fillRect(1310, SUELO - 140, 3, 16);
    for (const px of [700, 730, 760, 790]) x.fillRect(px, SUELO - 70 - (px % 60), 9, 70 + (px % 60));
    for (const [x0, x1] of [[1900, 2250]]) {
      let cx = x0;
      while (cx < x1) { const w = 22 + r() * 26, h = 40 + r() * 70; torre(x, [cx, 0], w, h, c.lejos, r, null); cx += w * 0.9; }
    }
    x.strokeStyle = "#16161a"; x.lineWidth = 6; x.lineCap = "round"; x.lineJoin = "round";
    x.beginPath();
    for (let a = 0; a < Math.PI * 6; a += 0.08) {
      const rr = 4 + a * 4.2, qx = 2900 + Math.cos(a) * rr, qy = SUELO - 260 + Math.sin(a) * rr * 0.8;
      if (a === 0) x.moveTo(qx, qy); else x.lineTo(qx, qy);
    }
    x.stroke();
    x.beginPath(); x.moveTo(2900, SUELO - 260); x.lineTo(3380, SUELO - 320); x.moveTo(2900, SUELO - 260); x.lineTo(3380, SUELO - 200); x.stroke();
    x.beginPath(); x.ellipse(3460, SUELO - 262, 90, 66, 0, 0, Math.PI * 2); x.stroke();
  },
  jackson(x, c, r) {
    x.fillStyle = c.lago;
    x.fillRect(0, SUELO - 7, ANCHO, 6);
    x.fillStyle = c.vela;
    x.fillRect(1800, SUELO - 26, 120, 14);
    x.fillRect(1820, SUELO - 38, 80, 12);
    x.fillStyle = c.willis;
    x.fillRect(1840, SUELO - 62, 7, 26); x.fillRect(1872, SUELO - 62, 7, 26);
    for (let i = 0; i < 60; i++) {
      const px = r() * ANCHO;
      x.fillStyle = r() < 0.5 ? c.arbol : c.cerca;
      x.beginPath(); x.ellipse(px, SUELO - 14, 14 + r() * 10, 10 + r() * 6, 0, 0, Math.PI * 2); x.fill();
    }
    for (const [x0, x1] of [[3000, 3300]]) {
      let cx = x0;
      while (cx < x1) { const w = 22 + r() * 26, h = 30 + r() * 50; torre(x, [cx, 0], w, h, c.lejos, r, null); cx += w * 0.9; }
    }
  },
  // 12/11: Houston: torres de cristal del centro, refinerias con chimeneas y
  // los balancines del petroleo en la llanura.
  houston(x, c, r) {
    for (const [x0, x1] of [[1500, 2600]]) {
      let cx = x0;
      while (cx < x1) {
        const w = 26 + r() * 40, h = 80 + r() * 170;
        torre(x, [cx, 0], w, h, c.lejos, r, r() < 0.3 ? "antena" : null);
        cx += w * 0.85;
      }
    }
    x.fillStyle = c.cerca;
    for (const rx of [400, 3100]) {
      for (let k = 0; k < 6; k++) x.fillRect(rx + k * 30, SUELO - 40 - (k % 3) * 12, 16, 40 + (k % 3) * 12);
      for (let k = 0; k < 3; k++) x.fillRect(rx + 20 + k * 50, SUELO - 90, 5, 90);
    }
    for (let i = 0; i < 14; i++) {
      const px = r() * ANCHO;
      x.fillStyle = c.cerca;
      x.fillRect(px, SUELO - 22, 3, 22);
      x.beginPath(); x.moveTo(px - 14, SUELO - 24); x.lineTo(px + 14, SUELO - 20); x.lineTo(px + 14, SUELO - 17); x.lineTo(px - 14, SUELO - 21); x.fill();
    }
  },
  // 12/11: Oklahoma City: la llanura con torres de petroleo, el parque eolico
  // y las torres del centro.
  oklahoma(x, c, r) {
    for (let i = 0; i < 18; i++) {
      const px = r() * ANCHO, h = 50 + r() * 30;
      x.strokeStyle = c.molino; x.lineWidth = 3;
      x.beginPath(); x.moveTo(px, SUELO - 4); x.lineTo(px, SUELO - 4 - h); x.stroke();
      for (let k = 0; k < 3; k++) {
        const a = k * Math.PI * 2 / 3 + r();
        x.beginPath(); x.moveTo(px, SUELO - 4 - h); x.lineTo(px + Math.cos(a) * 26, SUELO - 4 - h + Math.sin(a) * 26); x.stroke();
      }
    }
    x.fillStyle = c.cerca;
    for (let i = 0; i < 10; i++) {
      const px = r() * ANCHO, h = 40 + r() * 30;
      x.beginPath(); x.moveTo(px - 12, SUELO - 4); x.lineTo(px, SUELO - 4 - h); x.lineTo(px + 12, SUELO - 4); x.closePath(); x.fill();
    }
    for (const [x0, x1] of [[1800, 2300]]) {
      let cx = x0;
      while (cx < x1) {
        const w = 26 + r() * 34, h = 60 + r() * 110;
        torre(x, [cx, 0], w, h, c.lejos, r, null);
        cx += w * 0.9;
      }
    }
  },
  // 12/11: Fargo: la llanura nevada de Dakota del Norte, elevadores de grano,
  // el deposito de agua y la ventisca que lo vuelve todo blanco.
  fargo(x, c, r) {
    x.fillStyle = c.nieve;
    x.fillRect(0, SUELO - 6, ANCHO, 8);
    // Elevadores de grano.
    for (const ex of [700, 1500, 2900]) {
      x.fillStyle = c.silo;
      for (let k = 0; k < 4; k++) x.fillRect(ex + k * 24, SUELO - 70, 20, 70);
      x.fillRect(ex + 20, SUELO - 96, 30, 26);
      x.fillStyle = c.granero;
      x.fillRect(ex - 40, SUELO - 30, 40, 30);
    }
    // El deposito de agua.
    x.fillStyle = c.lejos;
    x.fillRect(2200, SUELO - 80, 3, 80); x.fillRect(2240, SUELO - 80, 3, 80);
    x.beginPath(); x.ellipse(2222, SUELO - 92, 30, 16, 0, 0, Math.PI * 2); x.fill();
    // Algunas casas y arboles pelados.
    for (let i = 0; i < 26; i++) {
      const px = r() * ANCHO;
      x.fillStyle = c.cerca;
      x.fillRect(px, SUELO - 14, 18 + r() * 14, 14);
      x.beginPath(); x.moveTo(px - 2, SUELO - 14); x.lineTo(px + 14, SUELO - 24); x.lineTo(px + 32, SUELO - 14); x.fill();
    }
    // Torres de la ciudad, a los lados.
    for (const [x0, x1] of [[3100, 3450], [400, 650]]) {
      let cx = x0;
      while (cx < x1) {
        const w = 22 + r() * 30, h = 30 + r() * 60;
        torre(x, [cx, 0], w, h, c.lejos, r, null);
        cx += w * 0.9;
      }
    }
  },
  // 08/11: Kansas (Wichita): la llanura de trigo hasta el horizonte, elevadores
  // de grano y, a lo lejos, el embudo del tornado bajo la nube (quieto: el que
  // gira es el de cerca, en la calle).
  kansas(x, c, r) {
    x.fillStyle = c.lejos;
    x.beginPath(); x.moveTo(0, SUELO);
    for (let i = 0; i <= 40; i++) x.lineTo((i / 40) * ANCHO, SUELO - 6 - Math.sin(i * 0.5) * 3 - r() * 2);
    x.lineTo(ANCHO, SUELO); x.fill();
    x.fillStyle = c.silo;
    for (let k = 0; k < 7; k++) {
      const cx = 200 + k * 560 + r() * 200;
      x.fillRect(cx, SUELO - 90, 26, 90); x.fillRect(cx + 26, SUELO - 70, 22, 70); x.fillRect(cx + 4, SUELO - 104, 16, 14);
    }
    x.fillStyle = c.granero;
    for (let k = 0; k < 9; k++) { const cx = 90 + k * 430 + r() * 120; x.fillRect(cx, SUELO - 22, 34, 22); }
    // La nube del tornado y el embudo.
    x.fillStyle = c.cerca;
    x.beginPath(); x.ellipse(1700, SUELO - 210, 520, 70, 0, 0, Math.PI * 2); x.fill();
    x.beginPath();
    x.moveTo(1600, SUELO - 200); x.quadraticCurveTo(1680, SUELO - 90, 1700, SUELO);
    x.lineTo(1716, SUELO); x.quadraticCurveTo(1740, SUELO - 100, 1820, SUELO - 200); x.closePath(); x.fill();
  },
  iowa(x, c, r) {
    // Iowa en invierno (01/11): campos llanos nevados hasta donde se ve,
    // hileras de arboles, granjas rojas con el tejado blanco, silos, un
    // elevador de grano y los molinos de viento (quietos: nada da vueltas).
    x.fillStyle = c.lejos;
    x.beginPath(); x.moveTo(0, SUELO);
    for (let i = 0; i <= 40; i++) x.lineTo((i / 40) * ANCHO, SUELO - 10 - Math.sin(i * 0.6) * 4 - r() * 3);
    x.lineTo(ANCHO, SUELO); x.fill();
    for (let i = 0; i < 26; i++) {                                   // hileras de arboles
      const cx = r() * ANCHO, w = 60 + r() * 140;
      x.fillStyle = c.arbol;
      for (let k = 0; k < w; k += 7) { const h = 10 + r() * 9; x.fillRect(cx + k, SUELO - h, 5, h); }
    }
    for (let k = 0; k < 10; k++) {                                    // granjas
      const cx = 140 + k * 400 + r() * 140;
      x.fillStyle = c.granero;
      x.fillRect(cx, SUELO - 30, 42, 30);
      x.fillStyle = c.nieve;
      x.beginPath(); x.moveTo(cx - 4, SUELO - 30); x.lineTo(cx + 21, SUELO - 47); x.lineTo(cx + 46, SUELO - 30); x.fill();
      x.fillStyle = c.silo;
      for (let s = 0; s < 1 + Math.floor(r() * 2); s++) {
        const sx = cx + 50 + s * 18;
        x.fillRect(sx, SUELO - 62, 14, 62);
        x.fillStyle = c.nieve; x.beginPath(); x.arc(sx + 7, SUELO - 62, 7, Math.PI, 0); x.fill();
        x.fillStyle = c.silo;
      }
    }
    x.fillStyle = c.cerca;                                            // elevador de grano
    x.fillRect(2300, SUELO - 110, 60, 110); x.fillRect(2360, SUELO - 80, 30, 80); x.fillRect(2318, SUELO - 128, 22, 18);
    x.strokeStyle = c.molino; x.lineWidth = 3; x.fillStyle = c.molino;
    for (let k = 0; k < 14; k++) {                                    // molinos de viento
      const mx = 80 + k * 290 + r() * 90, h = 70 + r() * 40, a0 = r() * Math.PI;
      x.fillRect(mx - 1.5, SUELO - h, 3, h);
      for (let b = 0; b < 3; b++) {
        const a = a0 + (b * Math.PI * 2) / 3;
        x.beginPath(); x.moveTo(mx, SUELO - h); x.lineTo(mx + Math.cos(a) * 26, SUELO - h + Math.sin(a) * 26); x.stroke();
      }
    }
  },
  desierto(x, c, r) {
    for (const [color, hBase, n] of [[c.lejos, 70, 7], [c.cerca, 45, 9]]) {
      for (let i = 0; i < n; i++) {
        const cx = r() * ANCHO, w = 160 + r() * 300, h = hBase + r() * 60;
        x.fillStyle = color;
        x.beginPath(); x.moveTo(cx - w * 0.15, SUELO); x.lineTo(cx, SUELO - h); x.lineTo(cx + w, SUELO - h); x.lineTo(cx + w * 1.15, SUELO); x.fill();
        x.fillStyle = "rgba(255,255,255,0.08)";
        for (let s = 1; s < 4; s++) x.fillRect(cx - w * 0.05, SUELO - h + s * (h / 4), w * 1.1, 3);
      }
    }
  },
  pueblo(x, c, r) {
    for (const [color, h0] of [[c.lejos, 60], [c.cerca, 35]]) {
      x.fillStyle = color;
      x.beginPath(); x.moveTo(0, SUELO);
      for (let i = 0; i <= 50; i++) x.lineTo((i / 50) * ANCHO, SUELO - h0 - Math.sin(i * 0.45 + h0) * 18 - r() * 6);
      x.lineTo(ANCHO, SUELO); x.fill();
    }
    for (let i = 0; i < 90; i++) { const tx = r() * ANCHO, rr = 8 + r() * 12; x.fillStyle = c.arbol; x.beginPath(); x.arc(tx, SUELO - 20 - r() * 20, rr, 0, Math.PI * 2); x.fill(); }
    x.fillStyle = c.cerca;
    x.fillRect(2100, SUELO - 90, 3, 90); x.fillRect(2130, SUELO - 90, 3, 90);
    x.beginPath(); x.ellipse(2116, SUELO - 98, 24, 13, 0, 0, Math.PI * 2); x.fill();
  },
};

// Colores de cada sitio a partir del cielo y la niebla del nivel.
function colores(sitio, cielo, niebla) {
  const base = { manhattan: 0x6f7f9c, ohio: 0x5f8a58, dc: 0x8592a6, desierto: 0xc07a4a, pueblo: 0x6f9a6a, phoenix: 0xa0644e, vegas: 0x5a4580, iowa: 0x8e9cb2, kansas: 0x5e6a5a, chicago: 0x66788f, milwaukee: 0x7a7f8f, minneapolis: 0x7a8aa0, rushmore: 0x2f4a36, fargo: 0x8a96a8, houston: 0x6a7a90, oklahoma: 0x8a7a5a, littlerock: 0x7a6a4a, jackson: 0x6a7a5a, nuevaorleans: 0x5a4a7a, birmingham: 0x7a6a5a, nashville: 0x7a5a6a, louisville: 0x6a7a8a }[sitio];
  return {
    lejos: mezcla(base, cielo, 0.55),
    cerca: mezcla(base, cielo, 0.3),
    suelo: mezcla(niebla, base, 0.25),
    granero: mezcla(0xa8443a, cielo, 0.35),
    silo: mezcla(0xc8ccd2, cielo, 0.3),
    arbol: mezcla(0x4f7a46, cielo, 0.4),
    monumento: mezcla(0xf3ece0, cielo, 0.2),
    nieve: mezcla(0xf6f9fc, cielo, 0.25),
    molino: mezcla(0xf4f6f8, cielo, 0.35),
    lago: mezcla(0x2f6fa8, cielo, 0.35),
    vela: mezcla(0xffffff, cielo, 0.2),
    willis: mezcla(0x2a2e36, cielo, 0.3),
    puente: mezcla(0xa8b4bc, cielo, 0.4),
    pino: mezcla(0x2a4a34, cielo, 0.45),
    letrero: mezcla(0xd8b040, cielo, 0.35),
  };
}

export function crearHorizonte(scene) {
  const c = document.createElement("canvas");
  c.width = ANCHO; c.height = ALTO;
  const tex = new THREE.CanvasTexture(c);
  tex.colorSpace = THREE.SRGBColorSpace;
  tex.wrapS = THREE.RepeatWrapping;
  tex.repeat.x = -1;                 // se ve por dentro: sin esto saldria al reves
  tex.anisotropy = 4;
  const geo = new THREE.CylinderGeometry(R, R, ALTO_BANDA, 72, 1, true, Math.PI - ARCO / 2, ARCO);
  const mat = new THREE.MeshBasicMaterial({ map: tex, side: THREE.BackSide, fog: false, transparent: true, depthWrite: false });
  const banda = new THREE.Mesh(geo, mat);
  banda.position.set(0, BAJO + ALTO_BANDA / 2, 9.8);
  banda.renderOrder = -2;
  scene.add(banda);

  // Nubes: sprites grandes y blancos, altos y lejanos, que van muy despacio.
  const texNube = (() => {
    const n = document.createElement("canvas");
    n.width = 512; n.height = 256;
    const x = n.getContext("2d");
    const bolas = [[150, 170, 70], [230, 130, 95], [330, 150, 80], [400, 180, 60], [90, 190, 45], [280, 190, 70]];
    for (const [bx, by, br] of bolas) {
      const g = x.createRadialGradient(bx - br * 0.3, by - br * 0.4, br * 0.2, bx, by, br);
      g.addColorStop(0, "rgba(255,255,255,1)"); g.addColorStop(0.75, "rgba(246,249,255,0.96)"); g.addColorStop(1, "rgba(225,235,250,0)");
      x.fillStyle = g; x.beginPath(); x.arc(bx, by, br, 0, Math.PI * 2); x.fill();
    }
    const t = new THREE.CanvasTexture(n);
    t.colorSpace = THREE.SRGBColorSpace;
    return t;
  })();
  const nubes = [];
  const rn = azar(77);
  for (let i = 0; i < 9; i++) {
    const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: texNube, fog: false, transparent: true, depthWrite: false, opacity: 0.95 }));
    const w = 70 + rn() * 70;
    s.scale.set(w, w / 2, 1);
    s.position.set(-170 + i * 42 + rn() * 20, 52 + rn() * 34, -210 - rn() * 50);
    s.renderOrder = -1;
    s.userData.v = 0.6 + rn() * 0.8;
    scene.add(s);
    nubes.push(s);
  }

  let pintado = "";
  return {
    // sitio: manhattan | ohio | dc | desierto | pueblo; colores del cielo y la niebla de ese momento.
    pintar(sitio, cielo, niebla) {
      const clave = sitio + cielo + niebla;
      if (clave === pintado) return;
      pintado = clave;
      const x = c.getContext("2d");
      x.clearRect(0, 0, ANCHO, ALTO);
      const col = colores(sitio, cielo, niebla);
      SITIOS[sitio](x, col, azar(sitio.length * 991));
      // Por debajo de la linea del suelo, del color de la niebla: se funde con la calle lejana.
      const g = x.createLinearGradient(0, SUELO - 6, 0, ALTO);
      g.addColorStop(0, col.suelo); g.addColorStop(1, new THREE.Color(niebla).getStyle());
      x.fillStyle = g; x.fillRect(0, SUELO - 2, ANCHO, ALTO - SUELO + 2);
      tex.needsUpdate = true;
      const blanco = sitio === "desierto" || sitio === "phoenix" ? 0xfff2e0 : sitio === "vegas" ? 0xffc8e4 : 0xffffff;
      for (const n of nubes) n.material.color.set(blanco);
    },
    // 07/11: dentro del metro no se ve el horizonte.
    mostrar(v) {
      if (banda.visible === v) return;
      banda.visible = v;
      for (const n of nubes) n.visible = v;
    },
    animar(dt) {
      for (const n of nubes) {
        n.position.x += n.userData.v * dt;
        if (n.position.x > 200) n.position.x -= 400;
      }
    },
  };
}
