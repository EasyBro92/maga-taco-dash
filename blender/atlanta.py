# Nivel 24: Atlanta, Georgia (14/11/2026).
#
#   blender -b -P blender/atlanta.py -- [pieza ...] [--rapido]
#
# Historia: «Su foto de la ficha policial en cada pared. Misión: "encuéntrame
#   11.780 votos". Aquí pasa de 270: ¡presidente electo!».
#   Por Peachtree Street (el arco del melocotón, el Capitolio de la cúpula de
#   oro, la torre de la pirámide dorada, el cilindro de cristal del hotel y el
#   mural de la ficha policial) persiguiendo las papeletas que se escapan; en
#   el pabellón del recuento, el trile de las urnas; y se llega al teatro de
#   las cúpulas, con la marquesina que dice «PRESIDENT ELECT».
# Obstáculos (carpeta obstaculos): la urna, la urna grande del trile, la
# papeleta y la papeleta de oro, la pancarta del fraude, las cajas de
# melocotones, el camión de los melocotones, la máquina y la mesa del recuento.
# En la acera (carpeta atlanta): la columna de anuncios con la ficha.

import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import *

def blanco():    return mat('blanco_atl', 0xf4f2ec, 0.5)
def negro():     return mat('negro_atl', 0x1b1c20, 0.4)
def azul():      return mat('azul_atl', 0x1f4a9a, 0.45)
def rojo():      return mat('rojo_atl', 0xc8282c, 0.45)
def oro():       return mat('oro_atl', 0xe8b840, 0.25)
def piedra():    return mat('piedra_atl', 0xe4dccb, 0.7)
def melocoton(): return mat('melocoton_atl', 0xf4a46a, 0.55)
def rubor():     return mat('rubor_atl', 0xe0604a, 0.55)
def hoja():      return mat('hoja_atl', 0x4f8a3a, 0.7)
def madera():    return mat('madera_atl', 0xb08a5a, 0.7)
def gris():      return mat('gris_atl', 0x8a9098, 0.5)
def cristal():   return mat('cristal_atl', 0x2a3a4a, 0.25)
def verdeosc():  return mat('verdeosc_atl', 0x2a4a3a, 0.6)
def bombilla():  return luz('bombilla_atl', 0xffe08a, 1.8)
def ladrillo():  return mat_bloques('ladrillo_atl', 0x9a5a42, 0x7a4434, ancho=0.5, alto=0.22)
def tablas():    return mat_bloques('tablas_atl', 0xd8a868, 0xc89858, ancho=4.0, alto=0.25)

def melocoton_bola(x, y, z, r):
    """Un melocotón de Georgia: la bola, su rubor, el rabito y la hoja."""
    esfera(melocoton(), x, y, z, r, 2, esc=(1, 0.95, 0.95))
    esfera(rubor(), x + r * 0.22, y - r * 0.3, z + r * 0.08, r * 0.8, 2)
    cil(mat('rabo_atl', 0x5a3a1e, 0.8), x, y, z + r * 0.85, r * 0.07, r * 0.32, 6)
    esfera(hoja(), x + r * 0.32, y, z + r * 1.05, r * 0.36, 1, esc=(1.2, 0.5, 0.25))

def ficha(x, y, z, w):
    """La foto de la ficha policial, en relieve y mirando a -y: el fondo gris
    azulado, los hombros del traje, la camisa, la corbata roja, la cara con el
    ceño fruncido y el tupé rubio. (x, z): el centro de abajo; w: el ancho."""
    h = w * 1.2
    caja(mat('fondo_ficha', 0x4a5868, 0.8), x, y, z, w, 0.1, h)
    yf = y - 0.05
    esfera(mat('traje_ficha', 0x1a2440, 0.6), x, yf, z, w * 0.44, 2, esc=(1, 0.2, 0.6), mitad=True)
    caja(blanco(), x, yf - 0.06, z, w * 0.15, 0.04, h * 0.2)
    caja(rojo(), x, yf - 0.09, z, w * 0.055, 0.04, h * 0.18)
    caja(rojo(), x, yf - 0.1, z + h * 0.17, w * 0.08, 0.04, h * 0.035)
    piel = mat('piel_ficha', 0xe8a070, 0.6)
    zc = z + h * 0.5
    esfera(piel, x, yf, zc, w * 0.2, 2, esc=(0.9, 0.3, 1.15))
    pelo = mat('pelo_ficha', 0xf0c850, 0.6)
    esfera(pelo, x + w * 0.02, yf + 0.01, z + h * 0.68, w * 0.21, 2, esc=(1.02, 0.3, 0.4))
    esfera(pelo, x + w * 0.11, yf, z + h * 0.66, w * 0.12, 1, esc=(1.2, 0.36, 0.55))
    yb = yf - w * 0.058
    ceja = mat('ceja_ficha', 0xc89a40, 0.6)
    for s in (-1, 1):                                   # el ceño: las cejas bajan hacia dentro
        rama(ceja, (x + s * w * 0.11, yb, zc + h * 0.075), (x + s * w * 0.03, yb, zc + h * 0.045), w * 0.013, w * 0.013, 6)
        esfera(negro(), x + s * w * 0.065, yb, zc + h * 0.02, w * 0.017, 1)
    boca = mat('boca_ficha', 0x8a3a30, 0.6)
    zb = zc - h * 0.085
    rama(boca, (x - w * 0.07, yb, zb - h * 0.016), (x - w * 0.025, yb, zb), w * 0.011, w * 0.011, 6)
    rama(boca, (x - w * 0.025, yb, zb), (x + w * 0.025, yb, zb), w * 0.011, w * 0.011, 6)
    rama(boca, (x + w * 0.025, yb, zb), (x + w * 0.07, yb, zb - h * 0.016), w * 0.011, w * 0.011, 6)
    esfera(piel, x, yb + w * 0.01, zc - h * 0.02, w * 0.03, 1, esc=(0.8, 1, 1.3))

def arco_herradura(x, y, z, w, h, marco, vidrio):
    """Una ventana con arco de herradura en una fachada que mira a -y."""
    r = w / 2
    caja(marco, x, y - 0.04, z - 0.15, w + 0.5, 0.08, h - r + 0.15)
    cil(marco, x, y - 0.04, z + h - r, r + 0.25, 0.08, 18, eje='Y')
    caja(vidrio, x, y - 0.07, z, w, 0.1, h - r)
    cil(vidrio, x, y - 0.07, z + h - r, r, 0.1, 18, eje='Y')

# ================================================================ edificios
def fox_theatre():
    """El teatro de las cúpulas (la meta): la fachada de ladrillo a rayas con
    arcos de herradura, almenas, los dos minaretes con su cúpula de cebolla,
    la marquesina de bombillas que dice «PRESIDENT ELECT · 270» y, a los lados
    de la puerta, la foto de la ficha."""
    Y = 16
    W, D, H = 46.0, 24.0, 18.0
    yf = Y - D / 2
    rayas = mat_franjas('rayas_fox', 0xdcb48a, 0xb8784e, 18, eje='Z', z0=-H / 2, alto=H)
    caja(rayas, 0, Y, 0, W, D, H)
    caja(piedra(), 0, yf - 0.2, H, W + 0.6, 0.8, 0.8)
    for k in range(23):
        caja(piedra(), -W / 2 + 1 + k * 2, yf - 0.1, H + 0.8, 0.9, 0.5, 0.9)
    vid = cristal()
    for k in range(7):                                   # los arcos de arriba
        x = -15 + k * 5
        arco_herradura(x, yf, 10.2, 1.8, 4.2, piedra(), vid)
    # Los minaretes con su cúpula de cebolla.
    cobre = mat('cupula_fox', 0xc8925a, 0.35)
    for s in (-1, 1):
        x = s * (W / 2 - 3)
        caja(rayas, x, yf + 1.5, 0, 6, 6, 25)
        caja(piedra(), x, yf + 1.5, 25, 6.8, 6.8, 0.7)
        for k in range(3):
            arco_herradura(x, yf - 1.5, 12 + k * 4.4, 1.4, 3.0, piedra(), vid)
        cil(piedra(), x, yf + 1.5, 25.7, 2.3, 2.6, 16)
        esfera(cobre, x, yf + 1.5, 30.0, 2.7, 2, esc=(1, 1, 1.15))
        cil(oro(), x, yf + 1.5, 32.6, 0.6, 3.6, 10, r2=0.03)
    # La marquesina de bombillas.
    caja(mat('marquesina_fox', 0x8a1e24, 0.5), 0, yf - 3.2, 5.2, 24, 6.4, 3.4)
    caja(oro(), 0, yf - 3.2, 8.6, 24.4, 6.8, 0.3)
    for k in range(40):
        for z in (5.35, 8.45):
            esfera(bombilla(), -11.7 + k * 0.6, yf - 6.47, z, 0.12, 1)
    caja(luz('tablero_fox', 0xfff2d0, 0.9), 0, yf - 6.42, 5.75, 21.6, 0.06, 2.4)
    texto(negro(), 'PRESIDENT ELECT', 0, yf - 6.47, 7.45, tam=0.95, prof=0.05)
    texto(rojo(), '- 270 -', 0, yf - 6.47, 6.3, tam=0.95, prof=0.05)
    texto(oro(), 'ATLANTA', 0, yf - 0.62, 16.0, tam=1.6, prof=0.08)
    caja(mat('fondo_letrero_fox', 0x5a1418, 0.5), 0, yf - 0.45, 15.1, 16, 0.2, 1.9)
    # La puerta y la foto de la ficha a los dos lados.
    caja(vid, 0, yf - 0.05, 0, 16, 0.1, 4.6)
    for k in range(5):
        caja(oro(), -6.4 + k * 3.2, yf - 0.12, 0, 0.18, 0.06, 4.6)
    for s in (-1, 1):
        caja(oro(), s * 14, yf - 0.06, 1.0, 2.1, 0.1, 2.5)
        ficha(s * 14, yf - 0.12, 1.1, 1.8)

def capitolio_georgia():
    """El Capitolio de Georgia: el cuerpo de piedra clara, el pórtico de
    columnas con su frontón, el tambor y la cúpula de oro con la estatua."""
    Y = 16
    W, D, H = 44.0, 26.0, 14.0
    yf = Y - D / 2
    p = piedra()
    caja(p, 0, Y, 0, W, D, H)
    caja(p, 0, yf - 0.3, H, W + 0.8, 0.8, 0.9)
    vid = cristal()
    for z in (2.5, 8.0):
        for k in range(12):
            x = -W / 2 + 2.5 + k * (W - 5) / 11
            if abs(x) < 8.5:
                continue
            ventana(x, z, 1.6, 3.0, y=yf, marco=blanco(), cristal=vid, remate='cornisa')
    # El pórtico: la plataforma, la escalinata, las columnas y el frontón.
    caja(p, 0, yf - 3.2, 0, 17, 6.4, 3.0)
    escalinata(p, 0, yf - 6.4, 0, 12, 10, huella=0.4, tabica=0.3)
    columnata(p, -6.6, 6.6, 6, yf - 5.6, 3.0, 0.55, 9.5)
    caja(p, 0, yf - 3.3, 12.5, 17, 6.6, 1.4)
    fronton(p, 0, yf - 6.6, 13.9, 17.4, 3.4, 6.6)
    texto(mat('letras_cap', 0x8a7a60, 0.6), 'GEORGIA', 0, yf - 6.66, 13.15, tam=0.8, prof=0.05)
    # El tambor con sus columnitas y la cúpula de oro.
    cil(p, 0, Y, H + 0.9, 7.5, 2.5, 32)
    cil(p, 0, Y, H + 3.4, 6.2, 6.5, 32)
    for k in range(16):
        a = k * math.tau / 16
        cil(blanco(), math.cos(a) * 6.45, Y + math.sin(a) * 6.45, H + 3.4, 0.28, 6.0, 8)
    cil(p, 0, Y, H + 9.9, 6.8, 0.9, 32)
    cupula(oro(), 0, Y, H + 10.8, 6.0, 6.8, 32, 8)
    cil(p, 0, Y, H + 17.4, 1.4, 2.6, 12)
    cupula(oro(), 0, Y, H + 20.0, 1.45, 1.4, 12, 4)
    # La estatua de la Libertad (Miss Freedom) con su antorcha.
    est = mat('estatua_cap', 0xd8d0c0, 0.5)
    cil(est, 0, Y, H + 21.3, 0.42, 1.8, 10, r2=0.25)
    esfera(est, 0, Y, H + 23.35, 0.3, 1)
    rama(est, (0.2, Y, H + 22.7), (0.55, Y, H + 24.0), 0.09, 0.08, 6)
    esfera(luz('antorcha_cap', 0xffb040, 1.4), 0.6, Y, H + 24.2, 0.18, 1)
    for s in (-1, 1):                                      # las banderas
        cil(gris(), s * 12, yf - 4, 0, 0.1, 13, 8)
        caja(mat('bandera_ga', 0x2a3a8a, 0.6), s * 12 + 1.0, yf - 4, 11.2, 2.0, 0.05, 1.3)

def torre_piramide():
    """La torre de la pirámide dorada: el rascacielos de granito rojizo con
    sus retranqueos y, arriba, la pirámide de celosía de oro con la aguja."""
    Y = 14
    g = mat_ventanas('granito_torre', 0x3a4a5a, 0x8a5a4a, paso_x=1.4, paso_z=3.6, hueco_x=0.9, hueco_z=2.4)
    caja(g, 0, Y, 0, 24, 24, 54)
    caja(g, 0, Y, 54, 20, 20, 6)
    caja(g, 0, Y, 60, 16, 16, 4)
    caja(mat('portal_torre', 0x2a2420, 0.4), 0, Y - 12.05, 0, 10, 0.1, 6)
    o = oro()
    z0, zt = 64, 80
    ap = (0, Y, zt)
    c = [(-8, -8), (8, -8), (8, 8), (-8, 8)]
    for (x, y) in c:
        rama(o, (x, Y + y, z0), ap, 0.35, 0.2, 6)
    for k in range(1, 6):
        f = k / 6
        for i in range(4):
            a, b = c[i], c[(i + 1) % 4]
            rama(o, (a[0] * (1 - f), Y + a[1] * (1 - f), z0 + (zt - z0) * f),
                 (b[0] * (1 - f), Y + b[1] * (1 - f), z0 + (zt - z0) * f), 0.16, 0.16, 5)
    for i in range(4):
        a, b = c[i], c[(i + 1) % 4]
        for t in (0.25, 0.5, 0.75):
            rama(o, (a[0] + (b[0] - a[0]) * t, Y + a[1] + (b[1] - a[1]) * t, z0), ap, 0.14, 0.08, 5)
    cil(o, 0, Y, zt, 0.4, 12, 8, r2=0.05)

def westin_cilindro():
    """El hotel del cilindro de cristal: la torre redonda de cristal bronce
    con sus aros, el restaurante giratorio arriba (las ventanas encendidas) y
    el zócalo con la marquesina de la entrada."""
    Y = 13
    cr = mat_ventanas('bronce_cil', 0x5a4a3a, 0x3a3028, paso_x=1.6, paso_z=3.6, hueco_x=1.4, hueco_z=3.0, variacion=1.15)
    cil(cr, 0, Y, 0, 11, 72, 40)
    aro = mat('aro_cil', 0x2a2420, 0.4)
    for k in range(1, 20):
        cil(aro, 0, Y, k * 3.6, 11.08, 0.2, 40)
    cil(mat('banda_cil', 0x2a2a2e, 0.4), 0, Y, 72, 11.6, 5, 40)
    cil(luz('restaurante_atl', 0xffd890, 0.8), 0, Y, 73.2, 11.68, 2.2, 40)
    cil(mat('banda_cil', 0x2a2a2e, 0.4), 0, Y, 77, 10.4, 1.0, 40)
    cil(gris(), 0, Y, 78, 3, 3, 12)
    caja(piedra(), 0, Y - 2, 0, 26, 22, 8)
    caja(cristal(), 0, -0.06, 0.2, 18, 0.1, 3.4)
    caja(negro(), 0, -1.6, 3.6, 10, 3.2, 0.4)
    texto(oro(), 'PEACHTREE PLAZA', 0, -3.22, 3.8, tam=0.5, prof=0.04)

def mural_ficha():
    """El mural de la ficha policial: un edificio viejo de ladrillo con la foto
    pintada en toda la fachada y «FIND 11,780 VOTES» debajo."""
    Y = 8
    caja(ladrillo(), 0, Y, 0, 20, 14, 16)
    caja(piedra(), 0, Y - 7.2, 16, 20.6, 0.6, 0.6)
    vid = cristal()
    for s in (-1, 1):
        caja(vid, s * 5.5, Y - 7.05, 0.4, 7, 0.1, 2.6)
        caja(mat('toldo_mural', 0x1f4a3a, 0.6), s * 5.5, Y - 7.6, 3.1, 7.4, 1.2, 0.25)
    caja(negro(), 0, Y - 7.05, 0, 2.2, 0.1, 3.0)
    caja(blanco(), 0, Y - 7.1, 3.62, 13, 0.08, 0.75)
    texto(rojo(), 'FIND 11,780 VOTES', 0, Y - 7.16, 3.99, tam=0.55, prof=0.04)
    ficha(0, Y - 7.06, 4.6, 9.0)

def ficha_poster():
    """La columna de anuncios de la acera, con la foto de la ficha pegada."""
    v = verdeosc()
    caja(v, 0, 0, 0, 1.15, 1.15, 0.3)
    caja(v, 0, 0, 0.3, 1.0, 1.0, 2.6)
    caja(v, 0, 0, 2.9, 1.25, 1.25, 0.22)
    cupula(v, 0, 0, 3.12, 0.55, 0.5, 16, 4)
    esfera(oro(), 0, 0, 3.7, 0.12, 1)
    caja(blanco(), 0, -0.5, 0.75, 0.94, 0.04, 1.2)
    ficha(0, -0.54, 0.82, 0.8)
    texto(rojo(), 'WANTED: VOTES', 0, -0.53, 1.9, tam=0.1, prof=0.02)

# ================================================================ cruzan la calle
def arco_melocoton():
    """El arco de Peachtree Street: dos postes blancos, el letrero y el
    melocotón gigante encima."""
    for s in (-1, 1):
        caja(blanco(), s * 9, 0, 0, 0.6, 0.6, 9.4)
        melocoton_bola(s * 9, 0, 10.0, 0.55)
    caja(blanco(), 0, 0, 6.2, 18.6, 0.5, 0.4)
    caja(blanco(), 0, 0, 8.6, 18.6, 0.5, 0.4)
    caja(mat('verde_arco', 0x2a6a3a, 0.7), 0, 0, 6.6, 17, 0.3, 2.0)
    texto(melocoton(), 'PEACHTREE ST', 0, -0.2, 7.55, tam=1.25, prof=0.07)
    o = texto(melocoton(), 'PEACHTREE ST', 0, 0.2, 7.55, tam=1.25, prof=0.07); o.rotation_euler = (math.pi / 2, 0, math.pi)
    melocoton_bola(0, 0, 10.7, 1.6)

def recuento():
    """El pabellón del recuento (momento estrella): la pista de madera de un
    pabellón de deportes; a los lados, las mesas largas con las máquinas, los
    montones de papeletas y los que cuentan; detrás, las gradas casi vacías;
    arriba, el techo oscuro con focos y los marcadores colgados que dicen
    11,780. Cruza la calle: el origen en el centro y la calle a lo largo de y."""
    L = 420
    caja(tablas(), 0, 0, -0.2, 20, L, 0.2)
    caja(mat('suelo_recuento', 0x8a6a48, 0.7), 0, 0, -0.22, 56, L, 0.2)
    for s in (-1, 1):
        caja(blanco(), s * 7.0, 0, 0, 0.14, L, 0.012)
    az = azul()
    for s in (-1, 1):                                    # la barrera azul con «RECOUNT»
        caja(az, s * 8.3, 0, 0, 0.3, L, 1.0)
        for k in range(int(L / 35)):
            y = -L / 2 + 17 + k * 35
            o = texto(blanco(), 'RECOUNT', 0, 0, 0.5, tam=0.5, prof=0.03)
            o.rotation_euler = (math.pi / 2, 0, -s * math.pi / 2)
            o.location = (s * (8.3 - 0.17), y, 0.5)
    # Las mesas del recuento, con papeletas, máquinas y los que cuentan.
    camisas = [0xc8282c, 0x2a5aa8, 0xf4f0e8, 0x3f8a4a, 0xe8b830]
    for s in (-1, 1):
        for k in range(int(L / 9)):
            y = -L / 2 + 5 + k * 9
            caja(blanco(), s * 11, y, 0, 1.4, 5.0, 0.76)
            for j in range(3):
                caja(blanco(), s * 11 + 0.3 * ((j % 2) * 2 - 1) * 0.6, y - 1.6 + j * 1.6, 0.76, 0.34, 0.44, 0.12 + 0.12 * ((k + j) % 3))
            if k % 2 == 0:
                caja(gris(), s * 11, y + 1.9, 0.76, 0.8, 0.7, 0.6)
                caja(luz('pantalla_rec', 0x4ad86a, 0.9), s * (11 - 0.41), y + 1.9, 1.05, 0.02, 0.5, 0.25)
            for j in (-1, 1):
                c = mat(f'camisa_rec{(k + j) % 5}', camisas[(k + j) % 5], 0.8)
                cil(c, s * 12.4, y + j * 1.2, 0, 0.32, 1.25, 6)
                esfera(mat('cara_rec', 0xe8b89a, 0.7), s * 12.4, y + j * 1.2, 1.5, 0.24, 1)
    # Las gradas (casi vacías: algunos que miran) y las paredes.
    for s in (-1, 1):
        for g in range(4):
            caja(mat('grada_rec', 0x2a4a8a, 0.8), s * (16 + g * 2.6), 0, 0, 2.6, L, 1.2 + g * 1.6)
            for k in range(int(L / 15)):
                if (k + g) % 3:
                    continue
                y = -L / 2 + 6 + k * 15 + g * 3
                c = mat(f'camisa_rec{(k + g) % 5}', camisas[(k + g) % 5], 0.8)
                cil(c, s * (16 + g * 2.6), y, 1.2 + g * 1.6, 0.4, 0.9, 6)
                esfera(mat('cara_rec', 0xe8b89a, 0.7), s * (16 + g * 2.6), y, 2.35 + g * 1.6, 0.3, 1)
        caja(mat('muro_rec', 0x2a2e36, 0.7), s * 27.5, 0, 0, 1.0, L, 22)
    caja(mat('techo_rec', 0x1a1c22, 0.8), 0, 0, 22, 56, L, 0.6)
    foco = luz('foco_rec', 0xfff4d8, 1.4)
    for k in range(int(L / 15)):
        for x in (-12, 0, 12):
            caja(foco, x, -L / 2 + 7 + k * 15, 21.7, 1.6, 1.6, 0.3)
    # Las banderolas que cuelgan y los marcadores que dicen 11,780.
    for k in range(int(L / 30)):
        y = -L / 2 + 15 + k * 30
        for s in (-1, 1):
            caja(rojo() if (k + (s > 0)) % 2 else az, s * 10.5, y, 12.5, 2.6, 0.08, 7)
            o = texto(blanco(), 'VOTE', s * 10.5, y - 0.06, 15.5, tam=0.7, prof=0.03)
    dig = luz('digitos_rec', 0xff5030, 1.5)
    for j in range(4):
        y = -L / 2 + 52 + j * 105
        for x in (-3, 3):
            cil(gris(), x, y, 17.5, 0.05, 4.5, 4)
        caja(negro(), 0, y, 12.5, 9.5, 5, 5)
        texto(dig, '11,780', 0, y - 2.52, 15.6, tam=1.7, prof=0.05)
        texto(oro(), 'VOTES', 0, y - 2.52, 13.6, tam=0.9, prof=0.05)
    # La entrada y la salida: la pared con el hueco de la calle y su letrero.
    m = mat('muro_rec', 0x2a2e36, 0.7)
    for (y, txt) in ((-L / 2 + 0.5, 'RECOUNT CENTER'), (L / 2 - 0.5, '11,780 VOTES')):
        for s in (-1, 1):
            caja(m, s * 18.5, y, 0, 19, 1.0, 22.3)
        caja(m, 0, y, 9, 18.2, 1.0, 13.3)
        caja(az, 0, y - 0.6, 9.8, 16, 0.2, 2.6)
        texto(blanco(), txt, 0, y - 0.72, 11.1, tam=1.2, prof=0.06)

# ================================================================ obstáculos
def urna_voto():
    """La urna de votar (saltar): la caja azul con la tapa blanca, la ranura
    con papeletas asomando y «VOTE» delante."""
    caja(azul(), 0, 0, 0, 1.3, 0.9, 0.74)
    caja(blanco(), 0, 0, 0.74, 1.36, 0.96, 0.1)
    caja(negro(), 0, 0, 0.84, 0.7, 0.12, 0.02)
    for k, dx in enumerate((-0.18, 0.04, 0.24)):
        caja(blanco(), dx, 0, 0.82, 0.34, 0.02, 0.2, giro=0.12 * (k - 1))
    texto(blanco(), 'VOTE', 0, -0.45, 0.38, tam=0.32, prof=0.03)
    for dx in (-0.5, 0.5):
        esfera(blanco(), dx, -0.46, 0.4, 0.06, 1)

def urna_trile():
    """La urna grande del trile: azul con los cantos dorados, una
    interrogación de oro delante y la ranura arriba. (Se levanta como un
    cubilete: por debajo está hueca.)"""
    W, D, H = 2.0, 1.5, 2.5
    caja(azul(), 0, 0, 0, W, D, H)
    o = oro()
    for s in (-1, 1):
        for t in (-1, 1):
            caja(o, s * W / 2, t * D / 2, 0, 0.12, 0.12, H)
    for t in (-1, 1):
        caja(o, 0, t * D / 2, H - 0.12, W + 0.12, 0.12, 0.12)
        caja(o, 0, t * D / 2, 0, W + 0.12, 0.12, 0.12)
    caja(blanco(), 0, 0, H, W + 0.1, D + 0.1, 0.12)
    caja(negro(), 0, 0, H + 0.12, 1.0, 0.14, 0.02)
    texto(o, '?', 0, -D / 2, 1.45, tam=1.4, prof=0.06)
    texto(blanco(), 'VOTE', 0, -D / 2, 0.42, tam=0.36, prof=0.04)

def papeleta():
    """La papeleta que se escapa (se coge): el papel blanco con la cabecera
    azul, las casillas y la cruz roja; de pie, mirando al jugador."""
    caja(blanco(), 0, 0, 0, 0.9, 0.04, 1.2)
    caja(azul(), 0, -0.025, 0.98, 0.9, 0.01, 0.22)
    texto(blanco(), 'BALLOT', 0, -0.032, 1.09, tam=0.14, prof=0.01)
    for k in range(3):
        z = 0.7 - k * 0.27
        caja(negro(), -0.28, -0.025, z, 0.16, 0.01, 0.16)
        caja(blanco(), -0.28, -0.034, z + 0.025, 0.11, 0.006, 0.11)
        caja(gris(), 0.12, -0.025, z + 0.06, 0.48, 0.01, 0.04)
    rama(rojo(), (-0.36, -0.045, 0.69), (-0.2, -0.045, 0.87), 0.025, 0.025, 6)
    rama(rojo(), (-0.36, -0.045, 0.87), (-0.2, -0.045, 0.69), 0.025, 0.025, 6)

def papeleta_oro():
    """La papeleta de oro que se esconde en una urna del trile (brilla)."""
    caja(luz('oro_brillo_atl', 0xffc840, 1.2), 0, 0, 0, 0.9, 0.05, 1.2)
    caja(blanco(), 0, -0.03, 0.15, 0.7, 0.01, 0.9)
    rama(rojo(), (-0.2, -0.05, 0.62), (-0.04, -0.05, 0.42), 0.04, 0.04, 6)
    rama(rojo(), (-0.04, -0.05, 0.42), (0.26, -0.05, 0.86), 0.04, 0.04, 6)

def cartel_fraude():
    """La pancarta de la Liga: «FRAUD!» (agacharse)."""
    for x in (-1.25, 1.25):
        cil(madera(), x, 0, 0, 0.07, 2.75, 8)
    caja(rojo(), 0, 0, 1.55, 2.4, 0.06, 1.05)
    caja(blanco(), 0, -0.035, 1.62, 2.2, 0.01, 0.06)
    texto(blanco(), 'FRAUD!', 0, -0.04, 2.08, tam=0.55, prof=0.03)

def cajas_melocoton():
    """Las cajas de melocotones de Georgia (saltar)."""
    t = mat_bloques('tablas_caja_atl', 0xc89a62, 0xa87a48, ancho=0.8, alto=0.12)
    for (x, z, g) in ((-0.42, 0, 0.05), (0.42, 0, -0.04), (0.0, 0.36, 0.1)):
        caja(t, x, 0, z, 0.8, 0.6, 0.36, giro=g)
        for i in range(3):
            for j in range(2):
                esfera(melocoton(), x - 0.24 + i * 0.24, -0.13 + j * 0.26, z + 0.38, 0.12, 2)
    texto(rojo(), 'GA PEACHES', -0.42, -0.31, 0.18, tam=0.09, prof=0.01)

def camion_melocotones():
    """El camión de los melocotones (no se pasa): la cabina blanca y la caja
    color melocotón con un melocotón gigante en el techo."""
    caja(melocoton(), 0, 0.9, 0.55, 2.3, 4.2, 2.3)
    caja(blanco(), 0, -1.95, 0.45, 2.2, 1.5, 1.7)
    caja(cristal(), 0, -2.71, 1.25, 1.9, 0.04, 0.75)
    caja(negro(), 0, -2.72, 0.35, 2.0, 0.08, 0.5)
    for s in (-1, 1):
        esfera(mat('faro_atl', 0xfff4c8, 0.2), s * 0.8, -2.74, 0.95, 0.13, 1)
        for y in (-1.9, 1.9):
            cil(negro(), s * 1.05, y, 0.45, 0.45, 0.3, 14, eje='X')
    texto(rubor(), 'GEORGIA PEACHES', 0, -1.22, 2.48, tam=0.26, prof=0.02)
    melocoton_bola(0, 0.9, 3.75, 0.95)

def maquina_recuento():
    """La máquina del recuento (no se pasa): el armario gris con la ranura,
    la bandeja llena de papeletas, la urna encima y la pantalla verde."""
    caja(gris(), 0, 0, 0, 1.7, 1.0, 1.35)
    caja(negro(), 0, -0.5, 0.95, 1.3, 0.04, 0.08)
    caja(blanco(), 0, -0.62, 0.55, 1.4, 0.3, 0.08)
    caja(blanco(), 0, -0.62, 0.63, 1.2, 0.24, 0.2)
    cil(negro(), 0.5, 0.2, 1.35, 0.06, 0.4, 8)
    caja(negro(), 0.5, 0.2, 1.75, 0.8, 0.12, 0.55)
    caja(luz('pantalla_atl', 0x4ad86a, 1.0), 0.5, 0.13, 1.8, 0.7, 0.02, 0.45)
    texto(negro(), 'COUNT', 0.5, 0.115, 2.02, tam=0.14, prof=0.01)
    caja(azul(), -0.4, 0.1, 1.35, 0.7, 0.6, 0.5)
    caja(blanco(), -0.4, 0.1, 1.85, 0.74, 0.64, 0.06)

def mesa_recuento():
    """La mesa del recuento (saltar): el tablero con montones de papeletas y
    el faldón azul de «RECOUNT»."""
    caja(madera(), 0, 0, 0.72, 2.0, 0.9, 0.06)
    for x in (-0.9, 0.9):
        for y in (-0.38, 0.38):
            cil(gris(), x, y, 0, 0.04, 0.72, 6)
    caja(azul(), 0, -0.44, 0.4, 2.0, 0.02, 0.34)
    texto(blanco(), 'RECOUNT', 0, -0.455, 0.57, tam=0.18, prof=0.01)
    for k in range(4):
        caja(blanco(), -0.7 + k * 0.46, 0, 0.78, 0.3, 0.4, 0.06 + 0.05 * (k % 3))

PIEZAS = {
    'fox_theatre':        (fox_theatre,        'atlanta',    dict(lado=2048, bisel=0.0)),
    'capitolio_georgia':  (capitolio_georgia,  'atlanta',    dict(lado=2048, bisel=0.0)),
    'torre_piramide':     (torre_piramide,     'atlanta',    dict(lado=2048, bisel=0.0)),
    'westin_cilindro':    (westin_cilindro,    'atlanta',    dict(lado=2048, bisel=0.0)),
    'mural_ficha':        (mural_ficha,        'atlanta',    dict(lado=1024, bisel=0.0)),
    'ficha_poster':       (ficha_poster,       'atlanta',    dict(lado=512, bisel=0.0)),
    'arco_melocoton':     (arco_melocoton,     'atlanta',    dict(lado=1024, bisel=0.0, suelo=False)),
    'recuento':           (recuento,           'atlanta',    dict(lado=2048, bisel=0.0, suelo=False)),
    'urna_voto':          (urna_voto,          'obstaculos', dict(lado=256, bisel=0.0)),
    'urna_trile':         (urna_trile,         'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
    'papeleta':           (papeleta,           'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
    'papeleta_oro':       (papeleta_oro,       'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
    'cartel_fraude':      (cartel_fraude,      'obstaculos', dict(lado=256, bisel=0.0, suelo=False)),
    'cajas_melocoton':    (cajas_melocoton,    'obstaculos', dict(lado=256, bisel=0.0)),
    'camion_melocotones': (camion_melocotones, 'obstaculos', dict(lado=512, bisel=0.0)),
    'maquina_recuento':   (maquina_recuento,   'obstaculos', dict(lado=256, bisel=0.0)),
    'mesa_recuento':      (mesa_recuento,      'obstaculos', dict(lado=256, bisel=0.0)),
}

correr(PIEZAS)
