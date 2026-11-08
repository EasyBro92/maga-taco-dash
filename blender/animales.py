# Los animales rehechos y el micrófono de verdad (08/11/2026).
#
#   blender -b -P blender/animales.py -- [pieza ...] [--rapido]
#
# Isidro (08/11): «mejora el diseño de los animales, las animaciones como
# caminan» y «los micrófono se ven muy claros hazlos mas realistas».
#   · Cada animal es ahora DOS piezas: el cuerpo sin patas y una pata (con el
#     origen en la cadera). El juego (world.js, ANDAR) pone cuatro patas en
#     su sitio y las mueve al andar, al paso que lleva el animal: ya no se
#     deslizan por la calle con las patas quietas.
#   · Formas de animal (lomo, pecho, grupa, cuello, cabeza con hocico, ojos
#     con brillo, orejas, cola) y pelo con un poco de textura.
#   · Los caballos del coche de Central Park y del carro de cerveza de San
#     Luis también llevan las patas aparte (sus cuerpos se rehacen en
#     obstaculos3.py y sanluis.py).
#   · El micrófono que se coge en Las Vegas: rejilla de metal oscuro, mango
#     negro mate y anillo cromado, como uno de verdad (antes era dorado y
#     gris claro y brillaba demasiado).
# Ejes: x hacia delante (la cabeza), y de lado, z arriba. Las patas cuelgan
# hacia -z desde su origen; las caderas están en world.js (ANDAR) y tienen que
# coincidir con las de aquí.

import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import *

def negro():  return mat('negro_an', 0x1b1c20, 0.45)
def blanco(): return mat('blanco_an', 0xf7f5ef, 0.6)
def pezuna(): return mat('pezuna_an', 0x2a2420, 0.5)
def brillo(): return mat('brillo_ojo', 0xffffff, 0.1)

def pelo(nombre, color, oscuro):
    """Pelo con algo de textura: manchitas alargadas de dos tonos parecidos."""
    # (sin junta: solo cambia un poco el tono de una manchita a otra)
    return mat_bloques(nombre, color, color, ancho=0.07, alto=0.12, grosor=0.0, desfase=0.37, variacion=1.09)

def ojo(x, y, z, r, s):
    """Ojo oscuro con su brillo (s = lado, -1 o 1)."""
    esfera(mat('ojo_an', 0x16110e, 0.15), x, y, z, r, 2)
    esfera(brillo(), x + r * 0.45, y + s * r * 0.55, z + r * 0.4, r * 0.3, 1)

def girar(o, rx=0.0, ry=0.0, rz=0.0):
    o.rotation_euler = (rx, ry, rz)
    return o

# ---------------------------------------------------------------- la vaca
def vaca():
    """Vaca frisona: cuerpo blanco con manchas negras, cabeza negra con la
    franja blanca, hocico rosado, cuernos cortos, ubre, cola con borla y el
    cencerro. Sin patas (vaca_pata). Cruza mirando a +x."""
    b = pelo('pelo_vaca', 0xf6f4ee, 0xe9e5dc)
    n = pelo('pelo_vaca_negro', 0x1f2024, 0x2a2b30)
    esfera(b, 0, 0, 1.05, 0.5, 3, esc=(1.7, 0.95, 0.84))                   # el tronco
    esfera(b, 0.58, 0, 1.08, 0.42, 3, esc=(1.0, 1.0, 1.08))               # pecho y cruz
    esfera(b, -0.6, 0, 1.12, 0.41, 3, esc=(1.0, 1.08, 1.0))               # la grupa
    esfera(b, 0.02, 0, 0.84, 0.44, 3, esc=(1.45, 0.98, 0.66))             # la tripa
    for s in (-1, 1):
        esfera(b, -0.62, s * 0.31, 1.4, 0.1, 2)                          # los huesos de la cadera
    # manchas negras en los lados y el lomo
    for x, y, z, r in ((0.18, -0.46, 1.08, 0.27), (-0.42, -0.44, 1.0, 0.2), (0.55, -0.42, 1.22, 0.17),
                       (-0.1, 0.47, 1.14, 0.28), (0.48, 0.43, 0.96, 0.16), (-0.62, 0.42, 1.2, 0.2)):
        esfera(n, x, y, z, r, 2, esc=(1.35, 0.22, 1.0))
    esfera(n, -0.18, 0, 1.47, 0.24, 2, esc=(1.4, 1.2, 0.2))
    esfera(n, 0.5, 0, 1.47, 0.16, 2, esc=(1.2, 1.3, 0.2))
    # el cuello, la papada y la cabeza
    rama(n, (0.8, 0, 1.2), (1.04, 0, 1.3), 0.31, 0.22, 14)
    esfera(b, 0.92, 0, 0.92, 0.17, 2, esc=(1.0, 0.5, 1.25))
    esfera(n, 1.16, 0, 1.28, 0.19, 3, esc=(1.45, 0.92, 1.0))
    esfera(b, 1.36, 0, 1.3, 0.09, 2, esc=(0.45, 0.65, 1.6))               # la franja blanca
    esfera(mat('hocico_vaca', 0xe8a8a0, 0.55), 1.39, 0, 1.13, 0.14, 3, esc=(1.1, 1.15, 0.88))
    for s in (-1, 1):
        esfera(mat('fosa_vaca', 0x4a2a2a, 0.6), 1.53, s * 0.055, 1.14, 0.022, 1)
        ojo(1.25, s * 0.16, 1.33, 0.035, s)
        o = esfera(n, 1.08, s * 0.27, 1.37, 0.1, 2, esc=(0.55, 1.5, 0.35))   # orejas
        girar(o, rx=s * 0.25)
        esfera(mat('oreja_dentro', 0xe8a8a0, 0.6), 1.1, s * 0.27, 1.36, 0.06, 1, esc=(0.4, 1.3, 0.2))
        rama(mat('cuerno', 0xf1e8d6, 0.45), (1.1, s * 0.11, 1.44), (1.14, s * 0.25, 1.53), 0.035, 0.012, 7)
    esfera(n, 1.12, 0, 1.45, 0.08, 2, esc=(1.0, 1.5, 0.5))                # el flequillo
    rama(mat('boca_vaca', 0x6a3a3a, 0.6), (1.47, -0.07, 1.06), (1.47, 0.07, 1.06), 0.01, 0.01, 5)
    # la ubre, la cola y el cencerro
    rosa = mat('ubre', 0xf0b0aa, 0.55)
    esfera(rosa, -0.36, 0, 0.66, 0.17, 2, esc=(1.1, 1.0, 0.8))
    for dx in (-0.07, 0.07):
        for dy in (-0.07, 0.07):
            rama(rosa, (-0.36 + dx, dy, 0.58), (-0.36 + dx, dy, 0.5), 0.022, 0.016, 5)
    rama(b, (-0.98, 0, 1.36), (-1.03, 0, 0.78), 0.035, 0.025, 6)
    esfera(n, -1.03, 0, 0.7, 0.07, 2, esc=(1.0, 1.0, 1.7))
    caja(mat('collar', 0x6a3a1e, 0.6), 0.95, 0, 1.0, 0.06, 0.5, 0.06, inclina=0.0)
    cil(mat('cencerro', 0xd6a024, 0.3), 0.97, 0, 0.78, 0.075, 0.15, 10, r2=0.05)

def vaca_pata():
    """Una pata de la vaca: muslo, rodilla, caña, menudillo y la pezuña."""
    b = pelo('pelo_vaca', 0xf6f4ee, 0xe9e5dc)
    rama(b, (0, 0, 0.05), (0.02, 0, -0.46), 0.13, 0.08, 10)
    esfera(b, 0.02, 0, -0.46, 0.078, 2)
    rama(b, (0.02, 0, -0.46), (0, 0, -0.82), 0.062, 0.052, 10)
    esfera(b, 0, 0, -0.83, 0.06, 2)
    cil(pezuna(), 0, 0, -0.95, 0.075, 0.12, 12, r2=0.06)
    caja(mat('raja_pezuna', 0x111111, 0.6), 0.04, 0, -0.95, 0.06, 0.012, 0.1)

# ---------------------------------------------------------------- el cerdo
def cerdo():
    """El cerdo rosa: cuerpo redondo, papada, morro con su disco y fosas,
    orejas caídas hacia delante, rabito rizado y algo de barro. Sin patas."""
    p = pelo('piel_cerdo', 0xf4a9b2, 0xeb9ca6)
    # (de una pieza: con varias bolas, el contorno marcaba las uniones como rayas)
    esfera(p, 0, 0, 0.54, 0.38, 4, esc=(1.6, 0.98, 0.9))
    esfera(p, 0.6, 0, 0.6, 0.23, 3, esc=(1.0, 1.0, 0.95))                 # la cabeza
    esfera(p, 0.6, 0, 0.47, 0.16, 2, esc=(1.1, 1.2, 0.7))                 # papada
    morro = mat('morro_cerdo', 0xe8838f, 0.5)
    cil(p, 0.74, 0, 0.56, 0.1, 0.1, 16, r2=0.11, eje='X')
    cil(morro, 0.81, 0, 0.56, 0.11, 0.03, 16, eje='X')
    for s in (-1, 1):
        esfera(mat('fosa_cerdo', 0x7a2f40, 0.6), 0.83, s * 0.04, 0.56, 0.022, 1)
        ojo(0.74, s * 0.12, 0.7, 0.03, s)
        o = esfera(p, 0.64, s * 0.14, 0.82, 0.1, 2, esc=(1.3, 0.85, 0.28))  # orejas caídas
        girar(o, rx=s * 0.4, ry=0.75)
    bpy.ops.mesh.primitive_torus_add(major_radius=0.06, minor_radius=0.016, location=(-0.6, 0, 0.66),
                                     rotation=(math.pi / 2, 0, 0))
    from comun import _poner
    _poner(bpy.context.object, p)                                         # el rabito
    barro = mat('barro', 0x7a5a3a, 0.9)
    esfera(barro, -0.18, -0.33, 0.42, 0.13, 2, esc=(1.5, 0.25, 1))
    esfera(barro, 0.25, 0.33, 0.36, 0.1, 2, esc=(1.4, 0.25, 0.8))

def cerdo_pata():
    p = pelo('piel_cerdo', 0xf4a9b2, 0xeb9ca6)
    rama(p, (0, 0, 0.04), (0, 0, -0.27), 0.085, 0.058, 10)
    cil(mat('pezuna_cerdo', 0x6a4848, 0.6), 0, 0, -0.38, 0.06, 0.11, 10, r2=0.055)
    caja(mat('raja_pezuna', 0x111111, 0.6), 0.035, 0, -0.38, 0.05, 0.01, 0.09)

# ---------------------------------------------------------------- el ciervo
def ciervo():
    """Ciervo de cola blanca: esbelto, tripa y garganta blancas, orejas grandes,
    hocico negro, astas con puntas y la cola blanca. Sin patas."""
    c = pelo('pelo_ciervo', 0xa8743a, 0x9a6832)
    b = pelo('pelo_ciervo_bl', 0xf2ece0, 0xe6dfd0)
    esfera(c, 0, 0, 1.08, 0.33, 3, esc=(1.65, 0.74, 0.8))
    esfera(c, 0.36, 0, 1.12, 0.26, 3)                                     # el pecho
    esfera(c, -0.36, 0, 1.12, 0.25, 3)
    esfera(b, 0.04, 0, 0.92, 0.22, 2, esc=(1.55, 0.7, 0.42))              # la tripa
    rama(c, (0.42, 0, 1.2), (0.64, 0, 1.56), 0.12, 0.08, 10)              # el cuello
    esfera(b, 0.6, 0, 1.4, 0.07, 2, esc=(0.7, 0.8, 1.4))                  # la garganta
    esfera(c, 0.73, 0, 1.62, 0.11, 3, esc=(1.5, 0.82, 0.88))
    esfera(c, 0.87, 0, 1.58, 0.065, 2, esc=(1.2, 0.9, 0.85))              # el morro
    esfera(negro(), 0.93, 0, 1.59, 0.03, 1)
    esfera(b, 0.88, 0, 1.54, 0.04, 1, esc=(1.2, 1.3, 0.6))
    cuerno = mat('cuerno_ciervo', 0xe2d5b6, 0.5)
    for s in (-1, 1):
        ojo(0.78, s * 0.075, 1.67, 0.022, s)
        o = esfera(c, 0.66, s * 0.13, 1.74, 0.07, 2, esc=(0.45, 1.6, 1.0))
        girar(o, rx=s * -0.35)
        # el asta: va hacia atrás y fuera, se curva hacia delante y echa puntas hacia arriba
        p = [(0.69, s * 0.05, 1.72), (0.64, s * 0.19, 1.86), (0.72, s * 0.24, 1.98), (0.86, s * 0.17, 2.03)]
        for a, bb in zip(p, p[1:]):
            rama(cuerno, a, bb, 0.022, 0.017, 6)
        for q in p[1:]:
            rama(cuerno, q, (q[0] + 0.02, q[1], q[2] + 0.13), 0.014, 0.006, 5)
    esfera(c, -0.54, 0, 1.2, 0.08, 2, esc=(0.8, 1.0, 1.3))                # la cola
    esfera(b, -0.57, 0, 1.15, 0.065, 2, esc=(0.6, 0.9, 1.3))

def ciervo_pata():
    c = pelo('pelo_ciervo', 0xa8743a, 0x9a6832)
    rama(c, (0, 0, 0.04), (0.03, 0, -0.38), 0.085, 0.048, 10)
    esfera(c, 0.03, 0, -0.38, 0.045, 2)
    rama(c, (0.03, 0, -0.38), (0, 0, -0.79), 0.034, 0.028, 8)
    cil(negro(), 0, 0, -0.85, 0.04, 0.07, 10, r2=0.032)

# ---------------------------------------------------------------- el alce
def alce():
    """El alce: enorme, marrón oscuro, joroba en los hombros, cabeza larga
    con el morro abultado, la «campanilla» bajo la barbilla y las astas en
    pala con puntas. Sin patas (que son largas y más claras)."""
    c = pelo('pelo_alce', 0x4a3424, 0x3e2b1e)
    o_ = pelo('pelo_alce_osc', 0x2e2018, 0x281b14)
    esfera(c, 0, 0, 1.62, 0.6, 3, esc=(1.55, 0.84, 0.82))
    esfera(c, 0.55, 0, 1.86, 0.55, 3, esc=(1.0, 0.88, 1.0))              # la joroba
    esfera(c, -0.6, 0, 1.55, 0.47, 3, esc=(1.0, 1.0, 0.95))
    esfera(o_, 0.45, 0, 2.3, 0.3, 2, esc=(1.6, 0.6, 0.45))                # crin oscura del lomo
    rama(c, (0.9, 0, 1.92), (1.2, 0, 1.94), 0.33, 0.26, 14)               # el cuello
    esfera(c, 1.48, 0, 1.8, 0.22, 3, esc=(1.9, 0.82, 1.0))                # la cabeza
    esfera(o_, 1.84, 0, 1.66, 0.19, 3, esc=(1.2, 0.95, 0.92))             # el morro abultado
    for s in (-1, 1):
        esfera(mat('fosa_alce', 0x120c08, 0.6), 2.03, s * 0.075, 1.62, 0.03, 1, esc=(1, 1, 1.5))
        ojo(1.46, s * 0.17, 1.9, 0.032, s)
        o = esfera(c, 1.32, s * 0.22, 2.0, 0.1, 2, esc=(0.5, 1.5, 0.8))
        girar(o, rx=s * -0.3)
    rama(o_, (1.42, 0, 1.6), (1.44, 0, 1.28), 0.07, 0.045, 8)             # la campanilla
    esfera(o_, 1.44, 0, 1.26, 0.055, 1, esc=(1, 1, 1.4))
    rama(mat('boca_alce', 0x150d08, 0.6), (1.94, -0.11, 1.54), (1.94, 0.11, 1.54), 0.012, 0.012, 5)
    # las astas en pala: un tallo, la pala y las puntas por el borde
    astas = mat('astas_alce', 0xd6c29a, 0.55)
    for s in (-1, 1):
        rama(astas, (1.38, s * 0.12, 2.05), (1.3, s * 0.4, 2.15), 0.05, 0.045, 8)
        o = esfera(astas, 1.26, s * 0.64, 2.26, 0.28, 3, esc=(0.8, 1.0, 0.16))
        girar(o, rx=s * 0.35)
        for k in range(6):
            a = math.radians(-60 + k * 27)
            px, py, pz = 1.26 + 0.24 * math.sin(a), s * (0.64 + 0.21 * math.cos(a)), 2.26 + 0.08 * math.cos(a)
            rama(astas, (px, py, pz), (px + 0.07 * math.sin(a), py + s * 0.08 * math.cos(a), pz + 0.16), 0.035, 0.01, 6)
    esfera(c, -1.02, 0, 1.72, 0.07, 2, esc=(0.8, 1.0, 1.3))               # la cola

def alce_pata():
    c = pelo('pelo_alce_pata', 0x8a7864, 0x7a6a58)
    a = pelo('pelo_alce', 0x4a3424, 0x3e2b1e)
    rama(a, (0, 0, 0.08), (0.03, 0, -0.6), 0.16, 0.09, 10)
    esfera(c, 0.03, 0, -0.6, 0.085, 2)
    rama(c, (0.03, 0, -0.6), (0, 0, -1.12), 0.07, 0.058, 10)
    esfera(c, 0, 0, -1.13, 0.068, 2)
    cil(negro(), 0, 0, -1.25, 0.085, 0.12, 12, r2=0.07)
    caja(mat('raja_pezuna', 0x111111, 0.6), 0.05, 0, -1.25, 0.07, 0.012, 0.11)

# ---------------------------------------------------------------- los pavos
PAVOS = ((0.15, -0.3), (-0.2, 0.32))

def pavos():
    """Dos pavos de granja escapados: cuerpo de plumas oscuras con reflejos,
    la cola en abanico con las puntas claras, cabeza azul con la carúncula
    roja y el pico. Sin patas (pavo_pata)."""
    pl = pelo('plumas_pavo', 0x5a3a24, 0x4a2e1c)
    for x, y in PAVOS:
        esfera(pl, x, y, 0.47, 0.24, 3, esc=(1.25, 0.95, 1.0))
        esfera(pl, x + 0.18, y, 0.5, 0.15, 2)                             # el pecho
        # la cola en abanico: medio disco y encima las plumas con la punta clara
        esfera(mat('pluma6a4428', 0x6a4428, 0.6), x - 0.29, y, 0.42, 0.5, 3, esc=(0.08, 1.0, 0.92), mitad=True)
        for k in range(11):
            a = (k - 5) * 0.27
            for r, lar, c in ((0.3, 0.38, 0x5a3a22), (0.5, 0.08, 0xd8c09a)):
                cy, cz = y + math.sin(a) * r, 0.42 + math.cos(a) * r
                o = caja(mat(f'pluma{c:06x}', c, 0.6), x - 0.25, cy, cz - lar / 2, 0.03, 0.14, lar)
                o.location = (x - 0.25, cy, cz)
                o.rotation_euler = (-a, 0, 0)
        for s in (-1, 1):
            esfera(pl, x - 0.02, y + s * 0.2, 0.5, 0.12, 2, esc=(1.4, 0.35, 0.8))   # las alas
        rama(mat('cuello_pavo', 0x8a6a8a, 0.5), (x + 0.22, y, 0.58), (x + 0.3, y, 0.76), 0.055, 0.04, 8)
        esfera(mat('cabeza_pavo', 0x7a9ad8, 0.45), x + 0.32, y, 0.8, 0.065, 2)
        rama(mat('moco_pavo', 0xd8202a, 0.5), (x + 0.37, y, 0.82), (x + 0.38, y, 0.68), 0.022, 0.016, 6)
        esfera(mat('moco_pavo', 0xd8202a, 0.5), x + 0.3, y, 0.7, 0.04, 1)
        cil(mat('pico_pavo', 0xe8c060, 0.4), x + 0.38, y, 0.8, 0.018, 0.06, 6, r2=0.005, eje='X')
        for s in (-1, 1):
            ojo(x + 0.35, y + s * 0.045, 0.83, 0.014, s)

def pavo_pata():
    m = mat('pata_pavo', 0xd89a48, 0.5)
    rama(m, (0, 0, 0.02), (0.02, 0, -0.24), 0.025, 0.018, 6)
    for a in (-0.5, 0, 0.5):
        rama(m, (0.02, 0, -0.24), (0.02 + 0.08 * math.cos(a), 0.08 * math.sin(a), -0.25), 0.01, 0.006, 4)

# ---------------------------------------------------------------- caballos
def caballo_pata():
    """Pata del caballo blanco de Central Park (coche de caballos)."""
    b = pelo('pelo_caballo_bl', 0xf1eee8, 0xe4e0d8)
    rama(b, (0, 0, 0.05), (0, 0.02, -0.42), 0.11, 0.065, 10)
    esfera(b, 0, 0.02, -0.42, 0.06, 2)
    rama(b, (0, 0.02, -0.42), (0, 0, -0.82), 0.045, 0.04, 8)
    esfera(b, 0, 0, -0.83, 0.052, 2)
    cil(negro(), 0, 0, -0.95, 0.062, 0.1, 12, r2=0.055)

def clydesdale_pata():
    """Pata del Clydesdale: marrón arriba, blanca abajo y el pelo largo de los
    cascos (las «plumas» de esta raza)."""
    m = pelo('pelo_clyde', 0x5a3420, 0x4e2c1a)
    b = pelo('pelo_caballo_bl', 0xf1eee8, 0xe4e0d8)
    rama(m, (0, 0, 0.06), (0, 0.02, -0.56), 0.17, 0.1, 10)
    esfera(m, 0, 0.02, -0.56, 0.09, 2)
    rama(b, (0, 0.02, -0.56), (0, 0, -1.0), 0.075, 0.07, 10)
    esfera(b, 0, 0, -1.07, 0.13, 2, esc=(1.0, 1.0, 1.1))                  # las plumas
    cil(negro(), 0, 0, -1.25, 0.1, 0.11, 12, r2=0.09)

# ---------------------------------------------------------------- micrófono
def microfono():
    """Micrófono de mano de verdad: rejilla de malla de metal oscuro, el anillo
    cromado, el mango negro mate que se estrecha y el conector de abajo.
    Centrado en el origen (el juego lo hace girar en el aire)."""
    rejilla = mat_bloques('rejilla_mic', 0x6f747b, 0x2a2d32, ancho=0.028, alto=0.028, grosor=0.006,
                          desfase=0.0, variacion=1.0)
    cromo = mat('cromo_mic', 0xc9ced6, 0.12)
    negro_m = mat('mango_mic', 0x1a1b1f, 0.55)
    esfera(rejilla, 0, 0, 0.26, 0.15, 3)
    cil(rejilla, 0, 0, 0.12, 0.13, 0.14, 24, r2=0.15)
    cil(cromo, 0, 0, 0.09, 0.135, 0.05, 24)
    cil(negro_m, 0, 0, -0.33, 0.055, 0.42, 20, r2=0.085)
    cil(mat('logo_mic', 0x8d939b, 0.3), 0, 0, -0.02, 0.075, 0.025, 20)
    cil(cromo, 0, 0, -0.37, 0.05, 0.04, 16)
    cil(mat('conector_mic', 0x0e0f11, 0.5), 0, 0, -0.39, 0.035, 0.02, 12)


PIEZAS = {
    'vaca':            (vaca,            'obstaculos', dict(lado=512, bisel=0.0)),
    'vaca_pata':       (vaca_pata,       'obstaculos', dict(lado=128, bisel=0.0, suelo=False)),
    'cerdo':           (cerdo,           'obstaculos', dict(lado=256, bisel=0.0)),
    'cerdo_pata':      (cerdo_pata,      'obstaculos', dict(lado=128, bisel=0.0, suelo=False)),
    'ciervo':          (ciervo,          'obstaculos', dict(lado=512, bisel=0.0)),
    'ciervo_pata':     (ciervo_pata,     'obstaculos', dict(lado=128, bisel=0.0, suelo=False)),
    'alce':            (alce,            'obstaculos', dict(lado=512, bisel=0.0)),
    'alce_pata':       (alce_pata,       'obstaculos', dict(lado=128, bisel=0.0, suelo=False)),
    'pavos':           (pavos,           'obstaculos', dict(lado=512, bisel=0.0)),
    'pavo_pata':       (pavo_pata,       'obstaculos', dict(lado=64, bisel=0.0, suelo=False)),
    'caballo_pata':    (caballo_pata,    'obstaculos', dict(lado=128, bisel=0.0, suelo=False)),
    'clydesdale_pata': (clydesdale_pata, 'obstaculos', dict(lado=128, bisel=0.0, suelo=False)),
    'microfono':       (microfono,       'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
}

correr(PIEZAS)
