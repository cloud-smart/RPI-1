from paho.mqtt import client as mqtt_client
import subprocess
import sys

f = open('/home/pi/RPI-1/ip.txt', 'r')
broker = f.read().strip()
#kafka_broker = broker + ":9092"
port = 1883
topic = "motion_detection"
username = 'user'
password = 'pwd'


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker! topic - " + topic)
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client()
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        sender = str(msg.payload.decode())
        print("Received " + sender + " from " + str(msg.topic)  + " topic")
        angle = 0
        if sender == "Sender 1":
            angle = 0
        elif sender == "Sender 2":
            angle = 90
        elif sender == "Sender 3" :
            angle = 180
        import motor
        motor.turn(angle)
        print(subprocess.run(["python", "/home/pi/RPI-1/cam.py"], capture_output = True))
        #print(subprocess.run(["bash", "cam.sh", broker + ":9092"], capture_output = True))
        #motor.turn(angle = 0)
    client.subscribe(topic)
    client.on_message = on_message
    
   

def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()
