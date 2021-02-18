"""Store keybords in JSON format."""

import json
from typing import Dict

from core.keyboard import Keyboard, Left96ButtonKeyboard,\
    Right81ButtonKeyboard, MidiData, NoteData, ProgramData, ControlData


class JsonFile:
    """Access keyboard's data stored in JSON file."""

    def __init__(self, filename: str = ""):
        self.filename = filename

    def load(self) -> Keyboard:
        """
        Read the file containing the keyboard in JSON format.

        Returns
        -------
        Keyboard
            The loaded keyboard.

        """
        with open(self.filename, "r") as file:
            try:
                return keyboard_from_dict(json.load(file))
            except KeyError as err:
                raise ValueError(
                    f"The file '{self.filename}' doesn't contain a valid "
                    "keyboard.") from err

    def save(self, kbd: Keyboard):
        """
        Write into the file the keyboard in JSON format.

        Parameters
        ----------
        kbd : Keyboard
            The keyboard to save.

        Returns
        -------
        None.

        """
        with open(self.filename, "w") as file:
            json.dump(keyboard_to_dict(kbd), file)


def keyboard_to_dict(kbd: Keyboard) -> Dict:
    """
    Convert a Keyboard to a dict.

    Parameters
    ----------
    kbd : Keyboard
        The keyboard to convert.

    Returns
    -------
    Dict
        The generated dict.

    """
    d = {}
    if isinstance(kbd, Left96ButtonKeyboard):
        d['__type__'] = "Left96ButtonKeyboard"
    elif isinstance(kbd, Right81ButtonKeyboard):
        d['__type__'] = "Right81ButtonKeyboard"
    d['name'] = kbd.name
    d['data'] = [mididata_to_dict(data) for data in kbd.keyboard]
    return d


def mididata_to_dict(data: MidiData) -> Dict:
    """
    Convert a MidiData to a dict.

    Parameters
    ----------
    data : MidiData
        The MidiData to convert.

    Returns
    -------
    Dict
        The generated dict.

    """
    d = {}
    if isinstance(data, NoteData):
        d['__type__'] = "NoteData"
        d['channel'] = data.channel
        d['pitch'] = data.pitch
        d['velocity'] = data.velocity
    elif isinstance(data, ProgramData):
        d['__type__'] = "ProgramData"
        d['channel'] = data.channel
        d['number'] = data.number
    elif isinstance(data, ControlData):
        d['__type__'] = "ControlData"
        d['channel'] = data.channel
        d['number'] = data.number
        d['value'] = data.value
    return d


def keyboard_from_dict(d: Dict) -> Keyboard:
    """
    Convert a dict to a Keyboard.

    Parameters
    ----------
    d : Dict
        The dict to convert.

    Raises
    ------
    ValueError
        In case the given Keyboard type is not known.

    Returns
    -------
    Keyboard
        The generated Keyboard.

    """
    if d['__type__'] == 'Left96ButtonKeyboard':
        kbd = Left96ButtonKeyboard()
    elif d['__type__'] == 'Right81ButtonKeyboard':
        kbd = Right81ButtonKeyboard()
    else:
        raise ValueError(f"Keyboard type '{d['__type__']}' unknown.")
    kbd.name = d['name']
    kbd.keyboard = [mididata_from_dict(data) for data in d['data']]
    return kbd


def mididata_from_dict(d: Dict) -> MidiData:
    """
    Convert a dict to a MidiData.

    Parameters
    ----------
    d : Dict
        The dict to convert.

    Raises
    ------
    ValueError
        In case the given MidiData type is not known.

    Returns
    -------
    MidiData
        The generated MidiData.

    """
    if d['__type__'] == 'NoteData':
        data = NoteData(d['channel'], d['pitch'], d['velocity'])
    elif d['__type__'] == 'ProgramData':
        data = ProgramData(d['channel'], d['number'])
    elif d['__type__'] == 'ControlData':
        data = ControlData(d['channel'], d['number'], d['value'])
    else:
        raise ValueError(f"MidiData type '{d['__type__']}' unknown.")
    return data
