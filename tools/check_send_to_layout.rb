# Comprobar si existe send_to_layout o metodos similares
methods = Sketchup.methods.grep(/layout/i)
model_methods = Sketchup.active_model.methods.grep(/layout/i)

"Sketchup layout methods: #{methods.inspect}\nModel layout methods: #{model_methods.inspect}"
