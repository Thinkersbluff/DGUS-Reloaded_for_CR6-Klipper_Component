Last Updated: 7 March 2026

# Introduction

This folder contains the files needed to add the DGUS T5UID1 full-stack support
to a Klipper3D repository (minimal set for CR6 printers: STM32 motherboard + stock display).

## How to install these [make menuconfig] extensions:

1. Copy these files from this folder into the klipper3D tree, preserving these paths:
  - klipper/src/generic/t5uid1/serial_irq.h
  - klipper/src/generic/t5uid1/serial_irq.c
  - klipper/src/stm32/t5uid1/serial.c
  - klipper/src/stm32/t5uid1/stm32_serial.h


2. Edit `src/stm32/Makefile` and add this line (at the bottom of the file):

    include src/stm32/t5uid1/Makefile
		See example at klipper/src/stm32/t5uid1/Makefile

3. Edit `src/stm32/Kconfig` and add this line (at the bottom of the file, just above 'endif'):

    source "src/stm32/t5uid1/Kconfig"
		See example at klipper/src/stm32/t5uid1/Kconfig

# CAUTION: Don't be "dirty"
The Moonraker application will "insult" your Klipper installation, once you modify Kconfig and/or Makefile, appending the string "-dirty" to the version number.  This same "insult" will appear in the Mainsail MACHINE tab window "System Loads".  If a Klipper update is released, you will actually need to revert those two files, before Moonraker will allow you to apply the update.

To work around this issue, I recommend that you use the manage_t5uid1_patches.sh script to revert the two files immediately after you successfully flash the new klipper.bin file.  (That way, you are less likely to forget how to restore the ability to apply the next update.)

## Revert the two files like this:
SSH into your Klipper host at copy/paste this instruction:
```
cd ~/klipper/scripts/dgus-reloaded 
./manage_t5uid1_patches.sh prepare
```
This does not remove the "insult" from the System Loads window, but it does cause Moonraker to remove the dirty flag from Klipper in the Update Manager, allowing you to apply the update.  
---

# WARNING:  Always backup your Klipper System before applying updates, in case you need to roll-back the update!!

There, I remembered to warn you, even if I always forget, myself...

See [4-Backup_Restore_Klipper.md](../1-Installation_Help_Docs/4-Backup_Restore_Klipper.md) for guidance on how to backup and restore the full klipper tree.

---

## If Updated Klipper throws an "mcu" error
If the update you apply makes the current klipper incompatible with the current klipper.bin file, you will need to reapply those edits to KConfig and Makefile, and build/flash a new klipper.bin, like this:

1. SSH into your Klipper host 
2. copy/paste this instruction, to edit KConfig and Makefile:
```
cd ~/klipper/scripts/dgus-reloaded 
./manage_t5uid1_patches.sh reapply
```
3. copy/paste this instruction, to build a new klipper.bin file:
```
cd ~klipper
make menuconfig
```
4. Verify that the settings match the current motherboard
5. Quit menuconfig (Q, then Y to save changes, if any)
6. copy/paste this instruction:
```
make clean
make
```
7. Flash the new klipper.bin file to your printer motherboard.

## If Updated Klipper throws an error against a DGUS-Reloaded Module
If Klipper throws an error against a DGUS-Reloaded module (e.g. [t5uid1]), the Klipper update may have refactored one or more function that the current DGUS-Reloaded code is calling.  
This kind of problem will usually require a code fix from me.
In the short-term, your only option may be to roll-back the last update, or to deliberately overwrite the klipper tree from a previously working commit#.


## Note: 
This extensions package is intentionally minimal — it implements the MCU-side
generic IRQ handler and an STM32 UART glue file ONLY for the STM32f103 processor, and ONLY for the four CR6 motherboards supported by DGUS-Reloaded for CR6.  
If you wish to support additional architectures, you will need to add the applicable `src/<arch>/t5uid1` files yourself.  
You may find helpful examples from Desuuu in the Reference Only folder.
