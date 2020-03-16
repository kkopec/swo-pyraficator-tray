import os
import re
import sys
from enum import Enum
from functools import partial
from PyQt5 import QtCore, QtGui, QtWidgets
from core import API_URL, Config, get_status, Status, StatusItem, State

class Icon(Enum):
    Failure = "red"
    InProgress = "yellow"
    Success = "green"
    Unknown = "unknown"

    def __str__(self):
        return self.value


get_menu_name = lambda status: f"Status: {Status[status]}"

have_same_items = lambda d1, d2: d1.keys() == d2.keys()

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class SystemTrayIcon(QtWidgets.QSystemTrayIcon):

    def __init__(self, config, parent=None):
        QtWidgets.QSystemTrayIcon.__init__(self, parent)
        self.config = config
        self.state = State()

        icon_path = resource_path(f'assets/{Icon[self.state.status]}.png')
        self.setIcon(QtGui.QIcon(icon_path))

        menu = QtWidgets.QMenu(parent)
        label_action = menu.addAction("Pyraficator-tray")
        label_action.triggered.connect(partial(SystemTrayIcon.open_in_browser, self, API_URL))
        menu.addSeparator()
        self.status_menu = menu.addMenu(f"Status: {Status.Unknown}")
        self.others_menu = menu.addMenu(f"Other Monitored Items")
        menu.addSeparator()
        exit_action = menu.addAction("Exit")

        exit_action.triggered.connect(self.exit)
        self.setContextMenu(menu)

        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(config.REFRESH_INTERVAL)
        self.timer.timeout.connect(self.refresh_state)
        self.timer.start()

    def exit(self):
        QtCore.QCoreApplication.exit()

    def open_in_browser(self, url):
        QtGui.QDesktopServices.openUrl(QtCore.QUrl(url))

    def refresh_state(self):
        new_state = get_status()

        same_status = new_state.status == self.state.status
        same_details = have_same_items(self.state.details, new_state.details)
        same_others = have_same_items(self.state.others, new_state.others)

        if not same_status:
            self.status_menu.setTitle(get_menu_name(new_state.status))
            icon_path = resource_path(f'assets/{Icon[new_state.status]}.png')
            self.setIcon(QtGui.QIcon(icon_path))

        if not same_details:
            self.create_menu_items(self.status_menu, new_state.details)
        if not same_others:
            self.create_menu_items(self.others_menu, new_state.others)

        self.state = new_state

        if new_state.status in self.config.NOTIFICATIONS_STATUSES and (not same_status or not same_details):
            self.show_notification()


    def create_menu_items(self, menu, items):
        menu.clear()
        for item in [i for i in items.values()]:
            action = menu.addAction(item.name)
            action.triggered.connect(partial(SystemTrayIcon.open_in_browser, self, item.link))

    def show_notification(self):
        items_no = len(self.state.details.keys())
        {
            "Success": lambda: self.showMessage("Weird", f"Everything works.", 1, self.config.NOTIFICATION_TIME),
            "InProgress": lambda: self.showMessage("Hold on", f"{items_no} item(s) in progress...", 2, self.config.NOTIFICATION_TIME),
            "Failure": lambda: self.showMessage("FUCK UP ALERT !!!", f"{items_no} failed item(s)!", 3, self.config.NOTIFICATION_TIME),
            "Unknown": lambda: None
        }[self.state.status]()

