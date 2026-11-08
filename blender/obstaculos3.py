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


# ---------------------------------------------------------------- comunes
def persona_x(x, y, ropa, piel, pelo, pantalon=0x3a4a6a, k=1.0, zapato=0x1d1f25):
    """Persona de dibujo animado que mira a +x (lo que cruza la calle)."""
    pant = mat(f'pantalon{pantalon:06x}', pantalon, 0.6)
    zap = mat(f'zapato{zapato:06x}', zapato, 0.5)
    for s in (-1, 1):
        cil(pant, x, y + s * 0.09 * k, 0, 0.075 * k, 0.82 * k, 10)
        caja(zap, x + 0.05 * k, y + s * 0.09 * k, 0, 0.26 * k, 0.13 * k, 0.08 * k)
    cil(ropa, x, y, 0.78 * k, 0.21 * k, 0.64 * k, 14, r2=0.18 * k)
    esfera(ropa, x, y, 1.4 * k, 0.19 * k, 2, esc=(0.8, 1.05, 0.5))
    cil(piel, x, y, 1.42 * k, 0.07 * k, 0.1 * k, 10)
    esfera(piel, x, y, 1.63 * k, 0.165 * k, 2, esc=(0.95, 1, 1.08))
    esfera(pelo, x - 0.03 * k, y, 1.7 * k, 0.17 * k, 2, esc=(1.0, 1.02, 0.75))
    for s in (-1, 1):
        esfera(negro(), x + 0.15 * k, y + s * 0.055 * k, 1.66 * k, 0.022 * k, 1)

def poste_barrera(cuerpo, tapa, baliza):
    """El poste de una barrera (a la izquierda del carril) y la horquilla de
    enfrente. La bisagra del brazo queda en (-0.72, 0, 0.95), como en el juego."""
    caja(cuerpo, -0.82, 0, 0, 0.3, 0.32, 1.02)
    caja(tapa, -0.82, 0, 1.02, 0.34, 0.36, 0.06)
    if baliza:
        esfera(baliza, -0.82, 0, 1.15, 0.07, 1)
    franjas = rayas('franjas_poste', 0xffc21a, 0x1d1f25, 6, 0.0, 0.9, eje='Z')
    caja(franjas, 0.88, 0, 0, 0.08, 0.08, 0.86)
    for s in (-1, 1):
        caja(mat('acero_horq', 0x2a2d33, 0.35), 0.88, s * 0.06, 0.86, 0.06, 0.03, 0.14)
    caja(cuerpo, 0.88, 0, 0, 0.26, 0.26, 0.05)

def brazo(c1, c2, luces=None):
    L = 1.72
    caja(rayas(f'franjas_brazo{c1:06x}', c1, c2, 8, 0.0, L, eje='X'), L / 2, 0, -0.045, L, 0.09, 0.09)
    caja(mat('contrapeso', 0x2a2d33, 0.4), -0.12, 0, -0.08, 0.22, 0.12, 0.16)
    if luces:
        for x in (0.5, 1.1, 1.62):
            esfera(luces, x, -0.05, 0.0, 0.035, 1)


# ---------------------------------------------------------------- Nueva York
def hidrante():
    """Una boca de riego abierta en pleno verano, en el bordillo de la acera
    (x = -1,65 desde el centro de su carril): el chorro cruza el carril y cae
    en el charco (se salta). 06/11: Isidro la quería en la acera y con el agua
    animada; el chorro, las gotas y las ondas los pone el juego."""
    rojo_h = mat('rojo_hidrante', 0xd8262e, 0.35)
    X = -1.65
    cil(rojo_h, X, 0, 0, 0.2, 0.08, 14)
    cil(rojo_h, X, 0, 0.08, 0.15, 0.5, 14)
    cil(rojo_h, X, 0, 0.58, 0.18, 0.06, 14)
    esfera(rojo_h, X, 0, 0.66, 0.15, 2, mitad=True)
    cil(rojo_h, X, 0, 0.78, 0.05, 0.08, 8)
    for s in (-1, 1):
        cil(rojo_h, X, s * 0.18, 0.38, 0.06, 0.12, 8, eje='Y')
    cil(rojo_h, X + 0.17, 0, 0.42, 0.08, 0.14, 10, eje='X')              # la boca abierta
    caja(mat('tapa_boca', 0x3a3d44, 0.5), X + 0.27, 0, 0.32, 0.03, 0.2, 0.2)   # la llave, colgando
    # El charco donde cae el chorro (oscuro y brillante: asfalto mojado) y el agua clara encima.
    cil(mat('asfalto_mojado', 0x3c4352, 0.08), 0.3, 0, 0.0, 0.8, 0.008, 24)
    cil(mat('charco', 0x7cc4ee, 0.05), 0.45, 0, 0.004, 0.5, 0.008, 22)

def balon():
    """Un balón de baloncesto gigante que viene botando (se salta)."""
    naranja_b = mat('naranja_balon', 0xf07a22, 0.6)
    R = 0.42
    esfera(naranja_b, 0, 0, R, R, 3)
    linea = mat('linea_balon', 0x2a1a12, 0.6)
    cil(linea, 0, 0, R, R + 0.006, 0.03, 32, eje='X')
    cil(linea, 0, 0, R, R + 0.006, 0.03, 32, eje='Y')
    cil(linea, 0, 0, R - 0.015, R + 0.006, 0.03, 32)

def semaforo():
    """El semáforo colgado del brazo sobre el carril (se pasa agachado)."""
    hierro = mat('hierro_semaforo', 0x2b3a2e, 0.4)
    cil(hierro, -0.92, 0.1, 0, 0.07, 2.7, 10)
    rama(hierro, (-0.92, 0.1, 2.62), (0.9, 0.1, 2.62), 0.05, 0.05, 8)
    rama(hierro, (-0.92, 0.1, 2.2), (-0.4, 0.1, 2.6), 0.03, 0.03, 6)
    caja(mat('caja_semaforo', 0x1d1f25, 0.45), 0, 0.1, 1.48, 0.36, 0.3, 1.0)
    cil(hierro, 0, 0.1, 2.48, 0.03, 0.14, 6)
    for z, color, encendida in ((2.24, 0xff2a2a, True), (1.98, 0xffb21a, False), (1.72, 0x2adf6a, False)):
        m = luz('semaforo_rojo', color, 1.0) if encendida else mat(f'apagada{color:06x}', (color & 0xfefefe) >> 1, 0.3)
        cil(m, 0, -0.06, z, 0.1, 0.04, 14, eje='Y')
        caja(mat('visera', 0x1d1f25, 0.45), 0, -0.1, z + 0.08, 0.24, 0.1, 0.03)
    caja(blanco(), 0, 0.12, 2.32, 0.9, 0.03, 0.2)                     # ONE WAY
    caja(negro(), 0, 0.1, 2.33, 0.86, 0.02, 0.17)
    texto(blanco(), 'ONE WAY', -0.05, 0.085, 2.415, tam=0.11, prof=0.008)

def carruaje():
    """El coche de caballos de Central Park, de espaldas: la calesa granate
    con sus ruedas grandes y el cochero con chistera; delante, el caballo blanco.
    Los faroles de atrás hacen de intermitente."""
    granate = mat('granate_calesa', 0x6a1a26, 0.35)
    caja(granate, 0, 0.9, 0.55, 1.3, 1.6, 0.55)
    caja(granate, 0, 0.55, 1.1, 1.3, 0.9, 0.35)
    caja(negro(), 0, 0.3, 1.45, 1.36, 0.6, 0.06)                        # la capota plegada
    esfera(negro(), 0, 0.15, 1.45, 0.66, 2, esc=(1.0, 0.35, 0.55), mitad=True)
    caja(mat('asiento_rojo', 0xb8202e, 0.5), 0, 0.9, 1.1, 1.1, 0.5, 0.15)
    for s in (-1, 1):
        rueda(s * 0.72, 0.45, 0.48, 0.08)
        rueda(s * 0.7, 1.55, 0.36, 0.08)
        cil(mat('farol', 0x2a2d33, 0.3), s * 0.62, -0.02, 1.16, 0.06, 0.2, 8)
        esfera(luz('luz_farol', 0xffd27a, 0.8), s * 0.62, -0.02, 1.26, 0.06, 1)
    # el cochero en el pescante
    persona_cochero = mat('levita', 0x1d1f25, 0.5)
    cil(persona_cochero, 0, 1.55, 1.2, 0.22, 0.55, 12, r2=0.18)
    esfera(mat('piel_cochero', 0xf0c4a0, 0.6), 0, 1.55, 1.92, 0.15, 2)
    cil(negro(), 0, 1.55, 2.02, 0.12, 0.3, 12)                          # chistera
    cil(negro(), 0, 1.55, 2.02, 0.2, 0.02, 12)
    # el caballo (08/11 (2): con forma de caballo y SIN patas: son la pieza
    # caballo_pata de animales.py, que el juego mueve al andar; las caderas
    # estan en world.js, ANDAR.carruaje)
    blanco_c = mat_bloques('pelo_caballo_bl', 0xf1eee8, 0xf1eee8, ancho=0.07, alto=0.12, grosor=0.0, desfase=0.37, variacion=1.09)
    crin = mat('crin', 0x9a8c7c, 0.6)
    esfera(blanco_c, 0, 2.55, 1.2, 0.4, 3, esc=(0.78, 1.55, 0.85))
    esfera(blanco_c, 0, 2.95, 1.24, 0.3, 3)                                # el pecho
    esfera(blanco_c, 0, 2.13, 1.27, 0.3, 3)                                # la grupa
    rama(blanco_c, (0, 2.98, 1.38), (0, 3.28, 1.9), 0.17, 0.11, 12)        # el cuello
    rama(crin, (0, 2.9, 1.5), (0, 3.2, 2.0), 0.05, 0.04, 6)                # la crin
    rama(blanco_c, (0, 3.3, 1.98), (0, 3.52, 1.68), 0.1, 0.075, 12)        # la cabeza
    esfera(blanco_c, 0, 3.53, 1.65, 0.08, 2)
    for s in (-1, 1):
        rama(blanco_c, (s * 0.05, 3.26, 2.02), (s * 0.07, 3.24, 2.14), 0.03, 0.006, 6)   # orejas
        caja(negro(), s * 0.1, 3.36, 1.86, 0.02, 0.1, 0.09)                # anteojeras
        esfera(negro(), s * 0.075, 3.43, 1.84, 0.02, 1)
    rama(crin, (0, 1.85, 1.38), (0, 1.75, 0.8), 0.06, 0.035, 6)            # la cola
    cil(mat('arnes', 0x241a14, 0.5), 0, 2.75, 1.2, 0.35, 0.07, 18, eje='Y')   # el arnes
    for s in (-1, 1):
        rama(mat('varas', 0x2a1a12, 0.5), (s * 0.4, 1.5, 0.8), (s * 0.35, 2.6, 1.1), 0.025, 0.025, 6)

def paseador():
    """Un paseador de perros de Nueva York con cinco perros atados, cruzando
    la calle (miran a +x)."""
    persona_x(-0.35, 0, mat('sudadera_pas', 0x3a7ac8, 0.6), mat('piel_pas', 0xc48a62, 0.6),
              mat('gorra_pas', 0xd8202a, 0.5), pantalon=0x2a2d36)
    correa = mat('correa', 0xd8202a, 0.5)
    perros = ((0.45, -0.55, 0xc8a070, 0.8), (0.7, -0.2, 0x2a2420, 1.0), (0.55, 0.2, 0xf4f0e8, 0.75),
              (0.85, 0.5, 0x8a5a32, 1.1), (0.35, 0.65, 0xe8d0a0, 0.7))
    for x, y, color, k in perros:
        pelo = mat(f'perro{color:06x}', color, 0.7)
        esfera(pelo, x, y, 0.36 * k, 0.17 * k, 2, esc=(1.6, 0.9, 0.9))
        esfera(pelo, x + 0.26 * k, y, 0.52 * k, 0.12 * k, 2)
        esfera(negro(), x + 0.37 * k, y, 0.5 * k, 0.03 * k, 1)
        for s in (-1, 1):
            esfera(pelo, x + 0.24 * k, y + s * 0.08 * k, 0.6 * k, 0.05 * k, 1, esc=(0.6, 0.6, 1.4))
            for dx in (-0.15, 0.15):
                cil(pelo, x + dx * k, y + s * 0.07 * k, 0, 0.035 * k, 0.26 * k, 6)
        rama(pelo, (x - 0.24 * k, y, 0.42 * k), (x - 0.34 * k, y, 0.6 * k), 0.025, 0.015, 5)
        rama(correa, (-0.2, 0.18, 1.05), (x + 0.2 * k, y, 0.45 * k), 0.01, 0.01, 4)


# ---------------------------------------------------------------- Findlay
def paso_nivel():
    """El paso a nivel del tren (Findlay es de vías): poste con la cruz de
    San Andrés y las dos luces rojas; el brazo es paso_nivel_brazo."""
    blanco_p = mat('blanco_paso', 0xf4f4f0, 0.5)
    poste_barrera(mat('caja_paso', 0x3a3d44, 0.4), mat('tapa_paso', 0x4a4e56, 0.4), None)
    cil(blanco_p, -0.82, 0.12, 1.0, 0.05, 1.1, 8)
    for g in (0.6, -0.6):                                               # la cruz
        o = caja(blanco_p, -0.82, 0.08, 1.88, 0.9, 0.03, 0.14)
        o.rotation_euler = (0, g, 0)
    texto(negro(), 'RAILROAD', -0.82, 0.06, 2.06, tam=0.075, prof=0.006)
    texto(negro(), 'CROSSING', -0.82, 0.06, 1.86, tam=0.075, prof=0.006)
    caja(negro(), -0.82, 0.08, 1.4, 0.62, 0.05, 0.08)
    for s in (-1, 1):
        cil(negro(), -0.82 + s * 0.28, 0.06, 1.4, 0.13, 0.08, 14, eje='Y')
        cil(luz('luz_paso', 0xff2a2a, 1.0), -0.82 + s * 0.28, 0.0, 1.4, 0.09, 0.03, 14, eje='Y')
    esfera(mat('campana', 0xd8b04a, 0.3), -0.82, 0.1, 2.18, 0.09, 2, mitad=True)

def paso_nivel_brazo():
    brazo(0xe8303a, 0xffffff, luces=luz('luz_brazo_paso', 0xff3a2a, 1.0))

def pavos():
    """Dos pavos de granja escapados que cruzan Main Street (miran a +x)."""
    marron = mat('pavo', 0x6a4428, 0.6)
    for x, y in ((0.15, -0.3), (-0.2, 0.32)):
        esfera(marron, x, y, 0.45, 0.24, 2, esc=(1.25, 0.95, 1.0))
        for k in range(7):                                              # la cola en abanico
            a = (k - 3) * 0.32
            c = (0x8a5a32, 0xc89a5a, 0x5a3820)[k % 3]
            caja(mat(f'pluma{c:06x}', c, 0.6), x - 0.28, y + math.sin(a) * 0.3, 0.45 + math.cos(a) * 0.3, 0.04, 0.12, 0.34, giro=0, inclina=0).rotation_euler = (a, 0, 0)
        rama(marron, (x + 0.2, y, 0.55), (x + 0.3, y, 0.75), 0.06, 0.05, 6)
        esfera(mat('cabeza_pavo', 0x6a8ac8, 0.5), x + 0.32, y, 0.8, 0.07, 2)
        rama(mat('moco_pavo', 0xd8202a, 0.5), (x + 0.37, y, 0.8), (x + 0.38, y, 0.68), 0.025, 0.02, 5)
        cil(mat('pico_pavo', 0xf2c23a, 0.4), x + 0.4, y, 0.8, 0.02, 0.06, 6, eje='X')
        for s in (-1, 1):
            esfera(negro(), x + 0.36, y + s * 0.045, 0.83, 0.015, 1)
            cil(mat('pata_pavo', 0xe8a03a, 0.5), x, y + s * 0.08, 0, 0.025, 0.25, 5)

def bandera_grande():
    """La bandera gigante de Flag City colgada sobre el carril (se pasa agachado)."""
    W, H, Z = 1.8, 1.05, 1.42
    cuerda = mat('cuerda', 0xd8d0b8, 0.6)
    for s in (-1, 1):
        cil(mat('mastil_band', 0xc8ccd2, 0.25), s * 0.95, 0.06, 0, 0.035, 2.75, 8)
        esfera(mat('bola_mastil', 0xf2c23a, 0.3), s * 0.95, 0.06, 2.78, 0.06, 1)
    rama(cuerda, (-0.95, 0.06, 2.6), (0.95, 0.06, 2.6), 0.012, 0.012, 4)
    caja(rayas('barras_grande', 0xe8303a, 0xffffff, 13, Z, H, eje='Z'), 0, 0.06, Z, W, 0.025, H)
    caja(azul(), -W / 2 + 0.38, 0.045, Z + H - 0.56, 0.76, 0.03, 0.56)
    for i in range(6):
        for j in range(4):
            caja(blanco(), -W / 2 + 0.1 + i * 0.112, 0.028, Z + H - 0.5 + j * 0.13, 0.05, 0.01, 0.05)
    for x in (-0.8, -0.27, 0.27, 0.8):
        rama(cuerda, (x, 0.06, 2.6), (x, 0.06, Z + H), 0.01, 0.01, 4)

def cortacesped():
    """Un granjero en su cortacésped de asiento (se le ve por detrás). El piloto
    ámbar de atrás hace de intermitente."""
    rojo_c = mat('rojo_corta', 0xc8262e, 0.35)
    caja(rojo_c, 0, 0.75, 0.25, 1.05, 1.5, 0.35)
    caja(rojo_c, 0, 1.2, 0.6, 0.9, 0.6, 0.3)                            # el capó
    caja(negro(), 0, 0.45, 0.62, 0.55, 0.45, 0.12)                      # el asiento
    caja(negro(), 0, 0.25, 0.7, 0.55, 0.1, 0.4)
    for s in (-1, 1):
        rueda(s * 0.58, 0.35, 0.3, 0.22)
        rueda(s * 0.48, 1.3, 0.2, 0.16)
        caja(ambar(), s * 0.38, -0.02, 0.4, 0.12, 0.03, 0.08)
    caja(mat('cuchilla', 0x3a3d44, 0.4), 0, 0.85, 0.06, 1.1, 0.7, 0.12)
    rama(negro(), (0, 1.0, 0.75), (0, 0.85, 1.12), 0.025, 0.025, 6)      # el volante
    cil(negro(), 0, 0.82, 1.12, 0.16, 0.03, 14, eje='Y')
    # el granjero, de espaldas
    cuadros = mat_bloques('cuadros_granjero', 0xc8262e, 0x2a1a12, ancho=0.08, alto=0.08, grosor=0.02, desfase=0.0)
    vaquero_pant = mat('peto', 0x3a5a9a, 0.6)
    for s in (-1, 1):
        rama(vaquero_pant, (s * 0.12, 0.5, 0.72), (s * 0.13, 0.85, 0.6), 0.08, 0.075, 8)
    cil(cuadros, 0, 0.45, 0.72, 0.24, 0.62, 14, r2=0.2)
    esfera(cuadros, 0, 0.45, 1.34, 0.21, 2, esc=(1.05, 0.8, 0.5))
    esfera(mat('piel_granjero', 0xe8b48c, 0.6), 0, 0.47, 1.55, 0.16, 2)
    esfera(mat('gorra_granjero', 0x2f6a3a, 0.5), 0, 0.47, 1.6, 0.17, 2, mitad=True)
    caja(mat('gorra_granjero', 0x2f6a3a, 0.5), 0, 0.68, 1.6, 0.22, 0.18, 0.025)
    for s in (-1, 1):
        rama(cuadros, (s * 0.22, 0.45, 1.3), (s * 0.14, 0.8, 1.12), 0.06, 0.055, 8)
    # la hierba cortada que sale por un lado
    for i in range(5):
        esfera(mat('hierba', 0x5aa83a, 0.7), 0.62 + i * 0.06, 0.9 - i * 0.1, 0.12 + i * 0.05, 0.06, 1)

def limonada():
    """El puesto de limonada de una niña, con su cartel (se esquiva)."""
    madera = mat('madera_puesto', 0xd8a868, 0.6)
    caja(madera, 0, 0.1, 0, 1.7, 0.6, 0.95)
    caja(mat('madera_osc', 0xa8743a, 0.6), 0, 0.1, 0.95, 1.8, 0.7, 0.05)
    for s in (-1, 1):
        caja(madera, s * 0.82, 0.38, 1.0, 0.06, 0.06, 1.05)
    caja(mat('cartel_lim', 0xfff4a0, 0.6), 0, 0.38, 1.85, 1.75, 0.04, 0.4)
    texto(mat('letra_lim', 0x2f7a3a, 0.5), 'LEMONADE', 0, 0.355, 2.08, tam=0.2, prof=0.015)
    texto(rojo(), '$0.25', 0, 0.355, 1.9, tam=0.14, prof=0.015)
    caja(mat('mantel', 0xf4c4d8, 0.6), 0, -0.21, 0.35, 1.72, 0.02, 0.55)
    texto(mat('letra_lim', 0x2f7a3a, 0.5), 'ICE COLD', 0, -0.225, 0.62, tam=0.14, prof=0.01)
    cil(mat('jarra', 0xf8f070, 0.2), -0.35, 0.05, 1.0, 0.13, 0.3, 14)
    for x in (0.1, 0.3, 0.5):
        cil(blanco(), x, -0.02, 1.0, 0.05, 0.12, 10, r2=0.06)
    esfera(mat('limon', 0xf8e030, 0.5), -0.6, -0.02, 1.06, 0.07, 2, esc=(1.3, 1, 1))
    # la niña detrás del puesto
    vestido = mat('vestido_nina', 0x6aaee8, 0.6)
    cil(vestido, 0.55, 0.45, 0.6, 0.2, 0.55, 12, r2=0.14)
    esfera(mat('piel_nina', 0xf2c4a0, 0.6), 0.55, 0.45, 1.32, 0.15, 2)
    esfera(mat('pelo_nina', 0xd8a040, 0.7), 0.55, 0.49, 1.38, 0.16, 2, esc=(1.05, 1, 0.8))
    for s in (-1, 1):
        esfera(negro(), 0.55 + s * 0.05, 0.31, 1.34, 0.02, 1)
        esfera(mat('pelo_nina', 0xd8a040, 0.7), 0.55 + s * 0.16, 0.5, 1.3, 0.06, 1)
    rama(vestido, (0.68, 0.45, 1.12), (0.8, 0.4, 1.45), 0.04, 0.035, 6)  # saluda


# ---------------------------------------------------------------- Phoenix
def serpiente():
    """Una serpiente de cascabel enroscada junto a una piedra (se salta)."""
    piel_s = mat_bloques('piel_serpiente', 0xb8925a, 0x6a4a2a, ancho=0.07, alto=0.05, grosor=0.012, variacion=1.1)
    for i in range(26):                                                 # el cuerpo en espiral
        a = i * 0.55
        r = 0.32 - i * 0.008
        esfera(piel_s, 0.1 + math.cos(a) * r, math.sin(a) * r, 0.08 + i * 0.006, 0.09, 1)
    for i in range(6):                                                  # el cuello que se levanta
        esfera(piel_s, 0.1 + 0.04 * i, -0.06 * i, 0.25 + i * 0.07, 0.075, 1)
    esfera(piel_s, 0.34, -0.38, 0.68, 0.1, 2, esc=(1.0, 1.4, 0.75))
    for s in (-1, 1):
        esfera(mat('ojo_serpiente', 0xf2c23a, 0.3), 0.34 + s * 0.06, -0.47, 0.71, 0.022, 1)
    rama(rojo(), (0.34, -0.5, 0.66), (0.34, -0.6, 0.64), 0.008, 0.008, 4)  # la lengua
    for i in range(4):                                                  # el cascabel
        esfera(mat('cascabel', 0xd8c49a, 0.5), -0.25 + 0.02 * i, 0.2, 0.25 + i * 0.07, 0.045, 1)
    piedra = mat('piedra', 0xa88a6a, 0.8)
    esfera(piedra, -0.55, 0.1, 0.25, 0.38, 2, esc=(1.0, 0.9, 0.7))
    esfera(piedra, 0.7, 0.2, 0.15, 0.25, 1, esc=(1.1, 0.9, 0.7))

def rueda_loca():
    """Una rueda de camión suelta que viene botando por la Ruta 66 (se salta)."""
    R = 0.45
    cil(neumatico(), 0, 0, R, R, 0.32, 24, eje='X')
    cil(mat('llanta_rueda', 0xd3d6da, 0.3), 0, 0, R, R * 0.5, 0.34, 16, eje='X')
    cil(mat('buje_rueda', 0x8a9099, 0.3), 0, 0, R, R * 0.18, 0.36, 10, eje='X')
    for k in range(12):                                                 # los tacos del dibujo
        a = k * math.pi / 6
        caja(mat('dibujo', 0x2a2b2e, 0.8), 0, math.sin(a) * R, R + math.cos(a) * R - 0.02, 0.34, 0.08, 0.04).rotation_euler = (a, 0, 0)

def pinata():
    """Una piñata de burro de colores colgada sobre el carril (se pasa agachado)."""
    cuerda = mat('cuerda', 0xd8d0b8, 0.6)
    for s in (-1, 1):
        cil(mat('poste_pinata', 0x8a6a4a, 0.7), s * 0.95, 0.05, 0, 0.04, 2.75, 8)
    rama(cuerda, (-0.95, 0.05, 2.65), (0.95, 0.05, 2.65), 0.012, 0.012, 4)
    rama(cuerda, (0, 0.05, 2.65), (0, 0.05, 2.15), 0.01, 0.01, 4)
    tiras = rayas('tiras_pinata', 0xff4a9a, 0xffd23a, 9, -0.5, 1.0, eje='X')
    esfera(tiras, 0, 0.05, 1.82, 0.32, 2, esc=(1.6, 0.75, 0.8))           # el cuerpo
    for sx in (-1, 1):
        for sy in (-1, 1):
            cil(mat('patas_pinata', 0x3ac8e8, 0.7), sx * 0.3, 0.05 + sy * 0.12, 1.38, 0.07, 0.3, 8)
    rama(tiras, (0.42, 0.05, 1.9), (0.55, 0.05, 2.15), 0.12, 0.1, 8)
    esfera(mat('cabeza_pinata', 0x8ae84a, 0.7), 0.62, 0.05, 2.18, 0.16, 2, esc=(1.4, 0.9, 0.9))
    for s in (-1, 1):
        rama(mat('orejas_pinata', 0xff8a2a, 0.7), (0.6, 0.05 + s * 0.06, 2.3), (0.55, 0.05 + s * 0.1, 2.5), 0.05, 0.02, 6)
        esfera(negro(), 0.74, 0.05 + s * 0.06, 2.24, 0.025, 1)
    rama(mat('cola_pinata', 0xff4a4a, 0.7), (-0.5, 0.05, 1.85), (-0.7, 0.05, 1.6), 0.04, 0.02, 6)
    for k in range(6):                                                  # los flecos
        c = (0xff4a9a, 0x3ac8e8, 0xffd23a)[k % 3]
        caja(mat(f'fleco{c:06x}', c, 0.7), -0.4 + k * 0.16, -0.18, 1.52, 0.1, 0.02, 0.2)

def autocaravana():
    """Una autocaravana blanca de jubilados de viaje, por detrás: franjas
    marrones, escalerilla, rueda de repuesto y bicis. Ámbar de intermitente."""
    blanco_a = mat('blanco_caravana', 0xf2efe6, 0.4)
    W, L, H = 1.85, 3.6, 2.55
    caja(blanco_a, 0, L / 2, 0.35, W, L, H - 0.35)
    caja(blanco_a, 0, L - 0.4, H, W - 0.2, 0.9, 0.35)                   # la capuchina
    for z, c in ((0.9, 0x8a5a32), (1.05, 0xd8903a), (1.18, 0xe8c070)):
        caja(mat(f'franja_car{c:06x}', c, 0.5), 0, L / 2, z, W + 0.02, L + 0.02, 0.1)
    caja(cristal(), 0.3, -0.02, 1.55, 0.9, 0.02, 0.5)
    for s in (-1, 1):
        caja(piloto(), s * 0.8, -0.02, 0.62, 0.15, 0.03, 0.22)
        caja(ambar(), s * 0.8, -0.02, 0.86, 0.15, 0.03, 0.12)
        rueda(s * (W / 2 - 0.1), 0.6, 0.36, 0.26)
        rueda(s * (W / 2 - 0.1), L - 0.7, 0.36, 0.26)
    cil(neumatico(), -0.45, -0.1, 1.35, 0.32, 0.2, 16, eje='Y')        # la de repuesto
    cil(mat('funda', 0x2f6a8a, 0.6), -0.45, -0.21, 1.35, 0.3, 0.02, 16, eje='Y')
    for z in (0.45, 0.75, 1.05, 1.35, 1.65, 1.95, 2.25):                # la escalerilla
        caja(gris(), 0.75, -0.06, z, 0.3, 0.03, 0.03)
    for s in (-1, 1):
        caja(gris(), 0.75 + s * 0.15, -0.06, 0.4, 0.03, 0.03, 2.2)
    caja(negro(), 0, -0.04, 0.25, W + 0.04, 0.12, 0.2)
    caja(mat('matricula_az', 0xf8f6e8, 0.6), 0, -0.1, 0.4, 0.42, 0.01, 0.13)
    texto(mat('granate', 0x8a1a26, 0.5), 'ARIZONA', 0, -0.108, 0.47, tam=0.06, prof=0.006)

def vaquero():
    """Un vaquero a caballo cruzando la calle (miran a +x)."""
    marron = mat('caballo_marron', 0x8a5228, 0.55)
    esfera(marron, 0, 0, 1.25, 0.4, 2, esc=(1.75, 0.85, 0.85))
    for sx in (-0.45, 0.45):
        for sy in (-0.17, 0.17):
            cil(marron, sx, sy, 0, 0.075, 1.0, 8)
            cil(negro(), sx, sy, 0, 0.085, 0.09, 8)
    rama(marron, (0.55, 0, 1.4), (0.85, 0, 1.95), 0.16, 0.12, 8)
    esfera(marron, 0.95, 0, 1.98, 0.14, 2, esc=(1.6, 0.8, 0.85))
    for s in (-1, 1):
        esfera(negro(), 1.02, s * 0.08, 2.05, 0.022, 1)
        rama(marron, (0.86, s * 0.06, 2.1), (0.82, s * 0.07, 2.25), 0.035, 0.015, 5)
    rama(mat('crin_osc', 0x2a1a12, 0.6), (0.55, 0, 1.6), (0.8, 0, 2.1), 0.05, 0.04, 6)
    rama(mat('crin_osc', 0x2a1a12, 0.6), (-0.68, 0, 1.35), (-0.85, 0, 0.8), 0.06, 0.03, 6)
    caja(mat('silla', 0x5a3418, 0.6), -0.05, 0, 1.55, 0.5, 0.62, 0.1)
    # el vaquero
    camisa = mat('camisa_vaquero', 0x2f6a9a, 0.6)
    vaq = mat('vaqueros', 0x3a4a7a, 0.6)
    for s in (-1, 1):
        rama(vaq, (-0.05, s * 0.16, 1.68), (0.05, s * 0.36, 1.2), 0.075, 0.07, 8)
        caja(mat('botas_vaq', 0x5a3418, 0.6), 0.1, s * 0.37, 1.05, 0.2, 0.1, 0.16)
    cil(camisa, -0.05, 0, 1.66, 0.2, 0.55, 12, r2=0.18)
    esfera(camisa, -0.05, 0, 2.25, 0.19, 2, esc=(0.8, 1.05, 0.5))
    esfera(mat('piel_vaquero', 0xd8a07a, 0.6), -0.04, 0, 2.46, 0.15, 2)
    sombrero = mat('sombrero_vaq', 0xc8a06a, 0.6)
    cil(sombrero, -0.04, 0, 2.55, 0.34, 0.03, 16)
    cil(sombrero, -0.04, 0, 2.57, 0.15, 0.2, 12, r2=0.13)
    caja(rojo(), 0.12, 0, 2.3, 0.05, 0.2, 0.08)                         # pañuelo
    for s in (-1, 1):
        rama(camisa, (-0.05, s * 0.2, 2.2), (0.3, s * 0.15, 1.85), 0.055, 0.05, 8)


# ---------------------------------------------------------------- Las Vegas
def ruleta():
    """Una ruleta de casino girando en su mesa baja (se salta)."""
    R = 0.72
    cil(mat('pie_ruleta', 0x3a1a12, 0.5), 0, 0, 0, 0.3, 0.55, 14, r2=0.2)
    cil(mat('madera_ruleta', 0x5a2a18, 0.35), 0, 0, 0.55, R + 0.1, 0.16, 32)
    rojo_r = mat('rojo_ruleta', 0xd8202a, 0.35)
    negro_r = mat('negro_ruleta', 0x1d1f25, 0.35)
    for k in range(16):                                                 # las casillas
        a = k * math.pi / 8
        o = caja(rojo_r if k % 2 else negro_r, math.cos(a) * R * 0.55, math.sin(a) * R * 0.55, 0.71, R * 0.62, R * 0.2, 0.03)
        o.rotation_euler = (0, 0, a)
    cil(mat('verde_cero', 0x1f8a3a, 0.35), 0, 0, 0.72, 0.2, 0.03, 16)
    cil(mat('oro_ruleta', 0xf2c23a, 0.25), 0, 0, 0.72, 0.1, 0.08, 12)
    for k in range(4):
        a = k * math.pi / 2
        rama(mat('oro_ruleta', 0xf2c23a, 0.25), (0, 0, 0.82), (math.cos(a) * 0.2, math.sin(a) * 0.2, 0.82), 0.02, 0.02, 5)
    esfera(blanco(), R * 0.78, 0.0, 0.76, 0.045, 1)                     # la bolita

def barrera_valet():
    """La barrera del aparcamiento del casino, con el letrero de neón VALET."""
    poste_barrera(mat('negro_valet', 0x1d1f25, 0.35), mat('oro_valet', 0xf2c23a, 0.25), luz('baliza_valet', 0xff3aa8, 1.0))
    caja(negro(), -0.82, -0.17, 0.55, 0.26, 0.02, 0.36)
    texto(luz('neon_valet', 0xff5ac8, 1.0), 'VALET', -0.82, -0.185, 0.62, tam=0.075, prof=0.01)
    texto(luz('neon_valet2', 0x5ae8ff, 1.0), 'PARKING', -0.82, -0.185, 0.47, tam=0.05, prof=0.008)

def barrera_valet_brazo():
    brazo(0xf2c23a, 0x1d1f25, luces=luz('luz_brazo_valet', 0xff5ac8, 1.0))

def cartel_boda():
    """El cartel de neón de una capilla de bodas colgado sobre el carril, con
    su corazón (se pasa agachado)."""
    for s in (-1, 1):
        cil(mat('poste_boda', 0x3a3d44, 0.35), s * 0.95, 0.06, 0, 0.04, 2.75, 8)
    rama(mat('barra_boda', 0x3a3d44, 0.35), (-0.95, 0.06, 2.62), (0.95, 0.06, 2.62), 0.03, 0.03, 6)
    for x in (-0.6, 0.6):
        rama(mat('cadena_boda', 0x8a9099, 0.3), (x, 0.06, 2.6), (x, 0.06, 2.32), 0.01, 0.01, 4)
    caja(mat('fondo_boda', 0x2a1a4a, 0.4), 0, 0.06, 1.48, 1.7, 0.08, 0.84)
    caja(mat('marco_boda', 0xf2c23a, 0.25), 0, 0.05, 2.3, 1.74, 0.09, 0.04)
    caja(mat('marco_boda', 0xf2c23a, 0.25), 0, 0.05, 1.46, 1.74, 0.09, 0.04)
    texto(luz('neon_boda', 0xff5ac8, 1.0), 'WEDDING', 0.15, 0.0, 2.08, tam=0.2, prof=0.015)
    texto(luz('neon_boda2', 0xffffff, 1.0), 'CHAPEL', 0.15, 0.0, 1.76, tam=0.18, prof=0.015)
    corazon = luz('neon_corazon', 0xff2a5a, 1.0)
    for s in (-1, 1):
        esfera(corazon, -0.62 + s * 0.08, 0.0, 1.98, 0.1, 2, esc=(1, 0.4, 1))
    o = caja(corazon, -0.62, 0.0, 1.78, 0.18, 0.04, 0.18)
    o.rotation_euler = (0, math.pi / 4, 0)
    texto(luz('neon_boda3', 0x5ae8ff, 1.0), '24 H', 0.15, 0.0, 1.55, tam=0.1, prof=0.01)

def descapotable():
    """Un descapotable rosa de los años 50, con aletas, por detrás; dentro,
    los recién casados. Los pilotos de las aletas hacen de intermitente."""
    rosa = mat('rosa_cadillac', 0xf28ac0, 0.25)
    W, L = 1.7, 3.2
    caja(rosa, 0, L / 2, 0.25, W, L, 0.48)
    for s in (-1, 1):
        caja(rosa, s * (W / 2 - 0.12), 0.35, 0.73, 0.18, 0.7, 0.18, inclina=-0.25)   # las aletas
        caja(piloto(), s * (W / 2 - 0.12), -0.02, 0.62, 0.12, 0.04, 0.22)
        rueda(s * (W / 2 - 0.08), 0.6, 0.32, 0.22)
        rueda(s * (W / 2 - 0.08), L - 0.6, 0.32, 0.22)
        cil(mat('cromo', 0xc8ccd2, 0.2), s * 0.45, -0.03, 0.4, 0.06, 0.06, 10, eje='Y')
    caja(mat('cromo', 0xc8ccd2, 0.2), 0, -0.04, 0.22, W + 0.04, 0.1, 0.14)
    caja(blanco(), 0, 1.6, 0.73, W - 0.3, 1.5, 0.12)                     # los asientos
    caja(blanco(), 0, 1.0, 0.73, W - 0.3, 0.12, 0.45)
    caja(cristal(), 0, 2.25, 0.73, W - 0.3, 0.04, 0.35, inclina=0.35)
    # los novios, de espaldas: ella con velo, él con tupé
    esfera(mat('velo', 0xffffff, 0.6), -0.32, 1.25, 1.15, 0.2, 2, esc=(1, 1, 1.3))
    cil(mat('vestido_novia', 0xffffff, 0.6), -0.32, 1.25, 0.82, 0.2, 0.32, 12)
    esfera(mat('tupe', 0x1a1a1a, 0.4), 0.32, 1.25, 1.2, 0.17, 2, esc=(1, 1.1, 1.0))
    cil(mat('chaqueta_novio', 0x1d1f25, 0.5), 0.32, 1.25, 0.82, 0.22, 0.32, 12)
    texto(blanco(), 'JUST MARRIED', 0, -0.06, 0.38, tam=0.09, prof=0.008)
    for k, s in enumerate((-0.5, -0.2, 0.2, 0.5)):                       # las latas
        rama(gris(), (s, 0.0, 0.3), (s * 1.1, -0.5 - 0.1 * k, 0.08), 0.006, 0.006, 4)
        cil(mat('lata', 0xc8ccd2, 0.3), s * 1.1, -0.55 - 0.1 * k, 0.08, 0.06, 0.14, 8, eje='Y')

def bailarinas():
    """Dos bailarinas de revista con sus plumas, cruzando el Strip (miran a +x)."""
    for y, c in ((-0.32, 0xff5ac8), (0.32, 0x5ae8ff)):
        traje = mat(f'traje_bail{c:06x}', c, 0.25)
        piel = mat('piel_bail', 0xf0c0a0, 0.6)
        for s in (-1, 1):
            cil(piel, 0, y + s * 0.07, 0, 0.06, 0.9, 10)
            caja(mat('tacon', 0xf2c23a, 0.3), 0.05, y + s * 0.07, 0, 0.18, 0.08, 0.1)
        cil(traje, 0, y, 0.82, 0.16, 0.55, 12, r2=0.15)
        esfera(piel, 0, y, 1.42, 0.15, 2, esc=(0.7, 1.0, 0.5))
        cil(piel, 0, y, 1.42, 0.06, 0.12, 8)
        esfera(piel, 0, y, 1.62, 0.14, 2)
        esfera(mat('pelo_bail', 0x5a2a12, 0.6), -0.03, y, 1.68, 0.15, 2, esc=(1, 1, 0.8))
        for s in (-1, 1):
            esfera(negro(), 0.13, y + s * 0.05, 1.65, 0.018, 1)
        # el tocado de plumas y la cola
        pluma = mat(f'pluma_bail{c:06x}', (c | 0x404040) & 0xffffff, 0.6)
        for k in range(5):
            a = (k - 2) * 0.35
            rama(pluma, (-0.02, y, 1.78), (-0.1, y + math.sin(a) * 0.35, 1.78 + math.cos(a) * 0.55), 0.06, 0.02, 6)
        for k in range(5):
            a = (k - 2) * 0.4
            rama(pluma, (-0.15, y, 0.95), (-0.45, y + math.sin(a) * 0.3, 0.95 + math.cos(a) * 0.65), 0.07, 0.02, 6)
        esfera(mat('brillo_bail', 0xf2c23a, 0.2), 0.02, y, 1.8, 0.05, 1)
        for s in (-1, 1):
            rama(piel, (0, y + s * 0.15, 1.38), (0.15, y + s * 0.32, 1.65), 0.045, 0.035, 6)


# ---------------------------------------------------------------- Des Moines
def bola_nieve():
    """Una bola de nieve gigante que viene rodando (se salta)."""
    R = 0.45
    nieve = mat('nieve', 0xf4f8fc, 0.7)
    esfera(nieve, 0, 0, R, R, 3)
    for k in range(7):                                                  # lo que ha ido cogiendo
        a, b = k * 0.9, k * 1.7
        p = (math.cos(a) * math.sin(b) * R, math.sin(a) * math.sin(b) * R, R + math.cos(b) * R)
        if k % 2:
            rama(mat('ramita', 0x5a3a1a, 0.7), p, (p[0] * 1.35, p[1] * 1.35, R + (p[2] - R) * 1.35), 0.02, 0.01, 4)
        else:
            esfera(mat('piedrecita', 0x6a6a72, 0.7), p[0], p[1], p[2], 0.05, 1)

def trineo():
    """Un niño en trineo que cruza la calle cuesta abajo (mira a +x)."""
    rojo_t = mat('rojo_trineo', 0xd8202a, 0.35)
    caja(rojo_t, 0, 0, 0.16, 1.0, 0.55, 0.08)
    for s in (-1, 1):
        rama(mat('patin_trineo', 0xc8ccd2, 0.25), (-0.5, s * 0.25, 0.04), (0.42, s * 0.25, 0.04), 0.025, 0.025, 6)
        rama(mat('patin_trineo', 0xc8ccd2, 0.25), (0.42, s * 0.25, 0.04), (0.6, s * 0.25, 0.22), 0.025, 0.025, 6)
        cil(rojo_t, 0, s * 0.25, 0.04, 0.03, 0.14, 6)
    rama(mat('cuerda_trineo', 0xf2c23a, 0.5), (0.55, -0.2, 0.22), (0.3, 0.0, 0.5), 0.012, 0.012, 4)
    abrigo = mat('abrigo_nino', 0x2f8ad8, 0.6)
    esfera(abrigo, -0.1, 0, 0.42, 0.22, 2, esc=(1.1, 1.0, 1.1))
    for s in (-1, 1):
        rama(mat('pant_nino', 0x2a3044, 0.6), (-0.05, s * 0.1, 0.3), (0.35, s * 0.12, 0.26), 0.07, 0.065, 8)
        caja(negro(), 0.4, s * 0.12, 0.2, 0.12, 0.1, 0.12)
        rama(abrigo, (-0.05, s * 0.2, 0.55), (0.25, s * 0.15, 0.45), 0.055, 0.05, 8)
    cil(mat('bufanda_nino', 0xffd23f, 0.6), -0.08, 0, 0.6, 0.13, 0.08, 12)
    esfera(mat('piel_nino', 0xf2c4a0, 0.6), -0.07, 0, 0.76, 0.14, 2)
    esfera(mat('gorro_nino', 0xd8202a, 0.6), -0.08, 0, 0.82, 0.145, 2, mitad=True)
    esfera(blanco(), -0.1, 0, 0.98, 0.05, 1)
    for s in (-1, 1):
        esfera(negro(), 0.05, s * 0.05, 0.78, 0.018, 1)

def rama_nevada():
    """Una rama de árbol cargada de nieve sobre el carril, con un jilguero
    (el pájaro de Iowa) encima (se pasa agachado)."""
    corteza = mat('corteza', 0x5a3a22, 0.8)
    nieve = mat('nieve', 0xf4f8fc, 0.7)
    rama(corteza, (-1.1, 0.1, 2.9), (-0.3, 0.05, 1.85), 0.16, 0.12, 8)
    rama(corteza, (-0.3, 0.05, 1.85), (0.95, 0.0, 1.7), 0.12, 0.06, 8)
    rama(corteza, (0.1, 0.03, 1.8), (0.5, -0.05, 2.15), 0.05, 0.03, 6)
    rama(corteza, (-0.5, 0.05, 2.05), (-0.2, -0.1, 2.4), 0.05, 0.03, 6)
    for x, z, r in ((-0.85, 2.62, 0.16), (-0.5, 2.15, 0.15), (-0.15, 1.97, 0.15), (0.25, 1.9, 0.13), (0.62, 1.84, 0.11), (0.45, 2.22, 0.08)):
        esfera(nieve, x, 0.04, z, r, 2, esc=(1.6, 1, 0.55))
    for x, z, h in ((-0.4, 1.86, 0.22), (-0.05, 1.74, 0.3), (0.3, 1.7, 0.18), (0.7, 1.64, 0.14)):   # carámbanos
        cil(mat('hielo', 0xcfeaff, 0.1), x, 0.03, z - h, 0.0, h, 6, r2=0.035)
    amarillo_p = mat('jilguero', 0xf8d81a, 0.5)
    esfera(amarillo_p, 0.25, 0.0, 2.05, 0.07, 2, esc=(1.3, 1, 1))
    esfera(amarillo_p, 0.33, 0.0, 2.12, 0.05, 2)
    esfera(negro(), 0.32, 0.0, 2.17, 0.03, 1)
    cil(mat('pico_jilguero', 0xf2a03a, 0.4), 0.39, 0, 2.12, 0.012, 0.04, 5, eje='X')
    caja(negro(), 0.17, 0, 2.06, 0.1, 0.06, 0.03)

def bus_escolar():
    """El autobús escolar amarillo, por detrás (este no se sube: se esquiva).
    Los pilotos ámbar de arriba hacen de intermitente."""
    amarillo_b = mat('amarillo_escolar', 0xffc21a, 0.4)
    W, L, H = 1.8, 3.6, 2.3
    caja(amarillo_b, 0, L / 2, 0.35, W, L, H - 0.35)
    caja(negro(), 0, L / 2, 0.95, W + 0.02, L + 0.02, 0.06)
    caja(negro(), 0, L / 2, 1.25, W + 0.02, L + 0.02, 0.04)
    caja(cristal(), 0, -0.02, 1.45, 0.62, 0.02, 0.5)                    # la puerta de emergencia
    caja(negro(), 0, -0.02, 0.4, 0.7, 0.02, 1.6)
    caja(amarillo_b, 0, -0.03, 0.45, 0.62, 0.02, 0.9)
    texto(negro(), 'SCHOOL BUS', 0, -0.04, 2.08, tam=0.15, prof=0.01)
    texto(negro(), 'EMERGENCY DOOR', 0, -0.045, 1.33, tam=0.05, prof=0.006)
    for s in (-1, 1):
        caja(cristal(), s * 0.62, -0.02, 1.45, 0.36, 0.02, 0.5)
        caja(piloto(), s * 0.72, -0.02, 0.6, 0.16, 0.03, 0.16)
        cil(ambar(), s * 0.6, -0.03, 2.1, 0.07, 0.04, 10, eje='Y')
        cil(piloto(), s * 0.78, -0.03, 2.1, 0.07, 0.04, 10, eje='Y')
        rueda(s * (W / 2 - 0.1), 0.65, 0.36, 0.26)
        rueda(s * (W / 2 - 0.1), L - 0.7, 0.36, 0.26)
        for k in range(4):
            caja(cristal(), s * (W / 2 + 0.01), 0.6 + k * 0.75, 1.55, 0.02, 0.55, 0.45)
    oct_m = rojo()                                                      # la señal de STOP del costado
    cil(oct_m, -W / 2 - 0.05, 0.4, 1.4, 0.18, 0.02, 8, eje='X')
    caja(negro(), 0, -0.04, 0.28, W + 0.04, 0.12, 0.2)
    texto(mat('azul_iowa', 0x1f3c88, 0.5), 'DES MOINES SCHOOLS', 0, -0.04, 1.12, tam=0.06, prof=0.006)

def ciervo():
    """Un ciervo de cola blanca cruzando la calle nevada (mira a +x)."""
    pardo = mat('ciervo', 0xa8743a, 0.6)
    esfera(pardo, 0, 0, 1.05, 0.33, 2, esc=(1.7, 0.75, 0.85))
    esfera(blanco(), 0.05, 0, 0.83, 0.2, 2, esc=(1.6, 0.6, 0.5))
    for sx in (-0.38, 0.38):
        for sy in (-0.13, 0.13):
            cil(pardo, sx, sy, 0, 0.05, 0.9, 8, r2=0.06)
            cil(negro(), sx, sy, 0, 0.055, 0.06, 8)
    rama(pardo, (0.45, 0, 1.15), (0.68, 0, 1.6), 0.11, 0.08, 8)
    esfera(pardo, 0.76, 0, 1.65, 0.11, 2, esc=(1.5, 0.8, 0.85))
    esfera(negro(), 0.92, 0, 1.63, 0.035, 1)
    for s in (-1, 1):
        esfera(negro(), 0.8, s * 0.07, 1.71, 0.02, 1)
        esfera(pardo, 0.68, s * 0.12, 1.78, 0.06, 1, esc=(0.6, 1.4, 1))
        cuerno = mat('cuerno_ciervo', 0xe8dcc0, 0.5)
        rama(cuerno, (0.72, s * 0.05, 1.76), (0.66, s * 0.22, 2.05), 0.025, 0.018, 5)
        rama(cuerno, (0.68, s * 0.15, 1.92), (0.82, s * 0.2, 2.06), 0.015, 0.01, 4)
        rama(cuerno, (0.66, s * 0.2, 2.0), (0.58, s * 0.3, 2.12), 0.015, 0.01, 4)
    esfera(blanco(), -0.58, 0, 1.18, 0.09, 2, esc=(0.8, 1, 1.3))          # la cola blanca


PIEZAS = {
    'microfonos':            (microfonos,            'obstaculos', dict(lado=256, bisel=0.0)),
    'barrera_control':       (barrera_control,       'obstaculos', dict(lado=256, bisel=0.0)),
    'barrera_control_brazo': (barrera_control_brazo, 'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
    'dron_tele':             (dron_tele,             'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
    'furgoneta_fake':        (furgoneta_fake,        'obstaculos', dict(lado=512)),
    'segway':                (segway,                'obstaculos', dict(lado=256, bisel=0.0)),
    # Nueva York
    'hidrante':              (hidrante,              'obstaculos', dict(lado=256, bisel=0.0)),
    'balon':                 (balon,                 'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
    'semaforo':              (semaforo,              'obstaculos', dict(lado=256, bisel=0.0)),
    'carruaje':              (carruaje,              'obstaculos', dict(lado=512, bisel=0.0)),
    'paseador':              (paseador,              'obstaculos', dict(lado=256, bisel=0.0)),
    # Findlay
    'paso_nivel':            (paso_nivel,            'obstaculos', dict(lado=256, bisel=0.0)),
    'paso_nivel_brazo':      (paso_nivel_brazo,      'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
    # pavos (08/11 (2): ahora en animales.py, con las patas aparte)
    'bandera_grande':        (bandera_grande,        'obstaculos', dict(lado=256, bisel=0.0)),
    'cortacesped':           (cortacesped,           'obstaculos', dict(lado=256, bisel=0.0)),
    'limonada':              (limonada,              'obstaculos', dict(lado=512, bisel=0.0)),
    # Phoenix
    'serpiente':             (serpiente,             'obstaculos', dict(lado=256, bisel=0.0)),
    'rueda_loca':            (rueda_loca,            'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
    'pinata':                (pinata,                'obstaculos', dict(lado=256, bisel=0.0)),
    'autocaravana':          (autocaravana,          'obstaculos', dict(lado=512)),
    'vaquero':               (vaquero,               'obstaculos', dict(lado=256, bisel=0.0)),
    # Las Vegas
    'ruleta':                (ruleta,                'obstaculos', dict(lado=256, bisel=0.0)),
    'barrera_valet':         (barrera_valet,         'obstaculos', dict(lado=256, bisel=0.0)),
    'barrera_valet_brazo':   (barrera_valet_brazo,   'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
    'cartel_boda':           (cartel_boda,           'obstaculos', dict(lado=256, bisel=0.0)),
    'descapotable':          (descapotable,          'obstaculos', dict(lado=512)),
    'bailarinas':            (bailarinas,            'obstaculos', dict(lado=256, bisel=0.0)),
    # Des Moines
    'bola_nieve':            (bola_nieve,            'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
    'trineo':                (trineo,                'obstaculos', dict(lado=256, bisel=0.0)),
    'rama_nevada':           (rama_nevada,           'obstaculos', dict(lado=256, bisel=0.0)),
    'bus_escolar':           (bus_escolar,           'obstaculos', dict(lado=512)),
    # ciervo (08/11 (2): ahora en animales.py, con las patas aparte)
}

correr(PIEZAS)
