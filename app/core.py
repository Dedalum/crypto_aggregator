"""
Core
"""

import asyncio
import app.config
import connectors.config
import netio.config
from dotenv import dotenv_values
from connectors.base_client import BaseClient
from model.result import Result
from model.job import Job
from netio.base_output import BaseOutput


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
        netio.config.Config(
            client=netio.config.Client[config_dict.get("OUTPUT")],
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


def get_output_client(config: netio.config.Config) -> BaseOutput:
    return config.client.value(config.host, config.client_id)


def run():
    """
    Run the main process
    """
    
    # parse the configuration for the application
    config = get_config()
    
    # create queue for passing the results from the konnektors
    results_queue = asyncio.Queue(maxsize=100)  # 100 results stocked max

    # create the Pulsar client
    netio_client = get_output_client(config.netio)
    netio_client.setup()

    # handle the results received on the result_queue in a new thread
    # resulsts: data coming from the various konnectors and to be sent to Pulsar
    handle_results_queue(netio_client, results_queue)

    # handle the jobs list
    handle_jobs(netio_client)


async def run_job(job: Job, results_queue: asyncio.Queue):

    # run the input module
    konnector = get_client(job.config.inputs)
    # result = konnector.get_result()
    # result = Result()
    # result.accounts = ["First account", "2nd account"]

    await results_queue.put(result)


async def handle_jobs(output_client: BaseOutput):
    while True:
        # receive job from Pulsar: sub /job
        job = await output_client.get_job()
        
        # TODO: add job to list of asyncio tasks 
        # run_job(job)


async def handle_results_queue(output_client: BaseOutput, queue: asyncio.Queue):
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