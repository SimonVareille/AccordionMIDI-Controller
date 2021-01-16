"""Definition of keyboard's DAO using MIDI protocol."""

import base64

from abc import abstractmethod
from ..keyboarddao import KeyboardDAO
from core.keyboard import Keyboard, Left96ButtonKeyboard, NoteData,\
    ProgramData, ControlData
from .mididatamididao import NoteDataMidiDAO, ProgramDataMidiDAO,\
    ControlDataMidiDAO
from core.arduino.io import midi_io


class KeyboardMidiDAO(KeyboardDAO):
    """Abstract class for representing a keyboard's DAO using MIDI."""

    @staticmethod
    @abstractmethod
    def from_bytes(data: bytearray) -> Keyboard:
        """
        Create a Keyboard from SysEx bytes.

        Parameters
        ----------
        data : bytearray, tuple or list of bytes
            Part of the SysEx message containing the keyboard.

        Returns
        -------
        Keyboard
            The created keyboard, or None if not a valid keyboard.

        """


class Left96ButtonKeyboardMidiDAO(KeyboardMidiDAO):
    """Represent a 96 left button keyboard's DAO using MIDI."""

    _keyboard_type = 0x02

    @staticmethod
    def from_bytes(data: bytearray) -> Left96ButtonKeyboard:
        """
        Create a Keyboard from SysEx bytes.

        Parameters
        ----------
        data : bytearray, tuple or list of bytes
            Part of the SysEx message containing the keyboard.

        Returns
        -------
        Left96ButtonKeyboard
            The created keyboard, or None if not a Left96ButtonKeyboard.

        """
        if data[0] == Left96ButtonKeyboardMidiDAO._keyboard_type:
            keyboard = Left96ButtonKeyboard()

            keyboard.name = bytes.decode(
                base64.b64decode(
                    data[1:data.index(0x00)]),
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

    @staticmethod
    def _to_bytes(kbd: Left96ButtonKeyboard) -> bytes:
        """
        Create a SysEx bytearray from a Left96ButtonKeyboard.

        Parameters
        ----------
        kbd : Left96ButtonKeyboard
            The keyboard to convert.

        Returns
        -------
        bytearray
            The created bytearray..

        """
        data = bytes([Left96ButtonKeyboardMidiDAO._keyboard_type])
        data += base64.b64encode(kbd.name.encode('utf-8'))
        data += bytes([0x00])

        keyboard_index = -1
        for i in range(96):
            midi_dao = None
            if isinstance(kbd.get_data(keyboard_index+2), NoteData):
                midi_dao = NoteDataMidiDAO
            elif isinstance(kbd.get_data(keyboard_index+2), ProgramData):
                midi_dao = ProgramDataMidiDAO
            elif isinstance(kbd.get_data(keyboard_index+2), ControlData):
                midi_dao = ControlDataMidiDAO
            # print(kbd.get_data(keyboard_index+2))
            data += midi_dao.to_bytes(
                    kbd.get_data(keyboard_index+2))
            keyboard_index = (keyboard_index + 16) % 95

        return data

    def send_set_current_keyboard(self, kbd: Left96ButtonKeyboard) -> None:
        """
        Set the given keyboard as current on remote.

        Parameters
        ----------
        kbd : Left96ButtonKeyboard
            The keyboard to set.

        Returns
        -------
        None.

        """
        data = bytes([0x02])
        data += self._to_bytes(kbd)
        midi_io.send_sysex(data)

    def send_store_keyboard(self, kbd: Left96ButtonKeyboard) -> None:
        """
        Store the given keyboard on remote.

        Parameters
        ----------
        kbd : Left96ButtonKeyboard
            The keyboard to store.

        Returns
        -------
        None.

        """
        data = bytes([0x01])
        data += self._to_bytes(kbd)
        midi_io.send_sysex(data)

    def send_delete_keyboard(self, kbd: Left96ButtonKeyboard) -> None:
        """
        Delete the given keyboard from remote.

        Parameters
        ----------
        kbd : Left96ButtonKeyboard
            The keyboard to delete.

        Returns
        -------
        None.

        """
        data = [0x04]
        data += bytes([self._keyboard_type])
        data += base64.b64encode(kbd.name.encode('utf-8'))
        data += bytes([0x00])
        midi_io.send_sysex(data)

    def send_rename_keyboard(self, kbd: Left96ButtonKeyboard,
                             new_name: str) -> None:
        """
        Rename the given keyboard on remote.

        Parameters
        ----------
        kbd : Left96ButtonKeyboard
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
        midi_io.send_sysex(data)
