# Backup & Restore Klipper

This document describes two helper scripts added to `Installation_Files/scripts` which make it easy to snapshot and restore your `~/klipper` tree.

Files added
- `Installation_Files/scripts/backup_klipper.sh` — creates a timestamped tar.gz archive of `~/klipper` and (if present) records the git commit SHA.
- `Installation_Files/scripts/restore_klipper.sh` — restores a tar.gz archive into `~/klipper`, stops/starts the `klipper` service, and optionally runs `make`.

Why use these
- Moonraker or the UI update action can change `~/klipper` unexpectedly; a quick backup before updating allows reliable rollback if a new host build is incompatible with your extras (e.g. `t5uid1.py`).

Script: `backup_klipper.sh`
- Purpose: create an archive snapshot of the current `~/klipper` tree and record the current git commit (if the tree is a git clone).
- Location: `Installation_Files/scripts/backup_klipper.sh`
- Basic usage (run on the Pi):

```sh
# default: saves to ~/klipper_backups and backs up ~/klipper
bash ~/klipper/scripts/backup_klipper.sh

# specify destination dir and klipper path:
bash ~/klipper/scripts/backup_klipper.sh /path/to/backups /home/pi/klipper
```

- Output: a file like `~/klipper_backups/klipper.20260308_123456.tar.gz` and (if git) `~/klipper_backups/klipper.20260308_123456.commit` containing the commit SHA.

- Script: `restore_klipper.sh`
- Purpose: restore a previously-created tar.gz archive into `~/klipper`, optionally rebuild, and restart the `klipper` service.
- Location: `Installation_Files/scripts/restore_klipper.sh`
- Basic usage:

```sh
# restore (default: does NOT run `make` after restore). The script will prompt
# for which backup to restore if you omit the archive path.
bash ~/klipper/scripts/restore_klipper.sh ~/klipper_backups/klipper.20260308_123456.tar.gz

# restore and run `make` (use this when you intentionally want to rebuild):
bash ~/klipper/scripts/restore_klipper.sh ~/klipper_backups/klipper.20260308_123456.tar.gz --build
```

- Behavior: the script prompts to confirm overwriting `~/klipper`, stops the `klipper` systemd service, removes the existing tree, extracts the archive, and by default does NOT run `make`. Use `--build` to run `make` in the restored tree; after that the script restarts the service.

Recommended workflow
1. Before attempting an update from Moonraker/UI, run the backup script:

```sh
bash ~/klipper/scripts/backup_klipper.sh
```

2. Proceed with the update via Moonraker/UI.

3. If the update breaks compatibility (errors in `klippy.log`, MCU protocol errors, or import/runtime errors for `t5uid1`), restore the previously-created archive:

```sh
bash ~/klipper/scripts/restore_klipper.sh ~/klipper_backups/klipper.20260308_123456.tar.gz
```

Notes & cautions
- The restore script removes the current `~/klipper` tree — ensure you have backups of any local changes you want to keep.
- If you maintain local edits, consider keeping them in a branch or applying them after restoration.
- For smaller backups or faster operations, consider using `git` to record and restore commits instead of tarballing the entire tree. The backup script already records the git commit SHA if present.

Optional improvements
- Add a small cron job or systemd timer to prune old backups in `~/klipper_backups` if you need to conserve space.
- Integrate a pre-update hook (or point the UI update button to a wrapper) to run `backup_klipper.sh` automatically before update operations.
