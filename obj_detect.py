from paho.mqtt import client as mqtt_client
import subprocess

f = open('/home/pi/RPI-1/ip.txt', 'r')
broker = f.read().strip()
#kafka_broker = broker + ":9092"
port = 1883
topic = "image_path"
username = 'user'
password = 'pwd'


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("\nConnected to MQTT Broker! topic - " + topic)
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client()
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client
    
def subscribe(client: mqtt_client):
	def on_message(client, userdata, msg):
		filepath = str(msg.payload.decode())
		print("\n" + filepath)
		print(subprocess.run(["python", "/home/pi/RPI-1/mobilenet/obj_det.py", "--prototxt", "/home/pi/RPI-1/mobilenet/SSD_MobileNet_prototxt.txt", "--model", "/home/pi/RPI-1/mobilenet/SSD_MobileNet.caffemodel", "--i", "/home/pi/RPI-1/" + filepath]))
		print(subprocess.run(["python", "/home/pi/RPI-1/gdrive_upload/upload.py", "/home/pi/RPI-1/" + filepath]))
	client.subscribe(topic)
	client.on_message = on_message

def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()
