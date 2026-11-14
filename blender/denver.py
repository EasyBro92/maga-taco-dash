# Nivel 29: Denver, Colorado (14/11/2026).
#
#   blender -b -P blender/denver.py -- [pieza ...] [--rapido]
#
# Historia: «"Colorado" quiere decir rojo en español: él dice que es una
#   señal». Acto de la Armada Española.
#   Por el 16th Street Mall en invierno (el arco de WELCOME de la estación, la
#   torre del reloj Daniels & Fisher, la Union Station con su neón y el oso
#   azul que mira dentro del centro de convenciones) mientras bajan rodando
#   bolas de nieve que crecen; la pista de esquí de las Rocosas, con las
#   puertas del eslalon; y se llega al Capitolio de Colorado, con su cúpula de
#   oro y el escalón que está a una milla de altura. Pancartas de España:
#   COLORADO = ROJO.
# Obstáculos (carpeta obstaculos): las puertas roja y azul del eslalon, el
# pino nevado, la telesilla, la pancarta COLORADO = ROJO y el autobús
# gratuito del Mall. (Las bolas de nieve que crecen usan la bola_nieve que ya
# existía.)

import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import *

def blanco():   return mat('blanco_den', 0xf6f4ee, 0.5)
def negro():    return mat('negro_den', 0x1c1c20, 0.4)
def granito():  return mat_bloques('granito_den', 0xc8c2b6, 0xa8a296, ancho=1.4, alto=0.7, grosor=0.008, variacion=1.04)
def granito_l(): return mat('granito_liso_den', 0xc0baae, 0.7)
def oro():      return mat('oro_den', 0xe8b840, 0.25)
def ladrillo(): return mat_bloques('ladrillo_den', 0xa86a4a, 0x7a4a34, ancho=0.4, alto=0.16)
def piedra():   return mat('piedra_den', 0xd8ccb4, 0.7)
def cristal():  return mat('cristal_den', 0x3a5a70, 0.15)
def rojo():     return mat('rojo_den', 0xc8202a, 0.45)
def azul():     return mat('azul_den', 0x2a5ab8, 0.45)
def gris():     return mat('gris_den', 0x8a9098, 0.4)
def nieve():    return mat('nieve_den', 0xf2f6fa, 0.85)
def pino_m():   return mat('pino_den', 0x2a5a3a, 0.85)
def tronco():   return mat('tronco_den', 0x5a3a26, 0.85)
def cesped():   return mat('cesped_den', 0x7a9a5a, 0.9)
def neon_rojo(): return luz('neon_rojo_den', 0xff3030, 1.7)
def bombilla():  return luz('bombilla_den', 0xfff0b0, 1.5)

def bandera_es(nombre, z0, alto):
    """Las franjas de la bandera de España (roja, amarilla, roja) en z0..z0+alto."""
    return mat_franjas(nombre, 0xc8202a, 0xf2c21a, 3, eje='Z', z0=z0, alto=alto)

def pino(x, y, alto=6.0, z=0.0):
    """Un pino nevado: el tronco y tres pisos de ramas con nieve encima."""
    cil(tronco(), x, y, z, 0.22, alto * 0.25, 8)
    for k in range(3):
        r = alto * (0.32 - k * 0.08)
        zz = z + alto * (0.18 + k * 0.24)
        cil(pino_m(), x, y, zz, r, alto * 0.36, 10, r2=0.05)
        cil(nieve(), x, y, zz + alto * 0.2, r * 0.5, alto * 0.1, 10, r2=0.04)

def persona_esqui(x, y, c, giro=0.0):
    """Un esquiador de lado de la pista: el cuerpo, el gorro y los esquís."""
    cil(mat(f'ropa_den_{c:06x}', c, 0.6), x, y, 0.15, 0.25, 1.15, 8)
    esfera(mat('piel_den', 0xe8c0a0, 0.7), x, y, 1.45, 0.2, 1)
    cil(rojo(), x, y, 1.55, 0.18, 0.18, 8, r2=0.05)
    caja(negro(), x, y, 0.02, 0.18, 1.7, 0.05, giro=giro)

# ================================================================ la meta
def capitolio_colorado():
    """El Capitolio de Colorado (la meta): el granito, el pórtico con columnas
    y frontón, el tambor con columnas y la cúpula de oro con su linterna, la
    escalinata con el escalón de una milla de altura, el césped nevado, la
    bandera y, de España, la pancarta COLORADO = ROJO."""
    Y = 26
    W, D, H = 56.0, 26.0, 15.0
    yf = Y - D / 2
    g = granito()
    caja(g, 0, Y, 0, W, D, H)
    caja(granito_l(), 0, Y, H, W + 0.6, D + 0.6, 0.8)
    for s in (-1, 1):
        caja(g, s * 22, yf - 1.5, 0, 12, 3, H)
        caja(granito_l(), s * 22, yf - 1.6, H, 12.4, 3.4, 0.8)
    for k in range(12):
        x = -24 + k * 4.36
        for z in (3.5, 8.5):
            if abs(x) < 9:
                continue
            ventana(x, z, 1.4, 2.8, y=yf - (3 if abs(abs(x) - 22) < 6.5 else 0), marco=granito_l(), cristal=cristal())
    # El pórtico.
    columnata(granito_l(), -7.5, 7.5, 6, yf - 3.5, 4.0, 0.55, 9.5)
    caja(g, 0, yf - 2, 0, 18, 4, 4.0)
    caja(granito_l(), 0, yf - 3.5, 13.5, 17.6, 3.2, 1.2)
    fronton(granito_l(), 0, yf - 3.5, 14.7, 17.6, 3.2, 3.2)
    puerta(0, 4.0, 2.6, 4.2, y=yf - 0.05, color=0x5a3a22, marco=granito_l())
    # El tambor, la cúpula de oro y la linterna.
    cil(g, 0, Y, H + 0.8, 8.5, 2.5, 32)
    cil(granito_l(), 0, Y, H + 3.3, 7.4, 7.0, 32)
    for k in range(16):
        a = k * math.tau / 16
        cil(blanco(), math.cos(a) * 7.7, Y + math.sin(a) * 7.7, H + 3.3, 0.32, 7.0, 10)
    caja(blanco(), 0, Y, H + 10.3, 16.6, 16.6, 0.01)
    cil(granito_l(), 0, Y, H + 10.3, 8.2, 0.9, 32)
    cupula(oro(), 0, Y, H + 11.2, 7.6, 8.2, 32, 10)
    cil(oro(), 0, Y, H + 19.2, 1.5, 3.0, 12)
    cupula(oro(), 0, Y, H + 22.2, 1.6, 1.6, 12, 4)
    esfera(oro(), 0, Y, H + 24.2, 0.45, 1)
    # La escalinata y el escalón de la milla.
    for k in range(12):
        caja(granito_l(), 0, yf - 5.8 - k * 0.55, 0, 20 + k * 0.6, 0.55, 4.0 - k * 0.33)
    caja(oro(), 0, yf - 5.8 - 7 * 0.55 - 0.28, 4.0 - 7 * 0.33 - 0.25, 3.4, 0.03, 0.22)
    texto(negro(), 'ONE MILE ABOVE SEA LEVEL', 0, yf - 5.8 - 7 * 0.55 - 0.3, 4.0 - 7 * 0.33 - 0.14, tam=0.15, prof=0.01)
    # El césped con nieve, los pinos, la bandera y la pancarta de España.
    caja(cesped(), 0, yf - 16, -0.05, 76, 22, 0.06)
    n = nieve()
    for (x, y, rx, ry) in ((-22, yf - 12, 9, 4), (20, yf - 20, 8, 3.5), (-14, yf - 22, 6, 3), (26, yf - 10, 5, 3)):
        esfera(n, x, y, 0, 1.0, 2, esc=(rx, ry, 0.25), mitad=True)
    for (x, y) in ((-32, yf - 6), (-30, yf - 18), (32, yf - 5), (30, yf - 17), (-36, yf + 4), (36, yf + 4)):
        pino(x, y, 9)
    cil(gris(), -16, yf - 12, 0, 0.13, 13, 8)
    caja(mat_franjas('bandera_us_den', 0xc8202a, 0xf6f4ee, 13, eje='Z', z0=10.6, alto=2.4), -14.2, yf - 12, 10.6, 3.6, 0.06, 2.4)
    caja(mat('canton_den', 0x2a3a8a, 0.6), -15.2, yf - 12.04, 11.7, 1.6, 0.06, 1.3)
    for x in (10.5, 21.5):
        cil(tronco(), x, yf - 14, 0, 0.12, 4.4, 8)
    caja(bandera_es('pancarta_es_capitolio', 2.8, 1.6), 16, yf - 14, 2.8, 11, 0.06, 1.6)
    texto(negro(), 'COLORADO = ROJO', 16, yf - 14.04, 3.6, tam=0.85, prof=0.03)

# ================================================================ edificios
def torre_daniels():
    """La torre del reloj Daniels & Fisher (el campanario de Venecia del Mall):
    ladrillo con bandas de piedra, los relojes en las cuatro caras, el
    campanario de arcos, el tejado de pirámide y la linterna."""
    Y = 6
    L = 7.0
    l = ladrillo()
    p = piedra()
    caja(l, 0, Y, 0, L, L, 44)
    for z in (0, 6, 18, 30):
        caja(p, 0, Y, z, L + 0.3, L + 0.3, 0.8 if z else 4.5)
    caja(cristal(), 0, Y - L / 2 - 0.05, 0.5, 3.2, 0.1, 3.2)
    for z in (9, 13, 21, 25, 33):
        for dx in (-1.5, 1.5):
            caja(cristal(), dx, Y - L / 2 - 0.04, z, 0.9, 0.08, 2.2)
    # Los relojes.
    for (dx, dy, rx) in ((0, -1, 0), (0, 1, 0), (-1, 0, 1), (1, 0, 1)):
        x, y = dx * (L / 2 + 0.1), Y + dy * (L / 2 + 0.1)
        o = cil(blanco(), x, y, 38, 2.2, 0.15, 24, eje='Y')
        if rx:
            o.rotation_euler = (math.pi / 2, 0, math.pi / 2)
        if dy == -1:
            caja(negro(), x, y - 0.12, 38, 0.12, 0.04, 1.6)
            caja(negro(), x + 0.5, y - 0.12, 38, 1.1, 0.04, 0.12)
    caja(p, 0, Y, 41, L + 0.5, L + 0.5, 0.6)
    # El campanario de arcos.
    for sx in (-1, 1):
        for sy in (-1, 1):
            caja(p, sx * 3.0, Y + sy * 3.0, 44, 1.0, 1.0, 5)
    caja(mat('campana_den', 0x6a5a2a, 0.35), 0, Y, 44.6, 2.2, 2.2, 2.4)
    caja(p, 0, Y, 49, L + 0.6, L + 0.6, 0.8)
    o = cil(mat('tejado_den', 0x4a7a6a, 0.6), 0, Y, 49.8, L * 0.72, 6.5, 4, r2=0.15)
    o.rotation_euler = (0, 0, math.pi / 4)
    cil(oro(), 0, Y, 56.3, 0.25, 1.6, 8)
    esfera(oro(), 0, Y, 58.0, 0.4, 1)

def union_station_den():
    """La Union Station de Denver: el edificio de granito claro, los tres
    grandes ventanales en arco, el reloj, el letrero UNION STATION y el
    TRAVEL BY TRAIN en neón rojo."""
    Y = 10
    W, D = 46.0, 16.0
    yf = Y - D / 2
    g = mat_bloques('granito_us_den', 0xd8ccb4, 0xbcae96, ancho=1.2, alto=0.6, grosor=0.008)
    caja(g, 0, Y, 0, W, D, 11)
    caja(g, 0, Y, 11, 20, D, 7)
    tejado(mat('tejado_us_den', 0x8a4a3a, 0.7), 0, Y - D / 2, Y + D / 2, 18, 20, 3.0, cumbrera='x')
    for s in (-1, 1):
        tejado(mat('tejado_us_den', 0x8a4a3a, 0.7), s * 16.5, Y - D / 2, Y + D / 2, 11, 13, 2.4, cumbrera='x')
    for x in (-6, 0, 6):
        caja(cristal(), x, yf - 0.05, 1.0, 4.4, 0.1, 9.5)
        cil(cristal(), x, yf - 0.05, 10.5, 2.2, 0.1, 16, eje='Y')
        caja(piedra(), x, yf - 0.1, 0.8, 4.8, 0.08, 0.3)
    for s in (-1, 1):
        for k in range(4):
            ventana(s * (12.5 + k * 2.8), 5.5, 1.3, 2.6, y=yf, marco=piedra(), cristal=cristal())
    cil(blanco(), 0, yf - 0.1, 15.5, 1.2, 0.1, 20, eje='Y')
    caja(negro(), 0, yf - 0.18, 15.5, 0.1, 0.04, 0.9)
    # Los letreros.
    caja(negro(), 0, yf + 1.5, 21.2, 18, 0.3, 1.8)
    texto(neon_rojo(), 'UNION STATION', 0, yf + 1.32, 22.1, tam=1.5, prof=0.06)
    caja(negro(), 0, yf - 0.35, 11.6, 15, 0.2, 1.4)
    texto(neon_rojo(), 'TRAVEL', -4.4, yf - 0.5, 12.3, tam=0.95, prof=0.05)
    texto(mat('blanco_neon_den', 0xfff4e0, 0.3), 'BY', 0, yf - 0.5, 12.3, tam=0.95, prof=0.05)
    texto(neon_rojo(), 'TRAIN', 4.2, yf - 0.5, 12.3, tam=0.95, prof=0.05)

def oso_azul():
    """El oso azul que mira dentro del centro de convenciones: la fachada de
    cristal en cuadrícula y el oso gigante de pie, con las patas y el hocico
    pegados al cristal (se le ve de lado al pasar)."""
    Y = 10
    W, D, H = 36.0, 12.0, 16.0
    yf = Y - D / 2
    caja(mat('hormigon_den', 0xb8b8b4, 0.7), 0, Y, 0, W, D, H)
    caja(cristal(), 0, yf - 0.05, 0.3, W - 2, 0.1, H - 1.5)
    marco = gris()
    for k in range(10):
        caja(marco, -16 + k * 3.55, yf - 0.12, 0.3, 0.18, 0.12, H - 1.5)
    for z in (4, 8, 12):
        caja(marco, 0, yf - 0.12, z, W - 2, 0.12, 0.18)
    caja(gris(), 0, yf - 0.6, H - 1.2, W + 1, 1.4, 1.2)
    # El oso (de lado: mira a +y, hacia el cristal).
    a = mat('oso_den', 0x3a78c8, 0.5)
    ox, oy = 4, yf - 3.2
    esfera(a, ox, oy, 4.2, 2.3, 2, esc=(1.0, 1.0, 1.9))
    esfera(a, ox, oy + 0.6, 9.0, 1.7, 2, esc=(1.0, 1.05, 1.0))
    esfera(a, ox, oy + 2.0, 8.9, 0.75, 2, esc=(0.8, 1.2, 0.7))
    esfera(negro(), ox, oy + 2.75, 9.0, 0.22, 1)
    for s in (-1, 1):
        esfera(a, ox + s * 1.1, oy + 0.4, 10.5, 0.5, 1)
        rama(a, (ox + s * 1.4, oy + 0.6, 7.2), (ox + s * 1.6, oy + 3.0, 8.4), 0.6, 0.45, 8)
        esfera(a, ox + s * 1.6, oy + 3.0, 8.4, 0.5, 1)
        cil(a, ox + s * 1.0, oy, 0, 0.75, 1.6, 10)
        esfera(a, ox + s * 1.0, oy - 0.2, 0.3, 0.7, 1, esc=(1, 1.4, 0.5))

# ================================================================ cruzan la calle
def arco_denver():
    """El arco de WELCOME de la Union Station (el de 1906): los dos pilares de
    hierro en celosía y el arco con las letras de bombillas; por detrás,
    MILE HIGH."""
    h = mat('hierro_den', 0x3a3e46, 0.45)
    for s in (-1, 1):
        for dx in (-0.4, 0.4):
            caja(h, s * 9 + dx, 0, 0, 0.18, 0.5, 7.2)
        for k in range(8):
            caja(h, s * 9, 0, 0.6 + k * 0.85, 0.9, 0.12, 0.1, inclina=0, giro=0)
    n = 24
    for k in range(n):
        a0 = math.pi * k / n
        a1 = math.pi * (k + 1) / n
        p0 = (-math.cos(a0) * 9, 0, 7.2 + math.sin(a0) * 2.4)
        p1 = (-math.cos(a1) * 9, 0, 7.2 + math.sin(a1) * 2.4)
        rama(h, p0, p1, 0.12, 0.12, 6)
    caja(h, 0, 0, 7.0, 18.4, 0.3, 0.25)
    caja(mat('tablero_den', 0x2a2e36, 0.6), 0, 0, 7.6, 9.6, 0.14, 1.5)
    texto(bombilla(), 'WELCOME', 0, -0.2, 8.3, tam=1.3, prof=0.06)
    o = texto(bombilla(), 'MILE HIGH', 0, 0.2, 8.3, tam=1.1, prof=0.06); o.rotation_euler = (math.pi / 2, 0, math.pi)

# ================================================================ la pista de esquí
def pista_esqui():
    """La pista de esquí de las Rocosas (momento estrella, al aire libre): la
    nieve pisada a rayas, las redes naranjas a los lados, bosques de pinos, la
    telesilla con sus torres, el cable y las sillas con gente, esquiadores
    mirando, la cabaña y los arcos de SALIDA y META.
    Cruza la calle: el origen en el centro y la calle a lo largo de y."""
    L = 420
    for k in range(6):
        caja(mat('pisada_a_den' if k % 2 else 'pisada_b_den', 0xf2f6fa if k % 2 else 0xe4ecf4, 0.8),
             -5.5 + k * 2.2, 0, -0.2, 2.2, L, 0.2)
    n = nieve()
    for s in (-1, 1):
        caja(n, s * 20, 0, -0.21, 28, L, 0.2)
    red = mat('red_den', 0xf28a1a, 0.7)
    for s in (-1, 1):
        caja(red, s * 7.4, 0, 0.0, 0.04, L, 1.0)
        for k in range(int(L / 6)):
            cil(gris(), s * 7.4, -L / 2 + 3 + k * 6, 0, 0.04, 1.1, 4)
    for k in range(int(L / 9)):
        y = -L / 2 + 4 + k * 9
        for s in (-1, 1):
            pino(s * (12 + (k * 7 % 5) * 2.2), y, 6 + (k % 3) * 1.6)
            if k % 2:
                pino(s * (22 + (k * 3 % 4) * 2.5), y + 4, 8 + (k % 2) * 2)
    # La telesilla, a la izquierda.
    for k in range(int(L / 40)):
        y = -L / 2 + 20 + k * 40
        cil(gris(), -16, y, 0, 0.35, 10, 10)
        caja(gris(), -16, y, 10, 3.6, 0.5, 0.4)
    cab = negro()
    for s in (-1, 1):
        caja(cab, -16 + s * 1.6, 0, 9.75, 0.06, L, 0.06)
    for k in range(int(L / 14)):
        y = -L / 2 + 7 + k * 14
        x = -16 + (1.6 if k % 2 else -1.6)
        cil(gris(), x, y, 7.0, 0.04, 2.8, 4)
        caja(gris(), x, y, 6.8, 1.4, 0.6, 0.1)
        caja(gris(), x, y + 0.3, 6.8, 1.4, 0.08, 0.6)
        if k % 3:
            persona_esqui(x - 0.3, y - 0.1, [0xc8202a, 0x2a5ab8, 0xf2c21a][k % 3])
    # Esquiadores mirando, la cabaña y los arcos.
    for k in range(int(L / 25)):
        y = -L / 2 + 12 + k * 25
        s = 1 if k % 2 else -1
        persona_esqui(s * 9.0, y, [0xc8202a, 0x2a5ab8, 0xf2c21a, 0x3f8a4a][k % 4])
        persona_esqui(s * 9.6, y + 1.2, [0xf2c21a, 0xe86a2a, 0x8a3ab8][k % 3])
    caja(tronco(), 15, -L / 2 + 30, 0, 8, 6, 3.5)
    tejado(mat('tejado_cabana_den', 0x6a3a2a, 0.8), 15, -L / 2 + 27, -L / 2 + 33, 3.5, 8, 2.5, cumbrera='y')
    caja(n, 15, -L / 2 + 30, 6.0, 8.6, 6.6, 0.25)
    for (y, txt) in ((-L / 2 + 1, 'SALIDA'), (L / 2 - 1, 'META')):
        for s in (-1, 1):
            caja(rojo(), s * 7.6, y, 0, 0.5, 0.5, 5.6)
        caja(rojo(), 0, y, 5.0, 15.7, 0.4, 1.3)
        texto(blanco(), txt, 0, y - 0.22, 5.65, tam=0.9, prof=0.04)

# ================================================================ obstáculos
def _puerta(color):
    """Una puerta del eslalon (se pasa por en medio): dos palos a los lados
    del carril con su bandera hacia fuera."""
    for s in (-1, 1):
        cil(blanco(), s * 1.05, 0, 0, 0.035, 1.9, 6)
        caja(color, s * 1.38, 0, 1.05, 0.66, 0.03, 0.75)
        cil(blanco(), s * 1.71, 0, 1.05, 0.03, 0.8, 6)

def puerta_roja():
    """La puerta roja del eslalon."""
    _puerta(rojo())

def puerta_azul():
    """La puerta azul del eslalon."""
    _puerta(azul())

def pino_nevado():
    """El pino nevado en medio de la pista (no se pasa)."""
    pino(0, 0, 4.6)

def telesilla():
    """Una silla de la telesilla colgando a la altura de la cabeza (agacharse):
    el brazo que baja del cable, el asiento, el respaldo y la barra."""
    g = gris()
    caja(negro(), 0, 0, 4.6, 0.08, 2.4, 0.08)
    cil(g, 0, 0, 2.5, 0.05, 2.15, 6)
    caja(g, 0, 0, 2.45, 1.7, 0.1, 0.08)
    for s in (-1, 1):
        cil(g, s * 0.82, 0, 1.75, 0.04, 0.75, 6)
    caja(mat('asiento_den', 0x2a5ab8, 0.5), 0, 0.1, 1.72, 1.6, 0.55, 0.1)
    caja(mat('asiento_den', 0x2a5ab8, 0.5), 0, 0.36, 1.82, 1.6, 0.08, 0.55)
    caja(g, 0, -0.35, 1.62, 1.5, 0.04, 0.04)

def cartel_colorado():
    """La pancarta de España (agacharse): COLORADO = ROJO."""
    for x in (-1.25, 1.25):
        cil(gris(), x, 0, 0, 0.06, 2.75, 8)
    caja(bandera_es('pancarta_es_obst_den', 1.5, 1.2), 0, 0, 1.5, 2.4, 0.05, 1.2)
    texto(negro(), 'COLORADO', 0, -0.035, 2.15, tam=0.3, prof=0.02)
    texto(blanco(), '= ROJO', 0, -0.035, 1.7, tam=0.22, prof=0.02)

def mallride():
    """El autobús gratuito del 16th Street Mall (no se pasa): bajo, de 5 m,
    azul y gris, con FREE MALLRIDE; el morro mira al jugador y está en el
    origen (el resto, hacia atrás, como los demás coches)."""
    Y = 2.5
    c = mat('mallride_den', 0x5a7a9a, 0.4)
    caja(c, 0, Y, 0.25, 2.1, 5.0, 2.4)
    caja(mat('techo_mall_den', 0xd8dce0, 0.5), 0, Y, 2.65, 2.0, 4.6, 0.3)
    caja(cristal(), 0, Y - 2.52, 1.1, 1.9, 0.04, 1.3)
    for s in (-1, 1):
        caja(cristal(), s * 1.06, Y + 0.3, 1.2, 0.02, 3.8, 1.0)
        for y in (-1.6, 1.6):
            cil(negro(), s * 0.9, Y + y, 0.38, 0.38, 0.25, 14, eje='X')
    caja(negro(), 0, Y - 2.52, 2.35, 1.6, 0.04, 0.28)
    texto(mat('led_den', 0xffb020, 0.3), 'FREE MALLRIDE', 0, Y - 2.55, 2.49, tam=0.18, prof=0.01)
    for s in (-1, 1):
        caja(mat('faro_den', 0xf4ecc0, 0.3), s * 0.75, Y - 2.53, 0.55, 0.3, 0.03, 0.18)

PIEZAS = {
    'capitolio_colorado': (capitolio_colorado, 'denver',     dict(lado=2048, bisel=0.0)),
    'torre_daniels':      (torre_daniels,      'denver',     dict(lado=1024, bisel=0.0)),
    'union_station_den':  (union_station_den,  'denver',     dict(lado=1024, bisel=0.0)),
    'oso_azul':           (oso_azul,           'denver',     dict(lado=1024, bisel=0.0)),
    'arco_denver':        (arco_denver,        'denver',     dict(lado=1024, bisel=0.0, suelo=False)),
    'pista_esqui':        (pista_esqui,        'denver',     dict(lado=2048, bisel=0.0, suelo=False)),
    'puerta_roja':        (puerta_roja,        'obstaculos', dict(lado=256, bisel=0.0)),
    'puerta_azul':        (puerta_azul,        'obstaculos', dict(lado=256, bisel=0.0)),
    'pino_nevado':        (pino_nevado,        'obstaculos', dict(lado=256, bisel=0.0)),
    'telesilla':          (telesilla,          'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
    'cartel_colorado':    (cartel_colorado,    'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
    'mallride':           (mallride,           'obstaculos', dict(lado=256, bisel=0.0)),
}

correr(PIEZAS)
