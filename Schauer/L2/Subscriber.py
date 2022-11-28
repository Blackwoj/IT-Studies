import paho.mqtt.client as mqtt
import requests
log = 0
def on_message(clt, userdata, message):
    global log
    log +=1
    requests.post('http://localhost:8080/mqtt', json = {"id": [log], "received_cpu_usage": str(message.payload.decode('utf-8'))})

mqtt_topics = ["WaterQualityStatus","HumidityStatus","TemperatureStatus","LocationStatus","AirQuailityStatus"]
client = mqtt.Client("P2")
client.connect("127.0.0.1")
client.on_connect = lambda a, b, c, d: client.subscribe(mqtt_topics[1])


client.on_message = on_message
client.loop_forever()
