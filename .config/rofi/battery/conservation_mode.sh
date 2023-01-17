#!/bin/bash
# Change Conservation Mode - Only accepts certain inputs
if [ "$1" = "on" ]
    then echo 1| sudo -A /usr/bin/tee /sys/bus/platform/drivers/ideapad_acpi/VPC2004:00/conservation_mode
elif [ "$1" = "off" ]
    then echo 0| sudo -A /usr/bin/tee /sys/bus/platform/drivers/ideapad_acpi/VPC2004:00/conservation_mode
fi
