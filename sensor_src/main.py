from machine import Pin, I2C, RTC
from umqtt.simple import MQTTClient
import time # for sleep_ms
import measure_Si7021 # for temp/RH measurement functions
import measure_LIS3DH # for accel measurement functions
import MQTT # for MQTT functions
import rtc_functions # for RTC functions

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

is_time_set = False

if not MQTT.connect_to_network():
    print('FAILURE: could not connect to EEERover WiFi')

else:

    # wait for time message
    time_client = MQTT.subscribe_time()
    print('waiting for broker time message...')
    while is_time_set == False:
        is_time_set, initial_datetime_str = MQTT.check_time(time_client)
        if is_time_set == True:
            led.high()
            rtc = rtc_functions.parse_datetime_string(initial_datetime_str)
            print('clock set')
        else:
            # blink LED with total pause of 1s
            led.high()
            time.sleep_ms(400)
            led.low()
            time.sleep_ms(100) # pause between loops

    # do sensing and publishing loop
    while 1:

        result = measure_Si7021.measure_both(i2c, addr_Si7021)
        x,y,z = measure_LIS3DH.measure_accel(i2c)
        max_accel = max(abs(x),abs(y),abs(z))

        #print('RH measured as', result['humi'], '%, \t temp measured as', result['temp'], 'oC')
        #MQTT.publish_temp_humi(result['temp'], result['humi'])
        MQTT.publish_packet(result['temp'], result['humi'], max_accel, rtc_functions.get_time_string(rtc))

        # blink LED with total pause of 1s
        led.high()
        time.sleep_ms(100)
        led.low()
        time.sleep_ms(900)
