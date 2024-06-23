
#General Import/Export functions that can be used a bit everywhere 

import bpy
import os

from . import coll_utils

from . extra_utils import dprint


#  dP""b8 888888  dP"Yb  88b 88  dP"Yb  8888b.  888888
# dP   `" 88__   dP   Yb 88Yb88 dP   Yb  8I  Yb 88__
# Yb  "88 88""   Yb   dP 88 Y88 Yb   dP  8I  dY 88""
#  YboodP 888888  YbodP  88  Y8  YbodP  8888Y"  888888


def import_geonodes( blend_path, geonode_names, link=False, ):
    """import geonode(s) from given blend_path"""
    return_list=[]
        
    with bpy.data.libraries.load(blend_path, link=link) as (data_from, data_to):
        
        #loop over every nodegroups in blend
        for g in data_from.node_groups:
            
            #check for name
            if g in geonode_names:
                
                #add to return list 
                if g not in return_list:
                    return_list.append(g)
                    
                #check if not already imported
                if g not in bpy.data.node_groups:
                    # add to import list  
                    data_to.node_groups.append(g)
                    
            continue

    if (len(return_list)==0):
        return [None]

    return return_list


def import_and_add_geonode(o, mod_name="", node_name="", blend_path="", copy=True, use_fake_user=True, unique_nodegroups=[], show_viewport=True,):
    """Create a geonode modifier, import node from blend path if does not exist in user file
    use 'unique_nodegroups' argument to automatically make nodegroups contained within this modifier unique"""

    #create new modifier that will gost geonode
    m = o.modifiers.new(name=mod_name,type="NODES")
    m.show_viewport = show_viewport
        
    #get geonodegraph
    geonode = bpy.data.node_groups.get(node_name)
    
    #import geonodegraph if not already in blend?
    if (geonode is None):
        import_geonodes(blend_path,[node_name],)
        geonode = bpy.data.node_groups[node_name]
        geonode.use_fake_user = use_fake_user
        
    #is geonodegraph unique? 
    if (copy):
        geonode = geonode.copy()

    #control if some nodegroups in this geonodegraph needs to be unique ?
    #even support up to 1x level nested (ex "s_distribution_manual.uuid_equivalence")
    for nm in unique_nodegroups:

        nnm = None 
        if ("." in nm):
            nm,nnm,*_ = nm.split(".")

        n = geonode.nodes.get(nm)

        if (n is None):
            print("ERROR failed to copy() ",nm)
            continue
            
        #support 1x level nested?
        if (nnm is not None):
            nn = n.node_tree.nodes.get(nnm)
            if (nn is None):
                print("ERROR failed to copy() ",nnm)
                continue
            nn.node_tree = nn.node_tree.copy()
            del nnm
            continue

        n.node_tree = n.node_tree.copy()    
        continue

    #assign nodegraph to modifier
    m.node_group = geonode
    
    #correct potential bug, unconnected nodes!
    from .. scattering.update_factory import ensure_buggy_links
    ensure_buggy_links()
    
    return m 


#  dP"Yb  88""Yb  88888 888888  dP""b8 888888 .dP"Y8
# dP   Yb 88__dP     88 88__   dP   `"   88   `Ybo."
# Yb   dP 88""Yb o.  88 88""   Yb        88   o.`Y8b
#  YbodP  88oodP "bodP' 888888  YboodP   88   8bodP'


def import_objects( blend_path="", object_names=[], link=False, link_coll="Geo-Scatter Import",):
    """import obj(s) from given blend_path"""

    #if all object names are already imported, then we simply skip this function
    if all([n in bpy.data.objects for n in object_names]):
        return object_names

    dprint(f"import_objects({os.path.basename(blend_path)})->start")

    r_list=[]

    with bpy.data.libraries.load(blend_path, link=link) as (data_from, data_to):
        
        #loop over every obj in blend
        for g in data_from.objects:
            
            #check if name in selected and not import twice
            if (g in object_names) and (g not in r_list):
                r_list.append(g)
                
                #import in data.objects if not already exists in this blend of course!
                if (g not in bpy.data.objects):
                    data_to.objects.append(g)
            
            continue

    dprint("import_objects->end")

    #Nothing found ?
    if (len(r_list)==0):
        return [None]

    #cleanse asset mark?
    for n in r_list:
        o = bpy.data.objects.get(n)
        if (o is None):
            continue
        if (o.asset_data is None):
            continue
        o.asset_clear()
        continue

    #store import in collection?
    if (link_coll not in (None,""),):
        
        #create Geo-Scatter collections if not already
        coll_utils.create_scatter5_collections()
        
        #get collection, create if not found
        import_coll = coll_utils.create_new_collection(link_coll, parent_name="Geo-Scatter")
        
        #always move imported in collection
        for n in r_list:
            if (n not in import_coll.objects):
                import_coll.objects.link(bpy.data.objects[n])

    return r_list


def export_objects( blend_path, objects_list, ):
    """export obj in a new .blend"""

    data_blocks = set(objects_list)
    bpy.data.libraries.write(blend_path, data_blocks, )

    return None


#    db    .dP"Y8 .dP"Y8 888888 888888     88""Yb 88""Yb  dP"Yb  Yb        dP .dP"Y8 888888 88""Yb
#   dPYb   `Ybo." `Ybo." 88__     88       88__dP 88__dP dP   Yb  Yb  db  dP  `Ybo." 88__   88__dP
#  dP__Yb  o.`Y8b o.`Y8b 88""     88       88""Yb 88"Yb  Yb   dP   YbdPYbdP   o.`Y8b 88""   88"Yb
# dP""""Yb 8bodP' 8bodP' 888888   88       88oodP 88  Yb  YbodP     YP  YP    8bodP' 888888 88  Yb


def get_selected_assets(context):
    """get the selected assets, of the first window found, first area"""

    #set global context
    assets, window, area = [], None, None

    #is context area already correct?
    if (context.area.ui_type=="ASSETS"):
        window, area = context.window, context.area

    #else try to find AB area in context window first
    if (area is None):
        for a in context.window.screen.areas:
            if (a.ui_type=="ASSETS"):
                window, area = context.window, a
                break

    #else try other windows?
    if (area is None):
        for w in context.window_manager.windows:
            for a in w.screen.areas:
                if (a.ui_type=="ASSETS"):
                    window, area = w, a
                    break

    #else raise error..
    if (area is None):
        print("SCATTER5_OT_get_browser_items->No match for windows/areas")
        return {'FINISHED'}

    #get assets, only object or collection
    with context.temp_override(window=window,area=area):
        for ass in bpy.context.selected_assets:
            if ass.id_type in ("OBJECT","COLLECTION"):
                assets.append(ass)
        
    return assets


def import_selected_assets(link=False, link_coll="Geo-Scatter Import",):
    """import selected object type assets from browser, link/append depends on technique"""

    #create Geo-Scatter collections if not already
    coll_utils.create_scatter5_collections()    
    #and create the return value list
    objects_found = []

    #define and get globals via operators in order to override contexts
    ass_ets = get_selected_assets(bpy.context)
    
    #did we found something?
    if (len(ass_ets)==0):
        return objects_found
    
    #we try to import the assets

    #sort assets by path (in order to batch import them)
    to_import = {}
    for ass in ass_ets:
        asspath = ass.full_library_path
        if (asspath not in to_import.keys()):
            to_import[asspath] = []
        to_import[asspath].append(ass.name)
        continue

    #import assets from path 
    for p,names in to_import.items():
        
        #import all the objects/collection objects
        import_objects(
            blend_path=p,
            object_names=names,
            link=link,
            )
        
        #mark them as found
        for n in names:
            o = bpy.data.objects.get(n)
            if (o is not None): 
                objects_found.append(o)
                
        continue
        
    return objects_found 


# 8b    d8    db    888888 888888 88""Yb 88    db    88
# 88b  d88   dPYb     88   88__   88__dP 88   dPYb   88
# 88YbdP88  dP__Yb    88   88""   88"Yb  88  dP__Yb  88  .o
# 88 YY 88 dP""""Yb   88   888888 88  Yb 88 dP""""Yb 88ood8


def import_materials(blend_path, material_names, link=False,):
    """import materials by name into blender data"""

    #if all material names are already imported, then we simply skip this function
    if all([n in bpy.data.materials for n in material_names]):
        return material_names

    r_list=[]

    with bpy.data.libraries.load(blend_path, link=link) as (data_from, data_to):
        
        #loop over every nodegroups in blend
        for g in data_from.materials:
            
            #check for name
            if (g in material_names):
                
                #add to return list 
                if (g not in r_list):
                    r_list.append(g)
                    
                #check if not already imported
                if (g not in bpy.data.materials):
                    # add to import list  
                    data_to.materials.append(g)
                    
            continue

    if (len(r_list)==0):
        return [None]

    return r_list


# 88 8b    d8    db     dP""b8 888888
# 88 88b  d88   dPYb   dP   `" 88__
# 88 88YbdP88  dP__Yb  Yb  "88 88""
# 88 88 YY 88 dP""""Yb  YboodP 888888


def import_image(fpath, hide=False, use_fake_user=False):
    """import images in bpy.data.images"""

    if (not os.path.exists(fpath)):
        return None 

    fname = os.path.basename(fpath)
    if (hide):
        fname = "." + fname

    image = bpy.data.images.get(fname)
    if (image is None):
        image = bpy.data.images.load(fpath) 
        image.name = fname

    image.use_fake_user=use_fake_user
    return image 


# 888888 Yb  dP 88""Yb  dP"Yb  88""Yb 888888     .dP"Y8 888888 88""Yb 88    db    88     88 8888P    db    888888 88  dP"Yb  88b 88
# 88__    YbdP  88__dP dP   Yb 88__dP   88       `Ybo." 88__   88__dP 88   dPYb   88     88   dP    dPYb     88   88 dP   Yb 88Yb88
# 88""    dPYb  88"""  Yb   dP 88"Yb    88       o.`Y8b 88""   88"Yb  88  dP__Yb  88  .o 88  dP    dP__Yb    88   88 Yb   dP 88 Y88
# 888888 dP  Yb 88      YbodP  88  Yb   88       8bodP' 888888 88  Yb 88 dP""""Yb 88ood8 88 d8888 dP""""Yb   88   88  YbodP  88  Y8


def serialization(d):
    """convert unknown blendertypes"""

    from mathutils import Euler, Vector, Color

    for key,value in d.items():
        
        #convert blender array type to list
        if (type(value) in [Euler, Vector, Color, bpy.types.bpy_prop_array]):
            d[key] = value[:] 
            
        #recursion needed for pattern texture data storage for example
        elif (type(value)==dict):
            d[key] = serialization(value)
        continue

    return d


#   .oooooo.   oooo
#  d8P'  `Y8b  `888
# 888           888   .oooo.    .oooo.o  .oooo.o  .ooooo.   .oooo.o
# 888           888  `P  )88b  d88(  "8 d88(  "8 d88' `88b d88(  "8
# 888           888   .oP"888  `"Y88b.  `"Y88b.  888ooo888 `"Y88b.
# `88b    ooo   888  d8(  888  o.  )88b o.  )88b 888    .o o.  )88b
#  `Y8bood8P'  o888o `Y888""8o 8""888P' 8""888P' `Y8bod8P' 8""888P'


classes = (
        
    )