# -*- coding: utf-8 -*-
# ==============================================================================
# LAYOUT PROFESIONAL TERMINADO - PROYECTO RESIDENCIAL BIFAMILIAR
# ==============================================================================
# Genera documento .layout A3 apaisado con 4 laminas completas:
# 1. Planta Baja Acotada (imagen PNG con cotas)
# 2. Planta Baja Editable (viewport SketchUp vinculado)
# 3. Perspectiva 3D Sur-Este
# 4. Vista Patio y Piscina
# Cada lamina tiene cajetin profesional completo.
# ==============================================================================

skp_path = "C:/Users/Oscar Martinez/Desktop/mi-casa/casa-bifamiliar-3d.skp"
png_path = "C:/Users/Oscar Martinez/Desktop/mi-casa/entrega/planos_2d/01_plano_2d_planta_baja.png"
layout_dir = "C:/Users/Oscar Martinez/Desktop/mi-casa/entrega/planos"
Dir.mkdir(layout_dir) unless Dir.exist?(layout_dir)
layout_path = "#{layout_dir}/casa-bifamiliar-COMPLETO.layout"

# ─── A3 Apaisado ───
PW = 16.535   # 420mm
PH = 11.693   # 297mm

doc = Layout::Document.new
info = doc.page_info
info.width  = PW
info.height = PH
info.left_margin   = 0.394  # 10mm
info.right_margin  = 0.394
info.top_margin    = 0.394
info.bottom_margin = 0.394

# ─── Capas ───
layer_frame  = doc.layers.first  # On Every Interior Page (default)
layer_frame.name = "Cajetin"

layer_vp     = doc.layers.add("Viewport")
layer_labels = doc.layers.add("Rotulos")

# ─── Colores ───
C_BLACK  = Sketchup::Color.new(28, 30, 33)
C_GRAY   = Sketchup::Color.new(107, 114, 128)
C_WHITE  = Sketchup::Color.new(255, 255, 255)
C_RED    = Sketchup::Color.new(185, 28, 28)
C_BLUE   = Sketchup::Color.new(15, 76, 129)
C_BG     = Sketchup::Color.new(250, 250, 252)

# ─── Helper: texto con estilo ───
def add_styled_text(doc, layer, page, x, y, w, h, text, size, bold, color, align=nil)
  bounds = Geom::Bounds2d.new(x, y, w, h)
  ft = Layout::FormattedText.new(text, bounds)
  doc.add_entity(ft, layer, page)
  len = ft.plain_text.length
  if len > 0
    style = ft.style(0, 1)
    style.font_size = size
    style.text_bold = bold
    style.font_family = "Arial"
    style.text_color = color
    if align
      style.text_alignment = align
    end
    ft.apply_style(style, 0, len)
  end
  ft
end

# ─── Helper: rectangulo con estilo ───
def add_styled_rect(doc, layer, page, x, y, w, h, stroke_w, stroke_c, fill=nil)
  bounds = Geom::Bounds2d.new(x, y, w, h)
  rect = Layout::Rectangle.new(bounds)
  doc.add_entity(rect, layer, page)
  rs = rect.style
  rs.stroked = true
  rs.stroke_width = stroke_w
  rs.stroke_color = stroke_c
  if fill
    rs.solid_filled = true
    rs.fill_color = fill
  else
    rs.solid_filled = false
  end
  rect.style = rs
  rect
end

# ─── Helper: cajetin profesional en cada lamina ───
def add_cajetin(doc, layer, layer_labels, page, num_lamina, titulo, subtitulo, escala_texto, c_black, c_gray, c_white, c_blue)
  pw = 16.535
  ph = 11.693

  # Marco exterior grueso
  add_styled_rect(doc, layer, page, 0.197, 0.197, pw - 0.394, ph - 0.394, 2.5, c_black)

  # Franja inferior del cajetin (fondo blanco)
  caj_y = ph - 1.35   # 10.343
  caj_h = 0.95
  add_styled_rect(doc, layer, page, 0.197, caj_y, pw - 0.394, caj_h, 1.5, c_black, c_white)

  # Linea separadora vertical en cajetin
  sep_x = pw - 5.5
  add_styled_rect(doc, layer, page, sep_x, caj_y, 0.01, caj_h, 1.0, c_black)

  # Textos cajetin izquierda
  add_styled_text(doc, layer_labels, page, 0.4, caj_y + 0.08, 10.0, 0.35, titulo, 14, true, c_black)
  add_styled_text(doc, layer_labels, page, 0.4, caj_y + 0.45, 10.0, 0.25, subtitulo, 9, false, c_gray)
  add_styled_text(doc, layer_labels, page, 0.4, caj_y + 0.70, 6.0, 0.20, escala_texto, 8, false, c_gray)

  # Textos cajetin derecha (datos proyecto)
  rx = sep_x + 0.2
  add_styled_text(doc, layer_labels, page, rx, caj_y + 0.05, 5.0, 0.25, "PROYECTO RESIDENCIAL BIFAMILIAR", 10, true, c_black)
  add_styled_text(doc, layer_labels, page, rx, caj_y + 0.32, 5.0, 0.20, "Palma del Rio, Cordoba", 8, false, c_gray)
  add_styled_text(doc, layer_labels, page, rx, caj_y + 0.55, 5.0, 0.20, "Sup. Util: 136,7 m2 | Exterior: 37,8 m2", 8, false, c_blue)
  add_styled_text(doc, layer_labels, page, rx, caj_y + 0.75, 5.0, 0.18, "Lamina #{num_lamina}", 7, true, c_gray)
end

# ======================================================================
# LAMINA 1: PLANTA BAJA ACOTADA (Imagen PNG con cotas integradas)
# ======================================================================
page1 = doc.pages.first

# Insertar plano PNG (ya tiene cotas, rotulos, mobiliario, colores)
if File.exist?(png_path)
  # Area de dibujo: margen + espacio para cajetin
  img_x = 0.6
  img_y = 0.4
  img_w = 15.3
  img_h = 9.4
  img_bounds = Geom::Bounds2d.new(img_x, img_y, img_w, img_h)
  img = Layout::Image.new(png_path, img_bounds)
  doc.add_entity(img, layer_vp, page1)
end

add_cajetin(doc, layer_frame, layer_labels, page1,
  "A-02", "PLANTA BAJA AMUEBLADA Y ACOTADA",
  "Con cotas interiores utiles, superficies por estancia y mobiliario",
  "Escala grafica 1:50 en A3 (420x297mm)", C_BLACK, C_GRAY, C_WHITE, C_BLUE)

# ======================================================================
# LAMINA 2: PLANTA BAJA EDITABLE (Viewport SketchUp vinculado)
# ======================================================================
page2 = doc.pages.add("Planta Baja Editable")

vp2_bounds = Geom::Bounds2d.new(1.5, 0.5, 13.5, 9.3)
skp2 = Layout::SketchUpModel.new(skp_path, vp2_bounds)
doc.add_entity(skp2, layer_vp, page2)
skp2.current_scene = 0  # PB_PLANTA_2D
skp2.render_mode = Layout::SketchUpModel::HYBRID_RENDER
skp2.preserve_scale_on_resize = true

# Rotulos de estancias sobre el viewport
# (posiciones aprox. mapeadas al viewport)
rooms = [
  [4.8, 3.8, "SALON-COMEDOR", "38,5 m2"],
  [9.2, 3.0, "COCINA", "18,7 m2"],
  [9.5, 5.3, "PORCHE", "11,4 m2"],
  [3.7, 6.5, "BANO COMUN", "5,7 m2"],
  [5.9, 6.5, "BANO SUITE", "5,6 m2"],
  [4.0, 8.2, "MASTER SUITE", "20,4 m2"],
  [2.7, 9.5, "DORM. 2", "11,7 m2"],
  [5.3, 9.5, "DORM. 3", "11,9 m2"],
  [9.8, 9.0, "COCHERA", "21,1 m2"],
  [9.5, 7.2, "PISCINA", "2,5x3,8m"],
]

rooms.each do |rx, ry, name, area|
  add_styled_text(doc, layer_labels, page2, rx, ry, 2.2, 0.22, name, 7, true, C_BLACK)
  add_styled_text(doc, layer_labels, page2, rx, ry + 0.20, 2.2, 0.18, area, 6, false, C_BLUE)
end

add_cajetin(doc, layer_frame, layer_labels, page2,
  "A-02b", "PLANTA BAJA EDITABLE (Vinculada a SketchUp)",
  "Viewport dinamico - Actualizar: clic derecho > Actualizar referencia del modelo",
  "Escala aprox. 1:50 en A3 | Proyeccion ortografica cenital", C_BLACK, C_GRAY, C_WHITE, C_BLUE)

# ======================================================================
# LAMINA 3: PERSPECTIVA 3D SUR-ESTE
# ======================================================================
page3 = doc.pages.add("Perspectiva 3D")

vp3_bounds = Geom::Bounds2d.new(0.6, 0.4, 15.3, 9.4)
skp3 = Layout::SketchUpModel.new(skp_path, vp3_bounds)
doc.add_entity(skp3, layer_vp, page3)
skp3.current_scene = 1  # PB_PERSPECTIVA_3D
skp3.render_mode = Layout::SketchUpModel::HYBRID_RENDER

add_cajetin(doc, layer_frame, layer_labels, page3,
  "A-05", "PERSPECTIVA 3D - VISTA SUR-ESTE",
  "Vista general desde la calle Moreno Torroba (fachada sur)",
  "Sin escala | Perspectiva conica FOV 45", C_BLACK, C_GRAY, C_WHITE, C_BLUE)

# ======================================================================
# LAMINA 4: VISTA PATIO / PISCINA
# ======================================================================
page4 = doc.pages.add("Vista Patio")

vp4_bounds = Geom::Bounds2d.new(0.6, 0.4, 15.3, 9.4)
skp4 = Layout::SketchUpModel.new(skp_path, vp4_bounds)
doc.add_entity(skp4, layer_vp, page4)
skp4.current_scene = 2  # PB_VISTA_PATIO
skp4.render_mode = Layout::SketchUpModel::HYBRID_RENDER

add_cajetin(doc, layer_frame, layer_labels, page4,
  "A-06", "VISTA PATIO Y PISCINA - NOR-OESTE",
  "Vista desde el patio trasero con piscina privada (2,50 x 3,80 m)",
  "Sin escala | Perspectiva conica FOV 40", C_BLACK, C_GRAY, C_WHITE, C_BLUE)

# ======================================================================
# LAMINA 5: CUADRO DE SUPERFICIES
# ======================================================================
page5 = doc.pages.add("Cuadro de Superficies")

# Marco
add_styled_rect(doc, layer_frame, page5, 0.197, 0.197, PW - 0.394, PH - 0.394, 2.5, C_BLACK)

# Titulo de la lamina
add_styled_text(doc, layer_labels, page5, 0.6, 0.5, 15.0, 0.5,
  "CUADRO DE SUPERFICIES UTILES - PLANTA BAJA (VIVIENDA A)", 18, true, C_BLACK)

add_styled_text(doc, layer_labels, page5, 0.6, 1.05, 15.0, 0.3,
  "Medidas interiores libres de tabique a tabique terminado", 10, false, C_GRAY)

# Tabla de superficies como texto formateado (Layout::Table requiere args especificos)
# Usamos texto tabulado con posiciones fijas
col_x = [0.8, 5.5, 9.5, 12.5]
header_y = 1.6

# Cabeceras
add_styled_text(doc, layer_labels, page5, col_x[0], header_y, 4.5, 0.3, "ESTANCIA", 11, true, C_WHITE)
add_styled_text(doc, layer_labels, page5, col_x[1], header_y, 3.5, 0.3, "MEDIDAS LIBRES", 11, true, C_WHITE)
add_styled_text(doc, layer_labels, page5, col_x[2], header_y, 2.5, 0.3, "SUP. UTIL", 11, true, C_WHITE)
add_styled_text(doc, layer_labels, page5, col_x[3], header_y, 3.5, 0.3, "OBSERVACIONES", 11, true, C_WHITE)

# Fondo cabecera
add_styled_rect(doc, layer_frame, page5, 0.6, header_y - 0.05, 15.3, 0.38, 1.0, C_BLACK, C_BLACK)

# Filas de datos
data = [
  ["Salon - Comedor",        "6,20 x 7,20 m",  "38,5 m2",  "Frente armarios 3,60 m"],
  ["Cocina con Isla",        "3,90 x 4,80 m",  "18,7 m2",  "Isla central 2,40 m"],
  ["Master Suite completa",  "3,00x2,60 + 1,95x3,60", "20,4 m2", "Vestidor 3,20 m + Bano"],
  ["Bano en Suite",          "2,42 x 2,30 m",  "5,6 m2",   "Ducha 2,35 m + 2 ventanas"],
  ["Bano Comun",             "2,47 x 2,30 m",  "5,7 m2",   "Ducha 2,35 m"],
  ["Dormitorio 2",           "3,00 x 3,90 m",  "11,7 m2",  "Armario empotrado 2,20 m"],
  ["Dormitorio 3",           "3,05 x 3,90 m",  "11,9 m2",  "Armario empotrado 2,20 m"],
  ["Pasillo Noche",          "1,20 m ancho",    "7,3 m2",   "Distribuidor independiente"],
  ["Gran Cochera",           "4,75 x 4,45 m",  "21,1 m2",  "Trastero + Lavadero"],
  ["Porche Cubierto",        "4,75 x 2,40 m",  "11,4 m2",  "Exterior protegido"],
  ["Patio + Piscina",        "4,75 x 5,55 m",  "26,4 m2",  "Piscina 2,50x3,80 m"],
]

row_h = 0.42
data.each_with_index do |row, i|
  ry = header_y + 0.45 + (i * row_h)

  # Fondo alterno
  if i.even?
    add_styled_rect(doc, layer_frame, page5, 0.6, ry - 0.05, 15.3, row_h, 0.3, C_GRAY, C_BG)
  end

  add_styled_text(doc, layer_labels, page5, col_x[0], ry, 4.5, 0.3, row[0], 10, true, C_BLACK)
  add_styled_text(doc, layer_labels, page5, col_x[1], ry, 3.5, 0.3, row[1], 10, false, C_BLACK)
  add_styled_text(doc, layer_labels, page5, col_x[2], ry, 2.5, 0.3, row[2], 10, true, C_BLUE)
  add_styled_text(doc, layer_labels, page5, col_x[3], ry, 3.5, 0.3, row[3], 9, false, C_GRAY)
end

# Totales
total_y = header_y + 0.45 + (data.length * row_h) + 0.15
add_styled_rect(doc, layer_frame, page5, 0.6, total_y - 0.05, 15.3, 0.45, 1.5, C_BLACK)
add_styled_text(doc, layer_labels, page5, col_x[0], total_y, 4.5, 0.35, "TOTAL INTERIOR CERRADO", 12, true, C_BLACK)
add_styled_text(doc, layer_labels, page5, col_x[2], total_y, 2.5, 0.35, "136,7 m2", 12, true, C_RED)

total_y2 = total_y + 0.50
add_styled_rect(doc, layer_frame, page5, 0.6, total_y2 - 0.05, 15.3, 0.45, 1.5, C_BLACK)
add_styled_text(doc, layer_labels, page5, col_x[0], total_y2, 4.5, 0.35, "TOTAL EXTERIOR (Porche+Patio)", 12, true, C_BLACK)
add_styled_text(doc, layer_labels, page5, col_x[2], total_y2, 2.5, 0.35, "37,8 m2", 12, true, C_RED)

total_y3 = total_y2 + 0.55
add_styled_text(doc, layer_labels, page5, col_x[0], total_y3, 10.0, 0.35,
  "SUPERFICIE CONSTRUIDA TOTAL EN PLANTA BAJA: 196,8 m2", 14, true, C_BLACK)

# Cajetin lamina 5
caj5_y = PH - 1.35
add_styled_rect(doc, layer_frame, page5, 0.197, caj5_y, PW - 0.394, 0.95, 1.5, C_BLACK, C_WHITE)
add_styled_text(doc, layer_labels, page5, 0.4, caj5_y + 0.10, 10.0, 0.35,
  "A-07  CUADRO DE SUPERFICIES UTILES", 14, true, C_BLACK)
add_styled_text(doc, layer_labels, page5, 0.4, caj5_y + 0.55, 10.0, 0.25,
  "Medidas interiores netas de tabique a tabique | Norma CTE", 9, false, C_GRAY)
add_styled_text(doc, layer_labels, page5, PW - 5.5, caj5_y + 0.10, 5.0, 0.25,
  "PROYECTO RESIDENCIAL BIFAMILIAR", 10, true, C_BLACK)
add_styled_text(doc, layer_labels, page5, PW - 5.5, caj5_y + 0.40, 5.0, 0.20,
  "Palma del Rio, Cordoba", 8, false, C_GRAY)

# ======================================================================
# GUARDAR
# ======================================================================
doc.save(layout_path)

"LAYOUT TERMINADO: #{doc.pages.count} laminas A3 profesionales en #{layout_path}"
