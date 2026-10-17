# -*- coding: utf-8 -*-
model = Sketchup.active_model
path = model.path
entities_count = model.entities.count
layers_info = model.layers.map { |l| "#{l.name} (visible: #{l.visible?})" }
pages_info  = model.pages.map { |p| p.name }
camera = model.active_view.camera

"DIAGNOSTICO SKETCHUP:\n" \
"Path: #{path.inspect}\n" \
"Entities: #{entities_count}\n" \
"Layers: #{layers_info.inspect}\n" \
"Pages/Scenes: #{pages_info.inspect}\n" \
"Camera eye: #{camera.eye.to_a.inspect}\n" \
"Camera target: #{camera.target.to_a.inspect}\n" \
"Camera perspective: #{camera.perspective?}"
