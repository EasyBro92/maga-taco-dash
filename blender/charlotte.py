# Nivel 25: Charlotte, Carolina del Norte (14/11/2026).
#
#   blender -b -P blender/charlotte.py -- [pieza ...] [--rapido]
#
# Historia: «El circuito de NASCAR».
#   Por Tryon Street, en la «ciudad de la reina» (el arco de QUEEN CITY, la
#   torre de la corona, la torre de las luces, la iglesia presbiteriana y el
#   taller de carreras) entre coches de carreras que van delante (ir a su
#   rebufo, pegado detrás, y salirse antes de que frenen); en el óvalo, de
#   noche y con focos, el accidente en cadena («the Big One»); y se llega al
#   salón de la fama, con su cinta de acero.
# Obstáculos (carpeta obstaculos): el coche de carreras (tres colores: el 45
# rojo, el 47 azul y el 1 amarillo), la pila de ruedas, la pancarta de la
# carrera, el carro de boxes y el camión del equipo.

import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import *

def blanco():   return mat('blanco_clt', 0xf4f2ec, 0.5)
def negro():    return mat('negro_clt', 0x1b1c20, 0.4)
def goma():     return mat('goma_clt', 0x202024, 0.85)
def gris():     return mat('gris_clt', 0x8a9098, 0.5)
def rojo():     return mat('rojo_clt', 0xd02a2a, 0.4)
def azul():     return mat('azul_clt', 0x2a5ad0, 0.4)
def amarillo(): return mat('amarillo_clt', 0xf0c020, 0.4)
def oro():      return mat('oro_clt', 0xe8b840, 0.25)
def cristal():  return mat('cristal_clt', 0x1e2a36, 0.2)
def acero():    return mat('acero_clt', 0xc8ccd2, 0.15)
def hormigon(): return mat('hormigon_clt', 0xb4b4ae, 0.8)

COLORES = {'rojo': (rojo, blanco, '45'), 'azul': (azul, blanco, '47'), 'amarillo': (amarillo, negro, '1')}

def coche_carreras(color, x=0.0, y=0.0, z=0.0, s=1):
    """Un coche de carreras de serie: con s=1 el morro mira a +y (de espaldas
    al jugador); con s=-1, al jugador. El alerón detrás, el número en las
    puertas, en el techo y en la trasera."""
    c, c2, num = COLORES[color][0](), COLORES[color][1](), COLORES[color][2]
    caja(c, x, y, z + 0.2, 1.96, 5.0, 0.55)
    caja(c, x, y - s * 0.2, z + 0.75, 1.6, 2.0, 0.45)
    vid = cristal()
    caja(vid, x, y + s * 1.05, z + 0.99 - 0.325, 1.5, 0.05, 0.65, inclina=s * 0.87)
    caja(vid, x, y - s * 1.475, z + 0.99 - 0.35, 1.5, 0.05, 0.7, inclina=-s * 0.92)
    for sx in (-1, 1):
        caja(vid, x + sx * 0.81, y - s * 0.2, z + 0.8, 0.02, 1.7, 0.35)
        caja(c2, x + sx * 0.985, y, z + 0.32, 0.02, 4.4, 0.14)
        cil(blanco(), x + sx * 0.99, y - s * 0.1, z + 0.52, 0.3, 0.02, 20, eje='X')
        o = texto(negro(), num, 0, 0, 0, tam=0.36, prof=0.02)
        o.rotation_euler = (math.pi / 2, 0, sx * math.pi / 2)
        o.location = (x + sx * 1.005, y - s * 0.1, z + 0.52)
        for sy in (-1.55, 1.55):
            cil(goma(), x + sx * 0.88, y + sy, z + 0.35, 0.35, 0.28, 16, eje='X')
            cil(oro(), x + sx * 1.03, y + sy, z + 0.35, 0.19, 0.02, 12, eje='X')
    caja(negro(), x, y - s * 2.45, z + 0.75, 1.9, 0.06, 0.28)
    for sx in (-1, 1):
        caja(negro(), x + sx * 0.9, y - s * 2.45, z + 0.6, 0.05, 0.25, 0.4)
    caja(negro(), x, y + s * 2.45, z + 0.08, 1.98, 0.2, 0.12)
    caja(negro(), x, y + s * 2.51, z + 0.3, 1.1, 0.04, 0.22)
    for sx in (-1, 1):
        caja(mat('faro_clt', 0xf4ecc0, 0.3), x + sx * 0.62, y + s * 2.51, z + 0.5, 0.42, 0.03, 0.15)
        caja(mat('piloto_clt', 0x6a1414, 0.4), x + sx * 0.62, y - s * 2.51, z + 0.52, 0.45, 0.03, 0.14)
    caja(blanco(), x, y - s * 0.2, z + 1.2, 1.1, 1.2, 0.012)
    o = texto(negro(), num, 0, 0, 0, tam=0.7, prof=0.02)
    o.rotation_euler = (0, 0, 0 if s > 0 else math.pi)
    o.location = (x, y - s * 0.2, z + 1.215)
    if s > 0:
        texto(c2, num, x, y - 2.51, z + 0.47, tam=0.34, prof=0.02)

def checkers(x0, y, z, n, lado, filas=2):
    """Una tira de cuadros de carreras en una fachada que mira a -y."""
    for f in range(filas):
        for k in range(n):
            caja(negro() if (k + f) % 2 else blanco(), x0 + (k + 0.5) * lado, y, z + f * lado, lado, 0.06, lado)

# ================================================================ edificios
def salon_fama():
    """El salón de la fama de las carreras (la meta): la caja de cristal, la
    cinta de acero que sube desde el suelo y pasa por encima, la pantalla con
    el 45 y, delante, los tres coches campeones en su podio."""
    Y = 20
    W, D, H = 52.0, 28.0, 18.0
    yf = Y - D / 2
    vid = mat_ventanas('cristal_hof', 0x3a6a8a, 0x2a3a48, paso_x=2.0, paso_z=3.0, hueco_x=1.8, hueco_z=2.7, variacion=1.2)
    caja(vid, 0, Y, 0, W, D, H)
    caja(mat('techo_hof', 0x5a6068, 0.5), 0, Y, H, W + 0.4, D + 0.4, 0.6)
    caja(luz('pantalla_hof', 0x2a5ac8, 0.9), 14, yf - 0.1, 5.5, 16, 0.12, 9)
    texto(blanco(), '#45', 14, yf - 0.2, 10.0, tam=4.0, prof=0.06)
    caja(mat('fondo_letras_hof', 0x1e2a3a, 0.5), 14, yf - 0.08, 15.1, 15, 0.1, 1.9)
    texto(blanco(), 'HALL OF FAME', 14, yf - 0.16, 16.0, tam=1.3, prof=0.06)
    a = acero()
    pts = [(-27, 0.4), (-20, 3.5), (-12, 8), (-4, 12.5), (4, 16), (11, 18.4), (17, 19.4), (24, 19.6), (27.5, 19.3)]
    for (x0, z0), (x1, z1) in zip(pts, pts[1:]):
        lg = math.hypot(x1 - x0, z1 - z0)
        ang = math.atan2(z1 - z0, x1 - x0)
        o = caja(a, (x0 + x1) / 2, yf - 1.0, (z0 + z1) / 2 - 1.6, lg + 0.6, 0.6, 3.2)
        o.rotation_euler = (0, -ang, 0)
    caja(cristal(), -6, yf - 0.06, 0, 14, 0.1, 4.2)
    # El podio de los campeones con los tres coches mirando a la calle.
    caja(mat('podio_hof', 0x2a2a30, 0.5), -12, yf - 7, 0, 18, 7, 0.6)
    checkers(-21, yf - 10.53, 0.0, 36, 0.5, filas=1)
    for (x, col) in ((-18, 'azul'), (-12, 'rojo'), (-6, 'amarillo')):
        coche_carreras(col, x, yf - 7, 0.6, s=-1)
    for x in (4, 28):
        cil(gris(), x, yf - 9, 0, 0.12, 11, 8)
        checkers(x + 0.1, yf - 9, 8.6, 6, 0.4, filas=4)

def torre_corona():
    """La torre de la corona: el rascacielos de granito rosado con sus
    retranqueos, el tambor, la cúpula y la corona de varillas con las puntas
    encendidas."""
    Y = 14
    g = mat_ventanas('granito_corona', 0x3a4a5a, 0xb89a88, paso_x=1.3, paso_z=3.5, hueco_x=0.7, hueco_z=2.4)
    caja(g, 0, Y, 0, 24, 24, 58)
    caja(g, 0, Y, 58, 20, 20, 6)
    liso = mat('granito_liso', 0xb89a88, 0.6)
    cil(liso, 0, Y, 64, 8.5, 5, 24)
    cupula(liso, 0, Y, 69, 7.5, 5, 24, 6)
    varilla = mat('varilla_corona', 0xd8b070, 0.3)
    punta = luz('punta_corona', 0xfff0c0, 1.2)
    for k in range(24):
        a = k * math.tau / 24
        h = 12 + 3 * (k % 2)
        cil(varilla, math.cos(a) * 8.6, Y + math.sin(a) * 8.6, 64, 0.22, h, 6)
        esfera(punta, math.cos(a) * 8.6, Y + math.sin(a) * 8.6, 64 + h, 0.28, 1)
    cil(oro(), 0, Y, 74, 0.3, 8, 8, r2=0.05)
    caja(cristal(), 0, Y - 12.05, 0, 10, 0.1, 7)
    caja(liso, 0, Y - 12.6, 7, 12, 1.2, 0.5)

def torre_led():
    """La torre de las luces: el rascacielos de cristal azul y, arriba, la
    jaula de barras encendidas (fijas, sin cambiar de color)."""
    Y = 13
    vid = mat_ventanas('cristal_led', 0x4a7a9a, 0x2a3a48, paso_x=1.5, paso_z=3.4, hueco_x=1.35, hueco_z=3.0, variacion=1.2)
    caja(vid, 0, Y, 0, 22, 20, 60)
    caja(vid, 0, Y + 2, 60, 18, 16, 8)
    led = luz('led_torre', 0x6ac8ff, 1.3)
    x0, x1, y0, y1 = -9, 9, Y - 6, Y + 10
    for k in range(5):
        for (xa, ya) in ((x0 + k * 4.5, y0), (x0 + k * 4.5, y1), (x0, y0 + k * 4), (x1, y0 + k * 4)):
            caja(led, xa, ya, 68, 0.35, 0.35, 12)
    for z in (71.8, 75.8, 79.8):
        caja(led, 0, y0, z, 18.35, 0.35, 0.35)
        caja(led, 0, y1, z, 18.35, 0.35, 0.35)
        caja(led, x0, (y0 + y1) / 2, z, 0.35, 16.35, 0.35)
        caja(led, x1, (y0 + y1) / 2, z, 0.35, 16.35, 0.35)
    caja(cristal(), 0, Y - 10.05, 0, 12, 0.1, 6)

def iglesia_presbiteriana():
    """La iglesia presbiteriana de piedra: la nave con su tejado de pizarra,
    la torre con el reloj, el rosetón y la aguja."""
    Y = 12
    pi = mat_bloques('piedra_igl', 0xb8a890, 0x9a8a72, ancho=0.9, alto=0.45)
    piz = mat('pizarra_igl', 0x4a4e58, 0.6)
    caja(pi, 0, Y + 2, 0, 16, 22, 11)
    tejado(piz, 0, Y - 9, Y + 13, 11, 16, 6)
    hastial(pi, 0, Y - 9, Y + 13, 11, 16, 6)
    vidriera = mat('vidriera_igl', 0x6a4a9a, 0.3)
    for s in (-1, 1):
        ventana(s * 5.2, 3.0, 1.6, 5.0, y=Y - 9, marco=mat('marco_igl', 0xd8ccb4, 0.6), cristal=vidriera, remate='fronton')
    ty = Y - 9
    caja(pi, 0, ty, 0, 5.5, 5.5, 22)
    for sx in (-1, 1):
        for sy in (-1, 1):
            cil(pi, sx * 2.75, ty + sy * 2.75, 22, 0.4, 3.2, 6, r2=0.05)
    cil(piz, 0, ty, 22, 2.6, 16, 8, r2=0.05)
    esfera(oro(), 0, ty, 38.2, 0.25, 1)
    caja(mat('puerta_igl', 0x4a2a1a, 0.6), 0, ty - 2.8, 0, 2.2, 0.1, 3.4)
    cil(mat('puerta_igl', 0x4a2a1a, 0.6), 0, ty - 2.8, 3.4, 1.1, 0.1, 16, eje='Y')
    cil(mat('marco_igl', 0xd8ccb4, 0.6), 0, ty - 2.79, 12.5, 1.6, 0.08, 20, eje='Y')
    cil(vidriera, 0, ty - 2.84, 12.5, 1.35, 0.08, 20, eje='Y')
    cil(blanco(), 0, ty - 2.82, 18.0, 1.15, 0.08, 24, eje='Y')
    rama(negro(), (0, ty - 2.9, 18.0), (0, ty - 2.9, 18.8), 0.06, 0.06, 4)
    rama(negro(), (0, ty - 2.9, 18.0), (0.55, ty - 2.9, 18.0), 0.06, 0.06, 4)

def garaje_carreras():
    """El taller de carreras: la nave de chapa con la franja de cuadros, dos
    persianas cerradas y una abierta, el coche del 45 en la puerta y ruedas."""
    Y = 8
    caja(mat('chapa_garaje', 0xd8dadc, 0.5), 0, Y, 0, 22, 14, 7.5)
    yf = Y - 7
    checkers(-11, yf - 0.05, 6.2, 44, 0.5, filas=2)
    per = mat_bloques('persiana_garaje', 0xb8bcc2, 0x9a9ea4, ancho=5.0, alto=0.3)
    for x in (-7, 7):
        caja(per, x, yf - 0.05, 0, 5, 0.1, 4.6)
    caja(mat('interior_garaje', 0x1a1c20, 0.8), 0, yf - 0.05, 0, 5, 0.1, 4.6)
    texto(rojo(), 'RACE SHOP', 0, yf - 0.1, 5.35, tam=1.0, prof=0.06)
    coche_carreras('rojo', 0, yf - 3.2, 0, s=-1)
    for (x, n) in ((-3.6, 4), (3.8, 3)):
        for k in range(n):
            cil(goma(), x, yf - 1.2, k * 0.3, 0.42, 0.28, 18)

# ================================================================ cruzan la calle
def arco_carrera():
    """El arco de QUEEN CITY: los postes a cuadros, el letrero y la corona."""
    for s in (-1, 1):
        for k in range(10):
            caja(negro() if k % 2 else blanco(), s * 9, 0, k * 0.94, 0.6, 0.6, 0.94)
    caja(blanco(), 0, 0, 6.2, 18.6, 0.5, 0.4)
    caja(blanco(), 0, 0, 8.6, 18.6, 0.5, 0.4)
    caja(mat('azul_arco_clt', 0x1f3a7a, 0.6), 0, 0, 6.6, 17, 0.3, 2.0)
    texto(oro(), 'QUEEN CITY', 0, -0.2, 7.55, tam=1.3, prof=0.07)
    o = texto(oro(), 'QUEEN CITY', 0, 0.2, 7.55, tam=1.3, prof=0.07); o.rotation_euler = (math.pi / 2, 0, math.pi)
    cil(oro(), 0, 0, 9.0, 1.3, 0.6, 18)
    for k in range(6):
        a = k * math.tau / 6
        cil(oro(), math.cos(a) * 1.1, math.sin(a) * 1.1, 9.6, 0.2, 1.2, 6, r2=0.03)
        esfera(rojo(), math.cos(a) * 1.25, math.sin(a) * 1.25, 9.3, 0.14, 1)

def speedway():
    """El óvalo (momento estrella), de noche y con focos: el asfalto con sus
    líneas, a la izquierda el muro blanco con la valla y la tribuna llena; a la
    derecha la explanada, el muro y el carril de boxes con los puestos de los
    equipos, los camiones y la torre con las posiciones; la pasarela de salida
    y la de meta. Cruza la calle: el origen en el centro y la calle a lo largo
    de y."""
    L = 420
    caja(mat('asfalto_spw', 0x3a3c40, 0.85), 0, 0, -0.2, 22, L, 0.2)
    for x in (-7.6, 7.6):
        caja(blanco(), x, 0, 0, 0.18, L, 0.012)
    caja(amarillo(), 8.6, 0, 0, 0.2, L, 0.012)
    caja(hormigon(), 18, 0, -0.21, 14, L, 0.2)
    caja(mat('cesped_spw', 0x3a7a3a, 0.9), 34, 0, -0.22, 20, L, 0.2)
    # A la izquierda: el muro, la valla y la tribuna.
    caja(blanco(), -9.4, 0, 0, 0.5, L, 1.25)
    caja(azul(), -9.13, 0, 0.1, 0.02, L, 0.35)
    for z in (2.0, 3.4, 4.8):
        cil(gris(), -9.6, 0, z, 0.035, L, 4, eje='Y')
    for k in range(int(L / 6)):
        cil(gris(), -9.6, -L / 2 + 3 + k * 6, 1.25, 0.07, 4.4, 6)
    gente = mat_bloques('gente_spw', 0x8a5a7a, 0x2a2a30, ancho=0.5, alto=0.7, variacion=1.7)
    for g in range(6):
        caja(gente, -12 - g * 3.4, 0, 0, 3.4, L, 1.4 + g * 2.6)
    camisas = [0xc8282c, 0x2a5aa8, 0xf4f0e8, 0xf0c020, 0x3f8a4a]
    for k in range(int(L / 4.2)):
        y = -L / 2 + 2 + k * 4.2
        cm = mat(f'camisa_spw{k % 5}', camisas[k % 5], 0.8)
        cil(cm, -11.4, y, 1.4, 0.45, 0.9, 6)
        esfera(mat('cara_spw', 0xe8b89a, 0.7), -11.4, y, 2.6, 0.32, 1)
    caja(hormigon(), -32.5, 0, 0, 1.0, L, 18)
    caja(mat('tejado_spw', 0x2a2e36, 0.6), -23, 0, 18, 22, L, 0.5)
    foco = luz('foco_spw', 0xfff8e8, 1.6)
    for k in range(int(L / 35)):
        y = -L / 2 + 17 + k * 35
        cil(gris(), -31, y, 18.5, 0.3, 10, 8)
        caja(gris(), -31, y, 28.5, 1.0, 5.4, 3.0)
        for i in range(3):
            for j in range(2):
                caja(foco, -30.48, y - 1.8 + i * 1.8, 28.9 + j * 1.3, 0.04, 1.4, 1.0)
    # A la derecha: el muro de boxes, los puestos, los camiones y la torre.
    caja(hormigon(), 11.2, 0, 0, 0.5, L, 1.0)
    caja(mat('asfalto_spw', 0x3a3c40, 0.85), 17, 0, -0.205, 8, L, 0.2)
    colores = [rojo, azul, amarillo]
    for k in range(int(L / 12)):
        y = -L / 2 + 6 + k * 12
        cm = colores[k % 3]()
        caja(cm, 22, y, 0, 1.2, 0.7, 0.95)
        for sx in (-1, 1):
            for sy in (-1, 1):
                cil(gris(), 22.6 + sx * 1.4, y + sy * 1.6, 0, 0.05, 2.8, 4)
        caja(cm, 22.6, y, 2.8, 3.2, 3.6, 0.12)
        cil(mat('mono_spw', 0xf4f0e8, 0.7), 20.6, y + 1.2, 0, 0.3, 1.25, 6)
        esfera(cm, 20.6, y + 1.2, 1.5, 0.27, 1)
    for k in range(int(L / 40)):
        y = -L / 2 + 20 + k * 40
        cm = colores[k % 3]()
        caja(cm, 30, y, 0.6, 2.6, 13, 3.4)
        caja(blanco(), 30, y - 7.6, 0.5, 2.4, 2.2, 3.0)
    torre = mat('torre_spw', 0x1e2024, 0.5)
    dig = luz('digitos_spw', 0xffd040, 1.5)
    for j in range(3):
        y = -L / 2 + 70 + j * 140
        caja(torre, 27, y, 0, 3.2, 3.2, 26)
        for i, n in enumerate(('45', '47', '1', '24', '8')):
            texto(dig, n, 27, y - 1.62, 23.5 - i * 2.4, tam=1.6, prof=0.05)
        texto(blanco(), 'POS', 27, y - 1.62, 25.6, tam=0.6, prof=0.04)
    # La pasarela de salida y la de meta (con su banda a cuadros en el suelo).
    for (y, txt) in ((-L / 2 + 12, 'START'), (L / 2 - 12, 'FINISH')):
        for s in (-1, 1):
            caja(gris(), s * 10.4, y, 0, 0.8, 0.8, 8.8)
        caja(mat('pasarela_spw', 0x2a2e36, 0.5), 0, y, 8.0, 21.6, 2.0, 1.8)
        checkers(-10.8, y - 1.04, 8.0, 54, 0.4, filas=1)
        texto(blanco(), txt, 0, y - 1.06, 9.2, tam=0.9, prof=0.05)
        for k in range(36):
            for f in range(2):
                caja(negro() if (k + f) % 2 else blanco(), -9 + (k + 0.5) * 0.5, y + (f - 0.5) * 0.5, 0, 0.5, 0.5, 0.014)

# ================================================================ obstáculos
def stock_car():
    """El coche de carreras rojo del 45 (de espaldas: va delante)."""
    coche_carreras('rojo')

def stock_car_azul():
    """El coche de carreras azul del 47."""
    coche_carreras('azul')

def stock_car_amarillo():
    """El coche de carreras amarillo del 1."""
    coche_carreras('amarillo')

def pila_ruedas():
    """La pila de ruedas (saltar)."""
    for (x, z) in ((-0.45, 0), (0.45, 0), (-0.45, 0.28), (0.45, 0.28), (0, 0.56)):
        cil(goma(), x, 0, z, 0.42, 0.28, 18)
        cil(amarillo(), x, 0, z + 0.11, 0.425, 0.05, 18)
        cil(mat('hueco_rueda', 0x0e0e10, 0.9), x, 0, z + 0.28, 0.2, 0.006, 12)

def cartel_carrera():
    """La pancarta de la carrera, con los cuadros arriba y abajo (agacharse)."""
    for x in (-1.25, 1.25):
        cil(gris(), x, 0, 0, 0.07, 2.75, 8)
    caja(blanco(), 0, 0, 1.55, 2.4, 0.06, 1.05)
    for f, z in ((0, 1.55), (1, 2.46)):
        for k in range(16):
            caja(negro() if (k + f) % 2 else blanco(), -1.125 + k * 0.15, -0.04, z, 0.15, 0.01, 0.14)
    texto(rojo(), 'RACE DAY', 0, -0.045, 2.08, tam=0.42, prof=0.02)

def carro_boxes():
    """El carro de boxes (saltar): la caja de herramientas roja con sus
    cajones, una rueda encima y el bidón de gasolina."""
    caja(rojo(), 0, 0, 0.12, 1.2, 0.7, 0.62)
    for z in (0.3, 0.48, 0.64):
        caja(gris(), 0, -0.36, z, 1.0, 0.02, 0.03)
    for sx in (-0.5, 0.5):
        for sy in (-0.28, 0.28):
            cil(negro(), sx, sy, 0.06, 0.06, 0.06, 8, eje='X')
    cil(goma(), -0.15, 0, 0.74, 0.36, 0.24, 16)
    cil(amarillo(), 0.45, 0, 0.74, 0.14, 0.32, 10)
    cil(negro(), 0.45, 0, 1.06, 0.04, 0.12, 6)

def camion_equipo():
    """El camión del equipo del 45 (no se pasa): la cabina blanca con la
    parrilla cromada y el remolque rojo con las franjas."""
    caja(rojo(), 0, 1.1, 0.8, 2.5, 6.0, 2.9)
    caja(blanco(), 0, -2.9, 0.5, 2.4, 2.0, 2.4)
    caja(blanco(), 0, -2.6, 2.9, 2.3, 1.4, 0.6)
    caja(cristal(), 0, -3.91, 1.75, 2.1, 0.04, 0.9)
    caja(acero(), 0, -3.92, 0.55, 1.6, 0.06, 1.1)
    caja(gris(), 0, -3.95, 0.3, 2.4, 0.12, 0.25)
    for sx in (-1, 1):
        esfera(mat('faro_clt', 0xf4ecc0, 0.3), sx * 0.95, -3.94, 0.75, 0.13, 1)
        caja(blanco(), sx * 1.255, 1.1, 2.2, 0.02, 6.0, 0.3)
        caja(azul(), sx * 1.255, 1.1, 1.8, 0.02, 6.0, 0.3)
        for y in (-3.0, 2.6, 3.6):
            cil(goma(), sx * 1.0, y, 0.5, 0.5, 0.4, 14, eje='X')
    caja(blanco(), 0, -1.92, 3.0, 1.6, 0.04, 0.6)
    texto(rojo(), '45', 0, -1.95, 3.3, tam=0.5, prof=0.02)

PIEZAS = {
    'salon_fama':            (salon_fama,            'charlotte',  dict(lado=2048, bisel=0.0)),
    'torre_corona':          (torre_corona,          'charlotte',  dict(lado=2048, bisel=0.0)),
    'torre_led':             (torre_led,             'charlotte',  dict(lado=2048, bisel=0.0)),
    'iglesia_presbiteriana': (iglesia_presbiteriana, 'charlotte',  dict(lado=1024, bisel=0.0)),
    'garaje_carreras':       (garaje_carreras,       'charlotte',  dict(lado=1024, bisel=0.0)),
    'arco_carrera':          (arco_carrera,          'charlotte',  dict(lado=1024, bisel=0.0, suelo=False)),
    'speedway':              (speedway,              'charlotte',  dict(lado=2048, bisel=0.0, suelo=False)),
    'stock_car':             (stock_car,             'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
    'stock_car_azul':        (stock_car_azul,        'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
    'stock_car_amarillo':    (stock_car_amarillo,    'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
    'pila_ruedas':           (pila_ruedas,           'obstaculos', dict(lado=256, bisel=0.0)),
    'cartel_carrera':        (cartel_carrera,        'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
    'carro_boxes':           (carro_boxes,           'obstaculos', dict(lado=256, bisel=0.0)),
    'camion_equipo':         (camion_equipo,         'obstaculos', dict(lado=512, bisel=0.0)),
}

correr(PIEZAS)
