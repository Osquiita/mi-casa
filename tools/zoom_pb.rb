# -*- coding: utf-8 -*-
model = Sketchup.active_model
p = model.pages["01_PLANTA_BAJA_2D"]
model.pages.selected_page = p if p
model.active_view.zoom_extents
model.active_view.refresh
"VISTA CENTRADA EN PLANTA BAJA"
