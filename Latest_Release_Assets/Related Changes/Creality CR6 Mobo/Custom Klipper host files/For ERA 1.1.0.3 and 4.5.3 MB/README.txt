Last Updated : 6 May 2025

These files were downloaded from the Mainsail MACHINE CONFIG FILES tab of the test printer, at release time.

While they are uniquely configured to run on the test system, they also provide you with a reference that should help you figure out how to tailor your own setup to work with DGUS-reloaded_CR6Community_Edition. 
   e.g. The author uses WINMERGE to compare old with new, when reviewing which changes to incorporate or ignore.

At release v1.3.5 of these files, the printer.cfg file was modified to correct a couple of configuration errors and to replace ACCEL_TO_DECEL with MINIMUM_CRUISE_RATIO.
This particular change follows modifications to Klipper made by Klipper3D.org.

At release v1.3.8, I incorporated an architectural change which moves the stock probe settings into their own cfg file (stockprobe.cfg)
I did that to support a user with a Creality v1.1.0.3 motherboard, who converted their CR6 to use a BTT MicroProbe instead of the stock strain gauge.
If you instead convert to a different sensor (e.g. BLTouch), you will need to develop your own custom .cfg file for that probe.

NOTE: If you decide to make a new installation of Mainsail/Moonraker/Klipper, then you can upload these files as-is, then proceed to tailor printer.cfg to match your system and to suit your preferences.
There are copious notes throughout the files where they require you to tailor them for your own system.

The Dev_Macros.cfg file adds a couple of macros that help developers research the names/states of available parameters.  It is not needed, for the DGUS-Reloaded app to work. You can comment-out the include statement from printer.cfg if you wish.