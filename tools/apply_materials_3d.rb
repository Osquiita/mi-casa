# -*- coding: utf-8 -*-
# Materiales v2: asigna colores por nombre de grupo.
MODEL = Sketchup.active_model
MATS = MODEL.materials

def mat(name, r, g, b, alpha = 1.0)
  m = MATS[name]; m = MATS.add(name) unless m
  m.color = Sketchup::Color.new(r, g, b)
  m.alpha = alpha if m.respond_to?(:alpha=)
  m
end

estuco   = mat("Estuco", 242, 240, 233)
estucogr = mat("EstucoGris", 215, 214, 208)
hormigon = mat("Hormigon", 178, 178, 175)
cristal  = mat("Cristal", 150, 195, 230, 0.45)
suelo    = mat("Suelo", 120, 92, 58)
cesped   = mat("Cesped", 148, 176, 106)
pavimento= mat("Pavimento", 184, 179, 169)
asfalto  = mat("Asfalto", 80, 80, 85)
madera   = mat("Madera", 184, 133, 87)
madera2  = mat("MaderaOscura", 143, 102, 64)
metal    = mat("Metal", 140, 148, 155)
coche    = mat("Coche", 102, 135, 163)
garage   = mat("GarageDoor", 66, 71, 79)
mobiliario= mat("Mobiliario", 200, 198, 192)
olivo    = mat("Olivo", 77, 133, 66)
trunk    = mat("Tronco", 107, 84, 61)

MODEL.entities.each do |e|
  next unless e.is_a?(Sketchup::Group)
  n = e.name.to_s
  layer = e.respond_to?(:layer) ? e.layer.name.to_s : ""
  m = nil

  if layer == "VENTANAS"
    m = cristal
  elsif layer == "PARCELA"
    if n =~ /calle|asfalto/ then m = asfalto
    elsif n =~ /cesped|seto|crown|hojas/ then m = cesped
    elsif n =~ /ground/ then m = suelo
    else m = cesped end
  elsif layer == "ESCALERA"
    m = hormigon
  elsif n =~ /olivo-crown|crown/ then m = olivo
  elsif n =~ /olivo-trunk|trunk/ then m = trunk
  elsif n =~ /olivo-pot|maceta|solera|slab|fj-|cub-|parap|pav-/ then m = hormigon
  elsif n =~ /pergola.*lama|pergola.*viga|lama-|wood/i then m = madera
  elsif n =~ /barandilla|alb-|metal/i then m = metal
  elsif n =~ /puerta|corredera|door/i then m = madera2
  elsif n =~ /porton|garage/i then m = garage
  elsif n =~ /coche-cuerpo/ then m = coche
  elsif n =~ /coche-techo/ then m = cristal
  elsif n =~ /coche|rueda/ then m = metal
  elsif n =~ /sofa|mesa|tv|butaca|isla|encim|frigo|cama|cab-|arm-|estant|wc|lavabo|ducha|escrit|macetero/ then m = mobiliario
  elsif layer == "MUROS" then m = estuco
  elsif layer == "TABIQUES" then m = estucogr
  end

  e.entities.each { |f| f.material = m if f.is_a?(Sketchup::Face) && m } if m
end

"materials ok"