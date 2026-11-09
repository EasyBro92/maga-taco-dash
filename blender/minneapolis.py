# Nivel 13: Minneapolis, Minnesota (09/11/2026).
#
#   blender -b -P blender/minneapolis.py -- [pieza ...] [--rapido]
#
# Isidro (09/11): «sigue creando más estados, aplica tus propias
# recomendaciones sin preguntas». Se aplicó lo recomendado: final en el jardín
# de esculturas (la cuchara gigante con la cereza, nevado) y un día de
# invierno de sol y mucho frío (luz `helada`). Historia: «Lagos helados y
# pistas de hockey de los canadienses».
#   Por Nicollet Mall hacia el suroeste, hasta el jardín de esculturas:
#   izquierda:  el Ayuntamiento (granito rojo y la torre del reloj) · la
#               Foshay Tower (el obelisco con su nombre arriba)
#   derecha:    el IDS Center (el cristal azul, las esquinas en escalera) ·
#               el Wells Fargo Center (la torre dorada escalonada) · la
#               basílica de Santa María (la cúpula, ya cerca del parque)
#   en medio:   el lago helado de Loring Park con tres pistas de hockey,
#               casetas de pesca en el hielo y patinadores
#   al fondo:   el jardín de esculturas: la cuchara-puente con la cereza, el
#               gallo azul y el Walker Art Center detrás
# Obstáculos (carpeta obstaculos): el disco de hockey gigante que viene
# deslizándose, la portería, el jugador canadiense que cruza patinando, la
# pancarta «SORRY, NO TARIFFS» (agacharse), la máquina de pulir el hielo y la
# caseta de pesca en el hielo.

import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import *
from comun import _poner

def blanco():   return mat('blanco_mpls', 0xfbfbf8, 0.5)
def negro():    return mat('negro_mpls', 0x1b1c20, 0.4)
def rojo():     return mat('rojo_mpls', 0xd52b1e, 0.45)
def azul():     return mat('azul_mpls', 0x1f3a7a, 0.45)
def amarillo(): return mat('amarillo_mpls', 0xf2c230, 0.5)
def acero():    return mat('acero_mpls', 0xd8dde2, 0.2)
def oscuro():   return mat('ventana_os_mpls', 0x2c3440, 0.3)
def nieve():    return mat('nieve_mpls', 0xf4f8fc, 0.75)
def hielo():    return mat('hielo_mpls', 0xd6e9f4, 0.08)
def madera():   return mat('madera_mpls', 0x8a5a32, 0.75)
def pino():     return mat('pino_mpls', 0x2a4a34, 0.85)
def tronco():   return mat('tronco_mpls', 0x5a4030, 0.9)
def cobre():    return mat('cobre_mpls', 0x6a9a88, 0.45)
def granito_r(): return mat_bloques('granito_rojo_mpls', 0xa8665a, 0x7a4a40, ancho=0.9, alto=0.45, grosor=0.015, variacion=1.1)
def granito_b(): return mat_bloques('granito_blanco_mpls', 0xe4dfd2, 0xbab4a6, ancho=1.0, alto=0.5, grosor=0.012, variacion=1.04)
def neumatico(): return mat('neumatico_mpls', 0x1e1e22, 0.85)

def rueda(x, y, r=0.3, ancho=0.22, z=None):
    z = r if z is None else z
    cil(neumatico(), x, y, z, r, ancho, 16, eje='X')
    cil(mat('llanta_mpls', 0xd3d6da, 0.3), x + (0.12 if x > 0 else -0.12), y, z, r * 0.5, 0.02, 12, eje='X')

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
    return cil(m, x, y, z + h - w / 2, w / 2, 0.12, 12, eje='Y')

def pino_nevado(x, y, z=0.0, h=7.0):
    """Abeto con nieve: tres conos oscuros con la punta blanca."""
    cil(tronco(), x, y, z, 0.25, h * 0.2, 6)
    for k in range(3):
        zz = z + h * (0.15 + k * 0.25)
        r = h * (0.3 - k * 0.07)
        cil(pino(), x, y, zz, r, h * 0.42, 9, r2=0.05)
        cil(nieve(), x, y, zz + h * 0.3, r * 0.32, h * 0.12, 9, r2=0.03)

def arbol_pelado(x, y, z=0.0, h=6.0):
    """Árbol de invierno sin hojas: tronco y cuatro ramas."""
    rama(tronco(), (x, y, z), (x, y, z + h * 0.55), 0.22, 0.15, 6)
    for k in range(4):
        a = k * math.pi / 2 + 0.4
        rama(tronco(), (x, y, z + h * 0.5), (x + math.cos(a) * h * 0.3, y + math.sin(a) * h * 0.3, z + h), 0.12, 0.04, 5)

def letrero_x(m, cadena, x, y, z, tam, sentido):
    """Letras en una cara que mira a +x (sentido 1) o a -x (sentido -1)."""
    o = texto(m, cadena, 0, 0, 0, tam=tam, prof=0.03)
    o.rotation_euler = (math.pi / 2, 0, sentido * math.pi / 2)
    o.location = (x, y, z)
    return o

# ================================================================ edificios
def ids_center():
    """El IDS Center (1972), el más alto de Minnesota: 241 m de cristal azul
    con las esquinas recortadas en escalera (el «zigurat»), y delante el Crystal
    Court, el patio de cristal en pirámide escalonada."""
    v = mat_ventanas('cristal_ids', 0x3e6a8a, 0x9ab4c4, paso_x=1.5, paso_z=3.6, hueco_x=1.38, hueco_z=3.3, variacion=1.04)
    Y, H, N, S, ALTO = 30, 15.0, 5, 1.3, 241
    for i in range(N + 1):
        a, b = H - S * i, H - S * (N - i)
        caja(v, 0, Y, 0, 2 * a, 2 * b, ALTO)
    caja(mat('remate_ids', 0x9ab4c4, 0.3), 0, Y, ALTO, 2 * (H - S * 2.5), 2 * (H - S * 2.5), 2.5)
    # El Crystal Court: cajas de cristal cada vez más pequeñas, una encima de otra.
    cc = mat_ventanas('crystal_court', 0x8ab8d4, 0xe8eef2, paso_x=1.2, paso_z=1.2, hueco_x=1.05, hueco_z=1.05, variacion=1.02)
    for k in range(5):
        caja(cc, 0, 8, 0 + k * 2.4, 36 - k * 6, 14 - k * 2.2, 2.4 if k else 9.6)
    texto(mat('letras_ids', 0xf2f2ee, 0.4), 'IDS CENTER', 0, 0.9, 7.6, tam=1.2, prof=0.05)

def foshay_tower():
    """La Foshay Tower (1929): un obelisco art déco como el de Washington, con
    FOSHAY en letras grandes en lo alto, sobre su base de piedra."""
    piedra = mat_ventanas('piedra_foshay', 0x2a3240, 0xd8ccb2, paso_x=1.2, paso_z=3.3, hueco_x=0.55, hueco_z=2.4, variacion=1.05)
    Y = 18
    caja(granito_b(), 0, Y, 0, 30, 24, 14)
    caja(mat('cornisa_foshay', 0xc8bca2, 0.6), 0, Y, 14, 30.6, 24.6, 0.8)
    o = cil(piedra, 0, Y, 14.8, 12.5, 100, 4, r2=9.0); o.rotation_euler = (0, 0, math.pi / 4)
    o = cil(mat('punta_foshay', 0xcfc3a8, 0.5), 0, Y, 114.8, 9.0, 16, 4, r2=0.3); o.rotation_euler = (0, 0, math.pi / 4)
    # FOSHAY en las cuatro caras, cerca de la punta.
    letras = mat('letras_foshay', 0xf6e2a0, 0.4)
    for (dx, dy, giro) in ((0, -1, 0), (0, 1, math.pi), (1, 0, math.pi / 2), (-1, 0, -math.pi / 2)):
        o = texto(letras, 'FOSHAY', 0, 0, 0, tam=2.4, prof=0.1)
        o.rotation_euler = (math.pi / 2, 0, giro)
        o.location = (dx * 7.0, Y + dy * 7.0, 105)
    caja(mat('puerta_foshay', 0x3a2a1e, 0.5), 0, Y - 12.05, 0, 6, 0.1, 5)
    texto(mat('letras_foshay_b', 0x6a5a40, 0.5), 'FOSHAY', 0, Y - 12.1, 11.5, tam=1.0, prof=0.04)

def wells_fargo_mpls():
    """El Wells Fargo Center (1988): la torre de piedra dorada en escalones,
    con la corona iluminada arriba."""
    v = mat_ventanas('piedra_wf', 0x34404e, 0xdcc8a0, paso_x=1.5, paso_z=3.5, hueco_x=0.9, hueco_z=2.6, variacion=1.05)
    Y = 22
    tramos = ((34, 26, 0, 168), (30, 22, 168, 192), (24, 18, 192, 210), (18, 13, 210, 222))
    for (w, d, z0, z1) in tramos:
        caja(v, 0, Y, z0, w, d, z1 - z0)
        caja(mat('corona_wf', 0xf2e2b8, 0.4), 0, Y, z1, w + 0.4, d + 0.4, 0.6)
        # Las luces de la corona en cada escalón.
        caja(luz('luz_wf', 0xffe6a8, 0.7), 0, Y - d / 2 - 0.05, z1 - 2.2, w * 0.7, 0.05, 1.2)
    caja(v, 0, Y, 222.6, 10, 8, 8)
    cil(mat('punta_wf', 0xe8d4a8, 0.4), 0, Y, 230.6, 5.5, 5.5, 4, r2=0.2).rotation_euler = (0, 0, math.pi / 4)
    caja(mat('vestibulo_wf', 0x4a5666, 0.2), 0, Y - 13.05, 0, 22, 0.1, 7)
    texto(mat('letras_wf', 0xc8202e, 0.4), 'WELLS FARGO', 0, Y - 13.1, 8.2, tam=1.3, prof=0.05)

def city_hall_mpls():
    """El Ayuntamiento de Minneapolis (1909): granito rojo rugoso, arcos de
    medio punto y la torre del reloj de 105 m con el tejado de cobre."""
    g = granito_r()
    Y = 16
    caja(g, 0, Y, 0, 42, 30, 28)
    caja(mat('cornisa_ch_mpls', 0x8a5248, 0.6), 0, Y, 28, 42.6, 30.6, 1.0)
    # El tejado a cuatro aguas, de cobre.
    o = cil(cobre(), 0, Y, 29, 26, 9, 4, r2=10); o.rotation_euler = (0, 0, math.pi / 4); o.scale = (1.15, 0.8, 1)
    vent = mat('ventana_ch_mpls', 0x2a2e36, 0.3)
    for z in (3, 11, 19):
        for x in range(-18, 19, 4):
            if abs(x) < 7:
                continue
            ventana_arco(vent, x, Y - 15.06, z, 1.6, 4.5 if z > 3 else 5.2)
    # Torreones en las esquinas.
    for sx in (-1, 1):
        cil(g, sx * 20, Y - 14, 0, 2.6, 33, 10)
        cil(cobre(), sx * 20, Y - 14, 33, 2.9, 6, 10, r2=0.2)
    # La torre del reloj en medio de la fachada.
    T = 12
    caja(g, 0, Y - 12, 0, T, T, 78)
    ventana_arco(mat('portal_ch_mpls', 0x3a2a20, 0.5), 0, Y - 18.06, 0, 5, 7.5)
    for z in (30, 42, 54):
        ventana_arco(vent, 0, Y - 18.06, z, 2.4, 6)
    for (dx, dy, giro) in ((0, -1, 0), (1, 0, math.pi / 2), (-1, 0, -math.pi / 2)):
        cx, cy = dx * (T / 2 + 0.06), Y - 12 + dy * (T / 2 + 0.06)
        e = cil(blanco(), cx, cy, 68, 3.6, 0.1, 24, eje='Y'); e.rotation_euler = (math.pi / 2, 0, giro)
        e = cil(negro(), cx, cy, 68, 3.9, 0.06, 24, eje='Y'); e.rotation_euler = (math.pi / 2, 0, giro); e.location = (cx * 1.0 - dx * 0.03, cy - dy * 0.03, 68)
        h = caja(negro(), cx + dx * 0.1, cy + dy * 0.1, 68, 0.3 if dx == 0 else 0.1, 0.1 if dx == 0 else 0.3, 2.6); h.rotation_euler = (0, 0, giro)
    # El campanario con arcos y el tejado alto de cobre.
    caja(g, 0, Y - 12, 78, T + 0.6, T + 0.6, 1.0)
    for (dx, dy, giro) in ((0, -1, 0), (1, 0, math.pi / 2), (-1, 0, -math.pi / 2), (0, 1, math.pi)):
        for k in (-1, 0, 1):
            hm = mat('hueco_ch_mpls', 0x1d1f25, 0.5)
            if dx == 0:
                ventana_arco(hm, k * 3.4, Y - 12 + dy * (T / 2 + 0.36), 80, 2.2, 6)
            else:
                caja(hm, dx * (T / 2 + 0.36), Y - 12 + k * 3.4, 80, 0.12, 2.2, 4.9)
                cil(hm, dx * (T / 2 + 0.36), Y - 12 + k * 3.4, 84.9, 1.1, 0.12, 12, eje='X')
    caja(g, 0, Y - 12, 79, T, T, 9)
    o = cil(cobre(), 0, Y - 12, 88, T * 0.72, 17, 4, r2=0.3); o.rotation_euler = (0, 0, math.pi / 4)
    for (sx, sy) in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
        cil(cobre(), sx * 5.4, Y - 12 + sy * 5.4, 88, 0.9, 6, 8, r2=0.1)
    cil(amarillo(), 0, Y - 12, 105, 0.12, 2.5, 6)
    texto(mat('letras_ch_mpls', 0xf2e6c8, 0.5), 'CITY HALL', 0, Y - 18.12, 8.6, tam=0.9, prof=0.04)

def basilica_mary():
    """La basílica de Santa María (1914), la primera de Estados Unidos: granito
    blanco, la gran cúpula de cobre con su linterna, las dos torres y el
    rosetón de la fachada."""
    g = granito_b()
    Y = 24
    caja(g, 0, Y, 0, 30, 46, 24)
    caja(mat('cornisa_bas', 0xd2ccbe, 0.6), 0, Y, 24, 30.6, 46.6, 1.0)
    # La fachada: el rosetón, el pórtico y las dos torres.
    fronton(g, 0, Y - 23, 25, 30, 7, 2)
    cil(mat('roseton_bas', 0x3a4a8a, 0.2), 0, Y - 23.1, 15, 4.4, 0.2, 24, eje='Y')
    cil(granito_b(), 0, Y - 23.05, 15, 5.0, 0.1, 24, eje='Y')
    caja(g, 0, Y - 25.5, 0, 16, 5, 11)
    columnata(g, -6.6, 6.6, 5, Y - 27.6, 0, 0.6, 10)
    fronton(g, 0, Y - 28.2, 11, 17, 3.2, 5.4)
    ventana_arco(mat('puerta_bas', 0x3a2a1e, 0.5), 0, Y - 28.1, 0, 3.6, 7)
    for sx in (-1, 1):
        caja(g, sx * 18, Y - 18, 0, 8, 8, 38)
        ventana_arco(mat('hueco_bas', 0x2a2e36, 0.4), sx * 18, Y - 22.06, 26, 2.2, 6)
        cil(g, sx * 18, Y - 18, 38, 3.4, 4, 12)
        cupula(cobre(), sx * 18, Y - 18, 42, 3.4, 4.5)
        cil(amarillo(), sx * 18, Y - 18, 46.5, 0.1, 2.5, 6)
    # El tambor y la cúpula, en el centro de la nave.
    cil(g, 0, Y + 4, 25, 12, 14, 24)
    for k in range(12):
        a = k * math.pi / 6
        caja(mat('hueco_bas', 0x2a2e36, 0.4), math.sin(a) * 12.0, Y + 4 - math.cos(a) * 12.0, 28, 2.2, 0.3, 7, giro=a)
    cupula(cobre(), 0, Y + 4, 39, 12.4, 16)
    cil(g, 0, Y + 4, 54, 2.4, 6, 12)
    cupula(cobre(), 0, Y + 4, 60, 2.6, 3)
    cil(amarillo(), 0, Y + 4, 63, 0.15, 4, 6)
    caja(amarillo(), 0, Y + 4, 65.5, 1.8, 0.2, 0.2)

# ================================================================ el lago helado
L_LAGO = 440.0

def pista_hockey(Y):
    """Una pista de hockey en el hielo del lago: las rayas pintadas, los
    círculos de saque y las vallas blancas de los lados con anuncios (los de
    los canadienses enfadados). Las puntas de la pista abiertas para pasar."""
    LARGO, ANCHO = 64.0, 26.0
    Z = 0.012
    caja(mat('hielo_pista', 0xeef6fb, 0.06), 0, Y, 0, ANCHO, LARGO, Z)
    caja(rojo(), 0, Y, Z, ANCHO, 0.45, 0.004)
    for s in (-1, 1):
        caja(azul(), 0, Y + s * 11, Z, ANCHO, 0.45, 0.004)
        caja(rojo(), 0, Y + s * 27, Z, ANCHO, 0.12, 0.004)
        for sx in (-1, 1):
            cil(rojo(), sx * 7, Y + s * 19, Z, 4.5, 0.004, 32)
            cil(mat('hielo_pista', 0xeef6fb, 0.06), sx * 7, Y + s * 19, Z + 0.002, 4.35, 0.004, 32)
            cil(rojo(), sx * 7, Y + s * 19, Z + 0.004, 0.35, 0.004, 12)
    cil(azul(), 0, Y, Z, 4.5, 0.004, 32)
    cil(mat('hielo_pista', 0xeef6fb, 0.06), 0, Y, Z + 0.002, 4.35, 0.004, 32)
    cil(azul(), 0, Y, Z + 0.004, 0.4, 0.004, 12)
    # Las vallas: blancas, con la franja amarilla abajo y los anuncios.
    anuncios = ('NO 51st STATE', 'SORRY!', 'EH?', 'HOCKEY', 'MINNESOTA', 'NO TARIFFS')
    for sx in (-1, 1):
        x = sx * ANCHO / 2
        caja(blanco(), x, Y, 0, 0.25, LARGO - 6, 1.15)
        caja(amarillo(), x - sx * 0.13, Y, 0, 0.02, LARGO - 6, 0.25)
        caja(mat('pasamanos_pista', 0xd52b1e, 0.5), x, Y, 1.15, 0.3, LARGO - 6, 0.08)
        for k in range(3):
            yy = Y - 18 + k * 18
            caja(azul(), x - sx * 0.14, yy, 0.35, 0.02, 9, 0.62)
            letrero_x(blanco(), anuncios[(k + (sx > 0) * 3) % 6], x - sx * 0.16, yy, 0.66, 0.42, -sx)
        # Las esquinas redondeadas (sin cerrar el paso: las puntas abiertas).
        for sy in (-1, 1):
            for k in range(4):
                a = (k + 0.5) / 4 * math.pi / 2
                cx = sx * (ANCHO / 2 - 3 + math.sin(a) * 3)
                cy = Y + sy * (LARGO / 2 - 3 + math.cos(a) * 3)
                caja(blanco(), cx, cy, 0, 0.25, 2.4, 1.15, giro=sy * sx * a)
            caja(blanco(), sx * (ANCHO / 2 - 4.5), Y + sy * LARGO / 2, 0, 3.4, 0.25, 1.15)
        # Los banquillos, por fuera de la valla.
        caja(madera(), sx * (ANCHO / 2 + 1.5), Y - 6, 0, 1.2, 10, 0.5)
    # Los focos de la pista, en postes.
    for sx in (-1, 1):
        for sy in (-1, 1):
            cil(negro(), sx * 16, Y + sy * 24, 0, 0.18, 12, 8)
            caja(luz('foco_pista', 0xfff6e0, 0.8), sx * 16, Y + sy * 24, 12, 1.6, 0.6, 0.6)

def caseta_lejos(x, y, k):
    """Caseta de pesca en el hielo, de colores, con su chimenea."""
    colores = (0xd52b1e, 0x2a6a3a, 0x1f3a7a, 0xe8a21a, 0x6a3a8a, 0x8a5a32)
    m = mat(f'caseta_lago{k % 6}', colores[k % 6], 0.6)
    caja(m, x, y, 0, 2.4, 3.0, 2.0)
    tejado(mat('tejado_caseta', 0x3a3a40, 0.7), x, y - 1.6, y + 1.6, 2.0, 2.6, 0.7)
    cil(negro(), x + 0.7, y + 0.8, 2.2, 0.08, 0.9, 6)
    caja(blanco(), x, y - 1.51, 0.9, 0.6, 0.02, 0.6)

def patinador(x, y, k, giro=0.0):
    """Patinador de lejos: abrigo de color, gorro y bufanda, inclinado."""
    ropas = (0xd52b1e, 0x1f3a7a, 0x2a6a3a, 0xe8a21a, 0x6a3a8a, 0x2a2a2a)
    piel = mat(f'piel_pat{k % 3}', (0xf1c8a0, 0xd9a47a, 0x8a5a3a)[k % 3], 0.6)
    r = mat(f'ropa_pat{k % 6}', ropas[k % 6], 0.6)
    c, s = math.cos(giro), math.sin(giro)
    P = lambda dx, dz: (x + dx * c, y + dx * s, dz)
    rama(mat('pantalon_pat', 0x2a2e3a, 0.6), P(0, 0.08), P(0.1, 0.85), 0.09, 0.09, 6)
    rama(mat('pantalon_pat', 0x2a2e3a, 0.6), P(0.1, 0.85), P(-0.35, 0.35), 0.09, 0.08, 6)
    rama(r, P(0.1, 0.85), P(0.25, 1.5), 0.24, 0.2, 8)
    esfera(piel, *P(0.3, 1.72), 0.16, 1)
    cil(r, *P(0.3, 1.82), 0.16, 0.18, 8, r2=0.05)
    rama(mat('bufanda_pat', 0xf2f2ee, 0.6), P(0.25, 1.52), P(0.0, 1.45), 0.08, 0.06, 5)

def lago_helado():
    """El lago helado de Loring Park: la calle se acaba en la orilla nevada y
    se cruza el lago por el hielo. Tres pistas de hockey seguidas, casetas de
    pesca de colores, patinadores, la casa de calentarse y, en las orillas,
    abetos nevados, árboles pelados y farolas. Cruza la calle: el origen en el
    centro y la calle a lo largo de y."""
    L = L_LAGO
    # El hielo, y la nieve de las orillas (las dos puntas, por donde se entra y
    # se sale, y los dos lados).
    caja(hielo(), 0, 0, -0.3, 400, L - 20, 0.3)
    for sy in (-1, 1):
        caja(nieve(), 0, sy * (L / 2 - 5), -0.3, 400, 10, 0.34)
        for k in range(16):
            x = -150 + k * 20
            if abs(x) < 12:
                continue
            esfera(nieve(), x + (k % 3) * 3, sy * (L / 2 - 9), 0, 4 + (k % 4), 2, esc=(1.6, 0.8, 0.35))
        # El letrero del parque, a la derecha de la entrada.
        if sy < 0:
            for x in (9.2, 13.8):
                cil(madera(), x, -L / 2 + 6, 0, 0.12, 2.6, 6)
            caja(mat('letrero_parque', 0x2a4a34, 0.6), 11.5, -L / 2 + 6, 1.4, 5.4, 0.15, 1.2)
            texto(mat('letras_parque', 0xf2e6c8, 0.5), 'LORING PARK', 11.5, -L / 2 + 5.9, 2.0, tam=0.5, prof=0.03)
    for sx in (-1, 1):
        caja(nieve(), sx * 160, 0, -0.3, 80, L, 0.9)
        for k in range(22):
            y = -L / 2 + 10 + k * 19.5
            x = sx * (128 + (k * 37) % 40)
            if k % 3:
                pino_nevado(x, y, 0.6, 8 + (k % 4) * 2)
            else:
                arbol_pelado(x, y, 0.6, 7 + (k % 3))
        for k in range(12):
            y = -L / 2 + 20 + k * 36
            cil(negro(), sx * 121, y, 0.6, 0.1, 4.0, 6)
            esfera(mat('globo_farola_mpls', 0xfff2d0, 0.3), sx * 121, y, 4.8, 0.3, 2)
    # Las pistas de hockey (por donde pasan los carriles).
    for Y in (-130, 0, 130):
        pista_hockey(Y)
    # Las casetas de pesca, lejos de los carriles.
    k = 0
    for sx in (-1, 1):
        for j in range(9):
            y = -190 + j * 46 + (j % 2) * 11
            x = sx * (30 + (j * 23) % 60)
            caseta_lejos(x, y, k)
            k += 1
    # Patinadores dando vueltas por el hielo (lejos de los carriles).
    for j in range(14):
        sx = -1 if j % 2 else 1
        patinador(sx * (20 + (j * 7) % 50), -180 + j * 26, j, giro=(j * 1.3) % 6.28)
    # La casa de calentarse, a la izquierda de la primera pista.
    X, Yc = -42, -150
    caja(mat('casa_calentar', 0x8a3a2a, 0.7), X, Yc, 0, 12, 8, 4)
    tejado(mat('tejado_casa_c', 0x3a3a40, 0.7), X, Yc - 4.3, Yc + 4.3, 4, 13, 2.6, cumbrera='x' if False else 'y')
    caja(nieve(), X, Yc, 6.1, 9, 8.6, 0.25)
    for x in (-3, 0, 3):
        caja(mat('ventana_casa_c', 0xffd890, 0.3), X + x, Yc - 4.02, 1.4, 1.2, 0.04, 1.2)
    texto(mat('letras_casa_c', 0xf2e6c8, 0.5), 'WARMING HOUSE', X, Yc - 4.06, 3.2, tam=0.45, prof=0.03)

# ================================================================ la meta
def cuchara_cereza():
    """La meta: el jardín de esculturas de Minneapolis, nevado. La plaza, el
    estanque helado con la cuchara-puente y la cereza (más grande que la de
    verdad, para verla bien), el gallo azul gigante, setos en filas y, detrás,
    el Walker Art Center con su torre de malla de aluminio."""
    Z = 0.25
    PY = 36          # el estanque
    caja(mat('plaza_walker', 0xc8c2b6, 0.8), 0, 10, 0, 60, 20, Z)
    caja(nieve(), 0, 70, 0, 260, 120, Z - 0.05)
    # Los setos en filas (con nieve por encima), a los dos lados.
    seto = mat('seto_walker', 0x34503a, 0.85)
    for sx in (-1, 1):
        for fila in range(3):
            for k in range(6):
                x, y = sx * (36 + fila * 8), 16 + k * 9
                cil(seto, x, y, Z, 1.6, 4.6, 8, r2=0.4)
                cil(nieve(), x, y, Z + 3.6, 0.7, 1.0, 8, r2=0.1)
    # El estanque helado.
    o = cil(hielo(), 0, PY, Z - 0.02, 18, 0.08, 40); o.scale = (1.6, 1, 1)
    o = cil(granito_b(), 0, PY, Z - 0.1, 18.8, 0.12, 40); o.scale = (1.6, 1, 1)
    # La cuchara: el mango apoyado a la izquierda, que sube en arco por
    # encima del estanque, y el cuenco a la derecha con la cereza.
    ac = mat('cuchara', 0xdfe4ea, 0.12)
    E = 2.5
    pts = []
    for k in range(13):
        u = k / 12
        x = (-15 + u * 26) * E / 1.4
        z = Z + (0.4 + 6.2 * math.sin(u * math.pi * 0.62)) * E / 1.4
        pts.append((x, PY, z))
    for k in range(12):
        r0 = (0.4 + 0.26 * k / 12) * E / 1.4
        rama(ac, pts[k], pts[k + 1], r0, r0 * 1.03, 10)
    bx, bz = pts[-1][0] + 4.2 * E / 1.4, pts[-1][2] + 0.4
    esfera(ac, bx, PY, bz, 4.6 * E / 1.4, 3, esc=(1.25, 0.62, 0.3))
    ce = mat('cereza', 0xa0101e, 0.18)
    R = 2.0 * E / 1.4
    esfera(ce, bx + 0.6, PY, bz + R * 0.95, R, 3)
    rama(mat('rabo_cereza', 0x5a3a1e, 0.5), (bx + 0.6, PY, bz + R * 1.9), (bx - 0.6, PY, bz + R * 3.2), 0.25, 0.18, 6)
    rama(mat('rabo_cereza', 0x5a3a1e, 0.5), (bx - 0.6, PY, bz + R * 3.2), (bx - 2.2, PY, bz + R * 3.6), 0.18, 0.14, 6)
    # El gallo azul gigante (a la izquierda, sobre su peana).
    az = mat('gallo_azul', 0x1838b8, 0.35)
    GX, GY = -30, 62
    caja(granito_b(), GX, GY, Z, 4, 4, 1.2)
    G = Z + 1.2
    for sy in (-0.5, 0.5):
        cil(az, GX, GY + sy, G, 0.3, 2.2, 8)
    esfera(az, GX, GY, G + 4.0, 2.4, 3, esc=(1.3, 0.9, 1.0))
    rama(az, (GX + 1.8, GY, G + 4.6), (GX + 2.6, GY, G + 7.2), 1.0, 0.7, 10)
    esfera(az, GX + 2.8, GY, G + 7.6, 0.95, 2)
    caja(az, GX + 3.9, GY, G + 7.4, 0.9, 0.3, 0.35)
    for k in range(4):
        caja(az, GX + 2.4 + k * 0.32, GY, G + 8.4 + (k % 2) * 0.25, 0.3, 0.2, 0.7)
    for k in range(5):
        a = 0.3 + k * 0.28
        rama(az, (GX - 2.4, GY, G + 4.6), (GX - 2.4 - math.cos(a) * 3.6, GY, G + 4.6 + math.sin(a) * 4.2), 0.55, 0.15, 6)
    # El Walker Art Center detrás: cajas de ladrillo y la torre de malla.
    malla = mat_ventanas('malla_walker', 0x8a9098, 0xc8ccd2, paso_x=0.6, paso_z=0.6, hueco_x=0.45, hueco_z=0.45, variacion=1.02)
    caja(mat_bloques('ladrillo_walker', 0x9a6a50, 0x6e4a38, ancho=0.4, alto=0.15, grosor=0.012), 0, 104, 0, 90, 24, 16)
    caja(malla, 18, 94, 0, 26, 26, 32)
    caja(mat('cristal_walker', 0x6a8aa8, 0.15), -24, 91.9, 2, 30, 0.2, 10)
    texto(mat('letras_walker', 0x1b1c20, 0.4), 'WALKER', 18, 80.9, 26, tam=3.2, prof=0.1)
    # Abetos nevados alrededor.
    for k in range(10):
        sx = -1 if k % 2 else 1
        pino_nevado(sx * (62 + (k * 7) % 20), 14 + k * 8, Z, 9 + (k % 3) * 2)
    texto(mat('letras_jardin', 0x3a3a3a, 0.5), 'MINNEAPOLIS SCULPTURE GARDEN', 0, 2.4, Z + 0.6, tam=0.45, prof=0.03)
    caja(mat('murete_jardin', 0xe6dfcc, 0.6), 0, 2.6, Z, 16, 0.8, 1.2)

# ================================================================ obstáculos
def disco_hockey():
    """El disco de hockey gigante que viene deslizándose por el hielo (se
    salta): negro, con la hoja de arce roja encima y la nieve que levanta."""
    cil(mat('disco', 0x15161a, 0.35), 0, 0, 0, 0.6, 0.42, 28)
    cil(mat('canto_disco', 0x2a2b30, 0.6), 0, 0, 0.1, 0.605, 0.22, 28)
    # La hoja de arce, de cajitas rojas (desde atrás se ve encima).
    hoja = rojo()
    caja(hoja, 0, 0, 0.42, 0.12, 0.5, 0.012)
    for (x, y, g) in ((0, 0.12, 0), (-0.15, 0.05, 0.6), (0.15, 0.05, -0.6), (-0.1, -0.08, 1.1), (0.1, -0.08, -1.1)):
        caja(hoja, x, y, 0.42, 0.18, 0.18, 0.012, giro=g)
    texto(blanco(), 'EH?', 0, -0.6, 0.22, tam=0.16, prof=0.01)
    for (x, y, r) in ((-0.5, 0.65, 0.16), (0.45, 0.7, 0.13), (0, 0.8, 0.2), (-0.25, 0.95, 0.1), (0.3, 1.0, 0.1)):
        esfera(nieve(), x, y, r * 0.6, r, 1)

def porteria_hockey():
    """La portería de hockey (se salta): el marco rojo, la red blanca y el
    disco dentro. La boca mira a quien llega."""
    tubo = mat('marco_porteria', 0xd52b1e, 0.35)
    W, H, F = 1.9, 1.2, 1.1
    for x in (-W / 2, W / 2):
        cil(tubo, x, 0, 0, 0.05, H, 8)
        rama(tubo, (x, 0, 0.03), (x * 0.8, F, 0.03), 0.04, 0.04, 6)
        rama(tubo, (x, 0, H), (x * 0.7, F * 0.5, 0.3), 0.04, 0.04, 6)
    cil(tubo, 0, 0, H, 0.05, W, 8, eje='X')
    rama(tubo, (-W * 0.4, F, 0.03), (W * 0.4, F, 0.03), 0.04, 0.04, 6)
    red = mat_bloques('red_porteria', 0xf6f8fa, 0x9aa2aa, ancho=0.12, alto=0.12, grosor=0.02, variacion=1.0)
    panel(red, (-W / 2, 0.02, H), (W / 2, 0.02, H), (W * 0.4, F, 0.05), (-W * 0.4, F, 0.05), grosor=0.02)
    for s in (-1, 1):
        panel(red, (s * W / 2, 0, 0.05), (s * W / 2, 0, H), (s * W * 0.4, F, 0.05), (s * W * 0.45, F * 0.5, 0.05), grosor=0.02)
    cil(mat('disco', 0x15161a, 0.35), 0.3, 0.6, 0.0, 0.12, 0.08, 12)
    caja(mat('raya_gol', 0xd52b1e, 0.5), 0, -0.05, 0, W + 0.6, 0.08, 0.01)

def jugador_hockey():
    """El jugador canadiense que cruza patinando (mira a +x): camiseta roja con
    la hoja de arce, casco con rejilla, guantes, el palo y los patines,
    inclinado hacia delante con una pierna atrás."""
    piel = mat('piel_jug', 0xecbc94, 0.6)
    camiseta = mat('camiseta_canada', 0xc8202a, 0.55)
    pant = mat('pantalon_jug', 0x1b1c20, 0.55)
    med = mat_franjas('medias_jug', 0xc8202a, 0xf2f2ee, 4, eje='Z', z0=0.1, alto=0.6)
    hoja = mat('patin_cuchilla', 0xdfe4ea, 0.15)
    # Las piernas: la de delante doblada, la de atrás estirada.
    rama(med, (0.15, -0.14, 0.12), (0.3, -0.14, 0.52), 0.1, 0.11, 6)
    rama(pant, (0.3, -0.14, 0.52), (0.05, -0.14, 0.95), 0.13, 0.15, 6)
    rama(med, (-0.6, 0.14, 0.12), (-0.3, 0.14, 0.5), 0.1, 0.11, 6)
    rama(pant, (-0.3, 0.14, 0.5), (0.0, 0.14, 0.95), 0.13, 0.15, 6)
    for (x, y) in ((0.2, -0.14), (-0.55, 0.14)):
        caja(negro(), x, y, 0.06, 0.34, 0.14, 0.14)
        caja(hoja, x, y, 0.0, 0.42, 0.03, 0.06)
    # El cuerpo inclinado, con la hoja de arce blanca en el pecho.
    rama(camiseta, (0.0, 0, 0.95), (0.3, 0, 1.55), 0.32, 0.3, 10)
    caja(blanco(), 0.31, 0, 1.28, 0.02, 0.3, 0.06)
    for (y, z, g) in ((0, 1.36, 0), (-0.09, 1.3, 0.6), (0.09, 1.3, -0.6)):
        o = caja(blanco(), 0.32, y, z, 0.02, 0.12, 0.12); o.rotation_euler = (g, 0, 0)
    for s in (-1, 1):
        caja(blanco(), 0.12, s * 0.31, 1.25, 0.3, 0.02, 0.12)
    # La cabeza con el casco y la rejilla.
    esfera(piel, 0.42, 0, 1.8, 0.18, 2)
    esfera(mat('casco_jug', 0xc8202a, 0.3), 0.4, 0, 1.86, 0.2, 2, esc=(1.05, 1, 0.85))
    for k in range(4):
        cil(acero(), 0.6, -0.12 + k * 0.08, 1.66, 0.012, 0.28, 4)
    caja(mat('cejas_jug', 0x3a2618, 0.6), 0.59, 0, 1.86, 0.04, 0.24, 0.04)
    # Los brazos y el palo, bajo y por delante.
    for s in (-1, 1):
        rama(camiseta, (0.25, s * 0.3, 1.5), (0.55, s * 0.25, 1.1), 0.09, 0.08, 6)
        esfera(negro(), 0.6, s * 0.22, 1.05, 0.11, 1)
    rama(mat('palo_jug', 0x9a6a3a, 0.5), (0.55, -0.22, 1.2), (1.2, 0.05, 0.05), 0.03, 0.03, 6)
    caja(negro(), 1.35, 0.08, 0.03, 0.36, 0.08, 0.1)
    texto(blanco(), 'CANADA', 0, 0, 0, tam=0.1, prof=0.01).rotation_euler = (math.pi / 2, 0, -math.pi / 2)
    bpy.context.object.location = (-0.22, 0, 1.4)

def pancarta_eh():
    """La pancarta de los canadienses colgada en medio (agacharse): «SORRY,
    NO TARIFFS» entre dos palos de hockey, con la hoja de arce."""
    for x in (-1.25, 1.25):
        cil(mat('palo_pancarta', 0x9a6a3a, 0.5), x, 0, 0, 0.07, 2.75, 8)
        caja(negro(), x, 0, 0, 0.4, 0.14, 0.12)
    tela = mat('tela_pancarta', 0xf6f6f2, 0.7)
    caja(tela, 0, 0, 1.55, 2.4, 0.06, 1.05)
    for x in (-1.15, 1.15):
        caja(rojo(), x, -0.01, 1.55, 0.3, 0.07, 1.05)
    texto(rojo(), 'SORRY,', 0, -0.04, 2.3, tam=0.26, prof=0.02)
    texto(rojo(), 'NO TARIFFS', 0, -0.04, 1.96, tam=0.26, prof=0.02)
    hoja = rojo()
    for (x, z, g) in ((0, 1.72, 0), (-0.14, 1.66, 0.6), (0.14, 1.66, -0.6)):
        o = caja(hoja, x, -0.04, z, 0.14, 0.02, 0.14); o.rotation_euler = (0, g, 0)

def pulidora_hielo():
    """La máquina de pulir el hielo de las pistas, vista por detrás: blanca y
    azul, con la cuchilla de agua atrás y el conductor sentado arriba."""
    W = 2.1
    bl = mat('blanco_pulidora', 0xf4f4f0, 0.35)
    caja(bl, 0, 1.6, 0.35, W, 3.2, 1.3)
    caja(azul(), 0, 1.6, 0.9, W + 0.02, 3.2, 0.25)
    caja(mat('cuchilla_pulidora', 0x8a9098, 0.3), 0, -0.1, 0.12, W + 0.2, 0.4, 0.4)
    caja(mat('agua_pulidora', 0xbfe4f4, 0.05), 0, -0.6, 0.0, W, 0.8, 0.01)
    caja(bl, 0, 1.0, 1.65, W - 0.2, 1.8, 0.8)
    texto(azul(), 'ICE', 0, -0.05, 1.95, tam=0.4, prof=0.02)
    for s in (-1, 1):
        caja(luz('piloto_pulidora', 0xff2a2a, 0.8), s * 0.8, -0.32, 1.0, 0.16, 0.04, 0.1)
        rueda(s * (W / 2 - 0.1), 0.6, 0.38, 0.26, z=0.38)
        rueda(s * (W / 2 - 0.1), 2.8, 0.38, 0.26, z=0.38)
    # El conductor sentado, con su gorro.
    caja(negro(), 0, 2.4, 1.65, 0.6, 0.6, 0.5)
    cil(mat('abrigo_pulidora', 0x2a6a3a, 0.6), 0, 2.45, 2.1, 0.26, 0.6, 10)
    esfera(mat('piel_pulidora', 0xecbc94, 0.6), 0, 2.45, 2.88, 0.18, 2)
    cil(rojo(), 0, 2.45, 2.98, 0.19, 0.18, 10, r2=0.08)
    esfera(blanco(), 0, 2.45, 3.18, 0.07, 1)
    caja(luz('rotativo_pulidora', 0xffa21a, 0.9), 0, 1.0, 2.45, 0.2, 0.2, 0.16)

def caseta_pesca():
    """La caseta de pesca en el hielo, de madera roja con el tejado nevado,
    la chimenea humeando y el pescador sentado delante con su caña."""
    caja(mat('caseta_roja', 0xb83a2a, 0.65), 0, 1.4, 0, 2.2, 2.6, 2.0)
    tejado(mat('tejado_caseta', 0x3a3a40, 0.7), 0, 0.0, 2.8, 2.0, 2.6, 0.7)
    caja(nieve(), 0, 1.4, 2.5, 1.6, 2.4, 0.18)
    cil(negro(), 0.7, 2.2, 2.2, 0.08, 1.1, 6)
    for (z, r) in ((3.5, 0.18), (3.85, 0.24), (4.25, 0.3)):
        esfera(mat('humo_caseta', 0xdfe4ea, 0.9), 0.75, 2.2, z, r, 1)
    caja(mat('puerta_caseta', 0x6a3a2a, 0.6), 0.4, 0.09, 0, 0.7, 0.04, 1.6)
    caja(blanco(), -0.5, 0.09, 1.1, 0.6, 0.03, 0.5)
    texto(rojo(), 'BAIT', -0.5, 0.06, 1.35, tam=0.16, prof=0.01)
    # El pescador en su taburete, delante del agujero.
    cil(mat('agujero_hielo', 0x1d3a4a, 0.1), -0.35, -0.7, 0, 0.25, 0.02, 14)
    cil(madera(), 0.3, -0.5, 0, 0.18, 0.45, 8)
    cil(mat('abrigo_pescador', 0x2a6a3a, 0.6), 0.3, -0.5, 0.45, 0.26, 0.6, 10, r2=0.22)
    esfera(mat('piel_pescador', 0xecbc94, 0.6), 0.3, -0.52, 1.22, 0.17, 2)
    cil(mat('gorro_pescador', 0xe86a1a, 0.6), 0.3, -0.52, 1.3, 0.18, 0.18, 10, r2=0.1)
    rama(mat('cana', 0x3a2a1e, 0.5), (0.2, -0.6, 0.85), (-0.5, -0.95, 1.5), 0.02, 0.012, 5)
    cil(blanco(), -0.5, -0.95, 0.02, 0.004, 1.48, 4)

PIEZAS = {
    'ids_center':        (ids_center,        'minneapolis', dict(lado=1024, bisel=0.0)),
    'foshay_tower':      (foshay_tower,      'minneapolis', dict(lado=1024, bisel=0.0)),
    'wells_fargo_mpls':  (wells_fargo_mpls,  'minneapolis', dict(lado=1024, bisel=0.0)),
    'city_hall_mpls':    (city_hall_mpls,    'minneapolis', dict(lado=1024, segmentos=1, min_bisel=1.0)),
    'basilica_mary':     (basilica_mary,     'minneapolis', dict(lado=1024, segmentos=1, min_bisel=1.0)),
    'lago_helado':       (lago_helado,       'minneapolis', dict(lado=2048, bisel=0.0, suelo=False)),
    'cuchara_cereza':    (cuchara_cereza,    'minneapolis', dict(lado=2048, bisel=0.0)),
    'disco_hockey':      (disco_hockey,      'obstaculos', dict(lado=256, bisel=0.0)),
    'porteria_hockey':   (porteria_hockey,   'obstaculos', dict(lado=256, bisel=0.0)),
    'jugador_hockey':    (jugador_hockey,    'obstaculos', dict(lado=256, bisel=0.0)),
    'pancarta_eh':       (pancarta_eh,       'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
    'pulidora_hielo':    (pulidora_hielo,    'obstaculos', dict(lado=512, bisel=0.0)),
    'caseta_pesca':      (caseta_pesca,      'obstaculos', dict(lado=256, bisel=0.0)),
}

correr(PIEZAS)
