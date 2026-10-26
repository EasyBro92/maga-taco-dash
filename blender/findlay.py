# Nivel 2: Main Street de Findlay, Ohio, «Flag City USA» (26/10/2026).
#
#   blender -b -P blender/findlay.py -- [pieza ...] [--rapido]
#
# Mismo estilo tipo Pixar que nueva_york.py. Subiendo por South Main Street
# hacia el norte, hasta el juzgado del condado de Hancock (1888):
#   oeste (izquierda): la antigua iglesia de 1867 que fue el periódico The
#                      Courier · la heladería Dietsch Brothers · el depósito de
#                      agua · el edificio Davis (1841, de los más antiguos)
#   este (derecha):    la sede de Marathon
#   al fondo:          el juzgado con su torre del reloj y John Hancock en lo
#                      alto, y delante la plaza con el escenario del mitin
# El resto de la calle son edificios únicos del kit (ladrillo de pueblo).
# Las distancias van comprimidas: es un juego, no un plano.
# Todas las fachadas en y = 0 mirando a -y.

import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import *

# ---------------------------------------------------------------- materiales
def arenisca(): return mat_bloques('arenisca_fdl', 0xc9b48f, 0xa8936f, ancho=1.1, alto=0.55, grosor=0.03, variacion=1.06)
def granito():  return mat_bloques('granito_fdl', 0x9c9890, 0x7e7a72, ancho=1.3, alto=0.6, grosor=0.03, variacion=1.04)
def ladrillo(nombre='ladrillo_fdl', color=0xb0583f):
    return mat_bloques(nombre, color, 0xdccfba, ancho=0.4, alto=0.15, grosor=0.012, mezcla=0.7)
def liso():     return mat('piedra_lisa_fdl', 0xeee4cf, 0.55)
def blanco():   return mat('blanco_fdl', 0xfbf9f3, 0.5)
def oscuro():   return mat('hueco_fdl', 0x2b2a2e, 0.8)
def vidrio():   return mat('vidrio_fdl', 0x5f86ad, 0.15)
def bronce():   return mat('bronce_fdl', 0x3e3a33, 0.4)
def cobre():    return mat('cobre_fdl', 0x6fa596, 0.6)
def pizarra():  return mat('pizarra_fdl', 0x4f5966, 0.7)
def oro():      return mat('oro_fdl', 0xe0b040, 0.3)
def madera():   return mat('madera_fdl', 0x8c5a36, 0.8)
def rojo():     return mat('rojo_fdl', 0xc8283a, 0.5)
def azul():     return mat('azul_fdl', 0x1f3c88, 0.5)

def ventanas(xs, z, w, h, remate=None, y=0.0, marco=None):
    for x in xs:
        ventana(x, z, w, h, y=y, marco=marco or blanco(), cristal=vidrio(), remate=remate)

def cornisa(W, D, z, h=0.5, vuelo=0.4, m=None):
    caja(m or liso(), 0, D / 2 - vuelo / 2, z, W, D + vuelo, h)

def toldo(x, z, w, color, y=0.0):
    caja(mat(f'toldo_{color:06x}', color, 0.6), x, y - 0.6, z, w, 1.2, 0.18, inclina=-0.35)

def escaparate(x, w, h=2.6, y=0.0):
    caja(bronce(), x, y - 0.05, 0.3, w + 0.2, 0.1, h + 0.2)
    caja(mat('escaparate_luz', 0xcfe3f2, 0.1), x, y - 0.09, 0.4, w, 0.04, h)

def bandera(x, y, z, alto=1.4, ancho=0.9, giro=0.0):
    """Asta con la bandera de EE. UU. (franjas rojas y blancas y el cuadro azul)."""
    cil(mat('asta', 0xd8d8d8, 0.3), x, y, z, 0.035, alto, 8)
    esfera(oro(), x, y, z + alto + 0.04, 0.06, 1)
    fh = ancho * 0.55
    z0 = z + alto - fh
    caja(mat_franjas(f'franjas{z0:.2f}', 0xd8283a, 0xffffff, 7, z0=z0, alto=fh), x + ancho / 2 + 0.03, y, z0, ancho, 0.03, fh)
    caja(azul(), x + 0.03 + ancho * 0.21, y - 0.02, z0 + fh * 0.46, ancho * 0.42, 0.02, fh * 0.54)

def guirnalda(x0, x1, y, z, n=6):
    """Banderines tricolores colgando en curva entre dos puntos."""
    colores = (rojo(), blanco(), azul())
    for k in range(n * 3):
        u = (k + 0.5) / (n * 3)
        x = x0 + (x1 - x0) * u
        caida = 0.35 * math.sin(u * math.pi)
        caja(colores[k % 3], x, y, z - caida, 0.3, 0.03, 0.34)


# ---------------------------------------------------------------- piezas únicas
def courier():
    """La antigua iglesia de 1867 que en 1909 pasó a ser el periódico The
    Courier: piedra, ventanales góticos, torre con aguja y el rótulo."""
    W, H, D = 24, 11, 18
    piedra = arenisca()
    caja(piedra, 0, D / 2, 0, W, D, H)
    tejado(pizarra(), 0, 0, D, H, W + 0.6, 5.5)
    hastial(piedra, 0, 0, D, H, W, 5.5)
    for x in (-8, 8):
        caja(piedra, x, 0.0, 1.0, 2.2, 0.15, 5.6)
        fronton(piedra, x, -0.08, 6.6, 2.4, 1.6, 0.15)
        caja(vidrio(), x, -0.1, 1.4, 1.5, 0.04, 5.0)
    # la torre del campanario con su aguja
    caja(piedra, 0, -0.5, 0, 6, 6, H + 7)
    caja(liso(), 0, -0.5, H + 7, 6.4, 6.4, 0.5)
    cil(pizarra(), 0, 2.5, H + 7.5, 3.4, 9.0, 4, r2=0.05)
    esfera(oro(), 0, 2.5, H + 16.6, 0.25, 1)
    caja(oscuro(), 0, -3.52, 0.4, 2.6, 0.06, 4.2)                         # la puerta
    fronton(piedra, 0, -3.6, 4.6, 3.2, 1.6, 0.2)
    caja(vidrio(), 0, -3.55, 8.0, 1.6, 0.04, 3.6)                         # ventanal de la torre
    caja(mat('reloj_fdl', 0xf6f0de, 0.4), 0, -3.56, H + 3.4, 2.2, 0.04, 2.2)
    caja(mat('cartel_courier', 0x1d2b46, 0.5), 0, -3.7, 5.3, 5.6, 0.12, 1.1)
    texto(mat('letras_courier', 0xf4e6c4, 0.4), 'THE COURIER', 0, -3.78, 5.85, tam=0.75, prof=0.05)

def heladeria():
    """Dietsch Brothers, la heladería de toda la vida: ladrillo, escaparate,
    toldo de rayas y un cucurucho gigante en el tejado."""
    W, H, D = 20, 6.5, 14
    caja(ladrillo('ladrillo_helados', 0xa9503b), 0, D / 2, 0, W, D, H)
    escaparate(-4.5, 7.5, h=3.0)
    escaparate(5.5, 5.5, h=3.0)
    caja(mat('puerta_helados', 0xf4e6c4, 0.5), 1.0, -0.06, 0.3, 1.4, 0.06, 2.6)
    caja(mat_franjas('toldo_helados', 0xd8283a, 0xffffff, 9, eje='X', z0=-W / 2, alto=W), 0, -0.7, 3.5, W - 1, 1.4, 0.18, inclina=-0.35)
    caja(mat('cartel_helados', 0xf6efe0, 0.4), 0, -0.12, 4.4, 14, 0.14, 1.4)
    texto(mat('letras_helados', 0xb8283a, 0.4), 'DIETSCH BROTHERS', 0, -0.2, 5.1, tam=0.9, prof=0.06)
    cornisa(W, D, H, 0.45, 0.35, m=liso())
    # el cucurucho del tejado
    galleta = mat('galleta', 0xd9a25a, 0.7)
    cil(galleta, 6, 4, H + 0.4, 0.15, 3.2, 16, r2=1.3)
    esfera(mat('helado_rosa', 0xf5a3b8, 0.6), 6, 4, H + 4.1, 1.45, 2)
    esfera(mat('helado_choco', 0x7a4a2c, 0.6), 6, 4, H + 5.5, 1.05, 2)
    esfera(mat('guinda', 0xd0182c, 0.3), 6, 4, H + 6.7, 0.35, 1)
    cil(bronce(), 6, 4, H, 0.12, 0.6, 8)

def deposito_agua():
    """El depósito de agua del pueblo sobre sus patas, con FINDLAY pintado,
    en un solar con césped, una valla blanca y banderas."""
    W, D = 20, 14
    caja(mat('cesped_fdl', 0x6fa64c, 0.9), 0, D / 2, 0, W, D, 0.08)
    caja(blanco(), 0, -0.2, 0, W - 1, 0.1, 0.9)                           # la valla
    for k in range(20):
        caja(blanco(), -9 + k * (18 / 19), -0.2, 0, 0.12, 0.14, 1.1)
    acero = mat('acero_deposito', 0xdde4ea, 0.4)
    cx, cy, alto = 0, 7, 22
    for a in range(4):
        ang = a * math.pi / 2 + math.pi / 4
        x, y = cx + 4.2 * math.cos(ang), cy + 4.2 * math.sin(ang)
        rama(acero, (x, y, 0), (cx + 2.6 * math.cos(ang), cy + 2.6 * math.sin(ang), alto), 0.3, 0.25, 8)
    cil(acero, cx, cy, 0, 0.6, alto, 10)                                  # tubo central
    cil(acero, cx, cy, alto - 0.5, 3.2, 0.5, 24)
    esfera(acero, cx, cy, alto + 3.5, 4.6, 3, esc=(1, 1, 0.85))
    cil(acero, cx, cy, alto + 7.2, 0.4, 1.0, 10, r2=0.05)
    caja(azul(), cx, cy - 4.3, alto + 2.6, 7.2, 0.25, 1.6)
    texto(blanco(), 'FINDLAY', cx, cy - 4.45, alto + 3.4, tam=1.3, prof=0.08)
    for x in (-7, 7):
        bandera(x, 2, 0, alto=6.0, ancho=2.0)

def davis():
    """El edificio Davis (1841): tres plantas de ladrillo, ventanas altas con
    guardapolvos de piedra y una cornisa de ménsulas."""
    W, H, D = 20, 13, 14
    caja(ladrillo('ladrillo_davis', 0x9e4f3a), 0, D / 2, 0, W, D, H)
    for x, c in ((-6, 0x2d5a3a), (0, 0x22314f), (6, 0x7a2a32)):
        escaparate(x, 4.6, h=3.0)
        toldo(x, 3.6, 5.2, c)
    caja(liso(), 0, -0.1, 4.1, W, 0.2, 0.4)
    for k in range(2):
        z = 5.2 + k * 3.6
        ventanas([-7.5, -4.5, -1.5, 1.5, 4.5, 7.5], z, 1.2, 2.5, marco=liso())
        for x in (-7.5, -4.5, -1.5, 1.5, 4.5, 7.5):
            fronton(liso(), x, -0.12, z + 2.6, 1.6, 0.35, 0.14)
    cornisa(W, D, H, 0.7, 0.6, m=liso())
    for k in range(12):
        caja(liso(), -9.2 + k * (18.4 / 11), -0.35, H - 0.55, 0.3, 0.5, 0.55)
    caja(liso(), 0, -0.16, H + 0.7, 6, 0.3, 1.2)
    texto(mat('letras_davis', 0x6b3a2a, 0.5), 'DAVIS 1841', 0, -0.33, H + 1.3, tam=0.6, prof=0.05)

def marathon():
    """La sede de Marathon: oficinas modernas de seis plantas, ladrillo claro y
    franjas de cristal, vestíbulo alto y el nombre encima de la entrada."""
    W, H, D = 40, 22, 16
    caja(mat_ventanas('muro_marathon', 0x6b93b8, 0xc9b9a0, paso_x=1.6, paso_z=3.0, hueco_x=1.3, hueco_z=2.0, variacion=1.12),
         0, D / 2, 4.5, W, D, H - 4.5)
    caja(granito(), 0, D / 2, 0, W, D, 4.5)
    caja(mat('vestibulo_marathon', 0xcfe3f2, 0.1), 0, -0.06, 0.3, 16, 0.05, 3.9)
    for x in (-8, -4, 0, 4, 8):
        caja(bronce(), x, -0.1, 0.3, 0.2, 0.1, 3.9)
    for x in (-18, -12, 12, 18):
        caja(mat('pilastra_marathon', 0xd8cbb2, 0.5), x, -0.2, 4.5, 1.2, 0.4, H - 4.5)
    caja(liso(), 0, D / 2, H, W + 0.4, D + 0.4, 0.6)
    caja(mat('rojo_marathon', 0xc8283a, 0.4), 0, -0.25, 4.7, 18, 0.3, 1.4)
    texto(blanco(), 'MARATHON', 0, -0.42, 5.4, tam=1.0, prof=0.06)
    for x in (-12, 12):
        bandera(x, -1.4, 0, alto=7.5, ancho=2.2)

def farola_bandera():
    """Farola de Main Street con su bandera: en Flag City las hay en todas."""
    poste = mat('poste_fdl', 0x2c3a34, 0.4)
    cil(poste, 0, 0, 0, 0.15, 0.3, 10, r2=0.1)
    cil(poste, 0, 0, 0.3, 0.07, 3.6, 8, r2=0.055)
    cil(poste, 0, 0, 3.9, 0.22, 0.12, 10)
    esfera(mat('foco_fdl', 0xfff3c4, 0.2), 0, 0, 4.25, 0.28, 2, esc=(1, 1, 1.2))
    cil(poste, 0, 0, 4.55, 0.24, 0.12, 10, r2=0.05)
    # el mástil inclinado hacia la calzada con la bandera
    rama(poste, (0, 0, 2.6), (0.75, 0, 3.4), 0.03, 0.025, 6)
    fh = 0.62
    caja(mat_franjas('franjas_farola', 0xd8283a, 0xffffff, 7, z0=2.75, alto=fh), 0.95, 0, 2.75, 1.0, 0.03, fh)
    caja(azul(), 0.66, -0.02, 2.75 + fh * 0.46, 0.42, 0.02, fh * 0.54)

def juzgado_final():
    """El juzgado del condado de Hancock (1888): piedra rústica con remates de
    granito, pabellones en las esquinas con mansarda, la torre del reloj con
    cúpula de cobre y John Hancock en lo alto. Delante, la plaza con el
    escenario del mitin, banderas y la pancarta."""
    W, H, D = 44, 15, 26
    piedra = arenisca()
    caja(granito(), 0, D / 2, 0, W, D, 1.6)                               # zócalo
    caja(piedra, 0, D / 2, 1.6, W, D, H - 1.6)
    caja(granito(), 0, D / 2, H, W + 0.6, D + 0.6, 0.7)
    # pabellones de las esquinas, salientes, con tejado de mansarda
    for s in (-1, 1):
        cx = s * (W / 2 - 4)
        caja(piedra, cx, D / 2 - 1, 0, 8, D + 2, H + 2)
        caja(granito(), cx, D / 2 - 1, H + 2, 8.6, D + 2.6, 0.5)
        cil(pizarra(), cx, D / 2 - 1, H + 2.5, 5.2, 4.0, 4, r2=3.2)
        ventanas([cx - 2, cx + 2], 3.2, 1.4, 3.6, y=-1.0, marco=granito(), remate='fronton')
        ventanas([cx - 2, cx + 2], 9.0, 1.4, 3.4, y=-1.0, marco=granito(), remate='cornisa')
    for x in (-12, -8, 8, 12):
        ventana(x, 3.2, 1.6, 3.6, marco=granito(), cristal=vidrio(), remate='cornisa')
        ventana(x, 9.0, 1.6, 3.4, marco=granito(), cristal=vidrio())
    # pórtico central con arcos y frontón
    caja(granito(), 0, -1.6, 0, 16, 3.2, 1.6)
    escalinata(granito(), 0, -3.2, 0, 12, 6, huella=0.4, tabica=0.27)
    for x in (-6, -2, 2, 6):
        cil(granito(), x, -2.6, 1.6, 0.6, 8.0, 14)
    caja(piedra, 0, -1.6, 9.6, 16, 3.2, 1.6)
    fronton(piedra, 0, -3.2, 11.2, 17, 3.2, 3.2)
    caja(oscuro(), 0, -0.05, 1.6, 3.0, 0.06, 5.0)
    texto(mat('letras_juzgado', 0x4a4036, 0.5), 'HANCOCK COUNTY', 0, -3.25, 10.4, tam=0.8, prof=0.06)
    # la torre del reloj
    tz = H + 0.7
    caja(piedra, 0, 8, tz, 10, 10, 9)
    caja(granito(), 0, 8, tz + 9, 11, 11, 0.6)
    for x, y, giro in ((0, 2.9, 0), (0, 13.1, math.pi), (-5.1, 8, -math.pi / 2), (5.1, 8, math.pi / 2)):
        cil(mat('esfera_reloj', 0xf6f0de, 0.4), x, y, tz + 5.5, 2.0, 0.12, 24, eje='Y' if giro in (0, math.pi) else 'X')
    caja(oscuro(), 0, 2.82, tz + 5.4, 0.12, 0.05, 1.5)                    # las agujas
    caja(oscuro(), 0.55, 2.82, tz + 5.5, 1.1, 0.05, 0.12)
    caja(piedra, 0, 8, tz + 9.6, 7.5, 7.5, 4.5)                          # el campanario
    for x in (-2.2, 0, 2.2):
        caja(oscuro(), x, 4.2, tz + 10.2, 1.2, 0.06, 3.0)
    cupula(cobre(), 0, 8, tz + 14.1, 4.4, 5.5)
    cil(cobre(), 0, 8, tz + 19.4, 0.9, 1.2, 12)
    # John Hancock en lo alto (figura sencilla de bronce)
    estatua = mat('estatua_hancock', 0x6f8f6a, 0.5)
    cil(estatua, 0, 8, tz + 20.6, 0.55, 2.0, 12, r2=0.35)
    esfera(estatua, 0, 8, tz + 23.0, 0.42, 2)
    rama(estatua, (0.3, 8, tz + 22.2), (1.1, 8, tz + 23.4), 0.12, 0.1, 6)
    # banderas en el tejado
    for x in (-18, 18):
        bandera(x, D / 2, H + 6.5, alto=4.5, ancho=1.8)
    # ---- la plaza y el escenario del mitin, delante (hacia -y) ----
    adoquin = mat_bloques('adoquin_plaza', 0xd8cdb8, 0xb9ad96, ancho=1.2, alto=1.2, grosor=0.04, variacion=1.05)
    caja(adoquin, 0, -13, 0, 62, 26, 0.06)
    tarima = mat('tarima', 0x6b4a32, 0.7)
    caja(tarima, 0, -12.5, 0, 14, 7, 1.0)                                 # el escenario (de -9 a -16)
    caja(rojo(), 0, -16.02, 0.1, 14, 0.06, 0.8)                           # faldón
    for k in range(7):
        caja(blanco() if k % 2 else azul(), -6 + k * 2, -16.06, 0.2, 0.6, 0.04, 0.6)
    escalinata(tarima, 0, -16.0, 0, 6, 4, huella=0.6, tabica=0.25)        # escalones hacia el público
    # el atril con micrófonos, a un lado para que se le vea en medio
    caja(mat('atril', 0x3b2a20, 0.6), -3.2, -13.2, 1.0, 1.2, 0.8, 1.3)
    caja(azul(), -3.2, -13.62, 1.5, 1.0, 0.04, 0.6)
    cil(bronce(), -3.2, -13.0, 2.3, 0.03, 0.5, 6)
    # la pancarta del fondo del escenario
    for x in (-6.8, 6.8):
        cil(bronce(), x, -9.4, 1.0, 0.1, 5.2, 8)
    caja(azul(), 0, -9.4, 3.6, 13.4, 0.12, 2.4)
    caja(rojo(), 0, -9.48, 3.6, 13.4, 0.04, 0.35)
    caja(rojo(), 0, -9.48, 5.65, 13.4, 0.04, 0.35)
    texto(blanco(), 'MAKE TACOS', 0, -9.5, 5.0, tam=0.9, prof=0.05)
    texto(blanco(), 'GREAT AGAIN', 0, -9.5, 4.1, tam=0.9, prof=0.05)
    # banderas alrededor del escenario y banderines
    for x in (-10, -8.2, 8.2, 10):
        bandera(x, -10, 0, alto=5.0, ancho=1.6)
    guirnalda(-7, 7, -9.3, 6.3)
    # altavoces a los lados
    for s in (-1, 1):
        caja(oscuro(), s * 8.4, -14.5, 0, 1.4, 1.2, 2.8)
        cil(mat('cono_altavoz', 0x55555c, 0.5), s * 8.4, -15.12, 1.8, 0.45, 0.06, 16, eje='Y')
        cil(mat('cono_altavoz', 0x55555c, 0.5), s * 8.4, -15.12, 0.8, 0.3, 0.06, 16, eje='Y')
    # farolas de la plaza
    for x in (-24, 24):
        for y in (-6, -20):
            cil(mat('poste_fdl', 0x2c3a34, 0.4), x, y, 0, 0.12, 4.2, 8)
            esfera(mat('foco_fdl', 0xfff3c4, 0.2), x, y, 4.5, 0.35, 2)


PIEZAS = {
    'courier':        (courier,        'findlay', dict(lado=1024, segmentos=2)),
    'heladeria':      (heladeria,      'findlay', dict(lado=1024, segmentos=2)),
    'deposito_agua':  (deposito_agua,  'findlay', dict(lado=1024, segmentos=2)),
    'davis':          (davis,          'findlay', dict(lado=1024, segmentos=2)),
    'marathon':       (marathon,       'findlay', dict(lado=1024, segmentos=2)),
    'farola_bandera': (farola_bandera, 'findlay', dict(lado=256, bisel=0.0)),
    'juzgado_final':  (juzgado_final,  'findlay', dict(lado=2048, segmentos=2)),
}

correr(PIEZAS)
