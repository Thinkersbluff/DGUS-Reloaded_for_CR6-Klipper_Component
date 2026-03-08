Last Updated: 7 March 2026

# Introduction

Klipper3D.org does not officially include support for Add-Ons in the Klipper architecture.  
There is, however, a folder called 'extras', in the klipper/klippy folder, where 3rd-party developers can install extensions, which klippy will find and enumerate at startup.  As long as we extension developer(s) are willing and able to refactor our code whenever Klipper3D.org changes functions upon which our extensions rely, then the 'extras' continue to work, even if Klipper itself is updated.

# What is t5uid1?

The t5uid1 folder and all of its contents (including the sub-folder dgus_reloaded/ and all of its contents) collectively constitute the core of the DGUS-Reloaded for CR6 extension to Klipper.  

Deploying this extension onto your host is as simple as copying all of this to the klipper/klippy/extras folder on your Klipper host.

# Do I need to manually edit any of these files?
Just a couple of them - as explained below.
I recommend that you don't modify any of the other files, if you are not trying to modify the functionality of the application.

## Default Filament Type Names
The file t5uid1/dgus_reloaded/presets.cfg defines some important default values, which are loaded into the display UI at boot time.  
Most of the values defined therein can subsequently be modified through the stock screen UI.  
The only values there which must be edited using a text editor to change presets.cfg itself are:  
 - filament_type_1_default_name = PLA+
 - filament_type_2_default_name = ASA
 - filament_type_3_default_name = PETG  
The small stock screen would not really work well with a QWERTY keyboard, and a pull-down list of all of the possible filament types seems futile, so I chose to require that you edit the file to change those names.

