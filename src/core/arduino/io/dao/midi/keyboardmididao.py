"""Definition of keyboard's DAO using MIDI protocol."""

from abc import abstractmethod
from core.arduino.io.dao.KeyboardDAO import KeyboardDAO
from core.keyboard import Keyboard


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
            The created keyboard.

        """
