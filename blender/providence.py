# Nivel 49: Providence, Rhode Island (16/11/2026).
#
#   blender -b -P blender/providence.py -- [pieza ...] [--rapido]
#
# Historia: «El estado más pequeño y el nivel más corto. Él dice que es
#   enorme, tremendo». Acto del Sentido Común. Por Westminster Street: el
#   edificio del bicho azul gigante en el tejado, la galería comercial más
#   antigua del país, el rascacielos «de Superman», los braseros de
#   WaterFire en la acera y, cruzando la calle, el arco de la piña de Federal
#   Hill. Lo pequeño: el jugador se encoge y pasa por debajo de los coches
#   (deslizándose); el momento estrella, el examen de la Universidad de
#   Brown (preguntas sobre Rhode Island: se contesta por el carril).
#   Final en el Capitolio de mármol con el Hombre Independiente en lo alto.
#   Pancarta del Sentido Común: LO PEQUEÑO TAMBIÉN VALE.
# Obstáculos (carpeta obstaculos): el arco del examen, el bicho azul (no se
# pasa ni por debajo) y la pancarta.

import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import *

def blanco():    return mat('blanco_pvd', 0xf6f4ee, 0.5)
def negro():     return mat('negro_pvd', 0x1c1c20, 0.4)
def cristal():   return mat('cristal_pvd', 0x3a5a70, 0.15)
def rojo():      return mat('rojo_pvd', 0xc8302a, 0.5)
def azul():      return mat('azul_pvd', 0x1e4a9a, 0.45)
def azul_bicho(): return mat('azul_bicho_pvd', 0x2a7ad8, 0.4)
def amarillo():  return mat('amarillo_pvd', 0xf2c21a, 0.45)
def oro():       return mat('oro_pvd', 0xe8b840, 0.22)
def rosa():      return mat('rosa_pvd', 0xf08aa8, 0.5)
def verde():     return mat('verde_pvd', 0x2a6a3a, 0.6)
def madera_o():  return mat('madera_oscura_pvd', 0x5a3a22, 0.85)
def hierro():    return mat('hierro_pvd', 0x2a2c30, 0.45)
def marmol():    return mat_bloques('marmol_pvd', 0xf0ece4, 0xd8d2c8, ancho=1.2, alto=0.6, grosor=0.006)
def marmol_l():  return mat('marmol_liso_pvd', 0xf4f0e8, 0.45)
def granito():   return mat_bloques('granito_pvd', 0xb8b4aa, 0x9a968c, ancho=1.2, alto=0.6, grosor=0.008)
def ladrillo():  return mat_bloques('ladrillo_pvd', 0xa04a32, 0x7a3828, ancho=0.4, alto=0.16)
def cesped():    return mat('cesped_pvd', 0x5a9a3a, 0.9)
def fuego():     return luz('fuego_pvd', 0xffa040, 1.5)
def farol():     return luz('farol_pvd', 0xfff0b0, 1.2)

def cartel_sentido(x, y, z, w, h, linea1, linea2=''):
    caja(azul(), x, y, z, w, 0.06, h)
    caja(blanco(), x, y - 0.01, z + h - h * 0.08, w, 0.06, h * 0.08)
    esfera(rosa(), x - w / 2 + h * 0.32, y - 0.06, z + h * 0.5, h * 0.24, 1, esc=(1.2, 0.4, 1))
    texto(blanco(), linea1, x + h * 0.25, y - 0.045, z + h * (0.5 if not linea2 else 0.56), tam=h * 0.3, prof=0.02)
    if linea2:
        texto(amarillo(), linea2, x + h * 0.25, y - 0.045, z + h * 0.2, tam=h * 0.2, prof=0.02)

def brasero(x, y, z=0, k=1.0):
    """Un brasero de WaterFire: el poste, la cesta de hierro y la llama."""
    cil(hierro(), x, y, z, 0.06 * k, 1.6 * k, 6)
    cil(hierro(), x, y, z + 1.6 * k, 0.45 * k, 0.4 * k, 8, r2=0.6 * k)
    for i in range(3):
        cil(fuego(), x + (i - 1) * 0.15 * k, y, z + 1.95 * k, 0.22 * k, (0.7 - abs(i - 1) * 0.2) * k, 6, r2=0.02 * k)

def bicho_m(x, y, z, k=1.0):
    """El bicho azul (la termita gigante): el cuerpo de tres partes, los ojos
    grandes, las antenas y las seis patas."""
    b = azul_bicho()
    esfera(b, x, y + 1.2 * k, z + 0.9 * k, 0.9 * k, 2, esc=(1, 1.4, 0.8))
    esfera(b, x, y, z + 0.95 * k, 0.6 * k, 2, esc=(1, 0.9, 0.85))
    esfera(b, x, y - 0.9 * k, z + 1.1 * k, 0.55 * k, 2)
    for s in (-1, 1):
        esfera(blanco(), x + s * 0.25 * k, y - 1.3 * k, z + 1.3 * k, 0.2 * k, 2)
        esfera(negro(), x + s * 0.27 * k, y - 1.47 * k, z + 1.33 * k, 0.09 * k, 1)
        rama(b, (x + s * 0.15 * k, y - 1.1 * k, z + 1.55 * k), (x + s * 0.5 * k, y - 1.6 * k, z + 2.3 * k), 0.05 * k, 0.03 * k, 6)
        for j in range(3):
            yy = y + (-0.3 + j * 0.45) * k
            rama(b, (x + s * 0.4 * k, yy, z + 0.8 * k), (x + s * 1.1 * k, yy - 0.1 * k, z + 0.9 * k), 0.08 * k, 0.07 * k, 6)
            rama(b, (x + s * 1.1 * k, yy - 0.1 * k, z + 0.9 * k), (x + s * 1.3 * k, yy, z), 0.07 * k, 0.05 * k, 6)
    for s in (-1, 1):
        caja(mat('ala_pvd', 0xb8d8f0, 0.2), x + s * 0.5 * k, y + 1.2 * k, z + 1.5 * k, 0.9 * k, 1.6 * k, 0.04 * k, giro=s * 0.2)

# ================================================================ la meta
def capitolio_ri():
    """El Capitolio de Rhode Island (la meta): mármol blanco de Georgia, el
    pórtico de columnas, las cuatro torrecillas y la gran cúpula de mármol
    con el Hombre Independiente dorado en lo alto; delante, el césped y la
    pancarta del Sentido Común."""
    Y = 28
    W, D, H = 60.0, 24.0, 16.0
    yf = Y - D / 2
    m = marmol()
    caja(cesped(), 0, Y - 12, -0.05, 100, 64, 0.06)
    caja(m, 0, Y, 0, W, D, H)
    caja(marmol_l(), 0, Y, H, W + 0.6, D + 0.6, 1.0)
    for k in range(13):
        x = -27 + k * 4.5
        for z in (2.0, 9.0):
            ventana(x, z, 1.6, 3.0, y=yf - 0.05, marco=marmol_l(), cristal=cristal())
    caja(marmol_l(), 0, yf - 4, 0, 20, 8, 1.2)
    for x in (-8, -4.8, -1.6, 1.6, 4.8, 8):
        cil(marmol_l(), x, yf - 7.2, 1.2, 0.7, 12, 16)
    caja(marmol_l(), 0, yf - 4, 13.2, 20.4, 8.4, 1.4)
    fronton(marmol_l(), 0, yf - 8.2, 14.6, 20.4, 3.6, 0.9)
    for (x, y) in ((-14, yf - 2), (14, yf - 2)):
        caja(m, x, y, H + 1, 4, 4, 4)
        cil(marmol_l(), x, y, H + 5, 2.0, 3, 12)
        cupula(marmol_l(), x, y, H + 8, 2.0, 2.0, 12, 4)
    Z = H + 1.0
    cil(m, 0, Y, Z, 11, 7, 28)
    for k in range(20):
        a = k * math.tau / 20
        cil(marmol_l(), math.cos(a) * 11.2, Y + math.sin(a) * 11.2, Z, 0.45, 7, 10)
    cil(marmol_l(), 0, Y, Z + 7, 11.6, 1.2, 28)
    cil(m, 0, Y, Z + 8.2, 9.5, 3, 28)
    cupula(marmol_l(), 0, Y, Z + 11.2, 9.5, 9, 28, 10)
    cil(marmol_l(), 0, Y, Z + 20, 2.2, 3.6, 12)
    cupula(marmol_l(), 0, Y, Z + 23.6, 2.2, 1.4, 12, 4)
    g = oro()
    cil(g, 0, Y, Z + 25, 0.35, 1.6, 8)
    esfera(g, 0, Y, Z + 27.0, 0.35, 1)
    rama(g, (0, Y, Z + 26.4), (0.6, Y - 0.2, Z + 27.6), 0.12, 0.08, 6)
    rama(g, (0.6, Y - 0.2, Z + 27.6), (0.7, Y - 0.2, Z + 28.6), 0.05, 0.05, 6)
    for x in (8, 22):
        cil(madera_o(), x, yf - 16, 0, 0.12, 4.4, 8)
    cartel_sentido(15, yf - 16, 2.8, 15, 1.6, 'LO PEQUEÑO TAMBIÉN VALE', 'EL SENTIDO COMÚN')

# ================================================================ edificios
def bicho_azul_edificio():
    """El edificio del bicho azul: la oficina de los exterminadores, de
    ladrillo, con la termita azul gigante (con sus alas) en el tejado."""
    Y = 8
    W, D, H = 16.0, 12.0, 7.0
    yf = Y - D / 2
    caja(ladrillo(), 0, Y, 0, W, D, H)
    caja(blanco(), 0, Y, H, W + 0.4, D + 0.4, 0.4)
    for x in (-5, 0, 5):
        ventana(x, 3.0, 2.0, 2.4, y=yf - 0.05, marco=blanco(), cristal=cristal())
    puerta(-5, 0, 1.6, 2.4, y=yf - 0.05)
    caja(blanco(), 2, yf - 0.1, 5.5, 9, 0.1, 1.0)
    texto(azul(), 'FUERA BICHOS', 2, yf - 0.16, 5.7, tam=0.5, prof=0.02)
    bicho_m(0, Y, H + 0.4, 3.2)

def arcade_ri():
    """La galería comercial más antigua del país (1828): granito, el
    pórtico de seis columnas jónicas, el frontón y THE ARCADE."""
    Y = 9
    W, D, H = 20.0, 18.0, 11.0
    yf = Y - D / 2
    g = granito()
    caja(g, 0, Y, 0, W, D, H)
    caja(g, 0, yf - 0.5, 0, 16, 1, 1.0)
    for k in range(6):
        cil(g, -6.25 + k * 2.5, yf - 2.2, 1.0, 0.5, 8.0, 16)
    caja(g, 0, yf - 1.6, 9.0, 16.4, 3.4, 1.2)
    fronton(g, 0, yf - 3.3, 10.2, 16.4, 3.0, 0.8)
    caja(cristal(), 0, yf - 0.05, 1.0, 6, 0.1, 6)
    texto(negro(), 'THE ARCADE · 1828', 0, yf - 3.35, 9.3, tam=0.55, prof=0.03)

def torre_superman():
    """El rascacielos «de Superman» (1928): art déco de piedra clara, los
    escalonamientos, la linterna de arriba y la antena."""
    Y = 10
    p = mat_bloques('piedra_deco_pvd', 0xd8ccb0, 0xb8ac90, ancho=1.0, alto=0.5, grosor=0.008)
    caja(p, 0, Y, 0, 20, 18, 30)
    caja(p, 0, Y, 30, 16, 14, 30)
    caja(p, 0, Y, 60, 12, 10, 18)
    caja(p, 0, Y, 78, 7, 7, 6)
    cil(p, 0, Y, 84, 2.5, 4, 8)
    cil(hierro(), 0, Y, 88, 0.15, 8, 6)
    for z in range(4, 76, 4):
        w = 20 if z < 30 else 16 if z < 60 else 12
        for k in range(int(w / 2.5)):
            caja(cristal(), -w / 2 + 1.25 + k * 2.5, Y - (9 if z < 30 else 7 if z < 60 else 5) - 0.05, z, 0.9, 0.1, 2.4)

def brasero_acera():
    """El brasero de WaterFire de la acera (sin río: para que se vea)."""
    brasero(0, 0, 0, 1.0)

# ================================================================ cruza la calle
def arco_federal_hill():
    """El arco de Federal Hill sobre Atwells Avenue: los dos pilares, el
    arco de hierro y la piña (la pigna) colgada en el centro."""
    for s in (-1, 1):
        caja(granito(), s * 8.5, 0, 0, 1.2, 1.2, 6.5)
    n = 20
    for k in range(n):
        u0, u1 = k / n, (k + 1) / n
        rama(hierro(), (-8.5 + 17 * u0, 0, 6.5 + 2.5 * math.sin(math.pi * u0)), (-8.5 + 17 * u1, 0, 6.5 + 2.5 * math.sin(math.pi * u1)), 0.15, 0.15, 6)
    cil(hierro(), 0, 0, 7.6, 0.03, 1.4, 4)
    pi = mat('pigna_pvd', 0x8a6a2a, 0.5)
    esfera(pi, 0, 0, 7.0, 0.55, 2, esc=(1, 1, 1.4))
    for k in range(12):
        a = k * math.tau / 12
        esfera(oro(), math.cos(a) * 0.5, math.sin(a) * 0.5, 6.7 + (k % 3) * 0.3, 0.12, 1)
    caja(verde(), 0, -0.1, 4.6, 7, 0.08, 0.9)
    texto(blanco(), 'FEDERAL HILL', 0, -0.15, 4.8, tam=0.5, prof=0.02)

# ================================================================ el patio de Brown
def patio_brown():
    """El patio de la Universidad de Brown (momento estrella): el camino de
    ladrillo (la calle), el césped, los edificios de ladrillo a los dos lados
    con sus ventanas y tejados, los olmos, los faroles y la torre del reloj.
    Cruza la calle: el origen en el centro. (360 m: el nivel es corto.)"""
    L = 360
    caja(mat_bloques('suelo_ladrillo_pvd', 0xa85a3e, 0x7a4030, ancho=0.4, alto=0.2, grosor=0.015), 0, 0, -0.2, 17, L, 0.2)
    caja(cesped(), 0, 0, -0.21, 120, L, 0.2)
    l = ladrillo()
    for s in (-1, 1):
        for k in range(int(L / 42)):
            y = -L / 2 + 21 + k * 42
            caja(l, s * 24, y, 0, 12, 34, 12)
            tejado(mat('tejado_brown_pvd', 0x4a4a52, 0.6), s * 24, y - 17, y + 17, 12, 12, 3, cumbrera='y')
            for j in range(6):
                for z in (2, 6, 9.5):
                    caja(cristal(), s * 17.95, y - 14 + j * 5.6, z, 0.1, 1.4, 2.2)
        for k in range(int(L / 18)):
            y = -L / 2 + 9 + k * 18
            x = s * (11 + (k % 2) * 2)
            cil(madera_o(), x, y, 0, 0.35, 4, 8)
            esfera(mat('olmo_pvd', 0x3a7a3a, 0.8), x, y, 6, 2.6, 1, esc=(1, 1, 0.85))
        for k in range(int(L / 24)):
            y = -L / 2 + 12 + k * 24
            cil(negro(), s * 7.2, y, 0, 0.08, 3.6, 6)
            esfera(farol(), s * 7.2, y, 3.7, 0.22, 1)
    for y in (-60, 100):
        caja(l, -16, y, 0, 5, 5, 22)
        for s in (-1, 1):
            cil(blanco(), -16 + s * 2.55, y, 16, 1.0, 0.1, 16, eje='X')
        cil(blanco(), -16, y - 2.55, 16, 1.0, 0.1, 16, eje='Y')
        o = cil(mat('tejado_brown_pvd', 0x4a4a52, 0.6), -16, y, 22, 3.8, 4, 4, r2=0.2)
        o.rotation_euler = (0, 0, math.pi / 4)
    for (y, txt) in ((-L / 2 + 1, 'EXAMEN'), (L / 2 - 1, 'APROBADO')):
        for s in (-1, 1):
            caja(l, s * 7.2, y, 0, 1.0, 1.0, 6)
        caja(mat('marron_pvd', 0x5a2a1a, 0.6), 0, y, 5.4, 15.4, 0.6, 1.0)
        texto(blanco(), 'BROWN · ' + txt, 0, y - 0.32, 5.6, tam=0.6, prof=0.04)

# ================================================================ obstáculos
def arco_examen():
    """El arco del examen (el juego pone la pregunta y las respuestas): los
    dos postes, el travesaño marrón con BROWN, las dos pizarras en blanco
    sobre los carriles de los lados y el ¿? del medio."""
    for s in (-1, 1):
        cil(hierro(), s * 4.0, 0, 0, 0.18, 6.4, 8)
    caja(mat('marron_pvd', 0x5a2a1a, 0.6), 0, 0, 5.8, 8.6, 0.3, 0.6)
    texto(blanco(), 'BROWN · EXAMEN', 0, -0.17, 5.9, tam=0.35, prof=0.02)
    for x in (-2.2, 2.2):
        caja(negro(), x, 0, 3.75, 3.6, 0.12, 1.65)
    caja(amarillo(), 0, 0, 4.0, 0.8, 0.12, 1.1)
    texto(negro(), '¿?', 0, -0.07, 4.2, tam=0.6, prof=0.02)

def bicho_azul():
    """El bicho azul de juguete gigante en la calle (no se pasa: ni por
    debajo, que no tiene hueco)."""
    bicho_m(0, 0.6, 0, 0.9)

def cartel_ri():
    """La pancarta del Sentido Común (agacharse): LO PEQUEÑO TAMBIÉN VALE."""
    for x in (-1.25, 1.25):
        cil(madera_o(), x, 0, 0, 0.07, 2.75, 8)
    caja(azul(), 0, 0, 1.5, 2.4, 0.05, 1.2)
    esfera(rosa(), -0.9, -0.05, 2.1, 0.2, 1, esc=(1.2, 0.4, 1))
    texto(blanco(), 'LO PEQUEÑO', 0.15, -0.035, 2.2, tam=0.2, prof=0.02)
    texto(amarillo(), 'TAMBIÉN VALE', 0.15, -0.035, 1.8, tam=0.2, prof=0.02)

PIEZAS = {
    'capitolio_ri':        (capitolio_ri,        'providence', dict(lado=2048, bisel=0.0)),
    'bicho_azul_edificio': (bicho_azul_edificio, 'providence', dict(lado=1024, bisel=0.0)),
    'arcade_ri':           (arcade_ri,           'providence', dict(lado=1024, bisel=0.0)),
    'torre_superman':      (torre_superman,      'providence', dict(lado=1024, bisel=0.0)),
    'brasero_acera':       (brasero_acera,       'providence', dict(lado=256, bisel=0.0)),
    'arco_federal_hill':   (arco_federal_hill,   'providence', dict(lado=1024, bisel=0.0, suelo=False)),
    'patio_brown':         (patio_brown,         'providence', dict(lado=2048, bisel=0.0, suelo=False)),
    'arco_examen':         (arco_examen,         'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
    'bicho_azul':          (bicho_azul,          'obstaculos', dict(lado=256, bisel=0.0)),
    'cartel_ri':           (cartel_ri,           'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
}

correr(PIEZAS)
