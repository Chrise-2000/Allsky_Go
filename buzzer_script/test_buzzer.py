#Connect Buzzer to the following GPIO Pints
#PIN  13 +ve (Red)
#PIN GRN -ve (Black)

#Set pin13 as Output

#########test_buzzer.py##################

from gpiozero import PWMOutputDevice
from time import sleep

buzzer = PWMOutputDevice(13, frequency=1000)  # 1kHz tone

buzzer.value = 0.5  # 50% duty cycle
sleep(2)  # Play tone for 2 seconds
buzzer.value = 0  # Turn off buzzer


