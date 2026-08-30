import lgpio
import time

pins = [5, 6, 13, 19]
labels = ["Phase A", "Phase B", "Phase C", "Phase D"]

h = lgpio.gpiochip_open(0)

for pin in pins:
    lgpio.gpio_claim_output(h, pin, 0)

sequence = [
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1],
]

try:
    while True:
        for idx, step in enumerate(sequence):
            print(f"Activating: {labels[idx]}")
            for pin, val in zip(pins, step):
                lgpio.gpio_write(h, pin, val)
            time.sleep(0.5)

except KeyboardInterrupt:
    pass

finally:
    for pin in pins:
        lgpio.gpio_write(h, pin, 0)
    lgpio.gpiochip_close(h)