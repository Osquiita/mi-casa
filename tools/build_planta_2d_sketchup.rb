# -*- coding: utf-8 -*-
# ==============================================================================
# PLANOS 2D ARQUITECTÓNICOS EN SKETCHUP (ESTILO PLANO DE PRESENTACIÓN JPG)
# ==============================================================================

M = 1000.0
MODEL = Sketchup.active_model
ENTS  = MODEL.entities
MATS  = MODEL.materials
VIEW  = MODEL.active_view
CAM   = VIEW.camera
PAGES = MODEL.pages

def mm(v)
  v * M
end

ENTS.clear!

def get_mat(name, r, g, b, alpha=1.0)
  m = MATS[name] || MATS.add(name)
  m.color = Sketchup::Color.new(r, g, b)
  m.alpha = alpha if m.respond_to?(:alpha=)
  m
end

mat_salon    = get_mat("Suelo_Salon", 250, 246, 238)
mat_cocina   = get_mat("Suelo_Cocina", 244, 239, 230)
mat_porche   = get_mat("Suelo_Porche", 234, 229, 218)
mat_patio    = get_mat("Suelo_Patio", 234, 242, 232)
mat_agua     = get_mat("Suelo_Agua", 210, 232, 240)
mat_olivo    = get_mat("Vegetacion_Olivo", 184, 212, 168)
mat_banos    = get_mat("Suelo_Banos", 240, 245, 247)
mat_dorm     = get_mat("Suelo_Dormitorios", 250, 248, 245)
mat_cochera  = get_mat("Suelo_Cochera", 235, 236, 238)
mat_terraza  = get_mat("Suelo_Terraza", 235, 240, 242)
mat_muro     = get_mat("Muro_Poche_Negro", 28, 30, 33)
mat_mueble   = get_mat("Mueble_Madera", 217, 210, 197)
mat_cama     = get_mat("Mueble_Cama", 245, 242, 234)
mat_sofa     = get_mat("Mueble_Sofa", 210, 220, 224)
mat_mesa     = get_mat("Mueble_Mesa", 230, 222, 201)
mat_puerta   = get_mat("Carpinteria_Madera", 196, 109, 41)
mat_vidrio   = get_mat("Carpinteria_Vidrio", 58, 134, 200)
mat_corten   = get_mat("Carpinteria_Corten", 168, 75, 36)
mat_blanco   = get_mat("Sanitario_Blanco", 255, 255, 255)
mat_texto    = get_mat("Texto_Negro", 28, 30, 33)

def get_entities(target)
  target.respond_to?(:entities) ? target.entities : target
end

def draw_rect(parent, x1, y1, x2, y2, mat, z=0.0)
  es = get_entities(parent)
  g = es.add_group
  ges = g.entities
  pts = [
    Geom::Point3d.new(mm(x1), mm(y1), mm(z)),
    Geom::Point3d.new(mm(x2), mm(y1), mm(z)),
    Geom::Point3d.new(mm(x2), mm(y2), mm(z)),
    Geom::Point3d.new(mm(x1), mm(y2), mm(z))
  ]
  f = ges.add_face(pts)
  f.reverse! if f.normal.z < 0
  f.material = mat
  g
end

def draw_wall(parent, x1, y1, x2, y2, z_height=0.15)
  es = get_entities(parent)
  g = es.add_group
  ges = g.entities
  pts = [
    Geom::Point3d.new(mm(x1), mm(y1), 0),
    Geom::Point3d.new(mm(x2), mm(y1), 0),
    Geom::Point3d.new(mm(x2), mm(y2), 0),
    Geom::Point3d.new(mm(x1), mm(y2), 0)
  ]
  f = ges.add_face(pts)
  f.reverse! if f.normal.z < 0
  f.pushpull(mm(z_height))
  g.material = get_mat("Muro_Poche_Negro", 28, 30, 33)
  ges.each { |face| face.material = get_mat("Muro_Poche_Negro", 28, 30, 33) if face.is_a?(Sketchup::Face) }
  g
end

def draw_circle_face(parent, cx, cy, r, mat, z=0.0)
  es = get_entities(parent)
  g = es.add_group
  ges = g.entities
  circle = ges.add_circle(Geom::Point3d.new(mm(cx), mm(cy), mm(z)), Geom::Vector3d.new(0,0,1), mm(r), 24)
  f = ges.add_face(circle)
  f.material = mat
  g
end

def draw_arc_swing(parent, x0, y0, r, start_ang_deg, end_ang_deg, color_mat)
  es = get_entities(parent)
  g = es.add_group
  ges = g.entities
  n = 16
  pts = []
  (0..n).each do |i|
    ang = (start_ang_deg + i * (end_ang_deg - start_ang_deg) / n.to_f) * Math::PI / 180.0
    pts << Geom::Point3d.new(mm(x0 + r * Math.cos(ang)), mm(y0 + r * Math.sin(ang)), mm(0.02))
  end
  (0...(pts.size-1)).each do |i|
    edge = ges.add_line(pts[i], pts[i+1])
    edge.material = color_mat
  end
  g
end

def add_label(parent, text, cx, cy, size=0.28, bold=true, z=0.03)
  es = get_entities(parent)
  g = es.add_group
  # add_3d_text(string, align, font, is_bold, is_italic, letter_height, tolerance, z, is_filled, extrusion)
  g.entities.add_3d_text(text, TextAlignCenter, "Arial", bold, false, mm(size), 0.0, 0.0, true, 0.0)
  
  bb = g.bounds
  w_half = (bb.max.x - bb.min.x) / 2.0
  h_half = (bb.max.y - bb.min.y) / 2.0
  
  tr = Geom::Transformation.translation(Geom::Point3d.new(mm(cx) - w_half, mm(cy) - h_half, mm(z)))
  g.transform!(tr)
  g.material = get_mat("Texto_Negro", 28, 30, 33)
  g
end

def draw_window_2d(parent, x1, y1, x2, y2, mat_v)
  es = get_entities(parent)
  g = es.add_group
  dx = x2 - x1
  dy = y2 - y1
  if dx.abs > dy.abs
    draw_rect(g, x1, y1 - 0.05, x2, y1 + 0.05, mat_v, 0.16)
  else
    draw_rect(g, x1 - 0.05, y1, x1 + 0.05, y2, mat_v, 0.16)
  end
  g
end

# ==============================================================================
# 1. PLANTA BAJA (VIVIENDA A)
# ==============================================================================
pb_group = ENTS.add_group
pb_group.name = "PLANTA_BAJA_2D"

draw_rect(pb_group, 1.4, 0, 6.4, 7.4, mat_salon)
draw_rect(pb_group, 6.4, 0, 10.4, 5.0, mat_cocina)
draw_rect(pb_group, 6.4, 5.0, 11.4, 7.6, mat_porche)
draw_rect(pb_group, 6.4, 7.6, 11.4, 13.0, mat_patio)
draw_rect(pb_group, 6.8, 8.0, 8.6, 9.8, mat_agua, 0.01)
draw_circle_face(pb_group, 9.7, 9.6, 0.75, mat_olivo, 0.01)
draw_rect(pb_group, 10.4, 0, 11.4, 5.0, mat_cochera)
draw_rect(pb_group, 0, 0, 1.4, 13.0, mat_dorm)
draw_rect(pb_group, 1.4, 7.4, 6.4, 8.8, mat_banos)
draw_rect(pb_group, 1.4, 8.8, 6.4, 10.2, mat_banos)
draw_rect(pb_group, 1.4, 10.2, 6.4, 13.0, mat_dorm)
draw_rect(pb_group, 0, 14.1, 3.2, 17.6, mat_dorm)
draw_rect(pb_group, 3.2, 14.1, 6.4, 17.6, mat_dorm)
draw_rect(pb_group, 6.4, 13.0, 8.0, 17.6, mat_cochera)
draw_rect(pb_group, 8.0, 13.0, 11.4, 17.6, mat_cochera)

(0..16).each do |st|
  sy = st * (5.0 / 17.0)
  pb_group.entities.add_line(Geom::Point3d.new(mm(10.4), mm(sy), mm(0.02)), Geom::Point3d.new(mm(11.4), mm(sy), mm(0.02)))
end

draw_wall(pb_group, -0.15, -0.15, 0.15, 17.75)
draw_wall(pb_group, 11.25, -0.15, 11.55, 5.00)
draw_wall(pb_group, 11.25, 5.00, 11.55, 13.00)
draw_wall(pb_group, 11.25, 13.00, 11.55, 17.75)

draw_wall(pb_group, -0.15, -0.15, 0.30, 0.15)
draw_wall(pb_group, 1.30, -0.15, 2.60, 0.15)
draw_wall(pb_group, 4.40, -0.15, 4.80, 0.15)
draw_wall(pb_group, 6.00, -0.15, 6.90, 0.15)
draw_wall(pb_group, 8.10, -0.15, 8.90, 0.15)
draw_wall(pb_group, 9.90, -0.15, 10.40, 0.15)

draw_wall(pb_group, -0.15, 17.45, 0.80, 17.75)
draw_wall(pb_group, 2.40, 17.45, 3.60, 17.75)
draw_wall(pb_group, 5.20, 17.45, 8.00, 17.75)

draw_wall(pb_group, 1.35, 0, 1.45, 1.4)
draw_wall(pb_group, 1.35, 4.6, 1.45, 6.1)
draw_wall(pb_group, 1.35, 6.8, 1.45, 7.9)
draw_wall(pb_group, 1.35, 8.6, 1.45, 13.0)
draw_wall(pb_group, 6.35, 0, 6.45, 1.0)
draw_wall(pb_group, 6.35, 4.4, 6.45, 5.0)
draw_wall(pb_group, 10.35, 0, 10.45, 5.0)
draw_wall(pb_group, 6.25, 7.4, 6.55, 13.0)
draw_wall(pb_group, 1.4, 7.35, 6.4, 7.45)
draw_wall(pb_group, 1.4, 8.75, 6.4, 8.85)
draw_wall(pb_group, 1.4, 10.15, 3.3, 10.25)
draw_wall(pb_group, 4.0, 10.15, 6.4, 10.25)
draw_wall(pb_group, 1.4, 12.95, 2.2, 13.05)
draw_wall(pb_group, 2.9, 12.95, 8.0, 13.05)
draw_wall(pb_group, 0, 14.05, 0.8, 14.15)
draw_wall(pb_group, 1.5, 14.05, 3.6, 14.15)
draw_wall(pb_group, 4.3, 14.05, 6.4, 14.15)
draw_wall(pb_group, 3.15, 14.1, 3.25, 17.6)
draw_wall(pb_group, 6.35, 13.0, 6.45, 17.6)
draw_wall(pb_group, 7.95, 13.0, 8.05, 13.3)
draw_wall(pb_group, 7.95, 13.9, 8.05, 17.6)

draw_wall(pb_group, 6.9, 7.45, 7.15, 7.70)
draw_wall(pb_group, 9.5, 7.45, 9.75, 7.70)

draw_window_2d(pb_group, 2.6, 0, 4.4, 0, mat_vidrio)
draw_window_2d(pb_group, 4.8, 0, 6.0, 0, mat_vidrio)
draw_window_2d(pb_group, 6.9, 0, 8.1, 0, mat_vidrio)
draw_window_2d(pb_group, 8.9, 0, 9.9, 0, mat_vidrio)
draw_window_2d(pb_group, 6.4, 5.0, 6.4, 7.4, mat_vidrio)
draw_window_2d(pb_group, 6.4, 7.8, 6.4, 8.4, mat_vidrio)
draw_window_2d(pb_group, 6.4, 9.0, 6.4, 9.6, mat_vidrio)
draw_window_2d(pb_group, 6.4, 11.0, 6.4, 12.2, mat_vidrio)
draw_window_2d(pb_group, 0.8, 17.6, 2.4, 17.6, mat_vidrio)
draw_window_2d(pb_group, 3.6, 17.6, 5.2, 17.6, mat_vidrio)
draw_window_2d(pb_group, 8.0, 17.6, 11.4, 17.6, mat_corten)

draw_arc_swing(pb_group, 0.3, 0, 0.9, 0, 90, mat_puerta)
draw_arc_swing(pb_group, 10.4, 0, 0.9, 0, 90, mat_puerta)
draw_arc_swing(pb_group, 1.4, 7.9, 0.7, 0, 90, mat_puerta)
draw_arc_swing(pb_group, 3.3, 10.2, 0.7, -90, 0, mat_puerta)
draw_arc_swing(pb_group, 2.2, 13.0, 0.7, 0, 90, mat_puerta)
draw_arc_swing(pb_group, 0.8, 14.1, 0.7, 0, 90, mat_puerta)
draw_arc_swing(pb_group, 3.6, 14.1, 0.7, 0, 90, mat_puerta)

draw_rect(pb_group, 1.8, 1.2, 4.6, 2.3, mat_sofa, 0.02)
draw_rect(pb_group, 2.0, 3.8, 4.2, 4.8, mat_mesa, 0.02)
draw_rect(pb_group, 2.6, 6.8, 4.8, 7.15, mat_mueble, 0.02)
draw_rect(pb_group, 7.0, 1.8, 9.4, 2.9, mat_blanco, 0.02)
draw_rect(pb_group, 6.5, 0.15, 10.2, 0.75, mat_mueble, 0.02)
draw_rect(pb_group, 1.6, 7.5, 2.8, 7.95, mat_blanco, 0.02)
draw_rect(pb_group, 1.6, 8.9, 2.8, 9.35, mat_blanco, 0.02)
draw_rect(pb_group, 5.4, 7.5, 6.3, 8.7, mat_blanco, 0.02)
draw_rect(pb_group, 5.4, 8.9, 6.3, 10.1, mat_blanco, 0.02)
draw_rect(pb_group, 3.8, 10.5, 5.6, 12.4, mat_cama, 0.02)
draw_rect(pb_group, 1.55, 10.5, 2.15, 12.7, mat_mueble, 0.02)
draw_rect(pb_group, 0.4, 15.0, 1.8, 16.9, mat_cama, 0.02)
draw_rect(pb_group, 3.6, 15.0, 5.0, 16.9, mat_cama, 0.02)
draw_rect(pb_group, 8.6, 14.2, 10.7, 17.1, mat_sofa, 0.02)

add_label(pb_group, "SALON - COMEDOR\n37,0 m2", 3.9, 2.6, 0.32)
add_label(pb_group, "COCINA CON ISLA\n20,0 m2", 8.4, 3.6, 0.32)
add_label(pb_group, "PORCHE CUBIERTO\n13,0 m2", 8.9, 6.3, 0.30)
add_label(pb_group, "PATIO CENTRAL\n27,0 m2", 8.9, 11.4, 0.32)
add_label(pb_group, "LAMINA\nAGUA", 7.7, 8.9, 0.22)
add_label(pb_group, "OLIVO", 9.7, 9.6, 0.22)
add_label(pb_group, "BANO COMUN\n7,0 m2", 3.9, 8.1, 0.26)
add_label(pb_group, "BANO SUITE\n7,0 m2", 3.9, 9.5, 0.26)
add_label(pb_group, "DORMITORIO PPAL\n14,0 m2", 2.8, 11.6, 0.28)
add_label(pb_group, "DORMITORIO 2\n11,2 m2", 1.6, 16.2, 0.28)
add_label(pb_group, "DORMITORIO 3\n11,2 m2", 4.8, 16.2, 0.28)
add_label(pb_group, "TRASTERO\n7,4 m2", 7.2, 15.3, 0.26)
add_label(pb_group, "COCHERA\n15,6 m2", 9.7, 15.6, 0.30)
add_label(pb_group, "PORTAL A", 0.8, -0.5, 0.26)
add_label(pb_group, "PORTAL B", 10.9, -0.5, 0.26)

add_label(pb_group, "PLANTA BAJA (VIVIENDA A) - ESCALA 1:50", 5.7, -1.6, 0.45)
draw_rect(pb_group, 0, -3.2, 11.4, -2.2, mat_blanco, 0.01)
add_label(pb_group, "PROYECTO RESIDENCIAL - PALMA DEL RIO (CORDOBA)\nLAMINA 2D-01 | PLANTA BAJA (VIVIENDA A) | SUP. UTIL: 133,4 m2", 5.7, -2.7, 0.24)

# ==============================================================================
# 2. PLANTA ALTA (VIVIENDA B) AL LADO EN X: 14.0 -> 25.40 m
# ==============================================================================
pa_group = ENTS.add_group
pa_group.name = "PLANTA_ALTA_2D"
OX = 14.0

draw_rect(pa_group, OX + 1.4, 0, OX + 6.4, 7.4, mat_salon)
draw_rect(pa_group, OX + 6.4, 5.0, OX + 11.4, 7.6, mat_salon)
draw_rect(pa_group, OX + 6.4, 0, OX + 10.4, 5.0, mat_cocina)
draw_rect(pa_group, OX + 6.4, 7.6, OX + 11.4, 13.0, mat_terraza)
draw_rect(pa_group, OX + 10.4, 0, OX + 11.4, 5.0, mat_cochera)
draw_rect(pa_group, OX + 0, 0, OX + 1.4, 13.0, mat_dorm)
draw_rect(pa_group, OX + 1.4, 7.4, OX + 6.4, 8.8, mat_banos)
draw_rect(pa_group, OX + 1.4, 8.8, OX + 6.4, 10.2, mat_banos)
draw_rect(pa_group, OX + 1.4, 10.2, OX + 6.4, 13.0, mat_dorm)
draw_rect(pa_group, OX + 0, 14.1, OX + 3.2, 17.6, mat_terraza)
draw_rect(pa_group, OX + 3.2, 14.1, OX + 6.4, 17.6, mat_dorm)
draw_rect(pa_group, OX + 6.4, 13.0, OX + 11.4, 17.6, mat_dorm)

(0..16).each do |st|
  sy = st * (5.0 / 17.0)
  pa_group.entities.add_line(Geom::Point3d.new(mm(OX + 10.4), mm(sy), mm(0.02)), Geom::Point3d.new(mm(OX + 11.4), mm(sy), mm(0.02)))
end

draw_wall(pa_group, OX - 0.15, -0.15, OX + 0.15, 17.75)
draw_wall(pa_group, OX + 11.25, -0.15, OX + 11.55, 17.75)
draw_wall(pa_group, OX - 0.15, -0.15, OX + 2.60, 0.15)
draw_wall(pa_group, OX + 6.00, -0.40, OX + 6.60, -0.10)
draw_wall(pa_group, OX + 9.90, -0.15, OX + 10.40, 0.15)
draw_wall(pa_group, OX + 3.20, 17.45, OX + 3.60, 17.75)
draw_wall(pa_group, OX + 5.20, 17.45, OX + 7.00, 17.75)
draw_wall(pa_group, OX + 11.20, 17.45, OX + 11.55, 17.75)

draw_wall(pa_group, OX + 10.35, 0, OX + 10.45, 5.0)
draw_wall(pa_group, OX + 6.35, 7.6, OX + 6.45, 13.0)
draw_wall(pa_group, OX + 6.4, 7.5, OX + 11.4, 7.6)
draw_wall(pa_group, OX + 6.4, 12.95, OX + 7.0, 13.05)
draw_wall(pa_group, OX + 10.4, 12.95, OX + 11.4, 13.05)
draw_wall(pa_group, OX + 1.4, 7.35, OX + 6.4, 7.45)
draw_wall(pa_group, OX + 1.4, 8.75, OX + 6.4, 8.85)
draw_wall(pa_group, OX + 1.4, 10.15, OX + 3.3, 10.25)
draw_wall(pa_group, OX + 4.0, 10.15, OX + 6.4, 10.25)
draw_wall(pa_group, OX + 1.4, 12.95, OX + 2.2, 13.05)
draw_wall(pa_group, OX + 2.9, 12.95, OX + 6.4, 13.05)
draw_wall(pa_group, OX + 0, 14.05, OX + 0.8, 14.15)
draw_wall(pa_group, OX + 1.5, 14.05, OX + 3.6, 14.15)
draw_wall(pa_group, OX + 4.3, 14.05, OX + 6.4, 14.15)
draw_wall(pa_group, OX + 3.15, 14.1, OX + 3.25, 17.6)

draw_window_2d(pa_group, OX + 2.6, -0.40, OX + 6.0, -0.40, mat_vidrio)
draw_window_2d(pa_group, OX + 6.6, -0.40, OX + 9.9, -0.40, mat_vidrio)
draw_window_2d(pa_group, OX + 6.4, 5.0, OX + 6.4, 7.6, mat_vidrio)
draw_window_2d(pa_group, OX + 7.0, 17.6, OX + 11.2, 17.6, mat_vidrio)
draw_window_2d(pa_group, OX + 7.0, 13.0, OX + 10.4, 13.0, mat_vidrio)
draw_window_2d(pa_group, OX + 3.6, 17.6, OX + 5.2, 17.6, mat_vidrio)

draw_rect(pa_group, OX + 1.8, 1.2, OX + 4.8, 2.3, mat_sofa, 0.02)
draw_rect(pa_group, OX + 2.0, 3.8, OX + 4.2, 4.8, mat_mesa, 0.02)
draw_rect(pa_group, OX + 7.0, 5.3, OX + 8.8, 6.2, mat_mesa, 0.02)
draw_rect(pa_group, OX + 7.0, 1.8, OX + 9.4, 2.9, mat_blanco, 0.02)
draw_rect(pa_group, OX + 3.8, 10.5, OX + 5.6, 12.4, mat_cama, 0.02)
draw_rect(pa_group, OX + 3.6, 15.0, OX + 5.0, 16.9, mat_cama, 0.02)
draw_rect(pa_group, OX + 7.2, 15.0, OX + 9.0, 16.9, mat_cama, 0.02)
draw_rect(pa_group, OX + 10.4, 13.2, OX + 11.1, 17.2, mat_mueble, 0.02)
draw_rect(pa_group, OX + 6.8, 13.3, OX + 8.4, 14.0, mat_mesa, 0.02)

add_label(pa_group, "SALON - COMEDOR DIAFANO\n50,0 m2", OX + 3.9, 2.6, 0.32)
add_label(pa_group, "COCINA PA\n20,0 m2", OX + 8.4, 3.6, 0.32)
add_label(pa_group, "ZONA LECTURA\n/ ESTUDIO", OX + 7.9, 5.75, 0.24)
add_label(pa_group, "VACIO SOBRE PATIO\n(DOBLE ALTURA - 27 m2)", OX + 8.9, 10.3, 0.30)
add_label(pa_group, "BANO COMUN\n7,0 m2", OX + 3.9, 8.1, 0.26)
add_label(pa_group, "BANO SUITE\n7,0 m2", OX + 3.9, 9.5, 0.26)
add_label(pa_group, "DORMITORIO PPAL\n14,0 m2", OX + 2.8, 11.6, 0.28)
add_label(pa_group, "TERRAZA PRIVADA\n11,2 m2", OX + 1.6, 15.8, 0.28)
add_label(pa_group, "DORMITORIO 3\n11,2 m2", OX + 4.8, 16.2, 0.28)
add_label(pa_group, "GRAN SUITE PRINCIPAL\n23,0 m2 (VESTIDOR 4m)", OX + 8.9, 14.3, 0.30)

add_label(pa_group, "PLANTA ALTA (VIVIENDA B) - ESCALA 1:50", OX + 5.7, -1.6, 0.45)
draw_rect(pa_group, OX, -3.2, OX + 11.4, -2.2, mat_blanco, 0.01)
add_label(pa_group, "PROYECTO RESIDENCIAL - PALMA DEL RIO (CORDOBA)\nLAMINA 2D-02 | PLANTA ALTA (VIVIENDA B) | SUP. UTIL: 132,2 m2", OX + 5.7, -2.7, 0.24)

# ------------------------------------------------------------------------------
# ESCENAS
# ------------------------------------------------------------------------------
CAM.perspective = false

# Escena 1: Vista General Lado a Lado
CAM.set(
  Geom::Point3d.new(12700.0, 7500.0, 45000.0),
  Geom::Point3d.new(12700.0, 7500.0, 0.0),
  Geom::Vector3d.new(0, 1, 0)
)
VIEW.zoom_extents
p_gen = PAGES["01_PLANO_GENERAL_2D"] || PAGES.add("01_PLANO_GENERAL_2D")
p_gen.update(127)

# Escena 2: Planta Baja
CAM.set(
  Geom::Point3d.new(5700.0, 7500.0, 30000.0),
  Geom::Point3d.new(5700.0, 7500.0, 0.0),
  Geom::Vector3d.new(0, 1, 0)
)
p_pb = PAGES["02_PLANTA_BAJA_2D"] || PAGES.add("02_PLANTA_BAJA_2D")
p_pb.update(127)

# Escena 3: Planta Alta
CAM.set(
  Geom::Point3d.new(OX + 5700.0, 7500.0, 30000.0),
  Geom::Point3d.new(OX + 5700.0, 7500.0, 0.0),
  Geom::Vector3d.new(0, 1, 0)
)
p_pa = PAGES["03_PLANTA_ALTA_2D"] || PAGES.add("03_PLANTA_ALTA_2D")
p_pa.update(127)

PAGES.selected_page = p_pb
VIEW.refresh

MODEL.save("C:/Users/Oscar Martinez/Desktop/mi-casa/casa-bifamiliar-3d.skp")
"PLANOS 2D ARQUITECTONICOS GENERADOS EN SKETCHUP CON EXITO"
