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
    ensure_collection,
    make_material,
    reset_scene,
    set_render_defaults,
    stamp_world,
)
from spherepop_blender.core import SPWorld, bind, collapse, pop, refuse


def animate_camera_path(cam):
    cam.location = (0.0, -24.0, 12.0)
    cam.keyframe_insert(data_path="location", frame=1)
    cam.location = (-7.0, -9.0, 5.5)
    cam.keyframe_insert(data_path="location", frame=140)
    cam.location = (-7.0, -3.0, 2.4)
    cam.keyframe_insert(data_path="location", frame=190)
    cam.location = (4.0, -14.0, 9.0)
    cam.keyframe_insert(data_path="location", frame=320)


def micro_world(world: SPWorld, host_eid: int, host_pos, base_frame: int, mat, bind_mat, collapse_mat):
    col = ensure_collection(f"MicroWorld_{host_eid:03d}")
    micro_nodes = []
    points = []

    for i in range(5):
        frame = base_frame + i * 8
        eid = pop(world, {"host": host_eid, "micro": i}, frame=frame)
        angle = (2.0 * math.pi * i) / 5.0
        loc = (
            host_pos[0] + 0.9 * math.cos(angle),
            host_pos[1] + 0.9 * math.sin(angle),
            host_pos[2] + 0.2 * math.sin(i),
        )
        points.append(loc)
        micro_nodes.append(eid)

        obj = create_event_sphere(world, world.events[eid], loc, radius=0.12, material=mat, collection=col)
        animate_scale_in(obj, start_frame=frame, duration=7)

    for i in range(len(micro_nodes)):
        left = micro_nodes[i]
        right = micro_nodes[(i + 1) % len(micro_nodes)]
        frame = base_frame + 52 + i * 6
        eid = bind(world, left, right, value={"host": host_eid, "kind": "micro-bind"}, frame=frame)
        link = create_link_curve(
            world,
            world.events[eid],
            points[i],
            points[(i + 1) % len(points)],
            material=bind_mat,
            bevel_depth=0.012,
        )
        animate_curve_reveal(link, start_frame=frame, duration=6)

    refuse(world, micro_nodes[1], reason="micro frontier exclusion", frame=base_frame + 96)

    collapse_frame = base_frame + 116
    ceid = collapse(world, *micro_nodes, value={"host": host_eid, "kind": "micro-collapse"}, frame=collapse_frame)
    center = (
        sum(p[0] for p in points) / len(points),
        sum(p[1] for p in points) / len(points),
        sum(p[2] for p in points) / len(points),
    )
    shell = create_collapse_shell(
        world,
        world.events[ceid],
        center,
        radius=1.1,
        material=collapse_mat,
        collection=col,
    )
    animate_scale_in(shell, start_frame=collapse_frame, duration=11)

    return ceid


def main() -> None:
    reset_scene()
    set_render_defaults(frame_end=380)

    world = SPWorld()

    outer_mat = make_material(
        "OuterDistinction",
        base=(0.2, 0.8, 1.0, 1.0),
        emission=(0.05, 0.35, 0.9, 1.0),
        emission_strength=1.7,
    )
    micro_mat = make_material(
        "MicroDistinction",
        base=(0.95, 0.8, 0.15, 1.0),
        emission=(0.95, 0.55, 0.0, 1.0),
        emission_strength=1.1,
    )
    micro_bind = make_material(
        "MicroBind",
        base=(0.95, 0.45, 0.2, 1.0),
        emission=(0.7, 0.2, 0.1, 1.0),
        emission_strength=1.0,
    )
    collapse_mat = make_material(
        "MicroCollapse",
        base=(0.85, 0.2, 0.95, 1.0),
        emission=(0.6, 0.1, 0.85, 1.0),
        emission_strength=2.2,
        alpha=0.35,
    )

    add_ground(size=42)
    add_world_light(energy=1100)
    cam = add_camera(location=(0, -24, 12), target=(0, 0, 2), lens=42)
    animate_camera_path(cam)

    hosts = [(-7.0, 0.0, 2.5), (0.0, 0.5, 2.7), (7.0, -0.6, 2.9)]
    host_nodes = []
    host_objects = []

    for i, pos in enumerate(hosts):
        frame = 12 + i * 12
        eid = pop(world, {"label": f"host-{i}"}, frame=frame)
        host_nodes.append(eid)
        obj = create_event_sphere(world, world.events[eid], pos, radius=2.0, material=outer_mat)
        animate_scale_in(obj, start_frame=frame, duration=12)
        host_objects.append(obj)

    local_collapses = []
    for i, host in enumerate(host_nodes):
        ceid = micro_world(
            world,
            host,
            hosts[i],
            base_frame=80 + i * 22,
            mat=micro_mat,
            bind_mat=micro_bind,
            collapse_mat=collapse_mat,
        )
        local_collapses.append(ceid)

        pulse_frame = 210 + i * 20
        host_obj = host_objects[i]
        host_obj.keyframe_insert(data_path="scale", frame=pulse_frame)
        host_obj.scale = tuple(s * 1.15 for s in host_obj.scale)
        host_obj.keyframe_insert(data_path="scale", frame=pulse_frame + 10)
        host_obj.scale = tuple(s / 1.15 for s in host_obj.scale)
        host_obj.keyframe_insert(data_path="scale", frame=pulse_frame + 20)

    top = collapse(world, *local_collapses, value={"kind": "macro-from-micro"}, frame=300)
    shell = create_collapse_shell(
        world,
        world.events[top],
        center=(0.0, 0.0, 2.8),
        radius=10.5,
        material=collapse_mat,
    )
    animate_scale_in(shell, start_frame=300, duration=18)

    stamp_world(
        bpy.context.scene,
        world,
        "Nested continuations let local histories construct representations at enclosing scales.",
    )


if __name__ == "__main__":
    main()
