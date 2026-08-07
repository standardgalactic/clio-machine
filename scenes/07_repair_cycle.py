from __future__ import annotations

import math
import sys
from pathlib import Path

import bpy

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from spherepop_blender.blender import (
    add_camera,
    add_ground,
    add_world_light,
    animate_curve_reveal,
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
    set_render_defaults(frame_end=320)

    world = SPWorld()
    positions = {}
    objects = {}

    base_mat = make_material(
        "RepairBase",
        base=(0.25, 0.65, 0.95, 1.0),
        emission=(0.0, 0.25, 0.65, 1.0),
        emission_strength=1.1,
    )
    candidate_mat = make_material(
        "RepairCandidate",
        base=(0.95, 0.65, 0.2, 1.0),
        emission=(0.75, 0.35, 0.0, 1.0),
        emission_strength=1.2,
    )
    rejected_mat = make_material(
        "RepairRejected",
        base=(0.45, 0.45, 0.5, 1.0),
        emission=(0.1, 0.1, 0.12, 1.0),
        emission_strength=0.2,
        alpha=0.45,
    )
    repaired_mat = make_material(
        "RepairCollapsed",
        base=(0.85, 0.2, 0.85, 1.0),
        emission=(0.75, 0.15, 0.75, 1.0),
        emission_strength=2.0,
        alpha=0.3,
    )

    add_ground(size=38)
    add_world_light(energy=1000)
    add_camera(location=(0, -20, 10), target=(0, 0, 1.0))

    base_nodes = []
    for i in range(6):
        frame = 10 + i * 8
        angle = i * (2.0 * math.pi / 6.0)
        pos = (4.2 * math.cos(angle), 4.2 * math.sin(angle), 0.8)
        eid = pop(world, {"kind": "unstable-base", "idx": i}, frame=frame)
        positions[eid] = pos
        base_nodes.append(eid)

        obj = create_event_sphere(world, world.events[eid], pos, radius=0.35, material=base_mat)
        animate_scale_in(obj, start_frame=frame, duration=8)
        objects[eid] = obj

    for i in range(len(base_nodes)):
        left = base_nodes[i]
        right = base_nodes[(i + 2) % len(base_nodes)]
        frame = 70 + i * 6
        eid = bind(world, left, right, value={"kind": "unstable-link"}, frame=frame)
        line = create_link_curve(
            world,
            world.events[eid],
            positions[left],
            positions[right],
            material=candidate_mat,
            bevel_depth=0.03,
        )
        animate_curve_reveal(line, start_frame=frame, duration=9)

    candidates = []
    for j in range(4):
        frame = 130 + j * 10
        pos = (-5.5 + j * 3.5, 6.5, 1.7)
        eid = pop(world, {"kind": "repair-candidate", "idx": j}, frame=frame)
        positions[eid] = pos
        candidates.append(eid)

        obj = create_event_sphere(world, world.events[eid], pos, radius=0.32, material=candidate_mat)
        animate_scale_in(obj, start_frame=frame, duration=8)
        objects[eid] = obj

    for idx, candidate in enumerate(candidates):
        anchor = base_nodes[idx]
        frame = 178 + idx * 7
        eid = bind(world, anchor, candidate, value={"kind": "candidate-attachment"}, frame=frame)
        link = create_link_curve(
            world,
            world.events[eid],
            positions[anchor],
            positions[candidate],
            material=candidate_mat,
            bevel_depth=0.025,
        )
        animate_curve_reveal(link, start_frame=frame, duration=8)

    rejected = [candidates[0], candidates[2]]
    for idx, target in enumerate(rejected):
        frame = 218 + idx * 16
        refuse(world, target, reason="inadmissible repair path", frame=frame)
        mark_refused(objects[target], frame=frame, archive_offset=(0.0, 0.0, -4.5), duration=14, scale_factor=0.7)
        objects[target].data.materials.clear()
        objects[target].data.materials.append(rejected_mat)

    kept = [c for c in candidates if c not in rejected]
    repaired = collapse(
        world,
        *(base_nodes + kept),
        value={"kind": "repaired-continuation"},
        frame=270,
    )
    shell = create_collapse_shell(
        world,
        world.events[repaired],
        center=(0.0, 1.8, 1.2),
        radius=7.4,
        material=repaired_mat,
    )
    animate_scale_in(shell, start_frame=270, duration=18)

    stamp_world(
        bpy.context.scene,
        world,
        "Repair emerges from selective continuation in a persistent possibility space.",
    )


if __name__ == "__main__":
    main()
