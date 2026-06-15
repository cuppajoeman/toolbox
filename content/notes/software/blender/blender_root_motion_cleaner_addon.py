bl_info = {
    "name": "Root Motion Cleaner",
    "author": "Codex",
    "version": (1, 0, 0),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > Animation > Root Motion Cleaner",
    "description": "Remove selected location axes from a root bone on the active Action or all Actions.",
    "category": "Animation",
}

import bpy
from bpy.props import BoolProperty, EnumProperty, PointerProperty, StringProperty


def iter_action_fcurves(action):
    if not action:
        return
    if hasattr(action, "fcurves"):
        yield from action.fcurves
        return
    for layer in getattr(action, "layers", []):
        for strip in getattr(layer, "strips", []):
            for channelbag in getattr(strip, "channelbags", []):
                for fcurve in getattr(channelbag, "fcurves", []):
                    yield fcurve


def active_action_for_armature(armature):
    if not armature or armature.type != "ARMATURE":
        return None
    if not armature.animation_data:
        return None
    return armature.animation_data.action


def root_location_path(root_bone_name):
    escaped_name = root_bone_name.replace("\\", "\\\\").replace('"', '\\"')
    return f'pose.bones["{escaped_name}"].location'


def action_has_slot_for_armature(action, armature):
    if not action or not armature:
        return False
    slots = getattr(action, "slots", None)
    if not slots:
        return True
    for slot in slots:
        if getattr(slot, "identifier", "") == armature.name:
            return True
    return False


def fcurve_first_value(fcurve):
    if not fcurve.keyframe_points:
        return 0.0
    return fcurve.keyframe_points[0].co.y


def flatten_fcurve(fcurve, mode):
    if mode == "ZERO":
        target_value = 0.0
    else:
        target_value = fcurve_first_value(fcurve)

    changed = 0
    for point in fcurve.keyframe_points:
        if point.co.y != target_value:
            point.co.y = target_value
            point.handle_left.y = target_value
            point.handle_right.y = target_value
            changed += 1
    if changed:
        fcurve.update()
    return changed


def clean_action_root_motion(action, root_bone_name, axes, mode, include_object_motion=False):
    root_path = root_location_path(root_bone_name)
    changed_curves = 0
    changed_keys = 0
    target_indices = {index for index, enabled in enumerate(axes) if enabled}

    for fcurve in list(iter_action_fcurves(action)):
        is_root_location = fcurve.data_path == root_path and fcurve.array_index in target_indices
        is_object_location = (
            include_object_motion
            and fcurve.data_path == "location"
            and fcurve.array_index in target_indices
        )
        if not is_root_location and not is_object_location:
            continue

        changed = flatten_fcurve(fcurve, mode)
        if changed:
            changed_curves += 1
            changed_keys += changed

    return changed_curves, changed_keys


class ROOTMOTIONCLEANER_Settings(bpy.types.PropertyGroup):
    armature: PointerProperty(
        name="Armature",
        description="Armature whose active Action is used when Scope is Active Action",
        type=bpy.types.Object,
        poll=lambda self, obj: obj.type == "ARMATURE",
    )

    root_bone_name: StringProperty(
        name="Root Bone",
        description="Bone whose location curves should be flattened",
        default="main",
    )

    scope: EnumProperty(
        name="Scope",
        description="Choose whether to clean the active Action or all Actions",
        items=(
            ("ACTIVE", "Active Action", "Clean only the Action currently assigned to the chosen armature"),
            ("ALL", "All Actions", "Clean every Action in the file"),
        ),
        default="ACTIVE",
    )

    mode: EnumProperty(
        name="Mode",
        description="How to flatten root movement",
        items=(
            ("KEEP_FIRST", "Keep First Frame", "Set each selected location axis to its first keyed value"),
            ("ZERO", "Zero", "Set each selected location axis to 0"),
        ),
        default="KEEP_FIRST",
    )

    axis_x: BoolProperty(name="X", default=True)
    axis_y: BoolProperty(name="Y", default=True)
    axis_z: BoolProperty(name="Z", default=True)

    include_object_motion: BoolProperty(
        name="Also Clean Object Location",
        description="Also flatten Action curves on the armature object's own location",
        default=False,
    )


class ROOTMOTIONCLEANER_OT_clean(bpy.types.Operator):
    bl_idname = "object.root_motion_cleaner_clean"
    bl_label = "Clean Root Motion"
    bl_description = "Flatten selected root-bone location axes on the active Action or all Actions"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        settings = context.scene.root_motion_cleaner
        armature = settings.armature or context.object

        if not settings.root_bone_name.strip():
            self.report({"ERROR"}, "Root Bone is required")
            return {"CANCELLED"}

        axes = (settings.axis_x, settings.axis_y, settings.axis_z)
        if not any(axes):
            self.report({"ERROR"}, "Enable at least one axis")
            return {"CANCELLED"}

        if settings.scope == "ACTIVE":
            if not armature or armature.type != "ARMATURE":
                self.report({"ERROR"}, "Choose an armature or select one")
                return {"CANCELLED"}
            action = active_action_for_armature(armature)
            if not action:
                self.report({"ERROR"}, "Chosen armature has no active Action")
                return {"CANCELLED"}
            actions = [action]
        else:
            actions = list(bpy.data.actions)

        total_curves = 0
        total_keys = 0
        cleaned_actions = 0
        skipped_actions = 0

        for action in actions:
            if settings.scope == "ALL" and armature and armature.type == "ARMATURE":
                if not action_has_slot_for_armature(action, armature):
                    skipped_actions += 1
                    continue

            changed_curves, changed_keys = clean_action_root_motion(
                action,
                settings.root_bone_name.strip(),
                axes,
                settings.mode,
                include_object_motion=settings.include_object_motion,
            )
            if changed_curves:
                cleaned_actions += 1
                total_curves += changed_curves
                total_keys += changed_keys

        self.report(
            {"INFO"},
            f"Cleaned {cleaned_actions} Action(s), {total_curves} curve(s), {total_keys} key(s). Skipped {skipped_actions}.",
        )
        return {"FINISHED"}


class ROOTMOTIONCLEANER_PT_panel(bpy.types.Panel):
    bl_label = "Root Motion Cleaner"
    bl_idname = "ROOTMOTIONCLEANER_PT_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Animation"

    def draw(self, context):
        layout = self.layout
        settings = context.scene.root_motion_cleaner

        layout.prop(settings, "armature")
        layout.prop(settings, "root_bone_name")
        layout.prop(settings, "scope")
        layout.prop(settings, "mode")

        row = layout.row(align=True)
        row.prop(settings, "axis_x", toggle=True)
        row.prop(settings, "axis_y", toggle=True)
        row.prop(settings, "axis_z", toggle=True)

        layout.prop(settings, "include_object_motion")
        layout.operator(ROOTMOTIONCLEANER_OT_clean.bl_idname)


classes = (
    ROOTMOTIONCLEANER_Settings,
    ROOTMOTIONCLEANER_OT_clean,
    ROOTMOTIONCLEANER_PT_panel,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.root_motion_cleaner = PointerProperty(type=ROOTMOTIONCLEANER_Settings)


def unregister():
    if hasattr(bpy.types.Scene, "root_motion_cleaner"):
        del bpy.types.Scene.root_motion_cleaner
    for cls in reversed(classes):
        try:
            bpy.utils.unregister_class(cls)
        except RuntimeError:
            pass


if __name__ == "__main__":
    register()
