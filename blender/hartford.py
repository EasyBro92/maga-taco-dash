# Nivel 45: Hartford, Connecticut (15/11/2026).
#
#   blender -b -P blender/hartford.py -- [pieza ...] [--rapido]
#
# Historia: «La capital de los seguros: ninguno le cubre los tropezones». Acto
#   del Sentido Común. Por Main Street: la torre de los seguros con su faro, la
#   casa de Mark Twain (ladrillo de dibujos, torrecillas), el antiguo Capitolio
#   con el águila y, cruzando la calle, el arco de los soldados del parque
#   Bushnell. La valla de Tom Sawyer: por los carriles de las orillas se pinta
#   la valla de blanco (como en el libro, la pinta otro… menos hoy); el momento
#   estrella, el tiovivo del parque Bushnell (montado en el caballito, que sube
#   y baja, hay que tocar cuando está a la altura de la anilla dorada para
#   cogerla). Final en el Capitolio de Connecticut, con su cúpula de oro.
#   Pancarta del Sentido Común: LEE LA LETRA PEQUEÑA.
# Obstáculos (carpeta obstaculos): el caballito del tiovivo (se monta: es un
# vehículo), el trozo de valla que se pinta, el cubo de pintura volcado, la
# furgoneta de los seguros y la pancarta.

import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import *

def blanco():    return mat('blanco_hfd', 0xf6f4ee, 0.5)
def negro():     return mat('negro_hfd', 0x1c1c20, 0.4)
def cristal():   return mat('cristal_hfd', 0x3a5a70, 0.15)
def rojo():      return mat('rojo_hfd', 0xc8202a, 0.45)
def azul():      return mat('azul_hfd', 0x1e4a9a, 0.45)
def amarillo():  return mat('amarillo_hfd', 0xf2c21a, 0.45)
def oro():       return mat('oro_hfd', 0xe8b840, 0.22)
def rosa():      return mat('rosa_hfd', 0xf08aa8, 0.5)
def gris():      return mat('gris_hfd', 0x8a9098, 0.4)
def hierro():    return mat('hierro_hfd', 0x2a2c30, 0.45)
def madera():    return mat('madera_hfd', 0x9a6a3e, 0.85)
def madera_o():  return mat('madera_oscura_hfd', 0x5a3a22, 0.85)
def marmol():    return mat_bloques('marmol_hfd', 0xf0ece4, 0xd8d2c8, ancho=1.2, alto=0.6, grosor=0.006)
def marmol_l():  return mat('marmol_liso_hfd', 0xf4f0e8, 0.45)
def piedra_p():  return mat_bloques('piedra_parda_hfd', 0x8a5a3e, 0x6a4430, ancho=0.9, alto=0.5, grosor=0.01)
def ladrillo():  return mat_bloques('ladrillo_hfd', 0xa85a3e, 0x7a4030, ancho=0.4, alto=0.16)
def granito():   return mat_bloques('granito_hfd', 0xb8b4aa, 0x9a968c, ancho=1.2, alto=0.6, grosor=0.008)
def cesped():    return mat('cesped_hfd', 0x5a9a3a, 0.9)
def bombilla():  return luz('bombilla_hfd', 0xffe6a0, 1.2)

def cartel_sentido(x, y, z, w, h, linea1, linea2=''):
    caja(azul(), x, y, z, w, 0.06, h)
    caja(blanco(), x, y - 0.01, z + h - h * 0.08, w, 0.06, h * 0.08)
    esfera(rosa(), x - w / 2 + h * 0.32, y - 0.06, z + h * 0.5, h * 0.24, 1, esc=(1.2, 0.4, 1))
    texto(blanco(), linea1, x + h * 0.25, y - 0.045, z + h * (0.5 if not linea2 else 0.56), tam=h * 0.3, prof=0.02)
    if linea2:
        texto(amarillo(), linea2, x + h * 0.25, y - 0.045, z + h * 0.2, tam=h * 0.2, prof=0.02)

def ventana_ojiva(x, z, w, h, y, marco):
    caja(cristal(), x, y, z, w, 0.1, h)
    o = cil(cristal(), x, y, z + h, w / 2, 0.1, 3, eje='Y')
    o.scale = (1, 1, 1.4)
    caja(marco, x, y - 0.03, z - 0.15, w + 0.3, 0.1, 0.15)

def caballito_m(x, y, z, k=1.0, col=None):
    """Un caballito de tiovivo (de lado, mirando a -y): el cuerpo blanco con
    la silla de colores, las patas dobladas y la crin dorada."""
    b = blanco()
    esfera(b, x, y, z + 1.2 * k, 0.5 * k, 2, esc=(0.6, 1.5, 0.75))
    rama(b, (x, y - 0.6 * k, z + 1.35 * k), (x, y - 0.9 * k, z + 1.85 * k), 0.2 * k, 0.15 * k, 8)
    esfera(b, x, y - 1.05 * k, z + 1.95 * k, 0.2 * k, 2, esc=(0.7, 1.4, 0.8))
    rama(oro(), (x, y - 0.75 * k, z + 1.95 * k), (x, y - 0.3 * k, z + 1.5 * k), 0.08 * k, 0.05 * k, 6)
    caja((col or rojo)(), x, y, z + 1.55 * k, 0.6 * k, 0.6 * k, 0.12 * k)
    for (dy, dz) in ((-0.5, -0.1), (0.5, 0.1)):
        for s in (-1, 1):
            rama(b, (x + s * 0.15 * k, y + dy * k, z + 1.0 * k), (x + s * 0.15 * k, y + (dy - 0.25) * k, z + (0.55 + dz) * k), 0.07 * k, 0.05 * k, 6)
    rama(oro(), (x, y + 0.7 * k, z + 1.2 * k), (x, y + 1.0 * k, z + 0.8 * k), 0.08 * k, 0.03 * k, 6)

# ================================================================ la meta
def capitolio_ct():
    """El Capitolio de Connecticut (la meta): gótico victoriano de mármol
    blanco, las ventanas en ojiva, las torrecillas de las esquinas con sus
    tejados, el tambor alto y la cúpula de pan de oro con nervios; delante, el
    césped del parque Bushnell y la pancarta del Sentido Común."""
    Y = 26
    W, D, H = 54.0, 26.0, 18.0
    yf = Y - D / 2
    m = marmol()
    caja(cesped(), 0, Y - 10, -0.05, 100, 64, 0.06)
    caja(m, 0, Y, 0, W, D, H)
    caja(marmol_l(), 0, Y, H, W + 0.6, D + 0.6, 1.0)
    for k in range(11):
        x = -24 + k * 4.8
        for z in (2.0, 8.5):
            ventana_ojiva(x, z, 1.6, 3.2, yf - 0.05, marmol_l())
    for (x, y) in ((-26, yf), (26, yf), (-26, Y + 12), (26, Y + 12)):
        caja(m, x, y, 0, 6, 6, H + 6)
        o = cil(mat('tejado_ct_hfd', 0x4a6a6a, 0.5), x, y, H + 6, 4.2, 7, 4, r2=0.2)
        o.rotation_euler = (0, 0, math.pi / 4)
    caja(m, 0, yf - 3, 0, 18, 6, 12)
    for x in (-6, -2, 2, 6):
        ventana_ojiva(x, 1.0, 2.2, 5.0, yf - 6.05, marmol_l())
    Z = H + 1.0
    cil(m, 0, Y, Z, 9.5, 6, 24)
    for k in range(12):
        a = k * math.tau / 12
        ventana_ojiva(math.cos(a) * 9.6, Z + 1.0, 1.2, 2.8, Y + math.sin(a) * 9.6, marmol_l())
    cil(m, 0, Y, Z + 6, 8.4, 8, 24)
    for k in range(16):
        a = k * math.tau / 16
        cil(marmol_l(), math.cos(a) * 8.6, Y + math.sin(a) * 8.6, Z + 6, 0.3, 8, 8)
    cil(marmol_l(), 0, Y, Z + 14, 9.0, 1.0, 24)
    cupula(oro(), 0, Y, Z + 15, 8.0, 12, 24, 10)
    for k in range(12):
        a = k * math.tau / 12
        rama(mat('nervio_ct_hfd', 0xc8982a, 0.3), (math.cos(a) * 8, Y + math.sin(a) * 8, Z + 15.1), (math.cos(a) * 1.5, Y + math.sin(a) * 1.5, Z + 26.6), 0.15, 0.08, 4)
    cil(oro(), 0, Y, Z + 27, 1.4, 3, 12, r2=0.3)
    esfera(oro(), 0, Y, Z + 30.5, 0.6, 1)
    for x in (8, 22):
        cil(madera_o(), x, yf - 16, 0, 0.12, 4.4, 8)
    cartel_sentido(15, yf - 16, 2.8, 14, 1.6, 'LEE LA LETRA PEQUEÑA', 'EL SENTIDO COMÚN')

# ================================================================ edificios
def torre_seguros():
    """La torre de los seguros (1919): la torre alta de granito con el
    tejado de pirámide y el faro arriba (la capital de los seguros)."""
    Y = 10
    g = granito()
    caja(g, 0, Y, 0, 22, 18, 14)
    caja(g, 0, Y, 14, 12, 12, 36)
    for z in range(16, 48, 3):
        for x in (-3.6, -1.2, 1.2, 3.6):
            caja(cristal(), x, Y - 6.05, z, 1.2, 0.1, 1.8)
    caja(marmol_l(), 0, Y, 50, 13, 13, 1)
    o = cil(mat('piramide_seg_hfd', 0x6a7a7a, 0.4), 0, Y, 51, 8.5, 9, 4, r2=1.0)
    o.rotation_euler = (0, 0, math.pi / 4)
    cil(cristal(), 0, Y, 60, 1.2, 2.4, 12)
    esfera(luz('faro_seg_hfd', 0xfff0c0, 1.3), 0, Y, 61.2, 0.8, 1)
    caja(blanco(), 0, Y - 9.05, 4.2, 12, 0.1, 1.4)
    texto(azul(), 'SEGUROS DE TODO', 0, Y - 9.1, 4.5, tam=0.75, prof=0.03)
    texto(negro(), '(menos tropezones)', 0, Y - 9.1, 3.6, tam=0.4, prof=0.02)

def casa_mark_twain():
    """La casa de Mark Twain (1874): gótico victoriano de ladrillo con
    dibujos rojos y negros, porches de madera, torrecillas y chimeneas."""
    Y = 9
    W, D = 22.0, 14.0
    yf = Y - D / 2
    l = mat_franjas('ladrillo_twain_hfd', 0xb8603e, 0x2a2a30, 14, eje='Z', z0=0, alto=12)
    caja(l, 0, Y, 0, W, D, 10)
    tejado(mat('tejado_twain_hfd', 0x3a3a42, 0.6), 0, Y - D / 2, Y + D / 2, 10, W, 5, cumbrera='x')
    for x in (-8, 8):
        caja(l, x, yf - 1, 0, 4, 4, 14)
        o = cil(mat('tejado_twain_hfd', 0x3a3a42, 0.6), x, yf - 1, 14, 2.9, 4, 4, r2=0.1)
        o.rotation_euler = (0, 0, math.pi / 4)
    caja(madera_o(), 0, yf - 2, 0, 12, 4, 0.4)
    caja(madera_o(), 0, yf - 2, 3.2, 12, 4, 0.2)
    for x in (-5.5, -2, 2, 5.5):
        cil(madera_o(), x, yf - 3.8, 0.4, 0.12, 2.8, 8)
    for x in (-4, 0, 4):
        ventana_ojiva(x, 4.8, 1.2, 2.2, yf - 0.05, madera_o())
    for x in (-6, 6):
        caja(l, x, Y + 2, 12, 1.2, 1.2, 5)
    caja(blanco(), 0, yf - 4.1, 1.0, 5, 0.1, 0.8)
    texto(negro(), 'MARK TWAIN', 0, yf - 4.16, 1.2, tam=0.5, prof=0.02)

def old_state_house():
    """El antiguo Capitolio (1796): ladrillo rojo con piedra clara, el
    balcón, el frontón, la cúpula blanca y el águila dorada."""
    Y = 9
    W, D, H = 24.0, 16.0, 12.0
    yf = Y - D / 2
    l = ladrillo()
    caja(l, 0, Y, 0, W, D, H)
    caja(blanco(), 0, Y, H, W + 0.4, D + 0.4, 0.6)
    tejado(mat('tejado_osh_hfd', 0x4a4a52, 0.6), 0, Y - D / 2, Y + D / 2, H + 0.6, W, 3.0, cumbrera='x')
    fronton(blanco(), 0, yf - 0.4, H + 0.6, 12, 3.0, 0.8)
    for k in range(5):
        x = -10 + k * 5
        for z in (1.5, 6.5):
            ventana(x, z, 1.6, 2.8, y=yf - 0.05, marco=blanco(), cristal=cristal())
    caja(blanco(), 0, yf - 1, 5.5, 8, 2, 0.2)
    cil(blanco(), 0, Y, H + 3.6, 2.2, 3, 8)
    cupula(blanco(), 0, Y, H + 6.6, 2.3, 2, 12, 4)
    esfera(oro(), 0, Y, H + 9.2, 0.5, 1, esc=(1.6, 0.8, 1))

def cubo_pintura():
    """Un cubo de pintura blanca con la brocha (para la acera)."""
    cil(gris(), 0, 0, 0, 0.3, 0.45, 16)
    cil(blanco(), 0, 0, 0.44, 0.28, 0.02, 16)
    rama(madera(), (0.05, 0, 0.4), (0.25, -0.1, 0.9), 0.04, 0.04, 6)
    caja(blanco(), 0.04, 0.02, 0.38, 0.12, 0.04, 0.12)

# ================================================================ cruza la calle
def arco_soldados():
    """El arco de los soldados y marineros (1886) del parque Bushnell: el
    arco de piedra parda con sus dos torres redondas de tejado cónico."""
    p = piedra_p()
    for s in (-1, 1):
        cil(p, s * 8.6, 0, 0, 1.8, 14, 16)
        o = cil(mat('tejado_arco_hfd', 0x6a4a3a, 0.6), s * 8.6, 0, 14, 2.0, 4, 16, r2=0.1)
        for z in (6, 10):
            caja(cristal(), s * 8.6, -1.82, z, 0.6, 0.1, 1.2)
    caja(p, 0, 0, 9, 15.4, 2.4, 3.2)
    n = 24
    for k in range(n):
        u0, u1 = k / n, (k + 1) / n
        p0 = (-7.0 + 14 * u0, 0, 5.0 + 4.0 * math.sin(math.pi * u0))
        p1 = (-7.0 + 14 * u1, 0, 5.0 + 4.0 * math.sin(math.pi * u1))
        rama(p, p0, p1, 0.5, 0.5, 6)
    caja(marmol_l(), 0, -1.25, 10.2, 10, 0.1, 1.0)
    texto(negro(), 'SOLDIERS & SAILORS', 0, -1.32, 10.45, tam=0.55, prof=0.02)

# ================================================================ el tiovivo
def carrusel_bushnell():
    """El tiovivo del parque Bushnell (momento estrella): la galería larga
    con el toldo a rayas, los caballitos en sus barras doradas a los lados,
    los espejos, las bombillas, el órgano y los arcos de SALIDA y META.
    Cruza la calle: el origen en el centro."""
    L = 420
    caja(mat_bloques('suelo_carrusel_hfd', 0x9a6a3e, 0x6a4a2a, ancho=3.0, alto=0.3, grosor=0.02), 0, 0, -0.2, 26, L, 0.2)
    for s in (-1, 1):
        caja(mat_franjas('toldo_carrusel_hfd', 0xc8202a, 0xf6f4ee, 70, eje='Y', z0=-L / 2, alto=L), s * 10, 0, 7.5, 9, L, 0.3)
        caja(mat('espejos_hfd', 0xb8d0e0, 0.1), s * 14, 0, 1.0, 0.2, L, 5)
        for k in range(int(L / 10)):
            y = -L / 2 + 5 + k * 10
            cil(oro(), s * 8.5, y, 0, 0.08, 7.5, 8)
            caballito_m(s * 8.5, y, 0.5 + (k % 3) * 0.5, 1.0, [rojo, azul, amarillo][k % 3])
            esfera(bombilla(), s * 6.0, y, 7.3, 0.12, 1)
    for k in range(int(L / 105)):
        y = -L / 2 + 50 + k * 105
        caja(mat('organo_hfd', 0x8a3a6a, 0.5), -12, y, 0, 3, 6, 5)
        for i in range(8):
            cil(oro(), -10.45, y - 2.5 + i * 0.7, 2.0, 0.2, 2.5 + (i % 3) * 0.5, 8)
    for (y, txt) in ((-L / 2 + 1, 'SALIDA'), (L / 2 - 1, 'META')):
        for s in (-1, 1):
            cil(oro(), s * 7.0, y, 0, 0.3, 6.4, 8)
        caja(rojo(), 0, y, 5.6, 14.6, 0.5, 0.6)
        caja(amarillo(), 0, y, 4.0, 10, 0.16, 1.4)
        texto(rojo(), 'CARRUSEL · ' + txt, 0, y - 0.1, 4.45, tam=0.55, prof=0.04)

# ================================================================ obstáculos
def caballito():
    """El caballito del tiovivo (un vehículo: se va montado y sube y baja),
    con su barra dorada y la base. Mira al jugador (-y); el juego le da la
    vuelta al montarlo."""
    caja(mat('base_cab_hfd', 0x8a3a6a, 0.5), 0, 1.0, 0, 1.2, 2.6, 0.3)
    cil(oro(), 0, 1.0, 0.3, 0.06, 3.0, 8)
    caballito_m(0, 1.0, 0.3, 1.0, rojo)

def valla_tom():
    """El trozo de valla de Tom Sawyer (va en la orilla; se pinta pasando a
    su lado): 7 m de tablas sin pintar, a lo largo de la calle."""
    m = mat('tabla_sin_pintar_hfd', 0xb8b0a0, 0.85)
    for k in range(24):
        y = -3.4 + k * 0.29
        caja(m, 0, y, 0, 0.06, 0.2, 1.05)
        cil(m, 0, y, 1.05, 0.1, 0.12, 3, r2=0.0)
    for z in (0.3, 0.8):
        caja(m, 0.05, 0, z, 0.04, 7.0, 0.1)

def cubo_volcado():
    """El cubo de pintura volcado con el charco blanco (se salta)."""
    o = cil(gris(), 0.2, 0, 0.3, 0.3, 0.45, 16, eje='X')
    caja(blanco(), -0.5, 0, 0.0, 1.4, 1.1, 0.03)
    esfera(blanco(), -0.6, 0.2, 0.03, 0.4, 1, esc=(1.2, 1, 0.08))

def furgon_seguros():
    """La furgoneta de los seguros (no se pasa): blanca con el paraguas
    rojo pintado y SEGUROS. El morro en el origen."""
    b = blanco()
    caja(b, 0, 1.0, 0.4, 2.2, 2.0, 1.4)
    caja(cristal(), 0, 0.0, 1.2, 1.9, 0.1, 0.6)
    caja(b, 0, 3.6, 0.4, 2.3, 3.6, 2.2)
    for s in (-1, 1):
        cil(rojo(), s * 1.17, 3.6, 1.9, 0.7, 0.05, 12, eje='X', r2=0.05)
        texto(azul(), 'SEGUROS', s * 1.18, 3.6, 0.9, tam=0.3, prof=0.01).rotation_euler = (math.pi / 2, 0, -s * math.pi / 2)
    for (y, s) in ((1.0, 1), (4.6, 1), (1.0, -1), (4.6, -1)):
        cil(negro(), s * 1.1, y, 0.38, 0.38, 0.3, 14, eje='X')
    for s in (-1, 1):
        caja(luz('faro_seg_obst_hfd', 0xfff2c0, 1.0), s * 0.8, -0.03, 0.75, 0.35, 0.05, 0.2)

def cartel_ct():
    """La pancarta del Sentido Común (agacharse): LEE LA LETRA PEQUEÑA."""
    for x in (-1.25, 1.25):
        cil(madera_o(), x, 0, 0, 0.07, 2.75, 8)
    caja(azul(), 0, 0, 1.5, 2.4, 0.05, 1.2)
    esfera(rosa(), -0.9, -0.05, 2.1, 0.2, 1, esc=(1.2, 0.4, 1))
    texto(blanco(), 'LEE LA', 0.15, -0.035, 2.2, tam=0.24, prof=0.02)
    texto(amarillo(), 'LETRA PEQUEÑA', 0.15, -0.035, 1.8, tam=0.18, prof=0.02)

# ================================================================ Main Street de verdad
# 26/11/2026: Isidro: «más que añadir edificios sin sentido quiero que sean los
# reales». Los edificios de Main Street en su orden de verdad (de norte a sur,
# por la acera este: G. Fox, el Cheney Building, el antiguo Capitolio, la torre
# de los seguros, el Atheneum, el ayuntamiento, la biblioteca y la casa
# Butler-McCook; enfrente, Center Church y su cementerio de 1640), y al final,
# frente al Capitolio, el teatro Bushnell y el parque.

def arco_medio(m, x, y, z, w, h, prof=0.1):
    """Hueco de medio punto: rectángulo de alto h y medio círculo encima."""
    caja(m, x, y, z, w, prof, h)
    cil(m, x, y, z + h, w / 2, prof, 16, eje='Y')

def g_fox():
    """Los almacenes G. Fox & Co. (1918; fachada art déco de 1938): once
    plantas de piedra clara con franjas negras y doradas de arriba abajo,
    escaparates y el rótulo grande sobre la marquesina."""
    W, D, H = 26.0, 18.0, 40.0
    Y = 1 + D / 2; yf = Y - D / 2
    caja(mat('piedra_fox_hfd', 0xe6dcc6, 0.5), 0, Y, 0, W, D, H)
    caja(negro(), 0, Y, H, W + 0.4, D + 0.4, 1.2)
    for k in range(7):
        x = -9 + k * 3
        caja(negro(), x, yf - 0.15, 6, 1.4, 0.3, H - 6)
        caja(oro(), x, yf - 0.31, 6, 0.28, 0.04, H - 6)
    for k in range(6):
        for z in range(8, int(H) - 2, 3):
            caja(cristal(), -7.5 + k * 3, yf - 0.05, z, 1.3, 0.1, 2.0)
    for x in (-9.5, -3.2, 3.2, 9.5):
        caja(cristal(), x, yf - 0.05, 0.5, 5.0, 0.1, 3.3)
    caja(negro(), 0, yf - 0.8, 4.2, W, 1.6, 0.4)
    caja(oro(), 0, yf - 0.4, 4.8, 15, 0.1, 1.4)
    texto(negro(), 'G. FOX & CO.', 0, yf - 0.47, 5.5, tam=1.0, prof=0.05)

def cheney_building():
    """El Cheney Building (1876, H. H. Richardson): arenisca roja y parda,
    arcos de medio punto que abarcan tres plantas, arcada abajo y tejado
    a dos aguas."""
    W, D, H = 26.0, 16.0, 21.0
    Y = 1 + D / 2; yf = Y - D / 2
    roja = mat_bloques('arenisca_cheney_hfd', 0xa4553c, 0x7a3c2a, ancho=1.0, alto=0.5, grosor=0.01)
    parda = mat('parda_cheney_hfd', 0x6a4636, 0.7)
    caja(roja, 0, Y, 0, W, D, H)
    caja(parda, 0, Y, H, W + 0.6, D + 0.6, 0.9)
    tejado(mat('tejado_cheney_hfd', 0x3a3a42, 0.6), 0, Y - D / 2, Y + D / 2, H + 0.9, W, 4.0, cumbrera='x')
    caja(parda, 0, yf - 0.1, 0, W + 0.2, 0.3, 4.6)
    for k in range(5):
        x = -10 + k * 5
        arco_medio(cristal(), x, yf - 0.3, 0.4, 3.4, 2.6)
        arco_medio(parda, x, yf - 0.12, 5.2, 4.2, 8.6, 0.12)
        arco_medio(cristal(), x, yf - 0.2, 5.6, 3.4, 8.2)
        for z in (8.2, 11.4):
            caja(parda, x, yf - 0.24, z, 3.6, 0.12, 0.35)
        for dx in (-1.0, 1.0):
            arco_medio(cristal(), x + dx, yf - 0.05, 17.0, 1.1, 1.6)
    caja(blanco(), 0, yf - 0.3, 4.75, 7.5, 0.06, 0.7)
    texto(parda, 'CHENEY BUILDING', 0, yf - 0.35, 5.1, tam=0.45, prof=0.02)

def center_church():
    """Center Church (First Church of Christ, 1807): ladrillo, pórtico blanco
    de cuatro columnas con frontón y el campanario blanco de pisos con la
    aguja; la congregación es de 1632, la de los fundadores de Hartford."""
    W, D, H = 18.0, 26.0, 12.0
    Y = 6 + D / 2; yf = Y - D / 2
    caja(ladrillo(), 0, Y, 0, W, D, H)
    tejado(mat('tejado_cc_hfd', 0x4a4a52, 0.6), 0, yf, Y + D / 2, H, W, 4.5)
    fronton(ladrillo(), 0, yf, H, W, 4.5, 0.2)
    caja(blanco(), 0, yf - 2.6, 0, 13, 5.2, 0.5)
    escalinata(blanco(), 0, yf - 5.2, 0, 13, 3, huella=0.3, tabica=0.17)
    columnata(blanco(), -4.5, 4.5, 4, yf - 4.4, 0.5, 0.42, 8.5)
    caja(blanco(), 0, yf - 2.4, 9.0, 12.6, 4.8, 1.1)
    fronton(blanco(), 0, yf - 4.8, 10.1, 12.8, 3.0, 4.8)
    puerta(0, 0.5, 2.0, 4.0, y=yf, color=0x24344e, marco=blanco())
    for x in (-4.5, 4.5):
        puerta(x, 0.5, 1.4, 3.2, y=yf, color=0x24344e, marco=blanco())
    for s in (-1, 1):
        for k in range(5):
            caja(cristal(), s * (W / 2 + 0.03), yf + 3 + k * 4.6, 2.0, 0.08, 1.6, 6.5)
    T = yf + 2.5
    caja(blanco(), 0, T, H, 5.2, 5.2, 6)
    cil(oro(), 0, T - 2.62, H + 3.2, 1.0, 0.08, 20, eje='Y')
    caja(blanco(), 0, T, H + 6, 4.2, 4.2, 4)
    for x in (-1.2, 1.2):
        arco_medio(negro(), x, T - 2.12, H + 6.8, 0.8, 1.8)
    cil(blanco(), 0, T, H + 10, 1.9, 3.5, 8)
    cil(blanco(), 0, T, H + 13.5, 1.6, 9.5, 8, r2=0.06)
    esfera(oro(), 0, T, H + 23.2, 0.32, 1)

def cementerio_antiguo():
    """El Ancient Burying Ground (1640), junto a Center Church: césped,
    lápidas de pizarra torcidas, la verja de hierro y árboles viejos."""
    import random
    W, D = 24.0, 22.0
    Y = 1 + D / 2; yf = Y - D / 2
    caja(cesped(), 0, Y, 0, W, D, 0.08)
    for k in range(23):
        cil(hierro(), -11 + k, yf + 0.2, 0, 0.05, 1.6, 6)
    caja(hierro(), 0, yf + 0.2, 1.45, W - 2, 0.06, 0.08)
    caja(hierro(), 0, yf + 0.2, 0.25, W - 2, 0.06, 0.08)
    pizarra = mat('pizarra_hfd', 0x4a4e56, 0.8)
    r = random.Random(1640)
    for fila in range(4):
        for k in range(6):
            x = -9 + k * 3.4 + r.uniform(-0.5, 0.5)
            y = yf + 4 + fila * 3.6 + r.uniform(-0.4, 0.4)
            caja(pizarra, x, y, 0, 0.9, 0.12, 1.0 + r.uniform(0, 0.4), giro=r.uniform(-0.15, 0.15), inclina=r.uniform(-0.12, 0.12))
            esfera(pizarra, x, y, 1.05, 0.45, 1, esc=(1, 0.14, 0.5))
    tronco = mat('tronco_hfd', 0x5a4232, 0.9)
    hoja = mat('hoja_otono_hfd', 0xc8782a, 0.8)
    for (x, y) in ((-8, yf + 15), (6, yf + 9), (9, yf + 18)):
        cil(tronco, x, y, 0, 0.45, 6, 8, r2=0.3)
        for (dx, dy, dz, rr) in ((0, 0, 7.2, 3.2), (1.6, 0.6, 6.0, 2.2), (-1.5, -0.4, 6.2, 2.3)):
            esfera(hoja, x + dx, y + dy, dz, rr, 2)
    caja(madera_o(), 9.5, yf - 0.1, 0, 0.15, 0.15, 2.2)
    caja(blanco(), 9.5, yf - 0.2, 1.4, 3.6, 0.08, 0.9)
    texto(negro(), 'ANCIENT BURYING', 9.5, yf - 0.25, 2.0, tam=0.28, prof=0.02)
    texto(negro(), 'GROUND  1640', 9.5, yf - 0.25, 1.62, tam=0.28, prof=0.02)

def atheneum():
    """El Wadsworth Atheneum (1844): el castillo gótico de granito gris, el
    museo de arte público más antiguo del país; dos torres almenadas a los
    lados de la entrada en ojiva y almenas por todo el borde."""
    W, D, H = 32.0, 20.0, 14.0
    Y = 2 + D / 2; yf = Y - D / 2
    g = granito()
    caja(g, 0, Y, 0, W, D, H)
    for k in range(16):
        caja(g, -15 + k * 2, yf + 0.4, H, 1.0, 0.8, 1.2)
    for s in (-1, 1):
        caja(g, s * 5, yf - 0.6, 0, 5, 5.2, H + 6)
        for (dx, dy) in ((-2, -2), (2, -2), (-2, 2), (2, 2), (0, -2), (-2, 0), (2, 0)):
            caja(g, s * 5 + dx, yf - 0.6 + dy, H + 6, 1.0, 1.0, 1.2)
        for z in (3, 8, 13.5):
            ventana_ojiva(s * 5, z, 0.9, 2.0, yf - 3.25, g)
    caja(g, 0, yf - 0.8, 0, 5, 1.6, 10)
    for k in range(5):
        caja(g, -2 + k, yf - 1.0, 10, 0.6, 1.2, 0.9)
    ventana_ojiva(0, 0.2, 3.0, 5.8, yf - 1.65, g)
    for x in (-13, -10, 10, 13):
        for z in (2.0, 7.6):
            ventana_ojiva(x, z, 1.3, 3.0, yf - 0.05, g)
    caja(blanco(), 0, yf - 1.65, 8.4, 4.4, 0.06, 0.9)
    texto(negro(), 'WADSWORTH', 0, yf - 1.7, 9.05, tam=0.38, prof=0.02)
    texto(negro(), 'ATHENEUM', 0, yf - 1.7, 8.62, tam=0.38, prof=0.02)

def ayuntamiento_hfd():
    """El Municipal Building (1915), el ayuntamiento: Beaux-Arts de granito
    claro, la planta baja almohadillada con tres arcos, columnas en las dos
    plantas de en medio y la cornisa."""
    W, D, H = 36.0, 22.0, 19.0
    Y = 2 + D / 2; yf = Y - D / 2
    g = granito()
    base = mat_bloques('almohadillado_hfd', 0xd8d2c4, 0xa8a294, ancho=1.6, alto=0.7, grosor=0.03)
    caja(base, 0, Y, 0, W, D, 5.5)
    caja(g, 0, Y, 5.5, W, D, H - 5.5)
    caja(marmol_l(), 0, Y, H, W + 0.8, D + 0.8, 1.0)
    caja(marmol_l(), 0, Y, 5.5, W + 0.3, D + 0.3, 0.5)
    for x in (-5, 0, 5):
        arco_medio(cristal(), x, yf - 0.05, 0.3, 2.8, 3.2)
    escalinata(marmol_l(), 0, yf - 0.1, 0, 16, 3, huella=0.32, tabica=0.12)
    columnata(marmol_l(), -14, 14, 10, yf - 0.7, 6.0, 0.45, 9.0)
    caja(marmol_l(), 0, yf - 0.6, 15.0, W - 4, 1.0, 0.8)
    for k in range(9):
        x = -12.4 + k * 3.1
        for z in (7.0, 11.0):
            caja(cristal(), x, yf - 0.05, z, 1.5, 0.1, 2.6)
        caja(cristal(), x, yf - 0.05, 16.3, 1.2, 0.1, 1.4)
    for x in (-15, -9, 9, 15):
        caja(cristal(), x, yf - 0.05, 1.3, 1.5, 0.1, 2.4)
    texto(negro(), 'MUNICIPAL BUILDING', 0, yf - 1.12, 15.4, tam=0.55, prof=0.03)

def biblioteca_hfd():
    """La biblioteca pública de Hartford (500 Main Street): el edificio de
    1957 envuelto en 2007 por una fachada de cristal, con base de piedra."""
    W, D, H = 30.0, 22.0, 14.0
    Y = 2 + D / 2; yf = Y - D / 2
    caja(mat('piedra_bib_hfd', 0xc8c0b0, 0.5), 0, Y, 0, W, D, 1.0)
    caja(mat('cristal_bib_hfd', 0x6a96b4, 0.12), 0, Y, 1.0, W, D, H - 1.0)
    for k in range(21):
        caja(gris(), -15 + k * 1.5, yf - 0.06, 1.0, 0.12, 0.12, H - 1.0)
    for z in (5.0, 9.5):
        caja(gris(), 0, yf - 0.08, z, W, 0.16, 0.25)
    caja(blanco(), 0, Y, H, W + 0.6, D + 0.6, 0.7)
    caja(blanco(), 0, yf - 2.0, 3.6, 10, 4.0, 0.3)
    for x in (-4.6, 4.6):
        cil(blanco(), x, yf - 3.8, 0, 0.15, 3.6, 8)
    caja(negro(), 0, yf - 0.12, 1.0, 4, 0.06, 2.6)
    texto(mat('azul_bib_hfd', 0x1c3a6a, 0.4), 'HARTFORD PUBLIC LIBRARY', 0, yf - 0.2, 4.4, tam=0.6, prof=0.03)

def butler_mccook():
    """La casa Butler-McCook (1782): la casa más antigua de Main Street, de
    tablas de madera, contraventanas, tejado a dos aguas y su jardín
    con la valla de estacas."""
    W, D, H = 14.0, 11.0, 7.0
    Y = 8 + D / 2; yf = Y - D / 2
    caja(cesped(), 0, 4, 0, 24, 8, 0.06)
    caja(mat('camino_bm_hfd', 0xc8b89a, 0.9), 0, 4, 0.03, 1.6, 8, 0.06)
    tablas = mat_franjas('tablas_bm_hfd', 0x8a6a4e, 0x6a4e3a, 30, eje='Z', z0=0, alto=H)
    caja(tablas, 0, Y, 0, W, D, H)
    tejado(mat('tejado_bm_hfd', 0x3e3a38, 0.7), 0, Y - D / 2, Y + D / 2, H, W, 3.6, cumbrera='x')
    for x in (-4, 4):
        caja(ladrillo(), x, Y + 1, H, 1.2, 1.2, 5)
    contra = mat('contra_bm_hfd', 0x2e4a3a, 0.6)
    for x in (-5, -2.5, 2.5, 5):
        for z in (1.2, 4.3):
            ventana(x, z, 1.0, 1.7, y=yf, marco=blanco(), cristal=cristal(), persiana=contra)
    ventana(0, 4.3, 1.0, 1.7, y=yf, marco=blanco(), cristal=cristal(), persiana=contra)
    puerta(0, 0.2, 1.3, 2.4, y=yf, color=0x2e4a3a, marco=blanco())
    fronton(blanco(), 0, yf - 0.15, 2.75, 2.0, 0.5, 0.2)
    for k in range(23):
        x = -11.5 + k * 1.0
        if abs(x) < 1.0:
            continue
        caja(blanco(), x, 0.3, 0, 0.1, 0.06, 1.0)
    for z in (0.3, 0.8):
        caja(blanco(), -6.5, 0.32, z, 10.2, 0.04, 0.08)
        caja(blanco(), 6.5, 0.32, z, 10.2, 0.04, 0.08)
    flor = mat('flores_bm_hfd', 0xd8546a, 0.7)
    for x in (-9, -6, 6, 9):
        esfera(flor, x, 1.4, 0.4, 0.7, 1, esc=(1.4, 1, 0.6))
    caja(blanco(), 7.5, -0.2, 1.1, 3.4, 0.06, 0.8)
    texto(negro(), 'BUTLER-McCOOK', 7.5, -0.24, 1.65, tam=0.26, prof=0.02)
    texto(negro(), 'HOUSE  1782', 7.5, -0.24, 1.3, tam=0.26, prof=0.02)

def bushnell_teatro():
    """El teatro The Bushnell (1930), frente al Capitolio: ladrillo rojo de
    estilo georgiano, el pórtico blanco de columnas con frontón y la
    torrecilla blanca de la cúpula dorada."""
    W, D, H = 36.0, 24.0, 15.0
    Y = 4 + D / 2; yf = Y - D / 2
    caja(ladrillo(), 0, Y, 0, W, D, H)
    caja(blanco(), 0, Y, H, W + 0.6, D + 0.6, 1.0)
    caja(blanco(), 0, yf - 2.2, 0, 16, 4.4, 0.6)
    escalinata(blanco(), 0, yf - 4.4, 0, 16, 3, huella=0.3, tabica=0.2)
    columnata(blanco(), -6, 6, 4, yf - 3.6, 0.6, 0.6, 11.0)
    caja(blanco(), 0, yf - 2.0, 11.6, 15, 4.2, 1.2)
    fronton(blanco(), 0, yf - 4.1, 12.8, 15.2, 3.2, 4.2)
    for x in (-3, 0, 3):
        puerta(x, 0.6, 1.8, 3.4, y=yf, color=0x2a1e18, marco=blanco())
        arco_medio(cristal(), x, yf - 0.05, 5.0, 1.6, 3.0)
    for s in (-1, 1):
        for k in range(3):
            x = s * (10 + k * 3)
            for z in (2.0, 8.0):
                ventana(x, z, 1.4, 2.6, y=yf, marco=blanco(), cristal=cristal(), remate='cornisa')
    cil(blanco(), 0, Y, H + 1.0, 3.2, 4.0, 8)
    cil(blanco(), 0, Y, H + 5.0, 2.4, 3.0, 8)
    cupula(oro(), 0, Y, H + 8.0, 2.3, 2.6, 16, 6)
    esfera(oro(), 0, Y, H + 11.0, 0.35, 1)
    texto(rojo(), 'THE BUSHNELL', 0, yf - 4.15, 12.0, tam=0.9, prof=0.04)

def parque_bushnell():
    """Un trozo del parque Bushnell (1854, el primer parque público pagado
    por una ciudad en Estados Unidos): césped, olmos viejos, un camino, una
    farola y un banco."""
    W, D = 24.0, 30.0
    Y = 1 + D / 2; yf = Y - D / 2
    caja(cesped(), 0, Y, 0, W, D, 0.07)
    caja(mat('camino_pq_hfd', 0xc8bca4, 0.9), 0, yf + 3, 0.04, W, 2.0, 0.06)
    tronco = mat('tronco_pq_hfd', 0x5a4232, 0.9)
    hojas = [mat('hoja_pq1_hfd', 0xd07a2a, 0.8), mat('hoja_pq2_hfd', 0xb8462a, 0.8), mat('hoja_pq3_hfd', 0xd8a830, 0.8)]
    for i, (x, y) in enumerate(((-7, yf + 8), (5, yf + 11), (-2, yf + 20), (8, yf + 24))):
        cil(tronco, x, y, 0, 0.5, 7, 8, r2=0.32)
        h = hojas[i % 3]
        for (dx, dy, dz, rr) in ((0, 0, 8.4, 3.6), (1.9, 0.8, 7.0, 2.5), (-1.8, -0.6, 7.2, 2.6), (0.4, -1.6, 9.4, 2.2)):
            esfera(h, x + dx, y + dy, dz, rr, 2)
    cil(hierro(), 9, yf + 1.6, 0, 0.09, 4, 8)
    esfera(bombilla(), 9, yf + 1.6, 4.2, 0.35, 1)
    caja(madera(), -3, yf + 4.6, 0.45, 2.2, 0.5, 0.08)
    caja(madera(), -3, yf + 4.85, 0.5, 2.2, 0.08, 0.5)
    for x in (-3.9, -2.1):
        caja(hierro(), x, yf + 4.6, 0, 0.08, 0.5, 0.45)


PIEZAS = {
    'g_fox':             (g_fox,             'hartford',   dict(lado=1024, bisel=0.0)),
    'cheney_building':   (cheney_building,   'hartford',   dict(lado=1024, bisel=0.0)),
    'center_church':     (center_church,     'hartford',   dict(lado=1024, bisel=0.0)),
    'cementerio_antiguo':(cementerio_antiguo,'hartford',   dict(lado=1024, bisel=0.0)),
    'atheneum':          (atheneum,          'hartford',   dict(lado=1024, bisel=0.0)),
    'ayuntamiento_hfd':  (ayuntamiento_hfd,  'hartford',   dict(lado=1024, bisel=0.0)),
    'biblioteca_hfd':    (biblioteca_hfd,    'hartford',   dict(lado=1024, bisel=0.0)),
    'butler_mccook':     (butler_mccook,     'hartford',   dict(lado=1024, bisel=0.0)),
    'bushnell_teatro':   (bushnell_teatro,   'hartford',   dict(lado=1024, bisel=0.0)),
    'parque_bushnell':   (parque_bushnell,   'hartford',   dict(lado=512, bisel=0.0)),
    'capitolio_ct':      (capitolio_ct,      'hartford',   dict(lado=2048, bisel=0.0)),
    'torre_seguros':     (torre_seguros,     'hartford',   dict(lado=1024, bisel=0.0)),
    'casa_mark_twain':   (casa_mark_twain,   'hartford',   dict(lado=1024, bisel=0.0)),
    'old_state_house':   (old_state_house,   'hartford',   dict(lado=1024, bisel=0.0)),
    'cubo_pintura':      (cubo_pintura,      'hartford',   dict(lado=256, bisel=0.0)),
    'arco_soldados':     (arco_soldados,     'hartford',   dict(lado=1024, bisel=0.0, suelo=False)),
    'carrusel_bushnell': (carrusel_bushnell, 'hartford',   dict(lado=2048, bisel=0.0, suelo=False)),
    'caballito':         (caballito,         'obstaculos', dict(lado=256, bisel=0.0)),
    'valla_tom':         (valla_tom,         'obstaculos', dict(lado=256, bisel=0.0)),
    'cubo_volcado':      (cubo_volcado,      'obstaculos', dict(lado=256, bisel=0.0)),
    'furgon_seguros':    (furgon_seguros,    'obstaculos', dict(lado=256, bisel=0.0)),
    'cartel_ct':         (cartel_ct,         'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
}

correr(PIEZAS)
