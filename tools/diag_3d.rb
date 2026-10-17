MODEL = Sketchup.active_model
layers = {}
MODEL.entities.each do |e|
  if e.is_a?(Sketchup::Group)
    if e.respond_to?(:layer)
      layers[e.layer.name] = layers.fetch(e.layer.name, 0) + 1
    end
  end
end
b = MODEL.bounds
min = b.min.to_a.map { |v| v.round }
max = b.max.to_a.map { |v| v.round }
"bounds_min=#{min} bounds_max=#{max}\n" + layers.map { |k, v| "#{k}: #{v}" }.join(" | ")