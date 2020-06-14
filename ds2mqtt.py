#!/usr/bin/env python

import json
import time
import configparser
from w1thermsensor import W1ThermSensor
import paho.mqtt.client as mqtt

config = configparser.ConfigParser()
config.read('config.ini')
broker_address = config.get('mqtt', 'broker')
port = config.get('mqtt', 'broker')
user = config.get('mqtt', 'broker')
password = config.get('mqtt', 'broker')
topic = config.get('mqtt', 'broker')

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
if user != "" and password != "":
    client.username_pw_set(user, password=password)
client.connect(broker_address)
client.loop_start()

def device_config(id, type):
    device = {}
    device['unit_of_measurement'] = degree + 'C'
    device['icon'] = 'mdi:thermometer'
    device['name'] = sensor.id
    device['state_topic'] = topic + '/sensor/' + sensor.id + '/state'
    device['unique_id'] = sensor.id
    device['device'] =  {
        "identifiers": sensor.id,
        "manufacturer": "Dallas",
        "model": sensor_type_name,
        "name": sensor.id,
    }
    return json.dumps(device)
    
for sensor in W1ThermSensor.get_available_sensors():
    sensor_type_name = TYPE_NAMES.get(sensor.type, hex(sensor.type))
    device = device_config(sensor.id, sensor_type_name)
    client.publish("homeassistant/sensor/" + sensor.id + "/temp/config",device)
   
while True:
    for sensor in W1ThermSensor.get_available_sensors():
        temperature = sensor.get_temperature()
        sensor_id = sensor.id
        print("Sensor %s has temperature %.2f" % (sensor_id, temperature))
        client.publish(topic + "/sensor/" + sensor_id +'/state', round(temperature,2))
    time.sleep(30)
