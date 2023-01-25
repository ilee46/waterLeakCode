from picamera import Picamera

camera = PiCamera()
camera.start_recording('home/pi/test.h264')
camera.stop_recording()
#adding more soon
