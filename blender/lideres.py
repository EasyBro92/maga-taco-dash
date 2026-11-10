# Los líderes de la caja sorpresa (10/11/2026). Isidro: «los premios se
# sienten muy sosos y sin ningún significado, cámbialos a nuevos personajes
# como Netanyahu, Vladimir Putin, Kim Jong-un y presidentes polémicos».
#
#   blender -b -P blender/lideres.py -- [id ...] [--rapido]
#
# Caricaturas de dibujos, con el mismo cuerpo que el presidente de piezas
# (personaje.py): se cambian la cabeza, el pelo, la camisa / cuello y, a
# algunos, lo que llevan en la mano. Así corren con las mismas animaciones.
#
# Sale, por cada uno, www/models/lideres/<id>.glb con las mallas
#   <id>_cabeza  <id>_pelo  <id>_resto  [<id>_extra]
# y su retrato (www/models/lideres/<id>.png) para la ruleta y la tienda.
# Los ojos, las cejas y la boca los pone el juego (cambian de gesto); para el
# retrato se ponen aquí unos iguales que no se exportan.

import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import *
from comun import _partes
from personaje import torno, lamina, elip, esfera_uv, frente, PERFIL, PROF

# piel, pelo (color, brillo), cejas, traje, cuello ('traje' | 'mao' | 'chandal' | 'banda'),
# insignia (dos colores), y la forma: ancho de cara, mandíbula, nariz.
LIDERES = {
    'putin': dict(piel=0xf3c9ad, pelo=(0xc9b394, 0xb59d7e), traje=0x2f333b, cuello='traje', pin=(0x2a4fb0, 0xd8322f),
                  ancho=0.96, mandibula=0.12, nariz=0.9, nuca=0.0, frente_pelo=0.11),
    'kim': dict(piel=0xf6d2ac, pelo=(0x1a1a1c, 0x2a2a2e), traje=0x26282d, cuello='mao', pin=(0xd8322f, 0x2a4fb0),
                ancho=1.16, mandibula=0.22, nariz=0.85, nuca=0.0, frente_pelo=0.0, rapado=0x3a3836),
    'netanyahu': dict(piel=0xefc2a1, pelo=(0xdedcd6, 0xc8c5be), traje=0x1f2a44, cuello='traje', pin=(0x2a5fd0, 0xffffff),
                      ancho=1.0, mandibula=0.18, nariz=1.15, nuca=0.0, frente_pelo=0.04),
    'xi': dict(piel=0xf4d0a6, pelo=(0x1c1c1e, 0x2c2c30), traje=0x24272e, cuello='traje', pin=(0xd8322f, 0xffd23c),
               ancho=1.05, mandibula=0.22, nariz=0.95, nuca=0.0, frente_pelo=0.0),
    'milei': dict(piel=0xf1c4a0, pelo=(0x5c3b22, 0x4a2e19), traje=0x1d1e22, cuello='traje', pin=(0x74b7e8, 0xffffff),
                  ancho=1.0, mandibula=0.2, nariz=1.05, nuca=0.0, frente_pelo=-0.02, patillas=True),
    'maduro': dict(piel=0xd8a27c, pelo=(0x221c19, 0x3a3532), traje=0x2140a0, cuello='chandal', pin=(0xffd23c, 0xd8322f),
                   ancho=1.08, mandibula=0.3, nariz=1.1, nuca=0.0, frente_pelo=0.0, bigote=0x1c1714),
    'bolsonaro': dict(piel=0xf0c4a3, pelo=(0x6e6762, 0x595350), traje=0x2b3346, cuello='banda', pin=(0x2fa84f, 0xffd23c),
                      ancho=1.0, mandibula=0.2, nariz=1.05, nuca=0.0, frente_pelo=0.03),
    'erdogan': dict(piel=0xeab995, pelo=(0xd0cbc3, 0xbab4ab), traje=0x2a2d35, cuello='traje', pin=(0xd8322f, 0xffffff),
                    ancho=1.02, mandibula=0.2, nariz=1.1, nuca=0.0, frente_pelo=0.09, bigote=0xc9c3ba),
}
CORBATA = {'putin': 0x55627a, 'netanyahu': 0x5a8fd8, 'xi': 0xc0272d, 'milei': 0x18181b,
           'bolsonaro': 0x2fa84f, 'erdogan': 0x7a1f2a}   # los otros no llevan

def piel(L):  return mat('piel_' + L['id'], L['piel'], 0.55)
def pelo(L):  return mat_franjas('pelo_' + L['id'], L['pelo'][0], L['pelo'][1], 18, eje='Y', z0=-0.45, alto=0.9)


# ---------------------------------------------------------------- cabeza
def cabeza(L):
    o = esfera_uv(piel(L), 0, 0, 0, 0.36, 36, 22)
    for v in o.data.vertices:
        x, y, z = v.co
        t = max(0.0, -z / 0.36)
        mof = max(0.0, 1 - abs(z + 0.05) / 0.25)          # los mofletes, a media cara
        v.co = (x * 1.03 * L['ancho'] * (1 + L['mandibula'] * t) * (1 + 0.04 * mof * (L['ancho'] - 1) * 10),
                y * 0.98 * (1 + 0.16 * t), z * 0.98)
    a = L['ancho']
    for s in (-1, 1):
        elip(piel(L), s * 0.39 * a, 0.0, -0.02, 0.07, esc=(0.5, 0.9, 1.15), sub=2)   # orejas
    n = L['nariz']
    elip(piel(L), 0, -0.352, -0.045, 0.062 * n, esc=(0.95, 1.0, 1.15), sub=2)       # nariz
    elip(piel(L), 0, -0.33, 0.02, 0.038 * n, esc=(0.8, 1.0, 1.6), sub=2)            # tabique
    if L.get('bigote'):
        b = mat('bigote_' + L['id'], L['bigote'], 0.8)
        for s in (-1, 1):
            elip(b, s * 0.055, -0.352, -0.118, 0.05, esc=(1.5, 0.55, 0.62), rot=(0, s * 0.25, 0), sub=2)
    # el casco de pelo (Kim: rapado a los lados, de otro color)
    m = mat('rapado_' + L['id'], L['rapado'], 0.8) if L.get('rapado') else pelo(L)
    o = esfera_uv(m, 0, 0.025, 0.005, 0.372, 36, 22, esc=(1.07 * a, 1.03, 1.0))
    bm = bmesh.new(); bm.from_mesh(o.data)
    fuera = []
    for v in bm.verts:
        x, y, z = v.co
        delante = -y / 0.372
        limite = 0.1 * max(0.0, delante) ** 0.6 - 0.18 * max(0.0, -delante) - 0.02 + L['frente_pelo'] * max(0.0, delante)
        if delante > -0.2:   # patillas (largas las de Milei), entrando poco a poco
            lado = min(1.0, max(0.0, (abs(x) - 0.24) / 0.08))
            limite = limite + (max(limite, -0.12 if L.get('patillas') else 0.02) - limite) * lado
        if z < limite - 0.06:
            fuera.append(v); continue
        # el borde se mete en la cabeza poco a poco: sin visera en la frente
        k = min(1.0, max(0.0, (z - (limite - 0.06)) / 0.1))
        k = k * k * (3 - 2 * k)
        v.co *= 0.88 + 0.12 * k
    bmesh.ops.delete(bm, geom=fuera, context='VERTS')
    bm.to_mesh(o.data); bm.free()


def casquete(m, L, r=0.385, alto=1.0, corte=0.12, frente=0.08, dx=0.0, dy=0.0):
    """Una capa de pelo pegada a la cabeza: una esfera algo mayor que el
    casco, recortada por abajo (más alta en la frente)."""
    o = esfera_uv(m, dx, 0.02 + dy, 0.0, r, 36, 22, esc=(1.07 * L['ancho'], 1.04, alto))
    bm = bmesh.new(); bm.from_mesh(o.data)
    # Por abajo se va metiendo en el casco poco a poco: sin escalón en la frente.
    dentro = 0.366 / r
    fuera = []
    for v in bm.verts:
        x, y, z = v.co
        delante = -y / r
        t = (corte + frente * max(0.0, delante) - 0.1 * max(0.0, -delante)) / alto
        if z < t - 0.07:
            fuera.append(v); continue
        k = min(1.0, max(0.0, (z - (t - 0.07)) / 0.11))
        k = k * k * (3 - 2 * k)
        v.co *= dentro + (1 - dentro) * k
    bmesh.ops.delete(bm, geom=fuera, context='VERTS')
    bm.to_mesh(o.data); bm.free()
    return o


def pelo_encima(L):
    """Lo de arriba del pelo, aparte (encima del casco)."""
    p, i = pelo(L), L['id']
    if i == 'putin':      # poco y fino
        casquete(p, L, r=0.378, alto=0.97, corte=0.2, frente=0.06)
    elif i == 'kim':      # el bloque alto de arriba, con los lados rapados
        casquete(p, L, r=0.385, alto=1.32, corte=0.16, frente=0.04)
        elip(p, 0, -0.26, 0.33, 0.1, esc=(2.4, 0.9, 0.55), rot=(0.5, 0, 0), sub=2)
    elif i == 'netanyahu':  # raya al lado, hacia atrás
        casquete(p, L, r=0.388, alto=1.06, corte=0.1, frente=0.1)
        elip(p, -0.08, -0.26, 0.3, 0.1, esc=(2.2, 1.0, 0.55), rot=(0.45, 0, 0.25), sub=2)
    elif i == 'xi':       # todo hacia atrás, liso y alto
        casquete(p, L, r=0.39, alto=1.1, corte=0.14, frente=0.12)
    elif i == 'milei':    # la melena: mechones gordos hacia todos lados
        casquete(p, L, r=0.395, alto=1.1, corte=0.02, frente=0.12)
        for k in range(10):
            ang = k / 10 * math.tau
            x, y = math.cos(ang) * 0.27, math.sin(ang) * 0.25 + 0.03
            elip(p, x, y, 0.27, 0.11, esc=(1.2, 1.2, 0.85), rot=(math.sin(ang) * 0.7, -math.cos(ang) * 0.7, ang), sub=2)
        elip(p, -0.09, -0.27, 0.3, 0.1, esc=(1.7, 1.0, 0.6), rot=(0.5, 0, 0.4), sub=2)   # el flequillo
    elif i == 'maduro':
        casquete(p, L, r=0.39, alto=1.08, corte=0.08, frente=0.1)
    elif i == 'bolsonaro':
        casquete(p, L, r=0.386, alto=1.04, corte=0.1, frente=0.1)
        elip(p, -0.1, -0.26, 0.29, 0.09, esc=(2.2, 1.0, 0.55), rot=(0.45, 0, 0.25), sub=2)
    else:                 # erdogan: con entradas
        casquete(p, L, r=0.383, alto=1.0, corte=0.14, frente=0.12)


# ---------------------------------------------------------------- camisa y cuello
def resto(L):
    i = L['id']
    oscuro = mat('oscuro_' + i, 0x1c2541 if L['cuello'] != 'mao' else 0x17181c, 0.5)
    blanco = mat('camisa', 0xffffff, 0.5)
    if L['cuello'] in ('traje', 'banda'):
        filas = []
        for k in range(8):
            z = 0.63 - k * (0.33 / 7)
            w = 0.115 * (z - 0.30) / 0.33
            filas.append([(x, frente(x, z, 0.004), z) for x in (-w, -w / 2, 0, w / 2, w)])
        lamina(blanco, filas, 0.012)
        for s in (-1, 1):
            filas = []
            for k in range(8):
                z = 0.63 - k * (0.37 / 7)
                w = max(0.0, 0.115 * (z - 0.30) / 0.33)
                filas.append([(x, frente(x, z, 0.008), z) for x in (s * w, s * (w + 0.04), s * (w + 0.08))])
            lamina(oscuro, filas, 0.014)
        cil(blanco, 0, 0, 0.6, 0.135, 0.07, 16)
    elif L['cuello'] == 'mao':     # Kim: cuello cerrado y botones en el centro
        cil(mat('cuello_' + i, L['traje'], 0.55), 0, 0, 0.585, 0.14, 0.09, 18)
        for z in (0.5, 0.4, 0.3, 0.2, 0.1):
            esfera(mat('boton_mao', 0x6b6e75, 0.3), 0, frente(0, z, 0.0), z, 0.02, 1)
        filas = [[(x, frente(x, z, 0.004), z) for x in (-0.006, 0.006)] for z in [0.05 + 0.55 * k / 6 for k in range(7)]]
        lamina(oscuro, filas, 0.008)
    else:                          # Maduro: chaqueta de chándal con la franja de la bandera
        cil(mat('cuello_' + i, 0x1a3585, 0.55), 0, 0, 0.58, 0.14, 0.08, 18)
        filas = [[(x, frente(x, z, 0.004), z) for x in (-0.008, 0.008)] for z in [0.0 + 0.6 * k / 6 for k in range(7)]]
        lamina(mat('cremallera', 0xd9d9d9, 0.3), filas, 0.01)
        for z0, c in ((0.36, 0xffd23c), (0.30, 0xd8322f)):
            filas = []
            for k in range(3):
                z = z0 + k * 0.025
                filas.append([(x, frente(x, z, 0.006), z) for x in [-0.33 + 0.66 * j / 16 for j in range(17)]])
            lamina(mat('franja_%x' % c, c, 0.5), filas, 0.01)
    if L['cuello'] == 'banda':     # Bolsonaro: la banda presidencial verde y amarilla
        for off, c in ((-0.03, 0x2fa84f), (0.0, 0xffd23c), (0.03, 0x2fa84f)):
            filas = []
            for k in range(12):
                f = k / 11
                x0 = -0.27 + 0.5 * f
                z = 0.55 - 0.5 * f + off
                filas.append([(x, frente(x, z, 0.012), z) for x in (x0 - 0.035, x0, x0 + 0.035)])
            lamina(mat('banda_%x' % c, c, 0.5), filas, 0.012)
    cil(piel(L), 0, 0, 0.6, 0.105 * min(1.1, L['ancho']), 0.16, 14)       # el cuello
    if L['cuello'] in ('traje', 'banda'):
        for z in (0.24, 0.15):
            esfera(mat('boton', 0x16182a, 0.4), 0, frente(0, z, 0.0), z, 0.022, 1)
    a, b = L['pin']
    caja(mat('pin_%x' % a, a, 0.4), -0.17, frente(-0.17, 0.5, 0.02), 0.49, 0.045, 0.012, 0.03)
    caja(mat('pin_%x' % b, b, 0.4), -0.185, frente(-0.185, 0.5, 0.026), 0.495, 0.018, 0.012, 0.02)
    filas = [[(x, -frente(x, z, 0.004), z) for x in (-0.012, 0.012)] for z in [0.12 + 0.42 * k / 6 for k in range(7)]]
    lamina(oscuro, filas, 0.008)


# ---------------------------------------------------------------- en la mano
def extra(L):
    """Va colgado del codo derecho, como la mano (la mano está en z = -0.3)."""
    if L['id'] == 'milei':        # la motosierra, apuntando hacia delante
        nar = mat('motor', 0xf28c1c, 0.4)
        caja(nar, 0, -0.08, -0.4, 0.12, 0.24, 0.16)
        caja(mat('asa', 0x222226, 0.6), 0, 0.02, -0.33, 0.03, 0.1, 0.04)
        caja(mat('espada', 0xc9ccd2, 0.25), 0, -0.42, -0.36, 0.02, 0.48, 0.07)
        cadena = mat('cadena', 0x4a4c52, 0.4)
        for k in range(12):
            caja(cadena, 0, -0.2 - k * 0.04, -0.375, 0.03, 0.02, 0.1)
    elif L['id'] == 'kim':        # un misil de juguete
        caja(mat('misil', 0xe9e9e4, 0.4), 0, -0.1, -0.34, 0.07, 0.3, 0.07)
        cil(mat('punta_misil', 0xd8322f, 0.4), 0, -0.25, -0.305, 0.05, 0.09, 12, r2=0.0, eje='Y')
        for s in (-1, 1):
            caja(mat('aleta', 0xd8322f, 0.4), s * 0.05, 0.02, -0.34, 0.06, 0.06, 0.012)


# ---------------------------------------------------------------- retrato
def retrato(L, hechas):
    """Una foto de la cabeza y los hombros, con ojos, cejas y boca como los del juego."""
    for o in hechas:
        o.hide_render = False
        if o.name.endswith(('_cabeza', '_pelo')):
            o.location.z = 0.78
    _partes.clear()
    torno(mat('traje_' + L['id'], L['traje'], 0.6), PERFIL, lados=32, prof=PROF)
    for s in (-1, 1):
        elip(mat('traje_' + L['id'], L['traje'], 0.6), s * 0.27, 0, 0.53, 0.14, esc=(1.15, 0.85, 0.9))
    if L['id'] in CORBATA:
        c = mat('corbata_' + L['id'], CORBATA[L['id']], 0.5)
        elip(c, 0, frente(0, 0.56, 0.025), 0.56, 0.045, esc=(1.0, 0.7, 0.9), sub=2)
        caja(c, 0, frente(0, 0.4, 0.03), 0.2, 0.08, 0.02, 0.34)
    blanco, negro = mat('ojo', 0xffffff, 0.3), mat('pupila', 0x2a1c10, 0.3)
    ceja = mat('ceja_' + L['id'], L['pelo'][0] if L['id'] != 'putin' else 0xa8916f, 0.8)
    for s in (-1, 1):
        elip(blanco, s * 0.1326, -0.312, 0.78 + 0.0234, 0.082, esc=(1, 1, 0.62), sub=3)
        elip(negro, s * 0.1326, -0.381, 0.78 + 0.026, 0.04, esc=(1, 0.6, 0.9), sub=2)
        elip(piel(L), s * 0.1326, -0.318, 0.78 + 0.05, 0.084, esc=(1.04, 1.04, 0.45), sub=3)   # párpado
        caja(ceja, s * 0.1326, -0.335, 0.78 + 0.11, 0.1, 0.03, 0.026, inclina=0, giro=0)
    caja(mat('boca', 0x8a2f2f, 0.5), 0, -0.336, 0.78 - 0.19, 0.09, 0.025, 0.022)
    sc = bpy.context.scene
    sc.render.resolution_x = sc.render.resolution_y = 256
    sc.render.film_transparent = True
    sc.cycles.samples = 12 if RAPIDO else 48
    sc.world.node_tree.nodes['Background'].inputs['Strength'].default_value = 0.55
    bpy.ops.object.light_add(type='SUN', location=(1, -2, 3))
    sol = bpy.context.object
    sol.data.energy = 3.2
    sol.rotation_euler = (math.radians(50), math.radians(10), math.radians(-25))
    bpy.ops.object.camera_add(location=(0.55, -2.35, 0.9))
    cam = bpy.context.object
    cam.data.lens = 72
    mira = bpy.data.objects.new('mira', None)
    bpy.context.scene.collection.objects.link(mira)
    mira.location = (0, 0, 0.74)
    rest = cam.constraints.new('TRACK_TO')
    rest.target = mira
    sc.camera = cam
    sc.render.filepath = os.path.join(MODELOS, 'lideres', L['id'] + '.png')
    sc.render.image_settings.file_format = 'PNG'
    sc.render.image_settings.color_mode = 'RGBA'
    bpy.ops.render.render(write_still=True)
    print('RETRATO', L['id'], flush=True)


def hacer(i):
    L = dict(LIDERES[i], id=i)
    empezar()
    bpy.context.scene.world.light_settings.distance = 0.3
    piezas = [('cabeza', cabeza, 512), ('pelo', pelo_encima, 256), ('resto', resto, 256)]
    if i in ('milei', 'kim'):
        piezas.append(('extra', extra, 128))
    hechas = []
    for nombre, fn, lado in piezas:
        fn(L)
        hechas.append(terminar(f'{i}_{nombre}', 'lideres', lado=lado, bisel=0.01, oclusion=0.55,
                               suelo=False, exportar=False))
    for o in hechas:
        o.hide_render = False
    bpy.ops.object.select_all(action='DESELECT')
    for o in hechas:
        o.select_set(True)
    salida = os.path.join(MODELOS, 'lideres')
    os.makedirs(salida, exist_ok=True)
    kw = dict(filepath=os.path.join(salida, i + '.glb'), export_format='GLB', use_selection=True,
              export_image_format='JPEG', export_apply=True, export_animations=False, export_yup=True)
    try:
        bpy.ops.export_scene.gltf(**kw, export_jpeg_quality=85)
    except TypeError:
        bpy.ops.export_scene.gltf(**kw)
    print('LIDER exportado:', i, len(hechas), 'partes', flush=True)
    retrato(L, hechas)


def hacer_trump():
    """Solo el retrato del presidente de siempre (para la lista de la tienda)."""
    import personaje as P
    empezar()
    L = dict(id='trump', piel=P.PIEL, pelo=(P.RUBIO1, P.RUBIO2), traje=0x2b3f7a)
    CORBATA['trump'] = 0xd8322f
    n0 = len(bpy.data.objects)
    P.cabeza(); P.tupe()
    for o in list(bpy.data.objects)[n0:]:
        o.location.z += 0.78
    P.torso_resto()
    retrato(L, [])


for i in (SOLO or list(LIDERES) + ['trump']):
    hacer_trump() if i == 'trump' else hacer(i)
