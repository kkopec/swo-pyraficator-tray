import json
import os

API_URL = 'https://hackaton.azurewebsites.net/status'
USERCONFIG_PATH = 'userconfig.json'

class Config():
    def __init__(self):
        self.REFRESH_INTERVAL = 10000
        self.NOTIFICATION_TIME = 5000
        self.NOTIFICATIONS_STATUSES = ['Failure']
        self.NOTIFICATIONS_REGEX = None

        if not os.path.exists(USERCONFIG_PATH):
            return

        with open(USERCONFIG_PATH) as json_file:
            data = json.load(json_file)
            self.REFRESH_INTERVAL = data['refreshInterval']
            self.NOTIFICATION_TIME = data['notificationTime']
            self.NOTIFICATIONS_STATUSES = data['notificationStatuses']

