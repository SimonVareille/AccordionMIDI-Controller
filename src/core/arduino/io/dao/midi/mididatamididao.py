"""Definition of MidiData's DAO using MIDI protocol."""

from abc import ABC, abstractmethod
from core.keyboard import MidiData


class MidiDataMidiDAO(ABC):
    """Abstract class for representing a MidiData's DAO using MIDI."""

    @staticmethod
    @abstractmethod
    def from_bytes(data: bytearray) -> MidiData:
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

        """
