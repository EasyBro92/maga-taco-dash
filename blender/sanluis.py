# Nivel 8: San Luis, Misuri (08/11/2026).
#
#   blender -b -P blender/sanluis.py -- [pieza ...] [--rapido]
#
# Isidro (08/11): «Aplica todas las preguntas que digas recomendados»: final
# bajo el arco Gateway y mañana soleada. Historia: «Bajo el arco Gateway, las
# etiquetas de precio no paran de crecer. Los aranceles los paga… ¿quién?».
#   izquierda:  el Old Courthouse (la cúpula verde) · la estación Union
#               Station con su torre del reloj
#   derecha:    el estadio de béisbol de los Cardinals
#   en medio:   el súper de los aranceles, «TARIFF MART» (el momento estrella:
#               por dentro, como el metro y el casino)
#   al fondo:   el arco Gateway, de acero, junto al río Misisipi, con un barco
#               de vapor en el muelle
# Obstáculos (carpeta obstaculos): la etiqueta de precio gigante colgada
# (agacharse; crece al acercarse), el carrito de la compra que viene rodando,
# las cajas con el precio, el carro de cerveza con caballos Clydesdale (cambia
# de carril) y el aficionado de los Cardinals (cruza).

import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import *

def blanco():   return mat('blanco_sl', 0xfbf8f2, 0.5)
def oscuro():   return mat('hueco_sl', 0x2b2c33, 0.8)
def vidrio():   return mat('vidrio_sl', 0x6a8aa8, 0.15)
def acero():    return mat('acero_arco', 0xdfe4ea, 0.12)
def hierro():   return mat('hierro_sl', 0x2c2e33, 0.4)
def rojo():     return mat('rojo_sl', 0xc8202e, 0.45)
def ladrillo(): return mat_bloques('ladrillo_sl', 0xa84a36, 0x8a3a2a, ancho=0.45, alto=0.2, grosor=0.02, variacion=1.08)
def caliza():   return mat_bloques('caliza_sl', 0xe4dcc8, 0xcdc2aa, ancho=1.4, alto=0.55, grosor=0.02, variacion=1.04)
def piedra_gris(): return mat_bloques('piedra_gris_sl', 0x9a9890, 0x828078, ancho=1.0, alto=0.5, grosor=0.03, variacion=1.06)
def cobre():    return mat('cobre_sl', 0x5f9e88, 0.5)
def luz_tubo(): return luz('fluorescente', 0xf4f8ff, 1.4)

# ================================================================ los edificios
def old_courthouse():
    """El Old Courthouse: piedra clara con pórtico de columnas y la cúpula de
    cobre verde sobre el tambor."""
    W, D = 30, 24
    caja(caliza(), 0, D / 2, 0, W, D, 14)
    caja(caliza(), 0, -1.5, 0, 14, 3.0, 1.2)
    columnata(blanco(), -5.6, 5.6, 6, -2.4, 1.2, 0.5, 9.0)
    caja(blanco(), 0, -1.5, 10.2, 14, 3.2, 1.2)
    fronton(blanco(), 0, -2.9, 11.4, 14, 3.0, 3.0)
    cil(caliza(), 0, D / 2, 14, 7.0, 7.0, 24)
    for k in range(16):
        a = k * 2 * math.pi / 16
        caja(oscuro(), math.sin(a) * 7.02, D / 2 - math.cos(a) * 7.02, 16.0, 0.9, 0.1, 2.6, giro=-a)
    cupula(cobre(), 0, D / 2, 21.0, 7.2, 7.5, lados=24, aros=6)
    cil(caliza(), 0, D / 2, 28.4, 1.2, 2.2, 12)
    cupula(cobre(), 0, D / 2, 30.6, 1.3, 1.2, lados=12, aros=4)
    for x in (-11, -8, 8, 11):
        ventana(x, 3.0, 1.6, 3.2, y=-0.1, marco=blanco(), cristal=vidrio())

def busch_stadium():
    """El estadio de béisbol: la fachada de ladrillo rojo con arcos, el letrero
    «BALLPARK» con el pájaro rojo y la estatua del jugador en la entrada."""
    W, D, H = 40, 30, 16
    caja(ladrillo(), 0, D / 2, 0, W, D, H)
    for x in range(-16, 17, 6):
        caja(oscuro(), x, -0.05, 0.3, 4.0, 0.1, 6.0)
        cil(oscuro(), x, -0.05, 6.3, 2.0, 0.1, 16, eje='Y')
        caja(oscuro(), x, -0.05, 10.0, 3.0, 0.1, 4.0)
    caja(hierro(), 0, D / 2, H, W, D, 0.5)
    for x in (-15, 15):
        cil(hierro(), x, 2.0, H, 0.2, 8.0, 8)
        caja(mat('foco_estadio', 0xf4f4e8, 0.3), x, 2.0, H + 8.0, 3.0, 0.6, 1.4)
    caja(mat('letrero_ball', 0xf6f2e8, 0.4), 0, -0.3, H - 3.6, 18, 0.3, 2.4)
    texto(rojo(), 'BALLPARK', -1.5, -0.5, H - 2.4, tam=1.5, prof=0.08)
    esfera(rojo(), 7.4, -0.5, H - 2.3, 0.7, 2, esc=(1.2, 0.6, 0.9))
    cil(mat('pico', 0xf2c230, 0.4), 8.3, -0.5, H - 2.3, 0.18, 0.4, 8, r2=0.02, eje='X')
    # La estatua del jugador con el bate.
    caja(caliza(), 0, -3.0, 0, 2.0, 2.0, 1.2)
    bronce = mat('bronce_sl', 0x6a4a2a, 0.35)
    cil(bronce, 0, -3.0, 1.2, 0.35, 1.6, 10)
    esfera(bronce, 0, -3.0, 3.1, 0.3, 2)
    rama(bronce, (0.2, -3.0, 2.6), (1.1, -3.2, 3.6), 0.08, 0.06, 6)

def union_station_stl():
    """Union Station de San Luis: piedra gris románica, arcos y la gran
    torre del reloj con su tejado puntiagudo."""
    W, D = 30, 22
    caja(piedra_gris(), 0, D / 2, 0, W, D, 12)
    tejado(mat('tejado_pizarra', 0x4a5258, 0.6), 0, 0, D, 12, W, 5)
    for x in (-10, -5, 0, 5, 10):
        caja(oscuro(), x, -0.05, 0.4, 2.6, 0.1, 4.0)
        cil(oscuro(), x, -0.05, 4.4, 1.3, 0.1, 14, eje='Y')
    # La torre del reloj.
    caja(piedra_gris(), 9.5, 4.0, 0, 6.0, 6.0, 30)
    cil(mat('esfera_reloj_sl', 0xfaf4e0, 0.4), 9.5, 0.95, 24.0, 1.6, 0.1, 24, eje='Y')
    caja(hierro(), 9.5, 0.88, 24.0, 0.08, 0.02, 1.2)
    caja(hierro(), 9.8, 0.88, 24.0, 0.7, 0.02, 0.08)
    for z in (30.0,):
        cil(mat('tejado_pizarra', 0x4a5258, 0.6), 9.5, 4.0, z, 4.4, 7.0, 4, r2=0.1).rotation_euler = (0, 0, math.pi / 4)
    texto(blanco(), 'UNION STATION', -2.0, -0.12, 9.6, tam=0.9, prof=0.06)

# ================================================================ la meta
def arco_gateway():
    """El arco Gateway: la catenaria de acero inoxidable (aquí 46 m), con su
    sección triangular que adelgaza hacia arriba, sobre el parque junto al
    río Misisipi, con un barco de vapor en el muelle. El jugador acaba
    debajo, en el paseo."""
    Y0 = 12.0
    caja(mat('cesped_arco', 0x6aa64c, 0.9), 0, 40, 0, 140, 90, 0.05)
    caja(mat('paseo_arco', 0xd6d0c4, 0.8), 0, 10, 0.02, 9, 40, 0.06)
    caja(mat('paseo_arco', 0xd6d0c4, 0.8), 0, Y0, 0.02, 64, 4, 0.06)
    # La catenaria: tramos de cilindro de pata a pata.
    A, H = 21.0, 46.0          # (algo más estrecho que el de verdad: que quepa en el móvil)
    n = 40
    pts = []
    for i in range(n + 1):
        t = -1 + 2 * i / n
        x = t * A
        z = H * (1 - (math.cosh(2.2 * t) - 1) / (math.cosh(2.2) - 1))
        pts.append((x, z))
    for i in range(n):
        (x1, z1), (x2, z2) = pts[i], pts[i + 1]
        r = 1.15 - 0.6 * (1 - abs(-1 + 2 * (i + 0.5) / n))
        rama(acero(), (x1, Y0, z1), (x2, Y0, z2), r + 0.05, r, 10)
    # El río y el barco de vapor.
    caja(mat('rio_misisipi', 0x5a7a7a, 0.15), 0, 95, -0.4, 200, 40, 0.3)
    bx, by = 24.0, 74.0
    blanco_b = mat('blanco_barco', 0xf6f4ee, 0.5)
    caja(blanco_b, bx, by, 0, 22, 7, 1.6)
    caja(blanco_b, bx, by, 1.6, 18, 6, 2.2)
    caja(blanco_b, bx - 1, by, 3.8, 12, 5, 2.0)
    for s in (-1, 1):
        cil(mat('chimenea_barco', 0x1d1f25, 0.5), bx + 6, by + s * 1.2, 3.8, 0.4, 6.0, 10)
    cil(rojo(), bx - 12.5, by, 2.4, 2.6, 4.6, 16, eje='X')
    texto(rojo(), 'MISSISSIPPI QUEEN', bx, by - 3.6, 2.6, tam=0.7, prof=0.04)

# ================================================================ el súper de los aranceles
PARED = 8.3
TECHO = 10.0
PUERTA = 3.8          # media puerta del súper (08/11 (2))
ALTO_PUERTA = 3.4
def suelo_super(): return mat_bloques('suelo_super', 0xeef0f2, 0xdfe2e6, ancho=1.2, alto=1.2, grosor=0.015, variacion=1.02)

def gondola(x, y, lado, k):
    """Una estantería de dos caras con productos de colores (cajas), perpendicular
    al pasillo, y su cartel de precio colgando encima."""
    caja(mat('gondola', 0xd8dce2, 0.4), x, y, 0, 4.0, 1.1, 2.2)
    colores = (0xd8283a, 0x2a6ab8, 0xf2c230, 0x3a9a4a, 0xe8781a, 0xa83ab8)
    for f, z in enumerate((0.25, 0.85, 1.45)):
        for c in range(5):
            col = colores[(c + f + k) % len(colores)]
            caja(mat('producto_%x' % col, col, 0.5), x - 1.6 + c * 0.8, y - 0.58, z, 0.6, 0.06, 0.45)
            caja(mat('producto_%x' % col, col, 0.5), x - 1.6 + c * 0.8, y + 0.58, z, 0.6, 0.06, 0.45)
    caja(mat('cartel_pasillo', 0x1f3a6a, 0.5), x, y, 4.6, 2.6, 0.08, 0.8)
    texto(mat('letra_pasillo', 0xfff2a0, 0.4), str(k + 1), x, y - 0.06, 5.0, tam=0.6, prof=0.02)

def super_pasillo():
    """30 m del súper por dentro: el pasillo central (la calle), estanterías de
    productos a los lados, carteles de precio, los tubos de luz a lo largo
    (a lo largo no parpadean) y la franja de la pared con «+145%»."""
    L = 30.0
    caja(suelo_super(), 0, 0, 0, PARED * 2, L, 0.09)
    for s in (-1, 1):
        for k, y in enumerate((-11.0, -5.5, 0.0, 5.5, 11.0)):
            gondola(s * 6.3, y, -s, k)
        caja(blanco(), s * (PARED + 0.1), 0, 0, 0.2, L, TECHO)
        caja(rojo(), s * (PARED - 0.02), 0, 5.6, 0.04, L, 1.2)
        for y in (-10.0, 5.0):
            o = texto(mat('letra_pared', 0xffffff, 0.4), 'PRICES +145%', 0, 0, 0, tam=0.7, prof=0.03)
            o.rotation_euler = (math.pi / 2, 0, -s * math.pi / 2)
            o.location = (s * (PARED - 0.06), y, 6.2)
    caja(mat('techo_super', 0xe8eaee, 0.6), 0, 0, TECHO, PARED * 2 + 0.4, L, 0.3)
    for x in (-5.0, -2.2, 2.2, 5.0):
        caja(luz_tubo(), x, 0, TECHO - 0.12, 0.25, L - 1.0, 0.1)

def super_entrada():
    """La fachada del súper (08/11 (2)). Isidro: «aparecen tuneles o tiendas
    sin ningún sentido, parecen abiertas de par en par». Antes era una caja
    más estrecha que la calle con un hueco enorme. Ahora es un súper de verdad
    que ocupa la manzana entera (levels.js quita los edificios de los lados):
    60 m de ancho y 13 de alto, con fondo hacia atrás, la franja roja, el
    letrero «TARIFF MART», escaparates con carteles de precios, la marquesina
    con la pancarta y una entrada del tamaño de una puerta. Las cuatro hojas
    de cristal (super_puerta) las pone world.js y se abren solas al llegar;
    encima, el cristal fijo. Carritos en fila a los lados."""
    D = 8.0
    y0 = -D / 2
    W = 30.0
    fachada = mat('fachada_super', 0xeceae4, 0.6)
    for s in (-1, 1):
        caja(fachada, s * (PUERTA + (W - PUERTA) / 2), y0 + 0.6, 0, W - PUERTA, 1.2, 13)
        caja(hierro(), s * PUERTA, y0 + 0.5, 0, 0.2, 0.3, 9.0)                    # el marco
        for k in range(4):                                                    # los escaparates
            x = s * (7.2 + k * 5.6)
            caja(vidrio(), x, y0 - 0.02, 0.6, 4.6, 0.1, 3.6)
            caja(hierro(), x, y0 - 0.06, 0.5, 4.8, 0.14, 0.12)
            c = (0xf2c230, 0xd8283a)[k % 2]
            caja(mat('cartel_esc_%x' % c, c, 0.5), x, y0 - 0.09, 1.5, 2.6, 0.04, 1.4)
            texto(rojo() if k % 2 == 0 else blanco(), ('+145%', 'SALE', '$999', 'TARIFFS')[k], x, y0 - 0.12, 2.0, tam=0.42, prof=0.02)
        for k in range(8):                                                    # carritos en fila
            caja(mat('carrito_fila', 0xb8bec6, 0.3), s * (5.0 + k * 0.6), y0 - 0.8, 0.3, 0.55, 0.9, 0.7)
        caja(fachada, s * W, y0 + 20, 0, 1.0, 40, 13)                         # el edificio sigue hacia atrás
    caja(mat('tejado_super', 0xb8bcc2, 0.8), 0, y0 + 20, 13, W * 2 + 1, 40, 0.3)
    # Encima de la puerta: el cristal fijo con sus montantes y, arriba, la fachada.
    caja(vidrio(), 0, y0 + 0.62, ALTO_PUERTA, PUERTA * 2, 0.1, 9.0 - ALTO_PUERTA)
    for x in (-1.9, 0.0, 1.9):
        caja(hierro(), x, y0 + 0.55, ALTO_PUERTA, 0.12, 0.16, 9.0 - ALTO_PUERTA)
    caja(hierro(), 0, y0 + 0.55, ALTO_PUERTA - 0.1, PUERTA * 2, 0.18, 0.22)
    caja(fachada, 0, y0 + 0.6, 9.0, PUERTA * 2, 1.2, 4.0)
    # La franja roja de arriba y el letrero.
    caja(rojo(), 0, y0 - 0.05, 11.7, W * 2, 0.3, 1.3)
    caja(rojo(), 0, y0 - 0.12, 9.2, 20.0, 0.3, 2.3)
    texto(blanco(), 'TARIFF MART', 0, y0 - 0.32, 9.9, tam=1.5, prof=0.08)
    # La marquesina con la pancarta de los precios.
    caja(rojo(), 0, y0 - 1.6, 4.5, 12.0, 3.2, 0.4)
    for s in (-1, 1):
        cil(hierro(), s * 5.6, y0 - 2.95, 0, 0.1, 4.5, 10)
    caja(mat('pancarta_precios', 0xf2c230, 0.5), 0, y0 - 3.24, 3.5, 8.6, 0.06, 1.0)
    texto(rojo(), 'NEW PRICES!', 0, y0 - 3.3, 3.95, tam=0.6, prof=0.03)
    # El umbral bajo la puerta y el vestíbulo (suelo, paredes y techo).
    caja(suelo_super(), 0, y0 + 0.6, 0, PUERTA * 2, 1.2, 0.09)
    caja(suelo_super(), 0, 0.6, 0, 9.2, D - 1.2, 0.09)
    for s in (-1, 1):
        caja(blanco(), s * 4.75, 0.6, 0, 0.3, D - 1.2, TECHO)
    caja(mat('techo_super', 0xe8eaee, 0.6), 0, 0.6, TECHO, 9.8, D - 1.2, 0.3)

def super_salida():
    """Las cajas registradoras y, al fondo, la pared de la salida con su
    puerta de cristal (las hojas, super_puerta, las pone world.js y se abren
    al llegar). Encima, «THANK YOU»."""
    D = 8.0
    caja(suelo_super(), 0, 0, 0, 9.2, D, 0.09)
    for s in (-1, 1):
        caja(blanco(), s * 4.75, 0, 0, 0.3, D, TECHO)
        caja(mat('caja_registradora', 0x2a2c31, 0.5), s * 4.0, -1.0, 0, 0.9, 2.4, 1.0)
        caja(mat('pantalla_caja', 0x6fd0ff, 0.3), s * 4.0, -1.0, 1.0, 0.3, 0.4, 0.35)
        caja(blanco(), s * 6.5, -D / 2 + 0.15, 0, 3.6, 0.3, TECHO)
        caja(blanco(), s * (PUERTA + (4.9 - PUERTA) / 2), D / 2 - 0.6, 0, 4.9 - PUERTA, 1.2, TECHO)
        caja(hierro(), s * PUERTA, D / 2 - 0.7, 0, 0.2, 0.3, 9.0)
    caja(mat('techo_super', 0xe8eaee, 0.6), 0, 0, TECHO, 9.8, D, 0.3)
    caja(vidrio(), 0, D / 2 - 0.62, ALTO_PUERTA, PUERTA * 2, 0.1, TECHO - ALTO_PUERTA)
    for x in (-1.9, 0.0, 1.9):
        caja(hierro(), x, D / 2 - 0.68, ALTO_PUERTA, 0.12, 0.16, TECHO - ALTO_PUERTA)
    caja(hierro(), 0, D / 2 - 0.68, ALTO_PUERTA - 0.1, PUERTA * 2, 0.18, 0.22)
    caja(rojo(), 0, D / 2 - 1.3, 6.2, 7.0, 0.3, 1.0)
    texto(blanco(), 'THANK YOU', 0, D / 2 - 1.48, 6.7, tam=0.5, prof=0.03)

def super_puerta():
    """Una hoja de la puerta automática: marco de aluminio, cristal, la barra
    y la pegatina. El origen, abajo en el centro."""
    alu = mat('aluminio_puerta', 0xaab0b8, 0.3)
    caja(mat('cristal_puerta', 0x8fb4cc, 0.12), 0, 0, 0.08, 1.8, 0.04, ALTO_PUERTA - 0.16)
    caja(alu, 0, 0, 0, 1.9, 0.07, 0.08)
    caja(alu, 0, 0, ALTO_PUERTA - 0.08, 1.9, 0.07, 0.08)
    for s in (-1, 1):
        caja(alu, s * 0.92, 0, 0, 0.06, 0.07, ALTO_PUERTA)
    caja(alu, 0, -0.05, 1.0, 1.4, 0.03, 0.05)
    caja(mat('pegatina_puerta', 0xf2c230, 0.5), 0, -0.03, 1.5, 0.5, 0.01, 0.2)

def etiqueta_precio():
    """La etiqueta de precio gigante colgada de un cable: «$999». Se pasa
    agachado (el juego la hace crecer al acercarse)."""
    caja(hierro(), 0, 0, 2.6, 2.0, 0.05, 0.05)
    rama(mat('cordel', 0xe8e0c8, 0.6), (0, 0, 2.6), (-0.45, 0, 2.15), 0.02, 0.02, 4)
    caja(mat('etiqueta', 0xfbf8ee, 0.5), 0, 0, 1.3, 1.7, 0.06, 0.9, giro=0.0)
    caja(rojo(), -0.62, 0, 1.75, 0.2, 0.07, 0.2)
    texto(rojo(), '$999', 0.12, -0.04, 1.75, tam=0.42, prof=0.02)
    texto(mat('letra_tachado', 0x2a2c31, 0.4), 'TARIFF', 0.12, -0.04, 1.42, tam=0.16, prof=0.015)

def carrito_compra():
    """Un carrito de la compra suelto que viene rodando hacia ti, lleno de
    productos. Se salta."""
    rejilla = mat('rejilla_carrito', 0xb8bec6, 0.25)
    for x in (-0.38, 0.38):
        caja(rejilla, x, 0.6, 0.35, 0.04, 0.95, 0.55)
    caja(rejilla, 0, 0.12, 0.35, 0.8, 0.04, 0.55)
    caja(rejilla, 0, 1.08, 0.35, 0.8, 0.04, 0.55)
    caja(rejilla, 0, 0.6, 0.33, 0.8, 0.95, 0.04)
    caja(rojo(), 0, -0.05, 0.92, 0.85, 0.08, 0.06)
    for x, y in ((-0.3, 0.2), (0.3, 0.2), (-0.3, 1.0), (0.3, 1.0)):
        cil(hierro(), x, y, 0.08, 0.08, 0.05, 10, eje='X')
    for k, col in enumerate((0xd8283a, 0x2a6ab8, 0xf2c230)):
        caja(mat('producto_%x' % col, col, 0.5), -0.2 + k * 0.2, 0.6, 0.45, 0.18, 0.4, 0.5)

def caja_precio():
    """Cajas de productos apiladas con la pegatina del precio nuevo: se saltan."""
    for (x, z, col) in ((-0.42, 0, 0x2a6ab8), (0.42, 0, 0xd8283a), (0.0, 0.42, 0xf2c230)):
        caja(mat('caja_prod_%x' % col, col, 0.6), x, 0.4, z, 0.8, 0.6, 0.42)
    cil(mat('pegatina_precio', 0xfbf8ee, 0.5), 0.1, 0.08, 0.62, 0.22, 0.02, 16, eje='Y')
    texto(rojo(), '+145%', 0.1, 0.06, 0.62, tam=0.1, prof=0.008)

def carro_clydesdale():
    """El carro de cerveza rojo tirado por dos caballos Clydesdale, visto por
    detrás: el carro con los barriles y, delante, los caballos (crines y patas
    blancas). Cambia de carril con el intermitente."""
    madera = mat('carro_rojo', 0xb8202a, 0.5)
    caja(madera, 0, 1.6, 0.6, 1.9, 3.0, 0.9)
    caja(mat('borde_oro', 0xe0b040, 0.3), 0, 1.6, 1.45, 1.95, 3.05, 0.08)
    for x in (-0.45, 0.45):
        for y in (0.9, 1.9):
            cil(mat('barril_carro', 0x8a5a34, 0.6), x, y, 1.5, 0.32, 0.8, 12)
    for s in (-1, 1):
        for y in (0.6, 2.6):
            cil(mat('rueda_carro', 0xd8c890, 0.6), s * 1.0, y, 0.55, 0.55, 0.1, 16, eje='X')
        caja(mat('piloto', 0xc0262c, 0.3), s * 0.7, 0.08, 0.75, 0.16, 0.03, 0.12)
        caja(mat('intermitente', 0xffa21a, 0.3), s * 0.7, 0.08, 0.95, 0.16, 0.03, 0.08)
    # Los caballos (08/11 (2): con forma de caballo y SIN patas: son la pieza
    # clydesdale_pata de animales.py, que el juego mueve al andar; las
    # caderas estan en world.js, ANDAR.carro_clydesdale).
    marron = mat_bloques('pelo_clyde', 0x5a3420, 0x5a3420, ancho=0.07, alto=0.12, grosor=0.0, desfase=0.37, variacion=1.09)
    crin = mat('crin_clyde', 0x2a1a10, 0.7)
    for x in (-0.45, 0.45):
        esfera(marron, x, 4.6, 1.62, 0.5, 3, esc=(0.75, 1.75, 0.85))
        esfera(marron, x, 5.15, 1.66, 0.38, 3)                             # el pecho
        esfera(marron, x, 4.05, 1.7, 0.4, 3)                               # la grupa
        rama(marron, (x, 5.32, 1.85), (x, 5.68, 2.42), 0.24, 0.15, 12)     # el cuello
        rama(crin, (x, 5.22, 2.0), (x, 5.58, 2.52), 0.07, 0.05, 6)
        rama(marron, (x, 5.72, 2.48), (x, 6.0, 2.12), 0.15, 0.11, 12)      # la cabeza
        esfera(blanco(), x, 6.02, 2.08, 0.11, 2)                           # el morro blanco
        for s in (-1, 1):
            rama(marron, (x + s * 0.07, 5.68, 2.55), (x + s * 0.09, 5.66, 2.7), 0.04, 0.008, 6)
            caja(mat('anteojera', 0x111111, 0.4), x + s * 0.15, 5.82, 2.3, 0.02, 0.13, 0.11)
        cil(mat('collera', 0x1d1f25, 0.4), x, 5.38, 1.95, 0.34, 0.13, 18, eje='Y')   # la collera
        cil(mat('borde_oro', 0xe0b040, 0.3), x, 5.32, 1.95, 0.36, 0.03, 18, eje='Y')
        rama(crin, (x, 3.72, 1.95), (x, 3.62, 1.35), 0.07, 0.04, 6)        # la cola
    caja(madera, 0, 3.4, 1.0, 0.1, 1.6, 0.1)

def fan_cardinals():
    """El aficionado de los Cardinals: camiseta roja, gorra con el pájaro y el
    dedo gigante de espuma. Cruza la calle (mira a +x)."""
    rojo_c = mat('rojo_cardinals', 0xc8202e, 0.5)
    piel = mat('piel_fanc', 0xe8b48c, 0.6)
    for sy in (-0.12, 0.12):
        cil(mat('pantalon_fanc', 0xe8e4dc, 0.6), 0, sy, 0, 0.1, 0.85, 8)
    caja(rojo_c, 0, 0, 0.85, 0.42, 0.52, 0.65)
    esfera(piel, 0, 0, 1.68, 0.2, 2)
    cil(rojo_c, 0, 0, 1.8, 0.21, 0.12, 12)
    caja(rojo_c, 0.18, 0, 1.82, 0.22, 0.3, 0.04)
    rama(rojo_c, (0, 0.28, 1.4), (0.15, 0.4, 1.95), 0.07, 0.06, 6)
    caja(mat('espuma', 0xf2c230, 0.6), 0.15, 0.42, 1.95, 0.12, 0.22, 0.5)
    caja(mat('espuma', 0xf2c230, 0.6), 0.15, 0.42, 2.45, 0.08, 0.08, 0.3)

PIEZAS = {
    'old_courthouse':     (old_courthouse,     'san_luis', dict(lado=1024, segmentos=2, min_bisel=1.0)),
    'busch_stadium':      (busch_stadium,      'san_luis', dict(lado=1024, segmentos=2, min_bisel=1.0)),
    'union_station_stl':  (union_station_stl,  'san_luis', dict(lado=1024, segmentos=2, min_bisel=1.0)),
    'arco_gateway':       (arco_gateway,       'san_luis', dict(lado=2048, segmentos=1, min_bisel=2.0)),
    'super_entrada':      (super_entrada,      'san_luis', dict(lado=2048, bisel=0.0)),
    'super_pasillo':      (super_pasillo,      'san_luis', dict(lado=2048, bisel=0.0, segmentos=2)),
    'super_puerta':       (super_puerta,       'san_luis', dict(lado=128, bisel=0.0, suelo=False)),
    'super_salida':       (super_salida,       'san_luis', dict(lado=512, bisel=0.0)),
    'etiqueta_precio':    (etiqueta_precio,    'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
    'carrito_compra':     (carrito_compra,     'obstaculos', dict(lado=256, bisel=0.0)),
    'caja_precio':        (caja_precio,        'obstaculos', dict(lado=256, bisel=0.0)),
    'carro_clydesdale':   (carro_clydesdale,   'obstaculos', dict(lado=512)),
    'fan_cardinals':      (fan_cardinals,      'obstaculos', dict(lado=256, bisel=0.0)),
}

correr(PIEZAS)
