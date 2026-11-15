# Nivel 40: Richmond, Virginia (15/11/2026).
#
#   blender -b -P blender/richmond.py -- [pieza ...] [--rapido]
#
# Historia: «Tanques del desfile de su cumpleaños. Ha rebautizado Defensa como
#   "Departamento de Guerra"». Acto del Sentido Común. Por Broad Street en un
#   día de desfile: la estación de Main Street con su torre del reloj, el
#   «Departamento de Guerra», el teatro Byrd y los globos de cumpleaños en las
#   aceras. Las minas de confeti escondidas en la calle (un detector avisa) y
#   el momento estrella, el desfile por Monument Avenue al paso del tambor
#   (tocar al ritmo). Final en el Capitolio de Virginia (el templo de
#   Jefferson). Pancarta del Sentido Común: LOS TANQUES ROMPEN LA CALLE.
# Obstáculos (carpeta obstaculos): el tanque del desfile, la tarta de
# cumpleaños, la placa de la mina de confeti y la pancarta.

import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import *

def blanco():    return mat('blanco_ric', 0xf6f4ee, 0.5)
def negro():     return mat('negro_ric', 0x1c1c20, 0.4)
def cristal():   return mat('cristal_ric', 0x3a5a70, 0.15)
def rojo():      return mat('rojo_ric', 0xc8202a, 0.45)
def azul():      return mat('azul_ric', 0x1e4a9a, 0.45)
def amarillo():  return mat('amarillo_ric', 0xf2c21a, 0.45)
def rosa():      return mat('rosa_ric', 0xf08aa8, 0.5)
def verde_m():   return mat('verde_militar_ric', 0x5a6a3a, 0.7)
def verde_o():   return mat('verde_militar_o_ric', 0x3a4a2a, 0.7)
def gris():      return mat('gris_ric', 0x8a9098, 0.4)
def hierro():    return mat('hierro_ric', 0x2a2c30, 0.45)
def madera_o():  return mat('madera_oscura_ric', 0x5a3a22, 0.85)
def ladrillo():  return mat_bloques('ladrillo_ric', 0xa85a3e, 0x7a4030, ancho=0.4, alto=0.16)
def piedra():    return mat_bloques('piedra_ric', 0xd8d4cc, 0xb8b4ac, ancho=1.3, alto=0.6, grosor=0.008)
def piedra_l():  return mat('piedra_lisa_ric', 0xe4e0d8, 0.6)
def cesped():    return mat('cesped_ric', 0x5a9a3a, 0.9)
def teja():      return mat('teja_ric', 0xb8502e, 0.7)

def cartel_sentido(x, y, z, w, h, linea1, linea2=''):
    """La pancarta del Sentido Común: azul, con el cerebro rosa."""
    caja(azul(), x, y, z, w, 0.06, h)
    caja(blanco(), x, y - 0.01, z + h - h * 0.08, w, 0.06, h * 0.08)
    esfera(rosa(), x - w / 2 + h * 0.32, y - 0.06, z + h * 0.5, h * 0.24, 1, esc=(1.2, 0.4, 1))
    texto(blanco(), linea1, x + h * 0.25, y - 0.045, z + h * (0.5 if not linea2 else 0.56), tam=h * 0.3, prof=0.02)
    if linea2:
        texto(amarillo(), linea2, x + h * 0.25, y - 0.045, z + h * 0.2, tam=h * 0.2, prof=0.02)

def globos(x, y, z, n=5, k=1.0):
    for i in range(n):
        a = i * math.tau / n
        gx, gy, gz = x + math.cos(a) * 0.35 * k, y + math.sin(a) * 0.35 * k, z + 1.4 * k + (i % 2) * 0.3 * k
        rama(blanco(), (x, y, z), (gx, gy, gz - 0.3 * k), 0.01, 0.01, 3)
        esfera([rojo, azul, amarillo, rosa, blanco][i % 5](), gx, gy, gz, 0.3 * k, 1, esc=(1, 1, 1.2))

def tanque_m(x, y, z=0.0, k=1.0):
    """Un tanque de oruga verde oliva (de frente a -y)."""
    v = verde_m()
    caja(v, x, y + 3.0 * k, z + 0.5 * k, 2.6 * k, 6.0 * k, 0.9 * k)
    for s in (-1, 1):
        caja(negro(), x + s * 1.25 * k, y + 3.0 * k, z, 0.5 * k, 6.2 * k, 0.9 * k)
        for i in range(5):
            cil(hierro(), x + s * 1.25 * k, y + (0.8 + i * 1.1) * k, z + 0.45 * k, 0.35 * k, 0.52 * k, 10, eje='X')
    caja(verde_o(), x, y + 3.4 * k, z + 1.4 * k, 1.8 * k, 2.4 * k, 0.7 * k)
    cil(verde_o(), x, y + 1.2 * k, z + 1.75 * k, 0.12 * k, 3.4 * k, 8, eje='Y')
    cil(verde_o(), x, y + 3.4 * k, z + 2.1 * k, 0.3 * k, 0.4 * k, 8)

# ================================================================ la meta
def capitolio_va():
    """El Capitolio de Virginia (la meta): el templo romano que diseñó
    Jefferson, blanco, en su colina: el pórtico con seis columnas jónicas y
    el frontón, las alas bajas, la escalinata y el césped con la pancarta."""
    Y = 24
    W, D, H = 30.0, 34.0, 16.0
    yf = Y - D / 2
    caja(cesped(), 0, Y - 4, -0.05, 90, 60, 0.06)
    caja(piedra(), 0, Y, 0, 50, D + 6, 2.5)
    caja(blanco(), 0, Y, 2.5, W, D, H)
    caja(piedra_l(), 0, Y, 2.5 + H, W + 0.6, D + 0.6, 1.0)
    fronton(piedra_l(), 0, yf - 3.0, 3.5 + H, W + 0.6, 5.5, 3.6)
    tejado(mat('tejado_va_ric', 0x8a8e96, 0.6), 0, Y - D / 2, Y + D / 2, 3.5 + H, W, 5.5, cumbrera='y')
    caja(blanco(), 0, yf - 3.0, 2.5, W, 6, 0.6)
    columnata(blanco(), -12.5, 12.5, 6, yf - 5.2, 3.1, 0.75, H - 0.6)
    for k in range(5):
        x = -12 + k * 6
        ventana(x, 6, 1.8, 4.0, y=yf - 0.05, marco=piedra_l(), cristal=cristal())
    for s in (-1, 1):
        caja(blanco(), s * 22, Y + 4, 2.5, 14, 20, 9)
        caja(piedra_l(), s * 22, Y + 4, 11.5, 14.4, 20.4, 0.8)
    for k in range(10):
        caja(piedra_l(), 0, yf - 6.2 - k * 0.5, 0, 22 + k * 0.6, 0.5, 2.5 - k * 0.25)
    for (x, y) in ((-30, yf - 10), (-36, yf - 22), (30, yf - 10), (36, yf - 22)):
        cil(madera_o(), x, y, 0, 0.35, 3.2, 8)
        esfera(mat('copa_ric', 0x3a7a3a, 0.85), x, y, 5.6, 3.2, 2, esc=(1, 1, 1.15))
    cil(gris(), -20, yf - 14, 0, 0.13, 13, 8)
    caja(mat('bandera_va_ric', 0x1e3a7a, 0.6), -18.2, yf - 14, 10.6, 3.6, 0.06, 2.4)
    for x in (8, 22):
        cil(madera_o(), x, yf - 16, 0, 0.12, 4.4, 8)
    cartel_sentido(15, yf - 16, 2.8, 14, 1.6, 'LOS TANQUES ROMPEN LA CALLE', 'EL SENTIDO COMÚN')

# ================================================================ edificios
def estacion_main_st():
    """La estación de Main Street (1901): ladrillo y piedra clara, el tejado
    de teja roja y la torre del reloj con su tejado alto."""
    Y = 10
    W, D = 36.0, 16.0
    yf = Y - D / 2
    l = ladrillo()
    caja(l, 4, Y, 0, 28, D, 12)
    caja(piedra_l(), 4, Y, 0, 28.2, D + 0.2, 1.4)
    tejado(teja(), 4, Y - D / 2, Y + D / 2, 12, 28, 6, cumbrera='x')
    for k in range(6):
        x = -6 + k * 4.2
        cil(piedra_l(), x, yf - 0.06, 4.5, 1.3, 0.12, 14, eje='Y')
        caja(cristal(), x, yf - 0.05, 1.4, 2.4, 0.1, 3.1)
        ventana(x, 7.4, 1.6, 2.6, y=yf - 0.05, marco=piedra_l(), cristal=cristal())
    T = 6.0
    x0 = -12
    caja(l, x0, yf + 1, 0, T, T, 26)
    for z in (12, 20):
        caja(piedra_l(), x0, yf + 1, z, T + 0.4, T + 0.4, 0.6)
    cil(blanco(), x0, yf + 1 - T / 2 - 0.1, 22.5, 2.0, 0.15, 24, eje='Y')
    caja(negro(), x0, yf + 1 - T / 2 - 0.22, 22.5, 0.12, 0.04, 1.5)
    caja(negro(), x0 + 0.45, yf + 1 - T / 2 - 0.22, 22.5, 1.0, 0.04, 0.12)
    o = cil(teja(), x0, yf + 1, 26, T * 0.74, 7, 4, r2=0.2)
    o.rotation_euler = (0, 0, math.pi / 4)
    caja(blanco(), 4, yf - 0.1, 12.3, 12, 0.1, 1.2)
    texto(azul(), 'MAIN STREET STATION', 4, yf - 0.16, 12.55, tam=0.7, prof=0.03)

def departamento_guerra():
    """El «Departamento de Guerra»: el edificio gris de gobierno, con
    columnas cuadradas, el letrero nuevo (DEPARTAMENTO DE GUERRA pegado encima
    de DEFENSA, tachado) y dos tanques de juguete en la puerta."""
    Y = 11
    W, D, H = 34.0, 18.0, 20.0
    yf = Y - D / 2
    p = piedra()
    caja(p, 0, Y, 0, W, D, H)
    caja(piedra_l(), 0, Y, H, W + 0.6, D + 0.6, 1.2)
    for k in range(8):
        x = -14 + k * 4
        caja(piedra_l(), x, yf - 0.4, 0, 1.4, 0.8, 16)
        for z in (2, 7, 12):
            caja(cristal(), x + 2, yf - 0.05, z, 1.8, 0.1, 3.0)
    caja(piedra_l(), 0, yf - 0.5, 16.2, W, 1.0, 1.4)
    texto(gris(), 'DEFENSA', -8, yf - 1.05, 16.5, tam=0.9, prof=0.03)
    caja(rojo(), -8, yf - 1.1, 16.9, 6, 0.04, 0.15)
    caja(amarillo(), 5, yf - 1.08, 16.3, 18, 0.06, 1.2)
    texto(negro(), 'DEPARTAMENTO DE GUERRA', 5, yf - 1.14, 16.55, tam=0.75, prof=0.03)
    puerta(0, 0, 3.0, 4.0, y=yf - 0.05, color=0x3a3a42, marco=piedra_l())
    for s in (-1, 1):
        tanque_m(s * 6, yf - 9, 0, 0.45)

def teatro_byrd():
    """El teatro Byrd (1928): la fachada de ladrillo y piedra, la marquesina
    con bombillas y el rótulo vertical BYRD."""
    Y = 8
    W, D, H = 18.0, 12.0, 13.0
    yf = Y - D / 2
    caja(ladrillo(), 0, Y, 0, W, D, H)
    for x in (-5, 0, 5):
        cil(piedra_l(), x, yf - 0.06, 8.5, 1.3, 0.12, 14, eje='Y')
        caja(cristal(), x, yf - 0.05, 6.0, 2.4, 0.1, 2.5)
    caja(mat('marquesina_byrd_ric', 0x2a2a3a, 0.5), 0, yf - 1.6, 3.4, 13, 3.2, 1.2)
    for k in range(26):
        caja(luz('bombilla_byrd_ric', 0xffe6a0, 1.2), -6.3 + k * 0.5, yf - 3.22, 4.45, 0.14, 0.06, 0.14)
    caja(blanco(), 0, yf - 3.25, 3.5, 12, 0.06, 0.95)
    texto(rojo(), 'BYRD THEATRE', 0, yf - 3.3, 3.75, tam=0.6, prof=0.02)
    caja(rojo(), 0, yf - 1.0, 5.2, 1.3, 1.2, 7.2)
    for k, ch in enumerate('BYRD'):
        texto(amarillo(), ch, 0, yf - 1.62, 11.0 - k * 1.5, tam=1.2, prof=0.03)

def globo_cumple():
    """Un poste con un ramo de globos de cumpleaños (para la acera)."""
    cil(gris(), 0, 0, 0, 0.06, 1.4, 6)
    caja(blanco(), 0, -0.07, 0.9, 0.5, 0.02, 0.35)
    texto(rojo(), '79', 0, -0.08, 0.98, tam=0.2, prof=0.01)
    globos(0, 0, 1.4, 6, 1.0)

# ================================================================ cruza la calle
def arco_desfile():
    """El arco del desfile de cumpleaños: dos postes con globos y la pancarta
    ¡FELIZ CUMPLEAÑOS, SEÑOR PRESIDENTE!; por detrás, DESFILE MILITAR."""
    for s in (-1, 1):
        caja(blanco(), s * 8.6, 0, 0, 0.6, 0.6, 7.8)
        globos(s * 8.6, 0, 7.8, 6, 1.4)
    caja(blanco(), 0, 0, 7.0, 18.0, 0.4, 0.5)
    caja(azul(), 0, 0, 4.4, 14, 0.18, 1.8)
    texto(amarillo(), '¡FELIZ CUMPLEAÑOS,', 0, -0.12, 5.3, tam=0.6, prof=0.04)
    texto(blanco(), 'SEÑOR PRESIDENTE!', 0, -0.12, 4.65, tam=0.55, prof=0.04)
    o = texto(amarillo(), 'DESFILE MILITAR', 0, 0.12, 5.0, tam=0.7, prof=0.04)
    o.rotation_euler = (math.pi / 2, 0, math.pi)

# ================================================================ el desfile
def desfile_monument():
    """El desfile por Monument Avenue (momento estrella, al aire libre): el
    paseo con su mediana de árboles, el público tras las vallas con
    banderitas, los tanques aparcados en fila, la carroza de la tarta de
    cumpleaños gigante, la tribuna, los tambores y los arcos de SALIDA y
    META. Cruza la calle: el origen en el centro."""
    L = 420
    caja(mat('asfalto_desfile_ric', 0x55585e, 0.9), 0, 0, -0.2, 24, L, 0.2)
    for s in (-1, 1):
        for k in range(int(L / 3)):
            caja(mat('valla_desfile_ric', 0xb8bcc4, 0.4), s * 7.6, -L / 2 + 1.5 + k * 3, 0, 0.08, 2.8, 1.1)
        for g in range(4):
            caja(mat_bloques('gente_ric', 0x8a5a7a, 0x2a2a30, ancho=0.5, alto=0.7, variacion=1.7), s * (9.5 + g * 2.6), 0, 0, 2.6, L, 1.7 + g * 0.3)
        for k in range(int(L / 4)):
            y = -L / 2 + 2 + k * 4
            cil(blanco(), s * 9.2, y, 1.7, 0.02, 0.7, 4)
            caja([rojo, azul, blanco][k % 3](), s * 9.2, y + 0.2, 2.25, 0.02, 0.4, 0.25)
        for k in range(int(L / 18)):
            y = -L / 2 + 9 + k * 18
            cil(madera_o(), s * 20, y, 0, 0.35, 3.5, 8)
            esfera(mat('copa_ric', 0x3a7a3a, 0.85), s * 20, y, 6, 3, 2, esc=(1, 1, 1.15))
    # Los tanques en fila a un lado y la tribuna al otro.
    for k in range(int(L / 35)):
        tanque_m(-16, -L / 2 + 10 + k * 35, 0, 1.0)
    for k in range(int(L / 105)):
        y = -L / 2 + 50 + k * 105
        caja(mat('tribuna_ric', 0x2a3a6a, 0.6), 18, y, 0, 6, 16, 2.0)
        caja(rojo(), 18, y, 2.0, 6.2, 16.2, 0.2)
        caja(blanco(), 15, y, 2.2, 0.1, 14, 1.0)
        texto(azul(), 'TRIBUNA', 14.94, y, 2.45, tam=0.5, prof=0.02).rotation_euler = (math.pi / 2, 0, math.pi / 2)
    # La carroza de la tarta.
    for y in (-60, 120):
        caja(mat('carroza_ric', 0x2a4a9a, 0.5), -14, y, 0, 5, 8, 1.2)
        cil(rosa(), -14, y, 1.2, 2.2, 1.6, 24)
        cil(blanco(), -14, y, 2.8, 1.6, 1.2, 24)
        for k in range(7):
            a = k * math.tau / 7
            cil(amarillo(), -14 + math.cos(a) * 1.1, y + math.sin(a) * 1.1, 4.0, 0.08, 0.8, 6)
    for (y, txt) in ((-L / 2 + 1, 'SALIDA'), (L / 2 - 1, 'META')):
        for s in (-1, 1):
            caja(blanco(), s * 7.0, y, 0, 0.5, 0.5, 6.2)
            globos(s * 7.0, y, 6.2, 5, 1.1)
        caja(blanco(), 0, y, 5.6, 14.6, 0.5, 0.6)
        caja(azul(), 0, y, 4.0, 10, 0.16, 1.4)
        texto(amarillo(), 'DESFILE · ' + txt, 0, y - 0.1, 4.45, tam=0.6, prof=0.04)

# ================================================================ obstáculos
def tanque():
    """El tanque del desfile (no se pasa): verde oliva, con sus orugas, la
    torreta, el cañón y una banderita. El morro en el origen."""
    tanque_m(0, 0.4, 0, 0.85)
    cil(gris(), 0.5, 3.2, 2.1, 0.03, 1.2, 4)
    caja(rojo(), 0.8, 3.2, 2.9, 0.5, 0.02, 0.3)

def tarta_cumple():
    """La tarta de cumpleaños en su mesita (se salta): rosa y blanca, con las
    velas."""
    caja(blanco(), 0, 0, 0, 1.6, 0.8, 0.45)
    cil(rosa(), 0, 0, 0.45, 0.45, 0.3, 20)
    cil(blanco(), 0, 0, 0.75, 0.32, 0.18, 20)
    for k in range(5):
        a = k * math.tau / 5
        cil(amarillo(), math.cos(a) * 0.22, math.sin(a) * 0.22, 0.93, 0.025, 0.14, 6)

def placa_mina():
    """La placa de la mina de confeti (aparece al pisarla): el disco de metal
    y el cono de fiesta reventado."""
    cil(hierro(), 0, 0, 0, 0.45, 0.06, 16)
    cil(rojo(), 0, 0, 0.06, 0.12, 0.35, 10, r2=0.2)
    for k in range(10):
        a = k * math.tau / 10
        caja([rojo, azul, amarillo, rosa][k % 4](), math.cos(a) * 0.4, math.sin(a) * 0.4, 0.02, 0.1, 0.06, 0.01)

def cartel_va():
    """La pancarta del Sentido Común (agacharse): LOS TANQUES ROMPEN LA CALLE."""
    for x in (-1.25, 1.25):
        cil(madera_o(), x, 0, 0, 0.07, 2.75, 8)
    caja(azul(), 0, 0, 1.5, 2.4, 0.05, 1.2)
    esfera(rosa(), -0.9, -0.05, 2.1, 0.2, 1, esc=(1.2, 0.4, 1))
    texto(blanco(), 'LOS TANQUES', 0.15, -0.035, 2.25, tam=0.2, prof=0.02)
    texto(blanco(), 'ROMPEN', 0.15, -0.035, 1.98, tam=0.2, prof=0.02)
    texto(amarillo(), 'LA CALLE', 0.15, -0.035, 1.7, tam=0.2, prof=0.02)

PIEZAS = {
    'capitolio_va':        (capitolio_va,        'richmond',   dict(lado=2048, bisel=0.0)),
    'estacion_main_st':    (estacion_main_st,    'richmond',   dict(lado=1024, bisel=0.0)),
    'departamento_guerra': (departamento_guerra, 'richmond',   dict(lado=1024, bisel=0.0)),
    'teatro_byrd':         (teatro_byrd,         'richmond',   dict(lado=1024, bisel=0.0)),
    'globo_cumple':        (globo_cumple,        'richmond',   dict(lado=256, bisel=0.0)),
    'arco_desfile':        (arco_desfile,        'richmond',   dict(lado=1024, bisel=0.0, suelo=False)),
    'desfile_monument':    (desfile_monument,    'richmond',   dict(lado=2048, bisel=0.0, suelo=False)),
    'tanque':              (tanque,              'obstaculos', dict(lado=256, bisel=0.0)),
    'tarta_cumple':        (tarta_cumple,        'obstaculos', dict(lado=256, bisel=0.0)),
    'placa_mina':          (placa_mina,          'obstaculos', dict(lado=256, bisel=0.0)),
    'cartel_va':           (cartel_va,           'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
}

correr(PIEZAS)
