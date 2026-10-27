# Obstáculos propios de cada ciudad (27/10/2026).
#
#   blender -b -P blender/obstaculos2.py -- [pieza ...] [--rapido]
#
# Isidro: los tres niveles se jugaban igual (siempre los mismos seis
# obstáculos). Estos son los de cada sitio, con las mismas reglas que
# obstaculos.py: caben en un carril (x de -0.95 a 0.95), miran al jugador por
# -y (en el juego, +z) y el origen es el centro del carril a ras de suelo. Los
# vehículos empiezan en y = 0 (lo que ve el jugador) y se alargan hacia +y.
#
#   Nueva York   taxi (esquivar) · alcantarilla con vapor (saltar)
#                andamio de obra (agacharse) · contenedor de escombros (esquivar)
#   Findlay      pacas de paja (saltar) · tractor (esquivar)
#                carroza del desfile (esquivar) · guirnalda «FLAG CITY» (agacharse)
#   Washington   valla metálica (saltar) · manifestantes del Burrito-Bot (agacharse)
#                agentes del Servicio Secreto (esquivar) · todoterreno de la comitiva (viene de frente)
#   Acera        valla de policía azul y verja negra (delante del público)

import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import *

def blanco():  return mat('blanco', 0xffffff, 0.5)
def negro():   return mat('negro', 0x1d1f25, 0.4)
def gris():    return mat('gris', 0x9aa1aa, 0.5)
def naranja(): return mat('naranja', 0xff7a1a, 0.45)
def rojo():    return mat('rojo', 0xe8303a, 0.45)
def azul():    return mat('azul', 0x2350c8, 0.45)
def oro():     return mat('oro', 0xf2c23a, 0.3)
def cristal(): return mat('cristal', 0x3a6fb0, 0.15)
def neumatico(): return mat('neumatico', 0x1d1e21, 0.8)
def faro():    return mat('faro', 0xfff3c4, 0.2)
def piloto():  return mat('piloto', 0xc0262c, 0.3)
def rayas(nombre, c1, c2, n, x0, ancho, eje='X'):
    return mat_franjas(nombre, c1, c2, n, eje=eje, z0=x0, alto=ancho)

def rueda(x, y, r=0.3, ancho=0.22, z=None):
    z = r if z is None else z
    cil(neumatico(), x, y, z, r, ancho, 16, eje='X')
    cil(mat('llanta', 0xd3d6da, 0.3), x + (0.12 if x > 0 else -0.12), y, z, r * 0.5, 0.02, 12, eje='X')

def bandera(x, y, z, w=0.36, h=0.24):
    """Banderita de EE. UU. que mira a -y."""
    caja(rayas('barras_eeuu', 0xe8303a, 0xffffff, 7, z, h, eje='Z'), x, y, z, w, 0.02, h)
    caja(azul(), x - w * 0.27, y - 0.012, z + h * 0.45, w * 0.46, 0.02, h * 0.55)

def persona(x, ropa, piel, pelo, pantalon=0x3a4a6a, brazos=None):
    """Una persona sencilla de dibujo animado, de cara al jugador."""
    pant = mat(f'pantalon{pantalon:06x}', pantalon, 0.6)
    for s in (-1, 1):
        cil(pant, x + s * 0.09, 0, 0, 0.075, 0.82, 10)
        caja(negro(), x + s * 0.09, -0.05, 0, 0.13, 0.26, 0.08)
    cil(ropa, x, 0, 0.78, 0.21, 0.64, 14, r2=0.18)
    esfera(ropa, x, 0, 1.4, 0.19, 2, esc=(1.05, 0.8, 0.5))
    cil(piel, x, 0, 1.42, 0.07, 0.1, 10)
    esfera(piel, x, 0, 1.63, 0.165, 2, esc=(1, 0.95, 1.08))
    esfera(pelo, x, 0.03, 1.7, 0.17, 2, esc=(1.02, 1.0, 0.75))
    for s in (-1, 1):                                                   # ojos
        esfera(negro(), x + s * 0.055, -0.15, 1.66, 0.022, 1)
    if brazos:
        for (a, b) in brazos:
            rama(ropa, a, b, 0.055, 0.05, 8)
            esfera(piel, b[0], b[1], b[2], 0.06, 1)


# ---------------------------------------------------------------- Nueva York
def taxi():
    """Taxi amarillo parado en el carril (se le ve por detrás: van en el mismo sentido)."""
    amarillo = mat('amarillo_taxi', 0xffc21a, 0.35)
    W, L = 1.6, 2.8
    caja(amarillo, 0, L / 2, 0.24, W, L, 0.56)                          # carrocería
    caja(amarillo, 0, L / 2 + 0.15, 0.8, W - 0.14, L * 0.55, 0.42)       # cabina
    y0 = L / 2 + 0.15 - L * 0.275
    caja(cristal(), 0, y0 - 0.02, 0.84, W - 0.3, 0.04, 0.32)            # luna trasera
    for s in (-1, 1):
        caja(cristal(), s * ((W - 0.14) / 2 + 0.01), L / 2 + 0.15, 0.86, 0.02, L * 0.5, 0.28)
        caja(rayas('cuadros_taxi', 0x1d1f25, 0xffffff, 18, 0, L, eje='Y'), s * (W / 2 + 0.01), L / 2, 0.56, 0.02, L, 0.1)
        caja(piloto(), s * 0.6, -0.01, 0.56, 0.32, 0.04, 0.16)
        rueda(s * (W / 2 - 0.08), 0.55, 0.3, 0.22)
        rueda(s * (W / 2 - 0.08), L - 0.55, 0.3, 0.22)
    caja(gris(), 0, -0.04, 0.2, W + 0.04, 0.1, 0.16)                    # parachoques
    caja(blanco(), 0, -0.02, 0.36, 0.46, 0.02, 0.14)                    # matrícula
    texto(negro(), 'NYC', 0, -0.035, 0.43, tam=0.1, prof=0.01)
    texto(negro(), 'TAXI', 0, -0.02, 0.66, tam=0.16, prof=0.02)
    caja(blanco(), 0, L / 2 + 0.15, 1.22, 0.72, 0.26, 0.24)             # el cartel del techo
    texto(negro(), 'TAXI', 0, L / 2 + 0.15 - 0.14, 1.34, tam=0.13, prof=0.02)

def alcantarilla():
    """Alcantarilla abierta con su barrera rayada (el vapor lo pone el juego)."""
    cil(gris(), 0, 0, 0.0, 0.52, 0.035, 28)
    cil(mat('agujero', 0x0d0e10, 0.9), 0, 0, 0.0, 0.43, 0.05, 28)
    o = cil(mat('tapa', 0x4a4c52, 0.6), 0.58, 0.42, 0.02, 0.4, 0.05, 24)
    o.rotation_euler = (0.25, -0.3, 0)
    for x in (-0.74, 0.74):
        for y in (-0.6, 0.6):
            cil(naranja(), x, y, 0, 0.045, 0.74, 10)
            esfera(blanco(), x, y, 0.76, 0.06, 1)
    for y in (-0.6, 0.6):
        caja(rayas('rayas_alcantarilla', 0xff7a1a, 0xffffff, 8, -0.74, 1.48), 0, y, 0.5, 1.48, 0.05, 0.14)
    for x in (-0.74, 0.74):
        caja(rayas('rayas_alcantarilla_y', 0xff7a1a, 0xffffff, 6, -0.6, 1.2, eje='Y'), x, 0, 0.5, 0.05, 1.2, 0.14)

def andamio():
    """Andamio de acera de Nueva York: se pasa agachado por debajo."""
    verde = mat('verde_andamio', 0x2e6b3d, 0.6)
    for s in (-1, 1):
        for y in (-0.28, 0.28):
            cil(verde, s * 0.9, y, 0, 0.05, 2.45, 8)
            caja(gris(), s * 0.9, y, 0, 0.2, 0.2, 0.05)
    caja(verde, 0, 0, 1.28, 1.98, 0.72, 0.1)                            # la plataforma
    caja(mat('contrachapado', 0x3f7f4c, 0.7), 0, -0.37, 1.2, 1.98, 0.05, 0.72)
    texto(blanco(), 'POST NO BILLS', 0, -0.4, 1.58, tam=0.16, prof=0.02)
    for x in (-0.55, 0.0, 0.55):
        esfera(mat('bombilla', 0xfff3a0, 0.2), x, 0, 1.2, 0.055, 1)
    caja(verde, 0, -0.34, 2.12, 1.98, 0.05, 0.06)                       # barandilla
    for x in (-0.6, 0, 0.6):
        caja(verde, x, -0.34, 1.9, 0.04, 0.04, 0.24)

def contenedor():
    """Contenedor de escombros de una obra."""
    chapa = mat('naranja_contenedor', 0xe9822a, 0.5)
    W, L, H = 1.75, 2.3, 1.12
    caja(chapa, 0, L / 2, 0.12, W, L, H)
    for y in (0.0, L):                                                  # refuerzos
        caja(mat('refuerzo', 0xc96a1c, 0.5), 0, y, 0.12, W + 0.04, 0.08, H)
    for x in (-0.55, 0.0, 0.55):
        caja(mat('refuerzo', 0xc96a1c, 0.5), x, -0.03, 0.12, 0.08, 0.06, H)
    for s in (-1, 1):
        caja(negro(), s * 0.68, L / 2, 0, 0.14, L, 0.13)
    caja(blanco(), 0, -0.04, 0.52, 1.0, 0.03, 0.3)
    texto(negro(), 'DEBRIS', 0, -0.06, 0.67, tam=0.17, prof=0.02)
    madera = mat('madera_obra', 0xc2945e, 0.7)
    caja(madera, -0.35, 0.9, 1.08, 0.14, 1.4, 0.08, inclina=0.45)
    caja(madera, 0.35, 1.4, 1.12, 0.12, 1.1, 0.08, giro=0.4, inclina=-0.35)
    esfera(mat('saco', 0xd8d2c4, 0.8), 0.15, 1.7, 1.22, 0.3, 1, esc=(1, 1, 0.7))
    esfera(mat('cascote', 0x8f8a84, 0.8), -0.3, 1.5, 1.2, 0.22, 1)

# ---------------------------------------------------------------- Findlay
def paca():
    """Tres pacas de paja: dos abajo y una encima."""
    paja = mat_franjas('paja', 0xeacb70, 0xd8ad4c, 9, eje='Z', z0=0.0, alto=0.9)
    cuerda = mat('cuerda', 0x8a5a2a, 0.7)
    for x, z in ((-0.47, 0.0), (0.47, 0.0), (0.0, 0.44)):
        caja(paja, x, 0.05 if z else 0, z, 0.9, 0.62, 0.44)
        for dx in (-0.22, 0.22):
            caja(cuerda, x + dx, 0.05 if z else 0, z, 0.035, 0.64, 0.45)
    for k in range(6):                                                  # pajitas sueltas
        caja(paja, -0.6 + k * 0.25, -0.32, 0.0, 0.18, 0.02, 0.01, giro=k * 0.7)

def tractor():
    """Tractor rojo de granja, de frente."""
    rojo2 = mat('rojo_tractor', 0xd8282a, 0.4)
    amarillo = mat('llanta_amarilla', 0xffc21a, 0.4)
    caja(rojo2, 0, 0.85, 0.42, 0.78, 1.45, 0.7)                         # capó
    caja(gris(), 0, 0.11, 0.48, 0.66, 0.04, 0.56)                       # rejilla
    for k in range(5):
        caja(negro(), -0.24 + k * 0.12, 0.09, 0.52, 0.04, 0.02, 0.48)
    for s in (-1, 1):
        esfera(faro(), s * 0.26, 0.1, 1.0, 0.075, 1)
    cil(negro(), 0.24, 1.1, 1.12, 0.045, 0.7, 8)                        # escape
    for s in (-1, 1):
        rueda(s * 0.6, 0.55, 0.36, 0.26)
        cil(neumatico(), s * 0.72, 2.15, 0.62, 0.62, 0.38, 22, eje='X')
        cil(amarillo, s * 0.92, 2.15, 0.62, 0.36, 0.03, 18, eje='X')
        caja(rojo2, s * 0.72, 2.15, 1.18, 0.42, 1.1, 0.06)              # guardabarros
    caja(rojo2, 0, 2.15, 0.7, 0.98, 0.95, 0.5)                          # cabina
    for x in (-0.46, 0.46):
        for y in (1.72, 2.58):
            cil(negro(), x, y, 1.2, 0.03, 0.95, 6)
    caja(rojo2, 0, 2.15, 2.15, 1.08, 1.05, 0.08)                        # techo
    caja(cristal(), 0, 1.73, 1.28, 0.88, 0.03, 0.7)
    caja(negro(), 0, 2.35, 1.2, 0.5, 0.4, 0.12)                         # asiento
    cil(negro(), 0, 1.95, 1.5, 0.16, 0.04, 14, eje='Y')                 # volante

def carroza():
    """Carroza del desfile de Findlay: plataforma con faldón y una mazorca gigante."""
    W, L = 1.85, 3.5
    caja(azul(), 0, L / 2, 0.15, W, L, 0.7)
    caja(rayas('falda_frente', 0xe8303a, 0xffffff, 9, -W / 2, W), 0, -0.02, 0.05, W + 0.02, 0.04, 0.55)
    for s in (-1, 1):
        caja(rayas('falda_lado', 0xe8303a, 0xffffff, 15, 0, L, eje='Y'), s * (W / 2 + 0.01), L / 2, 0.05, 0.04, L, 0.55)
    caja(mat('estrellas', 0xffffff, 0.5), 0, L / 2, 0.85, W - 0.1, L - 0.1, 0.04)
    granos = mat_bloques('granos', 0xffd23a, 0xd9a21e, ancho=0.1, alto=0.1, grosor=0.018, variacion=1.12)
    esfera(granos, 0, L / 2 + 0.3, 1.75, 0.42, 2, esc=(1, 1, 2.1))
    verde = mat('hoja_maiz', 0x4caf50, 0.6)
    for s in (-1, 1):
        rama(verde, (s * 0.15, L / 2 + 0.3, 0.95), (s * 0.62, L / 2 + 0.2, 2.1), 0.2, 0.02, 6)
    rama(verde, (0, L / 2 + 0.55, 0.95), (0.05, L / 2 + 0.75, 2.2), 0.2, 0.02, 6)
    caja(blanco(), 0, 0.0, 0.88, 1.3, 0.06, 0.42)
    texto(azul(), 'OHIO', 0, -0.04, 1.09, tam=0.3, prof=0.03)
    for s in (-1, 1):
        cil(gris(), s * 0.82, 0.25, 0.85, 0.02, 1.25, 6)
        bandera(s * 0.82 + s * 0.19, 0.25, 1.82)

def guirnalda():
    """Pancarta de Findlay, «Flag City USA», con banderitas: se pasa agachado."""
    for s in (-1, 1):
        cil(rayas('poste_azul', 0xffffff, 0x2350c8, 12, 0, 2.5, eje='Z'), s * 1.0, 0, 0, 0.055, 2.5, 10)
        esfera(oro(), s * 1.0, 0, 2.55, 0.09, 2)
        caja(gris(), s * 1.0, 0, 0, 0.32, 0.32, 0.08)
    caja(blanco(), 0, 0, 1.2, 1.95, 0.08, 0.56)
    caja(rojo(), 0, 0, 1.12, 2.0, 0.1, 0.08)
    caja(rojo(), 0, 0, 1.76, 2.0, 0.1, 0.08)
    texto(azul(), 'FLAG CITY', 0, -0.05, 1.56, tam=0.2, prof=0.03)
    texto(rojo(), 'USA', 0, -0.05, 1.33, tam=0.15, prof=0.03)
    for k in range(4):
        bandera(-0.6 + k * 0.4, -0.02, 0.86, 0.3, 0.2)

# ---------------------------------------------------------------- Washington
def valla_metal():
    """Valla metálica del Servicio Secreto (dos tramos)."""
    acero = mat('acero_negro', 0x2a2d33, 0.35)
    for x0 in (-0.48, 0.48):
        caja(acero, x0, 0, 0.86, 0.92, 0.05, 0.06)
        caja(acero, x0, 0, 0.14, 0.92, 0.05, 0.05)
        for k in range(8):
            caja(acero, x0 - 0.39 + k * 0.111, 0, 0.14, 0.025, 0.025, 0.74)
        for s in (-1, 1):
            caja(acero, x0 + s * 0.44, 0, 0, 0.05, 0.05, 0.92)
            caja(acero, x0 + s * 0.44, 0, 0, 0.06, 0.55, 0.04)
    caja(blanco(), 0.48, -0.04, 0.42, 0.52, 0.02, 0.3)
    texto(azul(), 'POLICE', 0.48, -0.055, 0.57, tam=0.11, prof=0.01)

def protesta():
    """Dos manifestantes del Burrito-Bot con su pancarta en alto: se pasa agachado."""
    piel1, piel2 = mat('piel1', 0xe8b48c, 0.6), mat('piel2', 0x9a6a48, 0.6)
    persona(-0.8, mat('sudadera_verde', 0x3fae5a, 0.6), piel1, mat('pelo1', 0x3a2618, 0.7),
            brazos=[((-0.72, 0, 1.36), (-0.66, -0.1, 1.9)), ((-0.88, 0, 1.36), (-0.74, -0.12, 1.6))])
    persona(0.8, mat('sudadera_naranja', 0xff8a2b, 0.6), piel2, mat('pelo2', 0x161616, 0.7), pantalon=0x2b2b33,
            brazos=[((0.72, 0, 1.36), (0.66, -0.1, 1.9)), ((0.88, 0, 1.36), (0.74, -0.12, 1.6))])
    madera = mat('palo', 0xb88a55, 0.7)
    for s in (-1, 1):
        cil(madera, s * 0.68, -0.12, 1.15, 0.025, 1.0, 6)
    caja(blanco(), 0, -0.14, 1.28, 1.5, 0.03, 0.66)
    texto(rojo(), 'BURRITO-BOT', 0, -0.17, 1.72, tam=0.16, prof=0.02)
    texto(azul(), '2028', 0, -0.17, 1.44, tam=0.22, prof=0.02)

def agentes():
    """Dos agentes del Servicio Secreto: traje negro, gafas de sol y pinganillo."""
    traje = mat('traje_agente', 0x1f2128, 0.45)
    cable = mat('cable', 0xe8e8e8, 0.4)
    for x, piel in ((-0.46, mat('piel1', 0xe8b48c, 0.6)), (0.46, mat('piel3', 0xc48a62, 0.6))):
        for s in (-1, 1):
            cil(traje, x + s * 0.1, 0, 0, 0.09, 0.85, 10)
            caja(negro(), x + s * 0.1, -0.06, 0, 0.15, 0.3, 0.09)
        cil(traje, x, 0, 0.8, 0.26, 0.82, 16, r2=0.33)
        esfera(traje, x, 0, 1.6, 0.33, 2, esc=(1, 0.75, 0.42))
        caja(blanco(), x, -0.24, 1.32, 0.12, 0.04, 0.32)
        caja(negro(), x, -0.26, 1.28, 0.05, 0.03, 0.34)
        for s in (-1, 1):                                               # manos juntas delante
            rama(traje, (x + s * 0.3, -0.02, 1.52), (x + s * 0.08, -0.28, 1.08), 0.09, 0.08, 10)
        esfera(piel, x, -0.31, 1.05, 0.09, 2)
        cil(piel, x, 0, 1.68, 0.09, 0.1, 12)
        esfera(piel, x, 0, 1.9, 0.18, 2, esc=(1, 0.95, 1.1))
        caja(negro(), x, -0.15, 1.93, 0.3, 0.06, 0.08)                  # gafas de sol
        esfera(negro(), x, 0.03, 2.01, 0.16, 2, esc=(1, 1, 0.5))        # pelo rapado
        rama(cable, (x + 0.18, 0, 1.88), (x + 0.22, 0.05, 1.62), 0.012, 0.012, 4)

def suv():
    """Todoterreno negro de la comitiva, de frente y con banderitas (las luces las pone el juego)."""
    negro2 = mat('negro_suv', 0x14161b, 0.22)
    W, L = 1.75, 3.0
    caja(negro2, 0, L / 2, 0.32, W, L, 0.66)
    caja(negro2, 0, L / 2 + 0.3, 0.98, W - 0.1, L - 0.75, 0.6)
    yv = L / 2 + 0.3 - (L - 0.75) / 2
    caja(cristal(), 0, yv - 0.02, 1.02, W - 0.24, 0.04, 0.5)
    for s in (-1, 1):
        caja(cristal(), s * ((W - 0.1) / 2 + 0.01), L / 2 + 0.3, 1.04, 0.02, L - 0.95, 0.42)
        caja(faro(), s * 0.6, -0.02, 0.66, 0.34, 0.04, 0.13)
        rueda(s * (W / 2 - 0.1), 0.6, 0.36, 0.26)
        rueda(s * (W / 2 - 0.1), L - 0.6, 0.36, 0.26)
        cil(gris(), s * 0.7, 0.28, 0.98, 0.012, 0.36, 6)
        bandera(s * 0.7 + s * 0.13, 0.28, 1.18, 0.24, 0.16)
    caja(mat('cromo', 0xc8ccd2, 0.2), 0, -0.02, 0.4, 0.86, 0.04, 0.4)  # calandra
    for k in range(5):
        caja(negro(), 0, -0.04, 0.44 + k * 0.07, 0.8, 0.02, 0.025)
    caja(negro(), 0, -0.05, 0.22, W + 0.05, 0.12, 0.18)

# ---------------------------------------------------------------- acera
def valla_policia():
    """Caballete azul de la policía de Nueva York, delante del público."""
    azul_p = mat('azul_policia', 0x2a4fa8, 0.45)
    for s in (-1, 1):
        for dy in (-1, 1):
            caja(azul_p, s * 0.9, dy * 0.12, 0, 0.08, 0.07, 0.95, inclina=dy * 0.25)
    caja(azul_p, 0, 0, 0.72, 2.0, 0.07, 0.22)
    texto(blanco(), 'POLICE LINE', 0, -0.04, 0.83, tam=0.13, prof=0.015)

def verja():
    """Tramo de verja negra con remates, delante del público de Washington."""
    hierro = mat('hierro', 0x23262c, 0.35)
    caja(hierro, 0, 0, 0.12, 2.0, 0.05, 0.06)
    caja(hierro, 0, 0, 0.92, 2.0, 0.05, 0.06)
    for k in range(13):
        x = -0.96 + k * 0.16
        caja(hierro, x, 0, 0.0, 0.03, 0.03, 1.08)
        cil(oro(), x, 0, 1.08, 0.03, 0.08, 6, r2=0.0)
    for s in (-1, 1):
        caja(hierro, s * 0.96, 0, 0, 0.08, 0.08, 1.15)


PIEZAS = {
    'taxi':          (taxi,          'obstaculos', dict(lado=512)),
    'alcantarilla':  (alcantarilla,  'obstaculos', dict(lado=512, bisel=0.0)),
    'andamio':       (andamio,       'obstaculos', dict(lado=512)),
    'contenedor':    (contenedor,    'obstaculos', dict(lado=512)),
    'paca':          (paca,          'obstaculos', dict(lado=512)),
    'tractor':       (tractor,       'obstaculos', dict(lado=512)),
    'carroza':       (carroza,       'obstaculos', dict(lado=1024)),
    'guirnalda':     (guirnalda,     'obstaculos', dict(lado=512)),
    'valla_metal':   (valla_metal,   'obstaculos', dict(lado=256, bisel=0.0)),
    'protesta':      (protesta,      'obstaculos', dict(lado=512, bisel=0.0)),
    'agentes':       (agentes,       'obstaculos', dict(lado=512, bisel=0.0)),
    'suv':           (suv,           'obstaculos', dict(lado=512)),
    'valla_policia': (valla_policia, 'publico',    dict(lado=256)),
    'verja':         (verja,         'publico',    dict(lado=256, bisel=0.0)),
}

correr(PIEZAS)
