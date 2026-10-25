# Kit de piezas de fachada para que cada edificio de relleno sea ÚNICO (25/10/2026).
#
#   blender -b -P blender/kit.py -- [pieza ...] [--rapido]
#
# Isidro: «que las calles no sean genéricas sino que cada edificio sea único y
# esté siempre en el mismo punto». Repetir el mismo tramo de 20 se notaba. En
# vez de modelar cien edificios, se modelan piezas (bajos de tienda, plantas de
# ventanas de varios estilos, cornisas y remates) y el juego monta con ellas un
# edificio distinto en cada solar: cuántas plantas, qué estilo, de qué color,
# qué toldo y qué rótulo. Lo decide una semilla fija por solar, así que cada
# edificio es siempre el mismo y está siempre en el mismo sitio.
#
# Todas salen CLARAS (casi blancas, solo con la sombra de los rincones y el
# dibujo de la piedra o el ladrillo): el juego les da el color de cada edificio.
# Cada pieza mide 20 de ancho, con la fachada en y = 0 mirando a -y y la base
# en z = 0; el juego las apila.
#   bajos:     4.6 de alto     plantas: 3.0     cornisas: 1.2     remates: lo suyo

import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import *

W, D = 20.0, 12.0
def pared():   return mat_bloques('kit_pared', 0xf3efe6, 0xdcd5c6, ancho=1.6, alto=0.55, grosor=0.01, variacion=1.02)
def lisa():    return mat('kit_lisa', 0xfbf8f1, 0.55)
def ladr():    return mat_bloques('kit_ladrillo', 0xefe6dc, 0xd2c6b6, ancho=0.4, alto=0.15, grosor=0.014, variacion=1.04)
def marco():   return mat('kit_marco', 0xffffff, 0.5)
def vidrio():  return mat('kit_vidrio', 0x4a6b92, 0.15)
def oscuro():  return mat('kit_hueco', 0x3a3a40, 0.8)
def metal():   return mat('kit_metal', 0x9aa0a8, 0.4)

def fila(xs, z, w, h, remate=None, y=0.0, persiana=None):
    for x in xs:
        ventana(x, z, w, h, y=y, marco=marco(), cristal=vidrio(), remate=remate, persiana=persiana)


# ---------------------------------------------------------------- bajos (4.6)
def bajo_tiendas():
    """Tres escaparates con su puerta entre pilastras."""
    caja(pared(), 0, D / 2, 0, W, D, 4.6)
    for x in (-6.4, 0, 6.4):
        caja(metal(), x, -0.05, 0.25, 5.4, 0.1, 3.3)
        caja(mat('kit_escaparate', 0xd5e6f3, 0.1), x, -0.09, 0.35, 5.0, 0.04, 3.1)
    for x in (-9.6, -3.2, 3.2, 9.6):
        caja(lisa(), x, -0.12, 0, 0.7, 0.25, 4.6)
    caja(lisa(), 0, -0.1, 3.75, W, 0.22, 0.85)                            # la banda del rótulo
    caja(lisa(), 0, D / 2, 4.5, W + 0.1, D + 0.1, 0.12)

def bajo_grande():
    """Un escaparate enorme y una entrada con arco."""
    caja(pared(), 0, D / 2, 0, W, D, 4.6)
    caja(metal(), -3, -0.05, 0.25, 12, 0.1, 3.4)
    caja(mat('kit_escaparate', 0xd5e6f3, 0.1), -3, -0.09, 0.35, 11.6, 0.04, 3.2)
    caja(oscuro(), 6.5, -0.04, 0, 3.2, 0.08, 3.2)
    cil(lisa(), 6.5, -0.06, 3.2, 1.75, 0.1, 20, eje='Y')
    cil(oscuro(), 6.5, -0.1, 3.2, 1.5, 0.04, 20, eje='Y')
    caja(lisa(), 0, D / 2, 4.5, W + 0.1, D + 0.1, 0.12)

def bajo_banco():
    """Piedra almohadillada con dos ventanales en arco (banco, hotel)."""
    caja(mat_bloques('kit_rustico', 0xece6da, 0xc9c0ae, ancho=1.2, alto=0.5, grosor=0.03), 0, D / 2, 0, W, D, 4.6)
    for x in (-5, 5):
        caja(marco(), x, -0.05, 0.6, 3.6, 0.1, 2.8)
        caja(vidrio(), x, -0.09, 0.7, 3.2, 0.04, 2.6)
        cil(marco(), x, -0.06, 3.4, 1.8, 0.1, 20, eje='Y')
        cil(vidrio(), x, -0.1, 3.4, 1.55, 0.04, 20, eje='Y')
    caja(oscuro(), 0, -0.04, 0, 2.4, 0.08, 3.4)
    caja(lisa(), 0, -0.3, 3.6, 3.4, 0.6, 0.25)
    caja(lisa(), 0, D / 2, 4.5, W + 0.1, D + 0.1, 0.12)


# ---------------------------------------------------------------- plantas (3.0)
def planta_lisa():
    caja(pared(), 0, D / 2, 0, W, D, 3.0)
    fila([-8, -4, 0, 4, 8], 0.6, 1.5, 1.9)

def planta_frontones():
    caja(pared(), 0, D / 2, 0, W, D, 3.0)
    fila([-7.5, -2.5, 2.5, 7.5], 0.55, 1.6, 1.8, remate='fronton')
    for x in (-10, -5, 0, 5, 10):
        caja(lisa(), x, -0.1, 0, 0.6, 0.2, 3.0)

def planta_miradores():
    """Dos miradores salientes y dos ventanas."""
    caja(pared(), 0, D / 2, 0, W, D, 3.0)
    for x in (-5, 5):
        caja(pared(), x, -0.6, 0.2, 4.2, 1.2, 2.6)
        caja(lisa(), x, -0.65, 2.8, 4.5, 1.35, 0.2)
        fila([x], 0.6, 2.6, 1.7, y=-1.2)
    fila([-9, 9], 0.6, 1.2, 1.8)

def planta_cristal():
    """Banda corrida de cristal (edificio moderno)."""
    caja(pared(), 0, D / 2, 0, W, D, 3.0)
    caja(vidrio(), 0, -0.04, 0.5, W - 0.6, 0.08, 2.1)
    for k in range(11):
        caja(metal(), -9.6 + k * 1.92, -0.1, 0.5, 0.1, 0.06, 2.1)

def planta_ladrillo():
    """Ladrillo con ventanas de arco rebajado."""
    caja(ladr(), 0, D / 2, 0, W, D, 3.0)
    for x in (-8, -4, 0, 4, 8):
        ventana(x, 0.55, 1.4, 1.8, marco=marco(), cristal=vidrio())
        caja(lisa(), x, -0.08, 2.45, 1.8, 0.16, 0.22)

def planta_balcones():
    caja(pared(), 0, D / 2, 0, W, D, 3.0)
    fila([-7.5, -2.5, 2.5, 7.5], 0.5, 1.5, 2.1)
    for x in (-7.5, 2.5):
        caja(lisa(), x + 2.5, -0.45, 0.35, 6.2, 0.9, 0.12)
        caja(metal(), x + 2.5, -0.88, 0.47, 6.2, 0.04, 0.05)
        caja(metal(), x + 2.5, -0.88, 1.2, 6.2, 0.04, 0.05)
        for k in range(13):
            caja(metal(), x - 0.6 + k * 0.5, -0.88, 0.47, 0.035, 0.035, 0.75)


# ---------------------------------------------------------------- cornisas (1.2)
def cornisa_clasica():
    caja(lisa(), 0, D / 2 - 0.3, 0, W + 0.2, D + 0.6, 0.35)
    caja(lisa(), 0, D / 2 - 0.5, 0.35, W + 0.6, D + 1.0, 0.55)
    for k in range(25):
        caja(lisa(), -9.6 + k * 0.8, -0.35, 0.12, 0.28, 0.28, 0.22)       # dentículos
    caja(lisa(), 0, D / 2 - 0.4, 0.9, W + 0.4, D + 0.8, 0.3)

def cornisa_deco():
    for i in range(3):
        caja(lisa(), 0, D / 2 - 0.2 + i * 0.4, i * 0.4, W + 0.4 - i * 0.6, D + 0.4 - i * 0.8, 0.4)
    for x in (-8, 0, 8):
        caja(lisa(), x, -0.3, 0, 1.2, 0.5, 1.6)

def cornisa_simple():
    caja(metal(), 0, D / 2, 0, W + 0.2, D + 0.2, 0.5)


# ---------------------------------------------------------------- remates
def remate_deposito():
    madera = mat('kit_madera', 0xd8c1a6, 0.8)
    for dx in (-0.7, 0.7):
        for dy in (-0.7, 0.7):
            cil(metal(), 4 + dx, 6 + dy, 0, 0.08, 1.6, 6)
    caja(metal(), 4, 6, 1.5, 2.2, 2.2, 0.12)
    cil(madera, 4, 6, 1.6, 1.15, 2.0, 16)
    for k in (0.3, 1.0, 1.7):
        cil(metal(), 4, 6, 1.6 + k, 1.17, 0.06, 16)
    cil(mat('kit_tejadillo', 0x9a8a7c, 0.8), 4, 6, 3.6, 1.25, 0.9, 16, r2=0.06)

def remate_mansarda():
    tejado(mat_bloques('kit_pizarra', 0xc9ced6, 0xaab0ba, ancho=0.45, alto=0.25, grosor=0.015), 0, 0.4, D - 0.4, 0, W, 3.0, vuelo=0.1, cumbrera='x')
    for x in (-6, 0, 6):
        caja(pared(), x, 1.2, 0, 1.6, 1.4, 1.8)
        fronton(lisa(), x, 0.45, 1.8, 1.9, 0.8, 1.5)
        ventana(x, 0.3, 0.8, 1.2, y=0.5, marco=marco(), cristal=vidrio())

def remate_atico():
    caja(pared(), 0, D / 2 + 1.5, 0, W - 5, D - 4, 3.2)
    caja(vidrio(), 0, 3.45, 0.4, W - 6, 0.05, 2.4)
    caja(lisa(), 0, D / 2 + 1.5, 3.2, W - 4.6, D - 3.6, 0.3)
    for k in range(6):
        esfera(mat('kit_planta', 0x9fc98c, 0.8), -7 + k * 2.8, 0.8, 0.5, 0.5, 1)

def remate_antena():
    caja(metal(), -5, 5, 0, 2.5, 2, 1.2)
    caja(metal(), 4, 7, 0, 3, 2.5, 1.0)
    cil(metal(), 0, 5, 0, 0.15, 6, 8, r2=0.05)
    esfera(mat('kit_baliza', 0xff5a4a, 0.3), 0, 5, 6.1, 0.2, 1)


# ---------------------------------------------------------------- extras
def toldo_kit():
    """Toldo de una tienda (el juego le da el color)."""
    caja(mat_franjas('kit_toldo', 0xffffff, 0xe6e6e6, 6, eje='X', z0=-2.6, alto=5.2), 0, -0.65, 0, 5.2, 1.3, 0.16, inclina=-0.4)
    for s in (-1, 1):
        fronton(mat('kit_toldo_lado', 0xf2f2f2), s * 2.55, -1.25, -0.5, 0.1, 0.5, 1.2)


SEG = dict(lado=512, segmentos=2)
PIEZAS = {n: (f, 'kit', dict(SEG)) for n, f in {
    'bajo_tiendas': bajo_tiendas, 'bajo_grande': bajo_grande, 'bajo_banco': bajo_banco,
    'planta_lisa': planta_lisa, 'planta_frontones': planta_frontones, 'planta_miradores': planta_miradores,
    'planta_cristal': planta_cristal, 'planta_ladrillo': planta_ladrillo, 'planta_balcones': planta_balcones,
    'cornisa_clasica': cornisa_clasica, 'cornisa_deco': cornisa_deco, 'cornisa_simple': cornisa_simple,
    'remate_deposito': remate_deposito, 'remate_mansarda': remate_mansarda, 'remate_atico': remate_atico,
    'remate_antena': remate_antena, 'toldo_kit': toldo_kit,
}.items()}
for n in ('cornisa_clasica', 'cornisa_deco', 'cornisa_simple', 'remate_deposito', 'remate_mansarda',
          'remate_atico', 'remate_antena', 'toldo_kit'):
    PIEZAS[n][2]['suelo'] = False

correr(PIEZAS)
