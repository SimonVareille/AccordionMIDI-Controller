"""Definition of keyboard's DAO using MIDI protocol."""

import base64

from abc import abstractmethod
from core.arduino.io.dao.KeyboardDAO import KeyboardDAO
from core.keyboard import Keyboard, Left96ButtonKeyboard
from .mididatamididao import NoteDataMidiDAO, ProgramDataMidiDAO,\
    ControlDataMidiDAO


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
        if data[0] == 0x02:
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
