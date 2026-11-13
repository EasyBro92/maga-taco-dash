# Nivel 15: Fargo, Dakota del Norte (12/11/2026).
#
#   blender -b -P blender/fargo.py -- [pieza ...] [--rapido]
#
# Isidro (12/11): «sigue creando mapas y que se sientan muy diferentes, con
# dinámicas diferentes». Historia: «Pusiste aranceles a unas islas donde solo
# viven pingüinos. Ahora el Rey Pingüino viene a cobrártelo en plena nevada».
#   Por Broadway, en plena ventisca, hasta el teatro de Fargo:
#   izquierda:  el hotel Donaldson (ladrillo y su letrero en el tejado) · el
#               Black Building (art déco, ocho plantas)
#   derecha:    la estación del Northern Pacific (tejados rojos y el reloj) ·
#               la torre Radisson (con el arco hueco en lo alto)
#   al fondo:   el teatro de Fargo con su letrero vertical FARGO y la
#               marquesina «TRUMP · TONIGHT»
# Obstáculos (carpeta obstaculos): el pingüino que cruza deslizándose sobre
# la tripa, la moto de nieve que viene hacia ti, la pancarta de los
# pingüinos y la placa de hielo del suelo (encima se resbala).

import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import *
from comun import _poner

def blanco():  return mat('blanco_fgo', 0xfbfbf8, 0.5)
def negro():   return mat('negro_fgo', 0x1b1c20, 0.4)
def rojo():    return mat('rojo_fgo', 0xc8282c, 0.45)
def crema():   return mat('crema_fgo', 0xeadcbc, 0.6)
def nieve():   return mat('nieve_fgo', 0xf4f8fc, 0.75)
def acero():   return mat('acero_fgo', 0xc8cdd2, 0.25)
def naranja(): return mat('naranja_fgo', 0xf28c1c, 0.5)
def amarillo(): return mat('amarillo_fgo', 0xf2c230, 0.5)
def madera():  return mat('madera_fgo', 0x8a5a32, 0.75)
def hielo():   return mat('hielo_fgo', 0xcfe6f4, 0.06)
def ladrillo_r(): return mat_ventanas('ladrillo_fgo', 0x2c3440, 0x9a4a36, paso_x=1.8, paso_z=3.3, hueco_x=1.0, hueco_z=1.9, variacion=1.06)
def neumatico(): return mat('neumatico_fgo', 0x1e1e22, 0.85)

def nieve_encima(x, y, z, w, d):
    caja(nieve(), x, y, z, w + 0.3, d + 0.3, 0.35)

def letras_verticales(m, cadena, x, y, z_arriba, tam, paso):
    for i, ch in enumerate(cadena):
        if ch != ' ':
            texto(m, ch, x, y, z_arriba - i * paso, tam=tam, prof=0.08)

# ================================================================ edificios
def fargo_theatre():
    """El teatro de Fargo (1926, fachada de 1937): crema con franjas, el
    letrero vertical FARGO en rojo, la marquesina con bombillas y, hoy,
    «TRUMP · TONIGHT»."""
    Y = 8
    cuerpo = mat_ventanas('fachada_teatro', 0x7a5a3a, 0xeadcbc, paso_x=2.2, paso_z=3.4, hueco_x=0.5, hueco_z=2.4, variacion=1.03)
    caja(cuerpo, 0, Y, 0, 26, 16, 13)
    caja(mat('franja_teatro', 0xb8323a, 0.5), 0, Y - 8.05, 12.2, 26, 0.1, 0.5)
    for x in (-10, -5, 5, 10):
        caja(crema(), x, Y - 8.2, 5, 0.6, 0.4, 8)
    nieve_encima(0, Y, 13, 26, 16)
    # El letrero vertical.
    caja(mat('letrero_teatro', 0xf2ead6, 0.4), 0, -0.6, 9, 2.6, 1.4, 14)
    caja(rojo(), 0, -0.6, 9, 2.9, 1.2, 0.3)
    caja(rojo(), 0, -0.6, 22.8, 2.9, 1.2, 0.3)
    letras_verticales(luz('neon_fargo', 0xff3a2a, 1.4), 'FARGO', 0, -1.35, 20.2, 2.1, 2.45)
    # La marquesina con las letras y las bombillas.
    caja(mat('marquesina_teatro', 0x1f3a7a, 0.4), 0, -1.6, 5.4, 16, 3.2, 2.6)
    caja(blanco(), 0, -3.22, 5.8, 14.6, 0.05, 1.8)
    texto(negro(), 'TRUMP · TONIGHT', 0, -3.27, 6.35, tam=0.95, prof=0.04)
    bombilla = luz('bombillas_teatro', 0xffe7a0, 1.2)
    for k in range(17):
        esfera(bombilla, -7.6 + k * 0.95, -3.25, 7.85, 0.13, 1)
        esfera(bombilla, -7.6 + k * 0.95, -3.25, 5.55, 0.13, 1)
    nieve_encima(0, -1.6, 8.0, 16, 3.2)
    for x in (-3, 3):
        caja(mat('puerta_teatro', 0x5a2a1e, 0.5), x, -0.02, 0, 2.4, 0.1, 3.4)
    caja(mat('taquilla', 0xb8323a, 0.5), 0, -0.6, 0, 1.6, 1.2, 2.8)

def hotel_donaldson():
    """El hotel Donaldson («el HoDo»): cuatro plantas de ladrillo rojo con
    arcos abajo y su letrero blanco encima del tejado."""
    Y = 9
    caja(ladrillo_r(), 0, Y, 0, 24, 18, 15)
    caja(mat_bloques('piedra_hodo', 0xd8ccb2, 0xb0a48a, ancho=1.0, alto=0.5), 0, Y, 0, 24.2, 18.2, 4)
    for k in range(5):
        x = -9.6 + k * 4.8
        caja(mat('arco_hodo', 0x2c3440, 0.3), x, Y - 9.1, 0.6, 3, 0.1, 2.6)
        cil(mat('arco_hodo', 0x2c3440, 0.3), x, Y - 9.1, 3.2, 1.5, 0.1, 12, eje='Y')
    caja(mat('cornisa_hodo', 0x5a2a1e, 0.6), 0, Y, 15, 24.6, 18.6, 0.7)
    nieve_encima(0, Y, 15.7, 24.6, 18.6)
    for x in (-8, 8):
        cil(acero(), x, Y - 4, 16, 0.12, 4, 6)
    caja(acero(), 0, Y - 4, 18.5, 17, 0.2, 0.2)
    texto(luz('letras_hodo', 0xfff4dc, 1.0), 'HOTEL DONALDSON', 0, Y - 4.15, 17.3, tam=1.5, prof=0.1)
    caja(mat('toldo_hodo', 0x1f3a2a, 0.6), 0, -1, 3.6, 8, 2, 0.3)
    caja(mat('puerta_hodo', 0x3a2a1e, 0.5), 0, -0.05, 0, 2.4, 0.1, 3.2)

def black_building():
    """El Black Building (1931): ocho plantas art déco de ladrillo claro con
    pilares verticales y el remate escalonado."""
    Y = 10
    v = mat_ventanas('ventanas_black', 0x2c3440, 0xd8c8a8, paso_x=1.6, paso_z=3.2, hueco_x=1.0, hueco_z=2.0, variacion=1.04)
    caja(v, 0, Y, 0, 26, 20, 27)
    for k in range(9):
        caja(mat('pilar_black', 0xe6d8b8, 0.6), -12 + k * 3, Y - 10.1, 4, 0.7, 0.3, 24)
    for k, (w, h) in enumerate(((22, 1.6), (16, 1.6), (9, 2.2))):
        caja(mat('remate_black', 0xe6d8b8, 0.6), 0, Y, 27 + k * 1.6, w, 16 - k * 4, h)
    nieve_encima(0, Y, 31.8, 9, 8)
    texto(mat('letras_black', 0x3a2a1e, 0.5), 'BLACK BUILDING', 0, Y - 10.1, 4.6, tam=1.0, prof=0.06)
    caja(mat_bloques('piedra_black', 0xcfc2a8, 0xa89a80, ancho=1.2, alto=0.6), 0, Y, 0, 26.2, 20.2, 4)

def radisson_fargo():
    """La torre Radisson (1985), la más alta de Fargo: hormigón claro y, en lo
    alto, el arco hueco que se ve desde toda la llanura."""
    Y = 12
    v = mat_ventanas('ventanas_radisson', 0x3a4a5a, 0xd6d2c8, paso_x=1.8, paso_z=3.2, hueco_x=1.2, hueco_z=1.6, variacion=1.03)
    caja(v, 0, Y, 0, 22, 18, 58)
    caja(mat_bloques('base_radisson', 0xbab4a8, 0x9a948a, ancho=1.4, alto=0.7), 0, Y, 0, 30, 22, 6)
    nieve_encima(0, Y, 6, 30, 22)
    # El remate: dos pilares unidos por un arco, con el hueco en medio.
    h = mat('remate_radisson', 0xe2ded4, 0.6)
    for s in (-1, 1):
        caja(h, s * 8, Y, 58, 6, 18, 12)
    for k in range(13):
        a = math.pi * k / 12
        x, z = math.cos(a) * 6.5, 70 + math.sin(a) * 5
        o = caja(h, x, Y, z - 1.2, 2.4, 18, 2.4); o.rotation_euler = (0, -a + math.pi / 2, 0)
    caja(h, 0, Y, 75.5, 22, 18, 1.2)
    nieve_encima(0, Y, 76.7, 22, 18)
    texto(mat('letras_radisson', 0x1f3a7a, 0.5), 'RADISSON', 0, Y - 11.1, 4.2, tam=1.2, prof=0.06)

def np_depot():
    """La estación del Northern Pacific (1898): ladrillo, tejados de teja roja
    a cuatro aguas con nieve y la torre del reloj."""
    Y = 8
    caja(ladrillo_r(), 0, Y, 0, 40, 14, 7)
    teja = mat('teja_depot', 0xa83a2a, 0.7)
    for (x, w) in ((-11, 18), (11, 18)):
        tejado(teja, x, Y - 7, Y + 7, 7, w, 4.5, vuelo=0.8, cumbrera='x')
        caja(nieve(), x, Y - 3.6, 9.2, w * 0.8, 3, 0.3).rotation_euler = (0.55, 0, 0)
    # La torre del reloj.
    caja(ladrillo_r(), 0, Y - 2, 0, 6, 6, 16)
    caja(blanco(), 0, Y - 5.06, 12.5, 2.4, 0.1, 2.4)
    cil(mat('esfera_reloj', 0xf6f2e6, 0.5), 0, Y - 5.1, 13.7, 1.0, 0.05, 20, eje='Y')
    caja(negro(), 0, Y - 5.18, 13.4, 0.1, 0.05, 0.7)
    caja(negro(), 0.25, Y - 5.18, 13.7, 0.5, 0.05, 0.08)
    cil(teja, 0, Y - 2, 16, 4.6, 5, 4, r2=0.2).rotation_euler = (0, 0, math.pi / 4)
    texto(mat('letras_depot', 0xf2e6c8, 0.5), 'NORTHERN PACIFIC', 0, Y - 7.1, 5.2, tam=0.9, prof=0.05)
    for k in range(6):
        caja(mat('ventana_depot', 0x2c3440, 0.3), -15 + k * 6, Y - 7.05, 1.2, 2, 0.1, 3)

# ================================================================ obstáculos
def pinguino_tripa():
    """El pingüino que cruza la calle deslizándose sobre la tripa (mira a +x):
    tumbado, con las aletas abiertas y la corona de la corte del Rey."""
    plumas, tripa = mat('pingu_negro', 0x1f2328, 0.5), mat('pingu_blanco', 0xf6f6f2, 0.5)
    esfera(plumas, 0, 0, 0.42, 0.42, 3, esc=(1.7, 0.9, 0.85))
    esfera(tripa, 0.05, 0, 0.3, 0.38, 3, esc=(1.6, 0.8, 0.6))
    esfera(plumas, 0.78, 0, 0.6, 0.3, 3)
    esfera(tripa, 0.92, 0, 0.58, 0.18, 2, esc=(0.8, 1.1, 1))
    caja(naranja(), 1.13, 0, 0.6, 0.22, 0.12, 0.08)
    for s in (-1, 1):
        esfera(negro(), 0.98, s * 0.13, 0.7, 0.05, 1)
        o = caja(plumas, 0.1, s * 0.6, 0.38, 0.6, 0.45, 0.07); o.rotation_euler = (s * 0.3, 0, s * 0.4)
        caja(naranja(), -0.75, s * 0.12, 0.15, 0.24, 0.14, 0.06)
    cil(amarillo(), 0.72, 0, 0.88, 0.16, 0.12, 10, r2=0.19)

def moto_nieve():
    """La moto de nieve que viene hacia ti (mira a -y): esquís delante, la
    cadena atrás y el piloto con casco y orejeras."""
    carro = mat('moto_nieve_rojo', 0xc8282c, 0.35)
    for s in (-1, 1):
        caja(acero(), s * 0.42, -0.9, 0.0, 0.14, 1.0, 0.05)
        o = caja(acero(), s * 0.42, -1.42, 0.0, 0.14, 0.2, 0.2); o.rotation_euler = (0.7, 0, 0)
    esfera(carro, 0, -0.45, 0.55, 0.45, 2, esc=(1.0, 1.6, 0.6))
    caja(carro, 0, 0.35, 0.25, 0.8, 1.4, 0.45)
    caja(neumatico(), 0, 0.45, 0.0, 0.6, 1.3, 0.3)
    caja(negro(), 0, 0.4, 0.7, 0.55, 1.0, 0.15)
    caja(mat('parabrisas_nieve', 0x9ab8d0, 0.1), 0, -0.85, 0.85, 0.6, 0.06, 0.35).rotation_euler = (-0.5, 0, 0)
    # El piloto.
    abrigo = mat('abrigo_moto', 0x2a5a8a, 0.6)
    cil(abrigo, 0, 0.3, 0.85, 0.3, 0.7, 10, r2=0.26)
    esfera(mat('casco_moto', 0xf2c230, 0.3), 0, 0.25, 1.8, 0.24, 2)
    caja(negro(), 0, 0.03, 1.78, 0.32, 0.05, 0.12)
    for s in (-1, 1):
        rama(abrigo, (s * 0.25, 0.25, 1.4), (s * 0.35, -0.35, 1.0), 0.08, 0.07, 6)

def cartel_pinguino():
    """La pancarta de la corte del Rey Pingüino (agacharse): «NO TARIFFS ON
    PENGUINS» entre dos postes de hielo."""
    for x in (-1.25, 1.25):
        cil(hielo(), x, 0, 0, 0.12, 2.75, 8)
        esfera(nieve(), x, 0, 2.75, 0.18, 1)
    caja(mat('tela_pingu', 0x1f3a7a, 0.6), 0, 0, 1.55, 2.4, 0.06, 1.05)
    texto(blanco(), 'NO TARIFFS', 0, -0.04, 2.25, tam=0.28, prof=0.02)
    texto(blanco(), 'ON PENGUINS', 0, -0.04, 1.88, tam=0.28, prof=0.02)
    esfera(mat('pingu_negro', 0x1f2328, 0.5), 0, -0.04, 1.65, 0.12, 2, esc=(1, 0.3, 1.2))

def placa_hielo():
    """La placa de hielo del suelo (se pisa: encima se resbala)."""
    caja(hielo(), 0, 0, 0.0, 2.2, 7.0, 0.04)   # 13/11: sin rendijas entre filas (parpadeaban)
    claro = mat('hielo_claro_fgo', 0xf2f8fc, 0.1)
    for k in range(7):
        o = caja(claro, -0.6 + (k % 3) * 0.6, 2.4 - k * 0.8, 0.045, 0.8, 0.05, 0.01); o.rotation_euler = (0, 0, 0.4 + k * 0.3)

PIEZAS = {
    'fargo_theatre':   (fargo_theatre,   'fargo', dict(lado=1024, bisel=0.0)),
    'hotel_donaldson': (hotel_donaldson, 'fargo', dict(lado=1024, segmentos=1, min_bisel=1.0)),
    'black_building':  (black_building,  'fargo', dict(lado=1024, bisel=0.0)),
    'radisson_fargo':  (radisson_fargo,  'fargo', dict(lado=1024, bisel=0.0)),
    'np_depot':        (np_depot,        'fargo', dict(lado=1024, segmentos=1, min_bisel=1.0)),
    'pinguino_tripa':  (pinguino_tripa,  'obstaculos', dict(lado=256, bisel=0.0)),
    'moto_nieve':      (moto_nieve,      'obstaculos', dict(lado=256, bisel=0.0)),
    'cartel_pinguino': (cartel_pinguino, 'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
    'placa_hielo':     (placa_hielo,     'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
}

correr(PIEZAS)
