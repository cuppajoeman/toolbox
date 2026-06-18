bl_info = {
    "name": "Empty Action Cleaner",
    "version": (1, 0, 0),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > Animation > Empty Action Cleaner",
    "description": "Delete Blender Actions that contain no animation keyframe data.",
    "category": "Animation",
}

import bpy
from bpy.props import BoolProperty, EnumProperty, IntProperty, PointerProperty


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


def action_keyframe_count(action):
    return sum(len(fcurve.keyframe_points) for fcurve in iter_action_fcurves(action))


def action_distinct_keyed_frames(action):
    frames = set()
    for fcurve in iter_action_fcurves(action):
        for point in fcurve.keyframe_points:
            frames.add(round(float(point.co.x), 6))
            if len(frames) > 1:
                return frames
    return frames


def action_has_animation_data(action, min_distinct_frames=2):
    return len(action_distinct_keyed_frames(action)) >= min_distinct_frames


def active_action_for_armature(armature):
    if not armature or armature.type != "ARMATURE":
        return None
    if not armature.animation_data:
        return None
    return armature.animation_data.action


def action_users_description(action):
    return f"users={action.users}, fake_user={action.use_fake_user}"


class EMPTYACTIONCLEANER_Settings(bpy.types.PropertyGroup):
    armature: PointerProperty(
        name="Armature",
        description="Armature whose active Action should be checked when Scope is Active Action",
        type=bpy.types.Object,
        poll=lambda self, obj: obj.type == "ARMATURE",
    )

    scope: EnumProperty(
        name="Scope",
        description="Choose whether to check the active Action or all Actions",
        items=(
            ("ACTIVE", "Active Action", "Check only the Action currently assigned to the chosen armature"),
            ("ALL", "All Actions", "Check every Action in the file"),
        ),
        default="ALL",
    )

    dry_run: BoolProperty(
        name="Dry Run",
        description="Only report what would be deleted",
        default=True,
    )

    print_details: BoolProperty(
        name="Print Details",
        description="Print deleted or skipped Action names to the console",
        default=True,
    )

    min_distinct_frames: IntProperty(
        name="Min Keyed Frames",
        description="Actions with fewer distinct keyed frames than this are deleted",
        default=2,
        min=1,
        max=100,
    )


class EMPTYACTIONCLEANER_OT_clean(bpy.types.Operator):
    bl_idname = "object.empty_action_cleaner_clean"
    bl_label = "Delete Empty Actions"
    bl_description = "Delete Actions that contain no keyframe animation data"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        settings = context.scene.empty_action_cleaner
        armature = settings.armature or context.object

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

        empty_actions = [
            action for action in actions
            if not action_has_animation_data(action, settings.min_distinct_frames)
        ]
        animated_count = len(actions) - len(empty_actions)

        if settings.print_details:
            for action in empty_actions:
                verb = "Would delete" if settings.dry_run else "Deleting"
                frame_count = len(action_distinct_keyed_frames(action))
                print(
                    f"Empty Action Cleaner: {verb} {action.name!r} "
                    f"(distinct_keyed_frames={frame_count}, {action_users_description(action)})"
                )

        if not settings.dry_run:
            for action in empty_actions:
                bpy.data.actions.remove(action, do_unlink=True)

        action_word = "would delete" if settings.dry_run else "deleted"
        self.report(
            {"INFO"},
            f"{action_word.capitalize()} {len(empty_actions)} empty Action(s). Kept {animated_count} animated Action(s).",
        )
        return {"FINISHED"}


class EMPTYACTIONCLEANER_PT_panel(bpy.types.Panel):
    bl_label = "Empty Action Cleaner"
    bl_idname = "EMPTYACTIONCLEANER_PT_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Animation"

    def draw(self, context):
        layout = self.layout
        settings = context.scene.empty_action_cleaner

        layout.prop(settings, "scope")
        if settings.scope == "ACTIVE":
            layout.prop(settings, "armature")
        layout.prop(settings, "dry_run")
        layout.prop(settings, "min_distinct_frames")
        layout.prop(settings, "print_details")
        layout.operator(EMPTYACTIONCLEANER_OT_clean.bl_idname)


classes = (
    EMPTYACTIONCLEANER_Settings,
    EMPTYACTIONCLEANER_OT_clean,
    EMPTYACTIONCLEANER_PT_panel,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.empty_action_cleaner = PointerProperty(type=EMPTYACTIONCLEANER_Settings)


def unregister():
    if hasattr(bpy.types.Scene, "empty_action_cleaner"):
        del bpy.types.Scene.empty_action_cleaner
    for cls in reversed(classes):
        try:
            bpy.utils.unregister_class(cls)
        except RuntimeError:
            pass


if __name__ == "__main__":
    register()
