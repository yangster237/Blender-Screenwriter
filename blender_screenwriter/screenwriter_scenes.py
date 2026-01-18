import bpy
from . import fountain_io

class SCREENWRITER_OT_sync_scenes(bpy.types.Operator):
    """Create Blender Scenes from Script Headers"""
    bl_idname = "screenwriter.sync_scenes"
    bl_label = "Sync Scenes"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        text = getattr(context, "edit_text", None)
        if not text and hasattr(context, "space_data") and context.space_data.type == "TEXT_EDITOR":
             text = context.space_data.text
             
        if not text:
            self.report({'ERROR'}, "No active text.")
            return {'CANCELLED'}
            
        # Parse data
        elements = fountain_io.parse_fountain_elements(text.as_string())
        
        headers = [c for (t, c) in elements if t == "HEADER"]
        
        if not headers:
            self.report({'WARNING'}, "No scene headers found.")
            return {'CANCELLED'}

        created_count = 0
        existing_scenes = {s.name for s in bpy.data.scenes}
        
        for header in headers:
            # Sanitize name?
            scene_name = header.strip()
            # Max length for blender name is 63 chars usually
            scene_name = scene_name[:63]
            
            if scene_name not in existing_scenes:
                bpy.data.scenes.new(name=scene_name)
                created_count += 1
                existing_scenes.add(scene_name)
        
        self.report({'INFO'}, f"Synced: Created {created_count} new scenes.")
        return {'FINISHED'}

def register():
    bpy.utils.register_class(SCREENWRITER_OT_sync_scenes)

def unregister():
    bpy.utils.unregister_class(SCREENWRITER_OT_sync_scenes)
