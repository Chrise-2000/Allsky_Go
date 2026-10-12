import subprocess
import time
import sys

subprocess.run(
    ["sudo", "wpa_cli", "-i", "wlan0", "wps_pbc"],
    check=True
)

for _ in range(30):
    result = subprocess.run(
        ["sudo", "wpa_cli", "-i", "wlan0", "status"],
        capture_output=True,
        text=True
    )

    if "wpa_state=COMPLETED" in result.stdout:
        print("Connected.")
        sys.exit(0)

    time.sleep(1)

print("WPS timeout after 30 seconds.")
sys.exit(1)