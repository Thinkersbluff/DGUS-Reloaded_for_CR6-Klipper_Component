#  Upgrading: Migrating an Existing DGUS‑Reloaded Installation to a New MainsailOS
** CAUTION: THIS GUIDE IS A WORK-IN_PROCESS. DO NOT RELY ON THIS GUIDE UNTIL THIS NOTICE IS REMOVED!!**

Last Updated: 14 August 2026

## Applies To: 
Existing DGUS‑Reloaded installations running on an outdated version of MainsailOS.

## Purpose
This guide explains how to safely transfer your existing DGUS-Reloaded Klipper installation while preserving what you can of any customisations you have made in ~printer_data and in ~klipper/klippy/extras.  You will still need to reinstall some things, but it should help you get back up and running on the new OS with the minimum risk and effort.

## Backgrounder
A MainsailOS upgrade is mandatory if you want to take advantage of the latest features and those features rely on an updated version of Python.  (e.g. Mainsail 1.2.x (BUllseye) relies on Python 3.9, which is now at end of life and  no longer supported.)

The only way to upgrade MainsailOS is to re-flash the Host with the latest version, which will in-turn erase the SD card (or will require a new SD card), removing all of the customizations you may have made to printer.cfg, etc..

You do have that option, and can certainly follow the instructions in 1-Installation_Manual.md, to make a fresh installation of MainsailOS and DGUS-Reloaded for CR6.

This guide is intended for users who prefer to backup their current system and then to restore what they can of that backup to the newly flashed upgraded system, rather than recreate it. 

The workflow is only slightly more complicated, to make and restore the applicable backups rather than to make a fresh install.  The "pay-off" is that you can avoid having to repeat a lot of the customisation work that you already completed to create your current DGUS-Reloaded installation.  Your call...


## ⚠️ Important Notes Before You Begin:
 * This is a full operating system upgrade.  
   Debian does not support in‑place upgrades from Python 3.9 to 3.11 or higher on MainsailOS.

 * KIAUH is not an operating‑system migration tool.
    You cannot avoid reflashing the SD card by piecemeal upgrading the individual elements with KIAUH. 
    For this reason, upgrading MainsailOS requires flashing MainsailOS onto a new SD card (recommended) or overwriting the current SD card.
   
 * Flashing will completely erase the existing system, if you flash to the current SD card.
     If you have a second SD card, seriously consider flashing Bookworm to that instead of overwriting the Bullseye SD card.  That way, you can always restore your system by reinserting the Bullseye SD card, if anything goes seriously wrong with this update.

 * You will need to recreate some of the Pi-Side files (like .service and .rules files) on your upgraded system and will need to reinstall 3rd party helper apps like Stable_Z_Home.py and gcode_shell_command.py, but these processes are quick and easy to complete, following the instructions in the Installation_Manual.
  
 * All of the Pi-side scripts copied to ~printer_data/config/scripts **MUST** contain Linux carriage returns (CR) and NOT Windows carriage return/line feed (CRLF).  They also must be made executable on the Linux system.  This guide includes simple commands that you can use to ensure that both of these conditions have been met. 


## 🧱 What Will Be Preserved With This Procedure
You will keep:

 * All of the DGUS‑Reloaded files: 
   * ~klipper/klippy/extras/t5uid1 and its subfolders
   * ~/printer_data/config/scripts/
 * All of the Mainsail Klipper Machine files in ~/printer_data/config, where most of your customizations and macros reside
 * The local Klipper git repository (as a tar.gz backup file and Commit reference)

❌ What Will NOT Be Preserved Automatically
 * The OS itself
 * System‑level packages
 * Python virtual environments
 * Systemd service overrides
 * Any custom software installed outside ~/printer_data or ~/klipper (e.g. KlipperScreen)

**If you installed anything manually under /usr/local, you must back it up yourself or re-install it on the new (upgraded) Host.**

---

### 🧩 Step 1 — Back Up Your System
Run:

``` bash
bash ~/printer_data/config/scripts/backup_klipper.sh
```
NOTE: If you receive a "no such file" error when running the above script, see the note under "Important Notes Before You Begin" about the need to convert CRLF to CR in all script files and the need to make them executable.


Then manually back up (copy):
```
Code
~/printer_data/
~/klipper_backups/
~/klipper/klippy/t5uid1
```

**Recommended backup method:**

From a second processor on the same network, running a Linux terminal, back up these folders from your Bullseye host to the second processor. 
 * Navigate to the target directory on the second processor
 * Replace <old-ip> with the actual ip address of the host being backed-up, before running them
 * Run each of these scripts in-turn:
``` bash
scp -r pi@<old-ip>:/home/pi/printer_data ./backup_printer_data
scp -r pi@<old-ip>:/home/pi/klipper_backups ./backup_klipper_backups
scp -r pi@<old-ip>:/home/pi/klipper/klippy/extras/t5uid1 ./backup_dgus-reloaded
scp -r pi@<new-ip>:/usr/local/*.sh ./backup_usr_local

```

**Alternative Backup Method**
If using an MS Windows machine and not comfortable with Linux terminal programs, this method also works:

 * Using an SFTP program like FileZilla, create and enter a new directory.
 * Download each of the above directories from the Bullseye host to the new directory on the Windows machine.


The above set of backups preserves:

 * All klipper_backups
 * The DGUS-Reloaded Klipper COmponent as you have tailored it for your printer
 * The Mainsail|Klipper|Moonraker|etc. configuration files as you have tailored them for your printer

You will be able to restore your tailored files to the new upgraded host, from these backups.
You will need to reinstall other elements of the system, which can not simply be copied. 

Don't worry, we will guide you through all of that restoration activity at step 4. 

If it helps relieve your mind, I recommend that you keep the current SD card aside, and flash the new MainsailOS to a new SD card.  That way, you can always fall-back to reinserting the original card back into the Host and deferring this upgrade altogether.

---

### 🧩 Step 2 — Flash the Newest MainsailOS
NB: Perform this step on your Windows or macOS laptop, not on the Pi.  
Tip: Using a new SD card is recommended. This preserves your current system and allows easy rollback or dual‑boot simply by swapping SD cards.


#### Option A — Use Raspberry Pi Imager’s built‑in MainsailOS (recommended)

This is the simplest and safest method.
Raspberry Pi Imager includes the latest official MainsailOS (64‑bit) image.

 * Remove the SD card from your Raspberry Pi and insert it into your laptop.
(Or insert a brand‑new SD card if you want to preserve your current installation.)

 * Download and install the latest Raspberry Pi Imager on your laptop and Open it.

 * Click Device → Choose Other specific-purpose OS → 3D Printing → MainsailOS → MainsailOS (64‑bit). (Precise route through the menus may vary with Imager version)
   (This installs MainsailOS from the same image you would otherwise download manually in Option B.)

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

### 🧩 Step 3 — Verify the Fresh System Before Restoring Backups
**NB: Perform these checks immediately after the Pi boots MainsailOS for the first time.**

When the Pi boots from the newly‑flashed SD card, MainsailOS performs several automatic first‑boot tasks:

 * Expands the filesystem to use the full SD card
 * Initializes Moonraker
 * Initializes Mainsail
 * Sets up the default user environment
 * Starts SSH
 * Connects to Wi‑Fi (if configured in Raspberry Pi Imager)

Before restoring your backups (at step 4), complete the following verifications:

#### 3.1 Verify network connectivity

Check that the Pi has a valid IP:

**Tip:** On first boot, If you have a display screen connected to the pi, and if the pi has connected to the local network, MainsailOS displays the Pi’s IP address at the top of the console screen (e.g., My IP address is 192.168.0.xxx).

If you must SSH into the host to interact with it, this next step assumes you have correctly enabled SSH and that you remember your password.  If you can not SSH into the Pi, you will need to repeat step 2.

```bash
hostname -I
```
If using Ethernet, skip Wi‑Fi checks
If using Wi‑Fi, confirm the Pi has Internet access:

```bash
iwconfig
ping -c 3 google.com
```

If the Pi did not connect:
 * Reflash the SD card
   * Re‑enter the local Wi‑Fi SSID and password into Raspberry Pi Imager
   * Ensure correct Wi‑Fi country capital is set (e.g., Ottawa for Canada)

#### 3.2 Verify SSH access
From your laptop (substitute <new-ip> with the ip of the new Host before running the command):

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

Via SSH, run this command on the host:

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
(or http://mainsailos.local, if mainsailos is the name you entered during the Mainsail pre-configuration)
```
You should see the Mainsail interface in your browser.

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



#### 3.9 Only proceed to Step 4 (Restore Backups) once all checks pass

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

#### Copy the Backed-up Files to the Upgraded Host
NB: Perform these restores from your Windows/macOS laptop, using the backups you created in Step 1.  
Replace <new-ip> with the IP address of your Bookworm Pi.

**NB: scp -r  overwrites existing directories, replacing their previous contents.**

```bash
scp -r ./backup_dgus-reloaded pi@<new-ip>:/home/pi/klipper/klippy/extras/t5uid1 
scp -r ./backup_printer_data pi@<new-ip>:/home/pi/printer_data
scp -r ./backup_klipper_backups pi@<new-ip>:/home/pi/klipper_backups
scp -r ./backup_usr_local pi@<new-ip>:/usr/local
```
This restores:
* All of the DGUS‑Reloaded files: 
   * ~klipper/klippy/extras/t5uid1 and its subfolders
   * ~/printer_data/config/scripts/
 * All of the Mainsail Klipper Machine files in ~/printer_data/config, where most of your customizations and macros reside
 * The local klipper_backup directory and files
 * The script `reset_cr6_mcu_comms.sh`, which restarts klipper when the printer is powered-on

#### Ensure That All Script Files are Executable

Use SSH to issue the following two commands to the upgraded Host:

1. Ensure that the line endings in the .sh files are all CR and not CRLF.

```bash
sed -i 's/\r$//' ~/printer_data/config/scripts/*.sh
sed -i 's/\r$//' /usr/local/*.sh
```
This strips the Windows carriage return (\r) at the end of every line in every .sh file in each of the two directories.

2. Ensure that all of the .sh files are executable on this Linux host

```bash
chmod +x ~/printer_data/config/scripts/*.sh
chmod +x  /usr/local/*.sh
```
This sets the executable bit on every script in the two directories.

#### Use the restore_klipper.sh Script to Restore the local Klipper repo

```bash
bash ~/printer_data/config/scripts/restore_klipper.sh
```
Choose the most recent archive, which you made at step 1. 
   TIP: Only copy the most recent tar.gz and commit file to the new host at this step, based on timestamps in the file manager, to avoid any ambiguity as to which archive you want restored.

This should completely restore the local klipper git repository to your system.
Later, we will use Moonraker and Mainsail to confirm that Klipper has been fully restored (or to repair any issues with that repository that Moonraker flags.)

#### Re-install Stable_Z_Home
Follow step 5 in the 1-Installation_Manual.md.

#### Re-Install KIAUH and gcode_shell_command
Some of the macros in DGUS-Reloaded rely on the gcode_shell_command.py.  You can either comment-out those macros or perform this installation.
KIAUH is a useful utility to be aware of, and is the easiest way to install gcode_shell_command.py, so this is a good time to install/restore it to your Klipper host.

To install KIAUH, first install git on your Linux device with 
```bash
sudo apt-get update && sudo apt-get install git -y
```
Then clone the script with 
```bash
cd ~ && git clone https://github.com/dw-0/kiauh.git
```
After that, start KIAUH by running 
```bash
cd ~
./kiauh/kiauh.sh
```
, which opens an interactive menu to install and manage Klipper and related tools.

Navigate to (E)xtensions and select 1) G-Code Shell Command.

   TIP: Make note of the other things that KIAUH allows you to install.  Add anything else that you would like, either now or later.

#### Re-Create the .service and .rules files

The .service and .rules files cannot just be copied from 6-Pi-side_scripts, they must be created.
The process in each case is the same:
 * SSH into the host
 * Open the file in 6-Pi-side_scripts and copy the contents
 * Use nano to create the new file with the same name and path on the host.
 * Copy the contents of the file in 6-Pi-side_scripts.
 * Paste those contents into the nano editor.
 * Ctrl-O in nano and press return, to write the file to the host.
 * Ctrl-X in nano, to close the editor

Example:
1. Open 6-Pi-side_scripts/etc/systemd/system/pushover_pause_monitor.service
2. Create the file on the host
```bash
nano /etc/systemd/system/pushover_pause_monitor.service
```
3. Copy the contents of 6-Pi-side_scripts/etc/systemd/system/pushover_pause_monitor.service
4. Paste those contents into the nano editor
5. Ctrl-O in nano and press return, to write the file to the host.
6. Ctrl-X in nano, to close the editor

Repeat steps 1-6 for each of:
 * 6-Pi-side_scripts/etc/systemd/system/reset_cr6_mcu_comms.service
 * 6-Pi-side_scripts/etc/udev/rules.d/99-reset_cr6_mcu_comms.rules  (NB: Be sure to use the version of the rules that correspond to your printer's motherboard.)


#### ⭐ Restart Required Services
After restoring the above files, via SSH on the new host:

Restart these two services:

```bash
sudo systemctl restart moonraker
sudo systemctl restart klipper
```

Enable services to ensure they start automatically:

```bash
sudo systemctl enable moonraker
sudo systemctl enable klipper
```

#### ⭐ Verify the restore
From your laptop:

 * Open Mainsail:
    http://<new-ip>
    or
    http://mainsailos.local
 * Navigate to the MACHINE tab
   * In the Update Manager window: 
     * Confirm that all of the managed components are reported to be "Up to Date"
     * Select the small blue circular arrow icon to refresh Moonraker's assessment
     * If Moonraker shows any of those components to be Incomplete, select that button and perform a Hard Reset.  Confirm that Moonraker then shows the component to be Up to Date.
     * If Moonraker shows that any of the components is Out of Date, select those buttons to update those components.
   * In the System Loads window:
     * Confirm that no problems are being reported.
       * Troubleshoot and resolve any problems shown.
       * TIP: The `mcu` box refers to the motherboard and the `Host` box refers to the Klipper host.  
   * Confirm that there are no notifications being reported (bell icon at top right of page)
      * Troubleshoot and resolve any problems shown.

---

### 🧩 Step 5 — Post‑Restore Validation (Confirm Everything Works Before Printing)
NB: Perform these checks immediately after completing Step 4.  
Your system now contains your restored Klipper, Moonraker, Mainsail, scripts, and configuration files.
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
