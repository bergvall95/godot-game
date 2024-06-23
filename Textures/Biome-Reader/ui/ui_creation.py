
#####################################################################################################
#
# ooooo     ooo ooooo        .oooooo.                                    .    o8o
# `888'     `8' `888'       d8P'  `Y8b                                 .o8    `"'
#  888       8   888       888          oooo d8b  .ooooo.   .oooo.   .o888oo oooo   .ooooo.  ooo. .oo.
#  888       8   888       888          `888""8P d88' `88b `P  )88b    888   `888  d88' `88b `888P"Y88b
#  888       8   888       888           888     888ooo888  .oP"888    888    888  888   888  888   888
#  `88.    .8'   888       `88b    ooo   888     888    .o d8(  888    888 .  888  888   888  888   888
#    `YbodP'    o888o       `Y8bood8P'  d888b    `Y8bod8P' `Y888""8o   "888" o888o `Y8bod8P' o888o o888o
#
#####################################################################################################


import bpy, os

from .. resources.icons import cust_icon
from .. resources.translate import translate
from .. resources import directories

from .. scattering.instances import find_compatible_instances
from .. scattering.emitter import is_ready_for_scattering

from .. utils.str_utils import word_wrap, smart_round
from .. utils.vg_utils import is_vg_active

from . import ui_templates
from . ui_emitter_select import emitter_header


def get_props():
    """get useful props used in interface"""

    addon_prefs = bpy.context.preferences.addons["Biome-Reader"].preferences
    scat_win    = bpy.context.window_manager.scatter5
    scat_ui     = scat_win.ui
    scat_scene  = bpy.context.scene.scatter5
    emitter     = scat_scene.emitter

    return (addon_prefs, scat_scene, scat_ui, scat_win, emitter)

def layout_spacing(layout):
    row = layout.row(align=True)

    left = row.column(align=True)
    left.scale_x = 0.8
    left.operator("scatter5.dummy",text="",icon="BLANK1", emboss=False,)
    center = row.column()
    right = row.column(align=True)
    right.scale_x = 0.8
    right.operator("scatter5.dummy",text="",icon="BLANK1", emboss=False,)

    return left, center, right


# ooo        ooooo            o8o                   ooooooooo.                                   oooo
# `88.       .888'            `"'                   `888   `Y88.                                 `888
#  888b     d'888   .oooo.   oooo  ooo. .oo.         888   .d88'  .oooo.   ooo. .oo.    .ooooo.   888
#  8 Y88. .P  888  `P  )88b  `888  `888P"Y88b        888ooo88P'  `P  )88b  `888P"Y88b  d88' `88b  888
#  8  `888'   888   .oP"888   888   888   888        888          .oP"888   888   888  888ooo888  888
#  8    Y     888  d8(  888   888   888   888        888         d8(  888   888   888  888    .o  888
# o8o        o888o `Y888""8o o888o o888o o888o      o888o        `Y888""8o o888o o888o `Y8bod8P' o888o



def draw_creation_panel(self,layout):
    """draw main creation panel"""

    addon_prefs, scat_scene, scat_ui, scat_win, emitter = get_props()

    main = layout.column()
    main.enabled = scat_scene.ui_enabled

    ui_templates.separator_box_out(main)
    ui_templates.separator_box_out(main)

    draw_density_scatter(self,main)
    ui_templates.separator_box_out(main)


    draw_biomes_scatter(self,main)
    ui_templates.separator_box_out(main)
        
    ui_templates.separator_box_out(main)
    ui_templates.separator_box_out(main)

    return



# oooooooooo.                                   o8o      .                     .oooooo..o                         .       .
# `888'   `Y8b                                  `"'    .o8                    d8P'    `Y8                       .o8     .o8
#  888      888  .ooooo.  ooo. .oo.    .oooo.o oooo  .o888oo oooo    ooo      Y88bo.       .ooooo.   .oooo.   .o888oo .o888oo  .ooooo.  oooo d8b
#  888      888 d88' `88b `888P"Y88b  d88(  "8 `888    888    `88.  .8'        `"Y8888o.  d88' `"Y8 `P  )88b    888     888   d88' `88b `888""8P
#  888      888 888ooo888  888   888  `"Y88b.   888    888     `88..8'             `"Y88b 888        .oP"888    888     888   888ooo888  888
#  888     d88' 888    .o  888   888  o.  )88b  888    888 .    `888'         oo     .d8P 888   .o8 d8(  888    888 .   888 . 888    .o  888
# o888bood8P'   `Y8bod8P' o888o o888o 8""888P' o888o   "888"     .8'          8""88888P'  `Y8bod8P' `Y888""8o   "888"   "888" `Y8bod8P' d888b
#                                                            .o..P'
#                                                            `Y8P'


def draw_density_scatter(self,layout):

    addon_prefs, scat_scene, scat_ui, scat_win, emitter = get_props()
    scat_op_crea = scat_scene.operators.create_operators
    scat_op = scat_scene.operators.add_psy_density
    
    box, is_open = ui_templates.box_panel(self, layout, 
        prop_str = "ui_create_densit", #INSTRUCTION:REGISTER:UI:BOOL_NAME("ui_create_densit");BOOL_VALUE(1)
        icon = "STICKY_UVS_DISABLE", 
        name = translate("Density Scatter"),
        popover_argument = "ui_create_densit", #INSTRUCTION:REGISTER:UI:ARGS_POINTERS("ui_create_densit")
        )
    if is_open:

            # layout spacing 
            left, area, right = layout_spacing(box)

            under_area = area.column()

            #Density Value 
            dens = under_area.row(align=True)
            dens.scale_y = 0.95
            densp = dens.row(align=True)
            densp.prop(scat_op, "f_distribution_density",)
            densp = dens.row(align=True)
            densp.scale_x = 0.63
            densp.prop(scat_op, "f_density_scale", text="")
            density_scale = scat_op.f_density_scale

            under_area.separator(factor=0.5)

            # Estimation, also see etimation function in add_psy
            density_value = scat_op.f_distribution_density

            #estimate surface area
            square_area = 0
            for s in scat_op_crea.get_f_surfaces():
                surface_area = s.scatter5.estimated_square_area
                square_area += surface_area
                continue

            estim = under_area.column()
            estim.active = False
            estim.scale_y = 0.75
            
            if (emitter.scatter5.estimated_square_area==-1):

                op = estim.operator("scatter5.exec_line",text=translate("Refresh Estimation"), icon="FILE_REFRESH", emboss=False,)
                op.api = "bpy.context.scene.scatter5.emitter.scatter5.estimate_square_area()"
                op.description = translate("Recalculate Emitter Surface m² Estimation")
             
            else:

                #adjust density from scale
                
                if   (density_scale=="cm"): ajusted_density=density_value*10_000
                elif (density_scale=="ha"): ajusted_density=density_value*0.0001
                elif (density_scale=="km"): ajusted_density=density_value*0.000001
                else:                       ajusted_density=density_value*1

                #find use case for chosen density

                if   ajusted_density==0:      use_case = translate("Empty")
                elif ajusted_density<0.00001: use_case = translate("Mountains")
                elif ajusted_density<0.001:   use_case = translate("Buildings")
                elif ajusted_density<0.1:     use_case = translate("Forest")
                elif ajusted_density<1.0:     use_case = translate("Bushes")
                elif ajusted_density<5.0:     use_case = translate("Plants")
                elif ajusted_density<30:      use_case = translate("Grass-Patches")
                elif ajusted_density<60:      use_case = translate("Dead-Leaves")
                elif ajusted_density<100:     use_case = translate("Grass-Blades")
                elif ajusted_density<1_000:   use_case = translate("Hair Clumps")
                elif ajusted_density<10_000:  use_case = translate("Donut Sprinkles")
                elif ajusted_density<100_000: use_case = translate("Single Hair")
                else:                         use_case = translate("Microscopic")

                nfo = estim.row(); left = nfo.row() ; left.scale_x=1.0 ; left.alignment="LEFT" ; right = nfo.row() ; right.alignment="RIGHT" 
                left.label(text=translate("Use-Case")+":")
                right.label(text=use_case)


                #adjust surface display from chosen unit

                if   (density_scale=="m"):  display_square_area = f"{smart_round(square_area)} m²"
                elif (density_scale=="cm"): display_square_area = f"{smart_round(square_area*10_000):,} cm²"
                elif (density_scale=="ha"): display_square_area = f"{smart_round(square_area*0.0001)} ha"
                elif (density_scale=="km"): display_square_area = f"{smart_round(square_area*0.000001)} km²"

                #Surface

                nfo = estim.row(); left = nfo.row() ; left.scale_x=1.0 ; left.alignment="LEFT" ; right = nfo.row() ; right.alignment="RIGHT" 
                left.label(text=translate("Surface(s) Area")+":")
                if (square_area<0):
                    op = right.operator("scatter5.exec_line", text="", icon="FILE_REFRESH", emboss=False,)
                    op.api = "[ s.scatter5.estimate_square_area() for s in scat_scene.operators.create_operators.get_f_surfaces()]"
                    op.description = translate("Recalculate surface(s) m² estimation, note that you can enter edit mode to automatically refresh m² estimation")
                else:
                    right.label(text=display_square_area,)

                #density in m², true density always in m²

                nfo = estim.row(); left = nfo.row() ; left.scale_x=1.0 ; left.alignment="LEFT" ; right = nfo.row() ; right.alignment="RIGHT" 
                left.label(text=translate("Scatter Density")+":")
                right.label(text=f"{round(density_value,3):,} /{density_scale}{'²' if density_scale!='ha' else''}")

                #particle-Count

                future_count = int(square_area*ajusted_density)
                nfo = estim.row(); left = nfo.row() ; left.scale_x=1.0 ; left.alignment="LEFT" ; right = nfo.row() ; right.alignment="RIGHT" 
                right.alert = (future_count>199_000)
                left.label(text=translate("Estimated Instances")+":")
                right.label(text=f"{future_count:,}")


            under_area.separator(factor=0.5)

            #Selection mode

            under_area.prop(scat_op, "selection_mode", text="",)

            under_area.separator()

            button_row = under_area.row()
            button_row.scale_y = 1.25

            button = button_row.row(align=True)
            button.enabled = is_ready_for_scattering()
            
            operator_text = translate("Scatter Object(s)") if (scat_op.selection_mode=="viewport") else translate("Scatter Asset(s)")
            op = button.operator("scatter5.add_psy_density", text=operator_text,)
            op.emitter_name = emitter.name
            op.surfaces_names = "_!#!_".join( o.name for o in scat_op_crea.get_f_surfaces() )
            op.instances_names = "_!#!_".join( o.name for o in bpy.context.selected_objects )
            op.selection_mode = scat_op.selection_mode
            op.psy_color_random = True 
            op.density_value = density_value
            op.density_scale = density_scale

            button_settings = button_row.row(align=True)
            button_settings.scale_x = 0.9
            button_settings.emboss = "NONE"
            button_settings.popover(panel="SCATTER5_PT_creation_operator_add_psy_density",text="", icon="OPTIONS",)

            ui_templates.separator_box_in(box)

    return 


# ooooooooo.                                             .         .oooooo..o                         .       .
# `888   `Y88.                                         .o8        d8P'    `Y8                       .o8     .o8
#  888   .d88' oooo d8b  .ooooo.   .oooo.o  .ooooo.  .o888oo      Y88bo.       .ooooo.   .oooo.   .o888oo .o888oo  .ooooo.  oooo d8b
#  888ooo88P'  `888""8P d88' `88b d88(  "8 d88' `88b   888         `"Y8888o.  d88' `"Y8 `P  )88b    888     888   d88' `88b `888""8P
#  888          888     888ooo888 `"Y88b.  888ooo888   888             `"Y88b 888        .oP"888    888     888   888ooo888  888
#  888          888     888    .o o.  )88b 888    .o   888 .      oo     .d8P 888   .o8 d8(  888    888 .   888 . 888    .o  888
# o888o        d888b    `Y8bod8P' 8""888P' `Y8bod8P'   "888"      8""88888P'  `Y8bod8P' `Y888""8o   "888"   "888" `Y8bod8P' d888b



def find_preset_name(compatible_instances):
    """find particle system name depending on instances and options"""

    scat_op = bpy.context.scene.scatter5.operators.add_psy_preset

    #auto color? 
    if (not scat_op.preset_find_name):
        return scat_op.preset_name

    for o in compatible_instances:
        return o.name

    return translate("No Object Found")


def find_preset_color(compatible_instances):
    """find particle system color depending on instances and options"""

    scat_op = bpy.context.scene.scatter5.operators.add_psy_preset

    #auto color? 
    if (not scat_op.preset_find_color):
        return  list(scat_op.preset_color)[:3]

    for o in compatible_instances:
        if (len(o.material_slots)!=0):
            for slot in o.material_slots:
                if (slot.material is not None):
                    return list(slot.material.diffuse_color)[:3]

    return list(scat_op.preset_color)[:3]



# oooooooooo.   o8o                                              .oooooo..o                         .       .
# `888'   `Y8b  `"'                                             d8P'    `Y8                       .o8     .o8
#  888     888 oooo   .ooooo.  ooo. .oo.  .oo.    .ooooo.       Y88bo.       .ooooo.   .oooo.   .o888oo .o888oo  .ooooo.  oooo d8b
#  888oooo888' `888  d88' `88b `888P"Y88bP"Y88b  d88' `88b       `"Y8888o.  d88' `"Y8 `P  )88b    888     888   d88' `88b `888""8P
#  888    `88b  888  888   888  888   888   888  888ooo888           `"Y88b 888        .oP"888    888     888   888ooo888  888
#  888    .88P  888  888   888  888   888   888  888    .o      oo     .d8P 888   .o8 d8(  888    888 .   888 . 888    .o  888
# o888bood8P'  o888o `Y8bod8P' o888o o888o o888o `Y8bod8P'      8""88888P'  `Y8bod8P' `Y888""8o   "888"   "888" `Y8bod8P' d888b



def draw_biomes_scatter(self,layout):
    
    addon_prefs, scat_scene, scat_ui, scat_win, emitter = get_props()
    scat_op_crea = scat_scene.operators.create_operators
    scat_op = scat_scene.operators.load_biome

    box, is_open = ui_templates.box_panel(self, layout, 
        prop_str = "ui_create_biomes", #INSTRUCTION:REGISTER:UI:BOOL_NAME("ui_create_biomes");BOOL_VALUE(1)
        icon = "ASSET_MANAGER", 
        name = translate("Biome Scatter"),
        popover_argument = "ui_create_biomes", #INSTRUCTION:REGISTER:UI:ARGS_POINTERS("ui_create_biomes")
        )
    if is_open:

            # layout spacing 
            left, area, right = layout_spacing(box)

            button_row = area.row()
            button_row.scale_y = 1.25

            from .. __init__ import bl_info
            plugin_name = bl_info["name"]

            button = button_row.row(align=True)
            op = button.operator("scatter5.open_editor", text=translate("Open Biomes"),)
            op.instructions = f"scat_win.category_manager='library'; bpy.context.preferences.active_section='ADDONS'; wm.addon_support=set(('COMMUNITY',)); wm.addon_search='{plugin_name}'; bpy.ops.scatter5.impost_addonprefs(state=True)"
            op.editor_type = "PREFERENCES"
            op.description = translate("Call the biome manager interface, this interface will temporarily hijack the preferences editor.")

            button_settings = button_row.row(align=True)
            button_settings.scale_x = 0.9
            button_settings.emboss = "NONE"
            button_settings.popover(panel="SCATTER5_PT_creation_operator_load_biome",text="", icon="OPTIONS",)

            ui_templates.separator_box_in(box)

    return 


#    .oooooo.   oooo
#   d8P'  `Y8b  `888
#  888           888   .oooo.    .oooo.o  .oooo.o  .ooooo.   .oooo.o
#  888           888  `P  )88b  d88(  "8 d88(  "8 d88' `88b d88(  "8
#  888           888   .oP"888  `"Y88b.  `"Y88b.  888ooo888 `"Y88b.
#  `88b    ooo   888  d8(  888  o.  )88b o.  )88b 888    .o o.  )88b
#   `Y8bood8P'  o888o `Y888""8o 8""888P' 8""888P' `Y8bod8P' 8""888P'



class SCATTER5_PT_creation(bpy.types.Panel):

    bl_idname      = "SCATTER5_PT_creation"
    bl_label       = translate("Create")
    bl_category    = "USER_DEFINED" #will be replaced right before ui.__ini__.register()
    bl_space_type  = "VIEW_3D"
    bl_region_type = "UI"
    bl_context     = ""
    bl_order       = 2

    @classmethod
    def poll(cls, context,):
        if (context.scene.scatter5.emitter is None):
            return False
        if (context.mode not in ("OBJECT","PAINT_WEIGHT","PAINT_VERTEX","PAINT_TEXTURE","EDIT_MESH")):
            return False
        return True 

    def draw_header(self, context):
        self.layout.label(text="", icon_value=cust_icon("W_BIOME"),)

    def draw_header_preset(self, context):
        emitter_header(self)

    def draw(self, context):
        layout = self.layout
        
        draw_creation_panel(self,layout)

        return None

classes = (

    SCATTER5_PT_creation,

    )

#if __name__ == "__main__":
#    register()

