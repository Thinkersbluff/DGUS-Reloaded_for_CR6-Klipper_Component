# Claims Verification - v1.4.4

Source: `Development_Project_Files/Development_Environment/klippy/extras/Release Notes_v1.4.4.txt`

> Replace all placeholders below with actual URLs before release:
> - `<DWIN_ISSUE_URL_XX>`
> - `<KLIPPER_COMMIT_URL_SHA>`
> - `<KLIPPER_PR_URL_ID>`
> - `<TEST_ARTIFACT_URL>`

---

## Claim 1: Added support for the BTT Smart Filament Sensor v1.0, while retaining the stock switch sensor type as the default config.
- [x] Pre-fix behavior documented
- [x] Post-fix test steps documented
- [x] Confirmed correct operation on Dev SE
- [x] Result confirms claim
- Evidence:
  - Issue: `NA`
  - Fix commit(s): `<KLIPPER_COMMIT_URL_SHA>`
  - PR (optional): `<KLIPPER_PR_URL_ID>`
  - Test artifact (optional): `<TEST_ARTIFACT_URL>`

    ### Impact classification
    - Breaks previous DWIN-t5uid1 interface contract?
      - [ ] Yes
      - [x] No
    - Breaks previous Klipper-t5uid1 interface contract?
      - [ ] Yes
      - [x] No
   - Breaks previous Klipper-mcu interface contract?
      - [ ] Yes
      - [x] No 
    - Impacts printer_data?
      - [x] Yes
      - [ ] No
    - Changes the back-end?
      - [x] Yes
      - [ ] No
    - Changes the front-end?
      - [ ] Yes
      - [x] No

## Claim 2: Moved the filament RunoutSensor configuration into its own cfg file, according to sensor type, with an [include...] in printer.cfg.
- [x] Pre-fix behavior documented
- [x] Post-fix test steps documented
- [x] Confirmed correct operation on Dev SE
- [x] Result confirms claim
- Evidence:
  - Issue: `NA`
  - Fix commit(s): `<KLIPPER_COMMIT_URL_SHA>`
  - PR (optional): `<KLIPPER_PR_URL_ID>`
  - Test artifact (optional): `<TEST_ARTIFACT_URL>`

    ### Impact classification
    - Breaks previous DWIN-t5uid1 interface contract?
      - [ ] Yes
      - [x] No
    - Breaks previous Klipper-t5uid1 interface contract?
      - [ ] Yes
      - [x] No
    - Breaks previous Klipper-mcu interface contract?
        - [ ] Yes
        - [x] No 
    - Impacts printer_data?
      - [x] Yes
      - [ ] No
    - Changes the back-end?
      - [x] Yes
      - [ ] No
    - Changes the front-end?
      - [ ] Yes
      - [x] No

## Claim 3: Made vars_out.cfg conditional, based on which type is defined in printer.cfg.
- [x] Pre-fix behavior documented
- [x] Post-fix test steps documented
- [x] Confirmed correct operation on Dev SE
- [x] Result confirms claim
- Evidence:
  - Issue: `NA`
  - Fix commit(s): `<KLIPPER_COMMIT_URL_SHA>`
  - PR (optional): `<KLIPPER_PR_URL_ID>`
  - Test artifact (optional): `<TEST_ARTIFACT_URL>`

    ### Impact classification
    - Breaks previous DWIN-t5uid1 interface contract?
      - [ ] Yes
      - [x] No
    - Breaks previous Klipper-t5uid1 interface contract?
      - [ ] Yes
      - [x] No
   - Breaks previous Klipper-mcu interface contract?
      - [ ] Yes
      - [x] No 
    - Impacts printer_data?
      - [ ] Yes
      - [x] No
    - Changes the back-end?
      - [x] Yes
      - [ ] No
    - Changes the front-end?
      - [ ] Yes
      - [x] No

## Claim 4: #84: The Auto_Unload_After_Print function ignores the Enable/Disable Toggle Button.
- [x] Pre-fix behavior documented
- [x] Post-fix test steps documented
- [x] Confirmed correct operation on Dev SE
- [x] Result confirms claim
- Evidence:
  - Issue: `[DWIN_ISSUE_URL_84](https://github.com/Thinkersbluff/DGUS-Reloaded_for_CR6-DWIN-SET_Component/issues/84)`
  - Fix commit(s): `<KLIPPER_COMMIT_URL_SHA>`
  - PR (optional): `<KLIPPER_PR_URL_ID>`
  - Test artifact (optional): `<TEST_ARTIFACT_URL>`

    ### Impact classification
    - Breaks previous DWIN-t5uid1 interface contract?
      - [ ] Yes
      - [ ] No
    - Breaks previous Klipper-t5uid1 interface contract?
      - [ ] Yes
      - [X] No
    - Breaks previous Klipper-mcu interface contract?
      - [ ] Yes
      - [x] No 
    - Impacts printer_data?
      - [ ] Yes
      - [x] No
    - Changes the back-end?
      - [ ] Yes
      - [ ] No
    - Changes the front-end?
      - [ ] Yes
      - [ ] No

## Claim 5: #83: The display switches prematurely away showing the probing screen (checkmarks) almost immediately.
- [x] Pre-fix behavior documented
- [x] Post-fix test steps documented
- [x] Confirmed correct operation on Dev SE
- [x] Result confirms claim
- Evidence:
  - Issue: `[DWIN_ISSUE_83](https://github.com/Thinkersbluff/DGUS-Reloaded_for_CR6-DWIN-SET_Component/issues/83)`
  - Fix commit(s): `<KLIPPER_COMMIT_URL_SHA>`
  - PR (optional): `<KLIPPER_PR_URL_ID>`
  - Test artifact (optional): `<TEST_ARTIFACT_URL>`

    ### Impact classification
    - Breaks previous DWIN-t5uid1 interface contract?
      - [ ] Yes
      - [x] No
    - Breaks previous Klipper-t5uid1 interface contract?
      - [ ] Yes
      - [x] No
    - Breaks previous Klipper-mcu interface contract?
      - [ ] Yes
      - [x] No 
    - Impacts printer_data?
      - [ ] Yes
      - [x] No
    - Changes the back-end?
      - [x] Yes
      - [ ] No
    - Changes the front-end?
      - [ ] Yes
      - [x] No

## Claim 6: #81: Rotation Distance is not updating with new value.
- [x] Pre-fix behavior documented
- [x] Post-fix test steps documented
- [x] Confirmed correct operation on Dev SE
- [x] Result confirms claim
- Evidence:
  - Issue: `[DWIN_ISSUE_81](https://github.com/Thinkersbluff/DGUS-Reloaded_for_CR6-DWIN-SET_Component/issues/81)`
  - Fix commit(s): `<KLIPPER_COMMIT_URL_SHA>`
  - PR (optional): `<KLIPPER_PR_URL_ID>`
  - Test artifact (optional): `<TEST_ARTIFACT_URL>`

    ### Impact classification
    - Breaks previous DWIN-t5uid1 interface contract?
      - [ ] Yes
      - [ ] No
    - Breaks previous Klipper-t5uid1 interface contract?
      - [ ] Yes
      - [ ] No
   - Breaks previous Klipper-mcu interface contract?
      - [ ] Yes
      - [x] No 
    - Impacts printer_data?
      - [ ] Yes
      - [x] No
    - Changes the back-end?
      - [ ] Yes
      - [ ] No
    - Changes the front-end?
      - [ ] Yes
      - [ ] No

## Claim 7: #80: Change Filament Temperature Preset buttons are not responsive.
- [x] Pre-fix behavior documented
- [x] Post-fix test steps documented
- [x] Confirmed correct operation on Dev SE
- [x] Result confirms claim
- Evidence:
  - Issue: `[DWIN_ISSUE_80](https://github.com/Thinkersbluff/DGUS-Reloaded_for_CR6-DWIN-SET_Component/issues/80)`
  - Fix commit(s): `<KLIPPER_COMMIT_URL_SHA>`
  - PR (optional): `<KLIPPER_PR_URL_ID>`
  - Test artifact (optional): `<TEST_ARTIFACT_URL>`

    ### Impact classification
    - Breaks previous DWIN-t5uid1 interface contract?
      - [ ] Yes
      - [x] No
    - Breaks previous Klipper-t5uid1 interface contract?
      - [ ] Yes
      - [x] No
   - Breaks previous Klipper-mcu interface contract?
      - [ ] Yes
      - [x] No 
    - Impacts printer_data?
      - [ ] Yes
      - [x] No
    - Changes the back-end?
      - [ ] Yes
      - [x] No
    - Changes the front-end?
      - [x] Yes
      - [ ] No

## Claim 8: #79: FIRMWARE_RESTART and RESTART take so long to affect the display that one wonders whether the command is running.
- [x] Pre-fix behavior documented
- [x] Post-fix test steps documented
- [x] Confirmed correct operation on Dev SE
- [x] Result confirms claim
- Evidence:
  - Issue: `[DWIN_ISSUE_79](https://github.com/Thinkersbluff/DGUS-Reloaded_for_CR6-DWIN-SET_Component/issues/79)`
  - Fix commit(s): `<KLIPPER_COMMIT_URL_SHA>`
  - PR (optional): `<KLIPPER_PR_URL_ID>`
  - Test artifact (optional): `<TEST_ARTIFACT_URL>`

    ### Impact classification
    - Breaks previous DWIN-t5uid1 interface contract?
      - [x] Yes
      - [ ] No
    - Breaks previous Klipper-t5uid1 interface contract?
      - [ ] Yes
      - [x] No
   - Breaks previous Klipper-mcu interface contract?
      - [ ] Yes
      - [x] No 
    - Impacts printer_data?
      - [ ] Yes
      - [x] No
    - Changes the back-end?
      - [x] Yes
      - [ ] No
    - Changes the front-end?
      - [x] Yes
      - [ ] No

## Claim 9: #77: Auto Unload of filament may overspeed extruder, if Flow Rate >> 100.
- [x] Pre-fix behavior documented
- [x] Post-fix test steps documented
- [x] Confirmed correct operation on Dev SE
- [x] Result confirms claim
- Evidence:
  - Issue: `[DWIN_ISSUE_77](https://github.com/Thinkersbluff/DGUS-Reloaded_for_CR6-DWIN-SET_Component/issues/77)`
  - Fix commit(s): `<KLIPPER_COMMIT_URL_SHA>`
  - PR (optional): `<KLIPPER_PR_URL_ID>`
  - Test artifact (optional): `<TEST_ARTIFACT_URL>`

    ### Impact classification
    - Breaks previous DWIN-t5uid1 interface contract?
      - [ ] Yes
      - [x] No
    - Breaks previous Klipper-t5uid1 interface contract?
      - [ ] Yes
      - [x] No
    - Breaks previous Klipper-mcu interface contract?
      - [ ] Yes
      - [x] No 
    - Impacts printer_data?
      - [ ] Yes
      - [x] No
    - Changes the back-end?
      - [x] Yes
      - [ ] No
    - Changes the front-end?
      - [ ] Yes
      - [x] No

## Claim 10: #76: The PID menu temperature value defaults to the init_py pla constants instead of to the type1 preset values.
- [x] Pre-fix behavior documented
- [x] Post-fix test steps documented
- [x] Confirmed correct operation on Dev SE
- [x] Result confirms claim
- Evidence:
  - Issue: `[DWIN_ISSUE_76](https://github.com/Thinkersbluff/DGUS-Reloaded_for_CR6-DWIN-SET_Component/issues/76)`
  - Fix commit(s): `<KLIPPER_COMMIT_URL_SHA>`
  - PR (optional): `<KLIPPER_PR_URL_ID>`
  - Test artifact (optional): `<TEST_ARTIFACT_URL>`

    ### Impact classification
    - Breaks previous DWIN-t5uid1 interface contract?
      - [ ] Yes
      - [ ] No
    - Breaks previous Klipper-t5uid1 interface contract?
      - [ ] Yes
      - [x] No
    - Breaks previous Klipper-mcu interface contract?
      - [ ] Yes
      - [x] No 
    - Impacts printer_data?
      - [ ] Yes
      - [ ] No
    - Changes the back-end?
      - [x] Yes
      - [ ] No
    - Changes the front-end?
      - [ ] Yes
      - [x] No

## Claim 11: #75: Updating the displayed State of RUNOUT_SENSOR and of AUTO_UNLOAD_FILAMENT_AFTER_PRINT sometimes takes up to 2 seconds.
- [x] Pre-fix behavior documented
- [x] Post-fix test steps documented
- [x] Confirmed correct operation on Dev SE
- [x] Result confirms claim
- Evidence:
  - Issue: `[DWIN_ISSUE_75](https://github.com/Thinkersbluff/DGUS-Reloaded_for_CR6-DWIN-SET_Component/issues/75)`
  - Fix commit(s): `<KLIPPER_COMMIT_URL_SHA>`
  - PR (optional): `<KLIPPER_PR_URL_ID>`
  - Test artifact (optional): `<TEST_ARTIFACT_URL>`

    ### Impact classification
    - Breaks previous DWIN-t5uid1 interface contract?
      - [ ] Yes
      - [ ] No
    - Breaks previous Klipper-t5uid1 interface contract?
      - [ ] Yes
      - [x] No
    - Breaks previous Klipper-mcu interface contract?
      - [ ] Yes
      - [x] No 
    - Impacts printer_data?
      - [ ] Yes
      - [ ] No
    - Changes the back-end?
      - [ ] Yes
      - [ ] No
    - Changes the front-end?
      - [ ] Yes
      - [ ] No

## Claim 12: #85: MCU 'mcu' has deprecated code (it is missing feature 'STEPPER_STEP_BOTH_EDGE').
- [x] Pre-fix behavior documented
- [x] Post-fix test steps documented
- [x] Confirmed correct operation on Dev SE
- [x] Result confirms claim
- Evidence:
  - Issue: `[DWIN_ISSUE_85](https://github.com/Thinkersbluff/DGUS-Reloaded_for_CR6-DWIN-SET_Component/issues/85)`
  - Fix commit(s): `<KLIPPER_COMMIT_URL_SHA>`
  - PR (optional): `<KLIPPER_PR_URL_ID>`
  - Test artifact (optional): `<TEST_ARTIFACT_URL>`

    ### Impact classification
    - Breaks previous DWIN-t5uid1 interface contract?
      - [ ] Yes
      - [x] No
    - Breaks previous Klipper-t5uid1 interface contract?
      - [ ] Yes
      - [x] No
    - Breaks previous Klipper-mcu interface contract?
      - [x] Yes
      - [ ] No 
    - Impacts printer_data?
      - [x] Yes
      - [ ] No
    - Changes the back-end?
      - [x] Yes
      - [ ] No
    - Changes the front-end?
      - [ ] Yes
      - [x] No

## Claim 13: #86: MCU 'mcu' has deprecated code (it is missing feature 'STEPPER_STEP_BOTH_EDGE').
- [x] Pre-fix behavior documented
- [x] Post-fix test steps documented
- [x] Confirmed correct operation on Dev SE
- [x] Result confirms claim
- Evidence:
  - Issue: `[DWIN_ISSUE_86](https://github.com/Thinkersbluff/DGUS-Reloaded_for_CR6-DWIN-SET_Component/issues/86)`
  - Fix commit(s): `<KLIPPER_COMMIT_URL_SHA>`
  - PR (optional): `<KLIPPER_PR_URL_ID>`
  - Test artifact (optional): `<TEST_ARTIFACT_URL>`

    ### Impact classification
    - Breaks previous DWIN-t5uid1 interface contract?
      - [ ] Yes
      - [x] No
    - Breaks previous Klipper-t5uid1 interface contract?
      - [ ] Yes
      - [x] No
   - Breaks previous Klipper-mcu interface contract?
      - [x] Yes
      - [ ] No 
    - Impacts printer_data?
      - [ ] Yes
      - [x] No
    - Changes the back-end?
      - [x] Yes
      - [ ] No
    - Changes the front-end?
      - [ ] Yes
      - [x] No

## Claim 14: #87: Pressing the Preset buttons does not change the nozzle or bed temperatures on the Manage Heaters page.
- [x] Pre-fix behavior documented
- [x] Post-fix test steps documented
- [x] Confirmed correct operation on Dev SE
- [x] Result confirms claim
- Evidence:
  - Issue: `[DWIN_ISSUE_87](https://github.com/Thinkersbluff/DGUS-Reloaded_for_CR6-DWIN-SET_Component/issues/87)`
  - Fix commit(s): `<KLIPPER_COMMIT_URL_SHA>`
  - PR (optional): `<KLIPPER_PR_URL_ID>`
  - Test artifact (optional): `<TEST_ARTIFACT_URL>`

    ### Impact classification
    - Breaks previous DWIN-t5uid1 interface contract?
      - [ ] Yes
      - [x] No
    - Breaks previous Klipper-t5uid1 interface contract?
      - [ ] Yes
      - [x] No
    - Breaks previous Klipper-mcu interface contract?
      - [ ] Yes
      - [x] No 
    - Impacts printer_data?
      - [ ] Yes
      - [x] No
    - Changes the back-end?
      - [ ] Yes
      - [ ] No
    - Changes the front-end?
      - [x] Yes
      - [ ] No