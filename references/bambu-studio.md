# Printing with Bambu Studio

**Bambu Studio does the slicing for you.** Infill, supports, the internal lattice, layer
height, brims — you do **not** model or calculate any of that in Blender. You export a
clean, watertight model (STL or 3MF) at true mm scale, open it in Bambu Studio, pick a
printer and filament, and it generates everything automatically with sensible defaults.

Your job in Blender is the **geometry**; Bambu Studio's job is the **print strategy**. This
file is how to drive Bambu Studio so you can give the user accurate, click-by-click
instructions.

> Menu labels move slightly between Bambu Studio versions. If the user's screen doesn't
> match, ask which version they're on (Help → About) and adapt — don't insist on a label.

## 1. Open the model

- Launch Bambu Studio and **drag the exported `.stl`/`.3mf` onto the build plate**
  (or File → Import → Import 3MF/STL, Ctrl+I).
- It should land at the correct size because you authored it in mm. **Sanity-check the
  dimensions** shown when the object is selected — if it's 1000× off, the export scale was
  wrong, not the slicer.

## 2. Pick the printer and filament

- **Printer** (top-left dropdown): choose the user's machine, e.g. **Bambu Lab A1 mini**,
  with the **0.4 mm nozzle**. Bambu Studio ships a tuned profile for every Bambu printer —
  use it rather than hand-entering bed size or limits.
- **Filament** (filament dropdown, top): choose the spool, e.g. **Bambu PLA Basic**
  (or "Generic PLA" for a third-party spool). On an A1 mini **without AMS** there's one
  external spool slot; with **AMS lite** you assign slots.

## 3. Choose quality (layer height)

In the **process/quality preset** dropdown (top), pick a layer height:

| Preset | Layer height | Use |
|--------|-------------|-----|
| Fine | 0.12 mm | fine detail, slower |
| **Standard** | **0.20 mm** | **default — good balance** |
| Draft | 0.28 mm | fast, coarse |

0.20 mm Standard is the right default for most parts.

## 4. Infill — Bambu Studio sets it; here's how to change it

Bambu Studio automatically fills the inside with an efficient pattern at a **sensible
default density (~15%)** — you don't model this. To change it: right panel → **Strength**
tab → **Infill**:

- **Sparse infill density (%)** — the strength-vs-material lever:
  - **5–10%** — decorative / non-load
  - **15%** — general default (leave it here unless there's a reason)
  - **25–50%** — functional / load-bearing
  - **100%** — maximum strength (slow, heavy; rarely needed)
- **Sparse infill pattern** — leave the default; **Gyroid** is a great all-rounder
  (strong in every direction) if you want to set one. The user almost never needs to touch
  the pattern.

## 5. Supports — Bambu Studio auto-generates them

If the part has overhangs steeper than ~45° (which a good design minimizes — see
`printability.md`), turn supports on and Bambu Studio figures out where they go: right
panel → **Support** tab:

- **Enable support** — tick it. If your model prints flat with no steep overhangs, leave
  it **off** (cleaner, faster, no scars).
- **Type** — **"Tree (auto)"** for organic/figurine shapes (less contact, easy to snap
  off, less scarring) or **"Normal (auto)"** for boxy/mechanical parts. Either way, *auto*
  means Bambu detects the overhangs — you don't place anything.
- Leave **threshold angle**, **top z-distance**, and **interface** at defaults; the
  defaults already give a gap so supports peel off cleanly. Only mention these if the user
  reports supports fusing to the part.

You generally do **not** need to choose support density or design the support yourself —
that's the whole point of letting the slicer do it.

## 6. Orientation and plate

- **Orientation matters for strength** (layer lines are the weak axis — see
  `printability.md`), and it's set here, not in Blender. Use the left toolbar:
  **Rotate**, **Place on face** (click the flat face you want on the bed), or
  **Auto-orient**.
- **Auto-arrange** (key `A`) spaces multiple objects on the plate.
- **Bed adhesion / brim:** right panel → **Others** tab → **Brim**. For tall or
  small-footprint parts, set **Brim type: Outer brim** (~5 mm) so the part doesn't pop off
  or tip. Most flat-based parts need only the default skirt.

## 7. Slice and check

- Click **Slice plate** (bottom-right).
- The **Preview** shows **estimated print time, filament weight/length, and cost** — read
  these back to the user; it's the authoritative material number (better than any
  pre-slice estimate). Scrub the layer slider to eyeball supports and infill.

## 8. Print

Two ways to get the sliced job to an A1 mini:

- **Send over the network:** click **Print plate** → Bambu Studio sends it to the printer
  over LAN/cloud. Confirm the right filament is loaded.
- **microSD card:** **Export plate sliced file** (`.3mf` or `.gcode`) → copy to the
  printer's microSD card → select it on the printer's screen. (We verified a `.gcode`
  export slices and runs on the A1 mini.)

## Quick recipe to tell the user (A1 mini + PLA Basic)

1. Drag the STL into Bambu Studio.
2. Printer → **Bambu Lab A1 mini (0.4)**; Filament → **Bambu PLA Basic**.
3. Quality → **0.20 mm Standard**.
4. Infill → leave **15%** (Strength tab) unless it needs to be stronger.
5. Supports → **off** if it prints flat; else **Tree (auto)**.
6. Make sure it's sitting on its flat base (Place on face if not).
7. **Slice** → check time/weight → **Print** (or export to microSD).
