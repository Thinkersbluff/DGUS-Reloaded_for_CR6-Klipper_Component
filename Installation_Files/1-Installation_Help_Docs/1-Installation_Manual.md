# Manual Installation Guide: DGUS-Reloaded for CR6 Printers on Klipper

> **Acknowledgement:** The structure of this guide is inspired by the excellent [KoenVanduffel/CR-6_Klipper README](https://github.com/KoenVanduffel/CR-6_Klipper), which covers the general process of installiing Klipper onto CR6 printers, clearly and concisely.
> This guide extends that process with the additional steps required to install the DGUS-Reloaded for CR6 'Add-on', to restore touchscreen functionality to the stock Creality CR6 display.
"

## Scope

This document walks you through the process of installing the full DGUS-Reloaded for CR6 system (including the display component) step-by-step, requiring that you manually perform each discrete task.

>**NOTE: If you already have a full system installed, and you want instead to update that system with a new release, close this document and refer to [4-Updating_Existing_Installation.md](4-Updating_Existing_Installation.md).**

---
## Before You Begin

### What You Will Need

- A Raspberry Pi (3b+ or 4b+, min 2 GB RAM recommended) as your Klipper host
- A Creality CR6 printer with one of these motherboards:
  - **Creality 4.5.2**
  - **Creality 4.5.3**
  - **Creality 1.1.0.3 ERA**
  - **BTT SKR CR6 V1.0**
- A Windows or Mac PC with internet access for downloading files
- Two microSD cards: one for the Pi (≥8 GB), one for flashing your printer (any size)
- A USB cable to connect the Pi to the printer
- An SSH client (e.g. [PuTTY](https://www.putty.org/)) and an SFTP client (e.g. [FileZilla](https://filezilla-project.org/))
  or a tool that combines both functions (e.g. [WinSCP](https://winscp.net/) or [MobaXterm](https://mobaxterm.mobatek.net/))

### Overview of the Full Process

| Phase | What you will do |
|---|---|
| 1 | Install Klipper + Mainsail (or Fluidd) on the Raspberry Pi |
| 2 | Download the DGUS-Reloaded release package to your PC |
| 3 | Flash the DWIN_SET firmware to the CR6 touchscreen display |
| 4 | Install the DGUS-Reloaded t5uid1 Klipper extras onto the Pi |
| 5 | Install the `stable_z_home` add-on onto the Pi |
| 6 | Flash the Klipper firmware binary to your CR6 motherboard |
| 7 | Copy and configure the Klipper host config files |
| 8 | Find and set the MCU serial interface ID in `printer.cfg` |
| 9 | Restart Klipper and verify |
| 10 | Post-install calibrations |
| 11 | (Optional) Configure your slicer |

---

## Step 1: Install Klipper and Mainsail (or Fluidd) on Your Raspberry Pi

> **What is Klipper?**  
> Klipper is a 3D printer firmware system that splits the work between a host computer (your Raspberry Pi) and the printer motherboard. The Pi runs the intelligence, the motherboard runs the motors and heaters.  
> Klipper requires a web front-end (Mainsail or Fluidd) and a communication broker (Moonraker). These are all installed together, as a package in this step.


### 1a. Download and install the Raspberry Pi Imager

Download the appropriate version for your PC from:
[https://www.raspberrypi.com/software/](https://www.raspberrypi.com/software/)

### 1b. Flash MainsailOS (recommended) or FluiddPI to the Pi's microSD card

- **Mainsail (recommended):** Follow the instructions at
  [https://docs-os.mainsail.xyz/](https://docs-os.mainsail.xyz/).
  MainsailOS can be installed directly through the Raspberry Pi Imager:
  click **Choose OS → Other specific-purpose OS → 3D printing → Mainsail OS**.

- **Fluidd:** Download a release image from
  [https://github.com/cadriel/FluiddPI/releases/](https://github.com/cadriel/FluiddPI/releases/).
  In the Imager, click **Choose OS → Use Custom** and select the downloaded image.

- **KIAUH (alternative, also useful for non-Pi hosts):** Follow the instructions at
  [https://github.com/th33xitus/kiauh](https://github.com/th33xitus/kiauh).

In the Raspberry Pi Imager's **settings gear** (bottom-right corner, v1.7.1 and later)
you can pre-configure:

- Hostname (e.g. `mainsailpi`)
- SSH enabled
- Username and password (default is `pi` / `raspberry` — **change the password**)
- Wi-Fi SSID and password

### 1c. Boot the Pi and verify SSH access

Insert the flashed microSD into the Pi, connect it to your network, and power it on.
Wait about 90 seconds, then connect via your SSH tool.


If this is the first boot and you did not pre-configure credentials via the Imager,
run the following first to set a new password:

```bash
sudo raspi-config
# Option 1 → S3: Change user password
sudo reboot
```

### 1d. Verify the Mainsail (or Fluidd) web interface

Once the Pi has rebooted, open a browser and navigate to `http://<pi-hostname-or-ip>`.
You should see the Mainsail or Fluidd interface.

---

## Step 2: Download the DGUS-Reloaded Release Package

1. Navigate to the **Releases** section of the DGUS-Reloaded Klipper repository:
   [https://github.com/Thinkersbluff/DGUS-Reloaded_for_CR6-Klipper_Component/releases](https://github.com/Thinkersbluff/DGUS-Reloaded_for_CR6-Klipper_Component/releases)

2. Download the **Source.zip** file for the latest release to a convenient location on
   your PC.

3. Extract the zip archive.

   > **NOTE:** The top-level folder name inside the zip can be very long (e.g.
   > `DGUS-Reloaded_for_CR6-Klipper_Component-2.0.0`). If your extraction fails due to path length,  shorten the top-level folder name first (e.g. to `DGUS-Reloaded`) before extracting.

You will refer to the contents of this extracted folder throughout the remaining steps.

---

## Step 3: Flash the DWIN_SET Firmware to Your CR6 Display

The CR6 stock touchscreen requires its own companion firmware (DWIN_SET) to
communicate with DGUS-Reloaded. This is a separate step from flashing the Klipper
motherboard firmware.

1. Navigate to the companion display firmware repository:
   [https://github.com/Thinkersbluff/DGUS-Reloaded_for_CR6-DWIN-SET_Component](https://github.com/Thinkersbluff/DGUS-Reloaded_for_CR6-DWIN-SET_Component)

2. Download the latest release and follow the flashing instructions provided there.
   The general procedure is:
   - Create a Master Boot Record (MBR) partition on a microSD card [Ensure that it is the first active partition on the card, and that it is less than 15Gb in size] 
   - Format the partition as FAT32, with an allocation unit size of 4096 bytes.
   - Copy the `DWIN_SET` folder to the **root** of the SD card in that MBR partition
   - Power off the printer
   - Remove the display bezel on the back of the CR6 screen; insert the microSD into the SD card slot on the display PCB
   - Power on the printer — the display will flash automatically (the screen turns blue during flashing) wait for the display to show END!
   - Power off, remove the microSD, and reattach the bezel

3. Power the printer back on to confirm the new display UI is running.
   Expect the display to show the splash screen, but it will not switch to the main menu until the motherboard firmware has also been flashed at step 6d.

---

## Step 4: Install the DGUS-Reloaded t5uid1 Klipper Extras

The `t5uid1` folder is the Python host-side component that enables Klipper to communicate with the DGUS-Reloaded display firmware.

### 4a. Transfer the files to the Pi

Using your SFTP client, connect to the Pi and upload the entire `t5uid1` folder and its contents, from the extracted release package onto the Pi.

```
Source (on your PC):
  <extracted release folder 't5uid1' in >/klippy/extras/

Destination (on the Pi):
Upload that 't5uid1' folder into
  ~/klipper/klippy/extras/
```

### 4b. Verify the copy

From an SSH session on the Pi, confirm the transferred files are present, by copy/pasting this script into your SSH window:

```bash
ls ~/klipper/klippy/extras/t5uid1/
```
Verify that the resulting list of files and folders on the Pi matches the contents of Installation_Files/2-DGUS-Reloaded_add-on/t5uid1/

---

## Step 5: Install the `stable_z_home` Add-On

`stable_z_home` is **required** by the DGUS-Reloaded START_PRINT macro.  Any filament contamination of the CR6 nozzle probe introduces an error into the Z=0.0 measurement.  More than any other factor, this error compromises the first layer quality by adding a bias to the Z Offset.

`stable_z_home` improves the accuracy and consistency of Z homing with the stock CR6 strain gauge probe, by enforcing a user-specified min-max range before computing the Z=0.0 height from an average of multiple measurements. If the probe min-max range exceeds the threshold, on the first pass, `stable_z_home` will try again, for a user-specified maximum number of tries, eventually aborting the print altogether, if the specified range is not achieved. 
[A typical achievable min-max range is 0.015mm.]

From an SSH session on the Pi:

### 5a. Clone the `stable_z_home` repository

```bash
cd ~
git clone https://github.com/matthewlloyd/Klipper-Stable-Z-Home.git
```

### 5b. Create a symlink in the Klipper extras directory

```bash
cd ~/klipper/klippy/extras
ln -s ~/Klipper-Stable-Z-Home/stable_z_home.py
```
NB: Linux file and folder names are case-sensitive. 

### 5c. Verify

```bash
ls -la ~/klipper/klippy/extras/stable_z_home.py
```

The entry should show an arrow (`->`) pointing to
`/home/pi/Klipper-Stable-Z-Home/stable_z_home.py`, confirming the symlink was created correctly.

> **Visual reference:** The following diagram from the repository README illustrates where the clone and the symlink should be located (assuming your username is `pi`):  
> ![Where to symlink stable_z_home.py](https://github.com/user-attachments/assets/d1991eb1-282e-47b8-b07d-51289273f077)

---

## Step 6: Flash the Klipper Firmware Binary to Your Motherboard

Klipper requires a small firmware binary to be flashed to your CR6 motherboard.  This binary handles the low-level printer hardware under direction from the Pi.  It also handles communications between the DGUS display firmware and Klipper, via the t5uid1 firmware.

### 6a. Locate the pre-built firmware binary

In the extracted release package, navigate to the subfolder for your motherboard:

| Your motherboard | Folder path (relative to extracted root) |
|---|---|
| Creality 4.5.2 | `4-klipper.bin_files/Creality CR6 Mobo [all]/` |
| Creality 4.5.3 or ERA 1.1.0.3 | `4-klipper.bin_files/Creality CR6 Mobo [all]/` |
| BTT SKR CR6 V1.0 | `4-klipper.bin_files/BTT SKR CR6 Only/` |

Inside that folder you will find a `.bin` file already built and named appropriately for flashing to your motherboard.

> **Why use the pre-built binary?**  
> The DGUS-Reloaded display protocol requires specific MCU firmware that includes the
> T5UID1 serial interface support. This support is not present in standard upstream
> Klipper. The pre-built `.bin` files in this release incorporate those modifications
> and have been tested to work together with the DGUS-Reloaded display firmware.
> Using `make menuconfig` and `make` per the standard Klipper installation instructions will **not** produce a compatible binary unless the DGUS-Reloaded `make_menu_Extensions` have first been applied. (See Installation Help document '3-Rebuilding_MCU_Firmware.md` for guidance on that approach.)

### 6b. Prepare the SD card

Format a microSD card as **FAT32 with allocation unit size of 4096 bytes.**
Any other format will prevent the motherboard from reading the SD card.

> A micro-SD card in a full-size SD adapter works fine, provided the formatting
> is correct.

### 6c. Copy and rename the binary

| Motherboard | Required filename on SD card |
|---|---|
| Creality 4.5.2, 4.5.3, ERA 1.1.0.3 | Any `.bin` filename — but it **must not** match the filename used at the last flash (e.g. rename to `klipper_new.bin`) |
| BTT SKR CR6 V1.0 | Exactly `firmware.bin` — the BTT bootloader requires this name |

### 6d. Flash the board

1. Power off the printer.
2. Insert the prepared SD card into the printer's motherboard SD slot.
3. Power on the printer. The board will flash automatically (approximately 10 seconds). The BTT motherboard will also flicker the nozzle LED while flashing the firmware.
4. Power off the printer and **remove the SD card** before the next power cycle.  

NOTES:
1. The BTT motherboard will rename the firmware.bin file FIRMWARE.CUR.
2. The Creality motherboards will not rename the bin file but will ignore that filename on subsequent power cycles.  That is why you need to rename the Creality klipper.bin file, each time you try again to flash it to the Creality boards.

---

## Step 7: Copy and Configure the Klipper Host Config Files

Klipper, Moonraker, and Mainsail (or Fluidd) each require configuration files.
The DGUS-Reloaded release package includes a set of pre-configured files for each supported motherboard.

### 7a. Locate the config files for your board

In the extracted release package:

| Your motherboard | Source folder |
|---|---|
| Creality 4.5.2 | `3-Custom_Klipper+Mainsail_Files\Creality CR6 Mobo\4.5.2 MB/` |
| Creality 4.5.3 or ERA 1.1.0.3 | `3-Custom_Klipper+Mainsail_Files\Creality CR6 Mobo\ERA 1.1.0.3 or 4.5.3 MB/` |
| BTT SKR CR6 V1.0 | `3-Custom_Klipper+Mainsail_Files\BTT SKR CR6 Only` |

Read the `README.txt` file inside that folder first — it explains the purpose of each file and notes any changes made in the latest release.

### 7b. Upload the config files to the Pi

The Klipper configuration files live at **`~/printer_data/config/`** on the Pi.

**Option A — Via the Mainsail/Fluidd web interface (easiest):**
Open the web interface in your browser, navigate to the **Machine** tab, and use the upload function to upload each file directly to `~/printer_data/config/`.

**Option B — Via SFTP:**
Use your SFTP client to copy the files directly to `~/printer_data/config/` on the Pi.

The files to copy are:

```
CR6.cfg
DGUS-Reloaded.cfg
DGUS_Menu_Macros.cfg
Dev_Macros.cfg
inputShaper.cfg
microprobe.cfg   (or stockprobe.cfg, depending on your probe — see notes below)
printer.cfg
```

> **WARNING: If you already have a working system:**  
> Do **not** overwrite these printer_data/config files blindly. Use a comparison tool such as
> [WinMerge](https://winmerge.org/downloads/?lang=en) to compare the new files with your existing ones and selectively transfer only the DGUS-Reloaded-specific additions.

### 7c. Critical customisations required in `printer.cfg`

Open `printer.cfg` in a text editor and review **every section carefully**.
Several settings must be tailored to your specific printer before you attempt to print.

Key items to check and adjust:

- **`[mcu]` serial:** Leave the placeholder for now — you will set this in Step 8.
- **Stepper motor currents and steps-per-mm:** These reflect the developer's specific hardware (direct-drive Orbiter extruder, etc.) and will likely not all match your printer, as-is.
- **`[extruder]` settings:** `rotation_distance`, `nozzle_diameter`, PID values,
  `pressure_advance`.
- **`[heater_bed]` PID values:** Will need re-tuning for your bed.
- **`[input_shaper]`:** The resonance frequency values are machine-specific and should
  be measured, not copied.
- **`[include timelapse.cfg]`:** If you do not have `moonraker-timelapse` installed,
  comment this line out (add `#` at the start).
- **`[include Dev_Macros.cfg]`:** Contains developer diagnostic macros not needed for
  normal printing. You may comment this out if you wish.
- **Fluidd users:** In `printer.cfg`, locate the line `[include mainsail.cfg]` and
  change it to `[include fluidd.cfg]`.

### 7d. Notes on probe configuration

- **`stockprobe.cfg`** is configured for the stock CR6 strain gauge levelling probe.  Use this file if you have the stock probe.
- **`microprobe.cfg`** is an alternative probe configuration for the BTT microprobe, if you have converted the printer from strain gauge to microprobe. Check the `README.txt` in your board's config folder to understand which file applies to your setup.
- If you have replaced your probe with a BLTouch or other type, you will need a configuration file appropriate for that probe and should not use either `stockprobe.cfg` or `microprobe.cfg`, as-is.

---

## Step 8: Find and Set the MCU Serial Interface ID in `printer.cfg`

Klipper needs to know the USB path that the Pi uses to communicate with your motherboard.

### 8a. Connect the Pi to the printer via USB

Make sure the Pi and printer are connected with a USB cable, and that the printer is powered on.

### 8b. Find the serial ID

From an SSH session on the Pi, run:

```bash
ls /dev/serial/by-id/*
```

The output will look something like this (your exact ID will differ):

```
/dev/serial/by-id/usb-Klipper_stm32f103xe_36FFD8054255373740662057-if00
```
Copy the full path string of the printer device.  

>**TIP:** If the ls command returns multiple device IDs, unplug the printer and re-run the command. Then plug it back in and re-run the command.  The string you need to copy is the one that disappears/reappears, when you unplug, replug the printer.

### 8c. Update `printer.cfg`

Open `printer.cfg` (via the Mainsail/Fluidd Machine tab, or via SSH + nano) and replace the placeholder value in the `[mcu]` section with the string you just copied:

```ini
[mcu]
serial: /dev/serial/by-id/usb-Klipper_stm32f103xe_36FFD8054255373740662057-if00
```

Save the file.

---

## Step 9: Restart Klipper and Verify

### 9a. Restart Klipper

From the Mainsail or Fluidd web interface, click the **Restart Firmware** button (or **Host Restart** followed by **Firmware Restart**).

Alternatively, from an SSH session:

```bash
sudo systemctl restart klipper
```

### 9b. Verify Klipper is ready

In the Mainsail or Fluidd web interface, watch the console. Within a few seconds you should see Klipper report `MCU` connection followed by a `Klipper state: Ready` message.

If you see error messages instead, the most common causes are:

- **Incorrect serial ID:** Re-run Step 8b and verify the string in `printer.cfg` matches exactly.
- **Config file errors:** Read the error message carefully — Klipper will report the filename and line number of any configuration problem.
- **Missing extras:** Confirm the `t5uid1` and `stable_z_home` files are in `~/klipper/klippy/extras/` (Steps 4–5).

For a full configuration verification checklist, follow the Klipper documentation here:  
[https://www.klipper3d.org/Config_checks.html](https://www.klipper3d.org/Config_checks.html)

> **Note — MCU comms lost after printer power-cycle:**  CR6 printers lose USB communications with the MCU each time the printer is switched off and back on. This leaves the DWIN_SET stuck on the boot screen, until you RESET or FIRMWARE_RESET, using Mainsail or KlipperScreen. If you want the DWIN_SET to boot through to the Home menu when you power-up your printer, then see [Appendix E: Automatic MCU Communications Recovery](appendix/E-Pi-Side_Recovery_Setup.md) for a simple three-file fix you can install on your Pi.

### 9c. Verify the display

With Klipper reporting Ready and your printer powered on, the CR6 touchscreen should now show the DGUS-Reloaded home screen. If the display is still showing the old Creality or a blank/corrupt screen, re-check that the DWIN_SET was flashed correctly (Step 3).

---
## Step 10: Post-Install Calibrations

**Do not attempt to print anything until you have completed the following calibrations.**
The config files contain the developer's calibration values, which will be wrong for your printer.

Perform these steps in order:

1. **PID-tune the hotend:**  
   From the DGUS-Reloaded **Calibrate** menu on the touchscreen, or from the
   Mainsail/Fluidd console:
   ```
   PID_CALIBRATE HEATER=extruder TARGET=200
   ```
   Then save: `SAVE_CONFIG`

2. **PID-tune the heated bed:**
   ```
   PID_CALIBRATE HEATER=heater_bed TARGET=60
   ```
   Then save: `SAVE_CONFIG`

3. **Set the Z-offset (nozzle-to-bed distance):**  
   From the Mainsail/Fluidd console:
   ```
   PROBE_CALIBRATE
   ```
   Follow the paper-test procedure described in the Klipper documentation:  
   [https://www.klipper3d.org/Bed_Level.html](https://www.klipper3d.org/Bed_Level.html)  
   Then save: `SAVE_CONFIG`

4. **Run the automatic bed levelling (ABL) routines:**  
   The DGUS-Reloaded macros include pre-defined ABL routines. Run them from the
   Mainsail console or from the display Calibrate menu:
   ```
   RUN_ABL_COLD
   RUN_ABL_BED_60
   RUN_ABL_BED_80
   ```
   Save after each, if they complete without error: `SAVE_CONFIG`

5. **Verify end-stops and motion:**  
   Follow the Klipper configuration checks guide to confirm all axes home correctly,
   end-stops trigger at the right positions, and the extruder moves in the correct
   direction:  
   [https://www.klipper3d.org/Config_checks.html](https://www.klipper3d.org/Config_checks.html)

### Step 10e: (Optional) Explore Available Test Macros

The system includes several test and utility macros to help you validate and maintain your printer. These are particularly useful after initial setup:

- **Travel tests** validate belt tension on X and Y axes by running rapid motion cycles
  - Available on all motherboards: `X_TRAVEL_TEST` and `Y_TRAVEL_TEST`
  - With TMC diagnostics (BTT SKR boards only): `X_TRAVEL_TEST_WITH_TMC` and `Y_TRAVEL_TEST_WITH_TMC`
  - For detailed information: [3-Common Maintenance Tasks § Validate Belt Tension](3-Common_Maintenance_Tasks.md#task-7-validate-and-adjust-belt-tension-using-travel-tests)

- **Calibration and utility macros** are pre-defined for common tasks (ABL at various bed temps, filament load/unload, LED control, etc.)

- You can add any of these macros to your DGUS custom menus via `DGUS_Menu_Macros.cfg`
  - For guidance: [2-Understanding Your System § Custom Macro Menus](2-Understanding_Your_System.md#custom-macro-menus-via-dgus_menu_macroscfg)

---
## Step 11 (Optional): Configure Your Slicer

The DGUS-Reloaded display relies on specific gcode commands from your slicer to show
print progress and time remaining:

- **`M73 P<percent>`** — sends print percentage to the display
- **`M73 R<minutes>`** — sends estimated time remaining to the display
- **`M117 <message>`** — sends a status text line to the display

Configure your slicer's start gcode to call the `START_PRINT` macro:

```
START_PRINT EXTRUDER_TEMP={material_print_temperature_layer_0} BED_TEMP={material_bed_temperature_layer_0}
```

And the end gcode to call `END_PRINT`:

```
END_PRINT
```

### Ultimaker Cura

At Cura 5.7.0 and later, use the **Display Info on LCD** plug-in.
Recommended settings for progress and time reporting are documented in the
[main repository README](https://github.com/Thinkersbluff/DGUS-Reloaded_for_CR6-Klipper_Component).

### OrcaSlicer

OrcaSlicer sends `M73 R..` and `M73 P..` messages by default. Ensure the option
**"Disable set remaining print time"** is **not** checked in your printer profile.

### Other slicers

Any slicer that can be configured to emit `M73 P` and `M73 R` messages will work.
Consult your slicer's documentation for how to enable these.

---

## Troubleshooting Reference

| Symptom | Likely Cause | Resolution |
|---|---|---|
| Klipper shows `Unable to connect` | Firmware not flashed, or wrong serial ID | Re-do Steps 6 and 8 |
| Display shows old Creality UI or blank screen | DWIN_SET not flashed or flash failed | Re-do Step 3 |
| Klipper error: `Unknown pin chip name 't5uid1'` | t5uid1 extras not installed | Re-do Step 4 |
| Klipper error: `Module 'stable_z_home' not found` | stable_z_home symlink missing | Re-do Step 5 |
| Display shows Ready screen but print crashes immediately | Config values not tailored to your hardware | Review Step 7c |
| `timelapse.cfg` error on startup | moonraker-timelapse not installed | Comment out `[include timelapse.cfg]` in printer.cfg |
| Klipper loses MCU connection every time the printer is power-cycled | USB re-enumeration timing issue between Pi and MCU | See [Appendix E: Automatic MCU Communications Recovery](appendix/E-Pi-Side_Recovery_Setup.md) |

---

## Further Reading

- **Klipper documentation:** [https://www.klipper3d.org/](https://www.klipper3d.org/)
- **DGUS-Reloaded display firmware repo:**
  [https://github.com/Thinkersbluff/DGUS-reloadedForKlipper_CR6](https://github.com/Thinkersbluff/DGUS-reloadedForKlipper_CR6)
- **Klipper-Stable-Z-Home:**
  [https://github.com/matthewlloyd/Klipper-Stable-Z-Home](https://github.com/matthewlloyd/Klipper-Stable-Z-Home)
- **Desuuuu DGUS-Reloaded Klipper wiki (original project):**
  [https://github.com/Desuuuu/DGUS-reloaded-Klipper/wiki](https://github.com/Desuuuu/DGUS-reloaded-Klipper/wiki)
- **KoenVanduffel general Klipper-on-CR6 README:**
  [https://github.com/KoenVanduffel/CR-6_Klipper](https://github.com/KoenVanduffel/CR-6_Klipper)
