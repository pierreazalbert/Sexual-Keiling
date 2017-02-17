"""
Functions to measure temperature and/or relative humidity from Si7021 I2C sensor
"""

"""
initialises 3 axis accelerometer
inputs:
    i2c - I2C object
    addr_LIS3DH - slave address of sensor (int)
outputs:
    none (eventually self test result?)
"""
def init_accel(i2c, addr_LIS3DH=0x18):
    import time

    print('initialising Accelerometer...')

    # to use I2C, CS pin must be tied high
    #TODO self test (section 3.2.2 and 8.11)

    # Select control register1, 0x20(32)
    #		0x2F        Power ON mode, Low Power enabled, Data rate 10 Hz
    #					X, Y, Z-Axis enabled
    control_register1_value = bytearray([0x2F])
    i2c.writeto_mem(addr_LIS3DH, 0x20, control_register1_value)

    # Select control register4, 0x23(35)
    #		0x00(00)	Continuous update, Full-scale selection = +/-4G
    control_register4_value = bytearray([0x01])
    i2c.writeto_mem(addr_LIS3DH, 0x23, control_register4_value)

    time.sleep(0.5) # todo check how short this can be made
    print('\tcomplete\n')

"""
reads 3 axis accelerometer
inputs:
    i2c - I2C object
    addr_LIS3DH - slave address of sensor (int)
outputs:
    acceleration for axes x, y, z
"""
def measure_accel(i2c, addr_LIS3DH=0x18):
    # 8-bit precision, left-justified, two's complement
    # data1 data 0
    # XX00  0000

    # X-Axis (LSB, MSB)
    # Read data back from 0x28(40), 2 bytes
    #data0x = i2c.readfrom_mem(addr_LIS3DH, 0x28, 1)
    data1x = i2c.readfrom_mem(addr_LIS3DH, 0x29, 1)
    xAccl = data1x[0]
    if xAccl > 127: # two's complement conversion
        xAccl -= 256

    # Y-Axis (LSB, MSB)
    # Read data back from 0x28(40), 2 bytes
    #data0y = i2c.readfrom_mem(addr_LIS3DH, 0x2A, 1)
    data1y = i2c.readfrom_mem(addr_LIS3DH, 0x2B, 1)
    yAccl = data1y[0]
    if yAccl > 127: # two's complement conversion
        yAccl -= 256

    # Z-Axis (LSB, MSB)
    # Read data back from 0x28(40), 2 bytes
    #data0z = i2c.readfrom_mem(addr_LIS3DH, 0x2C, 1)
    data1z = i2c.readfrom_mem(addr_LIS3DH, 0x2D, 1)
    zAccl = data1z[0]
    if zAccl > 127: # two's complement conversion
        zAccl -= 256

    # print(xAccl_test, yAccl_test, zAccl_test)
    return xAccl, yAccl, zAccl
