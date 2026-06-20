"""Check a Blender object for 3D-print problems and print a readable report.

Run via the Blender MCP `execute_blender_code`. By default it checks the active object;
set OBJECT_NAME to target a specific one. Uses Blender's built-in 3D-Print Toolbox
(object_print3d_utils) for the heavy lifting and adds a bounding-box size report in mm.

Run this BEFORE exporting. A non-manifold / non-watertight mesh slices into garbage no
matter how good the slicer settings are.
"""
import bpy
import addon_utils
import bmesh

OBJECT_NAME = None          # None => active object
THIN_WALL_MM = 0.8          # flag walls thinner than this
OVERHANG_DEG = 45.0         # flag faces steeper than this from horizontal bed

# --- enable the 3D-Print Toolbox add-on (name varies slightly by version) -----------
enabled = False
for mod_name in ("object_print3d_utils", "print3d_toolbox", "bl_ext.blender_org.print3d_toolbox"):
    try:
        addon_utils.enable(mod_name, default_set=True, persistent=True)
        enabled = True
        break
    except Exception:
        continue

# --- pick the object ----------------------------------------------------------------
obj = bpy.data.objects.get(OBJECT_NAME) if OBJECT_NAME else bpy.context.active_object
if obj is None or obj.type != 'MESH':
    raise RuntimeError("Select a mesh object (or set OBJECT_NAME) before running.")

bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.select_all(action='DESELECT')
obj.select_set(True)
bpy.context.view_layer.objects.active = obj

print("=" * 60)
print(f"PRINTABILITY REPORT: {obj.name}")
print("=" * 60)

# --- dimensions in mm (scene scale_length maps BU -> meters; *1000 for mm) -----------
sl = bpy.context.scene.unit_settings.scale_length or 1.0
dims_mm = [d * sl * 1000.0 for d in obj.dimensions]
print(f"Bounding box (mm): {dims_mm[0]:.2f} x {dims_mm[1]:.2f} x {dims_mm[2]:.2f}")
if max(dims_mm) > 256:
    print("  ! Larger than a typical 256 mm build plate — consider splitting into parts.")
if max(dims_mm) < 1:
    print("  ! Suspiciously tiny — check scene units (should be mm). See setup_scene.py.")

# --- manifold / normals via bmesh (works regardless of add-on availability) ---------
bm = bmesh.new()
bm.from_mesh(obj.data)
non_manifold_edges = sum(1 for e in bm.edges if not e.is_manifold)
boundary_edges = sum(1 for e in bm.edges if e.is_boundary)
print(f"Non-manifold edges: {non_manifold_edges}")
print(f"Boundary (open) edges: {boundary_edges}")
if non_manifold_edges == 0 and boundary_edges == 0:
    print("  OK: mesh appears watertight/manifold.")
else:
    print("  ! NOT watertight. Fix before slicing: Select > All by Trait > Non Manifold; "
          "Merge by Distance; Mesh > Normals > Recalculate Outside.")

# --- overhang scan via bmesh (works even when the 3D-Print Toolbox is absent) --------
# A downward-facing face shallower than (90 - OVERHANG_DEG) from horizontal needs
# support. We exclude the base resting on the bed (lowest ~0.5 mm) so a flat bottom
# doesn't count as an overhang.
import math
bm.normal_update()
zmin = min((obj.matrix_world @ v.co).z for v in bm.verts)
cos_t = math.cos(math.radians(OVERHANG_DEG))
overhang_faces = 0
for f in bm.faces:
    if f.normal.z < -cos_t:
        cz = sum((obj.matrix_world @ v.co).z for v in f.verts) / len(f.verts)
        if (cz - zmin) > (0.5 / 1000.0 / sl):
            overhang_faces += 1
print(f"Downward overhang faces > {OVERHANG_DEG} deg (would need support): {overhang_faces}")
if overhang_faces == 0:
    print("  OK: prints base-down with no supports.")
else:
    print("  ! has overhangs — reorient, add chamfers, or plan on supports. Also check "
          "bed stability for tall/top-heavy shapes (brim). See printability.md.")
bm.free()

# --- 3D-Print Toolbox deep checks (thin walls, overhangs, intersections) ------------
# Note: on Blender 4.2+ the toolbox is an optional *extension*; if it isn't installed,
# scene.print_3d won't exist and these ops are skipped — the bmesh checks above still
# cover manifoldness and overhangs, which catch the great majority of print problems.
if enabled:
    try:
        s = bpy.context.scene.print_3d
        s.thickness_min = THIN_WALL_MM / 1000.0 / sl
        s.angle_overhang = OVERHANG_DEG
    except Exception:
        pass
    for op_name, label in (
        ("check_solid", "Solid/manifold"),
        ("check_intersect", "Self-intersections"),
        ("check_degenerate", "Degenerate faces (zero area/thickness)"),
        ("check_thick", f"Thin walls (< {THIN_WALL_MM} mm)"),
        ("check_overhang", f"Overhangs (> {OVERHANG_DEG} deg)"),
    ):
        try:
            getattr(bpy.ops.mesh, "print3d_" + op_name)()
            print(f"  ran check: {label} (see Toolbox 'Result' panel / counts above)")
        except Exception as e:
            print(f"  (skipped {label}: {e})")
    print("Tip: bpy.ops.mesh.print3d_clean_non_manifold() can auto-fix many issues.")
else:
    print("3D-Print Toolbox not available in this build; relied on bmesh checks above. "
          "Manually verify thin walls and overhangs.")

print("=" * 60)
print("Reminder: also take a get_viewport_screenshot and eyeball the part, and confirm "
      "orientation puts loads ACROSS layers, not along them.")
