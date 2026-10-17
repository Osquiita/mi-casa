# -*- coding: utf-8 -*-
# Layout ya disponible en Sketchup 2026

layout_path = "C:/Users/Oscar Martinez/Desktop/mi-casa/entrega/planos/casa-bifamiliar-COMPLETO.layout"
pdf_path    = "C:/Users/Oscar Martinez/Desktop/mi-casa/entrega/planos/00_CUADERNO_PLANOS_LAYOUT_A3.pdf"

begin
  doc = Layout::Document.open(layout_path)
  status = doc.export(pdf_path)
  "EXPORT PDF OK: #{status} -> #{pdf_path}"
rescue => e
  "EXPORT PDF ERROR: #{e.class}: #{e.message}"
end
