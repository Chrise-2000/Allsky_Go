from gpiozero import PWMOutputDevice
from time import sleep

buzzer = PWMOutputDevice(13)

# Define musical notes (Hz)
C = 523
E = 659
F = 698
G = 784

# Define melody sequence (notes & durations)
melody = [
    (F, 0.3),
    (0, 0.1),  # Short pause
    (G, 0.3),
]

# Play the melody
for note, duration in melody:
    buzzer.frequency = note
    buzzer.value = 0.9  # 50% duty cycle
    sleep(duration)

# Turn off the buzzer
buzzer.value = 0
print("CODE complete!")
