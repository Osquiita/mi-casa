# Probar Table.new con 3 args
begin
  t = Layout::Table.new(3, 4, Geom::Bounds2d.new(1.0, 1.0, 8.0, 4.0))
  "TABLE OK rows=#{t.dimensions[0]} cols=#{t.dimensions[1]}"
rescue => e
  "TABLE 3arg error: #{e.class}: #{e.message}"
end
