# Nivel 33: Salt Lake City, Utah (14/11/2026).
#
#   blender -b -P blender/saltlake.py -- [pieza ...] [--rapido]
#
# Historia: «El desierto de sal: el tramo más rápido de la gira». Acto de la
#   Armada Española. Por State Street en pleno julio (hace tanto calor que en
#   el asfalto hay espejismos), con el ayuntamiento románico y su torre del
#   reloj, la estación de la Union Pacific, la Beehive House con su colmena y
#   el arco del águila (Eagle Gate) cruzando la calle; las colmenas de Utah
#   en las aceras. El momento estrella: el salar de Bonneville, donde se
#   baten los récords de velocidad: montado en el bólido, cambiando de marcha
#   a tiempo. Y se llega al Capitolio de Utah. Pancartas de España:
#   ¡ESCALANTE LLEGÓ PRIMERO! (los frailes Domínguez y Escalante, 1776).
# Obstáculos (carpeta obstaculos): el bloque de sal, la pancarta, el tren
# TRAX, el hot rod del salar, la baliza de las millas y el bólido (se monta:
# es un vehículo).

import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import *

def blanco():    return mat('blanco_slc', 0xf6f4ee, 0.5)
def negro():     return mat('negro_slc', 0x1c1c20, 0.4)
def granito():   return mat_bloques('granito_slc', 0xc4c0b6, 0xa6a298, ancho=1.4, alto=0.7, grosor=0.008, variacion=1.04)
def granito_l(): return mat('granito_liso_slc', 0xd0ccc2, 0.6)
def marmol():    return mat('marmol_slc', 0xeeeae2, 0.4)
def arenisca():  return mat_bloques('arenisca_slc', 0xb89a74, 0x94785a, ancho=0.9, alto=0.45, grosor=0.01, variacion=1.08)
def arenisca_l(): return mat('arenisca_lisa_slc', 0xc8aa84, 0.7)
def ladrillo():  return mat_bloques('ladrillo_slc', 0xa8603e, 0x7a4430, ancho=0.4, alto=0.16)
def pizarra():   return mat('pizarra_slc', 0x4a4e58, 0.55)
def cristal():   return mat('cristal_slc', 0x3a5a70, 0.15)
def rojo():      return mat('rojo_slc', 0xc8202a, 0.45)
def azul():      return mat('azul_slc', 0x2a4a9a, 0.45)
def amarillo():  return mat('amarillo_slc', 0xf2c21a, 0.45)
def oro():       return mat('oro_slc', 0xe8b840, 0.25)
def bronce():    return mat('bronce_slc', 0x5a4a2e, 0.35)
def gris():      return mat('gris_slc', 0x8a9098, 0.4)
def plata():     return mat('plata_slc', 0xc8ccd0, 0.25)
def hierro():    return mat('hierro_slc', 0x2a2c30, 0.45)
def madera_o():  return mat('madera_oscura_slc', 0x5a3a22, 0.85)
def cesped():    return mat('cesped_slc', 0x6a9a48, 0.9)
def copa():      return mat('copa_slc', 0x4a7a3a, 0.85)
def adobe():     return mat('adobe_slc', 0xe8d8b4, 0.85)
def verde_c():   return mat('verde_contra_slc', 0x2a5a3a, 0.5)
def sal():       return mat('sal_slc', 0xf4f2ec, 0.9)
def miel():      return mat('miel_slc', 0xe0a830, 0.45)

def bandera_es(nombre, z0, alto):
    """Las franjas de la bandera de España (roja, amarilla, roja) en z0..z0+alto."""
    return mat_franjas(nombre, 0xc8202a, 0xf2c21a, 3, eje='Z', z0=z0, alto=alto)

def colmena_de(m, x, y, z, r):
    """La colmena de Utah (la de paja, en forma de cúpula, con sus aros)."""
    for k in range(5):
        rr = r * (1.0 - k * 0.16)
        cil(m, x, y, z + k * r * 0.34, rr, r * 0.36, 18, r2=rr * 0.9)
    esfera(m, x, y, z + r * 1.7, r * 0.3, 1)
    caja(negro(), x, y - r * 0.95, z + 0.0, r * 0.4, 0.05, r * 0.3)

def aguila(m, x, y, z, k=1.0):
    """El águila de bronce con las alas abiertas (de frente a -y)."""
    esfera(m, x, y, z, 0.5 * k, 2, esc=(0.75, 0.8, 1.3))
    esfera(m, x, y - 0.35 * k, z + 0.7 * k, 0.27 * k, 1, esc=(0.9, 1.2, 0.9))
    esfera(amarillo(), x, y - 0.7 * k, z + 0.66 * k, 0.08 * k, 1, esc=(1, 1.5, 0.8))
    for s in (-1, 1):
        # Las alas: dos capas de plumas planas, levantadas.
        o = esfera(m, x + s * 1.25 * k, y + 0.05 * k, z + 0.75 * k, 0.5 * k, 2, esc=(2.7, 0.22, 0.95))
        o.rotation_euler = (0, -s * 0.42, 0)
        o = esfera(m, x + s * 1.9 * k, y + 0.08 * k, z + 1.05 * k, 0.5 * k, 2, esc=(2.0, 0.16, 0.7))
        o.rotation_euler = (0, -s * 0.6, 0)
        for i in range(4):
            o = esfera(m, x + s * (2.3 + i * 0.22) * k, y + 0.1 * k, z + (1.55 - i * 0.28) * k, 0.5 * k, 1, esc=(1.1, 0.12, 0.28))
            o.rotation_euler = (0, -s * (0.9 - i * 0.25), 0)

# ================================================================ la meta
def capitolio_utah():
    """El Capitolio de Utah (la meta): el granito gris, la columnata corintia
    a lo largo de toda la fachada, el pórtico con frontón, el tambor alto con
    columnas y la cúpula de cobre con la linterna; la escalinata, el césped,
    una colmena en el jardín, la bandera de Utah y la pancarta
    ¡ESCALANTE LLEGÓ PRIMERO! · 1776."""
    Y = 28
    W, D, H = 72.0, 26.0, 16.0
    yf = Y - D / 2
    g = granito()
    caja(g, 0, Y, 0, W, D, 4.0)
    caja(g, 0, Y + 1.5, 4.0, W - 2, D - 3, H - 4.0)
    caja(granito_l(), 0, Y, H, W + 0.4, D + 0.4, 1.2)
    caja(g, 0, Y, H + 1.2, W - 2, D - 2, 1.4)
    # La columnata de toda la fachada (sobre el zócalo) y las ventanas detrás.
    columnata(marmol(), -33, 33, 24, yf - 0.8, 4.0, 0.55, 12.0)
    for k in range(23):
        x = -31.6 + k * 2.87
        if abs(x) < 8:
            continue
        ventana(x, 5.2, 1.3, 3.4, y=yf + 1.45, marco=granito_l(), cristal=cristal())
        ventana(x, 10.6, 1.2, 2.6, y=yf + 1.45, marco=granito_l(), cristal=cristal())
    for k in range(18):
        ventana(-30 + k * 3.53, 1.0, 1.2, 2.0, y=yf - 0.05, marco=granito_l(), cristal=cristal())
    # El pórtico central adelantado.
    caja(g, 0, yf - 3.5, 0, 18, 7, 4.0)
    columnata(marmol(), -7, 7, 8, yf - 6.2, 4.0, 0.7, 12.0)
    caja(granito_l(), 0, yf - 4.5, H, 18, 9, 1.4)
    fronton(granito_l(), 0, yf - 5.6, H + 1.4, 18, 4.0, 6.0)
    puerta(0, 4.0, 2.8, 5.0, y=yf + 1.4, color=0x5a3a22, marco=granito_l())
    for k in range(14):
        caja(granito_l(), 0, yf - 7.8 - k * 0.5, 0, 22 + k * 0.7, 0.5, 4.0 - k * 0.28)
    # El tambor, la cúpula de cobre y la linterna.
    Z = H + 2.6
    cil(g, 0, Y, Z, 10.2, 3.6, 36)
    cil(granito_l(), 0, Y, Z + 3.6, 10.6, 0.7, 36)
    cil(granito_l(), 0, Y, Z + 4.3, 8.6, 9.0, 36)
    for k in range(24):
        a = k * math.tau / 24
        cil(marmol(), math.cos(a) * 9.0, Y + math.sin(a) * 9.0, Z + 4.3, 0.36, 9.0, 10)
    for k in range(12):
        a = k * math.tau / 12 + 0.13
        cil(cristal(), math.cos(a) * 8.65, Y + math.sin(a) * 8.65, Z + 5.6, 0.8, 5.0, 8)
    cil(granito_l(), 0, Y, Z + 13.3, 9.6, 1.1, 36)
    cu = mat('cobre_slc', 0x9aaa9a, 0.4)
    cupula(cu, 0, Y, Z + 14.4, 8.6, 10.0, 36, 10)
    for k in range(16):
        a = k * math.tau / 16
        rama(mat('nervio_slc', 0x8a9a8a, 0.4), (math.cos(a) * 8.6, Y + math.sin(a) * 8.6, Z + 14.5),
             (math.cos(a) * 1.8, Y + math.sin(a) * 1.8, Z + 24.1), 0.14, 0.08, 4)
    cil(granito_l(), 0, Y, Z + 24.1, 2.1, 3.6, 12)
    for k in range(8):
        a = k * math.tau / 8
        cil(marmol(), math.cos(a) * 2.15, Y + math.sin(a) * 2.15, Z + 24.1, 0.15, 3.6, 6)
    cupula(cu, 0, Y, Z + 27.7, 2.2, 2.0, 12, 4)
    cil(oro(), 0, Y, Z + 29.6, 0.15, 1.8, 6)
    esfera(oro(), 0, Y, Z + 31.5, 0.35, 1)
    # El césped, los árboles, la colmena del jardín, la bandera y la pancarta.
    caja(cesped(), 0, yf - 22, -0.05, 96, 28, 0.06)
    for (x, y) in ((-34, yf - 11), (-40, yf - 22), (34, yf - 11), (40, yf - 22), (-46, yf + 2), (46, yf + 2)):
        cil(madera_o(), x, y, 0, 0.35, 3.2, 8)
        esfera(copa(), x, y, 5.2, 3.2, 2, esc=(1, 1, 1.15))
    caja(mat('pedestal_slc', 0x9a9488, 0.6), -13, yf - 17, 0, 2.6, 2.6, 1.4)
    colmena_de(miel(), -13, yf - 17, 1.4, 1.0)
    cil(gris(), -23, yf - 15, 0, 0.13, 13, 8)
    caja(mat('bandera_ut_slc', 0x1e3a7a, 0.6), -21.2, yf - 15, 10.6, 3.6, 0.06, 2.4)
    colmena_de(oro(), -21.2, yf - 15.1, 11.1, 0.45)
    for x in (9.5, 21.5):
        cil(madera_o(), x, yf - 16, 0, 0.12, 4.4, 8)
    caja(bandera_es('pancarta_es_capitolio_slc', 2.8, 1.6), 15.5, yf - 16, 2.8, 12, 0.06, 1.6)
    texto(negro(), '¡ESCALANTE LLEGÓ PRIMERO!', 15.5, yf - 16.04, 3.75, tam=0.58, prof=0.03)
    texto(blanco(), '1776', 15.5, yf - 16.04, 3.0, tam=0.5, prof=0.03)

# ================================================================ edificios
def city_county_slc():
    """El ayuntamiento de Salt Lake City (City and County Building, 1894):
    arenisca románica, los arcos, las torrecillas de las esquinas con tejado
    de cono y la torre del reloj en el centro con la estatua encima."""
    Y = 10
    W, D, H = 40.0, 16.0, 14.0
    yf = Y - D / 2
    a = arenisca()
    caja(a, 0, Y, 0, W, D, H)
    caja(arenisca_l(), 0, Y, H, W + 0.4, D + 0.4, 0.8)
    tejado(pizarra(), 0, Y - D / 2, Y + D / 2, H + 0.8, W, 4.0, cumbrera='x')
    for k in range(9):
        x = -17 + k * 4.25
        if abs(x) < 4:
            continue
        for (z, h) in ((1.0, 3.0), (5.6, 2.8), (10.0, 2.4)):
            ventana(x, z, 1.5, h, y=yf - 0.05, marco=arenisca_l(), cristal=cristal())
            cil(arenisca_l(), x, yf - 0.08, z + h, 0.85, 0.12, 12, eje='Y').scale = (1, 1, 0.7)
    for s in (-1, 1):
        cil(a, s * 19.2, yf + 0.6, 0, 2.2, H + 3.0, 16)
        cil(pizarra(), s * 19.2, yf + 0.6, H + 3.0, 2.5, 4.5, 16, r2=0.1)
    # La entrada de arcos y la torre del reloj.
    for x in (-2.4, 0, 2.4):
        cil(arenisca_l(), x, yf - 0.1, 3.6, 1.05, 0.2, 14, eje='Y')
        caja(madera_o(), x, yf - 0.12, 0, 1.8, 0.1, 3.6)
    T = 7.0
    caja(a, 0, yf + 2.5, 0, T, T, 34)
    for z in (H, 22, 28.5):
        caja(arenisca_l(), 0, yf + 2.5, z, T + 0.4, T + 0.4, 0.7)
    for (dx, dy, rx) in ((0, -1, 0), (-1, 0, 1), (1, 0, 1)):
        x, y = dx * (T / 2 + 0.1), yf + 2.5 + dy * (T / 2 + 0.1)
        o = cil(blanco(), x, y, 25.2, 2.0, 0.15, 24, eje='Y')
        if rx:
            o.rotation_euler = (math.pi / 2, 0, math.pi / 2)
        if dy == -1:
            caja(negro(), x, y - 0.12, 25.2, 0.12, 0.04, 1.5)
            caja(negro(), x + 0.45, y - 0.12, 25.2, 1.0, 0.04, 0.12)
    for x in (-1.6, 1.6):
        caja(cristal(), x, yf + 2.5 - T / 2 - 0.05, 29.5, 1.2, 0.1, 3.0)
    o = cil(pizarra(), 0, yf + 2.5, 34, T * 0.74, 5.0, 4, r2=0.5)
    o.rotation_euler = (0, 0, math.pi / 4)
    cil(arenisca_l(), 0, yf + 2.5, 39, 0.7, 1.2, 10)
    cil(mat('estatua_slc', 0x7a8a7a, 0.4), 0, yf + 2.5, 40.2, 0.35, 2.2, 8, r2=0.2)
    esfera(mat('estatua_slc', 0x7a8a7a, 0.4), 0, yf + 2.5, 42.6, 0.28, 1)

def depot_slc():
    """La estación de la Union Pacific de Salt Lake (1909): estilo Segundo
    Imperio, la mansarda de pizarra, las dos torres delanteras con su
    tejado alto, el gran ventanal de arco en el centro y el letrero."""
    Y = 10
    W, D, H = 44.0, 16.0, 11.0
    yf = Y - D / 2
    l = ladrillo()
    p = mat_bloques('piedra_dep_slc', 0xd8cdb4, 0xb8ad94, ancho=1.0, alto=0.5, grosor=0.008)
    caja(l, 0, Y, 0, W, D, H)
    caja(p, 0, Y, 0, W + 0.2, D + 0.2, 1.4)
    caja(p, 0, Y, H, W + 0.4, D + 0.4, 0.6)
    caja(pizarra(), 0, Y, H + 0.6, W - 1, D - 1, 3.6)
    for k in range(10):
        x = -19.5 + k * 4.33
        caja(p, x, yf + 0.45, H + 1.2, 1.4, 1.0, 2.0)
        caja(cristal(), x, yf - 0.06, H + 1.5, 0.9, 0.05, 1.3)
        if abs(x) > 6:
            ventana(x, 2.4, 1.5, 3.4, y=yf - 0.05, marco=p, cristal=cristal())
            ventana(x, 7.2, 1.4, 2.6, y=yf - 0.05, marco=p, cristal=cristal())
    # El ventanal central.
    caja(p, 0, yf - 0.03, 1.2, 8.8, 0.1, 4.8)
    esfera(p, 0, yf - 0.03, 6.0, 4.4, 2, esc=(1, 0.02, 1), mitad=True)
    caja(cristal(), 0, yf - 0.07, 1.4, 8, 0.1, 4.6)
    esfera(cristal(), 0, yf - 0.07, 6.0, 4.0, 2, esc=(1, 0.02, 1), mitad=True)
    for x in (-2, 0, 2):
        caja(p, x, yf - 0.1, 1.4, 0.15, 0.05, 4.6 + (3.9 if x == 0 else 3.4))
    # Las torres con su mansarda alta.
    for s in (-1, 1):
        x = s * 9.5
        caja(l, x, yf - 0.5, 0, 6, 6, H + 4)
        caja(p, x, yf - 0.5, H + 4, 6.4, 6.4, 0.5)
        o = cil(pizarra(), x, yf - 0.5, H + 4.5, 4.2, 5.0, 4, r2=2.4)
        o.rotation_euler = (0, 0, math.pi / 4)
        caja(hierro(), x, yf - 0.5, H + 9.5, 3.0, 3.0, 0.3)
        for dz in (2.6, 7.4, 12.0):
            ventana(x, dz, 1.4, 2.6, y=yf - 3.55, marco=p, cristal=cristal())
    caja(mat('letrero_dep_slc', 0x2a3a5a, 0.5), 0, yf - 0.4, 12.0, 14, 0.15, 1.2)
    texto(blanco(), 'UNION PACIFIC', 0, yf - 0.5, 12.6, tam=0.9, prof=0.04)

def beehive_house():
    """La Beehive House (1854): dos pisos de adobe claro, las galerías de
    columnas blancas en los dos pisos, las contraventanas verdes y la
    linterna de arriba con la colmena dorada."""
    Y = 8
    W, D, H = 22.0, 12.0, 8.0
    yf = Y - D / 2
    a = adobe()
    caja(a, 0, Y, 0, W, D, H)
    tejado(mat('tejado_bh_slc', 0x5a5248, 0.6), 0, Y - D / 2, Y + D / 2, H, W, 2.6, cumbrera='x')
    for x in (-8, -4, 4, 8):
        for z in (0.9, 4.9):
            ventana(x, z, 1.2, 2.0, y=yf - 0.05, marco=blanco(), cristal=cristal())
            for s in (-1, 1):
                caja(verde_c(), x + s * 0.9, yf - 0.08, z, 0.5, 0.06, 2.0)
    puerta(0, 0, 1.4, 2.6, y=yf - 0.05, color=0x2a5a3a, marco=blanco())
    # Las galerías.
    for z in (0, 4.0):
        caja(blanco(), 0, yf - 1.4, z + 3.7, W - 1, 2.8, 0.2)
        for k in range(8):
            cil(blanco(), -9.8 + k * 2.8, yf - 2.6, z, 0.14, 3.7, 8)
    for k in range(20):
        caja(blanco(), -9.6 + k * 1.0, yf - 2.7, 4.0, 0.06, 0.06, 0.9)
    caja(blanco(), 0, yf - 2.7, 4.9, W - 1.5, 0.1, 0.1)
    # La linterna con la colmena.
    caja(a, 0, Y, H + 2.6, 3.0, 3.0, 2.2)
    for x in (-0.8, 0.8):
        caja(cristal(), x, Y - 1.55, H + 3.0, 0.6, 0.05, 1.2)
    caja(blanco(), 0, Y, H + 4.8, 3.4, 3.4, 0.25)
    colmena_de(oro(), 0, Y, H + 5.05, 0.9)
    caja(mat('placa_bh_slc', 0x2a5a3a, 0.5), 0, yf - 0.06, 3.0, 4.4, 0.08, 0.6)
    texto(oro(), 'BEEHIVE HOUSE', 0, yf - 0.11, 3.18, tam=0.32, prof=0.02)

def colmena():
    """La colmena de Utah sobre su peana, con INDUSTRY (para la acera)."""
    caja(granito_l(), 0, 0, 0, 1.1, 1.1, 0.9)
    texto(negro(), 'INDUSTRY', 0, -0.56, 0.4, tam=0.15, prof=0.02)
    colmena_de(miel(), 0, 0, 0.9, 0.62)
    for (x, z) in ((0.5, 1.9), (-0.45, 1.6), (0.3, 2.3)):
        esfera(amarillo(), x, -0.4, z, 0.06, 1, esc=(1.4, 1, 1))
        esfera(negro(), x + 0.04, -0.42, z, 0.035, 1)

# ================================================================ cruzan la calle
def eagle_gate():
    """El arco del águila (Eagle Gate) cruzando State Street: los dos
    pilares de piedra, el arco de hierro con la colmena en el centro y, encima,
    el águila de bronce con las alas abiertas."""
    p = granito_l()
    for s in (-1, 1):
        caja(p, s * 8.8, 0, 0, 1.6, 1.6, 6.0)
        caja(granito(), s * 8.8, 0, 6.0, 1.9, 1.9, 0.5)
    n = 36
    for k in range(n):
        u0, u1 = k / n, (k + 1) / n
        p0 = (-8.4 + 16.8 * u0, 0, 6.4 + 2.6 * math.sin(math.pi * u0))
        p1 = (-8.4 + 16.8 * u1, 0, 6.4 + 2.6 * math.sin(math.pi * u1))
        rama(bronce(), p0, p1, 0.26, 0.26, 8)
    colmena_de(bronce(), 0, 0, 8.6, 0.9)
    aguila(bronce(), 0, 0, 11.2, 1.7)
    for s in (-1, 1):
        cil(hierro(), s * 4.5, 0, 6.6, 0.05, 1.5, 6)

# ================================================================ el salar
def salar_bonneville():
    """El salar de Bonneville (momento estrella, al aire libre): la sal
    blanca con sus grietas, la línea negra del recorrido, las balizas de las
    millas a los lados, las luces del cronometraje, los equipos con sus
    carpas y remolques, los montes Silver Island a lo lejos y los arcos de
    SALIDA y META de BONNEVILLE SPEEDWAY. Cruza la calle: el origen en el
    centro y la calle a lo largo de y."""
    L = 420
    caja(mat_bloques('sal_grietas_slc', 0xf4f2ec, 0xd8d4c8, ancho=2.6, alto=2.2, grosor=0.012, variacion=1.03), 0, 0, -0.2, 120, L, 0.2)
    caja(negro(), 0, 0, -0.005, 0.35, L, 0.01)
    for s in (-1, 1):
        caja(negro(), s * 4.4, 0, -0.005, 0.12, L, 0.01)
    # Los montes Silver Island, lejos a los dos lados.
    for s in (-1, 1):
        for k in range(9):
            y = -L / 2 + 20 + k * 48
            h = 14 + (k * 7 % 9) * 2.2
            o = cil(mat('monte_slc', 0x8a6a5a, 0.9), s * (52 + (k % 3) * 6), y, 0, 18, h, 6, r2=3)
            o.scale = (0.6, 1.6, 1)
    # Las balizas de las millas y las luces del cronometraje.
    for k in range(int(L / 70)):
        y = -L / 2 + 35 + k * 70
        for s in (-1, 1):
            cil(hierro(), s * 7.5, y, 0, 0.08, 3.2, 6)
            caja(blanco(), s * 7.5, y, 2.4, 1.6, 0.1, 1.0)
            texto(negro(), f'MILE {k + 1}', s * 7.5, y - 0.07, 2.72, tam=0.32, prof=0.02)
            caja(negro(), s * 7.5, y, 1.2, 0.4, 0.4, 0.8)
            esfera(luz('luz_crono_slc', 0x40ff60, 1.4), s * 7.5, y - 0.22, 1.6, 0.12, 1)
    # Los equipos: carpas, remolques, banderas y algo de público.
    for k in range(int(L / 40)):
        y = -L / 2 + 20 + k * 40
        s = 1 if k % 2 else -1
        x = s * 16
        caja(mat(f'carpa_slc{k % 3}', [0xc8202a, 0x2a4a9a, 0xf2c21a][k % 3], 0.6), x, y, 2.6, 5, 5, 0.2)
        for dx in (-2.3, 2.3):
            for dy in (-2.3, 2.3):
                cil(gris(), x + dx, y + dy, 0, 0.05, 2.6, 4)
        caja(blanco(), x + s * 6, y + 3, 0, 2.4, 7, 2.6)
        caja(mat('rayas_rem_slc', 0x2a4a9a, 0.5), x + s * 6, y + 3, 1.2, 2.45, 7.05, 0.3)
        for i in range(4):
            cil(mat(f'camisa_slc{i}', [0xc8282c, 0x2a5aa8, 0xf4f0e8, 0xf0c020][i], 0.8), x - s * 2.5, y - 1.5 + i * 1.1, 0, 0.25, 1.4, 6)
            esfera(mat('cara_slc', 0xe8b89a, 0.7), x - s * 2.5, y - 1.5 + i * 1.1, 1.6, 0.2, 1)
        cil(gris(), x - s * 3.5, y + 4, 0, 0.05, 5.0, 4)
        caja(mat_franjas('cuadros_slc', 0x1c1c20, 0xf6f4ee, 6, eje='Z', z0=4.0, alto=1.0), x - s * 3.5 + 0.7, y + 4, 4.0, 1.4, 0.04, 1.0)
    # La torre del cronometraje.
    for y in (-60, 120):
        caja(blanco(), -24, y, 0, 4, 4, 8)
        caja(cristal(), -24, y - 2.05, 5.4, 3.4, 0.1, 2.0)
        caja(rojo(), -24, y, 8, 4.4, 4.4, 0.4)
        texto(rojo(), 'TIMING', -24, y - 2.06, 4.4, tam=0.5, prof=0.02)
    for (y, txt) in ((-L / 2 + 1, 'SALIDA'), (L / 2 - 1, 'META')):
        for s in (-1, 1):
            cil(hierro(), s * 7.2, y, 0, 0.25, 6.4, 8)
        cil(hierro(), 0, y, 6.0, 0.22, 14.8, 8, eje='X')
        caja(blanco(), 0, y, 4.0, 9.0, 0.16, 1.6)
        texto(rojo(), 'BONNEVILLE SPEEDWAY', 0, y - 0.1, 4.9, tam=0.52, prof=0.04)
        texto(negro(), txt, 0, y - 0.1, 4.25, tam=0.45, prof=0.04)

# ================================================================ obstáculos
def bloque_sal():
    """Los bloques de sal apilados (se saltan)."""
    s = mat_bloques('sal_bloque_slc', 0xf2efe6, 0xc8c2b0, ancho=0.5, alto=0.25, grosor=0.012, variacion=1.04)
    caja(s, 0, 0, 0, 1.9, 0.6, 0.5)
    caja(s, 0.1, 0, 0.5, 1.3, 0.55, 0.25)
    caja(azul(), 0, -0.31, 0.15, 0.7, 0.02, 0.2)
    texto(blanco(), 'SALT', 0, -0.32, 0.18, tam=0.12, prof=0.01)

def cartel_utah():
    """La pancarta de España (agacharse): ¡ESCALANTE LLEGÓ PRIMERO! · 1776."""
    for x in (-1.25, 1.25):
        cil(madera_o(), x, 0, 0, 0.07, 2.75, 8)
    caja(bandera_es('pancarta_es_obst_slc', 1.5, 1.2), 0, 0, 1.5, 2.4, 0.05, 1.2)
    texto(negro(), '¡ESCALANTE', 0, -0.035, 2.25, tam=0.24, prof=0.02)
    texto(negro(), 'LLEGÓ PRIMERO!', 0, -0.035, 1.95, tam=0.19, prof=0.02)
    texto(blanco(), '1776', 0, -0.035, 1.6, tam=0.2, prof=0.02)

def trax():
    """El tren ligero TRAX (no se pasa): plateado con la franja azul y roja,
    la cabina mirando al jugador y el pantógrafo. El morro en el origen."""
    pl = plata()
    caja(pl, 0, 4.6, 0.35, 2.6, 8.6, 2.9)
    caja(pl, 0, 0.5, 0.35, 2.6, 1.2, 2.6)
    caja(cristal(), 0, 0.0, 1.6, 2.3, 0.1, 1.1)
    for y in (1.6, 4.0, 6.4, 8.2):
        for s in (-1, 1):
            caja(cristal(), s * 1.31, y, 1.6, 0.05, 1.6, 1.0)
    for s in (-1, 1):
        caja(azul(), s * 1.31, 4.6, 0.9, 0.06, 8.6, 0.3)
        caja(rojo(), s * 1.31, 4.6, 1.2, 0.06, 8.6, 0.12)
    caja(azul(), 0, -0.05, 0.9, 2.6, 0.06, 0.3)
    caja(rojo(), 0, -0.06, 1.2, 2.6, 0.06, 0.12)
    caja(negro(), 0, -0.07, 2.75, 1.6, 0.05, 0.3)
    texto(amarillo(), 'TRAX', 0, -0.1, 2.8, tam=0.2, prof=0.01)
    for s in (-1, 1):
        caja(luz('faro_trax_slc', 0xfff2c0, 1.0), s * 0.95, -0.06, 0.55, 0.35, 0.05, 0.2)
    caja(hierro(), 0, 4.6, 0, 2.2, 8.6, 0.35)
    rama(hierro(), (0, 4.0, 3.25), (0, 5.0, 4.1), 0.04, 0.04, 4)
    caja(hierro(), 0, 5.0, 4.1, 1.4, 0.1, 0.06)

def hot_rod():
    """El hot rod de las carreras del salar (no se pasa): el morro largo y
    estrecho, las ruedas al aire, el motor con los tubos cromados, el número
    y la cabina baja. El morro en el origen."""
    r = mat('hotrod_slc', 0xd83a1a, 0.3)
    caja(r, 0, 1.6, 0.35, 0.9, 3.0, 0.6)
    cil(r, 0, 0.2, 0.62, 0.42, 0.6, 14, eje='Y', r2=0.1).scale = (1, 1, 0.65)
    caja(r, 0, 3.6, 0.35, 1.3, 1.6, 0.9)
    caja(negro(), 0, 3.3, 1.25, 1.0, 0.5, 0.5)
    caja(cristal(), 0, 3.05, 1.35, 0.95, 0.05, 0.35)
    for (y, rr) in ((0.9, 0.36), (3.9, 0.45)):
        for s in (-1, 1):
            cil(negro(), s * 0.85, y, rr, rr, 0.35, 16, eje='X')
            cil(plata(), s * 0.86, y, rr, rr * 0.5, 0.37, 12, eje='X')
    for s in (-1, 1):
        for k in range(3):
            rama(plata(), (s * 0.45, 1.8 + k * 0.35, 0.85), (s * 0.7, 2.0 + k * 0.35, 0.55), 0.05, 0.05, 6)
    cil(blanco(), 0, 2.6, 0.97, 0.3, 0.02, 16).scale = (1, 1, 1)
    texto(negro(), '270', 0, 2.6, 0.99, tam=0.26, prof=0.01).rotation_euler = (0, 0, 0)
    caja(blanco(), 0, -0.01, 0.6, 0.5, 0.02, 0.2)
    texto(negro(), '270', 0, -0.02, 0.63, tam=0.14, prof=0.01)

def baliza_sal():
    """La baliza de las millas del salar (se salta): el poste negro y
    blanco a franjas, bajo, con la banderita naranja."""
    cil(mat_franjas('baliza_franjas_slc', 0x1c1c20, 0xf6f4ee, 4, eje='Z', z0=0, alto=0.75), 0, 0, 0, 0.12, 0.75, 10)
    caja(negro(), 0, 0, 0, 0.5, 0.5, 0.06)
    caja(mat('banderita_slc', 0xf28a1a, 0.5), 0.22, 0, 0.5, 0.4, 0.02, 0.24)

def bolido_sal():
    """El bólido del récord de velocidad (un vehículo: se va de pie encima):
    un puro largo rojo, blanco y azul, con el morro afilado, la cabina de
    cristal, la aleta de cola, el paracaídas y el número 270. El morro mira al
    jugador (-y); el juego le da la vuelta al montarlo."""
    b = blanco()
    L = 8.0
    cil(b, 0, L * 0.55, 0.62, 0.62, L * 0.7, 20, eje='Y')
    cil(rojo(), 0, 0.85, 0.62, 0.62, 1.7, 20, eje='Y', r2=0.05)
    cil(azul(), 0, L - 0.3, 0.62, 0.55, 0.6, 20, eje='Y')
    for s in (-1, 1):
        caja(rojo(), s * 0.6, L * 0.55, 0.55, 0.06, L * 0.68, 0.18)
        caja(azul(), s * 0.6, L * 0.55, 0.8, 0.06, L * 0.68, 0.1)
    # La aleta de cola y los estabilizadores.
    caja(azul(), 0, L - 0.6, 1.1, 0.08, 1.4, 1.5, inclina=0.0)
    caja(rojo(), 0, L - 0.4, 2.4, 0.1, 1.0, 0.2)
    for s in (-1, 1):
        caja(azul(), s * 0.9, L - 0.5, 0.55, 0.9, 0.8, 0.06)
    # La cabina de cristal (delante de donde va de pie).
    esfera(cristal(), 0, 3.2, 1.12, 0.38, 2, esc=(1.0, 2.2, 0.8))
    # El número, la estrella y el paracaídas plegado.
    for s in (-1, 1):
        cil(blanco(), s * 0.63, 2.4, 0.62, 0.32, 0.02, 16, eje='X')
        texto(negro(), '270', s * 0.65, 2.4, 0.5, tam=0.22, prof=0.01).rotation_euler = (math.pi / 2, 0, -s * math.pi / 2)
    cil(rojo(), 0, L + 0.2, 0.62, 0.22, 0.4, 12, eje='Y')
    cil(mat('rueda_bol_slc', 0x2a2a2e, 0.5), 0, 1.6, 0.05, 0.08, 0.1, 8)
    caja(mat('suelo_bol_slc', 0x2a2a2e, 0.5), 0, L * 0.55, 0.0, 0.7, L * 0.6, 0.06)

PIEZAS = {
    'capitolio_utah':   (capitolio_utah,   'saltlake',   dict(lado=2048, bisel=0.0)),
    'city_county_slc':  (city_county_slc,  'saltlake',   dict(lado=1024, bisel=0.0)),
    'depot_slc':        (depot_slc,        'saltlake',   dict(lado=1024, bisel=0.0)),
    'beehive_house':    (beehive_house,    'saltlake',   dict(lado=1024, bisel=0.0)),
    'colmena':          (colmena,          'saltlake',   dict(lado=256, bisel=0.0)),
    'eagle_gate':       (eagle_gate,       'saltlake',   dict(lado=1024, bisel=0.0, suelo=False)),
    'salar_bonneville': (salar_bonneville, 'saltlake',   dict(lado=2048, bisel=0.0, suelo=False)),
    'bloque_sal':       (bloque_sal,       'obstaculos', dict(lado=256, bisel=0.0)),
    'cartel_utah':      (cartel_utah,      'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
    'trax':             (trax,             'obstaculos', dict(lado=256, bisel=0.0)),
    'hot_rod':          (hot_rod,          'obstaculos', dict(lado=256, bisel=0.0)),
    'baliza_sal':       (baliza_sal,       'obstaculos', dict(lado=256, bisel=0.0)),
    'bolido_sal':       (bolido_sal,       'obstaculos', dict(lado=256, bisel=0.0)),
}

correr(PIEZAS)
