"""Keyboard selection widgets."""

import os

from PyQt5.QtCore import QDir, QCoreApplication
from PyQt5.QtWidgets import QDockWidget, QTreeView, QFileSystemModel,\
    QVBoxLayout, QListView, QLabel, QWidget, QListWidget
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from core.origin import Origin
from core.keyboard import Keyboard, Right81ButtonKeyboard


class KeyboardFileSelection(QDockWidget):
    """Dock for displaying the directories containing keyboards."""

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.setWindowTitle(self.tr("File Selection"))
        self.tree_view = QTreeView(self)
        self.setWidget(self.tree_view)

        self.extensions = ["*.json"]

        self.selection_model = QFileSystemModel(self.tree_view)
        self.selection_model.setRootPath(os.getcwd())
        self.selection_model.setFilter(QDir.Files | QDir.AllDirs
                                       | QDir.NoDotAndDotDot)
        self.selection_model.setNameFilters(self.extensions)
        self.tree_view.setModel(self.selection_model)

        for i in range(1, self.selection_model.columnCount()):
            self.tree_view.hideColumn(i)


class ArduinoSelectionDock(QDockWidget):
    """Dock for displaying the keyboards currently within the Arduino."""

    def __init__(self, parent, controller, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.controller = controller
        self.setWindowTitle(self.tr("Arduino's keyboards"))

        arduino_widget = ArduinoSelectionWidget(controller)
        self.setWidget(arduino_widget)


class ArduinoSelectionWidget(QWidget):
    """Widget containing everithing needed to display keyboards of Arduino."""

    def __init__(self, controller, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.controller = controller
        self.controller.arduino.keyboards_list_changed.connect(
            self.update_keyboards)

        curr_kbds_label = QLabel(self.tr("Current keyboards"))
        self.current_keyboards = QTreeView()
        self.current_kbd_model = ArduinoSelectionModel()
        self.current_keyboards.setModel(self.current_kbd_model)
        self.current_keyboards.setHeaderHidden(True)

        stored_kbds_label = QLabel(self.tr("Stored keyboards"))
        self.stored_keyboards = QTreeView()
        self.stored_kbd_model = ArduinoSelectionModel()
        self.stored_keyboards.setModel(self.stored_kbd_model)
        self.stored_keyboards.setHeaderHidden(True)

        main_layout = QVBoxLayout()
        main_layout.addWidget(curr_kbds_label)
        main_layout.addWidget(self.current_keyboards)
        main_layout.addWidget(stored_kbds_label)
        main_layout.addWidget(self.stored_keyboards)

        self.setLayout(main_layout)

    def update_keyboards(self):
        """Update the keyboard lists to match the arduino internal state."""
        arduino = self.controller.arduino
        self.current_kbd_model.clear()
        self.stored_kbd_model.clear()
        for kbd in arduino.get_stored_keyboards():
            self.stored_kbd_model.add_keyboard(kbd)

        current = arduino.get_current_left_keyboard()
        if current:
            self.current_kbd_model.add_keyboard(current)

        current = arduino.get_current_right_keyboard()
        if current:
            self.current_kbd_model.add_keyboard(current)

    def current_keyboard_clicked(self, index):
        pass


class ArduinoSelectionModel(QStandardItemModel):
    """Provide a data model for the keyboard selection."""

    type_desc = {Right81ButtonKeyboard: {
        'desc': QCoreApplication.translate('ArduinoSelectionModel',
                                           "Right 81 buttons keyboard"),
        'icon': ''}
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.setHorizontalHeaderLabels([
        #     self.tr("Name")])
        self.type_items = {}

    def clear(self):
        self.type_items = {}
        super().clear()

    def add_keyboard(self, kbd: Keyboard):
        """
        Add a keyboard to the model.

        Parameters
        ----------
        kbd : Keyboard
            The keyboard to add.

        Returns
        -------
        None.

        """
        if type(kbd) not in self.type_items:
            self.type_items[type(kbd)] = QStandardItem(
                self.type_desc[type(kbd)]['desc'])
            item = self.type_items[type(kbd)]
            item.setEditable(False)
            self.invisibleRootItem().appendRow(item)

        type_item = self.type_items[type(kbd)]
        item = QStandardItem(kbd.name)
        item.setEditable(False)

        type_item.appendRow(item)
