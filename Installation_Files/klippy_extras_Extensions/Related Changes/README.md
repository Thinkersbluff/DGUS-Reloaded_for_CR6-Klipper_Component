Last Updated: 4 March 2026

# Greetings and a few words of encouragement:
Hello! 

The very thing that makes Klipper so powerful - the ability to customize so many printer behaviours and performance parameters - can also impose a significant learning curve, at first.

I have done my best to provide you with a full set of files and guidelines sufficient to get you started.  For some, it may be too much, others will still find I have not covered key details.

Please feel free to reach-out in the Discussions section, in either case. This is my "passion project."  I am happy to help.

# About The Repository Structure

I use GitHub to organize this project and to help me maintain configuration control.  

I am not a professional software developer, so I likely do not organize the structure or contents of this GitHub repository using "standard" naming conventions or organizational structures.  If that means that "real" developers sometimes struggle to find what they are looking for, now you know why.  Please feel free to offer me advice.

I imagine that many 3D printer owners curious about installing and using this firmware may not be familiar with navigating or cloning GitHub repositories.  I am doing my best, here, to structure my repository and the support documentation to be "intuitive" to you.  I trust that actual GitHub and software development "experts" will find it easy enough to adapt and cope with my "strange" choices.  Again, feel free to engage with me on the Discussions forum, if you have comments and recommendations.

## Overview - A Tale of Two Repositories

I use two repositories to manage the DGUS-Reloaded for CR6 system components:
1. I use this one - DGUS-Reloaded for CR6-Klipper Component - to maintain everything except the DWIN display component.
2. I use a second - DGUS-Reloaded for CR6-DWIN Component - to maintain the DWIN_SET firmware.

I tried managing both components in a single repository, but GitHub, Visual Studio Code and I all struggled with maintaining configuration control of so many files.  It is much easier for me - maybe not so much for you? = to keep them separate.

# About the Structure of this Klipper Component Repository

In this repository, I have organized files and information according to the following logical structure:

1. Root: 
 - The LICENSE file explains your legal rights to use or modify this code.
 - The README.MD file automatically appears on the home page of the repository, offering an introduction to the project and an overview of how to get started.
2. Development_Project_Files exposes some of my working files, to support people who wish to fork this repository for their own development purposes.  Users who just want to download and use the firmware should ignore that folder completely.
3. Installation_Files (this folder) is organized into the following sub-structure:
   1. docs - procedures and guidelines which clarify and detail how best to effect the installation
   2. klipper.bin_files - pre-compiled klipper.bin binaries, for users to flash to their CR6 motherboard.
   3. klippy_extras_Extensions 
      1. klippy\extras\- the main DGUS-Reloaded for CR6 application files.  Uploading these files and folders to your Klipper host (into the ~klipper/klippy/extras folder) will deploy most (but not all) of this application
      2. Related Changes
         1. Custom_Klipper+Mainsail_Files - a default set of configuration files for users to tailor for their own systems.  Pre-configured with the right pin numbers and reasonable default settings, as used on the Development Printer.  Annotated with tailoring recommendations for users. NOTE: The Dev Printer is non-stock, as are those of many others. [This is where Klipper and I collectively put the burden on you to understand what you need to change in these files.]
         2. Slicer_integration_tips - a set of examples of how I tailored Cura to integrate with DGUS-Reloaded for CR6.  The Start and End gcode examples should work for most slicers.  Slicer plug-ins are your challenge.
   4. make_menuconfig_Extensions 
      1. klipper - a set of modules to extend klipper/src/generic and klipper/src/stm32, to add to klipper.bin the t5ud1 "magic" that integrates the DWIN_SET component with the Klipper-Component of DGUS-Reloaded for CR6.
      2. README.MD explains whether and how to install these extensions.  Installing these enables you to configure and build a custom klipper.bin file for your motherboard, if the pre-compiled binaries become too old, again, to work with a future version of Klipper3D. 


NOTES: 
1. If you are trying to install this firmware onto a printer which is NOT a Creality CR6 machine (e.g. Vyper or Ender 3), I have neither the knowledge nor the time to help you.

2. I rely upon you and other CR6Community members to help "shake-down" this distribution and to provide validated tailored configurations.  If you encounter difficulties getting the latest version to work, please reach out to me on the CR6Community Discord.

3. The Custom_Klipper+Mainsail_Files I have included are derived from my own key configuration files. These were all verified and validated to work as an integrated set on my own CR6-SE, which has at least the following modifications on it: 
	- BTT SKR CR6 v1.0 motherboard
	- Converted to Direct Drive, with 
		- an Orbiter v1.5 extruder and pancake Moons extruder motor
		- a Dragon HF hotend
		- a BTT Smart Filament Runout Sensor (SFS) v1.0

When I started this project, I had a BTT SKR CR6 motherboard.  
For a few years, I used a Creality 1.1.0.3 ERA motherboard.
After "an unfortunate incident", I am back on the BTT board.  
I have uploaded copies of the configuration files for both the BTT and the Creality motherboards, here, to get you started. 

Be aware that you will likely need to change some settings before this distribution will work on your system. 
	e.g. Printer.cfg and CR6.cfg will both require edits to adjust the extruder & stepper motor and performance settings, for instance
I have done my best to annotate the files that require validation or modification, but in the end only you can ensure that your printer is correctly configured.

If you plan to install this modified Klipper onto an existing Klipper system, you may prefer to keep your existing configuration files and just compare yours with the ones I have included, to spot and transfer any relevant differences between the two. (A tool like Winmerge is excellent for that type of comparison and harmonization task.)

If you have no existing Klipper installation, you can start by uploading these files as-is, but you will still likely need to modify some of the settings, to be fully compatible with your own system.  I have included verbose annotations in the files, to help draw your attention to those settings you are most likely to need to tailor.


NOTE: If you already use Mainsail, make sure that you have updated it on or after Jan 2023.  They changed the design a little and corrected a couple of bugs in the CANCEL_PRINT macro used by this firmware.

If you use Fluidd, my apologies, but I do not, so you will likely need to do some additional work to configure your system.  I just don't know what that work will be.  Please share your experience and learning in Discussions, for the benefit of other Fluidd users.

ENJOY!