# -*- coding: utf-8 -*-
import fitz # PyMuPDF
import os

pdf_path = r"C:\Users\Oscar Martinez\Desktop\mi-casa\entrega\planos\00_CUADERNO_PLANOS_LAYOUT_A3.pdf"
out_dir  = r"C:\Users\Oscar Martinez\Desktop\mi-casa\entrega\planos_2d"
os.makedirs(out_dir, exist_ok=True)

artifact_dir = r"C:\Users\Oscar Martinez\.gemini\antigravity\brain\f2a400d1-b2ac-4bc5-8f7d-8be7048d2417"

doc = fitz.open(pdf_path)
print(f"Total paginas: {len(doc)}")

for i, page in enumerate(doc):
    pix = page.get_pixmap(dpi=150)
    out_name = f"lamina_{i+1:02d}_layout_a3.png"
    out_file = os.path.join(out_dir, out_name)
    pix.save(out_file)
    
    # Copia a artefactos
    art_file = os.path.join(artifact_dir, out_name)
    pix.save(art_file)
    print(f"Pagina {i+1} guardada en: {out_file}")

print("TODAS LAS LAMINAS EXPORTADAS A PNG")
