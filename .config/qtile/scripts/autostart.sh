#!/bin/bash

export PATH="/home/romeless/.local/bin:$PATH"

picom -b &
eww daemon &
volctl &
nm-applet &
mkfifo /tmp/vol-icon && ~/.config/qtile/scripts/vol_icon.sh &

# Low battery notifier
~/.config/qtile/scripts/check_battery.sh & disown

# Start welcome
eos-welcome & disown

# start polkit agent from GNOME
/usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1 & disown
