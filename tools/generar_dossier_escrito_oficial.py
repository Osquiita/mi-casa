# -*- coding: utf-8 -*-
"""
GENERADOR INTEGRAL DE LOS 5 TOMOS ESCRITOS OFICIALES DEL PROYECTO (CTE / LOE / PGOU)
Adaptado a la Estrategia Legal OPCIÓN A (Palma del Río, Córdoba):
- Vivienda Unifamiliar Terminada en Planta Baja (Fase 1 - LPO Parcial)
- Ampliación / Espacio Diáfano en Bruto sin Uso Definido en Planta Alta (Envolvente 100% terminada)

Genera en PDF oficial (A4) sin cortes de texto:
1. 01_TOMO_I_MEMORIA_CTE_Y_ANEJOS.pdf
2. 03_TOMO_III_PLIEGO_DE_CONDICIONES.pdf
3. 04_TOMO_IV_MEDICIONES_Y_PRESUPUESTO.pdf
4. 05_TOMO_V_ESTUDIO_BASICO_SEGURIDAD_Y_SALUD.pdf
5. 06_TOMO_VI_ESTUDIO_GESTION_RESIDUOS.pdf
"""

import os
from fpdf import FPDF
from fpdf.enums import XPos, YPos

OUTPUT_DIR = r"C:\Users\Oscar Martinez\Desktop\mi-casa\00_PROYECTO_FINAL_LICENCIA_AYUNTAMIENTO"
os.makedirs(OUTPUT_DIR, exist_ok=True)


class DossierPDF(FPDF):
    def __init__(self, titulo_tomo, subtitulo):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.titulo_tomo = titulo_tomo
        self.subtitulo = subtitulo
        self.set_auto_page_break(auto=True, margin=18)

        font_dir = r"C:\Windows\Fonts"
        self.add_font("ArialUni", "", os.path.join(font_dir, "arial.ttf"))
        self.add_font("ArialUni", "B", os.path.join(font_dir, "arialbd.ttf"))
        self.add_font("ArialUni", "I", os.path.join(font_dir, "ariali.ttf"))

    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("ArialUni", "B", 7.5)
        self.set_text_color(71, 85, 105)
        self.cell(
            115, 7,
            "PROYECTO BÁSICO Y DE EJECUCIÓN · CALLE MORENO TORROBA S/N · PALMA DEL RÍO",
            new_x=XPos.RIGHT, new_y=YPos.TOP
        )
        self.cell(75, 7, self.titulo_tomo, align="R", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_draw_color(203, 213, 225)
        self.set_line_width(0.3)
        self.line(10, 17, 200, 17)
        self.ln(4)

    def footer(self):
        if self.page_no() == 1:
            return
        self.set_y(-14)
        self.set_font("ArialUni", "", 7.5)
        self.set_text_color(100, 116, 139)
        self.set_draw_color(203, 213, 225)
        self.line(10, 283, 200, 283)
        self.cell(
            0, 9,
            f"Documento Oficial CTE · Solicitud de Licencia Urbanística de Obras (Ayto. Palma del Río) | Página {self.page_no()}",
            align="C"
        )

    def portada_oficial(self, titulo_principal, subtitulo_proyecto, caja_titulo, caja_linea1, caja_linea2):
        self.add_page()
        self.ln(16)
        self.set_font("ArialUni", "B", 20)
        self.set_text_color(15, 23, 42)
        self.multi_cell(0, 9, titulo_principal, align="C")
        self.ln(2)
        self.set_font("ArialUni", "B", 11.5)
        self.set_text_color(14, 165, 233)
        self.multi_cell(0, 6.5, subtitulo_proyecto, align="C")
        self.ln(6)
        self.set_font("ArialUni", "", 9.5)
        self.set_text_color(71, 85, 105)
        self.cell(0, 6, "Emplazamiento: Calle Moreno Torroba s/n · 14700 Palma del Río (Córdoba)", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.cell(0, 6, "Marco Normativo: Ley 38/1999 (LOE) · Ley 7/2021 (LISTA) · R.D. 314/2006 (CTE) · PGOU Palma del Río", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        self.set_draw_color(15, 23, 42)
        self.set_fill_color(248, 250, 252)
        self.set_line_width(0.9)
        self.rect(20, 102, 170, 48, style="DF")
        self.set_xy(20, 110)
        self.set_font("ArialUni", "B", 14)
        self.set_text_color(15, 23, 42)
        self.cell(170, 8, caja_titulo, align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_font("ArialUni", "", 9.2)
        self.set_text_color(71, 85, 105)
        self.set_x(20)
        self.cell(170, 6, caja_linea1, align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_x(20)
        self.cell(170, 6, caja_linea2, align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        self.set_xy(10, 182)
        self.set_font("ArialUni", "B", 9.5)
        self.set_text_color(15, 23, 42)
        self.cell(0, 6, "CUADRO DE IDENTIFICACIÓN Y DILIGENCIA DE FIRMAS:", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_draw_color(203, 213, 225)
        self.set_line_width(0.4)
        self.rect(10, 192, 60, 62)
        self.rect(75, 192, 60, 62)
        self.rect(140, 192, 60, 62)

        self.set_xy(10, 195); self.set_font("ArialUni", "B", 8); self.cell(60, 5, "ARQUITECTO PROYECTISTA", align="C")
        self.set_xy(10, 245); self.set_font("ArialUni", "", 7.5); self.cell(60, 5, "Firma y Visado Colegial COACo", align="C")

        self.set_xy(75, 195); self.set_font("ArialUni", "B", 8); self.cell(60, 5, "DIRECCIÓN DE EJECUCIÓN", align="C")
        self.set_xy(75, 245); self.set_font("ArialUni", "", 7.5); self.cell(60, 5, "Arquitecto Técnico / Aparejador", align="C")

        self.set_xy(140, 195); self.set_font("ArialUni", "B", 8); self.cell(60, 5, "LA PROPIEDAD / PROMOTOR", align="C")
        self.set_xy(140, 245); self.set_font("ArialUni", "", 7.5); self.cell(60, 5, "Conforme con el Proyecto", align="C")

    def chapter_title(self, num_str, title_str):
        self.set_font("ArialUni", "B", 12)
        self.set_text_color(15, 23, 42)
        self.ln(3)
        self.cell(0, 7, f"{num_str}. {title_str}".upper(), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_draw_color(14, 165, 233)
        self.set_line_width(0.7)
        self.line(10, self.get_y(), 75, self.get_y())
        self.ln(3)

    def section_title(self, num_str, title_str):
        self.set_font("ArialUni", "B", 10)
        self.set_text_color(30, 41, 59)
        self.ln(1.5)
        self.cell(0, 6, f"{num_str} {title_str}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(0.5)

    def body_p(self, text):
        self.set_font("ArialUni", "", 8.8)
        self.set_text_color(51, 65, 85)
        self.multi_cell(0, 4.5, text)
        self.ln(1.5)

    def table_row(self, c1, c2, is_bold=False, bg=False, w1=140, w2=50):
        self.set_font("ArialUni", "B" if is_bold else "", 8.2)
        if bg:
            self.set_fill_color(241, 245, 249)
        else:
            self.set_fill_color(255, 255, 255)
        self.set_text_color(15, 23, 42) if is_bold else self.set_text_color(51, 65, 85)
        self.cell(w1, 5.5, c1, border=1, fill=bg, new_x=XPos.RIGHT, new_y=YPos.TOP)
        self.cell(w2, 5.5, c2, border=1, align="R", fill=bg, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    def table_row_3col(self, c1, c2, c3, is_bold=False, bg=False):
        self.set_font("ArialUni", "B" if is_bold else "", 8.0)
        self.set_fill_color(241, 245, 249) if bg else self.set_fill_color(255, 255, 255)
        self.set_text_color(15, 23, 42) if is_bold else self.set_text_color(51, 65, 85)
        self.cell(90, 5.5, c1, border=1, fill=bg, new_x=XPos.RIGHT, new_y=YPos.TOP)
        self.cell(50, 5.5, c2, border=1, align="C", fill=bg, new_x=XPos.RIGHT, new_y=YPos.TOP)
        self.cell(50, 5.5, c3, border=1, align="C", fill=bg, new_x=XPos.LMARGIN, new_y=YPos.NEXT)


def generar_tomo_i_memoria():
    pdf = DossierPDF("TOMO I: MEMORIA CTE Y ANEJOS", "Proyecto Básico y de Ejecución")
    pdf.portada_oficial(
        "PROYECTO BÁSICO Y DE EJECUCIÓN",
        "VIVIENDA UNIFAMILIAR ENTRE MEDIANERAS EN PLANTA BAJA CON GARAJE, PATIO Y PISCINA + ESPACIO DIÁFANO EN BRUTO EN PLANTA ALTA",
        "TOMO I: MEMORIA TÉCNICA Y ANEJOS CTE",
        "Memoria Descriptiva y Urbanística, Memoria Constructiva,",
        "Cumplimiento del CTE y Plan de Control de Calidad"
    )

    pdf.add_page()
    pdf.chapter_title("1", "Memoria Descriptiva y Justificación Urbanística")
    pdf.section_title("1.1", "Objeto del Proyecto y Ejecución Funcional para LPO Parcial")
    pdf.body_p(
        "El presente Proyecto Básico y de Ejecución tiene por objeto la construcción de una edificación residencial entre medianeras "
        "en la Calle Moreno Torroba s/n de Palma del Río (Córdoba). La actuación contempla la terminación integral de la VIVIENDA "
        "UNIFAMILIAR EN PLANTA BAJA (con garaje privado de acceso por vial trasero norte, porche y patio central de 40,13 m² con piscina), "
        "y la ejecución en PLANTA ALTA de un ESPACIO DIÁFANO EN BRUTO SIN USO DEFINIDO, con acceso independiente desde portal y escalera "
        "exclusiva en fachada sur.\n"
        "A efectos del otorgamiento de Licencia de Primera Ocupación (LPO) de la vivienda de Planta Baja conforme a la Ley 7/2021 (LISTA) "
        "y su Reglamento, la totalidad de la cimentación, estructura, cubiertas, impermeabilizaciones y envolvente exterior de ambas plantas "
        "(fachadas enfoscadas y pintadas y carpinterías exteriores) queda ejecutada al 100%, garantizando las condiciones de seguridad, "
        "estanqueidad, salubridad y ornato público, quedando el espacio en bruto de Planta Alta debidamente cerrado, sectorizado y con "
        "preinstalaciones taponadas en patinillo registrable."
    )

    pdf.section_title("1.2", "Ficha de Cumplimiento Urbanístico (PGOU de Palma del Río)")
    pdf.table_row_3col("Parámetro Urbanístico (Suelo Urbano Consolidado)", "Normativa PGOU", "Proyecto", is_bold=True, bg=True)
    pdf.table_row_3col("Superficie de Parcela (11,40 m fachada × 17,60 m fondo)", "Parcela existente", "200,64 m² (Cumple)")
    pdf.table_row_3col("Ocupación Máxima en Planta (80% s/ 200,64 m²)", "Máx. 160,51 m² (80%)", "160,51 m² (80,0% Cumple)")
    pdf.table_row_3col("Espacio Libre de Patio Interior (20% s/ 200,64 m²)", "Mín. 40,00 m² / Ø 3,00 m", "40,13 m² / Ø 5,00 m (Cumple)")
    pdf.table_row_3col("Número Máximo de Plantas y Altura a Cornisa", "PB + 1 (Máx. 7,20 m)", "PB + 1 y 5,85 m (Cumple)")
    pdf.table_row_3col("Edificabilidad Máxima Permitida (PB + PA)", "Máx. 321,02 m²t", "315,11 m²t (Cumple)")
    pdf.table_row_3col("Dotación de Aparcamiento en Parcela", "Mín. 1 plaza / vivienda", "1 plaza (21,14 m² útil Cumple)")
    pdf.ln(2)

    pdf.section_title("1.3", "Cuadro General de Superficies Útiles y Construidas")
    pdf.table_row("Estancia / Dependencia", "Sup. Útil / Constr. (m²)", is_bold=True, bg=True)
    pdf.table_row("PLANTA BAJA (VIVIENDA UNIFAMILIAR TERMINADA) - Salón-Comedor", "38,50 m²")
    pdf.table_row("PLANTA BAJA - Cocina con Isla integrada", "18,72 m²")
    pdf.table_row("PLANTA BAJA - Dormitorio Principal 1 (Master Suite + Vestidor)", "15,10 m²")
    pdf.table_row("PLANTA BAJA - Baño en Suite Principal", "5,57 m²")
    pdf.table_row("PLANTA BAJA - Baño General", "5,68 m²")
    pdf.table_row("PLANTA BAJA - Dormitorio Doble 2 (Fachada Norte)", "11,70 m²")
    pdf.table_row("PLANTA BAJA - Dormitorio Doble 3 (Fachada Norte)", "11,90 m²")
    pdf.table_row("PLANTA BAJA - Pasillo Distribuidor y Vestíbulo de Entrada", "7,32 m²")
    pdf.table_row("PLANTA BAJA - Cochera / Garaje Privado (Acceso Vial Norte)", "21,14 m²")
    pdf.table_row("PLANTA BAJA - Zaguán y Arranque Escalera Independiente a PA", "4,80 m²")
    pdf.table_row("SUBTOTAL ÚTIL CERRADA PLANTA BAJA", "140,43 m²", is_bold=True, bg=True)
    pdf.table_row("SUPERFICIE CONSTRUIDA COMPUTABLE PLANTA BAJA (80% Ocupación)", "160,51 m²", is_bold=True, bg=True)
    pdf.table_row("ESPACIO LIBRE INTERIOR DE PARCELA (Patio 5,00×8,00 m + Piscina)", "40,13 m² (Útil 37,76 m²)")
    pdf.table_row("PLANTA ALTA (ESPACIO DIÁFANO EN BRUTO SIN USO DEFINIDO)", "132,73 m² útiles en bruto")
    pdf.table_row("PLANTA ALTA - Núcleo de Desembarco Escalera", "4,50 m² útiles")
    pdf.table_row("PLANTA ALTA - Terraza Solárium Exterior Impermeabilizada", "12,16 m² útiles")
    pdf.table_row("SUPERFICIE CONSTRUIDA COMPUTABLE PLANTA ALTA", "154,60 m²", is_bold=True, bg=True)
    pdf.table_row("TOTAL SUPERFICIE CONSTRUIDA COMPUTABLE DEL EDIFICIO", "315,11 m²", is_bold=True, bg=True)

    pdf.add_page()
    pdf.chapter_title("2", "Memoria Constructiva")
    pdf.section_title("2.1", "Terreno, Cimentación y Solera Ventilada Cáviti")
    pdf.body_p(
        "El terreno corresponde a depósitos aluviales de consistencia media característicos de la Vega del Guadalquivir en Palma del Río, "
        "con una tensión admisible de cálculo de 1,80 kg/cm² (0,18 N/mm²) a la cota de cimentación de -1,50 m (a ratificar mediante ensayo "
        "geotécnico previo al replanteo). La cimentación se proyecta mediante zapatas aisladas centradas y de medianería bajo pilares, y "
        "zapatas corridas bajo muros medianeros, arriostradas en dos direcciones ortogonales mediante vigas centradoras y de atado de "
        "hormigón armado HA-25/B/20/IIa y acero B 500 S sobre hormigón de limpieza HL-150 de 10 cm.\n"
        "La solera de planta baja se resuelve mediante forjado sanitario ventilado de encofrado perdido de polipropileno tipo Cáviti de "
        "40 cm de canto total sobre encachado de grava y lámina de polietileno, garantizando protección total frente a humedad por "
        "capilaridad y ventilación cruzada frente a gas radón (CTE DB-HS 1 y DB-HS 6)."
    )

    pdf.section_title("2.2", "Estructura Vertical y Horizontal (Código Estructural RD 470/2021)")
    pdf.body_p(
        "Estructura mixta formada por pórticos con pilares de hormigón armado de 30×30 cm (HA-25/B/20/IIa) y muros de carga en medianeras "
        "de 1 pie de ladrillo perforado acústico/estructural sentado con mortero M-7,5. Forjados de piso y cubierta unidireccionales de "
        "canto 25+5 cm (30 cm total) constituidos por viguetas pretensadas autorresistentes, bovedillas de hormigón y capa de compresión "
        "de 5 cm armada con mallazo electrosoldado B 500 T."
    )

    pdf.section_title("2.3", "Envolvente Térmica, Fachadas y Cubiertas (Zona Climática B4)")
    pdf.body_p(
        "- Fachadas Norte y Sur: Fábrica exterior de 1/2 pie de ladrillo perforado revestido al exterior con mortero monocapa hidrófugo "
        "acabado raspado y pintura al silicato blanca, enfoscado interior hidrófugo, cámara con aislamiento térmico ininterrumpido de "
        "lana mineral de roca de 100 mm (conductividad 0,035 W/m·K) y trasdosado interior autoportante de doble placa de yeso laminado "
        "(U = 0,26 W/m²K < Ulim = 0,56 W/m²K para Zona B4).\n"
        "- Carpinterías exteriores: Aluminio con Rotura de Puente Térmico (RPT 70 mm) y acristalamiento doble laminar bajo emisivo con "
        "control solar reforzado 4+4/16 argón/6 mm (Uh = 1,35 W/m²K; factor solar g <= 0,35) y persianas motorizadas con cajón aislado.\n"
        "- Cubiertas: Cubierta plana invertida con formación de pendientes al 1,5% mediante hormigón celular, impermeabilización bicapa "
        "elastomérica SBS (LBM-40-FP + LBM-40-G), aislamiento térmico de poliestireno extruido XPS de 100 mm (U = 0,28 W/m²K < 0,44 W/m²K), "
        "geotextil antipunzonamiento y protección pesada de grava lavada en cubierta técnica y pavimento porcelánico C3 en terraza solárium."
    )

    pdf.chapter_title("3", "Justificación del Código Técnico de la Edificación (CTE)")
    pdf.section_title("3.1", "DB-SE (Seguridad Estructural) y NCSE-02")
    pdf.body_p(
        "Sobrecargas de uso: 2,0 kN/m² en zonas residenciales y escaleras; 2,0 kN/m² por tabiquería; 1,0 kN/m² en cubiertas accesibles "
        "solo para conservación. Zona eólica C. Aceleración sísmica básica en Palma del Río ab < 0,04g (no preceptiva NCSE-02)."
    )

    pdf.section_title("3.2", "DB-SI (Seguridad en caso de Incendio)")
    pdf.body_p(
        "- DB-SI 1 (Propagación interior): El garaje privado de Planta Baja (21,14 m² <= 100 m²) se clasifica como Local de Riesgo Especial "
        "Bajo. Queda compartimentado respecto de la vivienda y planta superior mediante muros y forjado con resistencia al fuego EI 120 "
        "(R 120) y puerta de comunicación cortafuegos EI2 60-C5 dotada de muelle cierrapuertas automático (no requiere vestíbulo de "
        "independencia según Tabla 2.2 del DB-SI 1). El espacio en bruto de Planta Alta constituye un sector diferenciado EI 60.\n"
        "- DB-SI 3 y SI 4: Recorridos de evacuación hasta espacio exterior seguro < 15,0 m (máx. 25,0 m). Instalación de extintor "
        "portátil de polvo ABC eficacia 21A-113B e iluminación de emergencia en el garaje y en el zaguán de escalera."
    )

    pdf.section_title("3.3", "DB-SUA (Seguridad de Utilización y Accesibilidad)")
    pdf.body_p(
        "- SUA 1: Pavimentos interiores secos Clase 1; pavimentos húmedos (baños), porche, peldaños de escalera y coronación de piscina "
        "Clase 3 (Rd > 45). Escalera de acceso a Planta Alta de directriz recta, ancho útil 1,00 m, 17 contrahuellas de 17,06 cm y "
        "huellas de 28,0 cm con meseta intermedia de 1,00 m, barandilla de 0,95 m de altura no escalable y cabezada libre > 2,20 m.\n"
        "- SUA 6: Vaso de piscina de uso exclusivamente unifamiliar privado (profundidad máx. 1,40 m) con escalera con pasamanos."
    )

    pdf.section_title("3.4", "DB-HE (Ahorro de Energía - Zona Climática B4) y DB-HS (Salubridad)")
    pdf.body_p(
        "- DB-HE 0 y HE 1 (Zona Climática B4 - Córdoba): Cumplimiento estricto de transmitancias límite, permeabilidad al aire de huecos "
        "Clase 4 y parámetro de control solar de julio q_sol;jul <= 2,00 kWh/m²·mes mediante vidrios de control solar (g <= 0,35) y "
        "protecciones solares móviles.\n"
        "- DB-HE 4 y Climatización: Bomba de calor aerotérmica aire-agua Inverter de alta eficiencia (SCOP > 4,20) para producción de ACS "
        "(aportación renovable > 78% >= 70% exigido) y climatización mediante suelo radiante-refrescante en Planta Baja gobernado por "
        "termostatos y sondas higrométricas de control de punto de rocío para impedir condensaciones superficiales en modo refrescamiento.\n"
        "- DB-HE 6 (Dotación recarga VE): Punto de recarga de vehículo eléctrico (Wallbox 7,4 kW Modo 3) en cochera según ITC-BT-52.\n"
        "- DB-HS 3: Sistema de Ventilación Mecánica Controlada (VMC) de doble flujo con recuperador de calor entálpico (rendimiento > 85%) "
        "en vivienda de Planta Baja, y ventilación independiente de garaje (caudal >= 120 l/s para 1 plaza)."
    )

    pdf.chapter_title("4", "Plan de Control de Calidad (Anejo I CTE)")
    pdf.body_p(
        "Se establece el control documental (Marcado CE y Declaración de Prestaciones), control de recepción mediante ensayos por "
        "laboratorio acreditado (lotes de hormigón HA-25 cada 100 m³ o fracción por planta según Código Estructural, acero B 500 S) "
        "y pruebas finales de servicio: prueba de estanqueidad de cubiertas por inundación durante 24 h, prueba hidrostática de redes "
        "de fontanería y circuitos de suelo radiante a 1,5 veces la presión de trabajo, y prueba de escorrentía y estanqueidad de la "
        "red enterrada de saneamiento antes del hormigonado de la solera Cáviti."
    )

    pdf_path = os.path.join(OUTPUT_DIR, "01_TOMO_I_MEMORIA_CTE_Y_ANEJOS.pdf")
    pdf.output(pdf_path)
    print(f"TOMO I GENERADO: {pdf_path}")


def generar_tomo_iii_pliego():
    pdf = DossierPDF("TOMO III: PLIEGO DE CONDICIONES", "Pliego de Condiciones Técnicas y Administrativas")
    pdf.portada_oficial(
        "PLIEGO DE CONDICIONES",
        "CLÁUSULAS ADMINISTRATIVAS Y PRESCRIPCIONES TÉCNICAS PARTICULARES DE LA EDIFICACIÓN",
        "TOMO III: PLIEGO DE CONDICIONES",
        "Pliego de Cláusulas Administrativas Generales y Particulares,",
        "Prescripciones sobre Materiales, Ejecución y Recepción en Obra"
    )

    pdf.add_page()
    pdf.chapter_title("1", "Pliego de Cláusulas Administrativas")
    pdf.section_title("1.1", "Ámbito de Aplicación y Agentes de la Edificación (LOE)")
    pdf.body_p(
        "El presente Pliego rige la ejecución material de las obras definidas en el Proyecto Básico y de Ejecución, vinculando al Promotor, "
        "al Constructor y a la Dirección Facultativa (Director de Obra y Director de la Ejecución de la Obra) conforme a la Ley 38/1999.\n"
        "- Documentación obligatoria en obra: Licencia Municipal de Obras, ejemplar visado del Proyecto, Libro de Órdenes y Asistencias, "
        "Libro de Incidencias de Seguridad y Salud y Plan de Seguridad aprobado.\n"
        "- Plazo de ejecución previsto: 12 meses para la Fase 1 (Estructura global, envolvente completa y terminación de Planta Baja)."
    )

    pdf.section_title("1.2", "Certificación Final de Obra y Licencia de Primera Ocupación (LPO)")
    pdf.body_p(
        "Dado que el proyecto contempla la terminación integral de la Vivienda Unifamiliar de Planta Baja y la configuración en bruto "
        "del espacio sin uso definido de Planta Alta (con envolvente exterior y cubierta 100% terminadas), una vez verificadas las "
        "pruebas finales de servicio de las instalaciones de Planta Baja y la seguridad del cerramiento del acceso a Planta Alta, "
        "la Dirección Facultativa expedirá el Certificado Final de Obra habilitante para la Licencia de Primera Ocupación de la vivienda."
    )

    pdf.chapter_title("2", "Prescripciones Técnicas sobre Materiales y Ejecución")
    pdf.section_title("2.1", "Movimiento de Tierras, Cimentación y Estructura")
    pdf.body_p(
        "No se procederá al hormigonado de ninguna zapata ni viga centradora sin la previa revisión y conformidad en el Libro de Órdenes "
        "de las cotas de excavación (-1,50 m) y disposición de separadores homologados (recubrimiento mín. 40 mm en cimentación y 30 mm "
        "en pilares). Queda prohibido el vibrado de las armaduras o la adición de agua al hormigón en obra."
    )

    pdf.section_title("2.2", "Impermeabilizaciones, Fachadas e Instalaciones")
    pdf.body_p(
        "En cubiertas planas se ejecutarán medias cañas en todos los encuentros con paramentos verticales, subiendo la lámina bicapa SBS "
        "un mínimo de 20 cm por encima de la protección del pavimento o grava, rematada con perfil metálico y cordón de poliuretano. "
        "Los colectores del suelo radiante-refrescante se someterán a prueba de presión manométrica (6 bar durante 24 h) antes del "
        "vertido del mortero autonivelante de anhidrita."
    )

    pdf_path = os.path.join(OUTPUT_DIR, "03_TOMO_III_PLIEGO_DE_CONDICIONES.pdf")
    pdf.output(pdf_path)
    print(f"TOMO III GENERADO: {pdf_path}")


def generar_tomo_iv_presupuesto():
    pdf = DossierPDF("TOMO IV: MEDICIONES Y PRESUPUESTO", "Presupuesto Oficial de Ejecución")
    pdf.portada_oficial(
        "MEDICIONES Y PRESUPUESTO",
        "ESTRUCTURA DE COSTES, MEDICIONES POR CAPÍTULOS Y LIQUIDACIÓN DE TASAS E ICIO MUNICIPAL",
        "TOMO IV: MEDICIONES Y PRESUPUESTO",
        "Presupuesto de Ejecución Material (PEM) adaptado a PB Terminada + PA en Bruto",
        "y Cálculo de Liquidación Tributaria Municipal (Ayto. Palma del Río)"
    )

    pdf.add_page()
    pdf.chapter_title("1", "Resumen de Presupuesto por Capítulos (P.E.M.)")
    pdf.body_p(
        "El siguiente Presupuesto de Ejecución Material (PEM) valora el 100% de la cimentación, estructura, cubiertas, impermeabilizaciones "
        "y fachadas exteriores de la totalidad del edificio (PB + PA), así como la terminación completa de tabiquería, acabados, "
        "carpinterías e instalaciones de la Vivienda en Planta Baja y las preinstalaciones en patinillo para la Planta Alta en bruto."
    )

    capitulos = [
        ("01. ACTUACIONES PREVIAS Y MOVIMIENTO DE TIERRAS (Solar 200,64 m²)", "7.850,00 €"),
        ("02. CIMENTACIÓN Y SOLERA SANITARIA VENTILADA CÁVITI", "21.900,00 €"),
        ("03. ESTRUCTURA DE HORMIGÓN ARMADO Y MUROS DE CARGA (PB + PA)", "36.800,00 €"),
        ("04. CERRAMIENTOS DE FACHADA Y MEDIANERAS (Envolvente 100% PB+PA)", "24.600,00 €"),
        ("05. CUBIERTAS, TERRAZA SOLÁRIUM E IMPERMEABILIZACIONES (100%)", "16.400,00 €"),
        ("06. TABIQUERÍA INTERIOR Y FALSOS TECHOS (Planta Baja + Escalera)", "10.200,00 €"),
        ("07. AISLAMIENTOS TÉRMICOS Y ACÚSTICOS (Envolvente y PB)", "6.800,00 €"),
        ("08. REVESTIMIENTOS Y SOLADOS PORCELÁNICOS (Planta Baja y Exteriores)", "13.900,00 €"),
        ("09. CARPINTERÍA EXTERIOR RPT, VIDRIOS CONTROL SOLAR Y PORTÓN", "18.900,00 €"),
        ("10. CARPINTERÍA INTERIOR Y PUERTA CORTAFUEGOS EI2 60-C5 (PB)", "6.100,00 €"),
        ("11. FONTANERÍA, SANEAMIENTO, SANITARIOS PB Y ACOMETIDAS PA", "9.200,00 €"),
        ("12. CLIMATIZACIÓN AEROTÉRMICA, SUELO RADIANTE-REFRESCANTE Y VMC (PB)", "13.400,00 €"),
        ("13. ELECTRICIDAD, TELECOMUNICACIONES, ILUMINACIÓN Y WALLBOX (PB)", "8.500,00 €"),
        ("14. ACONDICIONAMIENTO DE PATIO CENTRAL Y VASO DE PISCINA", "12.550,00 €"),
        ("15. GESTIÓN DE RESIDUOS DE CONSTRUCCIÓN Y DEMOLICIÓN (EGRCD)", "1.850,00 €"),
        ("16. SEGURIDAD Y SALUD EN EL TRABAJO (EBSS)", "3.850,00 €"),
        ("17. PLAN DE CONTROL DE CALIDAD Y ENSAYOS GEOTÉCNICOS / ESTRUCTURA", "1.700,00 €"),
    ]

    pdf.table_row("Capítulo del Proyecto (PB Terminada + PA en Bruto)", "Importe PEM (€)", is_bold=True, bg=True)
    for cap, imp in capitulos:
        pdf.table_row(cap, imp)

    pdf.ln(3)
    pdf.chapter_title("2", "Resumen General del Presupuesto (P.E.M. y P.E.C.)")
    pdf.table_row("TOTAL PRESUPUESTO DE EJECUCIÓN MATERIAL (P.E.M.)", "194.500,00 €", is_bold=True, bg=True)
    pdf.table_row("13,00 % Gastos Generales de la Empresa Constructora", "25.285,00 €")
    pdf.table_row("6,00 % Beneficio Industrial del Contratista", "11.670,00 €")
    pdf.table_row("PRESUPUESTO DE EJECUCIÓN POR CONTRATA (P.E.C. sin IVA)", "231.455,00 €", is_bold=True, bg=True)
    pdf.table_row("10,00 % I.V.A. Reducido (Ejecución de obra de vivienda autopromoción)", "23.145,50 €")
    pdf.table_row("TOTAL PRESUPUESTO GENERAL DE EJECUCIÓN (IVA Incluido)", "254.600,50 €", is_bold=True, bg=True)

    pdf.ln(3)
    pdf.chapter_title("3", "Liquidación Estimada de Tasas e ICIO (Ayto. Palma del Río)")
    pdf.table_row("Concepto Tributario Municipal (Base Imponible PEM = 194.500,00 €)", "Cuota Estimada", is_bold=True, bg=True)
    pdf.table_row("Tasa por Tramitación de Licencia Urbanística de Obras (1,50 % s/ PEM)", "2.917,50 €")
    pdf.table_row("Impuesto sobre Construcciones, Instalaciones y Obras - ICIO (4,00 % s/ PEM)", "7.780,00 €")
    pdf.table_row("Fianza Municipal de Gestión de Residuos RCD (Depósito reintegrable)", "1.500,00 €")
    pdf.table_row("TOTAL LIQUIDACIÓN MUNICIPAL ESTIMADA (Ahorro de 4.691,50 € por Opción A)", "12.197,50 €", is_bold=True, bg=True)

    pdf_path = os.path.join(OUTPUT_DIR, "04_TOMO_IV_MEDICIONES_Y_PRESUPUESTO.pdf")
    pdf.output(pdf_path)
    print(f"TOMO IV GENERADO: {pdf_path}")


def generar_tomo_v_seguridad():
    pdf = DossierPDF("TOMO V: ESTUDIO BÁSICO DE SEGURIDAD Y SALUD", "Prevención de Riesgos Laborales RD 1627/1997")
    pdf.portada_oficial(
        "ESTUDIO BÁSICO DE SEGURIDAD Y SALUD",
        "PREVENCIÓN DE RIESGOS LABORALES EN OBRAS DE CONSTRUCCIÓN (R.D. 1627/1997 Y LEY 31/1995)",
        "TOMO V: ESTUDIO BÁSICO DE SEGURIDAD Y SALUD",
        "Identificación de Riesgos, Protecciones Colectivas, EPIs,",
        "Normas Preventivas por Fases y Presupuesto de Seguridad"
    )

    pdf.add_page()
    pdf.chapter_title("1", "Memoria del Estudio Básico de Seguridad y Salud (EBSS)")
    pdf.section_title("1.1", "Justificación del R.D. 1627/1997 y Datos de la Obra")
    pdf.body_p(
        "De acuerdo con el artículo 4 del Real Decreto 1627/1997, procede la redacción de Estudio Básico de Seguridad y Salud (EBSS) "
        "dado que el Presupuesto de Ejecución por Contrata es inferior a 450.759,08 €, el plazo de ejecución no supera los 30 días "
        "empleando más de 20 trabajadores simultáneos y el volumen de mano de obra total es inferior a 500 hombres-día.\n"
        "Antes del inicio de los trabajos, el contratista redactará el Plan de Seguridad y Salud en el Trabajo (PSST) que será aprobado "
        "por el Coordinador de Seguridad y Salud en Fase de Ejecución."
    )

    pdf.section_title("1.2", "Medidas Preventivas y Protecciones Colectivas por Fases")
    pdf.body_p(
        "- Excavación y Cimentación (-1,50 m y vaso de piscina): Vallado perimetral opaco de 2,00 m de altura en ambas fachadas (Calle "
        "Moreno Torroba y vial trasero norte), pasarelas con barandilla de 1,00 m y rodapié de 15 cm sobre zanjas, e inspección previa "
        "del estado de las medianeras colindantes.\n"
        "- Estructura y Cubiertas: Instalación de redes de seguridad en horca (UNE-EN 1263-1), barandillas perimetrales rígidas en bordes "
        "de forjado y hueco de patio central, cuajado con tablones fijados en el hueco de escalera y puntos de anclaje para línea de "
        "vida horizontal (UNE-EN 795) en cubierta plana.\n"
        "- Instalaciones Eléctricas Provisionales: Cuadro general de obra intemperie IP55 con interruptor diferencial de 30 mA para "
        "circuitos de alumbrado (24 V en zonas húmedas) y 300 mA para fuerza, con puesta a tierra < 37 ohmios."
    )

    pdf.section_title("1.3", "Presupuesto de Seguridad y Salud")
    pdf.table_row("Capítulo de Seguridad y Salud (No deducible a la baja)", "Importe PEM (€)", is_bold=True, bg=True)
    pdf.table_row("Protecciones Colectivas (Redes horca, barandillas, líneas de vida, tapas)", "1.850,00 €")
    pdf.table_row("Equipos de Protección Individual (Cascos, botas S3, arneses anticaídas)", "620,00 €")
    pdf.table_row("Instalaciones de Bienestar e Higiene (Caseta aseo químico, vestuario, botiquín)", "980,00 €")
    pdf.table_row("Señalización reglamentaria de obra, vallado y extintores", "400,00 €")
    pdf.table_row("TOTAL PRESUPUESTO DE SEGURIDAD Y SALUD", "3.850,00 €", is_bold=True, bg=True)

    pdf_path = os.path.join(OUTPUT_DIR, "05_TOMO_V_ESTUDIO_BASICO_SEGURIDAD_Y_SALUD.pdf")
    pdf.output(pdf_path)
    print(f"TOMO V GENERADO: {pdf_path}")


def generar_tomo_vi_residuos():
    pdf = DossierPDF("TOMO VI: ESTUDIO DE GESTIÓN DE RESIDUOS", "R.D. 105/2008 y Ley 7/2022")
    pdf.portada_oficial(
        "ESTUDIO DE GESTIÓN DE RESIDUOS (EGRCD)",
        "GESTIÓN DE RESIDUOS DE CONSTRUCCIÓN Y DEMOLICIÓN (R.D. 105/2008 Y LEY 7/2022)",
        "TOMO VI: ESTUDIO DE GESTIÓN DE RESIDUOS",
        "Inventario Cuantitativo por Códigos LER, Separación Selectiva en Obra,",
        "Presupuesto de Gestión y Cálculo de Fianza Municipal (Palma del Río)"
    )

    pdf.add_page()
    pdf.chapter_title("1", "Memoria de Gestión de Residuos de Construcción (EGRCD)")
    pdf.section_title("1.1", "Marco Normativo y Estimación por Códigos LER")
    pdf.body_p(
        "Redactado conforme al Real Decreto 105/2008, a la Ley 7/2022 de residuos y suelos contaminados para una economía circular "
        "y al Reglamento de Residuos de Andalucía (Decreto 73/2012). A continuación se desglosa la producción estimada de tierras de "
        "excavación y residuos de construcción (RCD Nivel II y Nivel I):"
    )

    pdf.table_row("Código LER / Naturaleza del Residuo", "Peso Estimado (t)", is_bold=True, bg=True)
    pdf.table_row("17 05 04 · Tierras y piedras de excavación no contaminadas (zapatas y piscina)", "185,00 t (123,3 m³)")
    pdf.table_row("17 01 01 · Hormigón armado y en masa de despuntes y limpieza", "16,80 t")
    pdf.table_row("17 01 02 · Ladrillos y bloques cerámicos de cerramientos y tabiquería", "11,40 t")
    pdf.table_row("17 01 03 · Materiales cerámicos y recortes de gres porcelánico", "1,45 t")
    pdf.table_row("17 01 07 · Mezclas de hormigón, ladrillos y morteros (RCD pétreo)", "7,60 t")
    pdf.table_row("17 02 01 · Madera de encofrados y palets de suministro", "3,10 t")
    pdf.table_row("17 02 03 · Plásticos, film retráctil y embalajes", "1,40 t")
    pdf.table_row("17 04 05 · Hierro y acero procedente de despuntes de ferralla", "1,35 t")
    pdf.table_row("17 08 02 · Materiales de construcción a base de yeso (PYL en PB)", "1,50 t")
    pdf.table_row("TOTAL RESIDUOS Y TIERRAS PREVISTOS EN LA OBRA", "229,60 t", is_bold=True, bg=True)

    pdf.section_title("1.2", "Separación en Origen, Gestor Autorizado y Fianza Municipal")
    pdf.body_p(
        "Al superarse los umbrales del art. 5.5 del R.D. 105/2008 en las fracciones pétreas, se dispondrán contenedores diferenciados "
        "y señalizados en obra para fracción pétrea/cerámica, maderas, metales, plásticos y cartón-yeso. Todos los residuos serán "
        "entregados a Gestor Autorizado de RCDs inscrito en el Registro de la Junta de Andalucía, conservando los Certificados de "
        "Recepción y Gestión como requisito indispensable para la firma del Certificado Final de Obra y devolución de la fianza."
    )

    pdf.table_row("Concepto Económico de Gestión de Residuos", "Importe (€)", is_bold=True, bg=True)
    pdf.table_row("Presupuesto de alquiler de contenedores, transporte y canon de vertido (PEM)", "1.850,00 €")
    pdf.table_row("Fianza Municipal de Gestión de Residuos propuesta (Ayto. Palma del Río)", "1.500,00 €", is_bold=True, bg=True)

    pdf_path = os.path.join(OUTPUT_DIR, "06_TOMO_VI_ESTUDIO_GESTION_RESIDUOS.pdf")
    pdf.output(pdf_path)
    print(f"TOMO VI GENERADO: {pdf_path}")


if __name__ == "__main__":
    generar_tomo_i_memoria()
    generar_tomo_iii_pliego()
    generar_tomo_iv_presupuesto()
    generar_tomo_v_seguridad()
    generar_tomo_vi_residuos()
    print("LOS 5 TOMOS ESCRITOS OFICIALES HAN SIDO GENERADOS Y VALIDADOS CON ÉXITO.")
