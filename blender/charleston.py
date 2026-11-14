# Nivel 26: Charleston, Carolina del Sur (14/11/2026).
#
#   blender -b -P blender/charleston.py -- [pieza ...] [--rapido]
#
# Historia: «Se escapa a jugar al golf: pelotas volando y carritos».
#   Por East Bay Street (el arco de CHARLESTON con la palmera y la luna, las
#   casas de colores de Rainbow Row, la iglesia de San Miguel, el Market Hall
#   y las mansiones de la Battery) entre calesas de turistas cuyo caballo va
#   dejando «regalitos»; en el campo de golf, persiguiendo su propia bola; y
#   se llega a la fuente de la piña, con el puente de los diamantes detrás.
# Obstáculos (carpeta obstaculos): la calesa de turistas (el caballo, sin
# patas: son caballo_pata, como el coche de caballos de Central Park), la
# boñiga, el carrito de golf aparcado, el búnker, el estanque, la bolsa de palos, la
# pancarta de FORE! y la bola de golf.

import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import *

def blanco():   return mat('blanco_chs', 0xf6f2ea, 0.55)
def negro():    return mat('negro_chs', 0x1b1c20, 0.4)
def verde():    return mat('verde_chs', 0x2a3a30, 0.5)          # el «verde Charleston» de las contraventanas
def piedra():   return mat('piedra_chs', 0xd8ccb4, 0.7)
def cristal():  return mat('cristal_chs', 0x2a3a4a, 0.25)
def bronce():   return mat('bronce_chs', 0xb08a40, 0.3)
def agua():     return mat('agua_chs', 0x5aa8d0, 0.15)
def hoja():     return mat('hoja_chs', 0x3f7a32, 0.8)
def tronco():   return mat('tronco_chs', 0x7a5a3a, 0.8)
def arena():    return mat('arena_chs', 0xe8d4a0, 0.9)
def goma():     return mat('goma_chs', 0x202024, 0.85)
def amarillo(): return mat('amarillo_chs', 0xf0c020, 0.45)
def rojo():     return mat('rojo_chs', 0xc8282c, 0.45)
def indigo():   return mat('indigo_chs', 0x1a3a6a, 0.5)

PASTELES = [0xf2b8c6, 0xf6dc8c, 0xa8d4e8, 0xc4e0a8, 0xdcc4e8, 0xf4c8a0]

def palmito(x, y, z=0.0, alto=6.0):
    """Una palmera palmito (el árbol de Carolina del Sur)."""
    cil(tronco(), x, y, z, 0.22, alto, 8, r2=0.17)
    for k in range(11):
        a = k * math.tau / 11
        caida = 0.9 + 0.5 * (k % 2)
        rama(hoja(), (x, y, z + alto), (x + math.cos(a) * 2.0, y + math.sin(a) * 2.0, z + alto - caida), 0.16, 0.04, 5)

def roble_musgo(x, y, alto=7.0):
    """Un roble con el musgo español colgando."""
    cil(tronco(), x, y, 0, 0.55, alto * 0.55, 10, r2=0.4)
    copa = mat('copa_roble_chs', 0x3a5a32, 0.85)
    for (dx, dy, dz, r) in ((0, 0, 0.75, 2.8), (-2.2, 0.5, 0.62, 2.2), (2.3, -0.4, 0.65, 2.3), (0.4, 1.8, 0.7, 2.0)):
        esfera(copa, x + dx, y + dy, alto * dz + 1.2, r, 2, esc=(1.25, 1.1, 0.7))
    musgo = mat('musgo_chs', 0x9aa48a, 0.9)
    for k in range(10):
        a = k * math.tau / 10
        px, py = x + math.cos(a) * 2.6, y + math.sin(a) * 2.2
        rama(musgo, (px, py, alto * 0.7), (px + 0.1, py, alto * 0.7 - 1.6 - (k % 3) * 0.4), 0.12, 0.03, 4)

# ================================================================ edificios
def rainbow_row():
    """Rainbow Row: seis casas georgianas estrechas, cada una de un color
    pastel, con contraventanas verdes, cornisa blanca, parapetos distintos y
    balcones de hierro."""
    Y = 7
    anchos = [6.5, 6.0, 7.0, 6.0, 6.5, 6.5]
    x = -sum(anchos) / 2
    vid = cristal()
    for i, w in enumerate(anchos):
        cx = x + w / 2
        h = 10.5 + (i % 3) * 0.8
        m = mat(f'estuco_chs{i}', PASTELES[i % 6], 0.75)
        caja(m, cx, Y, 0, w - 0.05, 12, h)
        caja(blanco(), cx, Y - 6.1, h - 0.6, w, 0.3, 0.35)
        if i % 3 == 1:
            fronton(blanco(), cx, Y - 6.15, h, w * 0.7, 1.2, 0.3)
        elif i % 3 == 0:
            caja(m, cx, Y - 5.85, h, w * 0.6, 0.3, 0.9)
            caja(m, cx, Y - 5.85, h + 0.9, w * 0.3, 0.3, 0.6)
        for z in (4.2, 7.4):
            for dx in (-w * 0.22, w * 0.22):
                ventana(cx + dx, z, 1.0, 1.9, y=Y - 6, marco=blanco(), cristal=vid, persiana=verde())
        puerta(cx - w * 0.22, 0, 1.0, 2.4, y=Y - 6, color=0x2a3a30, marco=blanco())
        ventana(cx + w * 0.22, 0.9, 1.1, 1.7, y=Y - 6, marco=blanco(), cristal=vid, persiana=verde())
        if i % 2 == 0:
            caja(negro(), cx, Y - 6.45, 3.95, w * 0.7, 0.8, 0.08)
            for k in range(7):
                cil(negro(), cx - w * 0.33 + k * w * 0.11, Y - 6.8, 4.03, 0.025, 0.85, 4)
            caja(negro(), cx, Y - 6.8, 4.85, w * 0.7, 0.04, 0.05)
        x += w

def san_miguel():
    """La iglesia de San Miguel: el cuerpo blanco, el pórtico de columnas con
    su frontón y la torre blanca por pisos con el reloj y la aguja."""
    Y = 12
    b = mat('estuco_sm', 0xf4f0e6, 0.6)
    caja(b, 0, Y + 2, 0, 18, 24, 12)
    tejado(mat('tejado_sm', 0x5a5e66, 0.6), 0, Y - 10, Y + 14, 12, 18, 4)
    hastial(b, 0, Y - 10, Y + 14, 12, 18, 4)
    vid = cristal()
    for s in (-1, 1):
        for z in (1.5, 6.5):
            ventana(s * 6.5, z, 1.6, 3.2, y=Y - 10, marco=blanco(), cristal=vid, remate='fronton')
    # La torre: el cuerpo cuadrado, el reloj, los pisos de ocho lados y la aguja.
    ty = Y - 7
    caja(b, 0, ty, 0, 6.5, 6.5, 21)
    caja(blanco(), 0, ty, 21, 7.0, 7.0, 0.5)
    for (z, r, h) in ((21.5, 2.9, 4.5), (26.0, 2.3, 3.6), (29.6, 1.8, 2.6)):
        cil(b, 0, ty, z, r, h, 8)
        cil(blanco(), 0, ty, z + h, r + 0.3, 0.3, 8)
    cil(mat('aguja_sm', 0x5a5e66, 0.6), 0, ty, 32.5, 1.5, 12, 8, r2=0.05)
    esfera(bronce(), 0, ty, 44.6, 0.3, 1)
    cil(blanco(), 0, ty - 3.3, 17.0, 1.25, 0.08, 24, eje='Y')
    rama(negro(), (0, ty - 3.38, 17.0), (0, ty - 3.38, 17.85), 0.06, 0.06, 4)
    rama(negro(), (0, ty - 3.38, 17.0), (0.6, ty - 3.38, 17.0), 0.06, 0.06, 4)
    # El pórtico.
    caja(b, 0, Y - 12, 0, 12, 4, 0.8)
    escalinata(b, 0, Y - 14, 0, 10, 4, huella=0.35, tabica=0.2)
    columnata(blanco(), -4.2, 4.2, 4, Y - 13, 0.8, 0.5, 8.0)
    caja(blanco(), 0, Y - 12, 8.8, 10, 4.4, 1.0)
    fronton(blanco(), 0, Y - 14.2, 9.8, 10.4, 2.6, 4.4)
    caja(mat('puerta_sm', 0x2a3a30, 0.6), 0, Y - 10.05, 0.8, 2.2, 0.1, 3.6)

def mercado_charleston():
    """El Market Hall: el templo de estuco rojizo sobre un piso de arcos, con
    sus columnas, el frontón y las escaleras dobles a los lados."""
    Y = 10
    r = mat('estuco_mk', 0xb0604a, 0.65)
    caja(r, 0, Y, 0, 16, 20, 5)
    for k in range(3):
        x = -5 + k * 5
        caja(negro(), x, Y - 10.05, 0, 2.6, 0.1, 3.0)
        cil(negro(), x, Y - 10.05, 3.0, 1.3, 0.1, 16, eje='Y')
    caja(r, 0, Y + 1, 5, 16, 18, 6.5)
    columnata(mat('columna_mk', 0xf0e6d2, 0.6), -5.4, 5.4, 4, Y - 9.2, 5, 0.55, 7.5)
    caja(r, 0, Y - 8.6, 12.5, 16.4, 3.4, 1.2)
    fronton(r, 0, Y - 10.3, 13.7, 16.8, 3.0, 4.0)
    caja(mat('friso_mk', 0xf0e6d2, 0.6), 0, Y - 10.32, 12.6, 9, 0.06, 0.9)
    texto(r, 'MARKET HALL', 0, Y - 10.4, 13.05, tam=0.75, prof=0.05)
    for s in (-1, 1):
        escalinata(piedra(), s * 9.4, Y - 4, 0, 2.4, 12, huella=0.42, tabica=0.42)
        caja(negro(), s * 10.7, Y - 7, 5.0, 0.06, 6, 0.9)
    # Los tinglados del mercado, detrás.
    caja(mat('tejado_mk', 0x6a6e76, 0.6), 0, Y + 20, 3.2, 12, 22, 0.4)
    for k in range(5):
        for s in (-1, 1):
            cil(blanco(), s * 5.5, Y + 11 + k * 4.5, 0, 0.2, 3.2, 8)

def casa_battery():
    """Una mansión de la Battery: la casa blanca con la galería de dos pisos
    («piazza») y sus columnas, el tejado a cuatro aguas, las chimeneas, la
    verja de hierro y un roble con musgo al lado."""
    Y = 13
    m = mat('estuco_bat', 0xf6ecc8, 0.6)
    caja(m, 0, Y, 0, 18, 16, 11)
    tejado(mat('tejado_bat', 0x4a5058, 0.6), 0, Y - 8, Y + 8, 11, 18, 4, cumbrera='x')
    for s in (-1, 1):
        caja(mat('ladrillo_bat', 0x9a5a42, 0.8), s * 6, Y + 2, 11, 1.2, 1.2, 5.5)
    vid = cristal()
    for z in (1.2, 5.6):
        caja(blanco(), 0, Y - 10, z - 0.4, 18.4, 4, 0.3)
        for k in range(6):
            ventana(-6.5 + k * 2.6, z, 1.3, 2.6, y=Y - 8, marco=blanco(), cristal=vid, persiana=verde())
        for k in range(30):
            cil(blanco(), -8.8 + k * 0.6, Y - 11.85, z - 0.1, 0.04, 0.9, 4)
        caja(blanco(), 0, Y - 11.85, z + 0.8, 18.2, 0.08, 0.08)
    caja(blanco(), 0, Y - 10, 9.6, 18.6, 4.4, 0.35)
    columnata(blanco(), -8.6, 8.6, 6, Y - 11.7, 0.8, 0.3, 4.1)
    columnata(blanco(), -8.6, 8.6, 6, Y - 11.7, 5.2, 0.26, 4.4)
    for k in range(40):
        cil(negro(), -10 + k * 0.5, Y - 14.5, 0, 0.03, 1.4, 4, r2=0.01)
    caja(negro(), 0, Y - 14.5, 1.2, 20, 0.05, 0.06)
    roble_musgo(14, Y - 6)

# ================================================================ la meta
def fuente_pina():
    """La fuente de la piña del parque del puerto (la meta): el estanque
    redondo, la taza de bronce y la piña con sus hojas, los chorros; detrás el
    muelle con los columpios, palmitos, el agua del puerto y, al fondo, el
    puente de las dos torres de diamante."""
    Y = 14
    p = piedra()
    cil(p, 0, Y, 0, 9.0, 0.8, 40)
    cil(agua(), 0, Y, 0.55, 8.5, 0.3, 40)
    cil(p, 0, Y, 0.85, 2.2, 1.6, 24)
    cil(bronce(), 0, Y, 2.45, 3.2, 0.5, 24, r2=2.2)
    cil(agua(), 0, Y, 2.9, 2.9, 0.06, 24)
    piel = mat_bloques('piel_pina', 0xc89a3a, 0x7a5a20, ancho=0.4, alto=0.3, desfase=0.5)
    esfera(piel, 0, Y, 4.6, 1.5, 3, esc=(1, 1, 1.35))
    hojas = mat('hojas_pina', 0x6a8a3a, 0.5)
    for k in range(12):
        a = k * math.tau / 12
        rama(hojas, (0, Y, 6.3), (math.cos(a) * 1.2, Y + math.sin(a) * 1.2, 8.2 + 0.5 * (k % 2)), 0.22, 0.03, 5)
    cil(hojas, 0, Y, 6.2, 0.4, 2.6, 8, r2=0.05)
    chorro = mat('chorro_chs', 0xc8e8f4, 0.1)
    for k in range(12):
        a = k * math.tau / 12 + 0.26
        rama(chorro, (math.cos(a) * 3.0, Y + math.sin(a) * 3.0, 2.9), (math.cos(a) * 5.6, Y + math.sin(a) * 5.6, 0.8), 0.09, 0.14, 5)
    for k in range(10):
        a = k * math.tau / 10
        cil(blanco(), math.cos(a) * 10.5, Y + math.sin(a) * 10.5, 0, 0.12, 1.0, 6)
    # El muelle de los columpios.
    caja(mat('madera_muelle', 0x9a7a5a, 0.8), 0, Y + 16, 0, 34, 6, 0.4)
    caja(mat('tejado_muelle', 0x4a5a4a, 0.6), 0, Y + 16, 4.2, 35, 6.6, 0.35)
    for k in range(8):
        x = -15 + k * (30 / 7)
        for dy in (-2.8, 2.8):
            cil(blanco(), x, Y + 16 + dy, 0.4, 0.12, 3.8, 8)
        if k < 7:
            xs = x + 15 / 7
            for dx in (-0.6, 0.6):
                rama(negro(), (xs + dx, Y + 14.2, 4.2), (xs + dx, Y + 14.2, 1.3), 0.02, 0.02, 4)
            caja(mat('columpio_chs', 0xf6f2ea, 0.6), xs, Y + 14.2, 1.1, 1.6, 0.6, 0.15)
    for (x, y) in ((-14, Y + 4), (14, Y + 4), (-20, Y + 10), (20, Y + 10), (-9, Y + 9), (9, Y + 9)):
        palmito(x, y, 0, 6.5)
    # El agua del puerto y el puente al fondo.
    caja(mat('agua_puerto', 0x3a7aa0, 0.2), 0, Y + 70, -0.15, 260, 100, 0.1)
    pu = mat('puente_chs', 0xe8ecf0, 0.5)
    caja(pu, 0, Y + 75, 16, 220, 4, 1.2)
    for s in (-1, 1):
        tx = s * 28
        for lx in (-5, 5):
            rama(pu, (tx + lx, Y + 75, 0), (tx, Y + 75, 50), 0.9, 0.6, 6)
        caja(pu, tx, Y + 75, 17.2, 11, 1.0, 0.9)
        cab = mat('cable_chs', 0xd8dce4, 0.4)
        for k in range(8):
            for d in (-1, 1):
                rama(cab, (tx, Y + 75, 47 - k * 2.5), (tx + d * (6 + k * 3.2), Y + 75, 17.2), 0.06, 0.06, 4)

# ================================================================ cruzan la calle
def arco_charleston():
    """El arco de CHARLESTON: postes blancos, el letrero añil con la palmera y
    la luna de la bandera de Carolina del Sur."""
    for s in (-1, 1):
        caja(blanco(), s * 9, 0, 0, 0.6, 0.6, 9.4)
    caja(blanco(), 0, 0, 6.2, 18.6, 0.5, 0.4)
    caja(blanco(), 0, 0, 8.6, 18.6, 0.5, 0.4)
    caja(indigo(), 0, 0, 6.6, 17, 0.3, 2.0)
    texto(blanco(), 'CHARLESTON', 0, -0.2, 7.55, tam=1.3, prof=0.07)
    o = texto(blanco(), 'CHARLESTON', 0, 0.2, 7.55, tam=1.3, prof=0.07); o.rotation_euler = (math.pi / 2, 0, math.pi)
    palmito(0, 0, 9.0, 2.6)
    for k in range(9):
        a = math.pi * (0.15 + 0.7 * k / 8)
        esfera(blanco(), -3.2 + math.cos(a) * 0.8, 0, 10.6 + math.sin(a) * 0.8, 0.16, 1)

# ================================================================ el campo de golf
def campo_golf():
    """El campo de golf (momento estrella, al aire libre): la calle de hierba
    segada a rayas a lo largo, el rough a los lados, el camino de los
    carritos, palmitos y robles con musgo, búnkeres y greenes con su bandera,
    el lago con su surtidor, la gente tras la cuerda y el marcador con
    TRUMP -18. Cruza la calle: el origen en el centro y la calle a lo largo de y."""
    L = 420
    for k in range(5):
        caja(mat('calle_golf_a' if k % 2 else 'calle_golf_b', 0x7ab85a if k % 2 else 0x6aa84a, 0.85),
             -4.4 + k * 2.2, 0, -0.2, 2.2, L, 0.2)
    rough = mat('rough_golf', 0x4a8a3a, 0.9)
    for s in (-1, 1):
        caja(rough, s * 16.5, 0, -0.21, 22, L, 0.2)
    caja(mat('camino_golf', 0xb8b4a8, 0.8), -9.5, 0, -0.18, 2.4, L, 0.2)
    carro = mat('carrito_dec', 0xf4f2ec, 0.5)
    for k in range(int(L / 45)):
        y = -L / 2 + 20 + k * 45
        caja(carro, -9.5, y, 0.35, 1.2, 2.2, 0.6)
        caja(carro, -9.5, y + 0.1, 1.9, 1.3, 1.9, 0.08)
        for dy in (-0.8, 0.8):
            cil(carro, -9.5 - 0.55, y + dy, 0.95, 0.04, 0.95, 4)
            cil(carro, -9.5 + 0.55, y + dy, 0.95, 0.04, 0.95, 4)
    for k in range(int(L / 18)):
        y = -L / 2 + 9 + k * 18
        for s in (-1, 1):
            if (k + (s > 0)) % 3 == 0:
                roble_musgo(s * (15 + (k % 2) * 4), y, 6.5)
            else:
                palmito(s * (13 + (k % 3) * 2.5), y + 4, 0, 5.5 + (k % 2))
    are = arena()
    green = mat('green_golf', 0x8ac86a, 0.8)
    for j in range(6):
        y = -L / 2 + 35 + j * 70
        s = 1 if j % 2 else -1
        esfera(are, s * 9.5, y - 12, 0, 1.0, 2, esc=(2.4, 3.6, 0.1), mitad=True)
        cil(green, s * 13.5, y, 0, 4.2, 0.06, 28)
        cil(blanco(), s * 13.5, y, 0, 0.04, 2.6, 6)
        caja(rojo(), s * 13.5 + 0.35, y, 2.0, 0.7, 0.03, 0.45)
        texto(blanco(), str(13 + j), s * 13.5 + 0.35, y - 0.03, 2.22, tam=0.3, prof=0.01)
    # El lago con su surtidor, a la derecha.
    caja(mat('lago_golf', 0x3a8ab8, 0.15), 21, 40, -0.17, 14, 130, 0.1)
    cil(mat('surtidor_golf', 0xd8f0f8, 0.2), 21, 40, 0, 0.25, 3.5, 10, r2=0.05)
    for k in range(12):
        rama(mat('junco_golf', 0x5a7a3a, 0.8), (14.6, -20 + k * 10, 0), (14.4, -20 + k * 10 + 0.3, 1.2), 0.05, 0.02, 4)
    # La gente tras la cuerda, a la izquierda, y el marcador.
    camisas = [0xc8282c, 0x2a5aa8, 0xf4f0e8, 0xf0c020, 0x3f8a4a]
    for k in range(int(L / 6)):
        y = -L / 2 + 3 + k * 6
        if k % 4 == 3:
            continue
        cm = mat(f'camisa_golf{k % 5}', camisas[k % 5], 0.8)
        cil(cm, -12.2, y, 0, 0.32, 1.3, 6)
        esfera(mat('cara_golf', 0xe8b89a, 0.7), -12.2, y, 1.55, 0.25, 1)
        cil(mat('visera_golf', 0xf4f2ec, 0.6), -12.2, y - 0.1, 1.72, 0.3, 0.05, 8)
    for k in range(int(L / 8)):
        cil(blanco(), -11.2, -L / 2 + 4 + k * 8, 0, 0.05, 0.9, 4)
    caja(mat('cuerda_golf', 0xf4e8c8, 0.6), -11.2, 0, 0.85, 0.04, L, 0.04)
    for y in (-L / 2 + 140, L / 2 - 120):
        caja(mat('marcador_golf', 0x1e3a2a, 0.6), -17, y, 0, 0.5, 12, 7)
        o = texto(amarillo(), 'LEADERS', 0, 0, 0, tam=0.9, prof=0.05)
        o.rotation_euler = (math.pi / 2, 0, -math.pi / 2); o.location = (-16.72, y, 6.0)
        for i, (n, sc) in enumerate((('TRUMP', '-18'), ('LIGA', '+4'), ('BOT', '+9'))):
            o = texto(blanco(), f'{n} {sc}', 0, 0, 0, tam=0.8, prof=0.05)
            o.rotation_euler = (math.pi / 2, 0, -math.pi / 2); o.location = (-16.72, y, 4.6 - i * 1.3)
    # La entrada y la salida: muretes de piedra con su letrero.
    for (y, txt) in ((-L / 2 + 2, 'GOLF CLUB'), (L / 2 - 2, '18')):
        for s in (-1, 1):
            caja(piedra(), s * 9, y, 0, 3, 0.8, 1.6)
        caja(mat('letrero_golf', 0x1e3a2a, 0.6), 9, y - 0.45, 1.6, 3.2, 0.1, 1.0)
        texto(amarillo(), txt, 9, y - 0.52, 2.1, tam=0.45, prof=0.03)

# ================================================================ obstáculos
def calesa_tour():
    """La calesa de turistas, de espaldas (va hacia +y): el carro con el toldo
    blanco de flecos, los turistas con sombrero y el cochero; delante, el
    caballo castaño con su sombrero de paja. SIN patas: son caballo_pata
    (como el coche de caballos de Central Park: las caderas en world.js)."""
    ca = mat('carro_calesa', 0x2a3a30, 0.5)
    caja(ca, 0, 0, 0.55, 1.8, 3.4, 0.3)
    caja(ca, 0, -1.65, 0.85, 1.8, 0.1, 0.55)
    for s in (-1, 1):
        caja(ca, s * 0.88, 0, 0.85, 0.06, 3.4, 0.35)
        for y in (-1.1, 1.2):
            cil(negro(), s * 0.95, y, 0.5, 0.5, 0.08, 16, eje='X')
            cil(mat('radio_calesa', 0xc8a040, 0.4), s * 0.99, y, 0.5, 0.12, 0.03, 10, eje='X')
    for s in (-1, 1):
        for y in (-1.6, 1.6):
            cil(blanco(), s * 0.85, y, 0.85, 0.04, 1.6, 6)
    caja(blanco(), 0, 0, 2.45, 2.0, 3.6, 0.1)
    for k in range(18):
        cil(blanco(), -0.95 + k * 0.112, -1.8, 2.25, 0.03, 0.2, 4)
    camisas = [0xc8282c, 0x2a5aa8, 0xf0c020, 0x3f8a4a, 0xe87aa8, 0xf4f0e8]
    for i, y in enumerate((-1.1, -0.3, 0.5)):
        caja(mat('banco_calesa', 0x7a5a3a, 0.7), 0, y, 0.85, 1.6, 0.4, 0.3)
        for j, x in enumerate((-0.45, 0.45)):
            cm = mat(f'turista_calesa{(i * 2 + j) % 6}', camisas[(i * 2 + j) % 6], 0.8)
            cil(cm, x, y, 1.15, 0.24, 0.55, 8)
            esfera(mat('cara_calesa', 0xe8b89a, 0.7), x, y, 1.85, 0.17, 1)
            cil(mat('sombrero_calesa', 0xf0e0b0, 0.7), x, y, 1.97, 0.26, 0.04, 10)
    cil(mat('levita_calesa', 0x1d1f25, 0.5), 0, 1.4, 1.0, 0.24, 0.6, 10)
    esfera(mat('cara_calesa', 0xe8b89a, 0.7), 0, 1.4, 1.75, 0.16, 1)
    cil(mat('sombrero_calesa', 0xf0e0b0, 0.7), 0, 1.4, 1.87, 0.25, 0.04, 10)
    # El caballo (como el de Central Park, castaño).
    c = mat('pelo_calesa', 0x8a5a32, 0.65)
    crin = mat('crin_calesa', 0x3a2416, 0.7)
    esfera(c, 0, 2.55, 1.2, 0.4, 3, esc=(0.78, 1.55, 0.85))
    esfera(c, 0, 2.95, 1.24, 0.3, 3)
    esfera(c, 0, 2.13, 1.27, 0.3, 3)
    rama(c, (0, 2.98, 1.38), (0, 3.28, 1.9), 0.17, 0.11, 12)
    rama(crin, (0, 2.9, 1.5), (0, 3.2, 2.0), 0.05, 0.04, 6)
    rama(c, (0, 3.3, 1.98), (0, 3.52, 1.68), 0.1, 0.075, 12)
    esfera(c, 0, 3.53, 1.65, 0.08, 2)
    for s in (-1, 1):
        rama(c, (s * 0.05, 3.26, 2.02), (s * 0.07, 3.24, 2.18), 0.03, 0.006, 6)
    cil(mat('paja_calesa', 0xe8c870, 0.8), 0, 3.28, 2.1, 0.22, 0.04, 12)
    cil(mat('paja_calesa', 0xe8c870, 0.8), 0, 3.28, 2.1, 0.12, 0.14, 12)
    rama(crin, (0, 1.85, 1.38), (0, 1.75, 0.8), 0.06, 0.035, 6)
    cil(mat('arnes_calesa', 0x241a14, 0.5), 0, 2.75, 1.2, 0.35, 0.07, 18, eje='Y')
    for s in (-1, 1):
        rama(mat('varas_calesa', 0x2a1a12, 0.5), (s * 0.4, 1.6, 0.8), (s * 0.35, 2.6, 1.1), 0.025, 0.025, 6)

def boniga():
    """El «regalito» del caballo de la calesa (saltar): el montoncito marrón
    en espiral y las tres rayitas del olor (fijas)."""
    m = mat('boniga', 0x6a4a2a, 0.7)
    esfera(m, 0, 0, 0, 0.42, 2, esc=(1, 0.9, 0.42), mitad=True)
    esfera(m, 0, 0, 0.14, 0.3, 2, esc=(1, 0.9, 0.55), mitad=True)
    esfera(m, 0, 0, 0.27, 0.18, 2, esc=(1, 0.9, 0.7), mitad=True)
    cil(m, 0, 0, 0.36, 0.07, 0.12, 8, r2=0.01)
    olor = mat('olor', 0x9ac85a, 0.6)
    for k, x in enumerate((-0.18, 0.0, 0.18)):
        z0 = 0.55
        for j in range(3):
            d = 0.06 if (j + k) % 2 else -0.06
            rama(olor, (x + (d if j else 0), 0, z0 + j * 0.12), (x - d, 0, z0 + (j + 1) * 0.12), 0.015, 0.015, 4)

def carrito_parado():
    """El carrito de golf aparcado (no se pasa; el carrito_golf de antes es un vehículo): blanco, con su techo, los asientos y
    la bolsa de palos detrás."""
    w = mat('carrito', 0xf4f2ec, 0.45)
    caja(w, 0, 0, 0.3, 1.25, 2.5, 0.55)
    caja(w, 0, -0.95, 0.85, 1.2, 0.6, 0.35)
    caja(mat('asiento_carrito', 0x2a3a4a, 0.6), 0, 0.15, 0.85, 1.1, 0.7, 0.2)
    caja(mat('asiento_carrito', 0x2a3a4a, 0.6), 0, 0.5, 1.05, 1.1, 0.12, 0.6)
    for sx in (-1, 1):
        for sy in (-0.95, 0.95):
            cil(w, sx * 0.55, sy, 0.85, 0.035, 1.05, 6)
            cil(goma(), sx * 0.6, sy, 0.26, 0.26, 0.2, 14, eje='X')
    caja(w, 0, 0, 1.9, 1.35, 2.3, 0.07)
    caja(cristal(), 0, -1.0, 1.25, 1.1, 0.03, 0.6, inclina=0.15)
    cil(mat('bolsa_palos', 0xc8282c, 0.6), 0, 1.15, 0.8, 0.2, 0.9, 12)
    for k in range(4):
        cil(mat('palo', 0xb8bcc2, 0.3), -0.1 + (k % 2) * 0.2, 1.1 + (k // 2) * 0.1, 1.7, 0.02, 0.25, 4)
        esfera(negro(), -0.1 + (k % 2) * 0.2, 1.1 + (k // 2) * 0.1, 1.97, 0.06, 1)
    for sx in (-1, 1):
        esfera(mat('faro_carrito', 0xfff4c8, 0.2), sx * 0.45, -1.26, 0.6, 0.08, 1)

def bunker():
    """El búnker de arena (saltar): la arena con su borde de césped y el
    rastrillo encima."""
    esfera(mat('borde_bunker', 0x4a8a3a, 0.9), 0, 0, 0, 1.05, 2, esc=(1.25, 0.85, 0.36), mitad=True)
    esfera(arena(), 0, -0.05, 0.05, 0.98, 2, esc=(1.2, 0.8, 0.36), mitad=True)
    rama(mat('rastrillo', 0xb08a5a, 0.6), (-0.6, -0.2, 0.42), (0.7, 0.2, 0.36), 0.03, 0.03, 4)
    caja(mat('rastrillo_cabeza', 0x3a3e44, 0.5), 0.7, 0.2, 0.32, 0.12, 0.5, 0.06, giro=0.3)

def estanque():
    """El estanque (saltar): el borde de piedra, el agua, una hoja de nenúfar
    y los juncos."""
    cil(piedra(), 0, 0, 0, 0.95, 0.32, 18)
    cil(agua(), 0, 0, 0.3, 0.82, 0.04, 18)
    cil(mat('nenufar', 0x5aa040, 0.7), 0.25, -0.2, 0.34, 0.2, 0.02, 10)
    esfera(mat('flor_nenufar', 0xf0a0c0, 0.6), 0.25, -0.2, 0.38, 0.06, 1)
    for k in range(6):
        a = k * math.tau / 6
        rama(mat('junco_golf', 0x5a7a3a, 0.8), (math.cos(a) * 0.8, math.sin(a) * 0.8, 0.3),
             (math.cos(a) * 0.9, math.sin(a) * 0.9, 0.85 + 0.1 * (k % 2)), 0.03, 0.01, 4)

def bolsa_golf():
    """La bolsa de palos caída en la calle (saltar)."""
    cil(mat('bolsa_palos', 0xc8282c, 0.6), 0, 0, 0.3, 0.3, 1.3, 14, eje='X')
    cil(blanco(), 0.55, 0, 0.3, 0.31, 0.1, 14, eje='X')
    for k in range(4):
        rama(mat('palo', 0xb8bcc2, 0.3), (-0.65, -0.12 + k * 0.08, 0.32 + (k % 2) * 0.08), (-1.15, -0.2 + k * 0.12, 0.45 + (k % 2) * 0.1), 0.02, 0.02, 4)
        esfera(negro(), -1.17, -0.2 + k * 0.12, 0.45 + (k % 2) * 0.1, 0.07, 1)

def cartel_fore():
    """La pancarta de FORE! (agacharse)."""
    for x in (-1.25, 1.25):
        cil(blanco(), x, 0, 0, 0.07, 2.75, 8)
        caja(rojo(), x + 0.25, 0, 2.45, 0.45, 0.03, 0.3)
    caja(amarillo(), 0, 0, 1.55, 2.4, 0.06, 1.05)
    texto(negro(), 'FORE!', 0, -0.04, 2.07, tam=0.6, prof=0.03)

def bola_golf():
    """La bola de golf de Trump (se coge donde cae)."""
    esfera(blanco(), 0, 0, 0.22, 0.22, 3)
    for k in range(10):
        a = k * math.tau / 10
        esfera(mat('hoyuelo', 0xd8d4cc, 0.6), math.cos(a) * 0.2, math.sin(a) * 0.2 * 0.3 - 0.08, 0.22 + math.sin(a * 2) * 0.05, 0.03, 1)

PIEZAS = {
    'fuente_pina':        (fuente_pina,        'charleston', dict(lado=2048, bisel=0.0)),
    'rainbow_row':        (rainbow_row,        'charleston', dict(lado=2048, bisel=0.0)),
    'san_miguel':         (san_miguel,         'charleston', dict(lado=2048, bisel=0.0)),
    'mercado_charleston': (mercado_charleston, 'charleston', dict(lado=1024, bisel=0.0)),
    'casa_battery':       (casa_battery,       'charleston', dict(lado=2048, bisel=0.0)),
    'arco_charleston':    (arco_charleston,    'charleston', dict(lado=1024, bisel=0.0, suelo=False)),
    'campo_golf':         (campo_golf,         'charleston', dict(lado=2048, bisel=0.0, suelo=False)),
    'calesa_tour':        (calesa_tour,        'obstaculos', dict(lado=512, bisel=0.0, suelo=False)),
    'boniga':             (boniga,             'obstaculos', dict(lado=256, bisel=0.0)),
    'carrito_parado':     (carrito_parado,     'obstaculos', dict(lado=256, bisel=0.0)),
    'bunker':             (bunker,             'obstaculos', dict(lado=256, bisel=0.0)),
    'estanque':           (estanque,           'obstaculos', dict(lado=256, bisel=0.0)),
    'bolsa_golf':         (bolsa_golf,         'obstaculos', dict(lado=256, bisel=0.0)),
    'cartel_fore':        (cartel_fore,        'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
    'bola_golf':          (bola_golf,          'obstaculos', dict(lado=128, bisel=0.0, suelo=False)),
}

correr(PIEZAS)
