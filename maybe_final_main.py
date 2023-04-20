#Water Savers Main Code
#
#
#Authors: Liam Bennett, Cody Chan, Leonardo Garcia, Ian Lee
#
#
#ALL IMPORTS**************************************************************
import RPi.GPIO as GPIO # Imports the GPIO library
from RPi_GPIO_i2c_LCD import lcd # Imports the LCD library
import time, sys # Imports the time library
import math
from picamera import PiCamera
from subprocess import call
import tflite_runtime
from tflite_runtime.interpreter import Interpreter
import numpy as np
import time
import cv2
import os
GPIO.setwarnings(False)
camera = PiCamera()

data = "/home/ianlee/tflite1/waterdrop_tflite/"
model_path = data + "detect.tflite"
label_path = data + "labelmap.txt"
video_path = "/home/ianlee/test2.mp4"

#We need to remove the camera video in order to replace it
def removeoldvideo(videofile):
    os.remove(video_path)

#Recording a video with the camera and saving it as .MP4
def conversion(f_h264, f_mp4):
    camera.resolution = (640,480)
    camera.framerate = 30
    camera.start_recording('/home/ianlee/test2.h264')
    camera.wait_recording(30)
    camera.stop_recording()
    command = "MP4Box -add " + f_h264 + " " + f_mp4
    call([command], shell = True)
        
    #convert .h264 to .MP4 with MP4box
    #MP4 is needed for OpenCV format
    

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
page_counter = 1
up = 5 #This is the GPIO pin for the "page up" button
GPIO.setup(up, GPIO.IN, pull_up_down = GPIO.PUD_UP)
buttonPress = True

#MAIN
rpt_int = int(input('Input desired report interval in seconds '))#Ask user for interval for reporting 
print('Reports every ', rpt_int,' seconds')

#Everytime the magnet passes the sensor, it counts the pulse
def Pulse_count(waterFlowPin):
    global rate_count, tot_count
    rate_count += 1
    tot_count += 1
    
#Add falling edge detection for pin 13 and ignoring further edge detection for 10ms
GPIO.add_event_detect(waterFlowPin, GPIO.FALLING, callback=Pulse_count, bouncetime = 10)

global rate_count, tot_count
rate_count = 0
tot_count = 0

#Buzzer function
def soundAlarm():
    BuzzerOp = GPIO.PWM(buzzerPinNum, 200)
    BuzzerOp.start(90)
    time.sleep(0.7)
    BuzzerOp.stop()
    time.sleep(0.7)
#   
#Video Process
#    
def video_process():
    interpreter = Interpreter(model_path)
    interpreter.allocate_tensors()
    
    with open(label_path, 'r') as f:
        labels = [line.strip() for line in f.readlines()]
    if labels[0] == '???':
        del(labels[0])

    height = input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    height = input_details[0]['shape'][1]
    width = input_details[0]['shape'][2]

    floating_model = (input_details[0]['dtype'] == np.float32)
    input_mean = 127.5
    input_std = 127.5

    # Check output layer name to determine if this model was created with TF2 or TF1,
    # because outputs are ordered differently for TF2 and TF1 models
    outname = output_details[0]['name']

    boxes_idx, classes_idx, scores_idx = 1, 3, 0

    min_conf_threshold = 0.5 
    # Open video file
    video = cv2.VideoCapture(video_path)
    imW = video.get(cv2.CAP_PROP_FRAME_WIDTH)
    imH = video.get(cv2.CAP_PROP_FRAME_HEIGHT)
    
    while(video.isOpened()):
        # Acquire frame and resize to expected shape [1xHxWx3]
        ret, frame = video.read()
        if not ret:
            print('Reached the end of the video!')
            break
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_resized = cv2.resize(frame_rgb, (width, height))
        input_data = np.expand_dims(frame_resized, axis=0)
        input_data = (np.float32(input_data) - input_mean) / input_std

        # Perform the actual detection by running the model with the image as input
        interpreter.set_tensor(input_details[0]['index'],input_data)
        interpreter.invoke()

        # Retrieve detection results
        boxes = interpreter.get_tensor(output_details[boxes_idx]['index'])[0] # Bounding box coordinates of detected objects
        classes = interpreter.get_tensor(output_details[classes_idx]['index'])[0] # Class index of detected objects
        scores = interpreter.get_tensor(output_details[scores_idx]['index'])[0] # Confidence of detected objects

        # Loop over all detections and draw detection box if confidence is above minimum threshold
        for i in range(len(scores)):
            if ((scores[i] > min_conf_threshold) and (scores[i] <= 1.0)):
                # Get bounding box coordinates and draw box
                # Interpreter can return coordinates that are outside of image dimensions, need to force them to be within image using max() and min()
                ymin = int(max(1,(boxes[i][0] * imH)))
                xmin = int(max(1,(boxes[i][1] * imW)))
                ymax = int(min(imH,(boxes[i][2] * imH)))
                xmax = int(min(imW,(boxes[i][3] * imW)))
            
                cv2.rectangle(frame, (xmin,ymin), (xmax,ymax), (10, 255, 0), 4)
    
                # Draw label
                object_name = labels[int(classes[i])] # Look up object name from "labels" array using class index
                label = '%s: %d%%' % (object_name, int(scores[i]*100)) # Example: 'person: 72%'
                labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2) # Get font size
                label_ymin = max(ymin, labelSize[1] + 10) # Make sure not to draw label too close to top of window
                cv2.rectangle(frame, (xmin, label_ymin-labelSize[1]-10), (xmin+labelSize[0], label_ymin+baseLine-10), (255, 255, 255), cv2.FILLED) # Draw white box to put label text in
                cv2.putText(frame, label, (xmin, label_ymin-7), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2) # Draw label text
                imagecounter = 1
        # All the results have been drawn on the frame, so it's time to display it.
        cv2.imshow('Object detector', frame)

        # Press 'q' to quit
        if cv2.waitKey(1) == ord('q'):
            break

    # Clean up
    video.release()
    cv2.destroyAllWindows()
    
#runs forever
while True:
    time_new = time.time()+rpt_int #time since running incremented by the report interval
    rate_count = 0 #Reset rate count
    time.sleep(0.7)
        
    if page_counter == 1:
        LperM = round(((rate_count*constant)/(rpt_int/60)),2) #Converts rate count to liters and report interval to minutes
        TotLit = round(tot_count * constant,1) #Converts total count to liters
        print('\nLiters / min', LperM, '(', rpt_int, 'second sample)')
        print('Total Liters ' , TotLit)
        lcdDisplay.set("Water Reporting", 1)
        lcdDisplay.set("Flow Rate:", 2)
        lcdDisplay.set(str(LperM), 3)
        lcdDisplay.set("Liters/Minute", 4)
        time.sleep(0.7)
        lcdDisplay.clear()
    
        if (LperM < 10 or LperM > 25):
            potentialLeakPresent = True
    
        if (LperM < 1):
            potentialLeakPresent = False
        
        if (LperM == 0):
            print('No flow')
        
        
        if (potentialLeakPresent):
            soundAlarm()
    elif page_counter == 2:
        OperM = round(((rate_count*constant)/(rpt_int/60)) * 33.81402, 2) #Converts liters to ounces and report interval to minutes
        TotOz = round(tot_count * constant * 33.81402, 1) #Converts total count to ounces
        print('\nOunces / min', OperM, '(', rpt_int, 'second sample)')
        print('Total Ounces ' , TotOz)
        lcdDisplay.set("Water Reporting",1)
        lcdDisplay.set("Flow Rate:",2)
        lcdDisplay.set(str(OperM), 3)
        lcdDisplay.set("Ounces/Minute", 4)
        time.sleep(0.7)
        lcdDisplay.clear()
    
        if (OperM < 338.1402 or OperM > 845.3506):
            potentialLeakPresent = True
    
        if (OperM < 33.81402):
            potentialLeakPresent = False
        
        if (OperM == 0):
            print('No flow')
        
        
        if (potentialLeakPresent):
            soundAlarm()
    else:
        page_counter = 1
    
    buttonPress = GPIO.input(up)
    if buttonPress == False:
        page_counter += 1
        
GPIO.cleanup()
print('Done')

    


    