"""DAO for keyboards."""

from abc import ABC, abstractmethod
from core.keyboard import Keyboard


class KeyboardDAO(ABC):
    """Abstract class for keyboard DAO."""

    def __init__(self):
        pass

    @staticmethod
    @abstractmethod
    def send_fetch_keyboards():
        """
        Ask remote to send keyboards.

        Returns
        -------
        None.

        """

    @abstractmethod
    def send_set_current_keyboard(self, kbd: Keyboard) -> None:
        """
        Set the given keyboard as current on remote.

        Parameters
        ----------
        kbd : Keyboard
            The keyboard to set.

        Returns
        -------
        None.

        """

    @abstractmethod
    def send_store_keyboard(self, kbd: Keyboard) -> None:
        """
        Store the given keyboard on remote.

        Parameters
        ----------
        kbd : Keyboard
            The keyboard to store.

        Returns
        -------
        None.

        """

    @abstractmethod
    def send_delete_keyboard(self, kbd: Keyboard) -> None:
        """
        Delete the given keyboard from remote.

        Parameters
        ----------
        kbd : Keyboard
            The keyboard to delete.

        Returns
        -------
        None.

        """

    @abstractmethod
    def send_rename_keyboard(self, kbd: Keyboard, new_name: str) -> None:
        """
        Rename the given keyboard on remote.

        Parameters
        ----------
        kbd : Keyboard
            The keyboard to rename.
        new_name : str
            The new name.

        Returns
        -------
        None.

        """
