from errors import BaseCustomError


class UnimplementedError(BaseCustomError):
    """
    Exception raised for unimplemented functionality.

    The UnimplementedError class is used to signal that a specific functionality
    or feature is not yet implemented.

    It inherits from the BaseCustomError class.

    Attributes
    ----------
    message : str
        Explanation of the error, optionally including a description of the
        unimplemented functionality.
    """

    def __init__(self, description: str | None = None):
        """
        Initialize the UnimplementedError instance with an optional description.

        The error message is constructed to include the optional description
        if provided.

        Parameters
        ----------
        description : str, optional
            A description of the unimplemented functionality. If not provided,
            the default message "Not implemented" is used.
        """
        if description is None:
            message = 'Not implemented'
        else:
            message = f'Not implemented: {description}'
        super().__init__(message)
