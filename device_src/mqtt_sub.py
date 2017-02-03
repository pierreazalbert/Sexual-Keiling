import paho.mqtt.client as mqtt
import json

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, rc):
    print("Connected with result code " + str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(topic_prefix)
    print("subscribed to", topic_prefix)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
    #msg_string = msg.payload.decode('UTF-8')
    #dict_derulo = json.loads(msg_string)


broker_address = '192.168.0.10'
#broker_address = 'iot.eclipse.org'
topic_prefix = 'esys/sexual-keiling/'

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker_address)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
