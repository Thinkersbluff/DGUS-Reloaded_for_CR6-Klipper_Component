CAUTION: When the following README was originally drafted, I expected that users would be installing this fork of Klipper to install DGUS-Reloaded.
Over the past year, it has become clear that:
1. It is neither possible nor necessary to keep this fork up to date with the Master branch at Klipper3D.org
2. Users can and should instead perform and maintain a clean copy of the latest Klipper on their systems, and install/maintain the DGUS-Reloaded t5uiud1 application files as if it was a "Plug-In"
3. For as long as the firmware.bin file included with this distribution continues to work with Klipper, there is no need to use Make Menuconfig to compile a new firmware.bin at each new release of Klipper.  In fact, one could not create a firmware.bin file that works with the DGUS-Reloaded DWIN_SET firmware from any other version of Klipper than the obsolete version on this repository.

As summarized in the DWIN_SET repository Readme, I recommend that you install and configure Mainsail and Klipper on your system first, and then return to the DWIN_SET component repository, to flash and integrate the stock TFT display into your system.


# DGUS-reloaded-Klipper, CR6Community Edition!
The Klipper in this repo is an old fork of Klipper3D/Master, which was modified [by Desuuuu](https://github.com/Desuuuu/klipper), to work with his version of the DGUS-reloaded python application (t5uid1) and a matching DWIN_SET application. 

I found Desuuu's DGUS-Reloaded project while I was searching for a way to preserve/restore some level of functionality to the stock TFT display on my CR6-SE printer, after converting the printer to Klipper.

Desuuu had at that time just decided to archive his project, so I decided to fork his project and adapt it to my own needs. 
I also try to maintain and share the python app, and Mainsail/Klipper configuration files here in this repository, to allow others with CR6 printers and similar machines to adopt or tailor my firmwares for you own purposes.

## PLEASE NOTE: The Klipper files on this repository are out of date and should not be installed onto your system, unless you are trying to run Make Menuconfig to build a custom klipper.bin file for a non-CR6 printer.  I have heard of folks achieving that, so I leave those files here for them.  The Related Changes folder in this repository already contains the klipper.bin file you will need to flash to a Creality CR6 motherboard or the BTT SKR CR6 motherboard.

The DGUS-Reloaded DWIN_SET firmware component is maintained in [this companion repo.](https://github.com/Thinkersbluff/DGUS-reloadedForKlipper_CR6)

>>  **NOTE: Each new release of the Klipper and DWIN_SET firmwares is published concurrently and the two are cross-referenced to the matching component in their respective release notes.**

* The Klipper component can be installed and used without the DWIN_SET component, if you do not value activating the stock TFT.
* The DWIN_SET component can NOT, however, be used without the matching version of the Klipper components.


## Who should __NOT__ use this firmware?
If your goal is to run Klipper on your CR6 without using the stock T5L DWIN display hardware, **then you do not need this modified version of Klipper.**
Just install the master Klipper3D.org version and configure it for your CR6 printer per the [Klipper3d.org installation and configuration documentation](https://github.com/Klipper3d/klipper/blob/master/docs/index.md).

Once you have the latest stock Klipper up and running on your system, you may enjoy browsing the Related Changes folder, here, to look for useful macros and settings.
If you need to look for CR6 pin names to configure Klipper on your system, these files may be a helpful resourse.

This repository may also be very helpful to get you started with Klipper on the CR6: https://github.com/KoenVanduffel/CR-6_Klipper

## Why Not Just Use the Desuuuu version of the Modified DGUS-Reloaded Klipper?

1. Most importantly, because Desuuuu has archived his dgus-reloaded-klipper fork, parts of which no longer work with the latest Klipper. 

2. To enable the CR6 UI functionality, I needed to edit a few of Desuuu's t5uid1 application files, so I needed to make my own (this) fork of those files.


## Is This Klipper Fork Using the latest Klipper3D/master version?
No.  

As of 30 Apr 2025:
- Thinkersbluff is no longer able to merge Klipper3D.org updates into this repo.
- The pre-built klipper.bin files available here DO, however, continue to work with Klipper as of v0.13.0-71-g3cf8899a
 
At some future release of Klipper, changes to the klipper.bin or Make Menuconfig functionality may no longer work with the pre-built klipper.bin files available here.
That may signal the end of this project, or it may force me (or one of you) to finally figure out what Desuuu did to the original Klipper files, that enabled the Klipper host to interact  with the stock TFT display firmware...

## Can I Install the Modified Klipper From This Repo?
You certainly could, but I definitely don't recommend it.   

I have left those modified files here for reference, because when Klipper3D.org make changes that "break" DGUS-Reloaded, I need to compare these archived files to the latest versions, to plan my updates.  

I recommend that you instead follow the guidance below.

## Can I Install the Latest Klipper from Klipper3D/master and STILL Use DGUS-Reloaded for CR6?
Yes, you can!  That is what I do, and I let Moonraker update my system, regularly.
As of February 2025, that still works (as long as you are using v1.3.2 or higher of the Klipper component.)

## Guidelines for How to Install DGUS-Reloaded with the Latest Klipper
Rather than install the full modified Klipper from this repository, you should instead follow these instructions to install the latest Klipper and then add the DGUS-Reloaded functionality to your system.  Moonraker will then automatically keep your Klipper installation up to date. 

1. Download and unzip the Source.zip file for the latest release on this repository. (NOTE: The file and folder names in Sources.zip are quite verbose, so you may first need to significantly shorten the top-level folder name in the zipfile ((e.g. to DGUS-Reloaded), to successfully "extract all" the contents.)

2. If you have not already done so, now create a Linux computer host for Klipper.  (NOTE: If you already have the Klipper/Mainsail host configured and are now updating it to use DGUS-Reloaded, then skip to step 6.)

There are many options for the Klipper host computer and it would greatly complicate these instructions if I tried to try to cover them all.  
For simplicity's sake, I will assume you are using a single Raspberry Pi Single Board Computer as your host.

3. There are two particularly easy ways to install Klipper with a Mainsail front-end, on a Raspberry Pi.  
   Both methods are supported by the Raspberry Pi Imager software. Download and install the appropriate version from here: [https://www.raspberrypi.com/software/](https://www.raspberrypi.com/software/)

4. To install MainsailOS (recommended), navigate to [https://docs-os.mainsail.xyz/](https://docs-os.mainsail.xyz/) and follow their instructions.
  OR  
   To use KIAUH (which may be easier if using a laptop or desktop computer as the Klipper host), navigate to [https://github.com/th33xitus/kiauh](https://github.com/th33xitus/kiauh) and follow those instructions.

Once you have installed Klipper and Mainsail, you should be able to browse to your Klipper host in the Mainsail front-end, to finish the installation and configuration:   

5. In the "Related Changes" folder from the unzipped Source.zip archive, open the "Custom Klipper host files" sub-folder of the motherboard sub-folder applicable to your printer.  
6. First read the ReadMe.txt file, to familiarize yourself with the purpose of each file and note any changes made since the last release.  
7. Then copy the applicable files into ~/printer_data/config on your host processor **and configure them for your specific printer/preferences.**  
   **NOTES:**  
          a)  You can upload files to ~/printer_data/config via the Mainsail MACHINE tab, rather than messing about with SFTP and nano, if you prefer.  
          b)  You can use a utility like [Winmerge](https://winmerge.org/downloads/?lang=en) to compare the new files with existing files, if you prefer to selectively modify the existing files, rather than replacing them.  
8. Copy the t5uid1 folder and contents into the ~/klipper/klippy/extras directory on your host (e.g. by using an SFTP program logged into your host, to transfer those files from the folder DGUS-Reloaded_for_CR6-Klipper_Component-..../klippy/extras that you extracted from the downloaded release zip file on your system.)
9. Follow the instructions on [https://github.com/matthewlloyd/Klipper-Stable-Z-Home](https://github.com/matthewlloyd/Klipper-Stable-Z-Home), to also install stable_z_home.py.  
   NOTE: To Clone a Repo:  
  i) log in to the Klipper host via SSH (e.g. Using PUtTy)  
 ii) At the Home directory, type:  <code>git clone https://github.com/matthewlloyd/Klipper-Stable-Z-Home.git</code>
10. In the "Related Changes" folder from the unzipped Source.zip archive, in the "Flash  motherbd" sub-folder of the motherboard sub-folder applicable to your printer,  find the  klipper.bin file and flash that file to your printer (the same way you would flash the Creality or Community Firmware to your motherboard.)
11. Restart your printer.
12. Restart Klipper.

Klipper should now connect with your mcu and Mainsail should support printing.  Until you have the matching DWIN_SET installed on your stock display, however, the display will still not function with Klipper.  

If instead you see error messages in Mainsail, you will need to resolve whatever problems are reported, until Klipper connects and reports "Ready".
  e.g. If your MCU serial interface id is not set correctly, then follow [the Klipper3D.org Klipper installation guidelines](https://www.klipper3d.org/Installation.html) to obtain the correct id and edit printer.cfg to insert it.

## Slicer-Specific Configuration Guidelines
The Print screens rely on receiving M73 P.. messages, to display % progress and M73 R.. messages, to display time remaining.
You will need to find and configure those settings in your slicer, for the screen to display those parameters. 

Klipper also differs from Marlin, regarding gcode commands and settings, as do each of the slicers. (e.g. variable names passed to Klipper macros are likely to differ between slicers)

See, "Configuring the Data Displayed", below, for what guidelines I can give you.

### Configuring the Data Displayed
#### Ultimaker Cura
At 5.7.0, Cura redacted the two Add-ins I used to recommend using, and replaced them with one new Add-In, "Display Info on LCD."
Here are the settings that I use, at 5.7.0+:  
![New Cura PlugIns_1of2](https://github.com/user-attachments/assets/f6f27bf4-17b7-4303-aefe-ce1373df5e83)
![New Cura PlugIns_2of2](https://github.com/user-attachments/assets/7422acee-a78c-447e-86e4-d79ef7a2c321)

The M118 instruction will log reports into the Klipper Log and display them in the Mainsail Console window.  
The M73 messages feed the % progress and Time remaining displays on the UI.
The Display Progress setting uses M117 messages to display Current Layer #, Total Layers and Estimated Time to complete the current print, on the display.  
#### OrcaSlicer
By default, OrcaSlicer sends both M73 R.. and M73 P.. messages.  Be sure that the box "Disable set remaining print time" in your printer profile is not checked.  
![image](https://github.com/Thinkersbluff/DGUS-Reloaded_for_CR6-Klipper_Component/assets/36551518/52f534ed-6a92-4424-a446-52903681d0a5)  

NOTE: I have not yet found any way to configure OrcaSlicer display the Layer information provided by Cura.
If you know of a way, please post a Discussion or Issue on the DGUS-Reloaded repo.

### Configuring the Start and End Gcodes
#### Ultimaker Cura
These are the Machine Code settings I use with Cura:  
![image](https://github.com/Thinkersbluff/DGUS-Reloaded_for_CR6-Klipper_Component/assets/36551518/6b7568cd-b96b-48b1-b9c3-61c7ecd22744)  

That last truncated line in the above image is:
start_print EXTRUDER_TEMP={material_print_temperature_layer_0} BED_TEMP={material_bed_temperature_layer_0}  
NOTE: I changed HOTEND_TEMP to EXTRUDER_TEMP because that is the parameter name recommended to OrcaSlicer users and I wanted the Klipper START_PRINT macro to be compatible, regardless of which slicer I used.  Apologies to any users of DGUS-reloaded who hits a Klipper error message because of this.  

#### OrcaSlicer
These are the Machine Code settings I use with OrcaSlicer:  
![image](https://github.com/Thinkersbluff/DGUS-Reloaded_for_CR6-Klipper_Component/assets/36551518/2e456fd4-1c9b-4baa-93ce-d60575bca2ca)  
  
![image](https://github.com/Thinkersbluff/DGUS-Reloaded_for_CR6-Klipper_Component/assets/36551518/2beb7124-e2c8-465e-b6c5-c9b333a2a4cb)  

![image](https://github.com/Thinkersbluff/DGUS-Reloaded_for_CR6-Klipper_Component/assets/36551518/d59a75fc-87db-4e0d-b522-983051909daa)   

NOTE: I also select "Use relative E distances, which is why the G92 E0 is necessary at the start of each new layer",  
![image](https://github.com/Thinkersbluff/DGUS-Reloaded_for_CR6-Klipper_Component/assets/36551518/03e0599b-670c-48c6-845a-370e8214ae08)  


#### Other Slicers
I do not use any other slicers. If you have information you think should be added here about configuring other slicers, please post a Discussion or Issue on the DGUS-Reloaded repo.

## A Word Of Warning About Klipper Documentation
Please note that Klipper3D are very good about keeping [their online documentation](https://www.klipper3d.org/) up to date with their latest firmware.
This repo, however, is NOT up-to-the-minute with every change they release.  That latency can mean that some of their online instructions do not work with this version of Klipper.  The documentation in this repo is, however, "frozen" at the most recent version of Klipper with which we have merged.  

IF you elect to install this modified Klipper INSTEAD of the Klipper3D version, THEN I recommend that you ALWAYS:
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
  
