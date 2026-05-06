# DGUS-Reloaded Installer Test Plan

Purpose
- Provide a concise, ordered test plan to verify `install_dgus_minimal.sh` modes and behavior.

Notes
- Run tests on a non-production Pi or after taking backups; some tests modify the live `~/klipper` tree if you enable apply-mode.
- The supplied verification script automates the read-only and staging tests by default and will only run potentially destructive apply steps when invoked with `--allow-apply`.

Tests (ordered)

1) Dry-run (with `--keep-temp`)
- Command:
  DGUS_BRANCH=Implement_scripted_download_install ./install_dgus_minimal.sh --dry-run --keep-temp
- Verify:
  - `/tmp/dgus_install/dryrun_report.txt` exists
  - Header contains `Timestamp:` and `Branch:`
  - `SOURCE:` entries precede file lists
  - No writes to `~/klipper`

2) Dry-run (no `--keep-temp`) — cleanup prompt
- Command:
  printf 'y\n' | DGUS_BRANCH=Implement_scripted_download_install ./install_dgus_minimal.sh --dry-run
- Verify:
  - The script prompts to remove `/tmp/dgus_install` and older trees
  - `/tmp/dgus_install` is removed after accepting prompt

3) Staging mode (interactive choice 2)
- Command (example board 3):
  printf '3\n2\n' | DGUS_BRANCH=Implement_scripted_download_install ./install_dgus_minimal.sh --keep-temp
- Verify:
  - Staged files exist under `~/t5uid1_staging`:
    - `~/t5uid1_staging/klippy_extras_Extensions/klippy/extras/t5uid1`
    - `~/t5uid1_staging/printer_data` (if board selected)
  - No changes to live `~/klipper` files

4) Apply from staging (interactive choice 4) — optional / destructive
- Precondition: staging from test (3)
- Command (safe defaults: do not stop/start klipper):
  printf '4\nn\nn\n' | DGUS_BRANCH=Implement_scripted_download_install ./install_dgus_minimal.sh --keep-temp
- Verify:
  - Files copied into `~/klipper` (extras and src)
  - `src/stm32/Kconfig` and `Makefile` patched idempotently
  - Backups created in `$HOME/.dgus_patch_backups` (or similar)

5) Apply immediate (interactive choice 1) — optional / destructive
- Command:
  DGUS_BRANCH=Implement_scripted_download_install ./install_dgus_minimal.sh
  (choose board, then choose 1)
- Verify: same as apply-from-staging

6) Idempotency
- Re-run an apply (step 4 or 5) and verify no duplicate Kconfig/Makefile entries:
  - `grep -c 'src/stm32/t5uid1/Kconfig' ~/klipper/src/stm32/Kconfig` should be `1`

7) `--clean` interactive removal
- Command:
  ./install_dgus_minimal.sh --clean
- Verify:
  - `/tmp/dgus_install` and any `/tmp/dgus_install.*` trees removed when answered `y`
  - `~/t5uid1_staging` removed when answered `y`

8) Edge cases
- Invalid branch: `DGUS_BRANCH=nonexistent ./install_dgus_minimal.sh` should error cleanly
- Missing `~/klipper`: script should prompt and abort or guide to install kiauh

Execution notes
- Use the provided verification script `Development_Project_Files/Future_Project_Ideas/Implement_Installation_by_Script/verify_installation.sh` to automate non-destructive checks and to run the interactive `--clean` test when desired.
- Avoid running destructive apply steps unless you have backups and are prepared to rebuild/flash the MCU if necessary.
