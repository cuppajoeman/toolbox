bl_info = {
    "name": "Better First Person Viewport",
    "version": (1, 7, 0),
    "blender": (4, 0, 0),
    "location": "3D Viewport > Sidebar > View > Better First Person",
    "description": "Smooth FPS-style free-fly viewport navigation using ESDF and mouse look",
    "category": "3D View",
}

import bpy
import math
import time
import gpu

from mathutils import Vector, Matrix
from bpy.props import FloatProperty
from gpu_extras.batch import batch_for_shader


addon_keymaps = []


# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------

FPS_FOV_DEGREES = 90.0
VIEWPORT_SENSOR_WIDTH = 32.0

UPDATE_HZ = 144.0
UPDATE_INTERVAL = 1.0 / UPDATE_HZ

PITCH_MIN = math.radians(-90.0)
PITCH_MAX = math.radians(90.0)


# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------

def clamp(value, low, high):
    return max(low, min(high, value))


def fov_to_lens(fov_degrees):
    fov_radians = math.radians(fov_degrees)

    return (
        VIEWPORT_SENSOR_WIDTH
        / (
            2.0
            * math.tan(fov_radians * 0.5)
        )
    )


def rotation_from_yaw_pitch(yaw, pitch):
    cp = math.cos(pitch)

    forward = Vector((
        cp * math.cos(yaw),
        cp * math.sin(yaw),
        math.sin(pitch),
    ))

    if forward.length_squared > 0.0:
        forward.normalize()

    right = Vector((
        math.sin(yaw),
        -math.cos(yaw),
        0.0,
    ))

    if right.length_squared > 0.0:
        right.normalize()

    up = right.cross(forward)

    if up.length_squared > 0.0:
        up.normalize()

    back = -forward

    return Matrix((
        right,
        up,
        back,
    )).transposed().to_quaternion()


# -----------------------------------------------------------------------------
# Navigation operator
# -----------------------------------------------------------------------------

class BETTERFPS_OT_navigate(bpy.types.Operator):
    bl_idname = "view3d.better_first_person_navigate"
    bl_label = "Better First Person Navigation"
    bl_description = "Smooth FPS-style free-fly viewport navigation"

    bl_options = {
        'BLOCKING',
        'GRAB_CURSOR',
    }

    _timer = None
    _draw_handle = None

    _running = False
    _stop_requested = False

    @classmethod
    def poll(cls, context):
        return (
            context.area is not None
            and context.area.type == 'VIEW_3D'
            and context.region is not None
            and context.region.type == 'WINDOW'
            and context.region_data is not None
        )

    # -------------------------------------------------------------------------
    # Crosshair
    # -------------------------------------------------------------------------

    def draw_crosshair(self):
        if not type(self)._running:
            return

        if bpy.context.area != self.area:
            return

        region = bpy.context.region

        if region is None:
            return

        cx = region.width * 0.5
        cy = region.height * 0.5

        radius = 6.0
        segments = 40

        vertices = []

        for i in range(segments):
            angle = (
                math.tau
                * i
                / segments
            )

            vertices.append((
                cx + math.cos(angle) * radius,
                cy + math.sin(angle) * radius,
            ))

        shader = gpu.shader.from_builtin(
            'UNIFORM_COLOR'
        )

        batch = batch_for_shader(
            shader,
            'LINE_LOOP',
            {
                "pos": vertices,
            },
        )

        gpu.state.blend_set('ALPHA')
        gpu.state.line_width_set(2.0)

        shader.bind()

        shader.uniform_float(
            "color",
            (
                1.0,
                1.0,
                1.0,
                1.0,
            ),
        )

        batch.draw(shader)

        gpu.state.line_width_set(1.0)
        gpu.state.blend_set('NONE')

    def add_crosshair(self):
        if self._draw_handle is not None:
            return

        self._draw_handle = (
            bpy.types.SpaceView3D.draw_handler_add(
                self.draw_crosshair,
                (),
                'WINDOW',
                'POST_PIXEL',
            )
        )

    def remove_crosshair(self):
        if self._draw_handle is None:
            return

        try:
            bpy.types.SpaceView3D.draw_handler_remove(
                self._draw_handle,
                'WINDOW',
            )
        except Exception:
            pass

        self._draw_handle = None

    # -------------------------------------------------------------------------
    # Mouse
    # -------------------------------------------------------------------------

    def update_mouse_center(self):
        self.center_x = (
            self.region.x
            + self.region.width // 2
        )

        self.center_y = (
            self.region.y
            + self.region.height // 2
        )

    def warp_to_center(self, context):
        self.update_mouse_center()

        self.ignore_warp_event = True

        context.window.cursor_warp(
            self.center_x,
            self.center_y,
        )

    def accumulate_mouse(self, event):
        if self.ignore_warp_event:
            self.ignore_warp_event = False
            return

        dx = event.mouse_x - self.center_x
        dy = event.mouse_y - self.center_y

        if dx == 0 and dy == 0:
            return

        self.mouse_dx += dx
        self.mouse_dy += dy

        self.mouse_needs_recenter = True

    # -------------------------------------------------------------------------
    # View
    # -------------------------------------------------------------------------

    def apply_view(self):
        rotation = rotation_from_yaw_pitch(
            self.yaw,
            self.pitch,
        )

        forward = (
            rotation
            @ Vector((0.0, 0.0, -1.0))
        )

        self.rv3d.view_rotation = rotation
        self.rv3d.view_distance = self.view_distance

        self.rv3d.view_location = (
            self.position
            + forward * self.view_distance
        )

        self.rv3d.view_perspective = 'PERSP'

        if self.area:
            self.area.tag_redraw()

    # -------------------------------------------------------------------------
    # Unified camera update
    # -------------------------------------------------------------------------

    def update_camera(self, context):
        now = time.perf_counter()

        dt = now - self.last_time
        self.last_time = now

        # Protect against giant jumps after stalls.
        dt = min(dt, 0.05)

        props = (
            context.scene
            .better_first_person_settings
        )

        camera_changed = False

        # ---------------------------------------------------------------------
        # Apply accumulated mouse movement
        # ---------------------------------------------------------------------

        if (
            self.mouse_dx != 0.0
            or self.mouse_dy != 0.0
        ):
            self.yaw -= (
                self.mouse_dx
                * props.mouse_sensitivity
            )

            self.pitch += (
                self.mouse_dy
                * props.mouse_sensitivity
            )

            self.pitch = clamp(
                self.pitch,
                PITCH_MIN,
                PITCH_MAX,
            )

            self.mouse_dx = 0.0
            self.mouse_dy = 0.0

            camera_changed = True

        # ---------------------------------------------------------------------
        # Calculate basis AFTER rotation update
        # ---------------------------------------------------------------------

        rotation = rotation_from_yaw_pitch(
            self.yaw,
            self.pitch,
        )

        forward = (
            rotation
            @ Vector((0.0, 0.0, -1.0))
        )

        right = (
            rotation
            @ Vector((1.0, 0.0, 0.0))
        )

        world_up = Vector((
            0.0,
            0.0,
            1.0,
        ))

        move = Vector((
            0.0,
            0.0,
            0.0,
        ))

        # ---------------------------------------------------------------------
        # ESDF
        # ---------------------------------------------------------------------

        if 'E' in self.keys:
            move += forward

        if 'D' in self.keys:
            move -= forward

        if 'S' in self.keys:
            move -= right

        if 'F' in self.keys:
            move += right

        # ---------------------------------------------------------------------
        # Vertical
        #
        # Space = up
        # Shift = down
        # ---------------------------------------------------------------------

        if 'SPACE' in self.keys:
            move += world_up

        shift_held = (
            'LEFT_SHIFT' in self.keys
            or
            'RIGHT_SHIFT' in self.keys
        )

        if shift_held:
            move -= world_up

        # ---------------------------------------------------------------------
        # Speed
        #
        # Tab = fast
        # Ctrl = slow
        # ---------------------------------------------------------------------

        if move.length_squared > 0.0:
            move.normalize()

            speed = props.move_speed

            tab_held = (
                'TAB' in self.keys
            )

            ctrl_held = (
                'LEFT_CTRL' in self.keys
                or
                'RIGHT_CTRL' in self.keys
            )

            if tab_held:
                speed *= props.boost_multiplier

            if ctrl_held:
                speed *= props.slow_multiplier

            self.position += (
                move
                * speed
                * dt
            )

            camera_changed = True

        # ---------------------------------------------------------------------
        # Apply complete transform once
        # ---------------------------------------------------------------------

        if camera_changed:
            self.apply_view()

        # ---------------------------------------------------------------------
        # Recenter cursor only after consuming accumulated motion
        # ---------------------------------------------------------------------

        if self.mouse_needs_recenter:
            self.mouse_needs_recenter = False

            self.warp_to_center(
                context
            )

    # -------------------------------------------------------------------------
    # Cleanup
    # -------------------------------------------------------------------------

    def finish(self, context):
        self.remove_crosshair()

        if self._timer is not None:
            try:
                context.window_manager.event_timer_remove(
                    self._timer
                )
            except Exception:
                pass

            self._timer = None

        type(self)._running = False
        type(self)._stop_requested = False

        self.keys.clear()

        try:
            context.window.cursor_modal_restore()
        except Exception:
            pass

        if self.area:
            self.area.tag_redraw()

    def cancel(self, context):
        self.finish(context)

    # -------------------------------------------------------------------------
    # Start
    # -------------------------------------------------------------------------

    def invoke(self, context, event):
        self.keys = set()

        self.area = None
        self.region = None
        self.rv3d = None
        self.space = None

        self.position = Vector((
            0.0,
            0.0,
            0.0,
        ))

        self.yaw = 0.0
        self.pitch = 0.0

        self.view_distance = 0.01

        self.last_time = 0.0

        # Accumulated mouse state.
        self.mouse_dx = 0.0
        self.mouse_dy = 0.0

        self.center_x = 0
        self.center_y = 0

        self.ignore_warp_event = False
        self.mouse_needs_recenter = False

        self._draw_handle = None

        if type(self)._running:
            return {'CANCELLED'}

        self.area = context.area
        self.region = context.region
        self.rv3d = context.region_data
        self.space = context.space_data

        # ---------------------------------------------------------------------
        # 90° FOV
        # ---------------------------------------------------------------------

        self.space.lens = fov_to_lens(
            FPS_FOV_DEGREES
        )

        # ---------------------------------------------------------------------
        # Recover existing view
        # ---------------------------------------------------------------------

        initial_rotation = (
            self.rv3d.view_rotation.copy()
        )

        self.view_distance = max(
            float(self.rv3d.view_distance),
            0.01,
        )

        self.position = (
            self.rv3d.view_location
            + initial_rotation
            @ Vector((
                0.0,
                0.0,
                self.view_distance,
            ))
        )

        forward = (
            initial_rotation
            @ Vector((
                0.0,
                0.0,
                -1.0,
            ))
        )

        if forward.length_squared == 0.0:
            forward = Vector((
                1.0,
                0.0,
                0.0,
            ))
        else:
            forward.normalize()

        self.yaw = math.atan2(
            forward.y,
            forward.x,
        )

        self.pitch = math.asin(
            clamp(
                forward.z,
                -1.0,
                1.0,
            )
        )

        self.pitch = clamp(
            self.pitch,
            PITCH_MIN,
            PITCH_MAX,
        )

        self.last_time = (
            time.perf_counter()
        )

        # ---------------------------------------------------------------------
        # Timer
        # ---------------------------------------------------------------------

        self._timer = (
            context.window_manager.event_timer_add(
                UPDATE_INTERVAL,
                window=context.window,
            )
        )

        context.window_manager.modal_handler_add(
            self
        )

        type(self)._running = True
        type(self)._stop_requested = False

        # Hide cursor.
        context.window.cursor_modal_set(
            'NONE'
        )

        self.add_crosshair()

        self.apply_view()

        self.warp_to_center(
            context
        )

        return {'RUNNING_MODAL'}

    # -------------------------------------------------------------------------
    # Key state
    # -------------------------------------------------------------------------

    def handle_key(self, event):
        tracked = {
            'E',
            'S',
            'D',
            'F',

            'SPACE',

            'TAB',

            'LEFT_SHIFT',
            'RIGHT_SHIFT',

            'LEFT_CTRL',
            'RIGHT_CTRL',
        }

        if event.type not in tracked:
            return False

        if event.value == 'PRESS':
            self.keys.add(
                event.type
            )

        elif event.value == 'RELEASE':
            self.keys.discard(
                event.type
            )

        return True

    # -------------------------------------------------------------------------
    # Modal loop
    # -------------------------------------------------------------------------

    def modal(self, context, event):
        # Stop request.
        if type(self)._stop_requested:
            self.finish(context)

            return {'FINISHED'}

        # Invalid viewport.
        if (
            self.area is None
            or self.area.type != 'VIEW_3D'
        ):
            self.finish(context)

            return {'CANCELLED'}

        # Middle mouse toggles off.
        if (
            event.type == 'MIDDLEMOUSE'
            and event.value == 'PRESS'
        ):
            self.finish(context)

            return {'FINISHED'}

        # Escape exits.
        if (
            event.type == 'ESC'
            and event.value == 'PRESS'
        ):
            self.finish(context)

            return {'FINISHED'}

        # Lost focus.
        if event.type == 'WINDOW_DEACTIVATE':
            self.keys.clear()

            self.mouse_dx = 0.0
            self.mouse_dy = 0.0

            return {'RUNNING_MODAL'}

        # ---------------------------------------------------------------------
        # Navigation-owned key state
        # ---------------------------------------------------------------------

        if self.handle_key(event):
            return {'RUNNING_MODAL'}

        # ---------------------------------------------------------------------
        # Mouse events ONLY collect delta.
        #
        # Do not rotate/apply the view here.
        # ---------------------------------------------------------------------

        if event.type in {
            'MOUSEMOVE',
            'INBETWEEN_MOUSEMOVE',
        }:
            self.accumulate_mouse(
                event
            )

            return {'RUNNING_MODAL'}

        # ---------------------------------------------------------------------
        # Single unified update path
        # ---------------------------------------------------------------------

        if event.type == 'TIMER':
            self.update_camera(
                context
            )

            return {'RUNNING_MODAL'}

        # Everything else gets handed back to Blender.
        return {'PASS_THROUGH'}


# -----------------------------------------------------------------------------
# Toggle operator
# -----------------------------------------------------------------------------

class BETTERFPS_OT_toggle(bpy.types.Operator):
    bl_idname = "view3d.better_first_person_toggle"
    bl_label = "Toggle Better First Person Viewport"
    bl_description = "Enable or disable first-person viewport navigation"

    def execute(self, context):
        if BETTERFPS_OT_navigate._running:
            BETTERFPS_OT_navigate._stop_requested = True

            return {'FINISHED'}

        bpy.ops.view3d.better_first_person_navigate(
            'INVOKE_DEFAULT'
        )

        return {'FINISHED'}


# -----------------------------------------------------------------------------
# Settings
# -----------------------------------------------------------------------------

class BetterFirstPersonSettings(bpy.types.PropertyGroup):
    move_speed: FloatProperty(
        name="Move Speed",
        description="Normal movement speed",
        default=8.0,
        min=0.01,
        soft_max=100.0,
    )

    mouse_sensitivity: FloatProperty(
        name="Mouse Sensitivity",
        description="Mouse look sensitivity",
        default=0.0025,
        min=0.0001,
        max=0.02,
        precision=4,
    )

    boost_multiplier: FloatProperty(
        name="Tab Fast",
        description="Speed multiplier while Tab is held",
        default=4.0,
        min=1.0,
        soft_max=20.0,
    )

    slow_multiplier: FloatProperty(
        name="Ctrl Slow",
        description="Speed multiplier while Ctrl is held",
        default=0.25,
        min=0.01,
        max=1.0,
        precision=2,
    )


# -----------------------------------------------------------------------------
# Sidebar
# -----------------------------------------------------------------------------

class BETTERFPS_PT_panel(bpy.types.Panel):
    bl_label = "Better First Person"
    bl_idname = "BETTERFPS_PT_panel"

    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "View"

    def draw(self, context):
        layout = self.layout

        props = (
            context.scene
            .better_first_person_settings
        )

        running = (
            BETTERFPS_OT_navigate._running
        )

        col = layout.column(
            align=True
        )

        col.operator(
            "view3d.better_first_person_toggle",
            text=(
                "Disable Better First Person"
                if running
                else
                "Enable Better First Person"
            ),
            icon=(
                'PAUSE'
                if running
                else
                'PLAY'
            ),
        )

        col.separator()

        col.prop(
            props,
            "move_speed",
        )

        col.prop(
            props,
            "mouse_sensitivity",
        )

        col.prop(
            props,
            "boost_multiplier",
        )

        col.prop(
            props,
            "slow_multiplier",
        )

        box = layout.box()

        box.label(text="Controls")

        box.label(
            text="E / D: Forward / Back"
        )

        box.label(
            text="S / F: Left / Right"
        )

        box.label(
            text="Space: Up"
        )

        box.label(
            text="Shift: Down"
        )

        box.label(
            text="Tab: Fast"
        )

        box.label(
            text="Ctrl: Slow"
        )

        box.label(
            text="Middle Mouse: Toggle"
        )

        box.label(
            text="Mouse: Look"
        )

        box.label(
            text="Esc: Exit"
        )

        box.separator()

        box.label(
            text="FOV: 90°"
        )

        box.label(
            text=f"Update: {int(UPDATE_HZ)} Hz"
        )

        box.label(
            text="Pitch: -90° to +90°"
        )


# -----------------------------------------------------------------------------
# Registration
# -----------------------------------------------------------------------------

classes = (
    BetterFirstPersonSettings,
    BETTERFPS_OT_navigate,
    BETTERFPS_OT_toggle,
    BETTERFPS_PT_panel,
)


# -----------------------------------------------------------------------------
# Keymap helpers
# -----------------------------------------------------------------------------

def remove_existing_keymaps():
    wm = bpy.context.window_manager

    if wm is None:
        return

    kc = wm.keyconfigs.addon

    if kc is None:
        return

    km = kc.keymaps.get(
        '3D View'
    )

    if km is None:
        return

    for kmi in list(
        km.keymap_items
    ):
        if (
            kmi.idname
            == "view3d.better_first_person_toggle"
        ):
            try:
                km.keymap_items.remove(
                    kmi
                )
            except Exception:
                pass


def register_keymaps():
    global addon_keymaps

    wm = bpy.context.window_manager

    if wm is None:
        return

    kc = wm.keyconfigs.addon

    if kc is None:
        return

    remove_existing_keymaps()

    km = kc.keymaps.new(
        name='3D View',
        space_type='VIEW_3D',
    )

    kmi = km.keymap_items.new(
        BETTERFPS_OT_toggle.bl_idname,
        type='MIDDLEMOUSE',
        value='PRESS',
    )

    addon_keymaps.append(
        (
            km,
            kmi,
        )
    )


def unregister_keymaps():
    global addon_keymaps

    for km, kmi in addon_keymaps:
        try:
            km.keymap_items.remove(
                kmi
            )
        except Exception:
            pass

    addon_keymaps.clear()

    remove_existing_keymaps()


# -----------------------------------------------------------------------------
# Development hot reload
# -----------------------------------------------------------------------------

def unregister_existing():
    remove_existing_keymaps()

    if hasattr(
        bpy.types.Scene,
        "better_first_person_settings",
    ):
        try:
            del bpy.types.Scene.better_first_person_settings
        except Exception:
            pass

    names = (
        "BETTERFPS_PT_panel",
        "BETTERFPS_OT_toggle",
        "BETTERFPS_OT_navigate",
        "BetterFirstPersonSettings",
    )

    for name in names:
        old_class = getattr(
            bpy.types,
            name,
            None,
        )

        if old_class is not None:
            try:
                bpy.utils.unregister_class(
                    old_class
                )
            except Exception:
                pass


# -----------------------------------------------------------------------------
# Register / unregister
# -----------------------------------------------------------------------------

def register():
    for cls in classes:
        bpy.utils.register_class(
            cls
        )

    bpy.types.Scene.better_first_person_settings = (
        bpy.props.PointerProperty(
            type=BetterFirstPersonSettings
        )
    )

    register_keymaps()


def unregister():
    unregister_keymaps()

    if hasattr(
        bpy.types.Scene,
        "better_first_person_settings",
    ):
        del bpy.types.Scene.better_first_person_settings

    for cls in reversed(
        classes
    ):
        try:
            bpy.utils.unregister_class(
                cls
            )
        except Exception:
            pass


# -----------------------------------------------------------------------------
# Development entry point
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    unregister_existing()

    register()

    print("Better First Person Viewport registered.")
    print(f"Unified camera update: {UPDATE_HZ:.0f} Hz")
    print(
        "ESDF move | Space up | Shift down | "
        "Tab fast | Ctrl slow | Middle Mouse toggle"
    )

