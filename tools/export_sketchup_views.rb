# -*- coding: utf-8 -*-
# ==============================================================================
# CONFIGURACIÓN DE CÁMARAS ARQUITECTÓNICAS Y EXPORTACIÓN DE VISTAS EN SKETCHUP
# ==============================================================================

MODEL = Sketchup.active_model
CAM   = MODEL.active_view.camera

def set_architectural_cam(cam, eye_x, eye_y, eye_z, target_x, target_y, target_z, fov=45)
  cam.perspective = true
  cam.fov = fov
  cam.set(
    Geom::Point3d.new(eye_x, eye_y, eye_z),
    Geom::Point3d.new(target_x, target_y, target_z),
    Geom::Vector3d.new(0, 0, 1)
  )
end

# Centro del solar en mm
CX = 5700.0
CY = 8800.0
CZ = 3000.0

views = {
  # 1. Fachada Principal Nivel Ojo (Calle Moreno Torroba)
  "01_fachada_principal_sur"   => [CX, -12000.0, 1650.0, CX, 4000.0, 2200.0, 48],
  
  # 2. Vista Tres Cuartos Sur-Este (Voladizo + Celosía de Madera)
  "02_fachada_sur_este_3cuartos" => [CX + 14000.0, -10000.0, 2800.0, CX, 3000.0, 2500.0, 45],
  
  # 3. Vista Axonométrica General
  "03_vista_axonometrica"      => [CX + 18000.0, -14000.0, 16000.0, CX, CY, CZ, 50],
  
  # 4. Patio Central Bioclimático (Pérgola + Olivo + Lámina de Agua)
  "04_patio_central_pergola"   => [CX + 4500.0, 5200.0, 1800.0, CX + 3000.0, 10000.0, 1500.0, 55],
  
  # 5. Fachada Trasera y Cochera (Calle Norte)
  "05_fachada_trasera_norte"   => [CX, 28000.0, 1800.0, CX, 14000.0, 2500.0, 46],
  
  # 6. Vista Aérea Posterior (Patio + Terraza PA)
  "06_axonometrica_posterior"  => [CX - 15000.0, 26000.0, 15000.0, CX, CY, CZ, 50]
}

dir = "C:/Users/Oscar Martinez/Desktop/mi-casa/entrega/renders/sketchup"
require "fileutils"
FileUtils.mkdir_p(dir)

results = []
view = MODEL.active_view

views.each do |name, v|
  set_architectural_cam(CAM, v[0], v[1], v[2], v[3], v[4], v[5], v[6])
  view.refresh
  filepath = "#{dir}/#{name}.png"
  begin
    view.write_image(filepath, 2560, 1440, false, 2.0)
    results << "#{name}: GUARDADO (#{filepath})"
  rescue StandardError => e
    results << "#{name}: ERROR #{e.message}"
  end
end

results.join("\n")
