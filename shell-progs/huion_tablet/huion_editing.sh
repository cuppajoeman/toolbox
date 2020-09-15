#!/usr/bin/env bash
# XOURNALPP bindings
PAD_ID=$(xsetwacom --list | grep 'Pad pad' | sed 's/[^0-9]*//g')
PEN_ID=$(xsetwacom --list | grep 'Pen' | sed 's/[^0-9]*//g')
# PAD
# Paste
xsetwacom set $PAD_ID button 1 key Ctrl V
# Copy
xsetwacom set $PAD_ID button 2 key Ctrl C
# Vertical space
xsetwacom set $PAD_ID button 3 key Ctrl Shift V
# New Page
xsetwacom set $PAD_ID button 8 key Ctrl D
# Zoom in
xsetwacom set $PAD_ID button 9 key Ctrl Shift +
# Zoom out
xsetwacom set $PAD_ID button 10 key Ctrl -

# Line
xsetwacom set $PAD_ID button 11 key Ctrl 6
# Hand
xsetwacom set $PAD_ID button 12 key Shift Ctrl A
# New eraser
xsetwacom set $PAD_ID button 13 key Shift Ctrl E
# Switch to Pen
xsetwacom set $PAD_ID button 14 key Shift Ctrl P

# PEN
# Undo
xsetwacom set $PEN_ID button 2 key Ctrl Z
# Selection
xsetwacom set $PEN_ID button 3 key Shift Ctrl R
