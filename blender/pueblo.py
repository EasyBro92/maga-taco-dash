# El pueblo en dibujo animado (21/10/2026). Ver comun.py.
#
#   blender -b -P blender/pueblo.py -- [pieza ...] [--rapido]
#
# El barrio residencial de EE. UU. de las películas (referencia que eligió
# Isidro en agosto: la casa victoriana de Gru). Cada casa trae su césped, su
# valla blanca de estacas y su camino hasta la acera. En la acera: robles,
# arbustos con flores, buzones con banderita y farolas de farol.
#
# Fachadas: la fachada en y = 0 mirando a -y; el jardín delante, hasta y = -3.2.

import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import *

JARDIN = 3.2          # fondo del jardín delantero

def marco():    return mat('marco', 0xffffff)
def blanco():   return mat('blanco_valla', 0xfbfaf5, 0.6)
def cesped():   return mat('cesped', 0x72c64e, 0.9)
def camino():   return mat('camino', 0xd8cfbd, 0.9)
def piedra():   return mat('piedra', 0xa8a197, 0.9)
def ladrillo(): return mat_bloques('ladrillo_chimenea', 0xb5523b, 0xe2d8c8, ancho=0.25, alto=0.085, grosor=0.012)
def hierro():   return mat('hierro', 0x2a2d33, 0.4)

def tablillas(nombre, color):
    """Pared de tablillas de madera (clapboard): solo juntas horizontales."""
    return mat_bloques(nombre, color, _oscurecer(color, 0.82), ancho=60, alto=0.16, grosor=0.012, desfase=0.0, variacion=1.0)

def tejas(nombre, color):
    return mat_bloques(nombre, color, _oscurecer(color, 0.7), ancho=0.32, alto=0.14, grosor=0.018, variacion=1.12)

def _oscurecer(c, f):
    r, g, b = (c >> 16) & 255, (c >> 8) & 255, c & 255
    return (int(r * f) << 16) | (int(g * f) << 8) | int(b * f)


def jardin(ancho, hueco_x, hueco_w=1.0, flores=(0xff4f6d, 0xffd23f, 0xb06bff)):
    """Césped, camino hasta la acera y valla de estacas con su puerta."""
    caja(cesped(), 0, -JARDIN / 2, 0, ancho, JARDIN, 0.05)
    caja(camino(), hueco_x, -JARDIN / 2, 0, hueco_w * 0.9, JARDIN, 0.07)
    y = -JARDIN + 0.08
    x = -ancho / 2 + 0.06
    while x < ancho / 2:
        if abs(x - hueco_x) > hueco_w / 2:
            caja(blanco(), x, y, 0, 0.09, 0.035, 0.62)
            cil(blanco(), x, y, 0.62, 0.064, 0.1, 4, r2=0.0)
        x += 0.19
    for a, b in ((-ancho / 2, hueco_x - hueco_w / 2), (hueco_x + hueco_w / 2, ancho / 2)):
        for z in (0.18, 0.48):
            caja(blanco(), (a + b) / 2, y + 0.03, z, b - a, 0.03, 0.07)
    # flores al pie de la valla
    for i, x in enumerate([v * 0.45 - ancho / 2 + 0.3 for v in range(int(ancho / 0.45))]):
        if abs(x - hueco_x) > hueco_w / 2 + 0.2:
            esfera(mat(f'flor{flores[i % 3]:06x}', flores[i % 3], 0.8), x, y + 0.25, 0.12, 0.12, 1)

def ventana_casa(x, z, w, h, persiana, y=0.0):
    ventana(x, z, w, h, y=y, persiana=persiana, remate='cornisa')

def porche(x, ancho, fondo, alto, techo, columnas=4):
    """Porche con suelo de madera, columnas, barandilla y tejadillo."""
    madera = mat('madera_porche', 0xc9a27a, 0.8)
    caja(madera, x, -fondo / 2, 0, ancho, fondo, 0.35)
    for i in range(columnas):
        cx = x - ancho / 2 + 0.12 + i * (ancho - 0.24) / (columnas - 1)
        cil(blanco(), cx, -fondo + 0.12, 0.35, 0.07, alto, 8)
    caja(blanco(), x, -fondo / 2 - 0.05, 0.35 + alto, ancho + 0.15, fondo + 0.1, 0.12)
    caja(techo, x, -fondo / 2 - 0.05, 0.47 + alto, ancho + 0.3, fondo + 0.35, 0.08, inclina=0.18)
    # barandilla con balaustres
    for a, b in ((x - ancho / 2 + 0.12, x - 0.45), (x + 0.45, x + ancho / 2 - 0.12)):
        if b - a < 0.3:
            continue
        caja(blanco(), (a + b) / 2, -fondo + 0.12, 0.95, b - a, 0.06, 0.06)
        n = int((b - a) / 0.16)
        for k in range(n + 1):
            caja(blanco(), a + k * (b - a) / n, -fondo + 0.12, 0.35, 0.035, 0.035, 0.6)
    escalinata(madera, x, -fondo, 0, 0.9, 2, huella=0.25, tabica=0.17)


# ---------------------------------------------------------------- casas
def victoriana(pared_c, tejado_c, persiana_c, torre=False, nombre='v'):
    W, D, H = 4.4, 4.0, 3.4
    pared = tablillas(f'tablillas{pared_c:06x}', pared_c)
    teja = tejas(f'tejas{tejado_c:06x}', tejado_c)
    persiana = mat(f'persiana{persiana_c:06x}', persiana_c, 0.6)
    caja(piedra(), 0, D / 2, 0, W + 0.1, D + 0.1, 0.35)
    caja(pared, 0, D / 2, 0.35, W, D, H - 0.35)
    caja(marco(), 0, D / 2, H - 0.12, W + 0.08, D + 0.08, 0.12)
    hastial(pared, 0, 0, D, H, W, 2.0)
    tejado(teja, 0, 0, D, H, W, 2.0, vuelo=0.3)
    cil(marco(), 0, -0.02, H + 0.75, 0.32, 0.08, 16, eje='Y')            # ojo de buey
    cil(mat('cristal', 0x2d4f86, 0.25), 0, -0.06, H + 0.75, 0.23, 0.04, 16, eje='Y')
    caja(ladrillo(), 1.3, 2.9, H, 0.5, 0.5, 2.4)
    caja(piedra(), 1.3, 2.9, H + 2.4, 0.62, 0.62, 0.12)
    for x in (-1.2, 1.2):                                               # planta de arriba
        ventana_casa(x, 2.05, 0.6, 0.9, persiana)
    ventana_casa(-1.2, 0.7, 0.75, 1.05, persiana)
    puerta(0.9, 0.35, 0.7, 1.35, color=persiana_c)
    porche(0.25, 3.6, 1.4, 1.45, teja)
    if torre:
        tx = -W / 2 - 0.1
        cil(pared, tx, 0.3, 0, 0.95, H + 0.9, 14)
        cil(marco(), tx, 0.3, H + 0.75, 1.0, 0.15, 14)
        cil(teja, tx, 0.3, H + 0.9, 1.15, 2.0, 14, r2=0.0)
        cil(hierro(), tx, 0.3, H + 2.85, 0.03, 0.45, 6)
        esfera(mat('dorado', 0xf2c23a, 0.3), tx, 0.3, H + 3.3, 0.07, 1)
        for z in (0.8, 2.1):
            ventana(tx, z, 0.45, 0.8, y=-0.62)
    for s in (-1.75, 1.75):                                             # setos
        esfera(mat('seto', 0x3f9a3a, 0.9), s, -0.35, 0.3, 0.4, 2, esc=(1.2, 0.8, 0.8))
    jardin(W + 2.4, 0.9)

def rancho():
    """Casa baja con garaje, entrada de coches y canasta."""
    W, D, H = 6.4, 4.2, 2.5
    pared = tablillas('tablillas_amarilla', 0xf6d77a)
    teja = tejas('tejas_marron', 0x8a5a3c)
    persiana = mat('persiana_verde', 0x2f6b4a, 0.6)
    caja(piedra(), 0, D / 2, 0, W + 0.1, D + 0.1, 0.25)
    caja(pared, 0, D / 2, 0.25, W, D, H - 0.25)
    caja(marco(), 0, D / 2, H - 0.12, W + 0.08, D + 0.08, 0.12)
    hastial(pared, 0, 0, D, H, W, 1.2, cumbrera='x')
    tejado(teja, 0, 0, D, H, W, 1.2, vuelo=0.35, cumbrera='x')
    caja(ladrillo(), -2.2, 2.6, H, 0.45, 0.45, 1.6)
    # garaje: puerta de paneles, la canasta encima y la entrada asfaltada
    paneles = mat_bloques('garaje', 0xf5f2ea, 0xcfc9bc, ancho=0.7, alto=0.4, grosor=0.02, desfase=0.0)
    caja(paneles, 1.7, -0.03, 0.25, 2.3, 0.06, 1.85)
    caja(marco(), 1.7, -0.05, 2.1, 2.5, 0.06, 0.1)
    caja(marco(), 1.7, -0.15, 2.35, 0.9, 0.05, 0.6)                    # tablero
    caja(mat('cuadro_rojo', 0xd8322f), 1.7, -0.18, 2.45, 0.4, 0.01, 0.3)
    caja(mat('cuadro_blanco', 0xffffff), 1.7, -0.19, 2.48, 0.32, 0.01, 0.22)
    cil(mat('aro', 0xff7a1a, 0.4), 1.7, -0.42, 2.4, 0.24, 0.04, 14)
    caja(mat('asfalto_entrada', 0x6e6e72, 0.9), 1.7, -JARDIN / 2, 0, 2.4, JARDIN, 0.07)
    # vivienda
    ventana_casa(-1.9, 0.75, 1.2, 1.0, persiana)
    ventana_casa(-0.35, 0.95, 0.6, 0.8, persiana)
    puerta(0.55, 0.25, 0.7, 1.4, color=0xd8322f)
    caja(madera := mat('madera_porche', 0xc9a27a, 0.8), 0.55, -0.4, 0, 1.2, 0.8, 0.25)
    for s in (-1, 1):
        esfera(mat('seto', 0x3f9a3a, 0.9), s * 1.1 - 1.2, -0.35, 0.28, 0.38, 2, esc=(1.2, 0.8, 0.8))
    jardin(W + 1.4, 0.55, hueco_w=0.9)

def colonial():
    W, D, H = 5.2, 4.0, 3.6
    pared = tablillas('tablillas_marino', 0x2f4a78)
    teja = tejas('tejas_gris', 0x5b6573)
    persiana = mat('persiana_negra', 0x1d2228, 0.6)
    caja(piedra(), 0, D / 2, 0, W + 0.1, D + 0.1, 0.35)
    caja(pared, 0, D / 2, 0.35, W, D, H - 0.35)
    caja(marco(), 0, D / 2, H - 0.14, W + 0.1, D + 0.1, 0.14)
    for s in (-1, 1):
        caja(marco(), s * W / 2, -0.02, 0.35, 0.16, 0.08, H - 0.35)       # esquinas blancas
    hastial(pared, 0, 0, D, H, W, 1.5, cumbrera='x')
    tejado(teja, 0, 0, D, H, W, 1.5, vuelo=0.3, cumbrera='x')
    for s in (-1, 1):
        caja(ladrillo(), s * (W / 2 - 0.3), 2.0, H, 0.55, 0.6, 2.0)
        bx = s * 1.2                                                     # buhardillas
        caja(pared, bx, 0.9, H + 0.1, 0.8, 0.9, 0.75)
        tejado(teja, bx, 0.45, 1.35, H + 0.85, 0.8, 0.35, vuelo=0.08, grosor=0.06)
        hastial(pared, bx, 0.45, 1.35, H + 0.85, 0.8, 0.35)
        ventana(bx, H + 0.25, 0.42, 0.5, y=0.45)
    for x in (-1.7, 0, 1.7):
        ventana_casa(x, 2.15, 0.6, 0.95, persiana)
    for x in (-1.7, 1.7):
        ventana_casa(x, 0.75, 0.65, 1.05, persiana)
    puerta(0, 0.35, 0.8, 1.45, color=0xd8322f)
    cil(marco(), 0, -0.04, 2.0, 0.42, 0.06, 16, eje='Y')                # abanico sobre la puerta
    columnata(blanco(), -0.65, 0.65, 2, -0.75, 0.35, 0.07, 1.65)
    caja(marco(), 0, -0.45, 2.0, 1.7, 0.95, 0.12)
    fronton(marco(), 0, -0.92, 2.12, 1.7, 0.42, 0.95)
    escalinata(piedra(), 0, -0.9, 0, 1.4, 2, huella=0.22, tabica=0.17)
    for s in (-1, 1):
        for k in (1.0, 2.2):
            esfera(mat('seto', 0x3f9a3a, 0.9), s * k, -0.35, 0.3, 0.36, 2)
    jardin(W + 1.8, 0.0, hueco_w=1.1)

def cabana_rosa():
    W, D, H = 4.0, 3.6, 2.4
    pared = tablillas('tablillas_rosa', 0xf4a6b8)
    teja = tejas('tejas_turquesa', 0x3f8f8a)
    persiana = mat('persiana_blanca', 0xffffff, 0.6)
    caja(piedra(), 0, D / 2, 0, W + 0.1, D + 0.1, 0.3)
    caja(pared, 0, D / 2, 0.3, W, D, H - 0.3)
    hastial(pared, 0, 0, D, H, W, 2.2)
    tejado(teja, 0, 0, D, H, W, 2.2, vuelo=0.35)
    ventana(0, H + 0.35, 0.55, 0.75, y=0.0, remate='cornisa')
    # mirador
    caja(pared, -0.9, -0.35, 0.3, 1.6, 0.7, 1.6)
    caja(teja, -0.9, -0.4, 1.9, 1.75, 0.85, 0.12, inclina=0.25)
    ventana(-0.9, 0.65, 1.1, 0.95, y=-0.7)
    caja(mat('jardinera', 0x6b3f2a), -0.9, -0.85, 0.5, 1.2, 0.2, 0.15)
    for k in range(6):
        esfera(mat(f'flor{[0xff4f6d, 0xffd23f][k % 2]:06x}', [0xff4f6d, 0xffd23f][k % 2], 0.8),
               -1.4 + k * 0.2, -0.85, 0.7, 0.09, 1)
    puerta(1.0, 0.3, 0.7, 1.3, color=0x3f8f8a)
    caja(mat('madera_porche', 0xc9a27a, 0.8), 1.0, -0.35, 0, 1.2, 0.7, 0.3)
    caja(teja, 1.0, -0.4, 1.85, 1.3, 0.8, 0.08, inclina=0.3)
    caja(ladrillo(), 1.2, 2.6, H + 0.6, 0.4, 0.4, 1.8)
    jardin(W + 1.6, 1.0, hueco_w=0.9, flores=(0xff7ab8, 0xffffff, 0xffd23f))

def iglesia():
    W, D, H = 5.0, 7.0, 3.4
    pared = tablillas('tablillas_iglesia', 0xfbfaf3)
    teja = tejas('tejas_iglesia', 0x5b6573)
    caja(piedra(), 0, D / 2, 0, W + 0.1, D + 0.1, 0.4)
    caja(pared, 0, D / 2, 0.4, W, D, H - 0.4)
    hastial(pared, 0, 0, D, H, W, 2.3)
    tejado(teja, 0, 0, D, H, W, 2.3, vuelo=0.3)
    for k in range(3):                                                  # ventanas ojivales al lado
        for s in (-1, 1):
            caja(mat('vidriera', 0x4a6fc4, 0.3), s * (W / 2 + 0.02), 1.6 + k * 1.8, 1.1, 0.04, 0.6, 1.4)
    # la torre del campanario delante
    tw = 1.7
    caja(pared, 0, -0.6, 0, tw, 1.4, H + 1.6)
    caja(marco(), 0, -0.6, H + 1.6, tw + 0.15, 1.55, 0.15)
    for dx in (-1, 1):
        for dy in (-1, 1):
            caja(pared, dx * (tw / 2 - 0.12), -0.6 + dy * 0.58, H + 1.75, 0.24, 0.24, 1.3)
    cil(mat('campana', 0xd9a53a, 0.3), 0, -0.6, H + 2.1, 0.35, 0.6, 12, r2=0.2)
    caja(marco(), 0, -0.6, H + 3.05, tw + 0.15, 1.55, 0.15)
    cil(teja, 0, -0.6, H + 3.2, 1.15, 3.4, 4, r2=0.0)
    caja(mat('dorado', 0xf2c23a, 0.3), 0, -0.6, H + 6.5, 0.07, 0.07, 0.8)
    caja(mat('dorado', 0xf2c23a, 0.3), 0, -0.6, H + 6.95, 0.45, 0.07, 0.07)
    caja(mat('reloj', 0xffffff, 0.4), 0, -1.32, H + 0.6, 0.75, 0.04, 0.75)
    cil(marco(), 0, -1.36, H + 0.97, 0.36, 0.04, 16, eje='Y')
    caja(hierro(), 0.1, -1.4, H + 0.95, 0.24, 0.02, 0.05)
    caja(hierro(), 0, -1.4, H + 0.97, 0.04, 0.02, 0.28)
    # puerta doble roja con escalones y el tablón de anuncios
    caja(mat('puerta_iglesia', 0xc0262c, 0.5), 0, -1.33, 0.4, 1.0, 0.04, 1.6)
    fronton(marco(), 0, -1.38, 2.0, 1.3, 0.5, 0.1)
    escalinata(piedra(), 0, -1.3, 0, 1.6, 2, huella=0.25, tabica=0.2)
    caja(mat('poste_cartel', 0x6b4a2f), 1.9, -2.6, 0, 0.08, 0.08, 1.0)
    caja(mat('poste_cartel', 0x6b4a2f), 2.9, -2.6, 0, 0.08, 0.08, 1.0)
    caja(mat('cartel_iglesia', 0x2f4a78, 0.5), 2.4, -2.62, 0.55, 1.3, 0.06, 0.6)
    texto(marco(), 'WELCOME', 2.4, -2.66, 0.85, tam=0.2, prof=0.02)
    jardin(W + 2.4, 0.0, hueco_w=1.4)


# ---------------------------------------------------------------- acera
def roble():
    tronco = mat('tronco', 0x6b4a2f, 0.9)
    rama(tronco, (0, 0, 0), (0.05, 0, 1.8), 0.24, 0.16)
    rama(tronco, (0.03, 0, 1.4), (0.7, 0.2, 2.5), 0.1, 0.06, 6)
    rama(tronco, (0.03, 0, 1.5), (-0.6, -0.3, 2.6), 0.1, 0.06, 6)
    verdes = [mat('hoja1', 0x4caf50, 0.8), mat('hoja2', 0x3d9a45, 0.8), mat('hoja3', 0x6cc04a, 0.8)]
    for i, (x, y, z, r) in enumerate(((0, 0, 3.0, 1.15), (0.85, 0.25, 2.7, 0.85), (-0.8, -0.2, 2.8, 0.85),
                                      (0.2, -0.8, 2.75, 0.8), (-0.2, 0.75, 2.9, 0.8), (0.3, 0.1, 3.75, 0.8),
                                      (-0.45, -0.1, 3.55, 0.7))):
        esfera(verdes[i % 3], x, y, z, r, 2, esc=(1, 1, 0.85))
    cil(cesped(), 0, 0, 0, 0.7, 0.04, 12)

def arbusto():
    verdes = [mat('seto', 0x3f9a3a, 0.9), mat('hoja3', 0x6cc04a, 0.8)]
    for i, (x, y, r) in enumerate(((0, 0, 0.5), (0.45, 0.1, 0.38), (-0.42, -0.05, 0.4))):
        esfera(verdes[i % 2], x, y, r * 0.75, r, 2, esc=(1, 1, 0.85))
    import random as _r
    _r.seed(4)
    for k in range(14):
        a = k / 14 * math.tau
        c = (0xff4f6d, 0xffd23f, 0xb06bff, 0xffffff)[k % 4]
        esfera(mat(f'flor{c:06x}', c, 0.8), math.cos(a) * 0.45, math.sin(a) * 0.3, 0.3 + _r.random() * 0.4, 0.07, 1)

def buzon_pueblo():
    caja(mat('poste_buzon', 0xf5f2ea, 0.6), 0, 0, 0, 0.1, 0.1, 1.0)
    negro = mat('buzon_negro', 0x24282e, 0.4)
    caja(negro, 0, 0, 1.0, 0.28, 0.5, 0.18)
    cil(negro, 0, 0, 1.18, 0.14, 0.5, 12, eje='Y')
    caja(mat('banderita', 0xd8322f, 0.4), 0.16, 0.1, 1.05, 0.02, 0.04, 0.4)
    caja(mat('banderita', 0xd8322f, 0.4), 0.16, 0.16, 1.32, 0.02, 0.16, 0.12)
    cil(mat('flor_buzon', 0xff4f6d, 0.8), 0, 0, 0, 0.35, 0.08, 12)

def farola_pueblo():
    negro = mat('farol', 0x22262b, 0.4)
    cil(negro, 0, 0, 0, 0.14, 0.3, 8, r2=0.1)
    cil(negro, 0, 0, 0.3, 0.06, 2.4, 8, r2=0.05)
    cil(negro, 0, 0, 2.7, 0.14, 0.08, 4)
    cil(mat('vidrio_farol', 0xffefb0, 0.2), 0, 0, 2.78, 0.16, 0.45, 4, r2=0.2)
    cil(negro, 0, 0, 3.23, 0.24, 0.25, 4, r2=0.0)
    for k in range(4):
        a = k / 4 * math.tau + math.pi / 4
        caja(negro, math.cos(a) * 0.16, math.sin(a) * 0.16, 2.78, 0.03, 0.03, 0.47)


def vict_blanca(): victoriana(0xfbf8ef, 0xc8412f, 0x2f4a78)
def vict_azul():   victoriana(0xa8c8e8, 0x5b6573, 0xffffff, torre=True)

PIEZAS = {
    'vict_blanca':   (vict_blanca,   'pueblo', dict(lado=1024)),
    'vict_azul':     (vict_azul,     'pueblo', dict(lado=1024)),
    'rancho':        (rancho,        'pueblo', dict(lado=1024)),
    'colonial':      (colonial,      'pueblo', dict(lado=1024)),
    'cabana_rosa':   (cabana_rosa,   'pueblo', dict(lado=1024)),
    'iglesia':       (iglesia,       'pueblo', dict(lado=1024)),
    'roble':         (roble,         'pueblo', dict(lado=512, bisel=0.0)),
    'arbusto':       (arbusto,       'pueblo', dict(lado=256, bisel=0.0)),
    'buzon_pueblo':  (buzon_pueblo,  'pueblo', dict(lado=256, bisel=0.0)),
    'farola_pueblo': (farola_pueblo, 'pueblo', dict(lado=256, bisel=0.0)),
}

correr(PIEZAS)
