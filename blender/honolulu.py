# Nivel 37: Honolulu, Hawái (15/11/2026).
#
#   blender -b -P blender/honolulu.py -- [pieza ...] [--rapido]
#
# Historia: «Surf, cocos que caen y golf otra vez». Acto de la Armada
#   Española. Por Kalakaua Avenue (Waikiki) una mañana de sol: la torre Aloha
#   con su reloj, el hotel rosa Royal Hawaiian, el Capitolio con sus columnas
#   de palmera y las palmeras de las aceras. Los cocos caen de las palmeras
#   (la sombra avisa) y botan al carril de al lado (la flecha avisa); el
#   momento estrella, el surf en Waikiki: la ola te levanta y en el aire se
#   hacen piruetas deslizando (si aterrizas girando, al agua). Final en el
#   palacio Iolani. Pancartas de España: PANIOLO = ESPAÑOL (los vaqueros de
#   Hawái se llaman así por los vaqueros españoles).
# Obstáculos (carpeta obstaculos): la tabla de surf (se monta: es un
# vehículo), el coco, la pancarta, las tablas de surf en su caballete, el
# carrito del raspado de hielo y el trolley de Waikiki.

import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import *

def blanco():    return mat('blanco_hnl', 0xf6f4ee, 0.5)
def negro():     return mat('negro_hnl', 0x1c1c20, 0.4)
def cristal():   return mat('cristal_hnl', 0x3a6a80, 0.15)
def rojo():      return mat('rojo_hnl', 0xc8202a, 0.45)
def azul():      return mat('azul_hnl', 0x2a6ab8, 0.45)
def amarillo():  return mat('amarillo_hnl', 0xf2c21a, 0.45)
def verde():     return mat('verde_hnl', 0x2a8a4a, 0.5)
def rosa():      return mat('rosa_hnl', 0xf0a0b0, 0.6)
def rosa_o():    return mat('rosa_oscuro_hnl', 0xd87890, 0.6)
def gris():      return mat('gris_hnl', 0x8a9098, 0.4)
def hierro():    return mat('hierro_hnl', 0x2a2c30, 0.45)
def madera():    return mat('madera_hnl', 0x8a5a34, 0.85)
def madera_o():  return mat('madera_oscura_hnl', 0x5a3a22, 0.85)
def piedra():    return mat('piedra_hnl', 0xe8e0cc, 0.7)
def arena():     return mat('arena_hnl', 0xf0dcae, 0.95)
def hoja():      return mat('hoja_palmera_hnl', 0x3a8a3a, 0.8)
def tronco_p():  return mat_bloques('tronco_palmera_hnl', 0x9a7a5a, 0x7a5a3e, ancho=1.0, alto=0.22, grosor=0.03)
def coco_m():    return mat('coco_hnl', 0x6a4a26, 0.8)
def cesped():    return mat('cesped_hnl', 0x5a9a3a, 0.9)

def bandera_es(nombre, z0, alto):
    return mat_franjas(nombre, 0xc8202a, 0xf2c21a, 3, eje='Z', z0=z0, alto=alto)

def palmera(x, y, z, h, inclina=0.25, giro=0.0, cocos=True):
    """Una palmera de cocos: el tronco curvo y anillado, las hojas y los cocos."""
    c, s = math.cos(giro), math.sin(giro)
    p0 = (x, y, z)
    pm = (x + c * h * inclina * 0.4, y + s * h * inclina * 0.4, z + h * 0.55)
    p1 = (x + c * h * inclina, y + s * h * inclina, z + h)
    rama(tronco_p(), p0, pm, 0.24 * h / 8, 0.2 * h / 8, 8)
    rama(tronco_p(), pm, p1, 0.2 * h / 8, 0.17 * h / 8, 8)
    for k in range(8):
        a = k * math.tau / 8
        q = (p1[0] + math.cos(a) * h * 0.38, p1[1] + math.sin(a) * h * 0.38, p1[2] - h * 0.1)
        rama(hoja(), p1, q, 0.32 * h / 8, 0.05, 4)
        o = esfera(hoja(), (p1[0] + q[0]) / 2, (p1[1] + q[1]) / 2, (p1[2] + q[2]) / 2 + 0.1, h * 0.2, 1, esc=(1, 0.35, 0.12))
        o.rotation_euler = (0, -0.25, a)
    if cocos:
        for k in range(3):
            a = k * math.tau / 3 + 0.4
            esfera(coco_m(), p1[0] + math.cos(a) * 0.3, p1[1] + math.sin(a) * 0.3, p1[2] - 0.35, 0.2 * h / 8, 1)

def lei(x0, x1, y, z, cuelga=0.6, n=16):
    """Una guirnalda de flores (lei) colgando."""
    for k in range(n):
        u = (k + 0.5) / n
        esfera([rosa, amarillo, rojo, blanco][k % 4](), x0 + (x1 - x0) * u, y, z - cuelga * 4 * u * (1 - u), 0.14, 1)

# ================================================================ la meta
def palacio_iolani():
    """El palacio Iolani (la meta): dos pisos de galerías con columnas, las
    torres de las esquinas y la del centro, el estuco claro, la escalinata,
    el césped con banianos y la pancarta PANIOLO = ESPAÑOL."""
    Y = 20
    W, D, H = 40.0, 22.0, 13.0
    yf = Y - D / 2
    p = piedra()
    caja(p, 0, Y, 0, W, D, H)
    caja(blanco(), 0, Y, H, W + 0.6, D + 0.6, 0.8)
    for z in (0, 6.2):
        caja(blanco(), 0, yf - 1.6, z + 5.8, W - 4, 3.2, 0.4)
        columnata(blanco(), -17, 17, 14, yf - 3.0, z, 0.3, 5.8)
        for k in range(7):
            ventana(-15 + k * 5, z + 1.2, 1.8, 3.6, y=yf - 0.05, marco=blanco(), cristal=cristal())
    for (x, h) in ((-18, 19), (18, 19), (0, 22)):
        caja(p, x, yf + 1.5, 0, 6, 6, h)
        caja(blanco(), x, yf + 1.5, h, 6.6, 6.6, 0.7)
        for dx in (-2.4, 2.4):
            caja(blanco(), x + dx, yf + 1.5 - 3.4, h + 0.7, 0.7, 0.7, 1.2)
        ventana(x, h - 4.5, 1.6, 2.8, y=yf - 1.55, marco=blanco(), cristal=cristal())
    cil(gris(), 0, yf + 1.5, 22.7, 0.08, 6, 6)
    caja(mat_franjas('bandera_hi_hnl', 0xf6f4ee, 0xc8202a, 8, eje='Z', z0=25.5, alto=2.4), 1.8, yf + 1.5, 25.5, 3.4, 0.05, 2.4)
    caja(azul(), 0.9, yf + 1.47, 26.7, 1.6, 0.05, 1.2)
    for k in range(10):
        caja(blanco(), 0, yf - 4.2 - k * 0.5, 0, 12 + k * 0.6, 0.5, 3.0 - k * 0.3)
    caja(cesped(), 0, yf - 16, -0.05, 80, 26, 0.06)
    for (x, y) in ((-28, yf - 10), (28, yf - 10), (-34, yf - 20), (34, yf - 20)):
        cil(madera_o(), x, y, 0, 1.2, 4, 10)
        esfera(mat('copa_baniano_hnl', 0x3a7a3a, 0.85), x, y, 6.5, 5, 2, esc=(1.3, 1.3, 0.8))
    for x in (8, 22):
        cil(madera_o(), x, yf - 15, 0, 0.12, 4.4, 8)
    caja(bandera_es('pancarta_es_hnl', 2.8, 1.6), 15, yf - 15, 2.8, 14, 0.06, 1.6)
    texto(negro(), 'PANIOLO = ESPAÑOL', 15, yf - 15.04, 3.35, tam=0.8, prof=0.03)

# ================================================================ edificios
def aloha_tower():
    """La torre Aloha (1926): la torre clara y estrecha de diez pisos, el
    reloj y ALOHA en las cuatro caras, el tejado de pirámide con su mástil."""
    Y = 8
    p = piedra()
    caja(p, 0, Y, 0, 16, 12, 6)
    caja(p, 0, Y, 6, 9, 9, 36)
    for z in range(8, 36, 3):
        for x in (-2.2, 0, 2.2):
            caja(cristal(), x, Y - 4.55, z, 1.0, 0.1, 1.8)
    caja(blanco(), 0, Y, 42, 10, 10, 1)
    for (dx, dy, rz) in ((0, -1, 0), (-1, 0, 1), (1, 0, 1)):
        x, y = dx * 5.1, Y + dy * 5.1
        o = cil(blanco(), x, y, 45.5, 2.0, 0.15, 24, eje='Y')
        if rz:
            o.rotation_euler = (math.pi / 2, 0, math.pi / 2)
        if dy == -1:
            caja(negro(), x, y - 0.12, 45.5, 0.12, 0.04, 1.5)
            caja(negro(), x + 0.45, y - 0.12, 45.5, 1.0, 0.04, 0.12)
            texto(rojo(), 'ALOHA', x, y - 0.1, 42.6, tam=1.0, prof=0.04)
    caja(p, 0, Y, 43, 9, 9, 5)
    o = cil(mat('tejado_aloha_hnl', 0x3a6a5a, 0.5), 0, Y, 48, 6.6, 6, 4, r2=0.3)
    o.rotation_euler = (0, 0, math.pi / 4)
    cil(gris(), 0, Y, 54, 0.1, 5, 6)
    texto(negro(), 'ALOHA TOWER', 0, Y - 6.06, 4.0, tam=0.9, prof=0.03)

def royal_hawaiian():
    """El hotel Royal Hawaiian (1927), el palacio rosa del Pacífico: estilo
    morisco español, los arcos, la torre central con su cúpula y las
    palmeras delante."""
    Y = 12
    W, D, H = 40.0, 18.0, 14.0
    yf = Y - D / 2
    r = rosa()
    caja(r, 0, Y, 0, W, D, H)
    caja(rosa_o(), 0, Y, H, W + 0.4, D + 0.4, 0.6)
    for k in range(9):
        x = -16 + k * 4
        for z in (1.0, 5.6, 9.8):
            caja(cristal(), x, yf - 0.05, z, 1.6, 0.1, 2.4)
            cil(rosa_o(), x, yf - 0.08, z + 2.4, 0.85, 0.12, 12, eje='Y')
    caja(r, 0, yf + 2, 0, 10, 10, 24)
    for z in (14, 20):
        caja(rosa_o(), 0, yf + 2, z, 10.4, 10.4, 0.5)
    for x in (-2.5, 0, 2.5):
        caja(cristal(), x, yf - 3.05, 21, 1.2, 0.1, 2.4)
    cupula(rosa_o(), 0, yf + 2, 24, 4.8, 5, 24, 6)
    cil(amarillo(), 0, yf + 2, 29, 0.15, 2, 6)
    caja(blanco(), 0, yf - 3.1, 15.0, 8, 0.1, 1.2)
    texto(rosa_o(), 'ROYAL HAWAIIAN', 0, yf - 3.16, 15.25, tam=0.7, prof=0.03)
    for x in (-18, -10, 10, 18):
        palmera(x, yf - 4, 0, 10, 0.15, 0.3 * x)

def capitolio_hawaii():
    """El Capitolio de Hawái (1969): el edificio cuadrado levantado sobre
    columnas que se abren arriba como palmeras, con el hueco del volcán en el
    centro y el estanque alrededor."""
    Y = 12
    W, D = 30.0, 20.0
    yf = Y - D / 2
    caja(mat('estanque_hnl', 0x3a7aa8, 0.1), 0, Y, -0.05, W + 8, D + 8, 0.1)
    p = mat('hormigon_hnl', 0xd8d4cc, 0.8)
    for k in range(8):
        x = -14 + k * 4
        cil(p, x, yf - 1.0, 0, 0.6, 12, 10, r2=1.2)
    caja(p, 0, Y, 12, W, D, 6)
    for x in range(-13, 14, 2):
        caja(cristal(), x, yf - 0.05, 13, 1.2, 0.1, 4)
    cil(mat('crater_hnl', 0x4a4a52, 0.8), 0, Y, 17.9, 6, 0.2, 24, r2=4)
    caja(blanco(), 0, yf - 1.2, 2.0, 10, 0.1, 1.0)
    texto(azul(), 'STATE CAPITOL', 0, yf - 1.26, 2.2, tam=0.55, prof=0.03)

def palmera_cocos():
    """Una palmera de cocos de la acera, algo inclinada."""
    palmera(0, 0, 0, 8.5, 0.22, 0.6)
    cil(mat('alcorque_hnl', 0x9a948a, 0.8), 0, 0, 0, 0.9, 0.2, 12)

# ================================================================ cruza la calle
def arco_aloha():
    """El arco de Waikiki: dos troncos de palmera, el letrero ALOHA · WAIKIKI
    y las guirnaldas de flores colgando; por detrás, MAHALO."""
    for s in (-1, 1):
        palmera(s * 8.6, 0, 0, 9, 0.05, 0, cocos=False)
    caja(madera(), 0, 0, 7.0, 17.6, 0.4, 0.5)
    caja(amarillo(), 0, 0, 5.0, 11, 0.18, 1.6)
    texto(rojo(), 'ALOHA', 0, -0.12, 5.75, tam=0.8, prof=0.04)
    texto(azul(), 'WAIKIKI', 0, -0.12, 5.15, tam=0.45, prof=0.04)
    o = texto(rojo(), 'MAHALO', 0, 0.12, 5.4, tam=0.8, prof=0.04)
    o.rotation_euler = (math.pi / 2, 0, math.pi)
    lei(-8.3, 8.3, -0.3, 6.9, 0.9, 30)
    for x in (-4, 4):
        cil(hierro(), x, 0, 6.6, 0.03, 0.5, 4)

# ================================================================ la playa
def playa_waikiki():
    """La playa de Waikiki (momento estrella): el mar con las franjas de
    espuma, la arena y los hoteles a la izquierda, las palmeras, las
    sombrillas, las canoas de balancín, los surfistas y Diamond Head al
    fondo a la derecha, y los arcos de SALIDA y META.
    Cruza la calle: el origen en el centro y la calle a lo largo de y."""
    L = 420
    caja(mat_franjas('mar_hnl', 0x2a8ab8, 0x3aa0c8, 70, eje='Y', z0=-L / 2, alto=L), 6, 0, -0.2, 46, L, 0.2)
    for k in range(int(L / 12)):
        caja(mat('espuma_hnl', 0xe8f4fa, 0.6), 6, -L / 2 + 6 + k * 12, -0.01, 40, 0.5, 0.02)
    caja(arena(), -24, 0, -0.15, 14, L, 0.2)
    # Los hoteles y las palmeras de la playa.
    for k in range(int(L / 30)):
        y = -L / 2 + 15 + k * 30
        col = [rosa, blanco, lambda: mat('hotel_amarillo_hnl', 0xf0e0a0, 0.6)][k % 3]()
        h = 18 + (k * 7 % 4) * 6
        caja(col, -40, y, 0, 12, 24, h)
        for z in range(3, h - 2, 3):
            caja(cristal(), -33.95, y, z, 0.1, 20, 1.4)
        palmera(-20, y - 8, 0, 9, 0.25, 0.3)
        palmera(-23, y + 6, 0, 8, 0.2, -0.4)
        cil(mat_franjas(f'sombrilla_hnl{k % 2}', [0xc8202a, 0x2a6ab8][k % 2], 0xf6f4ee, 6, eje='Z', z0=2.0, alto=0.5), -26, y, 2.0, 1.4, 0.5, 12, r2=0.05)
        cil(blanco(), -26, y, 0, 0.04, 2.0, 4)
    # Canoas y surfistas en el agua (lejos de los carriles).
    for k in range(int(L / 40)):
        y = -L / 2 + 20 + k * 40
        x = 12 + (k % 3) * 5
        esfera(mat('canoa_hnl', 0xc8202a, 0.5), x, y, 0.15, 0.5, 2, esc=(0.8, 7, 0.5))
        rama(madera(), (x - 0.4, y - 1, 0.3), (x - 2.0, y - 1, 0.3), 0.06, 0.06, 4)
        caja(amarillo(), x + 6, y + 10, 0.05, 0.5, 2.3, 0.08)
        cil(mat('surfista_hnl', 0x2a2a30, 0.6), x + 6, y + 10, 0.13, 0.22, 1.0, 6)
        esfera(mat('piel_hnl', 0xc8946a, 0.7), x + 6, y + 10, 1.3, 0.18, 1)
    # Diamond Head al fondo.
    o = cil(mat('diamond_head_hnl', 0x8a7a5a, 0.9), 70, 150, -0.2, 50, 28, 10, r2=26)
    o.scale = (1.0, 0.7, 1.0)
    cil(mat('crater_dh_hnl', 0x6a6a42, 0.9), 70, 150, 27.6, 25, 0.5, 10).scale = (1.0, 0.7, 1.0)
    for (y, txt) in ((-L / 2 + 1, 'SALIDA'), (L / 2 - 1, 'META')):
        for s in (-1, 1):
            cil(madera(), s * 7.0, y, -0.2, 0.3, 6.0, 8)
        caja(madera(), 0, y, 5.4, 14.4, 0.4, 0.5)
        caja(amarillo(), 0, y, 4.0, 9.0, 0.16, 1.3)
        texto(rojo(), 'WAIKIKI SURF · ' + txt, 0, y - 0.1, 4.4, tam=0.5, prof=0.04)

# ================================================================ obstáculos
def tabla_surf():
    """La tabla de surf (un vehículo: se va de pie encima): larga, amarilla con
    la franja roja y la quilla. La punta mira al jugador (-y)."""
    t = amarillo()
    esfera(t, 0, 1.5, 0.07, 0.5, 2, esc=(1.1, 6.0, 0.14))
    caja(rojo(), 0, 1.5, 0.13, 0.12, 5.0, 0.02)
    cil(blanco(), 0, 3.6, -0.05, 0.02, 0.3, 3, r2=0.0)

def coco():
    """El coco que cae de la palmera: la cáscara marrón y peluda con sus
    tres ojitos. Centrado en el origen."""
    esfera(coco_m(), 0, 0, 0, 0.3, 2, esc=(1, 1, 1.1))
    for (x, z) in ((-0.08, 0.1), (0.08, 0.1), (0, -0.02)):
        esfera(negro(), x, -0.28, z, 0.04, 1)

def cartel_hawaii():
    """La pancarta de España (agacharse): PANIOLO = ESPAÑOL."""
    for x in (-1.25, 1.25):
        cil(madera_o(), x, 0, 0, 0.07, 2.75, 8)
    caja(bandera_es('pancarta_es_obst_hnl', 1.5, 1.2), 0, 0, 1.5, 2.4, 0.05, 1.2)
    texto(negro(), 'PANIOLO', 0, -0.035, 2.15, tam=0.32, prof=0.02)
    texto(negro(), '= ESPAÑOL', 0, -0.035, 1.72, tam=0.26, prof=0.02)

def tablas_surf():
    """Las tablas de surf tumbadas en su caballete (se saltan)."""
    for x in (-0.9, 0.9):
        caja(madera(), x, 0, 0, 0.1, 0.8, 0.5)
    for k, c in enumerate((azul, rojo, amarillo)):
        o = esfera(c(), 0, 0, 0.55 + k * 0.08, 0.5, 2, esc=(4.0, 0.95, 0.12))
        o.rotation_euler = (0, 0, (k - 1) * 0.05)

def carrito_raspado():
    """El carrito del raspado de hielo (shave ice) con la sombrilla de
    colores (no se pasa)."""
    caja(blanco(), 0, 0.9, 0.3, 1.6, 1.8, 1.0)
    caja(mat_franjas('raspado_hnl', 0xe84a7a, 0x2a8ad8, 6, eje='X', z0=-0.8, alto=1.6), 0, 0.0, 0.5, 1.6, 0.02, 0.6)
    for (x, y) in ((-0.65, 0.2), (0.65, 0.2), (-0.65, 1.6), (0.65, 1.6)):
        cil(negro(), x, y, 0, 0.15, 0.3, 10)
    for k, c in enumerate((rojo, amarillo, azul)):
        cil(c(), -0.4 + k * 0.4, 0.9, 1.3, 0.16, 0.25, 10, r2=0.2)
        esfera(c(), -0.4 + k * 0.4, 0.9, 1.6, 0.18, 1)
    cil(hierro(), 0, 0.9, 1.3, 0.04, 1.2, 6)
    cil(mat_franjas('sombrilla_rasp_hnl', 0xf2c21a, 0x2a8a4a, 6, eje='Z', z0=2.5, alto=0.7), 0, 0.9, 2.5, 1.3, 0.7, 12, r2=0.05)
    texto(rojo(), 'SHAVE ICE', 0, -0.03, 1.15, tam=0.18, prof=0.01)

def trolley_waikiki():
    """El trolley de Waikiki (no se pasa): el tranvía abierto rojo con sus
    bancos de madera y el techo. El morro en el origen."""
    r = rojo()
    caja(r, 0, 4.5, 0.4, 2.5, 9.0, 0.6)
    caja(r, 0, 0.8, 0.4, 2.5, 1.6, 1.7)
    caja(cristal(), 0, 0.0, 1.3, 2.2, 0.1, 0.8)
    for y in range(2, 9, 2):
        for s in (-1, 1):
            cil(madera_o(), s * 1.2, y, 1.0, 0.07, 1.6, 6)
        caja(madera(), 0, y + 0.6, 1.0, 2.2, 0.4, 0.12)
    caja(r, 0, 4.5, 2.6, 2.7, 9.2, 0.25)
    caja(amarillo(), 0, 4.5, 2.85, 2.5, 9.0, 0.08)
    caja(amarillo(), 0, -0.02, 2.2, 2.0, 0.05, 0.35)
    texto(rojo(), 'WAIKIKI TROLLEY', 0, -0.04, 2.27, tam=0.2, prof=0.01)
    for (y, s) in ((1.0, 1), (7.8, 1), (1.0, -1), (7.8, -1)):
        cil(negro(), s * 1.15, y, 0.38, 0.38, 0.3, 14, eje='X')
    for s in (-1, 1):
        caja(luz('faro_trolley_hnl', 0xfff2c0, 1.0), s * 0.85, -0.03, 0.75, 0.35, 0.05, 0.2)

PIEZAS = {
    'palacio_iolani':    (palacio_iolani,    'honolulu',   dict(lado=2048, bisel=0.0)),
    'aloha_tower':       (aloha_tower,       'honolulu',   dict(lado=1024, bisel=0.0)),
    'royal_hawaiian':    (royal_hawaiian,    'honolulu',   dict(lado=1024, bisel=0.0)),
    'capitolio_hawaii':  (capitolio_hawaii,  'honolulu',   dict(lado=1024, bisel=0.0)),
    'palmera_cocos':     (palmera_cocos,     'honolulu',   dict(lado=256, bisel=0.0)),
    'arco_aloha':        (arco_aloha,        'honolulu',   dict(lado=1024, bisel=0.0, suelo=False)),
    'playa_waikiki':     (playa_waikiki,     'honolulu',   dict(lado=2048, bisel=0.0, suelo=False)),
    'tabla_surf':        (tabla_surf,        'obstaculos', dict(lado=256, bisel=0.0)),
    'coco':              (coco,              'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
    'cartel_hawaii':     (cartel_hawaii,     'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
    'tablas_surf':       (tablas_surf,       'obstaculos', dict(lado=256, bisel=0.0)),
    'carrito_raspado':   (carrito_raspado,   'obstaculos', dict(lado=256, bisel=0.0)),
    'trolley_waikiki':   (trolley_waikiki,   'obstaculos', dict(lado=256, bisel=0.0)),
}

correr(PIEZAS)
