# Updating an Existing DGUS-Reloaded for CR6 Installation

Last Updated: 9 March 2026

## Purpose

Use this guide when your printer is already running DGUS-Reloaded and you want to move to a newer DGUS-Reloaded release safely.

---

## Before You Start

1. Read the new release notes.
2. Confirm your motherboard type (4.5.2 / 4.5.3 / ERA / BTT SKR CR6).
3. SSH into your Pi.

---

## Step 1 — Back up first (required)

```bash
bash ~/klipper/scripts/dgus-reloaded/backup_klipper.sh
```

Expected: backup archive created successfully.

If needed later: see `4-Backup_Restore_Klipper.md`.

---

## Step 2 — Make Klipper repo clean before updating

```bash
~/printer_data/config/scripts/manage_t5uid1_patches.sh prepare
cd ~/klipper
git status --porcelain
```

Expected: empty output (clean tracked state).

If still dirty, stop and resolve tracked file changes first.

---

## Step 3 — Apply the DGUS-Reloaded release files

From the new release package, update:
- `t5uid1` extras
- board-specific config files in `~/printer_data/config/`
- board-specific prebuilt `klipper.bin` (if provided and required)

Do **not** blindly overwrite `printer.cfg` without review.

---

## Step 4 — Update Klipper host software (only if release notes instruct)

If release notes say to pin/rollback to a specific commit:

```bash
cd ~/klipper
git fetch --all --tags
git reset --hard <FULL_SHA_FROM_RELEASE_NOTES>
git rev-parse --short HEAD
```

Expected: short SHA matches release notes prefix.

Detailed instructions: `5-Force_Klipper_Version.md`.

---

## Step 5 — Rebuild/reflash MCU firmware when required

If host changed, or if Klipper reports MCU mismatch:
1. Reapply patches
2. Build firmware
3. Flash motherboard
4. Return repo to clean state

```bash
~/printer_data/config/scripts/manage_t5uid1_patches.sh reapply

cd ~/klipper
make clean
make
```

After flashing:
```bash
~/printer_data/config/scripts/manage_t5uid1_patches.sh prepare
```

Detailed instructions: `3-Rebuilding_MCU_Firmware.md`.

---

## Step 6 — Final verification

- Restart Klipper (`Firmware Restart`)
- Confirm Klipper state is `Ready`
- Confirm display is functional
- Confirm clean git status:

```bash
cd ~/klipper
git status --porcelain
```

Expected: empty output.

---

## Quick Decision Table

| Situation | Action |
|---|---|
| Moonraker says Klipper is dirty | Run `prepare` before update |
| Update broke compatibility | Use release-notes SHA reset flow |
| MCU mismatch warning | Rebuild/reflash MCU firmware |
| Unsure / risky change | Back up first |