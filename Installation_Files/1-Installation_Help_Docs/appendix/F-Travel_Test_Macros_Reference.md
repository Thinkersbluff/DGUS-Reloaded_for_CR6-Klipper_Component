# Appendix F: Travel Test Macros Reference

Last Updated: 5 May 2026

## Purpose

This appendix provides detailed technical reference for the travel test macros and related utilities included with DGUS-Reloaded.

**Quick links:**
- **Quick start:** [3-Common Maintenance Tasks § Task 7](3-Common_Maintenance_Tasks.md#task-7-validate-and-adjust-belt-tension-using-travel-tests)
- **High-level overview:** [2-Understanding Your System § Available System Macros](2-Understanding_Your_System.md#available-system-macros-and-utilities)

---

## Table of Contents

- [Macro Descriptions](#macro-descriptions)
  - [X_TRAVEL_TEST / Y_TRAVEL_TEST](#x_travel_test--y_travel_test)
  - [X_TRAVEL_TEST_WITH_TMC / Y_TRAVEL_TEST_WITH_TMC](#x_travel_test_with_tmc--y_travel_test_with_tmc)
  - [TMC_SNAPSHOT](#tmc_snapshot)
- [Understanding the Output](#understanding-the-output)
  - [Basic Test Console Output](#basic-test-console-output)
  - [TMC Test Console Output](#tmc-test-console-output)
  - [Reading TMC Registers](#reading-tmc-registers)
- [Result Interpretation Guide](#result-interpretation-guide)
  - [Pass Criteria](#pass-criteria)
  - [Warning Signs](#warning-signs)
  - [Failure Indicators](#failure-indicators)
- [Motherboard Compatibility](#motherboard-compatibility)
- [Troubleshooting](#troubleshooting)

---

## Macro Descriptions

### X_TRAVEL_TEST / Y_TRAVEL_TEST

**Purpose:** Rapid linear motion stress test for belt tension validation.

**Available on:** All motherboards (Creality and BTT SKR)

**What it does:**
1. Homes all axes (G28)
2. Raises Z by 5mm for safety
3. Reads current motion limits (velocity, acceleration)
4. Applies those limits as the test parameters
5. Moves to starting position (X10 or Y10)
6. Runs 20 rapid cycles end-to-end (X10 ↔ X230 or Y10 ↔ Y230)
7. Restores original motion limits
8. Prints summary to console

**Duration:** Approximately 30–60 seconds depending on belt position.

**Motion parameters:**
- Travel distance: 220 mm (X or Y)
- Rapid feed rate: 18000 mm/min (300 mm/sec)
- Number of cycles: 20 (10 forward + 10 return = 4400 mm total travel)

**Console output example:**
```
X_TRAVEL_TEST Read toolhead: max_velocity=300.0, max_accel=3500.0
X_TRAVEL_TEST Applying test limits: velocity=300.0, accel=3500.0
X_TRAVEL_TEST Restoring from local snapshot: velocity=300.0, accel=3500.0
```

**What to listen for:**
- ✅ Smooth, consistent humming/whining sound (normal stepper tone)
- ✅ Same volume on both the forward and return directions
- ❌ Grinding, clicking, or slipping sounds (belt slip, obstruction)
- ❌ Squealing or distressed motor noise (tension too high)
- ❌ Loud bang or sudden stop (mechanical jam, motor stall)

---

### X_TRAVEL_TEST_WITH_TMC / Y_TRAVEL_TEST_WITH_TMC

**Purpose:** X/Y travel test with before/after TMC2209 driver diagnostics capture.

**Available on:** BTT SKR CR6 board only (requires UART-connected drivers)

**What it does:**
1. Reads configured stealthchop thresholds for X and Y from `printer.cfg`
2. **Pre-test snapshot:** Captures TMC driver status
3. Forces spreadCycle mode (TPWMTHRS=1048575) on both X and Y
4. **Runs X_TRAVEL_TEST or Y_TRAVEL_TEST** (same 20-cycle motion)
5. **Post-test snapshot:** Captures driver status again
6. Restores original stealthchop thresholds
7. Prints **result interpretation guide**

**Duration:** Same as basic test (~30–60 seconds) plus a few seconds for TMC register reads.

**Key enhancement:** Shows **driver load stress** during rapid motion, revealing:
- Whether the motor was able to maintain position (StallGuard result)
- Thermal warnings (overtemp pre-warning flag)
- Electrical faults (short-to-ground, open-load, etc.)
- Whether the correct driving mode (spreadCycle) was active

**Console output example:**
```
X_TRAVEL_TEST_WITH_TMC stepper_x: stealthchop_threshold=0 → already always-spreadCycle (TPWMTHRS=1048575) — no write needed
TMC_SNAPSHOT --- X_TRAVEL_TEST pre-test ---
[raw register dumps...]
[basic test runs...]
TMC_SNAPSHOT --- X_TRAVEL_TEST post-test ---
[raw register dumps...]
X_TMC_RESULT === How to read the snapshot above ===
X_TMC_RESULT DRV_STATUS flags — PASS: none of these present | WARN: otpw=1 (overtemp pre-warning) | FAIL: ot=1 (overtemp), s2ga=1/s2gb=1 (short-to-GND), ola=1/olb=1 (open load)
X_TMC_RESULT stealth flag — expect stealth=0 (spreadCycle active). stealth=1 means stealthChop is running instead.
[...]
```

---

### TMC_SNAPSHOT

**Purpose:** Capture raw TMC2209 driver status for both X and Y steppers.

**Available on:** BTT SKR CR6 board only

**What it does:**
1. Calls `DUMP_TMC STEPPER=stepper_x`
2. Calls `DUMP_TMC STEPPER=stepper_y`
3. Prints start/end delimiters for easy parsing

**Usage:** Typically called by `X_TRAVEL_TEST_WITH_TMC` and `Y_TRAVEL_TEST_WITH_TMC` automatically, but can be called standalone:
```
TMC_SNAPSHOT LABEL="my custom label"
```

**Output:** Raw register dump (~50 lines per stepper):
```
GSTAT:      00000000
IFCNT:      000000c0 ifcnt=192
SLAVECONF:  00000200 senddelay=2
[...more registers...]
```

---

## Understanding the Output

### Basic Test Console Output

Example full output from `X_TRAVEL_TEST`:

```
X_TRAVEL_TEST Read toolhead: max_velocity=300.0, max_accel=3500.0
X_TRAVEL_TEST Applying test limits: velocity=300.0, accel=3500.0
X_TRAVEL_TEST Restoring from local snapshot: velocity=300.0, accel=3500.0
```

**Line 1:** Reports current velocity and acceleration limits from the toolhead (runtime values).

**Line 2:** The macro will apply these same values during the test (max of runtime vs configured).

**Line 3:** After the test completes, limits are restored. The values should match Line 1.

**If Line 3 values differ from Line 1:** Indicates an internal issue; the macro's save/restore may have failed. Verify macro syntax.

---

### TMC Test Console Output

A full `X_TRAVEL_TEST_WITH_TMC` output includes:

#### Section 1: Pre-Test Mode Check
```
X_TRAVEL_TEST_WITH_TMC stepper_x: stealthchop_threshold=0 → already always-spreadCycle (TPWMTHRS=1048575) — no write needed
X_TRAVEL_TEST_WITH_TMC stepper_y: stealthchop_threshold=0 → already always-spreadCycle (TPWMTHRS=1048575) — no write needed
```

This tells you whether the drivers are already in the desired mode (threshold=0 means always spreadCycle). If threshold was non-zero, the macro would announce "forcing spreadCycle."

#### Section 2: Pre-Test TMC Snapshot
```
TMC_SNAPSHOT --- X_TRAVEL_TEST pre-test ---
GSTAT:      00000000
IFCNT:      000000b5 ifcnt=181
[...more registers...]
TPWMTHRS:   000fffff tpwmthrs=1048575
[...rest of dump...]
```

**Key fields to note:**
- `GSTAT`: Should be `00000000` (no faults before test)
- `TPWMTHRS`: Will show `000fffff` (hex for 1048575 = "always spreadCycle")
- Other fields are the baseline state

#### Section 3: Motion Test Runs (not shown in output, but you hear/feel it)
The printer moves rapidly for ~30–60 seconds.

#### Section 4: Post-Test TMC Snapshot
```
TMC_SNAPSHOT --- X_TRAVEL_TEST post-test ---
GSTAT:      00000000
SG_RESULT:  000001b2 sg_result=434
DRV_STATUS: 40140000 cs_actual=20 stealth=1
[...more registers...]
```

**Compare pre and post:**
- `GSTAT`: Should still be `00000000` (no new faults)
- `SG_RESULT`: Will likely be higher post-test (load was applied)
- `DRV_STATUS`: Will show current state during/after motion
- `stealth`: Should be `0` (spreadCycle active), **NOT** `1`

#### Section 5: Result Interpretation Guide
```
X_TMC_RESULT === How to read the snapshot above ===
X_TMC_RESULT DRV_STATUS flags — PASS: none of these present | WARN: otpw=1 (overtemp pre-warning) | FAIL: ot=1 (overtemp), s2ga=1/s2gb=1 (short-to-GND), ola=1/olb=1 (open load)
X_TMC_RESULT stealth flag — expect stealth=0 (spreadCycle active). stealth=1 means stealthChop is running instead.
X_TMC_RESULT GSTAT — expect 0x00000000. Non-zero means a driver fault or undervoltage reset occurred during the test.
X_TMC_RESULT sg_result (StallGuard load) — 0=stall, higher=more load headroom. Note: SGTHRS=0 so no automatic stall action is configured.
X_TMC_RESULT cs_actual — effective current scale (0-31). Should match irun from IHOLD_IRUN during motion.
```

This is printed automatically to help you interpret the raw dumps above.

---

### Reading TMC Registers

#### GSTAT (Global Status)
**Format:** `GSTAT: 00000000`

**Meaning:** Bit flags indicating driver state.
- `00000000` = All clear (ideal)
- Non-zero = One or more faults occurred

**What each bit means:**
- `bit 0 (reset)`: Driver was reset
- `bit 1 (drv_err)`: Driver error
- `bit 2 (uv_cp)`: Under-voltage (charge pump)

**Action:** If non-zero, something went wrong. Check the other fields and investigate the mechanical setup.

---

#### DRV_STATUS (Driver Status)
**Format:** Example: `DRV_STATUS: 40140000 cs_actual=20 stealth=1 stst=1`

**Key fields:**
- `cs_actual`: Effective current scale (0–31). Should match configured `run_current` during motion.
- `stealth`: `0` = spreadCycle active ✅, `1` = stealthChop active ❌
- `stst`: Standstill flag (`1` = motor not moving currently)
- `otpw`: Overtemp pre-warning (`1` = driver getting hot, warning before shutdown)
- `ot`: Overtemp (`1` = driver too hot, will shut down)
- `s2ga`, `s2gb`: Short-to-ground faults
- `ola`, `olb`: Open-load faults (motor winding issue)

---

#### SG_RESULT (StallGuard Result)
**Format:** `SG_RESULT: 000001b2 sg_result=434`

**Meaning:** StallGuard load estimate. Higher = more motor load headroom, `0` = stall.

| Value | Meaning |
|---|---|
| 0 | Stall detected (motor can't maintain position) |
| 1–100 | Very low headroom (belt too tight or excessive load) |
| 100–300 | Normal load during motion |
| 300+ | Comfortable headroom |

**Note:** StallGuard is disabled by default (SGTHRS=0), so no automatic stall protection is active. This is just a diagnostic reading.

---

#### TPWMTHRS (StealthChop Threshold)
**Format:** `TPWMTHRS: 000fffff tpwmthrs=1048575`

**Meaning:** Velocity threshold for switching between modes.

| Value | Meaning |
|---|---|
| `1048575` (0xFFFFF) | Always spreadCycle (never switch to stealthChop) |
| `0` | Always stealthChop (never use spreadCycle) |
| Other | Switch modes at this velocity threshold |

In Klipper config, `stealthchop_threshold: 0` translates to hardware `TPWMTHRS: 1048575` (always spreadCycle).

---

#### IHOLD_IRUN (Current Configuration)
**Format:** `IHOLD_IRUN: 00081414 ihold=20 irun=20 iholddelay=8`

**Meaning:** Holding and running current settings.
- `ihold`: Current scale while holding (not moving) — should be lower to save power
- `irun`: Current scale while running (moving) — should match `run_current` from printer.cfg
- `iholddelay`: Delay before switching to hold current

**Expected:** `irun` should be in the range that corresponds to your configured `run_current` (typically 0.5–1.0 A on a CR6, which maps to current scales 16–32).

---

## Result Interpretation Guide

### Pass Criteria

**Your test passed if ALL of the following are true:**

| Check | Criterion |
|---|---|
| **Pre-test GSTAT** | `00000000` (no prior faults) |
| **Post-test GSTAT** | `00000000` (no new faults) |
| **Pre-test TPWMTHRS** | `000fffff` or whatever your configured threshold is |
| **Post-test stealth flag** | `stealth=0` (spreadCycle running) |
| **Post-test SG_RESULT** | `> 0` (no stall detected, headroom exists) |
| **Visual/auditory** | Smooth, consistent motion; no grinding, clicking, or squealing |

**Interpretation:** Your belt is properly tensioned and the motor can handle rapid cycles without slipping or overheating.

---

### Warning Signs

**Investigate further if:**

| Sign | Meaning | Next Steps |
|---|---|---|
| Post-test GSTAT non-zero | Driver fault during test | Check mechanical alignment, belt tension; look for binding |
| Post-test `otpw=1` | Overtemp pre-warning | Driver got hot; check heatsink, reduce duty cycle, verify cooling |
| Post-test `stealth=1` | Wrong mode (stealthChop instead of spreadCycle) | Macro bug or config issue; verify DGUS release version |
| Post-test SG_RESULT very low (< 50) | Very little motor load headroom | Belt tension may be too high or load too high; tighten belt slightly if loose, check for friction |
| Audible grinding/squealing | Mechanical friction or tension issue | Inspect belt, pulley alignment, and carriage for obstructions |

**These are not failures, but indicate potential issues to investigate.**

---

### Failure Indicators

**Stop and troubleshoot if:**

| Failure | Meaning | Action |
|---|---|---|
| GSTAT `bit 1` set (`drv_err`) | Driver error during motion | EMI/wiring issue possible; check USB cables, stepper wire shielding |
| GSTAT `bit 2` set (`uv_cp`) | Charge pump undervoltage | Power supply issue; verify Vin to stepper driver, check connections |
| `otpw=1` during test | Overtemp pre-warning (repeatedly) | Driver overheating; reduce test feed rate, add heatsink, check for short |
| `ot=1` | Overtemp shutdown (hard stop) | Driver forced shutdown; reduce current, check heatsink, wait for cooldown |
| `s2ga=1` or `s2gb=1` | Short to ground detected | Wiring fault; inspect stepper cable for damage, test continuity |
| `ola=1` or `olb=1` | Open-load (motor winding issue) | Motor coil fault; replace stepper motor |
| Post-test `stealth=1` on both axes | Macro set wrong mode | DGUS release issue; update macros from latest release |
| SG_RESULT `0` (stall) | Motor can't maintain position at speed | Belt too tight, or motor current too low; check belt and adjust |
| Visible skipped steps or lost position | Open-loop motor failure | Stepper lost position; adjust tension/speed, replace motor if persistent |

---

## Motherboard Compatibility

### BTT SKR CR6 V1.0

| Feature | Available? | Notes |
|---|---|---|
| X_TRAVEL_TEST | ✅ Yes | Full motion test with limits save/restore |
| Y_TRAVEL_TEST | ✅ Yes | Full motion test with limits save/restore |
| X_TRAVEL_TEST_WITH_TMC | ✅ Yes | Includes pre/post TMC snapshots |
| Y_TRAVEL_TEST_WITH_TMC | ✅ Yes | Includes pre/post TMC snapshots |
| TMC_SNAPSHOT | ✅ Yes | UART-connected drivers, full diagnostics |
| DUMP_TMC command | ✅ Yes | Underlying command works |
| SET_TMC_FIELD command | ✅ Yes | Underlying command works |

**Configuration:**
- Stepper drivers: TMC2209 in UART mode
- UART pins: `PC11` (RX), `PC10` (TX)
- Drivers on single UART line with address select

---

### Creality 4.5.2 / 4.5.3 / 1.1.0.3 ERA

| Feature | Available? | Notes |
|---|---|---|
| X_TRAVEL_TEST | ✅ Yes | Basic motion test works |
| Y_TRAVEL_TEST | ✅ Yes | Basic motion test works |
| X_TRAVEL_TEST_WITH_TMC | ❌ No | Requires UART drivers (not available on Creality board) |
| Y_TRAVEL_TEST_WITH_TMC | ❌ No | Requires UART drivers (not available on Creality board) |
| TMC_SNAPSHOT | ❌ No | Requires UART drivers |
| DUMP_TMC command | ❌ No | Standalone drivers, no communication protocol |
| SET_TMC_FIELD command | ❌ No | Standalone drivers, no communication protocol |

**Configuration:**
- Stepper drivers: TMC2209 in standalone (step/dir) mode
- No UART communication possible
- Driver state not readable at runtime

**Workaround:** Use basic `X_TRAVEL_TEST` / `Y_TRAVEL_TEST` and rely on visual/auditory feedback and measuring tools.

---

## Troubleshooting

### Macro Not Found / Fails to Run

**Symptom:** "Unknown command 'X_TRAVEL_TEST_WITH_TMC'" or similar

**Causes:**
1. Macro not loaded from config files
2. Config syntax error preventing macro from being parsed
3. Klipper restart didn't complete cleanly

**Solution:**
1. Verify macro is defined in your config (or `CR6.cfg` is `[include]`d into `printer.cfg`)
2. Check `~/printer_data/logs/klippy.log` for syntax errors
3. Restart Klipper: **Firmware Restart** in Mainsail/Fluidd
4. Try again

---

### Macro Runs But Doesn't Move

**Symptom:** Console shows setup messages, but printer doesn't move

**Causes:**
1. Printer not homed (G28 at start of macro fails silently)
2. Steppers disabled
3. Estop or pause active

**Solution:**
1. Manually home all axes: `G28`
2. Check Klipper state is "Ready"
3. Confirm no active emergency stop or print pause
4. Try macro again

---

### "Velocity Must Be Greater Than 0.0" Error

**Symptom:** Macro fails with this error during `SET_VELOCITY_LIMIT`

**Causes:**
1. Macro bug (stale/incorrect velocity restoration)
2. Motion limits were 0 before macro ran (shouldn't happen, but possible)
3. Corrupted macro from older release

**Solution:**
1. Update to latest DGUS-Reloaded release
2. If error persists, verify `printer.cfg` has reasonable `max_velocity` and `max_accel` values
3. If still failing, restore macro from backup or file an issue

---

### TMC Test Shows `stealth=1` (Wrong Mode)

**Symptom:** Post-test `DRV_STATUS` shows `stealth=1` instead of `stealth=0`

**Causes:**
1. Macro bug (TPWMTHRS value inverted) — known issue in early releases
2. Manual threshold override in macro call

**Solution:**
1. Update to latest DGUS-Reloaded release (issue fixed)
2. Verify `TPWMTHRS` value is `1048575` (0xFFFFF), not `0`

---

### No TMC Output Despite BTT Board

**Symptom:** TMC commands fail or return empty

**Causes:**
1. UART not connected or configured incorrectly
2. Stepper not recognized by Klipper
3. TMC address not set correctly in config

**Solution:**
1. Verify `uart_pin` and `tx_pin` are correct in `[tmc2209 stepper_x]` sections
2. Check `uart_address` for each driver (should be 0 and 1 for X and Y)
3. Verify Klipper recognizes drivers: `DUMP_TMC STEPPER=stepper_x` should work directly
4. If it doesn't, check UART wiring and configuration, refer to BTT SKR documentation

---

### Macro Runs But Limits Not Restored

**Symptom:** After test completes, motion limits remain changed (not restored to original)

**Causes:**
1. Macro bug or older release with save/restore issue
2. Motion limits were changed during test but not captured correctly

**Solution:**
1. Manually restore limits via console: `SET_VELOCITY_LIMIT VELOCITY=<your_max> ACCEL=<your_max>`
2. Update to latest DGUS-Reloaded release
3. File an issue if problem persists

---

## Related Documents

- [3-Common Maintenance Tasks § Task 7: Validate Belt Tension](../3-Common_Maintenance_Tasks.md#task-7-validate-and-adjust-belt-tension-using-travel-tests)
- [2-Understanding Your System § Available System Macros](../2-Understanding_Your_System.md#available-system-macros-and-utilities)
- [2-Understanding Your System § Custom Macro Menus](../2-Understanding_Your_System.md#custom-macro-menus-via-dgus_menu_macroscfg)
- Klipper Documentation: [TMC2209 Configuration](https://www.klipper3d.org/TMC_Drivers.html)
- Klipper Documentation: [Config Checks](https://www.klipper3d.org/Config_checks.html)
