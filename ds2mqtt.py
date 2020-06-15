#!/usr/bin/env python

import os.path
import json
import time
import configparser
import signal
import logging
from w1thermsensor import W1ThermSensor
import paho.mqtt.client as mqtt

degree = u"\N{DEGREE SIGN}"

def keyboardInterruptHandler(signal, frame):
    logger.info("KeyboardInterrupt (ID: {}), exiting...".format(signal))
    exit(0)

def setup_logging():
    global logger
    logger = logging.getLogger(os.path.basename(__file__))
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    fh = logging.FileHandler(os.path.basename(__file__) + '.log', mode='a', encoding=None, delay=False)
    fh.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

    ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    logger.addHandler(ch)
    logger.addHandler(fh)

#logger.debug('debug message')
#logger.info('info message')
#logger.warn('warn message')
#logger.error('error message')
#logger.critical('critical message')

def get_config_safe(section, option, default=None):
    try:
        return config.get(section, option)
    except (configparser.NoOptionError, configparser.NoSectionError, ValueError):
        logger.info('Could not find section [%s] option "%s"' % (section, option))
        return default

def on_connect(client, userdata, flags, rc):
    if int(str(rc)) == 0:
        logger.info("Connection successful")
        client.connected = True
    elif int(str(rc)) == 1:
        logger.warn("Connection refused - incorrect protocol version")
    elif int(str(rc)) == 2:
        logger.warn("Connection refused - invalid client identifier")
    elif int(str(rc)) == 3:
        logger.warn("Connection refused - server unavailable")
    elif int(str(rc)) == 4:
        logger.warn("Connection refused - bad username or password")
    elif int(str(rc)) == 5:
        logger.warn("Connection refused - not authorised")

def on_disconnect(client, userdata, rc):
    if rc != 0:
        logger.error("Unexpected disconnection. RC = " + str(rc))

def on_publish(client, userdata, mid):
    logger.info("Message " +str(mid)+ " published.")
                    
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

def connect_to_broker(host):
    global client
    logger.info("Connecting to " + broker)
    mqtt.Client.connected = False
    client = mqtt.Client()
    client.on_connect = on_connect
    #client.on_message = on_message
    #client.on_publish = on_publish
    if username != "" and password != "":
        client.username_pw_set(username, password=password)
    client.connect(host)
    client.loop_start()
    while not client.connected:
        time.sleep(0.2)

def get_config():
    global config, homeassistant, interval, broker, port, username, password, topic
    config = configparser.ConfigParser()

    try:
        config.read('config.ini')
    except configparser.ParsingError as e:
        exit(5)
    except configparser.ParsingError as e:
        exit(5)

    homeassistant = get_config_safe('general', 'homeassistant')
    interval = get_config_safe('general', 'interval','30')
    broker = get_config_safe('mqtt', 'broker')
    port = get_config_safe('mqtt', 'port', '1884')
    username = get_config_safe('mqtt', 'username')
    password = get_config_safe('mqtt', 'password')
    topic = get_config_safe('mqtt', 'topic')

def get_sensors():
    get_sensors = W1ThermSensor.get_available_sensors()
    logger.info("Found %s sensors" % (len(get_sensors)))
    return get_sensors

def publish_config(sensors):
    if homeassistant == "true":
        for sensor in sensors:
            device_json = device_config(sensor.id, sensor.type_name)
            logger.info("Publishing config for sensor " + sensor.id)
            client.publish("homeassistant/sensor/" + sensor.id + "/temp/config",device_json)

def publish_sensors(sensors):
    for sensor in sensors:
        temperature = sensor.get_temperature()
        logger.info("%s %s %.2f%sC" % (sensor.type_name, sensor.id, temperature, degree))
        client.publish(topic + "/sensor/" + sensor.id +'/state', round(temperature,2))
    logger.info("Sleeping for %s seconds" % (interval))
    time.sleep(float(interval))
    

def main():
    signal.signal(signal.SIGINT, keyboardInterruptHandler)
    setup_logging()
    get_config()
    connect_to_broker(broker)
    sensors = get_sensors()
    publish_config(sensors)
    while True:
        publish_sensors(sensors)

if __name__ == "__main__":
    main()
