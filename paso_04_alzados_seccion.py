# -*- coding: utf-8 -*-
"""PASO 04 - ALZADOS + SECCIÓN (P-03/P-04).
- Alzado principal (c/ Moreno Torroba, sur) y alzado trasero (calle trasera, norte).
- Sección Y-Y (corte longitudinal a X = 10,90 por la escalera, el porche, el vacío
  del patio y el dormitorio 2).
- Alturas: planta baja 0,00 a +2,90 · planta alta +2,90 a +5,80 · parapeto +6,10."""
import os
import ezdxf
from ezdxf.enums import TextEntityAlignment
from ezdxf.addons.drawing import RenderContext, Frontend
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
import matplotlib.pyplot as plt

BASE = os.path.dirname(os.path.abspath(__file__))
DXF = os.path.join(BASE, "paso-04-alzados-seccion.dxf")
PNG = os.path.join(BASE, "preview-04-alzados-seccion.png")

doc = ezdxf.new("R2010", setup=True)
doc.units = ezdxf.units.M
msp = doc.modelspace()

def layer(name, color, lw100, lt="CONTINUOUS"):
    doc.layers.add(name, color=color, linetype=lt)
    doc.layers.get(name).dxf.lineweight = lw100

layer("MUROS", 7, 50)
layer("HUECOS", 5, 25)
layer("CARPINT", 6, 18)
layer("ESTRUCT", 8, 25)
layer("TEXTO", 7, 18)
layer("COTAS", 5, 18)
layer("CAJETIN", 7, 35)

def txt(x, y, s, h=0.28, lay="TEXTO", rot=0.0, align=TextEntityAlignment.LEFT):
    t = msp.add_text(s, dxfattribs={"layer": lay, "height": h, "rotation": rot})
    t.set_placement((x, y), align=align)
    return t

def hline(ox, oy, x0, x1, z, lay):
    msp.add_line((ox + x0, oy + z), (ox + x1, oy + z), dxfattribs={"layer": lay})

def vline(ox, oy, x, z0, z1, lay):
    msp.add_line((ox + x, oy + z0), (ox + x, oy + z1), dxfattribs={"layer": lay})

def rect(ox, oy, x0, x1, z0, z1, lay):
    msp.add_lwpolyline([(ox + x0, oy + z0), (ox + x1, oy + z0), (ox + x1, oy + z1),
                        (ox + x0, oy + z1), (ox + x0, oy + z0)], dxfattribs={"layer": lay})

def band(ox, oy, x0, x1, z0, z1, lay):
    r = [(ox + x0, oy + z0), (ox + x1, oy + z0), (ox + x1, oy + z1), (ox + x0, oy + z1)]
    msp.add_lwpolyline(r, close=True, dxfattribs={"layer": lay})
    h = msp.add_hatch(dxfattribs={"layer": lay})
    h.set_solid_fill()
    h.paths.add_polyline_path(r, is_closed=True)

def alz_window(ox, oy, x0, x1, z0, z1):
    rect(ox, oy, x0, x1, z0, z1, "HUECOS")
    hline(ox, oy, x0, x1, (z0 + z1) / 2, "CARPINT")
    vline(ox, oy, (x0 + x1) / 2, z0, z1, "CARPINT")

def alz_door(ox, oy, x0, x1, z0, z1):
    rect(ox, oy, x0, x1, z0, z1, "HUECOS")
    vline(ox, oy, x0 + 0.10, z0 + 0.10, z1 - 0.10, "CARPINT")
    vline(ox, oy, x1 - 0.10, z0 + 0.10, z1 - 0.10, "CARPINT")
    hline(ox, oy, x0, x1, z1 - 0.25, "CARPINT")

# --- alturas
HB, HA = 2.90, 5.80
PP = 6.10
SILL, WH, DH = 0.90, 1.50, 2.10
POR = 2.40   # portón cochera

# ================================================================ ALZADO PRINCIPAL (sur)
AX, AY = 0.0, 0.0
hline(AX, AY, -0.30, 11.70, 0.00, "MUROS")          # línea de tierra
rect(AX, AY, 0.00, 11.40, 0.00, PP, "MUROS")        # contorno
hline(AX, AY, 0.00, 11.40, HB, "ESTRUCT")           # forjado P.B.
hline(AX, AY, 0.00, 11.40, HA, "ESTRUCT")           # forjado P.A.
hline(AX, AY, 0.00, 11.40, PP, "ESTRUCT")           # parapeto
# planta baja
alz_door(AX, AY, 0.30, 1.30, 0.00, DH)              # portal A
alz_window(AX, AY, 2.60, 4.40, SILL, SILL + WH)     # salón
alz_window(AX, AY, 4.80, 6.00, SILL, SILL + WH)     # salón
alz_window(AX, AY, 6.90, 8.10, SILL, SILL + WH)     # cocina
alz_window(AX, AY, 8.90, 9.90, SILL, SILL + WH)     # cocina
alz_door(AX, AY, 10.40, 11.40, 0.00, DH)            # portal B (escalera)
# planta alta
alz_window(AX, AY, 2.60, 4.40, HB + SILL, HB + SILL + WH)
alz_window(AX, AY, 4.80, 6.00, HB + SILL, HB + SILL + WH)
alz_window(AX, AY, 6.90, 8.10, HB + SILL, HB + SILL + WH)
alz_window(AX, AY, 8.90, 9.90, HB + SILL, HB + SILL + WH)
alz_window(AX, AY, 10.55, 11.15, 2.40, 3.90)        # hueco de escalera
txt(5.70, 6.35, "ALZADO PRINCIPAL · C/ MORENO TORROBA", 0.26, "TEXTO", align=TextEntityAlignment.MIDDLE_CENTER)
txt(0.80, 2.45, "P. BAJA", 0.20, "TEXTO", align=TextEntityAlignment.MIDDLE_CENTER)
txt(0.80, 5.35, "P. ALTA", 0.20, "TEXTO", align=TextEntityAlignment.MIDDLE_CENTER)

# ================================================================ ALZADO TRASERO (norte)
BX, BY = 0.0, -8.5
hline(BX, BY, -0.30, 11.70, 0.00, "MUROS")
rect(BX, BY, 0.00, 11.40, 0.00, PP, "MUROS")
hline(BX, BY, 0.00, 11.40, HB, "ESTRUCT")
hline(BX, BY, 0.00, 11.40, HA, "ESTRUCT")
hline(BX, BY, 0.00, 11.40, PP, "ESTRUCT")
# planta baja
alz_window(BX, BY, 0.80, 2.40, SILL, SILL + WH)     # dorm2
alz_window(BX, BY, 3.60, 5.20, SILL, SILL + WH)     # dorm3
alz_door(BX, BY, 8.60, 11.00, 0.00, POR)            # portón cochera
# planta alta
band(BX, BY, 0.00, 3.20, HB, HB + 1.10, "ESTRUCT")  # parapeto del patio
alz_window(BX, BY, 3.60, 5.20, HB + SILL, HB + SILL + WH)   # dorm3
alz_window(BX, BY, 7.00, 9.00, HB + SILL, HB + SILL + WH)   # dormitorio 2
alz_window(BX, BY, 9.80, 11.20, HB + SILL, HB + SILL + WH)  # dormitorio 2
txt(5.70, BY + 6.35, "ALZADO TRASERO · CALLE TRASERA", 0.26, "TEXTO", align=TextEntityAlignment.MIDDLE_CENTER)
txt(1.60, BY + 2.55, "PATIO DORM. 2", 0.20, "TEXTO", align=TextEntityAlignment.MIDDLE_CENTER)
txt(9.80, BY + 2.75, "PORTÓN COCHERA", 0.20, "TEXTO", align=TextEntityAlignment.MIDDLE_CENTER)

# ================================================================ SECCIÓN Y-Y (X = 10,90)
CX, CY = 0.0, -17.5
NR = 17
RUN = 5.0 / NR
RISE = HB / NR
hline(CX, CY, -0.30, 17.90, 0.00, "MUROS")           # línea de tierra
band(CX, CY, 0.00, 17.60, 0.00, 0.30, "ESTRUCT")     # solera planta baja
# escalera (tramos 0-5,00)
for i in range(NR):
    x0, x1 = i * RUN, (i + 1) * RUN
    z0, z1 = i * RISE, (i + 1) * RISE
    hline(CX, CY, x0, x1, z0, "CARPINT")
    vline(CX, CY, x1, z0, z1, "CARPINT")
vline(CX, CY, 0.00, 0.30, 2.10, "MUROS")             # jamba portal B
alz_door(CX, CY, -0.10, 0.10, 0.00, DH)              # portal B
# porche + pasillo (5,00-7,60) y vacío (7,60-13,00) y dorm2/cochera (13,00-17,60)
band(CX, CY, 5.00, 7.60, HB, HB + 0.30, "ESTRUCT")   # forjado porche/pasillo
band(CX, CY, 13.00, 17.60, HB, HB + 0.30, "ESTRUCT") # forjado dorm2
band(CX, CY, 5.00, 7.60, HA, HA + 0.30, "ESTRUCT")   # cubierta pasillo
band(CX, CY, 0.00, 5.00, HA, HA + 0.30, "ESTRUCT")   # cubierta escalera
band(CX, CY, 13.00, 17.60, HA, HA + 0.30, "ESTRUCT") # cubierta dorm2
band(CX, CY, 5.00, 7.60, 0.30, HB, "ESTRUCT")        # porche (sombreado)
# parapeto del patio trasero (dorm2 lado trasero)
vline(CX, CY, 17.60, 0.30, POR, "MUROS")             # muro trasero cochera
vline(CX, CY, 17.60, HB, PP, "MUROS")                # parapeto trasero dorm2
# cotas de altura
hline(CX, CY, -0.80, 0.00, HB, "COTAS")
hline(CX, CY, -0.80, 0.00, HA, "COTAS")
txt(CX - 1.35, 2.95, "+2,90", 0.22, "COTAS", align=TextEntityAlignment.MIDDLE_CENTER)
txt(CX - 1.35, 5.85, "+5,80", 0.22, "COTAS", align=TextEntityAlignment.MIDDLE_CENTER)
txt(CX - 1.35, 0.22, "±0,00", 0.22, "COTAS", align=TextEntityAlignment.MIDDLE_CENTER)
# rótulos
txt(CX + 2.10, 1.30, "ESCALERA · 17 PELDAÑOS", 0.22, "TEXTO", align=TextEntityAlignment.MIDDLE_CENTER)
txt(CX + 6.30, 1.60, "PORCHE", 0.24, "TEXTO", align=TextEntityAlignment.MIDDLE_CENTER)
txt(CX + 6.30, 4.60, "PASILLO", 0.24, "TEXTO", align=TextEntityAlignment.MIDDLE_CENTER)
txt(CX + 10.30, 2.80, "PATIO · VACÍO", 0.24, "TEXTO", align=TextEntityAlignment.MIDDLE_CENTER)
txt(CX + 15.30, 4.60, "DORM. 2", 0.24, "TEXTO", align=TextEntityAlignment.MIDDLE_CENTER)
txt(CX + 15.30, 1.30, "COCHERA", 0.24, "TEXTO", align=TextEntityAlignment.MIDDLE_CENTER)
txt(CX + 8.80, 7.10, "SECCIÓN Y-Y · X = 10,90 (ESCALERA / PORCHE / PATIO / DORM. 2)", 0.26,
    "TEXTO", align=TextEntityAlignment.MIDDLE_CENTER)

# ================================================================ TÍTULO + CAJETÍN
txt(8.90, 8.0, "ALZADOS Y SECCIÓN · ESCALA 1:100", 0.5, "TEXTO", align=TextEntityAlignment.MIDDLE_CENTER)
msp.add_lwpolyline([(0.0, -19.6), (17.60, -19.6), (17.60, -18.4), (0.0, -18.4), (0.0, -19.6)],
                   close=True, dxfattribs={"layer": "CAJETIN"})
txt(0.2, -19.35, "P-03/P-04 · ALZADOS + SECCIÓN · v1", 0.28, "CAJETIN")
txt(0.2, -18.7, "CASA BIFAMILIAR · PALMA DEL RÍO · SOLAR 200 m² · S1", 0.26, "CAJETIN")
txt(14.2, -19.35, "ESCALA 1:100", 0.26, "CAJETIN")
txt(16.4, -19.35, "m", 0.26, "CAJETIN")

doc.saveas(DXF)

# ---------------------------------------------------------------- preview
fig = plt.figure(figsize=(10, 14), dpi=130)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_facecolor("white")
ctx = RenderContext(doc)
Frontend(ctx, MatplotlibBackend(ax)).draw_layout(msp)
ax.set_aspect("equal")
fig.savefig(PNG, facecolor="white")
plt.close(fig)
print("OK ->", DXF)
print("PNG ->", PNG)
