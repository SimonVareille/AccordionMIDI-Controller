"""Data associated with each keyboard key."""

__all__ = ["MidiData", "NoteData", "ProgramData", "ControlData"]

from abc import ABC


def _verify_channel(channel):
    if not 0 <= channel <= 15:
        raise ValueError(
            "channel must be between 0 and 15, got {}".format(channel))


def _verify_pitch(pitch):
    if not 0 <= pitch <= 127:
        raise ValueError(
            "pitch must be between 0 and 127, got {}".format(pitch))


def _verify_velocity(velocity):
    if not 0 <= velocity <= 127:
        raise ValueError(
            "velocity must be between 0 and 127, got {}".format(velocity))


def _verify_number(number):
    if not 0 <= number <= 127:
        raise ValueError(
            "number must be between 0 and 127, got {}".format(number))


def _verify_value(value):
    if not 0 <= value <= 127:
        raise ValueError(
            "value must be between 0 and 127, got {}".format(value))


class MidiData(ABC):  # pylint: disable=R0903
    """Abstract class for representing midi data."""


class NoteData(MidiData):
    """Represents a midi note.

    Attributes
    ----------
        :channel: The channel the note is linked to.

        :pitch: The pitch of the note.

        :velocity: The velocity of the note.
    """

    def __init__(self, channel=None, pitch=None, velocity=None):
        self._channel = None
        self._pitch = None
        self._velocity = None

        _verify_channel(channel)
        self._channel = channel

        _verify_pitch(pitch)
        self._pitch = pitch

        _verify_velocity(velocity)
        self._velocity = velocity

    @property
    def channel(self):
        # pylint: disable=C0116
        return self._channel

    @channel.setter
    def channel(self, channel):
        _verify_channel(channel)
        self._channel = channel

    @property
    def pitch(self):
        # pylint: disable=C0116
        return self._pitch

    @pitch.setter
    def pitch(self, pitch):
        _verify_pitch(pitch)
        self._pitch = pitch

    @property
    def velocity(self):
        # pylint: disable=C0116
        return self._velocity

    @velocity.setter
    def velocity(self, velocity):
        _verify_velocity(velocity)
        self._velocity = velocity

    def __repr__(self):
        return "NoteData(channel={!r}, pitch={!r}, velocity={!r})".format(
            self.channel, self.pitch, self.velocity)

class ProgramData(MidiData):
    """Represents a midi program signal.

    Attributes
    ----------
        :channel: The channel the signal is linked to.

        :number: The number of the midi program to apply.
    """

    def __init__(self, channel=None, number=None):
        self._channel = None
        self._number = None

        _verify_channel(channel)
        self._channel = channel

        _verify_number(number)
        self._number = number

    @property
    def channel(self):
        # pylint: disable=C0116
        return self._channel

    @channel.setter
    def channel(self, channel):
        _verify_channel(channel)
        self._channel = channel

    @property
    def number(self):
        # pylint: disable=C0116
        return self._number

    @number.setter
    def number(self, number):
        _verify_number(number)
        self._number = number

    def __repr__(self):
        return "ProgramData(channel={!r}, number={!r})".format(
            self.channel, self.number)


class ControlData(MidiData):
    """Represents a midi control change signal.

    Attributes
    ----------
        :channel: The channel the signal is linked to.

        :number: Number of the control change.

        :value: Value of the control change.
    """

    def __init__(self, channel=None, number=None, value=None):
        self._channel = None
        self._number = None
        self._value = None

        _verify_channel(channel)
        self._channel = channel

        _verify_number(number)
        self._number = number

        _verify_value(value)
        self._value = value

    @property
    def channel(self):
        # pylint: disable=C0116
        return self._channel

    @channel.setter
    def channel(self, channel):
        _verify_channel(channel)
        self._channel = channel

    @property
    def number(self):
        # pylint: disable=C0116
        return self._number

    @number.setter
    def number(self, number):
        _verify_number(number)
        self._number = number

    @property
    def value(self):
        # pylint: disable=C0116
        return self._value

    @value.setter
    def value(self, value):
        _verify_value(value)
        self._value = value

    def __repr__(self):
        return "ControlData(channel={!r}, number={!r}, value={!r})".format(
            self.channel, self.number, self.value)
