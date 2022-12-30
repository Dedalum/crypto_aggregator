"""
Core
"""

import asyncio
import app.config
import connectors.config
import rx.config
from dotenv import dotenv_values
from connectors.base_client import BaseClient
from model.result import Result
from model.job import Job
from rx.base_output import BaseOutput


def get_config(config_file=".env") -> app.config.Config:
    """
    Load the config from the .env file and return a Configuration object.
    """
    config_dict = dotenv_values(config_file)
    config = app.config.Config(
        connectors.config.Config(
            client=connectors.config.Client[config_dict.get("INPUT")],
            api_key=config_dict.get("API_KEY"),
            api_secret=config_dict.get("API_SECRET"),
        ),
        rx.config.Config(
            client=rx.config.Client[config_dict.get("OUTPUT")],
            host=config_dict.get("HOST"),
            client_id=config_dict.get("CLIENT_ID"),
        ),
    )
    return config


def get_client(config: connectors.config.Config) -> BaseClient:
    """
    With a given configuration object, builds and return an input Client
    """
    return config.client.value(config.api_key, config.api_secret)


def get_output_client(config: rx.config.Config) -> BaseOutput:
    return config.client.value(config.host, config.client_id)


def run():
    """
    Run the main process
    """
    
    # parse the config file
    config = get_config()
    
    queue = asyncio.Queue(maxsize=100)  # 100 results stocked max

    # parse the data
    output_client = get_output_client(config.rx)
    output_client.setup()

    handle_queue(output_client, queue)



async def run_job(job: Job, queue: asyncio.Queue):

    # run the input module
    client = get_client(job.config.inputs)
    # result = client.get_result()
    result = Result()
    result.accounts = ["First account", "2nd account"]

    await queue.put(result)


async def handle_jobs(output_client: BaseOutput):
    while True:
        job = await output_client.get_job()
        
        # TODO: add job to list of asyncio tasks 
        # run_job(job)


async def handle_queue(output_client: BaseOutput, queue: asyncio.Queue):
    while True:
        try:
            result = await queue.get()

            # verify the data
            output_client.verify_result(result)
            data = output_client.serialize_result(result)

            # push the data to the output
            output_client.send_result(data)
            output_client.close_connection()
            # print(result)
        except asyncio.QueueEmpty:
            print("queue is empty")
        except Exception as e:
            print(f"{e}")