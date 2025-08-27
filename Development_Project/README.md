This PROJECT folder contains the python libraries which collectively constitute the DGUS-ReloadedForCR6 Klipper component.

**The t5uid1.py application imports and uses two files from klipper/klippy/extras:**
    - gcode_macro.py and 
    - heaters.py
    - 
Copies of those files are included here, to enable the import lines to work in this repository without throwing linting errors, and to support troubleshooting future changes, but **they do NOT form a part of the distribution package.**

The **KlipperFiles_ReferenceOnly** folder contains the Klipper files as they were last pulled into the repository.  They form an historical snapshot of the code, for reference in the event of bugs introduced by future changes. They **do NOT form a part of the distribution package.**