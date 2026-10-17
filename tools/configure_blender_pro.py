# -*- coding: utf-8 -*-
"""
Script de Configuración Profesional de Blender para Arquitectura y Conexión MCP en Tiempo Real.
Habilita addons clave de arquitectura (Archimesh, DXF, Sun Position), configura el motor de render
en calidad máxima PBR/AgX y activa el servidor Blender MCP en el puerto 9876.
"""
import os
import sys
import bpy
import addon_utils

print("================================================================")
print(" CONFIGURANDO BLENDER PARA ARQUITECTURA PROFESIONAL & MCP")
print("================================================================")

# 1. HABILITAR ADDONS DE ARQUITECTURA E INTEGRACION CAD
ADDONS_ARQUITECTURA = [
    "archimesh",               # Generación paramétrica de puertas, ventanas, muros y escaleras
    "io_import_dxf",           # Importación de planos 2D en formato CAD DXF
    "sun_position",            # Posicionamiento solar exacto por latitud/longitud y hora
    "materials_utils",         # Gestión avanzada de materiales PBR
]

enabled_count = 0
for addon in ADDONS_ARQUITECTURA:
    try:
        loaded_default, loaded_state = addon_utils.check(addon)
        if not loaded_state:
            addon_utils.enable(addon, default_set=True)
            print(f"[OK] Addon de Arquitectura activado: {addon}")
        else:
            print(f"[INFO] Addon ya estaba activo: {addon}")
        enabled_count += 1
    except Exception as e:
        print(f"[WARN] No se pudo activar {addon}: {e}")

# 2. CONFIGURAR REGLAS DE RENDERIZADO ARQUITECTONICO DE ALTA FIDELIDAD
scene = bpy.context.scene

# Configuración de Color y Gestión Tonal
try:
    scene.display_settings.display_device = "sRGB"
    scene.view_settings.view_transform = "AgX"
    scene.view_settings.look = "Punchy"
    print("[OK] Gestión de Color configurada en AgX Punchy (Alta Fidelidad Arquitectónica)")
except Exception:
    try:
        scene.view_settings.view_transform = "Filmic"
        scene.view_settings.look = "High Contrast"
        print("[OK] Gestión de Color configurada en Filmic High Contrast")
    except Exception as e:
        print(f"[WARN] Error en View Transform: {e}")

# Configuración de Render EEVEE / Cycles
engine_found = False
for engine in ("BLENDER_EEVEE_NEXT", "BLENDER_EEVEE", "CYCLES"):
    if engine in dir(bpy.types.RenderSettings):
        scene.render.engine = engine
        engine_found = True
        print(f"[OK] Motor de Render fijado en: {engine}")
        break

if hasattr(scene, "eevee"):
    eevee = scene.eevee
    for attr, val in [("use_ssr", True), ("use_ssr_refraction", True),
                      ("use_gtao", True), ("use_bloom", True)]:
        if hasattr(eevee, attr):
            try:
                setattr(eevee, attr, val)
            except Exception:
                pass
    if hasattr(eevee, "shadow_cascade_size"):
        try:
            eevee.shadow_cascade_size = "4096"
        except Exception:
            pass

# 3. REGISTRAR E INICIAR EL ADDON DE CONEXION BLENDER MCP
ADDON_PATH = r"C:\Users\Oscar Martinez\Desktop\mi-casa\tools\BlenderMCP_addon.py"

if os.path.exists(ADDON_PATH):
    try:
        # Cargar y ejecutar el script del addon en el entorno de Blender
        with open(ADDON_PATH, "r", encoding="utf-8") as f:
            code = f.read()
        exec(compile(code, "BlenderMCP_addon.py", "exec"), globals())
        print("[OK] Script BlenderMCP_addon cargado correctamente")

        # Intentar iniciar el servidor MCP si el operador está disponible
        if hasattr(bpy.ops, "wm") and hasattr(bpy.ops.wm, "start_mcp_server"):
            try:
                bpy.ops.wm.start_mcp_server()
                print("[OK] Servidor Blender MCP iniciado en el puerto 9876")
            except Exception as e:
                print(f"[INFO] Servidor MCP disponible (iniciar desde panel lateral 'N'): {e}")
    except Exception as e:
        print(f"[ERROR] Error al registrar BlenderMCP_addon: {e}")
else:
    print(f"[ERROR] No se encontró el archivo del addon en: {ADDON_PATH}")

# 4. GUARDAR PREFERENCIAS DE USUARIO
try:
    bpy.ops.wm.save_userpref()
    print("[OK] Preferencias de Blender guardadas permanentemente.")
except Exception as e:
    print(f"[INFO] Preferencias actualizadas en sesión actual: {e}")

print("================================================================")
print(" BLENDER CONFIGURADO AL MAXIMO NIVEL ARQUITECTONICO & MCP OK")
print("================================================================")
