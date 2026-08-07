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
    mark_refused,
    reset_scene,
    set_render_defaults,
    stamp_world,
)
from spherepop_blender.core import SPWorld, bind, pop, refuse


def main() -> None:
    reset_scene()
    set_render_defaults(frame_end=300)

    world = SPWorld()
    positions: dict[int, tuple[float, float, float]] = {}
    objects = {}

    active_mat = make_material(
        "ActiveFrontier",
        base=(0.15, 0.75, 0.55, 1.0),
        emission=(0.0, 0.45, 0.2, 1.0),
        emission_strength=1.7,
    )
    relation_mat = make_material(
        "HistoricalRelation",
        base=(0.8, 0.75, 0.2, 1.0),
        emission=(0.4, 0.3, 0.0, 1.0),
        emission_strength=0.8,
    )
    archive_mat = make_material(
        "ArchiveMarker",
        base=(0.35, 0.35, 0.4, 1.0),
        emission=(0.05, 0.05, 0.08, 1.0),
        emission_strength=0.2,
        alpha=0.5,
    )

    add_ground()
    add_world_light()
    add_camera(location=(0, -18, 10), target=(0, 0, -0.8))

    count = 10
    for i in range(count):
        frame = 10 + i * 5
        angle = (2.0 * math.pi * i) / count
        pos = (4.2 * math.cos(angle), 4.2 * math.sin(angle), 0.6)

        eid = pop(world, {"label": f"candidate-{i}"}, frame=frame)
        positions[eid] = pos

        obj = create_event_sphere(world, world.events[eid], pos, radius=0.42, material=active_mat)
        animate_scale_in(obj, start_frame=frame, duration=8)
        objects[eid] = obj

    relation_pairs = [(0, 2), (2, 4), (4, 6), (6, 8), (8, 0)]
    relation_ids = []
    for idx, (left, right) in enumerate(relation_pairs):
        frame = 75 + idx * 10
        eid = bind(world, left, right, value={"kind": "pre-refusal relation"}, frame=frame)
        relation_ids.append(eid)
        link = create_link_curve(
            world,
            world.events[eid],
            positions[left],
            positions[right],
            material=relation_mat,
            bevel_depth=0.035,
        )
        animate_curve_reveal(link, start_frame=frame, duration=9)

    targets = [2, 5, 8]
    for idx, target in enumerate(targets):
        frame = 145 + idx * 28
        refuse(world, target, reason="excluded from current continuation", frame=frame)

        obj = objects[target]
        mark_refused(
            obj,
            frame=frame,
            archive_offset=(0.0, 0.0, -5.5),
            duration=20,
            scale_factor=0.75,
        )

        marker_event = world.events[-1]
        marker = create_event_sphere(
            world,
            marker_event,
            (obj.location.x, obj.location.y, -4.8),
            radius=0.15,
            material=archive_mat,
        )
        animate_scale_in(marker, start_frame=frame + 12, duration=8)

    for idx, rid in enumerate(relation_ids[:3]):
        left, right = world.events[rid].parents
        history_bind = bind(
            world,
            left,
            right,
            value={"kind": "historical-reference"},
            frame=230 + idx * 12,
        )
        line = create_link_curve(
            world,
            world.events[history_bind],
            (positions[left][0], positions[left][1], positions[left][2] - 4.8),
            (positions[right][0], positions[right][1], positions[right][2] - 4.8),
            material=archive_mat,
            bevel_depth=0.02,
        )
        animate_curve_reveal(line, start_frame=230 + idx * 12, duration=10)

    stamp_world(
        bpy.context.scene,
        world,
        "Refusal moves distinctions out of participation without deleting history.",
    )


if __name__ == "__main__":
    main()
