# -*- coding: utf-8 -*-
# ==============================================================================
# VISTA 2D DE PLANTA BAJA EN SKETCHUP
# Configura SketchUp en Proyección Paralela Cenital (Vista en Planta 2D a 1,40m)
# ==============================================================================

MODEL = Sketchup.active_model
VIEW  = MODEL.active_view
CAM   = VIEW.camera
PAGES = MODEL.pages

# 1. Ocultar elementos de Planta Alta y Cubierta para ver la Planta Baja en limpio
MODEL.entities.each do |e|
  next unless e.is_a?(Sketchup::Group)
  n = e.name.to_s
  
  # Si es de planta alta, cubierta o lucernario -> ocultar
  if n =~ /_pa|cubierta|parapeto|albardilla|lucernario|balc|pat2|madera-d2|lama-sal/i
    e.hidden = true
  else
    e.hidden = false
  end
end

# 2. Configurar la cámara en Vista Superior Ortogonal (2D puro)
CAM.perspective = false # Proyección paralela (sin perspectiva 3D cónica)

# Centro del solar: X=5.70m (5700mm), Y=8.80m (8800mm)
center_x = 5700.0
center_y = 8800.0

# Cámara mirando desde arriba hacia abajo, eje Y como arriba en pantalla
CAM.set(
  Geom::Point3d.new(center_x, center_y, 30000.0), # Eye arriba
  Geom::Point3d.new(center_x, center_y, 0.0),     # Target abajo
  Geom::Vector3d.new(0, 1, 0)                     # Up vector hacia el norte (Y positivo)
)

# 3. Ajustar zoom a toda la planta baja
VIEW.zoom_extents

# 4. Crear escena permanente "01_PLANTA_BAJA_2D"
page = PAGES["01_PLANTA_BAJA_2D"] || PAGES.add("01_PLANTA_BAJA_2D")
PAGES.selected_page = page
page.update(1)

VIEW.refresh
"VISTA 2D PLANTA BAJA CONFIGURADA EN SKETCHUP"
