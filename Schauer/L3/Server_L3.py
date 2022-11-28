import os
from flask import Flask, request
import json

app = Flask(__name__)

@app.route('/home',methods=['GET'])
def base_page():
    return "water-quality humidity airQuality  location   temperature"


@app.route('/airQuality', methods=['POST','GET'])
def post_data():
    global my_json_data
    if request.method == 'POST':
        usage = request.get_data()
        z = json.loads(usage.decode('utf8').replace("'", '"'))
        my_json_data.append(z)
        return "Data Transfer Success"
    return my_json_data

@app.route('/mqtt', methods=['POST','GET'])
def post_data_mqtt():
    global my_json_data
    if request.method == 'POST':
        usage = request.get_data()
        z = json.loads(usage.decode('utf8').replace("'", '"'))
        my_json_data.append(z)
        return "Data Transfer Success"
    return my_json_data

my_json_data =[]
app.run(port=8080)

