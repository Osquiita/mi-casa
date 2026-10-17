# -*- coding: utf-8 -*-
model = Sketchup.active_model
pages = model.pages.map { |p| p.name }
skp_path = "C:/Users/Oscar Martinez/Desktop/mi-casa/casa-bifamiliar-3d.skp"
model.save(skp_path)

"SKP GUARDADO CON ESCENAS: #{pages.inspect} en #{skp_path}"
