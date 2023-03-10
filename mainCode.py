import RPi.GPIO as GPIO # Imports the GPIO library
from RPi_GPIO_i2c_LCD import lcd # Imports the LCD library
import time, sys # Imports the time library
import math
GPIO.setwarnings(False)

lcdDisplay = lcd.HD44780(0x27)
seconds = 0
waterFlowPin = 13 # This is the GPIO pin for the water flow sensor
GPIO.setmode(GPIO.BCM) #Refers to pin numbers as channels
GPIO.setup(waterFlowPin, GPIO.IN) # This configures the water flow sensor as an input device
buzzerPinNum = 12 # This is the GPIO pin for the buzzer
GPIO.setwarnings(False) # This disables GPIO warnings
GPIO.setmode(GPIO.BCM) # This configures us to set modes using  
GPIO.setup(buzzerPinNum, GPIO.OUT) # This configures the buzzer as an output device.
constant = 0.006 #Constant value for converting pulse count to liters
time_new = 0.0 #Initialize time since running program
rpt_int = 10
potentialLeakPresent = False

global rate_count, tot_count
rate_count = 0
tot_count = 0

#Everytime the magnet passes the sensor, it counts the pulse
def Pulse_count(waterFlowPin):
    global rate_count, tot_count
    rate_count += 1
    tot_count += 1
    
#Add falling edge detection for pin 13 and ignoring further edge detection for 10ms
GPIO.add_event_detect(waterFlowPin, GPIO.FALLING, callback=Pulse_count, bouncetime = 10)

#MAIN
rpt_int = int(input('Input desired report interval in seconds '))#Ask user for interval for reporting 
print('Reports every ', rpt_int,' seconds')


#Buzzer function
def soundAlarm():
    BuzzerOp = GPIO.PWM(buzzerPinNum, 200)
    BuzzerOp.start(90)
    time.sleep(1)
    BuzzerOp.stop()
    time.sleep(1)

while True:
    time_new = time.time()+rpt_int #time since running incremented by the report interval
    rate_count = 0 #Reset rate count
    time.sleep(1)
    LperM = round(((rate_count*constant)/(rpt_int/60)),2) #Converts rate count to liters and report interval to minutes
    TotLit = round(tot_count * constant,1) #Converts total count to liters
    print('\nLiters / min', LperM, '(', rpt_int, 'second sample)')
    print('Total Liters ' , TotLit)
    lcdDisplay.set("Water Reporting",1)
    lcdDisplay.set("Flow Rate:",2)
    lcdDisplay.set(str(LperM), 3)
    lcdDisplay.set("Liters/Minute", 4)
    time.sleep(1)
    lcdDisplay.clear()
    
    if (LperM < 10 or LperM > 25):
        potentialLeakPresent = True
    
    if (LperM < 1):
        potentialLeakPresent = False
        
    if (LperM == 0):
        print('No flow')
        
        
    if (potentialLeakPresent):
        soundAlarm()
        
GPIO.cleanup()
print('Done')
