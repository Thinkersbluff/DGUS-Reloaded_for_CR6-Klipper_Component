#!/usr/bin/env python3
import json
import csv
import os

LOGFILE = "/tmp/t5uid1_state_log.txt"
CSVFILE = "/home/pi/printer_data/config/t5uid1_state_log_export.csv"

def parse_line(line):
    try:
        # New JSON-style entries
        if line.strip().startswith("{"):
            data = json.loads(line)
            ts = data.get("timestamp", "")
            k = data.get("klipper", {})
            d = data.get("dgus", {})

            return [
                ts,
                k.get("print_state", ""),
                k.get("paused", ""),
                k.get("filepos", ""),
                k.get("filament_present", ""),
                d.get("current_page", ""),
                d.get("is_printing", ""),
                d.get("print_pause_time", ""),
                d.get("print_start_time", "")
            ]

        # Old text-style entries
        parts = line.split("|")
        ts = parts[0].strip()
        rest = "|".join(parts[1:]).strip()
        return [ts, rest]

    except Exception:
        return None

if __name__ == "__main__":
    rows = []

    if os.path.exists(LOGFILE):
        with open(LOGFILE) as f:
            for line in f:
                parsed = parse_line(line)
                if parsed:
                    rows.append(parsed)

    with open(CSVFILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "timestamp",
            "print_state",
            "paused",
            "filepos",
            "filament_present",
            "dgus_current_page",
            "dgus_is_printing",
            "dgus_print_pause_time",
            "dgus_print_start_time"
        ])
        for r in rows:
            writer.writerow(r)
