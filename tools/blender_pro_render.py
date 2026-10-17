# -*- coding: utf-8 -*-
"""Render EEVEE profesional de las vistas de la vivienda bifamiliar."""
import os
import bpy

OUT = r"C:\Users\Oscar Martinez\Desktop\mi-casa"
scene = bpy.context.scene

scene.render.resolution_x = 2560
scene.render.resolution_y = 1440

engine = None
for e in ("BLENDER_EEVEE_NEXT", "BLENDER_EEVEE"):
    if e in dir(bpy.types.RenderSettings):
        engine = e
        break
if engine:
    scene.render.engine = engine

try:
    scene.view_settings.view_transform = "Filmic"
    scene.view_settings.look = "AgX - Punchy"
except Exception:
    pass

# nombres para ocultar en vistas de interior
hide_keys = ("M_pb_front", "M_pa_front", "roof", "parapet_", "slab_pa_front")


def set_hidden(cams_hide):
    for obj in bpy.data.objects:
        if any(obj.name.startswith(k) for k in cams_hide):
            obj.hide_render = True
        else:
            obj.hide_render = False


def render_view(cam_name, fname, hide=()):
    cam = bpy.data.objects.get(cam_name)
    if cam is None:
        print("SIN CAMARA:", cam_name)
        return
    scene.camera = cam
    set_hidden(hide)
    path = os.path.join(OUT, fname)
    scene.render.filepath = path
    bpy.ops.render.render(write_still=True)
    print("RENDER OK:", fname, os.path.exists(path))


exterior = ()
interior = ("M_pb_front", "M_pa_front", "roof", "parapet_", "slab_pa_front", "roof_pat1", "roof_pat2", "roof_pat3")

render_view("cam_fachada", "pro-fachada.png", exterior)
render_view("cam_fachada2", "pro-fachada2.png", exterior)
render_view("cam_trasera", "pro-trasera.png", exterior)
render_view("cam_axo", "pro-axo.png", exterior)
render_view("cam_patios", "pro-patios.png", exterior)
render_view("cam_interior_pb", "pro-interior-pb.png", interior)
render_view("cam_interior_pa", "pro-interior-pa.png", interior)

print("ALL PRO RENDERS DONE")
