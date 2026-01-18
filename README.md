# Blender Screenwriter

A comprehensive screenwriting tool for Blender 4.0+. Write standard screenplay format directly in Blender's Text Editor, import/export Fountain files, and sync your script to Blender Scenes.

**Author**: Zheng Yang

## Features

### 📝 Formatting Tools
Located in the **Text Editor > UI Sidebar > Screenwriter** panel:
*   **Scene Header**: Auto-uppercases and formats headers (INT./EXT.).
*   **Action**: Standard action formatting.
*   **Character**: Auto-centers (indents) and uppercases character names.
*   **Dialogue**: Formats dialogue blocks.
*   **Parenthetical**: Handles `(parentheticals)` correctly.
*   **Transition**: Right-aligns transitions (CUT TO:).

### 📄 Fountain Support
Full support for the `.fountain` screenplay format.
*   **Import**: Open or Drag-and-Drop a `.fountain` file. The addon automatically detects it and formats the text with visual indentation.
*   **Export**: Export your script as a clean `.fountain` file compatible with other screenwriting apps (Final Draft, Fade In, etc.).
*   **Save Fountain**: A dedicated button to overwrite your current `.fountain` file correctly.

### 🎬 Scene Sync
*   **Sync to Scenes**: Analyzes your script and automatically creates a massive amount of Blender Scenes (`bpy.data.scenes`) corresponding to your Scene Headers. Perfect for layout and storyboarding.

## Installation

1.  Download `blender_screenwriter.zip`.
2.  Open Blender.
3.  Go to **Edit > Preferences > Add-ons**.
4.  Click **Install...** and select the zip file.
5.  Check the box next to **Text Editor: Screenwriter** to enable it.

## Usage

1.  Open the **Text Editor** area.
2.  Create a new text block or open a `.fountain` file.
3.  Press `N` to open the sidebar and navigate to the **Screenwriter** tab.
4.  Use the buttons to format your lines.
5.  To sync scenes, click **Sync to Scenes**.
