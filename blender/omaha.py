# Nivel 6: Omaha, Nebraska (08/11/2026).
#
#   blender -b -P blender/omaha.py -- [pieza ...] [--rapido]
#
# Isidro: «haz más mapas, todos los que puedas, con sus escenarios, obstáculos
# y su dinamismo». Para Omaha eligió el final en la antigua estación art déco
# (Union Station, hoy el museo Durham) y la luz de atardecer en la pradera.
# Historia: «Tierra de vacas. Por la calle, cajas de tus Filetes Trump, los
# que nadie compró».
#   izquierda:  la torre del First National (la más alta de Nebraska) · los
#               almacenes de ladrillo del Old Market con su marquesina
#   derecha:    la torre Woodmen · el teatro Orpheum con su letrero vertical
#   en medio:   los corrales de ganado (el momento estrella), con el arco de
#               la entrada «UNION STOCK YARDS»
#   al fondo:   Union Station, art déco, con su reloj
# Las fachadas en y = 0 mirando a -y. Lo que cruza la calle: origen en el
# centro de la calle y en el centro de su largo.
# Obstáculos (carpeta obstaculos): cajas de Filetes Trump (se saltan), el rollo
# de heno que viene rodando, el cartel del asador (agacharse), el camión de
# ganado (cambia de carril) y el aficionado de los Cornhuskers (cruza).

import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import *

def blanco():   return mat('blanco_om', 0xfbf8f2, 0.5)
def oscuro():   return mat('hueco_om', 0x2b2c33, 0.8)
def vidrio():   return mat('vidrio_om', 0x6a86a8, 0.15)
def vidrio_osc(): return mat('vidrio_osc_om', 0x2e3a48, 0.12)
def ladrillo(): return mat_bloques('ladrillo_om', 0x9e4e36, 0x7e3c2a, ancho=0.45, alto=0.2, grosor=0.02, variacion=1.08)
def ladrillo2(): return mat_bloques('ladrillo2_om', 0xb8724a, 0x965a38, ancho=0.45, alto=0.2, grosor=0.02, variacion=1.08)
def terracota(): return mat_bloques('terracota_om', 0xe8d2a8, 0xd2ba90, ancho=1.2, alto=0.5, grosor=0.012, variacion=1.03)
def granito():  return mat_bloques('granito_om', 0xb8b0a4, 0x9a9286, ancho=1.2, alto=0.6, grosor=0.02, variacion=1.04)
def oro():      return mat('oro_om', 0xe0b040, 0.25)
def hierro():   return mat('hierro_om', 0x2c2e33, 0.4)
def rojo():     return mat('rojo_om', 0xc8302a, 0.45)
def madera():   return mat('madera_om', 0x8a5a36, 0.7)
def madera_c(): return mat('madera_clara_om', 0xb98a5a, 0.7)
def bombilla(): return luz('bombilla_om', 0xffe2a0, 1.4)

def ventanas_fila(xs, z, w, h, marco=None, cristal=None):
    for x in xs:
        ventana(x, z, w, h, y=-0.1, marco=marco, cristal=cristal or vidrio())

def vaca_figura(x, y, giro=0.0, color=0x5a3a24):
    """Una vaca sencilla (para los corrales): cuerpo, cabeza, patas y manchas."""
    piel = mat('piel_%x' % color, color, 0.7)
    o = caja(piel, x, y, 0.75, 0.75, 1.7, 0.7, giro=giro)
    caja(blanco(), x + 0.05, y + 0.2, 1.1, 0.5, 0.5, 0.36, giro=giro)
    dx, dy = math.sin(-giro) * 1.0, math.cos(-giro) * 1.0
    caja(piel, x + dx, y - dy, 1.05, 0.42, 0.55, 0.42, giro=giro)
    caja(mat('hocico', 0xe8b4a0, 0.6), x + dx * 1.3, y - dy * 1.3, 1.05, 0.34, 0.18, 0.24, giro=giro)
    for sx in (-0.25, 0.25):
        for sy in (-0.6, 0.6):
            cil(piel, x + sx * math.cos(giro) - sy * math.sin(giro), y + sx * math.sin(giro) + sy * math.cos(giro), 0, 0.09, 0.78, 6)

# ================================================================ los edificios
def first_national():
    """La torre del First National Bank (la más alta de Nebraska): granito
    claro con bandas verticales de cristal oscuro y la coronación inclinada."""
    W, D, H = 30, 22, 66
    caja(granito(), 0, D / 2, 0, W, D, H)
    for x in (-10.5, -5.25, 0, 5.25, 10.5):
        caja(vidrio_osc(), x, -0.08, 6, 3.2, 0.2, H - 10)
    caja(vidrio(), 0, -0.1, 0.3, 12, 0.2, 5.0)
    caja(hierro(), 0, -1.6, 5.4, 14, 3.2, 0.35)
    texto(oro(), 'FIRST NATIONAL', 0, -3.25, 5.55, tam=0.6, prof=0.05)
    # La coronación: dos planos inclinados.
    o = caja(vidrio_osc(), 0, D / 2, H, W - 1, D * 0.7, 8, inclina=-0.35)
    caja(granito(), 0, D - 1, H, W, 2, 10)

def woodmen():
    """La torre Woodmen: cristal bronce con bandas blancas horizontales y el
    letrero en lo alto."""
    W, D, H = 30, 22, 52
    caja(mat('bronce_om', 0x6a5440, 0.2), 0, D / 2, 0, W, D, H)
    for p in range(1, 16):
        caja(blanco(), 0, -0.06, p * 3.3, W + 0.1, 0.14, 0.5)
    caja(blanco(), 0, D / 2, H, W + 0.4, D + 0.4, 1.2)
    texto(mat('letras_woodmen', 0x1f3a6a, 0.4), 'WOODMEN', 0, -0.2, H - 3, tam=2.2, prof=0.1)
    caja(vidrio(), 0, -0.1, 0.3, 10, 0.2, 4.4)

def old_market():
    """Los almacenes de ladrillo del Old Market: cuatro plantas, la marquesina
    de hierro sobre la acera con bombillas, toldos y el letrero."""
    W, D = 40, 20
    for k, (x, h, m) in enumerate(((-13, 15, ladrillo()), (0, 13, ladrillo2()), (13, 16, ladrillo()))):
        caja(m, x, D / 2, 0, 13.4, D, h)
        caja(mat('cornisa_om', 0xe6dcc6, 0.5), x, -0.15, h - 0.8, 13.6, 0.5, 0.8)
        for p in range(1, 4):
            ventanas_fila([x - 4.2, x - 1.4, x + 1.4, x + 4.2], 1.0 + p * 3.6, 1.6, 2.4, marco=mat('marco_om', 0xe8e0cc, 0.5))
        caja(oscuro(), x, -0.04, 0.3, 10, 0.06, 3.0)
        caja(mat('escaparate_om', 0xffe2a8, 0.5), x, -0.05, 0.6, 9, 0.04, 2.2)
    # La marquesina de hierro sobre la acera y su letrero.
    caja(hierro(), 0, -2.0, 3.6, W - 1, 4.0, 0.3)
    for x in range(-18, 19, 6):
        cil(hierro(), x, -3.8, 0, 0.1, 3.6, 8)
        esfera(bombilla(), x, -3.8, 3.45, 0.12, 1)
    caja(mat('letrero_om', 0x2c4a3a, 0.5), 0, -4.05, 3.95, 9.0, 0.12, 1.0)
    texto(oro(), 'OLD MARKET', 0, -4.12, 4.45, tam=0.65, prof=0.04)

def orpheum():
    """El teatro Orpheum: fachada de terracota con arcos, la marquesina de
    bombillas y el gran letrero vertical «ORPHEUM»."""
    W, D, H = 30, 26, 22
    caja(terracota(), 0, D / 2, 0, W, D, H)
    for x in (-9, 0, 9):
        caja(oscuro(), x, -0.04, 7.0, 5.0, 0.06, 9.0)
        cil(oscuro(), x, -0.04, 16.0, 2.5, 0.06, 18, eje='Y')
        caja(vidrio(), x, -0.06, 7.2, 4.4, 0.04, 8.4)
    caja(mat('cornisa_orph', 0xd4b880, 0.5), 0, -0.3, H - 1, W + 0.6, 0.8, 1.0)
    # La marquesina.
    caja(mat('marquesina_orph', 0xb02a2a, 0.5), 0, -2.0, 4.2, 18, 4.0, 1.4)
    for k in range(36):
        esfera(bombilla(), -8.8 + k * 0.5, -4.02, 4.35, 0.08, 1)
        esfera(bombilla(), -8.8 + k * 0.5, -4.02, 5.45, 0.08, 1)
    texto(mat('letra_marq', 0xfff2d0, 0.4), 'TONIGHT: TRUMP', 0, -4.05, 4.9, tam=0.55, prof=0.03)
    # El letrero vertical.
    caja(mat('letrero_orph', 0xc8302a, 0.45), 0, -1.6, 7.0, 1.4, 1.0, 13.0)
    for k, letra in enumerate('ORPHEUM'):
        o = texto(mat('letra_orph', 0xfff2d0, 0.4), letra, 0, 0, 0, tam=1.3, prof=0.06)
        o.rotation_euler = (math.pi / 2, 0, 0)
        o.location = (0, -2.13, 19.0 - k * 1.7)
        esfera(bombilla(), -0.55, -2.12, 19.0 - k * 1.7, 0.07, 1)
        esfera(bombilla(), 0.55, -2.12, 19.0 - k * 1.7, 0.07, 1)

# ================================================================ la meta
def union_station():
    """Union Station (1931), hoy el museo Durham: art déco de terracota
    clara, los pilares verticales, los tres ventanales enormes, el reloj
    encima de la entrada y las alas a los lados. Delante, la plaza con dos
    mástiles; el jugador se para al pie de la escalinata."""
    piedra = terracota()
    liso = mat('liso_us', 0xefe2c4, 0.5)
    # Las alas y el cuerpo central (más alto).
    for s in (-1, 1):
        caja(piedra, s * 30, 18, 0, 22, 30, 13)
        for x in (20.5, 25.5, 30.5, 35.5, 40.0):
            caja(liso, s * x, 2.9, 0, 1.2, 0.6, 13.6)
            caja(vidrio(), s * (x + 2.4), 2.95, 2.0, 3.4, 0.1, 9.0)
    caja(piedra, 0, 18, 0, 38, 30, 19)
    for x in (-17.5, -11.5, -5.8, 5.8, 11.5, 17.5):
        caja(liso, x, 2.85, 0, 1.6, 0.8, 20.5)
    # Los tres ventanales art déco.
    for x in (-8.6, 0, 8.6):
        caja(vidrio(), x, 2.9, 3.0, 4.4, 0.12, 13.5)
        for z in (6.0, 9.0, 12.0, 15.0):
            caja(hierro(), x, 2.82, z, 4.5, 0.06, 0.12)
        caja(hierro(), x, 2.82, 3.0, 0.12, 0.06, 13.5)
    # El reloj y el nombre.
    cil(liso, 0, 2.7, 17.4, 1.6, 0.2, 32, eje='Y')
    cil(mat('esfera_reloj', 0xfaf4e0, 0.4), 0, 2.58, 17.4, 1.35, 0.05, 32, eje='Y')
    for k in range(12):
        a = k * math.pi / 6
        caja(hierro(), math.sin(a) * 1.1, 2.53, 17.4 + math.cos(a) * 1.1 - 0.06, 0.08, 0.02, 0.12)
    caja(hierro(), 0.25, 2.52, 17.4, 0.6, 0.02, 0.07, inclina=0.0, giro=0.0)
    caja(hierro(), 0, 2.52, 17.4, 0.06, 0.02, 0.9)
    texto(oro(), 'UNION STATION', 0, 2.6, 19.6, tam=1.4, prof=0.12)
    caja(liso, 0, 18, 19, 39, 31, 0.8)
    # La entrada y la escalinata.
    caja(oscuro(), 0, 2.88, 0.6, 6.0, 0.1, 2.6)
    escalinata(liso, 0, 2.6, 0, 16, 4, huella=0.5, tabica=0.15)
    caja(mat('plaza_us', 0xd8ccb4, 0.8), 0, -12, 0, 90, 24, 0.05)
    for s in (-1, 1):
        cil(blanco(), s * 12, -6, 0, 0.12, 14, 8)
        caja(mat_franjas('bandera_us', 0xc8302a, 0xfbf8f2, 7, eje='Z', z0=12.4, alto=1.6), s * 12 + 1.4, -6, 12.4, 2.6, 0.04, 1.6)
        caja(mat('azul_us', 0x23408f, 0.45), s * 12 + 0.6, -6.03, 13.2, 1.0, 0.04, 0.8)

# ================================================================ los corrales
def corrales_entrada():
    """El arco de madera de la entrada a los corrales: «UNION STOCK YARDS» y
    una cabeza de toro encima."""
    for s in (-1, 1):
        caja(madera(), s * 9.8, 0, 0, 0.8, 0.8, 11.0)
        caja(madera(), s * 9.8, 0, 11.0, 1.2, 1.2, 0.4)
    caja(madera(), 0, 0, 9.6, 20.4, 0.7, 1.6)
    texto(mat('letras_corral', 0xfff2d0, 0.5), 'UNION STOCK YARDS', 0, -0.37, 10.4, tam=0.95, prof=0.05)
    esfera(mat('toro_arco', 0x3a2418, 0.6), 0, 0, 11.9, 0.7, 2, esc=(1.2, 0.8, 0.9))
    for s in (-1, 1):
        rama(mat('cuerno', 0xf2ead8, 0.5), (s * 0.6, 0, 12.1), (s * 1.6, 0, 12.6), 0.12, 0.04, 6)

def corrales():
    """30 m de los corrales de ganado: vallas de madera a los dos lados con
    vacas dentro, un granero rojo a la izquierda, pacas y un abrevadero."""
    L = 30.0
    for s in (-1, 1):
        for x in (4.6, 11.0):
            for k in range(11):
                caja(madera_c(), s * x, -L / 2 + k * 3, 0, 0.2, 0.2, 1.6)
            for z in (0.5, 1.0, 1.45):
                caja(madera_c(), s * x, 0, z, 0.08, L, 0.14)
        for k in range(10):
            caja(madera_c(), s * (4.6 + (11.0 - 4.6) / 2), -L / 2 + k * 3.3, 1.0, 6.4, 0.08, 0.14)
        tierra = mat('tierra_corral', 0x8a6a48, 0.95)
        caja(tierra, s * 7.8, 0, 0, 6.4, L, 0.04)
        vaca_figura(s * 6.6, -9.0, giro=0.3 * s, color=0x5a3a24)
        vaca_figura(s * 9.0, -1.5, giro=-0.5 * s, color=0x2a2420)
        vaca_figura(s * 7.2, 8.0, giro=0.9 * s, color=0x8a5a3a)
        caja(mat('abrevadero', 0x6a6e74, 0.4), s * 8.8, 4.0, 0, 0.9, 3.0, 0.7)
        caja(mat('agua_abrevadero', 0x5a8aa8, 0.2), s * 8.8, 4.0, 0.62, 0.7, 2.8, 0.05)
    # El granero rojo y las pacas.
    caja(mat('granero', 0xa8302a, 0.6), -18.0, 2.0, 0, 9.0, 12.0, 7.0)
    fronton(mat('granero', 0xa8302a, 0.6), -18.0, -4.0, 7.0, 9.0, 3.8, 12.0)
    caja(blanco(), -18.0, -4.05, 1.0, 3.6, 0.1, 4.4)
    caja(mat('puerta_granero', 0x7a2420, 0.6), -18.0, -4.1, 1.1, 3.2, 0.08, 4.2)
    paja = mat('paja_om', 0xd9b45a, 0.9)
    for k in range(4):
        cil(paja, 14.0 + (k % 2) * 1.6, -6.0 + k * 1.2, 0.75, 0.75, 1.2, 16, eje='X')

# ================================================================ los obstáculos
def caja_filetes():
    """Cajas de «Filetes Trump» apiladas (los que nadie compró): se saltan."""
    carton = mat('carton_filetes', 0xd6b88a, 0.8)
    for (x, z, g) in ((-0.42, 0, 0.05), (0.42, 0, -0.08), (0.0, 0.42, 0.12)):
        caja(carton, x, 0.4, z, 0.8, 0.6, 0.42, giro=g)
        caja(mat('banda_filetes', 0x1f2a4a, 0.5), x, 0.4, z + 0.12, 0.82, 0.62, 0.12, giro=g)
    texto(oro(), 'TRUMP STEAKS', 0, 0.08, 0.6, tam=0.12, prof=0.008)

def rodillo_heno():
    """Un rollo de heno redondo que viene rodando hacia ti. Va centrado en el
    origen (rueda sobre el eje x)."""
    paja = mat('paja_rollo', 0xd9b45a, 0.9)
    cil(paja, 0, 0, 0, 0.6, 1.4, 20, eje='X')
    for x in (-0.71, 0.71):
        cil(mat('cara_rollo', 0xc49a44, 0.9), x, 0, 0, 0.58, 0.02, 20, eje='X')
        cil(mat('espiral_rollo', 0xa8823a, 0.9), x * 1.01, 0, 0, 0.3, 0.02, 16, eje='X')
    caja(mat('cuerda', 0xe8e0c8, 0.6), 0, 0, -0.62, 0.06, 0.05, 1.24)

def cartel_steak():
    """El cartel colgado del asador («STEAKS» con una vaca): se pasa agachado."""
    caja(hierro(), 0, 0, 2.4, 2.0, 0.08, 0.08)
    for x in (-0.9, 0.9):
        caja(hierro(), x, 0, 2.4, 0.06, 0.06, 1.4)
    caja(mat('tabla_steak', 0x5a3a24, 0.6), 0, 0, 1.25, 1.9, 0.12, 0.85)
    texto(mat('letra_steak', 0xf2c230, 0.4), 'STEAKS', 0, -0.07, 1.68, tam=0.32, prof=0.02)
    texto(blanco(), 'OMAHA', 0, -0.07, 1.4, tam=0.18, prof=0.015)

def camion_ganado():
    """El camión de ganado (visto por detrás): la caja de aluminio con
    rendijas y las vacas asomando. Cambia de carril con el intermitente."""
    W, L = 1.9, 5.6
    alu = mat('aluminio_ganado', 0xc4c9cf, 0.3)
    caja(alu, 0, L / 2 + 0.6, 0.6, W, L - 1.0, 2.2)
    for z in (1.2, 1.6, 2.0, 2.4):
        caja(oscuro(), 0, 0.59, z, W - 0.3, 0.02, 0.12)
        for s in (-1, 1):
            caja(oscuro(), s * (W / 2 + 0.01), L / 2 + 0.6, z, 0.02, L - 1.4, 0.12)
    caja(mat('cabina_ganado', 0xc8302a, 0.45), 0, L - 0.2, 0.5, W, 1.4, 1.8)
    for s in (-1, 1):
        caja(mat('piloto', 0xc0262c, 0.3), s * 0.75, 0.58, 0.75, 0.2, 0.04, 0.14)
        caja(mat('intermitente', 0xffa21a, 0.3), s * 0.75, 0.58, 0.95, 0.2, 0.04, 0.1)
        for y in (1.2, 4.6):
            cil(mat('neumatico', 0x1d1e21, 0.8), s * (W / 2 - 0.1), y, 0.42, 0.42, 0.3, 14, eje='X')
    esfera(mat('vaca_asoma', 0x2a2420, 0.7), 0.4, 0.55, 2.1, 0.22, 1)
    texto(rojo(), 'NEBRASKA BEEF', 0, 0.56, 2.6, tam=0.16, prof=0.01)

def fan_huskers():
    """Un aficionado de los Cornhuskers de Nebraska: todo de rojo, con el
    gorro de mazorca de maíz. Cruza la calle (mira a +x)."""
    rojo_n = mat('rojo_huskers', 0xd01c2c, 0.5)
    piel = mat('piel_fan', 0xe8b48c, 0.6)
    for sy in (-0.12, 0.12):
        cil(mat('vaquero_pant', 0x3a4a6a, 0.6), 0, sy, 0, 0.1, 0.85, 8)
    caja(rojo_n, 0, 0, 0.85, 0.42, 0.52, 0.65)
    texto(blanco(), 'N', 0.22, 0, 1.15, tam=0.3, prof=0.02).rotation_euler = (math.pi / 2, 0, math.pi / 2)
    esfera(piel, 0, 0, 1.68, 0.2, 2)
    # El gorro de mazorca.
    cil(mat('mazorca_gorro', 0xf2c230, 0.6), 0, 0, 1.78, 0.17, 0.62, 12, r2=0.06)
    for s in (-1, 1):
        rama(mat('hoja_gorro', 0x6a9a3a, 0.6), (0, s * 0.15, 1.8), (-0.1, s * 0.32, 1.6), 0.05, 0.02, 5)
    # Los brazos en alto, con un banderín.
    for sy in (-0.3, 0.3):
        rama(rojo_n, (0, sy * 0.8, 1.4), (0.1, sy, 1.95), 0.07, 0.06, 6)
    caja(rojo_n, 0.12, 0.32, 1.95, 0.02, 0.5, 0.3)

PIEZAS = {
    'first_national':    (first_national,    'omaha', dict(lado=1024, segmentos=2)),
    'woodmen':           (woodmen,           'omaha', dict(lado=1024, segmentos=2)),
    'old_market':        (old_market,        'omaha', dict(lado=1024, segmentos=2, min_bisel=1.0)),
    'orpheum':           (orpheum,           'omaha', dict(lado=1024, segmentos=2, min_bisel=1.0)),
    'union_station':     (union_station,     'omaha', dict(lado=2048, segmentos=1, min_bisel=2.0)),
    'corrales_entrada':  (corrales_entrada,  'omaha', dict(lado=512, bisel=0.0)),
    'corrales':          (corrales,          'omaha', dict(lado=1024, bisel=0.0)),
    'caja_filetes':      (caja_filetes,      'obstaculos', dict(lado=256, bisel=0.0)),
    'rodillo_heno':      (rodillo_heno,      'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
    'cartel_steak':      (cartel_steak,      'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
    'camion_ganado':     (camion_ganado,     'obstaculos', dict(lado=512)),
    'fan_huskers':       (fan_huskers,       'obstaculos', dict(lado=256, bisel=0.0)),
}

correr(PIEZAS)
