"""Holds settings dialog"""
# pylint: disable=E0611
from PyQt5.QtCore import Qt, qFuzzyCompare, pyqtSignal, QSize, QSettings
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsItem,\
    QGraphicsObject, QGraphicsSimpleTextItem, QDialog, QFormLayout,\
    QVBoxLayout, QHBoxLayout, QSpinBox, QDial, QDialogButtonBox, QComboBox,\
    QWidget, QStackedWidget, QListWidget, QListView, QSplitter,\
    QListWidgetItem, QGroupBox
from PyQt5.QtGui import QPixmap, QPainter, QColor, QBrush, QIcon
from PyQt5.QtSvg import QGraphicsSvgItem

import gui.resources  # pylint: disable=W0611


class SettingsDialog(QDialog):
    """Display a dialog used to update settings."""

    settings_changed = pyqtSignal()

    def __init__(self, controller, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.controller = controller

        self.setWindowTitle(self.tr("Settings"))
        self.setWindowModality(Qt.WindowModal)

        self.topics = QListWidget(self)
        self.topics.setViewMode(QListView.ListMode)
        self.topics.setMovement(QListView.Static)
        self.topics.currentItemChanged.connect(self.change_page)

        self.pages = QStackedWidget(self)
        self.create_pages()
        self.topics.setCurrentRow(0)

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Apply\
            | QDialogButtonBox.Cancel

        button_box = QDialogButtonBox(QBtn, self)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        button_box.button(QDialogButtonBox.Apply).clicked.connect(self.apply)
        button_box.button(QDialogButtonBox.Apply).setEnabled(False)
        self.button_box = button_box

        main_layout = QVBoxLayout()
        splitter = QSplitter(self)
        splitter.addWidget(self.topics)
        splitter.addWidget(self.pages)
        main_layout.addWidget(splitter)
        main_layout.addWidget(button_box)
        self.setLayout(main_layout)

    def create_pages(self):
        """Create the pages."""
        self.add_page(IOPage(self.controller, self))

    def add_page(self, page):
        """Add a new page to the settings."""
        topic = QListWidgetItem(self.topics)
        topic.setIcon(page.icon)
        topic.setText(page.name)
        topic.setTextAlignment(Qt.AlignHCenter)
        topic.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        page.setting_modified.connect(self.setting_modified)
        self.pages.addWidget(page)

    def change_page(self, current, previous):
        """Change the current displayed page."""
        if not current:
            current = previous
        self.pages.setCurrentIndex(self.topics.row(current))

    def apply(self):
        """Apply (save) changes."""
        for index in range(self.pages.count()):
            self.pages.widget(index).apply()
        self.button_box.button(QDialogButtonBox.Apply).setEnabled(False)
        self.settings_changed.emit()

    def accept(self):
        """Apply (save) changes and quit the settings dialog."""
        self.apply()
        return super().accept()

    def setting_modified(self):
        """Update the UI."""
        self.button_box.button(QDialogButtonBox.Apply).setEnabled(True)


class IOPage(QWidget):
    """Page to configure the communication with the Arduino."""

    setting_modified = pyqtSignal()

    def __init__(self, controller, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = self.tr("Input/Output")
        self.icon = QIcon(":/icons/input-output.svg")
        self.controller = controller

        # Ports selection
        ports_grp = QGroupBox(self.tr("Ports"), self)
        port_form = QFormLayout()
        self.inport_combo = QComboBox()
        self.inport_combo.currentTextChanged.connect(self.setting_modified)
        self.outport_combo = QComboBox()
        self.outport_combo.currentTextChanged.connect(self.setting_modified)
        self.populate_ports_combos()
        port_form.addRow(self.tr("Input port:"), self.inport_combo)
        port_form.addRow(self.tr("Output port:"), self.outport_combo)
        ports_grp.setLayout(port_form)

        main_layout = QVBoxLayout()
        main_layout.addWidget(ports_grp)
        self.setLayout(main_layout)
        self.load_settings()

    def populate_ports_combos(self):
        """Update ports combobox with ports names."""
        inports, outports = self.controller.list_midi_ports()
        self.inport_combo.clear()
        self.inport_combo.addItem("-")
        self.inport_combo.addItems(inports)
        self.outport_combo.clear()
        self.outport_combo.addItem("-")
        self.outport_combo.addItems(outports)

    def load_settings(self):
        """Load the settings from QSettings."""
        settings = QSettings()
        settings.beginGroup("midi")

        inports, outports = self.controller.list_midi_ports()
        inport = str(settings.value("inport", "-"))
        if inport in inports:
            self.inport_combo.setCurrentText(inport)
        else:
            self.inport_combo.setCurrentText("-")

        outport = str(settings.value("outport", "-"))
        if outport in outports:
            self.outport_combo.setCurrentText(outport)
        else:
            self.outport_combo.setCurrentText("-")

        settings.endGroup()

    def apply(self):
        """Apply (save) changes."""
        settings = QSettings()
        settings.beginGroup("midi")

        inport = self.inport_combo.currentText()
        if str(settings.value("inport", "-")) != inport:
            settings.setValue("inport", inport)

        outport = self.outport_combo.currentText()
        if str(settings.value("outport", "-")) != outport:
            settings.setValue("outport", outport)

        settings.endGroup()
