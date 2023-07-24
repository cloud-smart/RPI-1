from picamera import PiCamera
import time

camera = PiCamera()

camera.start_preview()
time.sleep(10)

filename = "img.jpg"

camera.capture(filename)
