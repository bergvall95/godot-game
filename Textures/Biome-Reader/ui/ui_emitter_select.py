
#####################################################################################################
#
# oooooooooooo                    o8o      .       .                           ooooooooo.                                   oooo
# `888'     `8                    `"'    .o8     .o8                           `888   `Y88.                                 `888
#  888         ooo. .oo.  .oo.   oooo  .o888oo .o888oo  .ooooo.  oooo d8b       888   .d88'  .oooo.   ooo. .oo.    .ooooo.   888
#  888oooo8    `888P"Y88bP"Y88b  `888    888     888   d88' `88b `888""8P       888ooo88P'  `P  )88b  `888P"Y88b  d88' `88b  888
#  888    "     888   888   888   888    888     888   888ooo888  888           888          .oP"888   888   888  888ooo888  888
#  888       o  888   888   888   888    888 .   888 . 888    .o  888           888         d8(  888   888   888  888    .o  888
# o888ooooood8 o888o o888o o888o o888o   "888"   "888" `Y8bod8P' d888b         o888o        `Y888""8o o888o o888o `Y8bod8P' o888o
#
#####################################################################################################


import bpy

from .. resources.icons import cust_icon
from .. resources.translate import translate

from .. utils.str_utils import word_wrap 

from . import ui_templates


# ooooo   ooooo                           .o8
# `888'   `888'                          "888
#  888     888   .ooooo.   .oooo.    .oooo888   .ooooo.  oooo d8b
#  888ooooo888  d88' `88b `P  )88b  d88' `888  d88' `88b `888""8P
#  888     888  888ooo888  .oP"888  888   888  888ooo888  888
#  888     888  888    .o d8(  888  888   888  888    .o  888
# o888o   o888o `Y8bod8P' `Y888""8o `Y8bod88P" `Y8bod8P' d888b


def emitter_header(self):
    """draw main panels header"""

    addon_prefs = bpy.context.preferences.addons["Biome-Reader"].preferences
    scat_scene  = bpy.context.scene.scatter5
    emitter     = scat_scene.emitter
    layout      = self.layout
    mode        = bpy.context.mode

    row = layout.row(align=False)
    row.alignment = "RIGHT"
    row.prop(scat_scene, "emitter", text="",)
    
    return None


class SCATTER5_MT_emitter_dropdown_menu(bpy.types.Menu):

    bl_idname = "SCATTER5_MT_emitter_dropdown_menu"
    bl_label  = ""
    bl_description = ""

    def draw(self, context):
        layout=self.layout

        emitter = bpy.context.scene.scatter5.emitter
        emitters = bpy.context.scene.scatter5.get_all_emitters()

        for e in emitters:
            icon = cust_icon("W_EMITTER" if e is emitter else "W_EMITTER_EMPTY")
            row = layout.row()
            row.enabled = (e is not emitter)
            row.operator("scatter5.set_new_emitter",text=f"Use '{e.name}'", icon_value=icon,).obj_name = e.name
            continue

        layout.separator()

        if (bpy.context.object is not None):
            row = layout.row()
            row.active = bpy.context.object is not emitter
            ope = row.operator("scatter5.set_new_emitter", text=f"Use '{bpy.context.object.name}'", icon="RESTRICT_SELECT_OFF",)
            ope.obj_name = bpy.context.object.name

        layout.operator("scatter5.new_nonlinear_emitter", text=translate("New Empty Emitter"), icon="RNA_ADD",)
        layout.operator("scatter5.exec_line", text=translate("Back to Emitter Panel"), icon="LOOP_BACK",).api = "scat_scene.emitter = None"
        
        return None


# ooo        ooooo            o8o                   ooooooooo.                                   oooo
# `88.       .888'            `"'                   `888   `Y88.                                 `888
#  888b     d'888   .oooo.   oooo  ooo. .oo.         888   .d88'  .oooo.   ooo. .oo.    .ooooo.   888
#  8 Y88. .P  888  `P  )88b  `888  `888P"Y88b        888ooo88P'  `P  )88b  `888P"Y88b  d88' `88b  888
#  8  `888'   888   .oP"888   888   888   888        888          .oP"888   888   888  888ooo888  888
#  8    Y     888  d8(  888   888   888   888        888         d8(  888   888   888  888    .o  888
# o8o        o888o `Y888""8o o888o o888o o888o      o888o        `Y888""8o o888o o888o `Y8bod8P' o888o


def draw_emit_panel(self,layout):

    scat_scene = bpy.context.scene.scatter5
    emitters = scat_scene.get_all_emitters()
    has_emitters = bool(len(emitters)!=0)
        
    main = layout.column()
    main.enabled = scat_scene.ui_enabled

    ui_templates.separator_box_out(main)
    ui_templates.separator_box_out(main)

    if (not has_emitters):
        draw_info(self,main)
        ui_templates.separator_box_out(main)

    if (has_emitters):
        draw_swap(self,main)
        ui_templates.separator_box_out(main)
        
    
    main.separator(factor=50)
    
    return None 


# ooooo              .o88o.
# `888'              888 `"
#  888  ooo. .oo.   o888oo   .ooooo.
#  888  `888P"Y88b   888    d88' `88b
#  888   888   888   888    888   888
#  888   888   888   888    888   888
# o888o o888o o888o o888o   `Y8bod8P'


def draw_info(self,layout):

    box, is_open = ui_templates.box_panel(self, layout, 
        prop_str = "ui_emit_info", #INSTRUCTION:REGISTER:UI:BOOL_NAME("ui_emit_info");BOOL_VALUE(1)
        icon = "HELP", 
        name = translate("Information"),
        )
    if is_open:
            
            col = box.column()

            word_wrap( string=translate("Choose an emitter-object!\nEmitters is where scatter-system(s) settings will be stored.\nYou can swap emitters at any moment on our plugin headers."), layout=col, max_char=33, alignment="CENTER", active=True, icon="INFO")

            ui_templates.separator_box_in(box)

    return None 

# ooooo      ooo                       oooo   o8o                                                ooooo      ooo
# `888b.     `8'                       `888   `"'                                                `888b.     `8'
#  8 `88b.    8   .ooooo.  ooo. .oo.    888  oooo  ooo. .oo.    .ooooo.   .oooo.   oooo d8b       8 `88b.    8   .ooooo.  oooo oooo    ooo
#  8   `88b.  8  d88' `88b `888P"Y88b   888  `888  `888P"Y88b  d88' `88b `P  )88b  `888""8P       8   `88b.  8  d88' `88b  `88. `88.  .8'
#  8     `88b.8  888   888  888   888   888   888   888   888  888ooo888  .oP"888   888           8     `88b.8  888ooo888   `88..]88..8'
#  8       `888  888   888  888   888   888   888   888   888  888    .o d8(  888   888           8       `888  888    .o    `888'`888'
# o8o        `8  `Y8bod8P' o888o o888o o888o o888o o888o o888o `Y8bod8P' `Y888""8o d888b         o8o        `8  `Y8bod8P'     `8'  `8'

 
#"scatter5.new_nonlinear_emitter"

def draw_nonlinear_new(self,layout):

    box, is_open = ui_templates.box_panel(self, layout, 
        prop_str = "ui_emit_nonlinear_new", #INSTRUCTION:REGISTER:UI:BOOL_NAME("ui_emit_nonlinear_new");BOOL_VALUE(0)
        icon = "RNA_ADD", 
        name = translate("Dummy Emitter"),
        )
    if is_open:

            row = box.row()
            row.separator(factor=0.3)
            col = row.column()
            row.separator(factor=0.3)

            #button add new 

            button = col.row(align=True)
            button.scale_y=1.2
            button.operator("scatter5.new_nonlinear_emitter",text=translate("Create Dummy Emitter"), icon="RNA_ADD",)

            ui_templates.separator_box_in(box)

    return None 

#  .oooooo..o
# d8P'    `Y8
# Y88bo.      oooo oooo    ooo  .oooo.   oo.ooooo.
#  `"Y8888o.   `88. `88.  .8'  `P  )88b   888' `88b
#      `"Y88b   `88..]88..8'    .oP"888   888   888
# oo     .d8P    `888'`888'    d8(  888   888   888
# 8""88888P'      `8'  `8'     `Y888""8o  888bod8P'
#                                         888
#                                        o888o
 
def draw_swap(self,layout):

    box, is_open = ui_templates.box_panel(self, layout, 
        prop_str = "ui_emit_swap", #INSTRUCTION:REGISTER:UI:BOOL_NAME("ui_emit_swap");BOOL_VALUE(1)
        icon = "W_EMITTER", 
        name = translate("Emitters In Use"),
        )
    if is_open:

            row = box.row()
            row.separator(factor=0.3)
            element_box = row.box()
            row.separator(factor=0.3)

            #emitter select box 

            for e in bpy.context.scene.scatter5.get_all_emitters():
            
                element = element_box.row(align=True)
                element.scale_y = 0.8

                sub = element.row(align=True)
                sub.alignment = "LEFT"
                op = sub.operator("scatter5.set_new_emitter",text=e.name, emboss=False, icon_value=cust_icon("W_EMITTER"),)
                op.obj_name = e.name
                op.select = True

                #thanks blender aligmnet system
                sub = element.row(align=True)
                
                continue

            ui_templates.separator_box_in(box)

    return None 

# ooooooooo.                                                  oooo
# `888   `Y88.                                                `888
#  888   .d88'  .ooooo.  ooo. .oo.  .oo.    .ooooo.   .oooo.o  888 .oo.
#  888ooo88P'  d88' `88b `888P"Y88bP"Y88b  d88' `88b d88(  "8  888P"Y88b
#  888`88b.    888ooo888  888   888   888  888ooo888 `"Y88b.   888   888
#  888  `88b.  888    .o  888   888   888  888    .o o.  )88b  888   888
# o888o  o888o `Y8bod8P' o888o o888o o888o `Y8bod8P' 8""888P' o888o o888o


def draw_remesh(self,layout):

    box, is_open = ui_templates.box_panel(self, layout, 
        prop_str = "ui_emit_remesh", #INSTRUCTION:REGISTER:UI:BOOL_NAME("ui_emit_remesh");BOOL_VALUE(0)
        icon = "MOD_REMESH", 
        name = translate("Utility Remesh"),
        )
    if is_open:

            row = box.row()
            row.separator(factor=0.3)
            col = row.column()
            row.separator(factor=0.3)
       
            button = col.row(align=True)
            button.scale_y=1.2
            button.enabled = bpy.context.object.type=="MESH"
            op = button.operator("scatter5.grid_bisect", text=translate("Grid Bisect Selection"), icon="MOD_REMESH",)
            op.obj_list = "_!#!_".join([o.name for o in bpy.context.selected_objects if (o.type=="MESH")])

            ui_templates.separator_box_in(box)

    return None 


#    .oooooo.   oooo
#   d8P'  `Y8b  `888
#  888           888   .oooo.    .oooo.o  .oooo.o  .ooooo.   .oooo.o
#  888           888  `P  )88b  d88(  "8 d88(  "8 d88' `88b d88(  "8
#  888           888   .oP"888  `"Y88b.  `"Y88b.  888ooo888 `"Y88b.
#  `88b    ooo   888  d8(  888  o.  )88b o.  )88b 888    .o o.  )88b
#   `Y8bood8P'  o888o `Y888""8o 8""888P' 8""888P' `Y8bod8P' 8""888P'


class SCATTER5_PT_choose_emitter(bpy.types.Panel):

    bl_idname      = "SCATTER5_PT_choose_emitter"
    bl_label       = translate("Emitter")
    bl_category    = "USER_DEFINED" #will be replaced right before ui.__ini__.register()
    bl_space_type  = "VIEW_3D"
    bl_region_type = "UI"
    bl_context     = ""
    bl_order       = 0

    @classmethod
    def poll(cls, context,):
        if (context.mode not in ("OBJECT","PAINT_WEIGHT","PAINT_VERTEX","PAINT_TEXTURE","EDIT_MESH")):
            return False
        if (context.scene.scatter5.emitter is not None):
            return False
        return True 

    def draw_header(self, context):

        self.layout.label(text="", icon_value=cust_icon("W_BIOME"),)

    def draw_header_preset(self, context):

        layout = self.layout
        row = layout.row()
        row.scale_x = 0.85
        row.prop(bpy.context.scene.scatter5,"emitter",text="",icon_value=cust_icon("W_EMITTER"),)

    def draw(self, context):

        layout = self.layout
        draw_emit_panel(self,layout)


classes = (

    SCATTER5_PT_choose_emitter,
    SCATTER5_MT_emitter_dropdown_menu,
    
    )

#if __name__ == "__main__":
#    register()

