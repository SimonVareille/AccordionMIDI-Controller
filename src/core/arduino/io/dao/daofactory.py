"""Factory for the DAOs."""
from abc import ABC, abstractmethod
from .keyboarddao import KeyboardDAO
from .midi import Left96ButtonKeyboardMidiDAO, Right81ButtonKeyboardMidiDAO


class DAOFactory(ABC):
    """Abstract class for the DAO's factory."""

    def __init__(self):
        pass

    @staticmethod
    @abstractmethod
    def get_left_96_button_keyboard_dao() -> KeyboardDAO:
        """
        Return the appropriate Left96ButtonKeyboard's DAO.

        Returns
        -------
        KeyboardDAO
            The Left96ButtonKeyboard's DAO.

        """

    @staticmethod
    @abstractmethod
    def get_right_81_button_keyboard_dao() -> KeyboardDAO:
        """
        Return the appropriate Right81ButtonKeyboard's DAO.

        Returns
        -------
        KeyboardDAO
            The Right81ButtonKeyboard's DAO.

        """


class MidiDAOFactory(DAOFactory):
    """Factory for creating KeyboardMidiDAO."""

    @staticmethod
    def get_left_96_button_keyboard_dao() -> Left96ButtonKeyboardMidiDAO:
        """
        Return the Left96ButtonKeyboardMidiDAO.

        Returns
        -------
        Left96ButtonKeyboardMidiDAO
            The Left96ButtonKeyboardMidiDAO.

        """
        return Left96ButtonKeyboardMidiDAO()

    @staticmethod
    def get_right_81_button_keyboard_dao() -> Right81ButtonKeyboardMidiDAO:
        """
        Return the Right81ButtonKeyboardMidiDAO.

        Returns
        -------
        Right81ButtonKeyboardMidiDAO
            The Right81ButtonKeyboardMidiDAO.

        """
        return Right81ButtonKeyboardMidiDAO()
