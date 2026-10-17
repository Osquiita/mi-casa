# -*- coding: utf-8 -*-
# ==============================================================================
# MODELO 3D BIFAMILIAR COMPLETO - PLANTA BAJA, PLANTA ALTA Y CUBIERTAS
# ==============================================================================

M = 1000.0
MODEL = Sketchup.active_model
ENTS  = MODEL.entities
LAYERS = MODEL.layers
MATS  = MODEL.materials
VIEW  = MODEL.active_view
CAM   = VIEW.camera
PAGES = MODEL.pages

def mm(v); v * M; end

ENTS.clear!

def get_layer(name)
  LAYERS[name] || LAYERS.add(name)
end

lay_pb_muros   = get_layer("01_PB_MUROS")
lay_pb_suelos  = get_layer("02_PB_SUELOS")
lay_pb_muebles = get_layer("03_PB_MUEBLES")
lay_patio      = get_layer("04_PATIO_PISCINA")
lay_pa_muros   = get_layer("05_PA_MUROS")
lay_pa_suelos  = get_layer("06_PA_SUELOS")
lay_pa_muebles = get_layer("07_PA_MUEBLES")
lay_cubiertas  = get_layer("08_CUBIERTAS")

LAYERS.each { |l| l.visible = true }

def get_mat(name, r, g, b, alpha=1.0)
  m = MATS[name] || MATS.add(name)
  m.color = Sketchup::Color.new(r, g, b)
  m.alpha = alpha
  m
end

mat_muro    = get_mat("Muro_Blanco", 242, 242, 244)
mat_muro_t  = get_mat("Muro_Top_Gris", 35, 38, 42)
mat_salon   = get_mat("Suelo_Salon", 250, 248, 245)
mat_cocina  = get_mat("Suelo_Cocina", 245, 242, 236)
mat_patio   = get_mat("Suelo_Patio", 236, 253, 245)
mat_agua    = get_mat("Suelo_Agua", 146, 211, 240, 0.85)
mat_dorm    = get_mat("Suelo_Dormitorios", 252, 250, 247)
mat_madera  = get_mat("Mobiliario_Madera", 196, 109, 41)
mat_antrac  = get_mat("Mobiliario_Antracita", 51, 65, 85)
mat_sofa    = get_mat("Mobiliario_Sofa", 210, 220, 224)
mat_cama    = get_mat("Mobiliario_Cama", 248, 250, 252)
mat_vidrio  = get_mat("Vidrio", 14, 165, 233, 0.40)
mat_solar   = get_mat("Paneles_Solares", 30, 58, 138)
mat_grava   = get_mat("Grava_Cubierta", 203, 213, 225)

def add_box(x1, y1, z1, x2, y2, z2, mat, name, lay)
  g = ENTS.add_group
  g.name = name
  g.layer = lay
  pts = [
    Geom::Point3d.new(mm(x1), mm(y1), mm(z1)),
    Geom::Point3d.new(mm(x2), mm(y1), mm(z1)),
    Geom::Point3d.new(mm(x2), mm(y2), mm(z1)),
    Geom::Point3d.new(mm(x1), mm(y2), mm(z1))
  ]
  f = g.entities.add_face(pts)
  f.reverse! if f.normal.z < 0
  h = z2 - z1
  f.pushpull(mm(h)) if h.abs > 0.001
  g.entities.each { |face| face.material = mat if face.is_a?(Sketchup::Face) }
  g
end

# 1. PLANTA BAJA (Z = 0.00 a 1.20 m para visualización maqueta)
# Suelos PB
add_box(0.00, 0.00, 0.00, 6.40, 7.40, 0.01, mat_salon, "Suelo_Salon_PB", lay_pb_suelos)
add_box(6.40, 0.00, 0.00, 10.40, 5.00, 0.01, mat_cocina, "Suelo_Cocina_PB", lay_pb_suelos)
add_box(10.40, 0.00, 0.00, 11.40, 5.00, 0.01, mat_salon, "Suelo_Escalera_PB", lay_pb_suelos)
add_box(6.40, 5.00, 0.00, 11.40, 7.40, 0.01, mat_salon, "Suelo_Porche_PB", lay_pb_suelos)
add_box(6.40, 7.40, 0.00, 11.40, 13.00, 0.01, mat_patio, "Suelo_Patio_PB", lay_patio)
add_box(7.30, 8.20, -1.40, 9.80, 12.00, 0.00, mat_agua, "Piscina_PB", lay_patio)
add_box(0.00, 7.40, 0.00, 6.40, 13.50, 0.01, mat_dorm, "Suelo_Suite_Banos_PB", lay_pb_suelos)
add_box(0.00, 13.50, 0.00, 6.40, 17.60, 0.01, mat_dorm, "Suelo_Dormitorios_PB", lay_pb_suelos)
add_box(6.40, 13.00, 0.00, 11.40, 17.60, 0.01, mat_antrac, "Suelo_Cochera_PB", lay_pb_suelos)

# Muros PB (altura 1.20 m)
PB_H = 1.20
# Medianeras
add_box(-0.15, -0.15, 0.00, 0.15, 17.75, PB_H, mat_muro, "Med_Oeste_PB", lay_pb_muros)
add_box(11.25, -0.15, 0.00, 11.55, 17.75, PB_H, mat_muro, "Med_Este_PB", lay_pb_muros)
# Fachada Sur
add_box(-0.15, -0.15, 0.00, 2.60, 0.15, PB_H, mat_muro, "Fach_Sur_1_PB", lay_pb_muros)
add_box(4.40, -0.15, 0.00, 6.90, 0.15, PB_H, mat_muro, "Fach_Sur_2_PB", lay_pb_muros)
add_box(8.10, -0.15, 0.00, 10.40, 0.15, PB_H, mat_muro, "Fach_Sur_3_PB", lay_pb_muros)
# Fachada Norte
add_box(-0.15, 17.45, 0.00, 0.80, 17.75, PB_H, mat_muro, "Fach_Norte_1_PB", lay_pb_muros)
add_box(2.40, 17.45, 0.00, 3.60, 17.75, PB_H, mat_muro, "Fach_Norte_2_PB", lay_pb_muros)
add_box(5.20, 17.45, 0.00, 6.40, 17.75, PB_H, mat_muro, "Fach_Norte_3_PB", lay_pb_muros)
# Muro Cochera y Patio
add_box(6.30, 13.00, 0.00, 6.50, 17.60, PB_H, mat_muro, "Muro_Cochera_PB", lay_pb_muros)
add_box(6.30, 7.35, 0.00, 6.50, 13.00, PB_H, mat_muro, "Muro_Patio_PB", lay_pb_muros)

# Mobiliario Clave PB
add_box(1.80, 2.60, 0.00, 4.60, 3.70, 0.65, mat_sofa, "Sofa_PB", lay_pb_muebles)
add_box(7.00, 1.70, 0.00, 9.40, 2.80, 0.90, mat_antrac, "Isla_Cocina_PB", lay_pb_muebles)
add_box(1.95, 10.75, 0.00, 3.95, 12.70, 0.55, mat_cama, "Cama_Suite_PB", lay_pb_muebles)
add_box(6.80, 13.80, 0.00, 9.80, 17.20, 0.60, mat_antrac, "SUV_Garaje_PB", lay_pb_muebles)

# 2. PLANTA ALTA (Z = 2.90 a 4.10 m)
PA_Z = 2.90
PA_H = 1.20
# Forjado planta primera
add_box(0.00, 0.00, PA_Z - 0.25, 11.40, 7.40, PA_Z, mat_muro_t, "Forjado_PA_Sur", lay_pa_suelos)
add_box(0.00, 7.40, PA_Z - 0.25, 6.40, 17.60, PA_Z, mat_muro_t, "Forjado_PA_Oeste", lay_pa_suelos)
add_box(6.40, 13.00, PA_Z - 0.25, 11.40, 17.60, PA_Z, mat_muro_t, "Forjado_PA_Dorm2", lay_pa_suelos)

# Suelos PA
add_box(0.00, 0.00, PA_Z, 11.40, 7.40, PA_Z + 0.01, mat_salon, "Suelo_Gran_Salon_PA", lay_pa_suelos)
add_box(0.00, 7.40, PA_Z, 6.40, 13.50, PA_Z + 0.01, mat_dorm, "Suelo_Suite_PA", lay_pa_suelos)
add_box(6.40, 13.00, PA_Z, 11.40, 17.60, PA_Z + 0.01, mat_dorm, "Suelo_Dorm2_PA", lay_pa_suelos)
add_box(3.20, 13.80, PA_Z, 6.40, 17.60, PA_Z + 0.01, mat_dorm, "Suelo_Dorm3_PA", lay_pa_suelos)
add_box(0.00, 13.80, PA_Z, 3.20, 17.60, PA_Z + 0.01, mat_madera, "Suelo_Terraza_PA", lay_pa_suelos)

# Muros PA
add_box(-0.15, -0.15, PA_Z, 0.15, 17.75, PA_Z + PA_H, mat_muro, "Med_Oeste_PA", lay_pa_muros)
add_box(11.25, -0.15, PA_Z, 11.55, 17.75, PA_Z + PA_H, mat_muro, "Med_Este_PA", lay_pa_muros)
add_box(-0.15, -0.15, PA_Z, 2.60, 0.15, PA_Z + PA_H, mat_muro, "Fach_Sur_1_PA", lay_pa_muros)
add_box(4.40, -0.15, PA_Z, 6.90, 0.15, PA_Z + PA_H, mat_muro, "Fach_Sur_2_PA", lay_pa_muros)
add_box(8.10, -0.15, PA_Z, 11.40, 0.15, PA_Z + PA_H, mat_muro, "Fach_Sur_3_PA", lay_pa_muros)

# Barandilla hacia vacío patio en PA (Vidrio laminar h=1.10 m)
add_box(6.40, 7.40, PA_Z, 11.40, 7.45, PA_Z + 1.10, mat_vidrio, "Barandilla_Patio_PA_Sur", lay_pa_muros)
add_box(6.40, 7.40, PA_Z, 6.45, 13.00, PA_Z + 1.10, mat_vidrio, "Barandilla_Patio_PA_Oeste", lay_pa_muros)
add_box(6.40, 12.95, PA_Z, 11.40, 13.00, PA_Z + 1.10, mat_vidrio, "Barandilla_Patio_PA_Norte", lay_pa_muros)

# Mobiliario PA
add_box(1.80, 2.60, PA_Z, 4.60, 3.70, PA_Z + 0.65, mat_sofa, "Sofa_PA", lay_pa_muebles)
add_box(7.20, 5.40, PA_Z, 9.80, 6.40, PA_Z + 0.65, mat_sofa, "Estar_Vistas_Patio_PA", lay_pa_muebles)
add_box(1.95, 10.75, PA_Z, 3.95, 12.70, PA_Z + 0.55, mat_cama, "Cama_Suite_PA", lay_pa_muebles)
add_box(7.20, 14.50, PA_Z, 9.00, 16.50, PA_Z + 0.55, mat_cama, "Cama_Dorm2_PA", lay_pa_muebles)

# 3. CUBIERTA (Z = 5.80 m con paneles solares)
CUB_Z = 5.80
add_box(0.00, 0.00, CUB_Z - 0.30, 11.40, 7.40, CUB_Z, mat_grava, "Cubierta_Sur", lay_cubiertas)
add_box(0.00, 7.40, CUB_Z - 0.30, 6.40, 17.60, CUB_Z, mat_grava, "Cubierta_Oeste", lay_cubiertas)
add_box(6.40, 13.00, CUB_Z - 0.30, 11.40, 17.60, CUB_Z, mat_grava, "Cubierta_Norte", lay_cubiertas)

# Paneles Solares Fotovoltaicos en Cubierta Sur
for i in range(5):
  for j in range(2):
    px = 1.00 + i * 1.05
    py = 3.80 + j * 1.80
    add_box(px, py, CUB_Z + 0.15, px + 0.95, py + 1.60, CUB_Z + 0.35, mat_solar, "Panel_Solar", lay_cubiertas)
  end
end

# 4. Escenas Oficiales
PAGES.to_a.each { |p| PAGES.erase(p) }

# Escena 1: Planta Baja
CAM.perspective = false
cx = mm(5.70); cy = mm(8.80)
CAM.set(Geom::Point3d.new(cx, cy, mm(45.0)), Geom::Point3d.new(cx, cy, 0.0), Geom::Vector3d.new(0, 1, 0))
VIEW.zoom_extents
p1 = PAGES.add("01_PLANTA_BAJA_2D")
p1.update(127)

# Escena 2: Planta Alta
p2 = PAGES.add("02_PLANTA_ALTA_2D")
p2.update(127)

# Escena 3: Perspectiva 3D Completa
CAM.perspective = true
CAM.fov = 45.0
CAM.set(Geom::Point3d.new(mm(19.0), mm(-9.0), mm(16.0)), Geom::Point3d.new(cx, cy, mm(2.5)), Geom::Vector3d.new(0, 0, 1))
p3 = PAGES.add("03_PERSPECTIVA_3D_EXTERIOR")
p3.update(127)

# Escena 4: Vista Patio y Piscina
CAM.set(Geom::Point3d.new(mm(-3.0), mm(21.0), mm(14.0)), Geom::Point3d.new(mm(8.90), mm(10.0), mm(1.5)), Geom::Vector3d.new(0, 0, 1))
p4 = PAGES.add("04_VISTA_PATIO_PISCINA")
p4.update(127)

PAGES.selected_page = p3
VIEW.refresh

skp_path = "C:/Users/Oscar Martinez/Desktop/mi-casa/casa-bifamiliar-3d.skp"
MODEL.save(skp_path)

"MODELO 3D BIFAMILIAR COMPLETO (PB+PA+CUBIERTA) INYECTADO: #{ENTS.count} entidades creadas."
