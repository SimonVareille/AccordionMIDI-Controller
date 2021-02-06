"""Keyboard selection widget."""
from PyQt5.QtWidgets import QDockWidget, QTreeView
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from core.origin import Origin
from core.keyboard import Keyboard


class KeyboardSelection(QDockWidget):
    """Dock for displaying the list of known keyboard, from every origin."""

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.setWindowTitle(self.tr("Keyboard Selection"))
        self.tree_view = QTreeView(self)
        self.setWidget(self.tree_view)

        self.selection_model = SelectionModel()
        self.tree_view.setModel(self.selection_model)


class SelectionModel(QStandardItemModel):
    """Provide a data model for the keyboard selection."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setHorizontalHeaderLabels((
            self.tr("Origin"),
            self.tr("Keyboard")))
        self.origins = dict()

    def add_origin(self, origin: Origin, origin_name: str):
        """
        Add an origin to the model.

        Parameters
        ----------
        origin : Origin
            The origin to add.
        origin_name : str
            The name of the origin.

        Returns
        -------
        None.

        """
        self.origins[origin] = QStandardItem(origin_name)
        self.origins[origin].setEditable(False)
        self.invisibleRootItem().appendRow(self.origins[origin])

    def add_keyboard(self, origin: Origin, kbd: Keyboard):
        """
        Add a keyboard to the model.

        The keyboard is linked to origin.

        Parameters
        ----------
        origin : Origin
            The origin of the keyboard.
        kbd : Keyboard
            The keyboard to add.

        Returns
        -------
        None.

        """
        self.origins[origin].appendRow([None, QStandardItem(kbd.name)])
