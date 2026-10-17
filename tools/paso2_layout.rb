# -*- coding: utf-8 -*-
# ==============================================================================
# PASO 2: CREAR DOCUMENTO LAYOUT PROFESIONAL (A3 Horizontal)
# Layout:: namespace ya disponible en SketchUp 2026
# ==============================================================================

skp_path    = "C:/Users/Oscar Martinez/Desktop/mi-casa/casa-bifamiliar-3d.skp"
layout_dir  = "C:/Users/Oscar Martinez/Desktop/mi-casa/entrega/planos"
Dir.mkdir(layout_dir) unless Dir.exist?(layout_dir)
layout_path = "#{layout_dir}/casa-bifamiliar-planos.layout"

# ─── Documento A3 Apaisado ───
doc  = Layout::Document.new
info = doc.page_info
info.width  = 16.535   # 420mm
info.height = 11.693   # 297mm
info.left_margin   = 0.7874
info.right_margin  = 0.3937
info.top_margin    = 0.3937
info.bottom_margin = 0.7874

layer0 = doc.layers.first

# ═══════════════════════════════════════════════════════════════════════
# LÁMINA 1: PLANTA BAJA ACOTADA (~1:50)
# ═══════════════════════════════════════════════════════════════════════
page1 = doc.pages.first

vp_w = 12.0
vp_h = 9.0
vp_x = (16.535 - vp_w) / 2.0
vp_y = 0.5

bounds1 = Geom::Bounds2d.new(vp_x, vp_y, vp_w, vp_h)
skp1 = Layout::SketchUpModel.new(skp_path, bounds1)
doc.add_entity(skp1, layer0, page1)
skp1.current_scene = 0
skp1.render_mode = Layout::SketchUpModel::HYBRID_RENDER
skp1.preserve_scale_on_resize = true

# Título
tb1 = Geom::Bounds2d.new(0.9, 10.2, 8.0, 0.5)
t1 = Layout::FormattedText.new("A-02  PLANTA BAJA AMUEBLADA Y ACOTADA", tb1)
doc.add_entity(t1, layer0, page1)

# Cajetín
cb1 = Geom::Bounds2d.new(10.0, 10.0, 6.0, 1.4)
c1 = Layout::FormattedText.new(
  "PROYECTO RESIDENCIAL BIFAMILIAR\n" \
  "PALMA DEL RIO (CORDOBA)\n" \
  "SUP. UTIL CERRADA: 136,7 m2\n" \
  "SUP. EXTERIOR: 37,8 m2",
  cb1
)
doc.add_entity(c1, layer0, page1)

# ═══════════════════════════════════════════════════════════════════════
# LÁMINA 2: PERSPECTIVA 3D SUR-ESTE
# ═══════════════════════════════════════════════════════════════════════
page2 = doc.pages.add("PERSPECTIVA 3D")

bounds2 = Geom::Bounds2d.new(0.9, 0.5, 14.5, 9.5)
skp2 = Layout::SketchUpModel.new(skp_path, bounds2)
doc.add_entity(skp2, layer0, page2)
skp2.current_scene = 1
skp2.render_mode = Layout::SketchUpModel::HYBRID_RENDER

tb2 = Geom::Bounds2d.new(0.9, 10.2, 8.0, 0.5)
t2 = Layout::FormattedText.new("A-05  PERSPECTIVA 3D - VISTA SUR-ESTE", tb2)
doc.add_entity(t2, layer0, page2)

cb2 = Geom::Bounds2d.new(10.0, 10.0, 6.0, 1.4)
c2 = Layout::FormattedText.new(
  "PROYECTO RESIDENCIAL BIFAMILIAR\n" \
  "PALMA DEL RIO (CORDOBA)\n" \
  "PERSPECTIVA GENERAL",
  cb2
)
doc.add_entity(c2, layer0, page2)

# ═══════════════════════════════════════════════════════════════════════
# LÁMINA 3: VISTA PATIO / PISCINA
# ═══════════════════════════════════════════════════════════════════════
page3 = doc.pages.add("VISTA PATIO")

bounds3 = Geom::Bounds2d.new(0.9, 0.5, 14.5, 9.5)
skp3 = Layout::SketchUpModel.new(skp_path, bounds3)
doc.add_entity(skp3, layer0, page3)
skp3.current_scene = 2
skp3.render_mode = Layout::SketchUpModel::HYBRID_RENDER

tb3 = Geom::Bounds2d.new(0.9, 10.2, 8.0, 0.5)
t3 = Layout::FormattedText.new("A-06  VISTA PATIO Y PISCINA - NOR-OESTE", tb3)
doc.add_entity(t3, layer0, page3)

cb3 = Geom::Bounds2d.new(10.0, 10.0, 6.0, 1.4)
c3 = Layout::FormattedText.new(
  "PROYECTO RESIDENCIAL BIFAMILIAR\n" \
  "PALMA DEL RIO (CORDOBA)\n" \
  "PERSPECTIVA PATIO / PISCINA",
  cb3
)
doc.add_entity(c3, layer0, page3)

# ═══════════════════════════════════════════════════════════════════════
# GUARDAR
# ═══════════════════════════════════════════════════════════════════════
doc.save(layout_path)

"LAYOUT PROFESIONAL CREADO: #{doc.pages.count} laminas A3 en #{layout_path}"
