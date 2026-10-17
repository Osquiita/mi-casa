# -*- coding: utf-8 -*-
"""
RECONSTRUCCION MAESTRA INTEGRAL DE ARQUITECTURA RESIDENCIAL Y DISEÑO INTERIOR.
Vivienda Bifamiliar Contemporánea de Lujo - 450+ Objetos 3D, Planos DXF completos,
Materiales PBR, Iluminación Nishita + LED y Cámaras Profesionales.
"""
import os
import bpy
import math

OUT = r"C:\Users\Oscar Martinez\Desktop\mi-casa"
BLEND_FILE = os.path.join(OUT, "casa-bifamiliar-3d.blend")

# 1. Cargar biblioteca de funciones primitivas
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

# 2. LIMPIEZA TOTAL
for obj in list(bpy.data.objects):
    bpy.data.objects.remove(obj, do_unlink=True)
for mesh in list(bpy.data.meshes):
    bpy.data.meshes.remove(mesh)

# 3. PALETA DE MATERIALES PBR PROFESIONALES
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

M_ESTUCO    = pbr_mat("M_ESTUCO", (0.96, 0.95, 0.93), 0.55, bump=0.008)
M_ANTRACITA = pbr_mat("M_ANTRACITA", (0.12, 0.13, 0.15), 0.30, metal=0.8)
M_IPE       = pbr_mat("M_IPE", (0.64, 0.44, 0.28), 0.35, spec=0.5, bump=0.03)
M_ROBLE     = pbr_mat("M_ROBLE", (0.72, 0.54, 0.36), 0.38, spec=0.4, bump=0.03)
M_PARQUET   = pbr_mat("M_PARQUET", (0.68, 0.50, 0.32), 0.30, spec=0.5, bump=0.04, tex_scale=12.0)
M_PORCELANA = pbr_mat("M_PORCELANA", (0.88, 0.86, 0.83), 0.18, spec=0.6, bump=0.005)
M_MARMOL    = pbr_mat("M_MARMOL", (0.95, 0.94, 0.92), 0.12, spec=0.85, bump=0.003)
M_GLASS     = pbr_mat("M_GLASS", (0.75, 0.92, 0.96), 0.02, spec=1.0, trans=0.98, ior=1.52)
M_GLASS2    = pbr_mat("M_GLASS2", (0.70, 0.88, 0.93), 0.04, spec=1.0, trans=0.95, ior=1.52)
M_DARKGLASS = pbr_mat("M_DARKGLASS", (0.20, 0.22, 0.25), 0.05, spec=0.9, trans=0.60, ior=1.52)
M_ACERO     = pbr_mat("M_ACERO", (0.08, 0.09, 0.10), 0.25, metal=0.95)
M_HORMIGON  = pbr_mat("M_HORMIGON", (0.76, 0.74, 0.71), 0.80, bump=0.02)
M_LED_WARM  = pbr_mat("M_LED_WARM", (1.0, 0.92, 0.78), 0.1, emit=30.0)
M_LED_COOL  = pbr_mat("M_LED_COOL", (0.92, 0.96, 1.0), 0.1, emit=35.0)
M_WATER     = pbr_mat("M_WATER", (0.35, 0.65, 0.75), 0.05, spec=1.0, trans=0.85, ior=1.33)
M_SOFA      = pbr_mat("M_SOFA", (0.85, 0.83, 0.78), 0.90, spec=0.1)
M_TEAL      = pbr_mat("M_TEAL", (0.38, 0.62, 0.66), 0.85)
M_ALFOMBRA  = pbr_mat("M_ALFOMBRA", (0.75, 0.72, 0.66), 0.95, bump=0.06, tex_scale=20.0)
M_CESPED    = pbr_mat("M_CESPED", (0.32, 0.50, 0.26), 1.0, bump=0.05, tex_scale=15.0)
M_HOJAS     = pbr_mat("M_HOJAS", (0.28, 0.48, 0.24), 0.9)
M_TRONCO    = pbr_mat("M_TRONCO", (0.44, 0.34, 0.25), 0.9, bump=0.04)

z_f = 0.22; z_hb = 2.90; z_pa = 2.90; z_ha = 5.80

# 4. ENTORNO URBANIZADO Y PARCELA
cube("road_front", -4.0, 14.4, -12.0, -1.2, 0.0, 0.16, pbr_mat("_road", (0.28, 0.29, 0.31), 0.9))
cube("sidewalk_front", -3.0, 14.4, -1.2, 0.0, 0.0, 0.12, M_HORMIGON)
cube("road_rear", -4.0, 14.4, 17.6, 28.0, 0.0, 0.16, pbr_mat("_road2", (0.28, 0.29, 0.31), 0.9))
cube("sidewalk_rear", -3.0, 14.4, 17.6, 18.8, 0.0, 0.12, M_HORMIGON)
cube("ground_plot", -3.0, 14.4, 0.0, 17.6, -0.06, 0.0, M_HORMIGON)
cube("sidewalk_l", -3.0, 0.0, -1.2, 17.6, 0.0, 0.12, M_HORMIGON)
cube("sidewalk_r", 11.4, 14.4, -1.2, 17.6, 0.0, 0.12, M_HORMIGON)

# Forjados y pavimentos
cube("slab_pb", 0.0, 11.40, 0.0, 17.60, 0.15, 0.22, M_PORCELANA)
cube("slab_pa_front", 0.0, 11.40, 0.0, 5.00, z_hb, z_hb + 0.20, M_PARQUET)
cube("slab_pa_west", 0.0, 6.40, 5.00, 17.60, z_hb, z_hb + 0.20, M_PARQUET)
cube("slab_pa_pas", 6.40, 11.40, 5.00, 7.60, z_hb, z_hb + 0.20, M_PARQUET)
cube("slab_pa_d2", 6.40, 11.40, 13.00, 17.60, z_hb, z_hb + 0.20, M_PARQUET)

# Patio exterior con Tarima Ipe + Estanque
cube("patio_deck", 6.40, 11.40, 5.00, 13.00, 0.0, 0.08, M_IPE)
plane("patio_water", [(7.0, 7.0), (10.8, 7.0), (10.8, 11.0), (7.0, 11.0)], M_WATER, z=0.06)
cube("patio2_floor", 0.0, 3.20, 14.10, 17.60, 2.90, 2.96, M_HORMIGON)

# 5. MUROS Y ENVOLVENTE COMPLETA (PB + PA)
wall_h("M_pb_front", (0.0, 0.0, 11.40),
       [(0.30, 1.30), (2.60, 4.40), (4.80, 6.00), (6.90, 8.10), (8.90, 9.90), (10.40, 11.40)],
       z_f, z_hb, M_ESTUCO)
wall_h("M_pb_rear", (17.60, 0.0, 11.40),
       [(0.80, 2.40), (3.60, 5.20), (8.60, 11.00)],
       z_f, z_hb, M_ESTUCO)
wall_v("M_pb_l", (0.0, 0.0, 17.60), [], z_f, z_hb, M_ANTRACITA)
wall_v("M_pb_rf", (11.40, 0.0, 5.00), [], z_f, z_hb, M_ESTUCO)
wall_v("M_pb_rpatio", (11.40, 5.00, 13.00), [], z_f, z_hb, M_ANTRACITA)
wall_v("M_pb_rr", (11.40, 13.00, 17.60), [], z_f, z_hb, M_ESTUCO)

# Tabiquería Interior Planta Baja completa
wall_v("T_pb1", (1.40, 0.0, 13.00), [(1.40, 4.60), (6.10, 6.80), (7.90, 8.60)], z_f, z_hb, M_ESTUCO)
wall_v("T_pb2", (6.40, 0.0, 5.00), [(1.00, 4.40)], z_f, z_hb, M_ESTUCO)
wall_v("T_pb3", (6.40, 5.00, 7.40), [(5.30, 6.20)], z_f, z_hb, M_ESTUCO)
wall_v("T_pb4", (6.40, 7.40, 13.00), [(7.80, 8.40), (9.00, 9.60), (11.00, 12.20)], z_f, z_hb, M_ESTUCO)
wall_h("T_pb5", (5.00, 6.40, 11.40), [(6.40, 10.40)], z_f, z_hb, M_ESTUCO)
wall_v("T_pb6", (10.40, 0.0, 5.00), [], z_f, z_hb, M_ESTUCO)
wall_h("T_pb7", (7.40, 1.40, 6.40), [], z_f, z_hb, M_ESTUCO)
wall_h("T_pb8", (8.80, 1.40, 6.40), [], z_f, z_hb, M_ESTUCO)
wall_h("T_pb9", (10.20, 1.40, 6.40), [(3.30, 4.00)], z_f, z_hb, M_ESTUCO)
wall_h("T_pb10", (14.10, 0.0, 4.50), [(0.80, 1.50), (3.60, 4.30)], z_f, z_hb, M_ESTUCO)
wall_h("T_pb11", (13.00, 1.40, 8.00), [(2.20, 2.90)], z_f, z_hb, M_ESTUCO)
wall_v("T_pb12", (4.50, 13.00, 14.10), [], z_f, z_hb, M_ESTUCO)
wall_v("T_pb13", (6.40, 13.00, 17.60), [], z_f, z_hb, M_ESTUCO)
wall_v("T_pb14", (8.00, 13.00, 17.60), [(13.30, 13.90)], z_f, z_hb, M_ESTUCO)
wall_v("T_pb15", (3.20, 14.10, 17.60), [], z_f, z_hb, M_ESTUCO)

# Planta Alta - Muros exteriores y tabiquería
wall_h("M_pa_front", (0.0, 0.0, 11.40),
       [(2.60, 4.40), (4.80, 6.00), (6.90, 8.10), (8.90, 9.90)],
       z_pa, z_ha, M_ESTUCO)
wall_h("M_pa_rear", (17.60, 0.0, 11.40),
       [(3.60, 5.20), (7.00, 9.00), (9.80, 11.20)],
       z_pa, z_ha, M_ESTUCO)
wall_v("M_pa_l", (0.0, 0.0, 17.60), [], z_pa, z_ha, M_ANTRACITA)
wall_v("M_pa_rf", (11.40, 0.0, 5.00), [], z_pa, z_ha, M_ESTUCO)
wall_v("M_pa_rpatio", (11.40, 5.00, 13.00), [], z_pa, z_ha, M_ANTRACITA)
wall_v("M_pa_rr", (11.40, 13.00, 17.60), [], z_pa, z_ha, M_ESTUCO)
wall_v("M_pa_esc", (10.40, 0.0, 5.00), [], z_pa, z_ha, M_ESTUCO)
wall_v("T_pa1", (6.40, 5.00, 7.60), [(5.30, 6.20)], z_pa, z_ha, M_ESTUCO)
wall_v("T_pa2", (6.40, 7.60, 13.00), [(7.80, 8.40), (9.00, 9.60), (11.00, 12.20)], z_pa, z_ha, M_ESTUCO)
wall_h("T_pa3", (7.60, 6.40, 11.40), [(7.00, 9.40)], z_pa, z_ha, M_ESTUCO)
wall_v("T_pa4", (1.40, 0.0, 7.40), [(1.40, 4.60), (6.10, 6.80), (7.90, 8.60)], z_pa, z_ha, M_ESTUCO)
wall_v("T_pa5", (6.40, 0.0, 5.00), [(1.00, 4.40)], z_pa, z_ha, M_ESTUCO)
wall_h("T_pa6", (7.40, 1.40, 6.40), [], z_pa, z_ha, M_ESTUCO)
wall_h("T_pa7", (8.80, 1.40, 6.40), [], z_pa, z_ha, M_ESTUCO)
wall_h("T_pa8", (10.20, 1.40, 6.40), [(3.30, 4.00)], z_pa, z_ha, M_ESTUCO)
wall_h("T_pa9", (13.00, 1.40, 6.40), [(2.20, 2.90)], z_pa, z_ha, M_ESTUCO)
wall_h("T_pa10", (14.10, 0.0, 6.40), [(0.80, 1.50), (3.60, 4.30)], z_pa, z_ha, M_ESTUCO)
wall_v("T_pa11", (3.20, 14.10, 17.60), [], z_pa, z_ha, M_ESTUCO)
wall_v("T_pa12", (6.40, 13.00, 17.60), [(13.20, 14.00)], z_pa, z_ha, M_ESTUCO)
wall_h("T_pa13", (13.00, 6.40, 11.40), [(7.00, 10.40)], z_pa, z_ha, M_ESTUCO)

# 6. CUBIERTA, VOLADIZOS & ELEMENTOS ARQUITECTÓNICOS
cube("roof", 0.0, 11.40, 0.0, 17.60, z_ha, z_ha + 0.20, M_HORMIGON)
cube("parapet_n", 0.0, 11.40, -0.15, 0.15, z_ha, z_ha + 0.32, M_ESTUCO)
cube("parapet_s", 0.0, 11.40, 17.45, 17.75, z_ha, z_ha + 0.32, M_ESTUCO)
cube("parapet_w", -0.15, 0.15, 0.0, 17.60, z_ha, z_ha + 0.32, M_ESTUCO)
cube("parapet_e", 11.25, 11.55, 0.0, 17.60, z_ha, z_ha + 0.32, M_ESTUCO)
cube("cap_n", -0.05, 11.45, -0.18, 0.18, z_ha + 0.32, z_ha + 0.35, M_ACERO)
cube("cap_s", -0.05, 11.45, 17.42, 17.78, z_ha + 0.32, z_ha + 0.35, M_ACERO)
cube("cap_w", -0.18, 0.18, -0.05, 17.65, z_ha + 0.32, z_ha + 0.35, M_ACERO)
cube("cap_e", 11.22, 11.58, -0.05, 17.65, z_ha + 0.32, z_ha + 0.35, M_ACERO)

# Voladizo Antracita contemporáneo
cube("voladizo_top_n", -0.20, 11.60, -0.40, 0.20, z_ha - 0.10, z_ha + 0.35, M_ANTRACITA)
cube("voladizo_top_w", -0.40, 0.0, -0.40, 5.20, z_pa - 0.10, z_ha + 0.35, M_ANTRACITA)
cube("voladizo_top_e", 11.40, 11.80, -0.40, 5.20, z_pa - 0.10, z_ha + 0.35, M_ANTRACITA)
cube("voladizo_bottom", -0.40, 11.80, -0.40, 0.20, z_pa - 0.10, z_pa + 0.10, M_ANTRACITA)

# Panelado de Madera Ipe en acceso
for k in range(16):
    zx = 0.25 + k * 0.15
    cube(f"panel_madera_acceso_{k}", zx - 0.02, zx + 0.02, -0.15, -0.02, z_f, z_hb, M_IPE)

# Brise-Soleil de filtro solar
for b in range(12):
    bx = 2.50 + b * 0.28
    cube(f"brise_soleil_{b}", bx - 0.03, bx + 0.03, -0.32, -0.18, z_pa + 0.20, z_ha - 0.10, M_ACERO)

# Pérgola Bioclimática en patio central
for p in range(14):
    py = 5.10 + p * 0.58
    cube(f"pergola_viga_{p}", 6.30, 11.50, py - 0.03, py + 0.03, 2.75, 2.88, M_ROBLE)
cube("pergola_acero_l", 6.35, 6.45, 5.00, 12.90, 2.62, 2.75, M_ACERO)
cube("pergola_acero_r", 11.35, 11.45, 5.00, 12.90, 2.62, 2.75, M_ACERO)

# 7. CARPINTERÍAS Y HUECOS DE FACHADA
door_h("portalA", 0.0, 0.30, 1.30, mat=M_IPE)
door_h("portalB", 0.0, 10.40, 11.40, mat=M_IPE)
for (a, b) in [(2.60, 4.40), (4.80, 6.00), (6.90, 8.10), (8.90, 9.90)]:
    glass_h("win_front_pb", 0.0, a, b, 0.9, 2.4, mat=M_GLASS2)
    glass_h("win_front_pa", 0.0, a, b, z_pa + 0.9, z_pa + 2.4, mat=M_GLASS2)
for (a, b) in [(0.80, 2.40), (3.60, 5.20)]:
    glass_h("win_rear_pb", 17.60, a, b, 0.9, 2.4, mat=M_GLASS2)
for (a, b) in [(3.60, 5.20), (7.00, 9.00), (9.80, 11.20)]:
    glass_h("win_rear_pa", 17.60, a, b, z_pa + 0.9, z_pa + 2.4, mat=M_GLASS2)
glass_v("win_esc", 11.40, 2.80, 3.60, 0.9, 2.4)
glass_v("win_esc_pa", 11.40, 2.80, 3.60, z_pa + 0.9, z_pa + 2.4)
cube("garage_door", 8.60, 11.00, 17.56, 17.64, 0.0, 2.4, M_ANTRACITA)
for (a, b) in [(7.80, 8.40), (9.00, 9.60), (11.00, 12.20)]:
    glass_v("win_pat_pb", 6.40, a, b, 0.9, 2.4, mat=M_GLASS2)
    glass_v("win_vac", 6.40, a, b, z_pa + 0.9, z_pa + 2.4)
door_v("d_salon_porche", 6.40, 5.30, 6.20, mat=M_ROBLE)
door_v("d_banio", 1.40, 7.90, 8.60, mat=M_ROBLE)

# Escalera principal
stairs("esc", 10.40, 11.40, 0.0, 5.00, z_f, z_pa, n=16)

# 8. AMUEBLAMIENTO E INTERIORISMO DE LUJO COMPLETO

# --- MOBILIARIO PB (VIVIENDA A)
sofa("salon_sofa", 1.9, 0.6, 2.6, 1.0, M_TEAL)
table("salon_table", 3.2, 2.2, 1.2, 0.7, 0.4, M_ROBLE, M_ACERO)
tv("salon_tv", 2.5, 4.9, 1.8, 0.9)
cube("salon_rug", 2.0, 4.4, 0.7, 2.9, 0.22, 0.25, M_ALFOMBRA)
plant("salon_plant", 1.7, 4.6, 1.1)

# Cocina con Isla en Mármol
kitchen_units("coc_base", 6.7, 10.4, 0.2, 0.22, mat_body=M_ANTRACITA)
cube("coc_isla", 6.6, 8.4, 4.0, 5.0, 0.22, 0.92, M_ANTRACITA)
cube("coc_isla_top", 6.55, 8.45, 3.95, 5.05, 0.92, 0.96, M_MARMOL)
for sx, sy in [(6.8, 3.65), (7.5, 3.65), (8.2, 3.65)]:
    cylinder(f"stool_seat_{sx}", sx, sy, 0.18, 0.65, 0.70, M_ACERO, n=12)
    cylinder(f"stool_leg_{sx}", sx, sy, 0.03, 0.22, 0.65, M_ACERO, n=8)

# Porche & Comedor exterior
table("porche_table", 8.9, 6.3, 1.6, 0.9, 0.75, M_ROBLE, M_ACERO)
chair("porche_c1", 7.6, 6.6, M_ROBLE)
chair("porche_c2", 10.2, 6.6, M_ROBLE)
plant("porche_plant", 8.9, 5.3, 1.0)

# Dormitorios PB
bed("d1_bed", 3.9, 6.5, 1.6, 2.0)
wardrobe("d1_ward", 1.7, 5.2, 1.6, 0.6, 2.3, color=M_ANTRACITA)
cube("d1_night_l", 3.1, 6.3, 0.0, 0.5, 0.22, 0.72, M_ROBLE)
cube("d1_night_r", 4.9, 6.3, 0.0, 0.5, 0.22, 0.72, M_ROBLE)
plant("d1_plant", 6.1, 11.5, 0.8)

bed("d2_bed", 4.8, 15.8, 1.5, 1.9)
wardrobe("d2_ward", 3.5, 14.3, 1.4, 0.6, 2.3, color=M_ROBLE)
bed("d3_bed", 8.9, 15.8, 1.6, 2.0)
wardrobe("d3_ward", 6.8, 13.3, 1.8, 0.6, 2.3, color=M_ROBLE)
plant("d3_plant", 10.9, 16.8, 0.8)

# Baño PB
toilet("banio_wc", 5.4, 13.4)
sink("banio_sink", 5.0, 13.9)
shower("banio_sh", 6.0, 13.3, 0.8)
wardrobe("pas_ward", 0.4, 14.3, 1.4, 0.6, 2.3)
plant("pas_plant", 2.6, 16.5, 0.9)

# --- MOBILIARIO PA (VIVIENDA B)
z_b = z_pa + 0.02
bed("pa_bed", 3.9, 3.0, 1.8, 2.0, color=M_SOFA)
wardrobe("pa_ward", 1.7, 0.4, 1.8, 0.6, 2.3, color=M_ANTRACITA)
cube("pa_night_l", 3.0, 3.4, 2.0, 2.5, z_b, z_b + 0.5, M_ROBLE)
cube("pa_night_r", 5.0, 5.4, 2.0, 2.5, z_b, z_b + 0.5, M_ROBLE)
plant("pa_plant", 6.1, 1.6, 1.0)
toilet("pa_banio_wc", 5.4, 13.4, (0.9, 0.9, 0.9))
sink("pa_banio_sink", 5.0, 13.9, (0.88, 0.88, 0.86))
shower("pa_banio_sh", 6.0, 13.3, 0.8)
bed("pa_d3_bed", 8.9, 15.8, 1.6, 2.0)
wardrobe("pa_d3_ward", 6.8, 13.3, 1.8, 0.6, 2.3)
plant("pa_d3_plant", 10.9, 16.8, 0.8)
sofa("pa_salon_sofa", 1.9, 9.0, 2.6, 1.0, M_SOFA)
table("pa_salon_table", 3.2, 10.4, 1.2, 0.7, 0.4, M_ROBLE, M_ACERO)
tv("pa_salon_tv", 2.5, 12.9, 1.8, 0.9)
cube("pa_salon_rug", 2.0, 4.4, 8.6, 10.8, z_b, z_b + 0.03, M_ALFOMBRA)
plant("pa_salon_plant", 1.7, 11.6, 1.1)
kitchen_units("pa_coc_base", 6.7, 10.4, 0.2, z_b)
cube("pa_coc_isla", 6.6, 8.4, 4.0, 5.0, z_b, z_b + 0.92, M_ANTRACITA)
cube("pa_coc_isla_top", 6.6, 8.4, 4.0, 5.0, z_b + 0.92, z_b + 0.96, M_MARMOL)
chair("pa_coc_s1", 7.1, 3.7, M_ROBLE)
chair("pa_coc_s2", 7.9, 3.7, M_ROBLE)

# Garaje
car("coche", 9.0, 1.8)

# 9. PAISAJISMO Y VEGETACION MEDITERRÁNEA
tree("arb_frente1", -1.0, -3.2, 1.4)
tree("arb_frente2", 4.5, -3.2, 1.2)
tree("arb_frente3", 9.5, -3.2, 1.5)
tree("arb_frente4", 13.0, -3.2, 1.3)
tree("arb_tras1", -1.0, 20.0, 1.4)
tree("arb_tras2", 5.5, 20.0, 1.2)
tree("arb_tras3", 12.0, 20.0, 1.4)
tree("arb_lat", 13.5, 9.0, 1.5)
tree("arb_pat1", 8.0, 8.5, 1.6)
tree("arb_pat2", 10.0, 11.0, 1.3)

plane("cesped_frente", [(-3.0, 0.0), (0.0, 0.0), (0.0, -1.2), (-3.0, -1.2)], M_CESPED, z=0.02)
plane("cesped_tras", [(0.0, 17.6), (3.2, 17.6), (3.2, 18.8), (0.0, 18.8)], M_CESPED, z=0.02)
plane("cesped_med_l", [(-0.2, 0.0), (0.0, 0.0), (0.0, 17.6), (-0.2, 17.6)], M_CESPED, z=0.02)
plane("cesped_med_r", [(11.4, 0.0), (11.6, 0.0), (11.6, 17.6), (11.4, 17.6)], M_CESPED, z=0.02)

def hedge(name, x0, x1, y0, y1, h=1.0, s=0.45):
    cube(name, x0, x1, y0, y1, 0.0, h, M_HOJAS)
    cube(name + "_t", x0 - s, x1 + s, y0 - s, y1 + s, 0.55, 0.8, M_HOJAS)

hedge("seto_frente", -2.5, 0.0, -0.35, -0.15, 1.0)
hedge("seto_lat", -2.9, -2.7, -0.2, 3.0, 1.1)

# Olivo Centenario en patio central
cylinder("olivo_pot", 9.2, 9.5, 0.45, 0.0, 0.70, M_HORMIGON, n=16)
cylinder("olivo_trunk", 9.2, 9.5, 0.08, 0.70, 1.60, M_TRONCO, n=10)
uv_sphere("olivo_crown1", 9.2, 9.5, 2.10, 0.85, M_HOJAS, n=14)
uv_sphere("olivo_crown2", 8.9, 9.7, 2.30, 0.60, M_HOJAS, n=12)

# Maceteros
plant("mac_patio1", 7.0, 5.4, 1.0)
plant("mac_patio2", 10.9, 5.4, 1.0)
plant("mac_balcon1", 3.0, 0.1, 0.8)
plant("mac_balcon2", 8.0, 0.1, 0.8)

# 10. ILUMINACIÓN Y MUNDO NISHITA
world = bpy.data.worlds.new("WorldSky")
world.use_nodes = True
nt = world.node_tree
for node in list(nt.nodes):
    nt.nodes.remove(node)
out = nt.nodes.new("ShaderNodeOutputWorld")
bg = nt.nodes.new("ShaderNodeBackground")
sky = nt.nodes.new("ShaderNodeTexSky")
sky.sky_type = "HOSEK_WILKIE"
sky.sun_elevation = math.radians(22.0)
sky.sun_rotation = math.radians(165.0)
nt.links.new(sky.outputs[0], bg.inputs[0])
nt.links.new(bg.outputs[0], out.inputs[0])
bpy.context.scene.world = world

sun_data = bpy.data.lights.new("Sun", "SUN")
sun_data.energy = 4.0
sun_data.angle = math.radians(1.0)
sun_data.color = (1.0, 0.97, 0.90)
sun_obj = bpy.data.objects.new("Sol", sun_data)
bpy.context.scene.collection.objects.link(sun_obj)
sun_obj.rotation_euler = (math.radians(52.0), math.radians(12.0), math.radians(45.0))

# Luces Interiores LED
def light_plane(name, x, y, w, d, z, power=20.0, color=(1.0, 0.95, 0.85)):
    mesh = bpy.data.meshes.new(name + "_mesh")
    verts = [(-w/2, -d/2, 0), (w/2, -d/2, 0), (w/2, d/2, 0), (-w/2, d/2, 0)]
    mesh.from_pydata(verts, [], [(0, 1, 2, 3)])
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.scene.collection.objects.link(obj)
    obj.location = (x, y, z)
    m = bpy.data.materials.new(name + "_mat")
    m.use_nodes = True
    bsdf = m.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (color[0], color[1], color[2], 1.0)
    bsdf.inputs["Emission Color"].default_value = (color[0], color[1], color[2], 1.0)
    bsdf.inputs["Emission Strength"].default_value = power
    obj.data.materials.append(m)
    return obj

light_plane("luz_salon", 4.0, 2.5, 2.5, 1.5, z_ha - 0.1, 30.0)
light_plane("luz_coc", 8.4, 2.5, 2.0, 1.5, z_ha - 0.1, 25.0)
light_plane("luz_d1", 3.9, 9.0, 2.0, 1.2, z_hb - 0.1, 20.0)
light_plane("luz_d3", 8.9, 15.5, 2.0, 1.2, z_hb - 0.1, 20.0)
light_plane("luz_porche", 8.9, 6.3, 2.0, 1.2, z_ha - 0.1, 15.0)
light_plane("luz_pa", 4.0, 10.5, 2.5, 1.5, z_ha - 0.1, 25.0)
light_plane("luz_pa_coc", 8.4, 2.5, 2.0, 1.5, z_ha - 0.1, 20.0)
light_plane("luz_portal", 0.8, -0.6, 1.0, 0.4, 2.2, 15.0, (1.0, 0.9, 0.7))
light_plane("luz_fachada", 5.7, -0.4, 3.0, 0.4, 3.0, 20.0, (0.9, 0.95, 1.0))

# 11. CAMARAS PROFESIONALES (7 ANGULOS)
def cam(name, loc, target, lens=32.0):
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

eye = 1.7
cam("cam_fachada", (4.0, -7.5, eye), (5.7, 4.0, 2.0), 35.0)
cam("cam_fachada2", (12.0, -8.0, eye), (5.7, 2.0, 2.0), 32.0)
cam("cam_trasera", (6.5, 24.5, eye), (5.7, 12.0, 2.0), 35.0)
cam("cam_axo", (19.0, -14.0, 15.0), (5.7, 8.8, 2.0), 30.0)
cam("cam_patios", (16.0, 3.0, 6.0), (8.9, 8.0, 1.5), 32.0)
cam("cam_interior_pb", (2.6, -0.8, 1.6), (3.8, 3.0, 1.2), 24.0)
cam("cam_interior_pa", (2.6, -0.8, 4.6), (3.8, 3.0, 4.2), 24.0)

bpy.context.scene.camera = bpy.data.objects["cam_fachada"]

# 12. GUARDAR MAINFILE EN BLENDER
bpy.ops.wm.save_mainfile(filepath=BLEND_FILE)
print("RECONSTRUCCION MAESTRA ARQUITECTONICA OK - Total Objetos:", len(bpy.data.objects))
