# Alternative Script from @clevercode using gpiozero compatible with both Pi4 and Pi5 Architecture

# ***************INSTRUCTIONS**********************
# To move forward 512 steps:
# python3 allsky_focus_pi5.py 512

# To move backward 512 steps:
# python3 allsky_focus_pi5.py -512
# **************************************************

import time
import sys
from gpiozero import OutputDevice

# Map the GPIO pins for the ULN2003 Driver
# Using GPIO 5, 6, 13, 19
pin1 = OutputDevice(5)
pin2 = OutputDevice(6)
pin3 = OutputDevice(13)
pin4 = OutputDevice(19)

motor_pins = [pin1, pin2, pin3, pin4]

# Standard half step sequence for the 28BYJ-48 stepper motor
step_sequence = [
    [1, 0, 0, 1],
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1]
]

def step_motor(steps, delay=0.001):
    if steps < 0:
        direction = -1
        steps = abs(steps)
    else:
        direction = 1

    step_counter = 0

    for _ in range(steps):
        for pin in range(4):
            if step_sequence[step_counter][pin] != 0:
                motor_pins[pin].on()
            else:
                motor_pins[pin].off()

        step_counter += direction

        # Loop the sequence tracker
        if step_counter >= len(step_sequence):
            step_counter = 0
        if step_counter < 0:
            step_counter = len(step_sequence) - 1

        time.sleep(delay)

    # Turn off all pins at the end to prevent motor overheating
    for pin in motor_pins:
        pin.off()

# Listen for the number of steps from the terminal command
if __name__ == '__main__':
    if len(sys.argv) > 1:
        step_motor(int(sys.argv[1]))
