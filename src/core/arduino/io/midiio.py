"""Communication between arduino and computer, through MIDI."""

__all__ = ["MidiIO"]

import mido


class MidiIO:
    """Handle MIDI input and output."""

    def __init__(self):
        super().__init__()
        self.outport = None
        self.inport = None

    def __del__(self):
        """Ensure proper deletion of instance."""
        self.close_inport()
        self.close_outport()

    def _clear_inport_callback(self):
        """Clear the input port callback."""
        if self.inport:
            self.inport.callback = None

    def set_callback(self, callback):
        """
        Set the callback used when a new keyboard is created.

        Parameters
        ----------
        callback :
            A callback function to be called when a new keyboard is created.
            The function should take one argument (the keyboard).

        Returns
        -------
        None.

        """
        self.keyboard_callback = callback

    def close_inport(self):
        """Close the input port."""
        if self.inport:
            self._clear_inport_callback()
            self.inport.close()

    def close_outport(self):
        """Close the output port."""
        if self.outport:
            self.outport.close()

    def close(self):
        """Close both input and output port."""
        self.close_inport()
        self.close_outport()

    def connect(self, outport=None, inport=None):
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
        self.connect_output(outport)
        self.connect_input(inport)

    def connect_input(self, port=None):
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
        if not port:
            self.inport = mido.open_input(callback=self._message_recv)
        else:
            self.inport = mido.open_input(port,
                                          callback=self._message_recv)

    def connect_output(self, port=None):
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
        if not port:
            self.outport = mido.open_output(autoreset=False)
        else:
            self.outport = mido.open_output(port, autoreset=False)

    @staticmethod
    def list_input_ports():
        """
        List available input ports.

        Returns
        -------
        list of str
            List of available input ports names.

        """
        return mido.get_input_names()

    @staticmethod
    def list_output_ports():
        """
        List available output ports.

        Returns
        -------
        list of str
            List of available output ports names.

        """
        return mido.get_output_names()

    def input_ready(self):
        """
        Return True if the input is ready to use, False otherwise.

        Returns
        -------
        bool
            True if the input is ready, False otherwise.

        """
        if self.inport:
            return not self.inport.closed
        return False

    def output_ready(self):
        """
        Return True if the output is ready to use, False otherwise.

        Returns
        -------
        bool
            True if the output is ready, False otherwise.

        """
        if self.outport:
            return not self.outport.closed
        return False

    def _process_sysex(self, data):
        print(data)
        if data:
            if data[0] == 1:  # receiving a keyboard
                daoFactory = MidiDAOFactory()
                dao = None
                if data[2] == 0:
                    dao = daoFactory.get_right_81_button_keyboard_dao()
                elif data[2] == 1:
                    dao = daoFactory.get_left_96_button_keyboard_dao()

                if dao is not None:
                    keyboard = dao.from_bytes(data[1:])
                    self.keyboard_callback(keyboard)

    def send_sysex(self, data):
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
        self.outport.send(msg)

    def _message_recv(self, message):
        """Receive messages callback."""
        if message.type == "sysex":
            self._process_sysex(message.data)
