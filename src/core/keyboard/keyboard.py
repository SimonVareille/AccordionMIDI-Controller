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

    Format of this keyboard is as:
    |    66  67  68  69  70  71  72  73  74  75  76  77  78  79  80  81
    |      50  51  52  53  54  55  56  57  58  59  60  61  62  63  64  65
    |    34  35  36  37  38  39  40  41  42  43  44  45  46  47  48  49
    |  17  18  19  20  21  22  23  24  25  26  27  28  29  30  31  32  33
    |     1   2   3   4   5   6   7   8   9  10  11  12  13   14  15  16
    """

    def __init__(self, name=None):
        super().__init__(name)
        self.keyboard = [None, ]*81

    def __repr__(self):
        return "Right81ButtonKeyboard(name={!r})".format(self.name)

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
