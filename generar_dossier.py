# -*- coding: utf-8 -*-
"""Genera el dossier ejecutivo profesional para el cliente final.
Incluye portada, memoria descriptiva, cuadro de superficies,
planos (PNG previews), galeria de renders y presupuesto."""
import os
from fpdf import FPDF
from PIL import Image

BASE = r"C:\Users\Oscar Martinez\Desktop\mi-casa"
OUT  = os.path.join(BASE, "entrega", "documentacion")
os.makedirs(OUT, exist_ok=True)

# ================================================================ UTILIDADES
def best_renders():
    """Selecciona los mejores renders disponibles."""
    renders_dir = os.path.join(BASE, "entrega", "renders")
    candidates = [
        ("Fachada Principal (Dia)", os.path.join(renders_dir, "01-fachada-principal.png")),
        ("Fachada Principal (Noche)", os.path.join(renders_dir, "02-fachada-nocturna.png")),
        ("Alzado Trasero", os.path.join(renders_dir, "03-alzado-trasero.png")),
        ("Vista Axonometrica 3D", os.path.join(renders_dir, "04-vista-axonometrica.png")),
        ("Patio Central y Pergola", os.path.join(renders_dir, "05-patio-central.png")),
        ("Interior Salon Planta Baja", os.path.join(renders_dir, "06-interior-salon-pb.png")),
        ("Interior Cocina e Isla PB", os.path.join(renders_dir, "07-interior-cocina-pb.png")),
        ("Dormitorio Principal", os.path.join(renders_dir, "08-dormitorio-principal.png")),
        ("Interior Salon Planta Alta", os.path.join(renders_dir, "09-interior-salon-pa.png")),
        ("Porche y Patio Interior", os.path.join(renders_dir, "10-porche-patio.png")),
        # Fallbacks
        ("Fachada Principal", os.path.join(BASE, "pro-fachada.png")),
        ("Fachada Alternativa", os.path.join(BASE, "pro-fachada2.png")),
        ("Alzado Trasero (pro)", os.path.join(BASE, "pro-trasera.png")),
        ("Vista Axonometrica (pro)", os.path.join(BASE, "pro-axo.png")),
        ("Patios y Porche (pro)", os.path.join(BASE, "pro-patios.png")),
        ("Interior Planta Baja (pro)", os.path.join(BASE, "pro-interior-pb.png")),
        ("Interior Planta Alta (pro)", os.path.join(BASE, "pro-interior-pa.png")),
    ]
    result = []
    for title, path in candidates:
        if os.path.exists(path):
            result.append((title, path))
    return result[:10]  # max 10 renders

def plan_previews():
    """Obtiene las previews de los planos."""
    plans = [
        ("P-00: Parcela y Situacion", "preview-01-parcela.png"),
        ("P-01: Planta Baja (Vivienda A)", "preview-02-planta-baja.png"),
        ("P-02: Planta Alta (Vivienda B)", "preview-03-planta-alta.png"),
        ("P-03/P-04: Alzados y Seccion", "preview-04-alzados-seccion.png"),
        ("P-05: Cuadro de Superficies", "preview-05-cuadro-superficies.png"),
    ]
    result = []
    for title, fname in plans:
        path = os.path.join(BASE, fname)
        if os.path.exists(path):
            result.append((title, path))
    return result

# ================================================================ PDF
class DossierPDF(FPDF):
    def __init__(self):
        super().__init__('L', 'mm', 'A4')  # Landscape for architectural presentation
        self.set_auto_page_break(auto=True, margin=15)
    
    def header(self):
        if self.page_no() > 1:
            self.set_font("Helvetica", "I", 8)
            self.set_text_color(120, 120, 120)
            self.cell(0, 5, "Vivienda Bifamiliar . Palma del Rio (Cordoba)", align="L")
            self.cell(0, 5, f"Pag. {self.page_no()}", align="R", new_x="LMARGIN", new_y="NEXT")
            self.line(10, 12, 287, 12)
    
    def footer(self):
        self.set_y(-10)
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(150, 150, 150)
        self.cell(0, 5, "Documento confidencial . Proyecto Arquitectonico . 2026", align="C")

pdf = DossierPDF()

# ================================================================ PORTADA
pdf.add_page()
pdf.set_fill_color(25, 30, 40)
pdf.rect(0, 0, 297, 210, 'F')

# Imagen de portada (si existe un buen render de fachada)
cover_img = os.path.join(BASE, "pro-fachada.png")
if os.path.exists(cover_img):
    pdf.image(cover_img, x=0, y=0, w=297, h=210)
    # Overlay oscuro
    pdf.set_fill_color(0, 0, 0)
    pdf.set_draw_color(0, 0, 0)
    # Use a semi-transparent overlay effect by drawing multiple thin rectangles
    for i in range(80):
        alpha = 0.6
        pdf.set_fill_color(20, 25, 35)
        pdf.rect(0, 210 - 80 + i, 297, 1, 'F')

pdf.set_y(140)
pdf.set_font("Helvetica", "B", 36)
pdf.set_text_color(255, 255, 255)
pdf.cell(0, 18, "VIVIENDA BIFAMILIAR", align="C", new_x="LMARGIN", new_y="NEXT")
pdf.set_font("Helvetica", "", 18)
pdf.set_text_color(200, 200, 200)
pdf.cell(0, 10, "Palma del Rio . Cordoba", align="C", new_x="LMARGIN", new_y="NEXT")
pdf.ln(5)
pdf.set_font("Helvetica", "", 12)
pdf.set_text_color(170, 180, 190)
pdf.cell(0, 8, "Proyecto Basico y de Ejecucion", align="C", new_x="LMARGIN", new_y="NEXT")
pdf.cell(0, 8, "Agosto 2026", align="C", new_x="LMARGIN", new_y="NEXT")

# ================================================================ INDICE
pdf.add_page()
pdf.set_fill_color(255, 255, 255)
pdf.set_text_color(30, 35, 45)
pdf.set_font("Helvetica", "B", 28)
pdf.ln(15)
pdf.cell(0, 15, "INDICE", new_x="LMARGIN", new_y="NEXT")
pdf.ln(8)

toc = [
    ("1.", "Memoria Descriptiva", "3"),
    ("2.", "Datos del Solar y Normativa", "4"),
    ("3.", "Programa Funcional", "5"),
    ("4.", "Cuadro de Superficies", "6"),
    ("5.", "Planos Tecnicos", "7"),
    ("6.", "Visualizacion 3D - Galeria de Renders", "12"),
    ("7.", "Presupuesto Estimado", "17"),
    ("8.", "Ficha de Materiales y Acabados", "18"),
]

for num, title, page in toc:
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(50, 60, 80)
    pdf.cell(12, 10, num)
    pdf.set_font("Helvetica", "", 14)
    pdf.set_text_color(40, 45, 55)
    pdf.cell(200, 10, title)
    pdf.set_font("Helvetica", "", 14)
    pdf.set_text_color(120, 130, 140)
    pdf.cell(0, 10, page, align="R", new_x="LMARGIN", new_y="NEXT")
    pdf.line(22, pdf.get_y(), 275, pdf.get_y())
    pdf.ln(2)

# ================================================================ 1. MEMORIA DESCRIPTIVA
pdf.add_page()
pdf.set_text_color(30, 35, 45)
pdf.set_font("Helvetica", "B", 24)
pdf.ln(5)
pdf.cell(0, 12, "1. MEMORIA DESCRIPTIVA", new_x="LMARGIN", new_y="NEXT")
pdf.ln(5)
pdf.set_draw_color(60, 80, 120)
pdf.line(10, pdf.get_y(), 100, pdf.get_y())
pdf.ln(8)

pdf.set_font("Helvetica", "", 11)
pdf.set_text_color(50, 55, 65)

memoria = """El presente proyecto define la construccion de una VIVIENDA BIFAMILIAR entre medianeras en la localidad de Palma del Rio (Cordoba), sobre un solar de 200 m2 con fachada a dos calles: Calle Moreno Torroba al frente y calle trasera al fondo.

El edificio se organiza en dos viviendas completamente independientes:

    . Vivienda A (Planta Baja): Acceso por Portal A (fachada principal izquierda). Programa de 3 dormitorios, 2 banos, salon-comedor de 37 m2, cocina con isla de 20 m2, cochera con acceso a calle trasera y porche cubierto acristalado hacia el patio central.

    . Vivienda B (Planta Alta): Acceso por Portal B (fachada principal derecha) mediante escalera recta independiente encerrada en caja de obra. Programa de 3 dormitorios (incluyendo uno de 23 m2 sobre cochera), 2 banos, salon-comedor y cocina equivalentes a la Vivienda A, con un patio trasero elevado privado.

El patio interior central de 40 m2 (5,00 x 8,00 m) garantiza ventilacion cruzada e iluminacion natural en las estancias interiores de ambas plantas, conforme a las directrices de diseno bioclimatico para clima mediterraneo continental.

La estructura se resuelve con muros de carga de 30 cm en fachadas y medianeras, tabiqueria interior de 10 cm, y forjados unidireccionales de 22 cm de canto. La cubierta plana transitable se remata con un parapeto de 30 cm con albardilla metalica de zinc.

Los materiales exteriores propuestos son: estuco blanco mineral en fachadas, carpinteria de aluminio anodizado en tono antracita, persiana enrollable integrada, puerta de entrada de madera maciza de iroko, y puerta de garaje motorizada de chapa de acero galvanizado.

La instalacion electrica, de fontaneria, saneamiento y telecomunicaciones se disenan con trazados apilados verticalmente entre ambas plantas para optimizar recorridos y costes de ejecucion."""

pdf.multi_cell(0, 6, memoria)

# ================================================================ 2. DATOS DEL SOLAR
pdf.add_page()
pdf.set_text_color(30, 35, 45)
pdf.set_font("Helvetica", "B", 24)
pdf.ln(5)
pdf.cell(0, 12, "2. DATOS DEL SOLAR Y NORMATIVA", new_x="LMARGIN", new_y="NEXT")
pdf.ln(5)
pdf.set_draw_color(60, 80, 120)
pdf.line(10, pdf.get_y(), 130, pdf.get_y())
pdf.ln(8)

# Tabla de datos
pdf.set_font("Helvetica", "B", 11)
datos = [
    ("Ubicacion", "Palma del Rio, Cordoba (Andalucia)"),
    ("Tipo de solar", "Entre medianeras con doble fachada"),
    ("Dimensiones del solar", "11,40 m x 17,60 m = 200,00 m2"),
    ("Calle frontal", "C/ Moreno Torroba (fachada sur, Y = 0,00 m)"),
    ("Calle trasera", "Acceso cochera (fachada norte, Y = 17,60 m)"),
    ("Ocupacion maxima permitida", "80% = 160,00 m2 por planta"),
    ("Altura maxima permitida", "Planta Baja + Planta Alta + Cubierta plana"),
    ("Patio interior obligatorio", "5,00 x 8,00 m = 40,00 m2 (20% de parcela)"),
    ("No de viviendas", "2 (bifamiliar: Viv. A en PB, Viv. B en PA)"),
    ("Cota de planta baja", "+0,22 m sobre rasante"),
    ("Altura libre PB", "2,68 m (forjado a +2,90 m)"),
    ("Altura libre PA", "2,70 m (cubierta a +5,80 m)"),
    ("Parapeto de cubierta", "+6,10 m (0,30 m sobre cubierta)"),
]

pdf.set_fill_color(240, 243, 248)
for i, (param, valor) in enumerate(datos):
    fill = i % 2 == 0
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(40, 50, 70)
    pdf.cell(80, 8, param, border=0, fill=fill)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(60, 65, 75)
    pdf.cell(0, 8, valor, border=0, fill=fill, new_x="LMARGIN", new_y="NEXT")

# ================================================================ 3. PROGRAMA FUNCIONAL
pdf.add_page()
pdf.set_text_color(30, 35, 45)
pdf.set_font("Helvetica", "B", 24)
pdf.ln(5)
pdf.cell(0, 12, "3. PROGRAMA FUNCIONAL", new_x="LMARGIN", new_y="NEXT")
pdf.ln(5)
pdf.set_draw_color(60, 80, 120)
pdf.line(10, pdf.get_y(), 110, pdf.get_y())
pdf.ln(8)

# Vivienda A
pdf.set_font("Helvetica", "B", 16)
pdf.set_text_color(50, 60, 80)
pdf.cell(0, 10, "Vivienda A - Planta Baja", new_x="LMARGIN", new_y="NEXT")
pdf.ln(3)

rooms_a = [
    ("Salon-Comedor", "37,0 m2", "X 1,40-6,40 . Y 0,00-7,40"),
    ("Cocina con isla", "20,0 m2", "X 6,40-10,40 . Y 0,00-5,00"),
    ("Porche cubierto acristalado", "13,0 m2", "X 6,40-11,40 . Y 5,00-7,60"),
    ("Dormitorio principal (suite)", "14,0 m2", "X 1,40-6,40 . Y 10,20-13,00"),
    ("Dormitorio 2", "11,2 m2", "X 0,00-3,20 . Y 14,10-17,60"),
    ("Dormitorio 3", "11,2 m2", "X 3,20-6,40 . Y 14,10-17,60"),
    ("Bano completo", "7,0 m2", "X 1,40-6,40 . Y 7,40-8,80"),
    ("Bano suite", "7,0 m2", "X 1,40-6,40 . Y 8,80-10,20"),
    ("Trastero", "7,4 m2", "X 6,40-8,00 . Y 13,00-17,60"),
    ("Cochera", "15,6 m2", "X 8,00-11,40 . Y 13,00-17,60"),
]

pdf.set_font("Helvetica", "B", 9)
pdf.set_fill_color(50, 60, 80)
pdf.set_text_color(255, 255, 255)
pdf.cell(90, 7, "  Estancia", fill=True)
pdf.cell(30, 7, "Superficie", fill=True, align="C")
pdf.cell(0, 7, "  Coordenadas (metros)", fill=True, new_x="LMARGIN", new_y="NEXT")

pdf.set_text_color(40, 45, 55)
for i, (room, area, coords) in enumerate(rooms_a):
    fill = i % 2 == 0
    pdf.set_fill_color(245, 247, 250)
    pdf.set_font("Helvetica", "", 9)
    pdf.cell(90, 7, f"  {room}", fill=fill)
    pdf.set_font("Helvetica", "B", 9)
    pdf.cell(30, 7, area, fill=fill, align="C")
    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(100, 105, 115)
    pdf.cell(0, 7, f"  {coords}", fill=fill, new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(40, 45, 55)

pdf.ln(6)

# Vivienda B
pdf.set_font("Helvetica", "B", 16)
pdf.set_text_color(50, 60, 80)
pdf.cell(0, 10, "Vivienda B - Planta Alta", new_x="LMARGIN", new_y="NEXT")
pdf.ln(3)

rooms_b = [
    ("Salon-Comedor", "37,0 m2", "X 1,40-6,40 . Y 0,00-7,40"),
    ("Cocina con isla", "20,0 m2", "X 6,40-10,40 . Y 0,00-5,00"),
    ("Pasillo sobre porche", "13,0 m2", "X 6,40-11,40 . Y 5,00-7,60"),
    ("Dormitorio principal (suite)", "14,0 m2", "X 1,40-6,40 . Y 10,20-13,00"),
    ("Dormitorio 2 (sobre cochera)", "23,0 m2", "X 6,40-11,40 . Y 13,00-17,60"),
    ("Dormitorio 3", "11,2 m2", "X 3,20-6,40 . Y 14,10-17,60"),
    ("Bano completo", "7,0 m2", "X 1,40-6,40 . Y 7,40-8,80"),
    ("Bano suite", "7,0 m2", "X 1,40-6,40 . Y 8,80-10,20"),
    ("Patio trasero elevado", "11,2 m2", "X 0,00-3,20 . Y 14,10-17,60"),
]

pdf.set_font("Helvetica", "B", 9)
pdf.set_fill_color(50, 60, 80)
pdf.set_text_color(255, 255, 255)
pdf.cell(90, 7, "  Estancia", fill=True)
pdf.cell(30, 7, "Superficie", fill=True, align="C")
pdf.cell(0, 7, "  Coordenadas (metros)", fill=True, new_x="LMARGIN", new_y="NEXT")

pdf.set_text_color(40, 45, 55)
for i, (room, area, coords) in enumerate(rooms_b):
    fill = i % 2 == 0
    pdf.set_fill_color(245, 247, 250)
    pdf.set_font("Helvetica", "", 9)
    pdf.cell(90, 7, f"  {room}", fill=fill)
    pdf.set_font("Helvetica", "B", 9)
    pdf.cell(30, 7, area, fill=fill, align="C")
    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(100, 105, 115)
    pdf.cell(0, 7, f"  {coords}", fill=fill, new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(40, 45, 55)

# ================================================================ 4. CUADRO DE SUPERFICIES
pdf.add_page()
pdf.set_text_color(30, 35, 45)
pdf.set_font("Helvetica", "B", 24)
pdf.ln(5)
pdf.cell(0, 12, "4. CUADRO DE SUPERFICIES", new_x="LMARGIN", new_y="NEXT")
pdf.ln(5)
pdf.set_draw_color(60, 80, 120)
pdf.line(10, pdf.get_y(), 115, pdf.get_y())
pdf.ln(8)

surfaces = [
    ("", "Sup. Util", "Sup. Construida"),
    ("Vivienda A (Planta Baja)", "155,7 m2", "160,0 m2"),
    ("Vivienda B (Planta Alta)", "149,1 m2", "133,0 m2"),
    ("TOTAL VIVIENDAS", "304,8 m2", "293,0 m2"),
    ("", "", ""),
    ("Patio interior (PB)", "40,0 m2", "-"),
    ("Porche cubierto (PB)", "13,0 m2", "-"),
    ("Patio trasero elevado (PA)", "11,2 m2", "-"),
    ("Vacio patio central (PA)", "27,0 m2", "-"),
    ("TOTAL EXTERIORES", "91,2 m2", "-"),
]

for i, (concept, util, const) in enumerate(surfaces):
    is_total = "TOTAL" in concept
    is_header = i == 0
    is_empty = concept == "" and util == ""
    
    if is_empty:
        pdf.ln(3)
        continue
    
    if is_header:
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_fill_color(50, 60, 80)
        pdf.set_text_color(255, 255, 255)
    elif is_total:
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_fill_color(60, 80, 120)
        pdf.set_text_color(255, 255, 255)
    else:
        fill_flag = (i % 2 == 0)
        pdf.set_font("Helvetica", "", 10)
        pdf.set_fill_color(245, 247, 250)
        pdf.set_text_color(40, 45, 55)
    
    pdf.cell(120, 8, f"  {concept}", fill=True)
    pdf.cell(40, 8, util, fill=True, align="C")
    pdf.cell(40, 8, const, fill=True, align="C", new_x="LMARGIN", new_y="NEXT")

# ================================================================ 5. PLANOS TECNICOS
plans = plan_previews()
for title, path in plans:
    pdf.add_page()
    pdf.set_text_color(30, 35, 45)
    pdf.set_font("Helvetica", "B", 18)
    pdf.ln(3)
    pdf.cell(0, 10, title, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)
    
    try:
        img = Image.open(path)
        w, h = img.size
        aspect = w / h
        
        # Fit in landscape A4 (277mm wide x 175mm tall available)
        max_w = 275
        max_h = 170
        
        if aspect > max_w / max_h:
            img_w = max_w
            img_h = max_w / aspect
        else:
            img_h = max_h
            img_w = max_h * aspect
        
        x_offset = (297 - img_w) / 2
        pdf.image(path, x=x_offset, y=pdf.get_y(), w=img_w, h=img_h)
    except Exception as e:
        pdf.set_font("Helvetica", "I", 10)
        pdf.cell(0, 8, f"Error cargando imagen: {e}", new_x="LMARGIN", new_y="NEXT")

# ================================================================ 6. GALERIA DE RENDERS
renders = best_renders()
if renders:
    pdf.add_page()
    pdf.set_text_color(30, 35, 45)
    pdf.set_font("Helvetica", "B", 24)
    pdf.ln(5)
    pdf.cell(0, 12, "6. VISUALIZACION 3D", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(80, 85, 95)
    pdf.cell(0, 8, "Renders arquitectonicos generados con Blender EEVEE . 2560 x 1440 px", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)
    
    for title, path in renders:
        pdf.add_page()
        pdf.set_fill_color(20, 25, 35)
        pdf.rect(0, 0, 297, 210, 'F')
        
        try:
            img = Image.open(path)
            w, h = img.size
            aspect = w / h
            
            # Full bleed landscape
            if aspect > 297/190:
                img_w = 297
                img_h = 297 / aspect
            else:
                img_h = 190
                img_w = 190 * aspect
            
            x_offset = (297 - img_w) / 2
            y_offset = max(5, (195 - img_h) / 2)
            pdf.image(path, x=x_offset, y=y_offset, w=img_w, h=img_h)
        except Exception:
            pass
        
        # Title overlay at bottom
        pdf.set_y(193)
        pdf.set_font("Helvetica", "", 11)
        pdf.set_text_color(200, 205, 215)
        pdf.cell(0, 8, title, align="C")

# ================================================================ 7. PRESUPUESTO
pdf.add_page()
pdf.set_text_color(30, 35, 45)
pdf.set_font("Helvetica", "B", 24)
pdf.ln(5)
pdf.cell(0, 12, "7. PRESUPUESTO ESTIMADO", new_x="LMARGIN", new_y="NEXT")
pdf.ln(5)
pdf.set_draw_color(60, 80, 120)
pdf.line(10, pdf.get_y(), 120, pdf.get_y())
pdf.ln(8)

budget = [
    ("", "Medicion", "Precio unitario", "Importe"),
    ("Demoliciones y movimiento de tierras", "200 m2", "35 EUR/m2", "7.000 EUR"),
    ("Cimentacion y estructura", "293 m2", "280 EUR/m2", "82.040 EUR"),
    ("Cubierta plana e impermeabilizacion", "160 m2", "85 EUR/m2", "13.600 EUR"),
    ("Albanileria y cerramientos", "293 m2", "120 EUR/m2", "35.160 EUR"),
    ("Revestimientos y acabados", "293 m2", "95 EUR/m2", "27.835 EUR"),
    ("Carpinteria exterior (aluminio RPT)", "45 m2", "320 EUR/m2", "14.400 EUR"),
    ("Carpinteria interior (madera)", "28 ud.", "450 EUR/ud.", "12.600 EUR"),
    ("Instalacion electrica y domotica", "2 viv.", "8.500 EUR/viv.", "17.000 EUR"),
    ("Fontaneria y saneamiento", "2 viv.", "6.200 EUR/viv.", "12.400 EUR"),
    ("Climatizacion (A/A splits)", "2 viv.", "4.500 EUR/viv.", "9.000 EUR"),
    ("Pintura y decoracion", "293 m2", "22 EUR/m2", "6.446 EUR"),
    ("Urbanizacion exterior", "-", "-", "8.000 EUR"),
    ("Seguridad y Salud", "-", "-", "5.500 EUR"),
    ("Gestion de residuos", "-", "-", "3.500 EUR"),
    ("Honorarios profesionales", "-", "-", "28.000 EUR"),
    ("Licencias y tasas municipales", "-", "-", "12.000 EUR"),
]

for i, (concept, med, price, total) in enumerate(budget):
    is_header = i == 0
    
    if is_header:
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_fill_color(50, 60, 80)
        pdf.set_text_color(255, 255, 255)
    else:
        fill_flag = (i % 2 == 0)
        pdf.set_font("Helvetica", "", 9)
        pdf.set_fill_color(245, 247, 250) if fill_flag else pdf.set_fill_color(255, 255, 255)
        pdf.set_text_color(40, 45, 55)
    
    pdf.cell(100, 7, f"  {concept}", fill=True)
    pdf.cell(40, 7, med, fill=True, align="C")
    pdf.cell(40, 7, price, fill=True, align="C")
    pdf.set_font("Helvetica", "B" if is_header else "", 9)
    pdf.cell(0, 7, total, fill=True, align="R", new_x="LMARGIN", new_y="NEXT")

pdf.ln(3)
pdf.set_font("Helvetica", "B", 13)
pdf.set_fill_color(40, 55, 90)
pdf.set_text_color(255, 255, 255)
pdf.cell(180, 10, "  PRESUPUESTO TOTAL ESTIMADO (IVA no incluido)", fill=True)
pdf.cell(0, 10, "381.000 EUR  ", fill=True, align="R", new_x="LMARGIN", new_y="NEXT")
pdf.ln(3)
pdf.set_font("Helvetica", "I", 9)
pdf.set_text_color(100, 105, 115)
pdf.cell(0, 6, "* Presupuesto orientativo basado en precios medios de mercado para la zona de Cordoba (2026).", new_x="LMARGIN", new_y="NEXT")
pdf.cell(0, 6, "* Rango estimado: 350.000 EUR - 420.000 EUR segun calidades finales seleccionadas.", new_x="LMARGIN", new_y="NEXT")

# ================================================================ 8. FICHA DE MATERIALES
pdf.add_page()
pdf.set_text_color(30, 35, 45)
pdf.set_font("Helvetica", "B", 24)
pdf.ln(5)
pdf.cell(0, 12, "8. FICHA DE MATERIALES Y ACABADOS", new_x="LMARGIN", new_y="NEXT")
pdf.ln(5)
pdf.set_draw_color(60, 80, 120)
pdf.line(10, pdf.get_y(), 145, pdf.get_y())
pdf.ln(8)

materials = [
    ("FACHADAS", [
        ("Revestimiento", "Estuco mineral blanco, acabado liso, e=15 mm"),
        ("Zocalo", "Piedra natural caliza, pulida, h=40 cm"),
        ("Carpinteria", "Aluminio anodizado antracita, RPT, con rotura de puente termico"),
        ("Vidrio", "Doble acristalamiento bajo emisivo 6+16+6 mm con gas argon"),
        ("Persianas", "Enrollables motorizadas de aluminio inyectado, guia oculta"),
        ("Albardilla cubierta", "Chapa de zinc natural plegado, e=0,8 mm"),
    ]),
    ("SUELOS", [
        ("Interior viviendas", "Gres porcelanico rectificado 60x120 cm, acabado mate"),
        ("Banos", "Gres porcelanico antideslizante 30x60 cm, clase 2"),
        ("Cocina", "Gres porcelanico gran formato 120x120 cm"),
        ("Porche cubierto", "Tarima de madera de IPE tratada para exterior"),
        ("Patio central", "Adoquin de piedra natural irregular"),
        ("Cochera", "Hormigon pulido con tratamiento antipolvo"),
    ]),
    ("COCINA", [
        ("Mobiliario", "Lacado blanco mate, tiradores integrados tipo gola"),
        ("Encimera", "Marmol blanco Carrara, e=20 mm, canto biselado"),
        ("Electrodomesticos", "Gama media-alta empotrados, clase energetica A+++"),
        ("Fregadero", "Acero inoxidable AISI 304, 1 cubeta + escurridor"),
    ]),
    ("BANOS", [
        ("Revestimiento", "Gres porcelanico rectificado 30x90 cm, acabado satinado"),
        ("Sanitarios", "Porcelana vitrificada, inodoro suspendido con cisterna empotrada"),
        ("Griferia", "Monomando cromado, serie contemporanea"),
        ("Ducha", "Plato extraplano de resina mineral, mampara fija de vidrio 8 mm"),
    ]),
    ("INSTALACIONES", [
        ("Electricidad", "Grado de electrificacion elevado, mecanismos serie Simon 270"),
        ("Climatizacion", "Splits inverter multi-split, clase A++"),
        ("ACS", "Bomba de calor aerotermica, deposito 150 L"),
        ("Domotica", "Preinstalacion para control de persianas, iluminacion y climatizacion"),
    ]),
]

for section_title, items in materials:
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(50, 60, 80)
    pdf.cell(0, 9, section_title, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(1)
    
    for element, description in items:
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(60, 70, 90)
        pdf.cell(55, 6, f"  {element}")
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(70, 75, 85)
        pdf.cell(0, 6, description, new_x="LMARGIN", new_y="NEXT")
    
    pdf.ln(4)

# ================================================================ CONTRAPORTADA
pdf.add_page()
pdf.set_fill_color(25, 30, 40)
pdf.rect(0, 0, 297, 210, 'F')

pdf.set_y(75)
pdf.set_font("Helvetica", "B", 28)
pdf.set_text_color(255, 255, 255)
pdf.cell(0, 15, "VIVIENDA BIFAMILIAR", align="C", new_x="LMARGIN", new_y="NEXT")
pdf.set_font("Helvetica", "", 16)
pdf.set_text_color(180, 185, 195)
pdf.cell(0, 10, "Palma del Rio . Cordoba", align="C", new_x="LMARGIN", new_y="NEXT")

pdf.ln(15)
pdf.set_font("Helvetica", "", 11)
pdf.set_text_color(140, 145, 155)
pdf.cell(0, 8, "Proyecto Basico y de Ejecucion", align="C", new_x="LMARGIN", new_y="NEXT")
pdf.cell(0, 8, "Agosto 2026", align="C", new_x="LMARGIN", new_y="NEXT")
pdf.ln(10)
pdf.set_draw_color(80, 90, 110)
pdf.line(110, pdf.get_y(), 187, pdf.get_y())
pdf.ln(10)
pdf.set_font("Helvetica", "I", 10)
pdf.set_text_color(120, 125, 135)
pdf.cell(0, 7, "Superficie total construida: 293,0 m2", align="C", new_x="LMARGIN", new_y="NEXT")
pdf.cell(0, 7, "Presupuesto estimado: 381.000 EUR", align="C", new_x="LMARGIN", new_y="NEXT")

# ================================================================ GUARDAR
output_path = os.path.join(OUT, "dossier-proyecto-bifamiliar.pdf")
pdf.output(output_path)
print(f"Dossier generado: {output_path}")
print(f"Total paginas: {pdf.page_no()}")
