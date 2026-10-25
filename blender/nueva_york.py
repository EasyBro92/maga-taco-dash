# Nivel 1: la Quinta Avenida de Nueva York, de la Trump Tower al Flatiron (25/10/2026).
#
#   blender -b -P blender/nueva_york.py -- [pieza ...] [--rapido]
#
# Mismo estilo tipo Pixar que washington.py. Bajando hacia el sur:
#   este (izquierda):  Trump Tower · St. Regis · catedral de San Patricio · Saks
#                      · Madison Square Park
#   oeste (derecha):   Peninsula · Santo Tomás · Rockefeller Center (Atlas y los
#                      jardines) · Biblioteca Pública (los leones) · Empire State
#   al fondo:          el Flatiron, con el camión de tacos delante
# Y tramos de relleno de 20 de ancho (piedra de antes de la guerra, cristal,
# ladrillo, tienda de lujo) mezclados para que no se repita siempre el mismo.
# Todas las fachadas en y = 0 mirando a -y.

import os, sys, math, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import *

# ---------------------------------------------------------------- materiales
def caliza():  return mat_bloques('caliza_ny', 0xe4d7bd, 0xd0c1a3, ancho=1.6, alto=0.55, grosor=0.012, variacion=1.03)
def granito(): return mat_bloques('granito_ny', 0xaaa59c, 0x8f8a80, ancho=1.2, alto=0.6, grosor=0.03, variacion=1.04)
def marmol():  return mat_bloques('marmol_ny', 0xf1ede5, 0xe0dacd, ancho=1.8, alto=0.6, grosor=0.01, variacion=1.02)
def liso():    return mat('piedra_lisa_ny', 0xeee6d5, 0.55)
def bronce():  return mat('bronce_ny', 0x3e3a33, 0.4)
def vidrio():  return mat('vidrio_ny', 0x5f86ad, 0.15)
def oscuro():  return mat('hueco_ny', 0x2b2a2e, 0.8)
def oro():     return mat('oro_ny', 0xe0b040, 0.3)
def cobre():   return mat('cobre_verde', 0x6fa596, 0.6)
def cesped():  return mat('cesped_ny', 0x6fa64c, 0.9)
def blanco():  return mat('blanco_ny', 0xfbf9f3, 0.5)

def ventanas(xs, z, w, h, remate=None, y=0.0, marco=None):
    for x in xs:
        ventana(x, z, w, h, y=y, marco=marco or bronce(), cristal=vidrio(), remate=remate)

def cornisa(W, D, z, h=0.5, vuelo=0.4, m=None):
    caja(m or liso(), 0, D / 2 - vuelo / 2, z, W, D + vuelo, h)

def columnas(x0, x1, n, y, z, r, h, m=None):
    m = m or liso()
    columnata(m, x0, x1, n, y, z, r, h, basa=m, capitel=m)

def toldo(x, z, w, color, y=0.0):
    caja(mat(f'toldo_{color:06x}', color, 0.6), x, y - 0.6, z, w, 1.2, 0.18, inclina=-0.35)

def escaparate(x, w, h=2.6, y=0.0):
    caja(bronce(), x, y - 0.05, 0.3, w + 0.2, 0.1, h + 0.2)
    caja(mat('escaparate_luz', 0xcfe3f2, 0.1), x, y - 0.09, 0.4, w, 0.04, h)

def arco_gotico(m, x, z, w, h, y=0.0):
    """Ventana o puerta gótica: rectángulo con arco apuntado encima."""
    caja(m, x, y - 0.05, z, w + 0.3, 0.12, h)
    fronton(m, x, y - 0.11, z + h, w + 0.3, w * 0.9, 0.12)


# ---------------------------------------------------------------- tramos de relleno
def clasico(nombre='clasico', color=0xe4d7bd):
    """Edificio de piedra de antes de la guerra: tiendas abajo con toldos y
    seis plantas de ventanas con su cornisa."""
    W, H, D = 20, 24, 14
    piedra = mat_bloques(f'piedra_{nombre}', color, 0xcbbd9f, ancho=1.4, alto=0.5, grosor=0.012, variacion=1.03)
    caja(granito(), 0, D / 2, 0, W, D, 4.2)
    caja(piedra, 0, D / 2, 4.2, W, D, H - 4.2)
    for x, c in ((-6, 0x2d5a3a), (0, 0x7a2a32), (6, 0x22314f)):
        escaparate(x, 4.6)
        toldo(x, 3.3, 5.2, c)
    caja(liso(), 0, D / 2, 4.2, W + 0.2, D + 0.2, 0.4)
    for k in range(6):
        ventanas([-7.5, -4.5, -1.5, 1.5, 4.5, 7.5], 5.2 + k * 2.9, 1.3, 2.0,
                 remate='fronton' if k == 0 else ('cornisa' if k % 2 else None))
    cornisa(W, D, H, 0.7, 0.6)

def cristal_alto():
    """Torre de oficinas de cristal: el muro cortina entero y un vestíbulo alto."""
    W, H, D = 20, 34, 14
    caja(mat_ventanas('muro_ny', 0x6b93b8, 0xa9b6c2, paso_x=1.5, paso_z=2.6, hueco_x=1.38, hueco_z=2.35, variacion=1.15),
         0, D / 2, 5, W, D, H - 5)
    caja(mat('granito_negro', 0x34363b, 0.3), 0, D / 2 + 1, 0, W, D - 2, 5)
    caja(mat('vestibulo_ny', 0xcfe3f2, 0.1), 0, 0.95, 0.2, W - 2, 0.05, 4.6)
    for x in (-8, -4, 0, 4, 8):
        caja(mat('granito_negro', 0x34363b, 0.3), x, 0.4, 0, 0.8, 0.8, 5)
    caja(mat('marco_ny', 0x8b9198, 0.4), 0, D / 2, H, W + 0.3, D + 0.3, 0.6)

def ladrillo():
    """Ladrillo con remates de piedra y el depósito de agua en el tejado."""
    W, H, D = 20, 20, 14
    lad = mat_bloques('ladrillo_ny', 0xa9573f, 0xdccfba, ancho=0.4, alto=0.15, grosor=0.012, mezcla=0.7)
    caja(caliza(), 0, D / 2, 0, W, D, 4.0)
    caja(lad, 0, D / 2, 4.0, W, D, H - 4.0)
    escaparate(-5, 7)
    escaparate(5, 7)
    toldo(-5, 3.2, 7.4, 0xb8862b)
    toldo(5, 3.2, 7.4, 0x2d5a3a)
    for k in range(5):
        ventanas([-7, -3.5, 0, 3.5, 7], 5.0 + k * 2.9, 1.4, 2.1, remate='cornisa', marco=blanco())
    cornisa(W, D, H, 0.6, 0.5, m=caliza())
    madera = mat('madera_deposito', 0x8c5a36, 0.8)
    for dx in (-0.6, 0.6):
        for dy in (-0.6, 0.6):
            cil(bronce(), 5 + dx, 6 + dy, H + 0.6, 0.08, 1.4, 6)
    cil(madera, 5, 6, H + 2.0, 1.0, 1.8, 16)
    cil(mat('tejadillo', 0x5b4a3e, 0.8), 5, 6, H + 3.8, 1.08, 0.8, 16, r2=0.06)

def tienda_lujo(nombre='lujo', color=0xd8cfc0):
    """Tienda de lujo: piedra clara, escaparates de dos plantas y banderolas."""
    W, H, D = 20, 18, 14
    piedra = mat_bloques(f'piedra_{nombre}', color, 0xc2b8a6, ancho=2.0, alto=0.7, grosor=0.01)
    caja(piedra, 0, D / 2, 0, W, D, H)
    for x in (-6, 0, 6):
        escaparate(x, 4.4, h=6.0)
    caja(oro(), 0, -0.12, 6.8, W - 1, 0.1, 0.25)
    ventanas([-6, -2, 2, 6], 8.4, 1.5, 2.4)
    ventanas([-6, -2, 2, 6], 12.2, 1.5, 2.4)
    for x in (-8.5, 8.5):
        cil(bronce(), x, -0.4, 7.5, 0.05, 2.0, 6, eje='Y')
        caja(mat(f'banderola_{nombre}', 0x22314f, 0.5), x, -1.1, 6.0, 0.06, 0.9, 2.2)
    cornisa(W, D, H, 0.6, 0.4)


# ---------------------------------------------------------------- piezas únicas
def torre_trump():
    """La Trump Tower: cristal oscuro en dientes de sierra, letras doradas y la entrada."""
    W, H, D = 30, 46, 16
    negro = mat_ventanas('cristal_trump', 0x2a2e36, 0x1c1f25, paso_x=1.4, paso_z=2.4, hueco_x=1.25, hueco_z=2.1, variacion=1.25)
    caja(negro, 0, D / 2, 0, W, D, H)
    for k in range(5):                                                     # escalones con árboles
        z = 6 + k * 3
        caja(negro, -W / 2 + 2.5 + k * 1.5, 1.5 + k * 1.2, z, 5 - k * 0.6, 3, 3)
        for j in range(2):
            esfera(mat('arbol_terraza', 0x4f8f45, 0.8), -W / 2 + 2 + k * 1.5 + j * 1.6, 0.4 + k * 1.2, z + 3.6, 0.8, 1)
    caja(oro(), 0, -0.15, 5.8, 22, 0.25, 1.6)                              # rótulo
    texto(mat('letras_trump', 0xf4cf55, 0.25), 'TRUMP TOWER', 0, -0.32, 6.6, tam=1.25, prof=0.16)
    caja(oro(), 0, -0.8, 4.4, 9, 1.6, 0.3)                                  # marquesina
    caja(mat('puerta_trump', 0xd9b45a, 0.3), 0, -0.04, 0, 6, 0.08, 4.4)
    for x in (-3, 0, 3):
        caja(oscuro(), x, -0.1, 0.4, 2.2, 0.05, 3.6)
    for x in (-10, -6, 6, 10):
        cil(mat('asta', 0xd8d8d8, 0.3), x, -1.0, 4.4, 0.06, 4.0, 8)
        caja(mat_franjas('franjas_ny', 0xd8283a, 0xffffff, 7, z0=7.2, alto=1.0), x + 0.95, -1.0, 7.2, 1.8, 0.04, 1.0)
        caja(mat('azul_bandera', 0x1f3c88), x + 0.45, -1.03, 7.75, 0.8, 0.03, 0.45)

def st_regis():
    """Hotel St. Regis: Beaux-Arts de caliza con mansarda de cobre."""
    W, H, D = 30, 22, 16
    caja(granito(), 0, D / 2, 0, W, D, 4.5)
    caja(caliza(), 0, D / 2, 4.5, W, D, H - 4.5)
    caja(mat('marquesina_r', 0x2d2d2d, 0.4), 0, -1.2, 4.0, 8, 2.4, 0.3)
    escaparate(-9, 6, 3)
    escaparate(9, 6, 3)
    for k in range(5):
        ventanas([-12, -8, -4, 0, 4, 8, 12], 5.4 + k * 3.0, 1.3, 2.1, remate='fronton' if k % 2 == 0 else 'cornisa')
    cornisa(W, D, H, 0.7, 0.6)
    tejado(cobre(), 0, 0.6, D - 0.6, H + 0.7, W, 4.0, vuelo=0.2, cumbrera='x')
    for x in (-10, -5, 0, 5, 10):
        cil(liso(), x, 0.4, H + 2.0, 0.6, 0.5, 18, eje='Y')

def peninsula():
    """Hotel Peninsula: caliza con banderas y mansarda."""
    W, H, D = 30, 22, 16
    caja(caliza(), 0, D / 2, 0, W, D, H)
    caja(granito(), 0, D / 2, 0, W + 0.1, D + 0.1, 4.0)
    caja(oro(), 0, -1.0, 4.0, 10, 2.0, 0.25)
    for k in range(5):
        ventanas([-12, -8, -4, 0, 4, 8, 12], 5.0 + k * 3.0, 1.3, 2.1, remate='cornisa')
    ventanas([-12, -8, 8, 12], 0.8, 1.8, 2.4)
    cornisa(W, D, H, 0.7, 0.6)
    tejado(mat('pizarra_ny', 0x5c6672, 0.6), 0, 0.6, D - 0.6, H + 0.7, W, 3.6, vuelo=0.2, cumbrera='x')
    for k in range(4):
        x = -9 + k * 6
        cil(mat('asta', 0xd8d8d8, 0.3), x, -0.6, 5.0, 0.05, 3.5, 6)
        caja(mat('bandera_pen', 0xc8a34a, 0.5), x + 0.8, -0.6, 7.3, 1.5, 0.04, 1.0)

def santo_tomas():
    """Iglesia de Santo Tomás: gótica, con su torre a un lado."""
    W, D = 30, 20
    piedra = mat_bloques('piedra_gotica', 0xc9c0ae, 0xaea591, ancho=1.0, alto=0.5, grosor=0.02, variacion=1.04)
    caja(piedra, 0, D / 2, 0, W - 8, D, 16)
    hastial(piedra, 0, 0, D, 16, W - 8, 7)
    tejado(mat('pizarra_ny', 0x5c6672, 0.6), 0, 0, D, 16, W - 8, 7, vuelo=0.3)
    arco_gotico(oscuro(), -2, 0, 5, 7)
    cil(mat('rosetón', 0x7a5aa8, 0.3), -2, -0.12, 11, 2.2, 0.1, 24, eje='Y')
    cil(piedra, -2, -0.06, 11, 2.6, 0.08, 24, eje='Y')
    tx = W / 2 - 4
    caja(piedra, tx, D / 2 - 3, 0, 8, 8, 30)
    for z in (12, 20):
        arco_gotico(oscuro(), tx, z, 1.6, 4, y=D / 2 - 7)
    for dx in (-3.4, 3.4):
        cil(piedra, tx + dx, D / 2 - 6.6, 30, 0.6, 3, 4, r2=0.0)
    caja(liso(), tx, D / 2 - 3, 30, 8.6, 8.6, 0.6)

def catedral():
    """Catedral de San Patricio: gótica de mármol blanco con las dos agujas."""
    W, D = 60, 30
    piedra = mat_bloques('marmol_catedral', 0xefeae0, 0xd9d3c4, ancho=1.2, alto=0.5, grosor=0.012, variacion=1.03)
    caja(piedra, 0, D / 2, 0, 30, D, 22)                                   # nave
    hastial(piedra, 0, 0, D, 22, 30, 10)
    tejado(mat('cobre_cat', 0x7fa596, 0.6), 0, 0, D, 22, 30, 10, vuelo=0.3)
    arco_gotico(mat('puerta_cat', 0x5c4a32, 0.5), 0, 0, 6, 10, y=-0.2)
    cil(mat('roseton_cat', 0x5a6fb8, 0.3), 0, -0.15, 16, 4.0, 0.1, 32, eje='Y')
    cil(piedra, 0, -0.1, 16, 4.6, 0.08, 32, eje='Y')
    for s in (-1, 1):                                                       # las dos torres
        tx = s * 12
        caja(piedra, tx, 4, 0, 9, 8, 34)
        arco_gotico(mat('puerta_cat', 0x5c4a32, 0.5), tx, 0, 3, 7, y=0)
        for z in (12, 20, 27):
            arco_gotico(oscuro(), tx, z, 1.8, 4.5, y=0)
        cil(piedra, tx, 4, 34, 4.6, 26, 8, r2=0.0)                         # aguja
        for dx in (-4, 4):
            cil(piedra, tx + dx, 0.6, 34, 0.5, 6, 4, r2=0.0)
        cil(oro(), tx, 4, 60, 0.15, 2.4, 6)
    for s in (-1, 1):                                                       # cuerpos bajos a los lados
        caja(piedra, s * 24, D / 2 + 2, 0, 12, D - 4, 14)
        for k in range(2):
            arco_gotico(oscuro(), s * (21 + k * 6), 3, 2.4, 7, y=2)
    escalinata(piedra, 0, -0.2, 0, 26, 4, huella=0.5, tabica=0.25)

def rockefeller():
    """Rockefeller Center: los jardines del canal, el Atlas dorado y el 30 Rock detrás."""
    W, D = 60, 30
    deco = mat_ventanas('deco_rock', 0x3a4a5e, 0xd8cdb6, paso_x=1.6, paso_z=3.0, hueco_x=0.8, hueco_z=2.2, variacion=1.3)
    for s in (-1, 1):                                                       # los dos edificios bajos
        caja(deco, s * 21, D / 2, 0, 18, D, 24)
        caja(liso(), s * 21, D / 2, 24, 18.4, D + 0.4, 0.6)
        escaparate(s * 21, 12, 3.2)
    caja(deco, 0, D + 6, 0, 22, 12, 70)                                    # 30 Rock al fondo
    caja(liso(), 0, D + 6, 70, 22.4, 12.4, 0.8)
    caja(mat('losas_rock', 0xc9c2b4, 0.8), 0, D / 2, 0, 24, D, 0.12)      # el paseo
    for y in (5, 11, 17, 23):                                               # parterres y fuentes
        for s in (-1, 1):
            caja(granito(), s * 5, y, 0, 6, 4, 0.6)
            caja(mat('flores_rock', 0xe8486a, 0.8), s * 5, y, 0.6, 5.6, 3.6, 0.3)
        cil(mat('agua_ny', 0x6fa7c9, 0.1), 0, y, 0, 1.2, 0.5, 16)
    # Atlas sosteniendo los cielos, delante
    caja(granito(), 0, 1.5, 0, 3.5, 3.5, 2.5)
    caja(oro(), 0, 1.5, 2.5, 1.2, 0.8, 2.6)
    esfera(oro(), 0, 1.5, 5.6, 0.4, 2)
    cil(oro(), 0, 1.5, 7.5, 2.8, 0.15, 24, eje='X')
    cil(oro(), 0, 1.5, 7.5, 2.8, 0.15, 24, eje='Y')
    for k in range(10):                                                     # banderas del rink
        x = -10 + k * 2.2
        cil(mat('asta', 0xd8d8d8, 0.3), x, -1.0, 0, 0.05, 6.0, 6)
        c = (0xd8283a, 0x1f3c88, 0xf2c23a, 0x2fa84f, 0xffffff)[k % 5]
        caja(mat(f'bandera_rock_{c:06x}', c, 0.5), x + 0.7, -1.0, 5.0, 1.3, 0.04, 0.8)

def saks():
    """Saks: almacenes de caliza con toldos verdes y escaparates."""
    W, H, D = 40, 20, 16
    caja(caliza(), 0, D / 2, 0, W, D, H)
    for x in (-15, -9, -3, 3, 9, 15):
        escaparate(x, 4.6, 3.2)
        toldo(x, 3.9, 5.0, 0x2a5a3e)
    for k in range(4):
        ventanas([-16, -12, -8, -4, 0, 4, 8, 12, 16], 5.6 + k * 3.2, 1.4, 2.2, remate='cornisa' if k == 0 else None)
    cornisa(W, D, H, 0.7, 0.6)
    for x in (-12, 0, 12):
        cil(mat('asta', 0xd8d8d8, 0.3), x, -0.5, 6.0, 0.05, 3.0, 6, eje='Y')
        caja(mat_franjas('franjas_ny', 0xd8283a, 0xffffff, 7, z0=7.2, alto=1.0), x, -1.6, 6.2, 0.04, 1.6, 1.0)

def biblioteca():
    """Biblioteca Pública de Nueva York: mármol, tres arcos, columnas, escalinata y los leones."""
    W, H, D = 60, 18, 20
    caja(marmol(), 0, D / 2, 0, W, D, H)
    caja(marmol(), 0, D / 2, H, W - 16, D - 2, 3)
    escalinata(marmol(), 0, -0.2, 0, 36, 8, huella=0.5, tabica=0.25)
    caja(marmol(), 0, -2.5, 2.0, 30, 5, 1.0)                               # la terraza
    for x in (-8, 0, 8):                                                    # los tres arcos
        caja(oscuro(), x, -0.05, 3.0, 4.0, 0.1, 8)
        cil(oscuro(), x, -0.05, 11.0, 2.0, 0.1, 24, eje='Y')
    columnas(-13, 13, 8, -0.8, 3.0, 0.6, 11)
    caja(liso(), 0, D / 2 - 0.5, 14, 32, D + 1, 1.2)
    for x in (-24, -20, 20, 24):
        ventanas([x], 4, 1.6, 3.0, remate='fronton')
        ventanas([x], 9.5, 1.4, 2.4)
    for s in (-1, 1):                                                       # Paciencia y Fortaleza
        lx = s * 15
        caja(marmol(), lx, -6.5, 0, 3.0, 5.0, 2.2)
        piel = mat('leon', 0xe8e1d2, 0.6)
        caja(piel, lx, -6.5, 2.2, 1.6, 3.6, 1.2)
        esfera(piel, lx, -8.2, 3.6, 0.8, 2, esc=(1, 0.9, 1.1))
        esfera(mat('melena', 0xdcd3c0, 0.7), lx, -7.8, 3.6, 1.0, 2, esc=(1.1, 0.7, 1.2))
        caja(piel, lx, -5.0, 3.0, 0.8, 1.5, 0.6)
    for x in (-27, 27):
        cil(mat('asta', 0xd8d8d8, 0.3), x, -3, 0, 0.08, 9, 8)
        caja(mat_franjas('franjas_bib', 0xd8283a, 0xffffff, 7, z0=7.3, alto=1.5), x + 1.4, -3, 7.3, 2.7, 0.04, 1.5)

def empire():
    """Empire State: caliza en retranqueos art déco y su aguja."""
    W, D = 40, 30
    deco = mat_ventanas('deco_empire', 0x3c4c62, 0xddd2bc, paso_x=1.4, paso_z=2.8, hueco_x=0.75, hueco_z=2.0, variacion=1.3)
    caja(deco, 0, D / 2, 0, W, D, 18)
    escaparate(0, 10, 4.0)
    caja(oro(), 0, -0.15, 4.6, 12, 0.2, 1.0)
    texto(mat('letras_empire', 0xf4cf55, 0.25), 'EMPIRE STATE', 0, -0.3, 5.1, tam=0.85, prof=0.1)
    for i, (w, d, z, h) in enumerate(((30, 24, 18, 40), (22, 18, 58, 26), (14, 12, 84, 10), (9, 8, 94, 8))):
        caja(deco, 0, D / 2 + 1, z, w, d, h)
        caja(liso(), 0, D / 2 + 1, z, w + 0.4, d + 0.4, 0.6)
    cil(liso(), 0, D / 2 + 1, 102, 2.6, 10, 8, r2=1.2)                       # el mástil
    cil(mat('aguja', 0xc8ccd2, 0.4), 0, D / 2 + 1, 112, 0.5, 14, 8, r2=0.05)

def madison():
    """Madison Square Park: césped, caminos, árboles y bancos."""
    W, D = 40, 30
    caja(cesped(), 0, D / 2 - 6, 0, W, D + 12, 0.08)
    caja(mat('camino_ny', 0xd5cdbc, 0.9), 0, D / 2 - 6, 0, 3, D + 12, 0.1)
    caja(mat('camino_ny', 0xd5cdbc, 0.9), 0, 6, 0, W, 3, 0.1)
    hojas = [mat('hoja_ny1', 0x5e9a46, 0.8), mat('hoja_ny2', 0x4f8a3c, 0.8)]
    random.seed(7)
    for k in range(14):
        x = random.uniform(-17, 17); y = random.uniform(-5, 22)
        if abs(x) < 3 or abs(y - 6) < 2:
            continue
        cil(mat('tronco_ny', 0x6b4a2f, 0.9), x, y, 0, 0.35, 5.0, 10, r2=0.25)
        for j in range(4):
            esfera(hojas[(k + j) % 2], x + (j - 1.5) * 1.0, y + (j % 2) * 0.8, 6.2 + (j % 3) * 0.8, 2.2 - j * 0.2, 2)
    for x in (-12, -6, 6, 12):
        caja(mat('banco_ny', 0x2d5a3a, 0.6), x, -4.5, 0, 2.4, 0.6, 0.9)

def flatiron():
    """El Flatiron, de proa hacia el jugador, y el camión de tacos delante."""
    D = 50
    piedra = mat_bloques('terracota_flat', 0xe2d3b8, 0xcbbb9c, ancho=1.2, alto=0.55, grosor=0.012, variacion=1.03)
    me = bpy.data.meshes.new('flat'); bm = bmesh.new()
    base = [(0, 0), (-16, D), (16, D)]
    H = 58
    a = [bm.verts.new((x, y, 0)) for x, y in base]
    b = [bm.verts.new((x, y, H)) for x, y in base]
    bm.faces.new(a[::-1]); bm.faces.new(b)
    for i in range(3):
        j = (i + 1) % 3
        bm.faces.new((a[i], a[j], b[j], b[i]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new('flat', me); bpy.context.scene.collection.objects.link(o)
    from comun import _poner
    _poner(o, piedra)
    cil(piedra, 0, 1.2, 0, 1.6, H, 16)                                      # la proa redondeada
    for k in range(16):                                                     # ventanas en las dos caras
        z = 6 + k * 3.2
        for s in (-1, 1):
            for j in range(1, 6):
                t = j / 6
                x, y = s * 16 * t * 0.9, D * t * 0.9
                caja(vidrio(), x - s * 0.05, y, z, 0.06, 1.2, 2.0, giro=s * math.atan2(16, D))
    caja(liso(), 0, 0.2, H, 4, 1.5, 1.2)
    # el camión de tacos, aparcado delante (donde se para el jugador)
    camion = mat('camion_tacos', 0xf2a530, 0.5)
    ty = -16
    caja(camion, 0, ty, 0.6, 3.2, 7, 3.2)
    caja(mat('cabina', 0xe8463c, 0.5), 0, ty - 4.5, 0.6, 3.2, 2.2, 2.4)
    caja(vidrio(), 0, ty - 5.62, 1.8, 2.6, 0.05, 1.0)
    caja(mat('ventanilla', 0xfff2c4, 0.3), 1.62, ty + 0.5, 1.8, 0.05, 4.0, 1.4)
    caja(mat('mostrador', 0xd8d2c4, 0.5), 1.9, ty + 0.5, 1.7, 0.6, 4.2, 0.12)
    texto(mat('letras_tacos', 0xe8463c, 0.4), 'TACOS', 0, ty - 3.52, 2.9, tam=0.7, prof=0.06)
    for dy in (-3.5, 2.5):
        for s in (-1, 1):
            cil(mat('rueda_ny', 0x1d1e21, 0.8), s * 1.55, ty + dy, 0.55, 0.55, 0.4, 14, eje='X')
    esfera(mat('taco_gigante', 0xf2c25a, 0.5), 0, ty + 0.5, 4.6, 0.9, 2, esc=(1.5, 0.6, 1))  # el taco del techo


PIEZAS = {
    'clasico':      (lambda: clasico('clasico', 0xe4d7bd), 'nueva_york', dict(lado=1024, segmentos=2)),
    'clasico_gris': (lambda: clasico('clasico_gris', 0xcfcabf), 'nueva_york', dict(lado=1024, segmentos=2)),
    'cristal_alto': (cristal_alto, 'nueva_york', dict(lado=1024, segmentos=2)),
    'ladrillo':     (ladrillo,     'nueva_york', dict(lado=1024, segmentos=2)),
    'tienda_lujo':  (lambda: tienda_lujo('lujo', 0xd8cfc0), 'nueva_york', dict(lado=1024, segmentos=2)),
    'tienda_rosa':  (lambda: tienda_lujo('rosa', 0xe3c9bd), 'nueva_york', dict(lado=1024, segmentos=2)),
    'torre_trump':  (torre_trump,  'nueva_york', dict(lado=1024, segmentos=2)),
    'st_regis':     (st_regis,     'nueva_york', dict(lado=1024, segmentos=2)),
    'peninsula':    (peninsula,    'nueva_york', dict(lado=1024, segmentos=2)),
    'santo_tomas':  (santo_tomas,  'nueva_york', dict(lado=1024, segmentos=2)),
    'catedral':     (catedral,     'nueva_york', dict(lado=2048, segmentos=2)),
    'rockefeller':  (rockefeller,  'nueva_york', dict(lado=1024, segmentos=2)),
    'saks':         (saks,         'nueva_york', dict(lado=1024, segmentos=2)),
    'biblioteca':   (biblioteca,   'nueva_york', dict(lado=1024, segmentos=2)),
    'empire':       (empire,       'nueva_york', dict(lado=1024, segmentos=2)),
    'madison':      (madison,      'nueva_york', dict(lado=1024, bisel=0.0)),
    'flatiron':     (flatiron,     'nueva_york', dict(lado=2048, segmentos=2)),
}

correr(PIEZAS)
