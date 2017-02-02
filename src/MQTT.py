"""
Functions for MQTT with ESP8266
"""

def connect_to_network():
    import network

    network_essid = '<EEERover>'
    network_passw = '<exhibition>'

    # setup station connection - to connect ESP8266 to router
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(network_essid, network_passw)
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())

    # setup access point connection - so other devices can connect to ESP8266
    ap_if = network.WLAN(network.AP_IF)
    ap_if.active(False) # disable automatic access point to reduce overheads


def mqtt_publish(topic, data):
    from umqtt.simple import MQTTClient

    broker_address = '192.168.0.10'
    topic_prefix = 'esys/<Sexual-Keiling>/'

    client = MQTTClient(machine.unique_id(),broker_address)
    client.connect()
    client.publish(topic_prefix + topic, bytes(data,'utf-8'))
