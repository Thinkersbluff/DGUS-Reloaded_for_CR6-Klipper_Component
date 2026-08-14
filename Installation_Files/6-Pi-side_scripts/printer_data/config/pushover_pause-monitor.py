#!/usr/bin/env python3
import json
import os
import time
import requests

SECRETS_PATH = os.path.expanduser("~/printer_data/moonraker.secrets")
MOONRAKER_URL = "http://localhost:7125"

# --- Load Pushover credentials from moonraker.secrets ---
with open(SECRETS_PATH, "r") as f:
    secrets = json.load(f)

pushover_token = secrets["pushover"]["token"]
pushover_user_key = secrets["pushover"]["user_key"]

# --- Helper: query Moonraker pause state ---
def is_paused():
    try:
        r = requests.post(
            f"{MOONRAKER_URL}/printer/objects/query",
            json={"objects": {"pause_resume": ["is_paused"]}},
            timeout=3
        )
        return r.json()["result"]["status"]["pause_resume"]["is_paused"]
    except Exception:
        return False

# --- Helper: send emergency Pushover alert ---
def send_emergency_pushover(msg):
    requests.post(
        "https://api.pushover.net/1/messages.json",
        data={
            "token": pushover_token,
            "user": pushover_user_key,
            "message": msg,
            "priority": 2,
            "retry": 60,
            "expire": 3600
        },
        timeout=5
    )

# --- Helper: send BEEP_STOP to Klipper ---
def stop_beeping():
    try:
        requests.post(
            f"{MOONRAKER_URL}/printer/gcode/script",
            json={"script": "BEEP_STOP"},
            timeout=3
        )
    except Exception:
        pass

# --- Main loop ---
was_paused = False

while True:
    paused = is_paused()

    if paused:
        if not was_paused:
            # First detection of pause
            send_emergency_pushover("Printer paused — filament change required")
            was_paused = True
        else:
            # Repeating alert
            send_emergency_pushover("Printer still paused — attention required")
    else:
        if was_paused:
            # Pause ended — stop beeping
            stop_beeping()
            was_paused = False

    time.sleep(60)
