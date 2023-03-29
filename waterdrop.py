import cv2
import numpy

waterdrop_cascade = cv2.CascadeClassifier('/home/ianlee/waterdrop.xml')
cap = cv.VideoCapture('/home/ianlee/test2.mp4')

while True:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    wd = waterdrop_cascade.detectMultiScale(gray)
    for (x,y,w,h) in wd:
        print("Dripping Water Detected")
        cv2.rectangle(img, (x,y), (x+w), (y+h), (255, 255, 0),2)
        
cap.release()
cv2.destroyAllWindows