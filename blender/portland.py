# Nivel 35: Portland, Oregón (15/11/2026).
#
#   blender -b -P blender/portland.py -- [pieza ...] [--rapido]
#
# Historia: «Manifestantes disfrazados de rana hinchable (pasó de verdad)».
#   Acto de la Armada Española. Por Burnside Street hasta el letrero PORTLAND
#   OREGON con el ciervo que salta (White Stag): la librería Powell's, el
#   Portland Building con la estatua de Portlandia, la estación con su torre
#   GO BY TRAIN, el arco de rosas (la ciudad de las rosas) y los carritos de
#   comida. Las ranas hinchables tapan la calle: hay que tocarlas en la
#   pantalla para deshincharlas; y el momento estrella, la regata de barcos
#   dragón del Festival de las Rosas en el río Willamette (remar deslizando a
#   izquierda y derecha, alternando). Pancartas de España: ¿OREGÓN? ¡VIENE DE
#   OREJÓN! (una de las teorías del nombre).
# Obstáculos (carpeta obstaculos): la rana hinchable, la pancarta, el food
# truck, las bicis aparcadas y el barco dragón (se monta: es un vehículo).

import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import *

def blanco():    return mat('blanco_pdx', 0xf6f4ee, 0.5)
def negro():     return mat('negro_pdx', 0x1c1c20, 0.4)
def cristal():   return mat('cristal_pdx', 0x3a5a70, 0.15)
def rojo():      return mat('rojo_pdx', 0xc8202a, 0.45)
def azul():      return mat('azul_pdx', 0x2a4a9a, 0.45)
def amarillo():  return mat('amarillo_pdx', 0xf2c21a, 0.45)
def verde():     return mat('verde_pdx', 0x2a7a3a, 0.5)
def rosa():      return mat('rosa_pdx', 0xe84a7a, 0.5)
def gris():      return mat('gris_pdx', 0x8a9098, 0.4)
def hierro():    return mat('hierro_pdx', 0x2a2c30, 0.45)
def madera():    return mat('madera_pdx', 0x8a5a34, 0.85)
def madera_o():  return mat('madera_oscura_pdx', 0x5a3a22, 0.85)
def ladrillo():  return mat_bloques('ladrillo_pdx', 0xa85a3e, 0x7a4030, ancho=0.4, alto=0.16)
def piedra():    return mat('piedra_pdx', 0xe0d6c0, 0.7)
def cobre():     return mat('cobre_pdx', 0x6a8a6a, 0.4)
def oro():       return mat('oro_pdx', 0xe8b840, 0.25)
def piel():      return mat('piel_pdx', 0xe8b89a, 0.7)
def rana_v():    return mat('rana_verde_pdx', 0x5ac83a, 0.35)
def rana_c():    return mat('rana_clara_pdx', 0xc8f08a, 0.35)
def neon_b():    return luz('neon_blanco_pdx', 0xfff6e0, 1.3)
def neon_r():    return luz('neon_rojo_pdx', 0xff3a2a, 1.3)

def bandera_es(nombre, z0, alto):
    return mat_franjas(nombre, 0xc8202a, 0xf2c21a, 3, eje='Z', z0=z0, alto=alto)

def ciervo(m, x, y, z, k=1.0):
    """El ciervo blanco saltando (de lado, mirando a +x)."""
    esfera(m, x, y, z, 0.9 * k, 2, esc=(1.6, 0.6, 0.75))
    rama(m, (x + 1.1 * k, y, z + 0.3 * k), (x + 1.7 * k, y, z + 1.1 * k), 0.35 * k, 0.25 * k, 8)
    esfera(m, x + 1.95 * k, y, z + 1.25 * k, 0.35 * k, 2, esc=(1.4, 0.8, 0.8))
    for s in (-1, 1):
        rama(m, (x + 1.75 * k, y + s * 0.15 * k, z + 1.5 * k), (x + 1.5 * k, y + s * 0.6 * k, z + 2.6 * k), 0.08 * k, 0.05 * k, 5)
        rama(m, (x + 1.6 * k, y + s * 0.4 * k, z + 2.1 * k), (x + 2.1 * k, y + s * 0.55 * k, z + 2.6 * k), 0.06 * k, 0.04 * k, 5)
    for (dx, ex, ez) in ((0.9, 2.0, -1.0), (0.7, 1.7, -1.4), (-0.9, -2.2, -0.6), (-0.7, -2.0, -1.1)):
        rama(m, (x + dx * k, y, z - 0.3 * k), (x + ex * k, y, z + ez * k), 0.14 * k, 0.08 * k, 6)
    esfera(rojo(), x + 2.4 * k, y, z + 1.2 * k, 0.15 * k, 1)

# ================================================================ la meta
def white_stag():
    """El letrero PORTLAND OREGON (la meta): el edificio de ladrillo del
    White Stag junto al puente Burnside y, en el tejado, el gran letrero con
    el mapa de Oregón, PORTLAND en blanco, OREGON en rojo y el ciervo que
    salta encima. Delante, la pancarta ¿OREGÓN? ¡VIENE DE OREJÓN!"""
    Y = 18
    W, D, H = 46.0, 18.0, 16.0
    yf = Y - D / 2
    l = ladrillo()
    caja(l, 0, Y, 0, W, D, H)
    caja(piedra(), 0, Y, H, W + 0.4, D + 0.4, 0.7)
    for k in range(10):
        x = -20 + k * 4.45
        for z in (1.5, 5.5, 9.5, 13.0):
            ventana(x, z, 1.8, 2.4, y=yf - 0.05, marco=piedra(), cristal=cristal())
    caja(piedra(), 0, yf - 0.1, 0, W, 0.2, 1.2)
    # La estructura del letrero.
    S = H + 0.7
    for x in (-14, -5, 5, 14):
        caja(hierro(), x, Y + 2, S, 0.4, 0.4, 13)
    for z in (S + 2, S + 7, S + 12):
        caja(hierro(), 0, Y + 2.3, z, 32, 0.3, 0.3)
    # El mapa de Oregón (amarillo) con su costa irregular.
    m = mat('mapa_oregon_pdx', 0xf2d24a, 0.5)
    caja(m, 1.5, Y + 1.6, S + 1.5, 27, 0.3, 11)
    for k in range(6):
        caja(m, -12.6 - (k % 2) * 0.5, Y + 1.6, S + 1.5 + k * 1.8, 1.4, 0.3, 1.9)
    texto(neon_b(), 'PORTLAND', 1.5, Y + 1.35, S + 6.2, tam=4.2, prof=0.25)
    texto(neon_r(), 'OREGON', 1.5, Y + 1.35, S + 2.0, tam=2.6, prof=0.25)
    ciervo(neon_b(), 1.0, Y + 1.5, S + 15.5, 2.0)
    # La acera, los árboles y la pancarta.
    caja(mat('acera_pdx', 0xb8b4ac, 0.8), 0, yf - 10, -0.05, 70, 20, 0.06)
    for (x, y) in ((-26, yf - 6), (26, yf - 6), (-32, yf - 14), (32, yf - 14)):
        cil(madera_o(), x, y, 0, 0.3, 3.0, 8)
        esfera(mat('copa_pdx', 0x3a7a3a, 0.85), x, y, 5.0, 2.8, 2, esc=(1, 1, 1.2))
    for x in (8, 22):
        cil(madera_o(), x, yf - 13, 0, 0.12, 4.4, 8)
    caja(bandera_es('pancarta_es_stag_pdx', 2.8, 1.6), 15, yf - 13, 2.8, 14, 0.06, 1.6)
    texto(negro(), '¿OREGÓN? ¡VIENE DE OREJÓN!', 15, yf - 13.04, 3.4, tam=0.62, prof=0.03)

# ================================================================ edificios
def powells():
    """La librería Powell's (City of Books): la manzana entera de dos pisos,
    los escaparates llenos de libros de colores y el letrero rojo y blanco en
    la esquina."""
    Y = 9
    W, D = 34.0, 14.0
    yf = Y - D / 2
    caja(mat('fachada_powells_pdx', 0xd8c8a8, 0.8), 0, Y, 0, W, D, 9)
    caja(rojo(), 0, Y, 9, W + 0.3, D + 0.3, 0.6)
    for k in range(6):
        x = -14 + k * 5.6
        caja(cristal(), x, yf - 0.05, 0.6, 4.4, 0.1, 3.0)
        for i in range(12):
            caja([rojo, azul, amarillo, verde, negro, blanco][(k + i) % 6](), x - 1.9 + i * 0.34, yf - 0.12, 0.7, 0.26, 0.12, 0.9 + (i % 3) * 0.2)
        ventana(x, 5.2, 3.6, 2.4, y=yf - 0.05, marco=blanco(), cristal=cristal())
    caja(blanco(), 0, yf - 0.3, 4.0, 22, 0.25, 1.2)
    texto(rojo(), "POWELL'S CITY OF BOOKS", 0, yf - 0.45, 4.2, tam=0.85, prof=0.04)
    caja(rojo(), 15.6, yf - 1.0, 2.0, 1.2, 1.2, 11)
    for k, c in enumerate("POWELL'S"):
        texto(blanco(), c, 15.6, yf - 1.62, 11.6 - k * 1.15, tam=0.95, prof=0.03)

def portland_building():
    """El Portland Building (1982): el cubo crema con la base verde azulada,
    las pilastras enormes marrones con su capitel, las ventanitas cuadradas y,
    encima de la entrada, Portlandia: la estatua de cobre de la mujer
    arrodillada con el tridente."""
    Y = 11
    W, D, H = 28.0, 20.0, 26.0
    yf = Y - D / 2
    caja(mat('base_pb_pdx', 0x4a8a8a, 0.6), 0, Y, 0, W + 2, D + 2, 5)
    caja(mat('crema_pb_pdx', 0xf0e4c8, 0.7), 0, Y, 5, W, D, H - 5)
    for x in range(-12, 13, 2):
        for z in range(7, 25, 2):
            if abs(x) > 6 or z > 21:
                caja(cristal(), x, yf - 0.05, z, 1.0, 0.1, 1.0)
    pil = mat('pilastra_pb_pdx', 0x8a3a2a, 0.6)
    for x in (-4, 4):
        caja(pil, x, yf - 0.3, 5, 3.0, 0.6, 14)
        caja(pil, x, yf - 0.6, 19, 4.2, 1.2, 2.2)
    caja(mat('cristal_pb_pdx', 0x2a3a4a, 0.2), 0, yf - 0.1, 7, 5, 0.1, 12)
    caja(mat('remate_pb_pdx', 0x4a8a8a, 0.6), 0, Y, H, W + 0.4, D + 0.4, 1.0)
    # Portlandia.
    c = cobre()
    caja(piedra(), -9, yf - 1.6, 5, 4, 3, 0.6)
    esfera(c, -9, yf - 1.6, 6.7, 0.8, 2, esc=(1.1, 0.9, 1.0))
    cil(c, -9, yf - 1.6, 7.3, 0.55, 2.0, 10, r2=0.45)
    esfera(c, -9, yf - 1.7, 9.7, 0.45, 2)
    rama(c, (-8.5, yf - 1.6, 8.8), (-6.8, yf - 2.6, 9.2), 0.16, 0.12, 6)
    cil(c, -6.6, yf - 2.7, 5.6, 0.07, 6.5, 6)
    for dx in (-0.35, 0, 0.35):
        cil(c, -6.6 + dx, yf - 2.7, 12.0, 0.05, 0.8, 4, r2=0.01)
    texto(blanco(), 'THE PORTLAND BUILDING', 0, yf - 1.12, 2.0, tam=0.6, prof=0.03)

def union_station_pdx():
    """La estación de Portland (1896): ladrillo y piedra, la torre del reloj
    con su tejado de pirámide y los letreros de neón GO BY TRAIN y UNION
    STATION."""
    Y = 9
    W, D = 40.0, 14.0
    yf = Y - D / 2
    l = ladrillo()
    caja(l, 4, Y, 0, 32, D, 8)
    caja(piedra(), 4, Y, 0, 32.2, D + 0.2, 1.0)
    tejado(mat('tejado_us_pdx', 0x5a4a44, 0.6), 4, Y - D / 2, Y + D / 2, 8, 32, 3.4, cumbrera='x')
    for x in (-8, -3, 2, 7, 12, 17):
        ventana(x, 1.6, 1.6, 3.0, y=yf - 0.05, marco=piedra(), cristal=cristal())
        ventana(x, 5.4, 1.4, 1.8, y=yf - 0.05, marco=piedra(), cristal=cristal())
    caja(mat('letrero_us_pdx', 0x2a2a30, 0.5), 4, yf - 0.4, 8.6, 14, 0.2, 1.2)
    texto(neon_r(), 'UNION STATION', 4, yf - 0.55, 8.8, tam=0.9, prof=0.05)
    # La torre.
    T = 5.6
    x0 = -15
    caja(l, x0, yf + 1, 0, T, T, 28)
    for z in (8, 18):
        caja(piedra(), x0, yf + 1, z, T + 0.4, T + 0.4, 0.5)
    cil(blanco(), x0, yf + 1 - T / 2 - 0.1, 20.5, 1.7, 0.12, 24, eje='Y')
    caja(negro(), x0, yf + 1 - T / 2 - 0.2, 20.5, 0.1, 0.04, 1.3)
    caja(negro(), x0 + 0.4, yf + 1 - T / 2 - 0.2, 20.5, 0.85, 0.04, 0.1)
    for (k, w) in enumerate(('GO', 'BY', 'TRAIN')):
        texto(neon_r(), w, x0, yf + 1 - T / 2 - 0.15, 15.6 - k * 1.9, tam=1.3, prof=0.06)
    o = cil(mat('tejado_torre_pdx', 0x4a5a5a, 0.6), x0, yf + 1, 28, T * 0.74, 6, 4, r2=0.1)
    o.rotation_euler = (0, 0, math.pi / 4)
    cil(hierro(), x0, yf + 1, 34, 0.08, 2.0, 6)

def carrito_comida():
    """Un carrito de comida (food cart) de los de Portland, con su ventanilla,
    el toldo y la pizarra del menú (para la acera)."""
    caja(mat('cart_pdx', 0x2a8ab8, 0.5), 0, 0, 0.35, 3.0, 1.8, 2.3)
    caja(blanco(), 0, -0.91, 1.3, 1.6, 0.05, 0.9)
    caja(madera(), 0, -1.1, 1.25, 1.8, 0.4, 0.08)
    cil(negro(), -1.0, 0, 0.0, 0.3, 0.2, 12, eje='X')
    cil(negro(), 1.0, 0, 0.0, 0.3, 0.2, 12, eje='X')
    caja(mat_franjas('toldo_cart_pdx', 0xf2c21a, 0xf6f4ee, 6, eje='X', z0=-1.5, alto=3.0), 0, -1.2, 2.3, 3.0, 0.8, 0.08, inclina=0.25)
    caja(negro(), 1.9, -0.6, 0, 0.7, 0.05, 1.1)
    texto(blanco(), 'TACOS', 1.9, -0.63, 0.8, tam=0.16, prof=0.01)
    texto(amarillo(), 'KEEP PORTLAND WEIRD', 0, -0.94, 2.15, tam=0.14, prof=0.01)

# ================================================================ cruza la calle
def arco_rosas():
    """El arco de rosas (Portland, la ciudad de las rosas): el arco verde
    cubierto de rosas rojas y rosas, con CITY OF ROSES y, por detrás, KEEP
    PORTLAND WEIRD."""
    v = mat('seto_pdx', 0x3a7a3a, 0.85)
    n = 40
    for k in range(n):
        u0, u1 = k / n, (k + 1) / n
        p0 = (-8.4 + 16.8 * u0, 0, 7.6 * math.sin(math.pi * u0) + 0.0)
        p1 = (-8.4 + 16.8 * u1, 0, 7.6 * math.sin(math.pi * u1) + 0.0)
        rama(v, p0, p1, 0.45, 0.45, 8)
        if k % 2 == 0:
            esfera([rosa, rojo][k % 4 // 2](), p0[0], -0.35, p0[2], 0.3, 1)
            esfera([rojo, rosa][k % 4 // 2](), p0[0], 0.35, p0[2] + 0.2, 0.28, 1)
    for s in (-1, 1):
        caja(v, s * 8.4, 0, 0, 1.2, 1.2, 1.6)
    caja(blanco(), 0, 0, 5.2, 8, 0.15, 1.1)
    texto(rosa(), 'CITY OF ROSES', 0, -0.1, 5.45, tam=0.75, prof=0.04)
    o = texto(verde(), 'KEEP PORTLAND WEIRD', 0, 0.1, 5.5, tam=0.62, prof=0.04)
    o.rotation_euler = (math.pi / 2, 0, math.pi)

# ================================================================ el río
def rio_willamette():
    """El río Willamette en el Festival de las Rosas (momento estrella): el
    agua, las boyas de las calles de la regata, las orillas con césped y
    público, los barcos dragón amarrados, el puente Hawthorne (verde, de
    celosía, con sus dos torres) y el puente Steel por encima, y los arcos de
    SALIDA y META. Cruza la calle: el origen en el centro."""
    L = 420
    caja(mat_franjas('agua_rio_pdx', 0x3a6a8a, 0x467a98, 60, eje='Y', z0=-L / 2, alto=L), 0, 0, -0.2, 34, L, 0.2)
    for s in (-1, 1):
        # Las orillas: el muro, el césped, el paseo y el público.
        caja(mat('muro_rio_pdx', 0x9a948a, 0.8), s * 17.5, 0, -0.2, 1.0, L, 1.6)
        caja(mat('cesped_pdx', 0x6a9a48, 0.9), s * 22, 0, 1.2, 8, L, 0.2)
        for g in range(3):
            caja(mat_bloques('gente_pdx', 0x8a5a7a, 0x2a2a30, ancho=0.5, alto=0.7, variacion=1.7), s * (26 + g * 2.6), 0, 1.4, 2.6, L, 1.2 + g * 1.4)
        for k in range(int(L / 30)):
            y = -L / 2 + 15 + k * 30
            cil(madera_o(), s * 19.5, y, 1.4, 0.3, 3.0, 8)
            esfera(mat('copa_pdx', 0x3a7a3a, 0.85), s * 19.5, y, 5.2, 2.6, 2, esc=(1, 1, 1.2))
        # Las boyas de las calles de la regata.
        for x in (1.1, 3.3):
            for k in range(int(L / 3)):
                esfera([rojo, blanco][k % 2](), s * x, -L / 2 + 1.5 + k * 3, 0.02, 0.18, 1)
        # Barcos dragón amarrados en la orilla.
        for k in range(int(L / 50)):
            y = -L / 2 + 25 + k * 50
            esfera(mat(f'barco_amarrado_pdx{k % 3}', [0xc8202a, 0x2a6a3a, 0x2a4a9a][k % 3], 0.5), s * 14.5, y, 0.2, 0.5, 2, esc=(1.4, 9.0, 0.7))
    # Los puentes por encima.
    vh = mat('puente_hawthorne_pdx', 0x3a7a5a, 0.5)
    yb = -80
    for s in (-1, 1):
        caja(vh, s * 15, yb, 0, 3, 3, 26)
    caja(vh, 0, yb, 13, 34, 4, 1.0)
    for k in range(9):
        x = -16 + k * 4
        rama(vh, (x, yb - 1.8, 14), (x + 4, yb - 1.8, 19), 0.15, 0.15, 4)
        rama(vh, (x, yb - 1.8, 19), (x + 4, yb - 1.8, 14), 0.15, 0.15, 4)
    caja(vh, 0, yb - 1.8, 19, 34, 0.4, 0.4)
    caja(blanco(), 0, yb - 2.1, 15.2, 10, 0.1, 1.2)
    texto(verde(), 'HAWTHORNE BRIDGE', 0, yb - 2.2, 15.5, tam=0.6, prof=0.03)
    vs = hierro()
    ys = 110
    for s in (-1, 1):
        caja(vs, s * 16, ys, 0, 3, 3, 24)
    caja(vs, 0, ys, 15, 35, 5, 1.2)
    for k in range(10):
        caja(vs, -16 + k * 3.6, ys - 2.4, 16.2, 0.3, 0.3, 4)
    caja(vs, 0, ys - 2.4, 20, 35, 0.4, 0.4)
    for (y, txt) in ((-L / 2 + 1, 'SALIDA'), (L / 2 - 1, 'META')):
        for s in (-1, 1):
            caja(madera(), s * 5.0, y, -0.2, 0.6, 0.6, 6.2)
        caja(madera(), 0, y, 5.4, 10.6, 0.5, 0.6)
        caja(rosa(), 0, y, 3.8, 9.0, 0.16, 1.4)
        texto(blanco(), 'DRAGON BOATS · ' + txt, 0, y - 0.1, 4.25, tam=0.55, prof=0.04)

# ================================================================ obstáculos
def rana_hinchable():
    """El manifestante disfrazado de rana hinchable (no se pasa: se toca en
    la pantalla para deshincharlo): el cuerpo verde y redondo, la tripa clara,
    los ojos saltones, la boca sonriente, los brazos abiertos y las piernas
    del que va dentro."""
    v = rana_v()
    cil(negro(), -0.25, 0, 0, 0.12, 0.5, 8)
    cil(negro(), 0.25, 0, 0, 0.12, 0.5, 8)
    esfera(v, 0, 0, 1.25, 0.8, 2, esc=(1.0, 0.85, 1.05))
    esfera(rana_c(), 0, -0.42, 1.15, 0.6, 2, esc=(0.95, 0.5, 0.95))
    esfera(v, 0, -0.05, 2.0, 0.62, 2, esc=(1.05, 0.95, 0.75))
    for s in (-1, 1):
        esfera(v, s * 0.32, -0.12, 2.45, 0.24, 2)
        esfera(blanco(), s * 0.32, -0.3, 2.5, 0.16, 2)
        esfera(negro(), s * 0.32, -0.43, 2.52, 0.08, 1)
        rama(v, (s * 0.7, 0, 1.6), (s * 1.15, -0.1, 2.15), 0.2, 0.15, 8)
        esfera(v, s * 1.2, -0.1, 2.25, 0.18, 1, esc=(1.2, 0.8, 0.6))
    rama(mat('boca_rana_pdx', 0x2a5a1a, 0.5), (-0.35, -0.6, 1.85), (0.35, -0.6, 1.85), 0.04, 0.04, 6)
    caja(blanco(), 0, -0.86, 0.85, 0.5, 0.02, 0.32)
    texto(negro(), 'CROAK', 0, -0.87, 0.92, tam=0.1, prof=0.005)

def cartel_oregon():
    """La pancarta de España (agacharse): ¿OREGÓN? ¡VIENE DE OREJÓN!"""
    for x in (-1.25, 1.25):
        cil(madera_o(), x, 0, 0, 0.07, 2.75, 8)
    caja(bandera_es('pancarta_es_obst_pdx', 1.5, 1.2), 0, 0, 1.5, 2.4, 0.05, 1.2)
    texto(negro(), '¿OREGÓN?', 0, -0.035, 2.2, tam=0.28, prof=0.02)
    texto(negro(), '¡VIENE DE OREJÓN!', 0, -0.035, 1.78, tam=0.18, prof=0.02)

def food_truck():
    """El food truck (no se pasa): la furgoneta de colores con la ventanilla
    abierta, el toldo y el menú. El morro en el origen."""
    c = mat('foodtruck_pdx', 0xe8701a, 0.45)
    caja(c, 0, 1.0, 0.4, 2.3, 2.0, 1.5)
    caja(cristal(), 0, 0.02, 1.15, 2.0, 0.1, 0.65)
    caja(c, 0, 4.0, 0.4, 2.4, 4.2, 2.5)
    caja(amarillo(), 0, 4.0, 2.9, 2.4, 4.2, 0.12)
    for s in (-1, 1):
        caja(negro(), s * 1.22, 4.0, 1.3, 0.05, 2.4, 0.9)
        caja(blanco(), s * 1.23, 4.0, 2.3, 0.05, 3.6, 0.35)
        texto(rojo(), 'TACO LOCO', s * 1.25, 4.0, 2.35, tam=0.22, prof=0.01).rotation_euler = (math.pi / 2, 0, -s * math.pi / 2)
    for (y, s) in ((1.0, 1), (5.3, 1), (1.0, -1), (5.3, -1)):
        cil(negro(), s * 1.1, y, 0.38, 0.38, 0.3, 14, eje='X')
    for s in (-1, 1):
        caja(luz('faro_ft_pdx', 0xfff2c0, 1.0), s * 0.8, -0.03, 0.75, 0.35, 0.05, 0.2)

def bicis_aparcadas():
    """El aparcabicis con tres bicis (se salta)."""
    for x in (-0.8, 0, 0.8):
        rama(hierro(), (x - 0.3, 0, 0), (x - 0.3, 0, 0.75), 0.03, 0.03, 6)
        rama(hierro(), (x + 0.3, 0, 0), (x + 0.3, 0, 0.75), 0.03, 0.03, 6)
        rama(hierro(), (x - 0.3, 0, 0.75), (x + 0.3, 0, 0.75), 0.03, 0.03, 6)
    for (k, x) in enumerate((-0.75, 0.05, 0.85)):
        c = [rojo, azul, amarillo][k]()
        for y in (-0.5, 0.5):
            o = cil(negro(), x, y, 0.33, 0.33, 0.04, 16, eje='X')
        rama(c, (x, -0.5, 0.33), (x, 0.05, 0.75), 0.03, 0.03, 6)
        rama(c, (x, 0.5, 0.33), (x, 0.05, 0.75), 0.03, 0.03, 6)
        rama(c, (x, -0.35, 0.8), (x, 0.3, 0.78), 0.03, 0.03, 6)
        caja(negro(), x, -0.4, 0.85, 0.45, 0.06, 0.05)

def barco_dragon():
    """El barco dragón de la regata (un vehículo: se va de pie en la popa,
    llevando el timón): la canoa larga, la cabeza de dragón con su crin, los
    remeros con sus palas, el tambor delante y la cola de dragón. El morro
    mira al jugador (-y); el juego le da la vuelta al montarlo."""
    L = 9.0
    c = mat('casco_dragon_pdx', 0xc8202a, 0.45)
    esfera(c, 0, L / 2, 0.3, 0.5, 2, esc=(1.25, L, 0.75))
    caja(mat('cubierta_dragon_pdx', 0x8a5a34, 0.8), 0, L / 2, 0.45, 1.0, L - 1.4, 0.12)
    caja(amarillo(), 0, L / 2, 0.15, 1.3, L - 1.0, 0.12)
    # La cabeza del dragón (delante) y la cola (detrás).
    o_ = oro()
    rama(c, (0, 0.6, 0.5), (0, -0.2, 1.4), 0.3, 0.25, 8)
    esfera(verde(), 0, -0.35, 1.55, 0.38, 2, esc=(0.9, 1.4, 0.9))
    for s in (-1, 1):
        esfera(blanco(), s * 0.2, -0.55, 1.75, 0.1, 1)
        esfera(negro(), s * 0.2, -0.63, 1.77, 0.05, 1)
        rama(o_, (s * 0.15, -0.2, 1.85), (s * 0.3, 0.1, 2.3), 0.05, 0.02, 5)
    caja(rojo(), 0, -0.75, 1.42, 0.3, 0.2, 0.12)
    for k in range(5):
        cil(o_, 0, 0.0 + k * 0.18, 1.6 + k * 0.05, 0.08, 0.3, 6, r2=0.01)
    rama(c, (0, L - 0.6, 0.5), (0, L + 0.3, 1.4), 0.25, 0.08, 8)
    for k in range(3):
        rama(verde(), (0, L + 0.2, 1.2 + k * 0.1), (0, L + 0.6, 1.7 + k * 0.2), 0.08, 0.02, 5)
    # El tambor y los remeros.
    cil(mat('tambor_pdx', 0x8a3a2a, 0.6), 0, 1.4, 0.55, 0.3, 0.5, 12)
    for k in range(5):
        y = 2.4 + k * 1.15
        for s in (-1, 1):
            cil(mat('chaleco_pdx', 0xf2c21a, 0.6), s * 0.3, y, 0.55, 0.18, 0.55, 6)
            esfera(piel(), s * 0.3, y, 1.25, 0.14, 1)
            rama(madera(), (s * 0.4, y, 1.0), (s * 0.85, y + 0.3, 0.1), 0.03, 0.03, 4)
            caja(madera(), s * 0.88, y + 0.32, 0.0, 0.08, 0.25, 0.35)

PIEZAS = {
    'white_stag':        (white_stag,        'portland',   dict(lado=2048, bisel=0.0)),
    'powells':           (powells,           'portland',   dict(lado=1024, bisel=0.0)),
    'portland_building': (portland_building, 'portland',   dict(lado=1024, bisel=0.0)),
    'union_station_pdx': (union_station_pdx, 'portland',   dict(lado=1024, bisel=0.0)),
    'carrito_comida':    (carrito_comida,    'portland',   dict(lado=256, bisel=0.0)),
    'arco_rosas':        (arco_rosas,        'portland',   dict(lado=1024, bisel=0.0, suelo=False)),
    'rio_willamette':    (rio_willamette,    'portland',   dict(lado=2048, bisel=0.0, suelo=False)),
    'rana_hinchable':    (rana_hinchable,    'obstaculos', dict(lado=256, bisel=0.0)),
    'cartel_oregon':     (cartel_oregon,     'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
    'food_truck':        (food_truck,        'obstaculos', dict(lado=256, bisel=0.0)),
    'bicis_aparcadas':   (bicis_aparcadas,   'obstaculos', dict(lado=256, bisel=0.0)),
    'barco_dragon':      (barco_dragon,      'obstaculos', dict(lado=256, bisel=0.0)),
}

correr(PIEZAS)
