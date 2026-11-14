# Nivel 30: Cheyenne, Wyoming (14/11/2026).
#
#   blender -b -P blender/cheyenne.py -- [pieza ...] [--rapido]
#
# Historia: «Rodeo y estampida de bisontes». Acto de la Armada Española.
#   Por Capitol Avenue en pleno Cheyenne Frontier Days, el rodeo al aire libre
#   más grande del mundo («The Daddy of 'em All»): la estación de la Union
#   Pacific con su torre del reloj, el hotel Plains, la locomotora Big Boy y
#   las botas gigantes pintadas de las aceras. Una estampida de bisontes que
#   se para echando el lazo; el ruedo de Frontier Park, donde hay que aguantar
#   8 segundos encima del toro; y se llega al Capitolio de Wyoming, con su
#   cúpula de oro y el jinete del caballo que corcovea. Pancartas de España:
#   ¡RODEO ES ESPAÑOL! (rodeo, lazo, bronco y mustang son palabras españolas).
# Obstáculos (carpeta obstaculos): el toro del rodeo (se monta: es un
# vehículo), el barril del rodeo, la valla blanca del ruedo, el payaso en su
# barril, la pancarta de España y la diligencia con sus caballos. (Los
# bisontes de la estampida son los de Rushmore.)

import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import *

def blanco():    return mat('blanco_chy', 0xf6f4ee, 0.5)
def negro():     return mat('negro_chy', 0x1c1c20, 0.4)
def arenisca():  return mat_bloques('arenisca_chy', 0xd8c49a, 0xb8a47a, ancho=1.3, alto=0.6, grosor=0.008, variacion=1.05)
def arenisca_l(): return mat('arenisca_lisa_chy', 0xd0bc94, 0.7)
def roja():      return mat_bloques('arenisca_roja_chy', 0xa85a3e, 0x84442e, ancho=1.1, alto=0.5, grosor=0.008, variacion=1.06)
def roja_l():    return mat('roja_lisa_chy', 0x9a5038, 0.7)
def oro():       return mat('oro_chy', 0xe8b840, 0.25)
def ladrillo():  return mat_bloques('ladrillo_chy', 0xb8704a, 0x8a5034, ancho=0.4, alto=0.16)
def piedra():    return mat('piedra_chy', 0xe0d4bc, 0.7)
def cristal():   return mat('cristal_chy', 0x3a5a70, 0.15)
def rojo():      return mat('rojo_chy', 0xc8202a, 0.45)
def azul():      return mat('azul_chy', 0x2a4a9a, 0.45)
def amarillo():  return mat('amarillo_chy', 0xf2c21a, 0.45)
def gris():      return mat('gris_chy', 0x8a9098, 0.4)
def madera():    return mat('madera_chy', 0x8a5a34, 0.85)
def madera_o():  return mat('madera_oscura_chy', 0x5a3a22, 0.85)
def cesped():    return mat('cesped_chy', 0x7aa050, 0.9)
def tierra():    return mat('tierra_chy', 0xb8865a, 0.95)
def bronce():    return mat('bronce_chy', 0x6a4a2a, 0.35)
def hierro():    return mat('hierro_chy', 0x2a2c30, 0.45)
def cuero():     return mat('cuero_chy', 0x7a4a26, 0.7)

def bandera_es(nombre, z0, alto):
    """Las franjas de la bandera de España (roja, amarilla, roja) en z0..z0+alto."""
    return mat_franjas(nombre, 0xc8202a, 0xf2c21a, 3, eje='Z', z0=z0, alto=alto)

def caballo(m, x, y, z=0.0, mira=-1, k=1.0, crin=None):
    """Un caballo de lado (mira a +x si mira=1, a -x si -1): cuerpo, cuello,
    cabeza, cola y las cuatro patas."""
    s = mira
    esfera(m, x, y, z + 1.35 * k, 0.55 * k, 2, esc=(1.7, 0.75, 0.85))
    rama(m, (x + s * 0.75 * k, y, z + 1.5 * k), (x + s * 1.15 * k, y, z + 2.1 * k), 0.3 * k, 0.22 * k, 8)
    esfera(m, x + s * 1.35 * k, y, z + 2.1 * k, 0.24 * k, 1, esc=(1.6, 0.8, 0.9))
    rama(crin or m, (x - s * 0.9 * k, y, z + 1.5 * k), (x - s * 1.25 * k, y, z + 0.8 * k), 0.1 * k, 0.05 * k, 6)
    for dx in (0.6, -0.6):
        for dy in (-0.2, 0.2):
            cil(m, x + s * dx * k, y + dy * k, z, 0.09 * k, 1.05 * k, 6)

def jinete_bronco(m, x, y, z):
    """La estatua del jinete sobre el caballo que corcovea (el de las
    matrículas de Wyoming): el caballo de manos, el jinete con el sombrero y
    el brazo arriba."""
    # El caballo, levantado de atrás (las patas de delante en el aire).
    esfera(m, x, y, z + 1.7, 0.6, 2, esc=(1.7, 0.75, 0.85))
    rama(m, (x - 0.8, y, z + 1.4), (x - 1.25, y, z + 0.9), 0.28, 0.2, 8)
    esfera(m, x - 1.45, y, z + 0.85, 0.25, 1, esc=(1.6, 0.8, 0.9))
    for dy in (-0.2, 0.2):
        rama(m, (x + 0.7, y + dy, z + 1.5), (x + 0.9, y + dy, z), 0.1, 0.08, 6)
        rama(m, (x - 0.6, y + dy, z + 1.4), (x - 1.1, y + dy, z + 1.9), 0.1, 0.08, 6)
    rama(m, (x + 1.0, y, z + 2.0), (x + 1.6, y, z + 2.7), 0.1, 0.04, 6)
    # El jinete.
    rama(m, (x + 0.1, y, z + 2.2), (x + 0.3, y, z + 3.2), 0.22, 0.18, 8)
    esfera(m, x + 0.35, y, z + 3.45, 0.2, 1)
    cil(m, x + 0.35, y, z + 3.55, 0.42, 0.05, 12)
    cil(m, x + 0.35, y, z + 3.6, 0.2, 0.22, 10)
    rama(m, (x + 0.3, y, z + 3.0), (x - 0.2, y, z + 3.8), 0.07, 0.06, 6)
    for dy in (-0.25, 0.25):
        rama(m, (x + 0.1, y + dy, z + 2.25), (x + 0.2, y + dy, z + 1.5), 0.08, 0.07, 6)

def sombrero(m, x, y, z, r=0.35):
    """Un sombrero vaquero: el ala y la copa."""
    cil(m, x, y, z, r, 0.04, 14)
    cil(m, x, y, z + 0.03, r * 0.5, r * 0.6, 12, r2=r * 0.42)

# ================================================================ la meta
def capitolio_wyoming():
    """El Capitolio de Wyoming (la meta): la arenisca clara, el pórtico con
    columnas y frontón, las alas, el tambor con columnas, la cúpula de oro con
    su linterna y, delante, la estatua de bronce del jinete del caballo que
    corcovea; la bandera y, de España, la pancarta ¡RODEO ES ESPAÑOL!"""
    Y = 24
    W, D, H = 60.0, 24.0, 14.0
    yf = Y - D / 2
    g = arenisca()
    caja(g, 0, Y, 0, W, D, H)
    caja(arenisca_l(), 0, Y, H, W + 0.6, D + 0.6, 0.8)
    for s in (-1, 1):
        caja(g, s * 24, yf - 2, 0, 12, 4, H + 2)
        caja(arenisca_l(), s * 24, yf - 2.1, H + 2, 12.4, 4.4, 0.8)
        fronton(arenisca_l(), s * 24, yf - 4.1, H + 2.8, 12.4, 2.4, 4.4)
    for k in range(13):
        x = -26 + k * 4.33
        for z in (3.0, 8.5):
            if abs(x) < 9:
                continue
            ventana(x, z, 1.4, 3.0, y=yf - (4 if abs(abs(x) - 24) < 6.5 else 0), marco=arenisca_l(), cristal=cristal(),
                    remate='fronton' if z > 5 else None)
    # El pórtico.
    caja(g, 0, yf - 3, 0, 18, 6, 3.5)
    columnata(arenisca_l(), -7.5, 7.5, 6, yf - 5, 3.5, 0.6, 10)
    caja(arenisca_l(), 0, yf - 4.5, 13.5, 18, 4.5, 1.3)
    fronton(arenisca_l(), 0, yf - 5, 14.8, 18, 3.4, 4.5)
    puerta(0, 3.5, 2.6, 4.4, y=yf - 0.05, color=0x5a3a22, marco=arenisca_l())
    # El tambor, la cúpula de oro (más alta que ancha) y la linterna.
    cil(g, 0, Y, H + 0.8, 8.0, 3.0, 32)
    cil(arenisca_l(), 0, Y, H + 3.8, 6.6, 7.5, 32)
    for k in range(16):
        a = k * math.tau / 16
        cil(blanco(), math.cos(a) * 6.9, Y + math.sin(a) * 6.9, H + 3.8, 0.3, 7.5, 10)
    for k in range(8):
        a = k * math.tau / 8 + 0.2
        cil(cristal(), math.cos(a) * 6.65, Y + math.sin(a) * 6.65, H + 5.2, 0.7, 4.0, 8)
    cil(arenisca_l(), 0, Y, H + 11.3, 7.4, 0.9, 32)
    cupula(oro(), 0, Y, H + 12.2, 6.6, 9.4, 32, 10)
    for k in range(12):
        a = k * math.tau / 12
        rama(mat('nervio_chy', 0xc89a30, 0.3), (math.cos(a) * 6.6, Y + math.sin(a) * 6.6, H + 12.3),
             (math.cos(a) * 1.4, Y + math.sin(a) * 1.4, H + 21.3), 0.12, 0.08, 4)
    cil(arenisca_l(), 0, Y, H + 21.4, 1.6, 3.2, 12)
    for k in range(8):
        a = k * math.tau / 8
        cil(blanco(), math.cos(a) * 1.65, Y + math.sin(a) * 1.65, H + 21.4, 0.12, 3.2, 6)
    cupula(oro(), 0, Y, H + 24.6, 1.7, 1.8, 12, 4)
    cil(oro(), 0, Y, H + 26.3, 0.15, 1.6, 6)
    esfera(oro(), 0, Y, H + 28.0, 0.35, 1)
    # La escalinata y el césped.
    for k in range(10):
        caja(arenisca_l(), 0, yf - 7.6 - k * 0.55, 0, 20 + k * 0.6, 0.55, 3.5 - k * 0.33)
    caja(cesped(), 0, yf - 18, -0.05, 80, 24, 0.06)
    for (x, y) in ((-30, yf - 10), (-34, yf - 20), (30, yf - 9), (34, yf - 19), (-40, yf + 2), (40, yf + 2)):
        cil(madera_o(), x, y, 0, 0.35, 3.0, 8)
        esfera(mat('copa_chy', 0x4a7a3a, 0.85), x, y, 5.0, 3.0, 2, esc=(1, 1, 1.15))
    # El jinete de bronce, sobre su pedestal (a la izquierda, se ve al llegar).
    caja(granito := mat('pedestal_chy', 0x9a9488, 0.6), -13, yf - 16, 0, 4.4, 2.6, 2.4)
    jinete_bronco(bronce(), -13, yf - 16, 2.4)
    # La bandera y la pancarta de España.
    cil(gris(), -22, yf - 13, 0, 0.13, 13, 8)
    caja(mat('bandera_wy_chy', 0x2a3a8a, 0.6), -20.2, yf - 13, 10.6, 3.6, 0.06, 2.4)
    caja(rojo(), -20.2, yf - 13.04, 10.6, 3.6, 0.06, 0.25)
    caja(blanco(), -20.2, yf - 13.05, 10.85, 3.4, 0.06, 0.15)
    caja(blanco(), -20.2, yf - 13.06, 11.3, 1.6, 0.06, 1.2)
    for x in (9.5, 21.5):
        cil(madera_o(), x, yf - 15, 0, 0.12, 4.4, 8)
    caja(bandera_es('pancarta_es_capitolio_chy', 2.8, 1.6), 15.5, yf - 15, 2.8, 12, 0.06, 1.6)
    texto(negro(), '¡RODEO ES ESPAÑOL!', 15.5, yf - 15.04, 3.6, tam=0.78, prof=0.03)

# ================================================================ edificios
def cheyenne_depot():
    """La estación de la Union Pacific de Cheyenne (1887): arenisca roja y
    clara a franjas, los arcos románicos de la entrada, la torre del reloj con
    su tejado de pirámide y el letrero UNION PACIFIC."""
    Y = 9
    W, D = 40.0, 14.0
    yf = Y - D / 2
    r = roja()
    c = arenisca()
    caja(r, 0, Y, 0, W, D, 4)
    caja(c, 0, Y, 4, W, D, 0.8)
    caja(r, 0, Y, 4.8, W, D, 4.5)
    caja(c, 0, Y, 9.3, W + 0.4, D + 0.4, 0.7)
    tejado(mat('tejado_depot_chy', 0x5a5e66, 0.6), 0, Y - D / 2, Y + D / 2, 10.0, W, 4.0, cumbrera='x')
    # Los arcos de la entrada (a la derecha de la torre).
    for x in (4, 9, 14):
        caja(cristal(), x, yf - 0.05, 0.4, 3.0, 0.1, 2.8)
        cil(c, x, yf - 0.06, 3.2, 1.7, 0.12, 16, eje='Y')
        cil(cristal(), x, yf - 0.12, 3.2, 1.4, 0.1, 16, eje='Y')
    for x in (-16, -12, -8):
        ventana(x, 1.0, 1.4, 2.4, y=yf, marco=c, cristal=cristal())
    for x in (-16, -12, -8, 4, 9, 14):
        ventana(x, 5.6, 1.2, 2.4, y=yf, marco=c, cristal=cristal(), remate='cornisa')
    # La torre del reloj.
    T = 6.0
    caja(r, -3, yf - 1, 0, T, T, 22)
    for z in (4, 9.3, 15):
        caja(c, -3, yf - 1, z, T + 0.3, T + 0.3, 0.7)
    for (dx, dy, rx) in ((0, -1, 0), (-1, 0, 1), (1, 0, 1)):
        x, y = -3 + dx * (T / 2 + 0.1), yf - 1 + dy * (T / 2 + 0.1)
        o = cil(blanco(), x, y, 18.3, 1.8, 0.15, 24, eje='Y')
        if rx:
            o.rotation_euler = (math.pi / 2, 0, math.pi / 2)
        if dy == -1:
            caja(negro(), x, y - 0.12, 18.3, 0.12, 0.04, 1.3)
            caja(negro(), x + 0.4, y - 0.12, 18.3, 0.9, 0.04, 0.12)
    for dz in (10.5, 12.5):
        caja(cristal(), -3, yf - 1 - T / 2 - 0.05, dz, 1.2, 0.1, 1.6)
    o = cil(mat('tejado_torre_chy', 0x5a5e66, 0.6), -3, yf - 1, 22, T * 0.74, 6.5, 4, r2=0.12)
    o.rotation_euler = (0, 0, math.pi / 4)
    cil(hierro(), -3, yf - 1, 28.5, 0.08, 2.0, 6)
    # El letrero.
    caja(negro(), 9, yf - 0.4, 9.6, 14, 0.2, 1.3)
    texto(mat('letras_up_chy', 0xf2e8c8, 0.4), 'UNION PACIFIC', 9, yf - 0.55, 10.25, tam=0.95, prof=0.05)

def plains_hotel():
    """El hotel Plains (1911): cinco plantas de ladrillo con la planta baja de
    piedra, los toldos, la cornisa con motivos de los indios de las llanuras
    y el letrero THE PLAINS de arriba."""
    Y = 8
    W, D, H = 22.0, 16.0, 20.0
    yf = Y - D / 2
    l = ladrillo()
    caja(l, 0, Y, 0, W, D, H)
    caja(piedra(), 0, Y, 0, W + 0.3, D + 0.3, 4.2)
    for x in (-8, -4, 4, 8):
        caja(cristal(), x, yf - 0.08, 0.5, 3.0, 0.1, 3.0)
        caja(mat('toldo_plains_chy', 0x2a5a3a, 0.7), x, yf - 0.8, 3.4, 3.4, 1.4, 0.15, inclina=-0.3)
    puerta(0, 0, 2.6, 3.4, y=yf - 0.12, color=0x4a2e1a, marco=piedra())
    for p in range(4):
        for k in range(7):
            ventana(-9 + k * 3, 5.6 + p * 3.4, 1.3, 2.2, y=yf, marco=piedra(), cristal=cristal())
    # La cornisa con el dibujo de las llanuras (triángulos rojos y azules).
    caja(piedra(), 0, yf - 0.2, H - 1.4, W + 0.6, 0.6, 1.4)
    for k in range(11):
        x = -10 + k * 2
        fronton(rojo() if k % 2 else azul(), x, yf - 0.52, H - 1.25, 1.2, 0.9, 0.04)
    caja(piedra(), 0, Y, H, W + 1.0, D + 1.0, 0.5)
    # El letrero de arriba.
    for x in (-6, 6):
        caja(hierro(), x, Y + 2, H + 0.5, 0.2, 0.2, 3.4)
    caja(hierro(), 0, Y + 2, H + 3.6, 14, 0.15, 0.15)
    texto(mat('neon_plains_chy', 0xff3a2a, 0.3), 'THE PLAINS', 0, Y + 1.9, H + 2.2, tam=2.0, prof=0.08)

def big_boy():
    """La locomotora Big Boy de la Union Pacific (la de vapor más grande del
    mundo), en el parque Holliday: la caldera negra, la chimenea, la cabina,
    las dos tandas de ruedas motrices, el ténder con UNION PACIFIC y el 4004,
    sobre su vía y su balasto, con la verja."""
    Y = 6
    # El balasto, la vía y la verja.
    caja(mat('balasto_chy', 0x8a8070, 0.95), 0, Y, 0, 40, 4.4, 0.4)
    for s in (-1, 1):
        caja(hierro(), 0, Y + s * 0.72, 0.4, 40, 0.12, 0.15)
    for k in range(20):
        caja(madera_o(), -19 + k * 2, Y, 0.38, 0.3, 2.4, 0.06)
    for k in range(14):
        cil(hierro(), -19.5 + k * 3, Y - 3.5, 0, 0.05, 1.2, 6)
    caja(hierro(), 0, Y - 3.5, 1.1, 40, 0.06, 0.06)
    caja(cesped(), 0, Y - 1, -0.05, 44, 12, 0.06)
    n = negro()
    # La caldera y la chimenea.
    cil(n, -6, Y, 3.4, 1.55, 18, 20, eje='X')
    cil(mat('caldera_frente_chy', 0x3a3c40, 0.4), -15.05, Y, 3.4, 1.4, 0.15, 20, eje='X')
    esfera(mat('faro_chy', 0xf4ecc0, 0.3), -15.2, Y, 4.6, 0.35, 1)
    cil(n, -12, Y, 4.8, 0.45, 1.4, 12)
    cil(n, -7, Y, 4.8, 0.7, 0.8, 12)
    cil(n, -4, Y, 4.8, 0.6, 0.7, 12)
    caja(n, -6, Y, 1.0, 19, 2.4, 1.6)
    # La cabina.
    caja(n, 4.5, Y, 1.8, 3.6, 3.4, 4.0)
    caja(n, 4.5, Y, 5.8, 4.2, 3.8, 0.3)
    for s in (-1, 1):
        caja(cristal(), 4.5, Y + s * 1.71, 3.9, 1.4, 0.04, 1.0)
    # Las ruedas motrices (dos tandas de cuatro) y las bielas rojas.
    for x0 in (-13.5, -6.3):
        for k in range(4):
            cil(n, x0 + k * 1.75, Y - 1.25, 0.85, 0.8, 0.3, 16, eje='Y')
            cil(rojo(), x0 + k * 1.75, Y - 1.42, 0.85, 0.18, 0.06, 10, eje='Y')
        caja(gris(), x0 + 2.6, Y - 1.45, 0.75, 5.6, 0.06, 0.16)
    # El ténder.
    caja(n, 13.5, Y, 1.0, 13, 3.2, 3.8)
    for k in range(7):
        cil(n, 8.4 + k * 1.7, Y - 1.25, 0.6, 0.55, 0.25, 12, eje='Y')
    letras = mat('letras_tender_chy', 0xf2c21a, 0.4)
    texto(letras, 'UNION PACIFIC', 13.5, Y - 1.62, 3.6, tam=0.75, prof=0.03)
    texto(letras, '4004', 4.5, Y - 1.72, 2.6, tam=0.6, prof=0.03)
    # El cartel de delante.
    caja(madera(), -10, Y - 5, 0, 0.2, 0.2, 1.4)
    caja(madera(), -10, Y - 5.05, 1.2, 3.4, 0.1, 0.9)
    texto(blanco(), 'BIG BOY', -10, Y - 5.12, 1.65, tam=0.42, prof=0.02)

def bota_gigante():
    """Una de las botas gigantes pintadas de Cheyenne («These Boots Are Made
    for Talkin'»): 2,6 m, sobre su peana, pintada a colores (para la acera)."""
    # De lado (la punta hacia -x): así se lee la silueta desde la calle.
    caja(piedra(), -0.25, 0, 0, 2.2, 1.0, 0.3)
    tacon = madera_o()
    caja(tacon, 0.42, 0, 0.3, 0.42, 0.46, 0.34)
    caja(tacon, -0.55, 0, 0.3, 1.1, 0.5, 0.07)
    pie = mat('bota_pie_chy', 0xc8202a, 0.55)
    esfera(pie, -0.3, 0, 0.72, 0.42, 2, esc=(2.0, 0.62, 0.62))
    o = cil(pie, -1.05, 0, 0.6, 0.2, 0.42, 12, r2=0.03, eje='X')
    o.rotation_euler = (0, -math.pi / 2, 0)
    o.location = (-1.0, 0, 0.6)
    cana = mat('bota_cana_chy', 0x2fa8a0, 0.55)
    o = cil(cana, 0.2, 0, 0.7, 0.4, 1.85, 18, r2=0.44)
    o.scale = (1.2, 0.85, 1)
    cil(mat('bota_boca_chy', 0x1e6a64, 0.6), 0.2, 0, 2.5, 0.45, 0.1, 18).scale = (1.2, 0.85, 1)
    for s in (-1, 1):
        rama(cuero(), (0.2 + s * 0.5, 0, 2.45), (0.2 + s * 0.55, 0, 2.75), 0.07, 0.07, 6)
    # Lo pintado: el sol, las montañas y las puntadas.
    esfera(amarillo(), 0.2, -0.36, 2.0, 0.2, 1, esc=(1, 0.25, 1))
    for (x, h) in ((0.0, 0.42), (0.35, 0.3)):
        fronton(mat('montana_bota_chy', 0x5a3a8a, 0.6), x, -0.38, 1.25, 0.5, h, 0.04)
    for x in (-0.9, -0.6, -0.3, 0.0):
        caja(blanco(), x, -0.25, 0.82, 0.12, 0.02, 0.03)

# ================================================================ cruzan la calle
def arco_cheyenne():
    """El arco de los Cheyenne Frontier Days: dos troncos de pino y el
    travesaño, como la puerta de un rancho; el letrero colgado con CHEYENNE
    FRONTIER DAYS y, por detrás, THE DADDY OF 'EM ALL; encima, el jinete del
    caballo que corcovea recortado en chapa."""
    m = madera()
    for s in (-1, 1):
        cil(m, s * 8.6, 0, 0, 0.45, 8.0, 10)
        cil(madera_o(), s * 8.6, 0, 7.9, 0.5, 0.25, 10)
    cil(m, 0, 0, 7.2, 0.38, 18.4, 10, eje='X')
    for x in (-3.5, 3.5):
        cil(hierro(), x, 0, 5.3, 0.03, 1.9, 4)
    caja(madera_o(), 0, 0, 4.0, 11, 0.16, 1.5)
    texto(amarillo(), 'CHEYENNE FRONTIER DAYS', 0, -0.1, 4.75, tam=0.85, prof=0.05)
    o = texto(amarillo(), "THE DADDY OF 'EM ALL", 0, 0.1, 4.75, tam=0.8, prof=0.05)
    o.rotation_euler = (math.pi / 2, 0, math.pi)
    jinete_bronco(hierro(), 0, 0, 7.5)

# ================================================================ el ruedo
def arena_rodeo():
    """El ruedo de Frontier Park (momento estrella, al aire libre): la tierra
    del ruedo, la valla blanca a los dos lados, las tribunas llenas, los
    cajones de salida de los toros con sus números, los barriles, los payasos,
    las banderas, el palco del locutor y los arcos de SALIDA y META.
    Cruza la calle: el origen en el centro y la calle a lo largo de y."""
    L = 420
    caja(tierra(), 0, 0, -0.2, 24, L, 0.2)
    for k in range(int(L / 9)):
        caja(mat('tierra_rastrillada_chy', 0xa87a50, 0.95), -11 + (k * 7 % 22), -L / 2 + 4 + k * 9, -0.01, 3.0, 0.4, 0.01)
    blanco_v = blanco()
    for s in (-1, 1):
        # La valla blanca (tres tablones) y los postes.
        for z in (0.35, 0.95, 1.55):
            caja(blanco_v, s * 7.6, 0, z, 0.08, L, 0.25)
        for k in range(int(L / 3)):
            caja(blanco_v, s * 7.66, -L / 2 + 1.5 + k * 3, 0, 0.18, 0.18, 1.9)
        # Los anuncios de la valla.
        for k in range(int(L / 24)):
            y = -L / 2 + 12 + k * 24
            caja([rojo, azul, amarillo][k % 3](), s * 7.55, y, 0.4, 0.04, 8, 1.2)
    # Las tribunas: gente de colores subiendo hacia fuera, con el tejado.
    gente = mat_bloques('gente_chy', 0x8a5a7a, 0x2a2a30, ancho=0.5, alto=0.7, variacion=1.7)
    for s in (-1, 1):
        caja(mat('muro_tribuna_chy', 0x8a3a2a, 0.7), s * 9.0, 0, 0, 2.6, L, 1.8)
        for g in range(6):
            caja(gente, s * (11 + g * 3.2), 0, 0, 3.2, L, 2.0 + g * 2.4)
        caja(mat('tejado_tribuna_chy', 0xe8e4dc, 0.5), s * 20, 0, 18, 16, L, 0.4)
        for k in range(int(L / 30)):
            cil(hierro(), s * 27.5, -L / 2 + 15 + k * 30, 0, 0.25, 18, 8)
    camisas = [0xc8282c, 0x2a5aa8, 0xf4f0e8, 0xf0c020, 0x3f8a4a]
    for k in range(int(L / 3.6)):
        y = -L / 2 + 2 + k * 3.6
        s = -1 if k % 2 else 1
        cm = mat(f'camisa_chy{k % 5}', camisas[k % 5], 0.8)
        cil(cm, s * 10.6, y, 1.8, 0.42, 0.85, 6)
        esfera(mat('cara_chy', 0xe8b89a, 0.7), s * 10.6, y, 2.95, 0.3, 1)
        sombrero(mat('sombrero_chy%d' % (k % 3), [0xf2e8c8, 0x5a3a22, 0x1c1c20][k % 3], 0.7), s * 10.6, y, 3.18, 0.42)
    # Los cajones de salida (a la izquierda), con sus números y los vaqueros encima.
    for k in range(int(L / 70)):
        y0 = -L / 2 + 30 + k * 70
        for i in range(6):
            y = y0 + i * 2.6
            for z in (0.4, 1.0, 1.6, 2.2):
                caja(mat('cajon_chy', 0x4a6a8a, 0.5), -8.4, y, z, 0.08, 2.4, 0.18)
            caja(hierro(), -8.4, y - 1.25, 0, 0.12, 0.12, 2.6)
            caja(blanco(), -8.36, y, 2.5, 0.06, 0.9, 0.7)
            texto(negro(), str(i + 1), -8.3, y, 2.85, tam=0.5, prof=0.02).rotation_euler = (math.pi / 2, 0, -math.pi / 2)
            cil(mat('vaquero_chy', 0x3a5a8a, 0.7), -9.3, y, 2.6, 0.3, 0.9, 6)
            esfera(mat('cara_chy', 0xe8b89a, 0.7), -9.3, y, 3.7, 0.24, 1)
            sombrero(mat('sombrero_chy0', 0xf2e8c8, 0.7), -9.3, y, 3.9, 0.36)
    # Barriles y payasos junto a la valla, banderas y el palco del locutor.
    for k in range(int(L / 45)):
        y = -L / 2 + 22 + k * 45
        s = 1 if k % 2 else -1
        cil(mat('barril_lado_chy', 0x2a6ab8, 0.5), s * 6.3, y, 0, 0.45, 1.0, 14)
        cil(mat('barril_aro_chy', 0xf6f4ee, 0.5), s * 6.3, y, 0.45, 0.47, 0.12, 14)
        cil(mat('payaso_chy', 0xc8202a, 0.6), s * 6.4, y + 2, 0, 0.3, 1.2, 8)
        esfera(mat('cara_payaso_chy', 0xf6f0e6, 0.6), s * 6.4, y + 2, 1.45, 0.25, 1)
        esfera(rojo(), s * 6.4 - s * 0.24, y + 2, 1.45, 0.07, 1)
        sombrero(mat('sombrero_chy2', 0x1c1c20, 0.7), s * 6.4, y + 2, 1.66, 0.32)
    for k in range(int(L / 20)):
        y = -L / 2 + 10 + k * 20
        for s in (-1, 1):
            cil(gris(), s * 7.7, y, 1.9, 0.04, 3.0, 4)
            caja([rojo, blanco, azul][k % 3](), s * 7.7 + s * 0.5, y, 4.1, 1.0, 0.03, 0.7)
    for k in range(int(L / 140)):
        y = -L / 2 + 70 + k * 140
        caja(mat('palco_chy', 0x6a3a22, 0.7), 19, y, 18.4, 8, 6, 4.0)
        caja(cristal(), 15, y, 19.4, 0.1, 5, 2.2)
        caja(blanco(), 14.9, y, 22.6, 0.1, 6, 1.0)
        texto(rojo(), 'FRONTIER PARK', 14.85, y, 23.1, tam=0.7, prof=0.02).rotation_euler = (math.pi / 2, 0, math.pi / 2)
    for (y, txt) in ((-L / 2 + 1, 'SALIDA'), (L / 2 - 1, 'META')):
        for s in (-1, 1):
            cil(madera(), s * 7.0, y, 0, 0.3, 5.8, 8)
        cil(madera(), 0, y, 5.2, 0.28, 14.6, 8, eje='X')
        caja(madera_o(), 0, y, 3.9, 6.0, 0.14, 1.1)
        texto(amarillo(), txt, 0, y - 0.1, 4.45, tam=0.75, prof=0.04)

# ================================================================ obstáculos
def toro_rodeo():
    """El toro del rodeo (un vehículo: se monta encima): un cebú gris de
    lomo alto con la giba, los cuernos cortos, la cuerda con el cencerro y la
    cincha roja de las ancas. Mira al jugador (-y); el juego le da la vuelta
    al montarlo."""
    c = mat('toro_rodeo_chy', 0x8a8682, 0.7)
    o = mat('toro_oscuro_chy', 0x4a4644, 0.7)
    # El cuerpo, la giba y las ancas.
    esfera(c, 0, 0, 1.0, 0.62, 2, esc=(0.95, 2.1, 0.85))
    esfera(o, 0, -0.55, 1.45, 0.42, 2, esc=(1.0, 1.1, 0.9))
    esfera(c, 0, 0.9, 1.05, 0.55, 2, esc=(1.0, 1.0, 0.9))
    # La cabeza, el morro y los cuernos.
    esfera(o, 0, -1.4, 1.0, 0.34, 2, esc=(0.9, 1.25, 0.95))
    esfera(mat('morro_chy', 0x2a2624, 0.6), 0, -1.78, 0.9, 0.2, 1, esc=(1.1, 0.8, 0.8))
    for s in (-1, 1):
        rama(mat('cuerno_chy', 0xe8dcc0, 0.5), (s * 0.22, -1.45, 1.25), (s * 0.55, -1.5, 1.42), 0.07, 0.03, 6)
        esfera(negro(), s * 0.22, -1.62, 1.12, 0.05, 1)
        rama(o, (s * 0.25, -1.3, 1.15), (s * 0.48, -1.25, 1.1), 0.1, 0.05, 6)
    # Las patas.
    for y in (-0.7, 0.85):
        for s in (-1, 1):
            cil(c, s * 0.3, y, 0, 0.13, 0.75, 8, r2=0.16)
            cil(negro(), s * 0.3, y, 0, 0.14, 0.12, 8)
    # La cola, la cuerda con el cencerro y la cincha roja.
    rama(o, (0, 1.4, 1.2), (0, 1.55, 0.5), 0.06, 0.04, 6)
    cil(mat('cuerda_chy', 0xe8d8a8, 0.8), 0, -0.45, 1.0, 0.66, 0.1, 16, eje='Y')
    caja(amarillo(), 0, -0.46, 0.3, 0.2, 0.2, 0.25)
    cil(rojo(), 0, 0.75, 1.05, 0.55, 0.14, 16, eje='Y').scale = (1, 1, 0.9)

def barril_rodeo():
    """El barril de las carreras de barriles (se salta): azul con aros blancos."""
    b = mat('barril_azul_chy', 0x2a6ab8, 0.45)
    cil(b, 0, 0, 0, 0.42, 0.92, 16)
    for z in (0.08, 0.45, 0.82):
        cil(blanco(), 0, 0, z, 0.44, 0.06, 16)
    cil(mat('barril_tapa_chy', 0x1e4a8a, 0.5), 0, 0, 0.92, 0.4, 0.03, 16)

def valla_rodeo():
    """Un trozo de la valla blanca del ruedo (se salta): dos tablones y tres
    postes."""
    for x in (-0.95, 0, 0.95):
        caja(blanco(), x, 0, 0, 0.14, 0.14, 1.0)
    for z in (0.35, 0.75):
        caja(blanco(), 0, -0.05, z, 2.1, 0.06, 0.2)

def payaso_barril():
    """El payaso del rodeo metido en su barril acolchado (no se pasa): el
    barril rojo y amarillo y el payaso asomando con la cara pintada, la nariz
    roja y el sombrero."""
    cil(mat_franjas('barril_payaso_chy', 0xc8202a, 0xf2c21a, 4, eje='Z', z0=0, alto=1.15), 0, 0, 0, 0.55, 1.15, 16)
    cil(mat('acolchado_chy', 0x1c1c20, 0.6), 0, 0, 1.1, 0.58, 0.1, 16)
    cil(mat('camisa_payaso_chy', 0x2a6ab8, 0.6), 0, 0, 1.1, 0.3, 0.35, 10)
    esfera(mat('cara_payaso_chy', 0xf6f0e6, 0.6), 0, 0, 1.68, 0.24, 2)
    esfera(rojo(), 0, -0.24, 1.66, 0.07, 1)
    for s in (-1, 1):
        esfera(negro(), s * 0.09, -0.21, 1.76, 0.03, 1)
        rama(mat('camisa_payaso_chy', 0x2a6ab8, 0.6), (s * 0.28, 0, 1.35), (s * 0.55, -0.1, 1.75), 0.07, 0.06, 6)
    cil(rojo(), 0, -0.2, 1.56, 0.08, 0.02, 8, eje='Y')
    sombrero(mat('sombrero_payaso_chy', 0x5a3a22, 0.7), 0, 0, 1.86, 0.34)

def cartel_rodeo():
    """La pancarta de España (agacharse): ¡RODEO ES ESPAÑOL!"""
    for x in (-1.25, 1.25):
        cil(madera(), x, 0, 0, 0.07, 2.75, 8)
    caja(bandera_es('pancarta_es_obst_chy', 1.5, 1.2), 0, 0, 1.5, 2.4, 0.05, 1.2)
    texto(negro(), '¡RODEO', 0, -0.035, 2.15, tam=0.3, prof=0.02)
    texto(blanco(), 'ES ESPAÑOL!', 0, -0.035, 1.7, tam=0.22, prof=0.02)

def diligencia():
    """La diligencia del Oeste (no se pasa), con sus dos caballos: la caja
    roja con el techo y el equipaje, las ruedas amarillas y OVERLAND STAGE.
    Los caballos miran al jugador y el morro está en el origen (el resto,
    hacia atrás, como los demás coches)."""
    pelo = mat('caballo_chy', 0x7a4a2a, 0.7)
    crin = mat('crin_chy', 0x2a1a10, 0.7)
    for x in (-0.45, 0.45):
        esfera(pelo, x, 1.1, 1.25, 0.42, 2, esc=(0.7, 1.7, 0.85))
        rama(pelo, (x, 0.5, 1.45), (x, 0.2, 1.95), 0.22, 0.17, 8)
        esfera(pelo, x, 0.12, 1.95, 0.19, 1, esc=(0.8, 1.5, 0.9))
        rama(crin, (x, 0.45, 1.75), (x, 0.65, 1.95), 0.06, 0.04, 6)
        for y in (0.65, 1.55):
            for dx in (-0.16, 0.16):
                cil(pelo, x + dx, y, 0, 0.07, 1.0, 6)
    cil(madera_o(), 0, 2.2, 1.0, 0.05, 1.6, 6, eje='Y')
    # La caja de la diligencia.
    r = mat('diligencia_chy', 0xa82a26, 0.5)
    caja(r, 0, 4.1, 0.95, 1.7, 2.4, 1.6)
    caja(mat('techo_dil_chy', 0x2a1a10, 0.6), 0, 4.1, 2.55, 1.9, 2.6, 0.12)
    caja(cuero(), 0, 4.2, 2.67, 1.4, 1.6, 0.4)
    caja(madera_o(), 0, 2.85, 1.7, 1.6, 0.5, 0.12)
    caja(mat('pescante_chy', 0x2a1a10, 0.6), 0, 2.95, 1.82, 1.4, 0.1, 0.5)
    for s in (-1, 1):
        caja(cristal(), s * 0.86, 4.1, 1.7, 0.02, 0.9, 0.6)
        for y in (3.2, 5.0):
            cil(amarillo(), s * 0.92, y, 0.6, 0.6 if y > 4 else 0.45, 0.08, 14, eje='X')
            cil(madera_o(), s * 0.95, y, 0.6, 0.12, 0.1, 8, eje='X')
    caja(amarillo(), 0, 2.88, 1.2, 1.5, 0.04, 0.3)
    texto(negro(), 'OVERLAND', 0, 2.85, 1.35, tam=0.17, prof=0.01)

PIEZAS = {
    'capitolio_wyoming': (capitolio_wyoming, 'cheyenne',   dict(lado=2048, bisel=0.0)),
    'cheyenne_depot':    (cheyenne_depot,    'cheyenne',   dict(lado=1024, bisel=0.0)),
    'plains_hotel':      (plains_hotel,      'cheyenne',   dict(lado=1024, bisel=0.0)),
    'big_boy':           (big_boy,           'cheyenne',   dict(lado=1024, bisel=0.0)),
    'bota_gigante':      (bota_gigante,      'cheyenne',   dict(lado=256, bisel=0.0)),
    'arco_cheyenne':     (arco_cheyenne,     'cheyenne',   dict(lado=1024, bisel=0.0, suelo=False)),
    'arena_rodeo':       (arena_rodeo,       'cheyenne',   dict(lado=2048, bisel=0.0, suelo=False)),
    'toro_rodeo':        (toro_rodeo,        'obstaculos', dict(lado=256, bisel=0.0)),
    'barril_rodeo':      (barril_rodeo,      'obstaculos', dict(lado=256, bisel=0.0)),
    'valla_rodeo':       (valla_rodeo,       'obstaculos', dict(lado=256, bisel=0.0)),
    'payaso_barril':     (payaso_barril,     'obstaculos', dict(lado=256, bisel=0.0)),
    'cartel_rodeo':      (cartel_rodeo,      'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
    'diligencia':        (diligencia,        'obstaculos', dict(lado=256, bisel=0.0)),
}

correr(PIEZAS)
