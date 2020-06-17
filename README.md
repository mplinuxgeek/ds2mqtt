# ds2mqtt
Python script for reading DS18B20 sensors and publishing the values via MQTT with Home Assistant config/discovery support.

```
pi@zigbeegw:~/ds2mqtt $ ./ds2mqtt 
06/17/2020 03:26:47 AM - ds2mqtt - INFO - Connecting to 192.168.1.60
06/17/2020 03:26:48 AM - ds2mqtt - INFO - Connection successful
06/17/2020 03:26:48 AM - ds2mqtt - INFO - Found 2 sensors
06/17/2020 03:26:48 AM - ds2mqtt - INFO - Publishing config for sensor 00000c35451e
06/17/2020 03:26:48 AM - ds2mqtt - INFO - Publishing config for sensor 0316721d14ff
06/17/2020 03:26:49 AM - ds2mqtt - INFO - Publishing sensor 00000c35451e (DS18B20), temperature: 25.12°C
06/17/2020 03:26:50 AM - ds2mqtt - INFO - Publishing sensor 0316721d14ff (DS18B20), temperature: 18.00°C
06/17/2020 03:26:50 AM - ds2mqtt - INFO - Sleeping for 30 seconds
```

The script was written to support using DS18B20 sensors on a Raspberry Pi Zigbee Gateway Hat I have designed:
https://github.com/mplinuxgeek/rpi_cc2530-cc2591_hat
