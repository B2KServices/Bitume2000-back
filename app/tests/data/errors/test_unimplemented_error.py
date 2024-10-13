from errors.development_errors import UnimplementedError


def test_unimplemented_error():
    try:
        raise UnimplementedError()
    except UnimplementedError as e:
        assert str(e) == 'Not implemented'


def test_unimplemented_error_on_app(client):
    try:
        raise UnimplementedError('hello_world')
    except UnimplementedError as e:
        assert str(e) == 'Not implemented: hello_world'
