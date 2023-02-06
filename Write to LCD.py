#Install libraries
#sudo apt-get install python-pip
#sudo pip install RPLCD

import time        
from rpi_lcd import I2C

seconds = 0

lcd = LCD()

def writeToDisplay():
    lcd.text("Testing",0,0)
    lcd.text(str(seconds),1,0)
    lcd.text("Testing",1,2)
    second = second + 1
    time.sleep()
    
