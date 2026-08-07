from __future__ import annotations

import bpy
from mathutils import Vector

from .core import SPEvent, SPWorld


def reset_scene() -> None:
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)

    for datablocks in (
        bpy.data.meshes,
        bpy.data.curves,
        bpy.data.materials,
        bpy.data.cameras,
        bpy.data.lights,
        bpy.data.collections,
    ):
        for block in list(datablocks):
            if getattr(block, "users", 0) == 0 and block.name != "Collection":
                datablocks.remove(block)


def ensure_collection(name: str):
    collection = bpy.data.collections.get(name)
    if collection is None:
        collection = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(collection)
    return collection


def make_material(
    name: str,
    *,
    base=(0.8, 0.8, 0.8, 1.0),
    emission=(0.0, 0.0, 0.0, 1.0),
    emission_strength: float = 0.0,
    alpha: float = 1.0,
):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True

    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = base
    bsdf.inputs["Roughness"].default_value = 0.35

    if "Alpha" in bsdf.inputs:
        bsdf.inputs["Alpha"].default_value = alpha

    if "Emission Color" in bsdf.inputs:
        bsdf.inputs["Emission Color"].default_value = emission
        bsdf.inputs["Emission Strength"].default_value = emission_strength
    else:
        bsdf.inputs["Emission"].default_value = emission
        bsdf.inputs["Emission Strength"].default_value = emission_strength

    if alpha < 1.0:
        if hasattr(mat, "surface_render_method"):
            mat.surface_render_method = "DITHERED"
        elif hasattr(mat, "blend_method"):
            mat.blend_method = "BLEND"

    return mat


def create_event_sphere(
    world: SPWorld,
    event: SPEvent,
    location,
    *,
    radius: float = 0.45,
    material=None,
    collection=None,
):
    bpy.ops.mesh.primitive_ico_sphere_add(
        subdivisions=3,
        radius=radius,
        location=location,
    )
    obj = bpy.context.object
    obj.name = f"{event.op}_{event.eid:04d}"
    annotate_event_object(obj, event)

    if material is not None:
        obj.data.materials.append(material)

    if collection is not None:
        for existing in list(obj.users_collection):
            existing.objects.unlink(obj)
        collection.objects.link(obj)

    world.register_object(event.eid, obj.name)
    return obj


def create_collapse_shell(
    world: SPWorld,
    event: SPEvent,
    center,
    *,
    radius: float,
    material=None,
    collection=None,
):
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=radius,
        location=center,
        segments=28,
        ring_count=18,
    )
    obj = bpy.context.object
    obj.name = f"{event.op}_{event.eid:04d}_shell"
    annotate_event_object(obj, event)

    if material is not None:
        obj.data.materials.append(material)

    if collection is not None:
        for existing in list(obj.users_collection):
            existing.objects.unlink(obj)
        collection.objects.link(obj)

    world.register_object(event.eid, obj.name)
    return obj


def annotate_event_object(obj, event: SPEvent) -> None:
    obj["spherepop_eid"] = event.eid
    obj["spherepop_op"] = event.op
    obj["spherepop_frame"] = event.frame
    obj["spherepop_parents"] = list(event.parents)


def animate_scale_in(
    obj,
    *,
    start_frame: int,
    duration: int = 12,
    final_scale=(1.0, 1.0, 1.0),
):
    obj.scale = (0.001, 0.001, 0.001)
    obj.keyframe_insert(data_path="scale", frame=start_frame)

    obj.scale = final_scale
    obj.keyframe_insert(data_path="scale", frame=start_frame + duration)


def animate_scale_to(obj, *, start_frame: int, end_frame: int, scale_factor: float):
    obj.keyframe_insert(data_path="scale", frame=start_frame)
    obj.scale = tuple(scale_factor * s for s in obj.scale)
    obj.keyframe_insert(data_path="scale", frame=end_frame)


def _new_curve_between(name: str, start, end, *, bevel_depth: float = 0.035):
    curve_data = bpy.data.curves.new(name=f"{name}_curve", type="CURVE")
    curve_data.dimensions = "3D"
    curve_data.bevel_depth = bevel_depth
    curve_data.bevel_resolution = 4
    curve_data.resolution_u = 12

    spline = curve_data.splines.new(type="POLY")
    spline.points.add(1)
    spline.points[0].co = (*Vector(start), 1.0)
    spline.points[1].co = (*Vector(end), 1.0)

    obj = bpy.data.objects.new(name, curve_data)
    bpy.context.collection.objects.link(obj)
    return obj


def create_link_curve(
    world: SPWorld,
    event: SPEvent,
    start,
    end,
    *,
    material=None,
    bevel_depth: float = 0.035,
):
    obj = _new_curve_between(
        f"{event.op}_{event.eid:04d}",
        start,
        end,
        bevel_depth=bevel_depth,
    )
    annotate_event_object(obj, event)

    if material is not None:
        obj.data.materials.append(material)

    world.register_object(event.eid, obj.name)
    return obj


def animate_curve_reveal(
    obj,
    *,
    start_frame: int,
    duration: int = 12,
):
    curve = obj.data
    curve.bevel_factor_start = 0.0
    curve.bevel_factor_end = 0.0
    curve.keyframe_insert(data_path="bevel_factor_end", frame=start_frame)

    curve.bevel_factor_end = 1.0
    curve.keyframe_insert(data_path="bevel_factor_end", frame=start_frame + duration)


def mark_refused(
    obj,
    *,
    frame: int,
    archive_offset=(0.0, 0.0, -5.0),
    duration: int = 20,
    scale_factor: float = 0.7,
):
    start = obj.location.copy()
    end = start + Vector(archive_offset)

    obj.keyframe_insert(data_path="location", frame=frame)
    obj.keyframe_insert(data_path="scale", frame=frame)

    obj.location = end
    obj.scale = tuple(scale_factor * s for s in obj.scale)
    obj.keyframe_insert(data_path="location", frame=frame + duration)
    obj.keyframe_insert(data_path="scale", frame=frame + duration)

    obj["spherepop_refused"] = True
    obj["spherepop_refused_frame"] = frame


def add_camera(
    *,
    location=(0.0, -14.0, 8.0),
    target=(0.0, 0.0, 0.0),
    lens=50,
):
    bpy.ops.object.camera_add(location=location)
    cam = bpy.context.object
    cam.data.lens = lens

    direction = Vector(target) - cam.location
    cam.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()

    bpy.context.scene.camera = cam
    return cam


def add_world_light(
    *,
    energy: float = 900.0,
    location=(4.0, -4.0, 8.0),
):
    bpy.ops.object.light_add(type="AREA", location=location)
    light = bpy.context.object
    light.data.energy = energy
    light.data.shape = "DISK"
    light.data.size = 7.0
    return light


def add_ground(size: float = 30.0, location=(0, 0, -0.7)):
    bpy.ops.mesh.primitive_plane_add(size=size, location=location)
    plane = bpy.context.object
    plane.name = "Ground"
    return plane


def add_frontier_plane(*, size: float = 20.0, z: float = 0.0, material=None):
    bpy.ops.mesh.primitive_plane_add(size=size, location=(0.0, 0.0, z))
    plane = bpy.context.object
    plane.name = "FrontierPlane"
    if material is not None:
        plane.data.materials.append(material)
    return plane


def animate_location_z(obj, *, start_frame: int, end_frame: int, z_start: float, z_end: float):
    obj.location.z = z_start
    obj.keyframe_insert(data_path="location", frame=start_frame)
    obj.location.z = z_end
    obj.keyframe_insert(data_path="location", frame=end_frame)


def set_render_defaults(
    *,
    frame_end: int = 240,
    fps: int = 30,
    resolution=(1280, 720),
):
    scene = bpy.context.scene
    scene.frame_start = 1
    scene.frame_end = frame_end
    scene.render.fps = fps
    scene.render.resolution_x = resolution[0]
    scene.render.resolution_y = resolution[1]
    scene.render.resolution_percentage = 100


def stamp_world(scene, world: SPWorld, principle: str) -> None:
    scene["spherepop_event_count"] = len(world.events)
    scene["spherepop_frontier"] = sorted(world.frontier)
    scene["spherepop_principle"] = principle
