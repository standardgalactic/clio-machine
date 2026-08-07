from __future__ import annotations

import random
import sys
from pathlib import Path

import bpy

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from spherepop_blender.blender import (
    add_camera,
    add_frontier_plane,
    add_world_light,
    animate_curve_reveal,
    animate_location_z,
    animate_scale_in,
    create_collapse_shell,
    create_event_sphere,
    create_link_curve,
    make_material,
    mark_refused,
    reset_scene,
    set_render_defaults,
    stamp_world,
)
from spherepop_blender.core import SPWorld, bind, collapse, pop, refuse


def main() -> None:
    reset_scene()
    set_render_defaults(frame_end=340)

    world = SPWorld()
    rng = random.Random(5)
    positions = {}
    objects = {}

    node_mat = make_material(
        "HistoryNode",
        base=(0.2, 0.7, 1.0, 1.0),
        emission=(0.0, 0.3, 0.8, 1.0),
        emission_strength=1.0,
    )
    bind_mat = make_material(
        "HistoryBind",
        base=(0.9, 0.75, 0.2, 1.0),
        emission=(0.5, 0.35, 0.0, 1.0),
        emission_strength=0.9,
    )
    frontier_mat = make_material(
        "FrontierPlane",
        base=(0.2, 1.0, 0.7, 1.0),
        emission=(0.25, 1.0, 0.7, 1.0),
        emission_strength=3.2,
        alpha=0.25,
    )
    collapse_mat = make_material(
        "FrontierCollapse",
        base=(0.9, 0.2, 0.8, 1.0),
        emission=(0.9, 0.2, 0.8, 1.0),
        emission_strength=2.0,
        alpha=0.35,
    )

    add_world_light(energy=1200, location=(6, -6, 10))
    add_camera(location=(0, -22, 14), target=(0, 0, -2.0))

    frontier = add_frontier_plane(size=18.0, z=-7.0, material=frontier_mat)
    animate_location_z(frontier, start_frame=1, end_frame=330, z_start=-7.0, z_end=8.0)

    branches = [(0.0, -4.0), (-3.0, 1.0), (3.5, 1.2)]
    previous = []

    for layer in range(9):
        z = -7.0 + layer * 1.8
        current = []
        for branch_idx, (bx, by) in enumerate(branches):
            x = bx + rng.uniform(-0.7, 0.7)
            y = by + rng.uniform(-0.7, 0.7)
            frame = 10 + layer * 24 + branch_idx * 4
            eid = pop(world, {"layer": layer, "branch": branch_idx}, frame=frame)
            positions[eid] = (x, y, z)
            current.append(eid)

            obj = create_event_sphere(world, world.events[eid], positions[eid], radius=0.25, material=node_mat)
            animate_scale_in(obj, start_frame=frame, duration=7)
            objects[eid] = obj

        for idx, eid in enumerate(current):
            if layer > 0:
                parent = previous[idx]
                frame = 20 + layer * 24 + idx * 3
                rid = bind(world, parent, eid, value={"kind": "history-edge"}, frame=frame)
                line = create_link_curve(
                    world,
                    world.events[rid],
                    positions[parent],
                    positions[eid],
                    material=bind_mat,
                    bevel_depth=0.02,
                )
                animate_curve_reveal(line, start_frame=frame, duration=6)

        if layer in (4, 6):
            target = current[1]
            f = 28 + layer * 24
            refuse(world, target, reason="frontier exclusion", frame=f)
            mark_refused(objects[target], frame=f, archive_offset=(0.0, 0.0, -1.8), duration=12, scale_factor=0.75)

        if layer in (5, 8):
            cframe = 32 + layer * 24
            cid = collapse(world, *current, value={"layer": layer, "kind": "frontier-cluster"}, frame=cframe)
            center = (
                sum(positions[e][0] for e in current) / len(current),
                sum(positions[e][1] for e in current) / len(current),
                z,
            )
            shell = create_collapse_shell(
                world,
                world.events[cid],
                center,
                radius=1.7,
                material=collapse_mat,
            )
            animate_scale_in(shell, start_frame=cframe, duration=10)

        previous = current

    stamp_world(
        bpy.context.scene,
        world,
        "History persists in depth while the frontier advances as the active continuation plane.",
    )


if __name__ == "__main__":
    main()
