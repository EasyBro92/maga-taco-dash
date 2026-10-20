// Reporte de errores. Hoy captura y guarda localmente; el hueco para un
// servicio remoto (Sentry u otro) queda listo para conectarse en initErrorReporting
// en cuanto exista una cuenta/DSN real.
const LOG_KEY = "tacoDashErrorLog_v1";
const MAX_ENTRIES = 30;

let remoteReporter = null;

function readLog() {
  try {
    return JSON.parse(localStorage.getItem(LOG_KEY)) || [];
  } catch (e) {
    return [];
  }
}

function writeLog(entries) {
  try {
    localStorage.setItem(LOG_KEY, JSON.stringify(entries.slice(-MAX_ENTRIES)));
  } catch (e) {}
}

export function reportError(message, extra) {
  const entry = { message: String(message), extra: extra || null, time: new Date().toISOString() };
  console.error("[TacoDash]", entry.message, extra || "");
  const entries = readLog();
  entries.push(entry);
  writeLog(entries);
  if (remoteReporter) {
    try { remoteReporter(entry); } catch (e) {}
  }
}

export function getErrorLog() {
  return readLog();
}

export function clearErrorLog() {
  writeLog([]);
}

// Llamar aqui con un adaptador (ej. Sentry.captureException) cuando exista un DSN real.
export function setRemoteReporter(fn) {
  remoteReporter = fn;
}

export function initErrorReporting() {
  window.addEventListener("error", (e) => {
    reportError(e.message, { source: e.filename, line: e.lineno, col: e.colno, stack: e.error && e.error.stack });
  });
  window.addEventListener("unhandledrejection", (e) => {
    reportError("Unhandled promise rejection: " + (e.reason && e.reason.message ? e.reason.message : e.reason), { stack: e.reason && e.reason.stack });
  });
}
