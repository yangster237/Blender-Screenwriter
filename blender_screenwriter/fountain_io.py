import bpy
import os
from bpy_extras.io_utils import ImportHelper, ExportHelper

def is_scene_header(line):
    s = line.strip()
    return s.startswith(("INT.", "EXT.", "INT ", "EXT ", "EST.", ". ", "I/E"))

def is_character(line):
    # Basic heuristic: Uppercase and not a scene header
    s = line.strip()
    return s.isupper() and not is_scene_header(s)

def is_parenthetical(line):
    s = line.strip()
    return s.startswith("(") and s.endswith(")")

def is_transition(line):
    s = line.strip()
    # Forced transition or standard "TO:" ending
    if s.startswith(">"): return True
    return s.isupper() and s.endswith("TO:")

class SCREENWRITER_OT_export_fountain(bpy.types.Operator, ExportHelper):
    """Export current text to Fountain"""
    bl_idname = "screenwriter.export_fountain"
    bl_label = "Export Fountain"
    filename_ext = ".fountain"

    filter_glob: bpy.props.StringProperty(
        default="*.fountain",
        options={'HIDDEN'},
        maxlen=255,
    )

    def execute(self, context):
        text = getattr(context, "edit_text", None)
        
        # Fallback: Find first text editor with open text
        if not text:
            for area in context.screen.areas:
                if area.type == 'TEXT_EDITOR':
                    if area.spaces.active.text:
                        text = area.spaces.active.text
                        break
        
        if not text:
            # Fallback 2: Any text?
            if len(bpy.data.texts) > 0:
                 text = bpy.data.texts[0]
        
        if not text:
            self.report({'ERROR'}, "No text file found to export.")
            return {'CANCELLED'}

        content = ""
        for line in text.lines:
            # For export, we primarily just strip the indentation we added
            # Fountain format is remarkably resilient.
            # "                      HERO" -> "HERO" (Valid Character)
            # "          (beat)" -> "(beat)" (Valid Parenthetical)
            content += line.body.strip() + "\n"

        with open(self.filepath, 'w', encoding='utf-8') as f:
            f.write(content)
            
        self.report({'INFO'}, "Exported to " + self.filepath)
        return {'FINISHED'}

class SCREENWRITER_OT_import_fountain(bpy.types.Operator, ImportHelper):
    """Import Fountain file"""
    bl_idname = "screenwriter.import_fountain"
    bl_label = "Import Fountain"
    filename_ext = ".fountain"

    filter_glob: bpy.props.StringProperty(
        default="*.fountain",
        options={'HIDDEN'},
        maxlen=255,
    )

    def execute(self, context):
        with open(self.filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        text_name = os.path.basename(self.filepath)
        text = bpy.data.texts.new(name=text_name)
        
        # Try to switch view to new text
        if hasattr(context, "space_data") and context.space_data.type == 'TEXT_EDITOR':
             context.space_data.text = text
        else:
             for area in context.screen.areas:
                if area.type == 'TEXT_EDITOR':
                    area.spaces.active.text = text
                    break
        
        text.write("".join(lines)) # Write raw first, then format
        
        # Link the file to the text block for saving
        text.filepath = self.filepath
        
        # Format it
        format_text_block(text)
        text["screenwriter_init"] = True
        
        return {'FINISHED'}

def parse_fountain_elements(raw_content):
    """
    Parses raw text into a list of (type, content) tuples.
    Types: HEADER, ACTION, CHARACTER, DIALOGUE, PARENTHETICAL, TRANSITION
    """
    lines = raw_content.splitlines()
    elements = []
    
    if not lines: return elements

    for i, raw_line in enumerate(lines):
        line = raw_line.strip()
        
        if not line:
            continue
            
        # Context checks
        prev_line_empty = True
        if i > 0:
            prev_line_empty = (lines[i-1].strip() == "")
            
        element_type = "ACTION"
        content = line
        
        if is_scene_header(line):
            element_type = "HEADER"
            
        elif is_transition(line):
             element_type = "TRANSITION"
             if line.startswith(">"):
                 content = line[1:].strip()
                 
        elif is_character(line) and prev_line_empty:
            element_type = "CHARACTER"
            
        elif is_parenthetical(line):
            element_type = "PARENTHETICAL"
            
        else:
            # Dialogue Check
            is_dialogue = False
            if i > 0 and not prev_line_empty:
                prev_line = lines[i-1].strip()
                prev_prev_empty = True
                if i > 1:
                    prev_prev_empty = (lines[i-2].strip() == "")
                
                prev_is_char = is_character(prev_line) and prev_prev_empty
                prev_is_paren = is_parenthetical(prev_line)
                
                if prev_is_char or prev_is_paren:
                    is_dialogue = True
            
            if is_dialogue:
                 element_type = "DIALOGUE"
        
        elements.append( (element_type, content) )
        
    return elements

def format_text_block(text):
    """Parses the text block content as Fountain and applies visual formatting"""
    raw_content = text.as_string()
    lines = raw_content.splitlines()
    
    if not lines: return

    new_content = ""
    
    # We need to look behind, so we iterate by index
    for i, raw_line in enumerate(lines):
        line = raw_line.strip()
        
        if not line:
            new_content += "\n"
            continue
            
        # Context checks
        prev_line_empty = True
        if i > 0:
            prev_line_empty = (lines[i-1].strip() == "")
            
        indent = ""
        
        # 1. Scene Header: Always wins
        if is_scene_header(line):
            indent = ""
            
        # 2. Transition: Forced > or uppercase ending in TO: and preceded by empty line
        elif is_transition(line):
             # Logic: If it starts with > it's definitely a transition (strip it)
             # If it ends with TO: it should probably be preceded by empty line to be safe, 
             # but we'll accept it for now.
             indent = " " * 42
             if line.startswith(">"):
                 line = line[1:].strip()
                 
        # 3. Character: Uppercase, NOT a header/transition, and PRECEDED BY EMPTY LINE
        elif is_character(line) and prev_line_empty:
            indent = " " * 22
            
        # 4. Parenthetical: Wrapped in ()
        elif is_parenthetical(line):
            indent = " " * 16
            
        # 5. Dialogue: If previous line was Character or Parenthetical?
        else:
            # Complex Dialogue Check
            is_dialogue = False
            if i > 0 and not prev_line_empty:
                prev_line = lines[i-1].strip()
                
                # Was prev line a Character? (Uppercase, preceded by empty line [check i-2])
                prev_prev_empty = True
                if i > 1:
                    prev_prev_empty = (lines[i-2].strip() == "")
                
                prev_is_char = is_character(prev_line) and prev_prev_empty
                prev_is_paren = is_parenthetical(prev_line)
                
                if prev_is_char or prev_is_paren:
                    is_dialogue = True
            
            if is_dialogue:
                indent = " " * 10
            else:
                indent = "" # Action
        
        new_content += indent + line + "\n"
        
    text.clear()
    text.write(new_content)
    
    # Disable syntax highlight
    if hasattr(text, "use_syntax_highlight"): # Older blender
         text.use_syntax_highlight = False

def on_load_handler(dummy):
    """Event handler for when a .blend file is opened"""
    for text in bpy.data.texts:
        is_fountain = text.name.lower().endswith(".fountain")
        if text.filepath:
            is_fountain = is_fountain or text.filepath.lower().endswith(".fountain")
            
        if is_fountain and not text.get("screenwriter_init"):
            format_text_block(text)
            text["screenwriter_init"] = True

class SCREENWRITER_OT_format_fountain(bpy.types.Operator):
    """Format current text as Fountain (Manual Trigger)"""
    bl_idname = "screenwriter.format_fountain"
    bl_label = "Format as Fountain"

    def execute(self, context):
        text = getattr(context, "edit_text", None)
        if not text and hasattr(context, "space_data") and context.space_data.type == "TEXT_EDITOR":
             text = context.space_data.text
             
        if not text:
            self.report({'ERROR'}, "No active text.")
            return {'CANCELLED'}
            
        format_text_block(text)
        text["screenwriter_init"] = True
        return {'FINISHED'}

class SCREENWRITER_OT_save_fountain(bpy.types.Operator):
    """Save current text as Fountain (Overwrites file)"""
    bl_idname = "screenwriter.save_fountain"
    bl_label = "Save Fountain"

    def execute(self, context):
        text = getattr(context, "edit_text", None)
        if not text and hasattr(context, "space_data") and context.space_data.type == "TEXT_EDITOR":
             text = context.space_data.text
        
        if not text:
            self.report({'ERROR'}, "No active text to save.")
            return {'CANCELLED'}
            
        if not text.filepath:
            # If no file linked, trigger "Export" (Save As)
            return bpy.ops.screenwriter.export_fountain('INVOKE_DEFAULT')
            
        # Write File
        content = ""
        for line in text.lines:
            content += line.body.strip() + "\n"

        try:
            with open(text.filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            self.report({'INFO'}, f"Saved to {text.filepath}")
            text.is_dirty = False
        except Exception as e:
            self.report({'ERROR'}, f"Failed to save: {str(e)}")
            return {'CANCELLED'}
            
        return {'FINISHED'}

classes = [
    SCREENWRITER_OT_export_fountain,
    SCREENWRITER_OT_import_fountain,
    SCREENWRITER_OT_save_fountain,
    SCREENWRITER_OT_format_fountain,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
