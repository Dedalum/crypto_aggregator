"""
Binance API client
"""

from typing import List

from binance.spot import Spot
from model.account import Account
from model.investment import Investment
from model.result import Result
from model.trading_order import TradingOrder

from .base_connector import BaseConnector, BaseParser


class Client(BaseConnector):
    """
    Client class for Binance that connects to the Binance API and returns the
    required data.
    """

    def __init__(self, api_key: str, api_secret: str):
        super().__init__(api_key, api_secret)
        self.spot = Spot(key=self.api_key, secret=self.api_secret)
        self.parser = Parser()

    def _get_account_snapshot(self) -> dict:
        data = {}
        data["account_snapshot"] = self._check_response(
            self.spot.account_snapshot("SPOT")
        )

        return data

    def _get_account_orders(self, investments) -> dict:
        data = []
        for asset in investments:
            data.append(self._check_response(self.spot.get_orders(asset.label)))

        return data

    def get_result(self):
        investments = self.get_investments(self._get_account_snapshot())
        trading_orders = self.get_orders(self._get_account_orders(investments))

        account = self.parser.build_accounts({})
        account.investments = investments
        account.trading_orders = trading_orders

        result = Result()
        result.accounts = [account]
        return result

    def get_accounts(self, data: dict) -> dict:
        return self.parser.build_accounts(data)

    def get_orders(self, data: dict) -> dict:
        return self.parser.build_orders(data)

    def get_investments(self, data: dict) -> dict:
        return self.parser.build_investments(data)

    def _check_response(self, response: dict) -> dict:
        if response.get("code") != "200":  # > 299 and < 200
            print("Error querying data: {}".format(response.get("msg")))
            return {}
        return response


class Parser(BaseParser):
    """
    Data parser for the Binance API
    """

    def build_accounts(self, data: dict) -> Account:
        # TODO: method name is plural but we only return 1 Account
        account = Account()

        return account

    def build_orders(self, data: dict) -> List[TradingOrder]:
        pass

    def build_investments(self, data: dict) -> List[Investment]:
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
