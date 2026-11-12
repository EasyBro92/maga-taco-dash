# Nivel 14: Monte Rushmore, Dakota del Sur (12/11/2026).
#
#   blender -b -P blender/rushmore.py -- [pieza ...] [--rapido]
#
# Isidro (12/11): «sigue creando mapas y que se sientan muy diferentes, con
# dinámicas diferentes». Historia: «Quieres tu cara en la montaña, junto a los
# cuatro presidentes. El escultor dice que no… de momento».
#   Primero Rapid City, «la ciudad de los presidentes» (estatuas de bronce en
#   cada esquina): el hotel Alex Johnson, el dinosaurio verde del Dinosaur
#   Park en su colina y el cartel de Wall Drug. Luego las Black Hills por la
#   Iron Mountain Road: pinares, agujas de granito y túneles de roca. Al final
#   la Avenida de las Banderas y el monte con las cuatro caras… y el andamio
#   donde el escultor ha pintado (de mala gana) el contorno de la quinta.
# Obstáculos (carpeta obstaculos): el bisonte (embiste si te pones en su
# carril), el perrito de la pradera que asoma de su madriguera, la roca que
# cae de la montaña y la pancarta del sindicato de escultores.

import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import *
from comun import _poner

def granito():   return mat('granito_rush', 0xa59b8f, 0.85)
def granito_c(): return mat('granito_claro_rush', 0xc2b8aa, 0.8)
def granito_o(): return mat('granito_oscuro_rush', 0x756c62, 0.9)
def grieta():    return mat('grieta_rush', 0x5e584f, 0.95)
def pino():      return mat('pino_rush', 0x2b4a2e, 0.85)
def pino_c():    return mat('pino_claro_rush', 0x3c5e36, 0.85)
def tronco():    return mat('tronco_rush', 0x6a4a32, 0.9)
def hierba():    return mat('hierba_rush', 0x7a8a4a, 0.95)
def tierra():    return mat('tierra_rush', 0x9a7a54, 0.95)
def bronce():    return mat('bronce_rush', 0x7a5a32, 0.35)
def blanco():    return mat('blanco_rush', 0xf6f4ee, 0.5)
def negro():     return mat('negro_rush', 0x1b1c20, 0.4)
def rojo():      return mat('rojo_rush', 0xc8282c, 0.45)
def azul():      return mat('azul_rush', 0x1f3a7a, 0.45)
def madera():    return mat('madera_rush', 0x8a5a32, 0.75)
def acero():     return mat('acero_rush', 0xb8bec4, 0.3)
def naranja():   return mat('naranja_rush', 0xf28c1c, 0.5)

def pino_ponderosa(x, y, z=0.0, h=12.0, claro=False):
    """El pino de las Black Hills: tronco alto y copa en pisos, oscura."""
    cil(tronco(), x, y, z, 0.3 * h / 12, h * 0.45, 6)
    m = pino_c() if claro else pino()
    for k in range(4):
        zz = z + h * (0.3 + k * 0.17)
        r = h * (0.22 - k * 0.04)
        cil(m, x, y, zz, r, h * 0.26, 8, r2=r * 0.25)
    cil(m, x, y, z + h * 0.95, h * 0.05, h * 0.12, 6, r2=0.02)

def roca(x, y, z, r, esc=(1, 1, 1), m=None):
    """Una roca de granito: tres bultos juntos."""
    m = m or granito()
    esfera(m, x, y, z, r, 2, esc=esc)
    esfera(m, x + r * 0.5, y - r * 0.2, z + r * 0.1, r * 0.7, 2, esc=esc)
    esfera(granito_o(), x - r * 0.45, y + r * 0.1, z - r * 0.1, r * 0.6, 2, esc=esc)

def letras_verticales(m, cadena, x, y, z_arriba, tam, paso):
    for i, ch in enumerate(cadena):
        if ch != ' ':
            texto(m, ch, x, y, z_arriba - i * paso, tam=tam, prof=0.06)


# ================================================================ Rapid City
def hotel_alex_johnson():
    """El hotel Alex Johnson (1928): nueve plantas de ladrillo con las dos de
    arriba de entramado blanco y negro y tejados a dos aguas, y su letrero
    rojo vertical en la esquina."""
    lad = mat_ventanas('ladrillo_aj', 0x2c3440, 0x8a4a36, paso_x=1.6, paso_z=3.2, hueco_x=0.8, hueco_z=1.7, variacion=1.06)
    Y = 11
    caja(mat_bloques('piedra_aj', 0xcfc2a8, 0xa89a80, ancho=1.2, alto=0.6), 0, Y, 0, 30, 20, 4.5)
    caja(lad, 0, Y, 4.5, 30, 20, 22)
    # Las dos plantas de entramado.
    caja(blanco(), 0, Y, 26.5, 30, 20, 6)
    vigas = mat('vigas_aj', 0x3a2618, 0.7)
    for k in range(11):
        x = -14 + k * 2.8
        caja(vigas, x, Y - 10.05, 26.5, 0.35, 0.1, 6)
    for z in (26.6, 29.4, 32.3):
        caja(vigas, 0, Y - 10.05, z, 30, 0.1, 0.3)
    for k in range(5):
        x = -12 + k * 6
        o = caja(vigas, x, Y - 10.06, 27.2, 0.3, 0.1, 4.2); o.rotation_euler = (0, 0.55, 0)
    tejado(mat('tejado_aj', 0x5a3a2a, 0.8), 0, Y - 10, Y + 10, 32.5, 31, 7, vuelo=0.6)
    for x in (-9, 9):
        hastial(blanco(), x, Y - 10.5, Y - 4, 32.5, 7, 5)
    # El letrero rojo vertical en la esquina y HOTEL arriba.
    caja(rojo(), 13.5, -0.8, 9, 1.4, 1.2, 16)
    letras_verticales(mat('neon_aj', 0xffe9b0, 0.3), 'ALEX', 13.5, -1.45, 23, 1.3, 1.9)
    letras_verticales(mat('neon_aj', 0xffe9b0, 0.3), 'JOHNSON', 13.5, -1.45, 15.4, 1.0, 1.0)
    texto(rojo(), 'HOTEL ALEX JOHNSON', 0, Y - 10.1, 5.4, tam=1.1, prof=0.08)
    caja(mat('marquesina_aj', 0x2a3a2a, 0.6), 0, -1.2, 3.6, 10, 2.4, 0.4)
    caja(mat('puerta_aj', 0x3a2a1e, 0.5), 0, 0.95, 0, 4, 0.1, 3.5)

def dino_park():
    """El Dinosaur Park (1936): en lo alto de la colina, el brontosaurio verde
    con manchas blancas que se ve desde toda la ciudad."""
    # La colina, con hierba y rocas.
    esfera(hierba(), 0, 18, -6, 22, 3, esc=(1.1, 0.8, 0.55))
    for (x, y, r) in ((-12, 6, 2.2), (10, 8, 1.8), (-4, 4, 1.4), (14, 14, 2.6)):
        roca(x, y, 1.0, r, m=granito_o())
    for (x, y) in ((-16, 14), (17, 20), (-8, 24), (6, 26)):
        pino_ponderosa(x, y, 2.0, 9)
    verde = mat('dino_verde', 0x5aa64a, 0.5)
    manchas = mat('dino_manchas', 0xf2f2e6, 0.5)
    Z = 7.5
    # Cuerpo, patas, cuello largo hacia la calle y la cola.
    esfera(verde, 0, 16, Z + 4, 5, 3, esc=(0.75, 1.3, 0.75))
    for (x, y) in ((-2.4, 13), (2.4, 13), (-2.4, 19.5), (2.4, 19.5)):
        cil(verde, x, y, Z - 0.3, 1.0, 4.5, 10, r2=0.9)
    cuello = [(0, 12, Z + 6), (0, 9.5, Z + 9), (0, 7.5, Z + 12.5), (0, 6.5, Z + 15)]
    for a, b in zip(cuello, cuello[1:]):
        rama(verde, a, b, 1.6, 1.15, 10)
    esfera(verde, 0, 5.8, Z + 15.6, 1.4, 2, esc=(0.9, 1.6, 0.8))
    for s in (-1, 1):
        esfera(negro(), s * 0.75, 4.6, Z + 16.0, 0.22, 1)
    cola = [(0, 20, Z + 5), (0, 24, Z + 4), (0, 28, Z + 2.5), (0, 31, Z + 1.5)]
    for a, b in zip(cola, cola[1:]):
        rama(verde, a, b, 1.5 - cola.index(a) * 0.4, 1.1 - cola.index(a) * 0.35, 8)
    for (x, y, z) in ((3.2, 15, Z + 5), (-3.2, 17, Z + 4.5), (3, 19, Z + 3.5), (-2.8, 13.5, Z + 3.2), (0, 16, Z + 7.6)):
        esfera(manchas, x, y, z, 0.7, 1, esc=(0.4, 1, 1))
    # El letrero al pie de la colina.
    for x in (-3, 3):
        cil(madera(), x, 1, 0, 0.15, 2.6, 6)
    caja(mat('letrero_dino', 0x2a4a2e, 0.6), 0, 1, 1.4, 7, 0.2, 1.3)
    texto(mat('letras_dino', 0xf6e6b0, 0.5), 'DINOSAUR PARK', 0, 0.85, 2.0, tam=0.6, prof=0.04)

def wall_drug():
    """El cartel de Wall Drug, el más famoso de las carreteras de Dakota del
    Sur: amarillo, enorme, sobre postes de madera."""
    for x in (-8, -2.7, 2.7, 8):
        cil(madera(), x, 1.5, 0, 0.25, 9, 6)
        o = cil(madera(), x, 3.2, 0, 0.18, 6, 6); o.rotation_euler = (-0.5, 0, 0)
    caja(mat('cartel_wall', 0xf2c230, 0.6), 0, 1.0, 4, 20, 0.3, 7)
    caja(rojo(), 0, 0.84, 4.15, 19.6, 0.05, 0.4)
    caja(rojo(), 0, 0.84, 10.45, 19.6, 0.05, 0.4)
    texto(rojo(), 'WALL DRUG', 0, 0.8, 8.4, tam=2.4, prof=0.1)
    texto(mat('letras_wall', 0x1f3a7a, 0.5), 'FREE ICE WATER', 0, 0.8, 6.0, tam=1.2, prof=0.08)
    texto(mat('letras_wall', 0x1f3a7a, 0.5), '5¢ COFFEE · 2 MILES', 0, 0.8, 4.7, tam=0.8, prof=0.06)
    pino_ponderosa(-12, 6, 0, 10); pino_ponderosa(12, 7, 0, 11)

def estatua_bronce():
    """Una de las estatuas de presidentes de Rapid City, en su esquina: el
    presidente de bronce, de traje, con el sombrero en la mano, sobre su
    pedestal de granito con la placa."""
    caja(granito_c(), 0, 0, 0, 1.2, 1.2, 1.0)
    caja(granito(), 0, 0, 1.0, 1.0, 1.0, 0.12)
    caja(bronce(), 0, -0.61, 0.35, 0.6, 0.02, 0.35)
    b = bronce()
    for s in (-1, 1):
        cil(b, s * 0.13, 0, 1.12, 0.11, 0.8, 8, r2=0.1)
    cil(b, 0, 0, 1.85, 0.27, 0.75, 10, r2=0.22)
    esfera(b, 0, 0, 2.78, 0.16, 2, esc=(1, 1, 1.15))
    rama(b, (0.24, 0, 2.5), (0.36, -0.15, 1.95), 0.07, 0.06, 6)
    rama(b, (-0.24, 0, 2.5), (-0.3, -0.25, 2.1), 0.07, 0.06, 6)
    cil(b, -0.3, -0.32, 2.1, 0.16, 0.05, 10)            # el sombrero en la mano
    cil(b, -0.3, -0.32, 2.15, 0.09, 0.14, 10)

# ================================================================ Black Hills
def pinar():
    """Un trozo de bosque de las Black Hills: pinos ponderosa, rocas y hierba."""
    caja(hierba(), 0, 10, -0.05, 30, 20, 0.08)
    import random
    r = random.Random(14)
    for k in range(9):
        x, y = -13 + k * 3.2 + r.uniform(-1, 1), 4 + r.uniform(0, 12)
        pino_ponderosa(x, y, 0, r.uniform(10, 16), claro=k % 3 == 0)
    for k in range(3):
        roca(-10 + k * 10 + r.uniform(-2, 2), 2.5 + r.uniform(0, 3), 0.4, r.uniform(0.8, 1.6))

def agujas_granito():
    """Las «Needles»: agujas de granito altísimas entre los pinos."""
    caja(hierba(), 0, 10, -0.05, 26, 20, 0.08)
    import random
    r = random.Random(7)
    for k in range(7):
        x, y = -10 + k * 3.4 + r.uniform(-0.8, 0.8), 6 + r.uniform(0, 8)
        h = r.uniform(12, 26)
        cil(granito(), x, y, 0, r.uniform(1.4, 2.4), h, 9, r2=r.uniform(0.3, 0.8))
        esfera(granito_o(), x, y, h * 0.4, 1.6, 2, esc=(1, 1, 2.2))
        cil(grieta(), x + 0.6, y - 1.2, h * 0.2, 0.15, h * 0.5, 4)
    for k in range(4):
        pino_ponderosa(-11 + k * 7, 3 + (k % 2) * 3, 0, 9, claro=True)

def tunel_roca():
    """Un túnel de la Iron Mountain Road: la carretera pasa por debajo de la
    roca por un hueco justo (de un solo carril en la vida real; aquí caben los
    tres). Cruza la calle: el origen en el centro y la calle a lo largo de y."""
    # Las masas de roca a los lados y encima, sin tapar el hueco (|x| < 5.2, z < 7.2).
    for s in (-1, 1):
        esfera(granito(), s * 13.5, 0, 6, 8.3, 3, esc=(1, 0.95, 1.2))
        esfera(granito_o(), s * 18, 2, 3, 6, 2, esc=(1, 1, 1))
        caja(granito_o(), s * 6.0, 0, 0, 1.6, 13, 7.6)
    esfera(granito(), 0, 0, 13.5, 16, 3, esc=(1, 0.42, 0.42))
    esfera(granito_c(), -4, -2, 15, 8, 2, esc=(1, 0.6, 0.5))
    caja(grieta(), 0, 0, 7.2, 10.4, 13, 0.6)
    # El arco de piedra de la entrada (los dos lados).
    for sy in (-1, 1):
        for k in range(9):
            a = math.pi * k / 8
            x, z = math.cos(a) * 5.2, 4.6 + math.sin(a) * 2.6
            o = caja(granito_c(), x, sy * 6.6, z - 0.4, 1.4, 0.8, 0.9); o.rotation_euler = (0, -a + math.pi / 2, 0)
    for s in (-1, 1):
        for k in range(3):
            pino_ponderosa(s * (14 + k * 3), -4 + k * 4, 9 + k, 7)
    texto(mat('letras_tunel', 0xe8e2d4, 0.6), 'IRON MOUNTAIN ROAD', 0, -6.95, 8.4, tam=0.9, prof=0.06)

def avenida_banderas():
    """La Avenida de las Banderas, a la entrada del monumento: columnas de
    granito con la bandera de cada estado ondeando."""
    caja(granito_c(), 0, 3, 0, 30, 6, 0.3)
    colores = [(0x1f3a7a, 0xf2c230), (0xc8282c, 0xf6f4ee), (0x2a6a3a, 0xf6f4ee), (0x1f3a7a, 0xf6f4ee),
               (0x8a2a2a, 0xf2c230), (0x1f5aa8, 0xc8282c)]
    for k in range(6):
        x = -12.5 + k * 5
        caja(granito(), x, 1.5, 0.3, 1.4, 1.4, 4.2)
        caja(granito_c(), x, 1.5, 4.5, 1.6, 1.6, 0.25)
        cil(acero(), x + 0.5, 1.5, 4.75, 0.05, 6, 6)
        c1, c2 = colores[k]
        caja(mat('bandera_%x' % c1, c1, 0.6), x + 1.6, 1.5, 9.2, 2.2, 0.04, 1.4)
        caja(mat('bandera_%x' % c2, c2, 0.6), x + 1.6, 1.47, 9.6, 1.0, 0.05, 0.5)
    pino_ponderosa(-15, 9, 0, 13); pino_ponderosa(15, 10, 0, 12)

# ================================================================ el monte
def cara(x, y, z, s, quien):
    """Una cara tallada en la roca, mirando a -y. `s`: alto de la cabeza."""
    c, o = granito_c(), granito_o()
    esfera(c, x, y, z, s * 0.5, 3, esc=(0.78, 0.6, 1.0))              # la cabeza
    esfera(c, x, y - s * 0.1, z - s * 0.32, s * 0.3, 2, esc=(0.95, 0.75, 0.8))   # la mandíbula
    esfera(c, x, y - s * 0.24, z + s * 0.1, s * 0.34, 2, esc=(0.95, 0.4, 0.22))  # la frente y las cejas
    for sx in (-1, 1):                                                 # los ojos (cuencas en sombra)
        esfera(o, x + sx * s * 0.15, y - s * 0.27, z + s * 0.01, s * 0.07, 2, esc=(1.3, 0.5, 0.8))
        esfera(c, x + sx * s * 0.42, y + s * 0.02, z, s * 0.09, 2, esc=(0.4, 0.8, 1.4))   # las orejas
    esfera(c, x, y - s * 0.36, z - s * 0.1, s * 0.07, 2, esc=(0.8, 1.6, 2.0))     # la nariz
    caja(o, x, y - s * 0.3, z - s * 0.27, s * 0.18, s * 0.06, s * 0.02)            # la boca
    if quien == 'washington':        # la peluca con los rulos a los lados
        esfera(c, x, y + s * 0.12, z + s * 0.3, s * 0.42, 2, esc=(0.95, 0.7, 0.55))
        for sx in (-1, 1):
            esfera(c, x + sx * s * 0.38, y + s * 0.05, z + s * 0.08, s * 0.1, 2, esc=(0.6, 1.4, 0.8))
    elif quien == 'jefferson':       # el pelo largo hacia atrás, la cabeza girada
        esfera(c, x + s * 0.05, y + s * 0.15, z + s * 0.25, s * 0.42, 2, esc=(1.0, 0.75, 0.6))
    elif quien == 'roosevelt':       # el bigote y las gafas
        caja(o, x, y - s * 0.34, z - s * 0.18, s * 0.26, s * 0.08, s * 0.06)
        for sx in (-1, 1):
            o2 = cil(o, x + sx * s * 0.15, y - s * 0.32, z + s * 0.01, s * 0.09, s * 0.02, 12, eje='Y')
        caja(o, x, y - s * 0.33, z + s * 0.03, s * 0.08, s * 0.02, s * 0.015)
    else:                            # Lincoln: la barba y las mejillas hundidas
        esfera(o, x, y - s * 0.12, z - s * 0.38, s * 0.26, 2, esc=(1.0, 0.75, 0.75))
        for sx in (-1, 1):
            esfera(o, x + sx * s * 0.2, y - s * 0.22, z - s * 0.12, s * 0.06, 2, esc=(0.6, 0.4, 1.4))

def monte_rushmore():
    """El monte Rushmore: la montaña de granito con Washington, Jefferson,
    Roosevelt y Lincoln, los pinos al pie y, a la derecha, el andamio del
    escultor y el contorno pintado de la quinta cara (con su tupé naranja)."""
    # La montaña.
    esfera(granito(), 0, 40, 18, 52, 3, esc=(1.35, 0.55, 0.85))
    esfera(granito_o(), -45, 48, 10, 36, 3, esc=(1, 0.6, 0.8))
    esfera(granito_o(), 52, 46, 12, 34, 3, esc=(1, 0.6, 0.85))
    esfera(granito(), 10, 30, 40, 30, 3, esc=(1.3, 0.5, 0.6))
    # Los picos de granito detrás y a los lados (las Black Hills).
    import random
    rp = random.Random(11)
    for k in range(11):
        x = -78 + k * 15 + rp.uniform(-4, 4)
        if -45 < x < 25:
            y = 52 + rp.uniform(0, 10)
        else:
            y = 30 + rp.uniform(0, 14)
        h = rp.uniform(34, 62)
        cil(granito_o() if k % 2 else granito(), x, y, 0, rp.uniform(9, 14), h, 9, r2=rp.uniform(2, 5))
    # La pared lisa donde están las caras y los derrubios de debajo.
    caja(granito_c(), -8, 16, 22, 70, 4, 36)
    for k in range(10):
        esfera(granito_o(), -40 + k * 8, 10, 4 + (k % 3), 5 + (k % 4), 2, esc=(1.2, 0.8, 0.6))
    S = 22
    for (x, quien, dz) in ((-36, 'washington', 0), (-17, 'jefferson', -1), (-3, 'roosevelt', -3), (16, 'lincoln', -1)):
        cara(x, 11, 41 + dz, S, quien)
    # El andamio del escultor y la quinta cara, solo pintada.
    tubo = acero()
    X0, X1, Z0, Z1 = 30, 50, 22, 56
    for k in range(6):
        x = X0 + k * (X1 - X0) / 5
        cil(tubo, x, 12, Z0, 0.18, Z1 - Z0, 6)
    for k in range(9):
        z = Z0 + k * (Z1 - Z0) / 8
        caja(tubo, (X0 + X1) / 2, 12, z, X1 - X0, 0.3, 0.3)
        caja(madera(), (X0 + X1) / 2, 11.2, z, X1 - X0, 1.6, 0.18)
    pintura = rojo()
    for k in range(24):                                          # el contorno de la cara
        a = math.tau * k / 24
        o = caja(pintura, 40 + math.cos(a) * 7, 13.9, 38 + math.sin(a) * 9, 1.8, 0.15, 0.6)
        o.rotation_euler = (0, -a, 0)
    for (x, z, r) in ((36, 47, 3.5), (40, 48.5, 4.2), (45, 47.5, 3.8), (48, 45, 2.6)):   # el tupé
        esfera(naranja(), x, 13.9, z, r, 2, esc=(1.2, 0.12, 0.7))
    texto(pintura, '¿TRUMP?', 40, 13.8, 26.5, tam=3.2, prof=0.12)
    # La grúa del escultor.
    cil(mat('grua', 0xf2c230, 0.5), 58, 18, 0, 0.6, 62, 4)
    o = caja(mat('grua', 0xf2c230, 0.5), 50, 18, 61, 24, 0.8, 0.8)
    cil(acero(), 42, 18, 46, 0.05, 15, 4)
    # Los pinos al pie y la terraza del mirador.
    import random
    r = random.Random(3)
    for k in range(26):
        x = -70 + k * 5.6 + r.uniform(-2, 2)
        pino_ponderosa(x, 6 + r.uniform(0, 8), r.uniform(0, 3), r.uniform(10, 16), claro=k % 4 == 0)
    caja(granito_c(), 0, -6, 0, 60, 8, 1.2)
    for k in range(12):
        caja(granito(), -27.5 + k * 5, -9.6, 1.2, 1.0, 0.6, 1.0)

# ================================================================ obstáculos
def bisonte():
    """El bisonte, mirando a -y (hacia ti): la joroba peluda, la cabeza baja
    con los cuernos y la barba, y el cuerpo marrón oscuro."""
    pelo = mat('bisonte_pelo', 0x6a4a2e, 0.95)
    oscuro = mat('bisonte_oscuro', 0x3a2a1e, 0.9)
    esfera(oscuro, 0, 0.5, 1.15, 0.95, 3, esc=(0.85, 1.25, 0.8))        # el cuerpo de atrás
    esfera(pelo, 0, -0.45, 1.35, 1.0, 3, esc=(0.95, 0.9, 1.0))          # la joroba
    esfera(pelo, 0, -1.05, 0.95, 0.62, 3, esc=(0.9, 0.9, 1.0))          # la cabeza baja
    esfera(pelo, 0, -1.25, 0.55, 0.32, 2, esc=(1.0, 0.8, 1.2))          # la barba
    esfera(negro(), 0, -1.55, 0.85, 0.22, 2, esc=(1.2, 0.7, 0.8))       # el morro
    for s in (-1, 1):
        esfera(negro(), s * 0.32, -1.5, 1.08, 0.07, 1)                  # los ojos
        rama(mat('cuerno', 0xe8e0cc, 0.4), (s * 0.45, -1.1, 1.3), (s * 0.75, -1.15, 1.55), 0.09, 0.05, 6)
        rama(mat('cuerno', 0xe8e0cc, 0.4), (s * 0.75, -1.15, 1.55), (s * 0.68, -1.25, 1.78), 0.05, 0.02, 5)
    for (x, y) in ((-0.42, -0.6), (0.42, -0.6), (-0.4, 0.95), (0.4, 0.95)):
        cil(oscuro, x, y, 0, 0.14, 0.75, 8, r2=0.17)
        cil(negro(), x, y, 0, 0.15, 0.1, 8)
    rama(oscuro, (0, 1.55, 1.3), (0, 1.75, 0.8), 0.06, 0.04, 5)          # la cola

def perrito_pradera():
    """El perrito de la pradera, de pie y alerta (el juego lo hace asomar y
    esconderse en su madriguera)."""
    piel = mat('perrito_piel', 0xc89a64, 0.85)
    tripa = mat('perrito_tripa', 0xead2a8, 0.85)
    esfera(piel, 0, 0, 0.45, 0.24, 3, esc=(0.8, 0.72, 1.7))
    esfera(tripa, 0, -0.13, 0.45, 0.16, 2, esc=(0.85, 0.5, 1.6))
    esfera(piel, 0, -0.05, 0.9, 0.12, 3, esc=(0.9, 1.25, 0.9))
    esfera(tripa, 0, -0.19, 0.86, 0.06, 2, esc=(1.1, 0.9, 0.7))           # el hocico
    esfera(negro(), 0, -0.25, 0.88, 0.025, 1)
    for s in (-1, 1):
        esfera(negro(), s * 0.06, -0.16, 0.95, 0.025, 1)
        esfera(piel, s * 0.09, 0.0, 1.0, 0.025, 1, esc=(1, 0.6, 1))
        esfera(piel, s * 0.07, -0.2, 0.58, 0.05, 1, esc=(0.8, 0.8, 1.3))   # las patitas juntas
    rama(piel, (0, 0.2, 0.2), (0, 0.38, 0.35), 0.06, 0.03, 5)

def madriguera():
    """La madriguera: un montículo de tierra con el agujero en medio (se pisa)."""
    esfera(tierra(), 0, 0, -0.05, 0.75, 2, esc=(1, 1, 0.32))
    cil(mat('agujero_rush', 0x2a1e14, 0.9), 0, 0, 0.12, 0.3, 0.05, 14)
    for k in range(5):
        a = k * math.tau / 5
        esfera(tierra(), math.cos(a) * 0.7, math.sin(a) * 0.7, 0, 0.12, 1)

def roca_caida():
    """La roca que cae de la montaña (se salta)."""
    esfera(granito(), 0, 0, 0.5, 0.6, 2, esc=(1.1, 0.95, 0.9))
    esfera(granito_o(), 0.3, 0.15, 0.62, 0.38, 2)
    esfera(granito_c(), -0.25, -0.2, 0.75, 0.3, 2)
    caja(grieta(), 0.05, -0.55, 0.35, 0.05, 0.05, 0.5)

def cartel_no_caras():
    """La pancarta del sindicato de escultores (agacharse): «NO MORE FACES!»
    entre dos mazas de picapedrero."""
    for x in (-1.25, 1.25):
        cil(madera(), x, 0, 0, 0.07, 2.75, 8)
        caja(granito_o(), x, 0, 2.7, 0.3, 0.3, 0.25)
    caja(mat('tela_cartel_rush', 0xf6f2e6, 0.7), 0, 0, 1.55, 2.4, 0.06, 1.05)
    texto(rojo(), 'NO MORE', 0, -0.04, 2.25, tam=0.3, prof=0.02)
    texto(rojo(), 'FACES!', 0, -0.04, 1.85, tam=0.3, prof=0.02)
    texto(mat('letras_cartel_rush', 0x3a3a3a, 0.5), 'SCULPTORS UNION', 0, -0.04, 1.6, tam=0.12, prof=0.01)

PIEZAS = {
    'hotel_alex_johnson': (hotel_alex_johnson, 'rushmore', dict(lado=1024, segmentos=1, min_bisel=1.0)),
    'dino_park':          (dino_park,          'rushmore', dict(lado=1024, bisel=0.0)),
    'wall_drug':          (wall_drug,          'rushmore', dict(lado=1024, bisel=0.0)),
    'estatua_bronce':     (estatua_bronce,     'rushmore', dict(lado=256, bisel=0.0)),
    'pinar':              (pinar,              'rushmore', dict(lado=512, bisel=0.0)),
    'agujas_granito':     (agujas_granito,     'rushmore', dict(lado=512, bisel=0.0)),
    'tunel_roca':         (tunel_roca,         'rushmore', dict(lado=1024, bisel=0.0, suelo=False)),
    'avenida_banderas':   (avenida_banderas,   'rushmore', dict(lado=512, bisel=0.0)),
    'monte_rushmore':     (monte_rushmore,     'rushmore', dict(lado=2048, bisel=0.0)),
    'bisonte':            (bisonte,            'obstaculos', dict(lado=256, bisel=0.0)),
    'perrito_pradera':    (perrito_pradera,    'obstaculos', dict(lado=256, bisel=0.0)),
    'madriguera':         (madriguera,         'obstaculos', dict(lado=256, bisel=0.0)),
    'roca_caida':         (roca_caida,         'obstaculos', dict(lado=256, bisel=0.0)),
    'cartel_no_caras':    (cartel_no_caras,    'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
}

correr(PIEZAS)
