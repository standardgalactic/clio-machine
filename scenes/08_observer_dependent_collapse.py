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
    reset_scene,
    set_render_defaults,
    stamp_world,
)
from spherepop_blender.core import SPWorld, bind, collapse, pop


def camera_with_path(name: str, loc_start, loc_end, target):
    cam = add_camera(location=loc_start, target=target, lens=48)
    cam.name = name
    cam.location = loc_start
    cam.keyframe_insert(data_path="location", frame=1)
    cam.location = loc_end
    cam.keyframe_insert(data_path="location", frame=300)
    return cam


def main() -> None:
    reset_scene()
    set_render_defaults(frame_end=320)

    world = SPWorld()
    positions = {}

    node_mat = make_material(
        "ObserverNode",
        base=(0.25, 0.7, 0.95, 1.0),
        emission=(0.0, 0.25, 0.75, 1.0),
        emission_strength=1.2,
    )
    bind_mat = make_material(
        "ObserverBind",
        base=(0.9, 0.7, 0.15, 1.0),
        emission=(0.6, 0.35, 0.0, 1.0),
        emission_strength=0.9,
    )
    observer_a_mat = make_material(
        "ObserverACollapse",
        base=(0.95, 0.2, 0.35, 1.0),
        emission=(0.95, 0.2, 0.35, 1.0),
        emission_strength=2.2,
        alpha=0.3,
    )
    observer_b_mat = make_material(
        "ObserverBCollapse",
        base=(0.25, 0.95, 0.45, 1.0),
        emission=(0.25, 0.95, 0.45, 1.0),
        emission_strength=2.2,
        alpha=0.3,
    )
    observer_c_mat = make_material(
        "ObserverCCollapse",
        base=(0.35, 0.45, 1.0, 1.0),
        emission=(0.35, 0.45, 1.0, 1.0),
        emission_strength=2.2,
        alpha=0.3,
    )

    add_ground(size=34)
    add_world_light(energy=980)
    primary = camera_with_path("ObserverA", (0, -20, 11), (7, -14, 8), (0, 0, 1))
    camera_with_path("ObserverB", (-14, -12, 8), (-7, -20, 11), (0, 0, 1))
    camera_with_path("ObserverC", (10, -8, 7), (-12, -10, 10), (0, 0, 1))
    bpy.context.scene.camera = primary

    for i in range(12):
        frame = 10 + i * 6
        angle = (2.0 * math.pi * i) / 12.0
        r = 6.0 if i % 2 == 0 else 3.7
        z = 0.8 if i % 2 == 0 else 2.0
        pos = (r * math.cos(angle), r * math.sin(angle), z)
        eid = pop(world, {"label": f"n-{i}"}, frame=frame)
        positions[eid] = pos

        node = create_event_sphere(world, world.events[eid], pos, radius=0.32, material=node_mat)
        animate_scale_in(node, start_frame=frame, duration=7)

    for i in range(12):
        frame = 92 + i * 4
        a = i
        b = (i + 4) % 12
        eid = bind(world, a, b, value={"kind": "shared-structure"}, frame=frame)
        link = create_link_curve(
            world,
            world.events[eid],
            positions[a],
            positions[b],
            material=bind_mat,
            bevel_depth=0.018,
        )
        animate_curve_reveal(link, start_frame=frame, duration=8)

    observer_groups = [
        ("A", [0, 2, 3, 5, 8], observer_a_mat, (-2.0, 0.0, 1.3), 4.5),
        ("B", [1, 4, 6, 7, 10], observer_b_mat, (2.8, -0.8, 1.5), 4.4),
        ("C", [2, 6, 9, 10, 11], observer_c_mat, (0.4, 2.2, 1.8), 4.8),
    ]

    for idx, (observer_name, members, mat, center, radius) in enumerate(observer_groups):
        frame = 190 + idx * 28
        eid = collapse(
            world,
            *members,
            value={"observer": observer_name, "kind": "observer-collapse"},
            frame=frame,
        )
        shell = create_collapse_shell(
            world,
            world.events[eid],
            center=center,
            radius=radius,
            material=mat,
        )
        animate_scale_in(shell, start_frame=frame, duration=12)

    stamp_world(
        bpy.context.scene,
        world,
        "Multiple observers construct coexisting collapses over the same persistent history.",
    )


if __name__ == "__main__":
    main()
