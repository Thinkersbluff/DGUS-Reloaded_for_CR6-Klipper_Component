````markdown
Last Updated: 9 March 2026


# DGUS-reloaded-Klipper, CR6Community Edition!
Lets you use your stock Creality CR6 display with Klipper firmware, restoring touchscreen functionality after converting your printer to Klipper.

---

## Should You Use This?

- **YES:** If you want your CR6’s original touchscreen to work with Klipper.
- **NO:** If you don’t use the stock display, just install the latest Klipper from [Klipper3D.org](https://www.klipper3d.org/).

---

## How Does It Work?

- This project provides a Python application ('dgus-reloaded`), a pre-compiled Klipper.bin file, and a matching DWIN_SET firmware for your display.
- You install the latest Klipper as usual, then you integrate DGUS-Reloaded to enable the display:
   1. Flash the Klipper.bin to your motherboard.
   2. Flash the companion DWIN_SET firmware to your display*
   3. Install Stable-Z-Home.py to optimize probing and leveling performance
   4. Install and adapt the printer.cfg and companion configuration files from the Related Changes folder, to suit your taste, or just use them as-is.
   5. Adapt and integrate your slicer program into Moonraker, if you wish.

*The DGUS-Reloaded DWIN_SET firmware component is maintained in [this companion repo.](https://github.com/Thinkersbluff/DGUS-reloadedForKlipper_CR6)

Expand the more verbose sections below, for more details if/as required.
---

## FAQs
<details>
<summary><strong>Backstory and Credits</strong></summary>

The Klipper in this repo is an old fork of Klipper3D/Master, which was modified [by Desuuuu](https://github.com/Desuuuu/klipper), to work with his version of the DGUS-reloaded python application (t5uid1) and a matching DWIN_SET application. 

I found Desuuu's DGUS-Reloaded project while I was searching for a way to preserve/restore some level of functionality to the stock TFT display on my CR6-SE printer, after converting the printer to Klipper.

Desuuu had at that time just decided to archive his project, so I decided to fork his project and adapt it to my own needs. 
I also try to maintain and share the python app, and Mainsail/Klipper configuration files here in this repository, to allow others with CR6 printers and similar machines to adopt or tailor my firmwares for your own purposes.

## Why Not Just Use the Desuuuu version of the Modified DGUS-Reloaded Klipper?

1. Most importantly, because Desuuuu has archived his dgus-reloaded-klipper fork, parts of which no longer work with the latest Klipper. 

2. To enable the CR6 UI functionality, I needed to edit a few of Desuuu's t5uid1 application files, so I needed to make my own (this) fork of those files.

</details>

<details>
<summary><strong>More about Klipper</strong></summary>

```
**PLEASE NOTE: The Klipper files on this repository are out of date. 
They should not be installed onto your system, unless you are trying to run Make Menuconfig to build a custom klipper.bin file for a non-CR6 printer.  
I have heard of folks achieving that, so I leave those files here for them.  
The Related Changes folder in this repository already contains the klipper.bin file you will need to flash to a Creality CR6 motherboard or the BTT SKR CR6 motherboard.**
```

## Is This Klipper Fork Using the latest Klipper3D/master version?
No.  

As of 27 June 2025:
- Thinkersbluff is no longer able to merge Klipper3D.org updates into this repo.
- The pre-built klipper.bin files available here DO, however, continue to work with Klipper at v0.13.0-154-g9346ad19
 
At some future release of Klipper, changes to the klipper.bin or Make Menuconfig functionality may no longer work with the pre-built klipper.bin files available here.
That may signal the end of this project, or it may force me (or one of you) to finally figure out what Desuuu did to the original Klipper files, that enabled the Klipper host to interact  with the stock TFT display firmware...

## Can I Install the Modified Klipper From This Repo?
You certainly could, but I definitely don't recommend it.   

I have left those modified files here for reference, because when Klipper3D.org make changes that "break" DGUS-Reloaded, I need to compare these archived files to the latest versions, to plan my updates.  

I recommend that you instead follow the guidance below.

## Can I Install the Latest Klipper from Klipper3D/master and STILL Use DGUS-Reloaded for CR6?
Yes, you can!  That is what I do, and I let Moonraker update my system, regularly.
As of August 2025, that still works (as long as you are using v1.3.2 or higher of the Klipper component.)
</details>

<details>
<summary><strong>More Detailed Instructions for Integrating DGUS-Reloaded</strong></summary>

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
8. Copy the 'dgus-reloaded' folder and contents into the ~/klipper/klippy/extras directory on your host (e.g. by using an SFTP program logged into your host, to transfer those files from the folder DGUS-Reloaded_for_CR6-Klipper_Component-..../klippy/extras that you extracted from the downloaded release zip file on your system.)
9. Follow the instructions on [https://github.com/matthewlloyd/Klipper-Stable-Z-Home](https://github.com/matthewlloyd/Klipper-Stable-Z-Home), to also install stable_z_home.py.  

   i.e.:
    1. Clone the repo
   
      NOTE: To Clone a Repo:  
            i) log in to the Klipper host via SSH (e.g. Using PUtTy)  
           ii) At the user's pi login home directory (e.g. in /home/pi), type:  <code>git clone https://github.com/matthewlloyd/Klipper-Stable-Z-Home.git</code>
     
    2. Create a symlink in the /home/pi/klipper/klippy/extras folder, with the following two commands:

           cd ~/klipper/klippy/extras  
           ln -s ~/Klipper-Stable-Z-Home/stable_z_home.py

    This picture highlights where the clone and the symlink should be (assuming your user name is "pi", as recommended):  
    ![Where to symlink stable_z_home py](https://github.com/user-attachments/assets/d1991eb1-282e-47b8-b07d-51289273f077)

11. In the "Related Changes" folder from the unzipped Source.zip archive, in the "Flash  motherbd" sub-folder of the motherboard sub-folder applicable to your printer,  find the  klipper.bin file and flash that file to your printer (the same way you would flash the Creality or Community Firmware to your motherboard.)
12. Restart your printer.
13. Restart Klipper.

Klipper should now connect with your mcu and Mainsail should support printing.  Until you have the matching DWIN_SET installed on your stock display, however, the display will still not function with Klipper.  

If instead you see error messages in Mainsail, you will need to resolve whatever problems are reported, until Klipper connects and reports "Ready".
  e.g. If your MCU serial interface id is not set correctly, then follow [the Klipper3D.org Klipper installation guidelines](https://www.klipper3d.org/Installation.html) to obtain the correct id and edit printer.cfg to insert it.
</details>

 
 ## How to Contribute To This Project

Please feel free to contribute ideas and feedback in the Discussions section.

Since some of the behaviour of the DGUS-Reloaded UI is controlled by the DWIN_SET app and some by this Klipper back-end, it will be "cleaner" to keep all Issues together on one repo.  If you believe you have found a bug in the way the DGUS-Reloaded UI works on your CR6 printer, please therefore navigate to [the Issues folder on the DWIN_SET repo](https://github.com/Thinkersbluff/DGUS-Reloaded_for_CR6-DWIN-SET_Component/issues).  If there is no existing open or closed Issue that describes the same issue, then please raise a new Issue there.  

CR6Community Firmware features NOT present in this release may be developed in future releases, but no schedule commitment is possible for such extensions.  Users who are able to define and develop such modifications are welcome to fork this repository and to submit Pull Requests or to open Discussions or Issues as appropriate, to propose those changes.

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
  
