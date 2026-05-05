# Common Maintenance Tasks: DGUS-Reloaded for CR6 on Klipper

Last Updated: 9 March 2026

## Purpose

This guide gives task-based maintenance workflows for an **existing** DGUS-Reloaded installation.

- For background/context: see [2-Understanding_Your_System.md](2-Understanding_Your_System.md)
- For script syntax details: see [../scripts/README.md](../scripts/README.md)
- For full maintenance index: see [0-DGUS_Maintenance_Overview.md](0-DGUS_Maintenance_Overview.md)

---

## Prerequisites

- SSH access to your Klipper host
- Existing Klipper install at `~/klipper`
- DGUS scripts available under `~/printer_data/config/scripts/`
- Printer connected and powered on (for serial/MCU checks)

---

## Task 0: Quick Health Check (Start Here)

Use this before/after any maintenance action.

```bash
cd ~/klipper
git status -sb
git rev-parse --short HEAD
```

Expected:
- Current branch and commit shown
- `working tree clean` (or clear indication of modified tracked files)

---

## Task 1: Back Up Klipper Before Any Risky Change

### When to use
- Before update attempts
- Before hard reset
- Before patch/rebuild operations

### Why
Gives you a rollback point if update/rebuild fails.

### How

```bash
bash ~/printer_data/config/scripts/backup_klipper.sh
```

Expected outcome:
- A timestamped archive is created
- Script reports backup path

If needed, detailed restore steps are in:  
[appendix/B-Backup_Restore_Klipper.md](appendix/B-Backup_Restore_Klipper.md)

---

## Task 2: Clear “Dirty” Status So Moonraker Can Update Klipper

### When to use
- Moonraker/Mainsail says Klipper is **dirty**
- Update button is blocked or fails due to local changes

### Why
Tracked files (typically `Kconfig` / `Makefile`) were locally edited for DGUS build support.

### How

```bash
~/printer_data/config/scripts/manage_t5uid1_patches.sh prepare
cd ~/klipper
git status --porcelain
```

Expected outcome:
- No tracked-file modifications shown
- Moonraker should report Klipper as clean (after refresh/restart)

If still dirty:
```bash
cd ~/klipper
git status
```
Review remaining modified tracked files before updating.

---

## Task 3: Reapply DGUS Build Patches Before Building MCU Firmware

### When to use
- You need to build/flash a new `klipper.bin`
- You previously ran `prepare`

### Why
The build system needs DGUS-related edits present in tracked files.

### How

```bash
~/printer_data/config/scripts/manage_t5uid1_patches.sh reapply
cd ~/klipper
git status -sb
```

Expected outcome:
- `src/stm32/Kconfig` and `src/stm32/Makefile` show modified
- `make menuconfig` exposes required options for your DGUS workflow

After build/flash, run Task 2 (`prepare`) again to return to clean update state.

---

## Task 4: Recover After a Klipper Update Breaks Compatibility

### Typical symptoms
- `MCU 'mcu' has deprecated code...`
- Host starts but printer not fully operational
- Version mismatch warnings/errors

### Recovery paths

#### Option A (preferred): restore from backup
```bash
bash ~/printer_data/config/scripts/restore_klipper.sh
```
Then restart Klipper and verify status.

#### Option B: force known compatible commit
Use the SHA from DGUS release notes:

```bash
cd ~/klipper
git fetch --all --tags
git reset --hard <FULL_SHA>
git rev-parse --short HEAD
```

Confirm short SHA matches release-notes prefix.

Then continue with Task 5 (rebuild MCU firmware) if mismatch persists.

Detailed procedure:  
[appendix/C-Force_Klipper_Version.md](appendix/C-Force_Klipper_Version.md)

---

## Task 5: Rebuild and Reflash MCU Firmware to Match Host

### When to use
- Host changed version (update/reset/restore)
- MCU mismatch warnings/errors appear

### How (summary)

```bash
~/printer_data/config/scripts/manage_t5uid1_patches.sh reapply

cd ~/klipper
make clean
make
```

Then flash `~/klipper/out/klipper.bin` to your board with your normal SD-card board procedure.

After successful flash:
```bash
~/printer_data/config/scripts/manage_t5uid1_patches.sh prepare
```

Detailed step-by-step:
[appendix/A-Rebuilding_MCU_Firmware.md](appendix/A-Rebuilding_MCU_Firmware.md)

---

## Task 6: Verify Final Operational State

After any maintenance action:

1. Restart Klipper (Mainsail/Fluidd: **Firmware Restart**)
2. Confirm:
   - Klipper state is `Ready`
   - No MCU mismatch errors
   - Display responds normally
3. Confirm git clean state:

```bash
cd ~/klipper
git status --porcelain
```

Expected:
- Empty output (clean tracked state)

Optional diagnostic (if script exists in your package):
```bash
bash ~/printer_data/config/scripts/verify_installation.sh
```

---

## Decision Map (Fast)

| Situation | Run |
|---|---|
| “I want a safety point first” | Task 1 |
| “Moonraker says dirty” | Task 2 |
| “Need to build klipper.bin” | Task 3 → Task 5 |
| “Update broke system” | Task 4 |
| “MCU mismatch warning” | Task 5 |
| “Confirm everything is healthy” | Task 6 |

---

## Related Documents

- [0-DGUS_Maintenance_Overview.md](0-DGUS_Maintenance_Overview.md)
- [2-Understanding_Your_System.md](2-Understanding_Your_System.md)
- [appendix/A-Rebuilding_MCU_Firmware.md](appendix/A-Rebuilding_MCU_Firmware.md)
- [appendix/B-Backup_Restore_Klipper.md](appendix/B-Backup_Restore_Klipper.md)
- [appendix/C-Force_Klipper_Version.md](appendix/C-Force_Klipper_Version.md)
- [../scripts/README.md](../scripts/README.md)