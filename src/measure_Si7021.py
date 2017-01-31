def measure_temp(i2c, addr_Si7021=0x40):
    import time

    temp_readCommand = bytearray([0xF3])
    temp_minDelay = 7 #ms

    i2c.writeto(addr_Si7021, temp_readCommand)
    time.sleep_ms(temp_minDelay)
    temp_code = i2c.readfrom(0x40, 2)

    return (175.72 * (256*temp_code[0] + temp_code[1])/65536) - 46.85

def measure_humi(i2c, addr_Si7021=0x40):
    import time

    humi_readCommand = bytearray([0xF5])
    humi_minDelay = 17 #ms

    i2c.writeto(addr_Si7021, humi_readCommand)
    time.sleep_ms(humi_minDelay)
    humi_code = i2c.readfrom(addr_Si7021, 2)

    return (125*humi_code[0] + humi_code[1])/65536 - 6
