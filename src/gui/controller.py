"""Contains the main class of the GUI module.

Icons made by <a href="https://www.flaticon.com/authors/google"
title="Google">Google</a> from <a href="https://www.flaticon.com/"
title="Flaticon"> www.flaticon.com</a>
"""
import os

# pylint: disable=E0611
from PyQt5.QtCore import QSize, Qt, QObject, QCoreApplication, QSettings
from PyQt5.QtWidgets import QMainWindow, QAction, QFileDialog, QDialog,\
    QDialogButtonBox, QVBoxLayout, QFormLayout, QComboBox, QLabel
from PyQt5.QtGui import QIcon

from core import ControllerCore
from core.keyboard import Right81ButtonKeyboard

import gui.resources  # pylint: disable=W0611
from .toolbar import ToolBar
from .keyboardselection import ArduinoSelectionDock
from .keyboardview import CurrentKeyboardsWidget
from .settings import SettingsDialog


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

        edit_menu = menubar.addMenu(self.tr('&Edit'))
        edit_menu.addAction(self.actions.undo)
        edit_menu.addAction(self.actions.redo)
        edit_menu.addSeparator()
        edit_menu.addAction(self.actions.settings)

        # Tool bar

        self.toolbar = ToolBar(self, self.actions)
        self.addToolBar(Qt.TopToolBarArea, self.toolbar)

        # File selection dock
        # self.keyboard_selection = KeyboardFileSelection(self)
        # self.keyboard_selection.setAllowedAreas(
        #     Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        # self.addDockWidget(Qt.LeftDockWidgetArea, self.keyboard_selection)

        # self.populate_keyboard_selection_model()

        self.current_keyboards = CurrentKeyboardsWidget(self, self.controller)
        self.setCentralWidget(self.current_keyboards)
        self.current_keyboards.show_message.connect(self.show_status_message)

        self.connect_actions()

        self.load_settings()
        self.show_status_message(self.tr("Initialization done"))

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
        self.actions.new.triggered.connect(self.create_keyboard_dialog)
        self.actions.undo.triggered.connect(self.current_keyboards.undo)
        self.actions.redo.triggered.connect(self.current_keyboards.redo)
        self.actions.settings.triggered.connect(self.settings_dialog)
        self.actions.send.triggered.connect(self.current_keyboards.send)
        self.actions.store.triggered.connect(self.current_keyboards.store)
        self.actions.pull.triggered.connect(self.controller.pull_keyboards)
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

    def closeEvent(self, *args, **kwargs):
        """Clean everything before closing."""
        print("Closing...")
        self.controller.close_midi()
        super().closeEvent(*args, **kwargs)

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
        if filename:
            keyboard_state = self.controller.open(filename)
            self.current_keyboards.display_keyboard(keyboard_state)

    def create_keyboard_dialog(self):
        """
        Open the keyboard creation dialog.

        Returns
        -------
        None.

        """
        dlg = CreateKeyboardDialog()
        if dlg.exec_() and dlg.selected_type:
            keyboard_state = self.controller.create(dlg.selected_type)
            self.current_keyboards.display_keyboard(keyboard_state)

    def settings_dialog(self):
        """Open the settings dialog."""
        dlg = SettingsDialog(self.controller, self)
        dlg.settings_changed.connect(self.load_settings)
        dlg.exec_()

    def load_settings(self):
        """Update UI and core regarding settings."""
        settings = QSettings()

        settings.beginGroup("midi")
        self.controller.close_midi()
        inprt = str(settings.value("inport", "-"))
        if inprt == "-":
            inprt = None
        outprt = str(settings.value("outport", "-"))
        if outprt == "-":
            outprt = None

        self.controller.connect_midi(inprt, outprt)

        if self.controller.is_midi_output_ready():
            self.actions.send.setEnabled(True)
            self.actions.store.setEnabled(True)
        else:
            self.actions.send.setEnabled(False)
            self.actions.store.setEnabled(False)

        if(self.controller.is_midi_input_ready()
           and self.controller.is_midi_output_ready()):
            self.actions.pull.setEnabled(True)
        else:
            self.actions.pull.setEnabled(False)

        settings.endGroup()  # midi

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

    def show_status_message(self, message, timeout=5000):
        """
        Show the given message in the status bar for `time` milliseconds.

        Parameters
        ----------
        message : str
            The message to show.
        timeout : int, optional
            The time in milliseconds for wich to show the message.
            If 0, the message is displayed until another message comes.
            The default is 5000.

        Returns
        -------
        None.

        """
        self.statusBar().showMessage(message, timeout)


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
        # Undo
        self.undo = QAction(
            QIcon(':/icons/undo-button.svg'),
            self.tr('Undo'),
            owner)
        self.undo.setShortcut('Ctrl+Z')
        self.undo.setStatusTip(self.tr('Undo last action'))
        # Redo
        self.redo = QAction(
            QIcon(':/icons/redo-button.svg'),
            self.tr('Redo'),
            owner)
        self.redo.setShortcut('Ctrl+Shift+Z')
        self.redo.setStatusTip(self.tr('Redo last undoed action'))
        # Settings
        self.settings = QAction(
            QIcon(':/icons/settings.svg'),
            self.tr('Settings'),
            owner)
        self.settings.setShortcut('Ctrl+P')
        self.settings.setStatusTip(self.tr('Open settings dialog'))
        # Pull from Arduino
        self.pull = QAction(
            QIcon(':/icons/download-button.svg'),
            self.tr('Pull keyboards'),
            owner)
        self.pull.setStatusTip(self.tr('Pull keyboards from accordion'))
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
        # Send to Arduino
        self.send = QAction(
            QIcon(':/icons/send-button.svg'),
            self.tr('Send current keyboard to the accordion'),
            owner)
        # Store on Arduino
        self.store = QAction(
            QIcon(':/icons/upload-button.svg'),
            self.tr('Store current keyboard on accordion'),
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


class CreateKeyboardDialog(QDialog):
    """Dialog to create a new keyboard."""

    keyboard_types = [{'name': QCoreApplication.translate(
        'CreateKeyboardDialog',
        'Right 81 Buttons Keyboard'),
        'type': Right81ButtonKeyboard,
        'desc': QCoreApplication.translate(
        'CreateKeyboardDialog', """
<p>A right button keyboard of 81 button, as 4 rows of 16 buttons
and 1 row of 17 buttons.</p>
<br/>
<img src=':/right-81-buttons-svg/full.svg'>
""")}]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.selected_type = None

        self.setWindowTitle(self.tr("Create a new keyboard"))
        self.setWindowModality(Qt.WindowModal)

        main_layout = QVBoxLayout(self)

        self.keyboard_type = QComboBox(self)
        for kbd in self.keyboard_types:
            self.keyboard_type.addItem(kbd['name'])
        self.keyboard_type.currentIndexChanged.connect(self.set_description)

        self.description_label = QLabel(self)
        self.description_label.setTextFormat(Qt.RichText)
        self.set_description()

        form = QFormLayout(self)
        form.addRow(self.tr("Keyboard type:"), self.keyboard_type)
        form.addRow(self.tr("Description:"), self.description_label)

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.button_box = QDialogButtonBox(QBtn, self)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        main_layout.addLayout(form)
        main_layout.addWidget(self.button_box)

        self.setLayout(main_layout)

    def set_description(self, index=None):
        """Display the description of keyboard at given index."""
        if not index:
            index = self.keyboard_type.currentIndex()
        kbd = self.keyboard_types[index]
        self.description_label.setText(kbd['desc'])

    def accept(self):
        """Accept current choice."""
        index = self.keyboard_type.currentIndex()
        self.selected_type = self.keyboard_types[index]['type']
        super().accept()
