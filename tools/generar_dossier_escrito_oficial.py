# -*- coding: utf-8 -*-
"""
GENERADOR INTEGRAL DE LOS 3 TOMOS ESCRITOS OFICIALES DEL PROYECTO (CTE)
Genera en PDF oficial con fpdf2 y tipografía Arial de Windows:
1. TOMO I: MEMORIA TÉCNICA CTE Y ANEJOS (EBSS, RESIDUOS, CONTROL DE CALIDAD)
2. TOMO III: PLIEGO DE CONDICIONES TÉCNICAS Y ADMINISTRATIVAS PARTICULARES
3. TOMO IV: MEDICIONES, PRESUPUESTO (PEM / PEC) Y LIQUIDACIÓN MUNICIPAL (ICIO)
"""

import os
from fpdf import FPDF
from fpdf.enums import XPos, YPos

OUTPUT_DIR = r"C:\Users\Oscar Martinez\Desktop"
os.makedirs(OUTPUT_DIR, exist_ok=True)

class DossierPDF(FPDF):
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

def generar_tomo_i_memoria():
    pdf = DossierPDF("TOMO I: MEMORIA CTE Y ANEJOS", "Proyecto Básico y de Ejecución")
    pdf.add_page()
    pdf.ln(20)
    pdf.set_font("ArialUni", "B", 22); pdf.set_text_color(15, 23, 42)
    pdf.multi_cell(0, 10, "PROYECTO BÁSICO Y DE EJECUCIÓN", align="C")
    pdf.set_font("ArialUni", "B", 13); pdf.set_text_color(14, 165, 233)
    pdf.cell(0, 10, "VIVIENDA BIFAMILIAR ENTRE MEDIANERAS CON PATIO, PISCINA Y GARAJE", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(10)
    pdf.set_font("ArialUni", "", 10); pdf.set_text_color(71, 85, 105)
    pdf.cell(0, 6, "Emplazamiento: Calle Moreno Torroba s/n - 14700 Palma del Río (Córdoba)", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(0, 6, "Marco Normativo: Ley 38/1999 (LOE) - R.D. 314/2006 (CTE) - PGOU Palma del Río", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(20)
    pdf.set_draw_color(15, 23, 42); pdf.set_fill_color(248, 250, 252); pdf.set_line_width(1.0)
    pdf.rect(25, 105, 160, 48, style="DF")
    pdf.set_xy(25, 112); pdf.set_font("ArialUni", "B", 15); pdf.set_text_color(15, 23, 42)
    pdf.cell(160, 8, "TOMO I: MEMORIA TÉCNICA Y ANEJOS", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("ArialUni", "", 9.5); pdf.set_text_color(71, 85, 105)
    pdf.set_x(25); pdf.cell(160, 6, "Memoria Descriptiva, Constructiva, Justificación CTE,", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_x(25); pdf.cell(160, 6, "Estudio Básico de Seguridad y Salud y Gestión de Residuos", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.set_xy(10, 185); pdf.set_font("ArialUni", "B", 10)
    pdf.cell(0, 6, "CUADRO DE IDENTIFICACIÓN Y DILIGENCIA DE FIRMAS:", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_draw_color(203, 213, 225)
    pdf.rect(10, 195, 60, 65); pdf.rect(75, 195, 60, 65); pdf.rect(140, 195, 60, 65)
    pdf.set_xy(10, 198); pdf.set_font("ArialUni", "B", 8); pdf.cell(60, 5, "ARQUITECTO PROYECTISTA", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_xy(10, 248); pdf.set_font("ArialUni", "", 7.5); pdf.cell(60, 5, "Firma y Visado Colegial COACo", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_xy(75, 198); pdf.set_font("ArialUni", "B", 8); pdf.cell(60, 5, "DIRECCIÓN DE EJECUCIÓN", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_xy(75, 248); pdf.set_font("ArialUni", "", 7.5); pdf.cell(60, 5, "Arquitecto Técnico / Aparejador", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_xy(140, 198); pdf.set_font("ArialUni", "B", 8); pdf.cell(60, 5, "EL PROMOTOR", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_xy(140, 248); pdf.set_font("ArialUni", "", 7.5); pdf.cell(60, 5, "Conforme con el Proyecto", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.add_page()
    pdf.chapter_title("1", "Memoria Descriptiva y Justificación Urbanística")
    pdf.section_title("1.1", "Agentes del Proyecto y Objeto del Encargo")
    pdf.body_p("El presente Proyecto Básico y de Ejecución tiene por objeto la definición técnica, constructiva y normativa precisa para la construcción de una Edificación Residencial Bifamiliar compuesta por dos viviendas independientes (Vivienda A en Planta Baja y Vivienda B en Planta Alta), dotadas de garaje privado, porche, patio central con piscina privada y solárium.")

    pdf.section_title("1.2", "Marco Urbanístico Municipal (PGOU de Palma del Río)")
    pdf.body_p("La parcela se sitúa en Suelo Urbano Consolidado, con calificación Residencial Unifamiliar / Bifamiliar entre medianeras. Características urbanísticas:\n"
               "- Superficie de Parcela: 205,90 m² (11,60 m de fachada sur x 17,75 m de fondo pasante).\n"
               "- Tipología: Edificación entre medianeras con alineación directa a viales públicos en fachada sur y norte.\n"
               "- Altura máxima permitida: 2 plantas sobre rasante (B+1) y 7,20 m a cornisa. Cumple estrictamente (5,85 m totales).\n"
               "- Ocupación máxima de parcela: La edificación libera un patio central privativo de 28,00 m² (13,6% de la parcela), superando la exigencia municipal mínima del 10% para garantizar iluminación y ventilación natural directa.\n"
               "- Dotación obligatoria de aparcamiento: El proyecto incorpora 1 plaza de garaje cerrada de 21,14 m² en planta baja con acceso directo desde vial trasero y punto de recarga de vehículo eléctrico (Wallbox).")

    pdf.section_title("1.3", "Cuadro General de Superficies (Útiles y Construidas)")
    pdf.table_row("Estancia / Uso", "Superficie Útil (m²)", is_bold=True, bg=True)
    pdf.table_row("VIVIENDA A (PLANTA BAJA) - Salón-Comedor", "38,50 m²")
    pdf.table_row("VIVIENDA A (PLANTA BAJA) - Cocina con Isla", "18,72 m²")
    pdf.table_row("VIVIENDA A (PLANTA BAJA) - Master Suite (Dormitorio 1)", "15,10 m²")
    pdf.table_row("VIVIENDA A (PLANTA BAJA) - Baño en Suite con Doble Lavabo", "5,57 m²")
    pdf.table_row("VIVIENDA A (PLANTA BAJA) - Baño General", "5,68 m²")
    pdf.table_row("VIVIENDA A (PLANTA BAJA) - Dormitorio 2", "11,70 m²")
    pdf.table_row("VIVIENDA A (PLANTA BAJA) - Dormitorio 3", "11,90 m²")
    pdf.table_row("VIVIENDA A (PLANTA BAJA) - Pasillo Distribuidor y Gabanero", "8,69 m²")
    pdf.table_row("VIVIENDA A (PLANTA BAJA) - Garaje / Trastero Técnico", "21,14 m²")
    pdf.table_row("SUBTOTAL ÚTIL CERRADA VIVIENDA A", "137,00 m²", is_bold=True, bg=True)
    pdf.table_row("VIVIENDA A (EXTERIOR) - Porche Cubierto (100%)", "11,40 m²")
    pdf.table_row("VIVIENDA A (EXTERIOR) - Patio Ajardinado + Piscina", "26,36 m²")
    pdf.table_row("---", "---")
    pdf.table_row("VIVIENDA B (PLANTA ALTA) - Gran Salón-Comedor y Estar", "48,20 m²")
    pdf.table_row("VIVIENDA B (PLANTA ALTA) - Cocina con Isla", "18,72 m²")
    pdf.table_row("VIVIENDA B (PLANTA ALTA) - Master Suite (D1)", "15,10 m²")
    pdf.table_row("VIVIENDA B (PLANTA ALTA) - Baño en Suite", "5,57 m²")
    pdf.table_row("VIVIENDA B (PLANTA ALTA) - Baño General", "5,68 m²")
    pdf.table_row("VIVIENDA B (PLANTA ALTA) - Dormitorio 2", "21,14 m²")
    pdf.table_row("VIVIENDA B (PLANTA ALTA) - Dormitorio 3", "11,00 m²")
    pdf.table_row("VIVIENDA B (PLANTA ALTA) - Pasillo y Escalera Desembarco", "11,82 m²")
    pdf.table_row("SUBTOTAL ÚTIL CERRADA VIVIENDA B", "137,23 m²", is_bold=True, bg=True)
    pdf.table_row("VIVIENDA B (EXTERIOR) - Terraza Solárium Privada", "12,16 m²")
    pdf.table_row("TOTAL SUPERFICIE CONSTRUIDA DEL EDIFICIO", "351,40 m²", is_bold=True, bg=True)

    pdf.add_page()
    pdf.chapter_title("2", "Memoria Constructiva")
    pdf.section_title("2.1", "Sustentación del Edificio y Cimentación")
    pdf.body_p("De acuerdo con el informe geotécnico y las características del suelo de Palma del Río (Vega del Guadalquivir), la cimentación se resuelve mediante zapatas aisladas bajo pilares interiores y zapatas corridas bajo muros medianeros, enlazadas perimetralmente por vigas de atado y centradoras de hormigón armado HA-25/B/20/IIa.")
    pdf.body_p("Sobre el terreno se ejecuta una solera sanitaria ventilada tipo Cáviti de 40 cm de canto apoyada sobre encachado de grava drenante y lámina de polietileno de 200 galgas, garantizando el aislamiento frente a humedad por capilaridad y la ventilación natural continua contra gas radón (DB-HS1).")

    pdf.section_title("2.2", "Sistema Estructural")
    pdf.body_p("La estructura vertical está formada por pilares de hormigón armado de 30x30 cm y muros de carga en medianeras de fábrica de ladrillo macizo perforado de 1 pie de espesor. Los forjados horizontales son unidireccionales de 25+5 cm de canto con viguetas pretensadas y bovedillas de hormigón, con capa de compresión armada con mallazo electrosoldado B 500 T.")

    pdf.section_title("2.3", "Envolvente Térmica y Fachadas")
    pdf.body_p("- Fachadas exteriores: Hoja exterior de ladrillo cerámico perforado de 1/2 pie, enfoscado interior con mortero de cemento, aislamiento térmico continuo de panel de lana de roca de 100 mm (conductividad 0,035 W/mK), cámara de aire no ventilada de 3 cm y trasdosado autoportante de placa de yeso laminado de 15 mm.")
    pdf.body_p("- Carpinterías exteriores: Perfilería de aluminio extrusionado con Rotura de Puente Térmico (RPT) de 70 mm, con doble acristalamiento bajo emisivo y control solar 4/16/4 mm con gas argón (transmitancia térmica global Uh < 1,40 W/m²K).")
    pdf.body_p("- Cubiertas: Cubierta plana invertida no transitable en zonas técnicas protegida con capa de grava lavada (5 cm), lámina impermeabilizante bicapa de betún elastomérico SBS adherida y aislamiento térmico de poliestireno extruido (XPS) de 100 mm.")

    pdf.add_page()
    pdf.chapter_title("3", "Cumplimiento del Código Técnico de la Edificación (CTE)")
    pdf.section_title("3.1", "DB-SE: Seguridad Estructural")
    pdf.body_p("Cálculo efectuado conforme al Código Estructural (RD 470/2021) y DB-SE-AE (Acciones en la edificación): sobrecarga de uso en viviendas 2,0 kN/m², en cubiertas 1,0 kN/m², viento para zona eólica C y sismo para Palma del Río (aceleración sísmica básica ac < 0,04g, no siendo obligatoria la aplicación de la norma sismorresistente NCSE-02).")

    pdf.section_title("3.2", "DB-SI: Seguridad en caso de Incendio")
    pdf.body_p("- Sectorización: Cada vivienda constituye un sector de incendio independiente (EI 60). El garaje constituye un sector de riesgo especial bajo delimitado por paramentos EI 120 y puerta de acceso EI2 60-C5 con vestíbulo de independencia.")
    pdf.body_p("- Evacuación: Longitud de evacuación desde cualquier punto habitable hasta la salida del edificio < 14,0 m (máximo permitido 25,0 m).")
    pdf.body_p("- Dotación de Extintores: Se proyectan extintores portátiles de eficacia 21A-113B en garaje y vestíbulos comunes a distancia < 15 m.")

    pdf.section_title("3.3", "DB-SUA: Seguridad de Utilización y Accesibilidad")
    pdf.body_p("- Resbaladicidad de suelos: Pavimentos exteriores, porche, bordes de piscina y platos de ducha con clasificación Clase 3 (antideslizante Rd > 45 según UNE-ENV 12633). Pavimentos interiores secos Clase 1.")
    pdf.body_p("- Vaso de piscina: Dispone de escaleras romanas de acceso con peldaños de huella 30 cm y pasamanos de acero inoxidable, con profundidad máxima de 1,40 m y balizamiento visual del fondo.")

    pdf.section_title("3.4", "DB-HE: Ahorro de Energía (Edificio de Consumo Casi Nulo nZEB)")
    pdf.body_p("- HE-1: Envolvente térmica estanca sin puentes térmicos con transmitancias medias muy inferiores a los límites exigidos.")
    pdf.body_p("- HE-4: Contribución solar mínima para ACS. Se instala sistema de Bomba de Calor Aerotérmica de alta eficiencia (COP > 4,20) con interacumulador de 200 L, que aporta más del 78% de energía renovable, superando el 70% obligatorio.")
    pdf.body_p("- HE-5: Preinstalación para campo fotovoltaico de 4,5 kWp en cubierta plana sur.")

    pdf.section_title("3.5", "DB-HS: Salubridad y Ventilación Mecánica")
    pdf.body_p("Se incorpora sistema de Ventilación Mecánica Controlada (VMC) de doble flujo con recuperador de calor de alta eficiencia (>85%), con bocas de admisión de aire limpio en salones y dormitorios, y extracción en baños y cocinas según caudales DB-HS3.")

    pdf.add_page()
    pdf.chapter_title("4", "Anejos Reglamentarios Obligatorios")
    pdf.section_title("4.1", "Estudio Básico de Seguridad y Salud (EBSS)")
    pdf.body_p("Redactado en cumplimiento del R.D. 1627/1997. Identifica los riesgos laborales previsibles en las fases de excavación, cimentación, estructura, cerramientos, instalaciones y acabados, estableciendo las medidas preventivas colectivas (redes de horca, barandillas perimetrales de 1,00 m con rodapié, tapas de arqueta provisionales) y equipos de protección individual (EPIs).")

    pdf.section_title("4.2", "Estudio de Gestión de Residuos de Construcción (EGR)")
    pdf.body_p("Redactado en cumplimiento del R.D. 105/2008. Estimación cuantitativa de residuos generados en obra:\n"
               "- Tierras de excavación: 142,00 m³ (213,00 t) destinadas a relleno o gestor autorizado.\n"
               "- Residuos pétreos (hormigón, cerámicos, morteros): 38,50 t.\n"
               "- Residuos no pétreos (madera, plástico, metales, embalajes): 8,20 t.\n"
               "- Fianza municipal de gestión de residuos propuesta según ordenanza de Palma del Río: 1.500,00 €.")

    pdf_path = os.path.join(OUTPUT_DIR, "00_TOMO_I_MEMORIA_CTE_Y_ANEJOS.pdf")
    pdf.output(pdf_path)
    print(f"TOMO I MEMORIA CTE GENERADO: {pdf_path}")

def generar_tomo_iii_pliego():
    pdf = DossierPDF("TOMO III: PLIEGO DE CONDICIONES", "Pliego de Condiciones Técnicas y Administrativas")
    pdf.add_page()

    pdf.ln(20)
    pdf.set_font("ArialUni", "B", 22); pdf.set_text_color(15, 23, 42)
    pdf.multi_cell(0, 10, "PLIEGO DE CONDICIONES", align="C")
    pdf.set_font("ArialUni", "B", 13); pdf.set_text_color(14, 165, 233)
    pdf.cell(0, 10, "CLÁUSULAS ADMINISTRATIVAS Y PRESCRIPCIONES TÉCNICAS PARTICULARES", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(10)
    pdf.set_font("ArialUni", "", 10); pdf.set_text_color(71, 85, 105)
    pdf.cell(0, 6, "Emplazamiento: Calle Moreno Torroba s/n - Palma del Río (Córdoba)", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(0, 6, "Marco Normativo: Ley de Ordenación de la Edificación (LOE) y CTE Anejo I", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.ln(20)
    pdf.set_draw_color(15, 23, 42); pdf.set_fill_color(248, 250, 252); pdf.set_line_width(1.0)
    pdf.rect(25, 100, 160, 48, style="DF")
    pdf.set_xy(25, 108); pdf.set_font("ArialUni", "B", 15); pdf.set_text_color(15, 23, 42)
    pdf.cell(160, 8, "TOMO III: PLIEGO DE CONDICIONES", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("ArialUni", "", 9.5); pdf.set_text_color(71, 85, 105)
    pdf.set_x(25); pdf.cell(160, 6, "Pliego de Cláusulas Administrativas Generales y Particulares,", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_x(25); pdf.cell(160, 6, "Prescripciones sobre Materiales, Ejecución y Recepción de Unidades", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.add_page()
    pdf.chapter_title("1", "Pliego de Cláusulas Administrativas")
    pdf.section_title("1.1", "Ámbito y Relaciones entre los Agentes")
    pdf.body_p("Regula las obligaciones recíprocas entre el Promotor, el Constructor General adjudicatario y la Dirección Facultativa (Director de Obra y Director de Ejecución de la Obra) conforme a la Ley 38/1999 (LOE).")
    pdf.body_p("- Libro de Órdenes y Asistencias: Estará permanentemente en la obra a disposición exclusiva de la Dirección Facultativa.\n"
               "- Libro de Incidencias en materia de Seguridad y Salud: Custodiado por el Coordinador de Seguridad y Salud.\n"
               "- Plazo de Ejecución: Se establece un plazo estimado de 14 meses a partir de la firma del Acta de Replanteo e Inicio de Obras.")

    pdf.section_title("1.2", "Garantías, Recepción y Liquidación de Obra")
    pdf.body_p("- Recepción de la Obra: Se formalizará mediante Acta de Recepción suscrita por promotor y constructor dentro de los 30 días siguientes a la expedición del Certificado Final de Obra (CFO).\n"
               "- Plazos de Garantía LOE: 1 año para vicios o defectos de acabado; 3 años para vicios que afecten a la habitabilidad; 10 años para vicios que comprometan la resistencia mecánica y estabilidad del edificio (seguro decenal).")

    pdf.chapter_title("2", "Prescripciones Técnicas de Materiales y Ejecución")
    pdf.section_title("2.1", "Hormigones, Aceros y Cimentaciones")
    pdf.body_p("Todos los materiales deberán disponer del Marcado CE obligatorio y distintivo de calidad oficialmente reconocido. El hormigón HA-25 se someterá a control estadístico de resistencia mediante probetas cilíndricas normalizadas (UNE-EN 12390).")

    pdf.section_title("2.2", "Aislamientos, Estanqueidad e Instalaciones")
    pdf.body_p("Se exigirán ensayos de estanqueidad en todas las redes de saneamiento antes de su tapado mediante prueba de presión hidrostática, así como pruebas de servicio de fontanería y equilibrado hidráulico de los circuitos de climatización y suelo radiante.")

    pdf_path = os.path.join(OUTPUT_DIR, "00_TOMO_III_PLIEGO_DE_CONDICIONES.pdf")
    pdf.output(pdf_path)
    print(f"TOMO III PLIEGO GENERADO: {pdf_path}")

def generar_tomo_iv_presupuesto():
    pdf = DossierPDF("TOMO IV: MEDICIONES Y PRESUPUESTO", "Presupuesto Oficial de Ejecución")
    pdf.add_page()
    pdf.ln(20)
    pdf.set_font("ArialUni", "B", 22); pdf.set_text_color(15, 23, 42)
    pdf.multi_cell(0, 10, "PRESUPUESTO GENERAL Y MEDICIONES", align="C")
    pdf.set_font("ArialUni", "B", 13); pdf.set_text_color(14, 165, 233)
    pdf.cell(0, 10, "ESTRUCTURA DE COSTES, MEDICIONES Y LIQUIDACIÓN MUNICIPAL", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(10)
    pdf.set_font("ArialUni", "", 10); pdf.set_text_color(71, 85, 105)
    pdf.cell(0, 6, "Emplazamiento: Calle Moreno Torroba s/n - Palma del Río (Córdoba)", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(0, 6, "Formato FIEBDC-3 (BC3) - Presupuesto para Licencia Municipal de Obras", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(20)
    pdf.set_draw_color(15, 23, 42); pdf.set_fill_color(248, 250, 252); pdf.set_line_width(1.0)
    pdf.rect(25, 100, 160, 45, style="DF")
    pdf.set_xy(25, 108); pdf.set_font("ArialUni", "B", 15); pdf.set_text_color(15, 23, 42)
    pdf.cell(160, 8, "TOMO IV: MEDICIONES Y PRESUPUESTO", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("ArialUni", "", 9.5); pdf.set_text_color(71, 85, 105)
    pdf.set_x(25); pdf.cell(160, 6, "Desglose por Capítulos, Presupuesto de Ejecución Material (PEM)", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_x(25); pdf.cell(160, 6, "y Liquidación de Tasas e Impuestos Municipales (ICIO)", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.set_xy(10, 160)
    pdf.chapter_title("1", "Resumen de Presupuesto por Capítulos (PEM)")

    capitulos = [
        ("01. ACTUACIONES PREVIAS Y MOVIMIENTO DE TIERRAS", "8.450,00 €"),
        ("02. CIMENTACIÓN Y SOLERA SANITARIA CÁVITI", "22.350,00 €"),
        ("03. ESTRUCTURA DE HORMIGÓN ARMADO", "36.800,00 €"),
        ("04. CERRAMIENTOS DE FACHADA Y MEDIANERAS", "28.400,00 €"),
        ("05. CUBIERTAS E IMPERMEABILIZACIONES", "16.900,00 €"),
        ("06. TABIQUERÍA INTERIOR Y FALSOS TECHOS", "18.250,00 €"),
        ("07. AISLAMIENTOS TÉRMICOS Y ACÚSTICOS", "9.600,00 €"),
        ("08. REVESTIMIENTOS Y SOLADOS PORCELÁNICOS", "24.100,00 €"),
        ("09. CARPINTERÍA EXTERIOR RPT Y CERRAJERÍA", "26.500,00 €"),
        ("10. CARPINTERÍA INTERIOR DE MADERA", "11.200,00 €"),
        ("11. FONTANERÍA, SANEAMIENTO Y SANITARIOS", "15.400,00 €"),
        ("12. CLIMATIZACIÓN AEROTÉRMICA Y VMC", "21.500,00 €"),
        ("13. ELECTRICIDAD, ILUMINACIÓN Y WALLBOX", "14.800,00 €"),
        ("14. PATIO, PORCHE Y VASO DE PISCINA", "17.650,00 €"),
        ("15. GESTIÓN DE RESIDUOS DE CONSTRUCCIÓN (RCD)", "2.100,00 €"),
        ("16. SEGURIDAD Y SALUD EN EL TRABAJO", "3.850,00 €"),
        ("17. CONTROL DE CALIDAD Y ENSAYOS", "1.950,00 €"),
    ]

    pdf.table_row("Capítulo", "Importe PEM (€)", is_bold=True, bg=True)
    for cap, imp in capitulos:
        pdf.table_row(cap, imp)

    pdf.ln(4)
    pdf.chapter_title("2", "Resumen General y Liquidación de Contrata")
    pdf.table_row("TOTAL PRESUPUESTO DE EJECUCIÓN MATERIAL (P.E.M.)", "279.800,00 €", is_bold=True, bg=True)
    pdf.table_row("13,00 % Gastos Generales de la Empresa Constructora", "36.374,00 €")
    pdf.table_row("6,00 % Beneficio Industrial del Contratista", "16.788,00 €")
    pdf.table_row("PRESUPUESTO DE EJECUCIÓN POR CONTRATA (P.E.C. sin IVA)", "332.962,00 €", is_bold=True, bg=True)
    pdf.table_row("10,00 % I.V.A. Reducido (Promoción directa de vivienda)", "33.296,20 €")
    pdf.table_row("TOTAL PRESUPUESTO BASE DE LICITACIÓN CONTRATA", "366.258,20 €", is_bold=True, bg=True)

    pdf.ln(4)
    pdf.chapter_title("3", "Liquidación de Tasas e Impuestos Municipales (Ayto. Palma del Río)")
    pdf.table_row("Concepto Tributario Municipal", "Base / Tipo", is_bold=True, bg=True)
    pdf.table_row("Tasa por Licencia Urbanística de Obras", "1,50 % sobre PEM = 4.197,00 €")
    pdf.table_row("Impuesto sobre Construcciones, Instalaciones y Obras (ICIO)", "4,00 % sobre PEM = 11.192,00 €")
    pdf.table_row("Fianza de Gestión de Residuos (Depósito recuperable)", "1.500,00 €")
    pdf.table_row("TOTAL LIQUIDACIÓN INICIAL PARA INICIO DE EXPEDIENTE", "16.889,00 €", is_bold=True, bg=True)

    pdf_path = os.path.join(OUTPUT_DIR, "00_TOMO_IV_MEDICIONES_Y_PRESUPUESTO.pdf")
    pdf.output(pdf_path)
    print(f"TOMO IV PRESUPUESTO GENERADO: {pdf_path}")

if __name__ == "__main__":
    generar_tomo_i_memoria()
    generar_tomo_iii_pliego()
    generar_tomo_iv_presupuesto()
    print("LOS 3 TOMOS ESCRITOS OFICIALES HAN SIDO GENERADOS CON ÉXITO.")
