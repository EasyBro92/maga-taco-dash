# Nivel 27: Miami, Florida (14/11/2026). Nivel con jefe.
#
#   blender -b -P blender/miami.py -- [pieza ...] [--rapido]
#
# Historia: «Jefe. El huracán de papeles llega a Mar-a-Lago: carpetas con
#   tachones y cajas de documentos secretos en el baño. Intenta desviarlo con
#   su rotulador».
#   Por Ocean Drive, con el huracán encima (el arco de MIAMI BEACH, los hoteles
#   art déco con sus neones y la playa con las torres de socorrista) mientras
#   las olas cruzan la calle desde la playa; por el baño dorado de Mar-a-Lago,
#   con las lámparas de araña que se balancean entre cajas de documentos y
#   váteres de oro; el jefe (el remolino de papeles, que ya existía); y se
#   llega a Mar-a-Lago.
# Obstáculos (carpeta obstaculos): la ola, la lámpara de araña, el váter de
# oro, la torre de cajas, la cortina de la ducha, los flamencos, la tumbona,
# las sombrillas y la pancarta tachada. (El descapotable ya existía.)

import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import *

def blanco():   return mat('blanco_mia', 0xf8f6f0, 0.5)
def negro():    return mat('negro_mia', 0x1b1c20, 0.4)
def crema():    return mat('crema_mia', 0xf0e4c8, 0.65)
def rosa():     return mat('rosa_mia', 0xf0a0b8, 0.5)
def turquesa(): return mat('turquesa_mia', 0x48c8c0, 0.5)
def oro():      return mat('oro_mia', 0xe8b840, 0.25)
def gris():     return mat('gris_mia', 0x9aa0a8, 0.4)
def cristal():  return mat('cristal_mia', 0x2a4a5a, 0.2)
def arena():    return mat('arena_mia', 0xf0dca8, 0.9)
def mar():      return mat('mar_mia', 0x2a8ac8, 0.15)
def rojo():     return mat('rojo_mia', 0xc8282c, 0.45)
def hoja():     return mat('hoja_mia', 0x3f8a3a, 0.8)
def teja():     return mat_bloques('teja_mia', 0xb8583a, 0x8a3a24, ancho=0.35, alto=0.25)
def neon_rosa(): return luz('neon_rosa_mia', 0xff5aa8, 1.6)
def neon_turq(): return luz('neon_turq_mia', 0x40f0e0, 1.6)

def palmera_real(x, y, alto=11.0):
    """Una palmera real: el tronco gris claro y las hojas que cuelgan en arco."""
    cil(mat('tronco_palmera', 0xc8c0b0, 0.8), x, y, 0, 0.35, alto, 10, r2=0.25)
    cil(mat('capitel_palmera', 0x5a8a3a, 0.7), x, y, alto, 0.27, 1.4, 10, r2=0.2)
    for k in range(12):
        a = k * math.tau / 12
        top = (x, y, alto + 1.4)
        mid = (x + math.cos(a) * 1.7, y + math.sin(a) * 1.7, alto + 2.0 - 0.2 * (k % 2))
        fin = (x + math.cos(a) * 3.3, y + math.sin(a) * 3.3, alto + 0.4 - 0.4 * (k % 3))
        rama(hoja(), top, mid, 0.18, 0.13, 5)
        rama(hoja(), mid, fin, 0.13, 0.03, 5)

def cajas_pila(x, y, cols, filas, giro=0.0, sello=True):
    """Una pila de cajas de documentos (blancas, con su tapa) mirando a -y."""
    cj = mat('caja_doc_mia', 0xf2eee4, 0.7)
    tapa = mat('tapa_doc_mia', 0xd8d0c0, 0.7)
    for f in range(filas):
        for c in range(cols):
            cx = x + (c - (cols - 1) / 2) * 0.74 + (0.04 if f % 2 else 0)
            caja(cj, cx, y, f * 0.4, 0.7, 0.48, 0.34, giro=giro)
            caja(tapa, cx, y, f * 0.4 + 0.34, 0.72, 0.5, 0.05, giro=giro)
            if sello and (f + c) % 2 == 0:
                texto(rojo(), 'TOP SECRET', cx, y - 0.25, f * 0.4 + 0.17, tam=0.08, prof=0.01)

def inodoro(x, y, z=0.0, m=None):
    """Un váter de oro mirando a -y: la taza, el asiento abierto y la cisterna."""
    m = m or oro()
    cil(m, x, y, z, 0.2, 0.3, 14, r2=0.26)
    cil(m, x, y - 0.05, z + 0.3, 0.27, 0.12, 16)
    cil(mat('agua_vater', 0x8ac8e8, 0.1), x, y - 0.05, z + 0.4, 0.2, 0.03, 14)
    caja(m, x, y + 0.27, z + 0.42, 0.52, 0.06, 0.48, inclina=-0.15)
    caja(m, x, y + 0.42, z + 0.3, 0.5, 0.22, 0.55)
    caja(m, x, y + 0.42, z + 0.85, 0.54, 0.25, 0.05)

# ================================================================ la meta
def mar_a_lago():
    """Mar-a-Lago (la meta): la casa de estuco crema con tejados de teja, la
    galería de arcos, la torre con el mirador y el tejado de pirámide, las
    alas, las palmeras reales, la bandera grande, el arco de la entrada y, por
    el césped, papeles del huracán y cajas de documentos junto a la puerta."""
    Y = 22
    W, D, H = 48.0, 22.0, 11.0
    yf = Y - D / 2
    c = crema()
    caja(c, 0, Y, 0, W, D, H)
    tejado(teja(), 0, Y - D / 2, Y + D / 2, H, W, 3.5, cumbrera='x')
    hueco = mat('hueco_mia', 0x3a2a20, 0.8)
    for k in range(11):
        x = -20 + k * 4
        caja(hueco, x, yf - 0.05, 0, 2.4, 0.1, 3.4)
        cil(hueco, x, yf - 0.05, 3.4, 1.2, 0.1, 16, eje='Y')
        caja(c, x + 2, yf - 0.35, 0, 0.7, 0.7, 4.8)
    caja(c, 0, yf - 0.9, 4.8, W, 1.8, 0.3)
    persiana = mat('persiana_mia', 0x3a8a8a, 0.6)
    for k in range(10):
        x = -18 + k * 4
        if abs(x) < 5:
            continue
        ventana(x, 6.6, 1.3, 2.4, y=yf, marco=blanco(), cristal=cristal(), persiana=persiana)
    # La torre con el mirador.
    ty = yf + 3
    caja(c, 0, ty, 0, 9, 9, 24)
    for z in (8, 13, 18):
        caja(cristal(), 0, ty - 4.55, z, 1.6, 0.1, 2.6)
        cil(cristal(), 0, ty - 4.55, z + 2.6, 0.8, 0.1, 12, eje='Y')
    caja(c, 0, ty, 24, 9.6, 9.6, 0.5)
    for sx in (-1, 1):
        for sy in (-1, 1):
            caja(c, sx * 4.2, ty + sy * 4.2, 24.5, 1.2, 1.2, 4.0)
    caja(c, 0, ty, 28.5, 9.8, 9.8, 0.6)
    o = cil(teja(), 0, ty, 29.1, 7.4, 4.6, 4, r2=0.05)
    o.rotation_euler = (0, 0, math.pi / 4)
    esfera(oro(), 0, ty, 33.9, 0.35, 1)
    # Las alas.
    for s in (-1, 1):
        caja(c, s * 31, Y + 3, 0, 14, 16, 7.5)
        tejado(teja(), s * 31, Y - 5, Y + 11, 7.5, 14, 2.8, cumbrera='x')
        for k in range(3):
            caja(hueco, s * 31 - 4 + k * 4, Y - 5.05, 0, 2.2, 0.1, 3.2)
            cil(hueco, s * 31 - 4 + k * 4, Y - 5.05, 3.2, 1.1, 0.1, 14, eje='Y')
    # El césped, el arco de la entrada, las palmeras y la bandera.
    caja(mat('cesped_mia', 0x5a9a4a, 0.9), 0, yf - 7, -0.05, 70, 14, 0.06)
    for s in (-1, 1):
        caja(c, s * 4.6, yf - 9, 0, 1.4, 1.4, 6.2)
        palmera_real(s * 8, yf - 4, 11)
        palmera_real(s * 14, yf - 3, 12)
        palmera_real(s * 20, yf - 5, 10.5)
    caja(c, 0, yf - 9, 6.2, 10.6, 1.4, 1.2)
    caja(oro(), 0, yf - 9.75, 6.3, 7.0, 0.08, 1.0)
    texto(negro(), 'MAR-A-LAGO', 0, yf - 9.8, 6.8, tam=0.75, prof=0.04)
    cil(gris(), 18, yf - 6, 0, 0.15, 22, 8)
    caja(mat_franjas('bandera_mia', 0xc8282c, 0xf8f6f0, 13, eje='Z', z0=-1.4, alto=2.8), 20.6, yf - 6, 18.4, 5.0, 0.06, 2.8)
    caja(mat('canton_mia', 0x2a3a8a, 0.6), 19.2, yf - 6.04, 19.7, 2.2, 0.06, 1.5)
    # Lo que ha dejado el huracán: cajas junto a la puerta y papeles por el césped.
    cajas_pila(-2.8, yf - 1.2, 2, 3)
    cajas_pila(2.8, yf - 1.2, 2, 2)
    pap = mat('papel_mia', 0xf8f6f0, 0.6)
    for k in range(18):
        x = -14 + (k * 7.3) % 28
        y = yf - 3 - (k * 3.7) % 9
        caja(pap, x, y, 0.02, 0.5, 0.7, 0.01, giro=k * 0.7)
        if k % 3 == 0:
            caja(negro(), x, y, 0.035, 0.3, 0.08, 0.005, giro=k * 0.7)

# ================================================================ edificios
def _hotel(c1, c2, neon, letrero):
    """Un hotel art déco de Ocean Drive: blanco con franjas de color, viseras
    sobre las ventanas, la aleta central con el nombre en neón, la marquesina
    y la terraza con sombrillas."""
    Y = 8
    W, D, H = 20.0, 14.0, 14.0
    yf = Y - D / 2
    caja(blanco(), 0, Y, 0, W, D, H)
    caja(c1, 0, yf - 0.1, H, W + 0.4, 0.4, 0.6)
    for z in (3.6, 7.0, 10.4):
        caja(c1, 0, yf - 0.06, z, W + 0.1, 0.12, 0.45)
        caja(c1, 0, yf - 0.5, z + 2.55, W, 1.0, 0.08)
    for z in (4.3, 7.7, 11.1):
        for k in range(5):
            if k == 2:
                continue
            caja(cristal(), -8 + k * 4, yf - 0.03, z, 2.6, 0.06, 1.6)
    caja(c2, 0, yf - 0.8, 0, 3.2, 1.6, 18.5)
    caja(blanco(), 0, yf - 0.8, 18.5, 2.4, 1.2, 1.2)
    caja(c2, 0, yf - 0.8, 19.7, 1.2, 0.8, 1.6)
    for i, ch in enumerate(letrero):
        texto(neon, ch, 0, yf - 1.62, 16.6 - i * 1.6, tam=1.25, prof=0.06)
    caja(cristal(), 0, yf - 0.05, 0.3, 16, 0.1, 2.6)
    caja(c1, 0, yf - 1.6, 3.0, 12, 3.2, 0.3)
    caja(negro(), 0, yf - 3.18, 2.5, 6, 0.08, 0.8)
    texto(neon, 'HOTEL', 0, yf - 3.24, 2.9, tam=0.55, prof=0.04)
    for k, x in enumerate((-7.5, -4.5, 4.5, 7.5)):
        cil(blanco(), x, yf - 5, 0, 0.45, 0.75, 12)
        cil(gris(), x, yf - 5, 0, 0.04, 2.4, 6)
        cil(c1 if k % 2 else c2, x, yf - 5, 2.1, 1.4, 0.45, 12, r2=0.05)

def hotel_deco_rosa():
    """El hotel art déco rosa (con OCEAN en neón)."""
    _hotel(rosa(), mat('menta_mia', 0x9ae0c8, 0.5), neon_rosa(), 'OCEAN')

def hotel_deco_azul():
    """El hotel art déco turquesa (con TIDES en neón)."""
    _hotel(turquesa(), mat('melocoton_mia', 0xf8c8a0, 0.5), neon_turq(), 'TIDES')

def playa_socorrista():
    """La playa de Ocean Drive: la arena, el mar con la espuma, la torre de
    socorrista de colores con su rampa y su bandera, palmeras, sombrillas y
    tumbonas."""
    Y = 10
    caja(arena(), 0, Y, -0.05, 40, 22, 0.1)
    caja(mar(), 0, Y + 17, -0.08, 40, 12, 0.06)
    caja(blanco(), 0, Y + 10.8, -0.04, 40, 0.7, 0.05)
    for sx in (-1, 1):
        for sy in (-1, 1):
            cil(blanco(), sx * 1.1, Y + sy * 1.1, 0, 0.12, 2.6, 8)
    caja(mat_franjas('franjas_socorrista', 0xf0a0b8, 0xf6dc6a, 6, eje='X', z0=-1.6, alto=3.2), 0, Y, 2.6, 3.2, 3.0, 2.2)
    caja(turquesa(), 0, Y, 4.8, 3.8, 3.6, 0.3)
    caja(cristal(), 0, Y - 1.53, 3.3, 2.0, 0.06, 0.9)
    caja(mat('rampa_socorrista', 0xd8c8a8, 0.8), 0, Y - 3.5, 1.24, 1.2, 4.8, 0.12, inclina=0.57)
    cil(gris(), 1.5, Y - 1.5, 5.1, 0.05, 2.2, 6)
    caja(rojo(), 2.1, Y - 1.5, 6.6, 1.1, 0.04, 0.7)
    for (x, y, h) in ((-12, Y - 4, 10), (12, Y - 3, 11), (-17, Y + 3, 9), (17, Y + 4, 10.5)):
        palmera_real(x, y, h)
    for k, (x, y) in enumerate(((-7, Y - 3), (7, Y + 2), (-15, Y + 5), (15, Y - 5))):
        cil(gris(), x, y, 0, 0.04, 2.3, 6)
        cil(rosa() if k % 2 else turquesa(), x, y, 2.0, 1.5, 0.5, 12, r2=0.05)
        caja(blanco(), x + 1.6, y, 0.25, 0.7, 1.8, 0.12)

# ================================================================ cruzan la calle
def arco_miami():
    """El arco de MIAMI BEACH: pilonos art déco escalonados (rosa y
    turquesa), el letrero con el neón y una palmera a cada lado."""
    for s in (-1, 1):
        caja(rosa(), s * 9, 0, 0, 1.4, 1.4, 7.0)
        caja(turquesa(), s * 9, 0, 7.0, 1.0, 1.0, 2.2)
        caja(rosa(), s * 9, 0, 9.2, 0.6, 0.6, 1.0)
    caja(blanco(), 0, 0, 6.2, 18.6, 0.6, 0.4)
    caja(blanco(), 0, 0, 8.6, 18.6, 0.6, 0.4)
    caja(mat('fondo_arco_mia', 0x1e2a3a, 0.5), 0, 0, 6.6, 17, 0.3, 2.0)
    texto(neon_turq(), 'MIAMI BEACH', 0, -0.2, 7.55, tam=1.25, prof=0.07)
    o = texto(neon_rosa(), 'MIAMI BEACH', 0, 0.2, 7.55, tam=1.25, prof=0.07); o.rotation_euler = (math.pi / 2, 0, math.pi)

# ================================================================ el baño dorado
def bano_dorado():
    """El baño dorado de Mar-a-Lago (momento estrella): el suelo de mármol,
    las paredes de oro con espejos, el techo con luces, y a los lados váteres
    de oro, lavabos de mármol y pilas de cajas de documentos con TOP SECRET.
    Cruza la calle: el origen en el centro y la calle a lo largo de y."""
    L = 420
    marmol = mat_bloques('marmol_mia', 0xf2ece0, 0xd8cfc0, ancho=4.0, alto=4.0, grosor=0.01, variacion=1.04)
    caja(marmol, 0, 0, -0.2, 26, L, 0.2)
    o_ = oro()
    oscuro = mat('oro_oscuro_mia', 0xb08a30, 0.35)
    espejo = mat('espejo_mia', 0xc8d8e0, 0.05)
    for s in (-1, 1):
        caja(o_, s * 13, 0, 0, 0.6, L, 10)
        for k in range(int(L / 12)):
            y = -L / 2 + 6 + k * 12
            caja(espejo, s * 12.68, y, 2.0, 0.04, 6, 5.5)
            caja(oscuro, s * 12.6, y + 6, 0, 0.4, 0.8, 10)
    caja(mat('techo_mia', 0x8a6a3a, 0.6), 0, 0, 10, 27, L, 0.5)
    foco = luz('foco_mia', 0xfff0c8, 1.3)
    for k in range(int(L / 20)):
        for s in (-1, 1):
            caja(foco, s * 6, -L / 2 + 10 + k * 20, 9.8, 1.2, 1.2, 0.2)
    lav = mat('marmol_lavabo', 0xe8e0d4, 0.4)
    for s in (-1, 1):
        for k in range(int(L / 10)):
            y = -L / 2 + 5 + k * 10
            tipo = (k + (s > 0)) % 3
            if tipo == 0:
                inodoro(s * 10.5, y)
                inodoro(s * 10.5, y + 2.2)
            elif tipo == 1:
                cajas_pila(s * 9.8, y, 2, 4 + k % 3)
                cajas_pila(s * 9.8, y + 1.2, 3, 2 + k % 2, sello=False)
            else:
                caja(lav, s * 11.6, y, 0, 1.2, 3.2, 0.9)
                for dy in (-0.8, 0.8):
                    cil(o_, s * 11.8, y + dy, 0.9, 0.05, 0.35, 6)
                    rama(o_, (s * 11.8, y + dy, 1.25), (s * 11.45, y + dy, 1.2), 0.04, 0.03, 6)
                caja(mat_franjas('cortina_mia', 0xf0a0b8, 0xf8f6f0, 10, eje='Y', z0=-1.5, alto=3.0), s * 8.6, y, 0.4, 0.04, 3.0, 2.6)
                caja(o_, s * 8.6, y, 3.0, 0.08, 3.2, 0.06)
    for (y, txt) in ((-L / 2 + 0.5, 'MAR-A-LAGO'), (L / 2 - 0.5, 'EXIT')):
        for s in (-1, 1):
            caja(o_, s * 9, y, 0, 8.6, 1.0, 10.2)
        caja(o_, 0, y, 7.5, 9.6, 1.0, 2.7)
        caja(mat('fondo_letrero_mia', 0x2a1a10, 0.5), 0, y - 0.6, 8.0, 8, 0.2, 1.6)
        texto(oro(), txt, 0, y - 0.72, 8.8, tam=1.0, prof=0.06)

# ================================================================ obstáculos
def ola():
    """La ola del huracán que cruza la calle desde la playa (saltar): el agua
    alargada a lo largo de la calle, la cresta que se riza hacia la izquierda
    (-x) y la espuma."""
    a = mar()
    esfera(a, 0, 0, 0, 1.0, 2, esc=(0.9, 1.7, 0.62), mitad=True)
    esfera(mat('mar_claro_mia', 0x5ab8e0, 0.15), -0.25, 0, 0.45, 0.6, 2, esc=(0.75, 2.6, 0.55))
    esp = blanco()
    for k in range(9):
        y = -1.45 + k * 0.36
        esfera(esp, -0.45, y, 0.85 + 0.06 * (k % 2), 0.2 + 0.04 * (k % 3), 1)
        esfera(esp, -0.7, y + 0.15, 0.62, 0.13, 1)
    for k in range(6):
        esfera(esp, 0.6, -1.4 + k * 0.56, 0.08, 0.16, 1)

def lampara_arana():
    """La lámpara de araña del baño dorado (agacharse; se balancea de lado a
    lado en el juego): la cadena desde el techo (arriba, a 7,6 m) y la lámpara
    de oro con sus brazos, las velas y los cristales colgando."""
    o_ = oro()
    for k in range(14):
        z = 7.6 - k * 0.42
        cil(o_, 0, 0, z - 0.3, 0.05 if k % 2 else 0.035, 0.3, 6)
    cil(o_, 0, 0, 1.55, 0.12, 1.85, 10)
    esfera(o_, 0, 0, 1.45, 0.22, 2)
    cil(o_, 0, 0, 2.05, 0.75, 0.08, 20)
    cil(o_, 0, 0, 2.55, 0.45, 0.06, 16)
    vela = luz('vela_mia', 0xffe8a0, 1.4)
    cristal_l = mat('cristal_lampara', 0xd8f0f8, 0.05)
    for k in range(8):
        a = k * math.tau / 8
        x, y = math.cos(a) * 0.75, math.sin(a) * 0.75
        rama(o_, (0, 0, 1.75), (x, y, 2.1), 0.03, 0.03, 5)
        cil(blanco(), x, y, 2.13, 0.04, 0.18, 6)
        esfera(vela, x, y, 2.36, 0.05, 1)
        esfera(cristal_l, x * 0.95, y * 0.95, 1.9, 0.06, 1, esc=(1, 1, 1.6))
    for k in range(6):
        a = k * math.tau / 6 + 0.3
        esfera(cristal_l, math.cos(a) * 0.4, math.sin(a) * 0.4, 1.3, 0.07, 1, esc=(1, 1, 1.8))

def inodoro_oro():
    """El váter de oro (saltar), sobre su peana de mármol."""
    caja(mat('marmol_lavabo', 0xe8e0d4, 0.4), 0, 0, 0, 0.8, 1.0, 0.08)
    inodoro(0, -0.1, 0.08)

def torre_cajas():
    """La torre de cajas de documentos secretos (no se pasa), con papeles
    tachados asomando."""
    cajas_pila(0, 0, 2, 5)
    pap = mat('papel_mia', 0xf8f6f0, 0.6)
    for k in range(4):
        x = -0.5 + k * 0.33
        caja(pap, x, -0.2, 2.0 + (k % 2) * 0.1, 0.3, 0.02, 0.38, giro=0.2 * (k - 1.5))
        caja(negro(), x, -0.215, 2.15 + (k % 2) * 0.1, 0.22, 0.01, 0.05, giro=0.2 * (k - 1.5))

def cortina_ducha():
    """La cortina de la ducha en su barra (agacharse)."""
    for x in (-1.2, 1.2):
        cil(oro(), x, 0, 0, 0.05, 2.75, 8)
    cil(oro(), 0, 0, 2.7, 0.04, 2.4, 6, eje='X')
    caja(mat_franjas('cortina_obst', 0xf0a0b8, 0xf8f6f0, 12, eje='X', z0=-1.2, alto=2.4), 0, 0, 1.55, 2.3, 0.04, 1.15)
    for k in range(9):
        esfera(oro(), -1.1 + k * 0.275, 0, 2.7, 0.04, 1)

def _flamenco(x, y, giro=0.0, pata=False):
    r = rosa()
    pico = negro()
    esfera(r, x, y, 1.05, 0.26, 2, esc=(0.7, 1.25, 0.72))
    esfera(r, x, y - 0.25, 1.15, 0.13, 1)
    rama(r, (x, y + 0.25, 1.15), (x, y + 0.4, 1.45), 0.06, 0.05, 6)
    rama(r, (x, y + 0.4, 1.45), (x, y + 0.25, 1.7), 0.05, 0.045, 6)
    esfera(r, x, y + 0.2, 1.75, 0.09, 1)
    rama(mat('pico_rosa', 0xf8d0d8, 0.5), (x, y + 0.13, 1.75), (x, y + 0.02, 1.67), 0.035, 0.02, 5)
    rama(pico, (x, y + 0.02, 1.67), (x, y - 0.03, 1.6), 0.02, 0.008, 5)
    patas = mat('pata_flamenco', 0xe87a98, 0.6)
    rama(patas, (x + 0.06, y, 0.85), (x + 0.06, y, 0), 0.02, 0.02, 4)
    if pata:
        rama(patas, (x - 0.06, y, 0.85), (x - 0.06, y - 0.2, 0.55), 0.02, 0.02, 4)
        rama(patas, (x - 0.06, y - 0.2, 0.55), (x - 0.06, y + 0.05, 0.6), 0.02, 0.02, 4)
    else:
        rama(patas, (x - 0.06, y, 0.85), (x - 0.06, y, 0), 0.02, 0.02, 4)

def flamencos():
    """Tres flamencos rosas (no se pasa); uno a la pata coja."""
    _flamenco(-0.5, 0.1)
    _flamenco(0.05, -0.15, pata=True)
    _flamenco(0.55, 0.15)

def tumbona():
    """La tumbona de playa con su toalla (saltar)."""
    b = blanco()
    caja(b, 0, 0.2, 0.3, 0.75, 1.5, 0.08)
    caja(b, 0, -0.7, 0.3, 0.75, 0.6, 0.08, inclina=-0.6)
    for sx in (-1, 1):
        for y in (-0.6, 0.8):
            cil(gris(), sx * 0.33, y, 0, 0.025, 0.3, 4)
    caja(mat_franjas('toalla_mia', 0x48c8c0, 0xf6dc6a, 6, eje='Y', z0=-0.7, alto=1.4), 0, 0.1, 0.38, 0.6, 1.4, 0.02)

def sombrilla():
    """Dos sombrillas de playa a los lados del carril, con las telas que se
    juntan a la altura de la cabeza (agacharse)."""
    for k, sx in enumerate((-1.1, 1.1)):
        cil(gris(), sx, 0, 0, 0.04, 2.35, 6)
        cil(rosa() if k else turquesa(), sx * 0.75, 0, 1.75, 1.35, 0.55, 12, r2=0.05)
        esfera(blanco(), sx * 0.75, 0, 2.32, 0.06, 1)

def cartel_tachado():
    """El documento gigante con tachones negros y TOP SECRET (agacharse)."""
    for x in (-1.25, 1.25):
        cil(gris(), x, 0, 0, 0.06, 2.75, 8)
    caja(mat('papel_mia', 0xf8f6f0, 0.6), 0, 0, 1.5, 2.4, 0.05, 1.2)
    texto(rojo(), 'TOP SECRET', 0, -0.035, 2.45, tam=0.28, prof=0.02)
    for k, w in enumerate((1.8, 1.2, 1.9, 1.5)):
        caja(negro(), -0.1 + (k % 2) * 0.1, -0.035, 1.62 + k * 0.17, w, 0.01, 0.1)

PIEZAS = {
    'mar_a_lago':        (mar_a_lago,        'miami',      dict(lado=2048, bisel=0.0)),
    'hotel_deco_rosa':   (hotel_deco_rosa,   'miami',      dict(lado=1024, bisel=0.0)),
    'hotel_deco_azul':   (hotel_deco_azul,   'miami',      dict(lado=1024, bisel=0.0)),
    'playa_socorrista':  (playa_socorrista,  'miami',      dict(lado=1024, bisel=0.0)),
    'arco_miami':        (arco_miami,        'miami',      dict(lado=1024, bisel=0.0, suelo=False)),
    'bano_dorado':       (bano_dorado,       'miami',      dict(lado=2048, bisel=0.0, suelo=False)),
    'ola':               (ola,               'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
    'lampara_arana':     (lampara_arana,     'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
    'inodoro_oro':       (inodoro_oro,       'obstaculos', dict(lado=256, bisel=0.0)),
    'torre_cajas':       (torre_cajas,       'obstaculos', dict(lado=256, bisel=0.0)),
    'cortina_ducha':     (cortina_ducha,     'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
    'flamencos':         (flamencos,         'obstaculos', dict(lado=256, bisel=0.0)),
    'tumbona':           (tumbona,           'obstaculos', dict(lado=256, bisel=0.0)),
    'sombrilla':         (sombrilla,         'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
    'cartel_tachado':    (cartel_tachado,    'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
}

correr(PIEZAS)
