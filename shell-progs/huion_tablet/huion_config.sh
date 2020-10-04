#!/usr/bin/env bash

PEN_ID=$(xsetwacom --list | grep 'stylus' | sed 's/[^0-9]*//g')
# Bind the stylus to the main screen (if using multiple monitors)
# xsetwacom set $PEN_ID MapToOutput "HEAD-$1"
