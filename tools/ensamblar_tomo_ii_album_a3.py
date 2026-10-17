# -*- coding: utf-8 -*-
"""
Ensamblador del Álbum de Planos Reglamentarios A3 (Tomo II) para el Ayuntamiento de Palma del Río.
Combina la portada oficial A3 y los 8 planos reglamentarios:
P-00: Emplazamiento y Justificación PGOU (Escala 1:100)
P-01: Planta Baja Amueblada y Acotada (Escala 1:50)
P-02: Planta Alta Diáfana en Bruto (Escala 1:50)
P-03: Planta de Cubiertas e Instalaciones (Escala 1:100)
P-04: Alzados Exteriores Sur y Norte (Escala 1:100)
P-05: Secciones Constructivas A-A' y B-B' (Escala 1:75)
P-06: Estructura, Cimentación y Saneamiento (Escala 1:75)
P-07: Instalaciones Generales Clima/VMC/Electricidad/Fontanería (Escala 1:75)
"""

import os
from pathlib import Path
from pypdf import PdfWriter, PdfReader
from fpdf import FPDF
from fpdf.enums import XPos, YPos

ROOT = Path(__file__).resolve().parent.parent
PLANOS_DIR = ROOT / "entrega" / "planos_2d"
OUTPUT_DIR = ROOT / "00_PROYECTO_FINAL_LICENCIA_AYUNTAMIENTO"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def crear_portada_a3():
    pdf = FPDF(orientation="L", unit="mm", format="A3")
    font_dir = r"C:\Windows\Fonts"
    pdf.add_font("ArialUni", "", os.path.join(font_dir, "arial.ttf"))
    pdf.add_font("ArialUni", "B", os.path.join(font_dir, "arialbd.ttf"))
    pdf.add_page()

    # Marco perimetral
    pdf.set_draw_color(15, 23, 42)
    pdf.set_line_width(1.2)
    pdf.rect(10, 10, 400, 277)
    pdf.set_line_width(0.4)
    pdf.rect(12, 12, 396, 273)

    # Título principal
    pdf.set_xy(20, 35)
    pdf.set_font("ArialUni", "B", 26)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(380, 12, "PROYECTO BÁSICO Y DE EJECUCIÓN", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.set_font("ArialUni", "B", 15)
    pdf.set_text_color(14, 165, 233)
    pdf.cell(380, 9, "VIVIENDA UNIFAMILIAR EN PLANTA BAJA CON PATIO Y PISCINA + ESPACIO EN BRUTO EN PLANTA ALTA", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    pdf.set_font("ArialUni", "", 11)
    pdf.set_text_color(71, 85, 105)
    pdf.cell(380, 7, "Calle Moreno Torroba s/n · 14700 Palma del Río (Córdoba) | Ley 38/1999 (LOE) · R.D. 314/2006 (CTE)", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # Recuadro central
    pdf.set_fill_color(248, 250, 252)
    pdf.rect(80, 80, 260, 48, style="DF")
    pdf.set_xy(80, 90)
    pdf.set_font("ArialUni", "B", 20)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(260, 10, "TOMO II: ÁLBUM DE PLANOS REGLAMENTARIOS", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("ArialUni", "", 11)
    pdf.set_text_color(71, 85, 105)
    pdf.cell(260, 7, "Colección Completa de Láminas Técnicas Ejecutivas a Escalas Normalizadas (A3)", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(260, 7, "Aprobación de Licencia Urbanística de Obras · Visado Colegial COACo", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # Índice de láminas
    pdf.set_xy(60, 145)
    pdf.set_font("ArialUni", "B", 12)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(300, 7, "ÍNDICE GENERAL DE LÁMINAS TÉCNICAS:", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(2)

    laminas = [
        ("PLANO P-00", "SITUACIÓN, EMPLAZAMIENTO Y JUSTIFICACIÓN PGOU (OCUPACIÓN 80% Y PATIO 40 m²)", "ESCALA 1:100"),
        ("PLANO P-01", "PLANTA BAJA AMUEBLADA Y ACOTADA (MASTER SUITE, PATIO, PISCINA Y GARAJE)", "ESCALA 1:50"),
        ("PLANO P-02", "PLANTA ALTA · ESPACIO DIÁFANO EN BRUTO SIN USO DEFINIDO Y PREINSTALACIONES", "ESCALA 1:50"),
        ("PLANO P-03", "PLANTA DE CUBIERTAS E INSTALACIONES (XPS 100 mm, AEROTERMIA Y FOTOVOLTAICA)", "ESCALA 1:100"),
        ("PLANO P-04", "ALZADOS EXTERIORES GENERALES (FACHADA SUR MORENO TORROBA Y FACHADA NORTE GARAJE)", "ESCALA 1:100"),
        ("PLANO P-05", "SECCIONES CONSTRUCTIVAS LONGITUDINAL A-A' Y TRANSVERSAL B-B' (-1,50 m)", "ESCALA 1:75"),
        ("PLANO P-06", "ESTRUCTURA, CIMENTACIÓN Y RED DE SANEAMIENTO ENTERRADA (HA-25 Y PVC Ø160)", "ESCALA 1:75"),
        ("PLANO P-07", "INSTALACIONES GENERALES (CLIMATIZACIÓN B4, VMC DOBLE FLUJO, ELECTRICIDAD Y WALLBOX)", "ESCALA 1:75"),
    ]

    for cod, nom, esc in laminas:
        pdf.set_x(60)
        pdf.set_font("ArialUni", "B", 9.5)
        pdf.set_text_color(14, 165, 233)
        pdf.cell(32, 6, cod, border=0)
        pdf.set_font("ArialUni", "", 9.5)
        pdf.set_text_color(51, 65, 85)
        pdf.cell(210, 6, nom, border=0)
        pdf.set_font("ArialUni", "B", 9)
        pdf.set_text_color(15, 23, 42)
        pdf.cell(40, 6, esc, border=0, align="R", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # Diligencia de firmas
    pdf.set_xy(30, 225)
    pdf.set_draw_color(203, 213, 225)
    pdf.rect(40, 228, 90, 48)
    pdf.rect(165, 228, 90, 48)
    pdf.rect(290, 228, 90, 48)

    pdf.set_xy(40, 231); pdf.set_font("ArialUni", "B", 8.5); pdf.set_text_color(15, 23, 42); pdf.cell(90, 5, "ARQUITECTO PROYECTISTA", align="C")
    pdf.set_xy(40, 268); pdf.set_font("ArialUni", "", 8); pdf.set_text_color(100, 116, 139); pdf.cell(90, 5, "Firma y Visado Colegial COACo", align="C")

    pdf.set_xy(165, 231); pdf.set_font("ArialUni", "B", 8.5); pdf.set_text_color(15, 23, 42); pdf.cell(90, 5, "DIRECCIÓN DE EJECUCIÓN", align="C")
    pdf.set_xy(165, 268); pdf.set_font("ArialUni", "", 8); pdf.set_text_color(100, 116, 139); pdf.cell(90, 5, "Arquitecto Técnico / Aparejador", align="C")

    pdf.set_xy(290, 231); pdf.set_font("ArialUni", "B", 8.5); pdf.set_text_color(15, 23, 42); pdf.cell(90, 5, "LA PROPIEDAD / PROMOTOR", align="C")
    pdf.set_xy(290, 268); pdf.set_font("ArialUni", "", 8); pdf.set_text_color(100, 116, 139); pdf.cell(90, 5, "Conforme con el Proyecto", align="C")

    portada_path = PLANOS_DIR / "00_portada_album_a3.pdf"
    pdf.output(str(portada_path))
    return portada_path

def ensamblar_tomo_ii():
    portada = crear_portada_a3()
    writer = PdfWriter()

    # Añadir portada
    reader_p = PdfReader(str(portada))
    writer.add_page(reader_p.pages[0])

    planos_orden = [
        "00_plano_emplazamiento_pgou.pdf",
        "01_plano_arquitecto_planta_baja.pdf",
        "02_plano_arquitecto_planta_alta_bruto.pdf",
        "03_plano_cubiertas.pdf",
        "04_plano_alzados.pdf",
        "05_plano_secciones.pdf",
        "06_plano_estructura.pdf",
        "07_plano_instalaciones.pdf",
    ]

    for p_name in planos_orden:
        p_path = PLANOS_DIR / p_name
        if p_path.exists():
            r = PdfReader(str(p_path))
            writer.add_page(r.pages[0])
            print(f"Añadido al Álbum A3: {p_name}")

    out_pdf = OUTPUT_DIR / "02_TOMO_II_ALBUM_PLANOS_REGLAMENTARIOS_A3.pdf"
    with open(out_pdf, "wb") as f:
        writer.write(f)
    print(f"\nÁLBUM A3 REGLAMENTARIO GENERADO CON ÉXITO: {out_pdf}")

if __name__ == "__main__":
    ensamblar_tomo_ii()
