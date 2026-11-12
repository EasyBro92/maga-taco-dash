# Nivel 17: Oklahoma City, Oklahoma (12/11/2026).
#
#   blender -b -P blender/oklahoma.py -- [pieza ...] [--rapido]
#
# Historia: «Molinos de viento girando en la pista (él dice que dan cáncer)».
#   Por Bricktown (almacenes de ladrillo y el canal con su barca) y el centro
#   (la Devon Tower de cristal, el Crystal Bridge de los jardines), bajo el
#   puente Skydance (el pájaro de acero blanco) hasta el Capitolio, que tiene
#   un pozo de petróleo en el jardín.
# Obstáculos (carpeta obstaculos): el molino de viento en medio de la calle
# (la torre y, aparte, las aspas que giran y barren los carriles), el géiser
# de petróleo (el pozo y, aparte, el chorro) y la pancarta contra los molinos.

import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import *
from comun import _poner

def blanco():   return mat('blanco_ok', 0xf6f6f2, 0.45)
def negro():    return mat('negro_ok', 0x1b1c20, 0.4)
def petroleo(): return mat('petroleo_ok', 0x121014, 0.12)
def rojo():     return mat('rojo_ok', 0xc8282c, 0.45)
def acero():    return mat('acero_ok', 0xc4cad0, 0.25)
def oxido():    return mat('oxido_ok', 0x8a4a2a, 0.7)
def agua():     return mat('agua_ok', 0x3f7f9a, 0.05)
def verde():    return mat('verde_ok', 0x3f7a3a, 0.8)
def ladrillo(): return mat_ventanas('ladrillo_ok', 0x2c3440, 0x9a4a32, paso_x=2.0, paso_z=3.4, hueco_x=1.0, hueco_z=2.0, variacion=1.07)

# ================================================================ edificios
def devon_tower():
    """La Devon Energy Center (2012), la más alta de Oklahoma: cristal azulado,
    planta redondeada, la corona en bisel y la rotonda de cristal delante."""
    v = mat_ventanas('cristal_devon', 0x5f8fb0, 0x9fbcd0, paso_x=1.4, paso_z=3.4, hueco_x=1.25, hueco_z=3.0, variacion=1.02)
    Y = 20
    o = cil(v, 0, Y, 0, 15, 140, 28); o.scale = (1.0, 0.75, 1.0)
    o = cil(v, 0, Y, 140, 15, 10, 28, r2=6); o.scale = (1.0, 0.75, 1.0)
    caja(mat('aleta_devon', 0xd8e0e6, 0.3), 0, Y - 11.4, 0, 1.2, 0.6, 148)
    # La rotonda de cristal.
    cil(mat_ventanas('cristal_rotonda', 0x7faac4, 0xc8d6e0, paso_x=1.2, paso_z=2.0, hueco_x=1.05, hueco_z=1.8, variacion=1.02), 0, 6, 0, 9, 16, 24)
    cupula(mat('cupula_rotonda', 0xb8ccd8, 0.2), 0, 6, 16, 9, 3)
    texto(mat('letras_devon', 0x1f3a6a, 0.5), 'DEVON', 0, -3.1, 12, tam=1.4, prof=0.06)

def cristal_bridge():
    """El Crystal Bridge de los jardines Myriad: el invernadero de cristal en
    forma de tubo tumbado, sobre el estanque, con la selva dentro."""
    Y = 12
    caja(agua(), 0, Y - 2, -0.05, 46, 10, 0.12)
    caja(mat('cesped_ok', 0x6a9a4a, 0.9), 0, Y + 6, -0.05, 46, 12, 0.1)
    vid = mat_ventanas('vidrio_cb', 0x9fd0d8, 0xe8f2f4, paso_x=1.6, paso_z=1.6, hueco_x=1.45, hueco_z=1.45, variacion=1.01)
    cil(vid, 0, Y, 6, 7, 40, 24, eje='X')
    for k in range(9):
        cil(acero(), -18 + k * 4.5, Y, 6, 7.05, 0.3, 24, eje='X')
    for k in range(6):
        caja(acero(), -15 + k * 6, Y, 0, 0.6, 0.6, 2)
    for k in range(10):
        esfera(verde(), -16 + k * 3.6, Y + (k % 3 - 1) * 2, 4.5 + (k % 2), 2.2, 2)
    texto(mat('letras_cb', 0x2f5a3a, 0.5), 'MYRIAD GARDENS', 0, 2.4, 0.4, tam=1.0, prof=0.2).rotation_euler = (math.pi / 2, 0, 0)

def bricktown():
    """Bricktown: los almacenes de ladrillo rojo del ferrocarril, el canal
    delante con su barca-taxi y el letrero BRICKTOWN."""
    Y = 12
    caja(ladrillo(), -9, Y, 0, 20, 14, 14)
    caja(ladrillo(), 11, Y, 0, 18, 14, 10)
    for (x, w, h) in ((-9, 20, 14), (11, 18, 10)):
        caja(mat('cornisa_bt', 0x6a2a1e, 0.6), x, Y, h, w + 0.4, 14.4, 0.6)
    texto(mat('letras_bt', 0xf2e6c8, 0.5), 'BRICKTOWN', -9, Y - 7.1, 10.5, tam=1.6, prof=0.08)
    texto(mat('letras_bt2', 0xf2e6c8, 0.5), 'WAREHOUSE', 11, Y - 7.1, 7, tam=1.0, prof=0.06)
    # El canal y la barca.
    caja(agua(), 0, 2.5, -0.4, 40, 4, 0.3)
    for s in (-1, 1):
        caja(mat('borde_canal', 0xb08a6a, 0.8), 0, 2.5 + s * 2.1, -0.4, 40, 0.3, 0.45)
    caja(mat('barca_ok', 0xf2c230, 0.4), 6, 2.5, -0.2, 6, 2, 0.6)
    caja(mat('toldo_barca', 0x2f6fa8, 0.5), 6, 2.5, 1.2, 5, 2.1, 0.12)
    for (dx, dy) in ((-2.3, -0.9), (2.3, -0.9), (-2.3, 0.9), (2.3, 0.9)):
        cil(acero(), 6 + dx, 2.5 + dy, 0.4, 0.04, 0.8, 4)

def skydance():
    """El puente Skydance (2012): el pájaro de acero blanco (la tijereta,
    pájaro del estado) que cruza por encima. Cruza la calle: el origen en el
    centro y la calle a lo largo de y."""
    b = blanco()
    pts = []
    for k in range(17):                                  # el arco grande (el ala)
        t = k / 16
        x = -18 + 36 * t
        z = 2 + 18 * math.sin(math.pi * t) ** 0.8
        pts.append((x, 2 * math.sin(math.pi * t), z))
    for a, c in zip(pts, pts[1:]):
        rama(b, a, c, 0.45, 0.45, 8)
    pts2 = []
    for k in range(13):                                  # el segundo arco, inclinado (la cola)
        t = k / 12
        x = -14 + 30 * t
        z = 1 + 12 * math.sin(math.pi * t)
        pts2.append((x, -3 + 3 * t, z))
    for a, c in zip(pts2, pts2[1:]):
        rama(b, a, c, 0.35, 0.35, 8)
    for k in range(8):                                   # cables
        a = pts[2 + k * 2]
        rama(acero(), a, (a[0], 0, 7.2), 0.05, 0.05, 4)
    caja(mat('pasarela_sd', 0xd8dce0, 0.5), 0, 0, 7, 40, 4, 0.5)
    for s in (-1, 1):
        caja(acero(), 0, s * 2, 7.5, 40, 0.08, 1.1)
    for s in (-1, 1):
        caja(mat('pilar_sd', 0xd8dce0, 0.6), s * 17, 0, 0, 2, 4, 7)
    texto(mat('letras_sd', 0x1f3a6a, 0.5), 'SKYDANCE', 0, -2.05, 7.6, tam=0.8, prof=0.04)

def capitolio_ok():
    """El Capitolio de Oklahoma: piedra clara, columnas, la cúpula con «el
    Guardián» encima y, en el jardín, la torre de un pozo de petróleo."""
    piedra = mat_bloques('piedra_cap_ok', 0xe8e0cc, 0xc8bea8, ancho=1.4, alto=0.7)
    Y = 20
    caja(piedra, 0, Y, 0, 70, 30, 18)
    caja(mat('cornisa_cap_ok', 0xd8ccb2, 0.6), 0, Y, 18, 71, 31, 1)
    escalinata(piedra, 0, Y - 15, 0, 22, 8, huella=0.5, tabica=0.3)
    columnata(piedra, -10, 10, 8, Y - 16, 2.4, 0.8, 13)
    fronton(piedra, 0, Y - 16.5, 15.4, 24, 4, 2)
    cil(piedra, 0, Y, 19, 11, 10, 32)
    cupula(mat('cupula_cap_ok', 0xd8d2c4, 0.5), 0, Y, 29, 11, 9)
    cil(piedra, 0, Y, 38, 2.4, 3, 16)
    cupula(piedra, 0, Y, 41, 2.4, 2)
    cil(mat('guardian', 0x6a5a3a, 0.4), 0, Y, 43, 0.6, 4, 8)
    # El pozo de petróleo del jardín (Petunia nº 1).
    X0, Y0 = -26, 4
    for (dx, dy) in ((-2, -2), (2, -2), (-2, 2), (2, 2)):
        rama(oxido(), (X0 + dx, Y0 + dy, 0), (X0 + dx * 0.25, Y0 + dy * 0.25, 18), 0.2, 0.12, 6)
    for k in range(6):
        z = 2 + k * 3
        f = 1 - z / 20 * 0.75
        for (a, b) in (((-2, -2), (2, -2)), ((2, -2), (2, 2)), ((2, 2), (-2, 2)), ((-2, 2), (-2, -2))):
            rama(oxido(), (X0 + a[0] * f, Y0 + a[1] * f, z), (X0 + b[0] * f, Y0 + b[1] * f, z), 0.08, 0.08, 4)

# ================================================================ obstáculos
def molino_torre():
    """La torre del molino de viento, en medio de la calle (ocupa el carril
    del centro): blanca, la góndola arriba mirando hacia ti."""
    cil(blanco(), 0, 0, 0, 0.75, 8.2, 16, r2=0.42)
    caja(blanco(), 0, 0.3, 8.0, 1.0, 2.6, 1.0)
    cil(mat('base_molino', 0x8a8e92, 0.6), 0, 0, 0, 1.0, 0.4, 16)
    texto(mat('letras_molino', 0x2f6fa8, 0.5), 'WIND', 0, -0.72, 3.5, tam=0.45, prof=0.03)

def molino_rotor():
    """Las aspas del molino (el juego las hace girar y barren los carriles de
    los lados): tres palas largas y el buje, en el plano que mira a -y."""
    esfera(blanco(), 0, -0.2, 0, 0.55, 2, esc=(1, 1.3, 1))
    for k in range(3):
        a = k * math.tau / 3 + math.pi / 2
        x, z = math.cos(a), math.sin(a)
        o = caja(blanco(), x * 3.3, -0.3, z * 3.3 - 0.0, 0.7, 0.18, 6.4)
        o.rotation_euler = (0, -(a - math.pi / 2), 0)
        o.location = (x * 3.4, -0.3, z * 3.4)
        caja(rojo(), x * 6.4, -0.32, z * 6.4, 0.6, 0.2, 0.5).rotation_euler = (0, -(a - math.pi / 2), 0)

def geiser():
    """El pozo del que brota el petróleo: la boca con su llave y el charco
    negro y brillante alrededor (se pisa; el charco resbala)."""
    cil(petroleo(), 0, 0, 0.0, 1.25, 0.03, 24)
    cil(oxido(), 0, 0, 0, 0.28, 0.5, 12)
    cil(oxido(), 0, 0, 0.5, 0.36, 0.1, 12)
    cil(rojo(), 0.42, 0, 0.42, 0.2, 0.05, 12, eje='X')
    for k in range(5):
        a = k * math.tau / 5
        esfera(petroleo(), math.cos(a) * 0.7, math.sin(a) * 0.7, 0.02, 0.18, 1, esc=(1, 1, 0.3))

def chorro_petroleo():
    """El chorro de petróleo que sale del pozo (bloquea el carril mientras sale)."""
    for k in range(6):
        cil(petroleo(), 0, 0, k * 0.9, 0.42 - k * 0.03, 0.95, 12)
    for k in range(9):
        a = k * math.tau / 9
        esfera(petroleo(), math.cos(a) * 0.7, math.sin(a) * 0.7, 5.2 + (k % 3) * 0.3, 0.32, 2)
    esfera(petroleo(), 0, 0, 5.8, 0.7, 2, esc=(1, 1, 0.7))

def cartel_molinos():
    """La pancarta contra los molinos (agacharse): «STOP THE WINDMILLS!»."""
    for x in (-1.25, 1.25):
        cil(mat('palo_cm', 0x9a6a3a, 0.5), x, 0, 0, 0.07, 2.75, 8)
    caja(mat('tela_cm', 0xf6f2e6, 0.7), 0, 0, 1.55, 2.4, 0.06, 1.05)
    texto(rojo(), 'STOP THE', 0, -0.04, 2.22, tam=0.28, prof=0.02)
    texto(rojo(), 'WINDMILLS!', 0, -0.04, 1.84, tam=0.28, prof=0.02)

PIEZAS = {
    'devon_tower':     (devon_tower,     'oklahoma', dict(lado=1024, bisel=0.0)),
    'cristal_bridge':  (cristal_bridge,  'oklahoma', dict(lado=1024, bisel=0.0)),
    'bricktown':       (bricktown,       'oklahoma', dict(lado=1024, bisel=0.0)),
    'skydance':        (skydance,        'oklahoma', dict(lado=1024, bisel=0.0, suelo=False)),
    'capitolio_ok':    (capitolio_ok,    'oklahoma', dict(lado=2048, segmentos=1, min_bisel=1.0)),
    'molino_torre':    (molino_torre,    'obstaculos', dict(lado=256, bisel=0.0)),
    'molino_rotor':    (molino_rotor,    'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
    'geiser':          (geiser,          'obstaculos', dict(lado=256, bisel=0.0)),
    'chorro_petroleo': (chorro_petroleo, 'obstaculos', dict(lado=256, bisel=0.0)),
    'cartel_molinos':  (cartel_molinos,  'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
}

correr(PIEZAS)
