bl_info = {
    "name": "World Space UV",
    "version": (1, 1, 0),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > Tool > World Space UV",
    "description": "Project selected mesh UVs from world-space coordinates, with 1 meter = 1 UV unit by default.",
    "category": "UV",
}

import bpy
from bpy.props import BoolProperty, EnumProperty, FloatProperty, PointerProperty, StringProperty


def _project_world_position(world_position, world_normal, scale):
    normal = world_normal.normalized()
    ax = abs(normal.x)
    ay = abs(normal.y)
    az = abs(normal.z)

    if ax >= ay and ax >= az:
        u = world_position.y
        v = world_position.z
        if normal.x < 0.0:
            u = -u
    elif ay >= ax and ay >= az:
        u = world_position.x
        v = world_position.z
        if normal.y < 0.0:
            u = -u
    else:
        u = world_position.x
        v = world_position.y
        if normal.z < 0.0:
            u = -u

    return (u * scale, v * scale)


def _assign_world_space_uvs(obj, uv_map_name, scale, make_active, uv_target, selected_faces_only):
    mesh = obj.data
    if not mesh.polygons:
        return 0

    if uv_target == "ACTIVE" and mesh.uv_layers.active:
        uv_layer = mesh.uv_layers.active
    else:
        uv_layer = mesh.uv_layers.get(uv_map_name)
        if uv_layer is None:
            uv_layer = mesh.uv_layers.new(name=uv_map_name)

    if make_active:
        mesh.uv_layers.active = uv_layer

    normal_matrix = obj.matrix_world.to_3x3().inverted().transposed()
    loop_count = 0

    for polygon in mesh.polygons:
        if selected_faces_only and not polygon.select:
            continue

        world_normal = normal_matrix @ polygon.normal
        for loop_index in polygon.loop_indices:
            vertex_index = mesh.loops[loop_index].vertex_index
            world_position = obj.matrix_world @ mesh.vertices[vertex_index].co
            uv_layer.data[loop_index].uv = _project_world_position(world_position, world_normal, scale)
            loop_count += 1

    mesh.update()
    return loop_count


class WORLDSPACEUV_OT_project(bpy.types.Operator):
    bl_idname = "object.world_space_uv_project"
    bl_label = "Apply World Space UVs"
    bl_description = "Project selected mesh UVs from world-space coordinates"
    bl_options = {"REGISTER", "UNDO"}

    uv_map_name: StringProperty(
        name="UV Map",
        description="UV map to create or overwrite",
        default="WorldSpaceUV",
    )

    scale: FloatProperty(
        name="Scale",
        description="UV units per Blender meter. 1.0 means one meter equals one UV unit",
        default=1.0,
        min=0.0001,
        soft_min=0.01,
        soft_max=10.0,
    )

    make_active: BoolProperty(
        name="Make Active",
        description="Make the generated UV map the active UV map",
        default=True,
    )

    uv_target: EnumProperty(
        name="Write To",
        description="Choose whether to overwrite the active UV map or create/use a named UV map",
        items=[
            ("ACTIVE", "Active UV Map", "Overwrite the active UV map, creating one if the mesh has none"),
            ("NAMED", "Named UV Map", "Create or overwrite the named UV map"),
        ],
        default="ACTIVE",
    )

    selected_only: BoolProperty(
        name="Selected Objects Only",
        description="Apply to selected mesh objects instead of only the active object",
        default=True,
    )

    selected_faces_only: BoolProperty(
        name="Selected Faces Only",
        description="In Edit Mode, apply only to selected faces",
        default=False,
    )

    @classmethod
    def poll(cls, context):
        if context.mode not in {"OBJECT", "EDIT_MESH"}:
            return False
        return any(obj.type == "MESH" for obj in context.selected_objects)

    def execute(self, context):
        previous_mode = context.mode
        use_selected_faces = self.selected_faces_only and previous_mode == "EDIT_MESH"
        if previous_mode == "EDIT_MESH":
            bpy.ops.object.mode_set(mode="OBJECT")

        objects = context.selected_objects if self.selected_only else [context.active_object]
        mesh_objects = [obj for obj in objects if obj and obj.type == "MESH"]

        if not mesh_objects:
            self.report({"WARNING"}, "No mesh objects selected")
            return {"CANCELLED"}

        total_loops = 0
        for obj in mesh_objects:
            total_loops += _assign_world_space_uvs(
                obj,
                self.uv_map_name,
                self.scale,
                self.make_active,
                self.uv_target,
                use_selected_faces,
            )

        if previous_mode == "EDIT_MESH":
            bpy.ops.object.mode_set(mode="EDIT")

        self.report({"INFO"}, f"Assigned world-space UVs to {len(mesh_objects)} object(s), {total_loops} loops")
        return {"FINISHED"}


class WORLDSPACEUV_Settings(bpy.types.PropertyGroup):
    uv_map_name: StringProperty(
        name="UV Map",
        description="UV map to create or overwrite when Write To is set to Named UV Map",
        default="WorldSpaceUV",
    )

    scale: FloatProperty(
        name="Scale",
        description="UV units per Blender meter. Lower values make the texture larger; higher values tile it more",
        default=1.0,
        min=0.0001,
        soft_min=0.01,
        soft_max=10.0,
    )

    uv_target: EnumProperty(
        name="Write To",
        description="Choose whether to overwrite the active UV map or create/use a named UV map",
        items=[
            ("ACTIVE", "Active UV Map", "Overwrite the active UV map, creating one if the mesh has none"),
            ("NAMED", "Named UV Map", "Create or overwrite the named UV map"),
        ],
        default="ACTIVE",
    )

    make_active: BoolProperty(
        name="Make Active",
        description="Make the generated UV map the active UV map",
        default=True,
    )

    selected_only: BoolProperty(
        name="Selected Objects Only",
        description="Apply to selected mesh objects instead of only the active object",
        default=True,
    )

    selected_faces_only: BoolProperty(
        name="Selected Faces Only",
        description="In Edit Mode, apply only to selected faces",
        default=False,
    )


class WORLDSPACEUV_PT_panel(bpy.types.Panel):
    bl_label = "World Space UV"
    bl_idname = "WORLDSPACEUV_PT_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Tool"

    def draw(self, context):
        layout = self.layout
        settings = context.scene.world_space_uv_settings

        layout.label(text="1 meter = 1 UV unit at Scale 1.0")
        layout.prop(settings, "scale")
        layout.prop(settings, "uv_target")
        if settings.uv_target == "NAMED":
            layout.prop(settings, "uv_map_name")
        layout.prop(settings, "make_active")
        layout.prop(settings, "selected_only")
        layout.prop(settings, "selected_faces_only")

        op = layout.operator(WORLDSPACEUV_OT_project.bl_idname)
        op.scale = settings.scale
        op.uv_target = settings.uv_target
        op.uv_map_name = settings.uv_map_name
        op.make_active = settings.make_active
        op.selected_only = settings.selected_only
        op.selected_faces_only = settings.selected_faces_only


def menu_func(self, context):
    self.layout.operator(WORLDSPACEUV_OT_project.bl_idname)


classes = (
    WORLDSPACEUV_Settings,
    WORLDSPACEUV_OT_project,
    WORLDSPACEUV_PT_panel,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.world_space_uv_settings = PointerProperty(type=WORLDSPACEUV_Settings)
    bpy.types.VIEW3D_MT_object.append(menu_func)


def unregister():
    bpy.types.VIEW3D_MT_object.remove(menu_func)
    del bpy.types.Scene.world_space_uv_settings
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
