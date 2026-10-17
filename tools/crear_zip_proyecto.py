# -*- coding: utf-8 -*-
"""
CREADOR DE ARCHIVO ZIP OFICIAL DEL PROYECTO COMPLETO 'MI-CASA'
Empaqueta toda la estructura del proyecto en C:/Users/Oscar Martinez/Desktop/mi-casa-proyecto-completo.zip:
- Modelos 3D SketchUp (.skp) y LayOut (.layout)
- Colección completa de Planos 2D Ejecutivos (PDF y PNG de alta resolución)
- Dossier Oficial de Licencia Municipal (Tomos I, II, III y IV del CTE)
- Scripts de modelado, renderizado y utilidades (Python y Ruby)
- Renders fotorrealistas y perspectivas
Excluye únicamente la instalación pesada de software binario de Blender (7.000 archivos ejecutables) y cachés temporales.
"""

import os
import zipfile
import time

SRC_DIR = r"C:\Users\Oscar Martinez\Desktop\mi-casa"
ZIP_PATH = r"C:\Users\Oscar Martinez\Desktop\mi-casa-proyecto-completo.zip"

def crear_zip():
    print(f"Comenzando empaquetado de: {SRC_DIR}")
    print(f"Destino: {ZIP_PATH}")
    t0 = time.time()
    
    total_files = 0
    total_uncompressed = 0
    
    with zipfile.ZipFile(ZIP_PATH, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=6) as zipf:
        for root, dirs, files in os.walk(SRC_DIR):
            # Excluir la carpeta de software binario ejecutable y cachés
            if 'blender-5.2.0-windows-x64' in root:
                continue
            if '__pycache__' in root:
                continue
            
            for file in files:
                # Excluir el instalador binario .zip de blender (400 MB) para mantener el archivo ágil
                if file.lower() == 'blender.zip':
                    continue
                # Evitar incluir el propio zip si estuviera dentro
                if file.endswith('.zip') and 'mi-casa' in file:
                    continue
                
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, os.path.dirname(SRC_DIR))
                
                file_size = os.path.getsize(full_path)
                total_uncompressed += file_size
                total_files += 1
                
                zipf.write(full_path, rel_path)
                if total_files % 50 == 0:
                    print(f"  Empaquetados {total_files} archivos...")

    t1 = time.time()
    zip_size = os.path.getsize(ZIP_PATH)
    
    print("\n" + "="*60)
    print("EMPAQUETADO FINALIZADO CON ÉXITO")
    print("="*60)
    print(f"Archivo generado: {ZIP_PATH}")
    print(f"Archivos empaquetados: {total_files}")
    print(f"Tamaño original: {total_uncompressed / (1024*1024):.2f} MB")
    print(f"Tamaño del ZIP comprimido: {zip_size / (1024*1024):.2f} MB")
    print(f"Tiempo de compresión: {t1 - t0:.2f} segundos")

if __name__ == "__main__":
    crear_zip()
