# Lo de las calles de verdad: el corte de obras de los desvíos (08/11/2026).
#
#   blender -b -P blender/calles.py -- [pieza ...] [--rapido]
#
# Isidro (08/11): «haz que el personaje tenga que cambiar a otra carretera de
# vez en cuando». En los desvíos (levels.js, aplicarGiros) la calle de
# enfrente está cortada: estas vallas tapan los dos carriles que no giran
# (no se saltan ni se pasan por debajo: hay que cambiar de carril).
#   · corte_der / corte_izq: valla de obras de tres travesaños con franjas
#     naranjas y blancas, el letrero «ROAD CLOSED», dos luces ámbar (fijas,
#     sin parpadeo) y encima la flecha naranja «DETOUR» hacia el lado del giro.
# Ejes: x de lado, y hacia el fondo de la calle, z arriba; mira al jugador (-y).

import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import *

def blanco(): return mat('blanco_ca', 0xf6f4ee, 0.5)
def negro():  return mat('negro_ca', 0x1b1c20, 0.45)
def naranja(): return mat('naranja_ca', 0xf26a1b, 0.45)

def corte(lado):
    def f():
        franjas = mat_franjas('franjas_obras', 0xf26a1b, 0xf6f4ee, 10, eje='X', z0=-1.0, alto=2.0)
        for s in (-1, 1):                                   # las patas, con su pie
            caja(blanco(), s * 0.85, 0, 0, 0.1, 0.1, 1.55)
            caja(negro(), s * 0.85, 0, 0, 0.16, 0.7, 0.08)
            caja(mat('saco_arena', 0x8a7a5a, 0.9), s * 0.85, 0.22, 0.08, 0.3, 0.22, 0.14)
        for z in (0.42, 0.82, 1.22):                        # los tres travesaños
            caja(franjas, 0, -0.06, z, 2.0, 0.05, 0.24)
        caja(blanco(), 0, -0.07, 1.52, 1.5, 0.04, 0.42)     # ROAD CLOSED
        caja(negro(), 0, -0.065, 1.52, 1.56, 0.03, 0.48)
        texto(negro(), 'ROAD', 0, -0.095, 1.73, tam=0.15, prof=0.01)
        texto(negro(), 'CLOSED', 0, -0.095, 1.56, tam=0.15, prof=0.01)
        for s in (-1, 1):                                   # luces ámbar (fijas)
            cil(negro(), s * 0.85, 0, 1.55, 0.05, 0.1, 8)
            esfera(luz('luz_obras', 0xffb21a, 1.2), s * 0.85, -0.02, 1.72, 0.09, 2)
        # La flecha «DETOUR» hacia el lado del giro.
        cil(blanco(), 0, 0, 1.94, 0.03, 0.2, 6)
        caja(negro(), 0, -0.02, 2.1, 1.3, 0.03, 0.46)
        caja(naranja(), 0, -0.04, 2.12, 1.24, 0.03, 0.42)
        texto(negro(), 'DETOUR', -lado * 0.18, -0.07, 2.25, tam=0.13, prof=0.01)
        caja(negro(), -lado * 0.18, -0.065, 2.16, 0.62, 0.02, 0.07)
        o = caja(negro(), lado * 0.25, -0.065, 2.1, 0.22, 0.02, 0.22)
        o.rotation_euler = (0, math.pi / 4, 0)
        o.location = (lado * 0.18, -0.065, 2.195)
    return f

PIEZAS = {
    'corte_der': (corte(1),  'obstaculos', dict(lado=256, bisel=0.0)),
    'corte_izq': (corte(-1), 'obstaculos', dict(lado=256, bisel=0.0)),
}

correr(PIEZAS)
