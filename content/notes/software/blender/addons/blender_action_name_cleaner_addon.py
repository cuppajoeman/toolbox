bl_info = {
    "name": "Action Name Cleaner",
    "version": (1, 0, 0),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > Animation > Action Name Cleaner",
    "description": "Normalize Blender Action names by removing exporter noise and converting to snake_case.",
    "category": "Animation",
}

import re

import bpy
from bpy.props import BoolProperty, EnumProperty, PointerProperty


WRAPPER_WORDS = {
    "action",
    "animation",
    "base",
    "baseanimation",
    "layer",
    "layer0",
    "mixamo",
}


def active_action_for_armature(armature):
    if not armature or armature.type != "ARMATURE":
        return None
    if not armature.animation_data:
        return None
    return armature.animation_data.action


def split_export_segments(name):
    segments = []
    for part in re.split(r"[|:]", name):
        cleaned = part.strip()
        if cleaned:
            segments.append(cleaned)
    return segments or [name]


def strip_blender_numeric_suffix(name):
    return re.sub(r"\.\d{3,}$", "", name)


def looks_like_object_wrapper(segment):
    lowered = strip_blender_numeric_suffix(segment).lower()
    return lowered in {"armature", "skeleton", "rig", "root", "scene"}


def camel_to_words(text):
    text = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", text)
    text = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", text)
    text = re.sub(r"([A-Za-z])([0-9])", r"\1_\2", text)
    text = re.sub(r"([0-9])([A-Za-z])", r"\1_\2", text)
    return text


def to_snake_case(text):
    text = camel_to_words(text)
    text = re.sub(r"[^A-Za-z0-9]+", "_", text)
    text = re.sub(r"_+", "_", text)
    return text.strip("_").lower()


def remove_duplicate_adjacent_words(words):
    cleaned = []
    for word in words:
        if cleaned and cleaned[-1] == word:
            continue
        cleaned.append(word)
    return cleaned


def best_animation_segment(name):
    segments = split_export_segments(name)
    normalized_segments = []

    for segment in segments:
        if looks_like_object_wrapper(segment):
            continue
        snake = to_snake_case(segment)
        if not snake:
            continue
        words = [word for word in snake.split("_") if word and word not in WRAPPER_WORDS]
        words = remove_duplicate_adjacent_words(words)
        if words:
            normalized_segments.append("_".join(words))

    if not normalized_segments:
        return to_snake_case(name) or "action"

    # Exporters often produce strings like:
    # Armature.001|Walk|Walk:BaseAnimation
    # Prefer the longest meaningful repeated segment, then de-duplicate below.
    return max(normalized_segments, key=lambda value: (len(value.split("_")), len(value)))


def normalize_action_name(name):
    candidate = best_animation_segment(name)

    words = candidate.split("_")
    half = len(words) // 2
    if half > 0 and len(words) % 2 == 0 and words[:half] == words[half:]:
        words = words[:half]

    return "_".join(remove_duplicate_adjacent_words(words)) or "action"


def unique_action_name(base_name, current_action=None):
    existing = {
        action.name
        for action in bpy.data.actions
        if action != current_action
    }
    if base_name not in existing:
        return base_name

    index = 1
    while True:
        candidate = f"{base_name}_{index:02d}"
        if candidate not in existing:
            return candidate
        index += 1


def clean_action_name(action):
    new_name = unique_action_name(normalize_action_name(action.name), current_action=action)
    old_name = action.name
    action.name = new_name
    return old_name, new_name


class ACTIONNAMECLEANER_Settings(bpy.types.PropertyGroup):
    armature: PointerProperty(
        name="Armature",
        description="Armature whose active Action should be cleaned when Scope is Active Action",
        type=bpy.types.Object,
        poll=lambda self, obj: obj.type == "ARMATURE",
    )

    scope: EnumProperty(
        name="Scope",
        description="Choose whether to clean the active Action or all Actions",
        items=(
            ("ACTIVE", "Active Action", "Clean only the Action currently assigned to the chosen armature"),
            ("ALL", "All Actions", "Clean every Action in the file"),
        ),
        default="ALL",
    )

    print_mapping: BoolProperty(
        name="Print Mapping",
        description="Print old and new Action names to the console",
        default=True,
    )


class ACTIONNAMECLEANER_OT_clean(bpy.types.Operator):
    bl_idname = "object.action_name_cleaner_clean"
    bl_label = "Clean Action Names"
    bl_description = "Normalize Action names by removing exporter noise and converting to snake_case"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        settings = context.scene.action_name_cleaner
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

        changed = 0
        unchanged = 0
        for action in actions:
            old_name, new_name = clean_action_name(action)
            if old_name == new_name:
                unchanged += 1
            else:
                changed += 1
                if settings.print_mapping:
                    print(f"Action Name Cleaner: {old_name!r} -> {new_name!r}")

        self.report({"INFO"}, f"Renamed {changed} Action(s). Unchanged {unchanged}.")
        return {"FINISHED"}


class ACTIONNAMECLEANER_PT_panel(bpy.types.Panel):
    bl_label = "Action Name Cleaner"
    bl_idname = "ACTIONNAMECLEANER_PT_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Animation"

    def draw(self, context):
        layout = self.layout
        settings = context.scene.action_name_cleaner

        layout.prop(settings, "scope")
        if settings.scope == "ACTIVE":
            layout.prop(settings, "armature")
        layout.prop(settings, "print_mapping")
        layout.operator(ACTIONNAMECLEANER_OT_clean.bl_idname)


classes = (
    ACTIONNAMECLEANER_Settings,
    ACTIONNAMECLEANER_OT_clean,
    ACTIONNAMECLEANER_PT_panel,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.action_name_cleaner = PointerProperty(type=ACTIONNAMECLEANER_Settings)


def unregister():
    if hasattr(bpy.types.Scene, "action_name_cleaner"):
        del bpy.types.Scene.action_name_cleaner
    for cls in reversed(classes):
        try:
            bpy.utils.unregister_class(cls)
        except RuntimeError:
            pass


if __name__ == "__main__":
    register()
