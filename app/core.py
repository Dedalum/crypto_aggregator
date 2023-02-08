"""
Core
"""

import asyncio
import app.config
import connectors.config
import netio.config
from dotenv import dotenv_values
from model.job import Job
from netio.base_output import BaseOutput


def get_config(config_file=".env") -> app.config.Config:
    """
    Load the config from the .env file and return a Configuration object.
    """
    config_dict = dotenv_values(config_file)
    config = app.config.Config(
        netio.config.Config(
            client=netio.config.Client[config_dict.get("OUTPUT")],
            host=config_dict.get("HOST"),
            client_id=config_dict.get("CLIENT_ID"),
        ),
    )
    return config

def get_output_client(config: netio.config.Config) -> BaseOutput:
    return config.client.value(config.host, config.client_id)


def run():
    """
    Run the main process
    """
    asyncio.run(assemble_core())
    print("done")
    
async def assemble_core():
    # parse the configuration for the application
    config = get_config()

    # create the Pulsar or MQTT client
    netio_client = get_output_client(config.netio)
    netio_client.setup()
    
    # netio_client_run_task = asyncio.create_task(netio_client.run())

    # create queue for passing the results from the konnektors
    results_queue = asyncio.Queue(maxsize=100)  # 100 results stocked max

    # handle the results received on the result_queue in a new thread
    # results: data coming from the various konnectors and to be sent to Pulsar
    # netio_client_result_processor_task = asyncio.create_task(netio_client.result_processor(results_queue))

    # handle the jobs list
    jobs_queue = asyncio.Queue(maxsize=100)  # 100 results stocked max
    # netio_client_get_job_task = asyncio.create_task(netio_client.get_job(jobs_queue))
    # job_processor_task = asyncio.create_task(job_processor(results_queue, jobs_queue))

    await asyncio.gather(
        netio_client.result_processor(results_queue),
        netio_client.get_job(jobs_queue),
        job_processor(results_queue, jobs_queue),
        netio_client.run(),
    )


    # await asyncio.gather(
    #     netio_client_result_processor_task,
    #     netio_client_get_job_task,
    #     job_processor_task,
    #     netio_client_run_task,
    # )


async def run_job(job: Job, results_queue: asyncio.Queue):

    # run the input module
    result = job.connector.get_result()
    # result = Result()
    # result.accounts = ["First account", "2nd account"]

    await results_queue.put(result)


async def job_processor(results_queue: asyncio.Queue, jobs_queue: asyncio.Queue):
    print("Starting job processor")
    while True:
        job = await jobs_queue.get()
        # TODO: add job to list of asyncio tasks 
        await run_job(job, results_queue)  # TODO maybe possible to put as a oneline ?