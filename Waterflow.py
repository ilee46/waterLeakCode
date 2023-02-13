import RPi.GPIO as GPIO # Imports the GPIO library
import time, sys # Imports the time library
GPIO.setwarnings(False)

waterFlowPin = 13
GPIO.setmode(GPIO.BCM)
GPIO.setup(waterFlowPin, GPIO.IN)
minutes = 0
constant = 0.006
time_new = 0.0
rpt_int = 10

global rate_count, tot_count
rate_count = 0
tot_count = 0


def Pulse_count(waterFlowPin):
    global rate_count, tot_count
    rate_count += 1
    tot_count += 1
    
GPIO.add_event_detect(waterFlowPin, GPIO.FALLING, callback=Pulse_count, bouncetime = 10)

#MAIN
print('Water Flow - Approximate ', str(time.asctime(time.localtime(time.time()))))
rpt_int = int(input('Input desired report interval in seconds '))
print('Reports every ', rpt_int,' seconds')
print('Control C to exit')

while True:
    time_new = time.time()+rpt_int
    rate_count = 0
    while time.time() <= time_new:
        try:
            None
            #print(GPIO.input(input), end='')
        except KeyboardInterrupt:
            print('\nCTRL C - Exiting nicely')
            GPIO.cleanup()
            f.close()
            print('Done')
            sys.exit()
            
    minutes += 1
    
    LperM = round(((rate_count*constant)/(rpt_int/60)),2)
    TotLit = round(tot_count * constant,1)
    print('\nLiters / min', LperM, '(', rpt_int, 'second sample)')
    print('Total Liters ' , TotLit)
    print('Time (min & clock) ', minutes, '\t', time.asctime(time.localtime(time.time())),'\n')
    
GPIO.cleanup()
print('Done')

    