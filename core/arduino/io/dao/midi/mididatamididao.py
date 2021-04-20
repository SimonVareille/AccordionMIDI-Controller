"""Definition of MidiData's DAO using MIDI protocol."""

from abc import ABC, abstractmethod
from core.keyboard import MidiData, NoteData, ProgramData, ControlData


class MidiDataMidiDAO(ABC):
    """Abstract class for representing a MidiData's DAO using MIDI."""

    @staticmethod
    @abstractmethod
    def from_bytes(data: bytes) -> (MidiData, int):
        """
        Create a MidiData from SysEx bytes.

        Parameters
        ----------
        data : bytes
            Part of the SysEx message containing the MidiData.

        Returns
        -------
        MidiData
            The created MidiData, or None if not possible.
        int
            The number of bytes read.
        """

    @staticmethod
    @abstractmethod
    def to_bytes(data: MidiData) -> bytes:
        """
        Create a SysEx bytearray from MidiData.

        Parameters
        ----------
        data : MidiData
            The data to convert to SysEx bytearray.

        Returns
        -------
        bytes
            The created bytearray, or None if not possible.

        """


class NoteDataMidiDAO(MidiDataMidiDAO):
    """Represents a NoteData using midi."""

    @staticmethod
    def from_bytes(data: bytes) -> (NoteData, int):
        """
        Create a NoteData from SysEx bytes.

        Parameters
        ----------
        data : bytes
            Part of the SysEx message containing the NoteData.

        Returns
        -------
        NoteData
            The created NoteData or None if not possible.
        int
            The number of bytes read.

        """
        if data[0] == 0x01:
            channel = data[1]
            pitch = data[2]
            velocity = data[3]
            return NoteData(channel, pitch, velocity), 4
        return None, 0

    @staticmethod
    def to_bytes(data: NoteData) -> bytes:
        """
        Create a SysEx bytearray from NoteData.

        Parameters
        ----------
        data : NoteData
            The data to convert to SysEx bytearray.

        Returns
        -------
        bytes
            The created bytearray, or None if not possible.

        """
        return bytes([0x01, data.channel, data.pitch, data.velocity])


class ProgramDataMidiDAO(MidiDataMidiDAO):
    """Represents a ProgramData using midi."""

    @staticmethod
    def from_bytes(data: bytes) -> (ProgramData, int):
        """
        Create a ProgramData from SysEx bytes.

        Parameters
        ----------
        data : bytes
            Part of the SysEx message containing the ProgramData.

        Returns
        -------
        ProgramData
            The created ProgramData or None if not possible.
        int
            The number of bytes read.

        """
        if data[0] == 0x02:
            channel = data[1]
            program_number = data[2]
            return ProgramData(channel, program_number), 3
        return None, 0

    @staticmethod
    def to_bytes(data: ProgramData) -> bytes:
        """
        Create a SysEx bytearray from ProgramData.

        Parameters
        ----------
        data : ProgramData
            The data to convert to SysEx bytearray.

        Returns
        -------
        bytes
            The created bytearray, or None if not possible.

        """
        return bytes([0x02, data.channel, data.number])


class ControlDataMidiDAO(MidiDataMidiDAO):
    """Represents a ControlData using midi."""

    @staticmethod
    def from_bytes(data: bytes) -> (ControlData, int):
        """
        Create a ControlData from SysEx bytes.

        Parameters
        ----------
        data : bytes
            Part of the SysEx message containing the ControlData.

        Returns
        -------
        ControlData
            The created ControlData or None if not possible.
        int
            The number of bytes read.

        """
        if data[0] == 0x03:
            channel = data[1]
            number = data[2]
            value = data[3]
            return ControlData(channel, number, value), 4
        return None, 0

    @staticmethod
    def to_bytes(data: ControlData) -> bytes:
        """
        Create a SysEx bytearray from ControlData.

        Parameters
        ----------
        data : ControlData
            The data to convert to SysEx bytearray.

        Returns
        -------
        bytes
            The created bytearray, or None if not possible.

        """
        return bytes([0x03, data.channel, data.number, data.value])
