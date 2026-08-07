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


def centroid(points):
    count = len(points)
    return tuple(sum(p[i] for p in points) / count for i in range(3))


def max_radius(points, center):
    return max(math.dist(center, p) for p in points)


def main() -> None:
    reset_scene()
    set_render_defaults(frame_end=320)

    world = SPWorld()
    positions: dict[int, tuple[float, float, float]] = {}

    node_mat = make_material(
        "CollapseNode",
        base=(0.2, 0.6, 0.95, 1.0),
        emission=(0.0, 0.2, 0.7, 1.0),
        emission_strength=1.1,
    )
    bind_mat = make_material(
        "CollapseBind",
        base=(0.9, 0.6, 0.15, 1.0),
        emission=(0.5, 0.25, 0.05, 1.0),
        emission_strength=1.0,
    )
    shell_mat = make_material(
        "CollapseShell",
        base=(0.7, 0.2, 0.9, 1.0),
        emission=(0.35, 0.1, 0.65, 1.0),
        emission_strength=2.0,
        alpha=0.35,
    )
    super_shell_mat = make_material(
        "SuperCollapseShell",
        base=(0.95, 0.2, 0.55, 1.0),
        emission=(0.95, 0.2, 0.65, 1.0),
        emission_strength=2.4,
        alpha=0.3,
    )

    add_ground(size=34)
    add_world_light(energy=1000)
    add_camera(location=(0, -20, 11), target=(0, 0, 0.8))

    cluster_centers = [(-5.0, 0.0, 0.8), (0.0, 1.5, 0.9), (5.0, -0.4, 1.0)]
    collapsed_eids = []

    for cluster_idx, center in enumerate(cluster_centers):
        cluster_nodes = []
        for j in range(4):
            frame = 10 + cluster_idx * 26 + j * 6
            angle = j * (math.pi / 2.0) + cluster_idx * 0.3
            loc = (
                center[0] + 1.1 * math.cos(angle),
                center[1] + 1.1 * math.sin(angle),
                center[2] + 0.35 * math.sin(j),
            )
            eid = pop(world, {"cluster": cluster_idx, "idx": j}, frame=frame)
            positions[eid] = loc
            cluster_nodes.append(eid)

            obj = create_event_sphere(world, world.events[eid], loc, radius=0.35, material=node_mat)
            animate_scale_in(obj, start_frame=frame, duration=8)

        for k in range(len(cluster_nodes)):
            left = cluster_nodes[k]
            right = cluster_nodes[(k + 1) % len(cluster_nodes)]
            frame = 65 + cluster_idx * 20 + k * 5
            eid = bind(world, left, right, value={"cluster": cluster_idx}, frame=frame)
            line = create_link_curve(
                world,
                world.events[eid],
                positions[left],
                positions[right],
                material=bind_mat,
                bevel_depth=0.03,
            )
            animate_curve_reveal(line, start_frame=frame, duration=8)

        cframe = 120 + cluster_idx * 24
        collapse_eid = collapse(
            world,
            *cluster_nodes,
            value={"cluster": cluster_idx, "kind": "envelope"},
            frame=cframe,
        )
        collapsed_eids.append(collapse_eid)

        cluster_points = [positions[e] for e in cluster_nodes]
        center_pt = centroid(cluster_points)
        radius = max_radius(cluster_points, center_pt) + 0.85
        positions[collapse_eid] = center_pt

        shell = create_collapse_shell(
            world,
            world.events[collapse_eid],
            center_pt,
            radius=radius,
            material=shell_mat,
        )
        animate_scale_in(shell, start_frame=cframe, duration=14)

    super_frame = 235
    top = collapse(
        world,
        *collapsed_eids,
        value={"kind": "collapse-of-collapses"},
        frame=super_frame,
    )
    points = [positions[e] for e in collapsed_eids]
    c = centroid(points)
    r = max_radius(points, c) + 2.2
    shell = create_collapse_shell(
        world,
        world.events[top],
        c,
        radius=r,
        material=super_shell_mat,
    )
    animate_scale_in(shell, start_frame=super_frame, duration=18)

    stamp_world(
        bpy.context.scene,
        world,
        "Collapse creates new representations while retaining all parent distinctions.",
    )


if __name__ == "__main__":
    main()
