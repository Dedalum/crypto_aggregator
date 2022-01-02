"""
Core
"""

from dotenv import dotenv_values
from inputs.base_client import BaseClient
from inputs.config import Client as ClientEnum
from inputs.config import Configuration


def get_config(config_file=".env") -> Configuration:
    """
    Load the config from the .env file and return a Configuration object.
    """
    config_dict = dotenv_values(config_file)
    config = Configuration(
        client=ClientEnum[config_dict.get("INPUT")],
        api_key=config_dict.get("API_KEY"),
        api_secret=config_dict.get("API_SECRET"),
    )
    return config


def get_client(config: Configuration) -> BaseClient:
    """
    With a given configuration object, builds and return an input Client
    """
    return config.client.value(config.api_key, config.api_secret)


def run():
    """
    Run the main process
    """
    # parse the config file
    config = get_config()

    # run the input module
    client = get_client(config)
    data = client.get_data()
    # parse the data

    # verify the data

    # push the data to the output
