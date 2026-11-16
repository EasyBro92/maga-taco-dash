# Nivel 46: Burlington, Vermont (16/11/2026).
#
#   blender -b -P blender/burlington.py -- [pieza ...] [--rapido]
#
# Historia: «Helados y un senador con guantes de lana que lo critica todo».
#   Acto del Sentido Común. Por Church Street en otoño: el ayuntamiento de
#   ladrillo con sus arcos, la heladería con manchas de vaca y el cucurucho en
#   el tejado, el granero rojo con su silo y, cruzando la calle, el puente
#   cubierto. En la acera, el senador gruñón sentado con sus manoplas y su
#   cartel ¡TODO MAL!. Los montones de hojas: saltando encima se rebota al
#   siguiente (en cadena); el momento estrella, el paseo sobre el lago
#   Champlain, donde asoma Champ, el monstruo del lago: hay que hacerle fotos.
#   Final en la iglesia de ladrillo de lo alto de Church Street.
#   Pancarta del Sentido Común: NADA ES GRATIS.
# Obstáculos (carpeta obstaculos): el montón de hojas, Champ, el camión de la
# leche, la garrafa de sirope de arce y la pancarta.

import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import *

def blanco():    return mat('blanco_btv', 0xf6f4ee, 0.5)
def negro():     return mat('negro_btv', 0x1c1c20, 0.4)
def cristal():   return mat('cristal_btv', 0x3a5a70, 0.15)
def rojo():      return mat('rojo_btv', 0xb8302a, 0.6)
def azul():      return mat('azul_btv', 0x1e4a9a, 0.45)
def amarillo():  return mat('amarillo_btv', 0xf2c21a, 0.45)
def rosa():      return mat('rosa_btv', 0xf08aa8, 0.5)
def verde():     return mat('verde_btv', 0x2a6a3a, 0.6)
def gris():      return mat('gris_btv', 0x8a9098, 0.4)
def madera():    return mat('madera_btv', 0x9a6a3e, 0.85)
def madera_o():  return mat('madera_oscura_btv', 0x5a3a22, 0.85)
def ladrillo():  return mat_bloques('ladrillo_btv', 0xa04a32, 0x7a3828, ancho=0.4, alto=0.16)
def piedra():    return mat_bloques('piedra_btv', 0xc8c0b0, 0xa8a090, ancho=1.0, alto=0.5, grosor=0.01)
def agua():      return mat('agua_btv', 0x3a6a8a, 0.12)
def roca():      return mat('roca_btv', 0x8a8478, 0.9)
def piel():      return mat('piel_btv', 0xf0c8a8, 0.6)
def bombilla():  return luz('bombilla_btv', 0xffe6a0, 1.2)
HOJAS = [lambda: mat('hoja_roja_btv', 0xc8302a, 0.8), lambda: mat('hoja_naranja_btv', 0xe8782a, 0.8),
         lambda: mat('hoja_amarilla_btv', 0xf2b82a, 0.8), lambda: mat('hoja_ocre_btv', 0xa8602a, 0.8)]

def cartel_sentido(x, y, z, w, h, linea1, linea2=''):
    caja(azul(), x, y, z, w, 0.06, h)
    caja(blanco(), x, y - 0.01, z + h - h * 0.08, w, 0.06, h * 0.08)
    esfera(rosa(), x - w / 2 + h * 0.32, y - 0.06, z + h * 0.5, h * 0.24, 1, esc=(1.2, 0.4, 1))
    texto(blanco(), linea1, x + h * 0.25, y - 0.045, z + h * (0.5 if not linea2 else 0.56), tam=h * 0.3, prof=0.02)
    if linea2:
        texto(amarillo(), linea2, x + h * 0.25, y - 0.045, z + h * 0.2, tam=h * 0.2, prof=0.02)

def arce(x, y, z=0, k=1.0):
    """Un arce en otoño: el tronco y la copa de bolas rojas y naranjas."""
    cil(madera_o(), x, y, z, 0.18 * k, 2.4 * k, 8, r2=0.12 * k)
    for i, (dx, dy, dz, r) in enumerate(((0, 0, 3.2, 1.3), (0.8, 0.2, 2.8, 0.9), (-0.8, -0.2, 2.9, 0.95), (0.1, 0.7, 3.6, 0.8), (-0.2, -0.6, 3.8, 0.7))):
        esfera(HOJAS[i % 4](), x + dx * k, y + dy * k, z + dz * k, r * k, 1, esc=(1, 1, 0.85))

# ================================================================ la meta
def iglesia_unitaria():
    """La iglesia unitaria de lo alto de Church Street (1816): ladrillo rojo,
    el pórtico de columnas blancas con su frontón y el campanario blanco de
    madera, con sus pisos y la aguja; delante, los maceteros de Church Street
    y la pancarta del Sentido Común."""
    Y = 24
    W, D, H = 20.0, 30.0, 12.0
    yf = Y - D / 2
    l = ladrillo()
    caja(piedra(), 0, Y - 12, -0.05, 90, 60, 0.06)
    caja(l, 0, Y, 0, W, D, H)
    tejado(mat('tejado_btv', 0x4a4a52, 0.6), 0, Y - D / 2, Y + D / 2, H, W + 0.6, 4.5, cumbrera='y')
    hastial(l, 0, Y - D / 2, Y + D / 2, H, W, 4.5, cumbrera='y')
    for k in range(4):
        y = Y - 10 + k * 7
        for s in (-1, 1):
            caja(cristal(), s * (W / 2 + 0.05), y, 3.0, 0.1, 2.2, 6.0)
    caja(blanco(), 0, yf - 3, 0, 14, 6, 0.6)
    for x in (-5.4, -1.8, 1.8, 5.4):
        cil(blanco(), x, yf - 5.4, 0.6, 0.45, 9.0, 12)
    caja(blanco(), 0, yf - 3, 9.6, 14.4, 6.4, 1.0)
    fronton(blanco(), 0, yf - 6.2, 10.6, 14.4, 3.2, 0.8)
    puerta(0, 0.6, 2.6, 4.2, y=yf - 6.2)
    # el campanario
    caja(l, 0, yf + 3, 0, 6, 6, H + 5)
    caja(blanco(), 0, yf + 3, H + 5, 6.4, 6.4, 0.6)
    caja(blanco(), 0, yf + 3, H + 5.6, 5.2, 5.2, 5)
    for s in (-1, 1):
        caja(negro(), s * 2.62, yf + 3, H + 6.6, 0.1, 2.2, 3.0)
        caja(negro(), 0, yf + 3 + s * 2.62, H + 6.6, 2.2, 0.1, 3.0)
    caja(blanco(), 0, yf + 3, H + 10.6, 5.6, 5.6, 0.5)
    cil(blanco(), 0, yf + 3, H + 11.1, 2.2, 4.0, 8)
    for k in range(8):
        a = k * math.tau / 8
        cil(blanco(), math.cos(a) * 2.3, yf + 3 + math.sin(a) * 2.3, H + 11.1, 0.15, 4.0, 6)
    cil(blanco(), 0, yf + 3, H + 15.1, 2.4, 0.5, 8)
    cil(blanco(), 0, yf + 3, H + 15.6, 1.8, 11, 8, r2=0.05)
    esfera(mat('oro_btv', 0xe8b840, 0.22), 0, yf + 3, H + 26.8, 0.3, 1)
    # Church Street: maceteros con flores y la pancarta
    for x in (-8, 8):
        for y in (yf - 12, yf - 20):
            caja(madera(), x, y, 0, 1.6, 1.6, 0.7)
            for i in range(3):
                esfera(HOJAS[i](), x - 0.4 + i * 0.4, y, 0.85, 0.35, 1)
    for x in (8, 22):
        cil(madera_o(), x, yf - 16, 0, 0.12, 4.4, 8)
    cartel_sentido(15, yf - 16, 2.8, 14, 1.6, 'NADA ES GRATIS', 'EL SENTIDO COMÚN')

# ================================================================ edificios
def ayuntamiento_btv():
    """El ayuntamiento de Burlington (1928): ladrillo rojo de tres pisos, los
    tres arcos blancos de la entrada, la cornisa y el mástil."""
    Y = 9
    W, D, H = 26.0, 16.0, 14.0
    yf = Y - D / 2
    l = ladrillo()
    caja(l, 0, Y, 0, W, D, H)
    caja(blanco(), 0, Y, H, W + 0.6, D + 0.6, 0.8)
    for k in range(3):
        x = -5 + k * 5
        caja(blanco(), x, yf - 0.2, 0, 4.2, 0.5, 6.0)
        caja(cristal(), x, yf - 0.5, 0, 2.8, 0.1, 4.2)
        cil(cristal(), x, yf - 0.5, 4.2, 1.4, 0.1, 16, eje='Y')
    for k in range(6):
        x = -11 + k * 4.4
        for z in (7.5, 10.5):
            ventana(x, z, 1.6, 2.2, y=yf - 0.05, marco=blanco(), cristal=cristal())
    caja(blanco(), 0, yf - 0.3, 6.4, 12, 0.3, 0.9)
    texto(negro(), 'CITY HALL', 0, yf - 0.48, 6.55, tam=0.6, prof=0.03)
    cil(blanco(), 0, Y, H + 0.8, 0.08, 7, 8)
    caja(azul(), 0.9, Y, H + 6.2, 1.6, 0.04, 1.0)

def heladeria_vaca():
    """La heladería (Vermont: helados y vacas): la casita blanca con manchas
    negras de vaca, el toldo, el cucurucho gigante de tres bolas en el tejado
    y el cartel CONO GRATIS* (*mañana)."""
    Y = 7
    W, D, H = 12.0, 10.0, 6.0
    yf = Y - D / 2
    caja(blanco(), 0, Y, 0, W, D, H)
    n = negro()
    for (x, z, r) in ((-4, 4, 0.9), (-1.5, 1.5, 0.7), (2.5, 4.5, 1.0), (4.6, 1.8, 0.6), (0.8, 3.2, 0.5)):
        esfera(n, x, yf - 0.02, z, r, 1, esc=(1.3, 0.06, 0.9))
    for (y, z, r) in ((Y - 2, 3.5, 0.9), (Y + 2.5, 2.0, 0.8)):
        for s in (-1, 1):
            esfera(n, s * (W / 2 + 0.02), y, z, r, 1, esc=(0.06, 1.3, 0.9))
    caja(mat_franjas('toldo_helado_btv', 0xf08aa8, 0xf6f4ee, 10, eje='X', z0=-W / 2, alto=W), 0, yf - 1.2, 3.2, W, 2.4, 0.15, inclina=-0.25)
    caja(cristal(), 0, yf - 0.05, 0.4, 7, 0.1, 2.6)
    caja(blanco(), 0, Y, H, W + 0.4, D + 0.4, 0.4)
    cil(mat('barquillo_btv', 0xd8a050, 0.7), 0, Y, H + 0.4, 0.2, 4.5, 16, r2=1.4)
    for i, (c, dz) in enumerate(((0xf6e8c8, 5.3), (0x7a4a2a, 6.6), (0xf08aa8, 7.8))):
        esfera(mat(f'bola_btv_{i}', c, 0.6), 0, Y, H + dz, 1.35 - i * 0.12, 2)
    caja(blanco(), 0, yf - 0.1, 4.6, 7.5, 0.1, 1.2)
    texto(negro(), 'HELADOS DE VERMONT', 0, yf - 0.16, 4.9, tam=0.42, prof=0.02)
    caja(amarillo(), 4.6, yf - 0.8, 0, 1.6, 0.1, 1.6)
    texto(rojo(), 'CONO', 4.6, yf - 0.86, 1.05, tam=0.28, prof=0.02)
    texto(rojo(), 'GRATIS*', 4.6, yf - 0.86, 0.7, tam=0.24, prof=0.02)
    texto(negro(), '*mañana', 4.6, yf - 0.86, 0.35, tam=0.14, prof=0.02)

def granero_rojo():
    """El granero rojo de Vermont con el tejado a dos aguas quebrado, las
    puertas blancas en X y el silo con su cúpula."""
    Y = 10
    W, D, H = 14.0, 18.0, 6.0
    yf = Y - D / 2
    r = mat('rojo_granero_btv', 0xa8302a, 0.75)
    caja(r, 0, Y, 0, W, D, H)
    t = mat('tejado_granero_btv', 0x4a4a52, 0.6)
    ya, yb = Y - D / 2 - 0.3, Y + D / 2 + 0.3
    perfil = [(-W / 2 - 0.3, H - 0.2), (-W * 0.3, H + 2.8), (0, H + 4.0), (W * 0.3, H + 2.8), (W / 2 + 0.3, H - 0.2)]
    for (x0, z0), (x1, z1) in zip(perfil, perfil[1:]):
        panel(t, (x0, ya, z0), (x1, ya, z1), (x1, yb, z1), (x0, yb, z0), 0.12)
    def alto_techo(x):
        for (x0, z0), (x1, z1) in zip(perfil, perfil[1:]):
            if x0 <= x <= x1:
                return z0 + (z1 - z0) * (x - x0) / (x1 - x0)
        return H
    for yy in (Y - D / 2 + 0.15, Y + D / 2 - 0.15):
        for k in range(14):
            xc = -W / 2 + (k + 0.5) * W / 14
            h = alto_techo(xc) - H - 0.1
            if h > 0.1:
                caja(r, xc, yy, H, W / 14 + 0.02, 0.3, h)
    caja(blanco(), 0, yf - 0.05, 0, 5.0, 0.12, 4.4)
    for s in (-1, 1):
        rama(blanco(), (s * -2.4, yf - 0.12, 0.2), (s * 2.4, yf - 0.12, 4.2), 0.12, 0.12, 4)
    caja(r, 0, yf - 0.02, 0, 4.6, 0.1, 4.2)
    cil(blanco(), 0, yf - 0.1, H + 2.5, 0.6, 0.1, 12, eje='Y')
    cil(mat('silo_btv', 0x9aa0a8, 0.4), W / 2 + 3, Y + 3, 0, 2.6, 13, 20)
    cupula(mat('silo_btv', 0x9aa0a8, 0.4), W / 2 + 3, Y + 3, 13, 2.6, 2, 20, 6)
    for k in range(4):
        cil(gris(), W / 2 + 3, Y + 3, 1 + k * 3, 2.65, 0.15, 20)
    arce(-W / 2 - 3, Y - 4)

def arce_cubo():
    """Un arce de la acera con el cubo de savia colgado del tronco."""
    arce(0, 0, 0, 0.8)
    cil(gris(), 0, -0.2, 1.0, 0.16, 0.3, 12)
    cil(gris(), 0, -0.1, 1.3, 0.03, 0.18, 6, eje='Y')

def senador_manoplas():
    """El senador gruñón (sin nombre): sentado en la silla plegable con las
    piernas cruzadas, el anorak marrón, los brazos cruzados con sus manoplas
    de lana de colores, las gafas, el pelo blanco revuelto y, al lado, su
    cartel ¡TODO MAL!. Mira a -y (al jugador)."""
    hi = mat('silla_btv', 0x2a2c30, 0.45)
    for s in (-1, 1):
        rama(hi, (s * 0.3, -0.3, 0), (s * 0.3, 0.3, 0.55), 0.03, 0.03, 6)
        rama(hi, (s * 0.3, 0.3, 0), (s * 0.3, -0.3, 0.55), 0.03, 0.03, 6)
    caja(mat('lona_btv', 0x3a5a3a, 0.8), 0, 0, 0.5, 0.65, 0.6, 0.06)
    caja(mat('lona_btv', 0x3a5a3a, 0.8), 0, 0.3, 0.55, 0.65, 0.06, 0.6)
    an = mat('anorak_btv', 0x7a5a3a, 0.85)
    esfera(an, 0, 0.05, 0.95, 0.38, 2, esc=(1.1, 0.8, 1.25))
    pa = mat('pantalon_btv', 0x4a4a52, 0.8)
    rama(pa, (-0.15, -0.05, 0.6), (-0.15, -0.45, 0.62), 0.11, 0.1, 8)
    rama(pa, (-0.15, -0.45, 0.62), (-0.15, -0.5, 0.1), 0.1, 0.09, 8)
    rama(pa, (0.15, -0.05, 0.6), (-0.05, -0.45, 0.72), 0.11, 0.1, 8)
    rama(pa, (-0.05, -0.45, 0.72), (0.15, -0.65, 0.5), 0.1, 0.09, 8)
    for (x, y, z) in ((-0.15, -0.55, 0.05), (0.18, -0.72, 0.45)):
        esfera(negro(), x, y, z, 0.1, 1, esc=(0.9, 1.6, 0.7))
    rama(an, (-0.35, -0.05, 1.15), (0.2, -0.32, 0.95), 0.1, 0.1, 8)
    rama(an, (0.35, -0.05, 1.15), (-0.2, -0.36, 1.02), 0.1, 0.1, 8)
    ma = mat_franjas('manopla_btv', 0xe8e0d0, 0x7a3a5a, 6, eje='Z', z0=0.8, alto=0.4)
    for (x, z) in ((0.27, 0.95), (-0.27, 1.02)):
        esfera(ma, x, -0.36, z, 0.15, 2, esc=(1.1, 0.9, 1.2))
    esfera(piel(), 0, 0.0, 1.55, 0.2, 2, esc=(0.95, 0.95, 1.1))
    for s in (-1, 1):
        esfera(mat('pelo_btv', 0xf0f0ec, 0.9), s * 0.16, 0.05, 1.62, 0.09, 1)
        cil(negro(), s * 0.07, -0.19, 1.58, 0.05, 0.02, 10, eje='Y')
    caja(negro(), 0, -0.19, 1.58, 0.06, 0.02, 0.015)
    esfera(mat('pelo_btv', 0xf0f0ec, 0.9), 0, 0.08, 1.72, 0.12, 1, esc=(1.3, 1, 0.6))
    caja(negro(), 0, -0.19, 1.45, 0.1, 0.02, 0.02)
    cil(madera_o(), 0.7, 0.05, 0, 0.03, 1.6, 6)
    caja(blanco(), 0.7, 0.03, 1.3, 0.7, 0.04, 0.45)
    texto(rojo(), '¡TODO MAL!', 0.7, 0.0, 1.47, tam=0.13, prof=0.01)

# ================================================================ cruza la calle
def puente_cubierto():
    """El puente cubierto de madera roja (los de Vermont) que cruza la calle:
    las dos paredes de tablas con ventanucos, el tejado a dos aguas y las
    bocas con el remate blanco y su cartel."""
    r = mat('rojo_puente_btv', 0xa8302a, 0.8)
    L = 12.0
    for s in (-1, 1):
        caja(r, s * 10.4, 0, 0, 0.4, L, 5.6)
        for y in (-3, 3):
            caja(negro(), s * 10.18, y, 3.0, 0.05, 1.2, 0.9)
    tejado(mat('tejado_puente_btv', 0x4a4a52, 0.6), 0, -L / 2 - 0.4, L / 2 + 0.4, 5.6, 21.8, 3.4, cumbrera='y')
    for y in (-L / 2, L / 2):
        caja(r, 0, y, 5.6, 21, 0.3, 0.6)
        for k in range(20):
            u = (k + 0.5) / 20
            x = -10.5 + 21 * u
            h = 3.4 * (1 - abs(x) / 10.9)
            caja(r, x, y, 6.2, 1.05, 0.3, max(0.1, h - 0.6))
        caja(blanco(), 0, y - (0.2 if y < 0 else -0.2), 5.55, 21.2, 0.1, 0.2)
    caja(blanco(), 0, -L / 2 - 0.18, 6.6, 7, 0.1, 1.0)
    texto(negro(), 'PUENTE CUBIERTO · 1865', 0, -L / 2 - 0.24, 6.85, tam=0.5, prof=0.02)
    for k in range(6):
        caja(madera_o(), 0, -L / 2 + 1 + k * 2, 5.5, 20.4, 0.25, 0.25)

# ================================================================ el lago
def causeway_champlain():
    """El paseo sobre el lago Champlain (momento estrella): el camino de
    grava (la calle) con las orillas de rocas, el agua a los dos lados hasta
    lejos, los bancos, los carteles y las boyas. Cruza la calle: el origen
    en el centro."""
    L = 420
    a = agua()
    # (el suelo: en los tramos de dentro el juego quita su calle)
    caja(mat_bloques('grava_btv', 0xb8ae98, 0xa09680, ancho=0.5, alto=0.5, grosor=0.03), 0, 0, -0.2, 17, L, 0.2)
    for s in (-1, 1):
        caja(a, s * 50, 0, 0.1, 80, L, 0.04)
        for k in range(int(L / 1.6)):
            y = -L / 2 + 0.8 + k * 1.6
            h = 0.3 + ((k * 37) % 7) * 0.06
            caja(roca(), s * (8.0 + ((k * 13) % 5) * 0.25), y, -0.1, 1.4, 1.5, h, giro=((k * 29) % 9) * 0.2)
        for k in range(int(L / 60)):
            y = -L / 2 + 30 + k * 60 + s * 12
            caja(madera(), s * 6.6, y, 0.45, 0.5, 2.0, 0.08)
            caja(madera(), s * 6.85, y, 0.5, 0.08, 2.0, 0.5)
            for dy in (-0.8, 0.8):
                caja(hierro_m(), s * 6.6, y + dy, 0, 0.08, 0.08, 0.45)
        for k in range(int(L / 45)):
            y = -L / 2 + 20 + k * 45 + s * 9
            x = s * (20 + (k * 17) % 25)
            cil(mat('boya_btv', 0xf2f0e8, 0.5), x, y, 0.0, 0.35, 1.0, 10)
            cil(rojo(), x, y, 0.7, 0.36, 0.25, 10)
    for y in (-L / 2 + 6, L / 2 - 30):
        cil(madera_o(), -7.0, y, 0, 0.1, 2.6, 8)
        caja(verde(), -7.0, y - 0.1, 1.9, 2.4, 0.08, 0.7)
        texto(blanco(), 'ISLAND LINE', -7.0, y - 0.15, 2.05, tam=0.3, prof=0.02)

def hierro_m():  return mat('hierro_btv', 0x2a2c30, 0.45)

# ================================================================ obstáculos
def monton_hojas():
    """El montón de hojas de otoño (se salta ENCIMA para rebotar): bolas
    aplastadas rojas, naranjas y amarillas y hojas sueltas por encima."""
    for i, (x, y, z, r) in enumerate(((0, 0, 0.0, 1.1), (-0.6, 0.6, 0.0, 0.8), (0.6, -0.6, 0.0, 0.85), (0.5, 0.8, 0.0, 0.7),
                                      (-0.6, -0.8, 0.0, 0.7), (0.1, 0.1, 0.35, 0.8), (-0.3, -0.2, 0.55, 0.5))):
        esfera(HOJAS[i % 4](), x, y, z, r, 2, esc=(1.1, 1.3, 0.75))
    for k in range(14):
        a = k * 2.4
        rr = 0.3 + (k % 5) * 0.2
        caja(HOJAS[k % 4](), math.cos(a) * rr, math.sin(a) * rr * 1.2, 0.75 + (k % 3) * 0.08, 0.25, 0.2, 0.02, giro=a)

def champ():
    """Champ, el monstruo del lago Champlain (asoma del agua): el cuello
    largo verde, la cabeza simpática con los ojos grandes y dos jorobas
    detrás. El origen en el agua; mira a -y."""
    v = mat('champ_btv', 0x3a8a5a, 0.55)
    vc = mat('champ_claro_btv', 0x9ad0a0, 0.6)
    n = 10
    pts = [(0, 0.4 * math.sin(u * 1.4), -0.6 + 4.6 * u) for u in [k / n for k in range(n + 1)]]
    for k in range(n):
        rama(v, pts[k], pts[k + 1], 0.75 - 0.4 * k / n, 0.75 - 0.4 * (k + 1) / n, 10)
    hx, hy, hz = 0, 0.2, 4.2
    esfera(v, hx, hy - 0.3, hz, 0.6, 2, esc=(1, 1.5, 0.8))
    esfera(vc, hx, hy - 0.85, hz - 0.15, 0.4, 2, esc=(1, 1.2, 0.6))
    for s in (-1, 1):
        esfera(blanco(), hx + s * 0.32, hy - 0.55, hz + 0.25, 0.18, 2)
        esfera(negro(), hx + s * 0.34, hy - 0.68, hz + 0.27, 0.08, 1)
        esfera(v, hx + s * 0.3, hy - 0.1, hz + 0.55, 0.1, 1)
    esfera(vc, 0, -0.4, 1.6, 0.6, 1, esc=(1, 0.5, 1.6))
    for (y, r) in ((2.6, 1.1), (5.0, 0.8)):
        esfera(v, 0, y, -0.2, r, 2, esc=(0.8, 1.4, 1))
    rama(v, (0, 5.8, -0.2), (0, 7.4, 0.3), 0.35, 0.05, 8)

def camion_leche():
    """El camión de la leche (no se pasa): la cabina roja y la cisterna
    blanca con manchas de vaca y LECHE DE VERMONT. El morro en el origen."""
    r = rojo()
    caja(r, 0, 1.0, 0.45, 2.3, 2.0, 1.9)
    caja(cristal(), 0, -0.02, 1.5, 2.0, 0.1, 0.7)
    o = cil(blanco(), 0, 4.8, 1.55, 1.15, 5.0, 20, eje='Y')
    n = negro()
    for (y, z, sx) in ((3.4, 2.1, 1), (5.2, 1.3, -1), (6.4, 2.2, 1), (4.4, 1.0, 1)):
        esfera(n, sx * 1.12, y, z, 0.4, 1, esc=(0.08, 1.4, 0.9))
    for s in (-1, 1):
        texto(azul(), 'LECHE DE VERMONT', s * 1.17, 4.8, 1.5, tam=0.26, prof=0.01).rotation_euler = (math.pi / 2, 0, -s * math.pi / 2)
    caja(gris(), 0, 4.8, 0.35, 2.0, 5.4, 0.2)
    for (y, s) in ((1.0, 1), (3.6, 1), (6.2, 1), (1.0, -1), (3.6, -1), (6.2, -1)):
        cil(negro(), s * 1.1, y, 0.45, 0.45, 0.3, 14, eje='X')
    for s in (-1, 1):
        caja(luz('faro_leche_btv', 0xfff2c0, 1.0), s * 0.8, -0.03, 0.85, 0.35, 0.05, 0.2)

def garrafa_arce():
    """La garrafa de sirope de arce volcada (se salta): la jarra de plástico
    con el asa, la etiqueta con la hoja de arce y el charco de sirope."""
    g = mat('garrafa_btv', 0xc87a2a, 0.3)
    o = cil(g, 0, 0, 0.42, 0.42, 1.0, 16, eje='X')
    cil(blanco(), 0.0, 0, 0.42, 0.43, 0.5, 16, eje='X')
    esfera(rojo(), 0.0, -0.44, 0.45, 0.13, 1, esc=(1, 0.2, 1))
    cil(g, 0.62, 0, 0.42, 0.14, 0.25, 10, eje='X')
    rama(g, (-0.2, 0.0, 0.84), (0.3, 0.0, 0.84), 0.06, 0.06, 6)
    esfera(mat('sirope_btv', 0x8a4a12, 0.1), 0.95, 0.1, 0.01, 0.5, 1, esc=(1.4, 1, 0.05))

def cartel_vt():
    """La pancarta del Sentido Común (agacharse): NADA ES GRATIS."""
    for x in (-1.25, 1.25):
        cil(madera_o(), x, 0, 0, 0.07, 2.75, 8)
    caja(azul(), 0, 0, 1.5, 2.4, 0.05, 1.2)
    esfera(rosa(), -0.9, -0.05, 2.1, 0.2, 1, esc=(1.2, 0.4, 1))
    texto(blanco(), 'NADA ES', 0.15, -0.035, 2.2, tam=0.24, prof=0.02)
    texto(amarillo(), 'GRATIS', 0.15, -0.035, 1.8, tam=0.24, prof=0.02)

PIEZAS = {
    'iglesia_unitaria':   (iglesia_unitaria,   'burlington', dict(lado=2048, bisel=0.0)),
    'ayuntamiento_btv':   (ayuntamiento_btv,   'burlington', dict(lado=1024, bisel=0.0)),
    'heladeria_vaca':     (heladeria_vaca,     'burlington', dict(lado=1024, bisel=0.0)),
    'granero_rojo':       (granero_rojo,       'burlington', dict(lado=1024, bisel=0.0)),
    'arce_cubo':          (arce_cubo,          'burlington', dict(lado=256, bisel=0.0)),
    'senador_manoplas':   (senador_manoplas,   'burlington', dict(lado=512, bisel=0.0)),
    'puente_cubierto':    (puente_cubierto,    'burlington', dict(lado=1024, bisel=0.0, suelo=False)),
    'causeway_champlain': (causeway_champlain, 'burlington', dict(lado=2048, bisel=0.0, suelo=False)),
    'monton_hojas':       (monton_hojas,       'obstaculos', dict(lado=256, bisel=0.0)),
    'champ':              (champ,              'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
    'camion_leche':       (camion_leche,       'obstaculos', dict(lado=256, bisel=0.0)),
    'garrafa_arce':       (garrafa_arce,       'obstaculos', dict(lado=256, bisel=0.0)),
    'cartel_vt':          (cartel_vt,          'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
}

correr(PIEZAS)
