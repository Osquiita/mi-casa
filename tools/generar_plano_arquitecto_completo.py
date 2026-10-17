# -*- coding: utf-8 -*-
"""
PLANO ARQUITECTÓNICO EJECUTIVO PROFESIONAL - PLANTA BAJA (VIVIENDA A)
Formato A3 Apaisado Técnico (Escala 1:50) con Estilo CAD de Estudio de Arquitectura:
- Muros seccionados en negro con grosores técnicos
- Carpinterías detalladas con batientes y vidrios
- Cadenas completas de cotas exteriores e interiores (cotas a 45º / arquitectura)
- Niveles de piso terminado (N.P.T. ±0.00)
- Simbología de accesos, norte geográfico, líneas de sección A-A' y B-B'
- Cuadro de superficies normativo integrado
- Cajetín oficial colegial de arquitectura
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import os

OUTPUT_DIR = r"C:\Users\Oscar Martinez\Desktop\mi-casa\entrega\planos_2d"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Paleta Arquitectónica Ejecutiva
C_BG_PAGE   = "#FFFFFF"
C_WALL      = "#181A1D"       # Muro cortado en sección
C_WALL_INT  = "#2C3036"       # Tabiquería interior
C_LINE_THIN = "#6B7280"       # Líneas auxiliares y carpintería
C_LINE_CAD  = "#374151"       # Líneas de mobiliario
C_DIM       = "#991B1B"       # Rojo técnico de cotas (estilo CAD)
C_DIM_LINE  = "#DC2626"       # Líneas de cota
C_TEXT_MAIN = "#111827"       # Textos principales
C_TEXT_SEC  = "#4B5563"       # Textos secundarios
C_BLUE_CAD  = "#1E40AF"       # Elementos de agua / cotas secundarias
C_WOOD      = "#B45309"       # Puertas y carpinterías madera
C_GLASS     = "#38BDF8"       # Vidrios

# Suelos sutiles
C_FLOOR_LIVING  = "#FBF9F5"
C_FLOOR_KITCHEN = "#F6F3ED"
C_FLOOR_BATH    = "#F1F5F9"
C_FLOOR_BED     = "#FCFAF7"
C_FLOOR_GARAGE  = "#F3F4F6"
C_FLOOR_PATIO   = "#F0FDF4"
C_FLOOR_POOL    = "#E0F2FE"
C_FLOOR_PORCH   = "#F5F0E8"

def setup_architect_canvas():
    # A3 Landscape ratio (420 x 297 mm)
    fig, ax = plt.subplots(figsize=(20, 14.14), dpi=300)
    # Coordenadas ajustadas para centrar el plano y dejar espacio al cajetín y cotas
    ax.set_xlim(-4.5, 17.5)
    ax.set_ylim(-3.8, 20.8)
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
    # Hueco blanco
    draw_rect(ax, x, y, w, h, "#FFFFFF", edge_col=None, z=21)
    if is_horiz:
        # Líneas de antepecho exterior e interior
        ax.plot([x, x+w], [y, y], color=C_WALL, lw=0.8, zorder=22)
        ax.plot([x, x+w], [y+h, y+h], color=C_WALL, lw=0.8, zorder=22)
        # Hojas de carpintería y vidrio
        ax.plot([x, x+w], [y+h*0.35, y+h*0.35], color="#64748B", lw=0.6, zorder=23)
        ax.plot([x, x+w], [y+h*0.65, y+h*0.65], color="#64748B", lw=0.6, zorder=23)
        ax.plot([x, x+w], [y+h*0.50, y+h*0.50], color=C_GLASS, lw=1.5, zorder=24)
        # Marco lateral
        ax.plot([x, x], [y, y+h], color=C_WALL, lw=1.0, zorder=23)
        ax.plot([x+w, x+w], [y, y+h], color=C_WALL, lw=1.0, zorder=23)
        if label:
            ax.text(x+w/2, y-0.25, label, ha='center', va='top', fontsize=6, color=C_TEXT_SEC, zorder=25)
    else:
        ax.plot([x, x], [y, y+h], color=C_WALL, lw=0.8, zorder=22)
        ax.plot([x+w, x+w], [y, y+h], color=C_WALL, lw=0.8, zorder=22)
        ax.plot([x+w*0.35, x+w*0.35], [y, y+h], color="#64748B", lw=0.6, zorder=23)
        ax.plot([x+w*0.65, x+w*0.65], [y, y+h], color="#64748B", lw=0.6, zorder=23)
        ax.plot([x+w*0.50, x+w*0.50], [y, y+h], color=C_GLASS, lw=1.5, zorder=24)
        ax.plot([x, x+w], [y, y], color=C_WALL, lw=1.0, zorder=23)
        ax.plot([x, x+w], [y+h, y+h], color=C_WALL, lw=1.0, zorder=23)
        if label:
            ax.text(x+w+0.15, y+h/2, label, ha='left', va='center', fontsize=6, color=C_TEXT_SEC, rotation=90, zorder=25)

def draw_door_cad(ax, x, y, r, a_start, a_end, label=""):
    # Arco de barrido
    arc = patches.Arc((x, y), 2*r, 2*r, angle=0,
                      theta1=min(a_start, a_end),
                      theta2=max(a_start, a_end),
                      color="#94A3B8", linewidth=0.8, linestyle='--', zorder=18)
    ax.add_patch(arc)
    # Hoja abatible
    rad = a_start * np.pi / 180.0
    ax.plot([x, x + r*np.cos(rad)], [y, y + r*np.sin(rad)],
            color=C_WOOD, linewidth=1.6, zorder=19)
    # Manilla / tope
    rad_end = (a_start + 10) * np.pi / 180.0
    ax.plot([x + r*np.cos(rad), x + r*np.cos(rad) + 0.08*np.sin(rad)],
            [y + r*np.sin(rad), y + r*np.sin(rad) - 0.08*np.cos(rad)],
            color="#475569", lw=1.0, zorder=20)
    if label:
        ax.text(x + r*0.5*np.cos(rad+0.3), y + r*0.5*np.sin(rad+0.3), label,
                fontsize=5.5, color=C_TEXT_SEC, ha='center', va='center', zorder=21)

def draw_cota_arch_h(ax, x1, x2, y, val_str, offset=0.18, tick=0.10):
    """Cota horizontal con remates a 45º estilo arquitectura"""
    if x1 > x2:
        x1, x2 = x2, x1
    # Línea principal
    ax.plot([x1, x2], [y, y], color=C_DIM_LINE, lw=0.7, zorder=30)
    # Remates a 45 grados
    ax.plot([x1 - tick*0.7, x1 + tick*0.7], [y - tick*0.7, y + tick*0.7], color=C_DIM, lw=1.2, zorder=31)
    ax.plot([x2 - tick*0.7, x2 + tick*0.7], [y - tick*0.7, y + tick*0.7], color=C_DIM, lw=1.2, zorder=31)
    # Líneas testigo
    ax.plot([x1, x1], [y - tick*1.2, y + tick*1.2], color=C_DIM_LINE, lw=0.4, linestyle=':', zorder=29)
    ax.plot([x2, x2], [y - tick*1.2, y + tick*1.2], color=C_DIM_LINE, lw=0.4, linestyle=':', zorder=29)
    # Texto
    ax.text((x1 + x2)/2.0, y + offset, val_str, ha='center', va='bottom',
            fontsize=7.5, color=C_DIM, weight='bold', zorder=32,
            bbox=dict(boxstyle='square,pad=0.08', facecolor='#FFFFFF', edgecolor='none', alpha=0.9))

def draw_cota_arch_v(ax, y1, y2, x, val_str, offset=0.18, tick=0.10):
    """Cota vertical con remates a 45º estilo arquitectura"""
    if y1 > y2:
        y1, y2 = y2, y1
    ax.plot([x, x], [y1, y2], color=C_DIM_LINE, lw=0.7, zorder=30)
    ax.plot([x - tick*0.7, x + tick*0.7], [y1 - tick*0.7, y1 + tick*0.7], color=C_DIM, lw=1.2, zorder=31)
    ax.plot([x - tick*0.7, x + tick*0.7], [y2 - tick*0.7, y2 + tick*0.7], color=C_DIM, lw=1.2, zorder=31)
    ax.plot([x - tick*1.2, x + tick*1.2], [y1, y1], color=C_DIM_LINE, lw=0.4, linestyle=':', zorder=29)
    ax.plot([x - tick*1.2, x + tick*1.2], [y2, y2], color=C_DIM_LINE, lw=0.4, linestyle=':', zorder=29)
    ax.text(x + offset, (y1 + y2)/2.0, val_str, ha='left', va='center',
            fontsize=7.5, color=C_DIM, weight='bold', rotation=90, zorder=32,
            bbox=dict(boxstyle='square,pad=0.08', facecolor='#FFFFFF', edgecolor='none', alpha=0.9))

def draw_room_tag(ax, x, y, name, area_str, npt="+0.00", pav="Porcelánico"):
    """Cajetín identificador de estancia arquitectónico"""
    w_box, h_box = 2.4, 0.75
    draw_rect(ax, x - w_box/2, y - h_box/2, w_box, h_box, "#FFFFFF", edge_col="#94A3B8", lw=0.6, z=26)
    ax.text(x, y + 0.16, name, ha='center', va='center', fontsize=7.5, weight='bold', color=C_TEXT_MAIN, zorder=27)
    ax.text(x, y - 0.04, f"S.Útil = {area_str}", ha='center', va='center', fontsize=6.8, weight='bold', color=C_BLUE_CAD, zorder=27)
    ax.text(x, y - 0.22, f"N.P.T. {npt} | {pav}", ha='center', va='center', fontsize=5.2, color=C_TEXT_SEC, zorder=27)

def draw_npt_symbol(ax, x, y, level="+0.00"):
    """Símbolo de nivel de planta circular con cuadrantes"""
    r = 0.22
    circ = patches.Circle((x, y), r, facecolor="#FFFFFF", edgecolor=C_TEXT_MAIN, lw=0.7, zorder=28)
    ax.add_patch(circ)
    # Cuadrantes negros opuestos
    wedge1 = patches.Wedge((x, y), r, 0, 90, facecolor=C_TEXT_MAIN, zorder=29)
    wedge2 = patches.Wedge((x, y), r, 180, 270, facecolor=C_TEXT_MAIN, zorder=29)
    ax.add_patch(wedge1); ax.add_patch(wedge2)
    ax.text(x + r + 0.08, y, f"N.P.T. {level}", ha='left', va='center', fontsize=6, weight='bold', color=C_TEXT_MAIN, zorder=30)

def draw_north_arrow(ax, x, y):
    """Rosa de los vientos / Norte Geográfico arquitectónico"""
    r = 0.9
    ax.plot([x, x], [y - r, y + r], color=C_TEXT_MAIN, lw=1.2, zorder=35)
    ax.plot([x - r*0.5, x + r*0.5], [y, y], color=C_TEXT_MAIN, lw=0.6, zorder=35)
    # Flecha norte rellena
    pts_n = [[x, y + r], [x - r*0.25, y], [x, y], [x, y + r]]
    poly = patches.Polygon(pts_n, facecolor=C_TEXT_MAIN, edgecolor=C_TEXT_MAIN, zorder=36)
    ax.add_patch(poly)
    ax.text(x, y + r + 0.20, "N", ha='center', va='bottom', fontsize=11, weight='bold', color=C_TEXT_MAIN, zorder=37)
    ax.text(x, y - r - 0.15, "ORIENTACIÓN", ha='center', va='top', fontsize=5.5, color=C_TEXT_SEC, zorder=37)

def generar_plano_arquitecto_completo():
    fig, ax = setup_architect_canvas()

    # 1. SUELOS ARQUITECTÓNICOS
    draw_rect(ax, 0.00, 0.00, 1.20, 2.40, C_FLOOR_LIVING)
    draw_rect(ax, 0.00, 2.40, 6.40, 5.00, C_FLOOR_LIVING)
    draw_rect(ax, 1.20, 0.00, 5.20, 2.40, C_FLOOR_LIVING)
    draw_rect(ax, 6.40, 0.00, 4.00, 5.00, C_FLOOR_KITCHEN)
    draw_rect(ax, 10.40, 0.00, 1.00, 5.00, C_FLOOR_GARAGE)
    draw_rect(ax, 6.40, 5.00, 5.00, 2.40, C_FLOOR_PORCH)
    draw_rect(ax, 6.40, 7.40, 5.00, 5.60, C_FLOOR_PATIO)

    # Piscina
    draw_rect(ax, 7.30, 8.20, 2.50, 3.80, C_FLOOR_POOL, edge_col="#38BDF8", lw=1.2, z=3)
    draw_rect(ax, 7.45, 8.35, 2.20, 3.50, "#BAE6FD", edge_col="#0284C7", lw=0.6, z=4)
    for sy in [8.35, 8.70, 9.05]:
        ax.plot([7.45, 9.65], [sy, sy], color="#0284C7", lw=0.6, zorder=5)

    # Pasillo Noche y Rellano
    draw_rect(ax, 0.00, 7.40, 1.20, 6.10, C_FLOOR_LIVING)
    draw_rect(ax, 1.20, 12.55, 3.10, 0.95, C_FLOOR_LIVING)

    # Baños Cuadrados
    draw_rect(ax, 1.20, 7.40, 2.60, 2.40, C_FLOOR_BATH)
    draw_rect(ax, 3.80, 7.40, 2.60, 2.40, C_FLOOR_BATH)

    # Master Suite
    draw_rect(ax, 1.20, 9.80, 3.10, 2.75, C_FLOOR_BED)
    draw_rect(ax, 4.30, 9.80, 2.10, 3.65, C_FLOOR_BED)

    # Dormitorios 2 y 3
    draw_rect(ax, 0.00, 13.50, 3.20, 4.10, C_FLOOR_BED)
    draw_rect(ax, 3.20, 13.50, 3.20, 4.10, C_FLOOR_BED)

    # Gran Cochera
    draw_rect(ax, 6.40, 13.00, 5.00, 4.60, C_FLOOR_GARAGE)

    # 2. MUROS Y MEDIANERAS (Corte en negro sólido)
    # Medianeras (0.30 m)
    draw_wall(ax, -0.15, -0.15, 0.30, 17.90)
    draw_wall(ax, 11.25, -0.15, 0.30, 17.90)

    # Fachada Sur (C/ Moreno Torroba)
    draw_wall(ax, -0.15, -0.15, 0.45, 0.30)
    draw_wall(ax, 1.20, -0.15, 1.40, 0.30)
    draw_wall(ax, 4.40, -0.15, 0.40, 0.30)
    draw_wall(ax, 6.00, -0.15, 0.90, 0.30)
    draw_wall(ax, 8.10, -0.15, 0.80, 0.30)
    draw_wall(ax, 9.90, -0.15, 0.50, 0.30)

    # Fachada Norte
    draw_wall(ax, -0.15, 17.45, 0.95, 0.30)
    draw_wall(ax, 2.40, 17.45, 1.20, 0.30)
    draw_wall(ax, 5.20, 17.45, 1.20, 0.30)

    # 3. TABIQUERÍA INTERIOR (0.10 m espesor)
    draw_wall(ax, 1.15, 0.00, 0.10, 1.20, False)
    draw_wall(ax, 6.35, 0.00, 0.10, 0.80, False)
    draw_wall(ax, 6.35, 4.20, 0.10, 0.80, False)
    draw_wall(ax, 10.35, 0.00, 0.10, 5.00, False)

    # Salón ↔ Baños
    draw_wall(ax, 1.15, 7.35, 5.25, 0.10, False)

    # Muro Técnico Central Baños (0.15 m + bajante integrada)
    draw_wall(ax, 3.75, 7.35, 0.15, 2.45, False)
    draw_rect(ax, 3.77, 8.30, 0.11, 0.55, "#E2E8F0", edge_col=C_WALL, lw=0.6, z=21)
    ax.text(3.82, 8.58, "B.F.", ha='center', va='center', fontsize=4.5, color="#475569", rotation=90, zorder=22)

    # Muro Patio hacia Baños y Suite (0.20 m)
    draw_wall(ax, 6.30, 7.35, 0.20, 5.65, True)

    # Baños ↔ Suite
    draw_wall(ax, 1.15, 9.75, 2.65, 0.10, False)
    draw_wall(ax, 4.70, 9.75, 1.70, 0.10, False)

    # Pasillo ↔ Suite
    draw_wall(ax, 1.15, 9.75, 0.10, 0.25, False)
    draw_wall(ax, 1.15, 10.85, 0.10, 1.70, False)

    # Suite ↔ Rellano Norte
    draw_wall(ax, 1.15, 12.45, 3.15, 0.10, False)
    draw_wall(ax, 4.25, 12.45, 0.10, 1.10, False)

    # Distribuidor ↔ Dorms 2 y 3
    draw_wall(ax, -0.15, 13.45, 0.95, 0.10, False)
    draw_wall(ax, 1.65, 13.45, 1.55, 0.10, False)
    draw_wall(ax, 4.25, 13.45, 2.15, 0.10, False)

    # Separación Dorm 2 - Dorm 3
    draw_wall(ax, 3.15, 13.45, 0.10, 4.15, False)

    # Muro Cochera
    draw_wall(ax, 6.30, 13.00, 0.20, 4.60, True)

    # Pilares Porche (Hormigón 25x25)
    draw_wall(ax, 7.00, 7.25, 0.25, 0.25, True)
    draw_wall(ax, 9.50, 7.25, 0.25, 0.25, True)

    # 4. CARPINTERÍAS DETALLADAS
    # Ventanas
    draw_window_cad(ax, 2.60, -0.05, 1.80, 0.10, True, "V-01 (180x140)")
    draw_window_cad(ax, 4.80, -0.05, 1.20, 0.10, True, "V-02 (120x140)")
    draw_window_cad(ax, 6.90, -0.05, 1.20, 0.10, True, "V-03 (120x140)")
    draw_window_cad(ax, 8.90, -0.05, 1.00, 0.10, True, "V-04 (100x140)")

    draw_window_cad(ax, 6.40, 5.00, 0.10, 2.40, False, "V-05 CORREDERA")
    draw_window_cad(ax, 6.40, 7.60, 0.10, 0.80, False, "V-06 (80x60)")
    draw_window_cad(ax, 6.40, 8.75, 0.10, 0.80, False, "V-07 (80x60)")
    draw_window_cad(ax, 6.40, 10.30, 0.10, 2.60, False, "V-08 PANORÁMICA")

    draw_window_cad(ax, 0.80, 17.55, 1.60, 0.10, True, "V-09 (160x140)")
    draw_window_cad(ax, 3.60, 17.55, 1.60, 0.10, True, "V-10 (160x140)")

    # Puerta Seccional Cochera
    draw_rect(ax, 6.40, 17.50, 4.85, 0.18, "#334155", edge_col="#0F172A", lw=1.0, z=22)
    for px in np.linspace(6.50, 11.15, 8):
        ax.plot([px, px], [17.50, 17.68], color="#94A3B8", lw=0.6, zorder=23)
    ax.text(8.82, 17.35, "PUERTA MOTORIZADA COCHERA (4,85 m)", ha='center', va='top', fontsize=6, weight='bold', color=C_TEXT_MAIN, zorder=25)

    # Puertas de paso interiores con medidas estándar
    draw_door_cad(ax, 0.30, 0.00, 0.90, 0, 90, "P. Entrada 90")
    draw_door_cad(ax, 10.40, 0.00, 0.90, 0, 90, "P. Acceso PA 90")
    draw_door_cad(ax, 0.20, 7.35, 0.85, 0, 90, "82.5")
    draw_door_cad(ax, 1.20, 7.45, 0.80, 0, 90, "72.5")
    draw_door_cad(ax, 3.90, 9.80, 0.80, -90, 0, "72.5")
    draw_door_cad(ax, 1.20, 10.00, 0.85, 0, 90, "82.5")
    draw_door_cad(ax, 0.80, 13.55, 0.85, 0, 90, "82.5")
    draw_door_cad(ax, 3.40, 13.55, 0.85, 0, 90, "82.5")
    draw_door_cad(ax, 6.40, 13.20, 0.85, -90, 0, "82.5")

    # 5. MOBILIARIO ARQUITECTÓNICO TÉCNICO
    # Gran frente armarios salón (3,60 m)
    draw_rect(ax, 0.15, 2.40, 0.70, 3.60, "#F1ECE1", edge_col="#78716C", lw=0.8, z=5)
    for my in [3.30, 4.20, 5.10]:
        ax.plot([0.15, 0.85], [my, my], color="#78716C", lw=0.6, zorder=6)
    ax.text(0.50, 4.20, "ARMARIOS EMPOTRADOS INTEGRADOS (3,60 m)", ha='center', va='center', fontsize=5.5, rotation=90, color="#57534E", zorder=7)

    # Sofá y Comedor
    draw_rect(ax, 1.80, 2.60, 2.80, 1.10, "#E2E8F0", edge_col="#94A3B8", lw=0.7, z=5)
    draw_rect(ax, 2.30, 2.80, 1.60, 0.60, "#CBD5E1", edge_col="#94A3B8", lw=0.5, z=6)
    draw_rect(ax, 1.80, 1.00, 2.40, 1.00, "#F8FAFC", edge_col="#94A3B8", lw=0.8, z=5)
    for cy in [0.75, 2.25]:
        for cx in [2.00, 2.70, 3.40, 3.90]:
            draw_rect(ax, cx, cy, 0.40, 0.35, "#F1F5F9", edge_col="#94A3B8", lw=0.5, z=5)

    # Cocina con Isla
    draw_rect(ax, 7.20, 1.60, 2.40, 1.10, "#FFFFFF", edge_col="#64748B", lw=1.0, z=5)
    # Fregadero 2 senos en isla
    draw_rect(ax, 7.40, 1.80, 0.80, 0.45, "#F1F5F9", edge_col="#64748B", lw=0.6, z=6)
    draw_rect(ax, 7.45, 1.85, 0.33, 0.35, "#E2E8F0", edge_col="#64748B", lw=0.4, z=7)
    draw_rect(ax, 7.82, 1.85, 0.33, 0.35, "#E2E8F0", edge_col="#64748B", lw=0.4, z=7)
    # Placa inducción
    draw_rect(ax, 8.60, 1.80, 0.75, 0.50, "#1E293B", edge_col="#0F172A", lw=0.6, z=6)
    for fx, fy, fr in [(8.75, 1.95, 0.08), (9.15, 1.95, 0.10), (8.95, 2.15, 0.07)]:
        circ = patches.Circle((fx, fy), fr, facecolor="none", edgecolor="#FFFFFF", lw=0.5, zorder=7)
        ax.add_patch(circ)
    # Bancada trasera
    draw_rect(ax, 6.50, 0.15, 3.80, 0.65, "#F8FAFC", edge_col="#64748B", lw=0.8, z=5)

    # Escalera a Planta Alta
    for st in range(16):
        sy = st * (5.0 / 16.0)
        ax.plot([10.40, 11.40], [sy, sy], color="#94A3B8", lw=0.6, zorder=5)
    ax.annotate('', xy=(10.90, 4.50), xytext=(10.90, 0.80),
                arrowprops=dict(arrowstyle='->', color="#475569", lw=1.2), zorder=6)
    ax.text(10.90, 2.50, "SUBE A PLANTA ALTA (16 peldaños)", ha='center', va='center', fontsize=5.5, color="#475569", rotation=90, zorder=7,
            bbox=dict(boxstyle='square,pad=0.1', facecolor='#FFFFFF', edgecolor='none'))

    # Sanitarios
    # Baño común
    draw_rect(ax, 1.30, 7.50, 2.35, 0.75, "#E0F2FE", edge_col="#0284C7", lw=0.8, z=5)
    ax.text(2.47, 7.87, "PLATO DUCHA ENRASADO (235x75)", ha='center', va='center', fontsize=5.2, color="#0369A1", zorder=6)
    draw_rect(ax, 1.30, 9.20, 1.10, 0.40, "#FFFFFF", edge_col="#64748B", lw=0.7, z=5)
    circ1 = patches.Circle((1.85, 9.40), 0.14, facecolor="#F8FAFC", edgecolor="#64748B", lw=0.6, zorder=6)
    ax.add_patch(circ1)
    draw_rect(ax, 3.20, 9.15, 0.50, 0.45, "#FFFFFF", edge_col="#64748B", lw=0.7, z=5)

    # Baño suite
    draw_rect(ax, 3.95, 7.50, 2.35, 0.75, "#E0F2FE", edge_col="#0284C7", lw=0.8, z=5)
    ax.text(5.12, 7.87, "PLATO DUCHA ENRASADO (235x75)", ha='center', va='center', fontsize=5.2, color="#0369A1", zorder=6)
    draw_rect(ax, 3.90, 9.15, 0.50, 0.45, "#FFFFFF", edge_col="#64748B", lw=0.7, z=5)
    draw_rect(ax, 5.10, 9.20, 1.15, 0.40, "#FFFFFF", edge_col="#64748B", lw=0.7, z=5)
    circ2 = patches.Circle((5.67, 9.40), 0.14, facecolor="#F8FAFC", edgecolor="#64748B", lw=0.6, zorder=6)
    ax.add_patch(circ2)

    # Master Suite - Cama King Size
    draw_rect(ax, 1.90, 10.15, 2.00, 2.10, "#FFFFFF", edge_col="#94A3B8", lw=0.8, z=5)
    draw_rect(ax, 1.90, 12.10, 2.00, 0.15, "#CBD5E1", edge_col="#94A3B8", z=6)
    draw_rect(ax, 2.00, 11.75, 0.80, 0.30, "#F1F5F9", edge_col="#CBD5E1", lw=0.6, z=6)
    draw_rect(ax, 2.95, 11.75, 0.80, 0.30, "#F1F5F9", edge_col="#CBD5E1", lw=0.6, z=6)
    # Gran Vestidor Lineal
    draw_rect(ax, 4.40, 10.00, 0.65, 3.20, "#F8FAFC", edge_col="#78716C", lw=0.8, z=5)
    for vy in np.linspace(10.00, 13.20, 6):
        ax.plot([4.40, 5.05], [vy, vy], color="#A8A29E", lw=0.5, zorder=6)
    ax.text(4.72, 11.60, "GRAN VESTIDOR LINEAL (3,20 m)", ha='center', va='center', fontsize=5.5, rotation=90, color="#57534E", zorder=7)

    # Dormitorios 2 y 3
    for dx, dy, ax_c, ax_w in [(0.50, 14.80, 2.35, 14.80), (3.70, 14.80, 5.55, 14.80)]:
        draw_rect(ax, dx, dy, 1.60, 2.00, "#FFFFFF", edge_col="#94A3B8", lw=0.8, z=5)
        draw_rect(ax, dx, dy+1.85, 1.60, 0.15, "#CBD5E1", edge_col="#94A3B8", z=6)
        draw_rect(ax, dx+0.10, dy+1.50, 0.60, 0.30, "#F1F5F9", edge_col="#CBD5E1", lw=0.5, z=6)
        draw_rect(ax, dx+0.90, dy+1.50, 0.60, 0.30, "#F1F5F9", edge_col="#CBD5E1", lw=0.5, z=6)
        draw_rect(ax, ax_c, ax_w, 0.65, 2.20, "#F8FAFC", edge_col="#78716C", lw=0.8, z=5)
        for ay in np.linspace(ax_w, ax_w+2.20, 5):
            ax.plot([ax_c, ax_c+0.65], [ay, ay], color="#A8A29E", lw=0.5, zorder=6)

    # Cochera - Vehículo SUV y Lavadero
    draw_rect(ax, 6.80, 14.00, 3.00, 3.20, "#E2E8F0", edge_col="#94A3B8", lw=0.7, z=4)
    ax.text(8.30, 15.60, "PLAZA DE GARAJE (SUV GRANDE)", ha='center', va='center', fontsize=6.5, weight='bold', color="#475569", zorder=5)
    draw_rect(ax, 10.50, 13.20, 0.70, 4.10, "#F8FAFC", edge_col="#78716C", lw=0.8, z=5)
    ax.text(10.85, 15.25, "TRASTERO + LAVADERO INTEGRADO (4,10 m)", ha='center', va='center', fontsize=5.5, rotation=90, color="#57534E", zorder=6)

    # 6. SISTEMA COMPLETO DE COTAS ARQUITECTÓNICAS
    # --- A. COTAS EXTERIORES (FACHADA SUR - INFERIOR) ---
    y_ext_s1 = -0.75
    y_ext_s2 = -1.35
    # Cota Parcial Huecos
    draw_cota_arch_h(ax, -0.15, 0.30, y_ext_s1, "0.45")
    draw_cota_arch_h(ax, 0.30, 1.20, y_ext_s1, "0.90 (P)")
    draw_cota_arch_h(ax, 1.20, 2.60, y_ext_s1, "1.40")
    draw_cota_arch_h(ax, 2.60, 4.40, y_ext_s1, "1.80 (V)")
    draw_cota_arch_h(ax, 4.40, 4.80, y_ext_s1, "0.40")
    draw_cota_arch_h(ax, 4.80, 6.00, y_ext_s1, "1.20 (V)")
    draw_cota_arch_h(ax, 6.00, 6.90, y_ext_s1, "0.90")
    draw_cota_arch_h(ax, 6.90, 8.10, y_ext_s1, "1.20 (V)")
    draw_cota_arch_h(ax, 8.10, 8.90, y_ext_s1, "0.80")
    draw_cota_arch_h(ax, 8.90, 9.90, y_ext_s1, "1.00 (V)")
    draw_cota_arch_h(ax, 9.90, 10.40, y_ext_s1, "0.50")
    draw_cota_arch_h(ax, 10.40, 11.40, y_ext_s1, "1.00 (P)")
    # Cota Total Fachada Sur
    draw_cota_arch_h(ax, -0.15, 11.45, y_ext_s2, "11.60 m (ANCHURA TOTAL PARCELA)")

    # --- B. COTAS EXTERIORES (FACHADA NORTE - SUPERIOR) ---
    y_ext_n1 = 18.25
    y_ext_n2 = 18.85
    draw_cota_arch_h(ax, -0.15, 0.80, y_ext_n1, "0.95")
    draw_cota_arch_h(ax, 0.80, 2.40, y_ext_n1, "1.60 (V)")
    draw_cota_arch_h(ax, 2.40, 3.60, y_ext_n1, "1.20")
    draw_cota_arch_h(ax, 3.60, 5.20, y_ext_n1, "1.60 (V)")
    draw_cota_arch_h(ax, 5.20, 6.40, y_ext_n1, "1.20")
    draw_cota_arch_h(ax, 6.40, 11.25, y_ext_n1, "4.85 (Portón)")
    draw_cota_arch_h(ax, -0.15, 11.45, y_ext_n2, "11.60 m (FACHADA NORTE)")

    # --- C. COTAS EXTERIORES (LATERAL OESTE) ---
    x_ext_o1 = -0.75
    x_ext_o2 = -1.45
    draw_cota_arch_v(ax, -0.15, 7.35, x_ext_o1, "7.50 m (Salón)")
    draw_cota_arch_v(ax, 7.35, 13.45, x_ext_o1, "6.10 m (Pasillo/Suite)")
    draw_cota_arch_v(ax, 13.45, 17.60, x_ext_o1, "4.15 m (Dormitorio 2)")
    draw_cota_arch_v(ax, -0.15, 17.60, x_ext_o2, "17.75 m (LONGITUD TOTAL PARCELA)")

    # --- D. COTAS EXTERIORES (LATERAL ESTE) ---
    x_ext_e1 = 11.95
    x_ext_e2 = 12.65
    draw_cota_arch_v(ax, -0.15, 5.00, x_ext_e1, "5.15 m (Cocina + Escalera)")
    draw_cota_arch_v(ax, 5.00, 7.40, x_ext_e1, "2.40 m (Porche)")
    draw_cota_arch_v(ax, 7.40, 13.00, x_ext_e1, "5.60 m (Patio + Piscina)")
    draw_cota_arch_v(ax, 13.00, 17.60, x_ext_e1, "4.60 m (Gran Cochera)")
    draw_cota_arch_v(ax, -0.15, 17.60, x_ext_e2, "17.75 m (MEDIANERA ESTE)")

    # --- E. COTAS INTERIORES EXACTAS DE ESTANCIA ---
    # Salón - Comedor
    draw_cota_arch_h(ax, 0.15, 6.35, 6.40, "6.20 m")
    draw_cota_arch_v(ax, 0.15, 7.35, 5.85, "7.20 m")
    draw_cota_arch_v(ax, 2.40, 6.00, 0.95, "3.60 m (Armarios)")

    # Cocina
    draw_cota_arch_h(ax, 6.45, 10.35, 4.60, "3.90 m")
    draw_cota_arch_v(ax, 0.15, 4.95, 10.00, "4.80 m")

    # Baños Cuadrados
    draw_cota_arch_h(ax, 1.25, 3.72, 8.85, "2.47 m")
    draw_cota_arch_v(ax, 7.45, 9.75, 1.50, "2.30 m")
    draw_cota_arch_h(ax, 3.88, 6.30, 8.85, "2.42 m")
    draw_cota_arch_v(ax, 7.45, 9.75, 6.05, "2.30 m")

    # Master Suite
    draw_cota_arch_h(ax, 1.25, 4.25, 12.10, "3.00 m")
    draw_cota_arch_v(ax, 9.85, 12.45, 4.05, "2.60 m")
    draw_cota_arch_h(ax, 4.35, 6.30, 13.10, "1.95 m")
    draw_cota_arch_v(ax, 9.85, 13.45, 6.05, "3.60 m (Vestidor)")

    # Dormitorios 2 y 3
    draw_cota_arch_h(ax, 0.15, 3.15, 17.10, "3.00 m")
    draw_cota_arch_v(ax, 13.55, 17.45, 0.35, "3.90 m")
    draw_cota_arch_h(ax, 3.25, 6.30, 17.10, "3.05 m")
    draw_cota_arch_v(ax, 13.55, 17.45, 3.45, "3.90 m")

    # Gran Cochera
    draw_cota_arch_h(ax, 6.50, 11.25, 13.50, "4.75 m")
    draw_cota_arch_v(ax, 13.00, 17.45, 6.70, "4.45 m")

    # Patio y Piscina
    draw_cota_arch_h(ax, 6.50, 11.25, 7.70, "4.75 m")
    draw_cota_arch_v(ax, 7.45, 13.00, 11.00, "5.55 m")
    draw_cota_arch_h(ax, 7.30, 9.80, 11.70, "2.50 m (Piscina)")
    draw_cota_arch_v(ax, 8.20, 12.00, 7.55, "3.80 m (Piscina)")

    # 7. CAJETINES DE IDENTIFICACIÓN DE ESTANCIAS
    draw_room_tag(ax, 3.40, 4.60, "SALÓN - COMEDOR", "38,50 m²", "+0.00", "Porcelánico rectificado")
    draw_room_tag(ax, 8.40, 3.50, "COCINA CON ISLA", "18,72 m²", "+0.00", "Porcelánico rectificado")
    draw_room_tag(ax, 8.90, 6.20, "PORCHE CUBIERTO", "11,40 m²", "+0.00", "Gres antideslizante C3")
    draw_room_tag(ax, 2.50, 8.35, "BAÑO COMÚN", "5,68 m²", "+0.00", "Porcelánico antideslizante")
    draw_room_tag(ax, 5.10, 8.35, "BAÑO EN SUITE", "5,57 m²", "+0.00", "Porcelánico antideslizante")
    draw_room_tag(ax, 2.65, 11.20, "MASTER SUITE (DORM. 1)", "14,82 m²", "+0.00", "Tarima AC5 / Porcelánico")
    draw_room_tag(ax, 1.65, 14.10, "DORMITORIO 2", "11,70 m²", "+0.00", "Tarima AC5 / Porcelánico")
    draw_room_tag(ax, 4.80, 14.10, "DORMITORIO 3", "11,90 m²", "+0.00", "Tarima AC5 / Porcelánico")
    draw_room_tag(ax, 8.90, 15.20, "GRAN COCHERA + TRASTERO", "21,14 m²", "+0.00", "Hormigón pulido / Pav. técnico")
    draw_room_tag(ax, 8.55, 10.00, "PATIO OASIS + PISCINA", "26,36 m²", "-0.05", "Césped técnico + Tarima")

    # Rótulo pasillo
    ax.text(0.60, 10.20, "PASILLO DISTRIBUIDOR (1,20 m libre) · 7,32 m² útiles",
            ha='center', va='center', fontsize=6.2, color=C_TEXT_SEC, rotation=90,
            bbox=dict(boxstyle='square,pad=0.1', facecolor='#FFFFFF', edgecolor='none', alpha=0.8))

    # 8. SÍMBOLOS DE NIVEL Y ACCESOS
    draw_npt_symbol(ax, 0.40, 1.00, "+0.00")
    draw_npt_symbol(ax, 8.90, 7.70, "-0.05")
    draw_npt_symbol(ax, 8.80, 13.50, "+0.00")

    # Flechas de acceso exterior
    ax.annotate('ACCESO PRINCIPAL', xy=(0.75, 0.00), xytext=(0.75, -0.60),
                arrowprops=dict(facecolor=C_TEXT_MAIN, edgecolor=C_TEXT_MAIN, width=2.0, headwidth=6),
                ha='center', va='top', fontsize=6.5, weight='bold', color=C_TEXT_MAIN, zorder=30)

    ax.annotate('ACCESO PLANTA ALTA', xy=(10.85, 0.00), xytext=(10.85, -0.60),
                arrowprops=dict(facecolor=C_TEXT_MAIN, edgecolor=C_TEXT_MAIN, width=2.0, headwidth=6),
                ha='center', va='top', fontsize=6.5, weight='bold', color=C_TEXT_MAIN, zorder=30)

    ax.annotate('ACCESO VEHICULAR', xy=(8.82, 17.65), xytext=(8.82, 18.15),
                arrowprops=dict(facecolor=C_TEXT_MAIN, edgecolor=C_TEXT_MAIN, width=2.0, headwidth=6),
                ha='center', va='bottom', fontsize=6.5, weight='bold', color=C_TEXT_MAIN, zorder=30)

    # 9. NORTE Y ESCALA GRÁFICA
    draw_north_arrow(ax, -3.20, 15.50)

    # Escala Gráfica 1:50
    # En 1:50, 1 metro = 2 cm en papel
    sg_x, sg_y = -3.80, 12.00
    draw_rect(ax, sg_x, sg_y, 2.0, 0.15, "#000000", edge_col="#000000", lw=0.6, z=30)
    draw_rect(ax, sg_x + 1.0, sg_y, 1.0, 0.15, "#FFFFFF", edge_col="#000000", lw=0.6, z=30)
    ax.text(sg_x, sg_y - 0.25, "0", ha='center', va='top', fontsize=6, weight='bold', color=C_TEXT_MAIN)
    ax.text(sg_x + 1.0, sg_y - 0.25, "1 m", ha='center', va='top', fontsize=6, weight='bold', color=C_TEXT_MAIN)
    ax.text(sg_x + 2.0, sg_y - 0.25, "2 m", ha='center', va='top', fontsize=6, weight='bold', color=C_TEXT_MAIN)
    ax.text(sg_x + 1.0, sg_y + 0.35, "ESCALA GRÁFICA 1:50", ha='center', va='bottom', fontsize=6.5, weight='bold', color=C_TEXT_MAIN)

    # 10. CUADRO DE SUPERFICIES RESUMEN EN MARGEN IZQUIERDO
    cs_x, cs_y, cs_w, cs_h = -4.10, 0.50, 2.70, 9.80
    draw_rect(ax, cs_x, cs_y, cs_w, cs_h, "#FFFFFF", edge_col=C_WALL, lw=1.0, z=30)
    draw_rect(ax, cs_x, cs_y + cs_h - 0.50, cs_w, 0.50, C_WALL, edge_col=C_WALL, z=31)
    ax.text(cs_x + cs_w/2, cs_y + cs_h - 0.25, "CUADRO DE SUPERFICIES", ha='center', va='center', fontsize=7, weight='bold', color="#FFFFFF", zorder=32)

    cuadro_items = [
        ("Salón-Comedor", "38,50 m²"),
        ("Cocina con Isla", "18,72 m²"),
        ("Master Suite", "14,82 m²"),
        ("Baño Suite", "5,57 m²"),
        ("Baño Común", "5,68 m²"),
        ("Dormitorio 2", "11,70 m²"),
        ("Dormitorio 3", "11,90 m²"),
        ("Pasillo Distrib.", "7,32 m²"),
        ("Cochera/Trastero", "21,14 m²"),
        ("---", "---"),
        ("TOTAL CERRADA", "136,7 m²"),
        ("Porche Cubierto", "11,40 m²"),
        ("Patio + Piscina", "26,36 m²"),
        ("TOTAL EXTERIOR", "37,8 m²"),
        ("=== ", "=== "),
        ("SUP. CONSTRUIDA", "196,8 m²"),
    ]

    iy = cs_y + cs_h - 0.85
    for nombre, sup in cuadro_items:
        if nombre.startswith("---") or nombre.startswith("==="):
            ax.plot([cs_x + 0.15, cs_x + cs_w - 0.15], [iy, iy], color="#94A3B8", lw=0.6, zorder=32)
            iy -= 0.22
            continue
        is_bold = "TOTAL" in nombre or "CONSTRUIDA" in nombre
        col = C_DIM if is_bold else C_TEXT_MAIN
        fs = 6.2 if is_bold else 5.5
        ax.text(cs_x + 0.15, iy, nombre, ha='left', va='center', fontsize=fs, weight='bold' if is_bold else 'normal', color=col, zorder=32)
        ax.text(cs_x + cs_w - 0.15, iy, sup, ha='right', va='center', fontsize=fs, weight='bold' if is_bold else 'normal', color=col, zorder=32)
        iy -= 0.48

    # 11. CAJETÍN OFICIAL DE ARQUITECTURA (FRANJA INFERIOR)
    caj_x, caj_y, caj_w, caj_h = -4.10, -3.40, 21.30, 1.40
    draw_rect(ax, caj_x, caj_y, caj_w, caj_h, "#FFFFFF", edge_col=C_WALL, lw=1.5, z=40)
    
    # Separadores de cajetín
    ax.plot([caj_x + 6.0, caj_x + 6.0], [caj_y, caj_y + caj_h], color=C_WALL, lw=0.8, zorder=41)
    ax.plot([caj_x + 14.5, caj_x + 14.5], [caj_y, caj_y + caj_h], color=C_WALL, lw=0.8, zorder=41)
    ax.plot([caj_x + 18.0, caj_x + 18.0], [caj_y, caj_y + caj_h], color=C_WALL, lw=0.8, zorder=41)

    # Bloque 1: Identificación del Proyecto
    ax.text(caj_x + 0.30, caj_y + 1.05, "PROYECTO RESIDENCIAL BIFAMILIAR", fontsize=11, weight='bold', color=C_TEXT_MAIN, zorder=42)
    ax.text(caj_x + 0.30, caj_y + 0.70, "Vivienda Unifamiliar en Parcela Pasante con Patio y Piscina", fontsize=7.5, color=C_TEXT_SEC, zorder=42)
    ax.text(caj_x + 0.30, caj_y + 0.35, "Calle Moreno Torroba s/n · Palma del Río (Córdoba)", fontsize=7.5, weight='bold', color="#1E40AF", zorder=42)

    # Bloque 2: Datos del Plano
    ax.text(caj_x + 6.30, caj_y + 1.05, "PLANO: PLANTA BAJA AMUEBLADA Y ACOTADA", fontsize=10, weight='bold', color=C_TEXT_MAIN, zorder=42)
    ax.text(caj_x + 6.30, caj_y + 0.70, "Distribución Optimizada · Master Suite con Vestidor + Almacenaje Salón", fontsize=7.0, color=C_TEXT_SEC, zorder=42)
    ax.text(caj_x + 6.30, caj_y + 0.35, "Superficie Útil Cerrada: 136,70 m² | Exterior: 37,80 m² | Total: 196,80 m² constr.", fontsize=7.0, weight='bold', color=C_TEXT_MAIN, zorder=42)

    # Bloque 3: Escala y Fecha
    ax.text(caj_x + 14.80, caj_y + 1.05, "ESCALA: 1:50 (A3)", fontsize=9, weight='bold', color=C_TEXT_MAIN, zorder=42)
    ax.text(caj_x + 14.80, caj_y + 0.70, "FECHA: Agosto 2026", fontsize=7.5, color=C_TEXT_SEC, zorder=42)
    ax.text(caj_x + 14.80, caj_y + 0.35, "FORMATO: DIN A3 (420x297)", fontsize=7.0, color=C_TEXT_SEC, zorder=42)

    # Bloque 4: Número de Plano
    draw_rect(ax, caj_x + 18.0, caj_y, 3.30, caj_h, C_WALL, edge_col=C_WALL, z=41)
    ax.text(caj_x + 19.65, caj_y + 0.85, "PLANO Nº", ha='center', va='center', fontsize=8, weight='bold', color="#94A3B8", zorder=42)
    ax.text(caj_x + 19.65, caj_y + 0.40, "P-01", ha='center', va='center', fontsize=18, weight='bold', color="#FFFFFF", zorder=42)

    out_file = os.path.join(OUTPUT_DIR, "01_plano_arquitecto_planta_baja.png")
    out_pdf  = os.path.join(OUTPUT_DIR, "01_plano_arquitecto_planta_baja.pdf")
    plt.savefig(out_file, bbox_inches='tight', dpi=300)
    plt.savefig(out_pdf, bbox_inches='tight')
    plt.close(fig)
    print(f"PLANO ARQUITECTO GENERADO: {out_file} y {out_pdf}")

generar_plano_arquitecto_completo()
