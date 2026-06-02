#!/usr/bin/env bash
# https://wayland.freedesktop.org/libinput/doc/latest/pointer-acceleration.html#the-flat-pointer-acceleration-profile
xinput --list
read -p "Which of the above devices would you like to disable mouse sensivity on? (give the id number)" id
echo    # (optional) move to a new line
xinput --set-prop $id 'libinput Accel Profile Enabled' 0, 1
