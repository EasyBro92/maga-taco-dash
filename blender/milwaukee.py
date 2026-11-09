# Nivel 12: Milwaukee, Wisconsin (09/11/2026).
#
#   blender -b -P blender/milwaukee.py -- [pieza ...] [--rapido]
#
# Isidro (09/11): «sigue creando más estados, aplica tus propias
# recomendaciones sin preguntas». Se aplicó lo recomendado: final delante del
# museo de arte de Calatrava (las alas blancas junto al lago Míchigan) y tarde
# dorada de otoño. Historia: «Se sube a un camión de la basura con chaleco,
# como hizo de verdad. Quesos».
#   Por Wisconsin Avenue hacia el este, hasta el lago:
#   izquierda:  la iglesia del Gesu (las dos agujas góticas) · el Germania
#               Building (los cuatro cascos de cobre) · el Ayuntamiento (la
#               torre del reloj, de ladrillo rojo)
#   derecha:    el hotel Pfister · el U.S. Bank Center (la torre blanca)
#   en medio:   el puente sobre el río Milwaukee, con el paseo del río abajo y
#               la estatua de bronce del Fonz levantando los pulgares
#   al fondo:   el museo de arte de Calatrava: el puente blanco con su mástil
#               inclinado y las alas (las pone el juego: se abren al llegar)
# Obstáculos (carpeta obstaculos): la rueda de queso que viene rodando, la
# pila de cuñas de queso, el cubo de la basura, las bolsas de basura, el
# cartel de queso colgado (agacharse), el aficionado con el sombrero de queso
# que cruza, la moto de Milwaukee y el camión de la basura (el momento
# estrella: él va de pie encima, con el chaleco).

import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import *
from comun import _poner

def blanco():   return mat('blanco_mke', 0xfbf8f2, 0.5)
def negro():    return mat('negro_mke', 0x1d1f25, 0.4)
def rojo():     return mat('rojo_mke', 0xd52b1e, 0.45)
def azul():     return mat('azul_mke', 0x1f3a7a, 0.45)
def dorado():   return mat('dorado_mke', 0xe0b048, 0.25)
def acero():    return mat('acero_mke', 0xd8dde2, 0.25)
def oscuro():   return mat('ventana_os_mke', 0x2c3440, 0.3)
def cobre():    return mat('cobre_mke', 0x5e9e88, 0.45)
def queso():    return mat('queso_mke', 0xf2b632, 0.55)
def queso_in(): return mat('queso_dentro_mke', 0xf8d468, 0.6)
def agujero():  return mat('agujero_queso', 0xc8901e, 0.7)
def verde_pk(): return mat('verde_packers', 0x203a30, 0.55)
def oro_pk():   return mat('oro_packers', 0xffb612, 0.5)
def ladrillo(): return mat_bloques('ladrillo_mke', 0xa8523a, 0x6e3a2a, ancho=0.3, alto=0.1, grosor=0.012, variacion=1.08)
def crema():    return mat_bloques('ladrillo_crema_mke', 0xe6d6b0, 0xbcae8c, ancho=0.3, alto=0.1, grosor=0.012, variacion=1.05)
def arenisca(): return mat_bloques('arenisca_mke', 0xd8bc8a, 0xb8a070, ancho=0.9, alto=0.45, grosor=0.015, variacion=1.05)
def piedra_g(): return mat_bloques('piedra_gesu', 0x9a917e, 0x7a7262, ancho=0.7, alto=0.35, grosor=0.015, variacion=1.08)

def neumatico(): return mat('neumatico_mke', 0x1e1e22, 0.85)

def rueda(x, y, r=0.3, ancho=0.22, z=None):
    z = r if z is None else z
    cil(neumatico(), x, y, z, r, ancho, 16, eje='X')
    cil(mat('llanta_mke', 0xd3d6da, 0.3), x + (0.12 if x > 0 else -0.12), y, z, r * 0.5, 0.02, 12, eje='X')

def prisma(m, puntos, y0, y1):
    """Prisma de planta `puntos` [(x, z)...] (en el plano xz) de y0 a y1."""
    me = bpy.data.meshes.new('prisma')
    bm = bmesh.new()
    a = [bm.verts.new((x, y0, z)) for (x, z) in puntos]
    b = [bm.verts.new((x, y1, z)) for (x, z) in puntos]
    bm.faces.new(a)
    bm.faces.new(list(reversed(b)))
    n = len(puntos)
    for i in range(n):
        j = (i + 1) % n
        bm.faces.new((a[j], a[i], b[i], b[j]))
    bm.normal_update()
    bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new('prisma', me)
    bpy.context.collection.objects.link(o)
    return _poner(o, m)

def ventana_arco(m, x, y, z, w, h):
    """Ventana de medio punto en una fachada que mira a -y."""
    caja(m, x, y, z, w, 0.12, h - w / 2)
    c = cil(m, x, y, z + h - w / 2, w / 2, 0.12, 12, eje='Y')
    return c

def gotica(m, x, y, z, w, h):
    caja(m, x, y, z, w, 0.12, h)
    fronton(m, x, y - 0.06, z + h, w, w * 0.9, 0.12)

def hastial_escalonado(m, x, y, z, w, h, pasos=4, fondo=0.6):
    """El remate flamenco en escalones (el Ayuntamiento), de cara a -y."""
    for k in range(pasos):
        ww = w * (1 - k / pasos)
        caja(m, x, y, z + k * h / pasos, ww, fondo, h / pasos)

# ================================================================ los edificios
def gesu_church():
    """La iglesia del Gesu (1894), junto a la Universidad Marquette: piedra
    gris y parda, la gran portada gótica, el rosetón y las dos torres con sus
    agujas de 76 m."""
    p = piedra_g()
    os_ = oscuro()
    caja(mat('escalinata_gesu', 0xb8b0a0, 0.8), 0, 2.5, 0, 22, 5, 0.5)
    Y = 20
    # La nave detrás de la fachada.
    caja(p, 0, Y + 6, 0, 18, 34, 22)
    tejado(mat('tejado_gesu', 0x4a5058, 0.6), 0, Y - 10, Y + 23, 22, 18, 8, cumbrera='y')
    # La fachada: el cuerpo central con el hastial y las dos torres.
    caja(p, 0, Y - 9, 0, 14, 4, 24)
    fronton(p, 0, Y - 11, 24, 14, 8, 2)
    for sx in (-1, 1):
        x = sx * 9.5
        caja(p, x, Y - 9, 0, 7, 7, 34)
        for zz in (8, 18, 28):
            gotica(os_, x, Y - 12.55, zz, 1.4, 4.0)
        caja(p, x, Y - 9, 34, 7.6, 7.6, 1.0)
        for (ex, ey) in ((-3.3, -3.3), (3.3, -3.3), (-3.3, 3.3), (3.3, 3.3)):
            cil(p, x + ex, Y - 9 + ey, 35, 0.5, 5, 6, r2=0.05)
        cil(p, x, Y - 9, 35, 3.4, 4, 8).rotation_euler = (0, 0, math.pi / 8)
        cil(mat('aguja_gesu', 0x6e6a62, 0.6), x, Y - 9, 39, 3.3, 37, 8, r2=0.15).rotation_euler = (0, 0, math.pi / 8)
        rama(dorado(), (x, Y - 9, 76), (x, Y - 9, 78.5), 0.08, 0.08, 4)
        rama(dorado(), (x - 0.7, Y - 9, 77.6), (x + 0.7, Y - 9, 77.6), 0.07, 0.07, 4)
    # La portada: tres arcos apuntados y el rosetón encima.
    for (x, w, h) in ((0, 3.8, 7.5), (-4.6, 2.4, 5.5), (4.6, 2.4, 5.5)):
        gotica(mat('puerta_gesu', 0x3a2a20, 0.6), x, Y - 11.05, 0.5, w, h)
    cil(mat('marco_roseton', 0x8a8270, 0.6), 0, Y - 11.1, 15, 3.6, 0.2, 24, eje='Y')
    cil(mat('vidriera_gesu', 0x3a4a8a, 0.2), 0, Y - 11.2, 15, 3.1, 0.12, 24, eje='Y')
    for k in range(8):
        t = k * math.pi / 4
        rama(mat('marco_roseton', 0x8a8270, 0.6), (0, Y - 11.3, 15), (3.1 * math.cos(t), Y - 11.3, 15 + 3.1 * math.sin(t)), 0.12, 0.12, 4)

def germania():
    """El Germania Building (1896): ocho plantas de granito y ladrillo claro
    y, en lo alto, sus cuatro cúpulas de cobre verde con pincho, como los
    cascos del káiser."""
    v = mat_ventanas('ventanas_germania', 0x3e4a56, 0xd8c8a6, paso_x=1.8, paso_z=3.4, hueco_x=1.0, hueco_z=2.0, variacion=1.06)
    g = mat_bloques('granito_germania', 0x8a8478, 0x6a645a, ancho=1.0, alto=0.5, grosor=0.015)
    Y, W, D, H = 11, 40, 22, 36
    caja(v, 0, Y, 0, W, D, H)
    caja(g, 0, Y, 0, W + 0.4, D + 0.4, 6)
    for x in range(-18, 19, 6):
        caja(arenisca(), x, Y - D / 2 - 0.15, 6, 0.8, 0.3, H - 6)
    caja(arenisca(), 0, Y, H, W + 1.2, D + 1.2, 1.0)
    for x in (-15, -5, 5, 15):
        ventana_arco(mat('escaparate_ger', 0x34404c, 0.2), x, Y - D / 2 - 0.25, 0.4, 3.6, 4.6)
    caja(mat('puerta_ger', 0x3a2a20, 0.6), 0, Y - D / 2 - 0.25, 0, 3, 0.2, 3.6)
    texto(dorado(), 'GERMANIA', 0, Y - D / 2 - 0.3, 5.2, tam=0.9, prof=0.05)
    # Los cuatro cascos de cobre.
    for x in (-15, -5, 5, 15):
        cil(arenisca(), x, Y - 6, H + 1, 3.0, 4, 12)
        cil(cobre(), x, Y - 6, H + 5, 3.2, 0.6, 16)
        cupula(cobre(), x, Y - 6, H + 5.6, 3.0, 4.4, lados=20, aros=6)
        cil(cobre(), x, Y - 6, H + 9.8, 0.7, 1.2, 10)
        cil(cobre(), x, Y - 6, H + 11, 0.5, 3.4, 8, r2=0.02)
        for k in range(4):
            t = k * math.pi / 2
            esfera(dorado(), x + 3.0 * math.cos(t), Y - 6 + 3.0 * math.sin(t), H + 5.9, 0.3, 1)

def city_hall_mke():
    """El Ayuntamiento de Milwaukee (1895): renacimiento flamenco, ladrillo
    rojo con arenisca, los remates en escalones y la torre del reloj de 108 m
    con su cúpula de cobre y la linterna."""
    l = ladrillo()
    a = arenisca()
    v = mat_ventanas('ventanas_ch_mke', 0x3a4450, 0xa8523a, paso_x=1.6, paso_z=3.4, hueco_x=0.9, hueco_z=2.0, variacion=1.06)
    Y, W, D, H = 14, 40, 26, 34
    caja(v, 0, Y, 0, W, D, H)
    caja(a, 0, Y, 0, W + 0.4, D + 0.4, 5)
    for z in (12, 23):
        caja(a, 0, Y, z, W + 0.3, D + 0.3, 0.6)
    caja(a, 0, Y, H, W + 0.8, D + 0.8, 0.8)
    for x in (-14, 14):
        hastial_escalonado(l, x, Y - D / 2 + 0.3, H + 0.8, 9, 7, pasos=5)
        caja(a, x, Y - D / 2 - 0.05, H + 2, 1.6, 0.2, 2.4)
    tejado(mat('tejado_ch_mke', 0x7a3a2a, 0.6), 0, Y - D / 2, Y + D / 2, H + 0.8, W, 6, cumbrera='x')
    for x in (-6, 0, 6):
        ventana_arco(mat('puerta_ch', 0x3a2a20, 0.6), x, Y - D / 2 - 0.25, 0, 2.6, 4.4)
    # La torre del reloj, en la esquina de la izquierda (la de delante).
    TX, TY = -12, Y - 7
    caja(l, TX, TY, 0, 12, 12, 74)
    for z in (5, 20, 35, 50, 62):
        caja(a, TX, TY, z, 12.4, 12.4, 0.7)
    for zz in range(8, 60, 7):
        caja(oscuro(), TX, TY - 6.05, zz, 1.4, 0.12, 3.2)
    for (eje, nx, ny) in (('Y', 0, -1), ('X', -1, 0), ('X', 1, 0)):
        cx, cy = TX + nx * 6.1, TY + ny * 6.1
        cil(a, cx, cy, 68, 3.0, 0.2, 24, eje=eje)
        cil(blanco(), cx + nx * 0.1, cy + ny * 0.1, 68, 2.6, 0.2, 24, eje=eje)
        px, py = cx + nx * 0.25, cy + ny * 0.25
        tx, ty = -ny, nx
        rama(negro(), (px, py, 68), (px + 1.0 * tx, py + 1.0 * ty, 68.8), 0.1, 0.08, 4)
        rama(negro(), (px, py, 68), (px - 0.4 * tx, py - 0.4 * ty, 70.1), 0.08, 0.06, 4)
    caja(a, TX, TY, 74, 13, 13, 1.2)
    for sx in (-1, 1):
        for sy in (-1, 1):
            cil(cobre(), TX + sx * 5.6, TY + sy * 5.6, 75.2, 0.9, 6, 8, r2=0.1)
    cil(cobre(), TX, TY, 75.2, 5.6, 8, 8).rotation_euler = (0, 0, math.pi / 8)
    cupula(cobre(), TX, TY, 83.2, 5.4, 7, lados=16, aros=6)
    cil(cobre(), TX, TY, 90, 2.0, 5, 8).rotation_euler = (0, 0, math.pi / 8)
    cil(cobre(), TX, TY, 95, 2.2, 0.5, 8)
    cil(cobre(), TX, TY, 95.5, 1.8, 9, 8, r2=0.06)
    esfera(dorado(), TX, TY, 104.8, 0.45, 1)

def pfister_hotel():
    """El hotel Pfister (1893): ladrillo crema, arcos románicos abajo, su
    marquesina con el nombre y, detrás, la torre redonda de los años sesenta."""
    c = crema()
    v = mat_ventanas('ventanas_pfister', 0x3e4854, 0xe2d2ac, paso_x=1.6, paso_z=3.3, hueco_x=0.9, hueco_z=2.0, variacion=1.05)
    Y, W, D, H = 12, 30, 24, 30
    caja(v, 0, Y, 0, W, D, H)
    caja(c, 0, Y, 0, W + 0.4, D + 0.4, 6)
    caja(arenisca(), 0, Y, H, W + 1, D + 1, 1.2)
    for x in range(-12, 13, 4):
        if abs(x) > 1:
            ventana_arco(mat('arcos_pfister', 0x34404c, 0.2), x, Y - D / 2 - 0.25, 0.6, 2.6, 4.6)
    # La marquesina de la entrada.
    caja(mat('marquesina_pfister', 0x6a1f24, 0.5), 0, Y - D / 2 - 2.0, 3.8, 7, 4, 0.5)
    for x in (-3.3, 3.3):
        cil(dorado(), x, Y - D / 2 - 3.8, 0, 0.1, 3.8, 8)
    texto(dorado(), 'THE PFISTER', 0, Y - D / 2 - 4.05, 4.05, tam=0.55, prof=0.04)
    caja(mat('puerta_pfister', 0x2a2420, 0.5), 0, Y - D / 2 - 0.25, 0, 3, 0.2, 3.6)
    # La torre redonda de detrás.
    tv = mat_ventanas('ventanas_torre_pf', 0x4a5664, 0xd8ccb0, paso_x=1.4, paso_z=3.1, hueco_x=0.8, hueco_z=1.8)
    cil(tv, 4, Y + 18, 0, 10, 72, 24)
    cil(c, 4, Y + 18, 72, 10.4, 1.4, 24)
    texto(mat('letras_torre_pf', 0xc8202e, 0.4), 'PFISTER', 4, Y + 7.6, 68, tam=2.2, prof=0.1)

def us_bank_center():
    """El U.S. Bank Center (1973), el más alto de Wisconsin: 183 m de
    nervios blancos de arriba abajo, con la plaza delante."""
    v = mat_ventanas('nervios_usbank', 0x2e3642, 0xf2f2ee, paso_x=1.5, paso_z=3.6, hueco_x=0.75, hueco_z=3.45, variacion=1.03)
    caja(mat('plaza_usbank', 0xc8c2b6, 0.8), 0, 9, 0, 40, 18, 0.08)
    Y = 26
    caja(v, 0, Y, 0, 34, 24, 183)
    caja(mat('remate_usbank', 0xf0f0ea, 0.4), 0, Y, 183, 34.4, 24.4, 3)
    caja(mat('vestibulo_usbank', 0x5a6676, 0.2), 0, Y - 12.05, 0, 30, 0.1, 6)
    texto(mat('letras_usbank', 0x1f3a7a, 0.4), 'U.S. BANK', 0, Y - 12.15, 7.0, tam=1.4, prof=0.06)
    for x in (-12, 12):
        cil(mat('macetero_usb', 0x8a8478, 0.7), x, 8, 0, 1.4, 0.8, 12)
        esfera(mat('arbusto_usb', 0xc8802e, 0.8), x, 8, 1.6, 1.3, 2, esc=(1, 1, 0.8))

# ================================================================ el puente y el río
L_PUENTE = 50.0
RIO = 18.0          # el agua va de -18 a 18 (a lo largo de la calle)
AGUA_Z = -5.0

def fonz(X, Y, Z):
    """La estatua de bronce del Fonz (la de Happy Days, en el paseo del río):
    chupa de cuero, vaqueros y los dos pulgares arriba. Mira a -y (a quien
    llega por el puente). Un poco más grande que en la realidad, para verla."""
    b = mat('bronce_fonz', 0x7a5a30, 0.35)
    e = 1.3
    P = lambda x, y, z: (X + x * e, Y + y * e, Z + z * e)
    caja(mat('peana_fonz', 0x8a8478, 0.7), X, Y, Z, 1.4, 1.4, 0.35)
    Z += 0.35
    for sx in (-0.12, 0.12):
        cil(b, *P(sx, 0, 0), 0.11 * e, 0.85 * e, 8)
    cil(b, *P(0, 0, 0.82), 0.27 * e, 0.65 * e, 10, r2=0.3 * e)
    esfera(b, *P(0, 0, 1.66), 0.17 * e, 2)
    esfera(b, *P(0, 0.03, 1.78), 0.16 * e, 2, esc=(1, 1, 0.6))
    for sx in (-1, 1):
        rama(b, P(sx * 0.3, 0, 1.4), P(sx * 0.38, -0.3, 1.1), 0.07 * e, 0.06 * e, 6)
        rama(b, P(sx * 0.38, -0.3, 1.1), P(sx * 0.3, -0.42, 1.36), 0.06 * e, 0.05 * e, 6)
        caja(b, *P(sx * 0.3, -0.44, 1.36), 0.06 * e, 0.08 * e, 0.16 * e)

def puente_mke():
    """El puente de Wisconsin Avenue sobre el río Milwaukee: el tablero con
    barandillas de piedra y farolas, el río abajo, el paseo del río en las dos
    orillas con la estatua del Fonz, un barco y almacenes de ladrillo con sus
    letreros pintados. Cruza la calle: el origen en el centro."""
    L = L_PUENTE
    caja(mat('asfalto_puente_mke', 0x4a4c52, 0.8), 0, 0, -0.5, 8.4, L, 0.56)
    for s in (-1, 1):
        caja(mat('acera_puente_mke', 0xc8c2b6, 0.75), s * 6.2, 0, -0.5, 3.6, L, 0.68)
        caja(arenisca(), s * 8.2, 0, -2.6, 0.6, L, 2.2)
        caja(arenisca(), s * 8.2, 0, 0.18, 0.5, L, 0.2)
        caja(arenisca(), s * 8.2, 0, 1.05, 0.6, L, 0.18)
        for k in range(24):
            cil(arenisca(), s * 8.2, -L / 2 + 1 + k * 2.08, 0.38, 0.12, 0.67, 6, r2=0.08)
        for k in range(4):
            y = -15 + k * 10
            cil(negro(), s * 8.2, y, 1.23, 0.1, 4.2, 8)
            esfera(mat('globo_farola_mke', 0xfff2d0, 0.3), s * 8.2, y, 5.7, 0.35, 2)
    for x in (-4.6, 0, 4.6):
        caja(mat('viga_puente_mke', 0x4a5258, 0.5), x, 0, -2.4, 0.5, L, 1.9)
    caja(mat('rio_mke', 0x3a6a5a, 0.15), 0, 0, AGUA_Z - 0.2, 420, 2 * RIO, 0.2)
    for sy in (-1, 1):
        y0 = sy * RIO
        caja(mat('muro_rio_mke', 0x8a8478, 0.8), 0, y0 + sy * 0.5, AGUA_Z, 420, 1.0, -AGUA_Z)
        caja(mat('paseo_rio_mke', 0x9a7a5a, 0.8), 0, y0 - sy * 2.0, AGUA_Z, 420, 4.0, 1.2)
        caja(mat('suelo_orilla_mke', 0xb8b4ac, 0.85), 0, y0 + sy * 3.5, -0.12, 420, 7.0, 0.1)
        for k in range(30):
            x = -150 + k * 10
            if abs(x) < 10:
                continue
            caja(negro(), x, y0 - sy * 3.9, AGUA_Z + 1.2, 0.08, 0.08, 1.0)
        caja(negro(), 0, y0 - sy * 3.9, AGUA_Z + 2.15, 420, 0.06, 0.06)
    # El Fonz, en el paseo de la orilla de enfrente, a la derecha.
    fonz(9.5, RIO - 2.2, AGUA_Z + 1.2)
    # Los almacenes del Third Ward a las orillas, con sus letreros pintados.
    letreros = ('BREW CITY', 'CHEESE CO.', 'SAUSAGE', 'TANNERY', 'MALT HOUSE', 'CUSTARD')
    k = 0
    for sy in (-1, 1):
        for x in (-70, -46, 46, 70):
            y = sy * (RIO + 18)
            w, h = 20, 18 + (k % 3) * 6
            caja(ladrillo() if k % 2 else crema(), x, y, AGUA_Z, w, 18, h - AGUA_Z)
            caja(arenisca(), x, y, h, w + 0.6, 18.6, 0.8)
            for zz in range(2, int(h), 4):
                for xx in range(-8, 9, 3):
                    caja(oscuro(), x + xx, y - sy * 9.05, zz, 1.4, 0.1, 2.2)
            if sy > 0:
                caja(mat('fondo_letrero', 0x1d1f25, 0.6), x, y - 9.1, h - 4, w - 4, 0.1, 2.4)
                texto(mat('letras_almacen', 0xf2e6c8, 0.6), letreros[k % len(letreros)], x, y - 9.16, h - 2.8, tam=1.4, prof=0.04)
            k += 1
    barco_mke()

def barco_mke():
    """La barca de paseo del río (de las de cervecerías): plana, con toldo
    a rayas y gente sentada. Atracada junto al paseo de la izquierda."""
    X, Y = -26, -RIO + 6
    caja(blanco(), X, Y, AGUA_Z - 0.1, 12, 3.6, 0.9)
    caja(mat('cubierta_barca', 0x9a7a5a, 0.7), X, Y, AGUA_Z + 0.8, 11.6, 3.2, 0.1)
    for x in (-5, 5):
        for s in (-1, 1):
            cil(acero(), X + x, Y + s * 1.5, AGUA_Z + 0.9, 0.05, 2.0, 6)
    caja(mat_franjas('toldo_barca', 0xd52b1e, 0xffffff, 8, eje='X', z0=AGUA_Z + 2.9, alto=0.2), X, Y, AGUA_Z + 2.9, 11, 3.4, 0.15)
    pieles = [0xf1c8a0, 0xd9a47a, 0x8a5a3a, 0xf6d6b4]
    ropas = [0xd52b1e, 0x2a5aa8, 0xf2c230, 0x203a30, 0xffffff, 0xffb612]
    for i in range(4):
        for j in (-1, 1):
            x, y = X - 4 + i * 2.6, Y + j * 0.9
            cil(mat(f'ropa_barca{i % 6}', ropas[(i * 2 + (j > 0)) % 6], 0.6), x, y, AGUA_Z + 0.9, 0.22, 0.6, 8, r2=0.17)
            esfera(mat(f'piel_barca{i % 4}', pieles[(i + (j > 0)) % 4], 0.6), x, y, AGUA_Z + 1.7, 0.17, 1)

# ================================================================ la meta
def museo_calatrava():
    """La meta: el final de Wisconsin Avenue junto al lago. La plaza, el
    puente blanco de Calatrava (el Reiman) con su mástil inclinado y los
    tirantes, y el museo de arte: el pabellón blanco con la proa de cristal
    hacia el lago. Las alas las pone el juego (pieza ala_museo) a 80 m.
    (Más cerca que en la realidad, para que se vea grande al llegar.)"""
    Z = 0.3
    caja(mat('plaza_mam', 0xd2ccc0, 0.8), 0, 12, 0, 60, 24, Z)
    caja(mat('bordillo_mam', 0xb0aaa0, 0.7), 0, 0.2, 0, 60, 0.4, Z + 0.02)
    for s in (-1, 1):
        caja(mat('cesped_mam', 0x7a9a4a, 0.9), s * 22, 30, Z, 16, 60, 0.06)
        for k in range(6):
            y = 4 + k * 8
            rama(mat('tronco_mam', 0x6b4a2f, 0.9), (s * 22, y, Z), (s * 22, y, Z + 3), 0.22, 0.16)
            esfera(mat('hoja_mam', 0xd8902a if k % 2 else 0xc8602e, 0.8), s * 22, y, Z + 4.1, 2.0, 2, esc=(1, 1, 0.85))
    b = mat('blanco_calatrava', 0xf6f6f2, 0.35)
    # El puente: sube de la plaza por encima de la avenida del lago.
    caja(b, 0, 20, Z, 6, 10, 0.3)
    o = caja(b, 0, 33, Z, 6, 16.6, 0.5); o.rotation_euler = (math.atan2(4.2, 16), 0, 0); o.location = (0, 33, Z + 2.0)
    caja(b, 0, 50, Z + 4.2, 6, 18, 0.5)
    for s in (-1, 1):
        caja(mat('cristal_baranda', 0xb8d4e0, 0.15), s * 2.9, 50, Z + 4.7, 0.08, 18, 1.1)
        caja(b, s * 2.9, 50, Z + 5.8, 0.15, 18, 0.12)
    for y in (44, 54):
        cil(b, 0, y, 0, 0.8, Z + 4.2, 10)
    # El mástil inclinado (hacia el museo) y los tirantes hasta el tablero.
    pie, punta = (0, 16, Z), (0, 40, Z + 40)
    rama(b, pie, punta, 0.9, 0.3, 10)
    for k in range(8):
        y = 24 + k * 4.4
        zt = Z + (4.2 if y > 41 else 4.2 * max(0, (y - 25)) / 16)
        t = 0.45 + k * 0.07
        px, py, pz = 0, pie[1] + (punta[1] - pie[1]) * t, pie[2] + (punta[2] - pie[2]) * t
        for s in (-1, 1):
            rama(acero(), (px, py, pz), (s * 2.8, y, zt + 0.5), 0.05, 0.05, 4)
    # El pabellón: la base de cristal y el gran salón de proa.
    cr = mat_ventanas('cristal_mam', 0x8ab4cc, 0xf6f6f2, paso_x=1.6, paso_z=2.0, hueco_x=1.35, hueco_z=1.8, variacion=1.02)
    caja(cr, 0, 80, 0, 34, 46, 7)
    caja(b, 0, 80, 7, 35, 47, 0.8)
    perfil = [(-9, 0), (9, 0), (6, 16), (0, 24), (-6, 16)]
    prisma(cr, perfil, 62, 98)
    for y in range(62, 99, 4):
        prisma(b, [(-9.2, 0), (-8.8, 0), (-5.8, 16.1), (0, 24.3), (5.8, 16.1), (8.8, 0), (9.2, 0), (6.2, 16.4), (0, 24.7), (-6.2, 16.4)], y, y + 0.4)
    # La proa hacia el lago.
    prisma(b, [(-9, 0), (9, 0), (0, 22)], 98, 100)
    rama(b, (0, 100, 0), (0, 118, 18), 0.6, 0.3, 8)
    caja(b, 0, 80, 24.4, 1.2, 64, 1.0)                 # la espina de las alas
    # Las alas del edificio, alargadas a los lados.
    for s in (-1, 1):
        caja(cr, s * 40, 80, 0, 46, 22, 6)
        caja(b, s * 40, 80, 6, 46.6, 22.6, 0.6)
    # El lago Míchigan detrás.
    caja(mat('lago_mke', 0x3a7ab0, 0.15), 0, 400, -0.4, 900, 580, 0.2)
    texto(mat('letras_mam', 0x3a3a3a, 0.5), 'MILWAUKEE ART MUSEUM', 0, 2.4, Z + 0.6, tam=0.5, prof=0.03)
    caja(mat('murete_mam', 0xe6dfcc, 0.6), 0, 2.6, Z, 14, 0.8, 1.2)

def ala_museo():
    """Media ala de la Burke Brise Soleil: 36 lamas blancas a lo largo de la
    espina (el eje y del origen) que salen hacia +x, más largas en medio, como
    un ala de pájaro. El juego pone dos (una dada la vuelta) y las abre."""
    b = mat('blanco_ala', 0xfbfbf8, 0.35)
    N = 36
    for k in range(N):
        y = -31.5 + k * 1.8
        u = (k + 0.5) / N
        largo = 7 + 26 * math.sin(math.pi * u) ** 0.7
        rama(b, (0.6, y, 0), (largo, y + (u - 0.5) * 6, 0), 0.22, 0.07, 4)
    caja(b, 0.3, 0, -0.3, 0.6, 64, 0.6)

# ================================================================ obstáculos
def rueda_queso():
    """La rueda de queso de Wisconsin que viene rodando: la corteza naranja,
    las caras con agujeros y una cuña cortada. Centrada en su eje (rueda
    sobre el eje x)."""
    R, A = 0.5, 0.42
    cil(queso(), 0, 0, 0, R, A, 24, eje='X')
    for x in (-A / 2 - 0.005, A / 2 + 0.005):
        cil(queso_in(), x, 0, 0, R - 0.05, 0.01, 24, eje='X')
        for (yy, zz, r) in ((0.18, 0.12, 0.07), (-0.2, 0.05, 0.05), (0.02, -0.25, 0.08), (-0.1, 0.28, 0.05), (0.26, -0.16, 0.05)):
            cil(agujero(), x * 1.02, yy, zz, r, 0.012, 10, eje='X')
    caja(mat('etiqueta_queso', 0x1f3a7a, 0.5), 0, -R - 0.005, 0, A - 0.06, 0.02, 0.18)

def cuna_queso():
    """La pila de cuñas de queso gigantes sobre un palé (se salta): amarillas,
    con agujeros, y una banderita de Wisconsin."""
    caja(mat('pale_mke', 0xb8905a, 0.8), 0, 0, 0, 1.5, 1.0, 0.16)
    for (x, z, s, giro) in ((-0.32, 0.16, 1.0, 0.0), (0.36, 0.16, 0.85, math.pi), (0.0, 0.6, 0.7, 0.3)):
        o = prisma(queso_in(), [(-0.5 * s, 0), (0.5 * s, 0), (0.5 * s, 0.5 * s)], -0.38, 0.38)
        o.location = (x, 0, z); o.rotation_euler = (0, 0, giro)
        for (hx, hz) in ((0.1, 0.12), (-0.2, 0.08), (0.3, 0.3)):
            if hx * s < 0.45 * s:
                cil(agujero(), x + hx * s * (1 if giro == 0 else -1), -0.385, z + hz * s, 0.05 * s, 0.01, 10, eje='Y')
    cil(negro(), -0.55, 0.3, 0.16, 0.015, 0.75, 6)
    caja(azul(), -0.4, 0.3, 0.7, 0.28, 0.01, 0.18)

def cubo_basura():
    """El cubo de basura verde con ruedas de Milwaukee (se salta). Su tapa
    negra y las ruedas atrás."""
    v = mat('verde_cubo', 0x2f6a3a, 0.5)
    cil(v, 0, 0, 0.06, 0.34, 0.92, 4, r2=0.38).rotation_euler = (0, 0, math.pi / 4)
    caja(negro(), 0, 0.02, 0.98, 0.62, 0.68, 0.07)
    caja(negro(), 0, 0.33, 0.9, 0.62, 0.08, 0.12)
    rueda(-0.25, 0.32, 0.1, 0.06)
    rueda(0.25, 0.32, 0.1, 0.06)
    caja(blanco(), 0, -0.28, 0.5, 0.3, 0.02, 0.16)
    texto(negro(), 'MKE', 0, -0.295, 0.58, tam=0.09, prof=0.01)

def bolsas_basura():
    """El montón de bolsas de basura negras con su nudo (se salta)."""
    b = mat('bolsa_basura', 0x24262c, 0.25)
    for (x, y, z, r) in ((-0.45, 0, 0.28, 0.32), (0.4, 0.05, 0.27, 0.3), (0, -0.05, 0.3, 0.34), (-0.15, 0.1, 0.65, 0.27), (0.25, 0, 0.62, 0.25)):
        esfera(b, x, y, z, r, 2, esc=(1, 0.9, 0.95))
        cil(b, x, y, z + r * 0.9, 0.05, 0.14, 6, r2=0.09)
    cil(mat('cascara', 0xe8d24a, 0.6), 0.55, -0.25, 0.05, 0.06, 0.2, 6)

def cartel_queso():
    """El cartel de queso colgado en medio de la calle (agacharse): una cuña
    de queso gigante con «SAY CHEESE!» colgada de un cable entre dos postes."""
    for x in (-1.25, 1.25):
        cil(negro(), x, 0, 0, 0.06, 2.75, 8)
    cil(negro(), 0, 0, 2.7, 0.03, 2.5, 6, eje='X')
    for x in (-0.6, 0.6):
        cil(negro(), x, 0, 2.3, 0.015, 0.42, 4)
    o = prisma(queso(), [(-1.0, 0), (1.0, 0), (1.0, 0.9)], -0.1, 0.1)
    o.rotation_euler = (0, math.pi, 0)
    o.location = (0, 0, 2.3)
    for (x, z, r) in ((-0.55, 1.85, 0.08), (0.2, 1.75, 0.1), (0.62, 1.95, 0.06), (0.75, 1.62, 0.07)):
        cil(agujero(), x, -0.105, z, r, 0.01, 10, eje='Y')
    texto(rojo(), 'SAY CHEESE!', 0.2, -0.11, 2.12, tam=0.2, prof=0.02)

def fan_queso():
    """El aficionado con el sombrero de queso (los «cheeseheads»): camiseta
    verde con el número dorado, el queso en la cabeza y los brazos arriba.
    Cruza la calle (mira a +x)."""
    piel = mat('piel_fanq', 0xecbc94, 0.6)
    for sy in (-0.12, 0.12):
        cil(mat('pantalon_fanq', 0xe8e4dc, 0.6), 0, sy, 0, 0.1, 0.88, 8, r2=0.12)
        esfera(mat('zapato_fanq', 0x2a2a2a, 0.6), 0.05, sy, 0.05, 0.11, 1, esc=(1.4, 0.9, 0.6))
    cil(verde_pk(), 0, 0, 0.86, 0.27, 0.68, 12, r2=0.24)
    esfera(verde_pk(), 0, 0, 1.54, 0.25, 2, esc=(0.95, 1.15, 0.5))
    texto(oro_pk(), '12', 0, 0, 0, tam=0.22, prof=0.02).rotation_euler = (math.pi / 2, 0, math.pi / 2)
    bpy.context.object.location = (0.26, 0, 1.2)
    cil(piel, 0, 0, 1.58, 0.07, 0.12, 8)
    esfera(piel, 0, 0, 1.8, 0.19, 2, esc=(1, 1, 1.08))
    for sy in (-0.07, 0.07):
        esfera(blanco(), 0.17, sy, 1.83, 0.035, 1)
        esfera(negro(), 0.195, sy, 1.83, 0.018, 1)
    rama(mat('boca_fanq', 0x8a3a2a, 0.6), (0.18, -0.05, 1.72), (0.18, 0.05, 1.72), 0.015, 0.015, 4)
    # El sombrero de queso: una cuña con agujeros, la punta hacia delante.
    o = prisma(queso(), [(-0.26, 0), (0.34, 0), (-0.26, 0.24)], -0.24, 0.24)
    o.location = (0, 0, 1.92)
    for (x, y, z) in ((-0.1, -0.245, 2.0), (0.1, 0.245, 1.97), (-0.18, 0.245, 2.06)):
        cil(agujero(), x, y, z, 0.035, 0.01, 8, eje='Y')
    for sy in (-1, 1):
        rama(verde_pk(), (0, sy * 0.27, 1.45), (0.05, sy * 0.4, 1.95), 0.075, 0.065, 6)
        rama(piel, (0.05, sy * 0.4, 1.95), (0.08, sy * 0.42, 2.25), 0.06, 0.05, 6)
        esfera(piel, 0.08, sy * 0.42, 2.3, 0.07, 1)

def moto_harley():
    """La moto de Milwaukee (las de la fábrica de Juneau Avenue), vista por
    detrás: negra y cromada, con las alforjas de cuero y el motorista de
    chupa con casco. Cambia de carril con el intermitente."""
    n = mat('negro_moto', 0x18191c, 0.25)
    cr = mat('cromo_moto', 0xdfe3e8, 0.15)
    cu = mat('cuero_moto', 0x3a2a20, 0.6)
    rueda(0, 0.1, 0.34, 0.16, z=0.34)
    rueda(0, 1.7, 0.34, 0.14, z=0.34)
    caja(n, 0, 0.9, 0.45, 0.32, 1.4, 0.3)
    caja(n, 0, 0.25, 0.62, 0.42, 0.7, 0.14)               # el guardabarros
    for s in (-1, 1):
        caja(cu, s * 0.3, 0.45, 0.4, 0.2, 0.55, 0.38)     # las alforjas
        cil(cr, s * 0.2, 0.6, 0.28, 0.06, 1.1, 8, eje='Y')
        caja(luz('piloto_moto', 0xff2a2a, 0.8), s * 0.12, -0.02, 0.72, 0.08, 0.03, 0.05)
    esfera(n, 0, 1.35, 0.92, 0.26, 2, esc=(0.9, 1.4, 0.6))  # el depósito
    caja(cu, 0, 0.75, 0.78, 0.36, 0.55, 0.1)              # el asiento
    rama(cr, (-0.42, 1.6, 1.25), (0.42, 1.6, 1.25), 0.025, 0.025, 6)
    cil(cr, 0, 1.85, 1.0, 0.12, 0.08, 12, eje='Y')
    # El motorista.
    ch = mat('chupa_moto', 0x22201e, 0.5)
    for s in (-1, 1):
        rama(mat('vaquero_moto', 0x34466a, 0.6), (s * 0.14, 0.8, 0.88), (s * 0.24, 1.2, 0.8), 0.09, 0.08, 6)
        rama(mat('vaquero_moto', 0x34466a, 0.6), (s * 0.24, 1.2, 0.8), (s * 0.26, 1.25, 0.4), 0.08, 0.07, 6)
        rama(ch, (s * 0.2, 0.86, 1.5), (s * 0.38, 1.4, 1.3), 0.07, 0.06, 6)
    cil(ch, 0, 0.85, 0.88, 0.22, 0.7, 10, r2=0.25)
    texto(mat('letras_chupa', 0xe87a1e, 0.5), 'MKE', 0, 0.62, 1.3, tam=0.12, prof=0.01)
    esfera(mat('casco_moto', 0x18191c, 0.2), 0, 0.92, 1.78, 0.17, 2)
    esfera(mat('piel_moto', 0xd8a47a, 0.6), 0, 0.95, 1.7, 0.13, 1)

def camion_basura():
    """El camión de la basura blanco de Wisconsin (como el de verdad, con
    TRUMP en los lados), visto por detrás: la tolva de atrás, la caja y la
    cabina delante. Él va de pie encima de la cabina, agarrado a la baranda."""
    W = 2.3
    bl = mat('blanco_camion', 0xf4f4f0, 0.35)
    caja(mat('chasis_camion', 0x2a2c31, 0.6), 0, 4.2, 0.35, W - 0.3, 8.2, 0.35)
    # La tolva de atrás (con su boca y la pala).
    caja(bl, 0, 0.75, 0.7, W, 1.5, 1.9)
    caja(mat('boca_tolva', 0x2a2c31, 0.6), 0, -0.01, 0.95, W - 0.5, 0.05, 1.0)
    o = caja(bl, 0, 0.6, 2.4, W, 1.4, 0.4); o.rotation_euler = (0.35, 0, 0)
    for s in (-1, 1):
        caja(mat('naranja_camion', 0xe8721e, 0.5), s * (W / 2 - 0.15), -0.02, 0.85, 0.22, 0.04, 1.4)
        caja(luz('piloto_camion', 0xff2a2a, 0.8), s * 0.95, -0.03, 0.55, 0.18, 0.04, 0.12)
    caja(negro(), 0, -0.1, 0.42, W - 0.2, 0.25, 0.08)         # el estribo
    # La caja.
    caja(bl, 0, 3.9, 0.7, W, 4.8, 2.0)
    for s in (-1, 1):
        caja(rojo(), s * (W / 2 + 0.01), 3.9, 1.0, 0.02, 4.8, 0.18)
        caja(azul(), s * (W / 2 + 0.01), 3.9, 2.4, 0.02, 4.8, 0.18)
        o = texto(azul(), 'TRUMP', 0, 0, 0, tam=0.7, prof=0.03)
        o.rotation_euler = (math.pi / 2, 0, s * math.pi / 2)
        o.location = (s * (W / 2 + 0.03), 3.9, 1.7)
    # La cabina (sin morro, de las de la basura) y la baranda de arriba.
    caja(bl, 0, 7.4, 0.7, W, 2.0, 2.0)
    caja(mat('cristal_camion', 0x1d2533, 0.15), 0, 8.41, 1.6, W - 0.3, 0.02, 0.85)
    caja(mat('techo_camion', 0x3a3c42, 0.6), 0, 7.2, 2.7, W - 0.1, 1.9, 0.08)
    for s in (-1, 1):
        cil(acero(), s * 0.95, 8.1, 2.78, 0.035, 0.95, 6)
        cil(acero(), s * 0.95, 6.5, 2.78, 0.035, 0.95, 6)
        rama(acero(), (s * 0.95, 6.5, 3.7), (s * 0.95, 8.1, 3.7), 0.035, 0.035, 6)
        caja(luz('rotativo_camion', 0xffa21a, 0.9), s * 0.7, 8.2, 2.78, 0.2, 0.2, 0.16)
    rama(acero(), (-0.95, 8.1, 3.7), (0.95, 8.1, 3.7), 0.035, 0.035, 6)
    for s in (-1, 1):
        rueda(s * (W / 2 - 0.15), 1.6, 0.48, 0.32, z=0.48)
        rueda(s * (W / 2 - 0.15), 3.0, 0.48, 0.32, z=0.48)
        rueda(s * (W / 2 - 0.15), 7.3, 0.48, 0.32, z=0.48)

PIEZAS = {
    'gesu_church':     (gesu_church,     'milwaukee', dict(lado=1024, segmentos=1, min_bisel=1.0)),
    'germania':        (germania,        'milwaukee', dict(lado=1024, segmentos=1, min_bisel=1.0)),
    'city_hall_mke':   (city_hall_mke,   'milwaukee', dict(lado=1024, segmentos=1, min_bisel=1.0)),
    'pfister_hotel':   (pfister_hotel,   'milwaukee', dict(lado=1024, segmentos=1, min_bisel=1.0)),
    'us_bank_center':  (us_bank_center,  'milwaukee', dict(lado=1024, bisel=0.0)),
    'puente_mke':      (puente_mke,      'milwaukee', dict(lado=2048, bisel=0.0, suelo=False)),
    'museo_calatrava': (museo_calatrava, 'milwaukee', dict(lado=2048, bisel=0.0)),
    'ala_museo':       (ala_museo,       'milwaukee', dict(lado=256, bisel=0.0, suelo=False)),
    'rueda_queso':     (rueda_queso,     'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
    'cuna_queso':      (cuna_queso,      'obstaculos', dict(lado=256, bisel=0.0)),
    'cubo_basura':     (cubo_basura,     'obstaculos', dict(lado=256, bisel=0.0)),
    'bolsas_basura':   (bolsas_basura,   'obstaculos', dict(lado=256, bisel=0.0)),
    'cartel_queso':    (cartel_queso,    'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
    'fan_queso':       (fan_queso,       'obstaculos', dict(lado=256, bisel=0.0)),
    'moto_harley':     (moto_harley,     'obstaculos', dict(lado=512, bisel=0.0)),
    'camion_basura':   (camion_basura,   'obstaculos', dict(lado=512)),
}

correr(PIEZAS)
