# -*- coding: utf-8 -*-
"""PASO 05 - CUADRO DE SUPERFICIES + RESUMEN Y PRESUPUESTO ORIENTATIVO (P-05)."""
import os
import ezdxf
from ezdxf.enums import TextEntityAlignment
from ezdxf.addons.drawing import RenderContext, Frontend
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
import matplotlib.pyplot as plt

BASE = os.path.dirname(os.path.abspath(__file__))
DXF = os.path.join(BASE, "paso-05-cuadro-superficies.dxf")
PNG = os.path.join(BASE, "preview-05-cuadro-superficies.png")

doc = ezdxf.new("R2010", setup=True)
doc.units = ezdxf.units.M
msp = doc.modelspace()

def layer(name, color, lw100):
    doc.layers.add(name, color=color)
    doc.layers.get(name).dxf.lineweight = lw100

layer("TEXTO", 7, 18)
layer("TABLA", 5, 18)
layer("CAJETIN", 7, 35)

def txt(x, y, s, h=0.26, lay="TEXTO", align=TextEntityAlignment.LEFT, rot=0.0):
    t = msp.add_text(s, dxfattribs={"layer": lay, "height": h, "rotation": rot})
    t.set_placement((x, y), align=align)
    return t

def line(x0, y0, x1, y1, lay="TABLA"):
    msp.add_line((x0, y0), (x1, y1), dxfattribs={"layer": lay})

def row(y, est, sup, ref=""):
    line(1.5, y - 0.30, 9.2, y - 0.30)
    txt(2.0, y, est, 0.24, "TEXTO")
    txt(7.6, y, f"{sup:7.1f}", 0.24, "TEXTO", TextEntityAlignment.RIGHT)
    if ref:
        txt(8.2, y, ref, 0.22, "TEXTO")
    return y - 0.55

def sect(y, name):
    line(1.5, y + 0.15, 9.2, y + 0.15, "CAJETIN")
    txt(2.0, y, name, 0.28, "TEXTO")
    return y - 0.55

# --- encabezado
txt(5.35, 20.6, "CUADRO DE SUPERFICIES · CASA BIFAMILIAR", 0.55, "TEXTO", TextEntityAlignment.MIDDLE_CENTER)
txt(5.35, 20.0, "PALMA DEL RÍO (CÓRDOBA) · SOLAR 200 m² · OCUPACIÓN 80 % (160 m²/planta)", 0.24, "TEXTO", TextEntityAlignment.MIDDLE_CENTER)
txt(2.0, 19.0, "ESTANCIA", 0.30, "CAJETIN")
txt(7.6, 19.0, "SUP. (m²)", 0.30, "CAJETIN", TextEntityAlignment.RIGHT)
txt(8.2, 19.0, "REF.", 0.30, "CAJETIN")
line(1.5, 18.55, 9.2, 18.55, "CAJETIN")

y = 17.95
y = sect(y, "PLANTA BAJA · VIVIENDA A (P-01)")
for est, sup, ref in [
    ("Salón-comedor", 37.0, "A1"), ("Cocina", 20.0, "A2"), ("Vestíbulo", 8.3, "A3"),
    ("Corredor", 9.9, "A4"), ("Baño", 7.0, "A5"), ("Baño suite", 7.0, "A6"),
    ("Dorm. principal", 14.0, "A7"), ("Distribuidor", 5.0, "A8"), ("Vestidor dorm3", 2.1, "A9"),
    ("Dorm. 2", 11.2, "A10"), ("Dorm. 3", 11.2, "A11"), ("Trastero", 7.4, "A12"),
    ("Cochera", 15.6, "A13")]:
    y = row(y, est, sup, ref)
y = row(y, "SUBTOTAL ÚTIL P-01", 155.7, "A")

y = y - 0.35
y = sect(y, "PLANTA ALTA · VIVIENDA B (P-02)")
for est, sup, ref in [
    ("Salón-comedor diáfano (inc. pasillo)", 50.0, "B1"), ("Cocina", 20.0, "B2"), ("Corredor", 9.9, "B3"),
    ("Baño", 7.0, "B4"), ("Baño suite", 7.0, "B5"), ("Dorm. principal", 14.0, "B6"),
    ("Distribuidor", 7.0, "B7"),
    ("Dorm. 2 (sobre cochera)", 23.0, "B8"), ("Dorm. 3", 11.2, "B9")]:
    y = row(y, est, sup, ref)
y = row(y, "SUBTOTAL ÚTIL P-02", 149.1, "B")

y = y - 0.35
y = sect(y, "EXTERIORES")
y = row(y, "Patio planta baja", 40.0)
y = row(y, "Porche cubierto", 13.0)
y = row(y, "Patio trasero planta alta", 11.2)
y = row(y, "Vacío patio (no construido)", 27.0)

y = y - 0.40
txt(2.0, y, "RESUMEN", 0.30, "CAJETIN"); y -= 0.55
txt(2.0, y, "Superficie construida P-01 (Vivienda A):  160,0 m²  (80 % del solar)", 0.26, "TEXTO"); y -= 0.48
txt(2.0, y, "Superficie construida P-02 (Vivienda B):  133,0 m²  (sin el vacío del patio)", 0.26, "TEXTO"); y -= 0.48
txt(2.0, y, "Superficie útil total (A + B):  304,8 m²", 0.26, "TEXTO"); y -= 0.48
txt(2.0, y, "Total construido:  293,0 m²", 0.26, "TEXTO"); y -= 0.75
txt(2.0, y, "PRESUPUESTO ORIENTATIVO (construcción, sin urbanización ni honorarios)", 0.30, "CAJETIN"); y -= 0.55
txt(2.0, y, "293 m² × 1.300 €/m² ≈ 381.000 €  (rango estimado 350.000 – 420.000 €)", 0.28, "TEXTO"); y -= 0.55
txt(2.0, y, "Incluye: obra gruesa, cubierta, carpintería exterior, instalaciones básicas y acabados estándar.", 0.20, "TEXTO")

# --- cajetín
msp.add_lwpolyline([(0.0, -1.2), (11.0, -1.2), (11.0, 0.0), (0.0, 0.0), (0.0, -1.2)],
                   close=True, dxfattribs={"layer": "CAJETIN"})
txt(0.2, -0.95, "P-05 · CUADRO DE SUPERFICIES · v1", 0.26, "CAJETIN")
txt(0.2, -0.30, "CASA BIFAMILIAR · PALMA DEL RÍO · SOLAR 200 m² · S1", 0.24, "CAJETIN")
txt(8.2, -0.95, "ESCALA —", 0.24, "CAJETIN")

doc.saveas(DXF)

fig = plt.figure(figsize=(9, 13), dpi=130)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_facecolor("white")
ctx = RenderContext(doc)
Frontend(ctx, MatplotlibBackend(ax)).draw_layout(msp)
ax.set_aspect("equal")
fig.savefig(PNG, facecolor="white")
plt.close(fig)
print("OK ->", DXF)
print("PNG ->", PNG)
