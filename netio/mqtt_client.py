
"""
MQTT client output classes
"""


import asyncio
from connectors import binance
from model.job import BadJob, Job
import paho.mqtt.client as mqtt

from model.result import Result
from netio.base_output import BaseFormatter, BaseOutput, BaseVerifier

TOPIC_BASE_JOB = "job"


class Client(BaseOutput):
    def __init__(self, host: str, client_id: str):
        super().__init__(host, client_id)
        self.formatter = Formatter()
        self.client = None
        self.producer = None
        self.consumer = None

    def setup(self):
        self._set_client()
        self.client = mqtt.Client()
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message

        self._job_queue = asyncio.Queue()

        self.client.loop_forever()  #TODO code bloquant ?


    async def get_job(self, queue: asyncio.Queue):
        while True:
            try:
                job = self._job_queue.get()

                # push to the core's jobs queue
                queue.put(self._build_job(job))
            
            except BadJob:
                print(f"received job unsupported or wrong: {msg.data}")

            except Exception:
                self.consumer.negative_acknowledge(msg)

    def _set_client(self):
        pass

    def _send(self, data: str):
        self.client.publish(data.encode("utf-8"))

    def _on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        # /job/# -> on recoit des messages de /job, /job/abc, /job/123
        # /job -> on ne recoit que sur /job
        client.subscribe(f"{TOPIC_BASE_JOB}/#")


    def _on_message(self, client, userdata, msg):
        print(msg.topic+" "+str(msg.payload))

        # if messge received on TOPIC_BASE_JOB: job
        if msg.topic.start.startswith(TOPIC_BASE_JOB):
            job = self._build_job(msg.payload)
            self._job_queue.put(job)


    def close_connection(self):
        self.client.close()


class Formatter(BaseFormatter):
    def __init__(self):
        super().__init__()


class Verifier(BaseVerifier):
    def __init__(self):
        super().__init__()


