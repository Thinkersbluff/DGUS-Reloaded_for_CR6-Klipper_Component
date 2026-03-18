# Appendix E: Automatic MCU Communications Recovery After Printer Power-Cycle

Last Updated: 17 March 2026

---

## Purpose
CR6 printers lose USB communications between Klipper and the CR6 motherboard every time the printer is power-cycled.  Klipper shows an error such as `Unable to connect` or `Lost communication with MCU` after the printer is switched on, even though the Pi stayed powered the whole time.  DWIN_SET stays on the boot screen, which shows RESTART and FIRMWARE RESTART buttons, but those buttons do not work at that point because we have lost comms with Klipper.

This appendix describes how to install a three-file Pi-side recovery mechanism that:

- Detects when the CR6 motherboard USB device re-appears on the Pi after printer power-on
- Waits for the stable device path to be ready
- Automatically restarts Klipper

This applies to **all CR6 USB-connected motherboards**:

- BTT SKR CR6 V1.0
- Creality ERA 1.1.0.3
- Creality 4.5.2
- Creality 4.5.3

---

## Prerequisites

- SSH access to your Raspberry Pi
- The `pi` user (or your Klipper user) must have `sudo` privilege
- Klipper must already be installed and working when the printer USB is connected

---

## Step 0: Find Your MCU Device Values

You need two values from your Pi before you can install the files.  Run these commands over SSH.

### 0a. Find your MCU serial path

```bash
ls /dev/serial/by-id/
```

You will see one or more entries.  Copy the full name of the entry that contains `Klipper`, for example:

```
usb-Klipper_stm32f103xe_30FFDB054254353915721557-if00
```

This is your **MCU_DEV value**.  The full path you will use is `/dev/serial/by-id/` followed by that entry name.

### 0b. Find your MCU udev serial ID

```bash
for d in /dev/ttyACM*; do [ -e "$d" ] || continue; echo "$d -> $(udevadm info -q property -n "$d" | sed -n 's/^ID_SERIAL=//p')"; done
```

You will see output like:

```
/dev/ttyACM0 -> Klipper_stm32f103xe_30FFDB054254353915721557
/dev/ttyACM1 -> Klipper_stm32f103xe_30FFDB054254353915721557
```

The value after `->` is your **ID_SERIAL value**.

> **Note:** Both commands may show results for multiple USB interfaces from the same board.  Use the same string for both — the part that looks like `Klipper_stm32f103xe_30FFDB054254353915721557` (without the `-if00` suffix).

---

## Step 1: Create the Recovery Script

This script is run automatically when the MCU USB device appears.  It waits for the device to be ready, then restarts Klipper.

Copy and paste the entire block below into your SSH window.

**Replace `YOUR-MCU-SERIAL-ID-HERE` with your MCU_DEV value from Step 0a.**

```bash
sudo bash -c 'cat > /usr/local/reset_cr6_mcu_comms.sh' << 'SCRIPTEOF'
#!/bin/bash
set -euo pipefail

LOCK_FILE="/run/lock/reset_cr6_mcu_comms.lock"
MCU_DEV="/dev/serial/by-id/YOUR-MCU-SERIAL-ID-HERE"

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
SCRIPTEOF'
```

Then make it executable:

```bash
sudo chmod +x /usr/local/reset_cr6_mcu_comms.sh
```

Verify the file was created:

```bash
ls -l /usr/local/reset_cr6_mcu_comms.sh
```

Expected output:
```
-rwxr-xr-x 1 root root ... /usr/local/reset_cr6_mcu_comms.sh
```

---

## Step 2: Create the systemd Service Unit

This file tells systemd what to run when the udev rule fires.

Copy and paste the entire block below into your SSH window:

```bash
sudo bash -c 'cat > /etc/systemd/system/reset_cr6_mcu_comms.service' << 'SVCEOF'
[Unit]
Description=Reset CR6 MCU communications — restart Klipper when MCU USB appears
After=multi-user.target

[Service]
Type=oneshot
ExecStart=/usr/local/reset_cr6_mcu_comms.sh
SVCEOF'
```

Verify the file was created:

```bash
cat /etc/systemd/system/reset_cr6_mcu_comms.service
```

---

## Step 3: Create the udev Rule

This file watches for the MCU USB device to appear and tells systemd to run the service.

Copy and paste the entire block below.

**Replace `YOUR-ID-SERIAL-VALUE-HERE` with your ID_SERIAL value from Step 0b.**

```bash
sudo bash -c 'cat > /etc/udev/rules.d/99-reset_cr6_mcu_comms.rules' << 'UDEVEOF'
ACTION=="add", SUBSYSTEM=="tty", KERNEL=="ttyACM*", ENV{ID_SERIAL}=="YOUR-ID-SERIAL-VALUE-HERE", TAG+="systemd", ENV{SYSTEMD_WANTS}+="reset_cr6_mcu_comms.service"
UDEVEOF'
```

Verify the file was created:

```bash
cat /etc/udev/rules.d/99-reset_cr6_mcu_comms.rules
```

Confirm the line contains your ID_SERIAL value and `reset_cr6_mcu_comms.service`.

---

## Step 4: Reload systemd and udev

Tell the Pi to use the new files:

```bash
sudo systemctl daemon-reload
sudo udevadm control --reload-rules
```

---

## Step 5: Test the Recovery

Open **two SSH windows** on the Pi at the same time.

### Window 1 — watch the recovery script activity:

```bash
journalctl -f -t reset_cr6_mcu_comms
```

### Window 2 — watch Klipper:

```bash
journalctl -f -u klipper
```

Now **power-cycle the printer** (switch it off, wait 5 seconds, switch back on).

### Expected results in Window 1:

```
reset_cr6_mcu_comms[XXXX]: MCU add event detected; waiting for /dev/serial/by-id/...
reset_cr6_mcu_comms[XXXX]: MCU device present; restarting klipper
```

### Expected results in Window 2:

You will see Klipper stop, then start again:

```
systemd[1]: Stopping Klipper 3D Printer Firmware...
systemd[1]: Stopped Klipper 3D Printer Firmware.
systemd[1]: Started Klipper 3D Printer Firmware.
```

### Expected display on KlipperScreen / Mainsail / Fluidd:

During the restart, KlipperScreen may briefly show:

```
Unable to retrieve printer information from Moonraker
```

This is **normal and expected** during the Klipper restart.  The display will recover and show the Ready state within a few seconds.

### If the recovery script does not fire:

Run this command on the Pi and check whether your ID_SERIAL value appears correctly in the rule:

```bash
cat /etc/udev/rules.d/99-reset_cr6_mcu_comms.rules
```

Then confirm the udev rule matches what the Pi actually sees:

```bash
for d in /dev/ttyACM*; do [ -e "$d" ] || continue; echo "$d -> $(udevadm info -q property -n "$d" | sed -n 's/^ID_SERIAL=//p')"; done
```

The value in the rule must match the value returned by the command above exactly.

---

## Rollback: How to Remove This Setup

If you need to remove the recovery mechanism:

```bash
sudo rm /etc/udev/rules.d/99-reset_cr6_mcu_comms.rules
sudo rm /etc/systemd/system/reset_cr6_mcu_comms.service
sudo rm /usr/local/reset_cr6_mcu_comms.sh
sudo udevadm control --reload-rules
sudo systemctl daemon-reload
```

After removing, Klipper will no longer auto-restart when the printer is power-cycled.

---

## How It Works (Brief Technical Summary)

- The **udev rule** watches the Linux USB subsystem for a new `ttyACM*` device with the correct serial ID.
- When the printer is switched on, the MCU USB device appears and the rule fires.
- udev asks **systemd** to start `reset_cr6_mcu_comms.service`.
- The **service** runs the shell script.
- The **script** uses a lock file to prevent duplicate runs (the board shows up on two USB interfaces), waits up to 10 seconds for the stable device symlink to appear, then calls `systemctl restart klipper.service`.
- Klipper reconnects to the MCU and returns to Ready state.

This does not perform a hardware reset of the MCU.  It recovers comms from the situation where the Pi-to-MCU USB link is working but Klipper needs to be restarted to detect it.
