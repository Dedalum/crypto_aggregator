"""
Base class Client
"""


class BaseClient:
    """
    BaseClient to serve as the base model for every input module Clients
    """
    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret

    def get_data(self):
        pass
