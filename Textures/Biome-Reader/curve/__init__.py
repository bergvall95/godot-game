
#####################################################################################################
#   .oooooo.
#  d8P'  `Y8b
# 888          oooo  oooo  oooo d8b oooo    ooo  .ooooo.
# 888          `888  `888  `888""8P  `88.  .8'  d88' `88b
# 888           888   888   888       `88..8'   888ooo888
# `88b    ooo   888   888   888        `888'    888    .o
#  `Y8bood8P'   `V88V"V8P' d888b        `8'     `Y8bod8P'
#
#####################################################################################################


import bpy

from . import fallremap


#   ooooooooo.
#   `888   `Y88.
#    888   .d88'  .ooooo.   .oooooooo
#    888ooo88P'  d88' `88b 888' `88b
#    888`88b.    888ooo888 888   888
#    888  `88b.  888    .o `88bod8P'
#   o888o  o888o `Y8bod8P' `8oooooo.
#                          d"     YD
#                          "Y88888P'


classes = []
classes += fallremap.classes


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    


#if __name__ == "__main__":
#    register()