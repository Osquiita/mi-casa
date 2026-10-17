# -*- coding: utf-8 -*-
model = Sketchup.active_model
out = "C:/Users/Oscar Martinez/Desktop/mi-casa/entrega/modelo-3d/casa-bifamiliar-planos-2d.skp"
FileUtils.rm_f(out) if File.exist?(out)
status = model.save(out)
status.to_json