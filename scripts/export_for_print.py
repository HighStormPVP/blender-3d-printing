"""Export a Blender object as a print-ready STL or 3MF at the correct mm scale.

Run via the Blender MCP `execute_blender_code`. Set OBJECT_NAME and OUTPUT_PATH.
Export ONE file per separately-printed part, each oriented for its own best print.

3MF is preferred (carries units + multiple objects); STL is the universal fallback.
"""
import bpy
import os

OBJECT_NAME = None                       # None => active object
OUTPUT_PATH = "//part.3mf"               # .3mf or .stl ; "//" = next to the .blend file
APPLY_TRANSFORMS = True                  # bake scale/rotation so export size is correct

obj = bpy.data.objects.get(OBJECT_NAME) if OBJECT_NAME else bpy.context.active_object
if obj is None or obj.type != 'MESH':
    raise RuntimeError("Select a mesh object (or set OBJECT_NAME) before running.")

bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.select_all(action='DESELECT')
obj.select_set(True)
bpy.context.view_layer.objects.active = obj

if APPLY_TRANSFORMS:
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

path = bpy.path.abspath(OUTPUT_PATH)
os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
ext = os.path.splitext(path)[1].lower()

if ext == ".stl":
    # Newer Blender (4.x) uses the unified exporter; older has export_mesh.stl.
    try:
        bpy.ops.wm.stl_export(filepath=path, export_selected_objects=True,
                              global_scale=1.0, apply_modifiers=True)
    except AttributeError:
        bpy.ops.export_mesh.stl(filepath=path, use_selection=True,
                                global_scale=1.0, use_mesh_modifiers=True)
elif ext == ".3mf":
    try:
        bpy.ops.wm.threemf_export(filepath=path, use_selection=True)
    except Exception:
        # Fall back to STL if the 3MF add-on isn't enabled.
        path = os.path.splitext(path)[0] + ".stl"
        try:
            bpy.ops.wm.stl_export(filepath=path, export_selected_objects=True)
        except AttributeError:
            bpy.ops.export_mesh.stl(filepath=path, use_selection=True)
        print("3MF exporter unavailable; exported STL instead.")
else:
    raise RuntimeError("OUTPUT_PATH must end in .stl or .3mf")

sl = bpy.context.scene.unit_settings.scale_length or 1.0
dims_mm = [d * sl * 1000.0 for d in obj.dimensions]
print(f"Exported '{obj.name}' -> {path}")
print(f"Size (mm): {dims_mm[0]:.2f} x {dims_mm[1]:.2f} x {dims_mm[2]:.2f}")
print("Next: offer to slice it (see references/slicing-and-export.md).")
