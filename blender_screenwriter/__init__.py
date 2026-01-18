bl_info = {
    "name": "Screenwriter",
    "author": "Li Zheng Yang",
    "version": (1, 0),
    "blender": (4, 0, 0),
    "location": "Text Editor > UI > Screenwriter",
    "description": " tools for screenwriting in Blender",
    "warning": "",
    "doc_url": "",
    "category": "Text Editor",
}

import bpy
from . import screenwriter_ops
from . import screenwriter_ui
from . import fountain_io
from . import screenwriter_scenes

def menu_func_import(self, context):
    self.layout.operator(fountain_io.SCREENWRITER_OT_import_fountain.bl_idname, text="Fountain (.fountain)")

def menu_func_export(self, context):
    self.layout.operator(fountain_io.SCREENWRITER_OT_export_fountain.bl_idname, text="Fountain (.fountain)")

modules = [
    screenwriter_ops,
    screenwriter_ui,
    fountain_io,
    screenwriter_scenes,
]

def register():
    for module in modules:
        module.register()
    
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)
    
    # Register load handler
    bpy.app.handlers.load_post.append(fountain_io.on_load_handler)

def unregister():
    if fountain_io.on_load_handler in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.remove(fountain_io.on_load_handler)
        
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)

    for module in modules:
        module.unregister()

if __name__ == "__main__":
    register()
