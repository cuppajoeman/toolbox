#!/usr/bin/env bash
xinput --set-prop "Logitech M570" 'libinput Accel Profile Enabled' 0, 1 # turn off accel
xinput set-prop "Logitech M570"  "Coordinate Transformation Matrix" 80 0 0 0 80 0 0  0 1 # set sens
