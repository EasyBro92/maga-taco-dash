# MAGA Taco Dash — Decisiones de diseño y hoja de ruta

Registro de las decisiones tomadas el 2026-08-09 en una revisión de 50+ preguntas sobre diseño, rendimiento, estabilidad, jugabilidad y distribución. Objetivo confirmado: **publicar en Google Play y Apple App Store**, no solo como web/PWA.

## Contexto clave
- Empaquetado elegido: **Capacitor** para Android e iOS (un solo código web, funciona offline, acceso a APIs nativas).
- Contenido político (MAGA, "Covfefe Boost", "Orden Ejecutiva", tupé rubio): se **mantiene tal cual**, asumiendo el riesgo de rechazo/revisión en las tiendas (decisión consciente, no accidental).
- Monetización: **IAP + anuncios**, combinados.
- Dispositivo objetivo mínimo: **gama media/alta Android + iPhone reciente** (no gama muy baja).

## Decisiones por área

### Arte y diseño visual
- Personaje: acercarlo más a una referencia real (menos genérico de lo que es hoy).
- Seguir con primitivas geométricas (no modelos importados tipo Mixamo), pero mejorarlas.
- Añadir sombras reales (shadow mapping), reemplazando el blob 2D actual.
- Añadir más profundidad visual (materiales PBR / ambient occlusion) en vez del look flat actual.
- Añadir animación de tropiezo/caída antes de la pantalla de game over.
- Iterar el diseño del taco (concha, relleno, proporciones).
- Añadir más tipos de obstáculos (hoy solo hay 3: valla, pancarta, atril+guardaespaldas).
- Variar la escenografía de fondo según la distancia recorrida (hoy se repite siempre igual).
- Añadir partículas (polvo al correr/deslizar, impacto al chocar).
- Paleta de color actual (rojo/azul/dorado) es placeholder, abierta a cambio.

### Rendimiento
- Implementar pooling/reutilización de geometrías y materiales para obstáculos, tacos y power-ups (hoy se crean nuevos en cada spawn, a diferencia de la decoración de fondo que ya usa pool).
- Centralizar todos los materiales compartidos (hoy algunos se recrean por instancia).
- Añadir un selector de calidad gráfica manual en Ajustes (no detección automática).
- Borrar `vendor/three.module.js` (copia sin minificar de 1.27MB, no se usa) y añadir pantalla/indicador de carga.
- Culling/LOD: no es prioridad, el fog actual es suficiente por ahora.
- **Pendiente de verificar**: aún no se ha probado en un móvil real de gama baja/media — hacerlo antes de avanzar mucho más en optimización.

### Estabilidad
- Añadir mensaje de fallback claro si WebGL no está disponible.
- Añadir debounce a `resize()` (preventivo).
- Manejar pérdida de contexto WebGL (`webglcontextlost`).
- Añadir reporte de errores/crash reporting (tipo Sentry) **antes de publicar** en tiendas.
- El juego debe soportar **landscape además de portrait** (hoy el manifest fuerza portrait sin lock real).
- El runner principal debe funcionar 100% offline; si el ranking mundial no carga por falta de conexión, falla en silencio (sin mensaje de error).
- Backup de progreso: no se prioriza export/import manual — se prefiere cuenta/nube más adelante junto con el backend del ranking.
- **Pendiente de verificar**: desbloqueo de audio (`unlockAudio`) en iPhone/Safari real, no probado aún.

### Empaquetado y distribución
- Capacitor para Android e iOS (decisión ya tomada, ver arriba).
- Generar los iconos PNG en todos los tamaños que exigen las tiendas (incluye 1024×1024 sin transparencia para App Store) — hoy solo hay un SVG.

### Jugabilidad y balance
- Ritmo de aceleración de velocidad (BASE_SPEED→MAX_SPEED): sin veredicto aún, falta más playtesting antes de tocarlo.
- La dificultad/mezcla de obstáculos debe escalar con la distancia recorrida (hoy es probabilidad fija todo el tiempo).
- Aumentar la frecuencia de power-ups (hoy 8% por fila con obstáculos, se siente poco).
- Ampliar la ventana de streak (hoy 2.2s sin coger taco resetea el multiplicador — se siente muy corta).
- Explorar variar el número/ancho de carriles en el futuro (hoy fijo en 3).
- Añadir un "momento pico" (efectos visuales/sonido/cámara) al llegar al multiplicador x5.
- Añadir sistema de misiones diarias para retención (importante de cara a tiendas).
- Prioridad de lanzamiento: **pulir el runner base primero**, tienda y ranking después.

### Progresión, tienda y economía (para después del runner base)
- Cosméticos a vender primero: trajes/colores de traje, personajes alternativos completos, y skins temáticas para taco/power-ups.
- Precios balanceados: deben requerir varios días de juego para desbloquear (no inmediato, no inalcanzable).
- Ranking mundial: usar un servicio gestionado (Firebase/Supabase) en vez de backend propio.
- Monetización: IAP (tacos/cosméticos) + anuncios, combinados.

### Audio
- Modelo híbrido: mantener los SFX cortos sintetizados (funcionan bien), pero reemplazar la música de fondo por una pista grabada.
- La música debe responder a la intensidad del juego (más intensa con más velocidad/streak).
- Añadir voz grabada para las frases del personaje ("¡Tremendo!", etc.), hoy solo texto.

### Controles y UX
- Añadir indicador visual en tiempo real mientras se hace swipe (hoy solo se detecta al soltar).
- Añadir soporte de gamepad además de touch/teclado.
- Añadir botones on-screen visibles, además del swipe por gestos.
- Añadir tutorial breve la primera vez que se juega (hoy no hay onboarding).
- **Pendiente de verificar**: legibilidad del HUD bajo luz solar directa en móvil, no probado aún.

## Dirección de arte visual (ronda 2 — "más como Minion Rush", 2026-08-09)

Tras ver el juego funcionando, se hizo una segunda ronda de 15 preguntas específicamente sobre estilo visual, usando Minion Rush como referencia. Estas decisiones **refinan** (no contradicen) las de arte de la ronda 1: en vez de "más profundidad visual" genérico, ahora hay una dirección concreta.

- **Nivel de estilo**: cartoon **moderado** — no full chibi, pero tampoco solo pulir lo actual.
- **Shading**: toon/cel-shading (bandas de luz marcadas, look "gamey"), con **contorno negro** alrededor de personajes/objetos.
- **Proporciones del personaje**: exagerar un poco (cabeza algo más grande, formas más redondeadas) — un paso intermedio, no Minion Rush completo. Sigue debiendo acercarse a la referencia real decidida en la ronda 1, pero renderizada en este estilo.
- **Cara**: añadir ojos (hoy no tiene) + expresiones reactivas (sorpresa al chocar, alegría al recoger tacos).
- **Paleta**: subir la saturación general (personaje, mundo y UI) — más "golosina", menos tonos apagados.
- **Animación**: squash & stretch (estirarse al saltar, aplastarse al aterrizar/girar) en vez del balanceo lineal actual.
- **Cámara**: dinámica y reactiva — zoom/FOV punch en boost, temblor al chocar, inclinación en giros.
- **Efectos de velocidad**: líneas de velocidad + polvo bajo los pies al correr rápido.
- **Tacos**: brillo pulsante + rebote en el sitio + chispas doradas al recogerlos (no solo el giro actual).
- **Fondo**: público y banderas con animación propia (saludar/saltar, banderas ondeando), no solo estáticos moviéndose por el scroll.
- **Iluminación**: tipo "día soleado" brillante y contrastada, en vez de la neutra actual.
- **HUD**: más jugoso — contadores que rebotan/laten al subir, badges más grandes y redondeados.
- **Variedad de mundos**: apuntar a **4 o más** ambientes/temas distintos según la distancia (más ambicioso que el "2-3 para empezar" que se ofrecía como opción segura — foco tras el pulido base del runner).
- **Referencia**: mezcla de varios runners populares (Subway Surfers, Temple Run, Minion Rush), no un clon literal de un solo juego — también reduce el riesgo de parecerse demasiado a una IP ajena.

## Roadmap priorizado

**Fase 0 — Infraestructura y base técnica (antes de seguir añadiendo features)**

Estado: **hecho 1–9, pendiente 10** (2026-08-09). Detalle de lo completado más abajo en "Estado del proyecto".

1. ~~Configurar Capacitor para Android e iOS.~~ ✅
2. ~~Generar set completo de iconos PNG para ambas tiendas.~~ ✅
3. ~~Soporte landscape + portrait.~~ ✅ (queda pendiente afinar visualmente la cámara en landscape cuando se pueda probar en pantalla real, ver nota abajo)
4. ~~Pooling de geometrías/materiales para obstáculos, tacos y power-ups.~~ ✅
5. ~~Centralizar materiales compartidos.~~ ✅
6. ~~Borrar `three.module.js` sin usar + pantalla de carga.~~ ✅
7. ~~Selector de calidad gráfica en Ajustes.~~ ✅
8. ~~Fallback de WebGL no soportado + manejo de `webglcontextlost` + debounce de resize.~~ ✅
9. ~~Integrar reporte de errores (crash reporting).~~ ✅ (scaffold local; falta conectar un DSN real de Sentry u otro servicio cuando tengas cuenta)
10. **Pendiente — requiere tu máquina/dispositivos**: probar en Android real de gama media y en iPhone real (rendimiento, desbloqueo de audio en Safari/iOS, legibilidad de HUD al sol).

### Estado del proyecto (para retomar tras perder contexto otra vez)

- **Estructura nueva**: todo el código web (antes suelto en la raíz) ahora vive en `maga-taco-dash/www/` — es el `webDir` de Capacitor. `serve.js` ya apunta ahí, no hace falta tocar nada para seguir probando local con `npm start` o el toggle de PowerShell.
- **Capacitor**: `capacitor.config.json` en la raíz del proyecto, `appId` = `com.magatacodash.app`. Carpetas `android/` e `ios/` ya generadas con `npx cap add`.
  - **Android**: se puede compilar en Windows, pero hace falta instalar Android Studio / JDK / Android SDK en esta máquina primero (no estaban instalados al hacer este trabajo). Con eso listo: abrir `android/` en Android Studio o `npx cap open android`.
  - **iOS**: el proyecto Xcode ya está generado (`ios/App`), pero **compilarlo requiere una Mac con Xcode** — Windows no puede. Cuando tengas acceso a una Mac: `npx cap open ios` (o copiar la carpeta del proyecto a la Mac primero).
  - Cada vez que cambies algo dentro de `www/`, correr `npm run cap:sync` (alias de `cap copy`) para que Android/iOS reciban los cambios antes de compilar.
- **Iconos**: generados con `@capacitor/assets` a partir de `resources/icon.png` (1024×1024, rasterizado del SVG original). Si cambias el diseño del icono, reemplaza `resources/icon.png` y corre `npm run icons`.
- **Reporte de errores**: `www/src/errors.js` captura errores no manejados y los guarda en `localStorage` (clave `tacoDashErrorLog_v1`). `setRemoteReporter()` está listo para conectar Sentry u otro servicio en cuanto exista una cuenta — hoy no envía nada a ningún servidor.
- **Calidad gráfica**: nuevo ajuste en el menú de Ajustes (Baja/Media/Alta). Cambia `antialias` y el tope de `pixelRatio`; como `antialias` solo puede fijarse al crear el renderer, cambiar la opción recarga la página.
- **Pooling**: `world.js` ya recicla los meshes de obstáculos, tacos y power-ups en vez de crear/destruir geometría en cada spawn (antes era la fuente principal de basura para el recolector de memoria). Verificado con una simulación de 5000 frames + resets en Node sin errores.
- **Sin verificar visualmente todavía**: no se pudo tomar una captura de pantalla real del juego funcionando en esta sesión (el panel del navegador no estaba renderizando), así que el aspecto visual de landscape y de la pantalla de carga están implementados pero no vistos en vivo — conviene revisarlos jugando manualmente.

### Pase visual "más Minion Rush" — implementado (2026-08-09)

Se implementó todo el punto 16 de la lista de abajo. Resumen técnico de qué se tocó:

- **`www/src/toon.js`** (nuevo): `MeshToonMaterial` con gradiente de 4 bandas compartido + `withOutline()` (técnica "inverted hull": duplicado ligeramente más grande, `BackSide`, negro) para el borde tipo cómic.
- **`www/src/pool.js`** (nuevo): el pool genérico se extrajo de `world.js` para poder reusarlo también en `main.js` (polvo).
- **`character.js`**: reescrito con `toon()` + contorno, cabeza más grande (0.33→0.4 de radio), brazos/piernas pasados de cajas a `CapsuleGeometry` (más redondeados), colores saturados, ojos nuevos (blanco+pupila) con sistema de expresiones `setExpression("normal"|"surprised"|"happy")`, y squash & stretch (estiramiento al saltar, aplastamiento al aterrizar/deslizar, respiración sutil en idle) vía `root.scale`.
- **`world.js`**: todos los materiales pasados a `toon()`, contorno en las piezas grandes de obstáculos/taco/power-ups, paleta saturada, tacos con brillo pulsante + rebote en sitio + chispas doradas al recogerse (pool propio), público/banderas de fondo con animación propia (banderas ondean, público bota sutilmente) via `userData.kind`.
- **`main.js`**: iluminación más brillante/cálida y contrastada; cámara dinámica (FOV punch en boost, temblor en choque/game over, inclinación en cambios de carril); overlay CSS de líneas de velocidad (`#speedLines`) reactivo a la velocidad/boost; sistema de polvo bajo los pies al correr rápido; HUD con "pulso" al subir el contador de tacos + badges más grandes.
- Se conectó `character.setExpression()`: sorpresa al chocar (con o sin escudo), alegría al subir el multiplicador de racha.

**Verificado**: sintaxis de los 3 archivos grandes + ejecución real de `character.js`/`world.js` bajo Node (construcción + miles de frames simulados sin excepciones), y carga real en el navegador (sin errores de consola, sin entradas en el log de errores tras ejecutar todo el módulo con un contexto WebGL real — `MeshToonMaterial`/`DataTexture`/`CapsuleGeometry` sí llegaron a compilar shaders de verdad).

**No verificado — el panel del navegador no pudo componer frames en esta sesión, así que ningún resultado visual (colores, proporciones, si el contorno se ve bien, si el squash & stretch se siente bien, balance de las líneas de velocidad/polvo/temblor de cámara) fue visto en vivo.** Todo esto quedó implementado "a ciegas" siguiendo las 15 decisiones de la ronda 2 — es el primer punto a revisar jugando en un navegador real antes de dar por buena la dirección de arte.

### Ronda de ajustes tras el primer playtest real (2026-08-09)

El usuario probó el juego y dio feedback directo. Cambios aplicados:

- **Cámara mucho menos exagerada**: FOV punch de boost bajó de +8° a +2.5°, temblor de choque bajó de 0.18/0.28 a 0.06/0.1, inclinación en giros bajó de ×3.5 a ×1.1 con un tope máximo de ±0.05 rad, y todas las interpolaciones se hicieron más lentas/suaves.
- **Escenografía lateral densificada**: clusters de decoración cada 8 unidades en vez de 12, 4 personas por lado en vez de 3, y un graderío nuevo (`makeBleacher`, con público sentado) que aparece con 60% de probabilidad junto a cada cluster. Los backdrops (paneles rojo/azul) pasaron de cada 34 a cada 22 unidades.
- **Nuevo obstáculo "flash"**: fotógrafo con trípode + cámara + una bola de luz brillante pulsante (mismo lenguaje visual de brillo que el taco) que se salta igual que los obstáculos "low". Sustituye parte de la mezcla anterior — la probabilidad de "full" bajó de 25% a 20%, "low" de 40% a 35%, y "flash" entra con 15%.
- **Cielo degradado** (domo con vertex colors, horizonte claro → cenit azul intenso) en vez de color plano, y **destello de sol** (sprite radial aditivo generado por canvas) — ambos anclados directamente a la escena, no al grupo que hace scroll, para que nunca se queden atrás.
- **Tone mapping ACES + color space sRGB** en el renderer — colores más ricos y contrastados sin tocar cada material a mano.
- **Popup flotante "+N"** junto al contador de tacos del HUD cada vez que se recoge uno o varios.

Verificado igual que antes: sintaxis + stress test de Node en `world.js` (incluye el nuevo obstáculo, cielo, decoración densificada) sin excepciones, y carga real en navegador sin errores de consola ni entradas nuevas en el log de errores. **Sigue sin verse en vivo** — el panel del navegador no compuso frames tampoco en esta ronda.

### Segunda ronda de feedback tras jugarlo (2026-08-09)

- **Arreglado el "bug de la bola" al deslizarse**: el squash&stretch que se añadía en `setSlidePose` (escalaba todo el cuerpo 1.1×0.8×1.1) se quitó por completo — ahora el deslizamiento es solo la rotación de agachado que ya funcionaba antes de este pase visual.
- **El obstáculo "flash" (fotógrafo+trípode) se reemplazó por un proyectil real**: ahora es una bola de luz con estela que viaja hacia el jugador en línea recta por un carril fijo, a una velocidad de cierre lenta y constante (`FLARE_CLOSING_SPEED`, además del scroll normal), spawneando por temporizador (cada 5-9s) en vez de como parte de las filas de obstáculos. Solo se esquiva cambiando de carril (saltar/deslizar no ayuda) — variedad mecánica nueva, no solo visual. **Nota de contenido**: el usuario pidió literalmente "una bala" — decidí mantenerlo como un flash de cámara volador en vez de una bala/arma, porque el personaje ya es una caricatura reconocible de una figura política real y no me pareció apropiado mostrar disparos de arma dirigidos a esa figura. Si el usuario prefiere una estética distinta para este proyectil (que no sea ni bala ni flash), se puede ajustar fácilmente ya que la mecánica está separada del aspecto visual (`buildFlare()` en `world.js`).
- **Curvas suaves añadidas**: todo el grupo del mundo (pista, obstáculos, decoración) se desplaza lateralmente siguiendo una onda lenta (`Math.sin`) en función de la distancia recorrida — periodo de ~130 unidades, amplitud ~2.1. El personaje, la sombra y la cámara reciben el mismo offset cada frame, así que el carril relativo del jugador y toda la lógica de colisiones quedan exactamente igual (siguen siendo cálculos en espacio local); solo cambia la posición visual absoluta de todo el conjunto.
- **Skyline de ciudad estadounidense**: nuevos edificios low-poly (con ventanas y, a veces, un tanque de agua en el techo — típico de skyline de EEUU) en clusters reciclados más alejados que los paneles rojo/azul existentes, a ambos lados de la pista.

Verificado: stress test de Node (incluye ahora curvas + skyline + flares) sin excepciones, prueba dedicada del ciclo de vida completo de los flares (aparición → movimiento → impacto/despawn) corriendo en tiempo real sin errores, sintaxis de main.js, y carga real en navegador sin errores de consola ni entradas en el log de errores.

### Tercera ronda de feedback (2026-08-09)

- **Bug real encontrado en el skyline**: el suelo solo medía 14 unidades de ancho pero los edificios se colocaban a 13-20 — quedaba un hueco vacío (fondo del cielo asomando) entre la decoración cercana y los edificios, que es justo lo que se veía como "espacios blancos". Se ensanchó el suelo a 60 unidades para cubrir toda la zona.
- **Ventanas de los edificios corregido**: estaban puestas en las caras frontal/trasera (eje Z) de cada edificio, pero los edificios están alineados a lo largo de Z a los lados de la pista — esas caras casi nunca las ve el jugador. Se movieron a la cara que mira hacia la pista (eje X), con la rotación del edificio ajustada según el lado, así que ahora sí se ven.
- **Skyline más denso pero moderado**: dos hileras (cerca/lejos) por lado en vez de una, con menos espaciado entre edificios — más denso que antes pero sin disparar el número de meshes (se quitó el contorno de los edificios y las ventanas ahora solo están en una cara, ambos cambios pensados para compensar el coste de la mayor densidad).
- **Cámara reducida de nuevo**: FOV punch de boost bajó de +2.5° a +1.2°, temblor de choque de 0.06/0.1 a 0.035/0.055, inclinación en giros de ×1.1 a ×0.6 con tope más bajo (±0.03 rad) — segunda pasada de reducción tras el primer ajuste.

Verificado: stress test de Node sin excepciones, sintaxis de main.js, carga real en navegador sin errores de consola ni entradas en el log de errores.

### Cuarta ronda: 20 preguntas + rediseño grande (2026-08-09)

Se eliminó primero la "bola que da vueltas" (era el proyectil "flare" añadido en la ronda anterior — mecánica completa quitada de `world.js` y `main.js`, no solo el aspecto visual). Confirmado por 20 preguntas: la "lentitud" reportada era de **ritmo**, no de rendimiento (el juego va fluido incluso en móvil real probado por el usuario) — eso dio luz verde para seguir sumando contenido visual sin miedo a romper el framerate.

Cambios implementados:

- **Ritmo**: `BASE_SPEED` subió de 7.2 a 9.5 (y `MAX_SPEED` de 15.5 a 16.5 para mantener margen de aceleración).
- **Personaje reconstruido a fondo** (`character.js`), con Subway Surfers como referencia más cercana:
  - Brazos y piernas ahora en **dos segmentos** (brazo+antebrazo con codo, muslo+espinilla con rodilla) con rotación propia en la animación de correr/saltar — antes eran una sola pieza rígida.
  - **Cobertores de hombro/cadera/codo/rodilla** (esferas del color del traje en cada pivote) que tapan la unión sin importar el ángulo — esto es lo que arregla el "las articulaciones traspasan el cuerpo".
  - Cuello nuevo, manos con dedos marcados (antes esfera lisa), torso pasado de caja a cápsula (redondeado), nariz nueva, botones + pañuelo de bolsillo, pelo rediseñado por completo (forma tipo gota en vez de caja para el mechón barrido), más segmentos en toda la geometría (curvas más suaves), y una textura procedural sutil de tela (ruido generado por canvas) en el material del traje.
- **Sombras reales**: `renderer.shadowMap` activado (PCFSoftShadowMap), luz direccional con `castShadow` y frustum ajustado a la zona de juego, personaje proyecta sombra, suelo/alfombra la reciben. Se desactiva automáticamente en calidad "Baja" (el blob 2D original queda como respaldo solo en ese caso).
- **Carretera + gira de campaña por ciudades de EEUU**:
  - El suelo ancho ahora tiene una textura procedural de asfalto (en vez de color plano) y líneas amarillas discontinuas tipo autopista a los lados de la alfombra roja.
  - Cada ~260-480 unidades de distancia recorrida aparece un cartel real "WELCOME TO [CIUDAD]" (Nueva York, Chicago, Miami, Austin, Phoenix, Nashville, Detroit, Denver, Atlanta, Seattle, Boston, Las Vegas — rotan en orden) con el texto generado por canvas, a un lado de la pista. No usan pool (evento raro) — se construyen y se destruyen (`dispose` de geometría/material/textura) al pasar, para no acumular memoria en partidas largas.
- **Obstáculos actualizados**: más segmentos en cilindros/esferas de la valla, la pancarta y el atril+guardaespaldas, para que no desentonen con el personaje más detallado. El taco también subió un poco de segmentos.
- **Menús con más vida**: las tarjetas de overlay (inicio, ajustes, game over, etc.) ahora tienen animación de entrada (escala+fade) y un brillo dorado que pulsa suavemente en el borde; los botones grandes y pequeños tienen transición más suave al pulsarlos.

Verificado: stress test de Node en `world.js` (incluye ahora el sistema de carteles con distancia acumulada real) sin excepciones tras 5000 frames + resets, prueba dedicada de `character.js` (construcción + todos los métodos, incluidas las nuevas articulaciones de codo/rodilla) sin excepciones, sintaxis de `main.js`, y carga real en navegador con sombras/texturas canvas/todo el sistema activo sin errores de consola ni entradas en el log de errores.

**Nota de contenido**: los nombres de ciudades de EEUU en los carteles son solo texto genérico ("Welcome to Chicago" etc.) — no hay marcas, monumentos ni logos, así que no hay riesgo de derechos de autor/marca ahí.

### Quinta ronda: colisión lateral y más velocidad (2026-08-09)

- **Colisión menos estricta**: antes se comparaba el carril lógico (`currentLane`, que cambia al instante al pulsar) contra el del obstáculo. Como la posición visual real (`playerX`) tarda un poco en llegar al nuevo carril, a veces contaba como choque un simple roce lateral mientras el personaje aún estaba cruzando. Ahora se compara la posición X real del personaje contra el centro del carril del obstáculo, con un margen (`HIT_LANE_TOLERANCE = 0.85`, carril mide 2.2 de ancho) — así que solo cuenta si el personaje está razonablemente centrado en ese carril, no si lo está rozando de canto durante el cambio.
- **Velocidad +26%**: `BASE_SPEED` de 9.5 a 12, `MAX_SPEED` de 16.5 a 21, y `ACCEL` de 0.14 a 0.18 (llega antes a la velocidad máxima) para un ritmo más frenético.

Verificado: sintaxis de main.js, carga real en navegador sin errores de consola.

### Sexta ronda: aún más velocidad (2026-08-09)

El usuario probó el +26% y dijo que seguía sintiéndose lento. Segundo salto, más grande esta vez: `BASE_SPEED` de 12 a 17 (+42%), `MAX_SPEED` de 21 a 29 (+38%), `ACCEL` de 0.18 a 0.24. Verificado: sintaxis + carga real sin errores de consola.

### Séptima ronda: salto más ágil + inicio más suave (2026-08-09)

Con la velocidad ya subida dos veces, aparecieron dos efectos secundarios esperables:

- **Salto más rápido**: `JUMP_DURATION` bajó de 0.55s a 0.4s — con el ritmo más alto, dos vallas seguidas dejaban muy poco margen real (en segundos) entre un salto y el siguiente, y el salto se sentía lento/pesado en comparación.
- **Primeros ~3 segundos más suaves**: las filas de obstáculos generadas al iniciar cada partida (las más cercanas al punto de aparición, con z entre -14 y -52 aproximadamente — que es justo lo que tarda en recorrerse en unos 3s a la velocidad base actual) ahora tienen la mitad de probabilidad de traer obstáculos (27.5% en vez de 55%). El resto de la partida sigue igual.

Verificado: stress test de Node en world.js sin excepciones, sintaxis de main.js, carga real en navegador sin errores de consola.

### Octava ronda: sistema de biomas + realismo, sin preguntas (2026-08-09)

El usuario pidió ejecutar todas las mejoras visuales posibles sin preguntar nada, con foco en: pista no siempre recta, laterales con detalle urbano real (no solo edificios), zonas que cambien (desierto, pueblos, ciudades) a medida que avanza la distancia, y más realismo en personaje y entorno. Se ejecutó todo de una vez, con permiso explícito para no confirmar nada antes.

**Arquitectura nueva — sistema de biomas** (`world.js`): el "anillo exterior" de decoración (más allá de los paneles del mitin) dejó de ser un skyline fijo y pasó a ser un sistema de 3 biomas que rotan cada 260 unidades de distancia recorrida — **ciudad → desierto → pueblo → (repite)**. Cada bioma tiene su propio set de props con pooling independiente (no hay fugas de memoria — verificado con una simulación de 20.000 frames comprobando que el número de objetos en escena se estabiliza en vez de crecer sin límite). El suelo, la niebla y el color de fondo hacen una transición suave (interpolada) entre biomas; el domo del cielo se recolorea al cruzar a un bioma nuevo. Los props se generan calculando de antemano en qué bioma "aterrizarán" cuando el jugador realmente llegue ahí (no el bioma actual), así no hay costuras visibles.

**Detalle urbano real** (antes "solo edificios sin motivo"): farolas con luz, coches aparcados (5 colores), árboles con follaje, bancos, hidrantes, semáforos — todo esto ahora puebla el bioma ciudad junto a los edificios existentes.

**Bioma desierto**: cactus saguaro (tronco + brazos), rodadoras (tumbleweeds) que giran de verdad mientras ruedan, mesetas escalonadas, árboles muertos, y paleta de color más cálida (cielo/suelo/niebla en tonos naranja-arena).

**Bioma pueblo**: casas con tejado a cuatro aguas (4 colores de fachada), vallas de madera blanca, buzones, árboles — escala más residencial/pequeña que la ciudad.

**Pista menos monótona**: la curva ahora combina dos ondas de distinta frecuencia (130 y 47 unidades de periodo) en vez de un solo seno perfectamente repetitivo — serpentea de forma más orgánica.

**Personaje — segunda pasada de realismo**: textura sutil de piel (ruido procedural), corbata con patrón de rayas diagonales (textura canvas), cejas en dos segmentos con arco sutil (antes una caja recta), parpadeo periódico animado (se combina con el sistema de expresiones existente sin pisarlo), reloj de pulsera en la muñeca izquierda, cordones marcados en los zapatos, segundo mechón de pelo para dar volumen.

Verificado: stress test de Node en `world.js` (5000 frames + resets) y prueba dedicada de estabilidad de memoria del sistema de biomas (20.000 frames, conteo de objetos en escena estable ~500 sin crecimiento) sin excepciones; prueba dedicada de `character.js` (construcción + todos los métodos, incluido el nuevo parpadeo) sin excepciones; carga real en navegador con todo el sistema activo (biomas, texturas canvas, sombras) sin errores de consola ni entradas en el log de errores.

**Alcance real vs. "100 mejoras"**: en vez de forzar exactamente 100 cambios cosméticos triviales, se priorizó un sistema arquitectónicamente sólido (biomas con pooling propio, sin fugas) con ~14 props nuevos (cada uno con varias piezas geométricas) repartidos en 3 biomas, más 7 mejoras de detalle en el personaje y la curva orgánica de la pista — un conjunto grande y coherente en vez de relleno artificial.

### Novena ronda: pivote de estilo visual con capturas de referencia (2026-08-09)

El usuario pasó dos imágenes de referencia (una captura de Subway Surfers y un render del personaje "Jake") y dijo que el juego seguía viéndose "casi igual" — la ronda anterior añadió mucho contenido (biomas, props) pero no cambió el **tipo de sombreado**, que es lo que más define visualmente a Subway Surfers: nada de contorno negro tipo cómic, sombreado suave y brillante ("juguete de vinilo"), proporciones chibi marcadas, colores muy saturados y pocas formas grandes limpias en vez de mucho detalle pequeño.

**Nota de alcance**: se tomó la referencia como inspiración de *estilo/técnica de render* (tipo de shading, proporciones, paleta), no como copia literal — el personaje sigue siendo el presidente trajeado del concepto original (no un skater con sudadera), y el mundo sigue siendo la gira de campaña con tacos, no vías de tren. No se reprodujo el logo, el personaje "Jake" ni ningún asset de Subway Surfers.

Cambios (afectan a *todos* los materiales del juego a la vez, por venir de un solo punto central):

- **`toon.js` reescrito**: `MeshToonMaterial` (4 bandas duras) → `MeshPhongMaterial` (brillo especular suave). `withOutline()` pasó a ser una función vacía (no-op) — cero contorno negro en todo el juego, sin tener que tocar las decenas de sitios donde se llamaba.
- **Personaje simplificado y achibado** (`character.js`): se quitaron pinza de corbata, alfiler, pañuelo de bolsillo, botones del traje, gemelos, reloj de pulsera, cordones de zapato, y las 3 texturas de ruido procedural (tela/piel/corbata) — todo detalle fino que iba contra el look de formas grandes y limpias. Cabeza agrandada (0.4→0.46 de radio), torso y extremidades acortados para una proporción chibi más marcada. Colores del traje/corbata/piel más saturados y vivos. Zapatos blancos con un acento de color grande (en vez de cordones finos), manos redondeadas simples sin dedos marcados.
- **Paleta del mundo repintada tipo caramelo**: la textura de asfalto pasó de base oscura a base clara (para que el tinte de color de cada bioma se vea de verdad — antes se multiplicaba con una textura oscura y quedaba siempre apagado sin importar el color). Edificios ahora en morado/naranja-coral/turquesa/amarillo en vez de grises realistas. Alfombra, graderío y metal de obstáculos más vivos y claros. Colores de cielo/niebla de los 3 biomas más saturados.
- **Iluminación reajustada** para el nuevo material brillante: más luz ambiente (hemisférica 0.7→0.95), sol algo más suave (1.25→1.05) para no quemar los brillos especulares del Phong, y una luz de relleno nueva (frontal, suave, sin sombra) para evitar lados oscuros marcados — más plano y "de juguete", menos contraste dramático realista.

Verificado: sintaxis de `toon.js`/`main.js`, ejecución real en Node de `character.js` (construcción + todos los métodos) y `world.js` (5000 frames + resets) sin excepciones, carga real en navegador con el material Phong + iluminación nueva sin errores de consola ni entradas en el log de errores.

**Como siempre, sin verificación visual directa en esta sesión** (el panel del navegador no compuso frames) — este es el cambio más grande de dirección de arte hasta ahora y el que más necesita revisión con ojos reales antes de seguir iterando en detalle.

### Décima ronda: limpieza + casas reales + menos "blur" (2026-08-09)

Feedback tras ver el cambio de shading: le gustan las zonas por bioma pero "siguen siendo muy primitivas"; hay unos paneles rojo/azul sin sentido en los laterales; pidió casas de barrio mucho más realistas; y la niebla hacía que todo pareciera aparecer difuminado ("blur"). Se pidió de nuevo no preguntar y aplicar una tanda grande de cambios, buscando imágenes de referencia si hacía falta — se usaron las dos imágenes ya compartidas por el usuario (captura de gameplay + render del personaje) más conocimiento general del género, no se hizo una búsqueda web adicional porque no habría aportado detalle visual real que no se tuviera ya.

- **Bug encontrado y corregido — la "niebla como blur"**: el `Fog` iba de 15 a 52 unidades, pero los objetos aparecen en `SPAWN_Z=-60` — es decir, **todo nacía ya medio difuminado**, y se sentía como una neblina constante en vez de nitidez. Se amplió a `Fog(34, 78)`, casi hasta el plano lejano de la cámara (80), así que ahora se ve nítido mucho más lejos.
- **Paneles rojo/azul eliminados**: era `makeStageBackdrop()` (dos rectángulos de color con estrellitas doradas, sin ningún prop reconocible) — se quitó el sistema entero (función, array, spawn, reciclado).
- **Casas completamente rehechas**: antes era una caja con un cono de 4 caras encima. Ahora tienen zócalo, franja de remate, **tejado a dos aguas real** (dos paneles inclinados que se encuentran en una cumbrera, no una pirámide), chimenea, puerta con marco, porche con techo propio y postes, y ventanas con marco + contraventanas a ambos lados.
- **Acera con bordillo** a ambos lados de la alfombra (antes el suelo era una sola superficie sin ninguna referencia intermedia entre la pista y los edificios/casas).
- **Cableado eléctrico urbano**: postes con travesaño y cables colgando (curva simple tipo catenaria) en el bioma ciudad — toque clásico de calle americana.
- **Personaje**: mochila/riñonera a la espalda (silueta nueva, color dorado con franja roja), el pelo ahora tiene **movimiento secundario** (el mechón sigue el giro del cuerpo con un pequeño retraso, tipo resorte, en vez de moverse rígido pegado al cuerpo), y el salto/carrera tienen más "jugo" (rebote de cadera al correr subido de 0.04 a 0.06, estiramiento/aplastamiento del salto subido ~25%).

Verificado: sintaxis, stress test de Node en `world.js` (incluye las casas nuevas con la trigonometría del tejado) y `character.js` (mochila + pelo con retraso) sin excepciones, carga real en navegador sin errores de consola ni entradas en el log de errores.

### Onceava ronda: casas estilo victoriano con imagen de referencia (2026-08-09)

El usuario pasó una captura de Despicable Me/Minion Rush mostrando una casa victoriana blanca con tejado de tejas rojas, buhardilla, ventana circular, chimenea, valla blanca de estacas y césped — y pidió ese mismo nivel de detalle, "como si de verdad estuviera corriendo por la calle".

- **Textura de tablillas (clapboard)** en las paredes y **textura de tejas** en el tejado — ambas generadas por canvas (líneas oscuras finas sobre base blanca, se multiplican con el color real de la casa) en vez de color plano liso.
- **Buhardilla** (dormer): un cuerpo con su propio tejadillo a dos aguas y ventana, asomando del tejado principal (55% de probabilidad, para variedad).
- **Ventana circular decorativa** cerca de la cumbrera, con marco de color (50% de probabilidad).
- **Césped propio**: cada casa ahora trae su parcela de césped verde delante (hacia la pista) como parte del mismo grupo — antes el suelo del pueblo era solo un tinte de color sin ninguna parcela reconocible.
- **Valla blanca de estacas** bordeando el césped de cada casa (13 estacas + barandilla), en vez de depender de que un prop de valla suelto apareciera cerca por azar.
- Ventanas más altas con marco blanco + contraventanas de color variable (granate/verde/azul marino/ciruela, 4 variantes), chimenea con remate propio.

Verificado: stress test de Node (5000 frames + resets) y prueba de estabilidad de memoria (20.000 frames) con las casas mucho más pesadas geométricamente, sin excepciones ni fugas; carga real en navegador sin errores de consola.

### Doceava ronda: fundido en los bordes, sin "pop" (2026-08-09)

El usuario pasó otra captura de Subway Surfers y pidió específicamente que los objetos de los lados no aparezcan/desaparezcan de golpe — que parezca que "ya estaban ahí" y se van desvaneciendo al salir de cámara.

- **Fundido por escala en los bordes** (`edgeFade()` en `world.js`): los edificios, casas y decoración lateral (banderas, público, graderíos, nubes, banderines) ahora crecen suavemente desde el tamaño 0 en los primeros 8 unidades tras aparecer, y se encogen a 0 antes de reciclarse cerca de la cámara, en vez de aparecer/desaparecer de golpe. Es una función que solo depende de la posición Z actual del objeto (no hay que llevar la cuenta de "cuándo nació" cada uno), así que funciona igual de bien para los props con pool (edificios/casas, que se reciclan por adquisición/liberación) que para los que reciclan por salto de posición (banderas/público, que reaparecen lejos al cruzar cierto punto cercano a la cámara).
- Se dejó fuera a propósito: obstáculos, tacos, power-ups y las franjas/líneas del suelo — cambiar cómo aparecen los obstáculos podría afectar cuánto tiempo de reacción tiene el jugador, y no es lo que se pidió ("los lados", no el gameplay).
- Verificado con una inspección directa de la escena tras un `update()`: los objetos justo en el borde de aparición (a menos de 2 unidades de donde nacen) muestran escala reducida (0.14–0.17) mientras que los que están en medio del recorrido siguen a escala completa (1.0) — confirma que el fundido se activa donde debe y no en todas partes.

Verificado: stress test de Node sin excepciones, inspección dedicada de escalas por posición sin excepciones, carga real en navegador sin errores de consola.

### Treceava ronda: zona residencial real, Washington D.C. y selector de zona (2026-08-10)

Pidió una foto real de un barrio residencial de EEUU como referencia, una zona nueva con la Casa Blanca/Monumento a Washington/Pentágono, un selector de zona en el menú, y 20 preguntas para afinarlo. Se respondieron 3 preguntas (alcance del selector: bloquea toda la partida a esa zona; desbloqueo: todo abierto por ahora, se restringirá más adelante; estilo de monumentos: reconocibles pero estilizados) y luego el usuario pidió aplicar directamente las opciones recomendadas para el resto sin seguir preguntando.

**Decisiones aplicadas** (respondidas + recomendadas):
- El selector de zona bloquea **toda la partida** a la zona elegida (no solo el punto de partida).
- Todas las zonas están desbloqueadas por ahora (a petición del usuario, para poder probarlas — se planea restringir más adelante).
- Washington D.C. es una zona **solo por selección en el menú**, no entra en la rotación automática ciudad/desierto/pueblo.
- Monumentos reconocibles pero estilizados, mismo lenguaje low-poly que el resto del juego.

**Zona residencial repintada** (`world.js`, `makeHouse`): paleta ampliada con tonos oscuros marino/carbón + remates blancos (además de los claros ya existentes) para variedad tipo barrio moderno real. Porche cubierto con columnas de verdad (base+capitel) y un pequeño frontón triangular. Garaje adosado con puerta de panel y entrada de coches (65% de probabilidad). Setos recortados junto a la fachada. Densidad general de props subida (los clusters ahora aparecen cada 8 unidades en vez de 11, aplica a todas las zonas).

**Zona nueva "Washington D.C."** (`world.js`): sistema de "zona forzada" (`setForcedZone`) que fija toda la partida a una zona sin rotar — antes el sistema de biomas solo sabía rotar automáticamente. Props nuevos: Casa Blanca (pórtico con columnas, frontón, cúpula insinuada, ventanas en fila), Monumento a Washington (obelisco alto, prisma de 4 caras rotado 45° para el perfil característico), Pentágono (prisma de 5 caras real vía `CylinderGeometry` con `radialSegments=5` — la forma exacta sale gratis de la geometría — con un patio interior verde insinuado), un edificio gubernamental genérico con columnas para relleno, y cerezos (árboles con follaje rosa). Los carteles rotativos de "Welcome to [ciudad]" se desactivan automáticamente cuando hay una zona forzada (no tendría sentido ver "Welcome to Chicago" estando ya en una zona fija).

**Selector de zona en el menú** (`index.html`/`main.js`/`save.js`/`i18n.js`): fila de 5 botones en la pantalla de inicio (Auto/Ciudad/Desierto/Pueblo/Washington D.C.), la elección se guarda en el progreso guardado y se aplica llamando a `world.setForcedZone()` dentro de `resetRun()` — funciona igual para "Jugar" como para "Reintentar".

Verificado: stress test de Node (incluye simulación forzando la zona DC 3000 frames + volver a rotación automática después, sin excepciones), sintaxis de `main.js`, y **verificación funcional real en el navegador**: se hizo clic de verdad en el botón de Washington D.C. (se guardó `selectedZone: "dc"` en el progreso, el botón quedó resaltado), y luego en "Jugar" (pantalla de inicio se ocultó, HUD apareció, cero errores en el log tras construir toda la zona DC con materiales/sombras reales activos). Es la verificación más completa posible sin poder ver la pantalla directamente en esta sesión.

### Catorceava ronda: la niebla seguía sintiéndose como blur constante (2026-08-10)

El usuario pidió que los objetos no aparezcan detrás de un fondo difuminado, sino que la visión sea mucho más larga. El rango de niebla anterior (34-78) seguía cubriendo la mayor parte de la distancia de dibujado — con `SPAWN_Z=-60` y la cámara a ~7.2 de distancia en Z, los objetos nacen a unas **67 unidades de la cámara**, justo dentro de esa zona de niebla, así que en la práctica *todo* lo que aparecía ya estaba parcialmente difuminado, no solo el borde lejano.

- **Niebla retrasada mucho más**: de `Fog(34, 78)` a `Fog(68, 79)`. Como los objetos nacen a ~67 unidades (justo *antes* del nuevo inicio de niebla en 68), ahora aparecen ya completamente nítidos desde el momento en que se generan, y solo se funden con el fondo en un tramo muy corto (68→79) justo antes del límite de la cámara (`far=80`) — no como un velo constante detrás de todo el escenario.

Verificado: stress test de Node sin excepciones, carga real en navegador sin errores de consola.

### Quinceava ronda: el pop-in seguía notándose — la causa real era el radio del mundo, no solo la niebla (2026-08-14)

El usuario insistió: "aumentalo aun mas, se sigue viendo como aparecen en pantalla el fondo del mapa quiero que sea imperceptible". Iba por la tercera vuelta tocando solo el rango de niebla, así que esta vez tocaba entender **por qué** (68, 79) seguía sin ser suficiente en vez de volver a mover los mismos dos números a ciegas.

- **La causa real**: `Fog(68, 79)` ya estaba pegado al límite de la cámara (`far=80`), casi sin margen. Los props del centro nacen a ~67 unidades de la cámara — *fuera* del rango de niebla (68 es mayor que 67), o sea que nacían totalmente nítidos, sin ningún fundido de color. Pero los props laterales (desplazados hasta ~17 unidades en X para poblar los lados de la calle) están *más lejos* en línea recta de la cámara que los del centro a la misma Z (Pitágoras: hipotenusa siempre mayor que el cateto) — el peor caso llega a ~70.3 unidades. Con niebla empezando en 68, esos props laterales nacían ya *dentro* de la niebla pero sin margen para que se notara suave, y además el crecimiento de escala (`EDGE_FADE_IN_DIST`, de 0 a tamaño completo) pasaba en solo 8 unidades — muy poco espacio para que fuera gradual. Subir solo el rango de niebla otra vez chocaba además con lo que el usuario ya había pedido en la ronda anterior: nada de "blur" constante, quería visión más larga, no más neblina tapando todo.
- **La solución fue alargar el mundo, no solo repintar la niebla**: en vez de rellenar de niebla, se aleja el punto donde nace todo.
  - `SPAWN_Z`: -60 → **-90** (`world.js`). Los objetos nacen 30 unidades más lejos, donde por pura perspectiva ya se ven mucho más pequeños.
  - `EDGE_FADE_IN_DIST`: 8 → **30** (`world.js`). El crecimiento de escala de 0 a tamaño completo ahora pasa a lo largo de 30 unidades en vez de 8 — mientras el objeto todavía está lejos y chico en pantalla, no de golpe.
  - `camera.far`: 80 → **100** (`main.js`), para que la cámara pueda ver hasta el nuevo límite.
  - Niebla: `Fog(68, 79)` → **`Fog(82, 100)`** (`world.js`), ahora una franja corta pegada al límite real (100), en vez de ocupar casi toda la distancia de dibujado — se mantiene la filosofía "visión larga y nítida, niebla solo justo en el borde" que pidió el usuario, pero con más margen real.
  - **Domo de cielo**: radio 70 → **92** (`world.js`). Este fue el hallazgo importante de la ronda: el domo de cielo (una esfera opaca que cubre toda la escena) tenía el radio calibrado para el `camera.far=80` viejo — si solo se alargaban SPAWN_Z/niebla/cámara sin agrandar el domo, la esfera del cielo (más cerca que los props lejanos) los taparía antes de que llegaran al nuevo límite, o causaría parpadeos/recortes raros en el horizonte. Se subió a juego con margen extra para cubrir también los rayos diagonales hacia las esquinas de la cámara.
- **Compromiso de rendimiento asumido conscientemente**: con el mundo más largo hay más props vivos a la vez (verificado con el stress test: se estabiliza en ~750-760 children del grupo, frente a un rango menor con los valores anteriores). No se tocó el sistema de calidad gráfica para compensar esto — si el usuario nota que el juego va más lento en gama baja tras esta ronda, la solución sería escalar la densidad/distancia según `graphicsQuality`, pendiente de hacer solo si hace falta.

Verificado: stress test de Node (`test.mjs`, `test-edgefade.mjs`, y `test-biomes.mjs` de 20000 frames confirmando que el conteo de objetos vivos se estabiliza, sin fuga de memoria, con los nuevos valores), y carga real en navegador — se confirmaron en caliente los valores efectivos (`camera.far=100`, `fog.near=82`, `fog.far=100`, radio del domo=92) leyendo el estado real de Three.js vía un hook de depuración temporal (añadido y quitado en la misma ronda, no queda en el código), más una partida real iniciada sin errores de consola ni entradas en el log de errores.

### Dieciseisava ronda: franja blanca en el horizonte (2026-08-14)

El usuario mandó la primera captura de pantalla real de toda la sesión (el panel de navegador nunca había compuesto frames hasta ahora), marcando con un círculo rojo una franja horizontal blanca y vacía justo encima de los edificios, pidiendo que no se notara y que hubiera "mas espacio cargado, como si fuera real".

- **Causa encontrada**: la propia ronda 15 la causó sin querer. Al subir `EDGE_FADE_IN_DIST` de 8 a 30 para suavizar el crecimiento de los edificios, ese mismo fundido largo se aplicaba también a **todo** lo que va en el array `decor` — incluidas las nubes, que son el único contenido que ocupa la franja alta del cielo cerca del horizonte. Con un fundido de 30 unidades, las nubes tardaban igual de lento que un edificio en alcanzar tamaño completo, así que el tercio más lejano del mundo (donde cae la franja del horizonte en pantalla) se quedaba con nubes diminutas/invisibles — de ahí la franja vacía.
- **Arreglo dirigido, no un parche de niebla otra vez**: `edgeFade()` ahora acepta una distancia de entrada opcional (`inDist`) en vez de usar siempre la constante del módulo. Las nubes (marcadas con `userData.kind = "cloud"`) usan una entrada corta (8, la original) mientras que edificios y el resto de la decoración de suelo siguen usando la larga (30) — no hacía falta revertir nada de la ronda 15, solo separar el ritmo de fundido de las nubes del de los edificios.
- **Más nubes y más anchas**: de 1 nube por cluster a 2, y el rango lateral de aparición de ±10 a ±44 unidades (antes se quedaban cortas incluso respecto al ancho de los edificios del borde, ±17-20). Con esto la franja del horizonte queda poblada en todo el ancho de pantalla, no solo en el centro.

Verificado con los stress tests de Node (incluye un test nuevo, `test-cloudfade.mjs`, que confirma que las nubes llegan a escala casi completa mucho antes que el resto de props a la misma distancia) y, por primera vez en toda la sesión, **con capturas de pantalla reales** — el panel de navegador empezó a componer frames en esta ronda. Se comparó visualmente la franja del horizonte en zona Washington D.C. (la de la captura del usuario) y zona Desierto: en ambas las nubes cubren la franja de lado a lado, sin hueco plano visible. Cero errores de consola, log de errores vacío.

### Diecisieteava ronda: imán, carretera por bioma, y el pop-in que el usuario sigue viendo pero yo ya no reproduzco (2026-08-14)

El usuario reportó tres cosas en el mismo mensaje: los edificios "siguen" haciendo pop y el horizonte "sigue" blanco (a pesar de la ronda 16), el power-up imán no atrae nada, y la carretera es siempre la misma en vez de variar según la zona.

- **Imán reparado**: antes, `checkCollectibles()` solo ignoraba el filtro de carril mientras el imán estaba activo (`magnetTimeLeft > 0`) — la tortilla se recogía en silencio si pasaba cerca, pero nunca se movía visualmente, así que no se veía ningún "tirón" hacia el jugador. Ahora, con el imán activo, cada tortilla no recogida interpola su posición X en cada frame hacia `LANE_X[currentLane]` (el carril actual del jugador), así que vuelan de verdad hacia el personaje en vez de solo desaparecer si ya estaban en el carril correcto. Duración sin cambios (`MAGNET_DURATION = 6`, ya estaba cerca de los "5 segundos" pedidos).
- **Carretera por bioma**: `groundMat` usaba un único patrón de asfalto (ruido fino gris) en las cuatro zonas, con solo el tinte de color cambiando — de ahí que "siempre fuera la misma". Se añadió `makeDirtTexture()` (parches grandes irregulares + un par de rodadas, en vez del ruido fino y uniforme del asfalto) y `groundMat.map` ahora cambia al entrar en el desierto, en el mismo punto donde ya se recoloreaba el cielo al cruzar de zona. También se ocultan (`.visible = false`) las líneas amarillas discontinuas de autopista sobre tierra/arena — cada línea consulta la zona en su propia posición porque conviven varios tramos de bioma a la vez a lo largo de la pista, no solo la zona del jugador. Ciudad, pueblo y D.C. mantienen el asfalto con líneas (tiene sentido para calles/avenidas pavimentadas).
- **El pop-in / horizonte blanco — no lo reproduzco**: jugué varias partidas reales (con capturas de pantalla, que ya funcionan en esta sesión) en zona Ciudad y Desierto tras la ronda 16, y el horizonte se ve poblado de nubes de lado a lado, sin la franja blanca de la captura original del usuario, y sin ningún pop notorio de edificios en las capturas tomadas durante el movimiento real. Como no hay forma de que el mismo código produzca resultados distintos en el mismo servidor, lo más probable es que el usuario esté viendo una versión anterior: o el navegador de su dispositivo tiene en caché los archivos `.js` de antes de la ronda 15/16, o está probando una build de Android/iOS instalada previamente (que no se actualiza sola — `cap copy` solo sincroniza la carpeta del proyecto nativo, no reinstala la app). Pendiente de confirmar con el usuario cómo está probando antes de seguir tocando números de niebla/distancia a ciegas.

Verificado: sintaxis de `main.js` (`node --check` como módulo), stress test de Node de `world.js` sin excepciones, y partidas reales en el navegador en zona Ciudad y Desierto — cero errores de consola, log de errores vacío, líneas amarillas confirmadas ocultas en el desierto en las capturas.

### Dieciochoava ronda: el imán tiraba de toda la pista a la vez, y el pop-in sigue sin reproducirse (2026-08-14)

El usuario confirmó que la prueba es en navegador recién recargado (no caché), y corrigió el comportamiento del imán: lo que implementé en la ronda 17 movía **todas** las tortillas no recogidas de toda la pista hacia el carril del jugador en cuanto se activaba, en vez de solo las que el jugador va pasando cerca.

- **Imán con alcance limitado**: nueva constante `MAGNET_RANGE = 12` en `main.js` — con el imán activo, solo las tortillas con `z > -12` (a 12 unidades o menos por delante del jugador) empiezan a interpolar su X hacia `LANE_X[currentLane]`; las que están más lejos se quedan quietas en su carril original hasta que el avance normal de la pista las mete en rango. Se siente como ir absorbiendo lo que se va pasando, no como un salto instantáneo de todo el carril en toda la pista a la vez.
- **Error de sintaxis autoinfligido y corregido en el momento**: al escribir el comentario de esa constante puse `\` en vez de `//` como marcador de comentario (un lapsus, no un patrón real del código — comprobado leyendo el archivo de verdad). Habría roto la carga completa del módulo. Se detectó y corrigió antes de verificar, con `node --check` confirmando la sintaxis después.
- **Verificación precisa del alcance**: en vez de confiar en jugar a ciegas, se expuso temporalmente `world`, el carril actual y `checkCollectibles` vía un hook de depuración (quitado al terminar, confirmado con `grep` que no quedó rastro). Se forzó el imán activo, se hizo avanzar el mundo hasta tener una tortilla de otro carril justo en el borde del rango (z=-10.6) y otra justo fuera (z=-17.6), y se llamó a `checkCollectibles` varias veces a mano: la de dentro del rango pasó de x=2.2 a x=0 (su carril se igualó al del jugador); la de fuera se quedó exactamente en x=-2.2, sin moverse. Confirma el arreglo con números reales, no solo "no hay excepciones".
- **Pop-in / horizonte blanco**: sigue sin reproducirse por mi parte. Con la caché descartada, se probó además en proporciones de móvil reales (375×812) por si el recorte de FOV en pantalla angosta revelaba el hueco — tampoco ahí. Se le pidió al usuario una captura nueva del estado actual para poder ver exactamente qué sigue viendo en vez de seguir intentando reproducirlo a ciegas.

Verificado: `node --check` de `main.js` (sintaxis), prueba manual del alcance del imán con valores reales leídos del propio juego en ejecución (ver arriba), sin errores de consola ni entradas en el log de errores tras quitar el hook de depuración.

### Diecinueveava ronda: pase grande de detalle — "todo se ve cuadrado" (2026-08-14)

El usuario pidió, sin preguntar nada, al menos 100 cambios visuales para que carreteras, casas, peatones y "cada cosa que veas" se sintieran más realistas y menos a base de cajas. Se recorrieron las ~28 funciones `make*` de `world.js` y se les añadió detalle geométrico real a las más planas/cuadradas (no un recuento artificial — cada punto de abajo es una malla o textura nueva que antes no existía):

- **Peatones** (`makePerson`, el prop con más instancias del juego con diferencia): el torso pasó de una caja plana a una cápsula redondeada; se añadieron dos brazos, dos zapatos, y pelo (color al azar entre 5 tonos); el pantalón ahora varía de color en vez de ser siempre el mismo azul marino fijo. Es el cambio de mayor impacto visual porque este prop se repite decenas de veces en cada pantalla.
- **Banco** (`makeBench`): asiento de un bloque sólido → 3 listones separados; patas y reposabrazos en cajas → cilindros.
- **Farola** (`makeStreetLamp`): base ensanchada en la peana, brazo recto en caja → cilindro en diagonal, remate cónico sobre la luz.
- **Coche aparcado** (`makeParkedCar`): + espejos laterales, + faros delanteros y traseros (antes solo carrocería/cabina/ruedas).
- **Semáforo** (`makeTrafficLight`): + brazo de unión visible entre poste y caja, + visera sobre cada luz (antes las 3 bolas quedaban peladas).
- **Hidrante** (`makeFireHydrant`): + 2 bocas laterales.
- **Meseta del desierto** (`makeMesa`): antes 3 cajas apiladas idénticas; ahora cada capa tiene su propio tono de estrato (4 tonos), ancho/fondo irregular y una leve rotación (erosión), + 4 rocas sueltas en la base.
- **Valla genérica** (`makeFenceSegment`): + remate en punta sobre cada poste.
- **Buzón** (`makeMailbox`): + banderita roja lateral (el detalle clásico de un buzón de EEUU).
- **Edificio de gobierno** (`makeGovBuilding`, zona D.C.): antes una caja lisa con columnas pegadas; ahora tiene frontón triangular, escalinata de entrada, ventanas laterales y un asta con bandera en el techo.
- **Edificio de ciudad** (`makeBuilding`): + cornisa en el borde del techo, + puerta a pie de calle, + unidades de aire acondicionado al azar en el techo.
- **Casa Blanca** (`makeWhiteHouse`): + alas laterales (Ala Oeste/Este, antes solo el cuerpo central), + 2 chimeneas.
- **Acera**: antes un plano de color liso sin ninguna textura; ahora usa una textura de hormigón procedural con juntas de dilatación (`makeConcreteTexture`), a juego con el asfalto/tierra que ya tenían textura desde antes.

**Compromiso de rendimiento asumido conscientemente**: esto sube el número de mallas/llamadas de dibujo bastante (medido en el stress test de Node: ~2861 mallas y ~191k triángulos en una escena ya estabilizada — la cifra de triángulos es baja y no preocupa, pero 2861 llamadas de dibujo es más de lo ideal para gama baja de móvil). No se tocó el sistema de calidad gráfica para compensarlo. Si el usuario nota que el juego va más lento, la solución sería reducir el detalle de los props (sobre todo los peatones, por ser los más numerosos) cuando `graphicsQuality` esté en "baja".

Verificado: stress test de Node (`test.mjs`, `test-biomes.mjs` de 20000 frames, y un test nuevo `test-meshcount.mjs` que cuenta mallas/triángulos totales) sin excepciones ni fugas, y partidas reales en el navegador en zona Ciudad, Washington D.C. y Desierto con capturas — los peatones se ven claramente redondeados con brazos/pelo/zapatos visibles, sin errores de consola ni entradas en el log de errores.

### Vigésima ronda: la carretera siempre roja, los edificios "crecen" en vez de estar ya ahí, y nuevo power-up de boost (2026-08-14)

Tres mensajes seguidos del usuario, cada uno atendido en el momento:

- **La carretera cambia de color/textura por zona**: hasta ahora `carpetMat` (la alfombra de 3 carriles por la que corre el jugador) era un rojo fijo (`0xff2d3a`) en las 4 zonas — el usuario aclaró que para él "la carretera" es literalmente ese carril, no el asfalto de alrededor (que ya variaba desde la ronda 17). Se le añadió un campo `road` a cada entrada de `BIOME_COLORS` (ciudad/pueblo/D.C. en asfalto oscuro realista, desierto en tierra compacta) y `carpetMat` ahora sigue exactamente el mismo mecanismo de transición suave + cambio de textura que ya tenía `groundMat` (color con lerp continuo entre zonas, textura asfalto/tierra que cambia de golpe justo cuando cambia la zona). Las rayas blancas/amarillas que ya existían encima ahora se leen como marcas de carril reales en vez de flotar sobre un rojo sin sentido.
- **Los props ya no "crecen" al nacer — hallazgo importante**: el usuario aclaró la queja del pop-in que llevaba varias rondas sin resolverse del todo: no es que el crecimiento sea muy lento o muy rápido, es que **cualquier** crecimiento visible se lee como "esto acaba de aparecer", cuando lo que quiere es que parezca que el edificio ya estaba ahí y la niebla simplemente deja de taparlo. Se eliminó por completo el componente de fundido de *entrada* de `edgeFade()` (antes crecía de escala 0 a 1 a lo largo de `EDGE_FADE_IN_DIST`) — ahora los props nacen directamente a escala completa, y lo único que los oculta al nacer es la niebla (ya bien calibrada desde la ronda 15 para cubrir bien el punto de aparición). Se mantiene el fundido de *salida* (encogerse antes de reciclarse cerca del jugador), que es un mecanismo distinto y no fue parte de la queja. Esto también volvió innecesario el caso especial de fundido corto para las nubes que se había añadido en la ronda 16 (ya no hay fundido de entrada del que diferenciarse), así que se quitó junto con `EDGE_FADE_IN_DIST`.
- **Power-up de boost → flechas animadas en el suelo**: el usuario pidió sustituir el cono flotante ("Covfefe Boost") por flechas tipo boost pad de arcade de carreras. Se reemplazó por 3 chevrones planos (`THREE.Shape`/`ShapeGeometry`, no cajas rotadas a ojo) tumbados sobre la pista y apuntando hacia delante, con brillo emissive naranja y una animación de escala en ola que recorre las 3 flechas hacia el jugador (simula energía fluyendo hacia delante). Solo el kind "boost" usa esta lógica -- shield y magnet conservan su icono flotante girando de siempre.

**Verificación**: además del stress test de Node de costumbre, esta vez se verificó el chevron del boost con datos reales leídos del propio juego en ejecución (vía un `spawnPowerup` expuesto temporalmente y quitado al terminar) -- 6 vértices por chevron (coincide con el hexágono de la forma dibujada), rotación plana correcta, color/emissive correctos, y confirmado también visualmente en captura de pantalla real. El cambio de color de carretera se confirmó visualmente en Ciudad (asfalto oscuro) y Desierto (tierra clara) en la misma sesión de capturas.

### Vigesimoprimera ronda: horizonte de montañas permanente (2026-08-14)

El usuario mandó un GIF de Subway Surfers (tramo de montañas nevadas con una pagoda al fondo) diciendo: quiero el escenario así, que no aparezcan edificios sin más, que parezca que el personaje avanza *hacia* ellos.

- **El diagnóstico que faltaba**: las rondas 15-20 atacaron el problema por el lado de "esconder el nacimiento" (más distancia, más niebla, quitar el crecimiento de escala). Pero en la referencia lo que hace que el mundo se sienta continuo no es que el pop esté bien escondido — es que hay **un fondo lejano permanente** (la cordillera) que está ahí desde el primer frame y nunca nace ni muere. Eso da un punto de referencia fijo hacia el que avanzas; sin él, cualquier cosa que entre en escena se lee como "apareció", por bien tapada que esté.
- **Cordillera de fondo**: 16 conos de 5 lados (bajo poligonaje, mismo lenguaje low-poly del resto) repartidos a lo ancho del horizonte, a z≈-74/-82 — más allá del punto de aparición de los props (`SPAWN_Z = -90`) pero dentro del alcance de cámara. Son **hijos de la escena, no del grupo que hace scroll**: no se reciclan nunca, así que es estructuralmente imposible que hagan pop. Material `MeshBasicMaterial` con `fog: false` y un color desaturado por zona (nuevo campo `horizon` en `BIOME_COLORS`) que imita la perspectiva atmosférica — así se ve bien sin depender de que la niebla esté perfectamente calibrada. Se recolorea al cruzar de zona y en `reset()`, igual que el cielo y el suelo.
- **Error de orden de declaración detectado por los tests**: la primera versión colocaba el bloque del horizonte antes de la declaración de `BIOME_COLORS`, lo que reventaba con `ReferenceError: Cannot access 'BIOME_COLORS' before initialization` (las declaraciones `const` no se elevan como las de `var`). Lo detectó el stress test de Node al primer intento, antes de tocar el navegador — se movió el bloque justo después de `BIOME_COLORS` y quedó resuelto.

Verificado: stress test de Node sin excepciones y partida real en el navegador con captura — la cordillera se ve al fondo tras los edificios, y la carretera de la ronda 20 se confirma en asfalto oscuro.

### Vigesimosegunda ronda: z-fighting del suelo (regresión propia) + deslizamiento real (2026-08-14)

- **El suelo "medio transparente" que marea — regresión que introduje yo**: en la ronda 15 subí `camera.far` de 80 a 100 para alargar la vista. Eso reparte la misma precisión del buffer de profundidad sobre un rango mayor, así que a distancia deja de poder separar superficies muy juntas. Las capas del suelo estaban a y=0 (suelo), 0.01 (calzada), 0.012 (acera), 0.015-0.02 (rayas) — separaciones que antes bastaban y con far=100 ya no. Resultado: las superficies parpadean entre sí (z-fighting), que en pantalla se lee exactamente como "medio transparente" y marea. Se hizo evidente en la ronda 20 al quitar el rojo de la calzada, porque calzada y suelo pasaron a compartir textura y color parecidos. **Arreglo**: separaciones en Y mucho más generosas (calzada 0.04, acera 0.025, rayas 0.06-0.07) **y** `polygonOffset` en los materiales de calzada y acera, que resuelve el orden en el rasterizador sin depender de la distancia a cámara — es la solución robusta, la separación en Y sola volvería a fallar si algún día se sube más `camera.far`.
- **Deslizarse dos veces seguidas no se quedaba abajo**: `initControls` ignoraba por completo la acción "slide" si ya estabas deslizando (`!isSliding` en la condición). Con dos vallas seguidas, el jugador da al botón por segunda vez y no pasaba nada, así que se levantaba en medio de la segunda valla. Ahora un segundo toque **reinicia el cronómetro** del deslizamiento en vez de ignorarse (sin volver a sonar el efecto, para no solaparlo).
- **Pose de deslizamiento real en vez de ovillo**: `setSlidePose` solo rotaba y bajaba las caderas; brazos y piernas se quedaban en la pose de correr, y el conjunto se leía como una bola. Ahora se posa el cuerpo entero como un derrape de béisbol: torso muy reclinado, pierna adelantada estirada y la de atrás recogida, brazos hacia atrás, y la cabeza compensando la inclinación para seguir mirando al frente. Al soltar, resetea también la cabeza.

Pendiente de esta misma tanda: **rehacer el personaje para que no parezca un playmobil** (más realista y animado). Es el trabajo más grande de los cuatro puntos que pidió el usuario y va en su propia ronda, junto con lo acordado en las 10 preguntas de abajo.

Verificado: stress tests de Node (`test.mjs` y `test-character.mjs`) sin excepciones, y captura real en el navegador — la calzada se ve como asfalto sólido con las marcas de carril limpias, sin parpadeo.

### Vigesimotercera ronda: el personaje ya no parece un playmobil (2026-08-14)

Dos causas concretas del look "playmobil", ambas de proporción, no de detalle:

- **Cabeza desproporcionada**: r=0.46 contra un torso de r=0.25 — casi el doble de ancha. Se escaló el **grupo** entero de la cabeza a 0.78 en vez de tocar el radio de cada pieza, así ojos, cejas, nariz, orejas y mechones conservan sus proporciones y posiciones relativas exactas. Sigue siendo mayor que lo natural (es un runner caricaturesco), pero ya no domina la silueta.
- **Piernas cortas y rechonchas**: muslo 0.17→0.26 y espinilla 0.15→0.24, con radios algo más finos. La altura total del personaje apenas cambia (~2.17); lo que cambia es el reparto: menos cabeza, más pierna.
- **`HIP_Y` como constante única**: la altura de cadera estaba escrita a mano (0.92) en **cinco** sitios — construcción y cada pose de animación. Cambiar proporciones obligaba a acertar los cinco o el personaje se hundía en el suelo en una pose concreta. Ahora sale de una sola constante.

**Animación** (era una sola onda seno aplicada simétricamente a los cuatro miembros — un "juguete de cuerda"):
- Contrarrotación de hombros/caderas: el torso gira al revés que las piernas. Es lo que más separa una carrera real de un muñeco rígido.
- Rebote vertical al **doble** de frecuencia que la zancada. Antes usaba `cos(runPhase)`, así que el cuerpo solo botaba una vez por ciclo completo en vez de una vez por paso — se veía flotante.
- Brazos ligeramente desfasados respecto a las piernas (no en oposición perfecta) y cruzando algo hacia el pecho.
- Amplitud de zancada creciente con la velocidad: al esprintar las piernas se abren más, no solo van más rápido.
- Inclinación de carrera hacia delante, cabeza compensando el giro del torso para seguir mirando al frente.
- Pelo y corbata con inercia vertical a contratiempo del cuerpo; la corbata además ondea más cuanto más rápido vas.
- Salto asimétrico (una pierna más recogida que la otra) — dos piernas idénticas en el aire se leen como un muñeco.
- **Aterrizaje con peso**: nube de polvo a los pies + vibración corta al tocar suelo. Antes el salto terminaba en seco.
- **Inclinación en curvas** subida de 0.25 a 0.45, y ahora con giro en Y además del ladeo: el personaje se orienta hacia donde va en vez de desplazarse de lado siempre mirando al frente.
- **Fuga de estado entre poses**: al añadir rotaciones nuevas en `updateRun` (`hips.rotation.y`, `headGroup`), las poses de salto/deslizamiento/menú tenían que resetearlas o se quedaban pegadas al cambiar de estado. Se añadieron los resets en las tres.

**Dos errores propios detectados por los tests, no a ojo**:
1. Usé `curveX` para situar el polvo del aterrizaje, pero en ese punto del frame `curveX` aún no está calculado (se obtiene después, de `world.update`). Se cambió por la X real del personaje, que ya incluye el desplazamiento de la curva.
2. El primer test de proporciones medía la caja del personaje **incluyendo mallas invisibles**, y el escudo del power-up es una esfera oculta que cuelga más abajo que los pies — así que medía el escudo, no el pie, y daba una altura de cadera equivocada. Corregido el test para ignorar lo invisible y muestrear la zancada completa (el pie de apoyo es el que debe rozar el suelo, y oscila). Con eso, `HIP_Y` quedó ajustado a 0.845 y el pie de apoyo toca el suelo en y=-0.001.

Verificado: `test-character.mjs` sin excepciones, un `test-proportions.mjs` nuevo que mide contacto del pie a lo largo del ciclo, sintaxis de `main.js`, y partida real en el navegador con captura — proporciones claramente más humanas, sin errores de consola ni en el log de errores.

Pendiente de las 10 preguntas (abajo): expresión facial reactiva, desenfoque radial de velocidad, estela de fuego del boost, y el escalado por nivel de calidad gráfica.

### Vigesimocuarta ronda: calle de verdad en vez de props sueltos (2026-08-14)

- **Líneas de autopista sobre tierra — arreglo incompleto de la ronda 17**: entonces solo se ocultaron en el desierto las líneas amarillas exteriores (`roadLines`), y se olvidaron las rayas blancas de carril (`stripes`), que son justo las del centro del camino. Por eso el camino de tierra seguía teniendo marcas de autopista. Ahora ambas consultan el bioma en su propia posición.
- **Los edificios no formaban una calle**: cada prop caía a una X **aleatoria entre 9.5 y 16.5**. Sin línea de retranqueo común no hay manzana: quedaban sueltos, desalineados y sin continuidad — exactamente el "están separados, no tienen armonía". Ahora hay una línea de fachada casi constante (`FRONTAGE_X`) sobre la que los edificios se colocan pegados a lo largo de la calle, y el mobiliario urbano (farolas, coches, bancos, semáforos) va en una banda más cercana entre la acera y las fachadas. El desierto se queda disperso a propósito: ahí lo natural es que no haya alineación.
- **"Encarados a la cámara y no a la carretera"**: la rotación ya era correcta (la fachada con ventanas mira a la calzada), pero los edificios eran cajas **casi cúbicas** (w y d ambos 1.6-2.9). Al mirar calle abajo, la cara que más se ve es la lateral lisa, no la fachada, que queda de canto. Arreglado haciéndolos claramente más anchos a lo largo de la calle que hacia dentro de la manzana (d=3.4-5.6 vs w=1.8-2.8), que es como son los edificios reales entre medianeras.
- **"Todos se sienten igual"**: rejilla de ventanas (varias columnas por planta, con algunas apagadas al azar) en vez de una única ventana ancha por planta.

**Pop-in: sigue sin resolverse y ya van cinco rondas.** Cada intento ha atacado un mecanismo distinto (más distancia, más niebla, quitar el crecimiento de escala, cordillera de fondo) y el usuario sigue viéndolo. Mi conclusión, para no repetir el ciclo: el problema no es *cómo* aparecen sino **que aparecen** — mientras los edificios nazcan en un punto fijo delante del jugador, siempre habrá un instante en que un edificio no estaba y ahora está. Taparlo con niebla lo esconde a medias; el usuario ha rechazado explícitamente la niebla como solución. La solución real es que los edificios nazcan **fuera del campo de visión lateral** (a los lados, no de frente) o que la línea de fachada sea continua y solo se recicle por tramos, de modo que nunca haya un hueco que se rellene. Esto es un cambio de arquitectura del spawn, no un ajuste de números — pendiente de acordar con el usuario antes de meterse.

### Vigesimoquinta ronda: rediseño del traje y la cabeza del personaje (2026-08-17)

El usuario insistió en que seguía pareciendo un playmobil y pidió centrarse en el diseño del personaje principal. La ronda 23 arregló las **proporciones**; esta ataca la **construcción**, que es lo que quedaba delatándolo. Las tres causas concretas encontradas mirándolo de frente (hubo que mover la cámara del menú a propósito para poder verlo — el menú solo enseñaba su espalda):

- **Torso tubular sin silueta**: era una cápsula de grosor uniforme (r=0.25) de arriba abajo. Ahora es troncocónico (pecho 0.32 → cintura 0.20), aplastado en Z (más ancho que hondo, como un torso real), con remate redondeado de pecho y un faldón de chaqueta que se abre bajo la cintura. Da lectura de "traje" a distancia de juego, no de tubo pintado.
- **Brazos colgando de bolas sueltas**: el pivote del hombro estaba a X=±0.35 cuando el torso solo medía 0.25 de radio — el brazo quedaba flotando fuera del cuerpo con la bola de la articulación a la vista, que es literalmente el enganche de un playmobil. Ahora hay masas de hombro que continúan la línea de la chaqueta y el pivote se mete dentro de ellas (±0.265). Los brazos además adelgazan de hombro a muñeca (antes grosor constante) y tienen puño de camisa + muñeca de piel antes de la mano.
- **Pelo tipo casco encajado**: el casquete cubría 0.6·π, es decir toda la bola de la cabeza hasta las cejas — una peluca de playmobil. Ahora es más corto (0.42·π), desplazado atrás y ligeramente inclinado, dejando ver frente y sienes, con patillas que rompen el borde circular perfecto y una nuca que tapa el hueco por detrás.

**Bug real encontrado de paso**: el "cinturón" era `CapsuleGeometry(0.26, 0.02)` — una cápsula de **radio** 0.26 y longitud 0.02, o sea prácticamente una esfera negra del ancho del torso. En pantalla se veía como una panza negra enorme, no como un cinturón. Sustituido por un cilindro fino de verdad a la medida de la cintura.

**Camisa y cuello enterrados**: sus posiciones en Z (0.235 y 0.2) venían del torso cilíndrico fino y, con el pecho nuevo más hondo, quedaban **dentro** del torso y no se veían. Se recalcularon contra la superficie real del cono (que a la altura del pecho cae en z≈0.23), no a ojo. También se añadió pecho de camisa en V y corbata en dos piezas (nudo + pala) en vez de una tira recta.

**Cámara del menú**: apuntaba desde z positivo, así que la pantalla de inicio solo mostraba la espalda y la mochila. Ahora mira desde delante y apunta por debajo del pecho, de modo que la cara y el traje quedan por encima de la tarjeta del menú.

Verificado: `test-character.mjs` y `test-proportions.mjs` (el pie de apoyo sigue tocando el suelo tras todos los cambios), y capturas reales de frente, en menú y en partida — sin errores de consola ni entradas en el log de errores.

### Vigesimosexta ronda: caricatura — unos pocos rasgos reconocibles (2026-08-17)

El usuario pidió acercar el personaje a una caricatura de Donald Trump, aclarando que **no hace falta que sea reconocible, solo coger algunos detalles**. El juego ya iba en esa dirección desde el principio (título MAGA, traje azul, corbata roja, tupe rubio), así que es continuar el concepto, no cambiarlo. Se eligieron pocos rasgos, los que se leen a distancia de juego:

- **Paleta**: piel bronceada de tono cálido (0xf0b183, antes rosado de dibujo animado) y rubio pajizo (0xf3dc93, antes amarillo saturado). Es lo que más se nota desde la cámara de carrera, antes que cualquier detalle facial.
- **Tupe barrido y cruzado**: el mechón pasa a ser más ancho y volado, girado en diagonal para que cruce de un lado a otro, con un "alero" que sobresale por delante de la frente para que el peinado se lea también de perfil.
- **Mandíbula pesada**: mofletes bajos a los lados de la boca y papada suave bajo la barbilla, más la cara algo más ancha que alta. Da un aire adulto en vez de la cara de bebé redonda que tenía.
- **Corbata larga**: alargada de 0.34 a 0.52 para que pase por debajo del cinturón.

**Bug evitado**: `updateRun` escribía rotaciones **absolutas** sobre el tupe (`swoop.rotation.y = ...`, `.z = ...`) para la inercia del pelo. Con la pose base nueva (barrido en diagonal, con los tres ejes usados) eso habría borrado los ángulos en cuanto el personaje empezara a correr — el peinado se habría "desinflado" al primer frame de partida. Se guardan las rotaciones base al construir y la animación se **suma** a ellas.

**Verificación**: aquí el panel del navegador volvió a dejar de componer frames (el fallo recurrente de esta sesión), así que **este cambio no está verificado visualmente**. Sí está verificado que construye, que anima sin transformaciones inválidas (NaN/Infinity) tras 30 frames de carrera, que el pie de apoyo sigue tocando el suelo, y que no hay errores de consola ni en el log de errores. Pendiente de que el usuario confirme el aspecto.

**Riesgo de tienda (recordatorio)**: el riesgo político ya estaba asumido en el roadmap (Fase 3, punto 26). Acercar más el parecido a una persona real concreta lo aumenta: tanto Apple como Google tienen políticas sobre contenido que representa a personas reales, y una revisión podría pedir cambios. Sigue teniendo sentido mantener el plan B de assets/copy más genéricos.

### Vigesimoséptima ronda: segunda tanda de rasgos de caricatura (2026-08-17)

El usuario confirmó que con la ronda anterior aún no se distinguía y pidió más detalles. Se añadieron los que funcionan a tamaño pequeño (manchas de color y siluetas, no rasgos finos):

- **Antifaz claro alrededor de los ojos** (la marca de las gafas de sol sobre la piel bronceada). Es el detalle más identificable de esta caricatura concreta y el que mejor aguanta el tamaño pequeño, porque es una mancha de color y no una línea. Va dibujado por debajo de los ojos en el orden de construcción.
- **Ojos entornados**: el globo ocular se achata en vertical (0.68) y se le añade un párpado superior caído del color de la piel. Antes eran esferas redondas y saltonas, con cara de sorpresa permanente.
- **Cejas rubias** (0xd9be7a) en vez de marrón oscuro: era lo único de la cara que no encajaba con la paleta nueva y partía el rostro en dos.
- **Boca pequeña y fruncida** en vez de una raja ancha de 0.22.
- **Pin de bandera en la solapa**: dos franjas (roja y azul) del tamaño justo para leerse como insignia.

**Comprobación de interacción, no solo de que compila**: el sistema de expresiones y el parpadeo escriben sobre ojos y boca en cada frame, así que había riesgo de que borraran lo nuevo. Verificado que `applyEyeScale` escala el **grupo** del ojo (no la malla interior), de modo que el achatado del globo se conserva y el parpadeo se multiplica encima; y que `applyExpression` escribe `mouth.scale`, no la geometría, así que la boca estrecha se mantiene con `mouthScaleX = 1`.

**Sigue sin verificación visual**: el panel del navegador continuó sin componer frames durante toda esta ronda. Verificado que construye, que anima 30 frames sin transformaciones inválidas, que el pie de apoyo sigue tocando el suelo y que no hay errores de consola ni en el log de errores — pero el aspecto está sin confirmar por segunda ronda consecutiva.

### Vigesimoctava ronda: fondo blanco, monumentos de espaldas, multitud clonada (2026-08-17)

Tres bugs reales detrás de tres quejas que parecían estéticas:

- **"El fondo sigue siendo blanco"** — la cordillera del horizonte SÍ existía (se añadió en la ronda 21), pero su color (`0xaebfd6`) era casi idéntico al del cielo (`0x9fe6ff`) y además va sin niebla, así que se dibujaba y no se veía. Se oscurecieron y saturaron los colores de horizonte de las cuatro zonas. Además la fila solo cubría ±34 en X cuando a esa distancia la cámara abarca ~±50: quedaban huecos de cielo limpio en los laterales por donde se veía nacer a los edificios. Ahora son **dos filas** (±56 y ±59), la segunda más lejana y mezclada hacia el color del cielo para dar perspectiva atmosférica y tapar los valles de la primera.
- **"Washington no tiene Casa Blanca ni Capitolio"** — el Capitolio no existía, se ha creado (cuerpo con alas, escalinata, pórtico y sobre todo la cúpula sobre tambor con linterna, que es la silueta que lo identifica). Pero la Casa Blanca **sí estaba** y aun así no se reconocía: los monumentos se construyeron con el pórtico, las columnas y la escalinata en su cara **+Z**, mientras que `spawnOuterCluster` los rotaba 0/π como a los edificios corrientes (que tienen la fachada en −X). Resultado: los monumentos quedaban de canto o de espaldas a la calle. Se marcan ahora con `userData.frontZ` y el spawn les aplica un giro de 90° extra. Verificado con un test nuevo (`test-dc.mjs`): 53 monumentos vivos, los 53 orientados hacia la calzada. Casa Blanca y Capitolio van repetidos en la lista de fachada para que salgan más que el edificio genérico.
- **"La gente parece lego"** — todas las figuras del público eran clones exactos del mismo muñeco; una multitud de copias idénticas se lee como una caja de piezas por mucho que cambie el color de la camiseta. Ahora cada una tiene complexión y estatura propias, hombros redondeados que unen brazos y torso (antes los brazos salían de la nada por los costados, la unión típica de figura de juguete), piernas separadas en vez de un bloque único, y un 35% lleva gorra.

**Variedad de edificios**: antes todos eran la misma caja con ventanas y solo cambiaba el color. Se añadieron cuatro remates alternativos (cuerpo retranqueado tipo art déco, antena con baliza, cubierta a dos aguas, o cornisa simple) y toldo comercial sobre la puerta en un 40%.

Verificado: stress tests de Node (`test.mjs`, `test-biomes.mjs` de 20000 frames, `test-dc.mjs` nuevo) sin excepciones ni fugas, y carga real de la zona D.C. en el navegador sin errores de consola ni en el log de errores. **El aspecto sigue sin confirmarse visualmente**: el panel del navegador lleva tres rondas sin componer frames.

### Vigesimonovena ronda: imán que absorbe de verdad + desierto legible (2026-08-17)

- **El imán seguía sin atraer — diagnóstico anterior incompleto**: en la ronda 18 lo limité por alcance, pero solo interpolaba la **X** de la tortilla hacia el carril del jugador. La tortilla seguía avanzando a la velocidad normal de la pista, así que el imán parecía "ordenar" las tortillas en fila en vez de atraerlas. Ahora se interpola también la **Z** hacia el jugador (se resta distancia *además* del avance normal del mundo, por eso vuelan hacia él), con una fuerza que crece al acercarse (≈1 en el borde del rango, ≈3 encima del jugador) para dar succión acelerada, y con un radio de recogida más generoso porque al llegar volando no tiene por qué caer en la ventana estrecha de ±0.8.
  - Se descartó animar también la **Y** (arco al volar): `world.update()` reescribe la Y de cada tortilla cada frame con su propio rebote, así que el arco se perdería al frame siguiente. Se dejó anotado en el código para que nadie lo reintroduzca pensando que falta.
- **Desierto con "líneas de autopista"** — quedaba un tercer elemento que no se había ocultado: los **ribetes dorados** del borde de la alfombra. En las rondas 17 y 24 se ocultaron las líneas amarillas exteriores y las rayas blancas de carril, pero los ribetes son decoración de mitin y seguían dibujándose sobre la tierra. Ocultados en desierto y sustituidos por **arcenes de tierra removida**, para que la pista siga teniendo un borde legible.
- **El mareo del desierto**: pista y arena compartían textura (ambas `dirtTex`) **y** tonos muy parecidos (`0xc9a06a` sobre `0xe0b878`). Sin borde y sin contraste, la frontera de la pista desaparecía, no había referencia de dónde estabas y el conjunto se leía como una superficie plana y transparente. La pista pasa a ser bastante más oscura (`0x9c6b43`) y la arena algo más clara, además de los arcenes.

Verificado: stress test de Node sin excepciones, sintaxis de `main.js`, y partida real en el navegador sin errores de consola ni en el log de errores. El aspecto sigue sin confirmarse visualmente (el panel del navegador continúa sin componer frames).

### Trigésima ronda: capa de profundidad y fuera la mochila (2026-08-17)

- **Mochila amarilla quitada**: era un accesorio heredado de cuando el referente era Subway Surfers. Como la cámara de carrera ve al personaje **por detrás**, esa mochila era lo que más se veía durante toda la partida y tapaba el traje entero. Sustituida por el detalle de sastrería que corresponde ahí: costura central de la espalda y abertura inferior, en el tono oscuro de las solapas.
- **Capa intermedia de profundidad** (lo que faltaba para que el mundo dejara de sentirse plano): entre las fachadas de la calle (x≈10) y la cordillera del horizonte (z≈-80) no había absolutamente nada, así que se pasaba del detalle cercano al fondo lejano de golpe, como un decorado de dos planos. Se añade una capa de siluetas grandes sin detalle, a media distancia y muy separadas de la pista, distinta por zona:
  - **Ciudad / D.C.**: torres anónimas que insinúan una ciudad detrás de la primera línea de edificios (en D.C., algunas rematadas en cúpula).
  - **Pueblo**: masas de arboleda de copa redondeada, más bajas.
  - **Desierto**: mesetas y cerros lejanos.
  - Cada silueta va en uno de dos planos de profundidad, el de atrás con el color más mezclado hacia el cielo (perspectiva atmosférica).
  - Cuelgan de `scene`, no del grupo que hace scroll, y **no se crean ni reciclan nunca**: existen desde el primer frame y solo se muestra la del bioma activo. Por construcción no pueden hacer "pop", que es el problema que arrastramos hace rondas.

**Verificado esta vez SÍ visualmente** (el panel del navegador volvió a funcionar tras tres rondas sin componer frames): capturas de Pueblo y Washington D.C. confirman los tres planos (props cercanos → siluetas intermedias → montañas), las cúpulas y obeliscos de D.C. alineados y orientados a la calle, y la espalda del personaje ya sin la mochila. Además, un test nuevo (`test-midlayer.mjs`) comprueba que en cada zona hay **exactamente una** capa de fondo visible — el fallo silencioso más probable de este diseño habría sido mostrarlas todas a la vez. Stress tests de Node sin excepciones ni fugas.

### Trigésimo primera ronda: monumentos enanos y carga mucho más lejana (2026-08-17)

**Por qué no se veían la Casa Blanca, el Capitolio ni el Pentágono** — no era orientación (eso se arregló en la ronda 28) ni que faltaran: es que eran **diminutos**. Comparando alturas: Pentágono **0.55**, Casa Blanca **1.3**, Capitolio **1.5**, edificio de gobierno 1.8 — contra edificios de ciudad de **4 a 12** y un jugador de **2.2**. Eran monumentos más bajos que el propio personaje, perdidos entre la multitud y las farolas. Arreglado:
- Escalas de monumento: Casa Blanca ×2.4, Capitolio ×2.2, edificio de gobierno ×2.0, Pentágono ×1.6.
- El Pentágono además era un **disco plano** (altura 0.55 tumbada en el suelo): subido a 1.9 de alto, con el patio interior recolocado (se habría quedado enterrado dentro) y franjas horizontales que marcan las plantas.
- `FRONTAGE_X` pasa a ser **por zona**: D.C. usa 14.5 en vez de 10.5, porque la Casa Blanca escalada mide ~8 de ancho y con la línea común se habría subido a la acera.

**Que carguen mucho antes**: `SPAWN_Z` de -90 a **-128**, `camera.far` de 100 a **150**, niebla de (82,100) a **(118,150)**. Dos cosas que había que mover a juego o se rompía:
- El **domo de cielo** (radio 92) habría quedado *por dentro* del nuevo punto de aparición: los objetos nacerían fuera del cielo. Ampliado a 146.
- Las **montañas del horizonte** estaban en z≈-76/-86, delante del nuevo spawn. Movidas a -112/-124 (aún delante de -128, así que siguen tapando el punto de nacimiento) y agrandadas a juego con la distancia.

**Coste asumido y mitigado**: triplicar la distancia disparó el número de mallas de 2861 a **5712**. Como son llamadas de dibujo y esto va a móvil, se subió la separación entre grupos de props de 8 a 11, dejándolo en **4504**. Sigue siendo bastante más que antes (era el precio de lo que pediste), y la fachada continúa siendo continua porque los edificios miden 3.4-5.6 de ancho y van 2 por grupo, uno cada 5.5. **Si notas tirones en un móvil de gama baja, esto es lo primero que hay que mirar**: la vía clara sería escalar `SPAWN_Z` y la densidad según `graphicsQuality`, que sigue pendiente.

Verificado: stress tests (incluido `test-dc.mjs`: 74 monumentos vivos, los 74 orientados a la calle, y `test-midlayer.mjs`), medición de coste, y captura real de D.C. — la avenida se ve ahora mucho más larga, con cúpulas y obeliscos alineados a ambos lados hasta el fondo. Sin errores de consola ni en el log de errores.

### Trigésimo segunda ronda: expresión facial reactiva (2026-08-18)

Antes la cara solo cambiaba por **eventos puntuales** (chocar → sorpresa, coger taco → alegría) y volvía a "normal" con un `setTimeout` a ciegas. Corriendo a tope o recién arrancando ponía exactamente la misma cara: no reflejaba nada del estado de la partida.

Ahora la expresión tiene **dos capas**: una de fondo continua, calculada cada frame según cómo va la carrera, y destellos puntuales que la pisan unos instantes y luego dejan volver al fondo (antes el reset era siempre a "normal", así que un destello borraba el estado real).
- Dos expresiones nuevas: **`determined`** (ojos entornados, ceño, boca apretada) a velocidad alta o con boost, y **`worried`** (a medio camino del susto) cuando hay un obstáculo a menos de 11 unidades en tu carril y no llevas escudo.
- `flashExpression` pasa de `setTimeout` a temporizador por frame, que es lo que permite la vuelta a la capa de fondo.

**Dos comprobaciones que cambiaron el resultado**, en vez de dar por bueno que "no hay errores":
1. Espiando la expresión aplicada en partida real solo salían `normal` y `worried`. Con el umbral inicial (velocidad al 45%) hacían falta ~22 s de carrera para ver `determined` — más de lo que dura la mayoría de partidas, así que en la práctica no habría aparecido casi nunca. Bajado al 18% (~9 s de supervivencia).
2. Al medirlo, `maxSpeedFrac` en una partida desatendida llegaba solo a **0.02**: sin nadie jugando el personaje choca en ~1 segundo y la velocidad nunca sube, así que ese camino no es verificable con una partida automática. Se verificó por otra vía: un test nuevo (`test-expr.mjs`) compara la "firma" de la cara (posiciones y escalas de ceja y boca) entre las cinco expresiones y confirma que los 10 pares posibles dan caras distintas — es decir, ninguna expresión es un no-op.

Sondas temporales retiradas y comprobado que no queda rastro (`window.__expr` sale `undefined` en el navegador). Sin errores de consola ni en el log de errores.

Pendiente de las 10 preguntas: estela de fuego del boost, desenfoque radial de velocidad, y el escalado por `graphicsQuality` (este último ya es prioritario: ver el coste de 4504 mallas de la ronda 31).

### Trigésimo tercera ronda: 3 segundos de salida siempre limpios (2026-08-18)

Ya existía una "zona fácil" al principio de cada partida (ronda 7), pero solo **reducía a la mitad** la probabilidad de obstáculos (0.275 en vez de 0.55) — con lo que aún podía tocarte uno nada más arrancar. Ahora esa probabilidad es **0** en el tramo inicial.

- El umbral `EASY_ZONE_Z = -52` ya correspondía a los 3 segundos pedidos y se deja: a la velocidad inicial (17 u/s) son 51 unidades, así que un obstáculo en z=-51 tarda justo 3 s en alcanzar al jugador, que está en z=0.
- Solo afecta al relleno inicial: una vez rodando, las filas nuevas nacen en `SPAWN_Z` (-128), muy por debajo del umbral, y mantienen la dificultad normal. No cambia nada del resto de la partida.
- Los **tacos sí siguen apareciendo** en ese tramo (rama `else` de `spawnRow`), así que la salida no queda vacía ni aburrida.

Verificado con un test nuevo (`test-easystart.mjs`) que hace **300 resets** — porque el reparto es aleatorio y un solo reset podría salir limpio por pura suerte — y mide en cada uno el obstáculo más cercano al jugador convertido a segundos. Margen más corto encontrado: **3.29 s**, ningún reset por debajo de 3. Además, partida real en el navegador sin errores de consola ni en el log de errores.

### Dirección visual acordada — 10 preguntas de calidad estética (2026-08-14)

Respuestas del usuario a una ronda de 10 preguntas sobre calidad visual/estética. **Esto es el plan de trabajo visual pendiente**, aún no implementado (salvo lo ya hecho en rondas anteriores):

1. **Horizonte**: varias capas de montañas a distintas distancias y tonos, para profundidad real (no una sola fila como la de la ronda 21).
2. **Hora del día**: ciclo que avanza con la distancia (día → atardecer → noche), no una luz fija.
3. **Legibilidad nocturna**: la noche nunca llega a oscuridad total — farolas/ventanas/letreros encendidos **y además** obstáculos y tacos con brillo propio que ignora la luz ambiental. Las dos cosas.
4. **Relieve de pista**: ondulación vertical suave **y** tramos elevados tipo viaducto con caída a los lados (como el puente del GIF de referencia). Sin tocar la jugabilidad de saltar/esquivar.
5. **Personaje**: las cuatro — inclinarse en curvas y cambios de carril, más expresión facial reactiva, ropa/pelo con inercia, y aterrizaje con peso (flexión de rodillas + polvo).
6. **Velocidad**: desenfoque radial en los bordes de pantalla + estela de fuego tras el personaje durante el boost. (Descartado: zoom/vibración de cámara y saturación del mundo.)
7. **Ambiente**: partículas por zona (hojas/arena/papeles), pájaros y aviones de fondo, y charcos con reflejos en el asfalto. (Descartado: rayos de sol volumétricos.)
8. **Público**: las cuatro — que reaccionen al pasar el jugador, más variedad de cuerpos/edades/complementos, peatones caminando por la acera en ambos sentidos, y agrupación en corrillos irregulares en vez de alineados.
9. **Paleta**: cada zona con carácter propio y contraste fuerte entre ellas — ciudad fría azulada, desierto cálido dorado, pueblo verde suave, D.C. sobrio y claro.
10. **Prioridad/rendimiento**: aplicar todo, **pero** haciendo que el ajuste "Gráficos" (baja/media/alta) recorte automáticamente lo más caro en móviles flojos. Esto ya era deuda pendiente señalada en las rondas 15 y 19 (mallas/draw calls subiendo sin compensación por nivel de calidad) — ahora queda confirmado como parte del trabajo.

**Fase 1 — Pulido del runner base (prioridad confirmada antes de tienda)**
11. Playtesting dirigido: ajustar ritmo de velocidad según feedback real.
12. Ampliar ventana de streak, aumentar frecuencia de power-ups.
13. Escalar dificultad/mezcla de obstáculos con la distancia.
14. Nuevos tipos de obstáculos + variedad de escenografía por distancia.
15. Animación de tropiezo al chocar, partículas de polvo/impacto, momento pico en x5.
16. ~~Pase visual "más Minion Rush"~~ ✅ **implementado, pendiente de verificar jugando** (ver sección "Pase visual — implementado" arriba para el detalle técnico completo).
17. Iterar diseño del taco y del personaje (proporciones un poco exageradas, cabeza más grande, más parecido a la referencia real dentro de ese estilo).
18. Tutorial de onboarding la primera partida.
19. Botones on-screen + indicador de swipe en tiempo real + soporte de gamepad.
20. Música grabada con variación de intensidad + voz grabada del personaje.
20b. Más adelante (no bloquea el lanzamiento): ampliar de los ambientes iniciales a 4+ mundos/temas distintos según distancia.

**Fase 2 — Progresión y monetización (después de que el runner esté sólido)**
21. Conectar la UI de tienda ya soportada por `save.js` (trajes, personajes, skins).
22. Balancear precios (progresión de varios días).
23. Backend de ranking mundial (Firebase/Supabase) + UI de leaderboard.
24. Sistema de misiones diarias.
25. Integrar IAP + anuncios.

**Fase 3 — Publicación**
26. Revisión final de contenido (riesgo político asumido conscientemente — tener listo un plan B de assets/copy más suaves por si Apple/Google piden cambios en revisión).
27. Submission a Google Play y App Store.

### Trigésimo cuarta ronda: Washington D.C. rehecho en Blender (2026-10-20)

Isidro pidió hacer con este juego lo mismo que con AlienZ: rehacer los mapas en Blender con texturas. Decidió: estilo **dibujo animado mejorado** (no realista), **zona a zona empezando por D.C.**, y el personaje y los tacos **después**.

- `blender/comun.py` + `blender/dc.py`: cada pieza se modela por separado y sale como un solo objeto con una textura donde van horneados colores, ladrillo/sillería y la sombra de los rincones. Se genera con `blender -b -P blender/dc.py` (minuto y medio; `--rapido` para probar).
- Piezas: Casa Blanca (con verja y jardín), Capitolio (cúpula con columnas y nervios), Lincoln Memorial (con Lincoln sentado), edificio federal, casas de Georgetown, cerezo, farola y el obelisco (fijo al fondo). El Pentágono se quita: no pega en una calle.
- `www/src/models.js` las carga al arrancar; si alguna falla, se usan las piezas antiguas. `?sinblender` en la dirección arranca con las antiguas para comparar.
- Fachadas colocadas una detrás de otra según su ancho real (antes a distancia fija y se pisaban) y alineadas por delante en una misma línea.
- Medido en D.C.: 3.262 llamadas de dibujo por fotograma (antes 4.431) y 437.000 triángulos (antes 349.000).
- El juego no tenía copia: repositorio git solo local, etiqueta `antes-de-blender`.

### Trigésimo quinta ronda: la ciudad rehecha en Blender (2026-10-21)

Isidro dio por buena D.C. y pidió seguir con la ciudad, mismo estilo.

- `blender/ciudad.py`, 17 piezas. Fachadas: tienda de ladrillo con escalera de incendios y depósito de agua (dos: «PIZZA» roja y «TACOS» crema), torre de oficinas de cristal (azul y verde), rascacielos art déco «HOTEL», diner con letrero de neón, pisos con mirador y balcones (morado y naranja). Acera: árbol, farola de brazo, semáforo con cartel «MAGA AVE», boca de incendios, banco, buzón azul de correos. Coches aparcados: taxi, rojo y azul.
- Ventanas de las torres pintadas con la textura de ladrillo de Blender al revés (el ladrillo es el cristal y la junta la pared): un rascacielos entero cuesta 600 triángulos.
- `world.js`: la colocación de D.C. pasa a ser genérica (`ZONAS_BLENDER`): cada zona dice sus fachadas con su peso, su mobiliario y sus coches. Pueblo y desierto siguen con las piezas antiguas.
- Medido en la ciudad: 3.406 llamadas de dibujo por fotograma (antes 4.262) y 385.000 triángulos (antes 306.000). D.C. comprobado igual tras generalizar el código.

### Trigésimo sexta ronda: el pueblo rehecho en Blender (2026-10-21)

Isidro dio por buena la ciudad y pidió seguir con el pueblo. Se mantiene la referencia de agosto (la casa victoriana de Gru: tablillas, tejas rojas, ojo de buey, chimenea, valla blanca, césped).

- `blender/pueblo.py`, 10 piezas. Casas, cada una con su césped, camino y valla de estacas con flores: victoriana blanca de tejas rojas con porche, victoriana azul con torreón, casa baja amarilla con garaje, entrada de coches y canasta, colonial azul marino con buhardillas y portada, casita rosa de tejado turquesa con mirador, e iglesia blanca con campanario, reloj y cartel «WELCOME» (sale menos). Acera: roble, arbusto con flores, buzón con banderita y farola de farol. Coches: los de la ciudad.
- Paredes de tablillas y tejados de tejas pintados con la textura de ladrillo de Blender; tejados a dos aguas nuevos en `comun.py` (`tejado`, `hastial`, `panel`).
- Una zona puede usar piezas de otra carpeta (`"ciudad/coche_rojo"`).
- Medido en el pueblo: 3.456 llamadas de dibujo por fotograma (antes 5.280) y 442.000 triángulos (antes 315.000).

### Trigésimo séptima ronda: protagonista nuevo y suelo estilo Minions (2026-10-22)

Isidro pidió rediseñar el personaje «un poco parecido a Donald Trump, solo un poco», cambiar los colores del suelo y hacerlo todo más estilo Minions; permiso libre para descargar texturas (no hizo falta: las de dibujos salen mejor generadas).

- `blender/personaje.py`: 11 partes en un solo `www/models/personaje/personaje.glb`, cada una con su punto de giro en el origen del pivote de `character.js`. Estilo Gru: torso de tonel con chaqueta y solapas, camisa en V, insignia de la bandera, corbata roja larga hasta la cintura, piernas finas, zapatos negros en punta, manos pequeñas, cara de pera con mandíbula ancha, piel bronceada naranja con la marca blanca de las gafas, tupé rubio con mechas.
- Se queda el esqueleto de primitivas (todas las animaciones, ojos, cejas y boca que cambian de expresión); solo se cambian las formas. Traje y corbata se hornean en blanco y el juego los tiñe con el color de la tienda. Si el modelo no carga, sale el muñeco antiguo.
- Primera piel (0xf3a46a) salía marrón en el juego; se aclaró a 0xffbe86.
- Suelo estilo Minion Rush: calzada de asfalto azulado de dibujos (no negro) con manchas y grietas, aceras de baldosas grandes con relieve y color cálido por zona (nuevo `sidewalk` en `BIOME_COLORS`), losetas de plaza en ciudad y D.C., césped de dibujos en el pueblo, bordillo más gordo y rayas de carril amarillas.
- Medido en el pueblo: 3.234 llamadas de dibujo y 431.000 triángulos (antes 3.456 y 442.000).

### Trigésimo octava ronda: obstáculos, visibilidad y mecánicas de Minion Rush (2026-10-22)

Isidro pidió rediseñar los obstáculos y la visibilidad copiando de Minion Rush todo lo posible, en lo visual y en las mecánicas, y que sea atractivo. Se copian mecánicas y estilo, no sus personajes ni sus dibujos.

- `blender/obstaculos.py`, 9 modelos con contorno negro de dibujos y sombra en el suelo: barricada de caballetes y fila de conos (saltar), pancarta «MAGA» y arco de globos (deslizarse), guardaespaldas con atril y furgoneta de prensa «NEWS» (esquivar), coche patrulla con sirena que viene de frente (se puede saltar por encima: mide 1.2), autobús de campaña «MAGA TOUR» con rampa (subirse) y gorra roja (potenciador).
- Mecánicas nuevas: física vertical real (gravedad y velocidad de salto calculadas para que el salto normal se sienta igual); subir por la rampa, correr por el techo del autobús lleno de tacos y caer al acabarse; coche patrulla que adelanta a la pista (solo sale si su carril está libre y no se cruza cerca del jugador con una fila que tape los otros dos carriles; se lleva por delante los tacos); arcos de tacos encima de lo que se salta; modo gigante «Presidente Gigante» (gorra, 7 s, ×1.7, aplasta todo y da 5 tacos por golpe, la cámara sube); con escudo o gigante los obstáculos salen volando dando vueltas.
- Junto al autobús nunca hay más de un obstáculo más: siempre queda hueco.
- `?prueba` en la dirección activa `window.__juego` (estado, inmortal, saltar, gigante, carril) para comprobar mecánicas sin jugar a mano. Comprobado: barricada saltada 0 choques y sin saltar choca; pancarta, guardaespaldas y patrulla chocan; autobús 0 choques subiendo; gigante aplasta.
- Medido en el pueblo: 3.379 llamadas de dibujo y 481.000 triángulos (antes 3.234 y 431.000).

### Trigésimo novena ronda: rayo congelador, cohete, jefe y misiones (2026-10-22)

Isidro pidió seguir con más cosas de Minion Rush: rayo congelador, cohete, jefes y misiones.

- Modelos nuevos en `blender/obstaculos.py`: pistola de rayo, cohete rojo y blanco, barril de salsa, chile y el jefe «Burrito-Bot» (burrito robot con ojos rojos, pinzas y propulsores; rival inventado, nada de personas reales).
- **Rayo congelador** (6 s): lo que hay delante a menos de 45 se mete en un bloque de hielo (capa translúcida con la forma hinchada, `capaHielo` en models.js), se para y se rompe al tocarlo (+2 tacos). El autobús no se congela.
- **Cohete presidencial** (6.5 s): el personaje sube a 7 de altura montado en el cohete y vuela sin chocar; al despegar se llena de tacos el cielo de delante; las filas del último 1.6 s salen vacías para aterrizar limpio. Los tacos solo se cogen a la altura del personaje (antes se cogían los del suelo volando).
- **Jefe Burrito-Bot**: a los 1200 m y luego cada 2000. Flota delante con barra de vida, lanza barriles de salsa (se saltan) al carril del jugador el 60 % de las veces; el primero espera 5.5 s para no coincidir con obstáculos normales. Mientras está no salen obstáculos normales, solo tacos y chiles; cada chile cogido sale disparado hacia él. 5 golpes = +150 tacos y confeti; a los 40 s se va sin premio.
- **Misiones** (`missions.js`): tres activas de tipos distintos, de partida (tacos, distancia) o acumuladas (saltos, deslizar, autobuses, aplastar de gigante, hielo, cohete, jefe), con niveles que suben y premios de 60 a 800 tacos. Se ven en el menú y al acabar; aviso verde al cumplir una.
- `?prueba` ahora también tiene `rayo()`, `cohete()`, `jefe()` y `paso(n)`, que avanza el juego fotograma a fotograma aunque la ventana esté oculta. Comprobado: cohete a 6.96 de altura, 164 tacos y 0 choques, aterriza; rayo congela y rompe sin choque; jefe aparece, lanza barriles, cae con 5 chiles y da el premio; una misión se cumplió y se repuso sola.

### Cuadragésima ronda: el juego mareaba (2026-10-23)

Isidro: «lo único que me molesta es que el juego marea mucho… las carreteras con esos colores y esa textura marean al jugarlo unos segundos». Causas encontradas y arreglos:

- **La pista se balanceaba de lado sin parar** (curva de 2.1 cada ~130 u y otra de 0.55 cada ~47 u: un vaivén de 0.2-0.5 Hz, el típico de mareo en barco). `CURVE_AMPLITUDE` y `CURVE_AMPLITUDE2` a 0: pista recta.
- **Rayas de carril discontinuas** amarillas de 1.1 cada 3: a 25-30 u/s pasaban ~10 por segundo, efecto estroboscópico. Ahora continuas (tramos de 3 seguidos, reciclados a 129 para no solaparse) y blanco suave sin brillo; las doradas exteriores también continuas.
- **Texturas con dibujo pequeño y contraste** (juntas oscuras con relieve pintado, baldosas de 1 m, manchas y grietas en el asfalto, rayitas en el césped) que «tiemblan» al pasar. Ahora: asfalto liso con granulado finísimo, losas de acera de ~2 × 2.2 con la junta apenas marcada, losetas de plaza suaves, césped solo con manchas grandes; anisotropía 8.
- **Colores más tranquilos**: calzada gris pizarra (no azul vivo), aceras beis suave, césped menos chillón.
- **Cámara**: ya no se inclina al cambiar de carril, solo acompaña la mitad del cambio de carril (antes se deslizaba entero), y no sube y baja en cada salto (solo con el techo del autobús o el cohete). Líneas de velocidad rebajadas (máximo 0.35 en vez de 1).

### Cuadragésimo primera ronda: 32 preguntas — de juego sin fin a campaña con historia (2026-10-24)

Isidro: el personaje es «tosco, poco natural», la estética «Playmobil» no le convence, las casas son genéricas; quiere mapas «como la vida real» (edificios fijos en su sitio, no los mismos apareciendo sin parar), recrear la Casa Blanca con el personaje entrando al final, y que tenga historia y no sea sin fin. Pidió 30+ preguntas. Respuestas:

- Mareo (le sigue mareando algo menos, en todos los momentos): cámara más alta y lejana; empezar más lento. Efectos, público y cambio de carril como están. Juega en móvil vertical.
- Estética: animación tipo Pixar, colores naturales, luz distinta por nivel (Casa Blanca al atardecer), sin contorno negro.
- Personaje: con Meshy (enseñar malla antes de pagar), bastante más parecido a Trump, proporciones Pixar, animación de verdad con esqueleto.
- Historia: gira hasta la Casa Blanca en 5 niveles de 3-4 minutos con calles reales: Quinta Avenida → pueblo del Medio Oeste → Ruta 66 (Arizona) → Strip de Las Vegas → Pennsylvania Avenue. Primero se hace Washington. Final corto (~10 s) entrando por el pórtico norte. Entre niveles, mapa de EE. UU. con el autobús.
- Jugabilidad: al chocar se repite el nivel entero; el sin fin queda como extra; se quedan autobús, cohete, gigante, rayo y misiones; un jefe distinto al final de algunos niveles; estrellas 1-3; controles deslizando; el personaje habla con voz.

Aplicado ya: cámara de carrera de (0, 5.2, 7.2) a (0, 7.2, 9.8) mirando a z -18; velocidad de 13 a 25 con aceleración 0.12 (antes 17 a 29 con 0.24).

### Cuadragésimo segunda ronda: nivel 5, Pennsylvania Avenue hasta la Casa Blanca (2026-10-24)

Primer nivel de la gira (el último de la historia, que Isidro eligió hacer primero).

- `blender/washington.py`, estilo tipo Pixar (cantos redondeados con 2 segmentos, colores naturales de piedra): Archivos Nacionales (tramo con columnas gigantes y el gran pórtico), Justicia, IRS, antiguo Correos con su torre del reloj, Reagan, Wilson, Embajada de Canadá, edificio de cristal «FREEDOM», Navy Memorial con su plaza y fuentes, FBI brutalista, hotel Willard con mansarda y torreón, ala Este de la Galería Nacional, Pershing Park, Tesoro con su columnata, y la Casa Blanca (fachada norte, pórtico, jardín con fuente y camino curvo, verja) con las hojas de la puerta aparte.
- Los edificios federales son enormes: se modelan por tramos de 20 de fachada que el nivel repite en su orden real (`www/src/levels.js`). Cada lado es una lista en orden con los cruces de calle como huecos: la calle es siempre la misma (275 tramos), nada al azar.
- Obstáculos con azar de semilla (el mismo reparto en cada intento, como pidió: al chocar se repite el nivel entero); empiezan tranquilos y se van llenando; los últimos 190 m solo tacos. Mobiliario: farolas de globo y robles. Luz de atardecer (sol bajo y dorado, cielo cálido). Sin jefe en este nivel.
- Los modelos del nivel (6.4 MB) se cargan al entrar, no al abrir el juego (`cargarCarpeta`).
- Final (~10 s): frena tras la verja, va por la curva del camino alrededor de la fuente, sube la escalinata, se da la vuelta y saluda en la puerta, entra y se cierran las puertas; pantalla «¡Has llegado a la Casa Blanca!» con estrellas (350/700/1100 tacos) y misiones.
- JUGAR abre el mapa de EE. UU. con la ruta de la gira (NY → Ohio → Arizona → Las Vegas → Washington); los otros cuatro salen como «Próximamente». «♾️ Sin fin» queda como extra.
- Pendiente: personaje con Meshy (estilo Pixar, más parecido a Trump, animado con esqueleto), voces, los otros cuatro niveles, el Capitolio detrás de la salida.

### Cuadragésimo tercera ronda: el presidente de Meshy (2026-10-24)

Isidro pidió rehacer el personaje con Meshy enseñándole la malla antes de pagar.

- Tres mallas de prueba (20 créditos cada una, `--pixar --persona --solo-malla`, estilo Pixar nuevo en `z-resistance/herramientas/meshy.mjs`): la 1 y la 2 sin nombre salían un señor genérico sonriente; la 3, pidiendo «caricatura de Donald Trump», sí tiene el tupé ancho, el ceño y la cara ancha. Eligió la 3. Textura y esqueleto 15 créditos más. Total 75; saldo 360.
- `www/models/personaje/presidente.glb`: andar y correr de Meshy unidos en un archivo (`unir-animacion.mjs`) y adelgazado de 5.3 a 0.83 MB (`adelgazar.mjs --color 1024`).
- `www/src/presidente.js`: mismo contrato que el muñeco de `character.js` (que queda de respaldo, `?sinmeshy`). Corre con la animación de verdad; salto y deslizamiento son posturas encima; el saludo de la Casa Blanca levanta el brazo derecho. Material cambiado a Phong (el metálico de Meshy salía negro sin entorno). La altura sale de la geometría (los huesos ya están en metros; la caja en el mundo lo dejaba 4 veces más grande).
- Aprendido: con la animación parada el mezclador no reescribe los huesos, así que un giro relativo se acumula: hay que guardar la postura de partida y girar desde ella.
- La cara de Meshy no tiene gestos: las expresiones (sorpresa, alegría…) ya no se ven. Los colores de traje de la tienda tampoco (la textura viene pintada).

### Cuadragésimo cuarta ronda: menús con aire de Pixar (2026-10-25)

Isidro: el menú de inicio y el de ajustes «se sienten muy pesados y con una textura poco estilo Pixar».

- Fuera la tarjeta casi negra con borde dorado que brillaba, la letra con serifa y las sombras duras. Ahora: paneles blancos translúcidos con sombras suaves, letra redondeada (Fredoka para títulos y botones, Nunito para el texto, de Google Fonts), botón grande naranja de caramelo con su canto, botones pequeños en pastilla blanca, selección en azul.
- Inicio como panel inferior: logo de dibujos arriba (MAGA en rojo, TACO DASH en azul, contorno blanco, flotando) y el presidente de cuerpo entero saludando en medio (cámara del menú más lejos y mirando más abajo). Misiones compactas de una línea.
- La zona del sin fin sale ahora al pulsar «Sin fin» (antes cargaba el inicio). Ajustes con cada opción en su tarjeta con icono, deslizadores naranjas, selectores redondeados de idioma y gráficos, y «Borrar progreso» discreto abajo.
- Pantalla de carga clara (cielo) en vez de casi negra. Fin de partida, mapa y nivel superado cambian a juego.

### Cuadragésimo quinta ronda: modo historia en orden y frases como ataques (2026-10-25)

Isidro: siguiendo la lógica de AlienZ, que no se pueda elegir nivel (en orden; los superados se repiten); pidió proponer un modo historia. Le gustó la propuesta (el Burrito-Bot roba la receta del taco; cinco ingredientes) pero quiso que fuera también una carrera hacia la presidencia «contando mentiras», con el protagonista lanzando frases como «¡Fake news!» y «¡China! ¡China!», elegidas por mí y que sean muy divertidas.

- Historia «Rumbo a la Casa Blanca»: carrera a la presidencia contra el Burrito-Bot, candidato robot «hecho en China»; en cada ciudad un mitin y un ingrediente (🫓 Nueva York, 🌽 Ohio, 🌶️ Arizona, 🥫 Las Vegas —debate con el Burrito-Bot—, 🏛️ Washington). Cada nivel trae su frase en el mapa (`historia` en levels.js, en los dos idiomas).
- Bloqueo (`nivelAbierto` en levels.js): el 1 siempre; cada uno, si se superó el anterior (llegar al final, sin contar estrellas); los superados, siempre. Washington queda abierto mientras no exista el nivel 1 (lo decidió él). En el mapa, candados y el autobús en el nivel abierto más avanzado.
- Sin fin con candado hasta superar el nivel 1 entero: botón «🔒 Sin fin» y aviso «Pasa el nivel 1 (Quinta Avenida) para desbloquear el Sin fin». La zona se elige al abrirlo.
- Frases: micrófonos dorados por la pista (hasta 3; se empieza con 1). Un toque corto en la pantalla (o F / Intro) lanza un bocadillo enorme que vuela por el carril y tumba lo primero que pilla (+3 tacos). La frase depende del blanco: furgoneta «¡FAKE NEWS!», patrulla «¡CAZA DE BRUJAS!», guardaespaldas «¡ESTÁS DESPEDIDO!», barricada y conos «¡TOTAL DESASTRE!», pancarta y globos «¡TRISTE!», barril «¡HECHO EN CHINA!», el Burrito-Bot «¡CHINA! ¡CHINA!» (cuenta como golpe); sin nada delante, «¡CRÉEME!», «¡ENORME!», «¡COVFEFE!» o «¡NADIE LO HACE MEJOR!». En inglés, las originales.
- Comprobado: candados en el mapa y en Sin fin; la frase gasta el micrófono y tumba la furgoneta sin choque.
- Siguiente: el nivel 1, Quinta Avenida (lo eligió él). Pendiente: voces de las frases.

### Cuadragésimo sexta ronda: nivel 1 Quinta Avenida, y lo que no le gustaba de todo el juego (2026-10-25)

Pidió el nivel 1. A mitad de trabajo añadió: los objetos y el fondo aparecen de golpe; no quiere que cambie de golpe de un mapa a otro (mapas separados); el suelo parece estático con un efecto que hace que parezca que avanza; el público son «Playmobils sin alma»; todo más estilo Pixar; calles no genéricas, cada edificio único y siempre en el mismo punto. Público: lo quiso en Blender, gratis (no Meshy).

- Suelo: calzada, aceras y suelo eran láminas quietas (solo pasaban las rayas). Ahora cada textura se desplaza lo mismo que la pista, y en los niveles hay pasos de cebra en cada cruce real y tapas de alcantarilla junto al bordillo (`sueloDeNivel`), siempre en su sitio.
- Nada de golpe: las cosas nacen en z = -280 (antes -128), cámara hasta 320, niebla 130-285 y el tercio bajo del cielo del mismo color que la niebla: lo lejano sale de la bruma en vez de recortarse.
- Mapas separados: el Sin fin en «Auto» sortea una sola zona por partida (antes rotaba cada 260 m).
- Edificios únicos: `blender/kit.py` (17 piezas en blanco: 3 bajos, 6 tipos de planta, 3 cornisas, 4 remates y el toldo, menos de 1 MB) y `www/src/edificios.js` monta con ellas un edificio distinto por solar —plantas, estilo, color, toldos y rótulo de tienda— con una semilla que sale del sitio que ocupa: siempre el mismo edificio en el mismo punto. En las listas de los niveles, `["kit", N]`.
- Público: `blender/publico.py`, seis personas de una pieza con cara (ojos con brillo, cejas, nariz, sonrisa), pelo y ropa —ejecutivo, señora con banderita, niño con globo, abuelo con gorra roja y cartel «USA!», turista con cámara y seguidora con gorra—, unos 2.100 triángulos cada una, con el brazo derecho aparte: saludan, botan y se animan más al pasar el jugador. Menos gente por grupo y sin gradas.
- Nivel 1 (`blender/nueva_york.py`, levels.js): bajando por la Quinta Avenida desde la calle 56, luz de mañana. Izquierda (este): Trump Tower, St. Regis, catedral de San Patricio, Saks, Madison Square Park. Derecha (oeste): Peninsula, Santo Tomás, Rockefeller Center con Atlas y los jardines, Biblioteca Pública con los leones, Empire State. Entre medias, cuadras de cuatro edificios únicos del kit. Al final, el Flatiron con un camión de tacos: se planta delante, saluda y sale «¡Tortilla recuperada! 🫓». Sin autobuses ni patrullas; imán, escudo, turbo y micrófonos. Largo 3200.
- Desbloqueo: un nivel se abre al pasar todos los anteriores que ya existen (al pasar Nueva York se abre Washington mientras falten el 2, el 3 y el 4). Pasar el 1 abre el Sin fin. Comprobado.
- Medido en la Quinta Avenida: 3.689 llamadas de dibujo y 687.000 triángulos (más por ver el doble de lejos). Falta probarlo en el móvil.

### Revisión a fondo y arreglos (2026-10-27)

Isidro pidió revisar todo el juego a fondo («los niveles no sé cuándo acaban, son muy repetitivos») y, tras leer la revisión, «arregla todo esto».

- **Meta visible**: barra de progreso arriba con los edificios famosos (`hitos` en levels.js), la bandera del punto de control, la meta y un taco que avanza; debajo, «Faltan X m». En el sin fin, los metros de siempre.
- **Niveles por tramos** (`tramos` en levels.js, `PATRONES` en world.js): calma, suave/mixto, vallas (filas enteras que saltar o pasar agachado), slalom (el carril libre cambia de uno en uno), autobuses seguidos, festín (potenciador seguro y lluvia de tacos), lo de cada ciudad (obras en Nueva York, desfile en Findlay, comitiva en Washington), jefe y sprint final. Cada tramo con nombre sale en un cartel al entrar. Cada fila tiene la semilla de su metro: el mismo nivel siempre es igual, también al seguir desde el control. El sin fin encadena tramos al azar.
- **Obstáculos de cada ciudad** (`blender/obstaculos2.py`, 45 s): taxi, alcantarilla con vapor, andamio «POST NO BILLS», contenedor de escombros; pacas de paja, tractor, carroza con mazorca gigante, pancarta «FLAG CITY USA»; valla metálica, manifestantes con «BURRITO-BOT 2028», agentes del Servicio Secreto y todoterreno de la comitiva (viene de frente con luces). Vallas de policía y verja negra delante del público.
- **Punto de control** a mitad (arco hinchable «PUNTO DE CONTROL»). **Al chocar**: se cae de espaldas; pantalla propia del nivel («Te faltaban X m para el Flatiron», la barra), seguir allí pagando tacos (300, luego el doble), desde el control o desde el principio. Sin confeti al perder. Sin fin: «¡Fin de la carrera!» con seguir pagando.
- **Estrellas** = objetivos: llegar, sin chocar ni una vez y las 3 chapas de campaña escondidas (en arco sobre vallas, detrás de un obstáculo o en el techo de un autobús). Se suman entre intentos. Las estrellas antiguas (por tacos) cuentan como «llegar».
- **Velocidad** según lo recorrido (13 → 20/21,5/23), un 8 % más en el sprint: unos 3 minutos por nivel. **Pausa** con botón (sustituye a «EN») y sola al salir de la app; 3-2-1 al volver. **Gestos** al mover el dedo, sin esperar a levantarlo. **Tutorial** en el nivel 1 hasta pasarlo.
- **Burrito-Bot en los niveles**: huye con la tortilla al empezar Nueva York, y pelea en Findlay y en Washington (se va al acabar su tramo).
- **Misiones** solo posibles: antes de pasar Nueva York, solo tacos, metros, saltos y agacharse. **Mapa**: etiquetas sin montarse, Las Vegas → Washington en avión, anillo en la parada actual, objetivos de cada nivel y la nota del atajo a Washington.
- **Tienda**: gorras (roja, vaquero, chistera, corona) que van en la cabeza del presidente y trajes que se tiñen (negro, rojo, blanco, dorado), con el presidente probándoselo detrás del panel.
- **Un solo estilo**: sin contorno negro en nada; horizonte pintado por sitio (`horizonte.js`: Manhattan, campos y silos de Ohio, Washington con el obelisco, mesetas, colinas) en vez de las montañas de conos; nubes blancas y altas; banderas de EE. UU. pintadas; sin banderines sueltos ni líneas amarillas fuera de la acera; público distinto en cada sitio (y nadie en el desierto); pegatinas 2D (taco, chapa, tortilla, maíz, taco perfecto: `pegatinas.js`) e iconos propios (`iconos.js`) en vez de emojis; menú con la calle detrás del presidente.
- **Sonido**: efectos con capas en vez de pitidos, una canción por nivel (swing en Nueva York, country en Ohio, marcha en Washington, pop en el sin fin) y **voz del presidente** en castellano (`herramientas/voces.mjs`, con Piper de AlienZ: 35 frases, 242 KB en `www/voces/`). En inglés, sin voz.
- **Rendimiento**: de ~2.000 llamadas de dibujo a 520-620 (sin contornos ni montañas, rayas de carril en una pieza, un dibujo por taco, edificios del kit juntados por material y soltados al quitarlos).
- Comprobado con un piloto automático (`?prueba`: `__juego.accion`, `sinDibujar`): los tres niveles y el sin fin se recorren enteros, con sus tramos, el jefe y el punto de control.
- Pendiente: las fuentes Fredoka y Nunito siguen viniendo de Google (sin internet, la letra del sistema); bajarlas necesita su permiso. El ranking mundial sigue oculto (necesita servidor). Las caras de Meshy no tienen gestos.

### Nivel 3: Central Avenue de Phoenix, y lo que faltaba (2026-10-27)

Isidro: «¿Falta algo más? Si es así, continúa». Para el nivel 3 dijo que la gira va a la capital o a la ciudad más famosa de cada estado (lista en `GIRA.md`), con obstáculos que se irán desvelando; final en un diner de carretera y luz de tarde dorada. Dio permiso para bajar las letras de los menús y una voz en inglés.

- **Nivel 3, Phoenix** (`blender/phoenix.py`, levels.js): subiendo por Central Avenue. Hotel San Carlos con su letrero en el tejado, la torre Westward Ho con la antena roja, la biblioteca Burton Barr de cobre, el museo de arte y el Museo Heard (colonial, con torre de azulejo). Palmeras y saguaros en maceta en la acera, kit con estilo `desierto` (estuco cálido), horizonte con South Mountain y Camelback, luz `tarde`. Obstáculos nuevos: nopales, rodadoras que vienen rodando, saguaros, camioneta de los 50 y arco de neón «PHOENIX». Tramos propios: «¡Tormenta de rodadoras!» y dos persecuciones de la policía (coches de frente, luces rojas y azules por los bordes y sirena). Final `parada` en el diner de acero con un chile gigante en el tejado; sale «¡Chile recuperado!». Canción del Oeste.
- Los coches que vienen de frente (patrulla, comitiva de Washington) casi no salían: miraban toda la calle visible; ahora solo el trozo que alcanzan.
- Autobús de campaña con techo de bandera y trasera con detalles (antes una caja gris); receta del taco perfecto en el mapa (pegatinas nuevas de chile y salsa); el primer tramo ya no tapa el cartel del nivel.
- Letras Fredoka y Nunito dentro del juego (`www/fonts/`, 69 KB, licencia OFL): ya no dependen de internet. Voz en inglés (Piper `en_US-ryan-medium`, 63 MB fuera de git): las 40 frases en los dos idiomas.
- Washington ahora pide pasar Phoenix (el atajo dice que solo falta Las Vegas).
- Pendiente: el nivel 4, Las Vegas.

## Ideas de Subway Surfers y repaso (2026-10-28)

Isidro: «sigue buscando fallos… revisa Subway Surfers y juegos del mismo estilo
para copiar ideas que encajen». Lo que entra:

- **Tropezón** (el revisor de Subway Surfers): darse de lado contra algo al
  cambiar de carril ya no acaba la carrera. Rebota al carril de antes, pierde la
  racha y le sigue un coche de policía del nivel (patrulla o todoterreno, con
  luces y sirena) 7 s. Si vuelve a tropezar mientras, le pillan. De frente sigue
  siendo chocar. Al pagar para seguir, la policía se va.
- **Caída rápida**: deslizar hacia abajo en el aire baja de golpe y rueda al
  tocar suelo. Y ya no se pierden toques: un salto pulsado justo antes de
  aterrizar salta al caer, se puede saltar estando agachado y un instante
  después de caer del techo del autobús.
- **Botas Saltarinas** (las súper zapatillas): 10 s de saltos de 2,9 m, por
  encima de los coches. Desde Ohio y en el sin fin. Modelo en
  `blender/obstaculos.py` (botas).
- **Caja sorpresa**: una por nivel en un sitio fijo antes del punto de control
  (NY 1100 m, Findlay 1000, Phoenix 1150, Washington 950) y hasta dos en el sin
  fin. Se guarda al cogerla y se abre al acabar con una ruleta como la de las
  cajas de AlienZ: tacos (50 a 1500) o una prenda de la tienda. Si quedan sin
  abrir, hay botón en el menú. `src/cajas.js`, modelo `caja_sorpresa`.
- **Premio del día**: siete días seguidos con premio que crece (50 → 400 y el
  séptimo una caja + 500); si se salta un día, vuelve al primero.
- Repaso: los textos de fin de nivel aún llevaban emojis en el bocadillo.

## La historia de los 50 estados, aplicada (2026-10-28)

Isidro aprobó `HISTORIA.md` («aplícalo y ya cambiaremos si algo no quedó bien»).

- **Orden**: 51 paradas (`src/historia.js`), una por estado, y Washington la
  última (antes era la 5). `levels.js` solo guarda las calles hechas; las demás
  salen con candado. Washington sigue abierta al pasar Phoenix, como «avance del
  final».
- **Mapa**: los 50 estados y D.C. en casillas (en el móvil se ven igual Texas
  que Rhode Island). Ganado = rojo, más intenso con más estrellas; punto negro
  en los niveles con jefe. Debajo, los votos electorales (x/538, marca en 270).
- **Prólogo** de 4 pantallas la primera vez que se abre el mapa (el mote
  «TACO», el taco bowl, la Liga del Pantano, tacos = votantes); se repite con
  el botón «Historia».
- **Al ganar**: bocadillo «¡Arizona vota rojo!», la urna encima de la cabeza
  (en la Casa Blanca, el taco bowl), tipo de victoria por estrellas (por los
  pelos / clara / aplastante), «+11 votos electorales» y un mensaje del
  Candidato como en su red social.
- Fuera los ingredientes del taco. En Washington el Burrito-Bot viene mandado
  por la Liga del Pantano (falta el Monstruo del Pantano de verdad).

## Nivel 4: el Strip de Las Vegas, el debate (2026-10-29)

Isidro: «sigue con el nivel de Las Vegas: el debate contra el Burrito-Bot».
Eligió final en la torre dorada del hotel Trump, luz de anochecer con los
neones encendidos y ganar el debate con micrófonos.

- **La calle** (`blender/vegas.py`): subiendo por el Strip desde el cartel
  «Welcome to Fabulous Las Vegas». A la izquierda, la pirámide negra con su rayo
  de luz y la esfinge, el castillo de torres de colores, el lago de las fuentes
  y el palacio romano; a la derecha, la torre Eiffel encendida con el globo, la
  noria gigante y el campanario de Venecia con su góndola. Sin nombres de
  casinos en los letreros. El resto son hoteles del kit con estilo `vegas`
  (claros, con rótulos de neón y un letrero grande en el tejado). Horizonte con
  las montañas moradas, la ciudad encendida y la torre STRAT.
- **Luces que brillan solas**: `luz()` y `ventanas_luz()` en `comun.py`
  hornean una segunda textura (la de luz) que en el juego va de emisiva
  (`models.js`). Todo fijo: nada parpadea (se marea).
- **Luz `anochecer`**: cielo morado arriba y rosa abajo, bruma malva, sol bajo y
  rosado. Música de orquesta de casino.
- **Obstáculos nuevos**: dados gigantes que vienen rodando (tramo «¡Lluvia de
  dados!»), fichas de casino, tragaperras con el JACKPOT encendido, limusinas
  blancas (tramo «¡Atasco de limusinas!») y la marquesina «DEBATE» (se pasa
  agachado).
- **El debate**: el Burrito-Bot llega subido a su atril (rojo, con las
  estrellas y «2028»). En vez de chiles salen micrófonos: cada uno que coges le
  lanza una frase («¡La marioneta eres tú!», «¡Falso!», «¡Qué robot tan
  desagradable!», «¡Fake news!», «¡Hecho en China!»; las dos primeras las dijo
  de verdad en el debate de Las Vegas de 2016). La barra del jefe es la
  encuesta: empieza 50-50 y cada frase sube un 10 %. Al vencerlo: «¡Hecho en
  China, roto en América!».
- **Final** `parada` en la alfombra roja del hotel Trump (marquesina dorada con
  las letras encendidas, banderas, fuentes y palmeras), con cámara propia
  (`camaraFinal`) que mira hacia arriba para que se vea la torre.
- Voces: 15 frases nuevas en cada idioma (`herramientas/voces.mjs`, que fallaba
  desde la historia nueva porque leía `levels.js`).
- Washington ahora pide pasar también Las Vegas.
- Comprobado con el piloto automático: el nivel entero, los tramos y obstáculos
  nuevos, el debate (encuesta del 50 al 100 %) y el final («¡Nevada vota rojo!»,
  +6 votos). Pendiente: su veredicto en el móvil.

## Mapas vivos y más bonitos (2026-10-31)

Isidro: «dime qué más pondrías y qué cambiarías, mejora la estética y haz que
los mapas sean más dinámicos». De la lista que se le propuso eligió seis cosas
(dejó para otro día que el cielo cambie al correr y los tacos en 3D).

- **Vida en la calle** (world.js, «Los mapas vivos»): gente que anda por las
  aceras, detrás del público (las figuras del público, con paso y brazos);
  coches que cruzan por los cruces, siempre a más de 100 m del jugador, para
  que no parezcan obstáculos; palomas en la acera que salen volando al llegar.
- **Helicóptero de la tele de las Fake News** (`blender/obstaculos2.py`,
  `helicoptero`): dos veces por nivel (nunca en el jefe, el tutorial ni el
  sprint) viene por detrás, se queda grabando delante a la derecha y se va; el
  presidente le suelta «¡FAKE NEWS!». Palas como un disco borroso que gira
  despacio (sin parpadeo). De noche, con el haz del foco apuntándole.
- **Monumentos y árboles**: la rueda de la noria va aparte (`noria_rueda`) y
  gira; los chorros de las fuentes los pone el juego y suben y bajan en ola;
  los árboles y palmeras de la acera se mecen un poco.
- **Halos**: un brillo suave en neones, bombillas y farolas, todo en un dibujo
  por pieza. Blender apunta dónde brilla cada pieza sin hornear
  (`blender … -- --luces` → `models/<carpeta>/luces.json`). Solo de noche
  (Las Vegas) y, más flojo, al atardecer (las farolas de Washington).
- **Calle con más detalle**: parches de asfalto, manchas de aceite y charcos
  que reflejan el cielo (en Phoenix no, es el desierto), y la sombra de los
  edificios del lado del sol sobre su acera. Solo la acera: las sombras que
  cruzan la calzada hacen rayas al correr, y eso marea.
- **Las Vegas con más contraste**: cielo y bruma más oscuros, luz más baja.
- Coste medido contra la versión anterior en Las Vegas: de 640 a 697 dibujos
  por fotograma y unos 0,2 ms más de cálculo. Las palomas se dejaron en tres
  piezas cada una.
- Comprobado con el piloto automático: los cinco niveles enteros, sin errores,
  con el helicóptero dos veces en cada uno. Pendiente: su veredicto en el móvil.

## Cada mapa con sus obstáculos, y su voz de verdad (2026-10-31)

Isidro: «falta que los obstáculos sean diferentes en cada mapa, algunos se
pueden mantener, pero quiero que los mapas se sientan diferentes y más
dinámicos; las voces a veces no se entienden, busca las frases originales de
Trump y ponlas». Para las voces eligió «su voz de verdad» y dio permiso para
bajar whisper.cpp, su modelo de inglés y seis grabaciones de Commons.

- **Obstáculos por mapa** (`blender/obstaculos2.py`, levels.js): fuera conos,
  barricadas, pancartas y globos de todos los mapas (los globos se quedan en
  el desfile de Findlay y los conos en las obras de Nueva York). Solo la
  furgoneta de las Fake News sale en todos, porque es de la historia.
  - Nueva York: bolsas de basura, viga de grúa que se balancea un poco,
    carrito de perritos y repartidores en bici que vienen de frente (tramo
    «¡Repartidores a toda pastilla!», en lugar de «Hora punta»).
  - Findlay: calabazas y vacas. En su tramo («¡Vacas sueltas!») cruzan la
    calle y se paran en el centro de un carril antes de llegar al jugador.
  - Phoenix: calavera de vaca y el cartel de la autopista I-10.
  - Las Vegas: imitador de Elvis que baila.
  - Washington: cajas de papeles «TOP SECRET».
  - El modo sin fin usa los mismos por zona.
- **Su voz de verdad**: 18 frases suyas, en inglés, de grabaciones de dominio
  público (Voice of America y la Casa Blanca; ver `www/voces/LEEME.txt`):
  «This is fake news!», «It's a witch hunt and it's a disgrace!», «America
  first!», «We will make America great again!», «Tremendous!»… En castellano
  sale la traducción debajo, en el bocadillo del micrófono y en el de arriba.
  - Cómo se hizo: Blender pasa el audio a WAV (no hay FFmpeg en este PC),
    whisper.cpp dice dónde va cada palabra (`herramientas/_trump/`, fuera de
    git) y `herramientas/trump.mjs` corta y comprueba cada trozo con whisper.
  - Los tiempos se repasaron a mano (`herramientas/trump-tiempos.json`): en la
    investidura whisper se retrasaba hasta 3 s.
  - Se quitaron dos frases demasiado largas, porque las dijo muy despacio y
    con aplausos: «This American carnage…» y «Now arrives the hour of action».
  - Faltan «You're fired» (es de la tele), «Covfefe» y «Sad!» (solo los
    escribió). «Witch hunt» es la que peor se entiende: es una grabación al
    aire libre.
- Comprobado con el piloto automático: los cinco niveles enteros, sin
  errores, cada uno con sus obstáculos; las vacas cruzan y cerca del jugador
  siempre están en un carril. Pendiente: su veredicto en el móvil, y Des
  Moines (en pausa).

## Nivel 5: Des Moines, el caucus de Iowa (2026-11-01)

Isidro pidió seguir con Des Moines y eligió:
- **Final en el Capitolio dorado**: la cúpula de oro con su linterna y las
  cuatro cúpulas pequeñas de cobre verde con nervios dorados, como el de
  verdad, en lo alto de su colina nevada. El presidente se para al pie de la
  escalinata y la cámara mira hacia la cúpula.
- **Mañana de invierno**: el caucus de Iowa es en enero. Cielo frío y limpio,
  nieve en las aceras, los tejados y los árboles sin hojas, y nieve que cae
  despacio (copos grandes y pocos, sin brillos ni parpadeos: se marea).
- **Los cuatro tramos**: «¡Montañas de soja!» (un carril cortado que va
  cambiando, sacos para saltar y el tubo de grano por debajo), «¡Cerdos
  sueltos!» (cruzan la calle como las vacas de Findlay, pero se saltan),
  «¡Cosechadoras de frente!» (ocupan dos carriles y vienen hacia ti) y «¡La
  cola del caucus!» (una fila de votantes tapa un carril un buen trecho).
  Antes de la meta, «¡Ventisca!»: montones de nieve y la pancarta del caucus.
- La calle es Locust Street hacia el este, que acaba de verdad en el
  Capitolio: el parque de esculturas, la biblioteca central de cristal y cobre,
  el Hotel Fort Des Moines, la torre de acero corten, 801 Grand (la más alta de
  Iowa) y el antiguo edificio de la biblioteca de 1903 junto al río. Por encima
  de la calle cruzan las pasarelas acristaladas («skywalks») de Des Moines.
  Después del puente sobre el río, el East Village de ladrillo bajo.
- Obstáculos propios: sacos de soja, montaña de soja «FOR SALE · NO CHINA»,
  montón de nieve con la pala, mesa del caucus con la urna, tubo de grano,
  pancarta «IOWA CAUCUS», quitanieves, muñeco de nieve con gorra roja, cerdos,
  cosechadoras y votantes en cola. La furgoneta de las Fake News, como en todos.
- En la acera, un granjero nuevo (chaqueta de cuadros, peto y gorra con
  orejeras) entre el público.
- El helicóptero de la tele sale después del río: por el centro las pasarelas
  lo atravesarían.

## El mapa de la gira, como un mapa electoral (2026-11-02)

Isidro mandó una foto del mapa electoral de EE. UU. (estados rojos y azules con
sus votos) para que el mapa de la gira «se note más». Eligió:

- **Formas de verdad.** Los estados ya no son casillas: salen de us-atlas 3.0.1
  (`states-albers-10m.json`, mapas públicos del censo), convertidos con
  `herramientas/hacer-mapa.cjs` a `www/src/mapa-eeuu.js` (34 KB).
- **Azul los que faltan, rojo los ganados.** Como en las elecciones: todo empieza
  azul y cada estado que ganas se pinta de rojo (más intenso con más estrellas).
  La barra de votos también va de azul a rojo.
- Fondo oscuro como en la tele, el número de votos en cada estado y una leyenda
  («Ganados / Por ganar»).
- Los estados pequeños del noreste (VT, NH, MA, RI, CT, NJ, DE, MD, DC) llevan
  una etiqueta aparte con su raya, para poder tocarlos con el dedo.
- El nivel que toca, con borde dorado y un aro que late; el elegido, con borde
  blanco; los jefes, con su carita al lado del número.

## Las rayas del suelo ya no «van apareciendo» (2026-11-02)

Isidro: «las líneas del suelo van cargando y se ve claramente cómo van
apareciendo; pasa en todos los niveles y con más cosas». Era el asfalto: lleva
un `polygonOffset` (-2/-4) para no parpadear con el suelo de debajo, y ese
ajuste crece con la distancia. De lejos tapaba todo lo que va pintado encima, y
solo se veía a partir de una distancia fija que avanzaba contigo.

- Rayas de carril, pasos de cebra, alcantarillas, sombras de los obstáculos,
  flechas del turbo y la sombra del jugador llevan ahora un ajuste mayor
  (`sobreCalzada()` en world.js, -4/-8): se ven desde el fondo de la calle.
- Las flechas del turbo y la sombra del jugador estaban por debajo del asfalto;
  ahora van encima.
- La cámara pasa de `near` 0.1 a 0.5: el buffer de profundidad es 5 veces más
  preciso de lejos, y el césped y las entradas de las casas (subidos de 6 mm a
  2 cm) ya no se pisan con el suelo.

## El dragón de China (2026-11-03)

Isidro: «me gustaría que hubiera un jefe dragón brillante, y que cuando aparezca
el personaje repita de vez en cuando su frase ¡China!». Eligió:

- **Dónde:** en Des Moines (nivel 5: China ya no compra la soja de Iowa) y en el
  modo sin fin, por turnos con el Burrito-Bot (primero el dragón).
- **Cómo se le gana:** como al robot. Vuela delante y te escupe bolas de fuego que
  caen a tu carril y ruedan hacia ti (se saltan); tú le das con chiles y
  micrófonos. Cinco golpes.
- **Cómo es:** rojo y oro, el dragón del Año Nuevo chino (`blender/dragon.py`):
  cabeza con la mandíbula aparte (se abre al escupir), dieciséis trozos de cuerpo
  que siguen a la cabeza con retraso y ondean, patas y cola. Escamas de Voronoi;
  el oro, los dientes y los ojos llevan luz propia y cada trozo un halo dorado
  fijo: brilla también de día y nada parpadea.
- **La voz:** «CHINA!» con su voz de verdad, cortado de la cena de Estado con Xi
  Jinping (la Casa Blanca, 2026, dominio público; bajada con su permiso, versión
  de 240p). La primera vez a los 2,6 s de llegar y luego cada 6-9 s; también es
  lo que grita con el micrófono contra el dragón y sus bolas de fuego.
- En Des Moines va en lugar de la ventisca, de 2400 a 2900 m. La cola del caucus
  se acortó 150 m (2100-2400) para que la pelea dure unos 20 s, y la tercera
  chapa pasó de 2604 a 2300 m.
- Probado con el piloto automático: le dan los chiles, cae en unos 10 s, grita
  «China» dos veces, se saltan todas las bolas de fuego; en el sin fin salen
  dragón, robot, dragón; el debate de Las Vegas sigue igual.

## Menos tacos, niveles que crecen y voces que no se pisan (2026-11-05)

Isidro: «hay demasiados tacos, se hace monótono; los primeros niveles deben
ser más cortos y luego ir alargándose; muchos objetos son igual; los niveles
se sienten muy iguales; las voces no suenan cuando toca, repiten o no acaban
la locución; haz más dinámicos los modelos». Se midió todo con el piloto
automático y él eligió (tras compararlo con Subway Surfers y Minion Rush):

- **Tacos: tres de cada cuatro fuera.** Antes, 1.700–2.200 por nivel (unos
  10 por segundo). Ahora marcan un camino: un solo carril por fila, en tiras
  de dos filas con un trecho vacío (`TIRA`/`CICLO` en world.js), y el festín
  con dos carriles. Arcos como mucho cada tres filas. **Taco dorado** (vale
  10) arriba de algunos arcos y al final de algunos techos de autobús.
  **Premio al ganar**: 500 + 250 por estrella. Misiones de tacos rebajadas.
- **Largo: de 1,4 a 3,3 km.** Nueva York 1.400 m (1 min 24 s), Findlay 1.700,
  Phoenix 2.000, Las Vegas 2.300, Des Moines 2.600 y Washington 3.300 (unos
  3 min). Las calles se acortaron quitando cuadras del kit, sin tocar los
  monumentos; el río de Des Moines pasa a 1.557 m.
- **Cada nivel con su orden de tramos** (ya no el mismo esqueleto) y un solo
  festín por nivel salvo Washington.
- **Objeto de cada ciudad**: diez por nivel (manzanas, banderas, placas de
  sheriff, fichas, mazorcas y papeletas); los diez dan 300 tacos. Contador
  junto a las chapas y línea propia en la pantalla final; no cuenta para las
  estrellas.
- **Obstáculos repartidos**: salen de una bolsa barajada, así todos salen
  parecido y ninguno más de dos veces seguidas.
- **Más vivos**: algunos coches parados arrancan hacia ti (si la fila sigue
  siendo justa); la gente se balancea, lo que cuelga se mece, las plantas con
  la brisa y las fichas giran. Todo lento: nada tiembla ni parpadea.
- **Voces (director en audio.js)**: nada corta a nada; prioridades (jefe y
  meta, micrófono y «CHINA!», potenciadores, ánimo); 5 s de respiro antes de
  una de ánimo; las de ánimo solo al llegar a x3 y x5; las frases al azar no
  repiten ninguna de las tres últimas; todas se preparan al empezar la
  partida; el globo sale cuando suena y dura lo que la voz.

Pendiente, elegido por él: el momento estrella de cada nivel (en Blender, uno
por uno), dos o tres obstáculos nuevos por ciudad y las animaciones del
presidente con Meshy (enseñarle antes los créditos).

## Los tacos del cohete ya no se quedan en el aire (2026-11-06)

Isidro: «en todos los niveles, cuando se acaba el cohete presidencial se siguen
viendo los tacos en el aire». Al despegar se llenaba de tacos el cielo hasta el
horizonte (280 m) y las filas nuevas eran solo tacos del cielo, pero el vuelo
recorre unos 130 m: el resto se quedaba flotando al aterrizar, encima de una
calle vacía. Ahora:

- La calle se sigue llenando como siempre mientras se vuela (los niveles salen
  iguales con cohete o sin él).
- En el cielo solo hay tacos hasta donde llega el vuelo, menos el último
  segundo y medio.
- Donde se aterriza no queda ningún obstáculo (los autobuses sí, se cae en el techo).
- Al acabar, los que quedasen arriba se van con un destello (`quitarCielo`).

Probado en cinco niveles: ningún choque al aterrizar y ningún taco arriba.

## Obstáculos nuevos que se mueven: Washington (2026-11-06)

Isidro, jugando en Pennsylvania Avenue: «se hacen repetitivos los obstáculos,
faltan más tipos y más dinamismo». Washington solo tenía seis distintos (uno
solo para agacharse). Eligió **cinco nuevos por ciudad** (dos para saltar,
uno para agacharse y dos para esquivar), las **cuatro formas de moverse** y
hacerlo antes que el metro de Nueva York. Modelos en `blender/obstaculos3.py`;
el movimiento, en `moverNuevo` (world.js), y sirve para cualquier ciudad:

- **Cambia de carril**: el intermitente (un brillo ámbar suave) avisa desde
  unos 90 m y se pasa al carril de al lado hacia los 60 m. Nunca a un carril
  con algo en su fila, ni con un coche que venga, ni dejando un coche entre él
  y el jugador en el carril que deja. La furgoneta blanca de siempre y los
  taxis también lo hacen ahora (seis de cada diez).
- **Cruza la calle**: espera en la acera, cruza y se para en su carril antes
  de los 32 m; luego se vuelve a mirarte.
- **Barrera que sube y baja**: el brazo baja, sube y vuelve a bajar despacio
  (ciclo de 4,4 s). Arriba se pasa sin más; abajo se salta.
- **Bota hacia ti**: preparado para las ciudades que lo lleven.

Washington: **micrófonos de la prensa** en su tarima «PRESS» (saltar),
**barrera del control del Servicio Secreto** (sube y baja), **dron de la tele
de las Fake News** a la altura de la cabeza (agacharse), **furgoneta de las
Fake News** con parabólica (cambia de carril) y **turista en Segway** (cruza).
Él eligió los tres primeros; la barrera y el Segway, Claude.

Probado con el piloto automático en todo el nivel: 20 cambios de carril y 19
cruces; ningún choque con las furgonetas que cambian (el piloto mira el
intermitente, como una persona).

## Obstáculos nuevos en las otras cinco ciudades (2026-11-06)

Lo mismo que en Washington: cinco por ciudad, con las cuatro formas de
moverse repartidas. Los eligió Claude; Isidro puede cambiar cualquiera.

| Ciudad | Para saltar | Para agacharse | Para esquivar |
|---|---|---|---|
| Nueva York | boca de riego abierta · balón de baloncesto que viene botando | semáforo colgado | coche de caballos de Central Park (cambia de carril) · paseador con cinco perros (cruza) |
| Findlay | paso a nivel del tren (sube y baja) · pavos escapados (cruzan) | bandera gigante de Flag City | cortacésped con el granjero (cambia de carril) · puesto de limonada |
| Phoenix | serpiente de cascabel · rueda de camión que viene botando | piñata de burro | autocaravana (cambia de carril) · vaquero a caballo (cruza) |
| Las Vegas | ruleta girando · barrera del aparcamiento VALET (sube y baja) | cartel de neón de la capilla de bodas | descapotable rosa de los recién casados (cambia de carril) · bailarinas con plumas (cruzan) |
| Des Moines | bola de nieve que viene rodando · niño en trineo (cruza) | rama nevada con un jilguero | autobús escolar (cambia de carril) · ciervo (cruza) |

También salen en los tramos propios donde pegan: el cortacésped, los pavos
y la bandera en el desfile de Findlay; el coche de caballos en el atasco de
Nueva York; el vaquero entre las rodadoras; el descapotable entre las
limusinas; la piñata y el cartel de bodas en las filas de neones; el ciervo y
el autobús escolar con los cerdos. Las bailarinas no van con los dados (los
dados ruedan y las atravesaban).

**Reglas para que sea justo:**

- **Cambio de carril**: solo si, después, la fila sigue teniendo un carril
  libre al lado del libre de la fila de antes y de la de después (nunca hay que
  cruzar dos carriles de golpe, como en el atasco). Mientras cambia, cuenta en
  los dos carriles. Nunca a un carril con algo cerca o con algo que venga.
- **Lo que cruza** sale de la acera contraria si el camino está libre en su
  fila; si no, de la de su lado (nunca atraviesa otro obstáculo).
- **Lo que bota o rueda** solo viene hacia ti si su carril está libre en los
  60 m de delante; si no, bota en su sitio.

Probado con el piloto en los seis niveles. Nueva York, Findlay, Las Vegas y
Washington: cero choques, con 5–11 cambios de carril y hasta 19 cruces.
Phoenix: un choque (una calavera). Des Moines: solo con la cosechadora, que
ya pasaba antes y el piloto no sabe esquivar.

## Coches que giran de verdad, boca de riego en la acera y salida más viva (2026-11-06)

Isidro, tras jugar: «algunos mapas largos al principio se hacen aburridos, en
NY por ejemplo hay obstáculos mal colocados, los coches giran raro, poco
natural, hay bocas de agua en medio cuando deberían estar en la acera y
tirando agua, anima el agua».

- **Cambio de carril**: antes el coche se deslizaba de lado sin avanzar.
  Ahora arranca, avanza unos 7 m en su sentido mientras se pasa de carril y
  frena; el morro sigue la curva (unos 19°) y gira sobre las ruedas de atrás.
  Los que se ven por detrás (taxi, coche de caballos, autocaravana,
  descapotable, autobús escolar, cortacésped, furgoneta de las Fake News) se
  alejan; la furgoneta de la prensa, que te mira, viene. Pasa por encima de
  los tacos que pilla.
- **Marcha atrás**: el taxi, la camioneta y la limusina se ven por detrás y
  «arrancaban» hacia ti marcha atrás. Ya no arrancan; solo lo hacen los que
  te miran (furgoneta, tractor, quitanieves) y la carroza y el carrito de
  perritos.
- **Boca de riego**: va en el bordillo de la acera, nunca en el carril del
  centro, y el chorro cruza su carril (se salta). El agua corre por el
  chorro, vuelan gotas, salpica al caer y el charco hace ondas; todo suave,
  sin parpadeos.
- **Salida**: la velocidad subía igual en todo el nivel y en Washington casi
  no se notaba en el primer kilómetro. Ahora hace casi la mitad de la subida
  en los primeros 350 m (de 13 a unos 17-18) y el resto poco a poco. La calma
  del principio pasa de 150 m a 70-90 m en los cinco niveles largos.

**Mal colocados** (medidos con el piloto buscando cosas que se meten unas en
otras):

- Dos coches que cambiaban a la vez al mismo carril se encontraban: ahora
  cada uno cuenta hasta dónde llegará el otro.
- Un cambio de carril podía dejar un hueco sin salida (a dos carriles del de
  la fila siguiente, en Las Vegas): ahora desde cualquier carril libre se
  llega a uno libre de la fila de al lado moviéndose uno.
- Lo que bota, rueda o arranca ya no atraviesa potenciadores, chapas ni
  objetos de la ciudad.
- Lo que cruza no pasa por delante de lo que viene rodando o conduciendo:
  espera en la acera y, si a 58 m aún no puede, se queda allí (y no choca).
- Después de una fila cerrada en los tres carriles (vallas, el arco de la
  chapa) la siguiente no lleva obstáculos: a 7 m salía a veces un coche en tu
  carril estando aún en el aire.
- Al empezar cada partida el juego creía que ibas a 17 (o a la velocidad de
  la partida anterior) y los coches que vienen de frente recorrían más calle
  de la prevista: en Washington una escolta atravesaba a los agentes.

Probado con el piloto en los seis niveles: Nueva York, Findlay y Las Vegas
sin choques; en Phoenix, saltos justos (serpiente, calavera); en Des Moines,
la cosechadora de siempre y un ciervo; en Washington, a veces unos agentes
justo después de la escolta (hay hueco, el piloto no lo ve). Entre 1 y 10
cambios de carril por nivel.

## Los chiles se acaban con el jefe (2026-11-06)

Isidro: «cuando el Burrito-Bot está derrotado, los chiles siguen
apareciendo». El tramo del jefe mide unos 600 m y seguía poniendo tacos y
chiles hasta el final aunque el jefe ya se hubiera ido. Ahora, en cuanto se
va (vencido o porque se le acaba el tiempo), los chiles que quedan en la
pista se vuelven tacos y el resto del tramo es calle normal (`jefeSeVa`,
`jefeAcabado` en world.js). Vale también para el dragón de Des Moines.
Probado con el piloto en Findlay, Las Vegas y Des Moines: ningún chile
después del jefe y 37-44 obstáculos normales en lo que queda del tramo.

## Los momentos: algo nuevo cada 20 segundos (2026-11-06)

Isidro: «los mapas no deberían ser tan largos o al menos hay que añadir cosas
para hacerlo menos aburrido los 2 primeros minutos». Medidos con el piloto,
los niveles duran de 1:22 (Nueva York) a 2:49 (Washington). Entre el jefe,
los autobuses y el cohete solo pasaban 2 o 3 cosas que cambiaran el juego.
Le di a elegir entre hacerlos más cortos o meterles más cosas, y eligió «Más
cosas, muchas más, que no sea tan repetitivo». Eligió los doce momentos que
le propuse, uno cada 20 segundos. **El largo de los niveles no cambia.**

Los momentos (world.js, «Los momentos»; las piezas nuevas en
`blender/momentos.py`):

| Momento | Qué pasa | Dónde |
|---|---|---|
| Rampa gigante | Tres rampas: lanzan unos 2,8 s por el aire (sube 6 m) por un arco de tacos | Phoenix, Washington |
| Convoy | Camiones (y algún autobús) escalonados en los tres carriles: se corre por los techos | Las Vegas, Des Moines |
| Te persiguen | Algo te sigue por detrás todo el tramo; si tropiezas, te pillan | Nueva York (la prensa), Findlay (una vaca), Des Moines (la cosechadora) |
| Vehículo | Te subes 10 s: va un 20 % más rápido y arrolla todo | Findlay (carroza), Phoenix (carrito de golf), Las Vegas (descapotable), Des Moines (tractor), Washington (limusina) |
| Lluvia de tacos | Pasa el avión presidencial y los tacos caen del cielo, con su sombra en el suelo | Nueva York, Des Moines, Washington |
| Reto relámpago | «25 tacos en 10 segundos», con barra y cuenta atrás; premio de 100 tacos | Las Vegas, Des Moines, Washington |
| Alfombra roja | Va cambiando de carril, con tacos de oro (valen 5); algo encima te echa antes de cada cambio | Las Vegas, Washington |
| Elige tu premio | Tres arcos, uno por carril, cada uno con un potenciador distinto | Findlay, Las Vegas, Washington |
| Jefe de paso | El Burrito-Bot tira tres barriles y se va (sin barra ni chiles) | Nueva York, Phoenix |
| Desfile que cruza | Cada 21 m cruzan dos y dejan un hueco, siempre en el carril de al lado | Phoenix (vaqueros), Des Moines (ciervos), Washington (Segway) |
| Fans con gorras | La gente de la acera lanza gorras doradas con «x2»: tacos dobles 6 s | Las Vegas, Des Moines, Washington |
| Momento estrella | Uno grande por ciudad. Falta hacerlo; el primero es el metro de Nueva York | — |

Cómo va por dentro:
- Los que cambian la calle son tramos con su patrón: `rampa`, `convoy`,
  `lluvia`, `alfombra`, `premios`, `desfile_cruza` y `jefe_paso`.
- Los que van encima del tramo de la ciudad llevan `momento` en el tramo:
  `persigue`, `vehiculo`, `gorras` y `reto`.
- Las chapas que caían dentro de un convoy o de la alfombra se han movido.
  Los objetos de la ciudad no salen en esos tramos (`sitiosObjetos`).
- El punto de control de Findlay pasa de 680 a 720: quedaba pegado detrás de
  los arcos de premio.
- Contra el mareo:
  - en el convoy la cámara se queda a la altura de los techos;
  - la alfombra es lisa, sin rayas finas;
  - los perseguidores altos van más atrás, para que no tapen al personaje.

Probado con el piloto en los seis niveles: ningún choque dentro de los
momentos. Quedan los fallos de siempre del piloto: la cosechadora de Des
Moines y alguna barrera.

## Las Vegas, más clara (2026-11-06)

Isidro: «el mapa de las Vegas es algo oscuro, cuesta ver los obstáculos». El
sol del anochecer venía de delante, así que la cara de cada obstáculo que mira
al jugador quedaba a oscuras sobre una calzada también oscura. Ahora:
- una luz suave por detrás de la cámara (`fill`) ilumina esas caras;
- el relleno del cielo (`hemi`) es más claro;
- la calzada es algo más clara.

El cielo morado y los neones no cambian. Medido en la parte de la calle de la
pantalla, el brillo sube de 49 a 79; el de Nueva York es 112 y el de
Washington, 100.

## El metro de Nueva York, el momento estrella del nivel 1 (2026-11-07)

Lo que eligió Isidro: primero se corre por las vías y luego por el techo del
tren; va junto a la biblioteca, en la estación 5 Av; estación antigua; se entra
por una boca a ras de calle. Ocupa el sitio de las obras y el festín, y el
nivel sigue midiendo 1.400 m.

**La calle** (`blender/metro.py`, carpeta nueva_york; van en `fondo` como
piezas que cruzan la calle):

| Metros | Pieza |
|---|---|
| 772 | La boca: fachada de piedra justo después de la biblioteca, «SUBWAY» con el 7 morado, «5 AV» en mosaico y las farolas de globo verde |
| 780–828 | Dos trozos de túnel: hormigón, pilares negros, cables y lámparas |
| 828–978 | La estación 5 Av: andenes con el borde amarillo, azulejo blanco, la franja granate con «5 AV», dos filas de columnas verdes, bancos, carteles colgados y lámparas cálidas. Techo a 11 m |
| 978–1074 | Cuatro trozos de túnel |
| 1074 | La salida, con la luz del día al fondo |

Las paredes de la estación van a 8,3 m del centro: lo que sobresale de las
fachadas (toldos, escalones) llega hasta 8,5.

**Lo que se juega:**
- **Las vías (780–930).** Una de las vías de los lados es la de los trenes
  plateados que vienen de frente con los faros encendidos: salen tres y te los
  cruzas a unos 805, 826 y 847 m. En las otras dos vías, cada 14 m, torniquetes
  (se saltan), carteles colgados (se pasan agachado) o vagones parados con
  rampa (techo a 2,2 m, con tacos encima).
- **El techo del tren (930–1078).** Tres trenes parados, uno por vía. Se sube
  por la rampa del primer vagón y se corre por los techos unos 100 m, con
  tacos, la chapa del nivel y carteles colgados encima de algún techo. Al
  acabar, se baja a la vía y se sale a la calle.

**Por dentro:**
- La luz pasa poco a poco a la de la estación, cálida y fija
  (`world.factorMetro`, `luzMetro` en main.js).
- La niebla se vuelve oscura al fondo del túnel. Los halos de las lámparas
  brillan aunque el nivel sea de día.
- No se ven la gente, las banderas, los árboles, los letreros ni el
  horizonte de la calle.
- En el techo del tren la cámara se queda a la altura de los techos.
- Cada «autobús» lleva ahora su techo, su rampa y su largo (el vagón es más
  alto y largo que el autobús).
- Lo que va encima de un techo lleva `base`: desde abajo no se toca.
- Lo largo (el tren) desaparece cuando ha pasado entero.
- La chapa que estaba en 880 va ahora en el techo del tren (995). El
  helicóptero sale fuera del metro (420 y 1150).

Probado con el piloto: tres veces seguidas sin chocar, unos 6 s por los techos
y la luz cambia del todo. Los demás niveles siguen igual.

## Los momentos estrella de las otras cinco ciudades (2026-11-07)

Isidro: «Perfecto, hazlos». Eligió uno por ciudad; se hacen de uno en uno y
cada uno se publica al acabarlo (`blender/estrellas.py`):

| Ciudad | Momento estrella |
|---|---|
| Findlay | Túnel de banderas del 4 de julio, por encima de las carrozas del desfile |
| Phoenix | Puente de madera del tren sobre un cañón rojo |
| Las Vegas | Dentro del casino Trump, con lluvia de fichas al salir |
| Des Moines | La Feria del Estado: vaca de mantequilla, puestos, noria y cerdos |
| Washington | Dentro del Capitolio (lo eligió él en lugar de «drenar el pantano») |

### Findlay: el túnel de banderas (80–380 m)

Ocupa el sitio del desfile y de subirse a la carroza.
- Cada 18 m, dos mástiles en las aceras con una bandera gigante colgada sobre
  cada acera. Por encima de la calle van guirnaldas en abanico, a más de
  9,5 m: la cámara pasa por debajo y no por dentro.
- Por el carril del centro, una carroza cada 14 m (`carroza_desfile`: rampa
  detrás y cubierta azul con estrellas a 1,4 m). Se corre por encima saltando
  de una a otra.
- Por los lados, alguna carroza y obstáculos en el suelo; tacos encima de las
  carrozas.
- Cae confeti durante todo el tramo.

Probado con el piloto: 30 carrozas, unos 12 s por encima de ellas, sin choques.

### Las Vegas: dentro del casino Trump (380–550 m) y la lluvia de fichas (550–650)

Ocupa el sitio de los dados y de los premios. Va justo antes de la torre
Eiffel del París: dentro del casino no se vería.
- **La fachada (380):** cruza el Strip, con «TRUMP» en letras de oro gigantes,
  la marquesina de bombillas y una alfombra roja hasta la acera.
- **La sala (388–538):** moqueta roja, filas de tragaperras con pantallas de
  colores sobre una tarima, mesas de ruleta y de cartas, columnas de oro,
  letreros de neón («SLOTS», «777») y lámparas de araña.
- **Por el pasillo:** dados que vienen rodando, tragaperras, ruletas, montones
  de fichas y bailarinas que cruzan.
- **La lluvia de fichas al salir:** fichas de casino que caen del cielo con su
  sombra; cada una vale 5 tacos.

El metro pasa a ser un caso de los interiores (`nivel.interior` = { rango,
tipo }), cada uno con su luz y su niebla. Como Isidro dijo que Las Vegas era
oscura, el casino va más claro que la calle de noche: brillo 61-67 dentro,
78-94 fuera.

Probado con el piloto: sin choques, la luz cambia del todo y caen 44 fichas.

### Washington: dentro del Capitolio (40–208 m)

Ocupa el principio del nivel, antes de la comitiva: la investidura es en el
Capitolio y de ahí se baja por Pennsylvania Avenue.
- **La fachada este (40):** de lado a lado de la calle, con las columnas a los
  lados de la puerta, el frontón y «UNITED STATES CAPITOL».
- **Por dentro:**
  - El Salón de las Estatuas: suelo de mármol, la alfombra roja por el
    centro, estatuas de bronce y de mármol, cuadros y lámparas de araña.
  - La gran rotonda (110–140): sala redonda más alta, con cuadros enormes,
    estatuas alrededor y el medallón dorado en el suelo.
  - Otro tramo de pasillo.
  - La salida oeste a la avenida (200).
- **Por la alfombra:**
  - cordones de terciopelo que se saltan (a veces de lado a lado, con el arco
    de tacos);
  - guardias;
  - la prensa;
  - el dron de la tele;
  - turistas en Segway que cruzan.
- La rotonda es más ancha que la calle: en ese trozo no se ponen los
  edificios (`interior.sinEdificios`).
- La cúpula no está: con la cámara del juego quedaba siempre por encima de lo
  que se ve, y pesaba mucho para el móvil.

**El asfalto que se transparentaba (para todos los interiores).** El asfalto,
las aceras y las rayas llevan un ajuste para verse siempre bien
(polygonOffset). Por eso asomaban por debajo del suelo del metro, del casino y
del Capitolio, como una franja oscura. Ahora dos planos de corte quitan la
calle entre la entrada y la salida de cada interior (`actualizarCorte`), y
dentro tampoco se ponen pasos de cebra ni charcos.

Probado con el piloto: Nueva York, Las Vegas y Washington enteros, sin choques.

### Des Moines: la Feria del Estado de Iowa (440–760 m)

Ocupa el sitio de los cerdos y del tractor.
- **El escenario** (piezas de `fondo`):
  - el arco «IOWA STATE FAIR» con bombillas y taquillas;
  - puestos de comida en las dos aceras (corn dogs, chuletas, limonada,
    buñuelos), con toldos de rayas y nieve;
  - pacas de paja y guirnaldas de bombillas por encima de la calle;
  - carpas de rayas a la izquierda y la noria a la derecha.
- En ese trozo no se ponen edificios (`nivel.sinEdificios`): con ellos, la
  noria quedaba tapada y no parecía un recinto ferial.
- **Por la calle:** pacas, sacos de soja, guirnaldas que se pasan agachado,
  cerdos premiados, carritos de perritos y votantes. Cada 56 m, la vaca de
  mantequilla en su vitrina, en el carril del centro, con tacos a los lados.

Probado con el piloto: sin choques en la feria, salvo uno en la fila de la
chapa (tres obstáculos bajos), que el piloto a veces no salta.

## Jefes más largos, con más ataques y aranceles (2026-11-08)

Isidro: «Los jefes de los niveles duran muy poco además no lanzan ataques
algunos, me gustaría que el dragón rojo lance aranceles y en vez de chili yo
debería lanzar más aranceles». Antes caían en unos 8 s: bastaban 5 golpes y
salían chiles en más de la mitad de las filas. Ahora:
- **12 golpes** en lugar de 5, y el arma sale en el 27 % de las filas (antes
  el 55 %). Pueden quedarse hasta 75 s; si se acaba su tramo, se van.
- **Ataques que van rotando:**
  - **uno**: algo que rueda por tu carril.
  - **dos**: dos a la vez, en tu carril y en uno de al lado; el tercero queda
    libre.
  - **fuego** (el dragón): una bola de fuego a la altura de la cabeza, que se
    pasa agachado.
- **El dragón lanza cajas de aranceles** («TARIFF 125%», ruedan como los
  dados). El robot sigue con sus barriles.
- **Tú lanzas aranceles en lugar de chiles:** un sello rojo y dorado con
  «TARIFF 145%». En el debate de Las Vegas siguen los micrófonos.
- La barra del jefe va con los 12 golpes. En el debate, la encuesta sube
  hasta el 100 %.

Medido con un jugador que va a por los aranceles, cogiendo unos 14-17 de
23-26: los jefes duran de 22 a 30 s y lanzan de 15 a 21 ataques. El piloto no
choca con ninguno.

### Phoenix: el puente sobre el cañón (860–1130 m)

Ocupa el sitio de los neones.
- **El recorrido:**
  - se sale de la ciudad por un camino de tierra entre paredes de roca roja,
    con cactus, calaveras y piedras sueltas;
  - se cruza un puente de madera del tren de 150 m (920–1070), con la vía en
    el carril del centro, barandillas bajas y el caballete de madera hasta el
    río, 46 m más abajo;
  - a los lados quedan el cañón y unas mesetas de roca a lo lejos;
  - se vuelve por otro tramo de roca.
- **En el puente:**
  - agujeros de tablones rotos que se saltan;
  - rodadoras;
  - carteles;
  - vaqueros;
  - la vagoneta de mano que viene de frente por la vía.
- **Por dentro funciona como los interiores**, pero sin cambiar la luz
  (`interior.tipo = "canon"`):
  - no hay calle, edificios ni lo de las aceras;
  - el suelo de alrededor también se corta: bajo el puente se ve el precipicio;
  - la niebla es de polvo anaranjado y lejana.
- **La pared de la otra orilla:** el camino después del puente tiene una
  pared de roca que baja hasta el río. Sin ella, por debajo del borde se veía
  el cielo.

Con esto están los seis momentos estrella. Probado con el piloto en los seis
niveles: se completan todos. Los choques que quedan son los de siempre: el
desfile de vaqueros, la fila de la chapa de Findlay y la cosechadora.

## El final de la Casa Blanca y las armas de cada jefe (2026-11-08)

Isidro: «al llegar a la Casa Blanca el personaje gira de forma poco natural,
¿delante de la Casa Blanca hay una fuente? (si no, corrígela), y la puerta
cuando entra: no se ven las 2. Al Burrito-Bot sí quiero tirarle chiles; al
dragón, aranceles».
- **La fuente se queda:** la hay de verdad, en el jardín norte, el que da a
  Pennsylvania Avenue.
- **El giro:** al rodearla, el personaje iba de lado mirando siempre al
  frente. Ahora mira hacia donde va por la curva del camino.
- **La puerta:** la hoja derecha se cierra dada la vuelta y por detrás no se
  dibujaba. Ahora se ven las dos.
- **Las armas:** chiles para el Burrito-Bot (Findlay, Washington y el sin fin);
  sellos de aranceles para el dragón. En el debate, micrófonos.

## Nivel 6: Omaha, Nebraska (2026-11-08)

Isidro: «haz más mapas, todos los que puedas, con sus respectivos escenarios
y obstáculos, su dinamismo». Para Omaha eligió el final en la antigua
estación art déco y la luz de atardecer en la pradera (`pradera`).
Historia: tierra de vacas, con cajas de Filetes Trump por la calle.

- **La calle** (Farnam Street, 2.700 m, `blender/omaha.py`):
  - la torre del First National (la más alta de Nebraska), la torre Woodmen,
    los almacenes de ladrillo del Old Market con su marquesina de bombillas y
    el teatro Orpheum con su letrero vertical;
  - al fondo, Union Station, con su reloj y los ventanales art déco.
- **Obstáculos nuevos:**
  - cajas de Filetes Trump (se saltan);
  - el rollo de heno que viene rodando;
  - el cartel del asador (agacharse);
  - el camión de ganado, que cambia de carril;
  - el aficionado de los Cornhuskers con su gorro de mazorca, que cruza.
- **Momento estrella, la estampida en los corrales (440–790):**
  - el arco «UNION STOCK YARDS»;
  - vallas con vacas, graneros rojos y pacas;
  - vacas y rollos de heno por la calle;
  - una vaca que te persigue.
- **Momentos**, uno cada 20 s: rampa, premios, camiones de ganado, lluvia de
  tacos, gorras, el coche de caballos del Old Market (vehículo nuevo), jefe de
  paso, convoy, Huskers que cruzan, reto y alfombra roja.
- **Lo demás:**
  - el objeto de la ciudad son filetes;
  - la música es country con banjo;
  - el mensaje al ganar: «Hasta las vacas me quieren».

Probado con el piloto: 2:18, el nivel se completa y todos los obstáculos nuevos
salen.

## Nivel 7: Wichita, Kansas (2026-11-08)

Isidro eligió el final en el Guardián de las Llanuras y la luz de cielo de
tornado (`tornado`: verde gris, sin relámpagos que parpadeen, con la luz de
relleno por detrás para que se vean los obstáculos). Historia: un tornado como
el de El Mago de Oz se lleva las vallas.

- **La calle** (Douglas Avenue, 2.800 m, `blender/wichita.py`):
  - el Epic Center escalonado (la torre más alta de Kansas), Century II
    (redondo, con el tejado azul de gajos) y el museo de la aviación, con una
    avioneta subida a un poste;
  - al fondo, el Guardián de las Llanuras en su roca, con el anillo de
    braseros de fuego.
- **Obstáculos nuevos:**
  - la valla y la vaca que se lleva el tornado: cruzan por el aire, hay que
    agacharse;
  - el trozo de tejado que viene botando;
  - el espantapájaros;
  - la señorita Gulch en bicicleta, con Toto en la cesta, que cambia de carril.
- **El camino de baldosas amarillas (450–620):** de lado a lado de la calle,
  con tacos dorados. Se pinta como la alfombra roja, porque si no el asfalto se
  transparentaba.
- **Momento estrella, el tornado (700–1000):**
  - se sale a la pradera, sin edificios;
  - el embudo gira despacio a la derecha;
  - por la calle vuela de todo.
  - En el horizonte de Kansas también se ve un embudo a lo lejos.
- **Lo demás:**
  - el objeto de la ciudad son los zapatos de rubí de Dorothy;
  - la música es más tensa, en menor;
  - el mensaje al ganar: «no hay sitio como la Casa Blanca».
- **Para el juego en general:** las piezas que cruzan la calle pueden ir
  desplazadas a un lado (`x` en `fondo`).

Probado con el piloto: 2:18, el nivel se completa y salen todos los obstáculos.

## Nivel 8: San Luis, Misuri (08/11/2026)

Isidro: «Aplica todas las preguntas que digas recomendados». Se aplicó lo
recomendado: final bajo el arco Gateway y mañana soleada.

- **Historia:** las etiquetas de precio no paran de crecer (los aranceles).
- **Escenario (`blender/sanluis.py`):** el antiguo juzgado, el estadio de los
  Cardinals, Union Station y, al fondo de la calle, el arco Gateway.
- **Obstáculos nuevos:**
  - la etiqueta de precio gigante, que crece al acercarse (agacharse);
  - el carrito de la compra que viene rodando;
  - las cajas con el precio nuevo;
  - el carro de cerveza con caballos, que cambia de carril (y al que te subes);
  - el aficionado de los Cardinals, que cruza.
- **Momento estrella, el súper de los aranceles (450–800):** se entra en un
  supermercado; el pasillo central es la calle, con estanterías, luz de
  fluorescentes y «PRICES +145%» en las paredes.
- **Final:** el jugador se para delante del arco y la cámara mira hacia arriba
  para verlo entero; sin edificios en el último tramo para que no lo tapen.
- **Lo demás:** el objeto son las etiquetas de precio; la música, un blues de
  San Luis con swing.

Probado con el piloto: 2:25, el nivel se completa y salen todos los obstáculos.

## Nivel 9: Indianápolis, Indiana (08/11/2026)

Se aplicó lo recomendado sin preguntar: final en la meta del circuito y luz de
día de carrera (mediodía).

- **Historia:** «Los coches de carreras no esperan a nadie».
- **Escenario (`blender/indy.py`):** el Monumento a los Soldados y Marineros,
  el Capitolio de Indiana con su cúpula de cobre, el estadio de los Colts y
  el hotel de cristal azul.
- **Obstáculos nuevos:**
  - la pila de neumáticos (se salta);
  - la pancarta de cuadros (agacharse);
  - el mecánico con la rueda, que cruza;
  - el coche de seguridad, que cambia de carril;
  - el coche de carreras (solo en el circuito).
- **Momento estrella, la recta de las 500 millas (2340 hasta la meta):**
  - se entra por la puerta del circuito y la calle pasa a ser la pista,
    entre gradas llenas de público;
  - los coches de carreras van más despacio que el jugador y hay que
    adelantarlos. Cada coche se guarda su carril hasta que lo alcanzas, para
    no atravesar nada, y nunca hay más de dos a la vez.
- **Final:** el jugador se para encima de la franja de ladrillos de la meta;
  la cámara mira la torre Pagoda y la torre de posiciones.
- **Lo demás:**
  - el objeto son las banderas de cuadros;
  - la música es rock de carreras.
- **Para el juego en general:**
  - un interior puede ser «al aire libre» (`aire`): se quita la calle, pero
    no la luz de fuera ni el horizonte;
  - `sinEdificios` puede traer su propio tramo.

Probado con el piloto: 2:21, el nivel se completa y salen todos los obstáculos.

## Nivel 10: Detroit, Míchigan (08/11/2026)

Se aplicó lo recomendado sin preguntar: final delante del Renaissance Center y
luz de tarde.

- **Historia:** «La ciudad del motor, con coches llenos de aranceles. En el
  puente, canadienses enfadados: no quieren ser el estado 51».
- **Escenario (`blender/detroit.py`):** el Spirit of Detroit (la estatua verde
  con la esfera dorada), el teatro Fox con su letrero, el puño de Joe Louis,
  el Guardian Building naranja y, al fondo, el Renaissance Center.
- **Obstáculos nuevos:**
  - el coche con la etiqueta del arancel («+25%»), que a veces arranca hacia ti;
  - el alce;
  - el canadiense enfadado con el palo de hockey y el cartel «NO 51st STATE»,
    que sale de la acera a cortar el paso;
  - el barril de sirope de arce, que viene rodando;
  - la pancarta «NOT FOR SALE» (agacharse).
- **Momento estrella, el puente Ambassador (705–1065):**
  - es un puente colgante con dos torres verdes y el cable que baja hasta el
    centro;
  - se quita la calle y, muy abajo, se ve el río Detroit;
  - por el puente vienen canadienses, alces, pancartas y barriles de sirope.
  - La segunda mitad del puente son los tramos de la primera dados la vuelta
    (`giro` en `fondo`).
- **Lo demás:**
  - el objeto son las botellas de sirope de arce;
  - la música es soul de la Motown.

Probado con el piloto: 2:26, el nivel se completa y salen todos los obstáculos.

## Repaso del 08/11/2026 (tarde): lo que dijo Isidro al probar los niveles nuevos

> «faltan detalles en los mapas, me gustan pero se sienten muy parecidos, cuando
> juego y paso un nivel, al darle a jugar no me envia al último nivel
> disponible [...] mejora el diseño de los animales, las animaciones como
> caminan, los micrófono se ven muy claros [...] los obstáculos que tira el
> burrito bot se hunden en el suelo, falta que tenga sentido la carretera, hay
> coches que se cruzan donde no hay carreteras, añade algun cruce, y haz que el
> personaje tenga que cambiar a otra carretera de vez en cuando, en algunos
> sitios aparecen tuneles o tiendas sin ningún sentido [...] como el circuito»

Se aplicó lo recomendado sin preguntar:

- **Siguiente nivel.** Al ganar sale el botón grande «SIGUIENTE: nombre» y el
  mapa ya trae elegido el siguiente que toca (antes volvía a salir el mismo).
- **El barril del Robot Burrito** giraba sobre su base y medio barril se metía
  en el suelo: ahora gira sobre su eje.
- **Micrófono** (el que se coge en Las Vegas): de verdad, con rejilla de metal
  oscuro, mango negro mate y anillo cromado (`blender/animales.py`).
- **Animales** (`blender/animales.py`): vaca, cerdo, ciervo, alce, pavos y los
  caballos del coche de Central Park y del carro de San Luis.
  - Rehechos con forma de animal: lomo, pecho, cabeza con hocico, ojos con
    brillo, orejas, cola y pelo con algo de textura.
  - Las patas van aparte: el juego (`world.js`, ANDAR) las mueve al paso que
    lleva el animal, y la vaca que te persigue va al galope.
- **Cruces de verdad** (`levels.js`, crucesDeNivel; `world.js`, hacerCruce).
  - Cada hueco entre edificios es una calle lateral con asfalto, paso de
    cebra, stop, raya amarilla, semáforo y letrero verde («1st St»...).
  - Cada dos, la calle sigue también al otro lado (se quita el edificio que
    la tapaba).
  - Los coches solo cruzan en los cruces de cuatro, por su carril, y a veces
    hay uno esperando en el stop.
- **Desvíos** (aplicarGiros): uno o dos por nivel, hacia el 35 % y el 70 %.
  - La calle está cortada por obras y hay vallas «ROAD CLOSED / DETOUR» en
    dos carriles (`blender/calles.py`); también flechas en el suelo y un
    cartel naranja.
  - Hay que ponerse en el carril del giro; al llegar, el cartel verde de la
    calle nueva («OLIVE ST →») tapa la pantalla y ya vas por la otra calle.
  - Findlay y Phoenix no tienen sitio tranquilo para un desvío.
- **Entradas con sentido:**
  - **Súper de San Luis:** un edificio que ocupa la manzana, con escaparates,
    marquesina y puertas de cristal que se abren solas.
  - **Metro de Nueva York:** un edificio de estación de lado a lado, como
    Grand Central.
  - **Circuito de Indianápolis:** el muro del circuito con taquillas y un
    túnel de 30 m bajo las gradas.
- **Más variedad:**
  - Omaha, Wichita, San Luis, Indianápolis y Detroit tienen su estilo de
    edificios: colores, plantas, cornisas, depósitos y tiendas propias.
  - En las aceras hay bancos, buzones, bocas de riego y farolas con bandera.

## Nivel 11: Chicago, Illinois (08/11/2026)

Isidro: «Sigue con Chicago». Se aplicó lo recomendado sin preguntar: final
delante de la Alubia (Cloud Gate, en Millennium Park) y mañana de otoño con
viento.

- **Historia:** «La ciudad del viento: el viento le levanta el tupé».
- **Escenario (`blender/chicago.py`), bajando por Michigan Avenue:**
  - a la izquierda, el John Hancock (la torre negra con las cruces) y la
    Tribune Tower (la torre gótica);
  - a la derecha, la Water Tower (el castillo de piedra en su parque), la torre
    Trump con su nombre en letras de acero y el Wrigley Building (blanco, con
    el reloj);
  - el puente DuSable sobre el río teñido de verde: casetas de piedra en las
    esquinas, banderas de EE. UU. y de Chicago tiesas por el viento, Marina
    City al fondo y un barco de turistas que pasa por debajo;
  - al fondo, Millennium Park y la Alubia, que es un espejo de verdad (refleja
    cielo, ciudad y plaza).
  - El horizonte: el lago Michigan con veleros a la izquierda y la Willis
    Tower delante; las nubes corren más deprisa (hay viento).
- **Obstáculos nuevos:**
  - el paraguas dado la vuelta que cruza volando y dando vueltas;
  - los periódicos que vuelan a la altura de la cabeza (agacharse);
  - la papelera que viene rodando (saltar);
  - el carrito de perritos de Chicago, con el perrito gigante encima;
  - la pila de cajas de pizza de molde hondo (saltar).
- **Momento estrella, la ciudad del viento (1450–1880):**
  - al entrar se le levanta el tupé (un mechón que sube y baja despacio) y
    dice «¡Mi tupé!»;
  - paraguas, periódicos, papeleras, cajas de pizza y carritos, siempre con un
    carril libre;
  - a mitad, un paraguas abierto con los colores de Chicago: si lo coges, el
    viento te lleva por el aire (como el cohete), colgado del paraguas con el
    brazo levantado.
- **Lo demás:**
  - el objeto son los botes de laca (para el tupé);
  - la música es blues de Chicago;
  - los edificios del kit son de la escuela de Chicago (miradores, terracota
    blanca, caliza) con tiendas de pizza, perritos, blues y jazz.

## Cámara que sigue el cambio de carril (09/11/2026)

Isidro: «al cambiar de carril la cámara debería girar directamente, sin cambiar
de ventana, debería seguir para hacerlo más frenético».

- Antes (23/10, contra el mareo) la cámara solo acompañaba la mitad del cambio
  de carril y despacio: el jugador se iba a un lado de la pantalla.
- Ahora la sigue entera y rápido (`dt * 12`), como Subway Surfers: el jugador
  queda siempre en el centro.
- Mientras le alcanza gira un poco hacia él (como mucho 3,4°) y vuelve sola.
  La cámara gira primero y cabecea después (`rotation.order = "YXZ"`), así que
  el horizonte no se tuerce; sigue sin inclinarse (`rotation.z = 0`).

## Carga más rápida al abrir (09/11/2026)

Isidro: «el juego tarda mucho en cargar al inicio».

- La causa: al abrir, la app del móvil preguntaba a GitHub, archivo por archivo
  (unos 240, 23 MB de modelos), si había cambiado. La web, igual: lo pedía
  todo a internet cada vez.
- Ahora GitHub hace al publicar una lista de huellas (`www/huellas.json`, con
  `herramientas/huellas.mjs` en `pages.yml`; no va en git). Al abrir se baja
  solo esa lista y cada archivo sale de lo guardado (o de lo que trae el APK)
  si su huella coincide; solo se baja lo que ha cambiado.
- App: `MainActivity.java` (`pedirHuellas`, al pedir index.html). Hace falta
  instalar el APK nuevo una vez. Sin internet, como antes.
- Web: `sw.js` guarda cada archivo con su huella (caja `taco-dash-archivos`)
  y borra las cajas de versiones viejas. En el PC de pruebas (localhost) sigue
  pidiendo siempre lo último.
- Medido en el PC: la segunda vez, 0 KB descargados y los modelos listos en
  0,7 s (antes 12,8 MB y 3,7 s con fibra).

## La gente de la calle, rehecha (09/11/2026)

Isidro: «la gente mueve el brazo como locas, ¿puedes mejorar la estética de
las personas en general?».

- Antes: todos agitaban el brazo derecho deprisa y sin parar, y botaban.
  Eran bolas y palos sueltos con ojos saltones.
- `blender/publico.py`, rehecho:
  - cuerpo, brazos y piernas de una pieza suave cada uno (modificador de piel
    + subdivisión), proporciones de persona;
  - cara tranquila: ojos pequeños con iris y párpado, cejas, nariz, boca;
  - pelo con volumen;
  - cinco piezas por persona (`_cuerpo`, `_brazo_d/i`, `_pierna_d/i`) con el
    giro en hombro y cadera;
  - once personas: las siete de antes y cuatro nuevas (ejecutiva, obrero,
    estudiante, deportista), que salen en todas las ciudades;
  - unos 4.100 triángulos por persona (antes 2.500, con una pieza menos).
- En el juego (`world.js`, `personaPixar` y `animarPersona`):
  - quietos de lejos, respirando;
  - al pasar el jugador cada uno hace UNA cosa tranquila: aplaudir, saludar
    despacio, ondear su bandera o cartel, o seguirle con la mirada;
  - los que pasean andan de verdad, con las piernas y el brazo contrario;
  - nadie de pie en medio de una calle lateral.

## Nivel 12: Milwaukee (09/11/2026)

Isidro: «sigue creando más estados, aplica tus propias recomendaciones sin
preguntas». Se aplicó lo recomendado: final delante del museo de arte de
Calatrava, junto al lago, y tarde dorada de otoño (luz `dorada`).

- `blender/milwaukee.py`. Wisconsin Avenue hacia el lago (3.050 m):
  - la iglesia del Gesu, el Germania (los cascos de cobre), el Ayuntamiento
    (la torre del reloj), el hotel Pfister y el U.S. Bank Center;
  - el puente sobre el río Milwaukee con almacenes de ladrillo, una barca y
    la estatua del Fonz en el paseo del río;
  - la meta: el puente blanco con el mástil inclinado y el museo; sus alas
    (`ala_museo`, dos piezas) van cerradas y se abren despacio al llegar.
- Obstáculos nuevos: rueda de queso que rueda, cuñas de queso, cubo y bolsas
  de basura, cartel de queso colgado, aficionado con sombrero de queso que
  cruza, moto que cambia de carril y el camión de la basura.
- Momento estrella «basura»: se pone el chaleco reflectante (naranja con dos
  bandas plateadas, pintado en la textura del personaje: `setChaleco` en
  presidente.js; la tripa se busca por la altura porque el esqueleto de Meshy
  la pega a los muslos) y va de pie encima del camión arrollando cubos.
  El chaleco se queda hasta la meta.
- Ciudad «crema» (ladrillo color crema), polka con acordeón, horizonte del
  lago con el puente Hoan y el faro, objeto: cuñas de queso.

## Los vehículos esperan aparcados (09/11/2026)

Isidro: «a veces de golpe el personaje se sube a un coche, tractor o limusina,
pero lo hace sin activar nada, ¿no sería mejor que fuera un elemento que
encuentre en la partida y que ya está ahí, como esperando?». Hecho así:

- Al principio de cada tramo de vehículo, el vehículo está aparcado en el
  carril del medio, con una flecha amarilla que bota encima y una fila de
  tacos que lleva hasta él.
- Solo se sube quien pasa por su carril (también si se cambia a él cuando lo
  tiene al lado): salta por encima de la parte de atrás y cae donde se pisa.
- Quien va por otro carril pasa de largo y sigue el tramo a pie.
- El chaleco de Milwaukee se pone al subir al camión, no al empezar el tramo.

## Nivel 13: Minneapolis (09/11/2026)

Isidro: «sigue creando más estados, aplica tus propias recomendaciones sin
preguntas». Se aplicó lo recomendado: final en el jardín de esculturas (la
cuchara gigante con la cereza, nevado) y un día de invierno de sol y mucho
frío (luz `helada`: cielo azul, todo nevado).

- `blender/minneapolis.py`. Nicollet Mall hasta el jardín (3.150 m):
  - el Ayuntamiento (granito rojo, la torre del reloj), el IDS Center (el
    cristal azul con las esquinas en escalera), la Foshay Tower (el
    obelisco con FOSHAY arriba), el Wells Fargo Center y la basílica de
    Santa María;
  - el lago helado de Loring Park (pieza `lago_helado`, 440 m, va como
    interior al aire libre): tres pistas de hockey con vallas y anuncios de
    los canadienses («SORRY!», «NO TARIFFS», «EH?»), casetas de pesca,
    patinadores y la casa de calentarse;
  - la meta: la cuchara-puente con la cereza, el gallo azul y el Walker.
- Obstáculos nuevos: disco de hockey gigante que viene deslizándose (solo en
  el lago: en las vallas llegaba a la vez que una pancarta), portería,
  jugador canadiense que cruza patinando, pancarta «SORRY, NO TARIFFS»,
  máquina de pulir el hielo y caseta de pesca.
- Momento estrella «hockey»: cruzar el lago por las pistas; al final, la
  portería grande y el gol por el carril libre (+50 tacos y confeti).
- Los paseantes de la acera ya no andan dentro de los interiores (salían
  por el hielo).
- Ciudad de ladrillo rojo y cristal con nieve en los tejados, música de
  órgano de pabellón de hockey, horizonte con el puente de los arcos y el
  silo de la harina; objeto: patines.

## La cámara vuelve a como estaba (09/11/2026, tarde)

Isidro, probando la cámara que seguía entera el cambio de carril y giraba
hacia el jugador (puesta esta mañana): «no me gusta, déjalo como estaba».
Vuelve a la del 23/10: acompaña la mitad del cambio, despacio y sin girar.

## 10/11/2026 — Jefes de cada acto, revisión con Fable, cuenta e instalar

- Isidro: «revisa el juego… añade más jefes y haz el juego más gamberro… la auditoría con Fable». Revisión en tres partes (jugabilidad, textos y menús, mapas); luego pidió pausarla y hacer la cuenta y el botón de instalar.
- Jefes nuevos (blender/jefes.py, tabla `JEFES` en world.js): Rey Pingüino (sellos), los Papeles (rotuladores), el Toro (chiles), el Sentido Común (hamburguesas) y el Monstruo del Pantano (desatascadores), que ya es el jefe final de Washington. Cada uno con lo que rueda (se salta), lo que vuela a la cabeza (agacharse) y sus gritos. En el sin fin salen todos por turnos.
- Más gamberro: excusas al tropezar («¡Eso lo ha puesto Obama!») y títulos al chocar («¡Recuento! Esto no ha pasado»).
- Arreglos de la revisión de textos: el cartel de Wichita salía con el de Chicago (clave repetida), «Colección: 10 …» en vez de «Las 10 filetes», misión «Derrota a {n} jefes», el cartel del tramo ya no se sale en 360 px, el botón SIGUIENTE con la calle debajo, borrar progreso recarga, frases para los obstáculos que no tenían, inglés corregido.
- Cuenta (src/cuenta.js): usuario y contraseña, sin correo, en el Firebase de AlienZ (`tacodash/{uid}`); la partida se sube sola y al entrar se juntan sin perder nada. Falta publicar la regla de Firestore (z-resistance/firestore.rules): el permiso lo tiene que dar Isidro.
- Botón de instalar (src/instalar.js): en Android baja la app (www/descargas/TacoDash.apk), en Chrome del ordenador la ventana de instalar, en iPhone explica Compartir → Añadir a pantalla de inicio. No sale dentro de la app ni si ya está instalada.
- Pendiente de la revisión (pausada): barra del jefe empieza al 42 %, filas imposibles con el jefe del sin fin, obstáculos que ruedan en tramos de vallas, hitos tapados, y los 37 estados (hay tabla y plantillas de Fable).

## 10/11/2026 (2): los líderes de la caja sorpresa (v49)

Isidro: «los premios se sienten muy sosos y sin ningún significado, cámbialas
a nuevos personajes como Netanyahu, Vladimir Putin, Kim Jong-un y presidentes
polémicos del mundo; con Meshy si hace falta, pero si Blender puede, Blender».

- Hechos en Blender (`blender/lideres.py`), no en Meshy: cabeza, pelo y camisa
  propios sobre el cuerpo del muñeco de piezas, así corren con las mismas
  animaciones y no se gastan créditos. Cada uno tiene su retrato
  (`www/models/lideres/<id>.png`), que sale en la ruleta y en la tienda.
- Ocho: Putin y Kim (legendarios), Netanyahu y Xi (épicos), Milei, Maduro,
  Bolsonaro y Erdoğan (raros). Milei lleva motosierra y Kim un misil.
- Cada uno empieza las carreras con su ventaja: imán (Putin, Bolsonaro),
  gigante (Kim), escudo (Netanyahu, Erdoğan), tacos dobles (Xi), botas (Milei),
  turbo (Maduro). Sus frases salen en el globo; con ellos no suena la voz de
  Trump.
- La caja: tacos de relleno y líderes por rareza; el repetido se cambia por
  tacos (800 / 1500 / 3000). La primera caja trae un líder seguro. Las gorras y
  los trajes ya no salen en la caja: siguen en la tienda.
- Se eligen en Tienda → Líderes (el juego se recarga para montarlo). Los
  sombreros y trajes de la tienda son solo para Trump.
