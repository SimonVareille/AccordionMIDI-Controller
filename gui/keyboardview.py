"""Widgets displaying the keyboards."""
import os
import traceback
# from functools import partial

# pylint: disable=E0611
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QTabWidget, QVBoxLayout, QHBoxLayout,\
    QLabel, QLineEdit, QFileDialog, QMessageBox

from core import NothingToUndoError, NothingToRedoError
from core.keyboard import Left96ButtonKeyboard, Right81ButtonKeyboard
from .keyboardgraphicalview import Right81ButtonKeyboardGraphicalView


class CurrentKeyboardsWidget(QWidget):
    """Widget containing every keyboards widgets currently opened."""

    show_message = pyqtSignal([str], [str, int])

    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller

        self.layout = QVBoxLayout(self)
        self.tab_widget = QTabWidget(self)

        self.tab_widget.setTabsClosable(True)
        self.tab_widget.setMovable(True)

        self.tab_widget.tabCloseRequested.connect(self.close_tab)

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
        new_tab = KeyboardView(kbd_state, self.controller)

        if kbd_state.storage:
            self.tab_widget.addTab(new_tab,
                                   os.path.basename(kbd_state.storage.filename)
                                   + ('*' if not kbd_state.is_saved else ''))
        else:
            self.tab_widget.addTab(new_tab,
                                   "Untitled*")
        new_tab.changes_made.connect(self.keyboard_changed)
        new_tab.show_message.connect(self.show_message)
        self.tab_widget.setCurrentWidget(new_tab)

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
        for i in range(self.tab_widget.count()):
            tab = self.tab_widget.widget(i)
            if tab.keyboard_state == kbd_state:
                self.tab_widget.setCurrentWidget(tab)
                return
        self.add_keyboard(kbd_state)

    def keyboard_changed(self):
        """
        Update the view.

        Returns
        -------
        None.

        """
        index = self.tab_widget.indexOf(self.sender())
        kbd_state = self.sender().keyboard_state
        if kbd_state.storage:
            self.tab_widget.setTabText(index,
                                       os.path.basename(
                                           kbd_state.storage.filename)
                                       + ('*' if not kbd_state.is_saved
                                          else ''))
        else:
            self.tab_widget.setTabText(index, "Untitled*")

    def save(self, index=None):
        """Save keyboard at given index (or current if index is None)."""
        if index:
            tab = self.tab_widget.widget(index)
        else:
            tab = self.tab_widget.currentWidget()
        if tab:
            tab.save()

    def save_as(self, index=None):
        """Save keyboard at given index (or current if index is None).

        Prompt for a new name.
        """
        if index:
            tab = self.tab_widget.widget(index)
        else:
            tab = self.tab_widget.currentWidget()
        if tab:
            tab.save_as()

    def undo(self, index=None):
        """Undo changes at given index (or current if index is None)."""
        if index:
            tab = self.tab_widget.widget(index)
        else:
            tab = self.tab_widget.currentWidget()
        if tab:
            tab.undo()

    def redo(self, index=None):
        """Redo changes at given index (or current if index is None)."""
        if index:
            tab = self.tab_widget.widget(index)
        else:
            tab = self.tab_widget.currentWidget()
        if tab:
            tab.redo()

    def send(self, index=None):
        """Send keyboard at given index to Arduino.

        Send current keyboard if index is None.
        """
        if index:
            tab = self.tab_widget.widget(index)
        else:
            tab = self.tab_widget.currentWidget()
        if tab:
            tab.send()

    def store(self, index=None):
        """Store keyboard at given index to Arduino.

        Store current keyboard if index is None.
        """
        if index:
            tab = self.tab_widget.widget(index)
        else:
            tab = self.tab_widget.currentWidget()
        if tab:
            tab.store()

    def close_tab(self, index):
        """Close tab of given index."""
        tab = self.tab_widget.widget(index)
        kbd_state = tab.keyboard_state
        if kbd_state.storage and kbd_state.storage.filename:
            current_name = os.path.basename(kbd_state.storage.filename)
        else:
            current_name = "Untitled"
        if not kbd_state.is_saved:
            result = QMessageBox.question(
                self,
                self.tr("Unsaved changes"),
                self.tr(f"<b>{current_name}</b> has been modified.<br/>\
                        Would you like to save the changes?"),
                QMessageBox.StandardButtons(QMessageBox.Save
                                            | QMessageBox.Discard
                                            | QMessageBox.Cancel),
                QMessageBox.Cancel)
            if result == QMessageBox.Cancel:
                return
            if result == QMessageBox.Save:
                self.save(index)
        self.controller.close(kbd_state)
        self.tab_widget.removeTab(index)


class KeyboardView(QWidget):
    """Widget containing everything a keyboard need."""

    changes_made = pyqtSignal()
    show_message = pyqtSignal([str], [str, int])

    def __init__(self, kbd_state, controller):
        super().__init__()

        self.controller = controller
        self.keyboard_state = kbd_state

        self.main_layout = QVBoxLayout(self)

        self.name_layout = QHBoxLayout(self)
        self.name_edit = QLineEdit(kbd_state.keyboard.name)
        self.name_layout.addWidget(QLabel(self.tr("Name:")))
        self.name_layout.addWidget(self.name_edit)

        self.main_layout.addLayout(self.name_layout)

        if isinstance(kbd_state.keyboard, Right81ButtonKeyboard):
            self.keyboard_zone = Right81ButtonKeyboardGraphicalView(self,
                                                                    kbd_state)
        elif isinstance(kbd_state.keyboard, Left96ButtonKeyboard):
            raise NotImplementedError()
        else:
            raise UnknownKeyboardTypeError(
                f"Unknown keyboard type '{type(kbd_state.keyboard)}'.")
        self.main_layout.addWidget(self.keyboard_zone)

        self.setLayout(self.main_layout)

        self.connect_signals()

    def connect_signals(self):
        """Connect signals."""
        self.name_edit.editingFinished.connect(self.name_edited)
        self.keyboard_state.keyboard_changed.connect(self.update)

    def name_edited(self):
        """Emit a signal if name has changed."""
        if self.name_edit.text() != self.keyboard_state.keyboard.name:
            self.keyboard_state.rename(self.name_edit.text())
            self.changes_made.emit()

    def update(self):
        """Emit a signal to notify that keyboard has changed."""
        if self.name_edit.text() != self.keyboard_state.keyboard.name:
            self.name_edit.setText(self.keyboard_state.keyboard.name)
        self.changes_made.emit()

    def save(self):
        """Save keyboard."""
        if(self.keyboard_state.storage and
           self.keyboard_state.storage.filename):
            self.keyboard_state.save()
        else:
            self.save_as()

    def save_as(self):
        """Save keyboard under a new name."""
        if(self.keyboard_state.storage and
           self.keyboard_state.storage.filename):
            current_name = self.keyboard_state.storage.filename
        else:
            current_name = ""
        filename = QFileDialog.getSaveFileName(
            self,
            self.tr("Save Keyboard as"),
            current_name,
            self.tr("Keyboard Files (*.json)"))[0]
        if filename:
            self.controller.save_as(self.keyboard_state, filename)

    def undo(self):
        """Undo previous action."""
        try:
            self.keyboard_state.undo()
            self.update()
        except NothingToUndoError:
            pass

    def redo(self):
        """Redo previous undoed action."""
        try:
            self.keyboard_state.redo()
            self.update()
        except NothingToRedoError:
            pass

    def send(self):
        """Send the keyboard to the Arduino."""
        try:
            self.controller.arduino.set_current_keyboard(
                self.keyboard_state.keyboard)
            self.show_message.emit(
                self.tr("The keyboard has successfully been sent."))
        except Exception:
            QMessageBox.critical(
                self,
                self.tr("Error sending keyboard"),
                self.tr("The keyboard has not been sent.<br/>\
                        The following error occured:<br/>\
                        <code>{!s}</code>").format(traceback.format_exc()),
                QMessageBox.StandardButtons(QMessageBox.Ok),
                QMessageBox.Cancel)
            raise

    def store(self):
        """Store the keyboard to the Arduino."""
        try:
            self.controller.arduino.store_keyboard(
                self.keyboard_state.keyboard)
            self.show_message.emit(
                self.tr("The keyboard has successfully been stored."))
        except Exception:
            QMessageBox.critical(
                self,
                self.tr("Error sending keyboard"),
                self.tr("The keyboard has not been stored.<br/>\
                        The following error occured:<br/>\
                        <code>{!s}</code>").format(traceback.format_exc()),
                QMessageBox.StandardButtons(QMessageBox.Ok),
                QMessageBox.Cancel)
            raise


class UnknownKeyboardTypeError(Exception):
    """Keyboard type is unknown."""
