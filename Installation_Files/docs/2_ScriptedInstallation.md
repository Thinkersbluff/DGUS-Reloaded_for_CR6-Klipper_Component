# Scripted Installation Guide — DGUS-Reloaded for CR6

Last updated: 2026-03-05

**Purpose:** Provide a concise, repeatable set of commands and checks for installing the `klippy_extras_Extensions`, `make_menuconfig_Extensions`, and supporting scripts using the current installer scripts. 

**Assumptions**
This guide assumes you will run the installer directly on the target Raspberry Pi, through an SSH application which is logged into your home directory with sudo authority on that Pi.

**Prerequisites**
- A working Klipper host checkout in `~/klipper` (Mainsail/Fluidd installed).
- SSH access to the Pi and a shell prompt.
- `git`, `make`, `python3`, `wget` available on the Pi.
- The installation scripts and supporting files are already present in `~/klipper/scripts/dgus-reloaded/` (e.g. Extracted from the Source.zip file of the latest release and uploaded there on the target Pi via SFTP.).

**Files referenced by this guide**
- Installer: `~/klipper/scripts/dgus-reloaded/install_dgus_minimal.sh`
- Patch manager: `~/klipper/scripts/dgus-reloaded/manage_t5uid1_patches.sh`
- Support scripts (may include tests/README) in the same directory.

**Overview (high level)**
- Run preflight checks and stop Klipper.
- Run the installer script to copy extras and MCU sources into `~/klipper`.
- Verify files and applied patches.
- Build and flash the MCU firmware (interactive `make menuconfig` + `make`).
- Restart Klipper and verify operation.

**1) Preflight (on the Pi, over SSH)**
- Ensure you are the `pi` sudo user (or an account with access to `~/klipper`).

```sh
# stop klipper service while files are changed
sudo systemctl stop klipper

# quick sanity checks
[ -d "$HOME/klipper" ] || { echo "No ~/klipper found — install Klipper first"; exit 1; }
command -v git >/dev/null || { echo "git not found"; exit 1; }
command -v make >/dev/null || { echo "make not found"; exit 1; }
command -v python3 >/dev/null || { echo "python3 not found"; exit 1; }
```

- Backup the MCU Kconfig/Makefile before proceeding (installer also makes backups, but keep a local one):

```sh
mkdir -p "$HOME/.dgus_backups"
cp -v ~/klipper/src/stm32/Kconfig "$HOME/.dgus_backups/Kconfig.$(date +%Y%m%d_%H%M%S)"
cp -v ~/klipper/src/stm32/Makefile "$HOME/.dgus_backups/Makefile.$(date +%Y%m%d_%H%M%S)"
```

**2) Run the installer script**

- Navigate to the installer location you placed on the Pi (example path):

```sh
cd ~/klipper/scripts/dgus-reloaded
```

- Optionally force which branch the installer clones from (the script accepts `DGUS_BRANCH`):

```sh
# example: use the dgus-reloaded branch
DGUS_BRANCH=dgus-reloaded sudo bash ./install_dgus_minimal.sh

# or run without forcing a branch to use the remote repo's default branch
sudo bash ./install_dgus_minimal.sh
```

### Additional installer options

- `--dry-run` / `-n`: simulate the install and show exactly what would be copied or changed without writing to your live `~/klipper` tree. The script will stage files into a temporary directory and generate a dry-run report at the temporary path it creates (the script prints the path). Example:

```sh
DGUS_BRANCH=dgus-reloaded ./install_dgus_minimal.sh --dry-run
```

- `--keep-temp`: when provided, the script will not auto-delete the temporary clone/staging directory at the end of the run — useful together with `--dry-run` to inspect staged files. Example:

```sh
DGUS_BRANCH=dgus-reloaded ./install_dgus_minimal.sh --dry-run --keep-temp
```

When `--dry-run` is used the installer forces staging mode (does not apply changes to `~/klipper`). The dry-run report file inside the temporary directory lists the planned `rsync`/patch commands and the files that would be copied.


### Board-specific repository locations

When you choose a board during the interactive prompt, the installer looks for matching board-specific configuration files under the `Installation_Files` tree. The current repository layout uses the `klippy_extras_Extensions/Related Changes/Custom_Klipper+Mainsail_Files/` location for those files. Examples:

- BTT SKR CR6 V1.0:
  `Installation_Files/klippy_extras_Extensions/Related Changes/Custom_Klipper+Mainsail_Files/BTT SKR CR6 Only/`
- Creality 4.5.2 motherboard files:
  `Installation_Files/klippy_extras_Extensions/Related Changes/Custom_Klipper+Mainsail_Files/Creality CR6 Mobo/4.5.2 MB/`
- Creality 4.5.3 / ERA 1.1.0.3 motherboard files:
  `Installation_Files/klippy_extras_Extensions/Related Changes/Custom_Klipper+Mainsail_Files/Creality CR6 Mobo/ERA 1.1.0.3 or 4.5.3 MB/`

If the branch you request to clone does not contain the selected board directory, the installer will abort to avoid applying partial or missing board configurations.


### Summary

### Installer modes and switches

| Mode / Switch | Purpose | Actions performed |
|---|---|---|
| Normal run (no flags) | Install into the live `~/klipper` tree (interactive) | Sparse-clones the repo (default branch or `DGUS_BRANCH`); prompts for motherboard; offers to **apply** files to `~/klipper` or **stage** for review; when applying it copies extras and MCU sources, idempotently patches `src/stm32/Kconfig` and `src/stm32/Makefile`, installs add-ons, and optionally starts the `klipper` service. |
| `--dry-run` / `-n` | Simulate installation without modifying live `~/klipper tree` | Forces staging mode: sparse-clones into a temp dir, stages the same files as staging mode, runs `rsync --dry-run` to list changed files, and writes a `dryrun_report.txt` in the temp dir. Does not stop/start services or edit Kconfig/Makefile on the live tree. |
| `--keep-temp` | Retain the temporary clone/staging directory after the script exits | Prevents auto-cleanup of the cloned repo and staging area so you can inspect files and the `dryrun_report.txt` (useful with `--dry-run`). |
| Staging mode (interactive choice 2) | Stage files for manual review before applying | Copies extras and source trees into `~/t5uid1_staging` (or the script's temp staging path). No changes to `~/klipper` until you explicitly apply from staging. |
| Apply mode (interactive choice 1) | Immediately copy files into the live Klipper checkout | Uses `rsync` to copy extras and MCU sources into `~/klipper`, runs idempotent Kconfig/Makefile patches, optionally copies `printer_data`, and may prompt to stop/start the `klipper` service. |
| Apply from staging (interactive choice 4) | Apply files previously staged in `~/t5uid1_staging` | Copies staged files into `~/klipper` (same actions as Apply mode) so you can review and edit staged content before deployment. |
| `DGUS_BRANCH` (env) | Select remote branch to clone | If set, the script validates the remote branch exists then clones that branch; otherwise the remote repo's default branch is used. |

Use these modes together as needed (for example, `DGUS_BRANCH=dgus-reloaded ./install_dgus_minimal.sh --dry-run --keep-temp` to simulate installing a specific branch and keep the temp staging tree for inspection).

**3) Verify the installation**

Run the quick verification script (or the checks from the installer). Example checks:

```sh
set -e
MISSING=0
for f in \
  "$HOME/klipper/klippy/extras/t5uid1/t5uid1.py" \
  "$HOME/klipper/src/stm32/t5uid1/Kconfig" \
  "$HOME/klipper/src/stm32/t5uid1/Makefile" \
  "$HOME/klipper/src/generic/t5uid1/serial_irq.c"; do
  [ -f "$f" ] || { echo "MISSING: $f"; MISSING=1; }
done
grep -q 'src/stm32/t5uid1/Kconfig' ~/klipper/src/stm32/Kconfig || { echo "Kconfig not patched"; MISSING=1; }
grep -q 'src/stm32/t5uid1/Makefile' ~/klipper/src/stm32/Makefile || { echo "Makefile not patched"; MISSING=1; }
[ $MISSING -eq 0 ] && echo "Install verification passed" || echo "Install verification failed"
```

If verification fails, do not proceed to build — fix the missing files or restore from the backups you created.

**4) Build the MCU firmware (interactive)**

- Change to the Klipper source directory and run `make menuconfig`.

```sh
cd ~/klipper
make menuconfig
```

- Important MenuConfig notes for the BTT SKR CR6 V1.0 (also applicable to the supported boards):
  - Enable `extra low-level configuration options` (so GPIO startup options are visible).
  - Set `GPIO pins to set at micro-controller startup` to `!PA14` (this avoids the DWIN_SET conflict).

- After configuring, build:

```sh
make -j$(nproc)
```

- Copy `out/klipper.bin` to the microSD (or follow your normal flashing procedure). Example using a mounted SD card at `/media/pi/UNTITLED`:

```sh
cp out/klipper.bin /media/pi/UNTITLED/klipper.bin
sync
# insert SD into board and power on to flash
```

**5) Restart Klipper and validate**

```sh
sudo systemctl start klipper
sudo systemctl status klipper --no-pager
# tail recent host log lines
sudo journalctl -u klipper -n 200 --no-pager
```

- If you see an MCU protocol error, rebuild/flash the MCU binary and re-run the checks. The host and MCU must be built from compatible sources.

**6) Useful troubleshooting commands**
- Reapply patches if you re-cloned or reverted: `sudo bash ~/klipper/scripts/dgus-reloaded/manage_t5uid1_patches.sh reapply`
- Inspect Klippy log for tracebacks: `sudo journalctl -u klipper -n 500 --no-pager` (or view the `klippy.log` file used by your front-end).
- Check that `t5uid1` module imports cleanly by running Python import test:

```sh
python3 -c "import importlib, sys; sys.path.insert(0, '$HOME/klipper'); import klippy.extras.t5uid1.t5uid1 as t; print('import OK')"
```

**7) Rollback and safety notes**
- The installer creates backups in `$HOME/.dgus_patch_backups` (timestamped). To roll back, restore the original files from that backup and restart Klipper.
- If a host API mismatch occurs (e.g., `register_response` vs `register_serial_response`), update the host extras in `~/klipper/klippy/extras/t5uid1/t5uid1.py` as needed and restart.

**8) Validation checklist (what I will test when following this guide)**
- Installer completes without error and verification reports "Install verification passed".
- `make menuconfig` + `make` complete successfully and `out/klipper.bin` is produced.
- MCU flashes from SD and the printer's MCU connects to the host without `MCU Protocol` errors.
- The touchscreen boots to the DGUS-Reloaded UI and `t5uid1` extras log no import/runtime errors.

**9) Notes for maintainers**
- The installer currently sparse-clones the upstream repo; the default branch is used unless `DGUS_BRANCH` is supplied.
- Keep `INSTALL_SCRIPT_PROPOSAL.md` and `ManualInstallation.md` in sync with this scripted guide; the scripted guide is the concise, runnable form for field use.

---
