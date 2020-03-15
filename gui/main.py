import os
import sys
import re
from PyQt5 import QtCore, QtGui, QtWidgets
from config import ICON_PATH
from api import get_status, PycStatus
from enum import Enum

class Icon(Enum):
    Failure = "red",
    InProgress = "yellow",
    Success = "green"

    def __str__(self):
        return self.value


get_item_id = lambda item: re.search(r"((?<=with ID )\d+|SEQ)", item['details']).group()


class SystemTrayIcon(QtWidgets.QSystemTrayIcon):
    status = dict()

    def __init__(self, icon, parent=None):
        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
        menu = QtWidgets.QMenu(parent)
        exit_action = menu.addAction("Exit")

        exit_action.triggered.connect(self.exit)
        self.setContextMenu(menu)

        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(10000)
        self.timer.timeout.connect(self.get_status)
        self.timer.start()

    def exit(self):
        QtCore.QCoreApplication.exit()

    def get_status(self):
        result = get_status()
        status = result['status']
        details = result['statusDetails']

        icon_path = f'assets/{Icon[status]}.ico'
        self.setIcon(QtGui.QIcon(icon_path))

        if status == 'Failure':
            ids = [get_item_id(item) for item in details]
            should_ignore = all(id in self.status for id in ids)
            self.status = dict((id, True) for id in ids)

            if not should_ignore:
                self.showMessage("ALARMA !!!", f"{len(details)} items failed", 3, 5000)


def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName('Pyraficator5000')

    widget = QtWidgets.QWidget()
    tray_icon = SystemTrayIcon(QtGui.QIcon(ICON_PATH), widget)

    tray_icon.show()
    sys.exit(app.exec_())

