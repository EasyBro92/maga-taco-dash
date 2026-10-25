# El público de la acera, estilo Pixar (25/10/2026).
#
#   blender -b -P blender/publico.py -- [persona ...] [--rapido]
#
# Isidro: «el público parecen Playmobils sin alma». Antes eran cápsulas y
# esferas sueltas con la cabeza lisa. Ahora: seis personas distintas, de una
# pieza, con cara (ojos con su brillo, cejas, nariz, sonrisa), pelo, ropa con
# volumen y proporciones de dibujos (cabeza grande, manos y pies redondos).
# El brazo derecho va APARTE (`<nombre>_brazo`, con el giro en el hombro) para
# que el juego lo mueva: saludan, aplauden y se animan cuando pasa el jugador.
#
# Miran a -y (en el juego, +z). El origen, en el suelo entre los pies.

import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import *

PIELES = (0xf5c9a6, 0xe0a87e, 0xb57a52, 0x8a5636)

def elip(m, x, y, z, r, esc=(1, 1, 1), rot=(0, 0, 0), sub=2):
    o = esfera(m, x, y, z, r, sub, esc=esc)
    o.rotation_euler = rot
    return o

def cara(piel, x0, z0, r, pelo_c, sonrisa=True, gafas=False):
    """Cabeza con cara de dibujos: ojos con brillo, cejas, nariz, boca."""
    p = mat(f'piel{piel:06x}', piel, 0.55)
    elip(p, x0, 0, z0, r, esc=(1, 0.95, 1.05))
    for s in (-1, 1):
        elip(p, x0 + s * r * 0.98, 0, z0, r * 0.22, esc=(0.5, 0.8, 1))            # orejas
        elip(mat('ojo_blanco', 0xffffff, 0.2), x0 + s * r * 0.36, -r * 0.82, z0 + r * 0.12, r * 0.24, esc=(0.9, 0.5, 1.15))
        elip(mat('pupila', 0x2a1c14, 0.2), x0 + s * r * 0.36, -r * 0.95, z0 + r * 0.1, r * 0.13, esc=(1, 0.5, 1.1))
        elip(mat('brillo', 0xffffff, 0.1), x0 + s * r * 0.33, -r * 1.01, z0 + r * 0.16, r * 0.045)
        caja(mat(f'ceja{pelo_c:06x}', pelo_c, 0.7), x0 + s * r * 0.36, -r * 0.84, z0 + r * 0.42,
             r * 0.4, r * 0.1, r * 0.08, giro=0, inclina=0)
    elip(p, x0, -r * 0.98, z0 - r * 0.08, r * 0.17, esc=(0.9, 1, 1.1))           # nariz
    boca = mat('boca', 0x9a3a3a, 0.5)
    if sonrisa:
        bpy.ops.mesh.primitive_torus_add(major_radius=r * 0.26, minor_radius=r * 0.05, location=(x0, -r * 0.86, z0 - r * 0.32))
        o = bpy.context.object
        o.rotation_euler = (math.pi / 2, 0, 0)
        bm = bmesh.new(); bm.from_mesh(o.data)
        bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.co.y > -r * 0.05], context='VERTS')
        bm.to_mesh(o.data); bm.free()
        from comun import _poner
        _poner(o, boca)
    else:
        elip(boca, x0, -r * 0.9, z0 - r * 0.35, r * 0.14, esc=(1, 0.4, 0.8))
    if gafas:
        for s in (-1, 1):
            cil(mat('gafas', 0x2a2a2e, 0.3), x0 + s * r * 0.36, -r * 1.02, z0 + r * 0.12, r * 0.26, r * 0.04, 16, eje='Y')

def cuerpo_base(alto, ropa, pantalon, piel, zapatos=0x2a2a2e, falda=False, ancho=1.0):
    """Piernas, torso y brazo izquierdo (el derecho va aparte)."""
    p = mat(f'piel{piel:06x}', piel, 0.55)
    k = alto / 1.75
    for s in (-1, 1):
        if not falda:
            cil(mat(f'pant{pantalon:06x}', pantalon, 0.7), s * 0.1 * k, 0, 0.1 * k, 0.085 * k, 0.72 * k, 12, r2=0.1 * k)
        else:
            cil(p, s * 0.09 * k, 0, 0.1 * k, 0.05 * k, 0.5 * k, 10)
        elip(mat(f'zap{zapatos:06x}', zapatos, 0.4), s * 0.1 * k, -0.05 * k, 0.06 * k, 0.09 * k, esc=(1, 1.6, 0.7))
    ro = mat(f'ropa{ropa:06x}', ropa, 0.7)
    if falda:
        cil(ro, 0, 0, 0.5 * k, 0.32 * k * ancho, 0.42 * k, 18, r2=0.17 * k * ancho)
    elip(ro, 0, 0, 1.08 * k, 0.24 * k * ancho, esc=(1.0, 0.75, 1.35))            # torso
    elip(ro, 0, 0, 1.28 * k, 0.21 * k * ancho, esc=(1.15, 0.8, 0.6))             # hombros
    cil(p, 0, 0, 1.36 * k, 0.07 * k, 0.1 * k, 10)                                # cuello
    # brazo izquierdo, caído y algo separado
    rama(ro, (-0.24 * k * ancho, 0, 1.33 * k), (-0.31 * k * ancho, 0, 0.98 * k), 0.065 * k, 0.058 * k, 10)
    rama(ro, (-0.31 * k * ancho, 0, 0.98 * k), (-0.3 * k * ancho, -0.06 * k, 0.72 * k), 0.056 * k, 0.05 * k, 10)
    elip(p, -0.3 * k * ancho, -0.07 * k, 0.66 * k, 0.065 * k, esc=(0.9, 0.8, 1.1))
    return k

def brazo(alto, ropa, piel, ancho=1.0, objeto=None):
    """Brazo derecho, con el origen en el hombro (el juego lo gira)."""
    import comun
    antes = len(comun._partes)
    k = alto / 1.75
    ro = mat(f'ropa{ropa:06x}', ropa, 0.7)
    p = mat(f'piel{piel:06x}', piel, 0.55)
    rama(ro, (0, 0, 0), (0.07 * k, 0, -0.34 * k), 0.065 * k, 0.058 * k, 10)
    rama(ro, (0.07 * k, 0, -0.34 * k), (0.06 * k, -0.07 * k, -0.6 * k), 0.056 * k, 0.05 * k, 10)
    elip(p, 0.06 * k, -0.08 * k, -0.67 * k, 0.065 * k, esc=(0.9, 0.8, 1.1))
    if objeto == 'bandera':
        cil(mat('palo', 0x8a6a4a, 0.7), 0.06 * k, -0.08 * k, -0.75 * k, 0.012, 0.75 * k, 6)
        caja(mat_franjas('franjas_pub', 0xd8283a, 0xffffff, 5, z0=-0.3 * k, alto=0.3 * k), 0.06 * k + 0.2 * k, -0.08 * k,
             -0.3 * k, 0.4 * k, 0.01, 0.3 * k)
    elif objeto == 'cartel':
        cil(mat('palo', 0x8a6a4a, 0.7), 0.06 * k, -0.08 * k, -0.75 * k, 0.015, 1.0 * k, 6)
        caja(mat('cartel_pub', 0xffffff, 0.6), 0.06 * k, -0.1 * k, 0.05 * k, 0.55 * k, 0.02, 0.36 * k)
        texto(mat('letra_cartel', 0xd8283a, 0.5), 'USA!', 0.06 * k, -0.12 * k, 0.23 * k, tam=0.16 * k, prof=0.01)
    for o in comun._partes[antes:]:
        o["es_brazo"] = True
    return (0.24 * k * ancho, 0, 1.33 * k)                                        # dónde va el hombro


# ---------------------------------------------------------------- las seis personas
def ejecutivo():
    piel = PIELES[0]
    k = cuerpo_base(1.8, 0x2c3a52, 0x2c3a52, piel, ancho=1.1)
    caja(mat('camisa_e', 0xffffff, 0.5), 0, -0.2 * k, 1.12 * k, 0.12 * k, 0.04, 0.28 * k)
    caja(mat('corbata_e', 0x2f6bd8, 0.5), 0, -0.22 * k, 0.98 * k, 0.05 * k, 0.03, 0.34 * k)
    cara(piel, 0, 1.62 * k, 0.21 * k, 0x5a3a28)
    elip(mat('pelo_e', 0x5a3a28, 0.7), 0, 0.03 * k, 1.72 * k, 0.215 * k, esc=(1.02, 1, 0.6))
    return brazo(1.8, 0x2c3a52, piel, 1.1)

def senora():
    piel = PIELES[1]
    k = cuerpo_base(1.68, 0xe8607a, 0xe8607a, piel, zapatos=0xb83a52, falda=True)
    cara(piel, 0, 1.62 * k, 0.21 * k, 0x8a5a3a, gafas=True)
    pelo = mat('pelo_s', 0xc9c2b8, 0.7)
    elip(pelo, 0, 0.04 * k, 1.7 * k, 0.24 * k, esc=(1.05, 1.05, 0.75))
    elip(pelo, 0, 0.12 * k, 1.92 * k, 0.12 * k)                                  # moño
    elip(mat('collar', 0xf6f0e0, 0.3), 0, -0.14 * k, 1.3 * k, 0.12 * k, esc=(1, 0.5, 0.3))
    return brazo(1.68, 0xe8607a, piel, 1.0, 'bandera')

def chico():
    piel = PIELES[2]
    k = cuerpo_base(1.15, 0xffc53a, 0x3a6ad8, piel, zapatos=0xe8463c)
    cara(piel, 0, 1.6 * k, 0.26 * k, 0x2a1a12)                                  # cabezota de niño
    elip(mat('pelo_c', 0x2a1a12, 0.8), 0, 0.03 * k, 1.75 * k, 0.26 * k, esc=(1.05, 1.05, 0.55))
    cil(mat('cordel', 0xdddddd, 0.5), -0.3 * k, -0.07 * k, 0.66 * k, 0.006, 1.3, 4)
    elip(mat('globo_c', 0xe8463c, 0.25), -0.3 * k, -0.07 * k, 0.66 * k + 1.45, 0.2, esc=(1, 1, 1.2))
    return brazo(1.15, 0xffc53a, piel)

def abuelo():
    piel = PIELES[0]
    k = cuerpo_base(1.66, 0x7a8a5a, 0x8a7a6a, piel, zapatos=0x5a3a28, ancho=1.15)
    cara(piel, 0, 1.6 * k, 0.21 * k, 0xe8e4dc, gafas=True)
    elip(mat('bigote', 0xe8e4dc, 0.7), 0, -0.2 * k, 1.53 * k, 0.07 * k, esc=(1.6, 0.5, 0.5))
    gorra = mat('gorra_roja', 0xd8283a, 0.6)
    elip(gorra, 0, 0.0, 1.73 * k, 0.215 * k, esc=(1.02, 1.02, 0.55))
    caja(gorra, 0, -0.2 * k, 1.71 * k, 0.26 * k, 0.18 * k, 0.03 * k)
    return brazo(1.66, 0x7a8a5a, piel, 1.15, 'cartel')

def turista():
    piel = PIELES[3]
    k = cuerpo_base(1.74, 0x3ab0a0, 0xe0c890, piel, zapatos=0xf2f2f2)
    for x, y, c in ((-0.1, -0.2, 0xffd23f), (0.12, -0.21, 0xff7a3a), (0.0, -0.22, 0xff4f8a)):   # flores de la camisa
        elip(mat(f'flor{c:06x}', c, 0.6), x * k, y * k, 1.1 * k, 0.04 * k)
    cara(piel, 0, 1.62 * k, 0.21 * k, 0x1a1a1a)
    elip(mat('pelo_t', 0x1a1a1a, 0.8), 0, 0.03 * k, 1.72 * k, 0.22 * k, esc=(1.05, 1.05, 0.5))
    caja(mat('camara', 0x2a2a2e, 0.4), 0, -0.24 * k, 1.12 * k, 0.16 * k, 0.08 * k, 0.11 * k)
    cil(mat('objetivo', 0x5a6a7a, 0.2), 0, -0.29 * k, 1.12 * k, 0.04 * k, 0.05 * k, 12, eje='Y')
    return brazo(1.74, 0x3ab0a0, piel)

def fan():
    """Seguidora con gorra roja y camiseta de barras y estrellas."""
    piel = PIELES[1]
    k = cuerpo_base(1.7, 0x1f3c88, 0x2a3a5a, piel, zapatos=0xffffff)
    for i in range(3):
        caja(mat('franja_fan', 0xd8283a, 0.6), 0, -0.21 * k, (1.0 + i * 0.1) * k, 0.3 * k, 0.03, 0.035 * k)
    cara(piel, 0, 1.62 * k, 0.21 * k, 0xc98a3a)
    pelo = mat('pelo_f', 0xd99a3a, 0.7)
    elip(pelo, 0, 0.05 * k, 1.66 * k, 0.24 * k, esc=(1.05, 1.0, 0.85))
    elip(pelo, 0, 0.2 * k, 1.45 * k, 0.12 * k, esc=(1, 1, 1.6))                 # coleta
    gorra = mat('gorra_roja', 0xd8283a, 0.6)
    elip(gorra, 0, 0.0, 1.74 * k, 0.215 * k, esc=(1.02, 1.02, 0.55))
    caja(gorra, 0, -0.2 * k, 1.72 * k, 0.26 * k, 0.18 * k, 0.03 * k)
    return brazo(1.7, 0x1f3c88, piel, 1.0, 'bandera')


PERSONAS = {'ejecutivo': ejecutivo, 'senora': senora, 'chico': chico,
            'abuelo': abuelo, 'turista': turista, 'fan': fan}

for nombre, fn in PERSONAS.items():
    if SOLO and nombre not in SOLO:
        continue
    empezar()
    bpy.context.scene.world.light_settings.distance = 0.25
    # El brazo se construye en su sitio (hombro en el origen) y luego el cuerpo.
    from comun import _partes
    hombro = None
    # primero el cuerpo entero, guardando dónde va el hombro
    hombro = fn()
    # fn ya ha añadido el brazo derecho a _partes: separarlo
    import comun
    partes = list(comun._partes)
    # las piezas del brazo son las últimas que añadió `brazo()`
    n_brazo = sum(1 for o in partes if o.get('es_brazo'))
    cuerpo_obj = None
    comun._partes.clear()
    brazo_partes = [o for o in partes if o.get('es_brazo')]
    resto = [o for o in partes if not o.get('es_brazo')]
    comun._partes.extend(resto)
    c = terminar(f'{nombre}_cuerpo', 'publico', lado=256 if RAPIDO else 512, bisel=0.0, oclusion=0.5, suelo=False, exportar=False)
    comun._partes.extend(brazo_partes)
    b = terminar(f'{nombre}_brazo', 'publico', lado=128 if RAPIDO else 256, bisel=0.0, oclusion=0.4, suelo=False, exportar=False)
    # el brazo ya se hizo con el hombro en el origen: el juego lo pone en su sitio
    b.hide_render = False; c.hide_render = False
    bpy.ops.object.select_all(action='DESELECT')
    b.select_set(True); c.select_set(True)
    salida = os.path.join(MODELOS, 'publico')
    os.makedirs(salida, exist_ok=True)
    bpy.ops.export_scene.gltf(filepath=os.path.join(salida, f'{nombre}.glb'), export_format='GLB',
                              use_selection=True, export_image_format='JPEG', export_apply=True,
                              export_animations=False, export_yup=True)
    print(f'PERSONA {nombre}: hombro {tuple(round(v, 3) for v in hombro)}', flush=True)
