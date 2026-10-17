import urllib.request, json, os
import bpy

base_dir = r"C:\Users\Oscar Martinez\Desktop\mi-casa"
os.chdir(base_dir)

def get_asset_id(search_type, query):
    url = f"https://api.polyhaven.com/assets?t={search_type}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        res = urllib.request.urlopen(req)
        data = json.loads(res.read())
        matches = [k for k in data.keys() if query.replace('_',' ') in k.replace('_',' ') or query in k]
        if not matches:
            # fallback loose search
            matches = [k for k in data.keys() if any(w in k for w in query.split('_'))]
        if not matches:
            print(f"No results for {query}")
            return None
        print(f"Found {matches[0]} for {query}")
        return matches[0]
    except Exception as e:
        print(f"Error fetching {query}: {e}")
        return None

def apply_hdri(query):
    asset_id = get_asset_id('hdris', query)
    if not asset_id: return
    print(f"Applying HDRI: {asset_id}")
    url = f"https://api.polyhaven.com/files/{asset_id}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    res = urllib.request.urlopen(req)
    files = json.loads(res.read())
    hdri_url = files['hdri']['2k']['exr']['url']
    path = os.path.join(base_dir, f"{asset_id}_2k.exr")
    if not os.path.exists(path):
        urllib.request.urlretrieve(hdri_url, path)
    
    world = bpy.context.scene.world
    if not world:
        world = bpy.data.worlds.new("World")
        bpy.context.scene.world = world
    world.use_nodes = True
    tree = world.node_tree
    nodes = tree.nodes
    links = tree.links
    
    nodes.clear()
    
    tex_env = nodes.new('ShaderNodeTexEnvironment')
    tex_env.image = bpy.data.images.load(filepath=os.path.abspath(path))
    bg = nodes.new('ShaderNodeBackground')
    out = nodes.new('ShaderNodeOutputWorld')
    
    links.new(tex_env.outputs[0], bg.inputs[0])
    links.new(bg.outputs[0], out.inputs[0])

def apply_texture(query, objects_filter_func):
    asset_id = get_asset_id('textures', query)
    if not asset_id: return
    print(f"Applying texture: {asset_id}")
    
    url = f"https://api.polyhaven.com/files/{asset_id}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    res = urllib.request.urlopen(req)
    files = json.loads(res.read())
    
    blend_url = files['blend']['2k']['blend']['url']
    blend_path = os.path.join(base_dir, f"{asset_id}_2k.blend")
    
    if not os.path.exists(blend_path):
        urllib.request.urlretrieve(blend_url, blend_path)
    
    with bpy.data.libraries.load(blend_path, link=False) as (data_from, data_to):
        data_to.materials = data_from.materials
    
    mat = None
    if data_to.materials:
        mat = data_to.materials[0]
        print(f"Loaded material: {mat.name}")
    else:
        return
        
    for obj in bpy.data.objects:
        if obj.type == 'MESH' and objects_filter_func(obj.name):
            if not obj.data.materials:
                obj.data.materials.append(mat)
            else:
                obj.data.materials[0] = mat
            print(f"Assigned {mat.name} to {obj.name}")

apply_hdri('courtyard')
apply_texture('wood_floor', lambda n: (n.startswith('pav_') or n.startswith('pavPA_')) and 'patio' not in n and 'porche' not in n and 'cochera' not in n)
apply_texture('plaster', lambda n: n.startswith(('mF_', 'mPA_F', 'mT_', 'mPA_T')))
apply_texture('cobblestone', lambda n: n == 'patio_suelo')
apply_texture('concrete', lambda n: n.startswith('sidewalk') or n.startswith('acera'))
apply_texture('marble', lambda n: n in ('isla_top', 'islaPA_top'))

bpy.ops.wm.save_mainfile(filepath=r"C:\Users\Oscar Martinez\Desktop\mi-casa\casa-bifamiliar-3d.blend")
