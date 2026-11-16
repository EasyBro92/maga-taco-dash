# Nivel 47: Portland, Maine (16/11/2026).
#
#   blender -b -P blender/portlandme.py -- [pieza ...] [--rapido]
#
# Historia: «Langostas». Acto del Sentido Común. Por el Old Port: el
#   observatorio octogonal de 1807, los almacenes de ladrillo del puerto, la
#   casa de las langostas con la pared llena de boyas y, cruzando la calle, el
#   arco de pilotes del muelle. La medida de la langosta: solo valen las de
#   la medida (las pequeñas y las gigantes, al agua, o multa); el momento
#   estrella, la costa en la niebla: no se ve nada, pero el haz del faro va
#   marcando lo que viene con luces de colores. Final en el faro de Portland
#   Head. Pancarta del Sentido Común: SI HAY NIEBLA, VE DESPACIO.
# Obstáculos (carpeta obstaculos): la langosta (roja y azul), el camión de
# las langostas, la boya caída y la pancarta.

import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import *

def blanco():    return mat('blanco_pme', 0xf6f4ee, 0.5)
def negro():     return mat('negro_pme', 0x1c1c20, 0.4)
def cristal():   return mat('cristal_pme', 0x3a5a70, 0.15)
def rojo():      return mat('rojo_pme', 0xc8302a, 0.5)
def azul():      return mat('azul_pme', 0x1e4a9a, 0.45)
def amarillo():  return mat('amarillo_pme', 0xf2c21a, 0.45)
def rosa():      return mat('rosa_pme', 0xf08aa8, 0.5)
def verde():     return mat('verde_pme', 0x2a5a3a, 0.6)
def gris():      return mat('gris_pme', 0x8a9098, 0.4)
def tejas():     return mat('tejas_pme', 0x9aa0a4, 0.85)
def madera():    return mat('madera_pme', 0x9a6a3e, 0.85)
def madera_o():  return mat('madera_oscura_pme', 0x5a3a22, 0.85)
def ladrillo():  return mat_bloques('ladrillo_pme', 0x9a4a32, 0x6a3426, ancho=0.4, alto=0.16)
def granito():   return mat_bloques('granito_pme', 0xb0aca4, 0x8a8680, ancho=1.2, alto=0.6, grosor=0.008)
def roca():      return mat('roca_pme', 0x6a6660, 0.9)
def mar():       return mat('mar_pme', 0x3a5a6a, 0.15)
def pino():      return mat('pino_pme', 0x1e4a32, 0.8)
def langosta_r(): return mat('langosta_pme', 0xd0301e, 0.45)
def farol():     return luz('farol_pme', 0xfff0b0, 1.4)
BOYAS = [(0xe8402a, 0xf2f0e8), (0xf2c21a, 0x1e4a9a), (0x2a8a4a, 0xf2f0e8), (0xf08aa8, 0x1c1c20), (0x1e8ac8, 0xf2c21a)]

def cartel_sentido(x, y, z, w, h, linea1, linea2=''):
    caja(azul(), x, y, z, w, 0.06, h)
    caja(blanco(), x, y - 0.01, z + h - h * 0.08, w, 0.06, h * 0.08)
    esfera(rosa(), x - w / 2 + h * 0.32, y - 0.06, z + h * 0.5, h * 0.24, 1, esc=(1.2, 0.4, 1))
    texto(blanco(), linea1, x + h * 0.25, y - 0.045, z + h * (0.5 if not linea2 else 0.56), tam=h * 0.3, prof=0.02)
    if linea2:
        texto(amarillo(), linea2, x + h * 0.25, y - 0.045, z + h * 0.2, tam=h * 0.2, prof=0.02)

def boya(x, y, z, k=1.0, i=0, eje='Z'):
    """Una boya de langostero de dos colores (de pie o colgada)."""
    c1, c2 = BOYAS[i % len(BOYAS)]
    esfera(mat(f'boya_pme_{i % 5}a', c1, 0.5), x, y, z + 0.35 * k, 0.2 * k, 1, esc=(1, 1, 1.9))
    cil(mat(f'boya_pme_{i % 5}b', c2, 0.5), x, y, z + 0.3 * k, 0.205 * k, 0.14 * k, 10)
    cil(madera_o(), x, y, z + 0.7 * k, 0.03 * k, 0.4 * k, 6)

def nasa(x, y, z=0, k=1.0):
    """Una nasa de langostas: la caja de rejilla verde con el marco."""
    caja(mat('rejilla_pme', 0x3a6a4a, 0.7), x, y, z, 1.1 * k, 0.6 * k, 0.45 * k)
    for dx in (-0.5, 0.5):
        caja(madera(), x + dx * k, y, z + 0.45 * k, 0.06 * k, 0.62 * k, 0.04 * k)

def langosta_m(m, x, y, z, k=1.0):
    """Una langosta (mirando a -y, con las pinzas en alto)."""
    esfera(m, x, y + 0.1 * k, z + 0.22 * k, 0.2 * k, 2, esc=(0.9, 1.6, 0.8))
    for i in range(4):
        esfera(m, x, y + (0.45 + i * 0.16) * k, z + (0.2 - i * 0.02) * k, (0.15 - i * 0.02) * k, 1, esc=(1.1, 0.8, 0.6))
    caja(m, x, y + 1.15 * k, z + 0.1 * k, 0.32 * k, 0.12 * k, 0.04 * k)
    for s in (-1, 1):
        rama(m, (x + s * 0.12 * k, y - 0.15 * k, z + 0.3 * k), (x + s * 0.32 * k, y - 0.45 * k, z + 0.55 * k), 0.05 * k, 0.04 * k, 6)
        esfera(m, x + s * 0.36 * k, y - 0.62 * k, z + 0.62 * k, 0.15 * k, 2, esc=(0.8, 1.5, 0.7))
        rama(m, (x + s * 0.06 * k, y - 0.25 * k, z + 0.3 * k), (x + s * 0.3 * k, y - 0.9 * k, z + 0.4 * k), 0.012 * k, 0.008 * k, 4)
        for j in range(3):
            rama(m, (x + s * 0.12 * k, y + (0.05 + j * 0.13) * k, z + 0.18 * k), (x + s * 0.3 * k, y + (0.05 + j * 0.13) * k, z), 0.02 * k, 0.015 * k, 4)
        esfera(negro(), x + s * 0.07 * k, y - 0.17 * k, z + 0.36 * k, 0.035 * k, 1)

# ================================================================ la meta
def faro_portland():
    """El faro de Portland Head (la meta): las rocas, la torre blanca de
    cono, la galería negra, la linterna con la luz, la casa del farero de
    tejado rojo y la valla; delante, la pancarta del Sentido Común."""
    Y = 26
    r = roca()
    caja(mat('hierba_pme', 0x6a8a4a, 0.9), 0, Y - 12, -0.05, 100, 60, 0.06)
    for k in range(14):
        a = k * 0.9
        esfera(r, -14 + (k * 7) % 30, Y + 6 + (k * 5) % 12, 0, 2.5 + (k % 3), 1, esc=(1.3, 1, 0.5))
    T = blanco()
    cil(T, 0, Y + 4, 0, 3.4, 22, 20, r2=2.3)
    for z in (6, 12, 17):
        caja(cristal(), 0, Y + 4 - 2.9 + z * 0.045, z, 0.6, 0.1, 1.0)
    cil(negro(), 0, Y + 4, 22, 3.0, 0.4, 20)
    for k in range(16):
        a = k * math.tau / 16
        cil(negro(), math.cos(a) * 2.9, Y + 4 + math.sin(a) * 2.9, 22.4, 0.04, 1.0, 4)
    cil(negro(), 0, Y + 4, 23.4, 2.95, 0.1, 20)
    cil(cristal(), 0, Y + 4, 22.4, 1.6, 2.6, 12)
    esfera(farol(), 0, Y + 4, 23.6, 0.9, 2)
    cupula(negro(), 0, Y + 4, 25.0, 1.8, 1.4, 16, 4)
    esfera(negro(), 0, Y + 4, 26.6, 0.25, 1)
    caja(blanco(), 9, Y + 2, 0, 12, 8, 6)
    tejado(mat('tejado_rojo_pme', 0xa8302a, 0.6), 9, Y - 2, Y + 6, 6, 12, 2.8, cumbrera='x')
    for x in (5.5, 9, 12.5):
        for z in (1.2, 3.8):
            ventana(x, z, 1.1, 1.6, y=Y - 2.05, marco=blanco(), cristal=cristal())
    cil(ladrillo(), 11, Y + 3, 8, 0.5, 1.8, 6)
    for k in range(12):
        caja(blanco(), -12 + k * 2.2, Y - 6, 0, 0.1, 0.1, 1.1)
    caja(blanco(), -0.5, Y - 6, 0.8, 26, 0.1, 0.12)
    for x in (8, 22):
        cil(madera_o(), x, Y - 18, 0, 0.12, 4.4, 8)
    cartel_sentido(15, Y - 18, 2.8, 15, 1.6, 'SI HAY NIEBLA, VE DESPACIO', 'EL SENTIDO COMÚN')

# ================================================================ edificios
def observatorio_portland():
    """El observatorio de Portland (1807): la torre octogonal de tablas
    rojizas que se estrecha, las bandas blancas, el mirador acristalado de
    arriba con su cúpula y los mástiles de las banderas de señales."""
    Y = 8
    m = mat('tablas_obs_pme', 0x8a4a3a, 0.8)
    o = cil(m, 0, Y, 0, 4.2, 20, 8, r2=3.0)
    o.rotation_euler = (0, 0, math.pi / 8)
    for z in (6, 12, 18):
        r = 4.2 - 1.2 * z / 20
        b = cil(blanco(), 0, Y, z, r + 0.08, 0.3, 8)
        b.rotation_euler = (0, 0, math.pi / 8)
    for z in (3, 9, 15):
        caja(cristal(), 0, Y - (4.0 - 1.2 * z / 20) + 0.05, z, 0.9, 0.1, 1.4)
    b = cil(blanco(), 0, Y, 20, 3.4, 0.4, 8)
    b.rotation_euler = (0, 0, math.pi / 8)
    c = cil(cristal(), 0, Y, 20.4, 2.6, 2.4, 8)
    c.rotation_euler = (0, 0, math.pi / 8)
    for k in range(8):
        a = k * math.tau / 8
        cil(blanco(), math.cos(a) * 2.6, Y + math.sin(a) * 2.6, 20.4, 0.08, 2.4, 4)
    cupula(m, 0, Y, 22.8, 2.8, 1.6, 8, 3)
    cil(blanco(), 0, Y, 24.4, 0.08, 4, 6)
    for (x, c1) in ((-3, 0xc8302a), (3, 0x1e4a9a)):
        cil(blanco(), x, Y + 4, 0, 0.08, 14, 6)
        caja(mat(f'senal_pme_{c1}', c1, 0.5), x + 0.5, Y + 4, 12.6, 1.0, 0.04, 0.7)
    caja(m, 0, Y, 0, 6, 6, 3)
    caja(blanco(), 0, Y - 3.05, 2.2, 5, 0.1, 0.6)
    texto(negro(), 'OBSERVATORY 1807', 0, Y - 3.1, 2.3, tam=0.38, prof=0.02)

def almacen_old_port():
    """Los almacenes de ladrillo del Old Port: cuatro pisos, el zócalo de
    granito, las ventanas de arco, la cornisa y las tiendas de abajo."""
    Y = 8
    W, D, H = 24.0, 14.0, 14.0
    yf = Y - D / 2
    l = ladrillo()
    caja(granito(), 0, Y, 0, W, D, 3.6)
    caja(l, 0, Y, 3.6, W, D, H - 3.6)
    caja(granito(), 0, Y, H, W + 0.6, D + 0.6, 0.8)
    for k in range(6):
        x = -10 + k * 4
        for z in (4.6, 7.6, 10.6):
            caja(cristal(), x, yf - 0.05, z, 1.5, 0.1, 2.0)
            cil(granito(), x, yf - 0.06, z + 2.0, 0.8, 0.1, 10, eje='Y')
    for (x, c, txt) in ((-7, 0x2a5a3a, 'OLD PORT'), (0, 0xc8302a, 'LANGOSTAS VIVAS'), (7, 0x1e4a9a, 'CAFÉ')):
        caja(cristal(), x, yf - 0.05, 0.3, 5.5, 0.1, 2.6)
        caja(mat(f'toldo_pme_{c}', c, 0.6), x, yf - 0.9, 2.9, 6, 1.8, 0.12, inclina=-0.3)
        texto(blanco(), txt, x, yf - 0.12, 3.15, tam=0.4, prof=0.02)

def casa_langostas():
    """La casa de las langostas: la caseta de tablillas grises, la pared
    llena de boyas de colores colgadas, las nasas apiladas, las mesas de
    picnic y el cartel LOBSTER SHACK."""
    Y = 7
    W, D, H = 10.0, 8.0, 4.5
    yf = Y - D / 2
    caja(tejas(), 0, Y, 0, W, D, H)
    tejado(mat('tejado_shack_pme', 0x4a4a52, 0.6), 0, Y - D / 2, Y + D / 2, H, W, 2.2, cumbrera='x')
    hastial(tejas(), 0, Y - D / 2, Y + D / 2, H, W, 2.2, cumbrera='x')
    for k in range(18):
        boya(-4.2 + (k % 9) * 1.05, yf - 0.12, 0.9 + (k // 9) * 1.5, 0.9, k)
    caja(cristal(), 2.5, yf - 0.05, 3.1, 2.2, 0.1, 1.0)
    caja(blanco(), -1.5, yf - 0.1, 3.5, 5, 0.1, 0.8)
    texto(rojo(), 'LOBSTER SHACK', -1.5, yf - 0.16, 3.65, tam=0.45, prof=0.02)
    for k in range(5):
        nasa(W / 2 + 1.0, yf + 1 + (k % 2) * 0.7, (k // 2) * 0.47, 1.0)
    for x in (-3, 2):
        caja(madera(), x, yf - 4, 0.7, 2.2, 0.9, 0.08)
        for s in (-1, 1):
            caja(madera(), x, yf - 4 + s * 0.8, 0.4, 2.2, 0.3, 0.06)
            caja(madera(), x + s * 0.9, yf - 4, 0, 0.08, 1.8, 0.7)
    langosta_m(langosta_r(), 0, yf - 0.4, H + 1.6, 1.6)

def nasas_apiladas():
    """Las nasas apiladas con su boya (para la acera)."""
    nasa(0, 0, 0)
    nasa(0.1, 0.05, 0.47)
    nasa(-0.05, 0, 0.94, 0.95)
    boya(0.75, -0.2, 0, 1.0, 1)

# ================================================================ cruza la calle
def arco_old_port():
    """El arco del muelle del Old Port: dos pilotes gordos de madera con las
    cuerdas enrolladas, el travesaño con OLD PORT · PORTLAND, MAINE y las
    boyas colgadas."""
    for s in (-1, 1):
        cil(madera_o(), s * 9, 0, 0, 0.55, 7.5, 12)
        for z in (2.0, 2.3):
            cil(mat('cuerda_pme', 0xc8b088, 0.9), s * 9, 0, z, 0.62, 0.22, 12)
        esfera(madera_o(), s * 9, 0, 7.5, 0.55, 1, esc=(1, 1, 0.4))
    caja(madera(), 0, 0, 6.2, 19, 0.8, 1.0)
    caja(blanco(), 0, -0.42, 6.3, 11, 0.06, 0.8)
    texto(azul(), 'OLD PORT · PORTLAND, MAINE', 0, -0.47, 6.5, tam=0.5, prof=0.02)
    for k in range(8):
        x = -7.7 + k * 2.2
        if abs(x) < 5.6:
            continue
        cil(mat('cuerda_pme', 0xc8b088, 0.9), x, 0, 5.1, 0.025, 1.1, 4)
        boya(x, 0, 4.3, 1.1, k)

# ================================================================ la costa en la niebla
def costa_niebla():
    """La costa de Cape Elizabeth en la niebla (momento estrella): la
    carretera junto al mar, las rocas, los pinos a la izquierda, el mar a la
    derecha con boyas, los faroles de la orilla y, al final, el pequeño faro
    del espigón. Cruza la calle: el origen en el centro."""
    L = 420
    # (el suelo: en los tramos de dentro el juego quita su calle)
    caja(mat('asfalto_pme', 0x3a3c40, 0.9), 0, 0, -0.2, 17, L, 0.2)
    for x in (-1.1, 1.1):
        for k in range(int(L / 6)):
            caja(blanco(), x, -L / 2 + 3 + k * 6, -0.02, 0.12, 2.5, 0.03)
    caja(mat('hierba_costa_pme', 0x4a6a3a, 0.95), -40, 0, -0.2, 64, L, 0.2)
    caja(mar(), 50, 0, 0.1, 80, L, 0.04)
    for s in (-1, 1):
        for k in range(int(L / 1.8)):
            y = -L / 2 + 0.9 + k * 1.8
            caja(roca(), s * (8.2 + ((k * 13) % 5) * 0.3), y, -0.1, 1.5, 1.7, 0.35 + ((k * 37) % 7) * 0.08, giro=((k * 29) % 9) * 0.2)
    for k in range(int(L / 9)):
        y = -L / 2 + 4 + k * 9
        x = -12 - (k * 7) % 9
        cil(madera_o(), x, y, 0, 0.25, 1.2, 6)
        cil(pino(), x, y, 1.0, 1.8, 3.5, 7, r2=0.9)
        cil(pino(), x, y, 3.6, 1.3, 3.2, 7, r2=0.0)
    for k in range(int(L / 30)):
        y = -L / 2 + 15 + k * 30
        cil(negro(), 7.0, y, 0, 0.08, 3.4, 6)
        esfera(farol(), 7.0, y, 3.5, 0.22, 1)
        boya(20 + (k * 11) % 20, y + 8, 0.0, 1.8, k)
    Yf = L / 2 - 8
    cil(blanco(), 16, Yf, 0, 1.6, 7, 12, r2=1.3)
    cil(negro(), 16, Yf, 7, 1.5, 1.4, 12)
    esfera(farol(), 16, Yf, 7.7, 0.6, 1)
    cupula(negro(), 16, Yf, 8.4, 1.3, 0.8, 12, 3)

# ================================================================ obstáculos
def langosta():
    """La langosta en la calle (se coge si es de la medida; el juego la
    escala: pequeña, de ley o gigante). El origen en el suelo; mira a -y."""
    langosta_m(langosta_r(), 0, 0, 0, 1.0)

def langosta_azul():
    """La langosta azul (una entre un millón): vale siempre."""
    langosta_m(mat('langosta_azul_pme', 0x2a6ac8, 0.35), 0, 0, 0, 1.0)

def camion_langostas():
    """El camión de las langostas (no se pasa): rojo, con la langosta gigante
    en el techo y LANGOSTAS DE MAINE. El morro en el origen."""
    r = rojo()
    caja(r, 0, 1.0, 0.45, 2.3, 2.0, 1.9)
    caja(cristal(), 0, -0.02, 1.5, 2.0, 0.1, 0.7)
    caja(blanco(), 0, 4.4, 0.45, 2.4, 4.6, 2.5)
    for s in (-1, 1):
        texto(r, 'LANGOSTAS DE MAINE', s * 1.22, 4.4, 1.7, tam=0.24, prof=0.01).rotation_euler = (math.pi / 2, 0, -s * math.pi / 2)
    langosta_m(langosta_r(), 0, 4.0, 2.95, 1.7)
    for (y, s) in ((1.0, 1), (5.4, 1), (1.0, -1), (5.4, -1)):
        cil(negro(), s * 1.1, y, 0.45, 0.45, 0.3, 14, eje='X')
    for s in (-1, 1):
        caja(luz('faro_camion_pme', 0xfff2c0, 1.0), s * 0.8, -0.03, 0.85, 0.35, 0.05, 0.2)

def boya_suelta():
    """La boya grande caída en la calle (se salta), con su cuerda."""
    esfera(mat('boya_pme_0a', 0xe8402a, 0.5), 0, 0, 0.4, 0.4, 2, esc=(2.0, 1, 1))
    cil(mat('boya_pme_1b', 0x1e4a9a, 0.5), 0, 0, 0.4, 0.41, 0.3, 14, eje='X')
    cil(madera_o(), 1.0, 0, 0.4, 0.06, 0.6, 6, eje='X')
    rama(mat('cuerda_pme', 0xc8b088, 0.9), (1.3, 0, 0.4), (1.5, 0.6, 0.03), 0.03, 0.03, 4)

def cartel_me():
    """La pancarta del Sentido Común (agacharse): SI HAY NIEBLA, VE DESPACIO."""
    for x in (-1.25, 1.25):
        cil(madera_o(), x, 0, 0, 0.07, 2.75, 8)
    caja(azul(), 0, 0, 1.5, 2.4, 0.05, 1.2)
    esfera(rosa(), -0.9, -0.05, 2.1, 0.2, 1, esc=(1.2, 0.4, 1))
    texto(blanco(), 'SI HAY NIEBLA,', 0.15, -0.035, 2.2, tam=0.2, prof=0.02)
    texto(amarillo(), 'VE DESPACIO', 0.15, -0.035, 1.8, tam=0.2, prof=0.02)

PIEZAS = {
    'faro_portland':         (faro_portland,         'portlandme', dict(lado=2048, bisel=0.0)),
    'observatorio_portland': (observatorio_portland, 'portlandme', dict(lado=1024, bisel=0.0)),
    'almacen_old_port':      (almacen_old_port,      'portlandme', dict(lado=1024, bisel=0.0)),
    'casa_langostas':        (casa_langostas,        'portlandme', dict(lado=1024, bisel=0.0)),
    'nasas_apiladas':        (nasas_apiladas,        'portlandme', dict(lado=256, bisel=0.0)),
    'arco_old_port':         (arco_old_port,         'portlandme', dict(lado=1024, bisel=0.0, suelo=False)),
    'costa_niebla':          (costa_niebla,          'portlandme', dict(lado=2048, bisel=0.0, suelo=False)),
    'langosta':              (langosta,              'obstaculos', dict(lado=256, bisel=0.0)),
    'langosta_azul':         (langosta_azul,         'obstaculos', dict(lado=256, bisel=0.0)),
    'camion_langostas':      (camion_langostas,      'obstaculos', dict(lado=256, bisel=0.0)),
    'boya_suelta':           (boya_suelta,           'obstaculos', dict(lado=256, bisel=0.0)),
    'cartel_me':             (cartel_me,             'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
}

correr(PIEZAS)
