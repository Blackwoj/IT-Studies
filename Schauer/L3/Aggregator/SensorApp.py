import paho.mqtt.client as mqtt
import requests
import os
import csv
import time
import click as click
import configparser
import json

@click.command()
@click.option("--config_location",
              default='app4/Air_quality_sensor.ini',
             help='Path with file name to configure app.')
# @click.option("--config_location",
#               default='app5/Humidity_sensor.ini',
#              help='Path with file name to configure app.')

def main(config_location):
    print(f"Current config : {config_location}")
    config = configparser.ConfigParser() # defining file as a config type
    print(os.getcwd())
    os.chdir('..')
    print(os.getcwd())
    # if not os.path.isdir(config_location):
    #     raise Exception("There is configuration file!")
    config.read(config_location)
    print(config.sections()) #checking which sections contain config
    protocol, frequency, dataSource = read_config_file_default(config_location)
    data = get_data_from_csv_file(get_data_folder(config_location),dataSource)
    print('Use protocol: ' + protocol)
    print('Use frequency: ' + frequency)
    print('Use data source: ' + dataSource)
    print(f'Processed {len(data)} lines.')

    if protocol == 'http':
        host_url = read_config_file_protocol_http(config_location)
        while True:
            for row in data:
                send_http_message(host_url, json.dumps(row))
                time.sleep(float(frequency))
    elif protocol =='mqtt':
        mqtt_url, topic, client_ = read_config_protocol_mqtt(config_location)
        client = mqtt.Client(client_)
        client.connect(mqtt_url)
        client.subscribe(topic)
        for row in data:
            publish_mqtt_message(client, topic, json.dumps(row))
            time.sleep(float(frequency))

def read_config_file_default(config_location):
    config = configparser.ConfigParser()
    config.read(config_location)
    return config['DEFAULT']['Protocol'], config['DEFAULT']['Frequency'], config['DEFAULT']['Data']

def read_config_file_protocol_http(config_location):
    config = configparser.ConfigParser()
    os.chdir('..')
    config.read(config_location)
    return config['protocol.http']['Url']+config['protocol.http']['Path']

def read_config_protocol_mqtt(config_location):
    config = configparser.ConfigParser()
    os.chdir('..')
    config.read(config_location)
    return config['protocol.mqtt']['Url'], config['protocol.mqtt']['Topic'], config['protocol.mqtt']['Client']

def get_data_folder(config_location):
    config = configparser.ConfigParser()
    config.read(config_location)
    return config['DEFAULT']['App']

def get_data_from_csv_file(directory,file_name):
    os.chdir(os.getcwd()+'/'+directory)
    with open(file_name, mode = 'r') as file:
        file = csv.DictReader(file)
        list_rows = []
        for row in file:
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