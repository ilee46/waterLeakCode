import RPi.GPIO as GPIO # Imports the GPIO library
import time # Imports the time library

buzzerPinNum = 12 # This is the GPIO pin for the buzzer
GPIO.setwarnings(False) # This disables GPIO warnings
GPIO.setmode(GPIO.BCM) # This configures us to set modes using  
GPIO.setup(buzzerPinNum, GPIO.OUT) # This configures the buzzer as an output


def soundAlarm():
    BuzzerOp = GPIO.PWM(buzzerPinNum, 200)
    BuzzerOp.start(75)
    time.sleep(2)
    BuzzerOp.stop()
    time.sleep(2)
    

while 1:
    soundAlarm()
    