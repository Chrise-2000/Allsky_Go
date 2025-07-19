from gpiozero import PWMOutputDevice
from time import sleep

buzzer = PWMOutputDevice(13)

# Define musical notes (Hz)
C = 523
E = 659
G = 784

# Define melody sequence (notes & durations)
melody = [
    (C, 1.0)
]

# Play the melody
for note, duration in melody:
    buzzer.frequency = note
    buzzer.value = 0.9  # 50% duty cycle
    sleep(duration)

# Turn off the buzzer
buzzer.value = 0
#print("Melody complete!")
