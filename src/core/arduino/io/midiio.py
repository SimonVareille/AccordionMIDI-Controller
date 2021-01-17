"""Communication between arduino and computer, through MIDI."""

import mido
from .dao.midi import Right81ButtonKeyboardMidiDAO, Left96ButtonKeyboardMidiDAO


outport = None
"""The output port.
Must be set with `connect` or `connect_output` functions.
"""

inport = None
"""The input port.
Must be set with `connect` or `connect_input` functions.
"""

callback = None
"""The function to call when a keyboard is received.
Must take two parameters:
    keyboard: The received keyboard.
    origin: The keyboard's origin (from EEPROM or RAM) as string.
"""


def _clear_inport_callback():
    """Clear the input port callback."""
    if inport:
        inport.callback = None


def close_inport():
    """Close the input port."""
    if inport:
        _clear_inport_callback()
        inport.close()


def close_outport():
    """Close the output port."""
    if outport:
        outport.close()


def close():
    """Close both input and output port."""
    close_inport()
    close_outport()


def connect(outport=None, inport=None):
    """
    Connect to the specified MIDI output and input ports, if not None.

    If `outport` or `inport` is None, connects to default MIDI port.

    Parameters
    ----------
    outport : str, optional
        Name of the MIDI ouput port. The default is None.
    inport : str, optional
        Nome of the MIDI input port. The default is None.

    Returns
    -------
    None.

    """
    connect_output(outport)
    connect_input(inport)


def connect_input(port=None):
    """
    Connect to the specified input port.

    If `port` is None, connects to default MIDI input port.

    Parameters
    ----------
    port : str, optional
        Name of the MIDI input port, one of `list_input_ports()`.
        The default is None.

    Returns
    -------
    None.

    Exceptions
    ----------
    If connection fails, raises an error.

    """
    global inport
    if not port:
        inport = mido.open_input(callback=_message_recv)
    else:
        inport = mido.open_input(port, callback=_message_recv)


def connect_output(port=None):
    """
    Connect to the specified output port.

    If `port` is None, connects to default MIDI output port.

    Parameters
    ----------
    port : str, optional
        Name of the MIDI output port, one of `list_output_ports()`.
        The default is None.

    Returns
    -------
    None.

    Exceptions
    ----------
    If connection fails, raises an error.

    """
    global outport
    if not port:
        outport = mido.open_output(autoreset=False)
    else:
        outport = mido.open_output(port, autoreset=False)


def list_input_ports():
    """
    List available input ports.

    Returns
    -------
    list of str
        List of available input ports names.

    """
    return mido.get_input_names()


def list_output_ports():
    """
    List available output ports.

    Returns
    -------
    list of str
        List of available output ports names.

    """
    return mido.get_output_names()


def input_ready():
    """
    Return True if the input is ready to use, False otherwise.

    Returns
    -------
    bool
        True if the input is ready, False otherwise.

    """
    if inport:
        return not inport.closed
    return False


def output_ready():
    """
    Return True if the output is ready to use, False otherwise.

    Returns
    -------
    bool
        True if the output is ready, False otherwise.

    """
    if outport:
        return not outport.closed
    return False


def _process_sysex(data):
    if data:
        if (data[0] & 1 or  # receiving a keyboard from EEPROM
           data[0] & 2):  # receiving a keyboard from RAM
            dao = None
            if data[1] == 0x01:
                dao = Right81ButtonKeyboardMidiDAO()
            elif data[1] == 0x02:
                dao = Left96ButtonKeyboardMidiDAO()

            if dao is not None:
                keyboard = dao.from_bytes(data[1:])
                callback(keyboard, data[0])


def send_sysex(data):
    """
    Send a sysex message with given data.

    Parameters
    ----------
    data : list of bytes
        Bytearray, list or tuple of bytes to send.

    Returns
    -------
    None.

    """
    msg = mido.Message("sysex", data=data)
    outport.send(msg)


def _message_recv(message):
    """Receive messages callback."""
    if message.type == "sysex":
        _process_sysex(message.data)
