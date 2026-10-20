// Captura swipe (movil) y teclado (escritorio) y emite acciones: left, right, jump, slide.
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
    if (adx < swipeMinPx && ady < swipeMinPx) return; // tap, ignored here
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
    }
  });
}
