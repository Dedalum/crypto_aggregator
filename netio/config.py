"""
Config for inputs using dataclasses
"""

from dataclasses import dataclass
from enum import Enum

from netio import pulsar_client, mqtt_client


class Client(Enum):
    """
    Client class for the configuration to link between the config file and the
    corresponding input module client to use.
    """

    PULSAR = pulsar_client.Client
    MQTT = mqtt_client.Client


@dataclass
class Config:
    """
    Configuration class corresponding to the config file given by the user
    """

    client: Client
    host: str
    client_id: str
