# Nivel 19: Jackson, Misisipi (13/11/2026).
#
#   blender -b -P blender/jackson.py -- [pieza ...] [--rapido]
#
# Historia: «Barcos de vapor. Pajitas de papel que se deshacen (él volvió a
# las de plástico)».
#   Por Capitol Street (el viejo Capitolio griego, los bares de blues de Farish
#   Street, las magnolias) se embarca en un barco de vapor (por dentro: la
#   cubierta de madera, los camarotes blancos con balcones, las chimeneas
#   negras y las ruedas de paletas rojas a los lados) y se llega al Capitolio
#   de Misisipi, con el águila dorada en lo alto.
# Obstáculos (carpeta obstaculos): la pajita de papel gigante (de pie y, al
# acercarte, doblada en el suelo), el chorro de vapor que cruza la cubierta a
# la altura de la cabeza, la bala de algodón y la pancarta de las pajitas.

import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import *
from comun import _poner

def blanco():   return mat('blanco_ms', 0xf6f4ee, 0.5)
def negro():    return mat('negro_ms', 0x1b1c20, 0.4)
def rojo():     return mat('rojo_ms', 0xc8282c, 0.45)
def azul():     return mat('azul_ms', 0x1f4fa8, 0.45)
def madera():   return mat('madera_ms', 0xb88a5a, 0.8)
def madera_o(): return mat('madera_os_ms', 0x7a5232, 0.85)
def oro():      return mat('oro_ms', 0xe8b840, 0.25)
def agua():     return mat('agua_ms', 0x4a7a8a, 0.08)
def verde():    return mat('verde_ms', 0x2f5a32, 0.85)
def vapor_m():  return mat('vapor_ms', 0xf4f6f8, 0.9)
def piedra():   return mat_bloques('piedra_ms', 0xe6e0d0, 0xc6beac, ancho=1.4, alto=0.7)
def papel():    return mat_franjas('papel_pajita', 0xf6f2e6, 0xd8323a, 10, eje='Z', z0=0, alto=3.4)

# ================================================================ edificios
def capitolio_ms():
    """El Capitolio de Misisipi (1903): estilo Beaux-Arts, el pórtico de
    columnas, las dos alas con sus cúpulas pequeñas y la cúpula grande con el
    águila dorada encima."""
    Y = 20
    p = piedra()
    caja(p, 0, Y, 0, 80, 26, 15)
    caja(mat('cornisa_ms', 0xd8d0be, 0.6), 0, Y, 15, 81, 27, 1)
    escalinata(p, 0, Y - 13, 0, 22, 8, huella=0.5, tabica=0.3)
    columnata(p, -9, 9, 6, Y - 14, 2.4, 0.8, 12)
    fronton(p, 0, Y - 14.5, 14.4, 22, 4, 2)
    for s in (-1, 1):
        cil(p, s * 30, Y, 16, 4, 3, 16)
        cupula(mat('cupula_ms', 0xd6d2c8, 0.5), s * 30, Y, 19, 4, 3.5)
    cil(p, 0, Y, 16, 11, 9, 32)
    columnata(p, -9, 9, 8, Y - 11.5, 16, 0.45, 8)
    cupula(mat('cupula_ms', 0xd6d2c8, 0.5), 0, Y, 25, 11, 10)
    cil(p, 0, Y, 35, 2.5, 3, 16)
    # El águila dorada con las alas abiertas.
    esfera(oro(), 0, Y, 39.2, 0.8, 2, esc=(0.8, 0.9, 1.2))
    esfera(oro(), 0, Y - 0.5, 40.4, 0.45, 2)
    for s in (-1, 1):
        o = caja(oro(), s * 1.6, Y, 39.8, 2.6, 0.3, 0.9); o.rotation_euler = (0, s * -0.4, 0)
    texto(mat('letras_ms', 0x5a4a3a, 0.5), 'MISSISSIPPI', 0, Y - 14.6, 16.6, tam=1.2, prof=0.06)

def old_capitol_ms():
    """El viejo Capitolio de Misisipi (1839): griego, con el pórtico de
    columnas jónicas y la cúpula pequeña."""
    Y = 12
    p = mat_bloques('estuco_oc', 0xeee6d4, 0xd4ccb8, ancho=2, alto=1)
    caja(p, 0, Y, 0, 34, 18, 12)
    columnata(blanco(), -8, 8, 6, Y - 10.2, 0.6, 0.65, 10)
    fronton(blanco(), 0, Y - 10.8, 10.6, 18, 3.2, 2)
    caja(blanco(), 0, Y - 10, 0, 19, 3, 0.6)
    cil(p, 0, Y, 12, 4.5, 3.5, 24)
    cupula(mat('cupula_oc', 0xd8cfbc, 0.5), 0, Y, 15.5, 4.5, 3.5)
    texto(mat('letras_oc', 0x5a4a3a, 0.5), 'OLD CAPITOL', 0, Y - 12.4, 11.1, tam=0.7, prof=0.04)

def casa_blues():
    """Un bar de blues de Farish Street: casa de madera pintada, el porche,
    el letrero de neón BLUES y una guitarra enorme en el tejado."""
    Y = 7
    caja(mat('tablas_blues', 0x2f6a8a, 0.8), 0, Y, 0, 18, 12, 6)
    tejado(mat('tejado_blues', 0x6a3a2a, 0.8), 0, Y - 6, Y + 6, 6, 19, 3, vuelo=0.6, cumbrera='x')
    caja(madera_o(), 0, Y - 7.5, 0, 16, 3, 0.4)
    for x in (-7, -2.5, 2.5, 7):
        cil(madera_o(), x, Y - 8.6, 0.4, 0.12, 3, 6)
    caja(madera_o(), 0, Y - 7.5, 3.4, 16.4, 3.2, 0.25)
    caja(mat('puerta_blues', 0x8a2a1e, 0.6), 0, Y - 6.05, 0, 1.8, 0.1, 2.6)
    caja(negro(), 0, Y - 6.2, 4.2, 6.4, 0.2, 1.6)
    texto(luz('neon_blues', 0x3fa8ff, 1.5), 'BLUES', 0, Y - 6.35, 4.5, tam=1.0, prof=0.06)
    # La guitarra del tejado.
    G = mat('guitarra', 0xc86a2a, 0.4)
    esfera(G, 4, Y, 10, 1.2, 2, esc=(1, 0.25, 1.15))
    esfera(G, 4, Y, 11.5, 0.9, 2, esc=(1, 0.25, 1.1))
    caja(negro(), 4, Y - 0.3, 12.2, 0.35, 0.15, 3.6)
    cil(negro(), 4, Y - 0.32, 10.3, 0.35, 0.05, 12, eje='Y')

def magnolia():
    """La magnolia de la acera: hojas verde oscuro y flores blancas."""
    cil(madera_o(), 0, 0, 0, 0.22, 2.2, 6)
    for (x, y, z, r) in ((0, 0, 3.2, 1.6), (0.8, 0.3, 2.8, 1.1), (-0.7, -0.2, 2.9, 1.1), (0, 0.4, 4.1, 1.0)):
        esfera(verde(), x, y, z, r, 2)
    import random
    rr = random.Random(5)
    for k in range(14):
        a, b = rr.uniform(0, math.tau), rr.uniform(-0.6, 1.0)
        esfera(mat('flor_magnolia', 0xfaf6ee, 0.6), math.cos(a) * 1.5, math.sin(a) * 1.5, 3.2 + b, 0.18, 1)

def barco_vapor():
    """El barco de vapor del Misisipi (momento estrella), por dentro: se corre
    por la cubierta de madera; a los lados, los camarotes blancos de dos
    pisos con balcones, las chimeneas negras con corona y las ruedas de
    paletas rojas; alrededor, el río. Cruza la calle: el origen en el centro
    y la calle a lo largo de y."""
    L = 420
    caja(agua(), 0, 0, -0.6, 120, L + 40, 0.2)
    caja(madera(), 0, 0, -0.3, 30, L, 0.3)
    for k in range(int(L / 1.5)):                       # tablas
        caja(madera_o(), 0, -L / 2 + k * 1.5, -0.01, 8, 0.05, 0.02)
    for s in (-1, 1):
        # Camarotes de dos pisos con sus balcones y barandillas blancas.
        caja(blanco(), s * 11, 0, 0, 8, L - 20, 7)
        caja(blanco(), s * 11, 0, 7, 8.6, L - 20, 0.3)
        caja(blanco(), s * 11.5, 0, 7.3, 7, L - 40, 4)
        caja(mat('tejado_barco', 0x8a2a2a, 0.6), s * 11.5, 0, 11.3, 7.6, L - 36, 0.4)
        for k in range(int((L - 30) / 4)):
            y = -L / 2 + 15 + k * 4
            caja(mat('puerta_camarote', 0x3a5a7a, 0.5), s * 6.95, y, 0.3, 0.1, 1.4, 2.4)
            cil(blanco(), s * 6.6, y + 2, 0, 0.08, 3.5, 6)
        caja(blanco(), s * 6.6, 0, 3.4, 0.1, L - 20, 0.12)
        caja(blanco(), s * 6.6, 0, 1.0, 0.08, L - 20, 0.08)
        texto(rojo(), 'MISSISSIPPI QUEEN', s * 6.85, 0, 5.4, tam=1.6, prof=0.05).rotation_euler = (math.pi / 2, 0, -s * math.pi / 2)
        # Las chimeneas con su corona, delante y detrás.
        for y in (-L / 2 + 40, L / 2 - 120):
            cil(negro(), s * 12, y, 11.7, 1.1, 12, 16)
            for k in range(8):
                a = k * math.tau / 8
                cil(oro(), s * 12 + math.cos(a) * 1.15, y + math.sin(a) * 1.15, 23.7, 0.25, 1.2, 4, r2=0.02)
        # La rueda de paletas roja, en medio del costado.
        for k in range(12):
            a = k * math.tau / 12
            o = caja(rojo(), s * 16.5, math.cos(a) * 4, 3 + math.sin(a) * 4, 1.6, 0.4, 8.6)
            o.rotation_euler = (a, 0, 0)
        cil(madera_o(), s * 16.5, 0, 3, 0.6, 2, 12, eje='X')
    for (y, txt) in ((-L / 2 + 0.6, 'ALL ABOARD!'), (L / 2 - 0.6, 'BON VOYAGE')):
        for s in (-1, 1):
            cil(blanco(), s * 6, y, 0, 0.15, 6, 6)
        caja(blanco(), 0, y, 5, 13, 0.3, 1.4)
        texto(rojo(), txt, 0, y - 0.2, 5.3, tam=0.9, prof=0.05)

# ================================================================ obstáculos
def pajita_recta():
    """La pajita de papel gigante, de pie (de lejos cierra el carril)."""
    cil(papel(), 0, 0, 0, 0.32, 3.0, 16)
    o = cil(papel(), 0, 0.25, 3.15, 0.32, 0.9, 16); o.rotation_euler = (-0.6, 0, 0)
    for k in range(5):
        cil(mat('codo_pajita', 0xd8d2c4, 0.6), 0, 0, 2.9 + k * 0.06, 0.34, 0.03, 16)
    cil(mat('base_pajita', 0xb8b0a0, 0.7), 0, 0, 0, 0.5, 0.06, 16)

def pajita_doblada():
    """La pajita de papel deshecha: doblada y caída en el suelo (se salta)."""
    papel_m = mat('papel_mojado', 0xd8d0be, 0.9)
    rama(papel_m, (-1.4, 0, 0.3), (0.2, 0, 0.35), 0.32, 0.3, 12)
    rama(papel_m, (0.2, 0, 0.35), (0.9, -0.3, 0.6), 0.3, 0.28, 12)
    rama(papel_m, (0.9, -0.3, 0.6), (1.3, -0.5, 0.3), 0.28, 0.26, 12)
    for k in range(4):
        esfera(mat('mancha_pajita', 0xb8323a, 0.8), -1.1 + k * 0.6, -0.31, 0.38, 0.1, 1, esc=(1.2, 0.3, 1))
    esfera(mat('charco_ms', 0x9ab8c8, 0.1), 0, 0, 0.01, 1.2, 2, esc=(1.4, 1, 0.04))

def chorro_vapor():
    """El chorro de vapor que sale del tubo y cruza la cubierta a la altura de
    la cabeza (agacharse): el tubo en un lado y la nube a lo ancho."""
    cil(mat('tubo_vapor', 0x5a5e62, 0.4), 4.4, 0, 0, 0.25, 1.9, 10)
    o = cil(mat('tubo_vapor', 0x5a5e62, 0.4), 4.4, 0, 1.8, 0.25, 0.6, 10); o.rotation_euler = (0, -math.pi / 2, 0)
    for k in range(14):
        x = 3.6 - k * 0.55
        r = 0.32 + k * 0.025
        esfera(vapor_m(), x, (k % 3 - 1) * 0.12, 1.8 + (k % 2) * 0.12, r, 2)

def bala_algodon():
    """La bala de algodón de Misisipi, con sus cinchas (se salta)."""
    caja(mat('algodon', 0xf4f2ec, 0.95), 0, 0, 0, 1.6, 1.0, 0.9)
    for x in (-0.5, 0, 0.5):
        caja(mat('cincha', 0x8a6a42, 0.7), x, 0, -0.01, 0.06, 1.04, 0.94)
    for k in range(6):
        esfera(blanco(), -0.6 + k * 0.24, -0.5, 0.45 + (k % 2) * 0.2, 0.14, 1)

def cartel_pajitas():
    """La pancarta de las pajitas (agacharse): «BRING BACK PLASTIC STRAWS!»."""
    for x in (-1.25, 1.25):
        cil(madera_o(), x, 0, 0, 0.07, 2.75, 8)
    caja(mat('tela_pajitas', 0xf6f2e6, 0.7), 0, 0, 1.55, 2.4, 0.06, 1.05)
    texto(rojo(), 'BRING BACK', 0, -0.04, 2.25, tam=0.24, prof=0.02)
    texto(azul(), 'PLASTIC STRAWS!', 0, -0.04, 1.88, tam=0.2, prof=0.02)

PIEZAS = {
    'capitolio_ms':   (capitolio_ms,   'jackson', dict(lado=2048, segmentos=1, min_bisel=1.0)),
    'old_capitol_ms': (old_capitol_ms, 'jackson', dict(lado=1024, segmentos=1, min_bisel=1.0)),
    'casa_blues':     (casa_blues,     'jackson', dict(lado=1024, bisel=0.0)),
    'magnolia':       (magnolia,       'jackson', dict(lado=256, bisel=0.0)),
    'barco_vapor':    (barco_vapor,    'jackson', dict(lado=2048, bisel=0.0, suelo=False)),
    'pajita_recta':   (pajita_recta,   'obstaculos', dict(lado=256, bisel=0.0)),
    'pajita_doblada': (pajita_doblada, 'obstaculos', dict(lado=256, bisel=0.0)),
    'chorro_vapor':   (chorro_vapor,   'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
    'bala_algodon':   (bala_algodon,   'obstaculos', dict(lado=256, bisel=0.0)),
    'cartel_pajitas': (cartel_pajitas, 'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
}

correr(PIEZAS)
