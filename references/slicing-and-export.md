# Export and slicing

## Export formats

- **3MF (preferred):** carries real-world units, multiple objects, and metadata. Most
  modern slicers import it cleanly with correct scale. Blender exports 3MF via the
  built-in/IO add-on.
- **STL (universal fallback):** unitless triangle soup — works everywhere but you must
  make sure the model is authored in mm so it imports at the right size.
- **OBJ:** acceptable but no advantage here; avoid for printing.

Export **one file per separately-printed part**, each oriented for its own best print.
Use clear names tied to the assembly. `scripts/export_for_print.py` handles selecting an
object and exporting it at the correct scale.

Before export, re-run the printability checklist (`printability.md`) — a non-manifold
mesh slices into garbage no matter how good the slicer settings are.

## Offering to slice (mandatory ask)

After exporting, **ask the user whether they want it sliced and print-ready** so they can
go straight to the printer. If yes, gather:

1. **Which slicer** they use: PrusaSlicer, OrcaSlicer, Bambu Studio, or Cura.
2. **Printer model / profile** (build volume, nozzle dia).
3. **Filament** (PLA/PETG/ABS/etc.) and any preference on infill, layer height, supports.
4. **Print orientation** — recommend one based on strength (see `printability.md`); the
   slicer can also auto-orient.

If they don't have a slicer set up, just hand over the STL/3MF and confirm it's ready to
drop into any slicer.

## Command-line slicing

Most desktop slicers ship a CLI/headless mode, so you can produce G-code without opening
the GUI. Confirm the exact binary path and an existing **printer/filament config** with
the user first — slicing without a correct machine profile produces unusable G-code.

### PrusaSlicer / OrcaSlicer / SuperSlicer (same CLI family)
```bash
# Slice to G-code using a saved config bundle (.ini exported from the GUI)
prusa-slicer --export-gcode \
  --load my_printer_config.ini \
  --output part.gcode \
  part.3mf

# Handy overrides
prusa-slicer --export-gcode --load cfg.ini \
  --fill-density 20% \
  --layer-height 0.2 \
  --support-material \
  --output part.gcode part.stl
```
### OrcaSlicer (verified, incl. Bambu printers like the A1 mini)

OrcaSlicer's CLI loads the bundled **system profile JSON files** directly and resolves
their `inherits` chain from its own `resources/profiles` tree — so you don't need to
export anything from the GUI first. Point it at the machine + process and the filament:

```bash
ORCA="/c/Program Files/OrcaSlicer/orca-slicer.exe"
PROF="/c/Program Files/OrcaSlicer/resources/profiles/BBL"
"$ORCA" \
  --load-settings "$PROF/machine/Bambu Lab A1 mini 0.4 nozzle.json;$PROF/process/0.20mm Standard @BBL A1M.json" \
  --load-filaments "$PROF/filament/Bambu PLA Basic @BBL A1M.json" \
  --arrange 1 --orient 1 --slice 0 \
  --outputdir ./print_parts \
  part.stl
```

- `--orient 1` auto-picks a print orientation (a good cross-check on your intended one);
  drop it to keep the model's own orientation.
- Output is `plate_1.gcode`. Read its header comments for the real stats:
  `; model printing time:`, `; filament used [mm] =`, `; sparse_infill_density =`,
  `; enable_support =`.
- Profile names vary by printer/version — list `resources/profiles/<VENDOR>/{machine,
  process,filament}` to find the exact filenames for the user's printer and material.

Bambu Studio uses `bambu-studio` with similar flags, but its headless CLI is less
reliable than OrcaSlicer's — prefer OrcaSlicer for command-line slicing, or Bambu Studio's
GUI (it has built-in profiles for every Bambu printer).

### Cura (CuraEngine)
CuraEngine is lower-level and wants an explicit settings JSON/definition:
```bash
CuraEngine slice -v \
  -j path/to/printer_definition.def.json \
  -s infill_line_distance=2 \
  -l part.stl \
  -o part.gcode
```
Most users find the PrusaSlicer-family CLI easier; prefer it unless the user is on Cura.

### After slicing
Report back the **estimated print time and filament usage** the slicer prints to stdout —
that closes the loop on the filament-efficiency goal and lets the user sanity-check before
committing the print.

## Notes

- Verify the sliced result's reported dimensions match the intended mm size — a scale
  mistake shows up immediately here.
- If the user has no config bundle, point them to export one from their slicer GUI
  (Printer Settings → export config) rather than guessing machine limits.
