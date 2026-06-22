#!/usr/bin/env python3
import json
import urllib.request
from datetime import datetime

URL = (
    "http://127.0.0.1:7125/printer/objects/query"
    "?print_stats&pause_resume&virtual_sdcard&filament_motion_sensor%20RunoutSensor"
)

def query():
    try:
        with urllib.request.urlopen(URL) as f:
            data = json.loads(f.read().decode())

        status = data["result"]["status"]

        ps = status["print_stats"]["state"]
        pr = status["pause_resume"]["is_paused"]
        vs = status["virtual_sdcard"]["file_position"]

        try:
            fs = status["filament_motion_sensor RunoutSensor"]["filament_detected"]
        except:
            fs = "N/A"

        return f"{ps} | paused={pr} | filepos={vs} | filament={fs}"

    except Exception as e:
        return f"ERROR: {e}"

if __name__ == "__main__":
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"{timestamp} | {query()}\n"
    with open("/tmp/t5uid1_state_log.txt", "a") as f:
        f.write(line)
