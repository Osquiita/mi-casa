# -*- coding: utf-8 -*-
"""
GENERADOR INTEGRAL DE PLANOS TÉCNICOS ARQUITECTÓNICOS EJECUTIVOS
Genera la colección completa de planos oficiales para el Visado Colegial y Licencia de Obras:
- P-03: PLANTA DE CUBIERTAS E INSTALACIONES TÉCNICAS (Escala 1:100)
- P-04: ALZADOS EXTERIORES E INTERIOR DE PATIO (Escala 1:100)
- P-05: SECCIONES CONSTRUCTIVAS LONGITUDINAL Y TRANSVERSAL (Escala 1:75)
- P-06: ESTRUCTURA (CIMENTACIÓN Y SANEAMIENTO ENTERRADO) (Escala 1:75)
- P-07: INSTALACIONES GENERALES (CLIMATIZACIÓN, VMC, ELECTRICIDAD Y FONTANERÍA) (Escala 1:75)
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
C_WALL      = "#181A1D"
C_WALL_INT  = "#2C3036"
C_DIM       = "#B91C1C"
C_DIM_LINE  = "#DC2626"
C_TEXT_MAIN = "#0F172A"
C_TEXT_SEC  = "#475569"
C_BLUE_CAD  = "#0369A1"
C_WOOD      = "#B45309"
C_GLASS     = "#0EA5E9"

def setup_canvas(w=22, h=15.5):
    fig, ax = plt.subplots(figsize=(w, h), dpi=300)
    ax.set_aspect('equal')
    ax.axis('off')
    return fig, ax

def draw_cajetin(ax, num_plano, titulo_plano, desc_plano, escala="1:100", caj_x=-4.80, caj_y=-4.90, caj_w=21.80, caj_h=1.70):
    r = patches.Rectangle((caj_x, caj_y), caj_w, caj_h, facecolor="#FFFFFF", edgecolor=C_WALL, linewidth=1.3, zorder=40)
    ax.add_patch(r)
    ax.plot([caj_x + 6.8, caj_x + 6.8], [caj_y, caj_y + caj_h], color=C_WALL, lw=0.8, zorder=41)
    ax.plot([caj_x + 15.0, caj_x + 15.0], [caj_y, caj_y + caj_h], color=C_WALL, lw=0.8, zorder=41)
    ax.plot([caj_x + 18.6, caj_x + 18.6], [caj_y, caj_y + caj_h], color=C_WALL, lw=0.8, zorder=41)

    ax.text(caj_x + 0.30, caj_y + 1.25, "PROYECTO RESIDENCIAL BIFAMILIAR", fontsize=10.5, weight='bold', color=C_TEXT_MAIN, zorder=42)
    ax.text(caj_x + 0.30, caj_y + 0.85, "Vivienda Unifamiliar en Parcela Pasante con Patio y Piscina", fontsize=7.2, color=C_TEXT_SEC, zorder=42)
    ax.text(caj_x + 0.30, caj_y + 0.45, "Calle Moreno Torroba s/n · Palma del Río (Córdoba)", fontsize=7.2, weight='bold', color="#1E40AF", zorder=42)

    ax.text(caj_x + 7.10, caj_y + 1.25, f"PLANO: {titulo_plano}", fontsize=9.2, weight='bold', color=C_TEXT_MAIN, zorder=42)
    ax.text(caj_x + 7.10, caj_y + 0.85, desc_plano, fontsize=6.8, color=C_TEXT_SEC, zorder=42)
    ax.text(caj_x + 7.10, caj_y + 0.45, "Documento de Ejecución CTE · Aprobación de Licencia Municipal", fontsize=6.8, weight='bold', color=C_TEXT_MAIN, zorder=42)

    ax.text(caj_x + 15.30, caj_y + 1.25, f"ESCALA: {escala} (A3)", fontsize=8.5, weight='bold', color=C_TEXT_MAIN, zorder=42)
    ax.text(caj_x + 15.30, caj_y + 0.85, "FECHA: Octubre 2026", fontsize=7.0, color=C_TEXT_SEC, zorder=42)
    ax.text(caj_x + 15.30, caj_y + 0.45, "FORMATO: DIN A3", fontsize=6.8, color=C_TEXT_SEC, zorder=42)

    r_num = patches.Rectangle((caj_x + 18.6, caj_y), 3.20, caj_h, facecolor=C_WALL, edgecolor=C_WALL, zorder=41)
    ax.add_patch(r_num)
    ax.text(caj_x + 20.20, caj_y + 1.10, "PLANO Nº", ha='center', va='center', fontsize=7.5, weight='bold', color="#94A3B8", zorder=42)
    ax.text(caj_x + 20.20, caj_y + 0.55, num_plano, ha='center', va='center', fontsize=18, weight='bold', color="#FFFFFF", zorder=42)

def draw_cota_h(ax, x1, x2, y, val_str, offset=0.14, tick=0.08):
    if x1 > x2: x1, x2 = x2, x1
    ax.plot([x1, x2], [y, y], color=C_DIM_LINE, lw=0.6, zorder=30)
    ax.plot([x1 - tick, x1 + tick], [y - tick, y + tick], color=C_DIM, lw=1.1, zorder=31)
    ax.plot([x2 - tick, x2 + tick], [y - tick, y + tick], color=C_DIM, lw=1.1, zorder=31)
    ax.text((x1 + x2)/2.0, y + offset, val_str, ha='center', va='bottom', fontsize=6.8, color=C_DIM, weight='bold', zorder=32,
            bbox=dict(boxstyle='square,pad=0.06', facecolor='#FFFFFF', edgecolor='none', alpha=0.92))

def draw_cota_v(ax, y1, y2, x, val_str, offset=0.14, tick=0.08):
    if y1 > y2: y1, y2 = y2, y1
    ax.plot([x, x], [y1, y2], color=C_DIM_LINE, lw=0.6, zorder=30)
    ax.plot([x - tick, x + tick], [y1 - tick, y1 + tick], color=C_DIM, lw=1.1, zorder=31)
    ax.plot([x - tick, x + tick], [y2 - tick, y2 + tick], color=C_DIM, lw=1.1, zorder=31)
    ax.text(x + offset, (y1 + y2)/2.0, val_str, ha='left', va='center', fontsize=6.8, color=C_DIM, weight='bold', rotation=90, zorder=32,
            bbox=dict(boxstyle='square,pad=0.06', facecolor='#FFFFFF', edgecolor='none', alpha=0.92))

# ==============================================================================
# 1. PLANO P-03: PLANTA DE CUBIERTAS E INSTALACIONES TÉCNICAS
# ==============================================================================
def generar_plano_cubiertas():
    fig, ax = setup_canvas()
    ax.set_xlim(-5.2, 17.2)
    ax.set_ylim(-5.5, 21.8)

    # Base de cubierta
    r_base = patches.Rectangle((-0.15, -0.15), 11.60, 17.75, facecolor="#E2E8F0", edgecolor=C_WALL, lw=1.5, zorder=5)
    ax.add_patch(r_base)

    # Zona Patio Vacío (sin techar)
    r_patio = patches.Rectangle((6.40, 7.40), 5.00, 5.60, facecolor="#BAE6FD", edgecolor=C_WALL, lw=1.2, zorder=6)
    ax.add_patch(r_patio)
    ax.text(8.90, 10.20, "HUECO PATIO / PISCINA (SIN TECHAR)", ha='center', va='center', fontsize=7.0, weight='bold', color="#0369A1", zorder=7)

    # Peto perimetral (0.30 m)
    r_peto = patches.Rectangle((0.15, 0.15), 11.00, 17.15, facecolor="#F8FAFC", edgecolor="#94A3B8", lw=0.8, linestyle='--', zorder=7)
    ax.add_patch(r_peto)

    # Zonas de faldones y pendientes (1.5% a sumideros)
    for x, y, dx, dy in [(3.20, 3.70, 0, -1.2), (3.20, 10.50, 0, 1.2), (8.90, 3.70, 0, -1.2), (8.90, 15.00, 0, 1.2)]:
        ax.annotate('', xy=(x+dx, y+dy), xytext=(x, y),
                    arrowprops=dict(arrowstyle='->', color="#475569", lw=1.2), zorder=10)
        ax.text(x+dx/2, y+dy/2 + 0.25, "i = 1.5%", ha='center', va='bottom', fontsize=5.8, color="#475569", zorder=11)

    # Sumideros de pluviales sifónicos (8 unidades)
    sumideros = [(1.00, 1.00), (5.40, 1.00), (7.00, 1.00), (10.40, 1.00),
                 (1.00, 16.50), (5.40, 16.50), (7.00, 16.50), (10.40, 16.50)]
    for sx, sy in sumideros:
        circ = patches.Circle((sx, sy), 0.22, facecolor="#0284C7", edgecolor="#0369A1", lw=0.8, zorder=12)
        ax.add_patch(circ)
        ax.text(sx, sy, "S", ha='center', va='center', fontsize=4.8, weight='bold', color="#FFFFFF", zorder=13)
        ax.text(sx + 0.35, sy, "Sumidero Ø110", ha='left', va='center', fontsize=4.5, color="#0369A1", zorder=13)

    # Campo Solar Fotovoltaico (10 Paneles orientados al Sur, 30º inclinación)
    for i in range(5):
        for j in range(2):
            px = 1.00 + i * 1.05
            py = 3.80 + j * 1.80
            r_pan = patches.Rectangle((px, py), 0.95, 1.60, facecolor="#1E3A8A", edgecolor="#93C5FD", lw=0.7, zorder=15)
            ax.add_patch(r_pan)
            # Líneas de celdas
            ax.plot([px, px+0.95], [py+0.80, py+0.80], color="#60A5FA", lw=0.4, zorder=16)
    ax.text(3.40, 7.20, "CAMPO SOLAR FOTOVOLTAICO (10 PANELES · 4,5 kWp)", ha='center', va='bottom', fontsize=6.2, weight='bold', color="#1E3A8A", zorder=17)

    # Unidades Exteriores de Aerotermia (Vivienda A y Vivienda B)
    for k, (ax_x, name) in enumerate([(7.20, "AEROTERMIA VIV. A"), (9.20, "AEROTERMIA VIV. B")]):
        r_aero = patches.Rectangle((ax_x, 3.20), 1.40, 0.75, facecolor="#334155", edgecolor="#0F172A", lw=0.8, zorder=15)
        ax.add_patch(r_aero)
        c_fan = patches.Circle((ax_x + 0.70, 3.57), 0.28, facecolor="#64748B", edgecolor="#CBD5E1", lw=0.5, zorder=16)
        ax.add_patch(c_fan)
        ax.text(ax_x + 0.70, 2.85, name, ha='center', va='top', fontsize=5.0, weight='bold', color="#0F172A", zorder=17)

    # Cuadro de Especificaciones Técnicas de Cubierta
    draw_cota_h(ax, -0.15, 11.45, -0.80, "11.60 m (ANCHURA CUBIERTA)")
    draw_cota_v(ax, -0.15, 17.60, -0.80, "17.75 m (LONGITUD CUBIERTA)")

    # Cajetín
    draw_cajetin(ax, "P-03", "PLANTA DE CUBIERTAS E INSTALACIONES", "Cubierta Plana Invertida, Campo Solar Fotovoltaico y Climatización", "1:100")

    plt.savefig(os.path.join(OUTPUT_DIR, "03_plano_cubiertas.png"), bbox_inches='tight', dpi=300)
    plt.savefig(os.path.join(OUTPUT_DIR, "03_plano_cubiertas.pdf"), bbox_inches='tight')
    plt.close(fig)
    print("PLANO P-03 CUBIERTAS GENERADO.")

# ==============================================================================
# 2. PLANO P-04: ALZADOS EXTERIORES E INTERIOR DE PATIO
# ==============================================================================
def generar_plano_alzados():
    fig, ax = setup_canvas()
    ax.set_xlim(-5.2, 17.2)
    ax.set_ylim(-5.5, 21.8)

    # 1. ALZADO SUR (Calle Moreno Torroba) - Principal
    # Y = 11.50 a 18.00 (Anchura 11.60 m, Altura total 6.50 m)
    y_base_s = 12.00
    ax.plot([-1.5, 13.0], [y_base_s, y_base_s], color="#0F172A", lw=2.0, zorder=10) # Rasante calle
    # Fachada
    r_fach_s = patches.Rectangle((0.0, y_base_s), 11.40, 6.20, facecolor="#F8FAFC", edgecolor=C_WALL, lw=1.2, zorder=5)
    ax.add_patch(r_fach_s)
    # Línea de forjado intermedio (h = 2.90 m)
    ax.plot([0.0, 11.40], [y_base_s + 2.90, y_base_s + 2.90], color="#94A3B8", lw=0.8, linestyle='--', zorder=6)
    # Peto de cubierta
    ax.plot([0.0, 11.40], [y_base_s + 5.90, y_base_s + 5.90], color="#64748B", lw=0.8, zorder=6)

    # Huecos Planta Baja
    # Puerta Portal A
    r_pa = patches.Rectangle((0.30, y_base_s), 1.00, 2.20, facecolor="#C46D29", edgecolor="#7C2D12", lw=0.8, zorder=7)
    ax.add_patch(r_pa)
    # Ventanas Salón PB
    r_v1 = patches.Rectangle((2.60, y_base_s + 0.90), 1.80, 1.40, facecolor=C_GLASS, edgecolor="#0369A1", lw=0.8, zorder=7)
    r_v2 = patches.Rectangle((4.80, y_base_s + 0.90), 1.20, 1.40, facecolor=C_GLASS, edgecolor="#0369A1", lw=0.8, zorder=7)
    # Ventanas Cocina PB
    r_v3 = patches.Rectangle((6.90, y_base_s + 0.90), 1.20, 1.40, facecolor=C_GLASS, edgecolor="#0369A1", lw=0.8, zorder=7)
    r_v4 = patches.Rectangle((8.90, y_base_s + 0.90), 1.00, 1.40, facecolor=C_GLASS, edgecolor="#0369A1", lw=0.8, zorder=7)
    # Puerta Portal B (Escalera)
    r_pb = patches.Rectangle((10.40, y_base_s), 1.00, 2.20, facecolor="#C46D29", edgecolor="#7C2D12", lw=0.8, zorder=7)
    for p in [r_v1, r_v2, r_v3, r_v4, r_pb]: ax.add_patch(p)

    # Huecos Planta Alta (Alineados)
    r_va1 = patches.Rectangle((2.60, y_base_s + 3.80), 1.80, 1.40, facecolor=C_GLASS, edgecolor="#0369A1", lw=0.8, zorder=7)
    r_va2 = patches.Rectangle((4.80, y_base_s + 3.80), 1.20, 1.40, facecolor=C_GLASS, edgecolor="#0369A1", lw=0.8, zorder=7)
    r_va3 = patches.Rectangle((6.90, y_base_s + 3.80), 1.20, 1.40, facecolor=C_GLASS, edgecolor="#0369A1", lw=0.8, zorder=7)
    r_va4 = patches.Rectangle((8.90, y_base_s + 3.80), 1.00, 1.40, facecolor=C_GLASS, edgecolor="#0369A1", lw=0.8, zorder=7)
    r_va5 = patches.Rectangle((10.50, y_base_s + 3.40), 0.80, 1.80, facecolor=C_GLASS, edgecolor="#0369A1", lw=0.8, zorder=7)
    for p in [r_va1, r_va2, r_va3, r_va4, r_va5]: ax.add_patch(p)

    ax.text(5.70, y_base_s + 6.45, "ALZADO PRINCIPAL SUR (CALLE MORENO TORROBA)", ha='center', va='bottom', fontsize=7.5, weight='bold', color=C_TEXT_MAIN)
    ax.text(-0.30, y_base_s + 1.45, "+0,00", ha='right', va='center', fontsize=5.5, color="#64748B")
    ax.text(-0.30, y_base_s + 2.90, "+2,90 (P.A.)", ha='right', va='center', fontsize=5.5, color="#64748B")
    ax.text(-0.30, y_base_s + 5.90, "+5,90 (CUB.)", ha='right', va='center', fontsize=5.5, color="#64748B")

    # 2. ALZADO NORTE (Calle Trasera - Acceso Garaje)
    y_base_n = 2.00
    ax.plot([-1.5, 13.0], [y_base_n, y_base_n], color="#0F172A", lw=2.0, zorder=10)
    r_fach_n = patches.Rectangle((0.0, y_base_n), 11.40, 6.20, facecolor="#F8FAFC", edgecolor=C_WALL, lw=1.2, zorder=5)
    ax.add_patch(r_fach_n)
    ax.plot([0.0, 11.40], [y_base_n + 2.90, y_base_n + 2.90], color="#94A3B8", lw=0.8, linestyle='--', zorder=6)

    # Huecos PB Norte
    # Portón Garaje (4.85 m)
    r_gar = patches.Rectangle((6.40, y_base_n), 4.85, 2.40, facecolor="#334155", edgecolor="#0F172A", lw=1.0, zorder=7)
    ax.add_patch(r_gar)
    ax.text(8.82, y_base_n + 1.20, "PORTÓN COCHERA MOTORIZADO (4,85 m)", ha='center', va='center', fontsize=5.2, weight='bold', color="#FFFFFF", zorder=8)
    # Ventanas Dormitorios PB
    r_vn1 = patches.Rectangle((0.80, y_base_n + 0.90), 1.60, 1.40, facecolor=C_GLASS, edgecolor="#0369A1", lw=0.8, zorder=7)
    r_vn2 = patches.Rectangle((3.60, y_base_n + 0.90), 1.60, 1.40, facecolor=C_GLASS, edgecolor="#0369A1", lw=0.8, zorder=7)
    ax.add_patch(r_vn1); ax.add_patch(r_vn2)

    # Huecos PA Norte
    r_van1 = patches.Rectangle((0.80, y_base_n + 2.90), 1.60, 2.20, facecolor=C_GLASS, edgecolor="#0369A1", lw=0.8, zorder=7) # Terraza solarium
    r_van2 = patches.Rectangle((3.60, y_base_n + 3.80), 1.60, 1.40, facecolor=C_GLASS, edgecolor="#0369A1", lw=0.8, zorder=7)
    r_van3 = patches.Rectangle((7.00, y_base_n + 3.80), 2.00, 1.40, facecolor=C_GLASS, edgecolor="#0369A1", lw=0.8, zorder=7)
    r_van4 = patches.Rectangle((9.80, y_base_n + 3.80), 1.20, 1.40, facecolor=C_GLASS, edgecolor="#0369A1", lw=0.8, zorder=7)
    for p in [r_van1, r_van2, r_van3, r_van4]: ax.add_patch(p)

    ax.text(5.70, y_base_n + 6.45, "ALZADO TRASERO NORTE (CALLE POSTERIOR · GARAJE)", ha='center', va='bottom', fontsize=7.5, weight='bold', color=C_TEXT_MAIN)

    draw_cajetin(ax, "P-04", "ALZADOS EXTERIORES GENERALES", "Alzado Principal Sur (Moreno Torroba) y Alzado Trasero Norte (Garaje)", "1:100")

    plt.savefig(os.path.join(OUTPUT_DIR, "04_plano_alzados.png"), bbox_inches='tight', dpi=300)
    plt.savefig(os.path.join(OUTPUT_DIR, "04_plano_alzados.pdf"), bbox_inches='tight')
    plt.close(fig)
    print("PLANO P-04 ALZADOS GENERADO.")

# ==============================================================================
# 3. PLANO P-05: SECCIONES CONSTRUCTIVAS LONGITUDINAL Y TRANSVERSAL
# ==============================================================================
def generar_plano_secciones():
    fig, ax = setup_canvas()
    ax.set_xlim(-5.2, 17.2)
    ax.set_ylim(-5.5, 21.8)

    # 1. SECCIÓN LONGITUDINAL A-A' (Y = 0.00 a 17.75 m)
    y_s = 9.50
    # Línea de terreno natural
    ax.plot([-1.5, 17.5], [y_s, y_s], color="#0F172A", lw=2.0, zorder=10)
    # Solera ventilada tipo Cáviti (-0.40 a 0.00)
    r_sol = patches.Rectangle((0.0, y_s - 0.40), 17.60, 0.40, facecolor="#CBD5E1", edgecolor=C_WALL, lw=1.0, zorder=5)
    ax.add_patch(r_sol)
    ax.text(8.80, y_s - 0.25, "SOLERA VENTILADA SANITARIA TIPO CÁVITI (h=40 cm) + AISLAMIENTO TÉRMICO XPS", ha='center', va='center', fontsize=5.0, color="#334155")

    # Muros y forjados
    # Salón PB
    r_sal_pb = patches.Rectangle((0.0, y_s), 6.40, 2.60, facecolor="#FAF8F5", edgecolor=C_WALL, lw=0.8, zorder=6)
    # Porche PB
    r_por_pb = patches.Rectangle((6.40, y_s), 2.40, 2.60, facecolor="#F5EFE6", edgecolor=C_WALL, lw=0.8, zorder=6)
    # Patio y Piscina PB
    r_pat_pb = patches.Rectangle((8.80, y_s), 4.20, 2.60, facecolor="#ECFDF5", edgecolor="none", zorder=4)
    # Vaso de Piscina enterrado (profundidad 1.40 m)
    r_pisc = patches.Rectangle((9.50, y_s - 1.40), 3.00, 1.40, facecolor="#BAE6FD", edgecolor="#0284C7", lw=1.2, zorder=5)
    ax.add_patch(r_pisc)
    ax.text(11.00, y_s - 0.70, "PISCINA (-1,40 m)\nAgua + Depuración", ha='center', va='center', fontsize=5.5, weight='bold', color="#0369A1")
    # Cochera PB
    r_coch_pb = patches.Rectangle((13.00, y_s), 4.60, 2.60, facecolor="#F1F3F5", edgecolor=C_WALL, lw=0.8, zorder=6)
    for p in [r_sal_pb, r_por_pb, r_pat_pb, r_coch_pb]: ax.add_patch(p)

    # Forjado Intermedio Planta Primera (h = 0.30 m)
    r_forj1 = patches.Rectangle((0.0, y_s + 2.60), 8.80, 0.30, facecolor="#94A3B8", edgecolor=C_WALL, lw=0.9, zorder=7)
    r_forj1_coch = patches.Rectangle((13.00, y_s + 2.60), 4.60, 0.30, facecolor="#94A3B8", edgecolor=C_WALL, lw=0.9, zorder=7)
    ax.add_patch(r_forj1); ax.add_patch(r_forj1_coch)

    # Planta Alta
    r_pa_sal = patches.Rectangle((0.0, y_s + 2.90), 8.80, 2.60, facecolor="#FCFAF7", edgecolor=C_WALL, lw=0.8, zorder=6)
    r_pa_d2 = patches.Rectangle((13.00, y_s + 2.90), 4.60, 2.60, facecolor="#FCFAF7", edgecolor=C_WALL, lw=0.8, zorder=6)
    ax.add_patch(r_pa_sal); ax.add_patch(r_pa_d2)

    # Forjado Cubierta y Petos
    r_forj_cub1 = patches.Rectangle((0.0, y_s + 5.50), 8.80, 0.35, facecolor="#64748B", edgecolor=C_WALL, lw=1.0, zorder=7)
    r_forj_cub2 = patches.Rectangle((13.00, y_s + 5.50), 4.60, 0.35, facecolor="#64748B", edgecolor=C_WALL, lw=1.0, zorder=7)
    ax.add_patch(r_forj_cub1); ax.add_patch(r_forj_cub2)

    # Cotas de altura libre
    draw_cota_v(ax, y_s, y_s + 2.60, -0.60, "2.60 m libre (PB)")
    draw_cota_v(ax, y_s + 2.90, y_s + 5.50, -0.60, "2.60 m libre (PA)")
    draw_cota_v(ax, y_s, y_s + 5.85, -1.30, "5.85 m (TOTAL CORNISA)")

    ax.text(8.80, y_s + 6.30, "SECCIÓN LONGITUDINAL CONSTRUCTIVA A-A'", ha='center', va='bottom', fontsize=8.0, weight='bold', color=C_TEXT_MAIN)
    ax.text(3.20, y_s + 1.30, "SALÓN PB\n(h=2,60 m)", ha='center', va='center', fontsize=6.0, color="#475569")
    ax.text(3.20, y_s + 4.20, "GRAN SALÓN PA\n(h=2,60 m)", ha='center', va='center', fontsize=6.0, color="#475569")
    ax.text(15.30, y_s + 1.30, "COCHERA PB\n(h=2,60 m)", ha='center', va='center', fontsize=6.0, color="#475569")
    ax.text(15.30, y_s + 4.20, "DORMITORIO 2 PA\n(h=2,60 m)", ha='center', va='center', fontsize=6.0, color="#475569")

    # 2. DETALLE ESTRUCTURAL ZAPATAS
    y_sec_b = 0.50
    ax.plot([-1.5, 13.0], [y_sec_b, y_sec_b], color="#0F172A", lw=2.0, zorder=10)
    r_sec_b = patches.Rectangle((0.0, y_sec_b), 11.40, 5.80, facecolor="#F8FAFC", edgecolor=C_WALL, lw=1.2, zorder=5)
    ax.add_patch(r_sec_b)
    # Zapatas de cimentación
    for zx in [0.0, 5.70, 11.40]:
        r_zap = patches.Rectangle((zx - 0.70, y_sec_b - 1.00), 1.40, 0.80, facecolor="#94A3B8", edgecolor=C_WALL, lw=1.0, zorder=6)
        ax.add_patch(r_zap)
        ax.text(zx, y_sec_b - 0.60, "ZAPATA HA-25\n1,40x1,40x0,80", ha='center', va='center', fontsize=4.5, weight='bold', color="#FFFFFF", zorder=7)

    ax.text(5.70, y_sec_b + 6.10, "SECCIÓN TRANSVERSAL CONSTRUCTIVA B-B' (CRUJÍA CENTRAL Y CIMENTACIÓN)", ha='center', va='bottom', fontsize=7.5, weight='bold', color=C_TEXT_MAIN)

    draw_cajetin(ax, "P-05", "SECCIONES CONSTRUCTIVAS GENERALES", "Sección Longitudinal A-A' y Sección Transversal B-B' con Cimentación y Alturas", "1:75")

    plt.savefig(os.path.join(OUTPUT_DIR, "05_plano_secciones.png"), bbox_inches='tight', dpi=300)
    plt.savefig(os.path.join(OUTPUT_DIR, "05_plano_secciones.pdf"), bbox_inches='tight')
    plt.close(fig)
    print("PLANO P-05 SECCIONES GENERADO.")

# ==============================================================================
# 4. PLANO P-06: ESTRUCTURA (CIMENTACIÓN Y SANEAMIENTO ENTERRADO)
# ==============================================================================
def generar_plano_estructura():
    fig, ax = setup_canvas()
    ax.set_xlim(-5.2, 17.2)
    ax.set_ylim(-5.5, 21.8)

    # Contorno solar
    r_sol = patches.Rectangle((-0.15, -0.15), 11.60, 17.75, facecolor="#F8FAFC", edgecolor=C_WALL, lw=1.2, zorder=2)
    ax.add_patch(r_sol)

    # Zapatas corridas en medianeras (ancho 0.80 m x canto 0.60 m)
    r_zm_o = patches.Rectangle((-0.20, -0.20), 0.80, 17.80, facecolor="#CBD5E1", edgecolor="#475569", lw=0.9, zorder=4)
    r_zm_e = patches.Rectangle((10.80, -0.20), 0.80, 17.80, facecolor="#CBD5E1", edgecolor="#475569", lw=0.9, zorder=4)
    ax.add_patch(r_zm_o); ax.add_patch(r_zm_e)

    # Zapatas aisladas en pilares interiores (1.50 x 1.50 m)
    pilares = [
        (0.00, 0.00), (6.40, 0.00), (10.40, 0.00), (11.40, 0.00),
        (0.00, 7.40), (6.40, 7.40), (11.40, 7.40),
        (0.00, 13.50), (6.40, 13.50), (11.40, 13.50),
        (0.00, 17.60), (6.40, 17.60), (11.40, 17.60)
    ]
    for px, py in pilares:
        r_z = patches.Rectangle((px - 0.60, py - 0.60), 1.20, 1.20, facecolor="#94A3B8", edgecolor="#334155", lw=0.9, zorder=5)
        ax.add_patch(r_z)
        # Pilar de hormigón armado 30x30 cm
        r_pil = patches.Rectangle((px - 0.15, py - 0.15), 0.30, 0.30, facecolor="#1E293B", edgecolor="#0F172A", lw=0.7, zorder=6)
        ax.add_patch(r_pil)

    # Vigas riostras y centradoras (0.40 x 0.40 m)
    for y in [0.00, 7.40, 13.50, 17.60]:
        ax.plot([0.00, 11.40], [y, y], color="#475569", lw=2.5, zorder=4)
    for x in [0.00, 6.40, 11.40]:
        ax.plot([x, x], [0.00, 17.60], color="#475569", lw=2.5, zorder=4)

    # Red de Saneamiento Enterrada (Fecales y Pluviales)
    # Arquetas registrables 40x40 cm
    arquetas = [
        (1.80, 8.50, "A-01"), (5.50, 8.50, "A-02"), (8.50, 2.00, "A-03"),
        (10.50, 14.00, "A-04"), (6.00, 16.50, "A-05"), (1.00, 0.50, "A-SIFÓNICA")
    ]
    for ax_x, ax_y, label in arquetas:
        r_arq = patches.Rectangle((ax_x - 0.25, ax_y - 0.25), 0.50, 0.50, facecolor="#EA580C", edgecolor="#9A3412", lw=0.8, zorder=8)
        ax.add_patch(r_arq)
        ax.text(ax_x, ax_y + 0.35, label, ha='center', va='bottom', fontsize=5.0, weight='bold', color="#9A3412", zorder=9)

    # Colectores enterrados PVC Ø160 mm con pendiente 2%
    colectores = [
        ((5.50, 8.50), (1.80, 8.50)),
        ((1.80, 8.50), (1.00, 0.50)),
        ((8.50, 2.00), (1.00, 0.50)),
        ((10.50, 14.00), (6.00, 16.50)),
        ((6.00, 16.50), (1.80, 8.50)),
        ((1.00, 0.50), (0.75, -0.60)) # Acometida municipal
    ]
    for p_ini, p_fin in colectores:
        ax.annotate('', xy=p_fin, xytext=p_ini,
                    arrowprops=dict(arrowstyle='->', color="#DC2626", lw=1.5, linestyle='--'), zorder=7)

    ax.text(0.75, -0.80, "ACOMETIDA GENERAL AL ALCANTARILLADO MUNICIPAL (Ø200)", ha='center', va='top', fontsize=5.5, weight='bold', color="#DC2626")

    # Cuadro de características estructurales
    cs_x, cs_y = -4.80, 3.50
    patches_rect = patches.Rectangle((cs_x, cs_y), 4.20, 7.50, facecolor="#FFFFFF", edgecolor=C_WALL, lw=0.9, zorder=20)
    ax.add_patch(patches_rect)
    ax.text(cs_x + 2.10, cs_y + 7.10, "CUADRO DE CONTROL DE ESTRUCTURA", ha='center', va='center', fontsize=6.5, weight='bold', color=C_TEXT_MAIN)
    specs = [
        "Normativa: Código Estructural (RD 470/2021)",
        "Hormigón Zapatas: HA-25/B/20/IIa (Control Estadístico)",
        "Hormigón Vigas/Pilares: HA-30/B/20/IIa",
        "Acero Armaduras: B 500 S (Límite elástico 500 MPa)",
        "Recubrimiento mínimo: 40 mm en zapatas, 30 mm pilares",
        "Tensión admisible terreno: 2,00 kg/cm² a -1,20 m",
        "Saneamiento: PVC teja lisa corrugada SN4 Ø160 mm",
        "Pendiente mínima colectores: 2,0 % continuo"
    ]
    for idx, s in enumerate(specs):
        ax.text(cs_x + 0.20, cs_y + 6.30 - idx * 0.70, f"• {s}", ha='left', va='center', fontsize=5.0, color="#334155")

    draw_cajetin(ax, "P-06", "ESTRUCTURA Y CIMENTACIÓN", "Plano de Replanteo de Zapatas, Vigas Riostras y Red de Saneamiento Enterrada", "1:75")

    plt.savefig(os.path.join(OUTPUT_DIR, "06_plano_estructura.png"), bbox_inches='tight', dpi=300)
    plt.savefig(os.path.join(OUTPUT_DIR, "06_plano_estructura.pdf"), bbox_inches='tight')
    plt.close(fig)
    print("PLANO P-06 ESTRUCTURA GENERADO.")

# ==============================================================================
# 5. PLANO P-07: INSTALACIONES GENERALES (CTE DB-HE / DB-HS)
# ==============================================================================
def generar_plano_instalaciones():
    fig, ax = setup_canvas()
    ax.set_xlim(-5.2, 17.2)
    ax.set_ylim(-5.5, 21.8)

    # Base muros sutiles
    r_sol = patches.Rectangle((-0.15, -0.15), 11.60, 17.75, facecolor="#F8FAFC", edgecolor=C_WALL, lw=1.0, zorder=2)
    ax.add_patch(r_sol)

    # 1. Electricidad y Telecomunicaciones (REBT)
    # CGMP (Cuadro General de Mando y Protección) en entrada
    r_cgmp = patches.Rectangle((0.15, 0.40), 0.60, 0.25, facecolor="#EAB308", edgecolor="#A16207", lw=0.8, zorder=10)
    ax.add_patch(r_cgmp)
    ax.text(0.45, 0.80, "CGMP VIV. A", ha='center', va='bottom', fontsize=5.0, weight='bold', color="#A16207", zorder=11)

    # Punto de recarga Wallbox en Garaje (7.4 kW Modo 3)
    r_wb = patches.Rectangle((6.55, 16.80), 0.35, 0.45, facecolor="#0284C7", edgecolor="#0369A1", lw=0.8, zorder=10)
    ax.add_patch(r_wb)
    ax.text(6.55, 17.40, "PUNTO RECARGA VE\n(Wallbox 7,4 kW)", ha='left', va='bottom', fontsize=5.0, weight='bold', color="#0284C7", zorder=11)

    # 2. Fontanería y ACS Aerotermia (DB-HE4 / DB-HS4)
    # Batería de contadores en fachada sur
    r_cont = patches.Rectangle((0.30, -0.10), 0.80, 0.20, facecolor="#0284C7", edgecolor="#0369A1", lw=0.7, zorder=10)
    ax.add_patch(r_cont)
    ax.text(0.70, -0.30, "BATERÍA CONTADORES", ha='center', va='top', fontsize=4.8, color="#0284C7", zorder=11)

    # Depósito Interacumulador ACS 200L en Garaje
    circ_acs = patches.Circle((10.85, 15.20), 0.35, facecolor="#EF4444", edgecolor="#B91C1C", lw=0.8, zorder=10)
    ax.add_patch(circ_acs)
    ax.text(10.85, 15.20, "ACS\n200L", ha='center', va='center', fontsize=4.8, weight='bold', color="#FFFFFF", zorder=11)

    # Trazado de tuberías multicapa PEX aisladas
    ax.plot([0.70, 0.70, 10.85], [-0.10, 15.20, 15.20], color="#0284C7", lw=1.2, linestyle=':', zorder=8)
    ax.text(5.50, 8.50, "RED GENERAL DE AGUA FRÍA Y RETORNO ACS (PEX Ø25)", ha='center', va='center', fontsize=5.2, color="#0284C7", rotation=90)

    # 3. Ventilación Mecánica Controlada VMC (DB-HS3)
    # Recuperador de calor de doble flujo en techo de garaje
    r_vmc = patches.Rectangle((9.50, 16.00), 0.80, 0.60, facecolor="#10B981", edgecolor="#047857", lw=0.8, zorder=10)
    ax.add_patch(r_vmc)
    ax.text(9.90, 16.30, "VMC DOBLE FLUJO\n(Eficiencia > 85%)", ha='center', va='center', fontsize=4.5, weight='bold', color="#FFFFFF", zorder=11)

    # Red de bocas de extracción (baños/cocinas) y admisión (salón/dormitorios)
    extracciones = [(2.00, 9.50), (5.50, 9.50), (9.00, 2.00)]
    for ex_x, ex_y in extracciones:
        circ_ex = patches.Circle((ex_x, ex_y), 0.18, facecolor="#EF4444", edgecolor="#B91C1C", lw=0.6, zorder=12)
        ax.add_patch(circ_ex)
        ax.text(ex_x, ex_y - 0.25, "Extracción Ø125", ha='center', va='top', fontsize=4.2, color="#B91C1C", zorder=13)

    admisiones = [(3.00, 2.00), (3.00, 11.50), (1.50, 16.00), (4.50, 16.00)]
    for ad_x, ad_y in admisiones:
        circ_ad = patches.Circle((ad_x, ad_y), 0.18, facecolor="#3B82F6", edgecolor="#1D4ED8", lw=0.6, zorder=12)
        ax.add_patch(circ_ad)
        ax.text(ad_x, ad_y + 0.25, "Admisión Ø100", ha='center', va='bottom', fontsize=4.2, color="#1D4ED8", zorder=13)

    # 4. Seguridad Contra Incendios (DB-SI)
    # Extintores 21A-113B en pasillo y garaje
    for ext_x, ext_y in [(0.40, 7.60), (7.00, 13.50)]:
        r_ext = patches.Rectangle((ext_x - 0.15, ext_y - 0.15), 0.30, 0.30, facecolor="#DC2626", edgecolor="#7F1D1D", lw=0.7, zorder=14)
        ax.add_patch(r_ext)
        ax.text(ext_x, ext_y, "EXT", ha='center', va='center', fontsize=4.5, weight='bold', color="#FFFFFF", zorder=15)

    # Leyenda de instalaciones
    cs_x, cs_y = -4.80, 2.50
    patches_rect = patches.Rectangle((cs_x, cs_y), 4.20, 8.50, facecolor="#FFFFFF", edgecolor=C_WALL, lw=0.9, zorder=20)
    ax.add_patch(patches_rect)
    ax.text(cs_x + 2.10, cs_y + 8.10, "SIMBOLOGÍA DE INSTALACIONES (CTE)", ha='center', va='center', fontsize=6.2, weight='bold', color=C_TEXT_MAIN)
    leyenda = [
        ("CGMP", "Cuadro Eléctrico General con IGA, ID y PIAs"),
        ("Wallbox", "Recarga VE Tipo 2 Modo 3 (7,4 kW) REBT ITC-BT-52"),
        ("Aerotermia", "Bomba de Calor Inverter Clase A+++ (COP > 4.2)"),
        ("ACS 200L", "Interacumulador Vitrificado con Apoyo Solar"),
        ("VMC", "Ventilación Mecánica Doble Flujo DB-HS3"),
        ("Admisión", "Boca de impulsión de aire filtrado en estancias secas"),
        ("Extracción", "Boca de extracción de aire viciado en húmedas"),
        ("EXT 21A", "Extintor de polvo polivalente ABC 6 kg (DB-SI)")
    ]
    for idx, (cod, desc) in enumerate(leyenda):
        ax.text(cs_x + 0.20, cs_y + 7.30 - idx * 0.85, f"[{cod}]", ha='left', va='center', fontsize=5.2, weight='bold', color="#1E40AF")
        ax.text(cs_x + 0.20, cs_y + 6.95 - idx * 0.85, desc, ha='left', va='center', fontsize=4.5, color="#475569")

    draw_cajetin(ax, "P-07", "INSTALACIONES GENERALES", "Climatización Aerotérmica, Suelo Radiante, VMC, Electricidad, Wallbox y Fontanería", "1:75")

    plt.savefig(os.path.join(OUTPUT_DIR, "07_plano_instalaciones.png"), bbox_inches='tight', dpi=300)
    plt.savefig(os.path.join(OUTPUT_DIR, "07_plano_instalaciones.pdf"), bbox_inches='tight')
    plt.close(fig)
    print("PLANO P-07 INSTALACIONES GENERADO.")

if __name__ == "__main__":
    generar_plano_cubiertas()
    generar_plano_alzados()
    generar_plano_secciones()
    generar_plano_estructura()
    generar_plano_instalaciones()
    print("COLECCIÓN COMPLETA DE PLANOS TÉCNICOS GENERADA CON ÉXITO.")
