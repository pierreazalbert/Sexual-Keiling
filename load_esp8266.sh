#!/bin/bash

echo "writing accel. functions..."
ampy --port /dev/ttyUSB0 put sensor_src/measure_LIS3DH.py
echo "writing temp/RH functions..."
ampy --port /dev/ttyUSB0 put sensor_src/measure_Si7021.py
echo "writing MQTT functions..."
ampy --port /dev/ttyUSB0 put sensor_src/MQTT.py
echo "writing RTC functions..."
ampy --port /dev/ttyUSB0 put sensor_src/rtc_functions.py
echo "writing stats functions..."
ampy --port /dev/ttyUSB0 put sensor_src/stats.py
echo "writing main..."
ampy --port /dev/ttyUSB0 put sensor_src/main.py
echo "done"
