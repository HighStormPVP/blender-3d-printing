# Printability rules

This is the make-or-break reference. A model can look perfect and still slice into
nonsense if the geometry isn't physically valid. Work through these whenever you model
or fix a part destined for a printer.

## 1. Manifold / watertight geometry (the #1 rule)

Slicers turn a mesh into solid layers by asking, for every point, "am I inside the
object or outside?" That question only has an answer if the surface is a single, closed,
watertight shell — **manifold**. If it isn't, the slicer guesses, and you get missing
walls, blobs, or nothing.

A manifold mesh has:
- **No holes** — every edge is shared by exactly two faces (no boundary edges).
- **No non-manifold edges** — no edge shared by 3+ faces.
- **No internal faces** or stray geometry inside the shell.
- **Consistent outward-facing normals** — no flipped faces.
- **No self-intersections** — shells must not pass through themselves. This is the most
  common problem after a Boolean: clean it up, don't ship overlapping geometry.

How to fix in Blender:
- Select → All by Trait → Non Manifold (Edit Mode) to find problems.
- Mesh → Normals → Recalculate Outside (Shift+N) to fix flipped faces.
- Merge by Distance to weld duplicate/loose verts.
- Use the **3D-Print Toolbox** add-on (`object_print3d_utils`) — its "Check All" reports
  non-manifold, thin walls, sharp/overhang faces, and intersections, and it has
  one-click cleanup. `scripts/printability_check.py` enables and runs it.
- After Booleans: apply the modifier, then Merge by Distance + Recalculate Normals, and
  re-check for intersections.

## 2. Scale and units

Always work in **millimeters**. STL files are unitless — a model authored at Blender's
default scale can import as a 1-meter monster or a 1-mm speck. Set the scene to mm
(`scripts/setup_scene.py`) and state real target dimensions up front. Sanity-check the
bounding box before export.

## 3. Wall thickness and minimum feature size

The nozzle (commonly 0.4 mm) sets the floor on detail:

- **Minimum wall:** ~0.8 mm (2 perimeters). Below this the slicer may drop the wall
  entirely.
- **Structural / load-bearing walls:** 1.6–3 mm or more.
- **Minimum embossed/engraved detail:** ≥ 0.4 mm wide and deep, or it vanishes.
- **Pins/pegs:** avoid < 2 mm diameter — they print weak and snap.
- **Resin printing** allows finer detail (walls ~0.5 mm) but still needs thought about
  cure-strength and drain holes for hollows.

## 4. Overhangs, supports, and bridging

The printer lays plastic onto the layer below. With nothing beneath, it droops.

- **45° rule:** overhangs up to ~45° from vertical print cleanly unsupported. Steeper
  needs support or redesign.
- **Prefer chamfers over fillets on downward-facing edges.** A 45° chamfer under an
  overhang is self-supporting and uses less material than a rounded fillet that still
  needs support. (Top-facing edges can be filleted freely.)
- **Bridging:** flat spans between two supports print okay up to ~5–10 mm; longer sags.
- **Teardrop horizontal holes:** a circular horizontal hole has a 90° overhang at its
  top and prints messy. Making the top a teardrop/peak keeps it self-supporting.
- **Design supports away, not in.** The best support is geometry that doesn't need any —
  reorient or chamfer first; leave the rest to the slicer.

## 5. Bed adhesion / first layer

- Give the part a **flat base** with meaningful contact area. Tiny contact points peel
  off the bed mid-print.
- Avoid sharp pointed bottoms; add a small flat or a deliberate brim-friendly base.

## 6. Tolerances and clearances (parts that fit together)

FDM is not dimensionally perfect; holes shrink, outer dims grow slightly. Build in gaps:

- **Loose / sliding fit:** ~0.4–0.5 mm total clearance (0.2–0.25 mm per side).
- **Snug / press fit:** ~0.1–0.2 mm.
- **Threaded inserts / hardware:** size the hole to the part spec (see
  `assembly-and-hardware.md`).
- When unsure, leave 0.3 mm and tell the user it may need a test fit — tolerances vary
  by printer and filament.

## 7. Orientation for strength

Layer-to-layer adhesion is the **weakest** direction of an FDM part — it splits along
layer lines like wood splits along the grain. So:

- Orient the part so the **main load runs across layers (in-plane), not along the print
  Z seam**. A hook printed lying down is far stronger than one printed standing up.
- Long thin features are weakest if printed standing vertically.
- Tell the slicer-facing user the recommended print orientation; it's a real design
  decision, not an afterthought.

## 8. Common failure checklist (run before export)

- [ ] Watertight / manifold (no non-manifold edges, no holes)
- [ ] Normals all point outward
- [ ] No self-intersecting / overlapping shells (post-Boolean cleanup done)
- [ ] All walls ≥ ~0.8 mm (structural ones thicker)
- [ ] No overhangs > 45° that aren't intended to need support
- [ ] Flat, adequate base for bed adhesion
- [ ] Clearances added to mating surfaces
- [ ] Correct scale in mm (bounding box sanity-checked)
- [ ] Sensible print orientation chosen for strength
