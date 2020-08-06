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

# Make sure the accel is off, then we lower mouse sens (only applies to zowie mouse)
# xinput set-prop 8 "Coordinate Transformation Matrix" .5 0 0 0 .5 0 0 0 1

# === Graphical ===
# Set the screensaver
~/.fehbg &
# Screenshots
flameshot &
# Turn on compositor
picom -b
# Notifications
dunst &

# === Utilities ===
# File Sync
nextcloud &
# Optimus manager
optimus-manager-qt &
# Redshift
redshift-gtk &
# Clipboard
copyq &

# === Settings ===
# Swap caps and escape
setxkbmap -option caps:swapescape

exec i3
