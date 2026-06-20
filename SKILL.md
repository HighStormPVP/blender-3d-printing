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

### Prefer a single, filament-only print

The best result is almost always **one part (or a few printed parts) made entirely of
filament, with no separate hardware** — nothing to source, nothing to assemble, nothing
that can be the wrong size. Default to that. A model that prints in one piece and just
works is better than a clever one that needs a bearing, a screw, and a magnet from a
shop.

Only introduce separate materials/hardware (bearings, magnets, screws, springs, motors)
when the function genuinely cannot be achieved in filament alone — e.g. a part that must
spin freely under load really does want a bearing; a strong reusable thread really does
want a heat-set insert. Even then, prefer printed alternatives first (print-in-place
hinges, printed snap-fits, printed living hinges, printed threads) where they'd do the
job. When in doubt: filament only.

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

## Start here: settle the design before touching Blender

When the user asks for something open-ended — "make me a 3D print for a fidget toy,"
"I want to print a planter," "design me a phone stand" — **don't jump straight into
Blender.** You don't yet know what they actually want, and modeling the wrong thing
wastes everyone's time. First settle *what* you're building, with a quick branch:

> "Would you like to describe one you have in mind, or would you like me to come up with
> a few ideas for you?"

Then:

- **They describe it** → great. Ask only the gaps you still need (rough size, where it's
  used, any moving/functional parts), keeping the filament-only default in mind, then
  proceed.
- **They want ideas** → propose a few concrete, printable options (2–4), each a sentence
  or two on what it is and why it prints well. When they pick one (or remix), lock that
  as the design.

**Only once the design is settled** — they've fully described it, or accepted/adapted one
of your ideas — connect to the Blender MCP and start building. At that point: check the
Blender version, run the workflow below (set units → model → estimate → verify → export
→ slice/handoff). If the MCP isn't connected yet, that's the moment to walk them through
connecting it (see the version section for the right, version-accurate steps).

Skip the brainstorm only when the user has *already* given a complete, unambiguous spec —
then confirm you've got it and go.

## Check the Blender version first — give version-accurate instructions

Blender's menus, operator names, and add-on UI change between versions, so generic
instructions are often wrong. Before guiding the user through anything UI-related (or
relying on a specific operator), find out which version they're running and tailor your
instructions to it:

- If the Blender MCP is connected, query it directly:
  `import bpy; print(bpy.app.version_string)` via `execute_blender_code`.
- If it's not connected yet (e.g. you're helping them install the addon), ask, or have
  them check **Help → About Blender** (the splash screen also shows it).

Then phrase instructions for *their* version. Examples that differ:
- **Add-on install:** Blender **4.2+** → Preferences → Add-ons → the **▾ dropdown
  (top-right) → "Install from Disk…"**. Blender **3.x–4.1** → Preferences → Add-ons →
  **"Install…"** button at the top.
- **Sidebar:** hover the mouse **over the 3D viewport**, then press **N** (the key does
  nothing if the cursor is over another editor).
- **Exporters:** 4.x uses the unified `bpy.ops.wm.stl_export` / `wm.threemf_export`;
  older builds use `bpy.ops.export_mesh.stl`. The bundled scripts already try both, but
  mention the right one if you hand-write steps.

When unsure what a given version calls something, check rather than guess.

## Workflow

Follow this order. Don't skip the setup or the verification — most print failures are
caught there, not in the modeling.

1. **Understand the object physically.** Ask, if unclear: How big is it (real
   dimensions in mm)? Does it bear load, flex, or take impact? Does it fit onto or
   around something else (a shaft, a phone, a standard part)? Does it move? Will it see
   heat, sun, or outdoors? Knowing the forces tells you wall thickness, orientation,
   where it may break, and which **material** to recommend (see
   `references/materials.md` — heat/outdoors/load/flex are the four questions that pick
   it). For **resin (MSLA/SLA)** prints the rules differ — read
   `references/resin-printing.md`.

2. **Set the scene to real units.** Work in millimeters with sane scale before modeling.
   Run `scripts/setup_scene.py` (via `execute_blender_code`). FDM nozzles are typically
   0.4 mm — features thinner than ~0.8 mm won't print reliably.

3. **Model as printable solids.** Build with manifold, watertight geometry. Prefer
   chamfers over fillets on downward overhangs (a 45° chamfer is self-supporting; a
   rounded overhang needs support). Keep walls ≥ 0.8–1.2 mm, more for structural parts.
   Avoid zero-thickness faces, intersecting/overlapping shells, and sub-nozzle detail.
   See `references/printability.md`.

4. **Decide orientation for strength, support, and bed stability.** Layer adhesion is
   the weak axis — orient the part so loads run *across* layers, not *along* the seam
   between them. Design a flat base for bed adhesion and minimize overhangs. Also think
   about **stability while printing**: tall, narrow, top-heavy, or cantilevered shapes
   can tip over or be knocked off the bed by the print head — they need a broad base, or
   supports plus a brim to brace them (the slicer generates the supports; you design so
   they're feasible and you flag them). See `references/printability.md` for the 45°
   rule, support types (lattice vs. tree), and stability.

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

7. **Quantify the material cost.** Run `scripts/estimate_filament.py` to report the
   part's volume and its mass/cost across infill levels. This turns the
   filament-efficiency goal into real numbers and helps you recommend an infill.

8. **Export.** Use `scripts/export_for_print.py` for a single part, or
   `scripts/export_all_parts.py` to export every part to its own correctly-named file.
   Prefer **3MF** (carries real units and multiple objects cleanly); STL is the
   universal fallback.

9. **Offer to slice** (see mandatory ask below).

10. **Offer separate materials/hardware** only if the design needs them (see below).

11. **Hand off clearly.** Give the user a concise print summary (files, material,
    infill, orientation, supports, est. material, assembly order) using
    `references/handoff-template.md` so they can print without re-reading the chat.

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

**The default is filament-only** (see "Prefer a single, filament-only print" above) —
most prints should need no hardware at all, and that's the better outcome. Don't reach
for hardware unless the function truly requires it.

Some designs *are* genuinely better with a few non-printed parts: **bearings** (e.g. 608
skate bearings), **rubber bands**, **magnets**, **screws / heat-set threaded inserts**,
**springs**, **motors** (e.g. NEMA 17, 28BYJ-48), shafts, etc. If — and only if — the
function realistically requires one (a spinner needs a bearing; a hinged lid may want a
magnet; a moving mechanism may need a motor), and a printed alternative won't do,
proactively ask the user whether they want to incorporate it, and if so design the
correct pocket/boss/clearance for that exact part. **Do not bolt hardware onto things
that don't need it** — a static figurine or a wall bracket should print in filament
alone. See `references/assembly-and-hardware.md` for standard part dimensions and how to
design the pockets.

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
- `references/materials.md` — choosing PLA/PETG/ABS/TPU/Nylon/PC from the part's job, and
  how material choice changes walls, tolerances, and features.
- `references/resin-printing.md` — how MSLA/SLA differs from FDM: hollowing, drain/vent
  holes, orientation, no infill.
- `references/slicing-and-export.md` — export formats, units, and command-line slicing
  with PrusaSlicer / OrcaSlicer / CuraEngine.
- `references/handoff-template.md` — the print-ready summary to give the user at the end.

## Scripts (run via the Blender MCP `execute_blender_code`)

These are Blender Python. Read the file, then pass its contents to `execute_blender_code`
(adjust object names/paths as needed). They're written to be safe to re-run.

- `scripts/setup_scene.py` — set units to millimeters and a sane clip/grid scale.
- `scripts/printability_check.py` — enable Blender's 3D-Print Toolbox and report
  non-manifold edges, thin walls, overhangs, intersections, and bounding-box size in mm.
- `scripts/generators.py` — parametric feature library: bearing seats, screw/heat-set
  bosses, nut traps, teardrop holes, counterbores/countersinks, plus boolean helpers.
- `scripts/estimate_filament.py` — report mesh volume and mass/cost across infill levels.
- `scripts/export_for_print.py` — export one object as STL or 3MF at correct scale.
- `scripts/export_all_parts.py` — export every top-level part to its own named file.

When Blender MCP tools aren't available (you're only advising, not driving Blender),
use these files as the authoritative checklist and give the user the steps/Python to run
themselves.
