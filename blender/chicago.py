# Nivel 11: Chicago, Illinois (08/11/2026).
#
#   blender -b -P blender/chicago.py -- [pieza ...] [--rapido]
#
# Isidro (08/11): «Sigue con Chicago» y «Aplica todas las preguntas que digas
# recomendados». Se aplicó lo recomendado: final delante de la Alubia (Cloud
# Gate, en Millennium Park) y mañana de otoño con viento. Historia: «La ciudad
# del viento: el viento le levanta el tupé».
#   Bajando por Michigan Avenue (la Milla Magnífica) hacia el sur:
#   izquierda:  el John Hancock (la torre negra con las cruces) · la Tribune
#               Tower (la torre gótica)
#   derecha:    la Water Tower (el castillo de piedra) · el Wrigley Building
#               (blanco, con el reloj)
#   en medio:   el puente DuSable sobre el río teñido de verde, con las cuatro
#               casetas de piedra, las banderas tiesas de viento y un barco de
#               turistas; antes del río, a la derecha, la torre Trump con su
#               nombre en letras gigantes
#   al fondo:   Millennium Park y la Alubia (un espejo: su material lo pone el
#               juego)
# Obstáculos (carpeta obstaculos): el paraguas dado la vuelta que cruza
# volando, los periódicos que vuelan (agacharse), la papelera que viene
# rodando, el carrito de perritos de Chicago y la pila de cajas de pizza
# (saltar). Y además: el paraguas que te lleva volando (el momento estrella)
# y el mechón del tupé que levanta el viento.

import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import *
from comun import _poner

def blanco():   return mat('blanco_chi', 0xfbf8f2, 0.5)
def negro():    return mat('negro_chi', 0x1d1f25, 0.4)
def hierro():   return mat('hierro_chi', 0x2c2e33, 0.4)
def rojo():     return mat('rojo_chi', 0xd52b1e, 0.45)
def azul():     return mat('azul_chi', 0x1f3a7a, 0.45)
def celeste():  return mat('celeste_chi', 0x7fc4ec, 0.45)
def dorado():   return mat('dorado_chi', 0xe0b048, 0.25)
def acero():    return mat('acero_chi', 0xd8dde2, 0.25)
def oscuro():   return mat('ventana_os_chi', 0x2c3440, 0.3)
def hormigon(): return mat('hormigon_chi', 0xc4c0b8, 0.75)
def caliza():   return mat_bloques('caliza_chi', 0xeadbb2, 0xcdbb8e, ancho=0.8, alto=0.4, grosor=0.015, variacion=1.06)
def caliza_cl(): return mat_bloques('caliza_clara_chi', 0xe6dfcc, 0xcfc5ad, ancho=1.0, alto=0.5, grosor=0.015, variacion=1.04)
def verde_p():  return mat('verde_puente_chi', 0x56635c, 0.45)

def tronco(m, x, y, z, w0, d0, w1, d1, h):
    """Caja que se estrecha hacia arriba (el Hancock): base w0 x d0 en z,
    techo w1 x d1 en z + h, centrada en (x, y)."""
    me = bpy.data.meshes.new('tronco')
    bm = bmesh.new()
    vs = []
    for (w, d, zz) in ((w0, d0, z), (w1, d1, z + h)):
        vs.append([bm.verts.new((x + sx * w / 2, y + sy * d / 2, zz)) for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1))])
    a, b = vs
    bm.faces.new(list(reversed(a)))
    bm.faces.new(b)
    for i in range(4):
        j = (i + 1) % 4
        bm.faces.new((a[i], a[j], b[j], b[i]))
    bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new('tronco', me)
    bpy.context.collection.objects.link(o)
    return _poner(o, m)

def ventana_gotica(m, x, y, z, w, h, cara='y'):
    """Ventana alta y estrecha con la punta en arco (gótico), en una fachada
    que mira a -y (o a -x / +x con cara='-x' / '+x')."""
    if cara == 'y':
        caja(m, x, y, z, w, 0.12, h)
        fronton(m, x, y - 0.06, z + h, w, w * 0.8, 0.12)
    else:
        s = -1 if cara == '-x' else 1
        caja(m, x, y, z, 0.12, w, h)
        o = fronton(m, 0, 0, 0, w, w * 0.8, 0.12)
        o.rotation_euler = (0, 0, math.pi / 2)
        o.location = (x + s * 0.06, y, z + h)

def sombrilla(mats, cx, cy, z_punta, R=0.69, caida=0.29):
    """Sombrilla o paraguas abierto de ocho gajos: la punta arriba en el
    centro y el borde R más afuera y `caida` más abajo."""
    pend = math.atan2(caida, R)
    largo = math.hypot(R, caida)
    for k in range(8):
        t = k * math.pi / 4
        o = fronton(mats[k % len(mats)], 0, 0, 0, 2 * R * math.sin(math.pi / 8) + 0.02, largo, 0.02)
        o.rotation_euler = (-(math.pi / 2 - pend), 0, t)
        o.location = (cx + R * math.sin(t), cy - R * math.cos(t), z_punta - caida)

def bandera_eeuu(x, y, z, ancho=1.8, alto=1.0):
    """Bandera de EE. UU. tiesa por el viento, hacia +x, en lo alto de su asta."""
    z0 = z - alto
    caja(mat_franjas(f'franjas_chi{z0:.2f}', 0xd8283a, 0xffffff, 7, z0=z0, alto=alto), x + ancho / 2 + 0.05, y, z0, ancho, 0.03, alto)
    caja(azul(), x + 0.05 + ancho * 0.21, y - 0.02, z0 + alto * 0.46, ancho * 0.42, 0.02, alto * 0.54)
    caja(azul(), x + 0.05 + ancho * 0.21, y + 0.02, z0 + alto * 0.46, ancho * 0.42, 0.02, alto * 0.54)

def estrella6(m, x, y, z, r, cara='y'):
    """La estrella roja de seis puntas de la bandera de Chicago (dos triángulos)."""
    for g in (0, math.pi):
        o = fronton(m, 0, 0, 0, r * 1.73, r * 1.5, 0.02)
        o.rotation_euler = (0, g, 0) if cara == 'y' else (0, g, math.pi / 2)
        o.location = (x, y, z - r * 0.5 if g == 0 else z + r * 0.5)

def bandera_chicago(x, y, z, ancho=1.8, alto=1.0):
    """La bandera de Chicago: blanca, dos franjas celestes y cuatro estrellas
    rojas de seis puntas en medio. Tiesa por el viento, hacia +x."""
    z0 = z - alto
    caja(blanco(), x + ancho / 2 + 0.05, y, z0, ancho, 0.03, alto)
    for zz in (z0 + alto * 0.2, z0 + alto * 0.68):
        caja(celeste(), x + ancho / 2 + 0.05, y, zz, ancho, 0.05, alto * 0.13)
    for k in range(4):
        for s in (-1, 1):
            estrella6(rojo(), x + 0.05 + ancho * (0.2 + k * 0.2), y + s * 0.035, z0 + alto * 0.5, alto * 0.09)

# ================================================================ los edificios
def water_tower():
    """La Water Tower de 1869, la que aguantó el gran incendio: un castillo de
    caliza amarilla con torrecillas almenadas en las esquinas y la torre
    octogonal en medio, con su linterna. En su parquecito, separada de la acera."""
    p = caliza()
    os_ = oscuro()
    caja(mat('cesped_wt', 0x6e9a4a, 0.9), 0, 14, 0, 30, 28, 0.06)
    caja(mat('camino_wt', 0xd6ccb4, 0.8), 0, 4.2, 0, 3.4, 8.4, 0.08)
    Y = 15
    caja(p, 0, Y, 0, 13, 13, 12)
    for i in range(-3, 4):
        for (x, y, w, d) in ((i * 1.8, Y - 6.5, 0.9, 0.7), (i * 1.8, Y + 6.5, 0.9, 0.7),
                             (-6.5, Y + i * 1.8, 0.7, 0.9), (6.5, Y + i * 1.8, 0.7, 0.9)):
            caja(p, x, y, 12, w, d, 0.9)
    for sx in (-1, 1):
        for sy in (-1, 1):
            x, y = sx * 6.5, Y + sy * 6.5
            cil(p, x, y, 0, 1.5, 15.5, 8)
            cil(p, x, y, 15.5, 1.8, 0.7, 8)
            cil(p, x, y, 16.2, 1.2, 3.4, 8, r2=0.08)
    f = Y - 6.5
    caja(mat('puerta_wt', 0x4a3424, 0.6), 0, f - 0.05, 0, 2.6, 0.2, 4.4)
    fronton(p, 0, f - 0.4, 4.4, 3.6, 1.8, 0.4)
    for x in (-3.4, 3.4):
        ventana_gotica(os_, x, f - 0.05, 2.0, 1.0, 3.0)
        ventana_gotica(os_, x, f - 0.05, 7.0, 1.0, 2.6)
    for s in (-1, 1):
        for yy in (-3.0, 3.0):
            ventana_gotica(os_, s * 6.55, Y + yy, 2.0, 1.0, 3.0, cara='+x' if s > 0 else '-x')
            ventana_gotica(os_, s * 6.55, Y + yy, 7.0, 1.0, 2.6, cara='+x' if s > 0 else '-x')
    # La torre octogonal, en tres cuerpos que se estrechan.
    for (z, h, r) in ((12, 11, 4.4), (23.8, 9, 3.5), (33.6, 6, 2.6)):
        cil(p, 0, Y, z, r, h, 8).rotation_euler = (0, 0, math.pi / 8)
        cil(p, 0, Y, z + h, r + 0.45, 0.8, 8).rotation_euler = (0, 0, math.pi / 8)
        a = r * math.cos(math.pi / 8)
        for ang in range(8):
            t = ang * math.pi / 4
            px, py = (r + 0.3) * math.cos(t + math.pi / 8), (r + 0.3) * math.sin(t + math.pi / 8)
            cil(p, px, Y + py, z + h + 0.8, 0.3, 1.8, 6, r2=0.03)
        for (cx, cy, cara) in ((0, Y - a - 0.04, 'y'), (-a - 0.04, Y, '-x'), (a + 0.04, Y, '+x')):
            ventana_gotica(os_, cx, cy, z + h * 0.3, 0.9, h * 0.45, cara=cara)
    cil(p, 0, Y, 40.4, 1.9, 3.2, 8).rotation_euler = (0, 0, math.pi / 8)
    cil(mat('pizarra_wt', 0x5a5e66, 0.5), 0, Y, 43.6, 2.2, 3.6, 8, r2=0.12).rotation_euler = (0, 0, math.pi / 8)
    esfera(dorado(), 0, Y, 47.3, 0.25, 1)
    # Dos árboles en el parque.
    for x in (-11, 11):
        rama(mat('tronco_wt', 0x6b4a2f, 0.9), (x, 4, 0), (x, 4, 2.6), 0.22, 0.16)
        for (dx, dz, r) in ((0, 3.6, 1.8), (0.9, 3.0, 1.3), (-0.9, 3.1, 1.3)):
            esfera(mat('hoja_otono', 0xd8902a, 0.8), x + dx, 4, dz, r, 2, esc=(1, 1, 0.85))

def hancock():
    """El John Hancock: la torre negra que se estrecha hacia arriba, con las
    grandes cruces de acero en cada cara y las dos antenas."""
    vid = mat_ventanas('vidrio_hancock', 0x3e4148, 0x16181c, paso_x=1.6, paso_z=1.3, hueco_x=1.3, hueco_z=0.95, variacion=1.12)
    n = mat('acero_hancock', 0x121316, 0.35)
    caja(mat('plaza_hancock', 0xb8b0a4, 0.8), 0, 5, 0, 40, 10, 0.08)
    Y, H = 24, 128.0
    w0, d0, w1, d1 = 34.0, 24.0, 20.0, 14.0
    tronco(vid, 0, Y, 0, w0, d0, w1, d1, H)
    hw = lambda z: (w0 + (w1 - w0) * z / H) / 2
    hd = lambda z: (d0 + (d1 - d0) * z / H) / 2
    N = 5
    for i in range(N + 1):
        z = i * H / N
        caja(n, 0, Y - hd(z) - 0.25, max(0, z - 0.7), 2 * hw(z) + 0.6, 0.5, 1.4)
        for s in (-1, 1):
            caja(n, s * (hw(z) + 0.25), Y, max(0, z - 0.7), 0.5, 2 * hd(z) + 0.6, 1.4)
    for i in range(N):
        za, zb = i * H / N, (i + 1) * H / N
        for (a, b) in ((-1, 1), (1, -1)):
            rama(n, (a * hw(za), Y - hd(za) - 0.3, za), (b * hw(zb), Y - hd(zb) - 0.3, zb), 0.35, 0.35, 4)
            for s in (-1, 1):
                rama(n, (s * (hw(za) + 0.3), Y + a * hd(za), za), (s * (hw(zb) + 0.3), Y + b * hd(zb), zb), 0.35, 0.35, 4)
    for sx in (-1, 1):
        for sy in (-1, 1):
            rama(n, (sx * hw(0), Y + sy * hd(0), 0), (sx * hw(H), Y + sy * hd(H), H), 0.45, 0.45, 4)
    caja(n, 0, Y, H, w1 + 0.4, d1 + 0.4, 2.0)
    for x in (-4.5, 4.5):
        cil(n, x, Y + 2, H + 2, 0.7, 34, 6, r2=0.22)
    caja(mat('vestibulo_hancock', 0x6a7280, 0.2), 0, Y - hd(0) - 0.05, 0, 14, 0.1, 5)

def tribune_tower():
    """La Tribune Tower: la torre neogótica de caliza clara, con los pilares
    verticales, la gran entrada de arco y la corona de arbotantes."""
    p = caliza_cl()
    v = mat_ventanas('ventanas_tribune', 0x46505c, 0xe4dcc8, paso_x=1.5, paso_z=3.4, hueco_x=0.8, hueco_z=2.1, variacion=1.06)
    os_ = oscuro()
    Y = 12
    caja(v, 0, Y, 0, 26, 20, 50)
    for x in range(-12, 13, 3):
        caja(p, x, Y - 10.15, 6, 0.6, 0.3, 44)
    for y in range(-8, 9, 4):
        for s in (-1, 1):
            caja(p, s * 13.15, Y + y, 6, 0.3, 0.6, 44)
    caja(p, 0, Y, 0, 26.4, 20.4, 6)
    # La entrada: el gran arco de tres plantas, con la vidriera.
    caja(p, 0, Y - 10.5, 0, 12, 0.8, 12)
    ventana_gotica(os_, 0, Y - 10.95, 4.2, 5.0, 5.5)
    caja(mat('puerta_trib', 0x3a2a20, 0.5), 0, Y - 10.95, 0, 4, 0.12, 3.8)
    fronton(p, 0, Y - 10.9, 12, 12, 4, 0.8)
    texto(mat('letras_trib', 0x5a4a30, 0.5), 'TRIBUNE TOWER', 0, Y - 10.95, 10.6, tam=0.85, prof=0.04)
    # El remate: un cuerpo más estrecho y la corona octogonal con arbotantes.
    caja(p, 0, Y, 50, 26.4, 20.4, 1.0)
    caja(v, 0, Y, 51, 18, 14, 8)
    caja(p, 0, Y, 59, 18.4, 14.4, 0.8)
    c = cil(v, 0, Y, 59.8, 6.4, 12, 8); c.rotation_euler = (0, 0, math.pi / 8)
    c = cil(p, 0, Y, 71.8, 7.0, 1.0, 8); c.rotation_euler = (0, 0, math.pi / 8)
    for sx in (-1, 1):
        for sy in (-1, 1):
            rama(p, (sx * 8.6, Y + sy * 6.6, 59.8), (sx * 4.4, Y + sy * 4.4, 71.5), 0.45, 0.35, 6)
            cil(p, sx * 8.6, Y + sy * 6.6, 59.8, 0.75, 6.5, 6, r2=0.08)
    for k in range(8):
        t = k * math.pi / 4 + math.pi / 8
        cil(p, 6.6 * math.cos(t), Y + 6.6 * math.sin(t), 72.8, 0.45, 6.5, 6, r2=0.05)
    for k in range(8):
        t = k * math.pi / 4
        a = 6.4 * math.cos(math.pi / 8)
        o = caja(os_, a * math.cos(t), Y + a * math.sin(t), 61.5, 1.2, 0.15, 8)
        o.rotation_euler = (0, 0, t + math.pi / 2)
    cil(p, 0, Y, 72.8, 3.0, 5, 8, r2=1.2).rotation_euler = (0, 0, math.pi / 8)

def wrigley_building():
    """El Wrigley Building: terracota blanca que brilla al sol, con la torre
    del reloj (cuatro esferas), las columnas de arriba y la cúpula."""
    v = mat_ventanas('ventanas_wrigley', 0x52606e, 0xf6f2e8, paso_x=1.4, paso_z=3.4, hueco_x=0.75, hueco_z=1.9, variacion=1.05)
    liso = mat('terracota_wrigley', 0xf4f0e6, 0.5)
    Y = 11
    caja(v, 0, Y, 0, 28, 18, 46)
    caja(liso, 0, Y, 0, 28.4, 18.4, 6)
    caja(liso, 0, Y, 46, 28.8, 18.8, 1.2)
    caja(mat('puerta_wrigley', 0x3a3026, 0.5), 0, Y - 9.25, 0, 5, 0.12, 4)
    texto(mat('letras_wrigley', 0x2a4a7a, 0.5), 'WRIGLEY BUILDING', 0, Y - 9.3, 5.0, tam=0.8, prof=0.04)
    TX, TY = -5.0, Y - 1.0
    caja(v, TX, TY, 47.2, 10, 10, 13)
    caja(liso, TX, TY, 60.2, 11, 11, 7.5)
    caja(liso, TX, TY, 67.7, 11.6, 11.6, 0.8)
    esf, aguja = blanco(), negro()
    for (eje, nx, ny) in (('Y', 0, -1), ('X', -1, 0), ('X', 1, 0)):
        cx, cy = TX + nx * 5.55, TY + ny * 5.55
        tx, ty = -ny, nx                     # a la derecha de quien mira el reloj
        cil(mat('marco_reloj', 0x1d2a4a, 0.4), cx, cy, 64.0, 2.75, 0.14, 24, eje=eje)
        cil(esf, cx + nx * 0.08, cy + ny * 0.08, 64.0, 2.45, 0.14, 24, eje=eje)
        px, py = cx + nx * 0.2, cy + ny * 0.2
        rama(aguja, (px, py, 64.0), (px - 0.9 * tx, py - 0.9 * ty, 64.7), 0.09, 0.07, 4)
        rama(aguja, (px, py, 64.0), (px + 1.2 * tx, py + 1.2 * ty, 65.5), 0.07, 0.05, 4)
    caja(liso, TX, TY, 68.5, 7.5, 7.5, 6)
    for sx in (-1, 1):
        for sy in (-1, 1):
            cil(liso, TX + sx * 4.4, TY + sy * 4.4, 68.5, 0.45, 6, 10)
    caja(liso, TX, TY, 74.5, 9.6, 9.6, 0.8)
    cupula(liso, TX, TY, 75.3, 3.8, 3.4)
    cil(dorado(), TX, TY, 78.6, 0.45, 6, 8, r2=0.04)

def trump_chicago():
    """La torre Trump de Chicago, junto al río: cristal plateado en escalones
    y su nombre en letras de acero gigantes, de cara a la calle y a los dos
    lados (a quien llega). Va en la acera de la derecha, antes del Wrigley."""
    v = mat_ventanas('vidrio_trump_chi', 0x7a94a8, 0xb8c4cc, paso_x=1.5, paso_z=3.3, hueco_x=1.35, hueco_z=2.6, variacion=1.06)
    a = acero()
    Y = 16
    caja(mat('plaza_trump_chi', 0xc8c2b6, 0.8), 0, 20, 0, 40, 40, 0.08)
    escalones = ((34, 30, 0, 30), (28, 24, 30.8, 50), (22, 18, 81.6, 50), (16, 13, 132.4, 30))
    for (w, d, z, h) in escalones:
        caja(v, 0, Y, z, w, d, h)
        caja(a, 0, Y, z + h, w + 0.4, d + 0.4, 0.8)
    cil(a, 0, Y, 163.2, 1.4, 30, 8, r2=0.2)
    caja(mat('vestibulo_trump', 0x4a5a6a, 0.2), 0, Y - 15.05, 0, 12, 0.1, 5)
    # TRUMP: arriba, delante (se ve de lejos), y en la base, delante y a los
    # dos lados (se ve al pasar: la cámara va mirando a la calle).
    texto(a, 'TRUMP', 0, Y - 12.05, 52, tam=7.0, prof=0.5)
    caja(mat('banda_trump', 0x1d2430, 0.3), 0, Y - 15.1, 15.5, 30, 0.2, 7)
    texto(a, 'TRUMP', 0, Y - 15.25, 19, tam=5.5, prof=0.4)
    for s_ in (-1, 1):
        caja(mat('banda_trump', 0x1d2430, 0.3), s_ * 17.1, Y, 15.5, 0.2, 26, 7)
        o = texto(a, 'TRUMP', 0, 0, 0, tam=5.5, prof=0.4)
        o.rotation_euler = (math.pi / 2, 0, s_ * math.pi / 2)
        o.location = (s_ * 17.4, Y, 19)

# ================================================================ el puente y el río
L_PUENTE = 60.0
RIO = 24.0          # el agua va de -24 a 24 (a lo largo de la calle)
AGUA_Z = -7.0

def puente_dusable():
    """El puente DuSable de Michigan Avenue sobre el río Chicago: el tablero
    de acero con sus barandillas, las banderas de EE. UU. y de Chicago tiesas
    por el viento, las cuatro casetas de caliza de las esquinas con sus
    relieves y, abajo, el río teñido de verde con las orillas de piedra.
    Cruza la calle: el origen en el centro de la calle y del puente."""
    L = L_PUENTE
    # El tablero (la calle del puente) y las aceras.
    caja(mat('asfalto_dusable', 0x4a4c52, 0.8), 0, 0, -0.5, 8.4, L, 0.56)
    for s in (-1, 1):
        caja(mat('acera_dusable', 0xc8c2b6, 0.75), s * 6.2, 0, -0.5, 3.6, L, 0.68)
        caja(verde_p(), s * 8.2, 0, -2.8, 0.5, L, 2.4)                 # el canto de acero
        caja(verde_p(), s * 8.2, 0, 0.18, 0.12, L, 0.1)
        caja(verde_p(), s * 8.2, 0, 1.2, 0.14, L, 0.12)
        for k in range(30):
            caja(verde_p(), s * 8.2, -L / 2 + 1 + k * 2, 0.18, 0.1, 0.1, 1.05)
        # Las banderas, tiesas de viento (hacia +x, como sopla del lago).
        for k in range(5):
            y = -20 + k * 10
            cil(mat('asta_chi', 0xd8d8d8, 0.3), s * 8.2, y, 0.18, 0.05, 6.2, 8)
            esfera(dorado(), s * 8.2, y, 6.45, 0.09, 1)
            if (k + (s > 0)) % 2:
                bandera_eeuu(s * 8.2, y, 6.3)
            else:
                bandera_chicago(s * 8.2, y, 6.3)
    # Las vigas de debajo, de orilla a orilla.
    for x in (-4.6, 0, 4.6):
        caja(verde_p(), x, 0, -2.6, 0.5, L, 2.1)
    # Las cuatro casetas del puente, en las orillas.
    p = caliza_cl()
    rel = mat('relieve_dusable', 0xcbbf9e, 0.6)
    for sy in (-1, 1):
        for sx in (-1, 1):
            cx, cy = sx * 13.5, sy * (RIO + 3.0)
            caja(p, cx, cy, AGUA_Z, 7, 6, -AGUA_Z + 11)
            caja(p, cx, cy, 11, 7.6, 6.6, 0.9)
            caja(p, cx, cy, 11.9, 6.0, 5.0, 1.2)
            cara = cx - sx * 3.55
            o = caja(rel, cara, cy, 2.0, 0.2, 4.2, 7.0)
            # El relieve: figuras sencillas en la piedra.
            for k in (-1, 0, 1):
                esfera(rel, cara - sx * 0.12, cy + k * 1.2, 6.2 + abs(k) * -0.6, 0.45, 1, esc=(0.4, 1, 1.3))
                caja(rel, cara - sx * 0.12, cy + k * 1.2, 2.6, 0.2, 0.7, 3.0)
            for y in (cy - 2.2, cy + 2.2):
                ventana_gotica(oscuro(), cara - sx * 0.02, y, 3.0, 0.7, 2.0, cara='+x' if sx < 0 else '-x')
    # El río y las orillas: muros de piedra, el paseo de abajo y el suelo de arriba.
    caja(mat('rio_verde', 0x23a06a, 0.15), 0, 0, AGUA_Z - 0.2, 420, 2 * RIO, 0.2)
    for sy in (-1, 1):
        y0 = sy * RIO
        caja(mat('muro_rio', 0x9a9488, 0.8), 0, y0 + sy * 0.5, AGUA_Z, 420, 1.0, -AGUA_Z)
        caja(mat('paseo_rio', 0xb8b2a6, 0.8), sy * 0 + 0, y0 - sy * 2.0, AGUA_Z, 420, 4.0, 1.4)
        caja(mat('suelo_orilla', 0xb8b4ac, 0.85), 0, y0 + sy * 3.5, -0.12, 420, 7.0, 0.1)
        for k in range(14):
            x = -150 + k * 23 + (7 if sy > 0 else 0)
            if abs(x) < 18:
                continue
            rama(mat('tronco_rio', 0x6b4a2f, 0.9), (x, y0 + sy * 4.5, 0), (x, y0 + sy * 4.5, 2.4), 0.2, 0.14)
            esfera(mat('hoja_rio', 0x5a9a3e if k % 3 else 0xd8902a, 0.8), x, y0 + sy * 4.5, 3.3, 1.6, 2, esc=(1, 1, 0.9))
    # Marina City, las dos torres-mazorca, en la otra orilla, a la derecha.
    mz = mat('hormigon_marina', 0xdcd6ca, 0.7)
    for (x, y) in ((52, RIO + 20), (72, RIO + 20)):
        cil(mz, x, y, 0, 6.5, 62, 16)
        for z in range(4, 62, 3):
            cil(mz, x, y, z, 8.2, 0.35, 16)
        cil(mz, x, y, 62, 7.0, 1.0, 16)

def barco():
    """El barco de turistas del río (los de la ruta de arquitectura): casco
    blanco con la franja azul, la cubierta con la gente sentada y la cabina
    de delante. Navega a lo ancho del río (hacia +x)."""
    caja(blanco(), 0, 0, 0, 20, 5, 1.6)
    cil(blanco(), 10, 0, 0, 2.5, 1.6, 12).scale = (1.2, 1, 1)
    caja(azul(), 1, 0, 0.9, 21.5, 5.08, 0.35)
    caja(mat('cubierta_barco', 0x9a7a5a, 0.7), 0, 0, 1.6, 19, 4.6, 0.1)
    caja(mat('cabina_barco', 0x3a5a7a, 0.2), 7.5, 0, 1.7, 3, 4.0, 1.6)
    caja(blanco(), 7.5, 0, 3.3, 3.4, 4.4, 0.2)
    pieles = [0xf1c8a0, 0xd9a47a, 0x8a5a3a, 0xf6d6b4]
    ropas = [0xd52b1e, 0x2a5aa8, 0xf2c230, 0x2fa84f, 0xffffff, 0x7a3aa8]
    for i in range(6):
        for j in range(3):
            x, y = -7.5 + i * 2.2, -1.5 + j * 1.5
            caja(mat('banco_barco', 0x5a6a7a, 0.6), x, y, 1.7, 0.8, 1.2, 0.45)
            cil(mat(f'ropa_barco{(i + j) % 6}', ropas[(i * 3 + j) % 6], 0.6), x, y, 2.15, 0.22, 0.55, 8, r2=0.17)
            esfera(mat(f'piel_barco{(i + j) % 4}', pieles[(i + j * 2) % 4], 0.6), x, y, 2.9, 0.17, 1)

def cloud_gate():
    """La meta: Millennium Park. La plaza de granito con la Alubia en medio
    (la pone el juego, de espejo), los árboles de los lados, el murete de la
    entrada con su nombre y, detrás, los rascacielos de Randolph Street: el
    Aon (blanco), el Two Prudential (con la aguja) y el del tejado en diamante."""
    # La plaza va 30 cm por encima de la calle (un escalón): si no, el asfalto
    # de la calle se veía por encima de ella hasta la Alubia.
    Z = 0.3
    caja(mat('granito_mp', 0xc9c4ba, 0.8), 0, 30, 0, 100, 60, Z)
    caja(mat('bordillo_mp', 0xb0aaa0, 0.7), 0, 0.2, 0, 100, 0.4, Z + 0.02)
    caja(mat('cesped_mp', 0x6e9a4a, 0.9), -38, 30, Z, 24, 60, 0.06)
    caja(mat('cesped_mp', 0x6e9a4a, 0.9), 38, 30, Z, 24, 60, 0.06)
    for s in (-1, 1):
        caja(caliza_cl(), s * 18, 2.5, Z, 14, 1.2, 1.2)
        for k in range(6):
            y = 8 + k * 9
            rama(mat('tronco_mp', 0x6b4a2f, 0.9), (s * 34, y, Z), (s * 34, y, Z + 3.0), 0.25, 0.18)
            esfera(mat('hoja_mp', 0xd8902a if k % 2 else 0xc8602e, 0.8), s * 34, y, Z + 4.2, 2.2, 2, esc=(1, 1, 0.85))
    texto(mat('letras_mp', 0x3a3a3a, 0.5), 'MILLENNIUM PARK', -18, 1.85, Z + 0.6, tam=0.45, prof=0.03)
    texto(mat('letras_mp', 0x3a3a3a, 0.5), 'CLOUD GATE', 18, 1.85, Z + 0.6, tam=0.45, prof=0.03)
    # Los rascacielos de detrás.
    aon = mat_ventanas('ventanas_aon', 0x8a96a2, 0xeeeeea, paso_x=1.2, paso_z=3.4, hueco_x=0.55, hueco_z=2.6, variacion=1.04)
    caja(aon, -8, 120, 0, 34, 34, 150)
    caja(mat('remate_aon', 0xe6e6e2, 0.5), -8, 120, 150, 34.6, 34.6, 2)
    pru = mat_ventanas('ventanas_pru', 0x6a7a8a, 0xd8d2c6, paso_x=1.4, paso_z=3.3, hueco_x=1.0, hueco_z=2.2, variacion=1.05)
    caja(pru, 34, 105, 0, 26, 26, 112)
    for k, (w, h) in enumerate(((22, 8), (17, 7), (12, 6))):
        z = 112 + k * 7
        caja(pru, 34, 105, z, w, w, h)
    cil(mat('aguja_pru', 0xc8ccd2, 0.3), 34, 105, 133, 2.0, 30, 4, r2=0.1).rotation_euler = (0, 0, math.pi / 4)
    dia = mat_ventanas('ventanas_diamante', 0x5a6c80, 0xe2e0da, paso_x=1.4, paso_z=3.4, hueco_x=1.0, hueco_z=2.3, variacion=1.05)
    caja(dia, -48, 100, 0, 26, 26, 96)
    o = fronton(dia, -48, 87, 96, 26, 26, 26)
    caja(mat_ventanas('ventanas_fondo_mp', 0x6a7684, 0xcfcac0, paso_x=1.4, paso_z=3.3, hueco_x=0.9, hueco_z=2.0), 70, 90, 0, 30, 30, 70)
    caja(mat_ventanas('ventanas_fondo_mp2', 0x5a6a7c, 0xbfb8aa, paso_x=1.4, paso_z=3.3, hueco_x=0.9, hueco_z=2.0), -78, 85, 0, 30, 30, 60)

def alubia():
    """Cloud Gate, «la Alubia»: la gota de acero de 20 x 13 x 10 m con el arco
    de debajo (el ónfalo) por el que pasa la gente. Solo la forma: el juego le
    pone un espejo (lo que refleja es el cielo, la ciudad y la plaza)."""
    bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32, radius=1, location=(0, 0, 0))
    o = bpy.context.object
    bm = bmesh.new(); bm.from_mesh(o.data)
    RX, RY, RZ, CZ = 10.0, 6.5, 5.2, 4.7
    for v in bm.verts:
        u, w, h = v.co.x, v.co.y, v.co.z
        x, y, z = u * RX, w * RY, CZ + h * RZ
        if h < 0:
            # El arco de debajo: sube en medio y deja dos «pies» a los lados.
            arco = max(0.0, 1 - (u / 0.6) ** 2 - (w / 0.85) ** 2)
            z = max(0.0, z) + 3.6 * math.sqrt(arco) * (-h)
        v.co = (x, y, z)
    bm.to_mesh(o.data); bm.free()
    _poner(o, mat('espejo_alubia', 0xd8dde2, 0.1))

# ================================================================ obstáculos
def paraguas_volando():
    """Un paraguas negro dado la vuelta por el viento, que cruza la calle
    volando y dando vueltas: la tela hacia arriba, las varillas a la vista y
    el mango curvo. Va centrado en su eje (el juego lo hace girar)."""
    tela = mat('tela_paraguas', 0x22242a, 0.6)
    var = mat('varilla_paraguas', 0xb8bcc2, 0.3)
    Z = 1.0
    cil(var, 0, 0, Z - 0.45, 0.025, 1.25, 6)
    rama(mat('mango_paraguas', 0x6a3a1e, 0.5), (0, 0, Z - 0.45), (0.08, 0, Z - 0.6), 0.04, 0.04, 6)
    rama(mat('mango_paraguas', 0x6a3a1e, 0.5), (0.08, 0, Z - 0.6), (0.18, 0, Z - 0.5), 0.04, 0.04, 6)
    # La tela dada la vuelta: un cono abierto hacia arriba con ocho gajos.
    cil(tela, 0, 0, Z + 0.25, 0.08, 0.45, 8, r2=0.62)
    for k in range(8):
        t = k * math.pi / 4
        rama(var, (0.06 * math.cos(t), 0.06 * math.sin(t), Z + 0.25), (0.66 * math.cos(t), 0.66 * math.sin(t), Z + 0.72), 0.015, 0.015, 4)
        esfera(var, 0.66 * math.cos(t), 0.66 * math.sin(t), Z + 0.72, 0.03, 1)

def periodicos():
    """Un remolino de periódicos (el Tribune) volando a la altura de la cabeza:
    se pasa agachado. Hojas abiertas, con las columnas de letra."""
    hojas = [mat_franjas('papel_chi', 0xf2efe6, 0xb8b4aa, 9, eje='Z', z0=1.2, alto=1.0),
             mat('papel_chi2', 0xf6f3ea, 0.7)]
    pos = ((-0.6, 0.0, 1.55, 0.3, 0.2), (0.0, 0.1, 1.85, -0.4, 0.6), (0.6, -0.1, 1.5, 0.5, -0.3),
           (-0.25, 0.15, 2.1, 0.1, 1.1), (0.35, 0.05, 2.15, -0.2, -0.9), (0.05, -0.1, 1.4, 0.0, 0.0))
    for k, (x, y, z, rx, rz) in enumerate(pos):
        o = caja(hojas[k % 2], x, y, z, 0.62, 0.02, 0.44)
        o.rotation_euler = (rx, 0.25 * k, rz)
        if k in (1, 4):
            o = texto(negro(), 'TRIBUNE', 0, 0, 0, tam=0.08, prof=0.005)
            o.rotation_euler = (math.pi / 2 + rx, 0.25 * k, rz)
            o.location = (x, y - 0.02, z + 0.36)

def papelera():
    """La papelera de las calles de Chicago, volcada por el viento y rodando
    hacia ti: el cubo de metal oscuro con su tapa y la estrella de la ciudad.
    Centrada en su eje (rueda sobre el eje x)."""
    met = mat_bloques('chapa_papelera', 0x2f3a34, 0x24302a, ancho=0.12, alto=2.0, grosor=0.01, variacion=1.04)
    cil(met, 0, 0, 0, 0.4, 1.0, 16, eje='X')
    for x in (-0.48, 0.48):
        cil(mat('aro_papelera', 0x1d2420, 0.4), x, 0, 0, 0.42, 0.06, 16, eje='X')
    cil(mat('tapa_papelera', 0x1d2420, 0.5), -0.53, 0, 0, 0.36, 0.05, 16, eje='X')
    caja(blanco(), 0, -0.405, -0.15, 0.4, 0.02, 0.3)
    estrella6(rojo(), 0, -0.42, 0.0, 0.11)

def carrito_perritos():
    """El carrito de perritos al estilo de Chicago: el carro de acero con su
    sombrilla de rayas y, encima, el perrito gigante con mostaza amarilla,
    pepinillo, tomate y relish verde fosforito."""
    a = acero()
    caja(a, 0, 0, 0.35, 1.8, 0.9, 0.75)
    caja(rojo(), 0, -0.46, 0.55, 1.8, 0.02, 0.3)
    texto(blanco(), 'CHICAGO HOT DOGS', 0, -0.48, 0.7, tam=0.13, prof=0.01)
    for x in (-0.6, 0.6):
        cil(negro(), x, 0, 0.18, 0.18, 0.12, 12, eje='Y').location = (x, -0.5, 0.18)
        cil(negro(), x, 0, 0.18, 0.18, 0.12, 12, eje='Y').location = (x, 0.5, 0.18)
    cil(a, 0, 0, 1.1, 0.03, 1.1, 6)
    sombrilla([mat('sombrilla_roja', 0xd52b1e, 0.5), mat('sombrilla_amarilla', 0xf2c230, 0.5)], 0, 0, 2.15, R=0.95, caida=0.4)
    # El perrito gigante.
    pan = mat('pan_perrito', 0xe2a85a, 0.7)
    caja(pan, 0, 0, 1.12, 1.3, 0.42, 0.22)
    cil(mat('salchicha', 0xa8442a, 0.5), 0, 0, 1.38, 0.13, 1.6, 12, eje='X')
    for k in range(5):
        esfera(mat('mostaza', 0xf2d21a, 0.4), -0.5 + k * 0.25, 0, 1.52, 0.07, 1, esc=(1.6, 0.8, 0.6))
    caja(mat('pepinillo', 0x4a8a2a, 0.6), 0.25, 0.14, 1.36, 0.7, 0.1, 0.12)
    for x in (-0.5, -0.25):
        cil(mat('tomate_perrito', 0xd8302a, 0.5), x, -0.14, 1.36, 0.1, 0.06, 10, eje='Y')
    esfera(mat('relish', 0x5ae03a, 0.5), -0.1, 0, 1.53, 0.08, 1, esc=(2.5, 0.8, 0.6))

def cajas_pizza():
    """La pila de cajas de pizza de Chicago (la de molde hondo) y, encima,
    una abierta con la pizza: borde alto y tomate por encima. Se salta."""
    carton = mat('carton_pizza', 0xe6d2a8, 0.8)
    for k in range(4):
        o = caja(carton, 0.03 * (k % 2), 0, k * 0.17, 0.85, 0.85, 0.16)
        o.rotation_euler = (0, 0, 0.08 * (k - 1.5))
        if k % 2 == 0:
            texto(rojo(), 'DEEP DISH', 0, -0.44, k * 0.17 + 0.08, tam=0.09, prof=0.01)
    caja(carton, 0, 0, 0.68, 0.85, 0.85, 0.04)
    o = caja(carton, 0, 0.43, 0.7, 0.85, 0.04, 0.85)
    o.rotation_euler = (-0.35, 0, 0)
    cil(mat('borde_pizza', 0xc8883a, 0.7), 0, 0, 0.72, 0.38, 0.16, 18)
    cil(mat('tomate_pizza', 0xc8301e, 0.5), 0, 0, 0.76, 0.33, 0.13, 18)
    for (x, y) in ((-0.15, -0.1), (0.12, 0.08), (0.05, -0.18), (-0.1, 0.16)):
        esfera(mat('queso_pizza', 0xf2e0a8, 0.6), x, y, 0.89, 0.05, 1, esc=(1, 1, 0.4))

def paraguas_vuelo():
    """El paraguas que te lleva volando (el momento del viento): abierto, con
    los gajos de la bandera de Chicago (blanco y celeste) y la punta roja. El
    mango abajo, en el origen."""
    cil(mat('palo_vuelo', 0x2c2e33, 0.4), 0, 0, 0, 0.03, 1.15, 6)
    rama(mat('mango_vuelo', 0x6a3a1e, 0.5), (0, 0, 0), (0.1, 0, -0.14), 0.04, 0.04, 6)
    rama(mat('mango_vuelo', 0x6a3a1e, 0.5), (0.1, 0, -0.14), (0.2, 0, -0.04), 0.04, 0.04, 6)
    sombrilla([celeste(), blanco()], 0, 0, 1.22, R=0.72, caida=0.3)
    esfera(rojo(), 0, 0, 1.24, 0.06, 1)
    cil(rojo(), 0, 0, 1.24, 0.02, 0.18, 6)

def tupe_viento():
    """El mechón del tupé que levanta el viento: una lámina de pelo rubio,
    curvada y con mechas. La bisagra en el origen (atrás) y el pelo hacia
    delante (-y): el juego la levanta girándola."""
    pelo = mat_franjas('mechas_tupe', 0xe2c472, 0xc9a654, 10, eje='X', z0=-0.13, alto=0.26)
    for k in range(4):
        y0, y1 = -k * 0.06, -(k + 1) * 0.06 - 0.01
        caja(pelo, 0, (y0 + y1) / 2, -0.01 * k * k * 0.5, 0.25 - 0.012 * k, abs(y1 - y0), 0.035)
    esfera(pelo, 0, -0.255, -0.03, 0.12, 2, esc=(1.05, 0.35, 0.18))

PIEZAS = {
    'water_tower':       (water_tower,       'chicago', dict(lado=1024, segmentos=2, min_bisel=1.0)),
    'hancock':           (hancock,           'chicago', dict(lado=1024, bisel=0.0)),
    'tribune_tower':     (tribune_tower,     'chicago', dict(lado=1024, segmentos=1, min_bisel=1.0)),
    'wrigley_building':  (wrigley_building,  'chicago', dict(lado=1024, segmentos=1, min_bisel=1.0)),
    'trump_chicago':     (trump_chicago,     'chicago', dict(lado=1024, bisel=0.0)),
    'puente_dusable':    (puente_dusable,    'chicago', dict(lado=2048, bisel=0.0, suelo=False)),
    'barco':             (barco,             'chicago', dict(lado=512, bisel=0.0, suelo=False)),
    'cloud_gate':        (cloud_gate,        'chicago', dict(lado=2048, bisel=0.0)),
    'alubia':            (alubia,            'chicago', dict(lado=256, bisel=0.0, suelo=False)),
    'paraguas_volando':  (paraguas_volando,  'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
    'periodicos':        (periodicos,        'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
    'papelera':          (papelera,          'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
    'carrito_perritos':  (carrito_perritos,  'obstaculos', dict(lado=512, bisel=0.0)),
    'cajas_pizza':       (cajas_pizza,       'obstaculos', dict(lado=256, bisel=0.0)),
    'paraguas_vuelo':    (paraguas_vuelo,    'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
    'tupe_viento':       (tupe_viento,       'obstaculos', dict(lado=128, bisel=0.0, suelo=False)),
}

correr(PIEZAS)
