# -*- coding: utf-8 -*-
"""Organiza los archivos del proyecto en la carpeta de entrega."""
import os
import shutil

BASE = r"C:\Users\Oscar Martinez\Desktop\mi-casa"
ENTREGA = os.path.join(BASE, "entrega")

# Ensure directories exist
for d in ["planos", "renders", "modelo-3d", "documentacion"]:
    os.makedirs(os.path.join(ENTREGA, d), exist_ok=True)

# 1. Copy plan PDFs
print("=== PLANOS ===")
plan_files = [
    "plano-01-parcela.pdf",
    "plano-02-planta-baja.pdf",
    "plano-03-planta-alta.pdf",
    "plano-04-alzados-seccion.pdf",
    "plano-05-cuadro-superficies.pdf",
    "proyecto-completo.pdf",
]
for f in plan_files:
    src = os.path.join(BASE, f)
    if os.path.exists(src):
        shutil.copy2(src, os.path.join(ENTREGA, "planos", f))
        print(f"  Copiado: {f}")

# Also copy DXF files
dxf_files = [f for f in os.listdir(BASE) if f.endswith('.dxf')]
for f in dxf_files:
    src = os.path.join(BASE, f)
    shutil.copy2(src, os.path.join(ENTREGA, "planos", f))
    print(f"  Copiado: {f}")

# 2. Copy renders (best ones + new final renders)
print("\n=== RENDERS ===")
render_dir = os.path.join(ENTREGA, "renders")

# Copy pro-* renders
pro_renders = [f for f in os.listdir(BASE) if f.startswith('pro-') and f.endswith('.png')]
for f in pro_renders:
    src = os.path.join(BASE, f)
    shutil.copy2(src, os.path.join(render_dir, f))
    print(f"  Copiado: {f}")

# New renders are already in the renders folder (from render_final.py)
existing_renders = [f for f in os.listdir(render_dir) if f.endswith('.png')]
print(f"  Total renders en carpeta: {len(existing_renders)}")

# 3. Copy 3D model
print("\n=== MODELO 3D ===")
blend_files = [
    "casa-bifamiliar-3d.blend",
    "casa-bifamiliar-3d-LITE.blend",
]
for f in blend_files:
    src = os.path.join(BASE, f)
    if os.path.exists(src):
        shutil.copy2(src, os.path.join(ENTREGA, "modelo-3d", f))
        print(f"  Copiado: {f}")

# 4. Dossier PDF is already in documentacion from the generator script
print("\n=== DOCUMENTACION ===")
doc_dir = os.path.join(ENTREGA, "documentacion")
dossier = os.path.join(doc_dir, "dossier-proyecto-bifamiliar.pdf")
if os.path.exists(dossier):
    size_mb = os.path.getsize(dossier) / (1024*1024)
    print(f"  Dossier: {size_mb:.1f} MB")

# Copy PROYECTO.md as reference
src_proj = os.path.join(BASE, "PROYECTO.md")
if os.path.exists(src_proj):
    shutil.copy2(src_proj, os.path.join(doc_dir, "PROYECTO.md"))
    print("  Copiado: PROYECTO.md")

# 5. Summary
print("\n=== RESUMEN ENTREGA ===")
total_files = 0
total_size = 0
for root, dirs, files in os.walk(ENTREGA):
    for f in files:
        path = os.path.join(root, f)
        total_files += 1
        total_size += os.path.getsize(path)

print(f"  Total archivos: {total_files}")
print(f"  Tamano total: {total_size / (1024*1024):.1f} MB")
print(f"\n  Carpeta de entrega: {ENTREGA}")

# List contents
for d in ["planos", "renders", "modelo-3d", "documentacion"]:
    dpath = os.path.join(ENTREGA, d)
    files = os.listdir(dpath) if os.path.exists(dpath) else []
    print(f"\n  {d}/ ({len(files)} archivos)")
    for f in sorted(files):
        size = os.path.getsize(os.path.join(dpath, f)) / 1024
        print(f"    {f} ({size:.0f} KB)")
