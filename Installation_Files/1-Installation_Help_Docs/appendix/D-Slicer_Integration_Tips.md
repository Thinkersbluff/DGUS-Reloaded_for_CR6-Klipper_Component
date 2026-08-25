# Appendix D: Slicer Integration Tips
**OPtional**

Last Updated: 25 August 2026

## Purpose

This document provides slicer configuration guidelines to integrate your 3D printer slicer with DGUS-Reloaded for CR6.

**Is this required?** No. Your printer will work without slicer integration. However, configuring your slicer enables:
- Real-time print progress (%) display on the touchscreen
- Remaining print time display
- Layer information during printing

---

## Overview

The DGUS-Reloaded display screens rely on receiving specific G-code messages from your slicer:
- **M73 P** messages → display print progress percentage
- **M73 R** messages → display time remaining
- **M117** messages → display layer info and estimated layer time

Klipper also differs from Marlin in G-code commands and macro variable names. Each slicer handles these differently, so configuration is slicer-specific.

---

## Ultimaker Cura (5.7.0+)

### Configuring Data Display

At Cura 5.7.0, the plugin system was updated. Use the **"Display Info on LCD"** add-in with these settings:

![New Cura PlugIns_1of2](https://github.com/user-attachments/assets/f6f27bf4-17b7-4303-aefe-ce1373df5e83)

![New Cura PlugIns_2of2](https://github.com/user-attachments/assets/7422acee-a78c-447e-86e4-d79ef7a2c321)

**What each setting does:**

| Setting | Purpose |
|---|---|
| M118 instruction | Logs reports to Klipper log and Mainsail console |
| M73 messages | Feeds % progress and time remaining to display |
| Display Progress (M117) | Shows current layer #, total layers, and estimated layer time on DGUS display |

### Configuring Start and End G-codes

Use these Machine Code settings in your Cura printer profile:

![Cura Machine Code Settings](https://github.com/user-attachments/assets/6b7568cd-b96b-48b1-b9c3-61c7ecd22744)

The last (truncated) line is:
```
start_print EXTRUDER_TEMP={material_print_temperature_layer_0} BED_TEMP={material_bed_temperature_layer_0}
```

**Important note about variable names:**
I use `EXTRUDER_TEMP` (not `HOTEND_TEMP`) because this is the parameter name recommended for OrcaSlicer users. This makes the Klipper `START_PRINT` macro compatible regardless of which slicer you use. If you use different variable names in your own macros, you may see Klipper errors.

---

## OrcaSlicer

### Configuring Data Display

OrcaSlicer sends **M73 P** and **M73 R** messages by default.

**Critical setting:** In your printer profile, ensure the box **"Disable set remaining print time"** is **NOT checked**.

![OrcaSlicer M73 Settings](https://github.com/user-attachments/assets/52f534ed-6a92-4424-a446-52903681d0a5)

**Note:** Last I checked, OrcaSlicer did not support displaying layer information, like Cura does. If you find a way to enable this, please open a Discussion or Issue on the DGUS-Reloaded repository and I will update this tip.

### Configuring Start and End G-codes

Use these Machine Code settings in your OrcaSlicer printer profile:
```
start_print BED_TEMP=[bed_temperature_initial_layer_single] EXTRUDER_TEMP=[nozzle_temperature_initial_layer]
```

![OrcaSlicer Start G-code](https://github.com/user-attachments/assets/2e456fd4-1c9b-4baa-93ce-d60575bca2ca)

![OrcaSlicer End G-code Part 1](https://github.com/user-attachments/assets/2beb7124-e2c8-465e-b6c5-c9b333a2a4cb)

![OrcaSlicer End G-code Part 2](https://github.com/user-attachments/assets/d59a75fc-87db-4e0d-b522-983051909daa)

### Additional OrcaSlicer Setting

Enable **"Use relative E distances"** in your printer profile. This requires `G92 E0` at the start of each new layer:

![OrcaSlicer Relative E Distances](https://github.com/user-attachments/assets/03e0599b-670c-48c6-845a-370e8214ae08)

---

## Other Slicers

I currently only use Cura and I once used OrcaSlicer. If you have successfully configured another slicer (PrusaSlicer, SuperSlicer, Bambu Studio, etc.) for use with DGUS-Reloaded on CR6, please open a Discussion or Issue on the [DGUS-Reloaded repository](https://github.com/Thinkersbluff/DGUS-Reloaded_for_CR6-Klipper_Component) to share your settings.

Community contributions are welcome and appreciated!

---

## M73 Message Format Reference

For developers or advanced users configuring slicers not listed above:

| Message | Format | Purpose |
|---|---|---|
| Print progress | `M73 P<percent>` | Display current print progress (0-100) |
| Time remaining | `M73 R<minutes>` | Display estimated minutes remaining |
| Layer info | `M117 <message>` | Display custom message (layer #, time, etc.) |

Example Klipper macro output:
```gcode
M73 P50
M73 R120
M117 Layer 25/100 - Est. 2:15
```

---

## Troubleshooting Slicer Integration

| Symptom | Possible Cause | Solution |
|---|---|---|
| Progress % not showing on display | M73 P not being sent | Check slicer macro/plugin settings |
| Time remaining shows 0 or -- | M73 R not being sent | Verify "Disable remaining time" is unchecked (OrcaSlicer) |
| START_PRINT macro fails | Wrong variable names (HOTEND_TEMP vs EXTRUDER_TEMP) | Update macro or slicer variable names to match |
| Layer info not displaying | Using OrcaSlicer | OrcaSlicer doesn't support layer count display; use Cura for full features |

---

## Related Documents

- [1-Manual_Installation.md](../1-Manual_Installation.md) § Step 11 (Optional): Configure Your Slicer
- [4-Updating_Existing_Installation.md](../4-Updating_Existing_Installation.md) (mentions slicer compatibility)
