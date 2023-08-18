import time, datetime
from picamera2 import Picamera2, Preview
import subprocess

picam = Picamera2()

config = picam.create_preview_configuration()
picam.configure(config)

picam.start_preview()

picam.start()

x = "mobilenet/input/" + datetime.datetime.now().strftime("%d-%b-%y-%X") + ".jpeg"
picam.capture_file("/home/pi/RPI-1/" + x)

picam.close()

#subprocess.Popen(["python", "/home/pi/RPI-1/mobilenet/obj_det.py", "--prototxt", "/home/pi/RPI-1/mobilenet/SSD_MobileNet_prototxt.txt", "--model", "/home/pi/RPI-1/mobilenet/SSD_MobileNet.caffemodel", "--i", "/home/pi/RPI-1/" + x])
#subprocess.Popen(["python", "/home/pi/RPI-1/gdrive_upload/upload.py", "/home/pi/RPI-1/" + x])

