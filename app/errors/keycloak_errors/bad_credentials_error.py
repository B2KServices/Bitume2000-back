from errors import BaseCustomError


class BadCredentialsError(BaseCustomError):
    """
    Exception raised for invalid credentials.

    The BadCredentialsError class is used to signal that the provided credentials
    (e.g., username, password) are invalid or incorrect.

    It inherits from the BaseCustomError class.

    Attributes
    ----------
    message : str
        Explanation of the error, typically indicating why the credentials are considered bad.
    """

    def __init__(self, message: str):
        """
        Initialize the BadCredentialsError instance with a custom error message.

        The error message should provide details about why the credentials failed,
        such as incorrect username, password, or other authentication details.

        Parameters
        ----------
        message : str
            A descriptive message explaining why the credentials are considered bad.
        """
        super().__init__(message)
