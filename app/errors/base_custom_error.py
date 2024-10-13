class BaseCustomError(Exception):
    """
    Base class for custom exceptions in this application.

    The BaseCustomError class serves as the base class for all custom exceptions
    used within this application.

    It inherits from Python's built-in Exception class.

    Attributes
    ----------
    message : str
        Explanation of the error.
    """

    def __init__(self, *args):
        r"""
        Initialize the BaseCustomError instance with a variable number of arguments.

        The arguments are passed directly to the Exception class constructor
        to allow for flexibility in error message customization.

        Parameters
        ----------
        \*args : tuple
            Any additional arguments passed to the exception.
        """
        super().__init__(*args)
