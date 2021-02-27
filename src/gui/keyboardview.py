"""Widgets displaying the keyboards."""
import os

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QTabWidget, QVBoxLayout, QHBoxLayout,\
    QLabel, QLineEdit


class CurrentKeyboardsWidget(QWidget):
    """Widget containing every keyboards widgets currently opened."""

    def __init__(self, parent):
        super().__init__(parent)

        self.tabs = []
        self.layout = QVBoxLayout(self)
        self.tab_widget = QTabWidget(self)

        self.layout.addWidget(self.tab_widget)
        self.setLayout(self.layout)

    def add_keyboard(self, kbd_state):
        """
        Add a new keyboard to the keyboard list.

        Parameters
        ----------
        kbd_state : KeyboardState
            The keyboard to add.

        Returns
        -------
        None.

        """
        new_tab = KeyboardView(kbd_state)

        self.tab_widget.addTab(new_tab,
                               os.path.basename(kbd_state.storage.filename)
                               + ('*' if not kbd_state.is_saved else ''))
        new_tab.changes_made.connect(self.keyboard_changed)
        self.tabs.append(new_tab)

    def display_keyboard(self, kbd_state):
        """
        Display the given keyboard.

        If the keyboard is already open, switch to it.

        Parameters
        ----------
        kbd_state : KeyboardState
            The keyboard to display.

        Returns
        -------
        None.

        """
        self.add_keyboard(kbd_state)

    def keyboard_changed(self):
        index = self.tab_widget.indexOf(self.sender())
        kbd_state = self.sender().keyboard_state
        print("pass")
        self.tab_widget.setTabText(index,
                                   os.path.basename(kbd_state.storage.filename)
                                   + ('*' if not kbd_state.is_saved else ''))

class KeyboardView(QWidget):
    """Widget containing everything a keyboard need."""

    changes_made = pyqtSignal()

    def __init__(self, kbd_state):
        super().__init__()
        self.keyboard_state = kbd_state
        self.main_layout = QVBoxLayout(self)

        self.name_layout = QHBoxLayout(self)
        self.name_edit = QLineEdit(kbd_state.keyboard.name)
        self.name_layout.addWidget(QLabel(self.tr("Name:")))
        self.name_layout.addWidget(self.name_edit)

        self.main_layout.addLayout(self.name_layout)
        self.setLayout(self.main_layout)

        self.connect_signals()

    def connect_signals(self):
        self.name_edit.editingFinished.connect(self.name_edited)

    def name_edited(self):
        if self.name_edit.text() != self.keyboard_state.keyboard.name:
            self.keyboard_state.rename(self.name_edit.text())
            self.changes_made.emit()
