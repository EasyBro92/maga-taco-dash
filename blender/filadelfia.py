# Nivel 43: Filadelfia, Pensilvania (15/11/2026).
#
#   blender -b -P blender/filadelfia.py -- [pieza ...] [--rapido]
#
# Historia: «La Campana de la Libertad. Se pone en la freidora de un
#   McDonald's, como hizo de verdad». Acto del Sentido Común. Por Market
#   Street: el ayuntamiento con su torre y William Penn encima, el museo de
#   arte con sus escaleras, la freiduría con la caja de patatas gigante y los
#   carritos de pretzels en las aceras. La freidora: las cestas de patatas se
#   van dorando mientras se acercan (hay que coger las doradas, no las crudas
#   ni las quemadas); el momento estrella, la Casa de la Moneda, con las
#   prensas que golpean en cadena de un carril a otro. Final en el Salón de la
#   Independencia, con la Campana de la Libertad (y su grieta). Pancarta del
#   Sentido Común: LA CAMPANA YA ESTÁ ROTA.
# Obstáculos (carpeta obstaculos): el marco y el martillo de la prensa de
# monedas, el pretzel gigante, el autobús y la pancarta.

import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import *

def blanco():    return mat('blanco_phl', 0xf6f4ee, 0.5)
def negro():     return mat('negro_phl', 0x1c1c20, 0.4)
def cristal():   return mat('cristal_phl', 0x3a5a70, 0.15)
def rojo():      return mat('rojo_phl', 0xc8202a, 0.45)
def azul():      return mat('azul_phl', 0x1e4a9a, 0.45)
def amarillo():  return mat('amarillo_phl', 0xf2c21a, 0.45)
def rosa():      return mat('rosa_phl', 0xf08aa8, 0.5)
def gris():      return mat('gris_phl', 0x8a9098, 0.4)
def acero():     return mat('acero_phl', 0x9aa0a8, 0.3)
def hierro():    return mat('hierro_phl', 0x2a2c30, 0.45)
def madera_o():  return mat('madera_oscura_phl', 0x5a3a22, 0.85)
def ladrillo():  return mat_bloques('ladrillo_phl', 0xa85a3e, 0x7a4030, ancho=0.4, alto=0.16)
def piedra():    return mat_bloques('piedra_phl', 0xd8d0c0, 0xb8b0a0, ancho=1.2, alto=0.6, grosor=0.008)
def piedra_l():  return mat('piedra_lisa_phl', 0xe6dfd0, 0.6)
def bronce():    return mat('bronce_phl', 0x5a4a2e, 0.35)
def pretzel_m(): return mat('pretzel_phl', 0xa86a2a, 0.6)
def cobre():     return mat('cobre_phl', 0xc8783a, 0.3)

def cartel_sentido(x, y, z, w, h, linea1, linea2=''):
    caja(azul(), x, y, z, w, 0.06, h)
    caja(blanco(), x, y - 0.01, z + h - h * 0.08, w, 0.06, h * 0.08)
    esfera(rosa(), x - w / 2 + h * 0.32, y - 0.06, z + h * 0.5, h * 0.24, 1, esc=(1.2, 0.4, 1))
    texto(blanco(), linea1, x + h * 0.25, y - 0.045, z + h * (0.5 if not linea2 else 0.56), tam=h * 0.3, prof=0.02)
    if linea2:
        texto(amarillo(), linea2, x + h * 0.25, y - 0.045, z + h * 0.2, tam=h * 0.2, prof=0.02)

def campana(x, y, z, k=1.0):
    """La Campana de la Libertad, con su grieta, colgada de su yugo."""
    b = bronce()
    cil(b, x, y, z, 0.9 * k, 1.2 * k, 20, r2=0.6 * k)
    cil(b, x, y, z + 1.2 * k, 0.6 * k, 0.4 * k, 16, r2=0.3 * k)
    cil(b, x, y, z - 0.1 * k, 0.95 * k, 0.15 * k, 20)
    caja(negro(), x, y - 0.86 * k, z + 0.1 * k, 0.04 * k, 0.04 * k, 0.9 * k)
    caja(negro(), x + 0.05 * k, y - 0.85 * k, z + 0.6 * k, 0.04 * k, 0.04 * k, 0.4 * k)
    caja(madera_o(), x, y, z + 1.6 * k, 2.2 * k, 0.4 * k, 0.35 * k)

def pretzel_forma(m, x, y, z, k=1.0):
    """Un pretzel tumbado (la forma de lazo), en el plano x-y."""
    for i in range(16):
        a0, a1 = i * math.tau / 16, (i + 1) * math.tau / 16
        for (cx, cy) in ((-0.35 * k, 0.05 * k), (0.35 * k, 0.05 * k)):
            rama(m, (x + cx + math.cos(a0) * 0.35 * k, y + cy + math.sin(a0) * 0.3 * k, z), (x + cx + math.cos(a1) * 0.35 * k, y + cy + math.sin(a1) * 0.3 * k, z), 0.1 * k, 0.1 * k, 6)
    rama(m, (x - 0.5 * k, y - 0.4 * k, z), (x + 0.3 * k, y + 0.2 * k, z), 0.1 * k, 0.1 * k, 6)
    rama(m, (x + 0.5 * k, y - 0.4 * k, z), (x - 0.3 * k, y + 0.2 * k, z), 0.1 * k, 0.1 * k, 6)

# ================================================================ la meta
def salon_independencia():
    """El Salón de la Independencia (la meta): el edificio georgiano de
    ladrillo, las ventanas blancas, la torre de madera blanca con el reloj y
    el campanario; delante, la Campana de la Libertad en su pabellón y la
    pancarta del Sentido Común."""
    Y = 20
    W, D, H = 40.0, 16.0, 11.0
    yf = Y - D / 2
    l = ladrillo()
    caja(l, 0, Y, 0, W, D, H)
    caja(blanco(), 0, Y, H, W + 0.4, D + 0.4, 0.6)
    tejado(mat('tejado_phl', 0x4a4a52, 0.6), 0, Y - D / 2, Y + D / 2, H + 0.6, W, 3.0, cumbrera='x')
    for k in range(9):
        x = -17 + k * 4.25
        for z in (1.5, 6.5):
            ventana(x, z, 1.6, 2.8, y=yf - 0.05, marco=blanco(), cristal=cristal())
    puerta(0, 0, 2.0, 3.0, y=yf - 0.05, color=0x3a2a1e, marco=blanco())
    T = 7.0
    caja(l, 0, Y + 4, 0, T, T, 18)
    b = blanco()
    caja(b, 0, Y + 4, 18, T - 1, T - 1, 4)
    cil(b, 0, Y + 4, 22, 2.6, 4, 8)
    for k in range(8):
        a = k * math.tau / 8
        cil(b, math.cos(a) * 2.3, Y + 4 + math.sin(a) * 2.3, 22, 0.15, 4, 6)
    cupula(b, 0, Y + 4, 26, 2.7, 2.4, 16, 6)
    cil(b, 0, Y + 4, 28.4, 0.9, 2.2, 8, r2=0.3)
    cil(amarillo(), 0, Y + 4, 30.6, 0.08, 2.4, 6)
    cil(b, 0, Y + 4 - T / 2 + 0.4, 20, 1.5, 0.1, 20, eje='Y')
    caja(negro(), 0, Y + 4 - T / 2 + 0.3, 20, 0.1, 0.04, 1.1)
    # El pabellón de la campana delante.
    caja(mat('suelo_pabellon_phl', 0xc8c0b0, 0.8), 0, yf - 14, -0.04, 70, 22, 0.06)
    for (x, y) in ((-8, yf - 11), (-8, yf - 7), (-12, yf - 11), (-12, yf - 7)):
        cil(gris(), x, y, 0, 0.15, 4.2, 8)
    caja(cristal(), -10, yf - 9, 4.2, 5.4, 5.4, 0.2)
    campana(-10, yf - 9, 1.0, 1.0)
    for x in (8, 22):
        cil(madera_o(), x, yf - 16, 0, 0.12, 4.4, 8)
    cartel_sentido(15, yf - 16, 2.8, 14, 1.6, 'LA CAMPANA YA ESTÁ ROTA', 'EL SENTIDO COMÚN')

# ================================================================ edificios
def ayuntamiento_philly():
    """El ayuntamiento de Filadelfia (1901): el edificio enorme de piedra
    clara con mansardas, la torre altísima con el reloj y la estatua de
    William Penn en lo alto."""
    Y = 14
    p = piedra()
    caja(p, 0, Y, 0, 40, 24, 20)
    caja(mat('mansarda_phl', 0x4a5050, 0.6), 0, Y, 20, 38, 22, 4)
    for k in range(10):
        x = -18 + k * 4
        for z in (2, 7, 12, 16):
            ventana(x, z, 1.6, 2.6, y=Y - 12 - 0.05, marco=piedra_l(), cristal=cristal())
    T = 10.0
    caja(p, 0, Y, 20, T, T, 30)
    caja(piedra_l(), 0, Y, 50, T + 1, T + 1, 1.0)
    caja(blanco(), 0, Y, 51, 8, 8, 6)
    for (dx, dy, rz) in ((0, -1, 0), (-1, 0, 1), (1, 0, 1)):
        x, y = dx * 4.05, Y + dy * 4.05
        o = cil(blanco(), x, y, 54, 2.4, 0.15, 24, eje='Y')
        if rz:
            o.rotation_euler = (math.pi / 2, 0, math.pi / 2)
        if dy == -1:
            caja(negro(), x, y - 0.12, 54, 0.12, 0.04, 1.6)
    cupula(mat('cupula_phl', 0x7a8a8a, 0.5), 0, Y, 57, 4, 6, 16, 6)
    cil(bronce(), 0, Y, 63, 0.5, 4, 8)
    esfera(bronce(), 0, Y, 67.3, 0.45, 1)
    rama(bronce(), (0.3, Y, 66), (1.0, Y - 0.6, 66.5), 0.12, 0.08, 4)

def museo_arte():
    """El museo de arte de Filadelfia: el templo con columnas y frontones de
    tejado azul y las escaleras famosas por delante (72 escalones)."""
    Y = 22
    p = piedra()
    caja(p, 0, Y, 6, 40, 14, 14)
    caja(mat('tejado_museo_phl', 0x3a6a9a, 0.4), 0, Y, 20, 40.6, 14.6, 1.2)
    fronton(mat('frontis_phl', 0xd8c890, 0.5), 0, Y - 7.3, 21.2, 16, 4, 3)
    columnata(piedra_l(), -7, 7, 6, Y - 7.4, 6, 0.7, 14)
    for s in (-1, 1):
        caja(p, s * 26, Y + 6, 0, 12, 24, 18)
    for k in range(18):
        caja(piedra_l(), 0, Y - 8 - k * 0.8, 0, 26, 0.8, 6 - k * 0.33)
    texto(negro(), 'MUSEO DE ARTE', 0, Y - 7.2, 18.6, tam=0.9, prof=0.03)

def freiduria():
    """La freiduría de la esquina: el local amarillo y rojo, el mostrador y
    la caja de patatas fritas gigante en el tejado."""
    Y = 7
    yf = Y - 5
    caja(mat('freiduria_phl', 0xf2c21a, 0.6), 0, Y, 0, 14, 10, 6)
    caja(rojo(), 0, Y, 6, 14.4, 10.4, 0.5)
    caja(cristal(), 0, yf - 0.05, 0.6, 10, 0.1, 2.8)
    caja(rojo(), 0, yf - 0.1, 4.2, 10, 0.12, 1.2)
    texto(amarillo(), 'FRIES', 0, yf - 0.18, 4.4, tam=0.9, prof=0.03)
    caja(rojo(), 0, Y, 6.5, 3.2, 2.2, 3.0)
    caja(amarillo(), 0, Y - 1.12, 7.4, 1.4, 0.04, 0.8)
    for k in range(9):
        caja(mat('patata_frita_phl', 0xf2c84a, 0.6), -1.3 + k * 0.33, Y + (k % 3) * 0.3 - 0.3, 9.5, 0.22, 0.22, 1.6 + (k % 3) * 0.4)

def carrito_pretzel():
    """El carrito de los pretzels de Filadelfia (para la acera)."""
    caja(acero(), 0, 0, 0.4, 1.6, 0.9, 0.9)
    for s in (-1, 1):
        cil(negro(), s * 0.6, 0, 0.0, 0.22, 0.12, 12, eje='X')
    caja(cristal(), 0, 0, 1.3, 1.4, 0.8, 0.6)
    for k in range(3):
        pretzel_forma(pretzel_m(), -0.4 + k * 0.4, 0, 1.4, 0.4)
    cil(hierro(), 0, 0, 1.9, 0.03, 0.8, 4)
    cil(mat_franjas('sombrilla_pret_phl', 0x1e4a9a, 0xf2c21a, 6, eje='Z', z0=2.6, alto=0.5), 0, 0, 2.6, 1.0, 0.5, 12, r2=0.05)

# ================================================================ cruza la calle
def arco_philly():
    """El arco de Filadelfia: CIUDAD DEL AMOR FRATERNAL, con dos campanas
    colgando; por detrás, 1776."""
    for s in (-1, 1):
        caja(ladrillo(), s * 8.6, 0, 0, 0.8, 0.8, 7.8)
        caja(blanco(), s * 8.6, 0, 7.8, 1.0, 1.0, 0.3)
    caja(blanco(), 0, 0, 7.0, 18.0, 0.4, 0.5)
    caja(azul(), 0, 0, 4.4, 13, 0.18, 1.8)
    texto(amarillo(), 'PHILADELPHIA', 0, -0.12, 5.3, tam=0.75, prof=0.04)
    texto(blanco(), 'CIUDAD DEL AMOR FRATERNAL', 0, -0.12, 4.65, tam=0.38, prof=0.04)
    o = texto(amarillo(), '1776', 0, 0.12, 5.0, tam=1.0, prof=0.04)
    o.rotation_euler = (math.pi / 2, 0, math.pi)
    for x in (-5.5, 5.5):
        cil(hierro(), x, 0, 6.5, 0.03, 0.5, 4)
        campana(x, 0, 5.4, 0.5)

# ================================================================ la Casa de la Moneda
def casa_moneda_int():
    """La Casa de la Moneda por dentro (momento estrella): la nave con las
    vigas, las cintas transportadoras a los lados, los montones de monedas,
    las cajas de sacos y los arcos de SALIDA y META. (Las prensas de los
    carriles son obstáculos.) Cruza la calle: el origen en el centro."""
    L = 420
    caja(mat_bloques('suelo_moneda_phl', 0x7a7e86, 0x5a5e66, ancho=2.0, alto=2.0, grosor=0.02), 0, 0, -0.2, 26, L, 0.2)
    for s in (-1, 1):
        caja(mat('pared_moneda_phl', 0xc8ccd0, 0.7), s * 14, 0, 0, 0.6, L, 12)
        caja(hierro(), s * 9.5, 0, 0.8, 2.6, L, 0.3)
        for k in range(int(L / 6)):
            y = -L / 2 + 3 + k * 6
            cil(hierro(), s * 9.5, y, 0.3, 0.3, 2.4, 10, eje='X')
            for i in range(5):
                cil(cobre(), s * 9.5 + (i - 2) * 0.4, y + (k % 2) * 0.8, 1.15, 0.15, 0.05, 12)
        for k in range(int(L / 20)):
            y = -L / 2 + 10 + k * 20
            esfera(cobre(), s * 12, y, 0, 1.4, 1, esc=(1, 1, 0.45))
            caja(mat('saco_moneda_phl', 0xc8b088, 0.85), s * 12, y + 4, 0, 1.2, 1.2, 1.2)
            texto(negro(), '$', s * 12 - s * 0.62, y + 4, 0.55, tam=0.6, prof=0.02).rotation_euler = (math.pi / 2, 0, -s * math.pi / 2)
    for k in range(int(L / 12)):
        caja(hierro(), 0, -L / 2 + 6 + k * 12, 11, 28, 0.5, 0.6)
    for (y, txt) in ((-L / 2 + 1, 'SALIDA'), (L / 2 - 1, 'META')):
        for s in (-1, 1):
            caja(hierro(), s * 7.0, y, 0, 0.5, 0.5, 6.2)
        caja(hierro(), 0, y, 5.6, 14.6, 0.5, 0.6)
        caja(amarillo(), 0, y, 4.0, 10, 0.16, 1.4)
        texto(negro(), 'U.S. MINT · ' + txt, 0, y - 0.1, 4.45, tam=0.55, prof=0.04)

# ================================================================ obstáculos
def prensa_marco():
    """El marco de la prensa de monedas: las dos columnas de acero y el
    travesaño de arriba, con la placa de abajo y las monedas brillando
    (el martillo es otra pieza: sube y baja)."""
    for s in (-1, 1):
        caja(acero(), s * 1.05, 0, 0, 0.25, 0.8, 3.6)
    caja(acero(), 0, 0, 3.6, 2.35, 0.8, 0.4)
    caja(mat_franjas('franjas_prensa_phl', 0xf2c21a, 0x1c1c20, 8, eje='X', z0=-1.1, alto=2.2), 0, 0, 0, 2.1, 0.9, 0.12)
    for i in range(3):
        cil(cobre(), -0.5 + i * 0.5, 0, 0.12, 0.18, 0.03, 12)

def prensa_martillo():
    """El martillo de la prensa (baja y golpea): el bloque de acero con su
    cara de moneda (el origen arriba: cuelga)."""
    caja(mat('martillo_phl', 0x6a7078, 0.3), 0, 0, -1.6, 1.9, 0.7, 1.6)
    cil(amarillo(), 0, -0.36, -0.8, 0.45, 0.04, 16, eje='Y')
    texto(negro(), '1¢', 0, -0.39, -0.95, tam=0.3, prof=0.01)

def pretzel_gigante():
    """El pretzel gigante caído en la calle (se salta)."""
    pretzel_forma(pretzel_m(), 0, 0, 0.18, 1.6)
    for k in range(8):
        esfera(blanco(), -0.6 + k * 0.17, -0.1 + (k % 3) * 0.12, 0.34, 0.03, 1)

def autobus_septa():
    """El autobús de Filadelfia (no se pasa): plateado con las franjas azul,
    roja y blanca. El morro en el origen."""
    pl = acero()
    caja(pl, 0, 5.2, 0.4, 2.6, 10.4, 2.8)
    caja(cristal(), 0, 0.0, 1.4, 2.3, 0.1, 1.4)
    for y in range(1, 10, 2):
        for s in (-1, 1):
            caja(cristal(), s * 1.31, y + 0.5, 1.6, 0.05, 1.6, 1.0)
    for s in (-1, 1):
        caja(azul(), s * 1.31, 5.2, 0.9, 0.06, 10.4, 0.3)
        caja(rojo(), s * 1.31, 5.2, 1.2, 0.06, 10.4, 0.12)
    caja(negro(), 0, -0.03, 2.75, 1.6, 0.05, 0.3)
    texto(amarillo(), 'MARKET ST', 0, -0.05, 2.8, tam=0.18, prof=0.01)
    for (y, s) in ((1.6, 1), (8.4, 1), (1.6, -1), (8.4, -1)):
        cil(negro(), s * 1.2, y, 0.45, 0.45, 0.3, 14, eje='X')
    for s in (-1, 1):
        caja(luz('faro_bus_phl', 0xfff2c0, 1.0), s * 0.95, -0.03, 0.75, 0.35, 0.05, 0.2)

def cartel_pa():
    """La pancarta del Sentido Común (agacharse): LA CAMPANA YA ESTÁ ROTA."""
    for x in (-1.25, 1.25):
        cil(madera_o(), x, 0, 0, 0.07, 2.75, 8)
    caja(azul(), 0, 0, 1.5, 2.4, 0.05, 1.2)
    esfera(rosa(), -0.9, -0.05, 2.1, 0.2, 1, esc=(1.2, 0.4, 1))
    texto(blanco(), 'LA CAMPANA', 0.15, -0.035, 2.2, tam=0.2, prof=0.02)
    texto(amarillo(), 'YA ESTÁ ROTA', 0.15, -0.035, 1.8, tam=0.2, prof=0.02)

PIEZAS = {
    'salon_independencia': (salon_independencia, 'filadelfia', dict(lado=2048, bisel=0.0)),
    'ayuntamiento_philly': (ayuntamiento_philly, 'filadelfia', dict(lado=1024, bisel=0.0)),
    'museo_arte':          (museo_arte,          'filadelfia', dict(lado=1024, bisel=0.0)),
    'freiduria':           (freiduria,           'filadelfia', dict(lado=1024, bisel=0.0)),
    'carrito_pretzel':     (carrito_pretzel,     'filadelfia', dict(lado=256, bisel=0.0)),
    'arco_philly':         (arco_philly,         'filadelfia', dict(lado=1024, bisel=0.0, suelo=False)),
    'casa_moneda_int':     (casa_moneda_int,     'filadelfia', dict(lado=2048, bisel=0.0, suelo=False)),
    'prensa_marco':        (prensa_marco,        'obstaculos', dict(lado=256, bisel=0.0)),
    'prensa_martillo':     (prensa_martillo,     'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
    'pretzel_gigante':     (pretzel_gigante,     'obstaculos', dict(lado=256, bisel=0.0)),
    'autobus_septa':       (autobus_septa,       'obstaculos', dict(lado=256, bisel=0.0)),
    'cartel_pa':           (cartel_pa,           'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
}

correr(PIEZAS)
