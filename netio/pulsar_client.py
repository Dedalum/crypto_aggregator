"""
Pulsar client output classes
"""


import pulsar

from model.result import Result
from netio.base_output import BaseFormatter, BaseOutput, BaseVerifier


class Client(BaseOutput):
    def __init__(self, host: str, client_id: str):
        super().__init__(host, client_id)
        self.formatter = Formatter()
        self.client = None
        self.producer = None

    def setup(self):
        self._set_client()
        topic_producer = "output-{}".format(self.client_id)
        self._set_producer(topic_producer)

    def serialize_result(self, data: Result) -> str:
        # format
        serialized = self.formatter.run(data)
        return serialized

    def send_result(self, serialized: str):
        print("Sending result to Pulsar: {}".format(serialized))
        self._send(serialized)

    def _set_client(self):
        self.client = pulsar.Client("pulsar://{}".format(self.host))

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
