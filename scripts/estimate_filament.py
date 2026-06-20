"""Estimate filament usage and cost for a Blender object.

Run via the Blender MCP `execute_blender_code`. Reports the solid (envelope) volume of
the mesh, then mass and cost at a range of infill densities so the user can make the
strength-vs-material trade-off with real numbers — which is the whole point of the
filament-efficiency goal.

The infill numbers are ESTIMATES. Actual usage depends on perimeters, top/bottom layers,
supports, and the slicer's infill pattern. For a precise figure, slice the file and read
the slicer's report (see references/slicing-and-export.md). This is for quick
in-Blender comparison.
"""
import bpy
import bmesh

OBJECT_NAME = None          # None => active object
DENSITY_G_CM3 = 1.24        # PLA ~1.24, PETG ~1.27, ABS ~1.04, TPU ~1.21, Nylon ~1.14
PRICE_PER_KG = 25.0         # your filament price (same currency out as in)
SHELL_FRACTION = 0.20       # rough share of volume taken by perimeters + top/bottom skins
INFILLS = [0.10, 0.15, 0.20, 0.30, 0.50, 1.00]

obj = bpy.data.objects.get(OBJECT_NAME) if OBJECT_NAME else bpy.context.active_object
if obj is None or obj.type != 'MESH':
    raise RuntimeError("Select a mesh object (or set OBJECT_NAME) before running.")

# Mesh volume in Blender units^3, then convert to real cm^3 using the scene scale.
depsgraph = bpy.context.evaluated_depsgraph_get()
mesh = obj.evaluated_get(depsgraph).to_mesh()
bm = bmesh.new()
bm.from_mesh(mesh)
bm.transform(obj.matrix_world)
vol_bu3 = bm.calc_volume(signed=False)
bm.free()
obj.evaluated_get(depsgraph).to_mesh_clear()

sl = bpy.context.scene.unit_settings.scale_length or 1.0   # BU -> meters
vol_m3 = vol_bu3 * (sl ** 3)
vol_cm3 = vol_m3 * 1_000_000.0

print("=" * 60)
print(f"FILAMENT ESTIMATE: {obj.name}")
print("=" * 60)
print(f"Solid volume: {vol_cm3:.2f} cm^3  ({vol_cm3/1000:.3f} L)")
print(f"Density: {DENSITY_G_CM3} g/cm^3   Price: {PRICE_PER_KG}/kg")
print("-" * 60)
print(f"{'infill':>8} | {'~grams':>8} | {'~cost':>8}   (estimate, +{int(SHELL_FRACTION*100)}% shell)")
print("-" * 60)
for inf in INFILLS:
    # plastic fraction ~= shell + infill over the hollow interior, capped at solid.
    frac = min(1.0, SHELL_FRACTION + inf * (1.0 - SHELL_FRACTION))
    grams = vol_cm3 * DENSITY_G_CM3 * frac
    cost = grams / 1000.0 * PRICE_PER_KG
    flag = "  <- decorative" if inf <= 0.10 else ("  <- general" if inf <= 0.20 else
           ("  <- functional" if inf < 1.0 else "  <- max/solid"))
    print(f"{inf*100:6.0f}%  | {grams:7.1f}g | {cost:7.2f}{flag}")
print("-" * 60)
print("For an exact figure, slice the exported file and read its filament report.")
