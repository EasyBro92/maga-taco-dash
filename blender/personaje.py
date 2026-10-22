# El protagonista en dibujo animado estilo Gru / Minions (22/10/2026).
#
#   blender -b -P blender/personaje.py -- [--rapido]
#
# Un presidente de dibujos con un ligero aire a Donald Trump (solo un poco, lo
# pidió así Isidro): torso de tonel con chaqueta, piernas finas, zapatos negros
# en punta, manos pequeñas, mandíbula ancha, piel bronceada con la marca blanca
# de las gafas, tupé rubio y corbata larga.
#
# Sale UN archivo (www/models/personaje/personaje.glb) con una malla por parte.
# Cada una está modelada con su punto de giro en el origen, el mismo que usa el
# esqueleto de character.js, para que el juego la cuelgue tal cual y no se
# pierda ninguna animación:
#   torso_traje, torso_resto   cadera (hips)
#   corbata                    nudo de la corbata, colgando de hips
#   cabeza, tupe               headGroup (en medidas reales: el juego deshace
#                              la escala 0.78 de ese grupo)
#   brazo_traje                hombro
#   antebrazo_traje, mano      codo
#   muslo_traje                cadera de la pierna
#   espinilla_traje, zapato    rodilla
# Lo que lleva "traje" o "corbata" en el nombre se hornea en blanco (solo la
# sombra) y el juego le pone el color de la tienda.
#
# Ejes de Blender: z arriba, el personaje mira a -y (en el juego, +z).

import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import *
from comun import _poner

PIEL = 0xffbe86          # bronceado naranja claro (0xf3a46a salia marron en el juego)
PALIDO = 0xfff0dc
RUBIO1, RUBIO2 = 0xf8d77f, 0xecbf62

def traje():  return mat('traje', 0xffffff, 0.6)
def piel():   return mat('piel', PIEL, 0.55)
def blanco(): return mat('camisa', 0xffffff, 0.5)
def solapa(): return mat('solapa', 0x1c2541, 0.5)
def pelo():   return mat_franjas('pelo', RUBIO1, RUBIO2, 18, eje='Y', z0=-0.45, alto=0.9)


# ---------------------------------------------------------------- utilidades
def _objeto(nombre, bm, m):
    me = bpy.data.meshes.new(nombre)
    bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(nombre, me)
    bpy.context.scene.collection.objects.link(o)
    return _poner(o, m)

def torno(m, perfil, lados=28, prof=0.8):
    """Sólido de revolución (elíptico: `prof` aplasta el fondo) a partir de
    [(z, radio), ...] de abajo arriba, con tapas."""
    bm = bmesh.new()
    aros = []
    for z, r in perfil:
        aros.append([bm.verts.new((r * math.cos(a), prof * r * math.sin(a), z))
                     for a in (i / lados * math.tau for i in range(lados))])
    for a, b in zip(aros, aros[1:]):
        for i in range(lados):
            j = (i + 1) % lados
            bm.faces.new((a[i], a[j], b[j], b[i]))
    bm.faces.new(aros[0][::-1]); bm.faces.new(aros[-1])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return _objeto('torno', bm, m)

def lamina(m, filas, grosor=0.012):
    """Lámina con grosor a partir de filas de puntos (todas del mismo largo):
    sirve para camisa, solapas y corbata pegadas a la curva del pecho."""
    bm = bmesh.new()
    vs = [[bm.verts.new(p) for p in fila] for fila in filas]
    for a, b in zip(vs, vs[1:]):
        for i in range(len(a) - 1):
            bm.faces.new((a[i], a[i + 1], b[i + 1], b[i]))
    o = _objeto('lamina', bm, m)
    md = o.modifiers.new('grosor', 'SOLIDIFY')
    md.thickness = grosor
    md.offset = 0
    bpy.context.view_layer.objects.active = o
    bpy.ops.object.modifier_apply(modifier='grosor')
    return o

def elip(m, x, y, z, r, esc=(1, 1, 1), rot=(0, 0, 0), sub=3):
    o = esfera(m, x, y, z, r, sub, esc=esc)
    o.rotation_euler = rot
    return o

def esfera_uv(m, x, y, z, r, seg=32, aros=18, esc=(1, 1, 1)):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg, ring_count=aros, radius=r, location=(x, y, z))
    o = bpy.context.object
    o.scale = esc
    return _poner(o, m)


# ---------------------------------------------------------------- torso
# Perfil del tonel (z sobre la cadera, radio en x). El fondo es 0.8 del ancho.
PERFIL = [(-0.03, 0.29), (0.05, 0.275), (0.14, 0.29), (0.24, 0.32), (0.34, 0.345), (0.44, 0.35),
          (0.52, 0.335), (0.58, 0.295), (0.62, 0.215), (0.648, 0.12)]
PROF = 0.8

def radio(z):
    for (z0, r0), (z1, r1) in zip(PERFIL, PERFIL[1:]):
        if z0 <= z <= z1:
            return r0 + (r1 - r0) * (z - z0) / (z1 - z0)
    return PERFIL[0][1] if z < PERFIL[0][0] else PERFIL[-1][1]

def frente(x, z, sale=0.0):
    """y de la superficie delantera del pecho en (x, z), más `sale` hacia fuera."""
    r = radio(z)
    return -PROF * math.sqrt(max(r * r - x * x, 0.0)) - sale

def torso_traje():
    torno(traje(), PERFIL, lados=32, prof=PROF)
    for s in (-1, 1):
        elip(traje(), s * 0.27, 0, 0.53, 0.14, esc=(1.15, 0.85, 0.9))     # hombreras

def torso_resto():
    # camisa en V, siguiendo la curva del pecho
    filas = []
    for k in range(8):
        z = 0.63 - k * (0.33 / 7)
        w = 0.115 * (z - 0.30) / 0.33
        filas.append([(x, frente(x, z, 0.004), z) for x in (-w, -w / 2, 0, w / 2, w)])
    lamina(blanco(), filas, 0.012)
    # solapas a los lados de la V
    for s in (-1, 1):
        filas = []
        for k in range(8):
            z = 0.63 - k * (0.37 / 7)
            w = max(0.0, 0.115 * (z - 0.30) / 0.33)
            xs = [s * w, s * (w + 0.04), s * (w + 0.08)]
            filas.append([(x, frente(x, z, 0.008), z) for x in (xs if s < 0 else xs)])
        lamina(solapa(), filas, 0.014)
    cil(blanco(), 0, 0, 0.6, 0.135, 0.07, 16)                            # cuello de la camisa
    cil(piel(), 0, 0, 0.6, 0.105, 0.16, 14)                             # cuello
    for z in (0.24, 0.15):                                              # botones
        esfera(mat('boton', 0x16182a, 0.4), 0, frente(0, z, 0.0), z, 0.022, 1)
    # insignia de la bandera en la solapa
    caja(mat('pin_rojo', 0xd8322f, 0.4), -0.17, frente(-0.17, 0.5, 0.02), 0.49, 0.045, 0.012, 0.03)
    caja(mat('pin_azul', 0x2a4a9a, 0.4), -0.185, frente(-0.185, 0.5, 0.026), 0.495, 0.018, 0.012, 0.02)
    # costura y abertura de la espalda (lo que más se ve: la cámara va detrás)
    for z0, h in ((0.12, 0.42),):
        filas = [[(x, -frente(x, z, 0.004), z) for x in (-0.012, 0.012)] for z in
                 [z0 + h * k / 6 for k in range(7)]]
        lamina(solapa(), filas, 0.008)

def corbata():
    """La corbata cuelga del nudo (origen) hasta la cintura, pegada a la tripa."""
    ky = frente(0, 0.56, 0.02)
    filas = []
    n = 10
    for k in range(n + 1):
        z = 0.56 - k * (0.56 / n)
        w = 0.035 + 0.035 * k / n
        filas.append([(x, frente(0, z, 0.026) - ky, z - 0.56) for x in (-w, 0, w)])
    filas.append([(x, frente(0, 0, 0.026) - ky, -0.62) for x in (-0.004, 0, 0.004)])   # la punta
    lamina(traje(), filas, 0.016)
    elip(traje(), 0, -0.005, 0.005, 0.045, esc=(1.0, 0.7, 0.9), sub=2)  # nudo


# ---------------------------------------------------------------- cabeza
def cabeza():
    o = esfera_uv(piel(), 0, 0, 0, 0.36, 36, 22)
    # Cara de pera: la mandíbula se ensancha y se adelanta hacia abajo.
    for v in o.data.vertices:
        x, y, z = v.co
        t = max(0.0, -z / 0.36)
        v.co = (x * 1.05 * (1 + 0.3 * t), y * 0.98 * (1 + 0.16 * t), z * 0.98)
    for s in (-1, 1):
        elip(piel(), s * 0.4, 0.0, -0.02, 0.07, esc=(0.5, 0.9, 1.15), sub=2)   # orejas
    elip(piel(), 0, -0.352, -0.045, 0.066, esc=(0.95, 1.0, 1.15), sub=2)       # nariz
    elip(piel(), 0, -0.33, 0.02, 0.04, esc=(0.8, 1.0, 1.6), sub=2)             # tabique
    # la marca blanca de las gafas de sol alrededor de los ojos
    for s in (-1, 1):
        x, z = s * 0.133, 0.027
        r2 = 0.36 * 0.36 - (x / 1.05) ** 2 - (z / 0.98) ** 2
        y = -0.98 * math.sqrt(max(r2, 0)) + 0.012
        elip(mat('palido', PALIDO, 0.55), x, y, z, 0.105, esc=(1.0, 0.3, 0.82), sub=3)
    # el casco de pelo: arriba, detrás y a los lados, despejando la frente
    o = esfera_uv(pelo(), 0, 0.025, 0.005, 0.378, 36, 22, esc=(1.08, 1.03, 1.0))
    bm = bmesh.new(); bm.from_mesh(o.data)
    fuera = []
    for v in bm.verts:
        x, y, z = v.co
        delante = -y / 0.378                  # 1 en la cara, -1 en la nuca
        limite = 0.1 * max(0.0, delante) ** 0.6 - 0.18 * max(0.0, -delante) - 0.02
        if abs(x) > 0.3 and delante > -0.2:
            limite = max(limite, 0.02)        # patillas cortas, deja ver la oreja
        if z < limite:
            fuera.append(v)
    bmesh.ops.delete(bm, geom=fuera, context='VERTS')
    bm.to_mesh(o.data); bm.free()

def tupe():
    """El tupé, aparte para que el juego lo haga ondear al correr."""
    p = pelo()
    elip(p, -0.03, -0.1, 0.3, 0.21, esc=(1.85, 1.3, 0.55), rot=(0.15, 0, 0.18))
    elip(p, -0.11, -0.27, 0.27, 0.14, esc=(1.65, 1.0, 0.55), rot=(0.35, 0, 0.3))
    elip(p, 0.19, -0.06, 0.33, 0.12, esc=(1.4, 1.15, 0.5), rot=(0.1, 0, -0.35))
    elip(p, -0.26, -0.2, 0.2, 0.08, esc=(1.2, 1.0, 0.6), rot=(0.4, 0, 0.6))   # la punta que cae


# ---------------------------------------------------------------- brazos y piernas
def brazo_traje():
    esfera(traje(), 0, 0, 0, 0.095, 3)
    cil(traje(), 0, 0, -0.29, 0.075, 0.29, 16, r2=0.093)

def antebrazo_traje():
    esfera(traje(), 0, 0, 0, 0.077, 3)
    cil(traje(), 0, 0, -0.205, 0.064, 0.205, 16, r2=0.076)

def mano():
    cil(blanco(), 0, 0, -0.235, 0.068, 0.04, 16)                        # puño de la camisa
    cil(piel(), 0, 0, -0.27, 0.042, 0.04, 12)
    elip(piel(), 0, 0, -0.3, 0.06, esc=(1.0, 0.75, 1.1), sub=2)          # manos pequeñas
    for x in (-0.028, 0, 0.028):
        elip(piel(), x, -0.008, -0.36, 0.022, esc=(1, 1, 1.7), sub=2)
    elip(piel(), 0, -0.05, -0.29, 0.022, esc=(1, 1.2, 1.4), rot=(0.5, 0, 0), sub=2)

def muslo_traje():
    esfera(traje(), 0, 0, 0, 0.12, 3, esc=(1, 0.95, 0.95))
    cil(traje(), 0, 0, -0.36, 0.078, 0.36, 16, r2=0.1)

def espinilla_traje():
    esfera(traje(), 0, 0, 0, 0.08, 3)
    cil(traje(), 0, 0, -0.33, 0.068, 0.33, 16, r2=0.078)

def zapato():
    negro = mat('zapato', 0x1b1c22, 0.25)
    cil(mat('calcetin', 0x2a2a33, 0.6), 0, 0, -0.37, 0.067, 0.05, 14)
    elip(negro, 0, -0.05, -0.415, 0.1, esc=(0.85, 1.75, 0.58))
    elip(negro, 0, -0.21, -0.43, 0.065, esc=(0.95, 1.6, 0.6))            # la punta
    caja(mat('suela', 0x4a3324, 0.8), 0, -0.08, -0.47, 0.17, 0.44, 0.03)


PARTES = [
    ('torso_traje', torso_traje, 512),
    ('torso_resto', torso_resto, 512),
    ('corbata', corbata, 256),
    ('cabeza', cabeza, 1024),
    ('tupe', tupe, 512),
    ('brazo_traje', brazo_traje, 256),
    ('antebrazo_traje', antebrazo_traje, 256),
    ('mano', mano, 256),
    ('muslo_traje', muslo_traje, 256),
    ('espinilla_traje', espinilla_traje, 256),
    ('zapato', zapato, 256),
]

empezar()
bpy.context.scene.world.light_settings.distance = 0.3   # sombra de rincón corta: es pequeño
hechas = []
for nombre, fn, lado in PARTES:
    fn()
    hechas.append(terminar(nombre, 'personaje', lado=lado, bisel=0.01, oclusion=0.55,
                           suelo=False, exportar=False))
for o in hechas:
    o.hide_render = False
bpy.ops.object.select_all(action='DESELECT')
for o in hechas:
    o.select_set(True)
salida = os.path.join(MODELOS, 'personaje')
os.makedirs(salida, exist_ok=True)
bpy.ops.export_scene.gltf(filepath=os.path.join(salida, 'personaje.glb'), export_format='GLB',
                          use_selection=True, export_image_format='JPEG', export_apply=True,
                          export_animations=False, export_yup=True)
print('PERSONAJE exportado:', len(hechas), 'partes', flush=True)
