from machine import Pin, I2C
import time, measure_Si7021

i2c = I2C(scl=Pin(5),sda=Pin(4),freq=100000)

i2c_AddrList = i2c.scan()
addr_Si7021 = i2c_AddrList[0]

print("I2C address =",hex(addr_Si7021))
if addr_Si7021 != 0x40:
    print("Address should be 0x40, but is",hex(addr_Si7021),"instead")
    quit()

while 1:

    temp_C = measure_Si7021.measure_temp(i2c, addr_Si7021)
    print("Temp measured as",temp_C,"degrees C")

    humidity = measure_Si7021.measure_humi(i2c, addr_Si7021)
    print("Relative Humidity measured as",humidity,"%")

    time.sleep_ms(250)
