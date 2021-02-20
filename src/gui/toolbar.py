"""Toolbar of the controller."""

from PyQt5.QtWidgets import QToolBar, QAction, QApplication
from PyQt5.QtGui import QIcon

import gui.resources


class ToolBar(QToolBar):
    """The toolbar of the controller."""

    def __init__(self, owner, actions, *args, **kwargs):
        super().__init__(
            QApplication.translate("ToolBar", "Keyboard actions"),
            owner, *args, **kwargs)

        # disable toolbuttons that needs input or output port initialized
        actions.pull.setEnabled(False)

        # populate toolbar
        self.addAction(actions.pull)
        self.addAction(actions.new)
        self.addAction(actions.clone_keyboard)
        self.addAction(actions.delete_keyboard)
        self.addAction(actions.reset_keyboard)
        self.addAction(actions.apply_keyboard)
        self.addAction(actions.store_keyboard)
        self.addAction(actions.apply_and_store_keyboard)
        self.addSeparator()
        self.addAction(actions.about)
