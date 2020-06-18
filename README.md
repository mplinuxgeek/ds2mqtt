# DS2MQTT
Python script for reading DS18B20 sensors and publishing the values via MQTT with Home Assistant config/discovery support.

## Installation:

```
sudo git clone https://github.com/mplinuxgeek/ds2mqtt /opt/ds2mqtt
sudo chown -R pi:pi /opt/ds2mqtt
cd /opt/ds2mqtt/
cp config.ini.example config.ini
nano config.ini
```

## Running:

```
cd /opt/ds2mqtt/
./ds2mqtt
CTRL+C to exit
```

## Service
I've included a service file for use with systemd, providing the above installation steps were followed the service file will work.

```
sudo cp ds2mqtt.service /etc/systemd/system/ds2mqtt.service
sudo systemctl daemon-reload
sudo systemctl start ds2mqtt
sudo systemctl status ds2mqtt
```

ds2mqtt should now be running, verify in the log output.

The systemd log can be displayed like this:

```
pi@zigbeegw:/opt/ds2mqtt $ journalctl --no-pager -u ds2mqtt.service
Jun 17 06:20:33 zigbeegw systemd[1]: Started ds2mqtt.
Jun 17 06:20:33 zigbeegw ds2mqtt[2285]: 06/17/2020 06:20:33 AM - ds2mqtt - INFO - Connecting to 192.168.1.60
Jun 17 06:20:34 zigbeegw ds2mqtt[2285]: 06/17/2020 06:20:34 AM - ds2mqtt - INFO - Connection successful
Jun 17 06:20:34 zigbeegw ds2mqtt[2285]: 06/17/2020 06:20:34 AM - ds2mqtt - INFO - Found 2 sensors
Jun 17 06:20:34 zigbeegw ds2mqtt[2285]: 06/17/2020 06:20:34 AM - ds2mqtt - INFO - Publishing config for sensor 00000c35451e
Jun 17 06:20:34 zigbeegw ds2mqtt[2285]: 06/17/2020 06:20:34 AM - ds2mqtt - INFO - Publishing config for sensor 0316721d14ff
Jun 17 06:20:35 zigbeegw ds2mqtt[2285]: 06/17/2020 06:20:35 AM - ds2mqtt - INFO - Publishing sensor 00000c35451e (DS18B20), temperature: 26.69°C
Jun 17 06:20:36 zigbeegw ds2mqtt[2285]: 06/17/2020 06:20:36 AM - ds2mqtt - INFO - Publishing sensor 0316721d14ff (DS18B20), temperature: 18.88°C
Jun 17 06:20:36 zigbeegw ds2mqtt[2285]: 06/17/2020 06:20:36 AM - ds2mqtt - INFO - Sleeping for 30 seconds

```

Following the log can be done using the -f option in journalctl:
```
journalctl -f -u ds2mqtt.service
```

The script was written to support using DS18B20 sensors on a Raspberry Pi Zigbee Gateway Hat I have designed:
https://github.com/mplinuxgeek/rpi_cc2530-cc2591_hat
