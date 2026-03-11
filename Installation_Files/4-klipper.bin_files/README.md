Last Updated: 7 March 2026.

# Introduction

The Klipper3D.org documentation advises you to build and flash a klipper.bin file to your printer's motherboard, as part of the standard Klipper installation process.  
If you already have Klipper and Mainsail installed on your printer, as recommended, then you already did that at least once.

What makes DGUS-Reloaded for CR6 unique - and what allows Klipper and the stock CR6 DGUS/DWIN display to interact - is that we add full-stack support for the  serial interface between the motherboard and the display into the klipper.bin file.  

How we do that is documented in the installation help doc, "Rebuilding_MCU_Firmware.md"

Whether we need to do that depends on whether the applicable klipper.bin file in this folder works with the current version of Klipper installed on your system.

i.e. This folder provides a pre-built klipper.bin file that may save you the step of running make menuconfig and make, yourself.

Try flashing this file first.  
- If Klipper boots up without issue, your display will work when you install the DWIN component of DGUS-Reloaded for CR6.
- If Klipper throws one or more error referencing 'mcu', try building and flashing a new klipper.bin file, to see whether it fixes it.
- If Klipper throws one or more error even after flashing your custom klipper.bin, you may need to roll-back and wait for an update to this firmware.  
  [You did make a backup before updating Klipper, right??  [Yeah, me neither  ;( ]]