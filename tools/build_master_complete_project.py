# -*- coding: utf-8 -*-
"""
PROYECTO COMPLETO Y ACABADO - VIVIENDA BIFAMILIAR CONTEMPORÁNEA DE ALTO DISEÑO.
Incluye arquitectura completa, interiorismo de lujo por estancias, paisajismo,
materiales PBR texturizados y refresco automático de la interfaz gráfica de Blender.
"""
import os
import bpy
import math

OUT = r"C:\Users\Oscar Martinez\Desktop\mi-casa"
BLEND_FILE = os.path.join(OUT, "casa-bifamiliar-3d.blend")

# 1. Cargar biblioteca de funciones primitivas y helpers
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

# 2. LIMPIEZA TOTAL DE OBJETOS PREVIOS
for obj in list(bpy.data.objects):
    bpy.data.objects.remove(obj, do_unlink=True)
for mesh in list(bpy.data.meshes):
    bpy.data.meshes.remove(mesh)

# 3. CREACION DE MATERIALES PBR PROFESIONALES DE ALTA DEFINICIÓN
def pbr_mat(name, color=(0.8, 0.8, 0.8), rough=0.6, metal=0.0, spec=0.5,
            trans=0.0, ior=1.45, emit=0.0, bump=0.0, tex_scale=8.0):
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

# Materiales de Acabados de Lujo
M_FACHADA_BLANCA = pbr_mat("M_FACHADA_BLANCA", (0.96, 0.95, 0.93), 0.5, bump=0.008)
M_ANTRACITA      = pbr_mat("M_ANTRACITA", (0.12, 0.13, 0.15), 0.3, metal=0.8)
M_MADERA_IPE     = pbr_mat("M_MADERA_IPE", (0.64, 0.44, 0.28), 0.35, spec=0.5, bump=0.03)
M_MADERA_ROBLE   = pbr_mat("M_MADERA_ROBLE", (0.72, 0.54, 0.36), 0.38, spec=0.4, bump=0.03)
M_SUELO_PARQUET  = pbr_mat("M_SUELO_PARQUET", (0.68, 0.50, 0.32), 0.30, spec=0.5, bump=0.04, tex_scale=12.0)
M_SUELO_CERAMICO = pbr_mat("M_SUELO_CERAMICO", (0.85, 0.84, 0.81), 0.20, spec=0.6, bump=0.005)
M_MARMOL_GOLD    = pbr_mat("M_MARMOL_GOLD", (0.95, 0.94, 0.92), 0.12, spec=0.85, bump=0.003)
M_VIDRIO_TEMPLADO= pbr_mat("M_VIDRIO_TEMPLADO", (0.75, 0.92, 0.96), 0.02, spec=1.0, trans=0.98, ior=1.52)
M_VIDRIO_AHUMADO = pbr_mat("M_VIDRIO_AHUMADO", (0.20, 0.22, 0.25), 0.05, spec=0.9, trans=0.60, ior=1.52)
M_ACERO_NEGRO    = pbr_mat("M_ACERO_NEGRO", (0.08, 0.09, 0.10), 0.25, metal=0.95)
M_CONCRETO       = pbr_mat("M_CONCRETO", (0.76, 0.74, 0.71), 0.8, bump=0.02)
M_LED_WARM       = pbr_mat("M_LED_WARM", (1.0, 0.92, 0.78), 0.1, emit=30.0)
M_LED_COOL       = pbr_mat("M_LED_COOL", (0.92, 0.96, 1.0), 0.1, emit=35.0)
M_WATER          = pbr_mat("M_WATER", (0.35, 0.65, 0.75), 0.05, spec=1.0, trans=0.85, ior=1.33)
M_SOFA_TEXTIL    = pbr_mat("M_SOFA_TEXTIL", (0.85, 0.83, 0.78), 0.9, spec=0.1)
M_ALFOMBRA       = pbr_mat("M_ALFOMBRA", (0.75, 0.72, 0.66), 0.95, bump=0.06, tex_scale=20.0)
M_CESPED         = pbr_mat("M_CESPED", (0.32, 0.50, 0.26), 1.0, bump=0.05, tex_scale=15.0)
M_HOJAS          = pbr_mat("M_HOJAS", (0.28, 0.48, 0.24), 0.9)
M_TRONCO         = pbr_mat("M_TRONCO", (0.44, 0.34, 0.25), 0.9, bump=0.04)

z_f = 0.22; z_hb = 2.90; z_pa = 2.90; z_ha = 5.80

# 4. ENTORNO URBANIZADO Y PARCELA
cube("road_front", -4.0, 14.4, -12.0, -1.2, 0.0, 0.16, pbr_mat("_road", (0.28, 0.29, 0.31), 0.9))
cube("sidewalk_front", -3.0, 14.4, -1.2, 0.0, 0.0, 0.12, M_CONCRETO)
cube("road_rear", -4.0, 14.4, 17.6, 28.0, 0.0, 0.16, pbr_mat("_road2", (0.28, 0.29, 0.31), 0.9))
cube("sidewalk_rear", -3.0, 14.4, 17.6, 18.8, 0.0, 0.12, M_CONCRETO)
cube("ground_plot", -3.0, 14.4, 0.0, 17.6, -0.06, 0.0, M_CONCRETO)

# Pavimento Porcelánico Continuo en PB y Parquet en PA
cube("floor_pb", 0.0, 11.40, 0.0, 17.60, 0.15, 0.22, M_SUELO_CERAMICO)
cube("floor_pa", 0.0, 11.40, 0.0, 17.60, z_hb, z_hb + 0.10, M_SUELO_PARQUET)

# Patio exterior con Tarima de Exterior y Lámina de Agua (Piscina/Estanque)
cube("patio_deck", 6.40, 11.40, 5.00, 13.00, 0.0, 0.08, M_MADERA_IPE)
plane("patio_water", [(7.0, 7.0), (10.8, 7.0), (10.8, 11.0), (7.0, 11.0)], M_WATER, z=0.06)

# 5. MUROS Y ESTRUCTURA DE DISEÑO CONTEMPORÁNEO
wall_h("M_pb_front", (0.0, 0.0, 11.40), [(0.30, 1.30), (2.40, 5.80), (6.80, 10.20)], z_f, z_hb, M_FACHADA_BLANCA)
wall_h("M_pb_rear", (17.60, 0.0, 11.40), [(0.80, 2.40), (3.60, 5.20), (8.60, 11.00)], z_f, z_hb, M_FACHADA_BLANCA)
wall_v("M_pb_l", (0.0, 0.0, 17.60), [], z_f, z_hb, M_ANTRACITA)
wall_v("M_pb_rf", (11.40, 0.0, 5.00), [], z_f, z_hb, M_FACHADA_BLANCA)
wall_v("M_pb_rpatio", (11.40, 5.00, 13.00), [], z_f, z_hb, M_ANTRACITA)
wall_v("M_pb_rr", (11.40, 13.00, 17.60), [], z_f, z_hb, M_FACHADA_BLANCA)

# Tabiquería Interior Planta Baja
wall_v("T_pb1", (1.40, 0.0, 13.00), [(1.40, 4.60), (6.10, 6.80), (7.90, 8.60)], z_f, z_hb, M_FACHADA_BLANCA)
wall_v("T_pb2", (6.40, 0.0, 5.00), [(1.00, 4.40)], z_f, z_hb, M_FACHADA_BLANCA)
wall_v("T_pb4", (6.40, 7.40, 13.00), [(7.80, 8.40), (9.00, 9.60)], z_f, z_hb, M_FACHADA_BLANCA)
wall_h("T_pb5", (5.00, 6.40, 11.40), [(6.40, 10.40)], z_f, z_hb, M_FACHADA_BLANCA)

# Planta Alta - Muros exteriores
wall_h("M_pa_front", (0.0, 0.0, 11.40), [(2.40, 5.80), (6.80, 10.20)], z_pa, z_ha, M_FACHADA_BLANCA)
wall_h("M_pa_rear", (17.60, 0.0, 11.40), [(3.60, 5.20), (7.00, 11.00)], z_pa, z_ha, M_FACHADA_BLANCA)
wall_v("M_pa_l", (0.0, 0.0, 17.60), [], z_pa, z_ha, M_ANTRACITA)
wall_v("M_pa_rf", (11.40, 0.0, 5.00), [], z_pa, z_ha, M_FACHADA_BLANCA)

# 6. VOLUMETRÍA CONTEMPORÁNEA & VOLADIZO
cube("voladizo_top_n", -0.20, 11.60, -0.40, 0.20, z_ha - 0.10, z_ha + 0.35, M_ANTRACITA)
cube("voladizo_top_w", -0.40, 0.0, -0.40, 5.20, z_pa - 0.10, z_ha + 0.35, M_ANTRACITA)
cube("voladizo_top_e", 11.40, 11.80, -0.40, 5.20, z_pa - 0.10, z_ha + 0.35, M_ANTRACITA)
cube("voladizo_bottom", -0.40, 11.80, -0.40, 0.20, z_pa - 0.10, z_pa + 0.10, M_ANTRACITA)

# Panelado de Madera en Acceso
for k in range(16):
    zx = 0.25 + k * 0.15
    cube(f"panel_madera_acceso_{k}", zx - 0.02, zx + 0.02, -0.15, -0.02, z_f, z_hb, M_MADERA_IPE)

# Lamas Brise-Soleil de Filtro Solar en Planta Alta
for b in range(12):
    bx = 2.50 + b * 0.28
    cube(f"brise_soleil_{b}", bx - 0.03, bx + 0.03, -0.32, -0.18, z_pa + 0.20, z_ha - 0.10, M_ACERO_NEGRO)

# Pérgola Bioclimática en Patio Central
for p in range(14):
    py = 5.10 + p * 0.58
    cube(f"pergola_viga_{p}", 6.30, 11.50, py - 0.03, py + 0.03, 2.75, 2.88, M_MADERA_ROBLE)
cube("pergola_acero_l", 6.35, 6.45, 5.00, 12.90, 2.62, 2.75, M_ACERO_NEGRO)
cube("pergola_acero_r", 11.35, 11.45, 5.00, 12.90, 2.62, 2.75, M_ACERO_NEGRO)

# Carpinterías con Grandes Ventanales
glass_h("ventanal_pb1", 0.0, 2.40, 5.80, 0.22, 2.70, mat=M_VIDRIO_TEMPLADO)
glass_h("ventanal_pb2", 0.0, 6.80, 10.20, 0.22, 2.70, mat=M_VIDRIO_TEMPLADO)
glass_h("ventanal_pa1", 0.0, 2.40, 5.80, z_pa + 0.22, z_ha - 0.20, mat=M_VIDRIO_TEMPLADO)
glass_h("ventanal_pa2", 0.0, 6.80, 10.20, z_pa + 0.22, z_ha - 0.20, mat=M_VIDRIO_TEMPLADO)
door_h("puerta_principal", 0.0, 0.30, 1.30, mat=M_MADERA_IPE)

# 7. INTERIORISMO Y DECORACIÓN MODERNA COMPLETA

# --- SALÓN DE ESTAR
sofa("salon_sofa_modular", 1.9, 0.8, 2.8, 1.2, M_SOFA_TEXTIL)
cube("salon_alfombra_boucle", 1.8, 4.4, 0.6, 3.2, 0.22, 0.25, M_ALFOMBRA)
table("salon_mesa_centro", 3.1, 2.0, 1.2, 0.7, 0.42, M_MADERA_ROBLE, M_ACERO_NEGRO)
tv("salon_tv_oiled", 2.5, 4.9, 1.8, 0.9)
cube("salon_panel_tv", 1.8, 4.4, 4.88, 4.98, 0.22, 2.70, M_MADERA_ROBLE)
cube("salon_led_tv", 1.8, 4.4, 4.84, 4.87, 0.22, 2.70, M_LED_WARM)

# --- COCINA DE DISEÑO CON ISLA Y COMEDOR
kitchen_units("cocina_modulos", 6.7, 10.4, 0.2, 0.22, mat_body=M_ANTRACITA)
cube("isla_marmol_base", 6.50, 8.80, 3.90, 4.90, 0.22, 0.92, M_MARMOL_GOLD)
cube("isla_marmol_top", 6.45, 8.85, 3.85, 4.95, 0.92, 0.96, M_MARMOL_GOLD)

# Taburetes de barra de cocina
for sx in [6.8, 7.5, 8.2]:
    cylinder(f"taburete_asiento_{sx}", sx, 3.55, 0.19, 0.65, 0.70, M_ACERO_NEGRO, n=14)
    cylinder(f"taburete_patas_{sx}", sx, 3.55, 0.03, 0.22, 0.65, M_ACERO_NEGRO, n=8)

# Mesa de Comedor para 6 comensales
table("comedor_mesa", 8.9, 6.3, 1.8, 1.0, 0.75, M_MADERA_ROBLE, M_ACERO_NEGRO)
for cx in [8.2, 8.9, 9.6]:
    chair(f"comedor_silla_n_{cx}", cx, 5.6, M_SOFA_TEXTIL)
    chair(f"comedor_silla_s_{cx}", cx, 7.0, M_SOFA_TEXTIL)

# --- ESCALERA VOLADA
for step in range(16):
    sz = z_f + step * ((z_pa - z_f) / 16)
    sy = 0.0 + step * (5.00 / 16)
    cube(f"escalera_peldaño_{step}", 10.40, 11.35, sy, sy + 0.28, sz, sz + 0.08, M_MADERA_IPE)

# --- DORMITORIO PRINCIPAL (SUITE PA)
z_b = z_pa + 0.10
bed("dorm_suite_cama", 3.9, 3.0, 1.9, 2.1, color=M_SOFA_TEXTIL)
wardrobe("dorm_suite_vestidor", 1.7, 0.4, 2.0, 0.6, 2.4, color=M_ANTRACITA)
cube("suite_cabecero_led", 2.8, 5.0, 1.85, 1.95, z_b, z_b + 1.20, M_LED_WARM)

# --- BAÑO DE DISEÑO
toilet("banio_wc_suspendido", 5.4, 13.4, color=(0.95, 0.95, 0.95))
sink("banio_lavabo_doble", 5.0, 13.9, color=(0.90, 0.90, 0.88))
shower("banio_ducha_italiana", 6.0, 13.3, 0.9)

# --- VEGETACION Y PAISAJISMO
cylinder("olivo_maceta", 9.0, 9.0, 0.65, 0.08, 0.80, M_CONCRETO, n=20)
cylinder("olivo_tronco", 9.0, 9.0, 0.12, 0.80, 1.80, M_TRONCO, n=12)
uv_sphere("olivo_copa1", 9.0, 9.0, 2.40, 1.10, M_HOJAS, n=16)
uv_sphere("olivo_copa2", 8.6, 9.3, 2.60, 0.75, M_HOJAS, n=14)

tree("arbol_entrada", -1.5, -3.5, 1.5)
tree("arbol_trasero", 12.5, 20.5, 1.6)

# --- ILUMINACION LED FOSEADA DE ARQUITECTURA
cube("led_fachada_superior", -0.20, 11.60, -0.30, -0.25, z_ha - 0.08, z_ha - 0.02, M_LED_COOL)
cube("led_fachada_inferior", -0.20, 11.60, -0.30, -0.25, z_pa + 0.02, z_pa + 0.08, M_LED_COOL)

# 8. CAMARAS PROFESIONALES
def create_cam(name, loc, target, lens=32.0):
    cd = bpy.data.cameras.new(name)
    cd.lens = lens
    cd.sensor_width = 36.0
    obj = bpy.data.objects.new(name, cd)
    bpy.context.scene.collection.objects.link(obj)
    obj.location = loc
    empty = bpy.data.objects.new(name + "_target", None)
    bpy.context.scene.collection.objects.link(empty)
    empty.location = target
    tc = obj.constraints.new("TRACK_TO")
    tc.target = empty
    tc.track_axis = "TRACK_NEGATIVE_Z"
    tc.up_axis = "UP_Y"
    return obj

create_cam("cam_fachada_principal", (4.0, -8.0, 1.7), (5.7, 4.0, 2.0), 32.0)
create_cam("cam_axo_3d", (19.0, -14.0, 15.0), (5.7, 8.8, 2.0), 30.0)
create_cam("cam_interior_salon", (2.6, -0.8, 1.6), (3.8, 3.0, 1.2), 24.0)

bpy.context.scene.camera = bpy.data.objects.get("cam_fachada_principal")


# 9. GUARDAR ARCHIVO MAINFILE DE BLENDER
bpy.ops.wm.save_mainfile(filepath=BLEND_FILE)
print("PROYECTO COMPLETO GUARDADO EN:", BLEND_FILE, "- Objetos:", len(bpy.data.objects))
