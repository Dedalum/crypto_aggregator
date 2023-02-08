"""
Job model
"""

from connectors.base_connector import BaseConnector
from pydantic import BaseModel


class Job(BaseModel):
    id: int
    connector: BaseConnector

    class Config:
        arbitrary_types_allowed = True


class BadJob(Exception):
    pass