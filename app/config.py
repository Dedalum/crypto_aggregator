"""
Config for inputs using dataclasses
"""

from dataclasses import dataclass
from enum import Enum

import connectors.config
import rx.config


@dataclass
class Config:
    """
    Configuration class corresponding to the config file given by the user
    """

    inputs: connectors.config.Config
    rx: rx.config.Config
