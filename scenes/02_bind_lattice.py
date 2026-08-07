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
    create_event_sphere,
    create_link_curve,
    make_material,
    reset_scene,
    set_render_defaults,
    stamp_world,
)
from spherepop_blender.core import SPWorld, bind, pop


def main() -> None:
    reset_scene()
    set_render_defaults(frame_end=280)

    world = SPWorld()
    positions: dict[int, tuple[float, float, float]] = {}

    node_mat = make_material(
        "Distinction",
        base=(0.2, 0.65, 0.95, 1.0),
        emission=(0.0, 0.1, 0.35, 1.0),
        emission_strength=1.0,
    )
    bind_mat = make_material(
        "Binding",
        base=(0.95, 0.45, 0.15, 1.0),
        emission=(0.95, 0.25, 0.05, 1.0),
        emission_strength=1.5,
    )
    higher_mat = make_material(
        "HigherOrderBinding",
        base=(0.85, 0.2, 0.75, 1.0),
        emission=(0.55, 0.0, 0.45, 1.0),
        emission_strength=1.8,
    )

    add_ground()
    add_world_light()
    add_camera(location=(0, -18, 11), target=(0, 0, 1.7))

    count = 8
    for i in range(count):
        frame = 10 + i * 6
        angle = (2.0 * math.pi * i) / count
        location = (4.8 * math.cos(angle), 4.8 * math.sin(angle), 0.3)

        eid = pop(world, {"label": f"node-{i}"}, frame=frame)
        positions[eid] = location

        obj = create_event_sphere(
            world,
            world.events[eid],
            location,
            radius=0.45,
            material=node_mat,
        )
        animate_scale_in(obj, start_frame=frame, duration=8)

    binding_ids = []
    for i in range(count):
        left = i
        right = (i + 1) % count
        frame = 70 + i * 8

        eid = bind(world, left, right, value={"kind": "ring"}, frame=frame)
        binding_ids.append(eid)

        link = create_link_curve(
            world,
            world.events[eid],
            positions[left],
            positions[right],
            material=bind_mat,
            bevel_depth=0.045,
        )
        animate_curve_reveal(link, start_frame=frame, duration=10)

        mid = tuple((positions[left][axis] + positions[right][axis]) / 2.0 for axis in range(3))
        positions[eid] = (mid[0], mid[1], mid[2] + 1.6)
        obj = create_event_sphere(
            world,
            world.events[eid],
            positions[eid],
            radius=0.22,
            material=bind_mat,
        )
        animate_scale_in(obj, start_frame=frame + 5, duration=8)

    higher_nodes = []
    for j in range(0, len(binding_ids), 2):
        left = binding_ids[j]
        right = binding_ids[(j + 1) % len(binding_ids)]
        frame = 160 + (j // 2) * 14

        eid = bind(
            world,
            left,
            right,
            value={"kind": "binding-of-bindings"},
            frame=frame,
        )
        higher_nodes.append(eid)

        link = create_link_curve(
            world,
            world.events[eid],
            positions[left],
            positions[right],
            material=higher_mat,
            bevel_depth=0.03,
        )
        animate_curve_reveal(link, start_frame=frame, duration=12)

        mid = tuple((positions[left][axis] + positions[right][axis]) / 2.0 for axis in range(3))
        positions[eid] = (mid[0], mid[1], mid[2] + 1.8)
        node = create_event_sphere(
            world,
            world.events[eid],
            positions[eid],
            radius=0.2,
            material=higher_mat,
        )
        animate_scale_in(node, start_frame=frame + 4, duration=8)

    if len(higher_nodes) >= 2:
        final = bind(
            world,
            higher_nodes[0],
            higher_nodes[2],
            value={"kind": "second-order-lattice"},
            frame=235,
        )
        arc = create_link_curve(
            world,
            world.events[final],
            positions[higher_nodes[0]],
            positions[higher_nodes[2]],
            material=higher_mat,
            bevel_depth=0.026,
        )
        animate_curve_reveal(arc, start_frame=235, duration=14)

    stamp_world(
        bpy.context.scene,
        world,
        "Bind turns relations into first-class distinctions and binds them again.",
    )


if __name__ == "__main__":
    main()
