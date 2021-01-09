"""Definition of keyboard's DAO using MIDI protocol."""

from abc import abstractmethod
from core.arduino.io.dao.KeyboardDAO import KeyboardDAO
from core.keyboard import Keyboard, Left96ButtonKeyboard


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
