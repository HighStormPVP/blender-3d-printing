"""Export every top-level mesh object to its own print file.

Run via the Blender MCP `execute_blender_code`. Enforces the one-file-per-printed-part
rule: each separately-printed part gets its own correctly-named file at true mm scale.

Set OUTPUT_DIR and FORMAT. Object names become file names, so name your objects clearly
in Blender (e.g. "gripper_base", "jaw_left") before running.
"""
import bpy
import os
import re

OUTPUT_DIR = "//print_parts"   # "//" = next to the .blend file
FORMAT = "3mf"                 # "3mf" (preferred) or "stl"
ONLY_SELECTED = False          # True => export only selected objects

out_dir = bpy.path.abspath(OUTPUT_DIR)
os.makedirs(out_dir, exist_ok=True)

def safe(name):
    return re.sub(r'[^A-Za-z0-9_.-]+', '_', name).strip('_') or "part"

src = (bpy.context.selected_objects if ONLY_SELECTED else bpy.data.objects)
meshes = [o for o in src if o.type == 'MESH' and o.parent is None and not o.hide_render]
if not meshes:
    raise RuntimeError("No top-level mesh objects found to export.")

bpy.ops.object.mode_set(mode='OBJECT')
exported = []
for obj in meshes:
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    path = os.path.join(out_dir, f"{safe(obj.name)}.{FORMAT}")
    if FORMAT == "stl":
        try:
            bpy.ops.wm.stl_export(filepath=path, export_selected_objects=True, apply_modifiers=True)
        except AttributeError:
            bpy.ops.export_mesh.stl(filepath=path, use_selection=True, use_mesh_modifiers=True)
    else:
        try:
            bpy.ops.wm.threemf_export(filepath=path, use_selection=True)
        except Exception:
            path = os.path.splitext(path)[0] + ".stl"
            try:
                bpy.ops.wm.stl_export(filepath=path, export_selected_objects=True)
            except AttributeError:
                bpy.ops.export_mesh.stl(filepath=path, use_selection=True)
    exported.append(path)

print(f"Exported {len(exported)} part(s) to {out_dir}:")
for p in exported:
    print("  -", os.path.basename(p))
print("Next: offer to slice them (references/slicing-and-export.md).")
