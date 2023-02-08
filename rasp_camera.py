from picamera import Picamera
from subprocess import call 

camera = PiCamera()
def conversion(f_h264, f_mp4):
  camera.start_recording('home/pi/test.h264')
  camera.stop_recording()
  command = "MP4Box -add " + f_h264 + " " + f_mp4
  call([command], shell=true)
  
  
#convert .h264 to .MP4 with MP4box
# MP4 is needed for OpenCV format
#'sudo apt install -y gpac'

convert('home/pi/test.h264',''home/pi/test.mp4')
