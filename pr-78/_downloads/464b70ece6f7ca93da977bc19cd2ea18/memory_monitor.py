#############################################
# Personal Memory Monitor using Glances Server
#############################################
# Checks personal memory usage by user (via Glances processlist) and node-wide available memory
# Sends email alerts when thresholds are reached.

# libraries
import os
import time
import requests
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import argparse

# --- CONFIG ---
parser = argparse.ArgumentParser(description="Monitor memory usage and send alerts via email.")
parser.add_argument("--email", required=True, help="Email address to send alerts to")
parser.add_argument("--user-threshold", type=float, default=400.0, required=True, help="User memory threshold in GB")
parser.add_argument("--node-threshold", type=float, default=100.0, required=True, help="Minimum node free memory in GB")

args = parser.parse_args()
USER_EMAIL = args.email
USER_THRESHOLD_GB = args.user_threshold
NODE_FREE_MIN_GB = args.node_threshold
GLANCES_API_HOST = "http://localhost:61208"
EMAIL_COOLDOWN_MINUTES = 10
CHECK_INTERVAL = 5

last_alert_time = 0

# --- Helper Functions ---
def get_glances_api_path():
    for path in ["/api/4", "/api/3", "/api/v1"]:
        try:
            r = requests.get(f"{GLANCES_API_HOST}{path}/status", timeout=3)
            if r.ok:
                print(f"✅ Found Glances API: {path}")
                return f"{GLANCES_API_HOST}{path}/all"
        except requests.RequestException:
            continue
    raise ConnectionError("No valid Glances API found.")

def fetch_stats(api_url):
    try:
        r = requests.get(api_url, timeout=5)
        r.raise_for_status()
        return r.json()
    except requests.RequestException as e:
        print(f"⚠️ Failed to fetch Glances data: {e}")
        return None

def normalize_mb(value):
    """Convert memory in kB to MB"""
    return value / 1024  # Glances returns kB

def get_user_memory_gb(user):
    """Sum RSS memory of all processes for the user"""
    rss_kb = int(os.popen(f"ps -U {user} -o rss= | awk '{{sum+=$1}} END {{print sum}}'").read() or 0)
    return rss_kb / 1024 / 1024  # KB → GB

def send_email(subject, body, to_email):
    msg = MIMEMultipart()
    msg["From"] = to_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP("localhost") as server:
            server.sendmail(msg["From"], to_email, msg.as_string())
        print(f"📧 Alert sent: {subject}")
        return True
    except Exception as e:
        print(f"⚠️ Email failed: {e}")
        return False

def check_and_alert(api_url):
    global last_alert_time

    stats = fetch_stats(api_url)
    if not stats:
        return

    user = os.environ.get("USER", "unknown")
    user_gb = get_user_memory_gb(user)

    mem = stats.get("mem", {})
    node_total_gb = normalize_mb(mem.get("total", 0)) / 1024  # MB → GB
    node_free_gb = normalize_mb(mem.get("available", mem.get("free", 0))) / 1024  # MB → GB

    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    print(f"{timestamp} User: {user_gb:.2f} GB | Node Free: {node_free_gb:.2f}/{node_total_gb:.2f} GB")

    now_sec = time.time()
    cooldown_sec = EMAIL_COOLDOWN_MINUTES * 60

    # Determine alert
    alert_type = None
    message = None
    if user_gb > USER_THRESHOLD_GB:
        alert_type = "USER MEMORY ALERT"
        message = f"High memory usage ({user_gb:.2f} GB > {USER_THRESHOLD_GB:.1f} GB)"
    elif node_free_gb < NODE_FREE_MIN_GB:
        alert_type = "NODE MEMORY ALERT"
        message = f"Low node free memory ({node_free_gb:.2f} GB < {NODE_FREE_MIN_GB:.1f} GB)"
    else:
        return

    if now_sec - last_alert_time > cooldown_sec:
        subject = f"⚠️ {alert_type}: {message}"
        body = f"""
Hi there me!,

This is an automated system monitor.

{message}

Current stats:
- Your usage: {user_gb:.2f} GB
- Node free memory: {node_free_gb:.2f}/{node_total_gb:.2f} GB total

No more alerts will be sent for {EMAIL_COOLDOWN_MINUTES} minutes.

— Your Automated Self
        """
        if send_email(subject, body, USER_EMAIL):
            last_alert_time = now_sec
    else:
        remaining = int(cooldown_sec - (now_sec - last_alert_time))
        print(f"⏳ Alert on cooldown ({remaining}s left).")

# --- Main Loop ---
def main():
    print("--- Memory Monitor Starting ---")
    try:
        api_url = get_glances_api_path()
        user = os.environ.get("USER", "unknown")
        print(f"Monitoring {user} every {CHECK_INTERVAL}s (Email cooldown: {EMAIL_COOLDOWN_MINUTES} min)")
        print("----------------------------------------")

        while True:
            check_and_alert(api_url)
            time.sleep(CHECK_INTERVAL)
    except KeyboardInterrupt:
        print("Monitor stopped by user.")
    except Exception as e:
        print(f"FATAL ERROR: {e}")

if __name__ == "__main__":
    main()
