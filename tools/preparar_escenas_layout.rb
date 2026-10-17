# -*- coding: utf-8 -*-
# ==============================================================================
# PREPARAR ESCENAS PROFESIONALES EN SKETCHUP PARA LAYOUT 2025
# ==============================================================================
# Este script crea escenas orto + perspectivas optimizadas para vincular
# desde LayOut como viewports a escala real.

M     = 1000.0
MODEL = Sketchup.active_model
ENTS  = MODEL.entities
PAGES = MODEL.pages
VIEW  = MODEL.active_view
CAM   = VIEW.camera

def mm(v); v * M; end

# ─── Definir Estilos de Renderizado ───
# Usar un estilo limpio para planta (sin sombras, sin perfiles gruesos)
style_mgr = MODEL.styles
rendering  = MODEL.rendering_options

# ─── ESCENA 1: PLANTA BAJA 2D (Cenital Ortográfica) ───
scene_name_1 = "PB_PLANTA_2D"
p1 = PAGES[scene_name_1]
if p1
  PAGES.erase(p1)
end

# Configurar cámara ortográfica cenital
CAM.perspective = false
# Centro del modelo: X≈5.70, Y≈8.80
cx = mm(5.70)
cy = mm(8.80)
CAM.set(
  Geom::Point3d.new(cx, cy, mm(50.0)),   # eye (arriba)
  Geom::Point3d.new(cx, cy, 0.0),        # target (suelo)
  Geom::Vector3d.new(0, 1, 0)            # up = norte
)

# Zoom para encuadrar toda la planta baja
VIEW.zoom_extents

# Rendering limpio para planta
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

# Sombras OFF para vista 2D
shadow_info = MODEL.shadow_info
shadow_info["DisplayShadows"] = false

p1 = PAGES.add(scene_name_1)
p1.update(127)  # Guardar todo: cámara + capas + estilo

# ─── ESCENA 2: PERSPECTIVA 3D SUR-ESTE ───
scene_name_2 = "PB_PERSPECTIVA_3D"
p2 = PAGES[scene_name_2]
if p2
  PAGES.erase(p2)
end

CAM.perspective = true
CAM.fov = 45.0
CAM.set(
  Geom::Point3d.new(mm(18.0), mm(-8.0), mm(14.0)),  # eye
  Geom::Point3d.new(mm(5.70), mm(8.80), mm(0.6)),    # target
  Geom::Vector3d.new(0, 0, 1)                         # up
)

# Sombras sutiles para 3D
shadow_info["DisplayShadows"] = true
shadow_info["UseSunForAllShading"] = true
shadow_info["ShadowTime_time_t"]  = Time.new(2026, 6, 21, 10, 0, 0).to_i rescue shadow_info["ShadowTime_time_t"]
shadow_info["Light"]      = 80
shadow_info["Dark"]       = 50

p2 = PAGES.add(scene_name_2)
p2.update(127)

# ─── ESCENA 3: PERSPECTIVA 3D NOR-OESTE (Vista Patio/Piscina) ───
scene_name_3 = "PB_VISTA_PATIO"
p3 = PAGES[scene_name_3]
if p3
  PAGES.erase(p3)
end

CAM.perspective = true
CAM.fov = 40.0
CAM.set(
  Geom::Point3d.new(mm(-4.0), mm(20.0), mm(12.0)),  # eye nor-oeste
  Geom::Point3d.new(mm(8.90), mm(10.0), mm(0.6)),   # target al patio
  Geom::Vector3d.new(0, 0, 1)
)
p3 = PAGES.add(scene_name_3)
p3.update(127)

# ─── ESCENA 4: AXONOMETRÍA ISOMÉTRICA ───
scene_name_4 = "PB_AXONOMETRIA"
p4 = PAGES[scene_name_4]
if p4
  PAGES.erase(p4)
end

CAM.perspective = false
# Isométrica clásica: 30° arriba, 45° lateral
iso_dist = mm(30.0)
angle_h  = 45.0 * Math::PI / 180.0
angle_v  = 35.264 * Math::PI / 180.0  # arctan(1/sqrt(2)) para iso

ex = cx + iso_dist * Math.cos(angle_v) * Math.sin(angle_h)
ey = cy - iso_dist * Math.cos(angle_v) * Math.cos(angle_h)
ez = iso_dist * Math.sin(angle_v)

CAM.set(
  Geom::Point3d.new(ex, ey, ez),
  Geom::Point3d.new(cx, cy, mm(0.6)),
  Geom::Vector3d.new(0, 0, 1)
)
VIEW.zoom_extents

p4 = PAGES.add(scene_name_4)
p4.update(127)

# ─── Volver a la escena de planta para que sea la vista por defecto ───
PAGES.selected_page = p1

# Sombras off de vuelta para planta limpia
shadow_info["DisplayShadows"] = false

# ─── GUARDAR ───
skp_path = "C:/Users/Oscar Martinez/Desktop/mi-casa/casa-bifamiliar-3d.skp"
MODEL.save(skp_path)

"ESCENAS LAYOUT LISTAS: #{PAGES.count} escenas creadas. SKP guardado en #{skp_path}"
