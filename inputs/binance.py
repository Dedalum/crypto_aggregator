"""
Binance API client
"""

from typing import List

from binance.spot import Spot
from model.account import Account
from model.investment import Investment

from .base_client import BaseClient


class Client(BaseClient):
    """
    Client class for Binance that connects to the Binance API and returns the
    required data.
    """

    def __init__(self, api_key: str, api_secret: str):
        super().__init__(api_key, api_secret)
        self.spot = Spot(key=self.api_key, secret=self.api_secret)

    def get_data(self) -> dict:
        data = {}
        data["account_snapshot"] = self.spot.account_snapshot("SPOT")
        return data


class Parser:
    """
    Data parser for the Binance API
    """

    def get_account(self, data: dict) -> List[Account]:
        account = Account()

        return [account]

    def get_investments(self, data: dict) -> List[Investment]:
        investments = []
        invs_data = data.get("snapshotVos")[0]

        date = invs_data.get("update_time")
        for inv_data in invs_data.get("data").get("balances"):
            if inv_data.get("free") == "0":
                print("No free coin, skipping")
                continue

            investment = Investment()
            investment.label = inv_data.get("asset")
            # "locked" coins not included
            investment.quantity = float(inv_data.get("free"))
            investment.date = date

            investments.append(investment)

        return investments
