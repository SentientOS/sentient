import random
import csv
import argparse

# Log message templates
TEMPLATES = {
    "SAFE": [
        "Boot completed successfully",
        "User {user} logged in via {method}",
        "Battery level at {percent}%",
        "App {package} started",
        "System update installed",
        "Time synchronized with NTP server",
        "Log rotation completed",
        "Device connected to Wi-Fi network",
        "Screen turned off",
        "Background task finished"
    ],
    "WARNING": [
        "Battery level low: {percent}%",
        "High network latency: {latency}ms",
        "Unusual CPU usage: {cpu}%",
        "Repeated login failure from {ip}",
        "Filesystem usage high: {percent}%",
        "App {package} behaving abnormally",
        "Service {service} not responding",
        "Device {device} disconnected unexpectedly",
        "Possible DoS pattern detected",
        "Disk I/O threshold exceeded"
    ],
    "THREAT": [
        "Root access granted to {user}",
        "Unauthorized access attempt from {ip}",
        "Malicious app installed: {package}",
        "Firewall rule modified by {user}",
        "SELinux policy violation detected",
        "User {user} attempted to disable security",
        "Privileged command executed without confirmation",
        "Kernel panic occurred at {time}",
        "App {package} escalated privileges",
        "Sensitive data exfiltration detected"
    ]
}

# Sample values for template variables
USERS = ["john", "alice", "root", "admin", "system"]
METHODS = ["SSH", "console", "ADB", "terminal", "graphical"]
PERCENTAGES = [5, 10, 15, 20, 25, 50, 75, 90, 95, 100]
LATENCIES = [300, 500, 800, 1000, 1500]
CPUS = [70, 80, 90, 95, 100]
IPS = ["192.168.0.1", "10.0.0.5", "172.16.42.1", "203.0.113.12"]
PACKAGES = ["com.android.settings", "com.bad.actor", "com.system.update", "com.tool.exploit", "com.security.monitor"]
DEVICES = ["USB001", "HID_USB_42", "Storage_USB_3", "Keyboard_USB"]
SERVICES = ["LocationService", "AudioDaemon", "WifiManager", "UpdateService"]
TIMES = ["12:01:33", "03:45:00", "22:17:59", "17:29:12"]

# Class distribution (safe-heavy)
CLASS_DISTRIBUTION = {
    "SAFE": 0.7,
    "WARNING": 0.2,
    "THREAT": 0.1
}

def generate_logs(num_samples):
    logs = []
    for label, ratio in CLASS_DISTRIBUTION.items():
        n = int(num_samples * ratio)
        for _ in range(n):
            template = random.choice(TEMPLATES[label])
            log = template.format(
                user=random.choice(USERS),
                method=random.choice(METHODS),
                percent=random.choice(PERCENTAGES),
                latency=random.choice(LATENCIES),
                cpu=random.choice(CPUS),
                ip=random.choice(IPS),
                package=random.choice(PACKAGES),
                device=random.choice(DEVICES),
                service=random.choice(SERVICES),
                time=random.choice(TIMES)
            )
            logs.append((log, label))
    random.shuffle(logs)
    return logs

def write_csv(logs, filename):
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["text", "label"])
        writer.writerows(logs)
    print(f"✅ Generated {len(logs)} logs and saved to {filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate an augmented log dataset")
    parser.add_argument("--samples", type=int, default=1000, help="Total number of log entries")
    parser.add_argument("--output", type=str, default="augmented_log_dataset.csv", help="Output CSV file name")
    args = parser.parse_args()

    dataset = generate_logs(args.samples)
    write_csv(dataset, args.output)

