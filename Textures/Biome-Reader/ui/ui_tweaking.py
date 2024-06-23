
#####################################################################################################
#
# ooooo     ooo ooooo      ooooooooooooo                                      oooo         o8o
# `888'     `8' `888'      8'   888   `8                                      `888         `"'
#  888       8   888            888      oooo oooo    ooo  .ooooo.   .oooo.    888  oooo  oooo  ooo. .oo.    .oooooooo
#  888       8   888            888       `88. `88.  .8'  d88' `88b `P  )88b   888 .8P'   `888  `888P"Y88b  888' `88b
#  888       8   888            888        `88..]88..8'   888ooo888  .oP"888   888888.     888   888   888  888   888
#  `88.    .8'   888            888         `888'`888'    888    .o d8(  888   888 `88b.   888   888   888  `88bod8P'
#    `YbodP'    o888o          o888o         `8'  `8'     `Y8bod8P' `Y888""8o o888o o888o o888o o888o o888o `8oooooo.
#                                                                                                           d"     YD
#####################################################################################################       "Y88888P'


import bpy

from .. resources.icons import cust_icon
from .. resources.translate import translate

from .. utils.str_utils import word_wrap, count_repr

from .. scattering.texture_datablock import draw_texture_datablock

from . import ui_templates
from . ui_emitter_select import emitter_header


# oooooooooooo                                       .    o8o
# `888'     `8                                     .o8    `"'
#  888         oooo  oooo  ooo. .oo.    .ooooo.  .o888oo oooo   .ooooo.  ooo. .oo.    .oooo.o
#  888oooo8    `888  `888  `888P"Y88b  d88' `"Y8   888   `888  d88' `88b `888P"Y88b  d88(  "8
#  888    "     888   888   888   888  888         888    888  888   888  888   888  `"Y88b.
#  888          888   888   888   888  888   .o8   888 .  888  888   888  888   888  o.  )88b
# o888o         `V88V"V8P' o888o o888o `Y8bod8P'   "888" o888o `Y8bod8P' o888o o888o 8""888P'


def get_props():
    """get useful props used in interface""" 
    #IMPORTANT NOTE: perhaps a bad idea to constanly call this funciton in GUI, too many repetitive calls?

    addon_prefs = bpy.context.preferences.addons["Biome-Reader"].preferences
    scat_win    = bpy.context.window_manager.scatter5
    scat_ui     = scat_win.ui
    scat_scene  = bpy.context.scene.scatter5
    emitter     = scat_scene.emitter
    psy_active  = emitter.scatter5.get_psy_active()
    group_active  = emitter.scatter5.get_group_active()

    return (addon_prefs, scat_scene, scat_ui, scat_win, emitter, psy_active, group_active)

def warnings(layout, active=True, created=True,):
    """check if interface should be drawn, if nothing created or active"""

    emitter    = bpy.context.scene.scatter5.emitter
    psy_active = emitter.scatter5.get_psy_active()

    if (psy_active is None):

        txt = layout.row()
        txt.alignment = "CENTER"
        txt.label(text=translate("No System(s) Active."), icon="INFO") #unlikely
        ui_templates.separator_box_in(layout)
        
        return True

    return False

def lock_check(psy_active, s_category="s_distribution", prop=None ):
    """check if category is locked"""

    if psy_active.is_locked(s_category):
        return False 
    return prop

def active_check(psy_active, s_category="s_distribution", prop=None ):
    """check if category master allow is off"""

    if ( not getattr(psy_active,f"{s_category}_master_allow") ):
        return False 
    return prop


#  8888b.  88""Yb    db    Yb        dP     888888 888888 8b    d8 88""Yb 88        db    888888 888888 .dP"Y8
#   8I  Yb 88__dP   dPYb    Yb  db  dP        88   88__   88b  d88 88__dP 88       dPYb     88   88__   `Ybo."
#   8I  dY 88"Yb   dP__Yb    YbdPYbdP         88   88""   88YbdP88 88"""  88  .o  dP__Yb    88   88""   o.`Y8b
#  8888Y"  88  Yb dP""""Yb    YP  YP          88   888888 88 YY 88 88     88ood8 dP""""Yb   88   888888 8bodP'


def draw_visibility_methods(psy_active, layout, api):
    """draw viewport method in visibility and display features"""

    if (not layout):
        return None

    if (bpy.context.preferences.addons["Biome-Reader"].preferences.debug_interface):
        row = layout.row(align=True)
        row.alignment = "RIGHT"
        row.scale_x = 0.9
        row.prop(psy_active,f"{api}_viewport_method", text="")

    row = layout.box().row(align=True)
    row.alignment = "RIGHT"
    row.scale_y = 0.4
    row.scale_x = 0.95
    
    is_shaded = getattr(psy_active,f"{api}_allow_shaded")
    is_render = getattr(psy_active,f"{api}_allow_render")

    row.emboss = "NONE"
    rwoo = row.row(align=True) ; rwoo.active = True      ; rwoo.prop(psy_active,f"{api}_allow_screen", text="", icon="RESTRICT_VIEW_OFF",)
    rwoo = row.row(align=True) ; rwoo.active = is_shaded ; rwoo.prop(psy_active,f"{api}_allow_shaded", text="", icon="SHADING_RENDERED" if is_shaded else "NODE_MATERIAL")
    rwoo = row.row(align=True) ; rwoo.active = True      ; rwoo.prop(psy_active,f"{api}_allow_render", text="", icon="RESTRICT_RENDER_OFF" if is_render else "RESTRICT_RENDER_ON")    

    return None 

def draw_coll_ptr_prop(layout=None, system=None, api="", revert_api="", add_coll_name="", add_parent_name="Geo-Scatter User Col", draw_popover=True):
    """draw collection pointer template, for psy or group"""
        
    ptr_str = getattr(system,api)
    coll = bpy.data.collections.get(ptr_str)

    row = layout.row(align=True)

    #draw popover 
    if (coll is not None and draw_popover):
        pop = row.row(align=True)
        
        #transfer arguments for collection drawing & add/remove buttons
        pop.context_pointer_set("pass_ui_arg_collection", coll,)
        pop.context_pointer_set("pass_ui_arg_prop_name", getattr(system, f"passctxt_{api}"),)
        pop.popover(panel="SCATTER5_PT_collection_popover", text="", icon="OUTLINER",)

    #draw prop search
    row.prop_search( system, api, bpy.data, "collections",text="",)

    #draw arrow if filled and option
    if (coll is not None):
        if (revert_api!=""):
            row.prop( system, revert_api, text="",icon="ARROW_LEFTRIGHT")
    else: 
        op = row.operator("scatter5.create_coll", text="", icon="ADD")
        op.api = f"{'psy_active' if (type(system).__name__=='SCATTER5_PR_particle_systems') else 'group_active'}.{api}" 
        op.pointer_type = "str"
        op.coll_name = add_coll_name
        op.parent_name = add_parent_name

    return coll, row

def draw_camera_update_method(layout=None, psy_active=None):
    """draw context_scene.scatter5 camera update dependencies method"""

    scat_scene  = bpy.context.scene.scatter5

    col = layout.column(align=True)
    txt = col.row()
    txt.label(text=translate("Cam Update")+" :")

    col.prop(scat_scene,"factory_cam_update_method", text="")

    if (scat_scene.factory_cam_update_method=="update_delayed"):
        col.prop( scat_scene, "factory_cam_update_ms")
        col.separator(factor=0.5)

    elif (scat_scene.factory_cam_update_method=="update_apply") and psy_active:
        col.operator("scatter5.exec_line", text=translate("Refresh"), icon="FILE_REFRESH").api = f"psy_active.s_visibility_camdist_allow = not psy_active.s_visibility_camdist_allow ; psy_active.s_visibility_camdist_allow = not psy_active.s_visibility_camdist_allow"
        col.separator(factor=0.5)

    return None 

def draw_transition_control_feature(layout=None, psy_active=None, api="", fallnoisy=True,):
    """draw the transition control feature, this feature is repeated many times"""

    tocol, is_toggled = ui_templates.bool_toggle(layout, 
        prop_api=psy_active,
        prop_str=f"{api}_fallremap_allow",
        label=translate("Transition Control"),
        icon="FCURVE", 
        left_space=False,
        return_layout=True,
        )
    if is_toggled:

        #special case for camera distance, nodes is not the same as api
        if (api=="s_visibility_camdist"):
            api = "s_visibility_cam"

        #find back the fallremap node, the name node names & structure are standardized, otherwise will lead to issues!
        opapi = f"bpy.data.objects['{psy_active.scatter_obj.name}'].modifiers['{psy_active.get_scatter_mod().name}'].node_group.nodes['{api}'].node_tree.nodes['fallremap']"
        
        ope = tocol.row(align=True)
        op = ope.operator("scatter5.graph_dialog",text=translate("Falloff Graph"),icon="FCURVE")
        op.source_api = opapi
        op.mapping_api = f"{opapi}.mapping"
        op.psy_name = psy_active.name
            
        #special case for camera distance
        if (api=="s_visibility_cam"):
              ope.prop( psy_active, f"s_visibility_camdist_fallremap_revert", text="", icon="ARROW_LEFTRIGHT",)
        else: ope.prop( psy_active, f"{api}_fallremap_revert", text="", icon="ARROW_LEFTRIGHT",)

        tocol.separator(factor=0.3)

        if (fallnoisy):

            noisyt = tocol.column(align=True)
            noisyt.scale_y = 0.9
            noisyt.label(text=translate("Noise")+":")
            noisyt.prop( psy_active, f"{api}_fallnoisy_strength")
            noisytt = noisyt.column(align=True)
            noisytt.active = getattr(psy_active, f"{api}_fallnoisy_strength")!=0
            noisytt.prop( psy_active, f"{api}_fallnoisy_scale")
            noisyp = noisytt.row(align=True)
            noisyp.prop( psy_active, f"{api}_fallnoisy_seed")
            noisyb = noisyp.row(align=True)
            noisyb.scale_x = 1.2
            noisyb.prop( psy_active, f"{api}_fallnoisy_is_random_seed", icon_value=cust_icon("W_DICE"),text="",)

            tocol.separator(factor=0.3)

    return tocol, is_toggled 

def draw_universal_masks(layout=None, mask_api="", psy_api=None,):
    """every universal masks api should have _mask_ptr _mask_reverse"""

    _mask_ptr_str = f"{mask_api}_mask_ptr"
    _mask_ptr_val = getattr(psy_api, f"{mask_api}_mask_ptr")
    _mask_method_val = getattr(psy_api,f"{mask_api}_mask_method")
    _mask_color_sample_method_val = getattr(psy_api,f"{mask_api}_mask_color_sample_method")

    #group_api = "particle_groups" if (type(system).__name__=="SCATTER5_PR_particle_systems") else "particle_groups" if (type(system).__name__=="SCATTER5_PR_particle_groups") else "ERROR_NOT_FOUND"
    
    col = layout.column(align=True)

    col.separator(factor=0.5)

    title = col.row(align=True)
    title.scale_y = 0.9
    title.label(text=translate("Feature Mask")+":",)
    
    method = col.row(align=True)
    method.prop(psy_api,f"{mask_api}_mask_method", text="",)# icon_only=True, emboss=True,)

    if (_mask_method_val=="none"):
        return None 

    #### #### #### vg method

    if (_mask_method_val=="mask_vg"):
            
        #Mask Ptr

        mask = col.row(align=True)

        ptr = mask.row(align=True)
        ptr.alert = ( bool(_mask_ptr_val) and (_mask_ptr_val not in psy_api.get_surfaces_match_attr("vg")(psy_api, bpy.context, _mask_ptr_val)) )
        ptr.prop( psy_api, _mask_ptr_str, text="", icon="GROUP_VERTEX",)

        buttons = mask.row(align=True)
        buttons.scale_x = 0.93

        if (_mask_ptr_val!=""):
            buttons.prop( psy_api, f"{mask_api}_mask_reverse",text="",icon="ARROW_LEFTRIGHT")

        op = buttons.operator("scatter5.vg_quick_paint",
            text="",
            icon="BRUSH_DATA" if _mask_ptr_val else "ADD",
            depress=((bpy.context.mode=="PAINT_WEIGHT") and (getattr(bpy.context.object.vertex_groups.active,"name",'')==_mask_ptr_val)),
            )
        op.group_name = _mask_ptr_val
        op.mode = "vg"
        op.api = f"emitter.scatter5.particle_systems['{psy_api.name}'].{_mask_ptr_str}"

    #### #### #### vcol method

    elif (_mask_method_val=="mask_vcol"):

        set_color = (1,1,1)

        if (_mask_ptr_val!=""):

            #set color
            equivalence = {"id_picker":getattr(psy_api,f"{mask_api}_mask_id_color_ptr"),"id_greyscale":(1,1,1),"id_red":(1,0,0),"id_green":(0,1,0),"id_blue":(0,0,1),"id_black":(0,0,0),"id_white":(1,1,1),"id_saturation":(1,1,1),"id_value":(1,1,1),"id_hue":(1,1,1),"id_lightness":(1,1,1),"id_alpha":(1,1,1),}
            set_color = equivalence[_mask_color_sample_method_val]

            #sample method

            meth = col.row(align=True)
            if (_mask_color_sample_method_val=="id_picker"):
                color = meth.row(align=True)
                color.scale_x = 0.35
                color.prop(psy_api, f"{mask_api}_mask_id_color_ptr",text="")
            meth.prop( psy_api, f"{mask_api}_mask_color_sample_method", text="")

        #Mask Ptr

        mask = col.row(align=True)

        ptr = mask.row(align=True)
        ptr.alert = ( bool(_mask_ptr_val) and (_mask_ptr_val not in psy_api.get_surfaces_match_attr("vcol")(psy_api, bpy.context, _mask_ptr_val)) )
        ptr.prop( psy_api, _mask_ptr_str, text="", icon="GROUP_VCOL",)

        buttons = mask.row(align=True)
        buttons.scale_x = 0.93

        if (_mask_ptr_val!=""):
            buttons.prop( psy_api, f"{mask_api}_mask_reverse",text="",icon="ARROW_LEFTRIGHT")

        op = buttons.operator("scatter5.vg_quick_paint",
            text="",icon="BRUSH_DATA" if _mask_ptr_val else "ADD",
            depress=((bpy.context.mode=="PAINT_VERTEX") and (getattr(bpy.context.object.data.color_attributes.active_color,"name",'')==_mask_ptr_val)),
            )
        op.group_name =_mask_ptr_val
        op.mode = "vcol"
        op.set_color = set_color
        op.api = f"emitter.scatter5.particle_systems['{psy_api.name}'].{_mask_ptr_str}"

    #### #### #### noise method

    elif (_mask_method_val=="mask_noise"):

            noise_sett = col.column(align=True)
            noise_sett.scale_y = 0.9

            noise_sett.prop(psy_api, f"{mask_api}_mask_noise_brightness",)
            noise_sett.prop(psy_api, f"{mask_api}_mask_noise_contrast",)
            
            noise_sett.prop(psy_api, f"{mask_api}_mask_noise_scale",)

            sed = noise_sett.row(align=True)
            sed.prop( psy_api, f"{mask_api}_mask_noise_seed")
            sedbutton = sed.row(align=True)
            sedbutton.scale_x = 1.2
            sedbutton.prop( psy_api,f"{mask_api}_mask_noise_is_random_seed", icon_value=cust_icon("W_DICE"),text="")

    return col

def draw_feature_influence(layout=None, system=None, api_name="",):
    """draw the feature influence api"""

    col=layout.column(align=True)
    lbl=col.row()
    lbl.scale_y = 0.9
    lbl.label(text=translate("Influence")+":")

    #loop the 4 possible domain influence, density, scale or rotation 2x

    for dom in ("dist","scale","nor","tan"): 

        domain_api = f"{api_name}_{dom}"
        prop = f"{domain_api}_infl_allow"

        #is property domain supported? 
        if (prop not in system.bl_rna.properties.keys()): 
            continue

        allow = getattr(system,prop)
            
        #enable influence
        row = col.row(align=True)
        enabled = getattr(system, prop)
        
        row.prop( system, prop, text="", icon="CHECKBOX_HLT" if enabled else "CHECKBOX_DEHLT",)

        row = row.row(align=True)
        row.enabled = enabled

        #influence value 
        row.prop( system, f"{domain_api}_influence")

        #influence revert if exists?
        rev_api = f"{domain_api}_revert"
        if (rev_api in system.bl_rna.properties.keys()): 
            row.prop( system, rev_api, text="", icon="ARROW_LEFTRIGHT")

        continue

    return None 


# ooo        ooooo            o8o                   ooooooooo.                                   oooo
# `88.       .888'            `"'                   `888   `Y88.                                 `888
#  888b     d'888   .oooo.   oooo  ooo. .oo.         888   .d88'  .oooo.   ooo. .oo.    .ooooo.   888
#  8 Y88. .P  888  `P  )88b  `888  `888P"Y88b        888ooo88P'  `P  )88b  `888P"Y88b  d88' `88b  888
#  8  `888'   888   .oP"888   888   888   888        888          .oP"888   888   888  888ooo888  888
#  8    Y     888  d8(  888   888   888   888        888         d8(  888   888   888  888    .o  888
# o8o        o888o `Y888""8o o888o o888o o888o      o888o        `Y888""8o o888o o888o `Y8bod8P' o888o


def draw_tweaking_panel(self,layout):
    """draw main tweaking panel"""

    addon_prefs, scat_scene, scat_ui, scat_win, emitter, psy_active, group_active = get_props()

    main = layout.column()
    main.enabled = scat_scene.ui_enabled

    ui_templates.separator_box_out(main)
    ui_templates.separator_box_out(main)

    draw_particle_selection(self,main)
    ui_templates.separator_box_out(main)

    if (group_active is not None):
        
        draw_group_beginner_masks(self,main)
        ui_templates.separator_box_out(main)
    
    
    elif (psy_active is not None):
        
        draw_beginner_interface(self,main)
        ui_templates.separator_box_out(main)

        draw_removal_interface(self,main)
        ui_templates.separator_box_out(main)


    draw_pros_interface(self,main)
    ui_templates.separator_box_out(main)

    ui_templates.separator_box_out(main)
    ui_templates.separator_box_out(main)

    return 


#  .oooooo..o           oooo                          .    o8o                                   .o.
# d8P'    `Y8           `888                        .o8    `"'                                  .888.
# Y88bo.       .ooooo.   888   .ooooo.   .ooooo.  .o888oo oooo   .ooooo.  ooo. .oo.            .8"888.     oooo d8b  .ooooo.   .oooo.
#  `"Y8888o.  d88' `88b  888  d88' `88b d88' `"Y8   888   `888  d88' `88b `888P"Y88b          .8' `888.    `888""8P d88' `88b `P  )88b
#      `"Y88b 888ooo888  888  888ooo888 888         888    888  888   888  888   888         .88ooo8888.    888     888ooo888  .oP"888
# oo     .d8P 888    .o  888  888    .o 888   .o8   888 .  888  888   888  888   888        .8'     `888.   888     888    .o d8(  888
# 8""88888P'  `Y8bod8P' o888o `Y8bod8P' `Y8bod8P'   "888" o888o `Y8bod8P' o888o o888o      o88o     o8888o d888b    `Y8bod8P' `Y888""8o


def draw_particle_selection(self,layout):

    addon_prefs, scat_scene, scat_ui, scat_win, emitter, psy_active, group_active = get_props()

    box, is_open = ui_templates.box_panel(self, layout, 
        prop_str = "ui_tweak_select", #INSTRUCTION:REGISTER:UI:BOOL_NAME("ui_tweak_select");BOOL_VALUE(1)
        icon = "PARTICLES", 
        name = translate("System(s) List"),
        doc_panel = "SCATTER5_PT_docs", 
        popover_argument = "ui_tweak_select", #INSTRUCTION:REGISTER:UI:ARGS_POINTERS("ui_tweak_select")
        )
    if is_open:

        from .ui_system_list import draw_particle_selection_inner
        draw_particle_selection_inner(box, addon_prefs, scat_scene, emitter, psy_active, group_active)

        ui_templates.separator_box_in(box)

    return None



# ooooo                          .
# `888'                        .o8
#  888  ooo. .oo.    .oooo.o .o888oo  .oooo.   ooo. .oo.    .ooooo.   .ooooo.   .oooo.o
#  888  `888P"Y88b  d88(  "8   888   `P  )88b  `888P"Y88b  d88' `"Y8 d88' `88b d88(  "8
#  888   888   888  `"Y88b.    888    .oP"888   888   888  888       888ooo888 `"Y88b.
#  888   888   888  o.  )88b   888 . d8(  888   888   888  888   .o8 888    .o o.  )88b
# o888o o888o o888o 8""888P'   "888" `Y888""8o o888o o888o `Y8bod8P' `Y8bod8P' 8""888P'


class SCATTER5_UL_list_instances(bpy.types.UIList):
    """instance area"""

    def __init__(self,):
       self.use_filter_sort_alpha = True
       self.use_filter_show = False

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        
        if not item:
            return 

        addon_prefs, scat_scene, scat_ui, scat_win, emitter, psy_active, group_active = get_props()
        coll = psy_active.s_instances_coll_ptr

        #find index 

        i = None
        for i,o in enumerate(sorted(coll.objects, key= lambda o:o.name)):
            i+=1
            if o==item:
                break

        row = layout.row(align=True)
        row.scale_y = 0.7

        #select operator 

        selct = row.row()

        if (bpy.context.mode=="OBJECT"):

            selct.active = (item==bpy.context.object)
            op = selct.operator("scatter5.select_object",emboss=False,text="",icon="RESTRICT_SELECT_OFF" if item in bpy.context.selected_objects else "RESTRICT_SELECT_ON")
            op.obj_name = item.name
            op.coll_name = coll.name

        #name 

        name = row.row()
        name.prop(item,"name", text="", emboss=False, )

        #pick method chosen? 

        if (psy_active.s_instances_pick_method != "pick_random"):

            #pick rate slider 

            if (psy_active.s_instances_pick_method == "pick_rate"):

                slider = row.row()

                if (i<=20):
                    slider.prop( psy_active, f"s_instances_id_{i:02}_rate", text="",)
                else:
                    slider.alignment = "RIGHT"
                    slider.label(text=translate("Not Supported"),)

            #pick index 

            elif (psy_active.s_instances_pick_method == "pick_idx"):

                slider = row.row()
                slider.alignment= "RIGHT"
                slider.label(text=f"{i-1:02} ")

            #pick scale 

            elif (psy_active.s_instances_pick_method == "pick_scale"):

                slider = row.row(align=True)

                if (i<=20):
                    slider.scale_x = 0.71
                    slider.prop( psy_active, f"s_instances_id_{i:02}_scale_min", text="",)
                    slider.prop( psy_active, f"s_instances_id_{i:02}_scale_max", text="",)
                else:
                    slider.operator("scatter5.dummy",text=translate("Not Supported"),)

            #pick color 

            elif (psy_active.s_instances_pick_method == "pick_color"):

                clr = row.row(align=True)
                clr.alignment = "RIGHT"

                if (i<=20):
                      clr.prop( psy_active, f"s_instances_id_{i:02}_color", text="",)
                else: clr.label(text=translate("Not Supported"),)

        #remove operator 

        ope = row.row(align=False)
        ope.scale_x = 0.9
        ope.operator("scatter5.remove_instances",emboss=False,text="",icon="TRASH").ins_name = item.name

        return



# oooooooooo.                        o8o
# `888'   `Y8b                       `"'
#  888     888  .ooooo.   .oooooooo oooo  ooo. .oo.   ooo. .oo.    .ooooo.  oooo d8b  .oooo.o
#  888oooo888' d88' `88b 888' `88b  `888  `888P"Y88b  `888P"Y88b  d88' `88b `888""8P d88(  "8
#  888    `88b 888ooo888 888   888   888   888   888   888   888  888ooo888  888     `"Y88b.
#  888    .88P 888    .o `88bod8P'   888   888   888   888   888  888    .o  888     o.  )88b
# o888bood8P'  `Y8bod8P' `8oooooo.  o888o o888o o888o o888o o888o `Y8bod8P' d888b    8""888P'
#                        d"     YD
#                        "Y88888P'


sepa_small = 0.15
sepa_large = 3.15

def draw_beginner_interface(self,layout):

    addon_prefs, scat_scene, scat_ui, scat_win, emitter, psy_active, group_active = get_props()

    box, is_open = ui_templates.box_panel(self, layout, 
        prop_str = "ui_tweak_beginners", #INSTRUCTION:REGISTER:UI:BOOL_NAME("ui_tweak_beginners");BOOL_VALUE(1)
        name = translate("Beginner Interface"),
        )
    if is_open:

            if warnings(box):
                return None

            main = box.column()

            row = main.row()
            s1 = row.column()
            s1.scale_x = 1.25
            s1.active = True
            s1.alignment = "RIGHT"
            s2 = row.column() 

            #density controls 

            if (psy_active.s_distribution_method=="random"):
                s1.label(text="Density")
                s2.prop(psy_active, "s_distribution_density",text="")

                s1.label(text="Collision")
                ope = s2.row(align=True)
                ope.prop(psy_active,"s_distribution_limit_distance_allow", text="", icon="CHECKBOX_HLT" if psy_active.s_distribution_limit_distance_allow else "CHECKBOX_DEHLT")
                ope2 = ope.row(align=True)
                ope2.enabled = psy_active.s_distribution_limit_distance_allow
                ope2.prop(psy_active,"s_distribution_limit_distance",text="") 
                
            else:
                s1.label(text="Density")
                ope = s2.row()
                ope.active = False
                ope.operator("scatter5.dummy", text="Read Only")

            s1.separator(factor=sepa_small) ; s2.separator(factor=sepa_small)

            #vgroup paint

            s1.label(text=translate("Vertex-Group"),)

            ope = s2.row(align=True)
            ope.prop(psy_active,"s_mask_vg_allow", text="", icon="CHECKBOX_HLT" if psy_active.s_mask_vg_allow else "CHECKBOX_DEHLT")
            ope2 = ope.row(align=True)
            ope2.enabled = psy_active.s_mask_vg_allow
            exists = (psy_active.s_mask_vg_ptr!="")
            op = ope2.operator("scatter5.vg_quick_paint",
                text="Paint",
                icon="BRUSH_DATA" if exists else "ADD",
                depress=((bpy.context.mode=="PAINT_WEIGHT") and (getattr(bpy.context.object.vertex_groups.active,"name",'')==psy_active.s_mask_vg_ptr)),
                )
            op.group_name = psy_active.s_mask_vg_ptr
            op.mode = "vg" 
            op.api = f"emitter.scatter5.particle_systems['{psy_active.name}'].s_mask_vg_ptr"

            s1.separator(factor=sepa_small) ; s2.separator(factor=sepa_small)

            #seed 

            s1.label(text="Seed")
            ope = s2.row(align=True)
            op = ope.operator("scatter5.exec_line", text="Randomize", icon_value=cust_icon("W_DICE"),)
            op.api = f"psy_active.s_distribution_is_random_seed = True ; psy_active.get_scatter_mod().node_group.nodes['s_pattern1'].node_tree.nodes['texture'].node_tree.scatter5.texture.mapping_random_is_random_seed = True"

            #scale

            s1.separator(factor=sepa_large) ; s2.separator(factor=sepa_large)

            s1.label(text="Scale")
            s2.prop(psy_active,"s_beginner_default_scale",text="") 

            s1.separator(factor=sepa_small) ; s2.separator(factor=sepa_small)

            s1.label(text="Random")
            s2.prop(psy_active,"s_beginner_random_scale",text="", slider=True,) 

            s1.separator(factor=sepa_small) ; s2.separator(factor=sepa_small)

            s1.label(text=translate("Vertex-Group"),)

            ope = s2.row(align=True)

            op = ope.operator("scatter5.exec_line", text="", icon="CHECKBOX_HLT" if psy_active.s_scale_shrink_allow else "CHECKBOX_DEHLT", depress=psy_active.s_scale_shrink_allow, )
            op.api = f"psy_active.s_scale_shrink_allow = {not psy_active.s_scale_shrink_allow} ; psy_active.s_scale_shrink_mask_method = 'mask_vg' ; psy_active.s_scale_shrink_mask_reverse = True" 
            ope2 = ope.row(align=True)
            ope2.enabled = psy_active.s_scale_shrink_allow
            exists = (psy_active.s_scale_shrink_mask_ptr!="")
            op = ope2.operator("scatter5.vg_quick_paint",
                text="Paint",
                icon="BRUSH_DATA" if exists else "ADD",
                depress=((bpy.context.mode=="PAINT_WEIGHT") and (getattr(bpy.context.object.vertex_groups.active,"name",'')==psy_active.s_scale_shrink_mask_ptr)),
                )
            op.group_name = psy_active.s_scale_shrink_mask_ptr
            op.mode = "vg" 
            op.api = f"emitter.scatter5.particle_systems['{psy_active.name}'].s_scale_shrink_mask_ptr"

            #rotation 

            s1.separator(factor=sepa_large) ; s2.separator(factor=sepa_large)

            s1.label(text="Align")
            ope = s2.row(align=True)
            op = ope.operator("scatter5.exec_line",text="Normal", 
                depress=(psy_active.s_rot_align_z_allow and psy_active.s_rot_align_z_method=='meth_align_z_normal'),)
            op.api = f"psy_active.s_rot_align_z_allow = True ;  psy_active.s_rot_align_z_method ='meth_align_z_normal'"

            op = ope.operator("scatter5.exec_line",text="Local Z",
                depress=(psy_active.s_rot_align_z_allow and psy_active.s_rot_align_z_method=='meth_align_z_local'),)
            op.api = f"psy_active.s_rot_align_z_allow = True ;  psy_active.s_rot_align_z_method ='meth_align_z_local'"

            s1.separator(factor=sepa_small) ; s2.separator(factor=sepa_small)

            s1.label(text="Random")
            s2.prop(psy_active,"s_beginner_random_rot",text="", slider=True,)

            #texture

            s1.separator(factor=sepa_large) ; s2.separator(factor=sepa_large)

            texture_exists = True
            texture_node = psy_active.get_scatter_mod().node_group.nodes["s_pattern1"].node_tree.nodes["texture"]
            texture_props = texture_node.node_tree.scatter5.texture

            if (texture_node.node_tree.name.startswith(".TEXTURE *DEFAULT")):

                s1.label(text="Pattern")
                ope = s2.row(align=True)
                ope.context_pointer_set("pass_ui_arg_system", psy_active,)
                ope.context_pointer_set("pass_ui_arg_texture_node", texture_node,)
                op = ope.operator("scatter5.exec_line", text="New", icon="ADD")
                op.api = "bpy.ops.scatter5.scatter_texture_new(ptr_name='s_pattern1_texture_ptr',new_name='BR-Pattern') ; psy_active.s_pattern1_allow = True"
                op.undo = "Creating New Pattern"

            elif (psy_active.s_pattern1_allow):

                s1.label(text="Pattern")
                ope = s2.row(align=True)
                op = ope.operator("scatter5.exec_line", text="Active", icon="CHECKBOX_HLT", depress=True)
                op.api = f"psy_active.s_pattern1_allow = False"

                s1.separator(factor=sepa_small) ; s2.separator(factor=sepa_small)

                s1.label(text="Scale")
                s2.prop(texture_props, "scale", text="",)

                s1.separator(factor=sepa_small) ; s2.separator(factor=sepa_small)

                s1.label(text="Brightness")
                s2.prop(texture_props, "intensity", text="",)

                s1.separator(factor=sepa_small) ; s2.separator(factor=sepa_small)

                s1.label(text="Contrast")
                s2.prop(texture_props, "contrast", text="",)

                s1.separator(factor=sepa_small) ; s2.separator(factor=sepa_small)

                
            else:

                s1.label(text="Pattern")
                ope = s2.row(align=True)
                op = ope.operator("scatter5.exec_line", text=translate("Inactive"), icon="CHECKBOX_DEHLT", depress=False,)
                op.api = f"psy_active.s_pattern1_allow = True"

            #define instances 

            s1.separator(factor=sepa_large) ; s2.separator(factor=sepa_large)

            s1.label(text=translate("Displays"),)

            ope = s2.row(align=True)
            op = ope.operator("scatter5.exec_line", text=translate("Active") if psy_active.s_display_allow else translate("Inactive"), icon="CHECKBOX_HLT" if psy_active.s_display_allow else "CHECKBOX_DEHLT", depress=psy_active.s_display_allow, )
            op.api = f"psy_active.s_display_allow = {not psy_active.s_display_allow} " 

            s1.separator(factor=sepa_small) ; s2.separator(factor=sepa_small)

            s1.label(text=translate("Instances"),)

            ui_list = s2.column(align=True)
            ui_list.template_list("SCATTER5_UL_list_instances", "", psy_active.s_instances_coll_ptr, "objects", psy_active, "s_instances_list_idx", rows=5, sort_lock=True,)
                
            add = ui_list.column(align=True)
            add.active = (bpy.context.mode=="OBJECT")
            add.operator_menu_enum("scatter5.add_instances", "method", text=translate("Add Instance(s)"), icon="ADD")
        
            #Separator 

            ui_templates.separator_box_in(box)

    return

def draw_removal_interface(self,layout):

    addon_prefs, scat_scene, scat_ui, scat_win, emitter, psy_active, group_active = get_props()

    if (psy_active is None):
        return

    s_abiotic_used    = psy_active.is_category_used("s_abiotic")
    s_ecosystem_used  = psy_active.is_category_used("s_ecosystem")
    s_proximity_used  = psy_active.is_category_used("s_proximity")
    s_push_used       = psy_active.is_category_used("s_push")
    s_wind_used       = psy_active.is_category_used("s_wind")
    s_visibility_used = psy_active.is_category_used("s_visibility")

    if any([s_abiotic_used, s_ecosystem_used, s_proximity_used, s_push_used, s_wind_used, s_visibility_used,]):

        box, is_open = ui_templates.box_panel(self, layout, 
            prop_str = "ui_tweak_removal", #INSTRUCTION:REGISTER:UI:BOOL_NAME("ui_tweak_removal");BOOL_VALUE(1)
            name = translate("Advanced Features"),
            doc_panel = "SCATTER5_PT_docs", 
            popover_argument = "s_beginners_remove", #INSTRUCTION:REGISTER:UI:ARGS_POINTERS("s_beginners_remove")
            )
        if is_open:

            main = box.column()

            row = main.row()
            split = row.split(factor = 0.375)
            s1 = split.column()
            s1.alignment = "RIGHT"
            s2 = split.column()

            s1.separator(factor=sepa_small) ; s2.separator(factor=sepa_small)

            if (s_visibility_used):
                s1.separator(factor=sepa_small) ; s2.separator(factor=sepa_small)

                s1.label(text=translate("Optimizations"),)
                ope = s2.row(align=True)
                op = ope.operator("scatter5.exec_line", text=translate("Remove"), icon="PANEL_CLOSE", depress=False,)
                op.api = f"psy_active.s_visibility_master_allow = False"
                op.undo = translate("Remove Visibility Features")
                op.description = translate("There are more advanced feature enabled for this scatter-system! Would you like to remove it?")

            if (s_abiotic_used):
                s1.separator(factor=sepa_small) ; s2.separator(factor=sepa_small)

                s1.label(text=translate("Abiotic"),)
                ope = s2.row(align=True)
                op = ope.operator("scatter5.exec_line", text=translate("Remove"), icon="PANEL_CLOSE", depress=False,)
                op.api = f"psy_active.s_abiotic_master_allow = False"
                op.undo = translate("Remove Abiotic Features")
                op.description = translate("There are more advanced feature enabled for this scatter-system! Would you like to remove it?")

            if (s_ecosystem_used):
                s1.separator(factor=sepa_small) ; s2.separator(factor=sepa_small)

                s1.label(text=translate("Ecosystem"),)
                ope = s2.row(align=True)
                op = ope.operator("scatter5.exec_line", text=translate("Remove"), icon="PANEL_CLOSE", depress=False,)
                op.api = f"psy_active.s_ecosystem_master_allow = False"
                op.undo = translate("Remove Ecosystem Features")
                op.description = translate("There are more advanced feature enabled for this scatter-system! Would you like to remove it?")

            if (s_proximity_used):
                s1.separator(factor=sepa_small) ; s2.separator(factor=sepa_small)

                s1.label(text=translate("Proximity"),)
                ope = s2.row(align=True)
                op = ope.operator("scatter5.exec_line", text=translate("Remove"), icon="PANEL_CLOSE", depress=False,)
                op.api = f"psy_active.s_proximity_master_allow = False"
                op.undo = translate("Remove Proximity Features")
                op.description = translate("There are more advanced feature enabled for this scatter-system! Would you like to remove it?")

            if (s_push_used):
                s1.separator(factor=sepa_small) ; s2.separator(factor=sepa_small)

                s1.label(text=translate("Offset"),)
                ope = s2.row(align=True)
                op = ope.operator("scatter5.exec_line", text=translate("Remove"), icon="PANEL_CLOSE", depress=False,)
                op.api = f"psy_active.s_push_master_allow = False"
                op.undo = translate("Remove Offset Features")
                op.description = translate("There are more advanced feature enabled for this scatter-system! Would you like to remove it?")
            
            if (s_wind_used):
                s1.separator(factor=sepa_small) ; s2.separator(factor=sepa_small)

                s1.label(text=translate("Wind"),)
                ope = s2.row(align=True)
                op = ope.operator("scatter5.exec_line", text=translate("Remove"), icon="PANEL_CLOSE", depress=False,)
                op.api = f"psy_active.s_wind_master_allow = False"
                op.undo = translate("Remove Wind Features")
                op.description = translate("There are more advanced feature enabled for this scatter-system! Would you like to remove it?")
            
            #Separator 

            ui_templates.separator_box_in(box)

    return

def draw_pros_interface(self,layout):

    addon_prefs, scat_scene, scat_ui, scat_win, emitter, psy_active, group_active = get_props()

    box, is_open = ui_templates.box_panel(self, layout, 
        prop_str = "ui_tweak_pros", #INSTRUCTION:REGISTER:UI:BOOL_NAME("ui_tweak_pros");BOOL_VALUE(1)
        name = translate("Professional Workflow"),
        force_open = True,
        )
    if is_open:

        row = box.row()
        r1 = row.separator(factor=0.3)
        col = row.column()
        r3 = row.separator(factor=0.3)

        word_wrap(layout=col.box(), alignment="CENTER", max_char=38, active=True, string=translate("Get the tools you need to become a pro!\nOur user-friendly interface is perfect for newbies, but our paid tool-kit for professionals is where the magic happens.\n\nWith advanced features, an efficient pipelines, and useful scattering operators, you'll be able to handle the most challenging projects with ease."),)
                
        col.separator(factor=0.75)

        ope = col.row()
        ope.scale_y = 1.2
        ope.operator("wm.url_open", text=translate("Upgrade Today"),).url = "https://blendermarket.com/products/scatter"

        #Separator 

        ui_templates.separator_box_in(box)

    return

def draw_group_beginner_masks(self,layout):

    addon_prefs, scat_scene, scat_ui, scat_win, emitter, psy_active, group_active = get_props()

    box, is_open = ui_templates.box_panel(self, layout, 
        prop_str = "ui_beginners_tweak_group_masks", #INSTRUCTION:REGISTER:UI:BOOL_NAME("ui_beginners_tweak_group_masks");BOOL_VALUE(1)
        name = translate("Group Masks"),
        )
    if is_open:
            
        ui_is_active = True 
        ui_is_active = active_check(group_active, s_category="s_gr_mask", prop=ui_is_active, )
        
        ########## ########## Vgroup

        tocol, is_toggled = ui_templates.bool_toggle(box, 
            prop_api=group_active,
            prop_str="s_gr_mask_vg_allow", 
            label=translate("Vertex-Group"), 
            icon="WPAINT_HLT", 
            active=ui_is_active,
            return_layout=True,
            )
        if is_toggled:

                mask_col = tocol.column(align=True)
                mask_col.separator(factor=0.35)

                exists = (group_active.s_gr_mask_vg_ptr!="")

                #mask pointer

                mask = mask_col.row(align=True)

                ptr = mask.row(align=True)
                ptr.alert = ( bool(group_active.s_gr_mask_vg_ptr) and (group_active.s_gr_mask_vg_ptr not in group_active.get_surfaces_match_attr("vg")(group_active, bpy.context, group_active.s_gr_mask_vg_ptr)) )
                ptr.prop( group_active, f"s_gr_mask_vg_ptr", text="", icon="GROUP_VERTEX",)
                
                if exists:
                    mask.prop( group_active, f"s_gr_mask_vg_revert",text="",icon="ARROW_LEFTRIGHT",)

                #paint or create operator

                op = mask.operator("scatter5.vg_quick_paint",
                    text="",
                    icon="BRUSH_DATA" if exists else "ADD",
                    depress=((bpy.context.mode=="PAINT_WEIGHT") and (getattr(bpy.context.object.vertex_groups.active,"name",'')==group_active.s_gr_mask_vg_ptr)),
                    )
                op.group_name = group_active.s_gr_mask_vg_ptr
                op.mode = "vg" 
                op.api = f"emitter.scatter5.particle_groups['{group_active.name}'].s_gr_mask_vg_ptr"

                tocol.separator(factor=1)

        #Separator 

        ui_templates.separator_box_in(box)
            
    return 


#    .oooooo.   oooo
#   d8P'  `Y8b  `888
#  888           888   .oooo.    .oooo.o  .oooo.o  .ooooo.   .oooo.o
#  888           888  `P  )88b  d88(  "8 d88(  "8 d88' `88b d88(  "8
#  888           888   .oP"888  `"Y88b.  `"Y88b.  888ooo888 `"Y88b.
#  `88b    ooo   888  d8(  888  o.  )88b o.  )88b 888    .o o.  )88b
#   `Y8bood8P'  o888o `Y888""8o 8""888P' 8""888P' `Y8bod8P' 8""888P'


class SCATTER5_PT_tweaking(bpy.types.Panel):

    bl_idname      = "SCATTER5_PT_tweaking"
    bl_label       = translate("Tweak")
    bl_category    = "USER_DEFINED" #will be replaced right before ui.__ini__.register()
    bl_space_type  = "VIEW_3D"
    bl_region_type = "UI"
    bl_context     = "" #nothing == enabled everywhere
    bl_order       = 3

    @classmethod
    def poll(cls, context,):
        if context.scene.scatter5.emitter is None:
            return False
        if context.mode not in ("OBJECT","PAINT_WEIGHT","PAINT_VERTEX","PAINT_TEXTURE","EDIT_MESH"):
            return False
        return True 
        
    def draw_header(self, context):
        self.layout.label(text="", icon_value=cust_icon("W_BIOME"),)

    def draw_header_preset(self, context):
        emitter_header(self)

    def draw(self, context):
        layout = self.layout
        draw_tweaking_panel(self,layout)

classes = (
        
    SCATTER5_UL_list_instances,
    SCATTER5_PT_tweaking,

    )

#if __name__ == "__main__":
#    register()