import os
import pytz
from flask import Flask, request
import json

path = os.getcwd()+'/files'
print(path)
app = Flask(__name__)
os.chdir(path)


@app.route('/getData', methods=['GET'])
def get_content():
    return my_json_data

log = 1
@app.route('/mqtt', methods=['POST'])
def post_cpu_usage():
    usage = request.get_data()
    global my_json_data
    z = json.loads(usage.decode('utf8').replace("'", '"'))
    my_json_data.append(z)
    return "success"

my_json_data =[]
app.run(port=5002)

