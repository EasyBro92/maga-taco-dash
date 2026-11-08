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


PIEZAS = {
    'banderas_arco':   (banderas_arco,   'findlay',    dict(lado=1024, bisel=0.0)),
    'carroza_desfile': (carroza_desfile, 'obstaculos', dict(lado=1024)),
    'casino_entrada':  (casino_entrada,  'vegas',      dict(lado=1024, bisel=0.0)),
    'casino_sala':     (casino_sala,     'vegas',      dict(lado=2048, bisel=0.0, segmentos=2)),
    'casino_salida':   (casino_salida,   'vegas',      dict(lado=512, bisel=0.0)),
}

correr(PIEZAS)
