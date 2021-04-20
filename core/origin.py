"""Enumeration of the possible origin of each keyboard.

It's intended to differenciate keyboards comming from Arduino, from a local
database or from a remote DB.
"""

from enum import Enum


class Origin(Enum):
    """Enumeration of the possible keyboards's origin.

    The current possibilities are:
        - Arduino
    """

    Arduino = "Arduino"
