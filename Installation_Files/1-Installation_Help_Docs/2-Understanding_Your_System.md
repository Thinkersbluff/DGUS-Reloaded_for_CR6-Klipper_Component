# Understanding Your DGUS-Reloaded Klipper System

Last Updated: 9 March 2026

## Purpose

This document explains **how the pieces fit together** and **why certain maintenance is needed**.

If you just want to perform a specific task, see [3-Common_Maintenance_Tasks.md](3-Common_Maintenance_Tasks.md) instead.

---

## Table of Contents

- [The Klipper Architecture](#the-klipper-architecture)
- [How Updates Work](#how-updates-work)
- [Git Status and "Dirty" Repos](#git-status-and-dirty-repos)
- [Why DGUS-Reloaded Requires Patches](#why-dgus-reloaded-requires-patches)
- [MCU Firmware vs Host Software Versioning](#mcu-firmware-vs-host-software-versioning)
- [The Role of Configuration Files](#the-role-of-configuration-files)
- [Custom Macro Menus via DGUS_Menu_Macros.cfg](#custom-macro-menus-via-dgus_menu_macroscfg)
- [Available System Macros and Utilities](#available-system-macros-and-utilities)

---

## The Klipper Architecture

Unlike traditional 3D printer firmware (like Marlin), Klipper splits responsibilities between two components:

### 1. Host Software (Klippy)
- **Runs on:** Raspberry Pi (or similar Linux host)
- **Location:** `~/klipper`
- **Does:** All the complex math, G-code parsing, motion planning
- **Language:** Python

### 2. MCU Firmware
- **Runs on:** Printer motherboard (STM32 microcontroller)
- **Location:** Flashed to motherboard as `klipper.bin`
- **Does:** Real-time stepper control, hardware I/O, executes commands from host
- **Language:** C

**Why this matters:**
- When you update Klipper on the Pi, the **host** changes but the **MCU** doesn't
- If the host and MCU versions become incompatible, you'll see warnings or errors
- This is why you sometimes need to rebuild and reflash MCU firmware after updates

---

## How Updates Work

### The Update Chain

```
Klipper3d/klipper (GitHub)
    ↓
Moonraker (checks for updates)
    ↓
Mainsail/Fluidd (shows "Update Available")
    ↓
You click "Update"
    ↓
Moonraker uses Git to pull changes
    ↓
Klipper host software updated
```

### Key Players

#### Klipper3d/klipper
- **Official upstream repository:** https://github.com/Klipper3d/klipper
- Developers publish updates regularly (bug fixes, new features)
- Your Pi's `~/klipper` folder is a Git clone of this repo

#### Moonraker
- **Update manager service** running on your Pi
- Monitors multiple repos for updates (configured in `~/printer_data/config/moonraker.conf`)
- Uses Git to track what's installed vs. what's available upstream
- Reports status to Mainsail/Fluidd

#### Git
- **Version control system** that tracks file changes
- Knows the difference between:
  - Files from upstream (Klipper3d/klipper)
  - Files you've modified locally
  - Files that aren't tracked at all

---

## Git Status and "Dirty" Repos

This is the **#1 source of confusion** for new Klipper users.

### What "Dirty" Means

When Moonraker shows Klipper as **"dirty"**, it means:
> "Git has detected that one or more **tracked files** in `~/klipper` have been modified locally, and those changes don't match what's in the Git history."

### Why Moonraker Cares

Moonraker **refuses to update** a dirty repo because:
- Pulling new changes could overwrite your local edits
- This might break your system without warning
- Git might encounter merge conflicts it can't resolve automatically

### What Git Tracks (and What It Doesn't)

Git in `~/klipper` tracks:
- ✅ All **original Klipper files** from upstream (`.py` files, config samples, `Makefile`, `Kconfig`, etc.)

Git **does not** track:
- ❌ Files you add that weren't in the original repo (unless you `git add` them)
- ❌ Files listed in `.gitignore`
- ❌ Files in other directories like `~/printer_data/`

### Common Causes of "Dirty" Status

| What You Did | Why It's Dirty |
|---|---|
| Edited `src/stm32/Kconfig` to add T5UID1 support | `Kconfig` is a tracked file |
| Edited `src/stm32/Makefile` to add T5UID1 support | `Makefile` is a tracked file |
| Added `klippy/extras/t5uid1/` folder | **Not dirty** (untracked files) |
| Edited `~/printer_data/config/printer.cfg` | **Not dirty** (different directory) |
| Ran `make menuconfig` which auto-updated `.config` | **Not dirty** (`.config` is gitignored) |

### How to Check Git Status

```bash
cd ~/klipper
git status
```

**Clean output:**
```
On branch master
Your branch is up to date with 'origin/master'.

nothing to commit, working tree clean
```

**Dirty output:**
```
On branch master
Your branch is up to date with 'origin/master'.

Changes not staged for commit:
  modified:   src/stm32/Kconfig
  modified:   src/stm32/Makefile
```

### How to Clear Dirty Status

**Option 1: Revert changes** (if you don't need them anymore)
```bash
git checkout -- src/stm32/Kconfig src/stm32/Makefile
```

**Option 2: Use our patch management script** (recommended for DGUS-Reloaded)
```bash
~/printer_data/config/scripts/manage_t5uid1_patches.sh prepare
```
This removes the temporary edits so Moonraker sees a clean repo.

**See also:** [3-Common_Maintenance_Tasks.md § Clearing Dirty State](3-Common_Maintenance_Tasks.md#task-2-clearing-dirty-state-for-updates)

---

## Why DGUS-Reloaded Requires Patches

### The Challenge

Upstream Klipper doesn't include support for the DWIN T5UID1 touchscreen protocol used by CR6 displays.

To add this support, DGUS-Reloaded needs to:
1. **Add new untracked files** (extras, drivers) ← Git doesn't care about these
2. **Temporarily modify tracked files** (`Kconfig`, `Makefile`) ← Git **does** care about these

### Why We Modify Tracked Files

| File | Why We Edit It |
|---|---|
| `src/stm32/Kconfig` | Add T5UID1 configuration options to `make menuconfig` menu |
| `src/stm32/Makefile` | Include T5UID1 source files in MCU firmware build |

Without these edits, the Klipper build system doesn't know our T5UID1 code exists.

### The Workflow Dilemma

```
┌─────────────────────────────────────────────┐
│ Want to build MCU firmware?                 │
│ → Need patches APPLIED (edits present)      │
└─────────────────────────────────────────────┘
              ↕
┌─────────────────────────────────────────────┐
│ Want to update Klipper via Moonraker?       │
│ → Need patches REMOVED (no edits present)   │
└─────────────────────────────────────────────┘
```

### Our Solution: `manage_t5uid1_patches.sh`

This script toggles the edits on/off:

| Command | When to Use | What It Does |
|---|---|---|
| `./manage_t5uid1_patches.sh reapply` | Before building MCU firmware | Applies edits to `Kconfig` and `Makefile` |
| `./manage_t5uid1_patches.sh prepare` | Before allowing Moonraker update | Removes edits, making repo clean |

**Example workflow:**
```bash
# You want to rebuild MCU firmware
~/printer_data/config/scripts/manage_t5uid1_patches.sh reapply   # Apply edits
cd ~/klipper
make menuconfig                                                   # Configure build (sees T5UID1 options)
make                                                              # Build firmware
# Flash to motherboard...
~/printer_data/config/scripts/manage_t5uid1_patches.sh prepare   # Remove edits
git status                                                        # Now clean!
```

**See also:**
- [3-Common_Maintenance_Tasks.md § Clearing Dirty State](3-Common_Maintenance_Tasks.md#task-2-clearing-dirty-state-for-updates)
- [Appendix A: Rebuilding MCU Firmware](appendix/A-Rebuilding_MCU_Firmware.md)
- [scripts/README.md § manage_t5uid1_patches.sh](../scripts/README.md#manage_t5uid1_patchessh)

---

## MCU Firmware vs Host Software Versioning

### The Version Mismatch Problem

Klipper's host and MCU communicate using an internal protocol. When they're built from different Klipper versions, the protocol might not match.

**Symptoms of mismatch:**
```
MCU 'mcu' has deprecated code (it is missing feature 'STEPPER_STEP_BOTH_EDGE').
Recompiling and flashing is recommended
```

or worse:
```
Unable to connect to MCU 'mcu': incompatible firmware version
```

### When Mismatch Happens

| Scenario | Host Version | MCU Version | Result |
|---|---|---|---|
| Fresh install | v0.12.0-372 | v0.12.0-372 | ✅ Match |
| After Moonraker update | v0.12.0-380 | v0.12.0-372 | ⚠️ Warning (minor mismatch) |
| After major update | v0.13.0-10 | v0.12.0-372 | ❌ Error (incompatible) |

### How to Check Versions

**Host version:**
```bash
cd ~/klipper
git log -1 --oneline
```

**MCU version:**  
Look in Mainsail console after `FIRMWARE_RESTART`:
```
MCU 'mcu' shutdown: Rescheduled timer in the past
...
MCU config: ... version=v0.12.0-372-g88a71c3c ...
```

### When to Rebuild MCU Firmware

| Situation | Action Required |
|---|---|
| Warning about deprecated features | Rebuild recommended (non-urgent) |
| "Incompatible firmware version" error | **Rebuild required immediately** |
| After any host update that adds new features you want to use | Rebuild to enable those features |
| After restoring a backup to older host version | Rebuild to match older version |

**See also:** [Appendix A: Rebuilding MCU Firmware](appendix/A-Rebuilding_MCU_Firmware.md)

---

## The Role of Configuration Files

### Two Configuration Layers

Klipper uses configuration files at two different stages:

#### 1. Build-Time Config (MCU firmware)
- **File:** `.config` in `~/klipper/`
- **Created by:** `make menuconfig`
- **Purpose:** Tells the compiler which features to include in the MCU firmware binary
- **When it matters:** Only when building `klipper.bin`

**Example settings:**
- Processor model (STM32F103)
- Clock speed
- Communication interface (USB vs UART)
- Enable T5UID1 support ✓

#### 2. Runtime Config (Host software)
- **Files:** `~/printer_data/config/printer.cfg` (and included files)
- **Purpose:** Tells Klippy how to control your specific printer hardware
- **When it matters:** Every time Klipper starts

**Example settings:**
- Stepper motor directions and steps/mm
- Heater PID values
- Probe offsets
- Macros and display layout

### Why Both Are Needed

```
Build-time config (make menuconfig)
    ↓
Compiles into klipper.bin
    ↓
Flash to motherboard
    ↓
MCU firmware runs with those capabilities
    ↓
Runtime config (printer.cfg)
    ↓
Klippy uses those capabilities to control hardware
```

**Example:** T5UID1 support
1. Build-time: Enable T5UID1 in `make menuconfig` → firmware can talk to display
2. Runtime: Configure `[t5uid1]` section in `printer.cfg` → Klippy knows which pins/settings to use

### Config File Locations

| File | Location | Tracked by Git? | Purpose |
|---|---|---|---|
| `printer.cfg` | `~/printer_data/config/` | ❌ No | Main runtime config |
| `CR6.cfg` | `~/printer_data/config/` | ❌ No | CR6 hardware definitions |
| `*.cfg` (others) | `~/printer_data/config/` | ❌ No | Included configs (macros, etc.) |
| `.config` | `~/klipper/` | ❌ No (gitignored) | Build-time MCU config |
| `Kconfig` | `~/klipper/src/stm32/` | ✅ Yes | Defines available build options |
| `Makefile` | `~/klipper/src/stm32/` | ✅ Yes | Build system rules |

**Key takeaway:**
- Editing `printer.cfg` → never causes dirty status
- Editing `Kconfig` or `Makefile` → causes dirty status

**See also:** [Appendix D: Config Files Reference](appendix/D-Config_Files_Reference.md) *(future document)*

---

## Custom Macro Menus via DGUS_Menu_Macros.cfg

### What Is This File?

`DGUS_Menu_Macros.cfg` is a user-editable configuration file that tells DGUS-Reloaded which macros to display in custom menus on the touchscreen.

**Location:** `~/printer_data/config/DGUS_Menu_Macros.cfg`

**Important:** This file should NOT be `[include]`d into `printer.cfg`. DGUS-Reloaded reads it separately.

### How It Works

When you tap the **`[<>]` icon** on a DGUS-Reloaded display screen (e.g., Home, Calibrate, Paused Print):

1. DGUS-Reloaded looks up which section in `DGUS_Menu_Macros.cfg` corresponds to that screen
2. It displays a menu of macro names listed in that section (max 9 lines per page, unlimited pages)
3. You tap a macro name to run it
4. **DGUS-Reloaded performs no sanity checks** — it simply executes what you select

### Example: The `[Calibrate Macros]` Section

From `DGUS_Menu_Macros.cfg`:
```
[Calibrate Macros]
RUN_ABL_COLD
RUN_ABL_BED_60
RUN_ABL_BED_80
RUN_ABL_BED_95
FIRMWARE_RESTART
```

When you tap `[<>]` on the Calibrate screen, this list appears. Select one to run it.

### Screen-to-Section Mapping

| Display Screen | Config Section | Accessed From |
|---|---|---|
| Home (Screen 001) | `[Home]` | Main menu tap |
| SetUp (Screen 018) | `[SetUp Macros]` | Setup menu |
| Calibrate (Screen 009) | `[Calibrate Macros]` | Calibrate menu |
| Prepare (Screen 006) | `[Prepare Macros]` | Prepare menu |
| Print (Screen 016) | `[Print Macros]` | Print ready / Print finished |
| Print Active (Screen 003) | `[Active Print Macros]` | During active print |
| Print Paused (Screen 007, 011) | `[Paused Print Macros]` | While print is paused |

### How to Customize Your Macros

1. Open `DGUS_Menu_Macros.cfg` in a text editor (via SFTP or SSH)
2. Find the section that corresponds to the screen where you want to add a macro
3. Add the macro name on a new line
4. Save the file
5. Restart Klipper (or just refresh the DGUS display)

**Example:** To add a belt tension test to the Calibrate menu:
```
[Calibrate Macros]
RUN_ABL_COLD
RUN_ABL_BED_60
RUN_ABL_BED_80
RUN_ABL_BED_95
X_TRAVEL_TEST_WITH_TMC          # ← New line added
Y_TRAVEL_TEST_WITH_TMC          # ← New line added
FIRMWARE_RESTART
```

### Important: User Responsibility

**⚠️ WARNING:** You are responsible for the consequences of running macros. DGUS-Reloaded does **not** prevent unsafe operations.

**Examples of things that could go wrong:**
- Running `G28` (home) while the printer is paused mid-print
- Running `UNLOAD_FILAMENT` with a cold nozzle
- Running a test macro while another motion is in progress

**Best practice:** Only add macros to sections where they make sense for that context.

### Limitations

- Macro names must be defined in your Klipper config (`printer.cfg` or included files)
- Display space limits the first 32 characters of a macro name (longer names still work, but are truncated on screen)
- Menu order follows the order in the config file (edit to reorder)

**See also:** [Appendix F: Travel Test Macros Reference](appendix/F-Travel_Test_Macros_Reference.md)

---

## Available System Macros and Utilities

This section provides a high-level overview of the macros included with DGUS-Reloaded for CR6.

### Calibration & Bed Leveling Macros

| Macro | Purpose | When to Use |
|---|---|---|
| `RUN_ABL_COLD` | Auto bed leveling with cold nozzle | Before first print, after any mechanical changes |
| `RUN_ABL_BED_60` | ABL with bed at 60°C | Before printing PLA (typical) |
| `RUN_ABL_BED_80` | ABL with bed at 80°C | Before printing PETG |
| `RUN_ABL_BED_95` | ABL with bed at 95°C | Before printing ABS/ASA/Wood |

**Note:** Saves separate profiles for each temp. Load the appropriate profile in `START_PRINT` based on bed temperature.

### Utility Macros

| Macro | Purpose | When to Use |
|---|---|---|
| `LED_ON` | Turn on hotend LED | Visual diagnostics |
| `LED_OFF` | Turn off hotend LED | — |
| `LOAD_FILAMENT` | Load filament into nozzle | After unload or cold start |
| `UNLOAD_FILAMENT` | Retract and unload filament | Filament change, cold storage |
| `REPORT_FILAMENT_SENSOR_ENABLE_STATUS` | Show runout sensor status | Troubleshooting filament issues |
| `SAVE_CONFIG` | Save Klipper calibration values | After PID calibration, Z-offset tuning |
| `FIRMWARE_RESTART` | Restart Klipper host | After config edits, recovering from errors |

**Warnings:**
- `LOAD_FILAMENT` and `UNLOAD_FILAMENT` require the nozzle to be hot (≥185°C)
- Don't call these during an active print

### Belt Tension Validation Macros

| Macro | Purpose | Motherboard Support |
|---|---|---|
| `X_TRAVEL_TEST` | Rapid X-axis motion to stress belt/motors | All boards |
| `Y_TRAVEL_TEST` | Rapid Y-axis motion to stress belt/motors | All boards |
| `X_TRAVEL_TEST_WITH_TMC` | `X_TRAVEL_TEST` + TMC driver diagnostics before/after | BTT SKR CR6 only |
| `Y_TRAVEL_TEST_WITH_TMC` | `Y_TRAVEL_TEST` + TMC driver diagnostics before/after | BTT SKR CR6 only |
| `TMC_SNAPSHOT` | Capture current TMC2209 driver status | BTT SKR CR6 only |

**Purpose:** Validate belt tension and detect potential belt slip or motor issues. Runs rapid linear cycles and captures driver diagnostics (if available).

**Limitations:**
- Cannot directly measure belt tension (that still requires manual tools)
- Can reveal symptoms: vibration, skipped steps, driver faults
- Creality motherboards: no TMC diagnostics available

**See also:** [3-Common Maintenance Tasks § Validate and Adjust Belt Tension](3-Common_Maintenance_Tasks.md#task-7-validate-and-adjust-belt-tension-using-travel-tests)  
**Detailed reference:** [Appendix F: Travel Test Macros Reference](appendix/F-Travel_Test_Macros_Reference.md)

---

## Summary: Key Concepts

| Concept | What You Need to Know |
|---|---|
| **Host vs MCU** | Klipper runs on both; they must stay compatible |
| **Git dirty status** | Means tracked files were modified; blocks updates |
| **DGUS patches** | Temporarily edit tracked files; toggle with script |
| **Moonraker** | Manages updates; refuses to update dirty repos |
| **MCU version mismatch** | Warning/error when host and MCU are out of sync |
| **Build-time vs runtime config** | `.config` builds firmware; `printer.cfg` controls printer |

---

## What to Read Next

- **To perform maintenance tasks:** [3-Common_Maintenance_Tasks.md](3-Common_Maintenance_Tasks.md)
- **To rebuild MCU firmware:** [Appendix A: Rebuilding MCU Firmware](appendix/A-Rebuilding_MCU_Firmware.md)
- **To clear dirty state:** [3-Common_Maintenance_Tasks.md § Clearing Dirty State](3-Common_Maintenance_Tasks.md#task-2-clearing-dirty-state-for-updates)
- **For script syntax:** [scripts/README.md](../scripts/README.md)