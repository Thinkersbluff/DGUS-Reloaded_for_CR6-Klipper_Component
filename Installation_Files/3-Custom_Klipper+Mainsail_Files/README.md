Last Updated: 7 March 2026

# Introduction

Both Klipper and Mainsail require the user to build and maintain a set of text-based configuration files, to customize the system for your particular printer and preferences.

Since I know that the target for our firmware is uniquely some particular variation of Creality CR6 printer,  I can pre-build a default set of the standard Klipper configuration files for you.  

This folder contains a default set of these files, pre-configured to work on my own CR6-SE printer, but annotated to help you find and "correct" the parameters that are most likely to be different between your printer and mine.

## Which Motherboards are supported?

There are only four motherboards specific to the CR6 printers, so I also build and maintain four versions of these files, one for each of:
 1. the BTT SKR CR6 v1.0 (an after-market upgrade that was quite popular in its day, but which BigTreeTech decided to discontinue.)  I happen to have one of these boards myself, in my development printer (a Kickstarter CR6-SE).
 - the Creality CR6 motherboards:
   2. 4.5.2 (delivered in the early CR6-SE printers)
   3. 4.5.3 (delivered in the early CR6-MAX printers)
   4. 1.1.0.3 ERA (the current board in both SE and MAX printers)

## Where do these files go?

Klipper expects to find these files in the folder klipper/printer_data.

## Is this a complete set of the printer_data files?

No.  
Other programs in your Klipper/Mainsail ecosystem (Mainsail, Moonraker, Crowsnest, etc..) may read and write other configuration files to printer_data.

## Should Overwrite Existing printer_data Files With These Ones?
No.  
The set that I distribute with DGUS-Reloaded for CR6 includes files which already exist in printer_data (e.g. printer.cfg), but which needed to be modified to work with t5uid1 and with the display component.

Installing the Custom_Klipper+Mainsail_Files into your system requires you to compare the new files with the existing files on your system, to identify the differences and to decide how best to "merge" the two.  I strongly recommend that you use WinMerge to perform this task, if you have a Windows PC.

I do my best to guide you with comments in the files that you may need to edit, but ultimately it will come down to your understanding of what the settings do and what are the right values for your printer and preferences.  
This is the task where we most strongly experience that tradeoff between "Klipper the powerful" and "Klipper the complicated".

## How do I add/delete/modify these files?

Mainsail allows you to add/delete/modify the files in printer_data, through the MACHINE tab in the Mainsail side menu.
You can also use an SFTP tool like FileZilla to manage these files on the host.

## What is AppendToPrinter.cfg.txt For?

Klipper reserves the area at the bottom of printer.cfg to store configuration data.  One significant block of that data describes the bed mesh names and values.
Normally, one should not edit that area of printer.cfg, because it can create ambiguities and conflicts as Klipper initializes.
In the unique edge-case of a brand new installation of DGUS-Reloaded for CR6, if that area in printer.cfg is blank, then the initial loading of the Automatic Bed Leveling screen does not operate normally, and that can be confusing.  To work around the issue, I created a default set of meshes with the value of 0.0 at each point.  By appending this text to the bottom of printer.cfg, I work around that edge-case.  
If I have built and inspected the release properly, you will find that I already appended this text and you can ignore this file.
NOTE: The downside of my approach is that you will need to manually edit the mesh boundary values in for a CR6-MAX. (Sorry.)