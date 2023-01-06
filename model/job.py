"""
Job model
"""

from pydantic import BaseModel
import app


class Job(BaseModel):
    id: int
    config: app.config.Config