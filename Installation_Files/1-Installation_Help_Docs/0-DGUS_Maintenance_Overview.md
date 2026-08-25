# DGUS-Reloaded for CR6: Maintenance Overview

Last Updated: 5 May 2026

## Purpose

This guide helps you maintain and troubleshoot an existing DGUS-Reloaded installation on Klipper.

**Not what you need?**
- For first-time installation instructions → see [1-Installation_Manual.md](1-Installation_Manual.md)
- To better understand how the installed system works → see [2-Understanding_Your_System.md](2-Understanding_Your_System.md)
- To understand what common maintenance tasks to perform, when and how → see [3-Common_Maintenance_Tasks.md](3-Common_Maintenance_Tasks.md)
- For instructions on how to update your existing DGUS-Reloaded system to the latest release → see [4-Updating_Existing_Installation.md](4-Updating_Existing_Installation.md)
- For instructions on how to update Mainsail 1.2.x (Bullseye) to Mainsail 1.3.x (Bookworm) → see [5-Upgrade_Guide-Bullseye_to_Bookworm.md](5-Upgrade_Guide-Bullseye_to_Bookworm.md)

1. **Find your scenario** in the table below
2. **Follow the linked document** for detailed steps
3. **Consult the appendices** for in-depth procedures
4. **Reference scripts/README.md** for script syntax details

---

## Common Scenarios

| What You're Experiencing | Which Document to Follow |
|---|---|
| **"I want to understand why certain maintenance is needed"** | [2-Understanding Your System](2-Understanding_Your_System.md) |
| **"I want to add macros to my DGUS menu"** | [2-Understanding Your System § Custom Macro Menus](2-Understanding_Your_System.md#custom-macro-menus-via-dgus_menu_macroscfg) |
| **"I want to validate or adjust my belt tension"** | [3-Common Maintenance Tasks § Validate Belt Tension](3-Common_Maintenance_Tasks.md#task-7-validate-and-adjust-belt-tension-using-travel-tests) |
| **"Moonraker shows Klipper as 'dirty' and won't update"** | [3-Common Maintenance Tasks § Clearing Dirty State](3-Common_Maintenance_Tasks.md#task-2-clearing-dirty-state-for-updates) |
| **"Klipper updated and now shows MCU mismatch warning"** | [3-Common Maintenance Tasks § Rebuilding MCU Firmware](3-Common_Maintenance_Tasks.md#task-4-rebuilding-mcu-firmware-after-host-update) |
| **"Klipper updated and now won't start at all"** | [3-Common Maintenance Tasks § Handling Update Breakage](3-Common_Maintenance_Tasks.md#task-3-handling-update-breakage) |
| **"I want to back up before attempting an update"** | [3-Common Maintenance Tasks § Backup Before Update](3-Common_Maintenance_Tasks.md#task-1-backup-before-update) |
| **"I want help to test my belt tension"** | [Appendix F: Travel Test Macros Reference](appendix/F-Travel_Test_Macros_Reference.md) |
| **"I need to force Klipper to a specific version"** | [Appendix C: Force Klipper Version](appendix/C-Force_Klipper_Version.md) |
| **"I need detailed MCU firmware rebuild steps"** | [Appendix A: Rebuilding MCU Firmware](appendix/A-Rebuilding_MCU_Firmware.md) |
| **"I need to restore a previous backup"** | [Appendix B: Backup & Restore](appendix/B-Backup_Restore_Klipper.md) |
| **"I want script syntax and usage details"** | [scripts/README.md](../scripts/README.md) |
| **"I need help to implement/debug the automatic recovery feature"** | [Appendix E: Pi-Side Recovery Setup](appendix/E-Pi-Side_Recovery_Setup.md) |
| **"I need to upgrade my MainsailOS and want to migrate the existing DGUS-Reloaded installation "** | [5-Upgrading_Existing_MainsailOS_Installation](5-Upgrading_Existing_MainsailOS_Installation.md)|
| **"I need to find a spare GPIO signal pin OR I need to validate/correct an existing pin definition in my printer.cfg"** | [Appendix G: GPIO Pin Data](appendix/G-GPIO_Pin_Data.md) |

---

## Quick Reference: Essential Commands

| Task | Command |
|---|---|
| Check Klipper git status | `git -C ~/klipper status -sb` |
| Check current commit | `git -C ~/klipper rev-parse --short HEAD` |
| Clear dirty state (before update) | `bash ~/printer_data/config/scripts/manage_t5uid1_patches.sh prepare` |
| Reapply patches (before MCU build) | `bash ~/printer_data/config/scripts/manage_t5uid1_patches.sh reapply` |
| Back up Klipper | `bash ~/printer_data/config/scripts/backup_klipper.sh` |
| Restore Klipper | `bash ~/printer_data/config/scripts/restore_klipper.sh` |
| Run X-axis belt tension test | `X_TRAVEL_TEST` (basic) or `X_TRAVEL_TEST_WITH_TMC` (BTT boards) |
| Run Y-axis belt tension test | `Y_TRAVEL_TEST` (basic) or `Y_TRAVEL_TEST_WITH_TMC` (BTT boards) |
| Capture TMC driver diagnostics | `TMC_SNAPSHOT` |

---

## Document Index

### Core Guides
- [1-Installation_Manual.md](1-Installation_Manual.md) — First-time installation
- [2-Understanding_Your_System.md](2-Understanding_Your_System.md) — System architecture and concepts
- [3-Common_Maintenance_Tasks.md](3-Common_Maintenance_Tasks.md) — Task-oriented workflows

### Appendices (Detailed Procedures)
- [Appendix A: Rebuilding MCU Firmware](appendix/A-Rebuilding_MCU_Firmware.md)
- [Appendix B: Backup & Restore Klipper](appendix/B-Backup_Restore_Klipper.md)
- [Appendix C: Force Klipper Version](appendix/C-Force_Klipper_Version.md)
- [Appendix D: Slicer_Integration_Tips](appendix/D-Slicer_Integration_Tips.md)
- [Appendix E: Pi-Side Recovery Setup](appendix/E-Pi-Side_Recovery_Setup.md)
- [Appendix F: Travel Test Macros Reference](appendix/F-Travel_Test_Macros_Reference.md)
- [Appendix G: GPIO Pin Data](appendix/G-GPIO_Pin_Data)]

### Technical Reference
- [scripts/README.md](../scripts/README.md) — Script syntax and usage

---

## Prerequisites for Maintenance

All maintenance tasks assume:
- SSH access to the Klipper host (typically Raspberry Pi)
- DGUS-Reloaded scripts installed at `~/printer_data/config/scripts/`
- Existing working DGUS-Reloaded installation

If scripts are missing, see [scripts/README.md § Deploying scripts](../scripts/README.md#deploying-scripts-to-the-klipper-host-sftp-first).

---

## Getting Help

If you encounter issues not covered in this guide:
1. Check logs: `~/printer_data/logs/klippy.log`
2. Consult the DGUS-Reloaded GitHub Issues page
