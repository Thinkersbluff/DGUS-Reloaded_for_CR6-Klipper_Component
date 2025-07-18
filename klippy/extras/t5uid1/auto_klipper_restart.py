
# Thinkersbluff: If I turn the printer power off and back on, communications between Klipper and the mcu are lost, until I run a RESTART or FIRMWARE RESTART command on the Klipper Host.  Is there any command here in the T5UID1.py app that I could use to reset those communications with the Printer mcu?

# GitHub Copilot: No, there is **not** a command in your `T5UID1.py` code that can directly reset or re-establish communications with the printer MCU after a power cycle. The `T5UID1` class relies on the Klipper host's MCU management (via the `mcu` module and `self.mcu` object) for all low-level communications.
# **Summary:**  
# You must use Klipper's `RESTART` or `FIRMWARE_RESTART` commands to restore MCU communications after a power cycle. There is no function in `T5UID1.py` that can do this independently.
# If you want to automate this, you could create a macro or script on the host that detects MCU disconnects and issues a `RESTART` command, but this would be outside the scope of the `T5UID1` code.

# Thinkersbluff: Can you help me write and install such a script?

# GitHub Copilot: Certainly! Since your `T5UID1.py` code does not provide a way to reset the MCU connection, the best way to automate this is with a **Klipper host-side script** that detects MCU disconnects and issues a `RESTART` or `FIRMWARE_RESTART` command.
# Below is a simple Python script you can run on your Raspberry Pi (or wherever Klipper is running) that will monitor the Klipper log for MCU disconnects and automatically send a `RESTART` command to the Klipper host via its API.


#### 1. Install `requests` if not already installed:
#```powershell
# pip install requests

#### 2. Save this script as `auto_klipper_restart.py` on your Pi:
import time
import requests

KLIPPER_API_URL = "http://localhost:7125/printer/firmware_restart"
# **Note:**  
# You can change `KLIPPER_API_URL` to `http://localhost:7125/printer/restart` if you prefer `RESTART`.
# Make sure your Klipper API is enabled and accessible at port 7125 (default for Moonraker).
KLIPPER_LOG_PATH = "/home/pi/printer_data/logs/klippy.log"
CHECK_INTERVAL = 5  # seconds

def send_restart():
    try:
        r = requests.post(KLIPPER_API_URL)
        print("Sent FIRMWARE_RESTART command to Klipper host.")
    except Exception as e:
        print(f"Failed to send FIRMWARE_RESTART: {e}")

def monitor_log():
    print("Monitoring klippy.log for MCU disconnects...")
    last_size = 0
    while True:
        try:
            with open(KLIPPER_LOG_PATH, "r") as f:
                f.seek(last_size)
                lines = f.readlines()
                last_size = f.tell()
                for line in lines:
                    if "Lost communication with MCU" in line or "MCU 'mcu' shutdown" in line:
                        print("MCU disconnect detected!")
                        send_restart()
        except Exception as e:
            print(f"Error reading log: {e}")
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    monitor_log()

#### 3. Run the script in the background:
#```bash
# python3 /home/pi/auto_klipper_restart.py &

### How it works:
# The script tails `/home/pi/printer_data/logs/klippy.log` for MCU disconnect messages.
# When it sees a disconnect, it sends a `FIRMWARE_RESTART` command to the Klipper API.
# This will re-establish communications automatically, just as if you had run `FIRMWARE_RESTART` manually.