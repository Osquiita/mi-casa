# -*- coding: utf-8 -*-
"""Render 3D arquitectonico profesional. Reconstruye la vivienda bifamiliar
con materiales PBR texturizados, cielo realista Nishita, entorno urbanizado,
vegetacion y camaras a nivel de ojo humano."""
import os

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

import bpy
import math

OUT = r"C:\Users\Oscar Martinez\Desktop\mi-casa"
scene = bpy.context.scene

# ================================================================ LIMPIEZA
def clear_all():
    for obj in list(bpy.data.objects):
        bpy.data.objects.remove(obj, do_unlink=True)
    for mesh in list(bpy.data.meshes):
        bpy.data.meshes.remove(mesh)

clear_all()

# ================================================================ MATERIALES PBR
def pbr_mat(name, color=(0.8, 0.8, 0.8), rough=0.6, metal=0.0, spec=0.5,
            trans=0.0, ior=1.45, emit=0.0, bump=0.0, tex_color2=None,
            tex_scale=10.0, mix=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    bsdf = nt.nodes.get("Principled BSDF")
    out = nt.nodes.get("Material Output")
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
            bsdf.inputs["Emission Color"].default_value = (1, 1, 1, 1)
            bsdf.inputs["Emission Strength"].default_value = emit
        except Exception:
            pass
    if bump > 0 or tex_color2 is not None:
        ntex = nt.nodes.new("ShaderNodeTexNoise")
        ntex.inputs["Scale"].default_value = tex_scale
        ntex.inputs["Detail"].default_value = 8.0
        ntex.inputs["Roughness"].default_value = 0.5
        if tex_color2 is not None:
            mix_node = nt.nodes.new("ShaderNodeMix")
            mix_node.data_type = "RGBA"
            mix_node.inputs[0].default_value = mix
            mix_node.inputs[6].default_value = (color[0], color[1], color[2], 1.0)
            mix_node.inputs[7].default_value = (tex_color2[0], tex_color2[1], tex_color2[2], 1.0)
            nt.links.new(ntex.outputs["Fac"], mix_node.inputs[0])
            nt.links.new(mix_node.outputs[0], bsdf.inputs["Base Color"])
        if bump > 0:
            bump_node = nt.nodes.new("ShaderNodeBump")
            bump_node.inputs["Strength"].default_value = bump
            bump_node.inputs["Distance"].default_value = 0.02
            nt.links.new(ntex.outputs["Fac"], bump_node.inputs["Height"])
            nt.links.new(bump_node.outputs["Normal"], bsdf.inputs["Normal"])
    return m

M_WALL    = pbr_mat("M_WALL", (0.96, 0.95, 0.93), 0.65, spec=0.25, bump=0.012, tex_scale=6.0)
M_WALL2   = pbr_mat("M_WALL2", (0.90, 0.88, 0.85), 0.7, spec=0.2, bump=0.01, tex_scale=5.0)
M_STUCCO  = pbr_mat("M_STUCCO", (0.93, 0.92, 0.90), 0.6, spec=0.3, bump=0.02, tex_scale=4.0)
M_CONC    = pbr_mat("M_CONC", (0.78, 0.76, 0.72), 0.85, spec=0.15, bump=0.02, tex_scale=3.0)
M_SLAB    = pbr_mat("M_SLAB", (0.82, 0.80, 0.76), 0.8, spec=0.15, bump=0.015, tex_scale=5.0)
M_ROOF    = pbr_mat("M_ROOF", (0.74, 0.72, 0.68), 0.85, spec=0.1, bump=0.015, tex_scale=6.0)
M_WOOD    = pbr_mat("M_WOOD", (0.72, 0.52, 0.34), 0.4, spec=0.4, bump=0.04, tex_scale=2.0)
M_WOOD2   = pbr_mat("M_WOOD2", (0.56, 0.40, 0.25), 0.45, spec=0.35, bump=0.05, tex_scale=2.0)
M_WOODF   = pbr_mat("M_WOODF", (0.66, 0.48, 0.31), 0.35, spec=0.45, bump=0.05, tex_scale=8.0)
M_GLASS   = pbr_mat("M_GLASS", (0.78, 0.92, 0.96), 0.03, spec=1.0, trans=1.0, ior=1.52)
M_GLASS2  = pbr_mat("M_GLASS2", (0.70, 0.88, 0.93), 0.05, spec=1.0, trans=0.95, ior=1.52)
M_DARK    = pbr_mat("M_DARK", (0.20, 0.22, 0.24), 0.5)
M_FRAME   = pbr_mat("M_FRAME", (0.28, 0.30, 0.33), 0.4, metal=0.4)
M_GARAGE  = pbr_mat("M_GARAGE", (0.26, 0.28, 0.31), 0.5, metal=0.3, bump=0.02, tex_scale=4.0)
M_GREY    = pbr_mat("M_GREY", (0.55, 0.56, 0.58), 0.6)
M_WHITE   = pbr_mat("M_WHITE", (0.98, 0.97, 0.95), 0.6)
M_CHROME  = pbr_mat("M_CHROME", (0.85, 0.87, 0.90), 0.12, metal=1.0, spec=1.0)
M_METAL   = pbr_mat("M_METAL", (0.55, 0.58, 0.62), 0.35, metal=0.8)
M_SOFA    = pbr_mat("M_SOFA", (0.58, 0.70, 0.68), 0.9)
M_TEAL    = pbr_mat("M_TEAL", (0.40, 0.64, 0.68), 0.85)
M_BED     = pbr_mat("M_BED", (0.82, 0.80, 0.92), 0.9)
M_KITCH   = pbr_mat("M_KITCH", (0.93, 0.89, 0.83), 0.5, spec=0.4, bump=0.01, tex_scale=10.0)
M_COUNT   = pbr_mat("M_COUNT", (0.85, 0.84, 0.82), 0.3, spec=0.6)
M_STONE   = pbr_mat("M_STONE", (0.74, 0.68, 0.58), 0.85, spec=0.2, bump=0.03, tex_scale=3.0)
M_PAV     = pbr_mat("M_PAV", (0.72, 0.70, 0.66), 0.8, spec=0.25, bump=0.025, tex_scale=4.0)
M_GRASS   = pbr_mat("M_GRASS", (0.38, 0.54, 0.30), 1.0, bump=0.04, tex_scale=20.0)
M_LEAF    = pbr_mat("M_LEAF", (0.30, 0.52, 0.26), 1.0)
M_LEAF2   = pbr_mat("M_LEAF2", (0.24, 0.45, 0.22), 1.0)
M_TRUNK   = pbr_mat("M_TRUNK", (0.42, 0.33, 0.24), 0.9, bump=0.05, tex_scale=3.0)
M_GROUND  = pbr_mat("M_GROUND", (0.58, 0.58, 0.54), 1.0)
M_ROAD    = pbr_mat("M_ROAD", (0.32, 0.32, 0.34), 0.92, bump=0.05, tex_scale=8.0)
M_CAR     = pbr_mat("M_CAR", (0.40, 0.53, 0.64), 0.18, metal=0.8, spec=1.0)
M_CARBODY = pbr_mat("M_CARBODY", (0.36, 0.40, 0.45), 0.22, metal=0.85, spec=1.0)
M_CARWIN  = pbr_mat("M_CARWIN", (0.70, 0.86, 0.90), 0.04, trans=0.9, ior=1.52)

print("MATERIALES PBR OK")

# ================================================================ SOLAR / ENTORNO
z_f = 0.22
z_hb = 2.90
z_pa = 2.90
z_ha = 5.80

cube("road_front", -4.0, 14.4, -12.0, -1.2, 0.0, 0.16, M_ROAD)
cube("sidewalk_front", -3.0, 14.4, -1.2, 0.0, 0.0, 0.12, M_PAV)
cube("road_rear", -4.0, 14.4, 17.6, 28.0, 0.0, 0.16, M_ROAD)
cube("sidewalk_rear", -3.0, 14.4, 17.6, 18.8, 0.0, 0.12, M_PAV)
cube("ground_plot", -3.0, 14.4, 0.0, 17.6, -0.06, 0.0, M_GROUND)
cube("sidewalk_l", -3.0, 0.0, -1.2, 17.6, 0.0, 0.12, M_PAV)
cube("sidewalk_r", 11.4, 14.4, -1.2, 17.6, 0.0, 0.12, M_PAV)
cube("patio_floor", 6.40, 11.40, 5.00, 13.00, 0.0, 0.06, M_PAV)
cube("patio2_floor", 0.0, 3.20, 14.10, 17.60, 2.90, 2.96, M_STONE)
cube("patio2_edge_n", 0.0, 3.20, 17.48, 17.60, 2.90, 3.20, M_STUCCO)
cube("patio2_edge_w", 0.0, 0.12, 14.10, 17.60, 2.90, 3.20, M_STUCCO)
cube("patio2_edge_s", 0.0, 3.20, 14.10, 14.22, 2.90, 3.20, M_STUCCO)
cube("patio2_rail", 3.08, 3.20, 14.22, 17.48, 2.96, 3.30, M_METAL)
cube("slab_pb", 0.0, 11.40, 0.0, 17.60, 0.15, 0.22, M_SLAB)

# ================================================================ MUROS P-01
wall_h("M_pb_front", (0.0, 0.0, 11.40),
       [(0.30, 1.30), (2.60, 4.40), (4.80, 6.00), (6.90, 8.10), (8.90, 9.90), (10.40, 11.40)],
       z_f, z_hb, M_STUCCO)
wall_h("M_pb_rear", (17.60, 0.0, 11.40),
       [(0.80, 2.40), (3.60, 5.20), (8.60, 11.00)],
       z_f, z_hb, M_STUCCO)
wall_v("M_pb_l", (0.0, 0.0, 17.60), [], z_f, z_hb, M_WALL2)
wall_v("M_pb_rf", (11.40, 0.0, 5.00), [], z_f, z_hb, M_WALL)
wall_v("M_pb_rpatio", (11.40, 5.00, 13.00), [], z_f, z_hb, M_WALL2)
wall_v("M_pb_rr", (11.40, 13.00, 17.60), [], z_f, z_hb, M_WALL)
wall_v("T_pb1", (1.40, 0.0, 13.00), [(1.40, 4.60), (6.10, 6.80), (7.90, 8.60)], z_f, z_hb, M_WALL)
wall_v("T_pb2", (6.40, 0.0, 5.00), [(1.00, 4.40)], z_f, z_hb, M_WALL)
wall_v("T_pb3", (6.40, 5.00, 7.40), [(5.30, 6.20)], z_f, z_hb, M_WALL)
wall_v("T_pb4", (6.40, 7.40, 13.00), [(7.80, 8.40), (9.00, 9.60), (11.00, 12.20)], z_f, z_hb, M_WALL)
wall_h("T_pb5", (5.00, 6.40, 11.40), [(6.40, 10.40)], z_f, z_hb, M_WALL)
wall_v("T_pb6", (10.40, 0.0, 5.00), [], z_f, z_hb, M_WALL)
wall_h("T_pb7", (7.40, 1.40, 6.40), [], z_f, z_hb, M_WALL)
wall_h("T_pb8", (8.80, 1.40, 6.40), [], z_f, z_hb, M_WALL)
wall_h("T_pb9", (10.20, 1.40, 6.40), [(3.30, 4.00)], z_f, z_hb, M_WALL)
wall_h("T_pb10", (14.10, 0.0, 4.50), [(0.80, 1.50), (3.60, 4.30)], z_f, z_hb, M_WALL)
wall_h("T_pb11", (13.00, 1.40, 8.00), [(2.20, 2.90)], z_f, z_hb, M_WALL)
wall_v("T_pb12", (4.50, 13.00, 14.10), [], z_f, z_hb, M_WALL)
wall_v("T_pb13", (6.40, 13.00, 17.60), [], z_f, z_hb, M_WALL)
wall_v("T_pb14", (8.00, 13.00, 17.60), [(13.30, 13.90)], z_f, z_hb, M_WALL)
wall_v("T_pb15", (3.20, 14.10, 17.60), [], z_f, z_hb, M_WALL)

# ================================================================ FORJADO P-02
cube("slab_pa_front", 0.0, 11.40, 0.0, 5.00, z_hb, z_hb + 0.20, M_SLAB)
cube("slab_pa_west", 0.0, 6.40, 5.00, 17.60, z_hb, z_hb + 0.20, M_SLAB)
cube("slab_pa_pas", 6.40, 11.40, 5.00, 7.60, z_hb, z_hb + 0.20, M_SLAB)
cube("slab_pa_d2", 6.40, 11.40, 13.00, 17.60, z_hb, z_hb + 0.20, M_SLAB)

# ================================================================ MUROS P-02
wall_h("M_pa_front", (0.0, 0.0, 11.40),
       [(2.60, 4.40), (4.80, 6.00), (6.90, 8.10), (8.90, 9.90)],
       z_pa, z_ha, M_STUCCO)
wall_h("M_pa_rear", (17.60, 0.0, 11.40),
       [(3.60, 5.20), (7.00, 9.00), (9.80, 11.20)],
       z_pa, z_ha, M_STUCCO)
wall_v("M_pa_l", (0.0, 0.0, 17.60), [], z_pa, z_ha, M_WALL2)
wall_v("M_pa_rf", (11.40, 0.0, 5.00), [], z_pa, z_ha, M_WALL)
wall_v("M_pa_rpatio", (11.40, 5.00, 13.00), [], z_pa, z_ha, M_WALL2)
wall_v("M_pa_rr", (11.40, 13.00, 17.60), [], z_pa, z_ha, M_WALL)
wall_v("M_pa_esc", (10.40, 0.0, 5.00), [], z_pa, z_ha, M_WALL)
# T_pa1 removed in v8 to integrate hallway into PA living room (50 m2 open space)
wall_v("T_pa2", (6.40, 7.60, 13.00), [(7.80, 8.40), (9.00, 9.60), (11.00, 12.20)], z_pa, z_ha, M_WALL)
wall_h("T_pa3", (7.60, 6.40, 11.40), [(7.00, 9.40)], z_pa, z_ha, M_WALL)
wall_v("T_pa4", (1.40, 0.0, 7.40), [(1.40, 4.60), (6.10, 6.80), (7.90, 8.60)], z_pa, z_ha, M_WALL)
wall_v("T_pa5", (6.40, 0.0, 5.00), [(1.00, 4.40)], z_pa, z_ha, M_WALL)
wall_h("T_pa6", (7.40, 1.40, 6.40), [], z_pa, z_ha, M_WALL)
wall_h("T_pa7", (8.80, 1.40, 6.40), [], z_pa, z_ha, M_WALL)
wall_h("T_pa8", (10.20, 1.40, 6.40), [(3.30, 4.00)], z_pa, z_ha, M_WALL)
wall_h("T_pa9", (13.00, 1.40, 6.40), [(2.20, 2.90)], z_pa, z_ha, M_WALL)
wall_h("T_pa10", (14.10, 0.0, 6.40), [(0.80, 1.50), (3.60, 4.30)], z_pa, z_ha, M_WALL)
wall_v("T_pa11", (3.20, 14.10, 17.60), [], z_pa, z_ha, M_WALL)
wall_v("T_pa12", (6.40, 13.00, 17.60), [(13.20, 14.00)], z_pa, z_ha, M_WALL)
wall_h("T_pa13", (13.00, 6.40, 11.40), [(7.00, 10.40)], z_pa, z_ha, M_WALL)

# ================================================================ CUBIERTA + PARAPETO
cube("roof", 0.0, 11.40, 0.0, 17.60, z_ha, z_ha + 0.20, M_ROOF)
cube("roof_pat1", 6.40, 11.40, 5.00, 13.00, z_ha, z_ha + 0.20, M_ROOF)
cube("roof_pat2", 6.40, 11.40, 7.60, 13.00, z_ha, z_ha + 0.20, M_ROOF)
cube("roof_pat3", 0.0, 3.20, 14.10, 17.60, z_ha, z_ha + 0.20, M_ROOF)
cube("parapet_n", 0.0, 11.40, -0.15, 0.15, z_ha, z_ha + 0.32, M_ROOF)
cube("parapet_s", 0.0, 11.40, 17.45, 17.75, z_ha, z_ha + 0.32, M_ROOF)
cube("parapet_w", -0.15, 0.15, 0.0, 17.60, z_ha, z_ha + 0.32, M_ROOF)
cube("parapet_e", 11.25, 11.55, 0.0, 17.60, z_ha, z_ha + 0.32, M_ROOF)
# Remates metálicos de albardilla / vierteaguas en cinc
cube("cap_n", -0.05, 11.45, -0.18, 0.18, z_ha + 0.32, z_ha + 0.35, M_METAL)
cube("cap_s", -0.05, 11.45, 17.42, 17.78, z_ha + 0.32, z_ha + 0.35, M_METAL)
cube("cap_w", -0.18, 0.18, -0.05, 17.65, z_ha + 0.32, z_ha + 0.35, M_METAL)
cube("cap_e", 11.22, 11.58, -0.05, 17.65, z_ha + 0.32, z_ha + 0.35, M_METAL)

# Pergola bioclimática de madera en patio central (6.40 a 11.40)
for i in range(12):
    py = 5.2 + i * 0.65
    cube(f"pergola_slat_{i}", 6.30, 11.50, py - 0.04, py + 0.04, 2.70, 2.82, M_WOOD)
cube("pergola_beam_l", 6.35, 6.45, 5.00, 12.80, 2.58, 2.70, M_WOOD2)
cube("pergola_beam_r", 11.35, 11.45, 5.00, 12.80, 2.58, 2.70, M_WOOD2)

# Lamas decorativas de madera en acceso y balcones
for j in range(8):
    lx = 1.6 + j * 0.12
    cube(f"facade_slat_{j}", lx - 0.02, lx + 0.02, -0.10, -0.02, 0.2, 2.8, M_WOOD)



# ================================================================ HUECOS
door_h("portalA", 0.0, 0.30, 1.30, mat=M_WOOD2)
for (a, b) in [(2.60, 4.40), (4.80, 6.00), (6.90, 8.10), (8.90, 9.90)]:
    glass_h("win_front_pb", 0.0, a, b, 0.9, 2.4, mat=M_GLASS2)
door_h("portalB", 0.0, 10.40, 11.40, mat=M_WOOD2)
glass_v("win_esc", 11.40, 2.80, 3.60, 0.9, 2.4)
for (a, b) in [(0.80, 2.40), (3.60, 5.20)]:
    glass_h("win_rear_pb", 17.60, a, b, 0.9, 2.4, mat=M_GLASS2)
cube("garage_door", 8.60, 11.00, 17.56, 17.64, 0.0, 2.4, M_GARAGE)
for (a, b) in [(7.80, 8.40), (9.00, 9.60), (11.00, 12.20)]:
    glass_v("win_pat_pb", 6.40, a, b, 0.9, 2.4, mat=M_GLASS2)
for z in (z_f, z_pa):
    plane("glass_coc_%s" % int(z), [(6.40, 5.00), (10.40, 5.00), (10.40, 5.01), (6.40, 5.01)], M_GLASS, z=z + 0.9)
    plane("glass_coc2_%s" % int(z), [(6.40, 5.00), (10.40, 5.00), (10.40, 5.01), (6.40, 5.01)], M_GLASS, z=z + 2.4)
for (a, b) in [(2.60, 4.40), (4.80, 6.00), (6.90, 8.10), (8.90, 9.90)]:
    glass_h("win_front_pa", 0.0, a, b, z_pa + 0.9, z_pa + 2.4, mat=M_GLASS2)
for (a, b) in [(3.60, 5.20), (7.00, 9.00), (9.80, 11.20)]:
    glass_h("win_rear_pa", 17.60, a, b, z_pa + 0.9, z_pa + 2.4, mat=M_GLASS2)
glass_v("win_esc_pa", 11.40, 2.80, 3.60, z_pa + 0.9, z_pa + 2.4)
for (a, b) in [(7.80, 8.40), (9.00, 9.60), (11.00, 12.20)]:
    glass_v("win_vac", 6.40, a, b, z_pa + 0.9, z_pa + 2.4)
door_v("d_salon_porche", 6.40, 5.30, 6.20, mat=M_WOOD)
door_v("d_banio", 1.40, 7.90, 8.60, mat=M_WOOD)

# ================================================================ ESCALERA
stairs("esc", 10.40, 11.40, 0.0, 5.00, z_f, z_pa, n=16)

print("CASA ESTRUCTURAL OK")

# ================================================================ MOBILIARIO P-01
sofa("salon_sofa", 1.9, 0.6, 2.6, 1.0, M_TEAL)
table("salon_table", 3.2, 2.2, 1.2, 0.7, 0.4, M_WOOD, M_WOOD2)
tv("salon_tv", 2.5, 4.9, 1.8, 0.9)
cube("salon_rug", 2.0, 4.4, 0.7, 2.9, 0.0, 0.03, mat("_rug", (0.75, 0.70, 0.62), 0.95))
plant("salon_plant", 1.7, 4.6, 1.1)
kitchen_units("coc_base", 6.7, 10.4, 0.2, 0.0)
cube("coc_isla", 6.6, 8.4, 4.0, 5.0, 0.0, 0.92, M_KITCH)
cube("coc_isla_top", 6.55, 8.45, 3.95, 5.05, 0.92, 0.96, M_COUNT)
# Taburetes de diseño para la barra de cocina
for sx, sy in [(6.8, 3.65), (7.5, 3.65), (8.2, 3.65)]:
    cylinder(f"stool_seat_{sx}", sx, sy, 0.18, 0.65, 0.70, M_WOOD2, n=12)
    cylinder(f"stool_leg_{sx}", sx, sy, 0.03, 0.0, 0.65, M_METAL, n=8)
chair("coc_s1", 7.1, 3.7, M_WOOD2)
chair("coc_s2", 7.9, 3.7, M_WOOD2)
table("porche_table", 8.9, 6.3, 1.6, 0.9, 0.75, M_WOOD, M_METAL)
chair("porche_c1", 7.6, 6.6, M_WOOD2)
chair("porche_c2", 10.2, 6.6, M_WOOD2)
plant("porche_plant", 8.9, 5.3, 1.0)
# Olivo ornamental en macetón de hormigón en patio central
cylinder("olivo_pot", 9.2, 9.5, 0.45, 0.0, 0.70, M_CONC, n=16)
cylinder("olivo_trunk", 9.2, 9.5, 0.08, 0.70, 1.60, M_TRUNK, n=10)
uv_sphere("olivo_crown1", 9.2, 9.5, 2.10, 0.85, M_LEAF, n=14)
uv_sphere("olivo_crown2", 8.9, 9.7, 2.30, 0.60, M_LEAF2, n=12)
uv_sphere("olivo_crown3", 9.5, 9.3, 2.25, 0.55, M_LEAF2, n=12)

bed("d1_bed", 3.9, 6.5, 1.6, 2.0)
wardrobe("d1_ward", 1.7, 5.2, 1.6, 0.6, 2.3)
cube("d1_night_l", 3.1, 6.3, 0.0, 0.5, 0.0, 0.5, M_WOOD)
cube("d1_night_r", 4.9, 6.3, 0.0, 0.5, 0.0, 0.5, M_WOOD)
plant("d1_plant", 6.1, 11.5, 0.8)
toilet("banio_wc", 5.4, 13.4)
sink("banio_sink", 5.0, 13.9)
shower("banio_sh", 6.0, 13.3, 0.8)
wardrobe("pas_ward", 0.4, 14.3, 1.4, 0.6, 2.3)
plant("pas_plant", 2.6, 16.5, 0.9)
bed("d2_bed", 4.8, 15.8, 1.5, 1.9)
wardrobe("d2_ward", 3.5, 14.3, 1.4, 0.6, 2.3)
bed("d3_bed", 8.9, 15.8, 1.6, 2.0)
wardrobe("d3_ward", 6.8, 13.3, 1.8, 0.6, 2.3)
plant("d3_plant", 10.9, 16.8, 0.8)

print("MOBILIARIO P-01 OK")

# ================================================================ MOBILIARIO P-02
z_b = z_pa + 0.02
bed("pa_bed", 3.9, 3.0, 1.8, 2.0, M_BED)
wardrobe("pa_ward", 1.7, 0.4, 1.8, 0.6, 2.3)
cube("pa_night_l", 3.0, 3.4, 2.0, 2.5, z_b, z_b + 0.5, M_WOOD)
cube("pa_night_r", 5.0, 5.4, 2.0, 2.5, z_b, z_b + 0.5, M_WOOD)
plant("pa_plant", 6.1, 1.6, 1.0)
toilet("pa_banio_wc", 5.4, 13.4, (0.9, 0.9, 0.9))
sink("pa_banio_sink", 5.0, 13.9, (0.88, 0.88, 0.86))
shower("pa_banio_sh", 6.0, 13.3, 0.8)
bed("pa_d3_bed", 8.9, 15.8, 1.6, 2.0)
wardrobe("pa_d3_ward", 6.8, 13.3, 1.8, 0.6, 2.3)
plant("pa_d3_plant", 10.9, 16.8, 0.8)
sofa("pa_salon_sofa", 1.9, 9.0, 2.6, 1.0, M_SOFA)
table("pa_salon_table", 3.2, 10.4, 1.2, 0.7, 0.4, M_WOOD, M_WOOD2)
tv("pa_salon_tv", 2.5, 12.9, 1.8, 0.9)
cube("pa_salon_rug", 2.0, 4.4, 8.6, 10.8, z_b, z_b + 0.03, mat("_rug2", (0.7, 0.72, 0.68), 0.95))
plant("pa_salon_plant", 1.7, 11.6, 1.1)
kitchen_units("pa_coc_base", 6.7, 10.4, 0.2, z_b)
cube("pa_coc_isla", 6.6, 8.4, 4.0, 5.0, z_b, z_b + 0.92, M_KITCH)
cube("pa_coc_isla_top", 6.6, 8.4, 4.0, 5.0, z_b + 0.92, z_b + 0.96, M_COUNT)
chair("pa_coc_s1", 7.1, 3.7, M_WOOD2)
chair("pa_coc_s2", 7.9, 3.7, M_WOOD2)
table("pa_porche_table", 8.9, 6.3, 1.6, 0.9, 0.75, M_WOOD, M_METAL)
chair("pa_porche_c1", 7.6, 6.6, M_WOOD2)
chair("pa_porche_c2", 10.2, 6.6, M_WOOD2)
plant("pa_porche_plant", 8.9, 5.3, 1.0)

print("MOBILIARIO P-02 OK")

# ================================================================ VEGETACION Y ENTORNO
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
plane("cesped_frente", [(-3.0, 0.0), (0.0, 0.0), (0.0, -1.2), (-3.0, -1.2)], M_GRASS, z=0.02)
plane("cesped_tras", [(0.0, 17.6), (3.2, 17.6), (3.2, 18.8), (0.0, 18.8)], M_GRASS, z=0.02)
plane("cesped_medianera", [(-0.2, 0.0), (0.0, 0.0), (0.0, 17.6), (-0.2, 17.6)], M_GRASS, z=0.02)
plane("cesped_medianera_r", [(11.4, 0.0), (11.6, 0.0), (11.6, 17.6), (11.4, 17.6)], M_GRASS, z=0.02)

def hedge(name, x0, x1, y0, y1, h=1.0, s=0.45):
    cube(name, x0, x1, y0, y1, 0.0, h, M_LEAF)
    cube(name + "_t", x0 - s, x1 + s, y0 - s, y1 + s, 0.55, 0.8, M_LEAF2)

hedge("seto_frente", -2.5, 0.0, -0.35, -0.15, 1.0)
hedge("seto_lat", -2.9, -2.7, -0.2, 3.0, 1.1)
plant("mac_patio1", 7.0, 5.4, 1.0)
plant("mac_patio2", 10.9, 5.4, 1.0)
plant("mac_balcon1", 3.0, 0.1, 0.8)
plant("mac_balcon2", 8.0, 0.1, 0.8)
plant("mac_pat2_1", 0.6, 15.0, 1.0)
plant("mac_pat2_2", 2.6, 15.0, 1.0)
car("coche", 9.0, 1.8)

# ================================================================ LUCES INTERIORES
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
light_plane("luz_pa_d3", 8.9, 15.5, 2.0, 1.2, z_ha - 0.1, 20.0)
light_plane("luz_portal", 0.8, -0.6, 1.0, 0.4, 2.2, 15.0, (1.0, 0.9, 0.7))
light_plane("luz_fachada", 5.7, -0.4, 3.0, 0.4, 3.0, 20.0, (0.9, 0.95, 1.0))

print("VEGETACION + LUCES OK")

# ================================================================ MUNDO (CIELO NISHITA)
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
scene.world = world

sun_data = bpy.data.lights.new("Sun", "SUN")
sun_data.energy = 4.0
sun_data.angle = math.radians(1.0)
sun_data.color = (1.0, 0.97, 0.90)
sun_obj = bpy.data.objects.new("Sol", sun_data)
bpy.context.scene.collection.objects.link(sun_obj)
sun_obj.rotation_euler = (math.radians(52.0), math.radians(12.0), math.radians(45.0))

# ================================================================ CAMARAS PROFESIONALES
def cam(name, loc, target, lens=32.0):
    cd = bpy.data.cameras.new(name)
    cd.lens = lens
    cd.sensor_width = 36.0
    obj = bpy.data.objects.new(name, cd)
    bpy.context.scene.collection.objects.link(obj)
    obj.location = loc
    empty = bpy.data.objects.new(name + "_target", None)
    empty.empty_display_size = 0.3
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

scene.camera = bpy.data.objects["cam_fachada"]

# ================================================================ CONFIG RENDER EEVEE
engine = None
for e in ("BLENDER_EEVEE_NEXT", "BLENDER_EEVEE"):
    if e in dir(bpy.types.RenderSettings):
        engine = e
        break
if engine:
    scene.render.engine = engine
scene.render.resolution_x = 2560
scene.render.resolution_y = 1440
scene.render.film_transparent = False
try:
    scene.render.film_filter_width = 1.5
except Exception:
    pass
eevee = scene.eevee
for attr, val in (("use_ssr", True), ("use_ssr_refraction", True),
                  ("use_gtao", True), ("use_bloom", True)):
    if hasattr(eevee, attr):
        try:
            setattr(eevee, attr, val)
        except Exception:
            pass
try:
    eevee.shadow_cascade_size = "4096"
except Exception:
    pass
try:
    eevee.taa_render_samples = 64
except Exception:
    pass
try:
    scene.view_settings.view_transform = "Filmic"
    scene.view_settings.look = "AgX - Punchy"
except Exception:
    pass

bpy.ops.wm.save_mainfile(filepath=os.path.join(OUT, "casa-bifamiliar-3d.blend"))
print("RENDER PRO BUILD OK - objetos:", len(bpy.data.objects))
