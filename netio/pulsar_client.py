"""
Pulsar client output classes
"""


import asyncio
from connectors import binance
from model.job import BadJob, Job
import pulsar

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
        topic_producer = f"{TOPIC_BASE_JOB}/{self.client_id}/result"
        self._set_producer(topic_producer)

        self.consumer = self.client.subscribe(
            f"{TOPIC_BASE_JOB}", 
            "get-job",  #TODO ?
            properties={
                "consumer-name": f"client-{self.client_id}",
                "consumer-id": f"client-{self.client_id}",
            },
        )

    async def get_job(self, queue: asyncio.Queue):
        while True:
            msg = self.consumer.receive()
            try:
                print("Received message '{}' id='{}'".format(msg.data(), msg.message_id()))

                # Acknowledge successful processing of the message
                self.consumer.acknowledge(msg)

                queue.put(self._build_job(msg.data().decode('utf-8')))
            
            except BadJob:
                print(f"received job unsupported or wrong: {msg.data}")

            except Exception:
                self.consumer.negative_acknowledge(msg)

    def _set_client(self):
        self.client = pulsar.Client(f"pulsar://{self.host}")

    def _set_producer(self, topic: str):
        self.producer = self.client.create_producer(topic)

    def _send(self, data: str):
        self.producer.send(data.encode("utf-8"))

    def close_connection(self):
        self.client.close()


class Formatter(BaseFormatter):
    def __init__(self):
        super().__init__()


class Verifier(BaseVerifier):
    def __init__(self):
        super().__init__()


