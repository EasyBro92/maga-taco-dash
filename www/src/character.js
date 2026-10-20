import * as THREE from "../vendor/three.module.min.js";
import { toon, withOutline } from "./toon.js";

// Personaje estilo "juguete de vinilo" (referencia visual: Subway
// Surfers) -- formas grandes y limpias, pocos colores muy saturados,
// shading suave y brillante sin contorno (ver toon.js), proporciones
// chibi marcadas (cabeza grande, cuerpo y miembros cortos). Presidente
// trajeado como concepto propio, pero con esa ejecucion visual.
// Construido con primitivas, sin assets externos.

export const PLAYER_HEIGHT = 1.9;
export const PLAYER_RADIUS = 0.42;

// Altura de la cadera. Antes estaba escrita a mano (0.92) en cinco sitios
// distintos -- construccion + cada pose de animacion -- asi que cambiar las
// proporciones obligaba a acertar los cinco o el personaje se hundia en el
// suelo en una pose concreta. Ahora sale de aqui.
const HIP_Y = 0.845;

const COSMETIC_COLORS = {
  suit_navy: 0x2f6fff,
  suit_black: 0x2e3038,
  suit_red: 0xff3344,
  tie_red: 0xff4444,
  tie_blue: 0x3d7bff,
  tie_gold: 0xffc23c,
};

export function createCharacter(cosmetics) {
  cosmetics = cosmetics || { suit: "suit_navy", tie: "tie_red" };
  const suitColor = COSMETIC_COLORS[cosmetics.suit] || COSMETIC_COLORS.suit_navy;
  const tieColor = COSMETIC_COLORS[cosmetics.tie] || COSMETIC_COLORS.tie_red;

  // Colores solidos, sin textura: formas grandes y limpias en vez de
  // detalle fino, para acercarse al look "juguete" de la referencia.
  // Caricatura: piel bronceada de tono calido y rubio pajizo/anaranjado en
  // vez del amarillo dibujo animado. Son los dos rasgos que mas se leen a
  // distancia de juego, mucho antes que cualquier detalle de la cara.
  const skinMat = toon(0xf0b183);
  const hairMat = toon(0xf3dc93);
  const suitMat = toon(suitColor);
  const lapelMat = toon(0x16224a);
  const tieMat = toon(tieColor);
  const shoeMat = toon(0xffffff);
  const shoeAccentMat = toon(0x4caf50);
  const goldMat = toon(0xffce3d);
  const collarMat = toon(0xffffff);
  const eyeWhiteMat = toon(0xffffff);
  const pupilMat = toon(0x2a1c10);
  const mouthMat = toon(0xa33b3b);
  // Cejas rubias claras, a juego con el pelo: en marron oscuro cortaban la
  // cara en dos y era lo unico que no encajaba con el resto de la paleta.
  const browMat = toon(0xd9be7a);
  const noseMat = skinMat;

  const root = new THREE.Group();
  // El cuerpo se contruye mirando hacia +Z, pero el personaje corre hacia -Z
  // (la camara queda detras, viendo la espalda). Este grupo interno lo gira
  // 180 grados sin afectar las rotaciones que main.js aplica sobre `root`.
  const facing = new THREE.Group();
  facing.rotation.y = Math.PI;
  root.add(facing);

  function jointCap(radius, mat) {
    return new THREE.Mesh(new THREE.SphereGeometry(radius, 12, 10), mat || suitMat);
  }

  // ---- Piernas en dos segmentos (muslo + espinilla con rodilla real),
  // acortadas para un look chibi mas marcado ----
  function makeLeg(sign) {
    const hipPivot = new THREE.Group();
    hipPivot.position.set(sign * 0.15, HIP_Y, 0);
    hipPivot.add(jointCap(0.14)); // cobertor de cadera, tapa la union con el torso

    // Piernas alargadas respecto a la version anterior (muslo 0.17->0.26,
    // espinilla 0.15->0.24): las piernas cortas y rechonchas eran el segundo
    // motivo de que se leyera como un playmobil, despues de la cabeza.
    const thigh = new THREE.Mesh(new THREE.CapsuleGeometry(0.115, 0.26, 6, 10), suitMat);
    thigh.position.y = -0.19;
    withOutline(thigh);
    hipPivot.add(thigh);

    const kneePivot = new THREE.Group();
    kneePivot.position.y = -0.36;
    kneePivot.add(jointCap(0.095)); // cobertor de rodilla
    hipPivot.add(kneePivot);

    const shin = new THREE.Mesh(new THREE.CapsuleGeometry(0.088, 0.24, 6, 10), suitMat);
    shin.position.y = -0.17;
    withOutline(shin);
    kneePivot.add(shin);

    const shoe = new THREE.Mesh(new THREE.CapsuleGeometry(0.12, 0.16, 4, 10), shoeMat);
    shoe.rotation.z = Math.PI / 2;
    shoe.position.set(0, -0.35, 0.07);
    withOutline(shoe);
    kneePivot.add(shoe);
    // Puntera/detalle de color, gran forma simple en vez de cordones finos
    const toeAccent = new THREE.Mesh(new THREE.SphereGeometry(0.095, 10, 8), shoeAccentMat);
    toeAccent.scale.set(0.9, 0.7, 0.9);
    toeAccent.position.set(0, -0.37, 0.17);
    kneePivot.add(toeAccent);

    return { pivot: hipPivot, knee: kneePivot };
  }
  const leftLegRig = makeLeg(-1);
  const rightLegRig = makeLeg(1);
  const leftLeg = leftLegRig.pivot, rightLeg = rightLegRig.pivot;
  facing.add(leftLeg, rightLeg);

  // ---- Torso redondeado (capsula), compacto ----
  const hips = new THREE.Group();
  hips.position.y = HIP_Y;
  facing.add(hips);

  const TORSO_R = 0.25; // radio medio de referencia (lo usa el cinturon)

  // Torso troncoconico en vez de capsula de grosor uniforme: ancho de pecho
  // y hombros, estrecho de cintura, y aplastado en Z (mas ancho que hondo,
  // como un torso real). Un cilindro del mismo grosor de arriba abajo era
  // una de las causas principales del look playmobil -- no habia silueta de
  // chaqueta, solo un tubo.
  const CHEST_R = 0.32, WAIST_R = 0.20;
  const torso = new THREE.Mesh(new THREE.CylinderGeometry(CHEST_R, WAIST_R, 0.48, 20), suitMat);
  torso.position.y = 0.34;
  torso.scale.z = 0.8;
  hips.add(torso);

  // Remate superior del pecho, redondeado, para que el cono no acabe en un
  // canto duro justo debajo del cuello.
  const chestCap = new THREE.Mesh(new THREE.SphereGeometry(CHEST_R, 20, 12, 0, Math.PI * 2, 0, Math.PI * 0.5), suitMat);
  chestCap.position.y = 0.575;
  chestCap.scale.set(1, 0.5, 0.8);
  hips.add(chestCap);

  // Hombros reales: los brazos ya no cuelgan de una bola suelta al aire,
  // sino de una masa de hombro que continua la linea de la chaqueta.
  for (const side of [-1, 1]) {
    const shoulder = new THREE.Mesh(new THREE.SphereGeometry(0.135, 14, 12), suitMat);
    shoulder.position.set(side * 0.265, 0.545, 0);
    shoulder.scale.set(1.15, 0.95, 0.85);
    hips.add(shoulder);
  }

  // Faldon de la chaqueta: se abre un poco por debajo de la cintura, lo que
  // rompe el tubo recto y da lectura de "traje" a distancia de juego.
  // DoubleSide porque es un cilindro abierto (sin tapas): al abrirse hacia
  // fuera se ve tambien su cara interior por abajo.
  const jacketHem = new THREE.Mesh(
    new THREE.CylinderGeometry(0.225, 0.265, 0.14, 20, 1, true),
    toon(suitColor, { side: THREE.DoubleSide })
  );
  jacketHem.position.y = 0.13;
  jacketHem.scale.z = 0.82;
  hips.add(jacketHem);

  // Era CapsuleGeometry(0.26, 0.02): una capsula de RADIO 0.26, es decir casi
  // una esfera negra del ancho del torso -- se veia como una panza negra
  // enorme, no como un cinturon. Ahora es un cilindro fino de verdad, a la
  // medida de la cintura y aplastado en Z como el resto del cuerpo.
  const belt = new THREE.Mesh(new THREE.CylinderGeometry(WAIST_R + 0.015, WAIST_R + 0.015, 0.055, 20), toon(0x22242c));
  belt.position.y = 0.11;
  belt.scale.z = 0.82;
  hips.add(belt);
  const buckleBig = new THREE.Mesh(new THREE.BoxGeometry(0.055, 0.04, 0.025), goldMat);
  buckleBig.position.set(0, 0.11, 0.18);
  hips.add(buckleBig);

  // ---- Cuello corto (casi oculto, como en la referencia) ----
  const neck = new THREE.Mesh(new THREE.CylinderGeometry(0.1, 0.11, 0.08, 12), skinMat);
  neck.position.y = 0.63;
  hips.add(neck);

  // Camisa en V entre las solapas (antes solo habia solapas sobre el color
  // liso de la chaqueta, sin pecho de camisa visible).
  // Z calculados contra la superficie real del pecho, no a ojo: el torso es
  // un cono de CHEST_R=0.32 (arriba) a WAIST_R=0.20 (abajo) con escala Z 0.8,
  // asi que a la altura del pecho la cara frontal cae en z~0.23. Con los
  // valores anteriores (0.235 y 0.2, heredados del torso cilindrico fino)
  // camisa y cuello quedaban DENTRO del torso y no se veian.
  const shirt = new THREE.Mesh(new THREE.BoxGeometry(0.2, 0.3, 0.03), collarMat);
  shirt.position.set(0, 0.44, 0.252);
  hips.add(shirt);

  const collar = new THREE.Mesh(new THREE.BoxGeometry(0.27, 0.07, 0.1), collarMat);
  collar.position.set(0, 0.6, 0.25);
  hips.add(collar);

  // Solapas mas largas y giradas hacia fuera, siguiendo la V de la camisa.
  // Sus Z suben de 0.21 a 0.245 porque el pecho ahora es mas hondo (CHEST_R
  // 0.32 x escala 0.8 = 0.256) y con el valor viejo quedaban enterradas.
  for (const side of [-1, 1]) {
    const lapel = new THREE.Mesh(new THREE.BoxGeometry(0.13, 0.32, 0.025), lapelMat);
    lapel.position.set(side * 0.135, 0.42, 0.245);
    lapel.rotation.z = -side * 0.3;
    lapel.rotation.y = -side * 0.18;
    hips.add(lapel);
  }

  // Pin de bandera en la solapa izquierda: dos franjas (roja y azul) del
  // tamaño justo para leerse como una insignia y no como una mancha.
  const pinRed = new THREE.Mesh(new THREE.BoxGeometry(0.042, 0.028, 0.012), toon(0xd8322f));
  pinRed.position.set(-0.145, 0.5, 0.262);
  hips.add(pinRed);
  const pinBlue = new THREE.Mesh(new THREE.BoxGeometry(0.018, 0.028, 0.014), toon(0x2a4a9a));
  pinBlue.position.set(-0.157, 0.5, 0.264);
  hips.add(pinBlue);

  // Corbata en dos piezas: nudo + pala, en vez de una tira recta uniforme.
  const tieKnot = new THREE.Mesh(new THREE.BoxGeometry(0.075, 0.075, 0.04), tieMat);
  tieKnot.position.set(0, 0.552, 0.278);
  hips.add(tieKnot);
  // Corbata exageradamente larga, que pasa por debajo del cinturon: es el
  // otro guiño reconocible de la caricatura junto con el tupe.
  const tie = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.07, 0.52, 4), tieMat);
  tie.position.set(0, 0.28, 0.258);
  tie.rotation.y = Math.PI / 4;
  hips.add(tie);

  // Espalda de la chaqueta: antes habia aqui una mochila amarilla con correas
  // (heredada de cuando el referente era Subway Surfers). Como la camara de
  // carrera ve al personaje por detras, esa mochila era lo que mas se veia
  // durante toda la partida y tapaba el traje. Sustituida por el detalle de
  // sastreria que corresponde: costura central y abertura inferior.
  const backSeam = new THREE.Mesh(new THREE.BoxGeometry(0.022, 0.42, 0.02), lapelMat);
  backSeam.position.set(0, 0.36, -0.245);
  hips.add(backSeam);
  const backVent = new THREE.Mesh(new THREE.BoxGeometry(0.02, 0.13, 0.02), lapelMat);
  backVent.position.set(0, 0.14, -0.238);
  hips.add(backVent);

  // ---- Cabeza ----
  // Se escala el GRUPO entero (0.78) en vez de tocar el radio de cada pieza:
  // asi ojos, cejas, nariz, orejas y mechones mantienen sus proporciones y
  // posiciones relativas exactas entre si. Antes la cabeza (r=0.46) era casi
  // el doble de ancha que el torso (r=0.25) -- la causa principal del look
  // playmobil. Sigue siendo mas grande de lo natural (es un runner
  // caricaturesco, no realista), pero ya no domina la silueta.
  const headGroup = new THREE.Group();
  headGroup.position.y = 0.78;
  headGroup.scale.setScalar(0.78);
  hips.add(headGroup);

  const head = new THREE.Mesh(new THREE.SphereGeometry(0.46, 22, 18), skinMat);
  // Cara algo mas ancha que alta y con el volumen bajado hacia la mandibula,
  // en vez de una bola perfecta.
  head.scale.set(1.05, 0.98, 0.98);
  headGroup.add(head);

  // Mofletes/mandibula pesada: dos masas bajas a los lados de la boca que
  // ensanchan la parte inferior de la cara. Es lo que da el aire adulto y
  // algo hinchado de la caricatura, frente a la cara de bebe redonda.
  for (const side of [-1, 1]) {
    const jowl = new THREE.Mesh(new THREE.SphereGeometry(0.19, 12, 10), skinMat);
    jowl.scale.set(0.85, 0.78, 0.75);
    jowl.position.set(side * 0.21, -0.24, 0.29);
    headGroup.add(jowl);
  }
  // Papada suave bajo la barbilla.
  const chin = new THREE.Mesh(new THREE.SphereGeometry(0.17, 12, 10), skinMat);
  chin.scale.set(1.05, 0.62, 0.85);
  chin.position.set(0, -0.35, 0.2);
  headGroup.add(chin);

  // Antes: casquete de 0.6*PI que cubria toda la bola de la cabeza hasta las
  // cejas -- exactamente una peluca de playmobil encajada. Ahora es un
  // casquete mas corto (0.42*PI) y desplazado atras, de modo que se ve
  // frente y sienes: la cabeza se lee como una cabeza con pelo encima, no
  // como una pieza de plastico con tapa.
  const hair = new THREE.Mesh(new THREE.SphereGeometry(0.475, 20, 14, 0, Math.PI * 2, 0, Math.PI * 0.42), hairMat);
  hair.position.set(0, 0.11, -0.04);
  hair.scale.set(1.06, 1.15, 1.12);
  hair.rotation.x = -0.12;
  headGroup.add(hair);

  // Patillas cortas que bajan por delante de las orejas: rompen el borde
  // circular perfecto del casquete, que es lo que mas delata la "peluca".
  for (const side of [-1, 1]) {
    const sideburn = new THREE.Mesh(new THREE.SphereGeometry(0.1, 10, 8), hairMat);
    sideburn.scale.set(0.55, 1.25, 0.85);
    sideburn.position.set(side * 0.4, 0.1, -0.05);
    headGroup.add(sideburn);
  }
  // Nuca: tapa el hueco entre el casquete y el cuello por detras.
  const nape = new THREE.Mesh(new THREE.SphereGeometry(0.36, 14, 10), hairMat);
  nape.scale.set(1.02, 0.7, 0.72);
  nape.position.set(0, 0.02, -0.24);
  headGroup.add(nape);

  // Tupe barrido hacia delante y cruzado en diagonal, sobresaliendo por
  // encima de la frente: es el rasgo mas identificable de la caricatura, muy
  // por delante de cualquier detalle de la cara. Mas ancho y volado que el
  // mechon anterior, y girado en Y para que cruce de un lado al otro.
  const swoop = new THREE.Mesh(new THREE.SphereGeometry(0.21, 16, 12), hairMat);
  swoop.scale.set(1.75, 0.46, 1.15);
  swoop.position.set(-0.05, 0.36, 0.24);
  swoop.rotation.set(-0.14, 0.22, 0.3);
  headGroup.add(swoop);

  // Voladizo del flequillo: sobresale por delante de la frente, ese "alero"
  // caracteristico que hace que el peinado se lea de perfil.
  const swoopTip = new THREE.Mesh(new THREE.SphereGeometry(0.15, 14, 10), hairMat);
  swoopTip.scale.set(1.5, 0.38, 1.0);
  swoopTip.position.set(-0.16, 0.31, 0.33);
  swoopTip.rotation.set(-0.2, 0.35, 0.42);
  headGroup.add(swoopTip);

  // Segundo mechon, mas pequeno, para dar volumen detras del principal
  const swoop2 = new THREE.Mesh(new THREE.SphereGeometry(0.13, 12, 10), hairMat);
  swoop2.scale.set(1.35, 0.55, 1);
  swoop2.position.set(0.18, 0.38, 0.14);
  swoop2.rotation.z = -0.3;
  headGroup.add(swoop2);

  // Pose base del peinado: la animacion de carrera parte de estos valores en
  // vez de sobrescribirlos (ver updateRun).
  const SWOOP_BASE = swoop.rotation.clone();
  const SWOOP_TIP_BASE = swoopTip.rotation.clone();
  const SWOOP2_BASE = swoop2.rotation.clone();

  const earMat = skinMat;
  for (const side of [-1, 1]) {
    const ear = new THREE.Mesh(new THREE.SphereGeometry(0.068, 10, 8), earMat);
    ear.position.set(side * 0.45, -0.02, 0);
    headGroup.add(ear);
  }

  // ---- Ojos + cejas + nariz ----
  // Antifaz claro alrededor de los ojos: la marca de las gafas de sol sobre
  // la piel bronceada. Es EL detalle mas identificable de esta caricatura y
  // el que mejor funciona a tamaño pequeño, porque es una mancha de color y
  // no un rasgo fino. Va antes que los ojos para quedar por debajo.
  const paleMat = toon(0xffe0c4);
  for (const sign of [-1, 1]) {
    const patch = new THREE.Mesh(new THREE.SphereGeometry(0.135, 14, 12), paleMat);
    patch.scale.set(1.0, 0.85, 0.42);
    patch.position.set(sign * 0.17, 0.035, 0.345);
    headGroup.add(patch);
  }

  const eyeGroup = { left: new THREE.Group(), right: new THREE.Group() };
  const EYE_X = 0.17, EYE_Y = 0.03, EYE_Z = 0.4;
  for (const [side, sign] of [["left", -1], ["right", 1]]) {
    const g = eyeGroup[side];
    g.position.set(sign * EYE_X, EYE_Y, EYE_Z);
    const white = new THREE.Mesh(new THREE.SphereGeometry(0.105, 14, 12), eyeWhiteMat);
    // Ojos entornados: se achata el globo en vertical en vez de dejarlo
    // redondo y saltón, que daba una expresion de sorpresa permanente.
    white.scale.set(1, 0.68, 1);
    g.add(white);
    const pupil = new THREE.Mesh(new THREE.SphereGeometry(0.052, 10, 8), pupilMat);
    pupil.scale.set(1, 0.9, 1);
    pupil.position.set(0, 0.004, 0.086);
    g.add(pupil);
    // Parpado superior caido, del color de la piel, que corta el ojo por arriba.
    const lid = new THREE.Mesh(new THREE.SphereGeometry(0.108, 14, 10, 0, Math.PI * 2, 0, Math.PI * 0.5), skinMat);
    lid.scale.set(1.02, 0.5, 1.02);
    lid.position.y = 0.022;
    lid.rotation.x = -0.22;
    g.add(lid);
    headGroup.add(g);
  }

  const nose = new THREE.Mesh(new THREE.ConeGeometry(0.05, 0.09, 10), noseMat);
  nose.rotation.x = Math.PI / 2.3;
  nose.position.set(0, -0.05, 0.45);
  headGroup.add(nose);

  // Cejas en dos segmentos (arco sutil en vez de una caja recta plana)
  function makeBrow(sign) {
    const g = new THREE.Group();
    g.position.set(sign * 0.17, 0.16, 0.41);
    const inner = new THREE.Mesh(new THREE.BoxGeometry(0.07, 0.028, 0.03), browMat);
    inner.position.set(-sign * 0.03, 0, 0);
    inner.rotation.z = sign * 0.12;
    g.add(inner);
    const outer = new THREE.Mesh(new THREE.BoxGeometry(0.07, 0.026, 0.03), browMat);
    outer.position.set(sign * 0.032, 0.012, 0);
    outer.rotation.z = -sign * 0.22;
    g.add(outer);
    return g;
  }
  const browL = makeBrow(-1);
  const browR = makeBrow(1);
  headGroup.add(browL, browR);

  // Boca pequeña y fruncida en vez de una raja ancha: el mohin es el otro
  // gesto caracteristico. Se estrecha en X y se le da algo de volumen.
  const mouth = new THREE.Mesh(new THREE.BoxGeometry(0.13, 0.055, 0.035), mouthMat);
  mouth.position.set(0, -0.225, 0.435);
  headGroup.add(mouth);

  // ---- Brazos en dos segmentos (brazo + antebrazo con codo real), cortos ----
  function makeHand() {
    // Mano simple redondeada tipo guante, sin dedos marcados: formas
    // grandes y limpias en vez de detalle fino.
    const g = new THREE.Group();
    const palm = new THREE.Mesh(new THREE.SphereGeometry(0.1, 12, 10), skinMat);
    palm.scale.set(1, 1.05, 0.9);
    withOutline(palm);
    g.add(palm);
    return g;
  }

  function makeArm(sign) {
    // El pivote se mete DENTRO de la masa del hombro (0.265, la misma X que
    // el hombro de la chaqueta) en vez de a 0.35, que dejaba el brazo
    // colgando en el aire con una bola suelta a la vista entre torso y brazo
    // -- la union tipica de un playmobil.
    const shoulderPivot = new THREE.Group();
    shoulderPivot.position.set(sign * 0.265, 0.55, 0);

    // Brazo que adelgaza del hombro a la muñeca (antes grosor constante).
    const upperArm = new THREE.Mesh(new THREE.CylinderGeometry(0.088, 0.072, 0.29, 12), suitMat);
    upperArm.position.y = -0.145;
    shoulderPivot.add(upperArm);

    const elbowPivot = new THREE.Group();
    elbowPivot.position.y = -0.28;
    elbowPivot.add(jointCap(0.072)); // codo redondeado, continua el brazo
    shoulderPivot.add(elbowPivot);

    // Antebrazo en manga hasta media altura y luego piel (puño de camisa).
    const forearm = new THREE.Mesh(new THREE.CylinderGeometry(0.07, 0.055, 0.2, 12), suitMat);
    forearm.position.y = -0.1;
    elbowPivot.add(forearm);
    const cuff = new THREE.Mesh(new THREE.CylinderGeometry(0.057, 0.055, 0.03, 12), collarMat);
    cuff.position.y = -0.2;
    elbowPivot.add(cuff);
    const wrist = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.05, 0.06, 10), skinMat);
    wrist.position.y = -0.235;
    elbowPivot.add(wrist);

    const hand = makeHand();
    hand.position.y = -0.29; // tras el puño de camisa y la muñeca
    elbowPivot.add(hand);

    return { pivot: shoulderPivot, elbow: elbowPivot };
  }
  const leftArmRig = makeArm(-1);
  const rightArmRig = makeArm(1);
  const leftArm = leftArmRig.pivot, rightArm = rightArmRig.pivot;
  hips.add(leftArm, rightArm);

  // ---- Aura del escudo (Orden Ejecutiva), oculta por defecto ----
  const shield = new THREE.Mesh(
    new THREE.SphereGeometry(0.78, 16, 12),
    new THREE.MeshBasicMaterial({ color: 0xffce3d, transparent: true, opacity: 0.24, wireframe: false })
  );
  shield.position.y = 0.86;
  shield.visible = false;
  root.add(shield);

  // Sombra real proyectada por las piezas principales (el suelo la recibe en world.js)
  root.traverse((o) => { if (o.isMesh && o.material !== shield.material) o.castShadow = true; });

  let runPhase = 0;
  let leanTarget = 0;
  let hairLag = 0;
  const NEUTRAL_SCALE = new THREE.Vector3(1, 1, 1);

  // ---- Expresiones ----
  const EXPRESSIONS = {
    normal: { eyeScale: 1, browY: 0.16, browRotZ: 0, mouthScaleX: 1, mouthScaleY: 1, mouthY: -0.22 },
    surprised: { eyeScale: 1.3, browY: 0.21, browRotZ: 0, mouthScaleX: 0.6, mouthScaleY: 2.6, mouthY: -0.26 },
    happy: { eyeScale: 0.78, browY: 0.15, browRotZ: 0.18, mouthScaleX: 1.5, mouthScaleY: 1.4, mouthY: -0.2 },
    // Concentrado: a velocidad alta. Ojos entornados y cejas bajadas hacia
    // dentro (ceño), boca apretada.
    determined: { eyeScale: 0.82, browY: 0.115, browRotZ: -0.26, mouthScaleX: 0.85, mouthScaleY: 0.7, mouthY: -0.225 },
    // Apuro: con un obstaculo encima. A medio camino entre concentrado y
    // sorprendido, para que se note la tension sin el susto completo.
    worried: { eyeScale: 1.12, browY: 0.195, browRotZ: -0.14, mouthScaleX: 0.7, mouthScaleY: 1.7, mouthY: -0.245 },
  };
  // ---- Parpadeo periodico (independiente de la expresion: se combina con
  // la escala de ojos de la expresion actual en vez de pisarla) ----
  let currentEyeScale = 1;
  let blinkTimer = 2 + Math.random() * 3;
  let blinkElapsed = -1;
  const BLINK_DURATION = 0.14;
  let lastIdleT = 0;

  function applyEyeScale() {
    let factorY = 1;
    if (blinkElapsed >= 0) {
      const p = blinkElapsed / BLINK_DURATION;
      factorY = Math.max(0.05, p < 0.5 ? 1 - p * 2 : (p - 0.5) * 2);
    }
    eyeGroup.left.scale.set(currentEyeScale, currentEyeScale * factorY, currentEyeScale);
    eyeGroup.right.scale.set(currentEyeScale, currentEyeScale * factorY, currentEyeScale);
  }

  function updateBlink(dt) {
    if (blinkElapsed >= 0) {
      blinkElapsed += dt;
      if (blinkElapsed >= BLINK_DURATION) blinkElapsed = -1;
    } else {
      blinkTimer -= dt;
      if (blinkTimer <= 0) {
        blinkElapsed = 0;
        blinkTimer = 2.5 + Math.random() * 3;
      }
    }
    applyEyeScale();
  }

  function applyExpression(name) {
    const e = EXPRESSIONS[name] || EXPRESSIONS.normal;
    currentEyeScale = e.eyeScale;
    applyEyeScale();
    browL.position.y = e.browY; browR.position.y = e.browY;
    browL.rotation.z = e.browRotZ; browR.rotation.z = -e.browRotZ;
    mouth.scale.set(e.mouthScaleX, e.mouthScaleY, 1);
    mouth.position.y = e.mouthY;
  }
  applyExpression("normal");

  return {
    object3D: root,
    hips,

    // pose: velocidad de carrera en unidades/seg para escalar la zancada
    updateRun(dt, speedFactor) {
      runPhase += dt * 9 * speedFactor;
      const swing = Math.sin(runPhase);
      // Amplitud de zancada creciente con la velocidad: al esprintar las
      // piernas se abren mas, no solo se mueven mas rapido.
      const stride = 0.7 + Math.min(0.35, (speedFactor - 1) * 0.4);
      leftLeg.rotation.x = swing * stride;
      rightLeg.rotation.x = -swing * stride;
      // Los brazos van ligeramente adelantados de fase respecto a las piernas
      // (no en oposicion perfecta): un desfase pequeno rompe la simetria de
      // reloj que hacia que pareciera un juguete de cuerda.
      const armSwing = Math.sin(runPhase + 0.35);
      leftArm.rotation.x = -armSwing * 0.75;
      rightArm.rotation.x = armSwing * 0.75;
      // Los brazos tambien cruzan un poco hacia el pecho, como al correr de verdad.
      leftArm.rotation.z = 0.12 + Math.max(0, armSwing) * 0.18;
      rightArm.rotation.z = -0.12 - Math.max(0, -armSwing) * 0.18;
      // codos/rodillas se doblan al pasar por la parte trasera de la zancada
      leftLegRig.knee.rotation.x = Math.max(0, -swing) * 1.25;
      rightLegRig.knee.rotation.x = Math.max(0, swing) * 1.25;
      leftArmRig.elbow.rotation.x = 0.35 + Math.max(0, armSwing) * 0.55;
      rightArmRig.elbow.rotation.x = 0.35 + Math.max(0, -armSwing) * 0.55;
      // El rebote va al DOBLE de frecuencia que la zancada: cada paso empuja
      // el cuerpo hacia arriba una vez, no una vez por ciclo completo. Con
      // cos(runPhase) el personaje solo botaba cada dos pasos y se notaba
      // flotante/mecanico.
      hips.position.y = HIP_Y + Math.abs(Math.sin(runPhase)) * 0.075;
      // Contrarrotacion de hombros/caderas: el torso gira al reves que las
      // piernas. Es lo que mas separa una carrera real de una animacion de
      // muneco rigido.
      hips.rotation.y = -swing * 0.16;
      hips.rotation.x = 0.12; // ligera inclinacion hacia delante, postura de carrera
      // La cabeza compensa el giro del torso para seguir mirando al frente.
      headGroup.rotation.y = swing * 0.12;
      headGroup.rotation.x = -0.08 + Math.abs(Math.sin(runPhase)) * 0.04;
      // vuelve suavemente al escalado normal tras un salto/deslizada (squash & stretch)
      root.scale.lerp(NEUTRAL_SCALE, Math.min(1, dt * 8));
      // movimiento secundario del pelo: sigue el giro con un pequeno retraso
      hairLag += (leanTarget - hairLag) * Math.min(1, dt * 10);
      // La animacion se SUMA a la pose base del peinado en vez de escribir
      // rotaciones absolutas: con valores absolutos se perdian los angulos
      // del tupe (barrido y cruzado en diagonal) en cuanto empezaba a correr.
      const bob = Math.sin(runPhase * 2 - 0.6);
      swoop.rotation.set(SWOOP_BASE.x, SWOOP_BASE.y + hairLag * 0.6, SWOOP_BASE.z - bob * 0.09);
      swoopTip.rotation.set(SWOOP_TIP_BASE.x, SWOOP_TIP_BASE.y + hairLag * 0.75, SWOOP_TIP_BASE.z - bob * 0.13);
      swoop2.rotation.set(SWOOP2_BASE.x, SWOOP2_BASE.y + hairLag * 0.4, SWOOP2_BASE.z - bob * 0.07);
      // La corbata y la chaqueta ondean hacia atras con la velocidad.
      tie.rotation.x = -0.25 - Math.min(0.5, (speedFactor - 1) * 0.5) - Math.sin(runPhase * 2) * 0.12;
      updateBlink(dt);
    },

    setJumpPose(t) {
      // t: 0..1 progreso del salto
      const tuck = Math.sin(t * Math.PI);
      // Piernas asimetricas en el aire (una mas recogida que la otra): un
      // salto con las dos piernas exactamente iguales se lee como un muneco.
      leftLeg.rotation.x = 1.05 * tuck;
      rightLeg.rotation.x = 0.72 * tuck;
      leftArm.rotation.x = -0.5 * tuck;
      rightArm.rotation.x = -0.7 * tuck;
      leftArm.rotation.z = 0.12;
      rightArm.rotation.z = -0.12;
      leftLegRig.knee.rotation.x = tuck * 1.35;
      rightLegRig.knee.rotation.x = tuck * 0.85;
      leftArmRig.elbow.rotation.x = tuck * 0.6;
      rightArmRig.elbow.rotation.x = tuck * 0.75;
      // Se recoge al subir y estira las piernas al caer, buscando el suelo.
      hips.rotation.x = 0.3 * tuck;
      hips.rotation.y = 0;
      headGroup.rotation.y = 0;
      headGroup.rotation.x = -0.15 * tuck;
      // squash & stretch: se estira al despegar, se aplasta al aterrizar
      // (magnitud subida para que se note mas, mas "jugo" en el salto)
      const stretch = Math.max(0, 1 - t * 4);
      const squash = Math.max(0, (t - 0.75) * 4);
      const scaleY = 1 + 0.28 * stretch - 0.34 * squash;
      const scaleXZ = 1 - 0.18 * stretch + 0.26 * squash;
      root.scale.set(scaleXZ, scaleY, scaleXZ);
    },

    // Derrape de beisbol, no un ovillo: antes solo se rotaban y bajaban las
    // caderas y los brazos/piernas se quedaban en la pose de correr, asi que
    // el conjunto se leia como una bola. Ahora se posa el cuerpo entero --
    // torso muy reclinado hacia atras, una pierna estirada por delante y la
    // otra recogida debajo, brazos hacia atras -- como quien se tira al suelo
    // para pasar por debajo de algo.
    setSlidePose(active) {
      if (!active) {
        hips.rotation.x = 0;
        hips.rotation.z = 0;
        hips.position.y = HIP_Y;
        headGroup.rotation.set(0, 0, 0);
        return;
      }
      hips.rotation.x = -1.15;
      hips.rotation.y = 0;
      hips.rotation.z = 0.12; // ligero ladeo, no un derrape perfectamente plano
      hips.position.y = 0.34;
      // Pierna adelantada estirada, pierna de atras recogida.
      rightLeg.rotation.x = 0.95;
      rightLegRig.knee.rotation.x = 0.05;
      leftLeg.rotation.x = -0.35;
      leftLegRig.knee.rotation.x = 1.5;
      // Brazos hacia atras, uno rozando el suelo para equilibrarse.
      rightArm.rotation.x = 1.5;
      rightArm.rotation.z = -0.3;
      rightArmRig.elbow.rotation.x = 0.25;
      leftArm.rotation.x = 1.9;
      leftArm.rotation.z = 0.35;
      leftArmRig.elbow.rotation.x = 0.15;
      // La cabeza compensa la inclinacion del torso para seguir mirando al frente.
      headGroup.rotation.x = 0.9;
    },

    // Inclinacion al cambiar de carril / tomar curvas. Subida de 0.25 a 0.45
    // y con giro en Y ademas del ladeo: el personaje se orienta un poco hacia
    // donde va en vez de desplazarse de lado siempre mirando al frente, que
    // era otra cosa que lo hacia parecer una figura empujada sobre un rail.
    setLean(amount) {
      root.rotation.z = -amount * 0.45;
      root.rotation.y = amount * 0.3;
      leanTarget = amount;
    },

    setIdlePose(t) {
      const wave = Math.sin(t * 3);
      rightArm.rotation.z = -0.55 - wave * 0.35;
      rightArm.rotation.x = Math.sin(t * 3.4) * 0.12;
      leftArm.rotation.x = 0;
      leftArm.rotation.z = 0;
      leftLeg.rotation.x = 0;
      rightLeg.rotation.x = 0;
      leftLegRig.knee.rotation.x = 0.06;
      rightLegRig.knee.rotation.x = 0.06;
      leftArmRig.elbow.rotation.x = 0.1;
      rightArmRig.elbow.rotation.x = Math.max(0, -wave) * 0.3;
      hips.position.y = HIP_Y + Math.sin(t * 1.6) * 0.015;
      hips.rotation.x = 0;
      hips.rotation.y = Math.sin(t * 0.9) * 0.05; // peso que cambia de pie, no una estatua
      headGroup.rotation.set(0, Math.sin(t * 0.7) * 0.1, 0);
      // respiracion sutil
      const breathe = 1 + Math.sin(t * 1.6) * 0.012;
      root.scale.set(1 / breathe, breathe, 1 / breathe);
      updateBlink(Math.max(0, t - lastIdleT));
      lastIdleT = t;
    },

    setShieldActive(active) {
      shield.visible = active;
    },

    // name: "normal" | "surprised" | "happy"
    setExpression(name) {
      applyExpression(name);
    },
  };
}
