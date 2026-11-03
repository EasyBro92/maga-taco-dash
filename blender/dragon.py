# El dragón de China, jefe de Des Moines y del modo sin fin (03/11/2026).
#
#   blender -b -P blender/dragon.py -- [pieza ...] [--rapido]
#
# Isidro pidió «un jefe dragón brillante» y que, cuando salga, el presidente
# grite de vez en cuando «¡China!». Eligió el dragón del Año Nuevo chino: rojo
# con escamas y adornos dorados que brillan (el oro va con luz propia, así
# brilla también de día), bigotes y melena.
#
# Va por piezas porque en el juego el cuerpo serpentea: la cabeza, la
# mandíbula (se abre al escupir fuego; su origen es la bisagra), un trozo de
# cuerpo alargado que se repite cada vez más pequeño (se solapan y parece un
# cuerpo seguido), las patas (van pegadas a dos trozos) y la cola. Todas miran
# al jugador por -y (en el juego, +z) y tienen el origen en su centro. La bola
# de fuego es un obstáculo normal: origen a ras de suelo, se salta.

import os, sys, math
import bpy
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import *

ROJO = 0xd8232a
ROJO_OSCURO = 0x7a0e14


def mat_escamas(nombre, color, borde, claro, escala=6.0):
    """Escamas: celdas de Voronoi con el borde oscuro y el centro más claro."""
    m = bpy.data.materials.get(nombre)
    if m:
        return m
    m = bpy.data.materials.new(nombre)
    m.use_nodes = True
    nt = m.node_tree
    b = nt.nodes['Principled BSDF']
    b.inputs['Roughness'].default_value = 0.45
    tc = nt.nodes.new('ShaderNodeTexCoord')
    vo = nt.nodes.new('ShaderNodeTexVoronoi')
    vo.feature = 'DISTANCE_TO_EDGE'
    vo.inputs['Scale'].default_value = escala
    nt.links.new(tc.outputs['Object'], vo.inputs['Vector'])
    rampa = nt.nodes.new('ShaderNodeValToRGB')
    el = rampa.color_ramp.elements
    el[0].position, el[0].color = 0.0, (*lin(borde), 1)
    el[1].position, el[1].color = 0.06, (*lin(color), 1)
    tercero = el.new(0.32)
    tercero.color = (*lin(claro), 1)
    nt.links.new(vo.outputs['Distance'], rampa.inputs['Fac'])
    nt.links.new(rampa.outputs['Color'], b.inputs['Base Color'])
    return m


def rojo():     return mat('rojo_dragon', ROJO, 0.4)
def escamas():  return mat_escamas('escamas', ROJO, ROJO_OSCURO, 0xee4a3a)
def vientre():  return mat_bloques('vientre', 0xffc93a, 0xc8861e, ancho=4.0, alto=0.16, grosor=0.03, variacion=1.0)
def oro():      return luz('oro_dragon', 0xf2a91c, 0.4)
def oro_vivo(): return luz('oro_vivo', 0xffc93a, 0.8)
def blanco():   return luz('dientes', 0xffffff, 0.25)
def ojo():      return luz('ojo', 0xffffff, 0.35)
def negro():    return mat('negro', 0x15161b, 0.3)
def boca():     return mat('boca', 0x5a0d12, 0.7)


def punta(m, p0, p1, r0, lados=8):
    """Pincho o llama: un cono de p0 (gordo) a p1 (en punta)."""
    return rama(m, p0, p1, r0, 0.008, lados)


def curva(m, puntos, r0, r1, lados=6):
    """Un tubo que va de punto en punto adelgazando (los bigotes)."""
    n = len(puntos) - 1
    for k in range(n):
        a = r0 + (r1 - r0) * k / n
        b = r0 + (r1 - r0) * (k + 1) / n
        rama(m, puntos[k], puntos[k + 1], a, b, lados)
        if k:
            esfera(m, *puntos[k], a, 1)


def cabeza():
    """La cabeza, sin la mandíbula de abajo."""
    esfera(escamas(), 0, 0.25, 0.25, 0.95, 3, esc=(1.15, 1.0, 0.9))           # cráneo
    esfera(rojo(), 0, -0.95, 0.02, 0.7, 3, esc=(0.9, 1.4, 0.55))              # hocico largo
    esfera(rojo(), 0, -1.78, 0.14, 0.36, 3, esc=(1.2, 0.75, 0.55))            # punta de la nariz
    for s in (-1, 1):                                                          # orificios, pequeños y alargados
        esfera(boca(), s * 0.19, -1.93, 0.27, 0.07, 2, esc=(1.3, 0.6, 0.55))
    esfera(boca(), 0, -0.8, -0.28, 0.6, 3, esc=(0.85, 1.3, 0.3))              # dentro de la boca
    for x, largo in ((-0.42, 0.3), (-0.22, 0.15), (0.22, 0.15), (0.42, 0.3)):  # dientes de arriba
        punta(blanco(), (x, -1.5, -0.18), (x, -1.53, -0.2 - largo), 0.07, 6)
    # escamas doradas por el lomo del hocico
    for k in range(4):
        esfera(oro(), 0, -0.5 - 0.3 * k, 0.58 - 0.08 * k, 0.13 - 0.015 * k, 2, esc=(1.4, 1.0, 0.5))
    esfera(oro_vivo(), 0, -0.6, 0.97, 0.13, 2)                                 # la perla de la frente
    for s in (-1, 1):
        # ojos grandes de dibujo animado: blanco, iris dorado, pupila y brillo
        esfera(ojo(), s * 0.52, -0.5, 0.55, 0.3, 3)
        esfera(oro_vivo(), s * 0.55, -0.72, 0.57, 0.19, 2, esc=(1, 0.4, 1.15))
        esfera(negro(), s * 0.56, -0.78, 0.58, 0.12, 2, esc=(1, 0.45, 1.25))
        esfera(ojo(), s * 0.5, -0.86, 0.66, 0.04, 1)
        # cejas doradas que se van hacia atrás
        rama(oro(), (s * 0.2, -0.74, 0.84), (s * 0.85, -0.45, 1.0), 0.11, 0.08, 8)
        punta(oro(), (s * 0.85, -0.45, 1.0), (s * 1.2, 0.15, 1.25), 0.09)
        # cuernos de ciervo, dorados
        rama(oro(), (s * 0.4, 0.2, 0.92), (s * 0.75, 0.9, 1.75), 0.13, 0.07, 8)
        punta(oro(), (s * 0.75, 0.9, 1.75), (s * 0.8, 1.45, 2.05), 0.07)
        punta(oro(), (s * 0.6, 0.55, 1.35), (s * 1.08, 0.62, 1.62), 0.07)
        # abanico de la mejilla
        for k, dz in enumerate((0.1, -0.2)):
            punta(oro() if k == 0 else rojo(), (s * 0.95, -0.1, dz), (s * 1.45, 0.3, dz * 1.5), 0.13)
        # bigotes largos que caen en curva
        curva(oro(), [(s * 0.4, -1.82, 0.05), (s * 0.95, -1.98, -0.05), (s * 1.5, -1.8, -0.35),
                      (s * 1.85, -1.3, -0.75), (s * 1.9, -0.7, -1.15)], 0.055, 0.015)
    # melena alrededor de la nuca: mechones rojos y dorados hacia atrás
    for k in range(7):
        a = math.radians(-105 + k * 35)
        base = (math.sin(a) * 0.85, 0.75, 0.25 + math.cos(a) * 0.75)
        tip = (base[0] + math.sin(a) * 0.45, base[1] + 0.8, base[2] + math.cos(a) * 0.4)
        punta(oro() if k % 2 else mat('melena', 0xb3141c, 0.5), base, tip, 0.24, 10)


def mandibula():
    """La mandíbula de abajo: el origen es la bisagra (en la cabeza, 0, 0.15, -0.3)."""
    esfera(rojo(), 0, -0.9, -0.2, 0.62, 3, esc=(0.85, 1.35, 0.36))
    esfera(mat('lengua', 0xff5a6a, 0.5), 0, -1.0, 0.0, 0.28, 2, esc=(0.9, 1.5, 0.3))
    for x in (-0.4, -0.24, 0.24, 0.4):                                         # dientes de abajo
        punta(blanco(), (x, -1.48, 0.0), (x, -1.5, 0.2), 0.06, 6)
    esfera(oro(), 0, -1.5, -0.28, 0.2, 2, esc=(1.4, 1.0, 0.6))                 # barbilla dorada
    for k in range(5):                                                         # barba
        x = -0.36 + k * 0.18
        punta(oro() if k % 2 == 0 else rojo(), (x, -1.05 + abs(x) * 0.6, -0.32), (x * 1.3, -0.7, -0.9), 0.11)


def cuerpo():
    """Un trozo del cuerpo, alargado: escamas rojas, tripa dorada a rayas y la cresta."""
    esfera(escamas(), 0, 0, 0, 0.68, 3, esc=(1.0, 1.55, 0.95))
    esfera(vientre(), 0, 0, -0.26, 0.55, 3, esc=(0.85, 1.45, 0.7))
    for y in (-0.55, 0.0, 0.55):                                               # cresta del lomo
        punta(oro(), (0, y, 0.55), (0, y + 0.3, 0.98), 0.13)


def patas():
    """Dos patas con garras doradas; van pegadas debajo de un trozo del cuerpo."""
    for s in (-1, 1):
        rama(rojo(), (s * 0.45, 0, -0.3), (s * 0.95, -0.1, -0.85), 0.22, 0.17, 10)
        punta(oro(), (s * 0.8, -0.05, -0.6), (s * 1.12, 0.35, -0.5), 0.1)
        esfera(rojo(), s * 1.0, -0.2, -0.95, 0.2, 2, esc=(1.1, 1.3, 0.7))
        for dx in (-0.12, -0.04, 0.04, 0.12):
            punta(oro_vivo(), (s * 1.0 + dx, -0.36, -0.98), (s * 1.0 + dx * 1.3, -0.62, -1.1), 0.05, 6)


def cola():
    """La punta de la cola, con su penacho de llamas doradas."""
    esfera(escamas(), 0, 0, 0, 0.5, 3, esc=(1.0, 1.4, 0.95))
    rama(escamas(), (0, 0.4, 0), (0, 1.3, 0.2), 0.42, 0.15, 12)
    for y in (0.0, 0.6):
        punta(oro(), (0, y, 0.42), (0, y + 0.28, 0.8), 0.1)
    for k in range(7):
        a = math.radians(-66 + k * 22)
        punta(oro() if k % 2 == 0 else oro_vivo(), (0, 1.2, 0.2),
              (math.sin(a) * 0.9, 2.25, 0.2 + math.cos(a) * 0.9), 0.15)


def bola_fuego():
    """La bola de fuego que escupe: cae a la calle y rueda hacia ti. Se salta.
    Las llamas van hacia arriba y hacia atrás (+y), como si avanzara."""
    esfera(luz('fuego_centro', 0xffb52e, 0.9), 0, 0, 0.42, 0.4, 3)
    esfera(luz('fuego_dentro', 0xfff0a0, 1.0), 0, -0.12, 0.45, 0.26, 2)
    naranja = luz('llama_naranja', 0xff7a1a, 0.8)
    roja = luz('llama_roja', 0xe8361a, 0.6)
    amarilla = luz('llama_amarilla', 0xffc22e, 0.9)
    n = 12
    for k in range(n):
        a = k * 2 * math.pi / n
        for capa, (alto, m) in enumerate(((0.1, naranja), (0.35, roja if k % 2 else amarilla))):
            base = (math.cos(a) * 0.3, math.sin(a) * 0.3 * 0.6 + 0.08, 0.42 + alto * 0.5)
            tip = (math.cos(a) * 0.45, 0.35 + math.sin(a) * 0.2 + capa * 0.15, 0.75 + alto + 0.1 * math.cos(a * 2))
            punta(m, base, tip, 0.16 - capa * 0.03)


PIEZAS = {
    'dragon_cabeza':    (cabeza,     'obstaculos', dict(lado=1024, bisel=0.0, suelo=False)),
    'dragon_mandibula': (mandibula,  'obstaculos', dict(lado=512, bisel=0.0, suelo=False)),
    'dragon_cuerpo':    (cuerpo,     'obstaculos', dict(lado=512, bisel=0.0, suelo=False)),
    'dragon_patas':     (patas,      'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
    'dragon_cola':      (cola,       'obstaculos', dict(lado=512, bisel=0.0, suelo=False)),
    'bola_fuego':       (bola_fuego, 'obstaculos', dict(lado=256, bisel=0.0)),
}

correr(PIEZAS)
