# Multi-part assembly and hardware

When one printed lump won't do the job, split the design into parts and/or design around
standard non-printed hardware. Both require deliberate geometry — clearances, joints, and
correctly-sized pockets.

## When to split into multiple parts

Split the model when any of these is true:
- It's **larger than the build plate** (common FDM plates ~220×220 to 256×256 mm; check
  the user's printer).
- Different sections want **different print orientations** for strength or surface
  finish.
- It has **unavoidable steep overhangs** that splitting would turn into clean flat faces.
- It must **enclose hardware** (a bearing, a motor, magnets) that can't be inserted into
  a sealed print.
- A section needs to **move** relative to another.

**Each separately-printed part goes in its own export file**, named clearly
(e.g. `gripper_base.3mf`, `gripper_jaw_left.3mf`). Keep a master `.blend` with all parts
positioned as assembled, but export them individually, each oriented for its own best
print. Tell the user the suggested orientation and quantity per part.

## Joints between printed parts

- **Peg & hole:** simplest alignment. Peg ≥ 3 mm dia; hole = peg + ~0.3 mm clearance for
  a slip fit, +0.1 mm for a press fit.
- **Dovetail / sliding key:** strong against pull-apart; add ~0.2 mm clearance per face.
- **Screw bosses:** a cylindrical boss with a pilot hole; self-tapping screw cuts its own
  thread. Boss outer dia ≈ 2.5× screw dia; pilot hole ≈ screw core dia.
- **Snap-fit:** a cantilever hook that flexes and latches. Needs a flexible-enough
  filament (PLA works for light snaps, PETG/ABS/Nylon for repeated flexing) and a lead-in
  chamfer. Orient so the hook isn't pulled along layer lines.
- **Heat-set threaded inserts:** the strongest reusable threads in plastic (see below).
- **Glue surfaces:** for purely cosmetic splits, flat mating faces + alignment pegs.

Always add a **lead-in chamfer** on the entering edge of any peg/insert so parts start
square and don't jam on the first layer's elephant-foot bulge.

## Designing around standard hardware

Ask the user to confirm exact part numbers/sizes — these are common defaults, but parts
vary. Then model the pocket to the **part spec plus the right clearance**.

### Bearings
- **608** (skateboard/fidget): 22 mm OD × 8 mm ID × 7 mm wide. Pocket bore = 22.0 mm for
  a press fit, 22.2–22.3 mm for a drop-in; seat depth = 7 mm with a shoulder so it can't
  push through. Shaft through the ID = 8 mm + clearance, or use an 8 mm bolt.
- **623 / 624 / 625 / 626**: small bearings (e.g. 625 = 16 OD × 5 ID × 5 W). Confirm
  which.

### Magnets (round neodymium)
- Common sizes: 6×3 mm, 8×3 mm, 10×2 mm (dia × thickness).
- Pocket = magnet dia + ~0.1 mm, depth = thickness (or thickness − 0.2 mm if glued flush
  and you want it slightly proud). Mark/confirm **polarity** when magnets must attract
  across a joint. Leave a thin (~0.4–0.8 mm) wall over the magnet if you don't want it
  visible, or a blind pocket to glue into.

### Screws & nuts
- **M3** is the workhorse. Clearance hole = 3.2–3.4 mm; tap/self-tap pilot ≈ 2.5 mm.
- **Hex nut trap (M3):** pocket across-flats ≈ 5.5 mm + 0.2 mm, depth = nut height
  (~2.4 mm). Orient the trap so it's bridged over cleanly.
- Always confirm M-size and head type (socket cap vs. countersunk → model a counterbore
  or 90° countersink).

### Heat-set threaded inserts (recommended for reusable screw holes)
- Boss hole is sized to the insert's lead diameter (e.g. a common M3 insert wants a
  ~4.0 mm hole, ~5 mm deep). Insert is melted in with a soldering iron. Confirm the
  insert's datasheet hole size — these vary by brand.

### Springs & rubber bands
- Provide an anchor post/hook and a relief channel so the band/spring routes without
  rubbing print layers. Size the post so the band stays seated under tension.

### Motors
- **28BYJ-48** (small geared stepper): ~28 mm body dia, mounting tabs ~35 mm apart with
  M3/M4 holes; 5 mm half-D output shaft — model a matching D-bore for the coupler.
- **NEMA 17** (common stepper): 42.3 mm square face, 31 mm bolt circle (4× M3), 5 mm
  round shaft (often with a flat), 22 mm pilot boss (Ø ~22.5 mm pocket for centering).
  Leave clearance and ventilation; steppers get warm.
- Always confirm shaft diameter/flat and bolt pattern from the motor's datasheet.

## Process for hardware

1. Confirm the **exact part** with the user (number, dimensions).
2. Model the **pocket/boss/bore to spec + clearance** above.
3. Add **lead-in chamfers** and, for inside-the-print parts, a way to insert them
   (split the part, or a capture pocket inserted before closing).
4. Note assembly order in your handoff ("press the 608 into the hub before joining the
   two halves").
