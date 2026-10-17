# -*- coding: utf-8 -*-
# Guardar el modelo SKP con escenas listas para vincular a LayOut
model = Sketchup.active_model
path = "C:/Users/Oscar Martinez/Desktop/mi-casa/casa-bifamiliar-3d.skp"
status = model.save(path)
"SKP GUARDADO CON EXITO PARA LAYOUT: #{status} EN #{path}"
