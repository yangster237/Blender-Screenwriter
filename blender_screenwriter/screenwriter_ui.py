import bpy

class SCREENWRITER_PT_main_panel(bpy.types.Panel):
    """Creates a Panel in the Text Editor UI"""
    bl_label = "Screenwriter"
    bl_idname = "SCREENWRITER_PT_main_panel"
    bl_space_type = 'TEXT_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Screenwriter"

    def draw(self, context):
        layout = self.layout

        col = layout.column(align=True)
        col.operator("screenwriter.format_header", text="Scene Header")
        col.operator("screenwriter.format_action", text="Action")
        col.operator("screenwriter.format_character", text="Character")
        col.operator("screenwriter.format_dialogue", text="Dialogue")
        col.operator("screenwriter.format_parenthetical", text="Parenthetical")
        col.operator("screenwriter.format_transition", text="Transition")

        col.separator()
        col.operator("screenwriter.save_fountain", text="Save Fountain", icon="FILE_TICK")
        col.operator("screenwriter.format_fountain", text="Format Text as Fountain", icon="FILE_REFRESH")
        
        col.separator()
        col.operator("screenwriter.sync_scenes", text="Sync to Scenes", icon="SCENE_DATA")
        
        row = layout.row(align=True)

        row.operator("screenwriter.import_fountain", text="Import")
        row.operator("screenwriter.export_fountain", text="Export")

def register():
    bpy.utils.register_class(SCREENWRITER_PT_main_panel)

def unregister():
    bpy.utils.unregister_class(SCREENWRITER_PT_main_panel)
