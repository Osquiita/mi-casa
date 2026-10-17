# -*- coding: utf-8 -*-
# ==============================================================================
# CARGAR PLANOS 2D PNG DIRECTAMENTE EN SKETCHUP A ESCALA REAL
# ==============================================================================

model = Sketchup.active_model
ents  = model.entities
view  = model.active_view
cam   = view.camera
pages = model.pages

# 1. Limpiar geometría previa para dejar el espacio limpio
ents.clear!

# 2. Rutas a las imágenes de los planos
pb_path = "C:/Users/Oscar Martinez/Desktop/mi-casa/entrega/planos_2d/01_plano_2d_planta_baja.png"
pa_path = "C:/Users/Oscar Martinez/Desktop/mi-casa/entrega/planos_2d/02_plano_2d_planta_alta.png"

# 3. Insertar las imágenes como planos 2D a escala real en mm
# El solar mide 11.40m x 17.60m. La lámina completa con cajetín tiene 13.50m de ancho.
img_pb = nil
img_pa = nil

if File.exist?(pb_path)
  img_pb = ents.add_image(pb_path, Geom::Point3d.new(0, -3500.0, 0), 13500.0)
end

if File.exist?(pa_path)
  img_pa = ents.add_image(pa_path, Geom::Point3d.new(16000.0, -3500.0, 0), 13500.0)
end

# 4. Configurar la vista en 2D puro (Proyección Paralela Cenital)
cam.perspective = false

# Posicionar cámara sobre Planta Baja
cam.set(
  Geom::Point3d.new(6750.0, 7500.0, 35000.0),
  Geom::Point3d.new(6750.0, 7500.0, 0.0),
  Geom::Vector3d.new(0, 1, 0)
)
view.zoom_extents

# 5. Crear pestañas de escenas
p_pb = pages["01_PLANTA_BAJA_2D"] || pages.add("01_PLANTA_BAJA_2D")
pages.selected_page = p_pb
p_pb.update(127)

p_pa = pages["02_PLANTA_ALTA_2D"] || pages.add("02_PLANTA_ALTA_2D")
cam.set(
  Geom::Point3d.new(22750.0, 7500.0, 35000.0),
  Geom::Point3d.new(22750.0, 7500.0, 0.0),
  Geom::Vector3d.new(0, 1, 0)
)
p_pa.update(127)

p_gen = pages["03_AMBAS_PLANTAS_2D"] || pages.add("03_AMBAS_PLANTAS_2D")
cam.set(
  Geom::Point3d.new(14750.0, 7500.0, 55000.0),
  Geom::Point3d.new(14750.0, 7500.0, 0.0),
  Geom::Vector3d.new(0, 1, 0)
)
p_gen.update(127)

# Dejar seleccionada la Planta Baja
pages.selected_page = p_pb
view.refresh

model.save("C:/Users/Oscar Martinez/Desktop/mi-casa/casa-bifamiliar-3d.skp")
"PLANOS 2D PNG CARGADOS EN SKETCHUP PERFECTAMENTE"
