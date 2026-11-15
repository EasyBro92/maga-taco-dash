# Nivel 34: Seattle, Washington (15/11/2026).
#
#   blender -b -P blender/seattle.py -- [pieza ...] [--rapido]
#
# Historia: «Llueve sin parar: su pelo corre peligro». Acto de la Armada
#   Española. Por 5th Avenue bajo la lluvia, con el monorraíl por encima de la
#   acera: el mercado de Pike Place con su reloj y su letrero rojo, la Smith
#   Tower, la biblioteca de cristal y la cerdita de bronce Rachel en la acera.
#   El chaparrón: hay que ir de marquesina en marquesina para que no se moje el
#   tupé; y el momento estrella, los pescaderos de Pike Place, que te lanzan
#   salmones (hay que tocar justo cuando llegan para cogerlos). Final en la
#   Space Needle. Pancartas de España: JUAN DE FUCA LLEGÓ EN 1592 (el estrecho
#   lleva el nombre del griego que navegaba para España).
# Obstáculos (carpeta obstaculos): la marquesina de cristal (no estorba: se va
# debajo), el cajón de pescado con hielo, la pancarta, el carrito del café, el
# tranvía de South Lake Union y el salmón que vuela.

import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import *

def blanco():    return mat('blanco_sea', 0xf6f4ee, 0.5)
def negro():     return mat('negro_sea', 0x1c1c20, 0.4)
def hormigon():  return mat('hormigon_sea', 0xc8c6c0, 0.8)
def cristal():   return mat('cristal_sea', 0x3a5a70, 0.15)
def cristal_c(): return mat('cristal_claro_sea', 0x9ac0d8, 0.1)
def rojo():      return mat('rojo_sea', 0xc8202a, 0.45)
def azul():      return mat('azul_sea', 0x2a4a9a, 0.45)
def amarillo():  return mat('amarillo_sea', 0xf2c21a, 0.45)
def naranja():   return mat('naranja_sea', 0xe8701a, 0.45)
def verde():     return mat('verde_sea', 0x2a6a3a, 0.5)
def gris():      return mat('gris_sea', 0x8a9098, 0.4)
def plata():     return mat('plata_sea', 0xc8ccd0, 0.25)
def hierro():    return mat('hierro_sea', 0x2a2c30, 0.45)
def madera():    return mat('madera_sea', 0x8a5a34, 0.85)
def madera_o():  return mat('madera_oscura_sea', 0x5a3a22, 0.85)
def ladrillo():  return mat_bloques('ladrillo_sea', 0xa85a3e, 0x7a4030, ancho=0.4, alto=0.16)
def terracota(): return mat_bloques('terracota_sea', 0xf2eee4, 0xd8d2c4, ancho=0.9, alto=0.6, grosor=0.008)
def salmon_m():  return mat('salmon_sea', 0xe8806a, 0.5)
def salmon_l():  return mat('salmon_lomo_sea', 0x6a7a8a, 0.4)
def hielo():     return mat('hielo_sea', 0xe8f4fa, 0.2)
def bronce():    return mat('bronce_sea', 0x7a5a32, 0.3)
def piel():      return mat('piel_sea', 0xe8b89a, 0.7)
def neon_r():    return luz('neon_rojo_sea', 0xff3a2a, 1.4)

def bandera_es(nombre, z0, alto):
    return mat_franjas(nombre, 0xc8202a, 0xf2c21a, 3, eje='Z', z0=z0, alto=alto)

def salmon_pez(x, y, z, k=1.0, giro=0.0):
    """Un salmón tumbado de lado, la cabeza hacia -y (giro gira en planta)."""
    c, s = math.cos(giro), math.sin(giro)
    def p(dx, dy):
        return (x + dx * c - dy * s, y + dx * s + dy * c)
    o = esfera(salmon_m(), *p(0, 0), z, 0.5 * k, 2, esc=(0.32, 1.0, 0.42))
    o.rotation_euler = (0, 0, giro)
    o = esfera(salmon_l(), *p(0, 0.02 * k), z + 0.06 * k, 0.48 * k, 2, esc=(0.3, 0.95, 0.3))
    o.rotation_euler = (0, 0, giro)
    o = cil(salmon_l(), *p(0, 0.55 * k), z - 0.18 * k, 0.2 * k, 0.36 * k, 3, r2=0.02)
    o.rotation_euler = (0, math.pi / 2, giro + math.pi / 2)
    for sx in (-1, 1):
        esfera(negro(), *p(sx * 0.14 * k, -0.36 * k), z + 0.04 * k, 0.035 * k, 1)

# ================================================================ la meta
def space_needle():
    """La Space Needle (la meta): las tres parejas de patas que se estrechan
    en la cintura y se abren hasta el platillo, el núcleo de los ascensores,
    el platillo con el restaurante de cristal, el tejado dorado y la aguja.
    Delante, la plaza, la fuente y la pancarta JUAN DE FUCA LLEGÓ EN 1592."""
    Y = 30
    h = hormigon()
    b = blanco()
    cil(h, 0, Y, 0, 2.2, 56, 16)
    caja(oro_asc := mat('ascensor_sea', 0xe8b840, 0.3), 0, Y - 2.2, 4, 1.4, 0.4, 2.4)
    for k in range(3):
        a0 = k * math.tau / 3
        for d in (-0.22, 0.22):
            a = a0 + d
            p0 = (math.cos(a) * 11, Y + math.sin(a) * 11, 0)
            p1 = (math.cos(a) * 3.0, Y + math.sin(a) * 3.0, 34)
            p2 = (math.cos(a) * 7.5, Y + math.sin(a) * 7.5, 55)
            rama(b, p0, p1, 0.7, 0.45, 8)
            rama(b, p1, p2, 0.45, 0.55, 8)
        cil(b, math.cos(a0) * 3.1, Y + math.sin(a0) * 3.1, 33.6, 0.9, 0.8, 8)
    cil(b, 0, Y, 33.5, 3.6, 0.8, 18)
    for z in (14, 24, 44):
        cil(mat('anillo_sea', 0xdcdad4, 0.6), 0, Y, z, 2.6, 0.4, 16)
    # El platillo.
    cil(b, 0, Y, 54.5, 8.0, 1.0, 36, r2=13.5)
    cil(b, 0, Y, 55.5, 13.5, 0.7, 36)
    cil(cristal_c(), 0, Y, 56.2, 12.2, 3.0, 36)
    for k in range(24):
        a = k * math.tau / 24
        caja(b, math.cos(a) * 12.25, Y + math.sin(a) * 12.25, 56.2, 0.25, 0.25, 3.0)
    cil(b, 0, Y, 59.2, 13.2, 0.6, 36)
    cil(mat('tejado_needle_sea', 0xe0a030, 0.35), 0, Y, 59.8, 12.4, 1.6, 36, r2=5.0)
    cil(b, 0, Y, 61.4, 5.0, 2.0, 24, r2=3.5)
    cil(cristal_c(), 0, Y, 63.4, 3.4, 1.4, 18)
    cil(b, 0, Y, 64.8, 3.6, 0.5, 18, r2=1.0)
    cil(gris(), 0, Y, 65.3, 0.45, 14, 8, r2=0.08)
    # La plaza y la pancarta.
    caja(mat('plaza_sea', 0xb8b4ac, 0.8), 0, Y - 8, -0.05, 80, 50, 0.06)
    for (x, y) in ((-28, Y - 20), (-34, Y - 4), (28, Y - 20), (34, Y - 4)):
        cil(madera_o(), x, y, 0, 0.35, 3.2, 8)
        esfera(mat('copa_sea', 0x2a5a32, 0.85), x, y, 6.0, 3.0, 2, esc=(0.8, 0.8, 1.5))
    cil(gris(), -15, Y - 18, 0, 3.2, 0.5, 24)
    cil(mat('agua_fuente_sea', 0x5a90b8, 0.1), -15, Y - 18, 0.5, 2.9, 0.06, 24)
    for x in (8.5, 21.5):
        cil(madera_o(), x, Y - 22, 0, 0.12, 4.4, 8)
    caja(bandera_es('pancarta_es_needle_sea', 2.8, 1.6), 15, Y - 22, 2.8, 13, 0.06, 1.6)
    texto(negro(), 'JUAN DE FUCA LLEGÓ EN 1592', 15, Y - 22.04, 3.4, tam=0.62, prof=0.03)

# ================================================================ edificios
def mercado_pike():
    """El mercado de Pike Place: el edificio bajo con su toldo, el gran
    letrero rojo PUBLIC MARKET CENTER con el reloj en lo alto de la esquina,
    FARMERS MARKET debajo y los puestos de fruta y flores en la entrada."""
    Y = 8
    W, D = 30.0, 12.0
    yf = Y - D / 2
    caja(mat('fachada_pike_sea', 0xe0d4bc, 0.8), 0, Y, 0, W, D, 7.5)
    caja(madera_o(), 0, Y, 7.5, W + 0.4, D + 0.4, 0.5)
    for x in (-10, -4, 4, 10):
        ventana(x, 3.6, 2.4, 2.4, y=yf - 0.05, marco=madera_o(), cristal=cristal())
    caja(verde(), 0, yf - 1.4, 3.0, W - 2, 2.8, 0.2)
    caja(cristal(), 0, yf - 0.05, 0, 18, 0.1, 2.8)
    # Los puestos de la entrada (cajas de fruta y cubos de flores).
    for k in range(8):
        x = -12 + k * 3.4
        caja(madera(), x, yf - 1.6, 0, 2.6, 1.4, 0.9)
        for i in range(4):
            esfera([rojo, amarillo, naranja, verde][(k + i) % 4](), x - 0.9 + i * 0.6, yf - 1.6, 1.0, 0.24, 1)
    # El letrero del reloj.
    caja(hierro(), 0, yf + 1, 8.0, 0.3, 0.3, 4.0)
    caja(blanco(), 0, yf + 0.8, 11.6, 13, 0.3, 2.0)
    texto(neon_r(), 'PUBLIC MARKET', 0, yf + 0.6, 12.0, tam=1.1, prof=0.08)
    cil(blanco(), 0, yf + 0.7, 15.6, 1.9, 0.25, 32, eje='Y')
    cil(negro(), 0, yf + 0.55, 15.6, 1.75, 0.04, 32, eje='Y')
    cil(blanco(), 0, yf + 0.5, 15.6, 1.6, 0.04, 32, eje='Y')
    caja(negro(), 0, yf + 0.45, 15.6, 0.1, 0.04, 1.2)
    caja(negro(), 0.4, yf + 0.45, 15.6, 0.9, 0.04, 0.1)
    texto(neon_r(), 'CENTER', 0, yf + 0.6, 10.6, tam=0.75, prof=0.06)
    caja(mat('letrero_fm_sea', 0x2a2a30, 0.5), 0, yf - 0.1, 5.4, 12, 0.15, 1.1)
    texto(neon_r(), 'FARMERS MARKET', 0, yf - 0.2, 5.6, tam=0.75, prof=0.05)

def smith_tower():
    """La Smith Tower (1914): la base ancha de terracota blanca, la torre
    estrecha de muchos pisos y el tejado de pirámide con la bola de cristal."""
    Y = 9
    t = terracota()
    caja(t, 0, Y, 0, 22, 14, 14)
    for x in (-8, -4, 0, 4, 8):
        for z in (2, 6, 10):
            ventana(x, z, 1.4, 2.6, y=Y - 7 - 0.05, marco=blanco(), cristal=cristal())
    caja(t, 0, Y, 14, 12, 10, 38)
    for z in range(16, 50, 3):
        for x in (-3.6, -1.2, 1.2, 3.6):
            caja(cristal(), x, Y - 5.05, z, 1.2, 0.1, 1.8)
    caja(blanco(), 0, Y, 52, 13, 11, 0.8)
    o = cil(mat('piramide_sea', 0x3a6a5a, 0.4), 0, Y, 52.8, 8.2, 11, 4, r2=0.6)
    o.rotation_euler = (0, 0, math.pi / 4)
    for z in (55, 58):
        caja(cristal(), 0, Y - 3.4 + (z - 55) * 0.5, z, 2.0, 0.1, 1.4)
    esfera(cristal_c(), 0, Y, 64.3, 0.9, 2)
    puerta(0, 0, 3.0, 4.0, y=Y - 7 - 0.05, color=0x5a3a22, marco=blanco())
    texto(negro(), 'SMITH TOWER', 0, Y - 7.06, 4.6, tam=0.6, prof=0.03)

def biblioteca_seattle():
    """La biblioteca central de Seattle: los bloques de cristal con la red
    de rombos de acero, uno encima de otro y descolocados."""
    Y = 10
    red = mat_bloques('red_rombos_sea', 0x6a8aa8, 0x2a3038, ancho=1.6, alto=1.6, grosor=0.05, desfase=0.5)
    caja(red, 0, Y, 0, 30, 16, 8)
    caja(red, 2, Y - 2, 8, 34, 18, 7, inclina=0.0)
    caja(mat('suelo_bib_sea', 0x2a3038, 0.6), 2, Y - 2, 15, 34, 18, 0.4)
    caja(red, -2, Y + 1, 15.4, 28, 15, 8)
    caja(red, 3, Y - 1, 23.4, 24, 13, 6)
    caja(mat('suelo_bib_sea', 0x2a3038, 0.6), 3, Y - 1, 29.4, 24, 13, 0.4)
    caja(amarillo(), -9, Y - 8.1, 0, 3, 0.1, 3)
    texto(negro(), 'PUBLIC LIBRARY', 0, Y - 8.06, 3.2, tam=0.6, prof=0.03)

def cerdita_rachel():
    """Rachel, la cerdita hucha de bronce del mercado de Pike Place, sobre
    su peana (para la acera)."""
    caja(mat('peana_sea', 0x9a9488, 0.6), 0, 0, 0, 1.0, 1.6, 0.3)
    b = bronce()
    esfera(b, 0, 0, 0.85, 0.5, 2, esc=(0.95, 1.4, 0.95))
    esfera(b, 0, -0.68, 0.95, 0.3, 2, esc=(1, 0.9, 0.9))
    cil(b, 0, -0.98, 0.92, 0.13, 0.12, 12, eje='Y')
    for sx in (-1, 1):
        cil(b, sx * 0.14, -0.86, 1.18, 0.09, 0.14, 3, r2=0.0).rotation_euler = (0.4, 0, 0)
        for y in (-0.35, 0.4):
            cil(b, sx * 0.25, y, 0.3, 0.1, 0.3, 8)
    caja(negro(), 0, 0, 1.33, 0.06, 0.3, 0.03)
    rama(b, (0, 0.68, 0.95), (0, 0.85, 1.1), 0.04, 0.03, 6)

# ================================================================ por encima de la acera
def monorail():
    """El monorraíl de 1962 por encima de la acera de la izquierda: la viga
    de hormigón sobre sus pilares y el tren rojo y plateado encima.
    Va a lo largo de la calle: el origen en el centro."""
    L = 160
    X = -8.6
    h = hormigon()
    caja(h, X, 0, 7.0, 1.4, L, 1.4)
    for k in range(int(L / 20) + 1):
        y = -L / 2 + k * 20
        caja(h, X, y, 0, 1.0, 1.0, 7.0)
        caja(h, X, y, 6.4, 2.6, 1.2, 0.6)
    pl = plata()
    caja(pl, X, 10, 8.4, 3.0, 26, 2.6)
    caja(rojo(), X, 10, 8.4, 3.05, 26, 0.6)
    for y in range(0, 26, 3):
        for s in (-1, 1):
            caja(cristal(), X + s * 1.52, -2.5 + y, 9.4, 0.05, 2.2, 1.2)
    esfera(pl, X, -3.2, 9.7, 1.5, 2, esc=(1, 1.4, 0.9))
    caja(cristal(), X, -4.4, 9.9, 1.8, 0.1, 0.9)

# ================================================================ el mercado del pescado
def mercado_pescado():
    """Pike Place por dentro (momento estrella, cubierto a los lados): los
    puestos de pescado con sus camas de hielo y los salmones, los pescaderos
    con su peto naranja, los cubos de flores, los letreros rojos y los arcos
    de SALIDA y META. Cruza la calle: el origen en el centro."""
    L = 420
    caja(mat_bloques('suelo_mercado_sea', 0x8a7a6a, 0x5a4e44, ancho=0.4, alto=0.2, grosor=0.012, variacion=1.1), 0, 0, -0.2, 26, L, 0.2)
    for s in (-1, 1):
        # El soportal: los pilares, el tejado y la pared del fondo.
        caja(mat('pared_mercado_sea', 0xd8ccb4, 0.8), s * 13, 0, 0, 0.6, L, 7.5)
        caja(mat('tejado_mercado_sea', 0x4a4e58, 0.6), s * 10, 0, 6.5, 7.0, L, 0.4)
        for k in range(int(L / 6)):
            caja(verde(), s * 6.8, -L / 2 + 3 + k * 6, 0, 0.25, 0.25, 6.5)
        # Las camas de hielo con salmones.
        for k in range(int(L / 12)):
            y = -L / 2 + 6 + k * 12
            caja(madera_o(), s * 8.4, y, 0, 2.2, 9.0, 0.9)
            caja(hielo(), s * 8.4, y, 0.9, 2.1, 8.9, 0.18)
            for i in range(3):
                # (salmones sencillos: una pieza cada uno; con los de verdad salian 170.000 triangulos)
                o = esfera(salmon_m(), s * 8.3, y - 2.2 + i * 2.2, 1.2, 0.5, 1, esc=(0.75, 0.3, 0.32))
                o.rotation_euler = (0, 0, 0.3 * (i - 1))
            caja(blanco(), s * 7.2, y, 1.4, 0.04, 0.8, 0.5)
            caja(rojo(), s * 7.17, y, 1.55, 0.02, 0.5, 0.12)
        # Los pescaderos (peto naranja, botas) detrás de los puestos.
        for k in range(int(L / 18)):
            y = -L / 2 + 9 + k * 18
            cil(naranja(), s * 10.0, y, 0.0, 0.32, 1.45, 8)
            cil(blanco(), s * 10.0, y, 1.45, 0.3, 0.35, 8)
            esfera(piel(), s * 10.0, y, 2.05, 0.24, 1)
            rama(naranja(), (s * 10.0, y, 1.6), (s * 9.5, y, 2.35), 0.08, 0.07, 6)
        # Los letreros rojos colgados.
        for k in range(int(L / 35)):
            y = -L / 2 + 17 + k * 35
            caja(blanco(), s * 8.0, y, 5.0, 0.15, 6, 1.1)
            txt = ['PUBLIC MARKET', 'FRESH FISH', 'LOW FLYING FISH', 'MEAT & FISH'][k % 4]
            texto(neon_r(), txt, s * 8.0 - s * 0.1, y, 5.3, tam=0.5, prof=0.03).rotation_euler = (math.pi / 2, 0, -s * math.pi / 2)
        # Cubos de flores.
        for k in range(int(L / 24)):
            y = -L / 2 + 12 + k * 24
            for i in range(3):
                cil(gris(), s * 6.2, y + i * 0.8, 0, 0.3, 0.5, 10)
                esfera([rojo, amarillo, naranja][(k + i) % 3](), s * 6.2, y + i * 0.8, 0.75, 0.38, 1)
    for (y, txt) in ((-L / 2 + 1, 'SALIDA'), (L / 2 - 1, 'META')):
        for s in (-1, 1):
            caja(verde(), s * 6.8, y, 0, 0.4, 0.4, 6.4)
        caja(blanco(), 0, y, 5.0, 13.4, 0.3, 1.4)
        texto(neon_r(), 'PIKE PLACE · ' + txt, 0, y - 0.2, 5.35, tam=0.62, prof=0.04)

# ================================================================ obstáculos
def marquesina_lluvia():
    """La marquesina de cristal (no estorba: se va debajo y no te mojas):
    cuatro postes y el techo de cristal, de 14 m. El frente en el origen."""
    for y in (0.2, 7, 13.8):
        for s in (-1, 1):
            cil(hierro(), s * 1.08, y, 0, 0.06, 3.4, 8)
    caja(hierro(), 0, 7, 3.35, 2.4, 14, 0.12)
    caja(cristal_c(), 0, 7, 3.47, 2.3, 13.9, 0.06)
    for y in (0.2, 13.8):
        caja(hierro(), 0, y, 3.2, 2.3, 0.08, 0.15)

def cajon_hielo():
    """El cajón de pescado con hielo y salmones (se salta)."""
    caja(madera(), 0, 0, 0, 1.6, 0.8, 0.45)
    caja(hielo(), 0, 0, 0.45, 1.5, 0.7, 0.1)
    for i in range(3):
        salmon_pez(-0.45 + i * 0.45, 0, 0.6, 0.55, math.pi / 2 + (i - 1) * 0.2)
    caja(blanco(), 0, -0.41, 0.15, 0.6, 0.02, 0.2)
    texto(azul(), 'SALMON', 0, -0.42, 0.19, tam=0.11, prof=0.01)

def cartel_seattle():
    """La pancarta de España (agacharse): JUAN DE FUCA LLEGÓ EN 1592."""
    for x in (-1.25, 1.25):
        cil(madera_o(), x, 0, 0, 0.07, 2.75, 8)
    caja(bandera_es('pancarta_es_obst_sea', 1.5, 1.2), 0, 0, 1.5, 2.4, 0.05, 1.2)
    texto(negro(), 'JUAN DE FUCA', 0, -0.035, 2.2, tam=0.24, prof=0.02)
    texto(negro(), 'LLEGÓ EN 1592', 0, -0.035, 1.8, tam=0.22, prof=0.02)

def carrito_cafe():
    """El carrito del café expreso con su sombrilla (no se pasa)."""
    caja(mat('carrito_sea', 0x2a5a3a, 0.5), 0, 0.9, 0.3, 1.6, 1.8, 1.0)
    caja(madera(), 0, 0.9, 1.3, 1.7, 1.9, 0.08)
    for (x, y) in ((-0.65, 0.2), (0.65, 0.2), (-0.65, 1.6), (0.65, 1.6)):
        cil(negro(), x, y, 0, 0.15, 0.3, 10)
    cil(plata(), -0.3, 0.9, 1.38, 0.25, 0.5, 12)
    cil(negro(), 0.4, 0.9, 1.38, 0.08, 0.25, 8)
    cil(hierro(), 0, 0.9, 1.38, 0.04, 1.2, 6)
    cil(mat_franjas('sombrilla_sea', 0xc8202a, 0xf6f4ee, 6, eje='Z', z0=2.5, alto=0.7), 0, 0.9, 2.5, 1.3, 0.7, 12, r2=0.05)
    caja(blanco(), 0, -0.01, 0.65, 1.2, 0.02, 0.35)
    texto(rojo(), 'ESPRESSO', 0, -0.02, 0.72, tam=0.17, prof=0.01)

def tranvia_seattle():
    """El tranvía de South Lake Union (no se pasa): rojo, naranja y blanco,
    con la cabina mirando al jugador. El morro en el origen."""
    caja(blanco(), 0, 5.0, 0.35, 2.6, 9.6, 2.8)
    caja(naranja(), 0, 5.0, 0.35, 2.65, 9.6, 0.8)
    caja(rojo(), 0, 5.0, 1.15, 2.65, 9.6, 0.15)
    caja(cristal(), 0, 0.15, 1.6, 2.3, 0.1, 1.1)
    for y in range(1, 10, 2):
        for s in (-1, 1):
            caja(cristal(), s * 1.31, y + 0.5, 1.6, 0.05, 1.5, 1.0)
    caja(negro(), 0, 0.15, 2.85, 1.5, 0.06, 0.25)
    texto(amarillo(), 'S L U', 0, 0.1, 2.88, tam=0.18, prof=0.01)
    for s in (-1, 1):
        caja(luz('faro_tranvia_sea', 0xfff2c0, 1.0), s * 0.95, 0.12, 0.6, 0.35, 0.05, 0.2)
    caja(hierro(), 0, 5.0, 0, 2.2, 9.6, 0.35)
    rama(hierro(), (0, 4.5, 3.15), (0, 5.5, 4.0), 0.04, 0.04, 4)
    caja(hierro(), 0, 5.5, 4.0, 1.4, 0.1, 0.06)

def salmon():
    """El salmón que lanzan los pescaderos (vuela: la cabeza hacia -y)."""
    salmon_pez(0, 0, 0, 1.1)

PIEZAS = {
    'space_needle':      (space_needle,      'seattle',    dict(lado=2048, bisel=0.0)),
    'mercado_pike':      (mercado_pike,      'seattle',    dict(lado=1024, bisel=0.0)),
    'smith_tower':       (smith_tower,       'seattle',    dict(lado=1024, bisel=0.0)),
    'biblioteca_seattle': (biblioteca_seattle, 'seattle',  dict(lado=1024, bisel=0.0)),
    'cerdita_rachel':    (cerdita_rachel,    'seattle',    dict(lado=256, bisel=0.0)),
    'monorail':          (monorail,          'seattle',    dict(lado=1024, bisel=0.0, suelo=False)),
    'mercado_pescado':   (mercado_pescado,   'seattle',    dict(lado=2048, bisel=0.0, suelo=False)),
    'marquesina_lluvia': (marquesina_lluvia, 'obstaculos', dict(lado=256, bisel=0.0)),
    'cajon_hielo':       (cajon_hielo,       'obstaculos', dict(lado=256, bisel=0.0)),
    'cartel_seattle':    (cartel_seattle,    'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
    'carrito_cafe':      (carrito_cafe,      'obstaculos', dict(lado=256, bisel=0.0)),
    'tranvia_seattle':   (tranvia_seattle,   'obstaculos', dict(lado=256, bisel=0.0)),
    'salmon':            (salmon,            'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
}

correr(PIEZAS)
