# Probar estilos de texto
doc = Layout::Document.new
layer0 = doc.layers.first
page = doc.pages.first

# Texto con estilo
tb = Geom::Bounds2d.new(1.0, 1.0, 4.0, 0.5)
t = Layout::FormattedText.new("Test text", tb)
doc.add_entity(t, layer0, page)

# Ahora aplicar estilo
style = t.style(0, 4)
style.font_size = 24
style.text_bold = true
style.font_family = "Arial"
style.text_color = Sketchup::Color.new(28, 30, 33)
t.apply_style(style, 0, 9)

# Rectangle con estilo
rb = Geom::Bounds2d.new(0.5, 0.5, 15.0, 10.5)
rect = Layout::Rectangle.new(rb)
doc.add_entity(rect, layer0, page)
rs = rect.style
rs.stroked = true
rs.stroke_width = 2.0
rs.stroke_color = Sketchup::Color.new(28, 30, 33)
rs.solid_filled = false
rect.style = rs

doc.save("C:/Users/Oscar Martinez/Desktop/mi-casa/entrega/planos/test_styles.layout")
"STYLES TEST OK"
