from errors import BaseCustomError


class UnauthorizedError(BaseCustomError):
    """
    Exception raised for authentication failures.

    The UnauthorizedError class is used to signal that a user is not authenticated.

    It inherits from the BaseCustomError class.

    Attributes
    ----------
    message : str
        Explanation of the error.
    """

    def __init__(self):
        """
        Initializes the UnauthorizedError with a default error message.

        The default message indicates that the user is not authenticated.
        """
        message = 'You are not authenticated'
        super().__init__(message)
