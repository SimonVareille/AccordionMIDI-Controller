"""Core of the controller.

Contains everything a UI should need.
"""


class ControllerCore:
    """Core of the controller."""

    def __init__(self):
        self.modified_keyboards = None

    def apply_keyboard(self, kbd):
        pass

    def send_delete_keyboard(self, kbd):
        pass

    def send_rename_keyboard(self, kbd, new_name):
        pass

    def fetch_keyboards(self, origin):
        pass

