"""Definition of keyboards types."""

__all__ = ["Keyboard", "LeftKeyboard", "RightKeyboard"]

from abc import ABC, abstractmethod


class Keyboard(ABC):
    """Abstract class for representing a keyboard."""

    def __init__(self, name=None):
        self.name = name

    @abstractmethod
    def set_data(self, identifier, data):
        """
        Set the value of the data identified by `id`.

        Parameters
        ----------
        identifier : int
            Identifier of the data.
        data : MidiData
            Value of the data.

        Returns
        -------
        None.

        """

    @abstractmethod
    def get_data(self, identifier):
        """
        Get the value of the data identified by `id`.

        Parameters
        ----------
        identifier : int
            Identifier of the data.

        Returns
        -------
        The wanted data (of type MidiData) or `None`.

        """


class LeftKeyboard(Keyboard):
    """Left keyboard representation."""

    def set_data(self, identifier, data):
        """See Keyboard.setData."""

    def get_data(self, identifier):
        """See Keyboard.getData."""


class RightKeyboard(Keyboard):
    """Right keyboard representation."""

    def set_data(self, identifier, data):
        """See Keyboard.setData."""

    def get_data(self, identifier):
        """See Keyboard.getData."""
