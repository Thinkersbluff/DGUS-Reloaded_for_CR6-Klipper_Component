# DGUS-reloaded-Klipper (modified), CR6Community Edition!
The Klipper in this repo is a fork of Klipper3D/Master, which has been modified - [largely by Desuuuu](https://github.com/Desuuuu/klipper), and a little bit more by me - to work with the DGUS-reloaded DWIN_SET for CR6 printers located in [this companion repo.](https://github.com/Thinkersbluff/DGUS-reloadedForKlipper_CR6)

This repo was forked from [the master DGUS-RELOADED project repository](https://github.com/Desuuuu/Klipper).
The Desuuuu repo is in-turn forked from [the master Klipper3D.org github repository.](https://github.com/Klipper3d/klipper/)

>>**NOTE:** Desuuuu has also indicated that he intends to stop maintaining his dgus-reloaded-klipper fork, soon, so I am looking for CR6Community help to maintain and extend this fork. (See **How to Contribute**, below)

## Who should __NOT__ use this firmware?
If your goal is to run Klipper on your CR6 without using the stock T5L DWIN display hardware, **then you do not need this modified version of Klipper.**
Just install the master Klipper3D.org version and configure it for your CR6 printer per the [Klipper3d.org installation and configuration documentation](https://github.com/Klipper3d/klipper/blob/master/docs/index.md).

This repository may also be very helpful to get you started with Klipper on the CR6: https://github.com/KoenVanduffel/CR-6_Klipper

## Why Not Just Use the Desuuuu version of the Modified DGUS-Reloaded Klipper?
Some of the functionality implemented in the CR6-specific UI is either not present or is organized differently, in the Desuuuu companion display app.

1. Perhaps most importantly, Desuuuu has indicated that he intends to stop maintaining his dgus-reloaded-klipper fork. 

2. To enable the CR6 UI functionality, it is necessary to edit a few of the Desuuuu/Klipper files, for which I needed to make my own (this) fork of the t5uid1 application files.

Given both points 1 and 2 above, negotiating a common standard interface in both versions of DGUS-Reloaded was not a practical option.

## Is This Klipper Fork Using the latest Klipper3D/master version?
Sort of...
As of Jan 2023: 
- the latest release of Klipper is 0.11.0, available 28 Nov 2022.
- the Desuuuu fork was last updated with Klipper 0.10.0, available 29 Sept 2022.
- On 25 Jan 2023, Thinkersbluff was able to update the Klipper in this fork to 0.11.0, by merging this repo with [another fork of Klipper3D/Master maintained by gbkwiatt](https://github.com/gbkwiatt/klipper)

Worst-case, however, this solution may someday be limited to exploiting [the features and capabilities of Klipper at the last release with which we were able to merge without conflict](https://github.com/Thinkersbluff/dgus-reloaded_klipper/blob/DGUS-ReloadedForCR6/docs/Releases.md). 
e.g. At some future release of Klipper, changes to the klipper.bin or Make Menuconfig functionality may render the pre-built klipper.bin files available here non-functional.

Unfortunately, Moonraker flags installations of this repo (e.g. by configuring KIAUH to install Klipper from this repo instead of from the Klipper3D/Master github) as being "Invalid", which can be irritating.


## Is It Possible Instead to Install the Latest Klipper from Klipper3D/master and STILL Use DGUS-Reloaded for CR6?
Yes, actually! (Sort of...)

In Feb 2023, Thinkersbluff found that it is NOT actually necessary to use ALL of this modified Klipper, to make the DGUS-Reloaded display function work.

Instead, one really only needs to 
1. Download and flash the applicable klipper.bin file for the motherboard in your printer
2. Install the latest Klipper from Klipper3D/master (and Mainsail and Moonraker, all using KIAUH, per their documentation)
3. Install (into ~/printer_data/config on your host processor) the files located in the "Overwrite these Klipper host files" subfolder applicable to your motherboard, and configure them for your specific printer/preferences. (NOTE: You can do this via the Mainsail MACHINE tab, rather than messing about with SFTP and nano, for this part)
4. Copy the t5uid1 folder and contents into the ~/klipper/klippy/extras directory on your host (e.g. by using an SFTP program logged into your host, to transfer those files from where you extracted the downloaded release zip file on your system.)

After that, Moonraker will "happily" maintain your Klipper installation, without overwriting t5uid1.  
If, however, t5uid1 is updated, you may have to manually update your system, per step 4 above.


## A Word Of Warning About Klipper Documentation
Please note that Klipper3D are very good about keeping [their online documentation](https://www.klipper3d.org/) up to date with their latest firmware.
This repo, however, is NOT up-to-the-minute with every change they release.  That latency can mean that some of their online instructions do not work with this version of Klipper.  The documentation in this repo is, however, "frozen" at the most recent version of Klipper with which we have merged.  

I recommend that you ALWAYS:
 - use [this local copy of their documentation](https://github.com/Thinkersbluff/DGUS-Reloaded_for_CR6-Klipper_Component/blob/DGUS-ReloadedForCR6/docs/Overview.md), when seeking guidance on how this particular version of modified Klipper is used, if you have decided to install from here and not from Klipper3D/master.
 - use [the online Klipper documentation](https://www.klipper3d.org/), if you have installed Klipper from Klipper3D/master.
 
 ## How to Contribute To This Project

Please feel free to contribute ideas and feedback in the Discussions section.

Since some of the behaviour of the DGUS-Reloaded UI is controlled by the DWIN_SET app and some by this Klipper back-end, it will be "cleaner" to keep all Issues together on one repo.  If you believe you have found a bug in the way the DGUS-Reloaded UI works on your CR6 printer, please therefore navigate to [the Issues folder on the DWIN_SET repo](https://github.com/Thinkersbluff/DGUS-Reloaded_for_CR6-DWIN-SET_Component/issues).  If there is no existing open or closed Issue that describes the same issue, then please raise a new Issue there.  

CR6Community Firmware features NOT present in this release may be developed in future releases, but no schedule commitment is possible for such extensions.  Users who are able to define and develop such modifications are welcome to fork this repository and to submit Pull Requests or to open Discussions or Issues as appropriate, to propose those changes.

 One "future-proofing" option that comes to mind, for instance, is to pre-compile the Klipper.bin files and package the actual UI interface component (klippy/extras/t5uid1) as a py wheel to be installed into the Klipper3D/master version of Klipper with pip. 

> **If there are CR6Community members who are both capable and willing to take on the challenge of helping to future-proof this fork, please let me know in the Discussions section of this repo.  I am certainly open to reviewing PRs.**


## Is There Another Way to Re-Activate My Stock CR6 Display on Klipper?

If figuring out how to install and configure your system to work with this firmware is too difficult for you, but you still want a way to reuse your stock CR6 DWIN display, you may prefer trying [this alternative approach](https://github.com/Thinkersbluff/Klipper-dgus_CR6), which uses a separate serial interface to the display and the Moonraker API.  I only have the bandwidth to focus on this project or that one, but it is in my mind to try to someday develop a single DWIN_SET app that is compatible with either serial interface solution, if such a thing is desireable and possible.    

## Recommended References
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
  
