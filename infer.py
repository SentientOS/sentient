# external/sentient/infer.py

import time
import re

LOG_FILE = "/var/log/logcat.log"  # Update this path based on your system

def detect_threat(log_line: str) -> str:
    threat_patterns = [
        r"unauthorized access",
        r"root access granted",
        r"exploit attempt",
        r"failed login",
        r"malware detected"
    ]
    for pattern in threat_patterns:
        if re.search(pattern, log_line, re.IGNORECASE):
            return f"⚠️ Threat Detected: {pattern}"
    return ""

def monitor_logs():
    print("[Sentient] Starting log monitoring...")
    with open(LOG_FILE, "r") as log_file:
        while True:
            line = log_file.readline()
            if not line:
                time.sleep(0.5)
                continue
            alert = detect_threat(line)
            if alert:
                print(f"[Sentient Alert] {alert} | Log: {line.strip()}")

if __name__ == "__main__":
    monitor_logs()
