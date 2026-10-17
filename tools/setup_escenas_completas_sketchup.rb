# -*- coding: utf-8 -*-
# ==============================================================================
# CONFIGURACIÓN DE ESCENAS 2D Y 3D EN SKETCHUP
# Permite alternar con un solo clic entre las pestañas de Escenas en SketchUp:
#  - [01_PLANTA_BAJA_2D]
#  - [02_PLANTA_ALTA_2D]
#  - [03_PERSPECTIVA_3D]
# ==============================================================================

MODEL = Sketchup.active_model
VIEW  = MODEL.active_view
CAM   = VIEW.camera
PAGES = MODEL.pages

CX = 5700.0
CY = 8800.0

# ------------------------------------------------------------------------------
# ESCENA 1: PLANTA BAJA 2D (Activa por defecto)
# ------------------------------------------------------------------------------
MODEL.entities.each do |e|
  next unless e.is_a?(Sketchup::Group)
  n = e.name.to_s
  if n =~ /_pa|cubierta|parapeto|albardilla|lucernario|balc|pat2|madera-d2|lama-sal/i
    e.hidden = true
  else
    e.hidden = false
  end
end

CAM.perspective = false # Proyección paralela 2D ortogonal
CAM.set(
  Geom::Point3d.new(CX, CY, 30000.0),
  Geom::Point3d.new(CX, CY, 0.0),
  Geom::Vector3d.new(0, 1, 0)
)
VIEW.zoom_extents

p1 = PAGES["01_PLANTA_BAJA_2D"] || PAGES.add("01_PLANTA_BAJA_2D")
PAGES.selected_page = p1
p1.update(127) # Guarda cámara, capas, visibilidad de objetos y estilos

# ------------------------------------------------------------------------------
# ESCENA 2: PLANTA ALTA 2D
# ------------------------------------------------------------------------------
MODEL.entities.each do |e|
  next unless e.is_a?(Sketchup::Group)
  n = e.name.to_s
  if n =~ /cubierta|parapeto|albardilla|lucernario/i
    e.hidden = true
  else
    e.hidden = false
  end
end

p2 = PAGES["02_PLANTA_ALTA_2D"] || PAGES.add("02_PLANTA_ALTA_2D")
PAGES.selected_page = p2
p2.update(127)

# ------------------------------------------------------------------------------
# ESCENA 3: PERSPECTIVA 3D EXTERIOR
# ------------------------------------------------------------------------------
MODEL.entities.each do |e|
  next unless e.is_a?(Sketchup::Group)
  e.hidden = false # Todo visible
end

CAM.perspective = true # Perspectiva 3D cónica
CAM.fov = 45.0
CAM.set(
  Geom::Point3d.new(CX + 14000.0, -10000.0, 2800.0),
  Geom::Point3d.new(CX, 3000.0, 2500.0),
  Geom::Vector3d.new(0, 0, 1)
)

p3 = PAGES["03_PERSPECTIVA_3D"] || PAGES.add("03_PERSPECTIVA_3D")
PAGES.selected_page = p3
p3.update(127)

# Dejar seleccionada la Escena 1 (PLANTA BAJA 2D) como vista inicial activa
PAGES.selected_page = p1
VIEW.refresh

# Guardar cambios en el archivo .skp
MODEL.save("C:/Users/Oscar Martinez/Desktop/mi-casa/casa-bifamiliar-3d.skp")

"ESCENAS 2D Y 3D CONFIGURADAS EN SKETCHUP. VISTA ACTIVA: 01_PLANTA_BAJA_2D"
