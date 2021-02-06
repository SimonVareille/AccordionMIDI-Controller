"""Toolbar of the controller."""

from PyQt5.QtWidgets import QToolBar, QAction
from PyQt5.QtGui import QIcon


class ToolBar(QToolBar):
    """The toolbar of the controller."""

    def __init__(self, owner, *args, **kwargs):
        super().__init__("Keyboard actions", owner, *args, **kwargs)
        self.pull_action = QAction(QIcon('icons/download-button'),
                                   'Pull keyboards from accordion', owner)
        self.create_keyboard_action = QAction(QIcon('icons/round-add-button'),
                                              'Create new keyboard', owner)
        self.clone_keyboard_action = QAction(QIcon('icons/copy-content'),
                                             'Clone current keyboard', owner)
        self.delete_keyboard_action = QAction(
            QIcon('icons/round-delete-button'),
            'Delete current keyboard', owner)
        self.apply_keyboard_action = QAction(
            QIcon('icons/send-button'), 'Apply current keyboard on accordion',
            owner)
        self.store_keyboard_action = QAction(
            QIcon('icons/save-button'),
            'Store current keyboard on accordion',
            owner)
        self.apply_and_store_keyboard_action = QAction(
            QIcon('icons/upload-button'),
            'Apply and store current keyboard on accordion', owner)
        self.reset_keyboard_action = QAction(
            QIcon('icons/undo-button.svg'),
            'Reset current keyboard', owner)
        self.about_action = QAction(QIcon('icons/help.svg'), 'About', owner)

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
