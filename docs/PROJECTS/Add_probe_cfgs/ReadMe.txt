Last modified: 20 Feb 2025

Background:

At v 1.3.7, the DGUS-Reloaded Klipper component assumes the use of the stock strain gauge probe for all probing and homing.

These project files are designed to:

	1. Move all probe-dependent configuration settings into a new file - stockprobe.cfg - such that adding [include stockprobe.cfg] to printer.cfg will restore the stock configuration to the same functionality as at v1.3.7.
	2. Introduce a new configuration file - microprobe.cfg - to encapsulate all of the probe settings required if a printer has been converted from the stock strain gauge to instead use a BTT microprobe for all probing and homing.
	3. Modify the architecture of DGUS-Reloaded to enable configuring DGUS-Reloaded to facilitate similar future alternative probe conversions, such as replacing the stock gauge or the microprobe with a BLTouch. 

They have been tested and confirmed to work correctly on a CR6-SE using the stock strain gauge system.
They are now ready to be tested on a system which has been converted to use a BTT microprobe.

Tailoring Instructions:

1. Edit microprobe.cfg to correct the following settings:

x_offset 
	- measure the distance between the nozzle tip and the microprobe tip, along the x axis, in mm (zero is at the left end of the axis)
	- if the probe tip is to the left of the nozzle, enter a negative value
y_offset
	- as for x axis, but measured on y-axis (zero is at the front of the bed)

home_xy_position
	- subtract the x_offset from the x coordinate & subtract the y_offset from the y coordinate.
	NOTE: The goal is to specify the point on the bed where the nozzle will be, if the probe is at the center of the bed.
	REMINDER: The current values assume a CR6-SE printer bed.