from __future__ import annotations

import itertools
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
    set_render_defaults(frame_end=380)

    world = SPWorld()
    positions = {}
    objects = {}

    building_mat = make_material(
        "CityBuilding",
        base=(0.3, 0.65, 0.9, 1.0),
        emission=(0.0, 0.2, 0.55, 1.0),
        emission_strength=0.9,
    )
    street_mat = make_material(
        "CityStreet",
        base=(0.9, 0.72, 0.2, 1.0),
        emission=(0.45, 0.3, 0.0, 1.0),
        emission_strength=0.7,
    )
    closed_mat = make_material(
        "ClosedStreet",
        base=(0.45, 0.45, 0.52, 1.0),
        emission=(0.08, 0.08, 0.08, 1.0),
        emission_strength=0.2,
        alpha=0.45,
    )
    neighborhood_mat = make_material(
        "NeighborhoodCollapse",
        base=(0.95, 0.3, 0.75, 1.0),
        emission=(0.75, 0.15, 0.65, 1.0),
        emission_strength=1.8,
        alpha=0.33,
    )
    district_mat = make_material(
        "DistrictCollapse",
        base=(0.3, 0.95, 0.65, 1.0),
        emission=(0.2, 0.85, 0.55, 1.0),
        emission_strength=1.8,
        alpha=0.28,
    )

    add_ground(size=52)
    add_world_light(energy=1200)
    add_camera(location=(0, -28, 18), target=(0, 0, 0.5), lens=38)

    grid = range(-2, 3)
    building_ids = []
    ordered_cells = list(itertools.product(grid, grid))

    for idx, (gx, gy) in enumerate(ordered_cells):
        frame = 10 + idx * 3
        loc = (gx * 2.5, gy * 2.5, 0.7)
        eid = pop(world, {"kind": "building", "grid": (gx, gy)}, frame=frame)
        positions[eid] = loc
        building_ids.append(eid)

        obj = create_event_sphere(world, world.events[eid], loc, radius=0.42, material=building_mat)
        animate_scale_in(obj, start_frame=frame, duration=6)
        objects[eid] = obj

        for micro in range(3):
            micro_eid = pop(
                world,
                {"kind": "building-internal", "building": eid, "idx": micro},
                frame=frame + 35 + micro * 4,
            )
            micro_loc = (
                loc[0] + (micro - 1) * 0.12,
                loc[1],
                loc[2] + 0.18 * (micro + 1),
            )
            micro_obj = create_event_sphere(world, world.events[micro_eid], micro_loc, radius=0.08, material=building_mat)
            animate_scale_in(micro_obj, start_frame=frame + 35 + micro * 4, duration=4)

    roads = []
    cell_to_eid = {cell: building_ids[idx] for idx, cell in enumerate(ordered_cells)}
    for gx, gy in ordered_cells:
        current = cell_to_eid[(gx, gy)]
        for neighbor in ((gx + 1, gy), (gx, gy + 1)):
            if neighbor in cell_to_eid:
                other = cell_to_eid[neighbor]
                frame = 95 + len(roads) * 2
                rid = bind(world, current, other, value={"kind": "street"}, frame=frame)
                roads.append(rid)
                line = create_link_curve(
                    world,
                    world.events[rid],
                    positions[current],
                    positions[other],
                    material=street_mat,
                    bevel_depth=0.02,
                )
                animate_curve_reveal(line, start_frame=frame, duration=6)

    closed_roads = roads[::5]
    for idx, rid in enumerate(closed_roads):
        frame = 190 + idx * 12
        refuse(world, rid, reason="zoning or closure", frame=frame)

    for idx, rid in enumerate(closed_roads):
        obj_name = world.objects.get(rid)
        if not obj_name:
            continue
        obj = bpy.data.objects.get(obj_name)
        if obj is None:
            continue
        mark_refused(obj, frame=200 + idx * 10, archive_offset=(0, 0, -3.5), duration=12, scale_factor=0.7)
        if hasattr(obj.data, "materials"):
            obj.data.materials.clear()
            obj.data.materials.append(closed_mat)

    neighborhoods = [
        [cell_to_eid[(x, y)] for x in (-2, -1, 0) for y in (-2, -1, 0)],
        [cell_to_eid[(x, y)] for x in (0, 1, 2) for y in (-2, -1, 0)],
        [cell_to_eid[(x, y)] for x in (-2, -1, 0) for y in (0, 1, 2)],
        [cell_to_eid[(x, y)] for x in (0, 1, 2) for y in (0, 1, 2)],
    ]
    collapsed_neighborhoods = []

    for idx, members in enumerate(neighborhoods):
        frame = 250 + idx * 14
        eid = collapse(world, *members, value={"kind": "neighborhood", "idx": idx}, frame=frame)
        collapsed_neighborhoods.append(eid)

        center = (
            sum(positions[e][0] for e in members) / len(members),
            sum(positions[e][1] for e in members) / len(members),
            1.0,
        )
        shell = create_collapse_shell(
            world,
            world.events[eid],
            center,
            radius=4.1,
            material=neighborhood_mat,
        )
        animate_scale_in(shell, start_frame=frame, duration=10)
        positions[eid] = center

    district = collapse(world, *collapsed_neighborhoods, value={"kind": "district"}, frame=320)
    shell = create_collapse_shell(
        world,
        world.events[district],
        center=(0.0, 0.0, 1.6),
        radius=9.8,
        material=district_mat,
    )
    animate_scale_in(shell, start_frame=320, duration=15)

    stamp_world(
        bpy.context.scene,
        world,
        "Recursive city: buildings pop, streets bind, closures refuse, neighborhoods collapse hierarchically.",
    )


if __name__ == "__main__":
    main()
