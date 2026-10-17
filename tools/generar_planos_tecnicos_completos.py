# -*- coding: utf-8 -*-
"""
GENERADOR INTEGRAL DE PLANOS TÉCNICOS ARQUITECTÓNICOS EJECUTIVOS (CORREGIDO Y AUDITADO)
Adaptado a la Estrategia Legal OPCIÓN A (Palma del Río, Córdoba):
- P-00: SITUACIÓN, EMPLAZAMIENTO Y JUSTIFICACIÓN URBANÍSTICA PGOU (Escala 1:100)
- P-02: PLANTA ALTA DIÁFANA EN BRUTO SIN USO DEFINIDO + PREINSTALACIONES (Escala 1:50)
- P-03: PLANTA DE CUBIERTAS Y EVACUACIÓN DE PLUVIALES (Escala 1:100)
- P-04: ALZADOS EXTERIORES SUR (MORENO TORROBA) Y NORTE (VIAL GARAJE) (Escala 1:100)
- P-05: SECCIONES CONSTRUCTIVAS A-A' Y B-B' ACOTADAS (Escala 1:75)
- P-06: CIMENTACIÓN, ESTRUCTURA Y RED DE SANEAMIENTO ENTERRADA (Escala 1:75)
- P-07: INSTALACIONES GENERALES DE PLANTA BAJA Y ACOMETIDAS (CTE DB-HE / HS / SI) (Escala 1:75)
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
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


def draw_cajetin(ax, num_plano, titulo_plano, desc_plano, escala="1:100", caj_x=-5.00, caj_y=-4.90, caj_w=22.00, caj_h=1.75):
    r = patches.Rectangle((caj_x, caj_y), caj_w, caj_h, facecolor="#FFFFFF", edgecolor=C_WALL, linewidth=1.3, zorder=40)
    ax.add_patch(r)
    ax.plot([caj_x + 6.9, caj_x + 6.9], [caj_y, caj_y + caj_h], color=C_WALL, lw=0.8, zorder=41)
    ax.plot([caj_x + 15.6, caj_x + 15.6], [caj_y, caj_y + caj_h], color=C_WALL, lw=0.8, zorder=41)
    ax.plot([caj_x + 18.9, caj_x + 18.9], [caj_y, caj_y + caj_h], color=C_WALL, lw=0.8, zorder=41)

    ax.text(caj_x + 0.25, caj_y + 1.28, "PROYECTO BÁSICO Y DE EJECUCIÓN", fontsize=8.8, weight='bold', color=C_TEXT_MAIN, zorder=42)
    ax.text(caj_x + 0.25, caj_y + 0.85, "Vivienda Unifamiliar en PB + Espacio en Bruto en PA", fontsize=6.8, color=C_TEXT_SEC, zorder=42)
    ax.text(caj_x + 0.25, caj_y + 0.42, "Calle Moreno Torroba s/n · Palma del Río (Córdoba)", fontsize=6.8, weight='bold', color="#1E40AF", zorder=42)

    ax.text(caj_x + 7.15, caj_y + 1.28, f"PLANO: {titulo_plano}", fontsize=8.2, weight='bold', color=C_TEXT_MAIN, zorder=42)
    ax.text(caj_x + 7.15, caj_y + 0.85, desc_plano, fontsize=6.4, color=C_TEXT_SEC, zorder=42)
    ax.text(caj_x + 7.15, caj_y + 0.42, "Documento Reglamentario CTE · Solicitud Licencia de Obras", fontsize=6.4, weight='bold', color=C_TEXT_MAIN, zorder=42)

    ax.text(caj_x + 15.80, caj_y + 1.28, f"ESCALA: {escala}", fontsize=8.0, weight='bold', color=C_TEXT_MAIN, zorder=42)
    ax.text(caj_x + 15.80, caj_y + 0.85, "FECHA: Octubre 2026", fontsize=6.6, color=C_TEXT_SEC, zorder=42)
    ax.text(caj_x + 15.80, caj_y + 0.42, "FORMATO: DIN A3", fontsize=6.6, color=C_TEXT_SEC, zorder=42)

    r_num = patches.Rectangle((caj_x + 18.9, caj_y), 3.10, caj_h, facecolor=C_WALL, edgecolor=C_WALL, zorder=41)
    ax.add_patch(r_num)
    ax.text(caj_x + 20.45, caj_y + 1.20, "PLANO Nº", ha='center', va='center', fontsize=7.0, weight='bold', color="#94A3B8", zorder=42)
    ax.text(caj_x + 20.45, caj_y + 0.58, num_plano, ha='center', va='center', fontsize=16, weight='bold', color="#FFFFFF", zorder=42)


def draw_cota_h(ax, x1, x2, y, val_str, offset=0.14, tick=0.08):
    if x1 > x2:
        x1, x2 = x2, x1
    ax.plot([x1, x2], [y, y], color=C_DIM_LINE, lw=0.6, zorder=30)
    ax.plot([x1 - tick, x1 + tick], [y - tick, y + tick], color=C_DIM, lw=1.1, zorder=31)
    ax.plot([x2 - tick, x2 + tick], [y - tick, y + tick], color=C_DIM, lw=1.1, zorder=31)
    ax.text((x1 + x2) / 2.0, y + offset, val_str, ha='center', va='bottom', fontsize=6.5, color=C_DIM, weight='bold', zorder=32,
            bbox=dict(boxstyle='square,pad=0.06', facecolor='#FFFFFF', edgecolor='none', alpha=0.92))


def draw_cota_v(ax, y1, y2, x, val_str, offset=0.18, tick=0.08):
    if y1 > y2:
        y1, y2 = y2, y1
    ax.plot([x, x], [y1, y2], color=C_DIM_LINE, lw=0.6, zorder=30)
    ax.plot([x - tick, x + tick], [y1 - tick, y1 + tick], color=C_DIM, lw=1.1, zorder=31)
    ax.plot([x - tick, x + tick], [y2 - tick, y2 + tick], color=C_DIM, lw=1.1, zorder=31)
    ax.text(x - offset, (y1 + y2) / 2.0, val_str, ha='right', va='center', fontsize=6.5, color=C_DIM, weight='bold', rotation=90, zorder=32,
            bbox=dict(boxstyle='square,pad=0.06', facecolor='#FFFFFF', edgecolor='none', alpha=0.92))


# ==============================================================================
# 0. PLANO P-00: EMPLAZAMIENTO, OCUPACIÓN (80%) Y FICHA URBANÍSTICA PGOU
# ==============================================================================
def generar_plano_emplazamiento():
    fig, ax = setup_canvas()
    ax.set_xlim(-5.2, 17.2)
    ax.set_ylim(-5.5, 21.8)

    # Viales públicos Sur y Norte
    ax.text(5.70, -1.55, "CALLE MORENO TORROBA (FACHADA PRINCIPAL SUR · ACCESO PEATONAL)", ha='center', va='center', fontsize=7.5, weight='bold', color="#1E40AF", zorder=20)
    ax.text(5.70, 19.10, "VIAL PÚBLICO SECUNDARIO TRASERO (FACHADA NORTE · ACCESO RODADO COCHERA)", ha='center', va='center', fontsize=7.5, weight='bold', color="#1E40AF", zorder=20)

    # Huella edificada (80% = 160,51 m²)
    r_parcela = patches.Rectangle((0.00, 0.00), 11.40, 17.60, facecolor="#E2E8F0", edgecolor=C_WALL, lw=1.6, zorder=5)
    ax.add_patch(r_parcela)
    ax.text(3.20, 8.80, "HUELLA EDIFICADA COMPUTABLE\nOcupación = 80,0 % (160,51 m²)\nAlturas: B + 1 (5,85 m <= 7,20 m)", ha='center', va='center', fontsize=6.8, weight='bold', color=C_TEXT_MAIN, zorder=10)

    # Patio interior central (5,00 x 8,00 m = 40,00 m² -> 20% libre)
    r_patio = patches.Rectangle((6.40, 5.00), 5.00, 8.00, facecolor="#ECFDF5", edgecolor="#047857", lw=1.3, zorder=6)
    ax.add_patch(r_patio)

    # Círculo inscribible obligatorio PGOU (Ø 3,00 m mínimo; cabe Ø 5,00 m)
    c_insc = patches.Circle((8.90, 9.00), 2.50, facecolor="none", edgecolor="#DC2626", lw=1.1, linestyle='--', zorder=8)
    c_min = patches.Circle((8.90, 9.00), 1.50, facecolor="none", edgecolor="#0284C7", lw=1.0, linestyle=':', zorder=8)
    ax.add_patch(c_insc)
    ax.add_patch(c_min)
    ax.text(8.90, 9.00, "PATIO INTERIOR PRIVATIVO\n5,00 × 8,00 m = 40,00 m² (20%)\nØ Inscribible Real = 5,00 m\n(Mín. PGOU Ø 3,00 m)", ha='center', va='center', fontsize=5.8, weight='bold', color="#047857", zorder=10)

    # Cotas generales del solar
    draw_cota_h(ax, 0.00, 11.40, -0.75, "11,40 m (FACHADA SUR)")
    draw_cota_h(ax, 0.00, 6.40, 18.20, "6,40 m (Crujía Oeste)")
    draw_cota_h(ax, 6.40, 11.40, 18.20, "5,00 m (Crujía Patio/Cochera)")
    draw_cota_v(ax, 0.00, 17.60, -0.75, "17,60 m (FONDO TOTAL PARCELA)")
    draw_cota_v(ax, 0.00, 5.00, 12.25, "5,00 m (Sur)", offset=-0.20)
    draw_cota_v(ax, 5.00, 13.00, 12.25, "8,00 m (Patio)", offset=-0.20)
    draw_cota_v(ax, 13.00, 17.60, 12.25, "4,60 m (Norte)", offset=-0.20)

    # Cuadro de Justificación Urbanística a la izquierda (zorder=25 para texto sobre fondo zorder=20)
    cs_x, cs_y = -5.00, 3.50
    r_cuad = patches.Rectangle((cs_x, cs_y), 4.00, 9.20, facecolor="#FFFFFF", edgecolor=C_WALL, lw=0.9, zorder=20)
    ax.add_patch(r_cuad)
    ax.text(cs_x + 2.00, cs_y + 8.70, "PARÁMETROS PGOU PALMA DEL RÍO", ha='center', va='center', fontsize=6.2, weight='bold', color=C_TEXT_MAIN, zorder=25)
    datos_urb = [
        "Clasificación: Suelo Urbano Consolidado",
        "Uso Global: Residencial entre medianeras",
        "Solar: 11,40 × 17,60 m = 200,64 m²",
        "Ocupación Máx. PGOU: 80 % (160,51 m²)",
        "Ocupación Proyecto: 80,0 % (CUMPLE)",
        "Espacio Libre Patio: 40,13 m² (20,0 %)",
        "Diámetro Inscribible Patio: 5,00 m >= 3,00 m",
        "Altura Máx. Cornisa: 7,20 m (B+1)",
        "Altura Proyecto: 5,85 m (B+1) (CUMPLE)",
        "Modalidad: PB Terminada + PA en Bruto",
        "Aparcamiento: 1 Plaza en PB (21,14 m²)"
    ]
    for i, txt in enumerate(datos_urb):
        ax.text(cs_x + 0.18, cs_y + 8.00 - i * 0.72, f"• {txt}", ha='left', va='center', fontsize=4.8, color="#334155", zorder=25)

    draw_cajetin(ax, "P-00", "EMPLAZAMIENTO, PARCELA Y JUSTIFICACIÓN PGOU", "Alineaciones, Ocupación en Planta (80%), Patio Central y Cuadro Urbanístico", "1:100")

    plt.savefig(os.path.join(OUTPUT_DIR, "00_plano_emplazamiento_pgou.png"), bbox_inches='tight', dpi=300)
    plt.savefig(os.path.join(OUTPUT_DIR, "00_plano_emplazamiento_pgou.pdf"), bbox_inches='tight')
    plt.close(fig)
    print("PLANO P-00 EMPLAZAMIENTO GENERADO.")


# ==============================================================================
# 1. PLANO P-02: PLANTA ALTA DIÁFANA EN BRUTO (OPCIÓN A)
# ==============================================================================
def generar_plano_planta_alta_bruto():
    fig, ax = setup_canvas()
    ax.set_xlim(-5.2, 17.2)
    ax.set_ylim(-5.5, 21.8)

    # Contorno general de Planta Alta (11,40 x 17,60 m)
    r_pa = patches.Rectangle((0.00, 0.00), 11.40, 17.60, facecolor="#F8FAFC", edgecolor=C_WALL, lw=1.8, zorder=4)
    ax.add_patch(r_pa)

    # Vacío del Patio Central (X = 6,40 a 11,40; Y = 7,40 a 13,00)
    r_vacio = patches.Rectangle((6.40, 7.40), 5.00, 5.60, facecolor="#E0F2FE", edgecolor=C_WALL, lw=1.5, zorder=6)
    ax.add_patch(r_vacio)
    ax.plot([6.40, 11.40], [7.40, 13.00], color="#0284C7", lw=0.7, linestyle='--', zorder=7)
    ax.plot([6.40, 11.40], [13.00, 7.40], color="#0284C7", lw=0.7, linestyle='--', zorder=7)
    ax.text(8.90, 10.20, "VACÍO SOBRE PATIO Y PISCINA (PB)\nPetos y barandilla de seguridad h=1,10 m", ha='center', va='center', fontsize=6.2, weight='bold', color="#0369A1", zorder=10)

    # Terraza Solárium Exterior Impermeabilizada al Norte-Oeste (X = 0,00 a 3,20; Y = 13,80 a 17,60)
    r_solarium = patches.Rectangle((0.25, 13.80), 3.15, 3.55, facecolor="#FEF3C7", edgecolor=C_WALL, lw=1.2, zorder=6)
    ax.add_patch(r_solarium)
    ax.text(1.82, 15.55, "TERRAZA EXTERIOR\nIMPERMEABILIZADA\nS.Útil: 12,16 m²\n(Estanqueidad techo PB)", ha='center', va='center', fontsize=5.5, weight='bold', color="#92400E", zorder=10)

    # Desembarco de Escalera Independiente (X = 10,15 a 11,40; Y = 0,00 a 5,00)
    r_esc = patches.Rectangle((10.15, 0.25), 1.00, 4.75, facecolor="#E2E8F0", edgecolor=C_WALL, lw=1.2, zorder=6)
    ax.add_patch(r_esc)
    for sy in [0.60 + k * 0.28 for k in range(15)]:
        ax.plot([10.15, 11.15], [sy, sy], color="#475569", lw=0.6, zorder=7)
    ax.text(10.65, 5.35, "DESEMBARCO ESCALERA\nPuerta EI2 60-C5 con llave\n(Acceso cerrado en Fase 1)", ha='center', va='bottom', fontsize=5.0, weight='bold', color="#B91C1C", zorder=10)

    # Patinillos de Preinstalaciones (Acometidas taponadas para futura adecuación)
    for px, py, txt in [(5.80, 8.20, "PATINILLO 1\nBajante Ø110 + AF/ACS\ntaponadas"), (9.60, 4.80, "PATINILLO 2\nBajante Ø110 + Tubos\neléctricos/ICT en espera")]:
        r_pat = patches.Rectangle((px, py), 0.45, 0.45, facecolor="#FCA5A5", edgecolor="#B91C1C", lw=0.9, zorder=8)
        ax.add_patch(r_pat)
        ax.text(px - 0.15, py + 0.22, txt, ha='right', va='center', fontsize=4.8, weight='bold', color="#991B1B", zorder=10)

    # Pilares vistos en el espacio en bruto
    for px, py in [(0.15, 7.40), (6.40, 7.40), (0.15, 13.00), (6.40, 13.00)]:
        r_pil = patches.Rectangle((px - 0.15, py - 0.15), 0.30, 0.30, facecolor="#1E293B", edgecolor=C_WALL, lw=0.8, zorder=9)
        ax.add_patch(r_pil)

    # Texto central del espacio diáfano en bruto
    ax.text(3.30, 6.20,
            "ESPACIO DIÁFANO EN BRUTO · SIN USO DEFINIDO\n"
            "(NO HABILITADO EN ESTA FASE · EXCLUIDO DE LPO DE PLANTA BAJA)\n\n"
            "• Superficie útil en bruto: 132,73 m² | Construida: 154,60 m²\n"
            "• Estructura, forjado superior y cubierta 100 % terminados\n"
            "• Fachadas exteriores y carpinterías con vidrio 100 % instaladas\n"
            "• Interior en bruto sin solados, sin tabiquería y sin instalaciones activas",
            ha='center', va='center', fontsize=6.4, weight='bold', color="#1E293B", zorder=12,
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#FFFFFF', edgecolor='#0F172A', lw=1.0))

    ax.text(8.80, 15.20, "ZONA NORTE-ESTE EN BRUTO\n(Sobre Cochera PB · 21,14 m²)\nEstructura y cerramiento 100% terminados",
            ha='center', va='center', fontsize=5.8, weight='bold', color="#334155", zorder=12)

    # Cotas exteriores
    draw_cota_h(ax, 0.00, 11.40, -0.75, "11,40 m (FACHADA SUR)")
    draw_cota_v(ax, 0.00, 17.60, -0.75, "17,60 m (LONGITUD PARCELA)")

    # Cuadro de superficies izquierdo
    cs_x, cs_y = -5.00, 3.50
    r_cuad = patches.Rectangle((cs_x, cs_y), 4.00, 8.50, facecolor="#FFFFFF", edgecolor=C_WALL, lw=0.9, zorder=20)
    ax.add_patch(r_cuad)
    ax.text(cs_x + 2.00, cs_y + 8.00, "CUADRO SUPERFICIES PLANTA ALTA", ha='center', va='center', fontsize=6.0, weight='bold', color=C_TEXT_MAIN, zorder=25)
    filas_pa = [
        ("Régimen Licencia:", "Espacio en Bruto"),
        ("Uso declarado Fase 1:", "Sin uso definido"),
        ("Espacio Diáfano Bruto:", "132,73 m²"),
        ("Desembarco Escalera:", "4,50 m²"),
        ("TOTAL ÚTIL CERRADA PA:", "137,23 m²"),
        ("Terraza Impermeab.:", "12,16 m²"),
        ("Vacío Patio Central:", "28,00 m²"),
        ("SUP. CONSTRUIDA PA:", "154,60 m²"),
    ]
    for i, (k, v) in enumerate(filas_pa):
        ax.text(cs_x + 0.15, cs_y + 7.20 - i * 0.82, k, ha='left', va='center', fontsize=5.0, weight='bold', color="#334155", zorder=25)
        ax.text(cs_x + 3.85, cs_y + 7.20 - i * 0.82, v, ha='right', va='center', fontsize=5.0, color="#0F172A", zorder=25)

    draw_cajetin(ax, "P-02", "PLANTA ALTA · ESPACIO DIÁFANO EN BRUTO (SIN USO)", "Envolvente Exterior Terminada, Terraza Impermeabilizada y Acometidas en Espera", "1:50")

    plt.savefig(os.path.join(OUTPUT_DIR, "02_plano_arquitecto_planta_alta_bruto.png"), bbox_inches='tight', dpi=300)
    plt.savefig(os.path.join(OUTPUT_DIR, "02_plano_arquitecto_planta_alta_bruto.pdf"), bbox_inches='tight')
    plt.close(fig)
    print("PLANO P-02 PLANTA ALTA EN BRUTO GENERADO.")


# ==============================================================================
# 2. PLANO P-03: PLANTA DE CUBIERTAS E INSTALACIONES TÉCNICAS (CORREGIDO)
# ==============================================================================
def generar_plano_cubiertas():
    fig, ax = setup_canvas()
    ax.set_xlim(-5.2, 17.2)
    ax.set_ylim(-5.5, 21.8)

    # Base de cubierta (11,40 x 17,60 m exactos)
    r_base = patches.Rectangle((0.00, 0.00), 11.40, 17.60, facecolor="#E2E8F0", edgecolor=C_WALL, lw=1.6, zorder=4)
    ax.add_patch(r_base)

    # Peto perimetral interior
    r_peto = patches.Rectangle((0.30, 0.30), 10.80, 17.00, facecolor="#F8FAFC", edgecolor="#64748B", lw=0.8, linestyle='--', zorder=5)
    ax.add_patch(r_peto)

    # Zona Patio Vacío (sin techar) en zorder=8
    r_patio = patches.Rectangle((6.40, 7.40), 5.00, 5.60, facecolor="#BAE6FD", edgecolor=C_WALL, lw=1.4, zorder=8)
    ax.add_patch(r_patio)
    ax.plot([6.40, 11.40], [7.40, 13.00], color="#0284C7", lw=0.7, linestyle='--', zorder=9)
    ax.plot([6.40, 11.40], [13.00, 7.40], color="#0284C7", lw=0.7, linestyle='--', zorder=9)
    ax.text(8.90, 10.20, "VACÍO PATIO / PISCINA\n(SIN TECHAR)\n5,00 × 5,60 m", ha='center', va='center', fontsize=6.5, weight='bold', color="#0369A1", zorder=11)

    # Pendientes de faldones (i = 1,5%)
    for x, y, dx, dy in [(3.20, 3.00, 0, -1.3), (3.20, 10.50, 0, 1.5), (8.60, 2.80, 0, -1.2), (8.60, 14.50, 0, 1.3)]:
        ax.annotate('', xy=(x + dx, y + dy), xytext=(x, y),
                    arrowprops=dict(arrowstyle='->', color="#334155", lw=1.3), zorder=12)
        ax.text(x + 0.65, y + dy / 2.0, "i = 1,5 %", ha='left', va='center', fontsize=5.8, weight='bold', color="#334155", zorder=13)

    # Sumideros sifónicos Ø110
    sumideros = [
        (1.00, 0.90, "S-01 Ø110"), (5.10, 0.90, "S-02 Ø110"), (7.20, 0.90, "S-03 Ø110"), (10.20, 0.90, "S-04 Ø110"),
        (1.00, 16.60, "S-05 Ø110"), (5.10, 16.60, "S-06 Ø110"), (7.20, 16.60, "S-07 Ø110"), (10.20, 16.60, "S-08 Ø110")
    ]
    for sx, sy, lbl in sumideros:
        circ = patches.Circle((sx, sy), 0.22, facecolor="#0284C7", edgecolor="#0369A1", lw=0.8, zorder=14)
        ax.add_patch(circ)
        ax.text(sx, sy, "S", ha='center', va='center', fontsize=4.8, weight='bold', color="#FFFFFF", zorder=15)
        ax.text(sx, sy + (0.38 if sy < 8 else -0.38), lbl, ha='center', va='center', fontsize=4.6, weight='bold', color="#0369A1", zorder=15)

    # Campo Solar Fotovoltaico (10 Paneles orientados al Sur, 4,5 kWp)
    for i in range(5):
        for j in range(2):
            px = 0.95 + i * 1.02
            py = 3.60 + j * 1.75
            r_pan = patches.Rectangle((px, py), 0.92, 1.55, facecolor="#1E3A8A", edgecolor="#93C5FD", lw=0.7, zorder=15)
            ax.add_patch(r_pan)
            ax.plot([px, px + 0.92], [py + 0.77, py + 0.77], color="#60A5FA", lw=0.4, zorder=16)
    ax.text(3.45, 7.25, "CAMPO SOLAR FOTOVOLTAICO AUTOCONSUMO (10 MÓDULOS · 4,50 kWp)", ha='center', va='bottom', fontsize=5.8, weight='bold', color="#1E3A8A", zorder=17)

    # Unidad Exterior de Aerotermia PB + Bancada Reserva PA
    r_aero1 = patches.Rectangle((7.00, 3.20), 1.40, 0.75, facecolor="#334155", edgecolor="#0F172A", lw=0.9, zorder=15)
    c_fan1 = patches.Circle((7.70, 3.57), 0.26, facecolor="#64748B", edgecolor="#CBD5E1", lw=0.5, zorder=16)
    ax.add_patch(r_aero1); ax.add_patch(c_fan1)
    ax.text(7.70, 2.95, "AEROTERMIA PB\n(Activa Fase 1)", ha='center', va='top', fontsize=4.8, weight='bold', color="#0F172A", zorder=17)

    r_aero2 = patches.Rectangle((9.10, 3.20), 1.40, 0.75, facecolor="none", edgecolor="#64748B", lw=0.9, linestyle='--', zorder=15)
    ax.add_patch(r_aero2)
    ax.text(9.80, 2.95, "BANCADA RESERVA PA\n(Preinstalación)", ha='center', va='top', fontsize=4.8, color="#475569", zorder=17)

    draw_cota_h(ax, 0.00, 11.40, -0.75, "11,40 m (ANCHURA CUBIERTA)")
    draw_cota_v(ax, 0.00, 17.60, -0.75, "17,60 m (LONGITUD CUBIERTA)")

    draw_cajetin(ax, "P-03", "PLANTA DE CUBIERTAS E INSTALACIONES", "Cubierta Plana Invertida (XPS 100 mm), Sumideros Sifónicos, Aerotermia y Fotovoltaica", "1:100")

    plt.savefig(os.path.join(OUTPUT_DIR, "03_plano_cubiertas.png"), bbox_inches='tight', dpi=300)
    plt.savefig(os.path.join(OUTPUT_DIR, "03_plano_cubiertas.pdf"), bbox_inches='tight')
    plt.close(fig)
    print("PLANO P-03 CUBIERTAS GENERADO.")


# ==============================================================================
# 3. PLANO P-04: ALZADOS EXTERIORES SUR Y NORTE
# ==============================================================================
def generar_plano_alzados():
    fig, ax = setup_canvas()
    ax.set_xlim(-5.2, 17.2)
    ax.set_ylim(-5.5, 21.8)

    # 1. ALZADO PRINCIPAL SUR (Calle Moreno Torroba)
    y_base_s = 12.00
    ax.plot([-1.5, 13.0], [y_base_s, y_base_s], color="#0F172A", lw=2.0, zorder=10)
    r_fach_s = patches.Rectangle((0.0, y_base_s), 11.40, 5.85, facecolor="#F8FAFC", edgecolor=C_WALL, lw=1.4, zorder=5)
    ax.add_patch(r_fach_s)
    ax.plot([0.0, 11.40], [y_base_s + 2.90, y_base_s + 2.90], color="#94A3B8", lw=0.8, linestyle='--', zorder=6)

    # Huecos PB Sur
    # Portal Vivienda PB (A)
    r_pa = patches.Rectangle((0.30, y_base_s), 1.00, 2.20, facecolor="#C46D29", edgecolor="#7C2D12", lw=0.9, zorder=7)
    ax.add_patch(r_pa)
    ax.text(0.80, y_base_s + 1.10, "ACCESO\nVIVIENDA PB", ha='center', va='center', fontsize=4.6, weight='bold', color="#FFFFFF", rotation=90, zorder=8)

    # Ventanales Salón y Cocina PB
    for vx, vw in [(2.60, 1.80), (4.80, 1.20), (6.80, 1.40), (8.60, 1.20)]:
        r_v = patches.Rectangle((vx, y_base_s + 0.90), vw, 1.40, facecolor=C_GLASS, edgecolor="#0369A1", lw=0.8, zorder=7)
        ax.add_patch(r_v)

    # Portal Escalera PA
    r_pb = patches.Rectangle((10.15, y_base_s), 1.00, 2.20, facecolor="#334155", edgecolor="#0F172A", lw=0.9, zorder=7)
    ax.add_patch(r_pb)
    ax.text(10.65, y_base_s + 1.10, "ACCESO\nPLANTA ALTA", ha='center', va='center', fontsize=4.6, weight='bold', color="#FFFFFF", rotation=90, zorder=8)

    # Huecos Planta Alta Sur (Vidrios instalados 100% para ornato y estanqueidad)
    for vx, vw in [(2.60, 1.80), (4.80, 1.20), (6.80, 1.40), (8.60, 1.20)]:
        r_va = patches.Rectangle((vx, y_base_s + 3.80), vw, 1.40, facecolor=C_GLASS, edgecolor="#0369A1", lw=0.8, zorder=7)
        ax.add_patch(r_va)
    r_va_esc = patches.Rectangle((10.25, y_base_s + 3.40), 0.80, 1.80, facecolor=C_GLASS, edgecolor="#0369A1", lw=0.8, zorder=7)
    ax.add_patch(r_va_esc)

    ax.text(5.70, y_base_s + 6.30, "ALZADO PRINCIPAL SUR (CALLE MORENO TORROBA)", ha='center', va='bottom', fontsize=7.5, weight='bold', color=C_TEXT_MAIN)
    ax.text(-0.30, y_base_s, "+0,00", ha='right', va='center', fontsize=5.5, color="#64748B")
    ax.text(-0.30, y_base_s + 2.90, "+2,90 (Forjado PA)", ha='right', va='center', fontsize=5.5, color="#64748B")
    ax.text(-0.30, y_base_s + 5.85, "+5,85 (Cornisa)", ha='right', va='center', fontsize=5.5, color="#64748B")

    # 2. ALZADO TRASERO NORTE (Vial Secundario - Garaje)
    y_base_n = 2.00
    ax.plot([-1.5, 13.0], [y_base_n, y_base_n], color="#0F172A", lw=2.0, zorder=10)
    r_fach_n = patches.Rectangle((0.0, y_base_n), 11.40, 5.85, facecolor="#F8FAFC", edgecolor=C_WALL, lw=1.4, zorder=5)
    ax.add_patch(r_fach_n)
    ax.plot([0.0, 11.40], [y_base_n + 2.90, y_base_n + 2.90], color="#94A3B8", lw=0.8, linestyle='--', zorder=6)

    # Huecos PB Norte
    r_gar = patches.Rectangle((6.55, y_base_n), 4.60, 2.40, facecolor="#334155", edgecolor="#0F172A", lw=1.0, zorder=7)
    ax.add_patch(r_gar)
    ax.text(8.85, y_base_n + 1.20, "PORTÓN COCHERA AUTOMÁTICO MOTORIZADO", ha='center', va='center', fontsize=5.2, weight='bold', color="#FFFFFF", zorder=8)

    for vx, vw in [(0.80, 1.60), (3.60, 1.60)]:
        r_vn = patches.Rectangle((vx, y_base_n + 0.90), vw, 1.40, facecolor=C_GLASS, edgecolor="#0369A1", lw=0.8, zorder=7)
        ax.add_patch(r_vn)

    # Huecos PA Norte (Terraza solárium y ventanales instalados)
    r_van1 = patches.Rectangle((0.80, y_base_n + 2.90), 1.60, 2.20, facecolor=C_GLASS, edgecolor="#0369A1", lw=0.8, zorder=7)
    r_van2 = patches.Rectangle((3.60, y_base_n + 3.80), 1.60, 1.40, facecolor=C_GLASS, edgecolor="#0369A1", lw=0.8, zorder=7)
    r_van3 = patches.Rectangle((7.00, y_base_n + 3.80), 2.00, 1.40, facecolor=C_GLASS, edgecolor="#0369A1", lw=0.8, zorder=7)
    r_van4 = patches.Rectangle((9.80, y_base_n + 3.80), 1.20, 1.40, facecolor=C_GLASS, edgecolor="#0369A1", lw=0.8, zorder=7)
    for p in [r_van1, r_van2, r_van3, r_van4]:
        ax.add_patch(p)

    ax.text(5.70, y_base_n + 6.30, "ALZADO TRASERO NORTE (VIAL ACCESO RODADO COCHERA)", ha='center', va='bottom', fontsize=7.5, weight='bold', color=C_TEXT_MAIN)

    draw_cajetin(ax, "P-04", "ALZADOS EXTERIORES GENERALES", "Alzado Principal Sur (Moreno Torroba) y Alzado Trasero Norte (Garaje)", "1:100")

    plt.savefig(os.path.join(OUTPUT_DIR, "04_plano_alzados.png"), bbox_inches='tight', dpi=300)
    plt.savefig(os.path.join(OUTPUT_DIR, "04_plano_alzados.pdf"), bbox_inches='tight')
    plt.close(fig)
    print("PLANO P-04 ALZADOS GENERADO.")


# ==============================================================================
# 4. PLANO P-05: SECCIONES CONSTRUCTIVAS LONGITUDINAL Y TRANSVERSAL
# ==============================================================================
def generar_plano_secciones():
    fig, ax = setup_canvas()
    ax.set_xlim(-5.2, 17.2)
    ax.set_ylim(-5.5, 21.8)

    # 1. SECCIÓN LONGITUDINAL A-A' (Y = 0.00 a 17.60 m)
    y_s = 9.50
    ax.plot([-1.5, 17.5], [y_s, y_s], color="#0F172A", lw=2.0, zorder=10)

    # Solera ventilada tipo Cáviti
    r_sol = patches.Rectangle((0.0, y_s - 0.40), 17.60, 0.40, facecolor="#CBD5E1", edgecolor=C_WALL, lw=1.0, zorder=5)
    ax.add_patch(r_sol)
    ax.text(8.80, y_s - 0.25, "SOLERA SANITARIA VENTILADA CÁVITI (h=40 cm) · BARRERA CAPILARIDAD Y RADÓN", ha='center', va='center', fontsize=5.2, weight='bold', color="#1E293B", zorder=25)

    # Espacios PB
    r_sal_pb = patches.Rectangle((0.0, y_s), 5.00, 2.60, facecolor="#FAF8F5", edgecolor=C_WALL, lw=0.8, zorder=6)
    r_pat_pb = patches.Rectangle((5.00, y_s), 8.00, 2.60, facecolor="#ECFDF5", edgecolor="none", zorder=4)
    r_coch_pb = patches.Rectangle((13.00, y_s), 4.60, 2.60, facecolor="#F1F3F5", edgecolor=C_WALL, lw=0.8, zorder=6)
    for p in [r_sal_pb, r_pat_pb, r_coch_pb]:
        ax.add_patch(p)

    # Piscina enterrada
    r_pisc = patches.Rectangle((7.00, y_s - 1.40), 3.80, 1.40, facecolor="#BAE6FD", edgecolor="#0284C7", lw=1.2, zorder=5)
    ax.add_patch(r_pisc)
    ax.text(8.90, y_s - 0.70, "VASO PISCINA (-1,40 m)\nHormigón Gunitado", ha='center', va='center', fontsize=5.2, weight='bold', color="#0369A1", zorder=25)

    # Forjados
    r_forj1 = patches.Rectangle((0.0, y_s + 2.60), 5.00, 0.30, facecolor="#94A3B8", edgecolor=C_WALL, lw=0.9, zorder=7)
    r_forj1_coch = patches.Rectangle((13.00, y_s + 2.60), 4.60, 0.30, facecolor="#94A3B8", edgecolor=C_WALL, lw=0.9, zorder=7)
    ax.add_patch(r_forj1); ax.add_patch(r_forj1_coch)

    # Planta Alta en bruto
    r_pa_sal = patches.Rectangle((0.0, y_s + 2.90), 5.00, 2.60, facecolor="#FCFAF7", edgecolor=C_WALL, lw=0.8, zorder=6)
    r_pa_d2 = patches.Rectangle((13.00, y_s + 2.90), 4.60, 2.60, facecolor="#FCFAF7", edgecolor=C_WALL, lw=0.8, zorder=6)
    ax.add_patch(r_pa_sal); ax.add_patch(r_pa_d2)

    # Forjado Cubierta y Petos
    r_forj_cub1 = patches.Rectangle((0.0, y_s + 5.50), 5.00, 0.35, facecolor="#64748B", edgecolor=C_WALL, lw=1.0, zorder=7)
    r_forj_cub2 = patches.Rectangle((13.00, y_s + 5.50), 4.60, 0.35, facecolor="#64748B", edgecolor=C_WALL, lw=1.0, zorder=7)
    ax.add_patch(r_forj_cub1); ax.add_patch(r_forj_cub2)

    # Cotas de altura libre (zorder=32)
    draw_cota_v(ax, y_s, y_s + 2.60, -0.60, "2,60 m libre (PB)")
    draw_cota_v(ax, y_s + 2.90, y_s + 5.50, -0.60, "2,60 m libre (PA)")
    draw_cota_v(ax, y_s, y_s + 5.85, -1.30, "5,85 m (TOTAL CORNISA)")

    ax.text(8.80, y_s + 6.30, "SECCIÓN LONGITUDINAL CONSTRUCTIVA A-A'", ha='center', va='bottom', fontsize=8.0, weight='bold', color=C_TEXT_MAIN, zorder=25)
    ax.text(2.50, y_s + 1.30, "SALÓN-COCINA PB\n(h=2,60 m útil)", ha='center', va='center', fontsize=5.8, weight='bold', color="#334155", zorder=25)
    ax.text(2.50, y_s + 4.20, "PLANTA ALTA EN BRUTO\n(Sin uso definido)", ha='center', va='center', fontsize=5.8, weight='bold', color="#334155", zorder=25)
    ax.text(15.30, y_s + 1.30, "COCHERA PB\n(EI 120 Riesgo Especial)", ha='center', va='center', fontsize=5.8, weight='bold', color="#334155", zorder=25)
    ax.text(15.30, y_s + 4.20, "PA EN BRUTO NORTE\n(Sin uso definido)", ha='center', va='center', fontsize=5.8, weight='bold', color="#334155", zorder=25)

    # 2. SECCIÓN TRANSVERSAL B-B' (Cimentación y Zapatas a -1,50 m)
    y_sec_b = 0.50
    ax.plot([-1.5, 13.0], [y_sec_b, y_sec_b], color="#0F172A", lw=2.0, zorder=10)
    r_sec_b = patches.Rectangle((0.0, y_sec_b), 11.40, 5.85, facecolor="#F8FAFC", edgecolor=C_WALL, lw=1.2, zorder=5)
    ax.add_patch(r_sec_b)

    for zx in [0.0, 5.70, 11.40]:
        r_zap = patches.Rectangle((zx - 0.70, y_sec_b - 1.50), 1.40, 0.80, facecolor="#94A3B8", edgecolor=C_WALL, lw=1.0, zorder=6)
        ax.add_patch(r_zap)
        ax.text(zx, y_sec_b - 1.10, "ZAPATA HA-25\n1,40×1,40×0,80 m\n(-1,50 m cota apoyo)", ha='center', va='center', fontsize=4.5, weight='bold', color="#FFFFFF", zorder=25)

    ax.text(5.70, y_sec_b + 6.15, "SECCIÓN TRANSVERSAL CONSTRUCTIVA B-B' (CRUJÍA CENTRAL Y CIMENTACIÓN)", ha='center', va='bottom', fontsize=7.5, weight='bold', color=C_TEXT_MAIN, zorder=25)

    draw_cajetin(ax, "P-05", "SECCIONES CONSTRUCTIVAS GENERALES", "Sección Longitudinal A-A' y Sección Transversal B-B' con Cimentación (-1,50 m) y Alturas", "1:75")

    plt.savefig(os.path.join(OUTPUT_DIR, "05_plano_secciones.png"), bbox_inches='tight', dpi=300)
    plt.savefig(os.path.join(OUTPUT_DIR, "05_plano_secciones.pdf"), bbox_inches='tight')
    plt.close(fig)
    print("PLANO P-05 SECCIONES GENERADO.")


# ==============================================================================
# 5. PLANO P-06: ESTRUCTURA Y CIMENTACIÓN (ALINEADA Y LEYENDA VISIBLE)
# ==============================================================================
def generar_plano_estructura():
    fig, ax = setup_canvas()
    ax.set_xlim(-5.2, 17.2)
    ax.set_ylim(-5.5, 21.8)

    # Contorno solar (11,40 x 17,60 m)
    r_sol = patches.Rectangle((0.00, 0.00), 11.40, 17.60, facecolor="#F8FAFC", edgecolor=C_WALL, lw=1.4, zorder=2)
    ax.add_patch(r_sol)

    # Zapatas corridas en medianeras
    r_zm_o = patches.Rectangle((-0.10, -0.10), 0.70, 17.80, facecolor="#CBD5E1", edgecolor="#475569", lw=0.9, zorder=4)
    r_zm_e = patches.Rectangle((10.80, -0.10), 0.70, 17.80, facecolor="#CBD5E1", edgecolor="#475569", lw=0.9, zorder=4)
    ax.add_patch(r_zm_o); ax.add_patch(r_zm_e)

    # Pilares alineados exactamente a líneas de carga reales (Y = 0,00, 5,00, 13,00, 17,60)
    pilares = [
        (0.00, 0.00), (6.40, 0.00), (10.40, 0.00), (11.40, 0.00),
        (0.00, 5.00), (6.40, 5.00), (11.40, 5.00),
        (0.00, 13.00), (6.40, 13.00), (11.40, 13.00),
        (0.00, 17.60), (6.40, 17.60), (11.40, 17.60)
    ]
    for px, py in pilares:
        r_z = patches.Rectangle((px - 0.60, py - 0.60), 1.20, 1.20, facecolor="#94A3B8", edgecolor="#334155", lw=0.9, zorder=5)
        ax.add_patch(r_z)
        r_pil = patches.Rectangle((px - 0.15, py - 0.15), 0.30, 0.30, facecolor="#1E293B", edgecolor="#0F172A", lw=0.7, zorder=6)
        ax.add_patch(r_pil)

    # Vigas riostras y centradoras
    for y in [0.00, 5.00, 13.00, 17.60]:
        ax.plot([0.00, 11.40], [y, y], color="#475569", lw=2.5, zorder=4)
    for x in [0.00, 6.40, 11.40]:
        ax.plot([x, x], [0.00, 17.60], color="#475569", lw=2.5, zorder=4)

    # Red de Saneamiento Enterrada
    arquetas = [
        (1.80, 8.50, "A-01"), (5.50, 8.50, "A-02"), (8.50, 2.00, "A-03"),
        (10.50, 14.00, "A-04"), (6.00, 16.50, "A-05"), (1.00, 0.50, "A-SIFÓNICA")
    ]
    for ax_x, ax_y, label in arquetas:
        r_arq = patches.Rectangle((ax_x - 0.25, ax_y - 0.25), 0.50, 0.50, facecolor="#EA580C", edgecolor="#9A3412", lw=0.8, zorder=8)
        ax.add_patch(r_arq)
        ax.text(ax_x, ax_y + 0.35, label, ha='center', va='bottom', fontsize=5.0, weight='bold', color="#9A3412", zorder=9)

    colectores = [
        ((5.50, 8.50), (1.80, 8.50)),
        ((1.80, 8.50), (1.00, 0.50)),
        ((8.50, 2.00), (1.00, 0.50)),
        ((10.50, 14.00), (6.00, 16.50)),
        ((6.00, 16.50), (1.80, 8.50)),
        ((1.00, 0.50), (0.75, -0.60))
    ]
    for p_ini, p_fin in colectores:
        ax.annotate('', xy=p_fin, xytext=p_ini,
                    arrowprops=dict(arrowstyle='->', color="#DC2626", lw=1.5, linestyle='--'), zorder=7)

    ax.text(0.75, -0.80, "ACOMETIDA GENERAL AL ALCANTARILLADO MUNICIPAL (Ø200)", ha='center', va='top', fontsize=5.5, weight='bold', color="#DC2626", zorder=25)

    # Cuadro de características estructurales CON zorder=25 EN TEXTOS
    cs_x, cs_y = -4.80, 3.50
    patches_rect = patches.Rectangle((cs_x, cs_y), 4.20, 8.00, facecolor="#FFFFFF", edgecolor=C_WALL, lw=0.9, zorder=20)
    ax.add_patch(patches_rect)
    ax.text(cs_x + 2.10, cs_y + 7.50, "CUADRO DE CONTROL DE ESTRUCTURA", ha='center', va='center', fontsize=6.2, weight='bold', color=C_TEXT_MAIN, zorder=25)
    specs = [
        "Normativa: Código Estructural (RD 470/2021)",
        "Hormigón Zapatas: HA-25/B/20/IIa",
        "Hormigón Vigas/Pilares: HA-25/B/20/IIa",
        "Acero Armaduras: B 500 S (soldable)",
        "Recubrimiento mínimo: 40 mm en zapatas",
        "Cota de cimentación: -1,50 m",
        "Tensión admisible terreno: 1,80 kg/cm²",
        "Solera Sanitaria: Tipo Cáviti h=40 cm",
        "Saneamiento: PVC SN4 Ø160 mm al 2,0%"
    ]
    for idx, s in enumerate(specs):
        ax.text(cs_x + 0.20, cs_y + 6.70 - idx * 0.72, f"• {s}", ha='left', va='center', fontsize=5.0, color="#334155", zorder=25)

    draw_cajetin(ax, "P-06", "ESTRUCTURA Y CIMENTACIÓN", "Plano de Replanteo de Zapatas, Vigas Riostras y Red de Saneamiento Enterrada", "1:75")

    plt.savefig(os.path.join(OUTPUT_DIR, "06_plano_estructura.png"), bbox_inches='tight', dpi=300)
    plt.savefig(os.path.join(OUTPUT_DIR, "06_plano_estructura.pdf"), bbox_inches='tight')
    plt.close(fig)
    print("PLANO P-06 ESTRUCTURA GENERADO.")


# ==============================================================================
# 6. PLANO P-07: INSTALACIONES GENERALES (CTE DB-HE / DB-HS / DB-SI)
# ==============================================================================
def generar_plano_instalaciones():
    fig, ax = setup_canvas()
    ax.set_xlim(-5.2, 17.2)
    ax.set_ylim(-5.5, 21.8)

    r_sol = patches.Rectangle((0.00, 0.00), 11.40, 17.60, facecolor="#F8FAFC", edgecolor=C_WALL, lw=1.0, zorder=2)
    ax.add_patch(r_sol)

    # 1. Electricidad y Telecomunicaciones
    r_cgmp = patches.Rectangle((0.15, 0.40), 0.60, 0.25, facecolor="#EAB308", edgecolor="#A16207", lw=0.8, zorder=10)
    ax.add_patch(r_cgmp)
    ax.text(0.45, 0.80, "CGMP VIVIENDA PB", ha='center', va='bottom', fontsize=5.0, weight='bold', color="#A16207", zorder=25)

    # Punto de recarga Wallbox en Garaje (7.4 kW)
    r_wb = patches.Rectangle((6.55, 16.80), 0.35, 0.45, facecolor="#0284C7", edgecolor="#0369A1", lw=0.8, zorder=10)
    ax.add_patch(r_wb)
    ax.text(6.55, 17.40, "PUNTO RECARGA VE\n(Wallbox 7,4 kW ITC-BT-52)", ha='left', va='bottom', fontsize=5.0, weight='bold', color="#0284C7", zorder=25)

    # 2. Fontanería y ACS Aerotermia
    r_cont = patches.Rectangle((0.30, -0.10), 0.80, 0.20, facecolor="#0284C7", edgecolor="#0369A1", lw=0.7, zorder=10)
    ax.add_patch(r_cont)
    ax.text(0.70, -0.30, "BATERÍA CONTADORES", ha='center', va='top', fontsize=4.8, color="#0284C7", zorder=25)

    circ_acs = patches.Circle((10.85, 15.20), 0.35, facecolor="#EF4444", edgecolor="#B91C1C", lw=0.8, zorder=10)
    ax.add_patch(circ_acs)
    ax.text(10.85, 15.20, "ACS\n200L", ha='center', va='center', fontsize=4.8, weight='bold', color="#FFFFFF", zorder=25)

    ax.plot([0.70, 0.70, 10.85], [-0.10, 15.20, 15.20], color="#0284C7", lw=1.2, linestyle=':', zorder=8)
    ax.text(5.50, 8.50, "RED GENERAL DE AGUA FRÍA Y RETORNO ACS (PEX Ø25)", ha='center', va='center', fontsize=5.2, color="#0284C7", rotation=90, zorder=25)

    # 3. Ventilación Mecánica Controlada VMC (DB-HS3)
    r_vmc = patches.Rectangle((9.50, 16.00), 0.80, 0.60, facecolor="#10B981", edgecolor="#047857", lw=0.8, zorder=10)
    ax.add_patch(r_vmc)
    ax.text(9.90, 16.30, "VMC DOBLE FLUJO\n(Eficiencia > 85%)", ha='center', va='center', fontsize=4.5, weight='bold', color="#FFFFFF", zorder=25)

    extracciones = [(2.00, 8.50), (5.50, 8.50), (9.00, 2.00)]
    for ex_x, ex_y in extracciones:
        circ_ex = patches.Circle((ex_x, ex_y), 0.18, facecolor="#EF4444", edgecolor="#B91C1C", lw=0.6, zorder=12)
        ax.add_patch(circ_ex)
        ax.text(ex_x, ex_y - 0.25, "Extracción Ø125", ha='center', va='top', fontsize=4.2, color="#B91C1C", zorder=25)

    admisiones = [(3.00, 2.00), (3.00, 11.50), (1.50, 16.00), (4.50, 16.00)]
    for ad_x, ad_y in admisiones:
        circ_ad = patches.Circle((ad_x, ad_y), 0.18, facecolor="#3B82F6", edgecolor="#1D4ED8", lw=0.6, zorder=12)
        ax.add_patch(circ_ad)
        ax.text(ad_x, ad_y + 0.25, "Admisión Ø100", ha='center', va='bottom', fontsize=4.2, color="#1D4ED8", zorder=25)

    # 4. Seguridad Contra Incendios (DB-SI)
    for ext_x, ext_y in [(0.40, 7.60), (7.00, 13.50)]:
        r_ext = patches.Rectangle((ext_x - 0.15, ext_y - 0.15), 0.30, 0.30, facecolor="#DC2626", edgecolor="#7F1D1D", lw=0.7, zorder=14)
        ax.add_patch(r_ext)
        ax.text(ext_x, ext_y, "EXT", ha='center', va='center', fontsize=4.5, weight='bold', color="#FFFFFF", zorder=25)

    # Leyenda de instalaciones CON zorder=25 EN TEXTOS
    cs_x, cs_y = -4.80, 2.50
    patches_rect = patches.Rectangle((cs_x, cs_y), 4.20, 8.50, facecolor="#FFFFFF", edgecolor=C_WALL, lw=0.9, zorder=20)
    ax.add_patch(patches_rect)
    ax.text(cs_x + 2.10, cs_y + 8.10, "SIMBOLOGÍA DE INSTALACIONES (CTE)", ha='center', va='center', fontsize=6.2, weight='bold', color=C_TEXT_MAIN, zorder=25)
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
        ax.text(cs_x + 0.20, cs_y + 7.30 - idx * 0.85, f"[{cod}]", ha='left', va='center', fontsize=5.2, weight='bold', color="#1E40AF", zorder=25)
        ax.text(cs_x + 0.20, cs_y + 6.95 - idx * 0.85, desc, ha='left', va='center', fontsize=4.5, color="#475569", zorder=25)

    draw_cajetin(ax, "P-07", "INSTALACIONES GENERALES", "Climatización Aerotérmica, Suelo Radiante, VMC, Electricidad, Wallbox y Fontanería", "1:75")

    plt.savefig(os.path.join(OUTPUT_DIR, "07_plano_instalaciones.png"), bbox_inches='tight', dpi=300)
    plt.savefig(os.path.join(OUTPUT_DIR, "07_plano_instalaciones.pdf"), bbox_inches='tight')
    plt.close(fig)
    print("PLANO P-07 INSTALACIONES GENERADO.")


if __name__ == "__main__":
    generar_plano_emplazamiento()
    generar_plano_planta_alta_bruto()
    generar_plano_cubiertas()
    generar_plano_alzados()
    generar_plano_secciones()
    generar_plano_estructura()
    generar_plano_instalaciones()
    print("COLECCIÓN COMPLETA DE PLANOS TÉCNICOS GENERADA CON ÉXITO.")
