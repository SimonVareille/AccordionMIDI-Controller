"""Definition of keyboards types."""

__all__ = ["Keyboard", "Left96ButtonKeyboard", "Right81ButtonKeyboard"]

from abc import ABC, abstractmethod

from .mididata import MidiData


class Keyboard(ABC):
    """Abstract class for representing a keyboard."""

    def __init__(self, name: str = None):
        self.name = name

    @abstractmethod
    def set_data(self, identifier, data: MidiData):
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

    Format of this keyboard is as::

     96  95  94  93  92  91  90  89  88  87  86  85  84  83  82  81
       80  79  78  77  76  75  74  73  72  71  70  69  68  67  66  65
         64  63  62  61  60  59  58  57  56  55  54  53  52  51  50  49
           48  47  46  45  44  43  42  41  40  39  38  37  36  35  34  33
             32  31  30  29  28  27  26  25  24  23  22  21  20  19  18  17
               16  15  14  13  12  11  10   9   8   7   6   5   4   3   2   1

    """

    def __init__(self, name: str = None):
        super().__init__(name)
        self.keyboard = [None, ]*96

    def __repr__(self):
        return "Left96ButtonKeyboard(name={!r})".format(self.name)

    def __eq__(self, o):
        if self.name == o.name:
            for i in range(96):
                if self.keyboard[i] != o.keyboard[i]:
                    return False
            return True
        return False

    def set_data(self, identifier: int, data: MidiData):
        """
        Set the value of the data identified by `identifier`.

        Parameters
        ----------
        identifier : int
            index of the data to set (1-96).
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
        self.keyboard[identifier-1] = data

    def get_data(self, identifier: int):
        """
        Get the value of the data identified by `identifier`.

        Parameters
        ----------
        identifier : int
            index of the data to get (1-96).

        Returns
        -------
        MidiData
            The wanted data.

        """
        return self.keyboard[identifier-1]


class Right81ButtonKeyboard(Keyboard):
    """Right keyboard.

    Represent a right button keyboard of 81 button, as 4 rows of 16 buttons
    and 1 row of 17 buttons.

    Format of this keyboard is as::

        66  67  68  69  70  71  72  73  74  75  76  77  78  79  80  81
          50  51  52  53  54  55  56  57  58  59  60  61  62  63  64  65
        34  35  36  37  38  39  40  41  42  43  44  45  46  47  48  49
      17  18  19  20  21  22  23  24  25  26  27  28  29  30  31  32  33
         1   2   3   4   5   6   7   8   9  10  11  12  13  14  15  16
    """

    def __init__(self, name: str = None):
        super().__init__(name)
        self.keyboard = [None, ]*81

    def __repr__(self):
        return "Right81ButtonKeyboard(name={!r})".format(self.name)

    def __eq__(self, o):
        if self.name == o.name:
            for i in range(81):
                if self.keyboard[i] != o.keyboard[i]:
                    return False
            return True
        return False

    def set_data(self, identifier: int, data: MidiData):
        """
        Set the value of the data identified by `identifier`.

        Parameters
        ----------
        identifier : int
            index of the data to set (1-81).
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
        self.keyboard[identifier-1] = data

    def get_data(self, identifier: int):
        """
        Get the value of the data identified by `identifier`.

        Parameters
        ----------
        identifier : int
            index of the data to get (1-81).

        Returns
        -------
        MidiData
            The wanted data.

        """
        return self.keyboard[identifier-1]
