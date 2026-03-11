# DGUS-Reloaded for CR6: Maintenance Overview

Last Updated: 9 March 2026

## Purpose

This guide helps you maintain and troubleshoot an existing DGUS-Reloaded installation on Klipper.

**Not what you need?**
- For first-time installation instructions → see [1-Installation_Manual.md](1-Installation_Manual.md)
- To better understand how the installed system works → see [2-Understanding_Your_System.md](2-Understanding_Your_System.md)
- To understand what common maintenance tasks to perform, when and how → see [3-Common_Maintenance_Tasks.md](3-Common_Maintenance_Tasks.md)
- For instructions on how to update your existing system to the latest release → see [4-Updating_Existing_Installation.md](4-Updating_Existing_Installation.md)

1. **Find your scenario** in the table below
2. **Follow the linked document** for detailed steps
3. **Consult the appendices** for in-depth procedures
4. **Reference scripts/README.md** for script syntax details

---

## Common Scenarios

| What You're Experiencing | Which Document to Follow |
|---|---|
| **"I want to understand why certain maintenance is needed"** | [2-Understanding Your System](2-Understanding_Your_System.md) |
| **"Moonraker shows Klipper as 'dirty' and won't update"** | [3-Common Maintenance Tasks § Clearing Dirty State](3-Common_Maintenance_Tasks.md#task-2-clearing-dirty-state-for-updates) |
| **"Klipper updated and now shows MCU mismatch warning"** | [3-Common Maintenance Tasks § Rebuilding MCU Firmware](3-Common_Maintenance_Tasks.md#task-4-rebuilding-mcu-firmware-after-host-update) |
| **"Klipper updated and now won't start at all"** | [3-Common Maintenance Tasks § Handling Update Breakage](3-Common_Maintenance_Tasks.md#task-3-handling-update-breakage) |
| **"I want to back up before attempting an update"** | [3-Common Maintenance Tasks § Backup Before Update](3-Common_Maintenance_Tasks.md#task-1-backup-before-update) |
| **"I need to force Klipper to a specific version"** | [Appendix C: Force Klipper Version](appendix/C-Force_Klipper_Version.md) |
| **"I need detailed MCU firmware rebuild steps"** | [Appendix A: Rebuilding MCU Firmware](appendix/A-Rebuilding_MCU_Firmware.md) |
| **"I need to restore a previous backup"** | [Appendix B: Backup & Restore](appendix/B-Backup_Restore_Klipper.md) |
| **"I want script syntax and usage details"** | [scripts/README.md](../scripts/README.md) |

---

## Quick Reference: Essential Commands

| Task | Command |
|---|---|
| Check Klipper git status | `git -C ~/klipper status -sb` |
| Check current commit | `git -C ~/klipper rev-parse --short HEAD` |
| Clear dirty state (before update) | `cd ~/klipper/scripts/dgus-reloaded && ./manage_t5uid1_patches.sh prepare` |
| Reapply patches (before MCU build) | `cd ~/klipper/scripts/dgus-reloaded && ./manage_t5uid1_patches.sh reapply` |
| Back up Klipper | `bash ~/klipper/scripts/dgus-reloaded/backup_klipper.sh` |
| Restore Klipper | `bash ~/klipper/scripts/dgus-reloaded/restore_klipper.sh` |
| Verify installation health | `bash ~/klipper/scripts/dgus-reloaded/verify_installation.sh` |

---

## Document Index

### Core Guides
- [1-Manual_Installation.md](1-Manual_Installation.md) — First-time installation
- [2-Understanding_Your_System.md](2-Understanding_Your_System.md) — System architecture and concepts
- [3-Common_Maintenance_Tasks.md](3-Common_Maintenance_Tasks.md) — Task-oriented workflows

### Appendices (Detailed Procedures)
- [Appendix A: Rebuilding MCU Firmware](appendix/A-Rebuilding_MCU_Firmware.md)
- [Appendix B: Backup & Restore Klipper](appendix/B-Backup_Restore_Klipper.md)
- [Appendix C: Force Klipper Version](appendix/C-Force_Klipper_Version.md)
- [Appendix D: Config Files Reference](appendix/D-Config_Files_Reference.md) *(placeholder)*

### Technical Reference
- [scripts/README.md](../scripts/README.md) — Script syntax and usage

---

## Prerequisites for Maintenance

All maintenance tasks assume:
- SSH access to the Klipper host (typically Raspberry Pi)
- DGUS-Reloaded scripts installed at `~/klipper/scripts/dgus-reloaded/`
- Existing working DGUS-Reloaded installation

If scripts are missing, see [scripts/README.md § Deploying scripts](../scripts/README.md#deploying-scripts-to-the-klipper-host-sftp-first).

---

## Getting Help

If you encounter issues not covered in this guide:
1. Check logs: `~/printer_data/logs/klippy.log`
2. Verify installation health: `bash ~/klipper/scripts/dgus-reloaded/verify_installation.sh`
3. Consult the DGUS-Reloaded GitHub Issues page
