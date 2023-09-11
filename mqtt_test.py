from paho.mqtt import client as mqtt_client
import threading
import json
import time
import random

# number of request-> per thread
NUMBER_OF_REQUEST = 10
# scale -> second
REQUEST_INTERVAL = 1
# number of threads
NUMBER_OF_THREAD = 100
# broker url
broker = '----'
# mqtt port
port = 1883
# mqtt topic
topic = "----"
# thread sleep -> second
THREARD_SLEEP = 0


class mqttStruct(threading.Thread):
    def __init__(self, broker, port, topic, NUMBER_OF_REQUEST, REQUEST_INTERVAL, deviceId):
        super(mqttStruct, self).__init__()
        self.broker = broker
        self.port = port
        self.topic = topic
        self.json_temp = {
            "1": 17,
            "2": "value",
            "3": random.randint(1, 90),
            "4": 5
        }
        self.NUMBER_OF_REQUEST = NUMBER_OF_REQUEST
        self.REQUEST_INTERVAL = REQUEST_INTERVAL
        self.deviceId = deviceId

    def run(self):
        client = mqtt_client.Client()
        client.connect(self.broker, self.port)
        json_data = json.dumps(self.json_temp)
        for i in range(self.NUMBER_OF_REQUEST):
            time.sleep(self.REQUEST_INTERVAL)
            client.publish(topic, json_data)
            print(f'id {self.deviceId} send {json_data}')
        client.disconnect()


threads = []
for i in range(NUMBER_OF_THREAD):
    t = mqttStruct(broker=broker,
                   port=port,
                   topic=topic,
                   NUMBER_OF_REQUEST=NUMBER_OF_REQUEST,
                   REQUEST_INTERVAL=REQUEST_INTERVAL,
                   deviceId=i)
    threads.append(t)
for i in range(NUMBER_OF_THREAD):
    time.sleep(THREARD_SLEEP)
    threads.pop().start()
    print(f'thread {i} started')
