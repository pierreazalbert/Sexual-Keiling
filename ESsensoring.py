from machine import Pin, I2C

i2c = I2C(scl=Pin(5),sda=Pin(4),freq=100000)

addr = i2c.scan()

temp_read = bytearray([243])
humi_read = bytearray([245])
nbytes = 2


i2c.writeto(addr, temp_read)

temp = i2c.readfrom(addr, nbytes)

(175.72 * (256*temp[0] + temp[1])/65536) - 46.85




i2c.writeto(addr, humi_read)

humi = i2c.readfrom(addr, nbytes)

