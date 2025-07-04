# Startup Melody that runds 10 seconds after startup
#*****************************************
##Add startup_buzzer.py to boot files in command line:
#sudo nano /etc/rc.local   # Create Boot File 
#sudo chmod +x /etc/rc.local # Make Boot File Executable
#sudo reboot # Reboot System

#*****************************************


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
    (C, 0.13), (E, 0.13), (F, 0.15), (G, 0.2),
    (0, 0.1),  # Short pause
    (F, 0.15), (G, 0.5)
]

# Wait 10 seconds before sounding the buzzer
sleep(10)

# Play the melody
for note, duration in melody:
    buzzer.frequency = note
    buzzer.value = 0.5  # 50% duty cycle
    sleep(duration)

# Turn off the buzzer
buzzer.value = 0

