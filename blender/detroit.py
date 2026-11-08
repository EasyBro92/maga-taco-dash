# Nivel 10: Detroit, Míchigan (08/11/2026).
#
#   blender -b -P blender/detroit.py -- [pieza ...] [--rapido]
#
# Isidro (08/11): «Aplica todas las preguntas que digas recomendados». Se
# aplicó lo recomendado: final delante del Renaissance Center (las torres de
# cristal junto al río) y luz de tarde. Historia: «La ciudad del motor, con
# coches llenos de aranceles. En el puente, canadienses enfadados: no quieren
# ser el estado 51».
#   izquierda:  el Spirit of Detroit (la estatua verde con la esfera dorada)
#               · el Guardian Building (el rascacielos naranja art déco)
#   derecha:    el teatro Fox con su letrero · el puño de Joe Louis
#   en medio:   el puente Ambassador a Canadá (el momento estrella): seis
#               tramos de puente colgante (la otra mitad, los mismos dados la
#               vuelta) y las dos torres verdes
#   al fondo:   el Renaissance Center
# Obstáculos (carpeta obstaculos): el coche con arancel (viene de frente), el
# alce (cruza), el canadiense enfadado (cruza), el barril de sirope de arce
# (viene rodando) y la pancarta «CANADA IS NOT FOR SALE» (agacharse).

import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import *

def blanco():   return mat('blanco_de', 0xfbf8f2, 0.5)
def negro():    return mat('negro_de', 0x1d1f25, 0.4)
def hierro():   return mat('hierro_de', 0x2c2e33, 0.4)
def rojo():     return mat('rojo_de', 0xd52b1e, 0.45)
def dorado():   return mat('dorado_de', 0xe0b048, 0.25)
def bronce_v(): return mat('bronce_verde', 0x4f8a70, 0.45)
def marmol():   return mat_bloques('marmol_de', 0xece8de, 0xd8d2c4, ancho=1.6, alto=0.8, grosor=0.015, variacion=1.03)
def verde_p():  return mat('verde_puente', 0x5f8f6a, 0.45)
def hormigon(): return mat('hormigon_de', 0xc4c0b8, 0.75)
def vidrio_os(): return mat_ventanas('vidrio_rencen', 0x6f88a4, 0x9aaabb, paso_x=1.2, paso_z=1.1, hueco_x=1.05, hueco_z=0.85, variacion=1.15)

# ================================================================ los edificios
def spirit_detroit():
    """El Spirit of Detroit delante del ayuntamiento: la figura sentada de
    bronce verde con la esfera dorada en una mano y la familia en la otra,
    sobre su pedestal, con el muro de mármol detrás; el edificio blanco con
    sus ventanas, al fondo."""
    caja(mat('plaza_sd', 0xd8d0c0, 0.8), 0, 9, 0, 30, 18, 0.1)
    caja(marmol(), 0, 9.5, 0, 16, 1.2, 7.5)
    texto(mat('letras_sd', 0x6a5a40, 0.4), 'THE SPIRIT OF DETROIT', 0, 8.85, 6.2, tam=0.55, prof=0.04)
    caja(marmol(), 0, 5.5, 0, 6, 4, 1.4)
    b = bronce_v()
    caja(b, 0, 6.0, 1.4, 3.4, 2.4, 1.6)               # asiento y regazo
    for x in (-0.8, 0.8):
        caja(b, x, 4.6, 1.4, 0.9, 1.2, 1.5)            # piernas
    cil(b, 0, 6.3, 3.0, 1.3, 3.2, 12, r2=0.9)          # cuerpo
    esfera(b, 0, 6.2, 6.8, 0.75, 2)                    # cabeza
    rama(b, (-1.1, 6.0, 5.4), (-2.0, 4.6, 4.6), 0.35, 0.3, 8)
    rama(b, (1.1, 6.0, 5.4), (2.0, 4.6, 4.6), 0.35, 0.3, 8)
    esfera(dorado(), -2.1, 4.3, 5.4, 0.85, 2)          # la esfera dorada
    for k, x in enumerate((1.7, 2.1, 2.5)):            # la familia en la mano
        cil(b, x, 4.4, 4.7, 0.16, 0.9 - k * 0.15, 8)
        esfera(b, x, 4.4, 5.65 - k * 0.15, 0.15, 1)
    caja(mat_ventanas('ventanas_ayto', 0x5a6a7a, 0xece8de, paso_x=1.0, paso_z=1.1, hueco_x=0.55, hueco_z=0.7), 0, 22, 0, 30, 16, 36)
    caja(mat('remate_ayto', 0xd8d2c4, 0.6), 0, 22, 36, 30.4, 16.4, 1.0)

def guardian_building():
    """El Guardian Building: ladrillo naranja, cuerpo escalonado art déco con
    franjas verticales y las dos coronas octogonales arriba."""
    nar = mat_bloques('ladrillo_guardian', 0xc8602e, 0xa84e24, ancho=0.4, alto=0.2, grosor=0.02, variacion=1.06)
    franja = mat('franja_guardian', 0x8a3a1c, 0.6)
    caja(mat('base_guardian', 0x6a5a4a, 0.6), 0, 9, 0, 26, 18, 6)
    caja(nar, 0, 9, 6, 24, 18, 34)
    for x in range(-10, 11, 2):
        caja(franja, x, -0.05, 6, 0.5, 0.12, 34)
    caja(nar, 0, 11, 40, 16, 14, 12)
    for x in range(-6, 7, 2):
        caja(franja, x, 3.95, 40, 0.4, 0.12, 12)
    cil(nar, -3.5, 11, 52, 3.4, 6, 8)
    cil(mat('corona_guardian', 0xd8884a, 0.5), -3.5, 11, 58, 3.4, 4, 8, r2=1.0)
    cil(nar, 4.5, 11, 52, 2.4, 3, 8)
    cil(mat('corona_guardian', 0xd8884a, 0.5), 4.5, 11, 55, 2.4, 3, 8, r2=0.8)
    caja(mat('arco_guardian', 0xe8a060, 0.5), 0, -0.1, 0, 6, 0.3, 5)
    caja(mat('puerta_guardian', 0x2a2a30, 0.5), 0, -0.2, 0, 3.6, 0.2, 3.6)

def fox_theatre():
    """El teatro Fox: el edificio de oficinas de piedra clara con el gran
    letrero vertical rojo «FOX» y la marquesina con bombillas (fijas: nada
    parpadea) encima de la entrada."""
    piedra = mat_bloques('piedra_fox', 0xe2cfa8, 0xcab68e, ancho=1.2, alto=0.5, grosor=0.02, variacion=1.04)
    caja(piedra, 0, 10, 0, 30, 20, 32)
    for z in (6.0, 10.0, 14.0, 18.0, 22.0, 26.0):
        for x in range(-12, 13, 3):
            if abs(x) > 2:
                ventana(x, z, 1.4, 2.2, y=-0.05, marco=mat('marco_fox', 0x8a6a4a, 0.5), cristal=mat('cristal_fox', 0x4a5a6a, 0.2))
    caja(mat('cornisa_fox', 0xcab68e, 0.5), 0, 10, 32, 31, 21, 1.0)
    # El letrero vertical.
    caja(rojo(), 0, -1.2, 9, 2.4, 0.9, 18)
    for k, letra in enumerate('FOX'):
        texto(luz('letra_fox', 0xffe080, 1.0), letra, 0, -1.7, 22.5 - k * 5.0, tam=3.0, prof=0.1)
    # La marquesina.
    caja(mat('marquesina_fox', 0x9a1a1a, 0.5), 0, -2.0, 4.0, 16, 4.0, 2.4)
    caja(luz('bombillas_fox', 0xfff0b0, 0.8), 0, -4.02, 4.2, 15.4, 0.05, 0.2)
    caja(luz('bombillas_fox', 0xfff0b0, 0.8), 0, -4.02, 6.0, 15.4, 0.05, 0.2)
    caja(blanco(), 0, -4.04, 4.6, 12, 0.04, 1.2)
    texto(rojo(), 'TONIGHT: MAGA', 0, -4.08, 4.8, tam=0.7, prof=0.03)
    caja(mat('puerta_fox', 0x3a2a20, 0.5), 0, -0.1, 0, 10, 0.2, 3.6)

def puno_joe_louis():
    """El monumento a Joe Louis, «el Puño»: un brazo de bronce de 7 m con el
    puño cerrado, colgado en horizontal de una pirámide de cuatro patas."""
    caja(mat('plaza_puno', 0xd0c8b8, 0.8), 0, 8, 0, 20, 16, 0.1)
    caja(hormigon(), 0, 8, 0, 9, 9, 0.5)
    bron = mat('bronce_puno', 0x5a3e28, 0.35)
    top = (0, 8, 8.5)
    for x in (-3.5, 3.5):
        for y in (4.5, 11.5):
            rama(bron, (x, y, 0.5), top, 0.15, 0.12, 8)
    for y in (6.5, 9.5):
        rama(hierro(), (0, y - 0.7, 8.3), (0, y, 4.6), 0.03, 0.03, 4)
    rama(bron, (-3.0, 8, 4.4), (2.4, 8, 4.4), 0.5, 0.55, 12)          # el antebrazo
    esfera(bron, 3.0, 8, 4.4, 0.85, 2, esc=(1.1, 0.9, 0.95))         # el puño
    for k in range(4):
        cil(bron, 3.45, 7.6 + k * 0.27, 4.75, 0.17, 0.3, 8, eje='X')  # los nudillos

def ren_cen():
    """La meta: el Renaissance Center, la torre redonda de cristal oscuro en
    medio y las cuatro torres octogonales alrededor, sobre su zócalo de
    hormigón, con la plaza y la escalinata delante."""
    caja(mat('plaza_rc', 0xd8d2c6, 0.8), 0, 10, 0, 40, 20, 0.1)
    escalinata(hormigon(), 0, 4.0, 0.0, 22, 6)
    caja(hormigon(), 0, 34, 0, 80, 34, 9)
    caja(mat('vidrio_zocalo', 0x4a5a6a, 0.2), 0, 16.9, 1.0, 30, 0.2, 6)
    v = vidrio_os()
    cil(v, 0, 38, 9, 12, 92, 28)
    cil(mat('anillo_rc', 0x4a5a6c, 0.3), 0, 38, 101, 12.8, 5, 28)
    cil(v, 0, 38, 106, 11, 4, 28)
    cil(mat('remate_rc', 0x9aa4ae, 0.4), 0, 38, 110, 6, 3, 20)
    for x, y in ((-24, 24), (24, 24), (-24, 52), (24, 52)):
        cil(v, x, y, 9, 8, 62, 8).rotation_euler = (0, 0, math.pi / 8)
        cil(mat('remate_rc', 0x9aa4ae, 0.4), x, y, 71, 8.2, 1.2, 8).rotation_euler = (0, 0, math.pi / 8)

# ================================================================ el puente Ambassador
# El tablero va de 705 a 1065 (12 tramos de 30 m). El cable principal cuelga
# de las torres (40 m sobre el tablero) hasta 3 m en el centro: cada tramo
# lleva su trozo de curva. Del 0 al 5 son la primera mitad; la segunda son los
# mismos dados la vuelta (`giro` en levels.js).
L = 30.0
CABLE_X = 7.4
def alto_cable(u):
    return 3.0 + 37.0 * (2 * u - 1) ** 2

def puente_tramo(i):
    def f():
        u0 = i / 12.0
        caja(mat('asfalto_puente', 0x4a4c52, 0.8), 0, 0, -0.5, 8.4, L, 0.56)
        for s in (-1, 1):
            caja(mat('acera_puente', 0xb8b4ac, 0.75), s * 5.3, 0, -0.5, 1.8, L, 0.68)
            caja(hormigon(), s * 6.35, 0, -0.6, 0.3, L, 1.6)
            caja(verde_p(), s * 6.35, 0, 1.3, 0.12, L, 0.1)
            for k in range(12):
                caja(verde_p(), s * 6.35, -L / 2 + 1.25 + k * 2.5, 1.0, 0.08, 0.08, 0.35)
            # La cercha de debajo del tablero.
            caja(verde_p(), s * 6.9, 0, -5.6, 0.45, L, 0.45)
            caja(verde_p(), s * 6.9, 0, -1.2, 0.45, L, 0.45)
            for k in range(6):
                y = -L / 2 + k * 5
                caja(verde_p(), s * 6.9, y, -5.6, 0.3, 0.3, 4.6)
                rama(verde_p(), (s * 6.9, y, -5.4), (s * 6.9, y + 5, -1.0), 0.12, 0.12, 6)
            # El cable principal y las péndolas.
            h0, h1 = alto_cable(u0), alto_cable(u0 + 1 / 12.0)
            rama(mat('cable_puente', 0x3a4a44, 0.4), (s * CABLE_X, -L / 2, h0), (s * CABLE_X, L / 2, h1), 0.32, 0.32, 8)
            for k in range(6):
                y = -L / 2 + 2.5 + k * 5
                h = alto_cable(u0 + (y + L / 2) / L / 12.0)
                caja(mat('cable_puente', 0x3a4a44, 0.4), s * CABLE_X, y, -1.0, 0.07, 0.07, h + 1.0)
            # Una farola cada 15 m.
            for y in (-7.5, 7.5):
                cil(verde_p(), s * 6.35, y, 1.0, 0.08, 5.5, 8)
                caja(verde_p(), s * 5.95, y, 6.4, 0.9, 0.16, 0.12)
                caja(mat('farol_puente', 0xfff2c8, 0.3), s * 5.55, y, 6.2, 0.4, 0.3, 0.22)
        for y in (-10.0, 0.0, 10.0):
            caja(verde_p(), 0, y, -1.4, 14.2, 0.5, 0.6)
        # El río Detroit, muy abajo.
        caja(mat('rio_detroit', 0x2f6f8f, 0.15), 0, 0, -46, 520, L, 0.2)
    return f

def torre_ambassador():
    """Una torre del puente: las dos patas verdes a los lados del tablero, los
    travesaños con las cruces por encima de los camiones, el remate y el
    cable que pasa por arriba. Delante (en -y), la orilla en cuesta que baja
    al río: tapa el borde de la calle de después del puente."""
    v = verde_p()
    for s in (-1, 1):
        caja(v, s * CABLE_X, 0, -46, 1.8, 2.4, 89)
        caja(v, s * CABLE_X, 0, 43, 2.4, 3.0, 1.0)
        cil(v, s * CABLE_X, 0, 44, 1.0, 1.6, 8, r2=0.3)
        caja(hormigon(), s * CABLE_X, 0, -48, 4.0, 5.0, 4)
    for z in (9.0, 24.0, 38.0):
        caja(v, 0, 0, z, 2 * CABLE_X, 1.2, 1.4)
    for z0, z1 in ((10.4, 24.0), (25.4, 38.0)):
        rama(v, (-CABLE_X, 0, z0), (CABLE_X, 0, z1), 0.25, 0.25, 6)
        rama(v, (CABLE_X, 0, z0), (-CABLE_X, 0, z1), 0.25, 0.25, 6)
    texto(blanco(), 'AMBASSADOR BRIDGE', 0, -0.62, 9.25, tam=0.75, prof=0.04)
    # La orilla en cuesta, con hierba, bajando hasta el agua (la del principio
    # queda debajo de la calle y no se ve).
    caja(mat('orilla_verde', 0x5d7f4a, 0.9), 0, -12.5, -23.6 - 26.2, 300, 2.0, 52.4, inclina=-0.497)

# ================================================================ los obstáculos
def coche_arancel():
    """Un coche de Detroit de los de antes (azul, con el morro largo), mirando
    al jugador, con la etiqueta gigante del arancel en el techo («+25%»).
    Viene de frente."""
    W, Lc = 2.0, 4.8
    azul = mat('azul_detroit', 0x2a5ab8, 0.3)
    caja(azul, 0, Lc / 2, 0.3, W, Lc, 0.7)
    caja(azul, 0, Lc / 2 + 0.5, 1.0, W - 0.3, 2.2, 0.5)
    caja(mat('cristal_coche', 0x2c3e55, 0.15), 0, Lc / 2 - 0.62, 1.02, W - 0.4, 0.05, 0.42, inclina=-0.5)
    caja(mat('cromo', 0xd8dce2, 0.2), 0, -0.04, 0.35, W - 0.1, 0.12, 0.22)
    caja(mat('rejilla', 0x30343a, 0.4), 0, -0.02, 0.55, 1.2, 0.05, 0.25)
    for s in (-1, 1):
        cil(mat('faro', 0xfff2c0, 0.2), s * 0.75, -0.03, 0.62, 0.15, 0.05, 12, eje='Y')
        for y in (0.9, Lc - 0.9):
            cil(mat('neumatico', 0x1d1e21, 0.8), s * (W / 2 - 0.1), y, 0.36, 0.36, 0.28, 14, eje='X')
    # La etiqueta del arancel.
    caja(hierro(), 0, Lc / 2 + 0.5, 1.5, 0.06, 0.06, 0.5)
    caja(mat('etiqueta_amarilla', 0xf2c230, 0.4), 0, Lc / 2 + 0.5, 2.0, 1.6, 0.1, 0.8)
    texto(rojo(), '+25%', 0, Lc / 2 + 0.43, 2.2, tam=0.42, prof=0.02)

def alce():
    """El alce canadiense: cuerpo marrón oscuro, patas largas, la joroba, el
    hocico grande y las astas en pala. Cruza la calle (mira a +x)."""
    pelo = mat('pelo_alce', 0x4a3424, 0.8)
    for x in (-0.7, 0.7):
        for y in (-0.22, 0.22):
            cil(pelo, x, y, 0, 0.1, 1.15, 8)
    caja(pelo, 0, 0, 1.1, 1.9, 0.75, 0.85)
    caja(pelo, 0.55, 0, 1.75, 0.6, 0.6, 0.35)            # la joroba
    rama(pelo, (0.9, 0, 1.6), (1.3, 0, 2.0), 0.24, 0.2, 8)  # el cuello
    caja(pelo, 1.6, 0, 1.75, 0.75, 0.38, 0.42)            # la cabeza y el hocico
    caja(mat('morro_alce', 0x3a281a, 0.8), 1.98, 0, 1.75, 0.12, 0.34, 0.3)
    for s in (-1, 1):
        esfera(mat('ojo', 0x111111, 0.2), 1.62, s * 0.2, 2.02, 0.05, 1)
        astas = mat('astas', 0xd8c49a, 0.6)
        rama(astas, (1.4, s * 0.12, 2.15), (1.35, s * 0.55, 2.4), 0.06, 0.05, 6)
        caja(astas, 1.35, s * 0.85, 2.5, 0.5, 0.6, 0.08, giro=0.0, inclina=s * 0.35)
    caja(mat('barba_alce', 0x3a281a, 0.8), 1.55, 0, 1.38, 0.12, 0.08, 0.3)

def canadiense():
    """El canadiense enfadado: camisa de cuadros roja y negra, gorro de lana
    rojo con pompón, el palo de hockey en una mano y el cartel «NO 51st
    STATE» en la otra. Cruza la calle (mira a +x)."""
    camisa = mat_franjas('cuadros_lenador', 0xc8202a, 0x1d1f25, 6, eje='Z', z0=0.85, alto=0.66)
    piel = mat('piel_can', 0xe8b48c, 0.6)
    for sy in (-0.12, 0.12):
        cil(mat('vaquero_can', 0x2e4a7a, 0.6), 0, sy, 0, 0.11, 0.85, 8)
    caja(camisa, 0, 0, 0.85, 0.44, 0.54, 0.66)
    esfera(piel, 0, 0, 1.7, 0.21, 2)
    caja(mat('cejas', 0x3a2618, 0.6), 0.19, 0, 1.78, 0.04, 0.26, 0.04, inclina=0.0)
    cil(rojo(), 0, 0, 1.8, 0.22, 0.2, 12, r2=0.12)
    esfera(blanco(), 0, 0, 2.02, 0.08, 1)
    rama(camisa, (0, -0.28, 1.4), (0.25, -0.42, 1.1), 0.07, 0.06, 6)
    rama(mat('palo_hockey', 0x9a6a3a, 0.5), (0.25, -0.45, 1.3), (0.45, -0.45, 0.08), 0.03, 0.03, 6)
    caja(negro(), 0.55, -0.45, 0.02, 0.3, 0.08, 0.1)
    rama(camisa, (0, 0.28, 1.4), (0.2, 0.42, 1.9), 0.07, 0.06, 6)
    cil(mat('palo_cartel', 0x9a6a3a, 0.5), 0.2, 0.42, 1.3, 0.025, 1.4, 6)
    caja(blanco(), 0.22, 0.42, 2.25, 0.04, 0.9, 0.55)
    o = texto(rojo(), 'NO 51st', 0, 0, 0, tam=0.16, prof=0.01)
    o.rotation_euler = (math.pi / 2, 0, math.pi / 2)
    o.location = (0.25, 0.42, 2.48)
    o = texto(rojo(), 'STATE!', 0, 0, 0, tam=0.16, prof=0.01)
    o.rotation_euler = (math.pi / 2, 0, math.pi / 2)
    o.location = (0.25, 0.42, 2.28)

def barril_sirope():
    """El barril de sirope de arce, de madera con aros de hierro y la hoja de
    arce roja. Viene rodando: va centrado en el origen (rueda sobre el eje x)."""
    madera = mat_bloques('duelas', 0x9a6a3a, 0x7a4e28, ancho=0.18, alto=2.0, grosor=0.01, variacion=1.08)
    cil(madera, 0, 0, 0, 0.45, 1.1, 18, eje='X')
    for x in (-0.42, -0.2, 0.2, 0.42):
        cil(hierro(), x, 0, 0, 0.465, 0.05, 18, eje='X')
    for x in (-0.555, 0.555):
        cil(mat('tapa_barril', 0x7a4e28, 0.8), x, 0, 0, 0.42, 0.02, 18, eje='X')
        # La hoja de arce (rombo y punta) en cada tapa.
        o = caja(rojo(), x * 1.02, 0, 0, 0.02, 0.32, 0.32)
        o.rotation_euler = (math.pi / 4, 0, 0)

def pancarta_canada():
    """La pancarta de los canadienses colgada de dos postes: blanca con las
    franjas rojas de su bandera y «NOT FOR SALE». Se pasa agachado."""
    for x in (-0.95, 0.95):
        cil(hierro(), x, 0, 0, 0.04, 2.5, 6)
    caja(blanco(), 0, 0, 1.3, 1.9, 0.05, 0.9)
    for x in (-0.8, 0.8):
        caja(rojo(), x, -0.01, 1.3, 0.3, 0.06, 0.9)
    texto(rojo(), 'NOT FOR', 0, -0.04, 1.85, tam=0.2, prof=0.01)
    texto(rojo(), 'SALE', 0, -0.04, 1.5, tam=0.26, prof=0.01)

PIEZAS = {
    'spirit_detroit':    (spirit_detroit,    'detroit', dict(lado=1024, segmentos=2, min_bisel=1.0)),
    'guardian_building': (guardian_building, 'detroit', dict(lado=1024, segmentos=2, min_bisel=1.0)),
    'fox_theatre':       (fox_theatre,       'detroit', dict(lado=1024, segmentos=2, min_bisel=1.0)),
    'puno_joe_louis':    (puno_joe_louis,    'detroit', dict(lado=512, segmentos=2, min_bisel=1.0)),
    'ren_cen':           (ren_cen,           'detroit', dict(lado=2048, segmentos=1, min_bisel=2.0)),
    'torre_ambassador':  (torre_ambassador,  'detroit', dict(lado=1024, bisel=0.0, suelo=False)),
    'coche_arancel':     (coche_arancel,     'obstaculos', dict(lado=512)),
    'alce':              (alce,              'obstaculos', dict(lado=256, bisel=0.0)),
    'canadiense':        (canadiense,        'obstaculos', dict(lado=256, bisel=0.0)),
    'barril_sirope':     (barril_sirope,     'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
    'pancarta_canada':   (pancarta_canada,   'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
}
for _i in range(6):
    PIEZAS['puente_amb_%d' % _i] = (puente_tramo(_i), 'detroit', dict(lado=1024, bisel=0.0, suelo=False))

correr(PIEZAS)
