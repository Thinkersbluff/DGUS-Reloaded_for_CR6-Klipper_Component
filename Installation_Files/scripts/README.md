# DGUS manual-install maintenance scripts

This document describes helper scripts useful to users who install or maintain DGUS-Reloaded manually on a Klipper host.


## Table of contents
- [DGUS manual-install maintenance scripts](#dgus-manual-install-maintenance-scripts)
  - [Table of contents](#table-of-contents)
  - [manage\_t5uid1\_patches.sh](#manage_t5uid1_patchessh)
  - [backup\_klipper.sh](#backup_klippersh)
  - [restore\_klipper.sh](#restore_klippersh)
  - [git\_ignore.sh](#git_ignoresh)
  - [test\_syntax\_host.sh](#test_syntax_hostsh)

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




