"""Definition of keyboards types."""

__all__ = ["Keyboard", "Left96ButtonKeyboard", "Right81ButtonKeyboard"]

from abc import ABC, abstractmethod

from .mididata import MidiData


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
        MidiData
            The wanted data or `None`.

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

    def __init__(self, name=None):
        super().__init__(name)
        self.keyboard = [None, ]*81

    def set_data(self, identifier, data):
        """
        Set the value of the data identified by `identifier`.

        Parameters
        ----------
        identifier : int
            index of the data to set (0-80).
        data : MidiData
            data to set.

        Returns
        -------
        None.

        """
        if not isinstance(data, MidiData):
            raise TypeError(
                "data must be of type MidiData (or subclasses), not {}"
                .format(type(data)))
        self.keyboard[identifier] = data

    def get_data(self, identifier):
        """
        Get the value of the data identified by `identifier`.

        Parameters
        ----------
        identifier : int
            index of the data to get (0-80).

        Returns
        -------
        MidiData
            The wanted data.

        """
        return self.keyboard[identifier]
