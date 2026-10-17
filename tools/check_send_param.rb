# Comprobar parametros de send_to_layout
m = Sketchup.method(:send_to_layout)
"send_to_layout arity: #{m.arity}, parameters: #{m.parameters.inspect}"
