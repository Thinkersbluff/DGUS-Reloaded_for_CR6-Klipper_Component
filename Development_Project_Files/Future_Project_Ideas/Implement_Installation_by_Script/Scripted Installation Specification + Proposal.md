# Installation Script — Draft Proposal
*Last updated: 2026-02-20*

---

## Specification

The current repo is my development environment. It presently contains more elements than a user is going to need.  Users must presently read and follow a rather lengthy and complicated Readme file, to install the system on their printer.  

I think I could make it much easier for users to "upgrade" an existing installation of the latest Klipper, to download and install the full dgus_reloaded system as if it were a Klipper "add-on" application. 

Propose a Bash script-based approach, to:

1. Clone the applicable part(s) of this repository into the user's home directory
2. Copy the t5uid1 folder and contents into the user's ~/klipper/klippy/extras directory
3. Copy the src/stm32/t5uid1 folder and contents to the user's ~/klipper/src folder
4. Copy the src/generic/t5uid1 folder and contents to the user's ~/klipper/src folder
5. Patch the Makefile and KConfig files to include those new src/<board>/t5uid1 folders
6. Install the stable_z_home "add-on" on the user's system
7. Install the gcode_shell_command macro on the user's system
8. Verify that the installation has completed successfully (or handle failures with grace)
9. Prompt the user to run make menuconfig to generate klipper.bin for their particular motherboard. (Supporting only these four motherboards compatible with and marketed for the stock Creality CR6 printers:
- Creality 4.5.2
- Creality 4.5.3
- Creality 1.1.0.3 ERA
- BTT SKR CR6 V1.0)

## Assumptions and prerequisites

- Target OS: Raspberry Pi OS (Debian-based), running a standard KIAUH-style Klipper
  installation at `~/klipper`
- User has SSH access (PuTTY) and can paste into a terminal
- Klipper is already installed but **not yet running DGUS-Reloaded**
- Script language: **Bash** (runs directly in the SSH session)

---

## Structure: Two scripts

A single monolithic script would be too fragile — one failure mid-run could leave an unknown partial state. 

The recommended approach is to use **two scripts**:

| Script | Role |
|---|---|
| `install_dgus.sh` | Steps 1–8: installs all files, patches sources, installs add-ons, verifies |
| `build_firmware.sh` | Step 9: interactive board selection + `make menuconfig` guidance + `make` |

The user copy-pastes one command to run `install_dgus.sh`. Only after it reports success do they run `build_firmware.sh`.

---

## Important note on `make menuconfig`

The **current repo's README** explicitly states that `make menuconfig` is **not
supported** with the fork — pre-built `.bin` files are provided instead. However,
that restriction exists because the forked MCU code was never integrated into
upstream. The entire *purpose* of the `5-make_menuconfig_Extensions` patch set is to fix that.
After `install_dgus.sh` applies the patches to upstream, `make menuconfig` **will**
work again. `build_firmware.sh` is therefore legitimate — but the README needs
updating to clarify this.

---

## `install_dgus.sh` — step-by-step design

### Step 0 — Preflight checks

- Verify `~/klipper` exists and contains `src/stm32/Makefile` (i.e., this is actually
  a Klipper installation)
- Verify `git`, `python3`, and `make` are available
- Stop the Klipper service before modifying files:
  ```bash
  sudo systemctl stop klipper
  ```
- Create a timestamped backup of `~/klipper/src/stm32/Kconfig` and
  `~/klipper/src/stm32/Makefile` before patching

### Step 1 — Clone only the needed parts of this repo

Use `git sparse-checkout` to avoid pulling the entire repo (it is large due to binary
`.bin` files and dev artifacts):

```bash
git clone --no-checkout --filter=blob:none \
  https://github.com/YourUser/DGUS-Reloaded_for_CR6-Klipper_Component.git \
  /tmp/dgus_install
cd /tmp/dgus_install
git sparse-checkout init --cone
git sparse-checkout set \
  Installation_Files/2-DGUS-Reloaded_Add-on/t5uid1 \
  Installation_Files/5-make_menuconfig_Extensions/klipper/src
git checkout
```

> **TODO before publishing:** Replace `YourUser` with the actual GitHub account/org
> where this repo is hosted publicly. Also decide whether to pull from this repo
> directly, or from a separate leaner "release" repo containing only the install assets.

### Step 2 — Copy `t5uid1/` host extras

```bash
cp -r /tmp/dgus_install/Installation_Files/2-DGUS-Reloaded_Add-on/t5uid1 \
  ~/klipper/klippy/extras/t5uid1
```

Then apply the `variables.cfg` path fix in `t5uid1.py` using `sed`, so it works
regardless of installation location (replacing the hardcoded `/home/pi/klipper/...`
path with a path relative to the module file itself):

```bash
sed -i \
  "s|'/home/pi/klipper/klippy/extras/t5uid1/dgus_reloaded/variables.cfg'|os.path.join(os.path.dirname(__file__), 'dgus_reloaded', 'variables.cfg')|g" \
  ~/klipper/klippy/extras/t5uid1/t5uid1.py
```

### Step 3 — Copy MCU source trees

```bash
cp -r /tmp/dgus_install/Installation_Files/5-make_menuconfig_Extensions/klipper/src/stm32/t5uid1   ~/klipper/src/stm32/t5uid1
cp -r /tmp/dgus_install/Installation_Files/5-make_menuconfig_Extensions/klipper/src/generic/t5uid1  ~/klipper/src/generic/t5uid1
```

### Step 4 — Patch `src/stm32/Kconfig`

The idempotency check prevents the line being added twice if the script is re-run:

```bash
if ! grep -q 'src/stm32/t5uid1/Kconfig' ~/klipper/src/stm32/Kconfig; then
  sed -i 's|^endif$|source "src/stm32/t5uid1/Kconfig"\n\nendif|' \
    ~/klipper/src/stm32/Kconfig
fi
```

### Step 5 — Patch `src/stm32/Makefile`

```bash
if ! grep -q 'src/stm32/t5uid1/Makefile' ~/klipper/src/stm32/Makefile; then
  echo "" >> ~/klipper/src/stm32/Makefile
  echo "include src/stm32/t5uid1/Makefile" >> ~/klipper/src/stm32/Makefile
fi
```

### Step 6 — Install `stable_z_home`

Single-file download from the upstream GitHub repo:

```bash
wget -q -O ~/klipper/klippy/extras/stable_z_home.py \
  https://raw.githubusercontent.com/matthewlloyd/Klipper-Stable-Z-Home/main/stable_z_home.py
```

### Step 7 — Install `gcode_shell_command`

Sourced from the KIAUH extension collection:

```bash
wget -q -O ~/klipper/klippy/extras/gcode_shell_command.py \
  https://raw.githubusercontent.com/dw-0/kiauh/master/resources/gcode_shell_command.py
```

### Step 8 — Verify installation

Check that every expected file is in place, and that the Kconfig/Makefile patches
were applied:

```bash
ERRORS=0
for f in \
  ~/klipper/klippy/extras/t5uid1/__init__.py \
  ~/klipper/klippy/extras/t5uid1/t5uid1.py \
  ~/klipper/klippy/extras/t5uid1/var.py \
  ~/klipper/klippy/extras/t5uid1/page.py \
  ~/klipper/klippy/extras/t5uid1/routine.py \
  ~/klipper/klippy/extras/t5uid1/dgus_reloaded/__init__.py \
  ~/klipper/klippy/extras/t5uid1/dgus_reloaded/vars_in.cfg \
  ~/klipper/klippy/extras/t5uid1/dgus_reloaded/vars_out.cfg \
  ~/klipper/klippy/extras/t5uid1/dgus_reloaded/routines.cfg \
  ~/klipper/klippy/extras/t5uid1/dgus_reloaded/pages.cfg \
  ~/klipper/src/stm32/t5uid1/serial.c \
  ~/klipper/src/stm32/t5uid1/stm32_serial.h \
  ~/klipper/src/stm32/t5uid1/Kconfig \
  ~/klipper/src/stm32/t5uid1/Makefile \
  ~/klipper/src/generic/t5uid1/serial_irq.c \
  ~/klipper/src/generic/t5uid1/serial_irq.h \
  ~/klipper/klippy/extras/stable_z_home.py \
  ~/klipper/klippy/extras/gcode_shell_command.py; do
  [ -f "$f" ] || { echo "MISSING: $f"; ERRORS=$((ERRORS+1)); }
done

grep -q 'src/stm32/t5uid1/Kconfig' ~/klipper/src/stm32/Kconfig \
  || { echo "MISSING PATCH: src/stm32/Kconfig"; ERRORS=$((ERRORS+1)); }
grep -q 'src/stm32/t5uid1/Makefile' ~/klipper/src/stm32/Makefile \
  || { echo "MISSING PATCH: src/stm32/Makefile"; ERRORS=$((ERRORS+1)); }

if [ $ERRORS -eq 0 ]; then
  echo "SUCCESS: All files verified. Restarting Klipper..."
  sudo systemctl start klipper
else
  echo "FAILED: $ERRORS item(s) missing or not patched correctly."
  echo "Fix the errors listed above before running build_firmware.sh."
  echo "Klipper has NOT been restarted."
fi
```

---

## `build_firmware.sh` — step-by-step design

### Interactive board selection menu

```
==========================================================
  DGUS-Reloaded Klipper Firmware Builder
==========================================================
Please select your motherboard:

  1) Creality 4.5.3
  2) Creality 1.1.0.3 ERA   (same menuconfig settings as 4.5.3)
  3) Creality 4.5.2
  4) BTT SKR CR6 V1.0

Enter 1-4:
```

### Menuconfig instructions printed per board

Since `make menuconfig` is an interactive ncurses UI it cannot be scripted directly.
The script prints exact navigation instructions, launches `make menuconfig`, then waits
for the user to confirm they are done.

**Creality 4.5.3 and ERA 1.1.0.3:**
```
In the menuconfig screen, set the following options:
  Micro-controller Architecture  →  STM32
  Processor model                →  STM32F103
  Bootloader offset              →  28KiB bootloader
  Communication interface        →  Serial (on USART1 PA10/PA9)
  Enable DGUS T5UID1 screen      →  [*] (press Space to select)
  Screen serial interface        →  USART3 (on PB11/PB10)

Save and exit (press Q, then Y to confirm).
```

**Creality 4.5.2:**
```
In the menuconfig screen, set the following options:
  Micro-controller Architecture  →  STM32
  Processor model                →  STM32F103
  Bootloader offset              →  28KiB bootloader
  Communication interface        →  Serial (on USART1 PA10/PA9)
  Enable DGUS T5UID1 screen      →  [*] (press Space to select)
  Screen serial interface        →  USART3 (on PB11/PB10)

Save and exit (press Q, then Y to confirm).
```

**BTT SKR CR6 V1.0:**
```
In the menuconfig screen, set the following options:
  Micro-controller Architecture          →  STM32
  Processor model                        →  STM32F103
  Bootloader offset                      →  28KiB bootloader
  Communication interface                →  USB (on PA11/PA12)
  Enable extra low-level config options  →  [*] (press Space to select)
  GPIO pins to set at micro-ctrl startup →  !PA14
  Enable DGUS T5UID1 screen             →  [*] (press Space to select)
  Screen serial interface                →  USART2 (on PA3/PA2)

Save and exit (press Q, then Y to confirm).
```

### After menuconfig: run `make`

```bash
cd ~/klipper
mkdir -p out/src/stm32/t5uid1 out/src/generic/t5uid1
make
```

The `mkdir -p` line pre-creates the output subdirectories for the T5UID1 source
files. Without it the compiler fails with:
`fatal error: opening dependency file out/src/stm32/t5uid1/serial.d: No such file or directory`

### Board-specific flash instructions printed after a successful `make`

**Creality 4.5.3, ERA 1.1.0.3, and 4.5.2:**
```
Firmware built successfully: ~/klipper/out/klipper.bin

To flash your Creality motherboard:
  1. Copy out/klipper.bin to a FAT32-formatted SD card.
  2. The filename MUST end in ".bin" and MUST NOT match the last filename
     that was flashed (e.g., rename it to klipper_new.bin if needed).
  3. Insert the SD card into the printer while it is OFF.
  4. Power on the printer. The board will flash automatically (takes ~30 sec).
  5. Remove the SD card before the next power cycle.
```

**BTT SKR CR6 V1.0:**
```
Firmware built successfully: ~/klipper/out/klipper.bin

To flash your BTT SKR CR6:
  1. Copy out/klipper.bin to a FAT32-formatted SD card.
  2. RENAME the file to exactly: firmware.bin
     (The SKR CR6 bootloader requires this exact filename.)
  3. Insert the SD card into the board while it is OFF.
  4. Power on the printer. The board will flash automatically (takes ~30 sec).
  5. Remove the SD card before the next power cycle.

Note: "make flash" does NOT work on the SKR CR6. Always use the SD card method.
```

---

## Open questions / TODOs before publishing

1. **Repo URL**: Replace the placeholder `YourUser/DGUS-Reloaded_for_CR6-Klipper_Component`
   in Step 1 with the real public repo address.

2. **Release repo vs. this repo**: Decide whether `install_dgus.sh` should sparse-clone
   this development repo, or whether a separate leaner "release" repo should be created
   containing only the install-time assets (avoids users pulling large binary `.bin` files
   and dev artifacts they do not need).

3. **`gcode_shell_command` source URL**: Confirm the KIAUH raw URL is still valid and
   points to a stable version. Consider vendoring the file into this repo instead.

4. **`stable_z_home` optionality**: Is `stable_z_home` required by all users, or only
   by those using the stock CR6 strain gauge probe? If optional, the script should ask.

5. **Klipper service name**: Most KIAUH installs use `klipper` as the systemd service
   name, but some use `klipper-1` (multi-instance). Consider detecting this automatically.

6. **`sed` path-fix verification**: After applying the `sed` patch to `t5uid1.py`, the
   verification step should confirm the hardcoded path string is no longer present and
   the `os.path.join` form is.

7. **Idempotency of Step 3 (cp)**: If the script is re-run after a partial failure,
   `cp -r` will overwrite existing files silently. This is probably fine but should be
   noted — or a backup step added.

8. **Creality 4.5.2 pin differences**: The `4.5.2` board shares the same menuconfig
   settings as `4.5.3`/ERA in the T5UID1 options, but has different stepper/heater pin
   assignments in `printer.cfg`. The build script does not address `printer.cfg` — the
   user must still use the correct host config file for their board variant.

---

## `deploy_config.sh` — step-by-step design

This third script copies the per-board Custom Klipper host configuration files from
the repo into the user's Klipper config directory, and handles the single UI-specific
difference between Mainsail and Fluidd.

### Source folders in this repo

| Board selection | Source folder (relative to repo root) |
|---|---|
| Creality 4.5.3 or ERA 1.1.0.3 | `Installation_Files/3-Custom_Klipper+Mainsail_Files/Creality CR6 Mobo/ERA 1.1.0.3 or 4.5.3 MB/` |
| Creality 4.5.2 | `Installation_Files/3-Custom_Klipper+Mainsail_Files/Creality CR6 Mobo/4.5.2 MB/` |
| BTT SKR CR6 V1.0 | `Installation_Files/3-Custom_Klipper+Mainsail_Files/BTT SKR CR6 Only/` |

### Files copied in all cases

```
CR6.cfg
Dev_Macros.cfg
DGUS-Reloaded.cfg
DGUS_Menu_Macros.cfg
inputShaper.cfg
microprobe.cfg
printer.cfg
stockprobe.cfg
```

`README.txt` is intentionally **not** copied — it is a developer/release note, not a
Klipper config file, and would clutter the user's config directory.

### Step 0 — Preflight checks

- Verify that `install_dgus.sh` has already run successfully by checking for
  `~/klipper/klippy/extras/t5uid1/__init__.py`
- Verify that `~/printer_data/config/` exists (standard KIAUH install path)
- Create the staging destination directory if it does not already exist:
  ```bash
  mkdir -p ~/t5uid1/printer_data/config
  ```
  No overwrite risk: this directory is separate from the live Klipper config directory
  and is solely a staging area for the user to review before applying files manually.
### Step 1 — Ask for motherboard selection

Reuse the same numbered menu as `build_firmware.sh`:

```
Please select your motherboard:
  1) Creality 4.5.3
  2) Creality 1.1.0.3 ERA   (same config files as 4.5.3)
  3) Creality 4.5.2
  4) BTT SKR CR6 V1.0
```

### Step 2 — Ask for UI selection

```
Which web interface are you using?
  1) Mainsail  (recommended)
  2) Fluidd
```

### Step 3 — Copy the config files

```bash
# Example for Creality ERA/4.5.3 selection:
SRC_DIR="$REPO_DIR/Installation_Files/3-Custom_Klipper+Mainsail_Files/Creality CR6 Mobo/ERA 1.1.0.3 or 4.5.3 MB"
DEST_DIR="$HOME/printer_data/config"
t5uid1/
for f in CR6.cfg Dev_Macros.cfg DGUS-Reloaded.cfg DGUS_Menu_Macros.cfg \
          inputShaper.cfg microprobe.cfg printer.cfg stockprobe.cfg; do
  cp "$SRC_DIR/$f" "$DEST_DIR/$f"
done
```

### Step 4 — Apply the UI patch to `printer.cfg`

Inspecting all three board sets confirms that `printer.cfg` in every board folder
contains exactly this line:

```
[include mainsail.cfg]
```

For **Mainsail** users: no change needed — the line is correct as-is.

For **Fluidd** users: replace it with `[include fluidd.cfg]` using `sed`:

```bash
if [ "$UI_CHOICE" = "fluidd" ]; then
  sed -i 's/\[include mainsail\.cfg\]/[include fluidd.cfg]/' \
    "$DEST_DIR/printer.cfg"
fi
```


> **Note on destination path:** `$DEST_DIR` is `~/t5uid1/printer_data/config/` — a
> staging directory, not the live Klipper config directory. The UI patch is applied
> here so the staged files are ready to copy as-is when the user decides to deploy them.
This is the **only** difference between a Mainsail and Fluidd deployment. No separate
set of Fluidd config files needs to be maintained in the repo.

> **Why this is the only difference:**
> Both Mainsail and Fluidd are installed by KIAUH, which automatically places a
> `mainsail.cfg` or `fluidd.cfg` file in `~/printer_data/config/`. That file contains
> the UI-specific macro definitions (e.g. `PAUSE`, `RESUME`, `CANCEL_PRINT`) that each
> front-end expects. Every other file in the config set is UI-agnostic.

### Step 5 — Verify

Confirm all expected files were copied:

```bash
ERRORS=0
for f in CR6.cfg Dev_Macros.cfg DGUS-Reloaded.cfg DGUS_Menu_Macros.cfg \
          inputShaper.cfg microprobe.cfg printer.cfg stockprobe.cfg; do
  [ -f "$DEST_DIR/$f" ] || { echo "MISSING: $DEST_DIR/$f"; ERRORS=$((ERRORS+1)); }
done

if [ $ERRORS -eq 0 ]; then
  echo "SUCCESS: All config files deployed to $DEST_DIR"
elsestag
  echo "FAILED: $ERRORS file(s) missing. Check errors above."
fi
```

If Fluidd was selected, additionally verify the substitution was applied:

```bash
if [ "$UI_CHOICE" = "fluidd" ]; then
  grep -q '\[include fluidd\.cfg\]' "$DEST_DIR/printer.cfg" \
    && echo "Fluidd patch confirmed." \
    || echo "WARNING: Fluidd patch may not have applied correctly. Check printer.cfg manually."
fi
```

### Step 6 — Post-install instructions printed to user

```
=========================================================
  Config files deployed. IMPORTANT next steps:
===============staged. IMPORTANT next steps:
=========================================================

Your board-specific config files have been placed in:

    ~/t5uid1/printer_data/config/

They have NOT been copied to your live Klipper config directory yet.
Review and tailor them BEFORE copying them across.

1. Read the comments in each file carefully — especially printer.cfg.
   Several settings MUST be tailored to your specific printer before
   you attempt to print anything.

2. Use a comparison tool (e.g. WinMerge via SFTP, or 'diff' on the Pi)
   to compare the staged files with any existing files in:

    ~/printer_data/config/

   Copy across only the files (or parts of files) that you need.

3. microprobe.cfg is configured for the stock CR6 strain gauge probe.
   If you have replaced your probe (e.g. with a BTT MicroProbe or BLTouch),
   you will need to edit microprobe.cfg or replace it with a config
   appropriate for your probe type.

4. printer.cfg includes [include timelapse.cfg]. If you do not have
   moonraker-timelapse installed, comment that line out before deploying.

5. Dev_Macros.cfg contains developer diagnostic macros not needed for
   normal printing. You may comment out [include Dev_Macros.cfg] in
   printer.cfg if you wish.

6. Once your config files are in ~/printer_data/config/ and tailored,
   restart Klipper:
     sudo systemctl restart klipper

7. Then perform the following calibrations before your first print:
     - PID tune the hot end and bed (from the DGUS Calibrate menu)
     - Set your Z-offset (Mainsail/Fluidd console: PROBE_CALIBRATE)
     - Run RUN_ABL_COLD
     - Run RUN_ABL_BED_60
     - Run RUN_ABL_BED_80======================
```

---

## Open questions / TODOs specific to `deploy_config.sh`

9. **Overwrite protection**: If the user already has a working `printer.cfg`, blindly
   overwriting it would be destructive — RESOLVED**: Files are staged to `~/t5uid1/printer_data/config/`
   rather than deployed directly to `~/printer_data/config/`. This is safe for both
   new installs and upgrades: the user reviews and manually copies only what they need.
   No overwrite prompt or new-vs-upgrade detection is required in the script.

10. **Further scripted deployment**: The question of whether to add a fourth script that
    assists the user in copying/merging the staged files into the live config directory
    is deferred. For now, the post-install message directs the user to do this manually,
    using a comparison tool such as WinMerge.
11. **`moonraker.conf` not included**: The config file sets do not include
    `moonraker.conf`. This is correct — Moonraker's own installer (via KIAUH) creates
    it, and it contains UI-specific entries (`[update_manager mainsail]` vs.
    `[update_manager fluidd]`) that are already set correctly by the UI installer.
    The script does not need to touch it. However, the post-install message should
    remind the user that `moonraker.conf` may need manual review if they are migrating
    from a different UI.

12. **`timelapse.cfg`**: `printer.cfg` includes `[include timelapse.cfg]` with a
    comment that it can be commented out if moonraker-timelapse is not installed.
    The script should remind the user of this in its post-install output, or
    proactively comment out that line unless the user confirms they have
    moonraker-timelapse installed.
