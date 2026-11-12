# Nivel 16: Houston, Texas (12/11/2026).
#
#   blender -b -P blender/houston.py -- [pieza ...] [--rapido]
#
# Historia: «La NASA. Tu examigo Elon, enfadado tras la pelea, te persigue
# en cohete».
#   Por Main Street (el Bank of America con sus tejados escalonados, la torre
#   de JPMorgan Chase, el Ayuntamiento con su estanque) hacia el Space Center:
#   el Saturno V tumbado en su nave, el hangar de la Luna (por dentro: suelo
#   lunar con cráteres, el módulo lunar, banderas y las paredes pintadas de
#   noche con la Tierra) y, al final, el 747 de la NASA con el transbordador
#   encima (Independence Plaza).
# Obstáculos (carpeta obstaculos): el Cybertruck que Elon tira desde su nave
# (cae donde marca la diana), la nave de Elon (de adorno, en el cielo), el
# vehículo lunar, la roca lunar, el astronauta que cruza flotando y la
# pancarta «ELON 2028».

import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import *
from comun import _poner

def blanco():  return mat('blanco_hou', 0xf6f6f2, 0.45)
def negro():   return mat('negro_hou', 0x1b1c20, 0.4)
def rojo():    return mat('rojo_hou', 0xc8282c, 0.45)
def azul():    return mat('azul_hou', 0x1f4fa8, 0.45)
def acero():   return mat('acero_hou', 0xc4cad0, 0.25)
def inox():    return mat('inox_hou', 0xb8bec4, 0.18)
def gris_l():  return mat('gris_luna', 0x9a9a98, 0.95)
def gris_o():  return mat('gris_luna_os', 0x6e6e6c, 0.95)
def oro():     return mat('oro_hou', 0xe0b040, 0.3)

def cohete_cuerpo(m, x, y, z, r, largo, eje='Y'):
    return cil(m, x, y, z, r, largo, 24, eje=eje)

# ================================================================ edificios
def bank_of_america_hou():
    """El Bank of America Center (1983): granito rojo y tres torres
    escalonadas con tejados a dos aguas de estilo holandés."""
    gr = mat_ventanas('granito_boa', 0x2c3440, 0xa8564a, paso_x=1.5, paso_z=3.2, hueco_x=0.7, hueco_z=2.4, variacion=1.04)
    Y = 14
    for (w, d, h, dz) in ((34, 26, 30, 0), (26, 20, 52, 0), (16, 14, 72, 0)):
        caja(gr, 0, Y, 0, w, d, h)
        tejado(mat('tejado_boa', 0x7a3a30, 0.6), 0, Y - d / 2, Y + d / 2, h, w, 7, vuelo=0.3)
        hastial(gr, 0, Y - d / 2 - 0.3, Y - d / 2 + 2, h, w, 7)
        for s in (-1, 1):
            cil(mat('aguja_boa', 0x7a3a30, 0.5), s * (w / 2 - 1), Y - d / 2, h, 0.5, 4, 6, r2=0.05)
    texto(mat('letras_boa', 0xf2e6c8, 0.5), 'BANK OF AMERICA', 0, Y - 13.1, 5.5, tam=1.3, prof=0.06)

def jpmorgan_hou():
    """La JPMorgan Chase Tower (1982), la más alta de Texas: granito gris
    oscuro, la esquina cortada en bisel y la azotea plana."""
    v = mat_ventanas('cristal_jpm', 0x22303e, 0x6a6e72, paso_x=1.5, paso_z=3.4, hueco_x=1.2, hueco_z=2.7, variacion=1.03)
    Y = 15
    caja(v, 0, Y, 0, 30, 28, 140)
    o = caja(v, -12, Y - 12, 0, 10, 10, 140); o.rotation_euler = (0, 0, math.pi / 4)
    caja(mat('remate_jpm', 0x4a4e52, 0.6), 0, Y, 140, 30.6, 28.6, 2)
    caja(mat('base_jpm', 0x8a8e92, 0.6), 0, Y, 0, 34, 30, 8)
    texto(mat('letras_jpm', 0xe8e8e2, 0.5), 'JPMORGAN CHASE', 0, Y - 15.1, 6.2, tam=1.1, prof=0.06)

def city_hall_hou():
    """El Ayuntamiento de Houston (1939): piedra caliza, art déco, la torre
    central y el estanque largo delante con la palabra HOUSTON."""
    piedra = mat_ventanas('caliza_hou', 0x3a4450, 0xe6dcc4, paso_x=1.4, paso_z=3.2, hueco_x=0.6, hueco_z=2.0, variacion=1.03)
    Y = 16
    caja(piedra, 0, Y, 0, 40, 18, 14)
    caja(piedra, 0, Y, 14, 16, 14, 24)
    for k in range(3):
        caja(mat('remate_hou', 0xd8ccb2, 0.6), 0, Y, 38 + k * 1.6, 14 - k * 3, 12 - k * 3, 1.6)
    cil(acero(), 0, Y, 42.8, 0.15, 6, 6)
    caja(mat('agua_hou', 0x5aa0c8, 0.05), 0, 1, -0.05, 30, 8, 0.12)
    caja(mat('borde_estanque', 0xd8ccb2, 0.6), 0, 1, -0.05, 31, 9, 0.08)
    texto(mat('letras_hou_b', 0xf2f2ee, 0.4), 'HOUSTON', 0, 5.6, 0.4, tam=1.6, prof=0.3).rotation_euler = (math.pi / 2, 0, 0)
    texto(mat('letras_hou', 0x5a4a3a, 0.5), 'CITY HALL', 0, Y - 9.1, 11, tam=1.0, prof=0.05)

def saturno_v():
    """El Saturno V tumbado en el Rocket Park del Space Center: el cohete
    blanco y negro de la Luna, por fases, bajo su nave alargada."""
    Y = 10
    # La nave: tejado sobre pilares.
    for k in range(9):
        x = -32 + k * 8
        for s in (-1, 1):
            cil(acero(), x, Y + s * 7, 0, 0.25, 11, 6)
    caja(mat('tejado_nave', 0xd8dce0, 0.5), 0, Y, 11, 70, 16, 0.6)
    # El cohete, a lo largo (x), sobre sus soportes.
    z0 = 5
    for (x0, x1, r) in ((-30, -8, 5.0), (-8, 6, 5.0), (6, 16, 3.3), (16, 22, 3.3)):
        cil(blanco(), (x0 + x1) / 2, Y, z0, r, x1 - x0, 32, eje='X')
    for (x, w) in ((-26, 2), (-14, 3), (2, 2), (12, 1.5)):
        cil(negro(), x, Y, z0, 5.05 if x < 6 else 3.35, w, 32, eje='X')
    cil(blanco(), 25, Y, z0, 2.4, 6, 24, eje='X', r2=None)
    o = cil(blanco(), 30, Y, z0, 2.4, 6, 24, eje='X'); o.scale = (1, 1, 1)
    cil(blanco(), 33.5, Y, z0, 1.6, 3, 16, eje='X')
    for k in range(5):                           # los motores F-1
        a = k * math.tau / 5
        cil(mat('motor_f1', 0x3a3a3e, 0.4), -32.5, Y + math.cos(a) * 3, z0 + math.sin(a) * 3, 1.6, 3, 16, eje='X')
    for x in (-24, -4, 14):
        for s in (-1, 1):
            caja(acero(), x, Y + s * 2.5, 0, 1, 1, z0 - 3)
    texto(mat('letras_usa', 0x1b1c20, 0.4), 'USA', -18, Y - 5.1, z0 + 1.2, tam=2.4, prof=0.06)
    texto(rojo(), 'UNITED STATES', 0, Y - 5.1, z0 + 1, tam=1.2, prof=0.06)
    texto(mat('letras_rp', 0x1f4fa8, 0.5), 'ROCKET PARK', 0, 0.9, 0.6, tam=0.9, prof=0.05)

def independence_plaza():
    """Independence Plaza: el Boeing 747 de la NASA (blanco con la franja
    azul) sobre sus pilares, con el transbordador espacial encima."""
    # Los pilares.
    for (x, y) in ((-6, 0), (6, 0), (0, 14)):
        caja(mat('pilar_ip', 0x8a8e92, 0.6), x, y, 0, 3, 3, 10)
    # El fuselaje del 747 (a lo largo de y, mirando a -y) y la joroba.
    Z = 15
    cil(blanco(), 0, -6, Z, 3.6, 60, 32, eje='Y')
    esfera(blanco(), 0, -36, Z, 3.6, 3, esc=(1, 1.4, 1))
    esfera(blanco(), 0, -28, Z + 2.6, 2.6, 3, esc=(1, 3.0, 0.8))
    caja(azul(), 0, -6, Z - 0.4, 7.3, 60, 0.6)
    for s in (-1, 1):
        o = caja(blanco(), s * 16, -2, Z - 1.2, 28, 7, 0.7); o.rotation_euler = (0, s * -0.08, s * -0.35)
        for k in (8, 15):
            cil(mat('motor_747', 0xd0d4d8, 0.4), s * k, -6, Z - 3.2, 1.2, 4.5, 16, eje='Y')
        o = caja(blanco(), s * 6, 22, Z + 0.5, 10, 4, 0.5); o.rotation_euler = (0, 0, s * -0.3)
    caja(blanco(), 0, 22, Z + 3, 0.6, 6, 10)
    texto(azul(), 'NASA', 0, 23, Z + 7, tam=1.6, prof=0.05).rotation_euler = (math.pi / 2, 0, math.pi / 2)
    for k in range(12):
        caja(mat('ventanillas', 0x2c3440, 0.3), 3.55, -32 + k * 4, Z + 1.0, 0.1, 1.2, 0.6)
    # El transbordador encima: el morro negro, la panza negra y la cola.
    S = Z + 6
    cil(blanco(), 0, -4, S, 2.4, 30, 24, eje='Y')
    esfera(negro(), 0, -20, S, 2.4, 3, esc=(1, 1.6, 1))
    caja(negro(), 0, -4, S - 2.4, 4.4, 30, 0.6)
    for s in (-1, 1):
        o = caja(blanco(), s * 6, 4, S - 1.2, 9, 14, 0.5); o.rotation_euler = (0, 0, s * 0.25)
        caja(negro(), s * 6, 4, S - 1.5, 9, 14, 0.2)
    caja(blanco(), 0, 9, S + 2, 0.5, 6, 7)
    texto(mat('letras_ip', 0x1b1c20, 0.4), 'INDEPENDENCE', 2.45, -6, S + 0.6, tam=0.9, prof=0.04).rotation_euler = (math.pi / 2, 0, math.pi / 2)
    caja(mat('suelo_ip', 0xc8ccd0, 0.7), 0, -6, 0, 30, 70, 0.3)

def hangar_luna():
    """El hangar de la Luna del Space Center (momento estrella). Por dentro:
    el suelo lunar gris con cráteres, el módulo lunar, banderas, rocas y las
    paredes y el techo pintados de noche, con estrellas y la Tierra. Cruza la
    calle: el origen en el centro, la calle a lo largo de y."""
    L = 420
    caja(gris_l(), 0, 0, -0.3, 60, L, 0.3)
    import random
    r = random.Random(4)
    for k in range(70):                                   # cráteres
        x = r.choice((-1, 1)) * r.uniform(5, 26)
        y = r.uniform(-L / 2 + 10, L / 2 - 10)
        rr = r.uniform(1.2, 4)
        cil(gris_o(), x, y, -0.02, rr, 0.06, 18)
        cil(gris_l(), x, y, -0.02, rr * 0.75, 0.08, 18)
    for k in range(40):
        roca_lunar_suelta(r.choice((-1, 1)) * r.uniform(6, 26), r.uniform(-L / 2 + 6, L / 2 - 6), r.uniform(0.4, 1.4))
    # Las paredes y el techo: noche con estrellas (puntos claros).
    noche = mat('noche_hangar', 0x0e1426, 0.9)
    for s in (-1, 1):
        caja(noche, s * 30, 0, 0, 1, L, 22)
    caja(noche, 0, 0, 22, 61, L, 1)
    estrella = luz('estrellas_hangar', 0xf4f6ff, 1.2)
    for k in range(260):
        s = r.choice((-1, 1))
        if r.random() < 0.6:
            esfera(estrella, s * 29.4, r.uniform(-L / 2, L / 2), r.uniform(4, 21), r.uniform(0.06, 0.16), 1)
        else:
            esfera(estrella, r.uniform(-28, 28), r.uniform(-L / 2, L / 2), 21.4, r.uniform(0.06, 0.16), 1)
    for (y, s) in ((-120, 1), (60, -1)):                  # la Tierra pintada
        cil(mat('tierra_azul', 0x2f6fc8, 0.4), s * 29.3, y, 14, 4.5, 0.2, 32, eje='X')
        for (dy, dz, rr) in ((-1.5, 1, 1.6), (1.2, -1, 1.3), (0.5, 2.2, 0.9)):
            cil(mat('tierra_verde', 0x4f9a4a, 0.5), s * 29.1, y + dy, 14 + dz, rr, 0.2, 16, eje='X')
    # El módulo lunar y banderas de Estados Unidos.
    for (x, y) in ((-16, -60), (17, 110)):
        modulo_lunar(x, y)
    for (x, y) in ((-10, -150), (12, -10), (-12, 150)):
        cil(acero(), x, y, 0, 0.06, 4, 6)
        caja(azul(), x + 0.6, y, 3.2, 1.2, 0.03, 0.7)
        for k in range(4):
            caja(rojo() if k % 2 == 0 else blanco(), x + 1.25 + 0.3, y, 2.55 + k * 0.17, 1.9 if k > 1 else 0.6, 0.03, 0.15)
    texto(mat('letras_hangar', 0xf2f2ee, 0.5), 'MOON MISSION · SPACE CENTER HOUSTON', 0, -L / 2 + 0.6, 15, tam=1.6, prof=0.08)

def roca_lunar_suelta(x, y, r):
    esfera(gris_o(), x, y, r * 0.3, r, 2, esc=(1.2, 1, 0.7))

def modulo_lunar(x, y):
    oro_ = oro()
    caja(oro_, x, y, 1.6, 3.4, 3.4, 1.6)
    for (dx, dy) in ((-2.2, -2.2), (2.2, -2.2), (-2.2, 2.2), (2.2, 2.2)):
        rama(acero(), (x + dx * 0.6, y + dy * 0.6, 2), (x + dx, y + dy, 0.1), 0.08, 0.08, 6)
        cil(acero(), x + dx, y + dy, 0, 0.4, 0.1, 10)
    caja(mat('modulo_gris', 0xc8ccd0, 0.4), x, y, 3.2, 2.8, 2.8, 2.2)
    esfera(mat('modulo_gris', 0xc8ccd0, 0.4), x, y, 5.6, 0.6, 2)

# ================================================================ obstáculos
def cybertruck():
    """El Cybertruck de Elon (lo tira desde su nave): todo planchas de acero
    en ángulo, la luz de delante de lado a lado (mira a -y)."""
    perfil = [(-1.2, 0.35), (1.2, 0.35), (1.25, 0.95), (0.1, 1.85), (-1.25, 1.2), (-1.25, 0.95)]
    me = bpy.data.meshes.new('cyber')
    bm = bmesh.new()
    a = [bm.verts.new((-0.95, -y, z)) for (y, z) in perfil]
    b = [bm.verts.new((0.95, -y, z)) for (y, z) in perfil]
    bm.faces.new(a); bm.faces.new(list(reversed(b)))
    for i in range(len(perfil)):
        j = (i + 1) % len(perfil)
        bm.faces.new((a[i], a[j], b[j], b[i]))
    bm.normal_update(); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new('cyber', me); bpy.context.collection.objects.link(o); _poner(o, inox())
    caja(luz('luz_cyber', 0xf2f6ff, 1.0), 0, -1.27, 0.95, 1.8, 0.04, 0.08)
    caja(mat('cristal_cyber', 0x2c3440, 0.2), 0, -0.55, 1.42, 1.7, 0.9, 0.06).rotation_euler = (0.68, 0, 0)
    for (x, y) in ((-0.9, -0.85), (0.9, -0.85), (-0.9, 0.85), (0.9, 0.85)):
        cil(mat('rueda_cyber', 0x1e1e22, 0.85), x, y, 0.38, 0.38, 0.28, 16, eje='X')
    texto(negro(), 'X', 0, -1.3, 1.25, tam=0.35, prof=0.02)

def starship():
    """La nave de Elon (de adorno: flota en el cielo mientras te persigue):
    acero brillante, las aletas y la X."""
    cil(inox(), 0, 0, 0, 1.5, 9, 24)
    cil(inox(), 0, 0, 9, 1.5, 3.2, 24, r2=0.25)
    for k in range(4):
        a = k * math.pi / 2 + math.pi / 4
        o = caja(mat('aleta_ss', 0x8a8e92, 0.3), math.cos(a) * 1.9, math.sin(a) * 1.9, 0.3, 1.6, 0.15, 2.6); o.rotation_euler = (0, 0, a)
    for k in range(3):
        cil(mat('llama_ss', 0xffa030, 0.3), (k - 1) * 0.6, 0, -1.6, 0.35, 1.6, 10, r2=0.05)
    texto(negro(), 'X', 0, -1.52, 6, tam=1.2, prof=0.04)

def rover_lunar():
    """El vehículo lunar (se salta con la gravedad de la Luna)."""
    caja(acero(), 0, 0, 0.8, 1.8, 3.0, 0.15)
    for (x, y) in ((-1.0, -1.1), (1.0, -1.1), (-1.0, 1.1), (1.0, 1.1)):
        cil(mat('rueda_rover', 0x6a6a6e, 0.6), x, y, 0.5, 0.5, 0.3, 16, eje='X')
        caja(oro(), x, y, 0.95, 0.5, 0.9, 0.1)
    for s in (-1, 1):
        caja(mat('asiento_rover', 0x2f4a8a, 0.6), s * 0.45, 0.3, 0.95, 0.6, 0.6, 0.5)
    cil(acero(), 0.6, -1.2, 0.95, 0.04, 1.4, 6)
    o = cil(acero(), 0.6, -1.2, 2.35, 0.6, 0.06, 16, r2=0.4); o.rotation_euler = (0.5, 0, 0)

def roca_lunar():
    """La roca lunar (se salta)."""
    esfera(gris_l(), 0, 0, 0.45, 0.6, 2, esc=(1.2, 1.0, 0.8))
    esfera(gris_o(), 0.35, 0.1, 0.55, 0.35, 2)
    for k in range(4):
        cil(gris_o(), -0.3 + k * 0.2, -0.45, 0.5 + (k % 2) * 0.15, 0.08, 0.02, 8, eje='Y')

def astronauta():
    """El astronauta que cruza flotando (mira a +x), con su mochila y el casco dorado."""
    traje = mat('traje_astro', 0xf2f2ee, 0.6)
    cil(traje, 0, 0, 0.9, 0.38, 0.8, 12, r2=0.34)
    caja(mat('mochila_astro', 0xd8dce0, 0.5), -0.38, 0, 0.95, 0.3, 0.6, 0.75)
    esfera(traje, 0, 0, 1.95, 0.36, 3)
    esfera(oro(), 0.16, 0, 1.95, 0.28, 2, esc=(0.6, 0.95, 0.85))
    for s in (-1, 1):
        rama(traje, (0, s * 0.35, 1.55), (0.45, s * 0.6, 1.3), 0.12, 0.11, 8)
        rama(traje, (0, s * 0.15, 0.95), (0.15, s * 0.25, 0.25), 0.15, 0.14, 8)
        esfera(mat('bota_astro', 0xb8bcc0, 0.6), 0.2, s * 0.25, 0.15, 0.17, 2, esc=(1.4, 1, 0.8))
    caja(rojo(), 0.36, 0, 1.4, 0.04, 0.3, 0.2)
    caja(azul(), 0.36, -0.08, 1.46, 0.045, 0.12, 0.08)

def cartel_elon():
    """La pancarta de los fans de Elon (agacharse): «ELON 2028»."""
    for x in (-1.25, 1.25):
        cil(acero(), x, 0, 0, 0.07, 2.75, 8)
    caja(negro(), 0, 0, 1.55, 2.4, 0.06, 1.05)
    texto(blanco(), 'ELON', 0, -0.04, 2.2, tam=0.38, prof=0.02)
    texto(mat('letras_elon', 0x3fa8ff, 0.4), '2028', 0, -0.04, 1.78, tam=0.32, prof=0.02)

PIEZAS = {
    'bank_of_america_hou': (bank_of_america_hou, 'houston', dict(lado=1024, bisel=0.0)),
    'jpmorgan_hou':        (jpmorgan_hou,        'houston', dict(lado=1024, bisel=0.0)),
    'city_hall_hou':       (city_hall_hou,       'houston', dict(lado=1024, bisel=0.0)),
    'saturno_v':           (saturno_v,           'houston', dict(lado=1024, bisel=0.0)),
    'independence_plaza':  (independence_plaza,  'houston', dict(lado=2048, bisel=0.0)),
    'hangar_luna':         (hangar_luna,         'houston', dict(lado=2048, bisel=0.0, suelo=False)),
    'cybertruck':          (cybertruck,          'obstaculos', dict(lado=256, bisel=0.0)),
    'starship':            (starship,            'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
    'rover_lunar':         (rover_lunar,         'obstaculos', dict(lado=256, bisel=0.0)),
    'roca_lunar':          (roca_lunar,          'obstaculos', dict(lado=256, bisel=0.0)),
    'astronauta':          (astronauta,          'obstaculos', dict(lado=256, bisel=0.0)),
    'cartel_elon':         (cartel_elon,         'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
}

correr(PIEZAS)
