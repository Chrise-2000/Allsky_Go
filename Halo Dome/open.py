import time
from gpiozero import OutputDevice

# 360degrees of rotation is equivalent to 4096 steps

# ULN2003 driver pins (reference gpio pins for each motor driver connection)
pin1 = OutputDevice(17)
pin2 = OutputDevice(27)
pin3 = OutputDevice(22)
pin4 = OutputDevice(23)

motor_pins = [pin1, pin2, pin3, pin4]

# Standard half-step sequence for 28BYJ-48
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
    direction = 1  # always forward
    steps = abs(steps)

    step_counter = 0

    for _ in range(steps):
        for pin in range(4):
            if step_sequence[step_counter][pin]:
                motor_pins[pin].on()
            else:
                motor_pins[pin].off()

        step_counter += direction

        if step_counter >= len(step_sequence):
            step_counter = 0
        if step_counter < 0:
            step_counter = len(step_sequence) - 1

        time.sleep(delay)

    for pin in motor_pins:
        pin.off()

# Always perform the closing action
if __name__ == '__main__':
    step_motor(4096)
