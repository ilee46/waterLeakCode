import cv2
water_cascade = cv2.CasacadeClassifier("water.xml")

vid_capture = cv2.VideoCapture('/home/ianlee/test2.mp4')

while True:
    ret, img = vid_capture.read()
    
    