# ds2mqtt
Python script for reading DS18B20 sensors and publishing the values via MQTT with Home Assistant config/discovery support.

```
pi@zigbeegw:~/ds2mqtt $ ./ds2mqtt.py 
06/15/2020 04:41:39 PM - ds2mqtt.py - INFO - Connecting to 192.168.1.60
06/15/2020 04:41:39 PM - ds2mqtt.py - INFO - Connection successful
06/15/2020 04:41:39 PM - ds2mqtt.py - INFO - Found 2 sensors
06/15/2020 04:41:39 PM - ds2mqtt.py - INFO - Publishing config for sensor 00000c35451e
06/15/2020 04:41:39 PM - ds2mqtt.py - INFO - Publishing config for sensor 0316721d14ff
06/15/2020 04:41:40 PM - ds2mqtt.py - INFO - Publishing sensor 00000c35451e (DS18B20), temperature: 23.75°C
06/15/2020 04:41:41 PM - ds2mqtt.py - INFO - Publishing sensor 0316721d14ff (DS18B20), temperature: 17.94°C
06/15/2020 04:41:41 PM - ds2mqtt.py - INFO - Sleeping for 30 seconds
```

The script was written to support using DS18B20 sensors on a Raspberry Pi Zigbee Gateway Hat I have designed:
https://github.com/mplinuxgeek/rpi_cc2530-cc2591_hat
