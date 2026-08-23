bl_info = {
    "name": "Object Side Symmetrizer",
    "version": (1, 0, 0),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > Object > Object Side Symmetrizer",
    "description": "Mirror selected left/right objects and rename counterparts using flexible side markers.",
    "category": "Object",
}

import re
from dataclasses import dataclass

import bpy
from bpy.props import BoolProperty, EnumProperty
from mathutils import Matrix


LEFT_TOKENS = {"l", "left"}
RIGHT_TOKENS = {"r", "right"}
DELIMITERS = "._-"


@dataclass
class SideName:
    side: str
    counterpart_name: str
    delimiter: str
    token: str


def strip_blender_numeric_suffix(name):
    match = re.match(r"^(.*?)(\.\d{3,})$", name)
    if match:
        return match.group(1)
    return name


def side_for_token(token):
    lowered = token.lower()
    if lowered in LEFT_TOKENS:
        return "LEFT"
    if lowered in RIGHT_TOKENS:
        return "RIGHT"
    return None


def token_for_side(source_token, target_side):
    source_lower = source_token.lower()
    if source_lower in {"l", "r"}:
        replacement = "l" if target_side == "LEFT" else "r"
    else:
        replacement = "left" if target_side == "LEFT" else "right"

    if source_token.isupper():
        return replacement.upper()
    if len(source_token) > 1 and source_token[0].isupper() and source_token[1:].islower():
        return replacement.title()
    return replacement


def parse_side_name(name, target_side=None):
    clean_name = strip_blender_numeric_suffix(name)

    prefix = re.match(rf"^([A-Za-z]+)([{re.escape(DELIMITERS)}])(.+)$", clean_name)
    if prefix:
        token, delimiter, rest = prefix.groups()
        source_side = side_for_token(token)
        if source_side and source_side != target_side:
            next_side = target_side or ("RIGHT" if source_side == "LEFT" else "LEFT")
            next_token = token_for_side(token, next_side)
            return SideName(source_side, f"{next_token}{delimiter}{rest}", delimiter, token)

    suffix = re.match(rf"^(.+)([{re.escape(DELIMITERS)}])([A-Za-z]+)$", clean_name)
    if suffix:
        rest, delimiter, token = suffix.groups()
        source_side = side_for_token(token)
        if source_side and source_side != target_side:
            next_side = target_side or ("RIGHT" if source_side == "LEFT" else "LEFT")
            next_token = token_for_side(token, next_side)
            return SideName(source_side, f"{rest}{delimiter}{next_token}", delimiter, token)

    return None


def unique_object_name(base_name):
    if base_name not in bpy.data.objects:
        return base_name

    index = 1
    while True:
        candidate = f"{base_name}.{index:03d}"
        if candidate not in bpy.data.objects:
            return candidate
        index += 1


def reflection_matrix(axis):
    if axis == "X":
        return Matrix.Diagonal((-1.0, 1.0, 1.0, 1.0))
    if axis == "Y":
        return Matrix.Diagonal((1.0, -1.0, 1.0, 1.0))
    return Matrix.Diagonal((1.0, 1.0, -1.0, 1.0))


def remove_object_and_data(obj):
    data = getattr(obj, "data", None)
    bpy.data.objects.remove(obj, do_unlink=True)
    if data and getattr(data, "users", 0) == 0:
        if isinstance(data, bpy.types.Mesh):
            bpy.data.meshes.remove(data)
        elif isinstance(data, bpy.types.Curve):
            bpy.data.curves.remove(data)
        elif isinstance(data, bpy.types.Armature):
            bpy.data.armatures.remove(data)
        elif isinstance(data, bpy.types.Camera):
            bpy.data.cameras.remove(data)
        elif isinstance(data, bpy.types.Light):
            bpy.data.lights.remove(data)


def duplicate_mirrored_object(source, target_name, axis="X", overwrite=True, flip_mesh_normals=True):
    existing = bpy.data.objects.get(target_name)
    if existing and overwrite:
        remove_object_and_data(existing)
    elif existing:
        target_name = unique_object_name(target_name)

    duplicate = source.copy()
    if getattr(source, "data", None):
        duplicate.data = source.data.copy()
        duplicate.data.name = target_name
    duplicate.animation_data_clear()
    duplicate.name = target_name
    duplicate.matrix_world = reflection_matrix(axis) @ source.matrix_world

    if flip_mesh_normals and duplicate.type == "MESH":
        duplicate.data.flip_normals()

    collections = source.users_collection or [bpy.context.collection]
    for collection in collections:
        collection.objects.link(duplicate)
    return duplicate


def selected_side_objects(context, side):
    matches = []
    skipped = []
    for obj in context.selected_objects:
        side_name = parse_side_name(obj.name)
        if not side_name:
            skipped.append(obj)
            continue
        if side_name.side == side:
            matches.append((obj, side_name))
    return matches, skipped


class OBJECTSIDESYMMETRIZER_Settings(bpy.types.PropertyGroup):
    operation: EnumProperty(
        name="Operation",
        description="Choose what to do with selected left/right objects",
        items=(
            ("LEFT_TO_RIGHT", "Symmetrize Left To Right", "Duplicate selected left objects as mirrored right objects"),
            ("RIGHT_TO_LEFT", "Symmetrize Right To Left", "Duplicate selected right objects as mirrored left objects"),
            ("DELETE_LEFT", "Delete Lefts", "Delete selected objects named as left objects"),
            ("DELETE_RIGHT", "Delete Rights", "Delete selected objects named as right objects"),
        ),
        default="LEFT_TO_RIGHT",
    )

    mirror_axis: EnumProperty(
        name="Mirror Axis",
        description="World axis to mirror across",
        items=(
            ("X", "X", "Mirror across the world X axis plane"),
            ("Y", "Y", "Mirror across the world Y axis plane"),
            ("Z", "Z", "Mirror across the world Z axis plane"),
        ),
        default="X",
    )

    overwrite_existing: BoolProperty(
        name="Overwrite Existing Counterparts",
        description="Replace an existing object with the target counterpart name",
        default=True,
    )

    flip_mesh_normals: BoolProperty(
        name="Flip Mesh Normals",
        description="Flip mesh normals on mirrored mesh copies",
        default=True,
    )

    dry_run: BoolProperty(
        name="Dry Run",
        description="Only report what would happen",
        default=True,
    )

    print_mapping: BoolProperty(
        name="Print Mapping",
        description="Print source and target names to the console",
        default=True,
    )


class OBJECTSIDESYMMETRIZER_OT_run(bpy.types.Operator):
    bl_idname = "object.object_side_symmetrizer_run"
    bl_label = "Run Object Side Operation"
    bl_description = "Mirror or delete selected objects based on left/right name markers"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        settings = context.scene.object_side_symmetrizer

        if settings.operation == "LEFT_TO_RIGHT":
            source_side = "LEFT"
            matches, skipped = selected_side_objects(context, source_side)
            verb = "Would mirror" if settings.dry_run else "Mirrored"
            for obj, side_name in matches:
                target_name = parse_side_name(obj.name, target_side="RIGHT").counterpart_name
                if settings.print_mapping:
                    print(f"Object Side Symmetrizer: {obj.name!r} -> {target_name!r}")
                if not settings.dry_run:
                    duplicate_mirrored_object(
                        obj,
                        target_name,
                        axis=settings.mirror_axis,
                        overwrite=settings.overwrite_existing,
                        flip_mesh_normals=settings.flip_mesh_normals,
                    )
            self.report({"INFO"}, f"{verb} {len(matches)} object(s). Skipped {len(skipped)}.")
            return {"FINISHED"}

        if settings.operation == "RIGHT_TO_LEFT":
            source_side = "RIGHT"
            matches, skipped = selected_side_objects(context, source_side)
            verb = "Would mirror" if settings.dry_run else "Mirrored"
            for obj, side_name in matches:
                target_name = parse_side_name(obj.name, target_side="LEFT").counterpart_name
                if settings.print_mapping:
                    print(f"Object Side Symmetrizer: {obj.name!r} -> {target_name!r}")
                if not settings.dry_run:
                    duplicate_mirrored_object(
                        obj,
                        target_name,
                        axis=settings.mirror_axis,
                        overwrite=settings.overwrite_existing,
                        flip_mesh_normals=settings.flip_mesh_normals,
                    )
            self.report({"INFO"}, f"{verb} {len(matches)} object(s). Skipped {len(skipped)}.")
            return {"FINISHED"}

        delete_side = "LEFT" if settings.operation == "DELETE_LEFT" else "RIGHT"
        matches, skipped = selected_side_objects(context, delete_side)
        verb = "Would delete" if settings.dry_run else "Deleted"
        for obj, side_name in matches:
            if settings.print_mapping:
                print(f"Object Side Symmetrizer: delete {obj.name!r}")
            if not settings.dry_run:
                remove_object_and_data(obj)

        self.report({"INFO"}, f"{verb} {len(matches)} object(s). Skipped {len(skipped)}.")
        return {"FINISHED"}


class OBJECTSIDESYMMETRIZER_PT_panel(bpy.types.Panel):
    bl_label = "Object Side Symmetrizer"
    bl_idname = "OBJECTSIDESYMMETRIZER_PT_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Object"

    def draw(self, context):
        layout = self.layout
        settings = context.scene.object_side_symmetrizer

        layout.prop(settings, "operation")
        if settings.operation in {"LEFT_TO_RIGHT", "RIGHT_TO_LEFT"}:
            layout.prop(settings, "mirror_axis")
            layout.prop(settings, "overwrite_existing")
            layout.prop(settings, "flip_mesh_normals")
        layout.prop(settings, "dry_run")
        layout.prop(settings, "print_mapping")
        layout.operator(OBJECTSIDESYMMETRIZER_OT_run.bl_idname)


classes = (
    OBJECTSIDESYMMETRIZER_Settings,
    OBJECTSIDESYMMETRIZER_OT_run,
    OBJECTSIDESYMMETRIZER_PT_panel,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.object_side_symmetrizer = bpy.props.PointerProperty(type=OBJECTSIDESYMMETRIZER_Settings)


def unregister():
    if hasattr(bpy.types.Scene, "object_side_symmetrizer"):
        del bpy.types.Scene.object_side_symmetrizer
    for cls in reversed(classes):
        try:
            bpy.utils.unregister_class(cls)
        except RuntimeError:
            pass


if __name__ == "__main__":
    register()
