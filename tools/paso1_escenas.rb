# -*- coding: utf-8 -*-
# ==============================================================================
# GENERAR DOCUMENTO LAYOUT PROFESIONAL DESDE SKETCHUP (V2 - Fix)
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

# ─── 2. RENDERIZADO LIMPIO (solo opciones seguras) ────────────────────
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

# Solo opciones de rendering que sabemos que existen
begin; rendering["DisplayFog"]          = false; rescue; end
begin; rendering["DrawGround"]          = false; rescue; end
begin; rendering["DrawHorizon"]         = false; rescue; end
begin; rendering["DrawUnderground"]     = false; rescue; end
shadow_info["DisplayShadows"] = false

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

"ESCENAS CREADAS OK: #{PAGES.count} escenas. SKP guardado."
