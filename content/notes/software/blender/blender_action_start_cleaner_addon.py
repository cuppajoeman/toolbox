bl_info = {
    "name": "Action Start Cleaner",
    "version": (1, 0, 0),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > Animation > Action Start Cleaner",
    "description": "Shift Actions so their first keyframe starts at the chosen frame.",
    "category": "Animation",
}

import bpy
from bpy.props import BoolProperty, EnumProperty, FloatProperty, PointerProperty


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


def active_action_for_armature(armature):
    if not armature or armature.type != "ARMATURE":
        return None
    if not armature.animation_data:
        return None
    return armature.animation_data.action


def action_first_keyframe(action):
    first = None
    for fcurve in iter_action_fcurves(action):
        for point in fcurve.keyframe_points:
            frame = float(point.co.x)
            if first is None or frame < first:
                first = frame
    return first


def shift_fcurve_frames(fcurve, delta):
    for point in fcurve.keyframe_points:
        point.co.x += delta
        point.handle_left.x += delta
        point.handle_right.x += delta
    fcurve.update()


def shift_action_to_start(action, target_start):
    first = action_first_keyframe(action)
    if first is None:
        return None, 0.0
    delta = float(target_start) - first
    if abs(delta) < 0.000001:
        return first, 0.0
    for fcurve in iter_action_fcurves(action):
        shift_fcurve_frames(fcurve, delta)
    return first, delta


class ACTIONSTARTCLEANER_Settings(bpy.types.PropertyGroup):
    armature: PointerProperty(
        name="Armature",
        description="Armature whose active Action should be shifted when Scope is Active Action",
        type=bpy.types.Object,
        poll=lambda self, obj: obj.type == "ARMATURE",
    )

    scope: EnumProperty(
        name="Scope",
        description="Choose whether to shift the active Action or all Actions",
        items=(
            ("ACTIVE", "Active Action", "Shift only the Action currently assigned to the chosen armature"),
            ("ALL", "All Actions", "Shift every Action in the file"),
        ),
        default="ALL",
    )

    start_mode: EnumProperty(
        name="Start",
        description="Target start frame",
        items=(
            ("FRAME_1", "Frame 1", "Move first keyframe to frame 1"),
            ("SCENE_START", "Scene Start", "Move first keyframe to the scene start frame"),
            ("CUSTOM", "Custom", "Move first keyframe to a custom frame"),
        ),
        default="FRAME_1",
    )

    custom_start_frame: FloatProperty(
        name="Custom Frame",
        description="Custom target frame used when Start is Custom",
        default=1.0,
    )

    dry_run: BoolProperty(
        name="Dry Run",
        description="Only report what would be shifted",
        default=True,
    )

    print_details: BoolProperty(
        name="Print Details",
        description="Print old first keyframe and shift amount to the console",
        default=True,
    )


class ACTIONSTARTCLEANER_OT_clean(bpy.types.Operator):
    bl_idname = "object.action_start_cleaner_clean"
    bl_label = "Move First Keyframe To Start"
    bl_description = "Shift selected Actions so their first keyframe starts at the chosen frame"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        settings = context.scene.action_start_cleaner
        armature = settings.armature or context.object

        if settings.start_mode == "SCENE_START":
            target_start = float(context.scene.frame_start)
        elif settings.start_mode == "CUSTOM":
            target_start = settings.custom_start_frame
        else:
            target_start = 1.0

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

        shifted = 0
        unchanged = 0
        empty = 0

        for action in actions:
            first = action_first_keyframe(action)
            if first is None:
                empty += 1
                if settings.print_details:
                    print(f"Action Start Cleaner: empty Action {action.name!r}")
                continue

            delta = target_start - first
            if abs(delta) < 0.000001:
                unchanged += 1
                if settings.print_details:
                    print(f"Action Start Cleaner: unchanged {action.name!r}, first={first:g}")
                continue

            shifted += 1
            if settings.print_details:
                verb = "Would shift" if settings.dry_run else "Shifting"
                print(
                    f"Action Start Cleaner: {verb} {action.name!r}, "
                    f"first={first:g}, target={target_start:g}, delta={delta:g}"
                )

            if not settings.dry_run:
                shift_action_to_start(action, target_start)

        verb = "Would shift" if settings.dry_run else "Shifted"
        self.report({"INFO"}, f"{verb} {shifted} Action(s). Unchanged {unchanged}. Empty {empty}.")
        return {"FINISHED"}


class ACTIONSTARTCLEANER_PT_panel(bpy.types.Panel):
    bl_label = "Action Start Cleaner"
    bl_idname = "ACTIONSTARTCLEANER_PT_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Animation"

    def draw(self, context):
        layout = self.layout
        settings = context.scene.action_start_cleaner

        layout.prop(settings, "scope")
        if settings.scope == "ACTIVE":
            layout.prop(settings, "armature")
        layout.prop(settings, "start_mode")
        if settings.start_mode == "CUSTOM":
            layout.prop(settings, "custom_start_frame")
        layout.prop(settings, "dry_run")
        layout.prop(settings, "print_details")
        layout.operator(ACTIONSTARTCLEANER_OT_clean.bl_idname)


classes = (
    ACTIONSTARTCLEANER_Settings,
    ACTIONSTARTCLEANER_OT_clean,
    ACTIONSTARTCLEANER_PT_panel,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.action_start_cleaner = PointerProperty(type=ACTIONSTARTCLEANER_Settings)


def unregister():
    if hasattr(bpy.types.Scene, "action_start_cleaner"):
        del bpy.types.Scene.action_start_cleaner
    for cls in reversed(classes):
        try:
            bpy.utils.unregister_class(cls)
        except RuntimeError:
            pass


if __name__ == "__main__":
    register()
