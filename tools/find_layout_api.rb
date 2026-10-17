# Buscar donde esta la API de Layout
paths = $LOAD_PATH.select { |p| p.downcase.include?("layout") }
su_exe = Sketchup.find_support_file("SketchUp.exe", "")
su_dir = su_exe ? File.dirname(su_exe) : "NOT FOUND"

# Buscar en el directorio de instalacion
install_base = "C:/Program Files/SketchUp/SketchUp 2025"
layout_rb_files = []
if Dir.exist?(install_base)
  Dir.glob("#{install_base}/**/*.rb").each do |f|
    layout_rb_files << f if f.downcase.include?("layout")
  end
end

# Verificar si Layout namespace existe
layout_defined = defined?(Layout) ? "YES" : "NO"

# Check $LOAD_PATH completo
all_paths = $LOAD_PATH.join("\n")

"Layout defined: #{layout_defined}\nSU_DIR: #{su_dir}\nLayout in LOAD_PATH: #{paths.inspect}\nLayout .rb files found: #{layout_rb_files.first(5).inspect}\n\nFull LOAD_PATH:\n#{all_paths}"
