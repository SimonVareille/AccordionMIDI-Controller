"""Keyboard selection widget."""
from PyQt5.QtWidgets import QDockWidget


class KeyboardSelection(QDockWidget):
    """Dock for displaying the list of known keyboard, from every origin."""

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.setWindowTitle(self.tr("Keyboard Selection"))
