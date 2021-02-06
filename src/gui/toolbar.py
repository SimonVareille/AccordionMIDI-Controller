"""Toolbar of the controller."""

from PyQt5.QtWidgets import QToolBar, QAction, QApplication
from PyQt5.QtGui import QIcon


class ToolBar(QToolBar):
    """The toolbar of the controller."""

    def __init__(self, owner, *args, **kwargs):
        super().__init__(
            QApplication.translate("ToolBar", "Keyboard actions"),
            owner, *args, **kwargs)
        self.pull_action = QAction(
            QIcon('icons/download-button'),
            self.tr('Pull keyboards from accordion'),
            owner)
        self.create_keyboard_action = QAction(
            QIcon('icons/round-add-button'),
            self.tr('Create new keyboard'),
            owner)
        self.clone_keyboard_action = QAction(
            QIcon('icons/copy-content'),
            self.tr('Clone current keyboard'),
            owner)
        self.delete_keyboard_action = QAction(
            QIcon('icons/round-delete-button'),
            self.tr('Delete current keyboard'), owner)
        self.apply_keyboard_action = QAction(
            QIcon('icons/send-button'),
            self.tr('Apply current keyboard on accordion'),
            owner)
        self.store_keyboard_action = QAction(
            QIcon('icons/save-button'),
            self.tr('Store current keyboard on accordion'),
            owner)
        self.apply_and_store_keyboard_action = QAction(
            QIcon('icons/upload-button'),
            self.tr('Apply and store current keyboard on accordion'), owner)
        self.reset_keyboard_action = QAction(
            QIcon('icons/undo-button.svg'),
            self.tr('Reset current keyboard'), owner)
        self.about_action = QAction(
            QIcon('icons/help.svg'),
            self.tr('About'),
            owner)

        # disable toolbuttons that needs input or output port initialized
        self.pull_action.setEnabled(False)

        # populate toolbar
        self.addAction(self.pull_action)
        self.addAction(self.create_keyboard_action)
        self.addAction(self.clone_keyboard_action)
        self.addAction(self.delete_keyboard_action)
        self.addAction(self.reset_keyboard_action)
        self.addAction(self.apply_keyboard_action)
        self.addAction(self.store_keyboard_action)
        self.addAction(self.apply_and_store_keyboard_action)
        self.addSeparator()
        self.addAction(self.about_action)
