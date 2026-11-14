# Nivel 20: Nueva Orleans, Luisiana (13/11/2026).
#
#   blender -b -P blender/nuevaorleans.py -- [pieza ...] [--rapido]
#
# Historia: «Carnaval. Ha rebautizado el golfo de México como "golfo de
# América" y los mapas se vuelven locos».
#   Por Bourbon Street (las casas criollas con sus balcones de hierro, el Café
#   du Monde, el Superdome) entre carrozas del Mardi Gras que tiran tacos de
#   oro, se pasa bajo el cartel del «golfo de América» (ahí izquierda y
#   derecha van al revés) y se llega a la catedral de San Luis, en la plaza
#   Jackson.
# Obstáculos (carpeta obstaculos): las carrozas del rey y del bufón (van
# despacio delante de ti), el tranvía de St. Charles, la valla del desfile,
# la rosca de reyes y la pancarta del golfo.

import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import *
from comun import _poner

def blanco():   return mat('blanco_no', 0xf6f2ea, 0.5)
def negro():    return mat('negro_no', 0x1b1c20, 0.4)
def hierro():   return mat('hierro_no', 0x23262a, 0.45)
def morado():   return mat('morado_no', 0x5a2a8a, 0.5)
def verde():    return mat('verde_no', 0x1f8a4a, 0.5)
def oro():      return mat('oro_no', 0xe8b830, 0.25)
def piel():     return mat('piel_no', 0xf0c8a0, 0.6)
def pizarra():  return mat('pizarra_no', 0x3a4048, 0.6)
def helecho():  return mat('helecho_no', 0x3f7a32, 0.85)
def estuco():   return mat_bloques('estuco_no', 0xf4efe4, 0xdcd4c4, ancho=2.2, alto=1.1)

def galeria(x, y, z, w, alto=3.2):
    """Una galería de hierro colado (los balcones del Barrio Francés): el
    suelo, los postes finos, la barandilla con balaustres y helechos colgando."""
    caja(hierro(), x, y - 1, z, w, 2.1, 0.18)
    n = max(2, int(w / 2.2) + 1)
    for i in range(n):
        xx = x - w / 2 + 0.1 + i * (w - 0.2) / (n - 1)
        cil(hierro(), xx, y - 2, z, 0.06, alto, 6)
    caja(hierro(), x, y - 2, z + 1.0, w, 0.06, 0.06)
    caja(hierro(), x, y - 2, z + 0.15, w, 0.06, 0.06)
    for k in range(int(w / 0.3)):
        cil(hierro(), x - w / 2 + 0.15 + k * 0.3, y - 2, z + 0.15, 0.02, 0.85, 4)
    caja(hierro(), x, y - 2, z + alto - 0.15, w, 0.08, 0.15)
    for i in range(n - 1):
        xx = x - w / 2 + 1.2 + i * (w - 0.2) / (n - 1)
        esfera(helecho(), xx, y - 1.9, z + alto - 0.7, 0.42, 1, esc=(1, 1, 0.8))

def collares(x0, x1, y, z, n=10):
    """Collares del carnaval colgando de una barandilla (morado, verde y oro)."""
    cols = (morado(), verde(), oro())
    for k in range(n):
        x = x0 + (x1 - x0) * (k + 0.5) / n
        esfera(cols[k % 3], x, y, z - 0.3 - (k % 3) * 0.12, 0.12, 1)

# ================================================================ edificios
def catedral_sl():
    """La catedral de San Luis (la meta), en la plaza Jackson: fachada blanca,
    las tres agujas de pizarra (la del centro, la más alta, con el reloj),
    los tres portales y, a un lado, la estatua de Andrew Jackson a caballo."""
    Y = 22
    e = estuco()
    caja(e, 0, Y, 0, 34, 40, 15)
    caja(blanco(), 0, Y - 20.2, 15, 34.4, 0.6, 0.8)
    # La torre del centro y su aguja.
    caja(e, 0, Y - 17, 0, 9, 7, 27)
    caja(blanco(), 0, Y - 20.6, 26.6, 9.4, 0.4, 0.6)
    cil(pizarra(), 0, Y - 17, 27.2, 4.2, 15, 4, r2=0.15).rotation_euler = (0, 0, math.pi / 4)
    cil(oro(), 0, Y - 17, 42, 0.12, 2.2, 6)
    caja(oro(), 0, Y - 17, 43.2, 1.2, 0.12, 0.12)
    cil(blanco(), 0, Y - 20.55, 21.5, 1.9, 0.3, 24, eje='Y')
    cil(negro(), 0, Y - 20.75, 21.5, 1.6, 0.1, 24, eje='Y')
    caja(oro(), 0.5, Y - 20.85, 21.6, 1.1, 0.05, 0.12)
    caja(oro(), 0, Y - 20.85, 21.9, 0.12, 0.05, 0.9)
    # Las torres de los lados, con sus agujas de seis lados.
    for s in (-1, 1):
        caja(e, s * 14, Y - 17.5, 0, 6, 6, 20)
        caja(blanco(), s * 14, Y - 20.6, 19.6, 6.4, 0.4, 0.5)
        cil(pizarra(), s * 14, Y - 17.5, 20.1, 3, 8, 6, r2=0.12)
        cil(oro(), s * 14, Y - 17.5, 28, 0.09, 1.4, 6)
    # Los tres portales con columnas pareadas en dos pisos.
    for x in (-8, 0, 8):
        caja(mat('puerta_no', 0x4a2e1e, 0.6), x, Y - 20.3, 0, 2.6, 0.3, 4.6)
        cil(mat('puerta_no', 0x4a2e1e, 0.6), x, Y - 20.3, 4.6, 1.3, 0.3, 16, eje='Y')
        for dx in (-2.2, -1.7, 1.7, 2.2):
            cil(blanco(), x + dx, Y - 20.6, 0, 0.25, 7, 10)
            cil(blanco(), x + dx, Y - 20.6, 7.6, 0.22, 6, 10)
        caja(blanco(), x, Y - 20.6, 7.0, 5.4, 0.6, 0.6)
        ventana(x, 9, 1.6, 3, y=Y - 20.05, marco=blanco(), cristal=mat('vidriera_no', 0x3a5a8a, 0.2))
    fronton(blanco(), 0, Y - 20.6, 15.8, 16, 3, 0.6)
    texto(mat('letras_no', 0x5a4a3a, 0.5), 'ST. LOUIS CATHEDRAL', 0, Y - 20.9, 13.5, tam=0.9, prof=0.04)
    # La estatua de Andrew Jackson a caballo (bronce oscuro), a la izquierda.
    br = mat('bronce_no', 0x3a3a32, 0.35)
    X, YS = -24, -2
    caja(mat('granito_no', 0xb8b0a4, 0.6), X, YS, 0, 4, 6, 3.6)
    esfera(br, X, YS, 6.0, 1.2, 2, esc=(0.8, 1.8, 0.9))           # el cuerpo del caballo, encabritado
    rama(br, (X, YS - 1.4, 6.6), (X, YS - 2.4, 8.4), 0.45, 0.35, 8)   # el cuello
    esfera(br, X, YS - 2.7, 8.7, 0.55, 2, esc=(0.8, 1.4, 0.8))
    for dx in (-0.5, 0.5):
        rama(br, (X + dx, YS + 1.2, 5.4), (X + dx, YS + 1.6, 3.6), 0.22, 0.15, 6)   # patas de atrás, en el suelo
        rama(br, (X + dx, YS - 1.2, 6.0), (X + dx, YS - 2.2, 6.6), 0.2, 0.14, 6)    # las de delante, al aire
    rama(br, (X, YS + 1.6, 6.2), (X, YS + 2.6, 4.6), 0.15, 0.08, 6)                 # la cola
    cil(br, X, YS - 0.2, 7.0, 0.45, 1.6, 8)                                         # el jinete
    esfera(br, X, YS - 0.3, 8.9, 0.3, 2)
    rama(br, (X + 0.3, YS - 0.3, 8.2), (X + 0.5, YS - 1.2, 9.6), 0.1, 0.08, 6)      # saluda con el sombrero
    esfera(br, X + 0.5, YS - 1.3, 9.8, 0.3, 1, esc=(1, 1, 0.5))
    # La verja negra de la plaza y dos palmeras.
    for x in (-30, -18):
        for k in range(12):
            cil(hierro(), x + k * 0.5 if x < -20 else x - k * 0.5, -6, 0, 0.03, 1.6, 4)
    caja(hierro(), -24, -6, 1.5, 12, 0.06, 0.08)
    for x in (-34, 34):
        cil(mat('tronco_no', 0x8a6a4a, 0.8), x, 0, 0, 0.35, 9, 8)
        for k in range(7):
            a = k * math.tau / 7
            rama(helecho(), (x, 0, 9), (x + math.cos(a) * 3.2, math.sin(a) * 3.2, 7.6), 0.35, 0.08, 4)

def casa_criolla():
    """Una casa criolla del Barrio Francés: tres plantas de colores, las dos
    galerías de hierro con helechos, las contraventanas verdes, los faroles de
    gas y las banderas del carnaval."""
    Y = 6
    caja(mat_bloques('estuco_rosa_no', 0xe8a8a0, 0xd89890, ancho=2.5, alto=1.2), 0, Y, 0, 18, 12, 11.5)
    caja(blanco(), 0, Y - 6.1, 11.5, 18.4, 0.6, 0.6)
    for z in (0.4, 4.2, 8.0):
        for x in (-6, -2, 2, 6):
            ventana(x, z + (0 if z else 0), 1.4, 2.8, y=Y - 6, marco=blanco(), cristal=mat('cristal_no', 0x2a3a4a, 0.15),
                    persiana=mat('persiana_no', 0x2f6a3a, 0.6))
    galeria(0, Y - 6, 3.6, 18)
    galeria(0, Y - 6, 7.4, 18, alto=3.4)
    collares(-8.5, 8.5, Y - 8.05, 4.6, 14)
    collares(-8.5, 8.5, Y - 8.05, 8.4, 14)
    # Banderas del carnaval colgando de la galería.
    for (x, m) in ((-5, morado()), (0, verde()), (5, oro())):
        caja(m, x, Y - 8.1, 6.0, 1.2, 0.04, 1.6)
    # Faroles de gas.
    for x in (-8.6, 8.6):
        caja(hierro(), x, Y - 6.2, 2.6, 0.3, 0.4, 0.06)
        caja(luz('gas_no', 0xffc860, 1.2), x, Y - 6.45, 2.0, 0.3, 0.3, 0.55)

def cafe_du_monde():
    """El Café du Monde: la casa baja con el toldo de rayas verdes y blancas,
    el letrero y las mesitas de los buñuelos (beignets)."""
    Y = 7
    caja(blanco(), 0, Y, 0, 20, 12, 4.6)
    caja(mat('tejado_cdm', 0x5a5e62, 0.7), 0, Y, 4.6, 20.4, 12.4, 0.5)
    toldo = mat_franjas('toldo_cdm', 0x2f6a3a, 0xf4f4ee, 26, eje='X', z0=-10.5, alto=21)
    o = caja(toldo, 0, Y - 7.4, 3.0, 21, 3.4, 0.12); o.rotation_euler = (-0.35, 0, 0)
    caja(toldo, 0, Y - 9.05, 2.3, 21, 0.06, 0.6)
    caja(mat('letrero_cdm', 0x2f6a3a, 0.5), 0, Y - 6.4, 5.1, 12, 0.3, 1.4)
    texto(blanco(), 'CAFE DU MONDE', 0, Y - 6.6, 5.4, tam=0.75, prof=0.04)
    texto(mat('letras_cdm2', 0x2f6a3a, 0.5), 'FRENCH MARKET COFFEE STAND', 0, Y - 6.15, 3.4, tam=0.32, prof=0.03)
    for (x, y) in ((-7, -2.2), (-3, -3.2), (1, -2.2), (5, -3.2), (8, -2.0)):
        cil(blanco(), x, Y + y - 4, 0, 0.05, 0.75, 6)
        cil(blanco(), x, Y + y - 4, 0.75, 0.45, 0.05, 12)
        esfera(mat('beignet', 0xf2e6c8, 0.9), x, Y + y - 4, 0.86, 0.12, 1, esc=(1.3, 1, 0.6))
        for a in (0, math.pi):
            cil(mat('silla_cdm', 0x2f6a3a, 0.6), x + math.cos(a) * 0.7, Y + y - 4, 0, 0.18, 0.45, 8)

def superdome():
    """El Superdome: el estadio redondo con su cúpula baja y las franjas."""
    Y = 32
    p = mat('dome_no', 0xe6e0d2, 0.5)
    cil(mat_franjas('dome_franjas', 0xe6e0d2, 0x8a8e94, 16, eje='Z', z0=0, alto=16), 0, Y, 0, 31, 16, 48, r2=27)
    cupula(p, 0, Y, 16, 27, 11, lados=48)
    for k in range(4):
        cil(mat('anillo_dome', 0xc8c2b4, 0.5), 0, Y, 16 + k * 2.6, 26.6 - k * 5.4, 0.3, 48)
    o = texto(oro(), 'SUPERDOME', 0, Y - 29.6, 10.5, tam=3.2, prof=0.15); o.rotation_euler = (math.pi / 2 - 0.25, 0, 0)
    for x in (-14, 14):
        caja(mat('cristal_dome', 0x2a3a4a, 0.2), x, Y - 28.6, 0, 8, 1, 5)

# ================================================================ cruzan la calle
def arco_carnaval():
    """El arco del Mardi Gras sobre la calle (empieza el desfile): dos torres
    a rayas morado, verde y oro, las máscaras gigantes y el cartel."""
    for s in (-1, 1):
        caja(mat_franjas('torre_mg', 0x5a2a8a, 0x1f8a4a, 8, eje='Z', z0=0, alto=9), s * 8.5, 0, 0, 2, 2, 9)
        caja(oro(), s * 8.5, 0, 9, 2.4, 2.4, 0.4)
        # La máscara del carnaval encima.
        esfera(oro(), s * 8.5, 0, 11, 1.6, 2, esc=(1.2, 0.4, 0.8))
        for dx in (-0.6, 0.6):
            esfera(negro(), s * 8.5 + dx, -0.6, 11.2, 0.38, 1, esc=(1.2, 0.4, 0.8))
        for k in range(3):
            o = cil((morado(), verde(), oro())[k], s * 8.5 + (k - 1) * 0.7, 0.2, 11.8, 0.18, 2.6, 6, r2=0.02)
            o.rotation_euler = (0, (k - 1) * 0.45, 0)
    caja(morado(), 0, 0, 7.2, 15, 0.5, 2.2)
    texto(oro(), 'MARDI GRAS', 0, -0.3, 7.6, tam=1.4, prof=0.08)
    texto(verde(), 'PARADE', 0, 0.3, 7.7, tam=1.0, prof=0.08).rotation_euler = (math.pi / 2, 0, math.pi)
    collares(-7, 7, -0.3, 7.2, 22)
    # Guirnaldas de banderines.
    for k in range(20):
        x = -7.5 + k * 0.8
        caja((morado(), verde(), oro())[k % 3], x, 0, 6.2 - 0.6 * math.sin(math.pi * k / 19), 0.5, 0.04, 0.6)

def golfo_america():
    """El cartel gigante del «golfo de América» sobre la calle: el mapa del
    golfo con MÉXICO tachado, y las flechas cambiadas (aquí izquierda y
    derecha van al revés)."""
    for s in (-1, 1):
        cil(hierro(), s * 8, 0, 0, 0.35, 9, 10)
    caja(blanco(), 0, 0, 5.6, 16.5, 0.4, 5.4)
    caja(mat('mar_golfo', 0x3a7ab8, 0.3), 0, -0.22, 6.0, 15.6, 0.05, 4.6)
    esfera(mat('tierra_golfo', 0x9ac078, 0.8), -5.5, -0.22, 9.0, 3.2, 2, esc=(1.4, 0.05, 0.5))
    esfera(mat('tierra_golfo', 0x9ac078, 0.8), 6.0, -0.22, 7.5, 2.4, 2, esc=(1.0, 0.05, 1.3))
    texto(blanco(), 'GULF OF AMERICA', 0, -0.32, 7.6, tam=1.2, prof=0.05)
    texto(mat('tachado', 0xd8323a, 0.4), 'MEXICO', 0, -0.32, 6.4, tam=0.7, prof=0.05)
    caja(mat('tachado', 0xd8323a, 0.4), 0, -0.36, 6.7, 3.6, 0.04, 0.16)
    texto(oro(), '<- RIGHT', -5, -0.32, 6.0, tam=0.55, prof=0.05)
    texto(oro(), 'LEFT ->', 5, -0.32, 6.0, tam=0.55, prof=0.05)

# ================================================================ obstáculos
def _carroza_base(m_falda):
    caja(m_falda, 0, 0, 0.15, 2.1, 4.6, 1.0)
    caja(oro(), 0, 0, 1.15, 2.2, 4.7, 0.12)
    caja(oro(), 0, 0, 0.12, 2.2, 4.7, 0.1)
    for k in range(9):
        esfera(oro(), -1.05, -2.0 + k * 0.5, 0.95, 0.09, 1)
        esfera(oro(), 1.05, -2.0 + k * 0.5, 0.95, 0.09, 1)
    cil(negro(), 0, 0, 0, 0.9, 0.18, 12)

def carroza_rey():
    """La carroza del Rey del carnaval: falda morada con flecos de oro y la
    cabeza enorme del rey con su corona (va despacio delante de ti)."""
    _carroza_base(morado())
    esfera(piel(), 0, -1.0, 2.6, 1.1, 2, esc=(0.95, 0.9, 1.05))
    esfera(mat('barba_rey', 0xf4f0ea, 0.9), 0, -1.6, 2.0, 0.75, 2, esc=(1.1, 0.6, 0.8))
    for dx in (-0.38, 0.38):
        esfera(blanco(), dx, -1.95, 2.85, 0.18, 1)
        esfera(negro(), dx, -2.08, 2.85, 0.08, 1)
    esfera(mat('nariz_rey', 0xe89a80, 0.6), 0, -2.05, 2.55, 0.16, 1)
    cil(oro(), 0, -1.0, 3.45, 0.85, 0.5, 16)
    for k in range(6):
        a = k * math.tau / 6
        cil(oro(), math.cos(a) * 0.75, -1.0 + math.sin(a) * 0.75, 3.9, 0.12, 0.45, 4, r2=0.02)
        esfera(verde() if k % 2 else morado(), math.cos(a) * 0.82, -1.0 + math.sin(a) * 0.82, 3.65, 0.09, 1)
    # Detrás, el trono con las volutas.
    caja(verde(), 0, 1.3, 1.25, 1.8, 1.6, 1.6)
    for s in (-1, 1):
        esfera(oro(), s * 0.9, 1.3, 2.9, 0.4, 2, esc=(0.5, 1, 1))
    texto(oro(), 'REX', 0, -2.36, 0.45, tam=0.45, prof=0.03)

def carroza_bufon():
    """La carroza del bufón: falda verde y la cabeza del bufón con su gorro de
    tres puntas y cascabeles."""
    _carroza_base(verde())
    esfera(piel(), 0, -1.0, 2.5, 1.0, 2)
    for dx in (-0.35, 0.35):
        esfera(blanco(), dx, -1.85, 2.7, 0.17, 1)
        esfera(negro(), dx, -1.98, 2.7, 0.08, 1)
    o = esfera(mat('boca_bufon', 0xc8282c, 0.6), 0, -1.88, 2.2, 0.4, 1, esc=(1.2, 0.3, 0.4))
    for (a, m) in ((-0.9, morado()), (0, oro()), (0.9, verde())):
        rama(m, (0, -1.0, 3.2), (math.sin(a) * 1.4, -1.0, 3.2 + math.cos(a) * 1.3), 0.45, 0.12, 8)
        esfera(oro(), math.sin(a) * 1.5, -1.0, 3.2 + math.cos(a) * 1.4, 0.18, 1)
    caja(morado(), 0, 1.3, 1.25, 1.8, 1.6, 1.4)
    texto(oro(), 'COMUS', 0, -2.36, 0.45, tam=0.4, prof=0.03)

def tranvia_nola():
    """El tranvía verde de St. Charles: verde oliva con ribetes rojos, las
    ventanillas en fila, el trole y el letrero (viene hacia ti)."""
    V = mat('verde_tranvia', 0x3f5a32, 0.5)
    caja(V, 0, 0, 0.5, 2.1, 7.2, 2.4)
    caja(mat('rojo_tranvia', 0x8a2a24, 0.5), 0, 0, 0.45, 2.15, 7.25, 0.25)
    caja(mat('techo_tranvia', 0x5a5e5a, 0.6), 0, 0, 2.9, 2.0, 7.4, 0.35)
    caja(mat('techo_tranvia', 0x5a5e5a, 0.6), 0, 0, 3.25, 1.2, 6.6, 0.25)
    cr = mat('cristal_tranvia', 0xf0d890, 0.2)
    for s in (-1, 1):
        for k in range(9):
            caja(cr, s * 1.06, -3.0 + k * 0.75, 1.6, 0.04, 0.55, 0.9)
    caja(cr, 0, -3.62, 1.6, 1.5, 0.04, 0.9)
    caja(luz('faro_tranvia', 0xfff2c0, 1.2), 0, -3.65, 1.0, 0.35, 0.05, 0.35)
    caja(mat('letrero_tranvia', 0x1b1c20, 0.5), 0, -3.62, 2.65, 1.6, 0.06, 0.3)
    texto(luz('letras_tranvia', 0xffd860, 1.0), 'ST. CHARLES', 0, -3.67, 2.7, tam=0.2, prof=0.02)
    rama(hierro(), (0, 2.0, 3.5), (0, -1.0, 5.0), 0.04, 0.03, 4)
    for y in (-2.5, 2.5):
        caja(hierro(), 0, y, 0.0, 1.6, 1.2, 0.5)

def rosca_reyes():
    """La rosca de reyes del carnaval (King Cake) en su mesa: azúcar morado,
    verde y oro (se salta)."""
    caja(blanco(), 0, 0, 0.55, 1.6, 1.0, 0.08)
    for (x, y) in ((-0.7, -0.4), (0.7, -0.4), (-0.7, 0.4), (0.7, 0.4)):
        cil(mat('pata_mesa', 0x8a6a4a, 0.7), x, y, 0, 0.05, 0.55, 6)
    bpy.ops.mesh.primitive_torus_add(major_radius=0.55, minor_radius=0.2, location=(0, 0, 0.83))
    _poner(bpy.context.object, mat('masa_rosca', 0xd8a868, 0.8))
    for k in range(12):
        a = k * math.tau / 12
        esfera((morado(), verde(), oro())[k % 3], math.cos(a) * 0.55, math.sin(a) * 0.55, 0.98, 0.16, 1, esc=(1, 1, 0.45))

def valla_desfile():
    """La valla metálica de la policía en el desfile (se salta)."""
    for x in (-0.95, 0.95):
        rama(mat('acero_valla', 0xb8bec4, 0.3), (x, -0.4, 0), (x, 0, 1.0), 0.04, 0.04, 6)
        rama(mat('acero_valla', 0xb8bec4, 0.3), (x, 0.4, 0), (x, 0, 1.0), 0.04, 0.04, 6)
    caja(mat('acero_valla', 0xb8bec4, 0.3), 0, 0, 0.95, 2.0, 0.06, 0.06)
    caja(mat('acero_valla', 0xb8bec4, 0.3), 0, 0, 0.3, 2.0, 0.06, 0.06)
    for k in range(10):
        cil(mat('acero_valla', 0xb8bec4, 0.3), -0.9 + k * 0.2, 0, 0.3, 0.02, 0.65, 4)
    caja(mat('azul_nopd', 0x1f3a7a, 0.5), 0, -0.05, 0.5, 0.9, 0.04, 0.3)
    texto(blanco(), 'NOPD', 0, -0.08, 0.55, tam=0.2, prof=0.01)

def cartel_golfo():
    """La pancarta del golfo (agacharse): «GULF OF AMERICA»."""
    for x in (-1.25, 1.25):
        cil(hierro(), x, 0, 0, 0.07, 2.75, 8)
    caja(mat('tela_golfo', 0x3a7ab8, 0.7), 0, 0, 1.55, 2.4, 0.06, 1.05)
    texto(blanco(), 'GULF OF', 0, -0.04, 2.25, tam=0.26, prof=0.02)
    texto(oro(), 'AMERICA', 0, -0.04, 1.86, tam=0.3, prof=0.02)

PIEZAS = {
    'catedral_sl':    (catedral_sl,    'nuevaorleans', dict(lado=2048, segmentos=1, min_bisel=1.0)),
    'casa_criolla':   (casa_criolla,   'nuevaorleans', dict(lado=1024, bisel=0.0)),
    'cafe_du_monde':  (cafe_du_monde,  'nuevaorleans', dict(lado=1024, bisel=0.0)),
    'superdome':      (superdome,      'nuevaorleans', dict(lado=2048, segmentos=1, min_bisel=1.0)),
    'arco_carnaval':  (arco_carnaval,  'nuevaorleans', dict(lado=1024, bisel=0.0, suelo=False)),
    'golfo_america':  (golfo_america,  'nuevaorleans', dict(lado=1024, bisel=0.0, suelo=False)),
    'carroza_rey':    (carroza_rey,    'obstaculos', dict(lado=512, bisel=0.0)),
    'carroza_bufon':  (carroza_bufon,  'obstaculos', dict(lado=512, bisel=0.0)),
    'tranvia_nola':   (tranvia_nola,   'obstaculos', dict(lado=512, bisel=0.0)),
    'rosca_reyes':    (rosca_reyes,    'obstaculos', dict(lado=256, bisel=0.0)),
    'valla_desfile':  (valla_desfile,  'obstaculos', dict(lado=256, bisel=0.0)),
    'cartel_golfo':   (cartel_golfo,   'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
}

correr(PIEZAS)
