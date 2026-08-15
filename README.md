Last Updated: 14 August 2026


# DGUS-reloaded-Klipper, CR6Community Edition!
Lets you use your stock Creality CR6 display with Klipper firmware, restoring touchscreen functionality after converting your printer to Klipper.

### NOTE: If you don’t want to use the stock display, you do not need this firmware.  Just install the latest Klipper from [Klipper3D.org](https://www.klipper3d.org/).
---
## Supported Hardware

| Component | Compatibility |
|---|---|
| **Displays** | CR6-SE/MAX stock DWIN touchscreen |
| **Motherboards** | Creality 4.5.2, 4.5.3, ERA 1.1.0.3, BTT SKR CR6 V1.0 |
| **Klipper Host** | Raspberry Pi 3B+ or newer (or equivalent) |
| **OS** | Debian-based Linux (MainsailOS, FluiddPi, etc.) |
| **Mainsail** | Known to work with MainsailOS 1.2.x (Bullseye). Some Pi-Side scripts may require repair to work with MainsailOS 1.3.x+ (Bookworm) |
---
## How Does It Work?

### Project Structure

DGUS-Reloaded for CR6 consists of two synchronized components:

| Component | Repository | What It Does |
|---|---|---|
| **Klipper Backend** | [This repo](https://github.com/Thinkersbluff/DGUS-Reloaded_for_CR6-Klipper_Component) | t5uid1 Python modules, firmware binaries, config files |
| **Display Firmware** | [DWIN_SET repo](https://github.com/Thinkersbluff/DGUS-reloadedForKlipper_CR6) | Touchscreen UI application |

Both components must be installed and the two must be compatible with each other (see release notes).  

You install standard Klipper as usual, then integrate DGUS-Reloaded to enable the display:
   1. Flash the DWIN_SET firmware to your display*
   2. Install the t5uid1 extras and stable_z_home add-on to Klipper
   3. Flash the Klipper firmware binary to your motherboard
   4. Copy and configure the printer.cfg and companion configuration files
   5. (Optional) Configure your slicer for progress display integration


## Can I Install This with the Latest Klipper from Klipper3D?
 **Yes!** This project is designed to work with current Klipper releases. I run the latest Klipper and allow Moonraker to update automatically.

**Exception:** If Klipper developers refactor in a way that breaks DGUS-Reloaded compatibility, you may need to temporarily pin Klipper to a known-good version until I publish an update. To support this:
- Release notes include the **Git commit hash** of the Klipper version I've tested
- Installation files include scripts for pinning Klipper to specific commits
- Documentation includes guidance on rebuilding firmware when needed

See [Maintenance Documentation](Installation_Files/1-Installation_Help_Docs/README.md) for details.


## Does this work with the latest Mainsail/Moonraker 
 **TBD**
 Up until 12 August 2026, I ran this system successfully on Bullseye, unaware of Bookworm.
 When I tried to install PushOver and activate notifications, I hit a brick wall with Moonraker.
 Activating PushOver alerts (e.g. when M600 is fired) requires upgrading to BookWorm, which in turn requires reflashing Mainsail and reinstalling DGUS-Reloaded.
 I am presently reviewing the impacts to this project of upgrading my own development system to Bookworm.

 ### Backgrounder

 ⚠️ DGUS‑Reloaded works on any Klipper/Moonraker system, but Moonraker’s feature set depends on the installed OS.

**MainsailOS 1.2.x (Bullseye)**

 * Python 3.9

 * Older Moonraker build

 ❌ No notifications system

 ❌ No PushOver / Telegram / Discord / Email alerts

 ❌ No install-moonraker-notifications.sh script

 ✔ DGUS‑Reloaded firmware works normally

 ⚠️ Pi‑side scripts written for Python 3.9 may break when upgrading

**MainsailOS 1.3.x+ (Bookworm)**

 * Python 3.11

 * New Moonraker components

 ✔ Full notifications support

 ✔ PushOver alerts (e.g., when M600 triggers)

 ✔ Webhooks for Apple Shortcuts

 ✔ DGUS‑Reloaded firmware works normally


⚠️ CAUTION: Pi‑side scripts may require updates after upgrading to Python 3.11

If you need Moonraker notifications (PushOver, etc.), you must run MainsailOS Bookworm.
Bullseye cannot load Moonraker’s notifications plugin.

Upgrading from Bullseye → Bookworm requires reflashing the SD card with a fresh MainsailOS Bookworm image.  This is a full OS upgrade; MainsailOS does not support in‑place upgrades between Debian major versions.

After reflashing, restore your /home/pi/printer_data/ folder and reinstall DGUS‑Reloaded.

---

# Ready to Install?

👉 **[Start with the Installation Guide](Installation_Files/1-Installation_Help_Docs/README.md)**

The guide includes:
- Installation Manual (step-by-step with full control)
- Maintenance procedures (updates, troubleshooting, backups)
- Recovery workflows (when updates break compatibility)

---

**Want more context?** Expand the sections below for backstory, credits, and useful references.

<details>
<summary><strong>Backstory and Credits</strong></summary>

The Klipper in this repo is an old fork of Klipper3D/Master, which was modified [by Desuuuu](https://github.com/Desuuuu/klipper), to work with his version of the DGUS-reloaded python application (t5uid1) and a matching DWIN_SET application. 

I found Desuuuu's DGUS-Reloaded project while searching for a way to preserve touchscreen functionality on my CR6-SE after converting to Klipper.

Desuuu had at that time just decided to archive his project, so I decided to fork his project and adapt it to my own needs. 
I also try to maintain and share the python app, and Mainsail/Klipper configuration files here in this repository, to allow others with CR6 printers and similar machines to adopt or tailor my firmwares for your own purposes.

## Why Not Just Use the Desuuuu version of the Modified DGUS-Reloaded Klipper?

1. Most importantly, because Desuuuu has archived his dgus-reloaded-klipper fork, parts of which no longer work with the latest Klipper. 

2. To enable the CR6 UI functionality, I needed to edit a few of Desuuu's t5uid1 application files, so I needed to make my own (this) fork of those files.

</details>








 
 <details>
<summary><strong>How to Contribute To This Project</strong></summary>

Please feel free to contribute ideas and feedback in the Discussions section.

Since some of the behaviour of the DGUS-Reloaded UI is controlled by the DWIN_SET app and some by this Klipper back-end, it will be "cleaner" to keep all Issues together on one repo.  If you believe you have found a bug in the way the DGUS-Reloaded UI works on your CR6 printer, please therefore navigate to [the Issues folder on the DWIN_SET repo](https://github.com/Thinkersbluff/DGUS-Reloaded_for_CR6-DWIN-SET_Component/issues).  If there is no existing open or closed Issue that describes the same issue, then please raise a new Issue there.  

CR6Community Firmware features NOT present in this release may be developed in future releases, but no schedule commitment is possible for such extensions.  Users who are able to define and develop such modifications are welcome to fork this repository and to submit Pull Requests or to open Discussions or Issues as appropriate, to propose those changes.

> **If there are CR6Community members who are both capable and willing to take on the challenge of helping to future-proof this fork, please let me know in the Discussions section of this repo.  I am certainly open to reviewing PRs.**
</details>

<details>
<summary><strong>Is There Another Way to Re-Activate My Stock CR6 Display on Klipper?</strong></summary>

If figuring out how to install and configure your system to work with this firmware is too difficult for you, but you still want a way to reuse your stock CR6 DWIN display, you may prefer trying [this alternative approach](https://github.com/Thinkersbluff/Klipper-dgus_CR6), which uses a separate serial interface to the display and the Moonraker API.  I only have the bandwidth to focus on this project or that one, but it is in my mind to try to someday develop a single DWIN_SET app that is compatible with either serial interface solution, if such a thing is desireable and possible.    
</details>

<details>
<summary><strong>Recommended References</strong></summary>
To learn more about Klipper3d.org and about the DGUS-RELOADED project, you are strongly encouraged to follow these links:

### All about Klipper3D, in their own words  
[![Klipper](docs/img/klipper-logo-small.png)](https://www.klipper3d.org/)  https://www.klipper3d.org/

### The DGUS-RELOADED Klipper Project, by Desuuuu  
 https://github.com/Desuuuu/Klipper
 
#### Additional useful info is available in the Desuuuu/DGUS-reloaded-Klipper-config Wiki
* [Flashing the firmware](https://github.com/Desuuuu/DGUS-reloaded-Klipper/wiki/Flashing-the-firmware)
* [Print status](https://github.com/Desuuuu/DGUS-reloaded-Klipper/wiki/Print-status)
* [Print progress display](https://github.com/Desuuuu/DGUS-reloaded-Klipper/wiki/Print-progress-display)

 ### The Klipper-DGUS project, by SEHO85 (BUZZ-T on the CR6Community Discord)
 This project is the "alternative approach" to which I refer, above.
  - His GitHub project is here: https://github.com/seho85/klipper-dgus
  - The CR6-compatible fork of his DWIN_SET UI is here: https://github.com/Thinkersbluff/Klipper-dgus_CR6
  
</details>

