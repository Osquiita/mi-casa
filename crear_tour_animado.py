# -*- coding: utf-8 -*-
"""Crea la camara animada CAM_TOUR en el archivo .blend con keyframes suaves
recorriendo toda la casa (Fachada -> Salon PB -> Cocina -> Porche/Patio -> Gran Salon PA 50m2 -> Axonometrica)
para que el usuario SOLO TENGA QUE DARLE AL PLAY (Barra espaciadora) en Blender."""
import bpy
import math
import os
import shutil

BASE = r"C:\Users\Oscar Martinez\Desktop\mi-casa"
OUT_TOUR = os.path.join(BASE, "entrega", "renders", "tour_frames")
os.makedirs(OUT_TOUR, exist_ok=True)

def setup_tour_camera(blend_file_path):
    print(f"\nConfigurando CAM_TOUR en {blend_file_path}...")
    bpy.ops.wm.open_mainfile(filepath=blend_file_path)
    
    scene = bpy.context.scene
    FPS = 25
    TOTAL_FRAMES = 300
    scene.render.fps = FPS
    scene.frame_start = 1
    scene.frame_end = TOTAL_FRAMES
    scene.frame_current = 1
    
    cam_name = "CAM_TOUR"
    target_name = "CAM_TOUR_TARGET"
    
    cam_obj = bpy.data.objects.get(cam_name)
    if cam_obj:
        bpy.data.objects.remove(cam_obj, do_unlink=True)
    
    target_obj = bpy.data.objects.get(target_name)
    if target_obj:
        bpy.data.objects.remove(target_obj, do_unlink=True)
    
    cam_data = bpy.data.cameras.new(cam_name)
    cam_data.lens = 24.0  # 24mm gran angular
    cam_data.sensor_width = 36.0
    
    cam_obj = bpy.data.objects.new(cam_name, cam_data)
    bpy.context.scene.collection.objects.link(cam_obj)
    
    target_obj = bpy.data.objects.new(target_name, None)
    target_obj.empty_display_size = 0.3
    bpy.context.scene.collection.objects.link(target_obj)
    
    tc = cam_obj.constraints.new('TRACK_TO')
    tc.target = target_obj
    tc.track_axis = 'TRACK_NEGATIVE_Z'
    tc.up_axis = 'UP_Y'
    
    scene.camera = cam_obj
    
    # Keyframes del recorrido
    keyframes = [
        (1,   (5.7, -9.0, 1.70), (5.7, 4.0, 2.20), 32.0),   # 1. Fachada Principal exterior
        (40,  (0.8, -1.0, 1.70), (2.5, 3.5, 1.50), 24.0),   # 2. Entrando por Portal A
        (80,  (2.8, 1.5, 1.65),  (5.0, 3.5, 1.40), 22.0),   # 3. Salon-Comedor PB (37m2)
        (120, (7.5, 2.5, 1.65),  (8.5, 6.0, 1.50), 24.0),   # 4. Cocina con Isla mirando al Porche
        (160, (8.9, 7.5, 1.70),  (9.2, 9.5, 1.80), 24.0),   # 5. Patio central con Olivo y Pergola
        (200, (4.0, 2.5, 4.60),  (7.0, 5.5, 4.20), 22.0),   # 6. Gran Salon Diafano PA (50m2)
        (250, (1.6, 14.5, 4.60), (5.0, 15.5, 4.20), 24.0),  # 7. Patio trasero elevado PA
        (300, (18.0, -12.0, 14.0), (5.7, 8.8, 2.0), 28.0),  # 8. Vista Aerea Axonometrica Final
    ]
    
    for frame, loc, tgt, lens in keyframes:
        scene.frame_set(frame)
        
        cam_obj.location = loc
        cam_obj.keyframe_insert(data_path="location", index=-1, frame=frame)
        
        target_obj.location = tgt
        target_obj.keyframe_insert(data_path="location", index=-1, frame=frame)
        
        cam_data.lens = lens
        cam_data.keyframe_insert(data_path="lens", frame=frame)
    
    # Save main file with active CAM_TOUR camera and 1..300 frame timeline ready to press PLAY!
    bpy.ops.wm.save_mainfile(filepath=blend_file_path)
    print(f"OK: {blend_file_path} configurado con CAM_TOUR activa (Frames 1-300). Listo para dar al PLAY.")

# Apply to master blend and LITE blend
setup_tour_camera(os.path.join(BASE, "casa-bifamiliar-3d.blend"))
setup_tour_camera(os.path.join(BASE, "casa-bifamiliar-3d-LITE.blend"))

print("\n=== TOUR VIRTUAL LISTO EN AMBOS ARCHIVOS BLENDER (SOLO DAR AL PLAY) ===")
