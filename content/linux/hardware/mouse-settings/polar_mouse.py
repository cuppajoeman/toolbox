import struct
import math
import pyautogui
pyautogui.FAILSAFE = False

screen_width, screen_height = pyautogui.size()

aim_angle = 0

rotation_sensitivity = 0.005
y_axis_controls_length = True
aim_length_scale = 1
length_sensitivity = 0.0009

aim_length_x = screen_width / 2
aim_length_y = screen_height / 2
origin = (screen_width / 2, screen_height / 2)

max_distance = math.sqrt(aim_length_x ** 2 + aim_length_y ** 2)

def clamp(input, min, max):
    if (input < min):
        return min
    elif (input > max):
        return max
    return input

def translate(origin, point):
    print(origin, point)
    return tuple(map(sum,zip(origin, point)))

def polar_mouse_movement(delta_x, delta_y):
    global aim_length_scale
    global aim_angle

    if y_axis_controls_length:
        aim_length_scale = clamp(aim_length_scale + delta_y * length_sensitivity, 0, 1)

    aim_angle += delta_x * rotation_sensitivity

    x_pos = aim_length_scale * aim_length_x * math.cos(aim_angle)
    y_pos = aim_length_scale * aim_length_y * math.sin(aim_angle)

    # return clamp(x_pos + origin[0], -screen_width/2, screen_width/2), clamp(y_pos + origin[1], -screen_height/2, screen_height/2)
    return x_pos + origin[0], y_pos + origin[1]

def update_mouse_position(x_pos, y_pos):
    pyautogui.moveTo(x_pos, y_pos)

file = open( "/dev/input/mice", "rb" )

def getMouseEvent():
    buf = file.read(3)
    button = buf[0]
    left_pressed = button & 0x1
    middle_pressed = (button & 0x4) > 0
    right_pressed = (button & 0x2) > 0
    delta_x, delta_y = struct.unpack("bb", buf[1:])
    print ("L:%d, M: %d, R: %d, delta_x: %d, delta_x: %d\n" % (left_pressed, middle_pressed, right_pressed, delta_x, delta_y))
    return left_pressed, middle_pressed, right_pressed, delta_x, delta_y

while True:
    left_pressed, middle_pressed, right_pressed, delta_x, delta_y = getMouseEvent()
    x_pos, y_pos = polar_mouse_movement(delta_x, delta_y)
    if left_pressed:
        pyautogui.click()
    update_mouse_position(x_pos, y_pos)

file.close()

