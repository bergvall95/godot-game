
# oooooooooooo                                               .
# `888'     `8                                             .o8
#  888         oooo    ooo oo.ooooo.   .ooooo.  oooo d8b .o888oo
#  888oooo8     `88b..8P'   888' `88b d88' `88b `888""8P   888
#  888    "       Y888'     888   888 888   888  888       888
#  888       o  .o8"'88b    888   888 888   888  888       888 .
# o888ooooood8 o88'   888o  888bod8P' `Y8bod8P' d888b      "888"
#                           888
#                          o888o

import bpy, json, os  

from .. resources.icons import cust_icon
from .. resources.translate import translate

from .. utils.override_utils import mode_override


#   .oooooo.                                               .
#  d8P'  `Y8b                                            .o8
# 888      888 oo.ooooo.   .ooooo.  oooo d8b  .oooo.   .o888oo  .ooooo.  oooo d8b
# 888      888  888' `88b d88' `88b `888""8P `P  )88b    888   d88' `88b `888""8P
# 888      888  888   888 888ooo888  888      .oP"888    888   888   888  888
# `88b    d88'  888   888 888    .o  888     d8(  888    888 . 888   888  888
#  `Y8bood8P'   888bod8P' `Y8bod8P' d888b    `Y888""8o   "888" `Y8bod8P' d888b
#               888
#              o888o


class SCATTER5_OT_export_to_json(bpy.types.Operator):

    bl_idname  = "scatter5.export_to_json"
    bl_label   = translate("Choose Folder")
    bl_description = translate("Export the selected scatter-system(s) visible in the viewport as .json information data.")

    filepath : bpy.props.StringProperty(subtype="DIR_PATH")
    popup_menu : bpy.props.BoolProperty(default=True, options={"SKIP_SAVE",},)

    def invoke(self, context, event):

        scat_scene = bpy.context.scene.scatter5 
        emitter    = scat_scene.emitter
        psys_sel   = emitter.scatter5.get_psys_selected()

        if (len(psys_sel)==0):
            if (self.popup_menu):
                bpy.ops.scatter5.popup_menu(title=translate("Export Failed"), msgs=translate("No Scatter-System(s) Selected"), icon="ERROR",)
            return {'FINISHED'}

        context.window_manager.fileselect_add(self)

        return {'RUNNING_MODAL'}        

    def execute(self, context):

        return {'FINISHED'}


class SCATTER5_OT_export_to_instance(bpy.types.Operator):

    bl_idname  = "scatter5.export_to_instance"
    bl_label   = translate("Export Selected System(s) as Instance")
    bl_description = translate("Export the selected scatter-system(s) visible in the viewport as blender instances object in a newly created export collection.")
    bl_options = {'INTERNAL','UNDO'}

    option : bpy.props.StringProperty(default="", options={"SKIP_SAVE",},) #"remove"/"hide"
    popup_menu : bpy.props.BoolProperty(default=True, options={"SKIP_SAVE",},)


    def invoke(self, context, event):

        scat_scene = bpy.context.scene.scatter5 
        emitter    = scat_scene.emitter
        psys_sel   = emitter.scatter5.get_psys_selected()
        
        if (len(psys_sel)==0):
            if (self.popup_menu):
                bpy.ops.scatter5.popup_menu(title=translate("Export Failed"), msgs=translate("No Scatter-System(s) Selected"), icon="ERROR",)
            return {'FINISHED'}

        def draw(self, context):

            layout = self.layout
            layout.label(text=translate("What shall we do with the system(s) ?"))
            layout.separator()
            layout.operator("scatter5.export_to_instance",text=translate("Keep"),icon="RESTRICT_VIEW_OFF").option = "ignore"
            layout.operator("scatter5.export_to_instance",text=translate("Keep & Hide"),icon="RESTRICT_VIEW_ON").option = "hide"
            layout.operator("scatter5.export_to_instance",text=translate("Remove"),icon="TRASH").option = "remove"

            return None

        bpy.context.window_manager.popup_menu(draw)

        return {'FINISHED'}  
        
    def execute(self, context):
        return {'FINISHED'}      


class SCATTER5_OT_export_to_mesh(bpy.types.Operator):

    bl_idname  = "scatter5.export_to_mesh"
    bl_label   = translate("Merge Selected System(s) as Mesh")
    bl_description = translate("Export the selected scatter-system(s) visible in the viewport as one large merged mesh-object. Note that this process might be extremely computer intensive depending on how heavy is the resulting mesh. Use this operator wisely.")
    bl_options = {'INTERNAL','UNDO'}

    option : bpy.props.StringProperty(default="", options={"SKIP_SAVE",},) #"remove"/"hide"
    popup_menu : bpy.props.BoolProperty(default=True, options={"SKIP_SAVE",},)


    def invoke(self, context, event):

        scat_scene = bpy.context.scene.scatter5 
        emitter    = scat_scene.emitter
        psys_sel   = emitter.scatter5.get_psys_selected()
        
        if (len(psys_sel)==0):
            if (self.popup_menu):
                bpy.ops.scatter5.popup_menu(title=translate("Export Failed"), msgs=translate("No Scatter-System(s) Selected"), icon="ERROR",)
            return {'FINISHED'}

        def draw(self, context):

            layout=self.layout
            layout.label(text=translate("What shall we do with the system(s) ?"))
            layout.label(text=translate("(Beware, this process can be intensive)"))
            layout.separator()
            layout.operator("scatter5.export_to_mesh",text=translate("Keep"),icon="RESTRICT_VIEW_OFF").option = "ignore"
            layout.operator("scatter5.export_to_mesh",text=translate("Keep & Hide"),icon="RESTRICT_VIEW_ON").option = "hide"
            layout.operator("scatter5.export_to_mesh",text=translate("Remove"),icon="TRASH").option = "remove"

            return

        bpy.context.window_manager.popup_menu(draw)

        return {'FINISHED'}   

    def execute(self, context):
        return {'FINISHED'}


#           oooo
#           `888
#  .ooooo.   888   .oooo.    .oooo.o  .oooo.o  .ooooo.   .oooo.o
# d88' `"Y8  888  `P  )88b  d88(  "8 d88(  "8 d88' `88b d88(  "8
# 888        888   .oP"888  `"Y88b.  `"Y88b.  888ooo888 `"Y88b.
# 888   .o8  888  d8(  888  o.  )88b o.  )88b 888    .o o.  )88b
# `Y8bod8P' o888o `Y888""8o 8""888P' 8""888P' `Y8bod8P' 8""888P'


classes = (
    
    SCATTER5_OT_export_to_instance,
    SCATTER5_OT_export_to_json,
    SCATTER5_OT_export_to_mesh,

    )