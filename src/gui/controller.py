"""Contains the main class of the GUI module.

Icons made by <a href="https://www.flaticon.com/authors/google"
title="Google">Google</a> from <a href="https://www.flaticon.com/"
title="Flaticon"> www.flaticon.com</a>
"""
import os

from PyQt5.QtCore import QSize, Qt, QObject, QCoreApplication
from PyQt5.QtWidgets import QMainWindow, QAction, QFileDialog
from PyQt5.QtGui import QIcon

from core import ControllerCore

from .toolbar import ToolBar
from .keyboardselection import KeyboardFileSelection
from .keyboardview import CurrentKeyboardsWidget
import gui.resources


class ControllerGUI(QMainWindow):
    """Main class of the GUI module using QT framework."""

    def __init__(self):
        super().__init__()

        self.setMinimumSize(QSize(1600, 600))
        self.setWindowTitle("Controller")

        self.base_path = os.getcwd()

        # Controller core
        self.controller = ControllerCore()

        # Actions
        self.actions = Actions(self)

        # Menu bar
        menubar = self.menuBar()
        file_menu = menubar.addMenu(self.tr('&File'))
        file_menu.addAction(self.actions.new)
        file_menu.addAction(self.actions.open)
        file_menu.addAction(self.actions.save)
        file_menu.addAction(self.actions.save_as)
        file_menu.addSeparator()
        file_menu.addAction(self.actions.exit)

        # Tool bar

        self.toolbar = ToolBar(self, self.actions)
        self.addToolBar(Qt.TopToolBarArea, self.toolbar)

        # Keyboard selection dock
        self.keyboard_selection = KeyboardFileSelection(self)
        self.keyboard_selection.setAllowedAreas(
            Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.keyboard_selection)

        # self.populate_keyboard_selection_model()

        self.current_keyboards = CurrentKeyboardsWidget(self, self.controller)
        self.setCentralWidget(self.current_keyboards)

        self.connect_actions()

        self.statusBar().showMessage(self.tr("Initialization done"))

    def connect_actions(self):
        """
        Connect the QActions signals with internal slots.

        Returns
        -------
        None.

        """
        self.actions.exit.triggered.connect(self.close)
        self.actions.open.triggered.connect(self.open_file_dialog)
        self.actions.save.triggered.connect(self.current_keyboards.save)
        self.actions.save_as.triggered.connect(self.current_keyboards.save_as)
        # self.actions.pull.triggered.connect(
        #     self.pull_layouts)
        # self.actions.create_keyboard.triggered.connect(
        #     self.create_layout)
        # self.actions.clone_keyboard.triggered.connect(
        #     self.clone_layout)
        # self.actions.delete_keyboard.triggered.connect(
        #     self.delete_layout)
        # self.actions.apply_keyboard.triggered.connect(
        #     self.apply_layout)
        # self.actions.store_keyboard.triggered.connect(
        #     self.store_layout)
        # self.actions.apply_and_store_keyboard.triggered.connect(
        #         self.apply_and_store_layout)
        # self.actions.reset_keyboard.triggered.connect(
        #     self.reset_layout)
        # self.actions.about.triggered.connect(
        #     self.about_dialog)

    def close(self):
        """
        Close the applicaiton.

        Returns
        -------
        None.

        """
        QCoreApplication.quit()

    def open_file_dialog(self):
        """
        Open the file dialog.

        Returns
        -------
        None.

        """
        filename = QFileDialog.getOpenFileName(
            self,
            self.tr("Open Keyboard"),
            self.base_path,
            self.tr("Keyboard Files (*.json)"))[0]
        keyboard_state = self.controller.open(filename)
        self.current_keyboards.display_keyboard(keyboard_state)

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


class Actions(QObject):
    """Contains every QAction the GUI can use."""

    def __init__(self, owner):
        super().__init__(owner)
        # Exit
        self.exit = QAction(
            QIcon(':/icons/power-off-solid.svg'),
            self.tr('&Exit'),
            owner)
        self.exit.setShortcut('Ctrl+Q')
        self.exit.setStatusTip(self.tr('Exit application'))
        # Open
        self.open = QAction(
            QIcon(':/icons/folder-symbol.svg'),
            self.tr('&Open'),
            owner)
        self.open.setShortcut('Ctrl+O')
        self.open.setStatusTip(self.tr('Open a file'))
        # Save
        self.save = QAction(
            QIcon(':/icons/save-button.svg'),
            self.tr('&Save'),
            owner)
        self.save.setShortcut('Ctrl+S')
        self.save.setStatusTip(self.tr('Save a file'))
        # Save as
        self.save_as = QAction(
            QIcon(':/icons/save-button.svg'),
            self.tr('&Save as'),
            owner)
        self.save_as.setShortcut('Ctrl+Shift+S')
        self.save_as.setStatusTip(
            self.tr('Save a file currently edited as another name'))
        # New
        self.new = QAction(
            QIcon(':/icons/google-drive-file.svg'),
            self.tr('Create new keyboard'),
            owner)
        self.new.setShortcut('Ctrl+N')
        self.new.setStatusTip(self.tr('Create a new keyboard'))
        # Pull from Arduino
        self.pull = QAction(
            QIcon(':/icons/download-button.svg'),
            self.tr('Pull keyboards from accordion'),
            owner)
        # Clone
        self.clone_keyboard = QAction(
            QIcon(':/icons/copy-content.svg'),
            self.tr('Clone current keyboard'),
            owner)
        # Delete
        self.delete_keyboard = QAction(
            QIcon(':/icons/round-delete-button.svg'),
            self.tr('Delete current keyboard'),
            owner)
        # Apply on Arduino
        self.apply_keyboard = QAction(
            QIcon(':/icons/send-button.svg'),
            self.tr('Apply current keyboard on accordion'),
            owner)
        # Store on Arduino
        self.store_keyboard = QAction(
            QIcon(':/icons/save-button.svg'),
            self.tr('Store current keyboard on accordion'),
            owner)
        # Apply and store on Arduino
        self.apply_and_store_keyboard = QAction(
            QIcon(':/icons/upload-button.svg'),
            self.tr('Apply and store current keyboard on accordion'),
            owner)
        # Reset
        self.reset_keyboard = QAction(
            QIcon(':/icons/undo-button.svg'),
            self.tr('Reset current keyboard'),
            owner)
        # Help
        self.about = QAction(
            QIcon(':/icons/help.svg'),
            self.tr('About'),
            owner)