Last Updated : 5 May 2026

These files were built by updating the pin numbers in the ERA/4.5.3 files to be those of the BTT SKR CR6 board.

While they are uniquely configured to run on the test system, they also provide you with a reference that should help you figure out how to tailor your own setup to work with DGUS-reloaded_CR6Community_Edition.
There are copious notes throughout the files where you must tailor them for your own system.

At release v1.3.5 of these files, the printer.cfg file was modified to correct a couple of configuration errors and to replace ACCEL_TO_DECEL with MINIMUM_CRUISE_RATIO.
This particular change follows modifications to Klipper made by Klipper3D.org.

At release v1.3.7, I noticed that the TMC section for the extruder was missing from printer.cfg.
No idea when or how that got erased, but it was not intentional...
I put it back, using the printer.cfg file online at https://github.com/KoenVanduffel/CR-6_Klipper/tree/main

At release v1.3.8, I incorporated an architectural change which moves the stock probe settings into their own cfg file (stockprobe.cfg)
I did that to support one user with a Creality v1.1.0.3 motherboard, who converted their CR6 to use a BTT MicroProbe instead of the stock strain gauge.
I DO NOT KNOW WHAT PINs to substitute into this solution for a BTT SKR CR6 motherboard, so YOU will need to FIX microprobe.cfg, if you make the same conversion.  If you instead convert to a different sensor (e.g. BLTouch), you will need to develop your own custom .cfg file for the probe.

The Dev_Macros.cfg file adds a couple of macros that help developers research the names/states of available parameters.  It is not needed, for the DGUS-Reloaded app to work. You can comment-out the include statement from printer.cfg if you wish.