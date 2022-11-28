import psutil
import paho.mqtt.client as mqtt
import requests
import time


def cpu_change():
    global base_cpu_usage
    ac_cpu_usage = psutil.cpu_percent()
    if base_cpu_usage - ac_cpu_usage > 5 or base_cpu_usage - ac_cpu_usage < -5:
        base_cpu_usage = ac_cpu_usage
        print(base_cpu_usage)
        client.publish("cpu_usage", base_cpu_usage)
    return

base_cpu_usage = psutil.cpu_percent()
client = mqtt.Client("P1")
client.connect("127.0.0.1")
client.subscribe("cpu_usage")
while True:
    cpu_change()
    time.sleep(5)

