# -*- coding: utf-8 -*-
"""PASO 01 - PARCELA (revisado): solar, calles, medianeras, patio optimizado 5x8,
cotas, cajetin, leyenda, norte y barra de escala."""
import os
import ezdxf
from ezdxf.enums import TextEntityAlignment
from ezdxf.addons.drawing import RenderContext, Frontend
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
import matplotlib.pyplot as plt

from plan_data import (X0, Y0, X1, Y1, PX0, PY0, PX1, PY1, FRONT_D, REAR_D, LEFT_W)

BASE = os.path.dirname(os.path.abspath(__file__))
DXF = os.path.join(BASE, "paso-01-parcela.dxf")
PNG = os.path.join(BASE, "preview-01-parcela.png")

# ------------------------------------------------------------------ capas
doc = ezdxf.new("R2010", setup=True)
doc.units = ezdxf.units.M
msp = doc.modelspace()

def layer(name, color, lw100, lt="CONTINUOUS"):
    doc.layers.add(name, color=color, linetype=lt)
    doc.layers.get(name).dxf.lineweight = lw100

layer("PARCELA", 7, 60)
layer("HUELLA", 7, 25, "DASHED")
layer("PATIO", 3, 30)
layer("VIARIO", 8, 25)
layer("LINDE", 8, 25, "DASHED2")
layer("COTAS", 5, 18)
layer("NORTE", 5, 25)
layer("ESCALA", 5, 18)
layer("TEXTO", 7, 18)
layer("CAJETIN", 7, 35)

# ------------------------------------------------------------------ helpers
def txt(x, y, s, h=0.35, lay="TEXTO", rot=0.0, align=TextEntityAlignment.LEFT):
    t = msp.add_text(s, dxfattribs={"layer": lay, "height": h, "rotation": rot})
    t.set_placement((x, y), align=align)
    return t

def poly(pts, lay, close=True):
    msp.add_lwpolyline(pts, close=close, dxfattribs={"layer": lay})

def solid(pts, lay):
    h = msp.add_hatch(dxfattribs={"layer": lay})
    h.set_solid_fill()
    h.paths.add_polyline_path(pts, is_closed=True)

def cota_h(x1, x2, y, text, off=0.45):
    """Cota horizontal dibujada (extensiones + linea + flechas + texto)."""
    msp.add_line((x1, y), (x1, y - 0.35), dxfattribs={"layer": "COTAS"})
    msp.add_line((x2, y), (x2, y - 0.35), dxfattribs={"layer": "COTAS"})
    msp.add_line((x1, y), (x2, y), dxfattribs={"layer": "COTAS"})
    msp.add_line((x1, y), (x1 + 0.18, y - 0.09), dxfattribs={"layer": "COTAS"})
    msp.add_line((x1, y), (x1 + 0.18, y + 0.09), dxfattribs={"layer": "COTAS"})
    msp.add_line((x2, y), (x2 - 0.18, y - 0.09), dxfattribs={"layer": "COTAS"})
    msp.add_line((x2, y), (x2 - 0.18, y + 0.09), dxfattribs={"layer": "COTAS"})
    txt((x1 + x2) / 2, y + off, text, 0.38, "COTAS", align=TextEntityAlignment.MIDDLE_CENTER)

def cota_v(y1, y2, x, text, off=0.45):
    msp.add_line((x, y1), (x - 0.35, y1), dxfattribs={"layer": "COTAS"})
    msp.add_line((x, y2), (x - 0.35, y2), dxfattribs={"layer": "COTAS"})
    msp.add_line((x, y1), (x, y2), dxfattribs={"layer": "COTAS"})
    msp.add_line((x, y1), (x - 0.09, y1 + 0.18), dxfattribs={"layer": "COTAS"})
    msp.add_line((x, y1), (x + 0.09, y1 + 0.18), dxfattribs={"layer": "COTAS"})
    msp.add_line((x, y2), (x - 0.09, y2 - 0.18), dxfattribs={"layer": "COTAS"})
    msp.add_line((x, y2), (x + 0.09, y2 - 0.18), dxfattribs={"layer": "COTAS"})
    txt(x - off, (y1 + y2) / 2, text, 0.38, "COTAS", 90.0, TextEntityAlignment.MIDDLE_CENTER)

def cajetin(xa, ya, xb, yb):
    poly([(xa, ya), (xb, ya), (xb, yb), (xa, yb), (xa, ya)], "CAJETIN")
    yy = ya + 1.0
    msp.add_line((xa, yy), (xb, yy), dxfattribs={"layer": "CAJETIN"})
    msp.add_line((xa, yb - 0.55), (xb, yb - 0.55), dxfattribs={"layer": "CAJETIN"})
    msp.add_line((xb - 4.0, ya), (xb - 4.0, yb), dxfattribs={"layer": "CAJETIN"})
    msp.add_line((xb - 2.0, yy), (xb - 2.0, yb), dxfattribs={"layer": "CAJETIN"})
    txt(xa + 0.2, yb - 0.35, "PROYECTO: VIVIENDA UNIFAMILIAR BIFAMILIAR", 0.32, "CAJETIN")
    txt(xa + 0.2, yy + 0.3, "PALMA DEL RÍO · CÓRDOBA · SOLAR 200 m² · ZONA S1", 0.28, "CAJETIN")
    txt(xa + 0.2, yy + 0.05, "PLANO P-00 · SITUACIÓN E IMPLANTACIÓN", 0.28, "CAJETIN")
    txt(xb - 3.9, yy + 0.3, "ESCALA 1:100", 0.28, "CAJETIN")
    txt(xb - 1.9, yy + 0.3, "M", 0.28, "CAJETIN")

def leyenda(xa, ya, xb, yb):
    poly([(xa, ya), (xb, ya), (xb, yb), (xa, yb), (xa, ya)], "CAJETIN")
    txt(xa + 0.2, yb - 0.3, "LEYENDA", 0.3, "CAJETIN")
    items = [
        ("PARCELA (límite solar, LW 0,60)", "PARCELA", 0),
        ("PATIO 40 m² (5 x 8) · lindero derecho", "PATIO", 1),
        ("HUELLA 80% = 160 m²/planta", "HUELLA", 2),
        ("VIARIO (calles)", "VIARIO", 3),
        ("MEDIANERA (linderos vecinos)", "LINDE", 4),
        ("COTAS / NORTE / ESCALA", "COTAS", 5),
    ]
    for i, (label, lay, _) in enumerate(items):
        y = yb - 0.75 - i * 0.5
        msp.add_line((xa + 0.2, y), (xa + 1.0, y), dxfattribs={"layer": lay})
        txt(xa + 1.15, y, label, 0.26, "CAJETIN")

# ------------------------------------------------------------------ dibujo
# calles + medianeras
solid([(X0 - 2.5, Y0 - 3.2), (X1 + 0.5, Y0 - 3.2), (X1 + 0.5, Y0), (X0 - 2.5, Y0)], "VIARIO")
solid([(X0 - 2.5, Y1), (X1 + 0.5, Y1), (X1 + 0.5, Y1 + 3.2), (X0 - 2.5, Y1 + 3.2)], "VIARIO")
solid([(X1, Y0), (X1 + 2.0, Y0), (X1 + 2.0, Y1), (X1, Y1)], "LINDE")
solid([(X0 - 2.5, Y0), (X0, Y0), (X0, Y1), (X0 - 2.5, Y1)], "LINDE")

# limite solar
poly([(X0, Y0), (X1, Y0), (X1, Y1), (X0, Y1)], "PARCELA")

# patio (5 x 8)
poly([(PX0, PY0), (PX1, PY0), (PX1, PY1), (PX0, PY1)], "PATIO")
ph = msp.add_hatch(dxfattribs={"layer": "PATIO"})
ph.set_pattern_fill("NET3", scale=0.12)
ph.paths.add_polyline_path([(PX0, PY0), (PX1, PY0), (PX1, PY1), (PX0, PY1)], is_closed=True)

# huella edificable en L
poly([(X0, Y0), (X1, Y0), (X1, PY0), (PX0, PY0), (PX0, PY1), (X1, PY1), (X1, Y1), (X0, Y1)], "HUELLA")

# cotas
cota_h(X0, X1, -0.5, "11,40 m")
cota_v(Y0, Y1, -0.5, "17,60 m")
cota_h(PX0, PX1, PY0 - 0.5, "5,00 m")
cota_v(PY0, PY1, PX1 + 0.5, "8,00 m")

# textos
txt((X0 + X1) / 2, Y0 - 2.7, "C/ MORENO TORROBA  (FACHADA PRINCIPAL · 11,40 m)", 0.42, "TEXTO", align=TextEntityAlignment.MIDDLE_CENTER)
txt((X0 + X1) / 2, Y1 + 2.7, "C/ TRASERA  (ACCESO COCHERA)", 0.42, "TEXTO", align=TextEntityAlignment.MIDDLE_CENTER)
txt(X1 + 0.35, (Y0 + Y1) / 2, "MEDIANERA", 0.35, "TEXTO", 90.0, TextEntityAlignment.MIDDLE_CENTER)
txt(X0 - 0.5, (Y0 + Y1) / 2, "MEDIANERA", 0.35, "TEXTO", 90.0, TextEntityAlignment.MIDDLE_CENTER)
txt((PX0 + PX1) / 2, (PY0 + PY1) / 2 + 0.55, "PATIO 5,00 x 8,00 m", 0.42, "PATIO", align=TextEntityAlignment.MIDDLE_CENTER)
txt((PX0 + PX1) / 2, (PY0 + PY1) / 2 - 0.6, "40 m²", 0.42, "PATIO", align=TextEntityAlignment.MIDDLE_CENTER)
txt((X0 + X1) / 2, -0.32, "SOLAR 200 m² · SIN RETRANQUEOS · OCUPACIÓN 80% = ~160 m²/planta", 0.38, "TEXTO", align=TextEntityAlignment.MIDDLE_CENTER)
txt(X0 + 0.3, Y0 + 0.3, "ENTRE MEDIANERAS · FACHADA A DOS CALLES", 0.32, "TEXTO")
txt(X0 + 0.3, Y0 + 0.72, "ZONA S1 · EDIFICACIÓN A RAS DE CALLE", 0.32, "TEXTO")

# notas de diseno
nota_x, nota_y = PX0 + 0.3, PY0 + 0.3
txt(nota_x, nota_y, "PATIO 40 m² (dimensión optimizada):", 0.3, "TEXTO")
txt(nota_x, nota_y - 0.42, "· ancho 5,00 m → frente de día de 10,00 m", 0.28, "TEXTO")
txt(nota_x, nota_y - 0.78, "· fondo 8,00 m → bandas de 5,00 / 4,60 m", 0.28, "TEXTO")
txt(nota_x, nota_y - 1.14, "· luz + ventilación cruzada a dorm. y cocina", 0.28, "TEXTO")

# norte
nx, ny = X1 - 1.0, Y1 + 2.3
msp.add_circle((nx, ny), 0.75, dxfattribs={"layer": "NORTE"})
msp.add_line((nx, ny), (nx, ny + 0.62), dxfattribs={"layer": "NORTE"})
txt(nx, ny + 0.95, "N", 0.5, "NORTE", align=TextEntityAlignment.MIDDLE_CENTER)

# barra escala grafica
ex, ey = 0.0, -0.9
for i in range(6):
    seg = (i / 5.0) * 5.0
    msp.add_line((ex + seg, ey), (ex + seg, ey + 0.28), dxfattribs={"layer": "ESCALA"})
    msp.add_line((ex + seg, ey), (ex + seg + 1.0, ey), dxfattribs={"layer": "ESCALA"})
    txt(ex + seg, ey - 0.35, str(i), 0.3, "ESCALA", align=TextEntityAlignment.MIDDLE_CENTER)
txt(ex + 2.5, ey - 0.65, "ESCALA GRÁFICA (m)", 0.3, "ESCALA", align=TextEntityAlignment.MIDDLE_CENTER)

# cajetin + leyenda
cajetin(0.0, -4.6, 11.4, -3.0)
leyenda(-2.6, -4.6, 0.0, -2.6)

doc.saveas(DXF)

# ------------------------------------------------------------------ preview
fig = plt.figure(figsize=(9, 12.5), dpi=130)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_facecolor("white")
ctx = RenderContext(doc)
backend = MatplotlibBackend(ax)
Frontend(ctx, backend).draw_layout(msp)
ax.set_aspect("equal")
fig.savefig(PNG, facecolor="white")
plt.close(fig)
print("OK ->", DXF)
print("PNG ->", PNG)
