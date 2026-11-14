# Nivel 21: Birmingham, Alabama (13/11/2026).
#
#   blender -b -P blender/birmingham.py -- [pieza ...] [--rapido]
#
# Historia: «Un huracán que solo existe porque lo pintó él con un rotulador
# en el mapa (pasó de verdad)».
#   Por 20th Street (el cartel de «The Magic City», el teatro Alabama con su
#   letrero vertical, los hornos Sloss) mientras un rotulador gigante va
#   pintando muros de tinta en la calle; dentro de la fundición Sloss el
#   martinete manda ondas de hierro al rojo por el suelo; y se llega a la
#   estatua de Vulcano en lo alto de su torre.
# Obstáculos (carpeta obstaculos): el rotulador, el muro de tinta, la onda de
# choque, los lingotes, la vagoneta de mineral, el gancho de la grúa y la
# pancarta del huracán.

import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import *
from comun import _poner

def blanco():   return mat('blanco_bh', 0xf4f0e8, 0.5)
def negro():    return mat('negro_bh', 0x1b1c20, 0.4)
def tinta():    return mat('tinta_bh', 0x0c0c10, 0.12)
def hierro():   return mat('hierro_bh', 0x3a3e44, 0.5)
def oxido():    return mat('oxido_bh', 0x7a4a32, 0.85)
def rojo():     return mat('rojo_bh', 0xc8282c, 0.45)
def oro():      return mat('oro_bh', 0xe8b840, 0.25)
def verde():    return mat('verde_bh', 0x3f7a32, 0.85)
def arenisca(): return mat_bloques('arenisca_bh', 0xc8a878, 0xa88a5e, ancho=1.6, alto=0.8)
def ladrillo(): return mat_bloques('ladrillo_bh', 0x8a4a3a, 0x6a3a2e, ancho=0.5, alto=0.22)
def brasa(f=1.6): return luz('brasa_bh', 0xff7a1a, f)

# ================================================================ edificios
def vulcano():
    """Vulcano (la meta): la estatua de hierro más grande del mundo, en lo
    alto de su torre de arenisca en Red Mountain: levanta la punta de lanza
    con la derecha y apoya el martillo en el yunque con la izquierda."""
    Y = 24
    # La colina verde y la torre con su mirador.
    esfera(verde(), 0, Y, -6, 26, 2, esc=(1, 0.8, 0.35))
    a = arenisca()
    caja(a, 0, Y, 0, 10, 10, 30)
    caja(a, 0, Y, 0, 13, 13, 3)
    for k in range(6):
        caja(mat('ventana_torre', 0x2a2a2e, 0.4), 0, Y - 5.02, 4 + k * 4, 1.2, 0.05, 2.2)
    caja(a, 0, Y, 30, 13, 13, 1.2)
    for k in range(16):
        ang = k * math.tau / 16
        cil(hierro(), math.cos(ang) * 6.2, Y + math.sin(ang) * 6.2, 31.2, 0.06, 1.2, 4)
    caja(a, 0, Y, 31.2, 6, 6, 2)
    # La estatua (Z0 = los pies).
    H, Z0 = hierro(), 33.2
    for s in (-1, 1):
        rama(H, (s * 0.9, Y, Z0), (s * 0.8, Y, Z0 + 5.5), 0.75, 0.85, 10)          # piernas
        caja(H, s * 0.9, Y - 0.4, Z0, 1.0, 1.8, 0.6)                                 # pies (sandalias)
    caja(mat('delantal_bh', 0x34363a, 0.7), 0, Y - 0.8, Z0 + 3.2, 2.6, 0.3, 3.0)     # el delantal de herrero
    rama(H, (0, Y, Z0 + 5.4), (0, Y, Z0 + 9.6), 1.5, 1.7, 12)                         # el torso
    esfera(H, 0, Y, Z0 + 10.4, 1.6, 2, esc=(1.25, 0.9, 0.6))                          # hombros
    rama(H, (0, Y, Z0 + 10.8), (0, Y, Z0 + 11.6), 0.5, 0.5, 8)                        # cuello
    esfera(H, 0, Y, Z0 + 12.5, 1.0, 2)                                                # cabeza
    esfera(H, 0, Y - 0.5, Z0 + 11.9, 0.75, 2, esc=(1, 0.8, 0.9))                      # barba
    # Brazo derecho arriba con la punta de lanza.
    rama(H, (1.7, Y, Z0 + 10.6), (2.6, Y - 0.3, Z0 + 13.6), 0.55, 0.45, 8)
    rama(H, (2.6, Y - 0.3, Z0 + 13.6), (3.0, Y - 0.4, Z0 + 16.4), 0.45, 0.4, 8)
    cil(H, 3.05, Y - 0.4, Z0 + 16.4, 0.12, 2.2, 6)
    cil(H, 3.05, Y - 0.4, Z0 + 18.6, 0.45, 1.6, 4, r2=0.02)
    # Brazo izquierdo abajo con el martillo sobre el yunque.
    rama(H, (-1.7, Y, Z0 + 10.6), (-2.4, Y, Z0 + 7.6), 0.55, 0.45, 8)
    rama(H, (-2.4, Y, Z0 + 7.6), (-2.7, Y - 0.6, Z0 + 5.4), 0.45, 0.4, 8)
    cil(H, -2.8, Y - 0.6, Z0 + 3.0, 0.12, 2.6, 6)
    caja(H, -2.8, Y - 0.6, Z0 + 2.4, 1.4, 0.7, 0.7)
    caja(H, -3.2, Y - 0.2, Z0, 1.6, 1.2, 1.4)                                         # el yunque
    caja(H, -3.2, Y - 0.2, Z0 + 1.4, 2.2, 1.0, 0.4)
    texto(mat('letras_vul', 0x5a4a3a, 0.5), 'VULCAN', 0, Y - 6.6, 1.0, tam=1.4, prof=0.06)

def sloss_hornos():
    """Los hornos Sloss: dos altos hornos oxidados, las cuatro chimeneas de
    ladrillo, las tuberías y la nave de chapa con su letrero."""
    Y = 18
    o = oxido()
    for x in (-10, 6):
        cil(o, x, Y, 0, 4.2, 20, 20)
        cil(o, x, Y, 20, 4.2, 4, 20, r2=1.8)
        cil(o, x, Y, 24, 1.8, 6, 12)
        for k in range(5):
            cil(hierro(), x, Y, 2 + k * 4, 4.35, 0.3, 20)
    for k, x in enumerate((-20, -16, 14, 18)):
        cil(ladrillo(), x, Y + 6, 0, 1.4, 34 - (k % 2) * 4, 12, r2=1.1)
    rama(o, (-10, Y - 2, 26), (6, Y - 2, 26), 1.0, 1.0, 10)
    rama(o, (6, Y - 2, 26), (14, Y + 4, 18), 0.9, 0.9, 10)
    rama(o, (-10, Y + 2, 26), (-16, Y + 6, 20), 0.9, 0.9, 10)
    for x in (-18, 12):
        rama(hierro(), (x, Y - 6, 0), (x, Y - 6, 12), 0.5, 0.5, 8)
    caja(mat('chapa_bh', 0x6a6e72, 0.7), 0, Y - 8, 0, 40, 8, 7)
    tejado(mat('chapa_bh', 0x6a6e72, 0.7), 0, Y - 12, Y - 4, 7, 41, 2.5, cumbrera='x')
    caja(negro(), 0, Y - 12.1, 7.6, 18, 0.3, 2.2)
    texto(mat('letras_sloss', 0xf0e6d0, 0.5), 'SLOSS FURNACES', 0, Y - 12.3, 8.1, tam=1.2, prof=0.05)
    for x in (-14, -5, 5, 14):
        caja(brasa(1.2), x, Y - 12.05, 0, 3, 0.1, 3.5)

def alabama_theatre():
    """El teatro Alabama (1927): fachada de terracota, el gran ventanal en
    arco, la marquesina de bombillas y el letrero vertical ALABAMA."""
    Y = 8
    t = mat_bloques('terracota_bh', 0xe8d8b8, 0xd0bc98, ancho=1.2, alto=0.6)
    caja(t, 0, Y, 0, 22, 14, 18)
    caja(mat('cornisa_bh', 0xd8c49c, 0.6), 0, Y - 7.2, 18, 22.6, 0.8, 1)
    cil(mat('ventanal_bh', 0x3a4a5a, 0.2), 0, Y - 7.05, 9.5, 4.5, 0.1, 24, eje='Y')
    caja(mat('ventanal_bh', 0x3a4a5a, 0.2), 0, Y - 7.05, 5, 9, 0.1, 4.5)
    for x in (-8, 8):
        for z in (6, 11, 15):
            ventana(x, z, 1.6, 2.4, y=Y - 7, marco=blanco(), cristal=mat('cristal_bh', 0x2a3a4a, 0.2))
    # La marquesina.
    caja(negro(), 0, Y - 9, 3.6, 16, 4, 0.4)
    caja(mat('marquesina_bh', 0xf2e2b0, 0.4), 0, Y - 11, 3.0, 16, 0.3, 1.6)
    texto(rojo(), 'ALABAMA', 0, Y - 11.2, 3.35, tam=0.9, prof=0.05)
    bomb = luz('bombilla_bh', 0xffe08a, 1.6)
    for k in range(26):
        esfera(bomb, -7.8 + k * 0.62, Y - 11.25, 4.5, 0.09, 1)
        esfera(bomb, -7.8 + k * 0.62, Y - 11.25, 2.95, 0.09, 1)
    # El letrero vertical, saliendo de la fachada.
    caja(rojo(), 0, Y - 9.4, 6, 0.6, 4.2, 12)
    neon = luz('neon_alabama', 0xffd060, 1.8)
    for k, letra in enumerate('ALABAMA'):
        for s in (-1, 1):
            o = texto(neon, letra, s * 0.32, Y - 9.4, 16.2 - k * 1.6, tam=1.3, prof=0.05)
            o.rotation_euler = (math.pi / 2, 0, s * math.pi / 2)
    caja(mat('puertas_bh', 0x5a2a1e, 0.6), 0, Y - 7.05, 0, 8, 0.1, 2.8)

# ================================================================ cruzan la calle
def magic_city():
    """El cartel de bienvenida sobre la calle: «BIRMINGHAM, THE MAGIC CITY»,
    de hierro con bombillas, como el de la estación."""
    for s in (-1, 1):
        caja(hierro(), s * 9, 0, 0, 0.6, 0.6, 9)
        for z in (2, 4, 6):
            rama(hierro(), (s * 9, 0, z), (s * 9, 0, z + 2), 0.08, 0.08, 4)
    caja(hierro(), 0, 0, 6.2, 18.6, 0.5, 0.4)
    caja(hierro(), 0, 0, 8.6, 18.6, 0.5, 0.4)
    caja(negro(), 0, 0, 6.6, 17, 0.3, 2.0)
    bomb = luz('bombilla_mc', 0xffe08a, 1.8)
    texto(bomb, 'THE MAGIC CITY', 0, -0.2, 7.0, tam=1.1, prof=0.06)
    texto(blanco(), 'BIRMINGHAM', 0, -0.2, 9.1, tam=0.8, prof=0.06)
    o = texto(bomb, 'THE MAGIC CITY', 0, 0.2, 7.0, tam=1.1, prof=0.06); o.rotation_euler = (math.pi / 2, 0, math.pi)
    for k in range(30):
        esfera(bomb, -8.4 + k * 0.58, -0.22, 6.5, 0.07, 1)

def fundicion():
    """La fundición Sloss por dentro (momento estrella): la nave de hierro a
    oscuras, los canales de hierro fundido a los lados, las bocas de los
    hornos que brillan, las tuberías y las cerchas del techo. Cruza la calle:
    el origen en el centro y la calle a lo largo de y."""
    L = 420
    caja(mat('suelo_fund', 0x3a3836, 0.85), 0, 0, -0.2, 26, L, 0.2)
    for k in range(int(L / 3)):                               # chapas del suelo
        caja(mat('junta_fund', 0x2a2826, 0.9), 0, -L / 2 + k * 3, -0.005, 7.6, 0.06, 0.01)
    lad = ladrillo()
    for s in (-1, 1):
        caja(lad, s * 12, 0, 0, 2, L, 14)
        # El canal de hierro fundido junto a la calle.
        caja(hierro(), s * 6.3, 0, 0, 0.3, L, 0.4)
        caja(brasa(2.0), s * 7.4, 0, 0.05, 1.8, L, 0.1)
        caja(hierro(), s * 8.5, 0, 0, 0.3, L, 0.4)
        # Tuberías a lo largo de la pared.
        for z in (5, 7):
            cil(oxido(), s * 10.6, 0, z, 0.5, L, 12, eje='Y')
        # Las bocas de los hornos, cada 30 m.
        for k in range(int(L / 30)):
            y = -L / 2 + 15 + k * 30
            cil(oxido(), s * 11, y, 0, 3.2, 9, 16)
            caja(brasa(2.2), s * 9.4, y, 1.0, 0.2, 2.2, 2.6)
            caja(hierro(), s * 9.5, y, 3.6, 0.6, 2.8, 0.4)
    # Las cerchas y el techo.
    for k in range(int(L / 10)):
        y = -L / 2 + k * 10
        caja(hierro(), 0, y, 13.4, 24, 0.4, 0.6)
        for s in (-1, 1):
            rama(hierro(), (s * 11, y, 13.4), (0, y, 15.5), 0.15, 0.15, 4)
    caja(mat('techo_fund', 0x1e1c1a, 0.9), 0, 0, 15.6, 26, L, 0.3)
    for (y, txt) in ((-L / 2 + 0.6, 'SLOSS FURNACES'), (L / 2 - 0.6, 'MIND THE HAMMER')):
        caja(negro(), 0, y, 9, 12, 0.3, 1.6)
        texto(oro(), txt, 0, y - 0.2, 9.3, tam=0.9, prof=0.05)

# ================================================================ obstáculos
def rotulador():
    """El rotulador gigante con el que pintó el huracán: negro, la tapa
    quitada, la banda blanca y la punta de fieltro (vuela pintando)."""
    o = cil(negro(), 0, 0, 0, 0.34, 3.0, 16)
    cil(blanco(), 0, 0, 1.6, 0.35, 0.5, 16)
    texto(negro(), 'PERMANENT', 0, -0.36, 1.75, tam=0.13, prof=0.01)
    cil(mat('gris_rot', 0x6a6e72, 0.4), 0, 0, -0.35, 0.3, 0.35, 16)
    cil(tinta(), 0, 0, -0.85, 0.04, 0.5, 12, r2=0.16)
    cil(negro(), 0, 0, 3.0, 0.3, 0.25, 16, r2=0.22)

def trazo_tinta():
    """El muro de tinta que deja el rotulador: un trazo grueso y brillante de
    lado a lado del carril, con chorretones (no se pasa)."""
    t = tinta()
    caja(t, 0, 0, 0, 2.0, 0.5, 1.7)
    cil(t, 0, 0, 1.7, 0.25, 2.0, 12, eje='X')
    for x in (-1.0, 1.0):
        cil(t, x, 0, 0, 0.25, 1.95, 12)
    for (x, h) in ((-0.6, 0.5), (0.1, 0.8), (0.7, 0.35)):
        cil(t, x, -0.26, 0, 0.1, h, 8)
    esfera(t, 0, 0, 0.01, 1.3, 2, esc=(1.1, 0.7, 0.03))

def onda_choque():
    """La onda de choque del martinete: una cresta de hierro al rojo que corre
    por el suelo de lado a lado de la calle (se salta)."""
    cil(brasa(2.4), 0, 0, 0.32, 0.32, 7.0, 16, eje='X')
    cil(luz('brasa_clara', 0xffd060, 2.6), 0, 0, 0.5, 0.14, 7.1, 12, eje='X')
    for k in range(14):
        esfera(luz('chispa_bh', 0xffe08a, 2.6), -3.3 + k * 0.5, (k % 3 - 1) * 0.15, 0.7 + (k % 2) * 0.25, 0.07, 1)

def lingotes():
    """Una pila de lingotes de hierro (se salta)."""
    for fila in range(3):
        for k in range(4 - fila):
            caja(mat('lingote_bh', 0x4a4e54, 0.5), -0.6 + k * 0.4 + fila * 0.2, 0, fila * 0.28, 0.34, 1.2, 0.26)
    caja(oxido(), 0, 0, -0.01, 1.8, 1.3, 0.05)

def vagoneta_mineral():
    """La vagoneta de mineral de hierro, roja de óxido, en sus raíles (no se pasa)."""
    o = oxido()
    caja(o, 0, 0, 0.5, 1.8, 2.6, 1.3)
    caja(hierro(), 0, 0, 1.75, 1.9, 2.7, 0.1)
    esfera(mat('mineral_bh', 0x8a3a2a, 0.9), 0, 0, 1.8, 0.9, 2, esc=(1, 1.4, 0.5))
    for y in (-0.9, 0.9):
        for s in (-1, 1):
            cil(hierro(), s * 0.85, y, 0.35, 0.35, 0.15, 12, eje='X')
    for s in (-1, 1):
        caja(hierro(), s * 0.75, 0, 0, 0.1, 3.4, 0.08)

def gancho_grua():
    """El gancho de la grúa colgando de su cadena (agacharse)."""
    for k in range(10):
        o = bpy.ops.mesh.primitive_torus_add(major_radius=0.14, minor_radius=0.04, location=(0, 0, 4.6 - k * 0.24),
                                              rotation=(math.pi / 2, 0, (k % 2) * math.pi / 2))
        _poner(bpy.context.object, hierro())
    caja(mat('amarillo_bh', 0xe8b830, 0.5), 0, 0, 2.0, 2.2, 0.5, 0.5)
    caja(negro(), 0, -0.26, 2.05, 2.0, 0.02, 0.4)
    rama(hierro(), (0, 0, 2.0), (0, 0, 1.65), 0.12, 0.1, 8)
    rama(hierro(), (0, 0, 1.65), (0.35, 0, 1.45), 0.1, 0.08, 8)

def cartel_huracan():
    """La pancarta del huracán (agacharse): «ALABAMA WAS IN THE CONE!»."""
    for x in (-1.25, 1.25):
        cil(hierro(), x, 0, 0, 0.07, 2.75, 8)
    caja(blanco(), 0, 0, 1.55, 2.4, 0.06, 1.05)
    texto(rojo(), 'ALABAMA WAS', 0, -0.04, 2.25, tam=0.22, prof=0.02)
    texto(tinta(), 'IN THE CONE!', 0, -0.04, 1.88, tam=0.22, prof=0.02)

PIEZAS = {
    'vulcano':          (vulcano,          'birmingham', dict(lado=2048, segmentos=1, min_bisel=1.0)),
    'sloss_hornos':     (sloss_hornos,     'birmingham', dict(lado=2048, bisel=0.0)),
    'alabama_theatre':  (alabama_theatre,  'birmingham', dict(lado=1024, bisel=0.0)),
    'magic_city':       (magic_city,       'birmingham', dict(lado=1024, bisel=0.0, suelo=False)),
    'fundicion':        (fundicion,        'birmingham', dict(lado=2048, bisel=0.0, suelo=False)),
    'rotulador':        (rotulador,        'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
    'trazo_tinta':      (trazo_tinta,      'obstaculos', dict(lado=256, bisel=0.0)),
    'onda_choque':      (onda_choque,      'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
    'lingotes':         (lingotes,         'obstaculos', dict(lado=256, bisel=0.0)),
    'vagoneta_mineral': (vagoneta_mineral, 'obstaculos', dict(lado=256, bisel=0.0)),
    'gancho_grua':      (gancho_grua,      'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
    'cartel_huracan':   (cartel_huracan,   'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
}

correr(PIEZAS)
