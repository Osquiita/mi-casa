# -*- coding: utf-8 -*-
# ==============================================================================
# RECONSTRUCCIÓN FINAL DE LAYOUT CON PLANO ARQUITECTÓNICO PROFESIONAL
# ==============================================================================

plan_arch_png = "C:/Users/Oscar Martinez/Desktop/mi-casa/entrega/planos_2d/01_plano_arquitecto_planta_baja.png"
skp_path      = "C:/Users/Oscar Martinez/Desktop/mi-casa/casa-bifamiliar-3d.skp"
layout_path   = "C:/Users/Oscar Martinez/Desktop/mi-casa/entrega/planos/casa-bifamiliar-COMPLETO.layout"
desktop_path  = "C:/Users/Oscar Martinez/Desktop/00_PROYECTO_CASA_LAYOUT.layout"

PW = 16.535   # A3 = 420 mm
PH = 11.693   # A3 = 297 mm

doc = Layout::Document.new
info = doc.page_info
info.width  = PW
info.height = PH
info.left_margin   = 0.20
info.right_margin  = 0.20
info.top_margin    = 0.20
info.bottom_margin = 0.20

layer_base = doc.layers.first
layer_base.name = "Plano_Principal"

# ═══════════════════════════════════════════════════════════════════════
# LÁMINA 1: PLANO ARQUITECTÓNICO EJECUTIVO CON COTAS Y DETALLES (A-01)
# ═══════════════════════════════════════════════════════════════════════
page1 = doc.pages.first
if File.exist?(plan_arch_png)
  # Ocupa toda la lámina A3 manteniendo proporciones
  img_b = Geom::Bounds2d.new(0.20, 0.20, PW - 0.40, PH - 0.40)
  img = Layout::Image.new(plan_arch_png, img_b)
  doc.add_entity(img, layer_base, page1)
end

# ═══════════════════════════════════════════════════════════════════════
# LÁMINA 2: PERSPECTIVA 3D GENERAL SUR-ESTE (A-02)
# ═══════════════════════════════════════════════════════════════════════
page2 = doc.pages.add("Perspectiva 3D Sur-Este")
vp2_b = Geom::Bounds2d.new(0.30, 0.30, PW - 0.60, PH - 0.60)
skp2 = Layout::SketchUpModel.new(skp_path, vp2_b)
doc.add_entity(skp2, layer_base, page2)
skp2.current_scene = 1 # 02_PERSPECTIVA_3D
skp2.render_mode = Layout::SketchUpModel::RASTER_RENDER
skp2.render if skp2.render_needed?

# ═══════════════════════════════════════════════════════════════════════
# LÁMINA 3: VISTA PATIO Y PISCINA NOR-OESTE (A-03)
# ═══════════════════════════════════════════════════════════════════════
page3 = doc.pages.add("Vista Patio y Piscina")
vp3_b = Geom::Bounds2d.new(0.30, 0.30, PW - 0.60, PH - 0.60)
skp3 = Layout::SketchUpModel.new(skp_path, vp3_b)
doc.add_entity(skp3, layer_base, page3)
skp3.current_scene = 2 # 03_VISTA_PATIO_PISCINA
skp3.render_mode = Layout::SketchUpModel::RASTER_RENDER
skp3.render if skp3.render_needed?

# Guardar documento
doc.save(layout_path)

# Copiar a escritorio
require 'fileutils'
FileUtils.cp(layout_path, desktop_path)

# Exportar PDF A3
pdf_out = "C:/Users/Oscar Martinez/Desktop/mi-casa/entrega/planos/00_CUADERNO_PLANOS_LAYOUT_A3.pdf"
doc.export(pdf_out)

"LAYOUT ARQUITECTÓNICO CREADO Y EXPORTADO A ESCRITORIO OK"
