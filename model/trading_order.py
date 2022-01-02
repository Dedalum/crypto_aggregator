"""
TradingOrder
"""


class TradingOrder:
    def __init__(self):
        self.label = None
        self.quantity = None
        self.date = None
        self.order_type = None  # Enum
        self.order_side = None  # Enum: BUY, SELL
