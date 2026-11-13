# Nivel 18: Little Rock, Arkansas (13/11/2026).
#
#   blender -b -P blender/littlerock.py -- [pieza ...] [--rapido]
#
# Historia: «La mina de diamantes: tacos de oro para su torre».
#   Por President Clinton Avenue (el River Market, la biblioteca de Clinton
#   colgada sobre el césped, el viejo Capitolio blanco) se baja a la mina de
#   diamantes (por dentro: a oscuras, puntales de madera, farolillos, raíles,
#   vagonetas y vetas que brillan) y se sale hasta el Capitolio de Arkansas.
# Obstáculos (carpeta obstaculos): el jabalí Razorback (viene zigzagueando),
# el brillo del diamante (deslizándose encima se desentierra), la vagoneta de
# la mina, el puntal (agacharse), la caja de dinamita y la pancarta de los
# Razorbacks.

import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import *
from comun import _poner

def blanco():   return mat('blanco_ar', 0xf4f2ec, 0.5)
def negro():    return mat('negro_ar', 0x1b1c20, 0.4)
def rojo():     return mat('rojo_ar', 0x9d2235, 0.45)
def madera():   return mat('madera_ar', 0x7a5232, 0.8)
def madera_o(): return mat('madera_os_ar', 0x5a3a22, 0.85)
def roca():     return mat('roca_mina', 0x5e5246, 0.95)
def roca_o():   return mat('roca_mina_os', 0x3e342c, 0.95)
def tierra():   return mat('tierra_mina', 0x6a5440, 0.95)
def acero():    return mat('acero_ar', 0xa8aeb4, 0.3)
def oro():      return mat('oro_ar', 0xe8b840, 0.25)
def piedra():   return mat_bloques('piedra_ar', 0xe8e2d2, 0xc8c0ae, ancho=1.4, alto=0.7)

# ================================================================ edificios
def capitolio_ar():
    """El Capitolio de Arkansas (1915): piedra blanca, el pórtico de columnas,
    las dos alas y la cúpula con la linterna dorada."""
    Y = 20
    p = piedra()
    caja(p, 0, Y, 0, 76, 26, 16)
    caja(mat('cornisa_ar', 0xd8d0be, 0.6), 0, Y, 16, 77, 27, 1)
    escalinata(p, 0, Y - 13, 0, 24, 8, huella=0.5, tabica=0.3)
    columnata(p, -10, 10, 6, Y - 14, 2.4, 0.85, 13)
    fronton(p, 0, Y - 14.5, 15.4, 24, 4.5, 2)
    cil(p, 0, Y, 17, 12, 9, 32)
    columnata(p, -10, 10, 8, Y - 12.5, 17, 0.45, 8)
    cupula(mat('cupula_ar', 0xe6e0d0, 0.5), 0, Y, 26, 12, 10)
    cil(p, 0, Y, 36, 2.8, 4, 16)
    cupula(oro(), 0, Y, 40, 2.8, 2.2)
    cil(oro(), 0, Y, 42.2, 0.3, 3, 8)
    texto(mat('letras_ar', 0x5a4a3a, 0.5), 'ARKANSAS', 0, Y - 14.6, 17.6, tam=1.2, prof=0.06)

def clinton_library():
    """La biblioteca de Clinton (2004): la caja de cristal larga, colgada sobre
    el césped como un puente (lo llaman «el puente al siglo XXI»)."""
    Y = 14
    caja(mat('cesped_ar', 0x6a9a4a, 0.9), 0, Y, -0.05, 50, 26, 0.1)
    v = mat_ventanas('cristal_clinton', 0x6f8fa8, 0xd8dee2, paso_x=1.6, paso_z=1.8, hueco_x=1.45, hueco_z=1.6, variacion=1.02)
    caja(v, 6, Y, 8, 46, 14, 9)
    caja(mat('marco_clinton', 0xd8dee2, 0.4), 6, Y, 17, 46.6, 14.6, 0.6)
    for x in (-12, 4):
        caja(mat('pilar_clinton', 0xc8ccd0, 0.5), x, Y, 0, 4, 12, 8)
    for k in range(6):
        caja(mat('lama_clinton', 0xb8c0c6, 0.4), -14 + k * 8, Y - 7.1, 8.5, 0.3, 0.2, 8)
    for x in (-3, 3):
        cil(madera(), x, 2, 0, 0.12, 2, 6)
    caja(mat('letrero_clinton', 0x1f3a6a, 0.6), 0, 2, 1, 7, 0.2, 1.2)
    texto(blanco(), 'CLINTON LIBRARY', 0, 1.85, 1.6, tam=0.55, prof=0.04)

def old_state_house():
    """El viejo Capitolio (1842): blanco, griego, con el pórtico de columnas
    dóricas y las dos alas bajas."""
    Y = 12
    p = mat_bloques('estuco_osh', 0xf4f0e6, 0xdcd6c8, ancho=2, alto=1)
    caja(p, 0, Y, 0, 22, 16, 11)
    for s in (-1, 1):
        caja(p, s * 15, Y + 2, 0, 9, 12, 8)
    columnata(blanco(), -7, 7, 6, Y - 9.2, 0.6, 0.6, 9)
    fronton(blanco(), 0, Y - 9.8, 9.6, 16, 3, 2)
    caja(blanco(), 0, Y - 9, 0, 17, 3, 0.6)
    tejado(mat('tejado_osh', 0x8a8e92, 0.6), 0, Y - 8, Y + 8, 11, 22, 3)
    texto(mat('letras_osh', 0x5a4a3a, 0.5), 'OLD STATE HOUSE', 0, Y - 11.4, 9.9, tam=0.7, prof=0.04)

def river_market():
    """El River Market: los pabellones del mercado junto al río, con toldos
    de colores y el letrero."""
    Y = 10
    lad = mat_ventanas('ladrillo_rm', 0x2c3440, 0x9a4a32, paso_x=2.2, paso_z=3.4, hueco_x=1.6, hueco_z=2.4, variacion=1.06)
    caja(lad, 0, Y + 2, 0, 34, 14, 7)
    tejado(mat('tejado_rm', 0x3a5a3a, 0.6), 0, Y - 5, Y + 9, 7, 35, 3.5, vuelo=0.8, cumbrera='x')
    for k in range(5):
        x = -13 + k * 6.5
        c = [0xc8282c, 0xf2c230, 0x2f6fa8, 0x3a8a3a, 0xf28c1c][k]
        caja(mat('toldo_rm_%x' % c, c, 0.6), x, Y - 6.2, 2.6, 5.4, 2.4, 0.2).rotation_euler = (0.25, 0, 0)
        caja(mat('puesto_rm', 0xd8c8a6, 0.7), x, Y - 6.5, 0, 4.5, 1.6, 1.1)
    texto(mat('letras_rm', 0xf2e6c8, 0.5), 'RIVER MARKET', 0, Y - 5.1, 5, tam=1.2, prof=0.06)

def mina():
    """La mina de diamantes por dentro (momento estrella). Galería de roca con
    puntales de madera cada pocos metros, farolillos que alumbran, raíles por
    los tres carriles, vagonetas aparcadas y vetas de diamante que brillan.
    Cruza la calle: el origen en el centro, la calle a lo largo de y."""
    L = 420
    caja(tierra(), 0, 0, -0.3, 30, L, 0.3)
    for s in (-1, 1):                                    # paredes y techo de roca
        caja(roca(), s * 12.5, 0, 0, 4, L, 11)
    caja(roca_o(), 0, 0, 10, 29, L, 2)
    import random
    r = random.Random(18)
    for k in range(70):
        s = r.choice((-1, 1))
        esfera(roca_o() if k % 2 else roca(), s * r.uniform(9.8, 10.6), r.uniform(-L / 2, L / 2), r.uniform(1, 9), r.uniform(0.8, 2.2), 2, esc=(0.6, 1.2, 1))
    veta = luz('veta_diamante', 0xbff4ff, 1.4)
    for k in range(120):
        s = r.choice((-1, 1))
        esfera(veta, s * 10.35, r.uniform(-L / 2, L / 2), r.uniform(0.8, 8), r.uniform(0.08, 0.18), 1)
    farol = luz('farolillo_mina', 0xffc070, 1.5)
    for k in range(int(L / 7)):                          # puntales y farolillos
        y = -L / 2 + 3.5 + k * 7
        for s in (-1, 1):
            caja(madera_o(), s * 10, y, 0, 0.5, 0.5, 9.4)
        caja(madera_o(), 0, y, 9.2, 21, 0.6, 0.6)
        if k % 2 == 0:
            cil(negro(), 0, y, 8.3, 0.04, 0.9, 4)
            esfera(farol, 0, y, 8.1, 0.28, 2)
    for x in (-2.2, 0, 2.2):                             # raíles
        for s in (-1, 1):
            caja(acero(), x + s * 0.55, 0, 0, 0.1, L, 0.12)
    for k in range(int(L / 1.2)):
        caja(madera(), 0, -L / 2 + k * 1.2, -0.02, 7.2, 0.25, 0.06)
    for (x, y) in ((-8, -120), (8, -20), (-8, 70), (8, 160)):   # vagonetas aparcadas
        caja(mat('vagoneta_mina', 0x5a5e62, 0.4), x, y, 0.5, 1.6, 2.4, 1.2)
        esfera(mat('mineral', 0x8a7a6a, 0.9), x, y, 1.7, 0.8, 2, esc=(0.9, 1.3, 0.4))
    for (y, txt) in ((-L / 2 + 0.6, 'CRATER OF DIAMONDS'), (L / 2 - 0.6, 'SALIDA')):
        caja(madera(), 0, y, 7.2, 14, 0.3, 1.6)
        texto(mat('letras_mina', 0xf2e6c8, 0.5), txt, 0, y - 0.2, 7.7, tam=0.9, prof=0.05)

# ================================================================ obstáculos
def jabali():
    """El jabalí de los Razorbacks (mira a -y): rojo oscuro, la cresta de
    púas en el lomo, los colmillos blancos y el morro."""
    pelo = mat('jabali_pelo', 0x7a2a22, 0.9)
    oscuro = mat('jabali_oscuro', 0x4a1a14, 0.9)
    esfera(pelo, 0, 0.2, 0.75, 0.6, 3, esc=(0.8, 1.45, 0.85))
    esfera(pelo, 0, -0.75, 0.75, 0.42, 3, esc=(0.85, 1.0, 0.9))
    esfera(mat('morro_jabali', 0xc87a6a, 0.6), 0, -1.12, 0.66, 0.18, 2, esc=(1, 0.7, 0.8))
    for s in (-1, 1):
        esfera(negro(), s * 0.18, -1.05, 0.88, 0.05, 1)
        rama(mat('colmillo', 0xf4f0e2, 0.4), (s * 0.14, -1.1, 0.58), (s * 0.24, -1.2, 0.8), 0.04, 0.015, 5)
        esfera(oscuro, s * 0.25, -0.62, 1.08, 0.1, 1, esc=(0.6, 0.5, 1.4))
    for k in range(9):                                   # la cresta
        y = -0.6 + k * 0.16
        cil(oscuro, 0, y, 1.15 - abs(k - 3) * 0.03, 0.07, 0.25, 4, r2=0.0)
    for (x, y) in ((-0.28, -0.45), (0.28, -0.45), (-0.28, 0.75), (0.28, 0.75)):
        cil(oscuro, x, y, 0, 0.09, 0.42, 6)
    rama(oscuro, (0, 1.05, 0.85), (0, 1.25, 0.6), 0.04, 0.02, 4)

def brillo_diamante():
    """El brillo del diamante en el suelo: un montoncito de tierra y el
    diamante asomando (se pisa; deslizándose encima se desentierra)."""
    esfera(tierra(), 0, 0, -0.05, 0.6, 2, esc=(1, 1, 0.3))
    d = luz('diamante', 0xc8f6ff, 1.6)
    cil(d, 0, 0, 0.12, 0.28, 0.18, 8, r2=0.18)
    cil(d, 0, 0, 0.3, 0.18, 0.22, 8, r2=0.0)
    for k in range(4):
        a = k * math.pi / 2 + 0.4
        caja(luz('destello', 0xffffff, 1.5), math.cos(a) * 0.45, math.sin(a) * 0.45, 0.3, 0.04, 0.04, 0.3)

def vagoneta_mina():
    """La vagoneta de la mina llena de mineral, parada en su raíl."""
    hierro = mat('hierro_vag', 0x5a5e62, 0.45)
    caja(hierro, 0, 0, 0.35, 1.5, 2.3, 1.1)
    caja(mat('borde_vag', 0x3a3e42, 0.5), 0, 0, 1.4, 1.6, 2.4, 0.1)
    esfera(mat('mineral_vag', 0x8a7a6a, 0.9), 0, 0, 1.45, 0.75, 2, esc=(0.9, 1.4, 0.45))
    for k in range(3):
        esfera(luz('veta_vag', 0xbff4ff, 1.3), -0.3 + k * 0.3, -0.3 + k * 0.25, 1.75, 0.07, 1)
    for (x, y) in ((-0.6, -0.75), (0.6, -0.75), (-0.6, 0.75), (0.6, 0.75)):
        cil(negro(), x, y, 0.25, 0.25, 0.12, 12, eje='X')

def puntal():
    """El puntal de madera cruzado a la altura de la cabeza (agacharse)."""
    for x in (-1.2, 1.2):
        caja(madera_o(), x, 0, 0, 0.3, 0.3, 2.6)
    caja(madera_o(), 0, 0, 1.55, 2.8, 0.4, 0.45)
    cil(negro(), 0, 0, 1.25, 0.03, 0.3, 4)
    esfera(luz('farol_puntal', 0xffc070, 1.5), 0, 0, 1.15, 0.16, 2)

def tnt():
    """La caja de dinamita (se salta)."""
    caja(madera(), 0, 0, 0, 1.3, 0.9, 0.75)
    caja(rojo(), 0, -0.46, 0.25, 0.9, 0.02, 0.28)
    texto(mat('letras_tnt', 0xf6f2e6, 0.5), 'TNT', 0, -0.48, 0.38, tam=0.22, prof=0.01)
    for k in range(4):
        cil(mat('cartucho', 0xc8282c, 0.5), -0.36 + k * 0.24, 0.1, 0.75, 0.08, 0.35, 8)
    rama(negro(), (0.12, 0.1, 1.1), (0.3, -0.1, 1.35), 0.015, 0.015, 4)

def cartel_pig():
    """La pancarta de los Razorbacks (agacharse): «WOO PIG SOOIE!»."""
    for x in (-1.25, 1.25):
        cil(madera(), x, 0, 0, 0.07, 2.75, 8)
    caja(rojo(), 0, 0, 1.55, 2.4, 0.06, 1.05)
    texto(blanco(), 'WOO PIG', 0, -0.04, 2.22, tam=0.3, prof=0.02)
    texto(blanco(), 'SOOIE!', 0, -0.04, 1.84, tam=0.3, prof=0.02)

PIEZAS = {
    'capitolio_ar':    (capitolio_ar,    'littlerock', dict(lado=2048, segmentos=1, min_bisel=1.0)),
    'clinton_library': (clinton_library, 'littlerock', dict(lado=1024, bisel=0.0)),
    'old_state_house': (old_state_house, 'littlerock', dict(lado=1024, segmentos=1, min_bisel=1.0)),
    'river_market':    (river_market,    'littlerock', dict(lado=1024, bisel=0.0)),
    'mina':            (mina,            'littlerock', dict(lado=2048, bisel=0.0, suelo=False)),
    'jabali':          (jabali,          'obstaculos', dict(lado=256, bisel=0.0)),
    'brillo_diamante': (brillo_diamante, 'obstaculos', dict(lado=256, bisel=0.0)),
    'vagoneta_mina':   (vagoneta_mina,   'obstaculos', dict(lado=256, bisel=0.0)),
    'puntal':          (puntal,          'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
    'tnt':             (tnt,             'obstaculos', dict(lado=256, bisel=0.0)),
    'cartel_pig':      (cartel_pig,      'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
}

correr(PIEZAS)
