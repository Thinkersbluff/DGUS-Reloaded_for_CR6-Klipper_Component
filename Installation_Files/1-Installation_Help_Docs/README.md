Last Updated: 25 August 2026

# Introduction

## Scope
This section organizes and provides the Installation and Maintenance Help documentation for DGUS-Reloaded for CR6 on Klipper.

## Assumptions
These documents assume that the user is:
- using a Debian-based Linux operating system on the Klipper Host for their system.
- willing and able to install the suggested applications (or equivalents) to facilitate the installation process.
- comfortable with copying scripts from Help Docs and pasting those into an SSH application window, and running them.
- comfortable with using an SFTP tool (like FileZilla) to interactively manage the file system on their Klipper host and to transfer files back & forth between the Klipper host and their computer.
- familiar with basic concepts which enable understanding and following these documents as written.

NOTE: That last assumption is my way of saying that sometimes, these help docs may assume that you know something and therefore may not mention or discuss it.
If you find something in these docs to be "mystifying", I recommend that you explore your confusion with an AI bot like ChatGPT. (no joke)  The Microsoft CoPilot AI and the GitHub CoPilot AI have been of enormous help to me on this project, filling in my knowledge gaps.

---

# Document Organization

## About the File Numbering
I use numbers in each of the document titles to enforce the order in which I want the titles to be listed. I recommend that you begin by reviewing the scope and purpose of these documents in that numbered order to understand the gist of what you will be doing, and how.

---

# Core Documentation

## 0-DGUS_Maintenance_Overview.md
**Start here.**

This is the main entry point for all installation and maintenance tasks. It provides:
- A scenario-based index (find your problem → get pointed to the right document)
- Quick reference command table
- Links to all other documents in this set

**Use this when:**
- You're experiencing issues and need to troubleshoot
- You want to understand what maintenance tasks exist
- You need to find a specific procedure quickly

---

## 1-Installation_Manual.md
**First-time installation.**

If you are comfortable with using Linux and/or an SFTP tool to add/delete/modify files and directories on the Klipper host, you will likely find the manual installation process to be a quick, easy, and safe way to install DGUS-Reloaded into an existing Klipper-based system.   

If you decide to jump straight into installing Mainsail and Klipper and DGUS-Reloaded all on the same day, we can help you do that, too. If this is your first experience with Klipper, though, we do strongly recommend that you first install Klipper and Mainsail (or Fluidd), figure out how that works, and then come back to extend that system with DGUS-Reloaded.

This document walks you through:
- Installing Klipper + Mainsail/Fluidd on your Pi
- Flashing the DWIN_SET firmware to the CR6 display
- Installing DGUS-Reloaded extras and add-ons
- Flashing Klipper firmware to your motherboard
- Configuring and verifying the installation

**Use this when:**
- Performing a first-time install
- You prefer manual control over each step
- You want to understand exactly what's happening at each stage

> **NOTE:** If you already have a full system installed and want to update to a newer DGUS-Reloaded release, you can instead skip straight to the document [4-Updating_Existing_Installation.md](4-Updating_Existing_Installation.md).

---

## 2-Understanding_Your_System.md
**Contextual backgrounder: how the pieces fit together.**

This document explains the **why** behind the maintenance tasks. It covers:
- The Klipper architecture (host vs MCU split)
- How updates work (Moonraker, Git, upstream tracking)
- What "dirty" repos mean and why they block updates
- Why DGUS-Reloaded requires patches to tracked files
- MCU firmware vs host software versioning

**Use this when:**
- You want to understand why certain maintenance is needed
- Moonraker/Mainsail behavior seems confusing
- You're seeing "dirty" warnings and want context
- You're curious how the system works under the hood

This is **not** a task guide—it's educational context. For actual tasks, see documents 3 or 4.

---

## 3-Common_Maintenance_Tasks.md
**Task-oriented maintenance workflows.**

This is your **do this now** guide. It includes:
- Quick health checks
- Backing up before risky changes
- Clearing "dirty" status for Moonraker updates
- Reapplying DGUS patches before MCU builds
- Recovering after update breakage
- Rebuilding MCU firmware after host changes
- Final verification steps

**Use this when:**
- You need to perform a specific maintenance task
- Moonraker says Klipper is "dirty"
- Klipper updated and now shows errors/warnings
- You need to rebuild MCU firmware

Each task includes:
- When to use it
- Why it's needed
- Step-by-step commands
- Expected outcomes
- Links to appendices for detailed procedures

---

## 4-Updating_Existing_Installation.md
**Safe release-to-release update path.**

Use this guide when your printer is already running DGUS-Reloaded and you want to move to a newer  release.

This document provides:
- Pre-update backup steps
- How to apply new release files
- When/how to update Klipper host software
- When/how to rebuild MCU firmware
- Final verification checklist

**Use this when:**
- A new DGUS-Reloaded release is published
- You want to update from one DGUS version to another
- Release notes direct you to update

This is the **primary update playbook**—it orchestrates multiple maintenance tasks (documented in #3 and appendices) into a safe update workflow.

---

## 5-Upgrading_Existing_MainsailOS_Installation.md
**Safe MainsailOS-to-MainsailOS upgrade path.**

Use this guide when your printer is already running DGUS-Reloaded and you want to upgrade to a newer  release of MainsailOS.

This document provides:
- Pre-upgrade backup steps
- How to perform the MainsailOS upgrade
- Upgraded Host verification checklist
- How to restore DGUS-Reloaded to the upgraded system (including Pi-Side scripts)
- DGUS-Reloaded verification checklist
- When/how to update Klipper host software
- When/how to rebuild MCU firmware
- Final verification checklist

**Use this when:**
- You want to update the Python on your host (e.g. from 3.9 to 3.11 or higher)
- You want to make use of new Moonraker features that depend on a higher version of Python
- Release notes declare dependency on a higher version of MainsailOS than you have installed

---

# Appendices (Detailed Procedures)

The appendices contain **in-depth step-by-step procedures** for complex tasks. They are referenced by the core maintenance documents but can also be used standalone.

## appendix/A-Rebuilding_MCU_Firmware.md
**Detailed MCU firmware rebuild procedure.**

Covers:
- When and why to rebuild
- Step-by-step build process:
  - Applying DGUS patches
  - Running `make menuconfig`
  - Building the firmware
  - Flashing to motherboard
  - Cleaning patches afterward
- Board-specific flashing instructions
- Troubleshooting build errors

**Referenced by:**
- Document 3 (Task 5: Rebuild MCU Firmware)
- Document 4 (Step 5: Update workflow)

---

## appendix/B-Backup_Restore_Klipper.md
**Backup and restore procedures.**

Covers:
- Creating backups before risky operations
- Restoring from backup after failures
- Verifying backup integrity
- Troubleshooting restore issues

**Referenced by:**
- Document 3 (Task 1: Backup; Task 4: Recovery)
- Document 4 (Step 1: Pre-update backup)

---

## appendix/C-Force_Klipper_Version.md
**Emergency rollback to known-good commit.**

Covers:
- When to use this (recovery path, not routine maintenance)
- Finding the target SHA from release notes
- Using `git reset --hard` safely
- Verifying the rollback succeeded
- Warnings about when NOT to use this

**Referenced by:**
- Document 3 (Task 4: Recovery Option B)
- Document 4 (Step 4: Pin/rollback if directed)

---

## appendix/D-Slicer_Integration_Tips.md
**Configuration file reference guide.** *(Placeholder for future expansion)*

Will eventually cover:
- Purpose of each `.cfg` file in `~/printer_data/config/`
- Critical settings to review
- Board-specific differences
- Common customization patterns

---

## appendix/E-Pi-Side_Recovery_Setup.md


---

# Technical Reference

## ../scripts/README.md
**Script syntax and usage details.**

This is the **technical reference manual** for all DGUS-Reloaded scripts. For each script, it documents:
- Purpose and when to use it
- Command-line syntax
- Expected behavior
- Cross-references to task documents that use the script

**Use this when:**
- You need exact script syntax
- You want to understand what a script does before running it
- You're troubleshooting script behavior

This is **not** a task guide—it's a reference. For workflows, see documents 3 or 4.

---

# Optional Integration

## [Optional]Slicer_Integration_Tips
It is not absolutely necessary to modify your slicer to use DGUS-Reloaded for CR6. I do, however, recommend that you at least enable M73 messaging so that you will see displays of % print progress and print time remaining.

I don't have the bandwidth or energy to figure out how to integrate multiple slicers, so I only provide tips for the slicer I am using. At the moment, that slicer is Ultimaker Cura.

I am always happy to accept similar tips for other slicers from the user community, which I will copy to this folder.

---

# Document Flow Examples

## New User (First Install)
1. Read **1-Installation_Manual.md** 
2. Optionally consult **2-Understanding_Your_System.md**, if confused about concepts
3. Follow install steps
4. Bookmark **0-DGUS_Maintenance_Overview.md** for future use

## Existing User (Updating to New Release)
1. Read new release notes
2. Follow **4-Updating_Existing_Installation.md**
3. If recovery needed → follow links to **3-Common_Maintenance_Tasks.md** or appendices

## Existing User (Troubleshooting)
1. Start at **0-DGUS_Maintenance_Overview.md**
2. Find your scenario in the index
3. Follow link to **3-Common_Maintenance_Tasks.md** (or appendix)
4. If background needed → consult **2-Understanding_Your_System.md**

## Experienced User (Just Need Command Syntax)
1. Go directly to **../scripts/README.md**
2. Find script → get syntax
3. Run command

---

# Quick Reference Index

| I Need To... | Start Here |
|---|---|
| Install for the first time | [1-Installation_Manual.md](1-Installation_Manual.md) |
| Update to a new DGUS release | [4-Updating_Existing_Installation.md](4-Updating_Existing_Installation.md) |
| Understand how the system works | [2-Understanding_Your_System.md](2-Understanding_Your_System.md) |
| Troubleshoot an issue | [0-DGUS_Maintenance_Overview.md](0-DGUS_Maintenance_Overview.md) |
| Perform a specific maintenance task | [3-Common_Maintenance_Tasks.md](3-Common_Maintenance_Tasks.md) |
| Rebuild MCU firmware | [appendix/A-Rebuilding_MCU_Firmware.md](appendix/A-Rebuilding_MCU_Firmware.md) |
| Back up or restore Klipper | [appendix/B-Backup_Restore_Klipper.md](appendix/B-Backup_Restore_Klipper.md) |
| Rollback to a specific Klipper version | [appendix/C-Force_Klipper_Version.md](appendix/C-Force_Klipper_Version.md) |
| Look up script syntax | [../scripts/README.md](../scripts/README.md) |
