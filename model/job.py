"""
Job model
"""

from connectors.base_connector import BaseConnector
from pydantic import BaseModel
import app


class Job(BaseModel):
    id: int
    connector: BaseConnector


class BadJob(Exception):
    pass