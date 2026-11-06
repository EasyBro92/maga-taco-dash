# Piezas de los «momentos» (06/11/2026).
#
#   blender -b -P blender/momentos.py -- [pieza ...] [--rapido]
#
# Isidro: «los mapas se hacen aburridos... más cosas, muchas más, que no sea
# tan repetitivo». Eligió doce momentos de unos 10 segundos, uno cada 20 s.
# Estas son las piezas nuevas que necesitan (el resto se reutiliza):
#   rampa_salto   la rampa gigante: te lanza por los aires (una por carril)
#   camion        el convoy: como el autobús (rampa de 2.2, techo a 1.55,
#                 10.2 de largo), para correr por los techos
#   avion         el avión presidencial que suelta la lluvia de tacos
#   arco_premio   «elige tu premio»: un arco por carril con el premio dentro
#   carrito_golf  el vehículo de Phoenix: se va de pie en la plataforma de atrás
#
# Mismas reglas que obstaculos3.py: caben en un carril (x de -1 a 1), miran al
# jugador por -y (en el juego, +z), el origen es el centro del carril a ras de
# suelo y lo que se sube empieza en y = 0 y se alarga hacia +y.

import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import *

def blanco():  return mat('blanco', 0xffffff, 0.5)
def negro():   return mat('negro', 0x1d1f25, 0.4)
def gris():    return mat('gris', 0x9aa1aa, 0.5)
def rojo():    return mat('rojo', 0xe8303a, 0.45)
def azul():    return mat('azul', 0x2350c8, 0.45)
def marino():  return mat('marino', 0x1b2d6b, 0.45)
def oro():     return mat('oro', 0xf2c230, 0.25)
def cristal(): return mat('cristal', 0x3a6fb0, 0.15)
def neumatico(): return mat('neumatico', 0x1d1e21, 0.8)

def rayas(nombre, c1, c2, n, x0, ancho, eje='X'):
    return mat_franjas(nombre, c1, c2, n, eje=eje, z0=x0, alto=ancho)

def rueda(x, y, r=0.3, ancho=0.22, z=None):
    z = r if z is None else z
    cil(neumatico(), x, y, z, r, ancho, 16, eje='X')
    cil(mat('llanta', 0xd3d6da, 0.3), x + (0.12 if x > 0 else -0.12), y, z, r * 0.5, 0.02, 12, eje='X')

def cuña(nombre, m, w, largo, alto, y0=0.0):
    """Cuña de rampa: sube de 0 en y0 a `alto` en y0 + largo."""
    me = bpy.data.meshes.new(nombre)
    bm = bmesh.new()
    pts = []
    for x in (-w / 2, w / 2):
        pts.append([bm.verts.new((x, y0, 0)), bm.verts.new((x, y0 + largo, 0)), bm.verts.new((x, y0 + largo, alto))])
    a, b = pts
    bm.faces.new(a); bm.faces.new(b[::-1])
    for i in range(3):
        j = (i + 1) % 3
        bm.faces.new((a[j], a[i], b[i], b[j]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(nombre, me)
    bpy.context.scene.collection.objects.link(o)
    from comun import _poner
    return _poner(o, m)

def estrella(m, x, y, z, r, grosor=0.08, eje='Y'):
    """Estrella de cinco puntas plana; mira a -y (eje='Y') o hacia arriba (eje='Z')."""
    me = bpy.data.meshes.new('estrella')
    bm = bmesh.new()
    def p(ang, rr, d):
        u, v = math.sin(ang) * rr, math.cos(ang) * rr
        if eje == 'X': return (x + d, y + u, z + v)
        return (x + u, y + d, z + v) if eje == 'Y' else (x + u, y + v, z + d)
    for d in (0, grosor):
        anillo = [bm.verts.new(p(i * math.pi / 5, r if i % 2 == 0 else r * 0.42, d)) for i in range(10)]
        centro = bm.verts.new(p(0, 0, d))
        for i in range(10):
            bm.faces.new((centro, anillo[i], anillo[(i + 1) % 10]) if d == 0 else (centro, anillo[(i + 1) % 10], anillo[i]))
        if d == 0: abajo = anillo
        else: arriba = anillo
    for i in range(10):
        j = (i + 1) % 10
        bm.faces.new((abajo[i], abajo[j], arriba[j], arriba[i]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new('estrella', me)
    bpy.context.scene.collection.objects.link(o)
    from comun import _poner
    return _poner(o, m)


# ---------------------------------------------------------------- la rampa
def rampa_salto():
    """Rampa de saltos con la bandera: sube de 0 a 1.6 m en 4.4 m. Se ponen
    tres, una por carril, y al llegar arriba te lanza por los aires."""
    W, L, H = 2.16, 4.4, 1.6
    cuña('rampa', rayas('rampa_franjas', 0xe8303a, 0xffffff, 7, -W / 2, W), W, L, H)
    # Los costados azules con estrellas blancas (es lo que se ve entre carril y carril).
    for s in (-1, 1):
        cuña('costado', azul(), 0.04, L, H + 0.02).location.x = s * (W / 2 + 0.02)
        for k in range(5):
            y = 0.9 + k * 0.75
            estrella(blanco(), s * (W / 2 + 0.05), y, H * y / L * 0.55, 0.12, 0.02 * s, eje='X')
    # El borde de arriba, amarillo y negro, y el labio del suelo.
    caja(rayas('labio_rampa', 0xffd21a, 0x1d1f25, 8, -W / 2, W), 0, L - 0.08, H - 0.04, W, 0.16, 0.06)
    caja(rayas('pie_rampa', 0xffd21a, 0x1d1f25, 8, -W / 2, W), 0, 0.12, 0.0, W, 0.24, 0.03)
    # Detrás, las patas de hierro (se ven al pasar volando por encima).
    for s in (-1, 1):
        cil(gris(), s * (W / 2 - 0.15), L - 0.1, 0, 0.06, H - 0.04, 8)
    caja(gris(), 0, L - 0.1, H * 0.45, W - 0.3, 0.06, 0.06)


# ---------------------------------------------------------------- el convoy
def camion():
    """Camión del convoy de la campaña: como el autobús (rampa trasera de 2.2,
    techo a 1.55 hasta 10.2), pero de caja plateada y cabina roja."""
    W, H, R, L = 2.0, 1.55, 2.2, 10.2
    cuña('rampa', rayas('rampa_rayas', 0xffd21a, 0x1d1f25, 9, 0, R, eje='Y'), W - 0.1, R, H)
    # La caja: plateada con nervios, una franja roja y otra azul.
    caja(mat('plata', 0xc9ced6, 0.35), 0, R + 2.9, 0.42, W, 5.8, H - 0.42)
    for k in range(9):
        caja(mat('nervio', 0xaab0b9, 0.4), 0, R + 0.35 + k * 0.65, 0.42, W + 0.03, 0.06, H - 0.44)
    for s in (-1, 1):
        caja(rojo(), s * (W / 2 + 0.02), R + 2.9, 0.75, 0.02, 5.7, 0.16)
        caja(azul(), s * (W / 2 + 0.02), R + 2.9, 0.58, 0.02, 5.7, 0.12)
    # El techo, que es lo que se pisa: chapa con «MAGA» en grande.
    caja(mat('techo_camion', 0xdfe3e8, 0.4), 0, R + 2.9, H - 0.03, W - 0.04, 5.8, 0.04)
    for k, letra in enumerate('MAGA'):
        o = texto(rojo(), letra, 0, 0, 0, tam=0.95, prof=0.03)
        o.rotation_euler = (0, 0, 0)
        o.location = (0, R + 0.9 + (3 - k) * 1.3, H + 0.01)   # la M la mas lejos: se lee de lejos a cerca
    # La cabina, roja, con el techo a la misma altura (se sigue corriendo por encima).
    caja(rojo(), 0, R + 6.6, 0.35, W, 1.4, H - 0.35)
    caja(cristal(), 0, R + 7.31, 0.95, W - 0.3, 0.02, 0.5)
    caja(mat('cromo', 0xd6dade, 0.2), 0, R + 7.33, 0.4, W - 0.2, 0.04, 0.4)
    for s in (-1, 1):
        caja(cristal(), s * (W / 2 + 0.01), R + 6.75, 0.95, 0.02, 0.7, 0.45)
        cil(mat('cromo', 0xd6dade, 0.2), s * (W / 2 - 0.1), R + 6.0, H, 0.07, 0.5, 10)   # los tubos de escape
        caja(mat('chasis', 0x2a2c31, 0.6), s * (W / 2 - 0.2), R + 3.0, 0.25, 0.25, 7.6, 0.2)
        for y in (R + 0.6, R + 1.5, R + 4.6, R + 6.9):
            rueda(s * (W / 2 - 0.12), y, 0.38, 0.26)
    # La parte de atrás sobre la rampa: pilotos y la matrícula.
    for s in (-1, 1):
        caja(mat('piloto', 0xc0262c, 0.3), s * 0.82, R - 0.02, 0.5, 0.18, 0.04, 0.2)
    texto(azul(), 'MAGA EXPRESS', 0, R - 0.03, 1.38, tam=0.13, prof=0.02)


# ---------------------------------------------------------------- el avión
def avion():
    """El avión presidencial (azul claro y blanco, con la franja azul oscuro).
    Vuela muy alto: lo que más se ve es la panza y las alas. Morro hacia +y."""
    celeste = mat('celeste', 0x6fb3dd, 0.35)
    L, R = 26.0, 1.55
    cil(celeste, 0, 0, 0, R, L, 24, eje='Y')
    cil(blanco(), 0, 0, 0.45, R + 0.01, L - 0.4, 24, eje='Y')
    cil(marino(), 0, 0, 0.05, R + 0.025, L - 0.6, 24, eje='Y').scale = (1, 1, 0.12)
    esfera(celeste, 0, L / 2, 0, R, 3, esc=(1, 1.9, 1))                       # el morro
    esfera(blanco(), 0, L / 2 + 0.2, 0.45, R * 0.98, 3, esc=(1, 1.75, 0.75))
    esfera(blanco(), 0, L / 2 - 3.5, 1.15, R * 0.9, 3, esc=(0.85, 3.6, 0.7))  # la joroba de arriba
    cil(celeste, 0, -L / 2 - 2.6, 0.3, R, 5.2, 24, r2=0.35, eje='Y')   # la cola
    # Las alas, con flecha, y los cuatro motores.
    ala = mat('ala', 0xd7dde4, 0.4)
    for s in (-1, 1):
        caja(ala, s * 7.2, -1.0, -0.75, 13.5, 4.2, 0.32, giro=-s * 0.55)
        caja(ala, s * 3.6, -L / 2 - 2.8, 0.4, 6.0, 2.0, 0.22, giro=-s * 0.55)    # los timones de cola
        for k, dx in enumerate((4.6, 9.0)):
            x = s * dx
            y = -(dx - 7.2) * 0.61
            cil(mat('motor', 0xb9c1ca, 0.35), x, y, -1.55, 0.6, 2.6, 16, eje='Y')
            cil(negro(), x, y + 1.31, -1.55, 0.5, 0.02, 16, eje='Y')
    # La aleta de cola con la bandera.
    caja(celeste, 0, -L / 2 - 3.2, 0.8, 0.3, 3.4, 4.2, inclina=-0.45)
    caja(rayas('bandera_cola', 0xe8303a, 0xffffff, 7, 1.6, 2.2, eje='Z'), 0, -L / 2 - 3.9, 1.9, 0.34, 1.7, 2.2, inclina=-0.45)
    # Las letras de los costados.
    for s in (-1, 1):
        o = texto(marino(), 'UNITED STATES OF AMERICA', 0, 0, 0, tam=0.7, prof=0.03)
        o.rotation_euler = (math.pi / 2, 0, -s * math.pi / 2)
        o.location = (s * (R + 0.04), 1.0, 0.95)


# ---------------------------------------------------------------- elige tu premio
def arco_premio():
    """Arco de premio: dos postes con bombillas, el travesaño azul con
    estrellas y una estrella dorada encima. El premio flota dentro."""
    W, H = 2.0, 3.0
    for s in (-1, 1):
        cil(rayas('poste_premio', 0xe8303a, 0xffffff, 10, 0, H, eje='Z'), s * W / 2, 0, 0, 0.11, H, 12)
        cil(oro(), s * W / 2, 0, 0, 0.17, 0.12, 12)
        for k in range(6):
            esfera(luz('bombilla', 0xffe6a8, 1.4), s * (W / 2 - 0.13), -0.02, 0.45 + k * 0.45, 0.05, 1)
    caja(azul(), 0, 0, H, W + 0.3, 0.3, 0.42)
    for k in range(5):
        estrella(blanco(), -0.8 + k * 0.4, -0.17, H + 0.21, 0.11, 0.02)
    caja(rojo(), 0, 0, H - 0.08, W + 0.34, 0.32, 0.08)
    estrella(oro(), 0, -0.05, H + 0.95, 0.48, 0.1)


# ---------------------------------------------------------------- el carrito de golf
def carrito_golf():
    """Carrito de golf blanco, visto por detrás, con la bolsa de palos en la
    plataforma de atrás (ahí va él, de pie, agarrado al techo)."""
    W, L = 1.3, 2.5
    blanco_c = mat('carrito', 0xf4f4f0, 0.4)
    caja(blanco_c, 0, L / 2 + 0.2, 0.28, W, L - 0.4, 0.42)
    caja(mat('plataforma', 0x2a2c31, 0.6), 0, 0.25, 0.24, W - 0.1, 0.5, 0.12)     # la plataforma de atrás
    caja(mat('asiento', 0x7a1f24, 0.5), 0, 1.15, 0.7, W - 0.15, 0.55, 0.14)
    caja(mat('asiento', 0x7a1f24, 0.5), 0, 0.92, 0.84, W - 0.15, 0.1, 0.45)
    caja(blanco_c, 0, L - 0.25, 0.7, W - 0.1, 0.5, 0.35)                          # el morro
    for s in (-1, 1):
        rueda(s * (W / 2 - 0.05), 0.55, 0.22, 0.16)
        rueda(s * (W / 2 - 0.05), L - 0.35, 0.22, 0.16)
        cil(gris(), s * (W / 2 - 0.08), 0.62, 0.7, 0.03, 1.25, 8)                    # los postes del techo
        cil(gris(), s * (W / 2 - 0.08), L - 0.5, 0.95, 0.03, 1.0, 8)
        caja(mat('piloto', 0xc0262c, 0.3), s * 0.45, 0.02, 0.42, 0.14, 0.03, 0.08)
    caja(mat('toldo', 0x2e7d4a, 0.5), 0, 1.3, 1.95, W + 0.1, 2.0, 0.07)           # el toldo verde
    caja(cristal(), 0, L - 0.5, 1.0, W - 0.2, 0.03, 0.9, inclina=-0.15)
    # La bolsa de palos y los palos.
    cil(mat('bolsa_golf', 0xe8303a, 0.5), 0.35, 0.2, 0.3, 0.17, 0.85, 12)
    for k in range(4):
        rama(gris(), (0.3 + (k % 2) * 0.1, 0.15 + (k // 2) * 0.1, 1.1), (0.28 + (k % 2) * 0.14, 0.1 + (k // 2) * 0.12, 1.4), 0.015, 0.015, 5)
        cil(negro(), 0.28 + (k % 2) * 0.14, 0.1 + (k // 2) * 0.12, 1.4, 0.04, 0.08, 8)
    texto(rojo(), 'TRUMP NATIONAL', 0, 0.19, 0.55, tam=0.08, prof=0.01)


PIEZAS = {
    'rampa_salto':  (rampa_salto,  'obstaculos', dict(lado=512, bisel=0.0)),
    'camion':       (camion,       'obstaculos', dict(lado=1024)),
    'avion':        (avion,        'obstaculos', dict(lado=1024, suelo=False)),
    'arco_premio':  (arco_premio,  'obstaculos', dict(lado=256, bisel=0.0)),
    'carrito_golf': (carrito_golf, 'obstaculos', dict(lado=512, bisel=0.0)),
}

correr(PIEZAS)
