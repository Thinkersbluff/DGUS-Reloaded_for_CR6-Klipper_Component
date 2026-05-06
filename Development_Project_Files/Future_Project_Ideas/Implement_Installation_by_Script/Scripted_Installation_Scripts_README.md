# Scripted installation scripts

This document describes the scripts intended to support the scripted DGUS-Reloaded installation and verification flow on a Klipper host.

## Table of contents
- [Scripted installation scripts](#scripted-installation-scripts)
  - [Table of contents](#table-of-contents)
  - [Deploying scripts to the Klipper host (SFTP-first)](#deploying-scripts-to-the-klipper-host-sftp-first)
  - [install\_dgus\_minimal.sh](#install_dgus_minimalsh)
  - [verify\_installation.sh](#verify_installationsh)

## Deploying scripts to the Klipper host (SFTP-first)

Use your SFTP client to transfer the scripts into the host's Klipper directory and run them from a stable host path. This avoids assuming your PC can run remote git commands.

1) Create the destination folder on the host:

```bash
mkdir -p ~/printer_data/config/scripts
```

2) Upload the contents of `Installation_Files/scripts/` into `~/printer_data/config/scripts/`.

3) On the host, make the uploaded scripts executable:

```bash
cd ~/printer_data/config/scripts
chmod +x *.sh
ls -la
```

4) Run the installer or verification helpers from `~/klipper`.

Notes:
- Run commands as the user that owns `~/klipper` (often `pi`); the scripts prompt for `sudo` when needed.
- The scripts operate against `~/klipper` and `~/printer_data` by default; edit variables at the top of the script if your layout differs.

---

## install_dgus_minimal.sh
Purpose
- Sparse-clone the repository's `Installation_Files` tree, stage or apply DGUS extras and MCU source files into an existing `~/klipper` checkout, and idempotently patch `src/stm32/Kconfig` and `Makefile` when needed.

Usage
```bash
cd ~/printer_data/config/scripts
./install_dgus_minimal.sh [--dry-run|-n] [--keep-temp] [--clean]
```

Key options
- `--dry-run` / `-n`: simulate actions, write `/tmp/dgus_install/dryrun_report.txt` (includes timestamp and branch).
- `--keep-temp`: keep `/tmp/dgus_install` after run.
- `--clean`: interactively remove temp artifacts and staging area.

Notes
- Supports selecting board-specific printer configs; aborts if selected board folder is missing in the fetched tree.
- Staging mode copies files into `~/t5uid1_staging` for review; apply mode copies directly into `~/klipper`.

---

## verify_installation.sh
Purpose
- Automated verification script that runs safe, non-destructive checks (dry-run, staging, cleanup) and can run apply-mode tests when invoked with `--allow-apply`.

Usage
```bash
bash ~/printer_data/config/scripts/verify_installation.sh
# allow destructive apply tests:
bash ~/printer_data/config/scripts/verify_installation.sh --allow-apply
```

Notes
- Designed to automate the TestPlan; review PASS/WARN/FAIL output and logs after running.