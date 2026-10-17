# -*- coding: utf-8 -*-
"""
Genera Tomos V y VI independientes y prepara la carpeta con todos los archivos
sueltos listos para arrastrar y soltar a Gemini Web.
"""

import os
import shutil
from pathlib import Path
from fpdf import FPDF
from fpdf.enums import XPos, YPos

DESKTOP = Path(os.environ["USERPROFILE"]) / "Desktop"
DEST_DIR = DESKTOP / "ARCHIVOS_PARA_SUBIR_A_GEMINI_WEB"
SRC_REPO = DESKTOP / "mi-casa"
AYTO_DIR = SRC_REPO / "00_PROYECTO_FINAL_LICENCIA_AYUNTAMIENTO"

DEST_DIR.mkdir(parents=True, exist_ok=True)

class StandalonePDF(FPDF):
    def __init__(self, titulo_tomo, subtitulo):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.titulo_tomo = titulo_tomo
        self.subtitulo = subtitulo
        self.set_auto_page_break(auto=True, margin=20)
        
        font_dir = r"C:\Windows\Fonts"
        self.add_font("ArialUni", "", os.path.join(font_dir, "arial.ttf"))
        self.add_font("ArialUni", "B", os.path.join(font_dir, "arialbd.ttf"))
        self.add_font("ArialUni", "I", os.path.join(font_dir, "ariali.ttf"))

    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("ArialUni", "B", 8)
        self.set_text_color(71, 85, 105)
        self.cell(120, 7, "PROYECTO BÁSICO Y DE EJECUCIÓN - PALMA DEL RÍO (CÓRDOBA)", new_x=XPos.RIGHT, new_y=YPos.TOP)
        self.cell(70, 7, self.titulo_tomo, align="R", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_draw_color(203, 213, 225)
        self.set_line_width(0.3)
        self.line(10, 17, 200, 17)
        self.ln(5)

    def footer(self):
        if self.page_no() == 1:
            return
        self.set_y(-15)
        self.set_font("ArialUni", "", 8)
        self.set_text_color(100, 116, 139)
        self.set_draw_color(203, 213, 225)
        self.line(10, 282, 200, 282)
        self.cell(0, 10, f"Documento Oficial CTE - Aprobación de Licencia Municipal | Página {self.page_no()}", align="C")

    def chapter_title(self, num_str, title_str):
        self.set_font("ArialUni", "B", 13)
        self.set_text_color(15, 23, 42)
        self.ln(4)
        self.cell(0, 8, f"{num_str}. {title_str}".upper(), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_draw_color(14, 165, 233)
        self.set_line_width(0.8)
        self.line(10, self.get_y(), 70, self.get_y())
        self.ln(4)

    def section_title(self, num_str, title_str):
        self.set_font("ArialUni", "B", 10.5)
        self.set_text_color(30, 41, 59)
        self.ln(2)
        self.cell(0, 7, f"{num_str} {title_str}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(1)

    def body_p(self, text):
        self.set_font("ArialUni", "", 9.2)
        self.set_text_color(51, 65, 85)
        self.multi_cell(0, 4.8, text)
        self.ln(2)

    def table_row(self, c1, c2, is_bold=False, bg=False):
        self.set_font("ArialUni", "B" if is_bold else "", 8.5)
        if bg:
            self.set_fill_color(241, 245, 249)
        else:
            self.set_fill_color(255, 255, 255)
        self.set_text_color(15, 23, 42) if is_bold else self.set_text_color(71, 85, 105)
        self.cell(140, 6, c1, border=1, fill=bg, new_x=XPos.RIGHT, new_y=YPos.TOP)
        self.cell(50, 6, c2, border=1, align="R", fill=bg, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

def generar_tomo_v_ebss():
    pdf = StandalonePDF("TOMO V: ESTUDIO BÁSICO DE SEGURIDAD Y SALUD", "R.D. 1627/1997")
    pdf.add_page()
    pdf.ln(20)
    pdf.set_font("ArialUni", "B", 20); pdf.set_text_color(15, 23, 42)
    pdf.multi_cell(0, 10, "PROYECTO BÁSICO Y DE EJECUCIÓN", align="C")
    pdf.set_font("ArialUni", "B", 13); pdf.set_text_color(14, 165, 233)
    pdf.cell(0, 10, "VIVIENDA BIFAMILIAR ENTRE MEDIANERAS EN PALMA DEL RÍO (CÓRDOBA)", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(15)

    pdf.set_draw_color(15, 23, 42); pdf.set_fill_color(248, 250, 252); pdf.set_line_width(1.0)
    pdf.rect(25, 95, 160, 45, style="DF")
    pdf.set_xy(25, 105); pdf.set_font("ArialUni", "B", 15); pdf.set_text_color(15, 23, 42)
    pdf.cell(160, 8, "TOMO V: ESTUDIO BÁSICO DE SEGURIDAD Y SALUD", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("ArialUni", "", 9.5); pdf.set_text_color(71, 85, 105)
    pdf.set_x(25); pdf.cell(160, 6, "Prevención de Riesgos Laborales en Obras de Construcción (R.D. 1627/1997)", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_x(25); pdf.cell(160, 6, "y Ley 31/1995 de Prevención de Riesgos Laborales", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.add_page()
    pdf.chapter_title("1", "Memoria del Estudio Básico de Seguridad y Salud")
    pdf.section_title("1.1", "Objeto y Ámbito de Aplicación")
    pdf.body_p("El presente Estudio Básico de Seguridad y Salud (EBSS) establece las previsiones de seguridad y salud por las que deberá regirse la ejecución de la obra de edificación residencial en calle Moreno Torroba de Palma del Río, de conformidad con lo preceptuado en el Real Decreto 1627/1997, de 24 de octubre.\n"
               "Sirve de base directa para que la empresa adjudicataria redacte el preceptivo Plan de Seguridad y Salud en el Trabajo (PSST), que habrá de ser aprobado formalmente por el Coordinador de Seguridad y Salud durante la ejecución de las obras.")

    pdf.section_title("1.2", "Identificación de Riesgos y Medidas Preventivas por Fases")
    pdf.body_p("a) Fase de Movimiento de Tierras y Cimentación:\n"
               "- Riesgos: Sepultamiento por desprendimiento de tierras, caída de personas a distinto nivel, golpes por maquinaria de excavación.\n"
               "- Medidas: Balizamiento perimetral con valla de cerramiento móvil de 2,00 m de altura, entibación preventiva si se superan taludes estables, pasarelas de paso peatonal seguras sobre zanjas con barandillas reglamentarias (1,00 m, listón intermedio y rodapié de 15 cm).\n\n"
               "b) Fase de Estructura de Hormigón Armado:\n"
               "- Riesgos: Caída de altura desde bordes de forjado, caída de objetos sobre terceros en vía pública, atrapamiento en izado de cargas.\n"
               "- Medidas: Instalación obligatoria de redes de seguridad tipo horca (UNE-EN 1263-1) en el perímetro de fachada, barandillas metálicas de protección de borde de forjado encastradas en pilares, tapas rígidas y fijadas en huecos de escalera y patios, delimitación y corte de calle homologado por Policía Local durante hormigonado con autobomba.\n\n"
               "c) Fase de Cerramientos, Cubiertas e Instalaciones:\n"
               "- Riesgos: Caída de altura en trabajos de cubierta, electrocución por líneas provisionales de obra, inhalación de vapores en impermeabilización.\n"
               "- Medidas: Cuadro general de obra estanco con interruptores diferenciales de alta sensibilidad (30 mA), líneas de vida homologadas en cubierta plana para mantenimiento e impermeabilización.")

    pdf.section_title("1.3", "Medios de Protección Colectiva e Individual (EPIs)")
    pdf.body_p("Se priorizará en todo momento la protección colectiva frente a la individual. Dotación obligatoria de EPIs con marcado CE: casco de protección, calzado de seguridad con plantilla y puntera de acero (S3), guantes mecánicos, gafas de protección ocular y arnés anticaídas con absorbedor de energía.")

    pdf.section_title("1.4", "Presupuesto de Seguridad y Salud")
    pdf.table_row("Capítulo de Seguridad y Salud", "Importe PEM (€)", is_bold=True, bg=True)
    pdf.table_row("Protecciones Colectivas (redes horca, barandillas de forjado, tapas)", "1.850,00 €")
    pdf.table_row("Equipos de Protección Individual (cascos, botas, arneses, gafas)", "620,00 €")
    pdf.table_row("Instalaciones de Higiene y Bienestar (aseo portátil, vestuario, botiquín)", "980,00 €")
    pdf.table_row("Señalización de obra, balizamiento y extintores portátiles", "400,00 €")
    pdf.table_row("TOTAL PRESUPUESTO SEGURIDAD Y SALUD", "3.850,00 €", is_bold=True, bg=True)

    out_file = DEST_DIR / "05_TOMO_V_ESTUDIO_BASICO_SEGURIDAD_Y_SALUD.pdf"
    pdf.output(str(out_file))
    print(f"Generado: {out_file}")

def generar_tomo_vi_egr():
    pdf = StandalonePDF("TOMO VI: ESTUDIO DE GESTIÓN DE RESIDUOS (EGR)", "R.D. 105/2008")
    pdf.add_page()
    pdf.ln(20)
    pdf.set_font("ArialUni", "B", 20); pdf.set_text_color(15, 23, 42)
    pdf.multi_cell(0, 10, "PROYECTO BÁSICO Y DE EJECUCIÓN", align="C")
    pdf.set_font("ArialUni", "B", 13); pdf.set_text_color(14, 165, 233)
    pdf.cell(0, 10, "VIVIENDA BIFAMILIAR ENTRE MEDIANERAS EN PALMA DEL RÍO (CÓRDOBA)", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(15)

    pdf.set_draw_color(15, 23, 42); pdf.set_fill_color(248, 250, 252); pdf.set_line_width(1.0)
    pdf.rect(25, 95, 160, 45, style="DF")
    pdf.set_xy(25, 105); pdf.set_font("ArialUni", "B", 15); pdf.set_text_color(15, 23, 42)
    pdf.cell(160, 8, "TOMO VI: ESTUDIO DE GESTIÓN DE RESIDUOS", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("ArialUni", "", 9.5); pdf.set_text_color(71, 85, 105)
    pdf.set_x(25); pdf.cell(160, 6, "Residuos de Construcción y Demolición (R.D. 105/2008 y Ley 7/2022)", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_x(25); pdf.cell(160, 6, "Fianza Municipal Reguladora del Ayuntamiento de Palma del Río", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.add_page()
    pdf.chapter_title("1", "Memoria de Gestión de Residuos (EGRCD)")
    pdf.section_title("1.1", "Objeto y Marco Normativo")
    pdf.body_p("El presente Estudio de Gestión de Residuos de Construcción y Demolición (EGRCD) se redacta en cumplimiento estricto del Real Decreto 105/2008, de 1 de febrero, y de la Ley 7/2022, de 8 de abril, de residuos y suelos contaminados para una economía circular, así como de la Ordenanza Municipal de Limpieza y Residuos de Palma del Río.\n"
               "Establece la estimación de volumen y tonelaje de residuos que se producirán en la obra, clasificados según la Lista Europea de Residuos (LER), su destino previsto y la valoración económica que servirá de base para el depósito de la fianza municipal.")

    pdf.section_title("1.2", "Estimación Cuantitativa de Residuos por Código LER")
    pdf.table_row("Código LER / Tipología de Residuo", "Toneladas (t)", is_bold=True, bg=True)
    pdf.table_row("17 05 04 Tierras y piedras procedentes de excavación de cimentación y piscina", "213,00 t")
    pdf.table_row("17 01 01 Residuos de hormigón armado y masa", "18,40 t")
    pdf.table_row("17 01 02 Residuos de ladrillos y bloques cerámicos de fábrica", "14,20 t")
    pdf.table_row("17 01 03 Tejas y materiales cerámicos", "2,10 t")
    pdf.table_row("17 01 07 Mezclas de hormigón, ladrillos, tejas y cerámicos (mezclas RCD)", "9,30 t")
    pdf.table_row("17 02 01 Madera limpia procedente de encofrados y palets", "3,40 t")
    pdf.table_row("17 02 03 Plásticos y embalajes de materiales de obra", "1,80 t")
    pdf.table_row("17 04 05 Hierro y acero procedentes de recortes de ferralla", "1,50 t")
    pdf.table_row("17 08 02 Materiales de construcción a base de yeso (placas cartón yeso)", "2,20 t")
    pdf.table_row("TOTAL RESIDUOS GENERADOS PREVISTOS", "265,90 t", is_bold=True, bg=True)

    pdf.section_title("1.3", "Prescripciones de Separación en Obra y Destino")
    pdf.body_p("En cumplimiento del artículo 5 del R.D. 105/2008, al superarse los límites reglamentarios, se establece la separación selectiva en obra mediante contenedores debidamente señalizados para madera, plástico, metales, yeso y fracción pétrea.\n"
               "El destino final será una Planta de Valorización y Tratamiento de RCDs legalmente autorizada en la comarca de la Vega del Guadalquivir. La empresa constructora entregará a la Dirección Facultativa los correspondientes Certificados de Aceptación y Justificantes de Entrega emitidos por el gestor autorizado.")

    pdf.section_title("1.4", "Presupuesto y Determinación de la Fianza Municipal")
    pdf.table_row("Concepto Económico de Residuos", "Importe (€)", is_bold=True, bg=True)
    pdf.table_row("Coste previsto de transporte y entrega a gestor autorizado (PEM)", "2.100,00 €")
    pdf.table_row("Fianza Municipal Reguladora (Depósito recuperable Ayto. Palma del Río)", "1.500,00 €", is_bold=True, bg=True)
    pdf.body_p("La fianza será reintegrada formalmente al Promotor una vez finalizada la obra y emitido el Certificado Final de Obra con los justificantes de entrega de la totalidad de los residuos a gestor autorizado.")

    out_file = DEST_DIR / "06_TOMO_VI_ESTUDIO_GESTION_RESIDUOS.pdf"
    pdf.output(str(out_file))
    print(f"Generado: {out_file}")

def copiar_archivos_clave():
    archivos_ayto = [
        "01_TOMO_I_MEMORIA_CTE_Y_ANEJOS.pdf",
        "02_TOMO_II_ALBUM_PLANOS_REGLAMENTARIOS_A3.pdf",
        "03_TOMO_III_PLIEGO_DE_CONDICIONES.pdf",
        "04_TOMO_IV_MEDICIONES_Y_PRESUPUESTO.pdf"
    ]
    for f in archivos_ayto:
        src = AYTO_DIR / f
        if src.exists():
            shutil.copy2(str(src), str(DEST_DIR / f))
            print(f"Copiado: {f}")

    archivos_fuente = [
        SRC_REPO / "PROYECTO.md",
        SRC_REPO / "plan_data.py",
        SRC_REPO / "tools" / "generar_dossier_escrito_oficial.py",
        SRC_REPO / "tools" / "generar_planos_tecnicos_completos.py",
        SRC_REPO / "entrega" / "planos" / "proyecto-completo.pdf"
    ]
    for src in archivos_fuente:
        if src.exists():
            shutil.copy2(str(src), str(DEST_DIR / src.name))
            print(f"Copiado fuente: {src.name}")

if __name__ == "__main__":
    generar_tomo_v_ebss()
    generar_tomo_vi_egr()
    copiar_archivos_clave()
    print("\nCarpeta lista en el Escritorio: ARCHIVOS_PARA_SUBIR_A_GEMINI_WEB")
