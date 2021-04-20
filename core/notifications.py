"""Define classes used for notification between objects."""


class Notification:
    """Notify connected callables, optionnaly passing arguments to them.

    Usage:
        >>> update = Notification()
        >>> update.connect(print)
        >>> update("print me")
        print me
    """

    def __init__(self):
        self.call = []

    def __call__(self, *args, **kwargs):
        """
        Call every connected callables.

        Parameters
        ----------
        *args : optional
            Arguments to pas to the callables.
        **kwargs : optional
            Keyword arguments to pass to the callables.

        Returns
        -------
        None.

        """
        for call in self.call:
            call(*args, **kwargs)

    def connect(self, slot):
        """
        Connect a callable to the notification object.

        Parameters
        ----------
        slot : callable
            The callable to connect.

        Returns
        -------
        None.

        """
        self.call.append(slot)