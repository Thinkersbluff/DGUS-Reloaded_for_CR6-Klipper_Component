DGUS T5UID1 upstream integration files

This folder contains the files needed to add the DGUS T5UID1 full-stack support
to an upstream Klipper repository (minimal set for STM32 + host extras).

How to apply:

1. Copy the files from this folder into the upstream klipper tree preserving paths.

2. Edit `src/stm32/Makefile` and add the line (near other include lines):

    include src/stm32/t5uid1/Makefile

3. Edit `src/stm32/Kconfig` and add the line (near other source lines):

    source "src/stm32/t5uid1/Kconfig"

4. Add the new files:
  - src/generic/t5uid1/serial_irq.h
  - src/generic/t5uid1/serial_irq.c
  - src/stm32/t5uid1/serial.c
  - src/stm32/t5uid1/Makefile
  - src/stm32/t5uid1/Kconfig

Note: This package is intentionally minimal — it implements the MCU-side
generic IRQ handler and an STM32 UART glue file (with several pin choices),
plus the Python extras. If you support additional architectures, add `src/<arch>/t5uid1` accordingly.
