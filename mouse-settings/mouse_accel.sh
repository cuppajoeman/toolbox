#!/usr/bin/env bash
xinput --list
read -p "Which of the above devices would you like to disable mouse sensivity on? (give the id number)" id
echo    # (optional) move to a new line
xinput --set-prop $id 'libinput Accel Profile Enabled' 0, 1
