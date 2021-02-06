"""Contains the main class of the GUI module.

Icons made by <a href="https://www.flaticon.com/authors/google"
title="Google">Google</a> from <a href="https://www.flaticon.com/"
title="Flaticon"> www.flaticon.com</a>
"""
import sys
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow

from toolbar import ToolBar
from keyboardselection import KeyboardSelection


class ControllerGUI(QMainWindow):
    """Main class of the GUI module using QT framework."""

    def __init__(self):
        super().__init__()

        self.setMinimumSize(QSize(640, 480))
        self.setWindowTitle("Controller")

        self.toolbar = ToolBar(self)
        self.addToolBar(Qt.TopToolBarArea, self.toolbar)

        self.statusBar().showMessage("Initialization done")

    # def connect_toolbar(self):
    #     self.toolbar.pull_action.triggered.connect(self.pull_layouts)
    #     self.toolbar.create_keyboard_action.triggered.connect(self.create_layout)
    #     self.clone_layout_action.triggered.connect(self.clone_layout)
    #     self.delete_layout_action.triggered.connect(self.delete_layout)
    #     self.apply_layout_action.triggered.connect(self.apply_layout)
    #     self.store_layout_action.triggered.connect(self.store_layout)
    #     self.apply_and_store_layout_action.triggered.connect(
    #             self.apply_and_store_layout)
    #     self.reset_layout_action.triggered.connect(self.reset_layout)
    #     self.about_action.triggered.connect(self.about_dialog)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = ControllerGUI()
    main_win.show()
    sys.exit(app.exec_())
