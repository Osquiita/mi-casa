# Sondear clases disponibles en Layout API
classes = {}
["Image", "Rectangle", "Path", "Line", "LinearDimension",
 "AngularDimension", "Label", "Table", "Ellipse",
 "SketchUpModel", "FormattedText", "Group",
 "ConnectionPoint", "AutoTextDefinition"].each do |c|
  begin
    classes[c] = eval("defined?(Layout::#{c})") ? "YES" : "NO"
  rescue => e
    classes[c] = "ERROR: #{e.message}"
  end
end

# Comprobar metodos de FormattedText
ft_methods = Layout::FormattedText.instance_methods(false).sort.first(30)

# Comprobar metodos de Document
doc_methods = Layout::Document.instance_methods(false).sort.first(30)

# Comprobar auto text definitions
doc = Layout::Document.new
atd = doc.auto_text_definitions.map { |a| "#{a.name}:#{a.tag}" }.first(10) rescue "N/A"

"CLASSES:\n#{classes.map{|k,v| "  #{k}: #{v}"}.join("\n")}\n\nFormattedText methods: #{ft_methods.inspect}\n\nDocument methods: #{doc_methods.inspect}\n\nAutoText: #{atd.inspect}"
