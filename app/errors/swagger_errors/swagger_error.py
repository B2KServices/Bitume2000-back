from errors import BaseCustomError


class InvalidHeaderContentTypeError(BaseCustomError):
    def __init__(self, key: str):
        super().__init__(f'Invalid header content type for : {key} field')


class InvalidBodyContentTypeError(BaseCustomError):
    def __init__(self, key: str = None):
        super().__init__(f'Invalid body content type{f' for : {key} field' if key else ''}')


class InvalidResponseContentTypeError(BaseCustomError):
    def __init__(self, key: str):
        super().__init__(f'Invalid response content type for : {key} field')
