# import the necessary packages
import numpy as np
import argparse
import cv2
import psutil
import timeit, time
import os
import subprocess
import sys


# initialize the list of class labels MobileNet SSD was trained to
# detect, then generate a set of bounding box colors for each class
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
	"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
	"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
	"sofa", "train", "tvmonitor", "peacock", "deer", "pig", "bird", "snake"]
COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

def detect(args):
	person_count = 0

	# load our serialized model from disk
	print("[INFO] loading model...")
	net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])

	# load the input image and construct an input blob for the image
	# by resizing to a fixed 300x300 pixels and then normalizing it
	# (note: normalization is done via MobileNet SSD implementation)
	image = cv2.imread(args["image"])
	(h, w) = image.shape[:2]
	blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007843,
		(300, 300), 127.5)

	# pass the blob through the network and obtain the detections and
	# predictions
	print("[INFO] computing object detections...")
	net.setInput(blob)
	detections = net.forward()

	# loop over the detections
	for i in np.arange(0, detections.shape[2]):
		# extract the confidence (i.e., probability) associated with the
		# prediction
		confidence = detections[0, 0, i, 2]
		# filter out weak detections by ensuring the `confidence` is
		# greater than the minimum confidence
		if confidence > args["confidence"]:
			# extract the index of the class label from the `detections`,
			# then compute the (x, y)-coordinates of the bounding box for
			# the object
			idx = int(detections[0, 0, i, 1])
			box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
			(startX, startY, endX, endY) = box.astype("int")
			# display the prediction
			label = "{}: {:.2f}%".format(CLASSES[idx], confidence * 100)

			if CLASSES[idx] == 'person':
				person_count += 1

			print("[INFO] {}".format(label))
			cv2.rectangle(image, (startX, startY), (endX, endY),
				COLORS[idx], 2)
			y = startY - 15 if startY - 15 > 15 else startY + 15
			cv2.putText(image, label, (startX, y),
				cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)

	print("Number of person(s) detected in the image - " + str(person_count))
	
	if person_count > 0 :
		subprocess.run(["python", "/home/pi/RPI-1/deployment-server/update.py", str(args["image"][31:-5])], capture_output = True)
	
	#show the output image
	#cv2.imshow("Output", image)
	#cv2.waitKey(0)
	#print(args["image"][31:])
	
	cv2.imwrite("/home/pi/RPI-1/mobilenet/output/" + str(args["image"][31:]), image)

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to input image")
ap.add_argument("-p", "--prototxt", required=True,
	help="path to Caffe 'deploy' prototxt file")
ap.add_argument("-m", "--model", required=True,
	help="path to Caffe pre-trained model")
ap.add_argument("-c", "--confidence", type=float, default=0.2,
	help="minimum probability to filter weak detections")
args = vars(ap.parse_args())

#Run the model
detect(args)

#Log the memory consumed by the program
s = "File Name: " + args["image"] + "\nMemory consumed: {:.3f} MB".format(psutil.Process(os.getpid()).memory_info().rss / (1024 **2))

with open("/home/pi/RPI-1/mobilenet/RESOURCE_LOG.txt", 'a') as file:
	file.write(s + '\n')

print()
