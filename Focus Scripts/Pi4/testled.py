import RPi.GPIO as GPIO
import time

pins = [24, 27, 17, 23]   # IN1–IN4
labels = ["Phase A", "Phase B", "Phase C", "Phase D"]

GPIO.setmode(GPIO.BCM)
for p in pins:
    GPIO.setup(p, GPIO.OUT)
    GPIO.output(p, 0)

sequence = [
    [1,0,0,0],  # Phase A
    [0,1,0,0],  # Phase B
    [0,0,1,0],  # Phase C
    [0,0,0,1],  # Phase D
]

print("Running diagnostic…")
while True:
    for idx, step in enumerate(sequence):
        print("Activating:", labels[idx])
        for pin, val in zip(pins, step):
            GPIO.output(pin, val)
        time.sleep(0.5)

 

