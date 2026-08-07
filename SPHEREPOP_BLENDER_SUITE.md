# Spherepop Blender Suite

This repository now includes a Blender-oriented Spherepop visualization suite.

## Directories

- `/home/runner/work/clio-machine/clio-machine/spherepop_blender/` — reusable world/event model and `bpy` helpers.
- `/home/runner/work/clio-machine/clio-machine/scenes/` — ten scene scripts (`01_` through `10_`) that progress from Pop to recursive cosmology.
- `/home/runner/work/clio-machine/clio-machine/scripts/headless/` — headless Blender render runners.

## Run a single scene

```bash
blender --python scenes/01_pop_field.py
```

## Run a single headless render

```bash
scripts/headless/render_scene.sh 04_collapse_representation.py
```

## Render the full sequence

```bash
scripts/headless/render_all.sh
```

All scenes treat `SPWorld` event history as authoritative and use Blender objects as renderable projections of that history.
