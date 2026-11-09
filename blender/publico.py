# El público de la acera (25/10/2026; rehecho el 09/11/2026).
#
#   blender -b -P blender/publico.py -- [persona ...] [--rapido]
#
# 25/10: Isidro: «el público parecen Playmobils sin alma» -> personas con cara.
# 09/11: «la gente mueve el brazo como locas, ¿puedes mejorar la estética de
# las personas en general?». Aquellas eran bolas y palos sueltos con ojos
# saltones, y solo el brazo derecho se movía. Ahora:
#   - cuerpo, brazos y piernas de una pieza suave cada uno (malla de «piel»
#     con subdivisión: hombros, codos y rodillas sin juntas de muñeco);
#   - proporciones de dibujos de Pixar pero de persona (no cabezudos);
#   - cara tranquila: ojos pequeños con iris de color y párpado, cejas finas,
#     nariz, boca, orejas; pelo con volumen;
#   - CINCO piezas por persona, cada una con su giro en la articulación:
#     `<n>_cuerpo`, `<n>_brazo_d`, `<n>_brazo_i`, `<n>_pierna_d`, `<n>_pierna_i`.
#     El juego las mueve: andar de verdad (brazos contra piernas), aplaudir,
#     saludar despacio.
#   - once personas (siete de antes, rehechas, y cuatro nuevas).
#
# Miran a -y (en el juego, +z). El origen, en el suelo entre los pies.
# Al final imprime ARTICULACIONES con dónde va cada hombro y cada cadera.

import os, sys, math, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import *
from comun import _poner
import comun

PIELES = (0xf3c6a2, 0xdca27a, 0xb07650, 0x7f5034)
OJOS = (0x5a3a22, 0x3a6a9a, 0x4a6a3a, 0x2a1c14)


def M(color, rug=0.65):
    return mat(f'c{color:06x}_{int(rug * 100)}', color, rug)


def elip(m, x, y, z, r, esc=(1, 1, 1), rot=(0, 0, 0), sub=2, mitad=False):
    o = esfera(m, x, y, z, r, sub, esc=esc, mitad=mitad)
    o.rotation_euler = rot
    return o


def tubo(m, puntos, sub=2, tapas=True):
    """Malla orgánica a lo largo de una cadena de puntos (x, y, z, radio_x, radio_y):
    modificador de piel + subdivisión. Hace hombros, codos y cinturas sin juntas.
    (La subdivisión encoge un 8 % y deja las puntas planas a ras del último
    punto: se compensa el grosor y se añade una punta redondeada a cada lado.)"""
    from mathutils import Vector
    puntos = [(x, y, z, rx * 1.09, ry * 1.09) for x, y, z, rx, ry in puntos]
    if tapas:
        def punta(a, b):
            d = (Vector(a[:3]) - Vector(b[:3])).normalized() * min(a[3], a[4]) * 0.8
            return (a[0] + d.x, a[1] + d.y, a[2] + d.z, a[3] * 0.6, a[4] * 0.6)
        puntos = [punta(puntos[0], puntos[1])] + puntos + [punta(puntos[-1], puntos[-2])]
    me = bpy.data.meshes.new('tubo')
    o = bpy.data.objects.new('tubo', me)
    bpy.context.collection.objects.link(o)
    bm = bmesh.new()
    vs = [bm.verts.new(p[:3]) for p in puntos]
    for a, b in zip(vs, vs[1:]):
        bm.edges.new((a, b))
    bm.to_mesh(me)
    bm.free()
    o.modifiers.new('piel', 'SKIN')
    for i, p in enumerate(puntos):
        sv = o.data.skin_vertices[0].data[i]
        sv.radius = (p[3], p[4])
        sv.use_root = i == 0
    sd = o.modifiers.new('suave', 'SUBSURF')
    sd.levels = sub
    sd.render_levels = sub
    bpy.ops.object.select_all(action='DESELECT')
    o.select_set(True)
    bpy.context.view_layer.objects.active = o
    bpy.ops.object.modifier_apply(modifier='piel')
    bpy.ops.object.modifier_apply(modifier='suave')
    return _poner(o, m)


# ---------------------------------------------------------------- la cabeza
def cabeza(piel, ojo, x0, z0, r, pelo_c, peinado, sonrisa=0.22, gafas=None, bigote=False, barba=False):
    p = M(piel, 0.55)
    # cabeza de una pieza: barbilla, mejillas, sienes y coronilla
    tubo(p, [(x0, -r * 0.3, z0 - r * 0.62, r * 0.42, r * 0.4),
             (x0, -r * 0.08, z0 - r * 0.2, r * 0.8, r * 0.82),
             (x0, 0, z0 + r * 0.3, r * 0.86, r * 0.92),
             (x0, r * 0.05, z0 + r * 0.62, r * 0.6, r * 0.66)], sub=3)
    for s in (-1, 1):
        elip(p, x0 + s * r * 0.88, r * 0.05, z0 - r * 0.02, r * 0.2, esc=(0.45, 0.75, 1.1), sub=1)   # orejas
        ex, ey, ez = x0 + s * r * 0.36, -r * 0.87, z0 + r * 0.06
        elip(M(0xf8f6f0, 0.25), ex, ey, ez, r * 0.17, esc=(1.0, 0.45, 0.72))      # blanco del ojo
        elip(M(ojo, 0.3), ex, ey - r * 0.055, ez - r * 0.01, r * 0.095, esc=(1, 0.45, 1))     # iris
        elip(M(0x141010, 0.2), ex, ey - r * 0.085, ez - r * 0.01, r * 0.05, esc=(1, 0.4, 1), sub=1)  # pupila
        elip(M(0xffffff, 0.1), ex - s * r * 0.03, ey - r * 0.1, ez + r * 0.035, r * 0.022, sub=1)  # brillo
        elip(p, ex, ey - r * 0.012, ez + r * 0.045, r * 0.19, esc=(1.05, 0.5, 0.62), sub=1, mitad=True)  # párpado
        # ceja algo arqueada
        c = M(pelo_c, 0.8)
        rama(c, (ex - s * r * 0.17, ey - r * 0.02, ez + r * 0.2), (ex + s * r * 0.0, ey - r * 0.06, ez + r * 0.26), r * 0.035, r * 0.04, 6)
        rama(c, (ex + s * r * 0.0, ey - r * 0.06, ez + r * 0.26), (ex + s * r * 0.17, ey - r * 0.02, ez + r * 0.22), r * 0.04, r * 0.025, 6)
    elip(p, x0, -r * 0.95, z0 - r * 0.16, r * 0.13, esc=(0.75, 0.9, 1.15))       # nariz
    labio = M(0xb5585a, 0.5)
    if sonrisa:
        bpy.ops.mesh.primitive_torus_add(major_radius=r * sonrisa, minor_radius=r * 0.034,
                                         location=(x0, -r * 0.9, z0 - r * 0.32))
        o = bpy.context.object
        o.rotation_euler = (math.pi / 2, 0, 0)
        bm = bmesh.new(); bm.from_mesh(o.data)
        bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.co.y > -r * 0.08], context='VERTS')
        bm.to_mesh(o.data); bm.free()
        _poner(o, labio)
    else:
        elip(labio, x0, -r * 0.9, z0 - r * 0.4, r * 0.12, esc=(1.2, 0.4, 0.35))
    if bigote:
        elip(M(pelo_c, 0.8), x0, -r * 0.9, z0 - r * 0.28, r * 0.13, esc=(1.6, 0.5, 0.45))
    if barba:
        elip(M(pelo_c, 0.85), x0, -r * 0.35, z0 - r * 0.62, r * 0.6, esc=(1.05, 0.95, 0.75))
    if gafas:
        g = M(gafas, 0.3)
        for s in (-1, 1):
            bpy.ops.mesh.primitive_torus_add(major_radius=r * 0.2, minor_radius=r * 0.025,
                                             location=(x0 + s * r * 0.36, -r * 0.98, z0 + r * 0.06))
            o = bpy.context.object
            o.rotation_euler = (math.pi / 2, 0, 0)
            _poner(o, g)
        rama(g, (x0 - r * 0.16, -r * 1.0, z0 + r * 0.08), (x0 + r * 0.16, -r * 1.0, z0 + r * 0.08), r * 0.02, r * 0.02, 5)
    pelo(M(pelo_c, 0.85), x0, z0, r, peinado)


def pelo(m, x0, z0, r, peinado):
    """Peinados con volumen (no un casco liso)."""
    def casquete():
        # Por delante queda detras de la frente: el nacimiento del pelo sale alto.
        elip(m, x0, r * 0.24, z0 + r * 0.24, r * 1.0, esc=(0.97, 1.0, 0.98), sub=3)
    if peinado in ('corto', 'raya', 'canoso'):
        casquete()
        elip(m, x0 - r * 0.25, -r * 0.55, z0 + r * 0.62, r * 0.42, esc=(1.3, 0.8, 0.45), rot=(0.3, 0, 0.2))   # flequillo
        for s in (-1, 1):
            elip(m, x0 + s * r * 0.8, r * 0.15, z0 + r * 0.15, r * 0.28, esc=(0.5, 1.0, 1.2))  # patillas
    elif peinado == 'calvo':
        for s in (-1, 1):
            elip(m, x0 + s * r * 0.8, r * 0.25, z0 - r * 0.0, r * 0.32, esc=(0.45, 1.1, 0.8))
        elip(m, x0, r * 0.75, z0 - r * 0.02, r * 0.5, esc=(1.4, 0.45, 0.7))
    elif peinado == 'mono':          # moño de señora, pelo ahuecado
        casquete()
        elip(m, x0, r * 0.3, z0 + r * 1.05, r * 0.38)
        for s in (-1, 1):
            elip(m, x0 + s * r * 0.82, r * 0.0, z0 - r * 0.1, r * 0.34, esc=(0.55, 1.0, 1.1))
    elif peinado == 'coleta':
        casquete()
        elip(m, x0 + r * 0.2, -r * 0.55, z0 + r * 0.6, r * 0.45, esc=(1.4, 0.75, 0.45), rot=(0.3, 0, -0.25))
        rama(m, (x0, r * 0.95, z0 + r * 0.25), (x0, r * 1.2, z0 - r * 1.1), r * 0.25, r * 0.12, 8)
    elif peinado == 'melena':
        casquete()
        elip(m, x0, r * 0.45, z0 - r * 0.7, r * 0.95, esc=(1.12, 0.6, 1.0))
        for s in (-1, 1):
            elip(m, x0 + s * r * 0.82, r * 0.1, z0 - r * 0.55, r * 0.35, esc=(0.55, 0.9, 1.6))
        elip(m, x0 + r * 0.15, -r * 0.6, z0 + r * 0.58, r * 0.45, esc=(1.5, 0.7, 0.45), rot=(0.35, 0, -0.15))
    elif peinado == 'rizos':
        for i in range(14):
            a = i / 14 * math.tau
            elip(m, x0 + math.cos(a) * r * 0.72, r * 0.15 + math.sin(a) * r * 0.62, z0 + r * 0.62, r * 0.36, sub=1)
        casquete()
    elif peinado == 'nada':
        pass


def gorra(m, x0, z0, r, visera=None, casco=False):
    if casco:
        elip(m, x0, r * 0.05, z0 + r * 0.35, r * 1.12, esc=(1.0, 1.08, 0.78), mitad=True)
        cil(m, x0, r * 0.05, z0 + r * 0.3, r * 1.2, r * 0.07, 24)
        rama(m, (x0, -r * 0.7, z0 + r * 1.0), (x0, r * 0.8, z0 + r * 1.05), r * 0.08, r * 0.08, 6)
        return
    elip(m, x0, r * 0.06, z0 + r * 0.32, r * 1.03, esc=(1.0, 1.02, 0.72), mitad=True)
    elip(visera or m, x0, -r * 0.92, z0 + r * 0.36, r * 0.62, esc=(1.0, 0.85, 0.12))


# ---------------------------------------------------------------- el cuerpo
class P:
    """Medidas de una persona (k = estatura / 1.75)."""
    def __init__(self, alto, ancho=1.0, nino=False):
        self.k = k = alto / 1.75
        self.a = ancho
        self.nino = nino
        self.cad_z = 0.93 * k if not nino else 0.88 * k
        self.cad_x = 0.085 * k * ancho
        self.hom_z = 1.4 * k if not nino else 1.28 * k
        self.hom_x = 0.19 * k * ancho if not nino else 0.17 * k * ancho
        self.cab_z = (1.6 if not nino else 1.5) * k
        self.cab_r = (0.13 if not nino else 0.16) * k


def torso(p, ropa, pantalon=None, falda=None, cinturon=None, cuello=None, abierto=None):
    """Tronco: caderas, cintura, pecho y hombros de una pieza, y el cuello."""
    k, a = p.k, p.a
    z0, z1 = p.cad_z, p.hom_z
    ro = M(ropa)
    tubo(ro, [(0, 0, z0 + 0.09 * k, 0.15 * k * a, 0.1 * k),
              (0, 0, z0 + 0.2 * k, 0.15 * k * a, 0.1 * k),
              (0, 0, (z0 + z1) / 2 + 0.08 * k, 0.17 * k * a, 0.11 * k),
              (0, 0.005, z1 - 0.05 * k, p.hom_x * 0.95, 0.1 * k)])
    if pantalon is not None and cinturon is None:
        cinturon = 0x2a2420
    if pantalon is not None:              # caderas del pantalón (de él salen las piernas)
        tubo(M(pantalon), [(0, 0, z0 - 0.1 * k, 0.15 * k * a, 0.1 * k),
                           (0, 0, z0 + 0.02 * k, 0.158 * k * a, 0.106 * k),
                           (0, 0, z0 + 0.12 * k, 0.153 * k * a, 0.102 * k)])
    if falda is not None:
        cil(M(falda), 0, 0, z0 - 0.38 * k, 0.21 * k * a, 0.5 * k, 20, r2=0.15 * k * a)
    if cinturon is not None:
        o = cil(M(cinturon, 0.4), 0, 0, z0 + 0.07 * k, 0.16 * k * a, 0.035 * k, 20)
        o.scale = (1, 0.69, 1)
        caja(M(0xc9a64a, 0.3), 0, -0.11 * k, z0 + 0.075 * k, 0.04 * k, 0.012, 0.028 * k)
    piel = M(PIEL_ACTUAL[0], 0.55)
    cil(piel, 0, 0.0, z1 - 0.04 * k, 0.058 * k, p.cab_z - z1, 12, r2=0.052 * k)
    if cuello:                            # cuello de la camisa
        bpy.ops.mesh.primitive_torus_add(major_radius=0.062 * k, minor_radius=0.014 * k, location=(0, 0, z1 + 0.005 * k))
        _poner(bpy.context.object, M(cuello, 0.5))
    if abierto:                           # chaqueta abierta: la camisa por dentro
        caja(M(abierto, 0.5), 0, -0.108 * k, (z0 + z1) / 2 - 0.02 * k, 0.065 * k, 0.012 * k, (z1 - z0) * 0.55)


PIEL_ACTUAL = [0xffffff]


def brazo(p, lado, piel, manga, largo=True, objeto=None, puno=None):
    """Brazo con el origen en el hombro. lado: 1 = +x (el «derecho» del juego)."""
    k, s = p.k, lado
    L = p.hom_z - p.cad_z + 0.12 * k        # hasta la muñeca
    codo = (s * 0.03 * k, 0.0, -L * 0.48)
    muneca = (s * 0.045 * k, -0.035 * k, -L * 0.94)
    pm = M(piel, 0.55)
    tubo(pm, [(0, 0, -0.04 * k, 0.046 * k, 0.046 * k), (*codo, 0.036 * k, 0.036 * k), (*muneca, 0.027 * k, 0.024 * k)], sub=2)
    mg = M(manga)
    if largo == 'no':
        pass
    elif largo:
        tubo(mg, [(0, 0, -0.03 * k, 0.054 * k, 0.054 * k), (*codo, 0.043 * k, 0.043 * k),
                  (muneca[0], muneca[1] + 0.005 * k, muneca[2] + 0.05 * k, 0.036 * k, 0.034 * k)], sub=2)
        if puno:
            o = cil(M(puno, 0.5), muneca[0], muneca[1] + 0.004 * k, muneca[2] + 0.025 * k, 0.04 * k, 0.025 * k, 12)
    else:
        tubo(mg, [(0, 0, -0.03 * k, 0.058 * k, 0.058 * k), (codo[0] * 0.5, 0, codo[2] * 0.6, 0.05 * k, 0.05 * k)], sub=2)
    # mano: palma, dedos juntos y pulgar
    hx, hy, hz = muneca[0] + s * 0.004 * k, muneca[1] - 0.006 * k, muneca[2] - 0.055 * k
    elip(pm, hx, hy, hz, 0.042 * k, esc=(0.48, 0.95, 1.15))
    elip(pm, hx + s * 0.002 * k, hy - 0.005 * k, hz - 0.045 * k, 0.03 * k, esc=(0.5, 0.95, 1.0))
    rama(pm, (hx - s * 0.012 * k, hy - 0.025 * k, hz + 0.02 * k), (hx - s * 0.03 * k, hy - 0.045 * k, hz - 0.015 * k), 0.012 * k, 0.01 * k, 6)
    mano = (hx, hy, hz - 0.03 * k)
    if objeto == 'bandera':
        cil(M(0x8a6a4a, 0.7), mano[0], mano[1], mano[2] - 0.12 * k, 0.008, 0.75 * k, 6)
        caja(mat_franjas('franjas_pub', 0xd8283a, 0xffffff, 7, z0=mano[2] + 0.3 * k, alto=0.3 * k),
             mano[0] + s * 0.21 * k, mano[1], mano[2] + 0.3 * k, 0.4 * k, 0.008, 0.3 * k)
        caja(M(0x1f3c88), mano[0] + s * 0.1 * k, mano[1] - 0.005, mano[2] + 0.46 * k, 0.17 * k, 0.008, 0.14 * k)
    elif objeto == 'cartel':
        cil(M(0x8a6a4a, 0.7), mano[0], mano[1], mano[2] - 0.12 * k, 0.012, 1.0 * k, 6)
        caja(M(0xffffff, 0.6), mano[0], mano[1] - 0.02 * k, mano[2] + 0.6 * k, 0.55 * k, 0.02, 0.34 * k)
        texto(M(0xd8283a, 0.5), 'USA!', mano[0], mano[1] - 0.04 * k, mano[2] + 0.72 * k, tam=0.15 * k, prof=0.01)
    elif objeto == 'globo':
        cil(M(0xdddddd, 0.5), mano[0], mano[1], mano[2], 0.004, 1.15, 4)
        elip(M(0xe8463c, 0.25), mano[0], mano[1], mano[2] + 1.3, 0.19, esc=(1, 1, 1.18))
    elif objeto == 'bolso':
        caja(M(0x6a3a28, 0.45), mano[0] + s * 0.02 * k, mano[1], mano[2] - 0.2 * k, 0.07 * k, 0.24 * k, 0.17 * k)
        rama(M(0x4a2a1c, 0.5), (mano[0], mano[1] - 0.08 * k, mano[2] - 0.04 * k), (mano[0], mano[1] + 0.08 * k, mano[2] - 0.04 * k), 0.008, 0.008, 5)
    elif objeto == 'cafe':
        cil(M(0xf2efe6, 0.5), mano[0], mano[1] - 0.03 * k, mano[2] - 0.05 * k, 0.03 * k, 0.11 * k, 12, r2=0.036 * k)
        cil(M(0x2d5a3a, 0.5), mano[0], mano[1] - 0.03 * k, mano[2] - 0.01 * k, 0.033 * k, 0.04 * k, 12)
    elif objeto == 'telefono':
        caja(M(0x1d1f25, 0.3), mano[0], mano[1] - 0.04 * k, mano[2] - 0.02 * k, 0.04 * k, 0.012, 0.08 * k)


def pierna(p, lado, pantalon, zapato, piel=None, corto=False, calcetin=None, bota=False):
    """Pierna con el origen en la cadera."""
    k, s = p.k, lado
    L = p.cad_z
    rod = (s * 0.005 * k, -0.01 * k, -L * 0.5)
    tob = (s * 0.01 * k, 0.005 * k, -L * 0.9)
    if piel is not None:                    # pierna al aire (falda, pantalón corto)
        tubo(M(piel, 0.55), [(0, 0, 0, 0.078 * k, 0.078 * k), (*rod, 0.048 * k, 0.05 * k),
                             (rod[0], rod[1] + 0.014 * k, rod[2] - 0.12 * k, 0.055 * k, 0.058 * k), (*tob, 0.031 * k, 0.031 * k)])
    if not corto and piel is None:
        tubo(M(pantalon), [(0, 0, 0.02 * k, 0.09 * k, 0.092 * k), (*rod, 0.064 * k, 0.066 * k),
                           (tob[0], tob[1], tob[2] + 0.03 * k, 0.056 * k, 0.058 * k)])
    elif corto:
        tubo(M(pantalon), [(0, 0, 0.02 * k, 0.088 * k, 0.09 * k), (rod[0], rod[1], rod[2] * 0.55, 0.076 * k, 0.078 * k)])
    if calcetin:
        cil(M(calcetin, 0.7), tob[0], tob[1], tob[2] - 0.02 * k, 0.038 * k, 0.09 * k, 10)
    z = M(zapato, 0.4)
    if bota:
        cil(z, tob[0], tob[1], tob[2] - 0.05 * k, 0.05 * k, 0.16 * k, 12)
    elip(z, tob[0], tob[1] - 0.045 * k, -L + 0.04 * k, 0.05 * k, esc=(0.9, 2.1, 0.8))
    elip(M(0x2a2420, 0.7), tob[0], tob[1] - 0.045 * k, -L + 0.012 * k, 0.05 * k, esc=(0.95, 2.15, 0.28))   # suela


# ---------------------------------------------------------------- las personas
# Cada una devuelve las piezas: cuerpo(), brazo_d(), brazo_i(), pierna_d(), pierna_i().
def persona(alto, ancho, piel, ojo, ropa, pantalon, zapato, pelo_c, peinado, extra_cuerpo=None,
            manga=None, largo=True, puno=None, obj_d=None, obj_i=None, falda=None, piernas_piel=False,
            corto=False, cinturon=None, cuello=None, abierto=None, calcetin=None, bota=False, nino=False,
            cara_kw=None):
    p = P(alto, ancho, nino)
    PIEL_ACTUAL[0] = piel

    def cuerpo():
        torso(p, ropa, None if falda else pantalon, falda, cinturon, cuello, abierto)
        cabeza(piel, ojo, 0, p.cab_z, p.cab_r, pelo_c, peinado, **(cara_kw or {}))
        if extra_cuerpo:
            extra_cuerpo(p)

    return p, {
        'cuerpo': cuerpo,
        'brazo_d': lambda: brazo(p, 1, piel, manga or ropa, largo, obj_d, puno),
        'brazo_i': lambda: brazo(p, -1, piel, manga or ropa, largo, obj_i, puno),
        'pierna_d': lambda: pierna(p, 1, pantalon, zapato, piel if (falda or piernas_piel) else None, corto, calcetin, bota),
        'pierna_i': lambda: pierna(p, -1, pantalon, zapato, piel if (falda or piernas_piel) else None, corto, calcetin, bota),
    }


def ejecutivo():
    def extra(p):
        k = p.k
        caja(M(0xffffff, 0.5), 0, -0.1 * k, p.hom_z - 0.2 * k, 0.09 * k, 0.02, 0.18 * k)
        rama(M(0x2f6bd8, 0.45), (0, -0.115 * k, p.hom_z - 0.06 * k), (0, -0.125 * k, p.hom_z - 0.33 * k), 0.018 * k, 0.03 * k, 4)
        for s in (-1, 1):   # solapas
            caja(M(0x24304a, 0.6), s * 0.06 * k, -0.112 * k, p.hom_z - 0.3 * k, 0.04 * k, 0.015, 0.26 * k, giro=0, inclina=0)
    return persona(1.82, 1.08, PIELES[0], OJOS[1], 0x2c3a52, 0x2c3a52, 0x1d1a18, 0x5a3a28, 'raya',
                   extra, puno=0xffffff, cuello=0xffffff, obj_i='telefono')


def senora():
    def extra(p):
        k = p.k
        for i in range(5):
            a = (i - 2) * 0.32
            elip(M(0xf6f0e0, 0.25), math.sin(a) * 0.08 * k, -math.cos(a) * 0.08 * k - 0.03 * k, p.hom_z - 0.02 * k - abs(i - 2) * 0.012 * k, 0.014 * k, sub=2)
    return persona(1.66, 1.02, PIELES[1], OJOS[0], 0xd8607a, 0x000000, 0xb83a52, 0xd6d0c6, 'mono',
                   extra, falda=0x9a3a52, obj_d='bandera', cara_kw={'gafas': 0x8a3a52})


def chico():
    def extra(p):
        k = p.k
        elip(M(0xd8283a, 0.5), 0, -0.1 * k, p.hom_z - 0.22 * k, 0.05 * k, esc=(1, 0.3, 1), sub=1)
    return persona(1.2, 1.0, PIELES[2], OJOS[0], 0xffc53a, 0x3a6ad8, 0xe8463c, 0x2a1a12, 'rizos',
                   extra, largo=False, corto=True, piernas_piel=True, calcetin=0xffffff, nino=True, obj_i='globo',
                   cara_kw={'sonrisa': 0.3})


def abuelo():
    def extra(p):
        k = p.k
        for i in range(4):
            esfera(M(0xe8dcc0, 0.4), 0, -0.118 * k, p.cad_z + (0.12 + i * 0.09) * k, 0.01 * k, 1)
        gorra(M(0xd8283a, 0.6), 0, p.cab_z, p.cab_r)
    return persona(1.68, 1.12, PIELES[0], OJOS[1], 0x7a8a5a, 0x8a7a6a, 0x5a3a28, 0xe8e4dc, 'calvo',
                   extra, cinturon=0x3a2a1e, obj_d='cartel', cara_kw={'gafas': 0x3a3a3e, 'bigote': True})


def turista():
    def extra(p):
        k = p.k
        for x, z, c in ((-0.08, 1.12, 0xffd23f), (0.1, 1.2, 0xff7a3a), (0.02, 1.0, 0xff4f8a), (-0.1, 1.28, 0xff4f8a), (0.08, 1.02, 0xffd23f)):
            elip(M(c, 0.6), x * k, -0.105 * k, z * k, 0.025 * k, esc=(1, 0.4, 1), sub=1)
        caja(M(0x2a2a2e, 0.4), 0, -0.13 * k, 1.18 * k, 0.12 * k, 0.06 * k, 0.08 * k)
        cil(M(0x5a6a7a, 0.2), 0, -0.17 * k, 1.22 * k, 0.03 * k, 0.04 * k, 12, eje='Y')
        rama(M(0x1d1f25, 0.6), (-0.06 * k, -0.11 * k, 1.24 * k), (-0.05 * k, -0.02 * k, 1.42 * k), 0.006, 0.006, 4)
        rama(M(0x1d1f25, 0.6), (0.06 * k, -0.11 * k, 1.24 * k), (0.05 * k, -0.02 * k, 1.42 * k), 0.006, 0.006, 4)
        gorra(M(0xf2e8c8, 0.7), 0, p.cab_z, p.cab_r, visera=M(0x3ab0a0, 0.6))
    return persona(1.74, 1.04, PIELES[3], OJOS[3], 0x3ab0a0, 0xe0c890, 0xf2f2f2, 0x1a1a1a, 'corto',
                   extra, largo=False, corto=True, piernas_piel=True, calcetin=0xffffff, cinturon=0x6a4a2a)


def fan():
    def extra(p):
        k = p.k
        for i in range(3):
            caja(M(0xd8283a, 0.6), 0, -0.108 * k, p.cad_z + (0.16 + i * 0.075) * k, 0.26 * k, 0.012, 0.03 * k)
        gorra(M(0xd8283a, 0.6), 0, p.cab_z, p.cab_r)
    return persona(1.7, 0.98, PIELES[1], OJOS[1], 0x1f3c88, 0x3a5a8a, 0xffffff, 0xd99a3a, 'coleta',
                   extra, largo=False, obj_d='bandera')


def granjero():
    def extra(p):
        k = p.k
        peto = M(0x2f4f7a)
        caja(peto, 0, -0.1 * k, p.cad_z + 0.02 * k, 0.24 * k, 0.03, 0.3 * k)
        for s in (-1, 1):
            caja(peto, s * 0.08 * k, -0.1 * k, p.cad_z + 0.3 * k, 0.04 * k, 0.025, 0.2 * k)
            esfera(M(0xd9a520, 0.3), s * 0.08 * k, -0.115 * k, p.cad_z + 0.3 * k, 0.014 * k, 1)
        gm = M(0x2f6a3a, 0.6)
        gorra(gm, 0, p.cab_z, p.cab_r)
        for s in (-1, 1):
            elip(M(0xd8cbb2, 0.85), s * p.cab_r * 0.95, 0, p.cab_z, p.cab_r * 0.4, esc=(0.45, 0.9, 1.1))
    p, piezas = persona(1.8, 1.14, PIELES[0], OJOS[0], 0xc0302a, 0x2f4f7a, 0x5a3a28, 0x8a6a4a, 'corto',
                        extra, bota=True, cara_kw={'bigote': True})
    return p, piezas


def ejecutiva():
    """Nueva (09/11): mujer de negocios con americana, falda de tubo y café."""
    def extra(p):
        k = p.k
        for s in (-1, 1):
            caja(M(0x7a1f2e, 0.6), s * 0.055 * k, -0.105 * k, p.hom_z - 0.28 * k, 0.035 * k, 0.015, 0.24 * k)
    return persona(1.7, 0.95, PIELES[2], OJOS[0], 0x8a2a3a, 0x000000, 0x1d1a18, 0x2a1a12, 'melena',
                   extra, falda=0x2a2a32, abierto=0xf4efe6, obj_d='cafe', obj_i='bolso')


def obrero():
    """Nuevo: obrero con casco y chaleco reflectante."""
    def extra(p):
        k = p.k
        cha = M(0xff7a1a, 0.5)
        tubo(cha, [(0, 0, p.cad_z + 0.12 * k, 0.168 * k * p.a, 0.115 * k), (0, 0, (p.cad_z + p.hom_z) / 2 + 0.08 * k, 0.188 * k * p.a, 0.124 * k),
                   (0, 0, p.hom_z - 0.1 * k, 0.17 * k * p.a, 0.115 * k)], tapas=False)
        for z in (0.2, 0.32):
            o = cil(M(0xe8e8e0, 0.2), 0, 0, p.cad_z + z * k, 0.2 * k * p.a, 0.025 * k, 20)
            o.scale = (1, 0.7, 1)
        gorra(M(0xf2c230, 0.4), 0, p.cab_z, p.cab_r, casco=True)
    return persona(1.78, 1.12, PIELES[1], OJOS[0], 0x5a7a9a, 0x4a5a6a, 0x6a4a2a, 0x3a2a1e, 'corto',
                   extra, bota=True, cinturon=0x2a2420, cara_kw={'barba': True})


def estudiante():
    """Nuevo: estudiante con sudadera, vaqueros, zapatillas y mochila."""
    def extra(p):
        k = p.k
        mo = M(0x2d8a5a, 0.6)
        tubo(mo, [(0, 0.17 * k, p.cad_z + 0.2 * k, 0.13 * k, 0.07 * k), (0, 0.17 * k, p.hom_z - 0.08 * k, 0.13 * k, 0.07 * k)])
        for s in (-1, 1):
            rama(M(0x1d1f25, 0.6), (s * 0.1 * k, 0.12 * k, p.hom_z - 0.06 * k), (s * 0.11 * k, 0.0, p.hom_z + 0.01 * k), 0.012 * k, 0.012 * k, 5)
        elip(M(0x6a4aa8), 0, 0.09 * k, p.hom_z + 0.03 * k, 0.12 * k, esc=(1.1, 0.8, 0.45))   # capucha caída
    return persona(1.72, 1.0, PIELES[0], OJOS[2], 0x6a4aa8, 0x3a5a9a, 0xf2f2f2, 0xb8742e, 'corto',
                   extra, puno=0x5a3a98, obj_i='telefono')


def deportista():
    """Nueva: corredora con mallas, camiseta de tirantes y cinta en el pelo."""
    def extra(p):
        k = p.k
        o = cil(M(0x2fb8d8, 0.5), 0, 0.01 * k, p.cab_z + p.cab_r * 0.3, p.cab_r * 0.98, p.cab_r * 0.22, 20)
    return persona(1.68, 0.94, PIELES[3], OJOS[3], 0xff5a7a, 0x2a2a3a, 0x2fb8d8, 0x1a1a1a, 'coleta',
                   extra, largo='no', cinturon=0x2fb8d8, cara_kw={'sonrisa': 0.3})


PERSONAS = {'ejecutivo': ejecutivo, 'senora': senora, 'chico': chico, 'abuelo': abuelo, 'turista': turista,
            'fan': fan, 'granjero': granjero, 'ejecutiva': ejecutiva, 'obrero': obrero,
            'estudiante': estudiante, 'deportista': deportista}

def aligerar(partes):
    """Quita triángulos donde no se nota (formas suaves): en la calle hay muchas
    personas a la vez y el móvil tiene que poder con todas."""
    for o in partes:
        if o.type != 'MESH':
            continue
        tris = sum(len(f.vertices) - 2 for f in o.data.polygons)
        if tris <= 220:
            continue
        md = o.modifiers.new('aligerar', 'DECIMATE')
        md.ratio = max(96, tris * 0.17) / tris
        bpy.ops.object.select_all(action='DESELECT')
        o.select_set(True)
        bpy.context.view_layer.objects.active = o
        bpy.ops.object.modifier_apply(modifier='aligerar')


TEXTURA = {'cuerpo': 512, 'brazo_d': 256, 'brazo_i': 256, 'pierna_d': 128, 'pierna_i': 128}
articulaciones = {}
for nombre, fn in PERSONAS.items():
    if SOLO and nombre not in SOLO:
        continue
    empezar()
    bpy.context.scene.world.light_settings.distance = 0.2
    p, piezas = fn()
    hechos = []
    for pieza, hacer in piezas.items():
        comun._partes.clear()
        hacer()
        aligerar(comun._partes)
        o = terminar(f'{nombre}_{pieza}', 'publico', lado=TEXTURA[pieza], bisel=0.0, oclusion=0.45,
                     suelo=False, exportar=False)
        hechos.append(o)
    bpy.ops.object.select_all(action='DESELECT')
    for o in hechos:
        o.hide_render = False
        o.select_set(True)
    salida = os.path.join(MODELOS, 'publico')
    os.makedirs(salida, exist_ok=True)
    bpy.ops.export_scene.gltf(filepath=os.path.join(salida, f'{nombre}.glb'), export_format='GLB',
                              use_selection=True, export_image_format='JPEG', export_apply=True,
                              export_animations=False, export_yup=True)
    # En el juego: x igual, y = z de Blender.
    articulaciones[nombre] = [round(p.hom_x, 3), round(p.hom_z, 3), round(p.cad_x, 3), round(p.cad_z, 3)]
    print(f'PERSONA {nombre} hecha', flush=True)
print('ARTICULACIONES ' + json.dumps(articulaciones), flush=True)
