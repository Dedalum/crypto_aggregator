"""
Config for inputs using dataclasses
"""

from dataclasses import dataclass
from enum import Enum

import inputs.binance


class Client(Enum):
    """
    Client class for the configuration to link between the config file and the
    corresponding input module client to use.
    """

    BINANCE = inputs.binance.Client


@dataclass
class Config:
    """
    Configuration class corresponding to the config file given by the user
    """

    client: Client
    api_key: str
    api_secret: str
