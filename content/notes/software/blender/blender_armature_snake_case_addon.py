bl_info = {
    "name": "Armature Snake Case Renamer",
    "version": (1, 0, 0),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > Animation > Armature Snake Case",
    "description": "Rename an armature and its bones to snake_case.",
    "category": "Animation",
}

import re

import bpy
from bpy.props import BoolProperty, PointerProperty


def camel_to_words(text):
    text = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", text)
    text = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", text)
    text = re.sub(r"([A-Za-z])([0-9])", r"\1_\2", text)
    text = re.sub(r"([0-9])([A-Za-z])", r"\1_\2", text)
    return text


def strip_blender_numeric_suffix(name):
    return re.sub(r"\.\d{3,}$", "", name)


def to_snake_case(text):
    text = strip_blender_numeric_suffix(text)
    text = text.replace("'", "")
    text = camel_to_words(text)
    text = re.sub(r"[^A-Za-z0-9]+", "_", text)
    text = re.sub(r"_+", "_", text)
    return text.strip("_").lower()


def unique_name(base_name, used_names):
    candidate = base_name or "bone"
    if candidate not in used_names:
        used_names.add(candidate)
        return candidate

    index = 2
    while True:
        candidate = f"{base_name}_{index:02d}"
        if candidate not in used_names:
            used_names.add(candidate)
            return candidate
        index += 1


def rename_plan_for_bones(armature):
    used_names = set()
    plan = {}
    for bone in armature.data.bones:
        new_name = unique_name(to_snake_case(bone.name), used_names)
        plan[bone.name] = new_name
    return plan


def rename_armature_bones(armature, plan):
    changed = 0
    for old_name, new_name in plan.items():
        if old_name == new_name:
            continue
        bone = armature.data.bones.get(old_name)
        if bone:
            bone.name = new_name
            changed += 1
    return changed


def meshes_using_armature(armature):
    for obj in bpy.data.objects:
        if obj.type != "MESH":
            continue
        for modifier in obj.modifiers:
            if modifier.type == "ARMATURE" and modifier.object == armature:
                yield obj
                break


def rename_vertex_groups_for_armature(armature, plan):
    changed = 0
    for mesh in meshes_using_armature(armature):
        for old_name, new_name in plan.items():
            group = mesh.vertex_groups.get(old_name)
            if group and old_name != new_name:
                group.name = new_name
                changed += 1
    return changed


def escaped_data_path_name(name):
    return name.replace("\\", "\\\\").replace('"', '\\"')


def iter_action_fcurves(action):
    if not action:
        return
    seen = set()
    if hasattr(action, "fcurves"):
        for fcurve in action.fcurves:
            pointer = fcurve.as_pointer()
            seen.add(pointer)
            yield fcurve
    for layer in getattr(action, "layers", []):
        for strip in getattr(layer, "strips", []):
            for channelbag in getattr(strip, "channelbags", []):
                for fcurve in getattr(channelbag, "fcurves", []):
                    pointer = fcurve.as_pointer()
                    if pointer not in seen:
                        seen.add(pointer)
                        yield fcurve


def update_action_bone_paths(plan):
    changed = 0
    replacements = [
        (
            f'pose.bones["{escaped_data_path_name(old_name)}"]',
            f'pose.bones["{escaped_data_path_name(new_name)}"]',
        )
        for old_name, new_name in plan.items()
        if old_name != new_name
    ]

    for action in bpy.data.actions:
        for fcurve in iter_action_fcurves(action):
            old_path = fcurve.data_path
            new_path = old_path
            for old_token, new_token in replacements:
                new_path = new_path.replace(old_token, new_token)
            if old_path != new_path:
                fcurve.data_path = new_path
                changed += 1
    return changed


def update_constraint_targets(armature, plan):
    changed = 0
    for obj in bpy.data.objects:
        constraint_collections = [obj.constraints]
        if obj.type == "ARMATURE":
            constraint_collections.extend(pose_bone.constraints for pose_bone in obj.pose.bones)

        for constraints in constraint_collections:
            for constraint in constraints:
                target = getattr(constraint, "target", None)
                subtarget = getattr(constraint, "subtarget", "")
                if target == armature and subtarget in plan and subtarget != plan[subtarget]:
                    constraint.subtarget = plan[subtarget]
                    changed += 1
    return changed


def rename_armature_object_and_data(armature):
    old_object_name = armature.name
    old_data_name = armature.data.name
    armature.name = to_snake_case(armature.name) or "armature"
    armature.data.name = to_snake_case(armature.data.name) or f"{armature.name}_data"
    return old_object_name != armature.name, old_data_name != armature.data.name


class ARMATURESNAKECASE_Settings(bpy.types.PropertyGroup):
    armature: PointerProperty(
        name="Armature",
        description="Armature to rename",
        type=bpy.types.Object,
        poll=lambda self, obj: obj.type == "ARMATURE",
    )

    rename_object_and_data: BoolProperty(
        name="Rename Armature Object/Data",
        description="Also rename the armature object and armature data-block",
        default=True,
    )

    update_vertex_groups: BoolProperty(
        name="Update Vertex Groups",
        description="Rename matching vertex groups on meshes using this armature",
        default=True,
    )

    update_actions: BoolProperty(
        name="Update Action Paths",
        description="Update Action F-curve paths that reference renamed pose bones",
        default=True,
    )

    update_constraints: BoolProperty(
        name="Update Constraint Targets",
        description="Update constraint subtargets that point at renamed bones",
        default=True,
    )

    dry_run: BoolProperty(
        name="Dry Run",
        description="Only print/report the rename plan",
        default=True,
    )

    print_mapping: BoolProperty(
        name="Print Mapping",
        description="Print old and new names to the console",
        default=True,
    )


class ARMATURESNAKECASE_OT_rename(bpy.types.Operator):
    bl_idname = "object.armature_snake_case_rename"
    bl_label = "Rename Armature To Snake Case"
    bl_description = "Rename the selected armature and its bones to snake_case"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        settings = context.scene.armature_snake_case
        armature = settings.armature or context.object

        if not armature or armature.type != "ARMATURE":
            self.report({"ERROR"}, "Choose an armature or select one")
            return {"CANCELLED"}

        plan = rename_plan_for_bones(armature)
        changed_bones = sum(1 for old_name, new_name in plan.items() if old_name != new_name)

        if settings.print_mapping:
            for old_name, new_name in plan.items():
                if old_name != new_name:
                    print(f"Armature Snake Case: bone {old_name!r} -> {new_name!r}")

        if settings.dry_run:
            self.report({"INFO"}, f"Would rename {changed_bones} bone(s).")
            return {"FINISHED"}

        renamed_object = False
        renamed_data = False
        if settings.rename_object_and_data:
            renamed_object, renamed_data = rename_armature_object_and_data(armature)

        vertex_groups = 0
        actions = 0
        constraints = 0
        if settings.update_vertex_groups:
            vertex_groups = rename_vertex_groups_for_armature(armature, plan)
        if settings.update_actions:
            actions = update_action_bone_paths(plan)
        if settings.update_constraints:
            constraints = update_constraint_targets(armature, plan)

        renamed_bones = rename_armature_bones(armature, plan)

        self.report(
            {"INFO"},
            (
                f"Renamed {renamed_bones} bone(s), {vertex_groups} vertex group(s), "
                f"{actions} Action path(s), {constraints} constraint target(s). "
                f"Object renamed {renamed_object}. Data renamed {renamed_data}."
            ),
        )
        return {"FINISHED"}


class ARMATURESNAKECASE_PT_panel(bpy.types.Panel):
    bl_label = "Armature Snake Case"
    bl_idname = "ARMATURESNAKECASE_PT_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Animation"

    def draw(self, context):
        layout = self.layout
        settings = context.scene.armature_snake_case

        layout.prop(settings, "armature")
        layout.prop(settings, "rename_object_and_data")
        layout.prop(settings, "update_vertex_groups")
        layout.prop(settings, "update_actions")
        layout.prop(settings, "update_constraints")
        layout.prop(settings, "dry_run")
        layout.prop(settings, "print_mapping")
        layout.operator(ARMATURESNAKECASE_OT_rename.bl_idname)


classes = (
    ARMATURESNAKECASE_Settings,
    ARMATURESNAKECASE_OT_rename,
    ARMATURESNAKECASE_PT_panel,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.armature_snake_case = PointerProperty(type=ARMATURESNAKECASE_Settings)


def unregister():
    if hasattr(bpy.types.Scene, "armature_snake_case"):
        del bpy.types.Scene.armature_snake_case
    for cls in reversed(classes):
        try:
            bpy.utils.unregister_class(cls)
        except RuntimeError:
            pass


if __name__ == "__main__":
    register()
