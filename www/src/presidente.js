import * as THREE from "../vendor/three.module.min.js";

// El presidente de Meshy (24/10/2026): caricatura de Donald Trump estilo Pixar
// con esqueleto y animaciones de andar y correr (Isidro eligio la malla tras
// tres pruebas). Cumple el mismo contrato que el muñeco de character.js, asi
// que main.js no tiene que saber cual de los dos esta usando.
//
// Meshy solo trae andar y correr. El salto y el deslizamiento son posturas
// encima: la carrera va a camara lenta y el cuerpo entero se encoge, se estira
// o se tumba hacia atras. El saludo de la Casa Blanca mueve el brazo derecho.

const ALTURA = 2.05;   // en el juego (el muñeco viejo media ~1.9 hasta el tupe)

export function crearPresidente(gltf) {
  const root = new THREE.Group();
  // Mira a +Z como viene de Meshy; el juego corre hacia -Z: media vuelta.
  const facing = new THREE.Group();
  facing.rotation.y = Math.PI;
  root.add(facing);
  const pose = new THREE.Group();          // inclinar, tumbar al deslizarse
  facing.add(pose);

  const modelo = gltf.scene;
  pose.add(modelo);
  let malla = null;
  modelo.traverse((o) => {
    if (o.isMesh) {
      malla = o;
      o.castShadow = true;
      o.frustumCulled = false;             // la caja de reposo no cubre la carrera
      // El material de Meshy (metal y rugosidad) necesita un entorno que
      // reflejar y aqui salia casi negro: el mismo tipo de material que el
      // resto del juego, con su textura de color y su relieve.
      const m = o.material;
      if (m.map) m.map.colorSpace = THREE.SRGBColorSpace;
      o.material = new THREE.MeshPhongMaterial({ map: m.map, normalMap: m.normalMap || null, shininess: 22, specular: 0x262626 });
      m.dispose();
    }
  });
  // A su altura. Ojo: la malla va pegada a los huesos y estos ya estan en
  // metros (la escala 0.01 del Armature se compensa con huesos en cm), asi
  // que la altura buena es la de la geometria tal cual, no la de la caja en
  // el mundo (que salia cuatro veces mas pequeña y lo dejaba gigante).
  malla.geometry.computeBoundingBox();
  const g = malla.geometry.boundingBox;
  const esc = ALTURA / Math.max(0.01, g.max.y - g.min.y);
  modelo.scale.setScalar(esc);
  modelo.position.y = -g.min.y * esc;

  const mixer = new THREE.AnimationMixer(modelo);
  const clip = (texto) => gltf.animations.find((a) => a.name.includes(texto));
  const correr = mixer.clipAction(clip("running"));
  const andar = mixer.clipAction(clip("walking"));
  correr.play();
  andar.play();
  andar.weight = 0;

  const huesos = {};
  modelo.traverse((o) => { if (o.isBone) huesos[o.name] = o; });

  // ---- La tienda (27/10/2026): sombreros y trajes ----
  // Donde va un sombrero: en lo alto de la cabeza, calculado en reposo (antes
  // de que se mueva nada) y en el espacio del hueso de la cabeza, para que se
  // mueva con ella al correr. El sombrero viene mirando a +z y con la base en
  // y = 0; aqui se gira para que mire adonde mira el presidente.
  let marcoCabeza = null, sombreroPuesto = null;
  if (huesos.Head) {
    root.updateMatrixWorld(true);
    const h = huesos.Head;
    const qInv = h.getWorldQuaternion(new THREE.Quaternion()).invert();
    const s = h.getWorldScale(new THREE.Vector3()).x;
    const arriba = new THREE.Vector3(0, 1, 0).applyQuaternion(qInv).normalize();
    const delante0 = new THREE.Vector3(0, 0, -1).applyQuaternion(qInv);
    const lado = new THREE.Vector3().crossVectors(arriba, delante0).normalize();
    const delante = new THREE.Vector3().crossVectors(lado, arriba).normalize();
    const quat = new THREE.Quaternion().setFromRotationMatrix(new THREE.Matrix4().makeBasis(lado, arriba, delante));
    const punta = huesos.head_end ? huesos.head_end.position.clone() : new THREE.Vector3(0, 0.22 / s, 0);
    marcoCabeza = { punta, quat, escala: 1 / s };
  }
  // El traje se tiñe cambiando, en la textura, los pixeles azul marino del
  // traje por el color nuevo (conservando sus luces y sombras).
  const mapaOriginal = malla.material.map;
  const texturasTraje = {};
  let pixelesTraje = null;
  function texturaTraje(color) {
    if (texturasTraje[color]) return texturasTraje[color];
    const im = mapaOriginal.image;
    const c = document.createElement("canvas");
    c.width = im.width; c.height = im.height;
    const x = c.getContext("2d");
    x.drawImage(im, 0, 0);
    const datos = x.getImageData(0, 0, c.width, c.height);
    const d = datos.data;
    if (!pixelesTraje) {
      // Azul marino: el azul manda, poco rojo, y oscuro.
      pixelesTraje = [];
      for (let i = 0; i < d.length; i += 4) {
        const r = d[i], g = d[i + 1], b = d[i + 2];
        const max = Math.max(r, g, b), min = Math.min(r, g, b);
        if (b === max && b - r > 18 && b - g > 6 && max < 170 && (max - min) / (max || 1) > 0.18) pixelesTraje.push(i);
      }
    }
    const obj = new THREE.Color(color);
    const or = obj.r * 255, og = obj.g * 255, ob = obj.b * 255;
    const claro = (or + og + ob) / 3 > 150;
    for (const i of pixelesTraje) {
      const l = (d[i] * 0.3 + d[i + 1] * 0.5 + d[i + 2] * 0.2) / 70;   // luz de ese punto del traje (≈1 de media)
      const k = claro ? 0.55 + 0.45 * Math.min(1.6, l) : Math.min(1.6, 0.35 + 0.85 * l);
      d[i] = Math.min(255, or * k); d[i + 1] = Math.min(255, og * k); d[i + 2] = Math.min(255, ob * k);
    }
    x.putImageData(datos, 0, 0);
    const tex = new THREE.CanvasTexture(c);
    tex.flipY = mapaOriginal.flipY;
    tex.colorSpace = mapaOriginal.colorSpace;
    tex.wrapS = mapaOriginal.wrapS; tex.wrapT = mapaOriginal.wrapT;
    tex.anisotropy = 4;
    texturasTraje[color] = tex;
    return tex;
  }

  // Escudo (Orden Ejecutiva)
  const shield = new THREE.Mesh(
    new THREE.SphereGeometry(0.95, 16, 12),
    new THREE.MeshBasicMaterial({ color: 0xffce3d, transparent: true, opacity: 0.24 })
  );
  shield.position.y = 1.0;
  shield.visible = false;
  root.add(shield);

  let mega = 1;
  const NEUTRAL = new THREE.Vector3(1, 1, 1);
  let modoAndar = 0;                      // 0 corre, 1 anda (mezcla suave)
  let base = null;                        // postura de partida del saludo
  const q = new THREE.Quaternion();
  const EJE_Z = new THREE.Vector3(0, 0, 1);

  // Apunta un hueso (de el a su hijo) hacia una direccion del mundo, sin
  // depender de como vengan orientados los ejes de cada hueso en Meshy.
  // k: cuanto se acerca en este fotograma (para entrar en la postura suave).
  const _a = new THREE.Vector3(), _b = new THREE.Vector3(), _d = new THREE.Vector3();
  const _qd = new THREE.Quaternion(), _qw = new THREE.Quaternion(), _qp = new THREE.Quaternion();
  function apuntar(nombre, hijo, x, y, z, k) {
    const h = huesos[nombre], c = huesos[hijo];
    if (!h || !c || !h.parent) return;
    h.getWorldPosition(_a);
    c.getWorldPosition(_b);
    _b.sub(_a).normalize();
    _d.set(x, y, z).normalize();
    _qd.setFromUnitVectors(_b, _d);
    h.getWorldQuaternion(_qw);
    _qd.multiply(_qw);
    h.parent.getWorldQuaternion(_qp).invert();
    _qp.multiply(_qd);
    h.quaternion.slerp(_qp, k);
    h.updateMatrixWorld(true);
  }
  let deslizando = 0;
  const ATRAS = 0.45;                  // adelanta la postura: la cadera, sobre su sitio

  function mezclar(dt, objetivoAndar) {
    modoAndar += (objetivoAndar - modoAndar) * Math.min(1, dt * 5);
    andar.weight = modoAndar;
    correr.weight = 1 - modoAndar;
  }

  return {
    object3D: root,
    hips: pose,

    updateRun(dt, speedFactor) {
      base = null;
      // Por debajo de media velocidad anda (la escena final); si no, corre.
      const anda = speedFactor < 0.6 ? 1 : 0;
      mezclar(dt, anda);
      correr.timeScale = 0.75 + 0.45 * Math.max(0, speedFactor - 1) + 0.25;
      andar.timeScale = 1.1;
      pose.rotation.set(0, 0, 0);
      pose.position.set(0, 0, 0);   // (27/10: tambien z: tras deslizarse se quedaba medio metro atras)
      root.scale.lerp(NEUTRAL, Math.min(1, dt * 8));
      mixer.update(dt);
    },

    setJumpPose(t) {
      base = null;
      // En el aire: la carrera casi se para y el cuerpo se estira al despegar
      // y se aplasta al caer, como antes.
      mezclar(1 / 60, 0);
      correr.timeScale = 0.15;
      mixer.update(1 / 60);
      const tuck = Math.sin(t * Math.PI);
      pose.rotation.set(-0.25 * tuck, 0, 0);
      const stretch = Math.max(0, 1 - t * 4);
      const squash = Math.max(0, (t - 0.75) * 4);
      const sy = 1 + 0.18 * stretch - 0.22 * squash;
      const sxz = 1 - 0.1 * stretch + 0.16 * squash;
      root.scale.set(sxz * mega, sy * mega, sxz * mega);
    },

    setSlidePose(active) {
      if (!active) { deslizando = 0; pose.rotation.set(0, 0, 0); pose.position.y = 0; return; }
      // 26/10: deslizarse como en el beisbol (a Isidro el tablon tumbado le
      // parecia raro). Cadera casi en el suelo y cuerpo echado atras, pierna
      // derecha estirada por delante, la izquierda doblada por debajo y los
      // brazos arriba. Entra en unos fotogramas, no de golpe.
      deslizando++;
      const k = deslizando === 1 ? 0.5 : 0.45;
      const e = Math.min(1, deslizando / 5);
      base = null;
      mezclar(1, 0);
      correr.timeScale = 0;
      mixer.update(0);
      // (Negativo = hacia atras; la cadera se devuelve a su sitio con z.)
      pose.rotation.set(-0.7 * e, 0, 0);
      pose.position.set(0, -0.35 * e, ATRAS * e);
      root.scale.set(mega, mega, mega);
      root.updateMatrixWorld(true);
      // Direcciones en el mundo: se corre hacia -Z y la derecha es +X.
      apuntar("RightUpLeg", "RightLeg", 0.1, -0.22, -1, k);
      apuntar("RightLeg", "RightFoot", 0.1, -0.18, -1, k);
      apuntar("LeftUpLeg", "LeftLeg", -0.2, -0.3, -1, k);
      apuntar("LeftLeg", "LeftFoot", 0.75, -0.3, -0.15, k);
      apuntar("RightArm", "RightForeArm", 0.55, 0.75, 0.3, k);
      apuntar("RightForeArm", "RightHand", 0.25, 1, 0.1, k);
      apuntar("LeftArm", "LeftForeArm", -0.55, 0.75, 0.3, k);
      apuntar("LeftForeArm", "LeftHand", -0.25, 1, 0.1, k);
      apuntar("Head", "head_end", 0, 1, -0.6, k);
    },

    setLean(amount) {
      root.rotation.z = -amount * 0.35;
      root.rotation.y = amount * 0.25;
    },

    // Quieto (menu) y saludando (Casa Blanca): anda a camara lenta casi parado
    // y levanta el brazo derecho moviendo la mano.
    setIdlePose(t) {
      const brazo = huesos.RightArm, ante = huesos.RightForeArm;
      // La animacion parada no vuelve a escribir los huesos (el mezclador solo
      // escribe si el valor cambia), asi que el giro del brazo se iba sumando
      // y el brazo daba vueltas. Se guarda la postura de partida una vez y se
      // gira siempre desde ella.
      if (!base) {
        modoAndar = 1; andar.weight = 1; correr.weight = 0;
        andar.timeScale = 0;
        andar.time = 0.45;
        mixer.update(0);
        base = { brazo: brazo ? brazo.quaternion.clone() : null, ante: ante ? ante.quaternion.clone() : null };
      }
      pose.rotation.set(0, 0, 0);
      pose.position.set(0, 0, 0);   // (27/10: tambien z: tras deslizarse se quedaba medio metro atras)
      if (brazo) brazo.quaternion.copy(base.brazo).multiply(q.setFromAxisAngle(EJE_Z, -2.5 + Math.sin(t * 6) * 0.08));
      if (ante) ante.quaternion.copy(base.ante).multiply(q.setFromAxisAngle(EJE_Z, -0.9 + Math.sin(t * 7) * 0.5));
      const breathe = 1 + Math.sin(t * 1.6) * 0.012;
      root.scale.set(mega / breathe, mega * breathe, mega / breathe);
    },

    // 27/10: al chocar se cae de espaldas, con los brazos y las piernas al
    // aire (antes se quedaba congelado en la postura de correr). `t`: segundos
    // desde el choque.
    setCaida(t) {
      base = null;
      mezclar(1, 0);
      correr.timeScale = 0;
      mixer.update(0);
      const k = Math.min(1, t / 0.38);
      const e = k * k * (3 - 2 * k);
      const bote = t < 0.38 ? Math.sin(k * Math.PI) * 0.45 : Math.max(0, Math.sin(((t - 0.38) / 0.22) * Math.PI)) * 0.08 * (t < 0.6 ? 1 : 0);
      pose.rotation.set(-1.32 * e, 0, Math.sin(t * 9) * 0.04 * (1 - e));
      pose.position.set(0, -0.12 * e + bote, 0.75 * e);
      root.scale.set(mega, mega, mega);
      root.updateMatrixWorld(true);
      const kk = Math.min(1, 0.25 + t);
      apuntar("RightArm", "RightForeArm", 0.95, 0.35, 0.25, kk);
      apuntar("RightForeArm", "RightHand", 0.6, 0.8, 0.1, kk);
      apuntar("LeftArm", "LeftForeArm", -0.95, 0.35, 0.25, kk);
      apuntar("LeftForeArm", "LeftHand", -0.6, 0.8, 0.1, kk);
      apuntar("RightUpLeg", "RightLeg", 0.2, 0.75, -1, kk);
      apuntar("RightLeg", "RightFoot", 0.15, 0.9, -0.6, kk);
      apuntar("LeftUpLeg", "LeftLeg", -0.2, 0.45, -1, kk);
      apuntar("LeftLeg", "LeftFoot", -0.15, 0.7, -0.8, kk);
    },

    ponerSombrero(obj) {
      if (sombreroPuesto && sombreroPuesto.parent) sombreroPuesto.parent.remove(sombreroPuesto);
      sombreroPuesto = null;
      if (!obj || !marcoCabeza) return;
      const pivote = new THREE.Group();
      pivote.position.copy(marcoCabeza.punta).multiplyScalar(0.74);
      pivote.quaternion.copy(marcoCabeza.quat);
      pivote.scale.setScalar(marcoCabeza.escala * 1.4);   // la cabeza de caricatura es grande
      pivote.add(obj);
      huesos.Head.add(pivote);
      sombreroPuesto = pivote;
    },
    teñirTraje(color) {
      if (!mapaOriginal || !mapaOriginal.image) return;
      malla.material.map = color === null || color === undefined ? mapaOriginal : texturaTraje(color);
      malla.material.needsUpdate = true;
    },

    setShieldActive(active) { shield.visible = active; },
    setExpression() { /* la cara de Meshy no tiene gestos */ },
    setMega(k) {
      mega = k;
      NEUTRAL.setScalar(k);
      if (k === 1) root.scale.set(1, 1, 1);
    },
  };
}
