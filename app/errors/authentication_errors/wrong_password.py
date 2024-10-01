from errors import BaseCustomError


class WrongPasswordError(BaseCustomError):
    def __init__(self):
        message = 'Wrong password'
        super().__init__(message)
