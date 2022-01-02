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
        self.parser = BaseParser()

    def get_result(self):
        pass

    def get_accounts(self):
        pass


class BaseParser:
    """
    BaseParser
    """

    def build_accounts(self, data: dict) -> List[Account]
        pass

    def build_investments(self, data: dict) -> List[Investments]:
        pass

    def build_trading_orders(self, data: dict) -> List[TradingOrders]:
        pass
