from errors import BaseCustomError


class IncorrectVerificationCodeError(BaseCustomError):
    """
    Exception raised for incorrect verification code input.

    The IncorrectVerificationCodeError class is used to signal that the user
    has entered a wrong verification code.

    It inherits from the BaseCustomError class.

    Attributes
    ----------
    message : str
        Explanation of the error.
    """

    def __init__(self):
        """
        Initialize the IncorrectVerificationCodeError instance with a default message.

        The default message indicates that the user has entered a wrong verification code.
        """
        message = 'Wrong verification code'
        super().__init__(message)
