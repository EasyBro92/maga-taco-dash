# Washington D.C. en dibujo animado (20/10/2026). Ver comun.py.
#
#   blender -b -P blender/dc.py -- [casa_blanca capitolio ...] [--rapido]
#
# Fachadas: casa_blanca, capitolio, lincoln, federal, georgetown (la fachada en
# y = 0 mirando a -y, todo lo demás detrás). Acera: cerezo, farola. Fondo:
# monumento (el obelisco, para la capa lejana).

import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import *
from mathutils import Vector

# ---------------------------------------------------------------- colores
def liso():      return mat('blanco_liso', 0xfbf9f2, 0.5)
def marco():     return mat('marco', 0xffffff)
def cesped():    return mat('cesped', 0x6cc04a, 0.9)
def camino():    return mat('camino', 0xdcd3bf, 0.9)
def hierro():    return mat('hierro', 0x23272c, 0.4)
def bronce():    return mat('bronce', 0x56705f, 0.4)
def pizarra():   return mat('pizarra', 0x5b6573, 0.7)
def tejado():    return mat('tejado', 0x9aa3ad, 0.7)
def sombra():    return mat('sombra', 0x34333a, 0.9)

def bandera(x, y, z, alto=1.4, ancho=0.9):
    """Asta con la bandera de EE. UU. (franjas rojas y blancas y el cuadro azul)."""
    cil(mat('asta', 0xd8d8d8, 0.3), x, y, z, 0.035, alto, 8)
    esfera(mat('dorado', 0xf2c23a, 0.3), x, y, z + alto + 0.04, 0.06, 1)
    fh = ancho * 0.55
    z0 = z + alto - fh
    caja(mat_franjas(f'franjas{z0:.2f}', 0xd8283a, 0xffffff, 7, z0=z0, alto=fh), x + ancho / 2 + 0.03, y, z0, ancho, 0.03, fh)
    caja(mat('azul_bandera', 0x1f3c88), x + 0.03 + ancho * 0.21, y - 0.02, z0 + fh * 0.46, ancho * 0.42, 0.02, fh * 0.54)

def reja(x0, x1, y, alto=0.9, paso=0.32, hueco=(0, 0)):
    """Verja de barrotes negros; `hueco` = (centro, ancho) de la puerta abierta."""
    n = int((x1 - x0) / paso)
    for i in range(n + 1):
        x = x0 + i * paso
        if hueco[1] and abs(x - hueco[0]) < hueco[1] / 2:
            continue
        cil(hierro(), x, y, 0, 0.025, alto, 6)
        esfera(mat('dorado', 0xf2c23a, 0.3), x, y, alto, 0.04, 1)
    for a, b in ((x0, hueco[0] - hueco[1] / 2), (hueco[0] + hueco[1] / 2, x1)) if hueco[1] else ((x0, x1),):
        caja(hierro(), (a + b) / 2, y, alto - 0.12, b - a, 0.04, 0.05)
        caja(hierro(), (a + b) / 2, y, 0.12, b - a, 0.04, 0.05)

def rama(m, p0, p1, r0, r1, lados=8):
    p0, p1 = Vector(p0), Vector(p1)
    d = p1 - p0
    bpy.ops.mesh.primitive_cone_add(vertices=lados, radius1=r0, radius2=r1, depth=d.length,
                                    location=(p0 + p1) / 2)
    o = bpy.context.object
    o.rotation_mode = 'QUATERNION'
    o.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(d.normalized())
    return _poner_rama(o, m)

def _poner_rama(o, m):
    from comun import _poner
    return _poner(o, m)


# ---------------------------------------------------------------- Casa Blanca
def casa_blanca():
    W, H, D = 6.6, 3.4, 3.6
    piedra = mat_bloques('blanco_casa', 0xf7f4ea, 0xe0d9c6, ancho=0.8, alto=0.3, grosor=0.008)
    caja(piedra, 0, D / 2, 0, W, D, H)
    caja(liso(), 0, D / 2, H, W + 0.2, D + 0.2, 0.18)                  # cornisa
    caja(tejado(), 0, D / 2 + 0.2, H + 0.18, W - 0.8, D - 0.8, 0.35)
    caja(liso(), 0, 0.05, H + 0.18, W + 0.1, 0.18, 0.08)              # balaustrada
    caja(liso(), 0, 0.05, H + 0.5, W + 0.1, 0.18, 0.08)
    x = -W / 2 + 0.15
    while x < W / 2 - 0.1:
        cil(liso(), x, 0.05, H + 0.26, 0.045, 0.24, 8, r2=0.03)
        x += 0.26
    for s in (-1, 1):                                                  # chimeneas
        caja(liso(), s * 2.1, 2.4, H, 0.3, 0.6, 0.95)
    # dos plantas de 7 ventanas; la puerta en el centro
    for i in range(7):
        x = -W / 2 + 0.6 + i * (W - 1.2) / 6
        if i == 3:
            puerta(0, 0.1, 0.75, 1.45)
        else:
            ventana(x, 0.5, 0.55, 1.05, remate='fronton' if i % 2 else 'cornisa')
        ventana(x, 2.05, 0.5, 0.9, remate='cornisa')
    # pórtico norte: cuatro columnas y frontón
    caja(liso(), 0, -0.8, 0, 3.7, 1.6, 0.22)
    columnata(liso(), -1.5, 1.5, 4, -1.3, 0.22, 0.15, 3.0)
    caja(liso(), 0, -0.75, 3.22, 3.8, 1.7, 0.32)
    fronton(liso(), 0, -1.6, 3.54, 3.9, 0.85, 1.7)
    cil(mat('farolillo', 0xffe7a1, 0.3), 0, -0.6, 2.4, 0.13, 0.45, 8)  # el farol del pórtico
    escalinata(liso(), 0, -1.6, 0, 1.8, 2, huella=0.2, tabica=0.11)
    # alas bajas con su columnata
    for s in (-1, 1):
        cx = s * (W / 2 + 1.35)
        caja(piedra, cx, 1.6, 0, 2.7, 2.4, 1.8)
        caja(liso(), cx, 1.45, 1.8, 2.8, 2.7, 0.16)
        columnata(liso(), cx - 1.1, cx + 1.1, 5, 0.3, 0, 0.08, 1.8)
        for k in (-0.7, 0.7):
            ventana(cx + k, 0.5, 0.45, 0.8, y=0.4)
    bandera(0, 1.8, H + 0.53, alto=1.3, ancho=0.85)
    # el jardín con su verja
    caja(cesped(), 0, -1.6, 0, 12.6, 3.2, 0.05)
    caja(camino(), 0, -2.45, 0, 1.6, 1.7, 0.07)
    for s in (-1, 1):
        cil(mat('flores', 0xff4f6d, 0.8), s * 3.4, -1.8, 0, 0.75, 0.16, 16)
        cil(mat('flores2', 0xffd23f, 0.8), s * 3.4, -1.8, 0.1, 0.4, 0.14, 16)
        caja(mat('seto', 0x3f9a3a, 0.9), s * 4.9, -0.35, 0, 2.6, 0.45, 0.45)
    reja(-6.2, 6.2, -3.15, hueco=(0, 1.6))


# ---------------------------------------------------------------- Capitolio
def capitolio():
    marmol = mat_bloques('marmol', 0xf3efe4, 0xdcd4c1, ancho=0.85, alto=0.3, grosor=0.007)
    zocalo = mat_bloques('basamento', 0xe2d9c6, 0xc2b8a2, ancho=0.7, alto=0.25, grosor=0.015)
    caja(zocalo, 0, 1.6, 0, 16.2, 4.6, 0.6)                            # la terraza
    # cuerpo central y pórtico de ocho columnas
    caja(marmol, 0, 2.0, 0.6, 5.6, 4.0, 2.6)
    caja(liso(), 0, 2.0, 3.2, 5.9, 4.3, 0.16)
    for i in range(5):
        x = -2.4 + i * 1.2
        if abs(x) > 2.2:
            ventana(x, 1.0, 0.5, 0.85)
            ventana(x, 2.15, 0.45, 0.7)
    puerta(0, 0.6, 0.8, 1.5, color=0x6b5530)
    columnata(liso(), -2.1, 2.1, 8, -0.9, 0.6, 0.14, 2.2)
    caja(liso(), 0, -0.45, 2.8, 4.9, 1.25, 0.3)
    fronton(liso(), 0, -1.08, 3.1, 5.0, 0.8, 1.25)
    escalinata(liso(), 0, -0.7, 0, 3.6, 5, huella=0.3, tabica=0.12)
    # alas de unión y las cámaras de los extremos
    for s in (-1, 1):
        cx = s * 3.9
        caja(marmol, cx, 2.0, 0.6, 2.2, 3.4, 2.4)
        caja(liso(), cx, 2.0, 3.0, 2.35, 3.55, 0.14)
        for k in (-0.55, 0.55):
            ventana(cx + k, 1.0, 0.42, 0.8, y=0.3)
            ventana(cx + k, 2.05, 0.38, 0.6, y=0.3)
        ex = s * 6.5
        caja(marmol, ex, 1.8, 0.6, 3.0, 3.8, 2.6)
        caja(liso(), ex, 1.8, 3.2, 3.15, 3.95, 0.14)
        for k in (-1.15, 1.15):
            ventana(ex + k, 1.0, 0.4, 0.8, y=-0.1)
            ventana(ex + k, 2.15, 0.36, 0.6, y=-0.1)
        columnata(liso(), ex - 0.8, ex + 0.8, 4, -0.55, 0.6, 0.11, 2.0)
        caja(liso(), ex, -0.35, 2.6, 2.1, 0.62, 0.24)
        fronton(liso(), ex, -0.66, 2.84, 2.2, 0.5, 0.62)
    # la cúpula: tambor, columnata en anillo, ático, cúpula, linterna y la estatua
    cy, z = 2.0, 3.36
    cil(liso(), 0, cy, z, 2.05, 0.5, 32)
    cil(marmol, 0, cy, z + 0.5, 1.82, 1.3, 32)
    for i in range(20):
        a = i / 20 * math.tau
        cil(liso(), math.cos(a) * 2.02, cy + math.sin(a) * 2.02, z + 0.5, 0.075, 1.3, 8)
    for i in range(10):                                                # ventanas del tambor
        a = (i + 0.5) / 10 * math.tau
        caja(mat('cristal', 0x2d4f86, 0.25), math.cos(a) * 1.81, cy + math.sin(a) * 1.81, z + 0.75,
             0.4, 0.05, 0.75, giro=a + math.pi / 2)
    cil(liso(), 0, cy, z + 1.8, 2.2, 0.22, 32)
    cil(liso(), 0, cy, z + 2.02, 1.85, 0.5, 32)
    cupula(mat('cupula', 0xfbf8ef, 0.45), 0, cy, z + 2.52, 1.9, 2.1, lados=32, aros=10)
    for i in range(16):                                                # nervios
        a = i / 16 * math.tau
        for k in range(8):
            t0, t1 = k / 8 * math.pi / 2, (k + 1) / 8 * math.pi / 2
            p0 = (math.cos(a) * 1.92 * math.cos(t0), cy + math.sin(a) * 1.92 * math.cos(t0), z + 2.52 + 2.12 * math.sin(t0))
            p1 = (math.cos(a) * 1.92 * math.cos(t1), cy + math.sin(a) * 1.92 * math.cos(t1), z + 2.52 + 2.12 * math.sin(t1))
            if k < 7:
                rama(mat('nervio', 0xe9e3d3, 0.5), p0, p1, 0.045, 0.045, 4)
    zl = z + 4.5
    cil(liso(), 0, cy, zl, 0.4, 0.65, 16)
    for i in range(8):
        a = i / 8 * math.tau
        cil(liso(), math.cos(a) * 0.42, cy + math.sin(a) * 0.42, zl, 0.04, 0.6, 6)
    cupula(liso(), 0, cy, zl + 0.65, 0.44, 0.35, lados=16, aros=4)
    cil(bronce(), 0, cy, zl + 0.98, 0.11, 0.5, 8, r2=0.07)
    esfera(bronce(), 0, cy, zl + 1.55, 0.1, 1)
    bandera(-6.5, 2.0, 3.34, alto=1.1, ancho=0.7)
    bandera(6.5, 2.0, 3.34, alto=1.1, ancho=0.7)
    # césped y paseo
    caja(cesped(), 0, -2.3, 0, 16.2, 3.2, 0.05)
    caja(camino(), 0, -3.0, 0, 3.8, 1.8, 0.07)
    for s in (-1, 1):
        for k in (2.6, 5.0, 7.2):
            esfera(mat('seto', 0x3f9a3a, 0.9), s * k, -3.2, 0.3, 0.38, 2)


# ---------------------------------------------------------------- Lincoln
def lincoln():
    marmol = mat_bloques('marmol_l', 0xf2eee5, 0xdcd5c5, ancho=1.1, alto=0.35, grosor=0.007)
    caja(marmol, 0, 2.3, 0, 9.2, 5.0, 1.0)
    escalinata(liso(), 0, -0.2, 0, 4.4, 6, huella=0.26, tabica=1 / 6)
    caja(marmol, 0, 2.6, 1.0, 6.4, 3.4, 3.3)                          # la cella
    caja(sombra(), 0, 0.88, 1.0, 2.4, 0.04, 2.7)                       # la entrada en penumbra
    # Lincoln sentado, de mármol, asomando por la puerta
    caja(liso(), 0, 0.78, 1.0, 1.0, 0.45, 0.7)
    caja(liso(), 0, 0.72, 1.7, 0.66, 0.35, 0.75)
    esfera(liso(), 0, 0.7, 2.62, 0.17, 2)
    for s in (-1, 1):
        caja(liso(), s * 0.42, 0.6, 1.6, 0.16, 0.5, 0.18)
    # peristilo: doce columnas al frente y cuatro por lado
    columnata(liso(), -3.9, 3.9, 12, 0.25, 1.0, 0.17, 3.3)
    for s in (-1, 1):
        for k in range(1, 5):
            cil(liso(), s * 3.9, 0.25 + k * 0.95, 1.0, 0.17, 3.3, 12, r2=0.15)
    caja(liso(), 0, 2.3, 4.3, 8.5, 4.7, 0.45)                         # entablamento
    caja(mat('friso', 0xe6dfcf), 0, 2.3, 4.48, 8.55, 4.75, 0.1)
    caja(marmol, 0, 2.6, 4.75, 7.0, 3.6, 0.8)                         # ático
    caja(liso(), 0, 2.6, 5.55, 7.2, 3.8, 0.14)
    for i in range(9):                                                 # guirnaldas del ático
        esfera(mat('guirnalda', 0x7a9a6a, 0.8), -3.0 + i * 0.75, 0.75, 5.15, 0.11, 1, esc=(1.6, 0.6, 1))
    caja(cesped(), 0, -2.6, 0, 9.4, 1.6, 0.05)


# ---------------------------------------------------------------- edificio federal
def federal():
    W, D = 6.4, 4.0
    rustico = mat_bloques('rustico', 0xd8ccb0, 0xb2a587, ancho=0.9, alto=0.4, grosor=0.022)
    caliza = mat_bloques('caliza', 0xeae1cc, 0xd4c9af, ancho=0.9, alto=0.35, grosor=0.008)
    caja(rustico, 0, D / 2, 0, W, D, 1.4)
    caja(caliza, 0, D / 2 + 0.05, 1.4, W - 0.1, D - 0.1, 2.8)
    caja(liso(), 0, D / 2, 1.38, W + 0.1, D + 0.1, 0.1)
    caja(liso(), 0, D / 2, 4.2, W + 0.35, D + 0.35, 0.26)
    caja(caliza, 0, D / 2 + 0.1, 4.46, W - 0.3, D - 0.4, 0.5)
    caja(liso(), 0, D / 2 + 0.1, 4.96, W - 0.2, D - 0.3, 0.08)
    bahias = [-2.4, -1.2, 0, 1.2, 2.4]
    for x in bahias:
        if x == 0:
            puerta(0, 0.36, 0.8, 0.95, color=0x6b5530)
        else:
            ventana(x, 0.45, 0.6, 0.75, remate='cornisa')
        ventana(x + 0.05 * 0, 1.75, 0.55, 1.0, y=0.05, remate='fronton')
        ventana(x, 3.1, 0.5, 0.8, y=0.05)
    escalinata(liso(), 0, 0, 0, 1.6, 3, huella=0.22, tabica=0.12)
    columnata(liso(), -3.0, 3.0, 6, -0.12, 1.48, 0.12, 2.72)
    for s in (-1, 1):                                                  # faroles a la puerta
        cil(hierro(), s * 0.75, -0.25, 0.36, 0.04, 0.9, 6)
        esfera(mat('farolillo', 0xffe7a1, 0.3), s * 0.75, -0.25, 1.32, 0.12, 1)
    bandera(0, -0.3, 5.0, alto=1.3, ancho=0.8)


# ---------------------------------------------------------------- casas de Georgetown
def georgetown():
    casas = [
        (-2.0, 3.6, mat_bloques('ladrillo_rojo', 0xb5523b, 0xe7dccb, ancho=0.25, alto=0.085, grosor=0.012)),
        (0.0, 4.0, mat_bloques('pintura_amarilla', 0xf2cf6b, 0xe6c35e, ancho=0.25, alto=0.085, grosor=0.01, mezcla=0.35)),
        (2.0, 3.5, mat_bloques('pintura_azul', 0x86a3c9, 0x7b97bc, ancho=0.25, alto=0.085, grosor=0.01, mezcla=0.35)),
    ]
    persiana = mat('persiana', 0x24352b, 0.6)
    piedra = mat('piedra_gris', 0xb8b2a6, 0.8)
    for x, h, m in casas:
        caja(m, x, 1.6, 0, 2.0, 3.2, h)
        caja(piedra, x, 1.6, 0, 2.02, 3.22, 0.45)                       # el zócalo
        caja(marco(), x, 1.6, h, 2.12, 3.3, 0.16)                       # cornisa
        for k in range(9):                                              # dentículos
            caja(marco(), x - 0.9 + k * 0.225, -0.07, h - 0.1, 0.1, 0.1, 0.1)
        caja(pizarra(), x, 1.8, h + 0.16, 1.85, 2.8, 0.55)              # tejado
        caja(m, x, 0.62, h + 0.16, 0.72, 0.5, 0.62)                     # buhardilla
        fronton(pizarra(), x, 0.32, h + 0.78, 0.86, 0.32, 0.6)
        ventana(x, h + 0.28, 0.38, 0.34, y=0.37)
        puerta(x + 0.5, 0.6, 0.55, 1.15, color={-2.0: 0x1f4a2e, 0.0: 0xb42a2a, 2.0: 0x22314f}[x])
        caja(mat('fanal', 0xfff1c2, 0.3), x + 0.5, -0.04, 1.86, 0.5, 0.02, 0.16)
        escalinata(piedra, x + 0.5, 0, 0, 0.75, 4, huella=0.18, tabica=0.15)
        ventana(x - 0.45, 0.85, 0.5, 0.95, persiana=persiana)
        pisos = [1.95, 2.9] if h > 3.55 else [1.95]
        if h >= 3.9:
            pisos = [1.95, 3.0]
        for z in pisos:
            for k in (-0.45, 0.5):
                ventana(x + k, z, 0.48, 0.75, persiana=persiana)
        caja(mat('jardinera', 0x6b3f2a), x - 0.45, -0.12, 0.72, 0.6, 0.18, 0.14)
        for k in range(4):
            esfera(mat('flores', 0xff4f6d, 0.8), x - 0.68 + k * 0.15, -0.12, 0.9, 0.08, 1)
    caja(mat('piedra_gris', 0xb8b2a6, 0.8), 0, 1.6, 0, 6.05, 3.25, 0.02)


# ---------------------------------------------------------------- acera y fondo
def cerezo():
    tronco = mat('tronco', 0x5e3c2a, 0.9)
    caja(mat('tierra', 0x6b4e3a, 1.0), 0, 0, 0, 1.0, 1.0, 0.05)
    caja(mat('bordillo', 0xc9c3b6), 0, -0.48, 0, 1.04, 0.08, 0.1)
    caja(mat('bordillo', 0xc9c3b6), 0, 0.48, 0, 1.04, 0.08, 0.1)
    caja(mat('bordillo', 0xc9c3b6), -0.48, 0, 0, 0.08, 1.04, 0.1)
    caja(mat('bordillo', 0xc9c3b6), 0.48, 0, 0, 0.08, 1.04, 0.1)
    rama(tronco, (0, 0, 0), (0.08, 0, 1.3), 0.17, 0.12)
    for p in ((0.7, 0.3, 2.0), (-0.6, 0.4, 2.1), (0.1, -0.6, 2.05), (-0.2, 0.1, 2.4)):
        rama(tronco, (0.08, 0, 1.25), p, 0.1, 0.05, 6)
    rosas = [mat('flor1', 0xffb3cb, 0.8), mat('flor2', 0xff96b8, 0.8), mat('flor3', 0xffd3e1, 0.8)]
    for i, (x, y, z, r) in enumerate(((0, 0, 2.35, 0.8), (0.7, 0.3, 2.15, 0.6), (-0.65, 0.35, 2.2, 0.62),
                                      (0.15, -0.6, 2.15, 0.6), (-0.2, 0.55, 2.7, 0.55), (0.45, -0.1, 2.85, 0.5),
                                      (-0.5, -0.35, 2.6, 0.5), (0.0, 0.1, 3.1, 0.45))):
        esfera(rosas[i % 3], x, y, z, r, 2, esc=(1, 1, 0.82))
    cil(mat('petalos', 0xffc6d8, 0.9), 0, 0, 0.05, 0.42, 0.015, 16)


def farola():
    negro = mat('farola', 0x1d2a24, 0.35)
    cil(negro, 0, 0, 0, 0.17, 0.12, 12)
    cil(negro, 0, 0, 0.12, 0.13, 0.32, 8, r2=0.1)
    cil(negro, 0, 0, 0.44, 0.075, 2.0, 8, r2=0.06)
    cil(negro, 0, 0, 2.44, 0.13, 0.1, 12, r2=0.09)
    esfera(mat('globo', 0xfff4cf, 0.15), 0, 0, 2.78, 0.27, 2)
    cil(negro, 0, 0, 3.02, 0.08, 0.14, 8, r2=0.02)
    caja(mat('cartel_dc', 0x1f3c88), 0.0, -0.12, 1.75, 0.03, 0.22, 0.6)   # banderola


def monumento():
    piedra1 = mat('obelisco1', 0xf3eee3, 0.6)
    piedra2 = mat('obelisco2', 0xe7dfcd, 0.6)                          # el cambio de piedra a un tercio
    cil(mat('plaza', 0xd9d2c2, 0.9), 0, 0, 0, 3.0, 0.3, 32)
    cil(cesped(), 0, 0, 0, 5.5, 0.04, 32)
    cil(piedra1, 0, 0, 0.3, 0.95, 4.5, 4, r2=0.86)
    cil(piedra2, 0, 0, 4.8, 0.86, 9.0, 4, r2=0.68)
    cil(piedra2, 0, 0, 13.8, 0.68, 1.3, 4, r2=0.0)
    for i in range(12):
        a = i / 12 * math.tau
        x, y = math.cos(a) * 2.6, math.sin(a) * 2.6
        cil(mat('asta', 0xd8d8d8, 0.3), x, y, 0.3, 0.03, 2.0, 6)
        caja(mat_franjas('franjas_m', 0xd8283a, 0xffffff, 7, z0=1.95, alto=0.35), x + 0.33 * math.cos(a + 1.57),
             y + 0.33 * math.sin(a + 1.57), 1.95, 0.62, 0.02, 0.35, giro=a + 1.57)


PIEZAS = {
    'casa_blanca': (casa_blanca, 'dc', dict(lado=1024)),
    'capitolio':   (capitolio,   'dc', dict(lado=1024)),
    'lincoln':     (lincoln,     'dc', dict(lado=1024)),
    'federal':     (federal,     'dc', dict(lado=1024)),
    'georgetown':  (georgetown,  'dc', dict(lado=1024)),
    'cerezo':      (cerezo,      'dc', dict(lado=512, bisel=0.0)),
    'farola':      (farola,      'dc', dict(lado=256, bisel=0.01)),
    'monumento':   (monumento,   'dc', dict(lado=512, bisel=0.03)),
}

correr(PIEZAS)
