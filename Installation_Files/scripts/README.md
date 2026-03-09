# DGUS install scripts

This folder contains the lightweight installer and helper scripts used to stage, apply and manage the DGUS-Reloaded assets on a Klipper host.

## Table of contents
- [DGUS install scripts](#dgus-install-scripts)
  - [Table of contents](#table-of-contents)
  - [Deploying scripts to the Klipper host (SFTP-first)](#deploying-scripts-to-the-klipper-host-sftp-first)
  - [install\_dgus\_minimal.sh](#install_dgus_minimalsh)
  - [manage\_t5uid1\_patches.sh](#manage_t5uid1_patchessh)
  - [backup\_klipper.sh](#backup_klippersh)
  - [restore\_klipper.sh](#restore_klippersh)
  - [verify\_installation.sh](#verify_installationsh)
  - [git\_ignore.sh](#git_ignoresh)
  - [test\_syntax\_host.sh](#test_syntax_hostsh)

## Deploying scripts to the Klipper host (SFTP-first)

Use your SFTP client to transfer the scripts into the host's Klipper directory and run them from a stable host path. This avoids assuming your PC can run remote git commands.

1) Create the destination folder on the host:

```bash
mkdir -p ~/klipper/scripts/dgus-reloaded
```

2) Upload the contents of `Installation_Files/scripts/` into `~/klipper/scripts/dgus-reloaded/`.

3) On the host, make the uploaded scripts executable:

```bash
cd ~/klipper/scripts/dgus-reloaded
chmod +x *.sh
ls -la
```

4) Run the installer or helpers from `~/klipper` (examples below in each script section).

Notes:
- Run commands as the user that owns `~/klipper` (often `pi`); the scripts prompt for `sudo` when needed.
- The scripts operate against `~/klipper` and `~/printer_data` by default; edit variables at the top of the script if your layout differs.

---

## install_dgus_minimal.sh
Purpose
- Sparse-clone the repository's `Installation_Files` tree, stage or apply DGUS extras and MCU source files into an existing `~/klipper` checkout, and idempotently patch `src/stm32/Kconfig` and `Makefile` when needed.

Usage
```bash
cd ~/klipper
./scripts/dgus-reloaded/install_dgus_minimal.sh [--dry-run|-n] [--keep-temp] [--clean]
```

Key options
- `--dry-run` / `-n`: simulate actions, write `/tmp/dgus_install/dryrun_report.txt` (includes timestamp and branch).
- `--keep-temp`: keep `/tmp/dgus_install` after run.
- `--clean`: interactively remove temp artifacts and staging area.

Notes
- Supports selecting board-specific printer configs; aborts if selected board folder is missing in the fetched tree.
- Staging mode copies files into `~/t5uid1_staging` for review; apply mode copies directly into `~/klipper`.

---

## manage_t5uid1_patches.sh
Purpose
- Helper to remove, reapply or inspect DGUS `t5uid1` include lines in `~/klipper/src/stm32/Kconfig` and `~/klipper/src/stm32/Makefile` prior to pulling upstream updates.

Usage
```bash
cd ~/klipper
./scripts/dgus-reloaded/manage_t5uid1_patches.sh prepare
./scripts/dgus-reloaded/manage_t5uid1_patches.sh reapply
./scripts/dgus-reloaded/manage_t5uid1_patches.sh status
```

Notes
- `prepare` saves timestamped backups under `~/.dgus_patch_backups/prepare_<ts>/` and removes the DGUS include lines.
- `reapply` adds the include lines back idempotently.

---

## backup_klipper.sh
Purpose
- Create a timestamped tar.gz archive of `~/klipper` and record the current git commit SHA (if present). Backups are stored in `~/klipper_backups` by default.

Usage
```bash
bash ~/klipper/scripts/backup_klipper.sh
# or specify destination and klipper path
bash ~/klipper/scripts/backup_klipper.sh /path/to/backups /home/pi/klipper
```

Output
- Example: `~/klipper_backups/klipper.20260308_014600.tar.gz` and `... .commit` containing the SHA.

---

## restore_klipper.sh
Purpose
- Restore a timestamped archive into `~/klipper`. By default the script skips building (`make`) after restore; use `--build` to run `make`.

Usage
```bash
# interactive chooser from default backups
bash ~/klipper/scripts/restore_klipper.sh

# restore specific archive and build
bash ~/klipper/scripts/restore_klipper.sh /home/pi/klipper_backups/klipper.TS.tar.gz --build
```

Notes
- The script prompts before overwriting `~/klipper` and will stop/start the `klipper` service. Restoring only affects the host filesystem — it does not reflash the MCU.
- Default behavior: skip `make` (use `--build` to run `make` after restoring).

---

## verify_installation.sh
Purpose
- Automated verification script that runs safe, non-destructive checks (dry-run, staging, cleanup) and can run apply-mode tests when invoked with `--allow-apply`.

Usage
```bash
bash ~/klipper/scripts/verify_installation.sh
# allow destructive apply tests:
bash ~/klipper/scripts/verify_installation.sh --allow-apply
```

Notes
- Designed to automate the TestPlan; review PASS/WARN/FAIL output and logs after running.

---

## git_ignore.sh
Purpose
- Helper to add host-local excludes so your local DGUS files don't show as "dirty" in Git.

Usage
```bash
cd ~/klipper
./scripts/dgus-reloaded/git_ignore.sh
git status --porcelain
```

Notes
- This helper creates `.git/info/exclude` entries — it does not create commits.
- If the files listed in git_ignore.sh are not tracked by git, you do not need to run this script. It is only necessary if you are installing from a klipper fork that contains and tracks those files.

---

## test_syntax_host.sh
Purpose
- Convenience script to run `bash -n` against scripts in `~/klipper/scripts/dgus-reloaded` to catch syntax errors.

Usage
```bash
cd ~/klipper/scripts/dgus-reloaded
./test_syntax_host.sh
```

---




