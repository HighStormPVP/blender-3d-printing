# Print handoff template

When the model is done, exported, and verified, give the user a single clear summary so
they (or their slicer) know exactly how to print it. Don't make them dig the settings out
of the conversation. Fill in this template — keep it short and concrete.

```
PRINT HANDOFF — <part / assembly name>

Files:
  - <file1.3mf>  (<W × D × H mm>)   x<qty>
  - <file2.3mf>  (<W × D × H mm>)   x<qty>      # one line per separately-printed part

Material:        <PLA / PETG / TPU / ...>  — <one-line why, e.g. "PETG for outdoor + toughness">
Recommended infill:   <e.g. 20% gyroid>     (decorative 5–10% / general 15–20% / functional 30–50%)
Print orientation:    <which face down, and why — loads should run ACROSS layers>
Supports:        <none needed / tree supports on overhang at X / lattice for heavy part>
Bed adhesion:    <skirt / brim if tall or top-heavy / raft>   # brim also stops tipping
Layer height:    <e.g. 0.2 mm>   Nozzle: <0.4 mm assumed>

Estimated material:   <~Ng, ~cost>   (from estimate_filament.py or the slicer report)

Assembly / hardware:  <none>  OR
  - <e.g. "Press one 608 bearing (22×8×7) into the hub before joining halves">
  - <e.g. "2× M3×8 socket-cap screws into the rear bosses">

Post-processing:      <none / remove supports at X / light sanding on mating faces>
Notes:                <test-fit note, tolerance caveat, etc.>
```

## Why each line matters

- **Files + qty + size** — confirms scale is right and the print bed can hold each part.
- **Material + why** — the part's job (heat, outdoors, flex, load) drives this; see
  `materials.md`.
- **Infill** — the main filament-vs-strength lever; match it to use, don't default high.
- **Orientation** — a real strength decision (layer adhesion is the weak axis); state it.
- **Supports** — flags where the design needed help so the user enables them.
- **Estimated material** — closes the loop on the efficiency goal.
- **Assembly/hardware + order** — prevents the "sealed-in bearing" mistake.
- **Post-processing** — sets expectations (support scars, sanding for fit).

If anything was a judgment call (a tolerance, an orientation trade-off), say so plainly so
the user can adjust on a test print.
