"""Handle the consistency with the Arduino's state."""
import threading
from typing import List
from copy import deepcopy
from core.keyboard import Keyboard, Left96ButtonKeyboard, Right81ButtonKeyboard
from .io import midiio
from .io.dao.daofactory import MidiDAOFactory

# pylint: disable=C0123


class Arduino:
    """Reflect the Arduino current state and manage connexions."""

    def __init__(self):
        self.stored_keyboards = []
        self.current_left_keyboard = None
        self.current_right_keyboard = None
        self.stored_lock = threading.Lock()
        self.left_lock = threading.Lock()
        self.right_lock = threading.Lock()
        self.dao_factory = MidiDAOFactory()
        midiio.callback = self._add_keyboard_internal

    def _add_keyboard_internal(self, kbd: Keyboard, origin: str):
        """
        Add a keyboard to the list of stored keyboard.

        Parameters
        ----------
        kbd : Keyboard
            The keyboard to add.
        origin : str
            The keyboard's origin ("RAM" or "EEPROM")

        Returns
        -------
        None.

        """
        if origin == "EEPROM":
            with self.stored_lock:
                if kbd not in self.stored_keyboards:
                    self.stored_keyboards.append(kbd)
        elif origin == "RAM":
            if(isinstance(kbd, Left96ButtonKeyboard) and
               self.current_left_keyboard != kbd):
                with self.left_lock:
                    self.current_left_keyboard = kbd
            elif(isinstance(kbd, Right81ButtonKeyboard) and
                 self.current_right_keyboard != kbd):
                with self.right_lock:
                    self.current_right_keyboard = kbd

    def get_stored_keyboards(self) -> List[Keyboard]:
        """
        Return a deep copy of the stored keyboard.

        Returns
        -------
        List[Keyboard]
            The stored keyboards.

        """
        with self.stored_lock:
            return deepcopy(self.stored_keyboards)

    def get_current_left_keyboard(self) -> Keyboard:
        """
        Return a deep copy of the current left keyboard.

        Returns
        -------
        Keyboard
            The current left keyboard.

        """
        with self.left_lock:
            return deepcopy(self.current_left_keyboard)

    def get_current_right_keyboard(self) -> Keyboard:
        """
        Return a deep copy of the current right keyboard.

        Returns
        -------
        Keyboard
            The current right keyboard.

        """
        with self.right_lock:
            return deepcopy(self.current_right_keyboard)

    def fetch_keyboards(self):
        """
        Ask remote to send known keyboards.

        Returns
        -------
        None.

        """
        with self.stored_lock:
            self.stored_keyboards.clear()
        self.dao_factory.get_generic_keyboard_dao().send_fetch_keyboards()

    def set_current_keyboard(self, kbd: Keyboard):
        """
        Set the given keyboard as current.

        Parameters
        ----------
        kbd : Keyboard
            The keyboard to set.

        Returns
        -------
        None.

        """
        keyboard_dao = None
        if isinstance(kbd, Left96ButtonKeyboard):
            keyboard_dao = self.dao_factory.get_left_96_button_keyboard_dao()
            with self.left_lock:
                self.current_left_keyboard = kbd
        elif isinstance(kbd, Right81ButtonKeyboard):
            keyboard_dao = self.dao_factory.get_right_81_button_keyboard_dao()
            with self.right_lock:
                self.current_right_keyboard = kbd

        keyboard_dao.send_set_current_keyboard(kbd)

    def store_keyboard(self, kbd: Keyboard):
        """
        Store the given keyboard.

        Parameters
        ----------
        kbd : Keyboard
            The keyboard to store.

        Returns
        -------
        None.

        """
        keyboard_dao = None
        if isinstance(kbd, Left96ButtonKeyboard):
            keyboard_dao = self.dao_factory.get_left_96_button_keyboard_dao()
        elif isinstance(kbd, Right81ButtonKeyboard):
            keyboard_dao = self.dao_factory.get_right_81_button_keyboard_dao()

        keyboard_dao.send_store_keyboard(kbd)

        with self.stored_lock:
            for std_kb in self.stored_keyboards:
                if type(std_kb) == type(kbd) and std_kb.name == kbd.name:
                    self.stored_keyboards.remove(std_kb)
                    break

            self.stored_keyboards.append(kbd)

    def delete_keyboard(self, kbd: Keyboard):
        """
        Delete the given keyboard.

        Parameters
        ----------
        kbd : Keyboard
            The keyboard to delete.

        Returns
        -------
        None.

        """
        keyboard_dao = None
        if isinstance(kbd, Left96ButtonKeyboard):
            keyboard_dao = self.dao_factory.get_left_96_button_keyboard_dao()
        elif isinstance(kbd, Right81ButtonKeyboard):
            keyboard_dao = self.dao_factory.get_right_81_button_keyboard_dao()

        keyboard_dao.send_delete_keyboard(kbd)

        with self.stored_lock:
            for std_kb in self.stored_keyboards:
                if type(std_kb) == type(kbd) and std_kb.name == kbd.name:
                    self.stored_keyboards.remove(std_kb)
                    break

    def rename_keyboard(self, kbd: Keyboard, new_name: str):
        """
        Rename the given keyboard.

        Parameters
        ----------
        kbd : Keyboard
            The keyboard to rename..
        new_name : str
            The new name.

        Returns
        -------
        None.

        """
        keyboard_dao = None
        if isinstance(kbd, Left96ButtonKeyboard):
            keyboard_dao = self.dao_factory.get_left_96_button_keyboard_dao()
        elif isinstance(kbd, Right81ButtonKeyboard):
            keyboard_dao = self.dao_factory.get_right_81_button_keyboard_dao()

        keyboard_dao.send_rename_keyboard(kbd, new_name)

        with self.stored_lock:
            for std_kb in self.stored_keyboards:
                if type(std_kb) == type(kbd) and std_kb.name == kbd.name:
                    std_kb.name = new_name
                    break
