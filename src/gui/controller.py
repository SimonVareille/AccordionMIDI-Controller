"""Contains the main class of the GUI module.

Icons made by <a href="https://www.flaticon.com/authors/google"
title="Google">Google</a> from <a href="https://www.flaticon.com/"
title="Flaticon"> www.flaticon.com</a>
"""
import sys
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow

from core import ControllerCore
from core.origin import Origin

from .toolbar import ToolBar
from .keyboardselection import KeyboardSelection


class ControllerGUI(QMainWindow):
    """Main class of the GUI module using QT framework."""

    def __init__(self):
        super().__init__()

        self.setMinimumSize(QSize(640, 480))
        self.setWindowTitle("Controller")

        # Controller core
        self.controller = ControllerCore()

        # Tool bar

        self.toolbar = ToolBar(self)
        self.addToolBar(Qt.TopToolBarArea, self.toolbar)
        # self.connect_toolbar()

        # Keyboard selection dock
        self.keyboard_selection = KeyboardSelection(self)
        self.keyboard_selection.setAllowedAreas(
            Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.keyboard_selection)

        self.populate_keyboard_selection_model()

        self.statusBar().showMessage(self.tr("Initialization done"))

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

    def populate_keyboard_selection_model(self):
        """
        Populate the model.

        Returns
        -------
        None.

        """
        keyboards = self.controller.get_known_keyboards()
        for origin, lst_kbds in keyboards.items():
            self.keyboard_selection.selection_model.add_origin(origin)
            for kbd in lst_kbds:
                self.keyboard_selection.selection_model.add_keyboard(
                    origin, kbd)
