import serial
import time
import string
import pynmea2

def getCoords() :
	gps=""
	
	port = "/dev/serial0"
	ser = serial.Serial(port, baudrate=9600, timeout=0.5)
	dataout = pynmea2.NMEAStreamReader()
	newdata = ser.readline()

	if newdata[0:6] == b'$GNRMC' or newdata[0:6] == b'$GPRMC' :
		newmsg = pynmea2.parse(newdata.decode('utf-8'))
		lat = newmsg.latitude
		lng = newmsg.longitude
		if lat != 0.0 or lng != 0.0 :
			gps = "Latitude = " + str(lat) + " and Longitude = " + str(lng)

		gps = "Latitude = " + str(lat) + " and Longitude = " + str(lng)
	return gps
		
