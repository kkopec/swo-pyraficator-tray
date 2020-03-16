import json
import re
import requests
from enum import Enum
from core.models import State
from core.config import API_URL


def get_status():
    data = fetch_data()
    return parse_result(data)


def fetch_data():
    try:
        response = requests.get(API_URL)

        if response.status_code == 200:
            return response.json()
        else:
            return None
    except requests.ConnectionError:
        return None


def parse_result(json):
    return State(json) if json is not None else State()
