import subprocess

# Run the WPS push-button command
subprocess.run(["sudo", "wpa_cli", "-i", "wlan0", "wps_pbc"], check=True)

# Enable network
subprocess.run(["sudo", "wpa_cli", "-i", "wlan0", "enable_network", "0"], check=True)

# Reconfigure wpa_supplicant to apply changes
# subprocess.run(["sudo", "wpa_cli", "-i", "wlan0", "reconfigure"], check=True)

# Request an IP address via DHCP
subprocess.run(["sudo", "dhclient", "wlan0"], check=True)


# Optional: wait a few seconds for connection to establish
# import time
# time.sleep(20)

# Save the network configuration
# subprocess.run(["sudo", "wpa_cli", "-i", "wlan0", "save_config"], check=True)
