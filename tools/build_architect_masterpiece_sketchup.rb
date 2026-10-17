# -*- coding: utf-8 -*-
# ==============================================================================
# PROYECTO ARQUITECTÓNICO RESIDENCIAL - PALMA DEL RÍO
# Modelado 3D de Alta Precisión Arquitectónica en SketchUp (mm)
# ==============================================================================

M = 1000.0
ZF = 0.22; ZHB = 2.90; ZPA = 2.90; ZHA = 5.80
RF_B = ZHA; RF_T = ZHA + 0.20; PARA_T = ZHA + 0.32; ALB_T = ZHA + 0.36

MODEL = Sketchup.active_model
ENTS  = MODEL.entities
LAYS  = MODEL.layers

def mm(v)
  v * M
end

# Crear capas si no existen
["01_ESTRUCTURA", "02_MUROS_EXT", "03_TABIQUERIA", "04_CARPINTERIAS", 
 "05_CELOSIAS_MADERA", "06_MOBILIARIO", "07_PAISAJISMO", "08_ENTORNO"].each do |lay_name|
  LAYS.add(lay_name) unless LAYS[lay_name]
end

def box(x1, y1, z1, x2, y2, z2, name, layer_name="02_MUROS_EXT")
  g = ENTS.add_group
  g.name = name
  g.layer = LAYS[layer_name] if LAYS[layer_name]
  es = g.entities
  f = es.add_face([
    Geom::Point3d.new(mm(x1), mm(y1), mm(z1)),
    Geom::Point3d.new(mm(x2), mm(y1), mm(z1)),
    Geom::Point3d.new(mm(x2), mm(y2), mm(z1)),
    Geom::Point3d.new(mm(x1), mm(y2), mm(z1))
  ])
  f.reverse! if f.normal.z < 0
  f.pushpull(mm(z2 - z1))
  g
end

def clip(a, b, gaps)
  pts = ([a, b] + gaps.flatten.select { |p| p > a && p < b }).sort.uniq
  segs = []
  (0...(pts.size - 1)).each do |i|
    p = pts[i]; q = pts[i + 1]
    next if gaps.any? { |g| g[0] <= p && q <= g[1] }
    segs << [p, q] if q - p > 1e-6
  end
  segs
end

def wall_h(y, x0, x1, openings, t, z0, z1, name, layer="02_MUROS_EXT")
  gaps = openings.map { |o| o[0..1] }
  i = 0
  clip(x0, x1, gaps).each do |(a, b)|
    box(a, y - t / 2.0, z0, b, y + t / 2.0, z1, "#{name}-m#{i}", layer)
    i += 1
  end
  openings.each_with_index do |(a, b, alf, din), j|
    if alf && alf > z0
      box(a, y - t / 2.0, z0, b, y + t / 2.0, alf, "#{name}-alf#{j}", layer)
    end
    if din && din < z1
      box(a, y - t / 2.0, din, b, y + t / 2.0, z1, "#{name}-din#{j}", layer)
    end
  end
end

def wall_v(x, y0, y1, openings, t, z0, z1, name, layer="02_MUROS_EXT")
  gaps = openings.map { |o| o[0..1] }
  i = 0
  clip(y0, y1, gaps).each do |(a, b)|
    box(x - t / 2.0, a, z0, x + t / 2.0, b, z1, "#{name}-m#{i}", layer)
    i += 1
  end
  openings.each_with_index do |(a, b, alf, din), j|
    if alf && alf > z0
      box(x - t / 2.0, a, z0, x + t / 2.0, b, alf, "#{name}-alf#{j}", layer)
    end
    if din && din < z1
      box(x - t / 2.0, a, din, x + t / 2.0, b, z1, "#{name}-din#{j}", layer)
    end
  end
end

def window_frame_h(y, x0, x1, z0, z1, name)
  # Marcos perfilería RPT aluminio negro
  box(x0 - 0.04, y - 0.05, z0, x0 + 0.04, y + 0.05, z1, "#{name}_frame_l", "04_CARPINTERIAS")
  box(x1 - 0.04, y - 0.05, z0, x1 + 0.04, y + 0.05, z1, "#{name}_frame_r", "04_CARPINTERIAS")
  box(x0, y - 0.05, z0, x1, y + 0.05, z0 + 0.05, "#{name}_frame_b", "04_CARPINTERIAS")
  box(x0, y - 0.05, z1 - 0.05, x1, y + 0.05, z1, "#{name}_frame_t", "04_CARPINTERIAS")
  # Vidrio 3D
  box(x0 + 0.02, y - 0.015, z0 + 0.04, x1 - 0.02, y + 0.015, z1 - 0.04, "#{name}_glass", "04_CARPINTERIAS")
  # Vierteaguas exterior en piedra/cinc
  box(x0 - 0.05, y - 0.16, z0 - 0.04, x1 + 0.05, y - 0.05, z0, "#{name}_sill", "04_CARPINTERIAS")
end

def window_frame_v(x, y0, y1, z0, z1, name)
  # Marco RPT
  box(x - 0.05, y0 - 0.04, z0, x + 0.05, y0 + 0.04, z1, "#{name}_frame_l", "04_CARPINTERIAS")
  box(x - 0.05, y1 - 0.04, z0, x + 0.05, y1 + 0.04, z1, "#{name}_frame_r", "04_CARPINTERIAS")
  box(x - 0.05, y0, z0, x + 0.05, y1, z0 + 0.05, "#{name}_frame_b", "04_CARPINTERIAS")
  box(x - 0.05, y0, z1 - 0.05, x + 0.05, y1, z1, "#{name}_frame_t", "04_CARPINTERIAS")
  # Vidrio 3D
  box(x - 0.015, y0 + 0.02, z0 + 0.04, x + 0.015, y1 - 0.02, z1 - 0.04, "#{name}_glass", "04_CARPINTERIAS")
  # Vierteaguas exterior
  box(x - 0.16, y0 - 0.05, z0 - 0.04, x - 0.05, y1 + 0.05, z0, "#{name}_sill", "04_CARPINTERIAS")
end

def door_panel_h(y, x0, x1, z0, z1, name, wood=true)
  # Marco
  box(x0 - 0.04, y - 0.06, z0, x0 + 0.04, y + 0.06, z1, "#{name}_marco_l", "04_CARPINTERIAS")
  box(x1 - 0.04, y - 0.06, z0, x1 + 0.04, y + 0.06, z1, "#{name}_marco_r", "04_CARPINTERIAS")
  box(x0, y - 0.06, z1 - 0.05, x1, y + 0.06, z1, "#{name}_marco_t", "04_CARPINTERIAS")
  # Hoja
  lay = wood ? "05_CELOSIAS_MADERA" : "04_CARPINTERIAS"
  box(x0 + 0.02, y - 0.025, z0, x1 - 0.02, y + 0.025, z1 - 0.04, "#{name}_hoja", lay)
  # Manilla
  mx = (x1 - x0) > 0.8 ? x1 - 0.12 : x0 + 0.12
  box(mx - 0.02, y - 0.08, z0 + 1.0, mx + 0.02, y + 0.08, z0 + 1.05, "#{name}_manilla", "04_CARPINTERIAS")
end

# ==============================================================================
# LIMPIEZA COMPLETA DEL MODELO
# ==============================================================================
ENTS.clear!

# ==============================================================================
# 1. ENTORNO Y CALZADAS
# ==============================================================================
box(-4.0, -12.0, 0.0, 14.4, -1.2, 0.16, "calle_frente", "08_ENTORNO")
box(-3.0, -1.2, 0.0, 14.4, 0.0, 0.12, "acera_frente", "08_ENTORNO")
box(-4.0, 17.6, 0.0, 14.4, 28.0, 0.16, "calle_trasera", "08_ENTORNO")
box(-3.0, 17.6, 0.0, 14.4, 18.8, 0.12, "acera_trasera", "08_ENTORNO")
box(-3.0, 0.0, -0.06, 14.4, 17.6, 0.0, "terreno_solar", "08_ENTORNO")

# Césped y zonas verdes exteriores
box(-3.0, -1.2, 0.02, 0.0, 0.0, 0.06, "cesped_frente_l", "07_PAISAJISMO")
box(11.4, -1.2, 0.02, 14.4, 0.0, 0.06, "cesped_frente_r", "07_PAISAJISMO")
box(0.0, 17.6, 0.02, 3.2, 18.8, 0.06, "cesped_trasero", "07_PAISAJISMO")

# Setos bajos delimitadores
box(-2.5, -0.35, 0.0, 0.0, -0.15, 0.90, "seto_frente_l", "07_PAISAJISMO")
box(-2.9, -0.2, 0.0, -2.7, 3.0, 0.90, "seto_lateral_l", "07_PAISAJISMO")

# ==============================================================================
# 2. ESTRUCTURA Y FORJADOS
# ==============================================================================
# Solera de Planta Baja
box(0.0, 0.0, 0.15, 11.40, 17.60, ZF, "solera_pb", "01_ESTRUCTURA")

# Forjado Planta Alta (con VOLADIZO DE 40 cm en la banda central X: 2.60 -> 10.40)
box(0.0, 0.0, ZHB, 2.60, 5.00, ZHB + 0.20, "forjado_pa_ciego_izq", "01_ESTRUCTURA")
box(2.60, -0.40, ZHB, 10.40, 5.00, ZHB + 0.20, "forjado_pa_voladizo_central", "01_ESTRUCTURA")
box(10.40, 0.0, ZHB, 11.40, 5.00, ZHB + 0.20, "forjado_pa_caja_esc", "01_ESTRUCTURA")
box(0.0, 5.00, ZHB, 6.40, 17.60, ZHB + 0.20, "forjado_pa_oeste", "01_ESTRUCTURA")
box(6.40, 5.00, ZHB, 11.40, 7.60, ZHB + 0.20, "forjado_pa_galeria_patio", "01_ESTRUCTURA")
box(6.40, 13.00, ZHB, 11.40, 17.60, ZHB + 0.20, "forjado_pa_dorm2_trasero", "01_ESTRUCTURA")

# Forjado Cubierta Plana
box(0.0, 0.0, ZHA, 11.40, 17.60, ZHA + 0.20, "forjado_cubierta", "01_ESTRUCTURA")

# Parapetos y albardillas metálicas de cubierta
box(-0.15, -0.15, ZHA, 11.55, 0.15, PARA_T, "parapeto_sur", "02_MUROS_EXT")
box(-0.15, 17.45, ZHA, 11.55, 17.75, PARA_T, "parapeto_norte", "02_MUROS_EXT")
box(-0.15, -0.15, ZHA, 0.15, 17.75, PARA_T, "parapeto_oeste", "02_MUROS_EXT")
box(11.25, -0.15, ZHA, 11.55, 17.75, PARA_T, "parapeto_este", "02_MUROS_EXT")

# Albardillas de cinc
box(-0.05, -0.18, PARA_T, 11.45, 0.18, ALB_T, "albardilla_sur", "04_CARPINTERIAS")
box(-0.05, 17.42, PARA_T, 11.45, 17.78, ALB_T, "albardilla_norte", "04_CARPINTERIAS")
box(-0.18, -0.05, PARA_T, 0.18, 17.65, ALB_T, "albardilla_oeste", "04_CARPINTERIAS")
box(11.22, -0.05, PARA_T, 11.58, 17.65, ALB_T, "albardilla_este", "04_CARPINTERIAS")

# Lucernario lineal de cubierta sobre distribuidor noche (ZHA + 0.20 -> ZHA + 0.80)
box(0.20, 13.10, ZHA + 0.20, 4.30, 14.00, ZHA + 0.80, "lucernario_caja", "02_MUROS_EXT")
box(0.25, 13.15, ZHA + 0.80, 4.25, 13.95, ZHA + 0.84, "lucernario_vidrio", "04_CARPINTERIAS")

# ==============================================================================
# 3. PLANTA BAJA (VIVIENDA A): ENVOLVENTE Y MUROS
# ==============================================================================
# Medianeras
wall_v(0.0, 0.0, 17.60, [], 0.30, ZF, ZHB, "medianera_oeste_pb")
wall_v(11.40, 0.0, 5.00, [], 0.30, ZF, ZHB, "medianera_este_frente_pb")
wall_v(11.40, 5.00, 13.00, [], 0.30, ZF, ZHB, "muro_este_patio_pb")
wall_v(11.40, 13.00, 17.60, [], 0.30, ZF, ZHB, "medianera_este_tras_pb")

# Fachada Principal Sur (PB)
# Huecos: Portal A [0.30, 1.30], V-Salón1 [2.60, 4.40], V-Salón2 [4.80, 6.00],
#         V-Coc1 [6.90, 8.10], V-Coc2 [8.90, 9.90], Portal B [10.40, 11.40]
# Ventanas con h=1.80m (alf=0.60, din=2.40)
wall_h(0.0, 0.0, 11.40, [
  [0.30, 1.30, nil, 2.10],
  [2.60, 4.40, 0.60, 2.40],
  [4.80, 6.00, 0.60, 2.40],
  [6.90, 8.10, 0.60, 2.40],
  [8.90, 9.90, 0.60, 2.40],
  [10.40, 11.40, nil, 2.10]
], 0.30, ZF, ZHB, "fachada_sur_pb")

# Enmarque escultórico en piedra de Portal A
box(0.15, -0.15, ZF, 0.30, 0.05, 2.40, "enmarque_portalA_l", "02_MUROS_EXT")
box(1.30, -0.15, ZF, 1.45, 0.05, 2.40, "enmarque_portalA_r", "02_MUROS_EXT")
box(0.15, -0.15, 2.10, 1.45, 0.05, 2.40, "enmarque_portalA_top", "02_MUROS_EXT")

# Fachada Trasera Norte (PB)
# Huecos: Dorm 2 [0.80, 2.40], Dorm 3 [3.60, 5.20], Portón [8.00, 11.40]
wall_h(17.60, 0.0, 11.40, [
  [0.80, 2.40, 0.60, 2.40],
  [3.60, 5.20, 0.60, 2.40],
  [8.00, 11.40, nil, 2.50]
], 0.30, ZF, ZHB, "fachada_norte_pb")

# Muros y divisiones interiores PB
wall_v(1.40, 0.0, 13.00, [[1.40, 4.60, nil, 2.10], [7.90, 8.60, nil, 2.10]], 0.10, ZF, ZHB, "tabique_pasillo_pb", "03_TABIQUERIA")
wall_v(6.40, 0.0, 5.00, [[1.00, 4.40, nil, 2.60]], 0.10, ZF, ZHB, "tabique_saloncoc_pb", "03_TABIQUERIA")
wall_v(10.40, 0.0, 5.00, [], 0.15, ZF, ZHB, "muro_caja_escalera_pb")

# Muro de patio PB: GRAN APERTURA CRISTAL SUELO A TECHO AL PORCHE (X=6.40, Y: 5.00->7.40)
wall_v(6.40, 5.00, 7.40, [[5.00, 7.40, nil, nil]], 0.30, ZF, ZHB, "apertura_salon_porche_pb")
wall_v(6.40, 7.40, 13.00, [[7.80, 8.40, 1.40, 2.20], [9.00, 9.60, 1.40, 2.20], [11.00, 12.20, 0.60, 2.40]], 0.30, ZF, ZHB, "muro_patio_pb")

wall_h(5.00, 6.40, 10.40, [[6.40, 10.40, nil, nil]], 0.30, ZF, ZHB, "apertura_cocina_porche_pb")
wall_h(7.40, 1.40, 6.40, [], 0.10, ZF, ZHB, "tabique_bano1_pb", "03_TABIQUERIA")
wall_h(8.80, 1.40, 6.40, [], 0.10, ZF, ZHB, "tabique_bano2_pb", "03_TABIQUERIA")
wall_h(10.20, 1.40, 6.40, [[3.30, 4.00, nil, 2.10]], 0.10, ZF, ZHB, "tabique_suite_pb", "03_TABIQUERIA")
wall_h(13.00, 1.40, 8.00, [[2.20, 2.90, nil, 2.10]], 0.10, ZF, ZHB, "tabique_dppal_pb", "03_TABIQUERIA")
wall_v(4.50, 13.00, 14.10, [], 0.10, ZF, ZHB, "tabique_vestidor_pb", "03_TABIQUERIA")
wall_h(14.10, 0.0, 4.50, [[0.80, 1.50, nil, 2.10], [3.60, 4.30, nil, 2.10]], 0.10, ZF, ZHB, "tabique_distnoche_pb", "03_TABIQUERIA")
wall_v(3.20, 14.10, 17.60, [], 0.10, ZF, ZHB, "tabique_dorm2_dorm3_pb", "03_TABIQUERIA")
wall_v(6.40, 13.00, 17.60, [], 0.10, ZF, ZHB, "tabique_dorm3_trast_pb", "03_TABIQUERIA")
wall_v(8.00, 13.00, 17.60, [[13.30, 13.90, nil, 2.10]], 0.15, ZF, ZHB, "muro_trast_cochera_pb")

# Pilares escultóricos del porche en PB
box(6.90, 7.50, ZF, 7.10, 7.70, ZHB, "pilar_porche_1", "01_ESTRUCTURA")
box(9.50, 7.50, ZF, 9.70, 7.70, ZHB, "pilar_porche_2", "01_ESTRUCTURA")

# ==============================================================================
# 4. PLANTA ALTA (VIVIENDA B): ENVOLVENTE Y MUROS
# ==============================================================================
# Medianeras PA
wall_v(0.0, 0.0, 17.60, [], 0.30, ZPA, ZHA, "medianera_oeste_pa")
wall_v(11.40, 0.0, 5.00, [], 0.30, ZPA, ZHA, "medianera_este_frente_pa")
wall_v(11.40, 5.00, 13.00, [], 0.30, ZPA, ZHA, "muro_este_patio_pa")
wall_v(11.40, 13.00, 17.60, [], 0.30, ZPA, ZHA, "medianera_este_tras_pa")

# Fachada Principal Sur (PA)
# Banda izquierda ciega (0.00 -> 2.60)
# Banda central acristalada de suelo a techo:
# - Gran ventanal Salón PA [2.60, 6.00] con antepecho 0.40m y dintel a 2.60m (Z: 3.50 -> 5.70)
# - Gran ventanal Cocina PA [6.60, 9.90] con antepecho 0.40m y dintel a 2.60m (Z: 3.50 -> 5.70)
wall_h(0.0, 0.0, 10.40, [
  [2.60, 6.00, 3.50, 5.70],
  [6.60, 9.90, 3.50, 5.70]
], 0.30, ZPA, ZHA, "fachada_sur_pa")

# Fachada Trasera Norte (PA)
# Terraza descubierta [0.00, 3.20] con peto de 1.10m
# Ventana Dorm 3 [3.60, 5.20] con alf=0.80, din=2.60 (Z: 3.70 -> 5.50)
# Gran ventanal Dorm 2 [7.00, 11.20] de suelo a techo (Z: 3.50 -> 5.70)
box(0.0, 17.48, ZPA, 3.20, 17.60, ZPA + 1.10, "peto_terraza_pa_n", "02_MUROS_EXT")
box(0.0, 14.10, ZPA, 0.12, 17.60, ZPA + 1.10, "peto_terraza_pa_o", "02_MUROS_EXT")
box(0.0, 14.10, ZPA, 3.20, 14.22, ZPA + 1.10, "peto_terraza_pa_s", "02_MUROS_EXT")

wall_h(17.60, 3.20, 11.40, [
  [3.60, 5.20, 3.70, 5.50],
  [7.00, 11.20, 3.50, 5.70]
], 0.30, ZPA, ZHA, "fachada_norte_pa")

# Muros interiores PA
wall_v(10.40, 0.0, 5.00, [], 0.15, ZPA, ZHA, "muro_caja_escalera_pa")
# Galería acristalada PA sobre el patio central (X=6.40, Y: 5.00 -> 7.60)
wall_v(6.40, 5.00, 7.60, [[5.00, 7.60, nil, nil]], 0.30, ZPA, ZHA, "galeria_patio_pa")
wall_v(6.40, 7.60, 13.00, [[7.80, 8.40, 4.30, 5.10], [9.00, 9.60, 4.30, 5.10], [11.00, 12.20, 3.50, 5.30]], 0.30, ZPA, ZHA, "muro_patio_pa")

wall_h(7.40, 1.40, 6.40, [], 0.10, ZPA, ZHA, "tabique_bano1_pa", "03_TABIQUERIA")
wall_h(8.80, 1.40, 6.40, [], 0.10, ZPA, ZHA, "tabique_bano2_pa", "03_TABIQUERIA")
wall_h(10.20, 1.40, 6.40, [[3.30, 4.00, nil, 2.10]], 0.10, ZPA, ZHA, "tabique_suite_pa", "03_TABIQUERIA")
wall_h(13.00, 1.40, 6.40, [[2.20, 2.90, nil, 2.10]], 0.10, ZPA, ZHA, "tabique_dppal_pa", "03_TABIQUERIA")
wall_h(14.10, 0.0, 6.40, [[0.80, 1.50, nil, 2.10], [3.60, 4.30, nil, 2.10]], 0.10, ZPA, ZHA, "tabique_distnoche_pa", "03_TABIQUERIA")
wall_v(3.20, 14.10, 17.60, [], 0.10, ZPA, ZHA, "tabique_terraza_dorm3_pa", "03_TABIQUERIA")
wall_v(6.40, 13.00, 17.60, [[13.20, 14.00, nil, 2.10]], 0.10, ZPA, ZHA, "tabique_dorm2_pa", "03_TABIQUERIA")
wall_h(13.00, 6.40, 11.40, [[7.00, 10.40, 3.50, 5.70]], 0.10, ZPA, ZHA, "ventanal_dorm2_patio_pa", "03_TABIQUERIA")

# ==============================================================================
# 5. CELOSÍA INTEGRAL DE LAMAS DE MADERA (ESCALERA DERECHA)
# ==============================================================================
# Banda X: 10.40 -> 11.40, Y: -0.10 -> 0.00, Z: 0.00 -> 5.80 m
# 12 lamas verticales continuas de suelo a cubierta
(0..11).each do |idx|
  lx = 10.42 + idx * (0.96 / 11.0)
  box(lx - 0.02, -0.08, 0.0, lx + 0.02, -0.02, ZHA, "celosia_lama_v_#{idx}", "05_CELOSIAS_MADERA")
end
# Bastidores horizontales de fijación
[ZHB, ZHA].each_with_index do |zh, k|
  box(10.40, -0.09, zh - 0.04, 11.40, -0.01, zh, "celosia_bastidor_#{k}", "05_CELOSIAS_MADERA")
end

# ==============================================================================
# 6. PATIO CENTRAL: PÉRGOLA VOLADA, LÁMINA DE AGUA Y OLIVO
# ==============================================================================
# Pavimento noble de patio
box(6.40, 5.00, 0.0, 11.40, 13.00, 0.06, "pavimento_patio", "07_PAISAJISMO")

# Pérgola de 3 vigas de hormigón visto voladas (sección 20x30 cm)
[6.60, 8.90, 11.20].each_with_index do |vx, vi|
  box(vx - 0.10, 5.00, 2.65, vx + 0.10, 9.50, 2.95, "viga_hormigon_patio_#{vi}", "01_ESTRUCTURA")
end
# Lamas cruzadas de madera sobre las vigas
(0..7).each do |li|
  ly = 5.30 + li * 0.55
  box(6.50, ly - 0.03, 2.95, 11.30, ly + 0.03, 3.03, "lama_pergola_#{li}", "05_CELOSIAS_MADERA")
end

# Lámina de agua reflectante integrada
box(6.80, 8.00, 0.02, 8.60, 9.80, 0.06, "lamina_agua_borde", "07_PAISAJISMO")
box(6.85, 8.05, 0.04, 8.55, 9.75, 0.058, "lamina_agua_superficie", "04_CARPINTERIAS")

# Macetón con Olivo ornamental
box(9.20, 9.00, 0.06, 10.40, 10.20, 0.65, "olivo_jardinera", "07_PAISAJISMO")
box(9.70, 9.50, 0.65, 9.90, 9.70, 1.70, "olivo_tronco", "05_CELOSIAS_MADERA")
box(9.10, 8.90, 1.70, 10.50, 10.30, 2.80, "olivo_copa", "07_PAISAJISMO")

# ==============================================================================
# 7. CARPINTERÍAS, VENTANALES Y PUERTAS
# ==============================================================================
# Portales de entrada
door_panel_h(0.0, 0.30, 1.30, ZF, 2.10, "puerta_portalA", true)
door_panel_h(0.0, 10.40, 11.40, ZF, 2.10, "puerta_portalB", true)

# Ventanas PB Fachada Sur
window_frame_h(0.0, 2.60, 4.40, 0.60, 2.40, "win_salon1_pb")
window_frame_h(0.0, 4.80, 6.00, 0.60, 2.40, "win_salon2_pb")
window_frame_h(0.0, 6.90, 8.10, 0.60, 2.40, "win_coc1_pb")
window_frame_h(0.0, 8.90, 9.90, 0.60, 2.40, "win_coc2_pb")

# Ventanales PA Fachada Sur (de suelo a techo sobre el voladizo)
window_frame_h(-0.40, 2.60, 6.00, 3.50, 5.70, "win_salon_pa")
window_frame_h(-0.40, 6.60, 9.90, 3.50, 5.70, "win_cocina_pa")

# Gran cerramiento corredero Salón -> Porche en PB (suelo a techo)
window_frame_v(6.40, 5.00, 7.40, ZF, ZHB, "corredera_salon_porche_pb")

# Galería acristalada PA -> Patio central
window_frame_v(6.40, 5.00, 7.60, ZPA, ZHA, "galeria_vidrio_pa")

# Ventanas hacia patio interior (PB y PA)
window_frame_v(6.40, 7.80, 8.40, 1.40, 2.20, "win_bano1_pb")
window_frame_v(6.40, 9.00, 9.60, 1.40, 2.20, "win_bano2_pb")
window_frame_v(6.40, 11.00, 12.20, 0.60, 2.40, "win_dppal_pb")

window_frame_v(6.40, 7.80, 8.40, 4.30, 5.10, "win_bano1_pa")
window_frame_v(6.40, 9.00, 9.60, 4.30, 5.10, "win_bano2_pa")
window_frame_v(6.40, 11.00, 12.20, 3.50, 5.30, "win_dppal_pa")

# Ventanales de Dormitorio 2 PA al patio
window_frame_h(13.00, 7.00, 10.40, 3.50, 5.70, "win_dorm2_patio_pa")

# Fachada Trasera Norte
window_frame_h(17.60, 0.80, 2.40, 0.60, 2.40, "win_dorm2_pb")
window_frame_h(17.60, 3.60, 5.20, 0.60, 2.40, "win_dorm3_pb")
window_frame_h(17.60, 3.60, 5.20, 3.70, 5.50, "win_dorm3_pa")
window_frame_h(17.60, 7.00, 11.20, 3.50, 5.70, "win_dorm2_pa_norte")

# Portón cochera con celosía integrada
box(8.00, 17.52, ZF, 11.40, 17.58, ZF + 2.50, "porton_cochera_corten", "04_CARPINTERIAS")

# ==============================================================================
# 8. ESCALERA RESIDENCIAL DE ACCESO A PLANTA ALTA
# ==============================================================================
h_peld = (ZHB - ZF) / 17.0
t_peld = 5.00 / 17.0
(0..16).each do |step_i|
  sy0 = step_i * t_peld
  sy1 = sy0 + t_peld
  sz1 = ZF + (step_i + 1) * h_peld
  box(10.45, sy0, ZF, 11.35, sy1, sz1, "escalera_peld_#{step_i}", "01_ESTRUCTURA")
end
# Barandilla metálica de la escalera
box(10.43, 0.0, ZF + 0.90, 10.47, 5.00, ZHB + 0.90, "escalera_pasamanos", "04_CARPINTERIAS")

# ==============================================================================
# 9. MOBILIARIO PRINCIPAL A ESCALA ARQUITECTÓNICA
# ==============================================================================
# Salón PB
box(2.00, 2.20, ZF, 4.60, 3.10, ZF + 0.75, "sofa_salon_pb", "06_MOBILIARIO")
box(2.40, 4.20, ZF, 4.20, 5.80, ZF + 0.75, "mesa_comedor_pb", "06_MOBILIARIO")
box(2.20, 6.80, ZF + 0.40, 4.40, 7.15, ZF + 1.60, "mueble_tv_pb", "06_MOBILIARIO")

# Cocina PB: Isla con cascada
box(7.20, 2.00, ZF, 9.40, 3.00, ZF + 0.92, "isla_cocina_pb", "06_MOBILIARIO")
box(7.15, 1.95, ZF + 0.92, 9.45, 3.05, ZF + 0.96, "encimera_isla_pb", "06_MOBILIARIO")

# Dormitorios PB
box(4.00, 10.80, ZF, 5.80, 12.80, ZF + 0.55, "cama_dppal_pb", "06_MOBILIARIO")
box(1.00, 15.30, ZF, 2.60, 17.30, ZF + 0.55, "cama_dorm2_pb", "06_MOBILIARIO")
box(4.20, 15.30, ZF, 5.80, 17.30, ZF + 0.55, "cama_dorm3_pb", "06_MOBILIARIO")

# Salón PA (Espacio diáfano 50 m²)
box(2.00, 2.20, ZPA, 4.80, 3.20, ZPA + 0.75, "sofa_salon_pa", "06_MOBILIARIO")
box(2.40, 4.20, ZPA, 4.20, 5.80, ZPA + 0.75, "mesa_comedor_pa", "06_MOBILIARIO")

# Gran Dormitorio 2 PA (23 m²)
box(7.60, 14.80, ZPA, 9.40, 16.80, ZPA + 0.55, "cama_dorm2_pa", "06_MOBILIARIO")
box(9.80, 13.20, ZPA, 11.20, 17.20, ZPA + 2.40, "armario_vestidor_d2_pa", "06_MOBILIARIO")

"MODELO ARQUITECTONICO SKETCHUP GENERADO CON EXITO"
