# El metro de Nueva York: el momento estrella del nivel 1 (07/11/2026).
#
#   blender -b -P blender/metro.py -- [pieza ...] [--rapido] [--luces]
#
# Lo que eligió Isidro:
#   · primero se corre por las vías (trenes de frente, vagones parados con
#     rampa y torniquetes) y luego por el techo del tren
#   · junto a la biblioteca: la estación 5 Av, 300 m (de 772 a 1082)
#   · estación antigua: azulejos blancos, el «5 AV» en mosaico, columnas
#     verdes, trenes plateados y luz cálida y fija
#   · se entra por una boca a ras de calle con farolas verdes
#
# La estación y los túneles cruzan la calle de fachada a fachada (como las
# pasarelas de Des Moines): origen en el centro de la calle y en el centro de
# su largo, x de lado a lado (de -11.75 a 11.75) y +y hacia delante. El techo
# va a 11 m: la cámara va a unos 7 m (8,9 en el techo del tren).
#
# Los trenes, los torniquetes y el cartel son obstáculos (carpeta obstaculos):
# caben en un carril, miran al jugador por -y y empiezan en y = 0.

import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import *

ANCHO_CALLE = 11.75          # de la línea de fachadas al centro
TECHO = 11.0
CARRILES = (-2.2, 0.0, 2.2)
VIA = 3.7                    # las vías llegan hasta aquí; después, el andén
TUNEL = 4.6                  # pared del túnel
PARED = 8.3                  # pared de la estación: lo que sobresale de las fachadas (a 11,5) llega hasta 8,5

# ---------------------------------------------------------------- materiales
def azulejo():   return mat_bloques('azulejo_metro', 0xf3efe4, 0xd9d2c2, ancho=0.3, alto=0.15, grosor=0.008, variacion=1.02)
def mosaico():   return mat('mosaico_granate', 0x7a2e2a, 0.5)
def ocre():      return mat('mosaico_ocre', 0xd9a441, 0.4)
def verde():     return mat('verde_columna', 0x2f6a4c, 0.45)
def acero():     return mat('acero_metro', 0x4c4f55, 0.45)
def techo_m():   return mat('techo_metro', 0x34353a, 0.8)
def balasto():   return mat('balasto', 0x4b4844, 0.95)
def traviesa():  return mat('traviesa', 0x3d342d, 0.9)
def rail():      return mat('rail', 0xb5bac0, 0.25)
def anden():     return mat_bloques('anden_metro', 0xbdb6a8, 0xaba395, ancho=1.2, alto=1.2, grosor=0.01, variacion=1.02)
def amarillo():  return mat('borde_anden', 0xf2c230, 0.5)
def hormigon():  return mat_bloques('hormigon_tunel', 0x6b665f, 0x5d5852, ancho=2.4, alto=1.2, grosor=0.01, variacion=1.04)
def negro():     return mat('negro_metro', 0x1d1f25, 0.4)
def blanco():    return mat('blanco_metro', 0xfbf9f3, 0.5)
def morado():    return mat('morado_7', 0x9a3aa8, 0.4)
def caliza():    return mat_bloques('caliza_boca', 0xe4d7bd, 0xd0c1a3, ancho=1.6, alto=0.55, grosor=0.012, variacion=1.03)
def lampara():   return luz('lampara_metro', 0xffd9a0, 1.6)
def plata():     return mat('plata_tren', 0xc7ccd2, 0.25)
def cristal():   return mat('cristal_tren', 0x2c3e55, 0.15)

def texto_pared(m, cadena, x, y, z, tam, lado):
    """Letras en una pared lateral: lado 1 para la pared de la derecha (miran a -x), -1 para la de la izquierda."""
    o = texto(m, cadena, 0, 0, 0, tam=tam, prof=0.02)
    o.rotation_euler = (math.pi / 2, 0, -lado * math.pi / 2)
    o.location = (x, y, z)
    return o

def bala_7(x, y, z, r=0.32, eje='Y', lado=1):
    """El círculo morado con el 7 (la línea que para en 5 Av)."""
    cil(morado(), x, y, z, r, 0.03, 20, eje=eje)
    if eje == 'Y':
        texto(blanco(), '7', x, y - 0.02, z, tam=r * 1.3, prof=0.01)
    else:
        texto_pared(blanco(), '7', x + lado * 0.02, y, z, r * 1.3, lado)

def vias(largo, ancho=VIA):
    """Balasto, traviesas (poco contraste: rayas finas en el suelo marean) y raíles."""
    caja(balasto(), 0, 0, 0, ancho * 2, largo, 0.1)
    n = int(largo / 1.5)
    for xc in CARRILES:
        for k in range(n):
            caja(traviesa(), xc, -largo / 2 + 0.75 + k * 1.5, 0.1, 1.9, 0.26, 0.05)
        for s in (-1, 1):
            caja(rail(), xc + s * 0.72, 0, 0.1, 0.08, largo, 0.13)

def lamparas_techo(y, xs, z=TECHO - 0.75):
    for x in xs:
        caja(acero(), x, y, z + 0.18, 0.08, 0.08, 0.57)
        caja(lampara(), x, y, z, 0.9, 0.3, 0.18)


# ---------------------------------------------------------------- la estación
def metro_estacion():
    """Un trozo de 30 m de la estación 5 Av: tres vías, los andenes a los
    lados, paredes de azulejo blanco con la franja de mosaico y el «5 AV»,
    columnas verdes, vigas de acero y lámparas cálidas."""
    L = 30.0
    vias(L)
    W = PARED
    for s in (-1, 1):
        # El andén (a 1 m) con el borde amarillo y la cara oscura hacia las vías.
        caja(anden(), s * (VIA + (W - VIA) / 2), 0, 0, W - VIA, L, 1.0)
        caja(amarillo(), s * (VIA + 0.3), 0, 1.0, 0.6, L, 0.012)
        caja(mat('cara_anden', 0x57524b, 0.8), s * (VIA + 0.01), 0, 0.1, 0.02, L, 0.9)
        # La pared: azulejo, la franja de mosaico con borde ocre y el «5 AV».
        caja(azulejo(), s * (W + 0.1), 0, 1.0, 0.2, L, TECHO - 1.0)
        caja(mosaico(), s * (W - 0.02), 0, 3.8, 0.04, L, 0.7)
        caja(ocre(), s * (W - 0.03), 0, 3.72, 0.05, L, 0.08)
        caja(ocre(), s * (W - 0.03), 0, 4.5, 0.05, L, 0.08)
        for y in (-7.5, 7.5):
            caja(mosaico(), s * (W - 0.04), y, 2.2, 0.06, 4.2, 1.4)
            caja(ocre(), s * (W - 0.05), y, 2.15, 0.07, 4.4, 0.08)
            caja(ocre(), s * (W - 0.05), y, 3.55, 0.07, 4.4, 0.08)
            texto_pared(blanco(), '5 AV', s * (W - 0.08), y, 2.9, 0.9, s)
        # Columnas verdes (dos filas) y bancos.
        for y in (-11.25, -3.75, 3.75, 11.25):
            for x in (5.0, 7.0):
                caja(verde(), s * x, y, 1.0, 0.36, 0.36, TECHO - 1.0)
                caja(verde(), s * x, y, 1.0, 0.6, 0.6, 0.25)
                caja(verde(), s * x, y, TECHO - 0.6, 0.6, 0.6, 0.25)
        for y in (0.0,):
            caja(mat('banco_madera', 0x8a5a34, 0.6), s * 6.0, y, 1.4, 0.5, 2.6, 0.1)
            for dy in (-1.1, 1.1):
                caja(acero(), s * 6.0, y + dy, 1.0, 0.4, 0.08, 0.4)
        # Los carteles colgados sobre el andén.
        for y in (-7.5, 7.5):
            caja(negro(), s * 6.0, y, 5.6, 2.4, 0.08, 0.7)
            texto(blanco(), '5 Av', s * 6.0 - 0.35, y - 0.05, 5.95, tam=0.38, prof=0.01)
            bala_7(s * 6.0 + 0.8, y - 0.06, 5.95, 0.24)
            for dx in (-1.0, 1.0):
                caja(acero(), s * 6.0 + dx, y, 6.3, 0.04, 0.04, TECHO - 6.3)
    # El techo, las vigas y las lámparas.
    caja(techo_m(), 0, 0, TECHO, W * 2 + 0.4, L, 0.4)
    for y in (-11.25, -3.75, 3.75, 11.25):
        caja(acero(), 0, y, TECHO - 0.6, W * 2, 0.35, 0.6)
        lamparas_techo(y + 1.6, (-6.0, -2.2, 2.2, 6.0))


# ---------------------------------------------------------------- el túnel
def tunel(L, salida=False):
    """Túnel de vías: paredes de hormigón a 4,6 m, pilares de acero negros,
    cables y lámparas pequeñas. En los extremos, un muro que cierra el hueco
    hasta la línea de fachadas (por si al lado va la estación, más ancha)."""
    vias(L, TUNEL)
    for s in (-1, 1):
        caja(hormigon(), s * (TUNEL + 0.15), 0, 0, 0.3, L, TECHO)
        for k in range(int(L / 4)):
            y = -L / 2 + 2 + k * 4
            caja(negro(), s * (TUNEL - 0.12), y, 0, 0.24, 0.3, TECHO)
        for z in (1.6, 1.85, 2.1):
            cil(mat('cable', 0x26272b, 0.6), s * (TUNEL - 0.05), 0, z, 0.05, L, 8, eje='Y')
        for k in range(int(L / 8)):
            y = -L / 2 + 4 + k * 8
            caja(lampara(), s * (TUNEL - 0.08), y, 4.2, 0.12, 0.5, 0.25)
        # Los muros de los extremos (de 4,6 a la fachada).
        for y in (-L / 2 + 0.15, L / 2 - 0.15):
            caja(hormigon(), s * (TUNEL + (ANCHO_CALLE - TUNEL) / 2 + 0.15), y, 0, ANCHO_CALLE - TUNEL + 0.3, 0.3, TECHO)
    caja(techo_m(), 0, 0, TECHO, TUNEL * 2 + 0.6, L, 0.4)
    for k in range(int(L / 6)):
        caja(acero(), 0, -L / 2 + 3 + k * 6, TECHO - 0.5, TUNEL * 2, 0.3, 0.5)
    if salida:
        # La salida: el marco de piedra por dentro y la luz del día entrando.
        y = L / 2 - 0.4
        for s in (-1, 1):
            caja(caliza(), s * (TUNEL - 0.3), y, 0, 0.6, 0.8, TECHO)
        caja(caliza(), 0, y, TECHO - 1.0, TUNEL * 2, 0.8, 1.0)

def metro_tunel():  tunel(24.0)
def metro_salida(): tunel(8.0, salida=True)


# ---------------------------------------------------------------- la boca
def farola_globo(x, y):
    """La farola de las bocas de metro de Nueva York: poste de hierro verde y
    el globo verde encendido (abierto las 24 horas)."""
    hierro = mat('hierro_verde', 0x24503a, 0.5)
    cil(hierro, x, y, 0, 0.16, 0.4, 12)
    cil(hierro, x, y, 0.4, 0.07, 3.0, 10)
    cil(hierro, x, y, 3.3, 0.14, 0.12, 12)
    esfera(luz('globo_verde', 0x3fc060, 0.9), x, y, 3.7, 0.36, 2)
    cil(hierro, x, y, 4.02, 0.08, 0.18, 10, r2=0.02)

def metro_boca():
    """La boca (08/11 (2)). Isidro: «aparecen tuneles ... sin ningún sentido».
    Antes era una fachada suelta del ancho de la calle. Ahora es un edificio
    de estación de lado a lado de la avenida, como Grand Central al final de
    Park Avenue: 80 m de ancho y 26 de alto, de piedra, con ventanales altos,
    pisos de ventanas, el reloj, la cornisa y fondo hacia atrás (levels.js
    quita los edificios de los lados). El hueco del túnel, el letrero
    «SUBWAY» y «5 AV», el 7 morado y las farolas de globo verde como antes.
    Por dentro, 8 m de túnel ya con azulejo."""
    D = 8.0
    y0 = -D / 2
    W = 40.0
    piedra = caliza()
    ventanas = mat_ventanas('ventanas_terminal', 0x3a4a5e, 0xe4d7bd, paso_x=2.4, paso_z=3.0, hueco_x=1.4, hueco_z=1.9)
    for s in (-1, 1):
        caja(piedra, s * (TUNEL + (W - TUNEL) / 2), y0 + 0.6, 0, W - TUNEL, 1.2, TECHO)
        caja(ventanas, s * (TUNEL + (W - TUNEL) / 2), y0 + 0.6, TECHO, W - TUNEL, 1.2, 15)
        for k in range(3):                                   # los ventanales altos
            x = s * (10.0 + k * 9.5)
            caja(mat('ventanal_term', 0x2c3e55, 0.2), x, y0 - 0.02, 1.4, 4.4, 0.1, 8.2)
            for j in range(1, 4):
                caja(mat('marco_term', 0x3a3a3e, 0.4), x - 2.2 + j * 1.1, y0 - 0.06, 1.4, 0.12, 0.1, 8.2)
            caja(mat('marco_term', 0x3a3a3e, 0.4), x, y0 - 0.06, 5.4, 4.4, 0.1, 0.12)
        caja(piedra, s * W, y0 + 10.6, 0, 1.2, 20, 26)        # el edificio sigue hacia atrás
    caja(piedra, 0, y0 + 0.6, TECHO, TUNEL * 2, 1.2, 5)
    caja(ventanas, 0, y0 + 0.6, TECHO + 5, TUNEL * 2, 1.2, 10)
    caja(mat('cornisa_boca', 0xd6c6a6, 0.5), 0, y0 + 0.3, TECHO - 0.3, W * 2 + 0.4, 1.8, 0.6)
    caja(mat('cornisa_boca', 0xd6c6a6, 0.5), 0, y0 + 0.3, 25.6, W * 2 + 0.6, 2.0, 0.8)
    caja(mat('tejado_term', 0x3d6a5a, 0.6), 0, y0 + 10.6, 26.2, W * 2, 20, 0.5)
    caja(mat('zocalo_boca', 0x8f8a80, 0.6), 0, y0 + 0.5, 0, W * 2, 1.4, 0.7)
    # El reloj, encima del letrero.
    cil(ocre(), 0, y0 + 0.02, 19.2, 1.9, 0.15, 32, eje='Y')
    cil(mat('esfera_reloj', 0xf4eedc, 0.4), 0, y0 - 0.08, 19.2, 1.6, 0.15, 32, eje='Y')
    caja(negro(), 0, y0 - 0.2, 19.2, 0.1, 0.05, 1.15)
    caja(negro(), 0.4, y0 - 0.2, 19.15, 0.8, 0.05, 0.1)
    # El marco del hueco y el letrero.
    for s in (-1, 1):
        caja(mat('marco_boca', 0x3a3a3e, 0.4), s * (TUNEL + 0.2), y0 - 0.05, 0, 0.4, 0.3, TECHO + 0.4)
    caja(mat('marco_boca', 0x3a3a3e, 0.4), 0, y0 - 0.05, TECHO, TUNEL * 2 + 0.8, 0.3, 0.4)
    caja(mat('letrero_subway', 0x1f3d2e, 0.4), 0, y0 - 0.12, 12.0, 7.6, 0.12, 1.3)
    texto(blanco(), 'SUBWAY', -0.6, y0 - 0.2, 12.65, tam=0.85, prof=0.03)
    bala_7(2.8, y0 - 0.2, 12.65, 0.45)
    caja(mosaico(), 0, y0 - 0.08, 13.7, 4.6, 0.1, 1.2)
    caja(ocre(), 0, y0 - 0.1, 13.62, 4.8, 0.1, 0.08)
    caja(ocre(), 0, y0 - 0.1, 14.9, 4.8, 0.1, 0.08)
    texto(blanco(), '5 AV', 0, y0 - 0.15, 14.3, tam=0.8, prof=0.02)
    # Las farolas de globo verde, a los lados del hueco y en la acera.
    for s in (-1, 1):
        farola_globo(s * 5.4, y0 - 0.6)
        farola_globo(s * 9.6, y0 - 0.6)
        hierro = mat('hierro_verde', 0x24503a, 0.5)
        caja(hierro, s * 7.5, y0 - 0.6, 1.0, 3.6, 0.06, 0.06)
        for k in range(7):
            caja(hierro, s * (5.9 + k * 0.53), y0 - 0.6, 0, 0.04, 0.04, 1.0)
    # Por dentro: paredes de azulejo, techo y las vías.
    vias(D, TUNEL)
    for s in (-1, 1):
        caja(azulejo(), s * (TUNEL + 0.15), 0.6, 0, 0.3, D - 1.2, TECHO)
    caja(techo_m(), 0, 0.6, TECHO, TUNEL * 2 + 0.6, D - 1.2, 0.4)
    lamparas_techo(1.5, (-2.2, 2.2))

def coche_tren(y0, L=11.4, cabina=False, cola=True):
    """Un coche plateado del 7: costados de acero, la franja morada, ventanas
    y puertas, techo claro (por donde se corre) y los bogies debajo. El techo
    va a 2,2 m."""
    W = 2.0
    caja(plata(), 0, y0 + L / 2, 0.45, W, L, 1.6)
    caja(mat('techo_tren', 0xd9dde2, 0.4), 0, y0 + L / 2, 2.05, W - 0.04, L - 0.1, 0.15)
    for s in (-1, 1):
        caja(morado(), s * (W / 2 + 0.01), y0 + L / 2, 0.72, 0.02, L - 0.2, 0.12)
        for k in range(4):
            yv = y0 + 1.4 + k * (L - 2.8) / 3
            caja(cristal(), s * (W / 2 + 0.012), yv, 1.15, 0.02, 1.4, 0.6)
        for yp in (y0 + 3.2, y0 + L - 3.2):
            caja(mat('puerta_tren', 0xaeb4bb, 0.3), s * (W / 2 + 0.015), yp, 0.5, 0.02, 1.2, 1.5)
            caja(cristal(), s * (W / 2 + 0.02), yp, 1.25, 0.02, 0.9, 0.5)
    # Bogies y ruedas.
    for yb in (y0 + 2.0, y0 + L - 2.0):
        caja(negro(), 0, yb, 0.15, 1.7, 2.2, 0.3)
        for s in (-1, 1):
            for dy in (-0.7, 0.7):
                cil(negro(), s * 0.78, yb + dy, 0.28, 0.28, 0.12, 12, eje='X')
    # Los equipos del techo, a los lados (el centro se pisa).
    for s in (-1, 1):
        caja(mat('equipo_techo', 0xaab0b8, 0.4), s * 0.72, y0 + L / 2, 2.2, 0.4, L * 0.6, 0.08)
    if cola:
        # La parte de atrás: puerta de paso, pilotos y el 7.
        caja(mat('testero', 0xb9bfc6, 0.3), 0, y0 + 0.02, 0.45, W - 0.04, 0.04, 1.6)
        caja(cristal(), 0, y0 - 0.01, 1.2, 0.6, 0.02, 0.7)
        for s in (-1, 1):
            caja(mat('piloto_tren', 0xc0262c, 0.3), s * 0.75, y0 - 0.01, 1.7, 0.18, 0.02, 0.12)
        bala_7(0.6, y0 - 0.02, 1.85, 0.16)
    if cabina:
        # La cabina de delante (mirando al jugador): luna, faros y el letrero.
        caja(mat('testero', 0xb9bfc6, 0.3), 0, y0 + 0.02, 0.45, W - 0.04, 0.04, 1.6)
        caja(cristal(), 0, y0 - 0.01, 1.3, W - 0.5, 0.02, 0.55)
        caja(negro(), 0, y0 - 0.01, 1.92, 1.3, 0.02, 0.22)
        texto(mat('letrero_ambar', 0xffb84a, 0.3), 'FLUSHING', -0.2, y0 - 0.03, 2.03, tam=0.12, prof=0.005)
        bala_7(0.55, y0 - 0.03, 2.03, 0.1)
        for s in (-1, 1):
            esfera(luz('faro_tren', 0xfff4d8, 3.0), s * 0.68, y0 - 0.02, 0.75, 0.12, 2)
            caja(mat('piloto_tren', 0xc0262c, 0.3), s * 0.68, y0 - 0.01, 0.55, 0.14, 0.02, 0.08)

def tren():
    """El tren que viene de frente por la vía: dos coches enganchados, la
    cabina mirando al jugador con los faros encendidos."""
    coche_tren(0.0, cabina=True, cola=False)
    caja(negro(), 0, 11.5, 0.6, 1.2, 0.3, 1.4)        # el fuelle entre coches
    coche_tren(11.6)

def vagon():
    """Un coche parado con una rampa apoyada detrás: se sube corriendo y se
    sigue por el techo (como el autobús, pero a 2,2 m)."""
    R = 3.0
    me = bpy.data.meshes.new('rampa_vagon')
    bm = bmesh.new()
    pts = []
    for x in (-0.95, 0.95):
        pts.append([bm.verts.new((x, 0, 0)), bm.verts.new((x, R, 0)), bm.verts.new((x, R, 2.2))])
    a, b = pts
    bm.faces.new(a); bm.faces.new(b[::-1])
    for i in range(3):
        j = (i + 1) % 3
        bm.faces.new((a[j], a[i], b[i], b[j]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new('rampa_vagon', me)
    bpy.context.scene.collection.objects.link(o)
    from comun import _poner
    _poner(o, mat_franjas('rampa_vagon_rayas', 0xffd21a, 0x1d1f25, 9, eje='Y', z0=0, alto=R))
    coche_tren(R)

def coche_metro():
    """Un coche sin rampa, para enganchar detrás del vagón: el techo sigue a 2,2."""
    coche_tren(0.0, cola=False)
    caja(negro(), 0, 11.5, 0.6, 1.2, 0.3, 1.4)

def torniquete():
    """Dos torniquetes de acero con los brazos a la altura de la cintura y
    una barra arriba: se saltan."""
    inox = mat('inox', 0xc4c9cf, 0.25)
    for s in (-1, 1):
        caja(inox, s * 0.62, 0.3, 0, 0.32, 0.9, 0.95)
        caja(negro(), s * 0.62, 0.3, 0.95, 0.34, 0.92, 0.04)
        for k in range(3):
            ang = k * 2 * math.pi / 3
            rama(inox, (s * 0.45, 0.3, 0.85), (s * 0.45 - s * 0.45 * abs(math.cos(ang)), 0.3 + 0.35 * math.sin(ang), 0.85 - 0.25 * (k == 2)), 0.03, 0.03, 6)
    caja(acero(), 0, 0.3, 0.98, 1.8, 0.06, 0.06)
    caja(mat('luz_verde_torno', 0x5fd27a, 0.3), -0.62, 0.0, 0.7, 0.12, 0.02, 0.08)
    caja(mat('luz_roja_torno', 0xd8302c, 0.3), 0.62, 0.0, 0.7, 0.12, 0.02, 0.08)

def cartel_metro():
    """El cartel colgado de la estación («5 Av» y el 7): se pasa agachado.
    Las varillas suben hasta el techo."""
    caja(negro(), 0, 0, 1.3, 1.9, 0.08, 0.7)
    caja(blanco(), 0, -0.045, 1.33, 1.84, 0.01, 0.04)
    texto(blanco(), '5 Av', -0.25, -0.06, 1.68, tam=0.34, prof=0.01)
    bala_7(0.62, -0.06, 1.68, 0.2)
    for dx in (-0.75, 0.75):
        caja(acero(), dx, 0, 2.0, 0.04, 0.04, 10.0)


PIEZAS = {
    'metro_boca':     (metro_boca,     'nueva_york', dict(lado=2048, bisel=0.0, segmentos=2)),
    'metro_estacion': (metro_estacion, 'nueva_york', dict(lado=2048, bisel=0.0, segmentos=2)),
    'metro_tunel':    (metro_tunel,    'nueva_york', dict(lado=1024, bisel=0.0)),
    'metro_salida':   (metro_salida,   'nueva_york', dict(lado=512, bisel=0.0)),
    'tren':           (tren,           'obstaculos', dict(lado=1024)),
    'vagon':          (vagon,          'obstaculos', dict(lado=1024)),
    'coche_metro':    (coche_metro,    'obstaculos', dict(lado=1024)),
    'torniquete':     (torniquete,     'obstaculos', dict(lado=256, bisel=0.0)),
    'cartel_metro':   (cartel_metro,   'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
}

correr(PIEZAS)
