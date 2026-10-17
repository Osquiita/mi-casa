# -*- coding: utf-8 -*-
model = Sketchup.active_model
ents = model.entities

out = []
out << "=== DETALLE DE CARAS Y LINEAS DIBUJADAS POR EL USUARIO ==="
ents.each_with_index do |e, idx|
  if e.is_a?(Sketchup::Face)
    pts = e.vertices.map { |v| "(#{(v.position.x/1000.0).round(2)}, #{(v.position.y/1000.0).round(2)}, #{(v.position.z/1000.0).round(2)})" }.join(" -> ")
    out << "FACE [#{idx}]: Area=#{(e.area/1_000_000.0).round(2)} m2, Vertices=#{pts}"
  elsif e.is_a?(Sketchup::Edge)
    p1 = e.start.position
    p2 = e.end.position
    out << "EDGE [#{idx}]: (#{(p1.x/1000.0).round(2)}, #{(p1.y/1000.0).round(2)}, #{(p1.z/1000.0).round(2)}) -> (#{(p2.x/1000.0).round(2)}, #{(p2.y/1000.0).round(2)}, #{(p2.z/1000.0).round(2)})"
  end
end

File.write("C:/Users/Oscar Martinez/Desktop/mi-casa/tools/detalle_usuario.txt", out.join("\n"))
"DETALLE ESCRITO OK"
