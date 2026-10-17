# Exportar vista actual de SketchUp para verificar
view = Sketchup.active_model.active_view
out_img = "C:/Users/Oscar Martinez/Desktop/mi-casa/entrega/renders/sketchup_viewport_current.png"
view.write_image(out_img, 1600, 1000, false, 0.0)
"VIEWPORT EXPORTADO OK -> #{out_img}"
