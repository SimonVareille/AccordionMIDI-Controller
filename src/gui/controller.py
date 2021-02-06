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

        # self.connect_toolbar()

        self.statusBar().showMessage("Initialization done")

    def connect_toolbar(self):
        """
        Connect the toolbar signals with internal slots.

        Returns
        -------
        None.

        """
        self.toolbar.pull_action.triggered.connect(
            self.pull_layouts)
        self.toolbar.create_keyboard_action.triggered.connect(
            self.create_layout)
        self.toolbar.clone_keyboard_action.triggered.connect(
            self.clone_layout)
        self.toolbar.delete_keyboard_action.triggered.connect(
            self.delete_layout)
        self.toolbar.apply_keyboard_action.triggered.connect(
            self.apply_layout)
        self.toolbar.store_keyboard_action.triggered.connect(
            self.store_layout)
        self.toolbar.apply_and_store_keyboard_action.triggered.connect(
                self.apply_and_store_layout)
        self.toolbar.reset_keyboard_action.triggered.connect(
            self.reset_layout)
        self.toolbar.about_action.triggered.connect(
            self.about_dialog)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = ControllerGUI()
    main_win.show()
    sys.exit(app.exec_())
