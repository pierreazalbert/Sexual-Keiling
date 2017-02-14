"""
Functions for MQTT with ESP8266
"""

is_time_received = False
time_string = ''

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

    print('connecting to network...')
    # setup station connection - to connect ESP8266 to router
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
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
            print('\tsuccessfully connected to', network_essid, 'in', timeout_counter, 'ms')

    print('\tnetwork config:', sta_if.ifconfig())
    print('\tcomplete\n')

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
    topic = 'esys/sexual-keiling'

	# connect, publish and disconnect
    client = MQTTClient(machine.unique_id(),broker_address)
    client.connect()
    client.publish(topic, bytes(data,'utf-8'))
    client.disconnect() # connect and disconnect each time to save resources
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
        'humi': humi,
    }
    publish(json.dumps(json_derulo)) # publish json obj as a string

"""
publishes dict with temp and humi informtation through MQTT
inputs:
    temp - temperature value
    humi - humidity value
outputs:
    none
"""
def publish_packet(temp, humi, max_accel, datetime): 
    import json

    json_derulo = {
        'temp': temp,
        'humi': humi,
        'max_accel': max_accel,
        'datetime': datetime
    }
    publish(json.dumps(json_derulo)) # publish json obj as a string

"""
publishes informtation through MQTT
inputs:
    data - preferably in JSON format as a string
outputs:
    none
"""
def subscribe_time():
    from umqtt.simple import MQTTClient
    import machine

    broker_address = '192.168.0.10'
    topic = 'esys/time'
    #topic = b'esys/sexual-keiling'

	# connect, subscribe, check and disconnect
    client = MQTTClient(machine.unique_id(),broker_address)
    client.set_callback(sub_callback) # set sub_callback to run when message is received
    client.connect()
    client.subscribe(topic)

    return client

def check_time(client):
    from umqtt.simple import MQTTClient

    client.check_msg() # check for message
    if is_time_received == True: # once time has been received, disconnect
        client.disconnect()
        print(time_string)

    return is_time_received, time_string

def sub_callback(topic, msg):
    import json
    print((topic, msg))

    global is_time_received
    is_time_received = True
    global time_string
    time_json_string = msg.decode('UTF-8')
    time_json = json.loads(time_json_string)
    time_string = time_json['date']
