"""Set up a Blender scene for 3D printing: real-world millimeter units and sane scale.

Run via the Blender MCP `execute_blender_code` (or paste into Blender's Python console).
Safe to re-run. Modeling in mm from the start avoids the classic "imported at 1000x or
0.001x scale" disaster, because STL is unitless.
"""
import bpy

scene = bpy.context.scene

# Work in millimeters.
scene.unit_settings.system = 'METRIC'
scene.unit_settings.length_unit = 'MILLIMETERS'
# 1 Blender unit == 1 mm keeps numbers intuitive and exports at true size.
scene.unit_settings.scale_length = 0.001

# Make the viewport comfortable at mm scale (clip planes + larger grid).
for area in bpy.context.screen.areas:
    if area.type == 'VIEW_3D':
        for space in area.spaces:
            if space.type == 'VIEW_3D':
                space.clip_start = 0.1 * 0.001   # 0.1 mm
                space.clip_end = 10000 * 0.001   # 10 m
                space.overlay.grid_scale = 0.001  # grid in mm

print("Scene set to METRIC / MILLIMETERS (1 BU = 1 mm). Model real dimensions directly, "
      "e.g. a 40 mm cube = 40 units.")
