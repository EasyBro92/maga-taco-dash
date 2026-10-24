# Nivel 5: Pennsylvania Avenue, del Capitolio a la Casa Blanca (24/10/2026).
#
#   blender -b -P blender/washington.py -- [pieza ...] [--rapido]
#
# Estilo tipo Pixar (lo eligió Isidro): formas reales con los cantos suaves,
# colores naturales de piedra, ventanas con su marco y su cristal.
#
# Los edificios de la avenida son enormes, así que casi todos se hacen por
# TRAMOS: un trozo de fachada de 20 de ancho, muy detallado, que el nivel
# repite seguido (archivos_ala x N, etc.) y remata con su pieza principal
# (pórtico, torre…). Todas las fachadas en y = 0 mirando a -y; lo que
# sobresale (pórtico, escalinata, plaza) va hacia -y.
#
# Orden real yendo hacia el oeste (lo monta www/src/levels.js):
#   sur (izquierda):  Galería Este · Archivos · Justicia · IRS · Correos (torre)
#                     · Reagan · Wilson · Pershing Park
#   norte (derecha):  Embajada de Canadá · edificio de cristal · Navy Memorial
#                     · FBI · Willard
#   al fondo:         Tesoro · Casa Blanca (con las puertas aparte)

import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import *

# ---------------------------------------------------------------- materiales
def caliza():  return mat_bloques('caliza', 0xe6d9bf, 0xd4c5a8, ancho=1.6, alto=0.55, grosor=0.012, variacion=1.03)
def granito(): return mat_bloques('granito', 0xb7b1a7, 0x9c968b, ancho=1.2, alto=0.6, grosor=0.03, variacion=1.04)
def marmol():  return mat_bloques('marmol_w', 0xf2eee6, 0xe2dccf, ancho=1.8, alto=0.6, grosor=0.01, variacion=1.02)
def liso():    return mat('piedra_lisa', 0xefe7d6, 0.55)
def blanco():  return mat('blanco_cb', 0xfbf9f3, 0.5)
def bronce():  return mat('bronce_marco', 0x3e3a33, 0.4)
def vidrio():  return mat('vidrio', 0x5f86ad, 0.15)
def teja():    return mat_bloques('teja_roja', 0xb65a3e, 0x8f4130, ancho=0.4, alto=0.22, grosor=0.02, variacion=1.08)
def pizarra(): return mat_bloques('pizarra', 0x5c6672, 0x4a535e, ancho=0.45, alto=0.25, grosor=0.015, variacion=1.06)
def oscuro():  return mat('hueco', 0x2b2a2e, 0.8)
def cesped():  return mat('cesped', 0x6fa64c, 0.9)
def agua():    return mat('agua', 0x6fa7c9, 0.1)

def ventanas(xs, z, w, h, remate=None, y=0.0, marco=None):
    for x in xs:
        ventana(x, z, w, h, y=y, marco=marco or bronce(), cristal=vidrio(), remate=remate)

def ventanas_arco(xs, z, w, h, y=0.0, marco=None):
    """Ventana con arco de medio punto (románico)."""
    m = marco or bronce()
    for x in xs:
        ventana(x, z, w, h, y=y, marco=m, cristal=vidrio())
        cil(m, x, y - 0.03, z + h + 0.06, w / 2 + 0.08, 0.08, 20, eje='Y')
        cil(vidrio(), x, y - 0.075, z + h + 0.06, w / 2 - 0.02, 0.02, 20, eje='Y')

def cornisa(W, D, z, h=0.5, vuelo=0.4, m=None):
    caja(m or liso(), 0, D / 2 - vuelo / 2, z, W, D + vuelo, h)

def columnas_grandes(x0, x1, n, y, z, r, h, m=None):
    m = m or liso()
    columnata(m, x0, x1, n, y, z, r, h, basa=m, capitel=m)


# ---------------------------------------------------------------- tramos del sur
def archivos_ala():
    """Archivos Nacionales: tramo con columnas gigantes adosadas."""
    W, H, D = 20, 14, 14
    caja(granito(), 0, D / 2, 0, W, D, 3.5)
    caja(caliza(), 0, D / 2 + 0.3, 3.5, W, D - 0.6, H - 3.5)
    bahias = [-8, -4, 0, 4, 8]
    ventanas(bahias, 1.0, 1.4, 1.8, remate='cornisa')
    ventanas(bahias, 4.8, 1.5, 2.6, y=0.3, remate='fronton')
    ventanas(bahias, 8.6, 1.4, 2.0, y=0.3)
    columnas_grandes(-6, 6, 4, -0.15, 3.5, 0.5, 8.0)
    caja(liso(), 0, D / 2, 11.5, W, D + 0.3, 1.1)                       # entablamento
    caja(liso(), 0, D / 2, 12.6, W, D + 0.6, 0.35)
    caja(caliza(), 0, D / 2 + 0.6, 12.95, W, D - 1.2, 1.4)              # ático
    cornisa(W, D - 1.0, 14.35, 0.3, 0.2)

def archivos_portico():
    """Archivos Nacionales: el gran pórtico corintio con su frontón."""
    W, H, D = 34, 16, 16
    caja(granito(), 0, D / 2, 0, W, D, 3.5)
    caja(caliza(), 0, D / 2 + 0.5, 3.5, W, D - 1, H - 3.5)
    caja(granito(), 0, -1.5, 0, 26, 3.0, 3.5)                           # podio
    escalinata(granito(), 0, -3.0, 0, 18, 10, huella=0.28, tabica=0.35)
    columnas_grandes(-11, 11, 8, -2.2, 3.5, 0.75, 9.5)
    caja(liso(), 0, -1.3, 13.0, 25, 3.4, 1.3)
    fronton(liso(), 0, -3.0, 14.3, 25.5, 3.6, 3.4)
    fronton(mat('timpano', 0xd9cbb0, 0.6), 0, -3.05, 14.6, 21, 2.7, 0.2)
    caja(bronce(), 0, -0.05, 3.5, 3.0, 0.1, 6.0)                         # puertas de bronce
    ventanas([-14.5, 14.5], 4.8, 1.5, 2.6, remate='fronton')
    cornisa(W, D - 1, 16.0, 0.4, 0.2)

def justicia():
    """Departamento de Justicia: caliza art déco, tiras de ventanas y teja roja."""
    W, H, D = 20, 13, 14
    caja(granito(), 0, D / 2, 0, W, D, 1.4)
    caja(caliza(), 0, D / 2, 1.4, W, D, H - 1.4)
    for x in (-8, -4, 0, 4, 8):
        for z in (1.8, 5.2, 8.6):
            ventana(x, z, 1.6, 2.6, marco=mat('aluminio', 0x8f8d86, 0.35), cristal=vidrio())
        for z in (4.6, 8.0):                                             # antepechos de aluminio
            caja(mat('aluminio', 0x8f8d86, 0.35), x, -0.05, z, 1.7, 0.08, 0.5)
    for x in (-10, -6, -2, 2, 6, 10):
        caja(liso(), x, -0.12, 1.4, 0.7, 0.25, H - 2.4)                  # pilastras planas
    caja(mat('banda_deco', 0xcdbd9c, 0.6), 0, -0.05, H - 1.2, W, 0.15, 0.5)
    cornisa(W, D, H, 0.35, 0.3)
    tejado(teja(), 0, 0.5, D - 0.5, H + 0.35, W, 2.4, vuelo=0.3, cumbrera='x')

def irs():
    """Hacienda (IRS): clásico con frontoncillos y teja roja."""
    W, H, D = 20, 13, 14
    caja(mat_bloques('rustico_irs', 0xd6c8ab, 0xb9a988, ancho=1.2, alto=0.5, grosor=0.03), 0, D / 2, 0, W, D, 3.2)
    caja(caliza(), 0, D / 2, 3.2, W, D, H - 3.2)
    bahias = [-8, -4, 0, 4, 8]
    ventanas(bahias, 0.9, 1.5, 1.8)
    ventanas(bahias, 4.0, 1.4, 2.4, remate='fronton')
    ventanas(bahias, 7.6, 1.3, 2.0, remate='cornisa')
    ventanas(bahias, 10.5, 1.1, 1.3)
    caja(liso(), 0, D / 2, 3.1, W, D + 0.3, 0.3)
    cornisa(W, D, H, 0.5, 0.45)
    tejado(teja(), 0, 0.5, D - 0.5, H + 0.5, W, 2.8, vuelo=0.4, cumbrera='x')

def correos_torre():
    """Antiguo edificio de Correos: granito románico y su torre del reloj."""
    W, H, D = 30, 16, 16
    piedra = mat_bloques('granito_rosa', 0xc2ae9c, 0xa39080, ancho=1.0, alto=0.55, grosor=0.03, variacion=1.05)
    caja(piedra, 0, D / 2, 0, W, D, H)
    for x in (-12, -8, 8, 12):
        pass
    ventanas_arco([-12.5, -8.5, 8.5, 12.5], 1.2, 2.0, 2.4)
    ventanas_arco([-12.5, -8.5, 8.5, 12.5], 6.0, 1.6, 2.4)
    ventanas_arco([-12.5, -10.5, -8.5, 8.5, 10.5, 12.5], 10.6, 1.0, 1.8)
    tejado(pizarra(), 0, 0.5, D - 0.5, H, W, 5.0, vuelo=0.4, cumbrera='x')
    # la torre
    T = 9
    caja(piedra, 0, 1.5, 0, T, T, 42)
    ventanas_arco([0], 1.2, 3.2, 4.2, y=-3.0)                            # gran arco de entrada
    for z in (18, 24, 30):
        ventanas_arco([-2.2, 2.2], z, 1.2, 3.0, y=-3.0)
    caja(liso(), 0, 1.5, 36.5, T + 0.6, T + 0.6, 0.6)
    cil(mat('esfera_reloj', 0xf4efe2, 0.4), 0, -3.1, 39.0, 2.4, 0.2, 32, eje='Y')
    cil(bronce(), 0, -3.25, 39.0, 2.55, 0.08, 32, eje='Y')
    caja(bronce(), 0, -3.3, 39.0, 0.18, 0.05, 1.9)                       # agujas
    caja(bronce(), 0.6, -3.3, 39.0, 1.3, 0.05, 0.16)
    for s in (-1, 1):
        for t in (-1, 1):
            cil(piedra, s * (T / 2 - 0.4), 1.5 + t * (T / 2 - 0.4), 42, 0.6, 3.0, 12, r2=0.0)
    cil(pizarra(), 0, 1.5, 42, T * 0.72, 9.0, 4, r2=0.0)                 # chapitel
    cil(bronce(), 0, 1.5, 51, 0.12, 2.0, 8)

def correos():
    W, H, D = 20, 16, 16
    piedra = mat_bloques('granito_rosa', 0xc2ae9c, 0xa39080, ancho=1.0, alto=0.55, grosor=0.03, variacion=1.05)
    caja(piedra, 0, D / 2, 0, W, D, H)
    ventanas_arco([-7.5, -2.5, 2.5, 7.5], 1.2, 2.0, 2.4)
    ventanas_arco([-7.5, -2.5, 2.5, 7.5], 6.0, 1.6, 2.4)
    ventanas_arco([-8.5, -6.5, -3.5, -1.5, 1.5, 3.5, 6.5, 8.5], 10.6, 1.0, 1.8)
    tejado(pizarra(), 0, 0.5, D - 0.5, H, W, 5.0, vuelo=0.4, cumbrera='x')
    for x in (-5, 5):                                                    # buhardillas
        caja(piedra, x, 1.6, H + 0.3, 1.8, 1.4, 2.2)
        fronton(piedra, x, 0.9, H + 2.5, 2.0, 1.0, 1.4)
        ventana(x, H + 0.8, 0.9, 1.3, y=0.9, marco=bronce(), cristal=vidrio())

def reagan():
    """Edificio Reagan: columnata en las plantas altas."""
    W, H, D = 20, 13, 14
    caja(granito(), 0, D / 2, 0, W, D, 3.4)
    caja(caliza(), 0, D / 2 + 0.8, 3.4, W, D - 1.6, H - 3.4)
    ventanas([-8, -4, 0, 4, 8], 1.0, 1.6, 1.8, remate='cornisa')
    ventanas([-8, -4, 0, 4, 8], 4.6, 1.3, 2.2, y=0.8)
    ventanas([-8, -4, 0, 4, 8], 8.0, 1.3, 2.0, y=0.8)
    columnas_grandes(-9, 9, 10, -0.1, 3.4, 0.38, 7.4)
    caja(liso(), 0, D / 2, 10.8, W, D + 0.2, 1.0)
    cornisa(W, D, H - 1.2, 0.5, 0.4)
    tejado(teja(), 0, 0.6, D - 0.6, H - 0.7, W, 2.6, vuelo=0.4, cumbrera='x')

def wilson():
    """Edificio Wilson: Beaux-Arts de mármol blanco con columnas y balaustrada."""
    W, H, D = 40, 15, 16
    caja(mat_bloques('rustico_w', 0xe9e4da, 0xd2cbbd, ancho=1.4, alto=0.55, grosor=0.03), 0, D / 2, 0, W, D, 4)
    caja(marmol(), 0, D / 2 + 0.6, 4, W, D - 1.2, H - 4)
    ventanas_arco([-17, -13, -9, 9, 13, 17], 1.0, 1.6, 2.0, marco=bronce())
    ventanas([-17, -13, -9, 9, 13, 17], 5.0, 1.4, 2.4, y=0.6, remate='fronton')
    ventanas([-17, -13, -9, 9, 13, 17], 9.0, 1.3, 2.2, y=0.6, remate='cornisa')
    caja(marmol(), 0, -0.5, 0, 18, 1.5, 4)                               # cuerpo central adelantado
    escalinata(marmol(), 0, -1.25, 0, 6, 4, huella=0.3, tabica=0.25)
    puerta(0, 1.0, 2.2, 3.0, y=-1.25, color=0x3e3a33)
    columnas_grandes(-7.5, 7.5, 6, -1.6, 4, 0.55, 8.0)
    caja(liso(), 0, 0, 12, 19, 3.0, 1.0)
    cornisa(W, D, H - 2.0, 0.5, 0.4)
    caja(blanco(), 0, 0.2, H - 1.5, W, 0.5, 0.25)                        # balaustrada
    for k in range(48):
        caja(blanco(), -19.5 + k * (39 / 47), 0.2, H - 1.25, 0.2, 0.2, 0.9)
    caja(blanco(), 0, 0.2, H - 0.35, W, 0.55, 0.25)
    for s in (-1, 1):                                                    # grupos escultóricos
        esfera(blanco(), s * 7, 0.6, H + 0.6, 0.8, 2, esc=(1, 0.8, 1.2))

# ---------------------------------------------------------------- tramos del norte
def canada():
    """Embajada de Canadá: piedra clara moderna con la rotonda de columnas."""
    W, H, D = 30, 10, 14
    caja(mat_bloques('piedra_clara', 0xd9d1c2, 0xc4bba9, ancho=2.0, alto=0.8, grosor=0.02), 0, D / 2, 0, W, D, H)
    caja(mat_ventanas('cristal_canada', 0x5f86ad, 0xd9d1c2, paso_x=1.6, paso_z=2.5, hueco_x=1.3, hueco_z=2.0),
         4, -0.05, 2, 18, 0.1, 7)
    x0 = -10
    cil(liso(), x0, -2, 0, 4.2, 0.4, 32)
    for i in range(12):
        a = i / 12 * math.tau
        cil(liso(), x0 + math.cos(a) * 3.8, -2 + math.sin(a) * 3.8, 0.4, 0.3, 8.0, 12)
    cil(liso(), x0, -2, 8.4, 4.3, 0.7, 32)
    for k in range(3):                                                   # banderas de Canadá
        x = 6 + k * 4
        cil(mat('asta', 0xd8d8d8, 0.3), x, -1.2, 0, 0.06, 7.5, 8)
        caja(mat_franjas('bandera_canada', 0xd8283a, 0xffffff, 3, eje='X', z0=x + 0.05, alto=1.8),
             x + 0.95, -1.2, 6.3, 1.8, 0.03, 1.0)

def cristal():
    """Edificio de cristal moderno con la gran losa de mármol (el antiguo Newseum)."""
    W, H, D = 30, 18, 14
    caja(mat_ventanas('cristal_muro', 0x6b93b8, 0xb9c3cc, paso_x=1.5, paso_z=2.4, hueco_x=1.38, hueco_z=2.2, variacion=1.15),
         0, D / 2, 0, W, D, H)
    caja(mat('losa', 0xf0ece4, 0.5), -5, -0.6, 4, 12, 1.0, 13)
    texto(mat('letras_losa', 0x8f8a80, 0.6), 'FREEDOM', -5, -1.12, 12, tam=1.2, prof=0.08)
    caja(mat('marco_gris', 0x8b9198, 0.4), 0, D / 2, H, W + 0.4, D + 0.4, 0.5)
    caja(mat('marquesina', 0x8b9198, 0.4), 6, -1.5, 3.5, 12, 3.0, 0.3)

def navy():
    """Navy Memorial: plaza con fuentes y el marinero, con la columnata detrás."""
    W, H, D = 40, 13, 14
    caja(caliza(), 0, D / 2 + 2, 0, W, D, H)
    columnas_grandes(-18, 18, 16, 1.0, 0, 0.42, 9.5)
    caja(liso(), 0, 1.5, 9.5, W, 2.0, 1.2)
    ventanas([-15, -10, -5, 0, 5, 10, 15], 2.0, 1.5, 2.6, y=2.0)
    ventanas([-15, -10, -5, 0, 5, 10, 15], 6.2, 1.4, 2.2, y=2.0)
    cornisa(W, D, H, 0.5, 0.4)
    # la plaza delante
    caja(mat_bloques('losas_plaza', 0xc9c2b4, 0xb3ab9b, ancho=1.5, alto=1.5, grosor=0.03), 0, -3.5, 0, W, 7, 0.08)
    for s in (-1, 1):
        cil(granito(), s * 9, -3.5, 0, 3.4, 0.6, 32)
        cil(agua(), s * 9, -3.5, 0.55, 3.0, 0.06, 32)
        cil(granito(), s * 9, -3.5, 0.6, 0.4, 1.4, 12)
    cil(granito(), 0, -3.5, 0, 0.8, 1.6, 12)                             # el marinero
    caja(mat('bronce_estatua', 0x5f6b55, 0.4), 0, -3.5, 1.6, 0.5, 0.35, 1.2)
    esfera(mat('bronce_estatua', 0x5f6b55, 0.4), 0, -3.5, 3.0, 0.22, 2)
    for k in range(6):
        x = -15 + k * 6
        cil(mat('asta', 0xd8d8d8, 0.3), x, -6.4, 0, 0.06, 8.0, 8)

def fbi():
    """Edificio Hoover del FBI: hormigón brutalista con ventanas hundidas."""
    W, H, D = 20, 17, 16
    hormigon = mat_bloques('hormigon', 0xc6bfb2, 0xb2ab9d, ancho=3.0, alto=1.2, grosor=0.012, variacion=1.03)
    caja(oscuro(), 0, D / 2 + 2, 0, W, D - 2, 4.2)                        # planta baja hundida
    for x in (-8, -4, 0, 4, 8):
        caja(hormigon, x, 0.6, 0, 1.2, 1.2, 4.2)
    caja(hormigon, 0, D / 2, 4.2, W, D, H - 4.2)
    for k in range(6):                                                   # retícula profunda
        z = 5.0 + k * 1.9
        for i in range(7):
            x = -9 + i * 3
            caja(vidrio(), x, -0.02, z, 2.2, 0.05, 1.3)
        caja(hormigon, 0, -0.45, z - 0.35, W, 0.9, 0.35)
    for i in range(8):
        caja(hormigon, -10.5 + i * 3, -0.45, 4.2, 0.6, 0.9, H - 5.2)
    caja(hormigon, 0, -1.2, H - 2.2, W, 2.4, 2.2)                         # vuelo de arriba
    for i in range(10):
        caja(oscuro(), -9 + i * 2, -2.42, H - 1.7, 1.2, 0.05, 1.2)

def willard():
    """Hotel Willard: Beaux-Arts con mansarda de pizarra y torreón de esquina."""
    W, H, D = 35, 17, 16
    caja(mat_bloques('rustico_wi', 0xd8ccb5, 0xbdae94, ancho=1.2, alto=0.5, grosor=0.03), 0, D / 2, 0, W, D, 3.5)
    caja(mat_bloques('ladrillo_wi', 0xc9a688, 0xe0d2bd, ancho=0.4, alto=0.15, grosor=0.012, mezcla=0.6), 0, D / 2, 3.5, W, D, H - 3.5)
    xs = [-14, -10, -6, -2, 2, 6, 10, 14]
    ventanas_arco(xs[1:-1], 0.6, 1.8, 2.0)
    for z, r in ((4.4, 'fronton'), (7.2, 'cornisa'), (10.0, 'cornisa'), (12.8, None)):
        ventanas(xs, z, 1.2, 1.9, remate=r)
    caja(mat('toldo', 0x2d4a3a, 0.6), 0, -1.2, 3.0, 8, 2.4, 0.3)          # marquesina de la entrada
    for x in (-3.5, 3.5):
        cil(bronce(), x, -2.3, 0, 0.08, 3.0, 8)
    cornisa(W, D, H, 0.6, 0.5)
    tejado(pizarra(), 0, 0.6, D - 0.6, H + 0.6, W, 4.0, vuelo=0.2, cumbrera='x')
    for x in xs:                                                         # ojos de buey en la mansarda
        cil(liso(), x, 0.2, H + 1.9, 0.7, 0.6, 20, eje='Y')
        cil(vidrio(), x, -0.12, H + 1.9, 0.5, 0.05, 20, eje='Y')
    tx = W / 2 - 1                                                       # torreón
    cil(mat_bloques('ladrillo_wi', 0xc9a688, 0xe0d2bd, ancho=0.4, alto=0.15, grosor=0.012, mezcla=0.6), tx, 2.0, 0, 3.0, H + 1, 24)
    cupula(pizarra(), tx, 2.0, H + 1, 3.2, 4.0, lados=24, aros=8)
    cil(bronce(), tx, 2.0, H + 4.9, 0.1, 1.6, 8)
    for k in range(3):
        cil(mat('asta', 0xd8d8d8, 0.3), -6 + k * 6, -0.6, 4.2, 0.05, 3.5, 6)

def galeria_este():
    """Ala Este de la Galería Nacional: mármol rosado de ángulos afilados."""
    W, H, D = 40, 15, 16
    rosa = mat_bloques('marmol_rosa', 0xe6cdb5, 0xd6bca3, ancho=2.4, alto=0.8, grosor=0.008, variacion=1.02)
    caja(rosa, -6, D / 2, 0, 28, D, H)
    me = bpy.data.meshes.new('cuna')                                     # el prisma triangular
    bm = bmesh.new()
    a = [bm.verts.new(p) for p in ((8, 0, 0), (20, 0, 0), (8, D, 0))]
    b = [bm.verts.new((p.co.x, p.co.y, H)) for p in a]
    bm.faces.new(a[::-1]); bm.faces.new(b)
    for i in range(3):
        j = (i + 1) % 3
        bm.faces.new((a[i], a[j], b[j], b[i]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    from comun import _poner
    me2 = bpy.data.meshes.new('cuna'); bm.to_mesh(me2); bm.free()
    o = bpy.data.objects.new('cuna', me2); bpy.context.scene.collection.objects.link(o); _poner(o, rosa)
    caja(oscuro(), -6, -0.05, 0, 12, 0.1, 5.5)                            # entrada en sombra
    caja(vidrio(), -6, -0.07, 0.2, 11, 0.05, 5.0)
    caja(rosa, -6, -0.1, 5.5, 13, 0.3, 0.4)

# ---------------------------------------------------------------- otros
def pershing():
    """Pershing Park: césped, estanque, árboles y la estatua del general."""
    W, D = 40, 16
    caja(cesped(), 0, D / 2 - 4, 0, W, D + 8, 0.08)
    caja(granito(), 0, -1, 0, 18, 8, 0.4)
    caja(agua(), 0, -1, 0.35, 16, 6.6, 0.1)
    caja(granito(), 12, 4, 0, 2.0, 2.0, 2.4)
    caja(mat('bronce_estatua', 0x5f6b55, 0.4), 12, 4, 2.4, 0.7, 0.5, 1.6)
    esfera(mat('bronce_estatua', 0x5f6b55, 0.4), 12, 4, 4.3, 0.28, 2)
    hojas = [mat('hoja1', 0x5e9a46, 0.8), mat('hoja2', 0x4f8a3c, 0.8)]
    for k, (x, y) in enumerate(((-16, 3), (-12, 8), (-5, 9), (4, 8), (16, 2), (-17, -4))):
        cil(mat('tronco', 0x6b4a2f, 0.9), x, y, 0, 0.3, 4.0, 10, r2=0.2)
        for j in range(4):
            esfera(hojas[(k + j) % 2], x + (j - 1.5) * 0.9, y + (j % 2) * 0.8, 5.0 + (j % 3) * 0.7, 1.8 - j * 0.15, 2)

def tesoro():
    """Departamento del Tesoro: la larga columnata jónica al final de la avenida."""
    W, H, D = 60, 15, 18
    caja(granito(), 0, D / 2, 0, W, D, 2.4)
    caja(mat_bloques('granito_claro', 0xd9d6cf, 0xc3c0b7, ancho=1.8, alto=0.6, grosor=0.012), 0, D / 2 + 1.5, 2.4, W, D - 3, H - 2.4)
    ventanas([-26 + k * 4 for k in range(14)], 3.4, 1.3, 2.6, y=1.5, remate='cornisa')
    ventanas([-26 + k * 4 for k in range(14)], 7.6, 1.2, 2.2, y=1.5)
    columnas_grandes(-28, 28, 22, 0.2, 2.4, 0.45, 9.0)
    caja(liso(), 0, D / 2, 11.4, W, D + 0.3, 1.2)
    caja(blanco(), 0, 0.3, 12.6, W, 0.6, 0.25)
    for k in range(70):
        caja(blanco(), -29.5 + k * (59 / 69), 0.3, 12.85, 0.2, 0.2, 0.9)
    caja(blanco(), 0, 0.3, 13.75, W, 0.6, 0.25)
    escalinata(granito(), 0, 0, 0, 30, 6, huella=0.35, tabica=0.4)


# ---------------------------------------------------------------- la Casa Blanca
CB_PORTICO_Y = -7.0      # donde acaba el pórtico (lo usa el juego para la escena final)

def casa_blanca_final():
    """La Casa Blanca vista desde Pennsylvania Avenue (fachada norte), con el
    jardín, la fuente, el camino curvo y la verja. La puerta va aparte."""
    W, H, D = 46, 14, 22
    piedra = mat_bloques('arenisca_blanca', 0xf8f6f0, 0xe7e2d7, ancho=1.4, alto=0.5, grosor=0.008, variacion=1.02)
    caja(piedra, 0, D / 2, 0, W, D, H)
    caja(blanco(), 0, D / 2, H, W + 0.6, D + 0.6, 0.7)                   # cornisa
    caja(blanco(), 0, 0.2, H + 0.7, W + 0.2, 0.6, 0.3)                   # balaustrada
    for k in range(80):
        caja(blanco(), -22.8 + k * (45.6 / 79), 0.2, H + 1.0, 0.2, 0.2, 0.9)
    caja(blanco(), 0, 0.2, H + 1.9, W + 0.2, 0.6, 0.3)
    caja(pizarra(), 0, D / 2 + 1, H + 0.7, W - 4, D - 4, 1.4)
    for x in (-15, -5, 5, 15):                                           # chimeneas
        caja(piedra, x, D / 2, H + 0.7, 1.2, 2.4, 3.2)
    bahias = [-20.5 + k * 4.1 for k in range(11)]
    for i, x in enumerate(bahias):
        if abs(x) < 6:
            continue
        ventana(x, 1.6, 1.6, 3.6, marco=blanco(), cristal=vidrio(), remate='fronton' if i % 2 else 'cornisa',
                persiana=None)
        ventana(x, 7.8, 1.5, 3.2, marco=blanco(), cristal=vidrio(), remate='cornisa')
    # el pórtico norte: columnas jónicas, frontón y el farol
    caja(blanco(), 0, -3.5, 0, 16, 7.0, 1.0)                              # suelo del pórtico
    escalinata(blanco(), 0, -7.0, 0, 9, 4, huella=0.45, tabica=0.25)
    columnas_grandes(-6.6, 6.6, 4, -6.4, 1.0, 0.75, 10.5)
    columnas_grandes(-6.6, 6.6, 4, -3.4, 1.0, 0.7, 10.5)
    caja(blanco(), 0, -3.4, 11.5, 15.5, 7.4, 1.2)
    fronton(blanco(), 0, -7.1, 12.7, 16, 3.0, 7.4)
    fronton(mat('timpano_cb', 0xece8de, 0.6), 0, -7.15, 13.0, 13, 2.2, 0.2)
    cil(bronce(), 0, -3.4, 7.6, 0.04, 3.9, 6)
    cil(mat('farol_cb', 0xffe2a0, 0.2), 0, -3.4, 6.6, 0.45, 1.0, 8, r2=0.35)
    # el hueco de la puerta (las hojas van aparte) con su abanico encima
    caja(oscuro(), 0, -0.02, 1.0, 2.6, 0.06, 4.0)
    caja(blanco(), 0, -0.1, 1.0, 3.2, 0.12, 0.25)
    for s in (-1, 1):
        caja(blanco(), s * 1.5, -0.1, 1.0, 0.25, 0.14, 4.3)
    cil(blanco(), 0, -0.1, 5.3, 1.6, 0.12, 24, eje='Y')
    cil(vidrio(), 0, -0.16, 5.3, 1.35, 0.04, 24, eje='Y')
    caja(piedra, 0, -0.05, 4.6, 3.4, 0.1, 0.7)
    # alas oeste y este, más bajas
    for s in (-1, 1):
        cx = s * (W / 2 + 7)
        caja(piedra, cx, D / 2 + 3, 0, 14, D - 6, 6)
        caja(blanco(), cx, D / 2 + 3, 6, 14.4, D - 5.6, 0.5)
        ventanas([cx - 4.5, cx, cx + 4.5], 1.4, 1.4, 2.6, y=3.0, marco=blanco())
    bandera_y = D / 2
    cil(mat('asta', 0xd8d8d8, 0.3), 0, bandera_y, H + 2.2, 0.1, 6.0, 8)
    caja(mat_franjas('franjas_cb', 0xd8283a, 0xffffff, 7, z0=H + 6.0, alto=1.9), 1.8, bandera_y, H + 6.0, 3.4, 0.05, 1.9)
    caja(mat('azul_bandera', 0x1f3c88), 0.85, bandera_y - 0.04, H + 7.0, 1.5, 0.04, 0.9)
    # el jardín norte: césped, camino curvo hasta el pórtico, fuente y verja
    L = 34
    caja(cesped(), 0, -L / 2 - 2, 0, W + 30, L, 0.06)
    camino = mat('camino_cb', 0xdcd5c6, 0.9)
    caja(camino, 0, -L / 2 - 5, 0, 5, L - 6, 0.09)                        # el camino recto central
    for s in (-1, 1):                                                    # y la curva de coches
        for k in range(14):
            a = k / 13 * math.pi
            x, y = s * (11 * math.sin(a)), -9 - 22 * (k / 13)
            caja(camino, x, y, 0, 3.4, 2.4, 0.08, giro=s * math.cos(a) * 0.9)
    cil(granito(), 0, -22, 0, 4.2, 0.7, 40)                               # la fuente
    cil(agua(), 0, -22, 0.65, 3.8, 0.06, 40)
    cil(granito(), 0, -22, 0.7, 0.5, 1.8, 12)
    cil(agua(), 0, -22, 2.5, 0.9, 0.3, 16, r2=0.3)
    for s in (-1, 1):
        for x in (8, 14, 20):
            esfera(mat('seto', 0x3f7f3a, 0.9), s * x, -1.2, 0.8, 1.0, 2, esc=(1.3, 0.8, 0.8))
    # verja con la puerta abierta en el centro
    yv = -L - 2
    for x in [v * 0.45 for v in range(-60, 61)]:
        if abs(x) < 3.2:
            continue
        caja(oscuro(), x, yv, 0, 0.08, 0.08, 2.3)
        cil(mat("dorado", 0xd4a83a, 0.3), x, yv, 2.3, 0.07, 0.2, 4, r2=0.0)
    for s in (-1, 1):
        caja(oscuro(), s * 15.5, yv, 0.3, 24.6, 0.08, 0.1)
        caja(oscuro(), s * 15.5, yv, 2.0, 24.6, 0.08, 0.1)
        caja(piedra, s * 3.4, yv, 0, 0.9, 0.9, 3.0)                        # pilares de la puerta
        esfera(mat('farol_cb', 0xffe2a0, 0.2), s * 3.4, yv, 3.4, 0.35, 2)

def puerta_cb():
    """Una hoja de la puerta del pórtico norte (el juego pone dos y las cierra)."""
    caja(mat('puerta_madera', 0xf6f2ea, 0.45), 0.65, 0, 0, 1.3, 0.12, 4.0)
    for z in (0.5, 2.2):
        caja(mat('cuarteron', 0xe8e2d5, 0.5), 0.65, -0.07, z, 0.9, 0.04, 1.3)
    esfera(mat('pomo', 0xd4a83a, 0.3), 1.15, -0.12, 2.0, 0.07, 1)


PIEZAS = {
    'archivos_ala':      (archivos_ala,      'washington', dict(lado=1024, segmentos=2)),
    'archivos_portico':  (archivos_portico,  'washington', dict(lado=1024, segmentos=2)),
    'justicia':          (justicia,          'washington', dict(lado=1024, segmentos=2)),
    'irs':               (irs,               'washington', dict(lado=1024, segmentos=2)),
    'correos_torre':     (correos_torre,     'washington', dict(lado=1024, segmentos=2)),
    'correos':           (correos,           'washington', dict(lado=1024, segmentos=2)),
    'reagan':            (reagan,            'washington', dict(lado=1024, segmentos=2)),
    'wilson':            (wilson,            'washington', dict(lado=1024, segmentos=2)),
    'canada':            (canada,            'washington', dict(lado=1024, segmentos=2)),
    'cristal':           (cristal,           'washington', dict(lado=1024, segmentos=2)),
    'navy':              (navy,              'washington', dict(lado=1024, segmentos=2)),
    'fbi':               (fbi,               'washington', dict(lado=1024, segmentos=2)),
    'willard':           (willard,           'washington', dict(lado=1024, segmentos=2)),
    'galeria_este':      (galeria_este,      'washington', dict(lado=1024, segmentos=2)),
    'pershing':          (pershing,          'washington', dict(lado=1024, bisel=0.0)),
    'tesoro':            (tesoro,            'washington', dict(lado=1024, segmentos=2)),
    'casa_blanca_final': (casa_blanca_final, 'washington', dict(lado=2048, segmentos=2, bisel=0.04)),
    'puerta_cb':         (puerta_cb,         'washington', dict(lado=256, segmentos=2, suelo=False)),
}

correr(PIEZAS)
