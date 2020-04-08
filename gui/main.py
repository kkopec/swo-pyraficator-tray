import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from core import Config, VERSION
from gui.system_tray import SystemTrayIcon


def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName(f'Pyraficator-tray v{VERSION}')

    config = Config()

    widget = QtWidgets.QWidget()
    tray_icon = SystemTrayIcon(config, widget)

    tray_icon.show()
    sys.exit(app.exec_())
