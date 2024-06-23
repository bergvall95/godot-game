
#####################################################################################################
#
# ooooo     ooo ooooo      oooooooooooo                 .
# `888'     `8' `888'      `888'     `8               .o8
#  888       8   888        888         oooo    ooo .o888oo oooo d8b  .oooo.
#  888       8   888        888oooo8     `88b..8P'    888   `888""8P `P  )88b
#  888       8   888        888    "       Y888'      888    888      .oP"888
#  `88.    .8'   888        888       o  .o8"'88b     888 .  888     d8(  888
#    `YbodP'    o888o      o888ooooood8 o88'   888o   "888" d888b    `Y888""8o
#
#####################################################################################################


import bpy

from .. resources.icons import cust_icon
from .. resources.translate import translate

from . import ui_templates
from . ui_emitter_select import emitter_header

from .. utils.str_utils import word_wrap
from .. utils.vg_utils import is_vg_active

from .. utils.extra_utils import is_rendered_view


# ooo        ooooo            o8o                   ooooooooo.                                   oooo
# `88.       .888'            `"'                   `888   `Y88.                                 `888
#  888b     d'888   .oooo.   oooo  ooo. .oo.         888   .d88'  .oooo.   ooo. .oo.    .ooooo.   888
#  8 Y88. .P  888  `P  )88b  `888  `888P"Y88b        888ooo88P'  `P  )88b  `888P"Y88b  d88' `88b  888
#  8  `888'   888   .oP"888   888   888   888        888          .oP"888   888   888  888ooo888  888
#  8    Y     888  d8(  888   888   888   888        888         d8(  888   888   888  888    .o  888
# o8o        o888o `Y888""8o o888o o888o o888o      o888o        `Y888""8o o888o o888o `Y8bod8P' o888o


def draw_extra_panel(self,layout):

    scat_scene = bpy.context.scene.scatter5
        
    main = layout.column()
    main.enabled = scat_scene.ui_enabled

    ui_templates.separator_box_out(main)
    ui_templates.separator_box_out(main)


    draw_social(self,main)
    ui_templates.separator_box_out(main)
            
    main.separator(factor=50)
    
    return None 



#  .oooooo..o                      o8o            oooo
# d8P'    `Y8                      `"'            `888
# Y88bo.       .ooooo.   .ooooo.  oooo   .oooo.    888
#  `"Y8888o.  d88' `88b d88' `"Y8 `888  `P  )88b   888
#      `"Y88b 888   888 888        888   .oP"888   888
# oo     .d8P 888   888 888   .o8  888  d8(  888   888
# 8""88888P'  `Y8bod8P' `Y8bod8P' o888o `Y888""8o o888o



def draw_social(self,layout): #TODO update links
    """draw manual sub panel"""

    col = layout.column(align=True)
    box, is_open = ui_templates.box_panel(self, col, 
        prop_str = "ui_extra_links", #INSTRUCTION:REGISTER:UI:BOOL_NAME("ui_extra_links");BOOL_VALUE(1)
        icon = "HELP", 
        name = translate("Help and Links"), 
        )
    if is_open:

            row  = box.row()
            row1 = row.row() ; row1.scale_x = 0.17
            row2 = row.row()
            row3 = row.row() ; row3.scale_x = 0.17
            col = row2.column()

            #title
            txt=col.row(align=True)
            txt.label(text=translate("Official Websites")+":",)

            exp = col.row()
            exp.scale_y = 1.2
            exp.operator("wm.url_open", text=translate("Official Website"),).url = "https://www.geoscatter.com/"

            col.separator()

            exp = col.row()
            exp.scale_y = 1.2
            exp.operator("wm.url_open", text=translate("Discover The Biomes"),).url = "https://www.geoscatter.com/biomes.html"


            col.separator()

            #title
            txt=col.row(align=True)
            txt.label(text=translate("Social Media")+":",)

            exp = col.row()
            exp.scale_y = 1.2
            exp.operator("wm.url_open", text=translate("Youtube"),).url = "https://www.youtube.com/channel/UCdtlx635Lq69YvDkBsu-Kdg"

            col.separator()

            exp = col.row()
            exp.scale_y = 1.2
            exp.operator("wm.url_open", text=translate("Twitter"),).url = "https://twitter.com/geoscatter/"

            col.separator()

            exp = col.row()
            exp.scale_y = 1.2
            exp.operator("wm.url_open", text=translate("Instagram"),).url = "https://www.instagram.com/geoscatter"

            col.separator()

            #title
            txt=col.row(align=True)
            txt.label(text=translate("Customer Service")+":",)

            exp = col.row()
            exp.scale_y = 1.2
            exp.operator("wm.url_open", text=translate("Discord Community"),).url = "https://discord.com/invite/F7ZyjP6VKB"


            ui_templates.separator_box_in(box)

    return None


#    .oooooo.   oooo
#   d8P'  `Y8b  `888
#  888           888   .oooo.    .oooo.o  .oooo.o  .ooooo.   .oooo.o
#  888           888  `P  )88b  d88(  "8 d88(  "8 d88' `88b d88(  "8
#  888           888   .oP"888  `"Y88b.  `"Y88b.  888ooo888 `"Y88b.
#  `88b    ooo   888  d8(  888  o.  )88b o.  )88b 888    .o o.  )88b
#   `Y8bood8P'  o888o `Y888""8o 8""888P' 8""888P' `Y8bod8P' 8""888P'



class SCATTER5_PT_extra(bpy.types.Panel):

    bl_idname      = "SCATTER5_PT_extra"
    bl_label       = translate("Extra")
    bl_category    = "USER_DEFINED" #will be replaced right before ui.__ini__.register()
    bl_space_type  = "VIEW_3D"
    bl_region_type = "UI"
    bl_context     = ""
    bl_order       = 4

    @classmethod
    def poll(cls, context,):
        if (context.scene.scatter5.emitter is None):
            return False
        if (context.mode not in ("OBJECT","PAINT_WEIGHT","PAINT_VERTEX","PAINT_TEXTURE","EDIT_MESH")):
            return False
        return True 
      
    def draw_header(self, context):
        self.layout.label(text="", icon_value=cust_icon("W_BIOME"),)
        return None 

    def draw_header_preset(self, context):
        emitter_header(self)
        return None

    def draw(self, context):
        layout = self.layout
        draw_extra_panel(self,layout)
        return None


classes = (
            
    SCATTER5_PT_extra,

    )


#if __name__ == "__main__":
#    register()

