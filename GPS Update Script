from gps3 import gps3
import time

overlay_file = "/home/pi/allsky/config/overlay/gps_overlay.txt"

gps_socket = gps3.GPSDSocket()
data_stream = gps3.DataStream()
gps_socket.connect()
gps_socket.watch()

start_time = time.time()
runtime = 15 * 60  # 15 minutes

for new_data in gps_socket:
    if time.time() - start_time > runtime:
        break

    if new_data:
        data_stream.unpack(new_data)
        try:
            lat = float(data_stream.TPV['lat'])
            lon = float(data_stream.TPV['lon'])
        except (TypeError, ValueError):
            continue  # skip this loop if conversion fails

        with open(overlay_file, "w") as file:
            file.write(f"Latitude: {lat:.6f}\n")
            file.write(f"Longitude: {lon:.6f}\n")

        print(f"Updated overlay: Latitude = {lat:.6f}, Longitude = {lon:.6f}")

    time.sleep(1)
