# -*- coding: utf-8 -*-
"""PASO 03 - PLANTA ALTA (VIVIENDA B) EN BRUTO - v7.
- v6: espejo de P-01: COCINA junto a la escalera (X 6,40-10,40 x Y 0-5,00), salón
  ampliado (X 1,40-6,40 x Y 0-7,40) separado por PUERTA CORREDERA DOBLE. Fontanería
  apilada con planta baja.
- v7: DORMITORIO 2 al fondo-derecha (X 6,40-11,40 x Y 13,00-17,60, sobre la cochera)
  y PATIO al fondo-izquierda (X 0-3,20 x Y 14,10-17,60), intercambiando dorm2 y la
  antigua terraza. El patio de planta baja se mantiene (vacío X 6,40-11,40 x Y 7,60-13,00).
- Acceso: escalera recta (esquina derecha) -> PASILLO sobre el porche, entrada Vivienda B."""
import os
import math
import ezdxf
from ezdxf.enums import TextEntityAlignment
from ezdxf.addons.drawing import RenderContext, Frontend
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
import matplotlib.pyplot as plt

from plan_data import X0, Y0, X1, Y1, PX0, PY0, PX1, PY1

BASE = os.path.dirname(os.path.abspath(__file__))
DXF = os.path.join(BASE, "paso-03-planta-alta.dxf")
PNG = os.path.join(BASE, "preview-03-planta-alta.png")

doc = ezdxf.new("R2010", setup=True)
doc.units = ezdxf.units.M
msp = doc.modelspace()

def layer(name, color, lw100, lt="CONTINUOUS"):
    doc.layers.add(name, color=color, linetype=lt)
    doc.layers.get(name).dxf.lineweight = lw100

layer("MUROS", 7, 60)
layer("TAB_PREV", 3, 13, "DASHED")
layer("PUERTAS", 5, 18)
layer("VENTANAS", 5, 18)
layer("ESCALERA", 5, 18)
layer("MOBILIARIO", 8, 13)
layer("VACIO", 3, 25)
layer("PASILLO", 4, 25)
layer("TERRAZA", 4, 25)
layer("PREINST", 6, 18)
layer("TEXTO", 7, 18)
layer("CAJETIN", 7, 35)
layer("COTAS", 5, 18)

def txt(x, y, s, h=0.30, lay="TEXTO", rot=0.0, align=TextEntityAlignment.LEFT):
    t = msp.add_text(s, dxfattribs={"layer": lay, "height": h, "rotation": rot})
    t.set_placement((x, y), align=align)
    return t

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

def prev_line_h(y, x0, x1, gaps):
    for a, b in clip(x0, x1, gaps):
        msp.add_line((a, y), (b, y), dxfattribs={"layer": "TAB_PREV"})

def prev_line_v(x, y0, y1, gaps):
    for a, b in clip(y0, y1, gaps):
        msp.add_line((x, a), (x, b), dxfattribs={"layer": "TAB_PREV"})

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

def preinst(x, y, label):
    msp.add_circle((x, y), 0.22, dxfattribs={"layer": "PREINST"})
    txt(x, y, label, 0.20, "PREINST", align=TextEntityAlignment.MIDDLE_CENTER)

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

# ================================================================ GEOMETRÍA v7
SP_Y0, SP_Y1 = 5.90, 13.00                 # corredor X 0-1.40
HA_Y0, HA_Y1, HA_X1 = 13.00, 14.10, 6.40   # distribuidor X 0-6.40
B_Y0, B_Y1 = 7.40, 8.80                    # baño común
S_Y0, S_Y1 = 8.80, 10.20                   # baño suite
D_Y0, D_Y1 = 10.20, 13.00                  # dorm. principal
R_Y0, R_Y1 = 14.10, Y1                     # banda trasera

# --- v6: salón ampliado y cocina junto a escalera (espejo de P-01)
SAL_X0, SAL_X1 = 1.40, PX0                 # salón X 1.40-6.40
SAL_Y1 = B_Y0                              # salón Y 0-7.40
COC_X0, COC_X1 = PX0, 10.40                # cocina X 6.40-10.40 (junto a escalera)
COC_Y1 = 5.00                              # cocina Y 0-5.00
CD_Y0, CD_Y1 = 1.00, 4.40                  # corredera doble salón-cocina (en X 6.40)

# --- v7: dormitorio 2 al fondo-derecha, patio al fondo-izquierda
D2_X0, D2_X1 = PX0, X1                     # dorm. 2 X 6.40-11.40 (sobre cochera)
D2_Y0, D2_Y1 = HA_Y0, Y1                   # dorm. 2 Y 13.00-17.60
PAT_X0, PAT_X1 = X0, 3.20                  # patio X 0-3.20
PAT_Y0, PAT_Y1 = R_Y0, Y1                  # patio Y 14.10-17.60

# --- escalera recta directa + pasillo sobre porche
ST_X0, ST_X1 = 10.40, 11.40
ST_Y0, ST_Y1 = 0.00, 5.00
PS_Y0, PS_Y1 = 5.00, 7.60                  # pasillo X 6.40-11.40 (sobre el porche)
VO_Y0 = PS_Y1                              # vacío desde Y 7.60

# --- envolvente (obra)
wall_v(X0, Y0, Y1, [], 0.30, "MUROS")
wall_v(X1, Y0, PY0, [], 0.30, "MUROS")
wall_v(X1, PY0, PY1, [], 0.30, "MUROS")
wall_v(X1, PY1, Y1, [], 0.30, "MUROS")
wall_h(Y0, X0, X1, [(2.60, 4.40), (4.80, 6.00), (6.90, 8.10), (8.90, 9.90)], 0.30, "MUROS")
wall_h(Y1, X0, X1, [(3.60, 5.20), (7.00, 9.00), (9.80, 11.20)], 0.30, "MUROS")

# --- caja de escalera (obra) + pasillo sobre porche
wall_v(ST_X0, ST_Y0, ST_Y1, [], 0.15, "MUROS")               # caja escalera oeste
wall_h(PS_Y1, PX0, X1, [(7.00, 9.40)], 0.30, "MUROS")        # pasillo -> vacío (ventana)

# --- pared este de la columna húmeda (frente al vacío/pasillo)
# (v8: la pared en PX0 de Y=5.00 a 7.60 se elimina para integrar el pasillo sobre porche al salón -> gran salón de 50 m²)
wall_v(PX0, PS_Y1, PY1, [(7.80, 8.40), (9.00, 9.60), (11.00, 12.20)], 0.30, "MUROS")  # ventanas al vacío

# --- cocina -> pasillo (acristalado) sobre el forjado del porche
msp.add_line((6.40, 4.90), (10.40, 4.90), dxfattribs={"layer": "VENTANAS"})
msp.add_line((6.40, 5.10), (10.40, 5.10), dxfattribs={"layer": "VENTANAS"})
msp.add_line((6.40, 4.90), (6.40, 5.10), dxfattribs={"layer": "VENTANAS"})
msp.add_line((10.40, 4.90), (10.40, 5.10), dxfattribs={"layer": "VENTANAS"})

# --- tabiquería prevista (discontinua) v6 + v7 + v8
prev_line_v(1.40, Y0, SP_Y1, [(1.40, 4.60), (6.10, 6.80), (7.90, 8.60)])  # salón/corredor/baño
prev_line_v(PX0, Y0, COC_Y1, [(CD_Y0, CD_Y1)])                 # salón/cocina (corredera doble)
prev_line_h(B_Y0, 1.40, PX0, [])                               # salón/baño
prev_line_h(S_Y0, 1.40, PX0, [])                               # baño/suite
prev_line_h(D_Y0, 1.40, PX0, [(3.30, 4.00)])                   # suite/dorm (puerta)
prev_line_h(HA_Y0, 1.40, HA_X1, [(2.20, 2.90)])                # distribuidor sur (dorm ppal)
prev_line_h(HA_Y1, X0, HA_X1, [(0.80, 1.50), (3.60, 4.30)])    # distribuidor norte (patio + dorm3)
prev_line_v(3.20, R_Y0, Y1, [])                                # patio/dorm3

# --- v7: cerramiento del nuevo dormitorio 2 (fondo-derecha)
prev_line_v(PX0, HA_Y0, Y1, [(13.20, 14.00)])                  # puerta desde distribuidor
prev_line_h(HA_Y0, PX0, X1, [(7.00, 10.40)])                   # muro sur al vacío (ventana)

# --- vacío del patio (parcial: el porche lo cubre hasta Y 7.60)
void_poly = [(PX0, VO_Y0), (PX1, VO_Y0), (PX1, PY1), (PX0, PY1)]
vh = msp.add_hatch(dxfattribs={"layer": "VACIO"})
vh.set_pattern_fill("ANSI31", scale=0.15)
vh.paths.add_polyline_path(void_poly, is_closed=True)
msp.add_lwpolyline(void_poly + [void_poly[0]], dxfattribs={"layer": "VACIO"})
txt((PX0 + PX1) / 2, (VO_Y0 + PY1) / 2, "PATIO · VACÍO", 0.32, "VACIO", align=TextEntityAlignment.MIDDLE_CENTER)
txt((PX0 + PX1) / 2, (VO_Y0 + PY1) / 2 - 0.45, "27,0 m² (bajo el porche, cubierto)", 0.22, "VACIO", align=TextEntityAlignment.MIDDLE_CENTER)

# --- espacio pasillo integrado en el salón diáfano
txt(8.90, 6.60, "ZONA SALÓN COMPARTIDA", 0.28, "TEXTO", align=TextEntityAlignment.MIDDLE_CENTER)
txt(8.90, 6.20, "13,0 m² (SOBRE PORCHE)", 0.22, "TEXTO", align=TextEntityAlignment.MIDDLE_CENTER)

# --- v7: nuevo patio al fondo-izquierda (exterior, sin techar)
pat_poly = [(PAT_X0, PAT_Y0), (PAT_X1, PAT_Y0), (PAT_X1, PAT_Y1), (PAT_X0, PAT_Y1)]
pth = msp.add_hatch(dxfattribs={"layer": "TERRAZA"})
pth.set_pattern_fill("NET3", scale=0.12)
pth.paths.add_polyline_path(pat_poly, is_closed=True)
msp.add_lwpolyline(pat_poly + [pat_poly[0]], dxfattribs={"layer": "TERRAZA", "linetype": "DASHED"})

# ================================================================ PUERTAS
sliding_v(PX0, CD_Y0, CD_Y1)     # PUERTA CORREDERA DOBLE salón <-> cocina
door_v(1.40, 7.90, 8.60, 1)      # baño (desde corredor)
door_v(1.40, 7.90, 8.60, 1)      # baño (desde corredor)
door_h(D_Y0, 3.30, 4.00, -1)     # suite (desde dorm principal)
door_h(HA_Y0, 2.20, 2.90, 1)     # dorm. principal (desde distribuidor)
door_v(PX0, 13.20, 14.00, 1)     # distribuidor -> nuevo dorm. 2
door_h(HA_Y1, 0.80, 1.50, 1)     # distribuidor -> patio (fondo-izq)
door_h(HA_Y1, 3.60, 4.30, 1)     # dorm3

# ================================================================ VENTANAS
window_h(Y0, 2.60, 4.40)         # salón frente
window_h(Y0, 4.80, 6.00)         # salón frente
window_h(Y0, 6.90, 8.10)         # cocina frente
window_h(Y0, 8.90, 9.90)         # cocina frente
window_v(11.40, 2.80, 3.60)      # escalera (fachada derecha)
window_v(PX0, 7.80, 8.40)        # baño -> vacío
window_v(PX0, 9.00, 9.60)        # suite -> vacío
window_v(PX0, 11.00, 12.20)      # dorm. principal -> vacío
window_h(Y1, 3.60, 5.20)         # dorm3 trasera
window_h(Y1, 7.00, 9.00)         # nuevo dorm. 2 (trasera)
window_h(Y1, 9.80, 11.20)        # nuevo dorm. 2 (trasera)
window_h(HA_Y0, 7.00, 10.40)     # nuevo dorm. 2 -> vacío (ventana al patio)

# ================================================================ ESCALERA (bajada a portal)
for i in range(1, 18):
    y = ST_Y0 + i * (ST_Y1 - ST_Y0) / 17.0
    if y < ST_Y1:
        msp.add_line((ST_X0 + 0.05, y), (ST_X1 - 0.05, y), dxfattribs={"layer": "ESCALERA"})
msp.add_lwpolyline([(ST_X0, ST_Y0), (ST_X1, ST_Y0), (ST_X1, ST_Y1), (ST_X0, ST_Y1), (ST_X0, ST_Y0)],
                   dxfattribs={"layer": "ESCALERA"})
txt(10.90, 2.30, "ESCALERA", 0.24, "ESCALERA", 90.0, TextEntityAlignment.MIDDLE_CENTER)
txt(10.90, 4.30, "↓ PORTAL VIV. B", 0.20, "ESCALERA", align=TextEntityAlignment.MIDDLE_CENTER)

# ================================================================ ETIQUETAS
txt(0.70, 9.45, "CORREDOR", 0.26, "TEXTO", 90.0, TextEntityAlignment.MIDDLE_CENTER)
txt(2.25, 13.72, "DISTRIBUIDOR", 0.24, "TEXTO", align=TextEntityAlignment.MIDDLE_CENTER)
txt(2.25, 13.30, "LUCERNARIO", 0.20, "TEXTO", align=TextEntityAlignment.MIDDLE_CENTER)
txt(4.00, 0.60, "PUERTA CORREDERA DOBLE", 0.20, "TEXTO", align=TextEntityAlignment.MIDDLE_CENTER)
txt(1.60, 16.55, "PATIO", 0.30, "TEXTO", align=TextEntityAlignment.MIDDLE_CENTER)
txt(1.60, 16.15, "EXTERIOR · 11,2 m²", 0.22, "TEXTO", align=TextEntityAlignment.MIDDLE_CENTER)

# ================================================================ PREINSTALACIONES
preinst(7.00, 6.50, "E")          # cuadro eléctrico (pasillo entrada)
preinst(10.55, 6.50, "T")         # telecom pasillo
preinst(8.40, 4.30, "F")          # fontanería cocina (junto encimera sur)
preinst(8.80, 4.30, "BJ")         # bajante cocina (apilado con P-01)
preinst(4.60, 8.30, "F")          # fontanería baño
preinst(5.00, 8.30, "BJ")         # bajante baño
preinst(4.60, 9.90, "F")          # fontanería suite
preinst(5.00, 9.90, "BJ")         # bajante suite
preinst(3.40, 5.60, "CL")         # climatización salón
preinst(3.40, 6.10, "T")          # telecom salón
preinst(3.20, 12.60, "CL")        # climatización dorm principal
preinst(8.60, 14.50, "CL")        # climatización nuevo dorm. 2
preinst(4.20, 15.20, "CL")        # climatización dorm3

# ================================================================ MOBILIARIO (orientativo)
# salón-comedor (X 1,40-6,40 x Y 0-7,40)
furn(2.00, 2.40, 5.00, 3.10)       # sofá (frente al TV)
furn(2.60, 6.98, 4.20, 7.32)       # TV (pared del baño)
furn(2.40, 4.60, 4.00, 6.20)       # mesa comedor
furn(1.60, 0.30, 2.20, 0.90)       # butaca (junto a ventana)
# cocina (X 6,40-10,40 x Y 0-5,00)
furn(6.55, 4.55, 10.25, 4.90)      # encimera sur (abre al pasillo)
furn(10.05, 0.60, 10.35, 4.50)     # encimera este (junto a escalera)
furn(7.60, 2.20, 9.20, 2.70)       # isla
furn(9.55, 0.40, 10.00, 1.10)      # frigorífico
# baño común
furn(1.60, 7.45, 3.60, 7.80)       # lavabo baño
furn(2.20, 8.05, 2.60, 8.75)       # wc baño
furn(5.50, 7.55, 6.40, 8.65)       # ducha baño
# baño suite
furn(1.60, 8.85, 3.60, 9.20)       # lavabo suite
furn(2.20, 9.40, 2.60, 10.10)      # wc suite
furn(5.50, 8.95, 6.40, 10.05)      # ducha suite
# dorm. principal
furn(4.00, 11.00, 5.80, 13.00)     # cama dorm principal
furn(1.55, 10.80, 2.05, 12.60)     # armario dorm principal
# nuevo dormitorio 2 (X 6,40-11,40 x Y 13,00-17,60)
furn(7.00, 15.60, 8.60, 17.30)     # cama (frente a la ventana trasera)
furn(10.30, 13.30, 11.20, 15.00)   # armario (medianera este)
furn(6.80, 13.20, 7.60, 13.90)     # escritorio (junto ventana al vacío)
# dorm3
furn(4.90, 15.30, 6.40, 17.30)     # cama dorm3
furn(3.35, 15.40, 3.95, 17.20)     # armario dorm3
# patio (fondo-izquierda)
furn(1.20, 15.60, 1.80, 16.40)     # macetero

# ================================================================ ETIQUETAS DE ESTANCIAS
room_label(3.90, 3.70, "SALÓN-COMEDOR DIÁFANO", 50.0)
room_label(8.40, 2.50, "COCINA", 20.0)
room_label(3.90, 8.10, "BAÑO", 7.0)
room_label(3.90, 9.50, "BAÑO SUITE", 7.0)
room_label(3.90, 11.60, "DORM. PRINCIPAL", 14.0)
room_label(8.90, 14.80, "DORM. 2", 23.0)
room_label(4.80, 15.85, "DORM. 3", 11.2)

# ================================================================ NOTAS + LEYENDA
txt(0.2, 19.45, "PLANTA ALTA · VIVIENDA B · v8 (GRAN SALÓN DIÁFANO 50 m²)", 0.26, "TEXTO")
txt(0.2, 19.10, "• v8 · SIN PARED SEPARADORA SALÓN-PASILLO: SALÓN AMPLIADO A 50 m² CORD. INTEGRADO", 0.20, "TEXTO")
txt(0.2, 18.82, "• v7 · DORM. 2 AL FONDO-DERECHA (23 m²) Y PATIO TRASERO ELEVADO PRIVADO (11,2 m²)", 0.20, "TEXTO")
txt(0.2, 18.54, "• ACCESO: ESCALERA RECTA INDEPENDIENTE DESDE PORTAL B A PLANTA ALTA", 0.20, "TEXTO")
txt(0.2, 18.26, "• CUBIERTA CERRADA Y TRANSITABLE SÓLO PARA MANTENIMIENTO (SIN ESCALERA AL TEJADO)", 0.20, "TEXTO")
txt(0.2, 17.98, "• FLUIDEZ TOTAL DE ILUMINACIÓN Y VENTILACIÓN EN TODAS LAS CARPINTERÍAS", 0.20, "TEXTO")

# ================================================================ COTAS + SECCIÓN
dim_h(0.0, 11.40, -0.55, "11,40 m")
dim_v(11.70, 0.0, 17.60, "17,60 m")
msp.add_line((10.90, 0.25), (10.90, 17.35), dxfattribs={"layer": "COTAS", "linetype": "DASHED"})
txt(10.78, 0.55, "Y", 0.30, "COTAS", align=TextEntityAlignment.MIDDLE_CENTER)
txt(10.78, 17.05, "Y", 0.30, "COTAS", align=TextEntityAlignment.MIDDLE_CENTER)

lg = [(8.0, 17.85), (11.4, 17.85), (11.4, 19.7), (8.0, 19.7), (8.0, 17.85)]
msp.add_lwpolyline(lg, close=True, dxfattribs={"layer": "CAJETIN"})
txt(8.2, 19.45, "PREINSTALACIONES", 0.24, "CAJETIN")
leyenda = [("E", "ELECTRICIDAD"), ("F", "FONTANERÍA"), ("BJ", "BAJANTES"),
           ("S", "SANEAMIENTO"), ("CL", "CLIMATIZACIÓN"), ("T", "TELECOM")]
for i, (lab, desc) in enumerate(leyenda):
    y = 19.10 - i * 0.24
    msp.add_circle((8.35, y), 0.13, dxfattribs={"layer": "CAJETIN"})
    txt(8.35, y, lab, 0.18, "CAJETIN", align=TextEntityAlignment.MIDDLE_CENTER)
    txt(8.62, y, desc, 0.17, "CAJETIN")

# ================================================================ TÍTULO + CAJETÍN
txt((X0 + X1) / 2, Y0 - 1.10, "PLANTA ALTA · VIVIENDA B · EN BRUTO · ESCALA 1:50", 0.5, "TEXTO", align=TextEntityAlignment.MIDDLE_CENTER)
msp.add_lwpolyline([(0.0, -3.0), (11.40, -3.0), (11.40, -1.8), (0.0, -1.8), (0.0, -3.0)],
                   close=True, dxfattribs={"layer": "CAJETIN"})
txt(0.2, -2.75, "P-02 · PLANTA ALTA (VIVIENDA B) · v7", 0.28, "CAJETIN")
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
