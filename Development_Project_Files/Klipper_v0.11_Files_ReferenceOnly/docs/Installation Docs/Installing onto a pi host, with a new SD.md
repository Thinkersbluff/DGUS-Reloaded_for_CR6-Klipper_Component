How to Install DGUS-Reloaded for CR6 (Klipper Component) onto a pi host, starting with a new SD Card

Step 1: Format the SD card and install the 64-bit Mainsail OS version of Raspbian.

[There is an online guide by Mainsail-Crew, here.](https://docs.mainsail.xyz/setup/mainsail-os)

I chose this method:   
- Using the Raspberry Pi Imager:
  - Select 3D Printer OS -> Mainsail 64-bit
  - Select the target SD Card as Storage
  - Select the settings (gear) icon
  - Pre-configure the network SSID & password
  - Keep the username as pi (more stable)
  - Add sudo password
  - Write the OS to the Card

**VERY IMPORTANT: This step was missing from the online instructions, on 6 Feb 2023: To enable wifi on the pi, now find and follow the instructions in Wifi-README.txt on the SD card, BEFORE moving the card to the pi.** 


Step 2: Insert the SD card into the pi host  
- Ensure power on the host pi is off.
- Insert the card into the host pi (e.g. 3b+)
- OPTIONALLY: Connect a display and USB keyboard to the pi, to support the initial configuration of the pi
- Switch pi power on and wait for the system to boot up
- On first boot, wait a few minutes while the system runs a setup script to expand the filemanagement system to use the full SD card and to enable SSH. The script will end by rebooting the system to implement the changes and will stop at the pi login prompt.

Step 3: Find out on which IP address your pi is now operating. 

- Launch a browser on your PC or MAC
- Try opening the following address in a new tab:
  - hostname.local (where hostname is whatever you called your pi, when you set up the imager software to flash that card)
  - if that does not work, try one of these other methods:

    - If you did NOT connect a display and keyboard to the pi, you may be able to use your router to determine the allocated IP address. 
    HINT: If the physical pi has had an IP address before, the router will likely recognize the MAC address and will give it the same IP address again (if that is still available.)

    - If you did connect a display and keyboard to the pi, you can log into the pi and enter: _**Hostname -I**_ to discover the IP address.

Step 4: Launch a browser on your PC or MAC and navigate to the IP address you found at Step 3.
 - Your browser should open Mainsail, which should display this Klipper error: "Unable to open config file /home/pi/printer_data/config/printer.cfg 

 - You will now need to obtain a suitable Printer.CFG file and follow the Mainsail Installation Documentation instructions to edit and upload that file to this installation. (e.g. from https://github.com/KoenVanduffel/CR-6_Klipper)

Step 5: Add a printer.cfg file to the MACHINE section in Mainsail

[The online Mainsail guide for this step is here.](https://docs.mainsail.xyz/setup/mainsailos/klipper-setup)

Since the Mainsail crew have installed their own latest default configuration with this setup, I can not predict all of the changes you may have to make.

As an example, though, this is what I did when adapting their Dec 2022 configuration to work with my customized ERA 1.1.0.3 CR6-SE Test Printer at Release 1.2.3 of DGUS-Reloaded for CR6:

1. Download and unpack the Source.zip file from [the latest release page on the DGUS-Reloaded_for_CR6_Klipper_Component repository.](https://github.com/Thinkersbluff/DGUS-Reloaded_for_CR6-Klipper_Component/releases/tag/v1.2.3)
2. Navigate to the folder "DGUS-Reloaded_for_CR6-Klipper_Component-1.2.3.zip\DGUS-Reloaded_for_CR6-Klipper_Component-1.2.3\Related Changes\If you have an ERA 1.1.0.3 motherboard\Overwrite these Klipper host files\Use these configuration files to  tailor your Klipper config\"
3. Open the file ERA_cfgs_mainsail_dgus-reloaded_1.2.2.zip
4. Open the file printer.cfg, to use as a reference.

5. Using Mainsail in the browser:
   1. Navigate to MACHINE
   2. Click the Create File icon and enter printer.cfg as the filename
   3. Click the printer.cfg filename to edit the file
   4. Copy and tailor the contents of the reference printer.cfg file into the new printer.cfg file.
   5. Upload the reference inputShaper.cfg file, but be sure to calibrate it for your system before uncommenting that include in printer.cfg
   6. Upload the reference CR6.cfg file, but be sure to edit any values that do not match your system
   7. Select "Update All Components" in the Moonraker Update Manager window of the Mainsail MACHINE tab.
   8. When the update is complete, Klipper will declare an error, "Section 't5uid1' is not a valid config section."  This is the point where we need to install the customized DGUS-Reloaded version of Klipper.
   9. Using an FTP client (e.g. Filezilla):
      1.  Create a new directory ~/klipper/klippy/extras/t5uid1.
      2.  Create a new directory dgus_reloaded within the new t5uid1 directory.
      3.  Copy the latest files from the Source.zip file, from t5uid1 in the zip file into the new t5uid1 on the pi and from dgus_reloaded in the zip file into the new dgus_reloaded on the pi.
  10. Click Firmware Restart in the Mainsail window.
  11. Klipper should now display an error, "Section 'stable_z_home' is not a valid config section"
  12. Using an SSH client (like PUTtY), log into the pi and copy/paste the following sequence of commands:
      From the pi directory:
      1.  Enter: git clone https://github.com/matthewlloyd/Klipper-Stable-Z-Home.git
      2.  cd ~/klipper/klippy/extras
      3.  ln -s ~/Klipper-Stable-Z-Home/stable_z_home.py
  13. If you now inspect the directories, you should find that git has saved a clone of the repository Klipper_stable_z_home in the directory /home/pi and there is a symbolic link to the module stable_z_home.py in the /home/pi/klipper/klippy/extras folder.
  14. Select Firmware_Restart in the Mainsail menu and Klipper should now be ready to use.  IF you have any other error messages from Klipper at this point, you will need to figure out what it wants and fix it. Most of their messages are easy to understand.