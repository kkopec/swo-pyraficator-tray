import json
import re
import requests
from enum import Enum
from config import API_URL

class PycStatus(Enum):
    SUCCESS = 'Success',
    IN_PROGRESS = 'In Progress',
    FAILURE = 'Failure'

    def __eq__(self, other):
        val = self.value
        return val == other

def get_status():
    response = requests.get(API_URL)

    if response.status_code == 200:
        return response.json()
    else:
        print('error')
        # TODO: add error handling

