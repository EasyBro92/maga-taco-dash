# Nivel 31: Billings, Montana (14/11/2026).
#
#   blender -b -P blender/billings.py -- [pieza ...] [--rapido]
#
# Historia: «"Montana" viene de "montaña". Osos pardos». Acto de la Armada
#   Española.
#   Por Montana Avenue en otoño, con las Rimrocks (los acantilados de arenisca
#   que rodean la ciudad) al fondo: la estación del Northern Pacific, la torre
#   First Interstate (la más alta de Montana), la mansión Moss de arenisca
#   roja y el Skypoint, la marquesina de acero que cubre el cruce. Osos por la
#   calle (al pardo, hacerse el muerto; al negro, hacerse grande, como dicen
#   los guardas); el Gran Arreo de Montana por la pradera, empujando las vacas
#   hacia el corral; y se llega al pie de las Rimrocks, a la puerta de rancho
#   de THE MAGIC CITY. Pancartas de España: MONTANA = MONTAÑA.
# Obstáculos (carpeta obstaculos): el oso pardo y el oso negro, los dos
# corrales (a la derecha y a la izquierda de la calle), la pancarta de
# España, el tronco caído y el remolque del ganado.

import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import *

def blanco():    return mat('blanco_bil', 0xf6f4ee, 0.5)
def negro():     return mat('negro_bil', 0x1c1c20, 0.4)
def ladrillo():  return mat_bloques('ladrillo_bil', 0xa8603e, 0x7a4430, ancho=0.4, alto=0.16)
def ladrillo_c(): return mat_bloques('ladrillo_claro_bil', 0xd8b88a, 0xb89a6e, ancho=0.4, alto=0.16)
def arenisca_r(): return mat_bloques('arenisca_roja_bil', 0x9a4a32, 0x7a3626, ancho=1.0, alto=0.5, grosor=0.01, variacion=1.06)
def piedra():    return mat('piedra_bil', 0xe0d4bc, 0.7)
def cristal():   return mat('cristal_bil', 0x3a5a70, 0.15)
def rojo():      return mat('rojo_bil', 0xc8202a, 0.45)
def amarillo():  return mat('amarillo_bil', 0xf2c21a, 0.45)
def gris():      return mat('gris_bil', 0x8a9098, 0.4)
def hierro():    return mat('hierro_bil', 0x2a2c30, 0.45)
def madera():    return mat('madera_bil', 0x8a6038, 0.85)
def madera_o():  return mat('madera_oscura_bil', 0x5a3a22, 0.85)
def gris_madera(): return mat('madera_gris_bil', 0x9a8a78, 0.9)
def hierba():    return mat('hierba_bil', 0xb8a450, 0.95)
def tierra():    return mat('tierra_bil', 0xa88058, 0.95)
def pino_m():    return mat('pino_bil', 0x2a4a32, 0.85)
def alamo_m(c=0):  return mat('alamo_bil%d' % c, [0xe8b030, 0xd89a28, 0xc8b040][c % 3], 0.85)
def bronce():    return mat('bronce_bil', 0x6a4a2a, 0.35)

def bandera_es(nombre, z0, alto):
    """Las franjas de la bandera de España (roja, amarilla, roja) en z0..z0+alto."""
    return mat_franjas(nombre, 0xc8202a, 0xf2c21a, 3, eje='Z', z0=z0, alto=alto)

def acantilado(x0, x1, y, alto, prof=8.0, semilla=0):
    """Un trozo de las Rimrocks: arenisca en estratos (franjas claras y
    oscuras) con la cara un poco quebrada y pinos arriba."""
    est = mat_franjas('estratos_bil', 0xd8b47a, 0xb88a56, 9, eje='Z', z0=0, alto=alto)
    arriba = mat('roca_arriba_bil', 0x9a7a4a, 0.9)
    # Una pared seguida (el fondo) y, delante, salientes de roca de anchos y
    # alturas distintos, algo girados: así no parece una fila de edificios.
    caja(est, (x0 + x1) / 2, y + prof * 0.75, 0, x1 - x0, prof * 0.5, alto * 0.9)
    caja(arriba, (x0 + x1) / 2, y + prof * 0.75, alto * 0.9, x1 - x0 + 0.4, prof * 0.5 + 0.4, 0.5)
    x = x0
    k = 0
    while x < x1:
        w = 6 + 7 * (0.5 + 0.5 * math.sin(k * 2.7 + semilla))
        h = alto * (0.72 + 0.28 * (0.5 + 0.5 * math.sin(k * 1.9 + semilla * 3)))
        dy = 1.6 * math.sin(k * 2.3 + semilla)
        g = 0.12 * math.sin(k * 3.1 + semilla)
        caja(est, x + w / 2, y + dy + prof / 2, 0, w + 1.2, prof * 0.7, h, giro=g)
        caja(arriba, x + w / 2, y + dy + prof / 2, h, w + 1.4, prof * 0.7 + 0.3, 0.45, giro=g)
        if k % 2 == 0:
            pino(x + w / 2, y + dy + prof * 0.55, 4.5 + (k % 3), z=h + 0.4)
        x += w
        k += 1
    # Los derrubios del pie: montones de piedra suelta, como en las de verdad.
    for k in range(int((x1 - x0) / 6)):
        r = 2.2 + (k * 7 % 5) * 0.5
        esfera(mat('derrubio_bil', 0xb89a6a, 0.95), x0 + 3 + k * 6, y + 0.6, 0, r, 2, esc=(1.6, 0.9, 0.7), mitad=True)

def pino(x, y, alto=6.0, z=0.0):
    cil(madera_o(), x, y, z, 0.2, alto * 0.3, 8)
    for k in range(3):
        r = alto * (0.3 - k * 0.07)
        cil(pino_m(), x, y, z + alto * (0.2 + k * 0.24), r, alto * 0.38, 10, r2=0.05)

def alamo(x, y, alto=8.0, c=0):
    """Un álamo de río en otoño (cottonwood): el tronco y la copa amarilla."""
    cil(madera_o(), x, y, 0, 0.35, alto * 0.45, 8)
    esfera(alamo_m(c), x, y, alto * 0.65, alto * 0.32, 2, esc=(1.1, 1.0, 0.9))
    esfera(alamo_m(c + 1), x + alto * 0.18, y + 0.5, alto * 0.75, alto * 0.22, 1)

def vaca(x, y, mira=1, c=0x3a2a22):
    """Una vaca de lado (para el fondo y los corrales)."""
    m = mat(f'vaca_bil_{c:06x}', c, 0.7)
    esfera(m, x, y, 0.95, 0.45, 2, esc=(1.6, 0.8, 0.75))
    esfera(m, x + mira * 0.85, y, 1.05, 0.22, 1, esc=(1.4, 0.8, 0.9))
    esfera(blanco(), x + mira * 1.05, y, 1.0, 0.1, 1)
    for dx in (0.45, -0.45):
        for dy in (-0.18, 0.18):
            cil(m, x + dx, y + dy, 0, 0.07, 0.75, 6)

def vaquero_caballo(x, y, mira=1, camisa=0xc8202a):
    """Un vaquero a caballo (de lado), con su sombrero."""
    m = mat('caballo_bil', 0x7a4a2a, 0.7)
    esfera(m, x, y, 1.35, 0.55, 2, esc=(1.7, 0.75, 0.85))
    rama(m, (x + mira * 0.75, y, 1.5), (x + mira * 1.15, y, 2.1), 0.3, 0.22, 8)
    esfera(m, x + mira * 1.35, y, 2.1, 0.24, 1, esc=(1.6, 0.8, 0.9))
    for dx in (0.6, -0.6):
        for dy in (-0.2, 0.2):
            cil(m, x + dx, y + dy, 0, 0.09, 1.05, 6)
    rama(madera_o(), (x - mira * 0.9, y, 1.5), (x - mira * 1.25, y, 0.8), 0.1, 0.05, 6)
    cil(mat(f'camisa_bil_{camisa:06x}', camisa, 0.7), x, y, 1.85, 0.25, 0.8, 8)
    esfera(mat('cara_bil', 0xe8b89a, 0.7), x, y, 2.85, 0.2, 1)
    cil(mat('sombrero_bil', 0xe8dcc0, 0.7), x, y, 3.0, 0.38, 0.04, 12)
    cil(mat('sombrero_bil', 0xe8dcc0, 0.7), x, y, 3.03, 0.19, 0.24, 10, r2=0.16)

def valla_rancho(x0, x1, y, alto=1.3):
    """Valla de rancho de troncos (postes y dos travesaños)."""
    m = gris_madera()
    n = max(1, int((x1 - x0) / 3))
    for k in range(n + 1):
        cil(m, x0 + k * (x1 - x0) / n, y, 0, 0.1, alto, 6)
    for z in (alto * 0.45, alto * 0.85):
        cil(m, (x0 + x1) / 2, y, z, 0.07, x1 - x0, 6, eje='X')

def oso(m, hocico, x, y, z, k, giba=False):
    """Un oso a cuatro patas mirando a -y (al jugador) con la cabeza en y: el
    cuerpo va hacia +y. k: el tamaño."""
    cuerpo_y = y + 1.0 * k
    esfera(m, x, cuerpo_y, z + 0.95 * k, 0.6 * k, 2, esc=(0.95, 1.55, 0.85))
    esfera(m, x, cuerpo_y + 0.65 * k, z + 0.95 * k, 0.55 * k, 2, esc=(1.0, 1.0, 0.9))
    if giba:
        esfera(m, x, y + 0.6 * k, z + 1.38 * k, 0.42 * k, 2, esc=(1.0, 1.0, 0.7))
    # La cabeza, las orejas, el hocico y los ojos.
    esfera(m, x, y + 0.08 * k, z + 1.05 * k, 0.38 * k, 2)
    esfera(hocico, x, y - 0.25 * k, z + 0.95 * k, 0.17 * k, 1, esc=(1.0, 1.2, 0.85))
    esfera(negro(), x, y - 0.42 * k, z + 1.0 * k, 0.06 * k, 1)
    for s in (-1, 1):
        esfera(m, x + s * 0.27 * k, y + 0.12 * k, z + 1.38 * k, 0.12 * k, 1)
        esfera(negro(), x + s * 0.14 * k, y - 0.24 * k, z + 1.16 * k, 0.045 * k, 1)
    # Las patas, con las garras.
    for yy in (y + 0.45 * k, y + 1.55 * k):
        for s in (-1, 1):
            cil(m, x + s * 0.32 * k, yy, z, 0.17 * k, 0.75 * k, 8, r2=0.2 * k)
            for g in (-1, 0, 1):
                caja(mat('garra_bil', 0xe8dcc0, 0.5), x + s * 0.32 * k + g * 0.07 * k, yy - 0.18 * k, z, 0.03 * k, 0.1 * k, 0.04 * k)

# ================================================================ la meta
def rims_billings():
    """La meta: el pie de las Rimrocks, los acantilados de arenisca de
    Billings, con pinos arriba; delante, la puerta de rancho de troncos con
    THE MAGIC CITY, el oso pardo de bronce, los álamos amarillos del otoño y,
    de España, la pancarta MONTANA = MONTAÑA."""
    Y = 30
    acantilado(-60, 60, Y, 26, prof=12, semilla=0.4)
    caja(hierba(), 0, Y - 14, -0.05, 120, 30, 0.06)
    # La puerta del rancho.
    m = madera()
    for s in (-1, 1):
        cil(m, s * 9, Y - 16, 0, 0.6, 10, 10)
    cil(m, 0, Y - 16, 9.0, 0.5, 21, 10, eje='X')
    caja(madera_o(), 0, Y - 16, 6.2, 14, 0.25, 2.4)
    texto(amarillo(), 'THE MAGIC CITY', 0, Y - 16.15, 7.6, tam=1.3, prof=0.06)
    texto(blanco(), 'BILLINGS · MONTANA', 0, Y - 16.15, 6.6, tam=0.8, prof=0.05)
    for x in (-5, 5):
        cil(hierro(), x, Y - 16, 8.6, 0.05, 0.6, 4)
    # Cuernos de vaca encima.
    for s in (-1, 1):
        rama(mat('cuerno_bil', 0xe8dcc0, 0.5), (s * 0.4, Y - 16, 9.5), (s * 2.4, Y - 16, 10.6), 0.3, 0.08, 8)
    caja(madera_o(), 0, Y - 16, 9.3, 1.0, 0.6, 0.6)
    # El oso pardo de bronce sobre su roca.
    esfera(mat('roca_oso_bil', 0xb89a70, 0.9), -16, Y - 12, 0, 2.6, 2, esc=(1.2, 1.0, 0.6), mitad=True)
    oso(bronce(), bronce(), -16, Y - 13, 1.4, 1.6, giba=True)
    # Los álamos, la valla y la pancarta de España.
    for (x, y, c) in ((-30, Y - 8, 0), (-36, Y - 18, 1), (28, Y - 10, 2), (36, Y - 20, 0), (-24, Y - 24, 1), (22, Y - 25, 2)):
        alamo(x, y, 10, c)
    valla_rancho(-50, -11, Y - 16)
    valla_rancho(11, 50, Y - 16)
    for x in (11, 21):
        cil(madera_o(), x, Y - 21, 0, 0.12, 4.4, 8)
    caja(bandera_es('pancarta_es_meta_bil', 2.8, 1.6), 16, Y - 21, 2.8, 10, 0.06, 1.6)
    texto(negro(), 'MONTANA = MONTAÑA', 16, Y - 21.04, 3.6, tam=0.7, prof=0.03)

# ================================================================ edificios
def billings_depot():
    """La estación del Northern Pacific (1909): ladrillo claro, la planta baja
    con arcos, el tejado de teja roja con los hastiales de curvas y el
    letrero NORTHERN PACIFIC."""
    Y = 9
    W, D = 36.0, 13.0
    yf = Y - D / 2
    l = ladrillo_c()
    caja(l, 0, Y, 0, W, D, 8)
    caja(piedra(), 0, Y, 0, W + 0.3, D + 0.3, 0.8)
    caja(piedra(), 0, Y, 8, W + 0.4, D + 0.4, 0.5)
    tejado(mat('teja_bil', 0xa8483a, 0.7), 0, Y - D / 2, Y + D / 2, 8.5, W, 4.0, cumbrera='x')
    # Los hastiales de curvas (escalonados) con el ojo de buey.
    for s in (-1, 1):
        for (w, z0, h) in ((6.0, 8.5, 2.6), (4.4, 11.1, 1.2), (2.6, 12.3, 1.0)):
            caja(l, s * 10, yf - 0.4, z0, w, 0.8, h)
            caja(piedra(), s * 10, yf - 0.45, z0 + h, w + 0.3, 0.9, 0.2)
        cil(piedra(), s * 10, yf - 0.85, 10.3, 0.75, 0.1, 16, eje='Y')
        cil(cristal(), s * 10, yf - 0.92, 10.3, 0.55, 0.06, 16, eje='Y')
    for x in (-14, -10, -6, 6, 10, 14):
        caja(cristal(), x, yf - 0.05, 0.9, 2.4, 0.1, 3.4)
        cil(l, x, yf - 0.06, 4.3, 1.4, 0.1, 14, eje='Y')
        cil(cristal(), x, yf - 0.1, 4.3, 1.15, 0.1, 14, eje='Y')
    puerta(0, 0.8, 3.0, 3.6, y=yf - 0.06, color=0x4a2e1a, marco=piedra())
    caja(madera_o(), 0, yf - 2.2, 5.6, 26, 3.6, 0.25)
    for x in (-12, -6, 0, 6, 12):
        cil(madera_o(), x, yf - 3.8, 0, 0.12, 5.6, 8)
    caja(negro(), 0, yf - 0.4, 6.4, 13, 0.2, 1.1)
    texto(mat('letras_np_bil', 0xf2e8c8, 0.4), 'NORTHERN PACIFIC', 0, yf - 0.55, 6.95, tam=0.75, prof=0.05)

def first_interstate():
    """La torre First Interstate (la más alta de Montana): 20 plantas de
    hormigón claro con las franjas de cristal oscuro, el remate escalonado y
    el letrero arriba."""
    Y = 12
    W, D, H = 24.0, 20.0, 80.0
    yf = Y - D / 2
    h = mat('hormigon_fi_bil', 0xd8d0c0, 0.6)
    caja(h, 0, Y, 0, W, D, H)
    for k in range(9):
        x = -10 + k * 2.5
        caja(mat('franja_fi_bil', 0x2a3a4a, 0.2), x, yf - 0.05, 4.5, 1.4, 0.1, H - 8)
    caja(cristal(), 0, yf - 0.06, 0.3, W - 2, 0.1, 4.0)
    caja(h, 0, Y, H, W - 3, D - 3, 3.0)
    caja(h, 0, Y, H + 3, W - 7, D - 7, 2.5)
    caja(mat('remate_fi_bil', 0x2a3a4a, 0.3), 0, yf - 0.1, H - 3, W + 0.2, 0.3, 2.4)
    texto(mat('letras_fi_bil', 0xf6f4ee, 0.3), 'FIRST INTERSTATE', 0, yf - 0.3, H - 1.8, tam=1.3, prof=0.06)
    caja(piedra(), 0, yf - 3, 0, W + 6, 6, 0.3)

def moss_mansion():
    """La mansión Moss (1903): arenisca roja, el gran arco de la entrada, las
    ventanas de piedra, el tejado a cuatro aguas con buhardillas y las
    chimeneas, detrás de su verja y su jardín."""
    Y = 13
    W, D, H = 20.0, 14.0, 10.0
    yf = Y - D / 2
    r = arenisca_r()
    caja(r, 0, Y, 0, W, D, H)
    caja(r, 0, yf - 1.2, 0, 7, 2.4, H + 1.5)
    cil(r, 0, yf - 2.45, 2.0, 2.4, 0.2, 16, eje='Y')
    caja(mat('hueco_bil', 0x2a1a14, 0.8), 0, yf - 2.42, 0.3, 3.4, 0.05, 2.0)
    cil(mat('hueco_bil', 0x2a1a14, 0.8), 0, yf - 2.47, 2.3, 1.7, 0.06, 16, eje='Y')
    for x in (-7, -4, 4, 7):
        for z in (1.5, 6.0):
            ventana(x, z, 1.4, 2.6, y=yf, marco=piedra(), cristal=cristal())
    for z in (6.0, 9.0):
        ventana(0, z, 1.6, 1.8, y=yf - 2.4, marco=piedra(), cristal=cristal())
    o = cil(mat('tejado_moss_bil', 0x3a3e46, 0.6), 0, Y, H, W * 0.74, 6.0, 4, r2=W * 0.18)
    o.rotation_euler = (0, 0, math.pi / 4)
    o.scale = (1.0, D / W, 1)
    for x in (-6, 6):
        caja(r, x, yf + 1.4, H + 0.5, 2.0, 1.6, 2.2)
        fronton(r, x, yf + 0.6, H + 2.7, 2.0, 1.0, 1.6)
        caja(cristal(), x, yf + 0.55, H + 0.9, 1.0, 0.05, 1.2)
    for x in (-8, 8):
        caja(r, x, Y + 3, H, 1.2, 1.2, 6.5)
    caja(hierba(), 0, yf - 5, -0.05, W + 6, 10, 0.06)
    for k in range(13):
        cil(hierro(), -12 + k * 2, yf - 9.5, 0, 0.05, 1.6, 4)
    caja(hierro(), 0, yf - 9.5, 1.4, 24, 0.06, 0.06)

# ================================================================ cruzan la calle
def skypoint():
    """El Skypoint: la marquesina de acero que cubre el cruce del centro de
    Billings: cuatro columnas inclinadas y la gran vela de chapa clara con
    las luces por debajo."""
    a = mat('acero_sky_bil', 0x9aa4ae, 0.35)
    for sx in (-1, 1):
        for sy in (-1, 1):
            rama(a, (sx * 8.4, sy * 3.0, 0), (sx * 7.0, sy * 4.6, 11.0), 0.35, 0.25, 10)
    vela = mat('vela_sky_bil', 0xe8ecf0, 0.4)
    me_z = 11.0
    panel(vela, (-9, -5.5, me_z + 1.4), (9, -5.5, me_z), (9, 5.5, me_z + 1.4), (-9, 5.5, me_z + 2.4), 0.25)
    bomb = luz('bombilla_sky_bil', 0xfff0c0, 1.3)
    for x in range(-7, 8, 2):
        for y in (-3, 0, 3):
            esfera(bomb, x, y, me_z + 0.5 - 0.08 * x, 0.12, 1)
    for sx in (-1, 1):
        caja(a, sx * 7.0, 0, me_z - 0.1, 0.4, 9.6, 0.4)

# ================================================================ el arreo
def pradera_arreo():
    """La pradera del Gran Arreo de Montana (momento estrella, al aire
    libre): el camino de tierra del ganado, la hierba seca a los lados, las
    vallas de troncos, vacas pastando, vaqueros a caballo, álamos amarillos,
    el río Yellowstone a la derecha, las Rimrocks a la izquierda, pacas,
    un molino y los arcos de SALIDA y META del arreo.
    Cruza la calle: el origen en el centro y la calle a lo largo de y."""
    L = 420
    caja(tierra(), 0, 0, -0.2, 12, L, 0.2)
    for k in range(int(L / 7)):
        caja(mat('huellas_bil', 0x8a6a46, 0.95), -4 + (k * 5 % 9), -L / 2 + 3 + k * 7, -0.01, 0.5, 0.35, 0.01)
    for s in (-1, 1):
        caja(hierba(), s * 26, 0, -0.21, 40, L, 0.2)
    # Las vallas de troncos, lejos del camino (entre medias caben los corrales
    # a los que se lleva a las vacas, que pone el juego).
    for s in (-1, 1):
        m = gris_madera()
        for k in range(int(L / 4)):
            cil(m, s * 12.6, -L / 2 + 2 + k * 4, 0, 0.1, 1.4, 6)
        for z in (0.65, 1.2):
            cil(m, s * 12.6, 0, z, 0.07, L, 6, eje='Y')
    # El río Yellowstone a la derecha, con su orilla.
    caja(mat('rio_bil', 0x4a7aa8, 0.15), 30, 0, -0.15, 16, L, 0.1)
    for s in (-1, 1):
        caja(mat('orilla_bil', 0xc8b48a, 0.9), 30 + s * 8.6, 0, -0.18, 1.6, L, 0.12)
    # Las Rimrocks a la izquierda.
    est = mat_franjas('estratos_bil', 0xd8b47a, 0xb88a56, 9, eje='Z', z0=0, alto=22)
    for k in range(int(L / 20)):
        y = -L / 2 + 10 + k * 20
        h = 16 + 5 * math.sin(k * 1.3)
        caja(est, -44 - 3 * math.sin(k * 2.1), y, 0, 10, 21, h)
        caja(mat('roca_arriba_bil', 0x9a7a4a, 0.9), -44 - 3 * math.sin(k * 2.1), y, h, 10.4, 21.4, 0.5)
        if k % 2:
            pino(-42, y + 3, 5 + k % 3, z=h + 0.4)
    # Álamos, vacas pastando, vaqueros, pacas y el molino.
    for k in range(int(L / 18)):
        y = -L / 2 + 9 + k * 18
        alamo(21 + (k * 7 % 5), y, 8 + (k % 3), k)
        if k % 3 == 0:
            alamo(-19 - (k * 5 % 6), y + 6, 7 + (k % 2) * 2, k + 1)
    colores = [0x3a2a22, 0x7a4a2a, 0x1c1c20, 0x9a6a3a]
    for k in range(int(L / 14)):
        y = -L / 2 + 6 + k * 14
        s = 1 if k % 2 else -1
        vaca(s * (15 + (k * 3 % 5)), y, mira=-s if k % 3 else s, c=colores[k % 4])
    for k in range(int(L / 60)):
        y = -L / 2 + 25 + k * 60
        s = -1 if k % 2 else 1
        vaquero_caballo(s * 14.0, y, mira=1 if s < 0 else -1, camisa=[0xc8202a, 0x2a5ab8, 0xf2c21a][k % 3])
    for k in range(int(L / 50)):
        y = -L / 2 + 40 + k * 50
        cil(mat('paca_bil', 0xe0c070, 0.9), -15, y, 0.75, 0.75, 1.3, 14, eje='X')
        cil(mat('paca_bil', 0xe0c070, 0.9), -15, y + 1.6, 0.75, 0.75, 1.3, 14, eje='X')
    for y in (-L / 2 + 120, L / 2 - 110):
        for sx in (-1, 1):
            rama(gris(), (15 + sx * 1.2, y - 1.2, 0), (15 + sx * 0.3, y - 0.3, 9), 0.08, 0.06, 4)
            rama(gris(), (15 + sx * 1.2, y + 0.6, 0), (15 + sx * 0.3, y + 0.3, 9), 0.08, 0.06, 4)
        for k in range(12):
            a = k * math.tau / 12
            rama(mat('aspa_bil', 0xd8dce0, 0.5), (15, y - 0.4, 9.5), (15 + math.cos(a) * 2.2, y - 0.4, 9.5 + math.sin(a) * 2.2), 0.05, 0.12, 4)
        cil(gris(), 15, y + 0.6, 9.5, 0.1, 2.0, 6, eje='Y')
    for (y, txt) in ((-L / 2 + 1, 'GREAT MONTANA CATTLE DRIVE'), (L / 2 - 1, 'CORRALES')):
        for s in (-1, 1):
            cil(madera(), s * 6.6, y, 0, 0.32, 6.4, 8)
        cil(madera(), 0, y, 5.8, 0.3, 13.8, 8, eje='X')
        caja(madera_o(), 0, y, 4.3, 11.0 if len(txt) > 12 else 6.0, 0.14, 1.1)
        texto(amarillo(), txt, 0, y - 0.1, 4.85, tam=0.55 if len(txt) > 12 else 0.75, prof=0.04)

# ================================================================ obstáculos
def oso_pardo():
    """El oso pardo (grizzly): marrón, grande, con la giba de los hombros.
    Mira al jugador con la cabeza en el origen y el cuerpo hacia atrás (en el
    juego se pone de pie: entonces hay que agacharse, hacerse el muerto)."""
    oso(mat('pardo_bil', 0x7a5232, 0.8), mat('hocico_pardo_bil', 0xa87a50, 0.8), 0, 0, 0, 1.0, giba=True)

def oso_negro():
    """El oso negro: más pequeño, negro con el hocico marrón claro (en el
    juego se salta por encima: hacerse grande)."""
    oso(mat('negro_oso_bil', 0x24221f, 0.75), mat('hocico_negro_bil', 0xb8946a, 0.8), 0, 0, 0, 0.72)

def _corral(lado):
    """Un corral de troncos al lado de la calle con la puerta abierta hacia
    ella (lado 1: a la derecha, la puerta mira a -x; -1: a la izquierda), con
    vacas dentro y el letrero CORRAL con la flecha. La puerta está en el
    origen."""
    m = gris_madera()
    s = lado
    W, D = 5.0, 6.0
    x1 = s * W
    # Los cuatro lados; el de la calle con el hueco de la puerta (2,6 m).
    for (xa, xb, y) in ((0, x1, -D / 2), (0, x1, D / 2)):
        a, b = min(xa, xb), max(xa, xb)
        valla_rancho(a, b, y, 1.4)
    for (x, y0, y1) in ((x1, -D / 2, D / 2), (0, -D / 2, -1.3), (0, 1.3, D / 2)):
        n = max(1, int((y1 - y0) / 2))
        for k in range(n + 1):
            cil(m, x, y0 + k * (y1 - y0) / n, 0, 0.1, 1.4, 6)
        for z in (0.63, 1.19):
            cil(m, x, (y0 + y1) / 2, z, 0.07, y1 - y0, 6, eje='Y')
    # La puerta abierta (girada hacia fuera) y el suelo de paja.
    caja(m, 0, -1.3 - 1.25, 0.35, 0.1, 2.5, 0.12)
    caja(m, 0, -1.3 - 1.25, 0.95, 0.1, 2.5, 0.12)
    caja(mat('paja_bil', 0xd8b860, 0.95), x1 / 2, 0, 0, W - 0.3, D - 0.3, 0.05)
    vaca(x1 * 0.55, 1.2, mira=-s, c=0x7a4a2a)
    vaca(x1 * 0.7, -1.4, mira=s, c=0x1c1c20)
    # El letrero, que mira al jugador, con la flecha hacia la puerta.
    cil(madera_o(), x1 * 0.3, -D / 2 - 0.2, 0, 0.1, 2.9, 6)
    caja(amarillo(), x1 * 0.3, -D / 2 - 0.3, 2.0, 2.4, 0.1, 0.9)
    texto(negro(), 'CORRAL', x1 * 0.3, -D / 2 - 0.36, 2.45, tam=0.45, prof=0.02)
    # La flecha (apunta hacia la puerta, al lado de la calle).
    fl = mat('flecha_corral_bil', 0xc8202a, 0.5)
    caja(fl, x1 * 0.3 + s * 0.15, -D / 2 - 0.4, 3.0, 1.1, 0.06, 0.25)
    me = bpy.data.meshes.new('punta')
    import bmesh as _bm
    bm = _bm.new()
    xp = x1 * 0.3 - s * 0.45
    vs = [bm.verts.new((xp, -D / 2 - 0.44, 2.8)), bm.verts.new((xp, -D / 2 - 0.44, 3.45)), bm.verts.new((xp - s * 0.55, -D / 2 - 0.44, 3.125))]
    bm.faces.new(vs if s < 0 else vs[::-1])
    bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new('punta', me)
    bpy.context.scene.collection.objects.link(o)
    sd = o.modifiers.new('g', 'SOLIDIFY'); sd.thickness = 0.06
    bpy.context.view_layer.objects.active = o
    bpy.ops.object.modifier_apply(modifier='g')
    from comun import _poner
    _poner(o, fl)

def corral_der():
    """El corral a la derecha de la calle."""
    _corral(1)

def corral_izq():
    """El corral a la izquierda de la calle."""
    _corral(-1)

def cartel_montana():
    """La pancarta de España (agacharse): MONTANA = MONTAÑA."""
    for x in (-1.25, 1.25):
        cil(madera(), x, 0, 0, 0.07, 2.75, 8)
    caja(bandera_es('pancarta_es_obst_bil', 1.5, 1.2), 0, 0, 1.5, 2.4, 0.05, 1.2)
    texto(negro(), 'MONTANA', 0, -0.035, 2.15, tam=0.3, prof=0.02)
    texto(blanco(), '= MONTAÑA', 0, -0.035, 1.7, tam=0.24, prof=0.02)

def tronco_caido():
    """Un pino caído atravesado (se salta): el tronco con la corteza, los
    muñones de las ramas y el corte claro."""
    t = mat('corteza_bil', 0x5a4030, 0.9)
    cil(t, 0, 0, 0.32, 0.32, 2.1, 12, eje='X')
    for s in (-1, 1):
        cil(mat('corte_bil', 0xd8b888, 0.8), s * 1.06, 0, 0.32, 0.29, 0.03, 12, eje='X')
    for (x, a) in ((-0.5, 0.6), (0.3, -0.5), (0.7, 0.4)):
        rama(t, (x, 0, 0.5), (x + 0.15, 0.1, 0.5 + 0.35), 0.06, 0.03, 6)
    esfera(pino_m(), -0.85, 0.15, 0.55, 0.28, 1, esc=(1, 1, 0.6))

def remolque_ganado():
    """El remolque del ganado (no se pasa): de aluminio con las rendijas por
    las que se ven las vacas, el cuello de cisne delante. Mira al jugador y
    el morro está en el origen (el resto, hacia atrás), de 5 m."""
    al = mat('aluminio_bil', 0xc8ccd0, 0.3)
    Y = 2.75
    caja(al, 0, Y, 0.45, 2.1, 4.5, 2.0)
    caja(al, 0, 0.5, 1.45, 1.6, 1.0, 0.9)
    caja(hierro(), 0, 0.4, 0.45, 0.2, 0.8, 1.0)
    for k in range(4):
        caja(mat('rendija_bil', 0x2a2420, 0.8), 0, Y, 1.55 + k * 0.22, 2.12, 4.3, 0.08)
    for s in (-1, 1):
        for y in (Y - 1.0, Y + 0.5):
            cil(negro(), s * 1.0, y, 0.38, 0.38, 0.28, 14, eje='X')
    caja(al, 0, 0.5, 2.35, 1.7, 1.1, 0.06)
    caja(rojo(), 0, 0.5 - 0.52, 0.55, 1.6, 0.04, 0.12)
    for s in (-1, 1):
        caja(mat('piloto_bil', 0xff5030, 0.3), s * 0.8, 0.5 - 0.52, 0.75, 0.18, 0.03, 0.1)

PIEZAS = {
    'rims_billings':    (rims_billings,    'billings',   dict(lado=2048, bisel=0.0)),
    'billings_depot':   (billings_depot,   'billings',   dict(lado=1024, bisel=0.0)),
    'first_interstate': (first_interstate, 'billings',   dict(lado=1024, bisel=0.0)),
    'moss_mansion':     (moss_mansion,     'billings',   dict(lado=1024, bisel=0.0)),
    'skypoint':         (skypoint,         'billings',   dict(lado=1024, bisel=0.0, suelo=False)),
    'pradera_arreo':    (pradera_arreo,    'billings',   dict(lado=2048, bisel=0.0, suelo=False)),
    'oso_pardo':        (oso_pardo,        'obstaculos', dict(lado=256, bisel=0.0)),
    'oso_negro':        (oso_negro,        'obstaculos', dict(lado=256, bisel=0.0)),
    'corral_der':       (corral_der,       'obstaculos', dict(lado=512, bisel=0.0)),
    'corral_izq':       (corral_izq,       'obstaculos', dict(lado=512, bisel=0.0)),
    'cartel_montana':   (cartel_montana,   'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
    'tronco_caido':     (tronco_caido,     'obstaculos', dict(lado=256, bisel=0.0)),
    'remolque_ganado':  (remolque_ganado,  'obstaculos', dict(lado=256, bisel=0.0)),
}

correr(PIEZAS)
