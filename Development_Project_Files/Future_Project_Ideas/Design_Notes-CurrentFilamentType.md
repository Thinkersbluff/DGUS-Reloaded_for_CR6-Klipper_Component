# Design Notes: Current Filament Type Feature

**Status:** Future / Planning
**Date created:** 2026-06-07

---

## Problem Statement

The printer currently has no runtime knowledge of which filament type is physically loaded.
This causes two related issues:

1. **Temperature guards are generic.** `DGUS_FILAMENT_MOVE` blocks extrusion below the firmware `min_extrude_temp` (e.g. 180 °C), but that threshold is the same regardless of filament type. 180 °C may be adequate for PLA but is dangerously low for ABS or PETG.
2. **No reminder to update filament type when reloading.** The user can swap the physical filament on the printer without updating the "current filament type" setting, causing wrong temperature presets or wrong minimum-extrusion checks to be applied silently.

---

## Existing Infrastructure (What We Already Have)

### Per-type default temperatures (`__init__.py` constants)
```python
'temp_pla':  { 'hotend': 210, 'bed': 60 }
'temp_abs':  { 'hotend': 240, 'bed': 90 }
'temp_petg': { 'hotend': 225, 'bed': 80 }

'preset_pla':  1
'preset_abs':  2
'preset_petg': 3
```

### Per-type user-editable temperatures (presets in printer.cfg)
Stored and retrieved via `get_preset_values()` / `update_preset_value()`:
- `filament_type_1_default_nozzle_temp` / `filament_type_1_default_bed_temp`
- `filament_type_2_default_nozzle_temp` / `filament_type_2_default_bed_temp`
- `filament_type_3_default_nozzle_temp` / `filament_type_3_default_bed_temp`
- Display names: `filament_type_1_default_name`, `filament_type_2_default_name`, `filament_type_3_default_name`

These are editable from the SetUp screen and persisted in the `[dgus_reloaded]` presets section of `printer.cfg`.

### Runtime session variable
`set_variable("filament_type", data)` is written by `__temp_preset` (address 0x2010) when the user taps a filament preset button on the Temperature screen. This is a session-only variable — it is lost on RESTART/FIRMWARE_RESTART.

### `DGUS_FILAMENT_MOVE` macro (`DGUS-Reloaded.cfg`)
Currently checks at GCode execution time:
1. `printer[ext_name].can_extrude` — current temp ≥ firmware `min_extrude_temp`
2. `printer[ext_name].target ≥ min_extrude_temp` — heater is actively targeting an adequate temperature

A third per-filament-type check is the next logical step (see below).

---

## Proposed Additions

### 1. Per-type minimum extrusion temperature

Add a `min_extrude_temp` preset for each filament type to the `[dgus_reloaded]` presets section in `printer.cfg`, alongside the existing nozzle/bed defaults:

```ini
filament_type_1_min_extrude_temp: 185   # PLA
filament_type_2_min_extrude_temp: 220   # ABS
filament_type_3_min_extrude_temp: 210   # PETG
```

Add default fallback values to `__init__.py` constants:
```python
'temp_pla':  { 'hotend': 210, 'bed': 60, 'min_extrude': 185 }
'temp_abs':  { 'hotend': 240, 'bed': 90, 'min_extrude': 220 }
'temp_petg': { 'hotend': 225, 'bed': 80, 'min_extrude': 210 }
```

Add corresponding output vars (to display on SetUp screen) and input vars (to allow the user to edit the value) in `vars_out.cfg` / `vars_in.cfg`, following the same pattern as `filament_type_N_default_nozzle_temp`.

### 2. Third check in `DGUS_FILAMENT_MOVE`

After the two existing checks, add a per-filament-type minimum check:

```jinja2
{% set filament_type = get_variable("filament_type", 0)|int %}
{% if filament_type == 1 %}
  {% set type_min = get_preset_values('filament_type_1_min_extrude_temp',
                                      printer.t5uid1.constants.temp_pla.min_extrude) %}
{% elif filament_type == 2 %}
  {% set type_min = get_preset_values('filament_type_2_min_extrude_temp',
                                      printer.t5uid1.constants.temp_abs.min_extrude) %}
{% elif filament_type == 3 %}
  {% set type_min = get_preset_values('filament_type_3_min_extrude_temp',
                                      printer.t5uid1.constants.temp_petg.min_extrude) %}
{% else %}
  {% set type_min = min_temp %}  {# No filament type set — degrade to firmware minimum #}
{% endif %}
{% if printer[ext_name].target < type_min %}
  {% set msg = "Target %dC too low for filament type (min %dC)" % (printer[ext_name].target|int, type_min|int) %}
  DGUS_SET_MESSAGE MSG={msg}
  RESPOND TYPE=error MSG="{msg}"
  M300 S880 P500
{% else %}
  ...move commands...
{% endif %}
```

When `filament_type == 0` (unset), the check degrades gracefully to the firmware minimum, preserving backward compatibility.

### 3. Persist `filament_type` across RESTART

`set_variable` is session-only. To survive a RESTART, save and restore via `[save_variables]`:

In `__temp_preset` (vars_in.cfg), after setting the variable:
```jinja2
SAVE_VARIABLE VARIABLE=current_filament_type VALUE={data}
```

In the boot/startup routine, read it back:
```jinja2
{% set saved = printer.save_variables.variables.get("current_filament_type", 0) %}
{% do set_variable("filament_type", saved) %}
```

### 4. Auto-update `filament_type` when a preset is applied

Currently `__temp_preset` sets heater targets but does not update `filament_type`. Adding this would mean that tapping a preset button (PLA/ABS/PETG) automatically updates the current filament type — the most natural place for this to happen.

---

## SetUp Screen Design Considerations

### Where to show / set the current filament type

**Option A — Dedicated "Current Filament" row on the SetUp screen**
A read-only display field showing the current filament name (e.g. "PLA+") alongside a cycle button to step through the three types. Simple; requires one new row of screen real estate.

**Option B — Highlight the active preset button**
The three existing preset buttons on the Temperature screen already call `__temp_preset` and set `filament_type`. Drive their icon colour from `get_variable("filament_type")` so the active type is visually highlighted. No new screen space needed; leverages existing infrastructure.

**Option C — Confirmation popup on the Filament screen (015)**
When the user navigates to the Load/Unload screen, compare `filament_type` against the current heater target. If they appear inconsistent (e.g. filament_type = ABS but target = 215 °C), show a popup asking the user to confirm or change the filament type before proceeding.

**Recommendation:** Implement Option B first (lowest effort, reuses existing buttons and variable). Add Option A to SetUp screen in a subsequent pass if screen space allows. Option C is a future enhancement once B is stable.

### Reminding the user to update filament type when changing filament

The printer has no sensor for "filament was physically swapped". Practical mitigations:

- **On Load/Unload completion:** Write a reminder to the message field, e.g. "Loaded — filament type still: PLA+". The user can then navigate to SetUp or tap a preset to correct it.
- **Preset button auto-update (see §4 above):** Tapping a temperature preset automatically updates `filament_type`, so the normal warm-up workflow updates the type as a side-effect at no extra cost to the user.
- **Status bar indicator:** Add a small filament-type label (e.g. "PLA") to the Home and Print Status screens so the user can see the active setting at a glance without navigating away.

---

## Implementation Order (Suggested)

| Step | What | Screen changes needed? |
|------|------|----------------------|
| 1 | Add `min_extrude` defaults to `__init__.py` constants | No |
| 2 | Add `filament_type_N_min_extrude_temp` to presets in `printer.cfg` | No |
| 3 | Add input/output vars for the new presets (vars_in / vars_out) | Yes — SetUp screen |
| 4 | Add third check to `DGUS_FILAMENT_MOVE` | No |
| 5 | Make `__temp_preset` also update `filament_type` | No |
| 6 | Add `SAVE_VARIABLE` persistence + boot-time restore | No |
| 7 | Option B — highlight active preset button on Temperature screen | Yes — Temperature screen |
| 8 | Load/Unload completion reminder message | No |
| 9 | Option A — "Current Filament" row on SetUp screen | Yes — SetUp screen |

Steps 1, 2, 4, 5, 6, and 8 are purely code-side changes with no DWIN_SET project work required.
Steps 3, 7, and 9 require coordinated screen + code changes and should be batched into a single DWIN_SET editing session.
