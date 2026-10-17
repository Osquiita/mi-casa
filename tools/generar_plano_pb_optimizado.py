# -*- coding: utf-8 -*-
"""
Plano 2D Técnico - Ajuste de rótulos de baños
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import os

OUTPUT_DIR = r"C:\Users\Oscar Martinez\Desktop\mi-casa\entrega\planos_2d"
os.makedirs(OUTPUT_DIR, exist_ok=True)

C_WALL    = "#1C1E21"
C_LIVING  = "#FAF6EE"
C_KITCHEN = "#F4EFE6"
C_PORCH   = "#EAE5DA"
C_PATIO   = "#EAF2E8"
C_POOL    = "#BCE3F5"
C_POOL_IN = "#92D3F0"
C_BATH    = "#F0F5F7"
C_BED     = "#FAF8F5"
C_GARAGE  = "#EBECEE"
C_HALL    = "#F5F3EF"
C_WOOD    = "#C46D29"
C_GLASS   = "#3A86C8"
C_FURN    = "#D9D2C5"
C_BED_IN  = "#F5F2EA"
C_SOFA    = "#D2DCE0"
C_TEXT    = "#1C1E21"
C_MUTED   = "#6B7280"
C_STORAGE = "#E6DEC8"
C_COTA    = "#B91C1C"

def setup_ax():
    fig, ax = plt.subplots(figsize=(16, 23), dpi=220)
    ax.set_xlim(-1.8, 13.2)
    ax.set_ylim(-4.0, 19.5)
    ax.set_aspect('equal')
    ax.axis('off')
    return fig, ax

def add_rect(ax, x, y, w, h, fill_col, edge_col=None, lw=0.8, z=1):
    r = patches.Rectangle((x, y), w, h, facecolor=fill_col,
                           edgecolor=edge_col, linewidth=lw, zorder=z)
    ax.add_patch(r)
    return r

def add_wall(ax, x, y, w, h):
    r = patches.Rectangle((x, y), w, h, facecolor=C_WALL,
                           edgecolor=C_WALL, linewidth=0.5, zorder=10)
    ax.add_patch(r)

def add_window(ax, x, y, w, h, is_horiz=True):
    add_rect(ax, x, y, w, h, "#FFFFFF", edge_col=None, z=11)
    if is_horiz:
        ax.plot([x, x+w], [y+h/2, y+h/2], color=C_GLASS, lw=2.2, zorder=12)
        ax.plot([x, x+w], [y, y],         color=C_WALL,  lw=0.8, zorder=12)
        ax.plot([x, x+w], [y+h, y+h],     color=C_WALL,  lw=0.8, zorder=12)
    else:
        ax.plot([x+w/2, x+w/2], [y, y+h], color=C_GLASS, lw=2.2, zorder=12)
        ax.plot([x, x],         [y, y+h], color=C_WALL,  lw=0.8, zorder=12)
        ax.plot([x+w, x+w],     [y, y+h], color=C_WALL,  lw=0.8, zorder=12)

def add_door(ax, x, y, r, a_start, a_end):
    arc = patches.Arc((x, y), 2*r, 2*r, angle=0,
                       theta1=min(a_start, a_end),
                       theta2=max(a_start, a_end),
                       color=C_WOOD, linewidth=1.2, linestyle='--', zorder=8)
    ax.add_patch(arc)
    rad = a_start * np.pi / 180.0
    ax.plot([x, x + r*np.cos(rad)], [y, y + r*np.sin(rad)],
            color=C_WOOD, linewidth=1.8, zorder=9)

def add_bed(ax, x, y, w, h):
    add_rect(ax, x, y, w, h, C_BED_IN, edge_col=C_FURN, lw=1.0, z=5)
    add_rect(ax, x, y+h-0.15, w, 0.15, C_FURN, edge_col=C_FURN, z=6)
    pw = (w - 0.25) / 2
    add_rect(ax, x+0.08, y+h-0.45, pw, 0.25, "#FFF", edge_col=C_FURN, lw=0.8, z=6)
    add_rect(ax, x+w-0.08-pw, y+h-0.45, pw, 0.25, "#FFF", edge_col=C_FURN, lw=0.8, z=6)

def add_cota_interior_h(ax, x1, x2, y, text, offset=0.15):
    ax.annotate('', xy=(x1, y), xytext=(x2, y),
                arrowprops=dict(arrowstyle='<->', color=C_COTA, lw=0.8), zorder=15)
    ax.text((x1+x2)/2, y+offset, text, ha='center', va='bottom',
            fontsize=7.5, color=C_COTA, weight='bold', zorder=16,
            bbox=dict(boxstyle='square,pad=0.1', facecolor='#FFFFFF', edgecolor='none', alpha=0.85))

def add_cota_interior_v(ax, y1, y2, x, text, offset=0.15):
    ax.annotate('', xy=(x, y1), xytext=(x, y2),
                arrowprops=dict(arrowstyle='<->', color=C_COTA, lw=0.8), zorder=15)
    ax.text(x+offset, (y1+y2)/2, text, ha='left', va='center',
            fontsize=7.5, color=C_COTA, weight='bold', rotation=90, zorder=16,
            bbox=dict(boxstyle='square,pad=0.1', facecolor='#FFFFFF', edgecolor='none', alpha=0.85))

def generar_planta_baja_cotas():
    fig, ax = setup_ax()

    # 1. SUELOS
    add_rect(ax, 0.00, 0.00, 1.20, 2.40, C_HALL)
    add_rect(ax, 0.00, 2.40, 6.40, 5.00, C_LIVING)
    add_rect(ax, 1.20, 0.00, 5.20, 2.40, C_LIVING)
    add_rect(ax, 6.40, 0.00, 4.00, 5.00, C_KITCHEN)
    add_rect(ax, 10.40, 0.00, 1.00, 5.00, C_GARAGE)
    add_rect(ax, 6.40, 5.00, 5.00, 2.40, C_PORCH)
    add_rect(ax, 6.40, 7.40, 5.00, 5.60, C_PATIO)

    # Piscina
    add_rect(ax, 7.30, 8.20, 2.50, 3.80, C_POOL, edge_col="#54A5C9", lw=1.5, z=3)
    add_rect(ax, 7.45, 8.35, 2.20, 3.50, C_POOL_IN, edge_col="#76C4E8", lw=0.8, z=4)
    for sy in [8.35, 8.75, 9.15]:
        ax.plot([7.45, 9.65], [sy, sy], color="#54A5C9", lw=0.8, zorder=5)

    # Pasillo Noche y Rellano
    add_rect(ax, 0.00, 7.40, 1.20, 6.10, C_HALL)
    add_rect(ax, 1.20, 12.55, 3.10, 0.95, C_HALL)

    # Baños Cuadrados
    add_rect(ax, 1.20, 7.40, 2.60, 2.40, C_BATH)
    add_rect(ax, 3.80, 7.40, 2.60, 2.40, C_BATH)

    # Master Suite
    add_rect(ax, 1.20, 9.80, 3.10, 2.75, C_BED)
    add_rect(ax, 4.30, 9.80, 2.10, 3.65, C_BED)

    # Dormitorios 2 y 3
    add_rect(ax, 0.00, 13.50, 3.20, 4.10, C_BED)
    add_rect(ax, 3.20, 13.50, 3.20, 4.10, C_BED)

    # Gran Cochera
    add_rect(ax, 6.40, 13.00, 5.00, 4.60, C_GARAGE)

    # 2. MUROS EXTERIORES Y MEDIANERAS
    add_wall(ax, -0.15, -0.15, 0.30, 17.90)
    add_wall(ax, 11.25, -0.15, 0.30, 17.90)

    # Fachada Sur
    add_wall(ax, -0.15, -0.15, 0.45, 0.30)
    add_wall(ax, 1.20, -0.15, 1.40, 0.30)
    add_wall(ax, 4.40, -0.15, 0.40, 0.30)
    add_wall(ax, 6.00, -0.15, 0.90, 0.30)
    add_wall(ax, 8.10, -0.15, 0.80, 0.30)
    add_wall(ax, 9.90, -0.15, 0.50, 0.30)

    # Fachada Norte
    add_wall(ax, -0.15, 17.45, 0.95, 0.30)
    add_wall(ax, 2.40, 17.45, 1.20, 0.30)
    add_wall(ax, 5.20, 17.45, 1.20, 0.30)

    # 3. TABIQUERÍA INTERIOR
    add_wall(ax, 1.15, 0.00, 0.10, 1.20)
    add_wall(ax, 6.35, 0.00, 0.10, 0.80)
    add_wall(ax, 6.35, 4.20, 0.10, 0.80)
    add_wall(ax, 10.35, 0.00, 0.10, 5.00)

    # Salón ↔ Baños
    add_wall(ax, 1.15, 7.35, 5.25, 0.10)

    # Muro Técnico Central Baños
    add_wall(ax, 3.75, 7.35, 0.15, 2.45)
    add_rect(ax, 3.75, 8.30, 0.15, 0.60, "#D97706", edge_col=C_WALL, lw=0.8, z=13)

    # Muro Patio
    add_wall(ax, 6.30, 7.35, 0.20, 5.65)

    # Baños ↔ Suite
    add_wall(ax, 1.15, 9.75, 2.65, 0.10)
    add_wall(ax, 4.70, 9.75, 1.70, 0.10)

    # Pasillo ↔ Suite
    add_wall(ax, 1.15, 9.75, 0.10, 0.25)
    add_wall(ax, 1.15, 10.85, 0.10, 1.70)

    # Suite ↔ Rellano Norte
    add_wall(ax, 1.15, 12.45, 3.15, 0.10)
    add_wall(ax, 4.25, 12.45, 0.10, 1.10)

    # Distribuidor ↔ Dorms 2 y 3
    add_wall(ax, -0.15, 13.45, 0.95, 0.10)
    add_wall(ax, 1.65, 13.45, 1.55, 0.10)
    add_wall(ax, 4.25, 13.45, 2.15, 0.10)

    # Separación Dorm 2 - Dorm 3
    add_wall(ax, 3.15, 13.45, 0.10, 4.15)

    # Muro Cochera
    add_wall(ax, 6.30, 13.00, 0.20, 4.60)

    # Pilares Porche
    add_wall(ax, 7.00, 7.25, 0.25, 0.25)
    add_wall(ax, 9.50, 7.25, 0.25, 0.25)

    # 4. VENTANAS Y PUERTAS
    add_window(ax, 2.60, -0.05, 1.80, 0.10)
    add_window(ax, 4.80, -0.05, 1.20, 0.10)
    add_window(ax, 6.90, -0.05, 1.20, 0.10)
    add_window(ax, 8.90, -0.05, 1.00, 0.10)

    add_window(ax, 6.40, 5.00, 0.10, 2.40, False)
    add_window(ax, 6.40, 7.60, 0.10, 0.80, False)
    add_window(ax, 6.40, 8.75, 0.10, 0.80, False)
    add_window(ax, 6.40, 10.30, 0.10, 2.60, False)

    add_window(ax, 0.80, 17.55, 1.60, 0.10)
    add_window(ax, 3.60, 17.55, 1.60, 0.10)

    add_rect(ax, 6.40, 17.52, 4.85, 0.16, "#A84B24", edge_col="#6E2E13", lw=1.2, z=12)

    # Puertas
    add_door(ax, 0.30, 0.00, 0.90, 0, 90)
    add_door(ax, 10.40, 0.00, 0.90, 0, 90)
    add_door(ax, 0.20, 7.35, 0.85, 0, 90)
    add_door(ax, 1.20, 7.45, 0.80, 0, 90)
    add_door(ax, 3.90, 9.80, 0.80, -90, 0)
    add_door(ax, 1.20, 10.00, 0.85, 0, 90)
    add_door(ax, 0.80, 13.55, 0.85, 0, 90)
    add_door(ax, 3.40, 13.55, 0.85, 0, 90)
    add_door(ax, 6.40, 13.20, 0.85, -90, 0)

    # 5. MOBILIARIO
    add_rect(ax, 0.15, 2.40, 0.70, 3.60, C_STORAGE, edge_col=C_WOOD, lw=1.2, z=5)
    for my in [3.30, 4.20, 5.10]:
        ax.plot([0.15, 0.85], [my, my], color=C_WOOD, lw=0.8, zorder=6)

    add_rect(ax, 1.80, 2.60, 2.80, 1.10, C_SOFA, edge_col="#A3B8C0", lw=1.0, z=5)
    add_rect(ax, 1.80, 1.00, 2.40, 1.00, C_FURN, edge_col="#A89E8C", lw=1.0, z=5)
    for cy in [0.75, 2.25]:
        for cx in [2.00, 2.70, 3.40, 3.90]:
            add_rect(ax, cx, cy, 0.40, 0.35, "#ECE7DE", edge_col="#A89E8C", lw=0.8, z=5)
    add_rect(ax, 2.40, 6.80, 2.40, 0.45, "#DDD6C9", edge_col="#A89E8C", lw=1.0, z=5)

    add_rect(ax, 7.20, 1.60, 2.40, 1.10, "#FFFFFF", edge_col="#A89E8C", lw=1.2, z=5)
    add_rect(ax, 6.50, 0.15, 3.80, 0.65, "#EAE5DA", edge_col="#A89E8C", lw=0.8, z=5)

    for st in range(16):
        sy = st * (5.0 / 16.0)
        ax.plot([10.40, 11.40], [sy, sy], color="#9CA3AF", lw=0.8, zorder=5)

    # Baños
    add_rect(ax, 1.30, 7.50, 2.35, 0.75, "#FFFFFF", edge_col=C_GLASS, lw=1.0, z=5)
    add_rect(ax, 1.30, 9.20, 1.10, 0.40, "#FFFFFF", edge_col=C_FURN, lw=1.0, z=5)
    circ1 = patches.Circle((1.85, 9.40), 0.14, facecolor=C_BATH, edgecolor=C_FURN, lw=0.8, zorder=6)
    ax.add_patch(circ1)
    add_rect(ax, 3.20, 9.15, 0.50, 0.45, "#FFFFFF", edge_col=C_FURN, lw=1.0, z=5)

    add_rect(ax, 3.95, 7.50, 2.35, 0.75, "#FFFFFF", edge_col=C_GLASS, lw=1.0, z=5)
    add_rect(ax, 3.90, 9.15, 0.50, 0.45, "#FFFFFF", edge_col=C_FURN, lw=1.0, z=5)
    add_rect(ax, 5.10, 9.20, 1.15, 0.40, "#FFFFFF", edge_col=C_FURN, lw=1.0, z=5)
    circ2 = patches.Circle((5.67, 9.40), 0.14, facecolor=C_BATH, edgecolor=C_FURN, lw=0.8, zorder=6)
    ax.add_patch(circ2)

    # Master Suite
    add_bed(ax, 1.90, 10.15, 2.00, 2.10)
    add_rect(ax, 4.40, 10.00, 0.65, 3.20, "#EAE5DA", edge_col=C_FURN, lw=1.0, z=5)
    add_rect(ax, 5.50, 12.80, 0.80, 0.50, "#EAE5DA", edge_col=C_FURN, lw=0.8, z=5)

    # Dormitorios 2 y 3
    add_bed(ax, 0.50, 14.80, 1.60, 2.00)
    add_rect(ax, 2.35, 14.80, 0.65, 2.20, "#EAE5DA", edge_col=C_FURN, lw=1.0, z=5)
    add_bed(ax, 3.70, 14.80, 1.60, 2.00)
    add_rect(ax, 5.55, 14.80, 0.65, 2.20, "#EAE5DA", edge_col=C_FURN, lw=1.0, z=5)

    # Cochera
    add_rect(ax, 6.80, 14.00, 3.00, 3.20, "#D2DCE0", edge_col="#8B9CA5", lw=1.0, z=4)
    add_rect(ax, 10.50, 13.20, 0.70, 4.10, "#D9D2C5", edge_col=C_WOOD, lw=1.0, z=5)

    # 6. COTAS INTERIORES EXACTAS
    # Salón
    add_cota_interior_h(ax, 0.15, 6.35, 6.40, "6,20 m libres", offset=0.15)
    add_cota_interior_v(ax, 0.15, 7.35, 5.90, "7,20 m libres", offset=0.15)
    add_cota_interior_v(ax, 2.40, 6.00, 0.95, "3,60 m armarios", offset=0.10)

    # Cocina
    add_cota_interior_h(ax, 6.45, 10.35, 4.60, "3,90 m libres", offset=0.15)
    add_cota_interior_v(ax, 0.15, 4.95, 10.00, "4,80 m libres", offset=0.15)

    # Baños
    add_cota_interior_h(ax, 1.25, 3.72, 8.80, "2,47 m", offset=0.10)
    add_cota_interior_v(ax, 7.45, 9.75, 1.50, "2,30 m", offset=0.10)
    add_cota_interior_h(ax, 3.88, 6.30, 8.80, "2,42 m", offset=0.10)
    add_cota_interior_v(ax, 7.45, 9.75, 6.10, "2,30 m", offset=0.10)

    # Suite
    add_cota_interior_h(ax, 1.25, 4.25, 12.10, "3,00 m", offset=0.10)
    add_cota_interior_v(ax, 9.85, 12.45, 4.05, "2,60 m", offset=0.10)
    add_cota_interior_h(ax, 4.35, 6.30, 13.10, "1,95 m", offset=0.10)
    add_cota_interior_v(ax, 9.85, 13.45, 6.10, "3,60 m vestidor", offset=0.10)

    # Dorms 2 y 3
    add_cota_interior_h(ax, 0.15, 3.15, 17.10, "3,00 m libres", offset=0.15)
    add_cota_interior_v(ax, 13.55, 17.45, 0.35, "3,90 m libres", offset=0.15)
    add_cota_interior_h(ax, 3.25, 6.30, 17.10, "3,05 m libres", offset=0.15)
    add_cota_interior_v(ax, 13.55, 17.45, 3.45, "3,90 m libres", offset=0.15)

    # Cochera
    add_cota_interior_h(ax, 6.50, 11.25, 13.60, "4,75 m libres", offset=0.15)
    add_cota_interior_v(ax, 13.00, 17.45, 6.70, "4,45 m libres", offset=0.15)

    # Patio y Piscina
    add_cota_interior_h(ax, 6.50, 11.25, 7.70, "4,75 m libres patio", offset=0.15)
    add_cota_interior_v(ax, 7.45, 13.00, 11.00, "5,55 m libres patio", offset=0.15)
    add_cota_interior_h(ax, 7.30, 9.80, 11.70, "2,50 m piscina", offset=0.10)
    add_cota_interior_v(ax, 8.20, 12.00, 7.55, "3,80 m piscina", offset=0.10)

    # 7. RÓTULOS DESPEJADOS
    ax.text(3.60, 4.60, "SALÓN - COMEDOR\n38,5 m² útiles",
            ha='center', va='center', fontsize=10, weight='bold', color=C_TEXT)

    ax.text(8.40, 3.60, "COCINA CON ISLA\n18,7 m² útiles",
            ha='center', va='center', fontsize=9.5, weight='bold', color=C_TEXT)

    ax.text(8.90, 6.20, "PORCHE CUBIERTO\n11,4 m² útiles",
            ha='center', va='center', fontsize=8.5, weight='bold', color=C_TEXT)

    # Rótulos baños en zona de ducha / paso
    ax.text(2.55, 7.85, "BAÑO COMÚN\n5,7 m² útiles",
            ha='center', va='center', fontsize=7.5, weight='bold', color="#0F4C81", zorder=7)

    ax.text(5.10, 7.85, "BAÑO EN SUITE\n5,6 m² útiles",
            ha='center', va='center', fontsize=7.5, weight='bold', color="#0F4C81", zorder=7)

    ax.text(2.60, 12.85, "MASTER SUITE (14,8 m² útiles)\nTotal con Baño: 20,4 m²",
            ha='center', va='center', fontsize=8, weight='bold', color=C_TEXT)

    ax.text(1.65, 14.10, "DORMITORIO 2\n11,7 m² útiles",
            ha='center', va='center', fontsize=8.5, weight='bold', color=C_TEXT)

    ax.text(4.80, 14.10, "DORMITORIO 3\n11,9 m² útiles",
            ha='center', va='center', fontsize=8.5, weight='bold', color=C_TEXT)

    ax.text(8.90, 15.60, "GRAN COCHERA\n21,1 m² útiles",
            ha='center', va='center', fontsize=8.5, weight='bold', color=C_TEXT)

    ax.text(0.60, 10.20, "PASILLO NOCHE (1,20 m libre) · 7,3 m² útiles",
            ha='center', va='center', fontsize=6.5, color=C_MUTED, rotation=90)

    # 8. CAJETÍN
    add_rect(ax, 0.00, -3.60, 11.40, 1.30, "#FFFFFF", edge_col=C_WALL, lw=1.5, z=20)
    ax.text(0.30, -2.70, "PROYECTO RESIDENCIAL · PALMA DEL RIO (CÓRDOBA)",
            fontsize=11, weight='bold', color=C_TEXT, zorder=21)
    ax.text(0.30, -3.20, "LÁMINA 2D-01 · PLANTA BAJA CON COTAS INTERIORES ÚTILES Y SUPERFICIES REALES",
            fontsize=8.5, color=C_MUTED, zorder=21)
    ax.text(11.10, -2.95, "ESCALA 1:50 | SUP. ÚTIL CERRADA: 136,7 m² | EXTERIOR: 37,8 m²",
            ha='right', va='center', fontsize=9.5, weight='bold', color=C_TEXT, zorder=21)

    out_file = os.path.join(OUTPUT_DIR, "01_plano_2d_planta_baja.png")
    plt.savefig(out_file, bbox_inches='tight', dpi=220)
    plt.close(fig)
    print(f"PLANO PB COTAS INTERIORES AJUSTADO OK: {out_file}")

generar_planta_baja_cotas()
