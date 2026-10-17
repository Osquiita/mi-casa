# -*- coding: utf-8 -*-
# Inspeccionar cambios realizados por el usuario en SketchUp
model = Sketchup.active_model
ents = model.entities

report = []
report << "=== RESUMEN ENTIDADES SKETCHUP ==="
report << "Total entidades: #{ents.length}"

ents.each_with_index do |e, idx|
  if e.is_a?(Sketchup::Group)
    bb = e.bounds
    name = e.name.empty? ? "Sin Nombre" : e.name
    layer = e.layer.name
    report << "GROUP [#{idx}]: Name='#{name}', Layer='#{layer}', Min=(#{(bb.min.x/1000.0).round(2)}, #{(bb.min.y/1000.0).round(2)}, #{(bb.min.z/1000.0).round(2)}), Max=(#{(bb.max.x/1000.0).round(2)}, #{(bb.max.y/1000.0).round(2)}, #{(bb.max.z/1000.0).round(2)}), W=#{(bb.width/1000.0).round(2)}, H=#{(bb.height/1000.0).round(2)}, D=#{(bb.depth/1000.0).round(2)}"
  elsif e.is_a?(Sketchup::ComponentInstance)
    bb = e.bounds
    name = e.name.empty? ? e.definition.name : e.name
    layer = e.layer.name
    report << "COMP [#{idx}]: Name='#{name}', Layer='#{layer}', Min=(#{(bb.min.x/1000.0).round(2)}, #{(bb.min.y/1000.0).round(2)}, #{(bb.min.z/1000.0).round(2)}), Max=(#{(bb.max.x/1000.0).round(2)}, #{(bb.max.y/1000.0).round(2)}, #{(bb.max.z/1000.0).round(2)})"
  elsif e.is_a?(Sketchup::Face)
    bb = e.bounds
    report << "FACE [#{idx}]: Layer='#{e.layer.name}', Min=(#{(bb.min.x/1000.0).round(2)}, #{(bb.min.y/1000.0).round(2)}), Max=(#{(bb.max.x/1000.0).round(2)}, #{(bb.max.y/1000.0).round(2)})"
  elsif e.is_a?(Sketchup::Edge)
    # omit single edges unless needed
  end
end

report_str = report.join("\n")
File.write("C:/Users/Oscar Martinez/Desktop/mi-casa/tools/sketchup_dump.txt", report_str)
puts report_str
