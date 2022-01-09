"""
Result data model for the resulsts sent from the app to the output
"""

import json


class Result:
    def __init__(self):
        self.accounts = []

    def __str__(self):
        return json.dumps(self.accounts)
