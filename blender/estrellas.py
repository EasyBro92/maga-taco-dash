# Los momentos estrella de cada ciudad (07/11/2026). El de Nueva York, el
# metro, va aparte (metro.py). Isidro eligió:
#   Findlay      túnel de banderas gigantes y se corre por encima de las carrozas
#   Phoenix      puente de madera del tren sobre un cañón rojo
#   Las Vegas    dentro del casino Trump, con lluvia de fichas al salir
#   Des Moines   la Feria del Estado (vaca de mantequilla, puestos, noria, cerdos)
#   Washington   dentro del Capitolio (la rotonda, estatuas, alfombras, guardias)
#
#   blender -b -P blender/estrellas.py -- [pieza ...] [--rapido] [--luces]
#
# Las piezas que cruzan la calle: origen en el centro de la calle y en el
# centro de su largo, x de lado a lado y +y hacia delante. Los obstáculos:
# caben en un carril, miran al jugador por -y y empiezan en y = 0.

import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import *

def blanco():  return mat('blanco_e', 0xfbf9f3, 0.5)
def rojo():    return mat('rojo_e', 0xd8283a, 0.45)
def azul():    return mat('azul_e', 0x23408f, 0.45)
def oro():     return mat('oro_e', 0xe0b040, 0.3)
def negro():   return mat('negro_e', 0x1d1f25, 0.4)

def estrella(m, x, y, z, r, grosor=0.03, eje='Y'):
    """Estrella de cinco puntas plana: mira a -y (eje 'Y'), a ±x (eje 'X') o arriba ('Z')."""
    me = bpy.data.meshes.new('estrella')
    bm = bmesh.new()
    def p(ang, rr, d):
        u, v = math.sin(ang) * rr, math.cos(ang) * rr
        if eje == 'X': return (x + d, y + u, z + v)
        return (x + u, y + d, z + v) if eje == 'Y' else (x + u, y + v, z + d)
    caras = []
    for d in (0, grosor):
        anillo = [bm.verts.new(p(i * math.pi / 5, r if i % 2 == 0 else r * 0.42, d)) for i in range(10)]
        centro = bm.verts.new(p(0, 0, d))
        for i in range(10):
            bm.faces.new((centro, anillo[i], anillo[(i + 1) % 10]) if d == 0 else (centro, anillo[(i + 1) % 10], anillo[i]))
        caras.append(anillo)
    for i in range(10):
        j = (i + 1) % 10
        bm.faces.new((caras[0][i], caras[0][j], caras[1][j], caras[1][i]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new('estrella', me)
    bpy.context.scene.collection.objects.link(o)
    from comun import _poner
    return _poner(o, m)

def cuña(nombre, m, w, largo, alto, y0=0.0):
    me = bpy.data.meshes.new(nombre)
    bm = bmesh.new()
    pts = []
    for x in (-w / 2, w / 2):
        pts.append([bm.verts.new((x, y0, 0)), bm.verts.new((x, y0 + largo, 0)), bm.verts.new((x, y0 + largo, alto))])
    a, b = pts
    bm.faces.new(a); bm.faces.new(b[::-1])
    for i in range(3):
        j = (i + 1) % 3
        bm.faces.new((a[j], a[i], b[i], b[j]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(nombre, me)
    bpy.context.scene.collection.objects.link(o)
    from comun import _poner
    return _poner(o, m)

def bandera_colgada(x, y, z_arriba, ancho, alto, lado=1):
    """Bandera de EE. UU. colgada en vertical (franjas verticales y el cantón
    arriba a la izquierda vista desde la calle). `lado` hacia donde mira."""
    franjas = mat_franjas('franjas_colgada', 0xd8283a, 0xfbf9f3, 13, eje='X', z0=x - ancho / 2, alto=ancho)
    caja(franjas, x, y, z_arriba - alto, ancho, 0.04, alto)
    cw, ch = ancho * 0.4, alto * 0.53
    cx = x - ancho / 2 + cw / 2 if lado > 0 else x + ancho / 2 - cw / 2
    caja(azul(), cx, y - 0.03, z_arriba - ch, cw, 0.04, ch)
    caja(azul(), cx, y + 0.03, z_arriba - ch, cw, 0.04, ch)
    for f in range(4):
        for c in range(3):
            sx = cx - cw / 2 + cw * (c + 0.5) / 3
            sz = z_arriba - ch * (f + 0.5) / 4
            estrella(blanco(), sx, y - 0.06, sz, min(cw, ch) * 0.1, 0.01)
            estrella(blanco(), sx, y + 0.06, sz, min(cw, ch) * 0.1, 0.01)


# ================================================================ Findlay
def banderas_arco():
    """Findlay, «la ciudad de las banderas», el 4 de julio: dos mástiles en
    las aceras con un cable de lado a lado, una bandera gigante colgada sobre
    cada acera y, por encima de la calle, guirnaldas de abanicos rojos,
    blancos y azules (altas: la cámara pasa por debajo)."""
    poste = mat('mastil', 0xf2f0ea, 0.4)
    for s in (-1, 1):
        cil(poste, s * 10.4, 0, 0, 0.14, 11.4, 12)
        cil(mat('base_mastil', 0x5a5650, 0.6), s * 10.4, 0, 0, 0.3, 0.5, 12)
        esfera(oro(), s * 10.4, 0, 11.55, 0.22, 2)
        # La bandera gigante, colgada sobre la acera.
        bandera_colgada(s * 7.6, 0.0, 10.6, 3.8, 6.2, lado=-s)
    caja(mat('cable', 0x2a2c31, 0.5), 0, 0, 10.75, 20.8, 0.05, 0.05)
    # Las guirnaldas en abanico sobre la calle (de 9,6 a 10,7 m).
    for k, x in enumerate((-4.2, -2.1, 0.0, 2.1, 4.2)):
        for j, (c, r) in enumerate(((0xd8283a, 1.0), (0xfbf9f3, 0.78), (0x23408f, 0.5))):
            o = cil(mat('abanico_%d' % j, c, 0.5), x, -0.02 * j, 10.7, r, 0.03, 20, eje='Y')
            o.scale = (1, 1, 1)
        caja(mat('cable', 0x2a2c31, 0.5), x, 0.04, 10.7, 2.1, 0.06, 0.06)
    # (Se queda solo la mitad de abajo de cada abanico.)
    import bmesh as _b
    bpy.context.view_layer.update()
    for o in list(bpy.context.scene.objects):
        if o.type == 'MESH' and o.data.materials and o.data.materials[0].name.startswith('abanico_'):
            bm = _b.new(); bm.from_mesh(o.data)
            mw = o.matrix_world
            _b.ops.delete(bm, geom=[v for v in bm.verts if (mw @ v.co).z > 10.72], context='VERTS')
            bm.to_mesh(o.data); bm.free()

def carroza_desfile():
    """Carroza del desfile del 4 de julio con rampa detrás: la cubierta a
    1,4 m es una alfombra azul con estrellas (se corre por encima) y las
    faldas son de franjas. Delante, un águila dorada y dos banderas en las
    esquinas (el centro queda libre)."""
    W, R, H, L = 2.0, 2.4, 1.4, 9.5
    cuña('rampa_carroza', mat_franjas('rampa_carroza_rayas', 0xffd21a, 0x1d1f25, 9, eje='Y', z0=0, alto=R), W - 0.1, R, H)
    caja(mat_franjas('falda_carroza', 0xd8283a, 0xfbf9f3, 18, eje='Y', z0=R, alto=L - R), 0, R + (L - R) / 2, 0.08, W + 0.06, L - R, H - 0.12)
    caja(azul(), 0, R + (L - R) / 2, H - 0.06, W, L - R, 0.06)
    for k in range(5):
        for s in (-1, 1):
            estrella(blanco(), s * 0.6, R + 0.8 + k * 1.3, H + 0.001, 0.18, 0.006, eje='Z')
    caja(oro(), 0, R + (L - R) / 2, H - 0.14, W + 0.1, L - R + 0.1, 0.06)
    # Las esquinas de delante: banderas en sus mástiles.
    for s in (-1, 1):
        cil(oro(), s * 0.88, L - 0.25, H, 0.04, 2.6, 8)
        caja(mat_franjas('banderita', 0xd8283a, 0xfbf9f3, 7, eje='Z', z0=H + 1.8, alto=0.8), s * 0.88 + s * 0.6, L - 0.25, H + 1.8, 1.2, 0.03, 0.8)
        caja(azul(), s * 0.88 + s * 0.35, L - 0.25 - 0.02, H + 2.2, 0.5, 0.03, 0.4)
    # El águila, delante y baja (por debajo de lo que se ve corriendo encima).
    esfera(mat('aguila_cuerpo', 0x5a3a22, 0.6), 0, L + 0.3, 0.9, 0.5, 2, esc=(1, 0.8, 1.1))
    esfera(blanco(), 0, L + 0.5, 1.45, 0.26, 2)
    cil(oro(), 0, L + 0.78, 1.42, 0.08, 0.2, 8, r2=0.01, eje='Y')
    for s in (-1, 1):
        caja(mat('aguila_ala', 0x4a2e1a, 0.6), s * 0.9, L + 0.2, 0.8, 1.2, 0.2, 0.5, giro=s * 0.3, inclina=0.2)
    # Las ruedas, casi tapadas por la falda.
    for y in (R + 1.2, L - 1.2):
        for s in (-1, 1):
            cil(mat('rueda_carroza', 0x1d1e21, 0.8), s * 0.92, y, 0.3, 0.3, 0.2, 14, eje='X')


# ================================================================ Las Vegas
PARED_V = 8.3                 # lo que sobresale de las fachadas (a 11,5) llega hasta 8,5
TECHO_V = 11.0
def oro_v():      return mat('oro_casino', 0xe8b84a, 0.25)
# (07/11: mas claros: Isidro dijo que Las Vegas era oscura y no se veian los obstaculos.)
def granate():    return mat('granate_casino', 0x9a2a3e, 0.5)
def moqueta():    return mat_bloques('moqueta_casino', 0xa8263a, 0x962032, ancho=2.4, alto=2.4, grosor=0.04, variacion=1.03)
def cristal_n():  return mat('cristal_negro', 0x6a5040, 0.15)
def bombilla():   return luz('bombilla_casino', 0xffe2a8, 1.6)

def tragaperras_fila(x, y0, n, lado):
    """Una fila de tragaperras mirando al pasillo (lado: hacia donde miran, -1 = -x)."""
    pantallas = [luz('pantalla_%d' % k, c, 1.1) for k, c in enumerate((0x6fd0ff, 0xff7ad0, 0xffd04a))]
    for k in range(n):
        y = y0 + k * 0.85
        caja(mat('mueble_slot', 0x2a2c3a, 0.4), x, y, 0.3, 0.7, 0.75, 1.7)
        caja(pantallas[k % 3], x + lado * 0.36, y, 1.1, 0.02, 0.55, 0.6)
        caja(oro_v(), x + lado * 0.36, y, 1.85, 0.02, 0.6, 0.12)
        cil(mat('taburete', 0x8a1a2a, 0.5), x + lado * 0.85, y, 0.3, 0.2, 0.55, 10)

def casino_sala():
    """Un trozo de 30 m del casino Trump por dentro: moqueta granate, filas
    de tragaperras a los lados sobre una tarima, mesas de ruleta y de cartas,
    columnas doradas, paredes de espejo y oro, letreros de neón y lámparas de
    araña colgando sobre la calle (altas: la cámara pasa por debajo)."""
    L = 30.0
    W = PARED_V
    caja(moqueta(), 0, 0, 0, 7.8, L, 0.09)                     # el pasillo, por encima de las rayas
    for s in (-1, 1):
        caja(moqueta(), s * (3.9 + (W - 3.9) / 2), 0, 0, W - 3.9, L, 0.3)   # la tarima
        caja(oro_v(), s * 3.92, 0, 0, 0.06, L, 0.32)
        # Tragaperras junto a la pared y mesas entre las columnas.
        tragaperras_fila(s * 7.4, -L / 2 + 1.0, 33, -s)
        for y in (-7.5, 7.5):
            cil(mat('tapete', 0x1f6a3a, 0.7), s * 5.6, y, 0.3, 1.0, 0.9, 20)
            cil(oro_v(), s * 5.6, y, 1.2, 1.05, 0.06, 20)
            cil(mat('ruleta_c', 0x2a1810, 0.5), s * 5.6, y, 1.26, 0.35, 0.08, 18)
        for y in (0.0,):
            caja(mat('tapete', 0x1f6a3a, 0.7), s * 5.6, y, 0.3, 1.2, 2.4, 0.9)
            caja(oro_v(), s * 5.6, y, 1.2, 1.3, 2.5, 0.05)
        # La pared: espejo oscuro con marcos dorados y los neones.
        caja(cristal_n(), s * (W + 0.1), 0, 0.3, 0.2, L, TECHO_V - 0.3)
        for y in (-12, -4, 4, 12):
            caja(oro_v(), s * (W - 0.02), y, 0.3, 0.06, 0.18, TECHO_V - 0.3)
        caja(oro_v(), s * (W - 0.02), 0, 3.6, 0.06, L, 0.12)
        for y, texto_n, c in ((-7.5, 'SLOTS', 0xff5ad0), (7.5, '777', 0x6fe0ff)):
            o = texto(luz('neon_%s' % texto_n, c, 1.8), texto_n, 0, 0, 0, tam=1.1, prof=0.05)
            o.rotation_euler = (math.pi / 2, 0, -s * math.pi / 2)   # (mirando al pasillo)
            o.location = (s * (W - 0.08), y, 5.0)
        # Columnas doradas.
        for y in (-11.25, -3.75, 3.75, 11.25):
            cil(oro_v(), s * 4.25, y, 0.3, 0.28, TECHO_V - 0.3, 16)
            cil(oro_v(), s * 4.25, y, 0.3, 0.42, 0.4, 16)
            cil(oro_v(), s * 4.25, y, TECHO_V - 0.6, 0.42, 0.5, 16)
    # El techo artesonado y las lámparas de araña.
    caja(granate(), 0, 0, TECHO_V, W * 2 + 0.4, L, 0.4)
    for y in (-11.25, -3.75, 3.75, 11.25):
        caja(oro_v(), 0, y, TECHO_V - 0.35, W * 2, 0.3, 0.35)
    for y in (-7.5, 7.5):
        for x in (-2.2, 2.2):
            cil(oro_v(), x, y, 10.2, 0.03, 0.8, 6)
            cil(oro_v(), x, y, 9.9, 0.9, 0.08, 16)
            for k in range(8):
                a = k * math.pi / 4
                esfera(bombilla(), x + math.cos(a) * 0.8, y + math.sin(a) * 0.8, 10.05, 0.09, 1)
            esfera(mat('cristal_lampara', 0xf4f0ff, 0.1), x, y, 9.8, 0.35, 2, esc=(1, 1, 1.4))

def casino_entrada():
    """La fachada del casino Trump de lado a lado del Strip: cristal negro con
    marcos dorados, «TRUMP» en letras de oro gigantes, la entrada con la
    marquesina de bombillas y una alfombra roja hasta la calle."""
    D = 8.0
    y0 = -D / 2
    W = 11.75
    for s in (-1, 1):
        caja(cristal_n(), s * (4.6 + (W - 4.6) / 2), y0 + 0.6, 0, W - 4.6, 1.2, 18)
        for x in (5.4, 8.0, 10.6):
            caja(oro_v(), s * x, y0 - 0.02, 0, 0.25, 0.3, 18)
    caja(cristal_n(), 0, y0 + 0.6, TECHO_V, 9.2, 1.2, 7)
    for z in (11.0, 13.5, 17.8):
        caja(oro_v(), 0, y0 - 0.03, z, W * 2, 0.32, 0.25)
    # TRUMP en letras de oro.
    texto(oro_v(), 'TRUMP', 0, y0 - 0.1, 15.6, tam=3.0, prof=0.25)
    # La marquesina de la entrada, con bombillas.
    caja(oro_v(), 0, y0 - 1.2, 10.4, 10.4, 2.6, 0.5)
    for k in range(26):
        x = -5.0 + k * 0.4
        esfera(bombilla(), x, y0 - 2.55, 10.55, 0.08, 1)
    for s in (-1, 1):
        caja(oro_v(), s * 4.8, y0 - 0.1, 0, 0.4, 0.4, 10.4)
        for k in range(18):
            esfera(bombilla(), s * 4.55, y0 - 0.35, 0.6 + k * 0.55, 0.07, 1)
    # La alfombra roja hasta la acera (y por dentro, la moqueta).
    caja(mat('alfombra_casino', 0xb01028, 0.6), 0, y0 - 5, 0, 4.2, 10, 0.1)
    caja(moqueta(), 0, 0.6, 0, 9.2, D - 1.2, 0.09)
    for s in (-1, 1):
        caja(cristal_n(), s * 4.75, 0.6, 0, 0.3, D - 1.2, TECHO_V)
    caja(granate(), 0, 0.6, TECHO_V, 9.8, D - 1.2, 0.4)

def casino_salida():
    """La salida al Strip: el marco dorado por dentro, con la luz de fuera."""
    D = 8.0
    caja(moqueta(), 0, 0, 0, 9.2, D, 0.09)
    for s in (-1, 1):
        caja(cristal_n(), s * 4.75, 0, 0, 0.3, D, TECHO_V)
        caja(oro_v(), s * 4.3, D / 2 - 0.4, 0, 0.6, 0.6, TECHO_V)
        for k in range(16):
            esfera(bombilla(), s * 4.0, D / 2 - 0.75, 0.6 + k * 0.6, 0.07, 1)
        # Los muros de los lados hasta la fachada (por si se ve el hueco).
        caja(cristal_n(), s * 8.3, 0, 0, 7.0, 0.3, TECHO_V).location.y = -D / 2 + 0.15
    caja(granate(), 0, 0, TECHO_V, 9.8, D, 0.4)
    caja(oro_v(), 0, D / 2 - 0.4, TECHO_V - 1.0, 9.2, 0.6, 1.0)
    texto(oro_v(), 'THANK YOU', 0, D / 2 - 0.75, TECHO_V - 0.5, tam=0.6, prof=0.03)


# ================================================================ Washington
PARED_C = 8.3
TECHO_C = 11.0
def marmol_c():   return mat_bloques('marmol_capitolio', 0xf1ece0, 0xe2dccd, ancho=1.8, alto=1.8, grosor=0.012, variacion=1.02)
def suelo_c():    return mat_bloques('suelo_capitolio', 0xe9e1cf, 0xcfc4ad, ancho=1.5, alto=1.5, grosor=0.02, variacion=1.03)
def crema():      return mat('crema_capitolio', 0xf3ead6, 0.5)
def piedra_c():   return mat_bloques('piedra_capitolio', 0xf2efe8, 0xe0dcd2, ancho=1.6, alto=0.6, grosor=0.012, variacion=1.02)
def bronce_c():   return mat('bronce_capitolio', 0x6a4a2a, 0.35)
def alfombra_c(): return mat('alfombra_capitolio', 0xa8182c, 0.6)
def lampara_c():  return luz('lampara_capitolio', 0xfff0d0, 1.5)

def estatua(x, y, s=1.0, bronce=True, mira=0.0):
    """Una estatua en su pedestal (de bronce o de mármol)."""
    m = bronce_c() if bronce else mat('marmol_estatua', 0xf6f3ec, 0.4)
    caja(mat('pedestal', 0xd8d0c0, 0.5), x, y, 0, 1.1 * s, 1.1 * s, 1.3 * s)
    cil(m, x, y, 1.3 * s, 0.32 * s, 1.5 * s, 10, r2=0.26 * s)
    esfera(m, x, y, 3.0 * s, 0.22 * s, 2)
    caja(m, x, y, 2.45 * s, 0.9 * s, 0.3 * s, 0.25 * s, giro=mira)

def cuadro(x, y, z, w, h, color, lado):
    """Un cuadro enorme con marco dorado en una pared lateral (lado: hacia donde mira)."""
    caja(oro(), x, y, z - 0.15, 0.08, w + 0.3, h + 0.3)
    caja(mat('lienzo_%x' % color, color, 0.7), x + lado * 0.05, y, z, 0.04, w, h)

def arana(x, y, z, techo=TECHO_C):
    cil(oro(), x, y, z + 0.6, 0.03, techo - z - 0.6, 6)
    cil(oro(), x, y, z + 0.4, 0.7, 0.06, 16)
    for k in range(8):
        a = k * math.pi / 4
        esfera(lampara_c(), x + math.cos(a) * 0.62, y + math.sin(a) * 0.62, z + 0.52, 0.08, 1)
    esfera(mat('cristal_arana', 0xf4f0ff, 0.1), x, y, z + 0.2, 0.3, 2, esc=(1, 1, 1.3))

def capitolio_pasillo():
    """Un trozo de 30 m del Capitolio por dentro (el Salón de las Estatuas):
    suelo de mármol, la alfombra roja por el centro, paredes crema con
    pilastras, estatuas de bronce y de mármol, cuadros y lámparas."""
    L = 30.0
    W = PARED_C
    caja(suelo_c(), 0, 0, 0, W * 2, L, 0.09)
    caja(alfombra_c(), 0, 0, 0.09, 2.6, L, 0.01)
    for s in (-1, 1):
        caja(marmol_c(), s * (W + 0.1), 0, 0, 0.2, L, TECHO_C)
        for y in (-11.25, -3.75, 3.75, 11.25):
            caja(crema(), s * (W - 0.2), y, 0, 0.4, 0.8, TECHO_C)
            caja(oro(), s * (W - 0.35), y, TECHO_C - 0.9, 0.1, 0.9, 0.4)
        for y, c in ((-7.5, 0x4a6a8a), (7.5, 0x8a5a3a)):
            cuadro(s * (W - 0.1), y, 3.2, 5.0, 3.4, c, -s)
        for y in (-11.25, 0.0, 11.25):
            estatua(s * 6.6, y, 1.0, bronce=(y != 0.0))
        caja(oro(), s * (W - 0.05), 0, 7.6, 0.1, L, 0.2)
    caja(crema(), 0, 0, TECHO_C, W * 2 + 0.4, L, 0.4)
    for y in (-11.25, -3.75, 3.75, 11.25):
        caja(oro(), 0, y, TECHO_C - 0.3, W * 2, 0.4, 0.3)
    for y in (-7.5, 7.5):
        arana(0, y, 8.6)

def capitolio_rotonda():
    """La gran rotonda: una sala redonda (radio 13), más alta que los
    pasillos, con cuadros enormes, estatuas alrededor y una estrella dorada en
    el suelo."""
    L, R = 30.0, 13.0
    W = PARED_C
    caja(suelo_c(), 0, 0, 0, 2 * R + 1, L, 0.09)
    caja(alfombra_c(), 0, 0, 0.09, 2.6, L, 0.01)
    # El medallón del centro: aros de mármol dorado y crema (la estrella plana salía oscura).
    cil(mat('medallon_oro', 0xd8b868, 0.4), 0, 0, 0.09, 5.2, 0.012, 32)
    cil(mat('medallon_crema', 0xf2e8d2, 0.5), 0, 0, 0.1, 4.4, 0.012, 32)
    cil(mat('medallon_oro', 0xd8b868, 0.4), 0, 0, 0.11, 1.6, 0.012, 24)
    # El muro redondo (sin los huecos de los pasillos) y los pasillos hasta él.
    n = 48
    for i in range(n):
        a = (i + 0.5) * 2 * math.pi / n
        x, y = math.sin(a) * R, math.cos(a) * R
        if abs(x) < W + 0.5 and abs(y) > 8:
            continue
        caja(marmol_c(), x, y, 0, 2 * math.pi * R / n + 0.05, 0.4, 14.0, giro=-a)
    y0 = math.sqrt(R * R - W * W)
    for s in (-1, 1):
        for sy in (-1, 1):
            caja(marmol_c(), s * (W + 0.1), sy * (y0 + (L / 2 - y0) / 2), 0, 0.2, L / 2 - y0 + 0.4, TECHO_C)
        caja(crema(), s * (W + (R - W) / 2), 0, TECHO_C, R - W + 1, L, 0.3)
    # Cuadros enormes y estatuas alrededor.
    for k, c in enumerate((0x6a5a3a, 0x4a5a7a, 0x7a4a3a, 0x5a6a4a)):
        a = math.pi / 2 + (k - 1.5) * 0.42
        for s in (-1, 1):
            x, y = s * math.sin(a) * (R - 0.3), math.cos(a) * (R - 0.3)
            caja(oro(), x, y, 2.5, 3.6, 0.08, 2.6, giro=-s * a)
            caja(mat('lienzo_r%d' % k, c, 0.7), x * 0.99, y * 0.99, 2.65, 3.3, 0.04, 2.3, giro=-s * a)
    for k in range(6):
        a = math.pi / 2 + (k - 2.5) * 0.36
        for s in (-1, 1):
            estatua(s * math.sin(a) * (R - 2.2), math.cos(a) * (R - 2.2), 1.05, bronce=(k % 2 == 0))
    # El techo de la rotonda y las lámparas. (La cúpula no: con la cámara del
    # juego queda siempre por encima de lo que se ve, y pesa mucho para el móvil.)
    caja(crema(), 0, 0, 14.0, 2 * R + 1, L, 0.4)
    for k in range(8):
        a = k * math.pi / 4
        esfera(lampara_c(), math.sin(a) * (R - 0.8), math.cos(a) * (R - 0.8), 12.5, 0.15, 1)
    for x in (-2.2, 2.2):
        arana(x, 0, 9.2, techo=14.0)

def capitolio_fachada():
    """La fachada este del Capitolio de lado a lado de la calle: mármol
    blanco, columnas a los lados de la puerta, el frontón encima y las
    grandes puertas de bronce abiertas. Por dentro, 10 m de vestíbulo."""
    D = 10.0
    y0 = -D / 2
    W = 11.75
    piedra = piedra_c()
    for s in (-1, 1):
        caja(piedra, s * (4.6 + (W - 4.6) / 2), y0 + 0.8, 0, W - 4.6, 1.6, 18)
    caja(piedra, 0, y0 + 0.8, TECHO_C, 9.2, 1.6, 7)
    # Las columnas delante (fuera de los carriles), el entablamento y el frontón.
    for x in (5.3, 7.1, 8.9, 10.7):
        for s in (-1, 1):
            cil(blanco(), s * x, y0 - 1.6, 0.6, 0.42, 11.6, 16)
            caja(blanco(), s * x, y0 - 1.6, 0, 1.1, 1.1, 0.6)
            caja(blanco(), s * x, y0 - 1.6, 12.2, 1.0, 1.0, 0.5)
    caja(blanco(), 0, y0 - 1.0, 12.7, W * 2, 2.6, 1.4)
    fronton(blanco(), 0, y0 - 2.2, 14.1, W * 2 - 1, 4.2, 2.4)
    # Las puertas de bronce, abiertas hacia dentro.
    for s in (-1, 1):
        caja(bronce_c(), s * 4.3, y0 + 2.6, 0, 0.15, 4.4, 9.5, giro=s * 0.15)
    caja(oro(), 0, y0 - 0.05, TECHO_C - 0.6, 9.4, 0.2, 0.6)
    texto(oro(), 'UNITED STATES CAPITOL', 0, y0 - 2.3, 13.4, tam=0.75, prof=0.04)
    # Por dentro: el vestíbulo.
    caja(suelo_c(), 0, 1.0, 0, 9.2, D - 2.0, 0.09)
    caja(alfombra_c(), 0, 1.0, 0.09, 2.6, D - 2.0, 0.01)
    for s in (-1, 1):
        caja(marmol_c(), s * 4.75, 1.0, 0, 0.3, D - 2.0, TECHO_C)
    caja(crema(), 0, 1.0, TECHO_C, 9.8, D - 2.0, 0.4)
    arana(0, 1.5, 8.6)

def capitolio_salida():
    """La salida oeste: el marco de mármol por dentro, con la luz de fuera."""
    D = 8.0
    caja(suelo_c(), 0, 0, 0, 9.2, D, 0.09)
    caja(alfombra_c(), 0, 0, 0.09, 2.6, D, 0.01)
    for s in (-1, 1):
        caja(marmol_c(), s * 4.75, 0, 0, 0.3, D, TECHO_C)
        caja(blanco(), s * 4.3, D / 2 - 0.4, 0, 0.6, 0.6, TECHO_C)
        caja(marmol_c(), s * 6.5, -D / 2 + 0.15, 0, 3.6, 0.3, TECHO_C)
    caja(crema(), 0, 0, TECHO_C, 9.8, D, 0.4)
    caja(blanco(), 0, D / 2 - 0.4, TECHO_C - 1.0, 9.2, 0.6, 1.0)

def cordon():
    """Cordón de terciopelo rojo entre dos postes de latón (como en los
    museos): se salta."""
    laton = mat('laton', 0xd8b050, 0.25)
    rojo_t = mat('terciopelo', 0xa01828, 0.6)
    for x in (-0.85, 0.85):
        caja(laton, x, 0.3, 0, 0.36, 0.36, 0.05)
        cil(laton, x, 0.3, 0.05, 0.05, 0.85, 10)
        esfera(laton, x, 0.3, 0.95, 0.08, 1)
    rama(rojo_t, (-0.85, 0.3, 0.85), (0, 0.3, 0.63), 0.05, 0.05, 6)
    rama(rojo_t, (0, 0.3, 0.63), (0.85, 0.3, 0.85), 0.05, 0.05, 6)


# ================================================================ Des Moines
def nieve_f():   return mat('nieve_feria', 0xf4f7fb, 0.8)
def bombilla_f(): return luz('bombilla_feria', 0xffe6a8, 1.3)

def toldo_rayas(nombre, c1, c2, x, y, z, w, d, lado):
    """Toldo de rayas inclinado hacia la calle (lado: hacia donde cae)."""
    o = caja(mat_franjas(nombre, c1, c2, 10, eje='Y', z0=y - d / 2, alto=d), x, y, z, w, d, 0.08)
    o.rotation_euler = (0, lado * 0.25, 0)
    caja(nieve_f(), x, y, z + 0.08, w * 0.95, d * 0.95, 0.06).rotation_euler = (0, lado * 0.25, 0)
    return o

def puesto(x, y, lado, letrero, color, c2):
    """Un puesto de comida de la feria en la acera, mirando a la calle (lado:
    -1 si está a la derecha y mira a -x)."""
    madera = mat('madera_puesto', 0xc98e52, 0.6)
    caja(mat('puesto_%x' % color, color, 0.5), x, y, 0, 2.6, 3.6, 2.3)
    caja(madera, x + lado * 1.35, y, 0.9, 0.3, 3.6, 0.15)            # el mostrador
    caja(mat('hueco_puesto', 0x3a2a20, 0.8), x + lado * 1.31, y, 1.05, 0.02, 3.0, 1.0)
    toldo_rayas('toldo_%x' % color, color, 0xfbf9f3, x + lado * 1.2, y, 2.2, 1.6, 3.8, lado)
    caja(mat('letrero_puesto', 0xfbf3d8, 0.5), x, y, 2.5, 2.4, 0.15, 0.7).rotation_euler = (0, 0, math.pi / 2)
    o = texto(mat('letra_%x' % c2, c2, 0.4), letrero, 0, 0, 0, tam=0.36, prof=0.02)
    o.rotation_euler = (math.pi / 2, 0, lado * math.pi / 2)
    o.location = (x + lado * 0.09, y, 2.85)

def guirnalda_luces(y, z=9.8):
    """Una guirnalda de bombillas de lado a lado de la calle, alta."""
    caja(mat('cable', 0x2a2c31, 0.5), 0, y, z, 21.0, 0.04, 0.04)
    for k in range(21):
        esfera(bombilla_f(), -10 + k, y, z - 0.18 - 0.25 * math.sin(k / 20 * math.pi), 0.09, 1)

def feria_puestos(variante=0):
    """30 m de la Feria del Estado de Iowa: puestos de comida con toldos de
    rayas en las dos aceras (corn dogs, chuletas en palo, limonada, buñuelos),
    pacas de paja, barriles y guirnaldas de bombillas por encima de la calle.
    Nieve en los toldos: en el juego, Des Moines es en invierno."""
    nombres = [('CORN DOGS', 0xd8283a, 0x23408f), ('PORK CHOP', 0x2a7a3a, 0xd8283a),
               ('LEMONADE', 0xf2c230, 0x23408f), ('FUNNEL CAKE', 0x23408f, 0xd8283a)]
    for k, y in enumerate((-9.0, 4.0)):
        for s in (-1, 1):
            letrero, c, c2 = nombres[(k + variante * 2 + (s > 0)) % 4]
            puesto(s * 7.3, y, -s, letrero, c, c2)
    paja = mat('paja', 0xd9b45a, 0.9)
    for s in (-1, 1):
        for y in (-2.6, 10.5):
            caja(paja, s * 5.2, y, 0, 1.1, 0.6, 0.5)
            caja(paja, s * 5.2, y + 0.65, 0, 1.1, 0.6, 0.5)
            caja(paja, s * 5.2, y + 0.3, 0.5, 1.1, 0.6, 0.5)
        cil(mat('barril_feria', 0x8a5a34, 0.6), s * 5.0, -13.0, 0, 0.4, 1.0, 12)
    for y in (-12.0, 0.0, 12.0):
        guirnalda_luces(y)
    # Detrás de los puestos de la izquierda, una carpa de rayas (la noria va a la derecha).
    carpa(-17.5, 0.0 if variante == 0 else 6.0, 5.5 if variante == 0 else 4.5)
    for s in (-1, 1):
        for y in (-12.0, 0.0, 12.0):
            cil(mat('poste_feria', 0x5a4a3a, 0.6), s * 10.4, y, 0, 0.1, 10.0, 8)

def feria_puestos_b(): feria_puestos(1)

def carpa(x, y, r):
    """Una carpa redonda de rayas rojas y blancas con su bandera."""
    cil(mat_franjas('carpa_rayas', 0xd8283a, 0xfbf9f3, 16, eje='X', z0=x - r, alto=2 * r), x, y, 0, r, 4.0, 24)
    cil(mat('techo_carpa', 0xc8283a, 0.5), x, y, 4.0, r + 0.3, 3.6, 24, r2=0.2)
    cil(nieve_f(), x, y, 4.0, r + 0.32, 0.6, 24, r2=r * 0.8)
    cil(blanco(), x, y, 7.6, 0.05, 1.6, 6)
    caja(mat_franjas('bandera_feria', 0xd8283a, 0xfbf9f3, 7, eje='Z', z0=8.4, alto=0.8), x + 0.5, y, 8.4, 1.0, 0.03, 0.8)

def feria_entrada():
    """El arco de la entrada: dos torres con banderas y, de lado a lado por
    encima de la calle, «IOWA STATE FAIR» con bombillas. Taquillas en las aceras."""
    rojo_f = mat('rojo_feria', 0xc8283a, 0.5)
    for s in (-1, 1):
        caja(mat('torre_feria', 0xf4ead2, 0.6), s * 9.6, 0, 0, 2.2, 2.2, 12.5)
        caja(rojo_f, s * 9.6, 0, 12.5, 2.6, 2.6, 0.5)
        cil(blanco(), s * 9.6, 0, 13.0, 0.06, 3.0, 8)
        caja(mat_franjas('bandera_feria', 0xd8283a, 0xfbf9f3, 7, eje='Z', z0=15.0, alto=1.0), s * 9.6 + s * 0.75, 0, 15.0, 1.5, 0.04, 1.0)
        # La taquilla.
        caja(mat('taquilla', 0x23408f, 0.5), s * 6.6, -1.0, 0, 2.0, 1.8, 2.6)
        caja(mat('ventana_taquilla', 0xfbf3d8, 0.4), s * 6.6 - s * 1.01, -1.0, 1.1, 0.02, 1.0, 0.8)
        caja(nieve_f(), s * 6.6, -1.0, 2.6, 2.2, 2.0, 0.15)
    caja(azul(), 0, 0, 10.8, 18.0, 1.2, 1.8)
    caja(oro(), 0, -0.62, 10.75, 18.2, 0.06, 0.1)
    caja(oro(), 0, -0.62, 12.55, 18.2, 0.06, 0.1)
    texto(mat('letra_feria', 0xf2c230, 0.4), 'IOWA STATE FAIR', 0, -0.62, 11.7, tam=1.1, prof=0.06)
    for k in range(30):
        x = -8.7 + k * 0.6
        esfera(bombilla_f(), x, -0.66, 10.95, 0.08, 1)
        esfera(bombilla_f(), x, -0.66, 12.45, 0.08, 1)
    caja(nieve_f(), 0, 0, 12.6, 18.0, 1.2, 0.18)

def feria_noria():
    """La noria de la feria, grande, detrás de los edificios de la derecha
    (asoma por encima de los tejados). El origen en el centro de la calle."""
    X, ZC, R = 19.0, 17.5, 14.0          # (en la feria no hay edificios: se ve entera)
    hierro = mat('hierro_noria', 0xe8e2d6, 0.5)
    for s in (-1, 1):
        rama(hierro, (X - 7, s * 2.4, 0), (X, s * 1.2, ZC), 0.3, 0.22, 8)
        rama(hierro, (X + 7, s * 2.4, 0), (X, s * 1.2, ZC), 0.3, 0.22, 8)
    cil(hierro, X, 0, ZC, 0.8, 2.6, 16, eje='Y')
    n = 16
    for k in range(n):
        a = k * 2 * math.pi / n
        x, z = X + math.cos(a) * R, ZC + math.sin(a) * R
        for s in (-1, 1):
            rama(hierro, (X, s * 1.1, ZC), (x, s * 1.1, z), 0.08, 0.08, 6)
        a2 = (k + 1) * 2 * math.pi / n
        for s in (-1, 1):
            rama(hierro, (x, s * 1.1, z), (X + math.cos(a2) * R, s * 1.1, ZC + math.sin(a2) * R), 0.12, 0.12, 6)
        cabina = mat('cabina_%d' % (k % 4), (0xd8283a, 0x23408f, 0xf2c230, 0x2a7a3a)[k % 4], 0.5)
        caja(cabina, x, 0, z - 1.6, 1.4, 1.8, 1.2)
        esfera(bombilla_f(), x, -1.2, z, 0.25, 1)

def vaca_mantequilla():
    """La vaca de mantequilla de la feria de Iowa (de verdad: tamaño natural,
    esculpida en mantequilla) en su vitrina refrigerada sobre un remolque.
    Mira al jugador (la cabeza hacia -y)."""
    mantequilla = mat('mantequilla', 0xf6dc7a, 0.5)
    caja(mat('remolque', 0x5a5650, 0.6), 0, 1.3, 0, 1.9, 2.6, 0.45)
    for x in (-0.85, 0.85):
        for y in (0.5, 2.1):
            cil(negro(), x, y, 0.22, 0.22, 0.15, 12, eje='X')
    # La vaca: cuerpo, cabeza, patas, cuernos y la ubre.
    esfera(mantequilla, 0, 1.45, 1.35, 0.55, 2, esc=(0.75, 1.5, 0.8))
    esfera(mantequilla, 0, 0.55, 1.55, 0.27, 2, esc=(0.9, 1.25, 1.0))
    for x in (-0.22, 0.22):
        for y in (0.95, 2.0):
            cil(mantequilla, x, y, 0.45, 0.1, 0.65, 8)
        rama(mantequilla, (x * 0.6, 0.5, 1.75), (x * 1.3, 0.45, 1.95), 0.04, 0.02, 6)
    esfera(mat('ubre', 0xf8e49a, 0.5), 0, 1.6, 0.95, 0.18, 1)
    # La vitrina de cristal con el marco y el cartel.
    vidrio = mat('vidrio_vitrina', 0xbfe0f0, 0.08)
    for x in (-0.95, 0.95):
        caja(vidrio, x, 1.3, 0.45, 0.04, 2.5, 1.9)
    for y in (0.07, 2.53):
        caja(vidrio, 0, y, 0.45, 1.9, 0.04, 1.9)
    caja(mat('marco_vitrina', 0x8a8f96, 0.4), 0, 1.3, 2.35, 2.0, 2.6, 0.12)
    caja(mat('cartel_vaca', 0x23408f, 0.5), 0, 0.02, 2.0, 1.6, 0.04, 0.42)
    texto(mat('letra_vaca', 0xf2c230, 0.4), 'BUTTER COW', 0, -0.01, 2.21, tam=0.2, prof=0.01)


PIEZAS = {
    'banderas_arco':   (banderas_arco,   'findlay',    dict(lado=1024, bisel=0.0)),
    'carroza_desfile': (carroza_desfile, 'obstaculos', dict(lado=1024)),
    'casino_entrada':  (casino_entrada,  'vegas',      dict(lado=1024, bisel=0.0)),
    'casino_sala':     (casino_sala,     'vegas',      dict(lado=2048, bisel=0.0, segmentos=2)),
    'casino_salida':   (casino_salida,   'vegas',      dict(lado=512, bisel=0.0)),
    'capitolio_fachada': (capitolio_fachada, 'washington', dict(lado=1024, bisel=0.0, segmentos=2)),
    'capitolio_pasillo': (capitolio_pasillo, 'washington', dict(lado=1024, bisel=0.0, segmentos=2)),
    'capitolio_rotonda': (capitolio_rotonda, 'washington', dict(lado=2048, bisel=0.0, segmentos=2)),
    'capitolio_salida': (capitolio_salida, 'washington', dict(lado=1024, bisel=0.0, segmentos=2)),
    'cordon': (cordon, 'obstaculos', dict(lado=256, bisel=0.0)),
    'feria_entrada': (feria_entrada, 'des_moines', dict(lado=1024, bisel=0.0)),
    'feria_puestos': (feria_puestos, 'des_moines', dict(lado=1024, bisel=0.0, segmentos=2)),
    'feria_puestos_b': (feria_puestos_b, 'des_moines', dict(lado=1024, bisel=0.0, segmentos=2)),
    'feria_noria': (feria_noria, 'des_moines', dict(lado=1024, bisel=0.0, suelo=False)),
    'vaca_mantequilla': (vaca_mantequilla, 'obstaculos', dict(lado=512, bisel=0.0)),
}

correr(PIEZAS)
