from machine import Pin, I2C
#import pyb # for interrupt shizzz
import time # for sleep_ms
import measure_Si7021 # for temp/RH measurement functions
import measure_LIS3DH # for accel measurement functions
import MQTT # for MQTT functions
from umqtt.simple import MQTTClient

# set up and flash LED
led = Pin(14,Pin.OUT)
led.high()
time.sleep_ms(50)
led.low()

print('\n*************************************************************')
print('Welcome to the Sexual Keiling Temperature and Humidity Sensor')
print('*************************************************************\n')

i2c = I2C(scl=Pin(5),sda=Pin(4),freq=100000) #construct and initialise I2C object

# read slave address of I2C sensors
i2c_addr_list = i2c.scan()
addr_LIS3DH = i2c_addr_list[0]
addr_Si7021 = i2c_addr_list[1]

# print and verify slave addresses
print('Accel. Sensor address =', hex(addr_LIS3DH))
print('Temp/RH Sensor address =', hex(addr_Si7021), '\n')
if addr_LIS3DH != 0x18:
    print('FAILURE: address of Si7021 should be 0x18, but is', hex(addr_LIS3DH), 'instead\n')
if addr_Si7021 != 0x40:
    print('FAILURE: address of Si7021 should be 0x40, but is', hex(addr_Si7021), 'instead\n')

measure_LIS3DH.init_accel(i2c, addr_LIS3DH)
#result = measure_Si7021.measure_both(i2c, addr_Si7021)

if not MQTT.connect_to_network():
    print('FAILURE: could not connect to EEERover WiFi')

else:
    #timer_Si7021 = pyb.Timer(1, freq = 1)
    #timer_publish = pyb.Timer(2, freq = 1)

    #timer_Si7021.callback(measure_Si7021.measure_both(i2c, addr_Si7021))
    #timer_publish.callback(MQTT.publish_packet(result['temp'], result['humi'], max_accel))

    # do sensing and publishing loop
    while 1:
        result = measure_Si7021.measure_both(i2c, addr_Si7021)
        x,y,z = measure_LIS3DH.measure_accel(i2c)
        max_accel = max(abs(x),abs(y),abs(z))

        #print('RH measured as', result['humi'], '%, \t temp measured as', result['temp'], 'oC')
        #MQTT.publish_temp_humi(result['temp'], result['humi'])
        MQTT.publish_packet(result['temp'], result['humi'], max_accel)
        time.sleep_ms(500) # pause between loops
        # set up and flash LED
