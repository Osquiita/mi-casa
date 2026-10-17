# -*- coding: utf-8 -*-
# Escenas v2 + export PNG.
MODEL = Sketchup.active_model
CANVAS = MODEL.rendering_options
SHADOW = MODEL.shadow_info

CANVAS["BackgroundColor"] = Sketchup::Color.new(255, 255, 255)
CANVAS["DrawGround"] = true
CANVAS["GroundColor"] = Sketchup::Color.new(236, 234, 228)
CANVAS["EdgeColorMode"] = 2

begin
  SHADOW["display_shadows"] = true
  SHADOW["display_ground_shadows"] = true
  SHADOW["cast_shadows"] = true
  SHADOW["receive_shadows"] = true
  SHADOW["latitude"] = 37.693
  SHADOW["longitude"] = -5.282
  SHADOW["time"] = "13:30"
  SHADOW["day"] = 200
rescue StandardError
end

CAM = MODEL.active_view.camera

def look(cam, dsx, dsy, dsz, tx, ty, tz, fov = 50)
  cam.perspective = true; cam.fov = fov
  cam.set(Geom::Point3d.new(dsx, dsy, dsz), Geom::Point3d.new(tx, ty, tz), Geom::Vector3d.new(0, 0, 1))
end

cx, cy, cz = 5700.0, 8800.0, 3000.0
ZF = 220; ZPA = 2900
views = {
  "iso-general"    => [cx+16000, cy+20000, 14000, cx, cy, cz, 55],
  "iso-sur-este"   => [cx+16000, cy-18000, 13000, cx, cy, cz, 55],
  "alzado-sur"     => [cx, cy-30000, 2600, cx, cy, 2600, 42],
  "alzado-norte"   => [cx, cy+30000, 2600, cx, cy, 2600, 42],
  "alzado-este"    => [cx+28000, cy, 2600, cx, cy, 2600, 38],
  "patio-pergola"  => [cx+6500, cy+11000, 8000, cx+2000, cy+3000, 2000, 60],
  "interior-salon" => [2500, 3000, ZF+1700, 5000, 5000, ZF+1200, 28],
  "interior-pa"    => [2500, 11000, ZPA+1700, 5000, 12500, ZPA+1200, 28]
}

dir = "C:/Users/Oscar Martinez/Desktop/mi-casa/entrega/renders/sketchup"
require "fileutils"; FileUtils.mkdir_p(dir)

out = []; view = MODEL.active_view
views.each do |(name, v)|
  look(CAM, v[0], v[1], v[2], v[3], v[4], v[5], v[6])
  MODEL.active_view.refresh
  begin
    view.write_image("#{dir}/#{name}.png", 1600, 900, false, 3.0)
    out << "#{name}: ok"
  rescue StandardError => e
    out << "#{name}: ERR #{e.message}"
  end
end
out.join("\n")