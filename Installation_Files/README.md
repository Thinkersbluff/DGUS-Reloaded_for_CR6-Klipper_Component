Last Updated: 7 March 2026

# Installation_Files - DGUS-Reloaded for CR6 - Klipper Component

This folder organizes and provides the files that enable you to extend an existing Klipper3D + Mainsail system with the "back-end" of the DGUS-Reloaded for CR6 system.

Once this back-end is installed and operating, the user can flash the [DGUS-Reloaded for CR6 - DWIN_SET Component](https://github.com/Thinkersbluff/DGUS-Reloaded_for_CR6-DWIN-SET_Component) to the CR6 stock touchscreen display, restoring your ability to monitor and control your Klipper-based CR6 printer directly from the stock display.

---

## Overview

- [Installation_Help_Docs](1-Installation_Help_Docs/)  
    Guidelines detailing the suggested installation process; either manual or scripted.  
--
- [DGUS-Reloaded for CR6 Add-on](2-DGUS-Reloaded_Add-on/)   
    Klipper does not explicitly support "add-ons" or "extensions", but it does find and run python applications installed in the ~klipper/klippy/extras folder and it does expose various macros and state variables to these applications, at runtime.  
    To "install" these DGUS-Reloaded for CR6 python modules and configuration files, copy the folder klippy/extras/t5uid1 and its contents to klippy/extras on your Klipper3D host. Klippy will then process the t5uid1/_init_.py at boot time, and these files will collectively implement the DGUS-Reloaded for CR6 "back-end."  
--
- [Custom_Klipper+Mainsail_Files](3-Custom_Klipper%2BMainsail_Files/)  
    Both Klipper and Mainsail rely on various text files, to control their behaviour.  This folder provides a set of these files, pre-configured for each of the four supported CR6 motherboards.
    You will need to edit/tailor some of these files (e.g. printer.cfg), to function correctly with your printer.  This need for tailoring can be a little "intimidating" for new users.  I have done my best to annotate those files which are most likely to require edits and have often included reasonable starting values for you.
    If you need advice or clarification, do not hesitate to engage me in the Discussions forum.  
--
- [klipper.bin_files](4-klipper.bin_files/)  
    A pre-compiled binary to flash to the BTT or the Creality motherboard in your printer.  This version replaces the Klipper3D klipper.bin file and adds full-stack communications support between Klipper and the stock display.  
 -- 
- [make_menuconfig_Extensions/klipper](make_menuconfig_Extensions/klipper/)  
    The Klipper3D developers provide [extensive guidance for installation and configuration of their firmware, online](https://www.klipper3d.org/), so I will not try to repeat or paraphrase that guidance here.
    I will mention, though, that the klipper.bin_files I provide should make it unnecessary to follow the Klipper3D instructions for making and flashing your own klipper.bin file.
    The one exception to that will be when the Klipper3D developers make changes to the functionality of their mcu.py module.  In those cases, you will need to install these extensions before performing the make menuconfig step in their build process.
---
# Full Disclosure:
  I use this firmware as my "daily-driver" on my Kickstarter CR6-SE.  
  I also run KlipperScreen on a 7" touchscreen tablet, and I run Mainsail on a Linux PC on a laptop located just beside my printer.  
  I very rarely interact with KlipperScreen, but I do need to use either Klipperscreen or Mainsail to run Firmware Restart, after power-cycling the printer, to activate the stock display.  That is the one objectionable limitation I have not (yet?) overcome, with this system.