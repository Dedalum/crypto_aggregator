import sys
import json

import paho.mqtt.client as mqtt
from models.job import Job


class Client:
    def __init__(self, client_id, topic):
        self.client_id = client_id
        self.base_topic = topic
        self.mqtt_client = mqtt.Client(client_id=client_id)
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))

    def on_message(self, client, userdata, msg):
        print(msg.topic + " " + str(msg.payload))
        
    def subscribe(self, topic):
        self.mqtt_client.subscribe(f"{topic}/#")


def main():
    if len(sys.argv) != 2:
        print("Missing args: cmd <topic>")
        return

    topic = sys.argv[1]

    client = Client("worker-1", topic)
    client.mqtt_client.connect("127.0.0.1", 1883, 60)
    client.subscribe(topic)
    client.mqtt_client.loop_forever()


if __name__ == "__main__":
    main()
