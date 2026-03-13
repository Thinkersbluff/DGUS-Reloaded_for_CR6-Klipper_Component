# Claims Verification - v1.4.4

Source: `Development_Project_Files/Development_Environment/klippy/extras/Release Notes_v1.4.4.txt`

> Replace all placeholders below with actual URLs before release:
> - `<DWIN_ISSUE_URL_XX>`
> - `<KLIPPER_COMMIT_URL_SHA>`
> - `<TEST_ARTIFACT_URL>`

---

## Claim 1: Added support for the BTT Smart Filament Sensor v1.0, while retaining the stock switch sensor type as the default config.
- [x] Pre-fix behavior documented
- [x] Post-fix test steps documented
- [x] Confirmed correct operation on Dev SE
- [x] Result confirms claim
- Evidence:
  - Issue: `https://github.com/Thinkersbluff/DGUS-Reloaded_for_CR6-DWIN-SET_Component/issues/89`
  - Test artifact (optional): `NA`

    ### Impact classification
    - Impacts printer_data?
      - [x] Yes
        - Fix commit(s): `https://github.com/Thinkersbluff/DGUS-Reloaded_for_CR6-Klipper_Component/commit/d720e510ddfbdcb0bdd8ee9b16f89a1c3483222b`
      - [ ] No
    - Changes t5uid1 extras?
      - [x] Yes
        - Fix commit(s): `https://github.com/Thinkersbluff/DGUS-Reloaded_for_CR6-Klipper_Component/commit/d720e510ddfbdcb0bdd8ee9b16f89a1c3483222b`
    - Changes klipper.bin?
      - [ ] Yes
        - Fix commit(s):
      - [x] No
    - Changes klipper/src?
      - [ ] Yes
        - Fix commit(s):
      - [x] No
    - Changes DWIN_SET?
      - [ ] Yes
        - Fix commit(s):
      - [x] No

## Claim 2: #86: 'MCU' object has no attribute 'register_response'.
- [x] Pre-fix behavior documented
- [x] Post-fix test steps documented
- [x] Confirmed correct operation on Dev SE
- [x] Result confirms claim
- Evidence:
  - Issue: `https://github.com/Thinkersbluff/DGUS-Reloaded_for_CR6-DWIN-SET_Component/issues/86`
  - Test artifact (optional): `NA`

    ### Impact classification
    - Impacts printer_data?
      - [ ] Yes
        - Fix commit(s):
      - [x] No
    - Changes t5uid1 extras?
      - [x] Yes
        - Fix commit(s): `https://github.com/Thinkersbluff/DGUS-Reloaded_for_CR6-Klipper_Component/commit/4d85b53c425a62600bdf23047be545cd144e2fab`
      - [ ] No
    - Changes klipper.bin?
      - [ ] Yes
        - Fix commit(s):
      - [x] No
    - Changes klipper/src?
      - [ ] Yes
        - Fix commit(s):
      - [x] No
    - Changes DWIN_SET?
      - [ ] Yes
        - Fix commit(s):
      - [x] No

## Claim 3: #87: Pressing the Preset buttons does not change the nozzle or bed temperatures on the Manage Heaters page.
- [x] Pre-fix behavior documented
- [x] Post-fix test steps documented
- [x] Confirmed correct operation on Dev SE
- [x] Result confirms claim
- Evidence:
  - Issue: `https://github.com/Thinkersbluff/DGUS-Reloaded_for_CR6-DWIN-SET_Component/issues/87`
  - Test artifact (optional): `NA`

    ### Impact classification
    - Impacts printer_data?
      - [ ] Yes
        - Fix commit(s):
      - [x] No
    - Changes t5uid1 extras?
      - [ ] Yes
        - Fix commit(s):
      - [x] No
    - Changes klipper.bin?
      - [ ] Yes
        - Fix commit(s):
      - [x] No
    - Changes klipper/src?
      - [ ] Yes
        - Fix commit(s):
      - [x] No
    - Changes DWIN_SET?
      - [x] Yes
        - Fix commit(s): `https://github.com/Thinkersbluff/DGUS-Reloaded_for_CR6-DWIN-SET_Component/pull/88`
      - [ ] No

## Claim 4: #84: The Auto_Unload_After_Print function ignores the Enable/Disable Toggle Button.
- [x] Pre-fix behavior documented
- [x] Post-fix test steps documented
- [x] Confirmed correct operation on Dev SE
- [x] Result confirms claim
- Evidence:
  - Issue: `https://github.com/Thinkersbluff/DGUS-Reloaded_for_CR6-DWIN-SET_Component/issues/84`
  - Test artifact (optional):`NA`

    ### Impact classification
    - Impacts printer_data?
      - [ ] Yes
        - Fix commit(s):
      - [x] No
    - Changes t5uid1 extras?
      - [x] Yes
        - Fix commit(s): `https://github.com/Thinkersbluff/DGUS-Reloaded_for_CR6-Klipper_Component/commit/0ff135a9ec98e9be798e9849522b9b7a1c3c6ea0`
      - [ ] No
    - Changes klipper.bin?
      - [ ] Yes
        - Fix commit(s):
      - [x] No
    - Changes klipper/src?
      - [ ] Yes
        - Fix commit(s):
      - [x] No
    - Changes DWIN_SET?
      - [x] Yes
        - Fix commit(s): `https://github.com/Thinkersbluff/DGUS-Reloaded_for_CR6-DWIN-SET_Component/commit/0ba0f246f7459c471c9fbbe1ad433cc1372e956f`
      - [ ] No

## Claim 5: #83: The display switches prematurely away showing the probing screen (checkmarks) almost immediately.
- [x] Pre-fix behavior documented
- [x] Post-fix test steps documented
- [x] Confirmed correct operation on Dev SE
- [x] Result confirms claim
- Evidence:
  - Issue: `https://github.com/Thinkersbluff/DGUS-Reloaded_for_CR6-DWIN-SET_Component/issues/83`
  - Test artifact (optional): `NA`

    ### Impact classification
    - Impacts printer_data?
      - [ ] Yes
        - Fix commit(s):
      - [x] No
    - Changes t5uid1 extras?
      - [x] Yes
        - Fix commit(s): `https://github.com/Thinkersbluff/DGUS-Reloaded_for_CR6-Klipper_Component/commit/61d8cc538f9239a891cd0b1e70f00e25f15b8b6f`
      - [ ] No
    - Changes klipper.bin?
      - [ ] Yes
        - Fix commit(s):
      - [x] No
    - Changes klipper/src?
      - [ ] Yes
        - Fix commit(s):
      - [x] No
    - Changes DWIN_SET?
      - [ ] Yes
        - Fix commit(s):
      - [x] No

## Claim 6: #81: Rotation Distance is not updating with new value.
- [x] Pre-fix behavior documented
- [x] Post-fix test steps documented
- [x] Confirmed correct operation on Dev SE
- [x] Result confirms claim
- Evidence:
  - Issue: `https://github.com/Thinkersbluff/DGUS-Reloaded_for_CR6-DWIN-SET_Component/issues/81`
  - Test artifact (optional): `NA`

    ### Impact classification
    - Impacts printer_data?
      - [ ] Yes
        - Fix commit(s):
      - [x] No
    - Changes t5uid1 extras?
      - [x] Yes
        - Fix commit(s): `https://github.com/Thinkersbluff/DGUS-Reloaded_for_CR6-Klipper_Component/commit/7a415cee68b4f71bc7b39662cb5b3063905ae5b1`
      - [ ] No
    - Changes klipper.bin?
      - [ ] Yes
        - Fix commit(s):
      - [x] No
    - Changes klipper/src?
      - [ ] Yes
        - Fix commit(s):
      - [x] No
    - Changes DWIN_SET?
      - [ ] Yes
        - Fix commit(s):
      - [x] No

## Claim 7: #80: Change Filament Temperature Preset buttons are not responsive.
- [x] Pre-fix behavior documented
- [x] Post-fix test steps documented
- [x] Confirmed correct operation on Dev SE
- [x] Result confirms claim
- Evidence:
  - Issue: `https://github.com/Thinkersbluff/DGUS-Reloaded_for_CR6-DWIN-SET_Component/issues/80`
  - Test artifact (optional): `NA`

    ### Impact classification
    - Impacts printer_data?
      - [ ] Yes
        - Fix commit(s):
      - [x] No
    - Changes t5uid1 extras?
      - [ ] Yes
        - Fix commit(s):
      - [x] No
    - Changes klipper.bin?
      - [ ] Yes
        - Fix commit(s):
      - [x] No
    - Changes klipper/src?
      - [ ] Yes
        - Fix commit(s):
      - [x] No
    - Changes DWIN_SET?
      - [x] Yes
        - Fix commit(s): `https://github.com/Thinkersbluff/DGUS-Reloaded_for_CR6-DWIN-SET_Component/commit/71e1d5624cf3ab7897ffcf52a748a8115666fc5a#diff-531f81928bfe7db57e33a48c7e126d0cd2ddc2d056ef177ae882cc6eea5aa3a3`
      - [ ] No

## Claim 8: #79: FIRMWARE_RESTART and RESTART take so long to affect the display that one wonders whether the command is running.
- [x] Pre-fix behavior documented
- [x] Post-fix test steps documented
- [x] Confirmed correct operation on Dev SE
- [x] Result confirms claim
- Evidence:
  - Issue: `[DWIN_ISSUE_79](https://github.com/Thinkersbluff/DGUS-Reloaded_for_CR6-DWIN-SET_Component/issues/79)`
  - Test artifact (optional): `<TEST_ARTIFACT_URL>`

    ### Impact classification
    - Impacts printer_data?
      - [ ] Yes
        - Fix commit(s):
      - [x] No
    - Changes t5uid1 extras?
      - [x] Yes
        - Fix commit(s): `https://github.com/Thinkersbluff/DGUS-Reloaded_for_CR6-Klipper_Component/commit/fc5266169383e83bf123b8b069eb83a8f549fac0`
      - [ ] No
    - Changes klipper.bin?
      - [ ] Yes
        - Fix commit(s):
      - [x] No
    - Changes klipper/src?
      - [ ] Yes
        - Fix commit(s):
      - [x] No
    - Changes DWIN_SET?
      - [ ] Yes
        - Fix commit(s):
      - [x] No

## Claim 9: #77: Auto Unload of filament may overspeed extruder, if Flow Rate >> 100.
- [x] Pre-fix behavior documented
- [x] Post-fix test steps documented
- [x] Confirmed correct operation on Dev SE
- [x] Result confirms claim
- Evidence:
  - Issue: `https://github.com/Thinkersbluff/DGUS-Reloaded_for_CR6-DWIN-SET_Component/issues/77`
  - Test artifact (optional): `NA`

    ### Impact classification
    - Impacts printer_data?
      - [x] Yes
        - Fix commit(s): `https://github.com/Thinkersbluff/DGUS-Reloaded_for_CR6-Klipper_Component/commit/6b12dab07d0b54a24e4f3279c42b29d4ee35647d`
      - [ ] No
    - Changes t5uid1 extras?
      - [ ] Yes
        - Fix commit(s):
      - [x] No
    - Changes klipper.bin?
      - [ ] Yes
        - Fix commit(s):
      - [x] No
    - Changes klipper/src?
      - [ ] Yes
        - Fix commit(s):
      - [x] No
    - Changes DWIN_SET?
      - [ ] Yes
        - Fix commit(s):
      - [x] No

## Claim 10: #76: The PID menu temperature value defaults to the init_py pla constants instead of to the type1 preset values.
- [x] Pre-fix behavior documented
- [x] Post-fix test steps documented
- [x] Confirmed correct operation on Dev SE
- [x] Result confirms claim
- Evidence:
  - Issue: `[DWIN_ISSUE_76](https://github.com/Thinkersbluff/DGUS-Reloaded_for_CR6-DWIN-SET_Component/issues/76)`
  - Test artifact (optional): `NA`

    ### Impact classification
    - Impacts printer_data?
      - [ ] Yes
        - Fix commit(s):
      - [x] No
    - Changes t5uid1 extras?
      - [x] Yes
        - Fix commit(s): `https://github.com/Thinkersbluff/DGUS-Reloaded_for_CR6-Klipper_Component/commit/9ac431310fe3b32f21f9b913b80dd0a42a175b6e`
      - [ ] No
    - Changes klipper.bin?
      - [ ] Yes
        - Fix commit(s):
      - [x] No
    - Changes klipper/src?
      - [ ] Yes
        - Fix commit(s):
      - [x] No
    - Changes DWIN_SET?
      - [ ] Yes
        - Fix commit(s):
      - [x] No

## Claim 11: #85: MCU 'mcu' has deprecated code (it is missing feature 'STEPPER_STEP_BOTH_EDGE').
- [x] Pre-fix behavior documented
- [x] Post-fix test steps documented
- [x] Confirmed correct operation on Dev SE
- [x] Result confirms claim
- Evidence:
  - Issue: `https://github.com/Thinkersbluff/DGUS-Reloaded_for_CR6-DWIN-SET_Component/issues/85`
  - Test artifact (optional): `NA`

    ### Impact classification
    - Impacts printer_data?
      - [ ] Yes
        - Fix commit(s):
      - [x] No
    - Changes t5uid1 extras?
      - [ ] Yes
        - Fix commit(s):
      - [x] No
    - Changes klipper.bin?
      - [x] Yes
        - Fix commit(s): `https://github.com/Thinkersbluff/DGUS-Reloaded_for_CR6-Klipper_Component/commit/5096dcd9ba36f648abf806d7b1cb633cc995ad11`
      - [ ] No
    - Changes klipper/src?
      - [ ] Yes
        - Fix commit(s):
      - [x] No
    - Changes DWIN_SET?
      - [ ] Yes
        - Fix commit(s):
      - [x] No




