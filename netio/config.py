"""
Config for inputs using dataclasses
"""

from dataclasses import dataclass
from enum import Enum

import outputs.pulsar_client


class Client(Enum):
    """
    Client class for the configuration to link between the config file and the
    corresponding input module client to use.
    """

    PULSAR = outputs.pulsar_client.Client


@dataclass
class Config:
    """
    Configuration class corresponding to the config file given by the user
    """

    client: Client
    host: str
    client_id: str
