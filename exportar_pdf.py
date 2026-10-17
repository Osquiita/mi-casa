# -*- coding: utf-8 -*-
"""Exporta los planos aprobados (DXF) a PDF vectorial para imprimir/plotter."""
import os
import ezdxf
from ezdxf.addons.drawing import RenderContext, Frontend
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
import matplotlib.pyplot as plt

BASE = os.path.dirname(os.path.abspath(__file__))
JOBS = [
    ("paso-01-parcela.dxf",          "plano-01-parcela.pdf",          (10, 12)),
    ("paso-02-planta-baja.dxf",      "plano-02-planta-baja.pdf",      (9.5, 14)),
    ("paso-03-planta-alta.dxf",      "plano-03-planta-alta.pdf",      (9.5, 14)),
    ("paso-04-alzados-seccion.dxf",  "plano-04-alzados-seccion.pdf",  (10, 14)),
    ("paso-05-cuadro-superficies.dxf","plano-05-cuadro-superficies.pdf",(9, 13)),
]
for dxf, pdf, figsize in JOBS:
    path = os.path.join(BASE, dxf)
    doc = ezdxf.readfile(path)
    msp = doc.modelspace()
    fig = plt.figure(figsize=figsize, dpi=150)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_facecolor("white")
    ctx = RenderContext(doc)
    Frontend(ctx, MatplotlibBackend(ax)).draw_layout(msp)
    ax.set_aspect("equal")
    fig.savefig(os.path.join(BASE, pdf), facecolor="white")
    plt.close(fig)
    print("PDF ->", pdf)
