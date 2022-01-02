"""
Account model
"""


class Account:
    def __init__(self):
        self.id = None
        self.label = None
        self.amount = 0
        self.investments = []
        self.trading_orders = []

    def __str__(self):
        return "{} - {}".format(self.id, self.label)
