# Filament / material efficiency

Filament costs money and print time scales with material. The goal is to use the least
material the job allows **without** weakening the part below what its real-world use
demands. Strength and economy are a trade-off — make it deliberately, with the user's
use case in mind.

## The golden rule: let the slicer do infill

The single biggest efficiency lever is **not modeled in Blender at all** — it's the
slicer's **infill**. A part modeled as a clean solid and sliced at 15–20% gyroid infill
is already mostly hollow inside, with an efficient internal lattice that the slicer
generates and supports automatically.

So: **do not hand-model internal honeycombs, ribs, or lattices to "save plastic."**
You'll spend effort building fragile geometry that the slicer does better and stronger.
Model the clean outer (and where relevant inner) shape; pick infill at slice time.

Typical infill guidance to pass to the user:
- Decorative / non-load: 5–10%
- General parts: 15–20%
- Functional / moderate load: 30–50%
- High-stress / mechanical: 50–100% or solid walls + thick perimeters

## When to actually model it hollow

For **large** parts, modeling a hollow shell *does* help, because even low infill across
a big solid volume adds up. This is the user's "big parts hollow but still supported
inside" case. Do it like this:

1. Give the part a real **wall thickness** with a Solidify modifier (e.g. 2–3 mm), so it
   becomes a shell instead of a solid block.
2. Keep the shell **manifold** — Solidify with even thickness, then check for
   self-intersections on concave areas.
3. The slicer still adds **infill inside the shell walls' cavity** if you leave it
   hollow — OR you intentionally print the shell with a few perimeters and low infill.
   Either way the big interior volume is no longer solid plastic.
4. **Add drain/vent holes** for resin (so uncured resin escapes) and to avoid sealed air
   pockets in FDM. A couple of small holes in an unseen face is enough.

Don't over-thin: a hollow shell that's too thin warps, dents, and prints poorly. Match
wall thickness to size and handling (a big handled part wants thicker walls than a small
shelf bracket).

## Shape choices that save material

- **Chamfers beat fillets on downward overhangs** — a rounded underside often needs
  support material; a 45° chamfer prints in air and adds none. (See `printability.md`.)
- **Remove bulk that does nothing.** Solid blocks where only the surface matters can be
  shelled or pocketed on hidden faces.
- **Ribs/gussets over solid mass.** When a part needs stiffness, thin reinforcing ribs
  give most of the strength of a solid section at a fraction of the material. (Model
  these only when stiffness is the actual goal — not as a generic "infill" substitute.)
- **Right-size walls.** Don't default everything to thick walls; reserve thickness for
  where the load actually is.

## Print-time, not just plastic

Efficiency is also time. Fewer steep overhangs = less support = less wasted material and
post-processing. Fewer tiny details = faster. Bigger, simpler volumes print faster than
many fiddly thin features. Keep this in mind alongside raw gram count.

## Quick decision guide

- Small/medium functional part → model solid, recommend 15–30% infill.
- Large part / shell / enclosure → model with Solidify wall (2–3 mm) + drain holes,
  recommend low infill.
- Decorative → model solid (or shell if big), recommend 5–10% infill.
- Need stiffness without mass → add ribs/gussets, don't add solid bulk.
