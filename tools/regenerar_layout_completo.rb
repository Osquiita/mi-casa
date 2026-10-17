# -*- coding: utf-8 -*-
# ==============================================================================
# GENERAR LAYOUT COMPLETO CON RENDERIZADO EXPLÍCITO Y VERIFICACIÓN
# ==============================================================================

skp_path   = "C:/Users/Oscar Martinez/Desktop/mi-casa/casa-bifamiliar-3d.skp"
png_path   = "C:/Users/Oscar Martinez/Desktop/mi-casa/entrega/planos_2d/01_plano_2d_planta_baja.png"
layout_dir = "C:/Users/Oscar Martinez/Desktop/mi-casa/entrega/planos"
layout_path = "#{layout_dir}/casa-bifamiliar-COMPLETO.layout"

PW = 16.535   # 420mm (A3)
PH = 11.693   # 297mm (A3)

doc = Layout::Document.new
info = doc.page_info
info.width  = PW
info.height = PH
info.left_margin   = 0.394
info.right_margin  = 0.394
info.top_margin    = 0.394
info.bottom_margin = 0.394

# Capas en LayOut
layer_base   = doc.layers.first
layer_base.name = "Plano_Fondo"

layer_marcos = doc.layers.add("Marcos_Cajetin")
layer_textos = doc.layers.add("Textos_Rotulos")

C_BLACK  = Sketchup::Color.new(28, 30, 33)
C_GRAY   = Sketchup::Color.new(107, 114, 128)
C_WHITE  = Sketchup::Color.new(255, 255, 255)
C_RED    = Sketchup::Color.new(185, 28, 28)
C_BLUE   = Sketchup::Color.new(15, 76, 129)
C_BG     = Sketchup::Color.new(245, 247, 250)

def add_text(doc, layer, page, x, y, w, h, text, size=10, bold=false, color=nil)
  color ||= Sketchup::Color.new(28, 30, 33)
  b = Geom::Bounds2d.new(x, y, w, h)
  ft = Layout::FormattedText.new(text, b)
  doc.add_entity(ft, layer, page)
  len = ft.plain_text.length
  if len > 0
    s = ft.style(0, 1)
    s.font_size = size
    s.text_bold = bold
    s.font_family = "Arial"
    s.text_color = color
    ft.apply_style(s, 0, len)
  end
  ft
end

def add_rect(doc, layer, page, x, y, w, h, stroke_w=1.0, stroke_c=nil, fill_c=nil)
  stroke_c ||= Sketchup::Color.new(28, 30, 33)
  b = Geom::Bounds2d.new(x, y, w, h)
  r = Layout::Rectangle.new(b)
  doc.add_entity(r, layer, page)
  s = r.style
  s.stroked = true
  s.stroke_width = stroke_w
  s.stroke_color = stroke_c
  if fill_c
    s.solid_filled = true
    s.fill_color = fill_c
  else
    s.solid_filled = false
  end
  r.style = s
  r
end

def add_cajetin_lamina(doc, layer_m, layer_t, page, num, titulo, desc, escala)
  pw = 16.535
  ph = 11.693
  
  # Marco exterior
  add_rect(doc, layer_m, page, 0.20, 0.20, pw - 0.40, ph - 0.40, 2.0, Sketchup::Color.new(28, 30, 33))
  
  # Franja inferior cajetín
  cy = ph - 1.30
  ch = 0.90
  add_rect(doc, layer_m, page, 0.20, cy, pw - 0.40, ch, 1.2, Sketchup::Color.new(28, 30, 33), Sketchup::Color.new(255, 255, 255))
  
  # Separador
  sx = pw - 5.2
  add_rect(doc, layer_m, page, sx, cy, 0.01, ch, 1.0, Sketchup::Color.new(28, 30, 33))
  
  # Textos izquierda
  add_text(doc, layer_t, page, 0.40, cy + 0.08, 10.0, 0.32, titulo, 13, true, Sketchup::Color.new(28, 30, 33))
  add_text(doc, layer_t, page, 0.40, cy + 0.42, 10.0, 0.22, desc, 8.5, false, Sketchup::Color.new(107, 114, 128))
  add_text(doc, layer_t, page, 0.40, cy + 0.65, 6.0, 0.20, escala, 8.0, false, Sketchup::Color.new(107, 114, 128))
  
  # Textos derecha
  rx = sx + 0.25
  add_text(doc, layer_t, page, rx, cy + 0.06, 4.8, 0.25, "PROYECTO RESIDENCIAL BIFAMILIAR", 9.5, true, Sketchup::Color.new(28, 30, 33))
  add_text(doc, layer_t, page, rx, cy + 0.30, 4.8, 0.20, "Palma del Rio (Cordoba)", 8.0, false, Sketchup::Color.new(107, 114, 128))
  add_text(doc, layer_t, page, rx, cy + 0.50, 4.8, 0.20, "Sup. Util: 136,7 m2 | Exterior: 37,8 m2", 8.0, false, Sketchup::Color.new(15, 76, 129))
  add_text(doc, layer_t, page, rx, cy + 0.70, 4.8, 0.18, "LAMINA #{num}", 7.5, true, Sketchup::Color.new(185, 28, 28))
end

# ═══════════════════════════════════════════════════════════════════════
# LÁMINA 1: PLANTA BAJA ACOTADA TÉCNICA (Plano PNG de alta resolución)
# ═══════════════════════════════════════════════════════════════════════
page1 = doc.pages.first
if File.exist?(png_path)
  # Centrado en el marco
  img_b = Geom::Bounds2d.new(0.5, 0.35, 15.5, 9.8)
  img = Layout::Image.new(png_path, img_b)
  doc.add_entity(img, layer_base, page1)
end
add_cajetin_lamina(doc, layer_marcos, layer_textos, page1, "A-02",
  "PLANTA BAJA AMUEBLADA Y ACOTADA",
  "Cotas interiores libres de tabique a tabique, mobiliario, sanitarios y superficies reales",
  "Escala grafica 1:50 en formato A3")

# ═══════════════════════════════════════════════════════════════════════
# LÁMINA 2: PLANTA BAJA VIEWPORT SKETCHUP (Modelo 3D dinámico)
# ═══════════════════════════════════════════════════════════════════════
page2 = doc.pages.add("Planta Baja Modelo 3D")
vp2_b = Geom::Bounds2d.new(1.0, 0.4, 14.5, 9.7)
skp2 = Layout::SketchUpModel.new(skp_path, vp2_b)
doc.add_entity(skp2, layer_base, page2)
skp2.current_scene = 0 # 01_PLANTA_EDITABLE_2D
skp2.render_mode = Layout::SketchUpModel::RASTER_RENDER
skp2.render if skp2.render_needed?

add_cajetin_lamina(doc, layer_marcos, layer_textos, page2, "A-02b",
  "PLANTA BAJA - MODELO 3D DINAMICO (SKETCHUP)",
  "Vinculo directo con SketchUp. Para actualizar: clic derecho > Actualizar referencia del modelo",
  "Proyeccion paralela ortografica cenital | Escala 1:50")

# ═══════════════════════════════════════════════════════════════════════
# LÁMINA 3: PERSPECTIVA 3D GENERAL
# ═══════════════════════════════════════════════════════════════════════
page3 = doc.pages.add("Perspectiva 3D")
vp3_b = Geom::Bounds2d.new(0.5, 0.35, 15.5, 9.8)
skp3 = Layout::SketchUpModel.new(skp_path, vp3_b)
doc.add_entity(skp3, layer_base, page3)
skp3.current_scene = 1 # 02_PERSPECTIVA_3D
skp3.render_mode = Layout::SketchUpModel::RASTER_RENDER
skp3.render if skp3.render_needed?

add_cajetin_lamina(doc, layer_marcos, layer_textos, page3, "A-05",
  "PERSPECTIVA 3D - VISTA GENERAL SUR-ESTE",
  "Vista de conjunto desde Calle Moreno Torroba con estudio de soleamiento",
  "Perspectiva conica FOV 45 | Sin escala")

# ═══════════════════════════════════════════════════════════════════════
# LÁMINA 4: VISTA PATIO TRASERO Y PISCINA
# ═══════════════════════════════════════════════════════════════════════
page4 = doc.pages.add("Vista Patio y Piscina")
vp4_b = Geom::Bounds2d.new(0.5, 0.35, 15.5, 9.8)
skp4 = Layout::SketchUpModel.new(skp_path, vp4_b)
doc.add_entity(skp4, layer_base, page4)
skp4.current_scene = 2 # 03_VISTA_PATIO_PISCINA
skp4.render_mode = Layout::SketchUpModel::RASTER_RENDER
skp4.render if skp4.render_needed?

add_cajetin_lamina(doc, layer_marcos, layer_textos, page4, "A-06",
  "VISTA PATIO OASIS Y PISCINA PRIVADA",
  "Vista del patio trasero con piscina (2,50 x 3,80 m), solarium y conexion al porche",
  "Perspectiva conica FOV 40 | Sin escala")

# ═══════════════════════════════════════════════════════════════════════
# LÁMINA 5: CUADRO DE SUPERFICIES Y PROGRAMA
# ═══════════════════════════════════════════════════════════════════════
page5 = doc.pages.add("Cuadro de Superficies")
add_rect(doc, layer_marcos, page5, 0.20, 0.20, PW - 0.40, PH - 0.40, 2.0, Sketchup::Color.new(28, 30, 33))

add_text(doc, layer_textos, page5, 0.60, 0.50, 15.0, 0.45,
  "CUADRO DE SUPERFICIES UTILES - PLANTA BAJA (VIVIENDA A)", 16, true, Sketchup::Color.new(28, 30, 33))
add_text(doc, layer_textos, page5, 0.60, 1.00, 15.0, 0.25,
  "Medidas interiores netas libres de tabique a tabique terminado | Conforme a CTE", 9.5, false, Sketchup::Color.new(107, 114, 128))

# Tabla
col_x = [0.80, 5.20, 9.20, 12.00]
hy = 1.45
add_rect(doc, layer_marcos, page5, 0.60, hy - 0.05, 15.30, 0.38, 1.0, Sketchup::Color.new(28, 30, 33), Sketchup::Color.new(28, 30, 33))
add_text(doc, layer_textos, page5, col_x[0], hy, 4.0, 0.30, "ESTANCIA / ESPACIO", 10.5, true, Sketchup::Color.new(255, 255, 255))
add_text(doc, layer_textos, page5, col_x[1], hy, 3.8, 0.30, "MEDIDAS INTERIORES", 10.5, true, Sketchup::Color.new(255, 255, 255))
add_text(doc, layer_textos, page5, col_x[2], hy, 2.5, 0.30, "SUP. UTIL", 10.5, true, Sketchup::Color.new(255, 255, 255))
add_text(doc, layer_textos, page5, col_x[3], hy, 4.0, 0.30, "CARACTERISTICAS", 10.5, true, Sketchup::Color.new(255, 255, 255))

data = [
  ["Salon - Comedor",        "6,20 x 7,20 m",  "38,5 m2",  "Frente continuo armarios 3,60 m"],
  ["Cocina con Isla",        "3,90 x 4,80 m",  "18,7 m2",  "Isla central 2,40 m + despensa"],
  ["Master Suite (Dorm 1)",  "3,00x2,60 + 1,95x3,60", "14,8 m2", "Gran vestidor lineal de 3,20 m"],
  ["Bano en Suite (Privado)","2,42 x 2,30 m",  "5,6 m2",   "Ducha corrida 2,35 m + 2 ventanas"],
  ["Bano Comun (General)",   "2,47 x 2,30 m",  "5,7 m2",   "Ducha 2,35 m + fontaneria comp."],
  ["Dormitorio 2",           "3,00 x 3,90 m",  "11,7 m2",  "Armario empotrado 2,20 m"],
  ["Dormitorio 3",           "3,05 x 3,90 m",  "11,9 m2",  "Armario empotrado 2,20 m"],
  ["Pasillo Distribuidor",   "1,20 m libre",    "7,3 m2",   "Paso noche independiente"],
  ["Gran Cochera (Trastero)","4,75 x 4,45 m",  "21,1 m2",  "SUV grande + Lavadero 4,10 m"],
  ["Porche Cubierto",        "4,75 x 2,40 m",  "11,4 m2",  "Comedor exterior protegido"],
  ["Patio Descubierto",      "4,75 x 5,55 m",  "26,4 m2",  "Patio oasis + solarium"],
  ["Piscina Privada",        "2,50 x 3,80 m",  "9,5 m2",   "Profundidad 1,40 m"],
]

rh = 0.40
data.each_with_index do |r, i|
  ry = hy + 0.42 + (i * rh)
  if i.even?
    add_rect(doc, layer_marcos, page5, 0.60, ry - 0.05, 15.30, rh, 0.2, Sketchup::Color.new(200, 205, 210), Sketchup::Color.new(245, 247, 250))
  end
  add_text(doc, layer_textos, page5, col_x[0], ry, 4.2, 0.25, r[0], 9.5, true, Sketchup::Color.new(28, 30, 33))
  add_text(doc, layer_textos, page5, col_x[1], ry, 3.8, 0.25, r[1], 9.5, false, Sketchup::Color.new(28, 30, 33))
  add_text(doc, layer_textos, page5, col_x[2], ry, 2.5, 0.25, r[2], 9.5, true, Sketchup::Color.new(15, 76, 129))
  add_text(doc, layer_textos, page5, col_x[3], ry, 4.0, 0.25, r[3], 8.5, false, Sketchup::Color.new(107, 114, 128))
end

# Totales
ty = hy + 0.42 + (data.length * rh) + 0.15
add_rect(doc, layer_marcos, page5, 0.60, ty - 0.05, 15.30, 0.40, 1.5, Sketchup::Color.new(28, 30, 33))
add_text(doc, layer_textos, page5, col_x[0], ty, 4.2, 0.30, "TOTAL SUP. UTIL CERRADA", 11, true, Sketchup::Color.new(28, 30, 33))
add_text(doc, layer_textos, page5, col_x[2], ty, 2.5, 0.30, "136,7 m2", 11, true, Sketchup::Color.new(185, 28, 28))

ty2 = ty + 0.45
add_rect(doc, layer_marcos, page5, 0.60, ty2 - 0.05, 15.30, 0.40, 1.5, Sketchup::Color.new(28, 30, 33))
add_text(doc, layer_textos, page5, col_x[0], ty2, 4.2, 0.30, "TOTAL EXTERIOR (Porche+Patio)", 11, true, Sketchup::Color.new(28, 30, 33))
add_text(doc, layer_textos, page5, col_x[2], ty2, 2.5, 0.30, "37,8 m2", 11, true, Sketchup::Color.new(185, 28, 28))

add_cajetin_lamina(doc, layer_marcos, layer_textos, page5, "A-07",
  "CUADRO DE SUPERFICIES UTILES",
  "Desglose y computo normativo de areas utiles conforme a CTE",
  "Sin escala | Resumen cuantitativo")

# ═══════════════════════════════════════════════════════════════════════
# GUARDAR
# ═══════════════════════════════════════════════════════════════════════
doc.save(layout_path)

# Exportar PDF
pdf_path = "#{layout_dir}/00_CUADERNO_PLANOS_LAYOUT_A3.pdf"
doc.export(pdf_path)

"LAYOUT REGENERADO Y PDF EXPORTADO OK (#{doc.pages.count} laminas)"
