import paho.mqtt.client as mqtt

def on_connect(client, userdata, rc):
    print("Connected with result code "+str(rc))

client = mqtt.Client()
client.on_connect = on_connect
client.connect("iot.eclipse.org", 1883, 60)
client.publish('hello/', 'Hello, World!')
client.loop(2) #timeout = 2s
