from errors.authentication_errors import ForbiddenError, UnauthorizedError


def test_forbidden_error():
    try:
        raise ForbiddenError()
    except ForbiddenError as e:
        assert str(e) == 'You are not authorized to access this resource'


def test_unauthorized_error():
    try:
        raise UnauthorizedError()
    except UnauthorizedError as e:
        assert str(e) == 'You are not authenticated'
