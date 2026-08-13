#  Upgrade Guide: Migrating DGUS‑Reloaded from Bullseye to Bookworm

Last Updated: 12 August 2026

## Applies To: 
Existing DGUS‑Reloaded installations running on MainsailOS 1.2.x (Bullseye).

## Purpose
This guide explains how to safely transfer your existing DGUS-Reloaded Klipper installation from MainsailOS Bullseye to MainsailOS Bookworm while preserving your settings, macros, configuration, and Pi-Side scripts.

This OS upgrade is mandatory if you want:
 * Moonraker notifications (PushOver, Telegram, Discord, Email, Webhooks)
 * Moonraker PushOver alerts for M600
 * Modern Moonraker components
 * Python 3.11 compatibility
 * Long‑term support from MainsailOS

## ⚠️ Important Notes Before You Begin:
 * This is a full operating system upgrade.  
   Debian does not support in‑place upgrades from 3.9 to 3.11 on MainsailOS.

 * KIAUH is not an operating‑system migration tool.
    It cannot replace Bullseye with Bookworm, migrate Python 3.9 → 3.11, update systemd service definitions, or rebuild the underlying OS image.
    For this reason, upgrading to Bookworm requires flashing a new MainsailOS Bookworm SD card.
   
 * Flashing will completely erase the Bullseye system, if you flash to the current SD card.
     If you have a second SD card, seriously consider flashing Bookworm to that instead of overwriting the Bullseye SD card.  That way, you can always restore your system by reinserting the Bullseye SD card, if anything goes seriously wrong with this update.
  
 * Pi-side scripts **MUST** contain Linux carriage returns (CR) and NOT Windows carriage return/line feed (CRLF).  
   If you receive an error like this when running any of the scripts, it likely means that your script lines end with `CRLF` instead of `CR`:

``` bash
... ‘bash\r’: No such file or directory
```

  To fix all Pi-Side scripts at once:
   Run:

``` bash
    sed -i 's/\r$//' ~/printer_data/config/scripts/*.sh
```

## 🧱 What Will Be Preserved With This Procedure
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

---

### 🧩 Step 1 — Back Up Your System
Run:

``` bash
bash ~/printer_data/config/scripts/backup_klipper.sh
```
NOTE: If you receive a "no such file" error when running the above script, see the note under "Important Notes Before You Begin" about converting CRLF to CR in all script files.


Then manually back up:
```
Code
~/printer_data/
~/klipper/
~/moonraker/
~/mainsail/
~/printer_data/config/scripts/
~/klipper_backups/
```

**Recommended backup method:**

From a second processor on the same network, running a Linux terminal, back up these folders from your Bullseye host to the second processor. 
 * Navigate to the target directory on the second processor
 * Replace <old-ip> with the actual ip address of the Bullseye host, before running them
 * Run each of these scripts in-turn:
``` bash
scp -r pi@<old-ip>:/home/pi/printer_data ./backup_printer_data
scp -r pi@<old-ip>:/home/pi/klipper ./backup_klipper
scp -r pi@<old-ip>:/home/pi/moonraker ./backup_moonraker
scp -r pi@<old-ip>:/home/pi/mainsail ./backup_mainsail
scp -r pi@<old-ip>:/home/pi/printer_data/config/scripts ./backup_scripts
scp -r pi@<old-ip>:/home/pi/klipper_backups ./backup_klipper_backups

```

**Alternative Backup Method**
If using an MS Windows machine and not comfortable with Linux terminal programs, this method also works:

 * Using an SFTP program like FileZilla, create and enter a new directory.
 * Download each of the above directories from the Bullseye host to the new directory on the Windows machine.


The above set of backups preserves:

 * Klipper configuration
 * Moonraker configuration
 * Mainsail UI configuration
 * DGUS‑Reloaded scripts
 * DGUS‑Reloaded Python modules and configuration files
 * All macros
 * All gcode files
 * All logs
 * All timelapse settings
 * All history
 * All klipper_backups

#### Why the Pi-Side scripts are backed up separately
This "redundant" backup is optional but recommended.

Although printer_data/config/scripts is included inside the main printer_data backup, it is backed up separately as well. This allows:

 * restoring scripts independently
 * comparing script versions
 * keeping scripts in a dedicated backup folder
 * recovering scripts even if printer_data is partially restored

---

### 🧩 Step 2 — Flash MainsailOS Bookworm
NB: Perform this step on your Windows or macOS laptop, not on the Pi.  
Tip: Using a new SD card is recommended. This preserves your Bullseye system and allows easy rollback or dual‑boot simply by swapping SD cards.


#### Option A — Use Raspberry Pi Imager’s built‑in MainsailOS (recommended)
Raspberry Pi Imager includes the latest official MainsailOS 3.x Bookworm (64‑bit) image.
This is the simplest and safest method.

 * Remove the SD card from your Raspberry Pi and insert it into your laptop.
(Or insert a brand‑new SD card if you want to preserve your Bullseye installation.)

 * Install latest Raspberry Pi Imager on your laptop and Open it.

 * Click Choose OS → 3D Printing → MainsailOS → MainsailOS (64‑bit). (Precise route through the menus may vary with Imager version)
   (This installs the same Bookworm image you would download manually in Option B.)

 * Click Choose Storage, then select your SD card.

 * Click the gear icon (⚙️) to open Advanced Options, and configure:

    Hostname:  
    mainsailos (or your preferred name)

    Locale options:  
    ✔ Capital of Wi‑Fi country (e.g., Ottawa/Canada)
    ✔ Time zone (e.g. Toronto)
    ✔ Keyboard layout (e.g. US)

    Enable SSH:  
    ✔ Enable SSH
    ✔ Use password authentication

    Set username and password:  
    Username: pi  
    Password: (your chosen password)

    Configure Wi‑Fi (if using wireless):  
    ✔ SSID
    ✔ Password

    Click Write.
    Raspberry Pi Imager will erase the old Bullseye installation (if reusing the card) and write Bookworm.

    When finished, reinsert the SD card into your Pi and boot the Pi.

#### Option B — Use a manually downloaded image (alternate method)
If you prefer to download the image yourself:

 * Download the latest MainsailOS Bookworm image from
    https://mainsail.xyz

 * Remove the SD card from your Raspberry Pi and insert it into your laptop.

 * Install or open Raspberry Pi Imager.

 * Click Choose OS → Use custom, then select the .img.xz file you downloaded.

 * Configure Advanced Options as described in Option A.

 * Click Write.

 * Reinsert the SD card into your Pi and boot the Pi.

---

### 🧩 Step 3 — Verify the Fresh Bookworm System Before Restoring Backups
**NB: Perform these checks immediately after the Pi boots Bookworm for the first time.**

When the Pi boots from the newly‑flashed SD card, MainsailOS Bookworm performs several automatic first‑boot tasks:

 * Expands the filesystem to use the full SD card
 * Initializes Moonraker
 * Initializes Mainsail
 * Sets up the default user environment
 * Starts SSH
 * Connects to Wi‑Fi (if configured in Raspberry Pi Imager)

Before restoring your backups, complete the following verification steps:

#### 3.1 Verify network connectivity

Check that the Pi has a valid IP:

**Tip:** On first boot, If you have a display screen connected to the pi, and if the pi has connected to the local network, MainsailOS displays the Pi’s IP address at the top of the console screen (e.g., My IP address is 192.168.0.xxx).

```bash
hostname -I
```
If using Ethernet, skip Wi‑Fi checks
If using Wi‑Fi, confirm it connected:

```bash
iwconfig
ping -c 3 google.com
```

If the Pi did not connect:
 * Reflash the SD card
   * Re‑enter the local Wi‑Fi SSID and password into Raspberry Pi Imager
   * Ensure Wi‑Fi country is set (e.g., CA for Canada)

#### 3.2 Verify SSH access
From your laptop (substitute <new-ip> with the ip of the Bookworm pi before running the command):

```bash
ssh pi@<new-ip>

or 
ssh pi@mainsailos.local
```

If SSH fails:
 * Ensure SSH was enabled in Raspberry Pi Imager
 * Reflash and reconfigure
 * Try Ethernet temporarily

#### 3.3 Confirm the filesystem expanded correctly

If you are no longer connected via SSH from step 3.2, then reconnect now.

Then run:

``` bash
df -h /
```

 * You should see the SD card’s full capacity (e.g., 32G, 64G, etc.), less what is allocated for system use.

   Example:
   ```Code
   pi@mainsailOS:~ $ df -h /
   Filesystem      Size  Used Avail Use% Mounted on
   /dev/mmcblk0p2   58G  8.0G   48G  15% /
   ```

| Field        | Meaning                                   | Interpretation                                      |
|--------------|--------------------------------------------|-----------------------------------------------------|
| Filesystem   | The device containing the root filesystem  | `/dev/mmcblk0p2` is the main SD‑card partition      |
| Size         | Total usable space after expansion         | ~58 GB is normal for a 64 GB SD card                |
| Used         | Space consumed by OS + installed packages  | 8 GB is typical for MainsailOS Bookworm             |
| Avail        | Free space available to the user           | 48 GB confirms the filesystem expanded correctly    |
| Use%         | Percentage of space used                   | 15% indicates plenty of free space                  |



  If instead the response still shows Size to be quite small compared to the SD card rating, and Use% to be quite high, reboot once:

```bash
sudo reboot
```

This time, the expansion should complete.

#### 3.4 Verify that Moonraker is running
On the Pi:

```bash
systemctl status moonraker
```
**🛰️ How to Interpret Moonraker Status**

When you run:

```bash
systemctl status moonraker
```
you are checking whether Moonraker is healthy on the new Bookworm system.
You do not need to understand every line — only the key indicators.

✔ What you want to see
1. Service is running

```Code
Active: active (running)
```
This is the single most important line.
It means Moonraker started correctly, its Python environment is valid, and Bookworm’s systemd configuration is working.

2. The correct Python environment is in use

```Code
/home/pi/moonraker-env/bin/python -m moonraker
```
This confirms Moonraker is running inside its dedicated virtual environment, not the system Python.

3. No errors or warnings appear

If the status output shows only informational lines (Git repo checks, version info, etc.), the service is healthy.

✔ What may look strange but is normal
1. The “Active since…” timestamp may show an old date

Example:

```Code
Active: active (running) since Mon 2026-04-20 ...
```
This does not mean that Moonraker has been running for months.
It simply reflects preserved state from your restored printer_data directory.
It will update after your full restore.

2. Git diagnostic lines are informational

Lines such as:

```Code
Is Dirty: False
Commits Behind Count: 0
Diverged: False
Pinned Commit: None
```
mean the local Moonraker Git repository is clean and up‑to‑date.
These are not errors.

3. Optional components (e.g., Sonar) may report their own status

Example:

```Code
Git Repo sonar: Validity check for git repo passed
```
This is normal and indicates the component is installed and healthy.

✔ When to proceed
If you see:

 
 * Active: active (running)
 * No red error messages
 * A valid Python path
 * Normal Git repo diagnostics

…then Moonraker is fully operational and you can safely continue to the next step of the upgrade.


If you do not see the above signs of a healthy Moonraker, try running these commands:

```bash
sudo systemctl restart moonraker
sudo systemctl enable moonraker
```

Then review the recent Moonraker logs:
```bash
journalctl -u moonraker -n 50 --no-pager
```
Look for any startup issues.
If you find errors, stop and troubleshoot/resolve them.

#### 3.5 Verify that Mainsail is running
In your laptop browser, open:

```Code
http://<new-ip>
(or http://mainsail.local, if that is the name you entered during the Mainsail pre-configuration)
```
You should see the Mainsail interface.

In the bottom left-hand corner of the Mainsail DASHBOARD is a question mark inside a circle.
Clicking on that question mark will expose two version numbers, explained in the following table.

| Component | Example Version                 | Meaning                                                   |
|-----------|---------------------------------|-----------------------------------------------------------|
| Mainsail  | `v2.17.0`                       | Confirms the updated Mainsail front‑end is installed      |
| Klipper   | `v0.10.0‑19‑g1ed102e`           | Shows Klipper is running and communicating with Moonraker |


If you cannot open mainsailos.local, try running these commands on the pi:

```bash
sudo systemctl restart mainsail
sudo systemctl enable mainsail
```
Then:
```bash
sudo systemctl status mainsail
```

#### 3.6 Verify the Pi’s clock and timezone
Incorrect time causes:

 * SSL certificate failures
 * Moonraker API errors
 * Klipper refusing to start

Check:

```bash
timedatectl
```
```bash
timedatectl status
```
This shows NTP sync state.

Example:

```Code
pi@mainsailOS:~ $ timedatectl
               Local time: Wed 2026-08-12 21:35:51 EDT
           Universal time: Thu 2026-08-13 01:35:51 UTC
                 RTC time: n/a
                Time zone: America/Toronto (EDT, -0400)
System clock synchronized: yes
              NTP service: active
          RTC in local TZ: no
```

If the reported timezone is wrong:
```bash
# List all available installed timezones
find /usr/share/zoneinfo -type f | sed 's|/usr/share/zoneinfo/||' | sort
```

# Set your timezone (replace <your-timezone> with one from the list)
```bash
sudo timedatectl set-timezone <your-timezone>
```
Examples:
```bash
sudo timedatectl set-timezone Europe/Berlin
sudo timedatectl set-timezone America/Los_Angeles
sudo timedatectl set-timezone Asia/Singapore
sudo timedatectl set-timezone Australia/Sydney
```

3.7 Verify that the SD card is healthy
Run:

```bash
sudo dmesg | grep mmc
```
🧩 How to Interpret SD Card dmesg Output
When you run:

```bash
sudo dmesg | grep mmc
```
you are checking whether the Raspberry Pi successfully detected your SD card, initialized it in high‑speed mode, and expanded the filesystem to use the full capacity of the card.

Only a few lines matter, and they are easy to recognize.

✔ What you want to see
The following table explains the key messages you should look for:


| Message Example                                           | Meaning                                                     |
|-----------------------------------------------------------|-------------------------------------------------------------|
| `mmc0: new ultra high speed DDR50 SDXC card`              | SD card detected and running in a high‑speed mode          |
| `mmcblk0: mmc0:aaaa SN64G 59.5 GiB`                       | Card capacity correctly identified (e.g., 64 GB SDXC)      |
| `mmcblk0: p1 p2`                                          | Boot (`p1`) and root (`p2`) partitions found               |
| `EXT4-fs (mmcblk0p2): mounted filesystem ...`             | Root filesystem mounted successfully                        |
| `EXT4-fs (mmcblk0p2): resizing filesystem ...`            | Filesystem expansion has started                            |
| `EXT4-fs (mmcblk0p2): resized filesystem to ...`          | Filesystem expansion completed successfully                 |

✔ What may look unusual but is normal:  
 * Multiple mount/remount lines  
EXT4 often mounts read‑only first, then switches to read‑write.
This is normal during first boot.

 * “orphan cleanup” messages  
EXT4 performs routine housekeeping.
Not an error.

 * SDIO device detection (mmc1)  
This is the onboard WiFi chip, not your SD card.

✔ When to proceed

If you see:

 * The SD card detected in high‑speed mode

 * Partitions p1 and p2 listed

 * EXT4 mounting without errors

 * A successful filesystem resize

…then your SD card is fully initialized and ready, and you can safely continue to the next step of the upgrade.

If instead errors appear, replace the SD card and restart this process at Step 2.


#### 3.8 Optional: Update system packages

**NB: This step may take several minutes depending on your Pi model and SD card speed.**

```bash
sudo apt update
sudo apt upgrade -y
sudo apt autoremove -y
```
This ensures Bookworm is fully up to date before restoring your Klipper/Moonraker environment.

3.10 Only proceed to Step 4 (Restore Backups) once all checks pass
This ensures the restore process runs on a stable, fully‑initialized Bookworm system.

The above checks prevent:
 * corrupted restores
 * Moonraker failing to start
 * Klipper refusing to load configs
 * broken DGUS‑Reloaded Pi-Side scripts
 * missing dependencies
 * filesystem expansion issues
 * network failures during restore

---

### 🧩 Step 4 — Restore Your Backups
NB: Perform these restores from your Windows/macOS laptop, using the backups you created in Step 1.  
Replace <new-ip> with the IP address of your Bookworm Pi.

**NB: scp -r  overwrites existing directories, replacing their previous contents.**

You have two restore options depending on how much you want to bring back:

#### ⭐ Option A — Full Restore (Recommended)
Restore all backed‑up directories:

bash
scp -r ./backup_printer_data pi@<new-ip>:/home/pi/printer_data
scp -r ./backup_klipper pi@<new-ip>:/home/pi/klipper
scp -r ./backup_moonraker pi@<new-ip>:/home/pi/moonraker
scp -r ./backup_mainsail pi@<new-ip>:/home/pi/mainsail
scp -r ./backup_scripts pi@<new-ip>:/home/pi/printer_data/config/scripts
scp -r ./backup_klipper_backups pi@<new-ip>:/home/pi/klipper_backups

This restores:
 * Klipper source
 * Klipper configs
 * Moonraker configs^
 * Mainsail configs*
 * DGUS‑Reloaded Pi-Side scripts
 * Klipper backup archives
 * All macros, logs, history, timelapse settings, etc.

^NOTE: Restoring moonraker/ will overwrite Bookworm’s default update‑manager configuration. This is expected, but advanced users may wish to review update_manager settings after restore.
*NOTE: Restoring mainsail/ will overwrite any default Bookworm UI settings with your Bullseye UI configuration.

#### ⭐ Option B — Minimal Restore (Advanced Users Only)

Restore only the essential configuration directories:

``` bash
scp -r ./backup_printer_data pi@<new-ip>:/home/pi/printer_data
scp -r ./backup_klipper pi@<new-ip>:/home/pi/klipper
scp -r ./backup_moonraker pi@<new-ip>:/home/pi/moonraker
```

Use this only if:

 * you want a clean Mainsail install
 * you want to manually reinstall Pi-Side scripts
 * you want to keep Bookworm’s default UI configuration

Most users should choose Option A.

#### ⭐ Restart Required Services
After restoring files, SSH into the Pi:

```bash
ssh pi@<new-ip>
```

Restart all relevant services:

```bash
sudo systemctl restart moonraker
sudo systemctl restart mainsail
sudo systemctl restart klipper
```

Enable services to ensure they start automatically:

```bash
sudo systemctl enable moonraker
sudo systemctl enable mainsail
sudo systemctl enable klipper
```
#### ⭐ Verify the restore
From your laptop:

 * Open Mainsail:
    http://<new-ip>
    or
    http://mainsail.local

 * Confirm Klipper loads your printer configuration
 * Confirm Moonraker API is responding
 * Confirm macros, scripts, and UI settings are present
 * Confirm your printer connects normally

---

### 🧩 Step 5 — Post‑Restore Validation (Confirm Everything Works Before Printing)
NB: Perform these checks immediately after completing Step 4.  
Your Bookworm system now contains your restored Klipper, Moonraker, Mainsail, scripts, and configuration files.
Before attempting any prints, verify that all components are functioning correctly.

#### 5.1 Verify Moonraker is fully operational
On the Pi:

```bash
systemctl status moonraker
```
You should see:

```Code
Active: active (running)
```
If not:
```bash
sudo systemctl restart moonraker
```
Check logs for errors:

```bash
journalctl -u moonraker -n 50 --no-pager
```
Resolve any issues before continuing.

#### 5.2 Verify Mainsail is fully operational
From your laptop:

Open:

```Code
http://<new-ip>
```
or:
```Code
http://mainsailos.local
```

Confirm:

 * The Mainsail UI loads
 * The dashboard shows Moonraker connected
 * No “Moonraker offline” or “Klipper not ready” errors

If Mainsail fails:

```bash
sudo systemctl restart mainsail
systemctl status mainsail
```

#### 5.3 Verify Klipper loads your configuration
In Mainsail:

 * Open Machine → Klipper Configuration
 * Confirm your restored printer.cfg and other config files appear
 * Check for syntax errors or warnings
 * Click Restart Klipper

Or from SSH:

```bash
sudo systemctl restart klipper
systemctl status klipper
```

If Klipper reports configuration errors, fix them before continuing.

NOTE: If you previously used custom Python virtual environments, verify that your restored configuration does not reference old Python 3.9 paths.

#### 5.4 Verify DGUS‑Reloaded Pi-Side scripts and macros

In Mainsail:

 * Open Machine → Macros
 * Confirm your macros are present
 * Confirm DGUS‑Reloaded Pi-Side scripts appear under printer_data/config/scripts
 * Run a simple macro (e.g., STATUS_READY) to confirm Klipper responds normally

If Pi-Side scripts fail to run:

 * Check file permissions
  ```bash
  chmod +x ~/printer_data/config/scripts/*.sh
  ```
 * Convert any CRLF line endings to CR
 ``` bash
    sed -i 's/\r$//' ~/printer_data/config/scripts/*.sh
 ```
 * Check Moonraker logs for script‑related errors

#### 5.5 Verify printer hardware connectivity

In Mainsail:

 * Confirm the printer MCU is connected
 * Confirm temperature sensors report correct values
 * Confirm fans and heaters appear in the dashboard
 * Confirm the printer responds to:
   * Home X/Y/Z
   * Move commands
   * Fan commands
   * Heater commands

If the MCU is offline:

 * Check Klipper logs
 * Check USB cable
 * Rebuild firmware if needed
 * Reflash MCU

#### 5.6 Verify your restored Mainsail settings

Check:
 * Camera settings (if applicable)
 * Timelapse configuration
 * History and job logs
 * Custom UI settings
 * Printer profiles
 * Temperature presets

Ensure everything matches your Bullseye system.

#### 5.7 Verify your restored Moonraker configuration

Check:

 * API keys
 * Update manager configuration
 * Notifications
 * Plugins
 * Timelapse settings
 * File paths

Restart Moonraker if needed:
```bash
sudo systemctl restart moonraker
```

#### 5.8 Verify your restored Klipper backups

If you restored klipper_backups/, confirm:

```bash
ls -l /home/pi/klipper_backups
```

You should see:

 * .tar.gz backup archives
 * .commit files

These allow rollback or firmware rebuilds if needed.

#### 5.9 Perform a controlled test of basic printer functions

In Mainsail:

 * Heat the hotend to 150 °C*
 * Heat the bed to 50 °C
 * Home all axes
 * Move the toolhead 10 mm in X/Y/Z
 * Run a small test macro (e.g., STATUS_READY)
 * Run a dry‑run of a simple gcode file (no filament)

*Ensure filament is removed before heating.  This prevents accidental filament cooking.

Everything should behave normally.

#### 5.10 Only proceed to Step 6 (Optional: Rebuild MCU Firmware) once all checks pass

This ensures:

 * Klipper is stable
 * Moonraker is stable
 * Mainsail is stable
 * The Pi-Side Scripts are functional
 * Hardware is responding
 * No configuration errors remain
 * The system is ready for firmware rebuild or printing

---

## 🧩 Step 6 — (Optionally) Install Moonraker Notifications (with PushOver Support)
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

---

### 🧩 Step 7 — Validate DGUS‑Reloaded

Check:

 * Display responds to inputs and button presses
 * Display Page switching works
 * Variables update on display
 * M600 triggers PushOver, if this line is added to the M600 macro: 
 * No errors in klippy.log

---

### 🧩 Step 8 — Validate Moonraker
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

---

## 🎉 Upgrade Is Complete!
Your DGUS‑Reloaded installation is now running on:

 * Python 3.11
 * Modern Moonraker
 * Modern MainsailOS

Moonraker Now Has:

 * Full notifications support
 * Full PushOver support
