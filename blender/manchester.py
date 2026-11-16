# Nivel 48: Manchester, Nuevo Hampshire (16/11/2026).
#
#   blender -b -P blender/manchester.py -- [pieza ...] [--rapido]
#
# Historia: «La primera nevada. El lema del estado: Vive libre o muere». Acto
#   del Sentido Común. Por Elm Street con la primera nevada: el teatro Palace
#   con su marquesina, el ayuntamiento gótico con su torre, el diner de las
#   primarias (aquí empiezan) y, cruzando la calle, la matrícula gigante
#   VIVE LIBRE O MUERE. La guerra de bolas de nieve: los niños asoman de sus
#   fuertes y tiran (la sombra dice dónde cae); tocando a tiempo les das tú
#   primero. El momento estrella, el debate de las primarias: el otro
#   candidato lanza promesas y hay que devolverlas tocando justo cuando
#   llegan (¡FAKE NEWS!). Final en los molinos de Amoskeag con su torre del reloj.
#   Pancarta del Sentido Común: ABRÍGATE, QUE NIEVA.
# Obstáculos (carpeta obstaculos): el fuerte de nieve, el niño del gorro, el
# otro candidato con su atril y la pancarta.

import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import *

def blanco():    return mat('blanco_mht', 0xf6f4ee, 0.5)
def nieve():     return mat('nieve_mht', 0xf4f8fc, 0.7)
def negro():     return mat('negro_mht', 0x1c1c20, 0.4)
def cristal():   return mat('cristal_mht', 0x3a5a70, 0.15)
def rojo():      return mat('rojo_mht', 0xc8302a, 0.5)
def azul():      return mat('azul_mht', 0x1e4a9a, 0.45)
def amarillo():  return mat('amarillo_mht', 0xf2c21a, 0.45)
def rosa():      return mat('rosa_mht', 0xf08aa8, 0.5)
def verde():     return mat('verde_mht', 0x1e6a3a, 0.5)
def naranja():   return mat('naranja_mht', 0xe8782a, 0.5)
def madera():    return mat('madera_mht', 0x9a6a3e, 0.85)
def madera_o():  return mat('madera_oscura_mht', 0x5a3a22, 0.85)
def piedra():    return mat_bloques('piedra_mht', 0xb8b4a8, 0x9a968c, ancho=1.0, alto=0.5, grosor=0.01)
def ladrillo():  return mat_bloques('ladrillo_mht', 0xa04a32, 0x7a3828, ancho=0.4, alto=0.16)
def pino():      return mat('pino_mht', 0x1e4a32, 0.8)
def piel():      return mat('piel_mht', 0xf0c8a8, 0.6)
def bombilla():  return luz('bombilla_mht', 0xffe6a0, 1.3)

def cartel_sentido(x, y, z, w, h, linea1, linea2=''):
    caja(azul(), x, y, z, w, 0.06, h)
    caja(blanco(), x, y - 0.01, z + h - h * 0.08, w, 0.06, h * 0.08)
    esfera(rosa(), x - w / 2 + h * 0.32, y - 0.06, z + h * 0.5, h * 0.24, 1, esc=(1.2, 0.4, 1))
    texto(blanco(), linea1, x + h * 0.25, y - 0.045, z + h * (0.5 if not linea2 else 0.56), tam=h * 0.3, prof=0.02)
    if linea2:
        texto(amarillo(), linea2, x + h * 0.25, y - 0.045, z + h * 0.2, tam=h * 0.2, prof=0.02)

def pino_nevado(x, y, k=1.0):
    cil(madera_o(), x, y, 0, 0.22 * k, 1.0 * k, 6)
    for i, (r, z, h) in enumerate(((1.8, 0.8, 2.4), (1.4, 2.4, 2.2), (0.9, 3.9, 2.0))):
        cil(pino(), x, y, z * k, r * k, h * k, 7, r2=0.1 * k)
        cil(nieve(), x, y, (z + h * 0.55) * k, r * 0.5 * k, h * 0.45 * k, 7, r2=0.05 * k)

def nino_m(x, y, z, k=1.0, gorro=None):
    """Un niño abrigado: la cabeza con el gorro de pompón, la bufanda y el
    brazo levantado con la bola de nieve."""
    ab = mat('abrigo_nino_mht', 0x2a6ac8, 0.7)
    esfera(ab, x, y, z + 0.35 * k, 0.32 * k, 2, esc=(1, 0.9, 1.1))
    esfera(rojo(), x, y, z + 0.66 * k, 0.2 * k, 1, esc=(1.1, 1.1, 0.5))
    esfera(piel(), x, y, z + 0.85 * k, 0.22 * k, 2)
    for s in (-1, 1):
        esfera(negro(), x + s * 0.08 * k, y - 0.2 * k, z + 0.88 * k, 0.03 * k, 1)
    g = (gorro or rojo)()
    esfera(g, x, y, z + 0.95 * k, 0.23 * k, 2, mitad=True)
    esfera(blanco(), x, y, z + 1.2 * k, 0.08 * k, 1)
    rama(ab, (x + 0.25 * k, y, z + 0.5 * k), (x + 0.45 * k, y + 0.05 * k, z + 1.0 * k), 0.08 * k, 0.07 * k, 6)
    esfera(nieve(), x + 0.47 * k, y + 0.05 * k, z + 1.12 * k, 0.11 * k, 1)

# ================================================================ la meta
def molinos_amoskeag():
    """Los molinos de Amoskeag (la meta): la nave larguísima de ladrillo
    junto al río, las filas de ventanas, la torre del reloj en el centro con
    su tejado de pirámide, la chimenea, la nieve en los tejados y la
    pancarta del Sentido Común."""
    Y = 24
    W, D, H = 70.0, 14.0, 16.0
    yf = Y - D / 2
    l = ladrillo()
    caja(nieve(), 0, Y - 12, -0.05, 100, 60, 0.06)
    caja(l, 0, Y, 0, W, D, H)
    caja(nieve(), 0, Y, H, W + 0.4, D + 0.4, 0.4)
    for k in range(23):
        x = -33 + k * 3
        if abs(x) < 4:
            continue
        for z in (1.5, 5.5, 9.5, 13.0):
            caja(cristal(), x, yf - 0.05, z, 1.3, 0.1, 2.2)
    caja(l, 0, yf - 1, 0, 8, 8, H + 10)
    for s in (-1, 1):
        cil(blanco(), s * 4.05, yf - 1, H + 6.5, 1.6, 0.1, 20, eje='X')
        cil(negro(), s * 4.1, yf - 1, H + 6.5, 0.12, 0.1, 8, eje='X')
    cil(blanco(), 0, yf - 5.05, H + 6.5, 1.6, 0.1, 20, eje='Y')
    rama(negro(), (0, yf - 5.12, H + 6.5), (0, yf - 5.12, H + 7.6), 0.07, 0.05, 4)
    rama(negro(), (0, yf - 5.12, H + 6.5), (0.8, yf - 5.12, H + 6.5), 0.07, 0.05, 4)
    o = cil(mat('tejado_mht', 0x4a5a5a, 0.5), 0, yf - 1, H + 10, 6.0, 5, 4, r2=0.2)
    o.rotation_euler = (0, 0, math.pi / 4)
    cil(nieve(), 0, yf - 1, H + 10, 5.4, 2.0, 4, r2=3.0).rotation_euler = (0, 0, math.pi / 4)
    puerta(0, 0, 3, 4.2, y=yf - 5.05)
    cil(l, 28, Y + 9, 0, 1.8, 34, 16, r2=1.3)
    caja(blanco(), 0, yf - 5.1, 4.6, 10, 0.1, 1.2)
    texto(rojo(), 'AMOSKEAG', 0, yf - 5.16, 4.85, tam=0.8, prof=0.03)
    for x in (8, 22):
        cil(madera_o(), x, yf - 16, 0, 0.12, 4.4, 8)
    cartel_sentido(15, yf - 16, 2.8, 14, 1.6, 'ABRÍGATE, QUE NIEVA', 'EL SENTIDO COMÚN')
    for (x, y) in ((-30, Y - 20), (-22, Y - 26), (30, Y - 24)):
        pino_nevado(x, y, 1.4)

# ================================================================ edificios
def teatro_palace():
    """El teatro Palace (1915): ladrillo y piedra clara, la marquesina
    triangular con bombillas y el cartel PALACE vertical; nieve arriba."""
    Y = 8
    W, D, H = 18.0, 14.0, 13.0
    yf = Y - D / 2
    caja(ladrillo(), 0, Y, 0, W, D, H)
    caja(nieve(), 0, Y, H, W + 0.4, D + 0.4, 0.35)
    caja(piedra(), 0, yf - 0.1, 0, W, 0.3, 3.5)
    for x in (-6, -2, 2, 6):
        for z in (6, 9.5):
            ventana(x, z, 1.4, 2.2, y=yf - 0.05, marco=blanco(), cristal=cristal())
    caja(negro(), 0, yf - 1.6, 3.6, 12, 3.2, 1.4)
    for k in range(20):
        esfera(bombilla(), -5.7 + k * 0.6, yf - 3.25, 3.75, 0.08, 1)
    caja(blanco(), 0, yf - 3.22, 4.0, 11, 0.06, 0.8)
    texto(rojo(), 'ESTA NOCHE: LA PRIMARIA', 0, yf - 3.27, 4.2, tam=0.4, prof=0.02)
    caja(rojo(), 0, yf - 1.0, 6, 1.4, 0.4, 7)
    for i, ch in enumerate('PALACE'):
        texto(amarillo(), ch, 0, yf - 1.22, 11.8 - i * 1.0, tam=0.75, prof=0.03)

def city_hall_mht():
    """El ayuntamiento de Manchester (1845): gótico, de ladrillo con piedra,
    la torre cuadrada de la entrada con su aguja y las ventanas en arco."""
    Y = 9
    W, D, H = 20.0, 16.0, 11.0
    yf = Y - D / 2
    caja(ladrillo(), 0, Y, 0, W, D, H)
    tejado(mat('tejado_ch_mht', 0x4a4a52, 0.6), 0, Y - D / 2, Y + D / 2, H, W, 3.5, cumbrera='x')
    caja(nieve(), 0, Y - 2, H + 1.6, W + 0.6, 4.4, 0.25, inclina=0.42)
    for k in range(5):
        x = -8 + k * 4
        for z in (1.5, 6.0):
            caja(cristal(), x, yf - 0.05, z, 1.4, 0.1, 2.6)
            cil(cristal(), x, yf - 0.05, z + 2.6, 0.7, 0.1, 12, eje='Y')
    caja(piedra(), 0, yf - 2.5, 0, 5.5, 5, H + 9)
    for z in (H + 3, H + 6):
        caja(cristal(), 0, yf - 5.05, z, 1.2, 0.1, 2)
    cil(mat('aguja_mht', 0x4a4a52, 0.5), 0, yf - 2.5, H + 9, 3.6, 8, 4, r2=0.1).rotation_euler = (0, 0, math.pi / 4)
    puerta(0, 0, 2.4, 3.6, y=yf - 5.05)

def diner_flecha():
    """El diner de las primarias (aquí paran todos los candidatos): el vagón
    de acero brillante con la franja roja, la flecha roja gigante con
    bombillas, las ventanas corridas y los carteles de campaña."""
    Y = 6
    acero = mat('acero_mht', 0xc8ccd0, 0.25)
    o = cil(acero, 0, Y, 0.6, 2.6, 16, 20, eje='X')
    o.location = (0, Y, 2.7)
    caja(acero, 0, Y, 0, 16, 5.0, 2.7)
    caja(rojo(), 0, Y - 2.52, 1.0, 16, 0.08, 0.5)
    caja(cristal(), 0, Y - 2.55, 2.0, 14, 0.08, 1.4)
    caja(madera_o(), 0, Y - 2.6, 0, 16.4, 0.3, 0.6)
    caja(nieve(), 0, Y, 5.1, 16.2, 3.0, 0.25)
    for s in (-1, 1):
        cil(negro(), 9.5, Y - 1.5, 0, 0.12, 9.5, 6)
    flecha = rojo()
    caja(flecha, 6.5, Y - 1.5, 8.5, 6, 0.3, 1.2)
    o = cil(flecha, 3.0, Y - 1.5, 9.1, 1.4, 0.3, 3, eje='Y')
    o.rotation_euler = (math.pi / 2, math.pi / 2, 0)
    for k in range(10):
        esfera(bombilla(), 4.2 + k * 0.55, Y - 1.7, 8.6, 0.09, 1)
    texto(blanco(), 'DINER', 6.6, Y - 1.7, 8.85, tam=0.6, prof=0.03)
    for (x, c, txt) in ((-5, 0x1e4a9a, '¡VOTA!'), (-1, 0xc8302a, 'PRIMARIAS')):
        caja(blanco(), x, Y - 2.75, 0.6, 2.4, 0.06, 1.0)
        texto(mat(f'cartel_mht_{c}', c, 0.5), txt, x, Y - 2.8, 0.9, tam=0.35, prof=0.02)

def muneco_acera():
    """El muñeco de nieve de la acera: tres bolas, la nariz de zanahoria, la
    bufanda roja, el sombrero y los brazos de rama."""
    n = nieve()
    esfera(n, 0, 0, 0.45, 0.5, 2)
    esfera(n, 0, 0, 1.1, 0.36, 2)
    esfera(n, 0, 0, 1.6, 0.26, 2)
    cil(naranja(), 0, -0.24, 1.6, 0.05, 0.25, 8, r2=0.005, eje='Y')
    for s in (-1, 1):
        esfera(negro(), s * 0.09, -0.22, 1.68, 0.035, 1)
        rama(madera_o(), (s * 0.3, 0, 1.15), (s * 0.75, 0, 1.45), 0.03, 0.02, 4)
    cil(rojo(), 0, 0, 1.33, 0.29, 0.1, 12)
    caja(rojo(), 0.12, -0.25, 1.05, 0.1, 0.04, 0.32)
    cil(negro(), 0, 0, 1.8, 0.28, 0.04, 12)
    cil(negro(), 0, 0, 1.84, 0.18, 0.3, 12)

# ================================================================ cruza la calle
def arco_libre():
    """La matrícula gigante de Nuevo Hampshire que cruza la calle: los dos
    postes, la placa blanca con VIVE LIBRE O MUERE en verde y la nieve
    encima."""
    for s in (-1, 1):
        cil(negro(), s * 8.5, 0, 0, 0.3, 8.6, 10)
    caja(blanco(), 0, 0, 5.6, 15, 0.3, 3.0)
    caja(verde(), 0, -0.16, 5.7, 14.6, 0.04, 0.12)
    caja(verde(), 0, -0.16, 8.38, 14.6, 0.04, 0.12)
    texto(verde(), 'NEW HAMPSHIRE', 0, -0.2, 7.6, tam=0.55, prof=0.03)
    texto(verde(), 'VIVE LIBRE O MUERE', 0, -0.2, 6.3, tam=1.0, prof=0.04)
    caja(nieve(), 0, 0, 8.6, 15.2, 0.6, 0.3)

# ================================================================ el plató del debate
def estudio_debate():
    """El plató del debate de las primarias (momento estrella): el suelo
    azul brillante con estrellas, las gradas del público a los dos lados,
    los focos, las cámaras de televisión, las pantallas con DEBATE y las
    banderas. Cruza la calle: el origen en el centro."""
    L = 420
    caja(mat_bloques('suelo_plato_mht', 0x1e3a7a, 0x16306a, ancho=2.0, alto=2.0, grosor=0.02), 0, 0, -0.2, 17, L, 0.2)
    caja(mat('moqueta_mht', 0x5a1a2a, 0.9), 0, 0, -0.21, 80, L, 0.2)
    pub = [lambda: mat('pub_a_mht', 0xc8302a, 0.7), lambda: mat('pub_b_mht', 0x1e4a9a, 0.7), lambda: mat('pub_c_mht', 0xf2f0e8, 0.7)]
    for s in (-1, 1):
        for g in range(4):
            caja(mat('grada_mht', 0x3a3a48, 0.7), s * (11 + g * 1.6), 0, 0, 1.6, L, 0.6 + g * 0.7)
        for k in range(int(L / 2.5)):
            y = -L / 2 + 1.25 + k * 2.5
            g = k % 4
            esfera(pub[k % 3](), s * (11 + g * 1.6), y, 1.1 + g * 0.7, 0.35, 1, esc=(1, 1, 1.3))
        for k in range(int(L / 35)):
            y = -L / 2 + 17 + k * 35
            cil(negro(), s * 8.0, y, 0, 0.1, 6.5, 6)
            esfera(bombilla(), s * 7.7, y, 6.4, 0.35, 1)
            caja(negro(), s * 9.0, y + 6, 0.8, 0.8, 1.6, 0.9)
            cil(negro(), s * 8.5, y + 6, 1.25, 0.25, 0.6, 10, eje='X')
            cil(negro(), s * 9.0, y + 6, 0, 0.08, 0.8, 6)
        for k in range(int(L / 60)):
            y = -L / 2 + 30 + k * 60
            caja(negro(), s * 17.5, y, 4.0, 0.3, 9, 5)
            caja(azul(), s * 17.3, y, 4.3, 0.1, 8.4, 4.4)
            texto(blanco(), 'DEBATE', s * 17.2, y, 6.0, tam=1.0, prof=0.03).rotation_euler = (math.pi / 2, 0, -s * math.pi / 2)
    for (y, txt) in ((-L / 2 + 1, 'DEBATE'), (L / 2 - 1, 'FIN DEL DEBATE')):
        for s in (-1, 1):
            cil(rojo(), s * 7.0, y, 0, 0.3, 6.4, 8)
        caja(azul(), 0, y, 5.6, 14.6, 0.5, 0.8)
        texto(blanco(), 'PRIMARIAS · ' + txt, 0, y - 0.26, 5.75, tam=0.55, prof=0.04)

# ================================================================ obstáculos
def fuerte_nieve():
    """El fuerte de nieve (en la acera; detrás asoma el niño): el muro curvo
    de bloques de nieve con las almenas y un montón de bolas preparadas."""
    n = nieve()
    for k in range(7):
        a = -0.9 + k * 0.3
        x, y = math.sin(a) * 1.6, -math.cos(a) * 0.6
        caja(n, x, y, 0, 0.5, 0.4, 0.75, giro=a)
        if k % 2 == 0:
            caja(n, x, y, 0.75, 0.4, 0.4, 0.25, giro=a)
    for i in range(5):
        esfera(n, -0.6 + (i % 3) * 0.25, 0.3 + (i // 3) * 0.2, 0.12 + (i // 3) * 0.18, 0.13, 1)

def nino_nieve():
    """El niño del fuerte (sube y baja detrás del muro y tira)."""
    nino_m(0, 0, 0, 1.0)

def rival_debate():
    """El otro candidato del debate (sin nombre) detrás de su atril: traje
    gris, corbata azul, la sonrisa enorme y el dedo levantado; el atril con
    la estrella. Mira al jugador (-y)."""
    caja(mat('atril_mht', 0x1e3a7a, 0.4), 0, 0, 0, 1.3, 0.8, 1.25)
    caja(blanco(), 0, -0.41, 0.85, 1.0, 0.02, 0.25)
    esfera(rojo(), 0, -0.42, 0.55, 0.16, 1, esc=(1, 0.2, 1))
    tr = mat('traje_mht', 0x5a5e66, 0.6)
    esfera(tr, 0, 0.3, 1.45, 0.5, 2, esc=(1.1, 0.7, 1.0))
    caja(blanco(), 0, -0.05, 1.45, 0.25, 0.02, 0.45)
    caja(azul(), 0, -0.07, 1.4, 0.1, 0.02, 0.4)
    esfera(piel(), 0, 0.2, 2.2, 0.33, 2, esc=(0.95, 0.95, 1.1))
    esfera(mat('pelo_rival_mht', 0x6a4a2a, 0.7), 0, 0.3, 2.42, 0.3, 2, mitad=True)
    for s in (-1, 1):
        esfera(blanco(), s * 0.11, -0.1, 2.27, 0.07, 1)
        esfera(negro(), s * 0.11, -0.15, 2.27, 0.035, 1)
    caja(blanco(), 0, -0.12, 2.05, 0.3, 0.02, 0.07)
    rama(tr, (0.45, 0.2, 1.6), (0.65, -0.2, 2.2), 0.1, 0.08, 6)
    rama(piel(), (0.65, -0.2, 2.2), (0.68, -0.25, 2.55), 0.04, 0.03, 6)
    rama(tr, (-0.45, 0.2, 1.6), (-0.4, -0.25, 1.3), 0.1, 0.08, 6)

def cartel_nh():
    """La pancarta del Sentido Común (agacharse): ABRÍGATE, QUE NIEVA."""
    for x in (-1.25, 1.25):
        cil(madera_o(), x, 0, 0, 0.07, 2.75, 8)
    caja(azul(), 0, 0, 1.5, 2.4, 0.05, 1.2)
    esfera(rosa(), -0.9, -0.05, 2.1, 0.2, 1, esc=(1.2, 0.4, 1))
    texto(blanco(), 'ABRÍGATE,', 0.15, -0.035, 2.2, tam=0.22, prof=0.02)
    texto(amarillo(), 'QUE NIEVA', 0.15, -0.035, 1.8, tam=0.22, prof=0.02)
    caja(nieve(), 0, 0, 2.7, 2.5, 0.12, 0.08)

PIEZAS = {
    'molinos_amoskeag': (molinos_amoskeag, 'manchester', dict(lado=2048, bisel=0.0)),
    'teatro_palace':    (teatro_palace,    'manchester', dict(lado=1024, bisel=0.0)),
    'city_hall_mht':    (city_hall_mht,    'manchester', dict(lado=1024, bisel=0.0)),
    'diner_flecha':     (diner_flecha,     'manchester', dict(lado=1024, bisel=0.0)),
    'muneco_acera':     (muneco_acera,     'manchester', dict(lado=256, bisel=0.0)),
    'arco_libre':       (arco_libre,       'manchester', dict(lado=1024, bisel=0.0, suelo=False)),
    'estudio_debate':   (estudio_debate,   'manchester', dict(lado=2048, bisel=0.0, suelo=False)),
    'fuerte_nieve':     (fuerte_nieve,     'obstaculos', dict(lado=256, bisel=0.0)),
    'nino_nieve':       (nino_nieve,       'obstaculos', dict(lado=256, bisel=0.0)),
    'rival_debate':     (rival_debate,     'obstaculos', dict(lado=256, bisel=0.0)),
    'cartel_nh':        (cartel_nh,        'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
}

correr(PIEZAS)
