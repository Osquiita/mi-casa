# -*- coding: utf-8 -*-
"""PASO 02 - PLANTA BAJA (VIVIENDA A) - v6.1.
- Entrada Vivienda A -> fachada izquierda (X 0,30-1,30, puerta 1,00 m).
- Portal Vivienda B -> esquina derecha (X 10,40-11,40): escalera RECTA DIRECTA a planta alta.
- COCINA -> frente derecho (X 6,40-10,40), lindando con la escalera de P.A.
- La antigua cocina se incorpora al SALÓN (X 1,40-6,40 x Y 0-7,40 = 37 m²).
- Única separación cocina-salón: PUERTA CORREDERA DOBLE GRANDE (abierta = todo unido).
- Porche cubierto (X 6,40-11,40 x Y 5,00-7,60); cocina y salón abren al porche."""
import os
import math
import ezdxf
from ezdxf.enums import TextEntityAlignment
from ezdxf.addons.drawing import RenderContext, Frontend
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
import matplotlib.pyplot as plt

from plan_data import X0, Y0, X1, Y1, PX0, PY0, PX1, PY1

BASE = os.path.dirname(os.path.abspath(__file__))
DXF = os.path.join(BASE, "paso-02-planta-baja.dxf")
PNG = os.path.join(BASE, "preview-02-planta-baja.png")

doc = ezdxf.new("R2010", setup=True)
doc.units = ezdxf.units.M
msp = doc.modelspace()

def layer(name, color, lw100, lt="CONTINUOUS"):
    doc.layers.add(name, color=color, linetype=lt)
    doc.layers.get(name).dxf.lineweight = lw100

layer("MUROS", 7, 60)
layer("TABIQUES", 7, 25)
layer("PUERTAS", 5, 18)
layer("VENTANAS", 5, 18)
layer("ESCALERA", 5, 18)
layer("MOBILIARIO", 8, 13)
layer("PATIO", 3, 30)
layer("PORCHE", 4, 25)
layer("TEXTO", 7, 18)
layer("COTAS", 5, 18)
layer("CAJETIN", 7, 35)

def txt(x, y, s, h=0.30, lay="TEXTO", rot=0.0, align=TextEntityAlignment.LEFT):
    t = msp.add_text(s, dxfattribs={"layer": lay, "height": h, "rotation": rot})
    t.set_placement((x, y), align=align)
    return t

# ------------------------------------------------------------ paredes
def wall_rect(x1, y1, x2, y2, t, lay):
    if abs(y2 - y1) > abs(x2 - x1):  # vertical
        r = [(x1 - t/2, min(y1, y2)), (x1 + t/2, min(y1, y2)),
             (x1 + t/2, max(y1, y2)), (x1 - t/2, max(y1, y2))]
    else:  # horizontal
        r = [(min(x1, x2), y1 - t/2), (max(x1, x2), y1 - t/2),
             (max(x1, x2), y1 + t/2), (min(x1, x2), y1 + t/2)]
    msp.add_lwpolyline(r, close=True, dxfattribs={"layer": lay})
    h = msp.add_hatch(dxfattribs={"layer": lay})
    h.set_solid_fill()
    h.paths.add_polyline_path(r, is_closed=True)

def clip(a, b, gaps):
    pts = sorted(set([a, b] + [p for g in gaps for p in g if a < p < b]))
    segs = []
    for i in range(len(pts) - 1):
        p, q = pts[i], pts[i + 1]
        if any(g0 <= p and q <= g1 for g0, g1 in gaps):
            continue
        if q - p > 1e-6:
            segs.append((p, q))
    return segs

def wall_h(y, x0, x1, gaps, t=0.30, lay="MUROS"):
    for a, b in clip(x0, x1, gaps):
        wall_rect(a, y, b, y, t, lay)

def wall_v(x, y0, y1, gaps, t=0.30, lay="MUROS"):
    for a, b in clip(y0, y1, gaps):
        wall_rect(x, a, x, b, t, lay)

# ------------------------------------------------------------ puertas/ventanas
def door_v(x, y0, y1, side=1):
    w = y1 - y0
    msp.add_line((x, y0), (x + side * 0.7 * w, y0 + 0.7 * w), dxfattribs={"layer": "PUERTAS"})
    if side > 0:
        msp.add_arc((x, y0), w, 0, 90, dxfattribs={"layer": "PUERTAS"})
    else:
        msp.add_arc((x, y0), w, 90, 180, dxfattribs={"layer": "PUERTAS"})

def door_h(y, x0, x1, side=1):
    w = x1 - x0
    msp.add_line((x0, y), (x0 + 0.7 * w, y + side * 0.7 * w), dxfattribs={"layer": "PUERTAS"})
    if side > 0:
        msp.add_arc((x0, y), w, -90, 0, dxfattribs={"layer": "PUERTAS"})
    else:
        msp.add_arc((x0, y), w, 180, 270, dxfattribs={"layer": "PUERTAS"})

def sliding_v(x, y0, y1):
    h = y1 - y0
    msp.add_lwpolyline([(x - 0.20, y0), (x - 0.20, y0 + 0.55 * h), (x - 0.08, y0 + 0.55 * h),
                        (x - 0.08, y0), (x - 0.20, y0)], dxfattribs={"layer": "PUERTAS"})
    msp.add_lwpolyline([(x - 0.20, y0 + 0.45 * h), (x - 0.20, y1), (x - 0.08, y1),
                        (x - 0.08, y0 + 0.45 * h), (x - 0.20, y0 + 0.45 * h)], dxfattribs={"layer": "PUERTAS"})
    msp.add_line((x - 0.30, y0 + 0.5 * h), (x - 0.36, y0 + 0.5 * h), dxfattribs={"layer": "PUERTAS"})
    msp.add_line((x + 0.02, y0 + 0.5 * h), (x + 0.08, y0 + 0.5 * h), dxfattribs={"layer": "PUERTAS"})

def window_h(y, a, b, t=0.30):
    for dy in (-t * 0.30, t * 0.30):
        msp.add_line((a, y + dy), (b, y + dy), dxfattribs={"layer": "VENTANAS"})
    msp.add_line((a, y - t * 0.30), (a, y + t * 0.30), dxfattribs={"layer": "VENTANAS"})
    msp.add_line((b, y - t * 0.30), (b, y + t * 0.30), dxfattribs={"layer": "VENTANAS"})

def window_v(x, a, b, t=0.30):
    for dx in (-t * 0.30, t * 0.30):
        msp.add_line((x + dx, a), (x + dx, b), dxfattribs={"layer": "VENTANAS"})
    msp.add_line((x - t * 0.30, a), (x + t * 0.30, a), dxfattribs={"layer": "VENTANAS"})
    msp.add_line((x - t * 0.30, b), (x + t * 0.30, b), dxfattribs={"layer": "VENTANAS"})

def furn(x1, y1, x2, y2):
    msp.add_lwpolyline([(x1, y1), (x2, y1), (x2, y2), (x1, y2), (x1, y1)],
                       dxfattribs={"layer": "MOBILIARIO"})

def room_label(cx, cy, name, area):
    txt(cx, cy + 0.25, name, 0.32, "TEXTO", align=TextEntityAlignment.MIDDLE_CENTER)
    txt(cx, cy - 0.25, f"{area:.1f} m²", 0.28, "TEXTO", align=TextEntityAlignment.MIDDLE_CENTER)

def dim_h(x0, x1, y, label):
    msp.add_line((x0, y), (x1, y), dxfattribs={"layer": "COTAS"})
    for x in (x0, x1):
        msp.add_line((x, y - 0.10), (x, y + 0.10), dxfattribs={"layer": "COTAS"})
        msp.add_line((x, 0.0), (x, y), dxfattribs={"layer": "COTAS"})
    txt((x0 + x1) / 2, y + 0.18, label, 0.24, "COTAS", align=TextEntityAlignment.MIDDLE_CENTER)

def dim_v(x, y0, y1, label):
    msp.add_line((x, y0), (x, y1), dxfattribs={"layer": "COTAS"})
    for y in (y0, y1):
        msp.add_line((x - 0.10, y), (x + 0.10, y), dxfattribs={"layer": "COTAS"})
        msp.add_line((11.40, y), (x, y), dxfattribs={"layer": "COTAS"})
    txt(x + 0.28, (y0 + y1) / 2, label, 0.24, "COTAS", rot=90.0, align=TextEntityAlignment.MIDDLE_CENTER)

# ================================================================ GEOMETRÍA v6
SP_Y0, SP_Y1 = 5.90, 13.00                 # corredor X 0-1.40 (vestíbulo Y 0-5.90 + corredor)
HA_Y0, HA_Y1, HA_X1 = 13.00, 14.10, 4.50   # distribuidor Y 13.00-14.10 X 0-4.50
NOOK_X0, NOOK_Y0, NOOK_Y1 = 4.50, 13.00, 14.10  # nido-vestidor dorm3
TR_X0, TR_Y0 = 6.40, 13.00                  # trastero X 6.40-8.00
B_Y0, B_Y1 = 7.40, 8.80                     # baño común
S_Y0, S_Y1 = 8.80, 10.20                    # baño suite
D_Y0, D_Y1 = 10.20, 13.00                   # dorm. principal
R_Y0, R_Y1 = 14.10, Y1                       # banda trasera

# --- v6: salón ampliado, cocina junto a escalera, porche
SAL_X0, SAL_X1 = 1.40, PX0                   # salón X 1.40-6.40
SAL_Y1 = B_Y0                                # salón Y 0-7.40 (absorbe la antigua cocina)
COC_X0, COC_X1 = PX0, 10.40                  # cocina X 6.40-10.40
COC_Y1 = 5.00                                # cocina Y 0-5.00
ST_X0, ST_X1 = 10.40, 11.40                  # escalera X 10.40-11.40 (esquina derecha)
ST_Y0, ST_Y1 = 0.00, 5.00                    # escalera Y 0.00-5.00 (recta, desde la puerta)
PR_Y0, PR_Y1 = 5.00, 7.60                    # porche Y 5.00-7.60 (X 6.40-11.40)
CD_Y0, CD_Y1 = 1.00, 4.40                    # corredera doble salón-cocina (en X 6.40)

# --- envolvente
wall_v(X0, Y0, Y1, [], 0.30, "MUROS")                        # medianera izq
wall_v(X1, Y0, PY0, [], 0.30, "MUROS")                       # fachada der frente
wall_v(X1, PY0, PY1, [], 0.30, "MUROS")                      # medianera der (patio)
wall_v(X1, PY1, Y1, [], 0.30, "MUROS")                       # fachada der trasero
wall_h(Y0, X0, X1, [(0.30, 1.30), (2.60, 4.40), (4.80, 6.00), (6.90, 8.10), (8.90, 9.90), (10.40, 11.40)], 0.30, "MUROS")  # Moreno Torroba
wall_h(Y1, X0, X1, [(0.80, 2.40), (3.60, 5.20), (8.60, 11.00)], 0.30, "MUROS")   # calle trasera

# --- patio + porche
poly_p = [(PX0, PY0), (PX1, PY0), (PX1, PY1), (PX0, PY1)]
ph = msp.add_hatch(dxfattribs={"layer": "PATIO"})
ph.set_pattern_fill("NET3", scale=0.12)
ph.paths.add_polyline_path(poly_p, is_closed=True)
# porche cubierto (hatch diagonal + contorno discontinuo)
poly_pr = [(PX0, PR_Y0), (PX1, PR_Y0), (PX1, PR_Y1), (PX0, PR_Y1)]
prh = msp.add_hatch(dxfattribs={"layer": "PORCHE"})
prh.set_pattern_fill("ANSI32", scale=0.30)
prh.paths.add_polyline_path(poly_pr, is_closed=True)
msp.add_lwpolyline(poly_pr + [poly_pr[0]], dxfattribs={"layer": "PORCHE", "linetype": "DASHED"})
for cx in (7.00, 9.60):
    msp.add_lwpolyline([(cx - 0.10, PR_Y1 - 0.10), (cx + 0.10, PR_Y1 - 0.10),
                        (cx + 0.10, PR_Y1 + 0.10), (cx - 0.10, PR_Y1 + 0.10), (cx - 0.10, PR_Y1 - 0.10)],
                       dxfattribs={"layer": "MUROS"})

# --- pared izquierda del pasillo/corredor y vestíbulo (X 1.40)
wall_v(1.40, Y0, SP_Y1, [(1.40, 4.60), (6.10, 6.80), (7.90, 8.60)], 0.10, "TABIQUES")

# --- separación salón/cocina (corredera doble) + salón/porche + columna húmeda (X 6.40)
wall_v(PX0, Y0, COC_Y1, [(CD_Y0, CD_Y1)], 0.10, "TABIQUES")   # salón/cocina (corredera)
wall_v(PX0, COC_Y1, B_Y0, [(5.30, 6.20)], 0.30, "MUROS")      # salón/porche (puerta)
wall_v(PX0, B_Y0, PY1, [(7.80, 8.40), (9.00, 9.60), (11.00, 12.20)], 0.30, "MUROS")  # patio izq (ventanas)

# --- cocina -> porche (acristalado) + cierre del porche
wall_h(COC_Y1, PX0, X1, [(6.40, 10.40)], 0.30, "MUROS")       # solo X 10.40-11.40 (bajo escalera)
msp.add_line((6.40, 4.90), (10.40, 4.90), dxfattribs={"layer": "VENTANAS"})
msp.add_line((6.40, 5.10), (10.40, 5.10), dxfattribs={"layer": "VENTANAS"})
msp.add_line((6.40, 4.90), (6.40, 5.10), dxfattribs={"layer": "VENTANAS"})
msp.add_line((10.40, 4.90), (10.40, 5.10), dxfattribs={"layer": "VENTANAS"})

# --- caja de escalera (portal B, recta directa)
wall_v(ST_X0, ST_Y0, ST_Y1, [], 0.15, "MUROS")                # caja escalera oeste

# --- columna húmeda (tabiquería)
wall_h(B_Y0, 1.40, PX0, [], 0.10, "TABIQUES")                 # salón/baño común
wall_h(S_Y0, 1.40, PX0, [], 0.10, "TABIQUES")                 # baño común/suite
wall_h(D_Y0, 1.40, PX0, [(3.30, 4.00)], 0.10, "TABIQUES")     # suite/dorm (puerta suite)

# --- distribuidor + nido-vestidor + trastero + cochera
wall_h(HA_Y1, X0, HA_X1, [(0.80, 1.50), (3.60, 4.30)], 0.10, "TABIQUES")  # dorm2/dorm3
wall_h(HA_Y0, 1.40, 8.00, [(2.20, 2.90)], 0.10, "TABIQUES")  # sur: dorm princ + vestidor dorm3 + trastero
wall_v(HA_X1, HA_Y0, NOOK_Y1, [], 0.10, "TABIQUES")          # este del distribuidor (vestidor dorm3)
wall_v(TR_X0, HA_Y0, Y1, [], 0.10, "TABIQUES")               # dorm3/trastero (toda altura)
wall_v(8.00, HA_Y0, Y1, [(13.30, 13.90)], 0.15, "MUROS")     # trastero/cochera (puerta trastero)

# --- banda trasera
wall_v(3.20, R_Y0, Y1, [], 0.10, "TABIQUES")                 # dorm2/dorm3

# ================================================================ PUERTAS
door_h(Y0, 0.30, 1.30, 1)        # entrada Vivienda A (izquierda) · 1,00 m de ancho
door_h(Y0, 10.40, 11.40, 1)      # portal Vivienda B (esquina derecha, al pie de la escalera)
sliding_v(PX0, CD_Y0, CD_Y1)     # PUERTA CORREDERA DOBLE salón <-> cocina
door_v(PX0, 5.30, 6.20, -1)      # salón -> porche
door_v(1.40, 7.90, 8.60, 1)      # baño común (desde corredor)
door_h(D_Y0, 3.30, 4.00, -1)     # baño suite (desde dorm principal)
door_h(HA_Y0, 2.20, 2.90, 1)     # dorm. principal (desde distribuidor)
door_h(HA_Y1, 0.80, 1.50, 1)     # dorm2 (desde distribuidor)
door_h(HA_Y1, 3.60, 4.30, 1)     # dorm3 (desde distribuidor)
door_v(8.00, 13.30, 13.90, 1)    # trastero (desde cochera)

# ================================================================ VENTANAS
window_h(Y0, 2.60, 4.40)         # salón frente
window_h(Y0, 4.80, 6.00)         # salón frente
window_h(Y0, 6.90, 8.10)         # cocina frente
window_h(Y0, 8.90, 9.90)         # cocina frente
window_v(11.40, 2.80, 3.60)      # escalera (fachada derecha)
window_v(PX0, 7.80, 8.40)        # baño común -> patio
window_v(PX0, 9.00, 9.60)        # baño suite -> patio
window_v(PX0, 11.00, 12.20)      # dorm. principal -> patio
window_h(Y1, 0.80, 2.40)         # dorm2 trasera
window_h(Y1, 3.60, 5.20)         # dorm3 trasera
# portón cochera
msp.add_line((8.60, Y1), (8.60, Y1 + 0.30), dxfattribs={"layer": "PUERTAS"})
msp.add_line((11.00, Y1), (11.00, Y1 + 0.30), dxfattribs={"layer": "PUERTAS"})
msp.add_line((8.60, Y1 + 0.30), (11.00, Y1 + 0.30), dxfattribs={"layer": "PUERTAS"})
txt(9.80, Y1 + 0.65, "PORTÓN COCHERA", 0.24, "TEXTO", align=TextEntityAlignment.MIDDLE_CENTER)
txt(10.35, 13.42, "ABIERTO AL PATIO", 0.20, "TEXTO", align=TextEntityAlignment.MIDDLE_CENTER)

# ================================================================ ESCALERA VIVIENDA B (recta directa)
for i in range(1, 18):
    y = ST_Y0 + i * (ST_Y1 - ST_Y0) / 17.0
    if y < ST_Y1:
        msp.add_line((ST_X0 + 0.05, y), (ST_X1 - 0.05, y), dxfattribs={"layer": "ESCALERA"})
msp.add_lwpolyline([(ST_X0, ST_Y0), (ST_X1, ST_Y0), (ST_X1, ST_Y1), (ST_X0, ST_Y1), (ST_X0, ST_Y0)],
                   dxfattribs={"layer": "ESCALERA"})
txt(10.90, 2.30, "ESCALERA VIV. B", 0.26, "ESCALERA", 90.0, TextEntityAlignment.MIDDLE_CENTER)
txt(10.90, 4.30, "↑ PLANTA ALTA", 0.20, "ESCALERA", align=TextEntityAlignment.MIDDLE_CENTER)
txt(10.90, 0.75, "1,00 x 5,00 m", 0.20, "ESCALERA", align=TextEntityAlignment.MIDDLE_CENTER)
txt(10.90, -0.40, "PORTAL VIV. B", 0.22, "ESCALERA", align=TextEntityAlignment.MIDDLE_CENTER)

# ================================================================ ETIQUETAS
txt(0.70, 3.00, "VESTÍBULO", 0.24, "TEXTO", 90.0, TextEntityAlignment.MIDDLE_CENTER)
txt(0.70, 9.45, "CORREDOR", 0.26, "TEXTO", 90.0, TextEntityAlignment.MIDDLE_CENTER)
txt(2.25, 13.72, "DISTRIBUIDOR", 0.24, "TEXTO", align=TextEntityAlignment.MIDDLE_CENTER)
txt(2.25, 13.30, "LUCERNARIO", 0.20, "TEXTO", align=TextEntityAlignment.MIDDLE_CENTER)
txt(4.00, 0.60, "PUERTA CORREDERA DOBLE", 0.20, "TEXTO", align=TextEntityAlignment.MIDDLE_CENTER)

# patio + porche (texto en negro para legibilidad)
txt((PX0 + PX1) / 2, 9.90, "PATIO 5 x 8 m · 40 m²", 0.30, "TEXTO", align=TextEntityAlignment.MIDDLE_CENTER)
txt((PX0 + PX1) / 2, 8.90, "Luz y ventilación", 0.26, "TEXTO", align=TextEntityAlignment.MIDDLE_CENTER)
txt((PX0 + PX1) / 2, 6.55, "PORCHE CUBIERTO", 0.32, "TEXTO", align=TextEntityAlignment.MIDDLE_CENTER)
txt((PX0 + PX1) / 2, 6.15, "13,0 m² · TECHO +2,90", 0.24, "TEXTO", align=TextEntityAlignment.MIDDLE_CENTER)
txt((PX0 + PX1) / 2, 5.70, "Acceso desde salón y cocina", 0.22, "TEXTO", align=TextEntityAlignment.MIDDLE_CENTER)

# ================================================================ MOBILIARIO
# salón-comedor (X 1,40-6,40 x Y 0-7,40)
furn(2.00, 2.40, 5.00, 3.10)       # sofá (frente al TV)
furn(2.60, 6.98, 4.20, 7.32)       # TV (pared del baño)
furn(2.40, 4.60, 4.00, 6.20)       # mesa comedor
furn(1.60, 0.30, 2.20, 0.90)       # butaca (junto a ventana)
# cocina (X 6,40-10,40 x Y 0-5,00)
furn(6.55, 4.55, 10.25, 4.90)      # encimera sur (abre al porche)
furn(10.05, 0.60, 10.35, 4.50)     # encimera este (junto a escalera)
furn(7.60, 2.20, 9.20, 2.70)       # isla
furn(9.55, 0.40, 10.00, 1.10)      # frigorífico
# baño común
furn(1.60, 7.45, 3.60, 7.80)       # lavabo (mueble)
furn(2.20, 8.05, 2.60, 8.75)       # wc
furn(5.50, 7.55, 6.40, 8.65)       # ducha
# baño suite
furn(1.60, 8.85, 3.60, 9.20)       # lavabo (mueble)
furn(2.20, 9.40, 2.60, 10.10)      # wc
furn(5.50, 8.95, 6.40, 10.05)      # ducha
# dorm. principal
furn(4.00, 11.00, 5.80, 13.00)     # cama (pared norte)
furn(1.55, 10.80, 2.05, 12.60)     # armario (pared oeste)
# banda trasera
furn(0.15, 15.30, 1.65, 17.30)     # cama dorm2
furn(2.50, 15.20, 3.15, 17.00)     # armario dorm2
furn(4.90, 15.30, 6.40, 17.30)     # cama dorm3 (pared este)
furn(6.55, 13.20, 7.00, 17.40)     # estanterías trastero
# cochera
furn(8.30, 14.60, 10.10, 17.40)    # coche
# porche
furn(7.00, 6.30, 8.60, 6.90)       # mesa de terraza

# ================================================================ ETIQUETAS DE ESTANCIAS
room_label(3.90, 3.70, "SALÓN-COMEDOR", 37.0)
room_label(8.40, 2.50, "COCINA", 20.0)
room_label(3.90, 8.10, "BAÑO", 7.0)
room_label(3.90, 9.50, "BAÑO SUITE", 7.0)
room_label(3.90, 11.60, "DORM. PRINCIPAL", 14.0)
room_label(1.60, 15.85, "DORM. 2", 11.2)
room_label(4.30, 15.85, "DORM. 3", 11.2)
txt(5.45, 13.62, "VESTIDOR", 0.20, "TEXTO", align=TextEntityAlignment.MIDDLE_CENTER)
txt(5.45, 13.34, "DORM. 3 · 2,1 m²", 0.18, "TEXTO", align=TextEntityAlignment.MIDDLE_CENTER)
room_label(7.20, 15.30, "TRASTERO", 7.4)
room_label(9.70, 13.90, "COCHERA", 15.6)

# ================================================================ NOTAS
txt(0.2, 19.90, "v6.1 · COCINA JUNTO A ESCALERA Y SALÓN AMPLIADO:", 0.28, "TEXTO")
txt(0.2, 19.55, "• COCINA → FRENTE DERECHA (X 6,40–10,40), LINDANDO CON LA ESCALERA DE P.A.", 0.20, "TEXTO")
txt(0.2, 19.25, "• LA ANTIGUA COCINA SE INCORPORA AL SALÓN (X 1,40–6,40 × Y 0–7,40 = 37 m²)", 0.20, "TEXTO")
txt(0.2, 18.95, "• ÚNICA SEPARACIÓN COCINA–SALÓN: PUERTA CORREDERA DOBLE (ABIERTA = TODO UNIDO)", 0.20, "TEXTO")
txt(0.2, 18.65, "• COCINA Y SALÓN ABREN AL PORCHE · PORTAL VIV. B EN ESQUINA DERECHA", 0.20, "TEXTO")
txt(0.2, 18.35, "• PUERTAS DE ACCESO DESDE LA CALLE: PORTAL A Y PORTAL B · 1,00 m DE ANCHO", 0.20, "TEXTO")

# ================================================================ COTAS + SECCIÓN
dim_h(0.0, 11.40, -0.55, "11,40 m")
dim_v(11.70, 0.0, 17.60, "17,60 m")
msp.add_line((10.90, 0.25), (10.90, 17.35), dxfattribs={"layer": "COTAS", "linetype": "DASHED"})
txt(10.78, 0.55, "Y", 0.30, "COTAS", align=TextEntityAlignment.MIDDLE_CENTER)
txt(10.78, 17.05, "Y", 0.30, "COTAS", align=TextEntityAlignment.MIDDLE_CENTER)

# ================================================================ TÍTULO + CAJETÍN
txt((X0 + X1) / 2, Y0 - 1.10, "PLANTA BAJA · VIVIENDA A · ESCALA 1:50", 0.5, "TEXTO", align=TextEntityAlignment.MIDDLE_CENTER)
msp.add_lwpolyline([(0.0, -3.0), (11.40, -3.0), (11.40, -1.8), (0.0, -1.8), (0.0, -3.0)],
                   close=True, dxfattribs={"layer": "CAJETIN"})
txt(0.2, -2.75, "P-01 · PLANTA BAJA (VIVIENDA A) · v6.1", 0.28, "CAJETIN")
txt(0.2, -2.1, "CASA BIFAMILIAR · PALMA DEL RÍO · SOLAR 200 m² · S1", 0.26, "CAJETIN")
txt(9.4, -2.75, "ESCALA 1:50", 0.26, "CAJETIN")
txt(10.6, -2.75, "m", 0.26, "CAJETIN")

doc.saveas(DXF)

# ---------------------------------------------------------------- preview
fig = plt.figure(figsize=(9.5, 14), dpi=130)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_facecolor("white")
ctx = RenderContext(doc)
Frontend(ctx, MatplotlibBackend(ax)).draw_layout(msp)
ax.set_aspect("equal")
fig.savefig(PNG, facecolor="white")
plt.close(fig)
print("OK ->", DXF)
print("PNG ->", PNG)
