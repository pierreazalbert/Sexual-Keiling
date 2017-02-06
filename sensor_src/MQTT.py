"""
Functions for MQTT with ESP8266
"""

"""
connects device to network
inputs:
    network_essid - essid of network as a string, default = 'EEERover'
    network_passw - password of network as a string, default = 'exhibition'
outputs:
    True if success, False if fail
"""
def connect_to_network(network_essid = 'EEERover', network_passw = 'exhibition'):
    import network, time

    # setup station connection - to connect ESP8266 to router
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(network_essid, network_passw)

        # verify connection
        timeout_counter = 0
        timeout_limit = 10000 # 10 seconds
        while not sta_if.isconnected():
            timeout_counter = timeout_counter + 1
            if timeout_counter >= timeout_limit:
                print('could not connect to network')
                return False
            time.sleep_ms(1)
        if timeout_counter < timeout_limit:
            print('successfully connected to', network_essid, 'in', timeout_counter, 'ms')

    print('network config:', sta_if.ifconfig())

    # setup access point connection - so other devices can connect to ESP8266
    ap_if = network.WLAN(network.AP_IF)
    ap_if.active(False) # disable automatic access point to reduce overheads
    return True

"""
publishes informtation through MQTT
inputs:
    data - preferably in JSON format as a string
outputs:
    none
"""
def publish(data):
    from umqtt.simple import MQTTClient
    import machine

    broker_address = '192.168.0.10'
    topic = 'esys/sexual-keiling/'

	# connect, publish and disconnect
    client = MQTTClient(machine.unique_id(),broker_address)
    client.on_connect = on_connect
    client.connect()
    client.publish(topic, bytes(data,'utf-8'))
    client.disconnect()
    print('published: "' + data + '" to ' + topic)

"""
publishes dict with temp and humi informtation through MQTT
inputs:
    temp - temperature value
    humi - humidity value
outputs:
    none
"""
def publish_temp_humi(temp, humi):
    import json

    json_derulo = {
        'temp': temp,
        'humi': humi
    }
    publish(json.dumps(json_derulo)) # publish json obj as a string

# runs when successful connection to server is made
def on_connect(client, userdata, rc):
    print("Connected with result code " + str(rc))
