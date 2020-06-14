#!/usr/bin/env python

import os
import json
import time
import configparser
import signal
from w1thermsensor import W1ThermSensor
import paho.mqtt.client as mqtt

def keyboardInterruptHandler(signal, frame):
    print("KeyboardInterrupt (ID: {}), exiting...".format(signal))
    exit(0)

def get_config_safe(section, option, default=None):
    try:
        return config.get(section, option)
    except (configparser.NoOptionError, configparser.NoSectionError, ValueError):
        print('Could not find section [%s] option "%s"' % (section, option))
        return default

def on_connect(client, userdata, flags, rc):
    if int(str(rc)) == 0:
        print("Connection successful")
        client.connected = True
    elif int(str(rc)) == 1:
        print("Connection refused - incorrect protocol version")
    elif int(str(rc)) == 2:
        print("Connection refused - invalid client identifier")
    elif int(str(rc)) == 3:
        print("Connection refused - server unavailable")
    elif int(str(rc)) == 4:
        print("Connection refused - bad username or password")
    elif int(str(rc)) == 5:
        print("Connection refused - not authorised")

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload)) 

def device_config(id, name):
    device = {}
    device['unit_of_measurement'] = degree + 'C'
    device['icon'] = 'mdi:thermometer'
    device['name'] = id
    device['state_topic'] = topic + '/sensor/' + id + '/state'
    device['unique_id'] = id
    device['device'] =  {
        "identifiers": id,
        "manufacturer": "Dallas",
        "model": name,
        "name": id,
    }
    return json.dumps(device)

signal.signal(signal.SIGINT, keyboardInterruptHandler)

filename = 'config.ini'
if not os.path.exists(filename):
    print "File {} was not found".format(filename)
    exit(5)

config = configparser.ConfigParser()
config.read('config.ini')

homeassistant = get_config_safe('general', 'homeassistant')
interval = get_config_safe('general', 'interval','30')
broker = get_config_safe('mqtt', 'broker')
port = get_config_safe('mqtt', 'port', '1884')
user = get_config_safe('mqtt', 'user')
password = get_config_safe('mqtt', 'pass')
topic = get_config_safe('mqtt', 'topic')

degree = u"\N{DEGREE SIGN}"

mqtt.Client.connected = False
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
if user != "" and password != "":
    client.username_pw_set(user, password=password)
client.connect(broker)
client.loop_start()

print("Connecting to " + broker)
while not client.connected:
    time.sleep(0.2)

if homeassistant == "true":
    for sensor in W1ThermSensor.get_available_sensors():
        device = device_config(sensor.id, sensor.type_name)
        print("Publishing config for sensor " + sensor.id)
        client.publish("homeassistant/sensor/" + sensor.id + "/temp/config",device)

while True:
    for sensor in W1ThermSensor.get_available_sensors():
        temperature = sensor.get_temperature()
        print("%s %s %.2f%sC" % (sensor.type_name, sensor.id, temperature, degree))
        client.publish(topic + "/sensor/" + sensor.id +'/state', round(temperature,2))
    print("Sleeping for %s seconds" % (interval))
    time.sleep(float(interval))
