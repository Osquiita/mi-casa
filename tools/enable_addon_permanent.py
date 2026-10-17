# -*- coding: utf-8 -*-
import bpy
import addon_utils

addon_name = "BlenderMCP"
try:
    loaded_default, loaded_state = addon_utils.check(addon_name)
    if not loaded_state:
        addon_utils.enable(addon_name, default_set=True)
        print(f"[OK] Addon {addon_name} activado permanentemente en Blender.")
    else:
        print(f"[INFO] Addon {addon_name} ya estaba activo.")
    bpy.ops.wm.save_userpref()
    print("[OK] User preferences saved successfully.")
except Exception as e:
    print(f"[ERROR] Error al activar addon {addon_name}: {e}")
