Last Updated: 7 March 2026

# Introduction

## Scope
This section organizes and provides the Installation Help documentation.  

## Assumptions
These documents assume that the user is:
- using a Debian-based Linux operating system on the Klipper Host for their system.
- willing and able to install the suggested applications (or equivalents) to facilitate the installation process.
- comfortable with copying scripts from Help Docs and pasting those into an SSH application window, and running them.
- comfortable with using an SFTP tool (like FileZilla) to interactively manage the file system on their Klipper host and to transfer files back & forth between the Klipper host and their computer.
- familiar with basic concepts which enable understanding and following these documents as written.

NOTE: That last assumption is my way of saying that sometimes, these help docs may assume that you know something and therefore may not mention or discuss it.
If you find something in these docs to be "mystifying", I recommend that you explore your confusion with an AI bot like ChatGPT. (no joke)  The Microsoft CoPilot AI has been of enormous help to me, on this project, filling in my knowledge gaps.

# Overview

## About the File Numbering
I use numbers in each of the document titles, to force the order in which I want the titles to be listed.  I recommend that you first review the scope and purpose of these documents in that numbered order, to understand the gist of what you will be doing, and how.

## 1-Manual_Installation.md 
If you are comfortable with using Linux and/or an SFTP tool to add/delete/modify files and directories on the Klipper host, you will likely find the manual installation process to be the quickest, easiest, and safest way to install DGUS-Reloaded into your existing Klipper-based system.  

If you prefer to trust scripts to do most of the "heavy-lifting", and are comfortable with troubleshooting unexpected results, consider instead following the process documented in 2-Scripted_Installation.md.

## 2-Scripted_Installation.md
If you are comfortable with using shell scripts to automate downloading and configuring applications on your Klipper host, you will likely find the scripted installation process to be the most convenient way to install DGUS-Reloaded into your existing Klipper-based system.

If you find automated script-based installations a bit unnerving, or if you encounter problems while using the scripts that you can not find your way around, then you may prefer instead to follow the process documented in 1-Manual_Installation.md.

## 3-Rebuilding_MCU_Firmware.md
When you first install Klipper on your printer's motherboard, the Klipper3D.org's own documentation walks you through the process of configuring and building a klipper.bin file. You must then flash that binary file to the motherboard and connect the motherboard to the Klipper host (via a USB cable). That binary file then runs on the motherboard and enables Klipper to monitor and control the printer hardware.

>**There is always a risk, when you choose to update the Klipper firmware on your system, that the Klipper3D.org developers may have changed the Klipper firmware in some way that renders the existing klipper.bin file incompatible with the new version of Klipper.**

In order to extend Klipper to also work with the CR6 stock display, we need to make some small changes to the Klipper firmware before we run make menuconfig and before we make our DGUS-Reloaded for CR6 version of klipper.bin.

To help users avoid this part of the process, I always include pre-built versions of the klipper.bin files (in Installation_Files/4-klipper.bin_files/), which I confirm are compatible with the current version of Klipper when I first release them.  That will not help you if Klipper3D.org subsequently make additional changes to the mcu (klipper.bin) firmware, until I release a 'fix'.  
3-Rebuilding_MCU_Firmware.md documents the process by which you can configure and make your own updated klipper.bin file in that event, so that you don't always have to wait for me to issue a 'fix'.

## [Optional]Slicer_Integration_Tips
It is not absolutely necessary to modify your slicer, to use DGUS-Reloaded for CR6.  I do, however, recommend that you at least enable M73 messaging, so that you will see displays of %print progress and print time remaining.
I don't have the bandwidth or energy to figure out how to integrate multiple slicers, so I only provide tips for the slicer I am using.  At the moment, that slicer is Ultimaker Cura.
I am always happy to accept similar tips for other slicers from the user community, which I will copy to this folder.