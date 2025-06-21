from gpiozero import Button
import time
import subprocess
from datetime import datetime, timedelta
from signal import pause  # Efficiently keep the script running

button_a = Button(27, pull_up=False)  # Use pull-down mode
button_b = Button(17, pull_up=False)  # Button B

def run_script():
    yesterday = (datetime.today() - timedelta(days=1)).strftime('%Y%m%d')  # Get yesterday's date
    input_dir = f"/home/pi/allsky/images/{yesterday}"  # Construct the correct INPUT_DIR path
    subprocess.run(["/bin/bash", "/home/pi/allsky/scripts/generateForDay.sh", input_dir], check=True)

def handle_press():
    start_time = time.time()

    while button_b.is_pressed:
        time.sleep(0.1)  # Measure press duration

    press_duration = time.time() - start_time

    if press_duration >= 2:  # Long press (≥2s) → Shutdown
        subprocess.run(["sudo", "shutdown", "-h", "now"], check=True)

button_a.when_pressed = run_script  # Run script when Button A is pressed
button_b.when_pressed = handle_press  # Button B triggers shutdown only on long press

pause()  # Keeps the script running efficiently without high CPU usage
