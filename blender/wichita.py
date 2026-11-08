# Nivel 7: Wichita, Kansas (08/11/2026).
#
#   blender -b -P blender/wichita.py -- [pieza ...] [--rapido]
#
# Isidro eligió el final en el Guardián de las Llanuras (la estatua de acero
# junto a la unión de los dos ríos, con los braseros de fuego) y la luz de
# cielo de tornado (verde gris, sin relámpagos que parpadeen). Historia: «Un
# tornado como el de El Mago de Oz se lleva las vallas».
#   izquierda:  el Epic Center (la torre escalonada, la más alta de Kansas) ·
#               el museo de la aviación (Wichita, «capital mundial del aire»)
#               con una avioneta encima
#   derecha:    Century II, redondo, con el tejado azul de gajos
#   en medio:   el tornado pasando junto a la calle (el momento estrella) y el
#               camino de baldosas amarillas
#   al fondo:   el Guardián de las Llanuras en su roca, con el anillo de fuego
# Obstáculos (carpeta obstaculos): la valla que se lleva el viento (cruza a la
# altura de la cabeza: agacharse), el trozo de tejado que viene botando, el
# espantapájaros, la señorita Gulch en bicicleta (cambia de carril) y la vaca
# que se lleva el tornado (cruza por el aire: agacharse). El camino de baldosas
# amarillas lo pinta el juego (como la alfombra roja: si no, el asfalto se
# transparentaba).

import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import *

def blanco():   return mat('blanco_wi', 0xfbf8f2, 0.5)
def oscuro():   return mat('hueco_wi', 0x2b2c33, 0.8)
def vidrio():   return mat('vidrio_wi', 0x6a8aa0, 0.15)
def acero():    return mat('acero_wi', 0x6a5a4a, 0.35)
def hierro():   return mat('hierro_wi', 0x2c2e33, 0.4)
def rojo():     return mat('rojo_wi', 0xc8302a, 0.45)
def madera():   return mat('madera_wi', 0x8a6a48, 0.8)
def caliza():   return mat_bloques('caliza_wi', 0xe2d8c2, 0xcabda0, ancho=1.4, alto=0.55, grosor=0.02, variacion=1.04)
def fuego():    return luz('fuego_wi', 0xff8a2a, 2.2)

# ================================================================ los edificios
def epic_center():
    """El Epic Center: la torre escalonada de cristal verdoso y piedra clara,
    la más alta de Kansas, con la aguja arriba."""
    W, D = 30, 24
    vid = mat('vidrio_epic', 0x5a8a8a, 0.15)
    escalones = [(30, 24, 24), (24, 19, 14), (18, 14, 12), (12, 9, 10)]
    z = 0
    for (w, d, h) in escalones:
        caja(caliza(), 0, d / 2, z, w, d, h)
        for x in range(int(-w / 2) + 2, int(w / 2) - 1, 3):
            caja(vid, x, -0.06 + (D - d) / 2 * 0, z + 1.0, 1.8, 0.12, h - 2.0)
        caja(caliza(), 0, d / 2, z + h, w + 0.4, d + 0.4, 0.4)
        z += h
    cil(hierro(), 0, 5, z, 0.3, 8, 8, r2=0.05)
    caja(vidrio(), 0, -0.1, 0.3, 12, 0.2, 4.4)
    texto(mat('letras_epic', 0x2a5a5a, 0.4), 'EPIC CENTER', 0, -0.25, 5.4, tam=0.7, prof=0.05)

def century_ii():
    """Century II: el gran edificio redondo con el tejado azul de gajos."""
    R = 18.0
    blanco_c = mat('muro_century', 0xf0ece2, 0.5)
    cil(blanco_c, 0, R, 0, R, 9, 40)
    for k in range(40):
        a = k * 2 * math.pi / 40
        caja(vidrio(), math.sin(a) * R, R - math.cos(a) * R, 1.0, 2.0, 0.15, 5.5, giro=-a)
    # El tejado de gajos azules.
    azul_t = mat('tejado_century', 0x2a6ab8, 0.4)
    cupula(azul_t, 0, R, 9, R + 0.6, 6.0, lados=20, aros=6)
    for k in range(20):
        a = k * 2 * math.pi / 20
        rama(blanco(), (math.sin(a) * (R + 0.6), R - math.cos(a) * (R + 0.6), 9.0), (0, R, 15.0), 0.12, 0.08, 5)
    caja(mat('marquesina_century', 0x1f3a6a, 0.5), 0, -1.0, 4.0, 14, 2.4, 0.5)
    texto(blanco(), 'CENTURY II', 0, -2.25, 4.25, tam=0.75, prof=0.05)

def museo_aviacion():
    """El museo de la aviación: un hangar de chapa con el letrero «AIR
    CAPITAL OF THE WORLD» y una avioneta antigua subida en un poste."""
    W, D, H = 30, 24, 9
    chapa = mat_franjas('chapa_hangar', 0xc4c9cf, 0xaeb4bb, 30, eje='X', z0=-15, alto=30)
    caja(chapa, 0, D / 2, 0, W, D, H)
    cil(chapa, 0, D / 2, H, W / 2, D - 0.4, 24, eje='Y').scale = (1, 1, 0.35)
    caja(mat('portalon', 0x5a6a7a, 0.5), 0, -0.05, 0, 16, 0.1, 7.5)
    caja(mat('letrero_aire', 0x1f3a6a, 0.5), 0, -0.2, 8.0, 24, 0.2, 1.6)
    texto(mat('letras_aire', 0xf2c230, 0.4), 'AIR CAPITAL OF THE WORLD', 0, -0.35, 8.8, tam=0.9, prof=0.05)
    # La avioneta en su poste, inclinada como si despegara.
    cil(hierro(), 9, -4, 0, 0.25, 9, 10)
    av = mat('avioneta_museo', 0xd8302a, 0.4)
    cil(av, 9, -4, 9.6, 0.55, 4.2, 14, eje='Y').rotation_euler = (math.pi / 2 + 0.25, 0, 0)
    caja(blanco(), 9, -4.4, 9.6, 8.0, 1.2, 0.18)
    caja(blanco(), 9, -6.0, 9.7, 2.6, 0.7, 0.12)
    caja(av, 9, -6.1, 9.7, 0.12, 0.7, 1.0)
    cil(hierro(), 9, -2.0, 9.95, 0.12, 0.3, 8, eje='Y')

# ================================================================ la meta
def guardian_llanuras():
    """El Guardián de las Llanuras (Keeper of the Plains): la estatua de
    acero de 13 m con los brazos alzados, en lo alto de su roca, en la unión
    de los dos ríos; alrededor, el anillo de braseros con fuego. Delante, la
    plaza y la pasarela. El jugador se para delante de la roca."""
    roca = mat_bloques('roca_guardian', 0x9a8a72, 0x857560, ancho=1.8, alto=0.9, grosor=0.03, variacion=1.06)
    agua = mat('rio_wichita', 0x4a6a6a, 0.15)
    caja(agua, 0, 30, -0.4, 120, 50, 0.3)
    caja(mat('plaza_guardian', 0xd2c6ae, 0.8), 0, 0, 0, 70, 14, 0.06)
    # La roca y la escalera.
    cil(roca, 0, 22, 0, 9.0, 6.0, 24)
    escalinata(caliza(), 0, 12.5, 0, 6, 10, huella=0.5, tabica=0.25)
    # Los braseros de fuego alrededor de la roca.
    for k in range(10):
        a = math.pi + (k - 4.5) * 0.32
        x, y = math.sin(a) * 12.5, 22 - math.cos(a) * 12.5
        cil(roca, x, y, 0, 0.9, 1.6, 12)
        cil(mat('cuenco_fuego', 0x3a2a20, 0.6), x, y, 1.6, 0.8, 0.3, 12, r2=0.5)
        cil(fuego(), x, y, 1.85, 0.55, 1.1, 10, r2=0.05)
    # La estatua: el cuerpo, la cabeza con las plumas y los brazos en alto.
    ac = acero()
    cil(ac, 0, 22, 6.0, 1.0, 6.5, 12, r2=0.7)
    cil(ac, 0, 22, 12.5, 0.7, 2.5, 12, r2=0.55)
    esfera(ac, 0, 22, 15.6, 0.7, 2)
    for k in range(7):
        a = (k - 3) * 0.32
        rama(ac, (0, 22.3, 16.0), (math.sin(a) * 1.6, 22.6, 16.0 + math.cos(a) * 2.4), 0.12, 0.04, 5)
    for s in (-1, 1):
        rama(ac, (s * 0.7, 22, 14.4), (s * 2.6, 22, 17.6), 0.28, 0.2, 8)
        rama(ac, (s * 2.6, 22, 17.6), (s * 2.9, 22, 20.2), 0.2, 0.14, 8)
    # Las pasarelas a los lados (en curva, bajas).
    for s in (-1, 1):
        caja(mat('pasarela_guardian', 0xe8e0d0, 0.6), s * 22, 18, 0.5, 18, 3, 0.3, giro=s * 0.35)

# ================================================================ el tornado
def tornado_embudo():
    """El embudo del tornado que pasa junto a la calle (a la derecha, lejos):
    gris verdoso, ancho arriba y estrecho abajo, con la nube encima y los
    escombros girando alrededor. El juego lo hace girar despacio."""
    gris = mat('embudo', 0x6a7266, 0.9)
    claro = mat('embudo_claro', 0x8a9282, 0.9)
    X = 0.0
    for k in range(12):
        z = k * 3.0
        r = 1.2 + (k / 11) ** 1.6 * 9.0
        cil(gris if k % 2 else claro, X, 0, z, r, 3.2, 16, r2=r * 1.05)
    esfera(mat('nube_tornado', 0x4a5248, 0.9), X, 0, 40, 26, 2, esc=(1, 1, 0.25))
    # Escombros (tablas y tejas) alrededor.
    for k in range(10):
        a = k * 0.9
        z = 4 + k * 3
        r = 3 + k * 0.8
        caja(mat('escombro', 0x7a5a3a, 0.8), math.sin(a) * r, math.cos(a) * r, z, 1.4, 0.3, 0.1, giro=a)

def baldosas():
    """30 m del camino de baldosas amarillas (de El Mago de Oz) sobre la
    calle, con amapolas rojas a los lados. Las baldosas, grandes y de poco
    contraste (las juntas finas en el suelo parpadean)."""
    L = 30.0
    caja(mat_bloques('baldosa_amarilla', 0xf2c64a, 0xe0b23a, ancho=1.4, alto=0.7, grosor=0.03, variacion=1.04), 0, 0, 0, 7.4, L, 0.1)
    for s in (-1, 1):
        caja(mat('borde_baldosas', 0xd49a2a, 0.6), s * 3.75, 0, 0, 0.3, L, 0.13)
        for k in range(12):
            y = -L / 2 + 1.2 + k * 2.5
            for dx in (0.0, 0.7):
                x = s * (5.0 + dx + (k % 3) * 0.6)
                cil(mat('tallo', 0x4a7a3a, 0.6), x, y, 0, 0.03, 0.5, 5)
                esfera(mat('amapola', 0xd8202a, 0.5), x, y, 0.55, 0.16, 1, esc=(1, 1, 0.6))

# ================================================================ los obstáculos
def valla_volando():
    """Un trozo de valla de madera que se lleva el tornado: cruza la calle
    por el aire, a la altura de la cabeza (se pasa agachado). Mira a +x."""
    m = madera()
    for z in (1.55, 2.05):
        caja(m, 0, 0, z, 0.12, 1.9, 0.14, inclina=0.12)
    for y in (-0.8, 0.0, 0.8):
        caja(m, 0, y, 1.3, 0.1, 0.12, 1.1, inclina=0.12)

def tejado_volando():
    """Un trozo de tejado rojo con tejas que viene botando: se salta. Centrado
    en el origen."""
    caja(mat('tejas', 0xa83a2a, 0.7), 0, 0, -0.06, 1.6, 1.1, 0.12, inclina=0.3)
    caja(madera(), 0, 0, -0.18, 1.5, 1.0, 0.08, inclina=0.3)
    for k in range(4):
        caja(mat('teja_borde', 0x8a2a20, 0.7), -0.6 + k * 0.4, 0, 0.0, 0.08, 1.1, 0.06, inclina=0.3)

def espantapajaros():
    """El espantapájaros de El Mago de Oz: palo, camisa de cuadros, sombrero
    de paja y paja saliendo. Quieto."""
    cil(madera(), 0, 0.3, 0, 0.06, 2.4, 6)
    caja(madera(), 0, 0.3, 1.6, 1.5, 0.08, 0.08)
    caja(mat_franjas('camisa_cuadros', 0x2a5a8a, 0xd8c8a0, 8, eje='X', z0=-0.4, alto=0.8), 0, 0.3, 1.1, 0.7, 0.35, 0.65)
    caja(mat('pantalon_esp', 0x5a6a3a, 0.7), 0, 0.3, 0.55, 0.5, 0.3, 0.55)
    esfera(mat('saco_cabeza', 0xd8c49a, 0.8), 0, 0.3, 2.05, 0.24, 2)
    cil(mat('sombrero_paja', 0xb89a5a, 0.8), 0, 0.3, 2.22, 0.36, 0.05, 14)
    cil(mat('sombrero_paja', 0xb89a5a, 0.8), 0, 0.3, 2.25, 0.18, 0.22, 12, r2=0.13)
    for s in (-1, 1):
        rama(mat('paja_esp', 0xe0c46a, 0.9), (s * 0.75, 0.3, 1.64), (s * 0.95, 0.3, 1.5), 0.05, 0.02, 4)

def bruja_bici():
    """La señorita Gulch en su bicicleta, vista por detrás, con la cesta (y
    Toto asomando). Cambia de carril con el intermitente."""
    neg = mat('negro_gulch', 0x1d1f25, 0.5)
    for y in (0.1, 1.5):
        cil(hierro(), 0, y, 0.38, 0.38, 0.06, 18, eje='X')
    rama(hierro(), (0, 0.1, 0.4), (0, 1.0, 0.95), 0.04, 0.04, 6)
    rama(hierro(), (0, 1.5, 0.4), (0, 1.1, 1.1), 0.04, 0.04, 6)
    caja(mat('cesta', 0x9a7a4a, 0.8), 0, -0.1, 0.75, 0.5, 0.4, 0.35)
    esfera(mat('toto', 0x2a2420, 0.7), 0, -0.1, 1.15, 0.13, 1)
    cil(neg, 0, 0.7, 0.85, 0.28, 0.8, 10, r2=0.18)
    esfera(mat('piel_gulch', 0xe8c4a8, 0.6), 0, 0.75, 1.85, 0.17, 2)
    cil(neg, 0, 0.75, 1.96, 0.18, 0.12, 12)
    caja(mat('piloto', 0xc0262c, 0.3), 0, -0.32, 0.6, 0.14, 0.03, 0.08)
    for s in (-1, 1):
        caja(mat('intermitente', 0xffa21a, 0.3), s * 0.28, -0.31, 0.75, 0.08, 0.03, 0.06)

def vaca_volando():
    """Una vaca que se lleva el tornado (como en las películas): cruza la
    calle por el aire, de lado y a la altura de la cabeza (se pasa agachado).
    Mira a +x."""
    piel = mat('piel_volando', 0x2a2420, 0.7)
    blanco_v = blanco()
    caja(piel, 0, 0, 1.55, 1.6, 0.7, 0.6, giro=0.0, inclina=0.25)
    caja(blanco_v, 0.2, 0, 1.7, 0.6, 0.72, 0.3, inclina=0.25)
    caja(piel, 0.95, 0, 1.75, 0.5, 0.4, 0.4, inclina=0.25)
    caja(mat('hocico_v', 0xe8b4a0, 0.6), 1.2, 0, 1.75, 0.16, 0.32, 0.22)
    for sx in (-0.5, 0.5):
        for sy in (-0.22, 0.22):
            rama(piel, (sx, sy, 1.5), (sx + 0.25, sy * 1.6, 1.05), 0.08, 0.07, 6)
    rama(piel, (-0.8, 0, 1.75), (-1.2, 0, 2.1), 0.04, 0.03, 5)


PIEZAS = {
    'epic_center':       (epic_center,       'wichita', dict(lado=1024, segmentos=2)),
    'century_ii':        (century_ii,        'wichita', dict(lado=1024, segmentos=2, min_bisel=1.0)),
    'museo_aviacion':    (museo_aviacion,    'wichita', dict(lado=1024, segmentos=2, min_bisel=1.0)),
    'guardian_llanuras': (guardian_llanuras, 'wichita', dict(lado=2048, segmentos=1, min_bisel=2.0)),
    'tornado_embudo':    (tornado_embudo,    'wichita', dict(lado=512, bisel=0.0, suelo=False)),
    'valla_volando':     (valla_volando,     'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
    'tejado_volando':    (tejado_volando,    'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
    'espantapajaros':    (espantapajaros,    'obstaculos', dict(lado=256, bisel=0.0)),
    'bruja_bici':        (bruja_bici,        'obstaculos', dict(lado=256, bisel=0.0)),
    'vaca_volando':      (vaca_volando,      'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
}

correr(PIEZAS)
