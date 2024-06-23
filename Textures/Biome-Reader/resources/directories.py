

# oooooooooo.    o8o                                   .                       o8o
# `888'   `Y8b   `"'                                 .o8                       `"'
#  888      888 oooo  oooo d8b  .ooooo.   .ooooo.  .o888oo  .ooooo.  oooo d8b oooo   .ooooo.   .oooo.o
#  888      888 `888  `888""8P d88' `88b d88' `"Y8   888   d88' `88b `888""8P `888  d88' `88b d88(  "8
#  888      888  888   888     888ooo888 888         888   888   888  888      888  888ooo888 `"Y88b.
#  888     d88'  888   888     888    .o 888   .o8   888 . 888   888  888      888  888    .o o.  )88b
# o888bood8P'   o888o d888b    `Y8bod8P' `Y8bod8P'   "888" `Y8bod8P' d888b    o888o `Y8bod8P' 8""888P'


import bpy, os 

# Addon Path (searching is relative from this file.)

addon_dir              = os.path.dirname(os.path.dirname(__file__))     # ../addons/{Addon Name}/
addon_resources        = os.path.join( addon_dir ,"resources")          # ../addons/{Addon Name}/resources/
addon_license_type     = os.path.join( addon_resources ,"license")      # ../addons/{Addon Name}/resources/license/
addon_icons            = os.path.join( addon_resources ,"icons")        # ../addons/{Addon Name}/resources/icons/
addon_dat_icons        = os.path.join( addon_resources ,"dat icons")    # ../addons/{Addon Name}/resources/dat icons/
addon_thumbnail        = os.path.join( addon_resources ,"thumbnail")    # ../addons/{Addon Name}/resources/thumbnail/
addon_translations     = os.path.join( addon_resources ,"translations") # ../addons/{Addon Name}/resources/translations/
addon_blends           = os.path.join( addon_dir ,"blends")             # ../addons/{Addon Name}/blends/
addon_engine_blend     = os.path.join( addon_blends,"engine.blend")     # ../addons/{Addon Name}/blends/engine.blend
addon_logo_blend       = os.path.join( addon_blends,"logo.blend")       # ../addons/{Addon Name}/blends/logo.blend
addon_vgmasks_blend    = os.path.join( addon_blends,"vgmasks.blend")    # ../addons/{Addon Name}/blends/vgmasks.blend
addon_visualizer_blend = os.path.join( addon_blends,"visualizer.blend") # ../addons/{Addon Name}/blends/visualizer.blend
addon_merge_blend      = os.path.join( addon_blends,"merge.blend")      # ../addons/{Addon Name}/blends/merge.blend
addon_masks            = os.path.join( addon_dir ,"masks")              # ../addons/{Addon Name}/masks/

# Native Blender Paths & added ../data/library

blender_version = bpy.utils.resource_path("USER")                  # ../Blender Foundation/Blender/2.9x/
blender_addons  = os.path.join(blender_version,"scripts","addons") # ../Blender Foundation/Blender/2.9x/scripts/addons/
blender_user    = os.path.dirname(blender_version)                 # ../Blender Foundation/Blender/
blender_data    = os.path.join(blender_user,"data")                # ../Blender Foundation/Blender/data/
lib_default     = os.path.join(blender_data,"scatter library")     # ../Blender Foundation/Blender/data/scatter library/  

# Library Path 
    
lib_library = lib_default                                   # ../scatter library/ 
lib_market  = os.path.join(lib_library,"_market_")          # ../scatter library/_market_/   
lib_userhas = os.path.join(lib_library,"_possessions_")     # ../scatter library/_possessions_/    
lib_biomes  = os.path.join(lib_library,"_biomes_")          # ../scatter library/_biomes_/   
lib_presets = os.path.join(lib_library,"_presets_")         # ../scatter library/_presets_/   
lib_prescat = os.path.join(lib_presets,"per_categories")    # ../scatter library/_presets_/per_categories/
lib_bitmaps = os.path.join(lib_library,"_bitmaps_")         # ../scatter library/_bitmaps_/    



#it will need to update library globals directly after properties are register to access addon_prefs.library_path
#everything is evaluated when import so we are forced to fire up  update_lib_directories() from properties register

def update_lib(): 
    """update global from  directories module with user custom addon_prefs.library_path"""

    new_lib_library = bpy.context.preferences.addons["Biome-Reader"].preferences.library_path                   
    new_lib_market  = os.path.join(new_lib_library,"_market_") 
    new_lib_userhas = os.path.join(new_lib_library,"_possessions_")
    new_lib_biomes  = os.path.join(new_lib_library,"_biomes_") 
    new_lib_presets = os.path.join(new_lib_library,"_presets_")      
    new_lib_bitmaps = os.path.join(new_lib_library,"_bitmaps_")  

    #if user path is wrong or structure not respected, use default path

    if (    (not os.path.exists(new_lib_library) ) 
         or (not os.path.exists(new_lib_biomes) )
         or (not os.path.exists(new_lib_presets) ) 
         or (not os.path.exists(new_lib_bitmaps) ) 
        ):
        print(f"Error, didn't found essential paths: [\n  '{new_lib_library}',\n  '{new_lib_biomes}',\n  '{new_lib_presets}',\n  '{new_lib_bitmaps}'\n] ")
        return None 

    #apply changes
    global lib_library, lib_market, lib_userhas, lib_biomes, lib_presets, lib_prescat, lib_bitmaps

    lib_library = new_lib_library        
    lib_market  = new_lib_market
    lib_userhas = new_lib_userhas
    lib_biomes  = new_lib_biomes
    lib_presets = new_lib_presets   
    lib_prescat = os.path.join(lib_presets,"per_categories")
    lib_bitmaps = new_lib_bitmaps   

    library_startup()

    return None 


# ooooo         o8o   .o8                                                     .oooooo..o     .                          .
# `888'         `"'  "888                                                    d8P'    `Y8   .o8                        .o8
#  888         oooo   888oooo.  oooo d8b  .oooo.   oooo d8b oooo    ooo      Y88bo.      .o888oo  .oooo.   oooo d8b .o888oo oooo  oooo  oo.ooooo.
#  888         `888   d88' `88b `888""8P `P  )88b  `888""8P  `88.  .8'        `"Y8888o.    888   `P  )88b  `888""8P   888   `888  `888   888' `88b
#  888          888   888   888  888      .oP"888   888       `88..8'             `"Y88b   888    .oP"888   888       888    888   888   888   888
#  888       o  888   888   888  888     d8(  888   888        `888'         oo     .d8P   888 . d8(  888   888       888 .  888   888   888   888
# o888ooooood8 o888o  `Y8bod8P' d888b    `Y888""8o d888b        .8'          8""88888P'    "888" `Y888""8o d888b      "888"  `V88V"V8P'  888bod8P'
#                                                           .o..P'                                                                       888
#                                                           `Y8P'                                                                       o888o


def library_startup():
    """Startup the library directories"""

    from pathlib import Path

    global blender_data, lib_default, lib_biomes, lib_market, lib_userhas, lib_presets, lib_bitmaps   
    for p in [ blender_data, lib_default, lib_biomes, lib_market, lib_userhas, lib_presets, lib_bitmaps]:
        if not os.path.exists(p): 
            Path(p).mkdir(parents=True, exist_ok=True)

    return None      



