# Nivel 22: Nashville, Tennessee (14/11/2026).
#
#   blender -b -P blender/nashville.py -- [pieza ...] [--rapido]
#
# Historia: «Música country. Llega a la meta bailando el YMCA».
#   Por Broadway al atardecer (el arco de «Music City», el auditorio Ryman, el
#   edificio «Batman», un honky-tonk con su guitarra de neón) entre parejas
#   que bailan en línea de lado a lado; dentro del Grand Ole Opry el escenario
#   es el mástil de una guitarra gigante y hay que pisar las notas que
#   brillan; y se llega al Partenón de Nashville, donde baila el YMCA.
# Obstáculos (carpeta obstaculos): el bailarín vaquero, la nota del mástil,
# el amplificador, la bota vaquera, la batería y la pancarta de Music City.

import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import *
from comun import _poner

def blanco():   return mat('blanco_nv', 0xf4f0e8, 0.5)
def negro():    return mat('negro_nv', 0x1b1c20, 0.4)
def hierro():   return mat('hierro_nv', 0x3a3e44, 0.5)
def rojo():     return mat('rojo_nv', 0xc8282c, 0.45)
def oro():      return mat('oro_nv', 0xe8b840, 0.25)
def madera():   return mat('madera_nv', 0x8a5a32, 0.6)
def cuero():    return mat('cuero_nv', 0x7a4a26, 0.55)
def piel():     return mat('piel_nv', 0xe8b89a, 0.6)
def vaquero():  return mat('tela_vaquera', 0x3a5a8a, 0.8)
def piedra():   return mat_bloques('piedra_nv', 0xd8ccb0, 0xb8aa8c, ancho=1.6, alto=0.8)
def ladrillo(): return mat_bloques('ladrillo_nv', 0x9a4a36, 0x6e3426, ancho=0.5, alto=0.22)
def neon_rosa():  return luz('neon_rosa_nv', 0xff4a9a, 2.0)
def neon_azul():  return luz('neon_azul_nv', 0x4ac8ff, 2.0)
def neon_ambar(): return luz('neon_ambar_nv', 0xffc040, 2.0)
def bombilla():   return luz('bombilla_nv', 0xffe08a, 1.8)

def guitarra(m, x, y, z, alto=4.0, borde=None):
    """Una guitarra de pie (silueta): la caja en ocho, la boca, el mástil y
    la pala. (x, y) el centro y z la base; mira a -y."""
    k = alto / 4.0
    esfera(m, x, y, z + 0.8 * k, 0.8 * k, 2, esc=(1, 0.22, 1))
    esfera(m, x, y, z + 1.75 * k, 0.6 * k, 2, esc=(1, 0.22, 1))
    cil(negro(), x, y - 0.14 * k, z + 1.45 * k, 0.22 * k, 0.05, 16, eje='Y')
    caja(borde or madera(), x, y - 0.05 * k, z + 2.2 * k, 0.22 * k, 0.1 * k, 1.4 * k)
    caja(borde or madera(), x, y - 0.05 * k, z + 3.6 * k, 0.34 * k, 0.1 * k, 0.4 * k)

# ================================================================ edificios
def partenon():
    """El Partenón de Nashville (la meta): la réplica a tamaño real del de
    Atenas en Centennial Park: gradas, ocho columnas dóricas al frente, el
    friso y el frontón; delante, el escenario redondo donde se baila."""
    Y = 22
    p = piedra()
    W, D = 34.0, 30.0
    for k in range(3):
        caja(p, 0, Y, k * 0.5, W + 3 - k, D + 3 - k, 0.5)
    Z0 = 1.5
    for i in range(8):                                   # las ocho del frente
        x = -W / 2 + 1.2 + i * (W - 2.4) / 7
        cil(p, x, Y - D / 2 + 1.2, Z0, 1.05, 10.5, 16, r2=0.85)
        caja(p, x, Y - D / 2 + 1.2, Z0 + 10.5, 2.5, 2.5, 0.5)
    for s in (-1, 1):                                    # las de los lados
        for j in range(1, 8):
            cil(p, s * (W / 2 - 1.2), Y - D / 2 + 1.2 + j * 3.9, Z0, 1.05, 10.5, 12, r2=0.85)
    caja(mat('cella_nv', 0xc8b894, 0.8), 0, Y + 1.5, Z0, W - 7, D - 8, 10.5)
    caja(mat('puerta_part', 0x5a3a22, 0.5), 0, Y - D / 2 + 3.9, Z0, 4.5, 0.3, 7.5)
    caja(p, 0, Y, Z0 + 11.0, W, D, 1.6)                  # el entablamento
    for i in range(22):                                  # los triglifos
        caja(mat('triglifo_nv', 0xb09a78, 0.8), -W / 2 + 0.8 + i * (W - 1.6) / 21, Y - D / 2 - 0.05, Z0 + 11.4, 0.5, 0.1, 0.9)
    fronton(p, 0, Y - D / 2, Z0 + 12.6, W + 0.6, 4.6, D)
    fronton(mat('timpano_nv', 0xb8a888, 0.8), 0, Y - D / 2 - 0.06, Z0 + 12.9, W - 4, 3.6, 0.1)
    for (x, h) in ((-6, 1.6), (-3, 2.4), (0, 3.0), (3, 2.4), (6, 1.6)):      # las figuras del tímpano
        cil(blanco(), x, Y - D / 2 - 0.3, Z0 + 12.9, 0.35, h * 0.8, 8)
        esfera(blanco(), x, Y - D / 2 - 0.3, Z0 + 12.9 + h * 0.8 + 0.3, 0.32, 1)
    # El escenario redondo de delante, con sus focos y el cartel.
    cil(oro(), 0, Y - D / 2 - 14, 0, 7.5, 0.04, 32)
    cil(mat('tarima_nv', 0x6a4a2e, 0.6), 0, Y - D / 2 - 14, 0.04, 7.2, 0.02, 32)
    for k in range(20):
        a = k * math.tau / 20
        esfera(bombilla(), math.cos(a) * 7.3, Y - D / 2 - 14 + math.sin(a) * 7.3, 0.14, 0.13, 1)
    for s in (-1, 1):
        cil(hierro(), s * 9.5, Y - D / 2 - 6, 0, 0.18, 8, 8)
        caja(negro(), s * 9.5, Y - D / 2 - 6.3, 8, 1.6, 0.8, 0.8)
        caja(luz('foco_part', 0xfff0c0, 2.0), s * 9.5, Y - D / 2 - 6.75, 8.1, 1.2, 0.06, 0.6)
    caja(negro(), 0, Y - D / 2 - 5.2, 0, 13, 0.4, 2.4)
    texto(neon_ambar(), 'Y  M  C  A', 0, Y - D / 2 - 5.45, 1.25, tam=1.5, prof=0.08)

def ryman():
    """El auditorio Ryman, «la iglesia madre del country»: ladrillo rojo, el
    gran hastial, las ventanas ojivales con sus marcos blancos y el letrero."""
    Y = 11
    L = ladrillo()
    caja(L, 0, Y, 0, 30, 20, 13)
    hastial(L, 0, Y - 10, Y + 10, 13, 30, 7.5)
    tejado(mat('tejado_ryman', 0x4a4a52, 0.7), 0, Y - 10, Y + 10, 13, 30, 7.5)
    b = blanco()
    cr = mat('vidriera_nv', 0x3a5a7a, 0.2)
    for x in (-11.5, -7, 7, 11.5):                       # las ojivales de dos alturas
        for z in (1.4, 7.4):
            caja(b, x, Y - 10.05, z, 2.4, 0.16, 3.6)
            caja(cr, x, Y - 10.12, z + 0.15, 2.0, 0.06, 3.3)
            fronton(b, x, Y - 10.13, z + 3.6, 2.4, 1.5, 0.16)
            fronton(cr, x, Y - 10.2, z + 3.6, 1.9, 1.15, 0.06)
    for x in (-3.2, 0, 3.2):                             # las tres del centro
        caja(b, x, Y - 10.05, 7.0, 2.2, 0.16, 5.0)
        caja(cr, x, Y - 10.12, 7.15, 1.8, 0.06, 4.7)
        fronton(b, x, Y - 10.13, 12.0, 2.2, 1.6, 0.16)
        fronton(cr, x, Y - 10.2, 12.0, 1.7, 1.2, 0.06)
    cil(b, 0, Y - 10.1, 17.0, 1.5, 0.16, 20, eje='Y')    # el rosetón
    cil(cr, 0, Y - 10.2, 17.0, 1.2, 0.08, 20, eje='Y')
    for x in (-3.2, 0, 3.2):                             # las puertas
        caja(b, x, Y - 10.05, 0, 2.6, 0.16, 4.2)
        caja(mat('puerta_ryman', 0x5a2a1e, 0.6), x, Y - 10.12, 0, 2.2, 0.06, 3.6)
        fronton(b, x, Y - 10.13, 4.2, 2.6, 1.2, 0.16)
    caja(b, 0, Y - 10.1, 5.6, 16, 0.14, 1.2)
    texto(negro(), 'RYMAN AUDITORIUM', 0, Y - 10.2, 6.2, tam=0.95, prof=0.05)
    for s in (-1, 1):
        caja(L, s * 14.5, Y - 9.6, 0, 1.6, 1.6, 15.5)
        cil(mat('tejado_ryman', 0x4a4a52, 0.7), s * 14.5, Y - 9.6, 15.5, 1.3, 2.4, 4, r2=0.02)

def batman_building():
    """El «edificio Batman» (la torre de AT&T): cristal azul oscuro, el cuerpo
    que se estrecha arriba y las dos agujas como las orejas de la máscara."""
    Y = 14
    c = mat_ventanas('cristal_batman', 0x2a4a6a, 0x1e2a3a, paso_x=1.5, paso_z=1.9, hueco_x=1.2, hueco_z=1.5)
    g = mat('granito_batman', 0x5a5450, 0.6)
    caja(g, 0, Y, 0, 26, 22, 7)
    caja(mat('entrada_batman', 0x1e2a3a, 0.2), 0, Y - 11.05, 0, 9, 0.1, 5.5)
    caja(c, 0, Y, 7, 22, 18, 58)
    for s in (-1, 1):                                    # los hombros
        caja(g, s * 10.2, Y, 7, 1.8, 18.4, 60)
        caja(c, s * 8.2, Y, 65, 5.6, 18, 9)
        caja(g, s * 9.0, Y, 74, 4.0, 4.0, 3)
        cil(hierro(), s * 9.0, Y, 77, 0.9, 20, 8, r2=0.08)   # las orejas
    caja(c, 0, Y, 65, 10.8, 15, 5)                       # la frente (más baja: la máscara)
    caja(g, 0, Y - 9.1, 62, 22, 0.3, 1.2)
    for k in range(6):
        caja(mat('raya_batman', 0x8a9aaa, 0.3), 0, Y - 9.06, 12 + k * 9, 22, 0.1, 0.35)

def honky_tonk():
    """Un honky-tonk de Broadway: tres plantas de ladrillo, los balcones con
    gente, la guitarra gigante de neón, la bota y los letreros."""
    Y = 8
    L = mat_bloques('ladrillo_honky', 0x7a3a2a, 0x54281e, ancho=0.5, alto=0.22)
    caja(L, 0, Y, 0, 20, 14, 15)
    caja(mat('cornisa_honky', 0xd8c49c, 0.6), 0, Y - 7.2, 15, 20.6, 0.8, 0.9)
    cr = luz('ventana_honky', 0xffc878, 0.9)
    for z in (5.6, 10.4):
        for x in (-7.2, -2.4, 2.4, 7.2):
            ventana(x, z, 2.2, 3.0, y=Y - 7, marco=blanco(), cristal=cr)
        caja(hierro(), 0, Y - 8.0, z - 0.3, 19.6, 1.8, 0.14)          # el balcón
        for k in range(28):
            cil(hierro(), -9.6 + k * 0.71, Y - 8.85, z - 0.2, 0.035, 1.0, 4)
        caja(hierro(), 0, Y - 8.85, z + 0.8, 19.6, 0.08, 0.08)
    # La planta baja: puertas abiertas y el toldo.
    caja(luz('bar_dentro', 0xffb060, 1.0), 0, Y - 7.05, 0.2, 15, 0.1, 3.6)
    for x in (-5, 0, 5):
        caja(mat('puerta_honky', 0x4a2a1a, 0.6), x, Y - 7.12, 0.2, 0.3, 0.1, 3.6)
    caja(rojo(), 0, Y - 8.4, 4.0, 20, 2.8, 0.3, inclina=-0.25)
    caja(negro(), 0, Y - 7.3, 4.6, 14, 0.3, 1.5)
    texto(neon_rosa(), 'HONKY TONK', 0, Y - 7.55, 5.35, tam=1.15, prof=0.08)
    # La guitarra gigante de neón, de canto en la esquina, y la bota.
    caja(negro(), -8.2, Y - 8.6, 7.2, 0.5, 3.2, 10.5)
    for s in (-1, 1):
        o = texto(neon_ambar(), 'LIVE', -8.2 + s * 0.27, Y - 8.6, 16.6, tam=0.9, prof=0.05)
        o.rotation_euler = (math.pi / 2, 0, s * math.pi / 2)
        o = texto(neon_azul(), 'MUSIC', -8.2 + s * 0.27, Y - 8.6, 15.5, tam=0.75, prof=0.05)
        o.rotation_euler = (math.pi / 2, 0, s * math.pi / 2)
    guitarra(neon_ambar(), 8.0, Y - 7.6, 7.2, alto=7.0, borde=neon_rosa())
    for k in range(34):
        esfera(bombilla(), -9.8 + k * 0.6, Y - 7.7, 14.7, 0.09, 1)

# ================================================================ cruzan la calle
def arco_broadway():
    """El arco de neón sobre Broadway: «MUSIC CITY» con una guitarra a cada
    lado y sus bombillas."""
    for s in (-1, 1):
        caja(hierro(), s * 9, 0, 0, 0.6, 0.6, 9.4)
        guitarra(neon_rosa(), s * 9, -0.45, 3.0, alto=4.4, borde=neon_azul())
    caja(hierro(), 0, 0, 6.2, 18.6, 0.5, 0.4)
    caja(hierro(), 0, 0, 9.0, 18.6, 0.5, 0.4)
    caja(negro(), 0, 0, 6.6, 17, 0.3, 2.4)
    texto(neon_ambar(), 'MUSIC CITY', 0, -0.2, 7.5, tam=1.5, prof=0.08)
    texto(neon_azul(), 'NASHVILLE', 0, -0.2, 6.85, tam=0.5, prof=0.05)
    o = texto(neon_ambar(), 'MUSIC CITY', 0, 0.2, 7.5, tam=1.5, prof=0.08); o.rotation_euler = (math.pi / 2, 0, math.pi)
    for k in range(30):
        esfera(bombilla(), -8.4 + k * 0.58, -0.22, 9.45, 0.08, 1)

def opry():
    """El Grand Ole Opry por dentro (momento estrella): el escenario es el
    mástil de una guitarra gigante (palosanto, trastes de metal cada 7 m, los
    puntos de nácar y las seis cuerdas); a los lados las candilejas, los
    altavoces y los telones rojos; arriba, las cerchas con los focos. Cruza
    la calle: el origen en el centro y la calle a lo largo de y."""
    L = 420
    caja(mat('patio_opry', 0x1a1416, 0.9), 0, 0, -0.2, 26, L, 0.2)
    caja(mat('palosanto', 0x4a2c1c, 0.45), 0, 0, -0.02, 8.4, L, 0.05)            # el diapasón
    for s in (-1, 1):
        caja(mat('filete_mastil', 0xf0e6d0, 0.4), s * 4.25, 0, -0.02, 0.12, L, 0.06)
    tr = mat('traste_nv', 0xc8c8c0, 0.2)
    nacar = mat('nacar_nv', 0xf4f0e8, 0.2)
    for k in range(int(L / 7) + 1):
        y = -L / 2 + k * 7
        caja(tr, 0, y, 0.03, 8.4, 0.12, 0.03)
        if k % 4 == 2:
            cil(nacar, 0, y + 3.5, 0.031, 0.42, 0.005, 16)
    cu = mat('cuerda_nv', 0xd8c890, 0.25)
    for x in (-3.3, -1.98, -0.66, 0.66, 1.98, 3.3):                                  # las seis cuerdas (entre los carriles)
        caja(cu, x, 0, 0.06, 0.035, L, 0.02)
    telon = mat_franjas('telon_opry', 0x8a1a22, 0x6e1218, 2, eje='Z', z0=0.0, alto=0.6)
    for s in (-1, 1):
        caja(telon, s * 12, 0, 0, 1.2, L, 13)
        caja(mat('tarima_opry', 0x6a4a2e, 0.6), s * 8.4, 0, 0, 6.0, L, 0.5)       # la tarima de los lados
        for k in range(int(L / 4)):                                              # las candilejas
            esfera(bombilla(), s * 5.6, -L / 2 + 2 + k * 4, 0.6, 0.13, 1)
        caja(negro(), s * 5.6, 0, 0.5, 0.3, L, 0.06)
        for k in range(int(L / 30)):                                             # altavoces y guitarras, cada 30 m
            y = -L / 2 + 15 + k * 30
            caja(negro(), s * 9.2, y, 0.5, 2.2, 1.8, 3.4)
            for z in (1.3, 2.9):
                cil(mat('cono_altavoz', 0x4a4a52, 0.5), s * 8.08, y, z, 0.62, 0.06, 16, eje='X')
            if k % 2 == 0:
                guitarra(mat('guitarra_opry', 0xc8782a, 0.35), s * 9.4, y + 9, 0.5, alto=3.6)
            caja(mat('granero_opry', 0x9a2a22, 0.7), s * 11.3, y - 9, 0.5, 0.3, 6, 6.5)   # el granero rojo del decorado
            caja(blanco(), s * 11.1, y - 9, 0.5, 0.1, 2.2, 3.6)
    # Las cerchas con los focos (encendidos, quietos) y el techo.
    foco = luz('foco_opry', 0xfff0c0, 2.2)
    for k in range(int(L / 10)):
        y = -L / 2 + k * 10
        caja(hierro(), 0, y, 11.6, 24, 0.3, 0.5)
        for x in (-7.5, -2.5, 2.5, 7.5):
            cil(negro(), x, y, 10.9, 0.32, 0.7, 6)
            cil(foco, x, y, 10.86, 0.26, 0.04, 6)
    caja(mat('techo_opry', 0x120e10, 0.9), 0, 0, 13.0, 26, L, 0.3)
    for (y, txt) in ((-L / 2 + 0.6, 'GRAND OLE OPRY'), (L / 2 - 0.6, 'THANK YOU, NASHVILLE!')):
        caja(mat('granero_opry', 0x9a2a22, 0.7), 0, y, 8.2, 16, 0.3, 2.4)
        texto(neon_ambar(), txt, 0, y - 0.2, 9.4, tam=1.0, prof=0.06)

# ================================================================ obstáculos
def bailarin_linea():
    """El bailarín de baile en línea: botas, vaqueros, camisa de cuadros,
    pañuelo, los pulgares en el cinturón y el sombrero vaquero (da pasos de
    lado a lado con su pareja; no se pasa)."""
    for s in (-1, 1):
        rama(cuero(), (s * 0.2, -0.04, 0.0), (s * 0.2, 0, 0.45), 0.12, 0.11, 8)      # botas
        caja(cuero(), s * 0.2, -0.14, 0, 0.2, 0.42, 0.14)
        rama(vaquero(), (s * 0.2, 0, 0.45), (s * 0.17, 0, 0.98), 0.125, 0.14, 8)     # piernas
    caja(cuero(), 0, 0, 0.94, 0.62, 0.36, 0.1)
    caja(oro(), 0, -0.19, 0.94, 0.16, 0.03, 0.11)                                    # la hebilla
    cam = mat_bloques('camisa_cuadros', 0xc8282c, 0xf4f0e8, ancho=0.14, alto=0.14, grosor=0.02)
    rama(cam, (0, 0, 1.0), (0, 0, 1.52), 0.3, 0.34, 10)                              # el tronco
    esfera(cam, 0, 0, 1.52, 0.34, 2, esc=(1.1, 0.75, 0.5))
    for s in (-1, 1):                                                                # brazos en jarras
        rama(cam, (s * 0.36, 0, 1.5), (s * 0.56, 0.04, 1.2), 0.1, 0.085, 8)
        rama(cam, (s * 0.56, 0.04, 1.2), (s * 0.3, -0.12, 1.0), 0.085, 0.07, 8)
        esfera(piel(), s * 0.28, -0.14, 0.99, 0.08, 1)
    rama(piel(), (0, 0, 1.6), (0, 0, 1.72), 0.09, 0.09, 8)
    esfera(mat('panuelo_nv', 0x2a4a9a, 0.7), 0, -0.05, 1.63, 0.16, 1, esc=(1.2, 1, 0.6))
    esfera(piel(), 0, 0, 1.9, 0.24, 2)
    for dx in (-0.09, 0.09):
        esfera(negro(), dx, -0.22, 1.93, 0.03, 1)
    esfera(mat('bigote_nv', 0x5a3a22, 0.8), 0, -0.22, 1.82, 0.09, 1, esc=(1.6, 0.5, 0.4))
    # El sombrero: el ala ancha levantada a los lados y la copa hundida.
    sm = mat('sombrero_nv', 0xe8dcc0, 0.6)
    esfera(sm, 0, 0, 2.06, 0.5, 2, esc=(1.1, 1.0, 0.1))
    for s in (-1, 1):
        esfera(sm, s * 0.42, 0, 2.12, 0.2, 1, esc=(0.6, 1.6, 0.35))
    cil(sm, 0, 0, 2.06, 0.25, 0.3, 14, r2=0.21)
    cil(cuero(), 0, 0, 2.07, 0.255, 0.06, 14)

def nota_mastil():
    """La nota del mástil: un círculo que brilla en el suelo y la corchea
    flotando encima (se pisa: suena y da tacos)."""
    n = luz('nota_nv', 0x4ae0ff, 2.2)
    cil(luz('aro_nota', 0xffe08a, 2.0), 0, 0, 0.03, 1.0, 0.02, 28)
    cil(n, 0, 0, 0.05, 0.8, 0.02, 28)
    esfera(n, -0.12, 0, 1.0, 0.24, 2, esc=(1.2, 0.5, 0.85))
    caja(n, 0.12, 0, 1.0, 0.07, 0.07, 0.95)
    caja(n, 0.3, 0, 1.75, 0.36, 0.07, 0.2, giro=0.0)

def amplificador():
    """El amplificador de guitarra: la caja negra de tolex, la rejilla, los
    mandos y el piloto rojo (se salta)."""
    caja(negro(), 0, 0, 0, 1.2, 0.6, 0.95)
    caja(mat_bloques('rejilla_amp', 0x8a7a5a, 0x5a4e3a, ancho=0.05, alto=0.05, grosor=0.01), 0, -0.31, 0.08, 1.04, 0.03, 0.62)
    caja(oro(), 0, -0.31, 0.74, 1.04, 0.03, 0.14)
    for k in range(5):
        cil(negro(), -0.36 + k * 0.18, -0.34, 0.81, 0.035, 0.04, 8, eje='Y')
    esfera(luz('piloto_amp', 0xff3020, 2.0), 0.46, -0.33, 0.81, 0.03, 1)
    caja(cuero(), 0, 0, 0.95, 0.5, 0.08, 0.06)
    texto(blanco(), 'TACO', -0.3, -0.33, 0.56, tam=0.12, prof=0.01)

def bota_vaquera():
    """Una bota vaquera gigante de cuero repujado, con su tacón y la espuela
    (se salta)."""
    c = cuero()
    caja(mat('suela_nv', 0x2a1a12, 0.7), 0, -0.1, 0, 0.5, 1.25, 0.08)
    caja(mat('suela_nv', 0x2a1a12, 0.7), 0, 0.38, 0, 0.44, 0.3, 0.2)                 # el tacón
    esfera(c, 0, -0.42, 0.24, 0.26, 2, esc=(0.95, 1.5, 0.8))                         # la puntera
    rama(c, (0, 0.18, 0.12), (0, 0.22, 0.95), 0.27, 0.3, 12)                         # la caña
    cil(mat('ribete_bota', 0xe8dcc0, 0.5), 0, 0.22, 0.93, 0.31, 0.07, 12)
    for (z, col) in ((0.45, 0xe8b840), (0.65, 0xf4f0e8)):                            # el repujado
        cil(mat(f'repujado{col:06x}', col, 0.4), 0, -0.07, z, 0.1, 0.02, 5, eje='Y')
    cil(mat('espuela_nv', 0xc8c8c0, 0.2), 0, 0.62, 0.2, 0.12, 0.02, 8, eje='X')

def bateria():
    """La batería en su tarima: el bombo con el parche, los timbales, la caja
    y los platos (no se pasa)."""
    caja(negro(), 0, 0.1, 0, 2.3, 2.0, 0.3)
    cil(oro(), 0, 0.1, 0.3, 0.02, 0.02, 4)
    rj = mat('casco_bat', 0xb8242a, 0.25)
    cil(rj, 0, -0.1, 0.85, 0.55, 0.7, 20, eje='Y')                                   # el bombo
    cil(blanco(), 0, -0.46, 0.85, 0.5, 0.02, 20, eje='Y')
    texto(negro(), 'YMCA', 0, -0.49, 0.85, tam=0.22, prof=0.01)
    for s in (-1, 1):                                                                # los timbales
        cil(rj, s * 0.42, -0.1, 1.5, 0.3, 0.32, 16)
        cil(blanco(), s * 0.42, -0.1, 1.82, 0.3, 0.02, 16)
    cil(rj, -0.85, 0.2, 0.9, 0.34, 0.3, 16); cil(blanco(), -0.85, 0.2, 1.2, 0.34, 0.02, 16)   # la caja
    cil(rj, 0.85, 0.4, 0.3, 0.42, 0.75, 16); cil(blanco(), 0.85, 0.4, 1.05, 0.42, 0.02, 16)   # el goliat
    for (x, z) in ((-0.95, 2.0), (0.95, 1.95)):                                      # los platos
        cil(hierro(), x, 0.55, 0.3, 0.03, z - 0.3, 6)
        cil(oro(), x, 0.55, z, 0.42, 0.03, 20, r2=0.04)

def cartel_country():
    """La pancarta de Music City (agacharse)."""
    for x in (-1.25, 1.25):
        cil(madera(), x, 0, 0, 0.07, 2.75, 8)
    caja(mat('tela_country', 0xf2e2b0, 0.7), 0, 0, 1.55, 2.4, 0.06, 1.05)
    texto(rojo(), 'MUSIC CITY', 0, -0.04, 2.25, tam=0.26, prof=0.02)
    texto(negro(), 'YEE-HAW!', 0, -0.04, 1.86, tam=0.28, prof=0.02)

PIEZAS = {
    'partenon':        (partenon,        'nashville', dict(lado=2048, segmentos=1, min_bisel=1.0)),
    'ryman':           (ryman,           'nashville', dict(lado=2048, bisel=0.0)),
    'batman_building': (batman_building, 'nashville', dict(lado=2048, bisel=0.0)),
    'honky_tonk':      (honky_tonk,      'nashville', dict(lado=1024, bisel=0.0)),
    'arco_broadway':   (arco_broadway,   'nashville', dict(lado=1024, bisel=0.0, suelo=False)),
    'opry':            (opry,            'nashville', dict(lado=2048, bisel=0.0, suelo=False)),
    'bailarin_linea':  (bailarin_linea,  'obstaculos', dict(lado=256, bisel=0.0)),
    'nota_mastil':     (nota_mastil,     'obstaculos', dict(lado=128, bisel=0.0, suelo=False)),
    'amplificador':    (amplificador,    'obstaculos', dict(lado=256, bisel=0.0)),
    'bota_vaquera':    (bota_vaquera,    'obstaculos', dict(lado=256, bisel=0.0)),
    'bateria':         (bateria,         'obstaculos', dict(lado=256, bisel=0.0)),
    'cartel_country':  (cartel_country,  'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
}

correr(PIEZAS)
