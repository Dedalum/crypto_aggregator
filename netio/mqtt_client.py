
"""
MQTT client output classes
"""


import asyncio
from connectors import binance
from model.job import BadJob, Job
import paho.mqtt.client as mqtt

from model.result import Result
from netio.base_output import BaseFormatter, BaseOutput, BaseVerifier

TOPIC_BASE_JOB = "/job"


class Client(BaseOutput):
    def __init__(self, host: str, client_id: str):
        super().__init__(host, client_id)
        self.formatter = Formatter()
        self.client = None

    def setup(self):
        self.client = mqtt.Client(client_id=self.client_id)
        self.client.connect(self.host.split(":")[0], int(self.host.split(":")[1]), 60)
        self.client.on_connect = self._on_connect
        self._job_queue = asyncio.Queue()
        self.client.on_message = self._on_message

    async def run(self):
        print("Running MQTT client")
        self.client.loop_start()

    async def get_job(self, queue: asyncio.Queue):
        print("MQTT client getting jobs")
        while True:
            try:
                print(f"len job queue 2--: {self._job_queue.qsize()}")
                job = await self._job_queue.get()
                print(f"received job: {job}")

                # push to the core's jobs queue
                await queue.put(self._build_job(job))
            
            except BadJob:
                print(f"received job unsupported or wrong: {msg.data}")

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
        if msg.topic.startswith(TOPIC_BASE_JOB):  # TODO: check hierarchy topics
            job = self._build_job(msg.payload)
            try:
                print(f"pushing job: {job}")
                self._job_queue.put_nowait(job)
                print(f"len job queue: {self._job_queue.qsize()}")
            except BadJob as e:
                print(f"err: bad job {e}")


    def close_connection(self):
        self.client.close()


class Formatter(BaseFormatter):
    def __init__(self):
        super().__init__()


class Verifier(BaseVerifier):
    def __init__(self):
        super().__init__()


