#  Upgrade Guide: Migrating DGUS‑Reloaded from Bullseye to Bookworm

Last Updated: 12 August 2026

## Applies To: 
Existing DGUS‑Reloaded installations running on MainsailOS 1.2.x (Bullseye).

## Purpose
Bullseye cannot load Moonraker’s notifications plugin and cannot support sending notifications from your printer (e.g. through PushOver, when M600 fires).

This guide explains how to safely upgrade your Klipper host from MainsailOS Bullseye to MainsailOS Bookworm while preserving your DGUS‑Reloaded installation, macros, configuration, and scripts.

This upgrade is mandatory if you want:
 * Moonraker notifications (PushOver, Telegram, Discord, Email, Webhooks)
 * Moonraker PushOver alerts for M600
 * Modern Moonraker components
 * Python 3.11 compatibility
 * Long‑term support from MainsailOS

## ⚠️ Important Notes Before You Begin:
 * This is a full operating system upgrade.  
   Debian does not support in‑place upgrades from 3.9 to 3.11 on MainsailOS.

 * You must reflash the SD card.  
   KIAUH cannot perform this upgrade.

 * DGUS‑Reloaded is fully compatible with Python 3.11.  
   No code changes are required.

 * All DGUS‑Reloaded Python modules have been audited for Python 3.11 compatibility and confirmed safe.

 * The Pi‑side scripts are all Bash scripts and will continue to work.
  
 * Pi-side scripts **MUST** contain Linux carriage returns (CR) and NOT Windows carriage return/line feed (CRLF).  
   If you receive an error like this when running any of the scripts, it likely means that your script lines end with `CRLF` instead of `CR`:
```
... ‘bash\r’: No such file or directory
```

  To fix all scripts at once:
   Run:

``` bash
    sed -i 's/\r$//' ~/printer_data/config/scripts/*.sh
```

## 🧱 What Will Be Preserved
You will keep:

 * All DGUS‑Reloaded configuration
 * All DGUS‑Reloaded Python modules
 * All DGUS‑Reloaded scripts
 * All macros
 * All Klipper configuration
 * All Moonraker configuration
 * All timelapse settings
 * All history and job logs
 * All gcode files
 * All custom scripts in ~/printer_data/config/scripts/

❌ What Will NOT Be Preserved Automatically
 * The OS itself
 * System‑level packages
 * Python virtual environments
 * Systemd service overrides
 * Any custom software installed outside ~/printer_data or ~/klipper

**If you installed anything manually under /usr/local, back it up separately.**

### 🧩 Step 1 — Back Up Your System
Run:

``` bash
bash ~/printer_data/config/scripts/backup_klipper.sh
```
Then manually back up:
```
Code
~/printer_data/
~/klipper/
~/moonraker/
~/mainsail/
~/printer_data/config/scripts/
```
Recommended method:

``` bash
scp -r pi@<old-ip>:/home/pi/printer_data ./backup_printer_data
scp -r pi@<old-ip>:/home/pi/klipper ./backup_klipper
```

### 🧩 Step 2 — Flash MainsailOS Bookworm

 * Download the latest Bookworm image from:

    https://mainsail.xyz

 * Flash using Raspberry Pi Imager or Balena Etcher.

 * Boot the Pi.

### 🧩 Step 3 — Restore Your Backups
Copy your backups back:

``` bash
scp -r ./backup_printer_data pi@<new-ip>:/home/pi/printer_data
scp -r ./backup_klipper pi@<new-ip>:/home/pi/klipper
```
Restart services:

``` bash
sudo systemctl restart klipper
sudo systemctl restart moonraker
```

### 🧩 Step 4 — Reinstall DGUS‑Reloaded Scripts
If your scripts were stored under:

Code
~/printer_data/config/scripts/

They will already be restored.

If not, redeploy them using the Pi-Side scripts installation instructions.

## 🧩 Step 5 — (Optionally) Install Moonraker Notifications (with PushOver Support)
Now that you are on Bookworm, the moonraker_notifidations.sh script exists:

``` bash
cd ~/moonraker
./scripts/install-moonraker-notifications.sh
Restart Moonraker:
```
```bash
sudo systemctl restart moonraker
```

Add to moonraker.conf:

``` ini
[notifications]
enable: True

[push_over]
token = <your-token>
user_key = <your-user-key>
```

Test:

```bash
RESPOND PREFIX="notify" MSG="DGUS-Reloaded Bookworm upgrade successful"
```

### 🧩 Step 6 — Validate DGUS‑Reloaded
Run:

``` bash
bash ~/printer_data/config/scripts/verify_installation.sh
```

Check:

 * Display responds to inputs and button presses
 * Display Page switching works
 * Variables update on display
 * M600 triggers PushOver, if this line is added to the M600 macro: 
 * No errors in klippy.log

### 🧩 Step 7 — Validate Moonraker
Check:

```bash
systemctl status moonraker
journalctl -u moonraker -n 200 --no-pager
```
Ensure:

 * Notifications component loads
 * PushOver loads
 * No “unparsed config section” warnings in Moonraker.log or Mainsail Notifications
 * No Python errors

## 🎉 Upgrade Complete
Your DGUS‑Reloaded installation is now running on:

 * Python 3.11
 * Modern Moonraker
 * Modern MainsailOS

Moonraker Now Has:

 * Full notifications support
 * Full PushOver support
