import RPi.GPIO as GPIO
import time

pins = [24, 27, 17, 23]
#pins =  [23, 17, 27, 24]

sequence = [
    [1,0,0,0],
    [1,1,0,0],
    [0,1,0,0],
    [0,1,1,0],
    [0,0,1,0],
    [0,0,1,1],
    [0,0,0,1],
    [1,0,0,1]
]

GPIO.setmode(GPIO.BCM)
for p in pins:
    GPIO.setup(p, GPIO.OUT)
    GPIO.output(p, 0)

delay = 0.006
steps_per_rev = 4096
step_index = 0

for _ in range(steps_per_rev):
    pattern = sequence[step_index]
    for pin, val in zip(pins, pattern):
        GPIO.output(pin, val)
    step_index = (step_index - 1) % len(sequence)
    time.sleep(delay)

GPIO.cleanup()


