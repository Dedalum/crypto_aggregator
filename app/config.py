"""
Config for inputs using dataclasses
"""

from dataclasses import dataclass
from enum import Enum

import inputs.config
import outputs.config


@dataclass
class Config:
    """
    Configuration class corresponding to the config file given by the user
    """

    inputs: inputs.config.Config
    outputs: outputs.config.Config
