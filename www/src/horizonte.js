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
  const base = { manhattan: 0x6f7f9c, ohio: 0x5f8a58, dc: 0x8592a6, desierto: 0xc07a4a, pueblo: 0x6f9a6a, phoenix: 0xa0644e }[sitio];
  return {
    lejos: mezcla(base, cielo, 0.55),
    cerca: mezcla(base, cielo, 0.3),
    suelo: mezcla(niebla, base, 0.25),
    granero: mezcla(0xa8443a, cielo, 0.35),
    silo: mezcla(0xc8ccd2, cielo, 0.3),
    arbol: mezcla(0x4f7a46, cielo, 0.4),
    monumento: mezcla(0xf3ece0, cielo, 0.2),
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
      const blanco = sitio === "desierto" || sitio === "phoenix" ? 0xfff2e0 : 0xffffff;
      for (const n of nubes) n.material.color.set(blanco);
    },
    animar(dt) {
      for (const n of nubes) {
        n.position.x += n.userData.v * dt;
        if (n.position.x > 200) n.position.x -= 400;
      }
    },
  };
}
