MODEL = Sketchup.active_model
CANVAS = MODEL.rendering_options
out = []
{ "BackgroundColor" => Sketchup::Color.new(255, 255, 255),
  "DrawGround" => true,
  "GroundColor" => Sketchup::Color.new(236, 234, 228),
  "DisplaySky" => false,
  "EdgeColorMode" => 2,
  "EdgeDrawMode" => 1,
  "ModelTime" => true }
  .each do |k, v|
    begin
      CANVAS[k] = v
      out << "#{k}=ok"
    rescue StandardError => e
      out << "#{k}=ERR #{e.message}"
    end
  end
out.join("\n")