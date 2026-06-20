# Choosing a filament / material

The material is a design decision, not an afterthought — it changes how thick walls need
to be, how the part survives load and heat, and how much clearance to leave. Pick it from
the part's real-world job, then tell the user (it also drives the density used in
`scripts/estimate_filament.py`).

## FDM filaments

| Material | Strength / stiffness | Toughness (impact) | Heat resist. | Outdoor/UV | Flexible? | Print difficulty | Density (g/cm³) |
|----------|---------------------|--------------------|--------------|------------|-----------|------------------|-----------------|
| **PLA**  | High stiffness, brittle | Low | Low (~55 °C, softens in a hot car) | Poor | No | Easy | 1.24 |
| **PETG** | Good | Good | Medium (~75 °C) | Good | Slightly | Easy–medium | 1.27 |
| **ABS/ASA** | Good | Good | High (~95 °C) | ASA: excellent | No | Hard (warps, fumes, enclosure) | 1.04 |
| **TPU**  | Low (rubbery) | Very high | Medium | Good | **Yes** | Medium (slow) | 1.21 |
| **Nylon (PA)** | High | Very high | High | Medium | Slightly | Hard (absorbs moisture) | 1.14 |
| **PC**   | Very high | High | Very high (~110 °C) | Good | No | Hard (hot end + enclosure) | 1.20 |

### Quick selection guide

- **Prototype / decorative / dimensionally fussy / indoors** → **PLA**. Easiest, stiff,
  cheap. Just remember it's brittle and softens in heat (don't leave it in a car).
- **Functional part, outdoors, mild heat, needs some toughness** → **PETG**. The default
  "real part" material; survives drops better than PLA.
- **High heat or mechanical/automotive, can run an enclosure** → **ABS/ASA** (ASA for
  UV/outdoor).
- **Anything that must flex, grip, cushion, or seal** (phone bumpers, feet, gaskets,
  belts, living straps) → **TPU**. Specify a shore hardness (95A common, firmer = 60D).
- **Gears, living hinges, high-wear, high-impact** → **Nylon** (or PETG as an easier
  stand-in).

## How material affects the model

- **Brittle materials (PLA)** want thicker walls and generous fillets at stress
  concentrations; avoid thin cantilever snap-fits that will snap once.
- **Flexible materials (TPU)** change clearance logic — press fits behave differently,
  and "rigid" features go floppy if too thin. Snap-fits and living hinges love TPU/Nylon.
- **High-shrink materials (ABS/Nylon)** warp; keep large flat areas modest, add
  generous base contact, and expect slightly more dimensional drift — loosen tolerances.
- **Heat exposure** (motor mounts, anything near electronics or sun) rules out PLA — its
  low glass-transition temp means it creeps under sustained load and sags in heat.

## Resin (MSLA/SLA)

Resin is its own world — far finer detail but different mechanics (cured resin is often
stiff/brittle, some "tough"/"ABS-like" resins exist). It also needs **hollowing + drain
holes** rather than infill. See `references/resin-printing.md`.

When in doubt, recommend **PLA for looks/prototypes** and **PETG for function**, and ask
the user about heat, outdoors, load, and flex — those four answers pick the material.
