# DGUS manual-install maintenance scripts
This document describes helper scripts useful to users who install or maintain DGUS-Reloaded manually on a Klipper host.

## Table of contents
- [DGUS manual-install maintenance scripts](#dgus-manual-install-maintenance-scripts)
  - [Table of contents](#table-of-contents)
  - [Installing the Bash Shell (.sh) scripts on your Klipper host](#installing-the-bash-shell-sh-scripts-on-your-klipper-host)
  - [Purpose and Useage Explanations for each shell script](#purpose-and-useage-explanations-for-each-shell-script)
    - [manage\_t5uid1\_patches.sh](#manage_t5uid1_patchessh)
    - [backup\_klipper.sh](#backup_klippersh)
    - [restore\_klipper.sh](#restore_klippersh)
    - [git\_ignore.sh](#git_ignoresh)
    - [test\_syntax\_host.sh](#test_syntax_hostsh)
  - [DGUS Logging Subsystem Overview](#dgus-logging-subsystem-overview)
    - [Components](#components)
      - [t5uid1\_state\_logger.py](#t5uid1_state_loggerpy)
      - [t5uid1\_state\_exporter.py](#t5uid1_state_exporterpy)
      - [t5uid1\_log\_analyzer.py](#t5uid1_log_analyzerpy)
    - [Typical Workflow](#typical-workflow)

## Installing the Bash Shell (.sh) scripts on your Klipper host
To use the maintenance helpers on your Klipper host, copy all .sh files from this directory into the Klipper configuration scripts folder:

```Code
~/printer_data/config/scripts
```
After copying, run the following two commands on the Pi to normalize line endings and ensure all scripts are executable:

```bash
# 1) Convert any CRLF line endings to LF
find ~/printer_data/config/scripts -type f -name "*.sh" -exec sed -i 's/\r$//' {} \;

# 2) Make all scripts executable
chmod +x ~/printer_data/config/scripts/*.sh
```
These steps ensure the scripts run correctly under Bash on the Klipper host and avoid common issues caused by Windows-style line endings or missing executable permissions.

## Purpose and Useage Explanations for each shell script

### manage_t5uid1_patches.sh
Purpose
- Helper to remove, reapply or inspect DGUS `t5uid1` include lines in `~/klipper/src/stm32/Kconfig` and `~/klipper/src/stm32/Makefile` prior to pulling upstream updates.

Usage
```bash
~/printer_data/config/scripts/manage_t5uid1_patches.sh prepare
~/printer_data/config/scripts/manage_t5uid1_patches.sh reapply
~/printer_data/config/scripts/manage_t5uid1_patches.sh status
```

Notes
- `prepare` saves timestamped backups under `~/.dgus_patch_backups/prepare_<ts>/` and removes the DGUS include lines.
- `reapply` adds the include lines back idempotently.

---

### backup_klipper.sh
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

### restore_klipper.sh
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

### git_ignore.sh
Purpose
- Helper to add host-local excludes so your local DGUS files don't show as "dirty" in Git.

Usage
```bash
cd ~/klipper
bash ~/printer_data/config/scripts/git_ignore.sh
git status --porcelain
```

Notes
- This helper creates `.git/info/exclude` entries — it does not create commits.
- If the files listed in git_ignore.sh are not tracked by git, you do not need to run this script. It is only necessary if you are installing from a klipper fork that contains and tracks those files.

---

### test_syntax_host.sh
Purpose
- Convenience script to run `bash -n` against scripts in `~/printer_data/config/scripts` to catch syntax errors.

Usage
```bash
cd ~/printer_data/config/scripts
bash ./test_syntax_host.sh
```

## DGUS Logging Subsystem Overview
The three python (.py) modules in this folder collectively constitute a DGUS logging subsystem.
**Casual users of DGUS-Reloaded can and should ignore these files.**  

The DGUS Logging Subsystem provides a lightweight, host‑side diagnostic pipeline that records Klipper printer state, exports structured logs, and generates human‑readable analysis reports. It is designed to help DGUS‑Reloaded developer/users to debug UI state transitions, filament‑runout behavior, and DGUS/Klipper synchronization issues.

### Components
#### t5uid1_state_logger.py  
Periodically queries the Klipper API for key runtime fields (print state, pause status, virtual SD position, filament sensor status).
Each invocation appends a timestamped snapshot to /tmp/t5uid1_state_log.txt.
This forms the raw data source for all downstream analysis.

#### t5uid1_state_exporter.py  
Converts the raw text log into a structured CSV file at:
~/printer_data/config/t5uid1_state_log_export.csv  
The CSV format is easier to process, sort, filter, and feed into automated tools or spreadsheets.
It is the preferred input for the analyzer.

#### t5uid1_log_analyzer.py  
Loads either the CSV export or the raw text log and performs consistency checks across DGUS and Klipper state fields.
Detects illegal state transitions, DGUS/Klipper page mismatches, pause‑state inconsistencies, and filament‑runout events.  

Produces a detailed HTML report at:
~/printer_data/config/t5uid1_log_report.html

### Typical Workflow
1. Collect state snapshots  
Run t5uid1_state_logger.py manually or via cron/systemd to accumulate printer state entries in /tmp/t5uid1_state_log.txt.

2. Export structured data  
Run t5uid1_state_exporter.py to convert the raw log into a clean CSV dataset.

3. Analyze and report  
Run t5uid1_log_analyzer.py to generate an HTML report summarizing anomalies, warnings, and DEBUG_MARK annotations.

This subsystem is especially useful when diagnosing DGUS‑Reloaded behavior, validating UI page transitions, or investigating intermittent filament‑runout or pause‑state issues on the Klipper host.




