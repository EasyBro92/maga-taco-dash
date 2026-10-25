// Captura swipe (movil) y teclado (escritorio) y emite acciones: left, right, jump, slide
// y (25/10) frase: un toque corto en la pantalla, o la tecla F / Intro, lanza una frase.
let swipeMinPx = 28;

export function setSwipeThreshold(px) {
  swipeMinPx = px;
}

export function initControls(target, onAction) {
  let startX = 0, startY = 0, startT = 0, tracking = false;

  target.addEventListener("touchstart", (e) => {
    const t = e.changedTouches[0];
    startX = t.clientX; startY = t.clientY; startT = performance.now();
    tracking = true;
  }, { passive: true });

  target.addEventListener("touchend", (e) => {
    if (!tracking) return;
    tracking = false;
    const t = e.changedTouches[0];
    const dx = t.clientX - startX;
    const dy = t.clientY - startY;
    const adx = Math.abs(dx), ady = Math.abs(dy);
    if (adx < swipeMinPx && ady < swipeMinPx) {
      // Toque corto: lanzar una frase (si dura mucho, es que se dejo el dedo puesto).
      if (performance.now() - startT < 350) onAction("frase");
      return;
    }
    if (adx > ady) {
      onAction(dx > 0 ? "right" : "left");
    } else {
      onAction(dy > 0 ? "slide" : "jump");
    }
  }, { passive: true });

  window.addEventListener("keydown", (e) => {
    switch (e.key) {
      case "ArrowLeft": case "a": case "A": onAction("left"); break;
      case "ArrowRight": case "d": case "D": onAction("right"); break;
      case "ArrowUp": case "w": case "W": case " ": onAction("jump"); break;
      case "ArrowDown": case "s": case "S": onAction("slide"); break;
      case "f": case "F": case "Enter": onAction("frase"); break;
    }
  });
}
