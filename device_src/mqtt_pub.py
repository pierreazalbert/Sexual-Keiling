import paho.mqtt.client as mqtt
import json

def on_connect(client, userdata, rc):
    print("Connected with result code "+str(rc))

json_derulo = {
    'time': '12:30',
    'temp': '45.2',
    'RH' : '30.34',
    'accel': ['0', '0', '0']
}

print(json_derulo)

broker_address = '192.168.0.10'
topic = 'esys/sexual-keiling'

client = mqtt.Client()
client.on_connect = on_connect
client.connect(broker_address)
client.publish(topic, json.dumps(json_derulo))
client.loop(2) #timeout = 2s
