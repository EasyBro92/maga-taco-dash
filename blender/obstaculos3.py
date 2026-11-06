# Obstáculos nuevos con movimiento (06/11/2026).
#
#   blender -b -P blender/obstaculos3.py -- [pieza ...] [--rapido]
#
# Isidro, jugando en Pennsylvania Avenue: «se hacen repetitivos los
# obstáculos, faltan más tipos y más dinamismo». Eligió cinco nuevos por
# ciudad y cuatro formas de moverse (las mueve el juego, world.js):
#   cambia   se pasa al carril de al lado (avisa con el intermitente)
#   cruza    viene de la acera, cruza la calle y se para en su carril
#   barrera  el brazo sube y baja despacio (va en una pieza aparte, _brazo)
#   bota     viene botando hacia ti
#
# Mismas reglas que obstaculos2.py: caben en un carril (x de -0.95 a 0.95),
# miran al jugador por -y (en el juego, +z) y el origen es el centro del
# carril a ras de suelo. Los vehículos empiezan en y = 0 y se alargan hacia +y.
# Lo que cruza la calle mira a +x (hacia donde anda).
#
#   Washington   micrófonos de la prensa (saltar) · barrera del control (sube y baja)
#                dron de la tele (agacharse) · furgoneta de las Fake News (cambia de carril)
#                turista en Segway (cruza)

import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import *

def blanco():  return mat('blanco', 0xffffff, 0.5)
def negro():   return mat('negro', 0x1d1f25, 0.4)
def gris():    return mat('gris', 0x9aa1aa, 0.5)
def rojo():    return mat('rojo', 0xe8303a, 0.45)
def azul():    return mat('azul', 0x2350c8, 0.45)
def amarillo(): return mat('amarillo', 0xffc21a, 0.4)
def cristal(): return mat('cristal', 0x3a6fb0, 0.15)
def neumatico(): return mat('neumatico', 0x1d1e21, 0.8)
def piloto():  return mat('piloto', 0xc0262c, 0.3)
def ambar():   return mat('ambar', 0xff9a1a, 0.25)
def rayas(nombre, c1, c2, n, x0, ancho, eje='X'):
    return mat_franjas(nombre, c1, c2, n, eje=eje, z0=x0, alto=ancho)

def rueda(x, y, r=0.3, ancho=0.22, z=None, eje='X'):
    z = r if z is None else z
    cil(neumatico(), x, y, z, r, ancho, 16, eje=eje)
    if eje == 'X':
        cil(mat('llanta', 0xd3d6da, 0.3), x + (0.12 if x > 0 else -0.12), y, z, r * 0.5, 0.02, 12, eje='X')
    else:
        cil(mat('llanta', 0xd3d6da, 0.3), x, y + (0.12 if y > 0 else -0.12), z, r * 0.5, 0.02, 12, eje='Y')

def texto_lado(m, cadena, x, y, z, tam, lado):
    """Letras en un costado (lado -1 mira a -x, 1 a +x)."""
    o = texto(m, cadena, 0, 0, 0, tam=tam, prof=0.02)
    o.rotation_euler = (math.pi / 2, 0, -lado * math.pi / 2)
    o.location = (x, y, z)


# ---------------------------------------------------------------- Washington
def microfonos():
    """Los micrófonos de la prensa en el suelo: pies de distinta altura, cada
    uno con su espuma de color y el cubo con el nombre de la cadena. Apuntan
    al jugador, como en una rueda de prensa."""
    metal = mat('metal_pie', 0x2a2d33, 0.35)
    cable = mat('cable_mic', 0x16171a, 0.6)
    # la tarima de la prensa: así se lee de lejos como algo que hay que saltar
    T = 0.3
    caja(mat('tarima', 0x2a2d36, 0.5), 0, 0.02, 0, 1.84, 0.62, T)
    caja(mat('borde_tarima', 0xffc21a, 0.4), 0, -0.3, T - 0.05, 1.86, 0.03, 0.05)
    texto(blanco(), 'PRESS', 0, -0.295, T * 0.45, tam=0.14, prof=0.012)
    cadenas = ((-0.72, 0.4, 0xe8303a, 'FN'), (-0.36, 0.52, 0x2350c8, 'TV'),
               (0.0, 0.46, 0xffc21a, '24'), (0.36, 0.54, 0x2fae5a, 'CNX'), (0.72, 0.42, 0x1d1f25, 'NEWS'))
    for i, (x, h, color, letras) in enumerate(cadenas):
        y = 0.05 * ((i % 2) * 2 - 1)
        h += T
        for k in range(3):                                              # el trípode
            a = k * 2 * math.pi / 3 + 0.4
            rama(metal, (x, y, T + 0.18), (x + math.cos(a) * 0.15, y + math.sin(a) * 0.15, T), 0.012, 0.012, 5)
        cil(metal, x, y, T + 0.16, 0.016, h - T - 0.16, 6)
        rama(metal, (x, y, h), (x, y - 0.18, h + 0.04), 0.012, 0.012, 5)  # la jirafa hacia el jugador
        cil(metal, x, y - 0.2, h + 0.04, 0.024, 0.13, 8, eje='Y')
        esfera(mat(f'espuma{color:06x}', color, 0.85), x, y - 0.3, h + 0.04, 0.065, 2, esc=(1, 1.25, 1))
        cubo = mat(f'cubo{color:06x}', color, 0.4)
        caja(cubo, x, y - 0.2, h - 0.05, 0.11, 0.11, 0.09)
        texto(blanco(), letras, x, y - 0.256, h - 0.005, tam=0.045 if len(letras) < 4 else 0.032, prof=0.006)
        rama(cable, (x, y, T + 0.17), (x + 0.1, y + 0.22, T + 0.01), 0.01, 0.01, 4)   # el cable por la tarima
    rama(cable, (-0.6, 0.26, T + 0.01), (0.84, 0.28, T + 0.01), 0.012, 0.012, 4)

def barrera_control():
    """El control del Servicio Secreto: el poste con su caja (el brazo, que sube
    y baja, es barrera_control_brazo) y la horquilla donde descansa al otro lado."""
    azul_osc = mat('azul_control', 0x1f2c4a, 0.4)
    caja(azul_osc, -0.82, 0, 0, 0.3, 0.32, 1.02)
    caja(mat('tapa_control', 0x2a3a5c, 0.35), -0.82, 0, 1.02, 0.34, 0.36, 0.06)
    esfera(luz('baliza_control', 0xffb21a, 1.0), -0.82, 0, 1.15, 0.07, 1)
    caja(rojo(), -0.82, -0.165, 0.42, 0.22, 0.01, 0.22)
    texto(blanco(), 'STOP', -0.82, -0.172, 0.53, tam=0.075, prof=0.008)
    caja(blanco(), -0.82, -0.165, 0.76, 0.24, 0.01, 0.1)
    texto(azul(), 'U.S.S.S.', -0.82, -0.172, 0.81, tam=0.045, prof=0.006)
    franjas = rayas('franjas_poste', 0xffc21a, 0x1d1f25, 6, 0.0, 0.9, eje='Z')
    caja(franjas, 0.88, 0, 0, 0.08, 0.08, 0.86)                        # la horquilla
    for s in (-1, 1):
        caja(mat('acero_horq', 0x2a2d33, 0.35), 0.88, s * 0.06, 0.86, 0.06, 0.03, 0.14)
    caja(azul_osc, 0.88, 0, 0, 0.26, 0.26, 0.05)

def barrera_control_brazo():
    """El brazo de la barrera: el origen es la bisagra y se alarga hacia +x."""
    L = 1.72
    caja(rayas('franjas_brazo', 0xe8303a, 0xffffff, 8, 0.0, L, eje='X'), L / 2, 0, -0.045, L, 0.09, 0.09)
    caja(mat('contrapeso', 0x2a2d33, 0.4), -0.12, 0, -0.08, 0.22, 0.12, 0.16)
    cil(rojo(), 0.95, -0.06, -0.22, 0.16, 0.02, 8, eje='Y')            # la señal de STOP colgando
    texto(blanco(), 'STOP', 0.95, -0.075, -0.22, tam=0.08, prof=0.008)
    caja(mat('acero_horq', 0x2a2d33, 0.35), 0.95, -0.05, -0.08, 0.02, 0.02, 0.06)

def dron_tele():
    """El dron de la tele de las Fake News, a la altura de la cabeza: se pasa
    agachado. Las hélices son discos que pone el juego."""
    blanco_d = mat('blanco_dron', 0xf2f4f7, 0.35)
    azul_d = mat('azul_dron', 0x1f3c88, 0.4)
    gris_d = mat('gris_dron', 0x3a3d44, 0.4)
    Z = 1.66
    esfera(blanco_d, 0, 0, Z, 0.3, 3, esc=(1.25, 1.0, 0.42))           # el cuerpo
    caja(azul_d, 0, 0, Z - 0.02, 0.62, 0.5, 0.06)
    for sx in (-1, 1):
        for sy in (-1, 1):
            hx, hy = sx * 0.58, sy * 0.44
            rama(gris_d, (sx * 0.2, sy * 0.15, Z + 0.04), (hx, hy, Z + 0.08), 0.03, 0.025, 6)
            cil(gris_d, hx, hy, Z + 0.02, 0.05, 0.12, 8)              # el motor
            cil(mat('aro_dron', 0x5a5e66, 0.4), hx, hy, Z + 0.13, 0.27, 0.025, 20)   # el aro
            for k in range(2):
                caja(negro(), hx, hy, Z + 0.15, 0.4, 0.035, 0.012, giro=k * math.pi / 2 + 0.4)
            rama(gris_d, (hx, hy, Z + 0.02), (hx, hy, Z - 0.22), 0.015, 0.015, 5)    # las patas
    # la cámara colgando del cardán, mirando al jugador
    caja(gris_d, 0, -0.05, Z - 0.2, 0.06, 0.06, 0.12)
    esfera(negro(), 0, -0.08, Z - 0.26, 0.11, 2)
    cil(mat('lente_dron', 0x5a8ac8, 0.1), 0, -0.19, Z - 0.26, 0.055, 0.04, 12, eje='Y')
    esfera(luz('piloto_dron', 0xff2a2a, 1.0), 0, -0.3, Z + 0.06, 0.035, 1)
    texto(mat('rojo_dron', 0xd8202a, 0.4), 'FAKE NEWS', 0, -0.31, Z - 0.05, tam=0.085, prof=0.01)

def furgoneta_fake():
    """La furgoneta de la tele de las Fake News (se le ve por detrás): blanca,
    con la antena parabólica y el mástil en el techo y el logo en las puertas.
    Los intermitentes los pone el juego encima de los pilotos ámbar."""
    blanco_f = mat('blanco_furgo', 0xf4f6f8, 0.35)
    azul_f = mat('azul_furgo', 0x1f3c88, 0.4)
    rojo_f = mat('rojo_furgo', 0xd8202a, 0.4)
    W, L, H = 1.7, 2.9, 1.95
    caja(blanco_f, 0, L / 2, 0.28, W, L, H - 0.28)                     # la caja
    caja(azul_f, 0, L / 2, 0.62, W + 0.02, L + 0.02, 0.16)             # la franja azul
    caja(rojo_f, 0, L / 2, 0.8, W + 0.02, L + 0.02, 0.07)
    caja(negro(), 0, -0.01, 0.98, 0.02, 0.02, 0.92)                    # la junta de las puertas
    for s in (-1, 1):
        caja(cristal(), s * 0.42, -0.02, 1.4, 0.6, 0.02, 0.36)         # ventanillas de atrás
        caja(piloto(), s * 0.76, -0.02, 1.0, 0.13, 0.03, 0.26)
        caja(ambar(), s * 0.76, -0.02, 0.86, 0.13, 0.03, 0.12)
        rueda(s * (W / 2 - 0.1), 0.55, 0.33, 0.24)
        rueda(s * (W / 2 - 0.1), L - 0.5, 0.33, 0.24)
        texto_lado(azul_f, 'FAKE', s * (W / 2 + 0.012), 1.2, 1.45, 0.3, s)
        texto_lado(rojo_f, 'NEWS', s * (W / 2 + 0.012), 2.15, 1.45, 0.3, s)
    texto(azul_f, 'FAKE', 0, -0.03, 1.2, tam=0.17, prof=0.015)
    texto(rojo_f, 'NEWS', 0, -0.03, 1.0, tam=0.15, prof=0.015)
    caja(negro(), 0, -0.04, 0.2, W + 0.04, 0.12, 0.2)                 # el parachoques
    caja(mat('matricula', 0xf8f6e8, 0.6), 0, -0.1, 0.42, 0.42, 0.01, 0.13)
    texto(azul(), 'TV 24', 0, -0.108, 0.485, tam=0.07, prof=0.006)
    # el techo: la parabólica y el mástil de la antena
    gris_f = mat('gris_furgo', 0x8a9099, 0.4)
    cil(gris_f, 0, 1.0, H, 0.1, 0.14, 10)
    esfera(blanco_f, 0, 1.0, H + 0.5, 0.42, 2, esc=(1, 0.3, 1), mitad=False)
    caja(gris_f, 0, 1.06, H + 0.14, 0.1, 0.1, 0.3)
    cil(gris_f, 0.0, 0.88, H + 0.5, 0.04, 0.18, 6, eje='Y')
    cil(gris_f, 0.5, 2.2, H, 0.05, 0.9, 6)
    cil(gris_f, 0.5, 2.2, H + 0.9, 0.03, 0.35, 6)
    esfera(luz('punta_antena', 0xff3a2a, 1.0), 0.5, 2.2, H + 1.27, 0.04, 1)
    caja(mat('baca', 0x3a3d44, 0.4), 0, L / 2 + 0.3, H, W - 0.3, 1.4, 0.05)

def segway():
    """Un turista en Segway (en Washington se ven por toda la avenida): camisa
    de flores, casco, riñonera y la cámara al cuello. Mira a +x, hacia donde va."""
    plataforma = mat('plataforma_seg', 0x2a2d33, 0.4)
    for s in (-1, 1):
        cil(neumatico(), 0, s * 0.3, 0.24, 0.24, 0.12, 18, eje='Y')
        cil(mat('tapacubos_seg', 0xd8dbe0, 0.3), 0, s * 0.37, 0.24, 0.12, 0.02, 12, eje='Y')
        caja(mat('guardabarros', 0xd8202a, 0.4), 0, s * 0.3, 0.4, 0.32, 0.14, 0.12)
    caja(plataforma, 0, 0, 0.14, 0.36, 0.5, 0.1)
    rama(gris(), (0.0, 0, 0.22), (0.12, 0, 1.08), 0.03, 0.03, 8)          # la barra
    rama(negro(), (0.12, -0.26, 1.1), (0.12, 0.26, 1.1), 0.025, 0.025, 8)  # el manillar
    # el turista
    piel = mat('piel_turista', 0xf2c4a0, 0.6)
    camisa = mat_bloques('camisa_flores', 0x2fb4c8, 0xffe14a, ancho=0.06, alto=0.06, grosor=0.02, variacion=1.2)
    pant = mat('bermudas', 0xd8c49a, 0.6)
    for s in (-1, 1):
        cil(piel, -0.04, s * 0.1, 0.24, 0.065, 0.42, 10)                 # piernas
        cil(pant, -0.04, s * 0.1, 0.62, 0.095, 0.3, 10)
        caja(blanco(), -0.02, s * 0.1, 0.19, 0.24, 0.12, 0.08)            # zapatillas
    cil(camisa, -0.04, 0, 0.9, 0.25, 0.56, 14, r2=0.22)
    esfera(camisa, -0.04, 0, 1.44, 0.23, 2, esc=(0.8, 1.05, 0.45))
    caja(mat('rinonera', 0x1d1f25, 0.5), 0.17, 0, 0.92, 0.1, 0.3, 0.12)
    for s in (-1, 1):                                                  # brazos al manillar
        rama(camisa, (-0.04, s * 0.24, 1.38), (0.03, s * 0.27, 1.2), 0.07, 0.065, 8)
        rama(piel, (0.03, s * 0.27, 1.2), (0.12, s * 0.22, 1.1), 0.05, 0.045, 8)
    cil(piel, -0.04, 0, 1.48, 0.07, 0.1, 10)
    esfera(piel, -0.02, 0, 1.68, 0.16, 2, esc=(1.05, 0.95, 1.08))
    esfera(mat('casco_seg', 0xff8a1a, 0.4), -0.04, 0, 1.76, 0.18, 2, mitad=True, esc=(1.08, 1.0, 0.85))
    for s in (-1, 1):
        caja(negro(), 0.13, s * 0.06, 1.69, 0.03, 0.08, 0.05)            # gafas de sol
    caja(negro(), 0.17, 0, 1.3, 0.1, 0.15, 0.1)                         # la cámara al cuello
    cil(mat('lente_turista', 0x5a8ac8, 0.1), 0.23, 0, 1.35, 0.04, 0.05, 10, eje='X')
    # la banderita del tour
    cil(gris(), -0.16, 0.22, 0.2, 0.012, 1.9, 6)
    caja(rayas('barras_eeuu', 0xe8303a, 0xffffff, 7, 1.8, 0.22, eje='Z'), -0.16, 0.36, 1.8, 0.02, 0.28, 0.22)
    caja(azul(), -0.16, 0.29, 1.92, 0.024, 0.12, 0.1)


PIEZAS = {
    'microfonos':            (microfonos,            'obstaculos', dict(lado=256, bisel=0.0)),
    'barrera_control':       (barrera_control,       'obstaculos', dict(lado=256, bisel=0.0)),
    'barrera_control_brazo': (barrera_control_brazo, 'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
    'dron_tele':             (dron_tele,             'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
    'furgoneta_fake':        (furgoneta_fake,        'obstaculos', dict(lado=512)),
    'segway':                (segway,                'obstaculos', dict(lado=256, bisel=0.0)),
}

correr(PIEZAS)
