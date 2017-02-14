import paho.mqtt.client as mqtt
import json

# runs when successful connection to server is made
def on_connect_data(client, userdata, rc):
    print("Connected with result code " + str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    topic_data = 'esys/sexual-keiling'
    client.subscribe(topic_data)
    print("subscribed to", topic_data)

# runs when successful connection to server is made
def on_connect_time(client, userdata, rc):
    print("Connected with result code " + str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    topic_time = 'esys/time'
    client.subscribe(topic_time)
    print("subscribed to", topic_time)

# runs when message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
    msg_string = msg.payload.decode('UTF-8')
    #dict_derulo = json.loads(msg_string)

print('\n******************************************')
print('Welcome to the Sexual Keiling MQTT monitor')
print('******************************************\n')
print('Are you connected to the EEERover wifi?')
#input('Press Enter to continue\n')

broker_address = '192.168.0.10'

client_data = mqtt.Client()
client_data.on_connect = on_connect_data
client_data.on_message = on_message

client_time = mqtt.Client()
client_time.on_connect = on_connect_time
client_time.on_message = on_message

# todo check paho doc for a way to save this from infinite loop if no connection is made
client_data.connect(broker_address)
client_time.connect(broker_address)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
#client_data.loop_forever()
while 1:
    client_data.loop(0.1)
    client_time.loop(0.1)
