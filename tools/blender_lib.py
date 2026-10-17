# -*- coding: utf-8 -*-
"""Primitivas Blender sin dependencia de contexto (seguras para execute_code)."""
import bpy
import math


def _link(obj):
    bpy.context.scene.collection.objects.link(obj)
    return obj


def _assign(obj, material):
    if material is not None:
        if len(obj.data.materials) == 0:
            obj.data.materials.append(material)
        else:
            obj.data.materials[0] = material
    return obj


def _cube_mesh(name):
    mesh = bpy.data.meshes.new(name + "_mesh")
    verts = [(-0.5, -0.5, -0.5), (0.5, -0.5, -0.5), (0.5, 0.5, -0.5), (-0.5, 0.5, -0.5),
             (-0.5, -0.5, 0.5), (0.5, -0.5, 0.5), (0.5, 0.5, 0.5), (-0.5, 0.5, 0.5)]
    faces = [(0, 1, 2, 3), (4, 5, 6, 7), (0, 1, 5, 4),
             (2, 3, 7, 6), (1, 2, 6, 5), (0, 3, 7, 4)]
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    return mesh


def cube(name, x0, x1, y0, y1, z0, z1, material):
    w = x1 - x0; d = y1 - y0; h = z1 - z0
    obj = _link(bpy.data.objects.new(name, _cube_mesh(name)))
    obj.location = ((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2)
    obj.scale = (w, d, h)
    _assign(obj, material)
    return obj


def plane(name, pts, material, z=0.0, double=False):
    n = len(pts)
    verts = [(x, y, z) for (x, y) in pts]
    faces = [list(range(n))]
    if double:
        faces.append(list(range(n))[::-1])
    mesh = bpy.data.meshes.new(name + "_mesh")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = _link(bpy.data.objects.new(name, mesh))
    _assign(obj, material)
    return obj


def uv_sphere(name, cx, cy, cz, r, material, n=24):
    mesh = bpy.data.meshes.new(name + "_mesh")
    verts = []
    for i in range(n + 1):
        th = math.pi * i / n
        for j in range(n):
            ph = 2 * math.pi * j / n
            verts.append((cx + r * math.sin(th) * math.cos(ph),
                          cy + r * math.sin(th) * math.sin(ph),
                          cz + r * math.cos(th)))
    faces = []
    for i in range(n):
        for j in range(n):
            a = i * n + j
            b = i * n + (j + 1) % n
            c = (i + 1) * n + (j + 1) % n
            d = (i + 1) * n + j
            faces.append((a, b, c, d))
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = _link(bpy.data.objects.new(name, mesh))
    _assign(obj, material)
    return obj


def cylinder(name, cx, cy, r, z0, z1, material, n=20):
    mesh = bpy.data.meshes.new(name + "_mesh")
    verts = []
    for j in range(n):
        ph = 2 * math.pi * j / n
        verts.append((cx + r * math.cos(ph), cy + r * math.sin(ph), z0))
        verts.append((cx + r * math.cos(ph), cy + r * math.sin(ph), z1))
    faces = []
    for j in range(n):
        a0 = 2 * j; a1 = 2 * ((j + 1) % n)
        faces.append((a0, a1, a1 + 1, a0 + 1))
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = _link(bpy.data.objects.new(name, mesh))
    _assign(obj, material)
    return obj


# ================================================================ materiales
def mat(name, color=(0.8, 0.8, 0.8), rough=0.6, metal=0.0, spec=0.5, emit=0.0,
        trans=0.0, ior=1.45):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (color[0], color[1], color[2], 1.0)
    bsdf.inputs["Roughness"].default_value = rough
    bsdf.inputs["Metallic"].default_value = metal
    try:
        bsdf.inputs["Specular IOR Level"].default_value = spec
    except Exception:
        pass
    bsdf.inputs["Transmission Weight"].default_value = trans
    if ior is not None:
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
    return m


M_WALL   = mat("M_WALL", (0.965, 0.955, 0.935), 0.85, spec=0.2)
M_WALL2  = mat("M_WALL2", (0.90, 0.885, 0.86), 0.9, spec=0.15)
M_SLAB   = mat("M_SLAB", (0.82, 0.80, 0.76), 0.8, spec=0.15)
M_ROOF   = mat("M_ROOF", (0.74, 0.72, 0.68), 0.85)
M_WOOD   = mat("M_WOOD", (0.72, 0.52, 0.34), 0.45, spec=0.35)
M_WOOD2  = mat("M_WOOD2", (0.56, 0.40, 0.25), 0.5, spec=0.3)
M_GLASS  = mat("M_GLASS", (0.75, 0.90, 0.94), 0.05, spec=1.0, trans=1.0, ior=1.5)
M_DARK   = mat("M_DARK", (0.20, 0.22, 0.24), 0.55)
M_GREY   = mat("M_GREY", (0.55, 0.56, 0.58), 0.6)
M_WHITE  = mat("M_WHITE", (0.98, 0.97, 0.95), 0.7)
M_SOFA   = mat("M_SOFA", (0.60, 0.72, 0.70), 0.85)
M_TEAL   = mat("M_TEAL", (0.42, 0.66, 0.70), 0.8)
M_BED    = mat("M_BED", (0.82, 0.80, 0.92), 0.9)
M_KITCH  = mat("M_KITCH", (0.93, 0.89, 0.83), 0.55)
M_COUNT  = mat("M_COUNT", (0.85, 0.84, 0.82), 0.35)
M_STONE  = mat("M_STONE", (0.72, 0.66, 0.56), 0.9)
M_GRASS  = mat("M_GRASS", (0.42, 0.58, 0.36), 1.0)
M_LEAF   = mat("M_LEAF", (0.32, 0.55, 0.30), 1.0)
M_LEAF2  = mat("M_LEAF2", (0.26, 0.47, 0.25), 1.0)
M_TRUNK  = mat("M_TRUNK", (0.46, 0.36, 0.26), 0.9)
M_GROUND = mat("M_GROUND", (0.60, 0.60, 0.56), 1.0)
M_ROAD   = mat("M_ROAD", (0.34, 0.34, 0.36), 0.95)
M_GARAGE = mat("M_GARAGE", (0.26, 0.28, 0.31), 0.6, metal=0.3)
M_FRAME  = mat("M_FRAME", (0.30, 0.32, 0.35), 0.5)
M_CHROME = mat("M_CHROME", (0.85, 0.87, 0.90), 0.15, metal=1.0, spec=1.0)
M_CAR    = mat("M_CAR", (0.40, 0.53, 0.64), 0.2, metal=0.7, spec=1.0)
M_CARBODY= mat("M_CARBODY", (0.36, 0.40, 0.45), 0.25, metal=0.8, spec=1.0)
M_CARWIN = mat("M_CARWIN", (0.70, 0.86, 0.90), 0.05, trans=0.9, ior=1.5)
M_METAL  = mat("M_METAL", (0.55, 0.58, 0.62), 0.4, metal=0.8)

# ================================================================ helpers muros
def wall_h(name, run, gaps, z0, z1, material):
    y, x0, x1 = run
    segs = []
    cur = x0
    for g in sorted(gaps):
        if g[0] > cur:
            segs.append((cur, g[0]))
        cur = max(cur, g[1])
    if cur < x1:
        segs.append((cur, x1))
    for i, (a, b) in enumerate(segs):
        cube(f"{name}_{i}", a, b, y - 0.15, y + 0.15, z0, z1, material)


def wall_v(name, run, gaps, z0, z1, material):
    x, y0, y1 = run
    segs = []
    cur = y0
    for g in sorted(gaps):
        if g[0] > cur:
            segs.append((cur, g[0]))
        cur = max(cur, g[1])
    if cur < y1:
        segs.append((cur, y1))
    for i, (a, b) in enumerate(segs):
        cube(f"{name}_{i}", x - 0.15, x + 0.15, a, b, z0, z1, material)


def glass_h(name, y, x0, x1, z0, z1, mat=M_GLASS, frame=True):
    # Marco de 4 lados (izq, der, inferior, superior)
    if frame:
        cube(name + "_j0", x0 - 0.04, x0 + 0.04, y - 0.06, y + 0.06, z0, z1, M_FRAME)
        cube(name + "_j1", x1 - 0.04, x1 + 0.04, y - 0.06, y + 0.06, z0, z1, M_FRAME)
        cube(name + "_j_bot", x0, x1, y - 0.06, y + 0.06, z0, z0 + 0.06, M_FRAME)
        cube(name + "_j_top", x0, x1, y - 0.06, y + 0.06, z1 - 0.06, z1, M_FRAME)
        # Vierteaguas exterior
        cube(name + "_sill", x0 - 0.05, x1 + 0.05, y - 0.18, y - 0.06, z0 - 0.04, z0, M_GREY)
    # Doble acristalamiento con grosor 3D
    cube(name + "_glass_pane", x0 + 0.02, x1 - 0.02, y - 0.015, y + 0.015, z0 + 0.04, z1 - 0.04, mat)


def glass_v(name, x, y0, y1, z0, z1, mat=M_GLASS, frame=True):
    # Marco de 4 lados (inferior, superior, izq, der)
    if frame:
        cube(name + "_j0", x - 0.06, x + 0.06, y0 - 0.04, y0 + 0.04, z0, z1, M_FRAME)
        cube(name + "_j1", x - 0.06, x + 0.06, y1 - 0.04, y1 + 0.04, z0, z1, M_FRAME)
        cube(name + "_j_bot", x - 0.06, x + 0.06, y0, y1, z0, z0 + 0.06, M_FRAME)
        cube(name + "_j_top", x - 0.06, x + 0.06, y0, y1, z1 - 0.06, z1, M_FRAME)
        # Vierteaguas exterior
        cube(name + "_sill", x - 0.18, x - 0.06, y0 - 0.05, y1 + 0.05, z0 - 0.04, z0, M_GREY)
    # Doble acristalamiento con grosor 3D
    cube(name + "_glass_pane", x - 0.015, x + 0.015, y0 + 0.02, y1 - 0.02, z0 + 0.04, z1 - 0.04, mat)


def door_h(name, y, x0, x1, z0=0.0, z1=2.1, mat=M_WOOD2):
    # Marco completo (jambas izq/der y dintel superior)
    cube(name + "_f0", x0 - 0.03, x0 + 0.03, y - 0.06, y + 0.06, z0, z1, M_FRAME)
    cube(name + "_f1", x1 - 0.03, x1 + 0.03, y - 0.06, y + 0.06, z0, z1, M_FRAME)
    cube(name + "_top", x0, x1, y - 0.06, y + 0.06, z1 - 0.05, z1, M_FRAME)
    # Hoja de puerta
    cube(name + "_panel", x0 + 0.02, x1 - 0.02, y - 0.03, y + 0.03, z0, z1 - 0.04, mat)
    # Manetas metálicas en ambos lados
    mx = x1 - 0.12 if (x1 - x0) > 0.8 else x0 + 0.12
    cylinder(name + "_handle_l", mx, y - 0.08, 0.015, z0 + 1.0, z0 + 1.05, M_CHROME, n=8)
    cylinder(name + "_handle_r", mx, y + 0.08, 0.015, z0 + 1.0, z0 + 1.05, M_CHROME, n=8)


def door_v(name, x, y0, y1, z0=0.0, z1=2.1, mat=M_WOOD):
    # Marco completo (jambas inf/sup y dintel superior)
    cube(name + "_f0", x - 0.06, x + 0.06, y0 - 0.03, y0 + 0.03, z0, z1, M_FRAME)
    cube(name + "_f1", x - 0.06, x + 0.06, y1 - 0.03, y1 + 0.03, z0, z1, M_FRAME)
    cube(name + "_top", x - 0.06, x + 0.06, y0, y1, z1 - 0.05, z1, M_FRAME)
    # Hoja de puerta
    cube(name + "_panel", x - 0.03, x + 0.03, y0 + 0.02, y1 - 0.02, z0, z1 - 0.04, mat)
    # Manetas metálicas en ambos lados
    my = y1 - 0.12 if (y1 - y0) > 0.8 else y0 + 0.12
    cylinder(name + "_handle_l", x - 0.08, my, 0.015, z0 + 1.0, z0 + 1.05, M_CHROME, n=8)
    cylinder(name + "_handle_r", x + 0.08, my, 0.015, z0 + 1.0, z0 + 1.05, M_CHROME, n=8)


# ================================================================ mobiliario
def tree(name, x, y, s=1.0):
    cylinder(name + "_trunk", x, y, 0.16 * s, 0.0, 2.2 * s, M_TRUNK, n=10)
    uv_sphere(name + "_c1", x, y, 2.6 * s, 1.15 * s, M_LEAF, n=14)
    uv_sphere(name + "_c2", x - 0.5 * s, y + 0.35 * s, 3.0 * s, 0.75 * s, M_LEAF2, n=12)
    uv_sphere(name + "_c3", x + 0.55 * s, y - 0.3 * s, 3.0 * s, 0.75 * s, M_LEAF2, n=12)


def plant(name, x, y, s=0.7):
    cylinder(name + "_stem", x, y, 0.04 * s, 0.0, 0.35 * s, M_TRUNK, n=6)
    uv_sphere(name + "_leaf", x, y, 0.45 * s, 0.22 * s, M_LEAF2, n=10)


def table(name, x, y, w=1.6, d=0.9, h=0.74, top=M_WOOD, legs=M_WOOD2):
    cube(name + "_top", x - w / 2, x + w / 2, y - d / 2, y + d / 2, h - 0.04, h + 0.03, top)
    for sx in (-1, 1):
        for sy in (-1, 1):
            cube(name + "_leg", x + sx * (w / 2 - 0.05), x + sx * (w / 2 - 0.01),
                 y + sy * (d / 2 - 0.05), y + sy * (d / 2 - 0.01), 0.0, h - 0.04, legs)


def chair(name, x, y, color=M_WOOD2):
    cube(name + "_seat", x - 0.22, x + 0.22, y - 0.22, y + 0.22, 0.44, 0.50, color)
    cube(name + "_base", x - 0.20, x + 0.20, y - 0.20, y + 0.20, 0.30, 0.44, color)
    cube(name + "_back", x - 0.22, x + 0.22, y - 0.22, y - 0.10, 0.50, 0.95, color)


def bed(name, x, y, w=1.6, d=2.0, color=M_BED, head=(0.55, 0.52, 0.62)):
    cube(name + "_base", x - w / 2, x + w / 2, y - d / 2, y + d / 2, 0.0, 0.30, M_WOOD2)
    cube(name + "_matt", x - w / 2, x + w / 2, y - d / 2, y + d / 2, 0.30, 0.52, color)
    cube(name + "_pillow", x - w / 2, x + w / 2, y - d / 2 + 0.02, y - d / 2 + 0.55, 0.52, 0.60, M_WHITE)
    cube(name + "_head", x - w / 2 - 0.04, x + w / 2 + 0.04, y - d / 2 - 0.06, y - d / 2 + 0.10,
         0.30, 1.15, mat("_bedhead", head, 0.8))


def wardrobe(name, x, y, w=2.0, d=0.6, h=2.3, color=M_WOOD):
    cube(name, x, x + w, y, y + d, 0.0, h, color)
    for i in range(2):
        cube(name + "_div", x + w * (i + 0.5) - 0.015, x + w * (i + 0.5) + 0.015, y, y + d, 0.0, h, M_WOOD2)


def sofa(name, x, y, w=2.2, d=0.9, color=M_SOFA):
    cube(name + "_base", x, x + w, y, y + d, 0.0, 0.42, color)
    cube(name + "_back", x, x + w, y, y + 0.18, 0.42, 0.95, color)
    cube(name + "_arm_l", x, x + 0.22, y, y + d, 0.42, 0.80, color)
    cube(name + "_arm_r", x + w - 0.22, x + w, y, y + d, 0.42, 0.80, color)
    cube(name + "_pillows", x + 0.25, x + w - 0.25, y + 0.15, y + 0.30, 0.52, 0.62, M_WHITE)


def tv(name, x, y, w=1.4, h=0.8, screen=M_DARK):
    cube(name + "_stand", x - w / 2 - 0.03, x + w / 2 + 0.03, y - 0.30, y + 0.30, 0.05, 0.85, M_WOOD2)
    cube(name + "_panel", x - w / 2, x + w / 2, y - 0.03, y + 0.03, 0.75, 0.75 + h, M_FRAME)
    cube(name + "_screen", x - w / 2 + 0.03, x + w / 2 - 0.03, y - 0.02, y + 0.02, 0.78, 0.78 + h - 0.05,
         mat("_screen", (0.08, 0.1, 0.12), 0.1))


def kitchen_units(name, x0, x1, y0, zbase, mat_body=M_KITCH, n=4):
    cube(name + "_base", x0, x1, y0, y0 + 0.62, zbase, zbase + 0.96, mat_body)
    cube(name + "_top", x0, x1, y0, y0 + 0.62, zbase + 0.96, zbase + 1.0, M_COUNT)
    cube(name + "_up", x0, x1, y0, y0 + 0.40, zbase + 1.45, zbase + 2.25, mat_body)


def toilet(name, x, y, color=(0.95, 0.95, 0.95)):
    m = mat("_wc", color, 0.4)
    cube(name + "_bowl", x - 0.18, x + 0.18, y, y + 0.34, 0.36, 0.42, m)
    cube(name + "_ped", x - 0.15, x + 0.15, y - 0.28, y + 0.02, 0.10, 0.36, m)


def sink(name, x, y, color=(0.92, 0.92, 0.9)):
    m = mat("_sink", color, 0.35)
    cube(name + "_basin", x - 0.3, x + 0.3, y - 0.22, y + 0.22, 0.76, 0.80, m)
    cube(name + "_ped", x - 0.3, x + 0.3, y - 0.22, y + 0.22, 0.80, 1.02, m)


def shower(name, x, y, w=0.9):
    m = mat("_shower_floor", (0.7, 0.75, 0.74), 0.4)
    cube(name + "_floor", x - w / 2, x + w / 2, y, y + w, 0.0, 0.12, m)
    glass_v(name + "_wall", x + w / 2, y, y + w, 0.12, 2.1, frame=False)


def car(name, x, y, body=M_CAR, roof=M_CARBODY):
    cube(name + "_body", x - 0.95, x + 0.95, y - 2.05, y + 2.05, 0.25, 0.62, body)
    cube(name + "_cabin", x - 0.70, x + 0.30, y - 1.15, y + 1.15, 0.62, 1.02, roof)
    cube(name + "_glass_f", x - 0.66, x + 0.26, y - 1.12, y + 1.12, 0.62, 0.72, M_CARWIN)
    for wy in (-1.5, 1.5):
        for wx in (-0.7, 0.7):
            cylinder(name + f"_w{wx}{wy}", x + wx, y + wy, 0.34, 0.0, 0.25, M_CHROME, n=14)
            cylinder(name + f"_t{wx}{wy}", x + wx, y + wy, 0.18, 0.0, 0.27, M_DARK, n=14)


def stairs(name, x0, x1, y0, y1, z0, z1, n=16):
    h = (z1 - z0) / n
    t = (y1 - y0) / n
    for i in range(n):
        ya = y0 + i * t
        cube(f"{name}_step{i}", x0, x1, ya, ya + t, z0 + i * h, z0 + (i + 1) * h, M_STONE)
    cube(name + "_rail", x0 - 0.06, x0 + 0.06, y0, y1, z0, z0 + n * h + 0.35, M_METAL)


print("FUNCIONES OK")
