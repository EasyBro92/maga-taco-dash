# Nivel 36: Anchorage, Alaska (15/11/2026).
#
#   blender -b -P blender/anchorage.py -- [pieza ...] [--rapido]
#
# Historia: «Intenta comprar Alaska. Le recuerdan que ya es suya. "Pues compro
#   Groenlandia"». Acto de la Armada Española. Por 4th Avenue en verano (el sol
#   de medianoche), donde sale la carrera de trineos Iditarod: el teatro de la
#   4th Avenue, la cabaña de troncos con el tejado de hierba, el hotel Captain
#   Cook y los alces pintados de las aceras. Trump lleva el cheque gigante de
#   7,2 millones (lo que costó Alaska en 1867): ocupa el carril de al lado y se
#   cambia de lado tocando. El momento estrella: el hidroavión desde el lago
#   Hood por las montañas Chugach (tocar para subir, entre crestas y nubes).
#   Final en la estación del ferrocarril de Alaska, con el cartel SE VENDE
#   GROENLANDIA. Pancartas de España: VALDEZ Y CÓRDOVA SON NOMBRES ESPAÑOLES.
# Obstáculos (carpeta obstaculos): el hidroavión (se monta: es un vehículo), la
# cresta nevada y la nube de tormenta del vuelo, la pancarta y la nasa de los
# cangrejos reales. (Los alces son los de Detroit.)

import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import *

def blanco():    return mat('blanco_anc', 0xf6f4ee, 0.5)
def negro():     return mat('negro_anc', 0x1c1c20, 0.4)
def cristal():   return mat('cristal_anc', 0x3a5a70, 0.15)
def rojo():      return mat('rojo_anc', 0xc8202a, 0.45)
def azul():      return mat('azul_anc', 0x2a4a9a, 0.45)
def amarillo():  return mat('amarillo_anc', 0xf2c21a, 0.45)
def gris():      return mat('gris_anc', 0x8a9098, 0.4)
def hierro():    return mat('hierro_anc', 0x2a2c30, 0.45)
def madera():    return mat('madera_anc', 0x8a5a34, 0.85)
def madera_o():  return mat('madera_oscura_anc', 0x5a3a22, 0.85)
def tronco_m():  return mat_bloques('troncos_anc', 0x9a6a3e, 0x6a4628, ancho=3.0, alto=0.32, grosor=0.03)
def hierba():    return mat('hierba_anc', 0x5a8a3a, 0.9)
def nieve():     return mat('nieve_anc', 0xf4f8fc, 0.6)
def roca():      return mat('roca_anc', 0x6a6a72, 0.9)
def pino():      return mat('pino_anc', 0x2a4a34, 0.85)
def agua():      return mat('agua_anc', 0x3a6a8a, 0.15)
def piel():      return mat('piel_anc', 0xe8b89a, 0.7)

def bandera_es(nombre, z0, alto):
    return mat_franjas(nombre, 0xc8202a, 0xf2c21a, 3, eje='Z', z0=z0, alto=alto)

def abeto(x, y, z, h):
    cil(madera_o(), x, y, z, 0.18 * h / 6, h * 0.25, 6)
    for k in range(3):
        cil(pino(), x, y, z + h * (0.2 + k * 0.22), h * (0.28 - k * 0.07), h * 0.38, 7, r2=0.02)

def flores(x, y, z, n=5):
    for i in range(n):
        esfera([rojo, amarillo, lambda: mat('flor_rosa_anc', 0xe84a9a, 0.5), blanco][i % 4](), x - 0.4 * (n - 1) / 2 + i * 0.4, y, z, 0.2, 1)

# ================================================================ la meta
def estacion_alaska():
    """La estación del ferrocarril de Alaska (la meta): el edificio art déco
    claro con ALASKA RAILROAD, la locomotora amarilla y azul en el andén y,
    delante, el cartel SE VENDE GROENLANDIA y la pancarta de España."""
    Y = 16
    W, D, H = 50.0, 16.0, 10.0
    yf = Y - D / 2
    c = mat_bloques('estuco_anc', 0xe8e0cc, 0xd0c8b4, ancho=1.2, alto=0.6, grosor=0.006)
    caja(c, 0, Y, 0, W, D, H)
    caja(c, 0, Y, H, 18, D - 2, 3.5)
    caja(blanco(), 0, Y, H + 3.5, 18.4, D - 1.6, 0.5)
    for k in range(11):
        x = -22 + k * 4.4
        if abs(x) < 6:
            continue
        ventana(x, 1.5, 1.8, 3.2, y=yf - 0.05, marco=blanco(), cristal=cristal())
        ventana(x, 6.0, 1.6, 2.4, y=yf - 0.05, marco=blanco(), cristal=cristal())
    for x in (-3.5, 0, 3.5):
        caja(cristal(), x, yf - 0.05, 0.4, 2.6, 0.1, 8.0)
        caja(blanco(), x + 1.4, yf - 0.1, 0, 0.4, 0.15, 9.5)
    caja(azul(), 0, yf - 0.2, 10.4, 16, 0.2, 1.8)
    texto(amarillo(), 'ALASKA RAILROAD', 0, yf - 0.32, 10.8, tam=1.1, prof=0.05)
    # La locomotora en el andén (a la derecha).
    a = amarillo(); z = azul()
    caja(z, 30, Y - 4, 0.6, 3.2, 16, 3.4)
    caja(a, 30, Y - 4, 2.2, 3.25, 16, 0.6)
    caja(z, 30, Y - 12.4, 0.6, 3.2, 1.2, 4.2)
    caja(cristal(), 30, Y - 13.05, 3.3, 2.6, 0.1, 1.0)
    for y in range(-10, 4, 4):
        for s in (-1, 1):
            cil(negro(), 30 + s * 1.5, Y + y, 0.5, 0.5, 0.3, 14, eje='X')
    texto(a, 'ALASKA', 28.37, Y - 4, 1.6, tam=0.9, prof=0.03).rotation_euler = (math.pi / 2, 0, -math.pi / 2)
    # El césped, las flores y los carteles.
    caja(hierba(), 0, yf - 14, -0.05, 80, 24, 0.06)
    for x in (-20, -12, 12, 20):
        flores(x, yf - 3, 0.25, 6)
    for (x, y) in ((-30, yf - 8), (-36, yf - 18), (36, yf - 20)):
        abeto(x, y, 0, 9)
    for x in (-20, -8):
        cil(madera_o(), x, yf - 16, 0, 0.15, 4.6, 8)
    caja(blanco(), -14, yf - 16, 2.6, 13, 0.1, 2.2)
    caja(rojo(), -14, yf - 16.02, 4.2, 13, 0.1, 0.5)
    texto(blanco(), 'SE VENDE', -14, yf - 16.08, 4.28, tam=0.42, prof=0.02)
    texto(azul(), 'GROENLANDIA', -14, yf - 16.06, 3.25, tam=0.85, prof=0.03)
    texto(negro(), 'PREGUNTAR POR DONALD', -14, yf - 16.06, 2.75, tam=0.3, prof=0.02)
    for x in (9, 23):
        cil(madera_o(), x, yf - 16, 0, 0.12, 4.4, 8)
    caja(bandera_es('pancarta_es_anc', 2.8, 1.6), 16, yf - 16, 2.8, 14, 0.06, 1.6)
    texto(negro(), 'VALDEZ Y CÓRDOVA SON NOMBRES ESPAÑOLES', 16, yf - 16.04, 3.45, tam=0.48, prof=0.03)

# ================================================================ edificios
def teatro_4th():
    """El teatro de la 4th Avenue (1947): la fachada art déco con franjas
    verticales y el gran letrero 4TH AVENUE con su marquesina."""
    Y = 8
    W, D, H = 20.0, 12.0, 13.0
    yf = Y - D / 2
    c = mat('fachada_4th_anc', 0x9a7a5a, 0.7)
    caja(c, 0, Y, 0, W, D, H)
    for x in range(-9, 10, 2):
        caja(mat('franja_4th_anc', 0xb89a6a, 0.6), x, yf - 0.1, 4, 0.5, 0.2, H - 4)
    caja(c, 0, yf - 0.2, H, 8, 0.5, 2.5)
    caja(mat('marquesina_4th_anc', 0x2a2a3a, 0.5), 0, yf - 1.5, 3.4, 14, 3.0, 1.2)
    bomb = luz('bombilla_4th_anc', 0xffe6a0, 1.2)
    for k in range(26):
        caja(bomb, -6.5 + k * 0.52, yf - 3.02, 4.5, 0.14, 0.06, 0.14)
    caja(blanco(), 0, yf - 3.05, 3.5, 12.6, 0.06, 0.9)
    texto(rojo(), '4TH AVENUE', 0, yf - 3.1, 3.7, tam=0.6, prof=0.02)
    caja(rojo(), 0, yf - 1.2, 6.5, 1.2, 1.2, 9)
    for k, ch in enumerate('4TH AVE'):
        if ch != ' ':
            texto(amarillo(), ch, 0, yf - 1.82, 14.0 - k * 1.1, tam=0.9, prof=0.03)
    for x in (-3, 3):
        puerta(x, 0, 2.0, 2.8, y=yf - 0.05, color=0x8a2a1e, marco=amarillo())

def cabana_troncos():
    """La cabaña de troncos de la oficina de turismo, con el tejado cubierto
    de hierba y flores, el porche y el letrero LOG CABIN."""
    Y = 6
    W, D = 12.0, 8.0
    yf = Y - D / 2
    caja(tronco_m(), 0, Y, 0, W, D, 3.6)
    for z in (0.3, 1.0, 1.7, 2.4, 3.1):
        for s in (-1, 1):
            cil(madera(), s * (W / 2 + 0.1), yf - 0.1, z, 0.16, 0.5, 8, eje='Y')
    tejado(hierba(), 0, Y - D / 2 - 0.5, Y + D / 2 + 0.5, 3.6, W + 1.0, 2.2, cumbrera='x')
    for k in range(8):
        flores(-4.5 + k * 1.3, yf - 0.3, 4.4 + (k % 2) * 0.4, 2)
    caja(madera_o(), 0, yf - 1.4, 2.6, W - 1, 2.6, 0.15)
    for x in (-5, 0, 5):
        cil(madera(), x, yf - 2.5, 0, 0.14, 2.6, 8)
    ventana(-3.2, 1.0, 1.4, 1.4, y=yf - 0.05, marco=madera_o(), cristal=cristal())
    ventana(3.2, 1.0, 1.4, 1.4, y=yf - 0.05, marco=madera_o(), cristal=cristal())
    puerta(0, 0, 1.2, 2.2, y=yf - 0.05, color=0x5a3a22, marco=madera_o())
    caja(madera_o(), 0, yf - 2.75, 2.95, 4, 0.1, 0.6)
    texto(amarillo(), 'LOG CABIN', 0, yf - 2.82, 3.08, tam=0.4, prof=0.02)
    for x in (-8, 8):
        flores(x, yf - 1, 0.2, 5)

def hotel_captain_cook():
    """El hotel Captain Cook: las torres de ladrillo oscuro con franjas de
    ventanas y el letrero en lo alto."""
    Y = 10
    l = mat_bloques('ladrillo_cc_anc', 0x6a4a3a, 0x4a3226, ancho=0.4, alto=0.16)
    caja(l, -6, Y, 0, 14, 14, 42)
    caja(l, 8, Y + 2, 0, 12, 12, 30)
    for z in range(3, 41, 3):
        caja(cristal(), -6, Y - 7.05, z, 12, 0.1, 1.4)
    for z in range(3, 29, 3):
        caja(cristal(), 8, Y - 4.05, z, 10, 0.1, 1.4)
    caja(blanco(), -6, Y - 7.1, 42.4, 10, 0.1, 1.4)
    texto(madera_o(), 'CAPTAIN COOK', -6, Y - 7.15, 42.7, tam=0.8, prof=0.03)
    caja(mat('toldo_cc_anc', 0x2a3a5a, 0.5), 0, Y - 8.5, 3.0, 12, 3, 0.2)

def alce_pintado():
    """Un alce de fibra pintado de colores, de los de las aceras de
    Anchorage, sobre su peana (para la acera)."""
    caja(gris(), 0, 0, 0, 1.0, 2.2, 0.3)
    c = mat('alce_pintado_anc', 0x3a8ad8, 0.5)
    esfera(c, 0, 0.1, 1.55, 0.5, 2, esc=(0.7, 1.7, 0.8))
    for y in (-0.55, 0.65):
        for s in (-1, 1):
            cil(c, s * 0.2, y, 0.3, 0.09, 1.0, 8)
    rama(c, (0, -0.65, 1.8), (0, -0.95, 2.2), 0.22, 0.18, 8)
    esfera(c, 0, -1.15, 2.1, 0.25, 2, esc=(0.8, 1.6, 0.9))
    for s in (-1, 1):
        a = mat('cuerno_pintado_anc', 0xf2c21a, 0.5)
        caja(a, s * 0.5, -0.95, 2.55, 0.6, 0.35, 0.08, inclina=0.0)
        for k in range(3):
            rama(a, (s * (0.35 + k * 0.17), -0.95, 2.6), (s * (0.45 + k * 0.2), -0.95, 2.95), 0.05, 0.03, 5)
    for (x, y, z) in ((0.36, 0.3, 1.6), (-0.36, -0.2, 1.5), (0.3, -0.4, 1.3)):
        esfera([rojo, amarillo, blanco][int(abs(y) * 10) % 3](), x, y, z, 0.16, 1, esc=(0.3, 1, 1))

# ================================================================ cruza la calle
def arco_iditarod():
    """El arco de salida de la Iditarod: dos postes de troncos y el letrero
    IDITAROD · ANCHORAGE, y por detrás, NOME: 1.000 MILLAS."""
    for s in (-1, 1):
        cil(madera(), s * 8.6, 0, 0, 0.45, 7.8, 10)
    cil(madera(), 0, 0, 7.2, 0.4, 18.4, 10, eje='X')
    caja(azul(), 0, 0, 4.4, 12, 0.18, 1.8)
    texto(blanco(), 'IDITAROD', 0, -0.12, 5.25, tam=0.85, prof=0.04)
    texto(amarillo(), 'ANCHORAGE · SALIDA', 0, -0.12, 4.6, tam=0.45, prof=0.04)
    o = texto(blanco(), 'NOME: 1.000 MILLAS', 0, 0.12, 4.95, tam=0.6, prof=0.04)
    o.rotation_euler = (math.pi / 2, 0, math.pi)
    for x in (-4, 4):
        cil(hierro(), x, 0, 6.2, 0.03, 1.0, 4)
    for s in (-1, 1):
        for k in range(4):
            esfera(negro(), s * (6.5 - k * 0.9), -0.6, 0.45, 0.28, 1, esc=(1.6, 0.8, 0.8))

# ================================================================ el vuelo
def vuelo_chugach():
    """El vuelo en hidroavión (momento estrella, al aire libre): el lago Hood
    al principio, con sus muelles y avionetas, y luego el bosque de abetos y
    los ríos, con las montañas Chugach nevadas a los dos lados y un glaciar.
    Cruza la calle: el origen en el centro y la calle a lo largo de y."""
    L = 420
    caja(agua(), 0, -L / 2 + 45, -0.2, 60, 90, 0.2)
    caja(mat('bosque_suelo_anc', 0x4a6a3a, 0.9), 0, 45, -0.25, 60, L - 90, 0.2)
    caja(agua(), 6, 70, -0.15, 5, 140, 0.1)
    # Los muelles y las avionetas del lago.
    for k in range(5):
        y = -L / 2 + 10 + k * 16
        for s in (-1, 1):
            caja(madera(), s * 12, y, 0, 8, 1.4, 0.3)
            col = [rojo, amarillo, azul, blanco][(k + (s > 0)) % 4]()
            caja(col, s * 15, y + 2, 1.2, 1.2, 4.5, 1.0)
            caja(col, s * 15, y + 1.2, 2.3, 7.5, 1.2, 0.12)
            for d in (-0.7, 0.7):
                cil(blanco(), s * 15 + d, y + 2, 0.25, 0.25, 4.5, 8, eje='Y')
    # El bosque.
    for k in range(int((L - 90) / 9)):
        y = -L / 2 + 95 + k * 9
        for s in (-1, 1):
            for j in range(3):
                abeto(s * (9 + j * 5 + (k * 3 % 4)), y + j * 2.5, 0, 6 + (k + j) % 4 * 1.5)
    # Las montañas nevadas a los lados.
    for s in (-1, 1):
        for k in range(8):
            y = -L / 2 + 30 + k * 55
            h = 30 + (k * 13 % 20)
            x = s * (55 + (k % 3) * 10)
            cil(roca(), x, y, 0, 22, h, 6, r2=1.5).scale = (0.8, 1.4, 1)
            cil(nieve(), x, y, h * 0.62, 22 * 0.4, h * 0.38, 6, r2=1.4).scale = (0.8, 1.4, 1)
    # Un glaciar que baja entre dos montes.
    caja(mat('glaciar_anc', 0xb8d8ec, 0.3), -40, 120, 0, 14, 60, 4, inclina=0.0)
    for (y, txt) in ((-L / 2 + 1, 'DESPEGUE'), (L / 2 - 1, 'ATERRIZAJE')):
        for s in (-1, 1):
            cil(hierro(), s * 7.2, y, -0.2, 0.25, 6.4, 8)
        cil(hierro(), 0, y, 6.0, 0.22, 14.8, 8, eje='X')
        caja(blanco(), 0, y, 4.0, 9.0, 0.16, 1.5)
        texto(azul(), 'LAKE HOOD · ' + txt, 0, y - 0.1, 4.45, tam=0.5, prof=0.04)

# ================================================================ obstáculos
def hidroavion():
    """El hidroavión de los lagos de Alaska (un vehículo: se va de pie encima
    del ala, y vuela): el fuselaje rojo y blanco, el ala alta, la hélice, la
    cola y los dos flotadores. El morro mira al jugador (-y); el juego le da
    la vuelta al montarlo."""
    r = rojo()
    b = blanco()
    caja(r, 0, 2.6, 0.9, 1.1, 3.6, 1.1)
    cil(r, 0, 0.6, 1.45, 0.55, 0.9, 12, eje='Y', r2=0.35)
    caja(b, 0, 5.4, 1.1, 0.6, 2.4, 0.7)
    caja(cristal(), 0, 1.5, 1.85, 1.0, 1.2, 0.5)
    # El ala alta y los montantes.
    caja(b, 0, 2.2, 2.15, 9.0, 1.5, 0.12)
    caja(r, 0, 2.2, 2.17, 9.05, 0.5, 0.12)
    for s in (-1, 1):
        rama(hierro(), (s * 0.5, 2.4, 0.9), (s * 2.6, 2.3, 2.15), 0.04, 0.04, 4)
    # La hélice.
    cil(hierro(), 0, 0.1, 1.45, 0.1, 0.4, 8, eje='Y')
    caja(negro(), 0, -0.1, 1.45, 2.2, 0.06, 0.16)
    caja(negro(), 0, -0.1, 1.45, 0.16, 0.06, 2.2)
    # La cola.
    caja(r, 0, 6.6, 1.4, 0.08, 0.9, 1.2)
    caja(b, 0, 6.6, 1.25, 2.6, 0.8, 0.08)
    # Los flotadores.
    for s in (-1, 1):
        esfera(b, s * 1.0, 3.0, 0.25, 0.5, 2, esc=(0.7, 7.0, 0.6))
        rama(hierro(), (s * 1.0, 1.8, 0.4), (s * 0.4, 1.8, 0.9), 0.04, 0.04, 4)
        rama(hierro(), (s * 1.0, 3.8, 0.4), (s * 0.4, 3.8, 0.9), 0.04, 0.04, 4)
    texto(azul(), 'N270TC', 0.56, 3.0, 0.95, tam=0.18, prof=0.01).rotation_euler = (math.pi / 2, 0, math.pi / 2)

def cresta_nevada():
    """La cresta nevada del vuelo (hay que pasarle por encima): roca con la
    cima blanca, de 1 m de alto (el juego la estira) y 7,5 de ancho."""
    caja(roca(), 0, 0, 0, 7.6, 1.6, 0.75)
    for k in range(7):
        x = -3.3 + k * 1.1
        cil(roca(), x, 0, 0.7, 0.75, 0.25, 5, r2=0.35)
    caja(nieve(), 0, 0, 0.82, 7.4, 1.4, 0.18)

def nube_tormenta():
    """La nube de tormenta del vuelo (hay que pasarle por debajo): una nube
    gris oscura de 7,5 m de ancho, con la base plana en el origen."""
    n = mat('nube_anc', 0x6a7080, 0.9)
    for k in range(7):
        x = -3.3 + k * 1.1
        esfera(n, x, 0, 1.5 + (k % 2) * 0.3, 1.1 + (k % 3) * 0.2, 2, esc=(1.0, 0.9, 0.8))
    caja(n, 0, 0, 0.0, 7.4, 1.6, 0.9)

def cartel_alaska():
    """La pancarta de España (agacharse): VALDEZ Y CÓRDOVA SON NOMBRES ESPAÑOLES."""
    for x in (-1.25, 1.25):
        cil(madera_o(), x, 0, 0, 0.07, 2.75, 8)
    caja(bandera_es('pancarta_es_obst_anc', 1.5, 1.2), 0, 0, 1.5, 2.4, 0.05, 1.2)
    texto(negro(), 'VALDEZ Y CÓRDOVA', 0, -0.035, 2.25, tam=0.2, prof=0.02)
    texto(negro(), 'SON NOMBRES', 0, -0.035, 1.95, tam=0.18, prof=0.02)
    texto(negro(), 'ESPAÑOLES', 0, -0.035, 1.68, tam=0.18, prof=0.02)

def nasa_cangrejo():
    """La nasa de los cangrejos reales (se salta): la jaula de acero con la
    red y dos cangrejos rojos encima."""
    h = hierro()
    for (x, y) in ((-0.8, -0.8), (0.8, -0.8), (-0.8, 0.8), (0.8, 0.8)):
        cil(h, x, y, 0, 0.04, 0.8, 6)
    for z in (0.05, 0.78):
        for s in (-1, 1):
            caja(h, 0, s * 0.8, z, 1.65, 0.05, 0.05)
            caja(h, s * 0.8, 0, z, 0.05, 1.65, 0.05)
    red = mat_bloques('red_nasa_anc', 0x9aa0a8, 0x3a3c40, ancho=0.12, alto=0.12, grosor=0.02)
    caja(red, 0, -0.81, 0.05, 1.6, 0.02, 0.73)
    caja(red, 0, 0.81, 0.05, 1.6, 0.02, 0.73)
    for x in (-0.3, 0.35):
        esfera(rojo(), x, 0, 0.92, 0.22, 1, esc=(1.3, 1, 0.45))
        for s in (-1, 1):
            rama(rojo(), (x + s * 0.2, 0, 0.92), (x + s * 0.5, -0.1, 0.85), 0.03, 0.02, 4)
    caja(amarillo(), 0, -0.84, 0.4, 0.5, 0.02, 0.2)
    texto(negro(), 'KING CRAB', 0, -0.85, 0.44, tam=0.08, prof=0.005)

PIEZAS = {
    'estacion_alaska':   (estacion_alaska,   'anchorage',  dict(lado=2048, bisel=0.0)),
    'teatro_4th':        (teatro_4th,        'anchorage',  dict(lado=1024, bisel=0.0)),
    'cabana_troncos':    (cabana_troncos,    'anchorage',  dict(lado=1024, bisel=0.0)),
    'hotel_captain_cook': (hotel_captain_cook, 'anchorage', dict(lado=1024, bisel=0.0)),
    'alce_pintado':      (alce_pintado,      'anchorage',  dict(lado=256, bisel=0.0)),
    'arco_iditarod':     (arco_iditarod,     'anchorage',  dict(lado=1024, bisel=0.0, suelo=False)),
    'vuelo_chugach':     (vuelo_chugach,     'anchorage',  dict(lado=2048, bisel=0.0, suelo=False)),
    'hidroavion':        (hidroavion,        'obstaculos', dict(lado=256, bisel=0.0)),
    'cresta_nevada':     (cresta_nevada,     'obstaculos', dict(lado=256, bisel=0.0)),
    'nube_tormenta':     (nube_tormenta,     'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
    'cartel_alaska':     (cartel_alaska,     'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
    'nasa_cangrejo':     (nasa_cangrejo,     'obstaculos', dict(lado=256, bisel=0.0)),
}

correr(PIEZAS)
