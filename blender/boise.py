# Nivel 32: Boise, Idaho (14/11/2026).
#
#   blender -b -P blender/boise.py -- [pieza ...] [--rapido]
#
# Historia: «Patatas rodando cuesta abajo». Acto de la Armada Española.
#   Por Capitol Boulevard, de la estación (estilo misión española, con su
#   campanario) al Capitolio de Idaho: el teatro egipcio, el Basque Block (la
#   comunidad vasca más grande de América: el Basque Center, la casa de
#   huéspedes y el frontón Anduiza de 1914) y el camión de la patata gigante.
#   La patata caliente: hay que pasársela a los periodistas antes de que
#   queme; y el momento estrella, el Jaialdi en el Basque Block: los
#   aizkolaris (troncos que se cortan a hachazos, tocando la pantalla muy
#   deprisa). Pancartas: ¡AUPA BOISE!
# Obstáculos (carpeta obstaculos): el periodista (se le pasa la patata), el
# saco y la caja de patatas, la pancarta ¡AUPA BOISE!, el camión de la patata
# gigante, el tronco de los aizkolaris y la patata que baja rodando.

import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import *

def blanco():    return mat('blanco_boi', 0xf6f4ee, 0.5)
def negro():     return mat('negro_boi', 0x1c1c20, 0.4)
def arenisca():  return mat_bloques('arenisca_boi', 0xdcd4c0, 0xbab29e, ancho=1.3, alto=0.6, grosor=0.008, variacion=1.04)
def arenisca_l(): return mat('arenisca_lisa_boi', 0xe4ddcc, 0.65)
def marmol():    return mat('marmol_boi', 0xf0ece4, 0.4)
def estuco():    return mat('estuco_boi', 0xf2ece0, 0.85)
def teja():      return mat('teja_boi', 0xb8502e, 0.7)
def ladrillo():  return mat_bloques('ladrillo_boi', 0xa85a3e, 0x7a4030, ancho=0.4, alto=0.16)
def piedra():    return mat('piedra_boi', 0xe0d6c0, 0.7)
def cristal():   return mat('cristal_boi', 0x3a5a70, 0.15)
def rojo():      return mat('rojo_boi', 0xc8202a, 0.45)
def verde():     return mat('verde_boi', 0x1e7a3e, 0.45)
def azul():      return mat('azul_boi', 0x2a4a9a, 0.45)
def amarillo():  return mat('amarillo_boi', 0xf2c21a, 0.45)
def oro():       return mat('oro_boi', 0xe8b840, 0.25)
def cobre():     return mat('cobre_boi', 0x8a5a2a, 0.35)
def gris():      return mat('gris_boi', 0x8a9098, 0.4)
def hierro():    return mat('hierro_boi', 0x2a2c30, 0.45)
def madera():    return mat('madera_boi', 0x8a5a34, 0.85)
def madera_o():  return mat('madera_oscura_boi', 0x5a3a22, 0.85)
def cesped():    return mat('cesped_boi', 0x6a9a48, 0.9)
def copa():      return mat('copa_boi', 0x4a7a3a, 0.85)
def patata_m():  return mat('patata_boi', 0xb8884e, 0.85)
def patata_o():  return mat('patata_ojo_boi', 0x6a4a26, 0.9)
def piel():      return mat('piel_boi', 0xe8b89a, 0.7)
def ocre():      return mat_bloques('ocre_boi', 0xc8a060, 0xa88448, ancho=1.0, alto=0.5, grosor=0.008, variacion=1.05)

def patata(m, ojos, x, y, z, largo, ancho, alto, giro=0.0):
    """Una patata: un elipsoide algo abollado, con sus ojos."""
    sub = 3 if largo > 0.5 else 2
    o = esfera(m, x, y, z, 0.5, sub, esc=(largo, ancho, alto))
    o.rotation_euler = (0, 0, giro)
    o = esfera(m, x + math.cos(giro) * largo * 0.18, y + math.sin(giro) * largo * 0.18, z + alto * 0.04, 0.5,
               sub, esc=(largo * 0.7, ancho * 1.04, alto * 1.02))
    o.rotation_euler = (0, 0, giro)
    if largo < 0.5:
        return
    for (u, v, w) in ((0.2, -0.47, 0.1), (-0.25, -0.46, -0.05), (0.05, -0.43, 0.25), (-0.38, -0.36, 0.18), (0.36, -0.38, -0.16)):
        e = esfera(ojos, x + u * largo * math.cos(giro) - v * ancho * math.sin(giro),
                   y + u * largo * math.sin(giro) + v * ancho * math.cos(giro), z + w * alto, 0.03 * max(1, largo), 1,
                   esc=(1.4, 1.4, 0.6))
        e.rotation_euler = (0, 0, giro)

def guirnalda(x0, x1, y, z, n=14, cuelga=0.6):
    """Una cuerda de banderitas rojas, blancas y verdes (de fiesta)."""
    cil(hierro(), (x0 + x1) / 2, y, z, 0.015, abs(x1 - x0), 4, eje='X')
    cols = (rojo, blanco, verde)
    for k in range(n):
        u = (k + 0.5) / n
        x = x0 + (x1 - x0) * u
        zz = z - cuelga * 4 * u * (1 - u)
        o = cil(cols[k % 3](), x, y, zz - 0.42, 0.22, 0.42, 3, r2=0.0)
        o.rotation_euler = (math.pi, 0, 0)
        o.location = (x, y, zz)
        o.scale = (1, 0.15, 1)

# ================================================================ la meta
def capitolio_idaho():
    """El Capitolio de Idaho (la meta): la arenisca clara de Boise, el
    pórtico con cuatro columnas corintias de dos pisos, las alas con sus
    columnatas, el tambor alto con columnas, la cúpula blanca con nervios y
    la linterna con el águila de cobre; delante, la réplica de la Campana de
    la Libertad, la bandera y la pancarta ¡AUPA BOISE!"""
    Y = 26
    W, D, H = 64.0, 26.0, 15.0
    yf = Y - D / 2
    g = arenisca()
    caja(g, 0, Y, 0, W, D, H)
    caja(arenisca_l(), 0, Y, H, W + 0.6, D + 0.6, 0.9)
    caja(g, 0, Y, H + 0.9, W - 4, D - 4, 1.6)
    for s in (-1, 1):
        # Las alas: un poco adelantadas, con seis columnas y su ático.
        caja(g, s * 23, yf - 1.5, 0, 16, 3, H)
        columnata(marmol(), s * 23 - 6.5, s * 23 + 6.5, 6, yf - 3.2, 3.2, 0.55, 10.5)
        caja(arenisca_l(), s * 23, yf - 3.2, 13.7, 16, 1.6, 1.3)
        caja(g, s * 23, yf - 3.2, 3.0, 16, 1.6, 0.2)
        for k in range(5):
            x = s * 23 - 6.5 + k * 3.25 + 1.6
            if k < 4:
                ventana(x, 4.8, 1.3, 2.8, y=yf - 1.55, marco=arenisca_l(), cristal=cristal(), remate='fronton')
                ventana(x, 9.6, 1.3, 2.4, y=yf - 1.55, marco=arenisca_l(), cristal=cristal())
    for k in range(6):
        x = -11.5 + k * 4.6
        if abs(x) < 7:
            continue
        ventana(x, 4.5, 1.4, 3.0, y=yf - 0.05, marco=arenisca_l(), cristal=cristal(), remate='fronton')
    # El pórtico central: cuatro columnas de dos pisos y el frontón.
    caja(g, 0, yf - 4, 0, 16, 8, 3.4)
    columnata(marmol(), -5.4, 5.4, 4, yf - 7, 3.4, 0.8, 11.0)
    caja(arenisca_l(), 0, yf - 5.5, 14.4, 16, 6, 1.4)
    fronton(arenisca_l(), 0, yf - 6.2, 15.8, 16, 3.6, 5.2)
    puerta(0, 3.4, 2.6, 4.6, y=yf - 0.05, color=0x5a3a22, marco=arenisca_l())
    # La escalinata.
    for k in range(12):
        caja(arenisca_l(), 0, yf - 8.4 - k * 0.5, 0, 22 + k * 0.6, 0.5, 3.4 - k * 0.28)
    # El tambor (dos cuerpos), la cúpula blanca con nervios y la linterna.
    Z = H + 2.5
    cil(g, 0, Y, Z, 9.4, 3.2, 36)
    cil(arenisca_l(), 0, Y, Z + 3.2, 9.8, 0.6, 36)
    cil(arenisca_l(), 0, Y, Z + 3.8, 7.8, 8.0, 36)
    for k in range(20):
        a = k * math.tau / 20
        cil(marmol(), math.cos(a) * 8.2, Y + math.sin(a) * 8.2, Z + 3.8, 0.34, 8.0, 10)
    for k in range(10):
        a = k * math.tau / 10 + 0.16
        cil(cristal(), math.cos(a) * 7.85, Y + math.sin(a) * 7.85, Z + 5.2, 0.8, 4.4, 8)
    cil(arenisca_l(), 0, Y, Z + 11.8, 8.8, 1.0, 36)
    cil(g, 0, Y, Z + 12.8, 7.6, 1.6, 36)
    cupula(marmol(), 0, Y, Z + 14.4, 7.4, 10.5, 36, 10)
    for k in range(16):
        a = k * math.tau / 16
        rama(mat('nervio_boi', 0xd8d2c4, 0.4), (math.cos(a) * 7.4, Y + math.sin(a) * 7.4, Z + 14.5),
             (math.cos(a) * 1.6, Y + math.sin(a) * 1.6, Z + 24.6), 0.14, 0.08, 4)
    cil(arenisca_l(), 0, Y, Z + 24.6, 1.9, 3.4, 12)
    for k in range(8):
        a = k * math.tau / 8
        cil(marmol(), math.cos(a) * 1.95, Y + math.sin(a) * 1.95, Z + 24.6, 0.14, 3.4, 6)
    cupula(marmol(), 0, Y, Z + 28.0, 2.0, 1.8, 12, 4)
    cil(arenisca_l(), 0, Y, Z + 29.7, 0.5, 0.8, 8)
    # El águila de cobre, con las alas abiertas.
    c = cobre()
    esfera(c, 0, Y, Z + 31.2, 0.45, 2, esc=(0.8, 0.9, 1.4))
    esfera(c, 0, Y - 0.35, Z + 32.0, 0.25, 1, esc=(0.9, 1.2, 0.9))
    for s in (-1, 1):
        rama(c, (s * 0.2, Y, Z + 31.6), (s * 1.6, Y + 0.1, Z + 32.6), 0.22, 0.06, 4)
    # El césped, los árboles y la Campana de la Libertad (réplica) delante.
    caja(cesped(), 0, yf - 20, -0.05, 90, 26, 0.06)
    for (x, y) in ((-32, yf - 10), (-37, yf - 21), (32, yf - 10), (37, yf - 20), (-44, yf + 3), (44, yf + 3)):
        cil(madera_o(), x, y, 0, 0.35, 3.2, 8)
        esfera(copa(), x, y, 5.2, 3.2, 2, esc=(1, 1, 1.15))
    caja(mat('pedestal_boi', 0x9a9488, 0.6), -12, yf - 16, 0, 2.6, 2.6, 1.6)
    cil(mat('campana_boi', 0x5a4a32, 0.35), -12, yf - 16, 1.6, 0.95, 1.5, 18, r2=0.62)
    cil(mat('campana_boi', 0x5a4a32, 0.35), -12, yf - 16, 3.1, 0.55, 0.35, 12)
    caja(madera_o(), -12, yf - 16, 3.45, 2.2, 0.3, 0.3)
    for s in (-1, 1):
        caja(madera_o(), -12 + s * 1.05, yf - 16, 1.6, 0.25, 0.3, 2.15)
    # La bandera de Idaho y la pancarta.
    cil(gris(), -22, yf - 14, 0, 0.13, 13, 8)
    caja(mat('bandera_id_boi', 0x1e3a7a, 0.6), -20.2, yf - 14, 10.6, 3.6, 0.06, 2.4)
    esfera(mat('sello_id_boi', 0xe8d8a8, 0.5), -20.2, yf - 14.06, 11.8, 0.55, 1, esc=(1, 0.1, 1))
    for x in (9.5, 21.5):
        cil(madera_o(), x, yf - 15, 0, 0.12, 4.4, 8)
    cartel_aupa(15.5, yf - 15, 2.8, 12, 1.6)

def cartel_aupa(x, y, z, w, h):
    """La pancarta blanca con el borde rojo: ¡AUPA BOISE! / LA CASA VASCA DE AMÉRICA."""
    caja(blanco(), x, y, z, w, 0.06, h)
    for dz in (0, h - h * 0.1):
        caja(rojo(), x, y - 0.01, z + dz, w, 0.06, h * 0.1)
    texto(rojo(), '¡AUPA BOISE!', x, y - 0.045, z + h * 0.45, tam=h * 0.34, prof=0.03)
    texto(negro(), 'LA CASA VASCA DE AMÉRICA', x, y - 0.045, z + h * 0.16, tam=h * 0.12, prof=0.02)

# ================================================================ edificios
def boise_depot():
    """La estación de Boise (1925), de estilo misión española: el estuco
    blanco, los tejados de teja roja, los arcos de la galería, el campanario
    con sus arcos y el letrero UNION PACIFIC."""
    Y = 9
    W, D = 40.0, 14.0
    yf = Y - D / 2
    e = estuco()
    caja(e, 6, Y, 0, 28, D, 7.5)
    tejado(teja(), 6, Y - D / 2, Y + D / 2, 7.5, 28, 3.2, cumbrera='x')
    caja(e, -13, Y + 1, 0, 10, D - 2, 5.0)
    tejado(teja(), -13, Y - D / 2 + 1, Y + D / 2 - 1, 5.0, 10, 2.4, cumbrera='x')
    # La galería de arcos delante.
    caja(e, 6, yf - 1.6, 4.0, 26, 3.2, 0.8)
    tejado(teja(), 6, yf - 3.4, yf, 4.8, 26, 1.0, cumbrera='x')
    for k in range(7):
        x = -5 + k * 3.66
        caja(e, x - 1.6, yf - 3.0, 0, 0.6, 0.6, 4.0)
        cil(e, x, yf - 3.0, 4.0, 1.5, 0.6, 16, eje='Y').scale = (1, 1, 0.7)
    caja(e, 6 + 13 + 0.3, yf - 3.0, 0, 0.6, 0.6, 4.0)
    for x in (0, 6, 12, 18):
        ventana(x, 1.0, 1.6, 2.6, y=yf - 0.05, marco=madera_o(), cristal=cristal())
    for x in (-16, -10):
        ventana(x, 1.2, 1.4, 2.2, y=Y - D / 2 + 1 - 0.05, marco=madera_o(), cristal=cristal())
    # El campanario.
    T = 5.6
    x0, y0 = -6.5, yf + 1.2
    caja(e, x0, y0, 0, T, T, 22)
    for z in (7.5, 15.5):
        caja(e, x0, y0, z, T + 0.4, T + 0.4, 0.5)
    for (dx, dy) in ((0, -1), (-1, 0), (1, 0)):
        x, y = x0 + dx * (T / 2 + 0.05), y0 + dy * (T / 2 + 0.05)
        if dy:
            caja(negro(), x, y, 16.5, 2.2, 0.1, 3.4)
            cil(negro(), x, y, 19.9, 1.1, 0.1, 14, eje='Y')
            cil(mat('campana_dep_boi', 0xb89a40, 0.3), x, y + 0.6, 17.4, 0.55, 1.0, 12, r2=0.3)
        else:
            o = caja(negro(), x, y, 16.5, 0.1, 2.2, 3.4)
    # El reloj y el tejado del campanario.
    cil(blanco(), x0, y0 - T / 2 - 0.1, 11.6, 1.3, 0.12, 24, eje='Y')
    caja(negro(), x0, y0 - T / 2 - 0.2, 11.6, 0.1, 0.04, 1.0)
    caja(negro(), x0 + 0.35, y0 - T / 2 - 0.2, 11.6, 0.7, 0.04, 0.1)
    caja(e, x0, y0, 22, T + 0.5, T + 0.5, 0.6)
    o = cil(teja(), x0, y0, 22.6, T * 0.76, 3.6, 4, r2=0.1)
    o.rotation_euler = (0, 0, math.pi / 4)
    cil(hierro(), x0, y0, 26.2, 0.08, 1.6, 6)
    # El letrero.
    caja(mat('letrero_dep_boi', 0x2a3a5a, 0.5), 6, yf - 3.25, 5.0, 12, 0.15, 1.1)
    texto(blanco(), 'UNION PACIFIC', 6, yf - 3.36, 5.55, tam=0.8, prof=0.04)
    texto(madera_o(), 'BOISE', 6, yf - 0.06, 6.6, tam=0.6, prof=0.03)

def egyptian_theatre():
    """El teatro egipcio de Boise (1927): la fachada ocre con dos columnas
    enormes de capitel de loto, el disco solar con alas, las franjas de
    jeroglíficos de colores, el rótulo vertical EGYPTIAN y la marquesina con
    bombillas."""
    Y = 8
    W, D, H = 20.0, 12.0, 14.0
    yf = Y - D / 2
    o_ = ocre()
    caja(o_, 0, Y, 0, W, D, H)
    caja(mat('cornisa_eg_boi', 0xd8b878, 0.6), 0, yf - 0.3, H - 1.6, W + 0.6, 0.8, 1.6)
    for (z, c) in ((H - 2.4, azul), (H - 2.9, rojo), (H - 3.4, oro)):
        caja(c(), 0, yf - 0.06, z, W - 1, 0.1, 0.4)
    # Los jeroglíficos (rayitas y figuras) entre franjas.
    for k in range(18):
        x = -8.5 + k * 1.0
        caja([azul, rojo, verde][k % 3](), x, yf - 0.1, H - 5.0, 0.3, 0.08, 1.2 if k % 2 else 0.7)
    # Las columnas de loto.
    for s in (-1, 1):
        x = s * 4.8
        cil(mat('columna_eg_boi', 0xe0c88a, 0.6), x, yf - 1.0, 0, 0.9, 8.5, 18, r2=0.75)
        for z in (1.0, 2.2, 7.4):
            cil([azul, rojo, oro][int(z) % 3](), x, yf - 1.0, z, 0.93, 0.25, 18)
        cil(mat('loto_eg_boi', 0x3a8a6a, 0.5), x, yf - 1.0, 8.5, 0.8, 1.4, 18, r2=1.35)
        caja(o_, x, yf - 1.0, 9.9, 2.8, 2.0, 0.6)
    # El disco solar con alas.
    esfera(oro(), 0, yf - 0.2, 11.6, 0.65, 2, esc=(1, 0.2, 1))
    for s in (-1, 1):
        for k in range(4):
            caja([azul, oro][k % 2](), s * (1.2 + k * 0.7), yf - 0.15, 11.4 + k * 0.12, 0.7, 0.08, 0.5 - k * 0.07)
    # La entrada, la marquesina con bombillas y el rótulo vertical.
    for x in (-1.4, 1.4):
        puerta(x, 0, 1.6, 2.6, y=yf - 0.05, color=0x8a2a1e, marco=oro())
    caja(mat('marquesina_eg_boi', 0x1c1c3a, 0.5), 0, yf - 1.6, 3.4, 12, 3.2, 1.2)
    caja(blanco(), 0, yf - 3.22, 3.5, 11, 0.06, 1.0)
    texto(rojo(), 'EGYPTIAN', 0, yf - 3.26, 4.0, tam=0.5, prof=0.02)
    texto(negro(), 'TONIGHT · MAGA TACO', 0, yf - 3.26, 3.6, tam=0.26, prof=0.02)
    bomb = luz('bombilla_eg_boi', 0xffe6a0, 1.2)
    for k in range(24):
        caja(bomb, -5.8 + k * 0.5, yf - 3.25, 4.45, 0.14, 0.06, 0.14)
    caja(mat('rotulo_eg_boi', 0x1c1c3a, 0.5), 7.6, yf - 1.2, 5.0, 0.4, 1.4, 8.4)
    for k, c in enumerate('EGYPTIAN'):
        texto(amarillo(), c, 7.38, yf - 1.2, 12.6 - k * 1.0, tam=0.8, prof=0.03).rotation_euler = (math.pi / 2, 0, -math.pi / 2)
        texto(amarillo(), c, 7.82, yf - 1.2, 12.6 - k * 1.0, tam=0.8, prof=0.03).rotation_euler = (math.pi / 2, 0, math.pi / 2)

def casa_vasca():
    """El Basque Block: la casa de huéspedes de ladrillo (Jacobs-Uberuaga),
    el Basque Center blanco con contraventanas rojas y verdes y el letrero
    EUSKAL ETXEA, y el frontón Anduiza de 1914; guirnaldas de fiesta."""
    Y = 8
    D = 12.0
    yf = Y - D / 2
    # La casa de huéspedes (izquierda): ladrillo, porche blanco.
    l = ladrillo()
    caja(l, -11, Y, 0, 10, D, 8.0)
    tejado(mat('tejado_vasca_boi', 0x4a4a52, 0.6), -11, Y - D / 2, Y + D / 2, 8.0, 10, 3.0, cumbrera='x')
    caja(blanco(), -11, yf - 1.2, 2.8, 9, 2.4, 0.25)
    for x in (-15, -11, -7):
        cil(blanco(), x, yf - 2.2, 0, 0.12, 2.8, 8)
    for x in (-13.5, -8.5):
        ventana(x, 0.9, 1.3, 2.0, y=yf - 0.05, marco=blanco(), cristal=cristal())
        ventana(x, 4.4, 1.2, 2.0, y=yf - 0.05, marco=blanco(), cristal=cristal())
    puerta(-11, 0, 1.2, 2.3, y=yf - 0.05, color=0x1e5a32, marco=blanco())
    # El Basque Center (centro): estuco blanco, contraventanas, balcón de madera.
    e = estuco()
    caja(e, 1, Y, 0, 12, D, 9.0)
    tejado(teja(), 1, Y - D / 2, Y + D / 2, 9.0, 12, 2.6, cumbrera='x')
    for x in (-2.5, 1, 4.5):
        ventana(x, 1.0, 1.2, 1.9, y=yf - 0.05, marco=madera_o(), cristal=cristal())
        ventana(x, 5.2, 1.1, 1.8, y=yf - 0.05, marco=madera_o(), cristal=cristal())
        for s in (-1, 1):
            caja([rojo, verde][(int(x) + s) % 2](), x + s * 0.9, yf - 0.08, 5.2, 0.55, 0.06, 1.8)
    caja(madera_o(), 1, yf - 0.7, 4.6, 11, 1.4, 0.15)
    for k in range(12):
        caja(madera_o(), -4.3 + k * 0.96, yf - 1.35, 4.75, 0.08, 0.08, 0.9)
    caja(madera_o(), 1, yf - 1.35, 5.62, 11, 0.12, 0.1)
    caja(rojo(), 1, yf - 0.06, 7.6, 8.6, 0.1, 0.9)
    texto(blanco(), 'EUSKAL ETXEA', 1, yf - 0.12, 7.86, tam=0.5, prof=0.03)
    texto(madera_o(), 'BASQUE CENTER', 1, yf - 0.06, 3.5, tam=0.45, prof=0.03)
    # El frontón Anduiza (derecha): ladrillo y la fecha.
    caja(l, 13, Y, 0, 10, D, 10.5)
    caja(piedra(), 13, yf - 0.1, 10.0, 10.4, 0.4, 0.6)
    for x in (10, 13, 16):
        o = cil(piedra(), x, yf - 0.06, 6.6, 1.0, 0.1, 14, eje='Y')
        caja(cristal(), x, yf - 0.08, 4.6, 1.8, 0.08, 2.0)
    puerta(13, 0, 2.0, 3.0, y=yf - 0.05, color=0x1e5a32, marco=piedra())
    caja(piedra(), 13, yf - 0.1, 8.4, 7, 0.12, 1.0)
    texto(rojo(), 'ANDUIZA · 1914', 13, yf - 0.18, 8.62, tam=0.55, prof=0.03)
    texto(negro(), 'FRONTÓN', 13, yf - 0.06, 3.3, tam=0.42, prof=0.03)
    # Las guirnaldas de fiesta y el banco de la calle.
    guirnalda(-16, 18, yf - 1.8, 6.6, 26, 0.8)
    guirnalda(-16, 18, yf - 1.8, 8.6, 26, 0.6)
    for x in (-16, 18):
        cil(hierro(), x, yf - 1.8, 0, 0.07, 8.8, 6)

def patata_acera():
    """La patata gigante de Idaho sobre su peana (para la acera)."""
    caja(piedra(), 0, 0, 0, 1.3, 1.0, 0.7)
    texto(azul(), 'IDAHO', 0, -0.52, 0.22, tam=0.24, prof=0.02)
    patata(patata_m(), patata_o(), 0, 0, 1.25, 1.9, 1.1, 1.05, 0.3)

# ================================================================ cruzan la calle
def arco_vasco():
    """El arco de la calle del Basque Block: dos postes de madera y el
    letrero ONGI ETORRI · BASQUE BLOCK (bienvenidos), con guirnaldas; por
    detrás, AGUR!"""
    m = madera()
    for s in (-1, 1):
        caja(m, s * 8.6, 0, 0, 0.7, 0.7, 7.8)
        caja(madera_o(), s * 8.6, 0, 7.8, 0.9, 0.9, 0.3)
    caja(m, 0, 0, 7.0, 18.2, 0.5, 0.6)
    caja(rojo(), 0, 0, 4.2, 12, 0.18, 1.6)
    caja(blanco(), 0, -0.02, 4.35, 11.6, 0.18, 1.3)
    texto(rojo(), 'ONGI ETORRI', 0, -0.13, 5.05, tam=0.6, prof=0.04)
    texto(verde(), 'BASQUE BLOCK', 0, -0.13, 4.5, tam=0.42, prof=0.04)
    o = texto(rojo(), 'AGUR!', 0, 0.13, 4.75, tam=0.8, prof=0.04)
    o.rotation_euler = (math.pi / 2, 0, math.pi)
    for x in (-4, 4):
        cil(hierro(), x, 0, 5.8, 0.03, 1.2, 4)
    guirnalda(-8.3, 8.3, 0, 6.9, 22, 0.9)

# ================================================================ el Jaialdi
def plaza_aizkolari():
    """El Jaialdi en el Basque Block (momento estrella, al aire libre): el
    suelo de adoquines, las vallas rojas y blancas, el público vestido de
    blanco con pañuelo rojo y txapela, las pilas de troncos cortados, las
    piedras de los levantadores con sus kilos, los frontones a los lados, las
    carpas, las guirnaldas que cruzan y los arcos de SALIDA y META.
    Cruza la calle: el origen en el centro y la calle a lo largo de y."""
    L = 420
    caja(mat_bloques('adoquin_boi', 0x9a9088, 0x6a625a, ancho=0.5, alto=0.5, grosor=0.02, variacion=1.12), 0, 0, -0.2, 24, L, 0.2)
    for s in (-1, 1):
        # La valla de fiesta (franjas rojas y blancas).
        for k in range(int(L / 2.4)):
            caja([rojo, blanco][k % 2](), s * 7.6, -L / 2 + 1.2 + k * 2.4, 0, 0.12, 2.4, 1.1)
        # Las gradas con el público de blanco y rojo.
        for g in range(5):
            caja(mat_bloques('gente_boi', 0xe8e4dc, 0xc82a2a, ancho=0.5, alto=0.7, variacion=1.25), s * (10.5 + g * 3.0), 0, 0, 3.0, L, 1.6 + g * 2.0)
        caja(mat('muro_grada_boi', 0x6a3a2a, 0.7), s * 8.8, 0, 0, 2.2, L, 1.4)
    for k in range(int(L / 3.4)):
        y = -L / 2 + 2 + k * 3.4
        s = -1 if k % 2 else 1
        cil(mat('camisa_blanca_boi', 0xf2f0ea, 0.8), s * 10.2, y, 1.4, 0.4, 0.85, 6)
        cil(rojo(), s * 10.2, y, 2.2, 0.34, 0.12, 8)
        esfera(piel(), s * 10.2, y, 2.55, 0.28, 1)
        cil(negro(), s * 10.2, y, 2.74, 0.32, 0.1, 10)
    # Los frontones (paredes altas verdes con la línea) y las carpas.
    for k in range(int(L / 105)):
        y = -L / 2 + 50 + k * 105
        for s in (-1, 1):
            caja(mat('fronton_boi', 0x2a6a4a, 0.7), s * 26, y, 0, 1.2, 22, 14)
            caja(blanco(), s * 25.38, y, 1.0, 0.04, 22, 0.15)
            caja(blanco(), s * 25.38, y, 0, 0.04, 0.15, 14)
    for k in range(int(L / 60)):
        y = -L / 2 + 25 + k * 60
        s = 1 if k % 2 else -1
        caja(blanco(), s * 23, y, 0, 6, 6, 3.0)
        o = cil(blanco(), s * 23, y, 3.0, 4.3, 2.0, 4, r2=0.2)
        o.rotation_euler = (0, 0, math.pi / 4)
        caja(rojo(), s * 23, y - 3.05, 2.4, 6, 0.06, 0.5)
    # Los troncos cortados y las piedras de los levantadores, junto a la valla.
    for k in range(int(L / 30)):
        y = -L / 2 + 14 + k * 30
        s = -1 if k % 2 else 1
        for i in range(6):
            cil(mat('tronco_pila_boi', 0x8a6a44, 0.85), s * 6.6, y + (i % 3) * 0.55, 0.25 + (i // 3) * 0.48, 0.25, 1.4, 10, eje='X')
        caja(mat('piedra_harri_boi', 0x7a7a78, 0.7), s * 6.4, y + 4, 0, 0.8, 0.8, 0.7)
        texto(rojo(), '250', s * 6.4, y + 3.58, 0.3, tam=0.22, prof=0.02)
        cil(mat('piedra_harri_boi', 0x7a7a78, 0.7), s * 6.4, y + 6, 0, 0.42, 0.75, 14)
    # Las guirnaldas que cruzan por arriba.
    for k in range(int(L / 35)):
        guirnalda(-8.4, 8.4, -L / 2 + 17 + k * 35, 8.2, 22, 0.7)
    for k in range(int(L / 35)):
        for s in (-1, 1):
            cil(hierro(), s * 8.4, -L / 2 + 17 + k * 35, 0, 0.07, 8.4, 6)
    for (y, txt) in ((-L / 2 + 1, 'SALIDA'), (L / 2 - 1, 'META')):
        for s in (-1, 1):
            caja(madera(), s * 7.0, y, 0, 0.6, 0.6, 6.2)
        caja(madera(), 0, y, 5.6, 14.6, 0.5, 0.6)
        caja(rojo(), 0, y, 4.0, 7.0, 0.16, 1.3)
        texto(blanco(), 'JAIALDI · ' + txt, 0, y - 0.1, 4.45, tam=0.55, prof=0.04)

# ================================================================ obstáculos
def periodista():
    """El periodista de las noticias falsas (se le pasa la patata caliente):
    traje gris, corbata roja, la acreditación FAKE NEWS y el micrófono hacia
    delante. Mira al jugador (-y)."""
    traje = mat('traje_per_boi', 0x5a5e6a, 0.7)
    cil(negro(), -0.14, 0, 0, 0.11, 0.85, 8)
    cil(negro(), 0.14, 0, 0, 0.11, 0.85, 8)
    cil(traje, 0, 0, 0.82, 0.3, 0.7, 10, r2=0.34)
    caja(blanco(), 0, -0.3, 1.2, 0.18, 0.04, 0.3)
    caja(rojo(), 0, -0.33, 1.05, 0.08, 0.03, 0.42)
    caja(rojo(), 0.17, -0.33, 1.25, 0.22, 0.02, 0.14)
    texto(blanco(), 'FAKE', 0.17, -0.345, 1.29, tam=0.05, prof=0.005)
    texto(blanco(), 'NEWS', 0.17, -0.345, 1.23, tam=0.05, prof=0.005)
    esfera(piel(), 0, 0, 1.72, 0.2, 2, esc=(1, 1, 1.1))
    esfera(mat('pelo_per_boi', 0x3a2a1e, 0.8), 0, 0.04, 1.82, 0.2, 2, esc=(1.02, 1.0, 0.75))
    for s in (-1, 1):
        esfera(negro(), s * 0.07, -0.18, 1.74, 0.025, 1)
    caja(mat('boca_per_boi', 0x6a2a20, 0.6), 0, -0.185, 1.61, 0.09, 0.02, 0.025)
    for s in (-1, 1):
        caja(mat('ceja_per_boi', 0x3a2a1e, 0.8), s * 0.075, -0.185, 1.79, 0.07, 0.02, 0.018)
    # El brazo izquierdo abajo y el derecho con el micrófono hacia delante.
    rama(traje, (-0.33, 0, 1.45), (-0.38, -0.05, 0.95), 0.08, 0.07, 6)
    rama(traje, (0.33, 0, 1.45), (0.36, -0.45, 1.3), 0.08, 0.07, 6)
    esfera(piel(), 0.36, -0.5, 1.3, 0.07, 1)
    cil(negro(), 0.36, -0.6, 1.3, 0.04, 0.3, 8, eje='Y')
    esfera(mat('rejilla_per_boi', 0x3a3a3e, 0.5), 0.36, -0.78, 1.3, 0.07, 1)
    caja(rojo(), 0.36, -0.66, 1.3, 0.12, 0.08, 0.12)

def saco_patatas():
    """Dos sacos de arpillera de patatas de Idaho, uno encima del otro (se
    salta)."""
    arp = mat_bloques('arpillera_boi', 0xc8a878, 0xa88a5a, ancho=0.05, alto=0.05, grosor=0.006, variacion=1.05)
    for (x, z, g) in ((-0.35, 0, 0.1), (0.38, 0, -0.1), (0.0, 0.4, 0.05)):
        o = esfera(arp, x, 0, z + 0.22, 0.5, 2, esc=(0.75, 0.55, 0.45))
        o.rotation_euler = (0, 0, g)
    caja(blanco(), 0.0, -0.3, 0.6, 0.5, 0.02, 0.2)
    texto(azul(), 'IDAHO', 0.0, -0.31, 0.63, tam=0.12, prof=0.01)
    for (x, y) in ((-0.62, -0.1), (0.7, -0.05)):
        patata(patata_m(), patata_o(), x, y - 0.25, 0.07, 0.16, 0.1, 0.1)

def caja_patatas():
    """La caja de madera llena de patatas (se salta)."""
    m = madera()
    for z in (0, 0.25, 0.5):
        caja(m, 0, -0.45, z + 0.02, 1.5, 0.05, 0.2)
        caja(m, 0, 0.45, z + 0.02, 1.5, 0.05, 0.2)
    for s in (-1, 1):
        caja(madera_o(), s * 0.75, 0, 0, 0.06, 0.95, 0.75)
    caja(madera_o(), 0, 0, 0, 1.5, 0.9, 0.05)
    for k in range(14):
        x = -0.6 + (k % 7) * 0.2
        y = -0.25 + (k // 7) * 0.45
        patata(patata_m(), patata_o(), x, y, 0.72 + (k % 3) * 0.04, 0.24, 0.16, 0.14, k * 0.7)
    caja(blanco(), 0, -0.48, 0.3, 0.6, 0.02, 0.22)
    texto(rojo(), 'SPUDS', 0, -0.5, 0.34, tam=0.13, prof=0.01)

def cartel_boise():
    """La pancarta ¡AUPA BOISE! (agacharse)."""
    for x in (-1.25, 1.25):
        cil(madera(), x, 0, 0, 0.07, 2.75, 8)
    caja(blanco(), 0, 0, 1.5, 2.4, 0.05, 1.2)
    for z in (1.5, 2.58):
        caja(rojo(), 0, -0.01, z, 2.4, 0.05, 0.12)
    texto(rojo(), '¡AUPA', 0, -0.035, 2.17, tam=0.3, prof=0.02)
    texto(verde(), 'BOISE!', 0, -0.035, 1.72, tam=0.3, prof=0.02)

def camion_patata():
    """El camión de la patata gigante de Idaho (no se pasa): la cabina roja
    mirando al jugador, la plataforma y encima la patata de 7 m; en la
    cabina, el letrero BIG IDAHO POTATO. El morro en el origen."""
    r = mat('cabina_pat_boi', 0xc8202a, 0.4)
    caja(r, 0, 1.25, 0.55, 2.5, 2.5, 1.6)
    caja(r, 0, 1.6, 2.15, 2.5, 1.8, 1.1)
    caja(cristal(), 0, 0.68, 2.25, 2.2, 0.06, 0.85)
    caja(gris(), 0, -0.02, 0.55, 2.5, 0.1, 0.7)
    for s in (-1, 1):
        caja(luz('faro_pat_boi', 0xfff2c0, 1.0), s * 0.9, -0.05, 1.05, 0.4, 0.06, 0.25)
    caja(blanco(), 0, 1.0, 3.3, 2.5, 0.12, 0.7)
    texto(rojo(), 'BIG IDAHO', 0, 0.92, 3.73, tam=0.24, prof=0.02)
    texto(azul(), 'POTATO', 0, 0.92, 3.42, tam=0.24, prof=0.02)
    caja(hierro(), 0, 6.3, 0.55, 2.5, 7.2, 0.5)
    for y in (1.1, 4.0, 5.2, 8.6, 9.6):
        for s in (-1, 1):
            cil(negro(), s * 1.25, y, 0.5, 0.5, 0.32, 16, eje='X')
    patata(patata_m(), patata_o(), 0, 6.2, 2.3, 7.0, 2.6, 2.5, math.pi / 2)
    texto(azul(), 'IDAHO', 0, 2.75, 2.4, tam=0.4, prof=0.03)

def tronco_aizkolari():
    """El tronco de haya de los aizkolaris, de pie sobre su soporte (no se
    pasa: se corta a hachazos), con la corteza, la cara de arriba clara y la
    marca roja donde se corta."""
    cort = mat_bloques('corteza_boi', 0x6a5a48, 0x4a3a2c, ancho=0.12, alto=0.5, grosor=0.02, variacion=1.15)
    caja(madera_o(), 0, 0, 0, 1.2, 0.3, 0.12)
    caja(madera_o(), 0, 0, 0, 0.3, 1.2, 0.12)
    cil(cort, 0, 0, 0.12, 0.42, 2.2, 16)
    cil(mat('madera_clara_boi', 0xe8cc98, 0.8), 0, 0, 2.32, 0.4, 0.04, 16)
    for r in (0.3, 0.18):
        cil(mat('anillo_boi', 0xc8a878, 0.8), 0, 0, 2.33, r, 0.02, 16)
    cil(rojo(), 0, 0, 1.15, 0.43, 0.08, 16)
    caja(blanco(), 0, -0.43, 1.5, 0.36, 0.02, 0.24)
    texto(rojo(), 'AIZKORA', 0, -0.44, 1.56, tam=0.07, prof=0.005)

def patata_rodante():
    """La patata que baja rodando calle abajo (se salta). Centrada en su eje
    (rueda sobre el eje x)."""
    patata(patata_m(), patata_o(), 0, 0, 0, 0.95, 0.8, 0.8, math.pi / 2)

PIEZAS = {
    'capitolio_idaho':  (capitolio_idaho,  'boise',      dict(lado=2048, bisel=0.0)),
    'boise_depot':      (boise_depot,      'boise',      dict(lado=1024, bisel=0.0)),
    'egyptian_theatre': (egyptian_theatre, 'boise',      dict(lado=1024, bisel=0.0)),
    'casa_vasca':       (casa_vasca,       'boise',      dict(lado=1024, bisel=0.0)),
    'patata_acera':     (patata_acera,     'boise',      dict(lado=256, bisel=0.0)),
    'arco_vasco':       (arco_vasco,       'boise',      dict(lado=1024, bisel=0.0, suelo=False)),
    'plaza_aizkolari':  (plaza_aizkolari,  'boise',      dict(lado=2048, bisel=0.0, suelo=False)),
    'periodista':       (periodista,       'obstaculos', dict(lado=256, bisel=0.0)),
    'saco_patatas':     (saco_patatas,     'obstaculos', dict(lado=256, bisel=0.0)),
    'caja_patatas':     (caja_patatas,     'obstaculos', dict(lado=256, bisel=0.0)),
    'cartel_boise':     (cartel_boise,     'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
    'camion_patata':    (camion_patata,    'obstaculos', dict(lado=256, bisel=0.0)),
    'tronco_aizkolari': (tronco_aizkolari, 'obstaculos', dict(lado=256, bisel=0.0)),
    'patata_rodante':   (patata_rodante,   'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
}

correr(PIEZAS)
