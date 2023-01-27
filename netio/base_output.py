"""Base output class"""


import asyncio
import re
from model.job import BadJob, Job

from connectors import binance

from model.result import Result


class BaseOutput:
    def __init__(self, host: str, client_id: str):
        self.client_id = client_id
        self.formatter = BaseFormatter()
        self.verifier = BaseVerifier()
        self.host = self._parse_host(host)
        # self.queue = queue  # TODO: use queues as a pipeline between inputs and output

    def send_result(self, serialized: str):
        print("Sending result to Pulsar: {}".format(serialized))
        self._send(serialized)

    def verify_result(self, data: Result) -> Result:
        # check data
        return self.verifier.run(data)

    def serialize_result(self, data: Result) -> str:
        # format
        serialized = self.formatter.run(data)
        return serialized

    async def result_processor(self, queue: asyncio.Queue):
        while True:
            try:
                result = await queue.get()

                # verify the data
                self.verify_result(result)
                data = self.serialize_result(result)

                # push the data to the output
                self.send_result(data)
                # self.close_connection()
                # print(result)
            except asyncio.QueueEmpty:
                print("queue is empty")
            except Exception as e:
                print(f"err: {e}")
            
            # TODO: handle exit
            finally:
                self.close_connection()

    def setup(self):
        pass

    async def get_job(self):
        pass

    def _build_job(job_data: dict) -> Job:
        if job_data["connector"] == "binance":
            connector_class = binance.client
        else:
            print(f'unsupported connector {job_data["connector"]}')
            raise BadJob

        connector = connector_class(
            job_data["api_key"],
            job_data["api_secret"],
        )
  
        return Job(job_data["id"], connector)
        
    def _send(self, data: str):
        pass

    @staticmethod
    def _parse_host(host) -> str:
        try:
            return re.search(r"(\w+):(\d+)", host).group(0)
        except (TypeError, AttributeError, IndexError) as exc:
            raise ConfigurationError(exc)

        return None
        


class BaseFormatter:
    def __init__(self):
        pass

    def run(self, result: Result) -> Result:
        return str(result)


class BaseVerifier:
    def __init__(self):
        pass

    def run(self, result: Result) -> Result:
        return result


class ConfigurationError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = "Output configuration error: {}"
