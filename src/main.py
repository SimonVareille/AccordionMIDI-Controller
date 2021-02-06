"""Main module."""

import sys
from PyQt5.QtWidgets import QApplication

from gui.controller import ControllerGUI

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = ControllerGUI()
    main_win.show()
    sys.exit(app.exec_())
