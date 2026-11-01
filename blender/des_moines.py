# Nivel 5: Des Moines, Iowa (01/11/2026).
#
#   blender -b -P blender/des_moines.py -- [pieza ...] [--rapido]
#
# Isidro eligió: final en el Capitolio dorado, mañana de invierno (el caucus de
# Iowa es en enero) y los cuatro tramos (soja, cerdos, cosechadoras y la cola
# del caucus). Bajando por Locust Street hacia el este, que acaba en el
# Capitolio, al otro lado del río:
#   norte (izquierda): el parque de esculturas · la biblioteca central, una caja
#                      de cristal con malla de cobre · la torre de 801 Grand, la
#                      más alta de Iowa, con su pirámide · el pabellón de eventos
#   sur (derecha):     el Hotel Fort Des Moines (1919) con su letrero en el tejado
#                      · la torre oscura de acero corten · el antiguo edificio de
#                      la biblioteca (1903), hoy el Salón del Premio Mundial de
#                      la Alimentación, junto al río
#   en medio:          las pasarelas acristaladas («skywalks») que cruzan por
#                      encima de la calle, y el puente sobre el río Des Moines
#   al fondo:          el Capitolio, con la cúpula de oro y las cuatro cúpulas
#                      pequeñas de cobre verde en las esquinas, en lo alto de la
#                      colina con su escalinata
# Después del río, el East Village: ladrillo bajo (edificios del kit).
# Todo con nieve: en los tejados, en el césped y al pie de los árboles.
# Las distancias van comprimidas: es un juego, no un plano.
# Todas las fachadas en y = 0 mirando a -y. El puente y las pasarelas cruzan la
# calle: su origen va en el centro de la calle y se extienden a lo largo de x.

import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import *

# ---------------------------------------------------------------- materiales
def nieve():    return mat('nieve_dm', 0xf4f8fc, 0.7)
def blanco():   return mat('blanco_dm', 0xfbf8f2, 0.5)
def oscuro():   return mat('hueco_dm', 0x2b2c33, 0.8)
def vidrio():   return mat('vidrio_dm', 0x6f93b5, 0.15)
def caliza():   return mat_bloques('caliza_dm', 0xe6dcc6, 0xcfc3aa, ancho=1.4, alto=0.55, grosor=0.02, variacion=1.04)
def granito():  return mat_bloques('granito_dm', 0xc9b29a, 0xae9880, ancho=1.2, alto=0.6, grosor=0.025, variacion=1.04)
def ladrillo(): return mat_bloques('ladrillo_dm', 0x9a4a3a, 0x7e3a2e, ancho=0.45, alto=0.2, grosor=0.02, variacion=1.08)
def oro():      return mat('oro_dm', 0xe8b43a, 0.22)
def cobre():    return mat('cobre_verde', 0x5f9e88, 0.5)
def hierro():   return mat('hierro_dm', 0x2c2e33, 0.4)
def rojo():     return mat('rojo_dm', 0xc8302a, 0.45)
def agua():     return mat('agua_rio', 0x3f6a86, 0.12)

def techo_nieve(x, y, z, w, d, grosor=0.35):
    """La nieve de un tejado plano: una capa algo más pequeña que el tejado."""
    caja(nieve(), x, y, z, w - 0.3, d - 0.3, grosor)

def ventanas(xs, z, w, h, y=0.0, marco=None, cristal=None, remate=None):
    for x in xs:
        ventana(x, z, w, h, y=y, marco=marco or blanco(), cristal=cristal or vidrio(), remate=remate)

def arbol_nieve_en(x, y, alto=5.0, semilla=0):
    """Árbol de invierno sin hojas, con nieve en las ramas y un montón al pie."""
    tronco = mat('tronco_inv', 0x5a4636, 0.85)
    cil(tronco, x, y, 0, 0.22, alto * 0.55, 8, r2=0.15)
    for k in range(6):
        a = (k / 6 + semilla * 0.13) * math.tau
        h = alto * (0.45 + 0.08 * (k % 3))
        p0 = (x, y, h)
        p1 = (x + math.cos(a) * 1.3, y + math.sin(a) * 1.3, h + 1.2)
        p2 = (x + math.cos(a + 0.4) * 2.0, y + math.sin(a + 0.4) * 2.0, h + 2.0)
        rama(tronco, p0, p1, 0.11, 0.06, 6)
        rama(tronco, p1, p2, 0.06, 0.025, 5)
        rama(tronco, p1, (p1[0] + math.cos(a - 0.6) * 0.9, p1[1] + math.sin(a - 0.6) * 0.9, p1[2] + 1.0), 0.05, 0.02, 5)
        # la nieve, encima de cada rama
        rama(nieve(), (p0[0], p0[1], p0[2] + 0.1), (p1[0], p1[1], p1[2] + 0.08), 0.08, 0.05, 5)
    cil(tronco, x, y, alto * 0.55, 0.15, alto * 0.35, 6, r2=0.05)
    esfera(nieve(), x, y, 0.0, 0.9, 2, esc=(1.2, 1.2, 0.3))

def farol_parque(x, y):
    cil(hierro(), x, y, 0, 0.08, 3.4, 8)
    esfera(mat('globo_farol', 0xfff6dc, 0.2), x, y, 3.55, 0.25, 2)

def banco_nieve(x, y):
    madera = mat('madera_banco_dm', 0x7a5a3a, 0.7)
    caja(madera, x, y, 0.42, 1.8, 0.45, 0.06)
    caja(madera, x, y + 0.22, 0.48, 1.8, 0.06, 0.45)
    for s in (-1, 1):
        caja(hierro(), x + s * 0.8, y, 0, 0.08, 0.45, 0.45)
    caja(nieve(), x, y, 0.48, 1.7, 0.4, 0.06)


# ---------------------------------------------------------------- piezas únicas
def parque_esculturas():
    """El parque de esculturas de Locust Street: césped nevado, caminos
    limpios, árboles sin hojas y dos esculturas grandes (una de vigas rojas y
    una figura blanca sentada abrazándose las rodillas)."""
    W, D = 60, 34
    caja(nieve(), 0, D / 2, 0, W, D, 0.12)
    camino = mat('camino_dm', 0xb9bcc4, 0.9)
    caja(camino, 0, D / 2, 0.12, 3.2, D, 0.02)
    caja(camino, 0, 12, 0.12, W - 4, 2.6, 0.02)
    caja(mat('bordillo_dm', 0xc9c4b8, 0.8), 0, 0.3, 0, W, 0.6, 0.45)
    # la escultura de vigas rojas: tres patas que se juntan arriba
    acero = mat('acero_rojo', 0xd8401e, 0.45)
    top = (-14, 14, 9.5)
    for p in ((-19, 9, 0), (-9, 9, 0), (-15, 21, 0)):
        rama(acero, p, top, 0.5, 0.45, 4)
    rama(acero, top, (-10, 16, 12.5), 0.4, 0.3, 4)
    rama(acero, (-17, 12, 4.5), (-10.5, 12, 5.5), 0.3, 0.3, 4)
    # la figura blanca sentada, como hecha de letras de acero (aquí, de una pieza)
    fig = mat('figura_blanca', 0xf6f6f2, 0.3)
    esfera(fig, 14, 16, 2.6, 2.8, 3, esc=(1.0, 0.9, 1.0))                   # cuerpo
    esfera(fig, 14, 13.6, 2.2, 1.4, 2, esc=(1.6, 1.0, 1.4))                 # rodillas
    esfera(fig, 14, 15.2, 6.1, 1.25, 3)                                     # cabeza
    for s in (-1, 1):
        rama(fig, (14 + s * 2.2, 16, 4.4), (14 + s * 1.2, 13.4, 3.2), 0.5, 0.42, 8)   # brazos
    cil(caliza(), 14, 16, 0, 3.6, 0.5, 24)                                  # peana
    for k, (x, y) in enumerate(((-26, 6), (-4, 26), (5, 6), (24, 26), (27, 8), (-25, 28))):
        arbol_nieve_en(x, y, 5.5 + (k % 3) * 0.8, k)
    for x in (-24, -8, 8, 24):
        farol_parque(x, 3)
    for x in (-18, 18):
        banco_nieve(x, 10.4)
    caja(mat('cartel_parque', 0x2f4f3a, 0.6), 4.5, 0.6, 0.45, 5.2, 0.3, 1.0)
    texto(blanco(), 'SCULPTURE PARK', 4.5, 0.42, 0.95, tam=0.42, prof=0.04)

def biblioteca_dm():
    """La biblioteca central (2006): dos plantas de cristal con una malla de
    cobre dentro que la hace brillar dorada, y el tejado verde (nevado)."""
    W, D, H = 40, 26, 10
    malla = mat_ventanas('malla_cobre', 0xc79a5a, 0x5a4a3a, paso_x=1.5, paso_z=2.5, hueco_x=1.38, hueco_z=2.38, variacion=1.12)
    caja(malla, 0, D / 2, 0.4, W, D, H)
    caja(mat('zocalo_bib', 0x8f939a, 0.6), 0, D / 2, 0, W + 0.4, D + 0.4, 0.4)
    caja(mat('alero_bib', 0xe8e4dc, 0.5), 0, D / 2, H + 0.4, W + 1.2, D + 1.2, 0.4)
    techo_nieve(0, D / 2, H + 0.8, W + 1.2, D + 1.2, 0.5)
    caja(vidrio(), -8, -0.08, 0.4, 6, 0.1, 3.6)                              # la entrada
    caja(mat('marquesina_bib', 0xe8e4dc, 0.5), -8, -1.5, 3.8, 8, 3, 0.25)
    caja(nieve(), -8, -1.5, 4.05, 7.6, 2.6, 0.18)
    texto(oscuro(), 'PUBLIC LIBRARY', 6, -0.06, 4.2, tam=0.75, prof=0.06)
    caja(mat('acera_bib', 0xb9bcc4, 0.9), 0, -2.5, 0, W, 5, 0.08)
    for x in (-17, 2, 17):
        arbol_nieve_en(x, -3.2, 4.6, int(x))

def torre_801():
    """801 Grand (1991), la torre más alta de Iowa: granito rosado, ventanas
    en bandas, y arriba la gran pirámide de cobre verde con su aguja."""
    W, D = 36, 26
    caja(granito(), 0, D / 2, 0, W, D, 9)                                    # el zócalo
    caja(vidrio(), 0, -0.08, 0.3, 14, 0.1, 6.5)
    caja(granito(), 0, -1.6, 6.8, 16, 3.2, 0.6)
    caja(nieve(), 0, -1.6, 7.4, 15.6, 2.8, 0.2)
    techo_nieve(0, D / 2, 9, W, D, 0.3)
    texto(blanco(), '801 GRAND', 0, -0.06, 7.8, tam=0.7, prof=0.05)
    TW, TD, TH = 22, 18, 66
    fachada = mat_ventanas('torre801', 0x3a4f6a, 0xcdb49a, paso_x=1.6, paso_z=3.0, hueco_x=1.1, hueco_z=1.7, variacion=1.1)
    caja(fachada, 0, TD / 2 + 3, 9, TW, TD, TH)
    for x in (-TW / 2 - 0.4, TW / 2 + 0.4):                                 # aristas de granito
        caja(granito(), x, TD / 2 + 3, 9, 1.2, TD + 0.8, TH)
    # la corona escalonada y la pirámide
    z = 9 + TH
    caja(granito(), 0, TD / 2 + 3, z, TW + 2.0, TD + 2.0, 1.4)
    caja(granito(), 0, TD / 2 + 3, z + 1.4, TW, TD, 2.2)
    cil(cobre(), 0, TD / 2 + 3, z + 3.6, (TW + 2) * 0.72, 15, 4, r2=0.4).rotation_euler = (0, 0, math.pi / 4)
    cil(oro(), 0, TD / 2 + 3, z + 18.4, 0.25, 7, 6, r2=0.03)               # la aguja

def ruan():
    """La torre oscura de acero corten (1974), con sus ventanas estrechas."""
    W, D, H = 30, 22, 54
    corten = mat_ventanas('corten', 0x2a3240, 0x6a4030, paso_x=1.4, paso_z=3.0, hueco_x=0.55, hueco_z=2.2, variacion=1.1)
    caja(corten, 0, D / 2 + 2, 6, W - 4, D - 2, H)
    caja(mat('vestibulo_ruan', 0x9fbcd0, 0.15), 0, D / 2 + 2, 0, W - 6, D - 4, 6)
    for x in (-12, -4, 4, 12):
        caja(mat('pilar_corten', 0x5a3628, 0.7), x, 2.5, 0, 1.0, 1.0, 6)
    caja(mat('pilar_corten', 0x5a3628, 0.7), 0, D / 2 + 2, 6, W - 3, D - 1, 1.0)
    caja(mat('pilar_corten', 0x5a3628, 0.7), 0, D / 2 + 2, 6 + H, W - 3, D - 1, 1.2)
    techo_nieve(0, D / 2 + 2, 7.2 + H, W - 3, D - 1, 0.3)
    caja(mat('plaza_ruan', 0xb9bcc4, 0.9), 0, 0, 0, W, 6, 0.08)

def hotel_fort():
    """Hotel Fort Des Moines (1919): once plantas de ladrillo, bajo y cornisa
    de piedra blanca, la marquesina de la entrada y el letrero del tejado."""
    W, D = 30, 18
    H = 5 + 10 * 3.1
    caja(ladrillo(), 0, D / 2, 0, W, D, H)
    caja(caliza(), 0, D / 2 - 0.15, 0, W + 0.3, D + 0.3, 5)
    for x in (-10.5, -6, 6, 10.5):
        ventana(x, 1.0, 3.0, 3.2, y=-0.15, marco=mat('marco_fort', 0x3a2a22, 0.5), cristal=vidrio())
    caja(oscuro(), 0, -0.2, 0.3, 3.2, 0.06, 3.6)
    caja(mat('marquesina_fort', 0x3a2a22, 0.5), 0, -1.6, 3.7, 6.5, 3.2, 0.35)
    caja(nieve(), 0, -1.6, 4.05, 6.1, 2.8, 0.15)
    texto(oro(), 'HOTEL FORT DES MOINES', 0, -3.25, 3.85, tam=0.3, prof=0.04)
    for p in range(10):
        ventanas([-12.5, -9, -5.5, -2, 2, 5.5, 9, 12.5], 5.8 + p * 3.1, 1.5, 2.1,
                 marco=mat('marco_fort_alto', 0xefe6d6, 0.5), remate='cornisa' if p in (0, 9) else None)
    caja(caliza(), 0, D / 2 - 0.4, H - 0.4, W + 0.8, D + 0.8, 1.0)
    techo_nieve(0, D / 2, H + 0.6, W + 0.8, D + 0.8)
    # el letrero del tejado: armazón de hierro y letras rojas
    for x in (-11, -5.5, 0, 5.5, 11):
        caja(hierro(), x, 2.0, H + 0.6, 0.15, 0.15, 3.6)
    caja(hierro(), 0, 2.0, H + 4.1, 24, 0.15, 0.15)
    caja(hierro(), 0, 2.0, H + 1.0, 24, 0.15, 0.15)
    texto(rojo(), 'HOTEL FORT DES MOINES', 0, 1.85, H + 2.55, tam=1.45, prof=0.2)

def world_food():
    """El antiguo edificio de la biblioteca (1903), hoy el Salón del Premio
    Mundial de la Alimentación: piedra clara, ventanas de arco, el pórtico de
    entrada en medio y la balaustrada arriba."""
    W, D, H = 44, 24, 12
    caja(caliza(), 0, D / 2, 0, W, D, H)
    caja(mat_franjas('almohadillado', 0xd8ccb2, 0xc4b79c, 10, eje='Z', z0=0, alto=4), 0, D / 2 - 0.1, 0, W + 0.2, D + 0.2, 4)
    marco = mat('marco_wf', 0xf2ece0, 0.5)
    for x in (-18, -13, -8, 8, 13, 18):
        ventana(x, 1.2, 1.6, 2.2, y=-0.1, marco=marco, cristal=vidrio())
        caja(oscuro(), x, -0.03, 5.2, 2.2, 0.04, 4.0)                       # arcos de arriba
        cil(oscuro(), x, -0.03, 9.2, 1.1, 0.04, 16, eje='Y')
        caja(marco, x, -0.2, 5.0, 2.8, 0.3, 0.2)
    # el pórtico: cuatro columnas, la puerta de arco y el frontón
    caja(caliza(), 0, -1.5, 0, 12, 3.0, 1.0)
    escalinata(caliza(), 0, -3.0, 0, 9, 5, huella=0.35, tabica=0.2)
    columnata(marco, -4.5, 4.5, 4, -2.3, 1.0, 0.45, 8.5)
    caja(oscuro(), 0, -0.05, 1.0, 2.6, 0.06, 4.5)
    cil(oscuro(), 0, -0.05, 5.5, 1.3, 0.06, 16, eje='Y')
    caja(marco, 0, -1.6, 9.5, 11, 3.4, 1.0)
    fronton(marco, 0, -3.2, 10.5, 11.4, 2.2, 3.2)
    texto(oscuro(), 'HALL OF LAUREATES', 0, -3.35, 9.85, tam=0.42, prof=0.04)
    # cornisa, balaustrada y la nieve del tejado
    caja(marco, 0, D / 2 - 0.3, H, W + 0.6, D + 0.6, 0.6)
    for k in range(31):
        cil(marco, -21 + k * 1.4, -0.1, H + 0.6, 0.15, 0.9, 8)
    caja(marco, 0, -0.1, H + 1.5, W, 0.4, 0.25)
    techo_nieve(0, D / 2, H + 0.6, W, D, 0.4)
    for x in (-21, 21):
        arbol_nieve_en(x, -3.5, 5, int(x))

def arena():
    """El pabellón de eventos junto al río: chapa plateada, un gran
    ventanal inclinado y la marquesina roja."""
    W, D, H = 60, 40, 18
    chapa = mat_franjas('chapa_arena', 0xc9ced6, 0xb2b8c2, 40, eje='X', z0=-W / 2, alto=W)
    caja(chapa, 0, D / 2 + 4, 0, W, D, H)
    caja(vidrio(), 0, 2.2, 0, 34, 0.3, H - 1, inclina=-0.25)
    for k in range(9):
        caja(mat('montante_arena', 0x8a929c, 0.3), -16 + k * 4, 2.1, 0, 0.25, 0.4, H - 1, inclina=-0.25)
    caja(rojo(), 0, 0.5, 5.5, 36, 3.6, 0.6)
    caja(nieve(), 0, 0.5, 6.1, 35.6, 3.2, 0.2)
    texto(blanco(), 'EVENTS CENTER', 0, -1.33, 5.62, tam=0.5, prof=0.05)
    caja(chapa, 0, D / 2 + 4, H, W - 2, D - 2, 1.2)
    techo_nieve(0, D / 2 + 4, H + 1.2, W - 2, D - 2, 0.4)
    caja(mat('plaza_arena', 0xb9bcc4, 0.9), 0, 0, 0, W, 8, 0.08)
    for x in (-26, 26):
        arbol_nieve_en(x, -2.5, 5, int(x))

def rio():
    """El río Des Moines bajo el puente de Locust Street. Cruza la calle: el
    origen en el centro de la calle, el agua a los dos lados (x) y a lo largo
    (y) los 40 m que mide el puente. Pretiles de piedra con farolas en el
    borde del puente; en el agua, placas de hielo; y las orillas nevadas."""
    L = 40
    for s in (-1, 1):
        x0 = s * 10.5                                                        # el pretil (los paseantes van por x = 9-10)
        caja(agua(), s * 51, 0, -0.02, 81.6, L, 0.1)
        for k in range(14):                                                  # placas de hielo
            x = s * (14 + (k * 7.3) % 60)
            y = -L / 2 + 3 + (k * 11.7) % (L - 6)
            esfera(mat('hielo_rio', 0xe8f2f8, 0.4), x, y, 0.06, 1.2 + (k % 3) * 0.6, 1, esc=(1.6, 1.0, 0.08))
        caja(caliza(), x0, 0, 0, 0.6, L, 1.1)
        caja(nieve(), x0, 0, 1.1, 0.6, L, 0.12)
        for k in range(5):
            y = -L / 2 + 2 + k * 9
            caja(caliza(), x0, y, 0, 1.0, 1.0, 1.4)
            cil(hierro(), x0, y, 1.4, 0.08, 3.2, 8)
            esfera(mat('globo_puente', 0xfff3d0, 0.2), x0, y, 4.75, 0.28, 2)
        # las orillas con nieve
        for y in (-L / 2 - 6, L / 2 + 6):
            caja(nieve(), s * 50, y, 0, 82, 12, 0.15)
            for k in range(4):
                arbol_nieve_en(s * (16 + k * 16), y + (2 if y > 0 else -2), 4.8 + k % 2, k)

def skywalk():
    """Una pasarela acristalada de Des Moines (hay más de 6 km) cruzando por
    encima de la calle de fachada a fachada. El origen en el centro de la calle."""
    W, D, Z, H = 23.5, 3.6, 7.0, 3.0
    marco = mat('marco_skywalk', 0x3a4a5a, 0.4)
    caja(marco, 0, 0, Z, W, D, 0.5)                                          # el suelo
    caja(mat('cristal_skywalk', 0x8fb8d0, 0.12), 0, 0, Z + 0.5, W, D - 0.2, H - 0.7)
    caja(marco, 0, 0, Z + H - 0.2, W, D, 0.4)
    techo_nieve(0, 0, Z + H + 0.2, W, D, 0.25)
    for k in range(13):
        x = -W / 2 + 0.2 + k * (W - 0.4) / 12
        caja(marco, x, -D / 2 + 0.05, Z + 0.5, 0.18, 0.1, H - 0.7)
        caja(marco, x, D / 2 - 0.05, Z + 0.5, 0.18, 0.1, H - 0.7)
    for y in (-D / 2 + 0.05, D / 2 - 0.05):
        caja(marco, 0, y, Z + 1.55, W, 0.1, 0.12)

def capitolio_iowa():
    """El Capitolio de Iowa en lo alto de su colina nevada: el cuerpo de
    piedra clara con el pórtico de seis columnas, la gran cúpula de oro con su
    linterna y, en las cuatro esquinas, las cúpulas pequeñas de cobre verde con
    los nervios dorados. Delante, la escalinata hasta la calle (el jugador se
    para al pie) y las dos banderas."""
    piedra = caliza()
    liso = mat('piedra_lisa_cap', 0xefe8d8, 0.5)
    Z0 = 2.4                                                                 # la colina
    caja(nieve(), 0, 40, 0, 120, 70, Z0)
    caja(mat('muro_colina', 0xcfc3aa, 0.7), 0, 5.6, 0, 120, 0.8, Z0 + 0.1)
    escalinata(liso, 0, 5.6, 0, 16, 12, huella=0.46, tabica=0.2)
    caja(nieve(), -30, 5.0, Z0, 40, 1.4, 0.18)
    caja(nieve(), 30, 5.0, Z0, 40, 1.4, 0.18)
    camino = mat('camino_cap', 0xc9c4b8, 0.8)
    caja(camino, 0, 10, Z0, 16, 9, 0.04)
    # el cuerpo
    W, D, H = 76, 34, 16
    Y0 = 15
    caja(mat_franjas('basamento_cap', 0xd8ccb2, 0xc4b79c, 8, eje='Z', z0=Z0, alto=4), 0, Y0 + D / 2, Z0, W, D, 4)
    caja(piedra, 0, Y0 + D / 2, Z0 + 4, W, D, H - 4)
    for p, (z, h) in enumerate(((Z0 + 1.0, 2.0), (Z0 + 5.2, 3.6), (Z0 + 10.2, 3.0))):
        for k in range(16):
            x = -34 + k * 4.5
            if abs(x) < 9:
                continue
            ventana(x, z, 1.5, h, y=Y0, marco=liso, cristal=vidrio(), remate='fronton' if p == 1 else None)
    caja(liso, 0, Y0 + D / 2 - 0.4, Z0 + H, W + 0.8, D + 0.8, 1.0)          # cornisa
    for k in range(51):                                                      # balaustrada
        cil(liso, -37.5 + k * 1.5, Y0 - 0.2, Z0 + H + 1.0, 0.18, 1.0, 8)
    caja(liso, 0, Y0 - 0.2, Z0 + H + 2.0, W, 0.4, 0.3)
    techo_nieve(0, Y0 + D / 2, Z0 + H + 1.0, W, D, 0.5)
    # los pabellones de las esquinas, que salen un poco
    for s in (-1, 1):
        caja(piedra, s * 32, Y0 - 1.2, Z0, 12, 3, H)
        caja(liso, s * 32, Y0 - 1.4, Z0 + H, 12.6, 3.4, 1.0)
        for x in (-3, 0, 3):
            ventana(s * 32 + x, Z0 + 5.2, 1.4, 3.6, y=Y0 - 2.7, marco=liso, cristal=vidrio(), remate='fronton')
    # el pórtico de seis columnas con su frontón
    caja(liso, 0, Y0 - 3.5, Z0, 20, 7, 4)
    escalinata(liso, 0, Y0 - 7, Z0, 14, 8, huella=0.4, tabica=0.25)
    columnata(liso, -8.5, 8.5, 6, Y0 - 5.4, Z0 + 4, 0.75, 11)
    caja(liso, 0, Y0 - 3.4, Z0 + 15, 20.5, 7.2, 1.6)
    fronton(liso, 0, Y0 - 7.0, Z0 + 16.6, 21, 4.2, 7)
    caja(nieve(), 0, Y0 - 3.4, Z0 + 16.6, 0.5, 0.5, 0.1)
    caja(oscuro(), 0, Y0 - 0.05, Z0 + 4, 3.0, 0.06, 5.5)
    texto(oscuro(), 'STATE OF IOWA', 0, Y0 - 7.05, Z0 + 15.25, tam=0.9, prof=0.06)
    # la gran cúpula: tambor con columnas, ático, cúpula de oro y la linterna
    cx, cy, z = 0, Y0 + D / 2, Z0 + H + 1.0
    cil(liso, cx, cy, z, 12.5, 3.0, 40)
    z += 3.0
    cil(piedra, cx, cy, z, 10.5, 9.0, 40)
    for i in range(24):
        a = i / 24 * math.tau
        cil(liso, cx + math.cos(a) * 11.0, cy + math.sin(a) * 11.0, z, 0.42, 9.0, 10)
    for i in range(12):                                                      # ventanas del tambor
        a = (i + 0.5) / 12 * math.tau
        caja(vidrio(), cx + math.cos(a) * 10.45, cy + math.sin(a) * 10.45, z + 2.0, 2.0, 0.1, 4.5, giro=a + math.pi / 2)
    cil(liso, cx, cy, z + 9.0, 11.8, 1.2, 40)
    z += 10.2
    cil(piedra, cx, cy, z, 10.2, 2.2, 40)
    z += 2.2
    cupula(oro(), cx, cy, z, 10.0, 13.0, 40, 10)
    for i in range(16):                                                      # nervios
        a = i / 16 * math.tau
        pts = []
        for k in range(7):
            t = k / 6 * (math.pi / 2) * 0.96
            pts.append((cx + math.cos(a) * 10.08 * math.cos(t), cy + math.sin(a) * 10.08 * math.cos(t), z + 13.0 * math.sin(t)))
        for p0, p1 in zip(pts, pts[1:]):
            rama(mat('oro_nervio', 0xc8922a, 0.3), p0, p1, 0.16, 0.14, 5)
    z += 12.6
    cil(liso, cx, cy, z, 2.8, 1.0, 20)                                       # la linterna
    for i in range(10):
        a = i / 10 * math.tau
        cil(liso, cx + math.cos(a) * 2.3, cy + math.sin(a) * 2.3, z + 1.0, 0.18, 4.0, 8)
    cil(oscuro(), cx, cy, z + 1.0, 2.0, 4.0, 16)
    cil(liso, cx, cy, z + 5.0, 2.8, 0.6, 20)
    cupula(oro(), cx, cy, z + 5.6, 2.5, 3.0, 20, 6)
    cil(oro(), cx, cy, z + 8.4, 0.25, 3.0, 8, r2=0.05)
    esfera(oro(), cx, cy, z + 9.0, 0.45, 2)
    # las cuatro cúpulas pequeñas de cobre verde con nervios de oro
    for sx in (-1, 1):
        for sy in (0, 1):
            x, y = sx * 32, Y0 + 3 + sy * (D - 6)
            zz = Z0 + H + 1.0
            cil(liso, x, y, zz, 4.0, 1.4, 24)
            cil(piedra, x, y, zz + 1.4, 3.3, 4.2, 24)
            for i in range(10):
                a = i / 10 * math.tau
                cil(liso, x + math.cos(a) * 3.55, y + math.sin(a) * 3.55, zz + 1.4, 0.22, 4.2, 8)
            cil(liso, x, y, zz + 5.6, 3.9, 0.6, 24)
            cupula(cobre(), x, y, zz + 6.2, 3.6, 4.6, 24, 8)
            for i in range(8):
                a = i / 8 * math.tau
                pts = [(x + math.cos(a) * 3.66 * math.cos(t), y + math.sin(a) * 3.66 * math.cos(t), zz + 6.2 + 4.6 * math.sin(t))
                       for t in [k / 4 * (math.pi / 2) * 0.95 for k in range(5)]]
                for p0, p1 in zip(pts, pts[1:]):
                    rama(oro(), p0, p1, 0.07, 0.06, 4)
            cil(liso, x, y, zz + 10.7, 0.9, 1.4, 12)
            cupula(oro(), x, y, zz + 12.1, 0.9, 1.1, 12, 4)
            cil(oro(), x, y, zz + 13.1, 0.08, 1.2, 6, r2=0.02)
    # las banderas al pie de la escalinata: la de EE. UU. y la de Iowa
    for s in (-1, 1):
        x = s * 11.5
        cil(mat('mastil_cap', 0xd8dde3, 0.3), x, 4.0, 0, 0.12, 12, 8)
        esfera(oro(), x, 4.0, 12.1, 0.22, 1)
        if s < 0:
            caja(mat_franjas('barras_cap', 0xc8302a, 0xffffff, 13, eje='Z', z0=9.4, alto=2.4), x + 1.9, 4.0, 9.4, 3.6, 0.05, 2.4)
            caja(mat('canton_cap', 0x2a3f8a, 0.5), x + 0.9, 3.96, 10.5, 1.6, 0.05, 1.3)
        else:
            for k, c in enumerate((0x2a4fa8, 0xffffff, 0xc8302a)):            # la de Iowa: azul, blanco y rojo
                caja(mat(f'iowa{c:06x}', c, 0.5), x - 3.0 + k * 1.2, 4.0, 9.4, 1.2, 0.05, 2.4)
            texto(rojo(), 'IOWA', x - 1.8, 3.96, 9.75, tam=0.35, prof=0.02)
    # árboles nevados por la colina
    for k, (x, y) in enumerate(((-48, 12), (-44, 30), (48, 12), (44, 30), (-56, 46), (56, 46), (-22, 9), (22, 9))):
        arbol_nieve_en(x, y, 6 + (k % 3), k)
    # las faroles de la escalinata
    for s in (-1, 1):
        farol_parque(s * 9, 5.2)

def arbol_nieve():
    """Árbol de invierno de la acera (pieza)."""
    arbol_nieve_en(0, 0, 5.2, 3)


# min_bisel alto: solo se redondean los cantos de lo grande (en columnas,
# balaustres y nervios no se nota y multiplicaba los triángulos por cinco).
PIEZAS = {
    'parque_esculturas': (parque_esculturas, 'des_moines', dict(lado=1024, segmentos=1, min_bisel=1.0)),
    'biblioteca_dm':     (biblioteca_dm,     'des_moines', dict(lado=1024, segmentos=2, min_bisel=1.0)),
    'torre_801':         (torre_801,         'des_moines', dict(lado=1024, segmentos=2)),
    'ruan':              (ruan,              'des_moines', dict(lado=1024, segmentos=2)),
    'hotel_fort':        (hotel_fort,        'des_moines', dict(lado=1024, segmentos=2, min_bisel=1.0)),
    'world_food':        (world_food,        'des_moines', dict(lado=1024, segmentos=1, min_bisel=1.0)),
    'arena':             (arena,             'des_moines', dict(lado=1024, segmentos=2, min_bisel=1.0)),
    'rio':               (rio,               'des_moines', dict(lado=1024, bisel=0.0)),
    'skywalk':           (skywalk,           'des_moines', dict(lado=512, bisel=0.0)),
    'capitolio_iowa':    (capitolio_iowa,    'des_moines', dict(lado=2048, segmentos=1, min_bisel=2.0)),
    'arbol_nieve':       (arbol_nieve,       'des_moines', dict(lado=256, bisel=0.0)),
}

correr(PIEZAS)
