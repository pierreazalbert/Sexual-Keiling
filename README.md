# Sexual-Keiling
EE3-24 Embedded Systems - Lloyd Abbott, Pierre Azalbert, Jukka Hertzog, Periklis Korkontzelos

## Coursework 1 - IoT project

We have a temperature + humidity sensor that we can use with the Adafruit Huzzah Feather board. The board contains an ESP8266 chip with MicroPython on it.

### Deliverables
- Demo showing sensing, processing and upload of data
- Code submission via GitHub
- Website* marketing concept for product

### Timetable
- 2nd Feb: Lab on wifi
- 9th Feb: demo of project
- 16th Feb : submit code and website

### Our concept: an instrument temperature/humidity/impact monitor
- Embedded system comprising of a temperature/humidity sensor, an accelerometer, a battery and a power switch (+ Huzzah Feather ESP8266)
- Allows continuous monitoring of your instrument's casing (violin, cello, flute or even piano!)
- Detects potentially hamrful levels of humidity and/or temperature for your instrument + any strong impact (e.g. dropped case)
- Remote monitoring via Wi-Fi, mobile app with dashboard to see live data
- Sends notifications to your phone in case temperature/humidity/impact limits have been reached

### Work to be done
- [x] Set up I2C between humidity/temperature sensor and ESP8266
- [ ] Set up MQQT Wi-Fi protocol to send sensor data over the air
- [ ] Write code on desktop/laptop to receive sensor data, store it and process it (database? thresholds and alerts?)
- [ ] Make demo (static or functional) or mobile app to show live sensor data and alerts/notifications

### Optional tasks to get extra marks
- [ ] Set up I2C between accelerometer and ESP8266
- [ ] Connect battery and power switch to make device portable
- [ ] 3D print custom casing for whole device

### Useful Links
[MicroPy guide for ESP2866] (https://docs.micropython.org/en/latest/esp8266/index.html) (quick reference page will be v. useful)

[MicroPy I2C guide] (https://docs.micropython.org/en/latest/esp8266/library/machine.I2C.html)

[ESP8266 SparkFun Page w/ useful links] (https://www.sparkfun.com/products/13678)

[Feather Huzzah Guide] (https://learn.adafruit.com/adafruit-feather-huzzah-esp8266?view=all)

[Sensor documentation] (https://cdn.sparkfun.com/datasheets/Sensors/Weather/Si7021.pdf)

[Sensor SparkFun Page w/ useful links] (https://learn.sparkfun.com/tutorials/si7021-humidity-and-temperature-sensor-hookup-guide)

### Our ideas for an IoT device
instrument storage / greenhouse mointoring / holiday home environment control (prevent mould etc) / wood drying monitor (for fireplaces) / pantry monitoring / laundry drying monitor / rust n stuff / wine storage / sauna monitoring / body heat (sweat) / baby incubator / baby cradle monitor (https://blog.withings.com/2012/03/30/why-is-measuring-the-humidity-level-in-a-room-important-for-a-baby-2/) / tobacco storage (humidor) / shoe fungus prevention / home brewing, fermenting (yoghurt, etc) / biological petri dish monitor / fan-hat
