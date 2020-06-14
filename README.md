# ds2mqtt
Python script for reading DS18B20 sensors and publishing the values via MQTT with Home Assistant config/discovery support.

```
pi@zigbeegw:~ $ ds2mqtt/ds2mqtt.py 
Connecting to 192.168.1.60
Connection successful
Publishing config for sensor 00000c35451e
Publishing config for sensor 0316721d14ff
DS18B20 00000c35451e 23.81°C
DS18B20 0316721d14ff 18.38°C
Sleeping for 30 seconds
```

The script was written to support using DS18B20 sensors on a Raspberry Pi Zigbee Gateway Hat I have designed:
https://github.com/mplinuxgeek/rpi_cc2530-cc2591_hat
