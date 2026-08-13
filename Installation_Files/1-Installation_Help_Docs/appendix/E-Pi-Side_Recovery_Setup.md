# Appendix E: Automatic MCU Communications Recovery After Printer Power-Cycle

Last Updated: 13 August 2026

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

## Step 0: Find Your MCU_SERIAL_ID Value

You only need one value from your Pi before installing the files: **MCU_SERIAL_ID**.
Run this command over SSH.

### 0a. Find MCU_SERIAL_ID from udev

```bash
for d in /dev/ttyACM*; do [ -e "$d" ] || continue; echo "$d -> $(udevadm info -q property -n "$d" | sed -n 's/^ID_SERIAL=//p')"; done
```

You will see output like:

```
/dev/ttyACM0 -> Klipper_stm32f103xe_30FFDB054254353915721557
/dev/ttyACM1 -> Klipper_stm32f103xe_30FFDB054254353915721557
```

The value after `->` is your **MCU_SERIAL_ID**.  Example:

```
Klipper_stm32f103xe_30FFDB054254353915721557
```

### 0b. Optional sanity check of the by-id path

The recovery script builds this path automatically as:

```
/dev/serial/by-id/usb-${MCU_SERIAL_ID}-if00
```

You can verify your Pi exposes that path with:

```bash
ls /dev/serial/by-id/
```

You should see an entry like:

```
usb-Klipper_stm32f103xe_30FFDB054254353915721557-if00
```

---

## Step 1: Create the Recovery Script (using sudo nano)

This script is run automatically when the MCU USB device appears.  It waits for the
device to be ready, then restarts Klipper.

1. On your PC, open this template from the extracted release:
   `Installation_Files/6-Pi-side_scripts/usr/local/reset_cr6_mcu_comms.sh`
2. In your Pi SSH session, run:

```bash
sudo nano /usr/local/reset_cr6_mcu_comms.sh
```

3. Paste the full template content into nano.
4. Edit this line in the pasted file:

```bash
MCU_SERIAL_ID="YOUR-MCU-SERIAL-ID-HERE"
```

Replace `YOUR-MCU-SERIAL-ID-HERE` with your MCU_SERIAL_ID value from Step 0a.

Do not add `usb-` or `-if00` to this value.  The script appends those automatically
when it builds `MCU_DEV`.
5. Save and exit nano: `Ctrl+O`, `Enter`, then `Ctrl+X`.

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

## Step 2: Create the systemd Service Unit (using sudo nano)

This file tells systemd what to run when the udev rule fires.

1. On your PC, open this template from the extracted release:
    `Installation_Files/6-Pi-side_scripts/etc/systemd/system/reset_cr6_mcu_comms.service`
2. In your Pi SSH session, run:

```bash
sudo nano /etc/systemd/system/reset_cr6_mcu_comms.service
```

3. Paste the full template content into nano.
4. Save and exit nano: `Ctrl+O`, `Enter`, then `Ctrl+X`.

Verify the file was created:

```bash
cat /etc/systemd/system/reset_cr6_mcu_comms.service
```

---

## Step 3: Create the udev Rule (using sudo nano)

This file watches for the MCU USB device to appear and tells systemd to run the service.

**NB:** The BTT SKR CR6 board uses a Native USB serial interface (which is mounted as ttyACM*). However, Creality stock boards use a CH340 USB-to-Serial bridge chip via UART (Serial (on USART1 PA10/PA9)), which mounts as ttyUSB*.
For this reason, there are two versions of the udev Rule template in 6-Pi-side_scripts/etc/udev/rules.d.
**Take care to open the template that corresponds to the motherboard in your printer!**

1. On your PC, open this template from the extracted release:
    `Installation_Files/6-Pi-side_scripts/etc/udev/rules.d/<your motherboard>/99-reset_cr6_mcu_comms.rules`
2. In your Pi SSH session, run:

```bash
sudo nano /etc/udev/rules.d/99-reset_cr6_mcu_comms.rules
```

3. Paste the full template content into nano.
4. Replace `YOUR-MCU-SERIAL-ID-HERE` with your MCU_SERIAL_ID value from Step 0a.
5. Save and exit nano: `Ctrl+O`, `Enter`, then `Ctrl+X`.

Verify the file was created:

```bash
cat /etc/udev/rules.d/99-reset_cr6_mcu_comms.rules
```

Confirm the line contains your MCU_SERIAL_ID value and `reset_cr6_mcu_comms.service`.

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

Now **power-cycle the printer** (switch it off, wait 5 seconds, switch back on).


### Window 1 — review the recovery script activity:

```bash
journalctl -f -t reset_cr6_mcu_comms
```

### Window 2 — review Klipper's recovery activity:

```bash
journalctl -f -u klipper
```

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

Run this command on the Pi and check whether your MCU_SERIAL_ID value appears correctly in the rule:

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
