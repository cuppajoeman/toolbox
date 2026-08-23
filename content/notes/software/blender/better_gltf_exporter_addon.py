bl_info = {
    "name": "Better glTF Exporter",
    "version": (1, 0, 0),
    "blender": (4, 0, 0),
    "location": "File > Export > Better glTF (.gltf)",
    "description": "Exports glTF separate files with textures placed in a textures directory",
    "category": "Import-Export",
}

import os

import bpy
from bpy.props import BoolProperty, StringProperty
from bpy_extras.io_utils import ExportHelper


def _gltf_export_property_names():
    try:
        return set(bpy.ops.export_scene.gltf.get_rna_type().properties.keys())
    except Exception:
        return set()


def _set_if_supported(kwargs, supported, name, value):
    if name in supported:
        kwargs[name] = value


class EXPORT_SCENE_OT_better_gltf(bpy.types.Operator, ExportHelper):
    """Export glTF with a cleaner external file layout"""

    bl_idname = "export_scene.better_gltf"
    bl_label = "Better glTF"
    bl_options = {"PRESET"}

    filename_ext = ".gltf"

    filter_glob: StringProperty(default="*.gltf", options={"HIDDEN"}, maxlen=255)

    export_selected: BoolProperty(name="Selected Objects Only", default=False)
    apply_modifiers: BoolProperty(name="Apply Modifiers", default=True)
    export_lights: BoolProperty(name="Punctual Lights", default=True)

    texture_dir: StringProperty(
        name="Texture Directory",
        description="Directory for external textures, relative to the .gltf file",
        default="textures",
    )

    def execute(self, context):
        filepath = self.filepath
        if not filepath.lower().endswith(".gltf"):
            filepath += ".gltf"

        output_dir = os.path.dirname(filepath)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        texture_dir = self.texture_dir.strip().replace("\\", "/") or "textures"
        supported = _gltf_export_property_names()

        kwargs = {
            "filepath": filepath,
            "export_format": "GLTF_SEPARATE",
        }

        _set_if_supported(kwargs, supported, "export_texture_dir", texture_dir)
        _set_if_supported(kwargs, supported, "export_apply", self.apply_modifiers)
        _set_if_supported(kwargs, supported, "export_lights", self.export_lights)
        _set_if_supported(kwargs, supported, "export_selected", self.export_selected)
        _set_if_supported(kwargs, supported, "use_selection", self.export_selected)
        _set_if_supported(kwargs, supported, "export_texcoords", True)
        _set_if_supported(kwargs, supported, "export_normals", True)
        _set_if_supported(kwargs, supported, "export_yup", True)

        result = bpy.ops.export_scene.gltf(**kwargs)
        if "FINISHED" not in result:
            self.report({"ERROR"}, "Better glTF export failed")
            return {"CANCELLED"}

        self.report({"INFO"}, f"Exported glTF with textures in {texture_dir}/")
        return {"FINISHED"}


def menu_func_export(self, context):
    self.layout.operator(EXPORT_SCENE_OT_better_gltf.bl_idname, text="Better glTF (.gltf)")


classes = (EXPORT_SCENE_OT_better_gltf,)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)


def unregister():
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
