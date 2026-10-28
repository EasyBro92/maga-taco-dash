// Iconos propios de la interfaz (27/10/2026). Antes eran emojis, que cambian
// de un móvil a otro y no pegaban con el estilo Pixar de los menús. Todos con
// la misma mano: trazo redondeado, colores de la bandera y la tinta de la
// interfaz. Se pintan con `icono(nombre)` o con data-icono="nombre" en el HTML.

const T = "#22304f";       // tinta
const R = "#e8463c", A = "#2f6bd8", O = "#ffc23c", B = "#ffffff";
const svg = (cuerpo, vb = 24) => `<svg class="ico" viewBox="0 0 ${vb} ${vb}" aria-hidden="true">${cuerpo}</svg>`;
const estrella = (fill, stroke) => `<path d="M12 2.6l2.8 5.9 6.4.8-4.7 4.4 1.2 6.4L12 17l-5.7 3.1 1.2-6.4-4.7-4.4 6.4-.8z" fill="${fill}" stroke="${stroke}" stroke-width="1.6" stroke-linejoin="round"/>`;

const ICONOS = {
  pausa: svg(`<rect x="6" y="5" width="4.2" height="14" rx="1.6" fill="${T}"/><rect x="13.8" y="5" width="4.2" height="14" rx="1.6" fill="${T}"/>`),
  play: svg(`<path d="M8 5.5v13l10.5-6.5z" fill="${T}" stroke="${T}" stroke-width="2" stroke-linejoin="round"/>`),
  musica: svg(`<path d="M9 17.5V6.5l10-2v11" fill="none" stroke="${T}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/><circle cx="6.8" cy="17.5" r="2.6" fill="${T}"/><circle cx="16.8" cy="15.5" r="2.6" fill="${T}"/>`),
  musicaNo: svg(`<path d="M9 17.5V6.5l10-2v11" fill="none" stroke="#9aa4b8" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/><circle cx="6.8" cy="17.5" r="2.6" fill="#9aa4b8"/><circle cx="16.8" cy="15.5" r="2.6" fill="#9aa4b8"/><path d="M4 4l16 16" stroke="${R}" stroke-width="2.6" stroke-linecap="round"/>`),
  sonido: svg(`<path d="M4 9.5h3.5L12 5.5v13l-4.5-4H4z" fill="${T}" stroke="${T}" stroke-width="1.6" stroke-linejoin="round"/><path d="M15.5 9a4 4 0 010 6M18 6.5a7.5 7.5 0 010 11" fill="none" stroke="${T}" stroke-width="2.2" stroke-linecap="round"/>`),
  sonidoNo: svg(`<path d="M4 9.5h3.5L12 5.5v13l-4.5-4H4z" fill="#9aa4b8" stroke="#9aa4b8" stroke-width="1.6" stroke-linejoin="round"/><path d="M15.5 9.5l5 5M20.5 9.5l-5 5" stroke="${R}" stroke-width="2.4" stroke-linecap="round"/>`),
  mapa: svg(`<path d="M3.5 6.5l5.5-2 6 2 5.5-2v13l-5.5 2-6-2-5.5 2z" fill="#e9dcc0" stroke="${T}" stroke-width="1.8" stroke-linejoin="round"/><path d="M9 4.5v13M15 6.5v13" stroke="${T}" stroke-width="1.6"/><circle cx="17.5" cy="10" r="1.8" fill="${R}"/>`),
  infinito: svg(`<path d="M7 8.5c-2 0-3.5 1.5-3.5 3.5S5 15.5 7 15.5c3.5 0 6.5-7 10-7 2 0 3.5 1.5 3.5 3.5S19 15.5 17 15.5c-3.5 0-6.5-7-10-7z" fill="none" stroke="${A}" stroke-width="2.6" stroke-linecap="round"/>`),
  tienda: svg(`<path d="M4 9h16l-1.3 10.2a1.6 1.6 0 01-1.6 1.3H6.9a1.6 1.6 0 01-1.6-1.3z" fill="${O}" stroke="${T}" stroke-width="1.8" stroke-linejoin="round"/><path d="M8.5 9V7a3.5 3.5 0 017 0v2" fill="none" stroke="${T}" stroke-width="2" stroke-linecap="round"/>`),
  ajustes: svg(`<circle cx="12" cy="12" r="3.2" fill="none" stroke="${T}" stroke-width="2.2"/><path d="M12 3v2.6M12 18.4V21M3 12h2.6M18.4 12H21M5.6 5.6l1.9 1.9M16.5 16.5l1.9 1.9M5.6 18.4l1.9-1.9M16.5 7.5l1.9-1.9" stroke="${T}" stroke-width="2.4" stroke-linecap="round"/>`),
  idioma: svg(`<circle cx="12" cy="12" r="8.5" fill="none" stroke="${A}" stroke-width="2"/><path d="M3.5 12h17M12 3.5c3 3 3 14 0 17M12 3.5c-3 3-3 14 0 17" fill="none" stroke="${A}" stroke-width="1.8"/>`),
  candado: svg(`<rect x="5" y="10.5" width="14" height="10" rx="2.4" fill="#9aa4b8"/><path d="M8 10.5V8a4 4 0 018 0v2.5" fill="none" stroke="#9aa4b8" stroke-width="2.4"/><circle cx="12" cy="15.5" r="1.6" fill="${B}"/>`),
  meta: svg(`<path d="M6 21V3.5" stroke="${T}" stroke-width="2.2" stroke-linecap="round"/><path d="M6 4h12l-2.5 4L18 12H6z" fill="${B}" stroke="${T}" stroke-width="1.6" stroke-linejoin="round"/><path d="M9 4h3v4H9zM12 8h3v4h-3zM6 8h3v4H6z" fill="${T}"/>`),
  control: svg(`<path d="M6 21V3.5" stroke="${T}" stroke-width="2.2" stroke-linecap="round"/><path d="M6 4h11.5l-2.5 4 2.5 4H6z" fill="${A}" stroke="${T}" stroke-width="1.4" stroke-linejoin="round"/><path d="M10.2 6.2l.9 1.7 1.9.3-1.4 1.3.3 1.9-1.7-.9-1.7.9.3-1.9-1.4-1.3 1.9-.3z" fill="${B}"/>`),
  estrella: svg(estrella("#ffc23c", "#c98a00")),
  estrellaVacia: svg(estrella("#e3e8f1", "#b9c3d4")),
  check: svg(`<circle cx="12" cy="12" r="9.5" fill="#2fa84f"/><path d="M7.5 12.3l3 3 6-6.3" fill="none" stroke="${B}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>`),
  cruz: svg(`<circle cx="12" cy="12" r="9.5" fill="#dfe6f2"/><path d="M8.5 8.5l7 7M15.5 8.5l-7 7" stroke="#9aa4b8" stroke-width="2.4" stroke-linecap="round"/>`),
  escudo: svg(`<path d="M12 2.8l7.5 3v5.6c0 4.6-3.2 8-7.5 9.8-4.3-1.8-7.5-5.2-7.5-9.8V5.8z" fill="${O}" stroke="#b07a00" stroke-width="1.6" stroke-linejoin="round"/><path d="M12 7.2l1.5 3.1 3.3.4-2.4 2.3.6 3.3-3-1.6-3 1.6.6-3.3-2.4-2.3 3.3-.4z" fill="${B}"/>`),
  iman: svg(`<path d="M5.5 4.5h4v7a2.5 2.5 0 005 0v-7h4v7a6.5 6.5 0 01-13 0z" fill="${R}" stroke="#a5231b" stroke-width="1.4" stroke-linejoin="round"/><path d="M5.5 4.5h4v3h-4zM14.5 4.5h4v3h-4z" fill="#dfe6f2"/>`),
  boost: svg(`<path d="M13.5 2.5L5 13.5h6l-1.5 8 9-11.5h-6z" fill="${O}" stroke="#b07a00" stroke-width="1.6" stroke-linejoin="round"/>`),
  cohete: svg(`<path d="M12 2.5c3.5 2.5 5 6.5 4 11.5H8c-1-5 .5-9 4-11.5z" fill="${B}" stroke="${T}" stroke-width="1.6" stroke-linejoin="round"/><circle cx="12" cy="9" r="2" fill="${A}"/><path d="M8 14l-2.5 3.5H9M16 14l2.5 3.5H15" fill="${R}" stroke="${T}" stroke-width="1.4" stroke-linejoin="round"/><path d="M10 15.5h4l-2 5.5z" fill="${O}"/>`),
  regalo: svg(`<rect x="4" y="10" width="16" height="10.5" rx="1.6" fill="${A}" stroke="${T}" stroke-width="1.6"/><rect x="3" y="7" width="18" height="4" rx="1.2" fill="${A}" stroke="${T}" stroke-width="1.6"/><rect x="10.6" y="7" width="2.8" height="13.5" fill="${R}"/><path d="M12 7c-1.5-3.5-5.5-3.5-5 -1 .4 1.4 3 1 5 1zM12 7c1.5-3.5 5.5-3.5 5-1-.4 1.4-3 1-5 1z" fill="${R}" stroke="${T}" stroke-width="1.3" stroke-linejoin="round"/><text x="7.3" y="18.3" font-size="6.5" font-weight="900" font-family="sans-serif" fill="${O}">?</text>`),
  botas: svg(`<path d="M7 3.5h6v9.5l5.2 2.2c1.6.7 2.3 2 2.3 3.3v1.5H5.8l.4-3.5z" fill="${R}" stroke="${T}" stroke-width="1.6" stroke-linejoin="round"/><path d="M5.8 20h14.7" stroke="${T}" stroke-width="2.4" stroke-linecap="round"/><path d="M7 6h6" stroke="${B}" stroke-width="1.6"/><path d="M10 8.5l.8 1.6 1.7.2-1.3 1.1.4 1.7-1.6-.9-1.5.9.3-1.7-1.2-1.1 1.7-.2z" fill="${O}"/>`),
  gorra: svg(`<path d="M4 14.5c0-5 3.6-8.5 8-8.5s8 3.5 8 8.5z" fill="${R}" stroke="#a5231b" stroke-width="1.6" stroke-linejoin="round"/><path d="M2.5 14.5h17.5c1.2 0 1.2 2.5 0 2.5H4.5c-1.4 0-2-1.2-2-2.5z" fill="#c83228"/><circle cx="12" cy="10" r="1.4" fill="${B}"/>`),
  hielo: svg(`<path d="M12 2.5v19M3.8 7.2l16.4 9.6M3.8 16.8l16.4-9.6" stroke="#3fb8e8" stroke-width="2.4" stroke-linecap="round"/><path d="M9.5 4l2.5 2 2.5-2M9.5 20l2.5-2 2.5 2" fill="none" stroke="#3fb8e8" stroke-width="2" stroke-linecap="round"/>`),
  micro: svg(`<rect x="8.5" y="2.8" width="7" height="11" rx="3.5" fill="#dfe3ea" stroke="${T}" stroke-width="1.6"/><path d="M6 11a6 6 0 0012 0M12 17v4M8.5 21h7" fill="none" stroke="${O}" stroke-width="2.2" stroke-linecap="round"/>`),
  microVacio: svg(`<rect x="8.5" y="2.8" width="7" height="11" rx="3.5" fill="#eef1f6" stroke="#b9c3d4" stroke-width="1.6"/><path d="M6 11a6 6 0 0012 0M12 17v4M8.5 21h7" fill="none" stroke="#b9c3d4" stroke-width="2.2" stroke-linecap="round"/>`),
  chile: svg(`<path d="M15.5 6.5c2.5 1 3 4.5.5 8-2.5 3.4-7.5 6-11 5 3-1.5 6-4 7.5-7.5 1-2.3 1-4.5 3-5.5z" fill="${R}" stroke="#a5231b" stroke-width="1.4" stroke-linejoin="round"/><path d="M15.5 6.5c0-2 1-3.5 3-4" fill="none" stroke="#3fae3a" stroke-width="2.2" stroke-linecap="round"/>`),
  jefe: svg(`<rect x="5.5" y="4" width="13" height="16" rx="6" fill="#f0cf8a" stroke="#b5813a" stroke-width="1.6"/><rect x="7.5" y="9" width="3.5" height="2.6" rx="1" fill="${R}"/><rect x="13" y="9" width="3.5" height="2.6" rx="1" fill="${R}"/><path d="M8.5 15.5h7" stroke="${T}" stroke-width="2" stroke-linecap="round"/>`),
  repetir: svg(`<path d="M5 12a7 7 0 1 0 2.1-5" fill="none" stroke="${T}" stroke-width="2.4" stroke-linecap="round"/><path d="M5 3.5v4h4" fill="none" stroke="${T}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>`),
  casa: svg(`<path d="M3.5 11L12 4l8.5 7" fill="none" stroke="${T}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/><path d="M6 10v9.5h12V10" fill="none" stroke="${T}" stroke-width="2.4" stroke-linejoin="round"/>`),
  avion: svg(`<path d="M21 3.5L3 11l6.5 2.5L12 20l3-6.5z" fill="${B}" stroke="${T}" stroke-width="1.6" stroke-linejoin="round"/>`),
};

export function icono(nombre) {
  return ICONOS[nombre] || "";
}

// Rellena los elementos con data-icono="nombre" (delante de su texto).
export function pintarIconos(raiz = document) {
  raiz.querySelectorAll("[data-icono]").forEach((el) => {
    const viejo = el.querySelector(":scope > svg.ico");
    if (viejo) viejo.remove();
    el.insertAdjacentHTML("afterbegin", icono(el.dataset.icono));
  });
}
