"""Definition of keyboard's DAO using MIDI protocol."""

import base64

from abc import abstractmethod
import core.arduino.io.midiio as midiio
from core.keyboard import Keyboard, Left96ButtonKeyboard,\
    Right81ButtonKeyboard, NoteData, ProgramData, ControlData
from ..keyboarddao import KeyboardDAO
from .mididatamididao import NoteDataMidiDAO, ProgramDataMidiDAO,\
    ControlDataMidiDAO


class KeyboardMidiDAO(KeyboardDAO):
    """Abstract class for representing a keyboard's DAO using MIDI."""

    def __init__(self):
        super().__init__()
        self._keyboard_type = None

    @abstractmethod
    def from_bytes(self, data: bytes) -> Keyboard:
        """
        Create a Keyboard from SysEx bytes.

        Parameters
        ----------
        data : bytes, tuple or list of bytes
            Part of the SysEx message containing the keyboard.

        Returns
        -------
        Keyboard
            The created keyboard, or None if not a valid keyboard.

        """

    def _to_bytes(self, kbd: Keyboard) -> bytes:
        """
        Create a SysEx bytearray from a Keyboard.

        Parameters
        ----------
        kbd : Keyboard
            The keyboard to convert.

        Returns
        -------
        bytes
            The created bytearray.

        """

    @staticmethod
    def send_fetch_keyboards():
        """
        Ask remote to send keyboards.

        Returns
        -------
        None.

        """
        midiio.send_sysex([0x00])

    def send_set_current_keyboard(self, kbd: Keyboard) -> None:
        """
        Set the given keyboard as current on remote.

        Parameters
        ----------
        kbd : Keyboard
            The keyboard to set.

        Returns
        -------
        None.

        """
        data = bytes([0x02])
        data += self._to_bytes(kbd)
        midiio.send_sysex(data)

    def send_store_keyboard(self, kbd: Keyboard) -> None:
        """
        Store the given keyboard on remote.

        Parameters
        ----------
        kbd : Keyboard
            The keyboard to store.

        Returns
        -------
        None.

        """
        data = bytes([0x01])
        data += self._to_bytes(kbd)
        midiio.send_sysex(data)

    def send_delete_keyboard(self, kbd: Keyboard) -> None:
        """
        Delete the given keyboard from remote.

        Parameters
        ----------
        kbd : Keyboard
            The keyboard to delete.

        Returns
        -------
        None.

        """
        data = [0x04]
        data += bytes([self._keyboard_type])
        data += base64.b64encode(kbd.name.encode('utf-8'))
        data += bytes([0x00])
        midiio.send_sysex(data)

    def send_rename_keyboard(self, kbd: Keyboard,
                             new_name: str) -> None:
        """
        Rename the given keyboard on remote.

        Parameters
        ----------
        kbd : Keyboard
            The keyboard to rename.
        new_name : str
            The new name.

        Returns
        -------
        None.

        """
        data = [0x08]
        data += bytes([self._keyboard_type])
        data += base64.b64encode(kbd.name.encode('utf-8'))
        data += bytes([0x00])
        data += base64.b64encode(new_name.encode('utf-8'))
        data += bytes([0x00])
        midiio.send_sysex(data)


class Left96ButtonKeyboardMidiDAO(KeyboardMidiDAO):
    """Represent a 96 left button keyboard's DAO using MIDI."""

    def __init__(self):
        super().__init__()
        self._keyboard_type = 0x02

    def from_bytes(self, data: bytes) -> Left96ButtonKeyboard:
        """
        Create a Keyboard from SysEx bytes.

        Parameters
        ----------
        data : bytes, tuple or list of bytes
            Part of the SysEx message containing the keyboard.

        Returns
        -------
        Left96ButtonKeyboard
            The created keyboard, or None if not a Left96ButtonKeyboard.

        """
        if data[0] == self._keyboard_type:
            keyboard = Left96ButtonKeyboard()

            keyboard.name = bytes.decode(
                base64.b64decode(
                    bytes(data[1:data.index(0x00)])),
                'utf-8')

            data_index = data.index(0x00)+1

            # Index of the current key of the Left96ButtonKeyboard
            keyboard_index = -1
            for _ in range(96):
                data_midi_dao = None
                if data[data_index] == 0x01:
                    data_midi_dao = NoteDataMidiDAO
                elif data[data_index] == 0x02:
                    data_midi_dao = ProgramDataMidiDAO
                elif data[data_index] == 0x03:
                    data_midi_dao = ControlDataMidiDAO

                midi_data, skip = data_midi_dao.from_bytes(data[data_index:])

                keyboard.set_data(keyboard_index+2, midi_data)

                keyboard_index = (keyboard_index + 16) % 95

                data_index += skip
            return keyboard
        return None

    def _to_bytes(self, kbd: Left96ButtonKeyboard) -> bytes:
        """
        Create a SysEx bytearray from a Left96ButtonKeyboard.

        Parameters
        ----------
        kbd : Left96ButtonKeyboard
            The keyboard to convert.

        Returns
        -------
        bytes
            The created bytearray.

        """
        data = bytes([self._keyboard_type])
        data += base64.b64encode(kbd.name.encode('utf-8'))
        data += bytes([0x00])

        keyboard_index = -1
        for _ in range(96):
            midi_dao = None
            if isinstance(kbd.get_data(keyboard_index+2), NoteData):
                midi_dao = NoteDataMidiDAO
            elif isinstance(kbd.get_data(keyboard_index+2), ProgramData):
                midi_dao = ProgramDataMidiDAO
            elif isinstance(kbd.get_data(keyboard_index+2), ControlData):
                midi_dao = ControlDataMidiDAO
            data += midi_dao.to_bytes(
                    kbd.get_data(keyboard_index+2))
            keyboard_index = (keyboard_index + 16) % 95

        return data


class Right81ButtonKeyboardMidiDAO(KeyboardMidiDAO):
    """Represent a 81 rigt button keyboard's DAO using MIDI."""

    def __init__(self):
        super().__init__()
        self._keyboard_type = 0x01

    @staticmethod
    def _get_midi_data(data, data_index):
        data_midi_dao = None
        if data[data_index] == 0x01:
            data_midi_dao = NoteDataMidiDAO
        elif data[data_index] == 0x02:
            data_midi_dao = ProgramDataMidiDAO
        elif data[data_index] == 0x03:
            data_midi_dao = ControlDataMidiDAO
        return data_midi_dao.from_bytes(data[data_index:])

    @staticmethod
    def _get_midi_data_dao(midi_data):
        midi_dao = None
        if isinstance(midi_data, NoteData):
            midi_dao = NoteDataMidiDAO
        elif isinstance(midi_data, ProgramData):
            midi_dao = ProgramDataMidiDAO
        elif isinstance(midi_data, ControlData):
            midi_dao = ControlDataMidiDAO
        return midi_dao

    def from_bytes(self, data: bytes) -> Right81ButtonKeyboard:
        """
        Create a Keyboard from SysEx bytes.

        Parameters
        ----------
        data : bytes, tuple or list of bytes
            Part of the SysEx message containing the keyboard.

        Returns
        -------
        Right81ButtonKeyboard
            The created keyboard, or None if not a Right81ButtonKeyboard.

        """
        if data[0] == self._keyboard_type:
            keyboard = Right81ButtonKeyboard()

            keyboard.name = bytes.decode(
                base64.b64decode(
                    bytes(data[1:data.index(0x00)])),
                'utf-8')

            data_index = data.index(0x00)+1

            for i in range(5):
                midi_data, skip = self._get_midi_data(data, data_index)
                keyboard.set_data((66, 17, 34, 50, 67)[i], midi_data)
                data_index += skip

            for j in range(14):
                for i in range(5):
                    keyboard_index = (1, 18, 35, 51, 68)[i]+j
                    midi_data, skip = self._get_midi_data(data, data_index)
                    keyboard.set_data(keyboard_index, midi_data)
                    data_index += skip

            for i in range(6):
                midi_data, skip = self._get_midi_data(data, data_index)
                keyboard.set_data((15, 32, 49, 65, 16, 33)[i], midi_data)
                data_index += skip
            return keyboard
        return None

    def _to_bytes(self, kbd: Right81ButtonKeyboard) -> bytes:
        """
        Create a SysEx bytearray from a Right81ButtonKeyboard.

        Parameters
        ----------
        kbd : Right81ButtonKeyboard
            The keyboard to convert.

        Returns
        -------
        bytes
            The created bytearray.

        """
        data = bytes([self._keyboard_type])
        data += base64.b64encode(kbd.name.encode('utf-8'))
        data += bytes([0x00])

        for i in range(5):
            midi_data = kbd.get_data((66, 17, 34, 50, 67)[i])
            midi_dao = self._get_midi_data_dao(midi_data)
            data += midi_dao.to_bytes(midi_data)

        for j in range(14):
            for i in range(5):
                keyboard_index = (1, 18, 35, 51, 68)[i]+j
                midi_data = kbd.get_data(keyboard_index)
                midi_dao = self._get_midi_data_dao(midi_data)
                data += midi_dao.to_bytes(midi_data)

        for i in range(6):
            midi_data = kbd.get_data((15, 32, 49, 65, 16, 33)[i])
            midi_dao = self._get_midi_data_dao(midi_data)
            data += midi_dao.to_bytes(midi_data)

        return data
