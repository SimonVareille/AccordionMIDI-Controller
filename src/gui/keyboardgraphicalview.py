"""Holds graphical representation of keyboards."""
from copy import deepcopy

from PyQt5.QtCore import Qt, qFuzzyCompare, pyqtSignal
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsItem,\
    QGraphicsObject, QGraphicsSimpleTextItem, QDialog, QFormLayout,\
    QVBoxLayout, QHBoxLayout, QSpinBox, QDial, QDialogButtonBox, QComboBox,\
    QWidget
from PyQt5.QtGui import QPixmap, QPainter, QColor, QBrush
from PyQt5.QtSvg import QGraphicsSvgItem

from core.keyboard import NoteData, ProgramData, ControlData

import gui.resources


class KeyboardGraphicalView(QGraphicsView):
    """Represents a graphical keyboard."""

    zoom_changed = pyqtSignal()

    def __init__(self, parent, kbd_state):
        super().__init__(parent)

        self.keyboard_state = kbd_state

        self.setScene(QGraphicsScene(self))
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

        # Prepare background check-board pattern
        tile_pixmap = QPixmap(64, 64)
        tile_pixmap.fill(Qt.white)
        tile_painter = QPainter(tile_pixmap)
        color = QColor(220, 220, 220)
        tile_painter.fillRect(0, 0, 32, 32, color)
        tile_painter.fillRect(32, 32, 32, 32, color)
        tile_painter.end()
        # Apply background check-board pattern
        self.setBackgroundBrush(QBrush(tile_pixmap))

    def load_background_svg(self, filename):
        """
        Load the background svg image from filename.

        Parameters
        ----------
        filename : str
            The svg image to use.s

        Returns
        -------
        None.

        """
        self.svg_background = QGraphicsSvgItem(filename)

        self.svg_background.setFlags(QGraphicsItem.ItemClipsToShape)
        self.svg_background.setZValue(0)

        scene = self.scene()
        scene.addItem(self.svg_background)

    def zoom_factor(self):
        """
        Return the zoom factor.

        Returns
        -------
        qreal
            The zoom factor.

        """
        return self.transform().m11()

    def zoom_in(self):
        """
        Zoom inside by a factor of 2.

        Returns
        -------
        None.

        """
        self.zoom_by(2)

    def zoom_out(self):
        """
        Zoom outside by a factor of 2.

        Returns
        -------
        None.

        """
        self.zoom_by(0.5)

    def reset_zoom(self):
        """
        Reset zoom.

        Returns
        -------
        None.

        """
        if not qFuzzyCompare(self.zoomFactor(), 1):
            self.resetTransform()
            self.zoom_changed.emit()

    def zoom_by(self, factor):
        """
        Zoom by given factor.

        Parameters
        ----------
        factor : real
            Factor from wich to zoom.

        Returns
        -------
        None.

        """
        currentZoom = self.zoom_factor()
        if((factor < 1 and currentZoom < 0.1)
           or (factor > 1 and currentZoom > 10)):
            return
        self.scale(factor, factor)
        self.zoom_changed.emit()

    def wheelEvent(self, event):
        """
        Catch the wheel to zoom.

        Parameters
        ----------
        event : QWheelEvent
            The event sent by the wheel.

        Returns
        -------
        None.

        """
        self.zoom_by(pow(1.2, event.angleDelta().y() / 120))

    def drawBackground(self, painter, rect):
        """
        Draw the tiled background.

        Parameters
        ----------
        painter : QPainter
            QPainter on which to draw.
        rect : QRectF
            Unused.

        Returns
        -------
        None.

        """
        painter.save()
        painter.resetTransform()
        painter.drawTiledPixmap(self.viewport().rect(),
                                self.backgroundBrush().texture())
        painter.restore()

    def mm_to_px(self, x, y):
        return(x*0.03937008*self.logicalDpiX(),
               y*0.03937008*self.logicalDpiY())

    def px_to_mm(self, x, y):
        return(x/self.logicalDpiX()/25.4,
               y/self.logicalDpiY()/25.4)

    def mouseDoubleClickEvent(self, event):
        # items = self.items(self.mapToScene(event.pos()).toPoint())
        items = self.items(event.pos())
        for item in items:
            if isinstance(item, SvgButton):
                item.open_popup()
        super().mouseDoubleClickEvent(event)


class Right81ButtonKeyboardGraphicalView(KeyboardGraphicalView):
    """Represents a graphical right keyboard with 81 buttons."""

    def __init__(self, parent, kbd_state):
        super().__init__(parent, kbd_state)

        self.load_background_svg(":/right-81-buttons-svg/background.svg")
        self.load_buttons_svg(":/right-81-buttons-svg/button.svg")
        self.update()

    def load_buttons_svg(self, filename):
        """
        Load the buttons.

        Parameters
        ----------
        filename : str
            Name of the svg image to use.

        Returns
        -------
        None

        """
        self.buttons_svg = []
        scene = self.scene()

        def new_button(x, y, index):
            button = SvgButton(self, filename, index)
            button.midi_data_changed.connect(self.button_changed)
            button.setFlags(QGraphicsItem.ItemClipsToShape)
            # button.setCacheMode(QGraphicsItem.NoCache)
            button.setZValue(1)
            button.setPos(x, y)

            scene.addItem(button)
            return button

        button_gap = 67.47

        # First row
        for i in range(16):
            self.buttons_svg.append(new_button(
                75 + button_gap * i, 240, i+1))
        # Second row
        for i in range(17):
            self.buttons_svg.append(new_button(
                41.265 + button_gap * i, 185, i+17))
        # Third row
        for i in range(16):
            self.buttons_svg.append(new_button(
                75 + button_gap * i, 130, i+34))
        # Fourth row
        for i in range(16):
            self.buttons_svg.append(new_button(
                108.735 + button_gap * i, 75, i+50))
        # Fifth row
        for i in range(16):
            self.buttons_svg.append(new_button(
                75 + button_gap * i, 20, i+66))

    def update(self):
        for i in range(81):
            self.buttons_svg[i].set_midi_data(
                self.keyboard_state.keyboard.get_data(i+1))
            self.buttons_svg[i].update()

    def button_changed(self, index, midi_data):
        self.keyboard_state.set_keyboard_data(index, midi_data)


class SvgButton(QGraphicsObject):
    """Handle an svg button."""

    midi_data_changed = pyqtSignal(int, 'PyQt_PyObject')

    def __init__(self, parent, filename, index, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent = parent
        self.index = index
        self.midi_data = None
        self.show_midi_pitch = True
        self.button_svg = QGraphicsSvgItem(filename, self)

        self.button_svg.setTransformOriginPoint(
            self.button_svg.boundingRect().center())

        self.button_text = QGraphicsSimpleTextItem(self)

        font = self.button_text.font()
        font.setPointSize(18)
        self.button_text.setFont(font)
        self.center_text()

    def open_popup(self):
        dlg = ButtonDialog(self.parent)
        dlg.set_midi_data(self.midi_data)
        if dlg.exec_():
            self.midi_data = dlg.midi_data
            self.midi_data_changed.emit(self.index, self.midi_data)
        self.update()

    def set_midi_data(self, midi_data):
        self.midi_data = midi_data
        self.setToolTip(str(self.midi_data))

    def center_text(self):
        text_center = self.button_text.boundingRect().center()
        button_center = self.button_svg.boundingRect().center()
        self.button_text.setPos(button_center-text_center)

    def update(self, *args):
        if self.show_midi_pitch:
            if self.midi_data:
                self.button_text.setText(str(self.midi_data.pitch))
                self.center_text()
                self.setToolTip(str(self.midi_data))

    def boundingRect(self):
        return self.button_svg.boundingRect()

    def paint(self, painter, option, widget):
        pass


class ButtonDialog(QDialog):
    """Display a dialog used to modify properties of a button."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.midi_data = None

        self.setWindowTitle(self.tr("Edit Button"))
        self.setWindowModality(Qt.WindowModal)

        self.main_layout = QVBoxLayout()

        self.button_type = QComboBox()
        self.button_type.addItems([self.tr("Note"),
                                   self.tr("Program"),
                                   self.tr("Control")])
        self.button_type.currentIndexChanged.connect(self.button_type_changed)

        self.center = QWidget()  # NoteDataEditor()

        QBtn = QDialogButtonBox.Save | QDialogButtonBox.Cancel

        self.button_box = QDialogButtonBox(QBtn)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        self.main_layout.addWidget(self.button_type)
        self.main_layout.addWidget(self.center)
        self.main_layout.addWidget(self.button_box)
        self.setLayout(self.main_layout)

    def button_type_changed(self, index):
        print(index)

    def set_midi_data(self, midi_data):
        """
        Set the MIDI data to display (and to modify).

        Parameters
        ----------
        midi_data : MIDIData
            MIDI data.

        Returns
        -------
        None.

        """
        self.midi_data = midi_data
        # self.center.removeItem(self.center.itemAt(0))
        if isinstance(midi_data, NoteData):
            center = NoteDataEditor()
            # self.main_layout.replaceWidget(self.center, center)
            # self.main_layout.removeWidget(self.center)
            self.center.parentWidget().layout().replaceWidget(self.center, center)
            self.center = center
        elif isinstance(midi_data, ProgramData):
            self.center.addLayout(self._create_program_layout())
        elif isinstance(midi_data, ControlData):
            self.center.addLayout(self._create_control_layout())
        self.center.set_data(midi_data)

    def accept(self):
        """
        Save changes.

        Returns
        -------
        None.

        """
        self.midi_data = self.center.get_data()
        # if isinstance(self.midi_data, NoteData):
        #     self.midi_data.pitch = self.pitch_spin_box.value()
        #     self.midi_data.velocity = self.velocity_spin_box.value()
        #     self.midi_data.channel = self.channel_spin_box.value()
        super().accept()


class NoteDataEditor(QWidget):
    """Widget to edit a NoteData."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pitch_widget = PitchEditor()

        self.velocity_widget = VelocityEditor()

        self.channel_widget = ChannelEditor()

        self.form_layout = QFormLayout()
        self.form_layout.addRow(self.tr("Pitch:"), self.pitch_widget)
        self.form_layout.addRow(self.tr("Velocity:"), self.velocity_widget)
        self.form_layout.addRow(self.tr("Channel:"), self.channel_widget)
        self.setLayout(self.form_layout)

    def set_data(self, note_data):
        self.pitch_widget.set_value(note_data.pitch)
        self.velocity_widget.set_value(note_data.velocity)
        self.channel_widget.set_value(note_data.channel)

    def get_data(self):
        return NoteData(self.channel_widget.value(),
                        self.pitch_widget.value(),
                        self.velocity_widget.value())


class PitchEditor(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        pitch_layout = QHBoxLayout()
        self.pitch_spin_box = QSpinBox()
        self.pitch_spin_box.setRange(0, 127)

        # pitch_signature = KeySignatureSpinBox()

        pitch_layout.addWidget(self.pitch_spin_box)
        # pitch_layout.addWidget(pitch_signature)
        self.setLayout(pitch_layout)

    def set_value(self, value):
        self.pitch_spin_box.setValue(value)

    def value(self):
        return self.pitch_spin_box.value()


class VelocityEditor(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        velocity_layout = QHBoxLayout()
        self.velocity_spin_box = QSpinBox()
        self.velocity_spin_box.setRange(0, 127)
        velocity_dial = QDial()
        velocity_dial.setRange(self.velocity_spin_box.minimum(),
                               self.velocity_spin_box.maximum())
        velocity_dial.valueChanged.connect(self.velocity_spin_box.setValue)
        self.velocity_spin_box.valueChanged.connect(velocity_dial.setValue)
        velocity_layout.addWidget(self.velocity_spin_box)
        velocity_layout.addWidget(velocity_dial)
        self.setLayout(velocity_layout)

    def set_value(self, value):
        self.velocity_spin_box.setValue(value)

    def value(self):
        return self.velocity_spin_box.value()


class ChannelEditor(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        channel_layout = QHBoxLayout()
        self.channel_spin_box = QSpinBox()
        self.channel_spin_box.setRange(1, 16)
        channel_layout.addWidget(self.channel_spin_box)
        self.setLayout(channel_layout)

    def set_value(self, value):
        self.channel_spin_box.setValue(value)

    def value(self):
        return self.channel_spin_box.value()
