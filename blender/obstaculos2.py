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
#   Las Vegas    dado gigante (viene rodando: saltar) · fichas de casino (saltar)
#                tragaperras (esquivar) · limusina blanca (esquivar)
#                marquesina «DEBATE» (agacharse) · y el atril del Burrito-Bot
#                (va pegado al jefe en el debate; los neones brillan solos)
#   Todos        el helicóptero de la tele de las Fake News (31/10, decorado)
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

# ---------------------------------------------------------------- Phoenix
def costillas(x0):
    return mat_franjas('costillas_obst', 0x4f8f45, 0x3f7a38, 14, eje='X', z0=x0, alto=1.0)

def nopal():
    """Nopales en un montoncito de arena: se saltan (y pinchan)."""
    cil(mat('arena_obst', 0xd9b47a, 0.9), 0, 0, 0, 0.9, 0.12, 16, r2=0.75)
    pala = mat('nopal', 0x5a9a45, 0.6)
    for x, z, sx, giro in ((-0.45, 0.12, 0.34, 0.2), (0.4, 0.12, 0.3, -0.25), (0, 0.4, 0.3, 0.05), (-0.3, 0.55, 0.22, 0.6), (0.3, 0.62, 0.2, -0.5)):
        o = esfera(pala, x, 0, z + 0.25, 0.3, 2, esc=(sx / 0.3, 0.32, 1.0))
        o.rotation_euler = (0, giro, 0)
    for k in range(6):                                                  # flores amarillas
        esfera(mat('flor_nopal', 0xffd23f, 0.5), -0.5 + k * 0.2, -0.12, 0.75 + (k % 2) * 0.12, 0.05, 1)

def rodadora():
    """Rodadora del desierto: una bola de ramas secas que viene rodando."""
    seca = mat('rama_seca', 0xb08a55, 0.9)
    import random
    rnd = random.Random(7)
    for k in range(46):
        a, b = rnd.uniform(0, math.pi * 2), rnd.uniform(-1, 1)
        c, d = rnd.uniform(0, math.pi * 2), rnd.uniform(-1, 1)
        p0 = (0.42 * math.cos(a) * math.sqrt(1 - b * b), 0.42 * math.sin(a) * math.sqrt(1 - b * b), 0.45 + 0.42 * b)
        p1 = (0.42 * math.cos(c) * math.sqrt(1 - d * d), 0.42 * math.sin(c) * math.sqrt(1 - d * d), 0.45 + 0.42 * d)
        rama(seca, p0, p1, 0.022, 0.016, 4)

def saguaro():
    """Un saguaro enorme en mitad del carril: hay que esquivarlo."""
    cil(mat('arena_obst', 0xd9b47a, 0.9), 0, 0, 0, 0.85, 0.15, 16, r2=0.65)
    piel = costillas(-0.5)
    cil(piel, 0, 0, 0, 0.36, 2.6, 14, r2=0.32)
    esfera(piel, 0, 0, 2.6, 0.32, 2)
    for s, h in ((-1, 1.1), (1, 1.5)):
        rama(piel, (0, 0, h), (s * 0.62, 0, h + 0.12), 0.21, 0.21, 10)
        cil(piel, s * 0.62, 0, h, 0.21, 0.85, 10)
        esfera(piel, s * 0.62, 0, h + 0.85, 0.21, 1)
    esfera(mat('flor_saguaro', 0xfff3e0, 0.5), 0, -0.1, 2.85, 0.09, 1)

def pickup():
    """Camioneta de los años 50, turquesa, vista por detrás."""
    cuerpo = mat('turquesa_pickup', 0x3fb8b0, 0.3)
    W, L = 1.75, 3.0
    caja(cuerpo, 0, 0.75, 0.35, W, 1.5, 0.6)                             # la caja de carga
    caja(mat('fondo_caja', 0x2f8f88, 0.5), 0, 0.75, 0.7, W - 0.15, 1.35, 0.06)
    caja(cuerpo, 0, 2.3, 0.35, W, 1.6, 0.65)                             # el morro
    caja(cuerpo, 0, 1.85, 0.95, W - 0.25, 0.85, 0.7)                     # la cabina
    caja(cristal(), 0, 1.41, 1.05, W - 0.55, 0.04, 0.45)
    caja(mat('cromo_pickup', 0xd8dde3, 0.2), 0, -0.04, 0.25, W + 0.06, 0.1, 0.16)
    caja(blanco(), 0, -0.02, 0.4, 0.42, 0.02, 0.14)
    texto(azul(), 'ARIZONA', 0, -0.035, 0.47, tam=0.07, prof=0.01)
    for s in (-1, 1):
        caja(piloto(), s * 0.72, -0.01, 0.55, 0.16, 0.04, 0.2)
        cil(cuerpo, s * (W / 2 - 0.05), 0.6, 0.45, 0.42, 0.3, 14, eje='X')     # guardabarros
        rueda(s * (W / 2 - 0.1), 0.6, 0.34, 0.26)
        rueda(s * (W / 2 - 0.1), L - 0.5, 0.34, 0.26)

def arco_neon():
    """Arco de neón «PHOENIX» sobre el carril: se pasa agachado."""
    hierro = mat('hierro_neon', 0x2a2d33, 0.4)
    for s in (-1, 1):
        cil(hierro, s * 0.95, 0, 0, 0.06, 2.4, 8)
        caja(gris(), s * 0.95, 0, 0, 0.3, 0.3, 0.08)
    caja(mat('fondo_neon', 0x1d2b46, 0.5), 0, 0, 1.25, 1.95, 0.1, 0.6)
    texto(mat('neon_rosa', 0xff4fa0, 0.15), 'PHOENIX', 0, -0.06, 1.55, tam=0.3, prof=0.04)
    for k in range(9):                                                  # bombillas
        esfera(mat('bombilla_neon', 0xffe066, 0.2), -0.88 + k * 0.22, -0.05, 1.95, 0.05, 1)
    sol = mat('sol_neon', 0xffa21a, 0.2)
    cil(sol, 0, -0.06, 2.1, 0.28, 0.04, 16, eje='Y')

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


# ---------------------------------------------------------------- Las Vegas (29/10/2026)
def dado():
    """Dado gigante rojo de casino que viene rodando: el centro en el origen
    (el juego lo sube y lo hace girar sobre sí mismo)."""
    caja(mat('dado_rojo', 0xd8202a, 0.25), 0, 0, -0.45, 0.9, 0.9, 0.9)
    punto = mat('punto_dado', 0xffffff, 0.3)
    caras = {  # (eje fijo, signo): puntos en las otras dos coordenadas
        ('y', -1): [(0, 0)],
        ('y', 1): [(-0.22, -0.22), (0.22, 0.22), (-0.22, 0.22), (0.22, -0.22), (-0.22, 0), (0.22, 0)],
        ('x', 1): [(-0.22, -0.22), (0.22, 0.22)],
        ('x', -1): [(-0.22, -0.22), (0, 0), (0.22, 0.22)],
        ('z', 1): [(-0.22, -0.22), (0.22, 0.22), (-0.22, 0.22), (0.22, -0.22)],
        ('z', -1): [(-0.22, -0.22), (0.22, 0.22), (-0.22, 0.22), (0.22, -0.22), (0, 0)],
    }
    for (eje, sg), pts in caras.items():
        for a, b in pts:
            if eje == 'y':
                esfera(punto, a, sg * 0.45, b, 0.085, 1, esc=(1, 0.35, 1))
            elif eje == 'x':
                esfera(punto, sg * 0.45, a, b, 0.085, 1, esc=(0.35, 1, 1))
            else:
                esfera(punto, a, b, sg * 0.45, 0.085, 1, esc=(1, 1, 0.35))

def fichas():
    """Tres montones de fichas de casino: se saltan."""
    colores = [0xd8202a, 0x1d1f25, 0x2f9a4a, 0x2350c8]
    canto = mat('canto_ficha', 0xffffff, 0.4)
    for k, (x, y, n) in enumerate(((-0.5, 0.05, 7), (0.05, -0.1, 9), (0.55, 0.1, 6))):
        for i in range(n):
            c = colores[(i + k) % 4]
            cil(mat(f'ficha{c:06x}', c, 0.35), x, y, i * 0.095, 0.36, 0.085, 20)
            for j in range(6):                                          # el canto a rayas
                a = j / 6 * math.pi * 2
                caja(canto, x + math.cos(a) * 0.355, y + math.sin(a) * 0.355, i * 0.095 + 0.01,
                     0.06, 0.06, 0.065, giro=a)

def tragaperras():
    """Tragaperras gigante: cuerpo rojo y cromo, los tres rodillos con el 7,
    la palanca y el letrero JACKPOT encendido arriba."""
    cuerpo = mat('rojo_tragaperras', 0xc8202a, 0.3)
    cromo = mat('cromo_tragaperras', 0xd8dde3, 0.15)
    caja(cuerpo, 0, 0, 0, 1.7, 0.9, 2.2)
    caja(cromo, 0, -0.02, 0.05, 1.75, 0.95, 0.12)
    caja(cromo, 0, -0.02, 2.1, 1.75, 0.95, 0.12)
    caja(cromo, 0, -0.5, 1.0, 1.4, 0.1, 0.95)                           # marco de los rodillos
    for x in (-0.42, 0, 0.42):
        caja(luz('rodillo', 0xfff6e0, 0.7), x, -0.56, 1.08, 0.36, 0.04, 0.8)
        texto(luz('siete', 0xd8202a, 0.6), '7', x, -0.6, 1.47, tam=0.42, prof=0.03)
    caja(mat('bandeja', 0x2a2d33, 0.4), 0, -0.5, 0.3, 1.0, 0.2, 0.25)
    for k in range(4):
        cil(mat('moneda_oro', 0xf2c23a, 0.25), -0.3 + k * 0.2, -0.55, 0.55, 0.08, 0.02, 12)
    # la palanca
    cil(cromo, 0.95, 0, 1.0, 0.07, 0.6, 8, eje='X')
    rama(cromo, (1.05, 0, 1.0), (1.05, 0, 1.9), 0.05, 0.05, 8)
    esfera(mat('bola_palanca', 0xe8202a, 0.3), 1.05, 0, 1.95, 0.13, 2)
    # letrero
    caja(mat('fondo_jackpot', 0x1d2b46, 0.4), 0, 0, 2.2, 1.8, 0.4, 0.55)
    texto(luz('jackpot', 0xffe066, 1.0), 'JACKPOT', 0, -0.21, 2.47, tam=0.26, prof=0.03)
    for k in range(8):
        esfera(luz('bombilla_jp', 0xffe9a0, 1.0), -0.8 + k * 0.23, -0.21, 2.75, 0.05, 1)

def limusina():
    """Limusina blanca alargada, vista por detrás."""
    cuerpo = mat('blanco_limo', 0xf6f6f2, 0.25)
    W, L = 1.8, 4.4
    caja(cuerpo, 0, L / 2, 0.3, W, L, 0.6)
    caja(cuerpo, 0, L / 2 + 0.1, 0.9, W - 0.2, L - 1.6, 0.55)
    caja(mat('cristal_limo', 0x1d2533, 0.15), 0, L / 2 + 0.1, 0.95, W - 0.18, L - 1.9, 0.38)
    caja(mat('cromo_limo', 0xd8dde3, 0.2), 0, -0.04, 0.25, W + 0.06, 0.1, 0.14)
    caja(blanco(), 0, -0.02, 0.42, 0.42, 0.02, 0.14)
    texto(azul(), 'NEVADA', 0, -0.035, 0.49, tam=0.065, prof=0.01)
    for s in (-1, 1):
        caja(luz('piloto_limo', 0xff2a2a, 0.8), s * 0.75, -0.01, 0.55, 0.22, 0.04, 0.14)
        rueda(s * (W / 2 - 0.1), 0.65, 0.3, 0.24)
        rueda(s * (W / 2 - 0.1), L - 0.6, 0.3, 0.24)

def marquesina():
    """Marquesina de neón «DEBATE» con bombillas sobre el carril: se pasa agachado."""
    hierro = mat('hierro_marq', 0x2a2d33, 0.4)
    for s in (-1, 1):
        cil(hierro, s * 0.95, 0, 0, 0.07, 2.5, 8)
        caja(gris(), s * 0.95, 0, 0, 0.3, 0.3, 0.08)
    caja(mat('fondo_marq', 0x2a1446, 0.5), 0, 0, 1.3, 1.98, 0.14, 0.7)
    texto(luz('neon_debate', 0xff4fd8, 1.0), 'DEBATE', 0, -0.08, 1.65, tam=0.32, prof=0.04)
    bombilla = luz('bombilla_marq', 0xffe066, 1.0)
    for k in range(10):
        esfera(bombilla, -0.9 + k * 0.2, -0.08, 2.08, 0.05, 1)
        esfera(bombilla, -0.9 + k * 0.2, -0.08, 1.24, 0.05, 1)
    for s in (-1, 1):
        cil(luz('estrella_marq', 0x46e0d0, 1.0), s * 0.95, -0.05, 2.5, 0.18, 0.04, 5, eje='Y')

def atril():
    """El atril del Burrito-Bot para el debate: rojo con las estrellas
    amarillas, dos micrófonos y propulsores debajo (flota con él). El origen
    es el centro de la base; se pega delante del jefe en el juego."""
    rojo_c = mat('rojo_atril', 0xd8202a, 0.4)
    caja(mat('madera_atril', 0x6a3a22, 0.6), 0, 0, 0, 1.6, 0.8, 1.25)
    caja(rojo_c, 0, -0.05, 0.08, 1.5, 0.75, 1.1)
    caja(mat('tapa_atril', 0x3a2418, 0.6), 0, 0.05, 1.25, 1.8, 1.0, 0.1, inclina=-0.25)
    estrella = luz('estrella_atril', 0xffd23f, 0.8)
    cil(estrella, -0.4, -0.44, 0.85, 0.22, 0.04, 5, eje='Y')
    for x, z in ((-0.08, 1.05), (0.04, 0.92), (0.04, 0.72), (-0.08, 0.6)):
        cil(estrella, x, -0.44, z, 0.07, 0.04, 5, eje='Y')
    texto(luz('letra_atril', 0xffd23f, 0.8), '2028', 0.35, -0.45, 0.4, tam=0.24, prof=0.03)
    # micrófonos hacia la boca del robot
    for s in (-1, 1):
        rama(gris(), (s * 0.25, -0.2, 1.3), (s * 0.12, -0.5, 1.75), 0.025, 0.025, 6)
        esfera(negro(), s * 0.12, -0.52, 1.8, 0.07, 1, esc=(1, 1, 1.4))
    # propulsores
    for x in (-0.5, 0.5):
        cil(gris(), x, 0, -0.35, 0.22, 0.35, 12, r2=0.28)
        o = cil(luz('fuego_atril', 0xffa21a, 1.0), x, 0, -0.35, 0.18, 0.5, 10, r2=0.0)
        o.rotation_euler = (math.pi, 0, 0)
        o.location = (x, 0, -0.35 - 0.25)


# ---------------------------------------------------------------- 31/10: el helicóptero de las Fake News
def texto_lado(m, cadena, x, y, z, tam, lado):
    """Letras en un costado que mira a +x (lado 1) o a -x (lado -1)."""
    o = texto(m, cadena, 0, 0, 0, tam=tam, prof=0.03)
    o.rotation_euler = (math.pi / 2, 0, lado * math.pi / 2)
    o.location = (x + lado * 0.015, y, z)
    return o

def helicoptero():
    """Helicóptero de la tele de las Fake News: mira al jugador (el morro
    hacia -y), cabina blanca con franja roja y azul, cristal, el cámara en la
    puerta, el letrero en los dos costados, cola, patines y el foco debajo.
    Las palas las pone el juego (un disco borroso que gira despacio)."""
    blanco_h = mat('blanco_heli', 0xf4f6f8, 0.35)
    azul_h = mat('azul_heli', 0x1f3c88, 0.4)
    rojo_h = mat('rojo_heli', 0xd8202a, 0.4)
    esfera(blanco_h, 0, 0, 1.2, 1.0, 3, esc=(0.95, 1.6, 0.85))              # la cabina
    esfera(mat('cristal_heli', 0x2a4a6a, 0.1), 0, -0.8, 1.35, 0.85, 3, esc=(0.85, 0.95, 0.7))
    caja(rojo_h, 0, 0.05, 0.62, 1.86, 2.6, 0.2)                            # franjas
    caja(azul_h, 0, 0.05, 0.82, 1.84, 2.4, 0.14)
    rama(blanco_h, (0, 1.2, 1.35), (0, 4.6, 1.7), 0.32, 0.14, 10)            # la cola
    caja(azul_h, 0, 4.6, 1.7, 0.08, 0.7, 1.1, inclina=0.35)                  # deriva
    caja(blanco_h, 0, 4.4, 1.75, 1.1, 0.35, 0.06)                           # estabilizador
    cil(mat('rotor_cola', 0x3a3d44, 0.4), 0.16, 4.75, 2.05, 0.08, 0.12, 8, eje='X')
    caja(mat('mastil_rotor', 0x3a3d44, 0.4), 0, 0.1, 2.0, 0.3, 0.5, 0.35)    # el mástil del rotor
    cil(mat('buje', 0x2a2d33, 0.3), 0, 0.1, 2.35, 0.2, 0.18, 10)
    # patines
    patin = mat('patin', 0x3a3d44, 0.4)
    for s in (-1, 1):
        rama(patin, (s * 0.75, -1.3, 0.0), (s * 0.75, 1.3, 0.0), 0.06, 0.06, 6)
        rama(patin, (s * 0.75, -1.3, 0.0), (s * 0.75, -1.55, 0.18), 0.06, 0.06, 6)
        for y in (-0.6, 0.6):
            rama(patin, (s * 0.75, y, 0.0), (s * 0.45, y, 0.55), 0.05, 0.05, 6)
    # FAKE NEWS en los dos costados y en la cola
    for lado in (-1, 1):
        texto_lado(azul_h, 'FAKE', lado * 0.93, 0.15, 1.45, 0.36, lado)
        texto_lado(rojo_h, 'NEWS', lado * 0.9, 0.15, 1.05, 0.3, lado)
        texto_lado(rojo_h, 'TV', lado * 0.2, 3.1, 1.55, 0.26, lado)
    # el cámara asomado por la puerta (lado que da a la calle, -x)
    persona_x = -0.85
    cil(mat('ropa_camara', 0x2a2d33, 0.6), persona_x, -0.1, 0.85, 0.2, 0.55, 10)
    esfera(mat('piel_camara', 0xf0c8a0, 0.6), persona_x, -0.15, 1.55, 0.17, 2)
    esfera(mat('gorra_camara', 0xd8202a, 0.5), persona_x, -0.12, 1.66, 0.17, 2, mitad=True)
    caja(mat('camara_tv', 0x1d1e24, 0.4), persona_x - 0.25, -0.35, 1.3, 0.25, 0.55, 0.3)
    cil(mat('objetivo', 0x5a7aa0, 0.1), persona_x - 0.25, -0.65, 1.45, 0.1, 0.06, 10, eje='Y')
    esfera(luz('piloto_camara', 0xff2a2a, 1.0), persona_x - 0.25, -0.4, 1.62, 0.05, 1)
    # el foco de debajo y las luces de posición
    cil(mat('foco_heli', 0x3a3d44, 0.4), 0.3, -0.9, 0.35, 0.18, 0.25, 10)
    esfera(luz('lente_foco', 0xfff6d8, 1.0), 0.3, -0.9, 0.3, 0.14, 1)
    esfera(luz('luz_roja_heli', 0xff2a2a, 1.0), -0.95, 0.4, 1.0, 0.07, 1)
    esfera(luz('luz_verde_heli', 0x2aff6a, 1.0), 0.95, 0.4, 1.0, 0.07, 1)
    esfera(luz('baliza_heli', 0xff4a2a, 1.0), 0, 4.75, 2.3, 0.08, 1)


# ---------------------------------------------------------------- 31/10: cada mapa con los suyos
# Isidro: «falta que los obstáculos sean diferentes en cada mapa». Fuera los
# de siempre (conos, barricadas, pancartas, globos) y estos en su lugar:
#   Nueva York   bolsas de basura (saltar) · viga de grúa colgando (agacharse)
#                carrito de perritos (esquivar) · repartidor en bici (viene de frente)
#   Findlay      calabazas (saltar) · vaca (cruza la calle)
#   Phoenix      calavera de vaca (saltar) · cartel de la autopista I-10 (agacharse)
#   Las Vegas    imitador de Elvis (esquivar; baila)
#   Washington   cajas de papeles secretos (saltar)

def basura():
    """Bolsas de basura negras y una caja de cartón en la acera de Nueva York."""
    bolsa = mat('bolsa_basura', 0x26282e, 0.25)
    for x, y, r, h in ((-0.55, 0.05, 0.36, 0.62), (0.05, -0.05, 0.4, 0.7), (0.55, 0.1, 0.34, 0.58), (-0.2, 0.25, 0.3, 0.52)):
        esfera(bolsa, x, y, h * 0.5, r, 2, esc=(1, 1, h / (2 * r) * 1.05))
        cil(bolsa, x, y, h * 0.92, 0.07, 0.14, 8, r2=0.03)               # el nudo
        esfera(mat('brillo_bolsa', 0x5a5e68, 0.2), x - r * 0.35, y - r * 0.7, h * 0.62, r * 0.18, 1, esc=(1, 0.4, 1.5))
    carton = mat('carton', 0xc8955a, 0.8)
    caja(carton, 0.35, -0.25, 0, 0.5, 0.4, 0.38, giro=0.3)
    caja(mat('cinta_carton', 0xe8d2a8, 0.6), 0.35, -0.25, 0.38, 0.52, 0.08, 0.01, giro=0.3)

def viga():
    """Viga de acero naranja colgando de la grúa por dos cables: se pasa agachado."""
    naranja_v = mat('viga_naranja', 0xe8701a, 0.4)
    caja(naranja_v, 0, 0, 1.28, 2.0, 0.3, 0.05)                           # ala de abajo
    caja(naranja_v, 0, 0, 1.33, 2.0, 0.06, 0.34)                          # alma
    caja(naranja_v, 0, 0, 1.67, 2.0, 0.3, 0.05)                           # ala de arriba
    for x in (-0.7, -0.35, 0, 0.35, 0.7):
        cil(mat('remache', 0xb85a14, 0.4), x, -0.04, 1.5, 0.03, 0.02, 8, eje='Y')
    cable = mat('cable_grua', 0x2a2d33, 0.4)
    for x in (-0.6, 0.6):
        rama(cable, (x, 0, 1.72), (0, 0, 2.9), 0.02, 0.02, 6)
    rama(cable, (0, 0, 2.9), (0, 0, 4.2), 0.03, 0.03, 6)
    caja(mat('gancho', 0xf2c23a, 0.4), 0, 0, 2.85, 0.22, 0.12, 0.3)      # el gancho amarillo
    # rayas de peligro en los extremos
    for s in (-1, 1):
        caja(rayas('peligro', 0x1d1f25, 0xffd23f, 6, s * 0.95 - 0.1, 0.2), s * 0.9, -0.17, 1.33, 0.2, 0.02, 0.34)

def perritos():
    """El carrito de perritos calientes con su sombrilla."""
    acero = mat('acero_carrito', 0xd3d8de, 0.2)
    caja(acero, 0, 0, 0.35, 1.6, 0.85, 0.75)
    caja(mat('panel_carrito', 0xd8202a, 0.5), 0, -0.44, 0.45, 1.5, 0.02, 0.5)
    texto(mat('letras_carrito', 0xffd23f, 0.4), 'HOT DOGS', 0, -0.46, 0.72, tam=0.2, prof=0.02)
    caja(acero, 0, 0, 1.1, 1.65, 0.9, 0.06)
    for x in (-0.55, 0.55):
        cil(mat('olla', 0xaab2bc, 0.25), x, 0.05, 1.16, 0.18, 0.18, 14)
    for s in (-1, 1):
        rueda(s * 0.72, 0.25, 0.22, 0.12)
        cil(neumatico(), s * 0.6, -0.3, 0, 0.04, 0.35, 6)                 # patas
    cil(gris(), 0.0, 0.15, 1.16, 0.03, 1.15, 8)                          # el palo
    sombrilla = mat_franjas('sombrilla', 0xffd23f, 0xd8202a, 8, eje='X', z0=-1.1, alto=2.2)
    o = cil(sombrilla, 0.0, 0.15, 2.18, 1.05, 0.38, 16, r2=0.06)
    texto(mat('mostaza', 0xf2c23a, 0.4), 'NYC', 0, -0.47, 0.28, tam=0.12, prof=0.015)

def bici():
    """Repartidor en bici con la mochila cúbica, que viene de frente hacia el
    jugador (la rueda de delante en y = 0)."""
    cuadro = mat('cuadro_bici', 0x2f9a4a, 0.4)
    for y in (0.15, 1.25):
        bpy.ops.mesh.primitive_torus_add(major_radius=0.33, minor_radius=0.05, major_segments=24, minor_segments=6,
                                         location=(0, y, 0.38), rotation=(0, math.pi / 2, 0))
        from comun import _partes, _poner
        _poner(bpy.context.object, neumatico())
    rama(cuadro, (0, 0.15, 0.38), (0, 0.55, 0.85), 0.03, 0.03, 6)
    rama(cuadro, (0, 0.55, 0.85), (0, 1.25, 0.38), 0.03, 0.03, 6)
    rama(cuadro, (0, 0.55, 0.85), (0, 0.95, 0.85), 0.03, 0.03, 6)
    rama(cuadro, (0, 0.95, 0.85), (0, 1.25, 0.38), 0.03, 0.03, 6)
    rama(gris(), (-0.3, 0.2, 1.0), (0.3, 0.2, 1.0), 0.025, 0.025, 6)      # manillar
    rama(cuadro, (0, 0.15, 0.38), (0, 0.2, 1.0), 0.03, 0.03, 6)
    # el repartidor, inclinado hacia delante
    ropa = mat('ropa_repartidor', 0x2f9a4a, 0.6)
    rama(ropa, (0, 0.9, 0.95), (0, 0.55, 1.55), 0.2, 0.18, 10)            # tronco
    esfera(mat('piel_rep', 0xd9a77e, 0.6), 0, 0.45, 1.72, 0.16, 2)
    esfera(mat('casco', 0xff7a1a, 0.4), 0, 0.47, 1.8, 0.17, 2, mitad=True)
    for s in (-1, 1):
        rama(ropa, (s * 0.15, 0.6, 1.45), (s * 0.28, 0.22, 1.02), 0.06, 0.05, 6)   # brazos al manillar
        rama(mat('vaquero_rep', 0x3a4a6a, 0.6), (s * 0.1, 0.9, 0.95), (s * 0.12, 0.62, 0.62), 0.07, 0.06, 6)
        rama(mat('vaquero_rep', 0x3a4a6a, 0.6), (s * 0.12, 0.62, 0.62), (s * 0.12, 0.62, 0.3), 0.06, 0.05, 6)
    caja(mat('mochila_rep', 0xff7a1a, 0.5), 0, 0.98, 1.28, 0.55, 0.42, 0.55)   # la mochila cúbica
    texto(blanco(), 'FAST', 0, 0.76, 1.55, tam=0.11, prof=0.015)

def calabazas():
    """Calabazas de la feria del pueblo encima de una paca baja."""
    caja(mat('paja_baja', 0xe0c06a, 0.9), 0, 0.1, 0, 1.6, 0.6, 0.28)
    gajos = mat_franjas('calabaza', 0xff8a1a, 0xe8701a, 10, eje='X', z0=-1, alto=2)
    for x, y, r in ((-0.48, -0.05, 0.3), (0.12, 0.0, 0.36), (0.6, 0.12, 0.26), (-0.1, -0.35, 0.22)):
        z = 0.28 if y > -0.2 else 0
        esfera(gajos, x, y, z + r * 0.8, r, 2, esc=(1.15, 1.1, 0.85))
        rama(mat('rabito_calabaza', 0x4f7a2a, 0.6), (x, y, z + r * 1.45), (x + 0.04, y, z + r * 1.75), 0.04, 0.025, 6)

def vaca():
    """Una vaca frisona que cruza la calle (camina hacia +x, la cabeza delante)."""
    blanco_v = mat('blanco_vaca', 0xf6f4ee, 0.6)
    negro_v = mat('mancha_vaca', 0x1d1e22, 0.6)
    esfera(blanco_v, 0, 0, 1.0, 0.45, 3, esc=(1.9, 1.0, 0.95))            # el cuerpo
    for x, y, z, r in ((-0.35, -0.38, 1.1, 0.22), (0.35, 0.38, 0.95, 0.25), (-0.5, 0.36, 1.15, 0.2), (0.2, -0.42, 0.85, 0.18)):
        esfera(negro_v, x, y, z, r, 2, esc=(1.3, 0.25, 1))
    for x in (-0.55, 0.55):
        for y in (-0.22, 0.22):
            cil(blanco_v, x, y, 0, 0.09, 0.62, 8, r2=0.1)
            cil(negro_v, x, y, 0, 0.1, 0.08, 8)                           # pezuñas
    esfera(blanco_v, 0.95, 0, 1.25, 0.24, 2, esc=(1.3, 0.95, 1.0))        # la cabeza
    esfera(mat('hocico_vaca', 0xf2b6b0, 0.6), 1.22, 0, 1.18, 0.15, 2, esc=(0.9, 1.1, 0.8))
    for s in (-1, 1):
        esfera(negro_v, 1.05, s * 0.13, 1.33, 0.04, 1)                    # ojos (mirando de lado)
        rama(mat('cuerno', 0xf3ece0, 0.5), (0.95, s * 0.12, 1.45), (0.98, s * 0.25, 1.58), 0.04, 0.015, 6)
        esfera(blanco_v, 0.86, s * 0.25, 1.38, 0.08, 1, esc=(1, 1.6, 0.6))   # orejas
    esfera(mat('ubre', 0xf2b6b0, 0.6), -0.2, 0, 0.62, 0.17, 2)
    rama(blanco_v, (-0.85, 0, 1.2), (-0.98, 0, 0.7), 0.04, 0.03, 6)        # la cola
    esfera(negro_v, -0.98, 0, 0.66, 0.06, 1)
    cil(mat('cencerro', 0xd9a520, 0.3), 0.78, 0, 0.98, 0.07, 0.12, 8)

def calavera():
    """Calavera de vaca con cuernos sobre unas piedras del desierto."""
    piedra_c = mat('piedra_desierto', 0xb88a5a, 0.9)
    for x, y, r in ((-0.45, 0.05, 0.28), (0.4, 0.0, 0.3), (0.0, 0.18, 0.24), (0.7, 0.2, 0.18)):
        esfera(piedra_c, x, y, r * 0.55, r, 1, esc=(1.2, 1, 0.7))
    hueso = mat('hueso', 0xf3ece0, 0.6)
    esfera(hueso, 0, -0.05, 0.5, 0.22, 2, esc=(0.9, 0.8, 1.2))
    esfera(hueso, 0, -0.18, 0.3, 0.14, 2, esc=(0.8, 0.9, 1.0))            # el morro
    for s in (-1, 1):
        esfera(mat('cuenca', 0x2b2a2e, 0.8), s * 0.09, -0.22, 0.56, 0.06, 1)
        rama(hueso, (s * 0.16, 0, 0.66), (s * 0.55, 0, 0.75), 0.06, 0.04, 8)
        rama(hueso, (s * 0.55, 0, 0.75), (s * 0.68, 0, 0.98), 0.04, 0.015, 8)

def cartel_ruta():
    """Cartel verde de la autopista I-10 sobre el carril: se pasa agachado."""
    poste = mat('poste_autopista', 0x9aa3ad, 0.3)
    for s in (-1, 1):
        cil(poste, s * 0.95, 0, 0, 0.07, 2.3, 8)
        caja(gris(), s * 0.95, 0, 0, 0.3, 0.3, 0.08)
    caja(mat('verde_autopista', 0x1f6b3a, 0.5), 0, 0, 1.25, 1.96, 0.08, 0.8)
    caja(blanco(), 0, -0.045, 1.28, 1.86, 0.01, 0.74)
    caja(mat('verde_autopista', 0x1f6b3a, 0.5), 0, -0.05, 1.31, 1.8, 0.01, 0.68)
    # el escudo de la interestatal
    escudo = mat('azul_escudo', 0x2350c8, 0.4)
    cil(escudo, -0.6, -0.07, 1.65, 0.24, 0.02, 3, eje='Y')
    caja(rojo(), -0.6, -0.075, 1.83, 0.4, 0.01, 0.08)
    texto(blanco(), '10', -0.6, -0.09, 1.6, tam=0.18, prof=0.015)
    texto(blanco(), 'PHOENIX', 0.25, -0.07, 1.72, tam=0.17, prof=0.015)
    texto(blanco(), 'WEST', 0.25, -0.07, 1.48, tam=0.14, prof=0.015)

def elvis():
    """Imitador de Elvis con su traje blanco de estrella, el tupé, gafas de
    oro y el micrófono (en el juego baila)."""
    traje = mat('traje_elvis', 0xf8f6f0, 0.4)
    oro_e = mat('oro_elvis', 0xf2c23a, 0.2)
    piel = mat('piel_elvis', 0xe8b48e, 0.6)
    for s in (-1, 1):
        cil(traje, s * 0.13, 0, 0, 0.12, 0.95, 10, r2=0.09)               # pantalón de campana
        caja(negro(), s * 0.13, -0.05, 0, 0.16, 0.3, 0.08)
    cil(traje, 0, 0, 0.92, 0.27, 0.72, 14, r2=0.24)
    caja(oro_e, 0, 0, 0.92, 0.58, 0.58, 0.1)                              # el cinturón
    esfera(oro_e, 0, -0.29, 0.97, 0.08, 1)
    for k in range(6):
        esfera(oro_e, -0.15 + k * 0.06, -0.24, 1.3 + (k % 2) * 0.08, 0.025, 1)
    # cuello alto y la cabeza con el tupé
    cil(traje, 0, 0, 1.6, 0.16, 0.14, 12, r2=0.2)
    esfera(piel, 0, 0, 1.86, 0.17, 2, esc=(1, 0.95, 1.1))
    esfera(negro(), 0, 0.03, 1.98, 0.18, 2, esc=(1.05, 1.05, 0.7))
    esfera(negro(), 0, -0.1, 2.06, 0.11, 2, esc=(1.1, 1.3, 0.7))          # el tupé
    for s in (-1, 1):
        caja(oro_e, s * 0.07, -0.16, 1.88, 0.11, 0.03, 0.06)               # las gafas
        caja(negro(), s * 0.16, 0, 1.72, 0.04, 0.12, 0.22)                  # patillas
    # brazos: uno arriba con el micro, otro señalando
    rama(traje, (0.25, 0, 1.5), (0.5, -0.15, 1.85), 0.07, 0.06, 8)
    rama(traje, (0.5, -0.15, 1.85), (0.45, -0.25, 2.15), 0.06, 0.05, 8)
    cil(negro(), 0.45, -0.27, 2.12, 0.03, 0.18, 8)
    esfera(gris(), 0.45, -0.27, 2.32, 0.05, 1)
    rama(traje, (-0.25, 0, 1.5), (-0.55, -0.2, 1.3), 0.07, 0.06, 8)
    esfera(piel, -0.58, -0.22, 1.28, 0.06, 1)
    # la capa con el forro rojo
    caja(mat('capa_elvis', 0xd8202a, 0.5), 0, 0.22, 0.9, 0.62, 0.04, 0.75)

def cajas():
    """Cajas de documentos secretos con papeles encima («TOP SECRET»)."""
    carton = mat('carton_doc', 0xd9b382, 0.8)
    for x, y, z, g in ((-0.45, 0, 0, 0.1), (0.42, 0.05, 0, -0.08), (-0.05, 0.05, 0.4, 0.05)):
        caja(carton, x, y, z, 0.62, 0.45, 0.4, giro=g)
        caja(mat('tapa_doc', 0xc49c6a, 0.8), x, y, z + 0.38, 0.64, 0.47, 0.05, giro=g)
        texto(mat('sello_rojo', 0xd8202a, 0.5), 'TOP SECRET', x, y - 0.24, z + 0.2, tam=0.07, prof=0.01)
    papel = mat('papel', 0xf8f6f0, 0.7)
    for k, (x, y) in enumerate(((-0.1, -0.05), (0.05, 0.08), (0.12, -0.02))):
        caja(papel, x, y, 0.84 + k * 0.012, 0.28, 0.36, 0.008, giro=0.3 * k - 0.2)
    caja(mat('tachon', 0x1d1e22, 0.6), 0.12, -0.02, 0.88, 0.18, 0.04, 0.004, giro=0.2)


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
    'nopal':         (nopal,         'obstaculos', dict(lado=256, bisel=0.0)),
    'rodadora':      (rodadora,      'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
    'saguaro':       (saguaro,       'obstaculos', dict(lado=512, bisel=0.0)),
    'pickup':        (pickup,        'obstaculos', dict(lado=512)),
    'arco_neon':     (arco_neon,     'obstaculos', dict(lado=512, bisel=0.0)),
    'dado':          (dado,          'obstaculos', dict(lado=256, suelo=False)),
    'fichas':        (fichas,        'obstaculos', dict(lado=256, bisel=0.0)),
    'tragaperras':   (tragaperras,   'obstaculos', dict(lado=512)),
    'limusina':      (limusina,      'obstaculos', dict(lado=512)),
    'marquesina':    (marquesina,    'obstaculos', dict(lado=512, bisel=0.0)),
    'atril':         (atril,         'obstaculos', dict(lado=512, suelo=False)),
    'helicoptero':   (helicoptero,   'obstaculos', dict(lado=512, bisel=0.0, suelo=False)),
    'basura':       (basura,       'obstaculos', dict(lado=256, bisel=0.0)),
    'viga':         (viga,         'obstaculos', dict(lado=512, bisel=0.0)),
    'perritos':     (perritos,     'obstaculos', dict(lado=512)),
    'bici':         (bici,         'obstaculos', dict(lado=512, bisel=0.0)),
    'calabazas':    (calabazas,    'obstaculos', dict(lado=256, bisel=0.0)),
    'vaca':         (vaca,         'obstaculos', dict(lado=512, bisel=0.0)),
    'calavera':     (calavera,     'obstaculos', dict(lado=256, bisel=0.0)),
    'cartel_ruta':  (cartel_ruta,  'obstaculos', dict(lado=512, bisel=0.0)),
    'elvis':        (elvis,        'obstaculos', dict(lado=512, bisel=0.0)),
    'cajas':        (cajas,        'obstaculos', dict(lado=256)),
    'valla_policia': (valla_policia, 'publico',    dict(lado=256)),
    'verja':         (verja,         'publico',    dict(lado=256, bisel=0.0)),
}

correr(PIEZAS)
