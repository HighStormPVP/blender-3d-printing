# Print handoff template

When the model is done, exported, and verified, give the user a single clear summary so
they (or their slicer) know exactly how to print it. Don't make them dig the settings out
of the conversation. Fill in this template — keep it short and concrete.

```
PRINT HANDOFF — <part / assembly name>

Files:
  - <file1.stl>  (<W × D × H mm>)   x<qty>
  - <file2.stl>  (<W × D × H mm>)   x<qty>      # one line per separately-printed part

Material:        <PLA / PETG / TPU / ...>  — <one-line why, e.g. "PETG for outdoor + toughness">
Print orientation:    <which face down, and why — loads should run ACROSS layers>

In Bambu Studio (it handles infill + supports for you):
  - Printer:   <e.g. Bambu Lab A1 mini (0.4)>     Filament: <e.g. Bambu PLA Basic>
  - Quality:   <e.g. 0.20 mm Standard>
  - Infill:    <leave default ~15%, or raise to X% if it needs to be stronger>
  - Supports:  <off — prints flat>  OR  <on, Tree (auto) — has an overhang at X>

Assembly / hardware:  <none>  OR
  - <e.g. "Press one 608 bearing (22×8×7) into the hub before joining halves">
  - <e.g. "2× M3×8 socket-cap screws into the rear bosses">

Post-processing:      <none / light sanding on mating faces / clip supports if used>
Notes:                <test-fit note, tolerance caveat, est. ~Ng filament, etc.>
```

## Why each line matters

- **Files + qty + size** — confirms scale is right and the print bed can hold each part.
- **Material + why** — the part's job (heat, outdoors, flex, load) drives this; see
  `materials.md`.
- **Orientation** — a real strength decision (layer adhesion is the weak axis); state it.
- **Bambu Studio settings** — infill and supports are slicer settings, not modeled in
  Blender; give the user the printer/filament/quality to pick and note whether supports
  are needed. Defaults are usually right — only call out a change if the part needs it.
  See `bambu-studio.md`.
- **Assembly/hardware + order** — prevents the "sealed-in bearing" mistake.
- **Post-processing** — sets expectations (sanding for fit, clipping any supports).

If anything was a judgment call (a tolerance, an orientation trade-off), say so plainly so
the user can adjust on a test print.
