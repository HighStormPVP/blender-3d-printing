# blender-3d-printing

A [Claude](https://claude.com/claude-code) **Skill** that teaches Claude to design
3D-printable models in Blender that actually print well and survive real-world use — not
just render-only meshes.

It covers the things that make the difference between a pretty mesh and a part you can
hold in your hand:

- **Printability** — manifold/watertight geometry, wall thickness, overhangs & supports,
  bridging, tolerances/clearances, and orienting parts for strength along layer lines.
- **Filament efficiency** — modeling solids and letting the slicer do infill, hollowing
  large parts with proper wall thickness + drain holes, chamfers over fillets, and ribs
  instead of solid bulk.
- **Assembly & hardware** — splitting big models into separate print files, joint types,
  and correctly-sized pockets for bearings, magnets, screws, heat-set inserts, springs,
  and motors (only when the design actually needs them).
- **Export & slicing** — 3MF/STL export at true mm scale, and command-line slicing with
  PrusaSlicer / OrcaSlicer / Cura.

The skill is built to drive Blender directly through the
[Blender MCP](https://github.com/ahujasid/blender-mcp) (`execute_blender_code`,
`get_viewport_screenshot`), and works as a standalone knowledge reference even without it.

## What's inside

```
blender-3d-printing/
├── SKILL.md                          # entry point: mindset + workflow + the two mandatory asks
├── references/
│   ├── printability.md               # manifold rules, walls, overhangs, tolerances, orientation
│   ├── filament-efficiency.md        # solid vs shell, infill, hollowing big parts, lightweighting
│   ├── assembly-and-hardware.md      # multi-part splits, joints, bearing/magnet/screw/motor specs
│   └── slicing-and-export.md         # export formats + CLI slicing
└── scripts/                          # Blender Python, run via execute_blender_code
    ├── setup_scene.py                # set units to millimeters
    ├── printability_check.py         # 3D-Print Toolbox + bmesh manifold/size report
    └── export_for_print.py           # export STL/3MF at correct scale
```

## Install

**Claude Code (personal, all projects):**
```bash
git clone https://github.com/<you>/blender-3d-printing ~/.claude/skills/blender-3d-printing
```

**Claude Code (single project):**
```bash
git clone https://github.com/<you>/blender-3d-printing .claude/skills/blender-3d-printing
```

Then start Claude Code in that scope — the skill auto-loads and triggers whenever you ask
to model something for 3D printing.

## Usage

Just describe what you want to print:

> "Model a wall bracket for a 35 mm broom handle that screws into a stud."

> "I want to 3D print a fidget spinner — make it use a 608 bearing."

> "Make this vase printable and as light on filament as possible."

Claude will set the scene to millimeters, model with printable geometry, verify it's
watertight, export it, and offer to slice it. For best results, run the
[Blender MCP](https://github.com/ahujasid/blender-mcp) so Claude can build and check the
model in Blender directly.

## Requirements

- Blender 4.x recommended (the scripts handle both the new unified exporters and older
  operators).
- Optional but recommended: the Blender MCP server, for hands-on modeling.
- Optional: a slicer with a CLI (PrusaSlicer/OrcaSlicer/Cura) if you want print-ready
  G-code.

## License

MIT — see [LICENSE](LICENSE). Contributions and improvements welcome.
