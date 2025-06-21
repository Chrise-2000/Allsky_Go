#  SHUTDOWN MELODY
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
    (G, 0.15), (F, 0.15), (E, 0.15), (C, 0.15),
]
# Play the melody
for note, duration in melody:
    buzzer.frequency = note
    buzzer.value = 0.5  # 50% duty cycle
    sleep(duration)

# Turn off the buzzer
buzzer.value = 0
print("Melody complete!")

