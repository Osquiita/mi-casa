# -*- coding: utf-8 -*-
model = Sketchup.active_model
states = []
planos = [
  "paso-01-parcela.dxf",
  "paso-02-planta-baja.dxf",
  "paso-03-planta-alta.dxf",
  "paso-04-alzados-seccion.dxf",
  "paso-05-cuadro-superficies.dxf",
]
base = "C:/Users/Oscar Martinez/Desktop/mi-casa/"
planos.each do |p|
  begin
    s = model.import(File.join(base, p))
    states << [p, s]
  rescue StandardError => e
    states << [p, "ERROR: #{e.class}: #{e.message}"]
  end
end
states.to_json