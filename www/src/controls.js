// Captura swipe (movil) y teclado (escritorio) y emite acciones: left, right, jump, slide
// y (25/10) frase: un toque corto en la pantalla, o la tecla F / Intro, lanza una frase.
//
// 27/10: el gesto cuenta en cuanto el dedo ha recorrido lo bastante, sin
// esperar a que se levante (antes se leia al soltar y llegaba con retraso:
// costaba saltar a tiempo).
// 27/10 (2): un solo gesto por cada vez que se pone el dedo. Antes, con el
// dedo aun puesto, se encadenaba otro y un deslizamiento largo cambiaba dos
// carriles de golpe (de una esquina a la otra). Isidro prefiere tener que
// deslizar dos veces para pasar dos carriles.
let swipeMinPx = 28;

export function setSwipeThreshold(px) {
  swipeMinPx = px;
}

export function initControls(target, onAction) {
  let startX = 0, startY = 0, startT = 0, tracking = false, hizoGesto = false;

  target.addEventListener("touchstart", (e) => {
    const t = e.changedTouches[0];
    startX = t.clientX; startY = t.clientY; startT = performance.now();
    tracking = true; hizoGesto = false;
  }, { passive: true });

  target.addEventListener("touchmove", (e) => {
    if (!tracking || hizoGesto) return;
    const t = e.changedTouches[0];
    const dx = t.clientX - startX;
    const dy = t.clientY - startY;
    const adx = Math.abs(dx), ady = Math.abs(dy);
    if (adx < swipeMinPx && ady < swipeMinPx) return;
    if (adx > ady) onAction(dx > 0 ? "right" : "left");
    else onAction(dy > 0 ? "slide" : "jump");
    hizoGesto = true;   // hasta levantar el dedo, nada mas
  }, { passive: true });

  target.addEventListener("touchend", () => {
    if (!tracking) return;
    tracking = false;
    // Toque corto sin gesto: lanzar una frase (si dura mucho, se dejo el dedo puesto).
    if (!hizoGesto && performance.now() - startT < 350) onAction("frase");
  }, { passive: true });

  target.addEventListener("touchcancel", () => { tracking = false; }, { passive: true });

  window.addEventListener("keydown", (e) => {
    switch (e.key) {
      case "ArrowLeft": case "a": case "A": onAction("left"); break;
      case "ArrowRight": case "d": case "D": onAction("right"); break;
      case "ArrowUp": case "w": case "W": case " ": onAction("jump"); break;
      case "ArrowDown": case "s": case "S": onAction("slide"); break;
      case "f": case "F": case "Enter": onAction("frase"); break;
      case "Escape": case "p": case "P": onAction("pausa"); break;
    }
  });
}
