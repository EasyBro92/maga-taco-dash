# Nivel 44: Atlantic City, Nueva Jersey (15/11/2026).
#
#   blender -b -P blender/atlanticcity.py -- [pieza ...] [--rapido]
#
# Historia: «Sus casinos arruinados: con él hasta la banca pierde. Fichas
#   rodando». Acto del Sentido Común. Por el Boardwalk: el gran salón Boardwalk
#   Hall, el muelle con la noria, Lucy la elefanta (el edificio con forma de
#   elefante) y las tragaperras en las aceras. Las tragaperras sobre la calle:
#   tocar para parar los tres rodillos (lo que sale en cada carril: tacos, una
#   pila de fichas o el premio gordo); el momento estrella, el blackjack en el
#   casino (coger una carta por carril y plantarse antes de pasarse de 21).
#   Final en el casino arruinado de las cúpulas, CERRADO. Pancarta del Sentido
#   Común: LA BANCA SIEMPRE GANA.
# Obstáculos (carpeta obstaculos): el arco de la tragaperras, la pila de
# fichas, la ficha gigante tumbada, el minibús (jitney) y la pancarta.

import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import *

def blanco():    return mat('blanco_ac', 0xf6f4ee, 0.5)
def negro():     return mat('negro_ac', 0x1c1c20, 0.4)
def cristal():   return mat('cristal_ac', 0x3a5a70, 0.15)
def rojo():      return mat('rojo_ac', 0xc8202a, 0.45)
def azul():      return mat('azul_ac', 0x1e4a9a, 0.45)
def amarillo():  return mat('amarillo_ac', 0xf2c21a, 0.45)
def oro():       return mat('oro_ac', 0xe8b840, 0.22)
def rosa():      return mat('rosa_ac', 0xf08aa8, 0.5)
def verde():     return mat('verde_ac', 0x1e7a3e, 0.6)
def morado():    return mat('morado_ac', 0x6a2a8a, 0.5)
def gris():      return mat('gris_ac', 0x8a9098, 0.4)
def hierro():    return mat('hierro_ac', 0x2a2c30, 0.45)
def madera():    return mat('madera_ac', 0x9a6a3e, 0.85)
def madera_o():  return mat('madera_oscura_ac', 0x5a3a22, 0.85)
def piedra_l():  return mat('piedra_lisa_ac', 0xe4ddcc, 0.6)
def bombilla():  return luz('bombilla_ac', 0xffe6a0, 1.2)
def neon_r():    return luz('neon_rojo_ac', 0xff3a5a, 1.4)

def cartel_sentido(x, y, z, w, h, linea1, linea2=''):
    caja(azul(), x, y, z, w, 0.06, h)
    caja(blanco(), x, y - 0.01, z + h - h * 0.08, w, 0.06, h * 0.08)
    esfera(rosa(), x - w / 2 + h * 0.32, y - 0.06, z + h * 0.5, h * 0.24, 1, esc=(1.2, 0.4, 1))
    texto(blanco(), linea1, x + h * 0.25, y - 0.045, z + h * (0.5 if not linea2 else 0.56), tam=h * 0.3, prof=0.02)
    if linea2:
        texto(amarillo(), linea2, x + h * 0.25, y - 0.045, z + h * 0.2, tam=h * 0.2, prof=0.02)

def ficha(x, y, z, r=0.5, col=None, plana=True):
    """Una ficha de casino: el disco de color con las rayas blancas del canto."""
    c = (col or rojo)()
    if plana:
        cil(c, x, y, z, r, r * 0.22, 24)
        for k in range(8):
            a = k * math.tau / 8
            caja(blanco(), x + math.cos(a) * r * 0.98, y + math.sin(a) * r * 0.98, z, r * 0.18, r * 0.06, r * 0.22, giro=a)
        cil(blanco(), x, y, z + r * 0.22, r * 0.6, 0.01, 20)
    else:
        cil(c, x, y, z + r, r, r * 0.22, 24, eje='Y')

def tragaperras_m(x, y, z=0.0, k=1.0):
    """Una máquina tragaperras: el mueble rojo, la pantalla con los tres
    rodillos, la palanca y las bombillas de arriba."""
    caja(rojo(), x, y, z, 0.9 * k, 0.7 * k, 1.7 * k)
    caja(blanco(), x, y - 0.36 * k, z + 1.0 * k, 0.7 * k, 0.02 * k, 0.35 * k)
    for i in range(3):
        caja([amarillo, rojo, azul][i](), x + (-0.22 + i * 0.22) * k, y - 0.37 * k, z + 1.06 * k, 0.15 * k, 0.02 * k, 0.22 * k)
    cil(hierro(), x + 0.5 * k, y, z + 1.0 * k, 0.03 * k, 0.6 * k, 6)
    esfera(rojo(), x + 0.5 * k, y, z + 1.6 * k, 0.07 * k, 1)
    caja(oro(), x, y, z + 1.7 * k, 0.9 * k, 0.7 * k, 0.15 * k)
    for i in range(4):
        esfera(bombilla(), x + (-0.3 + i * 0.2) * k, y - 0.36 * k, z + 1.5 * k, 0.04 * k, 1)

# ================================================================ la meta
def casino_arruinado():
    """El casino arruinado de las cúpulas (la meta): el palacio con cúpulas
    de cebolla y minaretes, el gran letrero TAJ CASINO, el cartel CERRADO
    cruzado y las fichas tiradas por la escalinata; la pancarta del
    Sentido Común delante."""
    Y = 22
    W, D, H = 56.0, 20.0, 18.0
    yf = Y - D / 2
    caja(mat('fachada_taj_ac', 0xf0e6d8, 0.7), 0, Y, 0, W, D, H)
    for k in range(13):
        x = -24 + k * 4
        for z in (2, 7, 12):
            caja(cristal(), x, yf - 0.05, z, 2.0, 0.1, 3.0)
            cil(oro(), x, yf - 0.08, z + 3.0, 1.0, 0.1, 12, eje='Y')
    for (x, r) in ((0, 7), (-16, 4.5), (16, 4.5)):
        cil(mat('tambor_taj_ac', 0xf0e6d8, 0.7), x, Y, H, r * 0.8, 3, 24)
        o = esfera(morado(), x, Y, H + 3 + r * 0.6, r, 2, esc=(1, 1, 1.25))
        cil(oro(), x, Y, H + 3 + r * 1.85, 0.2, 3, 6, r2=0.02)
    for s in (-1, 1):
        cil(mat('minarete_ac', 0xf6f0e6, 0.6), s * 30, yf, 0, 1.6, 34, 12)
        esfera(morado(), s * 30, yf, 34.8, 2.0, 2, esc=(1, 1, 1.3))
    caja(rojo(), 0, yf - 0.4, 14.2, 30, 0.3, 3.0)
    texto(neon_r(), 'TAJ CASINO', 0, yf - 0.6, 14.6, tam=2.2, prof=0.12)
    caja(blanco(), 0, yf - 0.8, 8.5, 16, 0.12, 2.2)
    texto(rojo(), 'CERRADO', 0, yf - 0.9, 8.9, tam=1.5, prof=0.04)
    rama(rojo(), (-8, yf - 1.0, 8.6), (8, yf - 1.0, 10.6), 0.12, 0.12, 4)
    for k in range(10):
        caja(piedra_l(), 0, yf - 1.2 - k * 0.5, 0, 26 + k * 0.6, 0.5, 3.0 - k * 0.3)
    for k in range(9):
        ficha(-10 + k * 2.6, yf - 5 - (k % 3) * 1.3, 0.1, 0.45, [rojo, azul, verde, negro][k % 4])
    caja(mat('suelo_boardwalk_ac', 0x9a7a5a, 0.85), 0, yf - 14, -0.05, 80, 18, 0.06)
    for x in (8, 22):
        cil(madera_o(), x, yf - 15, 0, 0.12, 4.4, 8)
    cartel_sentido(15, yf - 15, 2.8, 14, 1.6, 'LA BANCA SIEMPRE GANA', 'EL SENTIDO COMÚN')

# ================================================================ edificios
def boardwalk_hall():
    """Boardwalk Hall (1929): el gran salón de ladrillo y piedra con el arco
    enorme en la fachada y las letras BOARDWALK HALL."""
    Y = 14
    W, D, H = 46.0, 28.0, 22.0
    yf = Y - D / 2
    caja(mat_bloques('ladrillo_ac', 0xb8784e, 0x8a5434, ancho=0.4, alto=0.16), 0, Y, 0, W, D, H)
    cil(mat('boveda_ac', 0x8a8a90, 0.5), 0, Y, H, W / 2 - 1, D, 24, eje='Y').scale = (1, 1, 0.35)
    cil(cristal(), 0, yf - 0.05, 9, 8, 0.12, 24, eje='Y')
    caja(piedra_l(), 0, yf - 0.1, 0, 18, 0.2, 9)
    for k in range(6):
        caja(cristal(), -6.5 + k * 2.6, yf - 0.15, 0.5, 2.0, 0.1, 7.5)
    caja(piedra_l(), 0, yf - 0.2, 18.4, 26, 0.3, 2.0)
    texto(negro(), 'BOARDWALK HALL', 0, yf - 0.4, 18.8, tam=1.3, prof=0.05)

def steel_pier():
    """El muelle de acero con la noria: la entrada con el letrero STEEL
    PIER, el muelle y la noria grande detrás."""
    Y = 10
    caja(blanco(), 0, Y - 4, 0, 16, 2, 6)
    caja(azul(), 0, Y - 5.05, 4.0, 14, 0.1, 1.6)
    texto(blanco(), 'STEEL PIER', 0, Y - 5.1, 4.3, tam=1.0, prof=0.04)
    caja(madera(), 0, Y + 14, 0, 14, 34, 1.0)
    cx, cz = 0, 20
    for k in range(16):
        a = k * math.tau / 16
        rama(hierro(), (cx, Y + 14, cz), (cx + math.cos(a) * 16, Y + 14, cz + math.sin(a) * 16), 0.1, 0.1, 4)
        caja([rojo, amarillo, azul, verde][k % 4](), cx + math.cos(a) * 16, Y + 13.5, cz + math.sin(a) * 16 - 1.2, 1.4, 1.2, 1.2)
    for k in range(32):
        a0, a1 = k * math.tau / 32, (k + 1) * math.tau / 32
        rama(hierro(), (cx + math.cos(a0) * 16, Y + 14, cz + math.sin(a0) * 16), (cx + math.cos(a1) * 16, Y + 14, cz + math.sin(a1) * 16), 0.15, 0.15, 4)
    for s in (-1, 1):
        rama(hierro(), (s * 8, Y + 14, 1), (cx, Y + 14, cz), 0.3, 0.3, 6)

def lucy_elefanta():
    """Lucy la elefanta (1881): el edificio de seis pisos con forma de
    elefante, con su casita (el howdah) en el lomo."""
    Y = 10
    g = mat('lucy_ac', 0xc8c0b0, 0.7)
    esfera(g, 0, Y, 12, 7, 2, esc=(1.6, 1.0, 0.9))
    for (x, y) in ((-6, Y - 3.5), (6, Y - 3.5), (-6, Y + 3.5), (6, Y + 3.5)):
        cil(g, x, y, 0, 2.0, 8, 12)
    esfera(g, -11, Y, 15, 4.5, 2, esc=(1, 0.95, 1))
    for s in (-1, 1):
        esfera(g, -10.5, Y + s * 4.5, 15, 3.4, 2, esc=(0.4, 1, 1.2))
    rama(g, (-14.5, Y, 14), (-16, Y - 1, 7), 1.2, 0.6, 10)
    rama(g, (-16, Y - 1, 7), (-16.5, Y - 2.5, 3), 0.6, 0.5, 10)
    for s in (-1, 1):
        rama(blanco(), (-14, Y + s * 1.5, 12), (-17, Y + s * 1.8, 10.5), 0.35, 0.1, 8)
        esfera(negro(), -14.6, Y + s * 2.0, 17, 0.4, 1)
    caja(rojo(), 0, Y, 18.5, 6, 5, 3)
    cupula(oro(), 0, Y, 21.5, 3, 2.5, 16, 4)
    for x in (-3, 3):
        caja(cristal(), x, Y - 7.1, 10, 1.4, 0.1, 1.8)
    caja(blanco(), 0, Y - 9, 0.5, 6, 0.1, 1.0)
    texto(rojo(), 'LUCY', 0, Y - 9.06, 0.75, tam=0.6, prof=0.02)

def tragaperras_acera():
    """Una tragaperras de la acera."""
    tragaperras_m(0, 0, 0, 1.0)

# ================================================================ cruza la calle
def arco_boardwalk():
    """El arco del Boardwalk: dos postes con bombillas y el letrero
    ATLANTIC CITY · EL BOARDWALK; por detrás, ¡HAGAN JUEGO!"""
    for s in (-1, 1):
        caja(rojo(), s * 8.6, 0, 0, 0.7, 0.7, 7.8)
        for k in range(8):
            esfera(bombilla(), s * 8.6, -0.37, 0.8 + k * 0.9, 0.1, 1)
    caja(rojo(), 0, 0, 7.0, 18.0, 0.4, 0.6)
    caja(oro(), 0, 0, 4.4, 13, 0.18, 1.8)
    texto(rojo(), 'ATLANTIC CITY', 0, -0.12, 5.3, tam=0.75, prof=0.04)
    texto(negro(), 'EL BOARDWALK', 0, -0.12, 4.65, tam=0.45, prof=0.04)
    o = texto(rojo(), '¡HAGAN JUEGO!', 0, 0.12, 5.0, tam=0.7, prof=0.04)
    o.rotation_euler = (math.pi / 2, 0, math.pi)
    for k in range(17):
        esfera(bombilla(), -8 + k, -0.22, 7.6, 0.1, 1)

# ================================================================ el casino
def casino_floor():
    """El casino por dentro (momento estrella): la moqueta roja con dibujos,
    las filas de tragaperras a los lados, las mesas de blackjack con sus
    crupieres, las ruletas, las lámparas de araña quietas y los arcos de
    SALIDA y META. Cruza la calle: el origen en el centro."""
    L = 420
    caja(mat_bloques('moqueta_ac', 0x8a1a2a, 0x6a1220, ancho=1.2, alto=1.2, grosor=0.08, variacion=1.15), 0, 0, -0.2, 28, L, 0.2)
    for s in (-1, 1):
        caja(mat('pared_casino_ac', 0x3a1a3a, 0.7), s * 15, 0, 0, 0.6, L, 10)
        # (las tragaperras del fondo, sencillas: con todo su detalle salian miles de piezas)
        for k in range(int(L / 2.4)):
            y = -L / 2 + 1.2 + k * 2.4
            caja(rojo(), s * 13.5, y, 0, 0.7, 1.6, 1.7)
            caja(amarillo(), s * 13.5 - s * 0.36, y, 1.0, 0.02, 1.2, 0.35)
            caja(oro(), s * 13.5, y, 1.7, 0.7, 1.6, 0.15)
        for k in range(int(L / 28)):
            y = -L / 2 + 14 + k * 28
            caja(verde(), s * 9, y, 0, 3.2, 2.0, 0.95)
            caja(madera_o(), s * 9, y, 0.95, 3.4, 2.2, 0.08)
            cil(mat('crupier_ac', 0xf6f4ee, 0.7), s * 10.8, y, 0, 0.3, 1.5, 8)
            cil(negro(), s * 10.8, y, 1.1, 0.32, 0.35, 8)
            esfera(mat('cara_ac', 0xe8b89a, 0.7), s * 10.8, y, 1.75, 0.22, 1)
            for i in range(3):
                caja(blanco(), s * 8.4, y - 0.8 + i * 0.8, 1.04, 0.3, 0.42, 0.01)
            ficha(s * 9.5, y + 0.6, 1.03, 0.12, rojo)
    for k in range(int(L / 35)):
        y = -L / 2 + 17 + k * 35
        cil(oro(), 0, y, 9.0, 0.05, 3, 4)
        for i in range(8):
            a = i * math.tau / 8
            esfera(bombilla(), math.cos(a) * 1.4, y + math.sin(a) * 1.4, 8.6, 0.15, 1)
        cil(oro(), 0, y, 8.4, 1.5, 0.15, 16)
    for (y, txt) in ((-L / 2 + 1, 'SALIDA'), (L / 2 - 1, 'META')):
        for s in (-1, 1):
            caja(oro(), s * 7.0, y, 0, 0.5, 0.5, 6.0)
        caja(oro(), 0, y, 5.4, 14.6, 0.5, 0.5)
        caja(negro(), 0, y, 3.9, 10, 0.16, 1.4)
        texto(amarillo(), 'BLACKJACK · ' + txt, 0, y - 0.1, 4.35, tam=0.55, prof=0.04)

# ================================================================ obstáculos
def arco_tragaperras():
    """El arco de la tragaperras sobre la calle (no estorba: lo que sale en
    cada carril sí): dos postes rojos y la caja dorada de arriba con las tres
    ventanas de los rodillos, una encima de cada carril (los símbolos los
    pone el juego)."""
    for s in (-1, 1):
        caja(rojo(), s * 3.7, 0, 0, 0.5, 0.6, 5.6)
    caja(oro(), 0, 0, 5.0, 8.0, 0.8, 2.0)
    for x in (-2.2, 0, 2.2):
        caja(negro(), x, -0.42, 5.25, 1.6, 0.05, 1.5)
    for k in range(16):
        esfera(bombilla(), -3.75 + k * 0.5, -0.42, 6.85, 0.08, 1)
    cil(hierro(), 4.3, 0, 5.4, 0.06, 1.4, 6)
    esfera(rojo(), 4.3, 0, 6.85, 0.2, 1)

def pila_fichas():
    """La pila de fichas gigantes (no se pasa): fichas de colores una encima
    de otra, algo torcidas."""
    for k in range(9):
        ficha(math.sin(k * 1.3) * 0.08, math.cos(k * 1.7) * 0.06, k * 0.22, 0.55, [rojo, azul, verde, negro, amarillo][k % 5])

def ficha_gigante():
    """Una ficha gigante tumbada en la calle (se salta)."""
    ficha(0, 0, 0, 0.75, azul)

def jitney():
    """El jitney, el minibús azul de Atlantic City (no se pasa). El morro en
    el origen."""
    a = mat('jitney_ac', 0x3a8ad8, 0.45)
    caja(a, 0, 3.0, 0.4, 2.3, 6.0, 2.2)
    caja(cristal(), 0, 0.0, 1.4, 2.0, 0.1, 0.9)
    for y in (1.2, 2.8, 4.4):
        for s in (-1, 1):
            caja(cristal(), s * 1.16, y, 1.4, 0.05, 1.2, 0.8)
    caja(blanco(), 0, 3.0, 0.6, 2.35, 6.0, 0.2)
    caja(blanco(), 0, -0.02, 2.2, 1.6, 0.05, 0.3)
    texto(azul(), 'JITNEY', 0, -0.04, 2.25, tam=0.2, prof=0.01)
    for (y, s) in ((1.0, 1), (5.0, 1), (1.0, -1), (5.0, -1)):
        cil(negro(), s * 1.1, y, 0.38, 0.38, 0.3, 14, eje='X')
    for s in (-1, 1):
        caja(luz('faro_jitney_ac', 0xfff2c0, 1.0), s * 0.8, -0.03, 0.75, 0.35, 0.05, 0.2)

def cartel_nj():
    """La pancarta del Sentido Común (agacharse): LA BANCA SIEMPRE GANA."""
    for x in (-1.25, 1.25):
        cil(madera_o(), x, 0, 0, 0.07, 2.75, 8)
    caja(azul(), 0, 0, 1.5, 2.4, 0.05, 1.2)
    esfera(rosa(), -0.9, -0.05, 2.1, 0.2, 1, esc=(1.2, 0.4, 1))
    texto(blanco(), 'LA BANCA', 0.15, -0.035, 2.2, tam=0.22, prof=0.02)
    texto(amarillo(), 'SIEMPRE GANA', 0.15, -0.035, 1.8, tam=0.2, prof=0.02)

PIEZAS = {
    'casino_arruinado':  (casino_arruinado,  'atlanticcity', dict(lado=2048, bisel=0.0)),
    'boardwalk_hall':    (boardwalk_hall,    'atlanticcity', dict(lado=1024, bisel=0.0)),
    'steel_pier':        (steel_pier,        'atlanticcity', dict(lado=1024, bisel=0.0)),
    'lucy_elefanta':     (lucy_elefanta,     'atlanticcity', dict(lado=1024, bisel=0.0)),
    'tragaperras_acera': (tragaperras_acera, 'atlanticcity', dict(lado=256, bisel=0.0)),
    'arco_boardwalk':    (arco_boardwalk,    'atlanticcity', dict(lado=1024, bisel=0.0, suelo=False)),
    'casino_floor':      (casino_floor,      'atlanticcity', dict(lado=2048, bisel=0.0, suelo=False)),
    'arco_tragaperras':  (arco_tragaperras,  'obstaculos',   dict(lado=256, bisel=0.0)),
    'pila_fichas':       (pila_fichas,       'obstaculos',   dict(lado=256, bisel=0.0)),
    'ficha_gigante':     (ficha_gigante,     'obstaculos',   dict(lado=256, bisel=0.0)),
    'jitney':            (jitney,            'obstaculos',   dict(lado=256, bisel=0.0)),
    'cartel_nj':         (cartel_nj,         'obstaculos',   dict(lado=256, bisel=0.0, suelo=False)),
}

correr(PIEZAS)
