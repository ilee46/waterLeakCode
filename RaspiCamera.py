from picamera import PiCamera
from subprocess import call

camera = PiCamera()
def conversion(f_h264, f_mp4):
    camera.resolution = (640,480)
    camera.start_recording('/home/ianlee/test2.h264')
    camera.wait_recording(10)
    camera.stop_recording()
    command = "MP4Box -add " + f_h264 + " " + f_mp4
    call([command], shell = True)
        
    #convert .h264 to .MP4 with MP4box
    #MP4 is needed for OpenCV format
    
conversion('/home/ianlee/test2.h264', '/home/ianlee/test2.mp4')