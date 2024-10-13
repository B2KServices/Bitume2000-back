from errors import BaseCustomError


class ForbiddenError(BaseCustomError):
    """
    Exception raised for access violations.

    The ForbiddenError class is used to signal that a user is not authorized
    to access a specific resource.

    It inherits from the BaseCustomError class.

    Attributes
    ----------
    message : str
        Explanation of the error.
    """

    def __init__(self):
        """
        Initialize the ForbiddenError instance with a default message.

        The default message indicates that the user is not authorized to access the resource.
        """
        message = 'You are not authorized to access this resource'
        super().__init__(message)
