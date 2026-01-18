import bpy


def get_current_line(text):
    if not text:
        return None
    return text.lines[text.current_line_index]

def set_line_text(text, content):
    if not text:
        return
    text.lines[text.current_line_index].body = content

def clean_text(text_body):
    """Strip whitespace and surrounding parentheses"""
    body = text_body.strip()
    # Remove all leading '(' and trailing ')'
    body = body.lstrip("(").rstrip(")")
    return body.strip()

class SCREENWRITER_OT_format_header(bpy.types.Operator):
    """Format current line as Scene Header"""
    bl_idname = "screenwriter.format_header"
    bl_label = "Scene Header"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        text = context.edit_text
        if not text:
             return {'CANCELLED'}
        
        fix_view_settings(context)
        line = get_current_line(text)
        content = clean_text(line.body).upper()
        
        set_line_text(text, content)
        
        return {'FINISHED'}

class SCREENWRITER_OT_format_action(bpy.types.Operator):
    """Format current line as Action"""
    bl_idname = "screenwriter.format_action"
    bl_label = "Action"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        text = context.edit_text
        if not text: return {'CANCELLED'}
        
        fix_view_settings(context)
        line = get_current_line(text)
        content = clean_text(line.body)
        set_line_text(text, content)
        return {'FINISHED'}

class SCREENWRITER_OT_format_character(bpy.types.Operator):
    """Format current line as Character"""
    bl_idname = "screenwriter.format_character"
    bl_label = "Character"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        text = context.edit_text
        if not text: return {'CANCELLED'}
        
        fix_view_settings(context)
        line = get_current_line(text)
        # 22 spaces is roughly center for character in standard courier
        indent = " " * 22 
        content = indent + clean_text(line.body).upper()
        set_line_text(text, content)
        return {'FINISHED'}

def fix_view_settings(context):
    """Disable syntax highlighting for screenplay look"""
    try:
        # Try to access current space
        if context.space_data and context.space_data.type == 'TEXT_EDITOR':
            context.space_data.show_syntax_highlight = False
    except:
        pass # Better safe than sorry to avoid crash

class SCREENWRITER_OT_format_dialogue(bpy.types.Operator):
    """Format current line as Dialogue"""
    bl_idname = "screenwriter.format_dialogue"
    bl_label = "Dialogue"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        text = context.edit_text
        if not text: return {'CANCELLED'}
        
        fix_view_settings(context)
        line = get_current_line(text)
        # 10 spaces for dialogue
        indent = " " * 10 
        content = indent + clean_text(line.body)
        set_line_text(text, content)
        return {'FINISHED'}

class SCREENWRITER_OT_format_parenthetical(bpy.types.Operator):
    """Format current line as Parenthetical"""
    bl_idname = "screenwriter.format_parenthetical"
    bl_label = "Parenthetical"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        text = context.edit_text
        if not text: return {'CANCELLED'}
        
        fix_view_settings(context)
        line = get_current_line(text)
        content = clean_text(line.body)
        
        # Add parens
        content = "(" + content + ")"
            
        # 16 spaces for parenthetical
        indent = " " * 16
        set_line_text(text, indent + content)
        return {'FINISHED'}

class SCREENWRITER_OT_format_transition(bpy.types.Operator):
    """Format current line as Transition"""
    bl_idname = "screenwriter.format_transition"
    bl_label = "Transition"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        text = context.edit_text
        if not text: return {'CANCELLED'}
        
        fix_view_settings(context)
        line = get_current_line(text)
        
        # Transitions are uppercase and right-aligned (approx 42 spaces)
        indent = " " * 42
        content = indent + clean_text(line.body).upper()
        
        # Ensure it ends with TO:? Standard convention but maybe user wants freedom
        # Let's just enforce case and indent
        
        set_line_text(text, content)
        return {'FINISHED'}

classes = [
    SCREENWRITER_OT_format_header,
    SCREENWRITER_OT_format_action,
    SCREENWRITER_OT_format_character,
    SCREENWRITER_OT_format_dialogue,
    SCREENWRITER_OT_format_parenthetical,
    SCREENWRITER_OT_format_transition,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
