"""
Account tests
"""

import pytest
from inputs.binance import Parser
from model.account import Account


class TestBinance:
    def test_get_investments(self, account_snapshot):
        parser = Parser()
        investments = parser.get_investments(account_snapshot)

        assert investments[0].label == "BTC"
        assert investments[1].label == "ETH"
        assert investments[2].label == "EUR"


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
