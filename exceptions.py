class Impossible(Exception):
    """Exception raised when an action cannot be performed.

    Reason given as the exception message.
    """
    pass


class InstantiationError(Exception):
    """ Exception raised when a class is instantiated poorly. """
    pass
