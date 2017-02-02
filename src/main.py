from machine import Pin, I2C
import time # for sleep_ms
import measure_Si7021 # for measurement functions
from umqtt.simple import MQTTClient


print('\n*************************************************************')
print('Welcome to the Sexual Keiling Temperature and Humidity Sensor\n')
input('Press Enter to continue\n')

i2c = I2C(scl=Pin(5),sda=Pin(4),freq=100000) #construct and initialise I2C object

# read slave address of I2C sensors
i2c_addr_list = i2c.scan()
addr_LIS3DH = i2c_addr_list[0]
addr_Si7021 = i2c_addr_list[1]

print('Accel. Sensor address =', hex(addr_LIS3DH))
print('Temp/RH Sensor address =', hex(addr_Si7021), '\n')
"""
if addr_Si7021 != 0x40:
    print('FAILURE: Address of Si7021 should be 0x40, but is', hex(addr_Si7021), 'instead\n')
    quit()
"""
while 1:

    result = measure_Si7021.measure_both(i2c, addr_Si7021)
    print('RH measured as', result['humi'], '%, \t temp measured as', result['temp'], 'oC')

    time.sleep_ms(250)
