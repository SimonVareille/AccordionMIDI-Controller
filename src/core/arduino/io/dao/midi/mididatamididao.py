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
            The created MidiData and the , or None if not possible.
        int
            The number of bytes read.
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
