# Nivel 3: Central Avenue de Phoenix, Arizona (27/10/2026).
#
#   blender -b -P blender/phoenix.py -- [pieza ...] [--rapido]
#
# Isidro: la gira va a la capital o a la ciudad más famosa de cada estado; en
# Arizona, Phoenix (las dos cosas). Eligió el final en un diner de carretera y
# luz de tarde dorada. Subiendo por Central Avenue hacia el norte:
#   oeste (izquierda): el Hotel San Carlos (1928) con su letrero en el tejado ·
#                      la biblioteca Burton Barr, un cajón de cobre
#   este (derecha):    la torre Westward Ho (1928) con su antena roja · el museo
#                      de arte de Phoenix · el Museo Heard, de estilo colonial
#   al fondo:          el diner con el chile gigante en el tejado
# Acera: palmeras altas y saguaros en maceta. El resto de la calle son edificios
# únicos del kit con estilo de desierto (estuco de colores cálidos).
# Las distancias van comprimidas: es un juego, no un plano.
# Todas las fachadas en y = 0 mirando a -y.

import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import *

# ---------------------------------------------------------------- materiales
def ladrillo_crema(): return mat_bloques('ladrillo_sc', 0xe2cc9f, 0xc9b184, ancho=0.5, alto=0.22, grosor=0.02, variacion=1.05)
def estuco(nombre, color): return mat(nombre, color, 0.75)
def piedra():   return mat_bloques('piedra_phx', 0xd8c7a6, 0xbfae8c, ancho=1.2, alto=0.6, grosor=0.03, variacion=1.04)
def blanco():   return mat('blanco_phx', 0xfbf6ec, 0.5)
def oscuro():   return mat('hueco_phx', 0x2b2a2e, 0.8)
def vidrio():   return mat('vidrio_phx', 0x5f86ad, 0.15)
def teja():     return mat_franjas('teja_phx', 0xb8502e, 0x9a3f22, 30, eje='X', z0=-30, alto=60)
def rojo():     return mat('rojo_phx', 0xd23a2e, 0.45)
def verde():    return mat('verde_phx', 0x2f6a3e, 0.6)
def neon(nombre, color): return mat(nombre, color, 0.15)

def ventanas(xs, z, w, h, remate=None, y=0.0, marco=None, cristal=None):
    for x in xs:
        ventana(x, z, w, h, y=y, marco=marco or blanco(), cristal=cristal or vidrio(), remate=remate)

def toldo(x, z, w, color, y=0.0):
    caja(mat(f'toldo_{color:06x}', color, 0.6), x, y - 0.6, z, w, 1.2, 0.18, inclina=-0.35)

def escaparate(x, w, h=2.8, y=0.0):
    caja(mat('marco_esc_phx', 0x3e3a33, 0.4), x, y - 0.05, 0.3, w + 0.2, 0.1, h + 0.2)
    caja(mat('escaparate_phx', 0xcfe3f2, 0.1), x, y - 0.09, 0.4, w, 0.04, h)

def arco(m, x, y, z, w, h, prof=0.4):
    """Hueco de arco de medio punto (oscuro) con su marco, en una fachada que mira a -y."""
    caja(oscuro(), x, y - 0.02, z, w, 0.04, h - w / 2)
    cil(oscuro(), x, y - 0.02, z + h - w / 2, w / 2, 0.04, 16, eje='Y')
    caja(m, x, y - prof / 2, z + h, w + 0.6, prof, 0.25)


# ---------------------------------------------------------------- piezas únicas
def san_carlos():
    """Hotel San Carlos (1928): ladrillo crema, siete plantas de ventanas, bajo
    con arcos y toldos verdes, y el letrero rojo de neón en el tejado."""
    W, D = 30, 18
    H = 4.6 + 7 * 3.1
    caja(ladrillo_crema(), 0, D / 2, 0, W, D, H)
    caja(piedra(), 0, D / 2 - 0.15, 0, W + 0.3, D + 0.3, 4.6)           # bajo de piedra
    for x in (-10, -5, 5, 10):
        arco(piedra(), x, -0.15, 0.4, 3.0, 3.8)
        toldo(x, 3.4, 3.4, 0x2f6a3e, y=-0.15)
    caja(oscuro(), 0, -0.2, 0.3, 3.0, 0.06, 3.4)                          # entrada
    caja(mat('marquesina_sc', 0x2f6a3e, 0.5), 0, -1.2, 3.6, 5.0, 2.4, 0.3)
    texto(blanco(), 'HOTEL SAN CARLOS', 0, -2.45, 3.75, tam=0.32, prof=0.04)
    for p in range(7):
        z = 5.2 + p * 3.1
        ventanas([-12.5, -9, -5.5, -2, 2, 5.5, 9, 12.5], z, 1.5, 2.0,
                 remate='cornisa' if p == 0 else None, marco=mat('marco_sc', 0xf4ead2, 0.5))
    caja(piedra(), 0, D / 2 - 0.4, H - 0.2, W + 0.8, D + 0.8, 0.8)       # cornisa
    caja(mat('pretil_sc', 0xd4bd8f, 0.6), 0, D / 2, H + 0.6, W, D, 0.9)
    # el letrero del tejado: armazon de hierro y letras rojas
    hierro = mat('hierro_sc', 0x2c2e33, 0.4)
    for x in (-11, -5.5, 0, 5.5, 11):
        caja(hierro, x, 2.0, H + 1.5, 0.15, 0.15, 3.2)
    caja(hierro, 0, 2.0, H + 4.6, 24, 0.15, 0.15)
    caja(hierro, 0, 2.0, H + 1.6, 24, 0.15, 0.15)
    texto(neon('neon_sc', 0xff3a2e), 'HOTEL SAN CARLOS', 0, 1.85, H + 3.1, tam=2.0, prof=0.2)

def westward_ho():
    """Westward Ho (1928): torre de 16 plantas de ladrillo claro, remate de
    tejas, el letrero y la gran antena roja y blanca en lo alto."""
    W, D = 30, 20
    base = mat_ventanas('muro_westward', 0x6f8fb0, 0xe7d6b4, paso_x=1.8, paso_z=3.0, hueco_x=1.1, hueco_z=2.0, variacion=1.15)
    caja(base, 0, D / 2, 0, W, D, 12)                                      # base de 3 plantas
    caja(piedra(), 0, D / 2 - 0.2, 0, W + 0.4, D + 0.4, 4.2)
    for x in (-9, -3, 3, 9):
        arco(piedra(), x, -0.2, 0.4, 3.2, 3.6)
    caja(mat('toldo_westward', 0x8a2a2a, 0.6), 0, -1.0, 3.6, 8, 2, 0.25)
    torre = mat_ventanas('torre_westward', 0x6f8fb0, 0xead9b8, paso_x=1.8, paso_z=3.0, hueco_x=1.0, hueco_z=2.0, variacion=1.15)
    caja(torre, 0, D / 2, 12, 16, 12, 34)                                  # la torre
    for x in (-8.1, 8.1):                                                  # pilastras
        caja(mat('pilastra_westward', 0xd9c39c, 0.6), x, D / 2 - 6.1, 12, 0.6, 0.6, 34)
    caja(piedra(), 0, D / 2, 46, 17, 13, 0.8)
    tejado(teja(), 0, D / 2 - 6.5, D / 2 + 6.5, 46.8, 17.2, 3.2, cumbrera='x')
    caja(mat('cartel_westward', 0x1d2b46, 0.5), 0, D / 2 - 6.2, 12.6, 14, 0.3, 2.0)
    texto(neon('neon_westward', 0xffe066), 'WESTWARD HO', 0, D / 2 - 6.4, 13.6, tam=1.4, prof=0.12)
    # la antena: celosia roja y blanca
    for k in range(6):
        c = rojo() if k % 2 == 0 else blanco()
        cil(c, 0, D / 2, 50 + k * 2.2, 0.9 - k * 0.12, 2.2, 4, r2=0.78 - k * 0.12)
    cil(rojo(), 0, D / 2, 63.2, 0.08, 4, 6)
    esfera(neon('luz_antena', 0xff3a2e), 0, D / 2, 67.3, 0.3, 1)

def biblioteca_barr():
    """Biblioteca Burton Barr (1995): un cajón de cobre ondulado con la fachada
    de cristal y lamas de acero."""
    W, D, H = 40, 26, 16
    cobre = mat_franjas('cobre_barr', 0xb5703f, 0x9a5c32, 60, eje='X', z0=-W / 2, alto=W)
    caja(cobre, 0, D / 2, 0, W, D, H)
    caja(vidrio(), 0, -0.05, 1.2, 26, 0.08, H - 2.4)
    acero = mat('acero_barr', 0xb9c0c8, 0.3)
    for z in range(3, int(H) - 1, 2):
        caja(acero, 0, -0.6, z, 26.5, 1.0, 0.1, inclina=0.35)
    for x in (-13.2, 13.2):
        caja(acero, x, -0.3, 0, 0.4, 0.6, H)
    caja(mat('plaza_barr', 0xd8cbb2, 0.8), 0, -3, 0, 30, 6, 0.15)
    texto(mat('letras_barr', 0x2b2a2e, 0.5), 'BURTON BARR CENTRAL LIBRARY', 0, -0.9, 0.9, tam=0.55, prof=0.05)

def museo_arte():
    """Museo de Arte de Phoenix: piedra clara, bajo y largo, con el gran
    pórtico de cristal y los estandartes de colores."""
    W, D, H = 40, 24, 11
    caja(piedra(), 0, D / 2, 0, W, D, H)
    caja(vidrio(), 0, -0.1, 0.3, 14, 0.1, 7)
    caja(piedra(), 0, -2.0, 7.3, 18, 4.0, 0.6)                             # visera
    for x in (-8.5, 8.5):
        cil(mat('pilar_museo', 0xe8dcc2, 0.6), x, -3.6, 0, 0.35, 7.3, 12)
    for k, c in enumerate((0xe8463c, 0x2f6bd8, 0xffc23c, 0x2fa84f)):     # estandartes
        x = -17 + k * 2.2
        caja(mat(f'estandarte{c:06x}', c, 0.6), x, -0.25, 3.0, 1.4, 0.06, 6.5)
    caja(mat('cartel_museo', 0x2b2a2e, 0.5), 0, -4.05, 7.5, 12, 0.08, 0.35)
    texto(blanco(), 'PHOENIX ART MUSEUM', 0, -4.12, 7.68, tam=0.42, prof=0.04)
    caja(mat('jardin_museo', 0xc9b48a, 0.9), 0, -6, 0, 36, 4, 0.1)

def museo_heard():
    """Museo Heard (1929): estilo colonial español, estuco claro, tejados de
    teja, soportales con arcos y una torre pequeña con cúpula."""
    W, D, H = 40, 22, 7.5
    muro = estuco('estuco_heard', 0xf1e3cc)
    caja(muro, 0, D / 2, 0, W, D, H)
    tejado(teja(), 0, -1.0, D + 0.5, H, W + 1, 2.6, cumbrera='x')
    # soportal con arcos
    caja(muro, 0, -1.6, H - 1.4, W - 6, 3.2, 1.4)
    for k in range(9):
        x = -14 + k * 3.5
        caja(muro, x, -3.0, 0, 0.7, 0.7, H - 1.4)
    for k in range(8):
        x = -12.25 + k * 3.5
        cil(oscuro(), x, -3.25, H - 2.2, 1.35, 0.04, 14, eje='Y')
    caja(mat('suelo_soportal', 0xb8503a, 0.8), 0, -1.6, 0, W - 6, 3.2, 0.15)
    # torre con cupula de azulejo
    caja(muro, 15, 6, 0, 5, 5, 13)
    for s in (-1, 1):
        cil(oscuro(), 15 + s * 1.2, 3.47, 9.5, 0.6, 0.05, 12, eje='Y')
    cupula(mat_franjas('azulejo_heard', 0x2f8fb8, 0xf3c94a, 10, eje='Z', z0=13, alto=3), 15, 6, 13, 2.6, 3.0)
    esfera(mat('remate_heard', 0xd9a520, 0.3), 15, 6, 16.2, 0.25, 1)
    caja(mat('cartel_heard', 0x5a3a24, 0.6), 0, -3.4, H - 0.9, 10, 0.1, 0.6)
    texto(blanco(), 'HEARD MUSEUM', 0, -3.5, H - 0.6, tam=0.45, prof=0.04)
    # palmeras y un saguaro en el patio de delante
    for x in (-18, 18):
        palmera_en(x, -6, 9)
    saguaro_en(-7, -5.5, 2.6)

def palmera_en(x, y, alto):
    tronco = mat_franjas('tronco_palmera', 0x9c7a55, 0x86643f, 28, eje='Z', z0=0, alto=12)
    cil(tronco, x, y, 0, 0.32, alto, 10, r2=0.22)
    seca = mat('hoja_seca', 0xa7864f, 0.8)
    verdes = mat('hoja_palmera', 0x3f8f3a, 0.6)
    for k in range(10):
        a = k / 10 * math.pi * 2
        dx, dy = math.cos(a), math.sin(a)
        rama(seca, (x, y, alto - 0.2), (x + dx * 0.9, y + dy * 0.9, alto - 1.6), 0.14, 0.05, 4)
        rama(verdes, (x, y, alto), (x + dx * 1.6, y + dy * 1.6, alto + 0.6), 0.16, 0.12, 4)
        rama(verdes, (x + dx * 1.6, y + dy * 1.6, alto + 0.6), (x + dx * 2.8, y + dy * 2.8, alto - 0.5), 0.12, 0.03, 4)
    esfera(mat('cogollo', 0x5a7a34, 0.6), x, y, alto, 0.4, 1)

def saguaro_en(x, y, alto):
    piel = mat_franjas('saguaro_costillas', 0x4f8f45, 0x3f7a38, 12, eje='X', z0=x - 0.4, alto=0.8)
    cil(piel, x, y, 0, 0.32, alto, 12, r2=0.28)
    esfera(piel, x, y, alto, 0.28, 2)
    for s, h in ((-1, alto * 0.45), (1, alto * 0.6)):
        rama(piel, (x, y, h), (x + s * 0.6, y, h + 0.1), 0.2, 0.2, 10)
        cil(piel, x + s * 0.6, y, h, 0.2, alto * 0.35, 10)
        esfera(piel, x + s * 0.6, y, h + alto * 0.35, 0.2, 1)

def palmera():
    """Palmera alta de Central Avenue (pieza de la acera)."""
    palmera_en(0, 0, 8.5)

def saguaro_maceta():
    """Saguaro en una maceta redonda de piedra (pieza de la acera)."""
    cil(piedra(), 0, 0, 0, 0.75, 0.6, 16)
    cil(mat('tierra_maceta', 0xc9a06a, 0.9), 0, 0, 0.6, 0.68, 0.04, 16)
    saguaro_en(0, 0, 2.6)

def diner_final():
    """El diner del final: vagón cromado con franja roja, ventanales, el
    letrero de neón, un chile gigante en el tejado, el aparcamiento con dos
    coches de los años 50 y el poste de «EAT»."""
    cromo = mat('cromo_diner', 0xd8dde3, 0.2)
    franja = rojo()
    W, D, H = 18, 7, 4.2
    # el aparcamiento delante, del ancho de la calle
    caja(mat('asfalto_diner', 0x55575e, 0.9), 0, -6, 0, 30, 16, 0.06)
    for x in (-9, -3, 3, 9):
        caja(blanco(), x, -9, 0.06, 0.15, 5, 0.02)
    # el vagon: base, cuerpo redondeado y tejado. 27/10 (2): acero acanalado
    # (antes salia beige y plano), ventanales con la luz de dentro, linea de neon.
    acero = mat_franjas('acero_diner', 0xf4f7fa, 0xbcc5cf, 46, eje='X', z0=-W / 2, alto=W)
    caja(mat('zocalo_diner', 0x2a2d33, 0.5), 0, D / 2, 0, W, D, 0.6)
    caja(acero, 0, D / 2, 0.6, W, D, H - 1.2)
    cil(cromo, 0, D / 2, H - 0.6, D / 2, W, 24, eje='X')
    caja(franja, 0, -0.03, 0.95, W + 0.04, 0.06, 0.45)
    caja(franja, 0, -0.03, H - 1.0, W + 0.04, 0.06, 0.25)
    caja(neon('neon_borde', 0x46e0d0), 0, -0.07, H - 0.68, W + 0.04, 0.05, 0.08)
    marco = mat('marco_diner', 0x9aa3ad, 0.25)
    for k in range(7):                                                     # ventanales
        x = -7.2 + k * 2.4
        if abs(x) < 0.5:
            continue
        caja(marco, x, -0.04, 1.5, 2.1, 0.04, 1.8)
        caja(mat('interior_diner', 0xffcf6a, 0.15), x, -0.07, 1.6, 1.9, 0.03, 1.6)
        caja(mat('lampara_diner', 0xfff6d8, 0.1), x, -0.09, 2.85, 1.2, 0.02, 0.12)
    caja(marco, 0, -0.05, 0.6, 1.6, 0.05, 2.6)
    caja(mat('puerta_diner', 0x8fd0e8, 0.1), 0, -0.08, 0.7, 1.3, 0.04, 2.35)
    caja(mat('cartel_diner', 0x1d2b46, 0.5), 0, -0.6, H + 0.3, 9, 0.4, 1.6)
    texto(neon('neon_diner', 0xff4fa0), 'DINER', 0, -0.85, H + 1.1, tam=1.3, prof=0.15)
    # el chile gigante del tejado (el ingrediente de este nivel): una curva de
    # verdad, gorda por el rabito y con la punta hacia arriba, sobre dos postes.
    chile = mat('chile_gigante', 0xe8302a, 0.3)
    puntos = []
    for i in range(9):
        t = i / 8
        x = -4.2 + 8.2 * t
        z = H + 2.9 + 1.0 * math.sin(math.pi * t * 0.85) - (2.2 * (t - 0.75) if t > 0.75 else 0) * -1
        r = 0.85 * (1 - 0.88 * t ** 1.6)
        puntos.append(((x, D / 2 - 0.5, z), r))
    for (p0, r0), (p1, r1) in zip(puntos, puntos[1:]):
        rama(chile, p0, p1, r0, r1, 18)
        esfera(chile, p1[0], p1[1], p1[2], r1, 2)
    esfera(chile, puntos[0][0][0], puntos[0][0][1], puntos[0][0][2], puntos[0][1], 2)
    rama(mat('brillo_chile', 0xff9a8a, 0.2), (-3.4, D / 2 - 1.25, H + 3.4), (0.4, D / 2 - 1.25, H + 4.0), 0.13, 0.08, 8)
    tallo = mat('tallo_chile', 0x3fae3a, 0.5)
    esfera(tallo, -4.75, D / 2 - 0.5, H + 2.95, 0.55, 2, esc=(0.7, 1.1, 1.1))
    rama(tallo, (-5.0, D / 2 - 0.5, H + 3.1), (-5.6, D / 2 - 0.5, H + 4.1), 0.22, 0.12, 8)
    for x in (-3.0, 2.2):
        cil(mat('soporte_chile', 0x2a2d33, 0.4), x, D / 2 - 0.5, H + 0.4, 0.12, 2.8, 6)
    # el poste de «EAT» con su flecha
    poste = mat('poste_diner', 0x2a2d33, 0.4)
    cil(poste, 12, -2, 0, 0.18, 9, 8)
    caja(mat('fondo_eat', 0x2f8fb8, 0.5), 12, -2.2, 6, 3.2, 0.3, 2.4)
    texto(neon('neon_eat', 0xffe066), 'EAT', 12, -2.4, 7.2, tam=1.1, prof=0.12)
    caja(neon('neon_flecha', 0xff4fa0), 10.2, -2.3, 5.7, 3.0, 0.2, 0.3, giro=0.0)
    # dos coches de los años 50 aparcados
    for x, c in ((-8, 0x46c2b8), (7, 0xe8463c)):
        cuerpo = mat(f'coche50_{c:06x}', c, 0.25)
        caja(cuerpo, x, -6, 0.35, 2.0, 4.4, 0.7)
        caja(cuerpo, x, -6.2, 1.05, 1.7, 2.2, 0.6)
        caja(vidrio(), x, -7.32, 1.08, 1.5, 0.04, 0.5)
        for s in (-1, 1):
            caja(cuerpo, x + s * 0.85, -4.2, 1.0, 0.12, 0.8, 0.35)        # aletas
            cil(mat('rueda_50', 0x1d1e21, 0.8), x + s * 0.95, -7.4, 0.35, 0.34, 0.24, 14, eje='X')
            cil(mat('rueda_50', 0x1d1e21, 0.8), x + s * 0.95, -4.6, 0.35, 0.34, 0.24, 14, eje='X')
        caja(cromo, x, -8.25, 0.4, 2.1, 0.12, 0.25)
    for x in (-13, 13.5):
        saguaro_en(x, 2, 3.0)


PIEZAS = {
    'san_carlos':      (san_carlos,      'phoenix', dict(lado=1024, segmentos=2)),
    'westward_ho':     (westward_ho,     'phoenix', dict(lado=1024, segmentos=2)),
    'biblioteca_barr': (biblioteca_barr, 'phoenix', dict(lado=1024, segmentos=2)),
    'museo_arte':      (museo_arte,      'phoenix', dict(lado=1024, segmentos=2)),
    'museo_heard':     (museo_heard,     'phoenix', dict(lado=1024, segmentos=2)),
    'palmera':         (palmera,         'phoenix', dict(lado=256, bisel=0.0)),
    'saguaro_maceta':  (saguaro_maceta,  'phoenix', dict(lado=256, bisel=0.0)),
    'diner_final':     (diner_final,     'phoenix', dict(lado=2048, segmentos=2)),
}

correr(PIEZAS)
