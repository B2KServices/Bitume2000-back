from errors import BaseCustomError


class FileMissingError(BaseCustomError):
    """
    Exception raised when a required file is missing.

    The FileMissingError class is used to signal that a required file is missing.

    It inherits from the BaseCustomError class.

    Attributes
    ----------
    message : str
        Explanation of the error.
    """

    def __init__(self):
        """
        Initialize the FileMissingError instance with a default message.

        The default message indicates that a required file is missing.
        """
        message = 'A file is required'
        super().__init__(message)


class NotAllowedFileExtensionError(BaseCustomError):
    """
    Exception raised when a file has an invalid extension.

    The NotAllowedFileExtensionError class is used to signal that a file has an invalid extension.

    It inherits from the BaseCustomError class.

    Attributes
    ----------
    message : str
        Explanation of the error, including the file name and allowed extensions.
    """

    def __init__(self, file_name: str, allowed_extensions: list[str]):
        """
        Initialize the NotAllowedFileExtensionError instance with the file name and allowed extensions.

        The error message is constructed to include the file name and a list of allowed extensions.

        Parameters
        ----------
        file_name : str
            The name of the file that has an invalid extension.
        allowed_extensions : list of str
            List of allowed file extensions.
        """
        message = (
            f"File '{file_name}' doesn't have the right extension. Allowed extensions are the following: {', '.join(allowed_extensions)}"
        )
        super().__init__(message)


class FileNotAllowedError(BaseCustomError):
    """
    Exception raised when a file is not allowed.

    The FileNotAllowedError class is used to signal that a specific file is not allowed.

    It inherits from the BaseCustomError class.

    Attributes
    ----------
    message : str
        Explanation of the error, including the file name that is not allowed.
    """

    def __init__(self, file_name: str):
        """
        Initialize the FileNotAllowedError instance with the file name that is not allowed.

        The error message is constructed to include the file name.

        Parameters
        ----------
        file_name : str
            The name of the file that is not allowed.
        """
        message = f"File '{file_name}' is not allowed"
        super().__init__(message)


class EmptyCSVFileError(BaseCustomError):
    """
    Exception raised when a CSV file is empty.

    The EmptyCSVFileError class is used to signal that a CSV file is empty.

    It inherits from the BaseCustomError class.

    Attributes
    ----------
    message : str
        Explanation of the error.
    """

    def __init__(self):
        """
        Initialize the EmptyCSVFileError instance with a default message.

        The default message indicates that the CSV file is empty.
        """
        message = 'CSV file is empty'
        super().__init__(message)


class UnEvenCSVFileError(BaseCustomError):
    """
    Exception raised when a CSV file contains lines with different lengths.

    The UnEvenCSVFileError class is used to signal that a CSV file contains lines
    with different lengths, which is unexpected for a properly formatted CSV file.

    It inherits from the BaseCustomError class.

    Attributes
    ----------
    message : str
        Explanation of the error, including the lengths of the lines in the CSV file.
    """

    def __init__(self, lengths: list[int]):
        """
        Initialize the UnEvenCSVFileError instance with the lengths of the lines in the CSV file.

        The error message is constructed to include the lengths of the lines.

        Parameters
        ----------
        lengths : list of int
            List containing the lengths of each line in the CSV file.
        """
        message = f'CSV file contains lines with different length. Lines length: {lengths}'
        super().__init__(message)
