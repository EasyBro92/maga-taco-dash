# Nivel 38: Los Ángeles, California (15/11/2026). Nivel con jefe: el Toro.
#
#   blender -b -P blender/losangeles.py -- [pieza ...] [--rapido]
#
# Historia: «Encierro de San Fermín por Hollywood Boulevard: el Toro,
#   paelleras y la siesta española, que lo deja todo congelado». Final del
#   acto de la Armada Española. Por Hollywood Boulevard al atardecer, con las
#   estrellas del Paseo de la Fama en la acera: la torre de Capitol Records,
#   el teatro El Capitan con su marquesina, el hotel Roosevelt con su neón y
#   las colinas, donde España ha cambiado las letras: LOS ÁNGELES. La siesta:
#   la calle llena de gente durmiendo (hamacas y dormilones) y hay que pasar
#   sin hacer ruido; el momento estrella, el rodaje en el plató (el director
#   grita lo que hay que hacer: ¡salta!, ¡agáchate!, ¡a la izquierda!...); y
#   el jefe, el Toro del encierro. Final en el teatro chino. Pancartas de
#   España: LOS ÁNGELES ES ESPAÑOL.
# Obstáculos (carpeta obstaculos): la hamaca (agacharse), el dormilón (se
# salta), el mozo de San Fermín, la cámara de cine, el autobús de las
# estrellas y la pancarta.

import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import *

def blanco():    return mat('blanco_la', 0xf6f4ee, 0.5)
def negro():     return mat('negro_la', 0x1c1c20, 0.4)
def cristal():   return mat('cristal_la', 0x3a5a70, 0.15)
def rojo():      return mat('rojo_la', 0xc8202a, 0.45)
def azul():      return mat('azul_la', 0x2a4a9a, 0.45)
def amarillo():  return mat('amarillo_la', 0xf2c21a, 0.45)
def verde():     return mat('verde_la', 0x2a6a4a, 0.5)
def oro():       return mat('oro_la', 0xe8b840, 0.25)
def rosa():      return mat('rosa_la', 0xe88aa8, 0.5)
def gris():      return mat('gris_la', 0x8a9098, 0.4)
def hierro():    return mat('hierro_la', 0x2a2c30, 0.45)
def madera():    return mat('madera_la', 0x8a5a34, 0.85)
def madera_o():  return mat('madera_oscura_la', 0x5a3a22, 0.85)
def estuco():    return mat('estuco_la', 0xf0e2c8, 0.8)
def teja():      return mat('teja_la', 0xb8502e, 0.7)
def piel():      return mat('piel_la', 0xe8b89a, 0.7)
def colina():    return mat('colina_la', 0x8a7a4a, 0.95)
def neon_r():    return luz('neon_rojo_la', 0xff3a2a, 1.4)
def bombilla():  return luz('bombilla_la', 0xffe6a0, 1.2)

def bandera_es(nombre, z0, alto):
    return mat_franjas(nombre, 0xc8202a, 0xf2c21a, 3, eje='Z', z0=z0, alto=alto)

def persona_blanca(x, y, z, giro=0.0, corre=False):
    """Un mozo de San Fermín: de blanco con el pañuelo y la faja rojos."""
    b = blanco()
    for s in (-1, 1):
        if corre:
            rama(b, (x + s * 0.12, y, z + 0.85), (x + s * 0.14, y + s * 0.35, z), 0.09, 0.07, 6)
        else:
            cil(b, x + s * 0.12, y, z, 0.09, 0.85, 6)
    cil(b, x, y, z + 0.82, 0.24, 0.65, 8)
    cil(rojo(), x, y, z + 0.85, 0.25, 0.12, 8)
    cil(rojo(), x, y, z + 1.4, 0.16, 0.1, 8)
    esfera(piel(), x, y, z + 1.68, 0.18, 1)
    for s in (-1, 1):
        rama(b, (x + s * 0.24, y, z + 1.35), (x + s * 0.4, y - 0.25, z + 1.7 if corre else z + 1.0), 0.06, 0.05, 5)

# ================================================================ la meta
def teatro_chino():
    """El teatro chino de Hollywood (la meta): el tejado de pagoda verde y
    rojo, las dos columnas rojas, el dragón de la fachada, el patio con las
    losas de las huellas y, detrás, las colinas con las letras que ha puesto
    España: LOS ÁNGELES. Delante, la pancarta LOS ÁNGELES ES ESPAÑOL."""
    Y = 18
    yf = Y - 8
    r = rojo()
    caja(mat('fachada_chino_la', 0xc8a070, 0.8), 0, Y, 0, 30, 16, 12)
    for s in (-1, 1):
        cil(r, s * 5, yf - 3, 0, 0.6, 12, 12)
        caja(mat('pagoda_verde_la', 0x2a6a5a, 0.6), s * 9, yf - 1, 10, 10, 6, 0.6)
    # Los tejados de pagoda (tres, uno encima de otro).
    for k, (w, z) in enumerate(((18, 12.0), (13, 16.0), (8, 19.5))):
        caja(mat('pagoda_verde_la', 0x2a6a5a, 0.6), 0, yf - 0.5, z, w, 8 - k * 1.5, 0.6)
        for s in (-1, 1):
            rama(mat('pagoda_verde_la', 0x2a6a5a, 0.6), (s * w / 2, yf - 0.5, z + 0.3), (s * (w / 2 + 1.2), yf - 0.5, z + 1.2), 0.25, 0.1, 5)
        caja(r, 0, yf - 0.5, z - 1.8, w - 1.5, 6 - k * 1.5, 1.8)
    cil(oro(), 0, yf - 0.5, 20.1, 0.4, 2.5, 8, r2=0.05)
    # El dragón (una silueta de cobre verde en la fachada).
    dm = mat('dragon_la', 0x3a8a6a, 0.4)
    for k in range(8):
        esfera(dm, -4 + k * 1.1, yf - 1.1, 9 + math.sin(k * 0.9) * 0.6, 0.45, 1, esc=(1.2, 0.4, 0.8))
    esfera(dm, 4.8, yf - 1.1, 9.6, 0.7, 1, esc=(1.3, 0.5, 1))
    caja(cristal(), 0, yf - 0.05, 0, 6, 0.1, 4)
    # El patio con las losas de las huellas.
    for k in range(10):
        x = -13 + (k % 5) * 6.5
        y = yf - 6 - (k // 5) * 5
        caja(mat('losa_la', 0xd0c8b8, 0.8), x, y, 0, 2.2, 2.2, 0.08)
        esfera(gris(), x - 0.4, y, 0.08, 0.2, 1, esc=(1, 1.3, 0.2))
        esfera(gris(), x + 0.4, y, 0.08, 0.2, 1, esc=(1, 1.3, 0.2))
    # Las colinas con las letras LOS ÁNGELES.
    o = cil(colina(), 0, Y + 40, 0, 60, 30, 10, r2=20)
    o.scale = (1.6, 0.6, 1)
    texto(blanco(), 'LOS ÁNGELES', 0, Y + 20, 20, tam=6.0, prof=0.4).rotation_euler = (math.pi / 2 - 0.35, 0, 0)
    # La pancarta.
    for x in (8, 22):
        cil(madera_o(), x, yf - 16, 0, 0.12, 4.4, 8)
    caja(bandera_es('pancarta_es_la', 2.8, 1.6), 15, yf - 16, 2.8, 14, 0.06, 1.6)
    texto(negro(), 'LOS ÁNGELES ES ESPAÑOL', 15, yf - 16.04, 3.35, tam=0.68, prof=0.03)

# ================================================================ edificios
def capitol_records():
    """La torre de Capitol Records (1956): redonda como una pila de discos,
    con los parasoles de cada piso y la aguja encima."""
    Y = 12
    caja(mat('base_cr_la', 0xd8d0c0, 0.7), 0, Y, 0, 20, 14, 4)
    b = blanco()
    for k in range(13):
        z = 4 + k * 2.6
        cil(cristal(), 0, Y, z, 7.0, 2.6, 24)
        cil(b, 0, Y, z + 2.2, 8.0, 0.35, 24)
    cil(b, 0, Y, 37.8, 6, 1.2, 24)
    cil(gris(), 0, Y, 39, 0.2, 9, 6)
    esfera(neon_r(), 0, Y, 48.2, 0.4, 1)
    caja(b, 0, Y - 7.1, 2.0, 10, 0.1, 1.2)
    texto(negro(), 'CAPITOL RECORDS', 0, Y - 7.16, 2.2, tam=0.75, prof=0.03)

def el_capitan():
    """El teatro El Capitan (1926): la fachada de estuco con arcos y
    columnitas y la gran marquesina con bombillas y EL CAPITAN."""
    Y = 8
    W, D, H = 22.0, 12.0, 15.0
    yf = Y - D / 2
    e = estuco()
    caja(e, 0, Y, 0, W, D, H)
    for x in (-7, -3.5, 0, 3.5, 7):
        cil(cristal(), x, yf - 0.05, 9.0, 1.2, 0.1, 14, eje='Y')
        caja(cristal(), x, yf - 0.05, 6.5, 2.4, 0.1, 2.5)
        for s in (-1, 1):
            cil(oro(), x + s * 1.35, yf - 0.2, 6.5, 0.15, 4.0, 8)
    caja(mat('marquesina_ec_la', 0x2a2a3a, 0.5), 0, yf - 1.8, 3.4, 18, 3.6, 1.6)
    for k in range(34):
        caja(bombilla(), -8.3 + k * 0.5, yf - 3.62, 4.85, 0.14, 0.06, 0.14)
    caja(blanco(), 0, yf - 3.65, 3.55, 16, 0.06, 1.15)
    texto(rojo(), 'EL CAPITAN', 0, yf - 3.7, 3.8, tam=0.8, prof=0.02)
    caja(rojo(), 0, yf - 1.0, 5.2, 1.4, 1.2, 9)
    for k, ch in enumerate('CAPITAN'):
        texto(amarillo(), ch, 0, yf - 1.62, 13.3 - k * 1.15, tam=0.95, prof=0.03)

def hotel_roosevelt():
    """El hotel Roosevelt (1927): estilo colonial español, el estuco claro,
    las tejas, la torre y el gran letrero rojo de neón en lo alto."""
    Y = 10
    e = estuco()
    caja(e, 0, Y, 0, 30, 16, 18)
    tejado(teja(), 0, Y - 8, Y + 8, 18, 30, 3, cumbrera='x')
    caja(e, 6, Y - 1, 18, 10, 10, 10)
    tejado(teja(), 6, Y - 6, Y + 4, 28, 10, 2.5, cumbrera='x')
    for k in range(7):
        x = -12 + k * 4
        for z in (2, 6, 10, 14):
            ventana(x, z, 1.6, 2.2, y=Y - 8 - 0.05, marco=madera_o(), cristal=cristal())
    for x in (3, 9):
        for z in (20, 24):
            ventana(x, z, 1.4, 2.0, y=Y - 6 - 0.05, marco=madera_o(), cristal=cristal())
    for x in (2, 10):
        caja(hierro(), x, Y - 1, 28, 0.2, 0.2, 5)
    caja(hierro(), 6, Y - 1, 32.6, 9, 0.2, 0.2)
    texto(neon_r(), 'ROOSEVELT', 6, Y - 1.1, 29.8, tam=1.4, prof=0.1)
    caja(blanco(), 0, Y - 8.1, 3.4, 10, 0.1, 1.0)
    texto(rojo(), 'HOLLYWOOD ROOSEVELT', 0, Y - 8.16, 3.6, tam=0.5, prof=0.02)

def estrella_fama():
    """La estrella del Paseo de la Fama (para la acera): el cuadro de
    terrazo oscuro, la estrella rosa con el borde dorado y el nombre TRUMP."""
    caja(mat('terrazo_la', 0x2a2a30, 0.3), 0, 0, 0, 1.6, 1.6, 0.06)
    r = rosa()
    for k in range(5):
        a = k * math.tau / 5 + math.pi / 2
        rama(r, (0, 0, 0.07), (math.cos(a) * 0.62, math.sin(a) * 0.62, 0.07), 0.22, 0.02, 3)
    cil(r, 0, 0, 0.06, 0.28, 0.02, 10)
    cil(oro(), 0, 0, 0.08, 0.14, 0.02, 10)
    texto(oro(), 'TRUMP', 0, -0.25, 0.1, tam=0.14, prof=0.01).rotation_euler = (0, 0, 0)

# ================================================================ cruza la calle
def arco_san_fermin():
    """El arco del encierro: dos postes y la pancarta roja y blanca ¡VIVA SAN
    FERMÍN!, con pañuelos rojos colgando; por detrás, ¡OLÉ!"""
    for s in (-1, 1):
        caja(blanco(), s * 8.6, 0, 0, 0.6, 0.6, 7.8)
    caja(blanco(), 0, 0, 7.0, 18.0, 0.4, 0.5)
    caja(rojo(), 0, 0, 4.4, 12, 0.18, 1.8)
    caja(blanco(), 0, -0.02, 4.6, 11.6, 0.18, 1.4)
    texto(rojo(), '¡VIVA SAN FERMÍN!', 0, -0.13, 5.0, tam=0.8, prof=0.04)
    o = texto(rojo(), '¡OLÉ!', 0, 0.13, 5.0, tam=1.0, prof=0.04)
    o.rotation_euler = (math.pi / 2, 0, math.pi)
    for k in range(14):
        x = -7.8 + k * 1.2
        cil(rojo(), x, 0, 6.2, 0.25, 0.7, 3, r2=0.0).rotation_euler = (math.pi, 0, 0)

# ================================================================ el plató
def plato_cine():
    """El plató de cine (momento estrella, al aire libre): fachadas falsas a
    los dos lados (el pueblo del Oeste, las casas de Nueva York, un castillo)
    con sus puntales por detrás, las cámaras en sus grúas, los focos, las
    sillas del director, las claquetas gigantes, el depósito de agua y los
    carteles SILENCIO, SE RUEDA. Cruza la calle: el origen en el centro."""
    L = 420
    caja(mat('suelo_plato_la', 0x9a948a, 0.9), 0, 0, -0.2, 26, L, 0.2)
    fachadas = [(0xc89a6a, 'SALOON'), (0x8a4a3a, 'BROOKLYN'), (0x9a9aa0, 'CASTLE'), (0xd8c8a8, 'BANK'), (0x6a8a6a, 'HOTEL')]
    for s in (-1, 1):
        for k in range(int(L / 16)):
            y = -L / 2 + 8 + k * 16
            c, txt = fachadas[(k + (s > 0) * 2) % 5]
            caja(mat(f'fachada_falsa_la{(k + (s > 0) * 2) % 5}', c, 0.8), s * 11, y, 0, 0.4, 14, 7 + (k % 3) * 2)
            for x in (-4, 0, 4):
                caja(cristal(), s * 10.78, y + x, 2.5, 0.05, 1.6, 2.0)
            caja(blanco(), s * 10.76, y, 6.0, 0.05, 6, 1.0)
            texto(negro(), txt, s * 10.7, y, 6.2, tam=0.6, prof=0.02).rotation_euler = (math.pi / 2, 0, -s * math.pi / 2)
            rama(madera(), (s * 11.2, y - 5, 6), (s * 14, y - 5, 0), 0.1, 0.1, 4)
            rama(madera(), (s * 11.2, y + 5, 6), (s * 14, y + 5, 0), 0.1, 0.1, 4)
    for k in range(int(L / 40)):
        y = -L / 2 + 20 + k * 40
        s = 1 if k % 2 else -1
        # La grúa con la cámara.
        caja(hierro(), s * 7.6, y, 0, 1.6, 2.4, 0.5)
        rama(hierro(), (s * 7.6, y, 0.5), (s * 5.4, y - 1.5, 4.8), 0.12, 0.1, 6)
        caja(negro(), s * 5.2, y - 1.6, 4.6, 0.8, 1.2, 0.8)
        cil(negro(), s * 5.2, y - 2.3, 5.0, 0.25, 0.4, 10, eje='Y')
        # Focos y silla del director.
        cil(hierro(), -s * 7.4, y + 6, 0, 0.05, 3.0, 6)
        cil(mat('foco_la', 0xf6f0d8, 0.3), -s * 7.4, y + 5.7, 3.0, 0.45, 0.6, 12, eje='Y')
        caja(madera(), s * 7.8, y + 10, 0.5, 0.8, 0.7, 0.08)
        caja(negro(), s * 7.8, y + 10.3, 0.5, 0.8, 0.06, 0.8)
        for dx in (-0.35, 0.35):
            for dy in (-0.3, 0.3):
                cil(madera(), s * 7.8 + dx, y + 10 + dy, 0, 0.03, 0.55, 4)
        # La claqueta gigante.
        caja(negro(), -s * 7.8, y + 16, 0, 0.15, 2.0, 1.6)
        caja(mat_franjas('claqueta_la', 0x1c1c20, 0xf6f4ee, 6, eje='Y', z0=-1, alto=2), -s * 7.8, y + 16, 1.6, 0.16, 2.0, 0.35)
    for k in range(int(L / 70)):
        y = -L / 2 + 35 + k * 70
        for s in (-1, 1):
            caja(rojo(), s * 7.6, y, 3.6, 0.1, 4.0, 1.0)
            texto(blanco(), 'SILENCIO, SE RUEDA', s * 7.53, y, 3.85, tam=0.38, prof=0.02).rotation_euler = (math.pi / 2, 0, -s * math.pi / 2)
    # El depósito de agua del estudio.
    for s in (-1, 1):
        cil(hierro(), s * 22, 30, 0, 0.3, 14, 6)
    cil(mat('deposito_la', 0xd8d0c0, 0.6), 0 - 22, 30, 14, 4, 5, 16)
    for (y, txt) in ((-L / 2 + 1, 'SALIDA'), (L / 2 - 1, 'META')):
        for s in (-1, 1):
            caja(negro(), s * 7.0, y, 0, 0.5, 0.5, 6.2)
        caja(negro(), 0, y, 5.6, 14.6, 0.5, 0.6)
        caja(mat_franjas('claqueta_arco_la', 0x1c1c20, 0xf6f4ee, 8, eje='X', z0=-6, alto=12), 0, y, 4.0, 12, 0.16, 1.4)
        texto(amarillo(), 'TOMA 1 · ' + txt, 0, y - 0.1, 4.45, tam=0.55, prof=0.04)

# ================================================================ obstáculos
def hamaca():
    """La hamaca colgada entre dos postes con uno durmiendo la siesta dentro
    (agacharse): la red a rayas y el que ronca, con el periódico en la cara."""
    for x in (-1.15, 1.15):
        cil(madera(), x, 0, 0, 0.07, 2.4, 8)
    m = mat_franjas('hamaca_la', 0xc8202a, 0xf2c21a, 5, eje='X', z0=-1.1, alto=2.2)
    esfera(m, 0, 0, 1.75, 0.5, 2, esc=(2.2, 0.75, 0.4))
    esfera(blanco(), -0.2, 0, 2.0, 0.5, 2, esc=(1.4, 0.5, 0.3))
    esfera(piel(), 0.75, 0, 2.05, 0.17, 1)
    caja(mat('periodico_la', 0xe8e4d8, 0.8), 0.75, -0.06, 2.12, 0.4, 0.3, 0.02)
    for x in (-1.15, 1.15):
        rama(hierro(), (x, 0, 2.3), (x * 0.85, 0, 1.95), 0.02, 0.02, 4)

def dormilon():
    """El dormilón tumbado en una esterilla, con la boina y el periódico en
    la cara (se salta; con cuidado, que se despierta)."""
    caja(mat_franjas('esterilla_la', 0x2a6ab8, 0xf6f4ee, 6, eje='X', z0=-0.9, alto=1.8), 0, 0, 0, 1.8, 0.8, 0.04)
    esfera(blanco(), -0.1, 0, 0.2, 0.5, 2, esc=(1.4, 0.55, 0.38))
    esfera(piel(), 0.68, 0, 0.22, 0.18, 1)
    cil(negro(), 0.74, 0, 0.36, 0.2, 0.06, 12)
    caja(mat('periodico_la', 0xe8e4d8, 0.8), 0.6, -0.06, 0.36, 0.35, 0.32, 0.02)
    for s in (-1, 1):
        cil(mat('pantalon_la', 0x3a3a42, 0.7), -0.75, s * 0.12, 0.1, 0.09, 0.6, 6, eje='X')
    texto(azul(), 'Zzz', 0.3, -0.05, 0.75, tam=0.22, prof=0.02)

def mozo():
    """El mozo de San Fermín corriendo (no se pasa): de blanco con el pañuelo
    y la faja rojos, y el periódico enrollado en la mano."""
    persona_blanca(0, 0, 0, corre=True)
    cil(mat('periodico_la', 0xe8e4d8, 0.8), 0.42, -0.3, 1.7, 0.05, 0.4, 6)

def camara_cine():
    """La cámara de cine en su carro (no se pasa): el carro con ruedas, el
    trípode, la cámara negra con sus dos bobinas y el foco."""
    caja(hierro(), 0, 0, 0.15, 1.2, 1.6, 0.25)
    for (x, y) in ((-0.5, -0.6), (0.5, -0.6), (-0.5, 0.6), (0.5, 0.6)):
        cil(negro(), x, y, 0, 0.15, 0.15, 10)
    cil(hierro(), 0, 0, 0.4, 0.08, 1.0, 6)
    caja(negro(), 0, 0, 1.4, 0.5, 0.9, 0.55)
    for y in (-0.2, 0.25):
        cil(negro(), 0, y, 2.15, 0.3, 0.08, 16, eje='X')
    cil(negro(), 0, -0.55, 1.65, 0.16, 0.35, 10, eje='Y')
    cil(cristal(), 0, -0.74, 1.65, 0.12, 0.03, 10, eje='Y')

def autobus_estrellas():
    """El autobús descapotable de las casas de las estrellas (no se pasa):
    rosa, con los asientos al aire y el letrero. El morro en el origen."""
    r = rosa()
    caja(r, 0, 4.5, 0.4, 2.5, 9.0, 1.6)
    caja(cristal(), 0, 0.02, 1.4, 2.2, 0.1, 0.6)
    for y in range(2, 9, 2):
        caja(madera(), 0, y, 2.0, 2.2, 0.5, 0.15)
        caja(madera(), 0, y + 0.3, 2.0, 2.2, 0.08, 0.5)
    caja(blanco(), 0, -0.02, 0.6, 2.3, 0.05, 0.4)
    texto(rojo(), 'STAR TOUR', 0, -0.04, 0.66, tam=0.22, prof=0.01)
    for (y, s) in ((1.0, 1), (7.8, 1), (1.0, -1), (7.8, -1)):
        cil(negro(), s * 1.15, y, 0.4, 0.4, 0.3, 14, eje='X')
    for s in (-1, 1):
        caja(luz('faro_bus_la', 0xfff2c0, 1.0), s * 0.85, -0.03, 1.0, 0.35, 0.05, 0.2)

def cartel_la():
    """La pancarta de España (agacharse): LOS ÁNGELES ES ESPAÑOL."""
    for x in (-1.25, 1.25):
        cil(madera_o(), x, 0, 0, 0.07, 2.75, 8)
    caja(bandera_es('pancarta_es_obst_la', 1.5, 1.2), 0, 0, 1.5, 2.4, 0.05, 1.2)
    texto(negro(), 'LOS ÁNGELES', 0, -0.035, 2.2, tam=0.28, prof=0.02)
    texto(negro(), 'ES ESPAÑOL', 0, -0.035, 1.78, tam=0.26, prof=0.02)

PIEZAS = {
    'teatro_chino':      (teatro_chino,      'losangeles', dict(lado=2048, bisel=0.0)),
    'capitol_records':   (capitol_records,   'losangeles', dict(lado=1024, bisel=0.0)),
    'el_capitan':        (el_capitan,        'losangeles', dict(lado=1024, bisel=0.0)),
    'hotel_roosevelt':   (hotel_roosevelt,   'losangeles', dict(lado=1024, bisel=0.0)),
    'estrella_fama':     (estrella_fama,     'losangeles', dict(lado=256, bisel=0.0)),
    'arco_san_fermin':   (arco_san_fermin,   'losangeles', dict(lado=1024, bisel=0.0, suelo=False)),
    'plato_cine':        (plato_cine,        'losangeles', dict(lado=2048, bisel=0.0, suelo=False)),
    'hamaca':            (hamaca,            'obstaculos', dict(lado=256, bisel=0.0)),
    'dormilon':          (dormilon,          'obstaculos', dict(lado=256, bisel=0.0)),
    'mozo':              (mozo,              'obstaculos', dict(lado=256, bisel=0.0)),
    'camara_cine':       (camara_cine,       'obstaculos', dict(lado=256, bisel=0.0)),
    'autobus_estrellas': (autobus_estrellas, 'obstaculos', dict(lado=256, bisel=0.0)),
    'cartel_la':         (cartel_la,         'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
}

correr(PIEZAS)
