# Nivel 39: Charleston, Virginia Occidental (15/11/2026).
#
#   blender -b -P blender/charlestonwv.py -- [pieza ...] [--rapido]
#
# Historia: «Vagonetas de su "precioso carbón limpio"». Empieza el acto del
#   Sentido Común (sus pancartas, azules con el cerebro rosa, dicen cosas de
#   sentido común). Por Capitol Street una tarde de otoño: el hotel Daniel
#   Boone, la panadería de los pepperoni rolls, el cargadero de carbón con su
#   cinta y las vagonetas de las aceras. El saco de carbón: Trump recoge
#   carbón «limpio» (pesa: va más lento de un carril a otro) y lo vacía en las
#   vagonetas; el momento estrella, la vagoneta por las vías del patio de
#   carbón (solo se cambia de vía en las agujas). Final en el Capitolio de
#   Virginia Occidental, con su cúpula de oro. Pancarta: EL CARBÓN MANCHA.
# Obstáculos (carpeta obstaculos): la vagoneta del patio (se monta: es un
# vehículo), la vía cortada, la aguja, el montón de carbón y la pancarta.

import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import *

def blanco():    return mat('blanco_wv', 0xf6f4ee, 0.5)
def negro():     return mat('negro_wv', 0x1c1c20, 0.4)
def carbon():    return mat('carbon_wv', 0x1a1a1e, 0.35)
def cristal():   return mat('cristal_wv', 0x3a5a70, 0.15)
def rojo():      return mat('rojo_wv', 0xc8202a, 0.45)
def azul():      return mat('azul_wv', 0x1e4a9a, 0.45)
def amarillo():  return mat('amarillo_wv', 0xf2c21a, 0.45)
def oro():       return mat('oro_wv', 0xe8b840, 0.22)
def rosa():      return mat('rosa_cerebro_wv', 0xf08aa8, 0.5)
def gris():      return mat('gris_wv', 0x8a9098, 0.4)
def hierro():    return mat('hierro_wv', 0x3a3c40, 0.45)
def oxido():     return mat('oxido_wv', 0x8a4a2a, 0.7)
def madera():    return mat('madera_wv', 0x8a5a34, 0.85)
def madera_o():  return mat('madera_oscura_wv', 0x5a3a22, 0.85)
def caliza():    return mat_bloques('caliza_wv', 0xe0d8c4, 0xc4bca8, ancho=1.3, alto=0.6, grosor=0.008)
def caliza_l():  return mat('caliza_lisa_wv', 0xe8e0cc, 0.6)
def ladrillo():  return mat_bloques('ladrillo_wv', 0xa85a3e, 0x7a4030, ancho=0.4, alto=0.16)
def cesped():    return mat('cesped_wv', 0x6a8a3a, 0.9)

def cartel_sentido(x, y, z, w, h, linea1, linea2=''):
    """La pancarta del Sentido Común: azul, con el cerebro rosa en la esquina."""
    caja(azul(), x, y, z, w, 0.06, h)
    caja(blanco(), x, y - 0.01, z + h - h * 0.08, w, 0.06, h * 0.08)
    esfera(rosa(), x - w / 2 + h * 0.32, y - 0.06, z + h * 0.5, h * 0.24, 1, esc=(1.2, 0.4, 1))
    texto(blanco(), linea1, x + h * 0.25, y - 0.045, z + h * (0.5 if not linea2 else 0.56), tam=h * 0.3, prof=0.02)
    if linea2:
        texto(amarillo(), linea2, x + h * 0.25, y - 0.045, z + h * 0.2, tam=h * 0.2, prof=0.02)

def rieles(x, y, largo, z=0.0, paso=0.9):
    """Dos rieles con sus traviesas, a lo largo de y."""
    for s in (-1, 1):
        caja(hierro(), x + s * 0.55, y, z + 0.12, 0.1, largo, 0.12)
    if largo > 50:
        # (en el patio, las traviesas pintadas en el balasto: miles de cajas tardaban demasiado)
        caja(mat_bloques('traviesas_wv', 0x5a3a22, 0x5a5550, ancho=1.6, alto=paso, grosor=0.3), x, y, z, 1.6, largo, 0.1)
        return
    for k in range(int(largo / paso)):
        caja(madera_o(), x, y - largo / 2 + paso / 2 + k * paso, z, 1.6, 0.25, 0.12)

def arbol_otono(x, y, h, k=0):
    cil(madera_o(), x, y, 0, 0.25 * h / 8, h * 0.45, 6)
    esfera(mat(f'hoja_otono_wv{k % 3}', [0xd8782a, 0xc8a030, 0xb84a2a][k % 3], 0.85), x, y, h * 0.7, h * 0.32, 1, esc=(1, 1, 1.1))

# ================================================================ la meta
def capitolio_wv():
    """El Capitolio de Virginia Occidental (la meta): la caliza clara, el
    pórtico con columnas, las alas largas, el tambor con su columnata y la
    cúpula dorada (más alta que la del Capitolio de Washington), con la
    linterna; delante, el césped y la pancarta del Sentido Común."""
    Y = 26
    W, D, H = 70.0, 24.0, 15.0
    yf = Y - D / 2
    c = caliza()
    caja(c, 0, Y, 0, W, D, H)
    caja(caliza_l(), 0, Y, H, W + 0.6, D + 0.6, 1.0)
    for k in range(16):
        x = -33 + k * 4.4
        if abs(x) < 9:
            continue
        for z in (2.0, 7.0, 11.0):
            ventana(x, z, 1.5, 2.6, y=yf - 0.05, marco=caliza_l(), cristal=cristal())
    caja(c, 0, yf - 4, 0, 18, 8, 3.5)
    columnata(caliza_l(), -7.5, 7.5, 6, yf - 7, 3.5, 0.7, 12)
    caja(caliza_l(), 0, yf - 5, H + 0.5, 18, 6, 1.2)
    fronton(caliza_l(), 0, yf - 6, H + 1.7, 18, 3.6, 4.4)
    puerta(0, 3.5, 2.6, 4.4, y=yf - 0.05, color=0x5a3a22, marco=caliza_l())
    for k in range(10):
        caja(caliza_l(), 0, yf - 8.4 - k * 0.5, 0, 22 + k * 0.6, 0.5, 3.5 - k * 0.33)
    Z = H + 1.0
    cil(c, 0, Y, Z, 10, 4, 36)
    cil(caliza_l(), 0, Y, Z + 4, 8.6, 9, 36)
    for k in range(24):
        a = k * math.tau / 24
        cil(blanco(), math.cos(a) * 9.0, Y + math.sin(a) * 9.0, Z + 4, 0.35, 9, 10)
    cil(caliza_l(), 0, Y, Z + 13, 9.6, 1.2, 36)
    cupula(oro(), 0, Y, Z + 14.2, 8.6, 12, 36, 10)
    for k in range(16):
        a = k * math.tau / 16
        rama(mat('nervio_oro_wv', 0xc8982a, 0.3), (math.cos(a) * 8.6, Y + math.sin(a) * 8.6, Z + 14.3),
             (math.cos(a) * 1.8, Y + math.sin(a) * 1.8, Z + 25.8), 0.14, 0.08, 4)
    cil(caliza_l(), 0, Y, Z + 26, 2.0, 3.4, 12)
    for k in range(8):
        a = k * math.tau / 8
        cil(blanco(), math.cos(a) * 2.05, Y + math.sin(a) * 2.05, Z + 26, 0.15, 3.4, 6)
    cupula(oro(), 0, Y, Z + 29.4, 2.1, 2.2, 12, 4)
    cil(oro(), 0, Y, Z + 31.5, 0.15, 2.0, 6)
    esfera(oro(), 0, Y, Z + 33.6, 0.4, 1)
    caja(cesped(), 0, yf - 20, -0.05, 90, 26, 0.06)
    for k, (x, y) in enumerate(((-30, yf - 10), (-38, yf - 20), (30, yf - 10), (38, yf - 20))):
        arbol_otono(x, y, 9, k)
    for x in (8, 22):
        cil(madera_o(), x, yf - 16, 0, 0.12, 4.4, 8)
    cartel_sentido(15, yf - 16, 2.8, 14, 1.6, 'EL CARBÓN MANCHA', 'EL SENTIDO COMÚN')

# ================================================================ edificios
def daniel_boone_hotel():
    """El hotel Daniel Boone (1929): la torre de ladrillo de diez pisos con
    la base de piedra y el letrero en lo alto."""
    Y = 10
    l = ladrillo()
    caja(caliza_l(), 0, Y, 0, 24, 16, 5)
    caja(l, 0, Y, 5, 22, 14, 28)
    for k in range(6):
        x = -9 + k * 3.6
        ventana(x, 1.2, 2.4, 2.8, y=Y - 8 - 0.05, marco=caliza_l(), cristal=cristal())
        for z in range(7, 31, 3):
            ventana(x, z, 1.2, 1.8, y=Y - 7 - 0.05, marco=caliza_l(), cristal=cristal())
    caja(caliza_l(), 0, Y, 33, 22.6, 14.6, 1.0)
    for x in (-8, 8):
        caja(hierro(), x, Y - 2, 34, 0.2, 0.2, 4)
    caja(hierro(), 0, Y - 2, 37.6, 18, 0.2, 0.2)
    texto(rojo(), 'DANIEL BOONE', 0, Y - 2.1, 35.0, tam=1.6, prof=0.1)

def panaderia_pepperoni():
    """La panadería de los pepperoni rolls (el bocadillo de los mineros):
    ladrillo, el toldo a rayas, el escaparate y el gran bollo con pepperoni
    encima del letrero."""
    Y = 7
    yf = Y - 5
    caja(ladrillo(), 0, Y, 0, 14, 10, 7)
    caja(caliza_l(), 0, Y, 7, 14.4, 10.4, 0.5)
    caja(cristal(), 0, yf - 0.05, 0.6, 10, 0.1, 2.6)
    caja(mat_franjas('toldo_pan_wv', 0xc8202a, 0xf6f4ee, 10, eje='X', z0=-6, alto=12), 0, yf - 1.0, 3.4, 12, 2.0, 0.12, inclina=0.3)
    caja(blanco(), 0, yf - 0.1, 4.4, 10, 0.12, 1.2)
    texto(rojo(), 'PEPPERONI ROLLS', 0, yf - 0.18, 4.65, tam=0.75, prof=0.03)
    pan = mat('bollo_wv', 0xd8a050, 0.7)
    esfera(pan, 0, Y, 9.0, 1.5, 2, esc=(2.2, 1, 0.8))
    for k in range(5):
        cil(mat('pepperoni_wv', 0xb8382a, 0.6), -2 + k, Y - 1.4, 9.0, 0.35, 0.06, 12, eje='Y')

def tipple_carbon():
    """El cargadero de carbón: la torre de chapa sobre patas de acero, la
    cinta inclinada que sube el carbón, el montón negro y las letras COAL."""
    Y = 12
    o = oxido()
    for (x, y) in ((-5, Y - 4), (5, Y - 4), (-5, Y + 4), (5, Y + 4)):
        caja(hierro(), x, y, 0, 0.6, 0.6, 12)
    caja(o, 0, Y, 12, 12, 10, 8)
    tejado(mat('tejado_tipple_wv', 0x5a5e66, 0.6), 0, Y - 5, Y + 5, 20, 12, 3, cumbrera='x')
    rama(hierro(), (14, Y, 0.5), (4, Y, 14), 0.8, 0.8, 4)
    caja(carbon(), 0, Y, 0, 9, 7, 2.5)
    esfera(carbon(), 12, Y, 0, 4, 1, esc=(1.2, 1, 0.6))
    caja(blanco(), 0, Y - 5.1, 16, 8, 0.1, 2.0)
    texto(negro(), 'COAL', 0, Y - 5.16, 16.4, tam=1.6, prof=0.04)

def carretilla_carbon():
    """La vagoneta pequeña de las aceras, llena de carbón, en su trozo de vía."""
    rieles(0, 0, 3.0)
    caja(oxido(), 0, 0, 0.35, 1.0, 1.6, 0.8)
    for y in (-0.5, 0.5):
        for s in (-1, 1):
            cil(hierro(), s * 0.55, y, 0.3, 0.22, 0.1, 12, eje='X')
    for k in range(6):
        esfera(carbon(), -0.3 + (k % 3) * 0.3, -0.4 + (k // 3) * 0.6, 1.2, 0.25, 1)

# ================================================================ cruza la calle
def arco_wv():
    """El letrero de bienvenida sobre la calle: WILD AND WONDERFUL · WEST
    VIRGINIA, con la silueta de las montañas; por detrás, VUELVE PRONTO."""
    for s in (-1, 1):
        caja(madera_o(), s * 8.6, 0, 0, 0.6, 0.6, 7.8)
    caja(madera_o(), 0, 0, 7.0, 18.0, 0.4, 0.5)
    caja(azul(), 0, 0, 4.2, 12, 0.18, 2.0)
    for k in range(5):
        fronton(mat('monte_arco_wv', 0x2a6a3a, 0.7), -4 + k * 2, -0.12, 5.4, 2.6, 0.7, 0.05)
    texto(amarillo(), 'WILD AND WONDERFUL', 0, -0.13, 4.9, tam=0.55, prof=0.04)
    texto(blanco(), 'WEST VIRGINIA', 0, -0.13, 4.35, tam=0.45, prof=0.04)
    o = texto(amarillo(), 'VUELVE PRONTO', 0, 0.13, 5.0, tam=0.7, prof=0.04)
    o.rotation_euler = (math.pi / 2, 0, math.pi)
    for x in (-4, 4):
        cil(hierro(), x, 0, 6.2, 0.03, 0.8, 4)

# ================================================================ el patio de carbón
def patio_carbon():
    """El patio de carbón (momento estrella, al aire libre): las tres vías por
    la calle, los montones de carbón, las cintas, las tolvas aparcadas en las
    vías de los lados, los postes con luces y los montes de otoño, y los arcos
    de SALIDA y META. Cruza la calle: el origen en el centro."""
    L = 420
    caja(mat('balasto_wv', 0x5a5550, 0.95), 0, 0, -0.2, 30, L, 0.2)
    for x in (-2.2, 0, 2.2):
        rieles(x, 0, L, z=-0.02)
    for s in (-1, 1):
        rieles(s * 9, 0, L, z=-0.02)
        for k in range(int(L / 14)):
            y = -L / 2 + 7 + k * 14
            if k % 3 == 1:
                continue
            caja(oxido(), s * 9, y, 0.5, 2.6, 10, 2.6)
            caja(carbon(), s * 9, y, 3.0, 2.4, 9.6, 0.4)
            for yy in (-3.5, 3.5):
                for ss in (-1, 1):
                    cil(hierro(), s * 9 + ss * 1.2, y + yy, 0.4, 0.38, 0.15, 10, eje='X')
        for k in range(int(L / 30)):
            y = -L / 2 + 15 + k * 30
            esfera(carbon(), s * 17, y, 0, 5, 1, esc=(1, 1.6, 0.55))
            rama(hierro(), (s * 22, y + 6, 0.5), (s * 15, y + 6, 6), 0.5, 0.5, 4)
        for k in range(int(L / 24)):
            y = -L / 2 + 12 + k * 24
            cil(madera_o(), s * 6.4, y, 0, 0.12, 5.5, 6)
            caja(mat('lampara_patio_wv', 0xfff0c0, 0.3), s * 6.4, y - 0.4, 5.3, 0.4, 0.4, 0.3)
        for k in range(int(L / 22)):
            arbol_otono(s * (28 + (k % 3) * 4), -L / 2 + 10 + k * 22, 9 + (k % 3), k)
    for (y, txt) in ((-L / 2 + 1, 'SALIDA'), (L / 2 - 1, 'META')):
        for s in (-1, 1):
            caja(madera_o(), s * 5.0, y, 0, 0.5, 0.5, 6.0)
        caja(madera_o(), 0, y, 5.4, 10.6, 0.5, 0.5)
        caja(amarillo(), 0, y, 3.9, 9.0, 0.16, 1.4)
        texto(negro(), 'PATIO DE CARBÓN · ' + txt, 0, y - 0.1, 4.35, tam=0.45, prof=0.04)

# ================================================================ obstáculos
def vagoneta_carbon():
    """La vagoneta del patio (un vehículo: Trump va de pie dentro): la caja
    de chapa oxidada con su borde, las cuatro ruedas y el carbón brillante.
    El frente mira al jugador (-y); el juego le da la vuelta al montarla."""
    o = oxido()
    caja(o, 0, 1.2, 0.35, 1.5, 2.4, 0.15)
    for s in (-1, 1):
        caja(o, s * 0.72, 1.2, 0.35, 0.08, 2.4, 0.95)
    for y in (0.02, 2.38):
        caja(o, 0, y, 0.35, 1.5, 0.08, 0.95)
    caja(hierro(), 0, 1.2, 1.3, 1.6, 2.5, 0.08)
    for y in (0.5, 1.9):
        for s in (-1, 1):
            cil(hierro(), s * 0.6, y, 0.28, 0.28, 0.12, 12, eje='X')
    for k in range(4):
        esfera(carbon(), -0.4 + (k % 2) * 0.8, 1.9 + (k // 2) * 0.3, 1.1, 0.25, 1)
    caja(amarillo(), 0, -0.03, 0.8, 0.8, 0.02, 0.25)
    texto(negro(), 'Nº 270', 0, -0.04, 0.84, tam=0.13, prof=0.005)

def barrera_via():
    """La vía cortada (no se pasa): el tope de vía de vigas, la señal roja y
    blanca y el cartel VÍA CORTADA."""
    rieles(0, 0, 2.0)
    caja(hierro(), 0, 0, 0.2, 1.6, 0.6, 0.9)
    for s in (-1, 1):
        rama(hierro(), (s * 0.6, 0.3, 1.0), (s * 0.6, 1.2, 0.2), 0.08, 0.08, 4)
    caja(mat_franjas('barrera_via_wv', 0xc8202a, 0xf6f4ee, 6, eje='X', z0=-1, alto=2), 0, -0.32, 0.8, 1.9, 0.08, 0.4)
    cil(hierro(), 0.9, -0.2, 0, 0.05, 2.2, 6)
    caja(rojo(), 0.9, -0.25, 1.6, 0.8, 0.04, 0.6)
    texto(blanco(), 'VÍA', 0.9, -0.28, 1.95, tam=0.15, prof=0.01)
    texto(blanco(), 'CORTADA', 0.9, -0.28, 1.72, tam=0.13, prof=0.01)

def aguja_via():
    """La aguja (el cambio de vía): los rieles que cruzan de una vía a otra
    en los tres carriles y la señal amarilla y negra AGUJA ← → con la
    palanca. Va en el carril del medio y tapa los tres (no estorba)."""
    for x in (-1.1, 1.1):
        for s in (-1, 1):
            rama(hierro(), (x - 1.1, -3.0, 0.1 + 0.02 * s), (x + 1.1, 3.0, 0.1 + 0.02 * s), 0.05, 0.05, 4)
            rama(hierro(), (x + 1.1, -3.0, 0.1 + 0.02 * s), (x - 1.1, 3.0, 0.1 + 0.02 * s), 0.05, 0.05, 4)
    caja(mat_franjas('aguja_franjas_wv', 0xf2c21a, 0x1c1c20, 10, eje='X', z0=-3.5, alto=7), 0, -3.2, 0.0, 7.0, 0.4, 0.04)
    for s in (-1, 1):
        cil(hierro(), s * 3.6, -3.0, 0, 0.06, 2.6, 6)
        caja(amarillo(), s * 3.6, -3.06, 2.0, 1.2, 0.05, 0.7)
        texto(negro(), 'AGUJA', s * 3.6, -3.1, 2.25, tam=0.18, prof=0.01)
        texto(negro(), '← →', s * 3.6, -3.1, 2.05, tam=0.16, prof=0.01)
        rama(rojo(), (s * 4.0, -2.5, 0), (s * 4.3, -2.5, 0.8), 0.05, 0.04, 6)
        esfera(rojo(), s * 4.3, -2.5, 0.85, 0.1, 1)

def carbon_monton():
    """Un montón de carbón en la calle (se salta)."""
    for k in range(9):
        a = k * 2.1
        esfera(carbon(), math.cos(a) * 0.5 * (k % 3) / 2, math.sin(a) * 0.3 * (k % 3) / 2, 0.2 + (k % 2) * 0.15, 0.32, 1)
    esfera(carbon(), 0, 0, 0.45, 0.35, 1)

def cartel_wv():
    """La pancarta del Sentido Común (agacharse): EL CARBÓN MANCHA."""
    for x in (-1.25, 1.25):
        cil(madera_o(), x, 0, 0, 0.07, 2.75, 8)
    caja(azul(), 0, 0, 1.5, 2.4, 0.05, 1.2)
    esfera(rosa(), -0.85, -0.05, 2.1, 0.22, 1, esc=(1.2, 0.4, 1))
    texto(blanco(), 'EL CARBÓN', 0.2, -0.035, 2.2, tam=0.24, prof=0.02)
    texto(blanco(), 'MANCHA', 0.2, -0.035, 1.8, tam=0.26, prof=0.02)

PIEZAS = {
    'capitolio_wv':        (capitolio_wv,        'charlestonwv', dict(lado=2048, bisel=0.0)),
    'daniel_boone_hotel':  (daniel_boone_hotel,  'charlestonwv', dict(lado=1024, bisel=0.0)),
    'panaderia_pepperoni': (panaderia_pepperoni, 'charlestonwv', dict(lado=1024, bisel=0.0)),
    'tipple_carbon':       (tipple_carbon,       'charlestonwv', dict(lado=1024, bisel=0.0)),
    'carretilla_carbon':   (carretilla_carbon,   'charlestonwv', dict(lado=256, bisel=0.0)),
    'arco_wv':             (arco_wv,             'charlestonwv', dict(lado=1024, bisel=0.0, suelo=False)),
    'patio_carbon':        (patio_carbon,        'charlestonwv', dict(lado=2048, bisel=0.0, suelo=False)),
    'vagoneta_carbon':     (vagoneta_carbon,     'obstaculos',   dict(lado=256, bisel=0.0)),
    'barrera_via':         (barrera_via,         'obstaculos',   dict(lado=256, bisel=0.0)),
    'aguja_via':           (aguja_via,           'obstaculos',   dict(lado=256, bisel=0.0)),
    'carbon_monton':       (carbon_monton,       'obstaculos',   dict(lado=256, bisel=0.0)),
    'cartel_wv':           (cartel_wv,           'obstaculos',   dict(lado=256, bisel=0.0, suelo=False)),
}

correr(PIEZAS)
