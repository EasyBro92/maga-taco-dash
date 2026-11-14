# Nivel 28: Albuquerque, Nuevo México (14/11/2026).
#
#   blender -b -P blender/albuquerque.py -- [pieza ...] [--rapido]
#
# Historia: «El festival de globos. Primeros carteles españoles. Un platillo
#   volante de Roswell (guiño a AlienZ)». Empieza el acto de la Armada
#   Española: España viene a reclamar los nombres que puso en el Oeste.
#   Por Central Avenue (la Ruta 66) por la mañana: el arco de la ROUTE 66 con
#   la pancarta de España («ALBURQUERQUE», con la R que perdió la ciudad), el
#   teatro KiMo, casas de adobe con ristras de chiles y el motel con su neón;
#   el platillo de Roswell que baja su rayo sobre tu carril; el campo de la
#   fiesta de los globos, con globos que aterrizan en la calle; y se llega a la
#   plaza del Old Town, ante la iglesia de San Felipe Neri.
# Obstáculos (carpeta obstaculos): el globo, el globo de España, el platillo,
# el horno de adobe, la ristra de chiles, la pancarta de ALBURQUERQUE, el
# lowrider y la cesta caída.

import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import *

def blanco():   return mat('blanco_abq', 0xf6f1e6, 0.5)
def negro():    return mat('negro_abq', 0x1c1c20, 0.4)
def adobe():    return mat_bloques('adobe_abq', 0xc89468, 0xb88458, ancho=1.6, alto=0.9, grosor=0.006, variacion=1.05)
def adobe_c():  return mat('adobe_claro_abq', 0xdcb48a, 0.9)
def estuco():   return mat('estuco_abq', 0xe8d2b0, 0.85)
def terracota(): return mat('terracota_abq', 0xb8583a, 0.7)
def turquesa(): return mat('turquesa_abq', 0x2fa8a0, 0.5)
def viga():     return mat('viga_abq', 0x6a4a30, 0.8)
def chile_r():  return mat('chile_abq', 0xb81c18, 0.45)
def gris():     return mat('gris_abq', 0x9aa0a8, 0.4)
def cristal():  return mat('cristal_abq', 0x2a3e4a, 0.2)
def rojo():     return mat('rojo_abq', 0xc8202a, 0.45)
def amarillo(): return mat('amarillo_abq', 0xf2c21a, 0.45)
def hierba():   return mat('hierba_abq', 0x7aa04a, 0.9)
def mimbre():   return mat_bloques('mimbre_abq', 0xa8783e, 0x7a5228, ancho=0.12, alto=0.08, grosor=0.02)
def neon_rojo(): return luz('neon_rojo_abq', 0xff3a3a, 1.6)
def neon_turq(): return luz('neon_turq_abq', 0x40f0e0, 1.6)
def neon_amar(): return luz('neon_amar_abq', 0xffd040, 1.6)

def bandera_es(nombre, z0, alto):
    """Las franjas de la bandera de España (roja, amarilla, roja) en z0..z0+alto."""
    return mat_franjas(nombre, 0xc8202a, 0xf2c21a, 3, eje='Z', z0=z0, alto=alto)

def ristra(x, y, z, largo=1.2):
    """Una ristra de chiles rojos colgando de (x, y, z)."""
    cil(mat('cuerda_abq', 0xc8b08a, 0.9), x, y, z - largo, 0.02, largo, 4)
    c = chile_r()
    for k in range(int(largo / 0.11)):
        zz = z - 0.08 - k * 0.11
        for j in range(3):
            a = j * math.tau / 3 + k * 0.9
            esfera(c, x + math.cos(a) * 0.07, y + math.sin(a) * 0.07, zz, 0.06, 1, esc=(0.8, 0.8, 1.6))

def vigas(x0, x1, y, z, paso=1.1):
    """Las vigas de madera que asoman por la fachada (mira a -y) bajo el pretil."""
    v = viga()
    n = int((x1 - x0) / paso)
    for k in range(n + 1):
        cil(v, x0 + k * paso, y - 0.45, z, 0.13, 0.9, 8, eje='Y')

def globo(x, y, z, r, c1, c2, cesta=True, n=8, nombre='gores_abq'):
    """Un globo aerostático: la envoltura a gajos de dos colores, la boca, las
    cuerdas, el quemador y la cesta de mimbre (con z en el fondo de la cesta)."""
    hz = z + 2.7 + r * 1.55             # centro de la envoltura (la boca, a 2,7 m)
    g = mat_franjas(nombre, c1, c2, n, eje='X', z0=x - r, alto=2 * r)
    esfera(g, x, y, hz, r, 3, esc=(1, 1, 1.12))
    cil(g, x, y, hz - r * 1.55, r * 0.32, r * 0.9, 16, r2=r * 0.86)
    if cesta:
        cu = mat('cuerda_abq', 0xc8b08a, 0.9)
        for sx in (-1, 1):
            for sy in (-1, 1):
                rama(cu, (x + sx * 0.45, y + sy * 0.45, z + 1.05), (x + sx * r * 0.3, y + sy * r * 0.3, hz - r * 1.55), 0.02, 0.02, 4)
        cil(gris(), x, y, z + 1.6, 0.18, 0.35, 8)
        caja(mimbre(), x, y, z, 1.1, 1.1, 1.05)
        caja(viga(), x, y, z + 1.02, 1.18, 1.18, 0.08)

# ================================================================ la meta
def san_felipe_neri():
    """La plaza del Old Town y la iglesia de San Felipe Neri (la meta): el
    adobe con sus dos torres blancas de madera con el chapitel y la cruz, la
    portada, el quiosco de la plaza, los álamos, las ristras y, de España, la
    pancarta ALBURQUERQUE (con la R) y su bandera."""
    Y = 22
    W, D, H = 16.0, 24.0, 10.0
    yf = Y - D / 2
    a = adobe()
    caja(a, 0, Y, 0, W, D, H)
    tejado(mat('tejado_sfn', 0x6a5a4a, 0.8), 0, Y - D / 2, Y + D / 2, H, W, 2.4, cumbrera='y')
    # La fachada: el hastial escalonado, la portada y la ventana del coro.
    for k, (w, h) in enumerate(((12, 1.2), (8, 1.0), (4, 0.9))):
        caja(a, 0, yf + 0.2, H + k * 1.1, w, 0.8, h + 0.1)
    caja(blanco(), 0, yf - 0.1, 0, 3.6, 0.3, 5.0)
    puerta(0, 0, 2.6, 4.2, y=yf - 0.25, color=0x5a3a22, marco=blanco())
    cil(blanco(), 0, yf - 0.25, 6.6, 1.0, 0.1, 16, eje='Y')
    cil(cristal(), 0, yf - 0.32, 6.6, 0.8, 0.05, 16, eje='Y')
    cr = blanco()
    caja(cr, 0, yf + 0.2, H + 3.3, 0.18, 0.18, 1.6)
    caja(cr, 0, yf + 0.2, H + 4.1, 0.9, 0.18, 0.18)
    # Las torres: adobe abajo; arriba, el campanario de madera blanca y el chapitel.
    for s in (-1, 1):
        tx = s * 10.0
        caja(a, tx, yf + 2.2, 0, 4.6, 4.6, 13)
        caja(blanco(), tx, yf + 2.2, 13, 4.9, 4.9, 0.4)
        for sx in (-1, 1):
            for sy in (-1, 1):
                caja(blanco(), tx + sx * 1.9, yf + 2.2 + sy * 1.9, 13.4, 0.4, 0.4, 3.0)
        caja(mat('campana_sfn', 0x8a6a2a, 0.35), tx, yf + 2.2, 14.2, 1.0, 1.0, 1.0)
        caja(blanco(), tx, yf + 2.2, 16.4, 4.9, 4.9, 0.4)
        o = cil(blanco(), tx, yf + 2.2, 16.8, 3.1, 4.6, 4, r2=0.06)
        o.rotation_euler = (0, 0, math.pi / 4)
        caja(cr, tx, yf + 2.2, 21.4, 0.14, 0.14, 1.3)
        caja(cr, tx, yf + 2.2, 22.0, 0.7, 0.14, 0.14)
        ventana(tx, 6.5, 1.0, 1.8, y=yf - 0.1, marco=blanco(), cristal=cristal())
        ristra(tx + s * -2.6, yf - 0.4, 3.4, 1.3)
    # La plaza: el suelo de ladrillo, el quiosco, los álamos y los bancos.
    caja(mat_bloques('ladrillo_plaza_abq', 0xb87a58, 0x8a5a40, ancho=0.5, alto=0.25), 0, yf - 10, -0.05, 60, 20, 0.08)
    kx, ky = -15, yf - 9
    cil(blanco(), kx, ky, 0, 4.2, 0.6, 8)
    for k in range(8):
        a8 = k * math.tau / 8 + math.pi / 8
        cil(blanco(), kx + math.cos(a8) * 3.6, ky + math.sin(a8) * 3.6, 0.6, 0.12, 3.2, 8)
    o = cil(mat('tejado_quiosco_abq', 0x2a7a6a, 0.6), kx, ky, 3.8, 4.6, 2.4, 8, r2=0.2)
    o.rotation_euler = (0, 0, math.pi / 8)
    copa = mat('alamo_abq', 0x6a9a3a, 0.85)
    for (x, y) in ((-26, yf - 3), (-7, yf - 15), (8, yf - 16), (24, yf - 4), (27, yf - 14)):
        cil(viga(), x, y, 0, 0.35, 4.5, 8, r2=0.25)
        for (dx, dy, dz, r) in ((0, 0, 6.6, 2.8), (-1.4, 0.6, 5.6, 2.0), (1.5, -0.4, 5.8, 2.1)):
            esfera(copa, x + dx, y + dy, dz, r, 2, esc=(1.1, 1.1, 0.95))
    for x in (-8, 8):
        caja(viga(), x, yf - 6, 0.45, 2.4, 0.5, 0.08)
    # España: la bandera y la pancarta ALBURQUERQUE, con la R que perdió.
    cil(gris(), 18, yf - 7, 0, 0.12, 12, 8)
    caja(bandera_es('bandera_es_sfn', 9.2, 2.6), 19.9, yf - 7, 9.2, 3.8, 0.06, 2.6)
    for x in (9.5, 20.5):
        cil(viga(), x, yf - 12, 0, 0.12, 4.6, 8)
    caja(bandera_es('pancarta_es_sfn', 3.0, 1.6), 15, yf - 12, 3.0, 11, 0.06, 1.6)
    texto(negro(), 'ALBURQUERQUE', 15, yf - 12.04, 3.8, tam=0.95, prof=0.03)
    texto(blanco(), 'CON R', 15, yf - 12.04, 3.27, tam=0.36, prof=0.03)

# ================================================================ edificios
def kimo_theatre():
    """El teatro KiMo (art déco de los pueblos): el estuco, las bandas de
    terracota, los ventanales escalonados con las calaveras de buey, la
    bandera vertical con KIMO en neón y la marquesina."""
    Y = 8
    W, D, H = 22.0, 14.0, 15.0
    yf = Y - D / 2
    e = estuco()
    caja(e, 0, Y, 0, W, D, H)
    t = terracota()
    for z in (4.0, 12.6):
        caja(t, 0, yf - 0.08, z, W + 0.2, 0.16, 0.5)
    for k, w in enumerate((W, 14, 8)):
        caja(e, 0, Y, H + k * 1.0, w, D, 1.0)
        caja(t, 0, yf - 0.08 + (D - D) / 2, H + k * 1.0 + 0.75, w + 0.1, 0.16, 0.25)
    for x in (-6.5, 0, 6.5):
        for k, (w, h) in enumerate(((3.6, 7.2), (3.0, 6.6), (2.4, 6.0))):
            caja(t if k % 2 == 0 else e, x, yf - 0.04 - k * 0.04, 5.0, w, 0.1, h)
        caja(cristal(), x, yf - 0.2, 5.4, 1.8, 0.06, 5.2)
        cal = blanco()
        esfera(cal, x, yf - 0.3, 11.6, 0.42, 2, esc=(1, 0.6, 1.1))
        for sx in (-1, 1):
            rama(cal, (x + sx * 0.3, yf - 0.3, 11.9), (x + sx * 0.95, yf - 0.4, 12.4), 0.08, 0.03, 6)
    # La bandera vertical con KIMO.
    caja(rojo(), 0, yf - 1.0, 6.2, 1.2, 1.4, 10.5)
    for i, ch in enumerate('KIMO'):
        texto(neon_amar(), ch, 0, yf - 1.72, 15.2 - i * 2.2, tam=1.7, prof=0.06)
    # La marquesina.
    caja(t, 0, yf - 1.6, 3.4, 13, 3.2, 1.3)
    caja(negro(), 0, yf - 3.22, 3.55, 11.6, 0.06, 1.0)
    texto(neon_amar(), 'HOY: TRUMP', 0, yf - 3.27, 4.05, tam=0.62, prof=0.04)
    caja(cristal(), 0, yf - 0.06, 0.2, 9, 0.1, 2.8)

def casa_adobe():
    """Una casa de adobe de estilo pueblo: dos cuerpos de bordes blandos, las
    vigas que asoman, los canalones, el porche de madera, puertas y ventanas
    turquesa, ristras de chiles y el horno en la acera."""
    Y = 8
    W, D = 20.0, 12.0
    yf = Y - D / 2
    a = adobe()
    caja(a, 0, Y, 0, W, D, 5.4)
    caja(a, 3, Y + 2, 5.4, 11, 7, 3.6)
    vigas(-9.2, 9.2, yf, 4.6)
    vigas(-2.0, 8.0, yf + 2.5, 8.2)
    for x in (-8, 6):
        cil(viga(), x, yf - 0.6, 4.9, 0.12, 1.2, 6, eje='Y')
    # El porche (portal) de madera, delante de la puerta.
    v = viga()
    caja(v, -2, yf - 2.2, 3.1, 8.6, 2.6, 0.2)
    for x in (-6, -2, 2):
        cil(v, x, yf - 3.3, 0, 0.14, 3.1, 8)
        caja(v, x, yf - 3.3, 3.0, 0.9, 0.3, 0.12)
    tq = turquesa()
    puerta(-2, 0, 1.4, 2.4, y=yf, color=0x2fa8a0, marco=v)
    for x in (-6.5, 2.5, 6.5):
        caja(tq, x, yf - 0.05, 1.0, 1.6, 0.1, 1.6)
        caja(cristal(), x, yf - 0.1, 1.15, 1.2, 0.05, 1.3)
    ventana(3, 6.4, 1.2, 1.4, y=yf + 2.5, marco=tq, cristal=cristal())
    for x in (-5.4, -3.3, 0.8):
        ristra(x, yf - 3.0, 2.95, 1.25)
    caja(blanco(), 5, yf - 0.06, 3.3, 3.6, 0.06, 0.7)
    texto(rojo(), 'ABIERTO', 5, yf - 0.1, 3.65, tam=0.42, prof=0.02)
    # El horno de adobe en la acera.
    esfera(adobe_c(), 8.2, yf - 2.2, 0.5, 0.9, 2, esc=(1, 1, 0.9), mitad=True)
    caja(adobe_c(), 8.2, yf - 2.2, 0, 2.0, 2.0, 0.5)

def motel_66():
    """El motel de la Ruta 66: la hilera de habitaciones con sus puertas de
    colores, la oficina, el poste con el letrero de neón (MOTEL, la flecha y
    el escudo de la ROUTE 66) y un coche de los años cincuenta aparcado."""
    Y = 10
    yf = Y - 4
    e = adobe_c()
    caja(e, 2, Y, 0, 26, 8, 3.4)
    caja(terracota(), 2, Y, 3.4, 26.4, 8.4, 0.3)
    colores = (turquesa(), rojo(), amarillo())
    for k in range(7):
        x = -9 + k * 3.6
        caja(colores[k % 3], x, yf - 0.05, 0, 1.0, 0.1, 2.2)
        caja(cristal(), x + 1.3, yf - 0.05, 1.0, 1.0, 0.08, 1.0)
    caja(e, -12, Y - 2, 0, 5, 6, 4.2)
    caja(cristal(), -12, Y - 5.05, 0.4, 3.6, 0.1, 2.2)
    caja(blanco(), -12, Y - 5.1, 3.0, 4.2, 0.06, 0.7)
    texto(negro(), 'OFICINA', -12, Y - 5.15, 3.35, tam=0.4, prof=0.02)
    # El poste y el letrero.
    px, py = 13.5, Y - 6.5
    cil(gris(), px, py, 0, 0.22, 11.5, 10)
    caja(mat('fondo_neon_abq', 0x1e2a3a, 0.5), px, py, 7.0, 1.0, 0.5, 4.6)
    for i, ch in enumerate('MOTEL'):
        texto(neon_rojo(), ch, px, py - 0.28, 10.9 - i * 0.88, tam=0.78, prof=0.05)
    caja(mat('fondo_neon_abq', 0x1e2a3a, 0.5), px - 1.2, py, 5.0, 3.8, 0.4, 1.4)
    texto(neon_turq(), 'VACANCY', px - 1.2, py - 0.23, 5.7, tam=0.5, prof=0.04)
    # El escudo de la ROUTE 66.
    esc = blanco()
    caja(esc, px, py, 12.2, 2.2, 0.2, 1.8)
    caja(esc, px, py, 11.6, 1.4, 0.2, 0.7)
    texto(negro(), 'US', px, py - 0.12, 13.6, tam=0.36, prof=0.02)
    texto(negro(), '66', px, py - 0.12, 12.8, tam=0.85, prof=0.03)
    # El coche de los cincuenta, aparcado.
    cx, cy = 3, yf - 3.5
    c = turquesa()
    caja(c, cx, cy, 0.3, 5.2, 2.0, 0.65, giro=math.pi / 2)
    caja(blanco(), cx - 0.2, cy, 0.95, 2.6, 1.7, 0.5, giro=math.pi / 2)
    caja(cristal(), cx - 0.2, cy - 0.86, 1.0, 2.2, 0.04, 0.38)
    for sx in (-1.7, 1.7):
        for sy in (-0.95, 0.95):
            cil(negro(), cx + sx, cy + sy, 0.35, 0.35, 0.22, 14, eje='Y')
    caja(gris(), cx + 2.65, cy, 0.25, 0.12, 2.0, 0.25)

# ================================================================ cruzan la calle
def arco_66():
    """El arco de la ROUTE 66 sobre Central Avenue: dos pilonos de estuco con
    bandas turquesa y remate escalonado, el letrero de neón y, colgada debajo,
    la pancarta de España: ALBURQUERQUE, con la R."""
    e = estuco()
    for s in (-1, 1):
        caja(e, s * 9, 0, 0, 1.6, 1.6, 7.0)
        caja(turquesa(), s * 9, 0, 5.0, 1.7, 1.7, 0.4)
        caja(e, s * 9, 0, 7.0, 1.1, 1.1, 1.4)
        caja(terracota(), s * 9, 0, 8.4, 0.6, 0.6, 0.7)
    fondo = mat('fondo_arco_abq', 0x1e2a3a, 0.5)
    caja(terracota(), 0, 0, 7.0, 18.6, 0.6, 0.35)
    caja(fondo, 0, 0, 7.35, 16.4, 0.4, 1.5)
    texto(neon_turq(), 'ROUTE 66', 0, -0.22, 8.1, tam=1.1, prof=0.06)
    o = texto(neon_rojo(), 'CENTRAL AVE', 0, 0.22, 8.1, tam=0.95, prof=0.06); o.rotation_euler = (math.pi / 2, 0, math.pi)
    caja(bandera_es('pancarta_es_arco', 5.2, 1.4), 0, 0, 5.2, 10.5, 0.06, 1.4)
    texto(negro(), 'ALBURQUERQUE', 0, -0.05, 5.9, tam=0.85, prof=0.03)
    texto(blanco(), 'CON R', 0, -0.05, 5.43, tam=0.32, prof=0.03)
    for x in (-5.2, 5.2):
        rama(mat('cuerda_abq', 0xc8b08a, 0.9), (x, 0, 6.6), (x * 1.5, 0, 7.05), 0.025, 0.025, 4)

# ================================================================ la fiesta de los globos
def campo_globos():
    """El campo de la fiesta de los globos (momento estrella, al aire libre):
    la hierba con los caminos de tierra, a los lados globos inflándose y
    globos de pie con su cesta, la gente tras la cuerda, los puestos de
    comida, los carteles de FIESTA DE GLOBOS y muchos globos en el cielo.
    Cruza la calle: el origen en el centro y la calle a lo largo de y."""
    L = 420
    for k in range(5):
        caja(mat('campo_a_abq' if k % 2 else 'campo_b_abq', 0x8aac58 if k % 2 else 0x7ea250, 0.9),
             -4.4 + k * 2.2, 0, -0.2, 2.2, L, 0.2)
    lado = hierba()
    for s in (-1, 1):
        caja(lado, s * 18, 0, -0.21, 25, L, 0.2)
        caja(mat('tierra_abq', 0xc8a878, 0.9), s * 7.6, 0, -0.18, 1.6, L, 0.2)
    colores = [(0xc8202a, 0xf2c21a), (0x2a5aa8, 0xf6f1e6), (0x2fa8a0, 0xf28a1a), (0x8a3ab8, 0xf2c21a),
               (0xe84a7a, 0xf6f1e6), (0x3f8a3a, 0xf2e21a), (0xf28a1a, 0x2a5aa8)]
    # De pie en el suelo, con su cesta, y en el cielo (más pequeños, más lejos).
    for k in range(int(L / 30)):
        y = -L / 2 + 15 + k * 30
        for s in (-1, 1):
            c1, c2 = colores[(k * 2 + (s > 0)) % len(colores)]
            globo(s * (14 + (k % 3) * 3), y + s * 6, 0, 4.2 + (k % 2) * 0.6, c1, c2,
                  nombre=f'gores_campo_{(k * 2 + (s > 0)) % len(colores)}')
    for k in range(int(L / 22)):
        y = -L / 2 + 8 + k * 22
        s = 1 if k % 2 else -1
        c1, c2 = colores[(k + 3) % len(colores)]
        globo(s * (10 + (k % 4) * 6), y, 16 + (k % 5) * 6, 3.0, c1, c2, nombre=f'gores_campo_{(k + 3) % len(colores)}')
    # Globos inflándose, tumbados en el suelo.
    for k in range(int(L / 60)):
        y = -L / 2 + 40 + k * 60
        s = -1 if k % 2 else 1
        c1, c2 = colores[(k + 1) % len(colores)]
        g = mat_franjas(f'gores_tumbado_{k % 3}', c1, c2, 8, eje='Y', z0=y - 6, alto=12)
        esfera(g, s * 22, y, 2.6, 3.4, 2, esc=(1.0, 1.7, 0.8))
        caja(mimbre(), s * 22, y - 6.2, 0, 1.1, 1.1, 1.05)
    # La gente tras la cuerda y los puestos.
    camisas = [0xc8282c, 0x2a5aa8, 0xf4f0e8, 0xf0c020, 0x3f8a4a, 0xe86a2a]
    piel = [0xe8c0a0, 0xc89070, 0x8a5a3a]
    cu = mat('cuerda_abq', 0xc8b08a, 0.9)
    for s in (-1, 1):
        caja(cu, s * 8.9, 0, 0.8, 0.04, L, 0.04)
        for k in range(int(L / 3.2)):
            y = -L / 2 + 1.5 + k * 3.2
            if (k + (s > 0)) % 4 == 0:
                continue
            x = s * (9.7 + (k % 3) * 0.5)
            cil(mat(f'gente_abq_{k % 6}', camisas[k % 6], 0.7), x, y, 0, 0.26, 1.25, 8)
            esfera(mat(f'piel_abq_{k % 3}', piel[k % 3], 0.7), x, y, 1.45, 0.2, 1)
    for k in range(int(L / 70)):
        y = -L / 2 + 30 + k * 70
        for s in (-1, 1):
            x = s * 26
            caja(blanco(), x, y, 0, 4, 3, 2.4)
            caja(rojo() if k % 2 else turquesa(), x, y - 0.4, 2.4, 4.4, 3.8, 0.25)
            caja(blanco(), x, y - 1.55, 2.0, 3.6, 0.06, 0.4)
            texto(rojo(), 'CHILE' if (k + (s > 0)) % 2 else 'BURRITOS', x, y - 1.6, 2.2, tam=0.32, prof=0.02)
    # La entrada y la salida: el cartel de FIESTA DE GLOBOS.
    for y in (-L / 2 + 1, L / 2 - 1):
        for s in (-1, 1):
            caja(estuco(), s * 9.5, y, 0, 1.2, 1.2, 6.6)
            globo(s * 9.5, y, 6.6, 0.9, 0xc8202a, 0xf2c21a, cesta=False, nombre='gores_arco')
        caja(turquesa(), 0, y, 5.0, 18, 0.5, 1.4)
        texto(blanco(), 'FIESTA DE GLOBOS', 0, y - 0.27, 5.7, tam=0.95, prof=0.04)

# ================================================================ obstáculos
def globo_aire():
    """El globo que aterriza en la calle (no se pasa cuando está en el suelo):
    la cesta abajo (el origen, en su fondo) y la envoltura a gajos rojos y
    amarillos... de Nuevo México."""
    globo(0, 0, 0, 2.2, 0xe84a1a, 0xf2c21a, nombre='gores_obst_a')

def globo_espana():
    """El globo de la Armada Española (no se pasa cuando está en el suelo):
    rojo y amarillo, con la pancarta ESPAÑA colgando de la cesta."""
    globo(0, 0, 0, 2.2, 0xc8202a, 0xf2c21a, n=4, nombre='gores_obst_es')
    caja(blanco(), 0, -0.58, 0.25, 1.0, 0.03, 0.5)
    texto(rojo(), 'ESPAÑA', 0, -0.6, 0.5, tam=0.2, prof=0.01)

def platillo():
    """El platillo volante de Roswell: el disco plateado con el aro de luces,
    la cúpula de cristal verde y la panza con la boca del rayo (el origen, en
    el centro de la panza)."""
    pl = mat('plata_abq', 0xc8ccd4, 0.2)
    os_ = mat('plata_oscura_abq', 0x6a707a, 0.3)
    cil(os_, 0, 0, 0, 0.9, 0.35, 24, r2=1.6)
    cil(pl, 0, 0, 0.35, 1.6, 0.35, 32, r2=2.6)
    cil(pl, 0, 0, 0.7, 2.6, 0.7, 32, r2=1.2)
    esfera(mat('cupula_abq', 0x6ae8a0, 0.1), 0, 0, 1.35, 1.0, 2, esc=(1, 1, 0.85), mitad=True)
    luces = luz('luz_platillo_abq', 0x9affb0, 1.4)
    for k in range(12):
        a = k * math.tau / 12
        esfera(luces, math.cos(a) * 2.45, math.sin(a) * 2.45, 0.72, 0.13, 1)
    cil(luz('boca_platillo_abq', 0xb8ffc8, 1.2), 0, 0, -0.02, 0.7, 0.04, 20)

def horno_adobe():
    """El horno de adobe (saltar): la cúpula de colmena sobre su base, con la
    boca y el agujero del humo."""
    a = adobe_c()
    caja(a, 0, 0, 0, 1.3, 1.3, 0.3)
    esfera(a, 0, 0, 0.3, 0.6, 2, esc=(1, 1, 1.05), mitad=True)
    caja(negro(), 0, -0.55, 0.3, 0.3, 0.08, 0.2)
    cil(negro(), 0, -0.55, 0.5, 0.15, 0.08, 10, eje='Y')

def ristra_chiles():
    """Las ristras de chiles colgando de una viga sobre el carril (agacharse)."""
    v = viga()
    for x in (-1.2, 1.2):
        cil(v, x, 0, 0, 0.09, 2.7, 8)
    cil(v, 0, 0, 2.6, 0.11, 2.6, 8, eje='X')
    for k, x in enumerate((-0.85, -0.45, 0.0, 0.45, 0.85)):
        ristra(x, 0, 2.55, 0.95 + 0.1 * (k % 2))

def cartel_alburquerque():
    """La pancarta de España (agacharse): ALBURQUERQUE, con la R que perdió la
    ciudad, sobre la bandera."""
    for x in (-1.25, 1.25):
        cil(gris(), x, 0, 0, 0.06, 2.75, 8)
    caja(bandera_es('pancarta_es_obst', 1.5, 1.2), 0, 0, 1.5, 2.4, 0.05, 1.2)
    texto(negro(), 'ALBURQUERQUE', 0, -0.035, 2.1, tam=0.3, prof=0.02)
    texto(blanco(), 'CON R', 0, -0.035, 1.7, tam=0.2, prof=0.02)

def lowrider():
    """El lowrider (no se pasa): el coche largo y bajo de pintura caramelo,
    con las llantas de radios y el techo blanco; el morro mira al jugador y
    está en el origen (el resto, hacia atrás, como los demás coches)."""
    Y = 2.85
    c = mat('caramelo_abq', 0x8a1a5a, 0.15)
    cromo = mat('cromo_abq', 0xe0e4ea, 0.1)
    caja(c, 0, Y, 0.18, 2.0, 5.6, 0.55)
    caja(c, 0, Y + 0.3, 0.73, 1.75, 2.4, 0.45)
    caja(blanco(), 0, Y + 0.3, 1.18, 1.65, 2.2, 0.06)
    vid = cristal()
    caja(vid, 0, Y - 0.95, 0.75, 1.6, 0.05, 0.42, inclina=-0.6)
    for sx in (-1, 1):
        caja(vid, sx * 0.88, Y + 0.3, 0.78, 0.02, 2.0, 0.34)
        caja(cromo, sx * 1.005, Y, 0.42, 0.02, 5.2, 0.06)
        for sy in (-1.75, 1.75):
            cil(negro(), sx * 0.85, Y + sy, 0.3, 0.3, 0.22, 16, eje='X')
            cil(cromo, sx * 0.97, Y + sy, 0.3, 0.22, 0.02, 12, eje='X')
    caja(cromo, 0, Y - 2.82, 0.2, 2.0, 0.08, 0.3)
    for sx in (-1, 1):
        caja(mat('faro_abq', 0xf4ecc0, 0.3), sx * 0.65, Y - 2.86, 0.45, 0.4, 0.03, 0.16)

def cesta_globo():
    """La cesta de un globo volcada en la calle, con la tela desinflada detrás
    (saltar)."""
    caja(mimbre(), 0, 0.2, 0, 1.0, 1.1, 0.85)
    caja(viga(), 0, -0.35, 0, 1.06, 0.08, 0.9)
    g = mat_franjas('gores_cesta', 0x2fa8a0, 0xf28a1a, 6, eje='X', z0=-1.0, alto=2.0)
    esfera(g, 0, 1.4, 0, 1.0, 2, esc=(1.0, 1.3, 0.45), mitad=True)

PIEZAS = {
    'san_felipe_neri':     (san_felipe_neri,     'albuquerque', dict(lado=2048, bisel=0.0)),
    'kimo_theatre':        (kimo_theatre,        'albuquerque', dict(lado=1024, bisel=0.0)),
    'casa_adobe':          (casa_adobe,          'albuquerque', dict(lado=1024, bisel=0.0)),
    'motel_66':            (motel_66,            'albuquerque', dict(lado=1024, bisel=0.0)),
    'arco_66':             (arco_66,             'albuquerque', dict(lado=1024, bisel=0.0, suelo=False)),
    'campo_globos':        (campo_globos,        'albuquerque', dict(lado=2048, bisel=0.0, suelo=False)),
    'globo_aire':          (globo_aire,          'obstaculos',  dict(lado=256, bisel=0.0, suelo=False)),
    'globo_espana':        (globo_espana,        'obstaculos',  dict(lado=256, bisel=0.0, suelo=False)),
    'platillo':            (platillo,            'obstaculos',  dict(lado=256, bisel=0.0, suelo=False)),
    'horno_adobe':         (horno_adobe,         'obstaculos',  dict(lado=256, bisel=0.0)),
    'ristra_chiles':       (ristra_chiles,       'obstaculos',  dict(lado=256, bisel=0.0, suelo=False)),
    'cartel_alburquerque': (cartel_alburquerque, 'obstaculos',  dict(lado=256, bisel=0.0, suelo=False)),
    'lowrider':            (lowrider,            'obstaculos',  dict(lado=256, bisel=0.0)),
    'cesta_globo':         (cesta_globo,         'obstaculos',  dict(lado=256, bisel=0.0)),
}

correr(PIEZAS)
