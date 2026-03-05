# make menuconfig Extensions to Integrate DGUS-Reloaded for CR6 (t5uid1) - DWIN Component With Klipper3D


This folder contains the files needed to add the DGUS T5UID1 full-stack support
to a Klipper3D repository (minimal set for CR6 printers: STM32 motherboard + stock display).

## PLEASE NOTE:
Before you try to install these [make menuconfig] extensions, I strongly recommend that you complete the first three steps in this sequence:

  1. First, install and configure Klipper3D on your host, and get it working with either Mainsail or Fluidd.
       Our friend KoenVanduffel [aka @K2Van on the CR6Community Discord] provides this very accessible guide to that process, specifically for CR6 users: https://github.com/KoenVanduffel/CR-6_Klipper.

  2. Then apply and calibrate the DGUS-Reloaded For CR6 - klippy_extras_Extensions.
     I offer guidance on how to do that, here in the ReadMe file:  https://github.com/Thinkersbluff/DGUS-Reloaded_for_CR6-Klipper_Component. 
     If, after completing this step, you do not see any errors or notifications requiring that you rebuild the MCU klipper.bin file, then applying the [make menuconfig] extensions is optional, until some future Klipper3D flags a problem.
     You can instead safely proceed directly to step 4.

  3. If Klipper does report a problem with MCU klipper.bin after completing step 2 (e.g.: MCU 'mcu' has deprecated code (it is missing feature 'STEPPER_STEP_BOTH_EDGE'), 
     then you do need to install these extensions, as described below.  Then use 'make menuconfig and make' to build and flash a new klipper.bin file to your motherboard.`

  4. Flash to your stock display the DGUS-Related For CR6 component that matches the Klipper component you installed at step 2.


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


## Note: 
This extensions package is intentionally minimal — it implements the MCU-side
generic IRQ handler and an STM32 UART glue file ONLY for the STM32f103 processor,
and ONLY for the four CR6 motherboards supported by DGUS-Reloaded for CR6. 
If you wish to support additional architectures, you will need to add the applicable `src/<arch>/t5uid1` files yourself.
You may find helpful examples from Desuuu in the Reference Only folder.
