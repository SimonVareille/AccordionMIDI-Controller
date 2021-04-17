"""Main module."""

import sys
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QApplication

from gui.controller import ControllerGUI

if __name__ == "__main__":
    app = QApplication(sys.argv)
    QCoreApplication.setOrganizationName("Accordion MIDI")
    QCoreApplication.setOrganizationDomain("")
    QCoreApplication.setApplicationName("Controller")
    main_win = ControllerGUI()
    main_win.show()
    sys.exit(app.exec_())
