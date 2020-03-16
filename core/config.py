import json
import os

API_URL = 'https://hackaton.azurewebsites.net/status'
USERCONFIG_PATH = 'userconfig.json'

class Config():
    def __init__(self):
        self.refreshInterval = 10000
        self.notificationTime = 5000
        self.notificationStatuses = ['Failure']
        self.notificationRegex = None

        if not os.path.exists(USERCONFIG_PATH):
            return

        with open(USERCONFIG_PATH) as json_file:
            properties = json.load(json_file)
            [setattr(self, prop, val) for prop, val in properties.items()]
