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
| **Mainsail** | Known to work with MainsailOS 1.2.x (Bullseye) and with MainssailOS 2.18.x (Trixie). May also work with other versions.|
---
## How Does It Work?

### Project Structure

DGUS-Reloaded for CR6 consists primarily of two synchronized subsystems:

| Subsystem | Repository | What It Does |
|---|---|---|
| **Klipper Backend** | [This repo](https://github.com/Thinkersbluff/DGUS-Reloaded_for_CR6-Klipper_Component) | t5uid1 Python modules, firmware binaries, config files, scripts, external Pi-Side utilities |
| **Display Firmware** | [DWIN_SET repo](https://github.com/Thinkersbluff/DGUS-reloadedForKlipper_CR6) | Touchscreen UI application |

Both subsystems must be installed and the two must be compatible with each other. Both subsystems are now each released under the same version number, to help users ensure that they have installed the correct versions with each other.  

TIPS: 
 * Users with little or no prior knowledge or experience of Linux systems may find the learning curve a bit steep at first.  I find that AI bots can ease that burden a little.  Be aware, though, that chatbots often make mistakes and it takes us users a little while to discover when we are being led astray...
 * I have included [a complete and detailed set of instructions](Installation_Files/1-Installation_Help_Docs) in this repository, bundled with the files to be installed and configured.
 * These help documents have been structured for ease of use by both novice and advanced users of Linux and Klipper.


## Can I Install This with the Latest Klipper from Klipper3D?
 **Yes!** This project is designed to work with current Klipper releases. I run the latest Klipper with Mainsail 2.18.x and allow Moonraker to update the system automatically.

**Exception:** If Klipper developers refactor in a way that breaks DGUS-Reloaded compatibility, you may need to temporarily pin Klipper to a known-good version until I publish a compatible update. To support this:
- Release notes include the **Git commit hash** of the Klipper version I've tested
- Installation files include scripts for pinning Klipper to specific commits
- Documentation includes guidance on rebuilding firmware when needed

See [Maintenance Documentation](Installation_Files/1-Installation_Help_Docs/README.md) for details.


## Does this work with the latest Mainsail/Moonraker 
As of 14 August 2026, I am running Mainsail 2.18.3 on my system and DGUS-Reloaded 2.0.3 is running fine.
I chose to upgrade from Mainsail 1.2.x to 2.18.3, because:
 * Python 3.9 on which Mainsail 2.1.x was based has gone End of Life
 * I wanted to experiment with using PushOver to transmit alerts to my Apple Watch when the Filament Runout Sensor paused my printer.  That required upgrading to at least Python 3.11, to enable Moonraker to send alerts via Aspire.

The next release of DGUS-Reloaded will include scripts, an  external python module and instructions to enable other users to implement their own notification solution.
I also plan to release a new Migration Guide to outline the workflow by which to preserve your existing customizations and to minimize the efforts required to re-install DGUS-Reloaded after flashing the new MainsailOS to your host.


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

