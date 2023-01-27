"""
Config for inputs using dataclasses
"""

from dataclasses import dataclass
from enum import Enum

import netio.config


@dataclass
class Config:
    """
    Configuration class corresponding to the config file given by the user
    """
    netio: netio.config.Config
