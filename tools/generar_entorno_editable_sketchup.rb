# -*- coding: utf-8 -*-
# ==============================================================================
# ENTORNO EDITABLE SKETCHUP - VERSIÓN 5 (MASTER SUITE + ALMACENAJE INTEGRADO SALÓN)
# ==============================================================================

M = 1000.0
MODEL = Sketchup.active_model
ENTS  = MODEL.entities
LAYERS = MODEL.layers
MATS  = MODEL.materials
VIEW  = MODEL.active_view
CAM   = VIEW.camera
PAGES = MODEL.pages

def mm(v)
  v * M
end

ENTS.clear!

def get_layer(name)
  LAYERS[name] || LAYERS.add(name)
end

lay_guia    = get_layer("00_PLANO_GUIA_PNG")
lay_muros   = get_layer("01_MUROS_EDITABLES")
lay_suelos  = get_layer("02_SUELOS_ZONAS")
lay_piscina = get_layer("03_PISCINA_PATIO")
lay_muebles = get_layer("04_MOBILIARIO_ALMACENAJE")

def get_mat(name, r, g, b, alpha=1.0)
  m = MATS[name] || MATS.add(name)
  m.color = Sketchup::Color.new(r, g, b)
  m.alpha = alpha
  m
end

mat_muro    = get_mat("Muro_Blanco_Editable", 242, 242, 244)
mat_muro_t  = get_mat("Muro_Top_GrisOscuro", 45, 48, 52)
mat_salon   = get_mat("Suelo_Salon", 250, 246, 238)
mat_cocina  = get_mat("Suelo_Cocina", 244, 239, 230)
mat_porche  = get_mat("Suelo_Porche", 234, 229, 218)
mat_patio   = get_mat("Suelo_Patio", 234, 242, 232)
mat_agua    = get_mat("Suelo_Piscina_Agua", 146, 211, 240, 0.85)
mat_banos   = get_mat("Suelo_Banos", 240, 245, 247)
mat_dorm    = get_mat("Suelo_Dormitorios", 250, 248, 245)
mat_hall    = get_mat("Suelo_Hall_Pasillo", 245, 243, 239)
mat_cochera = get_mat("Suelo_Cochera", 235, 236, 238)
mat_madera  = get_mat("Mobiliario_Madera_Roble", 196, 109, 41)
mat_sofa    = get_mat("Mobiliario_Sofa", 210, 220, 224)
mat_cama    = get_mat("Mobiliario_Cama", 245, 242, 234)

# 1. Plano Guía de Fondo (Bloqueado)
pb_path = "C:/Users/Oscar Martinez/Desktop/mi-casa/entrega/planos_2d/01_plano_2d_planta_baja.png"
if File.exist?(pb_path)
  g_img = ENTS.add_group
  g_img.name = "PLANO_GUIA_FONDO (Desbloquear si deseas moverlo)"
  g_img.layer = lay_guia
  img_pb = g_img.entities.add_image(pb_path, Geom::Point3d.new(mm(-1.5), mm(-3.8), -10.0), mm(14.4))
  g_img.locked = true
end

# 2. Suelos por Zonas
def add_floor_zone(x1, y1, x2, y2, mat, name, lay)
  g = ENTS.add_group
  g.name = name
  g.layer = lay
  pts = [
    Geom::Point3d.new(mm(x1), mm(y1), 0),
    Geom::Point3d.new(mm(x2), mm(y1), 0),
    Geom::Point3d.new(mm(x2), mm(y2), 0),
    Geom::Point3d.new(mm(x1), mm(y2), 0)
  ]
  f = g.entities.add_face(pts)
  f.reverse! if f.normal.z < 0
  f.material = mat
  g
end

add_floor_zone(0.00, 0.00, 1.20, 2.40, mat_hall, "Suelo_Hall_Entrada", lay_suelos)
add_floor_zone(0.00, 2.40, 6.40, 7.40, mat_salon, "Suelo_Salon_Almacenaje", lay_suelos)
add_floor_zone(1.20, 0.00, 6.40, 2.40, mat_salon, "Suelo_Comedor_Sur", lay_suelos)
add_floor_zone(6.40, 0.00, 10.40, 5.00, mat_cocina, "Suelo_Cocina", lay_suelos)
add_floor_zone(10.40, 0.00, 11.40, 5.00, mat_cochera, "Suelo_Escalera_PA", lay_suelos)
add_floor_zone(6.40, 5.00, 11.40, 7.40, mat_porche, "Suelo_Porche_Cubierto", lay_suelos)
add_floor_zone(6.40, 7.40, 11.40, 13.00, mat_patio, "Suelo_Patio", lay_suelos)
add_floor_zone(7.30, 8.20, 9.80, 12.00, mat_agua, "Piscina_Privada_2.50x3.80", lay_piscina)
add_floor_zone(0.00, 7.40, 1.20, 13.50, mat_hall, "Suelo_Pasillo_Noche", lay_suelos)
add_floor_zone(1.20, 12.55, 4.30, 13.50, mat_hall, "Suelo_Rellano_Dorms", lay_suelos)
add_floor_zone(1.20, 7.40, 3.80, 9.80, mat_banos, "Suelo_Bano_Comun", lay_suelos)
add_floor_zone(3.80, 7.40, 6.40, 9.80, mat_banos, "Suelo_Bano_Suite", lay_suelos)
add_floor_zone(1.20, 9.80, 4.30, 12.55, mat_dorm, "Suelo_MasterSuite_Cama", lay_suelos)
add_floor_zone(4.30, 9.80, 6.40, 13.45, mat_dorm, "Suelo_MasterSuite_GranVestidor", lay_suelos)
add_floor_zone(0.00, 13.50, 3.20, 17.60, mat_dorm, "Suelo_Dormitorio_2", lay_suelos)
add_floor_zone(3.20, 13.50, 6.40, 17.60, mat_dorm, "Suelo_Dormitorio_3", lay_suelos)
add_floor_zone(6.40, 13.00, 11.40, 17.60, mat_cochera, "Suelo_Gran_Cochera", lay_suelos)

# 3. Muros como Grupos 3D Editables
WALL_H = 1.20

def add_wall_part(x1, y1, x2, y2, height=WALL_H, name="Muro")
  g = ENTS.add_group
  g.name = name
  g.layer = LAYERS["01_MUROS_EDITABLES"]
  
  pts = [
    Geom::Point3d.new(mm(x1), mm(y1), 0),
    Geom::Point3d.new(mm(x2), mm(y1), 0),
    Geom::Point3d.new(mm(x2), mm(y2), 0),
    Geom::Point3d.new(mm(x1), mm(y2), 0)
  ]
  f = g.entities.add_face(pts)
  f.reverse! if f.normal.z < 0
  f.pushpull(mm(height))
  
  mat_w = MATS["Muro_Blanco_Editable"]
  mat_t = MATS["Muro_Top_GrisOscuro"]
  
  g.entities.each do |face|
    next unless face.is_a?(Sketchup::Face)
    if face.normal.z > 0.9
      face.material = mat_t
    else
      face.material = mat_w
    end
  end
  g
end

# Medianeras
add_wall_part(-0.15, -0.15, 0.15, 17.75, WALL_H, "Medianera_Oeste (17.60m)")
add_wall_part(11.25, -0.15, 11.55, 17.75, WALL_H, "Medianera_Este (17.60m)")

# Fachada Sur
add_wall_part(-0.15, -0.15, 0.30, 0.15, WALL_H, "Muro_Portal_A")
add_wall_part(1.20, -0.15, 2.60, 0.15, WALL_H, "Muro_Sur_Salon_1")
add_wall_part(4.40, -0.15, 4.80, 0.15, WALL_H, "Muro_Sur_Salon_2")
add_wall_part(6.00, -0.15, 6.90, 0.15, WALL_H, "Muro_Sur_Cocina_1")
add_wall_part(8.10, -0.15, 8.90, 0.15, WALL_H, "Muro_Sur_Cocina_2")
add_wall_part(9.90, -0.15, 10.40, 0.15, WALL_H, "Muro_Sur_EscaleraB")

# Fachada Norte
add_wall_part(-0.15, 17.45, 0.80, 17.75, WALL_H, "Muro_Norte_Dorm2")
add_wall_part(2.40, 17.45, 3.60, 17.75, WALL_H, "Muro_Norte_Centro_D2_D3")
add_wall_part(5.20, 17.45, 6.40, 17.75, WALL_H, "Muro_Norte_Dorm3")

# Tabiques Interiores
add_wall_part(1.15, 0.00, 1.25, 1.20, WALL_H, "Mocheta_Entrada_PortalA")
add_wall_part(6.35, 0.00, 6.45, 0.80, WALL_H, "Mocheta_Sur_Cocina")
add_wall_part(6.35, 4.20, 6.45, 5.00, WALL_H, "Mocheta_Norte_Cocina")
add_wall_part(10.35, 0.00, 10.45, 5.00, WALL_H, "Tabique_Cocina_EscaleraB")

# Salón - Baños y Pasillo Noche
add_wall_part(1.15, 7.35, 6.40, 7.45, WALL_H, "Tabique_Salon_Banos")

# Muro Técnico Central Baños
add_wall_part(3.72, 7.35, 3.88, 9.80, WALL_H, "Muro_Tecnico_Banos_Compartido")

# Muro Patio hacia Baños y Suite
add_wall_part(6.30, 7.35, 6.50, 7.60, WALL_H, "Muro_Patio_BanoSuite_Sur")
add_wall_part(6.30, 8.40, 6.50, 8.75, WALL_H, "Muro_Patio_BanoSuite_Centro")
add_wall_part(6.30, 9.55, 6.50, 10.30, WALL_H, "Muro_Patio_Suite_Sur")
add_wall_part(6.30, 12.90, 6.50, 13.00, WALL_H, "Muro_Patio_Suite_Norte")

# Baños - Suite
add_wall_part(1.15, 9.75, 3.90, 9.85, WALL_H, "Tabique_BanoComun_Suite")
add_wall_part(4.70, 9.75, 6.40, 9.85, WALL_H, "Tabique_BanoSuite_Suite")

# Pasillo Noche - Master Suite
add_wall_part(1.15, 9.75, 1.25, 10.00, WALL_H, "Mocheta_Puerta_Suite_Sur")
add_wall_part(1.15, 10.85, 1.25, 12.55, WALL_H, "Tabique_Pasillo_MasterSuite")

# Master Suite Ampliada hacia el Norte (Ala Este)
add_wall_part(1.15, 12.45, 4.30, 12.55, WALL_H, "Tabique_MasterSuite_Norte_Cama")
add_wall_part(4.25, 12.45, 4.35, 13.55, WALL_H, "Tabique_MasterSuite_Oeste_Vestidor")

# Rellano - Dormitorios 2 y 3
add_wall_part(-0.15, 13.45, 0.80, 13.55, WALL_H, "Tabique_Rellano_Dorm2_Oeste")
add_wall_part(1.65, 13.45, 3.40, 13.55, WALL_H, "Tabique_Rellano_Centro_D2_D3")
add_wall_part(4.25, 13.45, 6.40, 13.55, WALL_H, "Tabique_Rellano_Dorm3_Este")

# Separación Dormitorio 2 - Dormitorio 3
add_wall_part(3.15, 13.45, 3.25, 17.60, WALL_H, "Tabique_Medianero_Dorm2_Dorm3")

# Muro Cochera Oeste
add_wall_part(6.30, 13.00, 6.50, 17.60, WALL_H, "Muro_Oeste_Gran_Cochera")

# Pilares Porche
add_wall_part(6.90, 7.25, 7.15, 7.50, WALL_H, "Pilar_Porche_1")
add_wall_part(9.40, 7.25, 9.65, 7.50, WALL_H, "Pilar_Porche_2")

# 4. Mobiliario 3D Representativo
def add_furn_box(x1, y1, x2, y2, h, mat, name)
  g = ENTS.add_group
  g.name = name
  g.layer = LAYERS["04_MOBILIARIO_ALMACENAJE"]
  pts = [
    Geom::Point3d.new(mm(x1), mm(y1), 0),
    Geom::Point3d.new(mm(x2), mm(y1), 0),
    Geom::Point3d.new(mm(x2), mm(y2), 0),
    Geom::Point3d.new(mm(x1), mm(y2), 0)
  ]
  f = g.entities.add_face(pts)
  f.reverse! if f.normal.z < 0
  f.pushpull(mm(h))
  g.entities.each { |face| face.material = mat if face.is_a?(Sketchup::Face) }
  g
end

# Gran Frente de Armarios Almacenaje Salón (3,60 m)
add_furn_box(0.15, 2.40, 0.85, 6.00, 1.20, mat_madera, "Mueble_Almacenaje_Salon_3.60m")

# Gran Vestidor Master Suite
add_furn_box(4.40, 10.00, 5.05, 13.20, 1.20, mat_madera, "Gran_Vestidor_Suite_3.20m")

# Camas
add_furn_box(1.90, 10.15, 3.90, 12.25, 0.50, mat_cama, "Cama_KingSize_MasterSuite")
add_furn_box(0.50, 14.80, 2.10, 16.80, 0.50, mat_cama, "Cama_Dormitorio_2")
add_furn_box(3.70, 14.80, 5.30, 16.80, 0.50, mat_cama, "Cama_Dormitorio_3")

# Armarios Dormitorios 2 y 3
add_furn_box(2.35, 14.80, 3.00, 17.00, 1.20, mat_madera, "Armario_Dormitorio_2")
add_furn_box(5.55, 14.80, 6.20, 17.00, 1.20, mat_madera, "Armario_Dormitorio_3")

# Isla de Cocina
add_furn_box(7.20, 1.60, 9.60, 2.70, 0.90, mat_muro, "Isla_Cocina_2.40m")

# Armarios Trastero Cochera
add_furn_box(10.50, 13.20, 11.20, 17.30, 1.20, mat_madera, "Frente_Armarios_Cochera_Trastero")

# 5. Configurar Escenas en SketchUp
CAM.perspective = false
CAM.set(
  Geom::Point3d.new(mm(5.70), mm(8.80), mm(35.0)),
  Geom::Point3d.new(mm(5.70), mm(8.80), 0.0),
  Geom::Vector3d.new(0, 1, 0)
)
VIEW.zoom_extents

p1 = PAGES["01_PLANTA_EDITABLE_2D"] || PAGES.add("01_PLANTA_EDITABLE_2D")
PAGES.selected_page = p1
p1.update(127)

p2 = PAGES["02_PERSPECTIVA_3D_EDITABLE"] || PAGES.add("02_PERSPECTIVA_3D_EDITABLE")
CAM.perspective = true
CAM.fov = 45.0
CAM.set(
  Geom::Point3d.new(mm(18.0), mm(-8.0), mm(16.0)),
  Geom::Point3d.new(mm(5.70), mm(8.80), mm(1.0)),
  Geom::Vector3d.new(0, 0, 1)
)
p2.update(127)

PAGES.selected_page = p1
VIEW.refresh

MODEL.save("C:/Users/Oscar Martinez/Desktop/mi-casa/casa-bifamiliar-3d.skp")
"ENTORNO V5 OPTIMIZADO CARGADO EN SKETCHUP CON MOBILIARIO Y ALMACENAJE"
