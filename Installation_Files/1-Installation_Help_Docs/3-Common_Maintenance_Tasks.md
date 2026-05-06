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

## Task 7: Validate and Adjust Belt Tension Using Travel Tests

### When to use
- Printer assembled for the first time
- After manual belt adjustment on X or Y
- Noticing vibration, noise, or print quality issues
- Diagnosing potential belt slip or motor load problems

### Why

Travel tests run rapid linear motion cycles to stress the belt and motors. This helps reveal:
- **Belt tension too loose:** May skip steps, hear grinding/slipping
- **Belt tension too tight:** Motors work harder, may hear squealing, temperature warnings
- **Imbalanced tension:** One axis noisier or less smooth than the other
- **Motor issues:** TMC driver fault flags (BTT boards only)

### Important Limitations

⚠️ **Travel tests reveal symptoms but do NOT directly measure belt tension.** You will still need:
- A belt tension gauge (recommended: Luthier's gauge or similar)
- Manual tensioning procedure specific to your CR6 motherboard
- Multiple test iterations (adjust tension → test → repeat)

### How (Quick Start)

#### Option A: Basic test (all motherboards)

```bash
# From Mainsail console, or add to [Calibrate Macros] in DGUS_Menu_Macros.cfg:
X_TRAVEL_TEST
Y_TRAVEL_TEST
```

The printer will:
1. Home all axes
2. Raise Z slightly for safety
3. Run 20 rapid cycles on the specified axis (X10 to X230, or Y10 to Y230)
4. Restore original motion limits
5. Print results to console

**What to listen for:**
- Smooth, quiet motion with consistent tone
- No grinding, clicking, or slipping sounds
- Motor current draw shown in console should be reasonable

#### Option B: Advanced test with TMC diagnostics (BTT SKR CR6 only)

```bash
# From Mainsail console, or add to [Calibrate Macros]:
X_TRAVEL_TEST_WITH_TMC
Y_TRAVEL_TEST_WITH_TMC
```

Same motion as above, **plus:**
1. Captures TMC2209 driver status **before** the test (baseline)
2. Captures status **after** the test (shows load/stress response)
3. Prints a result interpretation guide so you know what "OK" looks like

**Key fields to review:**
- `GSTAT`: Should be `0x00000000` (no driver faults)
- `DRV_STATUS`: Should have NO error flags (`otpw`, `ot`, `s2ga`, `s2gb`, `ola`, `olb`)
- `stealth`: Should be `0` (spreadCycle mode active, not stealthChop)
- `sg_result`: StallGuard load estimate (higher = more headroom, 0 = stall)

### Adding Travel Tests to Your DGUS Menu

To make these tests easily accessible from the display:

1. Open `~/printer_data/config/DGUS_Menu_Macros.cfg` via SFTP
2. Find the `[Calibrate Macros]` section
3. Add the macros:

```
[Calibrate Macros]
RUN_ABL_COLD
RUN_ABL_BED_60
RUN_ABL_BED_80
RUN_ABL_BED_95
X_TRAVEL_TEST                    # ← Add these
Y_TRAVEL_TEST                    # ← Add these
X_TRAVEL_TEST_WITH_TMC           # ← (BTT boards only)
Y_TRAVEL_TEST_WITH_TMC           # ← (BTT boards only)
FIRMWARE_RESTART
```

4. Restart Klipper or refresh the DGUS display
5. Tap `[<>]` on the Calibrate screen to see the updated menu

### Interpreting Results

#### Visual / Auditory Clues

| Observation | Likely Cause | Action |
|---|---|---|
| Smooth, quiet motion, no grinding | ✅ Belt tension likely OK | Proceed to print |
| Grinding, clicking, or slipping sounds | Belt too loose | Tighten belt slightly, re-test |
| Squealing, motor sounds distressed | Belt too tight | Loosen belt slightly, re-test |
| Vibration visible on print head | Unbalanced tension (X vs Y) | Check both axes, adjust weaker one |

#### Console Output (Basic Test)

Expected output shows:
- Voltage limits applied before test
- Test running (20 cycles completed)
- Limits restored after test
- No error messages

If you see `ERROR: velocity must be greater than 0.0` or similar, stop and verify macro integrity.

#### Console Output (TMC Test with Interpretation Guide)

After the test, you'll see:
1. Raw TMC register dumps (pre-test and post-test)
2. **Result interpretation guide** with pass/warn/fail criteria
3. Restoration confirmation

**Pass criteria (for BTT boards):**
- `GSTAT`: `00000000`
- No `otpw`, `ot`, `s2ga`, `s2gb`, `ola`, `olb` flags in `DRV_STATUS`
- `stealth`: `0` (spreadCycle running)
- `sg_result` > 0 (load headroom exists)

### Next Steps: Adjusting Belt Tension

1. **Identify the axis with the problem** (X or Y)
2. **Adjust the belt tensioner for that axis:**
   - The CR6-SE has in-frame belt tensioners on both X and Y axes
   - X-axis: tensioner screws are at the right end of the X-axis gantry
   - Y-axis: tensioner screws are at the rear of the Y-axis frame
3. **Adjust incrementally:** Small turns (1/4 turn at a time)
4. **Re-test:** Run the travel test again after each adjustment
5. **Iterate:** Repeat until you get a smooth, quiet result
6. **Confirm with gauge:** Optional but recommended — measure final tension with a belt gauge

### Motherboard-Specific Notes

#### BTT SKR CR6 Board
- ✅ Full TMC driver diagnostics available via `X_TRAVEL_TEST_WITH_TMC` / `Y_TRAVEL_TEST_WITH_TMC`
- ✅ Can capture stress response and fault flags in real time

#### Creality 4.5.2 / 4.5.3 / ERA / 1.1.0.3 Boards
- ⚠️ Standalone TMC drivers (no UART diagnostics)
- ✅ Basic `X_TRAVEL_TEST` / `Y_TRAVEL_TEST` still available for motion stress testing
- ❌ No driver fault flags available — rely on visual/auditory feedback

### Troubleshooting Travel Tests

| Issue | Solution |
|---|---|
| Macro not found or fails to run | Ensure macro is defined in your `.cfg` files; restart Klipper |
| "velocity must be greater than 0.0" error | Internal macro bug; verify `.cfg` syntax, or restore from backup |
| TMC test shows `stealth=1` (wrong mode) | Macro firmware bug; update `.cfg` from latest release |
| No TMC output despite BTT board | UART connection issue; verify `uart_pin` / `tx_pin` in `printer.cfg` |

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
| "I want to validate or adjust belt tension" | Task 7 |
---

## Related Documents

- [0-DGUS_Maintenance_Overview.md](0-DGUS_Maintenance_Overview.md)
- [2-Understanding_Your_System.md](2-Understanding_Your_System.md)
- [appendix/A-Rebuilding_MCU_Firmware.md](appendix/A-Rebuilding_MCU_Firmware.md)
- [appendix/B-Backup_Restore_Klipper.md](appendix/B-Backup_Restore_Klipper.md)
- [appendix/C-Force_Klipper_Version.md](appendix/C-Force_Klipper_Version.md)
- [appendix/F-Travel_Test_Macros_Reference.md](appendix/F-Travel_Test_Macros_Reference.md)
- [../scripts/README.md](../scripts/README.md)