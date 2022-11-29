import paho.mqtt.client as mqtt
import requests
import os
import csv
import time
import click as click
import configparser
import json
from flask import Flask
import requests
app = Flask(__name__)

class Generator:
    def __init__(self,source) -> None:
        self.frequency = None
        self.data = None
        self.data_config = None
        self.data_source = source
        self.config = {
            'Default' : {'protocol' : '', 'frequency' : '', 'source' : self.data_source, 'app' : '', 'data':''},
            'Http' : {'url' : '', 'path' : ''},
            'Mqtt' : {'url' : '', 'topic' : '','client' : ''}
        }
        self.run = True

    def load_data_form_csv(self):
        self.data_config = self.config['Default']
        self.data = []
        os.chdir(os.getcwd() + '/' + self.data_config['app'])
        with open(self.data_config['data'], mode='r') as file:
            file = csv.DictReader(file)
            list_rows = []
            for row in file:
                list_rows.append(row)
            self.data = list_rows
        print(f'Processed {len(self.data)} lines.')

    def send_data(self):
        self.frequency = int(self.config['Default']['frequency'])
        if self.config['Default']['protocol'].lower() == 'mqtt':
            self.mqtt_config=self.config['Mqtt']
            print(f'Conected protocol Mqtt varibles: {self.mqtt_config}')
            self.publish_mqtt_message()
        elif self.config['Default']['protocol'].lower() == 'http':
            self.http_config=self.config['Http']
            print(f'Conected protocol Http varibles: {self.http_config}')
            self.send_http_message()

    def send_http_message(self):
        while self.run:
            content = {'data': next(self.data)}
            requests.post(self.http_config['url']+'/'+self.http_config['path'], data=content)
            print("sent: http url:" + self.http_config['url'] + " message:" + f'{content}')
            time.sleep(float(self.frequency))

    def publish_mqtt_message(self):
        client = mqtt.Client(self.mqtt_config['client'])
        client.connect(self.mqtt_config['127.0.0.1'])
        client.subscribe(self.mqtt_config['topic'])
        while self.run:
            content = {'data': next(self.data)}
            client.publish(self.mqtt_config['topic'], content)
            print("sent: mqtt topic:" + self.mqtt_config['topic'] + " message:" + f'{content}')
            time.sleep(float(self.frequency))
    #
    # @self.app.route('<source>/start', methods=['post'])
    # def start(self,source):
    #     self.config = {
    #         'data': {'source': source, 'channel': request.form.get('channel'),
    #                  'frequency': request.form.get('frequency'), 'data':request.form.get('file_name with ext')},
    #         'MQTT': {'broker': request.form.get('broker'), 'port': request.form.get('port'),
    #                  'topic': request.form.get('topic')},
    #         'HTTP': {'host': request.form.get('host'), 'port': request.form.get('port')},
    #     }
    def start(self,dict):
        self.config = {
            'Default' : {'protocol' : '', 'frequency' : '', 'source' : self.data_source, 'app' : '', 'data':''},
            'Http' : {'url' : '', 'path' : ''},
            'Mqtt' : {'url' : '', 'topic' : '','client' : ''}
        }
        self.load_data_form_csv()
        self.send_data()
    def stop(self):
        self.active = False

@app.route('/start', methods=['GET','POST'])
def start():
    config = {
        'data': {'source': requests.form.get('source'), 'protocol': request.form.get('protocol'),
                 'frequency': request.form.get('frequency'),'app':request.form.get('data directory'), 'data':request.form.get('file_name with ext')},
        'Mqtt': {'url': request.form.get('url'), 'topic': request.form.get('topic'),
                 'client': request.form.get('client')},
        'Http': {'host': request.form.get('host'), 'path': request.form.get('path')},
    }
    print("IM here ")
    config = requests.json()
    Generator.start(config)
@app.route('/stop', methods= ['post'])
def stop():
    Generator.stop = False
if __name__ == "__main__":
    app.run(port=5001)
    pass

