"""Communication between arduino and computer, through MIDI."""

import threading
from typing import List
from collections import deque
import mido
from .dao.midi import Right81ButtonKeyboardMidiDAO, Left96ButtonKeyboardMidiDAO

# pylint: disable=C0103

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

_sysex_queue = deque()
_sysex_lock = threading.Lock()


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


def connect(outprt: str = None, inprt: str = None):
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
    connect_output(outprt)
    connect_input(inprt)


def connect_input(port: str = None):
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
    # pylint: disable=W0603
    global inport
    if not port:
        inport = mido.open_input(callback=_message_recv)
    else:
        inport = mido.open_input(port, callback=_message_recv)


def connect_output(port: str = None):
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
    # pylint: disable=W0603
    global outport
    if not port:
        outport = mido.open_output(autoreset=False)
    else:
        outport = mido.open_output(port, autoreset=False)


def list_input_ports() -> List[str]:
    """
    List available input ports.

    Returns
    -------
    list of str
        List of available input ports names.

    """
    return mido.get_input_names()


def list_output_ports() -> List[str]:
    """
    List available output ports.

    Returns
    -------
    list of str
        List of available output ports names.

    """
    return mido.get_output_names()


def input_ready() -> bool:
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


def output_ready() -> bool:
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


def _process_sysex(data: bytes):
    if data:
        if (data[0] == 1 or  # receiving a keyboard from EEPROM
           data[0] == 2):  # receiving a keyboard from RAM
            dao = None
            if data[1] == 0x01:
                dao = Right81ButtonKeyboardMidiDAO()
            elif data[1] == 0x02:
                dao = Left96ButtonKeyboardMidiDAO()

            if dao is not None:
                keyboard = dao.from_bytes(data[1:])
                # pylint: disable=E1102
                callback(keyboard, "EEPROM" if data[0] == 1 else "RAM")
        elif data[0] == 0x0F:  # receiving confirmation for sending a SysEx
            with _sysex_lock:
                if len(_sysex_queue):
                    outport.send(_sysex_queue.popleft())
                    if len(_sysex_queue):
                        _send_pre_sysex()


def send_direct_sysex(data: bytes):
    """
    Send a sysex message with given data.

    The SysEx is immediatly sent. To warn the receiver that a SysEx will be
    sent, use send_sysex() instead.

    Parameters
    ----------
    data : list of bytes
        Bytearray, list or tuple of bytes to send.

    Returns
    -------
    None.

    """
    msg = mido.Message("sysex", data=bytes([0x7d]) + data)
    outport.send(msg)


def send_sysex(data: bytes):
    """
    Send a sysex message with given data.

    Warn the receiver that a SysEx will be sent.
    If a previous SysEx is already in the send queue, wait for this SysEx to
    be sent.

    Parameters
    ----------
    data : list of bytes
        Bytearray, list or tuple of bytes to send.

    Returns
    -------
    None.

    """
    msg = mido.Message("sysex", data=bytes([0x7d]) + data)
    with _sysex_lock:
        _sysex_queue.append(msg)
        if len(_sysex_queue) == 1:
            _send_pre_sysex()


def _send_pre_sysex():
    """Warn the receiver that a long SysEx will be sent."""
    send_direct_sysex(bytes([0x0f]))


def _message_recv(message: mido.Message):
    """Receive messages callback."""
    if message.type == "sysex":
        if message.data and message.data[0] == 0x7d:
            _process_sysex(message.data[1:])
