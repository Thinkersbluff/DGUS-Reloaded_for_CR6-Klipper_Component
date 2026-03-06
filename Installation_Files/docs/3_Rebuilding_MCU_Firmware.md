# Rebuilding the Klipper MCU Firmware After a Moonraker-Triggered Klipper Update

## The Problem

If you have allowed Moonraker to update Klipper on your host (Pi), you may see a warning like the following when you do a **Firmware Restart**:

```
MCU 'mcu' has deprecated code (it is missing feature 'STEPPER_STEP_BOTH_EDGE').
Recompiling and flashing is recommended
(MCU version 'v0.11.0-205-g5f0d252b', host version 'v0.13.0-557-g54c7b65d5').
```

### What this warning means

Your Klipper installation has two parts that must match each other in version:

| Part | Where it lives | Updated by |
|---|---|---|
| **Host software** (Klippy) | `~/klipper/` on the Pi | Moonraker (automatic) |
| **MCU firmware** (klipper.bin) | Flashed to your printer motherboard | You (manually) |

When Moonraker updates the host software, the MCU firmware already flashed to your
motherboard falls behind. The warning is Klipper telling you the two versions no
longer match closely enough. Printing may still work for now, but features may
behave incorrectly and future updates may eventually stop working altogether.

**The fix** is to recompile `klipper.bin` from the now-updated host source code and
reflash it to your motherboard.

### Why this is not straightforward for DGUS-Reloaded users

Standard upstream Klipper does **not** include the T5UID1 serial interface code that
DGUS-Reloaded requires. Running `make menuconfig` on a plain Klipper installation
will **not** show the DGUS T5UID1 options, and the resulting `klipper.bin` will not
support your stock CR6 display.

Before you can compile a compatible firmware binary, the **`dgus_upstream` MCU patch
package must be applied** to your Klipper source tree. This adds the T5UID1 source
files and patches the Kconfig and Makefile so the options appear in `make menuconfig`.

---

## Before You Begin

### Check whether the dgus_upstream patches are already applied

From an SSH session on the Pi, run:

```bash
ls ~/klipper/src/stm32/t5uid1/
```

- **If you see** `serial.c`, `Kconfig`, and `Makefile` listed — the patches are
  already in place. **Skip ahead to [Step 2](#step-2-stop-klipper).**
- **If you get** `No such file or directory` — the patches have not been applied.
  Continue with Step 1.

> **Why might the patches be missing?**  
> Moonraker updates Klipper by pulling the latest upstream source. If the
> `dgus_upstream` patches were applied as direct file copies rather than as a proper
> git branch merge, a `git pull` by Moonraker will **not** remove them — but if
> Klipper was reinstalled from scratch (e.g. via KIAUH), they would be lost.
> Checking first avoids re-applying patches that are already there.

---

## Step 1: Apply the dgus_upstream Patches (if not already present)

You need to copy three folders of MCU source files into your Klipper source tree and
patch two build-system files.

### 1a. Get the patch files onto the Pi

Download the latest DGUS-Reloaded release from:
[https://github.com/Thinkersbluff/DGUS-Reloaded_for_CR6-Klipper_Component/releases](https://github.com/Thinkersbluff/DGUS-Reloaded_for_CR6-Klipper_Component/releases)

Extract the zip on your PC, then use SFTP to copy the `dgus_upstream/src/` folder
to a temporary location on the Pi, e.g. `~/dgus_patch/src/`.

Alternatively, use `git sparse-checkout` to pull only the source files directly
onto the Pi (adjust the URL once a public release repo is established):

```bash
git clone --no-checkout --filter=blob:none \
  https://github.com/Thinkersbluff/DGUS-Reloaded_for_CR6-Klipper_Component.git \
  /tmp/dgus_install
cd /tmp/dgus_install
git sparse-checkout init --cone
git sparse-checkout set dgus_upstream/src
git checkout
```

### 1b. Copy the MCU source files

```bash
cp -r /tmp/dgus_install/dgus_upstream/src/stm32/t5uid1  ~/klipper/src/stm32/t5uid1
cp -r /tmp/dgus_install/dgus_upstream/src/generic/t5uid1 ~/klipper/src/generic/t5uid1
```

### 1c. Patch `src/stm32/Kconfig`

This adds the T5UID1 Kconfig block so `make menuconfig` can display the options.
The check prevents the line being added twice if this step is ever run again:

```bash
if ! grep -q 'src/stm32/t5uid1/Kconfig' ~/klipper/src/stm32/Kconfig; then
  sed -i 's|^endif$|source "src/stm32/t5uid1/Kconfig"\n\nendif|' \
    ~/klipper/src/stm32/Kconfig
fi
```

### 1d. Patch `src/stm32/Makefile`

This ensures the T5UID1 C files are compiled when the option is enabled:

```bash
if ! grep -q 'src/stm32/t5uid1/Makefile' ~/klipper/src/stm32/Makefile; then
  echo "" >> ~/klipper/src/stm32/Makefile
  echo "include src/stm32/t5uid1/Makefile" >> ~/klipper/src/stm32/Makefile
fi
```

### 1e. Verify the patches

```bash
ls ~/klipper/src/stm32/t5uid1/
# Expected: Kconfig  Makefile  serial.c  stm32_serial.h

ls ~/klipper/src/generic/t5uid1/
# Expected: serial_irq.c  serial_irq.h

grep 'src/stm32/t5uid1/Kconfig' ~/klipper/src/stm32/Kconfig && echo "Kconfig patch: OK"
grep 'src/stm32/t5uid1/Makefile' ~/klipper/src/stm32/Makefile && echo "Makefile patch: OK"
```

All four checks must pass before proceeding.

---

## Step 2: Stop Klipper

Before modifying the build, stop the Klipper service:

```bash
sudo systemctl stop klipper
```

---

## Step 3: Configure the Build for Your Motherboard

```bash
cd ~/klipper
make menuconfig
```

This opens an interactive text-based configuration screen. Navigate using the arrow
keys; press **Space** to toggle checkboxes; press **Q** then **Y** to save and exit.

Set the options exactly as listed for your motherboard below.

---

### Creality 4.5.3 or Creality 1.1.0.3 ERA

| Option | Value |
|---|---|
| Micro-controller Architecture | STM32 |
| Processor model | STM32F103 |
| Bootloader offset | 28KiB bootloader |
| Enable extra low-level configuration options | **[*]** (press Space to enable) |
| Communication interface | Serial (on USART1 PA10/PA9) |
| Enable DGUS T5UID1 screen | **[*]** (press Space to enable) |
| Screen serial interface | USART3 (on PB11/PB10) |
| Optimize stepper code for 'step on both edges' | **[*]** (default — leave enabled) |

> The 4.5.3 and ERA 1.1.0.3 boards share identical `make menuconfig` settings.
>
> **Note:** `Enable extra low-level configuration options` must be checked — without
> it, the `Screen serial interface` submenu is hidden and cannot be set.

---

### Creality 4.5.2

| Option | Value |
|---|---|
| Micro-controller Architecture | STM32 |
| Processor model | STM32F103 |
| Bootloader offset | 28KiB bootloader |
| Enable extra low-level configuration options | **[*]** (press Space to enable) |
| Communication interface | Serial (on USART1 PA10/PA9) |
| Enable DGUS T5UID1 screen | **[*]** (press Space to enable) |
| Screen serial interface | USART3 (on PB11/PB10) |
| Optimize stepper code for 'step on both edges' | **[*]** (default — leave enabled) |

> The 4.5.2 and 4.5.3/ERA boards use the same `make menuconfig` settings.
> They differ only in stepper and heater pin assignments inside `printer.cfg`,
> which this rebuild process does not affect.
>
> **Note:** `Enable extra low-level configuration options` must be checked — without
> it, the `Screen serial interface` submenu is hidden and cannot be set.

---

### BTT SKR CR6 V1.0

| Option | Value |
|---|---|
| Micro-controller Architecture | STM32 |
| Processor model | STM32F103 |
| Bootloader offset | 28KiB bootloader |
| Communication interface | USB (on PA11/PA12) |
| Enable extra low-level configuration options | **[*]** (press Space to enable) |
| GPIO pins to set at micro-controller startup | `!PA14` |
| Enable DGUS T5UID1 screen | **[*]** (press Space to enable) |
| Screen serial interface | USART2 (on PA3/PA2) |
| Optimize stepper code for 'step on both edges' | **[*]** (default — leave enabled) |

> **Note on "USB ids --->": ** When USB is selected as the communication interface,
> a `USB ids --->` submenu appears. **Do not change anything in it.** The defaults
> (`0x1d50` vendor ID, `0x614e` device ID, USB serial number from CHIPID) are the
> standard Klipper values and are correct for this board. Press **ESC** to leave
> that submenu without making changes.

**BTT SKR CR6 V1.0 — Important menuconfig details**

- **Enable extra low-level configuration options:** This must be enabled so the
  `GPIO pins to set at micro-controller startup` and other low-level options are visible.
- **GPIO pins to set at micro-controller startup:** Enter `!PA14` (exclamation mark
  before the pin) to ensure the board initializes the required GPIO at reset.

These two settings are required for correct behavior on the BTT SKR CR6 V1.0 board; omit-
ting them can prevent the MCU USB interface or display serial configuration from working as expected.

> **Important:** The BTT SKR CR6 uses **two separate serial interfaces** — USB for
> host communication and USART2 for the display. Make sure **Communication interface**
> is set to `USB (on PA11/PA12)` and **Screen serial interface** is set to
> `USART2 (on PA3/PA2)`. The display connector on the BTT SKR CR6 board is wired
> to PA2 (TX) and PA3 (RX) — **not** PA9/PA10. Using USART1 will produce no
> display output even though the firmware otherwise builds and runs correctly.

---

## Step 4: Compile the Firmware

```bash
cd ~/klipper
mkdir -p out/src/stm32/t5uid1 out/src/generic/t5uid1
make
```

The `mkdir -p` line creates the output subdirectories for the T5UID1 source files
before `make` runs. The Klipper build system creates these automatically for
directories declared in `dirs-y`, but only after the sub-Makefile containing that
declaration has been read during a clean build. Pre-creating them avoids the error:

```
fatal error: opening dependency file out/src/stm32/t5uid1/serial.d: No such file or directory
```

The build takes approximately 1–2 minutes. On success the final line will read:

```
Creating bin file out/klipper.bin
```

If `make` reports errors other than the missing-directory error above, the most
likely cause is that the Kconfig or Makefile patches from Step 1 were not applied
correctly. Re-check Step 1e and try again.

---

## Step 5: Copy `klipper.bin` to Your PC

The compiled binary is at:

```
~/klipper/out/klipper.bin
```

Use your SFTP client (WinSCP / MobaXterm) to download `klipper.bin` to your PC.

---

## Step 6: Flash the New Firmware to the Motherboard

### Prepare the SD card

Format a microSD card as **FAT32 with a 4096-byte (4 KB) sector size.** Any other
format will prevent the motherboard from reading the card.

### Creality 4.5.2, 4.5.3, or ERA 1.1.0.3

1. Copy `klipper.bin` to the SD card.
2. **Rename the file** so it does not match the filename used at the previous flash.
   For example, if you last flashed `klipper.bin`, rename it to `klipper_new.bin`.
   (The Creality bootloader refuses to flash a file whose name matches the last one.)
3. Power **off** the printer.
4. Insert the SD card into the printer motherboard's SD slot.
5. Power **on** the printer. The board flashes automatically (approximately 30 seconds).
6. Power **off** the printer and remove the SD card before the next power cycle.

### BTT SKR CR6 V1.0

1. Copy `klipper.bin` to the SD card.
2. **Rename the file to exactly `firmware.bin`.**
   The BTT SKR CR6 bootloader requires this exact filename; any other name will be
   ignored.
3. Power **off** the printer.
4. Insert the SD card into the board's SD slot.
5. Power **on** the printer. The board flashes automatically (approximately 30 seconds).
6. Power **off** the printer and remove the SD card before the next power cycle.

> **Note:** `make flash` does **not** work on the BTT SKR CR6. Always use the SD
> card method.

---

## Step 7: Restart Klipper and Confirm the Warning Is Gone

Restart the Klipper service:

```bash
sudo systemctl start klipper
```

Or use the **Firmware Restart** button in Mainsail / Fluidd.

In the Mainsail or Fluidd console, confirm that:

1. Klipper reports `Klipper state: Ready` with no MCU version mismatch warning.
2. The MCU and host versions now match (check the Klipper log or the System panel
   in Mainsail).

If the mismatch warning persists after the restart, the new binary may not have been
flashed successfully. Double-check the SD card filename and formatting, and repeat
Step 6.

---

## Keeping the Patches Across Future Moonraker Updates

Moonraker updates Klipper by running `git pull` inside `~/klipper`. The T5UID1
source files copied in Step 1 are **not tracked by git in the upstream Klipper
repository**, so `git pull` will **not remove them**. The patches will therefore
survive routine Moonraker updates.

However, if a future Klipper release moves or restructures `src/stm32/Kconfig` or
`src/stm32/Makefile`, the patches applied in Steps 1c–1d might need to be re-applied
or adjusted. If `make menuconfig` ever stops showing the DGUS T5UID1 options, re-run
the verification check in Step 1e to diagnose the problem.

---

## Quick Reference: Is a Firmware Rebuild Needed?

Run this from an SSH session on the Pi at any time:

```bash
grep "MCU 'mcu' has deprecated code" ~/printer_data/logs/klippy.log | tail -1
```

If this returns a line with version numbers, a rebuild is needed. Compare the
`MCU version` and `host version` strings — when they match (or are very close), no
rebuild is necessary.
