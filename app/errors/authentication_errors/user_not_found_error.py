from errors import BaseCustomError


class UsernameNotFoundError(BaseCustomError):
    def __init__(self, name):
        message = f"Username '{name}' not found"
        super().__init__(message)
