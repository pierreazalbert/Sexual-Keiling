from machine import Pin, I2C
import time

i2c = I2C(scl=Pin(5),sda=Pin(4),freq=100000)

sensorAddr = i2c.scan()
print("I2C address =",hex(sensorAddr[0]))
if sensorAddr[0] != 0x40:
    print("Address should be 0x40, but is",hex(sensorAddr[0]),"instead")
    quit()

temp_readCommand = bytearray([0xF3])
humi_readCommand = bytearray([0xF5])
# RH measuement automatically also measures temperature, so takes a bit longer
temp_minDelay = 7 #ms
humi_minDelay = 17 #ms

while 1:
    i2c.writeto(sensorAddr[0], temp_readCommand)
    time.sleep_ms(temp_minDelay)
    temp_code = i2c.readfrom(0x40, 2)

    temp_C = (175.72 * (256*temp_code[0] + temp_code[1])/65536) - 46.85
    print("Temp measured as",temp_C,"degrees C")

    i2c.writeto(sensorAddr[0], humi_readCommand)
    time.sleep_ms(humi_minDelay)
    humi_code = i2c.readfrom(sensorAddr[0], 2)

    humidity = (125*temp_code[0] + temp_code[1])/65536 - 6
    print("Relative Humidity measured as",humidity,"%")

    time.sleep_ms(500)
