const DICT = {
  es: {
    tapToStart: "Toca para correr",
    play: "JUGAR",
    shop: "Tienda",
    ranking: "Ranking",
    gameOver: "¡Te atraparon!",
    distance: "Distancia",
    retry: "REINTENTAR",
    menu: "Menú",
    newRecord: "¡Nuevo récord!",
    whatsYourName: "¿Cómo te llamas?",
    save: "Guardar",
    worldRanking: "Ranking mundial",
    close: "Cerrar",
    powerupShield: "Orden Ejecutiva",
    powerupMagnet: "Imán Dorado",
    powerupBoost: "Covfefe Boost",
    powerupMega: "Presidente Gigante",
    powerupFreeze: "Rayo Congelador",
    powerupRocket: "Cohete Presidencial",
    jefeLlega: "¡Llega el Burrito-Bot! Coge chiles 🌶️",
    jefeVencido: "¡Burrito-Bot derrotado!",
    jefeEscapa: "El Burrito-Bot huye...",
    misiones: "Misiones",
    misionCumplida: "¡Misión cumplida!",
    mis_tacos: "Recoge {n} tacos en una partida",
    mis_distancia: "Corre {n} m en una partida",
    mis_saltos: "Salta {n} obstáculos",
    mis_deslizar: "Deslízate bajo {n} obstáculos",
    mis_autobus: "Súbete a {n} autobuses",
    mis_gigante: "Aplasta {n} obstáculos en modo gigante",
    mis_hielo: "Rompe {n} obstáculos congelados",
    mis_cohete: "Vuela {n} veces en cohete",
    mis_jefe: "Derrota al Burrito-Bot {n} veces",
    settings: "Ajustes",
    music: "Música",
    sfx: "Sonido",
    sensitivity: "Sensibilidad",
    language: "Idioma",
    resetProgress: "Borrar progreso",
    resetConfirm: "¿Seguro? Se borrará tu récord, tacos y desbloqueos.",
    loading: "Cargando...",
    webglUnsupported: "Tu dispositivo no soporta este juego (falta WebGL).",
    quality: "Gráficos",
    qualityLow: "Baja",
    qualityMedium: "Media",
    qualityHigh: "Alta",
    zone: "Zona",
    zoneAuto: "🎲 Auto",
    zoneCity: "🏙️ Ciudad",
    zoneDesert: "🌵 Desierto",
    zoneTown: "🏘️ Pueblo",
    zoneDc: "🏛️ Washington D.C.",
  },
  en: {
    tapToStart: "Tap to run",
    play: "PLAY",
    shop: "Shop",
    ranking: "Ranking",
    gameOver: "You got caught!",
    distance: "Distance",
    retry: "RETRY",
    menu: "Menu",
    newRecord: "New record!",
    whatsYourName: "What's your name?",
    save: "Save",
    worldRanking: "World ranking",
    close: "Close",
    powerupShield: "Executive Order",
    powerupMagnet: "Golden Magnet",
    powerupBoost: "Covfefe Boost",
    powerupMega: "Giant President",
    powerupFreeze: "Freeze Ray",
    powerupRocket: "Presidential Rocket",
    jefeLlega: "Here comes Burrito-Bot! Grab chilis 🌶️",
    jefeVencido: "Burrito-Bot defeated!",
    jefeEscapa: "Burrito-Bot runs away...",
    misiones: "Missions",
    misionCumplida: "Mission complete!",
    mis_tacos: "Collect {n} tacos in one run",
    mis_distancia: "Run {n} m in one run",
    mis_saltos: "Jump over {n} obstacles",
    mis_deslizar: "Slide under {n} obstacles",
    mis_autobus: "Ride {n} buses",
    mis_gigante: "Smash {n} obstacles as a giant",
    mis_hielo: "Break {n} frozen obstacles",
    mis_cohete: "Fly the rocket {n} times",
    mis_jefe: "Defeat Burrito-Bot {n} times",
    settings: "Settings",
    music: "Music",
    sfx: "Sound",
    sensitivity: "Sensitivity",
    language: "Language",
    resetProgress: "Reset progress",
    resetConfirm: "Are you sure? This will erase your record, tacos and unlocks.",
    loading: "Loading...",
    webglUnsupported: "Your device doesn't support this game (WebGL missing).",
    quality: "Graphics",
    qualityLow: "Low",
    qualityMedium: "Medium",
    qualityHigh: "High",
    zone: "Zone",
    zoneAuto: "🎲 Auto",
    zoneCity: "🏙️ City",
    zoneDesert: "🌵 Desert",
    zoneTown: "🏘️ Suburbs",
    zoneDc: "🏛️ Washington D.C.",
  },
};

const CATCHPHRASES = {
  es: [
    "¡Tremendo!",
    "¡Nadie hace tacos mejor que yo!",
    "¡Increíble, believe me!",
    "¡Los mejores tacos, se lo prometo!",
    "¡Huge! Simplemente huge!",
    "¡Esto va a ser grande, muy grande!",
  ],
  en: [
    "Tremendous!",
    "Nobody makes tacos better than me!",
    "Believe me, incredible!",
    "The best tacos, believe me!",
    "Huge! Simply huge!",
    "This is going to be big, very big!",
  ],
};

export function randomCatchphrase() {
  const list = CATCHPHRASES[currentLang] || CATCHPHRASES.es;
  return list[Math.floor(Math.random() * list.length)];
}

const LANG_KEY = "tacoDashLang";

function detectDefaultLang() {
  const nav = (navigator.language || "es").toLowerCase();
  return nav.startsWith("en") ? "en" : "es";
}

let currentLang = localStorage.getItem(LANG_KEY) || detectDefaultLang();

export function getLang() {
  return currentLang;
}

export function t(key) {
  return (DICT[currentLang] && DICT[currentLang][key]) || DICT.es[key] || key;
}

export function setLang(lang) {
  currentLang = lang === "en" ? "en" : "es";
  localStorage.setItem(LANG_KEY, currentLang);
  applyI18n();
}

export function toggleLang() {
  setLang(currentLang === "es" ? "en" : "es");
}

export function applyI18n() {
  document.querySelectorAll("[data-i18n]").forEach((el) => {
    const key = el.getAttribute("data-i18n");
    el.textContent = t(key);
  });
  const langToggle = document.getElementById("langToggle");
  if (langToggle) langToggle.textContent = currentLang === "es" ? "EN" : "ES";
}
