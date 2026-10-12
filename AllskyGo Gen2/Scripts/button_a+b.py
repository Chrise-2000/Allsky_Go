from gpiozero import Button
import subprocess
from datetime import datetime, timedelta
from signal import pause

button_a = Button(9, pull_up=True)

# Hold button B for 2 seconds to trigger shutdown
button_b = Button(10, pull_up=True)

# Flag to prevent short-press action after a long press
long_press_triggered = False


def run_script():
    yesterday = (datetime.today() - timedelta(days=1)).strftime('%Y%m%d')
    input_dir = f"/home/pi/allsky/images/{yesterday}"

    subprocess.run(["python", "gfd_buzzer.py"], check=True)
    subprocess.run(
        ["/bin/bash", "/home/pi/allsky/scripts/generateForDay.sh", input_dir],
        check=True
    )
    subprocess.run(["python", "done_buzzer.py"], check=True)


def shutdown_system():
    global long_press_triggered

    long_press_triggered = True

    subprocess.run(["python", "shutdown_buzzer.py"], check=True)
    subprocess.run(["sudo", "shutdown", "-h", "now"], check=True)


def button_a_released():
    global long_press_triggered

    # Ignore release after a long press
    if long_press_triggered:
        long_press_triggered = False
        return

    # Short press action
    subprocess.run(["python", "wps_buzzer.py"], check=True)
    subprocess.run(["python", "wps_connection.py"], check=True)
    subprocess.run(["python", "done_buzzer.py"], check=True)


button_b.when_pressed = run_script

button_a.when_held = shutdown_system
button_a.when_released = button_a_released

pause()