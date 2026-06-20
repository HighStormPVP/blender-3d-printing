"""Parametric generators for common 3D-printing features in Blender.

Run via the Blender MCP `execute_blender_code`. These build correctly-dimensioned
helper geometry so you don't reinvent bearing seats, screw bosses, nut traps, teardrop
holes, and snap-fits every time. All sizes are in millimeters and assume the scene is
set to mm (see setup_scene.py); they convert mm -> Blender units via scene.scale_length.

Typical use:
    boss = screw_boss("m3_boss", outer_d=8, pilot_d=2.5, height=10)   # add material
    cut  = bearing_seat_cutter("seat", od=22, depth=7, bore=16)       # remove material
    boolean_cut(my_part, cut)                                          # subtract cutter
    boolean_union(my_part, boss)                                       # join boss

Clearances follow references/printability.md and assembly-and-hardware.md. Confirm exact
hardware dimensions with the user — defaults here are common values, not universal.
"""
import bpy
import math

def _mm(v):
    """Convert millimeters to Blender units for the current scene scale."""
    sl = bpy.context.scene.unit_settings.scale_length or 1.0
    return v / 1000.0 / sl

def _new_cylinder(name, dia_mm, height_mm, verts=64, location=(0, 0, 0)):
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=verts, radius=_mm(dia_mm) / 2.0, depth=_mm(height_mm),
        location=(_mm(location[0]), _mm(location[1]), _mm(location[2])))
    obj = bpy.context.active_object
    obj.name = name
    return obj

# --- cutters (boolean-subtract these to remove material) ----------------------------

def bearing_seat_cutter(name, od=22.0, depth=7.0, bore=0.0, drop_in=True):
    """A pocket for a bearing. od/depth = bearing outer dia/width.
    drop_in adds 0.25 mm so the bearing seats by hand; set False for a press fit.
    bore>0 adds a through-hole (e.g. shaft clearance) below the seat."""
    clr = 0.25 if drop_in else 0.0
    seat = _new_cylinder(name, od + 2 * clr, depth + 1.0, location=(0, 0, (depth) / 2.0))
    if bore > 0:
        hole = _new_cylinder(name + "_bore", bore, depth * 4, location=(0, 0, 0))
        boolean_union(seat, hole)
    return seat

def teardrop_hole_cutter(name, dia=8.0, length=20.0, clearance=0.3, axis='X'):
    """A horizontal hole that prints without support: a cylinder topped by a peak so the
    upper surface never exceeds 45 deg. Use for shafts/rods printed lying down."""
    d = dia + clearance
    cyl = _new_cylinder(name, d, length, location=(0, 0, 0))
    cyl.rotation_euler[0] = math.radians(90)  # lay along Y by default
    # peak: a box rotated 45 deg sitting on top of the bore
    bpy.ops.mesh.primitive_cube_add(size=_mm(d / math.sqrt(2)))
    peak = bpy.context.active_object
    peak.name = name + "_peak"
    peak.rotation_euler[1] = math.radians(45)
    peak.location[2] = _mm(d / 2.0)
    peak.scale[1] = length / (d / math.sqrt(2))
    boolean_union(cyl, peak)
    if axis == 'X':
        cyl.rotation_euler[2] = math.radians(90)
    return cyl

def nut_trap_cutter(name, across_flats=5.5, depth=2.6, clearance=0.2):
    """Hex pocket for a nut (M3 nut = 5.5 mm across flats, ~2.4 mm tall)."""
    # circumscribed-circle dia for a hex from across-flats: AF / cos(30)
    dia = (across_flats + clearance) / math.cos(math.radians(30))
    hexc = _new_cylinder(name, dia, depth + 0.4, verts=6, location=(0, 0, depth / 2.0))
    return hexc

def counterbore_cutter(name, head_d=5.5, head_h=3.0, shaft_d=3.4, shaft_len=20.0):
    """Cylindrical pocket for a socket-cap screw head + clearance shaft below it."""
    head = _new_cylinder(name, head_d + 0.3, head_h + 0.2, location=(0, 0, head_h / 2.0))
    shaft = _new_cylinder(name + "_shaft", shaft_d, shaft_len, location=(0, 0, -shaft_len / 2.0))
    boolean_union(head, shaft)
    return head

def countersink_cutter(name, head_d=6.0, shaft_d=3.4, shaft_len=20.0, angle=90.0):
    """Conical pocket for a flat-head (countersunk) screw. angle = included angle."""
    h = (head_d / 2.0) / math.tan(math.radians(angle / 2.0))
    bpy.ops.mesh.primitive_cone_add(
        vertices=64, radius1=_mm(head_d / 2.0 + 0.15), radius2=0,
        depth=_mm(h), location=(0, 0, _mm(-h / 2.0)))
    cone = bpy.context.active_object
    cone.name = name
    shaft = _new_cylinder(name + "_shaft", shaft_d, shaft_len, location=(0, 0, -h - shaft_len / 2.0))
    boolean_union(cone, shaft)
    return cone

# --- additive features (boolean-union these to add material) -------------------------

def screw_boss(name, outer_d=8.0, pilot_d=2.5, height=10.0):
    """A cylindrical post with a pilot hole for a self-tapping screw.
    Rule of thumb: outer_d ~= 2.5x screw dia, pilot ~= screw core dia."""
    boss = _new_cylinder(name, outer_d, height, location=(0, 0, height / 2.0))
    hole = _new_cylinder(name + "_pilot", pilot_d, height + 1.0, location=(0, 0, height / 2.0))
    boolean_cut(boss, hole)
    return boss

def heatset_boss(name, outer_d=6.0, insert_hole_d=4.0, depth=6.0, height=10.0):
    """Boss sized for a heat-set threaded insert (confirm hole dia from the insert spec;
    a common M3 insert wants ~4.0 mm). Strongest reusable threads in plastic."""
    boss = _new_cylinder(name, outer_d, height, location=(0, 0, height / 2.0))
    hole = _new_cylinder(name + "_insert", insert_hole_d, depth + 0.5,
                         location=(0, 0, height - depth / 2.0 + 0.25))
    boolean_cut(boss, hole)
    return boss

# --- boolean helpers ----------------------------------------------------------------

def boolean_cut(target, cutter, delete_cutter=True):
    _apply_boolean(target, cutter, 'DIFFERENCE', delete_cutter)

def boolean_union(target, other, delete_other=True):
    _apply_boolean(target, other, 'UNION', delete_other)

def _apply_boolean(target, tool, operation, delete_tool):
    mod = target.modifiers.new(name="bool_" + operation.lower(), type='BOOLEAN')
    mod.operation = operation
    mod.object = tool
    mod.solver = 'EXACT'
    bpy.context.view_layer.objects.active = target
    bpy.ops.object.modifier_apply(modifier=mod.name)
    if delete_tool:
        bpy.data.objects.remove(tool, do_unlink=True)
    # keep result watertight after the op
    _cleanup(target)

def _cleanup(obj):
    import bmesh
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=_mm(0.001))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(obj.data)
    bm.free()

print("generators loaded: bearing_seat_cutter, teardrop_hole_cutter, nut_trap_cutter, "
      "counterbore_cutter, countersink_cutter, screw_boss, heatset_boss, "
      "boolean_cut, boolean_union. All sizes in mm.")
