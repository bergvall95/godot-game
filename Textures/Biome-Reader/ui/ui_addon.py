

#####################################################################################################
#
# ooooo     ooo ooooo            .o.             .o8        .o8
# `888'     `8' `888'           .888.           "888       "888
#  888       8   888           .8"888.      .oooo888   .oooo888   .ooooo.  ooo. .oo.
#  888       8   888          .8' `888.    d88' `888  d88' `888  d88' `88b `888P"Y88b
#  888       8   888         .88ooo8888.   888   888  888   888  888   888  888   888
#  `88.    .8'   888        .8'     `888.  888   888  888   888  888   888  888   888
#    `YbodP'    o888o      o88o     o8888o `Y8bod88P" `Y8bod88P" `Y8bod8P' o888o o888o
#
#####################################################################################################


import bpy, os, platform 

from .. resources.icons import cust_icon
from .. resources.translate import translate
from .. resources import directories

from .. utils.str_utils import word_wrap, square_area_repr, count_repr

from . import ui_templates


# ooo        ooooo            o8o                         .o.             .o8        .o8
# `88.       .888'            `"'                        .888.           "888       "888
#  888b     d'888   .oooo.   oooo  ooo. .oo.            .8"888.      .oooo888   .oooo888   .ooooo.  ooo. .oo.
#  8 Y88. .P  888  `P  )88b  `888  `888P"Y88b          .8' `888.    d88' `888  d88' `888  d88' `88b `888P"Y88b
#  8  `888'   888   .oP"888   888   888   888         .88ooo8888.   888   888  888   888  888   888  888   888
#  8    Y     888  d8(  888   888   888   888        .8'     `888.  888   888  888   888  888   888  888   888
# o8o        o888o `Y888""8o o888o o888o o888o      o88o     o8888o `Y8bod88P" `Y8bod88P" `Y8bod8P' o888o o888o


def draw_addon(self,layout):
    """drawing dunction of AddonPrefs class, stored in properties"""

    row = layout.row()
    r1 = row.separator()
    col = row.column()
    r3 = row.separator()
        
    #Enter Manager 

    col.label(text=translate("Enter The Plugin Manager."),)

    enter = col.row()
    enter.scale_y = 1.5
    enter.operator("scatter5.impost_addonprefs", text=translate("Enter Manager"), icon_value=cust_icon("W_BIOME"),).state = True

    col.separator(factor=1.5)

    #Write license block 

    license_layout = col

    from .. __init__ import bl_info
    plugin_name = bl_info["name"]
    license_path = directories.addon_license_type

    license_layout.label(text=f"{plugin_name} Product: License Agreement.",)
    
    boxcol = license_layout.column(align=True)
    box = boxcol.box() #WARNING: Modifying this text does not in any shape or form change our legal conditions, find the conditions on www.geoscatter.com/legal 
    word_wrap(layout=box, max_char=81, alert=False, active=False, string=f"the “{plugin_name}” product is comprised of two licenses: a python script released under the GNU-GPL used for drawing an user interface, and a non-software geometry-node nodetree called the “GEO-SCATTER ENGINE” with a license similar to Royalty free licensing. By using {plugin_name}, users agree to the terms and conditions of both licenses. Only “GEO-SCATTER ENGINE” licenses downloaded from the official source listed on “www.geoscatter.com/download” are legitimate. Compared to the Royalty Free license, the “GEO-SCATTER ENGINE” end user license agreement provides an additional advantage by allowing users to freely share Blender scenes containing the nodetree, while also placing restrictions on how users may interact with our engine nodetree through the usage of scripts or plugins.",)
    boxl = boxcol.box()
    boxllbl = boxl.row()
    boxllbl.alignment = "CENTER"
    boxllbl.active = False
    boxllbl.operator("wm.url_open", text="Both licenses can be found on “www.geoscatter.com/legal”", emboss=False, ).url = "www.geoscatter.com/legal"

    is_individual = os.path.exists(os.path.join(license_path,"1.txt"))
    if (is_individual):
        license_layout.separator(factor=1.5)
        license_layout.label(text=f"{plugin_name} Engine: Individual License.",)
        boxcol = license_layout.column(align=True)
        box = boxcol.box() #WARNING: Modifying this text does not in any shape or form change our legal conditions, find the conditions on www.geoscatter.com/legal 
        word_wrap(layout=box, max_char=81, alert=False, active=False, string=f"The “Individual” license for “GEO-SCATTER ENGINE” is a non-transferable license that grants a single user the right to use the “GEO-SCATTER ENGINE” on any computer they own for either personal or professional use. This license legally requires a one-time fee and is subject to the terms and conditions outlined in the agreement found on “www.geoscatter.com/legal”. This license grants the licensee the permission to interact with our engine through the use of the “{plugin_name}” plugin.",)
        boxl = boxcol.box()
        boxllbl = boxl.row()
        boxllbl.alignment = "CENTER"
        boxllbl.active = False
        boxllbl.operator("wm.url_open", text="This agreement is available on “www.geoscatter.com/legal”", emboss=False, ).url = "www.geoscatter.com/legal"

    is_team = os.path.exists(os.path.join(license_path,"2.txt"))
    if (is_team):
        license_layout.separator(factor=1.5)
        license_layout.label(text=f"{plugin_name} Engine: Team License.",)
        boxcol = license_layout.column(align=True)
        box = boxcol.box() #WARNING: Modifying this text does not in any shape or form change our legal conditions, find the conditions on www.geoscatter.com/legal 
        word_wrap(layout=box, max_char=81, alert=False, active=False, string=f"The “Team” license for “GEO-SCATTER ENGINE” permits up to six users who belong to the same team or organization to use the “GEO-SCATTER ENGINE” on up to six computers. This license is transferable within the same organization but not to other organizations or individuals. A one-time fee is legally required for this license, and it is subject to the terms and conditions outlined in the agreement found on “www.geoscatter.com/legal”. This license grants licensee(s) the permission to interact with our engine through the use of the “{plugin_name}” plugin.",)
        boxl = boxcol.box()
        boxllbl = boxl.row()
        boxllbl.alignment = "CENTER"
        boxllbl.active = False
        boxllbl.operator("wm.url_open", text="This agreement is available on “www.geoscatter.com/legal”", emboss=False, ).url = "www.geoscatter.com/legal"
    
    is_studio = os.path.exists(os.path.join(license_path,"3.txt"))
    if (is_studio):
        license_layout.separator(factor=1.5)
        license_layout.label(text=f"{plugin_name} Engine: Studio License.",)
        boxcol = license_layout.column(align=True)
        box = boxcol.box() #WARNING: Modifying this text does not in any shape or form change our legal conditions, find the conditions on www.geoscatter.com/legal 
        word_wrap(layout=box, max_char=81, alert=False, active=False, string=f"The “Studio” license for “GEO-SCATTER ENGINE” allows every employee of a business to use the “GEO-SCATTER ENGINE” on an unlimited number of computers. Like the “Team” license, this license is transferable within the same organization but not to other organizations or individuals. A one-time fee is legally required for this license, and it is subject to the terms and conditions outlined in the agreement found on “www.geoscatter.com/legal”. This license grants licensee(s) permission to interact with our engine using our official “{plugin_name}” script, or custom scripts/plugins as well.",)
        boxl = boxcol.box()
        boxllbl = boxl.row()
        boxllbl.alignment = "CENTER"
        boxllbl.active = False
        boxllbl.operator("wm.url_open", text="This agreement is available on “www.geoscatter.com/legal”", emboss=False, ).url = "www.geoscatter.com/legal"
    
    license_layout.separator(factor=1.5)
    license_layout.label(text="Contact Information:",)
    boxcol = license_layout.column(align=True)
    box = boxcol.box()
    word_wrap(layout=box, max_char=81, alert=False, active=False, string="If you have any inquiries or any questions, you may contact us via “contact@geoscatter.com” or through our diverse social medial lised on “www.geoscatter.com” or within this very plugin.",)
    boxl = boxcol.box()
    boxllbl = boxl.row()
    boxllbl.alignment = "CENTER"
    boxllbl.active = False
    boxllbl.operator("wm.url_open", text="Visit “www.geoscatter.com”", emboss=False, ).url = "www.geoscatter.com"

    license_layout.label(text=f"Trademark.",)

    boxcol = license_layout.column(align=True)
    box = boxcol.box() #WARNING: Modifying this text does not in any shape or form change our legal conditions, find the conditions on www.geoscatter.com/legal 
    word_wrap(layout=box, max_char=81, alert=False, active=False, string=f"Please note that the “GEO-SCATTER” name & logo is a trademark or registered trademark of “BD3D DIGITAL DESIGN, SLU” in the U.S. and/or other countries. We reserve all rights over this trademark.",)
    boxl = boxcol.box()
    boxllbl = boxl.row()
    boxllbl.alignment = "CENTER"
    boxllbl.active = False
    boxllbl.operator("wm.url_open", text="Visit “www.geoscatter.com/legal”", emboss=False, ).url = "www.geoscatter.com/legal"

    disclaimer = col.column()
    disclaimer.separator(factor=0.7)
    disclaimer.active = True
    disclaimer.label(text="*Extend this interface if texts are not readable.",)

    col.separator(factor=2)

    return None


# ooooo   ooooo  o8o   o8o                     oooo         o8o
# `888'   `888'  `"'   `"'                     `888         `"'
#  888     888  oooo  oooo  .oooo.    .ooooo.   888  oooo  oooo  ooo. .oo.    .oooooooo
#  888ooooo888  `888  `888 `P  )88b  d88' `"Y8  888 .8P'   `888  `888P"Y88b  888' `88b
#  888     888   888   888  .oP"888  888        888888.     888   888   888  888   888
#  888     888   888   888 d8(  888  888   .o8  888 `88b.   888   888   888  `88bod8P'
# o888o   o888o o888o  888 `Y888""8o `Y8bod8P' o888o o888o o888o o888o o888o `8oooooo.
#                      888                                                   d"     YD
#                  .o. 88P                                                   "Y88888P'
#                  `Y888P


def addonpanel_overridedraw(self,context):
    """Impostor Main"""

    layout = self.layout

    scat_win = bpy.context.window_manager.scatter5

    #Prefs
    if (scat_win.category_manager=="prefs"):
        draw_add_prefs(self, layout)
        
    elif (scat_win.category_manager=="library"):
        from . ui_biome_library import draw_library_grid
        draw_library_grid(self, layout)

    elif (scat_win.category_manager=="market"):
        from . ui_biome_library import draw_online_grid
        draw_online_grid(self, layout)

    return None

            
def addonheader_overridedraw(self, context):
    """Impostor Header"""

    layout = self.layout

    scat_scene = context.scene.scatter5
    scat_win = bpy.context.window_manager.scatter5

    from .. __init__ import bl_info
    plugin_name = bl_info["name"]
    
    row = layout.row()
    row.template_header()

    scat = row.row(align=True)
    scat.scale_x = 1.1
    scat.menu("SCATTER5_MT_manager_header_menu_scatter", text=plugin_name, icon_value=cust_icon("W_BIOME"),)

    if (scat_win.category_manager=="library"):
        row.menu("SCATTER5_MT_manager_header_menu_interface", text=translate("Interface"),)
        row.menu("SCATTER5_MT_manager_header_menu_open", text=translate("File"),)
        popover = row.row(align=True)
        popover.emboss = "NONE"
        popover.popover(panel="SCATTER5_PT_creation_operator_load_biome", text="Settings",)

    elif (scat_win.category_manager=="market"):
        row.menu("SCATTER5_MT_manager_header_menu_interface", text=translate("Interface"),)
        row.menu("SCATTER5_MT_manager_header_menu_open", text=translate("File"),)

    elif (scat_win.category_manager=="lister_large"):
        row.menu("SCATTER5_MT_manager_header_menu_interface", text=translate("Interface"),)

    elif (scat_win.category_manager=="lister_stats"):
        row.menu("SCATTER5_MT_manager_header_menu_interface", text=translate("Interface"),)

    elif (scat_win.category_manager=="prefs"):
        row.menu("USERPREF_MT_save_load", text=translate("Preferences"),)

    layout.separator_spacer()

    if (scat_win.category_manager!="prefs"):
        
        emit = layout.row()
        # if (scat_scene.emitter is None):
        #     emitlbl = emit.row()
        #     emitlbl.label(text="   "+translate("Choose an emitter →"),)
        emit.prop(scat_scene,"emitter",text="", icon_value=cust_icon("W_EMITTER"),)

    exit = layout.row()
    exit.alert = True
    exit.operator("scatter5.impost_addonprefs",text=translate("Exit"),icon='PANEL_CLOSE').state = False

    return None


def addonnavbar_overridedraw(self, context):
    """importor T panel"""

    layout = self.layout

    scat_win = context.window_manager.scatter5
    scat_scene = context.scene.scatter5
    emitter = scat_scene.emitter

    #Close if user is dummy 

    if (not context.space_data.show_region_header):
        exit = layout.column()
        exit.alert = True
        exit.operator("scatter5.impost_addonprefs",text=translate("Exit"),icon='PANEL_CLOSE').state = False
        exit.scale_y = 1.8
        return None

    #Draw main categories 

    enum = layout.column()
    enum.scale_y = 1.3
    enum.prop(scat_win,"category_manager",expand=True)

    layout.separator(factor=4)

    #Per category T panel

    if (scat_win.category_manager=="library"):

        lbl = layout.row()
        lbl.active = False
        lbl.label(text=translate("Navigation"),)

        row = layout.row(align=True)
        row.scale_y = 1.0
        row.prop(scat_scene,"library_search",icon="VIEWZOOM",text="") 

        layout.separator(factor=0.33)

        wm = bpy.context.window_manager
        navigate = layout.column(align=True)
        navigate.scale_y = 1.0
        navigate.template_list("SCATTER5_UL_folder_navigation", "", wm.scatter5, "folder_navigation", wm.scatter5, "folder_navigation_idx",rows=20,)

        elements_count = 0 
        if (len(scat_win.folder_navigation)!=0):
            elements_count = scat_win.folder_navigation[scat_win.folder_navigation_idx].elements_count

        indic = navigate.box()
        indic.scale_y = 1.0
        indic.label(text=f'{elements_count} {translate("Elements in Folder")}')
        
        # layout.separator()

        # lbl = layout.row()
        # lbl.active = False
        # lbl.label(text=translate("Need More?"),)

        # row = layout.row(align=True)
        # row.scale_y = 1.0
        # row.operator("scatter5.exec_line",text=translate("Get Biomes"), icon="URL",).api = 'scat_win.category_manager = "market" ; bpy.context.area.tag_redraw()'

        # lbl = layout.row()
        # lbl.active = False
        # lbl.label(text=translate("Install a Scatpack?"),)

        # row = layout.row(align=True)
        # row.scale_y = 1.0
        # row.operator("scatter5.install_package", text=translate("Install a Pack"), icon="NEWFOLDER")

    elif (scat_win.category_manager=="market"):

        lbl = layout.row()
        lbl.active = False
        lbl.label(text=translate("All Biomes"),)

        row = layout.row(align=True)
        row.scale_y = 1.0
        row.operator("wm.url_open",text=translate("Visit Website"),icon="URL").url="https://geoscatter.com/biomes"

        lbl = layout.row()
        lbl.active = False
        lbl.label(text=translate("Share your Pack"),)

        row = layout.row(align=True)
        row.scale_y = 1.0
        row.operator("wm.url_open",text=translate("Contact Us"),icon="URL").url="https://discord.com/invite/F7ZyjP6VKB"

        lbl = layout.row()
        lbl.active = False
        lbl.label(text=translate("Refresh Page"),)

        row = layout.row(align=True)
        row.scale_y = 1.0
        row.operator("scatter5.manual_fetch_from_git",text=translate("Re-Fetch"), icon="FILE_REFRESH")

    elif (scat_win.category_manager=="lister_large"):

        if (emitter is not None):

            nbr = len(emitter.scatter5.get_psys_selected(all_emitters=scat_scene.factory_alt_selection_method=="all_emitters"))

            # lbl = layout.row()
            # lbl.active = False
            # lbl.label(text=translate("Batch Optimize"),)
            #
            # row = layout.row(align=True)
            # row.scale_y = 1.00
            # row.operator("scatter5.batch_optimization",text=translate("Set Optimizations"),icon="MEMORY")

            lbl = layout.row()
            lbl.active = False
            lbl.label(text=translate("Bounding-Box"),)

            row = layout.row(align=True)
            row.scale_y = 1.0
            row.operator("scatter5.batch_bounding_box",text=translate("Set Bounds"),icon="CUBE").pop_dialog = True

            lbl = layout.row()
            lbl.active = False
            lbl.label(text=translate("Alt Behavior")+f" [{nbr}]",)
            
            row = layout.row(align=True)
            if (scat_scene.factory_alt_allow):
                  row.scale_y = 1.1
                  row.prop(scat_scene,"factory_alt_selection_method",text="",)
            else: row.prop(scat_scene,"factory_alt_allow",text=translate("Enable Alt"), icon="BLANK1",)


    elif (scat_win.category_manager=="lister_stats"):

        if (emitter is not None):

            lbl = layout.row()
            lbl.active = False
            lbl.label(text=translate("Estimate Count"),)

            row = layout.row()
            row.scale_y = 1.0
            op = row.operator("scatter5.exec_line",text=translate("Refresh"),icon="FILE_REFRESH",)
            op.api = f"[ ( p.get_scatter_count(state='render',) , p.get_scatter_count(state='viewport') ) for o in bpy.context.scene.objects if len(o.scatter5.particle_systems) for p in o.scatter5.particle_systems ] ; [a.tag_redraw() for a in bpy.context.screen.areas]"
            op.description = translate("Re-compute the instance-count statistics of every single scatter-system in your scene. Note that you are able to show these stats in this lister interface! To do so, please enable the statistics in the header menu")

            lbl = layout.row()
            lbl.active = False
            lbl.label(text=translate("Estimate Area"),)

            row = layout.row()
            row.scale_y = 1.0
            op = row.operator("scatter5.exec_line",text=translate("Refresh"),icon="FILE_REFRESH",)
            op.api = f"[ p.get_surfaces_square_area(evaluate='recalculate', eval_modifiers=True, get_selection=False,) for o in bpy.context.scene.objects if len(o.scatter5.particle_systems) for p in o.scatter5.particle_systems] ; [a.tag_redraw() for a in bpy.context.screen.areas]"
            op.description = translate("Re-compute the square area statistics of every single scatter-surface in your scene. Note that you are able to show these stats in this lister interface! To do so, please enable the statistics in the header menu")

    elif (scat_win.category_manager=="prefs"):
        pass

    return None


# 88  88 88  88888    db     dP""b8 88  dP      dP"Yb  88""Yb 888888 88""Yb    db    888888  dP"Yb  88""Yb
# 88  88 88     88   dPYb   dP   `" 88odP      dP   Yb 88__dP 88__   88__dP   dPYb     88   dP   Yb 88__dP
# 888888 88 o.  88  dP__Yb  Yb      88"Yb      Yb   dP 88"""  88""   88"Yb   dP__Yb    88   Yb   dP 88"Yb
# 88  88 88 "bodP' dP""""Yb  YboodP 88  Yb      YbodP  88     888888 88  Yb dP""""Yb   88    YbodP  88  Yb


class SCATTER5_OT_impost_addonprefs(bpy.types.Operator):
    """Monkey patch drawing code of addon preferences to our own code, temporarily"""

    bl_idname      = "scatter5.impost_addonprefs"
    bl_label       = ""
    bl_description = translate("replace/restore native blender preference ui by custom scatter manager ui")

    state : bpy.props.BoolProperty()

    Status = False
    AddonPanel_OriginalDraw = None
    AddonNavBar_OriginalDraw = None
    AddonHeader_OriginalDraw = None

    def panel_hijack(self):
        """register impostors"""

        cls = type(self)
        if (cls.Status==True):
            return None

        #show header just in case user hided it (show/hide header on 'PREFERENCE' areas)

        for window in bpy.context.window_manager.windows:
            for area in window.screen.areas:
                if (area.type=='PREFERENCES'):
                    for space in area.spaces:
                        if (space.type=='PREFERENCES'):
                            space.show_region_header = True

        #Save Original Class Drawing Function in global , and replace their function with one of my own 

        cls.AddonPanel_OriginalDraw = bpy.types.USERPREF_PT_addons.draw
        bpy.types.USERPREF_PT_addons.draw = addonpanel_overridedraw
            
        cls.AddonNavBar_OriginalDraw = bpy.types.USERPREF_PT_navigation_bar.draw
        bpy.types.USERPREF_PT_navigation_bar.draw = addonnavbar_overridedraw
        
        cls.AddonHeader_OriginalDraw = bpy.types.USERPREF_HT_header.draw
        bpy.types.USERPREF_HT_header.draw = addonheader_overridedraw
        
        cls.Status=True

        return None

    def panel_restore(self):
        """restore and find original drawing classes"""

        cls = type(self)
        if (cls.Status==False):
            return None

        #restore original drawing code 
        
        bpy.types.USERPREF_PT_addons.draw = cls.AddonPanel_OriginalDraw
        cls.AddonPanel_OriginalDraw = None 

        bpy.types.USERPREF_PT_navigation_bar.draw = cls.AddonNavBar_OriginalDraw
        cls.AddonNavBar_OriginalDraw = None 

        bpy.types.USERPREF_HT_header.draw = cls.AddonHeader_OriginalDraw
        cls.AddonHeader_OriginalDraw = None 

        #Trigger Redraw, otherwise some area will be stuck until user put cursor 

        for window in bpy.context.window_manager.windows:
            for area in window.screen.areas:
                if (area.type == 'PREFERENCES'):
                    area.tag_redraw()
                    
        cls.Status=False

        return None

    def execute(self, context):

        if (self.state==True):
              self.panel_hijack()
        else: self.panel_restore()

        return{'FINISHED'}


# oooooooooo.                                        ooooo     ooo                              ooooooooo.                       .o88o.
# `888'   `Y8b                                       `888'     `8'                              `888   `Y88.                     888 `"
#  888      888 oooo d8b  .oooo.   oooo oooo    ooo   888       8   .oooo.o  .ooooo.  oooo d8b   888   .d88' oooo d8b  .ooooo.  o888oo   .oooo.o
#  888      888 `888""8P `P  )88b   `88. `88.  .8'    888       8  d88(  "8 d88' `88b `888""8P   888ooo88P'  `888""8P d88' `88b  888    d88(  "8
#  888      888  888      .oP"888    `88..]88..8'     888       8  `"Y88b.  888ooo888  888       888          888     888ooo888  888    `"Y88b.
#  888     d88'  888     d8(  888     `888'`888'      `88.    .8'  o.  )88b 888    .o  888       888          888     888    .o  888    o.  )88b
# o888bood8P'   d888b    `Y888""8o     `8'  `8'         `YbodP'    8""888P' `Y8bod8P' d888b     o888o        d888b    `Y8bod8P' o888o   8""888P'



def draw_add_prefs(self, layout):
    
    #limit panel width

    row = layout.row()
    row.alignment="LEFT"
    main = row.column()
    main.alignment = "LEFT"

    draw_add_packs(self,main)
    ui_templates.separator_box_out(main)

    draw_add_environment(self,main)
    ui_templates.separator_box_out(main)

    draw_add_paths(self,main)
    ui_templates.separator_box_out(main)

    draw_add_fetch(self,main)
    ui_templates.separator_box_out(main)

    #draw_add_lang(self,main)
    #ui_templates.separator_box_out(main)
    

    draw_add_npanl(self,main)
    ui_templates.separator_box_out(main)


    draw_add_dev(self,main)
    ui_templates.separator_box_out(main)
            
    for i in range(10):
        layout.separator_spacer()

    return None 


def draw_add_packs(self,layout):

    box, is_open = ui_templates.box_panel(self, layout, 
        prop_str = "ui_add_packs", #INSTRUCTION:REGISTER:UI:BOOL_NAME("ui_add_packs");BOOL_VALUE(1)
        icon = "NEWFOLDER", 
        name = translate("Install a Package"),
        popover_argument = "ui_add_packs", #INSTRUCTION:REGISTER:UI:ARGS_POINTERS("ui_add_packs")
        )
    if is_open:

            row = box.row()
            row.separator(factor=0.3)
            col = row.column()
            row.separator(factor=0.3)

            rwoo = col.row()
            rwoo.operator("scatter5.install_package", text=translate("Install a Package"), icon="NEWFOLDER")
            scatpack = rwoo.row()
            scatpack.operator("scatter5.exec_line", text=translate("Find Biomes Online"),icon_value=cust_icon("W_SUPERMARKET")).api = "scat_win.category_manager='market' ; bpy.ops.scatter5.tag_redraw()"

            ui_templates.separator_box_in(box)

    return None


def draw_add_fetch(self,layout):

    addon_prefs = bpy.context.preferences.addons["Biome-Reader"].preferences

    box, is_open = ui_templates.box_panel(self, layout, 
        prop_str = "ui_add_fetch", #INSTRUCTION:REGISTER:UI:BOOL_NAME("ui_add_fetch");BOOL_VALUE(1)
        icon = "URL", 
        name = translate("Scatpack Previews Fetch"),
        )
    if is_open:

            row = box.row()
            row.separator(factor=0.3)
            col = row.column()
            row.separator(factor=0.3)

            ui_templates.bool_toggle(col, 
                prop_api=addon_prefs,
                prop_str="fetch_automatic_allow", 
                label=translate("Automatically Fetch Packs Previews from Web."), 
                icon="FILE_REFRESH", 
                left_space=False,
                )
            
            col.separator()
            row = col.row()
            #
            subr = row.row()
            subr.active = addon_prefs.fetch_automatic_allow
            subr.prop(addon_prefs, "fetch_automatic_daycount", text=translate("Fetch every n Day"),)
            #
            subr = row.row()
            subr.operator("scatter5.manual_fetch_from_git", text=translate("Refresh Online Previews"), icon="FILE_REFRESH")

            ui_templates.separator_box_in(box)
    
    return None

    
def draw_add_browser(self,layout):

    addon_prefs = bpy.context.preferences.addons["Biome-Reader"].preferences

    box, is_open = ui_templates.box_panel(self, layout, 
        prop_str = "ui_add_browser", #INSTRUCTION:REGISTER:UI:BOOL_NAME("ui_add_browser");BOOL_VALUE(1)
        icon = "ASSET_MANAGER", 
        name = translate("Asset Browser Convert"),
        doc_panel = "SCATTER5_PT_docs", 
        popover_argument = "ui_add_browser", #INSTRUCTION:REGISTER:UI:ARGS_POINTERS("ui_add_browser")
        )
    if is_open:

            row = box.row()
            row.separator(factor=0.3)
            col = row.column()
            row.separator(factor=0.3)
            
            col.operator("scatter5.make_asset_library", text=translate("Convert blend(s) in folder"), icon="FILE_BLEND",)
                
            col.separator(factor=0.5)
            word_wrap(layout=col, max_char=70, alert=False, active=True, string=translate("Warning, this operator will quit this session to sequentially open all blends and marks their asset(s). Please do not interact with the interface until the task is finished.."),)

            ui_templates.separator_box_in(box)
    
    return None


def draw_clean_data(self,layout):

    addon_prefs = bpy.context.preferences.addons["Biome-Reader"].preferences

    box, is_open = ui_templates.box_panel(self, layout, 
        prop_str = "clean_data", #INSTRUCTION:REGISTER:UI:BOOL_NAME("clean_data");BOOL_VALUE(1)
        icon = "MESH_DATA", 
        name = translate("Clanse Data"),
        #doc_panel = "SCATTER5_PT_docs", 
        #popover_argument = "clean_data", #INSTRUCTION:REGISTER:UI:ARGS_POINTERS("clean_data")
        )
    if is_open:

            row = box.row()
            row.separator(factor=0.3)
            col = row.column()
            row.separator(factor=0.3)
            
            col.operator("scatter5.clean_unused_import_data", text=translate("Delete Unused Imports"), icon="TRASH",)
                
            col.separator(factor=0.5)

            op = col.operator("outliner.orphans_purge", text=translate("Purge Orphans Data"), icon="ORPHAN_DATA",)
            op.do_recursive = True
            
            ui_templates.separator_box_in(box)
    
    return None


def draw_add_lang(self,layout):

    box, is_open = ui_templates.box_panel(self, layout, 
        prop_str = "ui_add_lang", #INSTRUCTION:REGISTER:UI:BOOL_NAME("ui_add_lang");BOOL_VALUE(1)
        icon = "WORLD_DATA", 
        name = translate("Languages"),
        )
    if is_open: 

            box.label(text="TODO create .excel sheet, separate it per column into single column file, create enum from single column, make enum then made translate() fct work on restart")

            txt = box.column()
            txt.scale_y = 0.8
            txt.label(text="Supported Languages:")
            txt.label(text="        -English")
            txt.label(text="        -Spanish")
            txt.label(text="        -French")
            txt.label(text="        -Japanese")
            txt.label(text="        -Chinese (Simplified)")

            ui_templates.separator_box_in(box)

    return None 


def draw_add_npanl(self,layout):

    addon_prefs = bpy.context.preferences.addons["Biome-Reader"].preferences

    box, is_open = ui_templates.box_panel(self, layout, 
        prop_str = "ui_add_npanl", #INSTRUCTION:REGISTER:UI:BOOL_NAME("ui_add_npanl");BOOL_VALUE(1)
        icon = "MENU_PANEL", 
        name = translate("N Panel Name"),
        )
    if is_open:

            row = box.row()
            row.separator(factor=0.3)
            col = row.column()
            row.separator(factor=0.3)

            ope = col.row()
            ope.alert = (addon_prefs.tab_name in [""," ","  "])
            ope.prop(addon_prefs,"tab_name",text="")
            
            ui_templates.separator_box_in(box)

    return None


def draw_add_paths(self,layout):

    addon_prefs = bpy.context.preferences.addons["Biome-Reader"].preferences

    box, is_open = ui_templates.box_panel(self, layout, 
        prop_str = "ui_add_paths", #INSTRUCTION:REGISTER:UI:BOOL_NAME("ui_add_paths");BOOL_VALUE(1)
        icon = "FILEBROWSER", 
        name = translate("Scatter-Library Location"),
        doc_panel = "SCATTER5_PT_docs", 
        popover_argument = "ui_add_paths", #INSTRUCTION:REGISTER:UI:ARGS_POINTERS("ui_add_paths")
        )
    if is_open:

            row = box.row()
            row.separator(factor=0.3)
            col = row.column()
            row.separator(factor=0.3)
                
            is_library = os.path.exists(addon_prefs.library_path)
            is_biomes  = os.path.exists(os.path.join(addon_prefs.library_path,"_biomes_"))
            is_presets = os.path.exists(os.path.join(addon_prefs.library_path,"_presets_"))
            is_bitmaps = os.path.exists(os.path.join(addon_prefs.library_path,"_bitmaps_"))

            colc = col.column(align=True)

            pa = colc.row(align=True)
            pa.alert = not is_library
            pa.prop(addon_prefs,"library_path",text="")

            if ( False in (is_library, is_biomes, is_presets,) ):

                colc.separator(factor=0.7)

                warn = colc.column(align=True)
                warn.scale_y = 0.9
                warn.alert = True
                warn.label(text=translate("There's problem(s) with the location you have chosen"),icon="ERROR")
                
                if (not is_library):
                    warn.label(text=" "*10 + translate("-The chosen path does not exists"))
                if (not is_biomes):
                    warn.label(text=" "*10 + translate("-'_biomes_' Directory not Found"))
                if (not is_presets):
                    warn.label(text=" "*10 + translate("-'_presets_' Directory not Found"))
                if (not is_bitmaps):
                    warn.label(text=" "*10 + translate("-'_bitmaps_' Directory not Found"))

                warn.label(text=translate("We will use the default library location instead"),icon="BLANK1")

            if all([ is_library, is_biomes, is_presets, is_bitmaps]) and (directories.lib_library!=addon_prefs.library_path):
                colc.separator(factor=0.7)

                warn = colc.column(align=True)
                warn.scale_y = 0.85
                warn.label(text=translate("Chosen Library is Valid, Please save your addonprefs and restart blender."),icon="CHECKMARK")

            col.separator()

            row = col.row()
            col1 = row.column()
            col1.operator("scatter5.reload_biome_library", text=translate("Reload Library"), icon="FILE_REFRESH")
            col1.operator("scatter5.reload_preset_gallery", text=translate("Reload Presets"), icon="FILE_REFRESH")
            col1.operator("scatter5.dummy", text=translate("Reload Images"), icon="FILE_REFRESH")

            col2 = row.column()
            col2.operator("scatter5.open_directory", text=translate("Open Library"),icon="FOLDER_REDIRECT").folder = directories.lib_library
            col2.operator("scatter5.open_directory", text=translate("Open Default Library"),icon="FOLDER_REDIRECT").folder = directories.lib_default
            col2.operator("scatter5.open_directory", text=translate("Open Blender Addons"),icon="FOLDER_REDIRECT").folder = directories.blender_addons                    
            
            ui_templates.separator_box_in(box)

    return None 


def draw_add_environment(self,layout):

    addon_prefs = bpy.context.preferences.addons["Biome-Reader"].preferences

    box, is_open = ui_templates.box_panel(self, layout, 
        prop_str = "ui_add_environment", #INSTRUCTION:REGISTER:UI:BOOL_NAME("ui_add_environment");BOOL_VALUE(1)
        icon = "LONGDISPLAY", 
        name = translate("Biomes Environment Paths"),
        doc_panel = "SCATTER5_PT_docs", 
        popover_argument = "ui_add_environment", #INSTRUCTION:REGISTER:UI:ARGS_POINTERS("ui_add_environment")
        )
    if is_open:

            row = box.row()
            row.separator(factor=0.3)
            col = row.column()
            row.separator(factor=0.3)

            ui_templates.bool_toggle(col,
                prop_api=addon_prefs,
                prop_str="blend_environment_path_allow",
                label=translate("Search for blend(s) in priority in given paths"),
                icon="FILE_BLEND",
                left_space=False,
                )

            if (addon_prefs.blend_environment_path_allow):

                col.separator(factor=0.5)

                alcocol = col.column(align=True)
                alcol = alcocol.box().column()

                #property interface

                if (len(addon_prefs.blend_environment_paths)!=0):

                    for l in addon_prefs.blend_environment_paths:

                        row = alcol.row(align=True)

                        path = row.row(align=True)
                        path.alert = not os.path.exists(l.blend_folder)
                        path.prop(l, "blend_folder", text="", )

                        #find index for remove operator
                        for i,p in enumerate(addon_prefs.blend_environment_paths):
                            if (p.name==l.name):
                                break
                        
                        op = row.operator("scatter5.exec_line", text="", icon="TRASH",)
                        op.api = f"addon_prefs.blend_environment_paths.remove({i})"

                        continue

                else:
                    row = alcol.row(align=True)
                    row.active = False
                    row.label(text=translate("No Path(s) Found"))
                    
                #add button 

                addnew = alcocol.row(align=True)
                addnew.scale_y = 0.85
                op = addnew.operator("scatter5.exec_line", text=translate("Add New Path"), icon="ADD", depress=False)
                op.api = "n = addon_prefs.blend_environment_paths.add() ; n.name=str(len(addon_prefs.blend_environment_paths)-1)"
                op.description = translate("Add a path the biome system will search for blends in!")
                
                #too much nest warnings

                for p in addon_prefs.blend_environment_paths:
                    if (p.high_nest):

                        col.separator(factor=1.0)
                        alcol = col.column(align=True)
                        alcol.scale_y = 0.9
                        alcol.alert = True

                        word_wrap(layout=alcol, max_char=65, alert=True, active=True, icon="INFO", string=translate("Warning, some path(s) seems to contain a lot of folders? Our plugin will only search for files in the first two level of folders"),)
                        break 

                col.separator(factor=1.0)

            ui_templates.bool_toggle(col,
                prop_api=addon_prefs,
                prop_str="blend_environment_path_asset_browser_allow", 
                label=translate("Search for blend(s) in your blender asset-browser"),
                icon="ASSET_MANAGER",
                left_space=False,
                )

            if (addon_prefs.blend_environment_path_asset_browser_allow):

                col.separator(factor=0.5)
                alcol = col.box().column()

                if (len(bpy.context.preferences.filepaths.asset_libraries)!=0):

                    for l in bpy.context.preferences.filepaths.asset_libraries:

                        row = alcol.row()
                        row.enabled = False
                        row.prop(l,"path", text="")

                        continue
                else:
                    row = alcol.row(align=True)
                    row.active = False
                    row.label(text=translate("No Path(s) Found"))

                col.separator(factor=0.5)

            ui_templates.separator_box_in(box)

    return None


def draw_add_dev(self,layout):

    addon_prefs = bpy.context.preferences.addons["Biome-Reader"].preferences

    box, is_open = ui_templates.box_panel(self, layout, 
        prop_str = "ui_add_dev", #INSTRUCTION:REGISTER:UI:BOOL_NAME("ui_add_dev");BOOL_VALUE(1)
        icon = "CONSOLE", 
        name = translate("Debugging"),
        )
    if is_open:

            ui_templates.bool_toggle(box, 
                prop_api=addon_prefs,
                prop_str="debug_interface", 
                label=translate("Debug Interface."), 
                icon="GHOST_DISABLED", 
                left_space=True,
                )

            ui_templates.bool_toggle(box, 
                prop_api=addon_prefs,
                prop_str="debug", 
                label=translate("Debug Prints."),
                icon="CONSOLE", 
                left_space=True,
                )

            d = box.row()
            d.active = addon_prefs.debug
            ui_templates.bool_toggle(d, 
                prop_api=addon_prefs,
                prop_str="debug_depsgraph", 
                label=translate("Debug Prints (Depsgraph)."),
                icon="CONSOLE", 
                left_space=True,
                )

            row = box.row()
            row.separator(factor=0.3)
            col = row.column()
            row.separator(factor=0.3)

            op = col.operator("scatter5.fix_nodetrees", text=translate("Fix Nodetrees & Scatter Objects"), icon="TOOL_SETTINGS",)
            op.force_update = True
            
            col.separator(factor=0.5)

            col.operator("scatter5.icons_reload", text=translate("Reload Plugin Icons"), icon="TOOL_SETTINGS",)

            ui_templates.separator_box_in(box)

    return None




#    .oooooo.   oooo
#   d8P'  `Y8b  `888
#  888           888   .oooo.    .oooo.o  .oooo.o  .ooooo.   .oooo.o
#  888           888  `P  )88b  d88(  "8 d88(  "8 d88' `88b d88(  "8
#  888           888   .oP"888  `"Y88b.  `"Y88b.  888ooo888 `"Y88b.
#  `88b    ooo   888  d8(  888  o.  )88b o.  )88b 888    .o o.  )88b
#   `Y8bood8P'  o888o `Y888""8o 8""888P' 8""888P' `Y8bod8P' 8""888P'


classes = (
    
    SCATTER5_OT_impost_addonprefs,

    )


#if __name__ == "__main__":
#    register()