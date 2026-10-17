# -*- coding: utf-8 -*-
"""Genera un único PDF con todos los planos del proyecto, ordenados."""
import os
import ezdxf
from ezdxf.addons.drawing import RenderContext, Frontend
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "proyecto-completo.pdf")
JOBS = [
    ("paso-01-parcela.dxf",           "P-00 · SITUACIÓN Y PARCELA",           (10, 12)),
    ("paso-02-planta-baja.dxf",       "P-01 · PLANTA BAJA (VIVIENDA A)",      (9.5, 14)),
    ("paso-03-planta-alta.dxf",       "P-02 · PLANTA ALTA (VIVIENDA B)",      (9.5, 14)),
    ("paso-04-alzados-seccion.dxf",   "P-03/P-04 · ALZADOS Y SECCIÓN",        (10, 14)),
    ("paso-05-cuadro-superficies.dxf","P-05 · CUADRO DE SUPERFICIES",         (9, 13)),
]
with PdfPages(OUT) as pdf:
    for dxf, title, figsize in JOBS:
        doc = ezdxf.readfile(os.path.join(BASE, dxf))
        msp = doc.modelspace()
        fig = plt.figure(figsize=figsize, dpi=150)
        ax = fig.add_axes([0, 0, 1, 1])
        ax.set_facecolor("white")
        ctx = RenderContext(doc)
        Frontend(ctx, MatplotlibBackend(ax)).draw_layout(msp)
        ax.set_aspect("equal")
        pdf.savefig(fig)
        plt.close(fig)
        print("página ->", title)
print("PDF completo ->", OUT)
