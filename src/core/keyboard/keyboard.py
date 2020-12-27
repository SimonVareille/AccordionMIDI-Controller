"""Definition of keyboards types."""

__all__ = ["Keyboard", "Left96ButtonKeyboard", "Right81ButtonKeyboard"]

from abc import ABC, abstractmethod


class Keyboard(ABC):
    """Abstract class for representing a keyboard."""

    def __init__(self, name=None):
        self.name = name

    @abstractmethod
    def set_data(self, identifier, data):
        """
        Set the value of the data identified by `identifier`.

        Parameters
        ----------
        identifier : undefined
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
        Get the value of the data identified by `identifier`.

        Parameters
        ----------
        identifier : undefined
            Identifier of the data.

        Returns
        -------
        The wanted data (of type MidiData) or `None`.

        """


class Left96ButtonKeyboard(Keyboard):
    """Left keyboard.

    Represent a left button keyboard of 96 button, as 6 rows of 16 buttons.
    """

    def set_data(self, identifier, data):
        """See Keyboard.setData."""

    def get_data(self, identifier):
        """See Keyboard.getData."""


class Right81ButtonKeyboard(Keyboard):
    """Right keyboard.

    Represent a right button keyboard of 81 button, as 4 rows of 16 buttons
    and 1 row of 17 buttons.
    """

    def set_data(self, identifier, data):
        """See Keyboard.setData."""

    def get_data(self, identifier):
        """See Keyboard.getData."""
