# -*- coding: utf-8 -*-
"""
RECONSTRUCCION ARQUITECTONICA DE FACHADA CONTEMPORÁNEA DE LUJO & INTERIORISMO PREMIUM.
Genera una arquitectura residencial contemporánea de vanguardia en Blender.
"""
import os
import bpy
import math

# Cargar biblioteca de geometrías
LIB = r"C:\Users\Oscar Martinez\Desktop\mi-casa\tools\blender_lib.py"
with open(LIB, "r", encoding="utf-8") as f:
    lib_src = f.read()
ns = {}
exec(compile(lib_src, "blender_lib", "exec"), ns)
for _k in ("cube", "plane", "uv_sphere", "cylinder", "wall_h", "wall_v",
           "glass_h", "glass_v", "door_h", "door_v", "tree", "plant",
           "table", "chair", "bed", "wardrobe", "sofa", "tv", "kitchen_units",
           "toilet", "sink", "shower", "car", "stairs", "mat"):
    globals()[_k] = ns[_k]

# LIMPIEZA DE LA ESCENA
for obj in list(bpy.data.objects):
    bpy.data.objects.remove(obj, do_unlink=True)
for mesh in list(bpy.data.meshes):
    bpy.data.meshes.remove(mesh)

# ================================================================ MATERIALES PBR CONTEMPORANEOS
def pbr_mat(name, color=(0.8, 0.8, 0.8), rough=0.6, metal=0.0, spec=0.5,
            trans=0.0, ior=1.45, emit=0.0, bump=0.0, tex_scale=10.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    bsdf = nt.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (color[0], color[1], color[2], 1.0)
    bsdf.inputs["Roughness"].default_value = rough
    bsdf.inputs["Metallic"].default_value = metal
    try:
        bsdf.inputs["Specular IOR Level"].default_value = spec
    except Exception:
        pass
    bsdf.inputs["Transmission Weight"].default_value = trans
    try:
        bsdf.inputs["IOR"].default_value = ior
    except Exception:
        pass
    if emit > 0:
        try:
            bsdf.inputs["Emission Color"].default_value = (color[0], color[1], color[2], 1.0)
            bsdf.inputs["Emission Strength"].default_value = emit
        except Exception:
            pass
    if bump > 0:
        ntex = nt.nodes.new("ShaderNodeTexNoise")
        ntex.inputs["Scale"].default_value = tex_scale
        ntex.inputs["Detail"].default_value = 8.0
        bump_node = nt.nodes.new("ShaderNodeBump")
        bump_node.inputs["Strength"].default_value = bump
        bump_node.inputs["Distance"].default_value = 0.02
        nt.links.new(ntex.outputs["Fac"], bump_node.inputs["Height"])
        nt.links.new(bump_node.outputs["Normal"], bsdf.inputs["Normal"])
    return m

# Paleta de Materiales Contemporáneos de Lujo
M_WHITE_STUCCO = pbr_mat("M_WHITE_STUCCO", (0.97, 0.96, 0.94), 0.55, bump=0.01, tex_scale=5.0)
M_DARK_ANTRACITA= pbr_mat("M_DARK_ANTRACITA", (0.12, 0.13, 0.15), 0.35, metal=0.7)
M_WOOD_IPE     = pbr_mat("M_WOOD_IPE", (0.62, 0.42, 0.26), 0.35, spec=0.5, bump=0.04, tex_scale=3.0)
M_WOOD_TECA    = pbr_mat("M_WOOD_TECA", (0.75, 0.54, 0.35), 0.40, spec=0.4, bump=0.03, tex_scale=3.0)
M_CONCRETE     = pbr_mat("M_CONCRETE", (0.75, 0.73, 0.70), 0.75, bump=0.02, tex_scale=4.0)
M_GLASS_LUX    = pbr_mat("M_GLASS_LUX", (0.72, 0.90, 0.95), 0.02, spec=1.0, trans=0.98, ior=1.52)
M_MARBLE       = pbr_mat("M_MARBLE", (0.94, 0.93, 0.91), 0.15, spec=0.8, bump=0.005)
M_BLACK_STEEL  = pbr_mat("M_BLACK_STEEL", (0.08, 0.09, 0.10), 0.25, metal=0.95)
M_LED_WARM     = pbr_mat("M_LED_WARM", (1.0, 0.90, 0.75), 0.1, emit=25.0)
M_LED_FACADE   = pbr_mat("M_LED_FACADE", (0.95, 0.98, 1.0), 0.1, emit=35.0)
M_WATER        = pbr_mat("M_WATER", (0.35, 0.65, 0.75), 0.05, spec=1.0, trans=0.8, ior=1.33)
M_DECK         = pbr_mat("M_DECK", (0.58, 0.40, 0.26), 0.45, bump=0.05, tex_scale=4.0)
M_GRASS        = pbr_mat("M_GRASS", (0.32, 0.48, 0.25), 1.0, bump=0.05, tex_scale=15.0)
M_ROAD         = pbr_mat("M_ROAD", (0.28, 0.29, 0.31), 0.9, bump=0.04, tex_scale=6.0)

z_f = 0.22; z_hb = 2.90; z_pa = 2.90; z_ha = 5.80

# ================================================================ SOLAR Y ENTORNO URBANIZADO
cube("road_front", -4.0, 14.4, -12.0, -1.2, 0.0, 0.16, M_ROAD)
cube("sidewalk_front", -3.0, 14.4, -1.2, 0.0, 0.0, 0.12, M_CONCRETE)
cube("road_rear", -4.0, 14.4, 17.6, 28.0, 0.0, 0.16, M_ROAD)
cube("sidewalk_rear", -3.0, 14.4, 17.6, 18.8, 0.0, 0.12, M_CONCRETE)
cube("ground_plot", -3.0, 14.4, 0.0, 17.6, -0.06, 0.0, M_CONCRETE)
cube("patio_deck", 6.40, 11.40, 5.00, 13.00, 0.0, 0.08, M_DECK)
plane("patio_pool", [(7.0, 7.0), (10.8, 7.0), (10.8, 11.0), (7.0, 11.0)], M_WATER, z=0.06)

# ================================================================ MUROS P-01
wall_h("M_pb_front", (0.0, 0.0, 11.40),
       [(0.30, 1.30), (2.40, 5.80), (6.80, 10.20)],
       z_f, z_hb, M_WHITE_STUCCO)
wall_h("M_pb_rear", (17.60, 0.0, 11.40),
       [(0.80, 2.40), (3.60, 5.20), (8.60, 11.00)],
       z_f, z_hb, M_WHITE_STUCCO)
wall_v("M_pb_l", (0.0, 0.0, 17.60), [], z_f, z_hb, M_DARK_ANTRACITA)
wall_v("M_pb_rf", (11.40, 0.0, 5.00), [], z_f, z_hb, M_WHITE_STUCCO)
wall_v("M_pb_rpatio", (11.40, 5.00, 13.00), [], z_f, z_hb, M_DARK_ANTRACITA)
wall_v("M_pb_rr", (11.40, 13.00, 17.60), [], z_f, z_hb, M_WHITE_STUCCO)

# ================================================================ VOLUMETRÍA CONTEMPORÁNEA & MARCO EN VOLADIZO
# Marco proyectado en Planta Alta (Voladizo antracita de diseño)
cube("frame_top_n", -0.20, 11.60, -0.40, 0.20, z_ha - 0.10, z_ha + 0.35, M_DARK_ANTRACITA)
cube("frame_top_w", -0.40, 0.0, -0.40, 5.20, z_pa - 0.10, z_ha + 0.35, M_DARK_ANTRACITA)
cube("frame_top_e", 11.40, 11.80, -0.40, 5.20, z_pa - 0.10, z_ha + 0.35, M_DARK_ANTRACITA)
cube("frame_top_bottom", -0.40, 11.80, -0.40, 0.20, z_pa - 0.10, z_pa + 0.10, M_DARK_ANTRACITA)

# Revestimiento de Madera Bioclimática Ipe en acceso
for k in range(16):
    zx = 0.25 + k * 0.15
    cube(f"wood_panel_front_{k}", zx - 0.02, zx + 0.02, -0.15, -0.02, z_f, z_hb, M_WOOD_IPE)

# ================================================================ MUROS P-02
wall_h("M_pa_front", (0.0, 0.0, 11.40),
       [(2.40, 5.80), (6.80, 10.20)],
       z_pa, z_ha, M_WHITE_STUCCO)
wall_h("M_pa_rear", (17.60, 0.0, 11.40),
       [(3.60, 5.20), (7.00, 11.00)],
       z_pa, z_ha, M_WHITE_STUCCO)
wall_v("M_pa_l", (0.0, 0.0, 17.60), [], z_pa, z_ha, M_DARK_ANTRACITA)
wall_v("M_pa_rf", (11.40, 0.0, 5.00), [], z_pa, z_ha, M_WHITE_STUCCO)

# ================================================================ VENTANALES MURO CORTINA CONTEMPORÁNEO
glass_h("curtain_wall_pb1", 0.0, 2.40, 5.80, 0.22, 2.70, mat=M_GLASS_LUX)
glass_h("curtain_wall_pb2", 0.0, 6.80, 10.20, 0.22, 2.70, mat=M_GLASS_LUX)
glass_h("curtain_wall_pa1", 0.0, 2.40, 5.80, z_pa + 0.22, z_ha - 0.20, mat=M_GLASS_LUX)
glass_h("curtain_wall_pa2", 0.0, 6.80, 10.20, z_pa + 0.22, z_ha - 0.20, mat=M_GLASS_LUX)

# Lamas Brise-Soleil de protección solar en planta alta
for b in range(12):
    bx = 2.50 + b * 0.28
    cube(f"brise_soleil_{b}", bx - 0.03, bx + 0.03, -0.32, -0.18, z_pa + 0.20, z_ha - 0.10, M_BLACK_STEEL)

# ================================================================ PERGOLA BIOCLIMATICA DE ACERO Y MADERA
for p in range(14):
    py = 5.10 + p * 0.58
    cube(f"pergola_beam_{p}", 6.30, 11.50, py - 0.03, py + 0.03, 2.75, 2.88, M_WOOD_TECA)
cube("pergola_steel_l", 6.35, 6.45, 5.00, 12.90, 2.62, 2.75, M_BLACK_STEEL)
cube("pergola_steel_r", 11.35, 11.45, 5.00, 12.90, 2.62, 2.75, M_BLACK_STEEL)

# ================================================================ ILUMINACION ARQUITECTONICA FOSEADA LED
# Fajas de Luz LED en marco contemporáneo
cube("led_strip_facade_top", -0.20, 11.60, -0.30, -0.25, z_ha - 0.08, z_ha - 0.02, M_LED_FACADE)
cube("led_strip_facade_bottom", -0.20, 11.60, -0.30, -0.25, z_pa + 0.02, z_pa + 0.08, M_LED_FACADE)

# Bañadores de pared verticales LED cálidos
for w in range(4):
    wx = 0.5 + w * 3.2
    cube(f"wall_washer_{w}", wx - 0.10, wx + 0.10, -0.08, -0.04, 0.40, 2.60, M_LED_WARM)

# ================================================================ INTERIORISMO CONTEMPORÁNEO (ISLA MÁRMOL & MOBILIARIO)
# Isla de cocina de mármol Calacatta con cascada
cube("kitchen_island_marble", 6.50, 8.80, 3.90, 4.90, 0.0, 0.92, M_MARBLE)
cube("kitchen_island_top", 6.45, 8.85, 3.85, 4.95, 0.92, 0.96, M_MARBLE)
for s in [(6.8, 3.55), (7.5, 3.55), (8.2, 3.55)]:
    cylinder(f"lux_stool_seat_{s[0]}", s[0], s[1], 0.19, 0.64, 0.70, M_BLACK_STEEL, n=16)
    cylinder(f"lux_stool_base_{s[0]}", s[0], s[1], 0.03, 0.0, 0.64, M_BLACK_STEEL, n=10)

# Mueble de salón contemporáneo con panelado de madera e iluminación indirecta
cube("tv_panel_wood", 1.8, 4.4, 4.85, 4.98, 0.0, 2.70, M_WOOD_TECA)
cube("tv_screen_olect", 2.2, 4.0, 4.88, 4.96, 0.90, 1.80, M_BLACK_STEEL)
cube("tv_led_back", 1.8, 4.4, 4.84, 4.87, 0.0, 2.70, M_LED_WARM)

# Sofá modular contemporáneo en tono crema
sofa("lux_sofa", 1.9, 0.8, 2.8, 1.2, pbr_mat("_sofa_linen", (0.88, 0.86, 0.82), 0.9))

# Olivo Centenario en patio con macetón de microcemento
cylinder("olivo_pot_lux", 9.0, 9.0, 0.65, 0.08, 0.80, M_CONCRETE, n=20)
cylinder("olivo_trunk_lux", 9.0, 9.0, 0.12, 0.80, 1.80, M_WOOD_IPE, n=12)
uv_sphere("olivo_crown_1", 9.0, 9.0, 2.40, 1.10, pbr_mat("_leaf1", (0.28, 0.46, 0.24), 0.9), n=16)
uv_sphere("olivo_crown_2", 8.6, 9.3, 2.60, 0.75, pbr_mat("_leaf2", (0.22, 0.40, 0.20), 0.9), n=14)

# ================================================================ ESCALERA VOLADA DE DISEÑO
for step in range(16):
    sz = z_f + step * ((z_pa - z_f) / 16)
    sy = 0.0 + step * (5.00 / 16)
    cube(f"floating_step_{step}", 10.40, 11.35, sy, sy + 0.28, sz, sz + 0.08, M_WOOD_IPE)

# CUBIERTA & PARAPETO
cube("roof", 0.0, 11.40, 0.0, 17.60, z_ha, z_ha + 0.20, M_CONCRETE)
cube("parapet_cap_cinc", -0.20, 11.60, -0.40, 17.80, z_ha + 0.32, z_ha + 0.36, M_BLACK_STEEL)

# Guardar mainfile de Blender
OUT = r"C:\Users\Oscar Martinez\Desktop\mi-casa"
bpy.ops.wm.save_mainfile(filepath=os.path.join(OUT, "casa-bifamiliar-3d.blend"))

print("RECONSTRUCCION ARQUITECTURA CONTEMPORANEA DE LUJO COMPLETADA OK - Objetos:", len(bpy.data.objects))
