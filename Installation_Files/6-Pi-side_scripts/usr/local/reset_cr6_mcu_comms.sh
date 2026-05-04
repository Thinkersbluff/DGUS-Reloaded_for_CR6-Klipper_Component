#!/bin/bash
# reset_cr6_mcu_comms.sh
#
# Triggered by udev when the CR6 MCU USB device appears on the Pi.
# Waits for the stable /dev/serial/by-id symlink, then restarts Klipper.
#
# BEFORE INSTALLING: replace MCU_SERIAL_ID with the value from your system.
# Run this on the Pi to find it:
#   for d in /dev/ttyACM*; do [ -e "$d" ] || continue; echo "$d -> $(udevadm info -q property -n "$d" | sed -n 's/^ID_SERIAL=//p')"; done
#
# See Installation_Files/1-Installation_Help_Docs/appendix/E-Pi-Side_Recovery_Setup.md

set -euo pipefail

LOCK_FILE="/run/lock/reset_cr6_mcu_comms.lock"
MCU_SERIAL_ID="YOUR-MCU-SERIAL-ID-HERE"
MCU_DEV="/dev/serial/by-id/usb-${MCU_SERIAL_ID}-if00"

mkdir -p /run/lock
exec 9>"$LOCK_FILE"
flock -n 9 || exit 0

logger -t reset_cr6_mcu_comms "MCU add event detected; waiting for $MCU_DEV"

for _ in {1..20}; do
    if [ -e "$MCU_DEV" ]; then
        logger -t reset_cr6_mcu_comms "MCU device present; restarting klipper"
        /bin/systemctl restart klipper.service
        exit 0
    fi
    sleep 0.5
done

logger -t reset_cr6_mcu_comms "MCU device did not appear in time"
exit 1
