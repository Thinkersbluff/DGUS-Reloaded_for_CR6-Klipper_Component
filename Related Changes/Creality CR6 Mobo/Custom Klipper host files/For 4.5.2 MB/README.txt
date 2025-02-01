Last Updated : 31 Jan 2025

These files were built by updating the pin numbers in the ERA/4.5.3 files to be those of the 4.5.2 board.
[Only impacted the Nozzle Heater, Bed and Part Fan pins]

While they are uniquely configured to run on the test system, they also provide you with a reference that should help you figure out how to tailor your own setup to work with DGUS-reloaded_CR6Community_Edition. 
   e.g. The author uses WINMERGE to compare old with new, when reviewing which changes to incorporate or ignore.

At release v1.3.5 of these files, the printer.cfg file was modified to correct a couple of configuration errors and to replace ACCEL_TO_DECEL with MINIMUM_CRUISE_RATIO.
This particular change follows modifications to Klipper made by Klipper3D.org.

NOTE: If you decide to make a new installation of Mainsail/Moonraker/Klipper, then you can upload these files as-is, then proceed to tailor printer.cfg to match your system and to suit your preferences.
There are copious notes throughout the files where they require you to tailor them for your own system.

The Dev_Macros.cfg file adds a couple of macros that help developers research the names/states of available parameters.  It is not needed, for the DGUS-Reloaded app to work. You can comment-out the include statement from printer.cfg if you wish.