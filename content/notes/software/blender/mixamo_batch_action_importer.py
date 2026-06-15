bl_info = {
    "name": "Mixamo Batch Action Importer",
    "author": "Codex",
    "version": (1, 0, 0),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > Animation > Mixamo Batch",
    "description": "Batch-import Mixamo FBX animation armatures as reusable Actions on an existing armature.",
    "category": "Animation",
}

import os
import re
import traceback
from datetime import datetime

import bpy
from mathutils import Matrix
from bpy.props import (
    BoolProperty,
    EnumProperty,
    IntProperty,
    PointerProperty,
    StringProperty,
)


BONE_PATH_RE = re.compile(r'pose\.bones\["([^"]+)"\]')


def default_log_path():
    blend_path = bpy.data.filepath
    if blend_path:
        return os.path.join(os.path.dirname(blend_path), "mixamo_batch_import.log")
    return os.path.join(os.path.dirname(__file__), "mixamo_batch_import.log")


class BatchLogger:
    def __init__(self, filepath=None, mirror_to_console=True):
        self.filepath = bpy.path.abspath(filepath) if filepath else default_log_path()
        self.mirror_to_console = mirror_to_console
        self._file = None

    def __enter__(self):
        directory = os.path.dirname(self.filepath)
        if directory:
            os.makedirs(directory, exist_ok=True)
        self._file = open(self.filepath, "w", encoding="utf-8")
        self.write(f"Mixamo Batch Action Importer log")
        self.write(f"Started: {datetime.now().isoformat(timespec='seconds')}")
        self.write(f"Blend file: {bpy.data.filepath or '<unsaved>'}")
        self.write(f"Blender: {bpy.app.version_string}")
        self.write("")
        return self

    def __exit__(self, exc_type, exc, tb):
        self.write("")
        self.write(f"Finished: {datetime.now().isoformat(timespec='seconds')}")
        if self._file:
            self._file.close()
            self._file = None

    def write(self, message=""):
        text = str(message)
        if self.mirror_to_console:
            print(text)
        if self._file:
            self._file.write(text + "\n")
            self._file.flush()

    def __call__(self, message=""):
        self.write(message)

    def exception(self, message):
        self.write(message)
        self.write(traceback.format_exc())


def action_name_from_file(filepath):
    name = os.path.splitext(os.path.basename(filepath))[0]
    name = name.strip().replace(" ", "_")
    name = re.sub(r"[^A-Za-z0-9_.-]+", "_", name)
    name = re.sub(r"_+", "_", name)
    return name.strip("_") or "Mixamo_Action"


def strip_mixamo_prefix(name):
    if ":" in name:
        name = name.split(":")[-1]
    if name.startswith("mixamorig_"):
        name = name[len("mixamorig_"):]
    if name.startswith("mixamorig"):
        name = name[len("mixamorig"):]
    return name


def is_ignored_end_bone(name):
    lowered = name.lower()
    return (
        lowered.endswith("_end")
        or lowered.endswith(".end")
        or lowered.endswith("-end")
        or lowered.endswith("end")
    )


def make_unique_action_name(base_name, overwrite):
    existing = bpy.data.actions.get(base_name)
    if overwrite and existing:
        bpy.data.actions.remove(existing)
        return base_name

    if not existing:
        return base_name

    index = 1
    while True:
        candidate = f"{base_name}.{index:03d}"
        if not bpy.data.actions.get(candidate):
            return candidate
        index += 1


def iter_action_fcurves(action):
    """Yield (fcurve, owning_collection) for both legacy and Blender 5 layered Actions."""
    if hasattr(action, "fcurves"):
        for fcurve in action.fcurves:
            yield fcurve, action.fcurves
        return

    for layer in getattr(action, "layers", []):
        for strip in getattr(layer, "strips", []):
            for channelbag in getattr(strip, "channelbags", []):
                for fcurve in channelbag.fcurves:
                    yield fcurve, channelbag.fcurves


def action_fcurve_count(action):
    return sum(1 for _fcurve, _owner in iter_action_fcurves(action))


def action_frame_range(action):
    if hasattr(action, "frame_range"):
        frame_range = action.frame_range
        return frame_range[0], frame_range[1]

    if hasattr(action, "curve_frame_range"):
        frame_range = action.curve_frame_range
        return frame_range[0], frame_range[1]

    return 1.0, 1.0


def copy_keyframe_points(src_fcurve, dst_fcurve):
    points = src_fcurve.keyframe_points
    dst_fcurve.keyframe_points.add(len(points))
    for src_point, dst_point in zip(points, dst_fcurve.keyframe_points):
        dst_point.co = src_point.co
        dst_point.handle_left = src_point.handle_left
        dst_point.handle_right = src_point.handle_right
        dst_point.interpolation = src_point.interpolation
        dst_point.easing = src_point.easing
        dst_point.back = src_point.back
        dst_point.amplitude = src_point.amplitude
        dst_point.period = src_point.period
        dst_point.type = src_point.type
    dst_fcurve.update()


def copy_fcurve(src_fcurve, dst_action, data_path, group_name=None):
    dst_fcurve = dst_action.fcurves.new(data_path=data_path, index=src_fcurve.array_index)
    dst_fcurve.color_mode = src_fcurve.color_mode
    dst_fcurve.extrapolation = src_fcurve.extrapolation

    if group_name:
        dst_fcurve.group = dst_action.groups.get(group_name) or dst_action.groups.new(group_name)
    elif src_fcurve.group:
        dst_fcurve.group = dst_action.groups.get(src_fcurve.group.name) or dst_action.groups.new(src_fcurve.group.name)

    copy_keyframe_points(src_fcurve, dst_fcurve)

    for src_modifier in src_fcurve.modifiers:
        try:
            dst_fcurve.modifiers.new(type=src_modifier.type)
        except Exception:
            pass

    return dst_fcurve


def copy_fcurve_to_datablock(src_fcurve, dst_action, datablock, data_path, group_name=None):
    dst_fcurve = dst_action.fcurve_ensure_for_datablock(
        datablock,
        data_path,
        index=src_fcurve.array_index,
        group_name=group_name or "",
    )

    dst_fcurve.color_mode = src_fcurve.color_mode
    dst_fcurve.extrapolation = src_fcurve.extrapolation

    if len(dst_fcurve.keyframe_points) > 0:
        for index in range(len(dst_fcurve.keyframe_points) - 1, -1, -1):
            dst_fcurve.keyframe_points.remove(dst_fcurve.keyframe_points[index], fast=True)

    copy_keyframe_points(src_fcurve, dst_fcurve)

    for src_modifier in src_fcurve.modifiers:
        try:
            dst_fcurve.modifiers.new(type=src_modifier.type)
        except Exception:
            pass

    return dst_fcurve


def remap_bone_data_path(data_path, main_bone_names, strip_prefixes, ignore_end_bones, warnings):
    match = BONE_PATH_RE.search(data_path)
    if not match:
        return data_path, None, True

    imported_name = match.group(1)
    candidate_names = [imported_name]

    stripped = strip_mixamo_prefix(imported_name) if strip_prefixes else imported_name
    if stripped not in candidate_names:
        candidate_names.append(stripped)

    for candidate in candidate_names:
        if candidate in main_bone_names:
            if candidate == imported_name:
                return data_path, candidate, True
            remapped_path = data_path.replace(f'pose.bones["{imported_name}"]', f'pose.bones["{candidate}"]')
            return remapped_path, candidate, True

    if ignore_end_bones and any(is_ignored_end_bone(name) for name in candidate_names):
        return data_path, imported_name, False

    warnings["missing_bones"].add(stripped)
    return data_path, imported_name, False


def copy_filtered_action(
    imported_action,
    main_armature,
    action_name,
    strip_prefixes=True,
    ignore_end_bones=True,
    fake_user=True,
):
    main_bone_names = {bone.name for bone in main_armature.data.bones}
    warnings = {
        "missing_bones": set(),
        "skipped_fcurves": 0,
        "copied_fcurves": 0,
    }

    # Build a fresh Action assigned to the real target armature. In Blender 5.x,
    # Actions have slots; copying the imported Action preserves the temporary
    # imported armature's slot, so the Action Editor shows/binds "Armature.001".
    new_action = bpy.data.actions.new(action_name)
    new_action.name = action_name
    new_action.use_fake_user = fake_user

    anim_data = ensure_animation_data(main_armature)
    previous_action = anim_data.action
    previous_slot = anim_data.action_slot if hasattr(anim_data, "action_slot") else None
    anim_data.action = new_action

    for src_fcurve, _fcurve_owner in list(iter_action_fcurves(imported_action)):
        remapped_path, group_name, keep = remap_bone_data_path(
            src_fcurve.data_path,
            main_bone_names,
            strip_prefixes,
            ignore_end_bones,
            warnings,
        )
        if not keep:
            warnings["skipped_fcurves"] += 1
            continue

        copy_fcurve_to_datablock(src_fcurve, new_action, main_armature, remapped_path, group_name=group_name)
        warnings["copied_fcurves"] += 1

    if previous_action:
        anim_data.action = previous_action
        if previous_slot and hasattr(anim_data, "action_slot"):
            try:
                anim_data.action_slot = previous_slot
            except Exception:
                pass
    else:
        anim_data.action = None

    return new_action, warnings


def map_imported_bones(imported_armature, main_armature, strip_prefixes=True, ignore_end_bones=True):
    main_bone_names = {bone.name for bone in main_armature.data.bones}
    warnings = {
        "missing_bones": set(),
        "skipped_fcurves": 0,
        "copied_fcurves": 0,
        "baked_bones": 0,
        "baked_frames": 0,
        "ignored_end_bones": 0,
    }
    bone_map = []

    for imported_bone in imported_armature.data.bones:
        imported_name = imported_bone.name
        stripped = strip_mixamo_prefix(imported_name) if strip_prefixes else imported_name
        candidates = [imported_name]
        if stripped not in candidates:
            candidates.append(stripped)

        target_name = next((name for name in candidates if name in main_bone_names), None)
        if target_name:
            bone_map.append((imported_name, target_name))
        elif ignore_end_bones and any(is_ignored_end_bone(name) for name in candidates):
            warnings["ignored_end_bones"] += 1
        else:
            warnings["missing_bones"].add(stripped)

    warnings["baked_bones"] = len(bone_map)
    return bone_map, warnings


def bake_retargeted_action(
    imported_armature,
    imported_action,
    main_armature,
    action_name,
    strip_prefixes=True,
    ignore_end_bones=True,
    fake_user=True,
    sample_step=1,
):
    scene = bpy.context.scene
    view_layer = bpy.context.view_layer
    sample_step = max(1, int(sample_step))

    bone_map, warnings = map_imported_bones(
        imported_armature,
        main_armature,
        strip_prefixes=strip_prefixes,
        ignore_end_bones=ignore_end_bones,
    )

    new_action = bpy.data.actions.new(action_name)
    new_action.name = action_name
    new_action.use_fake_user = fake_user

    src_anim_data = ensure_animation_data(imported_armature)
    dst_anim_data = ensure_animation_data(main_armature)
    previous_src_action = src_anim_data.action
    previous_dst_action = dst_anim_data.action
    previous_dst_slot = dst_anim_data.action_slot if hasattr(dst_anim_data, "action_slot") else None
    previous_frame = scene.frame_current
    disabled_constraints = []

    src_anim_data.action = imported_action
    dst_anim_data.action = new_action

    for pose_bone in main_armature.pose.bones:
        for constraint in pose_bone.constraints:
            if constraint.type == "IK":
                disabled_constraints.append((constraint, constraint.influence))
                constraint.influence = 0.0

    # Keep root/object motion from the FBX exactly, but bake pose bones against
    # the target rest pose. This avoids copying local rotations that only make
    # sense for the temporary imported armature's bone rolls/rest matrices.
    main_bone_names = {bone.name for bone in main_armature.data.bones}
    for src_fcurve, _fcurve_owner in list(iter_action_fcurves(imported_action)):
        if BONE_PATH_RE.search(src_fcurve.data_path):
            continue
        copy_fcurve_to_datablock(src_fcurve, new_action, main_armature, src_fcurve.data_path, group_name=None)
        warnings["copied_fcurves"] += 1

    frame_start, frame_end = action_frame_range(imported_action)
    start = int(frame_start)
    end = int(frame_end)
    if end < start:
        end = start

    inv_target_world = main_armature.matrix_world.inverted()
    frames = list(range(start, end + 1, sample_step))
    if frames[-1] != end:
        frames.append(end)

    try:
        for frame in frames:
            scene.frame_set(frame)
            view_layer.update()

            for imported_name, target_name in bone_map:
                src_pose_bone = imported_armature.pose.bones.get(imported_name)
                dst_pose_bone = main_armature.pose.bones.get(target_name)
                if not src_pose_bone or not dst_pose_bone:
                    continue

                dst_pose_bone.rotation_mode = "QUATERNION"
                target_object_space_matrix = inv_target_world @ imported_armature.matrix_world @ src_pose_bone.matrix
                dst_pose_bone.matrix = target_object_space_matrix

            view_layer.update()

            for _imported_name, target_name in bone_map:
                dst_pose_bone = main_armature.pose.bones.get(target_name)
                if not dst_pose_bone:
                    continue
                dst_pose_bone.keyframe_insert("location", frame=frame)
                dst_pose_bone.keyframe_insert("rotation_quaternion", frame=frame)
                dst_pose_bone.keyframe_insert("scale", frame=frame)

            warnings["baked_frames"] += 1

    finally:
        for constraint, influence in disabled_constraints:
            constraint.influence = influence
        scene.frame_set(previous_frame)
        src_anim_data.action = previous_src_action
        if previous_dst_action:
            dst_anim_data.action = previous_dst_action
            if previous_dst_slot and hasattr(dst_anim_data, "action_slot"):
                try:
                    dst_anim_data.action_slot = previous_dst_slot
                except Exception:
                    pass
        else:
            dst_anim_data.action = None

    return new_action, warnings


def bone_local_rest_matrix(armature, bone_name):
    bone = armature.data.bones[bone_name]
    if bone.parent:
        return bone.parent.matrix_local.inverted() @ bone.matrix_local
    return bone.matrix_local.copy()


def bone_rest_correction(imported_armature, imported_bone_name, main_armature, target_bone_name):
    source_rest = bone_local_rest_matrix(imported_armature, imported_bone_name).to_3x3().to_quaternion()
    target_rest = bone_local_rest_matrix(main_armature, target_bone_name).to_3x3().to_quaternion()
    return target_rest.inverted() @ source_rest


def rest_corrected_action(
    imported_armature,
    imported_action,
    main_armature,
    action_name,
    strip_prefixes=True,
    ignore_end_bones=True,
    fake_user=True,
    sample_step=1,
):
    scene = bpy.context.scene
    view_layer = bpy.context.view_layer
    sample_step = max(1, int(sample_step))

    bone_map, warnings = map_imported_bones(
        imported_armature,
        main_armature,
        strip_prefixes=strip_prefixes,
        ignore_end_bones=ignore_end_bones,
    )

    corrections = {
        (imported_name, target_name): bone_rest_correction(imported_armature, imported_name, main_armature, target_name)
        for imported_name, target_name in bone_map
    }

    new_action = bpy.data.actions.new(action_name)
    new_action.name = action_name
    new_action.use_fake_user = fake_user

    src_anim_data = ensure_animation_data(imported_armature)
    dst_anim_data = ensure_animation_data(main_armature)
    previous_src_action = src_anim_data.action
    previous_dst_action = dst_anim_data.action
    previous_dst_slot = dst_anim_data.action_slot if hasattr(dst_anim_data, "action_slot") else None
    previous_frame = scene.frame_current

    src_anim_data.action = imported_action
    dst_anim_data.action = new_action

    for src_fcurve, _fcurve_owner in list(iter_action_fcurves(imported_action)):
        if BONE_PATH_RE.search(src_fcurve.data_path):
            continue
        copy_fcurve_to_datablock(src_fcurve, new_action, main_armature, src_fcurve.data_path, group_name=None)
        warnings["copied_fcurves"] += 1

    frame_start, frame_end = action_frame_range(imported_action)
    start = int(frame_start)
    end = int(frame_end)
    if end < start:
        end = start

    frames = list(range(start, end + 1, sample_step))
    if frames[-1] != end:
        frames.append(end)

    try:
        for frame in frames:
            scene.frame_set(frame)
            view_layer.update()

            for imported_name, target_name in bone_map:
                src_pose_bone = imported_armature.pose.bones.get(imported_name)
                dst_pose_bone = main_armature.pose.bones.get(target_name)
                if not src_pose_bone or not dst_pose_bone:
                    continue

                correction = corrections[(imported_name, target_name)]
                source_basis = src_pose_bone.matrix_basis
                source_basis_rotation = source_basis.to_quaternion()
                target_rotation = correction @ source_basis_rotation @ correction.inverted()

                dst_pose_bone.rotation_mode = "QUATERNION"
                dst_pose_bone.location = src_pose_bone.location
                dst_pose_bone.rotation_quaternion = target_rotation
                dst_pose_bone.scale = src_pose_bone.scale

            view_layer.update()

            for _imported_name, target_name in bone_map:
                dst_pose_bone = main_armature.pose.bones.get(target_name)
                if not dst_pose_bone:
                    continue
                dst_pose_bone.keyframe_insert("location", frame=frame)
                dst_pose_bone.keyframe_insert("rotation_quaternion", frame=frame)
                dst_pose_bone.keyframe_insert("scale", frame=frame)

            warnings["baked_frames"] += 1

    finally:
        scene.frame_set(previous_frame)
        src_anim_data.action = previous_src_action
        if previous_dst_action:
            dst_anim_data.action = previous_dst_action
            if previous_dst_slot and hasattr(dst_anim_data, "action_slot"):
                try:
                    dst_anim_data.action_slot = previous_dst_slot
                except Exception:
                    pass
        else:
            dst_anim_data.action = None

    return new_action, warnings


def ensure_animation_data(obj):
    if obj.animation_data is None:
        obj.animation_data_create()
    return obj.animation_data


def bind_action_to_armature(main_armature, action):
    anim_data = ensure_animation_data(main_armature)
    anim_data.action = action
    if getattr(action, "slots", None) and len(action.slots) > 0 and hasattr(anim_data, "action_slot"):
        anim_data.action_slot = action.slots[0]
    return anim_data


def push_action_to_nla(main_armature, action, track_name):
    anim_data = ensure_animation_data(main_armature)
    track = anim_data.nla_tracks.new()
    track.name = track_name
    frame_start, _frame_end = action_frame_range(action)
    strip = track.strips.new(action.name, int(frame_start), action)
    strip.name = action.name
    if getattr(action, "slots", None) and len(action.slots) > 0 and hasattr(strip, "action_slot"):
        strip.action_slot = action.slots[0]
    return track, strip


def add_constraint_influence_keys(action, main_armature, constraint_type="IK", influence=0.0):
    frame_start, frame_end = action_frame_range(action)
    start = int(frame_start)
    end = int(frame_end)
    if end < start:
        end = start

    anim_data = ensure_animation_data(main_armature)
    previous_action = anim_data.action
    previous_slot = anim_data.action_slot if hasattr(anim_data, "action_slot") else None
    anim_data.action = action

    keyed = 0
    try:
        for pose_bone in main_armature.pose.bones:
            for constraint in pose_bone.constraints:
                if constraint.type != constraint_type:
                    continue

                data_path = f'pose.bones["{pose_bone.name}"].constraints["{constraint.name}"].influence'
                fcurve = action.fcurve_ensure_for_datablock(
                    main_armature,
                    data_path,
                    index=0,
                    group_name=pose_bone.name,
                )
                if len(fcurve.keyframe_points) > 0:
                    for index in range(len(fcurve.keyframe_points) - 1, -1, -1):
                        fcurve.keyframe_points.remove(fcurve.keyframe_points[index], fast=True)
                fcurve.keyframe_points.add(2)
                fcurve.keyframe_points[0].co = (start, influence)
                fcurve.keyframe_points[1].co = (end, influence)
                for point in fcurve.keyframe_points:
                    point.interpolation = "CONSTANT"
                fcurve.update()
                keyed += 1
    finally:
        if previous_action:
            anim_data.action = previous_action
            if previous_slot and hasattr(anim_data, "action_slot"):
                try:
                    anim_data.action_slot = previous_slot
                except Exception:
                    pass
        else:
            anim_data.action = None

    return keyed


def imported_armatures_from_objects(objects):
    armatures = [obj for obj in objects if obj.type == "ARMATURE"]
    animated = [obj for obj in armatures if obj.animation_data and obj.animation_data.action]
    return animated or armatures


def remove_objects(objects):
    for obj in objects:
        bpy.data.objects.remove(obj, do_unlink=True)


def remove_temporary_actions(actions, report_fn=print):
    for action in actions:
        action_name = action.name
        if action_name not in bpy.data.actions:
            continue

        report_fn(f"Deleting temporary imported Action {action_name}")
        action.use_fake_user = False
        bpy.data.actions.remove(action, do_unlink=True)


def import_fbx(filepath):
    before = set(bpy.data.objects)
    bpy.ops.import_scene.fbx(filepath=filepath, automatic_bone_orientation=False)
    after = set(bpy.data.objects)
    return list(after - before)


def batch_import_mixamo_actions(settings, report_fn=print):
    main_armature = settings.main_armature
    if not main_armature or main_armature.type != "ARMATURE":
        raise ValueError("Choose a valid main armature.")

    folder = bpy.path.abspath(settings.folder)
    if not folder or not os.path.isdir(folder):
        raise ValueError(f"Choose a valid FBX folder: {folder}")

    fbx_files = [
        os.path.join(folder, name)
        for name in sorted(os.listdir(folder))
        if name.lower().endswith(".fbx")
    ]

    summary = {
        "files": len(fbx_files),
        "actions_created": 0,
        "warnings": [],
        "errors": [],
    }

    if not fbx_files:
        report_fn(f"No FBX files found in {folder}")
        return summary

    for filepath in fbx_files:
        base_action_name = action_name_from_file(filepath) if settings.rename_from_filename else None
        imported_objects = []
        imported_actions_to_remove = []

        try:
            report_fn("")
            report_fn("=" * 80)
            report_fn(f"Importing {os.path.basename(filepath)}")
            report_fn(f"Path: {filepath}")
            imported_objects = import_fbx(filepath)
            report_fn(f"Imported object count: {len(imported_objects)}")
            for obj in imported_objects:
                action_name = "<none>"
                if obj.animation_data and obj.animation_data.action:
                    action_name = obj.animation_data.action.name
                data_name = obj.data.name if getattr(obj, "data", None) else "<none>"
                report_fn(f"  object name={obj.name!r} type={obj.type} data={data_name!r} action={action_name!r}")

            imported_armatures = imported_armatures_from_objects(imported_objects)
            report_fn(f"Candidate armatures: {[obj.name for obj in imported_armatures]}")

            if not imported_armatures:
                summary["errors"].append(f"{os.path.basename(filepath)}: no imported armature found")
                report_fn("ERROR: no imported armature found")
                continue

            imported_armature = imported_armatures[0]
            imported_action = imported_armature.animation_data.action if imported_armature.animation_data else None
            report_fn(f"Chosen armature: {imported_armature.name!r}")
            report_fn(f"Imported action: {imported_action.name if imported_action else '<none>'}")

            if not imported_action:
                summary["errors"].append(f"{os.path.basename(filepath)}: imported armature has no Action")
                report_fn("ERROR: imported armature has no Action")
                continue
            imported_actions_to_remove.append(imported_action)

            if not base_action_name:
                base_action_name = imported_action.name or action_name_from_file(filepath)

            action_name = make_unique_action_name(base_action_name, settings.overwrite_existing)
            report_fn(f"Output action name: {action_name}")
            report_fn(f"Imported fcurve count: {action_fcurve_count(imported_action)}")
            report_fn(f"Main armature bone count: {len(main_armature.data.bones)}")

            transfer_mode = getattr(settings, "transfer_mode", "COPY")
            bake_sample_step = getattr(settings, "bake_sample_step", 1)

            if transfer_mode == "REST_CORRECTED":
                new_action, warnings = rest_corrected_action(
                    imported_armature,
                    imported_action,
                    main_armature,
                    action_name,
                    strip_prefixes=settings.strip_mixamo_prefix,
                    ignore_end_bones=settings.ignore_end_bones,
                    fake_user=settings.mark_fake_user,
                    sample_step=bake_sample_step,
                )
                report_fn(
                    f"Rest-corrected {warnings['baked_bones']} bone(s) over "
                    f"{warnings['baked_frames']} frame sample(s)"
                )
                if warnings.get("ignored_end_bones"):
                    report_fn(f"Ignored {warnings['ignored_end_bones']} terminal/end bone(s)")
            elif transfer_mode == "BAKE":
                new_action, warnings = bake_retargeted_action(
                    imported_armature,
                    imported_action,
                    main_armature,
                    action_name,
                    strip_prefixes=settings.strip_mixamo_prefix,
                    ignore_end_bones=settings.ignore_end_bones,
                    fake_user=settings.mark_fake_user,
                    sample_step=bake_sample_step,
                )
                report_fn(
                    f"Baked {warnings['baked_bones']} bone(s) over "
                    f"{warnings['baked_frames']} frame sample(s)"
                )
                if warnings.get("ignored_end_bones"):
                    report_fn(f"Ignored {warnings['ignored_end_bones']} terminal/end bone(s)")
            else:
                new_action, warnings = copy_filtered_action(
                    imported_action,
                    main_armature,
                    action_name,
                    strip_prefixes=settings.strip_mixamo_prefix,
                    ignore_end_bones=settings.ignore_end_bones,
                    fake_user=settings.mark_fake_user,
                )

            keyed_constraints = 0
            if getattr(settings, "disable_ik_constraints_in_actions", True):
                keyed_constraints = add_constraint_influence_keys(new_action, main_armature, constraint_type="IK", influence=0.0)
                if keyed_constraints:
                    report_fn(f"Keyed {keyed_constraints} IK constraint influence(s) to 0 in Action")

            if settings.assign_last_action:
                bind_action_to_armature(main_armature, new_action)
                report_fn(f"Assigned Action {new_action.name} to {main_armature.name}")

            if settings.push_to_nla:
                push_action_to_nla(main_armature, new_action, action_name)

            summary["actions_created"] += 1

            if warnings["missing_bones"]:
                missing = ", ".join(sorted(warnings["missing_bones"]))
                summary["warnings"].append(f"{os.path.basename(filepath)}: missing bones skipped: {missing}")
                report_fn(f"Missing bones skipped: {missing}")

            if warnings["skipped_fcurves"]:
                summary["warnings"].append(
                    f"{os.path.basename(filepath)}: skipped {warnings['skipped_fcurves']} F-curves"
                )

            report_fn(
                f"Created Action {new_action.name}: copied {warnings['copied_fcurves']} direct F-curves, "
                f"skipped {warnings['skipped_fcurves']}"
            )

        except Exception as exc:
            summary["errors"].append(f"{os.path.basename(filepath)}: {exc}")
            if hasattr(report_fn, "exception"):
                report_fn.exception(f"EXCEPTION while importing {os.path.basename(filepath)}: {exc}")
            else:
                traceback.print_exc()
        finally:
            for obj in imported_objects:
                if obj.animation_data and obj.animation_data.action in imported_actions_to_remove:
                    obj.animation_data.action = None

            if settings.delete_temp_imports and imported_objects:
                report_fn(f"Deleting {len(imported_objects)} temporary imported object(s)")
                remove_objects(imported_objects)

            remove_temporary_actions(imported_actions_to_remove, report_fn=report_fn)

    report_fn("Mixamo batch import finished.")
    report_fn(f"Files processed: {summary['files']}")
    report_fn(f"Actions created: {summary['actions_created']}")
    report_fn(f"Warnings: {len(summary['warnings'])}")
    report_fn(f"Errors: {len(summary['errors'])}")
    for warning in summary["warnings"]:
        report_fn(f"WARNING: {warning}")
    for error in summary["errors"]:
        report_fn(f"ERROR: {error}")

    return summary


class MIXAMO_BATCH_Settings(bpy.types.PropertyGroup):
    main_armature: PointerProperty(
        name="Main Armature",
        description="Existing rig that should receive the imported Actions",
        type=bpy.types.Object,
        poll=lambda self, obj: obj.type == "ARMATURE",
    )

    folder: StringProperty(
        name="FBX Folder",
        description="Folder containing Mixamo animation FBX files",
        subtype="DIR_PATH",
    )

    transfer_mode: EnumProperty(
        name="Transfer Mode",
        description="How animation from each imported FBX should be transferred to the main armature",
        items=(
            (
                "REST_CORRECTED",
                "Rest-Pose Corrected",
                "Experimental: convert source bone-local rotations into the target armature's rest-pose axes",
            ),
            (
                "COPY",
                "Direct Copy Curves",
                "Copy matching F-curves directly; use only when the imported and target armatures have the same rest pose",
            ),
            (
                "BAKE",
                "Bake Retargeted Pose",
                "Experimental: sample the imported pose and key equivalent transforms on the selected armature",
            ),
        ),
        default="COPY",
    )

    bake_sample_step: IntProperty(
        name="Bake Every N Frames",
        description="Frame step for baked retarget mode. 1 preserves every source frame",
        default=1,
        min=1,
        max=30,
    )

    rename_from_filename: BoolProperty(
        name="Rename From Filename",
        default=True,
    )

    mark_fake_user: BoolProperty(
        name="Mark Fake User",
        default=True,
    )

    push_to_nla: BoolProperty(
        name="Push To NLA",
        default=False,
    )

    assign_last_action: BoolProperty(
        name="Assign Last Action",
        description="Assign each created Action to the main armature as it is created. Final result leaves the last Action active",
        default=False,
    )

    delete_temp_imports: BoolProperty(
        name="Delete Temporary Imports",
        default=True,
    )

    strip_mixamo_prefix: BoolProperty(
        name="Strip Mixamo Prefix",
        description='Strip prefixes such as "mixamorig:" from imported F-curve bone paths',
        default=True,
    )

    ignore_end_bones: BoolProperty(
        name="Ignore *_end Bones",
        description="Skip imported terminal/end-bone F-curves if those bones do not exist on the main rig",
        default=True,
    )

    disable_ik_constraints_in_actions: BoolProperty(
        name="Disable IK In Imported Actions",
        description="Key IK constraint influence to 0 so imported Mixamo FK bone curves are not overridden by IK controls",
        default=True,
    )

    overwrite_existing: BoolProperty(
        name="Overwrite Existing Actions",
        description="Delete existing Actions with the same imported name. If disabled, make unique names",
        default=False,
    )

    log_to_file: BoolProperty(
        name="Log To File",
        description="Write detailed diagnostics to a log file",
        default=True,
    )

    log_path: StringProperty(
        name="Log File",
        description="Detailed import log path. Empty uses mixamo_batch_import.log beside the saved blend file",
        subtype="FILE_PATH",
        default="",
    )


class MIXAMO_BATCH_OT_import(bpy.types.Operator):
    bl_idname = "object.mixamo_batch_import_actions"
    bl_label = "Import Mixamo Actions"
    bl_description = "Batch-import Mixamo FBX animation files as Actions for the selected main armature"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        settings = context.scene.mixamo_batch_importer

        try:
            if settings.log_to_file:
                log_path = settings.log_path.strip() or default_log_path()
                with BatchLogger(log_path, mirror_to_console=True) as logger:
                    summary = batch_import_mixamo_actions(settings, report_fn=logger)
                print(f"Mixamo batch log written to: {log_path}")
            else:
                summary = batch_import_mixamo_actions(settings, report_fn=print)
        except Exception as exc:
            self.report({"ERROR"}, str(exc))
            return {"CANCELLED"}

        if summary["errors"]:
            self.report(
                {"WARNING"},
                f"Created {summary['actions_created']} Action(s), with {len(summary['errors'])} error(s). See console.",
            )
        else:
            self.report({"INFO"}, f"Created {summary['actions_created']} Action(s). See console for details.")

        if settings.log_to_file:
            self.report({"INFO"}, f"Log: {settings.log_path.strip() or default_log_path()}")

        return {"FINISHED"}


class MIXAMO_BATCH_PT_panel(bpy.types.Panel):
    bl_label = "Mixamo Batch"
    bl_idname = "MIXAMO_BATCH_PT_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Animation"

    def draw(self, context):
        layout = self.layout
        settings = context.scene.mixamo_batch_importer

        layout.prop(settings, "main_armature")
        layout.prop(settings, "folder")

        box = layout.box()
        box.prop(settings, "transfer_mode")
        if settings.transfer_mode == "BAKE":
            box.prop(settings, "bake_sample_step")
        box.prop(settings, "rename_from_filename")
        box.prop(settings, "mark_fake_user")
        box.prop(settings, "push_to_nla")
        box.prop(settings, "assign_last_action")
        box.prop(settings, "delete_temp_imports")
        box.prop(settings, "strip_mixamo_prefix")
        box.prop(settings, "ignore_end_bones")
        box.prop(settings, "disable_ik_constraints_in_actions")
        box.prop(settings, "overwrite_existing")
        box.prop(settings, "log_to_file")
        if settings.log_to_file:
            box.prop(settings, "log_path")

        layout.operator(MIXAMO_BATCH_OT_import.bl_idname)


classes = (
    MIXAMO_BATCH_Settings,
    MIXAMO_BATCH_OT_import,
    MIXAMO_BATCH_PT_panel,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.mixamo_batch_importer = PointerProperty(type=MIXAMO_BATCH_Settings)


def unregister():
    if hasattr(bpy.types.Scene, "mixamo_batch_importer"):
        del bpy.types.Scene.mixamo_batch_importer
    for cls in reversed(classes):
        try:
            bpy.utils.unregister_class(cls)
        except RuntimeError:
            pass


if __name__ == "__main__":
    register()
