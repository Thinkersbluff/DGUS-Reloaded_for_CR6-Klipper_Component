#!/usr/bin/env python3
import json
import csv
import os
from datetime import datetime

TXT_LOG = "/tmp/t5uid1_state_log.txt"
CSV_LOG = "/home/pi/printer_data/config/t5uid1_state_log_export.csv"
HTML_REPORT = "/home/pi/printer_data/config/t5uid1_log_report.html"

def parse_txt_line(line):
    """Parse old-style text log lines."""
    if "MARK:" in line:
        ts, msg = line.split("|", 1)
        return {
            "timestamp": ts.strip(),
            "type": "mark",
            "mark": msg.strip().replace("MARK:", "").strip()
        }

    if line.strip().startswith("{"):
        # JSON-style entry
        try:
            data = json.loads(line)
            data["type"] = "json"
            return data
        except:
            return None

    # Old text format
    try:
        ts, rest = line.split("|", 1)
        return {
            "timestamp": ts.strip(),
            "type": "raw",
            "raw": rest.strip()
        }
    except:
        return None

def parse_csv():
    """Parse CSV export."""
    rows = []
    if not os.path.exists(CSV_LOG):
        return rows

    with open(CSV_LOG) as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["type"] = "csv"
            rows.append(row)
    return rows

def load_logs():
    entries = []

    # Prefer CSV if available
    if os.path.exists(CSV_LOG):
        return parse_csv()

    # Otherwise parse TXT
    if os.path.exists(TXT_LOG):
        with open(TXT_LOG) as f:
            for line in f:
                parsed = parse_txt_line(line)
                if parsed:
                    entries.append(parsed)

    return entries

def parse_ts(ts):
    try:
        return datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")
    except:
        return None

def analyze(entries):
    anomalies = []
    marks = []

    last_state = None
    last_page = None
    last_filament = None
    last_paused = None
    last_mark = None

    for e in entries:
        ts = e.get("timestamp", "UNKNOWN")
        ts_obj = parse_ts(ts)

        # Track marks
        if e.get("type") == "mark":
            last_mark = e.get("mark", "")
            marks.append({"timestamp": ts, "mark": last_mark})
            continue

        # CSV-style structured entries
        if e.get("type") == "csv":
            state = e.get("print_state", "")
            paused = e.get("paused", "")
            page = e.get("dgus_current_page", "")
            filament = e.get("filament_present", "")

            # Illegal transitions
            if last_state and state and state != last_state:
                valid = {
                    ("printing", "paused"),
                    ("paused", "printing"),
                    ("printing", "standby"),
                    ("standby", "printing"),
                    ("paused", "standby")
                }
                if (last_state, state) not in valid:
                    anomalies.append({
                        "timestamp": ts,
                        "type": "ERROR",
                        "message": f"Illegal transition {last_state} → {state}",
                        "mark": last_mark or ""
                    })

            # DGUS/Klipper mismatch
            if page and state:
                if page == "printing" and state != "printing":
                    anomalies.append({
                        "timestamp": ts,
                        "type": "WARNING",
                        "message": f"DGUS page=printing but Klipper state={state}",
                        "mark": last_mark or ""
                    })
                if page == "print_paused" and state != "paused":
                    anomalies.append({
                        "timestamp": ts,
                        "type": "WARNING",
                        "message": f"DGUS page=print_paused but Klipper state={state}",
                        "mark": last_mark or ""
                    })

            # Filament inconsistencies
            if last_filament is not None and filament != last_filament:
                if filament == "False":
                    anomalies.append({
                        "timestamp": ts,
                        "type": "INFO",
                        "message": "Filament runout detected",
                        "mark": last_mark or ""
                    })
                else:
                    anomalies.append({
                        "timestamp": ts,
                        "type": "INFO",
                        "message": "Filament reinserted",
                        "mark": last_mark or ""
                    })

            # Paused mismatch
            if paused == "True" and state == "printing":
                anomalies.append({
                    "timestamp": ts,
                    "type": "WARNING",
                    "message": "pause_resume.is_paused=True but print_state=printing",
                    "mark": last_mark or ""
                })

            last_state = state
            last_page = page
            last_filament = filament
            last_paused = paused

        # JSON-style entries (if you later switch to JSON logging)
        elif e.get("type") == "json":
            # You can extend this branch similarly if needed
            pass

        # Raw text entries
        elif e.get("type") == "raw":
            anomalies.append({
                "timestamp": ts,
                "type": "RAW",
                "message": e.get("raw", ""),
                "mark": last_mark or ""
            })

    return anomalies, marks

def generate_html(anomalies, marks):
    html = []
    html.append("<!DOCTYPE html>")
    html.append("<html><head><meta charset='utf-8'>")
    html.append("<title>T5UID1 DGUS/Klipper Log Report</title>")
    html.append("<style>")
    html.append("body { font-family: sans-serif; margin: 20px; }")
    html.append("h1 { font-size: 20px; }")
    html.append("table { border-collapse: collapse; width: 100%; }")
    html.append("th, td { border: 1px solid #ccc; padding: 4px 6px; font-size: 12px; }")
    html.append("th { background: #eee; }")
    html.append(".ERROR { background: #ffe0e0; }")
    html.append(".WARNING { background: #fff4cc; }")
    html.append(".INFO { background: #e0f0ff; }")
    html.append(".RAW { background: #f0f0f0; }")
    html.append("</style></head><body>")

    html.append("<h1>T5UID1 DGUS/Klipper Log Analysis Report</h1>")

    html.append("<h2>Summary</h2>")
    html.append(f"<p>Total anomalies: {len(anomalies)}</p>")
    html.append(f"<p>Total marks: {len(marks)}</p>")

    if marks:
        html.append("<h3>Marks</h3>")
        html.append("<ul>")
        for m in marks:
            html.append(f"<li><b>{m['timestamp']}</b> — {m['mark']}</li>")
        html.append("</ul>")

    html.append("<h2>Anomalies</h2>")
    if not anomalies:
        html.append("<p>No anomalies detected.</p>")
    else:
        html.append("<table>")
        html.append("<tr><th>Timestamp</th><th>Type</th><th>Message</th><th>Nearest DEBUG_MARK</th></tr>")
        for a in anomalies:
            cls = a["type"]
            html.append(
                f"<tr class='{cls}'>"
                f"<td>{a['timestamp']}</td>"
                f"<td>{a['type']}</td>"
                f"<td>{a['message']}</td>"
                f"<td>{a['mark']}</td>"
                f"</tr>"
            )
        html.append("</table>")

    html.append("</body></html>")

    with open(HTML_REPORT, "w") as f:
        f.write("\n".join(html))

if __name__ == "__main__":
    entries = load_logs()
    anomalies, marks = analyze(entries)
    generate_html(anomalies, marks)

    print("=== DGUS/Klipper HTML report generated ===")
    print(f"File: {HTML_REPORT}")
