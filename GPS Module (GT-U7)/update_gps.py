from gps3 import gps3
import smbus
import time
import os
from datetime import datetime, timedelta

# === Setup ===
overlay_path = "/home/pi/allsky/config/overlay/gps_overlay.txt"
gps_timeout = timedelta(minutes=15)
boot_time = datetime.now()

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

def read_gps():
    global latitude, longitude
    for new_data in gps_socket:
        if new_data:
            data_stream.unpack(new_data)
            if data_stream.TPV['lat'] != 'n/a' and data_stream.TPV['lon'] != 'n/a':
                latitude = f"{data_stream.TPV['lat']:.6f}"
                longitude = f"{data_stream.TPV['lon']:.6f}"
                break
                
def read_sht31():
    try:
        bus.write_i2c_block_data(sht31_address, 0x2C, [0x06])
        time.sleep(0.5)
        data = bus.read_i2c_block_data(sht31_address, 0x00, 6)

        temp_raw = data[0] << 8 | data[1]
        humidity_raw = data[3] << 8 | data[4]

        temperature = -45 + (175 * temp_raw / 65535.0)
        humidity = 100 * humidity_raw / 65535.0

        return f"{temperature:.1f}°C", f"{humidity:.1f}%"
    except Exception:
        return "N/A", "N/A"

# === Main Loop ===
while True:
    now = datetime.now()

    # Update GPS only in the first 15 minutes
    if now - boot_time < gps_timeout:
        read_gps()

    # Always update temperature and humidity
    temp_str, humidity_str = read_sht31()

    # Write to overlay file
    with open(overlay_path, "w") as f:
        f.write(f"Latitude: {latitude}\n")
        f.write(f"Longitude: {longitude}\n")
        f.write(f"Temperature: {temp_str}\n")
        f.write(f"Humidity: {humidity_str}\n")
    time.sleep(300)  # Wait 5 minutes
