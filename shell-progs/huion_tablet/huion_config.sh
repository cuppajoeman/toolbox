#!/usr/bin/env bash

PEN_ID=$(xsetwacom --list | grep 'Pen' | sed 's/[^0-9]*//g')
# Bind the stylus to the main screen
xsetwacom set $PEN_ID MapToOutput "HEAD-$1"
