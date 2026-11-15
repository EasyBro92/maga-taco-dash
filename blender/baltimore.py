# Nivel 41: Baltimore, Maryland (15/11/2026).
#
#   blender -b -P blender/baltimore.py -- [pieza ...] [--rapido]
#
# Historia: «Cangrejos que pellizcan los tobillos». Acto del Sentido Común. Por
#   Pratt Street junto al Inner Harbor: la torre del reloj, las casas de
#   ladrillo con sus escalones de mármol, el acuario con sus pirámides de
#   cristal y los bancos de «la mejor ciudad de América». Los cangrejos azules
#   cruzan la calle de lado y, si te pillan, se te agarran al tobillo (no
#   puedes saltar: sacúdetelos cambiando de carril); el momento estrella, las
#   banderas de señales en el muelle (memorizar los colores y pasar por ellos
#   en orden). Final en el fuerte McHenry, con la bandera gigante. Pancarta
#   del Sentido Común: LOS CANGREJOS PELLIZCAN.
# Obstáculos (carpeta obstaculos): el cangrejo azul, la olla de cangrejos, el
# camión de las especias y la pancarta.

import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import *

def blanco():    return mat('blanco_bal', 0xf6f4ee, 0.5)
def negro():     return mat('negro_bal', 0x1c1c20, 0.4)
def cristal():   return mat('cristal_bal', 0x3a6a80, 0.15)
def rojo():      return mat('rojo_bal', 0xc8202a, 0.45)
def azul():      return mat('azul_bal', 0x1e4a9a, 0.45)
def amarillo():  return mat('amarillo_bal', 0xf2c21a, 0.45)
def rosa():      return mat('rosa_bal', 0xf08aa8, 0.5)
def gris():      return mat('gris_bal', 0x8a9098, 0.4)
def hierro():    return mat('hierro_bal', 0x2a2c30, 0.45)
def madera():    return mat('madera_bal', 0x8a5a34, 0.85)
def madera_o():  return mat('madera_oscura_bal', 0x5a3a22, 0.85)
def ladrillo():  return mat_bloques('ladrillo_bal', 0xa85a3e, 0x7a4030, ancho=0.4, alto=0.16)
def marmol():    return mat('marmol_bal', 0xf2f0ea, 0.3)
def agua():      return mat('agua_bal', 0x3a5a7a, 0.15)
def cesped():    return mat('cesped_bal', 0x5a9a3a, 0.9)
def azul_c():    return mat('cangrejo_azul_bal', 0x4a7aa8, 0.5)

def cartel_sentido(x, y, z, w, h, linea1, linea2=''):
    caja(azul(), x, y, z, w, 0.06, h)
    caja(blanco(), x, y - 0.01, z + h - h * 0.08, w, 0.06, h * 0.08)
    esfera(rosa(), x - w / 2 + h * 0.32, y - 0.06, z + h * 0.5, h * 0.24, 1, esc=(1.2, 0.4, 1))
    texto(blanco(), linea1, x + h * 0.25, y - 0.045, z + h * (0.5 if not linea2 else 0.56), tam=h * 0.3, prof=0.02)
    if linea2:
        texto(amarillo(), linea2, x + h * 0.25, y - 0.045, z + h * 0.2, tam=h * 0.2, prof=0.02)

def cangrejo_m(x, y, z, k=1.0, cocido=False):
    """Un cangrejo azul (o rojo, cocido): el caparazón ancho, las pinzas y las patas."""
    c = rojo() if cocido else azul_c()
    esfera(c, x, y, z + 0.18 * k, 0.5 * k, 2, esc=(1.3, 0.75, 0.35))
    for s in (-1, 1):
        cil(c, x + s * 0.62 * k, y, z + 0.18 * k, 0.07 * k, 0.24 * k, 4, r2=0.0).rotation_euler = (0, s * math.pi / 2, 0)
        rama(c, (x + s * 0.35 * k, y - 0.2 * k, z + 0.2 * k), (x + s * 0.55 * k, y - 0.55 * k, z + 0.3 * k), 0.06 * k, 0.05 * k, 5)
        esfera(rojo() if not cocido else c, x + s * 0.58 * k, y - 0.65 * k, z + 0.32 * k, 0.15 * k, 1, esc=(0.8, 1.3, 0.7))
        for i in range(3):
            rama(c, (x + s * 0.4 * k, y + (0.05 + i * 0.12) * k, z + 0.15 * k), (x + s * 0.75 * k, y + (0.15 + i * 0.15) * k, z), 0.03 * k, 0.02 * k, 4)
        esfera(negro(), x + s * 0.1 * k, y - 0.32 * k, z + 0.32 * k, 0.05 * k, 1)

# ================================================================ la meta
def fuerte_mchenry():
    """El fuerte McHenry (la meta): la estrella de cinco puntas de muros de
    ladrillo con su terraplén de hierba, los cañones, el edificio de dentro y
    el mástil con la bandera gigante de quince estrellas; delante, la
    pancarta del Sentido Común."""
    Y = 30
    l = ladrillo()
    caja(agua(), 0, Y + 10, -0.3, 160, 60, 0.2)
    caja(cesped(), 0, Y - 8, -0.05, 100, 40, 0.06)
    for k in range(5):
        a = -math.pi / 2 + k * math.tau / 5
        b = a + math.tau / 5
        p0 = (math.cos(a) * 18, Y + math.sin(a) * 18)
        p1 = (math.cos(b) * 18, Y + math.sin(b) * 18)
        m0 = (math.cos(a + math.tau / 10) * 11, Y + math.sin(a + math.tau / 10) * 11)
        for (q0, q1) in ((p0, m0), (m0, p1)):
            rama(l, (q0[0], q0[1], 1.8), (q1[0], q1[1], 1.8), 1.8, 1.8, 4)
        caja(madera_o(), math.cos(a) * 16, Y + math.sin(a) * 16, 3.6, 0.5, 2.2, 0.5, giro=a)
        cil(negro(), math.cos(a) * 16.5, Y + math.sin(a) * 16.5, 4.0, 0.25, 2.2, 8, eje='Y').rotation_euler = (math.pi / 2, 0, a + math.pi / 2)
    caja(mat('cuartel_bal', 0xe0d4bc, 0.8), 0, Y + 4, 0, 14, 6, 5)
    tejado(mat('tejado_bal', 0x5a4a44, 0.6), 0, Y + 1, Y + 7, 5, 14, 2, cumbrera='x')
    cil(blanco(), 0, Y - 4, 0, 0.25, 26, 8)
    caja(mat_franjas('bandera_us_bal', 0xc8202a, 0xf6f4ee, 15, eje='Z', z0=16, alto=9), 7.5, Y - 4, 16, 15, 0.1, 9)
    caja(azul(), 3.0, Y - 4.08, 20.2, 6.0, 0.1, 4.8)
    for k in range(15):
        esfera(blanco(), 0.8 + (k % 5) * 1.1, Y - 4.15, 20.8 + (k // 5) * 1.4, 0.18, 1, esc=(1, 0.3, 1))
    caja(mat('camino_bal', 0xc8bca8, 0.9), 0, Y - 24, -0.04, 6, 20, 0.05)
    for x in (8, 22):
        cil(madera_o(), x, Y - 26, 0, 0.12, 4.4, 8)
    cartel_sentido(15, Y - 26, 2.8, 14, 1.6, 'LOS CANGREJOS PELLIZCAN', 'EL SENTIDO COMÚN')

# ================================================================ edificios
def torre_reloj_bal():
    """La torre del reloj de Baltimore (1911): la torre de ladrillo y piedra
    con los cuatro relojes grandes y BALTIMORE en lugar de la marca, y la
    linterna con su tejado."""
    Y = 8
    T = 9.0
    caja(mat('base_torre_bal', 0xd8d0c0, 0.7), 0, Y, 0, 14, 12, 6)
    caja(ladrillo(), 0, Y, 6, T, T, 34)
    for z in range(9, 34, 3):
        caja(cristal(), 0, Y - T / 2 - 0.05, z, 1.4, 0.1, 1.8)
    caja(mat('piedra_bal', 0xe8e0cc, 0.6), 0, Y, 40, T + 0.6, T + 0.6, 6)
    for (dx, dy, rz) in ((0, -1, 0), (-1, 0, 1), (1, 0, 1)):
        x, y = dx * (T / 2 + 0.35), Y + dy * (T / 2 + 0.35)
        o = cil(blanco(), x, y, 43, 2.4, 0.15, 24, eje='Y')
        if rz:
            o.rotation_euler = (math.pi / 2, 0, math.pi / 2)
        if dy == -1:
            for k, ch in enumerate('BALTIMORE'):
                a = math.pi / 2 + (k - 4) * 0.35
                texto(negro(), ch, x + math.cos(a) * 1.8, y - 0.12, 43 + math.sin(a) * 1.8 - 0.2, tam=0.4, prof=0.02)
            caja(negro(), x, y - 0.14, 43, 0.12, 0.04, 1.4)
    o = cil(mat('tejado_torre_bal', 0x4a6a5a, 0.5), 0, Y, 46, T * 0.72, 5, 4, r2=0.5)
    o.rotation_euler = (0, 0, math.pi / 4)
    cil(hierro(), 0, Y, 51, 0.08, 3, 6)

def casas_formstone():
    """Cuatro casas adosadas de Baltimore: estrechas, de ladrillo o de
    piedra falsa (formstone), con los escalones de mármol blanco y las
    mosquiteras pintadas en las ventanas."""
    Y = 7
    yf = Y - 5
    cols = [ladrillo, lambda: mat_bloques('formstone_bal', 0xb8a890, 0x8a7a68, ancho=0.7, alto=0.45, variacion=1.15), ladrillo,
            lambda: mat_bloques('formstone2_bal', 0xa89a8a, 0x7a6a5a, ancho=0.6, alto=0.4, variacion=1.15)]
    for k in range(4):
        x = -9 + k * 6
        caja(cols[k](), x, Y, 0, 5.8, 10, 9)
        caja(madera_o(), x, Y, 9, 6, 10.2, 0.5)
        for z in (3.4, 6.6):
            ventana(x - 1.2, z, 1.1, 1.8, y=yf - 0.05, marco=blanco(), cristal=mat('mosquitera_bal', 0x7ab0d0, 0.6))
            ventana(x + 1.4, z, 1.1, 1.8, y=yf - 0.05, marco=blanco(), cristal=mat('mosquitera_bal', 0x7ab0d0, 0.6))
        puerta(x - 1.2, 0.9, 1.0, 2.2, y=yf - 0.05, color=[0x2a4a9a, 0xc8202a, 0x2a6a3a, 0x1c1c20][k], marco=blanco())
        for i in range(3):
            caja(marmol(), x - 1.2, yf - 0.4 - i * 0.35, 0, 1.6, 0.35, 0.9 - i * 0.3)

def acuario():
    """El acuario nacional: el edificio de hormigón con las franjas de
    colores y los tejados de pirámides de cristal."""
    Y = 12
    caja(mat('hormigon_bal', 0xd0ccc4, 0.8), 0, Y, 0, 32, 20, 14)
    for (z, c) in ((3, rojo), (5, azul), (7, amarillo)):
        caja(c(), 0, Y - 10.05, z, 32, 0.1, 0.6)
    for (x, s) in ((-8, 10), (6, 13)):
        o = cil(cristal(), x, Y, 14, s, s * 0.8, 4, r2=0.2)
        o.rotation_euler = (0, 0, math.pi / 4)
    caja(blanco(), 0, Y - 10.1, 10.5, 16, 0.1, 1.4)
    texto(azul(), 'NATIONAL AQUARIUM', 0, Y - 10.16, 10.8, tam=0.85, prof=0.03)

def banco_baltimore():
    """El banco de Baltimore con su letrero de «la mejor ciudad de América»
    (para la acera)."""
    caja(madera(), 0, 0, 0.45, 2.0, 0.5, 0.08)
    caja(blanco(), 0, 0.25, 0.55, 2.0, 0.08, 0.6)
    texto(negro(), 'BALTIMORE', 0, 0.2, 0.95, tam=0.14, prof=0.005)
    texto(negro(), 'THE GREATEST CITY', 0, 0.2, 0.75, tam=0.1, prof=0.005)
    texto(negro(), 'IN AMERICA', 0, 0.2, 0.62, tam=0.1, prof=0.005)
    for x in (-0.85, 0.85):
        caja(hierro(), x, 0, 0, 0.08, 0.5, 0.45)

# ================================================================ cruza la calle
def arco_harbor():
    """El arco del Inner Harbor: dos postes de muelle con cuerdas y la
    pancarta INNER HARBOR · CHARM CITY; por detrás, CANGREJOS: CUIDADO."""
    for s in (-1, 1):
        cil(madera(), s * 8.6, 0, 0, 0.4, 7.8, 10)
        cil(blanco(), s * 8.6, 0, 7.8, 0.45, 0.2, 10)
    cil(madera(), 0, 0, 7.2, 0.35, 18.0, 10, eje='X')
    caja(azul(), 0, 0, 4.4, 12, 0.18, 1.8)
    texto(blanco(), 'INNER HARBOR', 0, -0.12, 5.25, tam=0.75, prof=0.04)
    texto(amarillo(), 'CHARM CITY', 0, -0.12, 4.6, tam=0.5, prof=0.04)
    o = texto(amarillo(), 'CANGREJOS: CUIDADO', 0, 0.12, 5.0, tam=0.6, prof=0.04)
    o.rotation_euler = (math.pi / 2, 0, math.pi)
    cangrejo_m(0, 0, 6.2, 2.0, cocido=True)

# ================================================================ el muelle
def muelle_harbor():
    """El muelle del Inner Harbor (momento estrella, al aire libre): el
    entarimado de madera, el agua a la derecha con el velero de guerra USS
    Constellation, los mástiles de las banderas de señales, los bolardos,
    las casas y los pabellones a la izquierda y los arcos de SALIDA y META.
    Cruza la calle: el origen en el centro."""
    L = 420
    caja(mat_bloques('tarima_bal', 0x9a7a5a, 0x6a5240, ancho=4.0, alto=0.25, grosor=0.02), 0, 0, -0.2, 24, L, 0.2)
    caja(agua(), 30, 0, -0.5, 36, L, 0.2)
    for k in range(int(L / 6)):
        cil(negro(), 11.5, -L / 2 + 3 + k * 6, 0, 0.22, 0.7, 8)
    for k in range(int(L / 25)):
        y = -L / 2 + 12 + k * 25
        cil(blanco(), 9.5, y, 0, 0.1, 9, 6)
        for i in range(4):
            caja([rojo, amarillo, azul, blanco][(k + i) % 4](), 10.3, y, 7.6 - i * 1.3, 1.4, 0.04, 1.0)
        cil(blanco(), -9.5, y + 12, 0, 0.1, 9, 6)
        for i in range(4):
            caja([azul, rojo, blanco, amarillo][(k + i) % 4](), -8.7, y + 12, 7.6 - i * 1.3, 1.4, 0.04, 1.0)
    # El velero (USS Constellation).
    for y in (-80, 120):
        esfera(negro(), 26, y, 1.0, 0.5, 2, esc=(8, 50, 3.5))
        caja(blanco(), 26, y, 2.2, 6, 40, 0.3)
        for dy in (-12, 0, 12):
            cil(madera_o(), 26, y + dy, 2.5, 0.35, 22, 8)
            for z in (10, 15, 19):
                caja(madera_o(), 26, y + dy, z, 12 - (z - 10) * 0.6, 0.25, 0.25)
    # Casas y pabellones a la izquierda.
    for k in range(int(L / 30)):
        y = -L / 2 + 15 + k * 30
        caja(mat(f'pabellon_bal{k % 3}', [0xd8c8a8, 0xa85a3e, 0xc8d0d8][k % 3], 0.7), -18, y, 0, 10, 24, 8 + (k % 3) * 3)
        caja(cristal(), -12.95, y, 1, 0.1, 20, 3)
        caja(mat_franjas(f'toldo_pab_bal{k % 2}', [0xc8202a, 0x1e4a9a][k % 2], 0xf6f4ee, 8, eje='Y', z0=-12, alto=24), -12.3, y, 3.5, 1.5, 22, 0.12)
    for (y, txt) in ((-L / 2 + 1, 'SALIDA'), (L / 2 - 1, 'META')):
        for s in (-1, 1):
            cil(madera(), s * 7.0, y, 0, 0.35, 6.2, 8)
        cil(madera(), 0, y, 5.6, 0.3, 14.6, 8, eje='X')
        caja(azul(), 0, y, 4.0, 9.5, 0.16, 1.4)
        texto(blanco(), 'SEÑALES · ' + txt, 0, y - 0.1, 4.45, tam=0.55, prof=0.04)

# ================================================================ obstáculos
def cangrejo():
    """El cangrejo azul de la bahía de Chesapeake (cruza de lado; si te pilla
    se te agarra al tobillo). Mira al jugador (-y)."""
    cangrejo_m(0, 0, 0, 1.0)

def olla_cangrejos():
    """La olla de cangrejos al vapor con la especia (se salta): la cazuela
    plateada con cangrejos rojos asomando."""
    cil(mat('olla_bal', 0xc8ccd0, 0.25), 0, 0, 0, 0.55, 0.75, 20)
    cil(hierro(), 0, 0, 0.75, 0.57, 0.05, 20)
    for s in (-1, 1):
        caja(hierro(), s * 0.6, 0, 0.55, 0.12, 0.1, 0.08)
    for k in range(3):
        a = k * 2.1
        cangrejo_m(math.cos(a) * 0.2, math.sin(a) * 0.2, 0.62, 0.35, cocido=True)
    caja(amarillo(), 0, -0.56, 0.25, 0.4, 0.02, 0.25)
    texto(azul(), 'CRABS', 0, -0.57, 0.3, tam=0.09, prof=0.005)

def camion_especias():
    """El camión de reparto de la especia de los cangrejos (no se pasa):
    amarillo y azul, con un cangrejo pintado. El morro en el origen."""
    a = amarillo()
    caja(a, 0, 1.0, 0.45, 2.4, 2.0, 1.7)
    caja(cristal(), 0, 0.0, 1.35, 2.1, 0.1, 0.7)
    caja(a, 0, 4.6, 0.45, 2.5, 5.2, 2.8)
    for s in (-1, 1):
        caja(azul(), s * 1.26, 4.6, 1.6, 0.05, 4.8, 1.2)
        cangrejo_m(s * 1.32, 4.6, 1.7, 0.9, cocido=True)
    caja(azul(), 0, -0.02, 0.7, 2.3, 0.05, 0.3)
    texto(amarillo(), 'SPICE', 0, -0.04, 0.75, tam=0.2, prof=0.01)
    for (y, s) in ((1.0, 1), (6.2, 1), (1.0, -1), (6.2, -1)):
        cil(negro(), s * 1.15, y, 0.42, 0.42, 0.3, 14, eje='X')
    for s in (-1, 1):
        caja(luz('faro_especias_bal', 0xfff2c0, 1.0), s * 0.85, -0.03, 1.0, 0.35, 0.05, 0.2)

def cartel_md():
    """La pancarta del Sentido Común (agacharse): LOS CANGREJOS PELLIZCAN."""
    for x in (-1.25, 1.25):
        cil(madera_o(), x, 0, 0, 0.07, 2.75, 8)
    caja(azul(), 0, 0, 1.5, 2.4, 0.05, 1.2)
    esfera(rosa(), -0.9, -0.05, 2.1, 0.2, 1, esc=(1.2, 0.4, 1))
    texto(blanco(), 'LOS CANGREJOS', 0.15, -0.035, 2.2, tam=0.18, prof=0.02)
    texto(amarillo(), 'PELLIZCAN', 0.15, -0.035, 1.8, tam=0.24, prof=0.02)

PIEZAS = {
    'fuerte_mchenry':   (fuerte_mchenry,   'baltimore',  dict(lado=2048, bisel=0.0)),
    'torre_reloj_bal':  (torre_reloj_bal,  'baltimore',  dict(lado=1024, bisel=0.0)),
    'casas_formstone':  (casas_formstone,  'baltimore',  dict(lado=1024, bisel=0.0)),
    'acuario':          (acuario,          'baltimore',  dict(lado=1024, bisel=0.0)),
    'banco_baltimore':  (banco_baltimore,  'baltimore',  dict(lado=256, bisel=0.0)),
    'arco_harbor':      (arco_harbor,      'baltimore',  dict(lado=1024, bisel=0.0, suelo=False)),
    'muelle_harbor':    (muelle_harbor,    'baltimore',  dict(lado=2048, bisel=0.0, suelo=False)),
    'cangrejo':         (cangrejo,         'obstaculos', dict(lado=256, bisel=0.0)),
    'olla_cangrejos':   (olla_cangrejos,   'obstaculos', dict(lado=256, bisel=0.0)),
    'camion_especias':  (camion_especias,  'obstaculos', dict(lado=256, bisel=0.0)),
    'cartel_md':        (cartel_md,        'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
}

correr(PIEZAS)
