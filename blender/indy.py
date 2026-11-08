# Nivel 9: Indianápolis, Indiana (08/11/2026).
#
#   blender -b -P blender/indy.py -- [pieza ...] [--rapido]
#
# Isidro (08/11): «Aplica todas las preguntas que digas recomendados»: final en
# la meta del circuito y luz de día de carrera. Historia: «El circuito de las
# 500 millas. Los coches de carreras no esperan a nadie».
#   izquierda:  el Monumento de los Soldados (el obelisco de Monument Circle)
#               · el estadio de los Colts
#   derecha:    el Capitolio de Indiana (cúpula de cobre) · el hotel de
#               cristal azul
#   en medio:   la recta del circuito entre gradas (el momento estrella), con
#               la puerta de la entrada
#   al fondo:   la meta: la franja de ladrillos, la torre Pagoda y la torre de
#               posiciones, con las banderas de cuadros
# Obstáculos (carpeta obstaculos): el coche de carreras (viene de frente,
# rapidísimo), la pila de neumáticos (se salta), el mecánico con la rueda
# (cruza), la pancarta de cuadros (agacharse) y el coche de seguridad (cambia
# de carril).

import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import *

def blanco():   return mat('blanco_in', 0xfbf8f2, 0.5)
def negro():    return mat('negro_in', 0x1d1f25, 0.4)
def oscuro():   return mat('hueco_in', 0x2b2c33, 0.8)
def vidrio():   return mat('vidrio_in', 0x6a8aa8, 0.15)
def hierro():   return mat('hierro_in', 0x2c2e33, 0.4)
def rojo():     return mat('rojo_in', 0xc8202e, 0.45)
def caliza():   return mat_bloques('caliza_in', 0xe6dcc6, 0xcfc3aa, ancho=1.4, alto=0.55, grosor=0.02, variacion=1.04)
def ladrillo(): return mat_bloques('ladrillo_in', 0x9e4a36, 0x7e3a2a, ancho=0.45, alto=0.2, grosor=0.02, variacion=1.08)
def cobre():    return mat('cobre_in', 0x5f9e88, 0.5)
def cuadros(nombre, x0, ancho, n=8): return mat_franjas(nombre, 0x1d1f25, 0xfbf8f2, n, eje='X', z0=x0, alto=ancho)

# ================================================================ los edificios
def soldiers_monument():
    """El Monumento de los Soldados y Marineros (Monument Circle): el obelisco
    de piedra con la estatua de la Victoria arriba, las fuentes en escalones
    y las esculturas de la base."""
    W = 30
    caja(mat('plaza_mon', 0xd8d0c0, 0.8), 0, 12, 0, W, 24, 0.1)
    for k, (w, h) in enumerate(((16, 1.2), (12, 1.2), (8, 2.0))):
        caja(caliza(), 0, 12, sum(hh for _, hh in ((16, 1.2), (12, 1.2), (8, 2.0))[:k]), w, w, h)
    caja(mat('agua_fuente', 0x6aa0c8, 0.15), 0, 12 - 7.0, 0.6, 14, 2.2, 0.15)
    caja(caliza(), 0, 12, 4.4, 5.0, 5.0, 26)
    cil(caliza(), 0, 12, 30.4, 2.0, 6.0, 4, r2=1.4).rotation_euler = (0, 0, math.pi / 4)
    cil(mat('bronce_in', 0x6a4a2a, 0.35), 0, 12, 36.4, 0.6, 2.4, 10, r2=0.3)
    esfera(mat('bronce_in', 0x6a4a2a, 0.35), 0, 12, 39.0, 0.4, 2)
    for s in (-1, 1):
        rama(mat('bronce_in', 0x6a4a2a, 0.35), (0, 12, 38.4), (s * 1.2, 12, 39.6), 0.1, 0.05, 6)
    texto(mat('letras_mon', 0x6a4a2a, 0.4), 'SOLDIERS AND SAILORS', 0, 9.4, 6.0, tam=0.45, prof=0.04)

def statehouse_in():
    """El Capitolio de Indiana: piedra clara, el pórtico con columnas y la
    cúpula de cobre verde con su linterna."""
    W, D = 40, 26
    caja(caliza(), 0, D / 2, 0, W, D, 15)
    columnata(blanco(), -7, 7, 8, -2.0, 1.4, 0.55, 11.0)
    caja(blanco(), 0, -1.2, 12.4, 17, 3.0, 1.2)
    fronton(blanco(), 0, -2.6, 13.6, 17, 3.2, 3.0)
    cil(caliza(), 0, D / 2, 15, 7.5, 6.0, 24)
    cupula(cobre(), 0, D / 2, 21, 7.6, 8.0, lados=24, aros=6)
    cil(caliza(), 0, D / 2, 29, 1.3, 3.0, 12)
    cupula(cobre(), 0, D / 2, 32, 1.4, 1.4, lados=12, aros=4)
    for x in (-16, -12, 12, 16):
        ventana(x, 3.0, 1.8, 3.0, y=-0.1, marco=blanco(), cristal=vidrio())

def lucas_oil():
    """El estadio de los Colts: ladrillo rojo con arcos de cristal, la gran
    cristalera y el tejado que se abre, con el letrero de la herradura."""
    W, D, H = 40, 34, 20
    caja(ladrillo(), 0, D / 2, 0, W, D, H)
    for x in (-14, -7, 0, 7, 14):
        caja(vidrio(), x, -0.06, 2.0, 5.0, 0.12, 12.0)
        cil(vidrio(), x, -0.06, 14.0, 2.5, 0.12, 16, eje='Y')
    caja(mat('tejado_estadio', 0x9aa4ae, 0.4), 0, D / 2, H, W - 2, D - 2, 1.0)
    caja(mat('tejado_estadio', 0x9aa4ae, 0.4), 0, D / 2, H + 1.0, W - 10, D - 6, 2.4, inclina=0.0)
    caja(mat('letrero_colts', 0x1f3a8a, 0.5), 0, -0.3, H - 3.2, 14, 0.3, 2.4)
    o = cil(blanco(), -4.6, -0.5, H - 2.0, 0.9, 0.1, 20, eje='Y')
    texto(blanco(), 'STADIUM', 1.6, -0.5, H - 2.0, tam=1.1, prof=0.06)

def jw_marriott():
    """El hotel de cristal azul, alto y en curva."""
    W, D, H = 30, 20, 58
    azul_c = mat('vidrio_azul_jw', 0x3a7ab8, 0.12)
    for k in range(12):
        a = (k - 5.5) / 5.5
        caja(azul_c, a * 14, D / 2 + a * a * 3, 0, 2.6, D, H)
        for p in range(1, 18):
            caja(mat('franja_jw', 0x9ac0e0, 0.3), a * 14, a * a * 3 - 0.08, p * 3.3, 2.6, 0.12, 0.2)
    caja(mat('remate_jw', 0x2a5a8a, 0.3), 0, D / 2, H, W, D, 2.0)
    texto(blanco(), 'HOTEL', 0, -0.2, 4.2, tam=1.2, prof=0.06)

# ================================================================ el circuito
def grada():
    """30 m de la recta del circuito: el muro de la pista (blanco con franja
    roja), la valla de seguridad (postes y tres cables: una malla fina
    parpadearía) y, detrás, las gradas llenas de público de colores, con el
    tejadillo arriba."""
    L = 30.0
    caja(mat('asfalto_pista', 0x45474d, 0.8), 0, 0, 0, 8.4, L, 0.06)
    for s in (-1, 1):
        caja(mat('cesped_pista', 0x5a9a48, 0.8), s * 5.8, 0, 0, 2.8, L, 0.05)
    publico = [mat('publico_%d' % k, c, 0.6) for k, c in enumerate((0xd8283a, 0x2a6ab8, 0xf2c230, 0xfbf8f2, 0x3a9a4a, 0xe8781a))]
    for s in (-1, 1):
        caja(blanco(), s * 4.35, 0, 0, 0.3, L, 1.1)
        caja(rojo(), s * 4.18, 0, 0.75, 0.04, L, 0.18)
        for k in range(11):
            caja(hierro(), s * 4.45, -L / 2 + k * 3, 1.1, 0.1, 0.1, 3.4)
        for z in (2.0, 3.0, 4.3):
            caja(hierro(), s * 4.45, 0, z, 0.03, L, 0.03)
        # Las gradas: escalones subiendo hacia fuera, con gente (bloques de colores).
        for f in range(8):
            x = s * (7.0 + f * 1.4)
            z = 0.6 + f * 1.0
            caja(mat('grada_hormigon', 0xb8b4ac, 0.7), x, 0, 0, 1.4, L, z)
            for g in range(14):
                caja(publico[(f * 3 + g * 5 + (s > 0)) % len(publico)], x, -L / 2 + 1.0 + g * 2.1, z, 0.5, 0.5, 0.75)
                esfera(mat('cabeza_publico', 0xe8b48c, 0.6), x, -L / 2 + 1.0 + g * 2.1, z + 0.95, 0.18, 1)
        caja(mat('tejadillo_grada', 0xe8e4dc, 0.5), s * 12.0, 0, 11.5, 10.0, L, 0.3)
        for y in (-12.0, 0.0, 12.0):
            cil(hierro(), s * 16.8, y, 0, 0.2, 11.5, 8)

def circuito_entrada():
    """La entrada al circuito (08/11 (2)). Isidro: «el circuito que aparece ...
    no de forma realista». Antes era una puerta suelta y detrás, de golpe, las
    gradas. Ahora la calle llega al muro del circuito (ladrillo, 13,5 m de alto
    y 140 de ancho), con el letrero, el logo de la rueda con alas y las
    taquillas; detrás asoman las gradas con su tejado, y se entra por un
    túnel de 30 m por debajo de ellas, como en el de verdad. Al salir del
    túnel empieza la recta. Va de d a d + 34: el muro en y = -17 y el suelo
    desde y = -13 (donde levels.js quita la calle) hasta y = 17."""
    L = 34.0
    y0 = -L / 2
    T, H = 4.3, 10.0      # (10 m: la cámara del juego va alta y con menos se veía el techo por encima)
    M = 13.5              # alto del muro
    muro = ladrillo()
    hormi = mat_bloques('hormigon_tunel_in', 0x8a867e, 0x7a766e, ancho=2.4, alto=1.2, grosor=0.01, variacion=1.04)
    for s in (-1, 1):
        caja(muro, s * (T + (70 - T) / 2), y0 + 0.6, 0, 70 - T, 1.2, M)
        caja(blanco(), s * (T + (70 - T) / 2), y0 + 0.6, M, 70 - T, 1.5, 0.35)
    caja(muro, 0, y0 + 0.6, H, T * 2, 1.2, M - H)
    caja(blanco(), 0, y0 + 0.6, M, T * 2, 1.5, 0.35)
    for s in (-1, 1):                                       # el marco del túnel
        caja(blanco(), s * (T + 0.25), y0 - 0.1, 0, 0.5, 0.3, H + 0.5)
    caja(blanco(), 0, y0 - 0.1, H, T * 2 + 1.0, 0.3, 0.5)
    # Detrás del muro asoman las gradas, con su tejado y sus columnas.
    caja(mat('grada_trasera', 0xb8b4ac, 0.7), 0, y0 + 8.0, M, 140, 14, 5.5)
    for x in range(-66, 67, 12):
        caja(hierro(), x, y0 + 2.2, M, 0.3, 0.3, 7.0)
    caja(mat('tejadillo_grada', 0xe8e4dc, 0.5), 0, y0 + 8.0, M + 7.0, 140, 16, 0.4)
    # El letrero azul con la franja de cuadros, encima del túnel.
    caja(mat('letrero_ims', 0x1f3a8a, 0.5), 0, y0 - 0.15, H + 0.8, 26.0, 0.6, 2.4)
    texto(blanco(), 'INDIANAPOLIS MOTOR SPEEDWAY', 0, y0 - 0.5, H + 1.8, tam=0.85, prof=0.05)
    caja(cuadros('cuadros_puerta', -13.0, 26.0, 13), 0, y0 - 0.5, H + 0.85, 26.0, 0.05, 0.45)
    # El logo, la rueda con alas, a los dos lados del túnel.
    for s in (-1, 1):
        x = s * 13.0
        cil(blanco(), x, y0 - 0.05, 7.0, 1.3, 0.2, 24, eje='Y')
        cil(mat('rueda_logo', 0x1f3a8a, 0.5), x, y0 - 0.15, 7.0, 1.0, 0.1, 24, eje='Y')
        for w in (-1, 1):
            for k in range(3):
                caja(blanco(), x + w * (1.75 + k * 0.45), y0 - 0.1, 6.7 + k * 0.35, 0.8 - k * 0.15, 0.1, 0.25)
    # Las taquillas, a los lados de la entrada.
    for s in (-1, 1):
        x = s * 21.0
        caja(mat('taquilla', 0xe8e4dc, 0.5), x, y0 - 1.6, 0, 4.0, 2.4, 2.8)
        caja(vidrio(), x, y0 - 2.82, 1.0, 3.0, 0.05, 1.1)
        caja(rojo(), x, y0 - 1.6, 2.8, 4.4, 2.8, 0.3)
        texto(blanco(), 'TICKETS', x, y0 - 3.05, 2.3, tam=0.35, prof=0.02)
    # El túnel: paredes y techo de hormigón, las luces y el suelo.
    yt0, yt1 = y0 + 1.2, 13.0
    for s in (-1, 1):
        caja(hormi, s * (T + 0.2), (yt0 + yt1) / 2, 0, 0.4, yt1 - yt0, H)
    caja(hormi, 0, (yt0 + yt1) / 2, H, T * 2 + 0.8, yt1 - yt0, 0.4)
    for y in (-12.0, -6.0, 0.0, 6.0, 11.0):
        caja(luz('luz_tunel_in', 0xffe2b0, 1.2), 0, y, H - 0.08, 1.4, 0.5, 0.06)
    caja(mat('asfalto_pista', 0x45474d, 0.8), 0, 2.0, 0, 8.4, 30, 0.06)
    # A la salida del túnel, el muro de la pista y la hierba, como en las gradas.
    for s in (-1, 1):
        caja(mat('cesped_pista', 0x5a9a48, 0.8), s * 5.8, 15.0, 0, 2.8, 4.0, 0.05)
        caja(blanco(), s * 4.35, 15.0, 0, 0.3, 4.0, 1.1)
        caja(rojo(), s * 4.18, 15.0, 0.75, 0.04, 4.0, 0.18)
        caja(mat('grada_hormigon', 0xb8b4ac, 0.7), s * 12.0, 15.0, 0, 10.0, 4.0, 8.0)
        caja(mat('grada_hormigon', 0xb8b4ac, 0.7), s * (T + 2.6), 13.6, 0, 4.4, 1.2, H + 0.4)   # la boca de dentro

def meta_indy():
    """La meta: la franja de ladrillos de lado a lado (el jugador se para
    encima), a la izquierda la torre Pagoda de cristal con sus tejadillos y la
    torre de posiciones con los números (en el interior del óvalo, como en el
    de verdad), y a la derecha la grada sigue, con el puesto del juez y las
    banderas de cuadros."""
    caja(mat('asfalto_pista', 0x45474d, 0.8), 0, 40, 0, 8.4, 80, 0.06)
    caja(mat('cesped_pista', 0x5a9a48, 0.8), -20, 40, 0, 31.6, 80, 0.05)
    caja(mat('cesped_pista', 0x5a9a48, 0.8), 5.8, 40, 0, 2.8, 80, 0.05)
    caja(mat_bloques('ladrillos_meta', 0xa8503a, 0x8a3e2c, ancho=0.4, alto=0.2, grosor=0.02, variacion=1.06), 0, 0.5, 0, 8.4, 1.0, 0.09)
    for s in (-1, 1):
        caja(blanco(), s * 4.35, 40, 0, 0.3, 80, 1.1)
        caja(rojo(), s * 4.18, 40, 0.75, 0.04, 80, 0.18)
    # La Pagoda.
    for k in range(5):
        z = k * 5.0
        w = 14 - k * 1.6
        caja(vidrio(), -18, 16, z, w, w, 4.2)
        caja(blanco(), -18, 16, z + 4.2, w + 2.4, w + 2.4, 0.4)
    caja(blanco(), -18, 16, 25.0, 1.0, 1.0, 3.0)
    caja(cuadros('bandera_pagoda', -18, 2.4, 4), -16.8, 16, 26.6, 2.4, 0.04, 1.3)
    texto(mat('letras_pagoda', 0xfbf8f2, 0.4), 'INDIANAPOLIS', -18, 8.6, 21.2, tam=0.7, prof=0.04)
    # La torre de posiciones, con los números.
    caja(negro(), -9.0, 6, 0, 2.6, 2.0, 30)
    for k in range(10):
        texto(mat('numero_torre', 0xf2c230, 0.3), str((k * 7) % 33 + 1), -9.0, 4.95, 27.6 - k * 2.6, tam=1.1, prof=0.03)
    # La grada de la derecha sigue, con el puesto del juez sobre el muro.
    publico = [mat('publico_%d' % k, c, 0.6) for k, c in enumerate((0xd8283a, 0x2a6ab8, 0xf2c230, 0xfbf8f2, 0x3a9a4a, 0xe8781a))]
    for f in range(8):
        x = 7.0 + f * 1.4
        z = 0.6 + f * 1.0
        caja(mat('grada_hormigon', 0xb8b4ac, 0.7), x, 30, 0, 1.4, 60, z)
        for g in range(28):
            caja(publico[(f * 3 + g * 5) % len(publico)], x, 1.0 + g * 2.1, z, 0.5, 0.5, 0.75)
    caja(mat('tejadillo_grada', 0xe8e4dc, 0.5), 12.0, 30, 11.5, 10.0, 60, 0.3)
    caja(hierro(), 5.4, 0.8, 0, 0.3, 0.3, 4.0)
    caja(blanco(), 5.4, 0.8, 4.0, 2.2, 2.2, 0.3)
    caja(mat('puesto_juez', 0xd8202a, 0.5), 5.4, 0.8, 4.3, 2.2, 2.2, 1.0)
    for s in (-1, 1):
        cil(blanco(), 5.4 + s * 0.8, 0.0, 5.3, 0.05, 2.0, 6)
        caja(cuadros('bandera_juez_%d' % (s > 0), 5.4 + s * 1.6 - 0.8, 1.6, 4), 5.4 + s * 1.6, 0.0, 6.4, 1.6, 0.03, 1.0)

# ================================================================ los obstáculos
def indycar():
    """El coche de carreras (de ruedas descubiertas), visto por detrás: el
    alerón de atrás con el número, las ruedas gordas, el piloto con el casco
    amarillo y el morro afilado hacia delante. Va por la pista más despacio
    que el jugador: hay que adelantarlo."""
    W = 1.9
    pintura = mat('pintura_indy', 0xd8202a, 0.3)
    caja(pintura, 0, 2.3, 0.2, 0.8, 3.2, 0.45)
    caja(pintura, 0, 1.0, 0.2, 0.6, 0.8, 0.62)
    o = cil(pintura, 0, 4.4, 0.42, 0.24, 1.2, 10, r2=0.06, eje='Y')
    o.rotation_euler = (-math.pi / 2, 0, 0)
    caja(mat('aleron_indy', 0x1d1f25, 0.4), 0, 4.85, 0.12, W, 0.45, 0.06)
    caja(pintura, 0, 0.25, 0.75, W - 0.2, 0.3, 0.32)
    for x in (-0.82, 0.82):
        caja(mat('aleron_indy', 0x1d1f25, 0.4), x, 0.25, 0.3, 0.05, 0.45, 0.8)
    texto(blanco(), '45', 0, 0.08, 0.8, tam=0.24, prof=0.01)
    caja(mat('casco', 0xf2c230, 0.3), 0, 2.1, 0.66, 0.34, 0.42, 0.3)
    for s in (-1, 1):
        for y in (0.8, 3.7):
            cil(mat('neumatico_indy', 0x1d1e21, 0.8), s * 0.82, y, 0.36, 0.36, 0.34, 16, eje='X')

def pila_neumaticos():
    """Una pila de neumáticos (con el de arriba blanco y rojo): se salta."""
    for k in range(3):
        for x in (-0.5, 0.5):
            cil(mat('neumatico_pila', 0x1d1e21, 0.8), x, 0.4, k * 0.3, 0.42, 0.3, 16)
    cil(rojo(), -0.5, 0.4, 0.9, 0.42, 0.04, 16)
    cil(blanco(), 0.5, 0.4, 0.9, 0.42, 0.04, 16)

def pit_crew():
    """El mecánico del equipo con el mono rojo, el casco y una rueda en las
    manos. Cruza la calle (mira a +x)."""
    mono = mat('mono_pit', 0xd8202a, 0.5)
    for sy in (-0.12, 0.12):
        cil(mono, 0, sy, 0, 0.11, 0.85, 8)
    caja(mono, 0, 0, 0.85, 0.44, 0.5, 0.68)
    esfera(mat('casco_pit', 0xfbf8f2, 0.3), 0, 0, 1.7, 0.22, 2)
    cil(mat('neumatico_pit', 0x1d1e21, 0.8), 0.35, 0, 1.15, 0.34, 0.28, 16, eje='X')
    for sy in (-0.2, 0.2):
        rama(mono, (0, sy, 1.4), (0.3, sy * 0.8, 1.15), 0.07, 0.06, 6)

def bandera_cuadros():
    """La pancarta de cuadros colgada de un cable: se pasa agachado."""
    caja(hierro(), 0, 0, 2.6, 2.0, 0.05, 0.05)
    for x in (-0.85, 0.85):
        caja(hierro(), x, 0, 2.1, 0.03, 0.03, 0.5)
    caja(cuadros('pancarta_cuadros', -0.95, 1.9, 5), 0, 0, 1.3, 1.9, 0.05, 0.8)
    caja(rojo(), 0, -0.03, 1.2, 1.9, 0.06, 0.1)

def coche_seguridad():
    """El coche de seguridad (deportivo blanco con la barra de luces), visto
    por detrás. Cambia de carril con el intermitente."""
    W, L = 1.9, 4.4
    blanco_c = mat('blanco_pace', 0xf6f6f2, 0.3)
    caja(blanco_c, 0, L / 2, 0.3, W, L, 0.65)
    caja(blanco_c, 0, L / 2 + 0.3, 0.95, W - 0.3, 2.0, 0.4)
    caja(mat('cristal_pace', 0x2c3e55, 0.15), 0, L / 2 - 0.75, 0.97, W - 0.4, 0.05, 0.34, inclina=0.5)
    caja(rojo(), 0, L / 2, 0.7, W + 0.02, L, 0.12)
    caja(mat('barra_luces', 0xf2a81a, 0.3), 0, L / 2 + 0.3, 1.36, 1.2, 0.25, 0.12)
    for s in (-1, 1):
        caja(mat('piloto', 0xc0262c, 0.3), s * 0.7, 0.0, 0.7, 0.3, 0.04, 0.12)
        caja(mat('intermitente', 0xffa21a, 0.3), s * 0.7, 0.0, 0.88, 0.25, 0.04, 0.06)
        for y in (0.8, L - 0.8):
            cil(mat('neumatico', 0x1d1e21, 0.8), s * (W / 2 - 0.1), y, 0.34, 0.34, 0.26, 14, eje='X')
    texto(negro(), 'PACE CAR', 0, -0.02, 0.5, tam=0.16, prof=0.01)

PIEZAS = {
    'soldiers_monument': (soldiers_monument, 'indianapolis', dict(lado=1024, segmentos=2, min_bisel=1.0)),
    'statehouse_in':     (statehouse_in,     'indianapolis', dict(lado=1024, segmentos=2, min_bisel=1.0)),
    'lucas_oil':         (lucas_oil,         'indianapolis', dict(lado=1024, segmentos=2, min_bisel=1.0)),
    'jw_marriott':       (jw_marriott,       'indianapolis', dict(lado=1024, segmentos=2)),
    'grada':             (grada,             'indianapolis', dict(lado=2048, bisel=0.0, segmentos=2)),
    'circuito_entrada':  (circuito_entrada,  'indianapolis', dict(lado=2048, bisel=0.0, suelo=False)),
    'meta_indy':         (meta_indy,         'indianapolis', dict(lado=2048, segmentos=1, min_bisel=2.0)),
    'indycar':           (indycar,           'obstaculos', dict(lado=512)),
    'pila_neumaticos':   (pila_neumaticos,   'obstaculos', dict(lado=256, bisel=0.0)),
    'pit_crew':          (pit_crew,          'obstaculos', dict(lado=256, bisel=0.0)),
    'bandera_cuadros':   (bandera_cuadros,   'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
    'coche_seguridad':   (coche_seguridad,   'obstaculos', dict(lado=512)),
}

correr(PIEZAS)
