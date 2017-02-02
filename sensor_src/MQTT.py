"""
Functions for MQTT with ESP8266
"""

"""
connects device to network
inputs:
    network_essid - essid of network as a string, default = 'EEERover'
    network_passw - password of network as a string, default = 'exhibition'
outputs:
    none
"""
def connect_to_network(network_essid = 'EEERover', network_passw = 'exhibition'):
    import network, time

    # setup station connection - to connect ESP8266 to router
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(network_essid, network_passw)

        counter = 0
        while not sta_if.isconnected():
            counter = counter + 1
            if counter == 100:
                print('could not connect to network')
                break

    print('network config:', sta_if.ifconfig())

    # setup access point connection - so other devices can connect to ESP8266
    ap_if = network.WLAN(network.AP_IF)
    ap_if.active(False) # disable automatic access point to reduce overheads

"""
publishes informtation through MQTT
inputs:
    topic - topic of publish as a string
    data - preferably in JSON format as a string
outputs:
    none
"""
def publish(topic, data):
    from umqtt.simple import MQTTClient
    import machine

    broker_address = b'192.168.0.10'
    topic_prefix = 'esys/Sexual-Keiling/'

    client = MQTTClient(machine.unique_id(),broker_address)
    client.connect()
    client.publish(topic_prefix + topic, bytes(data,'utf-8'))
