# -*- coding: utf-8 -*-
g = Sketchup.active_model.entities.add_group
t = g.entities.add_text("SALON 37 m2", Geom::Point3d.new(1000, 2000, 50))
"NATIVE TEXT OK: #{t}"
