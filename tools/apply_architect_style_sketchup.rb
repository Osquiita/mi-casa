# -*- coding: utf-8 -*-
# ==============================================================================
# ESTILO VISUAL Y MATERIALES ARQUITECTÓNICOS PARA SKETCHUP
# ==============================================================================

MODEL = Sketchup.active_model
MATS  = MODEL.materials
ROPT  = MODEL.rendering_options
SINFO = MODEL.shadow_info

def create_mat(name, r, g, b, alpha=1.0)
  m = MATS[name] || MATS.add(name)
  m.color = Sketchup::Color.new(r, g, b)
  m.alpha = alpha if m.respond_to?(:alpha=)
  m
end

# Materiales PBR conceptuales
m_estuco     = create_mat("EstucoBlanco", 246, 244, 239)
m_hormigon   = create_mat("HormigonVisto", 195, 192, 186)
m_madera_v   = create_mat("MaderaIroko", 165, 110, 60)
m_madera_int = create_mat("MaderaRoble", 200, 155, 105)
m_aluminio   = create_mat("AluminioGrafito", 45, 48, 52)
m_vidrio     = create_mat("VidrioArquitectonico", 185, 215, 230, 0.35)
m_caliza     = create_mat("PiedraCaliza", 225, 220, 210)
m_agua       = create_mat("AguaReflejo", 70, 135, 165, 0.60)
m_corten     = create_mat("ChapaCorten", 145, 75, 45)
m_asfalto    = create_mat("Asfalto", 70, 72, 75)
m_cesped     = create_mat("CespedNatural", 125, 160, 90)
m_olivo      = create_mat("OlivoVerde", 95, 130, 75)
m_mueble     = create_mat("MobiliarioNeutro", 215, 212, 205)

# Asignación de materiales por grupo / capa / nombre
MODEL.entities.each do |e|
  next unless e.is_a?(Sketchup::Group)
  n = e.name.to_s
  lay = e.respond_to?(:layer) ? e.layer.name.to_s : ""
  m = nil

  if n =~ /glass|vidrio/i
    m = m_vidrio
  elsif n =~ /frame|marco|sill|albardilla|pasamanos|manilla/i
    m = m_aluminio
  elsif n =~ /corten|porton_cochera/i
    m = m_corten
  elsif n =~ /celosia|lama|enmarque|hoja|tronco/i
    m = m_madera_v
  elsif n =~ /viga_hormigon|solera|forjado|parapeto|pilar/i
    m = m_hormigon
  elsif n =~ /pavimento|acera/i
    m = m_caliza
  elsif n =~ /agua/i
    m = m_agua
  elsif n =~ /calle|asfalto/i
    m = m_asfalto
  elsif n =~ /cesped|seto|copa|jardinera/i
    m = m_cesped
  elsif n =~ /sofa|mesa|cama|isla|encimera|mueble|armario/i
    m = m_mueble
  elsif lay == "02_MUROS_EXT"
    m = m_estuco
  elsif lay == "03_TABIQUERIA"
    m = m_estuco
  elsif lay == "01_ESTRUCTURA"
    m = m_hormigon
  elsif lay == "04_CARPINTERIAS"
    m = m_aluminio
  elsif lay == "05_CELOSIAS_MADERA"
    m = m_madera_v
  end

  if m
    e.material = m
    e.entities.each { |f| f.material = m if f.is_a?(Sketchup::Face) }
  end
end

# Configuración de estilo visual y sombras arquitectónicas
ROPT["BackgroundColor"]   = Sketchup::Color.new(250, 250, 250)
ROPT["DrawGround"]        = true
ROPT["GroundColor"]        = Sketchup::Color.new(235, 233, 227)
ROPT["EdgeColorMode"]      = 0 # Color por material / todo negro estándar, no por ejes
ROPT["DrawBackEdges"]      = false
ROPT["DisplayColorByLayer"]= false
ROPT["SectionDefaultCutColor"] = Sketchup::Color.new(40, 40, 40)

begin
  SINFO["display_shadows"]        = true
  SINFO["display_ground_shadows"] = true
  SINFO["cast_shadows"]           = true
  SINFO["receive_shadows"]        = true
  SINFO["latitude"]               = 37.693 # Palma del Río (Córdoba)
  SINFO["longitude"]              = -5.282
  SINFO["time"]                   = "15:30" # Luz de tarde con sombras volumétricas
  SINFO["day"]                    = 180    # Solsticio de verano
  SINFO["Light"]                  = 85     # Intensidad de luz
  SINFO["Dark"]                   = 35     # Sombras suaves no empastadas
rescue StandardError => ex
  puts "Shadow setup note: #{ex.message}"
end

"ESTILO Y MATERIALES APLICADOS CORRECTAMENTE"
