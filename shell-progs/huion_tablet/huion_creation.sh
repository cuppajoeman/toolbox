#!/usr/bin/env bash

# Bind the stylus to the main screen
xsetwacom set 14 MapToOutput HEAD-0

# XOURNALPP bindings
# PAD
# Ellipse
xsetwacom set 17 button 1 key Ctrl 3
# Rectangle
xsetwacom set 17 button 2 key Ctrl 2
# Line
xsetwacom set 17 button 3 key Ctrl 6
# Highlight
xsetwacom set 17 button 8 key Shift Ctrl H
# Zoom in
xsetwacom set 17 button 9 key Ctrl Shift +
# Zoom out
xsetwacom set 17 button 10 key Ctrl -
# New Page
xsetwacom set 17 button 11 key Ctrl D
# Add vertical space
xsetwacom set 17 button 12 key Shift Ctrl V
# Switch to Eraser
xsetwacom set 17 button 13 key Shift Ctrl E
# Switch to Pen
xsetwacom set 17 button 14 key Shift Ctrl P
# PEN
# Undo
xsetwacom set 14 button 2 key Ctrl Z
# Selection
xsetwacom set 14 button 3 key Shift Ctrl R
