"""Factory for the DAOs."""
from abc import ABC, abstractmethod
from .keyboarddao import KeyboardDAO


class DAOFactory(ABC):
    """Abstract class for the DAO's factory."""

    def __init__(self):
        pass

    @abstractmethod
    def get_left_96_button_keyboard_dao(self) -> KeyboardDAO:
        """
        Return the appropriate Left96ButtonKeyboard's DAO.

        Returns
        -------
        KeyboardDAO
            The Left96ButtonKeyboard's DAO.

        """

    @abstractmethod
    def get_right_81_button_keyboard_dao(self) -> KeyboardDAO:
        """
        Return the appropriate Right81ButtonKeyboard's DAO.

        Returns
        -------
        KeyboardDAO
            The Right81ButtonKeyboard's DAO.

        """
