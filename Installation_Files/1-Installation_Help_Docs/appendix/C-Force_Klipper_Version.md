Last Updated: 8 March 2026
# Why Force Klipper to a known compatible commit?

If Mainsail displays an error after you update the Klipper firmware, you may need to roll-back that update to an earlier known "compatible" commit.

We strongly recommend that you always back up your klipper system, if it continues to work after an update. [see 4-Backup_Restore_Klipper.md](4-Backup_Restore_Klipper.md)

If you did not do that backup, this process should at least help you roll-back klipper to the version we used to validate the installed release of t5uid1. 

# WARNING:
>Performing a hard reset of klipper on your host will overwrite any edits you have made to any local klipper files that are tracked by git. (So, not the t5uid1 files or the dgus-reloaded scripts, for instance, but yes the python modules, config file, etc..)  

>**You must understand and accept that if you do this, 
it is at your own risk.**

## How to Force Klipper to a Known Compatible Version

### Prerequisites
- SSH access to your Pi
- Release Notes for DGUS-Reloaded with the target Klipper SHA

### Process

If you need to roll back the klipper on your host to a version of Klipper that has been tested and confirmed compatible with DGUS-Reloaded for CR6, perform this sequence of tasks: 

1. SSH into your Pi
2. Copy/paste the script below into the SSH window, but do not hit return, yet, for that last command line
3. Copy the full-SHA of the target klipper version from the Release Notes 
4. Paste that full-SHA into the last line of that script, replacing the placeholder string '<full-SHA>'. Do NOT include the '<>' characters.
5. Hit return to run that hard reset command

```bash
cd ~/klipper
git fetch --all --tags
git reset --hard <full-SHA>
```
6.  Verify the reset was successful by confirming the commit SHA:

```bash
git rev-parse --short HEAD
```
Compare the output to the SHA prefix in your Release Notes. They should match.

If you also need to build a new klipper.bin file, then proceed with steps 7-11. If the existing klipper.bin file is compatible with the reset klipper version, skip to step 12:

7. copy/paste this script into your SSH window, to reapply the edits to Kconfig and Makefile before running make menuconfig:
```bash
~/printer_data/config/scripts/manage_t5uid1_patches.sh reapply
```
8. copy/paste this script into your SSH window, to verify the settings that will be used when you run "make":
   
```bash
cd ~/klipper
make menuconfig
```
Exit menuconfig, then save if prompted.

9. copy/paste this script into your SSH window, to build a new klipper.bin file:

```bash
make clean
make
```
10. Copy klipper/out/klipper.bin to an SD card (e.g. using an SFTP tool)
11. Rename klipper.bin if/as required and flash to your motherboard.
    
12. Copy/paste this script into the SSH window on your pi:
```bash
FIRMWARE_RESET
```
13. In the Mainsail window, verify that Klipper connects to the printer without error. 
14. Run this script on your pi, to remove the changes from Kconfig and Makefile:  

``` bash
~/printer_data/config/scripts/manage_t5uid1_patches.sh prepare
```
15. Select Check for Updates in the Mainsail Update Manager window

### Expected Outcome
Mainsail shows klipper as "clean" (no dirty flag) at the target version.