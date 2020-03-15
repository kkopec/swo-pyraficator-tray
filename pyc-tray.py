import os
import sys
from PyQt5 import QtCore, QtGui, QtWidgets

class SystemTrayIcon(QtWidgets.QSystemTrayIcon):

    def __init__(self, icon, parent=None):
        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
        menu = QtWidgets.QMenu(parent)
        exitAction = menu.addAction("Exit")
        self.setContextMenu(menu)
        menu.triggered.connect(self.exit)

    def exit(self):
        QtCore.QCoreApplication.exit()


def main(image):
    icon='favicon.ico'
    app = QtWidgets.QApplication(sys.argv)

    widget = QtWidgets.QWidget()
    trayIcon = SystemTrayIcon(QtGui.QIcon(icon), widget)

    trayIcon.show()
    trayIcon.showMessage("title", "test")
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

