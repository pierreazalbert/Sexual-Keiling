"""
Functions to measure temperature and/or relative humidity from Si7021 I2C sensor
"""

"""
reads 3 axis accelerometer
inputs:
i2c - I2C object
addr_LIS3DH - slave address of sensor (int)
outputs:
acceleration for axes x, y, z
"""
def measure_accel(i2c, addr_LIS3DH=0x18):
    import time

    # to use I2C, CS pin must be tied high

    # Select control register1, 0x20(32)
    #		0x2F        Power ON mode, Low Power enabled, Data rate 10 Hz
    #					X, Y, Z-Axis enabled
    control_register_value = bytearray([0x2F])
    i2c.writeto_mem(addr_LIS3DH, 0x20, control_register_value)

    # Select control register4, 0x23(35)
    #		0x00(00)	Continuous update, Full-scale selection = +/-2G
    control_register_value = bytearray([0x00])
    i2c.writeto_mem(addr_LIS3DH, 0x23, control_register_value)

    time.sleep(0.5) # todo check how short this can be made

    # X-Axis (LSB, MSB)
    # Read data back from 0x28(40), 2 bytes
    data0 = i2c.readfrom_mem(addr_LIS3DH, 0x28, 1)
    #data1 = i2c.readfrom_mem(addr_LIS3DH, 0x29, 1)
    xAccl = data0[0] #* 256 + data0[0]
    #if xAccl > 32767 :
        #xAccl -= 65536
    if xAccl > 127: # two's complement conversion
        xAccl -= 256

    # Y-Axis (LSB, MSB)
    # Read data back from 0x28(40), 2 bytes
    data0 = i2c.readfrom_mem(addr_LIS3DH, 0x2A, 1)
    #data1 = i2c.readfrom_mem(addr_LIS3DH, 0x2B, 1)
    yAccl = data0[0] #* 256 + data0[0]
    #if yAccl > 32767 :
        #yAccl -= 65536
    if yAccl > 127: # two's complement conversion
        yAccl -= 256

    # Z-Axis (LSB, MSB)
    # Read data back from 0x28(40), 2 bytes
    data0 = i2c.readfrom_mem(addr_LIS3DH, 0x2C, 1)
    #data1 = i2c.readfrom_mem(addr_LIS3DH, 0x2D, 1)
    zAccl = data0[0] #* 256 + data0[0]
    #if zAccl > 32767 :
        #zAccl -= 65536
    if zAccl > 127: # two's complement conversion
        zAccl -= 256

    return xAccl, yAccl, zAccl
