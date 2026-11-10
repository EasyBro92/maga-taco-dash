# Los jefes que faltaban de la historia (09/11/2026).
#
#   blender -b -P blender/jefes.py -- [pieza ...] [--rapido]
#
# Isidro (09/11): «añade más jefes y haz el juego más gamberro». Uno por acto,
# como en HISTORIA.md, y el Monstruo del Pantano del final:
#   jefe_pinguino  el Rey Pingüino (Fargo): corona, capa de armiño y su cartel
#                  «TARIFF 10%» (el arancel a las islas de los pingüinos), de
#                  pie sobre un témpano que flota.
#   jefe_papeles   los Papeles (Miami): un remolino de carpetas tachadas con
#                  una caja de documentos dentro y dos ojos enfadados.
#   jefe_toro      el Toro de San Fermín (Los Ángeles): negro, pañuelo rojo y
#                  argolla en el morro. Va por el suelo, no flota.
#   jefe_cerebro   el Sentido Común (Boston): un cerebro rosa con gafas y
#                  birrete de Harvard.
#   jefe_pantano   el Monstruo del Pantano (Washington): un montón de barro
#                  verde con algas que lleva puesto un trozo de cada jefe.
# Lo que lanzan (obstáculos normales: origen a ras de suelo; los «altos»
# vuelan a la altura de la cabeza y se pasan agachado):
#   bloque_hielo, pez_helado · caja_documentos, carpeta_vuela ·
#   paellera, capote · libro_gordo, grafico_datos · bola_barro
# Y con lo que se les da: el rotulador gordo (los Papeles).
# Todos miran al jugador por -y.

import os, sys, math
import bpy
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import *

def blanco():  return mat('blanco_jf', 0xfbfbf8, 0.5)
def negro():   return mat('negro_jf', 0x18191e, 0.4)
def rojo():    return mat('rojo_jf', 0xd8262f, 0.45)
def oro():     return luz('oro_jf', 0xf2b01c, 0.45)
def naranja(): return mat('naranja_jf', 0xff8a1a, 0.4)
def ojo_b():   return luz('ojo_blanco_jf', 0xffffff, 0.3)


def punta(m, p0, p1, r0, lados=8):
    """Pincho o cono de p0 (gordo) a p1 (en punta)."""
    return rama(m, p0, p1, r0, 0.008, lados)


def ojos(x0, y, z, sep, r, enfadado=True, m_ceja=None):
    """Dos ojos de dibujo animado con pupila y ceja de enfadado."""
    for s in (-1, 1):
        esfera(ojo_b(), x0 + s * sep, y, z, r, 2, esc=(1, 0.5, 1.15))
        esfera(negro(), x0 + s * sep * 0.92, y - r * 0.45, z - r * 0.1, r * 0.48, 2, esc=(1, 0.5, 1))
        if enfadado:
            caja(m_ceja or negro(), x0 + s * sep, y - r * 0.3, z + r * 1.05, r * 2.2, r * 0.4, r * 0.38, inclina=0, giro=0).rotation_euler = (0, s * 0.35, 0)


# ================================================================ el Rey Pingüino
def jefe_pinguino():
    """El Rey Pingüino: 3,4 m, sobre un témpano que flota. Corona dorada, capa
    roja de armiño y el cartel del arancel en una aleta."""
    hielo = mat('tempano_jf', 0xd8eef8, 0.15)
    cil(hielo, 0, 0, 0, 1.6, 0.5, 9, r2=1.4)
    for k in range(6):
        a = k * 1.05
        caja(mat('tempano_b_jf', 0xbfe0f0, 0.15), math.cos(a) * 1.3, math.sin(a) * 1.3, 0.35, 0.5, 0.5, 0.35, giro=a)
    pluma = mat('pinguino_negro', 0x1c2230, 0.5)
    tripa = mat('pinguino_tripa', 0xf6f4ee, 0.55)
    esfera(pluma, 0, 0.1, 1.65, 1.05, 3, esc=(1.0, 0.9, 1.25))                    # cuerpo
    esfera(tripa, 0, -0.25, 1.5, 0.85, 3, esc=(0.95, 0.75, 1.15))                 # tripa blanca
    esfera(pluma, 0, 0.0, 2.95, 0.62, 3)                                          # cabeza
    for s in (-1, 1):                                                             # mejillas amarillas
        esfera(mat('mejilla_ping', 0xf6c83a, 0.5), s * 0.42, -0.25, 2.75, 0.22, 2, esc=(0.6, 0.6, 1.2))
    esfera(mat('cara_ping', 0xf6f4ee, 0.5), 0, -0.38, 2.85, 0.4, 2, esc=(1.05, 0.6, 0.9))
    ojos(0, -0.62, 3.0, 0.17, 0.11)
    punta(naranja(), (0, -0.55, 2.78), (0, -1.15, 2.7), 0.15)                     # pico
    for s in (-1, 1):                                                             # patas
        esfera(naranja(), s * 0.4, -0.35, 0.55, 0.28, 2, esc=(1, 1.4, 0.4))
    # La aleta izquierda, levantada con el cartel; la derecha, en la cadera.
    rama(pluma, (-0.95, 0, 2.1), (-1.55, -0.2, 2.9), 0.22, 0.12, 10)
    rama(mat('palo_ping', 0x8a5a32, 0.7), (-1.6, -0.25, 2.4), (-1.6, -0.25, 3.9), 0.05, 0.05, 8)
    caja(blanco(), -1.6, -0.3, 3.55, 1.5, 0.06, 0.8)
    caja(rojo(), -1.6, -0.34, 3.55, 1.56, 0.03, 0.86)
    caja(blanco(), -1.6, -0.36, 3.6, 1.44, 0.03, 0.72)
    texto(rojo(), 'TARIFF', -1.6, -0.4, 4.08, tam=0.3, prof=0.03)
    texto(negro(), '10%', -1.6, -0.4, 3.75, tam=0.32, prof=0.03)
    rama(pluma, (0.95, 0, 2.1), (1.15, -0.3, 1.5), 0.22, 0.12, 10)
    # La capa roja con el borde de armiño.
    capa = mat('capa_ping', 0xb01828, 0.55)
    caja(capa, 0, 0.65, 0.6, 1.9, 0.12, 2.3)
    caja(mat('armino', 0xfbfbf8, 0.8), 0, 0.6, 2.85, 2.0, 0.3, 0.3)
    for k in range(5):
        esfera(negro(), -0.8 + k * 0.4, 0.44, 3.0, 0.05, 1)
    # La corona.
    cil(oro(), 0, 0, 3.45, 0.42, 0.25, 16)
    for k in range(5):
        a = k * 2 * math.pi / 5 - math.pi / 2
        punta(oro(), (math.cos(a) * 0.38, math.sin(a) * 0.38, 3.65), (math.cos(a) * 0.4, math.sin(a) * 0.4, 4.0), 0.09)
        esfera(luz('rubi_ping', 0xff2040, 0.6), math.cos(a) * 0.43, math.sin(a) * 0.43, 3.57, 0.06, 1)

def bloque_hielo():
    """Bloque de hielo que lanza el Rey Pingüino: llega deslizándose. Se salta."""
    caja(mat('hielo_bloque', 0xbfe4f6, 0.08), 0, 0, 0, 1.1, 1.0, 0.85)
    caja(mat('hielo_luz', 0xeaf7fd, 0.05), -0.2, -0.505, 0.45, 0.5, 0.02, 0.3)
    texto(mat('arancel_hielo', 0x2a6ab0, 0.4), 'TARIFF', 0, -0.52, 0.4, tam=0.2, prof=0.02)

def pez_helado():
    """Un pez congelado que vuela a la altura de la cabeza: se pasa agachado."""
    m = mat('pez_plata', 0x8aa8c0, 0.3)
    esfera(m, 0, 0, 0.4, 0.35, 2, esc=(0.6, 1.6, 0.9))
    punta(m, (0, 0.45, 0.4), (0, 0.85, 0.65), 0.18)
    punta(m, (0, 0.45, 0.4), (0, 0.85, 0.15), 0.18)
    for s in (-1, 1):
        esfera(ojo_b(), s * 0.16, -0.3, 0.5, 0.08, 1)
        esfera(negro(), s * 0.19, -0.34, 0.5, 0.04, 1)
    esfera(mat('hielo_pez', 0xd8f0fa, 0.05), 0, 0, 0.4, 0.5, 2, esc=(0.75, 1.5, 1.0))


# ================================================================ los Papeles
def carpeta(m_tapa, x, y, z, giro=0.0, inclina=0.0, tam=1.0):
    """Carpeta marrón con dos tachones negros."""
    o = caja(m_tapa, x, y, z, 0.9 * tam, 0.08 * tam, 0.65 * tam, giro=giro, inclina=inclina)
    for k in range(2):
        b = caja(negro(), x, y, z + (0.18 + k * 0.22) * tam, 0.6 * tam, 0.1 * tam, 0.09 * tam, giro=giro, inclina=inclina)
    return o

def jefe_papeles():
    """El remolino de papeles: un embudo gris de viento con carpetas y hojas
    girando alrededor, la caja de documentos en el centro y ojos enfadados."""
    viento = mat('remolino_jf', 0xc9d2da, 0.7)
    viento2 = mat('remolino2_jf', 0xe4eaee, 0.7)
    for k in range(6):
        r0, r1 = 0.35 + k * 0.32, 0.55 + k * 0.32
        cil(viento if k % 2 else viento2, 0, 0, 0.2 + k * 0.6, r0, 0.62, 16, r2=r1)
    caja(mat('caja_doc_jf', 0xc8a878, 0.7), 0, -0.9, 1.6, 1.3, 0.9, 0.9)
    caja(mat('tapa_doc_jf', 0xb8986a, 0.7), 0, -0.9, 2.5, 1.36, 0.96, 0.15)
    texto(rojo(), 'SECRET', 0, -1.37, 2.05, tam=0.26, prof=0.03)
    ojos(0, -1.0, 3.2, 0.42, 0.24)
    tapa = mat('carpeta_jf', 0xd9b56a, 0.6)
    hoja = mat('hoja_jf', 0xfbfbf4, 0.6)
    for k in range(14):
        a = k * 2.4
        r = 1.0 + (k % 4) * 0.35
        z = 0.5 + (k * 0.27) % 3.2
        if k % 3 == 0:
            caja(hoja, math.cos(a) * r, math.sin(a) * r, z, 0.5, 0.03, 0.7, giro=a + 1.2, inclina=0.5)
        else:
            carpeta(tapa, math.cos(a) * r, math.sin(a) * r, z, giro=a + 1.57, inclina=0.35 * (k % 3 - 1))

def caja_documentos():
    """La caja de documentos que lanza: llega rodando y se salta."""
    caja(mat('caja_doc_jf', 0xc8a878, 0.7), 0, 0, 0, 0.95, 0.7, 0.7)
    caja(mat('tapa_doc_jf', 0xb8986a, 0.7), 0, 0, 0.66, 1.0, 0.75, 0.12)
    texto(rojo(), 'TOP SECRET', 0, -0.36, 0.38, tam=0.13, prof=0.02)
    for x in (-0.3, 0.3):
        caja(negro(), x, -0.36, 0.18, 0.28, 0.02, 0.06)

def carpeta_vuela():
    """Una carpeta abierta volando a la altura de la cabeza (agacharse)."""
    tapa = mat('carpeta_jf', 0xd9b56a, 0.6)
    caja(tapa, -0.32, 0, 0.2, 0.62, 0.05, 0.85, giro=0.25)
    caja(tapa, 0.32, 0, 0.2, 0.62, 0.05, 0.85, giro=-0.25)
    caja(mat('hoja_jf', 0xfbfbf4, 0.6), 0, -0.06, 0.25, 0.95, 0.03, 0.75)
    for k in range(3):
        caja(negro(), 0, -0.09, 0.4 + k * 0.17, 0.7, 0.02, 0.08)

def rotulador():
    """El rotulador gordo del mapa del huracán: lo que se le lanza a los Papeles."""
    cil(negro(), 0, 0, 0.0, 0.13, 0.75, 14)
    cil(mat('capuchon_rot', 0x2a2c34, 0.3), 0, 0, 0.72, 0.135, 0.22, 14)
    caja(blanco(), 0, -0.13, 0.25, 0.14, 0.02, 0.3)
    cil(negro(), 0, 0, -0.12, 0.06, 0.12, 10, r2=0.02)


# ================================================================ el Toro
def jefe_toro():
    """El Toro de San Fermín: 2,4 m de alto en la cruz, de frente al jugador,
    con el pañuelo rojo, la argolla, los cuernos y cara de muy malas pulgas."""
    piel = mat('toro_piel', 0x23191a, 0.6)
    esfera(piel, 0, 0.9, 1.5, 1.0, 3, esc=(1.0, 1.7, 0.85))                       # cuerpo
    esfera(piel, 0, -0.2, 1.75, 0.85, 3, esc=(1.15, 0.9, 0.95))                   # morrillo
    for (x, y) in ((-0.55, -0.1), (0.55, -0.1), (-0.55, 1.9), (0.55, 1.9)):      # patas
        cil(piel, x, y, 0, 0.2, 1.0, 10)
        cil(negro(), x, y, 0, 0.23, 0.15, 10)
    esfera(piel, 0, -0.95, 1.55, 0.55, 3, esc=(1.05, 1.0, 1.05))                  # cabeza
    esfera(mat('morro_toro', 0x6a4a44, 0.6), 0, -1.38, 1.38, 0.34, 2, esc=(1.2, 0.8, 0.8))
    for s in (-1, 1):
        esfera(negro(), s * 0.14, -1.62, 1.42, 0.07, 1)                           # narices
        rama(mat('cuerno_toro', 0xf0e6cc, 0.4), (s * 0.4, -0.9, 1.95), (s * 0.95, -1.25, 2.35), 0.13, 0.03, 10)
        esfera(piel, s * 0.6, -0.75, 1.85, 0.16, 2, esc=(1.4, 0.5, 0.7))           # orejas
    cil(oro(), 0, -1.62, 1.25, 0.15, 0.04, 16, eje='Y')                            # argolla
    ojos(0, -1.38, 1.75, 0.24, 0.12, m_ceja=mat('ceja_toro', 0x0e0a0a, 0.5))
    # Ojos rojos de rabia en la pupila.
    for s in (-1, 1):
        esfera(luz('rabia_toro', 0xff2a1a, 0.6), s * 0.22, -1.48, 1.73, 0.04, 1)
    # El pañuelo rojo de San Fermín al cuello.
    panu = mat('panuelo_toro', 0xd81e2a, 0.5)
    cil(panu, 0, -0.5, 1.15, 0.72, 0.28, 16, r2=0.68).rotation_euler = (0.35, 0, 0)
    punta(panu, (0, -1.05, 1.15), (0, -1.15, 0.65), 0.25, 4)
    # Vapor por la nariz (blanco suave).
    for s in (-1, 1):
        esfera(mat('vapor_toro', 0xf4f4f4, 0.9), s * 0.25, -1.85, 1.38, 0.13, 1)
        esfera(mat('vapor_toro', 0xf4f4f4, 0.9), s * 0.38, -2.0, 1.45, 0.09, 1)
    rama(piel, (0, 2.4, 1.8), (0, 3.0, 1.0), 0.07, 0.04, 6)                       # cola
    esfera(negro(), 0, 3.02, 0.95, 0.12, 1)

def paellera():
    """La paellera que lanza el Toro: rueda de canto hacia el jugador. Se salta."""
    hierro = mat('paellera_hierro', 0x3a3a40, 0.35)
    cil(hierro, 0, 0, 0.45, 0.45, 0.12, 24, eje='X')
    cil(mat('arroz_paella', 0xf2c23a, 0.7), -0.065, 0, 0.45, 0.4, 0.02, 24, eje='X')
    for k in range(6):
        a = k * 1.05
        esfera(mat('gamba_paella', 0xff6a3a, 0.5), -0.08, math.cos(a) * 0.25, 0.45 + math.sin(a) * 0.25, 0.06, 1)
        esfera(mat('guisante_paella', 0x4ab83a, 0.5), -0.08, math.cos(a + 0.5) * 0.15, 0.45 + math.sin(a + 0.5) * 0.15, 0.035, 1)
    for s in (-1, 1):
        caja(hierro, 0, s * 0.5, 0.42, 0.06, 0.14, 0.06)

def capote():
    """El capote rosa y amarillo que vuela a la altura de la cabeza (agacharse)."""
    caja(mat('capote_rosa', 0xe8508a, 0.6), 0, 0, 0, 1.6, 0.05, 0.9)
    caja(mat('capote_amarillo', 0xf2c23a, 0.6), 0, 0.03, 0.02, 1.6, 0.03, 0.86)
    cil(mat('palo_capote', 0x8a5a32, 0.7), 0, 0, 0.88, 0.04, 1.7, 8, eje='X')


# ================================================================ el Sentido Común
def jefe_cerebro():
    """El Sentido Común: un cerebro rosa gigante con gafas redondas, birrete
    de Harvard y un libro en cada mano."""
    rosa = mat('cerebro_rosa', 0xf2a0b0, 0.55)
    rosa2 = mat('cerebro_surco', 0xd87a8e, 0.6)
    esfera(rosa, 0, 0, 2.2, 1.2, 3, esc=(1.0, 0.9, 0.8))
    # Las circunvoluciones: tubos curvos encima.
    for k in range(7):
        x = -0.9 + k * 0.3
        rama(rosa2, (x, -0.8, 1.9), (x + 0.1, 0.0, 3.05), 0.1, 0.1, 8)
        rama(rosa2, (x + 0.1, 0.0, 3.05), (x, 0.8, 2.1), 0.1, 0.1, 8)
    rama(rosa2, (0, -1.05, 2.0), (0, 1.0, 2.0), 0.06, 0.06, 8)
    ojos(0, -1.0, 2.15, 0.38, 0.2)
    # Las gafas redondas.
    montura = mat('gafas_cer', 0x2a2420, 0.4)
    for s in (-1, 1):
        cil(montura, s * 0.38, -1.12, 2.15, 0.3, 0.05, 20, eje='Y')
        cil(mat('cristal_cer', 0xbfe0ee, 0.05), s * 0.38, -1.13, 2.15, 0.26, 0.04, 20, eje='Y')
    caja(montura, 0, -1.12, 2.18, 0.2, 0.05, 0.05)
    caja(negro(), 0, -1.0, 1.65, 0.35, 0.06, 0.06)                                 # boca de listillo
    # El birrete de Harvard (granate) con su borla.
    gran = mat('harvard_granate', 0x8a1c2a, 0.5)
    cil(gran, 0, 0, 2.95, 0.55, 0.3, 16)
    caja(gran, 0, 0, 3.25, 1.5, 1.5, 0.08, giro=0.785)
    rama(oro(), (0, 0, 3.35), (0.65, -0.3, 3.0), 0.03, 0.03, 6)
    esfera(oro(), 0.65, -0.3, 2.95, 0.08, 1)
    # Bracitos con libros.
    for s in (-1, 1):
        rama(rosa2, (s * 1.1, -0.2, 1.8), (s * 1.6, -0.6, 2.4), 0.1, 0.08, 8)
        caja(mat('libro_tapa_%d' % (s + 1), 0x1f4f8a if s < 0 else 0x2a7a3a, 0.5), s * 1.65, -0.7, 2.25, 0.5, 0.12, 0.65)
    cil(mat('pie_cer', 0xd87a8e, 0.6), 0, 0, 0.9, 0.3, 0.5, 12, r2=0.5)             # tronco del encéfalo

def libro_gordo():
    """El libro gordo que lanza: cae de canto y llega rodando. Se salta."""
    caja(mat('libro_tapa_0', 0x1f4f8a, 0.5), 0, 0, 0, 0.95, 0.6, 0.75)
    caja(mat('libro_hojas', 0xf6f0e0, 0.7), 0.02, 0, 0.04, 0.95, 0.5, 0.67)
    texto(oro(), 'FACTS', 0, -0.31, 0.38, tam=0.18, prof=0.02)

def grafico_datos():
    """Un gráfico de tarta volando a la altura de la cabeza (agacharse)."""
    cil(mat('tarta_azul', 0x2a6ab0, 0.5), 0, 0, 0.4, 0.6, 0.1, 24, eje='Y')
    caja(mat('tarta_roja', 0xd8262f, 0.5), 0.15, -0.06, 0.4, 0.3, 0.02, 0.3)
    caja(mat('tarta_amarilla', 0xf2c23a, 0.5), -0.15, -0.06, 0.15, 0.3, 0.02, 0.25)
    texto(blanco(), 'DATA', 0, -0.08, 0.72, tam=0.16, prof=0.02)


# ================================================================ el Monstruo del Pantano
def jefe_pantano():
    """El Monstruo del Pantano: un montón de barro verde con algas que gotea,
    con un trozo de cada jefe encima: los cuernos del toro, la corona del
    pingüino, el cerebro en la coronilla y una carpeta tachada en la mano."""
    barro = mat('pantano_verde', 0x4a6a2a, 0.75)
    barro2 = mat('pantano_oscuro', 0x34501e, 0.8)
    esfera(barro, 0, 0, 1.4, 1.4, 3, esc=(1.1, 0.9, 1.15))
    esfera(barro2, 0, 0, 0.4, 1.5, 2, esc=(1.1, 1.0, 0.35))
    for k in range(9):                                                            # algas que cuelgan
        a = k * 0.7 - 2.8
        rama(mat('alga_jf', 0x7a9a2a, 0.7), (math.sin(a) * 1.3, -math.cos(a) * 0.9, 2.3), (math.sin(a) * 1.5, -math.cos(a) * 1.05, 1.0), 0.09, 0.03, 6)
    ojos(0, -1.18, 2.0, 0.38, 0.24, m_ceja=barro2)
    caja(mat('boca_pantano', 0x1a2410, 0.6), 0, -1.22, 1.35, 0.9, 0.1, 0.25)
    for k in range(4):
        caja(mat('diente_pantano', 0xe8e0b0, 0.6), -0.3 + k * 0.2, -1.26, 1.45, 0.1, 0.05, 0.14)
    # Los trofeos de los otros jefes.
    for s in (-1, 1):
        rama(mat('cuerno_toro', 0xf0e6cc, 0.4), (s * 0.8, -0.2, 2.6), (s * 1.5, -0.5, 3.2), 0.16, 0.03, 10)
    esfera(mat('cerebro_rosa', 0xf2a0b0, 0.55), 0, 0.1, 2.85, 0.6, 2, esc=(1, 0.9, 0.65))
    cil(oro(), 0, 0.1, 3.15, 0.36, 0.22, 16)
    for k in range(5):
        a = k * 2 * math.pi / 5
        punta(oro(), (math.cos(a) * 0.33, 0.1 + math.sin(a) * 0.33, 3.35), (math.cos(a) * 0.35, 0.1 + math.sin(a) * 0.35, 3.65), 0.08)
    rama(barro, (1.3, -0.2, 1.6), (1.8, -0.7, 2.3), 0.25, 0.18, 8)
    carpeta(mat('carpeta_jf', 0xd9b56a, 0.6), 1.85, -0.8, 2.2, tam=1.2)
    rama(barro, (-1.3, -0.2, 1.6), (-1.7, -0.8, 1.2), 0.25, 0.18, 8)
    # Un taco de burrito-bot mordido en la otra mano.
    cil(mat('tortilla_jf', 0xf0cf8a, 0.6), -1.75, -0.9, 0.95, 0.28, 0.6, 12)

def bola_barro():
    """La bola de barro del pantano: cae y llega rodando. Se salta."""
    esfera(mat('pantano_verde', 0x4a6a2a, 0.75), 0, 0, 0.45, 0.45, 2, esc=(1, 1, 0.95))
    esfera(mat('pantano_oscuro', 0x34501e, 0.8), 0.15, -0.3, 0.6, 0.15, 1)
    esfera(mat('pantano_oscuro', 0x34501e, 0.8), -0.2, -0.32, 0.35, 0.12, 1)
    rama(mat('alga_jf', 0x7a9a2a, 0.7), (0.1, -0.2, 0.85), (0.3, -0.3, 1.05), 0.04, 0.02, 5)


def hamburguesa():
    """La hamburguesa de comida rápida (las que sirvió en la Casa Blanca): lo
    que se le lanza al Sentido Común."""
    pan = mat('pan_hamb', 0xe0a050, 0.6)
    cil(pan, 0, 0, 0.0, 0.42, 0.14, 18)
    cil(mat('carne_hamb', 0x5a3220, 0.8), 0, 0, 0.14, 0.44, 0.12, 18)
    cil(mat('queso_hamb', 0xf6c23a, 0.5), 0, 0, 0.26, 0.46, 0.03, 4).rotation_euler = (0, 0, 0.4)
    cil(mat('lechuga_hamb', 0x5ab83a, 0.6), 0, 0, 0.29, 0.45, 0.04, 14)
    cupula(pan, 0, 0, 0.33, 0.42, 0.3, lados=18, aros=5)
    for k in range(6):
        a = k * 1.05
        esfera(mat('sesamo_hamb', 0xfbf0d0, 0.5), math.cos(a) * 0.22, math.sin(a) * 0.22, 0.58, 0.035, 1, esc=(1, 0.6, 0.5))

def desatascador():
    """El desatascador para «drenar el pantano»: lo que se le lanza al Monstruo."""
    cil(mat('palo_desat', 0x8a5a32, 0.7), 0, 0, 0.3, 0.06, 0.9, 10)
    cupula(mat('goma_desat', 0xd8262f, 0.4), 0, 0, 0.0, 0.32, 0.32, lados=18, aros=5).rotation_euler = (math.pi, 0, 0)
    cil(mat('goma_desat', 0xd8262f, 0.4), 0, 0, 0.0, 0.33, 0.06, 18)


S = dict(lado=256, bisel=0.0)
J = dict(lado=1024, bisel=0.0, suelo=False)
PIEZAS = {
    'jefe_pinguino':   (jefe_pinguino,   'obstaculos', J),
    'bloque_hielo':    (bloque_hielo,    'obstaculos', S),
    'pez_helado':      (pez_helado,      'obstaculos', S),
    'jefe_papeles':    (jefe_papeles,    'obstaculos', J),
    'caja_documentos': (caja_documentos, 'obstaculos', S),
    'carpeta_vuela':   (carpeta_vuela,   'obstaculos', S),
    'rotulador':       (rotulador,       'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
    'jefe_toro':       (jefe_toro,       'obstaculos', J),
    'paellera':        (paellera,        'obstaculos', S),
    'capote':          (capote,          'obstaculos', S),
    'jefe_cerebro':    (jefe_cerebro,    'obstaculos', J),
    'libro_gordo':     (libro_gordo,     'obstaculos', S),
    'grafico_datos':   (grafico_datos,   'obstaculos', S),
    'jefe_pantano':    (jefe_pantano,    'obstaculos', J),
    'bola_barro':      (bola_barro,      'obstaculos', S),
    'hamburguesa':     (hamburguesa,     'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
    'desatascador':    (desatascador,    'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
}

correr(PIEZAS)
