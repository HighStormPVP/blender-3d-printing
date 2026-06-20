# Resin (MSLA / SLA) printing

The rest of this skill is FDM-first. Resin printing shares the watertight/manifold
requirement and the millimeter scale, but the physics of how the part forms are
different, so several design rules change. Read this when the user says resin, SLA, MSLA,
or mentions a printer like an Elegoo Saturn/Mars, Anycubic Photon, Phrozen, or Form 3.

## What's the same

- **Manifold/watertight geometry** is still mandatory (see `printability.md`).
- **Work in millimeters.**
- **Tolerances/clearances** for fits still apply — resin can actually hold tighter
  tolerances than FDM, but start similar (~0.2 mm) and refine.

## What changes

### 1. There is no infill — hollow instead
Resin parts cure solid; the slicer doesn't do FDM-style infill. A solid resin part wastes
expensive resin and can crack from internal curing stress. So for anything beyond small
parts:
- **Hollow the part** to a wall thickness of ~1.5–3 mm (use Solidify; the resin slicer
  can also hollow, but modeling it gives you control).
- This is the resin equivalent of the filament-efficiency goal — solid resin is heavy and
  costly.

### 2. Drain + anti-suction holes are mandatory for hollows
A sealed hollow traps uncured resin (a "resin trap") that never drains and can blow out
the print, and creates suction that can rip the part off the plate.
- Add **at least two holes**, ≥ 2–3 mm dia: one low to drain, one high to vent.
- Place them on hidden/bottom faces. More/bigger holes for larger cavities.

### 3. Orientation and supports are different
- Parts are usually printed **tilted at 30–45°** and lifted off the plate on supports,
  not flat on the bed — this reduces layer-line cross-section (suction) and improves
  detail.
- Supports are **point/nub supports** the slicer adds; you don't model them, but design
  so there's a sacrificial face to support against and no critical detail on the
  down-facing side.
- Avoid large flat areas parallel to the plate (huge suction force).

### 4. Detail and minimum features
- Resin resolves much finer detail than FDM — embossed text, fine textures, thin spikes
  all work where FDM can't.
- Minimum wall ~0.5 mm; very fine features still risk breaking off during washing/curing.

### 5. Material behavior
- Many standard resins are **stiff and brittle** once cured; choose a "tough,"
  "ABS-like," or "flexible" resin for functional/impact parts.
- Cured resin keeps curing (gets more brittle) with UV exposure over time; not ideal for
  long-term outdoor structural parts.

## Export & slicing
Export STL/3MF as usual, then slice in the resin slicer (Lychee, ChiTuBox, or the
vendor's slicer) where you set layer height (often 0.05 mm), exposure times, hollowing,
and supports. There's no command-line equivalent as universal as PrusaSlicer's, so for
resin, hand the file over and let the user finish in their resin slicer unless they say
otherwise.

## Resin design checklist
- [ ] Watertight/manifold
- [ ] Hollowed (walls ~1.5–3 mm) if anything but a small solid
- [ ] Drain + vent holes added to any hollow (no resin traps)
- [ ] No large flat face that would sit parallel to the plate
- [ ] Critical detail kept off the down-facing/supported side
- [ ] Appropriate resin chosen for the part's toughness needs
