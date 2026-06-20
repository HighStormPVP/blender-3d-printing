---
name: blender-3d-printing
description: >-
  Design 3D-printable models in Blender that will actually print well and survive
  real-world use. Use this skill whenever the user wants to model, design, or create
  something to be 3D printed — including FDM/resin prints, printable parts, STL/3MF
  export, "make this printable," fixing non-manifold/non-watertight meshes, wall
  thickness, supports, overhangs, tolerances for parts that fit together, multi-part
  assemblies, filament/material efficiency, slicing, or designing around hardware like
  bearings, magnets, screws, springs, or motors. Trigger this even when the user just
  says "model a [physical object]" or "I want to print a..." without saying the word
  "printable," because a model destined for a printer has very different requirements
  than a render-only model. Works through the Blender MCP (execute_blender_code,
  get_viewport_screenshot) when available.
---

# Designing for 3D Printing in Blender

## The core mindset

A model for 3D printing is **not** a model for rendering. A render only needs to *look*
right from a camera. A print becomes a **physical object** that:

- has real mass and consumes real filament/resin (money + time),
- is built up layer by layer by a machine with physical limits,
- will be picked up, snapped together, dropped, loaded, flexed, and worn,
- must obey gravity and physics while it prints *and* after.

So the goal is never "a pretty mesh." It is "a manifold, correctly-scaled, printable
solid that uses as little material as the job allows and holds up when someone uses it."
Keep that physical reality in mind at every step.

## Division of labor: Blender vs. the slicer

A huge source of mistakes is doing the slicer's job inside Blender. Be clear about who
owns what:

- **Blender owns geometry**: the outer/inner shape, wall thickness, holes, chamfers,
  tolerances, how parts mate, orientation features (flat bases, keys).
- **The slicer owns the print strategy**: infill pattern and density, support
  generation, perimeters, layer height, brims/rafts.

This matters for **filament efficiency**. Beginners try to model internal lattices to
"save plastic." Don't — that is exactly what slicer **infill** does, far better. Model
the part as a clean solid (or a clean hollow shell with drain holes for big parts) and
let the slicer fill it at, say, 15% gyroid. See `references/filament-efficiency.md`.

## Workflow

Follow this order. Don't skip the setup or the verification — most print failures are
caught there, not in the modeling.

1. **Understand the object physically.** Ask, if unclear: How big is it (real
   dimensions in mm)? Does it bear load, flex, or take impact? Does it fit onto or
   around something else (a shaft, a phone, a standard part)? Does it move? Knowing the
   forces tells you wall thickness, orientation, and where it may break.

2. **Set the scene to real units.** Work in millimeters with sane scale before modeling.
   Run `scripts/setup_scene.py` (via `execute_blender_code`). FDM nozzles are typically
   0.4 mm — features thinner than ~0.8 mm won't print reliably.

3. **Model as printable solids.** Build with manifold, watertight geometry. Prefer
   chamfers over fillets on downward overhangs (a 45° chamfer is self-supporting; a
   rounded overhang needs support). Keep walls ≥ 0.8–1.2 mm, more for structural parts.
   Avoid zero-thickness faces, intersecting/overlapping shells, and sub-nozzle detail.
   See `references/printability.md`.

4. **Decide orientation for strength and support.** Layer adhesion is the weak axis —
   orient the part so loads run *across* layers, not *along* the seam between them.
   Design a flat base for bed adhesion and minimize overhangs. See
   `references/printability.md`.

5. **Split into parts if needed.** If the model is larger than a typical build plate
   (~220–250 mm), has unavoidable steep overhangs, needs different orientations for
   strength, or must enclose hardware, split it into multiple parts with proper joints
   (pegs/holes, dovetails, screw bosses) and a clearance fit. **Put each separately-
   printed part in its own export file**, named clearly. See
   `references/assembly-and-hardware.md`.

6. **Verify printability — always.** Run `scripts/printability_check.py` to check for
   non-manifold edges, thin walls, bad normals, intersections, and overall dimensions,
   and take a `get_viewport_screenshot` to eyeball it. Fix issues before exporting. A
   mesh that isn't watertight will slice into garbage.

7. **Export.** Use `scripts/export_for_print.py` to export each part. Prefer **3MF**
   (carries real units and multiple objects cleanly); STL is the universal fallback.

8. **Offer to slice** (see mandatory ask below).

9. **Offer separate materials/hardware** only if the design needs them (see below).

## Two things to ALWAYS ask the user

These are explicit product requirements — don't forget them.

### 1. Offer to slice it

Once the model is exported and verified, **ask whether they want it sliced and ready to
print**, so they can go straight to the printer instead of slicing by hand. If yes,
you'll need their slicer (PrusaSlicer / OrcaSlicer / Cura / Bambu) and printer/filament
profile. See `references/slicing-and-export.md` for how to slice from the command line
and what to confirm first. If they don't have a slicer set up, just hand over the
STL/3MF and say it's ready to import.

### 2. Offer separate materials / hardware — only when the print genuinely needs it

Some designs are far better with a few non-printed parts: **bearings** (e.g. 608 skate
bearings), **rubber bands**, **magnets**, **screws / heat-set threaded inserts**,
**springs**, **motors** (e.g. NEMA 17, 28BYJ-28), shafts, etc. If — and only if — the
function realistically requires one (a spinner needs a bearing; a hinged lid may want a
magnet; a moving mechanism may need a motor), proactively ask the user whether they want
to incorporate it, and if so design the correct pocket/boss/clearance for that exact
part. **Do not bolt hardware onto things that don't need it** — a static figurine or a
bracket usually shouldn't ask for bearings. See `references/assembly-and-hardware.md`
for standard part dimensions and how to design the pockets.

## Reference files

Read the relevant one when you reach that part of the workflow:

- `references/printability.md` — manifold/watertight rules, wall thickness, overhangs &
  supports, bridging, tolerances/clearances, orientation for strength, common failures.
- `references/filament-efficiency.md` — solid vs. shell, when to hollow, drain holes,
  letting the slicer do infill, lightweighting big parts, chamfer-vs-fillet material
  cost.
- `references/assembly-and-hardware.md` — splitting models, joint types, clearance fits,
  and standard dimensions for bearings, magnets, screws, heat-set inserts, springs, and
  common motors.
- `references/slicing-and-export.md` — export formats, units, and command-line slicing
  with PrusaSlicer / OrcaSlicer / CuraEngine.

## Scripts (run via the Blender MCP `execute_blender_code`)

These are Blender Python. Read the file, then pass its contents to `execute_blender_code`
(adjust object names/paths as needed). They're written to be safe to re-run.

- `scripts/setup_scene.py` — set units to millimeters and a sane clip/grid scale.
- `scripts/printability_check.py` — enable Blender's 3D-Print Toolbox and report
  non-manifold edges, thin walls, overhangs, intersections, and bounding-box size in mm.
- `scripts/export_for_print.py` — select an object and export it as STL or 3MF at the
  correct scale.

When Blender MCP tools aren't available (you're only advising, not driving Blender),
use these files as the authoritative checklist and give the user the steps/Python to run
themselves.
