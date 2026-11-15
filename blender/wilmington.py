# Nivel 42: Wilmington, Delaware (15/11/2026).
#
#   blender -b -P blender/wilmington.py -- [pieza ...] [--rapido]
#
# Historia: «El pueblo de su rival dormilón: mecedoras y helados por la
#   calle». Acto del Sentido Común. Por Market Street: el teatro de la ópera
#   blanco, la heladería con el cucurucho gigante, la casa del porche lleno de
#   mecedoras y las mecedoras en las aceras. Las gallinas azules de Delaware
#   (la Blue Hen) se apartan si vas por su carril: hay que meterse en el último
#   momento para cogerlas; el momento estrella, el paseo marítimo de Rehoboth
#   con la torre de helado (cada bola se apila en el cucurucho y se tambalea
#   al cambiar de carril). Final en la estación de Wilmington, con su torre.
#   Pancarta del Sentido Común: EL HELADO SE DERRITE.
# Obstáculos (carpeta obstaculos): la gallina azul, el cucurucho caído, la
# mecedora, el camión de los helados y la pancarta.

import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import *

def blanco():    return mat('blanco_wil', 0xf6f4ee, 0.5)
def negro():     return mat('negro_wil', 0x1c1c20, 0.4)
def cristal():   return mat('cristal_wil', 0x3a5a70, 0.15)
def rojo():      return mat('rojo_wil', 0xc8202a, 0.45)
def azul():      return mat('azul_wil', 0x1e4a9a, 0.45)
def azul_g():    return mat('azul_gallina_wil', 0x3a6ab8, 0.5)
def amarillo():  return mat('amarillo_wil', 0xf2c21a, 0.45)
def rosa():      return mat('rosa_wil', 0xf08aa8, 0.5)
def menta():     return mat('menta_wil', 0x9ae0c0, 0.5)
def chocolate(): return mat('chocolate_wil', 0x6a3a22, 0.6)
def galleta():   return mat('galleta_wil', 0xd8a050, 0.7)
def gris():      return mat('gris_wil', 0x8a9098, 0.4)
def hierro():    return mat('hierro_wil', 0x2a2c30, 0.45)
def madera():    return mat('madera_wil', 0x9a6a3e, 0.85)
def madera_o():  return mat('madera_oscura_wil', 0x5a3a22, 0.85)
def ladrillo():  return mat_bloques('ladrillo_wil', 0xa85a3e, 0x7a4030, ancho=0.4, alto=0.16)
def piedra_l():  return mat('piedra_lisa_wil', 0xe4e0d8, 0.6)
def arena():     return mat('arena_wil', 0xf0dcae, 0.95)
def agua():      return mat('agua_wil', 0x3a7aa8, 0.15)

def cartel_sentido(x, y, z, w, h, linea1, linea2=''):
    caja(azul(), x, y, z, w, 0.06, h)
    caja(blanco(), x, y - 0.01, z + h - h * 0.08, w, 0.06, h * 0.08)
    esfera(rosa(), x - w / 2 + h * 0.32, y - 0.06, z + h * 0.5, h * 0.24, 1, esc=(1.2, 0.4, 1))
    texto(blanco(), linea1, x + h * 0.25, y - 0.045, z + h * (0.5 if not linea2 else 0.56), tam=h * 0.3, prof=0.02)
    if linea2:
        texto(amarillo(), linea2, x + h * 0.25, y - 0.045, z + h * 0.2, tam=h * 0.2, prof=0.02)

def mecedora_m(x, y, z=0.0, k=1.0, giro=0.0):
    """Una mecedora de madera blanca (de frente a -y)."""
    m = blanco()
    for s in (-1, 1):
        o = cil(m, x + s * 0.32 * k, y, z + 0.12 * k, 0.6 * k, 0.05 * k, 16, eje='X', r2=None)
        o.scale = (1, 1, 0.25)
        cil(m, x + s * 0.3 * k, y - 0.2 * k, z + 0.1 * k, 0.03 * k, 0.38 * k, 6)
        cil(m, x + s * 0.3 * k, y + 0.25 * k, z + 0.1 * k, 0.03 * k, 0.95 * k, 6)
    caja(m, x, y, z + 0.48 * k, 0.65 * k, 0.55 * k, 0.05 * k)
    for i in range(4):
        caja(m, x - 0.24 * k + i * 0.16 * k, y + 0.25 * k, z + 0.55 * k, 0.05 * k, 0.04 * k, 0.5 * k)
    caja(m, x, y + 0.25 * k, z + 1.02 * k, 0.65 * k, 0.05 * k, 0.06 * k)

def cucurucho_m(x, y, z, k=1.0, bolas=((rosa,), (chocolate,), (menta,))):
    cil(galleta(), x, y, z, 0.05 * k, 0.9 * k, 12, r2=0.32 * k)
    for i, (c,) in enumerate(bolas):
        esfera(c(), x, y, z + 1.05 * k + i * 0.42 * k, 0.33 * k, 2)

# ================================================================ la meta
def estacion_wilmington():
    """La estación de Wilmington (1908): ladrillo rojo y piedra, los arcos de
    la entrada, la torre del reloj con su tejado alto y el andén elevado; la
    pancarta del Sentido Común delante."""
    Y = 16
    W, D, H = 50.0, 16.0, 11.0
    yf = Y - D / 2
    l = ladrillo()
    caja(l, 0, Y, 0, W, D, H)
    caja(piedra_l(), 0, Y, H, W + 0.4, D + 0.4, 0.6)
    tejado(mat('tejado_wil', 0x5a4a44, 0.6), 0, Y - D / 2, Y + D / 2, H + 0.6, W, 4, cumbrera='x')
    for k in range(10):
        x = -22 + k * 4.9
        cil(piedra_l(), x, yf - 0.06, 4.8, 1.4, 0.12, 14, eje='Y')
        caja(cristal(), x, yf - 0.05, 1.0, 2.6, 0.1, 3.8)
        ventana(x, 7.4, 1.6, 2.4, y=yf - 0.05, marco=piedra_l(), cristal=cristal())
    T = 6.4
    caja(l, 0, yf - 1, 0, T, T, 26)
    for z in (11, 19):
        caja(piedra_l(), 0, yf - 1, z, T + 0.4, T + 0.4, 0.6)
    cil(blanco(), 0, yf - 1 - T / 2 - 0.1, 22.5, 2.1, 0.15, 24, eje='Y')
    caja(negro(), 0, yf - 1 - T / 2 - 0.22, 22.5, 0.12, 0.04, 1.6)
    caja(negro(), 0.45, yf - 1 - T / 2 - 0.22, 22.5, 1.0, 0.04, 0.12)
    o = cil(mat('tejado_torre_wil', 0x4a5a6a, 0.6), 0, yf - 1, 26, T * 0.74, 7, 4, r2=0.2)
    o.rotation_euler = (0, 0, math.pi / 4)
    caja(blanco(), 0, yf - 4.3, 12.2, 14, 0.1, 1.2)
    texto(rojo(), 'WILMINGTON STATION', 0, yf - 4.36, 12.45, tam=0.75, prof=0.03)
    caja(mat('acera_wil', 0xb8b4ac, 0.8), 0, yf - 12, -0.05, 70, 22, 0.06)
    for k, x in enumerate((-26, -20, 20, 26)):
        mecedora_m(x, yf - 5, 0, 1.4)
    for x in (8, 22):
        cil(madera_o(), x, yf - 15, 0, 0.12, 4.4, 8)
    cartel_sentido(15, yf - 15, 2.8, 14, 1.6, 'EL HELADO SE DERRITE', 'EL SENTIDO COMÚN')

# ================================================================ edificios
def opera_wilmington():
    """El teatro de la ópera (1871): la fachada blanca de hierro fundido con
    ventanas de arco, la cornisa y el letrero GRAND OPERA HOUSE."""
    Y = 8
    W, D, H = 22.0, 12.0, 16.0
    yf = Y - D / 2
    b = blanco()
    caja(b, 0, Y, 0, W, D, H)
    caja(piedra_l(), 0, Y, H, W + 0.6, D + 0.6, 1.2)
    for k in range(5):
        x = -8 + k * 4
        for z in (2.0, 7.0, 11.5):
            caja(cristal(), x, yf - 0.05, z, 2.0, 0.1, 3.0)
            cil(b, x, yf - 0.08, z + 3.0, 1.1, 0.12, 12, eje='Y')
        cil(b, x + 2, yf - 0.3, 0, 0.18, H, 8)
    caja(amarillo(), 0, yf - 0.15, 14.6, 14, 0.1, 1.0)
    texto(negro(), 'GRAND OPERA HOUSE', 0, yf - 0.21, 14.8, tam=0.6, prof=0.03)

def heladeria():
    """La heladería de la calle: el local de rayas rosas y blancas, el toldo,
    el escaparate de colores y el cucurucho gigante en el tejado."""
    Y = 7
    yf = Y - 5
    caja(mat_franjas('heladeria_wil', 0xf08aa8, 0xf6f4ee, 12, eje='X', z0=-7, alto=14), 0, Y, 0, 14, 10, 6)
    caja(blanco(), 0, Y, 6, 14.4, 10.4, 0.4)
    caja(cristal(), 0, yf - 0.05, 0.6, 10, 0.1, 2.8)
    for k in range(8):
        esfera([rosa, chocolate, menta, amarillo][k % 4](), -4 + k * 1.15, yf - 0.3, 1.0, 0.35, 1)
    caja(mat_franjas('toldo_hel_wil', 0xf08aa8, 0xf6f4ee, 10, eje='X', z0=-6, alto=12), 0, yf - 1, 3.6, 12, 2, 0.12, inclina=0.3)
    caja(blanco(), 0, yf - 0.1, 4.6, 8, 0.12, 1.0)
    texto(rosa(), 'ICE CREAM', 0, yf - 0.18, 4.8, tam=0.7, prof=0.03)
    cucurucho_m(0, Y, 6.4, 3.0)

def casa_mecedoras():
    """La casa de madera con el porche corrido lleno de mecedoras (en el
    pueblo del rival dormilón, todos se mecen)."""
    Y = 8
    W, D = 16.0, 10.0
    yf = Y - D / 2
    caja(mat('tablas_casa_wil', 0xe8e0cc, 0.85), 0, Y, 0, W, D, 7)
    tejado(mat('tejado_casa_wil', 0x4a5a6a, 0.6), 0, Y - D / 2, Y + D / 2, 7, W, 3.2, cumbrera='x')
    caja(madera(), 0, yf - 1.6, 0, W, 3.2, 0.5)
    caja(blanco(), 0, yf - 1.6, 3.4, W, 3.2, 0.15)
    for x in (-7.5, -2.5, 2.5, 7.5):
        cil(blanco(), x, yf - 3.1, 0.5, 0.12, 2.9, 8)
    for k in range(5):
        mecedora_m(-6 + k * 3, yf - 1.6, 0.5, 1.0)
    for x in (-5, 5):
        ventana(x, 1.4, 1.6, 2.0, y=yf - 0.05, marco=blanco(), cristal=cristal())
        ventana(x, 4.4, 1.4, 1.8, y=yf - 0.05, marco=blanco(), cristal=cristal())
    puerta(0, 0.5, 1.2, 2.4, y=yf - 0.05, color=0x2a4a6a, marco=blanco())

def mecedora():
    """Una mecedora blanca en la acera."""
    mecedora_m(0, 0, 0, 1.2)

# ================================================================ cruza la calle
def arco_first_state():
    """El arco de Delaware: DELAWARE · THE FIRST STATE (el primer estado en
    firmar la Constitución), con la gallina azul encima; por detrás, ZZZ…"""
    for s in (-1, 1):
        caja(azul(), s * 8.6, 0, 0, 0.6, 0.6, 7.8)
    caja(azul(), 0, 0, 7.0, 18.0, 0.4, 0.5)
    caja(amarillo(), 0, 0, 4.4, 12, 0.18, 1.8)
    texto(azul(), 'DELAWARE', 0, -0.12, 5.3, tam=0.8, prof=0.04)
    texto(negro(), 'THE FIRST STATE', 0, -0.12, 4.65, tam=0.45, prof=0.04)
    o = texto(azul(), 'ZZZ…', 0, 0.12, 5.0, tam=0.9, prof=0.04)
    o.rotation_euler = (math.pi / 2, 0, math.pi)
    gallina_m(0, 0, 7.5, 1.8)

def gallina_m(x, y, z, k=1.0):
    """La gallina azul de Delaware (Blue Hen), de frente a -y."""
    c = azul_g()
    esfera(c, x, y, z + 0.4 * k, 0.32 * k, 2, esc=(0.9, 1.1, 0.9))
    esfera(c, x, y - 0.25 * k, z + 0.72 * k, 0.17 * k, 2)
    cil(amarillo(), x, y - 0.42 * k, z + 0.72 * k, 0.05 * k, 0.12 * k, 6, eje='Y', r2=0.0)
    for s in (-1, 1):
        esfera(negro(), x + s * 0.08 * k, y - 0.38 * k, z + 0.78 * k, 0.025 * k, 1)
        esfera(c, x + s * 0.28 * k, y + 0.05 * k, z + 0.42 * k, 0.16 * k, 1, esc=(0.4, 1.1, 0.8))
        cil(amarillo(), x + s * 0.1 * k, y, z, 0.025 * k, 0.15 * k, 4)
    cil(rojo(), x, y - 0.25 * k, z + 0.88 * k, 0.07 * k, 0.1 * k, 6)
    rama(c, (x, y + 0.25 * k, z + 0.5 * k), (x, y + 0.45 * k, z + 0.8 * k), 0.12 * k, 0.04 * k, 5)

# ================================================================ el paseo marítimo
def paseo_rehoboth():
    """El paseo marítimo de Rehoboth Beach (momento estrella, al aire libre):
    la tarima de madera, la arena y el mar a un lado, las tiendas de helados,
    patatas y la sala de juegos al otro, las gaviotas en los postes y los
    arcos de SALIDA y META. Cruza la calle: el origen en el centro."""
    L = 420
    caja(mat_bloques('tarima_reh_wil', 0xb8946a, 0x8a6a4a, ancho=4.0, alto=0.22, grosor=0.02), 0, 0, -0.2, 22, L, 0.2)
    caja(arena(), 22, 0, -0.3, 22, L, 0.2)
    caja(agua(), 50, 0, -0.4, 34, L, 0.2)
    for k in range(int(L / 10)):
        caja(mat('espuma_wil', 0xe8f4fa, 0.6), 33.5, -L / 2 + 5 + k * 10, -0.18, 1.0, 6, 0.04)
    tiendas = [(0xf08aa8, 'ICE CREAM'), (0xf2c21a, 'FRIES'), (0x2a6ab8, 'FUNLAND'), (0x9ae0c0, 'TAFFY'), (0xf6f4ee, 'PIZZA')]
    for k in range(int(L / 14)):
        y = -L / 2 + 7 + k * 14
        c, txt = tiendas[k % 5]
        caja(mat(f'tienda_reh_wil{k % 5}', c, 0.7), -15, y, 0, 8, 12, 5 + (k % 2))
        caja(cristal(), -10.95, y, 0.4, 0.1, 9, 2.6)
        caja(blanco(), -10.9, y, 3.6, 0.1, 9, 0.9)
        texto(negro(), txt, -10.85, y, 3.8, tam=0.55, prof=0.02).rotation_euler = (math.pi / 2, 0, -math.pi / 2)
    for k in range(int(L / 9)):
        y = -L / 2 + 4.5 + k * 9
        cil(madera_o(), 11, y, 0, 0.12, 1.2, 6)
        caja(madera_o(), 11, y, 1.0, 0.1, 9, 0.1)
        if k % 3 == 0:
            esfera(blanco(), 11, y, 1.45, 0.22, 1, esc=(0.8, 1.2, 0.8))
            esfera(blanco(), 11, y - 0.2, 1.65, 0.12, 1)
            cil(amarillo(), 11, y - 0.35, 1.65, 0.03, 0.12, 4, eje='Y', r2=0.0)
    for k in range(int(L / 30)):
        y = -L / 2 + 15 + k * 30
        cil(mat_franjas(f'sombrilla_reh_wil{k % 2}', [0xf08aa8, 0x2a6ab8][k % 2], 0xf6f4ee, 6, eje='Z', z0=2.0, alto=0.5), 20, y, 2.0, 1.4, 0.5, 12, r2=0.05)
        cil(blanco(), 20, y, -0.2, 0.04, 2.2, 4)
    for (y, txt) in ((-L / 2 + 1, 'SALIDA'), (L / 2 - 1, 'META')):
        for s in (-1, 1):
            caja(madera(), s * 7.0, y, 0, 0.5, 0.5, 6.0)
        caja(madera(), 0, y, 5.4, 14.6, 0.5, 0.5)
        caja(rosa(), 0, y, 3.9, 10, 0.16, 1.4)
        texto(blanco(), 'REHOBOTH · ' + txt, 0, y - 0.1, 4.35, tam=0.55, prof=0.04)
        cucurucho_m(-5, y, 5.9, 1.2)
        cucurucho_m(5, y, 5.9, 1.2)

# ================================================================ obstáculos
def gallina_azul():
    """La gallina azul de Delaware (se coge: se aparta si vas por su carril)."""
    gallina_m(0, 0, 0, 1.3)

def cucurucho_caido():
    """El cucurucho gigante caído en la calle, con el helado derretido (se salta)."""
    o = cil(galleta(), 0.3, 0, 0.35, 0.05, 1.2, 12, r2=0.38)
    o.rotation_euler = (0, math.pi / 2, 0)
    o.location = (0.3, 0, 0.38)
    esfera(rosa(), -0.5, 0, 0.3, 0.42, 2, esc=(1, 1, 0.75))
    esfera(rosa(), -0.6, 0, 0.02, 0.7, 2, esc=(1.2, 1.0, 0.08))

def mecedora_obst():
    """Una mecedora en medio de la calle (se salta)."""
    mecedora_m(0, 0, 0, 1.0)

def camion_helados():
    """El camión de los helados (no se pasa): blanco y rosa, con la ventanilla
    y el cucurucho en el techo. El morro en el origen."""
    b = blanco()
    caja(b, 0, 1.0, 0.45, 2.3, 2.0, 1.6)
    caja(cristal(), 0, 0.0, 1.35, 2.0, 0.1, 0.7)
    caja(b, 0, 4.3, 0.45, 2.4, 4.6, 2.6)
    for s in (-1, 1):
        caja(rosa(), s * 1.21, 4.3, 0.5, 0.05, 4.6, 0.6)
        caja(negro(), s * 1.22, 4.3, 1.5, 0.05, 2.2, 0.9)
    cucurucho_m(0, 4.3, 3.05, 1.0)
    caja(rosa(), 0, -0.02, 0.7, 2.2, 0.05, 0.3)
    texto(blanco(), 'ICE CREAM', 0, -0.04, 0.74, tam=0.18, prof=0.01)
    for (y, s) in ((1.0, 1), (5.8, 1), (1.0, -1), (5.8, -1)):
        cil(negro(), s * 1.15, y, 0.42, 0.42, 0.3, 14, eje='X')
    for s in (-1, 1):
        caja(luz('faro_helados_wil', 0xfff2c0, 1.0), s * 0.85, -0.03, 1.0, 0.35, 0.05, 0.2)

def cartel_de():
    """La pancarta del Sentido Común (agacharse): EL HELADO SE DERRITE."""
    for x in (-1.25, 1.25):
        cil(madera_o(), x, 0, 0, 0.07, 2.75, 8)
    caja(azul(), 0, 0, 1.5, 2.4, 0.05, 1.2)
    esfera(rosa(), -0.9, -0.05, 2.1, 0.2, 1, esc=(1.2, 0.4, 1))
    texto(blanco(), 'EL HELADO', 0.15, -0.035, 2.2, tam=0.22, prof=0.02)
    texto(amarillo(), 'SE DERRITE', 0.15, -0.035, 1.8, tam=0.22, prof=0.02)

PIEZAS = {
    'estacion_wilmington': (estacion_wilmington, 'wilmington', dict(lado=2048, bisel=0.0)),
    'opera_wilmington':    (opera_wilmington,    'wilmington', dict(lado=1024, bisel=0.0)),
    'heladeria':           (heladeria,           'wilmington', dict(lado=1024, bisel=0.0)),
    'casa_mecedoras':      (casa_mecedoras,      'wilmington', dict(lado=1024, bisel=0.0)),
    'mecedora':            (mecedora,            'wilmington', dict(lado=256, bisel=0.0)),
    'arco_first_state':    (arco_first_state,    'wilmington', dict(lado=1024, bisel=0.0, suelo=False)),
    'paseo_rehoboth':      (paseo_rehoboth,      'wilmington', dict(lado=2048, bisel=0.0, suelo=False)),
    'gallina_azul':        (gallina_azul,        'obstaculos', dict(lado=256, bisel=0.0)),
    'cucurucho_caido':     (cucurucho_caido,     'obstaculos', dict(lado=256, bisel=0.0)),
    'mecedora_obst':       (mecedora_obst,       'obstaculos', dict(lado=256, bisel=0.0)),
    'camion_helados':      (camion_helados,      'obstaculos', dict(lado=256, bisel=0.0)),
    'cartel_de':           (cartel_de,           'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
}

correr(PIEZAS)
