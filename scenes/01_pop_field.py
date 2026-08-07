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
    add_ground,
    add_world_light,
    animate_scale_in,
    animate_scale_to,
    create_event_sphere,
    ensure_collection,
    make_material,
    reset_scene,
    set_render_defaults,
    stamp_world,
)
from spherepop_blender.core import SPWorld, pop


def add_nested_pop_field(world: SPWorld, host_eid: int, host_location, start_frame: int, nested_mat):
    nested_collection = ensure_collection(f"NestedPop_{host_eid:03d}")
    for j in range(5):
        frame = start_frame + j * 4
        eid = pop(
            world,
            {
                "label": f"nested-{host_eid}-{j}",
                "host": host_eid,
            },
            frame=frame,
        )
        offset = (
            0.2 * math.cos(j * 1.2),
            0.2 * math.sin(j * 1.2),
            0.2 * (j - 2),
        )
        loc = (
            host_location[0] + offset[0],
            host_location[1] + offset[1],
            host_location[2] + offset[2],
        )
        obj = create_event_sphere(
            world,
            world.events[eid],
            loc,
            radius=0.08,
            material=nested_mat,
            collection=nested_collection,
        )
        animate_scale_in(obj, start_frame=frame, duration=6)


def main() -> None:
    reset_scene()
    set_render_defaults(frame_end=280)

    world = SPWorld()
    rng = random.Random(11)

    active_mat = make_material(
        "PopActive",
        base=(0.15, 0.35, 0.95, 1.0),
        emission=(0.1, 0.25, 1.0, 1.0),
        emission_strength=2.0,
    )
    nested_mat = make_material(
        "NestedPop",
        base=(0.95, 0.6, 0.2, 1.0),
        emission=(0.8, 0.25, 0.05, 1.0),
        emission_strength=1.6,
    )

    add_ground()
    add_world_light()
    add_camera(location=(0, -17, 9), target=(0, 0, 1.8))

    total = 20
    for i in range(total):
        frame = 10 + i * 10
        angle = i * 0.85
        radius = 1.2 + 0.18 * i
        z = -0.3 + 0.22 * i

        x = math.cos(angle) * radius + rng.uniform(-0.3, 0.3)
        y = math.sin(angle) * radius + rng.uniform(-0.3, 0.3)

        eid = pop(world, {"label": f"d{i}", "creation_order": i}, frame=frame)
        event = world.events[eid]

        obj = create_event_sphere(
            world,
            event,
            (x, y, z),
            radius=0.4,
            material=active_mat,
        )
        animate_scale_in(obj, start_frame=frame, duration=8)

        salience_floor = 0.28 + (0.6 * (i / (total - 1)))
        animate_scale_to(
            obj,
            start_frame=frame + 12,
            end_frame=260,
            scale_factor=salience_floor,
        )

        if i % 6 == 0 and i > 0:
            add_nested_pop_field(
                world,
                eid,
                (x, y, z),
                start_frame=frame + 18,
                nested_mat=nested_mat,
            )

    stamp_world(
        scene=bpy.context.scene,
        world=world,
        principle="Pop accumulates distinctions; nested fields preserve ancestry.",
    )


if __name__ == "__main__":
    main()
