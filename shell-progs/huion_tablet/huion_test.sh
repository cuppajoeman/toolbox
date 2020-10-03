#!/usr/bin/env bash
# XOURNALPP bindings
PAD_ID=$(xsetwacom --list | grep 'Pad pad' | sed 's/[^0-9]*//g')
PEN_ID=$(xsetwacom --list | grep 'Pen' | sed 's/[^0-9]*//g')
# PAD
# Paste
xsetwacom set $PAD_ID button 1 'key +Ctrl +z -z '
# Copy
