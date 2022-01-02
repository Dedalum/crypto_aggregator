"""
Account tests
"""

import pytest
from inputs.binance import Parser
from model.account import Account


class TestBinanceParser:
    def test_get_investments(self, account_snapshot):
        parser = Parser()
        investments = parser.get_investments(account_snapshot)

        assert investments[0].label == "BTC"
        assert investments[1].label == "ETH"
        assert investments[2].label == "EUR"
        # TODO TO BE CONTINUED

    def test_get_trading_orders(self, account_orders):
        parser = Parser
        trading_orders = parser.get_trading_orders(account_orders)

        assert trading_orders[0].label == "LTCBTC"
        assert trading_orders[0].id == 1
        assert trading_orders[0].order_side == "BUY"  # TradingOrderSide.BUY


@pytest.fixture
def account_snapshot():
    """
    https://github.com/binance/binance-connector-python/blob/master/examples/spot/wallet/account_snapshot.py
    """
    return {
        "code": 200,
        "msg": "",
        "snapshotVos": [
            {
                "type": "spot",
                "updateTime": 1640476799000,
                "data": {
                    "totalAssetOfBtc": "10.0",
                    "balances": [
                        {"asset": "BNB", "free": "0", "locked": "0"},
                        {"asset": "BTC", "free": "9", "locked": "0"},
                        {"asset": "ETH", "free": "15", "locked": "0"},
                        {"asset": "EUR", "free": "1000", "locked": "0"},
                        {"asset": "USDT", "free": "0", "locked": "0"},
                    ],
                },
            }
        ],
    }


@pytest.fixture
def account_orders():
    """
    https://binance-docs.github.io/apidocs/spot/en/#current-open-orders-user_data
    """
    return [
        {
            "symbol": "LTCBTC",
            "orderId": 1,
            "orderListId": -1,  # Unless OCO, the value will always be -1
            "clientOrderId": "myOrder1",
            "price": "0.1",
            "origQty": "1.0",
            "executedQty": "0.0",
            "cummulativeQuoteQty": "0.0",
            "status": "NEW",
            "timeInForce": "GTC",
            "type": "LIMIT",
            "side": "BUY",
            "stopPrice": "0.0",
            "icebergQty": "0.0",
            "time": 1499827319559,
            "updateTime": 1499827319559,
            "isWorking": True,
            "origQuoteOrderQty": "0.000000",
        }
    ]
