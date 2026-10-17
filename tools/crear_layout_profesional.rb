# -*- coding: utf-8 -*-
# ==============================================================================
# GENERAR DOCUMENTO LAYOUT PROFESIONAL DESDE SKETCHUP
# ==============================================================================
# Ejecutar dentro de SketchUp vía MCP socket (ruby_eval).
# 1) Crea/actualiza escenas optimizadas para LayOut
# 2) Genera un .layout con láminas A3 profesionales
# ==============================================================================

M     = 1000.0
MODEL = Sketchup.active_model
ENTS  = MODEL.entities
PAGES = MODEL.pages
VIEW  = MODEL.active_view
CAM   = VIEW.camera

def mm(v); v * M; end

# ─── 1. LIMPIAR ESCENAS ANTIGUAS ──────────────────────────────────────
old_names = ["PB_PLANTA_2D", "PB_PERSPECTIVA_3D", "PB_VISTA_PATIO",
             "PB_AXONOMETRIA", "01_PLANTA_EDITABLE_2D", "02_PERSPECTIVA_3D_EDITABLE"]
old_names.each do |n|
  pg = PAGES[n]
  PAGES.erase(pg) if pg
end

# ─── 2. RENDERIZADO LIMPIO ───────────────────────────────────────────
rendering   = MODEL.rendering_options
shadow_info = MODEL.shadow_info

# ─── 3. ESCENA: PLANTA BAJA CENITAL ─────────────────────────────────
CAM.perspective = false
cx = mm(5.70)
cy = mm(8.80)
CAM.set(
  Geom::Point3d.new(cx, cy, mm(50.0)),
  Geom::Point3d.new(cx, cy, 0.0),
  Geom::Vector3d.new(0, 1, 0)
)
VIEW.zoom_extents

rendering["DrawSilhouettes"]     = true
rendering["SilhouetteWidth"]     = 2
rendering["EdgeDisplayMode"]     = 1
rendering["DrawDepthQue"]        = false
rendering["DisplayFog"]          = false
rendering["DrawGround"]          = false
rendering["DrawHorizon"]         = false
rendering["DrawUnderground"]     = false
rendering["DisplaySectionPlane"] = false
rendering["DisplaySectionCuts"]  = false
rendering["InactiveHidden"]      = false
rendering["InstanceHidden"]      = false
shadow_info["DisplayShadows"]    = false

p1 = PAGES.add("PB_PLANTA_2D")
p1.update(127)

# ─── 4. ESCENA: PERSPECTIVA SUR-ESTE ─────────────────────────────────
CAM.perspective = true
CAM.fov = 45.0
CAM.set(
  Geom::Point3d.new(mm(18.0), mm(-8.0), mm(14.0)),
  Geom::Point3d.new(mm(5.70), mm(8.80), mm(0.6)),
  Geom::Vector3d.new(0, 0, 1)
)
shadow_info["DisplayShadows"] = true
shadow_info["UseSunForAllShading"] = true
shadow_info["Light"]  = 80
shadow_info["Dark"]   = 50

p2 = PAGES.add("PB_PERSPECTIVA_3D")
p2.update(127)

# ─── 5. ESCENA: VISTA PATIO/PISCINA NOR-OESTE ────────────────────────
CAM.fov = 40.0
CAM.set(
  Geom::Point3d.new(mm(-4.0), mm(20.0), mm(12.0)),
  Geom::Point3d.new(mm(8.90), mm(10.0), mm(0.6)),
  Geom::Vector3d.new(0, 0, 1)
)
p3 = PAGES.add("PB_VISTA_PATIO")
p3.update(127)

# ─── 6. VOLVER A PLANTA Y GUARDAR ────────────────────────────────────
PAGES.selected_page = p1
shadow_info["DisplayShadows"] = false
VIEW.refresh

skp_path = "C:/Users/Oscar Martinez/Desktop/mi-casa/casa-bifamiliar-3d.skp"
MODEL.save(skp_path)

# ======================================================================
# 7. CREAR DOCUMENTO LAYOUT PROFESIONAL (A3 Horizontal)
# ======================================================================
require 'layout'

layout_dir = "C:/Users/Oscar Martinez/Desktop/mi-casa/entrega/planos"
Dir.mkdir(layout_dir) unless Dir.exist?(layout_dir)
LAYOUT_PATH = "#{layout_dir}/casa-bifamiliar-planos.layout"

# ─── Documento A3 Apaisado ───
# A3 = 420 x 297 mm = 16.535 x 11.693 pulgadas
doc = Layout::Document.new
info = doc.page_info
info.width  = 16.535   # 420mm
info.height = 11.693   # 297mm
info.left_margin   = 0.7874  # 20mm
info.right_margin  = 0.3937  # 10mm
info.top_margin    = 0.3937  # 10mm
info.bottom_margin = 0.7874  # 20mm

layer0 = doc.layers.first

# ─── LÁMINA 1: PLANTA BAJA (Escala ~1:50) ────────────────────────────
page1 = doc.pages.first

# Para escala 1:50 en A3 apaisado:
# El modelo mide aprox 11.70m x 17.75m
# A 1:50 → 234mm x 355mm = 9.21" x 13.98"
# Centrado en A3 horizontal
vp_w = 13.0    # viewport width en pulgadas
vp_h = 9.0     # viewport height en pulgadas
vp_x = (16.535 - vp_w) / 2.0   # centrar horizontalmente
vp_y = 0.6                      # margen superior

bounds1 = Geom::Bounds2d.new(vp_x, vp_y, vp_w, vp_h)
skp1 = Layout::SketchUpModel.new(skp_path, bounds1)
doc.add_entity(skp1, layer0, page1)

# Configurar para escena de planta
skp1.current_scene = 0
skp1.render_mode = Layout::SketchUpModel::HYBRID_RENDER
skp1.preserve_scale_on_resize = true

# Render para que procese
skp1.render if skp1.render_needed?

# ─── Textos de cajetín Lámina 1 ───
# Título
tb1 = Geom::Bounds2d.new(0.9, 10.4, 9.0, 0.4)
t1 = Layout::FormattedText.new("PLANTA BAJA AMUEBLADA Y ACOTADA", tb1)
doc.add_entity(t1, layer0, page1)

# Cajetín derecha
cb1 = Geom::Bounds2d.new(10.5, 10.2, 5.5, 1.2)
c1 = Layout::FormattedText.new(
  "PROYECTO RESIDENCIAL BIFAMILIAR\n" \
  "PALMA DEL RÍO (CÓRDOBA)\n" \
  "LÁMINA A-02 · PLANTA BAJA\n" \
  "SUP. ÚTIL: 136,7 m² | EXTERIOR: 37,8 m²",
  cb1
)
doc.add_entity(c1, layer0, page1)

# Indicación de escala
sb1 = Geom::Bounds2d.new(0.9, 10.9, 4.0, 0.3)
s1 = Layout::FormattedText.new("ESCALA APROX. 1:50 EN A3", sb1)
doc.add_entity(s1, layer0, page1)

# ─── LÁMINA 2: PERSPECTIVA 3D ────────────────────────────────────────
page2 = doc.pages.add("PERSPECTIVA 3D")

bounds2 = Geom::Bounds2d.new(0.9, 0.5, 14.5, 9.5)
skp2 = Layout::SketchUpModel.new(skp_path, bounds2)
doc.add_entity(skp2, layer0, page2)
skp2.current_scene = 1
skp2.render_mode = Layout::SketchUpModel::HYBRID_RENDER
skp2.render if skp2.render_needed?

tb2 = Geom::Bounds2d.new(0.9, 10.4, 9.0, 0.4)
t2 = Layout::FormattedText.new("PERSPECTIVA 3D · VISTA SUR-ESTE", tb2)
doc.add_entity(t2, layer0, page2)

cb2 = Geom::Bounds2d.new(10.5, 10.2, 5.5, 1.2)
c2 = Layout::FormattedText.new(
  "PROYECTO RESIDENCIAL BIFAMILIAR\n" \
  "PALMA DEL RÍO (CÓRDOBA)\n" \
  "LÁMINA A-05 · PERSPECTIVA GENERAL",
  cb2
)
doc.add_entity(c2, layer0, page2)

# ─── LÁMINA 3: VISTA PATIO / PISCINA ─────────────────────────────────
page3 = doc.pages.add("VISTA PATIO")

bounds3 = Geom::Bounds2d.new(0.9, 0.5, 14.5, 9.5)
skp3 = Layout::SketchUpModel.new(skp_path, bounds3)
doc.add_entity(skp3, layer0, page3)
skp3.current_scene = 2
skp3.render_mode = Layout::SketchUpModel::HYBRID_RENDER
skp3.render if skp3.render_needed?

tb3 = Geom::Bounds2d.new(0.9, 10.4, 9.0, 0.4)
t3 = Layout::FormattedText.new("VISTA PATIO Y PISCINA · NOR-OESTE", tb3)
doc.add_entity(t3, layer0, page3)

cb3 = Geom::Bounds2d.new(10.5, 10.2, 5.5, 1.2)
c3 = Layout::FormattedText.new(
  "PROYECTO RESIDENCIAL BIFAMILIAR\n" \
  "PALMA DEL RÍO (CÓRDOBA)\n" \
  "LÁMINA A-06 · PERSPECTIVA PATIO",
  cb3
)
doc.add_entity(c3, layer0, page3)

# ─── GUARDAR LAYOUT ──────────────────────────────────────────────────
doc.save(LAYOUT_PATH)

"LAYOUT PROFESIONAL CREADO: #{doc.pages.count} láminas A3. Archivo: #{LAYOUT_PATH}"
