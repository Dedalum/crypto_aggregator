"""
Investment model
"""


class Investment:
    def __init__(self):
        self.code = None  # isin
        self.label = None
        self.quantity = 0
        self.amount = 0
        self.date = None
