import os
import re
import sys
from enum import Enum
from functools import partial
from PyQt5 import QtCore, QtGui, QtWidgets
from core import Config, get_status, State, Status, StatusItem, WEB_URL

class Icon(Enum):
    Failure = "red"
    InProgress = "yellow"
    Success = "green"
    Unknown = "unknown"

    def __str__(self):
        return self.value

get_menu_name = lambda status: f"Status: {Status[status]}"

has_match = lambda text, pattern: bool(re.search(re.compile(pattern), text))

has_matching_items = lambda items, pattern: any([has_match(i.details, pattern) for i in items.values()])

have_same_items = lambda d1, d2: d1.keys() == d2.keys()

def has_matching_diff(old, new, pattern):
    det_old, det_new = list(map(lambda i: i.details, old.values())), list(map(lambda i: i.details, new.values()))
    diff = list(set(det_new) - set(det_old))
    filtered = list(filter(lambda d: has_match(d, pattern), diff))
    return len(filtered) > 0

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
        label_action.triggered.connect(partial(SystemTrayIcon.open_in_browser, self, WEB_URL))
        menu.addSeparator()
        self.status_menu = menu.addMenu(f"Status: {Status.Unknown}")
        self.others_menu = menu.addMenu(f"Other Monitored Items")
        menu.addSeparator()
        exit_action = menu.addAction("Exit")

        exit_action.triggered.connect(self.exit)
        self.setContextMenu(menu)

        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(config.refreshInterval)
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
        new_matching_items, has_matching, old_has_matching = None, None, None
        if self.config.notificationRegex is not None:
            new_matching_items = has_matching_diff(self.state.details, new_state.details, self.config.notificationRegex)
            has_matching = has_matching_items(new_state.details, self.config.notificationRegex)
            old_has_matching = has_matching_items(self.state.details, self.config.notificationRegex)
            new_state.observedChanged = new_state.status != Status.Success and (self.state.observedChanged or has_matching or new_matching_items)

        if not same_status:
            self.status_menu.setTitle(get_menu_name(new_state.status))
            icon_path = resource_path(f'assets/{Icon[new_state.status]}.png')
            self.setIcon(QtGui.QIcon(icon_path))

        if not same_details:
            self.create_menu_items(self.status_menu, new_state.details)
        if not same_others:
            self.create_menu_items(self.others_menu, new_state.others)

        should_show_notification = new_state.status in self.config.notificationStatuses and \
            (not same_status or not same_details) if self.config.notificationRegex is None else \
                (new_state.status == Status.Success and (not same_status and (old_has_matching or self.state.observedChanged))) or \
                (new_state.status == Status.InProgress and ((not same_status and has_matching) or new_matching_items)) or \
                (new_state.status == Status.Failure and ((not same_status and has_matching) or new_matching_items))

        self.state = new_state

        if should_show_notification:
            self.show_notification()


    def create_menu_items(self, menu, items):
        menu.clear()
        for item in [i for i in items.values()]:
            action = menu.addAction(item.name)
            action.triggered.connect(partial(SystemTrayIcon.open_in_browser, self, item.link))


    def show_notification(self):
        items_no = len(self.state.details.keys())
        {
            "Success": lambda: self.showMessage("Weird", f"Everything works", 1, self.config.notificationTime),
            "InProgress": lambda: self.showMessage("Hold on", f"{items_no} item(s) in progress...", 2, self.config.notificationTime),
            "Failure": lambda: self.showMessage("FUCK UP ALERT!!!", f"{items_no} item(s) failed!", 3, self.config.notificationTime),
            "Unknown": lambda: None
        }[self.state.status]()
