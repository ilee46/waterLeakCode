#Install libraries
#sudo apt-get install python-pip
#sudo pip install RPLCD

import time        
from RPi_GPIO_i2c_LCD import lcd

#Intialize our I2C Display


lcdDisplay = lcd.HD44780(0x27)
seconds = 0
    
while 1:
    seconds = seconds + 1
    lcdDisplay.set("Testing",1)
    lcdDisplay.set(seconds,2)
    lcdDisplay.set("Flow rate:",3)
    lcdDisplay.set("0 L/Min",4)
    time.sleep(1)
    
    #int pin15 = 
    #X = pulseIn(pin15,HIGH);
    #Y = pulseIn(pin15,LOW);