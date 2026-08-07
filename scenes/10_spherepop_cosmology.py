from __future__ import annotations

import math
import random
import sys
from pathlib import Path

import bpy

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from spherepop_blender.blender import (
    add_camera,
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
from spherepop_blender.core import SPWorld, bind, collapse, pop, refuse


def recursive_level(
    world: SPWorld,
    *,
    level: int,
    anchor,
    radius: float,
    frame_start: int,
    rng: random.Random,
    node_mat,
    bind_mat,
    collapse_mat,
):
    node_ids = []
    points = []

    count = 4 + level
    for i in range(count):
        frame = frame_start + i * 6
        angle = (2.0 * math.pi * i) / count
        r = radius * (0.55 + rng.random() * 0.25)
        loc = (
            anchor[0] + r * math.cos(angle),
            anchor[1] + r * math.sin(angle),
            anchor[2] + (rng.random() - 0.5) * radius * 0.35,
        )
        eid = pop(world, {"level": level, "idx": i}, frame=frame)
        node_ids.append(eid)
        points.append(loc)

        obj = create_event_sphere(world, world.events[eid], loc, radius=max(0.14, radius * 0.08), material=node_mat)
        animate_scale_in(obj, start_frame=frame, duration=7)

    for i in range(len(node_ids)):
        left = node_ids[i]
        right = node_ids[(i + 1) % len(node_ids)]
        frame = frame_start + 42 + i * 5
        eid = bind(world, left, right, value={"level": level}, frame=frame)
        link = create_link_curve(
            world,
            world.events[eid],
            points[i],
            points[(i + 1) % len(points)],
            material=bind_mat,
            bevel_depth=max(0.01, radius * 0.004),
        )
        animate_curve_reveal(link, start_frame=frame, duration=6)

    if len(node_ids) > 3:
        refuse(world, node_ids[1], reason="frontier exclusion", frame=frame_start + 86)

    collapse_frame = frame_start + 112
    ceid = collapse(world, *node_ids, value={"level": level, "kind": "level-collapse"}, frame=collapse_frame)
    center = (
        sum(p[0] for p in points) / len(points),
        sum(p[1] for p in points) / len(points),
        sum(p[2] for p in points) / len(points),
    )
    shell = create_collapse_shell(
        world,
        world.events[ceid],
        center,
        radius=radius * 0.78,
        material=collapse_mat,
    )
    animate_scale_in(shell, start_frame=collapse_frame, duration=12)

    return ceid, center


def main() -> None:
    reset_scene()
    set_render_defaults(frame_end=480)

    world = SPWorld()
    rng = random.Random(17)

    node_mat = make_material(
        "CosmosNode",
        base=(0.2, 0.7, 1.0, 1.0),
        emission=(0.0, 0.35, 0.85, 1.0),
        emission_strength=1.3,
    )
    bind_mat = make_material(
        "CosmosBind",
        base=(0.95, 0.75, 0.2, 1.0),
        emission=(0.7, 0.45, 0.0, 1.0),
        emission_strength=1.0,
    )
    collapse_mat = make_material(
        "CosmosCollapse",
        base=(0.95, 0.25, 0.95, 1.0),
        emission=(0.95, 0.25, 0.95, 1.0),
        emission_strength=2.4,
        alpha=0.3,
    )

    add_world_light(energy=1300, location=(8, -8, 16))
    cam = add_camera(location=(0, -18, 10), target=(0, 0, 0), lens=45)

    cam.location = (0, -14, 8)
    cam.keyframe_insert(data_path="location", frame=1)
    cam.location = (0, -26, 14)
    cam.keyframe_insert(data_path="location", frame=220)
    cam.location = (0, -42, 22)
    cam.keyframe_insert(data_path="location", frame=360)
    cam.location = (0, -58, 30)
    cam.keyframe_insert(data_path="location", frame=470)

    anchor = (0.0, 0.0, 0.0)
    radius = 5.0
    frame = 10
    collapsed = []

    for level in range(4):
        ceid, center = recursive_level(
            world,
            level=level,
            anchor=anchor,
            radius=radius,
            frame_start=frame,
            rng=rng,
            node_mat=node_mat,
            bind_mat=bind_mat,
            collapse_mat=collapse_mat,
        )
        collapsed.append(ceid)

        frame += 95
        radius *= 1.6
        anchor = (center[0] * 0.35, center[1] * 0.35, center[2] * 0.35)

    top = collapse(world, *collapsed, value={"kind": "cross-level-cosmos"}, frame=430)
    shell = create_collapse_shell(
        world,
        world.events[top],
        center=(0.0, 0.0, 0.0),
        radius=19.0,
        material=collapse_mat,
    )
    animate_scale_in(shell, start_frame=430, duration=16)

    stamp_world(
        bpy.context.scene,
        world,
        "Spherepop cosmology: no ontologically privileged scale in recursive persistent history.",
    )


if __name__ == "__main__":
    main()
