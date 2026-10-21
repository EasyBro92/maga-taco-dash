# La ciudad en dibujo animado (21/10/2026). Ver comun.py.
#
#   blender -b -P blender/ciudad.py -- [pieza ...] [--rapido]
#
# Un centro de ciudad de EE. UU. de dibujos: tiendas de ladrillo con escalera
# de incendios y depósito de agua, torres de cristal, un rascacielos art déco,
# un diner, pisos de colores. En la acera: árboles, farolas, semáforo, boca de
# incendios, banco, buzón de correos; y coches aparcados.
#
# Fachadas: la fachada en y = 0 mirando a -y. Coches: el largo a lo largo de x.

import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import *

def marco():   return mat('marco', 0xffffff)
def hierro():  return mat('hierro', 0x2a2d33, 0.4)
def gris():    return mat('gris', 0x8f969f, 0.6)
def oscuro():  return mat('oscuro', 0x33363c, 0.7)
def cristal(): return mat('cristal', 0x2d4f86, 0.25)
def azotea():  return mat('azotea', 0x7d7f84, 0.9)
def neumatico(): return mat('neumatico', 0x1d1e21, 0.8)


def aire_acondicionado(x, y, z):
    caja(gris(), x, y, z, 0.6, 0.5, 0.4)
    cil(oscuro(), x, y - 0.26, z + 0.2, 0.15, 0.03, 12, eje='Y')

def deposito_agua(x, y, z):
    """El depósito de madera de los tejados de Nueva York."""
    madera = mat('madera_deposito', 0x8c5a36, 0.8)
    for dx, dy in ((-0.4, -0.4), (0.4, -0.4), (-0.4, 0.4), (0.4, 0.4)):
        cil(hierro(), x + dx, y + dy, z, 0.04, 0.9, 6)
    caja(hierro(), x, y, z + 0.85, 1.1, 1.1, 0.06)
    cil(madera, x, y, z + 0.9, 0.62, 1.1, 14)
    for k in (0.15, 0.55, 0.95):
        cil(hierro(), x, y, z + 0.9 + k, 0.635, 0.04, 14)
    cil(mat('tejadillo', 0x5b4a3e, 0.8), x, y, z + 2.0, 0.68, 0.45, 14, r2=0.04)

def escalera_incendios(x0, x1, y, pisos):
    """Rellanos con barandilla y tramos en diagonal entre ellos."""
    for i, z in enumerate(pisos):
        caja(hierro(), (x0 + x1) / 2, y - 0.4, z, x1 - x0, 0.8, 0.05)
        caja(hierro(), (x0 + x1) / 2, y - 0.79, z + 0.75, x1 - x0, 0.04, 0.04)
        caja(hierro(), (x0 + x1) / 2, y - 0.79, z + 0.35, x1 - x0, 0.03, 0.03)
        n = int((x1 - x0) / 0.22)
        for k in range(n + 1):
            caja(hierro(), x0 + k * (x1 - x0) / n, y - 0.79, z, 0.025, 0.025, 0.77)
        for s in (x0, x1):
            caja(hierro(), s, y - 0.4, z + 0.75, 0.04, 0.8, 0.04)
        if i + 1 < len(pisos):
            z2 = pisos[i + 1]
            for dy in (-0.2, -0.55):
                rama(hierro(), (x0 + 0.25, y + dy, z + 0.05), (x1 - 0.25, y + dy, z2), 0.025, 0.025, 4)
            for k in range(1, 8):
                t = k / 8
                caja(hierro(), x0 + 0.25 + (x1 - x0 - 0.5) * t, y - 0.375, z + 0.05 + (z2 - z - 0.05) * t,
                     0.12, 0.38, 0.025)


# ---------------------------------------------------------------- fachadas
def tienda(ladrillo, rotulo, color_rotulo, toldo1, toldo2):
    W, D, H = 5.0, 4.0, 4.6
    pared = mat_bloques(f'ladrillo{ladrillo:06x}', ladrillo, 0xe4dccd, ancho=0.25, alto=0.085, grosor=0.012)
    caja(pared, 0, D / 2, 0, W, D, H)
    caja(azotea(), 0, D / 2, H, W - 0.2, D - 0.2, 0.02)
    caja(mat('cornisa', 0xe8e2d4), 0, D / 2, H, W + 0.3, D + 0.3, 0.28)
    for k in range(17):
        caja(mat('cornisa', 0xe8e2d4), -2.4 + k * 0.3, -0.17, H - 0.12, 0.12, 0.12, 0.12)
    # planta baja: escaparate, puerta y rótulo
    caja(oscuro(), 0, -0.02, 0, W, 0.06, 0.3)
    caja(mat('escaparate', 0x6fa6d8, 0.15), -0.6, -0.03, 0.3, 3.0, 0.04, 1.1)
    caja(marco(), -0.6, -0.06, 0.3, 3.1, 0.04, 0.06)
    for k in (-2.1, -1.1, -0.1, 0.9):
        caja(marco(), k, -0.06, 0.3, 0.06, 0.04, 1.1)
    puerta(1.6, 0.0, 0.75, 1.35, color=0x2b5f3a)
    caja(mat(f'rotulo{color_rotulo:06x}', color_rotulo, 0.5), 0, -0.08, 1.48, W - 0.2, 0.1, 0.42)
    texto(marco(), rotulo, 0, -0.13, 1.69, tam=0.32, prof=0.05)
    caja(mat_franjas(f'toldo{toldo1:06x}', toldo1, toldo2, 10, eje='X', z0=-2.2, alto=3.2),
         -0.6, -0.45, 1.05, 3.2, 0.9, 0.05, inclina=-0.45)
    # dos plantas de ventanas y la escalera de incendios
    for z in (2.15, 3.55):
        for x in (-1.6, 0.0, 1.6):
            ventana(x, z, 0.6, 0.85, remate='cornisa')
    escalera_incendios(-2.2, -0.3, 0.0, [2.05, 3.45])
    deposito_agua(1.2, 2.6, H + 0.02)
    aire_acondicionado(-1.4, 2.8, H + 0.02)

def oficina(nombre_vidrio, vidrio, H):
    W, D = 5.0, 4.0
    caja(mat('granito', 0x3f4248, 0.4), 0, D / 2, 0, W, D, 1.7)
    caja(mat('vestibulo', 0x9fd3f0, 0.15), 0, -0.02, 0.0, 3.6, 0.06, 1.5)
    for k in range(7):
        caja(gris(), -1.8 + k * 0.6, -0.06, 0, 0.06, 0.06, 1.5)
    caja(gris(), 0, -0.5, 1.5, 3.8, 1.0, 0.12)                         # marquesina
    cil(mat('puerta_giratoria', 0xbfe3f5, 0.1), 0, -0.25, 0, 0.45, 1.4, 16)
    fach = mat_ventanas(nombre_vidrio, vidrio, 0xd6dde4, paso_x=0.62, paso_z=1.05, hueco_x=0.54, hueco_z=0.8, variacion=1.3)
    caja(fach, 0, D / 2, 1.7, W, D, H - 1.7)
    for x in (-W / 2, W / 2):                                         # aristas de aluminio
        for y in (0, D):
            caja(gris(), x, y, 1.7, 0.14, 0.14, H - 1.7)
    caja(gris(), 0, D / 2, H, W + 0.15, D + 0.15, 0.25)
    caja(fach, 0, D / 2 + 0.3, H + 0.25, W * 0.66, D * 0.66, 1.3)
    caja(gris(), 0, D / 2 + 0.3, H + 1.55, W * 0.66 + 0.1, D * 0.66 + 0.1, 0.18)
    cil(gris(), 0.8, D / 2 + 0.3, H + 1.73, 0.06, 2.2, 6, r2=0.03)
    esfera(mat('baliza', 0xff3b3b, 0.3), 0.8, D / 2 + 0.3, H + 3.95, 0.09, 1)
    aire_acondicionado(-1.5, D / 2 + 1.2, H + 0.25)

def artdeco():
    W, D = 6.0, 4.5
    crema = 0xf1d9a6
    fach = mat_ventanas('deco_ventanas', 0x2f4a6e, crema, paso_x=0.75, paso_z=1.0, hueco_x=0.36, hueco_z=0.62, variacion=1.5)
    oro = mat('oro', 0xe0a93a, 0.35)
    caja(mat('deco_base', 0x8a3b2e, 0.6), 0, D / 2, 0, W, D, 1.6)       # zócalo granate
    caja(mat('portal', 0x1f2a3a, 0.4), 0, -0.03, 0, 1.6, 0.06, 1.4)
    caja(oro, 0, -0.08, 1.4, 2.0, 0.12, 0.25)
    fronton(oro, 0, -0.1, 1.65, 2.0, 0.6, 0.1)
    for s in (-1, 1):
        cil(oro, s * 1.15, -0.1, 0, 0.1, 1.65, 8)
    texto(mat('letra_oro', 0xe0a93a, 0.35), 'HOTEL', 0, -0.06, 2.6, tam=0.5, prof=0.06)
    tramos = [(W, D, 1.6, 8.0), (W * 0.74, D * 0.74, 9.6, 3.0), (W * 0.5, D * 0.5, 12.6, 2.0)]
    for w, d, z, h in tramos:
        caja(fach, 0, D / 2, z, w, d, h)
        caja(oro, 0, D / 2, z + h, w + 0.12, d + 0.12, 0.14)
        for k in range(int(w / 0.75) + 1):                              # pilastras que suben
            x = -w / 2 + k * w / int(w / 0.75)
            caja(mat('pilastra', 0xf6e6c2), x, D / 2 - d / 2 - 0.04, z, 0.14, 0.1, h)
    # la corona escalonada y la aguja
    z = 14.74
    for i, r in enumerate((1.1, 0.8, 0.5)):
        caja(mat('pilastra', 0xf6e6c2), 0, D / 2, z + i * 0.5, r * 2, r * 2, 0.5)
        caja(oro, 0, D / 2, z + i * 0.5 + 0.45, r * 2 + 0.1, r * 2 + 0.1, 0.07)
    cil(oro, 0, D / 2, z + 1.5, 0.22, 2.4, 8, r2=0.0)

def diner():
    W, D, H = 6.5, 3.5, 2.6
    acero = mat('acero', 0xd3dbe2, 0.25)
    rojo = mat('rojo_diner', 0xd63a3a, 0.4)
    caja(acero, 0, D / 2, 0, W, D, H)
    for s in (-1, 1):                                                   # los extremos redondeados
        cil(acero, s * W / 2, D / 2, 0, D / 2, H, 20)
    caja(rojo, 0, -0.02, 0.35, W, 0.06, 0.18)
    caja(rojo, 0, -0.02, 2.0, W, 0.06, 0.18)
    caja(mat('ventanal', 0x9fd3f0, 0.15), 0, -0.03, 0.75, W - 1.4, 0.04, 1.05)
    for k in range(9):
        caja(acero, -2.55 + k * 0.64, -0.06, 0.75, 0.07, 0.04, 1.05)
    caja(mat('tejado_diner', 0xf3efe6), 0, D / 2, H, W + 0.4, D + 0.4, 0.14)
    # el gran letrero de neón encima
    caja(hierro(), 0, 0.5, H + 0.14, 3.6, 0.12, 0.08)
    for s in (-1, 1):
        caja(hierro(), s * 1.5, 0.5, H + 0.14, 0.08, 0.08, 0.5)
    caja(mat('letrero', 0x1f3c88, 0.4), 0, 0.45, H + 0.6, 3.8, 0.14, 1.0)
    texto(mat('neon', 0xff5fa8, 0.2), 'DINER', 0, 0.38, H + 1.1, tam=0.7, prof=0.08)
    caja(mat('neon2', 0xffe14a, 0.2), 0, 0.37, H + 0.66, 3.6, 0.03, 0.06)
    caja(mat('neon2', 0xffe14a, 0.2), 0, 0.37, H + 1.48, 3.6, 0.03, 0.06)
    puerta(2.2, 0.15, 0.8, 1.6, color=0xd63a3a, marco=acero)
    escalinata(acero, 2.2, 0, 0, 1.2, 2, huella=0.2, tabica=0.08)
    caja(mat('acera_diner', 0xc9c3b6, 0.9), 0, -0.6, 0, W + 2.6, 1.2, 0.03)
    for x in (-2.0, -0.6, 0.8):                                          # mesitas fuera
        cil(rojo, x, -0.65, 0, 0.04, 0.7, 6)
        cil(acero, x, -0.65, 0.7, 0.32, 0.05, 14)
        cil(mat('sombrilla', 0xfff1d0, 0.6), x, -0.65, 0.75, 0.04, 1.0, 6)
        cil(rojo, x, -0.65, 1.7, 0.75, 0.3, 12, r2=0.05)

def apartamentos(color, nombre):
    W, D, H = 4.6, 4.0, 7.0
    estuco = mat_bloques(f'estuco{color:06x}', color, color, ancho=0.9, alto=0.3, grosor=0.0, mezcla=1.0)
    caja(estuco, 0, D / 2, 0, W, D, H)
    caja(marco(), 0, D / 2, H, W + 0.3, D + 0.3, 0.22)
    caja(marco(), 0, D / 2, 1.3, W + 0.06, D + 0.06, 0.1)
    # mirador central de arriba abajo
    caja(estuco, 0, -0.25, 1.4, 1.7, 0.55, H - 1.7)
    caja(marco(), 0, -0.27, H - 0.3, 1.85, 0.62, 0.12)
    pisos = [1.65, 3.0, 4.35, 5.7]
    for z in pisos:
        ventana(0, z, 0.9, 0.85, y=-0.52)
        for s in (-1, 1):
            ventana(s * 1.65, z, 0.6, 0.85)
    for z in pisos[1::2]:                                                # balcones
        for s in (-1, 1):
            caja(marco(), s * 1.65, -0.3, z - 0.1, 1.0, 0.6, 0.08)
            caja(hierro(), s * 1.65, -0.58, z + 0.55, 1.0, 0.03, 0.04)
            for k in range(6):
                caja(hierro(), s * 1.65 - 0.45 + k * 0.18, -0.58, z - 0.02, 0.025, 0.025, 0.58)
            esfera(mat('maceta', 0x4caf50, 0.8), s * 1.65 + 0.3, -0.4, z + 0.2, 0.17, 1)
    puerta(0, 0.0, 0.8, 1.15, color=0x22314f)
    escalinata(mat('piedra_gris', 0xb8b2a6, 0.8), 0, 0, 0, 1.2, 2, huella=0.18, tabica=0.07)
    for s in (-1, 1):
        ventana(s * 1.65, 0.4, 0.6, 0.65)
    aire_acondicionado(1.2, 2.6, H + 0.22)
    caja(oscuro(), -1.3, 2.8, H + 0.22, 0.7, 0.7, 0.9)                   # salida a la azotea


# ---------------------------------------------------------------- acera y calle
def arbol_ciudad():
    caja(hierro(), 0, 0, 0, 1.0, 1.0, 0.04)
    caja(mat('tierra', 0x6b4e3a, 1.0), 0, 0, 0, 0.8, 0.8, 0.05)
    tronco = mat('tronco', 0x6b4a2f, 0.9)
    rama(tronco, (0, 0, 0), (0.05, 0, 1.4), 0.12, 0.09)
    rama(tronco, (0.03, 0, 1.1), (0.4, 0.2, 1.8), 0.06, 0.04, 6)
    rama(tronco, (0.03, 0, 1.2), (-0.35, -0.2, 1.9), 0.06, 0.04, 6)
    verdes = [mat('hoja1', 0x4caf50, 0.8), mat('hoja2', 0x3d9a45, 0.8), mat('hoja3', 0x6cc04a, 0.8)]
    for i, (x, y, z, r) in enumerate(((0, 0, 2.2, 0.75), (0.5, 0.2, 1.95, 0.55), (-0.45, -0.15, 2.05, 0.55),
                                      (0.1, -0.4, 2.0, 0.5), (-0.1, 0.35, 2.6, 0.5), (0.25, 0.0, 2.75, 0.42))):
        esfera(verdes[i % 3], x, y, z, r, 2, esc=(1, 1, 0.85))

def farola_ciudad():
    poste = mat('poste', 0x5d646c, 0.4)
    cil(poste, 0, 0, 0, 0.13, 0.25, 10, r2=0.09)
    cil(poste, 0, 0, 0.25, 0.07, 3.0, 8, r2=0.05)
    rama(poste, (0, 0, 3.2), (0.35, 0, 3.55), 0.045, 0.04, 6)
    rama(poste, (0.35, 0, 3.55), (0.95, 0, 3.6), 0.04, 0.035, 6)
    esfera(poste, 1.1, 0, 3.58, 0.26, 2, esc=(1.4, 0.8, 0.5))
    esfera(mat('foco', 0xfff3c4, 0.2), 1.1, 0, 3.5, 0.2, 2, esc=(1.3, 0.7, 0.35))

def semaforo():
    amarillo = mat('semaforo', 0xf2c230, 0.4)
    cil(hierro(), 0, 0, 0, 0.12, 0.2, 10)
    cil(hierro(), 0, 0, 0.2, 0.065, 3.1, 8)
    caja(amarillo, 0, -0.12, 2.05, 0.38, 0.3, 1.05)
    for i, c in enumerate((0xff3b3b, 0xffce3d, 0x4caf50)):
        z = 2.82 - i * 0.33
        cil(oscuro(), 0, -0.27, z, 0.15, 0.04, 12, eje='Y')
        esfera(mat(f'luz{c:06x}', c, 0.2), 0, -0.29, z, 0.11, 1, esc=(1, 0.5, 1))
        caja(amarillo, 0, -0.36, z + 0.1, 0.3, 0.18, 0.03, inclina=0.3)
    caja(oscuro(), 0.12, -0.08, 1.2, 0.3, 0.2, 0.3)                       # el muñequito de cruzar
    caja(mat('peaton', 0xffffff, 0.3), 0.12, -0.185, 1.25, 0.12, 0.01, 0.18)
    caja(mat('cartel_calle', 0x1d7a3e, 0.5), 0.45, 0, 3.2, 1.0, 0.04, 0.24)
    texto(marco(), 'MAGA AVE', 0.45, -0.02, 3.32, tam=0.14, prof=0.02)

def hidrante():
    rojo = mat('hidrante', 0xd8322f, 0.4)
    cil(rojo, 0, 0, 0, 0.17, 0.08, 10)
    cil(rojo, 0, 0, 0.08, 0.12, 0.45, 10)
    cil(mat('tapa_hidrante', 0xf2c230, 0.4), 0, 0, 0.53, 0.14, 0.06, 10)
    esfera(rojo, 0, 0, 0.59, 0.12, 2, mitad=True)
    for s in (-1, 1):
        cil(rojo, s * 0.15, 0, 0.36, 0.05, 0.1, 8, eje='X')
    cil(rojo, 0, -0.14, 0.36, 0.065, 0.1, 8, eje='Y')

def banco():
    madera = mat('madera_banco', 0x9c6b3c, 0.8)
    for i in range(3):
        caja(madera, 0, -0.15 + i * 0.12, 0.42, 1.4, 0.1, 0.05)
    for i in range(2):
        caja(madera, 0, 0.17, 0.6 + i * 0.16, 1.4, 0.05, 0.1, inclina=-0.15)
    for s in (-1, 1):
        caja(hierro(), s * 0.6, 0, 0, 0.06, 0.45, 0.42)
        caja(hierro(), s * 0.6, 0.17, 0.42, 0.06, 0.06, 0.45)
        caja(hierro(), s * 0.6, -0.05, 0.58, 0.06, 0.42, 0.05)

def buzon():
    azul = mat('buzon', 0x1f4fa0, 0.45)
    for s in (-1, 1):
        for t in (-1, 1):
            caja(azul, s * 0.2, t * 0.18, 0, 0.06, 0.06, 0.25)
    caja(azul, 0, 0, 0.25, 0.5, 0.45, 0.65)
    cil(azul, 0, 0, 0.9, 0.25, 0.45, 16, eje='Y')
    caja(mat('ranura', 0x15161a), 0, -0.23, 0.95, 0.32, 0.02, 0.06)
    caja(mat('pegatina', 0xffffff, 0.4), 0, -0.235, 0.55, 0.3, 0.01, 0.16)
    caja(mat('aguila', 0xd8283a, 0.4), 0, -0.24, 0.6, 0.12, 0.01, 0.07)

def coche(color, taxi=False):
    """Coche de dibujos, el largo a lo largo de x."""
    chapa = mat(f'chapa{color:06x}', color, 0.3)
    caja(chapa, 0, 0, 0.22, 2.2, 1.0, 0.45)
    caja(chapa, -0.1, 0, 0.67, 1.25, 0.9, 0.42)
    vid = mat('luna', 0x2d4f86, 0.15)
    caja(vid, -0.1, 0, 0.71, 1.28, 0.92, 0.32)
    caja(chapa, -0.1, 0, 0.71, 0.08, 0.95, 0.34)                         # pilar central
    for x in (-0.72, 0.72):
        for y in (-0.48, 0.48):
            cil(neumatico(), x, y, 0.24, 0.24, 0.16, 14, eje='Y')
            cil(mat('llanta', 0xd3d6da, 0.3), x, y * 1.18, 0.24, 0.12, 0.02, 10, eje='Y')
    for y in (-0.33, 0.33):
        caja(mat('faro', 0xfff6d8, 0.2), 1.1, y, 0.42, 0.04, 0.22, 0.12)
        caja(mat('piloto', 0xc0262c, 0.3), -1.1, y, 0.42, 0.04, 0.22, 0.12)
    caja(gris(), 1.12, 0, 0.2, 0.08, 1.02, 0.1)
    caja(gris(), -1.12, 0, 0.2, 0.08, 1.02, 0.1)
    if taxi:
        caja(mat_franjas('cuadros', 0x111111, 0xffffff, 12, eje='X', z0=-1.1, alto=2.2), 0, 0, 0.5, 2.22, 1.02, 0.08)
        caja(mat('cartel_taxi', 0xfff3b0, 0.3), -0.1, 0, 1.09, 0.5, 0.22, 0.16)


def tienda_roja():   tienda(0xb5523b, 'PIZZA', 0x2b6b3a, 0xd8322f, 0xffffff)
def tienda_crema():  tienda(0xd9b98c, 'TACOS', 0xd8322f, 0x2b9a4a, 0xffffff)
def oficina_azul():  oficina('vidrio_azul', 0x3f7fc4, 12.5)
def oficina_verde(): oficina('vidrio_verde', 0x3aa38f, 10.0)
def apart_morado():  apartamentos(0xb48fd6, 'morado')
def apart_naranja(): apartamentos(0xffa86b, 'naranja')
def taxi():          coche(0xf4c430, taxi=True)
def coche_rojo():    coche(0xd8322f)
def coche_azul():    coche(0x2a6fd6)

PIEZAS = {
    'tienda_roja':    (tienda_roja,   'ciudad', dict(lado=1024)),
    'tienda_crema':   (tienda_crema,  'ciudad', dict(lado=1024)),
    'oficina_azul':   (oficina_azul,  'ciudad', dict(lado=1024)),
    'oficina_verde':  (oficina_verde, 'ciudad', dict(lado=1024)),
    'artdeco':        (artdeco,       'ciudad', dict(lado=1024)),
    'diner':          (diner,         'ciudad', dict(lado=1024)),
    'apart_morado':   (apart_morado,  'ciudad', dict(lado=1024)),
    'apart_naranja':  (apart_naranja, 'ciudad', dict(lado=1024)),
    'arbol_ciudad':   (arbol_ciudad,  'ciudad', dict(lado=512, bisel=0.0)),
    'farola_ciudad':  (farola_ciudad, 'ciudad', dict(lado=256, bisel=0.0)),
    'semaforo':       (semaforo,      'ciudad', dict(lado=256, bisel=0.01)),
    'hidrante':       (hidrante,      'ciudad', dict(lado=256, bisel=0.0)),
    'banco':          (banco,         'ciudad', dict(lado=256, bisel=0.0)),
    'buzon':          (buzon,         'ciudad', dict(lado=256, bisel=0.02)),
    'taxi':           (taxi,          'ciudad', dict(lado=512, bisel=0.04)),
    'coche_rojo':     (coche_rojo,    'ciudad', dict(lado=512, bisel=0.04)),
    'coche_azul':     (coche_azul,    'ciudad', dict(lado=512, bisel=0.04)),
}

correr(PIEZAS)
