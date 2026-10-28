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
    # 27/10: el techo es lo que mas se ve (desde la camara y corriendo por
    # encima): una bandera de EE. UU. en vez del gris liso.
    caja(rayas('techo_franjas', 0xe8303a, 0xffffff, 7, -W / 2, W), 0, y0 + L / 2, H - 0.04, W - 0.06, L - 0.06, 0.06)
    caja(azul(), 0, y0 + 0.9, H - 0.03, W - 0.06, 1.6, 0.06)
    for fila in range(5):
        for col in range(4):
            cil(blanco(), -0.66 + col * 0.44 + (fila % 2) * 0.22, y0 + 0.3 + fila * 0.28, H + 0.03, 0.06, 0.012, 5)
    for s in (-1, 1):
        for k in range(6):                                              # ventanillas
            caja(cristal(), s * (W / 2 + 0.01), y0 + 0.9 + k * 1.2, 0.85, 0.02, 0.95, 0.5)
        caja(azul(), s * (W / 2 + 0.02), y0 + L / 2 + 0.6, 0.38, 0.02, 3.5, 0.3)
        rueda(s * (W / 2 - 0.12), y0 + 1.2, 0.36, 0.25)
        rueda(s * (W / 2 - 0.12), y0 + L - 1.4, 0.36, 0.25)
    # 27/10: la trasera, que es lo que mas se ve (antes una pared blanca lisa
    # con la rampa: parecia una caja). Panel azul con estrellas, luna trasera,
    # franjas rojas y blancas, letrero, pilotos, matricula, parachoques y la
    # escalerilla al techo por encima de la rampa.
    caja(azul(), 0, y0 - 0.02, 0.35, W - 0.04, 0.04, H - 0.4)
    caja(rayas('franjas_bus', 0xe8303a, 0xffffff, 6, 0.35, 0.42, eje='Z'), 0, y0 - 0.04, 0.35, W - 0.1, 0.04, 0.42)
    caja(cristal(), 0, y0 - 0.045, 1.02, W - 0.5, 0.03, 0.38)            # luna trasera
    caja(gris(), 0, y0 - 0.05, 1.0, W - 0.42, 0.02, 0.04)
    for k in range(7):                                                  # estrellas a los lados de la luna
        for s in (-1, 1):
            cil(blanco(), s * (W / 2 - 0.13), y0 - 0.05, 0.9 + k * 0.08, 0.03, 0.02, 5, eje='Y')
    for s in (-1, 1):                                                   # luces de atrás
        caja(mat('piloto', 0xc0262c, 0.3), s * 0.78, y0 - 0.06, 0.82, 0.2, 0.04, 0.34)
        caja(mat('intermitente', 0xffa21a, 0.3), s * 0.78, y0 - 0.06, 0.74, 0.2, 0.04, 0.07)
    caja(mat('letrero_bus', 0xffffff, 0.4), 0, y0 - 0.06, 0.8, 1.15, 0.03, 0.17)
    texto(rojo(), 'MAGA TOUR', 0, y0 - 0.08, 0.885, tam=0.13, prof=0.02)
    caja(mat('matricula', 0xfff3c4, 0.4), 0, y0 - 0.06, 0.55, 0.42, 0.02, 0.13)
    texto(azul(), 'TACO 1', 0, y0 - 0.075, 0.615, tam=0.075, prof=0.01)
    caja(negro(), 0, y0 - 0.08, 0.3, W + 0.06, 0.12, 0.12)              # parachoques
    for s in (-1, 1):                                                   # escalerilla
        caja(gris(), s * 0.22, y0 - 0.07, 1.1, 0.03, 0.03, H - 1.1 + 0.15)
    for k in range(4):
        caja(gris(), 0, y0 - 0.07, 1.15 + k * 0.12, 0.44, 0.03, 0.025)
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


# ---------------------------------------------------------------- 22/10 (2): más Minion Rush
def rayo():
    """Pistola de rayo congelador (potenciador)."""
    hielo = mat('hielo', 0x7fe6ff, 0.2)
    caja(blanco(), 0, 0, 0, 0.22, 0.6, 0.22)                             # cuerpo
    cil(azul(), 0, -0.32, 0.11, 0.13, 0.12, 16, eje='Y')
    for k in range(3):                                                  # anillos del cañón
        cil(hielo, 0, -0.42 - k * 0.1, 0.11, 0.1 - k * 0.012, 0.05, 16, eje='Y')
    esfera(hielo, 0, -0.68, 0.11, 0.08, 2)
    caja(azul(), 0, 0.18, -0.22, 0.12, 0.18, 0.3, inclina=0.3)           # empuñadura
    esfera(hielo, 0, 0.12, 0.28, 0.1, 2)                                # depósito
    caja(gris(), 0, 0.12, 0.2, 0.1, 0.1, 0.06)

def cohete():
    """El cohete en el que se monta el personaje (punta hacia -y, que es hacia delante)."""
    cil(blanco(), 0, 0, 0.45, 0.45, 2.4, 20, eje='Y')
    cil(rojo(), 0, -1.45, 0.45, 0.46, 0.5, 20, eje='Y', r2=0.0)          # morro
    o = cil(rojo(), 0, -1.6, 0.45, 0.45, 0.9, 20, r2=0.0)
    o.rotation_euler = (math.pi / 2, 0, 0)
    cil(rojo(), 0, 0.2, 0.45, 0.47, 0.25, 20, eje='Y')                   # franja
    cil(azul(), 0, -0.5, 0.45, 0.47, 0.18, 20, eje='Y')
    for a in range(4):                                                   # aletas
        ang = a * math.pi / 2 + math.pi / 4
        caja(rojo(), math.cos(ang) * 0.55, 1.0, 0.45 + math.sin(ang) * 0.55, 0.08, 0.7, 0.5, giro=0, inclina=0)
    cil(gris(), 0, 1.3, 0.45, 0.3, 0.25, 16, eje='Y', r2=0.22)          # tobera
    o = cil(mat('fuego', 0xffa21a, 0.2), 0, 1.75, 0.45, 0.28, 0.7, 14, r2=0.0)
    o.rotation_euler = (-math.pi / 2, 0, 0)
    o = cil(mat('fuego2', 0xffe24a, 0.2), 0, 1.6, 0.45, 0.16, 0.45, 12, r2=0.0)
    o.rotation_euler = (-math.pi / 2, 0, 0)
    for s in (-1, 1):                                                    # ojo de buey
        cil(cristal(), s * 0.46, -0.6, 0.55, 0.13, 0.02, 14, eje='X')

def barril():
    """Barril de salsa que lanza el jefe: rueda hacia el jugador (eje x)."""
    cil(rojo(), 0, 0, 0.42, 0.42, 1.5, 20, eje='X')
    for x in (-0.6, 0, 0.6):
        cil(negro(), x, 0, 0.42, 0.44, 0.08, 20, eje='X')
    caja(mat('etiqueta', 0xffe24a, 0.4), 0, -0.42, 0.42, 0.7, 0.04, 0.3)
    texto(rojo(), 'SALSA', 0, -0.44, 0.42, tam=0.16, prof=0.02)
    cil(mat('llama', 0xff6a1a, 0.3), 0.3, -0.43, 0.6, 0.05, 0.02, 3, eje='Y')

def chile():
    """Chile picante: se recoge para dispararle al jefe."""
    roja = mat('chile', 0xff2a1a, 0.25)
    rama(roja, (0, 0, 0.55), (0.05, 0, 0.25), 0.16, 0.12, 14)
    rama(roja, (0.05, 0, 0.25), (-0.05, 0, 0.0), 0.12, 0.02, 12)
    esfera(roja, 0, 0, 0.55, 0.16, 2)
    verde = mat('rabito', 0x3fae3a, 0.5)
    cil(verde, 0, 0, 0.66, 0.1, 0.06, 10)
    rama(verde, (0, 0, 0.7), (0.08, 0, 0.88), 0.03, 0.02, 6)

def jefe():
    """Robot Burrito: el jefe rival. Flota con propulsores y mira al jugador."""
    tortilla = mat_bloques('tortilla', 0xf0cf8a, 0xd9a85a, ancho=0.35, alto=0.3, grosor=0.02, variacion=1.06)
    metal = mat('metal_jefe', 0x8f99a8, 0.35)
    cil(tortilla, 0, 0, 0.6, 1.1, 2.4, 24)                               # el burrito de pie
    cupula(tortilla, 0, 0, 3.0, 1.1, 0.7, lados=24, aros=6)
    for z in (1.2, 2.1):                                                 # pliegues de la tortilla
        cil(mat('pliegue', 0xd9a85a, 0.6), 0, 0, z, 1.13, 0.08, 24)
    for k, c in enumerate((0x5fd65f, 0xff4d4d, 0x8a5a34)):              # relleno asomando arriba
        esfera(mat(f'relleno{c:06x}', c, 0.7), -0.5 + k * 0.5, -0.2, 3.55, 0.3, 2)
    # cara de enfadado: ojos rojos de robot y ceño
    for s in (-1, 1):
        caja(metal, s * 0.38, -1.05, 2.25, 0.5, 0.14, 0.38)
        esfera(mat('ojo_robot', 0xff2030, 0.2), s * 0.38, -1.15, 2.25, 0.14, 2, esc=(1.4, 0.5, 1))
        caja(negro(), s * 0.38, -1.13, 2.55, 0.55, 0.08, 0.1, giro=0, inclina=0)
    caja(negro(), 0, -1.1, 1.75, 0.7, 0.06, 0.12)                        # boca
    for k in range(5):
        caja(blanco(), -0.24 + k * 0.12, -1.13, 1.73, 0.07, 0.04, 0.09)
    # brazos de robot y propulsores
    for s in (-1, 1):
        rama(metal, (s * 1.05, 0, 2.0), (s * 1.7, -0.4, 1.4), 0.12, 0.1, 10)
        esfera(metal, s * 1.7, -0.4, 1.4, 0.16, 2)
        rama(metal, (s * 1.7, -0.4, 1.4), (s * 1.6, -0.9, 2.0), 0.1, 0.09, 10)
        caja(mat('pinza', 0xff7a1a, 0.4), s * 1.6, -0.95, 2.05, 0.3, 0.2, 0.25)
        cil(metal, s * 0.6, 0.6, 0.0, 0.3, 0.8, 14, r2=0.24)
        o = cil(mat('fuego', 0xffa21a, 0.2), s * 0.6, 0.6, -0.55, 0.26, 0.6, 12, r2=0.0)
        o.rotation_euler = (math.pi, 0, 0)
    cil(metal, 0, 0, 0.35, 0.95, 0.3, 24)
    texto(mat('letra_jefe', 0xff2030, 0.3), 'BURRITO-BOT', 0, -1.12, 1.2, tam=0.22, prof=0.03)


# ---------------------------------------------------------------- 28/10: ideas de Subway Surfers
def bota(x, cuero, puntera, estrella):
    """Una bota de vaquero de pie: caña hacia arriba, puntera hacia -y."""
    caja(cuero, x, 0.02, 0.28, 0.2, 0.2, 0.42)                          # caña
    caja(puntera, x, 0.02, 0.66, 0.22, 0.22, 0.06)                      # boca de la caña
    caja(cuero, x, -0.1, 0.0, 0.2, 0.44, 0.22)                          # pie
    o = esfera(puntera, x, -0.32, 0.1, 0.11, 2, esc=(0.95, 1.5, 0.9))   # puntera
    caja(negro(), x, 0.06, -0.02, 0.2, 0.14, 0.12)                      # tacon
    caja(negro(), x, -0.12, -0.03, 0.21, 0.46, 0.04)                    # suela
    cil(estrella, x, -0.09, 0.4, 0.07, 0.03, 5, eje='Y')                # estrella en la caña
    for k in range(3):                                                   # pespuntes
        caja(puntera, x, -0.085, 0.18 + k * 0.08, 0.16, 0.01, 0.012)

def botas():
    """Botas de vaquero rojas con estrella: un rato de saltos altos."""
    cuero = mat('cuero_rojo', 0xd8262f, 0.45)
    puntera = mat('cuero_blanco', 0xf4efe6, 0.5)
    bota(-0.13, cuero, puntera, oro())
    bota(0.13, cuero, puntera, oro())
    for s in (-1, 1):                                                    # alitas doradas
        caja(oro(), s * 0.27, 0.06, 0.42, 0.14, 0.05, 0.1, giro=0, inclina=0)
        caja(oro(), s * 0.31, 0.06, 0.5, 0.12, 0.05, 0.08)

def caja_sorpresa():
    """Caja sorpresa azul con lazo rojo y blanco y una interrogación dorada."""
    azul_c = mat('caja_azul', 0x1f4fb0, 0.4)
    caja(azul_c, 0, 0, 0, 0.62, 0.62, 0.58)
    caja(azul_c, 0, 0, 0.58, 0.68, 0.68, 0.12)                          # tapa
    lazo = mat('lazo_rojo', 0xe8303a, 0.4)
    caja(lazo, 0, 0, 0, 0.14, 0.645, 0.705)
    caja(lazo, 0, 0, 0, 0.645, 0.14, 0.705)
    caja(blanco(), 0, 0, 0, 0.04, 0.65, 0.71)
    for s in (-1, 1):                                                    # el lazo de arriba
        esfera(lazo, s * 0.13, 0, 0.78, 0.11, 2, esc=(1.2, 0.5, 0.8))
    esfera(lazo, 0, 0, 0.75, 0.06, 1)
    for x in (-0.18, 0.18):                                              # una a cada lado del lazo
        texto(oro(), '?', x, -0.333, 0.3, tam=0.34, prof=0.05)


PIEZAS = {
    'rayo':           (rayo,           'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
    'cohete':         (cohete,         'obstaculos', dict(lado=512, bisel=0.0, suelo=False)),
    'barril':         (barril,         'obstaculos', dict(lado=256, bisel=0.0)),
    'chile':          (chile,          'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
    'jefe':           (jefe,           'obstaculos', dict(lado=1024, bisel=0.0, suelo=False)),
    'barricada':      (barricada,      'obstaculos', dict(lado=512)),
    'conos':          (conos,          'obstaculos', dict(lado=512)),
    'pancarta':       (pancarta,       'obstaculos', dict(lado=512)),
    'globos':         (globos,         'obstaculos', dict(lado=512, bisel=0.0)),
    'guardaespaldas': (guardaespaldas, 'obstaculos', dict(lado=512)),
    'furgoneta':      (furgoneta,      'obstaculos', dict(lado=512)),
    'patrulla':       (patrulla,       'obstaculos', dict(lado=512)),
    'autobus':        (autobus,        'obstaculos', dict(lado=1024)),
    'gorra':          (gorra,          'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
    'botas':          (botas,          'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
    'caja_sorpresa':  (caja_sorpresa,  'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
}

correr(PIEZAS)
