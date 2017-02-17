from machine import Pin, I2C, RTC
from umqtt.simple import MQTTClient
import time # for sleep_ms
import measure_Si7021 # for temp/RH measurement functions
import measure_LIS3DH # for accel measurement functions
import MQTT # for MQTT functions
import rtc_functions # for RTC functions
import stats # for mean_of_list

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
print('accel. Sensor address =', hex(addr_LIS3DH))
print('temp/rh Sensor address =', hex(addr_Si7021), '\n')
if addr_LIS3DH != 0x18:
    print('FAILURE: address of Si7021 should be 0x18, but is', hex(addr_LIS3DH), 'instead\n')
if addr_Si7021 != 0x40:
    print('FAILURE: address of Si7021 should be 0x40, but is', hex(addr_Si7021), 'instead\n')

measure_LIS3DH.init_accel(i2c, addr_LIS3DH) # initialise  accelerometer

is_time_set = False

if not MQTT.connect_to_network():
    print('FAILURE: could not connect to EEERover WiFi')

else:

    # wait for time message and calibrate resting values of acceleration
    x_list, y_list, z_list = [], [], []
    time_client = MQTT.subscribe_time() # subscribe to the broker's time message

    print('waiting for broker time message...')
    print('ensure that device is resting flat on a still surface while accelerometer parameters are calibrated')
    while is_time_set == False:
        is_time_set, initial_datetime_str = MQTT.check_time(time_client)
        if is_time_set == True:
            led.high()
            rtc = rtc_functions.parse_datetime_string(initial_datetime_str)
            print('\tclock set')

            #calculate resting values as the mean of the values whist waiting for broker
            x_rest = int(stats.mean_of_list(x_list))
            y_rest = int(stats.mean_of_list(y_list))
            z_rest = int(stats.mean_of_list(z_list))

            print('\tresting x, y, z values are', x_rest, ',', y_rest, ',', z_rest, '\n')

        else:
            # blink LED with total pause of 0.5s
            led.high()
            time.sleep_ms(400)
            led.low()
            time.sleep_ms(100) # pause between loops

            # add resting accelerometer measurement to list
            x_temp,y_temp,z_temp = measure_LIS3DH.measure_accel(i2c)
            x_list.append(x_temp)
            y_list.append(y_temp)
            z_list.append(z_temp)

    temp_humi_measure_delay = 17
    # do sensing and publishing loop
    while 1:

        x_list, y_list, z_list, temp_list, humi_list = [], [], [], [], []
        for i in range (20):

            if i == 0: # blink led once in every 20 loops
                led.high()

            # append acceleration sample to list
            x_raw, y_raw, z_raw = measure_LIS3DH.measure_accel(i2c)
            x_list.append(abs(x_raw - x_rest))
            y_list.append(abs(y_raw - y_rest))
            z_list.append(abs(z_raw - z_rest))

            # append temp_humi sample to list
            temp_humi = measure_Si7021.measure_both(i2c, addr_Si7021)
            temp_list.append(temp_humi['temp'])
            humi_list.append(temp_humi['humi'])

            # pause to save resources
            time.sleep_ms(100 - temp_humi_measure_delay)

            if i == 0: # blink led once in every 20 loops
                led.low()

        # take max values of accelerations
        x_max, y_max, z_max = max(x_list), max(y_list), max(z_list)
        print('\nx,y,z', x_max, y_max, z_max)
        max_accel = max(x_max, y_max, z_max)

        # take means of tempa and humi
        temp_mean = stats.mean_of_list(temp_list)
        humi_mean = stats.mean_of_list(humi_list)

        MQTT.publish_packet(temp_mean, humi_mean, max_accel, rtc_functions.get_time_string(rtc))
