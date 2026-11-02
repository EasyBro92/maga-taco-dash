// Convierte states-albers-10m.json (topojson) en caminos SVG por estado.
// Uso: node herramientas/hacer-mapa.cjs states-albers-10m.json www/src/mapa-eeuu.js 1.0
// (el json es de us-atlas 3.0.1: https://cdn.jsdelivr.net/npm/us-atlas@3.0.1/states-albers-10m.json)
const fs = require("fs");
const [, , ent, sal, tolArg] = process.argv;
const TOL = Number(tolArg || 0.6);
const topo = JSON.parse(fs.readFileSync(ent, "utf8"));
const { scale, translate } = topo.transform;

const CODIGOS = {
  Alabama: "AL", Alaska: "AK", Arizona: "AZ", Arkansas: "AR", California: "CA", Colorado: "CO",
  Connecticut: "CT", Delaware: "DE", "District of Columbia": "DC", Florida: "FL", Georgia: "GA",
  Hawaii: "HI", Idaho: "ID", Illinois: "IL", Indiana: "IN", Iowa: "IA", Kansas: "KS", Kentucky: "KY",
  Louisiana: "LA", Maine: "ME", Maryland: "MD", Massachusetts: "MA", Michigan: "MI", Minnesota: "MN",
  Mississippi: "MS", Missouri: "MO", Montana: "MT", Nebraska: "NE", Nevada: "NV", "New Hampshire": "NH",
  "New Jersey": "NJ", "New Mexico": "NM", "New York": "NY", "North Carolina": "NC", "North Dakota": "ND",
  Ohio: "OH", Oklahoma: "OK", Oregon: "OR", Pennsylvania: "PA", "Rhode Island": "RI",
  "South Carolina": "SC", "South Dakota": "SD", Tennessee: "TN", Texas: "TX", Utah: "UT", Vermont: "VT",
  Virginia: "VA", Washington: "WA", "West Virginia": "WV", Wisconsin: "WI", Wyoming: "WY",
};

// Arcos: deltas cuantizados -> puntos reales.
const arcos = topo.arcs.map((a) => {
  let x = 0, y = 0;
  return a.map(([dx, dy]) => { x += dx; y += dy; return [x * scale[0] + translate[0], y * scale[1] + translate[1]]; });
});
// Douglas-Peucker por arco, para que las fronteras compartidas sigan casando.
function dp(p, tol) {
  if (p.length < 3) return p;
  const keep = new Uint8Array(p.length); keep[0] = keep[p.length - 1] = 1;
  const pila = [[0, p.length - 1]];
  while (pila.length) {
    const [a, b] = pila.pop();
    const [ax, ay] = p[a], [bx, by] = p[b];
    const dx = bx - ax, dy = by - ay, L = Math.hypot(dx, dy);
    let mx = -1, mi = -1;
    for (let i = a + 1; i < b; i++) {
      // Arco cerrado (empieza y acaba en el mismo punto): distancia a ese punto.
      const d = L < 1e-9 ? Math.hypot(p[i][0] - ax, p[i][1] - ay) : Math.abs((p[i][0] - ax) * dy - (p[i][1] - ay) * dx) / L;
      if (d > mx) { mx = d; mi = i; }
    }
    if (mx > tol) { keep[mi] = 1; pila.push([a, mi], [mi, b]); }
  }
  return p.filter((_, i) => keep[i]);
}
const simples = arcos.map((a) => dp(a, TOL));
function anillo(ids) {
  const out = [];
  ids.forEach((i, k) => {
    let a = i < 0 ? simples[~i].slice().reverse() : simples[i];
    if (k) a = a.slice(1);
    out.push(...a);
  });
  return out;
}
function area(r) { let s = 0; for (let i = 0, j = r.length - 1; i < r.length; j = i++) s += r[j][0] * r[i][1] - r[i][0] * r[j][1]; return s / 2; }
function centroide(r) {
  let cx = 0, cy = 0, s = 0;
  for (let i = 0, j = r.length - 1; i < r.length; j = i++) {
    const f = r[j][0] * r[i][1] - r[i][0] * r[j][1];
    cx += (r[j][0] + r[i][0]) * f; cy += (r[j][1] + r[i][1]) * f; s += f;
  }
  return [cx / (3 * s), cy / (3 * s)];
}
const n = (v) => Math.round(v * 10) / 10;
const formas = {}, etiquetas = {}, cajas = {};
for (const g of topo.objects.states.geometries) {
  const cod = CODIGOS[g.properties.name];
  if (process.env.DEPURA) console.log(g.properties.name, g.type);
  if (!cod) { console.log("sin código:", g.properties.name); continue; }
  const polis = g.type === "Polygon" ? [g.arcs] : g.arcs;
  let d = "", mayor = null, mayorA = 0;
  let x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9;
  for (const poli of polis) {
    poli.forEach((ids, k) => {
      const r = anillo(ids);
      const A = r.length < 3 ? 0 : Math.abs(area(r));
      if (A < 1.5 && !(k === 0 && !mayor)) return; // islotes que no se ven
      d += "M" + r.map(([x, y]) => `${n(x)} ${n(y)}`).join("L") + "Z";
      if (k === 0 && A > mayorA) { mayorA = A; mayor = r; }
      for (const [x, y] of r) { x0 = Math.min(x0, x); y0 = Math.min(y0, y); x1 = Math.max(x1, x); y1 = Math.max(y1, y); }
    });
  }
  formas[cod] = d;
  etiquetas[cod] = centroide(mayor).map((v) => Math.round(v));
  cajas[cod] = [x0, y0, x1, y1].map((v) => Math.round(v));
}
const orden = Object.keys(formas).sort();
let js = "// Formas de los estados (02/11/2026), sacadas de us-atlas 3.0.1\n"
  + "// (states-albers-10m.json, mapas públicos del censo de EE. UU.), en proyección\n"
  + "// Albers de 975x610 con Alaska y Hawái abajo a la izquierda. Lo genera\n"
  + "// herramientas/hacer-mapa.cjs; no tocar a mano.\n";
js += "export const FORMAS = {\n" + orden.map((c) => `  ${c}: "${formas[c]}",`).join("\n") + "\n};\n";
js += "// Centro de la parte más grande de cada estado (para el número de votos).\n";
js += "export const CENTROS = {\n" + orden.map((c) => `  ${c}: [${etiquetas[c].join(", ")}],`).join("\n") + "\n};\n";
fs.writeFileSync(sal, js);
console.log("estados:", orden.length, "bytes:", js.length);
console.log(JSON.stringify(cajas));
