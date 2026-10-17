# Sondear Table, Rectangle, Image, Label, LinearDimension, Style
results = []

# Table
results << "TABLE methods: #{Layout::Table.instance_methods(false).sort.inspect}"

# Rectangle  
results << "RECTANGLE methods: #{Layout::Rectangle.instance_methods(false).sort.inspect}"

# Image
results << "IMAGE methods: #{Layout::Image.instance_methods(false).sort.inspect}"

# Label
results << "LABEL methods: #{Layout::Label.instance_methods(false).sort.inspect}"

# LinearDimension
results << "LINEARDIM methods: #{Layout::LinearDimension.instance_methods(false).sort.inspect}"

# Style
results << "STYLE methods: #{Layout::Style.instance_methods(false).sort.inspect}"

# Table.new signature test
begin
  t = Layout::Table.new(3, 4, 5.0, 3.0, Geom::Point2d.new(1.0, 1.0))
  results << "TABLE NEW: OK (#{t.class})"
rescue => e
  results << "TABLE NEW error: #{e.class}: #{e.message}"
end

# Image.new
begin
  png = "C:/Users/Oscar Martinez/Desktop/mi-casa/entrega/planos_2d/01_plano_2d_planta_baja.png"
  if File.exist?(png)
    bounds = Geom::Bounds2d.new(1.0, 1.0, 10.0, 7.0)
    img = Layout::Image.new(png, bounds)
    results << "IMAGE NEW: OK (#{img.class})"
  else
    results << "IMAGE: PNG not found"
  end
rescue => e
  results << "IMAGE NEW error: #{e.class}: #{e.message}"
end

# Rectangle.new
begin
  bounds = Geom::Bounds2d.new(0.5, 0.5, 15.5, 10.7)
  rect = Layout::Rectangle.new(bounds)
  results << "RECTANGLE NEW: OK (#{rect.class})"
rescue => e
  results << "RECTANGLE NEW error: #{e.class}: #{e.message}"
end

results.join("\n")
