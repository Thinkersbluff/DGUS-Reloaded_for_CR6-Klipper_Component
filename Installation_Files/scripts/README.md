# DGUS install scripts

This folder contains a lightweight installer for the DGUS-Reloaded assets in the
`Installation_Files` portion of this repository.

## Table of contents
- [install_dgus_minimal.sh](#install_dgus_minimalsh)
- [Manage T5UID1 patches](#manage-t5uid1-patches)
- [Requirements](#requirements)
- [Usage](#usage)

## Deploying scripts to the Klipper host (SFTP-first)

Use your SFTP client to transfer the scripts into the host's Klipper directory and run them from a stable host path. This avoids assuming your PC can run remote git commands.

1) Create the destination folder on the host (one-line SSH or create it with your SFTP client):

```bash
# create the target path under the Klipper user home
ssh user@<klipper-host> 'mkdir -p ~/klipper/scripts/dgus-reloaded'
```

2) Using your SFTP tool, upload the contents of the repository folder `Installation_Files/scripts/` into the newly-created host folder `~/klipper/scripts/dgus-reloaded/`.

3) On the host, make the uploaded scripts executable (copy/paste into an SSH session):

```bash
# from an SSH session on the host
cd ~/klipper/scripts/dgus-reloaded
chmod +x *.sh
ls -la
```

4) Run the installer or the patch manager from `~/klipper` (copy/paste into an SSH session):

```bash
# run the lightweight installer
cd ~/klipper
./scripts/dgus-reloaded/install_dgus_minimal.sh

# check/manage t5uid1 patches
cd ~/klipper
./scripts/dgus-reloaded/manage_t5uid1_patches.sh status
# prepare before pulling upstream
cd ~/klipper
./scripts/dgus-reloaded/manage_t5uid1_patches.sh prepare
# reapply after updating Klipper
cd ~/klipper
./scripts/dgus-reloaded/manage_t5uid1_patches.sh reapply
```

Notes:
- Run the commands as the user that owns `~/klipper` (often `pi` or `klipper`), not as root. The scripts will prompt for `sudo` when they need to stop/start services.
- The scripts operate against `~/klipper` and `~/printer_data` by default; edit script variables near the top if your layout differs.

## install_dgus_minimal.sh
- Purpose: sparse-clone only the `Installation_Files` tree, then copy the required
  files into an existing `~/klipper` installation (or stage them for review/edit, first).
- Main features:
  - Preflight check for an existing `~/klipper` tree; offers to clone/run KIAUH if klipper is missing.
  - Uses `git sparse-checkout` so it does not download large binary blobs.
  - Two deployment modes: "stage" (safe review) and "apply" (copy directly into the live tree).
  - Idempotent patches to `src/stm32/Kconfig` and `src/stm32/Makefile` to include the
    `t5uid1` source when present. Backups of patched files are saved with a `.bak.TIMESTAMP`.
  - Optionally copies board-specific `Custom_Klipper+Mainsail_Files` into `~/printer_data`.
  - If a board is selected, the script verifies the corresponding board folder exists in the fetched install tree and will abort with an explanatory error if it is missing (no fallback is attempted).

- ## Requirements
- `git`, `rsync`, `bash` and standard Unix utilities on the host (Raspberry Pi OS / Debian-like).
- Run as the user that owns `~/klipper` (script will prompt for `sudo` when stopping/starting services).

## Usage

1. Copy the script to the Klipper host or run it directly on the host:

```bash
chmod +x Installation_Files/scripts/install_dgus_minimal.sh
./Installation_Files/scripts/install_dgus_minimal.sh
```

1. Follow the interactive prompts:
- Select which CR6 motherboard the installation should target (the script prompts once and reuses this choice for staging or apply).
- Confirm whether to stage the files for review, to directly modify the current `~/klipper` tree on the host, or to "apply-from-staging" to apply files you previously staged and edited.
- If applying, choose whether to stop the `klipper` service before copying.

- ## Notes & Safety
- The script is conservative: staging mode is recommended for first-time runs.
- When patching `Kconfig`/`Makefile` the script appends an include line if not already present
  and saves a timestamped backup of the original file.
- If your repository layout differs from the script's expected paths, edit the script
  variables at the top (`REPO_URL`, `KLIPPER_DIR_DEFAULT`, etc.) before running.

- ## Support
- What is staged: extras, source trees (if present), and the selected board's `Custom_Klipper+Mainsail_Files` (if chosen).

- If the selected board folder is missing in the fetched install tree the script will abort with an explanatory message. Inspect the fetch output and the staging area (`~/t5uid1_staging`) to diagnose missing files.

- If you find missing source folders or incorrect relative paths after cloning, run the script in staging mode and inspect the staged tree at `~/t5uid1_staging`.
## Apply-from-staging
- If you previously ran the script in staging mode and edited files in `~/t5uid1_staging`, re-run the script and choose option 4 (Apply from existing staging area). The script will copy files from `~/t5uid1_staging` into your live `~/klipper` tree and perform the same idempotent Kconfig/Makefile patches.

Note: the script will abort if the selected board was chosen originally but the corresponding board folder is not present in the staging area.

## Manage T5UID1 patches
This repository includes `manage_t5uid1_patches.sh` to help you temporarily remove and reapply the DGUS `t5uid1` include lines in the Klipper `src/stm32/Kconfig` and `src/stm32/Makefile` files when updating upstream Klipper.

Usage examples (run on the Klipper host):

```bash
# prepare before pulling upstream updates
chmod +x Installation_Files/scripts/manage_t5uid1_patches.sh
./Installation_Files/scripts/manage_t5uid1_patches.sh prepare

# pull/update Klipper (e.g., git pull) and resolve upstream changes

# reapply DGUS includes after update
./Installation_Files/scripts/manage_t5uid1_patches.sh reapply

# check status
./Installation_Files/scripts/manage_t5uid1_patches.sh status
```

## Git-ignore helper

After staging or applying the DGUS files you may want to keep them locally on the host
without having the Klipper repo show as "dirty" in Moonraker. A host-local ignore helper
is provided: `git_ignore.sh`.

Usage (on the host):

```bash
# add host-local excludes (no commit created)
cd ~/klipper
./scripts/dgus-reloaded/git_ignore.sh

# verify
git status --porcelain
```

Note: `install_dgus_minimal.sh` will copy `git_ignore.sh` into `~/klipper/scripts/dgus-reloaded/`
when applying or staging, so you can run it later if needed.

Host-side syntax test
---------------------
A convenience script `test_syntax_host.sh` is provided to run shell syntax checks
on all scripts installed to `~/klipper/scripts/dgus-reloaded`. Copy/paste into an
SSH session on the host to run it:

```bash
cd ~/klipper/scripts/dgus-reloaded
./test_syntax_host.sh
```

This runs `bash -n` on each `.sh` file in the directory and reports any syntax errors.

Notes:
- `prepare` saves timestamped backups under `~/.dgus_patch_backups/prepare_<ts>/` and removes the DGUS lines.
- `reapply` saves a backup of the current files and then adds the DGUS include lines back idempotently.
- Use `status` to check whether the t5uid1 include lines are present.

