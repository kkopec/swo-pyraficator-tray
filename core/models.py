import re
from enum import Enum


class Status(Enum):
    Failure = "Failure"
    InProgress = "In Progress"
    Success = "Success"
    Unknown = "Unknown"

    def __str__(self):
        return self.value

    def __eq__(self, other):
        return self.name == other


class StatusItem:
    def __init__(self, item):
        self.id = self.extract_id(item['details'])
        self.name = self.extract_name(item['details'])
        self.details = item['details']
        self.link = item['link']

    def extract_id(self, text):
        return re.search(r"((?<=with ID )\d+|SEQ)", text).group()

    def extract_name(self, text):
        return re.search(r"(.+(?=with ID \d+)|C45 SEQ)", text).group()

    def __str__(self):
        return f"{self.id} | {self.name}"


INIT_STATE = {
    "status": "Unknown",
    "errorItems": None,
    "inProgressItems": None,
    "successItems": None,
}

class State:
    def __init__(self, item = INIT_STATE):
        self.status = item['status']
        self.success = self.parse_items(item['successItems'])
        self.in_progress = self.parse_items(item['inProgressItems'])
        self.error = self.parse_items(item['errorItems'])
        self.observedChanged = False


    def parse_items(self, items):
        status_items = [StatusItem(i) for i in items] if items is not None else []
        return dict([(item.id, item) for item in status_items])
