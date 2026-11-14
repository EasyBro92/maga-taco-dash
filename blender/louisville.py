# Nivel 23: Louisville, Kentucky (14/11/2026).
#
#   blender -b -P blender/louisville.py -- [pieza ...] [--rapido]
#
# Historia: «La carrera de caballos del Derby: los caballos le adelantan».
#   Por Main Street (el arco de «Derby City», el museo del bate Louisville
#   Slugger con su bate de seis pisos, la destilería de bourbon, el puesto
#   del cubo de pollo frito) mientras los bates gigantes caen atravesados en
#   la calle; en la pista de Churchill Downs los caballos del Derby vienen
#   por detrás y le adelantan; y se llega a la tribuna de las dos agujas.
# Obstáculos (carpeta obstaculos): el caballo del Derby con su jinete (dos
# colores) y su pata, el bate gigante, el seto de la pista, las barricas de
# bourbon, el cubo de pollo y la pancarta de las rosas.

import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import *
from comun import _poner

def blanco():   return mat('blanco_lv', 0xf4f0e8, 0.5)
def negro():    return mat('negro_lv', 0x1b1c20, 0.4)
def hierro():   return mat('hierro_lv', 0x3a3e44, 0.5)
def rojo():     return mat('rojo_lv', 0xc8282c, 0.45)
def oro():      return mat('oro_lv', 0xe8b840, 0.25)
def verde():    return mat('verde_lv', 0x2f6a3a, 0.8)
def seto():     return mat('seto_lv', 0x3f7a32, 0.9)
def fresno():   return mat('fresno_lv', 0xd8b47a, 0.45)
def roble():    return mat('roble_lv', 0x8a5a32, 0.6)
def piel():     return mat('piel_lv', 0xe8b89a, 0.6)
def castano():  return mat('castano_lv', 0x6a3a1e, 0.55)
def crin():     return mat('crin_lv', 0x1e1410, 0.7)
def rosa():     return mat('rosa_lv', 0xc8203a, 0.6)
def ladrillo(): return mat_bloques('ladrillo_lv', 0x8a4a3a, 0x6a3a2e, ancho=0.5, alto=0.22)
def tablas():   return mat_bloques('tablas_lv', 0xf4f0e8, 0xd8d2c4, ancho=6.0, alto=0.3)
def bombilla(): return luz('bombilla_lv', 0xffe08a, 1.8)

def bate(m, p0, p1, r=1.0):
    """Un bate de béisbol de p0 (el pomo) a p1 (la punta), de radio r en lo gordo."""
    from mathutils import Vector
    a, b = Vector(p0), Vector(p1)
    d = b - a
    rama(m, a, a + d * 0.03, r * 0.62, r * 0.62, 14)                    # el pomo
    rama(m, a + d * 0.03, a + d * 0.42, r * 0.36, r * 0.46, 14)         # el mango
    rama(m, a + d * 0.42, a + d * 0.72, r * 0.46, r, 14)
    rama(m, a + d * 0.72, a + d * 0.97, r, r, 14)                       # el barril
    rama(m, a + d * 0.97, b, r, r * 0.7, 14)

def aguja(x, y, z):
    """Una de las dos agujas de Churchill Downs: la torre de ocho lados con
    sus arcos, el chapitel de pizarra y el remate."""
    b = blanco()
    cil(b, x, y, z, 2.0, 4.5, 8)
    for k in range(8):
        a = k * math.tau / 8 + math.tau / 16
        caja(mat('arco_aguja', 0x3a4a5a, 0.4), x + math.cos(a) * 1.86, y + math.sin(a) * 1.86, z + 1.0, 0.8, 0.1, 2.4, giro=a + math.pi / 2)
    cil(b, x, y, z + 4.5, 2.3, 0.4, 8)
    cil(mat('pizarra_lv', 0x4a5258, 0.6), x, y, z + 4.9, 2.1, 8.5, 8, r2=0.12)
    cil(oro(), x, y, z + 13.4, 0.1, 1.4, 6)
    esfera(oro(), x, y, z + 14.9, 0.28, 1)

# ================================================================ edificios
def churchill_downs():
    """Churchill Downs (la meta): la tribuna blanca de 1895 con sus galerías,
    el tejado verde y las dos agujas; delante, el círculo del ganador con la
    herradura de rosas."""
    Y = 18
    b = tablas()
    W = 58.0
    caja(b, 0, Y, 0, W, 16, 13)
    for z in (4.2, 8.4):                                 # las galerías con su barandilla
        caja(blanco(), 0, Y - 8.6, z, W, 1.6, 0.25)
        caja(verde(), 0, Y - 9.4, z + 0.25, W, 0.1, 0.9)
    for k in range(15):                                  # los pilares
        x = -W / 2 + 1 + k * (W - 2) / 14
        caja(blanco(), x, Y - 9.2, 0, 0.45, 0.45, 13)
    cr = mat('cristal_cd', 0x3a4a5a, 0.3)
    for z in (0.6, 4.9, 9.1):
        for k in range(14):
            caja(cr, -W / 2 + 3 + k * (W - 2) / 14, Y - 8.05, z, 2.6, 0.1, 2.8)
    tejado(mat('tejado_cd', 0x2f5a3a, 0.6), 0, Y - 9.5, Y + 8, 13, W + 1, 5, cumbrera='x')
    for s in (-1, 1):
        aguja(s * 7.5, Y - 2, 16.4)
    caja(blanco(), 0, Y - 9.5, 13.0, 30, 0.3, 2.0)
    texto(verde(), 'CHURCHILL DOWNS', 0, Y - 9.7, 14.0, tam=1.5, prof=0.08)
    # El círculo del ganador: césped, el seto, la herradura de rosas y la copa.
    cil(seto(), 0, Y - 20, 0, 7.0, 0.04, 32)
    cil(mat('cesped_cd', 0x5a9a4a, 0.9), 0, Y - 20, 0.04, 6.4, 0.02, 32)
    for k in range(13):                                  # la herradura (abierta hacia el jugador)
        a = math.pi * (-0.15 + 1.3 * k / 12)
        esfera(rosa(), math.cos(a) * 4.4, Y - 16 + math.sin(a) * 0.01, 1.2 + math.sin(a) * 4.2, 0.75, 2)
    for s in (-1, 1):
        cil(blanco(), s * 4.3, Y - 16, 0, 0.14, 1.2, 8)
    cil(blanco(), 0, Y - 16, 0, 0.5, 1.4, 12)
    cil(oro(), 0, Y - 16, 1.4, 0.12, 0.6, 8)
    cil(oro(), 0, Y - 16, 2.0, 0.2, 0.9, 12, r2=0.5)
    texto(oro(), "WINNER'S CIRCLE", 0, Y - 12.4, 0.9, tam=0.8, prof=0.05)
    caja(verde(), 0, Y - 12.2, 0.2, 12, 0.3, 1.4)

def slugger_museum():
    """El museo del bate Louisville Slugger: la fábrica de ladrillo de cinco
    plantas y, apoyado en la fachada, el bate más grande del mundo (36 m)."""
    Y = 9
    L = ladrillo()
    caja(L, 0, Y, 0, 26, 16, 20)
    caja(mat('cornisa_lv', 0xd8c49c, 0.6), 0, Y - 8.2, 20, 26.6, 0.8, 1)
    for z in (5.4, 9.2, 13.0, 16.6):
        for k in range(6):
            ventana(-10.5 + k * 4.2, z, 2.4, 2.6, y=Y - 8, marco=blanco(), cristal=mat('cristal_lv', 0x2a3a4a, 0.2))
    caja(mat('entrada_slug', 0x2a3a4a, 0.2), 4, Y - 8.05, 0, 12, 0.1, 4.2)
    caja(hierro(), 4, Y - 8.9, 4.2, 13, 1.8, 0.25)
    texto(blanco(), 'LOUISVILLE SLUGGER', 4, Y - 9.85, 4.7, tam=0.8, prof=0.05)
    texto(oro(), 'MUSEUM & FACTORY', 4, Y - 8.2, 3.6, tam=0.5, prof=0.04)
    bate(fresno(), (-9.5, Y - 12.5, 0.2), (-8.0, Y - 8.9, 36.0), r=1.5)
    cil(mat('marca_bate', 0x2a2a2e, 0.5), -8.5, Y - 10.6, 25.0, 0.95, 0.06, 18, eje='Y')

def destileria():
    """La destilería de bourbon: el almacén negro de barricas (rickhouse) con
    sus ventanucos, el alambique de cobre y las barricas apiladas."""
    Y = 9
    n = mat_bloques('chapa_negra_lv', 0x24262a, 0x16181c, ancho=0.9, alto=6.0)
    caja(n, 0, Y, 0, 24, 16, 17)
    tejado(mat('tejado_dest', 0x4a4e54, 0.6), 0, Y - 8, Y + 8, 17, 24, 3.5)
    hastial(n, 0, Y - 8, Y + 8, 17, 24, 3.5)
    for z in (4, 7.5, 11, 14.5):
        for k in range(7):
            caja(mat('ventanuco_lv', 0x5a6a7a, 0.3), -9.6 + k * 3.2, Y - 8.05, z, 0.9, 0.1, 1.1)
    texto(blanco(), 'BOURBON', 0, Y - 8.15, 18.2, tam=1.6, prof=0.06)
    texto(oro(), 'KENTUCKY STRAIGHT', 0, Y - 8.15, 2.4, tam=0.6, prof=0.04)
    caja(roble(), 0, Y - 8.05, 0, 3.4, 0.14, 1.9)
    # El alambique de cobre, a la izquierda.
    cb = mat('cobre_lv', 0xc87a4a, 0.25)
    cil(cb, -8, Y - 10.5, 0, 1.5, 2.6, 16)
    esfera(cb, -8, Y - 10.5, 2.6, 1.5, 2, esc=(1, 1, 0.8))
    cil(cb, -8, Y - 10.5, 3.4, 0.4, 2.6, 10, r2=0.2)
    rama(cb, (-8, Y - 10.5, 6.0), (-5.5, Y - 10.5, 5.2), 0.18, 0.14, 8)
    # Barricas apiladas, a la derecha.
    for fila in range(3):
        for k in range(3 - fila):
            x = 6.0 + k * 1.5 + fila * 0.75
            cil(roble(), x, Y - 10.5, 0.7 + fila * 1.3, 0.7, 1.6, 14, eje='Y')
            for dy in (-0.55, 0.55):
                cil(hierro(), x, Y - 10.5 + dy, 0.7 + fila * 1.3, 0.72, 0.08, 14, eje='Y')

def pollo_frito():
    """El puesto de pollo frito de Kentucky: la caseta de rayas rojas y
    blancas y, en su poste, el cubo gigante (de tacos fritos)."""
    Y = 7
    r = mat_franjas('rayas_pollo', 0xc8282c, 0xf4f0e8, 12, eje='X', z0=-8.0, alto=16.0)
    caja(blanco(), 0, Y, 0, 16, 10, 4.6)
    caja(r, 0, Y - 0.5, 4.6, 17, 12, 0.9)
    tejado(rojo(), 0, Y - 5.5, Y + 5, 5.5, 16, 2.4, cumbrera='x')
    caja(mat('cristal_pollo', 0x8ab0c8, 0.2), 0, Y - 5.05, 1.0, 12, 0.1, 2.6)
    caja(rojo(), 0, Y - 5.1, 0, 2.2, 0.1, 3.4)
    texto(rojo(), 'KENTUCKY FRIED TACOS', 0, Y - 6.55, 5.05, tam=0.8, prof=0.05)
    # El cubo en su poste.
    cil(blanco(), 6.2, Y - 7.5, 0, 0.3, 9, 10)
    cubo = mat_franjas('rayas_cubo', 0xc8282c, 0xf4f0e8, 14, eje='X', z0=-2.6, alto=5.2)
    cil(cubo, 6.2, Y - 7.5, 9, 1.9, 4.2, 24, r2=2.6)
    cil(rojo(), 6.2, Y - 7.5, 13.2, 2.7, 0.3, 24)
    for k in range(7):                                   # los tacos fritos asomando
        a = k * math.tau / 7
        esfera(mat('frito_lv', 0xd89a48, 0.8), 6.2 + math.cos(a) * 1.5, Y - 7.5 + math.sin(a) * 1.5, 13.7, 0.8, 1, esc=(1, 1, 0.7))
    esfera(mat('frito_lv', 0xd89a48, 0.8), 6.2, Y - 7.5, 14.1, 0.9, 1)

# ================================================================ cruzan la calle
def arco_derby():
    """El arco de «DERBY CITY»: dos postes blancos, la herradura dorada con
    sus rosas y el letrero."""
    for s in (-1, 1):
        caja(blanco(), s * 9, 0, 0, 0.6, 0.6, 9.4)
        esfera(rosa(), s * 9, 0, 9.7, 0.6, 2)
    caja(blanco(), 0, 0, 6.2, 18.6, 0.5, 0.4)
    caja(blanco(), 0, 0, 8.6, 18.6, 0.5, 0.4)
    caja(verde(), 0, 0, 6.6, 17, 0.3, 2.0)
    texto(oro(), 'DERBY CITY', 0, -0.2, 7.55, tam=1.3, prof=0.07)
    o = texto(oro(), 'DERBY CITY', 0, 0.2, 7.55, tam=1.3, prof=0.07); o.rotation_euler = (math.pi / 2, 0, math.pi)
    for k in range(15):                                  # la herradura de arriba
        a = math.pi * (-0.1 + 1.2 * k / 14)
        esfera(oro(), math.cos(a) * 1.5, 0, 9.4 + math.sin(a) * 1.5, 0.3, 1)
    for k in range(24):
        esfera(rosa(), -8.3 + k * 0.72, -0.25, 6.4, 0.2, 1)

def hipodromo():
    """La pista de Churchill Downs (momento estrella): la recta de tierra
    entre barandillas blancas; a la izquierda, la tribuna llena de gente con
    las dos agujas; a la derecha, el césped de dentro con el marcador, los
    setos y los mástiles. Cruza la calle: el origen en el centro y la calle
    a lo largo de y."""
    L = 420
    caja(mat_bloques('tierra_pista', 0xb08a5e, 0xa47e54, ancho=3.0, alto=5.0, grosor=0.2), 0, 0, -0.2, 16, L, 0.2)
    b = blanco()
    for s in (-1, 1):                                    # las barandillas
        caja(b, s * 6.3, 0, 1.0, 0.14, L, 0.14)
        for k in range(int(L / 6)):
            rama(b, (s * 6.9, -L / 2 + 2 + k * 6, 0), (s * 6.3, -L / 2 + 2 + k * 6, 1.0), 0.07, 0.07, 4)
    # A la derecha: el césped de dentro, setos, el marcador y los mástiles.
    caja(mat('cesped_lv', 0x5a9a4a, 0.9), 16, 0, -0.2, 18, L, 0.22)
    caja(seto(), 8.4, 0, 0, 1.2, L, 0.9)
    for k in range(int(L / 60)):
        y = -L / 2 + 30 + k * 60
        caja(negro(), 16, y, 1.0, 1.2, 14, 6)                                    # el marcador de las apuestas
        for s in (-1, 1):
            cil(hierro(), 16, y + s * 6, 0, 0.2, 1.0, 8)
        o = texto(oro(), 'WIN  PLACE  SHOW', 15.36, y, 5.8, tam=1.0, prof=0.05); o.rotation_euler = (math.pi / 2, 0, -math.pi / 2)
        o = texto(bombilla(), '7 - 4 - 11', 15.36, y, 3.4, tam=1.6, prof=0.05); o.rotation_euler = (math.pi / 2, 0, -math.pi / 2)
        cil(b, 12, y + 30, 0, 0.12, 11, 8)                                       # el mástil con su banderín
        caja(rosa(), 12, y + 31.2, 9.4, 0.06, 2.4, 1.4)
        esfera(rosa(), 11, y + 15, 0.9, 1.1, 2, esc=(1, 2.4, 0.5))               # macizos de rosas
    # A la izquierda: la tribuna de tres gradas, la gente, el tejado y las agujas.
    grada = mat('grada_lv', 0xd8d2c4, 0.8)
    colores = [0xc8282c, 0x2a5aa8, 0xf0c030, 0xf4f0e8, 0xe87aa8, 0x3f8a4a, 0x8a4ac8]
    for g in range(3):
        caja(grada, -10.5 - g * 3.4, 0, 0, 3.4, L, 1.8 + g * 2.2)
        mg = mat(f'gente_lv{g}', colores[g * 2], 0.8)
        mh = mat(f'pamela_lv{g}', colores[g * 2 + 1], 0.7)
        for k in range(int(L / 4.2)):
            y = -L / 2 + 1.5 + k * 4.2 + g * 1.4
            z = 1.8 + g * 2.2
            cil(mg if k % 3 else mh, -10.0 - g * 3.4, y, z, 0.5, 0.9, 5)
            esfera(mat('cara_lv', 0xe8b89a, 0.7), -10.0 - g * 3.4, y, z + 1.15, 0.33, 1)
            if k % 3 == 1:                                                       # las pamelas del Derby
                cil(mh if k % 2 else mg, -10.0 - g * 3.4, y, z + 1.38, 0.7, 0.07, 6)
    caja(tablas(), -21.5, 0, 0, 1.0, L, 14)
    for k in range(int(L / 12)):
        caja(b, -9.2, -L / 2 + 6 + k * 12, 0, 0.3, 0.3, 14)
    caja(mat('tejado_cd', 0x2f5a3a, 0.6), -15, 0, 14, 14, L, 0.5)
    for dy in (-7.5, 7.5):
        aguja(-15, dy, 14.5)
    for (y, txt) in ((-L / 2 + 0.6, 'CHURCHILL DOWNS'), (L / 2 - 0.6, 'RUN FOR THE ROSES')):
        for s in (-1, 1):
            caja(b, s * 7.2, y, 0, 0.5, 0.5, 8.5)
        caja(verde(), 0, y, 6.4, 15, 0.3, 2.0)
        texto(oro(), txt, 0, y - 0.2, 7.4, tam=1.1, prof=0.06)

# ================================================================ obstáculos
def _caballo(seda, gorra):
    """El caballo del Derby, visto por detrás (galopa hacia +y): castaño, la
    crin y la cola negras, la mantilla con el número y el jinete con su
    casaca de seda. SIN patas: son la pieza derby_pata, que el juego mueve al
    galope (las caderas en world.js, ANDAR)."""
    c = castano()
    esfera(c, 0, 0, 1.38, 0.5, 2, esc=(0.82, 2.1, 0.9))                              # el cuerpo
    esfera(c, 0, -0.75, 1.42, 0.46, 2, esc=(0.88, 1.0, 0.95))                        # la grupa
    esfera(c, 0, 0.8, 1.45, 0.42, 2, esc=(0.85, 1.0, 1.0))                           # el pecho
    rama(c, (0, 0.9, 1.6), (0, 1.5, 2.25), 0.3, 0.2, 10)                             # el cuello
    rama(c, (0, 1.45, 2.25), (0, 1.95, 2.05), 0.2, 0.13, 10)                         # la cabeza
    esfera(mat('hocico_lv', 0x3a2416, 0.6), 0, 1.98, 2.03, 0.13, 1)
    for s in (-1, 1):
        cil(c, s * 0.1, 1.42, 2.36, 0.05, 0.16, 5, r2=0.01)                          # las orejas
    rama(crin(), (0, 0.95, 1.85), (0, 1.45, 2.38), 0.07, 0.05, 6)                    # la crin
    rama(crin(), (0, -1.18, 1.55), (0, -1.6, 1.0), 0.1, 0.03, 8)                     # la cola (al viento)
    caja(mat(f'mantilla_{seda:06x}', seda, 0.6), 0, -0.05, 1.3, 0.86, 0.8, 0.56)     # la mantilla
    texto(blanco(), '7', 0, -0.47, 1.6, tam=0.3, prof=0.02)
    # El jinete, encogido sobre el cuello.
    sd = mat(f'seda_{seda:06x}', seda, 0.4)
    rama(sd, (0, -0.1, 1.85), (0, 0.5, 2.3), 0.22, 0.2, 10)                          # la espalda
    for s in (-1, 1):
        rama(blanco(), (s * 0.3, -0.1, 1.85), (s * 0.44, 0.2, 1.45), 0.1, 0.08, 8)   # las piernas
        rama(negro(), (s * 0.44, 0.2, 1.45), (s * 0.44, 0.05, 1.15), 0.07, 0.06, 8)  # las botas
        rama(sd, (s * 0.2, 0.45, 2.25), (s * 0.16, 0.95, 2.05), 0.08, 0.07, 8)       # los brazos
    esfera(mat(f'gorra_{gorra:06x}', gorra, 0.4), 0, 0.62, 2.5, 0.2, 2)              # el casco
    caja(mat(f'gorra_{gorra:06x}', gorra, 0.4), 0, 0.82, 2.46, 0.24, 0.2, 0.04)
    esfera(piel(), 0, 0.68, 2.42, 0.16, 1)

def caballo_derby():
    """Caballo del Derby con la casaca roja."""
    _caballo(0xc8282c, 0xf4f0e8)

def caballo_derby_azul():
    """Caballo del Derby con la casaca azul."""
    _caballo(0x2a5aa8, 0xf0c030)

def derby_pata():
    """Pata del caballo del Derby (castaña, con la cuartilla blanca y el
    casco negro). El origen, en la cadera."""
    c = castano()
    rama(c, (0, 0, 0.05), (0, 0.02, -0.5), 0.13, 0.075, 10)
    esfera(c, 0, 0.02, -0.5, 0.07, 2)
    rama(c, (0, 0.02, -0.5), (0, 0, -0.9), 0.055, 0.045, 8)
    rama(blanco(), (0, 0, -0.9), (0, 0, -1.02), 0.05, 0.055, 8)
    cil(negro(), 0, 0, -1.13, 0.068, 0.11, 12, r2=0.06)

def bate_gigante():
    """El bate gigante de Louisville Slugger, de pie sobre el pomo (el origen
    está en el suelo, en el pomo: el juego lo tumba atravesado en la calle).
    Mide 5,4 m: tumbado tapa dos carriles."""
    bate(fresno(), (0, 0, 0), (0, 0, 5.4), r=0.42)
    cil(mat('marca_bate', 0x2a2a2e, 0.5), 0, -0.4, 3.9, 0.3, 0.04, 16, eje='Y')
    cil(rojo(), 0, 0, 1.2, 0.2, 0.5, 14)

def seto_derby():
    """El seto de la pista con su barra blanca y las rosas (se salta)."""
    caja(seto(), 0, 0, 0, 2.2, 0.6, 0.72)
    esfera(seto(), 0, 0, 0.7, 0.5, 2, esc=(2.2, 0.6, 0.35))
    for x in (-1.15, 1.15):
        caja(blanco(), x, 0, 0, 0.12, 0.7, 0.95)
    caja(blanco(), 0, -0.3, 0.42, 2.3, 0.06, 0.1)
    for k in range(5):
        esfera(rosa(), -0.8 + k * 0.4, -0.3, 0.78, 0.1, 1)

def barricas_bourbon():
    """Dos barricas de bourbon tumbadas en su calzo (se saltan)."""
    for (x, z) in ((-0.42, 0.4), (0.42, 0.4)):
        cil(roble(), x, 0, z, 0.4, 0.95, 14, eje='Y')
        for dy in (-0.32, 0.32):
            cil(hierro(), x, dy, z, 0.415, 0.06, 14, eje='Y')
        cil(mat('tapa_barrica', 0xa87a4a, 0.6), x, -0.48, z, 0.34, 0.02, 14, eje='Y')
    texto(negro(), 'KY', -0.42, -0.5, 0.4, tam=0.2, prof=0.01)
    caja(roble(), 0, 0, 0, 1.8, 0.2, 0.08)

def cubo_pollo():
    """El cubo gigante de pollo frito, de rayas rojas y blancas, lleno de
    tacos fritos (no se pasa)."""
    cubo = mat_franjas('rayas_cubo_ob', 0xc8282c, 0xf4f0e8, 10, eje='X', z0=-1.0, alto=2.0)
    cil(cubo, 0, 0, 0, 0.7, 1.7, 20, r2=0.98)
    cil(rojo(), 0, 0, 1.7, 1.02, 0.12, 20)
    for k in range(6):
        a = k * math.tau / 6
        esfera(mat('frito_ob', 0xd89a48, 0.8), math.cos(a) * 0.55, math.sin(a) * 0.55, 1.9, 0.34, 1, esc=(1, 1, 0.7))
    esfera(mat('frito_ob', 0xd89a48, 0.8), 0, 0, 2.05, 0.4, 1)
    caja(blanco(), 0, -0.86, 0.7, 0.9, 0.04, 0.5)
    texto(rojo(), 'KFT', 0, -0.9, 0.95, tam=0.3, prof=0.02)

def cartel_rosas():
    """La pancarta de la carrera de las rosas (agacharse)."""
    for x in (-1.25, 1.25):
        cil(blanco(), x, 0, 0, 0.07, 2.75, 8)
    caja(verde(), 0, 0, 1.55, 2.4, 0.06, 1.05)
    texto(blanco(), 'RUN FOR', 0, -0.04, 2.25, tam=0.26, prof=0.02)
    texto(oro(), 'THE ROSES', 0, -0.04, 1.86, tam=0.28, prof=0.02)
    for x in (-1.0, 1.0):
        esfera(rosa(), x, -0.05, 2.05, 0.12, 1)

PIEZAS = {
    'churchill_downs':    (churchill_downs,    'louisville', dict(lado=2048, bisel=0.0)),
    'slugger_museum':     (slugger_museum,     'louisville', dict(lado=2048, bisel=0.0)),
    'destileria':         (destileria,         'louisville', dict(lado=1024, bisel=0.0)),
    'pollo_frito':        (pollo_frito,        'louisville', dict(lado=1024, bisel=0.0)),
    'arco_derby':         (arco_derby,         'louisville', dict(lado=1024, bisel=0.0, suelo=False)),
    'hipodromo':          (hipodromo,          'louisville', dict(lado=2048, bisel=0.0, suelo=False)),
    'caballo_derby':      (caballo_derby,      'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
    'caballo_derby_azul': (caballo_derby_azul, 'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
    'derby_pata':         (derby_pata,         'obstaculos', dict(lado=128, bisel=0.0, suelo=False)),
    'bate_gigante':       (bate_gigante,       'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
    'seto_derby':         (seto_derby,         'obstaculos', dict(lado=256, bisel=0.0)),
    'barricas_bourbon':   (barricas_bourbon,   'obstaculos', dict(lado=256, bisel=0.0)),
    'cubo_pollo':         (cubo_pollo,         'obstaculos', dict(lado=256, bisel=0.0)),
    'cartel_rosas':       (cartel_rosas,       'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
}

correr(PIEZAS)
