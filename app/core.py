"""
Core
"""

import app.config
import inputs.config
import outputs.config
from dotenv import dotenv_values
from inputs.base_client import BaseClient
from model.result import Result
from outputs.base_output import BaseOutput


def get_config(config_file=".env") -> app.config.Config:
    """
    Load the config from the .env file and return a Configuration object.
    """
    config_dict = dotenv_values(config_file)
    config = app.config.Config(
        inputs.config.Config(
            client=inputs.config.Client[config_dict.get("INPUT")],
            api_key=config_dict.get("API_KEY"),
            api_secret=config_dict.get("API_SECRET"),
        ),
        outputs.config.Config(
            client=outputs.config.Client[config_dict.get("OUTPUT")],
            host=config_dict.get("HOST"),
            client_id=config_dict.get("CLIENT_ID"),
        ),
    )
    return config


def get_client(config: inputs.config.Config) -> BaseClient:
    """
    With a given configuration object, builds and return an input Client
    """
    return config.client.value(config.api_key, config.api_secret)


def get_output_client(config: outputs.config.Config) -> BaseOutput:
    return config.client.value(config.host, config.client_id)


def run():
    """
    Run the main process
    """
    # parse the config file
    config = get_config()

    # run the input module
    client = get_client(config.inputs)
    # result = client.get_result()
    result = Result()
    result.accounts = ["First account", "2nd account"]

    # parse the data
    output_client = get_output_client(config.outputs)
    output_client.setup()

    # verify the data
    output_client.verify_result(result)
    data = output_client.serialize_result(result)

    # push the data to the output
    output_client.send_result(data)
    output_client.close_connection()
    # print(result)
