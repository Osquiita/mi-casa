# encoding: UTF-8
# tools/sketchup_bridge_pro.rb
# Ejecuta la construcción 3D, estilos, escenas y envío a LayOut en una operación atómica.

model = Sketchup.active_model
model.start_operation('Construccion_Maestra_Mi_Casa', true)

begin
  tools_dir = __dir__
  scripts = [
    'inyectar_modelo_3d_perfeccionado.rb',
    'apply_architect_style_sketchup.rb',
    'setup_escenas_completas_sketchup.rb',
    'save_for_layout.rb',
    'reconstruir_layout_maestro.rb'
  ]

  scripts.each do |script_name|
    full_path = File.join(tools_dir, script_name)
    if File.exist?(full_path)
      load full_path
    end
  end

  model.commit_operation
  puts "EXITO: Modelo 3D y LayOut sincronizados correctamente."
rescue => e
  model.abort_operation
  puts "ERROR EN PUENTE SKETCHUP: #{e.message}"
  puts e.backtrace.first(5).join("\n")
end
