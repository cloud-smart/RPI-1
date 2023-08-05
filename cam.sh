SERVER_ADDR="$1"
FILENAME="img.jpg"
TOPIC="motion_detection"

#java -jar Producer.jar $SERVER_ADDR $FILENAME $TOPIC

python3 cam.py
python3 mobilenet/obj_det.py --prototxt mobilenet/SSD_MobileNet_prototxt.txt --model mobilenet/SSD_MobileNet.caffemodel --i mobilenet/nimg2.jpeg
