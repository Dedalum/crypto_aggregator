"""Base output class"""


import re

from model.result import Result


class BaseOutput:
    def __init__(self, host: str, client_id: str):
        self.client_id = client_id
        self.formatter = BaseFormatter()
        self.verifier = BaseVerifier()
        self.host = self._parse_host(host)
        # self.queue = queue  # TODO: use queues as a pipeline between inputs and output

    def send_result(self, serialized: str):
        pass

    def verify_result(self, data: Result) -> Result:
        # check data
        return self.verifier.run(data)

    def setup(self):
        pass

    async def get_job(self):
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
