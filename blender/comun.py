# Lo común de las piezas de MAGA Taco Dash hechas en Blender (20/10/2026).
#
# Estilo: dibujo animado (colores lisos, formas gordas, cantos redondeados).
# Cada pieza (un edificio, un árbol, una farola) se modela por separado y sale
# como UN objeto con UNA textura: los colores, los ladrillos y la sombra de los
# rincones (oclusión) se hornean juntos en ella. Así en el juego cada pieza es
# una sola llamada de dibujo y la ilumina la luz del propio juego.
#
# Ejes de Blender, pensados para la calle del juego:
#   x  a lo largo de la calle (el ancho de la fachada)
#   y  hacia dentro: la fachada está en y = 0 y mira a -y (a la calzada)
#   z  arriba, el suelo en z = 0
# Al exportar, -y de Blender pasa a ser +z del juego: por eso las piezas llevan
# `frontZ` en el juego.
#
#   blender -b -P dc.py -- [pieza ...] [--rapido]

import bpy, bmesh, math, os, sys, time
import numpy as np

ARGS = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
RAPIDO = '--rapido' in ARGS
SOLO = [a for a in ARGS if not a.startswith('--')]
AQUI = os.path.dirname(os.path.abspath(__file__))
MODELOS = os.path.join(AQUI, '..', 'www', 'models')
TMP = os.path.join(AQUI, '_tmp')
os.makedirs(TMP, exist_ok=True)


def lin(h):
    c = [((h >> s) & 255) / 255 for s in (16, 8, 0)]
    return tuple(v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in c)


# ---------------------------------------------------------------- materiales
_mats = {}

def _principled(m):
    return m.node_tree.nodes['Principled BSDF']

def mat(nombre, color, rug=0.6):
    """Color liso."""
    if nombre in _mats:
        return _mats[nombre]
    m = bpy.data.materials.new(nombre)
    m.use_nodes = True
    b = _principled(m)
    b.inputs['Base Color'].default_value = (*lin(color), 1)
    b.inputs['Roughness'].default_value = rug
    _mats[nombre] = m
    return m

def mat_bloques(nombre, color, junta, ancho=0.9, alto=0.35, grosor=0.012, mezcla=1.0, desfase=0.5, variacion=1.08):
    """Ladrillo o sillería: la textura de ladrillo de Blender proyectada en las
    paredes (u = x + y, v = z, vale para paredes que miren a x o a y).
    Con la junta gruesa y desfase 0 sirve para pintar ventanas: `color` es el
    cristal y `junta` la pared (ver `mat_ventanas`)."""
    if nombre in _mats:
        return _mats[nombre]
    m = bpy.data.materials.new(nombre)
    m.use_nodes = True
    nt = m.node_tree
    b = _principled(m)
    b.inputs['Roughness'].default_value = 0.7
    tc = nt.nodes.new('ShaderNodeTexCoord')
    sep = nt.nodes.new('ShaderNodeSeparateXYZ')
    suma = nt.nodes.new('ShaderNodeMath'); suma.operation = 'ADD'
    comb = nt.nodes.new('ShaderNodeCombineXYZ')
    nt.links.new(tc.outputs['Object'], sep.inputs[0])
    nt.links.new(sep.outputs['X'], suma.inputs[0])
    nt.links.new(sep.outputs['Y'], suma.inputs[1])
    nt.links.new(suma.outputs[0], comb.inputs['X'])
    nt.links.new(sep.outputs['Z'], comb.inputs['Y'])
    br = nt.nodes.new('ShaderNodeTexBrick')
    br.inputs['Scale'].default_value = 1.0
    br.inputs['Brick Width'].default_value = ancho
    br.inputs['Row Height'].default_value = alto
    br.inputs['Mortar Size'].default_value = grosor
    br.inputs['Mortar Smooth'].default_value = 0.2
    c1 = lin(color)
    c2 = tuple(min(1, v * variacion) for v in c1)
    br.inputs['Color1'].default_value = (*c1, 1)
    br.inputs['Color2'].default_value = (*c2, 1)
    br.inputs['Mortar'].default_value = (*lin(junta), 1)
    br.offset = desfase
    nt.links.new(comb.outputs[0], br.inputs['Vector'])
    if mezcla < 1.0:
        mx = nt.nodes.new('ShaderNodeMix'); mx.data_type = 'RGBA'
        mx.inputs['Factor'].default_value = mezcla
        mx.inputs['A'].default_value = (*c1, 1)
        nt.links.new(br.outputs['Color'], mx.inputs['B'])
        nt.links.new(mx.outputs['Result'], b.inputs['Base Color'])
    else:
        nt.links.new(br.outputs['Color'], b.inputs['Base Color'])
    _mats[nombre] = m
    return m

def mat_ventanas(nombre, cristal, pared, paso_x=0.9, paso_z=1.1, hueco_x=0.5, hueco_z=0.6, variacion=1.35):
    """Fachada entera de ventanas pintadas: rejilla de huecos `hueco_x` x
    `hueco_z` cada `paso_x` x `paso_z`. Unas ventanas salen más claras que
    otras (luz encendida)."""
    grosor = min(paso_x - hueco_x, paso_z - hueco_z) / 2
    return mat_bloques(nombre, cristal, pared, ancho=paso_x, alto=paso_z, grosor=grosor,
                       desfase=0.0, variacion=variacion)

# ---- Luces (29/10/2026, Las Vegas al anochecer) ----
# Lo que brilla solo (neones, bombillas, ventanas encendidas) se hornea además
# en una segunda textura, la de luz: en el juego va de `emissiveMap` y se ve
# encendido aunque la escena esté oscura. Fija: nada parpadea (Isidro se marea).
_luces = set()

def luz(nombre, color, fuerza=1.0):
    """Color liso que brilla solo (neón, bombilla)."""
    if nombre in _mats:
        return _mats[nombre]
    m = mat(nombre, color, 0.2)
    b = _principled(m)
    b.inputs['Emission Color'].default_value = (*lin(color), 1)
    b.inputs['Emission Strength'].default_value = fuerza
    _luces.add(nombre)
    return m

def ventanas_luz(nombre, cristal, pared, brillo=0.6, **kw):
    """Como `mat_ventanas`, pero los cristales están encendidos (las paredes no)."""
    if nombre in _mats:
        return _mats[nombre]
    m = mat_ventanas(nombre, cristal, pared, **kw)
    nt = m.node_tree
    br = next(n for n in nt.nodes if n.type == 'TEX_BRICK')
    b = _principled(m)
    inv = nt.nodes.new('ShaderNodeMath'); inv.operation = 'SUBTRACT'
    inv.inputs[0].default_value = 1.0
    nt.links.new(br.outputs['Fac'], inv.inputs[1])            # Fac = 1 en la junta (la pared)
    k = nt.nodes.new('ShaderNodeMath'); k.operation = 'MULTIPLY'
    k.inputs[1].default_value = brillo
    nt.links.new(inv.outputs[0], k.inputs[0])
    nt.links.new(br.outputs['Color'], b.inputs['Emission Color'])
    nt.links.new(k.outputs[0], b.inputs['Emission Strength'])
    _luces.add(nombre)
    return m

def mat_franjas(nombre, c1, c2, n, eje='Z', z0=0.0, alto=1.0):
    """Franjas (la bandera): n franjas a lo largo de `eje` entre z0 y z0+alto."""
    if nombre in _mats:
        return _mats[nombre]
    m = bpy.data.materials.new(nombre)
    m.use_nodes = True
    nt = m.node_tree
    b = _principled(m)
    tc = nt.nodes.new('ShaderNodeTexCoord')
    sep = nt.nodes.new('ShaderNodeSeparateXYZ')
    nt.links.new(tc.outputs['Object'], sep.inputs[0])
    a = nt.nodes.new('ShaderNodeMath'); a.operation = 'SUBTRACT'
    a.inputs[1].default_value = z0
    nt.links.new(sep.outputs[eje], a.inputs[0])
    k = nt.nodes.new('ShaderNodeMath'); k.operation = 'MULTIPLY'
    k.inputs[1].default_value = n / alto
    nt.links.new(a.outputs[0], k.inputs[0])
    md = nt.nodes.new('ShaderNodeMath'); md.operation = 'PINGPONG'
    md.inputs[1].default_value = 1.0
    nt.links.new(k.outputs[0], md.inputs[0])
    st = nt.nodes.new('ShaderNodeMath'); st.operation = 'GREATER_THAN'
    st.inputs[1].default_value = 0.5
    # pingpong(t, 1) sube y baja: >0.5 una franja sí y otra no
    fr = nt.nodes.new('ShaderNodeMath'); fr.operation = 'FRACT'
    h = nt.nodes.new('ShaderNodeMath'); h.operation = 'MULTIPLY'; h.inputs[1].default_value = 0.5
    nt.links.new(k.outputs[0], h.inputs[0])
    nt.links.new(h.outputs[0], fr.inputs[0])
    nt.links.new(fr.outputs[0], st.inputs[0])
    mx = nt.nodes.new('ShaderNodeMix'); mx.data_type = 'RGBA'
    mx.inputs['A'].default_value = (*lin(c1), 1)
    mx.inputs['B'].default_value = (*lin(c2), 1)
    nt.links.new(st.outputs[0], mx.inputs['Factor'])
    nt.links.new(mx.outputs['Result'], b.inputs['Base Color'])
    _mats[nombre] = m
    return m


# ---------------------------------------------------------------- geometría
_partes = []

def _poner(o, m):
    o.data.materials.clear()
    o.data.materials.append(m)
    _partes.append(o)
    return o

def caja(m, x, y, z, w, d, h, giro=0.0, inclina=0.0):
    """Caja con la base en z; (x, y) es su centro en planta."""
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, z + h / 2))
    o = bpy.context.object
    o.scale = (w, d, h)
    o.rotation_euler = (inclina, 0, giro)
    return _poner(o, m)

def cil(m, x, y, z, r, h, lados=12, r2=None, eje='Z'):
    """Cilindro (o tronco de cono con r2) con la base en z."""
    bpy.ops.mesh.primitive_cone_add(vertices=lados, radius1=r, radius2=r if r2 is None else r2,
                                    depth=h, location=(x, y, z + h / 2))
    o = bpy.context.object
    if eje == 'Y':
        o.rotation_euler = (math.pi / 2, 0, 0)
        o.location = (x, y, z)
    elif eje == 'X':
        o.rotation_euler = (0, math.pi / 2, 0)
        o.location = (x, y, z)
    return _poner(o, m)

def esfera(m, x, y, z, r, sub=2, esc=(1, 1, 1), mitad=False):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=sub, radius=r, location=(x, y, z))
    o = bpy.context.object
    o.scale = esc
    if mitad:
        bm = bmesh.new(); bm.from_mesh(o.data)
        bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.co.z < -1e-4], context='VERTS')
        bm.to_mesh(o.data); bm.free()
    return _poner(o, m)

def cupula(m, x, y, z, r, alto, lados=24, aros=8):
    """Media esfera de UV (meridianos limpios), base en z y alto `alto`."""
    bpy.ops.mesh.primitive_uv_sphere_add(segments=lados, ring_count=aros * 2, radius=r, location=(x, y, z))
    o = bpy.context.object
    bm = bmesh.new(); bm.from_mesh(o.data)
    bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.co.z < -1e-4], context='VERTS')
    bm.to_mesh(o.data); bm.free()
    o.scale = (1, 1, alto / r)
    return _poner(o, m)

def fronton(m, x, y, z, w, h, d):
    """Frontón triangular: base de ancho w en z, punta h más arriba, fondo d hacia +y."""
    me = bpy.data.meshes.new('fronton')
    bm = bmesh.new()
    vs = []
    for yy in (y, y + d):
        vs.append([bm.verts.new((x - w / 2, yy, z)), bm.verts.new((x + w / 2, yy, z)),
                   bm.verts.new((x, yy, z + h))])
    a, b = vs
    bm.faces.new(a[::-1]); bm.faces.new(b)
    for i in range(3):
        j = (i + 1) % 3
        bm.faces.new((a[i], a[j], b[j], b[i]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new('fronton', me)
    bpy.context.scene.collection.objects.link(o)
    return _poner(o, m)

def columnata(m, x0, x1, n, y, z, r, h, basa=None, capitel=None):
    """n columnas entre x0 y x1, con basa y capitel de caja."""
    for i in range(n):
        x = x0 + (x1 - x0) * (i / (n - 1) if n > 1 else 0.5)
        cil(m, x, y, z + r * 0.6, r, h - r * 1.2, lados=12, r2=r * 0.86)
        caja(basa or m, x, y, z, r * 2.6, r * 2.6, r * 0.6)
        caja(capitel or m, x, y, z + h - r * 0.6, r * 2.8, r * 2.8, r * 0.6)

def panel(m, a, b, c, d, grosor=0.1):
    """Losa de grosor `grosor` sobre el cuadrilátero a-b-c-d (faldones de tejado)."""
    me = bpy.data.meshes.new('panel')
    bm = bmesh.new()
    bm.faces.new([bm.verts.new(p) for p in (a, b, c, d)])
    bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new('panel', me)
    bpy.context.scene.collection.objects.link(o)
    md = o.modifiers.new('grosor', 'SOLIDIFY')
    md.thickness = grosor
    md.offset = 0
    bpy.context.view_layer.objects.active = o
    bpy.ops.object.modifier_apply(modifier='grosor')
    return _poner(o, m)

def tejado(m, x, y0, y1, z, w, h, vuelo=0.3, grosor=0.12, cumbrera='y'):
    """Tejado a dos aguas sobre un cuerpo de ancho w (en x) entre y0 e y1, alero
    en z y cumbrera h más arriba. cumbrera='y': el hastial mira a la calle;
    'x': los faldones miran a la calle."""
    if cumbrera == 'y':
        ya, yb = y0 - vuelo, y1 + vuelo
        k = h / (w / 2)
        xi, zi = x - w / 2 - vuelo, z - vuelo * k
        xd = x + w / 2 + vuelo
        panel(m, (xi, ya, zi), (x, ya, z + h), (x, yb, z + h), (xi, yb, zi), grosor)
        panel(m, (x, ya, z + h), (xd, ya, zi), (xd, yb, zi), (x, yb, z + h), grosor)
    else:
        xa, xb = x - w / 2 - vuelo, x + w / 2 + vuelo
        ym = (y0 + y1) / 2
        k = h / ((y1 - y0) / 2)
        panel(m, (xa, y0 - vuelo, z - vuelo * k), (xb, y0 - vuelo, z - vuelo * k), (xb, ym, z + h), (xa, ym, z + h), grosor)
        panel(m, (xa, ym, z + h), (xb, ym, z + h), (xb, y1 + vuelo, z - vuelo * k), (xa, y1 + vuelo, z - vuelo * k), grosor)

def hastial(m, x, y0, y1, z, w, h, cumbrera='y'):
    """El triángulo de pared bajo un tejado a dos aguas (relleno macizo)."""
    if cumbrera == 'y':
        return fronton(m, x, y0, z, w, h, y1 - y0)
    me = bpy.data.meshes.new('hastial')
    bm = bmesh.new()
    ym = (y0 + y1) / 2
    lados = []
    for xx in (x - w / 2, x + w / 2):
        lados.append([bm.verts.new((xx, y0, z)), bm.verts.new((xx, y1, z)), bm.verts.new((xx, ym, z + h))])
    a, b = lados
    bm.faces.new(a); bm.faces.new(b[::-1])
    for i in range(3):
        j = (i + 1) % 3
        bm.faces.new((a[j], a[i], b[i], b[j]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new('hastial', me)
    bpy.context.scene.collection.objects.link(o)
    return _poner(o, m)

def rama(m, p0, p1, r0, r1, lados=8):
    """Cilindro de p0 a p1 (ramas, barandillas en diagonal, brazos de farola)."""
    from mathutils import Vector
    p0, p1 = Vector(p0), Vector(p1)
    d = p1 - p0
    bpy.ops.mesh.primitive_cone_add(vertices=lados, radius1=r0, radius2=r1, depth=d.length,
                                    location=(p0 + p1) / 2)
    o = bpy.context.object
    o.rotation_mode = 'QUATERNION'
    o.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(d.normalized())
    return _poner(o, m)

def texto(m, cadena, x, y, z, tam=0.5, prof=0.04):
    """Letras en relieve sobre una fachada que mira a -y; (x, z) es el centro."""
    bpy.ops.object.text_add(location=(0, 0, 0))
    o = bpy.context.object
    o.data.body = cadena
    o.data.size = tam
    o.data.extrude = prof / 2
    o.data.align_x = 'CENTER'
    o.data.align_y = 'CENTER'
    o.data.resolution_u = 3
    bpy.ops.object.convert(target='MESH')
    o = bpy.context.object
    o.rotation_euler = (math.pi / 2, 0, 0)
    o.location = (x, y - prof / 2, z)
    return _poner(o, m)

def ventana(x, z, w, h, y=0.0, marco=None, cristal=None, remate=None, persiana=None):
    """Ventana en una fachada que mira a -y: marco que sale un poco, cristal
    hundido, alféizar y, si se pide, remate encima ('fronton' o 'cornisa')."""
    marco = marco or mat('marco', 0xffffff)
    cristal = cristal or mat('cristal', 0x2d4f86, 0.25)
    caja(marco, x, y - 0.03, z, w + 0.12, 0.08, h + 0.12)
    caja(cristal, x, y - 0.075, z + 0.06, w - 0.04, 0.02, h - 0.04)
    caja(marco, x, y - 0.09, z + 0.06 + (h - 0.04) * 0.55, w - 0.04, 0.02, 0.04)   # travesaño
    caja(marco, x, y - 0.09, z + 0.06, 0.04, 0.02, h - 0.04)                       # parteluz
    caja(marco, x, y - 0.09, z - 0.04, w + 0.24, 0.14, 0.07)                       # alféizar
    if remate == 'fronton':
        fronton(marco, x, y - 0.12, z + h + 0.1, w + 0.35, 0.22, 0.12)
    elif remate == 'cornisa':
        caja(marco, x, y - 0.06, z + h + 0.1, w + 0.3, 0.14, 0.08)
    if persiana:
        for s in (-1, 1):
            caja(persiana, x + s * (w / 2 + 0.16), y - 0.05, z, 0.2, 0.04, h)

def puerta(x, z, w, h, y=0.0, color=0x3a2a1e, marco=None):
    marco = marco or mat('marco', 0xffffff)
    caja(marco, x, y - 0.03, z, w + 0.16, 0.08, h + 0.08)
    caja(mat(f'puerta{color:06x}', color), x, y - 0.06, z, w, 0.04, h)
    caja(marco, x, y - 0.06, z + h + 0.08, w + 0.4, 0.12, 0.1)

def escalinata(m, x, y, z, w, n, huella=0.22, tabica=0.12, crece=0.0):
    """Escalones que bajan hacia -y desde (x, y, z+n*tabica)."""
    for i in range(n):
        caja(m, x, y - (n - i) * huella / 2, z,
             w + crece * (n - i), huella * (n - i), tabica * (i + 1))


# ---------------------------------------------------------------- horneado
def empezar():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    _mats.clear(); _partes.clear(); _luces.clear()
    sc = bpy.context.scene
    sc.render.engine = 'CYCLES'
    sc.cycles.device = 'CPU'
    sc.cycles.samples = 8 if RAPIDO else 40
    sc.view_settings.view_transform = 'Standard'
    w = bpy.data.worlds.new('mundo')
    w.use_nodes = True
    w.node_tree.nodes['Background'].inputs['Color'].default_value = (1, 1, 1, 1)
    w.light_settings.distance = 1.2
    sc.world = w
    return sc

def _imagen(nombre, lado, datos=False):
    im = bpy.data.images.new(nombre, lado, lado, alpha=False)
    if datos:
        im.colorspace_settings.name = 'Non-Color'
    return im

def _apuntar(materiales, im):
    for m in materiales:
        nt = m.node_tree
        n = nt.nodes.get('_hornear') or nt.nodes.new('ShaderNodeTexImage')
        n.name = '_hornear'
        n.image = im
        nt.nodes.active = n

def terminar(nombre, carpeta, lado=512, bisel=0.025, oclusion=0.7, suelo=True, exportar=True, segmentos=1, min_bisel=0.2):
    """Une las partes, redondea los cantos, hornea color + oclusión en una textura
    y exporta `nombre`.glb a www/models/<carpeta>/."""
    t0 = time.time()
    lado = min(lado, 256) if RAPIDO else lado
    bpy.ops.object.select_all(action='DESELECT')
    for o in _partes:
        o.select_set(True)
    bpy.context.view_layer.objects.active = _partes[0]
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    # Cantos redondeados solo en lo grande: en lo pequeño (marcos, barrotes,
    # balaustres) no se ve y multiplica los triángulos por cuatro.
    if bisel > 0:
        for o in _partes:
            if min(o.dimensions) >= min_bisel and len(o.data.polygons) <= 64:
                md = o.modifiers.new('bisel', 'BEVEL')
                md.width = bisel
                md.segments = segmentos
                md.limit_method = 'ANGLE'
                md.angle_limit = math.radians(35)
                bpy.context.view_layer.objects.active = o
                bpy.ops.object.modifier_apply(modifier='bisel')
    bpy.context.view_layer.objects.active = _partes[0]
    bpy.ops.object.join()
    ob = bpy.context.object
    ob.name = nombre
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    bpy.ops.object.shade_smooth_by_angle(angle=math.radians(38))

    # Un solo juego de UV, desplegado para el horneado
    while ob.data.uv_layers:
        ob.data.uv_layers.remove(ob.data.uv_layers[0])
    ob.data.uv_layers.new(name='UVMap')
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project(angle_limit=math.radians(60), island_margin=0.004, scale_to_bounds=True)
    bpy.ops.object.mode_set(mode='OBJECT')

    # Suelo para que la base se oscurezca donde toca el terreno (no se exporta)
    if suelo:
        bpy.ops.mesh.primitive_plane_add(size=200, location=(0, 0, -0.001))
        piso = bpy.context.object
        piso.data.materials.append(mat('_suelo', 0x808080))
    bpy.ops.object.select_all(action='DESELECT')
    ob.select_set(True)
    bpy.context.view_layer.objects.active = ob

    materiales = [s.material for s in ob.material_slots if s.material]
    sc = bpy.context.scene
    sc.render.bake.margin = 6

    color = _imagen(nombre + '_color', lado)
    _apuntar(materiales, color)
    bpy.ops.object.bake(type='DIFFUSE', pass_filter={'COLOR'}, use_clear=True)
    ao = _imagen(nombre + '_ao', lado, datos=True)
    _apuntar(materiales, ao)
    bpy.ops.object.bake(type='AO', use_clear=True)

    c = np.array(color.pixels[:], np.float32).reshape(lado, lado, 4)[..., :3]
    a = np.array(ao.pixels[:], np.float32).reshape(lado, lado, 4)[..., :1]
    # La oclusión oscurece sin llegar a negro: dibujo animado, no foto.
    f = (1 - oclusion) + oclusion * np.power(a, 0.8)
    out = np.ones((lado, lado, 4), np.float32)
    out[..., :3] = np.clip(c * f, 0, 1)
    fin = bpy.data.images.new(nombre, lado, lado, alpha=False)
    fin.pixels.foreach_set(out.ravel())
    ruta = os.path.join(TMP, nombre + '.png')
    fin.filepath_raw = ruta
    fin.file_format = 'PNG'
    fin.save()

    # Luces (29/10): lo que brilla solo, en otra textura (negra donde no hay luz).
    brilla = None
    if any(m.name in _luces for m in materiales):
        em = _imagen(nombre + '_emit', lado)
        _apuntar(materiales, em)
        bpy.ops.object.bake(type='EMIT', use_clear=True)
        e = np.array(em.pixels[:], np.float32).reshape(lado, lado, 4)
        e[..., 3] = 1
        brilla = bpy.data.images.new(nombre + '_luz', lado, lado, alpha=False)
        brilla.pixels.foreach_set(np.clip(e, 0, 1).ravel())
        brilla.filepath_raw = os.path.join(TMP, nombre + '_luz.png')
        brilla.file_format = 'PNG'
        brilla.save()

    # Material final: solo la textura
    m = bpy.data.materials.new(nombre)
    m.use_nodes = True
    b = _principled(m)
    b.inputs['Roughness'].default_value = 0.7
    tx = m.node_tree.nodes.new('ShaderNodeTexImage')
    tx.image = fin
    m.node_tree.links.new(tx.outputs['Color'], b.inputs['Base Color'])
    if brilla:
        tl = m.node_tree.nodes.new('ShaderNodeTexImage')
        tl.image = brilla
        m.node_tree.links.new(tl.outputs['Color'], b.inputs['Emission Color'])
        b.inputs['Emission Strength'].default_value = 1.0
    ob.data.materials.clear()
    ob.data.materials.append(m)

    if suelo:
        bpy.data.objects.remove(piso)
    tris = sum(len(p.vertices) - 2 for p in ob.data.polygons)
    if not exportar:
        # Varias piezas en un mismo archivo (el personaje): esta se aparta para
        # que no tape la luz de las siguientes, y se exporta todo al final.
        print(f'PARTE {nombre}: {tris} triángulos, textura {lado}, {time.time() - t0:.0f} s', flush=True)
        _partes.clear()
        ob.hide_render = True
        return ob
    salida = os.path.join(MODELOS, carpeta)
    os.makedirs(salida, exist_ok=True)
    bpy.ops.object.select_all(action='DESELECT')
    ob.select_set(True)
    kw = dict(filepath=os.path.join(salida, nombre + '.glb'), export_format='GLB', use_selection=True,
              export_image_format='JPEG', export_apply=True, export_animations=False,
              export_yup=True, export_normals=True, export_texcoords=True)
    try:
        bpy.ops.export_scene.gltf(**kw, export_jpeg_quality=85)
    except TypeError:
        bpy.ops.export_scene.gltf(**kw)
    dims = ob.dimensions
    print(f'PIEZA {nombre}: {tris} triángulos, {dims.x:.1f} x {dims.y:.1f} x {dims.z:.1f}, '
          f'textura {lado}, {time.time() - t0:.0f} s', flush=True)


def correr(piezas):
    """piezas: {nombre: (funcion, carpeta, opciones)}"""
    for nombre, (fn, carpeta, op) in piezas.items():
        if SOLO and nombre not in SOLO:
            continue
        empezar()
        fn()
        terminar(nombre, carpeta, **op)
