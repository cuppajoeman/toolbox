#!/bin/bash
xrandr --newmode $(cvt 1920 1080 60 | grep Mode | sed -e 's/.*"/1920x1080/')
xrandr --addmode VGA1 1920x1080
xrandr --output VGA1 --mode 1920x1080
