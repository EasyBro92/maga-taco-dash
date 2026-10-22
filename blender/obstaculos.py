# Obstáculos de la pista en dibujo animado, estilo Minion Rush (22/10/2026).
#
#   blender -b -P blender/obstaculos.py -- [pieza ...] [--rapido]
#
# Todos caben en un carril (2.2 de ancho: van de x = -0.95 a 0.95) y miran al
# jugador por -y (en el juego, +z). El origen es el centro del carril a ras de
# suelo, salvo el autobús, que lo tiene donde empieza la rampa.
#
#   Saltar:      barricada, conos
#   Deslizarse:  pancarta, globos            (lo de abajo queda libre hasta 1.1)
#   Esquivar:    guardaespaldas, furgoneta
#   Se mueve:    patrulla (viene de frente)
#   Subirse:     autobus (rampa de 2.2 y techo a 1.55 hasta 10.2 de largo)
#   Potenciador: gorra (el modo gigante)

import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import *

def blanco():  return mat('blanco', 0xffffff, 0.5)
def negro():   return mat('negro', 0x1d1f25, 0.4)
def gris():    return mat('gris', 0x9aa1aa, 0.5)
def naranja(): return mat('naranja', 0xff7a1a, 0.45)
def rojo():    return mat('rojo', 0xe8303a, 0.45)
def azul():    return mat('azul', 0x2350c8, 0.45)
def oro():     return mat('oro', 0xf2c23a, 0.3)
def cristal(): return mat('cristal', 0x3a6fb0, 0.15)
def neumatico(): return mat('neumatico', 0x1d1e21, 0.8)
def rayas(nombre, c1, c2, n, x0, ancho, eje='X'):
    return mat_franjas(nombre, c1, c2, n, eje=eje, z0=x0, alto=ancho)

def rueda(x, y, r=0.3, ancho=0.22):
    cil(neumatico(), x, y, r, r, ancho, 16, eje='X')
    cil(mat('llanta', 0xd3d6da, 0.3), x + (0.12 if x > 0 else -0.12), y, r, r * 0.5, 0.02, 12, eje='X')


# ---------------------------------------------------------------- saltar
def barricada():
    """Caballetes con dos tablas rayadas y la luz ámbar encima."""
    for s in (-1, 1):
        x = s * 0.82
        for dy in (-1, 1):
            caja(naranja(), x, dy * 0.12, 0, 0.09, 0.07, 0.82, inclina=dy * 0.28)
    tabla = rayas('rayas_barricada', 0xff7a1a, 0xffffff, 10, -0.95, 1.9)
    caja(tabla, 0, -0.04, 0.52, 1.9, 0.06, 0.24)
    caja(tabla, 0, -0.04, 0.16, 1.9, 0.06, 0.18)
    caja(negro(), -0.82, -0.04, 0.76, 0.16, 0.12, 0.06)
    esfera(mat('ambar', 0xffc21a, 0.2), -0.82, -0.04, 0.9, 0.1, 2)

def conos():
    """Tres conos con una barra rayada encima."""
    for x in (-0.72, 0, 0.72):
        caja(naranja(), x, 0, 0, 0.42, 0.42, 0.06)
        cil(naranja(), x, 0, 0.06, 0.17, 0.62, 16, r2=0.035)
        for z, r in ((0.3, 0.12), (0.47, 0.085)):
            cil(blanco(), x, 0, z, r + 0.008, 0.07, 16, r2=r - 0.008)
    caja(rayas('rayas_barra', 0xe8303a, 0xffffff, 8, -0.95, 1.9), 0, 0, 0.6, 1.9, 0.07, 0.07)


# ---------------------------------------------------------------- deslizarse
def pancarta():
    for s in (-1, 1):
        cil(rayas('poste_rayado', 0xffffff, 0xe8303a, 12, 0, 2.4, eje='Z'), s * 1.0, 0, 0, 0.055, 2.4, 10)
        esfera(oro(), s * 1.0, 0, 2.45, 0.09, 2)
        caja(gris(), s * 1.0, 0, 0, 0.32, 0.32, 0.08)
    caja(azul(), 0, 0, 1.15, 1.95, 0.08, 0.62)
    caja(rojo(), 0, 0, 1.08, 2.0, 0.1, 0.1)
    caja(rojo(), 0, 0, 1.73, 2.0, 0.1, 0.1)
    texto(blanco(), 'MAGA', 0, -0.04, 1.45, tam=0.44, prof=0.05)
    for k in range(9):                                                  # banderines debajo
        c = (rojo(), blanco(), azul())[k % 3]
        x = -0.9 + k * 0.225
        cil(c, x, 0, 0.93, 0.08, 0.15, 3, r2=0.0)

def globos():
    colores = (rojo(), blanco(), azul())
    k = 0
    for s in (-1, 1):                                                   # columnas a los lados
        for i in range(7):
            esfera(colores[k % 3], s * 0.93, 0, 0.2 + i * 0.3, 0.17, 2, esc=(1, 1, 1.15)); k += 1
    for i in range(9):                                                  # guirnalda de arriba
        x = -0.8 + i * 0.2
        z = 1.45 + 0.35 * math.sin(i / 8 * math.pi)
        esfera(colores[k % 3], x, 0, z, 0.19, 2, esc=(1, 1, 1.15)); k += 1
        esfera(colores[(k + 1) % 3], x + 0.1, -0.05, z - 0.22, 0.14, 2); k += 1
    for s in (-1, 1):
        caja(gris(), s * 0.93, 0, 0, 0.36, 0.36, 0.1)


# ---------------------------------------------------------------- esquivar
def guardaespaldas():
    traje = mat('traje_guarda', 0x23252d, 0.5)
    piel = mat('piel_guarda', 0xe8a77a, 0.6)
    # el atril presidencial delante
    caja(azul(), -0.42, -0.35, 0, 0.75, 0.5, 1.05)
    caja(azul(), -0.42, -0.42, 1.0, 0.85, 0.6, 0.08, inclina=-0.25)
    cil(oro(), -0.42, -0.62, 0.62, 0.18, 0.03, 20, eje='Y')
    cil(gris(), -0.25, -0.5, 1.05, 0.015, 0.3, 6)
    esfera(negro(), -0.25, -0.55, 1.36, 0.05, 1)
    # el guardaespaldas: armario de traje negro con los brazos cruzados
    x = 0.42
    for s in (-1, 1):
        cil(traje, x + s * 0.15, 0, 0, 0.11, 0.85, 10)
        caja(negro(), x + s * 0.15, -0.06, 0, 0.18, 0.32, 0.1)
    cil(traje, x, 0, 0.8, 0.36, 0.95, 16, r2=0.44)
    esfera(traje, x, 0, 1.75, 0.44, 2, esc=(1, 0.75, 0.45))
    caja(blanco(), x, -0.3, 1.45, 0.14, 0.05, 0.38)                    # camisa
    caja(negro(), x, -0.33, 1.4, 0.06, 0.03, 0.4)                       # corbata
    for s in (-1, 1):                                                   # brazos cruzados
        rama(traje, (x + s * 0.4, -0.05, 1.65), (x - s * 0.15, -0.38, 1.25), 0.11, 0.1, 10)
        esfera(piel, x - s * 0.2, -0.4, 1.24, 0.08, 2)
    cil(piel, x, 0, 1.85, 0.11, 0.12, 12)
    esfera(piel, x, 0, 2.08, 0.2, 2, esc=(1, 0.95, 1.1))                # cabeza pequeña
    caja(negro(), x, -0.17, 2.1, 0.32, 0.06, 0.08)                      # gafas de sol
    rama(mat('cable', 0xe8e8e8, 0.4), (x + 0.2, 0, 2.05), (x + 0.25, 0.05, 1.8), 0.012, 0.012, 4)
    esfera(negro(), x, 0.04, 2.2, 0.17, 2, esc=(1, 1, 0.5))             # pelo rapado

def furgoneta():
    """Furgoneta de la prensa: «NEWS» y antena parabólica."""
    W, L, H = 1.7, 2.6, 1.75
    caja(blanco(), 0, L / 2, 0.3, W, L, H - 0.3)
    caja(rojo(), 0, L / 2, 0.75, W + 0.02, L + 0.02, 0.18)
    caja(cristal(), 0, -0.01, 1.1, W - 0.25, 0.04, 0.5)                 # parabrisas
    caja(gris(), 0, -0.02, 0.38, W - 0.3, 0.04, 0.22)                   # rejilla
    for s in (-1, 1):
        caja(mat('faro', 0xfff3c4, 0.2), s * 0.62, -0.03, 0.45, 0.25, 0.04, 0.14)
        rueda(s * 0.78, 0.45, 0.3)
        rueda(s * 0.78, L - 0.45, 0.3)
    caja(negro(), 0, -0.05, 0.3, W + 0.05, 0.1, 0.12)                   # parachoques
    for s in (-1, 1):                                                   # el letrero en los lados
        caja(azul(), s * (W / 2 + 0.01), L / 2 + 0.2, 1.05, 0.02, 1.5, 0.42)
    texto(blanco(), 'NEWS', 0, -0.03, 1.5, tam=0.3, prof=0.03)
    cil(gris(), 0, L * 0.6, H, 0.05, 0.35, 8)
    o = cil(mat('parabolica', 0xf0f0f0, 0.4), 0, L * 0.6 - 0.1, H + 0.55, 0.42, 0.12, 20, r2=0.1)
    o.rotation_euler = (math.radians(-55), 0, 0)
    cil(gris(), 0, L * 0.6 - 0.35, H + 0.75, 0.025, 0.25, 6, r2=0.01)


# ---------------------------------------------------------------- se mueve
def patrulla():
    """Coche de policía de frente (el morro hacia el jugador)."""
    W, L = 1.5, 2.6
    caja(negro(), 0, L / 2, 0.25, W, L, 0.45)
    caja(blanco(), 0, L / 2 + 0.05, 0.42, W + 0.02, L * 0.55, 0.3)      # puertas blancas
    caja(negro(), 0, L / 2 + 0.15, 0.7, W - 0.1, L * 0.55, 0.42)
    caja(cristal(), 0, L / 2 - 0.45, 0.74, W - 0.15, 0.1, 0.34, inclina=-0.5)
    caja(cristal(), 0, L / 2 + 0.15, 0.74, W - 0.06, L * 0.5, 0.3)
    caja(negro(), 0, L / 2 + 0.15, 1.08, W - 0.1, L * 0.5, 0.06)
    caja(gris(), 0, L / 2 + 0.1, 1.14, W - 0.3, 0.32, 0.08)             # la sirena (las luces van aparte)
    for s in (-1, 1):
        caja(mat('faro', 0xfff3c4, 0.2), s * 0.52, -0.02, 0.42, 0.3, 0.04, 0.14)
        rueda(s * 0.66, 0.5, 0.28, 0.2)
        rueda(s * 0.66, L - 0.5, 0.28, 0.2)
    caja(gris(), 0, -0.04, 0.22, W + 0.05, 0.1, 0.14)
    caja(gris(), 0, -0.05, 0.36, 0.5, 0.04, 0.12)                       # rejilla
    caja(mat('escudo_policia', 0xf2c23a, 0.3), 0.0, L / 2, 0.55, W + 0.04, 0.35, 0.22)


# ---------------------------------------------------------------- subirse
def autobus():
    """Autobús de campaña con rampa trasera: se sube corriendo y se va por el techo."""
    W, L, H, R = 2.0, 8.0, 1.55, 2.2
    y0 = R
    # rampa amarilla y negra
    me = bpy.data.meshes.new('rampa')
    bm = bmesh.new()
    pts = []
    for x in (-W / 2 + 0.05, W / 2 - 0.05):
        pts.append([bm.verts.new((x, 0, 0)), bm.verts.new((x, y0, 0)), bm.verts.new((x, y0, H))])
    a, b = pts
    bm.faces.new(a); bm.faces.new(b[::-1])
    for i in range(3):
        j = (i + 1) % 3
        bm.faces.new((a[j], a[i], b[i], b[j]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new('rampa', me)
    bpy.context.scene.collection.objects.link(o)
    from comun import _poner
    _poner(o, rayas('rampa_rayas', 0xffd21a, 0x1d1f25, 9, 0, y0, eje='Y'))
    # carrocería con los colores de la bandera
    caja(blanco(), 0, y0 + L / 2, 0.35, W, L, H - 0.35)
    caja(azul(), 0, y0 + L / 2, 0.35, W + 0.02, L + 0.02, 0.35)
    caja(rojo(), 0, y0 + L / 2, 0.72, W + 0.03, L + 0.03, 0.08)
    caja(mat('techo_bus', 0xdfe3ea, 0.6), 0, y0 + L / 2, H - 0.04, W - 0.06, L - 0.06, 0.06)
    for s in (-1, 1):
        for k in range(6):                                              # ventanillas
            caja(cristal(), s * (W / 2 + 0.01), y0 + 0.9 + k * 1.2, 0.85, 0.02, 0.95, 0.5)
        caja(azul(), s * (W / 2 + 0.02), y0 + L / 2 + 0.6, 0.38, 0.02, 3.5, 0.3)
        rueda(s * (W / 2 - 0.12), y0 + 1.2, 0.36, 0.25)
        rueda(s * (W / 2 - 0.12), y0 + L - 1.4, 0.36, 0.25)
    for s in (-1, 1):                                                   # luces de atrás
        caja(mat('piloto', 0xc0262c, 0.3), s * 0.75, y0 - 0.01, 0.5, 0.25, 0.04, 0.3)
    texto(blanco(), 'MAGA TOUR', 0, y0 - 0.02, 1.15, tam=0.24, prof=0.03)
    # banderitas en el borde del techo
    for k in range(9):
        c = (rojo(), blanco(), azul())[k % 3]
        cil(c, -W / 2 + 0.06, y0 + 0.5 + k * 0.85, H, 0.07, 0.14, 3, r2=0.0)
        cil(c, W / 2 - 0.06, y0 + 0.5 + k * 0.85, H, 0.07, 0.14, 3, r2=0.0)


# ---------------------------------------------------------------- potenciador
def gorra():
    """Gorra roja de campaña: activa el modo gigante."""
    cupula(rojo(), 0, 0, 0, 0.3, 0.26, lados=24, aros=6)
    o = cil(rojo(), 0, -0.32, 0.02, 0.24, 0.03, 20)
    o.scale = (1.0, 0.75, 1.0)
    caja(blanco(), 0, -0.24, 0.1, 0.32, 0.04, 0.12, inclina=0.5)
    cil(blanco(), 0, -0.27, 0.16, 0.05, 0.02, 5, eje='Y')               # estrella
    esfera(rojo(), 0, 0, 0.26, 0.04, 1)


PIEZAS = {
    'barricada':      (barricada,      'obstaculos', dict(lado=512)),
    'conos':          (conos,          'obstaculos', dict(lado=512)),
    'pancarta':       (pancarta,       'obstaculos', dict(lado=512)),
    'globos':         (globos,         'obstaculos', dict(lado=512, bisel=0.0)),
    'guardaespaldas': (guardaespaldas, 'obstaculos', dict(lado=512)),
    'furgoneta':      (furgoneta,      'obstaculos', dict(lado=512)),
    'patrulla':       (patrulla,       'obstaculos', dict(lado=512)),
    'autobus':        (autobus,        'obstaculos', dict(lado=1024)),
    'gorra':          (gorra,          'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
}

correr(PIEZAS)
