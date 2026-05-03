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