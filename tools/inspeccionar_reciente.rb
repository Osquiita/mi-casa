# -*- coding: utf-8 -*-
# Inspección detallada de entidades, grupos, caras y cotas útiles en SketchUp
model = Sketchup.active_model
ents = model.entities

out = []
out << "=== INSPECCION EXACTA DE SKETCHUP TRAS CAMBIOS DEL USUARIO ==="
out << "Total entidades en raiz: #{ents.length}"

def inspect_entities(entities, prefix="", out=[])
  entities.each_with_index do |e, idx|
    layer_name = e.layer ? e.layer.name : "Sin_Capa"
    if e.is_a?(Sketchup::Group)
      bb = e.bounds
      name = e.name.empty? ? "Grupo_#{idx}" : e.name
      w = (bb.width/1000.0).round(3)
      h = (bb.height/1000.0).round(3)
      d = (bb.depth/1000.0).round(3)
      min_p = "(#{(bb.min.x/1000.0).round(3)}, #{(bb.min.y/1000.0).round(3)}, #{(bb.min.z/1000.0).round(3)})"
      max_p = "(#{(bb.max.x/1000.0).round(3)}, #{(bb.max.y/1000.0).round(3)}, #{(bb.max.z/1000.0).round(3)})"
      out << "#{prefix}GROUP [#{idx}]: Name='#{name}', Layer='#{layer_name}', Min=#{min_p}, Max=#{max_p}, W=#{w}, H=#{h}, D=#{d}"
    elsif e.is_a?(Sketchup::ComponentInstance)
      bb = e.bounds
      name = e.name.empty? ? e.definition.name : e.name
      min_p = "(#{(bb.min.x/1000.0).round(3)}, #{(bb.min.y/1000.0).round(3)}, #{(bb.min.z/1000.0).round(3)})"
      max_p = "(#{(bb.max.x/1000.0).round(3)}, #{(bb.max.y/1000.0).round(3)}, #{(bb.max.z/1000.0).round(3)})"
      out << "#{prefix}COMP [#{idx}]: Name='#{name}', Def='#{e.definition.name}', Layer='#{layer_name}', Min=#{min_p}, Max=#{max_p}"
    elsif e.is_a?(Sketchup::Face)
      bb = e.bounds
      pts = e.vertices.map { |v| "(#{(v.position.x/1000.0).round(3)}, #{(v.position.y/1000.0).round(3)})" }.join(" -> ")
      area = (e.area / 1_000_000.0).round(3)
      out << "#{prefix}FACE [#{idx}]: Area=#{area} m2, Layer='#{layer_name}', Pts=#{pts}"
    elsif e.is_a?(Sketchup::Edge)
      p1 = e.start.position
      p2 = e.end.position
      len = (e.length / 1000.0).round(3)
      out << "#{prefix}EDGE [#{idx}]: Len=#{len}m, (#{(p1.x/1000.0).round(3)}, #{(p1.y/1000.0).round(3)}) -> (#{(p2.x/1000.0).round(3)}, #{(p2.y/1000.0).round(3)})"
    elsif e.is_a?(Sketchup::Dimension)
      out << "#{prefix}DIM [#{idx}]: Text='#{e.text}'"
    elsif e.is_a?(Sketchup::Text)
      out << "#{prefix}TEXT [#{idx}]: Text='#{e.text}'"
    end
  end
end

inspect_entities(ents, "", out)

File.write("C:/Users/Oscar Martinez/Desktop/mi-casa/tools/sketchup_cambios_usuario_recientes.txt", out.join("\n"))
"INSPECCION COMPLETADA"
