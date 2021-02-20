"""Keyboard selection widgets."""

import os

from PyQt5.QtCore import QDir
from PyQt5.QtWidgets import QDockWidget, QTreeView, QFileSystemModel
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from core.origin import Origin
from core.keyboard import Keyboard


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


class ArduinoSelectionModel(QStandardItemModel):
    """Provide a data model for the keyboard selection."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setHorizontalHeaderLabels((
            self.tr("Origin"),
            self.tr("Keyboard")))
        self.origins = dict()

    def add_origin(self, origin: Origin):
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
        self.origins[origin] = QStandardItem(origin.value)
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
