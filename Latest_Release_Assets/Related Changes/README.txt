Last Updated: 7 Feb 2025

One of the challenges with installing this distribution on your system is that you will still likely need to make some customizations of your own.

In this(\Related Changes} folder, you will find:

 - Some images and instructions to help you configure the Ultimaker Cura slicer to work with the DGUS-Reloaded firmware 
	[NOTE: If you use Orca Slicer, I have added some instructions for configuring that in the repo Readme file, but I do not know whether it can be used to support Firmware Retraction.]

and

 - These two subfolders:
 	\Creality CR6 Mobo, and
 	\BTT SKR CR6 Only

Open the subfolder corresponding to whether you have the BTT motherboard or one of the three supported Creality motherboards.
There you will find two more subfolders, with contents specifically tailored to your motherboard.

1. \Related Changes\...\flash  motherboard

Part of the normal Klipper installation process involves using a utility called Make Menuconfig, to generate a configuration file, and then to Make (compile) a Klipper.bin based on that configuration file, with which to flash Klipper to your printer's motherboard. 
   BUT: Make Menuconfig is NOT supported by the latest Klipper, for this DGUS-Reloaded application.
In this repo, you will INSTEAD find pre-made klipper.bin files for the BTT SKR CR6 and Creality 4.5.2/4.5.3/1.1.0.3 motherboards.


You MUST** flash the firmware.bin file from the applicable folder (according to whether your motherboard is the BTT SKR CR6 or one of the three Creality motherboards) & skip the Make Menuconfig/Make steps.  
  ** Make Menuconfig will NOT reproduce these files, using the current version of Klipper, and the archived modified version of Klipper on this repo is no longer compatible with the latest configuration files.

NOTE: If you are trying to install this firmware onto a printer which is NOT a Creality CR6 machine (e.g. Vyper or Ender 3), I can not help you.  I do not know how Desuuu modified the older version of Klipper from which I forked the version on this repo, to implement the motherboard/DWIN_SET communications.  I have kept that history up here, on the off-chance that someone might want to explore that, but it is beyond my limited coding skills.


2. \Related Changes\...\Custom Klipper host files

Upload to the Machine folder in Mainsail any of these configuration files that you do not already have.  Compare the others (e.g. using WinMerge) to identify any edits that you should make, to configure the DGUS-Reloaded Klipper component.

Klipper, Moonraker and Mainsail each require configuration files to tailor their installation and operation.
I have only one CR6-SE printer on which to perform my development and testing, so I am not able to verify and validate that the files included with this distribution will operate on all possible CR6 machines.

I rely upon you and other CR6Community members to help "shake-down" this distribution and to provide validated tailored configurations.  If you encounter difficulties getting the latest version to work, please reach out to me on the CR6Community Discord.

I have included my key configuration files in this distribution, in the folder "Related Changes\...\Custom Klipper host files". These files were all verified and validated to work as an integrated set on my own CR6-SE, which has at least the following modifications on it: 
	- Creality 1.1.0.3 ERA motherboard
	- Converted to Direct Drive, with 
		- an Orbiter v1.5 extruder and pancake Moons extruder motor
		- a Dragon HF hotend

When I started this project, I had a BTT SKR CR6 motherboard.  
I now use a Creality 1.1.0.3 ERA motherboard.  
I have uploaded copies of the configuration files for both motherboards, here, to get you started. 

Be aware that you will likely need to change some settings before this distribution will work on your system. 
	e.g. Printer.cfg and CR6.cfg will both require edits to adjust the extruder & stepper motor and performance settings, for instance
I have done my best to annotate the files that require validation or modification, but in the end only you can ensure that your printer is correctly configured.

If you plan to install this modified Klipper onto an existing Klipper system, you may prefer to keep your existing configuration files and just compare yours with the ones I have included, to spot and transfer any relevant differences between the two. (A tool like Winmerge is excellent for that type of comparison and harmonization task.)

If you have no existing Klipper installation, you can start by uploading these files as-is, but you will still likely need to modify some of the settings, to be fully compatible with your own system.  I have included verbose annotations in the files, to help draw your attention to those settings you are most likely to need to tailor.


NOTE: If you already use Mainsail, make sure that you have updated it on or after Jan 2023.  They have changed the design a little and have corrected a couple of bugs in the CANCEL_PRINT macro used by this firmware.

If you use Fluidd, my apologies, but I do not, so you will likely need to do some additional work to configure your system.  I just don't know what that work will be.  Please share your experience and learning in Discussions, for the benefit of other Fluidd users.


