#!/usr/bin/env bash
sens=0.5
xinput --set-prop "Kingsis Peripherals ZOWIE Gaming mouse" 'libinput Accel Profile Enabled' 0, 1 # turn off accel
xinput set-prop "Kingsis Peripherals ZOWIE Gaming mouse"  "Coordinate Transformation Matrix" $sens 0 0 0 $sens 0 0  0 1 # set sens
