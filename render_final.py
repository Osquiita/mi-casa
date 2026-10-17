# -*- coding: utf-8 -*-
"""Render batch script - executes inside Blender's Python environment.
Run with: blender.exe --background file.blend --python render_final.py
"""
import bpy
import math
import os

scene = bpy.context.scene
OUT = r'C:\Users\Oscar Martinez\Desktop\mi-casa\entrega\renders'
os.makedirs(OUT, exist_ok=True)

# Rebuild 3D geometry with latest open-plan PA and fluid door/window settings
BUILD_SCRIPT = r'C:\Users\Oscar Martinez\Desktop\mi-casa\tools\blender_pro_build.py'
if os.path.exists(BUILD_SCRIPT):
    print("Rebuilding 3D model with updated open-plan geometry...")
    with open(BUILD_SCRIPT, 'r', encoding='utf-8') as f:
        exec(f.read())

# Extra cleanup: remove any wall T_pa1 or blocking door panels
for ob_name in ["T_pa1_0", "T_pa1_1", "T_pa1", "d_salon_porche_panel"]:
    ob = bpy.data.objects.get(ob_name)
    if ob:
        bpy.data.objects.remove(ob, do_unlink=True)
        print(f"Removed blocking object: {ob_name}")

# Configure EEVEE
try:
    scene.render.engine = 'BLENDER_EEVEE_NEXT'
except:
    scene.render.engine = 'BLENDER_EEVEE'

scene.render.resolution_x = 2560
scene.render.resolution_y = 1440
scene.render.film_transparent = False
scene.render.image_settings.file_format = 'PNG'
scene.render.image_settings.color_mode = 'RGB'
scene.render.image_settings.compression = 15

# Quality settings
eevee = scene.eevee
for attr, val in [('use_ssr', True), ('use_ssr_refraction', True), ('use_gtao', True)]:
    if hasattr(eevee, attr):
        try: setattr(eevee, attr, val)
        except: pass
try: eevee.taa_render_samples = 64
except: pass
try:
    scene.view_settings.view_transform = 'Filmic'
    scene.view_settings.look = 'AgX - Punchy'
except: pass

# Camera helper
def make_cam(name, loc, target, lens=32.0):
    existing = bpy.data.objects.get(name)
    if existing:
        bpy.data.objects.remove(existing, do_unlink=True)
    
    # Remove old target if exists
    target_obj = bpy.data.objects.get(name + '_target')
    if target_obj:
        bpy.data.objects.remove(target_obj, do_unlink=True)
    
    cd = bpy.data.cameras.new(name)
    cd.lens = lens
    cd.sensor_width = 36.0
    obj = bpy.data.objects.new(name, cd)
    bpy.context.scene.collection.objects.link(obj)
    obj.location = loc
    empty = bpy.data.objects.new(name + '_target', None)
    empty.empty_display_size = 0.3
    bpy.context.scene.collection.objects.link(empty)
    empty.location = target
    tc = obj.constraints.new('TRACK_TO')
    tc.target = empty
    tc.track_axis = 'TRACK_NEGATIVE_Z'
    tc.up_axis = 'UP_Y'
    return obj

eye = 1.70
z_pa = 2.90

# Define all cameras
cameras = {
    '01-fachada-principal': ((5.7, -8.5, eye), (5.7, 4.0, 2.5), 35),
    '02-fachada-nocturna': ((5.7, -8.5, eye), (5.7, 4.0, 2.5), 35),
    '03-alzado-trasero': ((5.7, 26.0, eye), (5.7, 12.0, 2.5), 35),
    '04-vista-axonometrica': ((20.0, -15.0, 16.0), (5.7, 8.8, 2.0), 28),
    '05-patio-central': ((9.0, 5.5, eye), (9.0, 10.0, 1.5), 24),
    '06-interior-salon-pb': ((2.8, 0.5, eye), (4.0, 4.0, 1.2), 22),
    '07-interior-cocina-pb': ((8.5, 4.5, eye), (8.5, 1.5, 1.0), 24),
    '08-dormitorio-principal': ((4.0, 10.5, eye), (4.0, 12.5, 1.2), 24),
    '09-interior-salon-pa': ((2.8, 0.5, eye + z_pa), (4.0, 4.0, z_pa + 1.2), 22),
    '10-porche-patio': ((8.5, 6.0, eye), (9.0, 9.0, 1.5), 28),
}

# Create all cameras
cam_objects = {}
for cam_name, (loc, target, lens) in cameras.items():
    cam_objects[cam_name] = make_cam('CAM_' + cam_name, loc, target, lens)

print(f'Created {len(cam_objects)} cameras')

# Store original sun/light settings for nocturnal render
sun = None
for obj in bpy.data.objects:
    if obj.type == 'LIGHT' and obj.data.type == 'SUN':
        sun = obj
        break

# Render each camera
for cam_name, cam_obj in cam_objects.items():
    print(f'Rendering: {cam_name}...')
    scene.camera = cam_obj
    
    # Special handling for nocturnal render
    if 'nocturna' in cam_name:
        # Reduce sun intensity for night scene
        if sun:
            original_energy = sun.data.energy
            sun.data.energy = 0.3
            sun.data.color = (0.3, 0.35, 0.5)
        
        # Darken world
        if scene.world and scene.world.use_nodes:
            bg = None
            for node in scene.world.node_tree.nodes:
                if node.type == 'BACKGROUND':
                    bg = node
                    break
            if bg:
                original_bg_strength = bg.inputs['Strength'].default_value
                bg.inputs['Strength'].default_value = 0.05
        
        # Boost interior lights
        for obj in bpy.data.objects:
            if obj.type == 'MESH' and 'luz_' in obj.name:
                for mat_slot in obj.material_slots:
                    if mat_slot.material and mat_slot.material.use_nodes:
                        for node in mat_slot.material.node_tree.nodes:
                            if node.type == 'BSDF_PRINCIPLED':
                                try:
                                    node.inputs['Emission Strength'].default_value *= 3.0
                                except: pass
    
    scene.render.filepath = os.path.join(OUT, cam_name)
    bpy.ops.render.render(write_still=True)
    print(f'  -> {cam_name}.png saved')
    
    # Restore settings after nocturnal render
    if 'nocturna' in cam_name:
        if sun:
            sun.data.energy = original_energy
            sun.data.color = (1.0, 0.97, 0.90)
        if scene.world and scene.world.use_nodes:
            if bg:
                bg.inputs['Strength'].default_value = original_bg_strength
        for obj in bpy.data.objects:
            if obj.type == 'MESH' and 'luz_' in obj.name:
                for mat_slot in obj.material_slots:
                    if mat_slot.material and mat_slot.material.use_nodes:
                        for node in mat_slot.material.node_tree.nodes:
                            if node.type == 'BSDF_PRINCIPLED':
                                try:
                                    node.inputs['Emission Strength'].default_value /= 3.0
                                except: pass

# Save the final blend file
bpy.ops.wm.save_mainfile(filepath=r'C:\Users\Oscar Martinez\Desktop\mi-casa\casa-bifamiliar-3d.blend')
print('=== ALL 10 RENDERS COMPLETE ===')
