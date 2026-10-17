# -*- coding: utf-8 -*-
"""
PLANO ARQUITECTÓNICO EJECUTIVO - PLANTA ALTA (VIVIENDA B) - ESCALA 1:50 (A3)
Proyecto: Vivienda Bifamiliar en Parcela Pasante
Emplazamiento: Calle Moreno Torroba s/n, Palma del Río (Córdoba)
Distribución completa con cotas, mobiliario, carpinterías, cuadro de superficies y cajetín oficial.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import os

OUTPUT_DIR = r"C:\Users\Oscar Martinez\Desktop\mi-casa\entrega\planos_2d"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Paleta Arquitectónica
C_WALL      = "#181A1D"       # Muros exteriores (negro sólido)
C_WALL_INT  = "#2C3036"       # Tabiquería interior
C_DIM       = "#B91C1C"       # Rojo técnico de cotas
C_DIM_LINE  = "#DC2626"       # Líneas de cota
C_TEXT_MAIN = "#0F172A"       # Textos principales
C_TEXT_SEC  = "#475569"       # Textos secundarios
C_BLUE_CAD  = "#0369A1"       # Azul técnico áreas
C_WOOD      = "#B45309"       # Puertas y madera
C_GLASS     = "#0EA5E9"       # Vidrios

# Suelos
C_FLOOR_LIVING  = "#FAF8F5"
C_FLOOR_KITCHEN = "#F5F2EC"
C_FLOOR_BATH    = "#F0F4F8"
C_FLOOR_BED     = "#FCFAF7"
C_FLOOR_TERRACE = "#F5EFE6"
C_FLOOR_VOID    = "#F1F5F9"

def setup_architect_canvas():
    fig, ax = plt.subplots(figsize=(22, 15.5), dpi=300)
    ax.set_xlim(-5.2, 17.2)
    ax.set_ylim(-5.5, 21.8)
    ax.set_aspect('equal')
    ax.axis('off')
    return fig, ax

def draw_rect(ax, x, y, w, h, fill_col, edge_col=None, lw=0.6, z=1):
    r = patches.Rectangle((x, y), w, h, facecolor=fill_col,
                           edgecolor=edge_col, linewidth=lw, zorder=z)
    ax.add_patch(r)
    return r

def draw_wall(ax, x, y, w, h, is_exterior=True):
    col = C_WALL if is_exterior else C_WALL_INT
    r = patches.Rectangle((x, y), w, h, facecolor=col,
                           edgecolor="#000000", linewidth=0.7, zorder=20)
    ax.add_patch(r)

def draw_window_cad(ax, x, y, w, h, is_horiz=True, label=""):
    draw_rect(ax, x, y, w, h, "#FFFFFF", edge_col=None, z=21)
    if is_horiz:
        ax.plot([x, x+w], [y, y], color=C_WALL, lw=0.8, zorder=22)
        ax.plot([x, x+w], [y+h, y+h], color=C_WALL, lw=0.8, zorder=22)
        ax.plot([x, x+w], [y+h*0.35, y+h*0.35], color="#64748B", lw=0.5, zorder=23)
        ax.plot([x, x+w], [y+h*0.65, y+h*0.65], color="#64748B", lw=0.5, zorder=23)
        ax.plot([x, x+w], [y+h*0.50, y+h*0.50], color=C_GLASS, lw=1.5, zorder=24)
        ax.plot([x, x], [y, y+h], color=C_WALL, lw=0.9, zorder=23)
        ax.plot([x+w, x+w], [y, y+h], color=C_WALL, lw=0.9, zorder=23)
        if label:
            ax.text(x+w/2, y-0.20, label, ha='center', va='top', fontsize=5.5, color=C_TEXT_SEC, zorder=25)
    else:
        ax.plot([x, x], [y, y+h], color=C_WALL, lw=0.8, zorder=22)
        ax.plot([x+w, x+w], [y, y+h], color=C_WALL, lw=0.8, zorder=22)
        ax.plot([x+w*0.35, x+w*0.35], [y, y+h], color="#64748B", lw=0.5, zorder=23)
        ax.plot([x+w*0.65, x+w*0.65], [y, y+h], color="#64748B", lw=0.5, zorder=23)
        ax.plot([x+w*0.50, x+w*0.50], [y, y+h], color=C_GLASS, lw=1.5, zorder=24)
        ax.plot([x, x+w], [y, y], color=C_WALL, lw=0.9, zorder=23)
        ax.plot([x, x+w], [y+h, y+h], color=C_WALL, lw=0.9, zorder=23)
        if label:
            ax.text(x+w+0.15, y+h/2, label, ha='left', va='center', fontsize=5.5, color=C_TEXT_SEC, rotation=90, zorder=25)

def draw_door_cad(ax, x, y, r, a_start, a_end, label=""):
    arc = patches.Arc((x, y), 2*r, 2*r, angle=0,
                      theta1=min(a_start, a_end),
                      theta2=max(a_start, a_end),
                      color="#94A3B8", linewidth=0.7, linestyle='--', zorder=18)
    ax.add_patch(arc)
    rad = a_start * np.pi / 180.0
    ax.plot([x, x + r*np.cos(rad)], [y, y + r*np.sin(rad)],
            color=C_WOOD, linewidth=1.5, zorder=19)
    if label:
        ax.text(x + r*0.45*np.cos(rad+0.35), y + r*0.45*np.sin(rad+0.35), label,
                fontsize=5.2, color=C_TEXT_SEC, ha='center', va='center', zorder=21)

def draw_sliding_door(ax, x1, y1, x2, y2, label=""):
    ax.plot([x1, x2], [y1, y2], color=C_GLASS, lw=2.2, zorder=23)
    ax.plot([x1, x2], [y1+0.04, y2+0.04], color="#475569", lw=0.8, linestyle='--', zorder=24)
    if label:
        ax.text((x1+x2)/2, (y1+y2)/2 + 0.15, label, ha='center', va='bottom', fontsize=5.2, color=C_TEXT_SEC, zorder=25)

def draw_cota_arch_h(ax, x1, x2, y, val_str, offset=0.14, tick=0.08):
    if x1 > x2: x1, x2 = x2, x1
    ax.plot([x1, x2], [y, y], color=C_DIM_LINE, lw=0.6, zorder=30)
    ax.plot([x1 - tick, x1 + tick], [y - tick, y + tick], color=C_DIM, lw=1.1, zorder=31)
    ax.plot([x2 - tick, x2 + tick], [y - tick, y + tick], color=C_DIM, lw=1.1, zorder=31)
    ax.plot([x1, x1], [y - tick*1.3, y + tick*1.3], color=C_DIM_LINE, lw=0.3, linestyle=':', zorder=29)
    ax.plot([x2, x2], [y - tick*1.3, y + tick*1.3], color=C_DIM_LINE, lw=0.3, linestyle=':', zorder=29)
    ax.text((x1 + x2)/2.0, y + offset, val_str, ha='center', va='bottom',
            fontsize=6.8, color=C_DIM, weight='bold', zorder=32,
            bbox=dict(boxstyle='square,pad=0.06', facecolor='#FFFFFF', edgecolor='none', alpha=0.92))

def draw_cota_arch_v(ax, y1, y2, x, val_str, offset=0.14, tick=0.08):
    if y1 > y2: y1, y2 = y2, y1
    ax.plot([x, x], [y1, y2], color=C_DIM_LINE, lw=0.6, zorder=30)
    ax.plot([x - tick, x + tick], [y1 - tick, y1 + tick], color=C_DIM, lw=1.1, zorder=31)
    ax.plot([x - tick, x + tick], [y2 - tick, y2 + tick], color=C_DIM, lw=1.1, zorder=31)
    ax.plot([x - tick*1.3, x + tick*1.3], [y1, y1], color=C_DIM_LINE, lw=0.3, linestyle=':', zorder=29)
    ax.plot([x - tick*1.3, x + tick*1.3], [y2, y2], color=C_DIM_LINE, lw=0.3, linestyle=':', zorder=29)
    ax.text(x + offset, (y1 + y2)/2.0, val_str, ha='left', va='center',
            fontsize=6.8, color=C_DIM, weight='bold', rotation=90, zorder=32,
            bbox=dict(boxstyle='square,pad=0.06', facecolor='#FFFFFF', edgecolor='none', alpha=0.92))

def draw_room_badge(ax, x, y, name, area_str, pav="Porcelánico"):
    w_box, h_box = 2.40, 0.65
    draw_rect(ax, x - w_box/2, y - h_box/2, w_box, h_box, "#FFFFFF", edge_col="#94A3B8", lw=0.5, z=26)
    ax.text(x, y + 0.14, name, ha='center', va='center', fontsize=7.0, weight='bold', color=C_TEXT_MAIN, zorder=27)
    ax.text(x, y - 0.04, f"S.Útil: {area_str}", ha='center', va='center', fontsize=6.5, weight='bold', color=C_BLUE_CAD, zorder=27)
    ax.text(x, y - 0.20, f"Pav: {pav}", ha='center', va='center', fontsize=4.8, color=C_TEXT_SEC, zorder=27)

def draw_north_arrow(ax, x, y):
    r = 0.8
    ax.plot([x, x], [y - r, y + r], color=C_TEXT_MAIN, lw=1.2, zorder=35)
    ax.plot([x - r*0.4, x + r*0.4], [y, y], color=C_TEXT_MAIN, lw=0.6, zorder=35)
    pts_n = [[x, y + r], [x - r*0.22, y], [x, y], [x, y + r]]
    poly = patches.Polygon(pts_n, facecolor=C_TEXT_MAIN, edgecolor=C_TEXT_MAIN, zorder=36)
    ax.add_patch(poly)
    ax.text(x, y + r + 0.15, "N", ha='center', va='bottom', fontsize=10, weight='bold', color=C_TEXT_MAIN, zorder=37)
    ax.text(x, y - r - 0.12, "NORTE", ha='center', va='top', fontsize=5.5, color=C_TEXT_SEC, zorder=37)

def generar_planta_alta():
    fig, ax = setup_architect_canvas()

    # 1. SUELOS ARQUITECTÓNICOS
    # Salón-Comedor y pasillo sobre porche
    draw_rect(ax, 0.00, 0.00, 6.40, 7.40, C_FLOOR_LIVING)
    draw_rect(ax, 6.40, 5.00, 5.00, 2.40, C_FLOOR_LIVING) # Salón integrado sobre porche
    # Cocina
    draw_rect(ax, 6.40, 0.00, 4.00, 5.00, C_FLOOR_KITCHEN)
    # Escalera desembarco
    draw_rect(ax, 10.40, 0.00, 1.00, 5.00, "#E2E8F0")

    # Pasillo Noche y distribuidor
    draw_rect(ax, 0.00, 7.40, 1.20, 6.10, C_FLOOR_LIVING)
    draw_rect(ax, 0.00, 12.80, 6.40, 1.00, C_FLOOR_LIVING)

    # Baños Planta Alta (Apilados)
    draw_rect(ax, 1.20, 7.40, 2.60, 2.40, C_FLOOR_BATH)
    draw_rect(ax, 3.80, 7.40, 2.60, 2.40, C_FLOOR_BATH)

    # Dormitorio Principal (Suite PA)
    draw_rect(ax, 1.20, 9.80, 5.20, 3.00, C_FLOOR_BED)

    # Dormitorio 2 (Sobre cochera, 5.00 x 4.60 = 23.00 m² brutos)
    draw_rect(ax, 6.40, 13.00, 5.00, 4.60, C_FLOOR_BED)

    # Dormitorio 3
    draw_rect(ax, 3.20, 13.80, 3.20, 3.80, C_FLOOR_BED)

    # Terraza Solárium Privada Norte (0.00 a 3.20 x 13.80 a 17.60 = 12.16 m²)
    draw_rect(ax, 0.00, 13.80, 3.20, 3.80, C_FLOOR_TERRACE, edge_col="#D97706", lw=0.6, z=2)
    # Suelo deck madera exterior
    for ty in np.linspace(13.90, 17.50, 10):
        ax.plot([0.10, 3.10], [ty, ty], color="#D97706", lw=0.3, zorder=3)

    # VACÍO PATIO Y PISCINA (Bajo rasante PA)
    draw_rect(ax, 6.40, 7.40, 5.00, 5.60, "#F8FAFC", edge_col="#94A3B8", lw=0.8, z=2)
    # Rayado diagonal de vacío
    for vx in np.linspace(6.60, 11.20, 8):
        ax.plot([vx, vx+1.0], [7.40, 8.40], color="#CBD5E1", lw=0.5, linestyle='--', zorder=3)
    ax.text(8.90, 10.20, "VACÍO SOBRE PATIO Y PISCINA (PB)", ha='center', va='center',
            fontsize=7.5, weight='bold', color="#64748B", zorder=4)
    ax.text(8.90, 9.70, "Barandilla perimetral de vidrio laminar h=1,10 m", ha='center', va='center',
            fontsize=5.5, color="#94A3B8", zorder=4)

    # 2. MUROS EXTERIORES Y MEDIANERAS (0.30 m)
    draw_wall(ax, -0.15, -0.15, 0.30, 17.90)
    draw_wall(ax, 11.25, -0.15, 0.30, 17.90)

    # Fachada Sur (C/ Moreno Torroba)
    draw_wall(ax, -0.15, -0.15, 2.75, 0.30)
    draw_wall(ax, 4.40, -0.15, 0.40, 0.30)
    draw_wall(ax, 6.00, -0.15, 0.90, 0.30)
    draw_wall(ax, 8.10, -0.15, 0.80, 0.30)
    draw_wall(ax, 9.90, -0.15, 0.65, 0.30)

    # Fachada Norte
    draw_wall(ax, -0.15, 17.45, 0.95, 0.30)
    draw_wall(ax, 2.40, 17.45, 1.20, 0.30)
    draw_wall(ax, 5.20, 17.45, 1.80, 0.30)
    draw_wall(ax, 9.00, 17.45, 0.80, 0.30)
    draw_wall(ax, 11.00, 17.45, 0.40, 0.30)

    # Muro Sur del Dormitorio 2 hacia el patio
    draw_wall(ax, 6.30, 12.85, 0.80, 0.30, True)
    draw_wall(ax, 9.50, 12.85, 1.90, 0.30, True)

    # Muro Oeste Dormitorio 2
    draw_wall(ax, 6.30, 13.00, 0.20, 4.60, True)

    # Muro Este de la Master Suite y Baños (Fachada al patio)
    draw_wall(ax, 6.30, 7.35, 0.20, 5.65, True)

    # Muro Sur Salón sobre porche hacia el vacío
    draw_wall(ax, 6.30, 7.25, 1.00, 0.25, True)
    draw_wall(ax, 9.80, 7.25, 1.60, 0.25, True)

    # 3. TABIQUERÍA INTERIOR (0.10 m)
    draw_wall(ax, 6.35, 0.00, 0.10, 0.80, False)
    draw_wall(ax, 6.35, 4.20, 0.10, 0.80, False)
    draw_wall(ax, 10.35, 0.00, 0.10, 5.00, False)

    # Salón ↔ Baños
    draw_wall(ax, 1.15, 7.35, 5.25, 0.10, False)

    # Muro Técnico Central Baños
    draw_wall(ax, 3.75, 7.35, 0.15, 2.45, False)
    draw_rect(ax, 3.77, 8.30, 0.11, 0.55, "#E2E8F0", edge_col=C_WALL, lw=0.5, z=21)
    ax.text(3.82, 8.58, "B.F.", ha='center', va='center', fontsize=4.2, color="#475569", rotation=90, zorder=22)

    # Baños ↔ Suite
    draw_wall(ax, 1.15, 9.75, 2.65, 0.10, False)
    draw_wall(ax, 4.70, 9.75, 1.70, 0.10, False)

    # Pasillo ↔ Suite
    draw_wall(ax, 1.15, 9.75, 0.10, 0.25, False)
    draw_wall(ax, 1.15, 10.85, 0.10, 2.05, False)

    # Suite ↔ Distribuidor Norte
    draw_wall(ax, 1.15, 12.75, 5.25, 0.10, False)

    # Distribuidor ↔ Terraza y Dorm 3
    draw_wall(ax, -0.15, 13.75, 0.95, 0.10, False)
    draw_wall(ax, 1.75, 13.75, 1.55, 0.10, False)
    draw_wall(ax, 4.25, 13.75, 2.15, 0.10, False)

    # Separación Terraza ↔ Dormitorio 3
    draw_wall(ax, 3.15, 13.75, 0.15, 3.85, True)

    # 4. CARPINTERÍAS
    # Fachada Sur
    draw_window_cad(ax, 2.60, -0.05, 1.80, 0.10, True, "V-11 (180x140)")
    draw_window_cad(ax, 4.80, -0.05, 1.20, 0.10, True, "V-12 (120x140)")
    draw_window_cad(ax, 6.90, -0.05, 1.20, 0.10, True, "V-13 (120x140)")
    draw_window_cad(ax, 8.90, -0.05, 1.00, 0.10, True, "V-14 (100x140)")

    # Fachada al Patio
    draw_window_cad(ax, 7.30, 7.30, 2.50, 0.15, True, "V-15 (Corredera Terraza Patio)")
    draw_window_cad(ax, 6.40, 7.60, 0.10, 0.80, False, "V-16 (80x60)")
    draw_window_cad(ax, 6.40, 8.75, 0.10, 0.80, False, "V-17 (80x60)")
    draw_window_cad(ax, 6.40, 10.10, 0.10, 2.50, False, "V-18 (Panorámico Suite)")
    draw_window_cad(ax, 7.10, 12.90, 2.40, 0.15, True, "V-19 (Balconera Dorm 2)")

    # Fachada Norte
    draw_window_cad(ax, 0.80, 17.55, 1.60, 0.10, True, "V-20 (Salida Terraza)")
    draw_window_cad(ax, 3.60, 17.55, 1.60, 0.10, True, "V-21 (160x140)")
    draw_window_cad(ax, 7.00, 17.55, 2.00, 0.10, True, "V-22 (200x140)")
    draw_window_cad(ax, 9.80, 17.55, 1.20, 0.10, True, "V-23 (120x140)")

    # Barandilla de vidrio hacia el patio (X 6.40 a 11.40)
    ax.plot([6.40, 11.40], [7.45, 7.45], color="#0EA5E9", lw=2.5, zorder=22)
    ax.plot([6.40, 6.40], [7.45, 13.00], color="#0EA5E9", lw=2.5, zorder=22)
    ax.plot([6.40, 11.40], [13.00, 13.00], color="#0EA5E9", lw=2.5, zorder=22)

    # Puertas
    draw_door_cad(ax, 10.40, 4.90, 0.90, 90, 180, "Entrada Viv. B 90")
    draw_sliding_door(ax, 6.40, 0.80, 6.40, 4.20, "Corredera Salón-Cocina (3.40 m)")
    draw_door_cad(ax, 0.20, 7.35, 0.85, 0, 90, "82.5")
    draw_door_cad(ax, 1.20, 7.45, 0.80, 0, 90, "72.5")
    draw_sliding_door(ax, 3.90, 9.80, 4.70, 9.80, "Corredera 80")
    draw_door_cad(ax, 1.20, 10.00, 0.85, 0, 90, "Suite 82.5")
    draw_door_cad(ax, 0.95, 13.85, 0.80, 0, 90, "Terraza 80")
    draw_door_cad(ax, 3.40, 13.85, 0.85, 0, 90, "82.5")
    draw_door_cad(ax, 6.40, 13.20, 0.85, -90, 0, "82.5")

    # Escalera desembarco (bajando a planta baja)
    for st in range(16):
        sy = st * (5.0 / 16.0)
        ax.plot([10.40, 11.40], [sy, sy], color="#94A3B8", lw=0.5, zorder=5)
    ax.annotate('', xy=(10.90, 0.80), xytext=(10.90, 4.50),
                arrowprops=dict(arrowstyle='->', color="#475569", lw=1.0), zorder=6)
    ax.text(10.90, 2.50, "BAJA A PLANTA BAJA", ha='center', va='center', fontsize=5.0, color="#475569", rotation=90, zorder=7,
            bbox=dict(boxstyle='square,pad=0.08', facecolor='#FFFFFF', edgecolor='none'))

    # 5. MOBILIARIO ARQUITECTÓNICO PLANTA ALTA
    # A. Salón - Comedor Ampliado
    draw_rect(ax, 0.15, 2.40, 0.70, 3.60, "#F1ECE1", edge_col="#78716C", lw=0.8, z=5)
    draw_rect(ax, 0.20, 3.50, 0.60, 1.40, "#1E293B", edge_col="#0F172A", lw=0.6, z=6)
    ax.text(0.50, 4.20, "MUEBLE TV INTEGRADO + LIBRERÍA", ha='center', va='center', fontsize=5.0, rotation=90, color="#FFFFFF", zorder=7)

    draw_rect(ax, 1.80, 2.60, 2.80, 1.10, "#E2E8F0", edge_col="#94A3B8", lw=0.7, z=5)
    draw_rect(ax, 3.60, 3.70, 1.00, 1.40, "#E2E8F0", edge_col="#94A3B8", lw=0.7, z=5)
    draw_rect(ax, 2.10, 3.90, 1.20, 0.60, "#CBD5E1", edge_col="#94A3B8", lw=0.5, z=6)
    draw_rect(ax, 1.80, 0.90, 2.20, 1.00, "#F8FAFC", edge_col="#78716C", lw=0.8, z=5)

    # Zona Salón sobre porche (estar panorámico con vistas al patio)
    draw_rect(ax, 7.20, 5.40, 2.60, 1.00, "#E2E8F0", edge_col="#94A3B8", lw=0.7, z=5)
    ax.text(8.50, 5.90, "ZONA ESTAR / LECTURA PANORÁMICA", ha='center', va='center', fontsize=4.8, color="#475569", zorder=6)

    # B. Cocina con Isla
    draw_rect(ax, 6.50, 0.15, 3.30, 0.65, "#F8FAFC", edge_col="#64748B", lw=0.7, z=5)
    draw_rect(ax, 9.70, 0.80, 0.65, 2.60, "#334155", edge_col="#0F172A", lw=0.8, z=5)
    draw_rect(ax, 7.00, 1.70, 2.40, 1.10, "#FFFFFF", edge_col="#64748B", lw=0.9, z=5)

    # C. Baños
    draw_rect(ax, 1.30, 7.50, 2.35, 0.75, "#E0F2FE", edge_col="#0284C7", lw=0.7, z=5)
    draw_rect(ax, 1.30, 9.20, 1.10, 0.45, "#FFFFFF", edge_col="#64748B", lw=0.6, z=5)
    draw_rect(ax, 3.20, 9.15, 0.45, 0.50, "#FFFFFF", edge_col="#64748B", lw=0.6, z=5)

    draw_rect(ax, 3.95, 7.50, 2.35, 0.75, "#E0F2FE", edge_col="#0284C7", lw=0.7, z=5)
    draw_rect(ax, 3.90, 9.15, 0.45, 0.50, "#FFFFFF", edge_col="#64748B", lw=0.6, z=5)
    draw_rect(ax, 4.85, 9.20, 1.40, 0.45, "#FFFFFF", edge_col="#64748B", lw=0.7, z=5)

    # D. Master Suite PA
    draw_rect(ax, 1.95, 10.75, 2.00, 1.95, "#FFFFFF", edge_col="#94A3B8", lw=0.8, z=5)
    draw_rect(ax, 1.40, 12.60, 3.10, 0.15, "#C46D29", edge_col="#9A3412", z=6)
    draw_rect(ax, 4.70, 10.15, 0.65, 2.50, "#F8FAFC", edge_col="#78716C", lw=0.8, z=5)
    circ_b = patches.Circle((5.85, 11.40), 0.32, facecolor="#F1F5F9", edgecolor="#94A3B8", lw=0.5, zorder=6)
    ax.add_patch(circ_b)

    # E. Dormitorio 2 PA (Gran Suite Juvenil / Estudio 23 m²)
    draw_rect(ax, 7.20, 14.50, 1.80, 2.00, "#FFFFFF", edge_col="#94A3B8", lw=0.7, z=5)
    draw_rect(ax, 9.80, 13.50, 0.65, 3.20, "#F8FAFC", edge_col="#78716C", lw=0.7, z=5)
    draw_rect(ax, 7.00, 16.90, 2.40, 0.50, "#FFFFFF", edge_col="#64748B", lw=0.6, z=5)
    ax.text(8.20, 17.15, "ZONA ESTUDIO / TELETRABAJO (2,40 m)", ha='center', va='center', fontsize=4.5, color="#475569", zorder=6)

    # F. Dormitorio 3 PA
    draw_rect(ax, 3.70, 14.50, 1.60, 2.00, "#FFFFFF", edge_col="#94A3B8", lw=0.7, z=5)
    draw_rect(ax, 5.55, 14.20, 0.65, 2.40, "#F8FAFC", edge_col="#78716C", lw=0.7, z=5)
    draw_rect(ax, 3.50, 16.90, 1.60, 0.50, "#FFFFFF", edge_col="#64748B", lw=0.6, z=5)

    # G. Terraza Solárium Norte
    circ_t1 = patches.Circle((1.20, 15.20), 0.40, facecolor="#FEF3C7", edgecolor="#D97706", lw=0.6, zorder=4)
    circ_t2 = patches.Circle((2.20, 15.20), 0.40, facecolor="#FEF3C7", edgecolor="#D97706", lw=0.6, zorder=4)
    ax.add_patch(circ_t1); ax.add_patch(circ_t2)
    ax.text(1.70, 16.20, "SOLÁRIUM PRIVADO", ha='center', va='center', fontsize=5.0, weight='bold', color="#B45309", zorder=5)

    # 6. COTAS EXTERIORES
    y_s1, y_s2, y_s3 = -0.80, -1.55, -2.30
    draw_cota_arch_h(ax, -0.15, 2.60, y_s1, "2.75 m")
    draw_cota_arch_h(ax, 2.60, 4.40, y_s1, "1.80 (V)")
    draw_cota_arch_h(ax, 4.40, 4.80, y_s1, "0.40")
    draw_cota_arch_h(ax, 4.80, 6.00, y_s1, "1.20 (V)")
    draw_cota_arch_h(ax, 6.00, 6.90, y_s1, "0.90")
    draw_cota_arch_h(ax, 6.90, 8.10, y_s1, "1.20 (V)")
    draw_cota_arch_h(ax, 8.10, 8.90, y_s1, "0.80")
    draw_cota_arch_h(ax, 8.90, 9.90, y_s1, "1.00 (V)")
    draw_cota_arch_h(ax, 9.90, 11.45, y_s1, "1.55 (Escalera)")

    draw_cota_arch_h(ax, -0.15, 6.40, y_s2, "6.55 m (SALÓN)")
    draw_cota_arch_h(ax, 6.40, 11.45, y_s2, "5.05 m (COCINA / ACCESO)")
    draw_cota_arch_h(ax, -0.15, 11.45, y_s3, "11.60 m (ANCHURA TOTAL SOLAR)")

    # --- FACHADA NORTE ---
    y_n1, y_n2 = 18.25, 19.00
    draw_cota_arch_h(ax, -0.15, 0.80, y_n1, "0.95")
    draw_cota_arch_h(ax, 0.80, 2.40, y_n1, "1.60 (V)")
    draw_cota_arch_h(ax, 2.40, 3.60, y_n1, "1.20")
    draw_cota_arch_h(ax, 3.60, 5.20, y_n1, "1.60 (V)")
    draw_cota_arch_h(ax, 5.20, 7.00, y_n1, "1.80")
    draw_cota_arch_h(ax, 7.00, 9.00, y_n1, "2.00 (V)")
    draw_cota_arch_h(ax, 9.00, 9.80, y_n1, "0.80")
    draw_cota_arch_h(ax, 9.80, 11.00, y_n1, "1.20 (V)")
    draw_cota_arch_h(ax, 11.00, 11.45, y_n1, "0.45")
    draw_cota_arch_h(ax, -0.15, 11.45, y_n2, "11.60 m (FACHADA NORTE)")

    # --- LATERALES ---
    x_o1, x_o2 = -0.80, -1.60
    draw_cota_arch_v(ax, -0.15, 7.35, x_o1, "7.50 m (Salón)")
    draw_cota_arch_v(ax, 7.35, 13.75, x_o1, "6.40 m (Suite/Pasillo)")
    draw_cota_arch_v(ax, 13.75, 17.60, x_o1, "3.85 m (Terraza Solárium)")
    draw_cota_arch_v(ax, -0.15, 17.60, x_o2, "17.75 m (LONGITUD TOTAL)")

    x_e1, x_e2 = 12.00, 12.85
    draw_cota_arch_v(ax, -0.15, 5.00, x_e1, "5.15 m (Cocina + Escalera)")
    draw_cota_arch_v(ax, 5.00, 7.40, x_e1, "2.40 m (Salón sobre porche)")
    draw_cota_arch_v(ax, 7.40, 13.00, x_e1, "5.60 m (Vacío Patio)")
    draw_cota_arch_v(ax, 13.00, 17.60, x_e1, "4.60 m (Dormitorio 2)")
    draw_cota_arch_v(ax, -0.15, 17.60, x_e2, "17.75 m (MEDIANERA ESTE)")

    # 7. COTAS INTERIORES EXACTAS
    draw_cota_arch_h(ax, 0.15, 6.35, 6.40, "6.20 m libres")
    draw_cota_arch_v(ax, 0.15, 7.35, 5.90, "7.20 m libres")
    draw_cota_arch_h(ax, 6.45, 11.25, 6.40, "4.80 m (Sobre porche)")
    draw_cota_arch_h(ax, 6.45, 10.35, 4.60, "3.90 m")
    draw_cota_arch_v(ax, 0.15, 4.95, 10.00, "4.80 m")

    draw_cota_arch_h(ax, 1.25, 3.72, 8.85, "2.47 m")
    draw_cota_arch_v(ax, 7.45, 9.75, 1.45, "2.30 m")
    draw_cota_arch_h(ax, 3.88, 6.30, 8.85, "2.42 m")
    draw_cota_arch_v(ax, 7.45, 9.75, 6.10, "2.30 m")

    draw_cota_arch_h(ax, 1.25, 6.30, 12.45, "5.05 m libres (SUITE PA)")
    draw_cota_arch_v(ax, 9.85, 12.75, 0.35, "2.90 m fondo")

    draw_cota_arch_h(ax, 6.50, 11.25, 13.40, "4.75 m")
    draw_cota_arch_v(ax, 13.00, 17.45, 6.65, "4.45 m (Dorm. 2)")

    draw_cota_arch_h(ax, 3.25, 6.30, 17.10, "3.05 m")
    draw_cota_arch_v(ax, 13.85, 17.45, 3.45, "3.60 m (Dorm. 3)")

    # 8. ETIQUETAS DE ESTANCIAS
    draw_room_badge(ax, 3.40, 4.80, "GRAN SALÓN - COMEDOR", "48,20 m²", "Porcelánico rect.")
    draw_room_badge(ax, 8.40, 3.60, "COCINA CON ISLA", "18,72 m²", "Porcelánico rect.")
    draw_room_badge(ax, 2.50, 8.35, "BAÑO COMÚN", "5,68 m²", "Antideslizante")
    draw_room_badge(ax, 5.10, 8.35, "BAÑO EN SUITE", "5,57 m²", "Antideslizante")
    draw_room_badge(ax, 2.95, 10.25, "MASTER SUITE (D1)", "15,10 m²", "Tarima AC5 / Porc.")
    draw_room_badge(ax, 8.80, 15.20, "DORMITORIO 2 (SUITE)", "21,14 m²", "Tarima AC5 / Porc.")
    draw_room_badge(ax, 4.80, 15.20, "DORMITORIO 3", "11,00 m²", "Tarima AC5 / Porc.")
    draw_room_badge(ax, 1.60, 15.20, "TERRAZA SOLÁRIUM", "12,16 m²", "Deck madera C3")

    ax.text(0.60, 10.20, "PASILLO NOCHE (1,20 m libre) · S.U. = 7,32 m²",
            ha='center', va='center', fontsize=5.8, color=C_TEXT_SEC, rotation=90,
            bbox=dict(boxstyle='square,pad=0.08', facecolor='#FFFFFF', edgecolor='none', alpha=0.85))

    draw_north_arrow(ax, -3.50, 16.20)

    # Escala Gráfica
    sg_x, sg_y = -4.50, 13.00
    draw_rect(ax, sg_x, sg_y, 2.0, 0.15, "#000000", edge_col="#000000", lw=0.5, z=30)
    draw_rect(ax, sg_x + 1.0, sg_y, 1.0, 0.15, "#FFFFFF", edge_col="#000000", lw=0.5, z=30)
    ax.text(sg_x, sg_y - 0.22, "0", ha='center', va='top', fontsize=5.8, weight='bold', color=C_TEXT_MAIN)
    ax.text(sg_x + 1.0, sg_y - 0.22, "1 m", ha='center', va='top', fontsize=5.8, weight='bold', color=C_TEXT_MAIN)
    ax.text(sg_x + 2.0, sg_y - 0.22, "2 m", ha='center', va='top', fontsize=5.8, weight='bold', color=C_TEXT_MAIN)
    ax.text(sg_x + 1.0, sg_y + 0.30, "ESCALA GRÁFICA 1:50", ha='center', va='bottom', fontsize=6.2, weight='bold', color=C_TEXT_MAIN)

    # Cuadro de Superficies Planta Alta
    cs_x, cs_y, cs_w, cs_h = -4.80, 0.80, 2.80, 10.20
    draw_rect(ax, cs_x, cs_y, cs_w, cs_h, "#FFFFFF", edge_col=C_WALL, lw=0.9, z=30)
    draw_rect(ax, cs_x, cs_y + cs_h - 0.50, cs_w, 0.50, C_WALL, edge_col=C_WALL, z=31)
    ax.text(cs_x + cs_w/2, cs_y + cs_h - 0.25, "SUPERFICIES PLANTA ALTA", ha='center', va='center', fontsize=6.5, weight='bold', color="#FFFFFF", zorder=32)

    cuadro_pa = [
        ("Salón-Comedor", "48,20 m²"),
        ("Cocina con Isla", "18,72 m²"),
        ("Master Suite (D1)", "15,10 m²"),
        ("Baño en Suite", "5,57 m²"),
        ("Baño Común", "5,68 m²"),
        ("Dormitorio 2 (Ext)", "21,14 m²"),
        ("Dormitorio 3", "11,00 m²"),
        ("Pasillo Distrib.", "7,32 m²"),
        ("Desembarco Esc.", "4,50 m²"),
        ("---", "---"),
        ("TOTAL CERRADA", "137,23 m²"),
        ("Terraza Solárium", "12,16 m²"),
        ("Vacío Patio (PB)", "28,00 m²"),
        ("TOTAL EXTERIOR", "12,16 m²"),
        ("=== ", "=== "),
        ("SUP. CONSTRUIDA", "154,60 m²"),
    ]

    iy = cs_y + cs_h - 0.85
    for nombre, sup in cuadro_pa:
        if nombre.startswith("---") or nombre.startswith("==="):
            ax.plot([cs_x + 0.15, cs_x + cs_w - 0.15], [iy, iy], color="#94A3B8", lw=0.5, zorder=32)
            iy -= 0.22
            continue
        is_bold = "TOTAL" in nombre or "CONSTRUIDA" in nombre
        col = C_DIM if is_bold else C_TEXT_MAIN
        fs = 6.0 if is_bold else 5.2
        ax.text(cs_x + 0.15, iy, nombre, ha='left', va='center', fontsize=fs, weight='bold' if is_bold else 'normal', color=col, zorder=32)
        ax.text(cs_x + cs_w - 0.15, iy, sup, ha='right', va='center', fontsize=fs, weight='bold' if is_bold else 'normal', color=col, zorder=32)
        iy -= 0.50

    # Cajetín Oficial
    caj_x, caj_y, caj_w, caj_h = -4.80, -4.90, 21.80, 1.70
    draw_rect(ax, caj_x, caj_y, caj_w, caj_h, "#FFFFFF", edge_col=C_WALL, lw=1.3, z=40)
    ax.plot([caj_x + 6.8, caj_x + 6.8], [caj_y, caj_y + caj_h], color=C_WALL, lw=0.8, zorder=41)
    ax.plot([caj_x + 15.0, caj_x + 15.0], [caj_y, caj_y + caj_h], color=C_WALL, lw=0.8, zorder=41)
    ax.plot([caj_x + 18.6, caj_x + 18.6], [caj_y, caj_y + caj_h], color=C_WALL, lw=0.8, zorder=41)

    ax.text(caj_x + 0.30, caj_y + 1.25, "PROYECTO RESIDENCIAL BIFAMILIAR", fontsize=10.5, weight='bold', color=C_TEXT_MAIN, zorder=42)
    ax.text(caj_x + 0.30, caj_y + 0.85, "Vivienda Unifamiliar en Parcela Pasante con Patio y Piscina", fontsize=7.2, color=C_TEXT_SEC, zorder=42)
    ax.text(caj_x + 0.30, caj_y + 0.45, "Calle Moreno Torroba s/n · Palma del Río (Córdoba)", fontsize=7.2, weight='bold', color="#1E40AF", zorder=42)

    ax.text(caj_x + 7.10, caj_y + 1.25, "PLANO: PLANTA ALTA (VIVIENDA B) AMUEBLADA Y ACOTADA", fontsize=9.0, weight='bold', color=C_TEXT_MAIN, zorder=42)
    ax.text(caj_x + 7.10, caj_y + 0.85, "Distribución Ejecutiva · 3 Dormitorios, 2 Baños, Gran Salón y Terraza Solárium", fontsize=6.8, color=C_TEXT_SEC, zorder=42)
    ax.text(caj_x + 7.10, caj_y + 0.45, "Superficie Útil Cerrada: 137,23 m² | Exterior: 12,16 m² | Constr.: 154,60 m²", fontsize=6.8, weight='bold', color=C_TEXT_MAIN, zorder=42)

    ax.text(caj_x + 15.30, caj_y + 1.25, "ESCALA: 1:50 (A3)", fontsize=8.5, weight='bold', color=C_TEXT_MAIN, zorder=42)
    ax.text(caj_x + 15.30, caj_y + 0.85, "FECHA: Octubre 2026", fontsize=7.0, color=C_TEXT_SEC, zorder=42)
    ax.text(caj_x + 15.30, caj_y + 0.45, "FORMATO: DIN A3", fontsize=6.8, color=C_TEXT_SEC, zorder=42)

    draw_rect(ax, caj_x + 18.6, caj_y, 3.20, caj_h, C_WALL, edge_col=C_WALL, z=41)
    ax.text(caj_x + 20.20, caj_y + 1.10, "PLANO Nº", ha='center', va='center', fontsize=7.5, weight='bold', color="#94A3B8", zorder=42)
    ax.text(caj_x + 20.20, caj_y + 0.55, "P-02", ha='center', va='center', fontsize=18, weight='bold', color="#FFFFFF", zorder=42)

    out_file = os.path.join(OUTPUT_DIR, "02_plano_arquitecto_planta_alta.png")
    out_pdf  = os.path.join(OUTPUT_DIR, "02_plano_arquitecto_planta_alta.pdf")
    plt.savefig(out_file, bbox_inches='tight', dpi=300)
    plt.savefig(out_pdf, bbox_inches='tight')
    plt.close(fig)
    print(f"PLANO PLANTA ALTA GENERADO: {out_file}")

generar_planta_alta()
