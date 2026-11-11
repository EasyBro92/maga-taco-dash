# Los líderes de la caja sorpresa (10/11/2026; rehechos el 11/11).
#
#   blender -b -P blender/lideres.py -- [id ...] [--rapido]
#
# 10/11: «los premios se sienten muy sosos»: ocho líderes polémicos.
# 11/11: «me gustan, pero se mueven raro, les falta bastante detalle y algo
# característico de ellos». Ahora:
#   - Van montados en el MISMO esqueleto que el presidente de Meshy
#     (presidente.glb) y el juego les pone sus animaciones de correr y andar:
#     se mueven igual que él. Cada pieza va pegada a sus huesos con pesos
#     suaves (por cercanía a cada hueso), así las rodillas, los codos y el
#     tronco se doblan sin romperse.
#   - Más detalle: ojos con iris, brillo y párpados, cejas con gesto, boca,
#     arrugas, mofletes, orejas; manos con dedos; traje con solapas,
#     pañuelo, bolsillos y botones; zapatos con suela y cordones.
#   - Lo suyo de cada uno, que se vea también desde detrás (la cámara va a su
#     espalda): el gorro ruso de Putin, el misil de Kim, el cartel de la bomba
#     de Netanyahu, el tarro de miel de Xi, la motosierra de Milei, el
#     pajarito y el chándal de Maduro, la camiseta del 17 de Bolsonaro y el
#     vaso de té de Erdoğan.
#
# Sale www/models/lideres/<id>.glb (malla con esqueleto, sin animaciones: el
# juego usa las del presidente) y su retrato <id>.png.
#
# Ejes de Blender: z arriba, el personaje mira a -y. Medidas en metros, las
# del esqueleto de Meshy (1,9 de alto).

import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import *
from comun import _partes, _poner
from personaje import lamina, elip, esfera_uv, torno
from mathutils import Vector, Matrix

PRESIDENTE = os.path.join(MODELOS, 'personaje', 'presidente.glb')

# ropa: traje | mao | cuero | chandal | camiseta
# boca: serio | mueca | sonrisa | abierta     cejas: rectas | arriba | enfado | gruesas
LIDERES = {
    'putin': dict(piel=0xf3c9ad, pelo=(0xc9b394, 0xb59d7e), ceja=0xa8916f, ojos=0x6f8fae,
                  ropa='traje', traje=0x2f333b, pantalon=0x2a2d33, corbata=0x55627a, pin=(0x2a4fb0, 0xd8322f),
                  ancho=0.96, mandibula=0.12, nariz=0.9, linea=0.27, gordo=0.95,
                  boca='mueca', parpado=0.38, cejas='rectas', arrugas=1, mofletes=0.0, extra='ushanka'),
    'kim': dict(piel=0xf6d2ac, pelo=(0x1a1a1c, 0x2a2a2e), ceja=0x1a1a1c, ojos=0x3a2a1e,
                ropa='mao', traje=0x2b2d33, pantalon=0x2b2d33, corbata=None, pin=(0xd8322f, 0xffd23c),
                ancho=1.16, mandibula=0.22, nariz=0.85, linea=0.2, gordo=1.15, rapado=0x47423e,
                boca='sonrisa', parpado=0.32, cejas='gruesas', arrugas=0, mofletes=0.55, extra='misil'),
    'netanyahu': dict(piel=0xefc2a1, pelo=(0xdedcd6, 0xc8c5be), ceja=0xb9b5ad, ojos=0x4a3a2e,
                      ropa='traje', traje=0x1f2a44, pantalon=0x1f2a44, corbata=0x5a8fd8, pin=(0x2a5fd0, 0xffffff),
                      ancho=1.0, mandibula=0.2, nariz=1.15, linea=0.22, gordo=1.04,
                      boca='mueca', parpado=0.22, cejas='arriba', arrugas=2, mofletes=0.1, extra='cartel'),
    'xi': dict(piel=0xf4d0a6, pelo=(0x1c1c1e, 0x2c2c30), ceja=0x1c1c1e, ojos=0x2e2018,
               ropa='traje', traje=0x24272e, pantalon=0x24272e, corbata=0xc0272d, pin=(0xd8322f, 0xffd23c),
               ancho=1.08, mandibula=0.24, nariz=0.95, linea=0.23, gordo=1.07,
               boca='sonrisa', parpado=0.3, cejas='rectas', arrugas=0, mofletes=0.3, extra='miel'),
    'milei': dict(piel=0xf1c4a0, pelo=(0x5c3b22, 0x4a2e19), ceja=0x4a2e19, ojos=0x4f7a8a,
                  ropa='cuero', traje=0x1b1b1e, pantalon=0x222226, corbata=None, pin=(0x74b7e8, 0xffffff),
                  ancho=1.0, mandibula=0.2, nariz=1.05, linea=0.12, gordo=1.0, patillas=True,
                  boca='abierta', parpado=0.0, cejas='enfado', arrugas=1, mofletes=0.0, extra='motosierra'),
    'maduro': dict(piel=0xd8a27c, pelo=(0x221c19, 0x3a3532), ceja=0x221c19, ojos=0x2a1a12,
                   ropa='chandal', traje=0x2140a0, pantalon=0x2140a0, corbata=None, pin=(0xffd23c, 0xd8322f),
                   ancho=1.08, mandibula=0.3, nariz=1.1, linea=0.17, gordo=1.13, bigote=0x1c1714,
                   boca='sonrisa', parpado=0.15, cejas='gruesas', arrugas=1, mofletes=0.15, extra='pajarito',
                   zapato=0xf2f2f2),
    'bolsonaro': dict(piel=0xf0c4a3, pelo=(0x6e6762, 0x595350), ceja=0x595350, ojos=0x4a3626,
                      ropa='camiseta', traje=0xffd23c, pantalon=0x2b3346, corbata=None, pin=None,
                      ancho=1.0, mandibula=0.2, nariz=1.05, linea=0.2, gordo=1.02,
                      boca='mueca', parpado=0.2, cejas='arriba', arrugas=2, mofletes=0.1, extra='banda'),
    # 11/11: el del pase de campaña (solo sale ahi)
    'boris': dict(piel=0xf6cdb4, pelo=(0xf4e4a2, 0xe2c977), ceja=0xe0cc8a, ojos=0x5a7fa8,
                  ropa='traje', traje=0x262a35, pantalon=0x262a35, corbata=0xc8102e, pin=(0x1f3f9a, 0xc8102e),
                  ancho=1.06, mandibula=0.18, nariz=1.0, linea=0.2, gordo=1.08,
                  boca='sonrisa', parpado=0.25, cejas='arriba', arrugas=1, mofletes=0.4, extra='brexit'),
    'erdogan': dict(piel=0xeab995, pelo=(0xd0cbc3, 0xbab4ab), ceja=0xbab4ab, ojos=0x4a3a24,
                    ropa='traje', traje=0x2a2d35, pantalon=0x2a2d35, corbata=0x7a1f2a, pin=(0xd8322f, 0xffffff),
                    ancho=1.02, mandibula=0.2, nariz=1.1, linea=0.26, gordo=1.03, bigote=0xc9c3ba,
                    boca='serio', parpado=0.32, cejas='gruesas', arrugas=2, mofletes=0.05, extra='te'),
}

ARRIBA = Vector((0, 0, 1))


def mezcla(a, b, k):
    ca = [(a >> s) & 255 for s in (16, 8, 0)]
    cb = [(b >> s) & 255 for s in (16, 8, 0)]
    c = [round(x + (y - x) * k) for x, y in zip(ca, cb)]
    return (c[0] << 16) | (c[1] << 8) | c[2]

def oscuro(c, k=0.75):
    return mezcla(c, 0x000000, 1 - k)


# ---------------------------------------------------------------- esqueleto
J = {}        # dónde empieza cada hueso (en reposo, en el mundo)
SEG = {}      # hueso -> (desde, hasta)
arm = char1 = None

def cargar_esqueleto():
    global arm, char1
    empezar()
    bpy.ops.import_scene.gltf(filepath=PRESIDENTE)
    for o in list(bpy.data.objects):
        if o.type == 'ARMATURE':
            arm = o
        elif o.type == 'MESH' and o.parent is not None:
            char1 = o
    for o in list(bpy.data.objects):
        if o.type == 'MESH' and o is not char1:
            bpy.data.objects.remove(o)
    char1.hide_render = True
    mw = arm.matrix_world
    J.clear(); SEG.clear()
    for b in arm.data.bones:
        J[b.name] = (mw @ b.head_local).copy()
    hijos = {'Hips': 'Spine02', 'Spine02': 'Spine01', 'Spine01': 'Spine', 'Spine': 'neck', 'neck': 'Head',
             'Head': 'head_end'}
    for s in ('Left', 'Right'):
        hijos.update({s + 'Shoulder': s + 'Arm', s + 'Arm': s + 'ForeArm', s + 'ForeArm': s + 'Hand',
                      s + 'UpLeg': s + 'Leg', s + 'Leg': s + 'Foot', s + 'Foot': s + 'ToeBase'})
        d = (J[s + 'Hand'] - J[s + 'ForeArm']).normalized()
        J[s + '_dedos'] = J[s + 'Hand'] + d * 0.13
        f = J[s + 'ToeBase'] - J[s + 'Foot']; f.z = 0; f.normalize()
        J[s + '_punta'] = J[s + 'ToeBase'] + f * 0.08
        hijos[s + 'Hand'] = s + '_dedos'
        hijos[s + 'ToeBase'] = s + '_punta'
    for h, c in hijos.items():
        SEG[h] = (J[h], J[c])

def mano_dir(s):
    return (J[s + 'Hand'] - J[s + 'ForeArm']).normalized()

def palma(s):
    return J[s + 'Hand'] + mano_dir(s) * 0.055


# ---------------------------------------------------------------- pesos
def marca(n0, huesos):
    """Las piezas hechas desde _partes[n0] se mueven con estos huesos."""
    for o in _partes[n0:]:
        if 'huesos' not in o:
            o['huesos'] = ','.join(huesos)

def _dist(p, a, b):
    ab = b - a
    t = max(0.0, min(1.0, (p - a).dot(ab) / max(ab.length_squared, 1e-9)))
    return (a + ab * t - p).length

def pesar():
    for o in _partes:
        hs = o.get('huesos', 'Spine').split(',')
        grupos = {h: (o.vertex_groups.get(h) or o.vertex_groups.new(name=h)) for h in hs}
        if len(hs) == 1:
            grupos[hs[0]].add(list(range(len(o.data.vertices))), 1.0, 'REPLACE')
            continue
        mw = o.matrix_world
        for v in o.data.vertices:
            p = mw @ v.co
            ws = sorted(((1.0 / (_dist(p, *SEG[h]) ** 2 + 1e-5) ** 4, h) for h in hs), reverse=True)[:3]
            tot = sum(w for w, _ in ws)
            for w, h in ws:
                if w / tot > 0.02:
                    grupos[h].add([v.index], w / tot, 'REPLACE')


# ---------------------------------------------------------------- formas
def bola(m, c, r, esc=(1, 1, 1), eje=None, sub=2):
    o = esfera(m, c[0], c[1], c[2], r, sub, esc=esc)
    if eje is not None:
        o.rotation_mode = 'QUATERNION'
        o.rotation_quaternion = Vector(eje).normalized().to_track_quat('Y', 'Z')
    return o

def tubo(m, a, b, r1, r2=None, lados=14):
    a, b = Vector(a), Vector(b)
    d = b - a
    bpy.ops.mesh.primitive_cone_add(vertices=lados, radius1=r1, radius2=r1 if r2 is None else r2,
                                    depth=max(d.length, 1e-4), location=(a + b) / 2)
    o = bpy.context.object
    o.rotation_mode = 'QUATERNION'
    o.rotation_quaternion = d.normalized().to_track_quat('Z', 'Y')
    return _poner(o, m)

def estrella(m, c, r, atras=False, grosor=0.006):
    bm = bmesh.new()
    cen = bm.verts.new((0, 0, 0))
    fuera = [bm.verts.new((math.sin(i / 10 * math.tau) * (r if i % 2 == 0 else r * 0.45), 0,
                           math.cos(i / 10 * math.tau) * (r if i % 2 == 0 else r * 0.45))) for i in range(10)]
    for i in range(10):
        bm.faces.new((cen, fuera[i], fuera[(i + 1) % 10]))
    me = bpy.data.meshes.new('estrella'); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new('estrella', me)
    bpy.context.scene.collection.objects.link(o)
    md = o.modifiers.new('g', 'SOLIDIFY'); md.thickness = grosor
    bpy.context.view_layer.objects.active = o
    bpy.ops.object.modifier_apply(modifier='g')
    o.location = c
    if atras:
        o.rotation_euler = (0, 0, math.pi)
    return _poner(o, m)


# ---------------------------------------------------------------- tronco
PERFIL = [(0.78, 0.228), (0.84, 0.232), (0.92, 0.245), (1.0, 0.252), (1.08, 0.252), (1.16, 0.246),
          (1.24, 0.232), (1.30, 0.212), (1.35, 0.178), (1.385, 0.13), (1.405, 0.075)]
PROF = 0.8
CY = -0.03

def radio(L, z):
    for (z0, r0), (z1, r1) in zip(PERFIL, PERFIL[1:]):
        if z0 <= z <= z1:
            return (r0 + (r1 - r0) * (z - z0) / (z1 - z0)) * L['gordo']
    return (PERFIL[0][1] if z < PERFIL[0][0] else PERFIL[-1][1]) * L['gordo']

def frente(L, x, z, sale=0.0):
    r = radio(L, z)
    return CY - PROF * math.sqrt(max(r * r - x * x, 0.0)) - sale

def espalda(L, x, z, sale=0.0):
    r = radio(L, z)
    return CY + PROF * math.sqrt(max(r * r - x * x, 0.0)) + sale

def cinta(L, m, x0, x1, z0, z1, sale=0.004, n=10, grosor=0.008, atras=False):
    """Una tira pegada al pecho (o a la espalda) entre x0..x1 y z0..z1."""
    f = espalda if atras else frente
    filas = []
    for k in range(3):
        z = z0 + (z1 - z0) * k / 2
        filas.append([(x, f(L, x, z, sale), z) for x in [x0 + (x1 - x0) * i / n for i in range(n + 1)]])
    return lamina(m, filas, grosor)

def letras(L, m, cadena, z, tam, prof=0.012, sale=-0.002):
    """Letras en la espalda, pegadas a su curva (la cámara va detrás)."""
    o = texto(m, cadena, 0, 0, z, tam, prof)
    o.rotation_euler = (math.pi / 2, 0, math.pi)
    bpy.context.view_layer.update()
    o.data.transform(o.matrix_world)
    o.matrix_world = Matrix.Identity(4)
    y0 = min(v.co.y for v in o.data.vertices)
    for v in o.data.vertices:
        v.co.y = espalda(L, v.co.x, v.co.z, sale) + (v.co.y - y0)
    return o

def tronco(L):
    i, ropa = L['id'], L['ropa']
    tela = mat('ropa_' + i, L['traje'], 0.3 if ropa == 'cuero' else 0.6)
    sombra = mat('ropa2_' + i, oscuro(L['traje'], 0.78), 0.6)
    blanco = mat('camisa', 0xf7f7f4, 0.5)
    n0 = len(_partes)
    o = torno(tela, PERFIL, 36, PROF)
    o.scale = (L['gordo'], L['gordo'], 1); o.location.y = CY
    for s in (-1, 1):                                                   # hombreras
        bola(tela, (s * 0.19, CY + 0.02, 1.33), 0.085, esc=(1.15 * L['gordo'], 0.9, 0.7))
    if ropa == 'traje':
        filas = []
        for k in range(9):
            z = 1.395 - k * (0.31 / 8)
            w = 0.085 * (z - 1.08) / 0.315
            filas.append([(x, frente(L, x, z, 0.003), z) for x in (-w, -w / 2, 0, w / 2, w)])
        lamina(blanco, filas, 0.01)                                     # camisa en V
        for s in (-1, 1):                                               # solapas
            filas = []
            for k in range(9):
                z = 1.4 - k * (0.33 / 8)
                w = max(0.0, 0.085 * (z - 1.07) / 0.33)
                a = 0.03 + 0.03 * (z - 1.07) / 0.33
                filas.append([(x, frente(L, x, z, 0.007), z) for x in (s * w, s * (w + a / 2), s * (w + a))])
            lamina(sombra, filas, 0.012)
        for s in (-1, 1):                                               # picos del cuello de la camisa
            bola(blanco, (s * 0.035, frente(L, s * 0.035, 1.385, 0.012), 1.385), 0.03, esc=(1.1, 0.4, 0.8), sub=2)
        cor = mat('corbata_' + i, L['corbata'], 0.45)
        bola(cor, (0, frente(L, 0, 1.37, 0.018), 1.37), 0.024, esc=(1.0, 0.7, 0.9), sub=2)   # nudo
        filas = []
        for k in range(11):
            z = 1.355 - k * (0.32 / 10)
            w = 0.018 + 0.016 * k / 10
            filas.append([(x, frente(L, x, z, 0.016), z) for x in (-w, 0, w)])
        filas.append([(x, frente(L, 0, 1.0, 0.016), 1.0) for x in (-0.002, 0, 0.002)])
        lamina(cor, filas, 0.01)
        bolsillo = mat('pañuelo', 0xffffff, 0.5)                        # pañuelo en el bolsillo
        cinta(L, sombra, 0.085, 0.17, 1.235, 1.245, 0.006, 6, 0.008)
        filas = [[(x, frente(L, x, 1.245, 0.008), 1.245) for x in (0.1, 0.12, 0.14, 0.16)],
                 [(x, frente(L, x, z, 0.008), z) for x, z in ((0.1, 1.27), (0.12, 1.258), (0.14, 1.272), (0.16, 1.26))]]
        lamina(bolsillo, filas, 0.006)
        for s in (-1, 1):                                               # bolsillos de abajo
            cinta(L, sombra, s * 0.08, s * 0.2, 0.9, 0.93, 0.006, 6, 0.008)
        for z in (0.98, 0.9):                                           # botones
            bola(mat('boton', 0x15161c, 0.3), (0, frente(L, 0, z, 0.004), z), 0.014, esc=(1, 0.5, 1), sub=1)
    elif ropa == 'mao':
        tubo(tela, (0, CY - 0.01, 1.36), (0, CY - 0.012, 1.425), 0.098, 0.092, 20)        # cuello cerrado
        cinta(L, sombra, -0.006, 0.006, 0.79, 1.39, 0.004, 2, 0.006)
        for z in (1.34, 1.25, 1.16, 1.07, 0.98, 0.89):
            bola(mat('boton_mao', 0x7a7d84, 0.3), (0, frente(L, 0, z, 0.006), z), 0.013, esc=(1, 0.5, 1), sub=1)
        for s in (-1, 1):
            cinta(L, sombra, s * 0.06, s * 0.17, 1.22, 1.26, 0.006, 6, 0.008)            # bolsillos del pecho
            cinta(L, sombra, s * 0.08, s * 0.21, 0.88, 0.93, 0.006, 6, 0.008)
        bola(mat('chapa_kim', 0xd8322f, 0.4), (0.125, frente(L, 0.125, 1.29, 0.008), 1.29), 0.02, esc=(1, 0.4, 1), sub=2)
    elif ropa == 'cuero':
        cam = mat('camiseta_negra', 0x2b2b30, 0.8)
        filas = []
        for k in range(9):
            z = 1.395 - k * (0.36 / 8)
            w = 0.1 * (z - 1.03) / 0.365
            filas.append([(x, frente(L, x, z, 0.003), z) for x in (-w, -w / 2, 0, w / 2, w)])
        lamina(cam, filas, 0.01)
        cuello = mat('cuero_cuello', 0x2c2c31, 0.3)
        for s in (-1, 1):
            filas = []
            for k in range(9):
                z = 1.41 - k * (0.38 / 8)
                w = max(0.0, 0.1 * (z - 1.03) / 0.38)
                filas.append([(x, frente(L, x, z, 0.008), z) for x in (s * w, s * (w + 0.035), s * (w + 0.07))])
            lamina(cuello, filas, 0.014)
            cinta(L, mat('cremallera', 0xcfd2d8, 0.25), s * 0.105, s * 0.112, 0.8, 1.03, 0.008, 2, 0.008)
        for s in (-1, 1):
            cinta(L, cuello, s * 0.09, s * 0.19, 0.95, 0.965, 0.006, 6, 0.008)
    elif ropa == 'chandal':
        amarillo, rojo = mat('ch_amarillo', 0xffd23c, 0.6), mat('ch_rojo', 0xd8322f, 0.6)
        for z0, z1, mm in ((1.2, 1.415, amarillo), (0.775, 0.9, rojo)):
            filas = [(z0 + (z1 - z0) * k / 6, 0) for k in range(7)]
            t = torno(mm, [(z, radio(L, z) / L['gordo'] + 0.004) for z, _ in filas], 36, PROF)
            t.scale = (L['gordo'], L['gordo'], 1); t.location.y = CY
        cinta(L, mat('cremallera', 0xcfd2d8, 0.25), -0.006, 0.006, 0.78, 1.4, 0.008, 2, 0.008)
        tubo(amarillo, (0, CY - 0.01, 1.37), (0, CY - 0.012, 1.425), 0.096, 0.09, 20)
        for k in range(8):                                              # las estrellas de la bandera
            a = -0.7 + 1.4 * k / 7
            x, z = math.sin(a) * 0.13, 1.06 + math.cos(a) * 0.08
            estrella(mat('estrella_blanca', 0xffffff, 0.5), (x, frente(L, x, z, 0.006), z), 0.018)
        letras(L, mat('letras_blancas', 0xffffff, 0.5), 'VENEZUELA', 1.04, 0.075)
    elif ropa == 'camiseta':
        verde, azul = mat('verde_br', 0x1f9a47, 0.6), mat('azul_br', 0x1f3f9a, 0.6)
        filas = []
        for k in range(5):
            z = 1.405 - k * (0.12 / 4)
            w = 0.075 * (z - 1.28) / 0.125
            filas.append([(x, frente(L, x, z, 0.004), z) for x in (-w - 0.02, -w, w, w + 0.02)])
        lamina(verde, filas, 0.01)                                      # cuello en V verde
        bola(azul, (0.12, frente(L, 0.12, 1.25, 0.006), 1.25), 0.03, esc=(0.8, 0.35, 1), sub=2)   # escudo
        letras(L, verde, 'BOLSONARO', 1.29, 0.06)
        letras(L, verde, '17', 1.1, 0.2, 0.016)
        for off, c in ((-0.028, 0x1f9a47), (0.0, 0xffd23c), (0.028, 0x1f9a47)):   # la banda
            filas = []
            for k in range(13):
                f = k / 12
                x0 = -0.2 + 0.4 * f
                z = 1.33 - 0.42 * f + off
                filas.append([(x, frente(L, x, z, 0.016), z) for x in (x0 - 0.03, x0, x0 + 0.03)])
            lamina(mat('banda_%x' % c, c, 0.5), filas, 0.012)
    if L.get('pin'):
        a, b = L['pin']
        caja(mat('pin_%x' % a, a, 0.4), 0.15, frente(L, 0.15, 1.3, 0.016), 1.29, 0.028, 0.008, 0.02)
        caja(mat('pin_%x' % b, b, 0.4), 0.142, frente(L, 0.142, 1.3, 0.02), 1.294, 0.012, 0.008, 0.012)
    if L['extra'] == 'miel':        # Xi: la etiqueta de la ropa, en grande
        cinta(L, mat('etiqueta_xi', 0xf6f4ec, 0.6), -0.15, 0.15, 1.1, 1.3, 0.006, 12, 0.008, atras=True)
        letras(L, mat('letras_negras', 0x1a1a1a, 0.5), 'MADE IN', 1.24, 0.065, 0.008, 0.012)
        letras(L, mat('letras_rojas', 0xd8322f, 0.5), 'CHINA', 1.155, 0.085, 0.008, 0.012)
    if L['extra'] == 'brexit':      # Boris
        letras(L, mat('letras_blancas', 0xffffff, 0.5), 'BREXIT', 1.12, 0.1, 0.014)
    if L['extra'] == 'motosierra':  # Milei: su grito en la chaqueta
        letras(L, mat('letras_oro', 0xf2c230, 0.4), '¡AFUERA!', 1.12, 0.085, 0.014)
    if L['extra'] == 'te':          # Erdogan: capa de sultan con la media luna
        rojo = mat('capa', 0xc8102e, 0.55)
        yb = lambda x, z: espalda(L, x, z, 0.015 + 0.06 * (1.39 - z) / 0.47)
        filas = []
        for k in range(9):
            z = 1.39 - k * (0.47 / 8)
            w = 0.16 + 0.1 * (1.39 - z) / 0.47
            filas.append([(x, yb(x, z), z) for x in [-w + 2 * w * j / 10 for j in range(11)]])
        lamina(rojo, filas, 0.012)
        cil(mat('luna', 0xffffff, 0.5), -0.02, yb(-0.02, 1.12) + 0.006, 1.12, 0.07, 0.006, 28, eje='Y')
        cil(rojo, 0.0, yb(0.0, 1.12) + 0.011, 1.12, 0.058, 0.006, 28, eje='Y')
        estrella(mat('luna', 0xffffff, 0.5), (0.085, yb(0.085, 1.12) + 0.012, 1.12), 0.03, atras=True)
    if ropa != 'camiseta':                                              # la costura de la espalda
        cinta(L, sombra, -0.005, 0.005, 0.79, 1.36, 0.003, 2, 0.006, atras=True)
    marca(n0, ['Hips', 'Spine02', 'Spine01', 'Spine', 'neck', 'LeftShoulder', 'RightShoulder'])
    # el cuello
    n0 = len(_partes)
    tubo(mat('piel_' + i, L['piel'], 0.55), (0, CY - 0.012, 1.36), (0, CY - 0.03, 1.5), 0.068 * min(1.15, L['ancho']), lados=16)
    marca(n0, ['neck', 'Head', 'Spine'])


def brazos(L):
    i, ropa = L['id'], L['ropa']
    tela = mat('ropa_' + i, L['traje'], 0.3 if ropa == 'cuero' else 0.6)
    piel = mat('piel_' + i, L['piel'], 0.55)
    for s in ('Left', 'Right'):
        H, E, W = J[s + 'Arm'], J[s + 'ForeArm'], J[s + 'Hand']
        d = mano_dir(s)
        # Las bolas de las articulaciones van con el hueso que nace en ellas
        # (giran sobre su centro y tapan la junta) y los tubos, rigidos con su
        # hueso: asi nada se estira ni se rompe al doblar.
        n0 = len(_partes)
        bola(tela, H, 0.078, sub=3)
        if ropa == 'camiseta':                                          # manga corta
            m = H + (E - H) * 0.55
            tubo(tela, H, m, 0.08, 0.072)
            tubo(mat('verde_br', 0x1f9a47, 0.6), m, m + (E - H).normalized() * 0.014, 0.074, 0.074)
            tubo(piel, m, E, 0.062, 0.058)
        else:
            tubo(tela, H, E, 0.076, 0.064)
        marca(n0, [s + 'Arm'])
        n0 = len(_partes)
        bola(piel if ropa == 'camiseta' else tela, E, 0.062 if ropa != 'camiseta' else 0.056)
        if ropa == 'camiseta':
            tubo(piel, E, W, 0.054, 0.044)
        else:
            tubo(tela, E, W - d * 0.02, 0.062, 0.054)
            puno = {'traje': 0xf7f7f4, 'mao': L['traje'], 'cuero': 0x2c2c31, 'chandal': 0xffd23c}[ropa]
            tubo(mat('puno_%x' % puno, puno, 0.5), W - d * 0.03, W + d * 0.004, 0.05, 0.05)
            if ropa == 'traje':
                bola(mat('gemelo', 0xd9b23c, 0.25), W - d * 0.012 + Vector((0, 0, 0.05)), 0.008, sub=1)
        marca(n0, [s + 'ForeArm'])
        # la mano: palma, cuatro dedos y el pulgar (hacia dentro)
        n0 = len(_partes)
        P = palma(s)
        lado = d.cross(ARRIBA).normalized()
        dentro = Vector((-1 if J[s + 'Hand'].x > 0 else 1, 0, 0))
        bola(piel, P, 0.048, esc=(1.0, 1.15, 0.55), eje=d)
        for k in range(4):
            o = P + d * 0.04 + lado * (-0.03 + 0.02 * k) - ARRIBA * 0.004
            tubo(piel, o, o + d * (0.045 - 0.006 * abs(k - 1.5)) - ARRIBA * 0.018, 0.011, 0.009, 8)
        o = P + dentro * 0.035 - d * 0.005
        tubo(piel, o, o + d * 0.04 + dentro * 0.015 + ARRIBA * 0.01, 0.012, 0.01, 8)
        marca(n0, [s + 'Hand'])


def piernas(L):
    i = L['id']
    pan = mat('pantalon_' + i, L['pantalon'], 0.6)
    raya = mat('pantalon2_' + i, oscuro(L['pantalon'], 0.8), 0.6)
    zap_c = L.get('zapato', 0x16171b)
    zap = mat('zapato_%x' % zap_c, zap_c, 0.25)
    suela = mat('suela_' + ('roja' if zap_c != 0x16171b else 'negra'), 0xd8322f if zap_c != 0x16171b else 0x3a2a20, 0.8)
    n0 = len(_partes)
    bola(pan, (0, CY + 0.01, 0.84), 0.2, esc=(1.05 * L['gordo'], 0.8 * L['gordo'], 0.55), sub=3)
    marca(n0, ['Hips'])
    for s in ('Left', 'Right'):
        U, K, A, T = J[s + 'UpLeg'], J[s + 'Leg'], J[s + 'Foot'], J[s + 'ToeBase']
        n0 = len(_partes)
        bola(pan, U, 0.105, sub=3)
        tubo(pan, U, K, 0.102, 0.08)
        if L['ropa'] == 'chandal':                                     # las rayas del chándal
            tubo(mat('ch_amarillo', 0xffd23c, 0.6), U + Vector((0.09 if U.x > 0 else -0.09, 0, 0)),
                 K + Vector((0.075 if U.x > 0 else -0.075, 0, 0)), 0.012, 0.01, 6)
        marca(n0, [s + 'UpLeg'])
        n0 = len(_partes)
        bola(pan, K, 0.08)
        tubo(pan, K, A + Vector((0, 0, 0.04)), 0.078, 0.064)
        tubo(raya, K + Vector((0, -0.075, 0)), A + Vector((0, -0.06, 0.06)), 0.006, 0.006, 6)   # la raya
        marca(n0, [s + 'Leg'])
        n0 = len(_partes)
        tubo(mat('calcetin', 0x24242a, 0.7), A + Vector((0, 0, 0.06)), A - Vector((0, 0, 0.03)), 0.05, 0.05, 12)
        f = T - A; f.z = 0; f.normalize()
        talon = Vector((A.x, A.y, 0)) - f * 0.06
        punta = Vector((J[s + '_punta'].x, J[s + '_punta'].y, 0))
        largo = (punta - talon).length
        c = (talon + punta) / 2
        bola(zap, (c.x, c.y, 0.058), 1, esc=(0.068, largo / 2, 0.058), eje=f, sub=3)
        bola(zap, (c.x + f.x * largo * 0.22, c.y + f.y * largo * 0.22, 0.05), 1, esc=(0.07, largo * 0.3, 0.05), eje=f, sub=2)
        giro = math.atan2(-f.x, f.y)
        bola(suela, (c.x, c.y, 0.014), 1, esc=(0.071, largo / 2 + 0.006, 0.016), eje=f, sub=3)
        for k in range(3):                                              # cordones
            p = c + f * (0.02 + 0.03 * k)
            caja(mat('cordon', 0xeeeeee, 0.6), p.x, p.y, 0.1 - 0.012 * k, 0.05, 0.012, 0.008, giro=giro)
        marca(n0, [s + 'Foot', s + 'ToeBase'])


# ---------------------------------------------------------------- cabeza
# Se modela a tamaño "de diseño" (radio 0,36, como el muñeco) y luego se
# encoge y se sube a su sitio sobre el cuello.
ESC_CABEZA = 0.64
CENTRO_CABEZA = Vector((0, -0.05, 1.69))

def cara_y(L, x, z):
    """La y de la superficie de la cara en (x, z) (diseño)."""
    z0 = z / 0.98
    t = max(0.0, -z0 / 0.36)
    mof = max(0.0, 1 - abs(z0 + 0.05) / 0.25)
    x0 = x / (1.03 * L['ancho'] * (1 + L['mandibula'] * t) * (1 + 0.04 * mof * (L['ancho'] - 1) * 10))
    return -math.sqrt(max(0.36 ** 2 - x0 * x0 - z0 * z0, 0.0)) * 0.98 * (1 + 0.16 * t)

def piel(L):  return mat('piel_' + L['id'], L['piel'], 0.55)
def pelo(L):  return mat_franjas('pelo_' + L['id'], L['pelo'][0], L['pelo'][1], 22, eje='Y', z0=-0.45, alto=0.9)

def casco(L, m):
    """El pelo pegado a la cabeza; la frente despejada hasta `linea`."""
    a = L['ancho']
    o = esfera_uv(m, 0, 0.025, 0.005, 0.372, 40, 24, esc=(1.07 * a, 1.03, 1.0))
    bm = bmesh.new(); bm.from_mesh(o.data)
    fuera = []
    for v in bm.verts:
        x, y, z = v.co
        delante = -y / 0.372
        limite = L['linea'] * max(0.0, delante) ** 0.8 - 0.02 - 0.18 * max(0.0, -delante)
        if delante > -0.2:   # patillas
            ladoo = min(1.0, max(0.0, (abs(x) - 0.24) / 0.08))
            limite += (min(limite, -0.12 if L.get('patillas') else 0.02) - limite) * ladoo if limite > 0.02 else 0
        if z < limite - 0.06:
            fuera.append(v); continue
        k = min(1.0, max(0.0, (z - (limite - 0.06)) / 0.1))
        k = k * k * (3 - 2 * k)
        v.co *= 0.88 + 0.12 * k
    bmesh.ops.delete(bm, geom=fuera, context='VERTS')
    bm.to_mesh(o.data); bm.free()

def casquete(L, m, r=0.385, alto=1.0, lado=0.1, frente_=0.25):
    o = esfera_uv(m, 0, 0.02, 0.0, r, 40, 24, esc=(1.07 * L['ancho'], 1.04, alto))
    bm = bmesh.new(); bm.from_mesh(o.data)
    dentro = 0.366 / r
    fuera = []
    for v in bm.verts:
        x, y, z = v.co
        delante = -y / r
        t = (lado + (frente_ - lado) * max(0.0, delante) - 0.1 * max(0.0, -delante)) / alto
        if z < t - 0.07:
            fuera.append(v); continue
        k = min(1.0, max(0.0, (z - (t - 0.07)) / 0.11))
        k = k * k * (3 - 2 * k)
        v.co *= dentro + (1 - dentro) * k
    bmesh.ops.delete(bm, geom=fuera, context='VERTS')
    bm.to_mesh(o.data); bm.free()

def tira_cara(L, m, puntos, grueso, sale=0.006, grosor=0.008):
    """Una tira fina sobre la cara que sigue `puntos` [(x, z)] (labios, arrugas)."""
    filas = [[(x, cara_y(L, x, z + dz) - sale, z + dz) for x, z in puntos] for dz in (grueso / 2, -grueso / 2)]
    return lamina(m, filas, grosor)

def cabeza(L):
    i, a = L['id'], L['ancho']
    p = piel(L)
    o = esfera_uv(p, 0, 0, 0, 0.36, 40, 26)
    for v in o.data.vertices:
        x, y, z = v.co
        t = max(0.0, -z / 0.36)
        mof = max(0.0, 1 - abs(z + 0.05) / 0.25)
        v.co = (x * 1.03 * a * (1 + L['mandibula'] * t) * (1 + 0.04 * mof * (a - 1) * 10),
                y * 0.98 * (1 + 0.16 * t), z * 0.98)
    # orejas con su hueco
    for s in (-1, 1):
        elip(p, s * 0.385 * a, 0.0, -0.02, 0.07, esc=(0.5, 0.9, 1.15), sub=2)
        elip(mat('oreja_' + i, oscuro(L['piel'], 0.82), 0.6), s * 0.405 * a, -0.012, -0.02, 0.04, esc=(0.3, 0.7, 1.0), sub=2)
    # nariz
    n = L['nariz']
    elip(p, 0, -0.352, -0.045, 0.062 * n, esc=(0.95, 1.0, 1.15), sub=3)
    elip(p, 0, -0.33, 0.02, 0.038 * n, esc=(0.8, 1.0, 1.6), sub=2)
    for s in (-1, 1):
        elip(p, s * 0.04 * n, -0.34, -0.07, 0.026 * n, esc=(1, 0.8, 0.8), sub=2)   # aletas
    # ojos: blanco, iris, pupila, brillo y párpado
    blanco, negro, brillo = mat('ojo', 0xfbfbf8, 0.2), mat('pupila', 0x120c08, 0.2), mat('brillo', 0xffffff, 0.1)
    iris = mat('iris_' + i, L['ojos'], 0.3)
    for s in (-1, 1):
        x, z = s * 0.128, 0.03
        y = cara_y(L, x, z) + 0.03
        elip(blanco, x, y, z, 0.07, esc=(1.0, 0.6, 0.78), sub=3)
        elip(iris, x, y - 0.036, z, 0.035, esc=(1, 0.45, 1), sub=2)
        elip(negro, x, y - 0.045, z, 0.018, esc=(1, 0.4, 1), sub=2)
        elip(brillo, x + 0.012, y - 0.05, z + 0.013, 0.008, sub=1)
        lid = esfera(p, x, y + 0.002, z, 0.074, 3, esc=(1.04, 0.66, 0.84), mitad=True)
        lid.rotation_euler = (-0.95 + L['parpado'] * 1.7, 0, 0)
        # párpado de abajo (fino)
        abajo = esfera(p, x, y + 0.004, z, 0.073, 2, esc=(1.03, 0.64, 0.82), mitad=True)
        abajo.rotation_euler = (math.pi + 1.15, 0, 0)
    # cejas
    c = mat('ceja_' + i, L['ceja'], 0.85)
    gira = {'rectas': -0.06, 'arriba': 0.28, 'enfado': -0.38, 'gruesas': -0.12}[L['cejas']]
    alto = 0.36 if L['cejas'] == 'gruesas' else 0.26
    for s in (-1, 1):
        x, z = s * 0.13, 0.135 + (0.012 if L['cejas'] == 'arriba' else 0)
        elip(c, x, cara_y(L, x, z) - 0.008, z, 0.06, esc=(1.4, 0.4, alto), rot=(0, s * gira, 0), sub=2)
    # boca
    labio = mat('labio_' + i, mezcla(L['piel'], 0x9a3a36, 0.45), 0.5)
    dentro, dientes = mat('boca_dentro', 0x3e1414, 0.7), mat('dientes', 0xf4f1ea, 0.3)
    N, z0, b = 11, -0.175, L['boca']
    ts = [-1 + 2 * k / (N - 1) for k in range(N)]
    if b == 'serio':
        tira_cara(L, labio, [(t * 0.055, z0 - 0.01 * t * t) for t in ts], 0.014)
    elif b == 'mueca':
        tira_cara(L, labio, [(t * 0.055, z0 + 0.022 * max(0, t) ** 2 - 0.006 * max(0, -t) ** 2) for t in ts], 0.013)
    elif b == 'sonrisa':
        arr = [(t * 0.065, z0 + 0.03 * t * t) for t in ts]
        aba = [(t * 0.065, z0 + 0.03 * t * t - 0.05 * (1 - t * t)) for t in ts]
        filas = [[(x, cara_y(L, x, z) - 0.004, z) for x, z in arr], [(x, cara_y(L, x, z) - 0.004, z) for x, z in aba]]
        lamina(dentro, filas, 0.008)
        tira_cara(L, dientes, [(x, z - 0.009) for x, z in arr], 0.018, 0.008, 0.006)
        tira_cara(L, labio, aba, 0.01, 0.009)
        tira_cara(L, labio, arr, 0.008, 0.009)
    else:   # abierta: gritando
        arr = [(t * 0.05, z0 + 0.03 * math.sqrt(max(0, 1 - t * t))) for t in ts]
        aba = [(t * 0.05, z0 - 0.06 * math.sqrt(max(0, 1 - t * t))) for t in ts]
        filas = [[(x, cara_y(L, x, z) - 0.004, z) for x, z in arr], [(x, cara_y(L, x, z) - 0.004, z) for x, z in aba]]
        lamina(dentro, filas, 0.008)
        tira_cara(L, dientes, [(x, z - 0.008) for x, z in arr], 0.014, 0.008, 0.006)
        elip(mat('lengua', 0xc0504d, 0.5), 0, cara_y(L, 0, z0 - 0.04) + 0.004, z0 - 0.042, 0.035, esc=(1, 0.5, 0.45), sub=2)
        tira_cara(L, labio, aba, 0.01, 0.009)
        tira_cara(L, labio, arr, 0.008, 0.009)
    # mofletes
    if L['mofletes'] >= 0.25:
        rosa = mat('moflete_' + i, mezcla(L['piel'], 0xe8706a, 0.12 + 0.35 * L['mofletes']), 0.6)
        for s in (-1, 1):
            x, z = s * 0.2 * a, -0.08
            elip(rosa, x, cara_y(L, x, z) + 0.012, z, 0.06, esc=(1.2, 0.3, 0.8), sub=2)
    # arrugas
    if L['arrugas']:
        r = mat('arruga_' + i, oscuro(L['piel'], 0.82), 0.6)
        for s in (-1, 1):   # bolsas de los ojos
            tira_cara(L, r, [(s * (0.09 + 0.08 * k / 6), -0.035 - 0.012 * math.sin(k / 6 * math.pi)) for k in range(7)], 0.005, 0.004, 0.004)
        if L['arrugas'] > 1:
            for z in (0.2, 0.235):   # la frente
                tira_cara(L, r, [(t * 0.11, z + 0.008 * (1 - t * t)) for t in ts], 0.005, 0.004, 0.004)
            for s in (-1, 1):        # de la nariz a la boca
                tira_cara(L, r, [(s * (0.075 + 0.035 * k / 6), -0.07 - 0.1 * k / 6) for k in range(7)], 0.005, 0.004, 0.004)
    # bigote
    if L.get('bigote'):
        bm_ = mat('bigote_' + i, L['bigote'], 0.85)
        for s in (-1, 1):
            elip(bm_, s * 0.05, -0.352, -0.118, 0.048, esc=(1.6, 0.55, 0.62), rot=(0, s * 0.28, 0), sub=3)
    # pelo
    casco(L, mat('rapado_' + i, L['rapado'], 0.85) if L.get('rapado') else pelo(L))
    pelo_encima(L)


def pelo_encima(L):
    p, i = pelo(L), L['id']
    if i == 'putin':      # lo tapa el gorro: poco y fino
        casquete(L, p, r=0.377, alto=0.98, lado=0.12, frente_=0.3)
    elif i == 'kim':      # el bloque alto de arriba, con los lados rapados
        casquete(L, p, r=0.39, alto=1.36, lado=0.17, frente_=0.22)
        elip(p, 0, -0.27, 0.3, 0.1, esc=(2.4, 0.9, 0.6), rot=(0.55, 0, 0), sub=3)
    elif i == 'netanyahu':  # raya al lado, hacia atrás
        casquete(L, p, r=0.39, alto=1.07, lado=0.04, frente_=0.25)
        elip(p, -0.07, -0.27, 0.27, 0.1, esc=(2.3, 1.0, 0.55), rot=(0.45, 0, 0.28), sub=3)
        tira_cara(L, mat('raya_' + i, oscuro(L['pelo'][1], 0.8), 0.8), [(0.11, 0.3 + 0.05 * k / 4) for k in range(5)], 0.004, -0.03, 0.004)
    elif i == 'xi':       # todo hacia atrás, liso y alto
        casquete(L, p, r=0.392, alto=1.13, lado=0.05, frente_=0.26)
    elif i == 'milei':    # la melena: mechones gordos hacia todos lados
        casquete(L, p, r=0.4, alto=1.12, lado=-0.02, frente_=0.15)
        for k in range(12):
            ang = k / 12 * math.tau
            x, y = math.cos(ang) * 0.28, math.sin(ang) * 0.26 + 0.03
            elip(p, x, y, 0.26, 0.11, esc=(1.2, 1.25, 0.85), rot=(math.sin(ang) * 0.7, -math.cos(ang) * 0.7, ang), sub=2)
        for k in range(5):
            elip(p, -0.14 + 0.07 * k, -0.27, 0.26 + 0.02 * (k % 2), 0.07, esc=(0.9, 0.9, 1.5), rot=(0.6, 0, 0.3 - 0.15 * k), sub=2)
    elif i == 'maduro':
        casquete(L, p, r=0.392, alto=1.08, lado=0.03, frente_=0.2)
        for k in range(4):
            elip(p, -0.12 + 0.08 * k, -0.25, 0.27, 0.07, esc=(1.2, 1.0, 0.6), rot=(0.5, 0, 0), sub=2)
    elif i == 'bolsonaro':
        casquete(L, p, r=0.388, alto=1.05, lado=0.05, frente_=0.23)
        elip(p, -0.09, -0.27, 0.25, 0.09, esc=(2.3, 1.0, 0.55), rot=(0.45, 0, 0.28), sub=3)
    elif i == 'boris':    # la melena rubia despeinada, con el flequillo encima de los ojos
        casquete(L, p, r=0.4, alto=1.12, lado=0.0, frente_=0.16)
        import random
        rnd = random.Random(7)
        for k in range(16):
            ang = k / 16 * math.tau + rnd.uniform(-0.2, 0.2)
            x, y = math.cos(ang) * 0.27, math.sin(ang) * 0.25 + 0.02
            elip(p, x, y, 0.25 + rnd.uniform(-0.03, 0.06), 0.1, esc=(1.3, 1.1, 0.7),
                 rot=(rnd.uniform(-0.6, 0.6), rnd.uniform(-0.6, 0.6), ang), sub=2)
        for k in range(6):   # el flequillo, cayendo hacia un lado
            elip(p, -0.17 + 0.065 * k, -0.28, 0.23 + 0.02 * (k % 2), 0.075, esc=(0.9, 0.8, 1.6), rot=(0.7, 0, 0.5 - 0.1 * k), sub=2)
        elip(p, 0.0, 0.0, 0.37, 0.18, esc=(1.5, 1.4, 0.7), rot=(0.2, 0.1, 0.3), sub=2)
    else:                 # erdogan: con entradas
        casquete(L, p, r=0.383, alto=1.0, lado=0.1, frente_=0.3)


def ushanka(L):
    """El gorro ruso de Putin, con las orejeras atadas arriba y la estrella."""
    piel_ = mat_franjas('piel_gorro', 0x6e5d4e, 0x5e4e41, 40, eje='X', z0=-0.5, alto=1.0)
    cil(piel_, 0, 0.02, 0.17, 0.405, 0.23, 32)
    elip(piel_, 0, 0.02, 0.4, 0.4, esc=(1, 1, 0.4), sub=3)
    elip(piel_, 0, -0.3, 0.29, 0.21, esc=(1.75, 0.35, 0.8), rot=(-0.25, 0, 0), sub=3)   # visera doblada
    for s in (-1, 1):
        elip(piel_, s * 0.25, 0.04, 0.5, 0.16, esc=(0.8, 1.3, 0.35), rot=(0, s * 0.35, 0), sub=3)
    estrella(mat('estrella_roja', 0xd8322f, 0.4), (0, -0.395, 0.3), 0.06, grosor=0.012)
    cil(mat('oro', 0xd9b23c, 0.3), 0, -0.38, 0.3, 0.075, 0.008, 24, eje='Y')


def cabeza_entera(L):
    n0 = len(_partes)
    cabeza(L)
    if L['extra'] == 'ushanka':
        ushanka(L)
    for o in _partes[n0:]:
        o.scale = tuple(v * ESC_CABEZA for v in o.scale)
        o.location = o.location * ESC_CABEZA + CENTRO_CABEZA
    marca(n0, ['Head'])


# ---------------------------------------------------------------- lo de cada uno
def extra(L):
    e = L['extra']
    P = palma('Right')
    d = mano_dir('Right')
    lado = d.cross(ARRIBA).normalized()
    n0 = len(_partes)
    hueso = 'RightHand'
    if e == 'misil':          # Kim: un misil hacia arriba, en la mano
        base = P + ARRIBA * 0.02
        tubo(mat('misil', 0xeeeee8, 0.4), base, base + ARRIBA * 0.46, 0.05, 0.05, 18)
        tubo(mat('misil_rojo', 0xd8322f, 0.4), base + ARRIBA * 0.46, base + ARRIBA * 0.6, 0.05, 0.0, 18)
        tubo(mat('misil_rojo', 0xd8322f, 0.4), base + ARRIBA * 0.22, base + ARRIBA * 0.25, 0.052, 0.052, 18)
        for k in range(4):
            a = k / 4 * math.tau
            v = Vector((math.cos(a), math.sin(a), 0))
            caja(mat('misil_rojo', 0xd8322f, 0.4), *(base + v * 0.062), 0.014, 0.07, 0.11, giro=a + math.pi / 2)
        for sy in (-1, 1):
            estrella(mat('estrella_roja', 0xd8322f, 0.4), base + ARRIBA * 0.34 + Vector((0, sy * 0.051, 0)), 0.026, atras=sy > 0)
    elif e == 'cartel':       # Netanyahu: el cartel de la bomba con la línea roja (ONU, 2012)
        base = P + ARRIBA * 0.01
        tubo(mat('palo', 0x9a6a3a, 0.7), base - ARRIBA * 0.02, base + ARRIBA * 0.42, 0.013, 0.013, 8)
        c = base + ARRIBA * 0.55
        caja(mat('carton', 0xf8f6ee, 0.6), c.x, c.y, c.z - 0.13, 0.32, 0.014, 0.26)
        for sy in (-1, 1):    # el dibujo por las dos caras
            y = c.y + sy * 0.009
            cil(mat('bomba', 0x111114, 0.4), c.x, y, c.z - 0.03, 0.075, 0.004, 24, eje='Y')
            caja(mat('bomba', 0x111114, 0.4), c.x + 0.03, y, c.z + 0.035, 0.03, 0.004, 0.03, giro=0, inclina=0)
            caja(mat('mecha', 0xe0a030, 0.5), c.x + 0.05, y, c.z + 0.06, 0.008, 0.004, 0.04)
            caja(mat('linea_roja', 0xd8322f, 0.4), c.x, c.y + sy * 0.013, c.z + 0.0, 0.24, 0.004, 0.016)
    elif e == 'miel':         # Xi: el tarro de miel (el de Winnie)
        c = P + ARRIBA * 0.085
        bola(mat('tarro', 0xd98a24, 0.25), c, 0.085, esc=(1, 1, 0.95), sub=3)
        tubo(mat('tarro', 0xd98a24, 0.25), c + ARRIBA * 0.06, c + ARRIBA * 0.1, 0.055, 0.06, 20)
        tubo(mat('etiqueta', 0xf3ead2, 0.6), c - ARRIBA * 0.02, c + ARRIBA * 0.025, 0.087, 0.087, 24)
        for k in range(5):    # la miel que rebosa
            a = k / 5 * math.tau
            bola(mat('miel', 0xffc21a, 0.15), c + ARRIBA * (0.09 - 0.02 * (k % 2)) + Vector((math.cos(a), math.sin(a), 0)) * 0.055, 0.022, esc=(1, 1, 1.4), sub=2)
        bola(mat('miel', 0xffc21a, 0.15), c + ARRIBA * 0.1, 0.05, esc=(1, 1, 0.4), sub=2)
    elif e == 'motosierra':   # Milei: la motosierra en alto
        eje = (d * 0.35 + ARRIBA).normalized()
        caja(mat('motor', 0xf28c1c, 0.4), P.x, P.y, P.z - 0.02, 0.1, 0.2, 0.15, giro=math.atan2(-eje.x, eje.y))
        caja(mat('motor_negro', 0x222226, 0.5), P.x, P.y, P.z + 0.13, 0.06, 0.06, 0.03)
        a, b = P + eje * 0.12, P + eje * 0.62
        tubo(mat('espada', 0xc9ccd2, 0.25), a, b, 0.035, 0.03, 4)
        cad = mat('cadena', 0x3a3c42, 0.4)
        for k in range(14):
            q = a + (b - a) * (k / 13)
            bola(cad, q, 0.016, esc=(1.6, 1.6, 0.8), sub=1)
    elif e == 'brexit':       # Boris: la bandera britanica en alto
        base = P + ARRIBA * 0.01
        tubo(mat('palo', 0x9a6a3a, 0.7), base - ARRIBA * 0.02, base + ARRIBA * 0.62, 0.012, 0.012, 8)
        c = base + ARRIBA * 0.5 + Vector((0.2 if base.x > 0 else -0.2, 0, 0))
        def banda(m, w, h, giro, grosor):
            bpy.ops.mesh.primitive_cube_add(size=1, location=(c.x, c.y, c.z))
            o = bpy.context.object
            o.scale = (w, grosor, h)
            o.rotation_euler = (0, giro, 0)
            return _poner(o, m)
        azul, blanco_, rojo_ = mat('uk_azul', 0x1f3f9a, 0.5), mat('uk_blanco', 0xffffff, 0.5), mat('uk_rojo', 0xc8102e, 0.5)
        banda(azul, 0.38, 0.22, 0, 0.006)
        a = math.atan2(0.22, 0.38)
        for g in (a, -a):
            banda(blanco_, 0.44, 0.045, g, 0.009)
            banda(rojo_, 0.44, 0.016, g, 0.011)
        banda(blanco_, 0.38, 0.07, 0, 0.012)
        banda(blanco_, 0.07, 0.22, 0, 0.012)
        banda(rojo_, 0.38, 0.04, 0, 0.015)
        banda(rojo_, 0.04, 0.22, 0, 0.015)
    elif e == 'te':           # Erdoğan: el vaso de té turco, con su platito
        c = P + ARRIBA * 0.03
        cil(mat('platito', 0xc8323a, 0.35), c.x, c.y, c.z, 0.065, 0.01, 24)
        filas_vaso = [(0.0, 0.03), (0.03, 0.038), (0.06, 0.028), (0.09, 0.034), (0.13, 0.04)]
        v = torno(mat('te', 0xa8401c, 0.15), [(z, r) for z, r in filas_vaso], 20, 1.0)
        v.location = (c.x, c.y, c.z + 0.01)
        tubo(mat('borde_oro', 0xd9b23c, 0.25), c + ARRIBA * 0.135, c + ARRIBA * 0.145, 0.041, 0.041, 20)
    elif e == 'pajarito':     # Maduro: el pajarito que le habla, en el hombro
        hueso = 'RightShoulder'
        c = Vector((-0.215, CY + 0.03, 1.49))
        am, az = mat('pajaro', 0xffd23c, 0.5), mat('pajaro_azul', 0x2a5fd0, 0.5)
        bola(am, c, 0.05, esc=(0.85, 1.25, 0.9), sub=3)
        bola(am, c + Vector((0, -0.05, 0.05)), 0.035, sub=3)
        tubo(mat('pico', 0xf28c1c, 0.4), c + Vector((0, -0.08, 0.05)), c + Vector((0, -0.11, 0.045)), 0.012, 0.0, 8)
        for s in (-1, 1):
            bola(mat('pupila', 0x120c08, 0.2), c + Vector((s * 0.022, -0.072, 0.06)), 0.007, sub=1)
            bola(az, c + Vector((s * 0.04, 0.0, 0.0)), 0.035, esc=(0.35, 1.2, 0.7), sub=2)
        tubo(az, c + Vector((0, 0.05, 0.0)), c + Vector((0, 0.11, 0.03)), 0.025, 0.006, 8)
    if e == 'pajarito':   # un poco mayor, que se vea
        for o in _partes[n0:]:
            o.scale = tuple(v * 1.35 for v in o.scale)
            o.location = c + (o.location - c) * 1.35
    marca(n0, [hueso])


# ---------------------------------------------------------------- retrato
def retrato(L, ob):
    sc = bpy.context.scene
    act = next((a for a in bpy.data.actions if 'walking' in a.name), None)
    if act and arm.animation_data is None:
        arm.animation_data_create()
    if act:
        arm.animation_data.action = act
        try:
            if act.slots:
                arm.animation_data.action_slot = act.slots[0]
        except Exception:
            pass
        sc.frame_set(int(act.frame_range[0] + 11))
    ob.hide_render = False
    sc.render.resolution_x = sc.render.resolution_y = 256
    sc.render.film_transparent = True
    sc.cycles.samples = 12 if RAPIDO else 48
    sc.world.node_tree.nodes['Background'].inputs['Strength'].default_value = 0.6
    bpy.ops.object.light_add(type='SUN', location=(1, -2, 3))
    sol = bpy.context.object
    sol.data.energy = 3.0
    sol.rotation_euler = (math.radians(50), math.radians(10), math.radians(-25))
    bpy.ops.object.camera_add(location=(0.5, -2.1, 1.78))
    cam = bpy.context.object
    cam.data.lens = 75
    mira = bpy.data.objects.new('mira', None)
    sc.collection.objects.link(mira)
    mira.location = (0, -0.05, 1.6)
    cam.constraints.new('TRACK_TO').target = mira
    sc.camera = cam
    sc.render.filepath = os.path.join(MODELOS, 'lideres', L['id'] + '.png')
    sc.render.image_settings.file_format = 'PNG'
    sc.render.image_settings.color_mode = 'RGBA'
    bpy.ops.render.render(write_still=True)
    print('RETRATO', L['id'], flush=True)


def vistas(L):
    """Fotos de prueba corriendo (blender/_tmp/<id>_vista<n>.png), con --vistas."""
    sc = bpy.context.scene
    act = next((a for a in bpy.data.actions if 'running' in a.name), None)
    arm.animation_data.action = act
    try:
        arm.animation_data.action_slot = act.slots[0]
    except Exception:
        pass
    sc.render.resolution_x, sc.render.resolution_y = 320, 400
    mira = bpy.data.objects['mira']
    mira.location = (0, 0, 1.0)
    cam = sc.camera
    cam.data.lens = 50
    for n, (pos, f) in enumerate((((1.6, 3.2, 1.7), 4), ((-3.4, -0.6, 1.2), 9), ((0.9, -3.3, 1.3), 13))):
        cam.location = pos
        sc.frame_set(int(act.frame_range[0] + f))
        sc.render.filepath = os.path.join(TMP, '%s_vista%d.png' % (L['id'], n))
        bpy.ops.render.render(write_still=True)


def hacer(i):
    L = dict(LIDERES[i], id=i)
    cargar_esqueleto()
    bpy.context.scene.world.light_settings.distance = 0.15
    tronco(L)
    brazos(L)
    piernas(L)
    cabeza_entera(L)
    extra(L)
    pesar()
    ob = terminar(i, 'lideres', lado=2048, bisel=0.004, oclusion=0.5, suelo=False, exportar=False, min_bisel=0.015)
    # Se pone en el sitio de la malla de Meshy: mismo padre y mismas medidas.
    M = char1.matrix_world.copy()
    ob.data.transform(M.inverted())
    ob.parent = arm
    ob.matrix_parent_inverse = char1.matrix_parent_inverse.copy()
    ob.matrix_basis = char1.matrix_basis.copy()
    md = ob.modifiers.new('Armature', 'ARMATURE')
    md.object = arm
    bpy.data.objects.remove(char1)
    if arm.animation_data:
        arm.animation_data.action = None
    for pb in arm.pose.bones:
        pb.matrix_basis = Matrix.Identity(4)
    bpy.ops.object.select_all(action='DESELECT')
    arm.select_set(True); ob.select_set(True)
    bpy.context.view_layer.objects.active = ob
    salida = os.path.join(MODELOS, 'lideres')
    os.makedirs(salida, exist_ok=True)
    kw = dict(filepath=os.path.join(salida, i + '.glb'), export_format='GLB', use_selection=True,
              export_image_format='JPEG', export_animations=False, export_yup=True, export_skins=True)
    try:
        bpy.ops.export_scene.gltf(**kw, export_jpeg_quality=85)
    except TypeError:
        bpy.ops.export_scene.gltf(**kw)
    tris = sum(len(p.vertices) - 2 for p in ob.data.polygons)
    print('LIDER exportado:', i, tris, 'triángulos', flush=True)
    retrato(L, ob)
    if '--vistas' in ARGS:
        vistas(L)


for i in (SOLO or LIDERES):
    hacer(i)
