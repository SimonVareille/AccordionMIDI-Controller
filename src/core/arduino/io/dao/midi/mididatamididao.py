"""Definition of MidiData's DAO using MIDI protocol."""

from abc import ABC, abstractmethod
from core.keyboard import MidiData, NoteData


class MidiDataMidiDAO(ABC):
    """Abstract class for representing a MidiData's DAO using MIDI."""

    @staticmethod
    @abstractmethod
    def from_bytes(data: bytearray) -> (MidiData, int):
        """
        Create a MidiData from SysEx bytes.

        Parameters
        ----------
        data : bytearray
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
    def to_bytes(data: MidiData) -> bytearray:
        """
        Create a SysEx bytearray from MidiData.

        Parameters
        ----------
        data : MidiData
            The data to convert to SysEx bytearray.

        Returns
        -------
        bytearray
            The created bytearray, or None if not possible.

        """


class NoteDataMidiDAO(MidiDataMidiDAO):
    """Represents a NoteData using midi."""

    @staticmethod
    def from_bytes(data: bytearray) -> (NoteData, int):
        """
        Create a NoteData from SysEx bytes.

        Parameters
        ----------
        data : bytearray
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
    def to_bytes(data: NoteData) -> bytearray:
        """
        Create a SysEx bytearray from NoteData.

        Parameters
        ----------
        data : NoteData
            The data to convert to SysEx bytearray.

        Returns
        -------
        bytearray
            The created bytearray, or None if not possible.

        """
        return bytearray([0x01, data.channel, data.pitch, data.velocity])
