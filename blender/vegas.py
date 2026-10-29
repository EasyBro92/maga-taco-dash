# Nivel 4: el Strip de Las Vegas, Nevada (29/10/2026).
#
#   blender -b -P blender/vegas.py -- [pieza ...] [--rapido]
#
# Isidro eligió: final en la torre dorada del hotel Trump y luz de anochecer
# con los neones encendidos (fijos, sin parpadeos: se marea). Subiendo por el
# Strip hacia el norte desde el cartel de bienvenida:
#   oeste (izquierda): el cartel «Welcome to Fabulous Las Vegas» · la pirámide
#                      negra con su rayo de luz y la esfinge · el castillo de
#                      torres de colores · el lago de las fuentes con el hotel
#                      italiano · el palacio romano de columnas
#   este (derecha):    la torre Eiffel a media escala con el globo · la noria
#                      gigante · el campanario y el palacio veneciano
#   al fondo:          la torre dorada del hotel Trump
# Lo que brilla va con `luz()` / `ventanas_luz()` (comun.py): en el juego se ve
# encendido aunque sea de noche. Sin nombres de casinos en los letreros.
# Las distancias van comprimidas: es un juego, no un plano.
# Todas las fachadas en y = 0 mirando a -y.

import os, sys, math
import bpy, bmesh
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import *

# ---------------------------------------------------------------- materiales
def blanco():  return mat('blanco_lv', 0xfbf6ec, 0.5)
def crema():   return mat('crema_lv', 0xf1e3c8, 0.6)
def oscuro():  return mat('hueco_lv', 0x24232a, 0.8)
def oro():     return mat('oro_lv', 0xe8b43a, 0.25)
def rojo():    return mat('rojo_lv', 0xd23a2e, 0.45)
def azul():    return mat('azul_lv', 0x2350c8, 0.45)
def agua():    return mat('agua_lv', 0x2f7fb8, 0.1)
def verde():   return mat('verde_lv', 0x2f6a3e, 0.6)
def piedra():  return mat_bloques('piedra_lv', 0xe6d6b8, 0xcdbd9d, ancho=1.2, alto=0.6, grosor=0.03, variacion=1.04)
def bombilla(): return luz('bombilla_lv', 0xffe9a0)
def neon(nombre, color, fuerza=1.0): return luz(nombre, color, fuerza)
def ventanas_hotel(nombre, pared, cristal=0xffd27a, brillo=0.55, **kw):
    """Fachada de hotel de noche: rejilla de ventanas, casi todas encendidas."""
    op = dict(paso_x=1.6, paso_z=3.0, hueco_x=1.0, hueco_z=1.9, variacion=1.25)
    op.update(kw)
    return ventanas_luz(nombre, cristal, pared, brillo=brillo, **op)

def losa(m, puntos, y, grosor=0.2):
    """Placa plana de cualquier forma en el plano de la fachada: `puntos` son
    (x, z) en orden; la placa va de y a y + grosor."""
    me = bpy.data.meshes.new('losa')
    bm = bmesh.new()
    bm.faces.new([bm.verts.new((x, y, z)) for x, z in puntos])
    bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new('losa', me)
    bpy.context.scene.collection.objects.link(o)
    md = o.modifiers.new('grosor', 'SOLIDIFY')
    md.thickness = grosor
    md.offset = 1
    bpy.context.view_layer.objects.active = o
    bpy.ops.object.modifier_apply(modifier='grosor')
    return poner(o, m)

def poner(o, m):
    o.data.materials.clear()
    o.data.materials.append(m)
    from comun import _partes
    _partes.append(o)
    return o

def piramide(m, x, y, z, lado, alto):
    """Pirámide de base cuadrada (lados paralelos a la calle)."""
    o = cil(m, x, y, z, lado / math.sqrt(2), alto, 4, r2=0.0)
    o.rotation_euler = (0, 0, math.pi / 4)
    return o

def aro(m, x, y, z, radio, grueso, lados=48):
    """Aro de pie en el plano de la fachada (la noria)."""
    bpy.ops.mesh.primitive_torus_add(major_radius=radio, minor_radius=grueso, major_segments=lados,
                                     minor_segments=8, location=(x, y, z), rotation=(math.pi / 2, 0, 0))
    return poner(bpy.context.object, m)

def palmera_en(x, y, alto):
    tronco = mat_franjas('tronco_palmera_lv', 0x9c7a55, 0x86643f, 28, eje='Z', z0=0, alto=12)
    cil(tronco, x, y, 0, 0.32, alto, 10, r2=0.22)
    verdes = mat('hoja_palmera_lv', 0x3f8f3a, 0.6)
    for k in range(9):
        a = k / 9 * math.pi * 2
        dx, dy = math.cos(a), math.sin(a)
        rama(verdes, (x, y, alto), (x + dx * 1.6, y + dy * 1.6, alto + 0.6), 0.16, 0.12, 4)
        rama(verdes, (x + dx * 1.6, y + dy * 1.6, alto + 0.6), (x + dx * 2.8, y + dy * 2.8, alto - 0.5), 0.12, 0.03, 4)
    esfera(mat('cogollo_lv', 0x5a7a34, 0.6), x, y, alto, 0.4, 1)

def cipres(x, y, alto):
    cil(mat('tronco_cipres', 0x5a4632, 0.8), x, y, 0, 0.2, 0.8, 8)
    o = esfera(mat('cipres', 0x2f5a35, 0.7), x, y, 0.8 + alto / 2, 0.5, 2, esc=(1.1, 1.1, alto))
    return o

def bandera(x, y, z, w=1.8, h=1.2):
    """Bandera de EE. UU. que mira a -y."""
    caja(mat_franjas('barras_lv', 0xe8303a, 0xffffff, 13, eje='Z', z0=z, alto=h), x + w / 2, y, z, w, 0.04, h)
    caja(azul(), x + w * 0.23, y - 0.03, z + h * 0.46, w * 0.46, 0.04, h * 0.54)

def mastil(x, y, alto):
    cil(mat('mastil_lv', 0xd8dde3, 0.2), x, y, 0, 0.09, alto, 8)
    esfera(oro(), x, y, alto, 0.16, 1)
    bandera(x + 0.1, y, alto - 1.5)

def bombillas(puntos, paso=0.55, r=0.07, y=-0.12):
    """Bombillas a lo largo de una línea quebrada (x, z) delante de la fachada."""
    for (x0, z0), (x1, z1) in zip(puntos, puntos[1:]):
        n = max(1, int(math.hypot(x1 - x0, z1 - z0) / paso))
        for k in range(n):
            t = k / n
            esfera(bombilla(), x0 + (x1 - x0) * t, y, z0 + (z1 - z0) * t, r, 1)


# ---------------------------------------------------------------- piezas únicas
def cartel_vegas():
    """El cartel «Welcome to Fabulous Las Vegas» (1959): rombo blanco con
    bombillas, las letras de WELCOME en monedas de plata, la estrella roja
    encima, sobre dos postes."""
    poste = mat('poste_cartel', 0xd8dde3, 0.3)
    for x in (-2.2, 2.2):
        caja(poste, x, 0.1, 0, 0.5, 0.3, 4.0)
    caja(mat('peana_cartel', 0xbfae8c, 0.8), 0, 0.1, 0, 7.0, 2.4, 0.4)
    contorno = [(-4.0, 5.2), (-4.0, 6.7), (0, 8.4), (4.0, 6.7), (4.0, 5.2), (0, 3.5)]
    losa(neon('cartel_blanco', 0xfff8ec, 0.35), contorno, 0.0, 0.25)
    bombillas(contorno + contorno[:1], paso=0.42, r=0.08, y=-0.06)
    letra_roja = neon('letra_roja_lv', 0xff2a2a, 0.9)
    letra_azul = neon('letra_azul_lv', 0x2a6bff, 0.9)
    plata = neon('moneda_lv', 0xf2f2f2, 0.4)
    for k, c in enumerate('WELCOME'):
        x = -2.7 + k * 0.9
        cil(plata, x, -0.04, 6.9, 0.4, 0.06, 16, eje='Y')
        texto(letra_roja, c, x, -0.12, 6.9, tam=0.48, prof=0.04)
    texto(letra_azul, 'TO FABULOUS', 0, -0.06, 6.15, tam=0.42, prof=0.04)
    texto(letra_roja, 'LAS VEGAS', 0, -0.06, 5.15, tam=1.05, prof=0.06)
    texto(letra_azul, 'NEVADA', 0, -0.06, 4.25, tam=0.36, prof=0.04)
    # la estrella de ocho puntas
    estrella = neon('estrella_lv', 0xff3a2e, 0.9)
    for k in range(8):
        a = k / 8 * math.pi * 2
        largo = 0.95 if k % 2 == 0 else 0.6
        rama(estrella, (0, 0.05, 9.2), (math.cos(a) * largo, 0.05, 9.2 + math.sin(a) * largo), 0.16, 0.02, 4)
    esfera(neon('centro_estrella', 0xffd23f, 1.0), 0, 0.05, 9.2, 0.25, 1)
    cil(poste, 0, 0.12, 8.3, 0.08, 0.5, 6)

def piramide_lv():
    """La pirámide negra de cristal con el rayo de luz en la punta, la esfinge
    delante y un obelisco."""
    cristal = ventanas_luz('cristal_piramide', 0x28304a, 0x161a26, brillo=0.25,
                           paso_x=2.2, paso_z=2.2, hueco_x=1.9, hueco_z=1.6, variacion=1.5)
    piramide(cristal, 0, 30, 0, 58, 40)
    # el rayo de luz que sale de la punta (hacia el cielo)
    cil(neon('rayo_piramide', 0xdfefff, 1.0), 0, 30, 39.5, 0.55, 30, 10, r2=0.9)
    # aristas encendidas
    canto = neon('canto_piramide', 0xffe9b0, 0.7)
    for sx, sy in ((-1, -1), (1, -1)):
        rama(canto, (sx * 29, 30 + sy * 29, 0.2), (0, 30, 40), 0.18, 0.12, 6)
    # la esfinge, tumbada mirando a la calle
    arena = mat_bloques('arenisca_esfinge', 0xd9b47a, 0xbf9a62, ancho=1.0, alto=0.5, grosor=0.03, variacion=1.04)
    caja(arena, 0, 0, 0, 7, 10, 1.2)                                       # peana
    caja(arena, 0, 2.2, 1.2, 4.4, 7, 2.4)                                  # el cuerpo
    for s in (-1, 1):
        caja(arena, s * 1.4, -2.6, 1.2, 1.2, 3.4, 0.9)                     # patas delante
    caja(arena, 0, -0.6, 3.4, 2.6, 2.4, 2.8)                                # pecho y cuello
    caja(arena, 0, -1.0, 5.2, 2.2, 2.0, 2.2)                                # la cabeza
    nemes = mat_franjas('nemes', 0x2f5fa8, 0xe8b43a, 12, eje='Z', z0=4.0, alto=4)
    caja(nemes, 0, -0.6, 4.8, 3.4, 2.2, 3.0)                                # el tocado
    caja(arena, 0, -1.9, 5.3, 1.8, 0.6, 1.9)                                # la cara
    caja(oscuro(), 0, -2.25, 5.3, 0.3, 0.3, 0.6)                            # la barba
    for s in (-1, 1):
        caja(oscuro(), s * 0.45, -2.22, 6.4, 0.35, 0.06, 0.18)
    # obelisco
    caja(arena, -21, -1, 0, 3, 3, 1)
    cil(arena, -21, -1, 1, 1.0, 14, 4, r2=0.55).rotation_euler = (0, 0, math.pi / 4)
    piramide(oro(), -21, -1, 15, 1.1, 1.2)
    # focos del suelo (la pirámide se ilumina desde abajo)
    for x in (-16, -8, 8, 16):
        caja(neon('foco_piramide', 0xfff3c4, 0.8), x, -1.5, 0, 1.0, 0.6, 0.4)

def castillo():
    """El castillo de cuento: muralla blanca con almenas, puerta y torres
    con tejados de cono rojos, azules y dorados; detrás, las dos torres del
    hotel con sus remates."""
    muro = mat_bloques('muro_castillo', 0xf3ece0, 0xd8cfc0, ancho=1.4, alto=0.7, grosor=0.04, variacion=1.03)
    colores = [mat('cono_rojo', 0xd23a2e, 0.4), mat('cono_azul', 0x2f6bd8, 0.4), mat('cono_oro', 0xf2c23a, 0.3)]
    # las torres del hotel, al fondo
    for s in (-1, 1):
        hotel = ventanas_hotel('hotel_castillo', 0xf3ece0, cristal=0xffd48a)
        caja(hotel, s * 13, 18, 0, 18, 8, 26)
        for x in (s * 13 - 9, s * 13 + 9):
            cil(muro, x, 18, 0, 1.6, 28, 12)
            cil(colores[(1 if s < 0 else 0)], x, 18, 28, 2.0, 4.5, 12, r2=0.0)
    # la muralla
    caja(muro, 0, 3, 0, 36, 6, 10)
    for k in range(18):
        caja(muro, -17 + k * 2, 0.4, 10, 1.1, 1.0, 1.0)                    # almenas
    # la puerta con el puente levadizo
    caja(oscuro(), 0, -0.05, 0, 5, 0.1, 5.5)
    cil(oscuro(), 0, -0.05, 5.5, 2.5, 0.1, 18, eje='Y')
    caja(mat('madera_puente', 0x7a4a2a, 0.8), 0, -2.4, 0, 5, 4.6, 0.3)
    for x in (-2.8, 2.8):
        rama(mat('cadena', 0x3a3a40, 0.4), (x, -4.5, 0.4), (x, -0.2, 7.0), 0.06, 0.06, 6)
    # el foso
    caja(agua(), 0, -2.5, 0, 40, 4.5, 0.12)
    # las torres de delante con sus conos
    for k, x in enumerate((-18, -11, 11, 18)):
        cil(muro, x, 1, 0, 2.2, 15, 14)
        cil(muro, x, 1, 15, 2.6, 0.8, 14)
        cil(colores[k % 3], x, 1, 15.8, 2.7, 6.5, 14, r2=0.0)
        esfera(oro(), x, 1, 22.4, 0.25, 1)
        for z in (5, 10):
            caja(neon('ventana_castillo', 0xffc95a, 0.9), x, -1.15, z, 0.5, 0.1, 1.4)   # saeteras encendidas
    for x in (-5, 5):
        cil(muro, x, 0.5, 0, 1.6, 13, 12)
        cil(colores[2], x, 0.5, 13, 1.9, 4.5, 12, r2=0.0)
        mastil(x, 0.5, 18.5 - 0.5)
    # focos
    for x in (-15, -7, 7, 15):
        caja(neon('foco_castillo', 0xfff3c4, 0.8), x, -1.2, 0, 0.9, 0.5, 0.35)

def fuentes():
    """El hotel italiano en curva detrás de un lago con fuentes, la
    balaustrada y las farolas."""
    hotel = ventanas_hotel('hotel_fuentes', 0xf0dcc0, cristal=0xffd27a)
    teja = mat_franjas('teja_lv', 0xb8502e, 0x9a3f22, 30, eje='X', z0=-30, alto=60)
    # el cuerpo central y las dos alas abiertas hacia la calle
    caja(hotel, 0, 30, 0, 22, 10, 34)
    tejado(teja, 0, 25, 35, 34, 22, 3.0, cumbrera='x')
    for s in (-1, 1):
        o = caja(hotel, s * 19, 26, 0, 18, 10, 30, giro=s * 0.38)
        caja(crema(), s * 19, 26, 30, 18.6, 10.6, 1.0, giro=s * 0.38)
    caja(crema(), 0, 24.6, 0, 24, 1.0, 6)                                   # el bajo con arcos
    for x in (-8, -4, 0, 4, 8):
        cil(oscuro(), x, 24.05, 3.2, 1.3, 0.08, 14, eje='Y')
    # el lago
    caja(agua(), 0, 10, 0, 56, 26, 0.15)
    caja(piedra(), 0, -3.1, 0, 56, 0.6, 0.5)                                # el borde
    # balaustrada
    bal = mat('balaustre', 0xf3ece0, 0.5)
    caja(bal, 0, -3.1, 1.0, 56, 0.5, 0.18)
    for k in range(57):
        cil(bal, -28 + k, -3.1, 0.5, 0.11, 0.5, 6, r2=0.07)
    # farolas italianas
    for x in (-24, -12, 0, 12, 24):
        cil(mat('farola_fuentes', 0x2a2d33, 0.4), x, -3.1, 1.2, 0.1, 3.6, 8)
        esfera(bombilla(), x, -3.1, 5.0, 0.32, 2)
    # los chorros de las fuentes, en una curva sobre el lago
    chorro = neon('chorro_fuente', 0xeaf6ff, 0.55)
    espuma = neon('espuma_fuente', 0xffffff, 0.45)
    for k in range(17):
        t = k / 16
        x = -24 + 48 * t
        y = 6 + 7 * (1 - (2 * t - 1) ** 2)
        alto = 6 + 8 * abs(math.sin(t * math.pi * 3))
        cil(chorro, x, y, 0.1, 0.38, alto, 8, r2=0.1)
        esfera(espuma, x, y, alto, 0.8, 1, esc=(1, 1, 0.7))
    # cipreses a los lados
    for x in (-27, 27):
        for y in (2, 8, 14):
            cipres(x, y, 5)

def cesar():
    """El palacio romano: torre blanca de hotel detrás y delante un templo de
    columnas con luz azul, dos estatuas, una fuente y cipreses."""
    torre = ventanas_hotel('hotel_cesar', 0xf6f1e6, cristal=0x9fd0ff, brillo=0.5)
    caja(torre, 0, 20, 0, 34, 10, 30)
    caja(blanco(), 0, 19.6, 30, 35, 10.8, 1.2)
    fronton(blanco(), 0, 14.6, 31.2, 18, 3.5, 1)
    # el templo
    marmol = mat('marmol_lv', 0xf6f1e6, 0.45)
    caja(marmol, 0, 4, 0, 32, 8, 1.0)                                       # el podio
    escalinata(marmol, 0, 0, 0, 20, 4, huella=0.3, tabica=0.25)
    caja(marmol, 0, 5, 1.0, 30, 6, 9)                                       # la nave
    columnata(marmol, -13, 13, 10, 0.6, 1.0, 0.45, 8.6)
    caja(marmol, 0, 2.5, 9.6, 30, 6.6, 1.4)                                 # el entablamento
    caja(neon('azul_cesar', 0x3a8cff, 1.0), 0, -0.85, 9.7, 29.6, 0.08, 0.3)   # la luz azul
    fronton(marmol, 0, -0.8, 11.0, 30, 3.6, 7)
    caja(neon('azul_cesar', 0x3a8cff, 1.0), 0, -0.86, 11.05, 26, 0.06, 0.12)
    # estatuas sobre pedestal
    for x in (-15.5, 15.5):
        caja(marmol, x, -3, 0, 1.6, 1.6, 2.4)
        cil(marmol, x, -3, 2.4, 0.45, 1.6, 10, r2=0.35)
        esfera(marmol, x, -3, 4.3, 0.32, 2)
        rama(marmol, (x + 0.35, -3, 3.6), (x + 0.9, -3.2, 4.6), 0.1, 0.08, 6)
    # la fuente redonda
    cil(piedra(), 0, -6.5, 0, 3.4, 0.6, 24)
    cil(agua(), 0, -6.5, 0.6, 3.1, 0.02, 24)
    cil(marmol, 0, -6.5, 0.6, 0.4, 1.6, 12)
    cil(neon('chorro_cesar', 0xeaf6ff, 0.55), 0, -6.5, 2.2, 0.25, 2.4, 8, r2=0.05)
    for x in (-21, -18, 18, 21):
        cipres(x, -1, 6)

def torre_eiffel():
    """La torre Eiffel a media escala, encendida en dorado, entre los dos
    cuerpos del casino de tejado azul; delante, el globo aerostático."""
    hierro = neon('hierro_eiffel', 0xc08a4a, 0.35)
    yc = 9
    # las cuatro patas hasta la primera plataforma
    for sx in (-1, 1):
        for sy in (-1, 1):
            rama(hierro, (sx * 8, yc + sy * 8, 0), (sx * 4, yc + sy * 4, 13), 0.9, 0.6, 8)
            rama(hierro, (sx * 4, yc + sy * 4, 13), (sx * 1.6, yc + sy * 1.6, 28), 0.55, 0.35, 8)
    # arcos entre las patas (de cara a la calle)
    for s in (-1, 1):
        rama(hierro, (-6.5, yc + s * 6.5, 6.5), (0, yc + s * 6.5, 9.0), 0.35, 0.35, 6)
        rama(hierro, (0, yc + s * 6.5, 9.0), (6.5, yc + s * 6.5, 6.5), 0.35, 0.35, 6)
    caja(hierro, 0, yc, 13, 10, 10, 1.2)                                    # 1.ª plataforma
    caja(hierro, 0, yc, 28, 4.2, 4.2, 0.9)                                  # 2.ª plataforma
    cil(hierro, 0, yc, 28.9, 1.3, 15, 8, r2=0.35)                           # la aguja
    caja(hierro, 0, yc, 43.6, 1.4, 1.4, 1.2)
    cil(hierro, 0, yc, 44.8, 0.1, 3.0, 6)
    esfera(neon('baliza_eiffel', 0xff3a2e, 1.0), 0, yc, 47.9, 0.25, 1)
    bombillas([(-5, 14.3), (5, 14.3)], paso=0.6, r=0.1, y=yc - 5.1)
    bombillas([(-2.1, 29), (2.1, 29)], paso=0.5, r=0.09, y=yc - 2.2)
    # el casino de los lados: piedra clara y tejado de pizarra azul
    pizarra = mat('pizarra_lv', 0x3f5f8a, 0.5)
    fachada = ventanas_hotel('casino_paris', 0xefe2c8, cristal=0xffd27a, brillo=0.5, paso_x=2.4, paso_z=3.2)
    for s in (-1, 1):
        caja(fachada, s * 14, 6, 0, 12, 12, 9)
        caja(pizarra, s * 14, 6, 9, 12.4, 12.4, 0.4)
        tejado(pizarra, s * 14, 0, 12, 9.4, 12, 3.5, cumbrera='x')
        caja(neon('marquesina_paris', 0xffe066, 0.8), s * 14, -0.4, 3.8, 10, 0.8, 0.5)
    # el globo aerostático, en su pedestal
    franjas = mat_franjas('globo_lv', 0x2f5fd8, 0xf2c23a, 10, eje='Z', z0=4.5, alto=8)
    cil(mat('pie_globo', 0x2a2d33, 0.4), -14, -4, 0, 0.5, 4.5, 10)
    esfera(franjas, -14, -4, 8.2, 3.3, 3, esc=(1, 1, 1.15))
    cil(mat('cesta_globo', 0x8a5a34, 0.8), -14, -4, 3.6, 0.8, 1.0, 10)
    esfera(neon('luz_globo', 0xfff0c0, 0.8), -14, -7.3, 8.2, 0.5, 1)

def noria():
    """La noria gigante: el aro con luces de colores, las cabinas de cristal,
    los radios, las dos patas y el paseo de tiendas a sus pies."""
    zc, R, yc = 24, 20, 6
    aro(neon('aro_noria', 0xff4fd8, 0.9), 0, yc - 0.6, zc, R, 0.45)
    aro(mat('aro_noria_acero', 0xd8dde3, 0.3), 0, yc + 0.6, zc, R, 0.35)
    cable = mat('radio_noria', 0xbfc6cf, 0.3)
    for k in range(28):
        a = k / 28 * math.pi * 2
        x, z = math.cos(a) * R, zc + math.sin(a) * R
        rama(cable, (0, yc, zc), (x, yc, z), 0.06, 0.06, 4)
        # cabina: una burbuja de cristal colgada por fuera del aro
        cx, cz = math.cos(a) * (R + 1.0), zc + math.sin(a) * (R + 1.0)
        esfera(neon('cabina_noria', 0xbfe8ff, 0.45), cx, yc - 1.1, cz, 0.75, 2, esc=(1.25, 1, 0.9))
    cil(mat('cubo_noria', 0x8f99a8, 0.3), 0, yc, zc, 1.6, 2.6, 16, eje='Y')
    esfera(neon('centro_noria', 0x46e0d0, 1.0), 0, yc - 1.4, zc, 0.7, 2)
    pata = mat('pata_noria', 0xe8ecf0, 0.3)
    for s in (-1, 1):
        rama(pata, (s * 9, yc - 3, 0), (0, yc - 1.5, zc), 0.8, 0.5, 10)
        rama(pata, (s * 9, yc + 3, 0), (0, yc + 1.5, zc), 0.8, 0.5, 10)
    # el paseo de tiendas
    paseo = ventanas_hotel('paseo_noria', 0x3a3f52, cristal=0x9fe8ff, brillo=0.6, paso_x=3.0, paso_z=6.0, hueco_x=2.6, hueco_z=4.0)
    for s in (-1, 1):
        caja(paseo, s * 13, 2, 0, 14, 4, 6)
        caja(neon('rotulo_paseo', 0xff4fa0, 0.9), s * 13, -0.1, 6.2, 12, 0.2, 0.4)
    for x in (-4, 4):
        palmera_en(x, -2, 7)

def campanile():
    """El palacio veneciano: arcos blancos abajo, la fachada rosa y la
    loggia; el campanario de ladrillo con el tejado verde y el ángel dorado;
    detrás, la torre del hotel; delante, el canal con una góndola."""
    torre_h = ventanas_hotel('hotel_veneciano', 0xefe2c8, cristal=0xffd27a, brillo=0.5)
    caja(torre_h, 4, 24, 0, 32, 10, 36)
    caja(crema(), 4, 23.6, 36, 33, 10.8, 1.2)
    # el palacio
    rosa = mat_bloques('rosa_palacio', 0xf2c7c0, 0xfbf0ea, ancho=0.8, alto=0.5, grosor=0.06, variacion=1.04)
    caja(rosa, 6, 4, 7, 30, 8, 8)
    caja(blanco(), 6, 4, 0, 30, 8, 7)
    for k in range(9):                                                      # arcos de abajo
        x = 6 - 13 + k * 3.25
        caja(oscuro(), x, -0.03, 0.2, 2.0, 0.06, 4.0)
        cil(oscuro(), x, -0.03, 4.2, 1.0, 0.06, 12, eje='Y')
    caja(blanco(), 6, -0.4, 6.6, 30, 1.0, 0.5)                               # la loggia
    for k in range(17):
        x = 6 - 14 + k * 1.75
        cil(blanco(), x, -0.6, 7.1, 0.16, 2.6, 8)
    for k in range(5):
        x = 6 - 10 + k * 5
        caja(neon('ventana_palacio', 0xffc95a, 0.8), x, -0.05, 10.6, 1.3, 0.1, 2.2)
    for k in range(20):                                                      # almenas de encaje
        caja(blanco(), 6 - 14.25 + k * 1.5, 4, 15, 0.7, 7.6, 0.8)
    # el campanario
    ladrillo = mat_bloques('ladrillo_campanile', 0xb8604a, 0x8f4a38, ancho=0.5, alto=0.22, grosor=0.02, variacion=1.06)
    cx, cy = -16, 3
    caja(ladrillo, cx, cy, 0, 6, 6, 30)
    caja(blanco(), cx, cy, 30, 6.6, 6.6, 0.6)
    caja(blanco(), cx, cy, 30.6, 6, 6, 5)
    for s in (-1, 1):
        caja(neon('campana_luz', 0xffd27a, 0.8), cx + s * 1.4, cy - 3.02, 31.3, 1.1, 0.06, 3.4)
    caja(blanco(), cx, cy, 35.6, 6.6, 6.6, 0.6)
    caja(ladrillo, cx, cy, 36.2, 5.4, 5.4, 4)
    piramide(mat('tejado_verde', 0x4f9a7a, 0.5), cx, cy, 40.2, 5.6, 7)
    esfera(oro(), cx, cy, 47.6, 0.5, 2)
    # el canal y la góndola
    caja(mat('agua_canal', 0x2f8f9a, 0.1), -2, -3.5, 0, 46, 3.6, 0.12)
    caja(blanco(), -2, -1.6, 0, 46, 0.3, 0.6)
    gondola = mat('gondola', 0x1d1e24, 0.4)
    esfera(gondola, -6, -3.5, 0.3, 0.6, 2, esc=(6, 1, 0.5))
    rama(gondola, (-9.5, -3.5, 0.4), (-10.6, -3.5, 1.4), 0.15, 0.08, 6)
    cil(mat_franjas('rayas_gondolero', 0xffffff, 0x1d1e24, 8, eje='Z', z0=0.6, alto=0.8), -3.5, -3.5, 0.6, 0.25, 0.8, 10)
    esfera(mat('piel_gondolero', 0xf0c8a0, 0.6), -3.5, -3.5, 1.65, 0.2, 2)
    cil(mat('sombrero_gondolero', 0xf2d27a, 0.6), -3.5, -3.5, 1.8, 0.32, 0.08, 12)
    rama(mat('remo', 0x8a5a34, 0.8), (-3.2, -3.5, 1.2), (-2.2, -3.5, -0.2), 0.04, 0.04, 6)
    # farolillos
    for x in (-24, 12, 20):
        cil(mat('poste_canal', 0x2a2d33, 0.4), x, -1.6, 0.6, 0.08, 3.0, 8)
        esfera(bombilla(), x, -1.6, 3.8, 0.28, 2)

def hotel_trump():
    """La torre dorada del hotel Trump: el cristal dorado encendido, las letras
    TRUMP arriba, la marquesina dorada de la entrada, la alfombra roja, las
    banderas, dos fuentes y palmeras."""
    oro_cristal = ventanas_luz('cristal_trump', 0xf2c25a, 0xb88a2a, brillo=0.42,
                               paso_x=1.5, paso_z=3.0, hueco_x=1.3, hueco_z=2.6, variacion=1.12)
    W, D, H = 24, 12, 64
    caja(oro_cristal, 0, 14, 0, W, D, H)
    caja(oro(), 0, 14, H, W + 0.6, D + 0.6, 1.0)                           # remate
    caja(oro_cristal, 0, 14, H + 1, W - 4, D - 3, 3.5)
    for s in (-1, 1):                                                       # aristas
        caja(oro(), s * W / 2, 8, 0, 0.6, 0.6, H)
    texto(neon('letras_trump', 0xfff3c0, 1.0), 'TRUMP', 0, 7.7, H - 5.2, tam=4.6, prof=0.3)
    # el cuerpo bajo, de piedra crema y oro
    base = mat_bloques('piedra_trump', 0xf3e6c8, 0xd9c69c, ancho=2.0, alto=1.0, grosor=0.04, variacion=1.03)
    caja(base, 0, 7, 0, 40, 14, 8)
    caja(oro(), 0, 7, 8, 40.6, 14.6, 0.6)
    for x in (-16, -10, 10, 16):
        caja(neon('escaparate_trump', 0xffd27a, 0.7), x, -0.05, 1.0, 4, 0.1, 5)
    # la entrada: puertas doradas y marquesina con columnas
    puertas = ventanas_luz('puerta_trump', 0xffdf9a, 0xb88a2a, brillo=0.5, paso_x=1.5, paso_z=5.2, hueco_x=1.3, hueco_z=4.6, variacion=1.05)
    caja(puertas, 0, -0.05, 0, 6, 0.1, 5)
    caja(oro(), 0, -4, 5.2, 16, 8, 0.7)
    caja(neon('borde_marquesina', 0xfff3c0, 0.9), 0, -8.02, 5.25, 16, 0.08, 0.3)
    texto(neon('letras_marquesina', 0xffd86a, 0.9), 'TRUMP', 0, -8.05, 6.5, tam=1.6, prof=0.15)
    for x in (-7, 7):
        for y in (-7.4, -1):
            cil(oro(), x, y, 0, 0.3, 5.2, 12)
    for x in range(-6, 7, 2):
        esfera(bombilla(), x, -4, 5.1, 0.18, 1)
    # la alfombra roja hasta la acera, con sus postes
    caja(mat('alfombra_trump', 0xc0262c, 0.9), 0, -9, 0, 3.6, 18, 0.06)
    for y in (-16, -12, -8):
        for s in (-1, 1):
            cil(oro(), s * 2.4, y, 0, 0.08, 1.0, 8)
            esfera(oro(), s * 2.4, y, 1.0, 0.13, 1)
    cuerda = mat('cuerda_trump', 0x8a1a22, 0.6)
    for s in (-1, 1):
        rama(cuerda, (s * 2.4, -16, 0.9), (s * 2.4, -12, 0.9), 0.05, 0.05, 6)
        rama(cuerda, (s * 2.4, -12, 0.9), (s * 2.4, -8, 0.9), 0.05, 0.05, 6)
    # banderas, fuentes y palmeras
    for x in (-10, 10):
        mastil(x, -9, 11)
    for x in (-16, 16):
        cil(piedra(), x, -9, 0, 2.6, 0.6, 20)
        cil(agua(), x, -9, 0.6, 2.3, 0.02, 20)
        cil(neon('chorro_trump', 0xeaf6ff, 0.55), x, -9, 0.6, 0.25, 3.4, 8, r2=0.06)
        esfera(neon('espuma_trump', 0xffffff, 0.45), x, -9, 4.0, 0.6, 1, esc=(1, 1, 0.7))
    for x in (-21, 21):
        palmera_en(x, -5, 9)


PIEZAS = {
    'cartel_vegas':  (cartel_vegas,  'vegas', dict(lado=1024, bisel=0.0)),
    'piramide':      (piramide_lv,   'vegas', dict(lado=1024, segmentos=2)),
    'castillo':      (castillo,      'vegas', dict(lado=1024, segmentos=2)),
    'fuentes':       (fuentes,       'vegas', dict(lado=1024, segmentos=2)),
    'cesar':         (cesar,         'vegas', dict(lado=1024, segmentos=2)),
    'torre_eiffel':  (torre_eiffel,  'vegas', dict(lado=1024, segmentos=2)),
    'noria':         (noria,         'vegas', dict(lado=1024, bisel=0.0)),
    'campanile':     (campanile,     'vegas', dict(lado=1024, segmentos=2)),
    'hotel_trump':   (hotel_trump,   'vegas', dict(lado=2048, segmentos=2)),
}

correr(PIEZAS)
