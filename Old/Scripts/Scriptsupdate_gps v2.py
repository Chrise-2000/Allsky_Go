from gps3 import gps3
import smbus
import time
import os
import sys
import signal
import logging
import json
from datetime import datetime, timedelta

# === Logging Setup ===
logging.basicConfig(
    filename='/home/pi/scripts/gps_overlay.log',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# === Graceful Exit ===
def signal_handler(sig, frame):
    logging.info("Exiting gracefully...")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# === Setup ===
overlay_path = "/home/pi/allsky/config/overlay/gps_overlay.txt"
gps_timeout = timedelta(minutes=30)
boot_time = datetime.now()
last_gps_fix_time = None

# === Initialize I2C for SHT31 ===
bus = smbus.SMBus(1)
sht31_address = 0x44  # or 0x45

# === GPS Setup ===
gps_socket = gps3.GPSDSocket()
data_stream = gps3.DataStream()
gps_socket.connect()
gps_socket.watch()

latitude = "N/A"
longitude = "N/A"

try:
    with open("/home/pi/scripts/last_gps.txt", "r") as f:
        lat_str, lon_str = f.read().strip().split(",")
        latitude = lat_str
        longitude = lon_str
        last_gps_fix_time = datetime.now() - timedelta(minutes=5)  # Assume recent fix
        logging.info(f"📍 Loaded last known GPS: {latitude}, {longitude}")
except Exception:
    logging.warning("No previous GPS fix found.")

# === Functions ===

def read_gps(timeout=60):
    global latitude, longitude, last_gps_fix_time
    start_time = time.time()

    for new_data in gps_socket:
        if time.time() - start_time > timeout:
            logging.warning(f"⚠️ GPS timeout after {timeout} seconds.")
            break

        if new_data:
            data_stream.unpack(new_data)
            mode = data_stream.TPV.get('mode', 1)
            lat = data_stream.TPV.get('lat', 'n/a')
            lon = data_stream.TPV.get('lon', 'n/a')

            try:
                if int(mode) >= 2 and lat != 'n/a' and lon != 'n/a' and lat != 0.0 and lon != 0.0:
                    latitude = f"{lat:.3f}"
                    longitude = f"{lon:.3f}"
                    last_gps_fix_time = datetime.now()
                    logging.info(f"✅ GPS fix: Lat {latitude}, Lon {longitude}")
                    with open("/home/pi/scripts/last_gps.txt", "w") as f:
                        f.write(f"{latitude},{longitude}")
                    break
            except (ValueError, TypeError) as e:
                pass #quietly move one
		#logging.warning(f"⚠️ Skipping invalid GPS mode value: {mode} ({e})")

# Define update settings.json V2

def update_settings_json(lat, lon):
    config_path = '/home/pi/allsky/config/settings.json'
    try:
        lat_prefix = '+' if lat >= 0 else '-'
        lon_prefix = '+' if lon >= 0 else '-'

        with open(config_path, 'r') as file:
            data = json.load(file)

        data["latitude"] = f"{lat_prefix}{abs(lat):.3f}"
        data["longitude"] = f"{lon_prefix}{abs(lon):.3f}"

        with open(config_path, 'w') as file:
            json.dump(data, file, indent=4)

        logging.info(f"📝 settings.json updated → latitude: {data['latitude']}, longitude: {data['longitude']}")
    except Exception as e:
        logging.error(f"❌ Failed to update settings.json: {e}")


# Define temp + humidity

def read_sht31():
    try:
        bus.write_i2c_block_data(sht31_address, 0x2C, [0x06])
        time.sleep(0.5)
        data = bus.read_i2c_block_data(sht31_address, 0x00, 6)

        temp_raw = data[0] << 8 | data[1]
        humidity_raw = data[3] << 8 | data[4]

        temperature = -45 + (175 * temp_raw / 65535.0)
        humidity = 100 * humidity_raw / 65535.0

        return f"{temperature:.1f}degC", f"{humidity:.1f}%"
    except Exception as e:
        logging.error(f"SHT31 read error: {e}")
        return "N/A", "N/A"

# === Main Loop ===

while True:
    now = datetime.now()

    # Try to get GPS fix if not available or expired
    if last_gps_fix_time is None or (now - last_gps_fix_time) > timedelta(minutes=10):
        read_gps()

    # Always update temperature and humidity
    temp_str, humidity_str = read_sht31()


    # Determine GPS status text for overlay
    try:
        lat_val = float(latitude)
        lon_val = float(longitude)
        if lat_val == 0.0 and lon_val == 0.0:
            gps_status = "GPS: False Fix\n"
        elif last_gps_fix_time is None or (now - last_gps_fix_time) > timedelta(minutes=10):
            gps_status = "GPS: No Fix\n"
        else:
            gps_status = f"Latitude: {latitude}\nLongitude: {longitude}\n"
            update_settings_json(latitude, longitude)
    except ValueError:
        gps_status = "GPS: No Fix\n"


    # Write to Overlay
    try:
        with open(overlay_path, "w", encoding="utf-8") as f:
            f.write(gps_status)
            f.write(f"Temperature: {temp_str}\n")
            f.write(f"Humidity: {humidity_str}\n")
        logging.info("Overlay updated.")
    except Exception as e:
        logging.error(f"Failed to write overlay: {e}")

    time.sleep(300)  # Wait 5 minutes
