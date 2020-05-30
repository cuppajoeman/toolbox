#!/bin/sh
#
# ~/.xinitrc
#
# Executed by startx (run your window manager from here)

if [ -d /etc/X11/xinit/xinitrc.d ]; then
  for f in /etc/X11/xinit/xinitrc.d/*; do
    [ -x "$f" ] && . "$f"
  done
  unset f
fi

[[ -f ~/.Xresources ]] && xrdb -merge -I$HOME ~/.Xresources

# Make sure the accel is off, then we lower mouse sens
xinput set-prop 8 "Coordinate Transformation Matrix" .5 0 0 0 .5 0 0 0 1
# Set the screensaver
feh --bg-max --randomize ~/MEGA/backgrounds/* &
# Screenshots
flameshot &
# File Sync
megasync &
# Swap caps and escape
setxkbmap -option caps:swapescape
# Turn on compositor
picom &
# Notifications
dunst &
exec i3
