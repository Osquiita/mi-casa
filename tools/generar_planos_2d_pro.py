# -*- coding: utf-8 -*-
"""Generador de Planos Arquitectónicos 2D de Calidad Publicación / Estudio.
Ajustado para máxima legibilidad, sin ningún solapamiento, con puertas abatibles y cotas nítidas.
"""
import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Arc

OUT_DIR = r"C:\Users\Oscar Martinez\Desktop\mi-casa\entrega\planos_2d"
os.makedirs(OUT_DIR, exist_ok=True)

W, D = 11.40, 17.60

def draw_door_swing(ax, x0, y0, r, theta1, theta2, color="#B85D1A", lw=1.2):
    arc = Arc((x0, y0), 2*r, 2*r, angle=0, theta1=theta1, theta2=theta2, color=color, lw=lw, ls="--", zorder=8)
    ax.add_patch(arc)

def draw_interior_door(ax, x0, y0, w, orientation="h", side=1):
    """Dibuja puerta interior con hoja y arco."""
    if orientation == "h":
        ax.plot([x0, x0 + w*0.7], [y0, y0 + side*w*0.7], color="#3A4048", lw=1.5, zorder=8)
        t1, t2 = (0, 90) if side > 0 else (-90, 0)
        draw_door_swing(ax, x0, y0, w, t1, t2, color="#8C8275")
    else:
        ax.plot([x0, x0 + side*w*0.7], [y0, y0 + w*0.7], color="#3A4048", lw=1.5, zorder=8)
        t1, t2 = (0, 90) if side > 0 else (90, 180)
        draw_door_swing(ax, x0, y0, w, t1, t2, color="#8C8275")

def draw_furniture_bed(ax, x, y, w, d):
    # Base
    ax.add_patch(patches.Rectangle((x, y), w, d, facecolor="#F5F2EA", edgecolor="#8C8275", lw=1.0, zorder=2))
    # Cabecero
    ax.add_patch(patches.Rectangle((x, y + d - 0.12), w, 0.12, facecolor="#A89F91", edgecolor="#6E6659", lw=1.0, zorder=3))
    # Almohadas
    if w >= 1.4:
        ax.add_patch(patches.Rectangle((x + 0.1, y + d - 0.50), (w-0.3)/2, 0.32, facecolor="#FFFFFF", edgecolor="#B0A89C", lw=0.8, zorder=3))
        ax.add_patch(patches.Rectangle((x + 0.2 + (w-0.3)/2, y + d - 0.50), (w-0.3)/2, 0.32, facecolor="#FFFFFF", edgecolor="#B0A89C", lw=0.8, zorder=3))
    else:
        ax.add_patch(patches.Rectangle((x + 0.1, y + d - 0.50), w - 0.2, 0.32, facecolor="#FFFFFF", edgecolor="#B0A89C", lw=0.8, zorder=3))

def draw_furniture_table(ax, x, y, w, d, chairs=3):
    ax.add_patch(patches.Rectangle((x, y), w, d, facecolor="#E6DEC9", edgecolor="#7A6F5D", lw=1.2, zorder=2))
    for i in range(chairs):
        cx = x + (i + 0.5) * (w / chairs)
        ax.add_patch(patches.Rectangle((cx - 0.18, y + d + 0.04), 0.36, 0.30, facecolor="#D4CABA", edgecolor="#6E6659", lw=0.8, zorder=2))
        ax.add_patch(patches.Rectangle((cx - 0.18, y - 0.34), 0.36, 0.30, facecolor="#D4CABA", edgecolor="#6E6659", lw=0.8, zorder=2))

def draw_furniture_sofa(ax, x, y, w, d):
    ax.add_patch(patches.Rectangle((x, y), w, d, facecolor="#D2DCE0", edgecolor="#5C666B", lw=1.2, zorder=2))
    ax.add_patch(patches.Rectangle((x, y), w, 0.20, facecolor="#A3B2B8", edgecolor="#5C666B", lw=1.0, zorder=3))
    ax.add_patch(patches.Rectangle((x, y), 0.18, d, facecolor="#A3B2B8", edgecolor="#5C666B", lw=1.0, zorder=3))
    ax.add_patch(patches.Rectangle((x + w - 0.18, y), 0.18, d, facecolor="#A3B2B8", edgecolor="#5C666B", lw=1.0, zorder=3))

def draw_bathroom_fixtures(ax, x_room, y_room, w_room, d_room):
    # Ducha
    ax.add_patch(patches.Rectangle((x_room + w_room - 0.95, y_room + 0.1), 0.85, d_room - 0.2, facecolor="#EBF4F6", edgecolor="#7BA3AD", lw=1.0, zorder=2))
    ax.plot([x_room + w_room - 0.95, x_room + w_room - 0.10], [y_room + 0.1, y_room + d_room - 0.1], color="#7BA3AD", lw=0.6, zorder=2)
    # Lavabo mueble
    ax.add_patch(patches.Rectangle((x_room + 0.2, y_room + 0.1), 1.2, 0.45, facecolor="#FFFFFF", edgecolor="#7BA3AD", lw=1.0, zorder=2))
    ax.text(x_room + 0.8, y_room + 0.32, "LAVABO", ha="center", va="center", fontsize=6, color="#487B8A")
    # WC
    ax.add_patch(patches.Rectangle((x_room + 2.0, y_room + 0.1), 0.40, 0.55, facecolor="#FFFFFF", edgecolor="#7BA3AD", lw=1.0, zorder=2))
    ax.text(x_room + 2.2, y_room + 0.37, "WC", ha="center", va="center", fontsize=6, color="#487B8A")

# ==============================================================================
# 1. PLANTA BAJA (VIVIENDA A)
# ==============================================================================
def generar_plano_pb():
    fig, ax = plt.subplots(figsize=(12, 19), dpi=200)
    ax.set_xlim(-1.8, W + 2.2)
    ax.set_ylim(-3.8, D + 2.8)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FFFFFF")

    # Fondos de Estancias
    ax.add_patch(patches.Rectangle((0, 0), W, D, facecolor="#FFFFFF", zorder=0))
    ax.add_patch(patches.Rectangle((1.4, 0), 5.0, 7.4, facecolor="#FAF6EE", zorder=1)) # Salón
    ax.add_patch(patches.Rectangle((6.4, 0), 4.0, 5.0, facecolor="#F4EFE6", zorder=1)) # Cocina
    ax.add_patch(patches.Rectangle((6.4, 5.0), 5.0, 2.6, facecolor="#EAE5DA", zorder=1)) # Porche cubierto
    ax.add_patch(patches.Rectangle((6.4, 7.6), 5.0, 5.4, facecolor="#EAF2E8", zorder=1)) # Patio
    
    # Lámina de agua y olivo
    ax.add_patch(patches.Rectangle((6.8, 8.0), 1.8, 1.8, facecolor="#D2E8F0", edgecolor="#6AA4B8", lw=1.2, zorder=2))
    ax.text(7.7, 8.9, "LÁMINA\nDE AGUA", ha="center", va="center", fontsize=7.5, color="#2D6B82", weight="bold", zorder=3)
    ax.add_patch(patches.Circle((9.7, 9.6), 0.75, facecolor="#B8D4A8", edgecolor="#5C8A47", lw=1.2, zorder=2))
    ax.text(9.7, 9.6, "OLIVO", ha="center", va="center", fontsize=8, color="#385C27", weight="bold", zorder=3)

    # Escalera Portal B
    ax.add_patch(patches.Rectangle((10.4, 0), 1.0, 5.0, facecolor="#EBECEE", zorder=1))
    for step in range(17):
        sy = step * (5.0 / 17.0)
        ax.plot([10.4, 11.4], [sy, sy], color="#8C9299", lw=0.8, zorder=2)
    ax.annotate("", xy=(10.9, 4.2), xytext=(10.9, 0.8), arrowprops=dict(arrowstyle="->", color="#3A4048", lw=1.5), zorder=3)
    ax.text(10.9, 2.5, "SUBE A P.A.", rotation=90, ha="center", va="center", fontsize=7.5, color="#2D3136", weight="bold", zorder=4)

    # Zonas húmedas y noche
    ax.add_patch(patches.Rectangle((0, 0), 1.4, 13.0, facecolor="#F7F7F7", zorder=1))
    ax.add_patch(patches.Rectangle((1.4, 7.4), 5.0, 1.4, facecolor="#F0F5F7", zorder=1))
    ax.add_patch(patches.Rectangle((1.4, 8.8), 5.0, 1.4, facecolor="#F0F5F7", zorder=1))
    ax.add_patch(patches.Rectangle((1.4, 10.2), 5.0, 2.8, facecolor="#FAF8F5", zorder=1))
    ax.add_patch(patches.Rectangle((0, 14.1), 3.2, 3.5, facecolor="#FAF8F5", zorder=1))
    ax.add_patch(patches.Rectangle((3.2, 14.1), 3.2, 3.5, facecolor="#FAF8F5", zorder=1))
    ax.add_patch(patches.Rectangle((6.4, 13.0), 1.6, 4.6, facecolor="#F0F0F0", zorder=1))
    ax.add_patch(patches.Rectangle((8.0, 13.0), 3.4, 4.6, facecolor="#EBECEE", zorder=1))

    # Mobiliario PB
    draw_furniture_sofa(ax, 1.8, 1.2, 2.8, 1.1)
    ax.add_patch(patches.Rectangle((2.6, 6.8), 2.2, 0.35, facecolor="#D9D2C5", edgecolor="#6E6659", lw=1.0, zorder=2))
    ax.text(3.7, 6.98, "MUEBLE TV", ha="center", va="center", fontsize=7, color="#4A443A", zorder=3)
    draw_furniture_table(ax, 2.0, 3.8, 2.2, 1.0, chairs=3)
    
    # Isla de cocina
    ax.add_patch(patches.Rectangle((7.0, 1.8), 2.4, 1.1, facecolor="#FFFFFF", edgecolor="#5C666B", lw=1.2, zorder=2))
    ax.text(8.2, 2.35, "ISLA DE COCINA\n(CON BARRA)", ha="center", va="center", fontsize=8, color="#2D3136", weight="bold", zorder=3)
    ax.add_patch(patches.Rectangle((6.5, 0.15), 3.7, 0.6, facecolor="#E8E2D5", edgecolor="#5C666B", lw=1.0, zorder=2))
    ax.text(8.35, 0.45, "BANCADA COCINA + ELECTRODOMÉSTICOS", ha="center", va="center", fontsize=6.5, color="#5C666B")

    # Dormitorio Principal
    draw_furniture_bed(ax, 3.8, 10.5, 1.8, 1.9)
    ax.add_patch(patches.Rectangle((1.55, 10.5), 0.6, 2.2, facecolor="#D9D2C5", edgecolor="#6E6659", lw=1.0, zorder=2))
    ax.text(1.85, 11.6, "ARMARIO", rotation=90, ha="center", va="center", fontsize=7, color="#4A443A", zorder=3)

    # Baños
    draw_bathroom_fixtures(ax, 1.4, 7.4, 5.0, 1.4)
    draw_bathroom_fixtures(ax, 1.4, 8.8, 5.0, 1.4)

    # Dormitorios 2 y 3
    draw_furniture_bed(ax, 0.4, 15.0, 1.4, 1.9)
    draw_furniture_bed(ax, 3.6, 15.0, 1.4, 1.9)
    ax.add_patch(patches.Rectangle((2.3, 14.3), 0.7, 1.6, facecolor="#D9D2C5", edgecolor="#6E6659", lw=1.0, zorder=2))
    ax.text(2.65, 15.1, "ARMARIO", rotation=90, ha="center", va="center", fontsize=6, color="#4A443A", zorder=3)
    ax.add_patch(patches.Rectangle((5.5, 14.3), 0.7, 1.6, facecolor="#D9D2C5", edgecolor="#6E6659", lw=1.0, zorder=2))
    ax.text(5.85, 15.1, "ARMARIO", rotation=90, ha="center", va="center", fontsize=6, color="#4A443A", zorder=3)

    # Coche en cochera
    ax.add_patch(patches.Rectangle((8.6, 14.2), 2.1, 2.9, facecolor="#D2DCE0", edgecolor="#3A4048", lw=1.2, zorder=2))
    ax.text(9.65, 15.65, "PLAZA GARAJE\n(COCHERA)", ha="center", va="center", fontsize=8, color="#2D3136", weight="bold", zorder=3)

    # Muros Poché Sólidos
    wall_color = "#1C1E21"
    ax.add_patch(patches.Rectangle((-0.15, -0.15), 0.30, D + 0.30, facecolor=wall_color, zorder=5))
    ax.add_patch(patches.Rectangle((W - 0.15, -0.15), 0.30, 5.15, facecolor=wall_color, zorder=5))
    ax.add_patch(patches.Rectangle((W - 0.15, 5.0), 0.30, 8.0, facecolor=wall_color, zorder=5))
    ax.add_patch(patches.Rectangle((W - 0.15, 13.0), 0.30, 4.75, facecolor=wall_color, zorder=5))

    # Fachada Sur (PB)
    ax.add_patch(patches.Rectangle((-0.15, -0.15), 0.45, 0.30, facecolor=wall_color, zorder=5))
    ax.add_patch(patches.Rectangle((1.30, -0.15), 1.30, 0.30, facecolor=wall_color, zorder=5))
    ax.add_patch(patches.Rectangle((4.40, -0.15), 0.40, 0.30, facecolor=wall_color, zorder=5))
    ax.add_patch(patches.Rectangle((6.00, -0.15), 0.90, 0.30, facecolor=wall_color, zorder=5))
    ax.add_patch(patches.Rectangle((8.10, -0.15), 0.80, 0.30, facecolor=wall_color, zorder=5))
    ax.add_patch(patches.Rectangle((9.90, -0.15), 0.50, 0.30, facecolor=wall_color, zorder=5))

    # Fachada Norte (PB)
    ax.add_patch(patches.Rectangle((-0.15, D - 0.15), 0.95, 0.30, facecolor=wall_color, zorder=5))
    ax.add_patch(patches.Rectangle((2.40, D - 0.15), 1.20, 0.30, facecolor=wall_color, zorder=5))
    ax.add_patch(patches.Rectangle((5.20, D - 0.15), 2.80, 0.30, facecolor=wall_color, zorder=5))

    # Muros interiores
    ax.add_patch(patches.Rectangle((1.35, 0), 0.10, 1.4, facecolor=wall_color, zorder=5))
    ax.add_patch(patches.Rectangle((1.35, 4.6), 0.10, 1.5, facecolor=wall_color, zorder=5))
    ax.add_patch(patches.Rectangle((1.35, 6.8), 0.10, 1.1, facecolor=wall_color, zorder=5))
    ax.add_patch(patches.Rectangle((1.35, 8.6), 0.10, 4.4, facecolor=wall_color, zorder=5))
    ax.add_patch(patches.Rectangle((6.35, 0), 0.10, 1.0, facecolor=wall_color, zorder=5))
    ax.add_patch(patches.Rectangle((6.35, 4.4), 0.10, 0.6, facecolor=wall_color, zorder=5))
    ax.add_patch(patches.Rectangle((10.35, 0), 0.10, 5.0, facecolor=wall_color, zorder=5))
    ax.add_patch(patches.Rectangle((6.25, 7.4), 0.30, 5.6, facecolor=wall_color, zorder=5))
    ax.add_patch(patches.Rectangle((1.4, 7.35), 5.0, 0.10, facecolor=wall_color, zorder=5))
    ax.add_patch(patches.Rectangle((1.4, 8.75), 5.0, 0.10, facecolor=wall_color, zorder=5))
    ax.add_patch(patches.Rectangle((1.4, 10.15), 1.9, 0.10, facecolor=wall_color, zorder=5))
    ax.add_patch(patches.Rectangle((4.0, 10.15), 2.4, 0.10, facecolor=wall_color, zorder=5))
    ax.add_patch(patches.Rectangle((1.4, 12.95), 0.8, 0.10, facecolor=wall_color, zorder=5))
    ax.add_patch(patches.Rectangle((2.9, 12.95), 5.1, 0.10, facecolor=wall_color, zorder=5))
    ax.add_patch(patches.Rectangle((0, 14.05), 0.8, 0.10, facecolor=wall_color, zorder=5))
    ax.add_patch(patches.Rectangle((1.5, 14.05), 2.1, 0.10, facecolor=wall_color, zorder=5))
    ax.add_patch(patches.Rectangle((4.3, 14.05), 2.1, 0.10, facecolor=wall_color, zorder=5))
    ax.add_patch(patches.Rectangle((3.15, 14.1), 0.10, 3.5, facecolor=wall_color, zorder=5))
    ax.add_patch(patches.Rectangle((6.35, 13.0), 0.10, 4.6, facecolor=wall_color, zorder=5))
    ax.add_patch(patches.Rectangle((7.95, 13.0), 0.10, 4.6, facecolor=wall_color, zorder=5))

    # Pilares de porche
    ax.add_patch(patches.Rectangle((6.9, 7.45), 0.25, 0.25, facecolor=wall_color, zorder=6))
    ax.add_patch(patches.Rectangle((9.5, 7.45), 0.25, 0.25, facecolor=wall_color, zorder=6))

    # Puertas interiores con abatimiento
    draw_interior_door(ax, 1.4, 7.9, 0.70, orientation="v", side=1) # Baño común
    draw_interior_door(ax, 3.3, 10.2, 0.70, orientation="h", side=-1) # Suite
    draw_interior_door(ax, 2.2, 13.0, 0.70, orientation="h", side=1) # Dorm Ppal
    draw_interior_door(ax, 0.8, 14.1, 0.70, orientation="h", side=1) # Dorm 2
    draw_interior_door(ax, 3.6, 14.1, 0.70, orientation="h", side=1) # Dorm 3
    draw_interior_door(ax, 8.0, 13.3, 0.60, orientation="v", side=1) # Trastero

    # Portal A (Entrada PB)
    ax.plot([0.3, 0.3 + 0.9], [0, 0.9], color="#C46D29", lw=2.5, zorder=8)
    draw_door_swing(ax, 0.3, 0, 0.9, 0, 90, color="#C46D29")
    ax.text(0.8, -0.45, "PORTAL A\n(VIV. A)", ha="center", va="center", fontsize=8, color="#C46D29", weight="bold")

    # Portal B (Entrada PA)
    ax.plot([10.4, 10.4 + 0.9], [0, 0.9], color="#C46D29", lw=2.5, zorder=8)
    draw_door_swing(ax, 10.4, 0, 0.9, 0, 90, color="#C46D29")
    ax.text(10.9, -0.45, "PORTAL B\n(VIV. B)", ha="center", va="center", fontsize=8, color="#C46D29", weight="bold")

    # Corredera Doble Salón-Cocina
    ax.plot([6.4, 6.4], [1.0, 4.4], color="#2B4C7E", lw=3.5, zorder=8)
    ax.text(6.05, 2.7, "CORREDERA EMBUTIDA (3,40 m)\n(SALÓN Y COCINA UNIBLES)", rotation=90, ha="center", va="center", fontsize=7, color="#2B4C7E", weight="bold")

    # Gran Corredera Salón -> Porche
    ax.plot([6.4, 6.4], [5.0, 7.4], color="#3A86C8", lw=3.5, zorder=8)
    ax.text(6.05, 6.2, "VENTANAL SUELO-TECHO\n(CONEXIÓN SALÓN-PORCHE)", rotation=90, ha="center", va="center", fontsize=7, color="#3A86C8", weight="bold")

    # Ventanales Fachada Sur
    for wx0, wx1 in [(2.6, 4.4), (4.8, 6.0), (6.9, 8.1), (8.9, 9.9)]:
        ax.plot([wx0, wx1], [0, 0], color="#3A86C8", lw=3.5, zorder=8)
        ax.plot([wx0, wx1], [-0.10, -0.10], color="#8C8275", lw=1.2, zorder=8)

    # Ventanas traseras y portón
    for wx0, wx1 in [(0.8, 2.4), (3.6, 5.2)]:
        ax.plot([wx0, wx1], [D, D], color="#3A86C8", lw=3.5, zorder=8)
    ax.plot([8.0, 11.4], [D, D], color="#A84B24", lw=4.5, zorder=8)
    ax.text(9.7, D + 0.45, "PORTÓN COCHERA (CORTÉN)", ha="center", va="center", fontsize=8, color="#A84B24", weight="bold")

    # Ventanas al patio
    for wy0, wy1 in [(7.8, 8.4), (9.0, 9.6), (11.0, 12.2)]:
        ax.plot([6.4, 6.4], [wy0, wy1], color="#3A86C8", lw=3.5, zorder=8)

    # Etiquetas de Estancias
    def label_room(x, y, name, area_str):
        ax.text(x, y + 0.18, name, ha="center", va="center", fontsize=9, color="#1C1E21", weight="bold", zorder=10)
        ax.text(x, y - 0.22, area_str, ha="center", va="center", fontsize=8, color="#5C666B", weight="bold", zorder=10)

    label_room(3.9, 2.6, "SALÓN - COMEDOR", "37,0 m²")
    label_room(8.4, 3.6, "COCINA", "20,0 m²")
    label_room(8.9, 6.3, "PORCHE CUBIERTO", "13,0 m²")
    label_room(8.9, 11.4, "PATIO CENTRAL", "27,0 m² (DESCUBIERTO)")
    label_room(3.9, 8.05, "BAÑO COMÚN", "7,0 m²")
    label_room(3.9, 9.45, "BAÑO EN SUITE", "7,0 m²")
    label_room(2.8, 11.6, "DORMITORIO\nPRINCIPAL", "14,0 m²")
    label_room(1.6, 16.2, "DORMITORIO 2", "11,2 m²")
    label_room(4.8, 16.2, "DORMITORIO 3", "11,2 m²")
    label_room(7.2, 15.3, "TRASTERO", "7,4 m²")

    # Cotas Exteriores
    ax.plot([0, W], [-1.2, -1.2], color="#3A4048", lw=1.0)
    ax.plot([0, 0], [-1.4, -1.0], color="#3A4048", lw=1.0)
    ax.plot([W, W], [-1.4, -1.0], color="#3A4048", lw=1.0)
    ax.text(W/2, -1.55, "FACHADA SUR (C/ MORENO TORROBA) · 11,40 m", ha="center", va="center", fontsize=9, color="#1C1E21", weight="bold")

    ax.plot([W + 0.8, W + 0.8], [0, D], color="#3A4048", lw=1.0)
    ax.plot([W + 0.6, W + 1.0], [0, 0], color="#3A4048", lw=1.0)
    ax.plot([W + 0.6, W + 1.0], [D, D], color="#3A4048", lw=1.0)
    ax.text(W + 1.25, D/2, "FONDO TOTAL DEL SOLAR · 17,60 m", rotation=90, ha="center", va="center", fontsize=9, color="#1C1E21", weight="bold")

    # Cajetín Inferior
    ax.add_patch(patches.Rectangle((0, -3.2), W, 1.0, facecolor="#FFFFFF", edgecolor="#1C1E21", lw=1.5, zorder=10))
    ax.text(0.3, -2.55, "PROYECTO RESIDENCIAL · PALMA DEL RÍO (CÓRDOBA)", fontsize=10.5, color="#1C1E21", weight="bold", zorder=11)
    ax.text(0.3, -2.95, "LÁMINA 2D-01 · PLANTA BAJA (VIVIENDA A) · DISTRIBUCIÓN Y MOBILIARIO", fontsize=8.5, color="#5C666B", zorder=11)
    ax.text(W - 0.3, -2.75, "ESCALA 1:50 | SUPERFICIE ÚTIL: 133,4 m²", ha="right", va="center", fontsize=8.5, color="#1C1E21", weight="bold", zorder=11)

    out_file = os.path.join(OUT_DIR, "01_plano_2d_planta_baja.png")
    plt.savefig(out_file, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    print("PLANO PB OK:", out_file)
    return out_file

# ==============================================================================
# 2. PLANTA ALTA (VIVIENDA B)
# ==============================================================================
def generar_plano_pa():
    fig, ax = plt.subplots(figsize=(12, 19), dpi=200)
    ax.set_xlim(-1.8, W + 2.2)
    ax.set_ylim(-3.8, D + 2.8)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FFFFFF")

    # Fondos de Estancias
    ax.add_patch(patches.Rectangle((0, 0), W, D, facecolor="#FFFFFF", zorder=0))
    # Gran Salón-Comedor Diáfano (50 m²)
    ax.add_patch(patches.Rectangle((1.4, 0), 5.0, 7.4, facecolor="#FAF6EE", zorder=1))
    ax.add_patch(patches.Rectangle((6.4, 5.0), 5.0, 2.6, facecolor="#FAF6EE", zorder=1))
    # Cocina PA
    ax.add_patch(patches.Rectangle((6.4, 0), 4.0, 5.0, facecolor="#F4EFE6", zorder=1))

    # Vacío Patio Central
    ax.add_patch(patches.Rectangle((6.4, 7.6), 5.0, 5.4, facecolor="#E6EAE8", hatch="//", edgecolor="#9BAE9E", lw=1.2, zorder=1))
    ax.text(8.9, 10.3, "VACÍO SOBRE PATIO\n(DOBLE ALTURA · 27 m²)", ha="center", va="center", fontsize=9, color="#486B50", weight="bold", zorder=3)

    # Escalera PA
    ax.add_patch(patches.Rectangle((10.4, 0), 1.0, 5.0, facecolor="#EBECEE", zorder=1))
    for step in range(17):
        sy = step * (5.0 / 17.0)
        ax.plot([10.4, 11.4], [sy, sy], color="#8C9299", lw=0.8, zorder=2)
    ax.text(10.9, 2.5, "LLEGADA ESCALERA", rotation=90, ha="center", va="center", fontsize=7.5, color="#2D3136", weight="bold", zorder=4)

    # Celosía de madera en fachada
    for li in range(12):
        lx = 10.42 + li * (0.96 / 11.0)
        ax.plot([lx, lx], [-0.15, 0.05], color="#C46D29", lw=2.2, zorder=8)
    ax.text(10.9, -0.45, "CELOSÍA MADERA\n(FILTRO SOLAR)", ha="center", va="center", fontsize=7, color="#C46D29", weight="bold")

    # Zonas húmedas y noche
    ax.add_patch(patches.Rectangle((0, 0), 1.4, 13.0, facecolor="#F7F7F7", zorder=1))
    ax.add_patch(patches.Rectangle((1.4, 7.4), 5.0, 1.4, facecolor="#F0F5F7", zorder=1))
    ax.add_patch(patches.Rectangle((1.4, 8.8), 5.0, 1.4, facecolor="#F0F5F7", zorder=1))
    ax.add_patch(patches.Rectangle((1.4, 10.2), 5.0, 2.8, facecolor="#FAF8F5", zorder=1))

    # Terraza Privada PA
    ax.add_patch(patches.Rectangle((0, 14.1), 3.2, 3.5, facecolor="#EBF0F2", hatch="\\\\", edgecolor="#7A9AA8", lw=1.2, zorder=1))
    ax.text(1.6, 15.8, "TERRAZA PRIVADA\nDESCUBIERTA\n(11,2 m²)", ha="center", va="center", fontsize=8, color="#3A6B7E", weight="bold", zorder=3)

    # Dormitorio 3 y Gran Dormitorio 2
    ax.add_patch(patches.Rectangle((3.2, 14.1), 3.2, 3.5, facecolor="#FAF8F5", zorder=1))
    ax.add_patch(patches.Rectangle((6.4, 13.0), 5.0, 4.6, facecolor="#FAF8F5", zorder=1))

    # Mobiliario PA
    draw_furniture_sofa(ax, 1.8, 1.2, 3.0, 1.1)
    draw_furniture_table(ax, 2.0, 3.8, 2.2, 1.0, chairs=3)
    ax.add_patch(patches.Rectangle((7.0, 5.3), 1.8, 0.9, facecolor="#E6DEC9", edgecolor="#7A6F5D", lw=1.0, zorder=2))
    ax.text(7.9, 5.75, "ZONA LECTURA\n/ ESTUDIO", ha="center", va="center", fontsize=7.5, color="#4A443A", zorder=3)
    
    # Isla Cocina PA
    ax.add_patch(patches.Rectangle((7.0, 1.8), 2.4, 1.1, facecolor="#FFFFFF", edgecolor="#5C666B", lw=1.2, zorder=2))
    ax.text(8.2, 2.35, "ISLA COCINA PA", ha="center", va="center", fontsize=8, color="#2D3136", weight="bold", zorder=3)

    # Dormitorio Principal PA
    draw_furniture_bed(ax, 3.8, 10.5, 1.8, 1.9)
    ax.add_patch(patches.Rectangle((1.55, 10.5), 0.6, 2.2, facecolor="#D9D2C5", edgecolor="#6E6659", lw=1.0, zorder=2))

    # Baños PA
    draw_bathroom_fixtures(ax, 1.4, 7.4, 5.0, 1.4)
    draw_bathroom_fixtures(ax, 1.4, 8.8, 5.0, 1.4)

    # Dormitorio 3 PA
    draw_furniture_bed(ax, 3.6, 15.0, 1.4, 1.9)

    # Gran Dormitorio 2 PA (Suite de 23 m²)
    draw_furniture_bed(ax, 7.2, 15.0, 1.8, 1.9)
    ax.add_patch(patches.Rectangle((10.4, 13.2), 0.7, 4.0, facecolor="#D9D2C5", edgecolor="#6E6659", lw=1.0, zorder=2))
    ax.text(10.75, 15.2, "VESTIDOR LINEAL (4,00 m)", rotation=90, ha="center", va="center", fontsize=7, color="#4A443A", zorder=3)
    ax.add_patch(patches.Rectangle((6.8, 13.3), 1.6, 0.7, facecolor="#E6DEC9", edgecolor="#7A6F5D", lw=1.0, zorder=2))
    ax.text(7.6, 13.65, "MESA DE TRABAJO", ha="center", va="center", fontsize=7, color="#4A443A", zorder=3)

    # Muros Poché PA
    wall_color = "#1C1E21"
    ax.add_patch(patches.Rectangle((-0.15, -0.15), 0.30, D + 0.30, facecolor=wall_color, zorder=5))
    ax.add_patch(patches.Rectangle((W - 0.15, -0.15), 0.30, 5.15, facecolor=wall_color, zorder=5))
    ax.add_patch(patches.Rectangle((W - 0.15, 5.0), 0.30, 8.0, facecolor=wall_color, zorder=5))
    ax.add_patch(patches.Rectangle((W - 0.15, 13.0), 0.30, 4.75, facecolor=wall_color, zorder=5))

    # Fachada Sur PA (Voladizo 40 cm)
    ax.add_patch(patches.Rectangle((-0.15, -0.15), 2.75, 0.30, facecolor=wall_color, zorder=5))
    ax.add_patch(patches.Rectangle((6.00, -0.40), 0.60, 0.30, facecolor=wall_color, zorder=5))
    ax.add_patch(patches.Rectangle((9.90, -0.15), 0.50, 0.30, facecolor=wall_color, zorder=5))

    # Fachada Norte PA
    ax.add_patch(patches.Rectangle((3.20, D - 0.15), 0.40, 0.30, facecolor=wall_color, zorder=5))
    ax.add_patch(patches.Rectangle((5.20, D - 0.15), 1.80, 0.30, facecolor=wall_color, zorder=5))
    ax.add_patch(patches.Rectangle((-0.15, D - 0.15), 3.35, 0.15, facecolor="#7A9AA8", zorder=5))
    ax.add_patch(patches.Rectangle((3.15, 14.1), 0.10, 3.5, facecolor="#7A9AA8", zorder=5))

    # Muros interiores PA
    ax.add_patch(patches.Rectangle((6.35, 7.6), 0.15, 5.4, facecolor=wall_color, zorder=5))
    ax.add_patch(patches.Rectangle((6.4, 7.5), 5.0, 0.15, facecolor=wall_color, zorder=5))
    ax.add_patch(patches.Rectangle((6.4, 12.95), 0.6, 0.15, facecolor=wall_color, zorder=5))
    ax.add_patch(patches.Rectangle((10.4, 12.95), 1.0, 0.15, facecolor=wall_color, zorder=5))
    ax.add_patch(patches.Rectangle((1.4, 7.35), 5.0, 0.10, facecolor=wall_color, zorder=5))
    ax.add_patch(patches.Rectangle((1.4, 8.75), 5.0, 0.10, facecolor=wall_color, zorder=5))
    ax.add_patch(patches.Rectangle((1.4, 10.15), 1.9, 0.10, facecolor=wall_color, zorder=5))
    ax.add_patch(patches.Rectangle((4.0, 10.15), 2.4, 0.10, facecolor=wall_color, zorder=5))
    ax.add_patch(patches.Rectangle((1.4, 12.95), 0.8, 0.10, facecolor=wall_color, zorder=5))
    ax.add_patch(patches.Rectangle((2.9, 12.95), 3.5, 0.10, facecolor=wall_color, zorder=5))
    ax.add_patch(patches.Rectangle((0, 14.05), 0.8, 0.10, facecolor=wall_color, zorder=5))
    ax.add_patch(patches.Rectangle((1.5, 14.05), 2.1, 0.10, facecolor=wall_color, zorder=5))
    ax.add_patch(patches.Rectangle((4.3, 14.05), 2.1, 0.10, facecolor=wall_color, zorder=5))
    ax.add_patch(patches.Rectangle((6.35, 13.0), 0.10, 0.2, facecolor=wall_color, zorder=5))
    ax.add_patch(patches.Rectangle((6.35, 14.0), 0.10, 3.6, facecolor=wall_color, zorder=5))

    # Puertas interiores PA
    draw_interior_door(ax, 1.4, 7.9, 0.70, orientation="v", side=1)
    draw_interior_door(ax, 3.3, 10.2, 0.70, orientation="h", side=-1)
    draw_interior_door(ax, 2.2, 13.0, 0.70, orientation="h", side=1)
    draw_interior_door(ax, 0.8, 14.1, 0.70, orientation="h", side=1)
    draw_interior_door(ax, 3.6, 14.1, 0.70, orientation="h", side=1)
    draw_interior_door(ax, 6.4, 13.2, 0.80, orientation="v", side=1) # Dorm 2

    # Grandes Ventanales PA
    ax.plot([2.6, 6.0], [-0.40, -0.40], color="#3A86C8", lw=4.0, zorder=8)
    ax.plot([6.6, 9.9], [-0.40, -0.40], color="#3A86C8", lw=4.0, zorder=8)
    ax.text(4.3, -0.75, "GRAN VENTANAL SALÓN PA\n(SUELO A TECHO 3,40 m)", ha="center", va="center", fontsize=7.5, color="#3A86C8", weight="bold")
    ax.text(8.25, -0.75, "GRAN VENTANAL COCINA PA\n(SUELO A TECHO 3,30 m)", ha="center", va="center", fontsize=7.5, color="#3A86C8", weight="bold")

    # Galería hacia el patio
    ax.plot([6.4, 6.4], [5.0, 7.6], color="#3A86C8", lw=4.0, zorder=8)
    ax.text(6.05, 6.3, "GALERÍA MIRADOR ACRISTALADA\n(VISTAS DIRECTAS AL PATIO)", rotation=90, ha="center", va="center", fontsize=7, color="#3A86C8", weight="bold")

    # Ventanales Dorm 2 PA
    ax.plot([7.0, 11.2], [D, D], color="#3A86C8", lw=4.0, zorder=8)
    ax.text(9.1, D + 0.45, "VENTANAL PANORÁMICO DORM 2 (4,20 m)", ha="center", va="center", fontsize=8, color="#3A86C8", weight="bold")
    ax.plot([7.0, 10.4], [13.0, 13.0], color="#3A86C8", lw=3.5, zorder=8)
    ax.text(8.7, 12.6, "VENTANAL DORM 2 AL PATIO", ha="center", va="center", fontsize=7, color="#3A86C8", weight="bold")

    # Ventana Dorm 3
    ax.plot([3.6, 5.2], [D, D], color="#3A86C8", lw=3.5, zorder=8)

    # Etiquetas de Estancias PA
    def label_room_pa(x, y, name, area_str):
        ax.text(x, y + 0.18, name, ha="center", va="center", fontsize=9, color="#1C1E21", weight="bold", zorder=10)
        ax.text(x, y - 0.22, area_str, ha="center", va="center", fontsize=8, color="#5C666B", weight="bold", zorder=10)

    label_room_pa(3.9, 2.6, "SALÓN - COMEDOR DIÁFANO", "50,0 m² (INTEGRA PASILLO)")
    label_room_pa(8.4, 3.6, "COCINA", "20,0 m²")
    label_room_pa(3.9, 8.05, "BAÑO COMÚN", "7,0 m²")
    label_room_pa(3.9, 9.45, "BAÑO EN SUITE", "7,0 m²")
    label_room_pa(2.8, 11.6, "DORMITORIO\nPRINCIPAL", "14,0 m²")
    label_room_pa(4.8, 16.2, "DORMITORIO 3", "11,2 m²")
    label_room_pa(8.9, 14.3, "GRAN DORMITORIO 2 (SUITE)", "23,0 m²")

    # Cotas Exteriores
    ax.plot([0, W], [-1.2, -1.2], color="#3A4048", lw=1.0)
    ax.plot([0, 0], [-1.4, -1.0], color="#3A4048", lw=1.0)
    ax.plot([W, W], [-1.4, -1.0], color="#3A4048", lw=1.0)
    ax.text(W/2, -1.55, "FACHADA SUR CON VOLADIZO · 11,40 m", ha="center", va="center", fontsize=9, color="#1C1E21", weight="bold")

    ax.plot([W + 0.8, W + 0.8], [0, D], color="#3A4048", lw=1.0)
    ax.plot([W + 0.6, W + 1.0], [0, 0], color="#3A4048", lw=1.0)
    ax.plot([W + 0.6, W + 1.0], [D, D], color="#3A4048", lw=1.0)
    ax.text(W + 1.25, D/2, "FONDO TOTAL DEL SOLAR · 17,60 m", rotation=90, ha="center", va="center", fontsize=9, color="#1C1E21", weight="bold")

    # Cajetín Inferior
    ax.add_patch(patches.Rectangle((0, -3.2), W, 1.0, facecolor="#FFFFFF", edgecolor="#1C1E21", lw=1.5, zorder=10))
    ax.text(0.3, -2.55, "PROYECTO RESIDENCIAL · PALMA DEL RÍO (CÓRDOBA)", fontsize=10.5, color="#1C1E21", weight="bold", zorder=11)
    ax.text(0.3, -2.95, "LÁMINA 2D-02 · PLANTA ALTA (VIVIENDA B) · DISTRIBUCIÓN Y MOBILIARIO", fontsize=8.5, color="#5C666B", zorder=11)
    ax.text(W - 0.3, -2.75, "ESCALA 1:50 | SUPERFICIE ÚTIL: 132,2 m²", ha="right", va="center", fontsize=8.5, color="#1C1E21", weight="bold", zorder=11)

    out_file = os.path.join(OUT_DIR, "02_plano_2d_planta_alta.png")
    plt.savefig(out_file, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    print("PLANO PA OK:", out_file)
    return out_file

if __name__ == "__main__":
    generar_plano_pb()
    generar_plano_pa()
