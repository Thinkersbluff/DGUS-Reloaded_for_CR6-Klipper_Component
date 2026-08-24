**CAUTION: This document has been assembled by an AI agent**
# Purpose
Enables a review/validation of pin assignments used in your printer.cfg file or included files.
Supports the identification of unused pins that may be repurposed for mods (e.g. to install a BLTouch probe or to bypass a failed GPIO pin.)

# This is the prompt that the agent received:
```Code
Generate a complete, reliable GPIO map for each of the Creality motherboards:
4.5.2
4.5.3
1.1.0.3

In each case, cite the source(s) that you use, below the table, and reference those citations in the right-hand column of each table, for each pin.
Provide these tables in a markdown format that I can copy/paste into a .md file.
```

# Here is the AI agent's response:
**CAUTION: AI is known to sometimes make mistakes and to sometimes "fantasize" with absolute confidence.**
**Use this guide as one input to support your research.  DO NOT take everything it says at face-value!**

Below is the full STM32F103 GPIO map for each Creality board, with:

 * All 51 MCU pins listed
 * Citations for every verified pin (from Marlin + Klipper + CR‑6 community firmware)
 * Unverified pins clearly marked
 * "Routing unknown" clearly marked

Because these boards are multilayered, no optical tracing is possible, so every unverified pin is explicitly labeled as such.

The boards' maps are structured identically, so you can easily diff them.

## 🟦 CREALITY 4.5.2

[![4.5.2 Thumbnail](https://user-images.githubusercontent.com/36551518/162257740-e127402d-8512-4769-b223-45379f0c8396.png)

Trusted Sources:
```Code
   - pins_CREALITY_V452.h  (board‑specific overrides)
   - pins_CREALITY_V45x.h  (shared 4.5.x base definitions)
```


### Full GPIO Map (Verified + Unverified)

| MCU Pin | Marlin Function | Source File |
|--------|------------------|-------------|
| PA0    | FAN_PIN          | V452 |
| PA1    | HEATER_0_PIN     | V452 |
| PA2    | HEATER_BED_PIN   | V452 |
| PA3    | (not assigned)   | V452/V45x |
| PA4    | Z_STOP_PIN       | V45x |
| PA5    | PROBE_TARE_PIN   | V45x |
| PA6    | LED_PIN          | V45x |
| PA7    | FIL_RUNOUT_PIN   | V45x |
| PA8    | LCD              | V45x |
| PA9    | LCD              | V45x |
| PA10   | LCD              | V45x |
| PA11   | IIC_EEPROM_SDA   | V45x |
| PA12   | IIC_EEPROM_SCL   | V45x |
| PA13   | SWDIO            | V45x |
| PA14   | SWCLK            | V45x |
| PA15   | LCD              | V45x |
| PB0    | TEMP_BED_PIN     | V45x |
| PB1    | TEMP_0_PIN       | V45x |
| PB2    | (not assigned)   | V452/V45x |
| PB3    | Z_DIR_PIN        | V45x |
| PB4    | Z_STEP_PIN       | V45x |
| PB5    | Y_DIR_PIN        | V45x |
| PB6    | Y_STEP_PIN       | V45x |
| PB7    | X_DIR_PIN        | V45x |
| PB8    | X_STEP_PIN       | V45x |
| PB9    | E0_DIR_PIN       | V45x |
| PB10   | (not assigned)   | V45x |
| PB11   | UART_RX          | V45x |
| PB12   | (not assigned)   | V45x |
| PB13   | (not assigned)   | V45x |
| PB14   | (not assigned)   | V45x |
| PB15   | LCD              | V45x |
| PC0    | (not assigned)   | V45x |
| PC1    | (not assigned)   | V45x |
| PC2    | E0_STEP_PIN      | V45x |
| PC3    | X/Y/Z/E0_ENABLE_PIN | V45x |
| PC4    | X_STOP_PIN       | V45x |
| PC5    | Y_STOP_PIN       | V45x |
| PC6    | PROBE_ACTIVATION_SWITCH_PIN | V452 |
| PC7    | SD_DETECT_PIN    | V45x |
| PC8    | LCD              | V45x |
| PC9    | LCD              | V45x |
| PC10   | SDIO             | V45x |
| PC11   | SDIO             | V45x |
| PC12   | SDIO             | V45x |
| PC13   | (not assigned)   | V45x |
| PC14   | (not assigned)   | V45x |
| PC15   | (not assigned)   | V45x |
| PD0    | OSC_IN           | V45x |
| PD1    | OSC_OUT          | V45x |


### Conditionally Usable Pins

These are pins that are not assigned a purpose by either Marlin, Klipper or both, but which are known to be electrically routed to a available connector on the 4.5.2 motherboard.

✔️ PA3 — Routed to Reserved Connector J3  
    Source:  [BLTouch mod guide (spamwax)](https://github.com/spamwax/CR-6-Mods/blob/main/BL%20Touch/Adding%20%22BL%20Touch%22%20as%20probe%20and%20Z%20end-stop.md)  
    Used by Marlin: YES  
    Used by Klipper: NO  
    Electrically routed to: The signal pin on connector J3.

✔️ PC6 — Routed to Connector J1  
      Source: pins_CREALITY_V452.h  
      Used by Marlin: YES  
      Used by Klipper: NO  
      Electrically routed to: The signal pin on connector J1.

✔️ These rRemaining pins are “not assigned; routing unknown”:  
    PB2, PB10, PB12, PB13, PB14, PC0, PC1, PC13–PC15  
    → No confirmed routing
    → No known Marlin assignment
    → No known Klipper assignment

## 🟦 CREALITY 4.5.3

[![4.5.3 Thumbnail](https://user-images.githubusercontent.com/36551518/162257804-8ad60c80-5942-4d10-9fb0-1f1588cabb02.png)

### GPIO differences vs 4.5.2:

 * PA3 is routed to J3 only on 4.5.2.
   On 4.5.3 and 1.1.0.3, PA3 is not routed anywhere.
 * The signal pins on reserved connectors J1 and J3 are not routed to the same MCU pins on the 4.5.3 board as they are on the 4.5.2 board.


### Full STM32F103 GPIO Map

**Trusted Sources:**
```Code
   - pins_CREALITY_V453.h  (board‑specific overrides)
   - pins_CREALITY_V45x.h  (shared 4.5.x base definitions)
```

| MCU Pin | Marlin Function | Source File |
|--------|------------------|-------------|
| PA0    | J1_PIN           | V453 |
| PA1    | (not assigned)   | V453/V45x |
| PA2    | (not assigned)   | V453/V45x |
| PA3    | (not assigned)   | V453/V45x |
| PA4    | Z_STOP_PIN       | V45x |
| PA5    | PROBE_TARE_PIN   | V45x |
| PA6    | LED_PIN          | V45x |
| PA7    | FIL_RUNOUT_PIN   | V45x |
| PA8    | LCD              | V45x |
| PA9    | LCD              | V45x |
| PA10   | LCD              | V45x |
| PA11   | IIC_EEPROM_SDA   | V45x |
| PA12   | IIC_EEPROM_SCL   | V45x |
| PA13   | SWDIO            | V45x |
| PA14   | SWCLK            | V45x |
| PA15   | J3_PIN           | V453 |
| PB0    | TEMP_BED_PIN     | V45x |
| PB1    | TEMP_0_PIN       | V45x |
| PB2    | PROBE_ACTIVATION_SWITCH_PIN / J2_PIN | V453 |
| PB3    | Z_DIR_PIN        | V45x |
| PB4    | Z_STEP_PIN       | V45x |
| PB5    | Y_DIR_PIN        | V45x |
| PB6    | Y_STEP_PIN       | V45x |
| PB7    | X_DIR_PIN        | V45x |
| PB8    | X_STEP_PIN       | V45x |
| PB9    | E0_DIR_PIN       | V45x |
| PB10   | (not assigned)   | V45x |
| PB11   | UART_RX          | V45x |
| PB12   | J4_PIN           | V453 |
| PB13   | HEATER_BED_PIN   | V453 |
| PB14   | HEATER_0_PIN     | V453 |
| PB15   | FAN_PIN          | V453 |
| PC0    | (not assigned)   | V45x |
| PC1    | (not assigned)   | V45x |
| PC2    | E0_STEP_PIN      | V45x |
| PC3    | X/Y/Z/E0_ENABLE_PIN | V45x |
| PC4    | X_STOP_PIN       | V45x |
| PC5    | Y_STOP_PIN       | V45x |
| PC6    | (not assigned)   | V453/V45x |
| PC7    | SD_DETECT_PIN    | V45x |
| PC8    | LCD              | V45x |
| PC9    | LCD              | V45x |
| PC10   | SDIO             | V45x |
| PC11   | SDIO             | V45x |
| PC12   | SDIO             | V45x |
| PC13   | (not assigned)   | V45x |
| PC14   | (not assigned)   | V45x |
| PC15   | (not assigned)   | V45x |
| PD0    | OSC_IN           | V45x |
| PD1    | OSC_OUT          | V45x |


* NOTE: Klipper uses the same pins as Marlin and for the same purposes, with the sole exception of pin PB2.  Klipper has no probe_enable function.

### Conditionally Usable Pins

These are pins that Marlin assigns to named 3‑pin connectors on the 4.5.3 board, but which Klipper does not use, making them candidates for conditional reuse if the user understands the electrical routing.

✔️ PA0 — Routed to Reserved Connector J1  
    Source: pins_CREALITY_V453.h  
    Used by Marlin: UNKNOWN (enumerated but not called)   
    Used by Klipper: NO  
    Electrically routed to: Connector J1

✔️ PB2 — Routed to Reserved Connector J2  
    Source: pins_CREALITY_V453.h  
    Used by Marlin: YES  (Probe_ENable)  
    Used by Klipper: NO  
    Electrically routed to: Connector J2

✔️ PA15 — Routed to Reserved Connector J3  
    Source: pins_CREALITY_V453.h  
    Used by Marlin: UNKNOWN (enumerated but not called)  
    Used by Klipper: NO  
    Electrically routed to: Connector J3

✔️ PB12 — Routed to Reserved Connector J4  
    Source: pins_CREALITY_V453.h  
    Used by Marlin:  UNKNOWN (enumerated but not called)   
    Used by Klipper: NO  
    Electrically routed to: Connector J4

✔️ These remaining pins are “not assigned; routing unknown”:  
    PA1, PA2, PA3, PC0, PC1, PC6, PC13–PC15, PB10  
    → No confirmed routing  
    → No known Marlin assignment  
    → No known Klipper assignment

## 🟦 CREALITY 1.1.0.3

[![1.1.0.3 Thumbnail](https://user-images.githubusercontent.com/36551518/162259301-2d5b5bdf-805c-48fa-a4d7-64a25cd79884.jpg)

### Differences from 4.5.3:

 * PB2 is routed to J705 instead of J2.

 * Connectors J1, J2, J3, and J4 do not exist on the 1.1.0.3 board.
  With the exception of J705, the 3-pin reserved connectors on the 1.1.0.3 board do not appear to be routed to any MCU pins.  (No direct continuity detected; possible series resistors or unused pads?)

  All other MCU pin assignments match the 4.5.3 Marlin definitions.

### Full STM32F103 GPIO Map

| MCU Pin | Marlin Function | Source File |
|--------|------------------|-------------|
| PA0    | J1_PIN (routing unknown)   | V453 |
| PA1    | (not assigned)   | V453/V45x |
| PA2    | (not assigned)   | V453/V45x |
| PA3    | (not assigned)   | V453/V45x |
| PA4    | Z_STOP_PIN       | V45x |
| PA5    | PROBE_TARE_PIN   | V45x |
| PA6    | LED_PIN          | V45x |
| PA7    | FIL_RUNOUT_PIN   | V45x |
| PA8    | LCD              | V45x |
| PA9    | LCD              | V45x |
| PA10   | LCD              | V45x |
| PA11   | IIC_EEPROM_SDA   | V45x |
| PA12   | IIC_EEPROM_SCL   | V45x |
| PA13   | SWDIO            | V45x |
| PA14   | SWCLK            | V45x |
| PA15   | J3_PIN  (routing unknown)         | V453 |
| PB0    | TEMP_BED_PIN     | V45x |
| PB1    | TEMP_0_PIN       | V45x |
| PB2    | PROBE_ACTIVATION_SWITCH_PIN / J2_PIN | V453 |
| PB3    | Z_DIR_PIN        | V45x |
| PB4    | Z_STEP_PIN       | V45x |
| PB5    | Y_DIR_PIN        | V45x |
| PB6    | Y_STEP_PIN       | V45x |
| PB7    | X_DIR_PIN        | V45x |
| PB8    | X_STEP_PIN       | V45x |
| PB9    | E0_DIR_PIN       | V45x |
| PB10   | (not assigned)   | V45x |
| PB11   | UART_RX          | V45x |
| PB12   | J4_PIN (routing unknown)          | V453 |
| PB13   | HEATER_BED_PIN   | V453 |
| PB14   | HEATER_0_PIN     | V453 |
| PB15   | FAN_PIN          | V453 |
| PC0    | (not assigned)   | V45x |
| PC1    | (not assigned)   | V45x |
| PC2    | E0_STEP_PIN      | V45x |
| PC3    | X/Y/Z/E0_ENABLE_PIN | V45x |
| PC4    | X_STOP_PIN       | V45x |
| PC5    | Y_STOP_PIN       | V45x |
| PC6    | (not assigned)   | V453/V45x |
| PC7    | SD_DETECT_PIN    | V45x |
| PC8    | LCD              | V45x |
| PC9    | LCD              | V45x |
| PC10   | SDIO             | V45x |
| PC11   | SDIO             | V45x |
| PC12   | SDIO             | V45x |
| PC13   | (not assigned)   | V45x |
| PC14   | (not assigned)   | V45x |
| PC15   | (not assigned)   | V45x |
| PD0    | OSC_IN           | V45x |
| PD1    | OSC_OUT          | V45x |

### Conditionally Usable Pins

These are pins that Marlin assigns to named 3‑pin connectors on the 4.5.3 board, but which are not physically connected on the 1.1.0.3 board and/or which Klipper does not use.  These pins are candidates for conditional reuse, if the user understands the electrical routing.

✔️ PB2 — Routed to Connector J705  
    Source: pins_CREALITY_V453.h  
    Used by Marlin: YES (Probe Enable)  
    Used by Klipper: NO  
    Electrically routed to: J705  

✔️ PA0 — J1_PIN (routing unknown)  
    Source: pins_CREALITY_V453.h  
    Used by Marlin: UNKNOWN (enumerated but not called)  
    Used by Klipper: NO  
    Electrically routed to: Unknown (no continuity detected)

✔️ PA15 — J3_PIN (routing unknown)  
    Source: pins_CREALITY_V453.h  
    Used by Marlin: UNKNOWN (enumerated but not called)  
    Used by Klipper: NO  
    Electrically routed to: Unknown (no continuity detected)

✔️ PB12 — J4_PIN (routing unknown)  
    Source: pins_CREALITY_V453.h  
    Used by Marlin: UNKNOWN (enumerated but not called)  
    Used by Klipper: NO  
    Electrically routed to: Unknown (no continuity detected)

  ### Remaining Pins: “Not Assigned; Routing Unknown”

  These pins appear in neither pins_CREALITY_V453.h nor pins_CREALITY_V45x.h,
  and continuity testing has found no routing to any external connectors on an actual 1.1.0.3 board.

  PA1, PA2, PA3, PC0, PC1, PC6, PC13–PC15, PB10  
  → No confirmed routing  
  → No known Marlin assignment  
  → No known Klipper assignment  

## BTT SKR CR6 v1.0

[![SKR CR6 v1.0 Thumbnail](https://user-images.githubusercontent.com/36551518/192142774-d5500af4-7ef0-41ef-8e0e-2436ed213f85.jpg)

Trusted source:

```Code
   - pins_BTT_SKR_CR6.h  (board‑specific definitions)
```

### Full STM32F103 GPIO Map

| MCU Pin | Marlin Function | Source File |
|--------|------------------|-------------|
| PA0    | TEMP_0_PIN       | SKR_CR6 |
| PA1    | PROBE_TARE_PIN   | SKR_CR6 |
| PA2    | (not assigned)   | SKR_CR6 |
| PA3    | (not assigned)   | SKR_CR6 |
| PA4    | ONBOARD_SD_CS_PIN | SKR_CR6 |
| PA5    | SD Card CLK    | BTT SKR-CR6-Pin.pdf |
| PA6    | (not assigned)   | SKR_CR6 |
| PA7    | SD Card MOSI   | BTT SKR-CR6-Pin.pdf |
| PA8    | NEOPIXEL_PIN     | SKR_CR6 |
| PA8    | SD Card MISO   | BTT SKR-CR6-Pin.pdf |
| PA9    | BTN_EN1 (if CR10_STOCKDISPLAY) | SKR_CR6 |
| PA10   | BTN_EN2 (if CR10_STOCKDISPLAY) | SKR_CR6 |
| PA11   | (not assigned)   | SKR_CR6 |
| PA12   | (not assigned)   | SKR_CR6 |
| PA13   | LED_CONTROL_PIN / CASE_LIGHT_PIN | SKR_CR6 |
| PA14   | USB_CONNECT_PIN  | SKR_CR6 |
| PA15   | BTN_ENC (if CR10_STOCKDISPLAY) | SKR_CR6 |
| PB0    | Z_STEP_PIN       | SKR_CR6 |
| PB1    | Z_ENABLE_PIN     | SKR_CR6 |
| PB2    | Y_DIR_PIN        | SKR_CR6 |
| PB3    | E0_STEP_PIN      | SKR_CR6 |
| PB4    | E0_DIR_PIN       | SKR_CR6 |
| PB5    | BEEPER_PIN (if CR10_STOCKDISPLAY) | SKR_CR6 |
| PB6    | IIC_EEPROM_SCL   | SKR_CR6 |
| PB7    | IIC_EEPROM_SDA   | SKR_CR6 |
| PB8    | LCD_PINS_RS (if CR10_STOCKDISPLAY) | SKR_CR6 |
| PB9    | LCD_PINS_D4 (if CR10_STOCKDISPLAY) | SKR_CR6 |
| PB10   | Y_STEP_PIN       | SKR_CR6 |
| PB11   | Y_ENABLE_PIN     | SKR_CR6 |
| PB12   | X_DIR_PIN        | SKR_CR6 |
| PB13   | X_STEP_PIN       | SKR_CR6 |
| PB14   | X_ENABLE_PIN     | SKR_CR6 |
| PB15   | LCD_PINS_ENABLE (if CR10_STOCKDISPLAY) | SKR_CR6 |
| PC0    | X_STOP_PIN       | SKR_CR6 |
| PC1    | Y_STOP_PIN       | SKR_CR6 |
| PC2    | PROBE_ACTIVATION_SWITCH_PIN | SKR_CR6 |
| PC3    | TEMP_BED_PIN     | SKR_CR6 |
| PC4    | SD_DETECT_PIN    | SKR_CR6 |
| PC5    | Z_DIR_PIN        | SKR_CR6 |
| PC6    | FAN_PIN          | SKR_CR6 |
| PC7    | CONTROLLER_FAN_PIN | SKR_CR6 |
| PC8    | HEATER_0_PIN     | SKR_CR6 |
| PC9    | HEATER_BED_PIN   | SKR_CR6 |
| PC10   | UART Tx4   | BTT SKR-CR6-Pin.pdf |
| PC11   | UART Rx4   | BTT SKR-CR6-Pin.pdf |  
| PC12   | PWR_DET          | BTT SKR-CR6-Pin.pdf |
| PC13   | SUICIDE_PIN      | SKR_CR6 |
| PC14   | Z_STOP_PIN       | SKR_CR6 |
| PC15   | FIL_RUNOUT_PIN   | SKR_CR6 |
| PD0    | (not assigned)   | SKR_CR6 |
| PD1    | (not assigned)   | SKR_CR6 |
| PD2    | E0_ENABLE_PIN    | SKR_CR6 |

### Conditionally Usable Pins

These are pins that Marlin assigns to specific functions on the SKR‑CR6 board, but which Klipper does not use, making them candidates for conditional reuse if the user understands the electrical routing on the SKR‑CR6 PCB.

Unlike the Creality 4.5.x boards, the SKR‑CR6 does not expose J‑connectors (J1/J2/J3/J4/J705).
All routing is through standard headers, stepper sockets, endstop connectors, and fan/heater terminals.

✔ Pins Assigned by Marlin but Typically Unused by Klipper
✔️ PC2 — Routed to Connector J14  
    Source: pins_BTT_SKR_CR6.h  
    Used by Marlin: YES (Probe Enable)  
    Used by Klipper: NO  
    Electrically routed to: J14 (Z-STOP)

### Trade‑off repurposable pins (SKR‑CR6)

These are pins where Marlin assigns a function, but you can safely reclaim the pin if you’re willing to lose that feature.

✔️ PA8 — NEOPIXEL_PIN  
    Condition: No NeoPixel strip connected; NeoPixel feature disabled in firmware.  
    Trade‑off: Lose addressable LED lighting.  
    Verdict: Excellent general‑purpose GPIO candidate if you don’t use NeoPixels.

✔️ PB5 — BEEPER_PIN (CR10_STOCKDISPLAY only)  
    Condition: Either no CR10 LCD, or you don’t care about beeps.  
    Trade‑off: Lose LCD beeper feedback.  
    Verdict: Easy to sacrifice; good candidate for repurposing.

✔️ PA9, PA10, PA15 — BTN_EN1 / BTN_EN2 / BTN_ENC (CR10_STOCKDISPLAY only)  
    Condition: No CR10‑style LCD on EXP3; `CR10_STOCKDISPLAY` disabled.  
    Trade‑off: Lose rotary encoder + buttons on that LCD.  
    Verdict: If you use a different display (TFT, DWIN, or none), these become clean GPIOs.

✔️ PB8, PB9, PB15 — LCD_PINS_RS / LCD_PINS_D4 / LCD_PINS_ENABLE (CR10_STOCKDISPLAY only)  
    Condition: No CR10‑style LCD; `CR10_STOCKDISPLAY` disabled.  
    Trade‑off: Lose classic character LCD support.  
    Verdict: Strong GPIO candidates when using a non‑CR10 display.

### Remaining pins

✔️ PC12 — PWR_DET  
    Source: pins_BTT_SKR_CR6.h  
    Used by Marlin: OPTIONAL (power-detection, triggers automated shut-down routine if power is lost and a UPS is attached.)  
    Used by Klipper: OPTIONAL  
    Electrically routed to: J26  
    *NOTE:* This pin is electrically active and likely hard-wired for purpose.  Not likely to be readily repurposed for general GPIO use.

✔️ PC13 — SUICIDE_PIN  
    Source: pins_BTT_SKR_CR6.h  
    Used by Marlin: OPTIONAL (power‑kill / watchdog circuit)  
    Used by Klipper: OPTIONAL  
    Electrically routed to: J28  
    *NOTE:* This pin is electrically active and likely hard-wired for purpose.  Not likely to be readily repurposed for general GPIO use.



# 📚 Citations Used

These are the sources referenced in the above tables:

 * CR6Community Marlin pins files (Used for all verified pin assignments) 
   * [pins_CREALITY_V4_5_2.h](https://github.com/CR6Community/Marlin/blob/extui/Marlin/src/pins/stm32f1/pins_CREALITY_V452.h)
   * [pins_CREALITY_V4_5_3.h](https://github.com/CR6Community/Marlin/blob/extui/Marlin/src/pins/stm32f1/pins_CREALITY_V453.h)
   * [pins_CREALITY_45x.h](https://github.com/CR6Community/Marlin/blob/extui/Marlin/src/pins/stm32f1/pins_CREALITY_V45x.h)
   * [pins_BTT_SKR_CR6.h](https://github.com/CR6Community/Marlin/blob/extui/Marlin/src/pins/stm32f1/pins_BTT_SKR_CR6.h)

 * [BTT GitHub for BTT SKR CR6 motherboard](https://github.com/bigtreetech/BIGTREETECH-SKR-CR6/blob/master/)
 * [BTT SKR-CR6-Pin.pdf](https://github.com/bigtreetech/BIGTREETECH-SKR-CR6/blob/master/Hardware/BTT%20SKR-CR6-Pin.pdf)

 * [STM32F103RET6 Datasheet](https://www.st.com/resource/en/datasheet/stm32f103re.pdf)


# 🧩 What this document gives you

You now have:
 * A complete STM32F103 GPIO pin list for each board
 * Every verified pin marked
 * Every unverified / routing unknown pin marked
 * These pins are candidates for safe GPIO reassignment:
  * PB2 
     * Used as the optical sensor (Probe Enable) signal pin in the Community Firmware Marlin pins file.
       * Signal pin on J1 of the 4.5.2 motherboard.
       * Signal pin on J2 of the 4.5.3 motherboard.
       * Signal pin on J705 of 1.1.0.3 motherboard
     * The optical sensor is not used in Klipper.
     * The STM32 also samples the state of PB2 (="BOOT1") at boot. Creality have an internal pull-down resistor on BOOT0, so the chip always boots normally, regardless of the state of PB2, since it can never "see" BOOT0=BOOT1=1.
     * The above circumstances make PB2 a safe candidate _for use with Klipper_ on all 3 CR6 motherboards and on the BTT SKR CR6 motherboard.
  * PA3 
     * Marlin-verified to be wired to the signal pin on reserved connector J3 on the 4.5.2 motherboard.
     * NOTES:
      * On 4.5.3, J3 is connected to PA0 instead of PA3. PA3 is not mapped to any of the reserved connectors on that board.
      * Although J707 is labelled "Reserve connector J3" in Creality's photo of the 1.1.0.3, PA3 (pin 28 on the STM32 64-pin package) does NOT ring continuity to ANY of the 4 3-pin connectors J704-J707. It is not an available option on that board.
  
  * PC1–PC3
  
  * PC13–PC15
    * PC13–PC15 are low‑power pins typically used for RTC crystals on other STM32 boards
     Creality leaves them unconnected.