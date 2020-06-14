#!/usr/bin/env python

import json
import time
from w1thermsensor import W1ThermSensor
import paho.mqtt.client as mqtt

broker_address="192.168.1."
port = 1884
user = ""
password = ""
topic = "ds2mqtt"

THERM_SENSOR_DS18S20 = 0x10
THERM_SENSOR_DS1822 = 0x22
THERM_SENSOR_DS18B20 = 0x28
THERM_SENSOR_DS1825 = 0x3B
THERM_SENSOR_DS28EA00 = 0x42
THERM_SENSOR_MAX31850K = 0x3B
TYPE_NAMES = {
    THERM_SENSOR_DS18S20: "DS18S20",
    THERM_SENSOR_DS1822: "DS1822",
    THERM_SENSOR_DS18B20: "DS18B20",
    THERM_SENSOR_DS1825: "DS1825",
    THERM_SENSOR_DS28EA00: "DS28EA00",
    THERM_SENSOR_MAX31850K: "MAX31850K",
}

degree = u"\N{DEGREE SIGN}"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code {}".format(rc))

client = mqtt.Client()
client.on_connect = on_connect
client.username_pw_set(user, password=password)
client.connect(broker_address)
client.loop_start()

for sensor in W1ThermSensor.get_available_sensors():
    sensor_type_name = TYPE_NAMES.get(sensor.type, hex(sensor.type))
    discover = {}
    discover['unit_of_measurement'] = degree + 'C'
    discover['icon'] = 'mdi:thermometer'
    discover['name'] = sensor.id
    discover['state_topic'] = topic + '/sensor/' + sensor.id + '/state'
    discover['unique_id'] = sensor.id
    discover['device'] =  {
        "identifiers": sensor.id,
        "manufacturer": "Dallas",
        "model": sensor_type_name,
        "name": sensor.id,
    }
    json_str = json.dumps(discover)
    client.publish("homeassistant/sensor/" + sensor.id + "/temp/config",json_str)

while True:
    for sensor in W1ThermSensor.get_available_sensors():
        temperature = sensor.get_temperature()
        sensor_id = sensor.id
        print("Sensor %s has temperature %.2f" % (sensor_id, temperature))
        client.publish(topic + "/sensor/" + sensor_id +'/state', round(temperature,2))
    time.sleep(30)
