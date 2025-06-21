#Remember to Insert as subprocess into Button_a+b.py script

from gpiozero import PWMOutputDevice
from time import sleep

buzzer = PWMOutputDevice(13)

# Define musical notes (Hz)
C = 523
E = 659
G = 784

# Define melody sequence (notes & durations)
melody = [
    (C, 0.1), (0, 0.1), (C, 0.1), (0, 0.1), (C, 0.1), (E, 0.3),
    (G, 0.4)
]

# Play the melody
for note, duration in melody:
    buzzer.frequency = note
    buzzer.value = 0.5  # 50% duty cycle
    sleep(duration)

# Turn off the buzzer
buzzer.value = 0
#print("Melody complete!")


