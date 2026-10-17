# -*- coding: utf-8 -*-
# Guardar modelo actual y enviar a LayOut
model = Sketchup.active_model
skp_path = "C:/Users/Oscar Martinez/Desktop/mi-casa/casa-bifamiliar-3d.skp"
model.save(skp_path)

# Copiar el archivo .layout al Escritorio para acceso directo en 1 clic
layout_src = "C:/Users/Oscar Martinez/Desktop/mi-casa/entrega/planos/casa-bifamiliar-COMPLETO.layout"
layout_dst = "C:/Users/Oscar Martinez/Desktop/00_PROYECTO_CASA_LAYOUT.layout"

require 'fileutils'
FileUtils.cp(layout_src, layout_dst) if File.exist?(layout_src)

# Llamar a send_to_layout
status = Sketchup.send_to_layout(skp_path)

"SEND TO LAYOUT EJECUTADO: #{status}\nCopia en escritorio: #{layout_dst}"
