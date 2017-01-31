# reads temperature
# inputs:
#   i2c - I2C object
#   addr_Si7021 - slave address of sensor (int)
# outputs
#   temperature in degrees C
def measure_temp(i2c, addr_Si7021=0x40):
    import time

    temp_readCommand = bytearray([0xF3])
    temp_minDelay = 7 #ms, comes from datasheet

    i2c.writeto(addr_Si7021, temp_readCommand) # send read command
    time.sleep_ms(temp_minDelay) # wait for conversion to be complete
    temp_code = i2c.readfrom(0x40, 2) # read result

    return (175.72 * (256*temp_code[0] + temp_code[1])/65536) - 46.85

# reads humidity
# inputs:
#   i2c - I2C object
#   addr_Si7021 - slave address of sensor (int)
# outputs
#   humidity %
def measure_humi(i2c, addr_Si7021=0x40):
    import time

    humi_readCommand = bytearray([0xF5])
    humi_minDelay = 17 #ms, comes from datasheet

    i2c.writeto(addr_Si7021, humi_readCommand) # send read command
    time.sleep_ms(humi_minDelay) # wait for conversion to be complete
    humi_code = i2c.readfrom(addr_Si7021, 2) # read result

    return (125*humi_code[0] + humi_code[1])/65536 - 6

# reads temperature and humidity
# inputs:
#   i2c - I2C object
#   addr_Si7021 - slave address of sensor (int)
# outputs
#   'temp' - temperature in degrees C
#   'humi' - humidity %
def measure_both(i2c, addr_Si7021=0x40):
    import time

    humi_readCommand = bytearray([0xF5])
    humi_minDelay = 17 #ms, comes from datasheet
    # this command reads temp from previous humi measurement
    temp_readCommand_noMeasure = bytearray([0xE0])

    # measure and read humidity
    i2c.writeto(addr_Si7021, humi_readCommand) # send read command
    time.sleep_ms(humi_minDelay) # wait for conversion to be complete
    humi_code = i2c.readfrom(addr_Si7021, 2) # read result
    # read temp
    i2c.writeto(addr_Si7021, temp_readCommand_noMeasure) # send read command
    temp_code = i2c.readfrom(addr_Si7021, 2) # read result

    humi = (125*humi_code[0] + humi_code[1])/65536 - 6
    temp = (175.72 * (256*temp_code[0] + temp_code[1])/65536) - 46.85

    return { 'temp':temp, 'humi':humi }
