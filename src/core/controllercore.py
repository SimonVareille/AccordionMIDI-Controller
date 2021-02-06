"""Core of the controller.

Contains everything a UI should need.
"""
from typing import Dict, List

from .origin import Origin
from .arduino import Arduino, midiio
from .keyboard import Keyboard, MidiData


class ControllerCore:
    """Core of the controller."""

    def __init__(self):
        self.keyboards = dict()
        """Keep modified keyboards.
        dict[Origin, (Keyboard, History)]
        """
        self.arduino = Arduino()
        self.history = History()

    def rename_keyboard(self, kbd: Keyboard, new_name: str):
        """
        Rename the given keyboard.

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
        self.history.execute(RenameKeyboard(kbd, new_name))

    def set_keyboard_data(self, kbd: Keyboard, index, data: MidiData):
        """
        Set the keyboard's data identified by index.

        Parameters
        ----------
        kbd : Keyboard
            The keyboard to modify.
        index : undefined
            The index of the data to set.
        data : MidiData
            The data to set.

        Returns
        -------
        None.

        """
        self.history.execute(SetKeyboardData(kbd, index, data))

    def get_known_keyboards(self, origin: List[Origin] = None
                            ) -> Dict[Origin, List[Keyboard]]:
        """
        Return all known keyboards.

        If `origin` is specified, only keyboards from theses origins will be
        returned.

        Parameters
        ----------
        origin : List[Origin], optional
            The origins from which the keyoards will be returned. If None every
            known keyboard will be returned. The default is None.

        Returns
        -------
        Dict[Origin, List[Keyboard]]
            The keyboards, as a dict. The keys are origins, the values are
            list of Keyboards

        """
        result = dict()
        if origin is None or Origin.Arduino in origin:
            result[Origin.Arduino] = self.arduino.get_stored_keyboards()
            if self.arduino.get_current_left_keyboard():
                result[Origin.Arduino].append(
                    self.arduino.get_current_left_keyboard())
            if self.arduino.get_current_right_keyboard():
                result[Origin.Arduino].append(
                    self.arduino.get_current_right_keyboard())
        return result


class History():
    """Keep an history of every action performed."""

    def __init__(self):
        self._commands = list()
        self._redo = list()

    def execute(self, command):
        """
        Execute the specified command and store it in history.

        Parameters
        ----------
        command :
            The command to execute.

        Returns
        -------
        None.

        """
        self._commands.append(command)
        command.execute()
        self._redo.clear()

    def undo(self):
        """
        Undo the pevious command.

        Returns
        -------
        None.

        """
        command = self._commands.pop()
        self._redo.append(command)
        command.undo()

    def redo(self):
        """
        Redo the previously undoed command.

        Returns
        -------
        None.

        """
        command = self._redo.pop()
        self._commands.append(command)
        command.execute()


class RenameKeyboard():
    def __init__(self, kbd, new_name):
        self.last_name = kbd.name
        self.new_name = new_name
        self.kbd = kbd

    def execute(self):
        self.kbd.name = self.new_name

    def undo(self):
        self.kbd.name = self.last_name


class SetKeyboardData():
    def __init__(self, kbd, index, data):
        self.kbd = kbd
        self.index = index
        self.prev_data = self.kbd.get_data(index)
        self.data = data

    def execute(self):
        self.kbd.set_data(self.index, self.data)

    def undo(self):
        self.kbd.set_data(self.index, self.prev_data)