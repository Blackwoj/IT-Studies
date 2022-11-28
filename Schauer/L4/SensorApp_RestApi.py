import configparser
import csv
import json
import multiprocessing
import os
import threading
import time

import click as click
import paho.mqtt.client as mqtt
import requests
from flask import Flask, request

app = Flask(__name__)
process = []
configutation_sensor = {}
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
@app.route('/config', methods=['POST'])
def post_config():
    process[0].kill()
    req = str(request.get_data(), 'utf-8')
    loads = json.loads(req)
    turn_on = True
    actuator = False
    for key in loads.keys():
        configutation_sensor[key] = loads[key]
        if key == "status":
            if loads[key] == "off":
                turn_on = False
        elif key == "actuator":
            if loads[key] == "on":
                actuator = True
    if turn_on and not actuator:
        process_send_sensor_info = multiprocessing.Process(target=send_sensor_info,
                                                           args=(configutation_sensor["frequency"],
                                                                 configutation_sensor["protocol"],
                                                                 configutation_sensor["url"],
                                                                 configutation_sensor["topic"]),
                                                           name="send_sensor_info")
        process_send_sensor_info.start()
        process[0] = process_send_sensor_info
    elif actuator:
        process_send_sensor_info = multiprocessing.Process(target=send_sensor_info_grouse_values,
                                                           args=(configutation_sensor["frequency"],
                                                                 configutation_sensor["protocol"],
                                                                 configutation_sensor["url"],
                                                                 configutation_sensor["topic"]),
                                                           name="send_sensor_info")
        process_send_sensor_info.start()
        process[0] = process_send_sensor_info
    return "success"


@app.route('/config', methods=['GET'])
def get_config():
    return json.dumps(configutation_sensor)

@click.command()
@click.option("--config_location",
              default='app4/Air_quality_sensor.ini',
             help='Path with file name to configure app.')

def main(config_location):
    print('Configuration location: ' + config_location)

    config = configparser.ConfigParser()
    config.read(config_location)
    print(os.getcwd())
    print(config.sections())

    protocol_, frequency_, dataSource_ = read_config_file_default(config_location)
    config_external_port_ = get_external_settings_config(config_location)
    url_mqtt_, topic_mqtt_, client_ = get_mqtt_config(config_location)
    http_url_ = get_http_url(config_location)
    rows_ = get_data_from_csv_file(get_app_folder(config_location) + "/" + dataSource_)

    print('Use external port for config: ' + config_external_port_)
    print('Use protocol: ' + protocol_)
    print('Use frequency: ' + frequency_)
    print('Use data source: ' + dataSource_)
    print(f'Processed {len(rows_)} lines.')
    configutation_sensor["protocol"] = protocol_
    configutation_sensor["frequency"] = frequency_
    configutation_sensor["dataSource"] = dataSource_
    configutation_sensor["config_location"] = config_location
    if protocol_ == "http":
        configutation_sensor["url"] = http_url_
    else:
        configutation_sensor["url"] = url_mqtt_
    configutation_sensor["topic"] = topic_mqtt_
    configutation_sensor["status"] = "on"

    process_send_sensor_info = multiprocessing.Process(target=send_sensor_info,
                                                       args=(frequency_, protocol_,
                                                             configutation_sensor["url"], topic_mqtt_),
                                                       name="send_sensor_info")
    process_send_sensor_info.start()
    process.append(process_send_sensor_info)
    app.run(port=get_external_settings_config(config_location))


def send_sensor_info(frequency_, protocol_, url, topic):
    config_location = configutation_sensor["config_location"]
    rows_ = get_data_from_csv_file(get_app_folder(config_location) + "/" + configutation_sensor["dataSource"])
    if protocol_ == 'http':
        url_ = url
        while True:
            for row in rows_:
                send_http_message(url_, json.dumps(row))
                time.sleep(float(frequency_))
    elif protocol_ == 'mqtt':
        print('Use protocol: mqtt')
        url_, topic_, client_ = get_mqtt_config(config_location)
        url_ = url
        topic_ = topic
        client = mqtt.Client(client_)
        client.connect(url_)
        client.subscribe(topic_)
        while True:
            for row in rows_:
                publish_mqtt_message(client, topic_, json.dumps(row))
                time.sleep(float(frequency_))


def send_sensor_info_grouse_values(frequency_, protocol_, url_, topic_):
    config_location = configutation_sensor["config_location"]
    rows_ = get_data_from_csv_file(get_app_folder(config_location) + "/" + configutation_sensor["dataSource"])
    if protocol_ == 'http':
        while True:
            for row in rows_:
                send_http_message(url_, json.dumps(row))
                time.sleep(float(frequency_))
    elif protocol_ == 'mqtt':
        print('Use protocol: mqtt')
        url_from_file_, topic_from_file_, client_ = get_mqtt_config(config_location)
        client = mqtt.Client(client_)
        client.connect(url_)
        client.subscribe(topic_)
        row = rows_[0]
        row["outside/inside"] = "inside"
        while True:
            row["temp"] = str(float(row["temp"]) + 0.5)
            publish_mqtt_message(client, topic_, json.dumps(row))
            time.sleep(float(frequency_))


def read_config_file_default(config_location):
    config = configparser.ConfigParser()
    config.read(config_location)
    return config['DEFAULT']['Protocol'], config['DEFAULT']['Frequency'], config['DEFAULT']['Data']


def get_http_url(config_location):
    config = configparser.ConfigParser()
    config.read(config_location)
    return config['protocol.http']['Url'] + config['protocol.http']['Path']


def get_app_folder(config_location):
    config = configparser.ConfigParser()
    config.read(config_location)
    return config['DEFAULT']['App']


def get_mqtt_config(config_location):
    config = configparser.ConfigParser()
    config.read(config_location)
    return config['protocol.mqtt']['Url'], config['protocol.mqtt']['Topic'], config['protocol.mqtt']['Client']


def get_external_settings_config(config_location):
    config = configparser.ConfigParser()
    config.read(config_location)
    return config['external.properties']['Port']


def get_data_from_csv_file(file_name):
    with open(file_name, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        list_rows = []
        for row in csv_reader:
            list_rows.append(row)
        return list_rows


def send_http_message(url, json_message):
    requests.post(url, data=json_message, headers={'content-type': 'application/json'})
    print("sent: http url:" + url + " message:" + json_message)


def publish_mqtt_message(client, topic, json_message):
    client.publish(topic, json_message)
    print("sent: mqtt topic:" + topic + " message:" + json_message)


if __name__ == '__main__':
    main()