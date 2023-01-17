#!/usr/bin/env bash

dir="$HOME/.config/rofi/battery"
rofi_command="rofi -theme $dir/battery.rasi"

cur_profile=$(powerprofilesctl get)
con_mode=$(cat /sys/bus/platform/drivers/ideapad_acpi/VPC2004:00/conservation_mode)
con_mode_readable=""

if [ "$con_mode" == "1" ]
    then con_mode_readable="ON"
elif [ "$con_mode" == "0" ]
    then con_mode_readable="OFF"
fi

# Options
performance=""
balanced=""
powersaver=""
conservative=""

# Variable passed to rofi
options="$powersaver\n$balanced\n$performance\n$conservative"

chosen="$(echo -e "$options" | $rofi_command -p "Current Profile: $cur_profile | Conservation Mode: $con_mode_readable" -dmenu -selected-row 2)"
case  $chosen in
    $performance)
        powerprofilesctl set performance
        ;;
    $balanced)
        powerprofilesctl set balanced
        ;;
    $powersaver)
        powerprofilesctl set power-saver
        ;;
    $conservative)
        if [ "$con_mode" == "1" ]
            then echo 0| sudo -A /usr/bin/tee /sys/bus/platform/drivers/ideapad_acpi/VPC2004:00/conservation_mode
        elif [ "$con_mode" == "0" ]
            then echo 1| sudo -A /usr/bin/tee /sys/bus/platform/drivers/ideapad_acpi/VPC2004:00/conservation_mode
        fi
        ;;
esac