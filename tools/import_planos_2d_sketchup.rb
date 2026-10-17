# -*- coding: utf-8 -*-
MODEL = Sketchup.active_model
ENTS  = MODEL.entities
VIEW  = MODEL.active_view
CAM   = VIEW.camera
PAGES = MODEL.pages

# Limpiar entidades anteriores
ENTS.clear!

# Rutas a las imágenes de los planos 2D
img_pb_path = "C:/Users/Oscar Martinez/Desktop/mi-casa/entrega/planos_2d/01_plano_2d_planta_baja.png"
img_pa_path = "C:/Users/Oscar Martinez/Desktop/mi-casa/entrega/planos_2d/02_plano_2d_planta_alta.png"

# Dimensiones en mm (Solar 11.40m x 17.60m con márgenes de cajetín: ancho ~13.5m, alto ~20.0m)
# Importar imagen de Planta Baja
if File.exist?(img_pb_path)
  img_pb = ENTS.add_image(img_pb_path, Geom::Point3d.new(0, -3500, 0), 13500.0)
end

# Importar imagen de Planta Alta al lado
if File.exist?(img_pa_path)
  img_pa = ENTS.add_image(img_pa_path, Geom::Point3d.new(16000, -3500, 0), 13500.0)
end

# Configurar vista cenital ortogonal (2D puro)
CAM.perspective = false
VIEW.zoom_extents

# Configurar Escenas
p1 = PAGES["01_PLANTA_BAJA_2D"] || PAGES.add("01_PLANTA_BAJA_2D")
PAGES.selected_page = p1

MODEL.save("C:/Users/Oscar Martinez/Desktop/mi-casa/casa-bifamiliar-3d.skp")
"PLANOS 2D IMPORTADOS EN SKETCHUP CON EXITO"
